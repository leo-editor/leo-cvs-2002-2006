#@+leo
#@+node:0::@file leoImport.py
#@+body
#@@language python

from leoGlobals import *
from leoUtils import *
import traceback

# Synonyms
indent_refs = true ; dont_indent_refs = false


#@<< scripts >>
#@+node:2::<< scripts >>
#@+body
#@+others
#@+node:1::importFiles
#@+body
# An example of running this script:
#
# import leoImport
# leoImport.importFiles("c:/prog/test", ".py")

def importFiles (dir, type = None, kind = "@file"):
	
	import os,traceback

	# Check the params.
	if kind != "@file" and kind != "@root":
		es("kind must be @file or @root: " + `kind`)
		return
	if not os.path.exists(dir):
		es("directory does not exist: " + `dir`)
		return
	
	c = top() # Get the commander.
	
	try:
		files = os.listdir(dir)
		files2 = []
		for f in files:
			path = os.path.join(dir,f)
			if os.path.isfile(path):
				name, ext = os.path.splitext(f)
				if type == None or ext == type:
					files2.append(path)
		if len(files2) > 0:
			c.importCommands.importFilesCommand(files2,kind)
	except:
		es("exception in importFiles script")
		es_exception()
#@-body
#@-node:1::importFiles
#@-others
#@-body
#@-node:2::<< scripts >>


