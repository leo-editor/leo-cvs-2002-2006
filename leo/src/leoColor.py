#@+leo
#@+node:0::@file leoColor.py
#@+body
#@@language python

# Syntax coloring routines for Leo.py

from leoGlobals import *
import string,Tkinter,tkColorChooser


#@<< define colorizer constants >>
#@+node:2::<< define colorizer constants >>
#@+body
# These defaults are sure to exist.
default_colors_dict = {
	# tag name      :(     option name,           default color),
	"comment"       :("comment_color",               "red"),
	"cwebName"      :("cweb_section_name_color",     "red"),
	"pp"             :("directive_color",             "blue"),
	"docPart"        :("doc_part_color",              "red"),
	"keyword"        :("keyword_color",               "blue"),
	"leoKeyword"     :("leo_keyword_color",           "blue"),
	"link"           :("section_name_color",          "red"),
	"nameBrackets"   :("section_name_brackets_color", "blue"),
	"string"         :("string_color",                "#00aa00"), # Used by IDLE.
	"name"           :("undefined_section_name_color","red"),
	"latexBackground":("latex_background_color","white") }
#@-body
#@-node:2::<< define colorizer constants >>


#@<< define colorizer keywords >>
#@+node:1::<< define colorizer keywords >>
#@+body
#@<< leo keywords >>
#@+node:2::<< leo keywords >>
#@+body
leoKeywords = [
		"@","@c","@code","@color","@comment",
		"@delims","@doc","@encoding","@end_raw",
		"@first","@header","@ignore",
		"@language","@last","@lineending",
		"@nocolor","@noheader","@nowrap","@others",
		"@pagewidth","@path","@quiet","@raw","@root","@root-code","@root-doc",
		"@silent","@tabwidth","@terse",
		"@unit","@verbose","@wrap" ]

#@-body
#@-node:2::<< leo keywords >>



#@<< actionscript keywords >>
#@+node:1::<< actionscript keywords >>
#@+body
actionscript_keywords = (
#Jason 2003-07-03 
#Actionscript keywords for Leo adapted from UltraEdit syntax highlighting
"break", "call", "continue", "delete", "do", "else", "false", "for", "function", "goto", "if", "in", "new", "null", "return", "true", "typeof", "undefined", "var", "void", "while", "with", "#include", "catch", "constructor", "prototype", "this", "try", "_parent", "_root", "__proto__", "ASnative", "abs", "acos", "appendChild", "asfunction", "asin", "atan", "atan2", "attachMovie", "attachSound", "attributes", "BACKSPACE", "CAPSLOCK", "CONTROL", "ceil", "charAt", "charCodeAt", "childNodes", "chr", "cloneNode", "close", "concat", "connect", "cos", "createElement", "createTextNode", "DELETEKEY", "DOWN", "docTypeDecl", "duplicateMovieClip", "END", "ENTER", "ESCAPE", "enterFrame", "entry", "equal", "eval", "evaluate", "exp", "firstChild", "floor", "fromCharCode", "fscommand", "getAscii", "getBeginIndex", "getBounds", "getBytesLoaded", "getBytesTotal", "getCaretIndex", "getCode", "getDate", "getDay", "getEndIndex", "getFocus", "getFullYear", "getHours", "getMilliseconds", "getMinutes", "getMonth", "getPan", "getProperty", "getRGB", "getSeconds", "getTime", "getTimer", "getTimezoneOffset", "getTransform", "getURL", "getUTCDate", "getUTCDay", "getUTCFullYear", "getUTCHours", "getUTCMilliseconds", "getUTCMinutes", "getUTCMonth", "getUTCSeconds", "getVersion", "getVolume", "getYear", "globalToLocal", "gotoAndPlay", "gotoAndStop", "HOME", "haschildNodes", "hide", "hitTest", "INSERT", "Infinity", "ifFrameLoaded", "ignoreWhite", "indexOf", "insertBefore", "int", "isDown", "isFinite", "isNaN", "isToggled", "join", "keycode", "keyDown", "keyUp", "LEFT", "LN10", "LN2", "LOG10E", "LOG2E", "lastChild", "lastIndexOf", "length", "load", "loaded", "loadMovie", "loadMovieNum", "loadVariables", "loadVariablesNum", "localToGlobal", "log", "MAX_VALUE", "MIN_VALUE", "max", "maxscroll", "mbchr", "mblength", "mbord", "mbsubstring", "min", "NEGATIVE_INFINITY", "NaN", "newline", "nextFrame", "nextScene", "nextSibling", "nodeName", "nodeType", "nodeValue", "on", "onClipEvent", "onClose", "onConnect", "onData", "onLoad", "onXML", "ord", "PGDN", "PGUP", "PI", "POSITIVE_INFINITY", "parentNode", "parseFloat", "parseInt", "parseXML", "play", "pop", "pow", "press", "prevFrame", "previousSibling", "prevScene", "print", "printAsBitmap", "printAsBitmapNum", "printNum", "push", "RIGHT", "random", "release", "removeMovieClip", "removeNode", "reverse", "round", "SPACE", "SQRT1_2", "SQRT2", "scroll", "send", "sendAndLoad", "set", "setDate", "setFocus", "setFullYear", "setHours", "setMilliseconds", "setMinutes", "setMonth", "setPan", "setProperty", "setRGB", "setSeconds", "setSelection", "setTime", "setTransform", "setUTCDate", "setUTCFullYear", "setUTCHours", "setUTCMilliseconds", "setUTCMinutes", "setUTCMonth", "setUTCSeconds", "setVolume", "setYear", "shift", "show", "sin", "slice", "sort", "start", "startDrag", "status", "stop", "stopAllSounds", "stopDrag", "substr", "substring", "swapDepths", "splice", "split", "sqrt", "TAB", "tan", "targetPath", "tellTarget", "toggleHighQuality", "toLowerCase", "toString", "toUpperCase", "trace", "UP", "UTC", "unescape", "unloadMovie", "unLoadMovieNum", "unshift", "updateAfterEvent", "valueOf", "xmlDecl", "_alpha", "_currentframe", "_droptarget", "_focusrect", "_framesloaded", "_height", "_highquality", "_name", "_quality", "_rotation", "_soundbuftime", "_target", "_totalframes", "_url", "_visible", "_width", "_x", "_xmouse", "_xscale", "_y", "_ymouse", "_yscale", "and", "add", "eq", "ge", "gt", "le", "lt", "ne", "not", "or", "Array", "Boolean", "Color", "Date", "Key", "Math", "MovieClip", "Mouse", "Number", "Object", "Selection", "Sound", "String", "XML", "XMLSocket"
)
#@-body
#@-node:1::<< actionscript keywords >>


#@<< c keywords >>
#@+node:3::<< c keywords >>
#@+body
c_keywords = (
	# C keywords
	"auto","break","case","char","continue",
	"default","do","double","else","enum","extern",
	"float","for","goto","if","int","long","register","return",
	"short","signed","sizeof","static","struct","switch",
	"typedef","union","unsigned","void","volatile","while",
	# C++ keywords
	"asm","bool","catch","class","const_cast",
	"delete","dynamic_cast","explicit","false","friend",
	"inline","mutable","namespace","new","operator",
	"private","protected","public","reinterpret_cast","static_cast",
	"template","this","throw","true","try",
	"typeid","typename","using","virtual","wchar_t")
#@-body
#@-node:3::<< c keywords >>

cweb_keywords = c_keywords

#@<< html keywords >>
#@+node:4::<< html keywords >>
#@+body
# No longer used by syntax colorer.
html_keywords = ()

if 0: # Not used at present.
	unused_keywords = (
		# html constructs.
		"a","body","cf",
		"h1","h2","h3","h4","h5","h6",
		"head","html","hr",
		"i","img","li","lu","meta",
		"p","title","ul",
		# Common tags
		"caption","col","colgroup",
		"table","tbody","td","tfoot","th","thead","tr",
		"script","style")

	html_specials = ( "<%","%>" )
#@-body
#@-node:4::<< html keywords >>


#@<< java keywords >>
#@+node:5::<< java keywords >>
#@+body
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
#@-body
#@-node:5::<< java keywords >>


#@<< latex keywords >>
#@+node:6::<< latex keywords >>
#@+body
#If you see two idenitical words, with minor capitalization differences
#DO NOT ASSUME that they are the same word. For example \vert produces
#a single vertical line and \Vert produces a double vertical line
#Marcus A. Martin.

