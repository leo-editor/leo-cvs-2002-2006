#@+leo

#@+node:0::@file leoColor.py
#@+body
#@@language python

# Syntax coloring routines for Leo.py

from leoGlobals import *
from leoUtils import *
import string, Tkinter, tkColorChooser, traceback


#@<< define colorizer constants >>
#@+node:1::<< define colorizer constants >>
#@+body
# We only define states that can continue across lines.
normalState, docState, nocolorState, string3State, blockCommentState = 1,2,3,4,5

# These defaults are sure to exist.
default_colors_dict = {
	# tag name     :(     option name,           default color),
	"comment"      :("comment_color",               "red"),
	"cwebName"     :("cweb_section_name_color",     "red"),
	"pp"           :("directive_color",             "blue"),
	"docPart"      :("doc_part_color",              "red"),
	"keyword"      :("keyword_color",               "blue"),
	"leoKeyword"   :("leo_keyword_color",           "blue"),
	"link"         :("section_name_color",          "red"),
	"nameBrackets" :("section_name_brackets_color", "blue"),
	"string"       :("string_color",                "#00aa00"), # Used by IDLE.
	"name"         :("undefined_section_name_color","red") }

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
	
cweb_keywords = c_keywords

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
	
	#@<< class colorizer methods >>
	#@+node:5::<< class colorizer methods >>
	#@+body
	#@+others
	#@+node:1:C=2:color.__init__
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
	#@-node:1:C=2:color.__init__
	#@+node:2::color.callbacks...
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
	#@-node:2::color.callbacks...
	#@+node:3:C=3:colorize
	#@+body
	def colorize(self,v,body):
	
		if self.enabled:
			flag,language = self.updateSyntaxColorer(v)
			self.colorizeAnyLanguage(v,body,language,flag)
	#@-body
	#@-node:3:C=3:colorize
	#@+node:4:C=4:colorizeAnyLanguage
	#@+body
	tags = (
		"blank", "comment", "cwebName", "docPart", "keyword", "leoKeyword",
		"link", "name", "nameBrackets", "pp", "string", "tab")
	
	def colorizeAnyLanguage(self,v,body,language,flag):
		
		#trace(`language`)
	
		hyperCount = 0 # Number of hypertext tags
		self.body = body # For callbacks
		s = body.get("1.0", "end")
		sel = body.index("insert") # get the location of the insert point
		start, end = string.split(sel,'.')
		start = int(start)
		# trace(`self.count` + `v`)
		# trace(`body.tag_names()`)
	
		if 0: # Remove all tags from the selected line.
			for tag in self.tags:
				body.tag_remove(tag, index(start,0), index(start,"end"))
		else: # Remove all tags from body.
			body.tag_delete(
				"blank", "comment", "cwebName", "docPart", "keyword", "leoKeyword",
				"link", "name", "nameBrackets", "pp", "string", "tab")
		
		#@<< configure tags >>
		#@+node:1:C=5:<< configure tags >>
		#@+body
		config = app().config
		assert(config)
		
		for name in default_colors_dict:
			option_name,default_color = default_colors_dict[name]
			option_color = config.getColorsPref(option_name)
			color = choose(option_color,option_color,default_color)
			# Must use foreground, not fg.
			try:
				body.tag_config(name, foreground=color)
			except: # Recover after a user error.
				body.tag_config(name, foreground=default_color)
		
		underline_undefined = config.getBoolColorsPref("underline_undefined_section_names")
		use_hyperlinks      = config.getBoolColorsPref("use_hyperlinks")
		self.use_hyperlinks = use_hyperlinks
		
		# underline=var doesn't seem to work.
		if use_hyperlinks: 
			body.tag_config("link",underline=1) # defined
			body.tag_config("name",underline=0) # undefined
		else:
			body.tag_config("link",underline=0)
			if underline_undefined:
				body.tag_config("name",underline=1)
			else:
				body.tag_config("name",underline=0)
		
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
		#@-body
		#@-node:1:C=5:<< configure tags >>

		
		#@<< configure language-specific settings >>
		#@+node:2::<< configure language-specific settings >>
		#@+body
		# Define has_string, keywords, single_comment_start, block_comment_start, block_comment_end
		
		(single_comment_start,
			block_comment_start,
			block_comment_end) = set_delims_from_language(language)
		
		has_string = language != plain_text_language
		
		languages = ["c","cweb","html","java","pascal","perl","perlpod","python"]
		
		keywords = []
		if language==cweb_language:
			for i in c_keywords:
				keywords.append(i)
			for i in cweb_keywords:
				keywords.append(i)
		else:
			for name in languages:
				exec("if language==%s_language: keywords=%s_keywords" % (name,name))
		
		if 1: # 7/8/02: Color plain text unless we are under the control of @nocolor.
			state = choose(flag,normalState,nocolorState)
		else: # Stupid: no coloring at all in plain text.
			state = choose(language==plain_text_language,nocolorState,normalState)
		
		lb = choose(language==cweb_language,"@<","<<")
		rb = choose(language==cweb_language,"@>",">>")
		#@-body
		#@-node:2::<< configure language-specific settings >>

		self.count += 1
		
		lines = string.split(s,'\n')
		n = 0 # The line number for indices, as in n.i
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
					if delim=="'''":
						j = string.find(s,"'''",i)
					elif delim=='"""':
						j = string.find(s,'"""', i)
					else:
						state=normalState ; self.delim = None ; continue
					
					if j == -1:
						# The entire line is part of the triple-quoted string.
						body.tag_add("string", index(n,i), index(n,"end"))
						i = sLen # skipt the rest of the line.
					else:
						# End the string
						body.tag_add("string", index(n,i), index(n,j+3))
						i = j + 3 ; state = normalState ; self.delim = None
					#@-body
					#@-node:2::<< continue python triple string >>
					#@-node:3::Multiline State Handlers

					continue
				elif state == docState:
					
					#@<< continue doc part >>
					#@+node:3::Multiline State Handlers
					#@+node:1::<< continue doc part >>
					#@+body
					if language == cweb_language:
						
						#@<< handle cweb doc part >>
						#@+node:1::<< handle cweb doc part >>
						#@+body
						word = self.getCwebWord(s,i)
						if word and len(word) > 0:
							j = i + len(word)
							if word in ("@<","@(","@c","@d","@f","@p"):
								state = normalState # end the doc part and rescan
							else:
								# The control code does not end the doc part.
								body.tag_add("keyword", index(n,i), index(n,j))
								i = j
								if word in ("@^","@.","@:","@="): # Ended by "@>"
									j = string.find(s,"@>",i)
									if j > -1:
										body.tag_add("cwebName", index(n,i), index(n,j))
										body.tag_add("nameBrackets", index(n,j), index(n,j+2))
										i = j + 2
						else:
							# Everthing up to the next "@" is in the doc part.
							j = string.find(s,"@",i+1)
							if j == -1: j = len(s)
							body.tag_add("docPart", index(n,i), index(n,j))
							i = j
						#@-body
						#@-node:1::<< handle cweb doc part >>

					else:
						
						#@<< handle noweb doc part >>
						#@+node:2::<< handle noweb doc part >>
						#@+body
						if i == 0 and match(s,i,lb):
							# Possible section definition line.
							state = normalState # rescan the line.
							continue
						if i == 0 and ch == '@':
							j = self.skip_id(s,i+1)
							word = s[i:j]
							word = string.lower(word)
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
						#@-node:2::<< handle noweb doc part >>
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
						body.tag_add("leoKeyword", index(n,0), index(n,j))
						i = j ; state = normalState
					else:
						# The entire line is in the nocolor part.
						# Add tags for blanks and tabs to make "Show Invisibles" work.
						for ch in s[i:]:
							if ch == ' ':
								body.tag_add("blank", index(n,i))
							elif ch == '\t':
								body.tag_add("tab", index(n,i))
							i += 1
					#@-body
					#@-node:4::<< continue nocolor state >>
					#@-node:3::Multiline State Handlers

					continue
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

					continue
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

				elif ch == '#' and language in [c_language,cweb_language]:
					
					#@<< handle C preprocessor line >>
					#@+node:7::<< handle C preprocessor line >>
					#@+body
					body.tag_add("pp", index(n,i), index(n,"end"))
					i = sLen
					#@-body
					#@-node:7::<< handle C preprocessor line >>

				elif match(s,i,lb) or (language==cweb_language and match(s,i,"@(")):
					
					#@<< handle possible section ref or def >>
					#@+node:8::<< handle possible section ref or def >>
					#@+body
					body.tag_add("nameBrackets", index(n,i), index(n,i+2))
					
					# See if the line contains the rb
					j = string.find(s,rb+"=",i+2) ; k = 3
					if j == -1:
						j = string.find(s,rb,i+2) ; k = 2
					if j == -1:
						i += 2
					else:
						if language != cweb_language:
							searchName = body.get(index(n,i),   index(n,j+k)) # includes brackets
							ref = findReference(searchName,v)
						
						if language == cweb_language:
							body.tag_add("cwebName", index(n,i+2), index(n,j))
						elif ref:
							body.tag_add("link", index(n,i+2), index(n,j))
							if self.use_hyperlinks:
								
								#@<< set the hyperlink >>
								#@+node:1::<< set the hyperlink >>
								#@+body
								# Set the bindings to vnode callbacks.
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
					#@-body
					#@-node:8::<< handle possible section ref or def >>

				elif ch == '@':
					
					#@<< handle possible @keyword >>
					#@+node:9::<< handle possible @keyword >>
					#@+body
					word = None
					if language == cweb_language:
						
						#@<< Handle all cweb control codes >>
						#@+node:1::<< Handle all cweb control codes >>
						#@+body
						word = self.getCwebWord(s,i)
						if word:
							# Color and skip the word.
							j = i + len(word)
							body.tag_add("keyword",index(n,i),index(n,j))
							i = j
						
							if word in ("@ ","@\t","@\n","@*","@**"):
								state = docState
								continue ;
						
							if word in ("@^","@.","@:","@="): # Ended by "@>"
								j = string.find(s,"@>",i)
								if j > -1:
									body.tag_add("cwebName", index(n,i), index(n,j))
									body.tag_add("nameBrackets", index(n,j), index(n,j+2))
									i = j + 2

						#@-body
						#@-node:1::<< Handle all cweb control codes >>

					if not word:
						
						#@<< Handle non-cweb @keywords >>
						#@+node:2::<< Handle non-cweb @keywords >>
						#@+body
						j = self.skip_id(s,i+1)
						word = s[i:j]
						word = string.lower(word)
						if i != 0 and word != "@others":
							word = "" # can't be a Leo keyword, even if it looks like it.
						
						# 7/8/02: don't color doc parts in plain text.
						if language != plain_text_language and (word == "@" or word == "@doc"):
							# at-space starts doc part
							body.tag_add("leoKeyword", index(n,i), index(n,j))
							# Everything on the line is in the doc part.
							body.tag_add("docPart", index(n,j), index(n,sLen))
							i = sLen ; state = docState
						elif word == "@nocolor":
							# Nothing on the line is colored.
							body.tag_add("leoKeyword", index(n,i), index(n,j))
							i = j ; state = nocolorState
						elif word in leoKeywords:
							body.tag_add("leoKeyword", index(n,i), index(n,j))
							i = j
						else:
							i = j
						#@-body
						#@-node:2::<< Handle non-cweb @keywords >>
					#@-body
					#@-node:9::<< handle possible @keyword >>

				elif ch in string.letters:
					
					#@<< handle possible keyword >>
					#@+node:10::<< handle possible  keyword >>
					#@+body
					j = self.skip_id(s,i)
					word = s[i:j]
					if word in keywords:
						body.tag_add("keyword", index(n,i), index(n,j))
					i = j
					#@-body
					#@-node:10::<< handle possible  keyword >>

				elif ch == ' ':
					
					#@<< handle blank >>
					#@+node:11::<< handle blank >>
					#@+body
					body.tag_add("blank", index(n,i)) ; i += 1
					#@-body
					#@-node:11::<< handle blank >>

				elif ch == '\t':
					
					#@<< handle tab >>
					#@+node:12::<< handle tab >>
					#@+body
					body.tag_add("tab", index(n,i)) ; i += 1
					#@-body
					#@-node:12::<< handle tab >>

				else:
					
					#@<< handle normal character >>
					#@+node:13::<< handle normal character >>
					#@+body
					# body.tag_add("normal", index(n,i))
					i += 1

					#@-body
					#@-node:13::<< handle normal character >>

				assert(progress < i)
	#@-body
	#@+node:3::Multiline State Handlers
	#@-node:3::Multiline State Handlers
	#@-node:4:C=4:colorizeAnyLanguage
	#@+node:5:C=6:scanColorDirectives
	#@+body
	#@+at
	#  This code scans the node v and all of v's ancestors looking for @color and @nocolor directives.

	#@-at
	#@@c
	
	def scanColorDirectives(self,v):
	
		c = self.commands
		language = c.target_language
		while v:
			s = v.t.bodyString
			bits, dict = is_special_bits(s)
			
			#@<< Test for @comment or @language >>
			#@+node:1::<< Test for @comment or @language >>
			#@+body
			#@+at
			#  Disabling syntax coloring when @comment is seen is stupid and confusing.  If the user want's plain text, then an 
			# @language plain should work.  Moreover, why not recognize directives even in plain text?  If the user _really_ want 
			# no syntax coloring, an @nocolor in a parent node will work fine.

			#@-at
			#@@c
			
			if btest(comment_bits,bits):
				# @comment effectively disables syntax coloring.
				if 0: # 7/8/02: This is stupid and confusing.
					language = plain_text_language
				break
			
			elif btest(language_bits,bits):
				issue_error_flag = false
				i = dict["language"]
				language, delim1, delim2, delim3 = set_language(s,i,issue_error_flag,c.target_language)
				break
			#@-body
			#@-node:1::<< Test for @comment or @language >>

			v = v.parent()
		# trace(`language`)
		return language
	#@-body
	#@-node:5:C=6:scanColorDirectives
	#@+node:6::color.schedule
	#@+body
	def schedule(self,v,body):
	
		if self.enabled:
			body.after_idle(self.idle_colorize,v,body)
			
	def idle_colorize(self,v,body):
	
		# trace(`v` + ", " + `body`)
		if v and body and self.enabled:
			self.colorize(v,body)
	#@-body
	#@-node:6::color.schedule
	#@+node:7::getCwebWord
	#@+body
	def getCwebWord (self,s,i):
		
		if not match(s,i,"@"):
			return None
		
		ch1 = ch2 = ch3 = word = None
		if i + 1 < len(s): ch1 = s[i+1]
		if i + 2 < len(s): ch2 = s[i+2]
		if i + 3 < len(s): ch3 = s[i+3]
	
		if match(s,i,"@**"):
			word = "@**"
		elif not ch1:
			word = "@"
		elif not ch2:
			word = s[i:i+2]
		elif (
			(ch1 in string.letters and not ch2 in string.letters) or # single-letter control code
			ch1 not in string.letters # non-letter control code
		):
			word = s[i:i+2]
			
		# if word: trace(`word`)
			
		return word
	#@-body
	#@-node:7::getCwebWord
	#@+node:8:C=7:updateSyntaxColorer
	#@+body
	# Returns (flag,language)
	# flag is true unless an unambiguous @nocolor is seen.
	
	def updateSyntaxColorer (self,v):
		
		# 7/8/02: return a tuple.
		flag = self.useSyntaxColoring(v)
		language = self.scanColorDirectives(v)
		return flag,language

	#@-body
	#@-node:8:C=7:updateSyntaxColorer
	#@+node:9::useSyntaxColoring
	#@+body
	# Return true if v unless v is unambiguously under the control of @nocolor.
	
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
			# Otherwise, the @nocolor specification must be unambiguous.
			elif no_color and not color:
				val = false ; break
			elif color and not no_color:
				val = true ; break
			else:
				v = v.parent()
		# trace("useSyntaxColoring",`val`)
		return val
	#@-body
	#@-node:9::useSyntaxColoring
	#@+node:10::Utils
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
	
		self.delim = delim = s[i:i+3]
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
	#@-node:10::Utils
	#@-others
	
	#@-body
	#@-node:5::<< class colorizer methods >>

	

