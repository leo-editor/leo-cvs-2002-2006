#@+leo

#@+node:0::@file leoColor.py
#@+body
# Syntax coloring routines for Leo.py

from leoGlobals import *
from leoUtils import *
import keyword, string


#@<< define colorizer constants >>
#@+node:1::<< define colorizer constants >>
#@+body
# We only define states that can continue across lines.
normalState, docState, nocolorState, string3State, blockCommentState = 1,2,3,4,5
#@-body
#@-node:1::<< define colorizer constants >>


#@<< define colorizer keywords >>
#@+node:2:C=1:<< define colorizer keywords >>
#@+body
leoKeywords = (
	# Leo 2 directives.
	"@","@c","@code","@doc","@color","@comment",
	"@delims","@first","@language","@nocolor","@others",
	"@pagewidth","@path","@tabwidth",
	# Leo 1 directives.
	"@cweb","@ignore","@noweb","@root","@unit","@silent","@terse","@verbose")
	
c_keywords = (
	# C keywords
	"auto","break","case","char","continue",
	"default","do","double","else","enum","extern",
	"float","for","goto","if","int","long","register","return",
	"short","signed","sizeof","static","struct","switch",
	"typedef","union","unsigned","void","volatile","while"
	# C++ keywords
	"asm","bool","catch","class","const_cast",
	"delete","dynamic_cast","explicit","false","friend",
	"inline","mutable","namespace","new","operator",
	"private","protected","public","reinterpret_cast","static_cast",
	"template","this","throw","true","try",
	"typeid","typename","using","virtual","wchar_t")

cweb_keywords = (
	"@<","@>","@>=","@","@ ","@*",
	"@c","@d","@D","@f","@p")

html_keywords = (
	# HTML constructs.
	"<","</",">",
	'"',
	"<!---","<!--","<!",
	"<%","%>",
	"<a","</a",
	"<img",
	"<cf","</cf",
	# Common tags: tables
	"<table","</table",
	"<td","</td",
	"<th","</th",
	"<tr","</tr",
	"<caption","</caption",
	"<col","</col",
	"<colgroup","</colgroup",
	"<tbody","</tbody",
	"<tfoot","</tfoot",
	"<thead","</thead",	
	# Common tags: styles
	"<style","</style",
	# Common tags: scripts
	"<script","</script",
	# Escapes
	"&amp;", "&lt;", "&gt;", "&quot;" )

java_keywords = (
	"abstract","boolean","break","byte","byvalue",
	"case","cast","catch","char","class","const","continue",
	"default","do","double","else","extends",
	"false","final","finally","float","for","future",
	"generic","goto","if","implements","import","inner",
	"instanceof","int","interface","long","native",
	"new","null","operator","outer",
	"package","private","protected","public","rest","return",
	"short","static","super","switch","synchronized",
	"this","throw","transient","true","try",
	"var","void","volatile","while")

pascal_keywords = (
	"and","array","as","begin",
	"case","const","class","constructor","cdecl"
	"div","do","downto","destructor","dispid","dynamic",
	"else","end","except","external",
	"false","file","for","forward","function","finally",
	"goto","if","in","is","label","library",
	"mod","message","nil","not","nodefault""of","or","on",
	"procedure","program","packed","pascal"
	"private","protected","public","published",
	"record","repeat","raise","read","register",
	"set","string","shl","shr","stdcall",
	"then","to","true","type","try","until","unit","uses"
	"var","virtual","while","with","xor"
	# object pascal
	"asm","absolute","abstract","assembler","at","automated",
	"finalization",
	"implementation","inherited","initialization","inline","interface",
	"object","override","resident","resourcestring",
	"threadvar",
	# limited contexts
	"exports","property","default","write","stored","index","name" )