latex_keywords = (
	#special keyworlds
	"\\@", "\\(", "\\)", "\\{", "\\}",
	#A
	"\\acute", "\\addcontentsline", "\\addtocontents", "\\addtocounter", "\\address",
	"\\addtolength", "\\addvspace", "\\AE", "\\ae", "\\aleph", "\\alph", "\\angle",
	"\\appendix", 
	"\\approx",	"\\arabic", "\\arccos", "\\arcsin", "\\arctan", "\\ast", "\\author",
	#B
	"\\b", "\\backmatter", "\\backslash", "\\bar", "\\baselineskip", "\\baselinestretch",
	"\\begin", "\\beta", "\\bezier", "\\bf", "\\bfseries", "\\bibitem", "\\bigcap", 
	"\\bigcup", "\\bigodot", "\\bigoplus", "\\bigotimes", "\\bigskip", "\\biguplus", 
	"\\bigvee", "\\bigwedge",	"\\bmod", "\\boldmath", "\\Box", "\\breve", "\\bullet",
	#C
	"\\c", "\\cal", "\\caption", "\\cdot", "\\cdots", "\\centering", "\\chapter", 
	"\\check", "\\chi", "\\circ", "\\circle", "\\cite", "\\cleardoublepage", "\\clearpage", 
	"\\cline",	"\\closing", "\\clubsuit", "\\coprod", "\\copywright", "\\cos", "\\cosh", 
	"\\cot", "\\coth",	"csc",
	#D
	"\\d", "\\dag", "\\dashbox", "\\date", "\\ddag", "\\ddot", "\\ddots", "\\decl", 
	"\\deg", "\\Delta", 
	"\\delta", "\\depthits", "\\det", 
	"\\DH", "\\dh", "\\Diamond", "\\diamondsuit", "\\dim", "\\div", "\\DJ", "\\dj", 
	"\\documentclass", "\\documentstyle", 
	"\\dot", "\\dotfil", "\\downarrow",
	#E
	"\\ell", "\\em", "\\emph", "\\end", "\\enlargethispage", "\\ensuremath", 
	"\\enumi", "\\enuii", "\\enumiii", "\\enuiv", "\\epsilon", "\\equation", "\\equiv",	
	"\\eta", "\\example", "\\exists", "\\exp",
	#F
	"\\fbox", "\\figure", "\\flat", "\\flushbottom", "\\fnsymbol", "\\footnote", 
	"\\footnotemark", "\\fotenotesize", 
	"\\footnotetext", "\\forall", "\\frac", "\\frame", "\\framebox", "\\frenchspacing", 
	"\\frontmatter",
	#G
	"\\Gamma", "\\gamma", "\\gcd", "\\geq", "\\gg", "\\grave", "\\guillemotleft", 
	"\\guillemotright",	"\\guilsinglleft", "\\guilsinglright",
	#H
	"\\H", "\\hat", "\\hbar", "\\heartsuit", "\\heightits", "\\hfill", "\\hline", "\\hom",
	"\\hrulefill",	"\\hspace", "\\huge",	"\\Huge",	"\\hyphenation"
	#I
	"\\Im", "\\imath", "\\include", "includeonly", "indent", "\\index", "\\inf", "\\infty", 
	"\\input", "\\int", "\\iota",	"\\it", "\\item", "\\itshape",
	#J
	"\\jmath", "\\Join",
	#K
	"\\k", "\\kappa", "\\ker", "\\kill",
	#L
	"\\label", "\\Lambda", "\\lambda", "\\langle", "\\large", "\\Large", "\\LARGE", 
	"\\LaTeX", "\\LaTeXe", 
	"\\ldots", "\\leadsto", "\\left", "\\Leftarrow", "\\leftarrow", "\\lefteqn", "\\leq",
	"\\lg", "\\lhd", "\\lim", "\\liminf", "\\limsup", "\\line", 	"\\linebreak", 
	"\\linethickness", "\\linewidth",	"\\listfiles",
	"\\ll", "\\ln", "\\location", "\\log", "\\Longleftarrow", "\\longleftarrow", 
	"\\Longrightarrow",	"longrightarrow",
	#M
	"\\mainmatter", "\\makebox", "\\makeglossary", "\\makeindex","\\maketitle", "\\markboth", "\\markright",
	"\\mathbf", "\\mathcal", "\\mathit", "\\mathnormal", "\\mathop",
	"\\mathrm", "\\mathsf", "\\mathtt", "\\max", "\\mbox", "\\mdseries", "\\medskip",
	"\\mho", "\\min", "\\mp", "\\mpfootnote", "\\mu", "\\multicolumn", "\\multiput",
	#N
	"\\nabla", "\\natural", "\\nearrow", "\\neq", "\\newcommand", "\\newcounter", 
	"\\newenvironment", "\\newfont",
	"\\newlength",	"\\newline", "\\newpage", "\\newsavebox", "\\newtheorem", "\\NG", "\\ng",
	"\\nocite", "\\noindent", "\\nolinbreak", "\\nopagebreak", "\\normalsize",
	"\\not", "\\nu", "nwarrow",
	#O
	"\\Omega", "\\omega", "\\onecolumn", "\\oint", "\\opening", "\\oval", 
	"\\overbrace", "\\overline",
	#P
	"\\P", "\\page", "\\pagebreak", "\\pagenumbering", "\\pageref", "\\pagestyle", 
	"\\par", "\\parbox",	"\\paragraph", "\\parindent", "\\parskip", "\\part", 
	"\\partial", "\\per", "\\Phi", 	"\\phi",	"\\Pi", "\\pi", "\\pm", 
	"\\pmod", "\\pounds", "\\prime", "\\printindex", "\\prod", "\\propto", "\\protext", 
	"\\providecomamnd", "\\Psi",	"\\psi", "\\put",
	#Q
	"\\qbezier", "\\quoteblbase", "\\quotesinglbase",
	#R
	"\\r", "\\raggedbottom", "\\raggedleft", "\\raggedright", "\\raisebox", "\\rangle", 
	"\\Re", "\\ref", 	"\\renewcommand", "\\renewenvironment", "\\rhd", "\\rho", "\\right", 
	"\\Rightarrow",	"\\rightarrow", "\\rm", "\\rmfamily",
	"\\Roman", "\\roman", "\\rule", 
	#S
	"\\s", "\\samepage", "\\savebox", "\\sbox", "\\sc", "\\scriptsize", "\\scshape", 
	"\\searrow",	"\\sec", "\\section",
	"\\setcounter", "\\setlength", "\\settowidth", "\\settodepth", "\\settoheight", 
	"\\settowidth", "\\sf", "\\sffamily", "\\sharp", "\\shortstack", "\\Sigma", "\\sigma", 
	"\\signature", "\\sim", "\\simeq", "\\sin", "\\sinh", "\\sl", "\\SLiTeX",
	"\\slshape", "\\small", "\\smallskip", "\\spadesuit", "\\sqrt", "\\sqsubset",	
	"\\sqsupset", "\\SS",
	"\\stackrel", "\\star", "\\subsection", "\\subset", 
	"\\subsubsection", "\\sum", "\\sup", "\\supressfloats", "\\surd", "\\swarrow",
	#T
	"\\t", "\\table", "\\tableofcontents", "\\tabularnewline", "\\tan", "\\tanh", 
	"\\tau", "\\telephone",	"\\TeX", "\\textbf",
	"\\textbullet", "\\textcircled", "\\textcompworkmark",	"\\textemdash", 
	"\\textendash", "\\textexclamdown", "\\textheight", "\\textquestiondown", 
	"\\textquoteblleft", "\\textquoteblright", "\\textquoteleft",
	"\\textperiod", "\\textquotebl", "\\textquoteright", "\\textmd", "\\textit", "\\textrm", 
	"\\textsc", "\\textsl", "\\textsf", "\\textsuperscript", "\\texttt", "\\textup",
	"\\textvisiblespace", "\\textwidth", "\\TH", "\\th", "\\thanks", "\\thebibligraphy",
	"\\Theta", "theta", 
	"\\tilde", "\\thinlines", 
	"\\thispagestyle", "\\times", "\\tiny", "\\title",	"\\today", "\\totalheightits", 
	"\\triangle", "\\tt", 
	"\\ttfamily", "\\twocoloumn", "\\typeout", "\\typein",
	#U
	"\\u", "\\underbrace", "\\underline", "\\unitlength", "\\unlhd", "\\unrhd", "\\Uparrow",
	"\\uparrow",	"\\updownarrow", "\\upshape", "\\Upsilon", "\\upsilon", "\\usebox",	
	"\\usecounter", "\\usepackage", 
	#V
	"\\v", "\\value", "\\varepsilon", "\\varphi", "\\varpi", "\\varrho", "\\varsigma", 
	"\\vartheta", "\\vdots", "\\vec", "\\vector", "\\verb", "\\Vert", "\\vert", 	"\\vfill",
	"\\vline", "\\vphantom", "\\vspace",
	#W
	"\\widehat", "\\widetilde", "\\widthits", "\\wp",
	#X
	"\\Xi", "\\xi",
	#Z
	"\\zeta" )
#@-body
#@-node:6::<< latex keywords >>


#@<< pascal keywords >>
#@+node:7::<< pascal keywords >>
#@+body
pascal_keywords = (
	"and","array","as","begin",
	"case","const","class","constructor","cdecl"
	"div","do","downto","destructor","dispid","dynamic",
	"else","end","except","external",
	"false","file","for","forward","function","finally",
	"goto","if","in","is","label","library",
	"mod","message","nil","not","nodefault""of","or","on",
	"procedure","program","packed","pascal",
	"private","protected","public","published",
	"record","repeat","raise","read","register",
	"set","string","shl","shr","stdcall",
	"then","to","true","type","try","until","unit","uses",
	"var","virtual","while","with","xor"
	# object pascal
	"asm","absolute","abstract","assembler","at","automated",
	"finalization",
	"implementation","inherited","initialization","inline","interface",
	"object","override","resident","resourcestring",
	"threadvar",
	# limited contexts
	"exports","property","default","write","stored","index","name" )
#@-body
#@-node:7::<< pascal keywords >>