#@<< define color panel data >>
#@+node:4::<< define color panel data >>
#@+body
colorPanelData = (
	#Dialog name,                option name,         default color),
	("Brackets",          "section_name_brackets_color", "blue"),
	("Comments",          "comment_color",               "red"),
	("CWEB section names","cweb_section_name_color",     "red"),
	("Directives",        "directive_color",             "blue"),
	("Doc parts",         "doc_part_color",              "red"),
	("Keywords" ,         "keyword_color",               "blue"),
	("Leo Keywords",      "leo_keyword_color",           "blue"),
	("Section Names",     "section_name_color",          "red"),
	("Strings",           "string_color",   "#00aa00"), # Used by IDLE.
	("Undefined Names",   "undefined_section_name_color","red") )

colorNamesList = (
	"gray60", "gray70", "gray80", "gray85", "gray90", "gray95",
	"snow1", "snow2", "snow3", "snow4", "seashell1", "seashell2",
	"seashell3", "seashell4", "AntiqueWhite1", "AntiqueWhite2", "AntiqueWhite3",
	"AntiqueWhite4", "bisque1", "bisque2", "bisque3", "bisque4", "PeachPuff1",
	"PeachPuff2", "PeachPuff3", "PeachPuff4", "NavajoWhite1", "NavajoWhite2",
	"NavajoWhite3", "NavajoWhite4", "LemonChiffon1", "LemonChiffon2",
	"LemonChiffon3", "LemonChiffon4", "cornsilk1", "cornsilk2", "cornsilk3",
	"cornsilk4", "ivory1", "ivory2", "ivory3", "ivory4", "honeydew1", "honeydew2",
	"honeydew3", "honeydew4", "LavenderBlush1", "LavenderBlush2",
	"LavenderBlush3", "LavenderBlush4", "MistyRose1", "MistyRose2",
	"MistyRose3", "MistyRose4", "azure1", "azure2", "azure3", "azure4",
	"SlateBlue1", "SlateBlue2", "SlateBlue3", "SlateBlue4", "RoyalBlue1",
	"RoyalBlue2", "RoyalBlue3", "RoyalBlue4", "blue1", "blue2", "blue3", "blue4",
	"DodgerBlue1", "DodgerBlue2", "DodgerBlue3", "DodgerBlue4", "SteelBlue1",
	"SteelBlue2", "SteelBlue3", "SteelBlue4", "DeepSkyBlue1", "DeepSkyBlue2",
	"DeepSkyBlue3", "DeepSkyBlue4", "SkyBlue1", "SkyBlue2", "SkyBlue3",
	"SkyBlue4", "LightSkyBlue1", "LightSkyBlue2", "LightSkyBlue3",
	"LightSkyBlue4", "SlateGray1", "SlateGray2", "SlateGray3", "SlateGray4",
	"LightSteelBlue1", "LightSteelBlue2", "LightSteelBlue3",
	"LightSteelBlue4", "LightBlue1", "LightBlue2", "LightBlue3",
	"LightBlue4", "LightCyan1", "LightCyan2", "LightCyan3", "LightCyan4",
	"PaleTurquoise1", "PaleTurquoise2", "PaleTurquoise3", "PaleTurquoise4",
	"CadetBlue1", "CadetBlue2", "CadetBlue3", "CadetBlue4", "turquoise1",
	"turquoise2", "turquoise3", "turquoise4", "cyan1", "cyan2", "cyan3", "cyan4",
	"DarkSlateGray1", "DarkSlateGray2", "DarkSlateGray3",
	"DarkSlateGray4", "aquamarine1", "aquamarine2", "aquamarine3",
	"aquamarine4", "DarkSeaGreen1", "DarkSeaGreen2", "DarkSeaGreen3",
	"DarkSeaGreen4", "SeaGreen1", "SeaGreen2", "SeaGreen3", "SeaGreen4",
	"PaleGreen1", "PaleGreen2", "PaleGreen3", "PaleGreen4", "SpringGreen1",
	"SpringGreen2", "SpringGreen3", "SpringGreen4", "green1", "green2",
	"green3", "green4", "chartreuse1", "chartreuse2", "chartreuse3",
	"chartreuse4", "OliveDrab1", "OliveDrab2", "OliveDrab3", "OliveDrab4",
	"DarkOliveGreen1", "DarkOliveGreen2", "DarkOliveGreen3",
	"DarkOliveGreen4", "khaki1", "khaki2", "khaki3", "khaki4",
	"LightGoldenrod1", "LightGoldenrod2", "LightGoldenrod3",
	"LightGoldenrod4", "LightYellow1", "LightYellow2", "LightYellow3",
	"LightYellow4", "yellow1", "yellow2", "yellow3", "yellow4", "gold1", "gold2",
	"gold3", "gold4", "goldenrod1", "goldenrod2", "goldenrod3", "goldenrod4",
	"DarkGoldenrod1", "DarkGoldenrod2", "DarkGoldenrod3", "DarkGoldenrod4",
	"RosyBrown1", "RosyBrown2", "RosyBrown3", "RosyBrown4", "IndianRed1",
	"IndianRed2", "IndianRed3", "IndianRed4", "sienna1", "sienna2", "sienna3",
	"sienna4", "burlywood1", "burlywood2", "burlywood3", "burlywood4", "wheat1",
	"wheat2", "wheat3", "wheat4", "tan1", "tan2", "tan3", "tan4", "chocolate1",
	"chocolate2", "chocolate3", "chocolate4", "firebrick1", "firebrick2",
	"firebrick3", "firebrick4", "brown1", "brown2", "brown3", "brown4", "salmon1",
	"salmon2", "salmon3", "salmon4", "LightSalmon1", "LightSalmon2",
	"LightSalmon3", "LightSalmon4", "orange1", "orange2", "orange3", "orange4",
	"DarkOrange1", "DarkOrange2", "DarkOrange3", "DarkOrange4", "coral1",
	"coral2", "coral3", "coral4", "tomato1", "tomato2", "tomato3", "tomato4",
	"OrangeRed1", "OrangeRed2", "OrangeRed3", "OrangeRed4", "red1", "red2", "red3",
	"red4", "DeepPink1", "DeepPink2", "DeepPink3", "DeepPink4", "HotPink1",
	"HotPink2", "HotPink3", "HotPink4", "pink1", "pink2", "pink3", "pink4",
	"LightPink1", "LightPink2", "LightPink3", "LightPink4", "PaleVioletRed1",
	"PaleVioletRed2", "PaleVioletRed3", "PaleVioletRed4", "maroon1",
	"maroon2", "maroon3", "maroon4", "VioletRed1", "VioletRed2", "VioletRed3",
	"VioletRed4", "magenta1", "magenta2", "magenta3", "magenta4", "orchid1",
	"orchid2", "orchid3", "orchid4", "plum1", "plum2", "plum3", "plum4",
	"MediumOrchid1", "MediumOrchid2", "MediumOrchid3", "MediumOrchid4",
	"DarkOrchid1", "DarkOrchid2", "DarkOrchid3", "DarkOrchid4", "purple1",
	"purple2", "purple3", "purple4", "MediumPurple1", "MediumPurple2",
	"MediumPurple3", "MediumPurple4", "thistle1", "thistle2", "thistle3",
	"thistle4" )

