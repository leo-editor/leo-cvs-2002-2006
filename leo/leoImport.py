#@+leo

#@+node:0::@file leoImport.py
#@+body
from leoGlobals import *
from leoUtils import *

indent_refs = true ; dont_indent_refs = false

class leoImportCommands:

	#@+others
	#@+node:1::is... methods
	#@+body
	def isCodeStart(self,s,i):  return match(s,i,"@c") or match(s,i,"@p")
	def isMacroStart(self,s,i): return match(s,i,"@d") or match(s,i,"@f")
	def isTeXStart(self,s,i):   return match(s,i,"@ ") or match(s,i,"@*")
	
	def isModuleStart(self,s,i):
		return self.isCodeStart(s,i) or self.isMacroStart(s,i) or self.isTeXStart(s,i)
			
	def isAtAt(self,s,i):       return match(s,i,"@@")
	def isNameStart(self,s,i):  return match(s,i,"@<")
	def isNameEnd(self,s,i):    return match(s,i,"@>")
	#@-body
	#@-node:1::is... methods
	#@+node:2::error
	#@+body
	def error (self,s): es(s)
	#@-body
	#@-node:2::error
	#@+node:3::import.__init__ (new)
	#@+body
	def __init__ (self,commands):
	
		self.commands = commands
		
		#@<< initialize importFiles ivars >>
		#@+node:1::<< initialize importFiles ivars >>
		#@+body
		self.fileName = None # The original file name, say x.cpp
		self.methodName = None # x, as in < < x methods > > =
		self.fileType = None
		
		# These mark the points in the present function.
		self.scan_start = 0 # The start of the unscanned text.
		self.function_start = None
		self.function_end = None
		self.name_start = None
		self.name_end = None
		
		# Used by CWEBtoOutline
		self.cweb_st = None
		#@-body
		#@-node:1::<< initialize importFiles ivars >>
	#@-body
	#@-node:3::import.__init__ (new)
	#@+node:4::Top Level
	#@+node:1::CWEBToOutline
	#@+node:1::createCWEBHeadline
	#@+body
	def createCWEBHeadline (self,parent,headline,body):
	
		# Create the vnode.
		v = parent.insertAsLastChild()
		v.initHeadString(headline)
		# Attach the body text.
		v.t.setTnodeText(body)
		v.t.setSelection(0,0)
	#@-body
	#@-node:1::createCWEBHeadline
	#@+node:2::createHeadlineFromBody
	#@+body
	#@+at
	#  This method determines the proper headline text. If the body text contains a section definition the headline becomes the 
	# corresponding section reference. Otherwise,if the body text contains @c the headline becomes the function name that is 
	# presumed to follow the @c. Otherwise,if the body text contains @d name the headline becomes @d name. Otherwise,the headline 
	# is simply "code"

	#@-at
	#@@c
	
	def createHeadlineFromBody (self,s):
		
		macro_start = macro_end = None
		
		#@<< Scan for a section definition,@d or @c >>
		#@+node:1::<< Scan for a section definition, @d or @c >>
		#@+body
		i = 0
		while i < len(s):
			start = end = None
			i = skip_ws_and_nl(s,i)
			# Allow constructs such as @ @c
			if self.isTeXStart(s,i):
				i += 2
			if not macro_start and self.isMacroStart(s,i):
				
				#@<< set macro_start and macro_end >>
				#@+node:1::<< set macro_start and macro_end >>
				#@+body
				macro_start = i # Remember the @d or @f
				i += 2
				# Scan past the first identifier.
				i = skip_ws(s,i)
				while i < len(s) and is_c_id(s[i]):
					i += 1
				macro_end = i
				#@-body
				#@-node:1::<< set macro_start and macro_end >>

			elif self.isCodeStart(s,i):
				
				#@<< Return the function name >>
				#@+node:2::<< Return the function name >>
				#@+body
				i += 2 # Skip the @c or @p
				while i < len(s):
					i = skip_ws_and_nl(s,i)
					if i < len(s) and (s[i]=='_' or s[i] in string.letters):
						start = i
						while i < len(s) and is_c_id(s[i]):
							i += 1
						end = i
					elif i < len(s) and s[i] == '(' and start:
						return s[start:end]
					else: i += 1
				return "outer function"
				#@-body
				#@-node:2::<< Return the function name >>

			elif self.isNameStart(s,i):
				start = i ; i += 2
				while i < len(s) and not self.isNameEnd(s,i) and not is_nl(s,i):
					i += 1
				if self.isNameEnd(s,i):
					i += 2 ; end = i
					i = skip_ws(s,i)
					if match(s,i,"+=") or match(s,i,"="):
						# Set the headline to the section reference.
						return s[start:end]
			else: i = skip_line(s,i)
		#@-body
		#@-node:1::<< Scan for a section definition, @d or @c >>

		if macro_start and macro_end:
			return s[macro_start:macro_end]
		else:
			return "code"
	#@-body
	#@-node:2::createHeadlineFromBody
	#@+node:3::createOutlineFromCWEB
	#@+body
	def createOutlineFromCWEB (self,path,parent):
	
		junk, fileName = os.path.split(path)
		# Create the top-level headline.
		v = parent.insertAsLastChild()
		v.initHeadString(fileName)
		# Scan the file,creating one section for each function definition.
		self.scanCWEBFile(path,v)
		return v
	#@-body
	#@-node:3::createOutlineFromCWEB
	#@+node:4::cstCanonicalize
	#@+body
	#@+at
	#  We canonicalize strings before looking them up, but strings are entered in the form they are first encountered.

	#@-at
	#@@c
	
	def cstCanonicalize (self,s,lower=true):
		
		if lower:
			s = string.lower(s)
		s = string.replace(s,"\t"," ")
		s = string.replace(s,"\r"," ")
		s = string.replace(s,"\n"," ")
		s = string.replace(s,"  "," ")
		s = string.strip(s)
		return s
	#@-body
	#@-node:4::cstCanonicalize
	#@+node:5::cstDump
	#@+body
	def cstDump (self):
	
		self.cweb_st.sort()
		s = "Dump of cwt...\n"
		for name in self.cweb_st:
			s = s + name + "\n"
		return s
	#@-body
	#@-node:5::cstDump
	#@+node:6::cstEnter
	#@+body
	# We only enter the section name into the symbol table if the ... convention is not used.
	
	def cstEnter (self,s):
	
		# Don't enter names that end in "..."
		s = string.rstrip(s)
		if s.endswith("..."): return
		
		# Put the section name in the symbol table, retaining capitalization.
		lower = self.cstCanonicalize(s,true)  # do lower
		upper = self.cstCanonicalize(s,false) # don't lower.
		for name in self.cweb_st:
			if string.lower(name) == lower:
				return
		self.cweb_st.append(upper)
	#@-body
	#@-node:6::cstEnter
	#@+node:7::cstLookup
	#@+body
	# This method returns a string if the indicated string is a prefix of an entry in the cweb_st
	
	def cstLookup (self,target):
		
		# Do nothing if the ... convention is not used.
		target = string.strip(target)
		if not target.endswith("..."): return target
		# Canonicalize the target name, and remove the trailing "..."
		ctarget = target[:-3]
		ctarget = self.cstCanonicalize(ctarget)
		ctarget = string.strip(ctarget)
		found = false ; result = target
		for s in self.cweb_st:
			cs = self.cstCanonicalize(s)
			if cs[:len(ctarget)] == ctarget:
				if found:
					es("****** " + target + ": is also a prefix of: " + s)
				else:
					found = true ; result = s
					es("replacing: " + target + " with: " + s)
		return result
	#@-body
	#@-node:7::cstLookup
	#@+node:8:C=1:CWEBToOutlineCommand
	#@+body
	def CWEBToOutlineCommand (self,files):
	
		c = self.commands ; current = c.currentVnode()
		if current == None: return
		if len(files) < 1: return
		c.beginUpdate()
		i = 0
		while i < len(files):
			fileName = files[i] ; i += 1
			v = self.createOutlineFromCWEB(fileName,current)
			c.contractVnode(v)
			v.setDirty()
			c.setChanged(true)
		c.selectVnode(current)
		c.endUpdate()
	#@-body
	#@-node:8:C=1:CWEBToOutlineCommand
	#@+node:9:C=2:massageCWEBBody
	#@+body
	def massageCWEBBody (self,s):
	
		
		#@<< Remove most newlines from @space and @* sections >>
		#@+node:1::<< Remove most newlines from @space and @* sections >>
		#@+body
		i = 0
		while i < len(s):
			i = skip_ws_and_nl(s,i)
			if self.isTeXStart(s,i):
				# Scan to end of the section.
				start = end = i ; i += 2
				while i < len(s):
					i = skip_ws_and_nl(s,i)
					if self.isModuleStart(s,i) or self.isNameStart(s,i):
						break
					else:
						end = i ; i = skip_to_end_of_line(s,i)
				# Remove newlines from start to end.
				j = start
				while j < end:
					if s[j] == '\n':
						s = s[:j] + " " + s[j+1:]
					j += 1
			else: i = skip_line(s,i)
		#@-body
		#@-node:1::<< Remove most newlines from @space and @* sections >>

		
		#@<< Replace abbreviated names with full names >>
		#@+node:2::<< Replace abbreviated names with full names >>
		#@+body
		i = 0
		while i < len(s):
			if self.isNameStart(s,i):
				i += 2 ; start = i
				while i < len(s) and not self.isNameEnd(s,i) and not self.isNameStart(s,i):
					i += 1
				if i < len(s) and self.isNameEnd(s,i):
					name = s[start:i]
					name2 = self.cstLookup(name)
					if name != name2:
						# Replace name by name2.
						s = s[:start] + name2 + s[i:]
						i = start + len(name2)
			else: i += 1
		#@-body
		#@-node:2::<< Replace abbreviated names with full names >>

		s = string.rstrip(s)
		return s
	#@-body
	#@-node:9:C=2:massageCWEBBody
	#@+node:10:C=3:scanCWEBFile
	#@+body
	def scanCWEBFile (self,fileName,parent):
	
		try: # Read the file into s.
			f = open(fileName)
			s = f.read()
		except: s = None
		self.cweb_st = None
		
		#@<< Create a symbol table of all section names >>
		#@+node:1::<< Create a symbol table of all section names >>
		#@+body
		i = 0
		while i < len(s):
			if self.isAtAt(s,i):
				i += 2
			elif self.isNameStart(s,i):
				i += 2 ; start = i
				while i < len(s) and not self.isNameEnd(s,i) and not self.isNameStart(s,i):
					if self.isAtAt(s,i): i += 2
					else: i += 1
				if self.isNameEnd(s,i):
					self.cstEnter(s[start,i])
			else: i += 1
		
		trace(self.cstDump())
		#@-body
		#@-node:1::<< Create a symbol table of all section names >>

		
		#@<< Create a node for limbo text >>
		#@+node:2::<< Create a node for limbo text >>
		#@+body
		i = 0
		while i < len(s):
			i = skip_ws_and_nl(s,i)
			if self.isModuleStart(s,i): break
			else: i = skip_line(s,i)
			
		j = skip_ws(s,i)
		if j < i:
			self.createCWEBHeadline(parent,"Limbo",s[j:i])
		#@-body
		#@-node:2::<< Create a node for limbo text >>

		while i < len(s):
			
			#@<< Create a node for the next module >>
			#@+node:3::<< Create a node for the next module >>
			#@+body
			assert(self.isModuleStart(s,i))
			start = i
			if self.isTeXStart(s,i):
				i += 2 ; i = skip_line(s,i)
				while i < len(s):
					i = skip_ws_and_nl(s,i)
					if self.isModuleStart(s,i): break
					else: i = skip_line(s,i)
			if self.isMacroStart(s,i):
				i += 2 ; i = skip_line(s,i)
				# Place all @d directives in the same node.
				while i < len(s):
					i = skip_ws_and_nl(s,i)
					if self.isModuleStart(s,i) and not self.isMacroStart(s,i): break
					else: i = skip_line(s,i)
			if self.isCodeStart(s,i):
				i += 2 ; i = skip_line(s,i)
				while i < len(s):
					i = skip_ws_and_nl(s,i)
					if self.isModuleStart(s,i): break
					else: i = skip_line(s,i)
			body = s[start:i]
			body = self.massageCWEBBody(body)
			headline = self.createHeadlineFromBody(body)
			self.createCWEBHeadline(parent,headline,body)
			#@-body
			#@-node:3::<< Create a node for the next module >>
	#@-body
	#@-node:10:C=3:scanCWEBFile
	#@-node:1::CWEBToOutline
	#@+node:2::Import
	#@+node:1::convertMoreStringsToOutlineAfter
	#@+body
	# Almost all the time spent in this command is spent here.
	
	def convertMoreStringsToOutlineAfter (self,strings,firstVnode):
	
		c = self.commands
		if len(strings) == 0: return None
		if not self.stringsAreValidMoreFile(strings): return None
		c.beginUpdate()
		firstLevel, junk = self.moreHeadlineLevel(strings[0])
		index = 0 ; lastLevel = -1 ; theRoot = lastVnode = None
		while index < len(strings):
			s = strings[index] ; i = 0
			level, newFlag = self.moreHeadlineLevel(s)
			level -= firstLevel
			if level >= 0:
				
				#@<< Link a new vnode v into the outline >>
				#@+node:1::<< Link a new vnode v into the outline >>
				#@+body
				assert(level >= 0)
				if not lastVnode:
					theRoot = v = firstVnode.insertAfter()
				elif level == lastLevel:
					v = lastVnode.insertAfter()
				elif level == lastLevel + 1:
					v = lastVnode.insertAsNthChild(0)
				else:
					assert(level < lastLevel)
					while level < lastLevel:
						lastLevel -= 1
						lastVnode = lastVnode.parent()
						assert(lastVnode)
						assert(lastLevel >= 0)
					v = lastVnode.insertAfter()
				lastVnode = v
				lastLevel = level
				#@-body
				#@-node:1::<< Link a new vnode v into the outline >>

				
				#@<< Set the headline string, skipping over the leader >>
				#@+node:2::<< Set the headline string, skipping over the leader >>
				#@+body
				j = 0
				while match(s,i,'\t'):
					j += 1
				if match(s,j,"+ ") or match(s,j,"- "):
					j += 2
				v.initHeadline(s[j:])
				#@-body
				#@-node:2::<< Set the headline string, skipping over the leader >>

				
				#@<< Count the number of following body lines >>
				#@+node:3::<< Count the number of following body lines >>
				#@+body
				bodyLines = 0
				index += 1 # Skip the headline.
				while index < len(strings):
					s = strings[index]
					level, junk = self.moreHeadlineLevel(s)
					level -= firstLevel
					if level >= 0:
						break
					# Remove first backslash of the body line.
					if match(s,0,'\\'):
						strings[index] = s[1:]
					bodyLines += 1
					index += 1
				#@-body
				#@-node:3::<< Count the number of following body lines >>

				
				#@<< Add the lines to the body text of v >>
				#@+node:4::<< Add the lines to the body text of v >>
				#@+body
				if bodyLines > 0:
					body = ""
					n = index - bodyLines
					while n < index:
						body += strings[n]
						if n != index - 1:
							body += "\n"
						n += 1
					v.t.setTnodeText(body)
				#@-body
				#@-node:4::<< Add the lines to the body text of v >>

				v.setDirty()
			else: index += 1
		if theRoot:
			theRoot.setDirty()
			c.setChanged(true)
		c.endUpdate()
		return theRoot
	#@-body
	#@-node:1::convertMoreStringsToOutlineAfter
	#@+node:2::ImportFilesCommand
	#@+body
	def ImportFilesCommand (self,files):
	
		c = self.commands ; current = c.currentVnode()
		if not current: return
		if len(files) < 1: return
		c.beginUpdate()
		if 1: # range of update...
		  	c.selectVnode(current)
			if len(files) == 2:
				
				#@<< Create a parent for two files having a common prefix >>
				#@+node:1::<< Create a parent for two files having a common prefix >>
				#@+body
				#@+at
				#  The two filenames have a common prefix everything before the last period is the same.  For example, x.h and x.cpp.

				#@-at
				#@@c
				
				name0 = files[0]
				name1 = files[1]
				prefix0, junk = os.path.splitext(name0)
				prefix1, junk = os.path.splitext(name1)
				if len(prefix0) > 0 and prefix0 == prefix1:
					current = current.insertAsLastChild()
					junk, nameExt = os.path.split(prefix1)
					name,ext = os.path.splitext(prefix1)
					current.initHeadString(name)
				#@-body
				#@-node:1::<< Create a parent for two files having a common prefix >>

			i = 0
			while i < len(files):
				fileName = files[0]
				v = self.createOutline(fileName,current)
				c.contractVnode(v)
				v.setDirty()
				c.setChanged(true)
				i += 1
			c.validateOutline()
		  	c.selectVnode(current)
		c.endUpdate()
	#@-body
	#@-node:2::ImportFilesCommand
	#@+node:3::importMoreText
	#@+body
	# On entry,files contains at most one file to convert.
	def importMoreText (self,files):
	
		c = self.commands ; current = c.currentVnode()
		if current == None: return
		if len(files) < 1: return
		fileName = files[0]
		
		#@<< Read the file into array >>
		#@+node:1::<< Read the file into array >>
		#@+body
		try:
			file = open(fileName)
			array = file.readlines()
			file.close()
		except: array = []
		#@-body
		#@-node:1::<< Read the file into array >>

		# Convert the string to an outline and insert it after the current node.
		newVnode = self.convertMoreStringsToOutlineAfter(array,current)
		if newVnode:
			c.endEditing()
			c.validateOutline()
			c.editVnode(newVnode)
			newVnode.setDirty()
			c.setChanged(true)
		else:
			es(fileName + " is not a valid MORE file.")
	#@-body
	#@-node:3::importMoreText
	#@+node:4::moreHeadlineLevel
	#@+body
	# return the headline level of s,or -1 if the string is not a MORE headline.
	def moreHeadlineLevel (self,s):
	
		level = 0 ; i = 0
		while match(s,i,'\t'):
			level += 1
			i += 1
		plusFlag = choose(match(s,i,"+"),true,false)
		if match(s,i,"+ ") or match(s,i,"- "):
			return level, plusFlag
		else:
			return -1, plusFlag
	#@-body
	#@-node:4::moreHeadlineLevel
	#@+node:5::stringsAreValidMoreFile
	#@+body
	def stringsAreValidMoreFile (self,strings):
	
		if len(strings) < 1: return false
		level1, plusFlag = self.moreHeadlineLevel(strings[0])
		if level1 == -1: return false
		# Check the level of all headlines.
		i = 0 ; 	lastLevel = level1
		while i < len(strings):
			s = strings[i] ; i += 1
			level, newFlag = self.moreHeadlineLevel(s)
			if level > 0:
				if level < level1 or level > lastLevel + 1:
					return false # improper level.
				elif level > lastLevel and plusFlag == false:
					return false # parent of this node has no children.
				elif level == lastLevel and plusFlag == true:
					return false # last node has missing child.
				else:
					lastLevel = level
					plusFlag = newFlag
		return true
	#@-body
	#@-node:5::stringsAreValidMoreFile
	#@-node:2::Import
	#@+node:3::Export
	#@+node:1::exportMoreText
	#@+body
	def exportMoreText (self):
	
		c = self.commands ; v = c.currentVnode()
		if v:
			app().clipboard = v.convertTreeToString()
	#@-body
	#@-node:1::exportMoreText
	#@+node:2:C=4:flattenOutline
	#@+body
	def flattenOutline (self,fileName):
	
		c = self.commands ; v = c.currentVnode()
		if not v: return
		after = v.nodeAfterTree()
		firstLevel = v.level()
		try:
			file = open(fileName,'w')
			while v and v != after:
				head = v.moreHead(firstLevel)
				file.write( head + '\n')
				body = v.moreBody() # Inserts escapes.
				if len(body) > 0:
					file.write(body + '\n')
				v = v.threadNext()
			file.close()
		except:
			es("File error while flattening the outline")
	#@-body
	#@-node:2:C=4:flattenOutline
	#@+node:3:C=5:outlineToNoweb
	#@+body
	def outlineToNoweb (self,fileName):
	
		c = self.commands ; v = c.currentVnode()
		if v == None: return
		after = v.nodeAfterTree()
		try:
			file = open(fileName,'w')
			while v and v != after:
				s = self.convertToNoweb(v)
				if len(s) > 0:
					file.write(s)
					if s[-1] != '\n':
						file.write('\n')
				v = v.threadNext()
			file.close()
		except:
			es("File error in Outline To noweb command")
	#@-body
	#@-node:3:C=5:outlineToNoweb
	#@+node:4::convertToNoweb
	#@+body
	#@+at
	#  This code converts a vnode to noweb text as follows:
	# 
	# Convert @root to << * >>
	# Convert @doc to @
	# Convert @code to << name >>=, assuming the headline contains << name >>
	# Ignore other directives
	# Format parts so they fit in pagewidth columns.
	# Output code parts as is.

	#@-at
	#@@c
	
	def convertToNoweb (self,v):
	
		if not v: return ""
		s = v.bodyString()
		i = 0 ; result = []
		while i < len(s):
			i = skip_ws_and_nl(s,i)
			if match_word(s,i,"@doc") or match(s,i,"@ "):
				i = self.convertDocPartToNoweb(s,i,result)
			elif (match_word(s,i,"@code") or match(s,i,"@c") or
				match_word(s,i,"@root") or match(s,i,"<<")):
				i = self.convertCodePartToNoweb(s,i,v,result)
			elif s[i] == '@':
				i = skip_line(s,i) # Ignore all other directives.
			else: # Assume we are in a doc part.
				i = self.convertDocPartToNoweb(s,i,result)
		return listToString(result)
	#@-body
	#@-node:4::convertToNoweb
	#@+node:5::convertCodePartToNoweb
	#@+body
	# The code part should start either with @code or @root or < < section name > > =
	
	def convertCodePartToNoweb (self,s,i,v,result):
	
		if i >= len(s): return i
		if match_word(s,i,"@c"):
			
			#@<< handle @c >>
			#@+node:1::<< handle @c >>
			#@+body
			i = skip_line(s,i)
			
			#@<< put v's headline in head >>
			#@+node:1::<< put v's headline in head>>
			#@+body
			head = v.headString()
			j = skip_ws(head,0)
			if match(head,j,"<<"):
				j += 2 ; k = j
				while k < len(head) and not match(head,k,">>"):
					k += 1
				if match(head,k,">>"): head = head[j:k]
				else: head = None
			else: head = None
			#@-body
			#@-node:1::<< put v's headline in head>>

			if head:
				# for ch in "\n" + head + "=": result.append(ch)
				result.append("\n" + head + "=")
			else:
				# for ch in "\n\n" + angleBrackets("*** no section name for @c ***"): result.append(ch)
				result.append("\n\n" + angleBrackets("*** no section name for @c ***"))
			#@-body
			#@-node:1::<< handle @c >>

		elif match(s,i,"@root"):
			
			#@<< handle @root >>
			#@+node:2::<< handle @root >>
			#@+body
			j = skip_ws(s,i+5)
			i = skip_line(s,i)
			if j < i:
				
				#@<< Set name >>
				#@+node:1::<< Set name >>
				#@+body
				delim = ' ' ; name = None
				if match(s,j,"<"):
					j += 1 ; delim = ">"
				elif match(s,j,'"'):
					j += 1 ; delim = '"'
				else: delim = ' '
				k = j
				while k < len(s) and s[k] != delim and not is_nl(s,k):
					k += 1
				if j < k:
					name = string.strip(s[j:k])
				if not name or len(name) == 0:
					name = "*"
				#@-body
				#@-node:1::<< Set name >>

			result += "\n\n" + angleBrackets(" " + name + " ") + "="
			#@-body
			#@-node:2::<< handle @root >>

		elif match(s,i,"<<"):
			
			#@<< copy the line to result >>
			#@+node:3::<< copy the line to result >>
			#@+body
			j = i ; i = skip_line(s,i)
			for ch in s[j:i]:
				result.append(ch)
			#@-body
			#@-node:3::<< copy the line to result >>

		i = self.copyPart(s,i,result)
		return i
	#@-body
	#@-node:5::convertCodePartToNoweb
	#@+node:6::convertDocPartToNoweb
	#@+body
	def convertDocPartToNoweb (self,s,i,outerResult):
	
		if match_word(s,i,"@doc") or match_word(s,i,"@ "):
			i = skip_line(s,i)
		i = skip_ws_and_nl(s,i)
		result = []
		i = self.copyPart(s,i,result)
		if len(result) > 0:
			# We could break long lines in result here.
			for ch in "@ \n":
				outerResult.append(ch)
			for ch in result:
				outerResult.append(ch)
		return i
	#@-body
	#@-node:6::convertDocPartToNoweb
	#@+node:7::copyPart
	#@+body
	# Copies characters to result until the end of the present section is seen.
	
	def copyPart (self,s,i,result):
	
		while i < len(s):
			j = i # We should be at the start of a line here.
			i = skip_nl(s,i) ; i = skip_ws(s,i)
			if match_word(s,i,"@doc") or match_word(s,i,"@c") or match_word(s,i,"@root"):
				return i
			elif match(s,i,"<<"):
				k = find_on_line(s,i,">>=")
				if k > -1: return i
			elif match(s,i,"@ ") or match(s,i,"@@"):
				return i
			elif s[i] == '@':
				i = skip_line(s,i) # Ignore all other directives.
			else:
				# Copy the entire line.
				i = skip_line(s,j)
				for ch in s[j:i]:
					result.append(ch)
		return i
	#@-body
	#@-node:7::copyPart
	#@-node:3::Export
	#@+node:4::createOutline
	#@+body
	def createOutline (self,fileName,parent):
	
		junk, self.fileName = os.path.split(fileName) # junk/fileName
		self.methodName, type = os.path.splitext(self.fileName) # methodName.fileType
		self.fileType = type
		trace(`self.fileName`)
		trace(`self.fileType`)
		# All file types except the following just get copied to the parent node.
		appendFileFlag = type not in [".c", ".cpp", ".java", ".pas", ".py"]
		
		#@<< Read file into s >>
		#@+node:1::<< Read file into s >>
		#@+body
		try:
			file = open(fileName)
			s = file.read()
			file.close()
		except:
			es("Can not read " + fileName)
			return
		#@-body
		#@-node:1::<< Read file into s >>

		# Create the top-level headline.
		v = parent.insertAsLastChild()
		v.initHeadString(self.fileName)
		if appendFileFlag:
			v.setBodyStringOrPane(s)
		elif type == ".c" or type == ".cpp":
			self.scanCText(s,v)
		elif type == ".java":
			self.scanJavaText(s,v,true) #outer level
		elif type == ".pas":
			self.scanPascalText(s,v)
		elif type == ".py":
			self.scanPythonText(s,v)
		else:
			es("createOutline: can't happen")
		return v
	#@-body
	#@-node:4::createOutline
	#@-node:4::Top Level
	#@+node:5::Utilities
	#@+node:1::createHeadline
	#@+body
	def createHeadline (self,parent,body,headline):
	
		trace(`headline`)
		# Create the vnode.
		v = parent.insertAsLastChild()
		v.initHeadString(headline)
		# Set the body.
		if len(body) > 0: 
			v.setBodyStringOrPane(body)
		return v
	#@-body
	#@-node:1::createHeadline
	#@+node:2::getPythonIndent
	#@+body
	#@+at
	#  This code returns the leading whitespace of a line, ignoring blank and comment lines.
	# 
	# This routine should be called at, or just after, a newline character.

	#@-at
	#@@c
	
	def getPythonIndent (self,s,i):
		
		j = skip_to_end_of_line(s,0) ; trace(s[:j])
		c = self.commands
		i = 0
		while i < len(s):
			i, width = skip_leading_ws_with_indent(s,i,c.tab_width)
			if is_nl(s,i) or match(s,i,"#"):
				i = skip_line(s,i) # ignore blank lines and comments.
			else:
				return width
		return 0
	#@-body
	#@-node:2::getPythonIndent
	#@+node:3::massageBody
	#@+body
	# Inserts < < path methods > > = at the start of the body text and after leading comments.
	
	def massageBody (self,s,methodKind):
		
		j = skip_to_end_of_line(s,0) ; trace(s[:j])
		c = self.commands
		cweb = (self.fileType == "c" and not c.use_noweb_flag)
		lb = choose(cweb,"@<","<<")
		rb = choose(cweb,"@>=",">>=")
		intro = lb + " " + self.methodName + " " + methodKind + " " + rb
		if self.fileType == "py":
			
			#@<< massage python text >>
			#@+node:1::<< massage python text >>
			#@+body
			# For Python, we want to delete all but one tab from the text.
			
			newBody = self.undentPythonBody(s)
			# newBody = self.massageAngleBrackets(newBody)
			newLine = choose(is_nl(newBody,0),"","\n")
			return intro + newLine + newBody
			#@-body
			#@-node:1::<< massage python text >>

		else:
			
			#@<< massage other text >>
			#@+node:2::<< massage other text >>
			#@+body
			newBody, comment = self.skipLeadingComments(s)
			# newBody = self.massageAngleBrackets(newBody)
			newLine = choose(is_nl(newBody,0),"","\n")
			if len(comment) > 0:
				return comment + "\n" + intro + newLine + newBody
			else:
				return intro + newLine + newBody
			#@-body
			#@-node:2::<< massage other text >>
	#@-body
	#@-node:3::massageBody
	#@+node:4::massageAngleBrackets (do not use!)
	#@+body
	# Converts < < to @ < < and > > to @ > > everywhere.
	
	def massageAngleBrackets (self,s):
	
		# Do not use @ < < inside strings.
		j = skip_line(s,0) ; trace(s[:j])
		lb = "@" ; lb += "<<"
		rb = "@" ; rb += ">>"
		s = string.replace(s,"<<",lb)
		s = string.replace(s,">>",rb)
		return s
	#@-body
	#@-node:4::massageAngleBrackets (do not use!)
	#@+node:5::massageComment
	#@+body
	#@+at
	#  Returns s with all runs of whitespace and newlines converted to a single blank.  It also removes leading and trailing whitespace.

	#@-at
	#@@c
	
	def massageComment (self,s):
	
		j = skip_line(s,0) ; trace(s[:j])
		s = string.strip(s)
		s = string.replace(s,"\n"," ")
		s = string.replace(s,"\r"," ")
		s = string.replace(s,"\t"," ")
		s = string.replace(s,"  "," ")
		s = string.strip(s)
		return s
	#@-body
	#@-node:5::massageComment
	#@+node:6::skipLeadingComments
	#@+body
	#@+at
	#  This skips all leading comments in s, returning the remaining body text and the massaged comment text. Comment text is 
	# massaged as follows:
	# 
	# . Leading // on a line is deleted.
	# . A line starting with /// << or /// -- end -- << is deleted.
	# . The / * and * / characters surrounding a block comment are removed.
	# . Any sequence of whitespace and newlines is replaced by a single blank.
	# . Leading and trailing whitespace is deleted.
	# 
	# Returns (body, comment)

	#@-at
	#@@c
	
	def skipLeadingComments (self,s):
	
		trace(`get_line(s,0)`)
		comment = "" ; newComment = ""
		s = string.lstrip(s)
		i = 0
		while i < len(s):
			# Skip lines starting with /// <<
			if match(s,i,"/// <<"):
				while i < len(s) and s[i] != '\n':
					i += 1
				while i < len(s) and is_ws_or_nl(s,i):
					i += 1
			elif match(s,i,"/// -- end -- <<"):
				while i < len(s) and s[i] != '\n':
					i += 1
				while i < len(s) and is_ws_or_nl(s,i):
					i += 1
			elif match(s,i,"//"): # Handle a C++ comment.
				i += 2
				while i < len(s) and s[i] == '/':
					i += 1
				commentStart = i
				while i < len(s) and not is_nl(s,i):
					i += 1
				newComment = self.massageComment(s[commentStart:i-1])
				comment = comment + newComment + "\n"
				while is_ws_or_nl(s,i):
					i += 1
			elif match(s,i,"/*"): # Handle a block C comment.
				i += 2 ; commentStart = i
				while i < len and not match(s,i,"*/"):
					i += 1
				if match(s,i,"*/"):
					i += 2
				newComment = self.massageComment(s[commentStart:i-2])
				comment = comment + newComment + "\n"
				while is_ws_or_nl(s,i):
					i += 1
			else: break
		return s[i:], comment
	#@-body
	#@-node:6::skipLeadingComments
	#@+node:7::undentPythonBody
	#@+body
	#@+at
	#  Removes extra leading indentation from all lines.  We look at the first line to determine how much leading whitespace to delete.

	#@-at
	#@@c
	
	def undentPythonBody (self,s):
		
		j = skip_to_end_of_line(s,0) ; trace(s[:j])
		c = self.commands
		i = 0 ; result = ""
		# Copy an @code line as is.
		if match(s,i,"@code"):
			j = i ; i = skip_line(s,i)
			result += s[j:i]
		# Calculate the amount to be removed from each line.
		undent = self.getPythonIndent(s,i)
		if undent == 0: return s
		while i < len(s):
			j = i ; i = skip_line(s,i)
			line = s[j:i]
			line = removeLeadingWhitespace(line,undent,c.tab_width)
			result += line
		return result
	#@-body
	#@-node:7::undentPythonBody
	#@-node:5::Utilities
	#@+node:6::Language Specific
	#@+node:1::scanJavaText
	#@+body
	#@+at
	#  This code creates a child of parent for each Java function definition seen.  See the comments for scanCText for what the text
	# looks like.

	#@-at
	#@@c
	
	def scanJavaText (self,s,parent,outerFlag): # TRUE if at outer level.
	
		j = skip_to_end_of_line(s,0) ; trace(s[:j])
		method_seen = false
		class_seen = false # TRUE is class keyword seen at outer level.
		lparen = None   # Non-null if '(' seen at outer level.
		
		#@<< Initialize the ImportFiles private globals >>
		#@+node:1:C=6:<< Initialize the ImportFiles private globals >>
		#@+body
		# Shared by several routines...
		scan_start = i = 0
		function_start = i
		function_end = None
		name_start = name_end = None
		#@-body
		#@-node:1:C=6:<< Initialize the ImportFiles private globals >>

		trace()
		while i < len(s): 
			ch = s[i]
			# These cases skip tokens.
			if ch == '/':
				
				#@<< handle possible C comments >>
				#@+node:4:C=7:Shared by C and Java
				#@+node:1::<< handle possible C comments >>
				#@+body
				i += 1 # skip the opening '/'
				if i < len(s) and s[i] == '/':
					i = skip_line(s,i)
				elif i < len(s) and s[i] == '*':
					i += 1
					i = skip_block_comment(s,i)
				#@-body
				#@-node:1::<< handle possible C comments >>
				#@-node:4:C=7:Shared by C and Java

			elif ch == '"' or ch == '\'':
				i = skip_string(s,i)
			# These cases help determine where functions start.
			elif ch == '=':
				
				#@<< handle equal sign in C or Java >>
				#@+node:4:C=7:Shared by C and Java
				#@+node:2::<< handle equal sign in C or Java >>
				#@+body
				#@+at
				#  We can not be seeing a function definition when we find an equal sign at the top level. Equal signs inside 
				# parentheses are handled by the open paren logic.

				#@-at
				#@@c
				
				i += 1 # skip the '='
				function_start = None # We can't be in a function.
				lparen = None   # We have not seen an argument list yet.
				if  i < len(s) and s[i] == '=':
					i = skip_braces(s,i)
				#@-body
				#@-node:2::<< handle equal sign in C or Java >>
				#@-node:4:C=7:Shared by C and Java

			elif ch == '(':
				
				#@<< handle open paren in C or Java >>
				#@+node:4:C=7:Shared by C and Java
				#@+node:3::<< handle open paren in C or Java >>
				#@+body
				lparen = i
				# This will skip any equal signs inside the paren.
				i = skip_parens(s,i)
				if i < len(s) and s[i] == ')':
					i += 1
					i = skip_ws_and_nl(s,i)
					if i < len(s) and s[i] == ';':
						lparen = None # not a function definition.
				else: lparen = None
				#@-body
				#@-node:3::<< handle open paren in C or Java >>
				#@-node:4:C=7:Shared by C and Java

			elif ch == ';':
				
				#@<< handle semicolon in C or Java >>
				#@+node:4:C=7:Shared by C and Java
				#@+node:4::<< handle semicolon in C or Java >>
				#@+body
				#@+at
				#  A semicolon signals the end of a declaration, thereby potentially starting the _next_ function defintion.   
				# Declarations end a function definition unless we have already seen a parenthesis, in which case we are seeing an 
				# old-style function definition.

				#@-at
				#@@c
				
				i += 1 # skip the semicolon.
				if lparen == None:
					function_start = i + 1 # The semicolon ends the declaration.
				#@-body
				#@-node:4::<< handle semicolon in C or Java >>
				#@-node:4:C=7:Shared by C and Java

				class_seen = false
			# This cases and the default case can create child nodes.
			elif ch == '{':
				
				#@<< handle open curly bracket in Java >>
				#@+node:2::<< handle open curly bracket in Java >>
				#@+body
				brace_ip1 = i
				i = skip_braces(s,i) # Skip all inner blocks.
				brace_ip2 = i
				if (i < len(s) and s[i] == '}' and
					(not outerFlag and lparen or outerFlag and class_seen) and
					name_start and name_end and function_start):
					# Point i _after_ the last character of the method.
					i += 1
					if is_nl(s,i):
						i = skip_nl(s,i)
					function_end = i
					headline = s[name_start,name_end]
					if outerFlag:
						leader = "" ; decl_leader = ""
						headline = "class " + headline
						methodKind = "classes"
					else:
						leader = "\t" # Indent only inner references.
						decl_leader = "\n"  # Declaration leader for inner references.
						methodKind = "methods"
					if method_seen:
						# Include everything after the last fucntion.
						function_start = scan_start
					else:
						
						#@<< create a Java declaration node >>
						#@+node:1::<< create a Java declaration node >>
						#@+body
						save_ip = i
						i = scan_start
						while i < function_start and is_ws_or_nl(s,i):
							i += 1
						if i < function_start:
							headline = angleBrackets(self.methodName + " declarations ")
							# Append the headline to the parent's body.
							parent.appendStringToBody(decl_leader + leader + headline + "\n")
							decls = s[scan_start:function_start]
							body = "@code\n\n" + decls
							self.createHeadline(parent,body,headline)
						i = save_ip
						scan_start = i
						#@-body
						#@-node:1::<< create a Java declaration node >>

						
						#@<< append Java method reference to parent node >>
						#@+node:2::<< append Java method reference to parent node >>
						#@+body
						kind = choose(outerFlag,"classes","methods")
						name = angleBrackets(self.methodName + " " + kind)
						parent.appendStringToBody(leader + name + "\n")
						#@-body
						#@-node:2::<< append Java method reference to parent node >>

					if outerFlag:
						# Create a headline for the class.
						body = s[function_start:brace_ip1+1]
						body = self.massageBody(body,methodKind)
						v = self.createHeadline(parent,body,headline)
						
						#@<< recursively scan the text >>
						#@+node:3::<< recursively scan the text >>
						#@+body
						# These mark the points in the present function.
						oldMethodName = self.methodName
						self.methodName = headline
						self.scanJavaText(s[brace_ip1+1,brace_ip2], # Don't include either brace.
							v,false) # inner level
						self.methodName = oldMethodName
						# Append the brace to the parent.
						v.appendStringToBody("}")
						i = brace_ip2 + 1 # Start after the closing brace.
						#@-body
						#@-node:3::<< recursively scan the text >>

					else:
						# Create a single headline for the method.
						body = s[function_start:function_end]
						body = self.massageBody(body,methodKind)
						self.createHeadline(parent,body,headline)
					method_seen = true
					scan_start = i
					function_start = i # Set the start of the _next_ function.
					lparen = None
					class_seen = false
				else: i += 1
				#@-body
				#@-node:2::<< handle open curly bracket in Java >>

			elif is_c_id(s[i]):
				
				#@<< skip and remember the Java id >>
				#@+node:3::<< skip and remember the Java id >>
				#@+body
				if match_c_word(s,i,"class"):
					class_seen = true
					i = skip_c_id(s,i)
					i = skip_ws_and_nl(s,i)
					if i < len(s) and is_c_id(s[i]):
						# Remember the class name.
						name_start = i
						i = skip_c_id(s,i)
						name_end = i - 1
				elif class_seen:
					# Remember a possible method name.
					name_start = i
					i = skip_c_id(s,i)
					name_end = i - 1
				else: i = skip_c_id(s,i)
				#@-body
				#@-node:3::<< skip and remember the Java id >>

			else: i += 1
		
		#@<< Append any unused text to the parent's body text >>
		#@+node:5:C=8:<< Append any unused text to the parent's body text >>
		#@+body
		# Used by C, Java and Pascal parsers.
		# Do nothing if only whitespace is left.
		
		i = skip_ws_and_nl(s,scan_start)
		if i < len(s):
			parent.appendStringToBody(s[scan_start:])
		#@-body
		#@-node:5:C=8:<< Append any unused text to the parent's body text >>
	#@-body
	#@+node:4:C=7:Shared by C and Java
	#@-node:4:C=7:Shared by C and Java
	#@-node:1::scanJavaText
	#@+node:2::scanCText
	#@+body
	#@+at
	#  This code creates a child of parent for each C function definition seen.
	# 
	# After calling this function the body text of the parent node will look like this:
	# 	..whatever was in the parent node before the call..
	# 	..all text before the first method found..
	# 	<< gModuleName methods >>
	# 	..all text after the last method found..
	# 
	# Each new child node will have the form
	# 	..the text of the method
	# Namesspaces change the gModuleName global and recursively call self function with a text covering only the range of the
	# namespace. This effectively changes the definition line of any created child nodes. The namespace is written to the top level.

	#@-at
	#@@c
	
	def scanCText (self,s,parent):
	
		trace(`get_line(s,0)`)
		c = self.commands
		include_seen = false ; method_seen = false
		first_ip = i = 0 # To terminate backwards scans.
		lparen = None   # Non-null if '(' seen at outer level.
		methodKind = choose(self.fileType == "c","functions","methods")
		
		#@<< Initialize the ImportFiles private globals >>
		#@+node:1:C=6:<< Initialize the ImportFiles private globals >>
		#@+body
		# Shared by several routines...
		scan_start = i = 0
		function_start = i
		function_end = None
		name_start = name_end = None
		#@-body
		#@-node:1:C=6:<< Initialize the ImportFiles private globals >>

		while i < len(s): 
			ch = s[i]
			# These cases skip tokens.
			if ch == '/':
				
				#@<< handle possible C comments >>
				#@+node:5:C=7:Shared by C and Java
				#@+node:1::<< handle possible C comments >>
				#@+body
				i += 1 # skip the opening '/'
				if i < len(s) and s[i] == '/':
					i = skip_line(s,i)
				elif i < len(s) and s[i] == '*':
					i += 1
					i = skip_block_comment(s,i)
				#@-body
				#@-node:1::<< handle possible C comments >>
				#@-node:5:C=7:Shared by C and Java

			elif ch == '"' or ch == '\'':
				i = skip_string(s,i)
			# These cases help determine where functions start.
			elif ch == '=':
				
				#@<< handle equal sign in C or Java >>
				#@+node:5:C=7:Shared by C and Java
				#@+node:2::<< handle equal sign in C or Java >>
				#@+body
				#@+at
				#  We can not be seeing a function definition when we find an equal sign at the top level. Equal signs inside 
				# parentheses are handled by the open paren logic.

				#@-at
				#@@c
				
				i += 1 # skip the '='
				function_start = None # We can't be in a function.
				lparen = None   # We have not seen an argument list yet.
				if  i < len(s) and s[i] == '=':
					i = skip_braces(s,i)
				#@-body
				#@-node:2::<< handle equal sign in C or Java >>
				#@-node:5:C=7:Shared by C and Java

			elif ch == '(':
				
				#@<< handle open paren in C or Java >>
				#@+node:5:C=7:Shared by C and Java
				#@+node:3::<< handle open paren in C or Java >>
				#@+body
				lparen = i
				# This will skip any equal signs inside the paren.
				i = skip_parens(s,i)
				if i < len(s) and s[i] == ')':
					i += 1
					i = skip_ws_and_nl(s,i)
					if i < len(s) and s[i] == ';':
						lparen = None # not a function definition.
				else: lparen = None
				#@-body
				#@-node:3::<< handle open paren in C or Java >>
				#@-node:5:C=7:Shared by C and Java

			elif ch == ';':
				
				#@<< handle semicolon in C or Java >>
				#@+node:5:C=7:Shared by C and Java
				#@+node:4::<< handle semicolon in C or Java >>
				#@+body
				#@+at
				#  A semicolon signals the end of a declaration, thereby potentially starting the _next_ function defintion.   
				# Declarations end a function definition unless we have already seen a parenthesis, in which case we are seeing an 
				# old-style function definition.

				#@-at
				#@@c
				
				i += 1 # skip the semicolon.
				if lparen == None:
					function_start = i + 1 # The semicolon ends the declaration.
				#@-body
				#@-node:4::<< handle semicolon in C or Java >>
				#@-node:5:C=7:Shared by C and Java

			# These cases and the default case can create child nodes.
			elif ch == '#':
				
				#@<< handle # sign >>
				#@+node:2::<< handle # sign >>
				#@+body
				# if statements may contain function definitions.
				i += 1  # Skip the '#'
				if not include_seen and match_c_word(s,i,"include"):
					include_seen = true
					
					#@<< create a child node for all #include statements >>
					#@+node:1::<< create a child node for all #include statements >>
					#@+body
					# Scan back to the start of the line.
					include_start = i
					while include_start > first_ip and not is_nl(s,include_start):
						include_start -= 1
					if is_nl(s,include_start):
						include_start = skip_nl(s,include_start)
					# Scan to the next line that is neither blank nor and #include.
					i = include_start
					i = skip_pp_directive(s,i)
					i = skip_nl(s,i)
					include_end = i
					while i < len(s):
						i = skip_ws_and_nl(s,i)
						if match_c_word(s,i,"#include"):
							i = skip_pp_directive(s,i)
							i = skip_nl(s,i)
							include_end = i
						elif i + 2 < len(s) and s[i] == '\\':
							# Handle possible comment.
							if s[i+1] == '\\':
								i = skip_to_end_of_line(s,i)
							elif s[i+1] == '*':
								i = skip_block_comment(s,i + 2)
							else:
								i = include_end ; break
						else:
							i = include_end ; break
					headline = angleBrackets(" " + self.methodName + " #includes ")
					body = "@code\n\n" + s[include_start:include_end]
					self.createHeadline(parent,body,headline)
					# Append any previous text to the parent's body.
					save_ip = i
					#
					i = scan_start
					while i < include_start and is_ws_or_nl(s,i):
						i += 1
					if i < include_start:
						parent.appendStringToBody(s[i:include_start])
					#
					i = save_ip
					scan_start = i
					function_start = i
					# Append the headline to the parent's body.
					parent.appendStringToBody(headline + "\n")
					#@-body
					#@-node:1::<< create a child node for all #include statements >>

				else: i = skip_pp_directive(s,i)
				#@-body
				#@-node:2::<< handle # sign >>

			elif ch == '{':
				
				#@<< handle open curly bracket in C >>
				#@+node:3::<< handle open curly bracket in C >>
				#@+body
				i = skip_braces(s,i) # Skip all inner blocks.
				if (i < len(s) and s[i] == '}' and  # This may fail if #if's contain unmathed curly braces.
					lparen and name_start and name_end and function_start):
					# Point i _after_ the last character of the function.
					i += 1
					if i < len(s) and(s[i] == '\r' or s[i] == '\n'):
						i = skip_nl(s,i)
					function_end = i
					if method_seen:
						function_start = scan_start # Include everything after the last fucntion.
					else:
						
						#@<< create a declaration node >>
						#@+node:1::<< create a declaration node >>
						#@+body
						save_ip = i
						i = scan_start
						while i < function_start and is_ws_or_nl(s,i):
							i += 1
						if i < function_start:
							headline = angleBrackets(self.methodName + " declarations ")
							# Append the headline to the parent's body.
							parent.appendStringToBody(headline + "\n")
							decls = s[scan_start:function_start]
							body = "@code\n\n" + decls
							self.createHeadline(parent,body,headline)
						i = save_ip
						scan_start = i
						#@-body
						#@-node:1::<< create a declaration node >>

						
						#@<< append C function/method reference to parent node >>
						#@+node:2::<< append C function/method reference to parent node >>
						#@+body
						cweb = not c.use_noweb_flag
						lb = choose(cweb,"@<","<<")
						rb = choose(cweb,"@>",">>")
						s = lb + self.methodName + " " + methodKind + rb
						parent.appendStringToBody(s + "\n")
						#@-body
						#@-node:2::<< append C function/method reference to parent node >>

					length = name_end - name_start + 1
					headline = (name_start,length)
					body = s[function_start:function_end]
					body = self.massageBody(body,"functions")
					self.createHeadline(parent,body,headline)
					method_seen = true
					scan_start = i
					function_start = i # Set the start of the _next_ function.
					lparen = 0
				else: i += 1
				#@-body
				#@-node:3::<< handle open curly bracket in C >>

			elif is_c_id(ch):
				
				#@<< skip c identif ier, typedef, struct, union, namespace >>
				#@+node:4::<< skip c identifier, typedef, struct, union, namespace >>
				#@+body
				if match_c_word(s,i,"typedef"):
					i = skip_typedef(s,i)
					lparen = None
				elif match_c_word(s,i,"struct"):
					i = skip_typedef(s,i)
					# lparen = NULL ;  # This can appear in an argument list.
				elif match_c_word(s,i,"union"):
					i = skip_typedef(s,i)
					# lparen = NULL ;  # This can appear in an argument list.
				elif match_c_word(s,i,"namespace"):
					
					#@<< Create children for the namespace >>
					#@+node:2::<< Create children for the namespace >>
					#@+body
					# skip the "namespace" keyword.
					i += 9
					i = skip_ws_and_nl(s,i)
					# Skip the namespace name.
					namespace_name_start = i
					namespace_name_end = None
					if i < len(s) and is_c_id(s[i]):
						i = skip_c_id(s,i)
						namespace_name_end = i - 1
					else: namespace_name_start = None
					# Skip the '{'
					i = skip_ws_and_nl(s,i)
					if i < len(s) and s[i] == '{' and namespace_name_start:
						inner_ip = i + 1
						i = skip_braces(s,i)
						if i < len(s) and s[i] == '}':
							# Append everything so far to the body.
							if inner_ip > scan_start:
								parent.appendStringToBody(s[scan_start:inner_ip])
							# Save and change gModuleName to namespaceName
							savedMethodName = self.methodName
							namespaceName = s[namespace_name_start:namespace_name_end]
							self.methodName = "namespace " + namespaceName
							# Recursively call this function .
							self.scanCText(s[inner_ip:],parent)
							# Restore gModuleName and continue scanning.
							savedMethodName = savedMethodName
							scan_start = i
							function_start = i
					#@-body
					#@-node:2::<< Create children for the namespace >>

				else:
					# Remember the last name before an open parenthesis.
					if lparen == None:
						name_start = i
					i = skip_c_id(s,i)
					if lparen == None:
						name_end = i - 1
					
					#@<< test for operator keyword >>
					#@+node:1::<< test for operator keyword >>
					#@+body
					# We treat a C++ a construct such as operator + as a function name.
					if match(s[name_start:name_end],0,"operator"):
						i = skip_ws(s,i) # Don't allow newline in headline.
						if  i < len(s) and not is_c_id(s[i]) and s[i] != ' ' and s[i] != '\n' and s[i] != '\r':
							while i < len(s) and not is_c_id(s[i]) and s[i] != ' ' and s[i] != '\n' and s[i] != '\r':
								i += 1
							name_end = i - 1
					#@-body
					#@-node:1::<< test for operator keyword >>
				#@-body
				#@-node:4::<< skip c identifier, typedef, struct, union, namespace >>

			else: i += 1
		
		#@<< Append any unused text to the parent's body text >>
		#@+node:6:C=8:<< Append any unused text to the parent's body text >>
		#@+body
		# Used by C, Java and Pascal parsers.
		# Do nothing if only whitespace is left.
		
		i = skip_ws_and_nl(s,scan_start)
		if i < len(s):
			parent.appendStringToBody(s[scan_start:])
		#@-body
		#@-node:6:C=8:<< Append any unused text to the parent's body text >>
	#@-body
	#@+node:5:C=7:Shared by C and Java
	#@-node:5:C=7:Shared by C and Java
	#@-node:2::scanCText
	#@+node:3::scanPascalText
	#@+body
	#@+at
	#  Creates a child of parent for each Pascal function definition seen.  See the comments for scanCText for what the text looks like.

	#@-at
	#@@c
	
	def scanPascalText (self,s,parent):
	
		trace(`get_line(s,0)`)
		method_seen = false
		methodKind = "methods"
		
		#@<< Initialize the ImportFiles private globals >>
		#@+node:1:C=6:<< Initialize the ImportFiles private globals >>
		#@+body
		# Shared by several routines...
		scan_start = i = 0
		function_start = i
		function_end = None
		name_start = name_end = None
		#@-body
		#@-node:1:C=6:<< Initialize the ImportFiles private globals >>

		while i < len(s):
			ch = s[i]
			if ch == '{':
				i = skip_pascal_braces(s,i)
			elif ch == '/':
				
				#@<< handle possible Pascal single-line comment >>
				#@+node:2::<< handle possible Pascal function >>
				#@+node:4::<< skip the function definition, or continue >>
				#@+node:1::<< skip past the semicolon >>
				#@+node:1::<< handle possible Pascal single-line comment >>
				#@+body
				i += 1 # skip the opening '/'
				if  i < len(s) and s[i] == '/':
					i = skip_to_end_of_line(s,i)
				#@-body
				#@-node:1::<< handle possible Pascal single-line comment >>
				#@-node:1::<< skip past the semicolon >>
				#@-node:4::<< skip the function definition, or continue >>
				#@-node:2::<< handle possible Pascal function >>

			elif ch == '(':
				
				#@<< handle possible Pascal block comment >>
				#@+node:2::<< handle possible Pascal function >>
				#@+node:4::<< skip the function definition, or continue >>
				#@+node:1::<< skip past the semicolon >>
				#@+node:2::<< handle possible Pascal block comment >>
				#@+body
				i += 1 # skip the '('
				if  i < len(s) and s[i] == '*':
					i += 1 # skip the '*'
					i = skip_pascal_block_comment(s,i)
				#@-body
				#@-node:2::<< handle possible Pascal block comment >>
				#@-node:1::<< skip past the semicolon >>
				#@-node:4::<< skip the function definition, or continue >>
				#@-node:2::<< handle possible Pascal function >>

			elif ch == '"' or ch == '\'':
				i = skip_pascal_string(s,i)
			elif is_c_id(s[i]):
				
				#@<< handle possible Pascal function >>
				#@+node:2::<< handle possible Pascal function >>
				#@+body
				if match_c_word(s,i,"begin"):
					i = skip_pascal_begin_end(s,i)
					if match_c_word(s,i,"end"):
						i = skip_c_id(s,i)
				elif (match_c_word(s,i,"function")  or match_c_word(s,i,"procedure") or
					match_c_word(s,i,"constructor") or match_c_word(s,i,"destructor")):
					start = i
					i = skip_c_id(s,i)
					i = skip_ws_and_nl(s,i)
					
					#@<< remember the function name, or continue >>
					#@+node:3::<< remember the function name, or continue >>
					#@+body
					if i < len(s) and is_c_id(s[i]):
						name_start = i
						i = skip_c_id(s,i)
						while i + 1 < len(s) and s[i] == '.' and is_c_id(s[i+1]):
							i += 1
							name_start = i
							i = skip_c_id(s,i)
						name_end = i - 1
					else: continue
					#@-body
					#@-node:3::<< remember the function name, or continue >>

					
					#@<< skip the function definition, or continue >>
					#@+node:4::<< skip the function definition, or continue >>
					#@+body
					
					#@<< skip past the semicolon >>
					#@+node:1::<< skip past the semicolon >>
					#@+body
					while i < len(s) and s[i] != ';':
						# The paremeter list may contain "inner" semicolons.
						if s[i] == '(':
							i = skip_parens(s,i)
							if i < len(s) and s[i] == ')':
								i += 1
							else: break
						else: i += 1
					if i < len(s) and s[i] == ';':
						i += 1
					i = skip_ws_and_nl(s,i)
					if match_c_word(s,i,"var"):
						# Skip to the next begin.
						i = skip_c_id(s,i)
						done = false
						while i < len(s) and not done:
							ch = s[i]
							if ch == '{':
								i = skip_pascal_braces(s,i)
							elif ch == '/':
								
								#@<< handle possible Pascal single-line comment >>
								#@+node:1::<< handle possible Pascal single-line comment >>
								#@+body
								i += 1 # skip the opening '/'
								if  i < len(s) and s[i] == '/':
									i = skip_to_end_of_line(s,i)
								#@-body
								#@-node:1::<< handle possible Pascal single-line comment >>

							elif ch == '(':
								
								#@<< handle possible Pascal block comment >>
								#@+node:2::<< handle possible Pascal block comment >>
								#@+body
								i += 1 # skip the '('
								if  i < len(s) and s[i] == '*':
									i += 1 # skip the '*'
									i = skip_pascal_block_comment(s,i)
								#@-body
								#@-node:2::<< handle possible Pascal block comment >>

							elif ch == '"' or ch == '\'':
								i = skip_pascal_string(s,i)
							elif match_c_word(s,i,"begin"):
								done = true
							else: i += 1
					#@-body
					#@-node:1::<< skip past the semicolon >>

					if not match_c_word(s,i,"begin"):
						continue
					# Skip to the matching end.
					i = skip_pascal_begin_end(s,i)
					if match_c_word(s,i,"end"):
						i = skip_c_id(s,i)
						i = skip_ws_and_nl(s,i)
						if i < len(s) and s[i] == ';':
							i += 1
						i = skip_ws(s,i)
						if i < len(s) and(s[i] == '\n' or s[i] == '\r'):
							i = skip_nl(s,i)
					else: continue
					#@-body
					#@-node:4::<< skip the function definition, or continue >>

					if method_seen == false:
						method_seen = true
						
						#@<< create a child node for leading declarations >>
						#@+node:1::<< create a child node for leading declarations >>
						#@+body
						save_ip = i
						i = scan_start
						while i < start and is_ws_or_nl(s,i):
							i += 1
						if i < start:
							headline = angleBrackets(self.methodName + " declarations ")
							# Append the headline to the parent's body.
							parent.appendStringToBody(headline + "\n")
							body = "@code\n\n" + s[scan_start:start]
							self.createHeadline(parent,body,headline)
						i = save_ip
						scan_start = i
						#@-body
						#@-node:1::<< create a child node for leading declarations >>

						
						#@<< append noweb method reference to the parent node >>
						#@+node:5::<< append noweb method reference to the parent node >>
						#@+body
						# Append the headline to the parent's body.
						ref = angleBrackets(" " + self.methodName + " methods ")
						parent.appendStringToBody(ref + "\n")
						#@-body
						#@-node:5::<< append noweb method reference to the parent node >>

						function_start = start
					else: function_start = scan_start
					
					#@<< create a child node for the function >>
					#@+node:2::<< create a child node for the function >>
					#@+body
					# Point i _after_ the last character of the function.
					i = skip_ws(s,i)
					if i < len(s) and(s[i] == '\r' or s[i] == '\n'):
						i = skip_nl(s,i)
					function_end = i
					length = name_end - name_start + 1
					headline = (name_start,length)
					body = s[function_start:function_end]
					body = self.massageBody(body,methodKind)
					self.createHeadline(parent,body,headline)
					scan_start = i
					#@-body
					#@-node:2::<< create a child node for the function >>

				else: i = skip_c_id(s,i)
				#@-body
				#@-node:2::<< handle possible Pascal function >>

			else: i += 1
		
		#@<< Append any unused text to the parent's body text >>
		#@+node:3:C=8:<< Append any unused text to the parent's body text >>
		#@+body
		# Used by C, Java and Pascal parsers.
		# Do nothing if only whitespace is left.
		
		i = skip_ws_and_nl(s,scan_start)
		if i < len(s):
			parent.appendStringToBody(s[scan_start:])
		#@-body
		#@-node:3:C=8:<< Append any unused text to the parent's body text >>
	#@-body
	#@-node:3::scanPascalText
	#@+node:4::Python scanners
	#@+node:1::scanPythonClass
	#@+body
	#@+at
	#  Creates a child node c of parent for the class, and children of c for each def in the class.

	#@-at
	#@@c
	
	def scanPythonClass (self,s,i,parent):
	
		trace(`get_line(s,i)`)
		start = i
		
		#@<< set classname and headline, or return i >>
		#@+node:1::<< set classname and headline, or return i >>
		#@+body
		# Skip to the class name.
		i = skip_ws(s,i)
		i = skip_c_id(s,i) # skip "class"
		i = skip_ws_and_nl(s,i)
		if i < len(s) and is_c_id(s[i]):
			j = i ; i = skip_c_id(s,i)
			classname = s[j:i]
			headline = "class " + classname
		else: return i
		#@-body
		#@-node:1::<< set classname and headline, or return i >>

		i = skip_line(s,0) # Skip the class line.
		
		#@<< create class_vnode >>
		#@+node:2::<< create class_vnode  >>
		#@+body
		# Create the section name using the old value of self.methodName.
		body = angleBrackets(" " + self.methodName + " methods ") + "=\n\n"
		# i points just after the class line.
		body2 = s[start:i]
		body2 = self.undentPythonBody(body2)
		body += body2
		class_vnode = self.createHeadline(parent,body,headline)
		#@-body
		#@-node:2::<< create class_vnode  >>

		savedMethodName = self.methodName
		self.methodName = headline
		# Create a node for leading declarations of the class.
		i = self.scanPythonDecls(s,class_vnode,indent_refs)
		
		#@<< append a reference to class_vnode's methods >>
		#@+node:3::<< Append a reference to class_vnode's methods >>
		#@+body
		# This must be done after the declaration reference is generated.
		ref = "\t" + angleBrackets(" class " + classname + " methods ")
		class_vnode.appendStringToBody(ref + "\n\n")
		#@-body
		#@-node:3::<< Append a reference to class_vnode's methods >>

		
		#@<< create nodes for all defs of the class >>
		#@+node:4::<< create nodes for all defs of the class >>
		#@+body
		line_start = find_line_start(s,i)
		indent1 = self.getPythonIndent(s[line_start:],0)
		# Skip past blank lines.
		i = skip_blank_lines(s,i)
		start = i
		indent = indent1
		while i < len(s) and indent >= indent1:
			progress = i
			if is_nl(s,i):
				j = skip_nl(s,i)
				indent = self.getPythonIndent(s,j)
				if indent >= indent1: i = j
			elif match_c_word(s,i,"def"):
				j = self.scanPythonDef(s,i,class_vnode)
				i += j ; start = i
				indent = self.getPythonIndent(s,i)
			elif match_c_word(s,i,"class"):
				start = i = self.scanPythonClass(s,start,class_vnode)
				indent = self.getPythonIndent(s,i)
			elif s[i] == '#':
				i = skip_to_end_of_line(s,i)
			elif s[i] == '"' or s[i] == '\'':
				i = skip_python_string(s,i)
			else: i += 1
			assert(progress < i)
		#@-body
		#@-node:4::<< create nodes for all defs of the class >>

		self.methodName = savedMethodName
		return i
	#@-body
	#@-node:1::scanPythonClass
	#@+node:2::scanPythonDef
	#@+body
	#@+at
	#  Creates a node of parent for the def.

	#@-at
	#@@c
	
	def scanPythonDef (self,s,i,parent):
	
		trace(`get_line(s,i)`)
		start = i
		
		#@<< set headline or return i >>
		#@+node:1::<< set headline or return i >>
		#@+body
		i = skip_ws(s,0)
		i = skip_c_id(s,i) # Skip the "def"
		i = skip_ws_and_nl(s,i)
		if i < len(s) and is_c_id(s[i]):
			j = i ; i = skip_c_id(s,i)
			headline = s[j:i]
			trace("headline:" + `headline`)
		else: return i
		#@-body
		#@-node:1::<< set headline or return i >>

		
		#@<< skip the Python def >>
		#@+node:2::<< skip the Python def >>
		#@+body
		# This doesn't handle nested defs or classes.  It should.
		# Set indent1 to the indentation of the def line.
		
		line_start = find_line_start(s,start)
		indent1 = self.getPythonIndent(s[line_start:],0)
		i = skip_line(s,i) # Skip the def line.
		indent = self.getPythonIndent(s,i)
		while i < len(s) and indent >= indent1:
			progress = i
			ch = s[i]
			if is_nl(s,i):
				i = skip_nl(s,i)
				indent = self.getPythonIndent(s,i)
				if indent <= indent1: break
			elif ch == '#': i = skip_line(s,i)
			elif ch == '"' or ch == '\'': i = skip_python_string(s,i)
			else: i += 1
			assert(progress < i)
		#@-body
		#@-node:2::<< skip the Python def >>

		# Create the def node.
		savedMethodName = self.methodName
		self.methodName = headline
		
		#@<< Create def node >>
		#@+node:3::<< Create def node >>
		#@+body
		# Create the header line.
		body = angleBrackets(" " + savedMethodName + " methods ") + "=\n\n"
		# Create body.
		start = skip_blank_lines(s,start)
		body2 = s[:i]
		body2 = self.undentPythonBody(body2)
		body += body2
		# Create the node.
		self.createHeadline(parent,body,headline)
		#@-body
		#@-node:3::<< Create def node >>

		self.methodName = savedMethodName
		return i
	#@-body
	#@-node:2::scanPythonDef
	#@+node:3::scanPythonDecls
	#@+body
	def scanPythonDecls (self,s,parent,indent_parent_ref_flag):
		
		j = skip_to_end_of_line(s,0) ; trace(s[:j])
		i = 0 ; done = false
		while not done and i < len(s):
			progress = i
			ch = s[i]
			if ch == '\n': i = skip_nl(s,i)
			elif ch == '#': i = skip_to_end_of_line(s,i)
			elif ch == '"' or ch == '\'': i = skip_python_string(s,i)
			elif is_c_id(s[i]):
				
				#@<< break on def or class >>
				#@+node:1::<< break on def or class >>
				#@+body
				if match_c_word(s,i,"def") or match_c_word(s,i,"class"):
					i = find_line_start(s,i)
					done = true
					break
				else:
					i = skip_c_id(s,i)
				#@-body
				#@-node:1::<< break on def or class >>

			else: i += 1
			assert(progress < i)
		j = skip_blank_lines(s,0)
		if is_nl(s,j):
			j = skip_nl(s,j)
		if j < i:
			
			#@<< Create a child node for declarations >>
			#@+node:2::<< Create a child node for declarations >>
			#@+body
			# Create the body.
			body = "@code\n\n" + s[j:i]
			body = self.undentPythonBody(body)
			# Create the headline.
			headline = angleBrackets(" " + self.methodName + " declarations ")
			# Append the headline to the parent's body.
			ctab = choose(indent_parent_ref_flag,"\t","")
			parent.appendStringToBody(ctab + headline + "\n")
			# Create the node for the decls
			self.createHeadline(parent,body,headline)
			#@-body
			#@-node:2::<< Create a child node for declarations >>

		return i
	#@-body
	#@-node:3::scanPythonDecls
	#@+node:4::scanPythonText
	#@+body
	#@+at
	#  This code creates a child of parent for each Python function definition seen.  See the comments for scanCText for what the 
	# text looks like.

	#@-at
	#@@c
	
	def scanPythonText (self,s,parent):
		
		j = skip_to_end_of_line(s,0) ; trace(s[:j])
		decls_seen = false
		start = i = 0
		while i < len(s):
			progress = i
			# j = skip_line(s,i) ; trace(s[i:j])
			ch = s[i]
			if ch == '\n': i = skip_nl(s,i)
			elif ch == '#': i = skip_to_end_of_line(s,i)
			elif ch == '"' or ch == '\'': i = skip_python_string(s,i)
			elif is_c_id(ch):
				
				#@<< handle possible Python function or class >>
				#@+node:1::<< handle possible Python function or class >>
				#@+body
				if match_c_word(s,i,"def"):
					if not decls_seen:
						j = self.scanPythonDecls(s[i:],parent,dont_indent_refs)
						i += j ; start = i
						decls_seen = true
					j = self.scanPythonDef(s,i,parent)
					i += j ; start = i
				elif match_c_word(s,i,"class"):
					if not decls_seen:
						j = self.scanPythonDecls(s[start:],parent,dont_indent_refs)
						i = start + j ; start = i
						decls_seen = true
					j = self.scanPythonClass(s,start,parent)
					i = start + j ; start = i
				else:
					i = skip_c_id(s,i)
				#@-body
				#@-node:1::<< handle possible Python function or class >>

			else: i += 1
			assert(progress < i)
		
		#@<< Append a reference to the methods of this file >>
		#@+node:2::<< Append a reference to the methods of this file >>
		#@+body
		ref = angleBrackets(" " + self.methodName + " methods ")
		parent.appendStringToBody(ref + "\n\n")
		#@-body
		#@-node:2::<< Append a reference to the methods of this file >>

		
		#@<< Append any unused python text to the parent's body text >>
		#@+node:3::<< Append any unused python text to the parent's body text >>
		#@+body
		# Do nothing if only whitespace is left.
		i = start ; i = skip_ws_and_nl(s,i)
		if i < len(s):
			parent.appendStringToBody(s[start:])
		#@-body
		#@-node:3::<< Append any unused python text to the parent's body text >>
	#@-body
	#@-node:4::scanPythonText
	#@-node:4::Python scanners
	#@-node:6::Language Specific
	#@-others

#@-body
#@-node:0::@file leoImport.py
#@-leo
