#@+leo

#@+node:0::@file leoImport.py

#@+body
from leoGlobals import *
from leoUtils import *


#@<< constants and synonyms >>

#@+node:1::<< constants and synonyms >>

#@+body
indent_refs = true ; dont_indent_refs = false
#@-body

#@-node:1::<< constants and synonyms >>


class importFiles:

	#@+others

	#@+node:2::error

	#@+body
	def error(s): es(s)
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
		#@-body

		#@-node:1::<< initialize importFiles ivars >>

	#@-body

	#@-node:3::import.__init__ (new)

	#@+node:4::Top Level

	#@+node:1::ImportFilesCommand

	#@+body
	def ImportFilesCommand (self,files):
	
		c = self.commands
		current = c.getCurrentVnode()
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
				prefix0 = name0.BeforeLast('.')
				prefix1 = name1.BeforeLast('.')
				if len(prefix0) > 0 and prefix0 == prefix1:
					current = current.insertAsLastChild()
					current.initHeadString(prefix0.AfterLast('\\'))
				#@-body

				#@-node:1::<< Create a parent for two files having a common prefix >>

			i = 0
			while i < count:
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

	#@-node:1::ImportFilesCommand

	#@+node:2::createOutline

	#@+body
	def createOutline (self,fileName,parent):
	
		c = self.commands
		junk, self.fileName = os.path.split(fileName) # junk/fileName
		self.methodName, self.fileType = os.path.splitext(self.fileName) # methodName.fileType
		trace(`self.fileName`)
		# All file types except the following just get copied to the parent node.
		appendFileFlag = type in ["c", "cpp", "cxx", "java", "pas", "py"]
		
	#@<< Read file into buf >>

		#@+node:1::<< Read file into buf >>

		#@+body
		try:
			file = open(fileName)
			buf = file.read()
			file.close()
		except: buf = None
		#@-body

		#@-node:1::<< Read file into buf >>

		# Create the top-level headline.
		v = parent.insertAsLastChild()
		v.initHeadString(self.fileName)
		if appendFileFlag:
			# Set the body text of the root.
			v.t.setTnodeText(buf)
			v.t.setSelection(0,0)
		else:
			if type == "c" or type == "cpp" or type == "cxx":
				self.scanCText(buf,v)
			elif type == "java":
				self.scanJavaText(buf,v,true) #outer level
			elif type == "pas":
				self.scanPascalText(buf,v)
			elif type == "py":
				self.scanPythonText(buf,v)
		return v
	#@-body

	#@-node:2::createOutline

	#@-node:4::Top Level

	#@+node:5::Utilities

	#@+node:1::createHeadline

	#@+body
	def createHeadline (self,parent,body,headline):
	
		# Create the vnode.
		v = parent.insertAsLastChild()
		v.initHeadString(headline)
		# Set the body.
		if len(body) > 0: 
			v.t.setTnodeText(body)
			v.t.setSelection(0,0)
		return v
	#@-body

	#@-node:1::createHeadline

	#@+node:2::getPythonIndent (replace?)

	#@+body

	#@+at
	#  This code takes care not to use blank lines or comment lines in the computation.
	# 
	# This routine can be called at, or just after, a newline character.

	#@-at

	#@@c
	
	def getPythonIndent(self,s,i):
	
		indent = 0
		while i < len(s):
			if s[i] == ' ':
				indent += 1
				i += 1
			elif s[i] == '\t':
				indent += c.tab_width
				i += 1
			elif is_nl(s,i):
				# Blank lines do not affect indentation.
				indent = 0
				i = skip_nl(s,i)
			elif s[i] == '#':
				indent = 0
				# Comment lines do not affect indentation.
				i = skip_line(s,i)
			else: break
		return indent
	#@-body

	#@-node:2::getPythonIndent (replace?)

	#@+node:3::massageBody

	#@+body
	# Inserts < < path methods > > = at the start of the body text and after leading comments.
	
	def massageBody(self,s,methodKind):
		
		# methods = choose(self.fileType == "c","functions","methods")
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
	
	def massageAngleBrackets(self,s):
	
		# Do not use @ < < inside strings.
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
	
	def massageComment(self,s):
	
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
	
	def skipLeadingComments(self,s2):
	
		s = s2
		comment = "" ; newComment = ""
		s = string.lstrip(s)
		i = 0
		while i + 2 < len(s):
			# Skip lines starting with /// <<
			if  i + 6 < len and s.Mid(i,6) == "/// <<":
				while i < len and s[i] != '\n':
					i += 1
				while i < len and is_ws_or_nl(s,i):
					i += 1
			elif i + 16 < len and s.Mid(i,16) == "/// -- end -- <<":
				while i < len and s[i] != '\n':
					i += 1
				while i < len and is_ws_or_nl(s,i):
					i += 1
			elif match(s,i,"//"): # Handle a C++ comment.
				i += 2
				while i < len and s[i] == '/':
					i += 1
				commentStart = i
				while i < len and not is_nl(s,i):
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

	#@+node:7::undentPythonBody (rewrite)

	#@+body

	#@+at
	#  Removes extra leading indentation from all lines.  We look at the first line to determine how much leading whitespace to delete.

	#@-at

	#@@c
	
	def undentPythonBody(self,body):
		
		s = body ; undent = 0
		result = ""
		# Copy an @code line as is.
		if match(s,i,"@code"):
			j = i ; i = skip_past_line(s,i)
			result += s[j:i]
		# Calculate the amount to be removed from each line.
		undent = getPythonIndent(s,i)
		if undent == 0: return body
		while i < len(s):
			ws = 0
			j = skip_past_line(s,i)
			# Skip undent whitespace
			while  i < len(s) and ws < undent:
				if s[i] == ' ':
					ws += 1
					i += 1
				elif s[i] == '\t':
					ws += c.tab_width
					i += 1
				else: break
			result += s[i:j-1]
			i = j
		return result
	#@-body

	#@-node:7::undentPythonBody (rewrite)

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
	
		method_seen = false
		class_seen = false # TRUE is class keyword seen at outer level.
		lparen = None   # Non-null if '(' seen at outer level.
		
	#@<< Initialize the ImportFiles private globals >>

		#@+node:1:C=1:<< Initialize the ImportFiles private globals >>

		#@+body
		# Shared by several routines...
		scan_start = i
		function_start = i
		function_end = None
		name_start = name_end = None
		#@-body

		#@-node:1:C=1:<< Initialize the ImportFiles private globals >>

		while i < len(s): 
			ch = s[i]
			# These cases skip tokens.
			if ch == '/':
				
	#@<< handle possible C comments >>

				#@+node:4:C=2:Shared by C and Java

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

				#@-node:4:C=2:Shared by C and Java

			elif ch == '"' or ch == '\'':
				i = skip_string(s,i)
			# These cases help determine where functions start.
			elif ch == '=':
				
	#@<< handle equal sign in C or Java >>

				#@+node:4:C=2:Shared by C and Java

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

				#@-node:4:C=2:Shared by C and Java

			elif ch == '(':
				
	#@<< handle open paren in C or Java >>

				#@+node:4:C=2:Shared by C and Java

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

				#@-node:4:C=2:Shared by C and Java

			elif ch == ';':
				
	#@<< handle semicolon in C or Java >>

				#@+node:4:C=2:Shared by C and Java

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

				#@-node:4:C=2:Shared by C and Java

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
						scanJavaText(s[brace_ip1+1,brace_ip2], # Don't include either brace.
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
				if is_c_word(s,i,"class"):
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

		#@+node:5:C=3:<< Append any unused text to the parent's body text >>

		#@+body
		# Used by C, Java and Pascal parsers.
		# Do nothing if only whitespace is left.
		
		i = skip_ws_or_nl(s,scan_start)
		if i < len(s):
			parent.appendStringToBody(s[scan_start:])
		#@-body

		#@-node:5:C=3:<< Append any unused text to the parent's body text >>

	#@-body

	#@+node:4:C=2:Shared by C and Java

	#@-node:4:C=2:Shared by C and Java

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
	
	def scanCText(self,s,parent):
	
		include_seen = false ; method_seen = false
		first_ip = i # To terminate backwards scans.
		lparen = None   # Non-null if '(' seen at outer level.
		methodKind = choose(self.fileType == "c","functions","methods")
		
	#@<< Initialize the ImportFiles private globals >>

		#@+node:1:C=1:<< Initialize the ImportFiles private globals >>

		#@+body
		# Shared by several routines...
		scan_start = i
		function_start = i
		function_end = None
		name_start = name_end = None
		#@-body

		#@-node:1:C=1:<< Initialize the ImportFiles private globals >>

		while i < len(s): 
			ch = s[i]
			# These cases skip tokens.
			if ch == '/':
				
	#@<< handle possible C comments >>

				#@+node:5:C=2:Shared by C and Java

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

				#@-node:5:C=2:Shared by C and Java

			elif ch == '"' or ch == '\'':
				i = skip_string(s,i)
			# These cases help determine where functions start.
			elif ch == '=':
				
	#@<< handle equal sign in C or Java >>

				#@+node:5:C=2:Shared by C and Java

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

				#@-node:5:C=2:Shared by C and Java

			elif ch == '(':
				
	#@<< handle open paren in C or Java >>

				#@+node:5:C=2:Shared by C and Java

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

				#@-node:5:C=2:Shared by C and Java

			elif ch == ';':
				
	#@<< handle semicolon in C or Java >>

				#@+node:5:C=2:Shared by C and Java

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

				#@-node:5:C=2:Shared by C and Java

			# These cases and the default case can create child nodes.
			elif ch == '#':
				
	#@<< handle # sign >>

				#@+node:2::<< handle # sign >>

				#@+body
				# if statements may contain function definitions.
				i += 1  # Skip the '#'
				if not include_seen and is_c_word(s,i,"include"):
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
						if is_c_word(s,i,"#include"):
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
					headline = angleBracket(" " + self.methodName + " #includes ")
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

			elif is_c_id(s,i):
				
	#@<< skip c identif ier, typedef, struct, union, namespace >>

				#@+node:4::<< skip c identifier, typedef, struct, union, namespace >>

				#@+body
				if is_c_word(s,i,"typedef"):
					i = skip_typedef(s,i)
					lparen = None
				elif is_c_word(s,i,"struct"):
					i = skip_typedef(s,i)
					# lparen = NULL ;  # This can appear in an argument list.
				elif is_c_word(s,i,"union"):
					i = skip_typedef(s,i)
					# lparen = NULL ;  # This can appear in an argument list.
				elif is_c_word(s,i,"namespace"):
					
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
							len = inner_ip - scan_start
							if len > 0:
								parent.appendStringToBody(s[scan_start:inner_ip])
							# Save and change gModuleName to namespaceName
							savedMethodName = self.methodName
							len = namespace_name_end - namespace_name_start + 1
							namespaceName(namespace_name_start,len)
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
					if match(s[name_start:name_end],"operator"):
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

		#@+node:6:C=3:<< Append any unused text to the parent's body text >>

		#@+body
		# Used by C, Java and Pascal parsers.
		# Do nothing if only whitespace is left.
		
		i = skip_ws_or_nl(s,scan_start)
		if i < len(s):
			parent.appendStringToBody(s[scan_start:])
		#@-body

		#@-node:6:C=3:<< Append any unused text to the parent's body text >>

	#@-body

	#@+node:5:C=2:Shared by C and Java

	#@-node:5:C=2:Shared by C and Java

	#@-node:2::scanCText

	#@+node:3::scanPascalText

	#@+body

	#@+at
	#  Creates a child of parent for each Pascal function definition seen.  See the comments for scanCText for what the text looks like.

	#@-at

	#@@c
	
	def scanPascalText(self,s,parent):
	
		method_seen = false
		methodKind("methods")
		
	#@<< Initialize the ImportFiles private globals >>

		#@+node:1:C=1:<< Initialize the ImportFiles private globals >>

		#@+body
		# Shared by several routines...
		scan_start = i
		function_start = i
		function_end = None
		name_start = name_end = None
		#@-body

		#@-node:1:C=1:<< Initialize the ImportFiles private globals >>

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
				if is_c_word(s,i,"begin"):
					i = skip_pascal_begin_end(s,i)
					if is_c_word(s,i,"end"):
						i = skip_c_id(s,i)
				elif (is_c_word(s,i,"function")  or is_c_word(s,i,"procedure") or
					is_c_word(s,i,"constructor") or is_c_word(s,i,"destructor")):
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
					if is_c_word(s,i,"var"):
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
							elif is_c_word(s,i,"begin"):
								done = true
							else: i += 1
					#@-body

					#@-node:1::<< skip past the semicolon >>

					if not is_c_word(s,i,"begin"):
						continue
					# Skip to the matching end.
					i = skip_pascal_begin_end(s,i)
					if is_c_word(s,i,"end"):
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

		#@+node:3:C=3:<< Append any unused text to the parent's body text >>

		#@+body
		# Used by C, Java and Pascal parsers.
		# Do nothing if only whitespace is left.
		
		i = skip_ws_or_nl(s,scan_start)
		if i < len(s):
			parent.appendStringToBody(s[scan_start:])
		#@-body

		#@-node:3:C=3:<< Append any unused text to the parent's body text >>

	#@-body

	#@-node:3::scanPascalText

	#@+node:4::Python scanners

	#@+node:1::scanPythonClass

	#@+body

	#@+at
	#  Creates a child node c of parent for the class, and children of c for each def in the class.

	#@-at

	#@@c
	
	def scanPythonClass(self,s,parent):
	
		
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
		body = angleBrakets(" " + self.methodName + " methods ") + "=\n\n"
		# i points just after the class line.
		body2 = s[start:i]
		body2 = undentPythonBody(body2)
		body += body2
		class_vnode = self.createHeadline(parent,body,headline)
		#@-body

		#@-node:2::<< create class_vnode  >>

		savedMethodName = self.methodName
		self.methodName = headline
		# Create a node for leading declarations of the class.
		i = scanPythonDecls(s,class_vnode,indent_refs)
		
	#@<< append a reference to class_vnode's methods >>

		#@+node:3::<< Append a reference to class_vnode's methods >>

		#@+body
		# This must be done after the declaration reference is generated.
		ref = "\t" + angleBrakets(" class " + classname + " methods ")
		class_vnode.appendStringToBody(ref + "\n\n")
		#@-body

		#@-node:3::<< Append a reference to class_vnode's methods >>

		
	#@<< create nodes for all defs of the class >>

		#@+node:4::<< create nodes for all defs of the class >>

		#@+body
		line_start = find_line_start(s,i)
		indent1 = getPythonIndent(s[line_start:])
		# Skip past blank lines.
		i = skip_blank_lines(s,i)
		start = i
		indent = indent1
		while i < len(s) and indent >= indent1:
			if is_nl(s[i]):
				j = skip_nl(s,i)
				indent = getPythonIndent(s,j)
				if indent >= indent1: i = j
			elif is_c_word(s,i,"def"):
				start = i = scanPythonDef(start,s,i,class_vnode)
				indent = getPythonIndent(s,i)
			elif is_c_word(s,i,"class"):
				start = i = scanPythonClass(start,s,i,class_vnode)
				indent = getPythonIndent(s,i)
			elif s[i] == '#':
				i = skip_to_end_of_line(s,i)
			elif s[i] == '"' or s[i] == '\'':
				i = skip_python_string(s,i)
			else: i += 1
		#@-body

		#@-node:4::<< create nodes for all defs of the class >>

		self.methodName = savedMethodName
		return i
	#@-body

	#@-node:1::scanPythonClass

	#@+node:2::scanPythonDef

	#@+body

	#@+at
	#  Creates a node of parent for the def.  i points to "def".
	# 
	# start is only used to scan for the start of the def line; it's exact value doesn't matter much.

	#@-at

	#@@c
	
	def scanPythonDef(self,start,s,parent):
	
		
	#@<< set headline or return i >>

		#@+node:1::<< set headline or return i >>

		#@+body
		i = skip_ws(s,i)
		i = skip_c_id(s,i) # Skip the "def"
		i = skip_ws_and_nl(s,i)
		if i < len(s) and is_c_id(s[i]):
			j = i ; i = skip_c_id(s,i)
			headline = s[j:i]
		else: return i
		#@-body

		#@-node:1::<< set headline or return i >>

		
	#@<< skip the Python def >>

		#@+node:2::<< skip the Python def >>

		#@+body
		# This doesn't handle nested defs or classes.  It should.
		# Set indent1 to the indentation of the def line.
		
		line_start = find_line_start(s,i)
		indent1 = getPythonIndent(s[line_start:])
		i = skip_line(s,i) # Skip the def line.
		indent = getPythonIndent(s,i)
		while i < len(s) and indent >= indent1:
			ch = s[i]
			if is_nl(s,i):
				i = skip_nl(s,i)
				indent = getPythonIndent(s,i)
				if indent <= indent1: break
			elif ch == '#': i = skip_line(s,i)
			elif ch == '"' or ch == '\'': i = skip_python_string(s,i)
			else: i += 1
		#@-body

		#@-node:2::<< skip the Python def >>

		# Create the def node.
		save = self.methodName
		self.methodName = headline
		
	#@<< Create def node >>

		#@+node:3::<< Create def node >>

		#@+body
		# Create the header line.
		body = angleBrackets(" " + savedMethodName + " methods ") + "=\n\n"
		# Create body.
		start = skip_blank_lines(s,start)
		body2= s[:i]
		body2 = undentPythonBody(body2)
		body += body2
		# Create the node.
		self.createHeadline(parent,body,headline)
		#@-body

		#@-node:3::<< Create def node >>

		self.methodName = save
		return i
	#@-body

	#@-node:2::scanPythonDef

	#@+node:3::scanPythonDecls

	#@+body
	def scanPythonDecls(self,s,parent,indent_parent_ref_flag):
		
		i = 0 ; done = false
		while not done and i < len(s):
			ch = s[i]
			if ch == '\n': i = skip_nl(s,i)
			elif ch == '#': i = skip_to_end_of_line(s,i)
			elif ch == '"' or ch == '\'': i = skip_python_string(s,i)
			elif is_c_id(s[i]):
				
	#@<< break on def or class >>

				#@+node:1::<< break on def or class >>

				#@+body
				if is_c_word(s,i,"def") or is_c_word(s,i,"class"):
					i = find_line_start(s,i)
					done = true
					break
				else:
					i = skip_c_id(s,i)
				#@-body

				#@-node:1::<< break on def or class >>

			else: i += 1
		j = skip_blank_lines(s,0)
		if is_nl(s,j):
			j = skip_nl(s,j)
		if j < i:
			
	#@<< Create a child node for declarations >>

			#@+node:2::<< Create a child node for declarations >>

			#@+body
			# Create the body.
			body = "@code\n\n" + s[j:i]
			body = undentPythonBody(body)
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
	
	def scanPythonText(self,s,parent):
		
		decls_seen = false ; methodKind = "methods"
		start = i = 0
		while i < len(s):
			ch = s[i]
			if ch == '\n': i = skip_nl(s,i)
			elif ch == '#': i = skip_to_end_of_line(s,i)
			elif ch == '"' or ch == '\'': i = skip_python_string(s,i)
			elif is_c_id(ch):
				
	#@<< handle possible Python function or class >>

				#@+node:1::<< handle possible Python function or class >>

				#@+body
				if is_c_word(s,i,"def"):
					if not decls_seen:
						start = i = scanPythonDecls(s[i:],parent,dont_indent_refs)
						decls_seen = true
					start = i = scanPythonDef(start,s[i:],parent)
				elif is_c_word(s,i,"class"):
					if not decls_seen:
						start = i = scanPythonDecls(s[start:],parent,dont_indent_refs)
						decls_seen = true
					start = i = scanPythonClass(s[start:],parent)
				else:
					i = skip_c_id(s,i)
				#@-body

				#@-node:1::<< handle possible Python function or class >>

			else: i += 1
		
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
