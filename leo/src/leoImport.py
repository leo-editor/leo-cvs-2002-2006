#@+leo-ver=4
#@+node:@file leoImport.py
#@@language python

from leoGlobals import *

#@<< scripts >>
#@+node:<< scripts >>
#@+others
#@+node:importFiles
# An example of running this script:
#
# import leoImport
# leoImport.importFiles("c:/prog/test", ".py")

def importFiles (dir, type = None, kind = "@file"):
	
	from leoGlobals import os_path_exists,os_path_isfile,os_path_join,os_path_splitext

	# Check the params.
	if kind != "@file" and kind != "@root":
		es("kind must be @file or @root: " + `kind`)
		return
	if not os_path_exists(dir):
		es("directory does not exist: " + `dir`)
		return
	
	c = top() # Get the commander.
	
	try:
		files = os.listdir(dir)
		files2 = []
		for f in files:
			path = os_path_join(dir,f)
			if os_path_isfile(path):
				name, ext = os_path_splitext(f)
				if type == None or ext == type:
					files2.append(path)
		if len(files2) > 0:
			c.importCommands.importFilesCommand(files2,kind)
	except:
		es("exception in importFiles script")
		es_exception()
#@nonl
#@-node:importFiles
#@-others
#@nonl
#@-node:<< scripts >>
#@nl