#@<< perl keywords >>
#@+node:8::<< perl keywords >>
#@+body
perl_keywords = (
	"continue","do","else","elsif","format","for","format","for","foreach",
	"if","local","package","sub","tr","unless","until","while","y",
	# Comparison operators
	"cmp","eq","ge","gt","le","lt","ne",
	# Matching ooperators
	"m","s",
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
#@-body
#@-node:8::<< perl keywords >>

perlpod_keywords = perl_keywords

#@<< python keywords >>
#@+node:9::<< python keywords >>
#@+body
python_keywords = (
	"and",       "del",       "for",       "is",        "raise",    
	"assert",    "elif",      "from",      "lambda",    "return",   
	"break",     "else",      "global",    "not",       "try",      
	"class",     "except",    "if",        "or",        "yield",   
	"continue",  "exec",      "import",    "pass",      "while",
	"def",       "finally",   "in",        "print")
#@-body
#@-node:9::<< python keywords >>


#@<< tcl/tk keywords >>
#@+node:10::<< tcl/tk keywords >>
#@+body
tcltk_keywords = ( # Only the tcl keywords are here.
	"after",     "append",    "array",
	"bgerror",   "binary",    "break",
	"catch",     "cd",        "clock",
	"close",     "concat",    "continue",
	"dde",
	"encoding",  "eof",       "eval",
	"exec",      "exit",      "expr",
	"fblocked",  "fconfigure","fcopy",     "file",      "fileevent",
	"filename",  "flush",     "for",       "foreach",   "format",
	"gets",      "glob",      "global",
	"history",
	"if",        "incr",      "info",      "interp",
	"join",
	"lappend",   "lindex",    "linsert",   "list",      "llength",
	"load",      "lrange",    "lreplace",  "lsearch",   "lsort",
	"memory",    "msgcat",
	"namespace",
	"open",
	"package",   "parray",    "pid",
	"proc",      "puts",      "pwd",
	"read",      "regexp",    "registry",   "regsub",
	"rename",    "resource",  "return",
	"scan",      "seek",      "set",        "socket",   "source",
	"split",     "string",    "subst",      "switch",
	"tell",      "time",      "trace",
	"unknown",   "unset",     "update",     "uplevel",   "upvar",
	"variable",  "vwait",
	"while" )
#@-body
#@-node:10::<< tcl/tk keywords >>


#@<< php keywords >>
#@+node:11::<< php keywords >>
#@+body
php_keywords = ( # 08-SEP-2002 DTHEIN
	"__CLASS__", "__FILE__", "__FUNCTION__", "__LINE__",
	"and", "as", "break",
	"case", "cfunction", "class", "const", "continue",
	"declare", "default", "do",
	"else", "elseif", "enddeclare", "endfor", "endforeach",
	"endif", "endswitch",  "endwhile", "eval", "extends",
	"for", "foreach", "function", "global", "if",
	"new", "old_function", "or", "static", "switch",
	"use", "var", "while", "xor" )
	
# The following are supposed to be followed by ()
php_paren_keywords = (
	"array", "die", "echo", "empty", "exit",
	"include", "include_once", "isset", "list",
	"print", "require", "require_once", "return",
	"unset" )
	
# The following are handled by special case code:
# "<?php", "?>"

#@-body
#@-node:11::<< php keywords >>


#@<< rebol keywords >>
#@+node:12::<< rebol keywords >>
#@+body
rebol_keywords = (
#Jason 2003-07-03 
#based on UltraEdit syntax highlighting
"about", "abs", "absolute", "add", "alert", "alias", "all", "alter", "and", "and~", "any", "append", "arccosine", "arcsine", "arctangent", "array", "ask", "at",  
"back", "bind", "boot-prefs", "break", "browse", "build-port", "build-tag",  
"call", "caret-to-offset", "catch", "center-face", "change", "change-dir", "charset", "checksum", "choose", "clean-path", "clear", "clear-fields", "close", "comment", "complement", "compose", "compress", "confirm", "continue-post", "context", "copy", "cosine", "create-request", "crypt", "cvs-date", "cvs-version",  
"debase", "decode-cgi", "decode-url", "decompress", "deflag-face", "dehex", "delete", "demo", "desktop", "detab", "dh-compute-key", "dh-generate-key", "dh-make-key", "difference", "dirize", "disarm", "dispatch", "divide", "do", "do-boot", "do-events", "do-face", "do-face-alt", "does", "dsa-generate-key", "dsa-make-key", "dsa-make-signature", "dsa-verify-signature",  
"echo", "editor", "either", "else", "emailer", "enbase", "entab", "exclude", "exit", "exp", "extract", 
"fifth", "find", "find-key-face", "find-window", "flag-face", "first", "flash", "focus", "for", "forall", "foreach", "forever", "form", "forskip", "fourth", "free", "func", "function",  
"get", "get-modes", "get-net-info", "get-style",  
"halt", "has", "head", "help", "hide", "hide-popup",  
"if", "import-email", "in", "inform", "input", "insert", "insert-event-func", "intersect", 
"join", 
"last", "launch", "launch-thru", "layout", "license", "list-dir", "load", "load-image", "load-prefs", "load-thru", "log-10", "log-2", "log-e", "loop", "lowercase",  
"make", "make-dir", "make-face", "max", "maximum", "maximum-of", "min", "minimum", "minimum-of", "mold", "multiply",  
"negate", "net-error", "next", "not", "now",  
"offset-to-caret", "open", "open-events", "or", "or~", 
"parse", "parse-email-addrs", "parse-header", "parse-header-date", "parse-xml", "path-thru", "pick", "poke", "power", "prin", "print", "probe", "protect", "protect-system",  
"q", "query", "quit",  
"random", "read", "read-io", "read-net", "read-thru", "reboot", "recycle", "reduce", "reform", "rejoin", "remainder", "remold", "remove", "remove-event-func", "rename", "repeat", "repend", "replace", "request", "request-color", "request-date", "request-download", "request-file", "request-list", "request-pass", "request-text", "resend", "return", "reverse", "rsa-encrypt", "rsa-generate-key", "rsa-make-key", 
"save", "save-prefs", "save-user", "scroll-para", "second", "secure", "select", "send", "send-and-check", "set", "set-modes", "set-font", "set-net", "set-para", "set-style", "set-user", "set-user-name", "show", "show-popup", "sine", "size-text", "skip", "sort", "source", "split-path", "square-root", "stylize", "subtract", "switch",  
"tail", "tangent", "textinfo", "third", "throw", "throw-on-error", "to", "to-binary", "to-bitset", "to-block", "to-char", "to-date", "to-decimal", "to-email", "to-event", "to-file", "to-get-word", "to-hash", "to-hex", "to-idate", "to-image", "to-integer", "to-issue", "to-list", "to-lit-path", "to-lit-word", "to-local-file", "to-logic", "to-money", "to-none", "to-pair", "to-paren", "to-path", "to-rebol-file", "to-refinement", "to-set-path", "to-set-word", "to-string", "to-tag", "to-time", "to-tuple", "to-url", "to-word", "trace", "trim", "try",  
"unfocus", "union", "unique", "uninstall", "unprotect", "unset", "until", "unview", "update", "upgrade", "uppercase", "usage", "use",  
"vbug", "view", "view-install", "view-prefs",  
"wait", "what", "what-dir", "while", "write", "write-io",  
"xor", "xor~",  
"action!", "any-block!", "any-function!", "any-string!", "any-type!", "any-word!",  
"binary!", "bitset!", "block!",  
"char!",  
"datatype!", "date!", "decimal!", 
"email!", "error!", "event!",  
"file!", "function!",  
"get-word!",  
"hash!",  
"image!", "integer!", "issue!",  
"library!", "list!", "lit-path!", "lit-word!", "logic!",  
"money!",  
"native!", "none!", "number!",  
"object!", "op!",  
"pair!", "paren!", "path!", "port!",  
"refinement!", "routine!",  
"series!", "set-path!", "set-word!", "string!", "struct!", "symbol!",  
"tag!", "time!", "tuple!",  
"unset!", "url!",  
"word!",  
"any-block?", "any-function?", "any-string?", "any-type?", "any-word?",  
"binary?", "bitset?", "block?",  
"char?", "connected?", "crypt-strength?", 
"datatype?", "date?", "decimal?", "dir?",  
"email?", "empty?", "equal?", "error?", "even?", "event?", "exists?", "exists-key?"
"file?", "flag-face?", "found?", "function?",  
"get-word?", "greater-or-equal?", "greater?",  
"hash?", "head?",  
"image?", "in-window?", "index?", "info?", "input?", "inside?", "integer?", "issue?",  
"length?", "lesser-or-equal?", "lesser?", "library?", "link-app?", "link?", "list?", "lit-path?", "lit-word? logic?",  
"modified?", "money?",  
"native?", "negative?", "none?", "not-equal?", "number?",  
"object?", "odd?", "offset?", "op?", "outside?",  
"pair?", "paren?", "path?", "port?", "positive?",  
"refinement?", "routine?",  
"same?", "screen-offset?", "script?", "series?", "set-path?", "set-word?", "size?", "span?", "strict-equal?", "strict-not-equal?", "string?", "struct?",  
"tag?", "tail?", "time?", "tuple?", "type?",  
"unset?", "url?",  
"value?", "view?", 
"within?", "word?",  
"zero?"
)
#@-body
#@-node:12::<< rebol keywords >>


#@-body
#@-node:1::<< define colorizer keywords >>


#@<< define color panel data >>
#@+node:3::<< define color panel data >>
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
#@-node:3::<< define color panel data >>



#@+others
#@+node:4::class leoColorPanel
#@+body
class baseLeoColorPanel:
	"""The base class for Leo's color panel."""

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
		self.nameButtons = {}
		self.option_names = {}
		# Save colors for revert.  onOk alters this.
		self.revertColors = {}
		config = app().config
		for name,option_name,default_color in colorPanelData:
			self.revertColors[option_name] = config.getColorsPref(option_name)
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
		attachLeoIcon(top)
	
		
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
			
			b2 = Tk.Button(f,width=12,text=option_color)
			self.nameButtons[name]=b2
			
			# 9/15/02: Added self=self to remove Python 2.1 warning.
			callback = lambda name=name,self=self:self.showColorPicker(name)
			b3 = Tk.Button(f,text="Color Picker...",command=callback)
		
			# 9/15/02: Added self=self to remove Python 2.1 warning.
			callback = lambda name=name,color=color,self=self:self.showColorName(name,color)
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
			top.focus_set() # Get all keystrokes.
	#@-body
	#@-node:2::run
	#@+node:3::showColorPicker
	#@+body
	def showColorPicker (self,name):
		
		option_name = self.option_names[name]
		color = app().config.getColorsPref(option_name)
		rgb,val = tkColorChooser.askcolor(color=color)
		if val != None:
			self.update(name,val)
	#@-body
	#@-node:3::showColorPicker
	#@+node:4::showColorName
	#@+body
	def showColorName (self,name,color):
		
		np = leoColorNamePanel(self,name,color)
		np.run(name,color)
	#@-body
	#@-node:4::showColorName
	#@+node:5::colorPanel.onOk, onCancel, onRevert
	#@+body
	def onOk (self):
		# Update the revert colors
		config = app().config
		for name in self.changed_options:
			option_name = self.option_names[name]
			self.revertColors[option_name] = config.getColorsPref(option_name)
		self.changed_options = []
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
		config = app().config
		for name in self.changed_options:
			option_name = self.option_names[name]
			old_val = self.revertColors[option_name]
			# Update the current settings.
			config.setColorsPref(option_name,old_val)
			# Update the buttons.
			b = self.buttons[name]
			b.configure(bg=old_val)
			b = self.nameButtons[name]
			b.configure(text=`old_val`)
		self.changed_options = []
		self.commands.recolor()
	#@-body
	#@-node:5::colorPanel.onOk, onCancel, onRevert
	#@+node:6::update
	#@+body
	def update (self,name,val):
		
		config = app().config
		# es(str(name) + " = " + str(val))
		
		# Put the new color in the button.
		b = self.buttons[name]
		b.configure(bg=val)
		option_name = self.option_names[name]
		
		# Put the new color name or value in the name button.
		b = self.nameButtons[name]
		b.configure(text=str(val))
		
		# Save the changed option names for revert and cancel.
		if name not in self.changed_options:
			self.changed_options.append(name)
	
		# Set the new value and recolor.
		config.setColorsPref(option_name,val)
		self.commands.recolor()
	#@-body
	#@-node:6::update
	#@-others

	
class leoColorPanel (baseLeoColorPanel):
	"""A class that creates Leo's color picker panel."""
	pass


#@-body
#@-node:4::class leoColorPanel
#@+node:5::class leoColorNamePanel
#@+body
class baseLeoColorNamePanel:
	"""The base class for Leo's color name picker panel."""

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
				es_exception()
	
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
		self.revertColor = color
		
		Tk = Tkinter
		config = app().config
	
		self.top = top = Tk.Toplevel(app().root)
		top.title("Color names for " + '"' + name + '"')
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
		top.focus_set() # Get all keystrokes.
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

	
class leoColorNamePanel(baseLeoColorNamePanel):
	"""A class that creates Leo's color name picker panel."""
	pass
#@-body
#@-node:5::class leoColorNamePanel
#@+node:6::class colorizer
#@+body
class baseColorizer:
	"""The base class for Leo's syntax colorer."""

	#@+others
	#@+node:1::color.__init__
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
		self.comment_string = None # Set by scanColorDirectives on @comment
		# For incremental coloring.
		self.tags = (
			"blank","comment","cwebName","docPart","keyword","leoKeyword",
			"latexModeBackground","latexModeKeyword",
			"latexBackground","latexKeyword",
			"link","name","nameBrackets","pp","string","tab",
			"elide","bold","bolditalic","italic") # new for wiki styling.
		self.color_pass = 0
		self.incremental = false
		self.redoColoring = false
		self.redoingColoring = false
		self.sel = None
		self.lines = []
		self.states = []
		self.last_flag = "unknown"
		self.last_language = "unknown"
		self.last_comment = "unknown"
		# For use of external markup routines.
		self.last_markup = "unknown" 
		self.markup_string = "unknown"
		
		#@<< ivars for communication between colorAllDirectives and its allies >>
		#@+node:1::<< ivars for communication between colorAllDirectives and its allies >>
		#@+body
		# Copies of arguments.
		self.v = None
		self.body = None
		self.language = None
		self.flag = None
		self.line_index = 0
		
		# Others.
		self.single_comment_start = None
		self.block_comment_start = None
		self.block_comment_end = None
		self.has_string = None
		self.string_delims = ("'",'"')
		self.has_pp_directives = None
		self.keywords = None
		self.lb = None
		self.rb = None
		self.rootMode = None # None, "code" or "doc"
		
		config = app().config
		self.latex_cweb_docs     = config.getBoolColorsPref("color_cweb_doc_parts_with_latex")
		self.latex_cweb_comments = config.getBoolColorsPref("color_cweb_comments_with_latex")
		# print "docs,comments",`self.latex_cweb_docs`,`self.latex_cweb_comments`
		#@-body
		#@-node:1::<< ivars for communication between colorAllDirectives and its allies >>

		
		#@<< define dispatch dicts >>
		#@+node:2::<< define dispatch dicts >>
		#@+body
		self.state_dict = {
			"blockComment" : self.continueBlockComment,
			"doubleString" : self.continueDoubleString, # 1/25/03
			"nocolor"      : self.continueNocolor,
			"normal"       : self.doNormalState,
			"singleString" : self.continueSingleString,  # 1/25/03
			"string3s"     : self.continueSinglePythonString,
			"string3d"     : self.continueDoublePythonString,
			"doc"          : self.continueDocPart }
			
		# Eventually all entries in these dicts will be entered dynamically
		# under the control of the XML description of the present language.
		
		if 0: # not ready yet.
		
			self.dict1 = { # 1-character patterns.
				'"' : self.doString,
				"'" : self.doString,
				'@' : self.doPossibleLeoKeyword,
				' ' : self.doBlank,
				'\t': self.doTab }
		
			self.dict2 = {} # 2-character patterns
			
			# Searching this list might be very slow!
			mutli_list = [] # Multiple character patterns.
			
			# Enter single-character patterns...
			if self.has_pp_directives:
				dict1 ["#"] = self.doPPDirective
						
			for ch in string.letters:
				dict1 [ch] = self.doPossibleKeyword
			dict1 ['_'] = self.doPossibleKeyword
			
			if self.language == "latex":
				dict1 ['\\'] = self.doPossibleKeyword
				
			if self.language == "php":
				dict1 ['<'] = self.doSpecialPHPKeyword
				dict1 ['?'] = self.doSpecialPHPKeyword
			
			# Enter potentially multi-character patterns.  (or should this be just 2-character patterns)
			if self.language == "cweb":
				dict2 ["@("] = self.doPossibleSectionRefOrDef
			else:
				dict2 ["<<"] = self.doPossibleSectionRefOrDef
				
			if self.single_comment_start:
				n = len(self.single_comment_start)
				if n == 1:
					dict1 [self.single_comment_start] = self.doSingleCommentLine
				elif n == 2:
					dict2 [self.single_comment_start] = self.doSingleCommentLine
				else:
					mutli_list.append((self.single_comment_start,self.doSingleCommentLine),)
			
			if self.block_comment_start:
				n = len(self.block_comment_start)
				if n == 1:
					dict1 [self.block_comment_start] = self.doBlockComment
				elif n == 2:
					ddict2 [self.block_comment_start] = self.doBlockComment
				else:
					mutli_list.append((self.block_comment_start,self.doBlockComment),)
		#@-body
		#@-node:2::<< define dispatch dicts >>

		
		#@<< define fonts and data for wiki tags >>
		#@+node:3::<< define fonts and data for wiki tags >>
		#@+body
		self.bold_font = config.getFontFromParams(
			"body_text_font_family", "body_text_font_size",
			"body_text_font_slant",  "body_text_font_weight")
		
		self.bold_font.configure(weight="bold")
		
		self.italic_font = config.getFontFromParams(
			"body_text_font_family", "body_text_font_size",
			"body_text_font_slant",  "body_text_font_weight")
			
		self.italic_font.configure(slant="italic")
			
		self.bolditalic_font = config.getFontFromParams(
			"body_text_font_family", "body_text_font_size",
			"body_text_font_slant",  "body_text_font_weight")
			
		self.bolditalic_font.configure(weight="bold",slant="italic")
		
		self.color_tags_list = []
		self.image_references = []
		
		#@-body
		#@-node:3::<< define fonts and data for wiki tags >>
	#@-body
	#@-node:1::color.__init__
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
	#@+node:3::colorize & recolor_range
	#@+body
	# The main colorizer entry point.
	
	def colorize(self,v,body,incremental=false):
	
		if self.enabled:
			# print "colorize:incremental",incremental
			self.incremental=incremental
			self.updateSyntaxColorer(v)
			self.colorizeAnyLanguage(v,body)
			
	# Called from incremental undo code.
	# Colorizes the lines between the leading and trailing lines.
			
	def recolor_range(self,v,body,leading,trailing):
		
		if self.enabled:
			# print "recolor_range:leading,trailing",leading,trailing
			self.incremental=true
			self.updateSyntaxColorer(v)
			self.colorizeAnyLanguage(v,body,leading=leading,trailing=trailing)
	
	#@-body
	#@-node:3::colorize & recolor_range
	#@+node:4::colorizeAnyLanguage & allies
	#@+body
	def colorizeAnyLanguage (self,v,body,leading=None,trailing=None):
		
		"""Color the body pane either incrementally or non-incrementally"""
		
		#trace(`v`)
		try:
			
			#@<< initialize ivars & tags >>
			#@+node:1::<< initialize ivars & tags >> colorizeAnyLanguage
			#@+body
			# Add any newly-added user keywords.
			for d in globalDirectiveList:
				name = '@' + d
				if name not in leoKeywords:
					leoKeywords.append(name)
			
			# Copy the arguments.
			self.v = v
			self.body = body
			s = body.get("1.0","end")
			self.sel = sel = body.index("insert") # get the location of the insert point
			start, end = string.split(sel,'.')
			start = int(start)
			
			# trace(`self.language`)
			# trace(`self.count` + `self.v`)
			# trace(`body.tag_names()`)
			
			if not self.incremental:
				self.removeAllTags()
				self.removeAllImages()
			
			self.redoColoring = false
			self.redoingColoring = false
			
			
			#@<< configure tags >>
			#@+node:1::<< configure tags >>
			#@+body
			config = app().config
			assert(config)
			
			for name in default_colors_dict.keys(): # Python 2.1 support.
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
			if 0: # use_hyperlinks: # Use the same coloring, even when hyperlinks are in effect.
				body.tag_config("link",underline=1) # defined
				body.tag_config("name",underline=0) # undefined
			else:
				body.tag_config("link",underline=0)
				if underline_undefined:
					body.tag_config("name",underline=1)
				else:
					body.tag_config("name",underline=0)
					
			# 8/4/02: we only create tags for whitespace when showing invisibles.
			if self.showInvisibles:
				for name,option_name,default_color in (
					("blank","show_invisibles_space_background_color","Gray90"),
					("tab",  "show_invisibles_tab_background_color",  "Gray80")):
					option_color = config.getColorsPref(option_name)
					color = choose(option_color,option_color,default_color)
					try:
						body.tag_config(name,background=color)
					except: # Recover after a user error.
						body.tag_config(name,background=default_color)
				
			# 11/15/02: Colors for latex characters.  Should be user options...
			
			if 1: # Alas, the selection doesn't show if a background color is specified.
				body.tag_configure("latexModeBackground",foreground="black")
				body.tag_configure("latexModeKeyword",foreground="blue")
				body.tag_configure("latexBackground",foreground="black")
				body.tag_configure("latexKeyword",foreground="blue")
			else: # Looks cool, and good for debugging.
				body.tag_configure("latexModeBackground",foreground="black",background="seashell1")
				body.tag_configure("latexModeKeyword",foreground="blue",background="seashell1")
				body.tag_configure("latexBackground",foreground="black",background="white")
				body.tag_configure("latexKeyword",foreground="blue",background="white")
				
			# Tags for wiki coloring.
			if self.showInvisibles:
				body.tag_configure("elide",background="yellow")
			else:
				body.tag_configure("elide",elide="1")
			body.tag_configure("bold",font=self.bold_font)
			body.tag_configure("italic",font=self.italic_font)
			body.tag_configure("bolditalic",font=self.bolditalic_font)
			for name in self.color_tags_list:
				self.body.tag_configure(name,foreground=name)
			#@-body
			#@-node:1::<< configure tags >>

			
			#@<< configure language-specific settings >>
			#@+node:2::<< configure language-specific settings >>
			#@+body
			# Define has_string, keywords, single_comment_start, block_comment_start, block_comment_end.
			
			if self.language == "cweb": # Use C comments, not cweb sentinel comments.
				delim1,delim2,delim3 = set_delims_from_language("c")
			elif self.comment_string:
				delim1,delim2,delim3 = set_delims_from_string(self.comment_string)
			elif self.language == "plain": # 1/30/03
				delim1,delim2,delim3 = None,None,None
			else:
				delim1,delim2,delim3 = set_delims_from_language(self.language)
			
			self.single_comment_start = delim1
			self.block_comment_start = delim2
			self.block_comment_end = delim3
			
			# A strong case can be made for making this code as fast as possible.
			# Whether this is compatible with general language descriptions remains to be seen.
			self.has_string = self.language != "plain"
			if self.language == "plain":
				self.string_delims = ()
			elif self.language == "html":
				self.string_delims = ('"')
			else:
				self.string_delims = ("'",'"')
			self.has_pp_directives = self.language in ("c","cweb","latex")
			
			# The list of languages for which keywords exist.
			# Eventually we might just use language_delims_dict.keys()
			languages = [
				"actionscript","c","cweb","html","java","latex",
				"pascal","perl","perlpod","php","python","rebol","tcltk"]
			
			self.keywords = []
			if self.language == "cweb":
				for i in c_keywords:
					self.keywords.append(i)
				for i in cweb_keywords:
					self.keywords.append(i)
			else:
				for name in languages:
					if self.language==name: 
						# print "setting keywords for",name
						exec("self.keywords=%s_keywords" % name)
			
			# Color plain text unless we are under the control of @nocolor.
			# state = choose(self.flag,"normal","nocolor")
			state = self.setFirstLineState()
			
			if 1: # 10/25/02: we color both kinds of references in cweb mode.
				self.lb = "<<"
				self.rb = ">>"
			else:
				self.lb = choose(self.language == "cweb","@<","<<")
				self.rb = choose(self.language == "cweb","@>",">>")
			#@-body
			#@-node:2::<< configure language-specific settings >>

			
			self.hyperCount = 0 # Number of hypertext tags
			self.count += 1
			lines = string.split(s,'\n')
			#@-body
			#@-node:1::<< initialize ivars & tags >> colorizeAnyLanguage

			doHook("init-color-markup",colorer=self,v=self.v)
			self.color_pass = 0
			if self.incremental and (
				
				#@<< all state ivars match >>
				#@+node:2::<< all state ivars match >>
				#@+body
				self.flag == self.last_flag and
				self.last_language == self.language and
				self.comment_string == self.last_comment and
				self.markup_string == self.last_markup
				#@-body
				#@-node:2::<< all state ivars match >>
 ):
				
				#@<< incrementally color the text >>
				#@+node:3::<< incrementally color the text >>
				#@+body
				#@+at
				#   Each line has a starting state.  The starting state for 
				# the first line is always "normal".
				# 
				# We need remember only self.lines and self.states between 
				# colorizing.  It is not necessary to know where the text 
				# comes from, only what the previous text was!  We must always 
				# colorize everything when changing nodes, even if all lines 
				# match, because the context may be different.
				# 
				# We compute the range of lines to be recolored by comparing 
				# leading lines and trailing lines of old and new text.  All 
				# other lines (the middle lines) must be colorized, as well as 
				# any trailing lines whose states may have changed as the 
				# result of changes to the middle lines.

				#@-at
				#@@c

				# trace("incremental")
				
				# 6/30/03: make a copies of everything
				old_lines = self.lines[:]
				old_states = self.states[:]
				new_lines = lines[:]
				new_states = []
				
				new_len = len(new_lines)
				old_len = len(old_lines)
				
				if new_len == 0:
					self.states = []
					self.lines = []
					return
				
				# Bug fix: 11/21/02: must test against None.
				if leading != None and trailing != None:
					# print "leading,trailing:",leading,trailing
					leading_lines = leading
					trailing_lines = trailing
				else:
					
					#@<< compute leading, middle & trailing lines >>
					#@+node:1::<< compute leading, middle & trailing  lines >>
					#@+body
					#@+at
					#  The leading lines are the leading matching lines.  The 
					# trailing lines are the trailing matching lines.  The 
					# middle lines are all other new lines.  We will color at 
					# least all the middle lines.  There may be no middle 
					# lines if we delete lines.

					#@-at
					#@@c

					min_len = min(old_len,new_len)
					
					i = 0
					while i < min_len:
						if old_lines[i] != new_lines[i]:
							break
						i += 1
					leading_lines = i
					
					if leading_lines == new_len:
						# All lines match, and we must color _everything_.
						# (several routine delete, then insert the text again,
						# deleting all tags in the process).
						# print "recolor all"
						leading_lines = trailing_lines = 0
					else:
						i = 0
						while i < min_len - leading_lines:
							if old_lines[old_len-i-1] != new_lines[new_len-i-1]:
								break
							i += 1
						trailing_lines = i
					
					#@-body
					#@-node:1::<< compute leading, middle & trailing  lines >>

					
				middle_lines = new_len - leading_lines - trailing_lines
				# print "middle lines", middle_lines
				
				
				#@<< clear leading_lines if middle lines involve @color or @recolor  >>
				#@+node:2::<< clear leading_lines if middle lines involve @color or @recolor  >>
				#@+body
				#@+at
				#  11/19/02: Changing @color or @nocolor directives requires 
				# we recolor all leading states as well.

				#@-at
				#@@c

				if trailing_lines == 0:
					m1 = new_lines[leading_lines:]
					m2 = old_lines[leading_lines:]
				else:
					m1 = new_lines[leading_lines:-trailing_lines]
					m2 = old_lines[leading_lines:-trailing_lines]
				m1.extend(m2) # m1 now contains all old and new middle lines.
				if m1:
					for s in m1:
						i = skip_ws(s,0)
						if match_word(s,i,"@color") or match_word(s,i,"@nocolor"):
							leading_lines = 0
							break
				
				#@-body
				#@-node:2::<< clear leading_lines if middle lines involve @color or @recolor  >>

				
				#@<< initialize new states >>
				#@+node:3::<< initialize new states >>
				#@+body
				# Copy the leading states from the old to the new lines.
				i = 0
				while i < leading_lines and i < old_len: # 12/8/02
					new_states.append(old_states[i])
					i += 1
					
				# We know the starting state of the first middle line!
				if middle_lines > 0 and i < old_len:
					new_states.append(old_states[i])
					i += 1
					
				# Set the state of all other middle lines to "unknown".
				first_trailing_line = new_len - trailing_lines
				while i < first_trailing_line:
					new_states.append("unknown")
					i += 1
				
				# Copy the trailing states from the old to the new lines.
				j = old_len - trailing_lines
				while j < old_len and j < len(old_states):
					new_states.append(old_states[j])
					j += 1
					i += 1 # for the assert below.
				
				while j < len(old_states):
					new_states.append("unknown")
					j += 1
					i += 1 # for the assert below.
					
				# A crucial assertion.  If it fails we won't handle continued states properly.
				assert(i == new_len)
					# Step 1 writes leading_lines lines
					# Step 2 writes (new_len - trailing_lines - leading_lines) lines.
					# Step 3 writes trailing_lines lines.
				
				# print "i:", i
				if 0:
					for i in xrange(len(new_lines)):
						print new_states[i],new_lines[i]
				#@-body
				#@-node:3::<< initialize new states >>

				
				#@<< colorize until the states match >>
				#@+node:4::<< colorize until the states match >>
				#@+body
				# Colorize until the states match.
				# All middle lines have "unknown" state, so they will all be colored.
				
				# Start in the state _after_ the last leading line, which may be unknown.
				i = leading_lines
				while i > 0:
					if i < old_len and i < new_len:
						state = new_states[i]
						assert(state!="unknown")
						break
					else:
						i -= 1
				
				if i == 0:
					# Color plain text unless we are under the control of @nocolor.
					# state = choose(self.flag,"normal","nocolor")
					state = self.setFirstLineState()
					new_states[0] = state
				
				# The new_states[] will be "unknown" unless the lines match,
				# so we do not need to compare lines here.
				while i < new_len:
					self.line_index = i + 1
					state = self.colorizeLine(new_lines[i],state)
					i += 1
					# Set the state of the _next_ line.
					if i < new_len and state != new_states[i]:
						new_states[i] = state
					else: break
					
				# Update the ivars
				self.states = new_states
				self.lines = new_lines
				#@-body
				#@-node:4::<< colorize until the states match >>
				#@-body
				#@-node:3::<< incrementally color the text >>

			else:
				
				#@<< non-incrementally color the text >>
				#@+node:4::<< non-incrementally color the text >>
				#@+body
				# trace("non-incremental")
				
				self.line_index = 1 # The Tk line number for indices, as in n.i
				for s in lines:
					state = self.colorizeLine(s,state)
					self.line_index += 1
				
				#@-body
				#@-node:4::<< non-incrementally color the text >>

			if self.redoColoring:
				
				#@<< completely recolor in two passes >>
				#@+node:7::<< completely recolor in two passes >>
				#@+body
				# This code is executed only if graphics characters will be inserted by user markup code.
				
				# Pass 1:  Insert all graphics characters.
				
				self.removeAllImages()
				s = self.body.get("1.0","end")
				lines = s.split('\n')
				
				self.color_pass = 1
				self.line_index = 1
				state = self.setFirstLineState()
				for s in lines:
					state = self.colorizeLine(s,state)
					self.line_index += 1
				
				# Pass 2: Insert one blank for each previously inserted graphic.
				
				self.color_pass = 2
				self.line_index = 1
				state = self.setFirstLineState()
				for s in lines:
					
					#@<< kludge: insert a blank in s for every image in the line >>
					#@+node:1::<< kludge: insert a blank in s for every image in the line >>
					#@+body
					#@+at
					#  A spectacular kludge.
					# 
					# Images take up a real index, yet the get routine does 
					# not return any character for them!
					# In order to keep the colorer in synch, we must insert 
					# dummy blanks in s at the positions corresponding to each image.

					#@-at
					#@@c

					inserted = 0
					
					for photo,image,line_index,i in self.image_references:
						if self.line_index == line_index:
							n = i+inserted ; 	inserted += 1
							s = s[:n] + ' ' + s[n:]
					
					#@-body
					#@-node:1::<< kludge: insert a blank in s for every image in the line >>

					state = self.colorizeLine(s,state)
					self.line_index += 1
				
				#@-body
				#@-node:7::<< completely recolor in two passes >>

			
			#@<< update state ivars >>
			#@+node:5::<< update state ivars >>
			#@+body
			self.last_flag = self.flag
			self.last_language = self.language
			self.last_comment = self.comment_string
			self.last_markup = self.markup_string
			#@-body
			#@-node:5::<< update state ivars >>

		except:
			
			#@<< set state ivars to "unknown" >>
			#@+node:6::<< set state ivars to "unknown" >>
			#@+body
			self.last_flag = "unknown"
			self.last_language = "unknown"
			self.last_comment = "unknown"
			#@-body
			#@-node:6::<< set state ivars to "unknown" >>

			es_exception()
	#@-body
	#@-node:4::colorizeAnyLanguage & allies
	#@+node:5::colorizeLine & allies
	#@+body
	def colorizeLine (self,s,state):
	
		# print "line,inc,state,s:",self.line_index,self.incremental,state,s
	
		if self.incremental:
			self.removeTagsFromLine()
	
		i = 0
		while i < len(s):
			self.progress = i
			func = self.state_dict[state]
			i,state = func(s,i)
	
		return state
	#@-body
	#@+node:1::continueBlockComment
	#@+body
	def continueBlockComment (self,s,i):
		
		j = s.find(self.block_comment_end,i)
	
		if j == -1:
			j = len(s) # The entire line is part of the block comment.
			if self.language=="cweb":
				self.doLatexLine(s,i,j)
			else:
				if not doHook("color-optional-markup",
					colorer=self,v=self.v,s=s,i=i,j=j,colortag="comment"):
					self.tag("comment",i,j)
			return j,"blockComment" # skip the rest of the line.
	
		else:
			# End the block comment.
			k = len(self.block_comment_end)
			if self.language=="cweb" and self.latex_cweb_comments:
				self.doLatexLine(s,i,j)
				self.tag("comment",j,j+k)
			else:
				if not doHook("color-optional-markup",
					colorer=self,v=self.v,s=s,i=i,j=j+k,colortag="comment"):
					self.tag("comment",i,j+k)
			i = j + k
			return i,"normal"
	#@-body
	#@-node:1::continueBlockComment
	#@+node:2::continueSingle/DoubleString
	#@+body
	def continueDoubleString (self,s,i):
		return self.continueString(s,i,'"',"doubleString")
		
	def continueSingleString (self,s,i):
		return self.continueString(s,i,"'","singleString")
	
	# Similar to skip_string.
	def continueString (self,s,i,delim,continueState):
		# trace(delim + s[i:])
		continueFlag = choose(self.language=="html",true,false)
		j = i
		while i < len(s) and s[i] != delim:
			if s[i:] == "\\":
				i = len(s) ; continueFlag = true ; break
			elif s[i] == "\\":
				i += 2
			else:
				i += 1
		if i >= len(s):
			i = len(s)
		elif s[i] == delim:
			i += 1 ; continueFlag = false
		self.tag("string",j,i)
		state = choose(continueFlag,continueState,"normal")
		return i,state
	#@-body
	#@-node:2::continueSingle/DoubleString
	#@+node:3::continueDocPart
	#@+body
	def continueDocPart (self,s,i):
		
		state = "doc"
		if self.language == "cweb":
			
			#@<< handle cweb doc part >>
			#@+node:1::<< handle cweb doc part >>
			#@+body
			word = self.getCwebWord(s,i)
			if word and len(word) > 0:
				j = i + len(word)
				if word in ("@<","@(","@c","@d","@f","@p"):
					state = "normal" # end the doc part and rescan
				else:
					# The control code does not end the doc part.
					self.tag("keyword",i,j)
					i = j
					if word in ("@^","@.","@:","@="): # Ended by "@>"
						j = s.find("@>",i)
						if j > -1:
							self.tag("cwebName",i,j)
							self.tag("nameBrackets",j,j+2)
							i = j + 2
			elif match(s,i,self.lb):
				j = self.doNowebSecRef(s,i)
				if j == i + 2: # not a section ref.
					self.tag("docPart",i,j)
				i = j
			elif self.latex_cweb_docs:
				# Everything up to the next "@" is latex colored.
				j = s.find("@",i+1)
				if j == -1: j = len(s)
				self.doLatexLine(s,i,j)
				i = j
			else:
				# Everthing up to the next "@" is in the doc part.
				j = s.find("@",i+1)
				if j == -1: j = len(s)
				self.tag("docPart",i,j)
				i = j
			#@-body
			#@-node:1::<< handle cweb doc part >>

		else:
			
			#@<< handle noweb doc part >>
			#@+node:2::<< handle noweb doc part >>
			#@+body
			if i == 0 and match(s,i,"<<"):
				# Possible section definition line.
				return i,"normal" # rescan the line.
			
			if i == 0 and s[i] == '@':
				j = self.skip_id(s,i+1,chars='-')
				word = s[i:j]
				word = word.lower()
			else:
				word = ""
			
			if word in ["@c","@code","@unit","@root","@root-code","@root-doc","@color","@nocolor"]:
				# End of the doc part.
				self.body.tag_remove("docPart",self.index(i),self.index(j))
				self.tag("leoKeyword",i,j)
				i = j ; state = "normal"
			else:
				# The entire line is in the doc part.
				j = len(s)
				if not doHook("color-optional-markup",
					colorer=self,v=self.v,s=s,i=i,j=j,colortag="docPart"):
					self.tag("docPart",i,j)
				i = j # skip the rest of the line.
			
			#@-body
			#@-node:2::<< handle noweb doc part >>

		return i,state
	#@-body
	#@-node:3::continueDocPart
	#@+node:4::continueNocolor
	#@+body
	def continueNocolor (self,s,i):
	
		if i == 0 and s[i] == '@':
			j = self.skip_id(s,i+1)
			word = s[i:j]
			word = word.lower()
		else:
			word = ""
		
		if word == "@color" and self.language != "plain":
			# End of the nocolor part.
			self.tag("leoKeyword",0,j)
			return i,"normal"
		else:
			# The entire line is in the nocolor part.
			# Add tags for blanks and tabs to make "Show Invisibles" work.
			for ch in s[i:]:
				if ch == ' ':
					self.tag("blank",i,i+1)
				elif ch == '\t':
					self.tag("tab",i,i+1)
				i += 1
			return i,"nocolor"
	#@-body
	#@-node:4::continueNocolor
	#@+node:5::continueSingle/DoublePythonString
	#@+body
	def continueDoublePythonString (self,s,i):
		j = s.find('"""',i)
		return self.continuePythonString(s,i,j,"string3d")
	
	def continueSinglePythonString (self,s,i):
		j = s.find("'''",i)
		return self.continuePythonString(s,i,j,"string3s")
	
	def continuePythonString (self,s,i,j,continueState):
	
		if j == -1: # The entire line is part of the triple-quoted string.
			j = len(s)
			if continueState == "string3d":
				if not doHook("color-optional-markup",
					colorer=self,v=self.v,s=s,i=i,j=j,colortag="string"):
					self.tag("string",i,j)
			else:
				self.tag("string",i,j)
			return j,continueState # skip the rest of the line.
	
		else: # End the string
			if continueState == "string3d":
				if not doHook("color-optional-markup",
					colorer=self,v=self.v,s=s,i=i,j=j,colortag="string"):
					self.tag("string",i,j+3)
				else:
					self.tag("string",i,j+3)
			else:
				self.tag("string",i,j+3)
			return j+3,"normal"
	#@-body
	#@-node:5::continueSingle/DoublePythonString
	#@+node:6::doAtKeyword: NOT for cweb keywords
	#@+body
	# Handles non-cweb keyword.
	
	def doAtKeyword (self,s,i):
	
		j = self.skip_id(s,i+1,chars="-") # to handle @root-code, @root-doc
		word = s[i:j]
		word = word.lower()
		if i != 0 and word != "@others":
			word = "" # can't be a Leo keyword, even if it looks like it.
		
		# 7/8/02: don't color doc parts in plain text.
		if self.language != "plain" and (word == "@" or word == "@doc"):
			# at-space is a Leo keyword.
			self.tag("leoKeyword",i,j)
			k = len(s) # Everything on the line is in the doc part.
			if not doHook("color-optional-markup",
				colorer=self,v=self.v,s=s,i=j,j=k,colortag="docPart"):
				self.tag("docPart",j,k)
			return k,"doc"
		elif word == "@nocolor":
			# Nothing on the line is colored.
			self.tag("leoKeyword",i,j)
			return j,"nocolor"
		elif word in leoKeywords:
			self.tag("leoKeyword",i,j)
			return j,"normal"
		else:
			return j,"normal"
	#@-body
	#@-node:6::doAtKeyword: NOT for cweb keywords
	#@+node:7::doLatexLine
	#@+body
	# Colorize the line from i to j.
	
	def doLatexLine (self,s,i,j):
	
		while i < j:
			if match(s,i,"\\"):
				k = self.skip_id(s,i+1)
				word = s[i:k]
				if word in latex_keywords:
					self.tag("latexModeKeyword",i,k)
				i = k
			else:
				self.tag("latexModeBackground",i,i+1)
				i += 1
	#@-body
	#@-node:7::doLatexLine
	#@+node:8::doNormalState
	#@+body
	## To do: rewrite using dynamically generated tables.
	
	def doNormalState (self,s,i):
	
		ch = s[i] ; state = "normal"
	
		if ch in string.letters or ch == '_' or (
			(ch == '\\' and self.language=="latex") or
			(ch in '/&<>' and self. language=="html")):
			
			#@<< handle possible keyword >>
			#@+node:1::Valid regardless of latex mode
			#@+node:1::<< handle possible  keyword >>
			#@+body
			if self.language == "latex":
				
				#@<< handle possible latex keyword >>
				#@+node:1::<< handle possible latex keyword >>
				#@+body
				if match(s,i,"\\"):
					j = self.skip_id(s,i+1)
					word = s[i:j]
					if word in latex_keywords:
						self.tag("latexKeyword",i,j)
					else:
						self.tag("latexBackground",i,j)
				else:
					self.tag("latexBackground",i,i+1)
					j = i + 1 # skip the character.
				#@-body
				#@-node:1::<< handle possible latex keyword >>

			elif self.language == "html":
				
				#@<< handle possible html keyword >>
				#@+node:2::<< handle possible html keyword >>
				#@+body
				if match(s,i,"<!---") or match(s,i,"<!--"):
					if match(s,i,"<!---"): k = 5
					else: k = 4
					self.tag("comment",i,i+k)
					j = i + k ; state = "blockComment"
				elif match(s,i,"<"):
					if match(s,i,"</"): k = 2
					else: k = 1
					j = self.skip_id(s,i+k)
					self.tag("keyword",i,j)
				elif match(s,i,"&"):
					j = self.skip_id(s,i+1,';')
					self.tag("keyword",i,j)
				elif match(s,i,"/>"):
					j = i + 2
					self.tag("keyword",i,j)
				elif match(s,i,">"):
					j = i + 1
					self.tag("keyword",i,j)
				else:
					j = i + 1
				
				#@-body
				#@-node:2::<< handle possible html keyword >>

			else:
				
				#@<< handle general keyword >>
				#@+node:3::<< handle general keyword >>
				#@+body
				j = self.skip_id(s,i)
				word = s[i:j]
				if word in self.keywords:
					self.tag("keyword",i,j)
				elif self.language == "php":
					if word in php_paren_keywords and match(s,j,"()"):
						self.tag("keyword",i,j+2)
						j += 2
				
				#@-body
				#@-node:3::<< handle general keyword >>

			i = j
			#@-body
			#@-node:1::<< handle possible  keyword >>
			#@-node:1::Valid regardless of latex mode

		elif match(s,i,self.lb):
			i = self.doNowebSecRef(s,i)
		elif ch == '@':
			
			#@<< handle at keyword >>
			#@+node:1::Valid regardless of latex mode
			#@+node:2::<< handle at keyword >>
			#@+body
			if self.language == "cweb":
				if match(s,i,"@(") or match(s,i,"@<"):
					
					#@<< handle cweb ref or def >>
					#@+node:2::<< handle cweb ref or def >>
					#@+body
					self.tag("nameBrackets",i,i+2)
					
					# See if the line contains the right name bracket.
					j = s.find("@>=",i+2)
					k = choose(j==-1,2,3)
					if j == -1:
						j = s.find("@>",i+2)
					
					if j == -1:
						i += 2
					else:
						self.tag("cwebName",i+2,j)
						self.tag("nameBrackets",j,j+k)
						i = j + k
					
					#@-body
					#@-node:2::<< handle cweb ref or def >>

				else:
					word = self.getCwebWord(s,i)
					if word:
						
						#@<< Handle cweb control word >>
						#@+node:1::<< Handle cweb control word >>
						#@+body
						# Color and skip the word.
						assert(self.language=="cweb")
						
						j = i + len(word)
						self.tag("keyword",i,j)
						i = j
						
						if word in ("@ ","@\t","@\n","@*","@**"):
							state = "doc"
						elif word in ("@<","@(","@c","@d","@f","@p"):
							state = "normal"
						elif word in ("@^","@.","@:","@="): # Ended by "@>"
							j = s.find("@>",i)
							if j > -1:
								self.tag("cwebName",i,j)
								self.tag("nameBrackets",j,j+2)
								i = j + 2
						#@-body
						#@-node:1::<< Handle cweb control word >>

					else:
						i,state = self.doAtKeyword(s,i)
			else:
				i,state = self.doAtKeyword(s,i)
			#@-body
			#@-node:2::<< handle at keyword >>
			#@-node:1::Valid regardless of latex mode

		elif match(s,i,self.single_comment_start):
			
			#@<< handle single-line comment >>
			#@+node:1::Valid regardless of latex mode
			#@+node:3::<< handle single-line comment >>
			#@+body
			# print "single-line comment i,s:",i,s
			
			if self.language == "cweb" and self.latex_cweb_comments:
				j = i + len(self.single_comment_start)
				self.tag("comment",i,j)
				self.doLatexLine(s,j,len(s))
				i = len(s)
			else:
				j = len(s)
				if not doHook("color-optional-markup",
					colorer=self,v=self.v,s=s,i=i,j=j,colortag="comment"):
					self.tag("comment",i,j)
				i = j
			#@-body
			#@-node:3::<< handle single-line comment >>
			#@-node:1::Valid regardless of latex mode

		elif match(s,i,self.block_comment_start):
			
			#@<< start block comment >>
			#@+node:1::Valid regardless of latex mode
			#@+node:4::<< start block comment >>
			#@+body
			k = len(self.block_comment_start)
			
			if not doHook("color-optional-markup",
				colorer=self,v=self.v,s=s,i=i,j=i+k,colortag="comment"):
				self.tag("comment",i,i+k)
			
			i += k ; state = "blockComment"
			#@-body
			#@-node:4::<< start block comment >>
			#@-node:1::Valid regardless of latex mode

		elif ch == '%' and self.language=="cweb":
			
			#@<< handle latex line >>
			#@+node:1::Valid regardless of latex mode
			#@+node:5::<< handle latex line >>
			#@+body
			self.tag("keyword",i,i+1)
			i += 1 # Skip the %
			self.doLatexLine(s,i,len(s))
			i = len(s)
			#@-body
			#@-node:5::<< handle latex line >>
			#@-node:1::Valid regardless of latex mode

		elif self.language=="latex":
			
			#@<< handle latex normal character >>
			#@+node:2::Vaid only in latex mode
			#@+node:1::<< handle latex normal character >>
			#@+body
			if self.language=="cweb":
				self.tag("latexModeBackground",i,i+1)
			else:
				self.tag("latexBackground",i,i+1)
			i += 1
			#@-body
			#@-node:1::<< handle latex normal character >>
			#@-node:2::Vaid only in latex mode

		# ---- From here on self.language != "latex" -----
		elif ch in self.string_delims:
			
			#@<< handle string >>
			#@+node:3::Valid when not in latex_mode
			#@+node:1::<< handle string >>
			#@+body
			if self.language == "python":
			
				delim = s[i:i+3]
				j, state = self.skip_python_string(s,i)
				if delim == '"""':
					# Only handle wiki items in """ strings.
					if not doHook("color-optional-markup",
						colorer=self,v=self.v,s=s,i=i,j=j,colortag="string"):
						self.tag("string",i,j)
				else:
					self.tag("string",i,j)
				i = j
			
			else:
				j, state = self.skip_string(s,i)
				self.tag("string",i,j)
				i = j
			
			#@-body
			#@-node:1::<< handle string >>
			#@-node:3::Valid when not in latex_mode

		elif ch == '#' and self.has_pp_directives:
			
			#@<< handle C preprocessor line >>
			#@+node:3::Valid when not in latex_mode
			#@+node:2::<< handle C preprocessor line >>
			#@+body
			# 10/17/02: recognize comments in preprocessor lines.
			j = i
			while i < len(s):
				if match(s,i,self.single_comment_start) or match(s,i,self.block_comment_start):
					break
				else: i += 1
			
			self.tag("pp",j,i)
			#@-body
			#@-node:2::<< handle C preprocessor line >>
			#@-node:3::Valid when not in latex_mode

		elif self.language == "php" and (match(s,i,"<") or match(s,i,"?")):
			
			#@<< handle special php keywords >>
			#@+node:3::Valid when not in latex_mode
			#@+node:3::<< handle special php keywords >>
			#@+body
			if match(s,i,"<?php"):
				self.tag("keyword",i,i+5)
				i += 5
			elif match(s,i,"?>"):
				self.tag("keyword",i,i+2)
				i += 2
			else:
				i += 1
			
			#@-body
			#@-node:3::<< handle special php keywords >>
			#@-node:3::Valid when not in latex_mode

		elif ch == ' ':
			
			#@<< handle blank >>
			#@+node:3::Valid when not in latex_mode
			#@+node:4::<< handle blank >>
			#@+body
			if self.showInvisibles:
				self.tag("blank",i,i+1)
			i += 1
			#@-body
			#@-node:4::<< handle blank >>
			#@-node:3::Valid when not in latex_mode

		elif ch == '\t':
			
			#@<< handle tab >>
			#@+node:3::Valid when not in latex_mode
			#@+node:5::<< handle tab >>
			#@+body
			if self.showInvisibles:
				self.tag("tab",i,i+1)
			#print "tab",i,self.body.cget("tabs"),self.body.tag_config("tab")
			i += 1
			#@-body
			#@-node:5::<< handle tab >>
			#@-node:3::Valid when not in latex_mode

		else:
			
			#@<< handle normal character >>
			#@+node:3::Valid when not in latex_mode
			#@+node:6::<< handle normal character >>
			#@+body
			# self.tag("normal",i,i+1)
			i += 1
			#@-body
			#@-node:6::<< handle normal character >>
			#@-node:3::Valid when not in latex_mode

	
		assert(self.progress < i)
		return i,state
	
	#@-body
	#@+node:1::Valid regardless of latex mode
	#@-node:1::Valid regardless of latex mode
	#@+node:2::Vaid only in latex mode
	#@-node:2::Vaid only in latex mode
	#@+node:3::Valid when not in latex_mode
	#@-node:3::Valid when not in latex_mode
	#@-node:8::doNormalState
	#@+node:9::doNowebSecRef
	#@+body
	def doNowebSecRef (self,s,i):
	
		self.tag("nameBrackets",i,i+2)
		
		# See if the line contains the right name bracket.
		j = s.find(self.rb+"=",i+2)
		k = choose(j==-1,2,3)
		if j == -1:
			j = s.find(self.rb,i+2)
		if j == -1:
			return i + 2
		else:
			searchName = self.body.get(self.index(i),self.index(j+k)) # includes brackets
			ref = findReference(searchName,self.v)
			if ref:
				self.tag("link",i+2,j)
				if self.use_hyperlinks:
					
					#@<< set the hyperlink >>
					#@+node:1::<< set the hyperlink >>
					#@+body
					# Set the bindings to vnode callbacks.
					# Create the tag.
					# Create the tag name.
					tagName = "hyper" + `self.hyperCount`
					self.hyperCount += 1
					self.body.tag_delete(tagName)
					self.tag(tagName,i+2,j)
					ref.tagName = tagName
					self.body.tag_bind(tagName,"<Control-1>",ref.OnHyperLinkControlClick)
					self.body.tag_bind(tagName,"<Any-Enter>",ref.OnHyperLinkEnter)
					self.body.tag_bind(tagName,"<Any-Leave>",ref.OnHyperLinkLeave)
					#@-body
					#@-node:1::<< set the hyperlink >>

			elif k == 3: # a section definition
				self.tag("link",i+2,j)
			else:
				self.tag("name",i+2,j)
			self.tag("nameBrackets",j,j+k)
			return j + k
	#@-body
	#@-node:9::doNowebSecRef
	#@+node:10::removeAllTags & removeTagsFromLines
	#@+body
	def removeAllTags (self):
		
		# Warning: the following DOES NOT WORK: self.body.tag_delete(self.tags)
		for tag in self.tags:
			self.body.tag_delete(tag)
	
		for tag in self.color_tags_list:
			self.body.tag_delete(tag)
		
	def removeTagsFromLine (self):
		
		# print "removeTagsFromLine",self.line_index
		for tag in self.tags:
			self.body.tag_remove(tag,self.index(0),self.index("end"))
			
		for tag in self.color_tags_list:
			self.body.tag_remove(tag,self.index(0),self.index("end"))
	#@-body
	#@-node:10::removeAllTags & removeTagsFromLines
	#@-node:5::colorizeLine & allies
	#@+node:6::scanColorDirectives
	#@+body
	def scanColorDirectives(self,v):
		
		"""Scan vnode v and v's ancestors looking for @color and @nocolor directives,
		setting corresponding colorizer ivars.
		"""
	
		c = self.commands
		language = c.target_language
		self.language = language # 2/2/03
		self.comment_string = None
		self.rootMode = None # None, "code" or "doc"
		while v:
			s = v.t.bodyString
			dict = get_directives_dict(s)
			
			#@<< Test for @comment or @language >>
			#@+node:1::<< Test for @comment or @language >>
			#@+body
			# 10/17/02: @comment and @language may coexist in the same node.
			
			if dict.has_key("comment"):
				k = dict["comment"]
				self.comment_string = s[k:]
			
			if dict.has_key("language"):
				i = dict["language"]
				language,junk,junk,junk = set_language(s,i)
				self.language = language # 2/2/03
			
			if dict.has_key("comment") or dict.has_key("language"):
				break
			#@-body
			#@-node:1::<< Test for @comment or @language >>

			
			#@<< Test for @root, @root-doc or @root-code >>
			#@+node:2::<< Test for @root, @root-doc or @root-code >>
			#@+body
			if dict.has_key("root") and not self.rootMode:
			
				k = dict["root"]
				if match_word(s,k,"@root-code"):
					self.rootMode = "code"
				elif match_word(s,k,"@root-doc"):
					self.rootMode = "doc"
				else:
					doc = app().config.at_root_bodies_start_in_doc_mode
					self.rootMode = choose(doc,"doc","code")
			
			#@-body
			#@-node:2::<< Test for @root, @root-doc or @root-code >>

			v = v.parent()
		return self.language # For use by external routines.
	
	#@-body
	#@-node:6::scanColorDirectives
	#@+node:7::color.schedule
	#@+body
	def schedule(self,v,body,incremental=0):
	
		if self.enabled:
			self.incremental=incremental
			body.after_idle(self.idle_colorize,v,body)
			
	def idle_colorize(self,v,body):
	
		# trace(`v` + ", " + `body`)
		if v and body and self.enabled:
			self.colorize(v,body,self.incremental)
	#@-body
	#@-node:7::color.schedule
	#@+node:8::getCwebWord
	#@+body
	def getCwebWord (self,s,i):
		
		# trace(get_line(s,i))
		if not match(s,i,"@"):
			return None
		
		ch1 = ch2 = word = None
		if i + 1 < len(s): ch1 = s[i+1]
		if i + 2 < len(s): ch2 = s[i+2]
	
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
	#@-node:8::getCwebWord
	#@+node:9::removeAllImages
	#@+body
	def removeAllImages (self):
		
		for photo,image,line_index,i in self.image_references:
			try:
				index = self.body.index(image)
				# print "removing image at: ", `index`
				self.body.delete(index)
			except:
				pass # The image may have been deleted earlier.
		
		self.image_references = []
	#@-body
	#@-node:9::removeAllImages
	#@+node:10::updateSyntaxColorer
	#@+body
	# self.flag is true unless an unambiguous @nocolor is seen.
	
	def updateSyntaxColorer (self,v):
		
		self.flag = self.useSyntaxColoring(v)
		self.scanColorDirectives(v)
	
	#@-body
	#@-node:10::updateSyntaxColorer
	#@+node:11::useSyntaxColoring
	#@+body
	# Return true if v unless v is unambiguously under the control of @nocolor.
	
	def useSyntaxColoring (self,v):
	
		first = v ; val = true
		while v:
			s = v.t.bodyString
			dict = get_directives_dict(s)
			no_color = dict.has_key("nocolor")
			color = dict.has_key("color")
			# trace(`dict` + ", " + `v`)
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
	#@-node:11::useSyntaxColoring
	#@+node:12::Utils
	#@+body
	#@+at
	#  These methods are like the corresponding functions in leoGlobals.py 
	# except they issue no error messages.

	#@-at
	#@-body
	#@+node:1::index & tag
	#@+body
	def index (self,i):
		
		return "%s.%s" % (self.line_index,i)
			
	def tag (self,name,i,j):
	
		self.body.tag_add(name,self.index(i),self.index(j))
	#@-body
	#@-node:1::index & tag
	#@+node:2::setFirstLineState
	#@+body
	def setFirstLineState (self):
		
		if self.flag:
			if self.rootMode:
				state = choose(self.rootMode=="code","normal","doc")
			else:
				state = "normal"
		else:
			state = "nocolor"
	
		return state
	#@-body
	#@-node:2::setFirstLineState
	#@+node:3::skip_id
	#@+body
	def skip_id(self,s,i,chars=None):
	
		n = len(s)
		while i < n:
			ch = s[i]
			if ch in string.letters or ch in string.digits or ch == '_':
				i += 1
			elif chars and ch in chars:
				i += 1
			else: break
		return i
	
	#@-body
	#@-node:3::skip_id
	#@+node:4::skip_python_string
	#@+body
	def skip_python_string(self,s,i):
	
		delim = s[i:i+3]
		if delim == "'''" or delim == '"""':
			k = s.find(delim,i+3)
			if k == -1:
				return len(s),choose(delim=="'''","string3s","string3d")
			else:
				return k+3, "normal"
		else:
			return self.skip_string(s,i)
	#@-body
	#@-node:4::skip_python_string
	#@+node:5::skip_string
	#@+body
	def skip_string(self,s,i):
	
		delim = s[i] ; i += 1
		assert(delim == '"' or delim == "'")
		n = len(s)
		while i < n and s[i] != delim:
			if s[i:] == "\\":
				return n,choose(delim=="'","singleString","doubleString")
			elif s[i] == '\\' :
				i += 2
			else: i += 1
	
		if i >= n:
			if self.language=="html":
				return n,"doubleString"
			else:
				return n, "normal"
		elif s[i] == delim:
			i += 1
		return i,"normal"
	
	#@-body
	#@-node:5::skip_string
	#@-node:12::Utils
	#@-others

	
class colorizer (baseColorizer):
	"""Leo's syntax colorer class"""
	pass
#@-body
#@-node:6::class colorizer
#@-others
#@-body
#@-node:0::@file leoColor.py
#@-leo
