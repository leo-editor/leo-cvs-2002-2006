#@+leo

#@+node:0::@file leoFileCommands.py
#@+body
#@@language python

from leoGlobals import *
from leoUtils import *

import leoDialog,leoNodes
import os,os.path,time,traceback

class BadLeoFile:
	def __init__(self, message):
		self.message = message
	def __str__(self):
		return "Bad Leo File:" + self.message

class fileCommands:

	#@+others
	#@+node:1::leoFileCommands._init_
	#@+body
	def __init__(self,commands):
	
		# trace("__init__", "fileCommands.__init__")
		self.commands = commands
		self.frame = commands.frame
		self.initIvars()
	
	def initIvars(self):
	
		# General
		self.maxTnodeIndex = 0
		self.numberOfTnodes = 0
		self.topVnode = None
		self.mFileName = ""
		self.fileDate = -1
		# For reading
		self.fileFormatNumber = 0
		self.ratio = 0.5
		self.tnodesDict = {}
		self.fileBuffer = None ; self.fileIndex = 0
		self.dummy_v = None
		self.dummy_t = None
		# For writing
		self.read_only = false
		self.outputFile = None # File for normal writing
		self.outputString = None # String for pasting
		self.openDirectory = None
		self.usingClipboard = false
	#@-body
	#@-node:1::leoFileCommands._init_
	#@+node:2::Reading
	#@+node:1::createVnode
	#@+body
	def createVnode(self,parent,back,tref,headline):
	
		# trace(`headline` + ", parent:" + `parent` + ", back:" + `back`)
		v = None ; c = self.commands
		# Shared tnodes are placed in the file even if empty.
		if tref == -1:
			t = leoNodes.tnode()
		else:
			t = self.getT(tref)
			if not t:
				t = self.newTnode(tref)
		if back: # create v after back.
			v = back.insertAfter(t)
		elif parent: # create v as the parent's first child.
			v = parent.insertAsNthChild(0,t)
		else: # create a root vnode
			v = leoNodes.vnode(c, t)
			v.moveToRoot()
			c.tree.rootVnode = v
		v.initHeadString(headline)
		return v
	#@-body
	#@-node:1::createVnode
	#@+node:2::finishPaste (creating join lists could be a problem)
	#@+body
	# This method finishes pasting the outline from the clipboard.
	def finishPaste(self):
	
		c=self.commands
		current = c.currentVnode()
		after = current.nodeAfterTree()
		c.beginUpdate()
		if 1: # inside update...
			if 0: # Warning: this will only join pasted clones, and is very dangerous.
				
				#@<< Create join lists of all pasted vnodes >>
				#@+node:1::<< Create join lists of all pasted vnodes >>
				#@+body
				# Pass 1: create all join lists using tnode::joinHead
				v = c.currentVnode()
				while v and v != after:
					# Put v at the head of t's list of joined vnodes.
					v.setJoinList(v.t.joinHead)
					v.t.setJoinHead(v)
					v = v.threadNext()
					
				# Pass 2: circularize each join list.
				v = c.currentVnode()
				while v and v != after:
					head = v.t.joinHead
					if not head:
						v = v.threadNext() ;continue
					# Make sure we don't handle this list again.
					v.t.setJoinHead(None)
					# Clear the join list if it has only one member.
					if head == v and not v.getJoinList():
						v.setJoinList(None)
						v = v.threadNext() ; continue
					# Point last at the last vnode of the list.
					last = head
					while last and last.getJoinList():
						last = last.getJoinList()
					assert(last)
					# Link last to head.
					last.setJoinList(head)
					v = v.threadNext()
				#@-body
				#@-node:1::<< Create join lists of all pasted vnodes >>

			
			#@<< Recompute clone bits for pasted vnodes >>
			#@+node:2::<< Recompute clone bits for pasted vnodes >>
			#@+body
			#@+at
			#  This must be done after the join lists have been created.  The saved clone bit is unreliable for pasted nodes.

			#@-at
			#@@c
			
			v = c.currentVnode()
			while v and v != after:
				v.initClonedBit(v.shouldBeClone())
				v.clearDirty()
				v = v.threadNext()
			#@-body
			#@-node:2::<< Recompute clone bits for pasted vnodes >>

			self.compactFileIndices()
			c.selectVnode(current)
		c.endUpdate()
		return current
	#@-body
	#@-node:2::finishPaste (creating join lists could be a problem)
	#@+node:3::get routines
	#@+node:1:C=1:get & match (basic)(leoFileCommands)
	#@+body
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
	
	def getTag (self,tag):
		if not self.matchTag(tag):
			print "getTag(", tag, ") failed:"
			raise BadLeoFile("expecting" + tag)
			
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
		# if string.find(self.fileBuffer,tag,i,i+len(tag)) == i:
		if tag == self.fileBuffer[i:i+len(tag)]:
			self.fileIndex += len(tag)
			return true
		else:
			return false
	#@-body
	#@-node:1:C=1:get & match (basic)(leoFileCommands)
	#@+node:2::getClipboardHeader
	#@+body
	def getClipboardHeader (self):
	
		self.getTag("<leo_header")
		# New in version 1.7: fields may appear in any order.
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
	#@-body
	#@-node:2::getClipboardHeader
	#@+node:3::getCloneWindows
	#@+body
	# For compatibility with old file formats.
	
	def getCloneWindows (self):
	
		if self.matchTag("<clone_windows>"):
			while self.matchTag("<clone_window vtag=\"V"):
				self.getLong() ; self.getDquote() ; self.getTag(">")
				self.getTag("<global_window_position")
				self.getPosition()
				self.getTag("/>")
				self.getTag("</clone_window>")
			self.getTag("</clone_windows>")
	#@-body
	#@-node:3::getCloneWindows
	#@+node:4::getEscapedString
	#@+body
	def getEscapedString (self):
	
		# The next '<' begins the ending tag.
		i = self.fileIndex
		self.fileIndex = j = string.find(self.fileBuffer,'<',i)
		if j == -1:
			raise BadLeoFile("unterminated escaped string")
		else:
			# Allocates memory
			return self.xmlUnescape(self.fileBuffer[i:j])
	#@-body
	#@-node:4::getEscapedString
	#@+node:5:C=2:getFindPanelSettings
	#@+body
	def getFindPanelSettings (self):
	
		c = self.commands ; config = app().config
		
		#@<< Set defaults of all flags >>
		#@+node:1::<< Set defaults of all flags >>
		#@+body
		import leoFind
		
		for var in leoFind.ivars:
			exec("c.%s_flag = false" % var)

		#@-body
		#@-node:1::<< Set defaults of all flags >>

		self.getTag("<find_panel_settings")
		while 1:
			if   self.matchTag("batch="): c.batch_flag = self.getDqBool()
			elif self.matchTag("wrap="): c.wrap_flag = self.getDqBool()
			elif self.matchTag("whole_word="): c.whole_word_flag = self.getDqBool()
			elif self.matchTag("ignore_case="): c.ignore_case_flag = self.getDqBool()
			elif self.matchTag("pattern_match="): c.pattern_match_flag = self.getDqBool()
			elif self.matchTag("search_headline="): c.search_headline_flag = self.getDqBool()
			elif self.matchTag("search_body="): c.search_body_flag = self.getDqBool()
			elif self.matchTag("suboutline_only="): c.suboutline_only_flag = self.getDqBool()
			elif self.matchTag("mark_changes="): c.mark_changes_flag = self.getDqBool()
			elif self.matchTag("mark_finds="): c.mark_finds_flag = self.getDqBool()
			elif self.matchTag("reverse="): c.reverse_flag = self.getDqBool()
			else: break
		self.getTag(">")
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
		app().findFrame.init(c)
	#@-body
	#@-node:5:C=2:getFindPanelSettings
	#@+node:6:C=3:getGlobals
	#@+body
	def getGlobals (self):
	
		self.getTag("<globals")
	
		self.getTag("body_outline_ratio=\"")
		self.ratio = self.getDouble() ; self.getDquote() ; self.getTag(">")
	
		self.getTag("<global_window_position")
		y,x,h,w = self.getPosition() ; self.getTag("/>")
		# print ("y,x,h,w:" + `y` + "," + `x` + "," + `h` + "," + `w`)
		
		# Bug fix: 7/15/02: use max, not min!!!
		y = max(y,0) ; x = max(x,0)
		g = "%dx%d%+d%+d" % (w,h,x,y)
		self.frame.top.geometry(g)
		# 7/15/02: Redraw the window before writing into it.
		self.frame.top.deiconify()
		self.frame.top.lift()
		self.frame.top.update()
	
		self.getTag("<global_log_window_position")
		self.getPosition() ; self.getTag("/>") # no longer used.
	
		self.getTag("</globals>")
	#@-body
	#@-node:6:C=3:getGlobals
	#@+node:7:C=4:getLeoFile (Leo2)
	#@+body
	# The caller should enclose this in begin/endUpdate.
	
	def getLeoFile (self,frame,fileName,atFileNodesFlag):
	
		c=self.commands
		
		#@<< warn on read-only files >>
		#@+node:1::<< warn on read-only files >>
		#@+body
		# 8/13/02
		try:
			self.read_only = false
			self.read_only = not os.access(fileName,os.W_OK)
			if self.read_only:
				es("read only: " + fileName)
				d = leoDialog.leoDialog()
				d.askOk(
					"Read-only ouline",
					"Warning: the outline: " + fileName + " is read-only.")
		except:
			if 0: # testing only: access may not exist on all platforms.
				es("exception getting file access")
				traceback.print_exc()
		#@-body
		#@-node:1::<< warn on read-only files >>

			
		self.mFileName = frame.mFileName
		self.tnodesDict = {} ; ok = true
		try:
			c.tree.initing = true # inhibit endEditLabel from marking the file changed.
			self.getXmlVersionTag() # leo.py 3.0
			self.getTag("<leo_file>")
			self.getLeoHeader()
			self.getGlobals()
			self.getPrefs()
			self.getFindPanelSettings()
			c.frame.resizePanesToRatio(self.ratio) # Causes window to appear.
			es("reading: " + fileName)
			self.getVnodes()
			self.getTnodes()
			self.getCloneWindows()
			self.getTag("</leo_file>")
			
			#@<< Create join lists of all vnodes >>
			#@+node:2::<< Create join lists of all vnodes >>
			#@+body
			# Pass 1: create all join lists using the joinHead field in each tnode
			v = c.rootVnode()
			while v:
				v.setJoinList(v.t.joinHead)
				v.t.setJoinHead(v)
				v = v.threadNext()
			
			# Pass 2: Circularize each join list.
			v = c.rootVnode()
			while v:
				head = v.t.joinHead
				if not head:
					v = v.threadNext() ; continue
				# Make sure we don't handle this list again.
				v.t.setJoinHead(None)
				# Clear the join list if it has only one member.
				if head == v and not v.getJoinList():
					v.setJoinList(None)
					v = v.threadNext() ; continue
				# Point last at the last vnode of the list.
				last = head
				while last and last.getJoinList():
					assert(last != last.getJoinList())
					last = last.getJoinList()
				assert(last)
				# Link last to head.
				last.setJoinList(head)
				v = v.threadNext()
			#@-body
			#@-node:2::<< Create join lists of all vnodes >>

		except BadLeoFile, message: # All other exceptions are Leo bugs
			# traceback.print_exc()
			alert(self.mFileName + " is not a valid Leo file: " + `message`)
			ok = false
		# Leo2: read all @file nodes and reset orphan bits.
		if ok and atFileNodesFlag:
			at = c.atFileCommands
			at.readAll(c.rootVnode(), false) # partialFlag
		if not c.tree.currentVnode:
			c.tree.currentVnode = c.tree.rootVnode
		c.selectVnode(c.tree.currentVnode) # load body pane
		c.tree.initing = false # Enable changes in endEditLabel
		self.tnodesDict = {}
		return ok, self.ratio
	#@-body
	#@-node:7:C=4:getLeoFile (Leo2)
	#@+node:8::getLeoHeader
	#@+body
	def getLeoHeader (self):
	
		# Set defaults.
		self.maxTnodeIndex = 0
		self.numberOfTnodes = 0
		self.getTag("<leo_header")
		# New in version 1.7: attributes may appear in any order.
		while 1:
			if self.matchTag("file_format="):
				self.getDquote() ; self.fileFormatNumber = self.getLong() ; self.getDquote()
			elif self.matchTag("tnodes="):
				self.getDquote() ; self.numberOfTnodes = self.getLong() ; self.getDquote()
			elif self.matchTag("max_tnode_index="):
				self.getDquote() ; self.maxTnodeIndex = self.getLong() ; self.getDquote()
			elif self.matchTag("clone_windows="):
				self.getDquote() ; self.getLong() ; self.getDquote() # no longer used.
			else:
				self.getTag("/>")
				break
	#@-body
	#@-node:8::getLeoHeader
	#@+node:9:C=5:getLeoOutline (from clipboard)
	#@+body
	# This method reads a Leo outline from string s in clipboard format.
	def getLeoOutline (self,s):
	
		self.usingClipboard = true
		self.fileBuffer = s ; self.fileIndex = 0
		self.tnodesDict = {}
		try:
			self.getXmlVersionTag() # leo.py 3.0
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
		self.tnodesDict = {}
		self.usingClipboard = false
		return v
	#@-body
	#@-node:9:C=5:getLeoOutline (from clipboard)
	#@+node:10::getPosition
	#@+body
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
	#@-body
	#@-node:10::getPosition
	#@+node:11:C=6:getPrefs
	#@+body
	def getPrefs (self):
	
		c = self.commands ; config = app().config
		
		self.getTag("<preferences")
		while 1:
			if self.matchTag("allow_rich_text="):
				self.getDquote() ; self.getBool() ; self.getDquote() #ignored
			elif self.matchTag("tab_width="):
				self.getDquote() ; c.tab_width = self.getLong() ; self.getDquote()
			elif self.matchTag("page_width="):
				self.getDquote() ; c.page_width = self.getLong() ; self.getDquote()
			elif self.matchTag("tangle_bat="):
				self.getDquote() ; c.tangle_batch_flag = self.getBool() ; self.getDquote()
			elif self.matchTag("untangle_bat="):
				self.getDquote() ; c.untangle_batch_flag = self.getBool() ; self.getDquote()
			# New in version 0.10
			elif self.matchTag("output_doc_chunks="):
				self.getDquote() ; c.output_doc_flag = self.getBool() ; self.getDquote()
			elif self.matchTag("noweb_flag="):
				# New in version 0.19: Ignore this flag.
				self.getDquote() ; self.getBool() ; self.getDquote()
			elif self.matchTag("extended_noweb_flag="):
				# New in version 0.19: Ignore this flag.
				self.getDquote() ; self.getBool() ; self.getDquote()
			elif self.matchTag("defaultTargetLanguage="):
				# New in version 0.15
				self.getDquote()
				
				#@<< check for syntax coloring prefs >>
				#@+node:1:C=7:<< check for syntax coloring prefs >>
				#@+body
				# Must match longer tags before short prefixes.
				language = c_language # default
				
				if self.matchTag("CWEB"):
					language = cweb_language ; self.getDquote();
				elif self.matchTag("C"):
					language = c_language ; self.getDquote()
				elif self.matchTag("HTML"):
					language = html_language ; self.getDquote()
				elif self.matchTag("Java"):
					language = java_language ; self.getDquote()
				elif self.matchTag("LaTeX"):
					language = latex_language ; self.getDquote()
				elif self.matchTag("Pascal"):
					language = pascal_language ; self.getDquote()
				elif self.matchTag("PerlPod"):
					language = perlpod_language ; self.getDquote()
				elif self.matchTag("Perl"):
					language = perl_language ; self.getDquote()
				elif self.matchTag("Plain"):
					language = plain_text_language ; self.getDquote()
				elif self.matchTag("Python"):
					language = python_language ; self.getDquote()
				elif self.matchTag("tcl/tk"):
					language = tcltk_language ; self.getDquote()
					
				# print(`language`)
				
				c.target_language = language
				#@-body
				#@-node:1:C=7:<< check for syntax coloring prefs >>

			elif self.matchTag("use_header_flag="):
				self.getDquote() ; c.use_header_flag = self.getBool() ; self.getDquote()
			else: break
		self.getTag(">")
		while 1:
			if self.matchTag("<defaultDirectory>"):
				# New in version 0.16.
				c.tangle_directory = self.getEscapedString()
				self.getTag("</defaultDirectory>")
				if not os.path.exists(c.tangle_directory):
					es("default tangle directory not found:" + c.tangle_directory)
			elif self.matchTag("<TSyntaxMemo_options>"):
				self.getEscapedString() # ignored
				self.getTag("</TSyntaxMemo_options>")
			else: break
		self.getTag("</preferences>")
		
		# Override .leo file's preferences if settings are in leoConfig.txt.
		if config.configsExist:
			config.setCommandsIvars(c)
	#@-body
	#@-node:11:C=6:getPrefs
	#@+node:12::getSize
	#@+body
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
	#@-body
	#@-node:12::getSize
	#@+node:13::getT
	#@+body
	def getT (self,index):
	
		if self.tnodesDict.has_key(index):
			return self.tnodesDict[index]
		else:
			return None
	#@-body
	#@-node:13::getT
	#@+node:14::getTnode
	#@+body
	def getTnode (self):
	
		# we have already matched <t.
		index = -1
		# New in version 1.7: attributes may appear in any order.
		while 1:
			if self.matchTag("tx=\"T"):
				index = self.getIndex() ; self.getDquote()
			elif self.matchTag("rtf=\"1\""): pass # ignored
			elif self.matchTag("rtf=\"0\""): pass # ignored
			else: break
		self.getTag(">")
		t = self.getT(index)
		if t:
			s = self.getEscapedString()
			t.setTnodeText(s)
		else: # No vnode refers to this tnode.
			es("no tnode with index: " + `index` + ".  The text will be discarded")
			self.getEscapedString()
		self.getTag("</t>")
	#@-body
	#@-node:14::getTnode
	#@+node:15::getTnodes
	#@+body
	def getTnodes (self):
	
		if self.matchTag("<tnodes>"):
			while self.matchTag("<t"):
				self.getTnode()
			self.getTag("</tnodes>")
	#@-body
	#@-node:15::getTnodes
	#@+node:16::getVnode (Leo2)
	#@+body
	def getVnode (self,parent,back):
	
		# trace("parent:" + `parent` + ", back:" + `back`)
		c=self.commands
		# Create a single dummy vnode to carry status bits.
		if not self.dummy_v:
			self.dummy_t = leoNodes.tnode(0,"")
			self.dummy_v = leoNodes.vnode(c, self.dummy_t)
			self.dummy_v.initHeadString("dummy")
		self.dummy_v.statusBits=0
		currentVnodeFlag = false # true if the 'V' attribute seen.
		topVnodeFlag = false # true if 'T' attribute seen.
		tref = -1 ; headline = ""
		# we have already matched <v.
		while 1:
			if self.matchTag("t=\"T"):
				tref = self.getIndex() ; self.getDquote()
			elif self.matchTag("vtag=\"V"):
				self.getIndex() ; self.getDquote() # ignored
			elif self.matchTag("a=\""):
				
				#@<< Handle vnode attribute bits >>
				#@+node:1::<< Handle vnode attribute bits  >>
				#@+body
				# The a=" has already been seen.
				while 1:
					if   self.matchChar('C'): self.dummy_v.initClonedBit(true)
					elif self.matchChar('D'): pass # no longer used.
					elif self.matchChar('E'): self.dummy_v.initExpandedBit()
					elif self.matchChar('M'): self.dummy_v.initMarkedBit()
					elif self.matchChar('O'): self.dummy_v.setOrphan()
					elif self.matchChar('T'): topVnodeFlag = true
					elif self.matchChar('V'): currentVnodeFlag = true
					else: break
				self.getDquote()
				#@-body
				#@-node:1::<< Handle vnode attribute bits  >>

			else: break
		self.getTag(">")
		# Leo2: headlines are optional.
		if self.matchTag("<vh>"):
			headline = self.getEscapedString() ; self.getTag("</vh>")
		# Link v into the outline using parent and back.
		v = self.createVnode(parent,back,tref,headline)
		v.statusBits = self.dummy_v.statusBits
		# Remember various info that may have been specified.
		if currentVnodeFlag:
			c.tree.currentVnode = v
		if topVnodeFlag: c.mTopVnode = v
		# Recursively create all nested nodes.
		parent = v ; back = None
		while self.matchTag("<v"):
			back = self.getVnode(parent,back)
		# End this vnode.
		self.getTag("</v>")
		return v
	#@-body
	#@-node:16::getVnode (Leo2)
	#@+node:17::getVnodes
	#@+body
	def getVnodes (self):
	
		c=self.commands
		if  self.usingClipboard:
			# Paste after the current vnode.
			back = c.currentVnode() ; parent = back.parent()
		else:
			back = None ; parent = None
	
		self.getTag("<vnodes>")
		while self.matchTag("<v"):
			back = self.getVnode(parent,back)
		self.getTag("</vnodes>")
	#@-body
	#@-node:17::getVnodes
	#@+node:18:C=8:getXmlVersionTag
	#@+body
	#@+at
	#  Parses the xml version string, and sets the xml version string.
	# 
	# For example, given: <?xml version="1.0" encoding="UTF-8"?>
	# the version string is the string UTF-8 (without the quotes)

	#@-at
	#@@c
	
	def getXmlVersionTag (self):
		
		config = app().config
		self.getTag(prolog_prefix_string)
		version = self.getDqString()
		# config.version overrides the version in the .leo file.
		if not config.xml_version_string:
			config.xml_version_string = version
		self.getTag(prolog_postfix_string)

	#@-body
	#@-node:18:C=8:getXmlVersionTag
	#@+node:19::skipWs
	#@+body
	def skipWs (self):
	
		while self.fileIndex < len(self.fileBuffer):
			ch = self.fileBuffer[self.fileIndex]
			if ch == ' ' or ch == '\t':
				self.fileIndex += 1
			else: break
	
		# The caller is entitled to get the next character.
		if  self.fileIndex >= len(self.fileBuffer):
			raise BadLeoFile("")
	#@-body
	#@-node:19::skipWs
	#@+node:20::skipWsAndNl
	#@+body
	def skipWsAndNl (self):
	
		while self.fileIndex < len(self.fileBuffer):
			ch = self.fileBuffer[self.fileIndex]
			if ch == ' ' or ch == '\t' or ch == '\r' or ch == '\n':
				self.fileIndex += 1
			else: break
	
		# The caller is entitled to get the next character.
		if  self.fileIndex >= len(self.fileBuffer):
			raise BadLeoFile("")
	#@-body
	#@-node:20::skipWsAndNl
	#@-node:3::get routines
	#@+node:4::newTnode
	#@+body
	def newTnode(self,index):
	
		if self.tnodesDict.has_key(index):
			es("bad tnode index: " + `index` + ". Using empty text.")
			return leoNodes.tnode()
		else:
			t = leoNodes.tnode()
			t.setFileIndex(index)
			self.tnodesDict[index] = t
			return t
	#@-body
	#@-node:4::newTnode
	#@+node:5::readAtFileNodes
	#@+body
	def readAtFileNodes (self):
	
		c = self.commands
		c.atFileCommands.readAll(c.currentVnode(), true) # partialFlag
	#@-body
	#@-node:5::readAtFileNodes
	#@+node:6:C=9:fileCommands.readOutlineOnly
	#@+body
	def readOutlineOnly (self,file,fileName):
	
		c=self.commands
		# Read the entire file into the buffer
		self.fileBuffer = file.read() ; file.close()
		self.fileIndex = 0
		
		#@<< Set the default directory >>
		#@+node:1:C=10:<< Set the default directory >>
		#@+body
		#@+at
		#  The most natural default directory is the directory containing the .leo file that we are about to open.  If the user 
		# has specified the "Default Directory" preference that will over-ride what we are about to set.

		#@-at
		#@@c
		
		dir = os.path.dirname(fileName) 
		if len(dir) > 0:
			c.openDirectory = dir
		#@-body
		#@-node:1:C=10:<< Set the default directory >>

		c.beginUpdate()
		ok, ratio = self.getLeoFile(self.frame,fileName,false) # readAtFileNodes
		c.endUpdate()
		c.frame.top.deiconify()
		c.setChanged(false)
		c.frame.resizePanesToRatio(ratio)
		# This should be done after the pane size has been set.
		if 0: # This can not be done at present.
			if self.topVnode:
				c.tree.scrollTo(self.topVnode)
				c.tree.Refresh()
		# delete the file buffer
		self.fileBuffer = ""
		return ok
	#@-body
	#@-node:6:C=9:fileCommands.readOutlineOnly
	#@+node:7:C=11:fileCommands.open
	#@+body
	def open(self,file,fileName):
	
		c=self.commands
		# Read the entire file into the buffer
		# t = getTime()
		self.fileBuffer = file.read() ; file.close()
		self.fileIndex = 0
		
		#@<< Set the default directory >>
		#@+node:1:C=10:<< Set the default directory >>
		#@+body
		#@+at
		#  The most natural default directory is the directory containing the .leo file that we are about to open.  If the user 
		# has specified the "Default Directory" preference that will over-ride what we are about to set.

		#@-at
		#@@c
		
		dir = os.path.dirname(fileName) 
		if len(dir) > 0:
			c.openDirectory = dir
		#@-body
		#@-node:1:C=10:<< Set the default directory >>

		# esDiffTime("open:read all", t)
	
		c.beginUpdate()
		if 1: # inside update...
			c.loading = true # disable c.changed
			ok, ratio = self.getLeoFile(self.frame,fileName,true) # readAtFileNodes
			c.loading = false # reenable c.changed
			c.setChanged(false)
			# This should be done after the pane size has been set.
			top = c.tree.topVnode
			if 0: # This can't be done directly.
				if top: c.tree.scrollTo(top)
		c.endUpdate()
		# delete the file buffer
		self.fileBuffer = ""
		# esDiffTime("open: exit",t)
		return ok
	#@-body
	#@-node:7:C=11:fileCommands.open
	#@+node:8::xmlUnescape
	#@+body
	def xmlUnescape(self,s):
	
		if s:
			s = string.replace(s, '\r', '')
			s = string.replace(s, "&lt;", '<')
			s = string.replace(s, "&gt;", '>')
			s = string.replace(s, "&amp;", '&')
		return s
	#@-body
	#@-node:8::xmlUnescape
	#@-node:2::Reading
	#@+node:3::Writing
	#@+node:1::assignFileIndices
	#@+body
	def assignFileIndices (self):
	
		c=self.commands ; v = c.rootVnode()
		while v:
			t = v.t
			# 8/28/99.  Write shared tnodes even if they are empty.
			if t.hasBody() or v.getJoinList():
				if t.fileIndex == 0:
					self.maxTnodeIndex += 1
					t.setFileIndex(self.maxTnodeIndex)
			else:
				t.setFileIndex(0)
			v = v.threadNext()
	#@-body
	#@-node:1::assignFileIndices
	#@+node:2::compactFileIndices
	#@+body
	def compactFileIndices (self):
	
		c = self.commands ; v = c.rootVnode()
		self.maxTnodeIndex = 0
		while v: # Clear all indices.
			v.t.setFileIndex(0)
			v = v.threadNext()
		v = c.rootVnode()
		while v: # Set indices for all tnodes that will be written.
			t = v.t
			if t.hasBody() or v.getJoinList(): # 8/28/99. Write shared tnodes even if they are empty.
				if t.fileIndex == 0:
					self.maxTnodeIndex += 1
					t.setFileIndex(self.maxTnodeIndex)
			v = v.threadNext()
	#@-body
	#@-node:2::compactFileIndices
	#@+node:3::shouldCompactOnSave
	#@+body
	#@+at
	#  This method sets policy for when we should compact a file before doing a Save Command.

	#@-at
	#@@c
	
	def shouldCompactOnSave (self):
	
		c=self.commands
		# Count the number of tnodes used
		c.clearAllVisited()
		v = c.rootVnode() ; tnodesUsed = 0
		while v:
			t = v.t
			if t and not t.isVisited():
				tnodesUsed += 1
				t.setVisited()
			v = v.threadNext()
		tnodesUnused = self.maxTnodeIndex - tnodesUsed
		return tnodesUnused > 100
	#@-body
	#@-node:3::shouldCompactOnSave
	#@+node:4::put routines
	#@+node:1::putClipboardHeader
	#@+body
	def putClipboardHeader (self):
	
		tnodes = 0
		
		#@<< count the number of tnodes >>
		#@+node:1::<< count the number of tnodes >>
		#@+body
		c=self.commands
		c.clearAllVisited()
		
		# Count the vnode and tnodes.
		v = c.currentVnode()
		after = v.nodeAfterTree()
		while v and v != after:
			t = v.t
			if t and not t.isVisited() and (t.hasBody() or v.getJoinList()):
				t.setVisited()
				tnodes += 1
			v = v.threadNext()
		#@-body
		#@-node:1::<< count the number of tnodes >>

		self.put('<leo_header file_format="1" tnodes=')
		self.put_in_dquotes(`tnodes`)
		self.put(" max_tnode_index=")
		self.put_in_dquotes(`tnodes`)
		self.put("/>") ; self.put_nl()
	#@-body
	#@-node:1::putClipboardHeader
	#@+node:2:C=12:put (basic)(leoFileCommands)
	#@+body
	# All output eventually comes here.
	def put (self,s):
		if s and len(s) > 0:
			if self.outputFile: # Write to a file
				try:
					try:
						self.outputFile.write(s)
					except UnicodeError:
						xml_encoding = app().config.xml_version_string
						s = s.encode(xml_encoding)
						self.outputFile.write(s)
				except:
					traceback.print_exc()
					es("exception writing:" + `s`)
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
	#@-body
	#@-node:2:C=12:put (basic)(leoFileCommands)
	#@+node:3::putEscapedString
	#@+body
	#@+at
	#  Surprisingly, the call to xmlEscape here is _much_ faster than calling put for each characters of s.

	#@-at
	#@@c
	
	def putEscapedString (self,s):
	
		if s and len(s) > 0:
			self.put(self.xmlEscape(s))
	#@-body
	#@-node:3::putEscapedString
	#@+node:4:C=13:putFindSettings
	#@+body
	def putFindSettings (self):
	
		c = self.commands ; config = app().config
	
		self.put("<find_panel_settings")
		
		
		#@<< put find settings that may exist in leoConfig.txt >>
		#@+node:1::<< put find settings that may exist in leoConfig.txt >>
		#@+body
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
		#@-body
		#@-node:1::<< put find settings that may exist in leoConfig.txt >>

		
		self.put("</find_panel_settings>") ; self.put_nl()
	#@-body
	#@-node:4:C=13:putFindSettings
	#@+node:5::putGlobals
	#@+body
	def putGlobals (self):
	
		c=self.commands
		self.put("<globals")
		
		#@<< put the body/outline ratio >>
		#@+node:1::<< put the body/outline ratio >>
		#@+body
		# Puts an innumerate number of digits
		
		self.put(" body_outline_ratio=") ; self.put_in_dquotes(`c.frame.ratio`)
		#@-body
		#@-node:1::<< put the body/outline ratio >>

		self.put(">") ; self.put_nl()
		
		#@<< put the position of this frame >>
		#@+node:2:C=14:<< put the position of this frame >>
		#@+body
		width,height,left,top = get_window_info(self.frame.top)
		# print ("t,l,h,w:" + `top` + ":" + `left` + ":" + `height` + ":" + `width`)
		
		self.put_tab()
		self.put("<global_window_position")
		self.put(" top=") ; self.put_in_dquotes(`top`)
		self.put(" left=") ; self.put_in_dquotes(`left`)
		self.put(" height=") ; self.put_in_dquotes(`height`)
		self.put(" width=") ; self.put_in_dquotes(`width`)
		self.put("/>") ; self.put_nl()
		#@-body
		#@-node:2:C=14:<< put the position of this frame >>

		
		#@<< put the position of the log window >>
		#@+node:3::<< put the position of the log window >>
		#@+body
		top = left = height = width = 0 # no longer used
		self.put_tab()
		self.put("<global_log_window_position")
		self.put(" top=") ; self.put_in_dquotes(`top`)
		self.put(" left=") ; self.put_in_dquotes(`left`)
		self.put(" height=") ; self.put_in_dquotes(`height`)
		self.put(" width=") ; self.put_in_dquotes(`width`)
		self.put("/>") ; self.put_nl()
		#@-body
		#@-node:3::<< put the position of the log window >>

		self.put("</globals>") ; self.put_nl()
	#@-body
	#@-node:5::putGlobals
	#@+node:6::putHeader
	#@+body
	def putHeader (self):
	
		tnodes = 0 ; clone_windows = 0 # Always zero in Leo2.
	
		self.put("<leo_header")
		self.put(" file_format=") ; self.put_in_dquotes("2")
		self.put(" tnodes=") ; self.put_in_dquotes(`tnodes`)
		self.put(" max_tnode_index=") ; self.put_in_dquotes(`self.maxTnodeIndex`)
		self.put(" clone_windows=") ; self.put_in_dquotes(`clone_windows`)
		self.put("/>") ; self.put_nl()
	#@-body
	#@-node:6::putHeader
	#@+node:7::putLeoOutline (to clipboard)
	#@+body
	# Writes a Leo outline to s in a format suitable for pasting to the clipboard.
	
	def putLeoOutline (self):
	
		self.outputString = "" ; self.outputFile = None
		self.usingClipboard = true
		# self.assignFileIndices() // The caller does this.
		self.putProlog()
		self.putClipboardHeader()
		self.putVnodes()
		self.putTnodes()
		self.putPostlog()
		s = self.outputString
		self.outputString = None
		self.usingClipboard = false
		return s
	#@-body
	#@-node:7::putLeoOutline (to clipboard)
	#@+node:8:C=15:putPrefs
	#@+body
	def putPrefs (self):
	
		c = self.commands ; config = app().config
	
		self.put("<preferences")
		self.put(" allow_rich_text=") ; self.put_dquoted_bool(0) # no longer used
		
		
		#@<< put prefs that may exist in leoConfig.txt >>
		#@+node:1::<< put prefs that may exist in leoConfig.txt >>
		#@+body
		dict = config.languageNameDict
		
		if c.target_language and dict.has_key(c.target_language):
			language = dict[c.target_language]
		else:
			language = "Plain"
		
		if config.configsExist and not config.read_only: # 8/6/02
			pass # config.update has already been called.
		else:
			self.put(" tab_width=") ; self.put_in_dquotes(`c.tab_width`)
			self.put(" page_width=") ; self.put_in_dquotes(`c.page_width`)
			self.put(" tangle_bat=") ; self.put_dquoted_bool(c.tangle_batch_flag)
			self.put(" untangle_bat=") ; self.put_dquoted_bool(c.untangle_batch_flag)
			self.put(" output_doc_chunks=") ; self.put_dquoted_bool(c.output_doc_flag)
			self.put(" use_header_flag=") ; self.put_dquoted_bool(c.use_header_flag)
			self.put(" defaultTargetLanguage=") ; self.put_in_dquotes(language)
		
		self.put(">") ; self.put_nl()
		# New in version 0.16
		
		#@<< put default directory >>
		#@+node:1::<< put default directory >>
		#@+body
		if config.configsExist:
			pass # Has been done earlier.
		elif len(c.tangle_directory) > 0:
			self.put_tab()
			self.put("<defaultDirectory>")
			self.putEscapedString(c.tangle_directory)
			self.put("</defaultDirectory>")
			self.put_nl()
		#@-body
		#@-node:1::<< put default directory >>
		#@-body
		#@-node:1::<< put prefs that may exist in leoConfig.txt >>

		
		self.put("</preferences>") ; self.put_nl()
	#@-body
	#@-node:8:C=15:putPrefs
	#@+node:9:C=16:putProlog
	#@+body
	def putProlog (self):
	
		if 0: # leo.py 2.x code
			self.put(prolog_string) ; self.put_nl()
			# internal or external DTD goes here
			self.put("<leo_file>") ; self.put_nl()
		else: # leo.py 3.x code
			config = app().config
			version = config.xml_version_string
			if not version or len(version) == 0:
				# This is used only for new files without leoConfig.txt.
				if 0: # "UTF-8"
					version = prolog_version_string1 # leo.py 2.x
				else: # "ISO-8859-1"
					version = prolog_version_string2 # leo.py 3.0
			self.put(prolog_prefix_string) ; self.put_dquote()
			self.put(version) ; self.put_dquote()
			self.put(prolog_postfix_string) ; self.put_nl()
			self.put("<leo_file>") ; self.put_nl()

	#@-body
	#@-node:9:C=16:putProlog
	#@+node:10::putPostlog
	#@+body
	def putPostlog (self):
	
		self.put("</leo_file>") ; self.put_nl()
	#@-body
	#@-node:10::putPostlog
	#@+node:11::putTnodes (Leo2)
	#@+body
	#@+at
	#  This method puts all tnodes in index order.  All tnode indices must have been assigned at this point.

	#@-at
	#@@c
	def putTnodes (self):
	
		c=self.commands
		tnodes = {}
		if self.usingClipboard: # write the current tree.
			v = c.currentVnode() ; after = v.nodeAfterTree()
		else: # write everything
			v = c.rootVnode() ; after = None
		# Populate tnodes
		while v and v != after:
			index = v.t.fileIndex
			if index > 0 and not tnodes.has_key(index):
				tnodes[index] = v.t
			v = v.threadNext()
		# Put all tnodes in index order.
		self.put("<tnodes>") ; self.put_nl()
		#
		keys = tnodes.keys() ; keys.sort()
		for index in keys:
			t = tnodes[index]
			assert(t)
			# New for Leo2: write only those tnodes whose vnodes were written.
			if t.isVisited(): self.putTnode(t)
		#
		self.put("</tnodes>") ; self.put_nl()
	#@-body
	#@-node:11::putTnodes (Leo2)
	#@+node:12::putTnode
	#@+body
	def putTnode (self,t):
	
		self.put("<t tx=") ; self.put_in_dquotes("T" + `t.fileIndex`)
		self.put(">")
		if t and t.bodyString and len(t.bodyString) > 0:
			self.putEscapedString(t.bodyString)
		self.put("</t>") ; self.put_nl()
	#@-body
	#@-node:12::putTnode
	#@+node:13::putVnodes (Leo2)
	#@+body
	#@+at
	#  This method puts all vnodes by starting the recursion.  putVnode will write all vnodes in the order in which they appear in 
	# the outline.

	#@-at
	#@@c
	def putVnodes (self):
	
		c=self.commands
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
					c.tree.topVnode) # Write the top-vnode status bit.
				v = v.next()
		self.put("</vnodes>") ; self.put_nl()
	#@-body
	#@-node:13::putVnodes (Leo2)
	#@+node:14::putVnode (Leo2)
	#@+body
	#@+at
	#  This writes full headline and body text for all vnodes, even orphan and @ignored nodes.  This allows all Leo outlines to be 
	# used as backup files.

	#@-at
	#@@c
	
	def putVnode (self,v,topVnode):
	
		c = self.commands
		self.put("<v")
		
		#@<< Put tnode index if this vnode has body text >>
		#@+node:1::<< Put tnode index if this vnode has body text >>
		#@+body
		t = v.t
		if t and (t.hasBody() or v.getJoinList()):
			if t.fileIndex > 0:
				self.put(" t=") ; self.put_in_dquotes("T" + `t.fileIndex`)
				v.t.setVisited() # Indicate we wrote the body text.
			else:
				es("error writing file(bad vnode)!")
				es("try using the Save To command")
		#@-body
		#@-node:1::<< Put tnode index if this vnode has body text >>

		
		#@<< Put attribute bits >>
		#@+node:2::<< Put attribute bits >>
		#@+body
		# Dummy vnodes carry all attributes.
		current = c.currentVnode()
		top = topVnode
		if ( v.isCloned() or v.isExpanded() or v.isMarked() or
			v == current or v == top ):
			self.put(" a=") ; self.put_dquote()
			if v.isCloned(): self.put("C")
			if v.isExpanded(): self.put("E")
			if v.isMarked(): self.put("M")
			if v.isOrphan(): self.put("O")
			if v == top: self.put("T")
			if v == current: self.put("V")
			self.put_dquote()
		#@-body
		#@-node:2::<< Put attribute bits >>

		self.put(">")
		
		#@<< write the head text >>
		#@+node:3::<< write the head text >>
		#@+body
		headString = v.headString()
		if len(headString) > 0:
			self.put("<vh>")
			self.putEscapedString(headString)
			self.put("</vh>")
		#@-body
		#@-node:3::<< write the head text >>

		child = v.firstChild()
		if child:
			self.put_nl()
			while child:
				self.putVnode(child,topVnode)
				child = child.next()
		self.put("</v>") ; self.put_nl()
	#@-body
	#@-node:14::putVnode (Leo2)
	#@-node:4::put routines
	#@+node:5:C=17:save
	#@+body
	def save(self,fileName):
	
		c=self.commands
		c.beginUpdate()
		if 1: # within update...
			c.endEditing()# Set the current headline text.
			self.compactFileIndices() # 1/14/02: always recompute file indices
			
			#@<< Set the default directory for new files >>
			#@+node:1::<< Set the default directory for new files >>
			#@+body
			# 8/13/02: Set c.openDirectory for new files for the benefit of leoAtFile.scanAllDirectives.
			
			if not c.openDirectory or len(c.openDirectory) == 0:
				dir = os.path.dirname(fileName) 
				if len(dir) > 0 and os.path.isabs(fileName) and os.path.exists(fileName):
					c.openDirectory = dir
			#@-body
			#@-node:1::<< Set the default directory for new files >>

			if self.write_LEO_file(fileName,false): # outlineOnlyFlag
				c.setChanged(false) # Clears all dirty bits.
				es("saved: " + shortFileName(fileName))
				if app().config.save_clears_undo_buffer:
					es("clearing undo")
					c.undoer.clearUndoState()
		c.endUpdate()
	#@-body
	#@-node:5:C=17:save
	#@+node:6::saveAs
	#@+body
	def saveAs(self,fileName):
	
		c=self.commands
		c.beginUpdate()
		if 1: # within update...
			c.endEditing() # Set the current headline text.
			self.compactFileIndices()
			if self.write_LEO_file(fileName,false): # outlineOnlyFlag
				c.setChanged(false) # Clears all dirty bits.
				es("saved: " + shortFileName(fileName))
		c.endUpdate()
	#@-body
	#@-node:6::saveAs
	#@+node:7::saveTo
	#@+body
	def saveTo (self,fileName):
	
		c=self.commands
		c.beginUpdate()
		if 1: # within update...
			c.endEditing()# Set the current headline text.
			self.compactFileIndices()
			if self.write_LEO_file(fileName,false): # outlineOnlyFlag
				es("saved: " + shortFileName(fileName))
		c.endUpdate()
	#@-body
	#@-node:7::saveTo
	#@+node:8::xmlEscape
	#@+body
	# Surprisingly, this is a time critical routine.
	
	def xmlEscape(self,s):
	
		assert(s and len(s) > 0) # check is made in putEscapedString
		s = string.replace(s, '\r', '')
		s = string.replace(s, '&', "&amp;")
		s = string.replace(s, '<', "&lt;")
		s = string.replace(s, '>', "&gt;")
		return s
	#@-body
	#@-node:8::xmlEscape
	#@+node:9::writeAtFileNodes
	#@+body
	def writeAtFileNodes (self):
	
		c = self.commands ; v = c.currentVnode()
		if v:
			at = c.atFileCommands
			at.writeAll(v,true) # partialFlag
	#@-body
	#@-node:9::writeAtFileNodes
	#@+node:10::writeOutlineOnly
	#@+body
	def writeOutlineOnly (self):
	
		c=self.commands
		c.endEditing()
		self.compactFileIndices()
		self.write_LEO_file(self.mFileName,true) # outlineOnlyFlag
	#@-body
	#@-node:10::writeOutlineOnly
	#@+node:11:C=18:write_LEO_file
	#@+body
	def write_LEO_file(self,fileName,outlineOnlyFlag):
	
		c=self.commands ; config = app().config
		
		if not outlineOnlyFlag:
			try:
				# Leo2: write all @file nodes and set orphan bits.
				at = c.atFileCommands
				at.writeAll(c.rootVnode(), false) # forceFlag
			except:
				es("exception writing derived files")
				traceback.print_exc()
				return false
				
		if self.read_only:
			es("read only: " + fileName)
			return false
	
		try:
			
			#@<< create backup file >>
			#@+node:1:C=19:<< create backup file >>
			#@+body
			# rename fileName to fileName.bak if fileName exists.
			if os.path.exists(fileName):
				try:
					backupName = os.path.join(app().loadDir,fileName)
					backupName = fileName + ".bak"
					if os.path.exists(backupName):
						os.unlink(backupName)
					# os.rename(fileName,backupName)
					utils_rename(fileName,backupName)
				except:
					es("exception creating " + backupName)
					traceback.print_exc()
					backupName = None
			else:
				backupName = None
			#@-body
			#@-node:1:C=19:<< create backup file >>

			self.mFileName = fileName
			self.outputFile = open(fileName, 'w')
			if not self.outputFile:
				es("can not open " + fileName)
				
				#@<< delete backup file >>
				#@+node:2::<< delete backup file >>
				#@+body
				if backupName and os.path.exists(backupName):
					try:
						os.unlink(backupName)
					except:
						es("exception deleting " + backupName)
						traceback.print_exc()

				#@-body
				#@-node:2::<< delete backup file >>

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
			traceback.print_exc() 
			if self.outputFile:
				try:
					self.outputFile.close()
					self.outputFile = None
				except:
					es("exception closing: " + fileName)
					traceback.print_exc()
			
			#@<< erase filename and rename backupName to fileName >>
			#@+node:3:C=20:<< erase filename and rename backupName to fileName >>
			#@+body
			es("error writing " + fileName)
			
			if fileName and os.path.exists(fileName):
				try:
					os.unlink(fileName)
				except:
					es("exception deleting " + fileName)
					traceback.print_exc()
					
			if backupName:
				es("restoring " + fileName + " from " + backupName)
				try:
					# os.rename(backupName, fileName)
					utils_rename(backupName, fileName)
				except:
					es("exception renaming " + backupName + " to " + fileName)
					traceback.print_exc()

			#@-body
			#@-node:3:C=20:<< erase filename and rename backupName to fileName >>

			return false
	
		if self.outputFile:
			try:
				self.outputFile.close()
				self.outputFile = None
			except:
				es("exception closing: " + fileName)
				traceback.print_exc()
			
			#@<< delete backup file >>
			#@+node:2::<< delete backup file >>
			#@+body
			if backupName and os.path.exists(backupName):
				try:
					os.unlink(backupName)
				except:
					es("exception deleting " + backupName)
					traceback.print_exc()

			#@-body
			#@-node:2::<< delete backup file >>

			return true
		else: # This probably will never happen because errors should raise exceptions.
			
			#@<< erase filename and rename backupName to fileName >>
			#@+node:3:C=20:<< erase filename and rename backupName to fileName >>
			#@+body
			es("error writing " + fileName)
			
			if fileName and os.path.exists(fileName):
				try:
					os.unlink(fileName)
				except:
					es("exception deleting " + fileName)
					traceback.print_exc()
					
			if backupName:
				es("restoring " + fileName + " from " + backupName)
				try:
					# os.rename(backupName, fileName)
					utils_rename(backupName, fileName)
				except:
					es("exception renaming " + backupName + " to " + fileName)
					traceback.print_exc()

			#@-body
			#@-node:3:C=20:<< erase filename and rename backupName to fileName >>

			return false
	#@-body
	#@-node:11:C=18:write_LEO_file
	#@-node:3::Writing
	#@-others
#@-body
#@-node:0::@file leoFileCommands.py
#@-leo