class baseLeoImportCommands:
	"""The base class for Leo's import commands."""
	#@	@+others
	#@+node:import.__init__
	def __init__ (self,c):
	
		self.c = c
		
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
		self.encoding = app.tkEncoding # 2/25/03: was "utf-8"
	#@-node:import.__init__
	#@+node:createOutline
	def createOutline (self,fileName,parent):
	
		c = self.c ; current = c.currentVnode()
		junk, self.fileName = os_path_split(fileName) # junk/fileName
		self.methodName,ext = os_path_splitext(self.fileName) # methodName.fileType
		
		self.fileType = ext
		self.setEncoding()
		# trace(`self.fileName`) ; trace(`self.fileType`)
		# All file types except the following just get copied to the parent node.
		# Note: we should _not_ import header files using this code.
		ext = ext.lower()
		appendFileFlag = ext not in (
			".c", ".cpp", ".cxx", ".el", ".java", ".pas", ".py", ".pyw", ".php")
		#@	<< Read file into s >>
		#@+node:<< Read file into s >>
		try:
			file = open(fileName)
			s = file.read()
			s = toUnicode(s,self.encoding)
			file.close()
		except:
			es("can not open " + fileName)
			import leoTest ; leoTest.fail()
			return None
		#@nonl
		#@-node:<< Read file into s >>
		#@nl
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
		elif ext in (".c", ".cpp", ".cxx"):
			self.scanCText(s,v)
		elif ext == ".el":
			self.scanElispText(s,v)
		elif ext == ".java":
			self.scanJavaText(s,v,true) #outer level
		elif ext == ".pas":
			self.scanPascalText(s,v)
		elif ext in (".py", ".pyw"):
			self.scanPythonText(s,v)
		elif ext == ".php":
			self.scanPHPText(s,v) # 08-SEP-2002 DTHEIN
		else:
			es("createOutline: can't happen")
		return v
	#@nonl
	#@-node:createOutline
	#@+node:importDerivedFiles
	def importDerivedFiles (self,parent,fileName):
		
		c = self.c ; at = c.atFileCommands
		current = c.currentVnode()
		
		c.beginUpdate()
		v = parent.insertAfter()
		v.initHeadString("Imported @file " + fileName)
		c.undoer.setUndoParams("Import",v,select=current)
		at.read(v,importFileName=fileName)
		c.selectVnode(v)
		v.expand()
		c.endUpdate()
	#@-node:importDerivedFiles
	#@+node:importFilesCommand
	def importFilesCommand (self,files,treeType):
	
		c = self.c
		if c == None: return
		v = current = c.currentVnode()
		if current == None: return
		if len(files) < 1: return
		self.treeType = treeType
		c.beginUpdate()
		if 1: # range of update...
			if len(files) == 2:
				#@			<< Create a parent for two files having a common prefix >>
				#@+node:<< Create a parent for two files having a common prefix >>
				#@+at 
				#@nonl
				# The two filenames have a common prefix everything before the 
				# last period is the same.  For example, x.h and x.cpp.
				#@-at
				#@@c
				
				name0 = files[0]
				name1 = files[1]
				prefix0, junk = os_path_splitext(name0)
				prefix1, junk = os_path_splitext(name1)
				if len(prefix0) > 0 and prefix0 == prefix1:
					current = current.insertAsLastChild()
					junk, nameExt = os_path_split(prefix1)
					name,ext = os_path_splitext(prefix1)
					current.initHeadString(name)
				#@nonl
				#@-node:<< Create a parent for two files having a common prefix >>
				#@nl
			for i in xrange(len(files)):
				fileName = files[i]
				v = self.createOutline(fileName,current)
				if v: # 8/11/02: createOutline may fail.
					es("imported " + fileName)
					v.contract()
					v.setDirty()
					c.setChanged(true)
			c.validateOutline()
			current.expand()
		c.endUpdate()
		c.selectVnode(current)
	#@nonl
	#@-node:importFilesCommand
	#@+node:convertMoreString/StringsToOutlineAfter
	# Used by paste logic.
	
	def convertMoreStringToOutlineAfter (self,s,firstVnode):
		s = string.replace(s,"\r","")
		strings = string.split(s,"\n")
		return self.convertMoreStringsToOutlineAfter(strings,firstVnode)
	
	# Almost all the time spent in this command is spent here.
	
	def convertMoreStringsToOutlineAfter (self,strings,firstVnode):
	
		c = self.c
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
				#@			<< Link a new vnode v into the outline >>
				#@+node:<< Link a new vnode v into the outline >>
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
				#@nonl
				#@-node:<< Link a new vnode v into the outline >>
				#@nl
				#@			<< Set the headline string, skipping over the leader >>
				#@+node:<< Set the headline string, skipping over the leader >>
				j = 0
				while match(s,j,'\t'):
					j += 1
				if match(s,j,"+ ") or match(s,j,"- "):
					j += 2
				
				v.initHeadString(s[j:])
				#@nonl
				#@-node:<< Set the headline string, skipping over the leader >>
				#@nl
				#@			<< Count the number of following body lines >>
				#@+node:<< Count the number of following body lines >>
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
				#@nonl
				#@-node:<< Count the number of following body lines >>
				#@nl
				#@			<< Add the lines to the body text of v >>
				#@+node:<< Add the lines to the body text of v >>
				if bodyLines > 0:
					body = ""
					n = index - bodyLines
					while n < index:
						body += strings[n]
						if n != index - 1:
							body += "\n"
						n += 1
					v.t.setTnodeText(body)
				#@nonl
				#@-node:<< Add the lines to the body text of v >>
				#@nl
				v.setDirty()
			else: index += 1
			assert progress < index
		if theRoot:
			theRoot.setDirty()
			c.setChanged(true)
		c.endUpdate()
		return theRoot
	#@nonl
	#@-node:convertMoreString/StringsToOutlineAfter
	#@+node:importFlattenedOutline
	# On entry,files contains at most one file to convert.
	def importFlattenedOutline (self,files):
	
		c = self.c ; current = c.currentVnode()
		if current == None: return
		if len(files) < 1: return
		self.setEncoding()
		fileName = files[0]
		#@	<< Read the file into array >>
		#@+node:<< Read the file into array >>
		try:
			file = open(fileName)
			s = file.read()
			s = string.replace(s,"\r","")
			s = toUnicode(s,self.encoding)
			array = string.split(s,"\n")
			file.close()
		except:
			es("Can not open " + fileName, color="blue")
			import leoTest ; leoTest.fail()
			return
		#@-node:<< Read the file into array >>
		#@nl
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
	#@nonl
	#@-node:importFlattenedOutline
	#@+node:moreHeadlineLevel
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
	#@nonl
	#@-node:moreHeadlineLevel
	#@+node:stringIs/stringsAreValidMoreFile
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
	#@nonl
	#@-node:stringIs/stringsAreValidMoreFile
	#@+node:createOutlineFromWeb
	def createOutlineFromWeb (self,path,parent):
	
		c = self.c ; current = c.currentVnode()
		junk, fileName = os_path_split(path)
		# Create the top-level headline.
		v = parent.insertAsLastChild()
		c.undoer.setUndoParams("Import",v,select=current)
		v.initHeadString(fileName)
		if self.webType=="cweb":
			v.setBodyStringOrPane("@ignore\n" + self.rootLine + "@language cweb")
	
		# Scan the file,creating one section for each function definition.
		self.scanWebFile(path,v)
		return v
	#@nonl
	#@-node:createOutlineFromWeb
	#@+node:importWebCommand
	def importWebCommand (self,files,webType):
	
		c = self.c ; current = c.currentVnode()
		if current == None: return
		if len(files) < 1: return
		self.webType = webType
		c.beginUpdate()
		for i in xrange(len(files)):
			fileName = files[i]
			v = self.createOutlineFromWeb(fileName,current)
			v.contract()
			v.setDirty()
			c.setChanged(true)
		c.selectVnode(current)
		c.endUpdate()
	#@nonl
	#@-node:importWebCommand
	#@+node:findFunctionDef
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
	#@nonl
	#@-node:findFunctionDef
	#@+node:scanBodyForHeadline
	#@+at 
	#@nonl
	# This method returns the proper headline text.
	# 
	# 1. If s contains a section def, return the section ref.
	# 2. cweb only: if s contains @c, return the function name following the 
	# @c.
	# 3. cweb only: if s contains @d name, returns @d name.
	# 4. Otherwise, returns "@"
	#@-at
	#@@c
	
	def scanBodyForHeadline (self,s):
		
		if self.webType == "cweb":
			#@		<< scan cweb body for headline >>
			#@+node:<< scan cweb body for headline >>
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
			#@nonl
			#@-node:<< scan cweb body for headline >>
			#@nl
		else:
			#@		<< scan noweb body for headline >>
			#@+node:<< scan noweb body for headline >>
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
			#@nonl
			#@-node:<< scan noweb body for headline >>
			#@nl
		return "@" # default.
	#@nonl
	#@-node:scanBodyForHeadline
	#@+node:scanWebFile (handles limbo)
	def scanWebFile (self,fileName,parent):
	
		type = self.webType
		lb = choose(type=="cweb","@<","<<")
		rb = choose(type=="cweb","@>",">>")
	
		try: # Read the file into s.
			f = open(fileName)
			s = f.read()
		except:
			es("Can not import " + fileName, color="blue")
			return
	
		#@	<< Create a symbol table of all section names >>
		#@+node:<< Create a symbol table of all section names >>
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
		#@nonl
		#@-node:<< Create a symbol table of all section names >>
		#@nl
		#@	<< Create nodes for limbo text and the root section >>
		#@+node:<< Create nodes for limbo text and the root section >>
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
		#@nonl
		#@-node:<< Create nodes for limbo text and the root section >>
		#@nl
		while i < len(s):
			progress = i
			#@		<< Create a node for the next module >>
			#@+node:<< Create a node for the next module >>
			if type=="cweb":
				assert(self.isModuleStart(s,i))
				start = i
				if self.isDocStart(s,i):
					i += 2
					while i < len(s):
						i = skip_ws_and_nl(s,i)
						if self.isModuleStart(s,i): break
						else: i = skip_line(s,i)
				#@	<< Handle cweb @d, @f, @c and @p directives >>
				#@+node:<< Handle cweb @d, @f, @c and @p directives >>
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
				#@nonl
				#@-node:<< Handle cweb @d, @f, @c and @p directives >>
				#@nl
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
			#@nonl
			#@-node:<< Create a node for the next module >>
			#@nl
			assert(progress < i)
	#@nonl
	#@-node:scanWebFile (handles limbo)
	#@+node:cstCanonicalize
	# We canonicalize strings before looking them up, but strings are entered in the form they are first encountered.
	
	def cstCanonicalize (self,s,lower=true):
		
		if lower:
			s = string.lower(s)
		s = string.replace(s,"\t"," ")
		s = string.replace(s,"\r","")
		s = string.replace(s,"\n"," ")
		s = string.replace(s,"  "," ")
		s = string.strip(s)
		return s
	#@nonl
	#@-node:cstCanonicalize
	#@+node:cstDump
	def cstDump (self):
	
		self.web_st.sort()
		s = "Web Symbol Table...\n\n"
		for name in self.web_st:
			s += name + "\n"
		return s
	#@nonl
	#@-node:cstDump
	#@+node:cstEnter
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
	#@nonl
	#@-node:cstEnter
	#@+node:cstLookup
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
	#@nonl
	#@-node:cstLookup
	#@+node:scanPythonClass
	def scanPythonClass (self,s,i,start,parent):
	
		"""Creates a child node c of parent for the class, and children of c for each def in the class."""
	
		# trace(get_line(s,i))
		classIndent = self.getLeadingIndent(s,i)
		#@	<< set classname and headline, or return i >>
		#@+node:<< set classname and headline, or return i >>
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
		#@nonl
		#@-node:<< set classname and headline, or return i >>
		#@nl
		i = skip_line(s,i) # Skip the class line.
		#@	<< create class_vnode >>
		#@+node:<< create class_vnode  >>
		# Create the section name using the old value of self.methodName.
		if  self.treeType == "@file":
			prefix = ""
		else:
			prefix = angleBrackets(" " + self.methodName + " methods ") + "=\n\n"
			self.methodsSeen = true
		
		# i points just after the class line.
		body = s[start:i]
		body = self.undentBody(body)
		class_vnode = self.createHeadline(parent,prefix + body,headline)
		#@-node:<< create class_vnode  >>
		#@nl
		savedMethodName = self.methodName
		self.methodName = headline
		# Create a node for leading declarations of the class.
		i = self.scanPythonDecls(s,i,class_vnode,classIndent,indent_parent_ref_flag=true)
		#@	<< create nodes for all defs of the class >>
		#@+node:<< create nodes for all defs of the class >>
		indent =  self.getLeadingIndent(s,i)
		start = i = skip_blank_lines(s,i)
		parent_vnode = None # 7/6/02
		while i < len(s) and indent > classIndent:
			progress = i
			if is_nl(s,i):
				backslashNewline = i > 0 and match(s,i-1,"\\\n")
				j = skip_nl(s,i)
				if not backslashNewline:
					indent = self.getLeadingIndent(s,j)
					if indent > classIndent: i = j
					else: break
				else: i = j
			elif match_c_word(s,i,"def"):
				if not parent_vnode:
					#@			<< create parent_vnode >>
					#@+node:<< create parent_vnode >>
					# This must be done after the declaration reference is generated.
					if self.treeType == "@file":
						class_vnode.appendStringToBody("\t@others\n")
					else:
						ref = angleBrackets(" class " + classname + " methods ")
						class_vnode.appendStringToBody("\t" + ref + "\n\n")
					parent_vnode = class_vnode
					#@nonl
					#@-node:<< create parent_vnode >>
					#@nl
				i = start = self.scanPythonDef(s,i,start,parent_vnode)
				indent = self.getLeadingIndent(s,i)
			elif match_c_word(s,i,"class"):
				if not parent_vnode:
					#@			<< create parent_vnode >>
					#@+node:<< create parent_vnode >>
					# This must be done after the declaration reference is generated.
					if self.treeType == "@file":
						class_vnode.appendStringToBody("\t@others\n")
					else:
						ref = angleBrackets(" class " + classname + " methods ")
						class_vnode.appendStringToBody("\t" + ref + "\n\n")
					parent_vnode = class_vnode
					#@nonl
					#@-node:<< create parent_vnode >>
					#@nl
				i = start = self.scanPythonClass(s,i,start,parent_vnode)
				indent = self.getLeadingIndent(s,i)
			elif s[i] == '#': i = skip_to_end_of_line(s,i)
			elif s[i] == '"' or s[i] == '\'': i = skip_python_string(s,i)
			else: i += 1
			assert(progress < i)
		#@nonl
		#@-node:<< create nodes for all defs of the class >>
		#@nl
		#@	<< append any other class material >>
		#@+node:<< append any other class material >>
		s2 = s[start:i]
		if s2:
			class_vnode.appendStringToBody(s2)
		#@nonl
		#@-node:<< append any other class material >>
		#@nl
		self.methodName = savedMethodName
		return i
	#@-node:scanPythonClass
	#@+node:scanPythonDef
	def scanPythonDef (self,s,i,start,parent):
	
		"""Creates a node of parent for the def."""
	
		# trace(get_line(s,i))
		#@	<< set headline or return i >>
		#@+node:<< set headline or return i >>
		i = skip_ws(s,i)
		i = skip_c_id(s,i) # Skip the "def"
		i = skip_ws_and_nl(s,i)
		if i < len(s) and is_c_id(s[i]):
			j = i ; i = skip_c_id(s,i)
			headline = s[j:i]
			# trace("headline:" + `headline`)
		else: return i
		#@nonl
		#@-node:<< set headline or return i >>
		#@nl
		#@	<< skip the Python def >>
		#@+node:<< skip the Python def >>
		# Set defIndent to the indentation of the def line.
		defIndent = self.getLeadingIndent(s,start)
		i = skip_line(s,i) # Skip the def line.
		indent = self.getLeadingIndent(s,i)
		while i < len(s) and indent > defIndent:
			progress = i
			ch = s[i]
			if is_nl(s,i):
				backslashNewline = i > 0 and match(s,i-1,"\\\n")
				i = skip_nl(s,i)
				if not backslashNewline:
					indent = self.getLeadingIndent(s,i)
					if indent <= defIndent:
						break
			elif ch == '#':
				i = skip_to_end_of_line(s,i) # 7/29/02
			elif ch == '"' or ch == '\'':
				i = skip_python_string(s,i)
			else: i += 1
			assert(progress < i)
		#@nonl
		#@-node:<< skip the Python def >>
		#@nl
		# Create the def node.
		savedMethodName = self.methodName
		self.methodName = headline
		#@	<< Create def node >>
		#@+node:<< Create def node >>
		# Create the prefix line for @root trees.
		if self.treeType == "@file":
			prefix = ""
		else:
			prefix = angleBrackets(" " + savedMethodName + " methods ") + "=\n\n"
			self.methodsSeen = true
		
		# Create body.
		start = skip_blank_lines(s,start)
		body = s[start:i]
		body = self.undentBody(body)
		
		# Create the node.
		self.createHeadline(parent,prefix + body,headline)
		
		#@-node:<< Create def node >>
		#@nl
		self.methodName = savedMethodName
		return i
	#@-node:scanPythonDef
	#@+node:scanPythonDecls
	def scanPythonDecls (self,s,i,parent,indent,indent_parent_ref_flag=true):
		
		done = false ; start = i
		while not done and i < len(s):
			progress = i
			# trace(get_line(s,i))
			ch = s[i]
			if ch == '\n':
				backslashNewline = i > 0 and match(s,i-1,"\\\n")
				i = skip_nl(s,i)
				# 2/14/03: break on lesser indention.
				j = skip_ws(s,i)
				if not is_nl(s,j) and not match(s,j,"#") and not backslashNewline:
					lineIndent = self.getLeadingIndent(s,i)
					if lineIndent <= indent:
						break
			elif ch == '#': i = skip_to_end_of_line(s,i)
			elif ch == '"' or ch == '\'':
				i = skip_python_string(s,i)
			elif is_c_id(ch):
				#@			<< break on def or class >>
				#@+node:<< break on def or class >>
				if match_c_word(s,i,"def") or match_c_word(s,i,"class"):
					i = find_line_start(s,i)
					done = true
					break
				else:
					i = skip_c_id(s,i)
				#@nonl
				#@-node:<< break on def or class >>
				#@nl
			else: i += 1
			assert(progress < i)
		j = skip_blank_lines(s,start)
		if is_nl(s,j): j = skip_nl(s,j)
		if j < i:
			#@		<< Create a child node for declarations >>
			#@+node:<< Create a child node for declarations >>
			headline = ref = angleBrackets(" " + self.methodName + " declarations ")
			leading_tab = choose(indent_parent_ref_flag,"\t","")
			
			# Append the reference to the parent's body.
			parent.appendStringToBody(leading_tab + ref + "\n") # 7/6/02
			
			# Create the node for the decls.
			body = self.undentBody(s[j:i])
			if self.treeType == "@root":
				body = "@code\n\n" + body
			self.createHeadline(parent,body,headline)
			#@nonl
			#@-node:<< Create a child node for declarations >>
			#@nl
		return i
	#@nonl
	#@-node:scanPythonDecls
	#@+node:scanPythonText
	# See the comments for scanCText for what the text looks like.
	
	def scanPythonText (self,s,parent):
	
		"""Creates a child of parent for each Python function definition seen."""
	
		decls_seen = false ; start = i = 0
		self.methodsSeen = false
		while i < len(s):
			progress = i
			# trace(get_line(s,i))
			ch = s[i]
			if ch == '\n' or ch == '\r': i = skip_nl(s,i)
			elif ch == '#': i = skip_to_end_of_line(s,i)
			elif ch == '"' or ch == '\'': i = skip_python_string(s,i)
			elif is_c_id(ch):
				#@			<< handle possible Python function or class >>
				#@+node:<< handle possible Python function or class >>
				if match_c_word(s,i,"def") or match_word(s,i,"class"):
					isDef = match_c_word(s,i,"def")
					if not decls_seen:
						parent.appendStringToBody("@ignore\n" + self.rootLine + "@language python\n")
						i = start = self.scanPythonDecls(s,start,parent,-1,indent_parent_ref_flag=false)
						decls_seen = true
						if self.treeType == "@file": # 7/29/02
							parent.appendStringToBody("@others\n") # 7/29/02
					if isDef:
						i = start = self.scanPythonDef(s,i,start,parent)
					else:
						i = start = self.scanPythonClass(s,i,start,parent)
				else:
					i = skip_c_id(s,i)
				#@nonl
				#@-node:<< handle possible Python function or class >>
				#@nl
			else: i += 1
			assert(progress < i)
		if not decls_seen: # 2/17/03
			parent.appendStringToBody("@ignore\n" + self.rootLine + "@language python\n")
		#@	<< Append a reference to the methods of this file >>
		#@+node:<< Append a reference to the methods of this file >>
		if self.treeType == "@root" and self.methodsSeen:
			parent.appendStringToBody(
				angleBrackets(" " + self.methodName + " methods ") + "\n\n")
		#@nonl
		#@-node:<< Append a reference to the methods of this file >>
		#@nl
		#@	<< Append any unused python text to the parent's body text >>
		#@+node:<< Append any unused python text to the parent's body text >>
		# Do nothing if only whitespace is left.
		i = start ; i = skip_ws_and_nl(s,i)
		if i < len(s):
			parent.appendStringToBody(s[start:])
		#@nonl
		#@-node:<< Append any unused python text to the parent's body text >>
		#@nl
	#@nonl
	#@-node:scanPythonText
	#@+node:scanPHPText (Dave Hein)
	# 08-SEP-2002 DTHEIN: Added for PHP import support.
	#
	# PHP uses both # and // as line comments, and /* */ as block comments
	
	def scanPHPText (self,s,parent):
	
		"""Creates a child of parent for each class and function definition seen."""
	
		import re
		#@	<< Append file if not pure PHP >>
		#@+node:<< Append file if not pure PHP >>
		# If the file does not begin with <?php or end with ?> then
		# it is simply appended like a generic import would do.
		s.strip() #remove inadvertent whitespace
		if not s.startswith("<?php") \
		or not (s.endswith("?>") or s.endswith("?>\n") or s.endswith("?>\r\n")):
			es("File seems to be mixed HTML and PHP; importing as plain text file.")
			parent.setBodyStringOrPane("@ignore\n" + self.rootLine + s)
			return
		#@nonl
		#@-node:<< Append file if not pure PHP >>
		#@nl
	
		#@	<< define scanPHPText vars >>
		#@+node:<< define scanPHPText vars >>
		scan_start = 0
		class_start = 0
		function_start = 0
		i = 0
		class_body = ""
		class_node = ""
		phpClassName = re.compile("class\s+([a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*)")
		phpFunctionName = re.compile("function\s+([a-zA-Z_\x7f-\xff][a-zA-Z0-9_\x7f-\xff]*)")
		
		# 14-SEP-2002 DTHEIN: added these 2 variables to allow use of @first/last
		startOfCode = s.find("\n") + 1 # this should be the line containing the initial <?php
		endOfCode = s.rfind("?>") # this should be the line containing the last ?>
		#@-node:<< define scanPHPText vars >>
		#@nl
		# 14-SEP-2002 DTHEIN: Make leading <?php use the @first directive
		parent.appendStringToBody("@first ")	
		parent.appendStringToBody(s[:startOfCode])
		scan_start = i = startOfCode
		while i < endOfCode:
			# line = get_line(s,i) ; trace(`line`)
			ch = s[i]
			# These cases skip tokens.
			if ch == '/' or ch == '#':
				#@			<< handle possible PHP comments >>
				#@+node:<< handle possible PHP comments >>
				if match(s,i,"//"):
					i = skip_line(s,i)
				elif match(s,i,"#"):
					i = skip_line(s,i)
				elif match(s,i,"/*"):
					i = skip_block_comment(s,i)
				else:
					i += 1
				#@nonl
				#@-node:<< handle possible PHP comments >>
				#@nl
			elif ch == '<':
				#@			<< handle possible heredoc string >>
				#@+node:<< handle possible heredoc string >>
				if match(s,i,"<<<"):
					i = skip_heredoc_string(s,i)
				else:
					i += 1
				#@-node:<< handle possible heredoc string >>
				#@nl
			elif ch == '"' or ch == '\'':
				i = skip_string(s,i)
			# These cases help determine where functions start.
			# FIXME: probably want to capture 'var's as class member data
			elif ch == 'f' or ch =='c':
				#@			<< handle possible class or function >>
				#@+node:<< handle possible class or function >>
				#@+at 
				#@nonl
				# In PHP, all functions are typeless and start with the 
				# keyword "function;  all classes start with the keyword 
				# class.
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
				#@nonl
				#@-node:<< handle possible class or function >>
				#@nl
			elif class_start and (ch == '}'):
				#@			<< handle end of class >>
				#@+node:<< handle end of class >>
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
				#@-node:<< handle end of class >>
				#@nl
			else: i += 1
		#@	<< Append any unused text to the parent's body text >>
		#@+node:<< Append any unused text to the parent's body text >>
		parent.appendStringToBody(s[scan_start:endOfCode])
		#@-node:<< Append any unused text to the parent's body text >>
		#@nl
		# 14-SEP-2002 DTHEIN: Make leading <?php use the @first directive
		parent.appendStringToBody("@last ")	
		parent.appendStringToBody(s[endOfCode:])
	#@nonl
	#@-node:scanPHPText (Dave Hein)
	#@+node:scanCText
	# Creates a child of parent for each C function definition seen.
	
	def scanCText (self,s,parent):
	
		#@	<< define scanCText vars >>
		#@+node:<< define scanCText vars >>
		c = self.c
		include_seen = method_seen = false
		methodKind = choose(self.fileType==".c","functions","methods")
		lparen = None   # Non-null if '(' seen at outer level.
		scan_start = function_start = 0
		name = None
		i = 0
		#@nonl
		#@-node:<< define scanCText vars >>
		#@nl
		while i < len(s):
			# line = get_line(s,i) ; trace(`line`)
			ch = s[i]
			# These cases skip tokens.
			if ch == '/':
				#@			<< handle possible C comments >>
				#@+node:<< handle possible C comments >>
				if match(s,i,"//"):
					i = skip_line(s,i)
				elif match(s,i,"/*"):
					i = skip_block_comment(s,i)
				else:
					i += 1
				#@nonl
				#@-node:<< handle possible C comments >>
				#@nl
			elif ch == '"' or ch == '\'':
				i = skip_string(s,i)
			# These cases help determine where functions start.
			elif ch == '=':
				#@			<< handle equal sign in C >>
				#@+node:<< handle equal sign in C>>
				#@+at 
				#@nonl
				# We can not be seeing a function definition when we find an 
				# equal sign at the top level. Equal signs inside parentheses 
				# are handled by the open paren logic.
				#@-at
				#@@c
				
				i += 1 # skip the '='
				function_start = None # We can't be in a function.
				lparen = None   # We have not seen an argument list yet.
				if match(s,i,'='):
					i = skip_braces(s,i)
				#@nonl
				#@-node:<< handle equal sign in C>>
				#@nl
			elif ch == '(':
				#@			<< handle open paren in C >>
				#@+node:<< handle open paren in C >>
				lparen = i
				# This will skip any equal signs inside the paren.
				i = skip_parens(s,i)
				if match(s,i,')'):
					i += 1
					i = skip_ws_and_nl(s,i)
					if match(s,i,';'):
						lparen = None # not a function definition.
				else: lparen = None
				#@nonl
				#@-node:<< handle open paren in C >>
				#@nl
			elif ch == ';':
				#@			<< handle semicolon in C >>
				#@+node:<< handle semicolon in C >>
				#@+at 
				#@nonl
				# A semicolon signals the end of a declaration, thereby 
				# potentially starting the _next_ function defintion.   
				# Declarations end a function definition unless we have 
				# already seen a parenthesis, in which case we are seeing an 
				# old-style function definition.
				#@-at
				#@@c
				
				i += 1 # skip the semicolon.
				if lparen == None:
					function_start = i + 1 # The semicolon ends the declaration.
				#@nonl
				#@-node:<< handle semicolon in C >>
				#@nl
			# These cases and the default case can create child nodes.
			elif ch == '#':
				#@			<< handle # sign >>
				#@+node:<< handle # sign >>
				# if statements may contain function definitions.
				i += 1  # Skip the '#'
				if not include_seen and match_c_word(s,i,"include"):
					include_seen = true
					#@	<< create a child node for all #include statements >>
					#@+node:<< create a child node for all #include statements >>
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
					#@nonl
					#@-node:<< create a child node for all #include statements >>
					#@nl
				else:
					j = i
					i = skip_pp_directive(s,i)
				#@nonl
				#@-node:<< handle # sign >>
				#@nl
			elif ch == '{':
				#@			<< handle open curly bracket in C >>
				#@+node:<< handle open curly bracket in C >> (scans function)
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
						#@		<< create a declaration node >>
						#@+node:<< create a declaration node >>
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
						#@nonl
						#@-node:<< create a declaration node >>
						#@nl
						#@		<< append C function/method reference to parent node >>
						#@+node:<< append C function/method reference to parent node >>
						if self.treeType == "@file":
							parent.appendStringToBody("@others\n")
						else:
							cweb = c.target_language == "cweb"
							lb = choose(cweb,"@<","<<")
							rb = choose(cweb,"@>",">>")
							parent.appendStringToBody(
								lb + " " + self.methodName + " " + methodKind + " " + rb + "\n")
						#@nonl
						#@-node:<< append C function/method reference to parent node >>
						#@nl
					headline = name
					body = s[function_start:function_end]
					body = self.massageBody(body,"functions")
					self.createHeadline(parent,body,headline)
					
					method_seen = true
					scan_start = function_start = i # Set the start of the _next_ function.
					lparen = None
				else:
					i += 1
				#@nonl
				#@-node:<< handle open curly bracket in C >> (scans function)
				#@nl
			elif is_c_id(ch):
				#@			<< handle id, class, typedef, struct, union, namespace >>
				#@+node:<< handle id, class, typedef, struct, union, namespace >>
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
					#@	<< create children for the namespace >>
					#@+node:<< create children for the namespace >>
					#@+at 
					#@nonl
					# Namesspaces change the self.moduleName and recursively 
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
					#@nonl
					#@-node:<< create children for the namespace >>
					#@nl
				# elif match_c_word(s,i,"class"):
					# < < create children for the class > >
				else:
					# Remember the last name before an open parenthesis.
					if lparen == None:
						j = i ; i = skip_c_id(s,i) ; name = s[j:i]
					else:
						i = skip_c_id(s,i)
					#@	<< test for operator keyword >>
					#@+node:<< test for operator keyword >>
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
					#@nonl
					#@-node:<< test for operator keyword >>
					#@nl
				#@nonl
				#@-node:<< handle id, class, typedef, struct, union, namespace >>
				#@nl
			else: i += 1
		#@	<< Append any unused text to the parent's body text >>
		#@+node:<< Append any unused text to the parent's body text >>
		# Used by C, Java and Pascal parsers.
		# Do nothing if only whitespace is left.
		
		i = skip_ws_and_nl(s,scan_start)
		if i < len(s):
			parent.appendStringToBody(s[scan_start:])
		#@nonl
		#@-node:<< Append any unused text to the parent's body text >>
		#@nl
	#@nonl
	#@-node:scanCText
	#@+node:scanElispText & allies
	def scanElispText(self,s,v):
		
		c = self.c
		v.appendStringToBody("@ignore\n@language elisp\n")
		i = 0 ; start = 0
		while i < len(s):
			progress = i
			ch = s[i] ; # trace(get_line(s,i))
			if ch == ';':
				i = skip_line(s,i)
			elif ch == '(':
				j = self.skipElispParens(s,i)
				k = skip_ws(s,i+1)
				if match_word(s,k,"defun") or match_word(s,k,"defconst") or match_word(s,k,"defvar"):
					data = s[start:i]
					if data.strip():
						self.createElispDataNode(v,data)
					self.createElispFunction(v,s[i:j+1])
					start = j+1
				i = j
			else:
				i += 1
			assert(progress < i)
		data = s[start:len(s)]
		if data.strip():
			self.createElispDataNode(v,data)
	#@nonl
	#@-node:scanElispText & allies
	#@+node:skipElispParens
	def skipElispParens (self,s,i):
		
		level = 0 ; n = len(s)
		assert(match(s,i,'('))
		
		while i < n:
			c = s[i]
			if c == '(':
				level += 1 ; i += 1
			elif c == ')':
				level -= 1
				if level <= 0:
					return i
				i += 1
			elif c == '"': i = skip_string(s,i) # Single-quotes are not strings.
			elif match(s,i,";"):  i = skip_line(s,i)
			else: i += 1
		return i
	#@-node:skipElispParens
	#@+node:skipElispId
	def skipElispId (self,s,i):
	
		n = len(s)
		while i < n:
			c = s[i]
			if c in string.ascii_letters or c in string.digits or c == '-':
				i += 1
			else: break
		return i
	#@nonl
	#@-node:skipElispId
	#@+node:createElispFunction
	def createElispFunction (self,v,s):
		
		body = s
		i = 1 # Skip the '('
		i = skip_ws(s,i)
	
		# Set the prefix in the headline.
		assert(match(s,i,"defun") or match_word(s,i,"defconst") or match_word(s,i,"defvar"))
		if match_word(s,i,"defconst"):
			prefix = "const "
		elif match_word(s,i,"defvar"):
			prefix = "var "
		else:
			prefix = ""
	
		# Skip the "defun" or "defconst" or "defvar"
		i = self.skipElispId(s,i)
		
		# Get the following id.
		i = skip_ws(s,i)
		j = self.skipElispId(s,i)
		id = prefix + s[i:j]
	
		self.createHeadline(v,body,id)
	#@-node:createElispFunction
	#@+node:createElispDataNode
	def createElispDataNode (self,v,s):
		
		data = s
		# trace(len(data))
		
		# Skip blank lines and comment lines.
		i = 0
		while i < len(s):
			i = skip_ws_and_nl(s,i)
			if match(s,i,';'):
				i = skip_line(s,i)
			else: break
	
		# Find the next id, probably prefixed by an open paren.
		if match(s,i,"("):
			i = skip_ws(s,i+1)
		j = self.skipElispId(s,i)
		id = s[i:j]
		if not id:
			id = "unnamed data"
	
		self.createHeadline(v,data,id)
	#@nonl
	#@-node:createElispDataNode
	#@+node:scanJavaText
	# Creates a child of parent for each Java function definition seen.
	
	def scanJavaText (self,s,parent,outerFlag): # true if at outer level.
	
		#@	<< define scanJavaText vars >>
		#@+node:<< define scanJavaText vars >>
		method_seen = false
		class_seen = false # true: class keyword seen at outer level.
		interface_seen = false # true: interface keyword seen at outer level.
		lparen = None  # not None if '(' seen at outer level.
		scan_start = 0
		name = None
		function_start = 0 # choose(outerFlag, None, 0)
		i = 0
		#@nonl
		#@-node:<< define scanJavaText vars >>
		#@nl
		# if not outerFlag: trace("inner:" + `s`)
		while i < len(s):
			# trace(`get_line(s,i)`)
			ch = s[i]
			# These cases skip tokens.
			if ch == '/':
				#@			<< handle possible Java comments >>
				#@+node:<< handle possible Java comments >>
				if match(s,i,"//"):
					i = skip_line(s,i)
				elif match(s,i,"/*"):
					i = skip_block_comment(s,i)
				else:
					i += 1
				#@nonl
				#@-node:<< handle possible Java comments >>
				#@nl
			elif ch == '"' or ch == '\'': i = skip_string(s,i)
			# These cases help determine where functions start.
			elif ch == '=':
				#@			<< handle equal sign in Java >>
				#@+node:<< handle equal sign in Java >>
				#@+at 
				#@nonl
				# We can not be seeing a function definition when we find an 
				# equal sign at the top level. Equal signs inside parentheses 
				# are handled by the open paren logic.
				#@-at
				#@@c
				
				i += 1 # skip the '='
				function_start = 0 # 3/23/03: (bug fix: was None) We can't be in a function.
				lparen = None   # We have not seen an argument list yet.
				if match(s,i,'='):
					i = skip_braces(s,i)
				#@nonl
				#@-node:<< handle equal sign in Java >>
				#@nl
			elif ch == '(':
				#@			<< handle open paren in Java >>
				#@+node:<< handle open paren in Java >>
				lparen = i
				# This will skip any equal signs inside the paren.
				i = skip_parens(s,i)
				if match(s,i,')'):
					i += 1
					i = skip_ws_and_nl(s,i)
					if match(s,i,';'):
						lparen = None # not a function definition.
				else: lparen = None
				#@nonl
				#@-node:<< handle open paren in Java >>
				#@nl
			elif ch == ';':
				#@			<< handle semicolon in Java >>
				#@+node:<< handle semicolon in Java >>
				#@+at 
				#@nonl
				# A semicolon signals the end of a declaration, thereby 
				# potentially starting the _next_ function defintion.   
				# Declarations end a function definition unless we have 
				# already seen a parenthesis, in which case we are seeing an 
				# old-style function definition.
				#@-at
				#@@c
				
				i += 1 # skip the semicolon.
				if lparen == None:
					function_start = i + 1 # The semicolon ends the declaration.
				#@nonl
				#@-node:<< handle semicolon in Java >>
				#@nl
				class_seen = false
			# These cases can create child nodes.
			elif ch == '{':
				#@			<< handle open curly bracket in Java >>
				#@+node:<< handle open curly bracket in Java >>
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
						#@		<< create a Java declaration node >>
						#@+node:<< create a Java declaration node >>
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
						#@nonl
						#@-node:<< create a Java declaration node >>
						#@nl
						#@		<< append Java method reference to parent node >>
						#@+node:<< append Java method reference to parent node >>
						if self.treeType == "@file":
							if outerFlag:
								parent.appendStringToBody("\n@others\n")
							else:
								parent.appendStringToBody("\n\t@others\n")
						else:
							kind = choose(outerFlag,"classes","methods")
							ref_name = angleBrackets(" " + self.methodName + " " + kind + " ")
							parent.appendStringToBody(leader + ref_name + "\n")
						#@nonl
						#@-node:<< append Java method reference to parent node >>
						#@nl
					if outerFlag: # Create a class.
						# Backtrack so we remove leading whitespace.
						function_start = find_line_start(s,function_start)
						body = s[function_start:brace_ip1+1]
						body = self.massageBody(body,methodKind)
						v = self.createHeadline(parent,body,headline)
						#@		<< recursively scan the text >>
						#@+node:<< recursively scan the text >>
						# These mark the points in the present function.
						# trace("recursive scan:" + `get_line(s,brace_ip1+ 1)`)
						oldMethodName = self.methodName
						self.methodName = headline
						self.scanJavaText(s[brace_ip1+1:brace_ip2], # Don't include either brace.
							v,false) # inner level
						self.methodName = oldMethodName
						#@-node:<< recursively scan the text >>
						#@nl
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
				#@nonl
				#@-node:<< handle open curly bracket in Java >>
				#@nl
			elif is_c_id(s[i]):
				#@			<< skip and remember the Java id >>
				#@+node:<< skip and remember the Java id >>
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
				#@nonl
				#@-node:<< skip and remember the Java id >>
				#@nl
			else: i += 1
		#@	<< Append any unused text to the parent's body text >>
		#@+node:<< Append any unused text to the parent's body text >>
		# Used by C, Java and Pascal parsers.
		# Do nothing if only whitespace is left.
		
		i = skip_ws_and_nl(s,scan_start)
		if i < len(s):
			parent.appendStringToBody(s[scan_start:])
		#@nonl
		#@-node:<< Append any unused text to the parent's body text >>
		#@nl
	#@nonl
	#@-node:scanJavaText
	#@+node:scanPascalText
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
				#@			<< handle possible Pascal function >>
				#@+node:<< handle possible Pascal function >>
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
					#@	<< remember the function name, or continue >>
					#@+node:<< remember the function name, or continue >>
					if i < len(s) and is_c_id(s[i]):
						j = i ; i = skip_c_id(s,i)
						while i + 1 < len(s) and s[i] == '.' and is_c_id(s[i+1]):
							i += 1 ; j = i
							i = skip_c_id(s,i)
						name = s[j:i]
					else: continue
					#@nonl
					#@-node:<< remember the function name, or continue >>
					#@nl
					#@	<< skip the function definition, or continue >>
					#@+node:<< skip the function definition, or continue >>
					#@<< skip past the semicolon >>
					#@+node:<< skip past the semicolon >>
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
					#@nonl
					#@-node:<< skip past the semicolon >>
					#@nl
					
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
					#@nonl
					#@-node:<< skip the function definition, or continue >>
					#@nl
					if not method_seen:
						method_seen = true
						#@		<< create a child node for leading declarations >>
						#@+node:<< create a child node for leading declarations >>
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
						#@nonl
						#@-node:<< create a child node for leading declarations >>
						#@nl
						#@		<< append noweb method reference to the parent node >>
						#@+node:<< append noweb method reference to the parent node >>
						# Append the headline to the parent's body.
						if self.treeType == "@file":
							parent.appendStringToBody("@others\n")
						else:
							parent.appendStringToBody(
								angleBrackets(" " + self.methodName + " methods ") + "\n")
						#@nonl
						#@-node:<< append noweb method reference to the parent node >>
						#@nl
						function_start = start
					else: function_start = scan_start
					#@	<< create a child node for the function >>
					#@+node:<< create a child node for the function >>
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
					#@nonl
					#@-node:<< create a child node for the function >>
					#@nl
				else: i = skip_c_id(s,i)
				#@nonl
				#@-node:<< handle possible Pascal function >>
				#@nl
			else: i += 1
		#@	<< Append any unused text to the parent's body text >>
		#@+node:<< Append any unused text to the parent's body text >>
		# Used by C, Java and Pascal parsers.
		# Do nothing if only whitespace is left.
		
		i = skip_ws_and_nl(s,scan_start)
		if i < len(s):
			parent.appendStringToBody(s[scan_start:])
		#@nonl
		#@-node:<< Append any unused text to the parent's body text >>
		#@nl
	#@nonl
	#@-node:scanPascalText
	#@+node:convertCodePartToWeb
	# Headlines not containing a section reference are ignored in noweb and generate index index in cweb.
	
	def convertCodePartToWeb (self,s,i,v,result):
	
		# trace(get_line(s,i))
		c = self.c ; nl = self.output_newline
		lb = choose(self.webType=="cweb","@<","<<")
		rb = choose(self.webType=="cweb","@>",">>")
		h = string.strip(v.headString())
		#@	<< put v's headline ref in head_ref >>
		#@+node:<< put v's headline ref in head_ref>>
		#@+at 
		#@nonl
		# We look for either noweb or cweb brackets. head_ref does not include 
		# these brackets.
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
		#@nonl
		#@-node:<< put v's headline ref in head_ref>>
		#@nl
		#@	<< put name following @root or @file in file_name >>
		#@+node:<< put name following @root or @file in file_name >>
		if match(h,0,"@file") or match(h,0,"@root"):
			line = h[5:]
			line = string.strip(line)
			#@	<< set file_name >>
			#@+node:<< Set file_name >>
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
			#@nonl
			#@-node:<< Set file_name >>
			#@nl
		else:
			file_name = line = None
		#@-node:<< put name following @root or @file in file_name >>
		#@nl
		if match_word(s,i,"@root"):
			i = skip_line(s,i)
			#@		<< append ref to file_name >>
			#@+node:<< append ref to file_name >>
			if self.webType == "cweb":
				if not file_name:
					result += "@<root@>=" + nl
				else:
					result += "@(" + file_name + "@>" + nl # @(...@> denotes a file.
			else:
				if not file_name:
					file_name = "*"
				result += lb + file_name + rb + "=" + nl
			#@-node:<< append ref to file_name >>
			#@nl
		elif match_word(s,i,"@c") or match_word(s,i,"@code"):
			i = skip_line(s,i)
			#@		<< append head_ref >>
			#@+node:<< append head_ref >>
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
			#@nonl
			#@-node:<< append head_ref >>
			#@nl
		elif match_word(h,0,"@file"):
			# Only do this if nothing else matches.
			#@		<< append ref to file_name >>
			#@+node:<< append ref to file_name >>
			if self.webType == "cweb":
				if not file_name:
					result += "@<root@>=" + nl
				else:
					result += "@(" + file_name + "@>" + nl # @(...@> denotes a file.
			else:
				if not file_name:
					file_name = "*"
				result += lb + file_name + rb + "=" + nl
			#@-node:<< append ref to file_name >>
			#@nl
			i = skip_line(s,i) # 4/28/02
		else:
			#@		<< append head_ref >>
			#@+node:<< append head_ref >>
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
			#@nonl
			#@-node:<< append head_ref >>
			#@nl
		i,result = self.copyPart(s,i,result)
		return i, string.strip(result) + nl
		
	#@+at 
	#@nonl
	# %defs a b c
	#@-at
	#@nonl
	#@-node:convertCodePartToWeb
	#@+node:convertDocPartToWeb (handle @ %def)
	def convertDocPartToWeb (self,s,i,result):
		
		nl = self.output_newline
	
		# trace(get_line(s,i))
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
	#@nonl
	#@-node:convertDocPartToWeb (handle @ %def)
	#@+node:convertVnodeToWeb
	#@+at 
	#@nonl
	# This code converts a vnode to noweb text as follows:
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
		startInCode = not app.config.at_root_bodies_start_in_doc_mode
		nl = self.output_newline
		s = v.bodyString()
		lb = choose(self.webType=="cweb","@<","<<")
		i = 0 ; result = "" ; docSeen = false
		while i < len(s):
			progress = i
			# trace(get_line(s,i))
			i = skip_ws_and_nl(s,i)
			if self.isDocStart(s,i) or match_word(s,i,"@doc"):
				i,result = self.convertDocPartToWeb(s,i,result)
				docSeen = true
			elif (match_word(s,i,"@code") or match_word(s,i,"@root") or
				match_word(s,i,"@c") or match(s,i,lb)):
				#@			<< Supply a missing doc part >>
				#@+node:<< Supply a missing doc part >>
				if not docSeen:
					docSeen = true
					result += choose(self.webType=="cweb",nl+"@ ",nl+"@"+nl)
				#@nonl
				#@-node:<< Supply a missing doc part >>
				#@nl
				i,result = self.convertCodePartToWeb(s,i,v,result)
			elif self.treeType == "@file" or startInCode:
				#@			<< Supply a missing doc part >>
				#@+node:<< Supply a missing doc part >>
				if not docSeen:
					docSeen = true
					result += choose(self.webType=="cweb",nl+"@ ",nl+"@"+nl)
				#@nonl
				#@-node:<< Supply a missing doc part >>
				#@nl
				i,result = self.convertCodePartToWeb(s,i,v,result)
			else:
				i,result = self.convertDocPartToWeb(s,i,result)
				docSeen = true
			assert(progress < i)
		result = string.strip(result)
		if len(result) > 0:
			result += nl
		return result
	#@nonl
	#@-node:convertVnodeToWeb
	#@+node:copyPart
	# Copies characters to result until the end of the present section is seen.
	
	def copyPart (self,s,i,result):
	
		# trace(get_line(s,i))
		lb = choose(self.webType=="cweb","@<","<<")
		rb = choose(self.webType=="cweb","@>",">>")
		type = self.webType
		while i < len(s):
			progress = j = i # We should be at the start of a line here.
			i = skip_nl(s,i) ; i = skip_ws(s,i)
			if self.isDocStart(s,i):
				return i, result
			if (match_word(s,i,"@doc") or
				match_word(s,i,"@c") or
				match_word(s,i,"@root") or
				match_word(s,i,"@code")): # 2/25/03
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
	#@nonl
	#@-node:copyPart
	#@+node:exportHeadlines
	def exportHeadlines (self,fileName):
		
		c = self.c ; v = c.currentVnode()
		nl = self.output_newline
		if not v: return
		self.setEncoding()
		after = v.nodeAfterTree()
		firstLevel = v.level()
		try:
			mode = app.config.output_newline
			mode = choose(mode=="platform",'w','wb')
			file = open(fileName,mode)
			while v and v != after:
				head = v.moreHead(firstLevel,useVerticalBar=true)
				head = toEncodedString(head,self.encoding,reportErrors=true)
				file.write(head + nl)
				v = v.threadNext()
			file.close()
		except:
			es("exception while exporting headlines")
			es_exception()
	#@nonl
	#@-node:exportHeadlines
	#@+node:flattenOutline
	def flattenOutline (self,fileName):
	
		c = self.c ; v = c.currentVnode()
		nl = self.output_newline
		if not v: return
		self.setEncoding()
		after = v.nodeAfterTree()
		firstLevel = v.level()
		try:
			# 10/14/02: support for output_newline setting.
			mode = app.config.output_newline
			mode = choose(mode=="platform",'w','wb')
			file = open(fileName,mode)
			while v and v != after:
				head = v.moreHead(firstLevel)
				head = toEncodedString(head,self.encoding,reportErrors=true)
				file.write(head + nl)
				body = v.moreBody() # Inserts escapes.
				if len(body) > 0:
					body = toEncodedString(body,self.encoding,reportErrors=true)
					file.write(body + nl)
				v = v.threadNext()
			file.close()
		except:
			es("exception while flattening outline")
			es_exception()
	#@nonl
	#@-node:flattenOutline
	#@+node:outlineToWeb
	def outlineToWeb (self,fileName,webType):
	
		c = self.c ; v = c.currentVnode()
		nl = self.output_newline
		if v == None: return
		self.setEncoding()
		self.webType = webType
		after = v.nodeAfterTree()
		try: # This can fail if the file is open by another app.
			# 10/14/02: support for output_newline setting.
			mode = app.config.output_newline
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
					s = toEncodedString(s,self.encoding,reportErrors=true)
					file.write(s)
					if s[-1] != '\n':
						file.write(nl)
				v = v.threadNext()
			file.close()
		except:
			es("exception in Outline To noweb command")
			es_exception()
	#@nonl
	#@-node:outlineToWeb
	#@+node:removeSentinelsCommand
	def removeSentinelsCommand (self,fileName):
	
		self.setEncoding()
		path, self.fileName = os_path_split(fileName) # path/fileName
		#@	<< Read file into s >>
		#@+node:<< Read file into s >>
		try:
			file = open(fileName)
			s = file.read()
			s = toUnicode(s,self.encoding)
			file.close()
		except:
			es("Can not open " + fileName, color="blue")
			import leoTest ; leoTest.fail()
			return
		#@nonl
		#@-node:<< Read file into s >>
		#@nl
		valid = true
		line_delim = start_delim = end_delim = None
		#@	<< set delims from the header line >>
		#@+node:<< set delims from the header line >>
		# This code is similar to atFile::scanHeader.
		
		tag = "@+leo" ; tag2 = "-ver="
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
		# Skip a version tag. Bug fix: 10/15/03
		if valid and match(s,i,tag2):
			i += len(tag2) + 1 # Skip the tag and the actual version.
		# The closing comment delim is the trailing non-whitespace.
		i = j = skip_ws(s,i)
		while i < len(s) and not is_ws(s[i]) and not is_nl(s,i):
			i += 1
		if j < i:
			start_delim = line_delim
			end_delim = s[j:i]
			line_delim = None
		#@nonl
		#@-node:<< set delims from the header line >>
		#@nl
		if valid == false:
			es("invalid @+leo sentinel in " + fileName)
			return
	
		# trace("line: '%s', start: '%s', end: '%s'" % (line_delim,start_delim,end_delim))
	
		s = self.removeSentinelLines(s,line_delim,start_delim,end_delim)
		ext = app.config.remove_sentinels_extension
		if ext == None or len(ext) == 0:
			ext = ".txt"
		if ext[0] == '.':
			newFileName = os_path_join(path,fileName+ext)
		else:
			head,ext2 = os_path_splitext(fileName) 
			newFileName = os_path_join(path,head+ext+ext2)
		#@	<< Write s into newFileName >>
		#@+node:<< Write s into newFileName >>
		try:
			mode = app.config.output_newline
			mode = choose(mode=="platform",'w','wb')
			file = open(newFileName,mode)
			s = toEncodedString(s,self.encoding,reportErrors=true)
			file.write(s)
			file.close()
			es("creating: " + newFileName)
		except:
			es("exception creating: " + newFileName)
			es_exception()
		#@nonl
		#@-node:<< Write s into newFileName >>
		#@nl
	#@nonl
	#@-node:removeSentinelsCommand
	#@+node:removeSentinelLines
	#@+at 
	#@nonl
	# Properly removes all sentinel lines in s.  Only leading single-line 
	# comments may be sentinels.
	# 
	# line_delim, start_delim and end_delim are the comment delimiters.
	#@-at
	#@@c
	
	def removeSentinelLines(self,s,line_delim,start_delim,end_delim):
	
		i = 0 ; result = [] ; first = true
		while i < len(s):
			start = i # The start of the next syntax element.
			if first or is_nl(s,i):
				first = false
				#@			<< handle possible sentinel >>
				#@+node:<< handle possible sentinel >>
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
				#@nonl
				#@-node:<< handle possible sentinel >>
				#@nl
			elif match(s,i,line_delim):
				i = skip_to_end_of_line(s,i)
			elif match(s,i,start_delim):
				i = skip_matching_delims(s,i,start_delim,end_delim)
			elif match(s,i,"'") or match(s,i,'"'):
				i = skip_string(s,i)
			else:
				i += 1
			assert(i==0 or start<i)
			result.append(s[start:i])# 12/11/03: hugely faster than string concatenation.
	
		result = ''.join(result) 
		return result
	#@nonl
	#@-node:removeSentinelLines
	#@+node:weave
	def weave (self,filename):
		
		c = self.c ; v = c.currentVnode()
		nl = self.output_newline
		if not v: return
		self.setEncoding()
		#@	<< open filename to f, or return >>
		#@+node:<< open filename to f, or return >>
		try:
			# 10/14/02: support for output_newline setting.
			mode = app.config.output_newline
			mode = choose(mode=="platform",'w','wb')
			f = open(filename,mode)
			if not f: return
		except:
			es("exception opening:" + filename)
			es_exception()
			return
		#@nonl
		#@-node:<< open filename to f, or return >>
		#@nl
		after = v.nodeAfterTree()
		while v and v != after:
			s = v.bodyString()
			s2 = string.strip(s)
			if s2 and len(s2) > 0:
				f.write("-" * 60) ; f.write(nl)
				#@			<< write the context of v to f >>
				#@+node:<< write the context of v to f >>
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
					line = toEncodedString(line,self.encoding,reportErrors=true)
					f.write(line)
					f.write(nl)
				#@-node:<< write the context of v to f >>
				#@nl
				f.write("-" * 60) ; f.write(nl)
				s = toEncodedString(s,self.encoding,reportErrors=true) # 2/25/03
				f.write(string.rstrip(s) + nl)
			v = v.threadNext()
		f.flush()
		f.close()
	#@nonl
	#@-node:weave
	#@+node:createHeadline
	def createHeadline (self,parent,body,headline):
	
		# trace("parent,headline:" + `parent` + ":" + `headline`)
		# Create the vnode.
		v = parent.insertAsLastChild()
		v.initHeadString(headline,self.encoding)
		# Set the body.
		if len(body) > 0:
			v.setBodyStringOrPane(body,self.encoding)
		return v
	#@nonl
	#@-node:createHeadline
	#@+node:error
	def error (self,s): es(s)
	#@nonl
	#@-node:error
	#@+node:getLeadingIndent
	def getLeadingIndent (self,s,i):
	
		"""Return the leading whitespace of a line, ignoring blank and comment lines."""
	
		c = self.c
		i = find_line_start(s,i)
		while i < len(s):
			# trace(`get_line(s,i)`)
			j = skip_ws(s,i) # Bug fix: 2/14/03
			if is_nl(s,j) or match(s,j,"#"): # Bug fix: 2/14/03
				i = skip_line(s,i) # ignore blank lines and comment lines.
			else:
				i, width = skip_leading_ws_with_indent(s,i,c.tab_width)
				# trace("returns:" + `width`)
				return width
		# trace("returns:0")
		return 0
	#@nonl
	#@-node:getLeadingIndent
	#@+node:isDocStart and isModuleStart
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
	#@-node:isDocStart and isModuleStart
	#@+node:massageBody
	def massageBody (self,s,methodKind):
		
		# trace(`s`)
		# trace(`get_line(s,0)`)
		c = self.c
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
	#@nonl
	#@-node:massageBody
	#@+node:massageComment
	def massageComment (self,s):
	
		"""Returns s with all runs of whitespace and newlines converted to a single blank.
		
		Also removes leading and trailing whitespace."""
	
		# trace(`get_line(s,0)`)
		s = string.strip(s)
		s = string.replace(s,"\n"," ")
		s = string.replace(s,"\r"," ")
		s = string.replace(s,"\t"," ")
		s = string.replace(s,"  "," ")
		s = string.strip(s)
		return s
	#@nonl
	#@-node:massageComment
	#@+node:massageWebBody
	def massageWebBody (self,s):
	
		type = self.webType
		lb = choose(type=="cweb","@<","<<")
		rb = choose(type=="cweb","@>",">>")
		#@	<< Remove most newlines from @space and @* sections >>
		#@+node:<< Remove most newlines from @space and @* sections >>
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
		#@nonl
		#@-node:<< Remove most newlines from @space and @* sections >>
		#@nl
		#@	<< Replace abbreviated names with full names >>
		#@+node:<< Replace abbreviated names with full names >>
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
		#@nonl
		#@-node:<< Replace abbreviated names with full names >>
		#@nl
		s = string.rstrip(s)
		return s
	#@nonl
	#@-node:massageWebBody
	#@+node:setEncoding
	def setEncoding (self):
		
		# scanDirectives checks the encoding: may return None.
		dict = scanDirectives(self.c)
		encoding = dict.get("encoding")
		if encoding and isValidEncoding(encoding):
			self.encoding = encoding
		else:
			self.encoding = app.tkEncoding # 2/25/03
	
		# print self.encoding
	#@-node:setEncoding
	#@+node:skipLeadingComments
	def skipLeadingComments (self,s):
	
		"""Skips all leading comments in s, returning the remaining body text and the massaged comment text.
	
		Returns (body, comment)"""
	
		# trace(`get_line(s,0)`)
		s_original = s
		s = string.lstrip(s)
		i = 0 ; comment = ""
		if self.fileType in [".c", ".cpp"]: # 11/2/02: don't mess with java comments.
			#@		<< scan for C-style comments >>
			#@+node:<< scan for C-style comments >>
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
			#@nonl
			#@-node:<< scan for C-style comments >>
			#@nl
		elif self.fileType == ".pas":
			#@		<< scan for Pascal comments >>
			#@+node:<< scan for Pascal comments >>
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
			#@nonl
			#@-node:<< scan for Pascal comments >>
			#@nl
		elif self.fileType == ".py":
			#@		<< scan for Python comments >>
			#@+node:<< scan for Python comments >>
			while i < len(s) and match(s,i,'#'):
				j = i + 1 ; i = skip_line(s,i)
				comment = self.undentBody(comment)
				comment = comment + self.massageComment(s[j:i]) + "\n"
				# 8/2/02: Preserve leading whitespace for undentBody
				i = skip_ws(s,i)
				i = skip_blank_lines(s,i)
			#@nonl
			#@-node:<< scan for Python comments >>
			#@nl
		comment = string.strip(comment)
		if len(comment) == 0:
			return s_original, "" # Bug fix: 11/2/02: don't skip leading whitespace!
		elif self.treeType == "@file":
			return s[i:], "@ " + comment
		else:
			return s[i:], "@ " + comment + "\n"
	#@nonl
	#@-node:skipLeadingComments
	#@+node:undentBody
	# We look at the first line to determine how much leading whitespace to delete.
	
	def undentBody (self,s):
	
		"""Removes extra leading indentation from all lines."""
	
		# trace(`s`)
		c = self.c
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
	#@nonl
	#@-node:undentBody
	#@-others
	
class leoImportCommands (baseLeoImportCommands):
	"""A class that implements Leo's import commands."""
	pass
#@nonl
#@-node:@file leoImport.py
#@-leo