#@-body
#@-node:4::<< define color panel data >>

	
class leoColorPanel:
	
	#@<< class leoColorPanel methods >>
	#@+node:6:C=8:<< class leoColorPanel methods >>
	#@+body
	#@+others
	#@+node:1::colorPanel.__init__
	#@+body
	def __init__ (self,c):
		
		self.commands = c
		self.frame = c.frame
		# Set by run.
		self.top = None
		# Options provisionally set by callback.
		self.changed_options = []
		# For communication with callback.
		self.buttons = {}
		self.option_names = {}
	#@-body
	#@-node:1::colorPanel.__init__
	#@+node:2::run
	#@+body
	def run (self):
		
		c = self.commands ; Tk = Tkinter
		config = app().config
		
		self.top = top = Tk.Toplevel(app().root)
		top.title("Syntax colors for " + shortFileName(c.frame.title))
		top.protocol("WM_DELETE_WINDOW", self.onOk)
	
		
		#@<< create color panel >>
		#@+node:1::<< create color panel >>
		#@+body
		outer = Tk.Frame(top,bd=2,relief="groove")
		outer.pack(anchor="n",pady=2,ipady=1,expand=1,fill="x")
		
		# Create all the rows.
		for name,option_name,default_color in colorPanelData:
			# Get the color.
			option_color = config.getColorsPref(option_name)
			color = choose(option_color,option_color,default_color)
			# Create the row.
			f = Tk.Frame(outer,bd=2)
			f.pack()
			
			lab=Tk.Label(f,text=name,width=17,anchor="e")
		
			b1 = Tk.Button(f,text="",state="disabled",bg=color,width=4)
			self.buttons[name]=b1 # For callback.
			self.option_names[name]=option_name # For callback.
			
			b2 = Tk.Button(f,width=10,text=option_color)
			
			callback = lambda name=name,color=color:self.showColorPicker(name,color)
			b3 = Tk.Button(f,text="Color Picker...",command=callback)
		
			callback = lambda name=name,color=color:self.showColorName(name,color)
			b4 = Tk.Button(f,text="Color Name...",command=callback)
		
			lab.pack(side="left",padx=3)
			b1.pack (side="left",padx=3)
			b2.pack (side="left",padx=3)
			b3.pack (side="left",padx=3)
			b4.pack (side="left",padx=3)
			
		# Create the Ok, Cancel & Revert buttons
		f = Tk.Frame(outer,bd=2)
		f.pack()
		b = Tk.Button(f,width=6,text="OK",command=self.onOk)
		b.pack(side="left",padx=4)
		b = Tk.Button(f,width=6,text="Cancel",command=self.onCancel)
		b.pack(side="left",padx=4,expand=1,fill="x")
		b = Tk.Button(f,width=6,text="Revert",command=self.onRevert)
		b.pack(side="right",padx=4)
		#@-body
		#@-node:1::<< create color panel >>

		center_dialog(top) # Do this _after_ building the dialog!
		top.resizable(0,0)
		
		# We are associated with a commander, so
		# There is no need to make this a modal dialog.
		if 0:
			top.grab_set() # Make the dialog a modal dialog.
			top.focus_force() # Get all keystrokes.
	#@-body
	#@-node:2::run
	#@+node:3::showColorPicker
	#@+body
	def showColorPicker (self,name,color):
		
		rgb,val = tkColorChooser.askcolor(color=color)
		self.update(name,color)
	#@-body
	#@-node:3::showColorPicker
	#@+node:4::showColorName
	#@+body
	def showColorName (self,name,color):
		
		np = leoColorNamePanel(self,name,color)
		np.run(name,color)
	#@-body
	#@-node:4::showColorName
	#@+node:5:C=9:colorPanel.onOk, onCancel, onRevert
	#@+body
	def onOk (self):
		if 1: # Hide the window, preserving its position.
			self.top.withdraw()
		else: # works.
			self.commands.frame.colorPanel = None
			self.top.destroy()
		
	def onCancel (self):
		self.onRevert()
		if 1: # Hide the window, preserving its position.
			self.top.withdraw()
		else: # works.
			self.commands.frame.colorPanel = None
			self.top.destroy()
		
	def onRevert (self):
		for option_name,old_val in self.changed_options:
			app().config.setColorsPref(option_name,old_val)
		self.changed_options = []
		self.commands.recolor()
	#@-body
	#@-node:5:C=9:colorPanel.onOk, onCancel, onRevert
	#@+node:6::update
	#@+body
	def update (self,name,val):
		
		config = app().config
		es(`val`)
		
		# Put the new color in the button.
		b = self.buttons[name]
		b.configure(bg=val)
		option_name = self.option_names[name]
		
		# Save the old value for revert.
		old = config.getColorsPref(option_name)
		self.changed_options.append((option_name,old))
		
		# Set the new value and recolor.
		config.setColorsPref(option_name,val)
		self.commands.recolor()
	#@-body
	#@-node:6::update
	#@-others
	
	#@-body
	#@-node:6:C=8:<< class leoColorPanel methods >>

	