class leoImportCommands:

	#@+others
	#@+node:1::import.__init__
	#@+body
	def __init__ (self,commands):
	
		self.commands = commands
		
		# Set by ImportFilesFommand.
		self.treeType = "@file" # "@root" or "@file"
		# Set by ImportWebCommand.
		self.webType = "@noweb" # "cweb" or "noweb"
	
		# Set by create_outline.
		self.fileName = None # The original file name, say x.cpp
		self.methodName = None # x, as in < < x methods > > =
		self.fileType = None # ".py", ".c", etc.
		self.rootLine = "" # Empty or @root + self.fileName
	
		# Support of output_newline option
		self.output_newline = getOutputNewline()
		
		# Used by Importers.
		self.web_st = []
	
	#@-body
	#@-node:1::import.__init__
	#@+node:3::Import
	#@+node:1::createOutline
	#@+body
	def createOutline (self,fileName,parent):
	
		c = self.commands ; current = c.currentVnode()
		junk, self.fileName = os.path.split(fileName) # junk/fileName
		self.methodName, type = os.path.splitext(self.fileName) # methodName.fileType
		self.fileType = type
		# trace(`self.fileName`) ; trace(`self.fileType`)
		# All file types except the following just get copied to the parent node.
		# 08-SEP-2002 DTHEIN: Added php
		# 9/9/02: E.K.Ream.  Allow upper case, add cxx.
		# Note: we should _not_ import header files using this code.
		appendFileFlag = string.lower(type) not in [".c", ".cpp", ".cxx", ".java", ".pas", ".py", ".php"]
		
		#@<< Read file into s >>
		#@+node:1::<< Read file into s >>
		#@+body
		try:
			file = open(fileName)
			s = file.read()
			file.close()
		except:
			es("can not read " + fileName)
			return None
		#@-body
		#@-node:1::<< Read file into s >>

		# Create the top-level headline.
		v = parent.insertAsLastChild()
		c.undoer.setUndoParams("Import",v,select=current)
		if self.treeType == "@file":
			v.initHeadString("@file " + self.fileName)
		else:
			v.initHeadString(self.fileName)
			
		self.rootLine = choose(self.treeType=="@file","","@root "+self.fileName+'\n')
	
		if appendFileFlag:
			v.setBodyStringOrPane("@ignore\n" + self.rootLine + s)
		elif type == ".c" or type == ".cpp":
			self.scanCText(s,v)
		elif type == ".java":
			self.scanJavaText(s,v,true) #outer level
		elif type == ".pas":
			self.scanPascalText(s,v)
		elif type == ".py":
			self.scanPythonText(s,v)
		elif type == ".php":
			self.scanPHPText(s,v) # 08-SEP-2002 DTHEIN
		else:
			es("createOutline: can't happen")
		return v
	#@-body
	#@-node:1::createOutline
	#@+node:2::importFilesCommand
	#@+body
	def importFilesCommand (self,files,treeType):
	
		c = self.commands
		if c == None: return
		v = current = c.currentVnode()
		if current == None: return
		if len(files) < 1: return
		self.treeType = treeType
		c.beginUpdate()
		if 1: # range of update...
			if len(files) == 2:
				
				#@<< Create a parent for two files having a common prefix >>
				#@+node:1::<< Create a parent for two files having a common prefix >>
				#@+body
				#@+at
				#  The two filenames have a common prefix everything before 
				# the last period is the same.  For example, x.h and x.cpp.

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

			for i in xrange(len(files)):
				fileName = files[i]
				v = self.createOutline(fileName,current)
				if v: # 8/11/02: createOutline may fail.
					es("imported " + fileName)
					c.contractVnode(v)
					v.setDirty()
					c.setChanged(true)
			c.validateOutline()
			c.expandVnode(current)
		c.endUpdate()
		c.selectVnode(current)
	#@-body
	#@-node:2::importFilesCommand
	#@+node:3::importFlattenedOutline & allies
	#@+node:1::convertMoreString/StringsToOutlineAfter
	#@+body
	# Used by paste logic.
	
	def convertMoreStringToOutlineAfter (self,s,firstVnode):
		s = string.replace(s,"\r","")
		strings = string.split(s,"\n")
		return self.convertMoreStringsToOutlineAfter(strings,firstVnode)
	
	# Almost all the time spent in this command is spent here.
	
	def convertMoreStringsToOutlineAfter (self,strings,firstVnode):
	
		c = self.commands
		if len(strings) == 0: return None
		if not self.stringsAreValidMoreFile(strings): return None
		c.beginUpdate()
		firstLevel, junk = self.moreHeadlineLevel(strings[0])
		lastLevel = -1 ; theRoot = lastVnode = None
		index = 0
		while index < len(strings):
			progress = index
			s = strings[index]
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
				while match(s,j,'\t'):
					j += 1
				if match(s,j,"+ ") or match(s,j,"- "):
					j += 2
				
				v.initHeadString(s[j:])
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
			assert progress < index
		if theRoot:
			theRoot.setDirty()
			c.setChanged(true)
		c.endUpdate()
		return theRoot
	#@-body
	#@-node:1::convertMoreString/StringsToOutlineAfter
	#@+node:2::importFlattenedOutline
	#@+body
	# On entry,files contains at most one file to convert.
	def importFlattenedOutline (self,files):
	
		c = self.commands ; current = c.currentVnode()
		if current == None: return
		if len(files) < 1: return
		fileName = files[0]
		
		#@<< Read the file into array >>
		#@+node:1::<< Read the file into array >>
		#@+body
		try:
			file = open(fileName)
			s = file.read()
			s = string.replace(s,"\r","")
			array = string.split(s,"\n")
			file.close()
		except: array = []
		#@-body
		#@-node:1::<< Read the file into array >>

		# Convert the string to an outline and insert it after the current node.
		newVnode = self.convertMoreStringsToOutlineAfter(array,current)
		if newVnode:
			c.undoer.setUndoParams("Import",newVnode,select=current)
			c.endEditing()
			c.validateOutline()
			c.editVnode(newVnode)
			newVnode.setDirty()
			c.setChanged(true)
		else:
			es(fileName + " is not a valid MORE file.")
	#@-body
	#@-node:2::importFlattenedOutline
	#@+node:3::moreHeadlineLevel
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
	#@-node:3::moreHeadlineLevel
	#@+node:4::stringIs/stringsAreValidMoreFile
	#@+body
	# Used by paste logic.
	
	def stringIsValidMoreFile (self,s):
		
		s = string.replace(s,"\r","")
		strings = string.split(s,"\n")
		return self.stringsAreValidMoreFile(strings)
	
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
	#@-node:4::stringIs/stringsAreValidMoreFile
	#@-node:3::importFlattenedOutline & allies
	#@+node:4::importWebCommand & allies
	#@+node:1::createOutlineFromWeb
	#@+body
	def createOutlineFromWeb (self,path,parent):
	
		c = self.commands ; current = c.currentVnode()
		junk, fileName = os.path.split(path)
		# Create the top-level headline.
		v = parent.insertAsLastChild()
		c.undoer.setUndoParams("Import",v,select=current)
		v.initHeadString(fileName)
		if self.webType=="cweb":
			v.setBodyStringOrPane("@ignore\n" + self.rootLine + "@language cweb")
	
		# Scan the file,creating one section for each function definition.
		self.scanWebFile(path,v)
		return v
	#@-body
	#@-node:1::createOutlineFromWeb
	#@+node:2::importWebCommand
	#@+body
	def importWebCommand (self,files,webType):
	
		c = self.commands ; current = c.currentVnode()
		if current == None: return
		if len(files) < 1: return
		self.webType = webType
		c.beginUpdate()
		for i in xrange(len(files)):
			fileName = files[i]
			v = self.createOutlineFromWeb(fileName,current)
			c.contractVnode(v)
			v.setDirty()
			c.setChanged(true)
		c.selectVnode(current)
		c.endUpdate()
	#@-body
	#@-node:2::importWebCommand
	#@+node:3::findFunctionDef
	#@+body
	def findFunctionDef (self,s,i):
		
		# Look at the next non-blank line for a function name.
		i = skip_ws_and_nl(s,i)
		k = skip_line(s,i)
		name = None
		while i < k:
			if is_c_id(s[i]):
				j = i ; i = skip_c_id(s,i) ; name = s[j:i]
			elif s[i] == '(':
				if name: return name
				else: break
			else: i += 1
		return None
	#@-body
	#@-node:3::findFunctionDef
	#@+node:4::scanBodyForHeadline
	#@+body
	#@+at
	#  This method returns the proper headline text.
	# 
	# 1. If s contains a section def, return the section ref.
	# 2. cweb only: if s contains @c, return the function name following the @c.
	# 3. cweb only: if s contains @d name, returns @d name.
	# 4. Otherwise, returns "@"

	#@-at
	#@@c

	def scanBodyForHeadline (self,s):
		
		if self.webType == "cweb":
			
			#@<< scan cweb body for headline >>
			#@+node:1::<< scan cweb body for headline >>
			#@+body
			i = 0
			while i < len(s):
				i = skip_ws_and_nl(s,i)
				# line = get_line(s,i) ; trace(`line`)
				# Allow constructs such as @ @c, or @ @<.
				if self.isDocStart(s,i):
					i += 2 ; i = skip_ws(s,i)
				if match(s,i,"@d") or match(s,i,"@f"):
					# Look for a macro name.
					directive = s[i:i+2]
					i = skip_ws(s,i+2) # skip the @d or @f
					if i < len(s) and is_c_id(s[i]):
						j = i ; skip_c_id(s,i) ; return s[j:i]
					else: return directive
				elif match(s,i,"@c") or match(s,i,"@p"):
					# Look for a function def.
					name = self.findFunctionDef(s,i+2)
					return choose(name,name,"outer function")
				elif match(s,i,"@<"):
					# Look for a section def.
					# A small bug: the section def must end on this line.
					j = i ; k = find_on_line(s,i,"@>")
					if k > -1 and (match(s,k+2,"+=") or match(s,k+2,"=")):
						return s[j:k+2] # return the section ref.
				i = skip_line(s,i)
			#@-body
			#@-node:1::<< scan cweb body for headline >>

		else:
			
			#@<< scan noweb body for headline >>
			#@+node:2::<< scan noweb body for headline >>
			#@+body
			i = 0
			while i < len(s):
				i = skip_ws_and_nl(s,i)
				# line = get_line(s,i) ; trace(`line`)
				if match(s,i,"<<"):
					k = find_on_line(s,i,">>=")
					if k > -1:
						ref = s[i:k+2]
						name = string.strip(s[i+2:k])
						if name != "@others":
							return ref
				else:
					name = self.findFunctionDef(s,i)
					if name:
						return name
				i = skip_line(s,i)
			#@-body
			#@-node:2::<< scan noweb body for headline >>

		return "@" # default.
	#@-body
	#@-node:4::scanBodyForHeadline
	#@+node:5::scanWebFile (handles limbo)
	#@+body
	def scanWebFile (self,fileName,parent):
	
		type = self.webType
		lb = choose(type=="cweb","@<","<<")
		rb = choose(type=="cweb","@>",">>")
	
		try: # Read the file into s.
			f = open(fileName)
			s = f.read()
		except: s = None
	
		
		#@<< Create a symbol table of all section names >>
		#@+node:1::<< Create a symbol table of all section names >>
		#@+body
		i = 0 ; 	self.web_st = []
		while i < len(s):
			i = skip_ws_and_nl(s,i)
			# line = get_line(s,i) ; trace(`line`)
			if self.isDocStart(s,i):
				if type == "cweb": i += 2
				else: i = skip_line(s,i)
			elif type == "cweb" and match(s,i,"@@"):
				i += 2
			elif match(s,i,lb):
				i += 2 ; j = i ; k = find_on_line(s,j,rb)
				if k > -1: self.cstEnter(s[j:k])
			else: i += 1
		
		# trace(self.cstDump())
		#@-body
		#@-node:1::<< Create a symbol table of all section names >>

		
		#@<< Create nodes for limbo text and the root section >>
		#@+node:2::<< Create nodes for limbo text and the root section >>
		#@+body
		i = 0
		while i < len(s):
			i = skip_ws_and_nl(s,i)
			if self.isModuleStart(s,i) or match(s,i,lb):
				break
			else: i = skip_line(s,i)
			
		j = skip_ws(s,0)
		if j < i:
			self.createHeadline(parent,"@ " + s[j:i],"Limbo")
		
		j = i
		if match(s,i,lb):
			while i < len(s):
				i = skip_ws_and_nl(s,i)
				if self.isModuleStart(s,i):
					break
				else: i = skip_line(s,i)
			self.createHeadline(parent,s[j:i],angleBrackets(" @ "))
			
		# trace(`get_line(s,i)`)
		#@-body
		#@-node:2::<< Create nodes for limbo text and the root section >>

		while i < len(s):
			progress = i
			
			#@<< Create a node for the next module >>
			#@+node:3::<< Create a node for the next module >>
			#@+body
			if type=="cweb":
				assert(self.isModuleStart(s,i))
				start = i
				if self.isDocStart(s,i):
					i += 2
					while i < len(s):
						i = skip_ws_and_nl(s,i)
						if self.isModuleStart(s,i): break
						else: i = skip_line(s,i)
				
				#@<< Handle cweb @d, @f, @c and @p directives >>
				#@+node:1::<< Handle cweb @d, @f, @c and @p directives >>
				#@+body
				if match(s,i,"@d") or match(s,i,"@f"):
					i += 2 ; i = skip_line(s,i)
					# Place all @d and @f directives in the same node.
					while i < len(s):
						i = skip_ws_and_nl(s,i)
						if match(s,i,"@d") or match(s,i,"@f"): i = skip_line(s,i)
						else: break
					i = skip_ws_and_nl(s,i)
					
				while i < len(s) and not self.isModuleStart(s,i):
					i = skip_line(s,i)
					i = skip_ws_and_nl(s,i)
				
				if match(s,i,"@c") or match(s,i,"@p"):
					i += 2 ; 
					while i < len(s):
						i = skip_line(s,i)
						i = skip_ws_and_nl(s,i)
						if self.isModuleStart(s,i):
							break
				#@-body
				#@-node:1::<< Handle cweb @d, @f, @c and @p directives >>

			else:
				assert(self.isDocStart(s,i)) # isModuleStart == isDocStart for noweb.
				start = i ; i = skip_line(s,i)
				while i < len(s):
					i = skip_ws_and_nl(s,i)
					if self.isDocStart(s,i): break
					else: i = skip_line(s,i)
				
			body = s[start:i]
			body = self.massageWebBody(body)
			headline = self.scanBodyForHeadline(body)
			self.createHeadline(parent,body,headline)
			#@-body
			#@-node:3::<< Create a node for the next module >>

			assert(progress < i)
	#@-body
	#@-node:5::scanWebFile (handles limbo)
	#@+node:6::Symbol table
	#@+node:1::cstCanonicalize
	#@+body
	#@+at
	#  We canonicalize strings before looking them up, but strings are entered 
	# in the form they are first encountered.

	#@-at
	#@@c

	def cstCanonicalize (self,s,lower=true):
		
		if lower:
			s = string.lower(s)
		s = string.replace(s,"\t"," ")
		s = string.replace(s,"\r","")
		s = string.replace(s,"\n"," ")
		s = string.replace(s,"  "," ")
		s = string.strip(s)
		return s
	#@-body
	#@-node:1::cstCanonicalize
	#@+node:2::cstDump
	#@+body
	def cstDump (self):
	
		self.web_st.sort()
		s = "Web Symbol Table...\n\n"
		for name in self.web_st:
			s += name + "\n"
		return s
	#@-body
	#@-node:2::cstDump
	#@+node:3::cstEnter
	#@+body
	# We only enter the section name into the symbol table if the ... convention is not used.
	
	def cstEnter (self,s):
	
		# Don't enter names that end in "..."
		s = string.rstrip(s)
		if s.endswith("..."): return
		
		# Put the section name in the symbol table, retaining capitalization.
		lower = self.cstCanonicalize(s,true)  # do lower
		upper = self.cstCanonicalize(s,false) # don't lower.
		for name in self.web_st:
			if string.lower(name) == lower:
				return
		self.web_st.append(upper)
	#@-body
	#@-node:3::cstEnter
	#@+node:4::cstLookup
	#@+body
	# This method returns a string if the indicated string is a prefix of an entry in the web_st.
	
	def cstLookup (self,target):
		
		# Do nothing if the ... convention is not used.
		target = string.strip(target)
		if not target.endswith("..."): return target
		# Canonicalize the target name, and remove the trailing "..."
		ctarget = target[:-3]
		ctarget = self.cstCanonicalize(ctarget)
		ctarget = string.strip(ctarget)
		found = false ; result = target
		for s in self.web_st:
			cs = self.cstCanonicalize(s)
			if cs[:len(ctarget)] == ctarget:
				if found:
					es("****** " + target + ": is also a prefix of: " + s)
				else:
					found = true ; result = s
					# es("replacing: " + target + " with: " + s)
		return result
	#@-body
	#@-node:4::cstLookup
	#@-node:6::Symbol table
	#@-node:4::importWebCommand & allies
	#@+node:5::Scanners for createOutline
	#@+node:1::Python scanners
	#@+node:1::scanPythonClass
	#@+body
	#@+at
	#  Creates a child node c of parent for the class, and children of c for 
	# each def in the class.

	#@-at
	#@@c

	def scanPythonClass (self,s,i,start,parent):
	
		# line = get_line(s,i) ; trace(`line`)
		classIndent = self.getLeadingIndent(s,i)
		
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
		else:
			return i
		#@-body
		#@-node:1::<< set classname and headline, or return i >>

		i = skip_line(s,i) # Skip the class line.
		
		#@<< create class_vnode >>
		#@+node:2::<< create class_vnode  >>
		#@+body
		# Create the section name using the old value of self.methodName.
		if  self.treeType == "@file":
			prefix = ""
		else:
			prefix = angleBrackets(" " + self.methodName + " methods ") + "=\n\n"
		
		# i points just after the class line.
		body = s[start:i]
		body = self.undentBody(body)
		class_vnode = self.createHeadline(parent,prefix + body,headline)
		
		#@-body
		#@-node:2::<< create class_vnode  >>

		savedMethodName = self.methodName
		self.methodName = headline
		# Create a node for leading declarations of the class.
		i = self.scanPythonDecls(s,i,class_vnode,indent_refs)
		
		#@<< create nodes for all defs of the class >>
		#@+node:3::<< create nodes for all defs of the class >>
		#@+body
		indent =  self.getLeadingIndent(s,i)
		start = i = skip_blank_lines(s,i)
		parent_vnode = None # 7/6/02
		while i < len(s) and indent > classIndent:
			progress = i
			if is_nl(s,i):
				j = skip_nl(s,i)
				indent = self.getLeadingIndent(s,j)
				if indent > classIndent: i = j
				else: break
			elif match_c_word(s,i,"def"):
				if not parent_vnode:
					
					#@<< create parent_vnode >>
					#@+node:1::<< create parent_vnode >>
					#@+body
					# This must be done after the declaration reference is generated.
					if self.treeType == "@file":
						class_vnode.appendStringToBody("\t@others\n")
					else:
						ref = angleBrackets(" class " + classname + " methods ")
						class_vnode.appendStringToBody("\t" + ref + "\n\n")
					parent_vnode = class_vnode
					#@-body
					#@-node:1::<< create parent_vnode >>

				i = start = self.scanPythonDef(s,i,start,parent_vnode)
				indent = self.getLeadingIndent(s,i)
			elif match_c_word(s,i,"class"):
				if not parent_vnode:
					
					#@<< create parent_vnode >>
					#@+node:1::<< create parent_vnode >>
					#@+body
					# This must be done after the declaration reference is generated.
					if self.treeType == "@file":
						class_vnode.appendStringToBody("\t@others\n")
					else:
						ref = angleBrackets(" class " + classname + " methods ")
						class_vnode.appendStringToBody("\t" + ref + "\n\n")
					parent_vnode = class_vnode
					#@-body
					#@-node:1::<< create parent_vnode >>

				i = start = self.scanPythonClass(s,i,start,parent_vnode)
				indent = self.getLeadingIndent(s,i)
			elif s[i] == '#': i = skip_to_end_of_line(s,i)
			elif s[i] == '"' or s[i] == '\'': i = skip_python_string(s,i)
			else: i += 1
			assert(progress < i)
		#@-body
		#@-node:3::<< create nodes for all defs of the class >>

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

	def scanPythonDef (self,s,i,start,parent):
	
		# line = get_line(s,i) ; trace(`line`)
		
		#@<< set headline or return i >>
		#@+node:1::<< set headline or return i >>
		#@+body
		i = skip_ws(s,i)
		i = skip_c_id(s,i) # Skip the "def"
		i = skip_ws_and_nl(s,i)
		if i < len(s) and is_c_id(s[i]):
			j = i ; i = skip_c_id(s,i)
			headline = s[j:i]
			# trace("headline:" + `headline`)
		else: return i
		#@-body
		#@-node:1::<< set headline or return i >>

		
		#@<< skip the Python def >>
		#@+node:2::<< skip the Python def >>
		#@+body
		# Set defIndent to the indentation of the def line.
		defIndent = self.getLeadingIndent(s,start)
		i = skip_line(s,i) # Skip the def line.
		indent = self.getLeadingIndent(s,i)
		while i < len(s) and indent > defIndent:
			progress = i
			ch = s[i]
			if is_nl(s,i):
				i = skip_nl(s,i)
				indent = self.getLeadingIndent(s,i)
				if indent <= defIndent:
					break
			elif ch == '#':
				i = skip_to_end_of_line(s,i) # 7/29/02
			elif ch == '"' or ch == '\'':
				i = skip_python_string(s,i)
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
		# Create the prefix line for @root trees.
		if self.treeType == "@file":
			prefix = ""
		else:
			prefix = angleBrackets(" " + savedMethodName + " methods ") + "=\n\n"
		
		# Create body.
		start = skip_blank_lines(s,start)
		body = s[start:i]
		body = self.undentBody(body)
		
		# Create the node.
		self.createHeadline(parent,prefix + body,headline)
		#@-body
		#@-node:3::<< Create def node >>

		self.methodName = savedMethodName
		return i
	#@-body
	#@-node:2::scanPythonDef
	#@+node:3::scanPythonDecls
	#@+body
	def scanPythonDecls (self,s,i,parent,indent_parent_ref_flag):
		
		done = false ; start = i
		while not done and i < len(s):
			progress = i
			# line = get_line(s,i) ; trace(`line`)
			ch = s[i]
			if ch == '\n': i = skip_nl(s,i)
			elif ch == '#': i = skip_to_end_of_line(s,i)
			elif ch == '"' or ch == '\'':
				i = skip_python_string(s,i)
			elif is_c_id(ch):
				
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
		j = skip_blank_lines(s,start)
		if is_nl(s,j): j = skip_nl(s,j)
		if j < i:
			
			#@<< Create a child node for declarations >>
			#@+node:2::<< Create a child node for declarations >>
			#@+body
			headline = ref = angleBrackets(" " + self.methodName + " declarations ")
			leading_tab = choose(indent_parent_ref_flag,"\t","")
			
			# Append the reference to the parent's body.
			parent.appendStringToBody(leading_tab + ref + "\n") # 7/6/02
			
			# Create the node for the decls.
			body = self.undentBody(s[j:i])
			if self.treeType == "@root":
				body = "@code\n\n" + body
			self.createHeadline(parent,body,headline)
			#@-body
			#@-node:2::<< Create a child node for declarations >>

		return i
	#@-body
	#@-node:3::scanPythonDecls
	#@+node:4::scanPythonText
	#@+body
	#@+at
	#  This code creates a child of parent for each Python function definition 
	# seen.  See the comments for scanCText for what the text looks like.

	#@-at
	#@@c

	def scanPythonText (self,s,parent):
	
		decls_seen = false ; start = i = 0
		while i < len(s):
			progress = i
			# line = get_line(s,i) ; trace(`line`)
			ch = s[i]
			if ch == '\n' or ch == '\r': i = skip_nl(s,i)
			elif ch == '#': i = skip_to_end_of_line(s,i)
			elif ch == '"' or ch == '\'': i = skip_python_string(s,i)
			elif is_c_id(ch):
				
				#@<< handle possible Python function or class >>
				#@+node:1::<< handle possible Python function or class >>
				#@+body
				if match_c_word(s,i,"def") or match(s,i,"class"):
					isDef = match_c_word(s,i,"def")
					if not decls_seen:
						parent.appendStringToBody("@ignore\n" + self.rootLine + "@language python\n")
						i = start = self.scanPythonDecls(s,start,parent,dont_indent_refs)
						decls_seen = true
						if self.treeType == "@file": # 7/29/02
							parent.appendStringToBody("@others\n") # 7/29/02
					if isDef:
						i = start = self.scanPythonDef(s,i,start,parent)
					else:
						i = start = self.scanPythonClass(s,i,start,parent)
				else:
					i = skip_c_id(s,i)
				#@-body
				#@-node:1::<< handle possible Python function or class >>

			else: i += 1
			assert(progress < i)
		
		#@<< Append a reference to the methods of this file >>
		#@+node:2::<< Append a reference to the methods of this file >>
		#@+body
		if self.treeType == "@file":
			pass
		else:
			parent.appendStringToBody(
				angleBrackets(" " + self.methodName + " methods ") + "\n\n")
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
	#@-node:1::Python scanners
	#@+node:2::scanPHPText (Dave Hein)
	#@+body
	#@+at
	#   08-SEP-2002 DTHEIN: Added for PHP import support
	# Creates a child of parent for each class and function definition seen.
	# 
	# PHP uses both # and // as line comments, and /* */ as block comments

	#@-at
	#@@c
	def scanPHPText (self,s,parent):
		import re
		
		#@<< Append file if not pure PHP >>
		#@+node:1::<< Append file if not pure PHP >>
		#@+body
		# If the file does not begin with <?php or end with ?> then
		# it is simply appended like a generic import would do.
		s.strip() #remove inadvertent whitespace
		if not s.startswith("<?php") \
		or not (s.endswith("?>") or s.endswith("?>\n") or s.endswith("?>\r\n")):
			es("File seems to be mixed HTML and PHP; importing as plain text file.")
			parent.setBodyStringOrPane("@ignore\n" + self.rootLine + s)
			return
		#@-body
		#@-node:1::<< Append file if not pure PHP >>

	
		
		#@<< define scanPHPText vars >>
		#@+node:2::<< define scanPHPText vars >>
		#@+body
		scan_start = 0
		class_start = 0
		function_start = 0
		c = self.commands
		i = 0
		class_body = ""
		class_node = ""
		phpClassName = re.compile("class\s+([a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*)")
		phpFunctionName = re.compile("function\s+([a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*)")
		
		# 14-SEP-2002 DTHEIN: added these 2 variables to allow use of @first/last
		startOfCode = s.find("\n") + 1 # this should be the line containing the initial <?php
		endOfCode = s.rfind("?>") # this should be the line containing the last ?>
		
		#@-body
		#@-node:2::<< define scanPHPText vars >>

		# 14-SEP-2002 DTHEIN: Make leading <?php use the @first directive
		parent.appendStringToBody("@first ")	
		parent.appendStringToBody(s[:startOfCode])
		scan_start = i = startOfCode
		while i < endOfCode:
			# line = get_line(s,i) ; trace(`line`)
			ch = s[i]
			# These cases skip tokens.
			if ch == '/' or ch == '#':
				
				#@<< handle possible PHP comments >>
				#@+node:4::<< handle possible PHP comments >>
				#@+body
				if match(s,i,"//"):
					i = skip_line(s,i)
				elif match(s,i,"#"):
					i = skip_line(s,i)
				elif match(s,i,"/*"):
					i = skip_block_comment(s,i)
				else:
					i += 1
				#@-body
				#@-node:4::<< handle possible PHP comments >>

			elif ch == '<':
				
				#@<< handle possible heredoc string >>
				#@+node:3::<< handle possible heredoc string >>
				#@+body
				if match(s,i,"<<<"):
					i = skip_heredoc_string(s,i)
				else:
					i += 1
				
				#@-body
				#@-node:3::<< handle possible heredoc string >>

			elif ch == '"' or ch == '\'':
				i = skip_string(s,i)
			# These cases help determine where functions start.
			# FIXME: probably want to capture 'var's as class member data
			elif ch == 'f' or ch =='c':
				
				#@<< handle possible class or function >>
				#@+node:5::<< handle possible class or function >>
				#@+body
				#@+at
				#  In PHP, all functions are typeless and start with the 
				# keyword "function;  all classes start with the keyword class.
				# 
				# Functions can be nested, but we don't handle that right now 
				# (I don't think it is a common practice anyway).

				#@-at
				#@@c
				if match(s,i,"function "):
					#we want to make the function a subnode of either the @file node or a class node
					# 1. get the function name
					# 2. make a reference in the parent
					# 3. create the child node, and dump the function in it.
					function_start = i
					m = phpFunctionName.match(s[i:])
					if (None == m): # function keyword without function name
						i += len("function ")
					else:
						headline = angleBrackets(" function " + m.group(1) + " ")
						# find the end of the function
						openingBrace = s.find('{',i)
						function_end = skip_php_braces(s,openingBrace)
						function_end = skip_to_end_of_line(s,function_end - 1) + 1 # include the line end
						# Insert skipped text into parent's body.
						if class_start:
							class_body += s[scan_start:function_start]
						else:
							parent.appendStringToBody(s[scan_start:function_start])
						# Append the headline to the parent's body.
						if class_start:
							class_body += (headline + "\n")
						else:
							parent.appendStringToBody(headline + "\n")
						# Backup to capture leading whitespace (for undent purposes)
						while (function_start > 0) and (s[function_start - 1] in [" ", "\t"]):
							function_start -= 1
						# Get the body and undent it
						function_body = s[function_start:function_end]
						function_body = self.undentBody(function_body)
						if self.treeType != "@file":
							function_body = "@code\n\n" + function_body
						# Create the new node
						if class_start:
							self.createHeadline(class_node,function_body,headline)
						else:
							self.createHeadline(parent,function_body,headline)
						i = function_end
						scan_start = i
						function_end = 0
						function_start = 0 #done with this function
						function_body = ""
						
				elif match(s,i,"class "):
					# we want to make the class a subnode of the @file node
					# 1. get the class name
					# 2. make a reference in the parent
					# 3. create the child node and dump the function in it
					class_start = i
					class_body = ""
					m = phpClassName.match(s[i:])
					if (None == m): # class keyword without class name
						i += len("class ")
					else:
						# Insert skipped text into parent's body.
						parent.appendStringToBody(s[scan_start:class_start])
						# create the headline name
						headline = angleBrackets(" class " + m.group(1) + " ")
						# find the place to start looking for methods (functions)
						openingBrace = s.find('{',i)
						# find the end of the class
						class_end = skip_php_braces(s,openingBrace)
						class_end = skip_to_end_of_line(s,class_end - 1) + 1 # include the line end
						# Append the headline to the parent's body.
						parent.appendStringToBody(headline + "\n")
						# Backup to capture leading whitespace (for undent purposes)
						while (class_start > 0) and (s[class_start - 1] in [" ", "\t"]):
							class_start -= 1
						scan_start = class_start
						# Create the new node
						class_node = self.createHeadline(parent,"",headline)
						i = openingBrace
					
				else:
					i += 1
				#@-body
				#@-node:5::<< handle possible class or function >>

			elif class_start and (ch == '}'):
				
				#@<< handle end of class >>
				#@+node:6::<< handle end of class >>
				#@+body
				# Capture the rest of the body
				class_body += s[scan_start:class_end]
				# insert the class node's body
				if self.treeType != "@file":
					class_body = "@code\n\n" + class_body
				class_body = self.undentBody(class_body)
				class_node.appendStringToBody(class_body)
				# reset the indices
				i = class_end
				scan_start = i
				class_end = 0
				class_start = 0 #done with this class
				class_body=""
				
				#@-body
				#@-node:6::<< handle end of class >>

			else: i += 1
		
		#@<< Append any unused text to the parent's body text >>
		#@+node:7::<< Append any unused text to the parent's body text >>
		#@+body
		parent.appendStringToBody(s[scan_start:endOfCode])
		
		#@-body
		#@-node:7::<< Append any unused text to the parent's body text >>

		# 14-SEP-2002 DTHEIN: Make leading <?php use the @first directive
		parent.appendStringToBody("@last ")	
		parent.appendStringToBody(s[endOfCode:])
	#@-body
	#@-node:2::scanPHPText (Dave Hein)
	#@+node:3::scanCText
	#@+body
	# Creates a child of parent for each C function definition seen.
	
	def scanCText (self,s,parent):
	
		
		#@<< define scanCText vars >>
		#@+node:1::<< define scanCText vars >>
		#@+body
		c = self.commands
		include_seen = method_seen = false
		methodKind = choose(self.fileType==".c","functions","methods")
		lparen = None   # Non-null if '(' seen at outer level.
		scan_start = function_start = 0
		name = None
		i = 0
		#@-body
		#@-node:1::<< define scanCText vars >>

		while i < len(s):
			# line = get_line(s,i) ; trace(`line`)
			ch = s[i]
			# These cases skip tokens.
			if ch == '/':
				
				#@<< handle possible C comments >>
				#@+node:5::<< handle possible C comments >>
				#@+body
				if match(s,i,"//"):
					i = skip_line(s,i)
				elif match(s,i,"/*"):
					i = skip_block_comment(s,i)
				else:
					i += 1
				#@-body
				#@-node:5::<< handle possible C comments >>

			elif ch == '"' or ch == '\'':
				i = skip_string(s,i)
			# These cases help determine where functions start.
			elif ch == '=':
				
				#@<< handle equal sign in C >>
				#@+node:6::<< handle equal sign in C>>
				#@+body
				#@+at
				#  We can not be seeing a function definition when we find an 
				# equal sign at the top level. Equal signs inside parentheses 
				# are handled by the open paren logic.

				#@-at
				#@@c

				i += 1 # skip the '='
				function_start = None # We can't be in a function.
				lparen = None   # We have not seen an argument list yet.
				if match(s,i,'='):
					i = skip_braces(s,i)
				#@-body
				#@-node:6::<< handle equal sign in C>>

			elif ch == '(':
				
				#@<< handle open paren in C >>
				#@+node:7::<< handle open paren in C >>
				#@+body
				lparen = i
				# This will skip any equal signs inside the paren.
				i = skip_parens(s,i)
				if match(s,i,')'):
					i += 1
					i = skip_ws_and_nl(s,i)
					if match(s,i,';'):
						lparen = None # not a function definition.
				else: lparen = None
				#@-body
				#@-node:7::<< handle open paren in C >>

			elif ch == ';':
				
				#@<< handle semicolon in C >>
				#@+node:8::<< handle semicolon in C >>
				#@+body
				#@+at
				#  A semicolon signals the end of a declaration, thereby 
				# potentially starting the _next_ function defintion.   
				# Declarations end a function definition unless we have 
				# already seen a parenthesis, in which case we are seeing an 
				# old-style function definition.

				#@-at
				#@@c

				i += 1 # skip the semicolon.
				if lparen == None:
					function_start = i + 1 # The semicolon ends the declaration.
				#@-body
				#@-node:8::<< handle semicolon in C >>

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
					include_start = i = find_line_start(s,i)
					
					# Scan to the next line that is neither blank nor and #include.
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
					body = s[include_start:include_end]
					body = self.undentBody(body)
					prefix = choose(self.treeType == "@file","","@code\n\n")
					self.createHeadline(parent,prefix + body,headline)
					parent.appendStringToBody("@ignore\n" + self.rootLine + "@language c\n")
					
					# Append any previous text to the parent's body.
					save_ip = i ; i = scan_start
					while i < include_start and is_ws_or_nl(s,i):
						i += 1
					if i < include_start:
						parent.appendStringToBody(s[i:include_start])
					scan_start = function_start = i = save_ip
					# Append the headline to the parent's body.
					parent.appendStringToBody(headline + "\n")
					#@-body
					#@-node:1::<< create a child node for all #include statements >>

				else:
					j = i
					i = skip_pp_directive(s,i)
				#@-body
				#@-node:2::<< handle # sign >>

			elif ch == '{':
				
				#@<< handle open curly bracket in C >>
				#@+node:3::<< handle open curly bracket in C >> (scans function)
				#@+body
				j = i = skip_braces(s,i) # Skip all inner blocks.
				
				# This may fail if #if's contain unmatched curly braces.
				if (match(s,i,'}') and lparen and name and function_start):
					# Point i _after_ the last character of the function.
					i += 1
					if is_nl(s,i):
						i = skip_nl(s,i)
					function_end = i
					if method_seen:
						# Include everything after the last function.
						function_start = scan_start 
					else:
						
						#@<< create a declaration node >>
						#@+node:1::<< create a declaration node >>
						#@+body
						save_ip = i
						i = scan_start
						while i < function_start and is_ws_or_nl(s,i):
							i += 1
						if i < function_start:
							headline = angleBrackets(" " + self.methodName + " declarations ")
							# Append the headline to the parent's body.
							parent.appendStringToBody(headline + "\n")
							decls = s[scan_start:function_start]
							decls = self.undentBody(decls)
							if self.treeType == "@file":
								body = decls
							else:
								body = "@code\n\n" + decls
							self.createHeadline(parent,body,headline)
						i = save_ip
						scan_start = i
						#@-body
						#@-node:1::<< create a declaration node >>

						
						#@<< append C function/method reference to parent node >>
						#@+node:2::<< append C function/method reference to parent node >>
						#@+body
						if self.treeType == "@file":
							parent.appendStringToBody("@others\n")
						else:
							cweb = c.target_language == "cweb"
							lb = choose(cweb,"@<","<<")
							rb = choose(cweb,"@>",">>")
							parent.appendStringToBody(
								lb + " " + self.methodName + " " + methodKind + " " + rb + "\n")
						#@-body
						#@-node:2::<< append C function/method reference to parent node >>

					headline = name
					body = s[function_start:function_end]
					body = self.massageBody(body,"functions")
					self.createHeadline(parent,body,headline)
					
					method_seen = true
					scan_start = function_start = i # Set the start of the _next_ function.
					lparen = None
				else:
					i += 1
				#@-body
				#@-node:3::<< handle open curly bracket in C >> (scans function)

			elif is_c_id(ch):
				
				#@<< handle id, class, typedef, struct, union, namespace >>
				#@+node:4::<< handle id, class, typedef, struct, union, namespace >>
				#@+body
				if match_c_word(s,i,"typedef"):
					i = skip_typedef(s,i)
					lparen = None
				elif match_c_word(s,i,"struct"):
					i = skip_typedef(s,i)
					# lparen = None ;  # This can appear in an argument list.
				elif match_c_word(s,i,"union"):
					i = skip_typedef(s,i)
					# lparen = None ;  # This can appear in an argument list.
				elif match_c_word(s,i,"namespace"):
					
					#@<< create children for the namespace >>
					#@+node:1::<< create children for the namespace >>
					#@+body
					#@+at
					#  Namesspaces change the self.moduleName and recursively 
					# call self function with a text covering only the range 
					# of the namespace. This effectively changes the 
					# definition line of any created child nodes. The 
					# namespace is written to the top level.

					#@-at
					#@@c

					# skip the "namespace" keyword.
					i += len("namespace")
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
					if match(s,i,'{') and namespace_name_start:
						inner_ip = i + 1
						i = skip_braces(s,i)
						if match(s,i,'}'):
							# Append everything so far to the body.
							if inner_ip > scan_start:
								parent.appendStringToBody(s[scan_start:inner_ip])
							# Save and change self.moduleName to namespaceName
							savedMethodName = self.methodName
							namespaceName = s[namespace_name_start:namespace_name_end]
							self.methodName = "namespace " + namespaceName
							# Recursively call this function .
							self.scanCText(s[inner_ip:],parent)
							# Restore self.moduleName and continue scanning.
							self.methodName = savedMethodName
							scan_start = function_start = i
					#@-body
					#@-node:1::<< create children for the namespace >>

				# elif match_c_word(s,i,"class"):
					# < < create children for the class > >
				else:
					# Remember the last name before an open parenthesis.
					if lparen == None:
						j = i ; i = skip_c_id(s,i) ; name = s[j:i]
					else:
						i = skip_c_id(s,i)
					
					#@<< test for operator keyword >>
					#@+node:2::<< test for operator keyword >>
					#@+body
					# We treat a C++ a construct such as operator + as a function name.
					if match(name,0,"operator"):
						j = i
						i = skip_ws(s,i) # Don't allow newline in headline.
						if (i < len(s) and not is_c_id(s[i]) and
							s[i]!=' ' and s[i]!='\n' and s[i]!='\r'):
							while (i < len(s) and not is_c_id(s[i]) and
								s[i]!=' ' and s[i]!='\n' and s[i] != '\r'):
								i += 1
							name = s[j:i] # extend the name.
					#@-body
					#@-node:2::<< test for operator keyword >>
				#@-body
				#@-node:4::<< handle id, class, typedef, struct, union, namespace >>

			else: i += 1
		
		#@<< Append any unused text to the parent's body text >>
		#@+node:9::<< Append any unused text to the parent's body text >>
		#@+body
		# Used by C, Java and Pascal parsers.
		# Do nothing if only whitespace is left.
		
		i = skip_ws_and_nl(s,scan_start)
		if i < len(s):
			parent.appendStringToBody(s[scan_start:])
		#@-body
		#@-node:9::<< Append any unused text to the parent's body text >>
	#@-body
	#@-node:3::scanCText
	#@+node:4::scanJavaText
	#@+body
	# Creates a child of parent for each Java function definition seen.
	
	def scanJavaText (self,s,parent,outerFlag): # true if at outer level.
	
		
		#@<< define scanJavaText vars >>
		#@+node:1::<< define scanJavaText vars >>
		#@+body
		method_seen = false
		class_seen = false # true: class keyword seen at outer level.
		interface_seen = false # true: interface keyword seen at outer level.
		lparen = None  # not None if '(' seen at outer level.
		scan_start = 0
		name = None
		function_start = 0 # choose(outerFlag, None, 0)
		i = 0
		#@-body
		#@-node:1::<< define scanJavaText vars >>

		# if not outerFlag: trace("inner:" + `s`)
		while i < len(s):
			# trace(`get_line(s,i)`)
			ch = s[i]
			# These cases skip tokens.
			if ch == '/':
				
				#@<< handle possible Java comments >>
				#@+node:4::<< handle possible Java comments >>
				#@+body
				if match(s,i,"//"):
					i = skip_line(s,i)
				elif match(s,i,"/*"):
					i = skip_block_comment(s,i)
				else:
					i += 1
				#@-body
				#@-node:4::<< handle possible Java comments >>

			elif ch == '"' or ch == '\'': i = skip_string(s,i)
			# These cases help determine where functions start.
			elif ch == '=':
				
				#@<< handle equal sign in Java >>
				#@+node:5::<< handle equal sign in Java >>
				#@+body
				#@+at
				#  We can not be seeing a function definition when we find an 
				# equal sign at the top level. Equal signs inside parentheses 
				# are handled by the open paren logic.

				#@-at
				#@@c

				i += 1 # skip the '='
				function_start = None # We can't be in a function.
				lparen = None   # We have not seen an argument list yet.
				if match(s,i,'='):
					i = skip_braces(s,i)
				#@-body
				#@-node:5::<< handle equal sign in Java >>

			elif ch == '(':
				
				#@<< handle open paren in Java >>
				#@+node:6::<< handle open paren in Java >>
				#@+body
				lparen = i
				# This will skip any equal signs inside the paren.
				i = skip_parens(s,i)
				if match(s,i,')'):
					i += 1
					i = skip_ws_and_nl(s,i)
					if match(s,i,';'):
						lparen = None # not a function definition.
				else: lparen = None
				#@-body
				#@-node:6::<< handle open paren in Java >>

			elif ch == ';':
				
				#@<< handle semicolon in Java >>
				#@+node:7::<< handle semicolon in Java >>
				#@+body
				#@+at
				#  A semicolon signals the end of a declaration, thereby 
				# potentially starting the _next_ function defintion.   
				# Declarations end a function definition unless we have 
				# already seen a parenthesis, in which case we are seeing an 
				# old-style function definition.

				#@-at
				#@@c

				i += 1 # skip the semicolon.
				if lparen == None:
					function_start = i + 1 # The semicolon ends the declaration.
				#@-body
				#@-node:7::<< handle semicolon in Java >>

				class_seen = false
			# These cases can create child nodes.
			elif ch == '{':
				
				#@<< handle open curly bracket in Java >>
				#@+node:2::<< handle open curly bracket in Java >>
				#@+body
				brace_ip1 = i
				i = skip_braces(s,i) # Skip all inner blocks.
				brace_ip2 = i
				
				if not match (s,i,'}'):
					es("unmatched '{'")
				elif not name:
					i += 1
				elif (outerFlag and (class_seen or interface_seen)) or (not outerFlag and lparen):
					# trace("starting:"+name)
					# trace("outerFlag:"+`outerFlag`)
					# trace("lparen:"`lparen`)
					# trace("class_seen:"+`class_seen`)
					# trace("scan_start:"+get_line_after(s,scan_start))
					# trace("func_start:"+get_line_after(s,function_start))
					# trace("s:"+get_line(s,i))
				
					# Point i _after_ the last character of the method.
					i += 1
					if is_nl(s,i):
						i = skip_nl(s,i)
					function_end = i
					headline = name
					if outerFlag:
						leader = "" ; decl_leader = ""
						if class_seen:
							headline = "class " + headline
							methodKind = "classes"
						else:
							headline = "interface " + headline
							methodKind = "interfaces"
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
							
						if outerFlag:
							parent.appendStringToBody("@ignore\n" + self.rootLine + "@language java\n")
						
						if i < function_start:
							decl_headline = angleBrackets(" " + self.methodName + " declarations ")
						
							# Append the headline to the parent's body.
							parent.appendStringToBody(decl_leader + leader + decl_headline + "\n")
							scan_start = find_line_start(s,scan_start) # Backtrack so we remove leading whitespace.
							decls = s[scan_start:function_start]
							decls = self.undentBody(decls)
							body = choose(self.treeType == "@file",decls,"@code\n\n" + decls)
							self.createHeadline(parent,body,decl_headline)
						
						i = save_ip
						scan_start = i
						#@-body
						#@-node:1::<< create a Java declaration node >>

						
						#@<< append Java method reference to parent node >>
						#@+node:2::<< append Java method reference to parent node >>
						#@+body
						if self.treeType == "@file":
							if outerFlag:
								parent.appendStringToBody("\n@others\n")
							else:
								parent.appendStringToBody("\n\t@others\n")
						else:
							kind = choose(outerFlag,"classes","methods")
							ref_name = angleBrackets(" " + self.methodName + " " + kind + " ")
							parent.appendStringToBody(leader + ref_name + "\n")
						#@-body
						#@-node:2::<< append Java method reference to parent node >>

					if outerFlag: # Create a class.
						# Backtrack so we remove leading whitespace.
						function_start = find_line_start(s,function_start)
						body = s[function_start:brace_ip1+1]
						body = self.massageBody(body,methodKind)
						v = self.createHeadline(parent,body,headline)
						
						#@<< recursively scan the text >>
						#@+node:3::<< recursively scan the text >>
						#@+body
						# These mark the points in the present function.
						# trace("recursive scan:" + `get_line(s,brace_ip1+ 1)`)
						oldMethodName = self.methodName
						self.methodName = headline
						self.scanJavaText(s[brace_ip1+1:brace_ip2], # Don't include either brace.
							v,false) # inner level
						self.methodName = oldMethodName
						
						#@-body
						#@-node:3::<< recursively scan the text >>

						# Append the brace to the parent.
						v.appendStringToBody("}")
						i = brace_ip2 + 1 # Start after the closing brace.
					else: # Create a method.
						# Backtrack so we remove leading whitespace.
						function_start = find_line_start(s,function_start)
						body = s[function_start:function_end]
						body = self.massageBody(body,methodKind)
						self.createHeadline(parent,body,headline)
						i = function_end
					method_seen = true
					scan_start = function_start = i # Set the start of the _next_ function.
					lparen = None ; class_seen = false
				else: i += 1
				#@-body
				#@-node:2::<< handle open curly bracket in Java >>

			elif is_c_id(s[i]):
				
				#@<< skip and remember the Java id >>
				#@+node:3::<< skip and remember the Java id >>
				#@+body
				if match_c_word(s,i,"class") or match_c_word(s,i,"interface"):
					if match_c_word(s,i,"class"):
						class_seen = true
					else:
						interface_seen = true
					i = skip_c_id(s,i) # Skip the class or interface keyword.
					i = skip_ws_and_nl(s,i)
					if i < len(s) and is_c_id(s[i]):
						# Remember the class or interface name.
						j = i ; i = skip_c_id(s,i) ; name = s[j:i]
				else:
					j = i ; i = skip_c_id(s,i)
					if not lparen and not class_seen:
						name = s[j:i] # Remember the name.
				#@-body
				#@-node:3::<< skip and remember the Java id >>

			else: i += 1
		
		#@<< Append any unused text to the parent's body text >>
		#@+node:8::<< Append any unused text to the parent's body text >>
		#@+body
		# Used by C, Java and Pascal parsers.
		# Do nothing if only whitespace is left.
		
		i = skip_ws_and_nl(s,scan_start)
		if i < len(s):
			parent.appendStringToBody(s[scan_start:])
		#@-body
		#@-node:8::<< Append any unused text to the parent's body text >>
	#@-body
	#@-node:4::scanJavaText
	#@+node:5::scanPascalText
	#@+body
	# Creates a child of parent for each Pascal function definition seen.
	
	def scanPascalText (self,s,parent):
	
		method_seen = false ; methodKind = "methods"
		scan_start = function_start = i = 0
		name = None
		while i < len(s):
			# line = get_line(s,i) ; trace(`line`)
			ch = s[i]
			if ch == '{': i = skip_pascal_braces(s,i)
			elif ch == '"' or ch == '\'': i = skip_pascal_string(s,i)
			elif match(s,i,"//"): i = skip_to_end_of_line(s,i)
			elif match(s,i,"(*"): i = skip_pascal_block_comment(s,i)
			elif is_c_id(s[i]):
				
				#@<< handle possible Pascal function >>
				#@+node:1::<< handle possible Pascal function >>
				#@+body
				if match_c_word(s,i,"begin"):
					i = skip_pascal_begin_end(s,i)
					if match_c_word(s,i,"end"):
						i = skip_c_id(s,i)
				elif (match_c_word(s,i,"function")  or match_c_word(s,i,"procedure") or
					match_c_word(s,i,"constructor") or match_c_word(s,i,"destructor")):
				
					# line = get_line(s,i) ; trace(`line`)
					
					start = i
					i = skip_c_id(s,i)
					i = skip_ws_and_nl(s,i)
					
					#@<< remember the function name, or continue >>
					#@+node:3::<< remember the function name, or continue >>
					#@+body
					if i < len(s) and is_c_id(s[i]):
						j = i ; i = skip_c_id(s,i)
						while i + 1 < len(s) and s[i] == '.' and is_c_id(s[i+1]):
							i += 1 ; j = i
							i = skip_c_id(s,i)
						name = s[j:i]
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
							if match(s,i,')'):
								i += 1
							else: break
						else: i += 1
					if match(s,i,';'):
						i += 1
					i = skip_ws_and_nl(s,i)
					
					if match_c_word(s,i,"var"):
						# Skip to the next begin.
						i = skip_c_id(s,i)
						done = false
						while i < len(s) and not done:
							ch = s[i]
							if ch == '{': i = skip_pascal_braces(s,i)
							elif match(s,i,"//"): i = skip_to_end_of_line(s,i)
							elif match(s,i,"(*"): i = skip_pascal_block_comment(s,i)
							elif is_c_id(ch):
								if match_c_word(s,i,"begin"): done = true
								else: i = skip_c_id(s,i)
							elif ch == '"' or ch == '\'': i = skip_pascal_string(s,i)
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
						if match(s,i,';'):
							i += 1
						i = skip_ws(s,i)
						if is_nl(s,i):
							i = skip_nl(s,i)
					else: continue
					#@-body
					#@-node:4::<< skip the function definition, or continue >>

					if not method_seen:
						method_seen = true
						
						#@<< create a child node for leading declarations >>
						#@+node:1::<< create a child node for leading declarations >>
						#@+body
						save_ip = i
						i = scan_start
						while i < start and is_ws_or_nl(s,i):
							i += 1
						if i < start:
							parent.appendStringToBody("@ignore\n" + self.rootLine + "@language pascal\n")
							headline = angleBrackets(self.methodName + " declarations ")
							# Append the headline to the parent's body.
							parent.appendStringToBody(headline + "\n")
							if self.treeType == "@file":
								body = s[scan_start:start]
							else:
								body = "@code\n\n" + s[scan_start:start]
							body = self.undentBody(body)
							self.createHeadline(parent,body,headline)
						i = save_ip
						scan_start = i
						#@-body
						#@-node:1::<< create a child node for leading declarations >>

						
						#@<< append noweb method reference to the parent node >>
						#@+node:5::<< append noweb method reference to the parent node >>
						#@+body
						# Append the headline to the parent's body.
						if self.treeType == "@file":
							parent.appendStringToBody("@others\n")
						else:
							parent.appendStringToBody(
								angleBrackets(" " + self.methodName + " methods ") + "\n")
						#@-body
						#@-node:5::<< append noweb method reference to the parent node >>

						function_start = start
					else: function_start = scan_start
					
					#@<< create a child node for the function >>
					#@+node:2::<< create a child node for the function >>
					#@+body
					# Point i _after_ the last character of the function.
					i = skip_ws(s,i)
					if is_nl(s,i):
						i = skip_nl(s,i)
					function_end = i
					headline = name
					body = s[function_start:function_end]
					body = self.massageBody(body,methodKind)
					self.createHeadline(parent,body,headline)
					scan_start = i
					#@-body
					#@-node:2::<< create a child node for the function >>

				else: i = skip_c_id(s,i)
				#@-body
				#@-node:1::<< handle possible Pascal function >>

			else: i += 1
		
		#@<< Append any unused text to the parent's body text >>
		#@+node:2::<< Append any unused text to the parent's body text >>
		#@+body
		# Used by C, Java and Pascal parsers.
		# Do nothing if only whitespace is left.
		
		i = skip_ws_and_nl(s,scan_start)
		if i < len(s):
			parent.appendStringToBody(s[scan_start:])
		#@-body
		#@-node:2::<< Append any unused text to the parent's body text >>
	#@-body
	#@-node:5::scanPascalText
	#@-node:5::Scanners for createOutline
	#@-node:3::Import
	#@+node:4::Export
	#@+node:1::convertCodePartToWeb
	#@+body
	#@+at
	#  Headlines not containing a section reference are ignored in noweb and 
	# generate index index in cweb.

	#@-at
	#@@c

	def convertCodePartToWeb (self,s,i,v,result):
	
		# line = get_line(s,i) ; trace(`line`)
		c = self.commands ; nl = self.output_newline
		lb = choose(self.webType=="cweb","@<","<<")
		rb = choose(self.webType=="cweb","@>",">>")
		h = string.strip(v.headString())
		
		#@<< put v's headline ref in head_ref >>
		#@+node:1::<< put v's headline ref in head_ref>>
		#@+body
		#@+at
		#  We look for either noweb or cweb brackets. head_ref does not 
		# include these brackets.

		#@-at
		#@@c

		head_ref = None
		j = 0
		if match(h,j,"<<"):
			k = string.find(h,">>",j)
		elif match(h,j,"<@"):
			k = string.find(h,"@>",j)
		else:
			k = -1
		
		if k > -1:
			head_ref = string.strip(h[j+2:k])
			if len(head_ref) == 0:
				head_ref = None
		#@-body
		#@-node:1::<< put v's headline ref in head_ref>>

		
		#@<< put name following @root or @file in file_name >>
		#@+node:2::<< put name following @root or @file in file_name >>
		#@+body
		if match(h,0,"@file") or match(h,0,"@root"):
			line = h[5:]
			line = string.strip(line)
			
			#@<< set file_name >>
			#@+node:1::<< Set file_name >>
			#@+body
			# set j & k so line[j:k] is the file name.
			# trace(`line`)
			
			if match(line,0,"<"):
				j = 1 ; k = string.find(line,">",1)
			elif match(line,0,'"'):
				j = 1 ; k = string.find(line,'"',1)
			else:
				j = 0 ; k = string.find(line," ",0)
			if k == -1:
				k = len(line)
			
			file_name = string.strip(line[j:k])
			if file_name and len(file_name) == 0:
				file_name = None
			#@-body
			#@-node:1::<< Set file_name >>

		else:
			file_name = line = None
		
		#@-body
		#@-node:2::<< put name following @root or @file in file_name >>

		if match_word(s,i,"@root"):
			i = skip_line(s,i)
			
			#@<< append ref to file_name >>
			#@+node:3::<< append ref to file_name >>
			#@+body
			if self.webType == "cweb":
				if not file_name:
					result += "@<root@>=" + nl
				else:
					result += "@(" + file_name + "@>" + nl # @(...@> denotes a file.
			else:
				if not file_name:
					file_name = "*"
				result += lb + file_name + rb + "=" + nl
			
			#@-body
			#@-node:3::<< append ref to file_name >>

		elif match_word(s,i,"@c") or match_word(s,i,"@code"):
			i = skip_line(s,i)
			
			#@<< append head_ref >>
			#@+node:4::<< append head_ref >>
			#@+body
			if self.webType == "cweb":
				if not head_ref:
					result += "@^" + h + "@>" + nl # Convert the headline to an index entry.
					result += "@c" + nl # @c denotes a new section.
				else: 
					escaped_head_ref = string.replace(head_ref,"@","@@")
					result += "@<" + escaped_head_ref + "@>=" + nl
			else:
				if not head_ref:
					if v == c.currentVnode():
						head_ref = choose(file_name,file_name,"*")
					else:
						head_ref = "@others"
			
				result += lb + head_ref + rb + "=" + nl
			#@-body
			#@-node:4::<< append head_ref >>

		elif match_word(h,0,"@file"):
			# Only do this if nothing else matches.
			
			#@<< append ref to file_name >>
			#@+node:3::<< append ref to file_name >>
			#@+body
			if self.webType == "cweb":
				if not file_name:
					result += "@<root@>=" + nl
				else:
					result += "@(" + file_name + "@>" + nl # @(...@> denotes a file.
			else:
				if not file_name:
					file_name = "*"
				result += lb + file_name + rb + "=" + nl
			
			#@-body
			#@-node:3::<< append ref to file_name >>

			i = skip_line(s,i) # 4/28/02
		else:
			
			#@<< append head_ref >>
			#@+node:4::<< append head_ref >>
			#@+body
			if self.webType == "cweb":
				if not head_ref:
					result += "@^" + h + "@>" + nl # Convert the headline to an index entry.
					result += "@c" + nl # @c denotes a new section.
				else: 
					escaped_head_ref = string.replace(head_ref,"@","@@")
					result += "@<" + escaped_head_ref + "@>=" + nl
			else:
				if not head_ref:
					if v == c.currentVnode():
						head_ref = choose(file_name,file_name,"*")
					else:
						head_ref = "@others"
			
				result += lb + head_ref + rb + "=" + nl
			#@-body
			#@-node:4::<< append head_ref >>

		i,result = self.copyPart(s,i,result)
		return i, string.strip(result) + nl
		

	#@+at
	#  %defs a b c

	#@-at
	#@-body
	#@-node:1::convertCodePartToWeb
	#@+node:2::convertDocPartToWeb (handle @ %def)
	#@+body
	def convertDocPartToWeb (self,s,i,result):
		
		nl = self.output_newline
	
		# line = get_line(s,i) ; trace(`line`)
		if match_word(s,i,"@doc"):
			i = skip_line(s,i)
		elif match(s,i,"@ ") or match(s,i,"@\t") or match(s,i,"@*"):
			i += 2
		elif match(s,i,"@\n"):
			i += 1
		i = skip_ws_and_nl(s,i)
		i, result2 = self.copyPart(s,i,"")
		if len(result2) > 0:
			# Break lines after periods.
			result2 = string.replace(result2,".  ","." + nl)
			result2 = string.replace(result2,". ","." + nl)
			result += nl+"@"+nl+string.strip(result2)+nl+nl
		else:
			# All nodes should start with '@', even if the doc part is empty.
			result += choose(self.webType=="cweb",nl+"@ ",nl+"@"+nl)
		return i, result
	#@-body
	#@-node:2::convertDocPartToWeb (handle @ %def)
	#@+node:3::convertVnodeToWeb
	#@+body
	#@+at
	#  This code converts a vnode to noweb text as follows:
	# 
	# Convert @doc to @
	# Convert @root or @code to << name >>=, assuming the headline contains << 
	# name >>
	# Ignore other directives
	# Format doc parts so they fit in pagewidth columns.
	# Output code parts as is.

	#@-at
	#@@c

	def convertVnodeToWeb (self,v):
	
		if not v: return ""
		nl = self.output_newline
		s = v.bodyString()
		lb = choose(self.webType=="cweb","@<","<<")
		i = 0 ; result = "" ; docSeen = false
		while i < len(s):
			progress = i
			# line = get_line(s,i) ; trace(`line`)
			i = skip_ws_and_nl(s,i)
			if self.isDocStart(s,i) or match_word(s,i,"@doc"):
				i,result = self.convertDocPartToWeb(s,i,result)
				docSeen = true
			elif (match_word(s,i,"@code") or match_word(s,i,"@root") or
				match_word(s,i,"@c") or match(s,i,lb)):
				
				#@<< Supply a missing doc part >>
				#@+node:1::<< Supply a missing doc part >>
				#@+body
				if not docSeen:
					docSeen = true
					result += choose(self.webType=="cweb",nl+"@ ",nl+"@"+nl)
				#@-body
				#@-node:1::<< Supply a missing doc part >>

				i,result = self.convertCodePartToWeb(s,i,v,result)
			elif self.treeType == "@file":
				
				#@<< Supply a missing doc part >>
				#@+node:1::<< Supply a missing doc part >>
				#@+body
				if not docSeen:
					docSeen = true
					result += choose(self.webType=="cweb",nl+"@ ",nl+"@"+nl)
				#@-body
				#@-node:1::<< Supply a missing doc part >>

				i,result = self.convertCodePartToWeb(s,i,v,result)
			else:
				i,result = self.convertDocPartToWeb(s,i,result)
				docSeen = true
			assert(progress < i)
		result = string.strip(result)
		if len(result) > 0:
			result += nl
		return result
	#@-body
	#@-node:3::convertVnodeToWeb
	#@+node:4::copyPart
	#@+body
	# Copies characters to result until the end of the present section is seen.
	
	def copyPart (self,s,i,result):
	
		# line = get_line(s,i) ; trace(`line`)
		lb = choose(self.webType=="cweb","@<","<<")
		rb = choose(self.webType=="cweb","@>",">>")
		type = self.webType
		while i < len(s):
			progress = j = i # We should be at the start of a line here.
			# line = get_line(s,i) ; trace(`line`)
			i = skip_nl(s,i) ; i = skip_ws(s,i)
			if self.isDocStart(s,i):
				return i, result
			if match_word(s,i,"@doc") or match_word(s,i,"@c") or match_word(s,i,"@root"):
				return i, result
			elif (match(s,i,"<<") and # must be on separate lines.
				find_on_line(s,i,">>=") > -1):
				return i, result
			else:
				# Copy the entire line, escaping '@' and
				# Converting @others to < < @ others > >
				i = skip_line(s,j) ; line = s[j:i]
				if type == "cweb":
					line = string.replace(line,"@","@@")
				else:
					j = skip_ws(line,0)
					if match(line,j,"@others"):
						line = string.replace(line,"@others",lb + "@others" + rb)
					elif match(line,0,"@"):
						# Special case: do not escape @ %defs.
						k = skip_ws(line,1)
						if not match(line,k,"%defs"):
							line = "@" + line
				result += line
			assert(progress < i)
		return i, string.rstrip(result)
	#@-body
	#@-node:4::copyPart
	#@+node:5::flattenOutline
	#@+body
	def flattenOutline (self,fileName):
	
		c = self.commands ; v = c.currentVnode()
		nl = self.output_newline
		if not v: return
		after = v.nodeAfterTree()
		firstLevel = v.level()
		try:
			# 10/14/02: support for output_newline setting.
			mode = app().config.output_newline
			mode = choose(mode=="platform",'w','wb')
			file = open(fileName,mode)
			while v and v != after:
				head = v.moreHead(firstLevel)
				file.write(head + nl)
				body = v.moreBody() # Inserts escapes.
				if len(body) > 0:
					file.write(body + nl)
				v = v.threadNext()
			file.close()
		except:
			es("exception while flattening outline")
			es_exception()
	#@-body
	#@-node:5::flattenOutline
	#@+node:6::outlineToWeb
	#@+body
	def outlineToWeb (self,fileName,webType):
	
		c = self.commands ; v = c.currentVnode()
		nl = self.output_newline
		if v == None: return
		self.webType = webType
		after = v.nodeAfterTree()
		try: # This can fail if the file is open by another app.
			# 10/14/02: support for output_newline setting.
			mode = app().config.output_newline
			mode = choose(mode=="platform",'w','wb')
			file = open(fileName,mode)
			self.treeType = "@file"
			# Set self.treeType to @root if v or an ancestor is an @root node.
			while v:
				flag, junk = is_special(v.bodyString(),0,"@root")
				if flag:
					self.treeType = "@root" ; break
				else: v = v.parent()
			v = c.currentVnode()
			while v and v != after:
				s = self.convertVnodeToWeb(v)
				if len(s) > 0:
					file.write(s)
					if s[-1] != '\n':
						file.write(nl)
				v = v.threadNext()
			file.close()
		except:
			es("exception in Outline To noweb command")
			es_exception()
	#@-body
	#@-node:6::outlineToWeb
	#@+node:7::removeSentinelsCommand
	#@+body
	def removeSentinelsCommand (self,fileName):
	
		path, self.fileName = os.path.split(fileName) # path/fileName
		# trace(`self.fileName`)
		
		#@<< Read file into s >>
		#@+node:1::<< Read file into s >>
		#@+body
		try:
			file = open(fileName)
			s = file.read()
			file.close()
		except:
			es("exception while reading " + fileName)
			es_exception()
			return
		#@-body
		#@-node:1::<< Read file into s >>

		valid = true
		line_delim = start_delim = end_delim = None
		
		#@<< set delims from the header line >>
		#@+node:2::<< set delims from the header line >>
		#@+body
		#@+at
		#  This code is similar to atFile::scanHeader.

		#@-at
		#@@c

		tag = "@+leo"
		# Skip any non @+leo lines.
		i = 0
		while i < len(s) and not find_on_line(s,i,tag):
			i = skip_line(s,i)
		# We should be at the @+leo line.
		i = j = skip_ws(s,i)
		# The opening comment delim is the initial non-whitespace.
		while i < len(s) and not match(s,i,tag) and not is_ws(s[i]) and not is_nl(s,i):
			i += 1
		if j < i: line_delim = s[j:i]
		else: valid = false
		# Make sure we have @+leo
		i = skip_ws(s,i)
		if match(s,i,tag): i += len(tag)
		else: valid = false
		# The closing comment delim is the trailing non-whitespace.
		i = j = skip_ws(s,i)
		while i < len(s) and not is_ws(s[i]) and not is_nl(s,i):
			i += 1
		if j < i:
			start_delim = line_delim
			end_delim = s[j:i]
			line_delim = None
		#@-body
		#@-node:2::<< set delims from the header line >>

		if valid == false:
			es("invalid @+leo sentinel in " + fileName)
		else:
			if 0:
				trace("line:"+`line_delim`+","+
					"start:"+`start_delim`+","+
					"end:"+`end_delim`)
			s = self.removeSentinelLines(s,line_delim,start_delim,end_delim)
			ext = app().config.remove_sentinels_extension
			if ext == None or len(ext) == 0:
				ext = ".txt"
			if ext[0] == '.':
				newFileName = os.path.join(path,fileName+ext)
			else:
				head,ext2 = os.path.splitext(fileName) 
				newFileName = os.path.join(path,head+ext+ext2)
			# newFileName = os.path.join(path,fileName+".txt") # 8/4/02: use txt, not tmp.
			
			#@<< Write s into newFileName >>
			#@+node:3::<< Write s into newFileName >>
			#@+body
			try:
				# 10/14/02: support for output_newline setting.
				mode = app().config.output_newline
				mode = choose(mode=="platform",'w','wb')
				file = open(newFileName,mode)
				file.write(s)
				file.close()
				es("creating: " + newFileName)
			except:
				es("exception creating: " + newFileName)
				es_exception()
			#@-body
			#@-node:3::<< Write s into newFileName >>
	#@-body
	#@-node:7::removeSentinelsCommand
	#@+node:8::removeSentinelLines
	#@+body
	#@+at
	#  Properly removes all sentinel lines in s.  Only leading single-line 
	# comments may be sentinels.
	# 
	# line_delim, start_delim and end_delim are the comment delimiters.

	#@-at
	#@@c

	def removeSentinelLines(self,s,line_delim,start_delim,end_delim):
	
		i = 0 ; result = "" ; first = true
		while i < len(s):
			start = i # The start of the next syntax element.
			if first or is_nl(s,i):
				first = false
				
				#@<< handle possible sentinel >>
				#@+node:1::<< handle possible sentinel >>
				#@+body
				i = skip_nl(s,i)
				i = skip_ws(s,i)
				
				if line_delim:
					if match(s,i,line_delim):
						j = i + len(line_delim)
						i = skip_to_end_of_line(s,i)
						if match(s,j,"@"):
							continue # Remove the sentinel.
				elif start_delim:
					if match(s,i,start_delim):
						j = i + len(start_delim)
						i = skip_matching_delims(s,i,start_delim,end_delim)
						if match(s,j,"@"):
							continue # Remove the sentinel.
				#@-body
				#@-node:1::<< handle possible sentinel >>

			elif match(s,i,line_delim):
				i = skip_to_end_of_line(s,i)
			elif match(s,i,start_delim):
				i = skip_matching_delims(s,i,start_delim,end_delim)
			elif match(s,i,"'") or match(s,i,'"'):
				i = skip_string(s,i)
			else:
				i += 1
			assert(i==0 or start<i)
			result += s[start:i]
		return result
	#@-body
	#@-node:8::removeSentinelLines
	#@+node:9::weave
	#@+body
	def weave (self,filename):
		
		c = self.commands ; v = c.currentVnode()
		nl = self.output_newline
		if not v: return
		
		#@<< open filename to f, or return >>
		#@+node:1::<< open filename to f, or return >>
		#@+body
		try:
			# 10/14/02: support for output_newline setting.
			mode = app().config.output_newline
			mode = choose(mode=="platform",'w','wb')
			f = open(filename,mode)
			if not f: return
		except:
			es("exception opening:" + filename)
			es_exception()
			return
		#@-body
		#@-node:1::<< open filename to f, or return >>

		after = v.nodeAfterTree()
		while v and v != after:
			s = v.bodyString()
			s2 = string.strip(s)
			if s2 and len(s2) > 0:
				f.write("-" * 60) ; f.write(nl)
				
				#@<< write the context of v to f >>
				#@+node:2::<< write the context of v to f >>
				#@+body
				# write the headlines of v, v's parent and v's grandparent.
				context = [] ; v2 = v
				for i in xrange(3):
					if not v2: break
					context.append(v2.headString())
					v2 = v2.parent()
				
				context.reverse()
				indent = ""
				for line in context:
					f.write(indent)
					indent += '\t'
					f.write(line)
					f.write(nl)
				
				#@-body
				#@-node:2::<< write the context of v to f >>

				f.write("-" * 60) ; f.write(nl)
				f.write(string.rstrip(s) + nl)
			v = v.threadNext()
		f.flush()
		f.close()
	#@-body
	#@-node:9::weave
	#@-node:4::Export
	#@+node:5::Utilities
	#@+node:1::createHeadline
	#@+body
	def createHeadline (self,parent,body,headline):
	
		# trace("parent,headline:" + `parent` + ":" + `headline`)
		# Create the vnode.
		v = parent.insertAsLastChild()
		v.initHeadString(headline)
		# Set the body.
		if len(body) > 0:
			v.setBodyStringOrPane(body)
		return v
	#@-body
	#@-node:1::createHeadline
	#@+node:2::error
	#@+body
	def error (self,s): es(s)
	#@-body
	#@-node:2::error
	#@+node:3::getLeadingIndent
	#@+body
	#@+at
	#  This code returns the leading whitespace of a line, ignoring blank and 
	# comment lines.

	#@-at
	#@@c

	def getLeadingIndent (self,s,i):
	
		c = self.commands
		i = find_line_start(s,i)
		while i < len(s):
			# trace(`get_line(s,i)`)
			if is_nl(s,i) or match(s,i,"#"):
				i = skip_line(s,i) # ignore blank lines and comments.
			else:
				i, width = skip_leading_ws_with_indent(s,i,c.tab_width)
				# trace("returns:" + `width`)
				return width
		# trace("returns:0")
		return 0
	#@-body
	#@-node:3::getLeadingIndent
	#@+node:4::isDocStart and isModuleStart
	#@+body
	# The start of a document part or module in a noweb or cweb file.
	# Exporters may have to test for @doc as well.
	
	def isDocStart (self,s,i):
		
		if not match(s,i,"@"):
			return false
	
		j = skip_ws(s,i+1)
		if match(s,j,"%defs"):
			return false
		elif self.webType == "cweb" and match(s,i,"@*"):
			return true
		else:
			return match(s,i,"@ ") or match(s,i,"@\t") or match(s,i,"@\n")
	
	def isModuleStart (self,s,i):
	
		if self.isDocStart(s,i):
			return true
		else:
			return self.webType == "cweb" and (
				match(s,i,"@c") or match(s,i,"@p") or
				match(s,i,"@d") or match(s,i,"@f"))
	
	#@-body
	#@-node:4::isDocStart and isModuleStart
	#@+node:5::massageBody
	#@+body
	def massageBody (self,s,methodKind):
		
		# trace(`s`)
		# trace(`get_line(s,0)`)
		c = self.commands
		if self.treeType == "@file":
			if self.fileType == ".py": # 7/31/02: was "py"
				return self.undentBody(s)
			else:
				newBody, comment = self.skipLeadingComments(s)
				newBody = self.undentBody(newBody)
				newLine = choose(is_nl(newBody,0),"\n","\n\n")
				if len(comment) > 0:
					return comment + "\n@c" + newLine + newBody
				else:
					return newBody
		else:
			# Inserts < < self.methodName methodKind > > =
			cweb = self.fileType == "c" and not c.use_noweb_flag
			lb = choose(cweb,"@<","<<")
			rb = choose(cweb,"@>=",">>=")
			intro = lb + " " + self.methodName + " " + methodKind + " " + rb
			if self.fileType == ".py": # 7/31/02: was "py"
				newBody = self.undentBody(s)
				newLine = choose(is_nl(newBody,0),"\n","\n\n")
				return intro + newLine + newBody
			else:
				newBody, comment = self.skipLeadingComments(s)
				newBody = self.undentBody(newBody)
				newLine = choose(is_nl(newBody,0),"\n","\n\n")
				if len(comment) > 0:
					return comment + "\n" + intro + newLine + newBody
				else:
					return intro + newLine + newBody
	#@-body
	#@-node:5::massageBody
	#@+node:6::massageComment
	#@+body
	#@+at
	#  Returns s with all runs of whitespace and newlines converted to a 
	# single blank.  It also removes leading and trailing whitespace.

	#@-at
	#@@c

	def massageComment (self,s):
	
		# trace(`get_line(s,0)`)
		s = string.strip(s)
		s = string.replace(s,"\n"," ")
		s = string.replace(s,"\r"," ")
		s = string.replace(s,"\t"," ")
		s = string.replace(s,"  "," ")
		s = string.strip(s)
		return s
	#@-body
	#@-node:6::massageComment
	#@+node:7::massageWebBody
	#@+body
	def massageWebBody (self,s):
	
		type = self.webType
		lb = choose(type=="cweb","@<","<<")
		rb = choose(type=="cweb","@>",">>")
		
		#@<< Remove most newlines from @space and @* sections >>
		#@+node:1::<< Remove most newlines from @space and @* sections >>
		#@+body
		i = 0
		while i < len(s):
			i = skip_ws_and_nl(s,i)
			if self.isDocStart(s,i):
				# Scan to end of the doc part.
				if match(s,i,"@ %def"):
					# Don't remove the newline following %def
					i = skip_line(s,i) ; start = end = i
				else:
					start = end = i ; i += 2
				while i < len(s):
					i = skip_ws_and_nl(s,i)
					if self.isModuleStart(s,i) or match(s,i,lb):
						end = i ; break
					elif type == "cweb": i += 1
					else: i = skip_to_end_of_line(s,i)
				# Remove newlines from start to end.
				doc = s[start:end]
				doc = string.replace(doc,"\n"," ")
				doc = string.replace(doc,"\r","")
				doc = string.strip(doc)
				if doc and len(doc) > 0:
					if doc == "@":
						doc = choose(self.webType=="cweb", "@ ","@\n")
					else:
						doc += "\n\n"
					# trace("new doc:" + `doc`)
					s = s[:start] + doc + s[end:]
					i = start + len(doc)
			else: i = skip_line(s,i)
		#@-body
		#@-node:1::<< Remove most newlines from @space and @* sections >>

		
		#@<< Replace abbreviated names with full names >>
		#@+node:2::<< Replace abbreviated names with full names >>
		#@+body
		i = 0
		while i < len(s):
			# trace(`get_line(s,i)`)
			if match(s,i,lb):
				i += 2 ; j = i ; k = find_on_line(s,j,rb)
				if k > -1:
					name = s[j:k]
					name2 = self.cstLookup(name)
					if name != name2:
						# Replace name by name2 in s.
						# trace("replacing:" + `name` + ", by:" + `name2`)
						s = s[:j] + name2 + s[k:]
						i = j + len(name2)
			i = skip_line(s,i)
		#@-body
		#@-node:2::<< Replace abbreviated names with full names >>

		s = string.rstrip(s)
		return s
	#@-body
	#@-node:7::massageWebBody
	#@+node:8::skipLeadingComments
	#@+body
	#@+at
	#  This skips all leading comments in s, returning the remaining body text 
	# and the massaged comment text.
	# Returns (body, comment)

	#@-at
	#@@c

	def skipLeadingComments (self,s):
	
		# trace(`get_line(s,0)`)
		s_original = s
		s = string.lstrip(s)
		i = 0 ; comment = ""
		if self.fileType in [".c", ".cpp"]: # 11/2/02: don't mess with java comments.
			
			#@<< scan for C-style comments >>
			#@+node:1::<< scan for C-style comments >>
			#@+body
			while i < len(s):
				if match(s,i,"//"): # Handle a C++ comment.
					while match(s,i,'/'):
						i += 1
					j = i ; i = skip_line(s,i)
					comment = comment + self.massageComment(s[j:i]) + "\n"
					# 8/2/02: Preserve leading whitespace for undentBody
					i = skip_ws(s,i)
					i = skip_blank_lines(s,i)
				elif match(s,i,"/*"): # Handle a block C comment.
					j = i + 2 ; i = skip_block_comment (s,i)
					k = choose(match(s,i-2,"*/"),i-2,i)
					if self.fileType == ".java":
						# 8/2/02: a hack: add leading whitespace then remove it.
						comment = self.undentBody(comment)
						comment2 = ' ' * 2 + s[j:k]
						comment2 = self.undentBody(comment2)
						comment = comment + comment2 + "\n"
					else:
						comment = comment + self.massageComment(s[j:k]) + "\n"
					# 8/2/02: Preserve leading whitespace for undentBody
					i = skip_ws(s,i)
					i = skip_blank_lines(s,i)
				else: break
			#@-body
			#@-node:1::<< scan for C-style comments >>

		elif self.fileType == ".pas":
			
			#@<< scan for Pascal comments >>
			#@+node:2::<< scan for Pascal comments >>
			#@+body
			while i < len(s):
				if match(s,i,"//"): # Handle a Pascal line comment.
					while match(s,i,'/'):
						i += 1
					j = i ; i = skip_line(s,i)
					comment = comment + self.massageComment(s[j:i]) + "\n"
					# 8/2/02: Preserve leading whitespace for undentBody
					i = skip_ws(s,i)
					i = skip_blank_lines(s,i)
				elif match(s,i,'(*'):
					j = i + 1 ; i = skip_pascal_block_comment(s,i)
					comment = comment + self.massageComment(s[j:i]) + "\n"
					# 8/2/02: Preserve leading whitespace for undentBody
					i = skip_ws(s,i)
					i = skip_blank_lines(s,i)
				else: break
			#@-body
			#@-node:2::<< scan for Pascal comments >>

		elif self.fileType == ".py":
			
			#@<< scan for Python comments >>
			#@+node:3::<< scan for Python comments >>
			#@+body
			while i < len(s) and match(s,i,'#'):
				j = i + 1 ; i = skip_line(s,i)
				comment = self.undentBody(comment)
				comment = comment + self.massageComment(s[j:i]) + "\n"
				# 8/2/02: Preserve leading whitespace for undentBody
				i = skip_ws(s,i)
				i = skip_blank_lines(s,i)
			#@-body
			#@-node:3::<< scan for Python comments >>

		comment = string.strip(comment)
		if len(comment) == 0:
			return s_original, "" # Bug fix: 11/2/02: don't skip leading whitespace!
		elif self.treeType == "@file":
			return s[i:], "@ " + comment
		else:
			return s[i:], "@ " + comment + "\n"
	#@-body
	#@-node:8::skipLeadingComments
	#@+node:9::undentBody
	#@+body
	#@+at
	#  Removes extra leading indentation from all lines.  We look at the first 
	# line to determine how much leading whitespace to delete.

	#@-at
	#@@c

	def undentBody (self,s):
	
		# trace(`s`)
		c = self.commands
		i = 0 ; result = ""
		# Copy an @code line as is.
		if match(s,i,"@code"):
			j = i ; i = skip_line(s,i) # don't use get_line: it is only for dumping.
			result += s[j:i]
		# Calculate the amount to be removed from each line.
		undent = self.getLeadingIndent(s,i)
		if undent == 0: return s
		while i < len(s):
			j = i ; i = skip_line(s,i) # don't use get_line: it is only for dumping.
			line = s[j:i]
			# trace(`line`)
			line = removeLeadingWhitespace(line,undent,c.tab_width)
			result += line
		return result
	#@-body
	#@-node:9::undentBody
	#@-node:5::Utilities
	#@-others
#@-body
#@-node:0::@file leoImport.py
#@-leo