perl_keywords = (
	"continue","do","else","elsif","format","for","format","for","foreach",
	"if","local","package","sub","tr","unless","until","while","y",
	# Comparison operators
	"cmp","eq","ge","gt","le","lt","ne",
	# Matching ooperators
	"m","s"
	# Unary functions
	"alarm","caller","chdir","cos","chroot","exit","eval","exp",
	"getpgrp","getprotobyname","gethostbyname","getnetbyname","gmtime",
	"hex","int","length","localtime","log","ord","oct",
	"require","reset","rand","rmdir","readlink",
	"scalar","sin","sleep","sqrt","srand","umask",
	# Transfer ops
	"next","last","redo","go","dump",
	# File operations...
	"select","open",
	# FL ops
	"binmode","close","closedir","eof",
	"fileno","getc","getpeername","getsockname","lstat",
	"readdir","rewinddir","stat","tell","telldir","write",
	# FL2 ops
	"bind","connect","flock","listen","opendir",
	"seekdir","shutdown","truncate",
	# FL32 ops
	"accept","pipe",
	# FL3 ops
	"fcntl","getsockopt","ioctl","read",
	"seek","send","sysread","syswrite",
	# FL4 & FL5 ops
	"recv","setsocket","socket","socketpair",
	# Array operations
	"pop","shift","split","delete",
	# FLIST ops
	"sprintf","grep","join","pack",
	# LVAL ops
	"chop","defined","study","undef",
	# f0 ops
	"endhostent","endnetent","endservent","endprotoent",
	"endpwent","endgrent","fork",
	"getgrent","gethostent","getlogin","getnetent","getppid",
	"getprotoent","getpwent","getservent",
	"setgrent","setpwent","time","times","wait","wantarray",
	# f1 ops
	"getgrgid","getgrnam","getprotobynumber","getpwnam","getpwuid",
	"sethostent","setnetent","setprotoent","setservent",
	# f2 ops
	"atan2","crypt",
	"gethostbyaddr","getnetbyaddr","getpriority","getservbyname","getservbyport",
	"index","link","mkdir","msgget","rename",
	"semop","setpgrp","symlink","unpack","waitpid",
	# f2 or 3 ops
	"index","rindex","substr",
	# f3 ops
	"msgctl","msgsnd","semget","setpriority","shmctl","shmget","vec",
	# f4 & f5 ops
	"semctl","shmread","shmwrite","msgrcv",
	# Assoc ops
	"dbmclose","each","keys","values",
	# List ops
	"chmod","chown","die","exec","kill",
	"print","printf","return","reverse",
	"sort","system","syscall","unlink","utime","warn")

perlpod_keywords = perl_keywords
	
python_keywords = (
	"and",       "del",       "for",       "is",        "raise",    
	"assert",    "elif",      "from",      "lambda",    "return",   
	"break",     "else",      "global",    "not",       "try",      
	"class",     "except",    "if",        "or",        "yield",   
	"continue",  "exec",      "import",    "pass",      "while",
	"def",       "finally",   "in",        "print")
#@-body
#@-node:2:C=1:<< define colorizer keywords >>


#@<< define colorizer functions >>
#@+node:3::<< define colorizer functions >>
#@+body
def index(i,j):

	if type(i) != type("end"):
		i = `i`
	if type(j) != type("end"):
		j = `j`
	return i + '.' + j

#@-body
#@-node:3::<< define colorizer functions >>