class leoColorNamePanel:
	
	#@<< class leoColorNamePanel methods >>
	#@+node:7::<< class leoColorNamePanel methods >>
	#@+body
	#@+others
	#@+node:1::namePanel.__init__
	#@+body
	def __init__ (self, colorPanel, name, color):
		
		self.colorPanel = colorPanel
		self.name = name
		self.color = color
		self.revertColor = color
	#@-body
	#@-node:1::namePanel.__init__
	#@+node:2::getSelection
	#@+body
	def getSelection (self):
	
		box = self.box ; color = None
		
		# Get the family name if possible, or font otherwise.
		items = box.curselection()
	
		if len(items)> 0:
			try: # This shouldn't fail now.
				items = map(int, items)
				color = box.get(items[0])
			except:
				es("unexpected exception")
				traceback.print_exc()
	
		if not color:
			color = self.color
		return color
	#@-body
	#@-node:2::getSelection
	#@+node:3::run
	#@+body
	def run (self,name,color):
		
		assert(name==self.name)
		assert(color==self.color)
		
		Tk = Tkinter
		config = app().config
	
		self.top = top = Tk.Toplevel(app().root)
		top.title("Color names for " + `name`)
		top.protocol("WM_DELETE_WINDOW", self.onOk)
	
		
		#@<< create color name panel >>
		#@+node:1::<< create color name panel >>
		#@+body
		# Create organizer frames
		outer = Tk.Frame(top,bd=2,relief="groove")
		outer.pack(fill="both",expand=1)
		
		upper = Tk.Frame(outer)
		upper.pack(fill="both",expand=1)
		
		# A kludge to give vertical space to the listbox!
		spacer = Tk.Frame(upper) 
		spacer.pack(side="right",pady="2i") 
		
		lower = Tk.Frame(outer)
		# padx=20 gives more room to the Listbox!
		lower.pack(padx=40) # Not expanding centers the buttons.
		
		# Create and populate the listbox.
		self.box = box = Tk.Listbox(upper) # height doesn't seem to work.
		box.bind("<Double-Button-1>", self.onApply)
		
		if color not in colorNamesList:
			box.insert(0,color)
			
		names = list(colorNamesList) # It's actually a tuple.
		names.sort()
		for name in names:
			box.insert("end",name)
		
		bar = Tk.Scrollbar(box)
		bar.pack(side="right", fill="y")
		box.pack(padx=2,pady=2,expand=1,fill="both")
		
		bar.config(command=box.yview)
		box.config(yscrollcommand=bar.set)
			
		# Create the row of buttons.
		for text,command in (
			("OK",self.onOk),
			("Cancel",self.onCancel),
			("Revert",self.onRevert),
			("Apply",self.onApply) ):
				
			b = Tk.Button(lower,text=text,command=command)
			b.pack(side="left",pady=6,padx=4)
		#@-body
		#@-node:1::<< create color name panel >>

		self.select(color)
		
		center_dialog(top) # Do this _after_ building the dialog!
		# top.resizable(0,0)
		
		# This must be a modal dialog.
		top.grab_set()
		top.focus_force() # Get all keystrokes.
	#@-body
	#@-node:3::run
	#@+node:4::onOk, onCancel, onRevert, OnApply
	#@+body
	def onApply (self,event=None):
		self.color = color = self.getSelection()
		self.colorPanel.update(self.name,color)
	
	def onOk (self):
		color = self.getSelection()
		self.colorPanel.update(self.name,color)
		self.top.destroy()
		
	def onCancel (self):
		self.onRevert()
		self.top.destroy()
		
	def onRevert (self):
		self.color = color = self.revertColor
		self.select(self.color)
		self.colorPanel.update(self.name,color)
	#@-body
	#@-node:4::onOk, onCancel, onRevert, OnApply
	#@+node:5::select
	#@+body
	def select (self,color):
	
		# trace(color)
	
		# The name should be on the list!
		box = self.box
		for i in xrange(0,box.size()):
			item = box.get(i)
			if color == item:
				box.select_clear(0,"end")
				box.select_set(i)
				box.see(i)
				return
	
		# trace("not found:" + `color`)
	#@-body
	#@-node:5::select
	#@-others
	
	#@-body
	#@-node:7::<< class leoColorNamePanel methods >>
#@-body
#@-node:0::@file leoColor.py
#@-leo