class colorizer:

	#@+others
	#@+node:4:C=2:color.__init__
	#@+body
	def disable (self):
	
		print "disabling all syntax coloring"
		self.enabled=false
	
	def __init__(self, commands):
	
		self.commands = commands
		self.count = 0 # how many times this has been called.
		self.use_hyperlinks = false # true: use hyperlinks and underline "live" links.
		self.enabled = true # true: syntax coloring enabled
		self.showInvisibles = false # true: show "invisible" characters.
		self.delim = None # delimiter for triple strings.
		trace("-nocolor", self.disable)
	#@-body
	#@-node:4:C=2:color.__init__
	#@+node:5::color.callbacks...
	#@+node:1::OnHyperLinkControlClick
	#@+body
	def OnHyperLinkControlClick (self,v):
	
		pass
	#@-body
	#@-node:1::OnHyperLinkControlClick
	#@+node:2::OnHyperLinkEnter
	#@+body
	def OnHyperLinkEnter (self,v):
	
		pass # trace(`v` + ", " + `v.tagName`)
	#@-body
	#@-node:2::OnHyperLinkEnter
	#@+node:3::OnHyperLinkLeave
	#@+body
	def OnHyperLinkLeave (self,v):
	
		pass # trace(`v`)
	#@-body
	#@-node:3::OnHyperLinkLeave
	#@-node:5::color.callbacks...
	#@+node:6:C=3:colorize
	#@+body
	def colorize(self,v,body):
	
		if self.enabled:
			type = self.updateSyntaxColorer(v)
	
			if 1:
				self.colorizeAnyLanguage(v,body,type)
			else:
				if type == python_language:
					self.colorizePython(v,body)
				else:
					self.colorizePlain(body)
	#@-body
	#@-node:6:C=3:colorize
	#@+node:7::colorizePlain
	#@+body
	def colorizePlain (self,body):
	
		# Remove all tags from body.
		body.tag_delete(
			"comment", "docPart", "keyword", "leoKeyword",
			"name", "nameBrackets", "string")
	#@-body
	#@-node:7::colorizePlain
	#@+node:8:C=4:colorizePython
	#@+body
	tags = (
		"blank", "comment", "docPart", "keyword", "leoKeyword",
		"link", "name", "nameBrackets", "string", "tab")
	
	def colorizePython(self,v,body):
	
		hyperCount = 0 # Number of hypertext tags
		self.body = body # For callbacks
		s = body.get("1.0", "end")
		sel = body.index("insert") # get the location of the insert point
		start, end = string.split(sel,'.')
		start = int(start)
		# trace(`self.count` + `sel`)
		# trace(`body.tag_names()`)
	
		if 0: # Remove all tags from the selected line.
			for tag in self.tags:
				body.tag_remove(tag, index(start,0), index(start,"end"))
		else: # Remove all tags from body.
			body.tag_delete(
				"blank", "comment", "docPart", "keyword", "leoKeyword",
				"link", "name", "nameBrackets", "string", "tab")
		
		#@<< configure tags >>
		#@+node:1:C=5:<< configure tags >>
		#@+body
		# Must use foreground, not fg
		body.tag_config("comment", foreground="red")
		body.tag_config("docPart", foreground="red")
		body.tag_config("keyword", foreground="blue")
		if self.use_hyperlinks: # underline=self.use_hyperlinks doesn't seem to work.
			body.tag_config("link", foreground="red",underline=1) # Defined section name
		else:
			body.tag_config("link", foreground="red",underline=0) # Defined section name
		body.tag_config("leoKeyword", foreground="blue")
		if 0: # Looks good, but problems when text is selected.
			body.tag_config("name", foreground="red", background="gray90") # Undefined section name
		else: # Reverse the underlining used for defined section names.
			if self.use_hyperlinks: # underline=(not self.use_hyperlinks) doesn't seem to work.
				body.tag_config("name", foreground="red", underline=0) # Undefined section name
			else:
				body.tag_config("name", foreground="red", underline=1) # Undefined section name
		body.tag_config("nameBrackets", foreground="blue")
		body.tag_config("string", foreground="gray50")
		
		if self.showInvisibles:
			if 1: # Very poor, and vaguely usable.
				body.tag_config("blank",background="black",bgstipple="gray25")
				body.tag_config("tab",background="black",bgstipple="gray50")
			else: # Doesn't work, but does increase the spacing ;-)
				body.tag_config("blank",font="Symbol")
				body.tag_config("tab",font="Symbol")
		else:
			body.tag_config("blank",background="white")
			body.tag_config("tab",background="white")
		
		# body.tag_config("normal", foreground="black")
		#@-body
		#@-node:1:C=5:<< configure tags >>

		self.count += 1
		
		lines = string.split(s,'\n')
		state = normalState ; n = 0
		for s in lines:
			n += 1 ; i = 0 ; sLen = len(s)
			# trace(`n` + ", " + `s`)
			while i < sLen:
				ch = s[i]
				if state == string3State:
					
					#@<< continue python triple string >>
					#@+node:3::<< continue python triple string >>
					#@+body
					j = string.find(s, '"""', i)
					if j == -1:
						# The entire line is part of the triple-quoted string.
						body.tag_add("string", index(n,i), index(n,"end"))
						i = sLen # skipt the rest of the line.
					else:
						# End the string
						body.tag_add("string", index(n,i), index(n,j+3))
						i = j + 3 ; state = normalState
					#@-body
					#@-node:3::<< continue python triple string >>

					continue
				elif state == docState:
					
					#@<< continue doc part >>
					#@+node:2::<< continue doc part >>
					#@+body
					if i == 0 and ch == '@':
						j = self.skip_id(s,i+1)
						word = s[i:j]
						word = string.lower(word)
					elif i == 0 and match(s,i,"<<"): # Bug fix: 2/15/02
						# Possible section definition line.
						j = string.find(s,">>=",i+2)
						if j != -1:
							state = normalState
							continue # rescan the line
					else:
						word = ""
					
					if word == "@c" or word == "@code":
						# End of the doc part.
						body.tag_remove("docPart", index(n,i), index(n,j))
						body.tag_add("leoKeyword", index(n,i), index(n,j))
						i = j ; state = normalState
					else:
						# The entire line is in the doc part.
						body.tag_add("docPart", index(n,i), index(n,sLen))
						i = sLen # skipt the rest of the line.
					#@-body
					#@-node:2::<< continue doc part >>

					continue
				elif state == nocolorState:
					
					#@<< continue nocolor state >>
					#@+node:4::<< continue nocolor state >>
					#@+body
					if i == 0 and ch == '@':
						j = self.skip_id(s,i+1)
						word = s[i:j]
						word = string.lower(word)
					else:
						word = ""
					
					if word == "@color":
						# End of the nocolor part.
						## body.tag_remove("normal", index(n,0), index(n,j))
						body.tag_add("leoKeyword", index(n,0), index(n,j))
						i = j ; state = normalState
					else:
						# The entire line is in the nocolor part.
						## body.tag_add("normal", index(n,0), index(n,sLen))
						i = sLen # skipt the rest of the line.
					#@-body
					#@-node:4::<< continue nocolor state >>

				else: assert(state == normalState)
	
				if ch == '"' or ch == "'":
					
					#@<< handle python string >>
					#@+node:5::<< handle python string >>
					#@+body
					j, state = self.skip_python_string(s,i)
					body.tag_add("string", index(n,i), index(n,j))
					i = j
					#@-body
					#@-node:5::<< handle python string >>

				elif ch == '#':
					
					#@<< handle python comment >>
					#@+node:6::<< handle python comment >>
					#@+body
					body.tag_add("comment", index(n,i), index(n,"end"))
					i = sLen
					#@-body
					#@-node:6::<< handle python comment >>

				elif ch == '<':
					
					#@<< handle possible section ref or def >>
					#@+node:8::<< handle possible section ref or def >>
					#@+body
					if s[i:i+2] == "<<":
						# See if the line contains >>
						
						j = string.find(s,">>=",i+2) ; k = 3
						if j == -1:
							j = string.find(s,">>",i+2) ; k = 2
						if j == -1:
							## body.tag_add("normal", index(n,i), index(n,i+1))
							i += 2
						else:
							searchName = body.get(index(n,i),   index(n,j+k)) # includes brackets
							# linkName   = body.get(index(n,i+2), index(n,j)) # does not include brackets
							ref = findReference(searchName,v)
							## body.tag_remove("normal", index(n,i), index(n,j+k))
							body.tag_add("nameBrackets", index(n,i), index(n,i+k))
							if ref:
								body.tag_add("link", index(n,i+2), index(n,j))
								
								#@<< set the hyperlink >>
								#@+node:1::<< set the hyperlink >>
								#@+body
								# Set the bindings to vnode callbacks.
								if self.use_hyperlinks:
									# Create the tag.
									# Create the tag name.
									tagName = "hyper" + `hyperCount`
									hyperCount += 1
									body.tag_delete(tagName)
									body.tag_add(tagName, index(n,i+2), index(n,j))
									ref.tagName = tagName
									body.tag_bind(tagName,"<Control-1>",ref.OnHyperLinkControlClick)
									body.tag_bind(tagName,"<Any-Enter>",ref.OnHyperLinkEnter)
									body.tag_bind(tagName,"<Any-Leave>",ref.OnHyperLinkLeave)
								#@-body
								#@-node:1::<< set the hyperlink >>

							elif k == 3: # a section definition
								body.tag_add("link", index(n,i+2), index(n,j))
							else:
								body.tag_add("name", index(n,i+2), index(n,j))
							body.tag_add("nameBrackets", index(n,j), index(n,j+k))
							i = j + k
					else: # a single '<'
						## body.tag_add("normal", index(n,i))
						i += 1
					#@-body
					#@-node:8::<< handle possible section ref or def >>

				elif ch == '@':
					
					#@<< handle possible @keyword >>
					#@+node:7::<< handle possible @keyword >>
					#@+body
					j = self.skip_id(s,i+1)
					word = s[i:j]
					word = string.lower(word)
					if i != 0 and word != "@others":
						word = "" # can't be a Leo keyword, even if it looks like it.
					
					# to do: the keyword should start the line.
					if word == "@" or word == "@doc":
						# at-space starts doc part
						## body.tag_remove("normal", index(n,i), index(n,j))
						body.tag_add("leoKeyword", index(n,i), index(n,j))
						# Everything on the line is in the doc part.
						body.tag_add("docPart", index(n,j), index(n,sLen))
						i = sLen ; state = docState
					elif word == "@nocolor":
						# Nothing on the line is colored.
						## body.tag_add("normal", index(n,j), index(n,sLen))
						i = sLen ; state = nocolorState
					elif word in leoKeywords:
						## body.tag_remove("normal", index(n,i), index(n,j))
						body.tag_add("keyword", index(n,i), index(n,j))
						i = j
					else:
						## body.tag_add("normal", index(n,i), index(n,j+1))
						i = j
					#@-body
					#@-node:7::<< handle possible @keyword >>

				elif ch in string.letters:
					
					#@<< handle possible python keyword >>
					#@+node:9::<< handle possible python keyword >>
					#@+body
					j = self.skip_id(s,i)
					word = s[i:j]
					if keyword.iskeyword(word):
						## body.tag_remove("normal", index(n,i), index(n,j))
						body.tag_add("keyword", index(n,i), index(n,j))
					else:
						pass # body.tag_add("normal", index(n,i), index(n,j))
					i = j
					#@-body
					#@-node:9::<< handle possible python keyword >>

				elif ch == ' ':
					
					#@<< handle blank >>
					#@+node:10::<< handle blank >>
					#@+body
					body.tag_add("blank", index(n,i)) ; i += 1

					#@-body
					#@-node:10::<< handle blank >>

				elif ch == '\t':
					
					#@<< handle tab >>
					#@+node:11::<< handle tab >>
					#@+body
					body.tag_add("tab", index(n,i)) ; i += 1

					#@-body
					#@-node:11::<< handle tab >>

				else:
					
					#@<< handle normal character >>
					#@+node:12::<< handle normal character >>
					#@+body
					# body.tag_add("normal", index(n,i))
					i += 1

					#@-body
					#@-node:12::<< handle normal character >>
	#@-body
	#@-node:8:C=4:colorizePython
	#@+node:9:C=6:colorizeAnyLanguage
	#@+body
	tags = (
		"blank", "comment", "docPart", "keyword", "leoKeyword",
		"link", "name", "nameBrackets", "string", "tab")
	
	def colorizeAnyLanguage(self,v,body,language):
	
		hyperCount = 0 # Number of hypertext tags
		self.body = body # For callbacks
		s = body.get("1.0", "end")
		sel = body.index("insert") # get the location of the insert point
		start, end = string.split(sel,'.')
		start = int(start)
		# trace(`self.count` + `sel`)
		# trace(`body.tag_names()`)
	
		if 0: # Remove all tags from the selected line.
			for tag in self.tags:
				body.tag_remove(tag, index(start,0), index(start,"end"))
		else: # Remove all tags from body.
			body.tag_delete(
				"blank", "comment", "docPart", "keyword", "leoKeyword",
				"link", "name", "nameBrackets", "string", "tab")
		
		#@<< configure tags >>
		#@+node:1::<< configure tags >>
		#@+body
		# Must use foreground, not fg
		body.tag_config("comment", foreground="red")
		body.tag_config("docPart", foreground="red")
		body.tag_config("keyword", foreground="blue")
		if self.use_hyperlinks: # underline=self.use_hyperlinks doesn't seem to work.
			body.tag_config("link", foreground="red",underline=1) # Defined section name
		else:
			body.tag_config("link", foreground="red",underline=0) # Defined section name
		body.tag_config("leoKeyword", foreground="blue")
		if 0: # Looks good, but problems when text is selected.
			body.tag_config("name", foreground="red", background="gray90") # Undefined section name
		else: # Reverse the underlining used for defined section names.
			if self.use_hyperlinks: # underline=(not self.use_hyperlinks) doesn't seem to work.
				body.tag_config("name", foreground="red", underline=0) # Undefined section name
			else:
				body.tag_config("name", foreground="red", underline=1) # Undefined section name
		body.tag_config("nameBrackets", foreground="blue")
		body.tag_config("string", foreground="gray50")
		
		if self.showInvisibles:
			if 1: # Very poor, and vaguely usable.
				body.tag_config("blank",background="black",bgstipple="gray25")
				body.tag_config("tab",background="black",bgstipple="gray50")
			else: # Doesn't work, but does increase the spacing ;-)
				body.tag_config("blank",font="Symbol")
				body.tag_config("tab",font="Symbol")
		else:
			body.tag_config("blank",background="white")
			body.tag_config("tab",background="white")
		
		# body.tag_config("normal", foreground="black")
		#@-body
		#@-node:1::<< configure tags >>

		
		#@<< configure language-specific settings >>
		#@+node:2::<< configure language-specific settings >>
		#@+body
		# Define has_string, keywords[], single_comment_start, block_comment_start, block_comment_end
		
		(single_comment_start,
			block_comment_start,
			block_comment_end) = set_delims_from_language(language)
		
		has_string = language != plain_text_language
		
		languages = ["c","cweb","html","java","pascal","perl","perlpod","python"]
		
		keywords = []
		for name in languages:
			exec("if language==%s_language: keywords=%s_keywords" % (name,name))
			
		state = choose(language==plain_text_language,nocolorState,normalState)
		#@-body
		#@-node:2::<< configure language-specific settings >>

		self.count += 1
		
		lines = string.split(s,'\n')
		n = 0
		for s in lines:
			n += 1 ; i = 0 ; sLen = len(s)
			# trace(`n` + ", " + `s`)
			while i < sLen:
				progress = i
				ch = s[i]
				if state == string3State:
					
					#@<< continue python triple string >>
					#@+node:3::Multiline State Handlers
					#@+node:2::<< continue python triple string >>
					#@+body
					delim = self.delim
					assert(delim=="'" or delim=='"')
					if delim=="'":
						j = string.find(s,"'''",i)
					else:
						j = string.find(s,'"""', i)
					
					if j == -1:
						# The entire line is part of the triple-quoted string.
						body.tag_add("string", index(n,i), index(n,"end"))
						i = sLen # skipt the rest of the line.
					else:
						# End the string
						body.tag_add("string", index(n,i), index(n,j+3))
						i = j + 3 ; state = normalState
					#@-body
					#@-node:2::<< continue python triple string >>
					#@-node:3::Multiline State Handlers

					continue
				elif state == docState:
					
					#@<< continue doc part >>
					#@+node:3::Multiline State Handlers
					#@+node:1::<< continue doc part >>
					#@+body
					if i == 0 and ch == '@':
						j = self.skip_id(s,i+1)
						word = s[i:j]
						word = string.lower(word)
					elif i == 0 and match(s,i,"<<"): # Bug fix: 2/15/02
						# Possible section definition line.
						j = string.find(s,">>=",i+2)
						if j != -1:
							state = normalState
							continue # rescan the line
					else:
						word = ""
					
					if word in ["@c","@code","@unit","@root","@color","@nocolor"]:
						# End of the doc part.
						body.tag_remove("docPart", index(n,i), index(n,j))
						body.tag_add("leoKeyword", index(n,i), index(n,j))
						i = j ; state = normalState
					else:
						# The entire line is in the doc part.
						body.tag_add("docPart", index(n,i), index(n,sLen))
						i = sLen # skipt the rest of the line.
					#@-body
					#@-node:1::<< continue doc part >>
					#@-node:3::Multiline State Handlers

					continue
				elif state == nocolorState:
					
					#@<< continue nocolor state >>
					#@+node:3::Multiline State Handlers
					#@+node:4::<< continue nocolor state >>
					#@+body
					if i == 0 and ch == '@':
						j = self.skip_id(s,i+1)
						word = s[i:j]
						word = string.lower(word)
					else:
						word = ""
					
					if word == "@color" and language != plain_text_language:
						# End of the nocolor part.
						## body.tag_remove("normal", index(n,0), index(n,j))
						body.tag_add("leoKeyword", index(n,0), index(n,j))
						i = j ; state = normalState
					else:
						## body.tag_add("normal", index(n,0), index(n,sLen))
						# The entire line is in the nocolor part.
						# Add tags for blanks and tabs to make "Show Invisibles" work.
						for ch in s[i:]:
							if ch == ' ':
								body.tag_add("blank", index(n,i))
							elif ch == '\t':
								body.tag_add("tab", index(n,i))
							i += 1
						## i = sLen # skipt the rest of the line.
					continue
					#@-body
					#@-node:4::<< continue nocolor state >>
					#@-node:3::Multiline State Handlers

				elif state == blockCommentState:
					
					#@<< continue block comment >>
					#@+node:3::Multiline State Handlers
					#@+node:3::<< continue block comment >>
					#@+body
					j = string.find(s,block_comment_end,i)
					if j == -1:
						# The entire line is part of the block comment.
						body.tag_add("comment", index(n,i), index(n,"end"))
						i = sLen # skipt the rest of the line.
					else:
						# End the block comment.
						k = len(block_comment_end)
						body.tag_add("comment", index(n,i), index(n,j+k))
						i = j + k ; state = normalState
					#@-body
					#@-node:3::<< continue block comment >>
					#@-node:3::Multiline State Handlers

				else: assert(state == normalState)
	
				if has_string and ch == '"' or ch == "'":
					
					#@<< handle string >>
					#@+node:4::<< handle string >>
					#@+body
					if language == python_language:
						j, state = self.skip_python_string(s,i)
						body.tag_add("string", index(n,i), index(n,j))
						i = j
					else:
						j = self.skip_string(s,i)
						body.tag_add("string", index(n,i), index(n,j))
						i = j
					#@-body
					#@-node:4::<< handle string >>

				elif single_comment_start and match(s,i,single_comment_start):
					
					#@<< handle single-line comment >>
					#@+node:6::<< handle single-line comment >>
					#@+body
					body.tag_add("comment", index(n,i), index(n,"end"))
					i = sLen
					#@-body
					#@-node:6::<< handle single-line comment >>

				elif block_comment_start and match(s,i,block_comment_start):
					
					#@<< start block comment >>
					#@+node:5::<< start block comment >>
					#@+body
					k = len(block_comment_start)
					body.tag_add("comment", index(n,i), index(n,i+k))
					i += k ; state = blockCommentState
					#@-body
					#@-node:5::<< start block comment >>

				elif ch == '<':
					
					#@<< handle possible section ref or def >>
					#@+node:8::<< handle possible section ref or def >>
					#@+body
					if s[i:i+2] == "<<":
						# See if the line contains >>
						
						j = string.find(s,">>=",i+2) ; k = 3
						if j == -1:
							j = string.find(s,">>",i+2) ; k = 2
						if j == -1:
							## body.tag_add("normal", index(n,i), index(n,i+1))
							i += 2
						else:
							searchName = body.get(index(n,i),   index(n,j+k)) # includes brackets
							# linkName   = body.get(index(n,i+2), index(n,j)) # does not include brackets
							ref = findReference(searchName,v)
							## body.tag_remove("normal", index(n,i), index(n,j+2))
							body.tag_add("nameBrackets", index(n,i), index(n,i+2))
							if ref:
								body.tag_add("link", index(n,i+2), index(n,j))
								
								#@<< set the hyperlink >>
								#@+node:1::<< set the hyperlink >>
								#@+body
								# Set the bindings to vnode callbacks.
								if self.use_hyperlinks:
									# Create the tag.
									# Create the tag name.
									tagName = "hyper" + `hyperCount`
									hyperCount += 1
									body.tag_delete(tagName)
									body.tag_add(tagName, index(n,i+2), index(n,j))
									ref.tagName = tagName
									body.tag_bind(tagName,"<Control-1>",ref.OnHyperLinkControlClick)
									body.tag_bind(tagName,"<Any-Enter>",ref.OnHyperLinkEnter)
									body.tag_bind(tagName,"<Any-Leave>",ref.OnHyperLinkLeave)
								#@-body
								#@-node:1::<< set the hyperlink >>

							elif k == 3: # a section definition
								body.tag_add("link", index(n,i+2), index(n,j))
							else:
								body.tag_add("name", index(n,i+2), index(n,j))
							body.tag_add("nameBrackets", index(n,j), index(n,j+k))
							i = j + k
					else: # a single '<'
						## body.tag_add("normal", index(n,i))
						i += 1
					#@-body
					#@-node:8::<< handle possible section ref or def >>

				elif ch == '@':
					
					#@<< handle possible @keyword >>
					#@+node:7::<< handle possible @keyword >>
					#@+body
					j = self.skip_id(s,i+1)
					word = s[i:j]
					word = string.lower(word)
					if i != 0 and word != "@others":
						word = "" # can't be a Leo keyword, even if it looks like it.
					
					# to do: the keyword should start the line.
					if word == "@" or word == "@doc":
						# at-space starts doc part
						## body.tag_remove("normal", index(n,i), index(n,j))
						body.tag_add("leoKeyword", index(n,i), index(n,j))
						# Everything on the line is in the doc part.
						body.tag_add("docPart", index(n,j), index(n,sLen))
						i = sLen ; state = docState
					elif word == "@nocolor":
						# Nothing on the line is colored.
						## body.tag_add("normal", index(n,j), index(n,sLen))
						body.tag_add("keyword", index(n,i), index(n,j))
						i = j ; state = nocolorState
					elif word in leoKeywords:
						## body.tag_remove("normal", index(n,i), index(n,j))
						body.tag_add("keyword", index(n,i), index(n,j))
						i = j
					else:
						## body.tag_add("normal", index(n,i), index(n,j+1))
						i = j
					#@-body
					#@-node:7::<< handle possible @keyword >>

				elif ch in string.letters:
					
					#@<< handle possible keyword >>
					#@+node:9::<< handle possible  keyword >>
					#@+body
					j = self.skip_id(s,i)
					word = s[i:j]
					if word in keywords:
						## body.tag_remove("normal", index(n,i), index(n,j))
						body.tag_add("keyword", index(n,i), index(n,j))
					else:
						pass # body.tag_add("normal", index(n,i), index(n,j))
					i = j
					#@-body
					#@-node:9::<< handle possible  keyword >>

				elif ch == ' ':
					
					#@<< handle blank >>
					#@+node:10::<< handle blank >>
					#@+body
					body.tag_add("blank", index(n,i)) ; i += 1
					#@-body
					#@-node:10::<< handle blank >>

				elif ch == '\t':
					
					#@<< handle tab >>
					#@+node:11::<< handle tab >>
					#@+body
					body.tag_add("tab", index(n,i)) ; i += 1
					#@-body
					#@-node:11::<< handle tab >>

				else:
					
					#@<< handle normal character >>
					#@+node:12::<< handle normal character >>
					#@+body
					# body.tag_add("normal", index(n,i))
					i += 1

					#@-body
					#@-node:12::<< handle normal character >>

				assert(progress < i)
	#@-body
	#@+node:3::Multiline State Handlers
	#@-node:3::Multiline State Handlers
	#@-node:9:C=6:colorizeAnyLanguage
	#@+node:10:C=7:scanColorDirectives
	#@+body
	#@+at
	#  This code scans the node v and all of v's ancestors looking for @color and @nocolor directives.

	#@-at
	#@@c
	
	def scanColorDirectives(self,v):
	
		c = self.commands
		val = c.target_language
		while v:
			s = v.t.bodyString
			bits, dict = is_special_bits(s)
			
			#@<< Test for @comment or @language >>
			#@+node:1::<< Test for @comment or @language >>
			#@+body
			if btest(comment_bits,bits):
				# @comment effectively disables syntax coloring.
				val = plain_text_language
				break
			
			elif btest(language_bits,bits):
				issue_error_flag = false
				i = dict["language"]
				val, delim1, delim2, delim3 = set_language(s,i,issue_error_flag,c.target_language)
				break
			#@-body
			#@-node:1::<< Test for @comment or @language >>

			v = v.parent()
		# trace(`val`)
		return val
	#@-body
	#@-node:10:C=7:scanColorDirectives
	#@+node:11::color.schedule
	#@+body
	def schedule(self,v,body):
	
		if self.enabled:
			body.after_idle(self.idle_colorize,v,body)
			
	def idle_colorize(self,v,body):
	
		# trace(`v` + ", " + `body`)
		if v and body and self.enabled:
			self.colorize(v,body)
	#@-body
	#@-node:11::color.schedule
	#@+node:12::updateSyntaxColorer
	#@+body
	# Returns the language to be used for syntax coloring of v.
	
	def updateSyntaxColorer (self,v):
	
		if self.useSyntaxColoring(v):
			return self.scanColorDirectives(v)
		else:
			return plain_text_language
	#@-body
	#@-node:12::updateSyntaxColorer
	#@+node:13::useSyntaxColoring
	#@+body
	# Return true if v is unambiguously under the control of @color or @nocolor.
	
	def useSyntaxColoring (self,v):
	
		first = v ; val = true
		while v:
			s = v.t.bodyString
			bits, dict = is_special_bits(s)
			no_color = ( bits & nocolor_bits ) != 0
			color = ( bits & color_bits ) != 0
			# trace(`bits` + ", " + `v`)
			# A color anywhere in the target enables coloring.
			if color and v == first:
				val = true ; break
			# Otherwise, the specification must be unambiguous.
			elif no_color and not color:
				val = false ; break
			elif color and not no_color:
				val = true ; break
			else:
				v = v.parent()
		trace("-useSyntaxColoring",`val`)
		return val
	#@-body
	#@-node:13::useSyntaxColoring
	#@+node:14::Utils
	#@+body
	#@+at
	#  These methods are like the corresponding functions in leoUtils.py except they issue no error messages.

	#@-at
	#@-body
	#@+node:1::skip_id
	#@+body
	def skip_id(self,s,i):
	
		n = len(s)
		while i < n:
			ch = s[i]
			if ch in string.letters or ch in string.digits or ch == '_':
				i += 1
			else: break
		return i

	#@-body
	#@-node:1::skip_id
	#@+node:2::skip_python_string
	#@+body
	def skip_python_string(self,s,i):
	
		delim = s[i:i+3]
		if delim == "'''" or delim == '"""':
			k = string.find(s,delim,i+3)
			if k == -1:
				return len(s), string3State
			else:
				return k+3, normalState
		else:
			return self.skip_string(s,i), normalState
	#@-body
	#@-node:2::skip_python_string
	#@+node:3::skip_string
	#@+body
	def skip_string(self,s,i):
	
		# Remember delim for colorizeAnyLanguage.
		self.delim = delim = s[i] ; i += 1
		assert(delim == '"' or delim == '\'')
		n = len(s)
		while i < n and s[i] != delim:
			if s[i] == '\\' : i += 2
			else: i += 1
	
		if i >= n:
			return n
		elif s[i] == delim:
			i += 1
		return i
	#@-body
	#@-node:3::skip_string
	#@-node:14::Utils
	#@-others

#@-body
#@-node:0::@file leoColor.py
#@-leo
