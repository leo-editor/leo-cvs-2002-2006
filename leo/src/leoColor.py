#@+leo-ver=4
#@+node:@file leoColor.py
"""Syntax coloring routines for Leo."""

#@@language python

import leoGlobals as g
from leoGlobals import true,false

import re
import string

# php_re = re.compile("<?(\s|=|[pP][hH][pP])")
php_re = re.compile("<?(\s[pP][hH][pP])")

#@<< define leo keywords >>
#@+node:<< define leo keywords >>
# leoKeywords is used by directivesKind, so it should be a module-level symbol.

# leoKeywords must be a list so that plugins may alter it.

leoKeywords = [
	"@","@c","@code","@color","@comment",
	"@delims","@doc","@encoding","@end_raw",
	"@first","@header","@ignore",
	"@language","@last","@lineending",
	"@nocolor","@noheader","@nowrap","@others",
	"@pagewidth","@path","@quiet","@raw","@root","@root-code","@root-doc",
	"@silent","@tabwidth","@terse",
	"@unit","@verbose","@wrap" ]
#@nonl
#@-node:<< define leo keywords >>
#@nl
#@<< define colorizer constants >>
#@+node:<< define colorizer constants >>
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
#@nonl
#@-node:<< define colorizer constants >>
#@nl

#@+others
#@+node:class colorizer
class baseColorizer:
	"""The base class for Leo's syntax colorer."""
	#@	<< define colorizer keywords >>
	#@+node:<< define colorizer keywords >> colorizer
	#@+others
	#@+node:actionscript keywords
	actionscript_keywords = [
	#Jason 2003-07-03 
	#Actionscript keywords for Leo adapted from UltraEdit syntax highlighting
	"break", "call", "continue", "delete", "do", "else", "false", "for", "function", "goto", "if", "in", "new", "null", "return", "true", "typeof", "undefined", "var", "void", "while", "with", "#include", "catch", "constructor", "prototype", "this", "try", "_parent", "_root", "__proto__", "ASnative", "abs", "acos", "appendChild", "asfunction", "asin", "atan", "atan2", "attachMovie", "attachSound", "attributes", "BACKSPACE", "CAPSLOCK", "CONTROL", "ceil", "charAt", "charCodeAt", "childNodes", "chr", "cloneNode", "close", "concat", "connect", "cos", "createElement", "createTextNode", "DELETEKEY", "DOWN", "docTypeDecl", "duplicateMovieClip", "END", "ENTER", "ESCAPE", "enterFrame", "entry", "equal", "eval", "evaluate", "exp", "firstChild", "floor", "fromCharCode", "fscommand", "getAscii", "getBeginIndex", "getBounds", "getBytesLoaded", "getBytesTotal", "getCaretIndex", "getCode", "getDate", "getDay", "getEndIndex", "getFocus", "getFullYear", "getHours", "getMilliseconds", "getMinutes", "getMonth", "getPan", "getProperty", "getRGB", "getSeconds", "getTime", "getTimer", "getTimezoneOffset", "getTransform", "getURL", "getUTCDate", "getUTCDay", "getUTCFullYear", "getUTCHours", "getUTCMilliseconds", "getUTCMinutes", "getUTCMonth", "getUTCSeconds", "getVersion", "getVolume", "getYear", "globalToLocal", "gotoAndPlay", "gotoAndStop", "HOME", "haschildNodes", "hide", "hitTest", "INSERT", "Infinity", "ifFrameLoaded", "ignoreWhite", "indexOf", "insertBefore", "int", "isDown", "isFinite", "isNaN", "isToggled", "join", "keycode", "keyDown", "keyUp", "LEFT", "LN10", "LN2", "LOG10E", "LOG2E", "lastChild", "lastIndexOf", "length", "load", "loaded", "loadMovie", "loadMovieNum", "loadVariables", "loadVariablesNum", "localToGlobal", "log", "MAX_VALUE", "MIN_VALUE", "max", "maxscroll", "mbchr", "mblength", "mbord", "mbsubstring", "min", "NEGATIVE_INFINITY", "NaN", "newline", "nextFrame", "nextScene", "nextSibling", "nodeName", "nodeType", "nodeValue", "on", "onClipEvent", "onClose", "onConnect", "onData", "onLoad", "onXML", "ord", "PGDN", "PGUP", "PI", "POSITIVE_INFINITY", "parentNode", "parseFloat", "parseInt", "parseXML", "play", "pop", "pow", "press", "prevFrame", "previousSibling", "prevScene", "print", "printAsBitmap", "printAsBitmapNum", "printNum", "push", "RIGHT", "random", "release", "removeMovieClip", "removeNode", "reverse", "round", "SPACE", "SQRT1_2", "SQRT2", "scroll", "send", "sendAndLoad", "set", "setDate", "setFocus", "setFullYear", "setHours", "setMilliseconds", "setMinutes", "setMonth", "setPan", "setProperty", "setRGB", "setSeconds", "setSelection", "setTime", "setTransform", "setUTCDate", "setUTCFullYear", "setUTCHours", "setUTCMilliseconds", "setUTCMinutes", "setUTCMonth", "setUTCSeconds", "setVolume", "setYear", "shift", "show", "sin", "slice", "sort", "start", "startDrag", "status", "stop", "stopAllSounds", "stopDrag", "substr", "substring", "swapDepths", "splice", "split", "sqrt", "TAB", "tan", "targetPath", "tellTarget", "toggleHighQuality", "toLowerCase", "toString", "toUpperCase", "trace", "UP", "UTC", "unescape", "unloadMovie", "unLoadMovieNum", "unshift", "updateAfterEvent", "valueOf", "xmlDecl", "_alpha", "_currentframe", "_droptarget", "_focusrect", "_framesloaded", "_height", "_highquality", "_name", "_quality", "_rotation", "_soundbuftime", "_target", "_totalframes", "_url", "_visible", "_width", "_x", "_xmouse", "_xscale", "_y", "_ymouse", "_yscale", "and", "add", "eq", "ge", "gt", "le", "lt", "ne", "not", "or", "Array", "Boolean", "Color", "Date", "Key", "Math", "MovieClip", "Mouse", "Number", "Object", "Selection", "Sound", "String", "XML", "XMLSocket"
	]
	#@nonl
	#@-node:actionscript keywords
	#@+node:c# keywords
	csharp_keywords = [
		"abstract","as",
		"base","bool","break","byte",
		"case","catch","char","checked","class","const","continue",
		"decimal","default","delegate","do","double",
		"else","enum","event","explicit","extern",
		"false","finally","fixed","float","for","foreach",
		"get","goto",
		"if","implicit","in","int","interface","internal","is",
		"lock","long",
		"namespace","new","null",
		"object","operator","out","override",
		"params","partial","private","protected","public",
		"readonly","ref","return",
		"sbyte","sealed","set","short","sizeof","stackalloc",
		"static","string","struct","switch",
		"this","throw","true","try","typeof",
		"uint","ulong","unchecked","unsafe","ushort","using",
		"value","virtual","void","volatile",
		"where","while",
		"yield"]
	#@nonl
	#@-node:c# keywords
	#@+node:c/c++ keywords
	c_keywords = [
		# C keywords
		"auto","break","case","char","continue",
		"default","do","double","else","enum","extern",
		"float","for","goto","if","int","long","register","return",
		"short","signed","sizeof","static","struct","switch",
		"typedef","union","unsigned","void","volatile","while",
		# C++ keywords
		"asm","bool","catch","class","const","const_cast",
		"delete","dynamic_cast","explicit","false","friend",
		"inline","mutable","namespace","new","operator",
		"private","protected","public","reinterpret_cast","static_cast",
		"template","this","throw","true","try",
		"typeid","typename","using","virtual","wchar_t"]
	#@nonl
	#@-node:c/c++ keywords
	#@+node:css keywords
	css_keywords = [
	#html tags
	"address", "applet", "area", "a", "base", "basefont",
	"big", "blockquote", "body", "br", "b", "caption", "center",
	"cite", "code", "dd", "dfn", "dir", "div", "dl", "dt", "em", "font",
	"form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "hr", "html", "img",
	"input", "isindex", "i", "kbd", "link", "li", "link", "map", "menu",
	"meta", "ol", "option", "param", "pre", "p", "samp",
	"select", "small", "span", "strike", "strong", "style", "sub", "sup",
	"table", "td", "textarea", "th", "title", "tr", "tt", "ul", "u", "var",
	#units
	"mm", "cm", "in", "pt", "pc", "em", "ex", "px",
	#colors
	"aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow", "white",
	#important directive
	"!important",
	#font rules
	"font", "font-family", "font-style", "font-variant", "font-weight", "font-size",
	#font values
	"cursive", "fantasy", "monospace", "normal", "italic", "oblique", "small-caps",
	"bold", "bolder", "lighter", "medium", "larger", "smaller",
	"serif", "sans-serif",
	#background rules
	"background", "background-color", "background-image", "background-repeat", "background-attachment", "background-position",
	#background values
	"contained", "none", "top", "center", "bottom", "left", "right", "scroll", "fixed",
	"repeat", "repeat-x", "repeat-y", "no-repeat",
	#text rules
	"word-spacing", "letter-spacing", "text-decoration", "vertical-align", "text-transform", "text-align", "text-indent", "text-transform", "text-shadow", "unicode-bidi", "line-height",
	#text values
	"normal", "none", "underline", "overline", "blink", "sub", "super", "middle", "top", "text-top", "text-bottom",
	"capitalize", "uppercase", "lowercase", "none", "left", "right", "center", "justify",
	"line-through",
	#box rules
	"margin", "margin-top", "margin-bottom", "margin-left", "margin-right",
	"margin", "padding-top", "padding-bottom", "padding-left", "padding-right",
	"border", "border-width", "border-style", "border-top", "border-top-width", "border-top-style", "border-bottom", "border-bottom-width", "border-bottom-style", "border-left", "border-left-width", "border-left-style", "border-right", "border-right-width", "border-right-style", "border-color",
	#box values
	"width", "height", "float", "clear",
	"auto", "thin", "medium", "thick", "left", "right", "none", "both",
	"none", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset",
	#display rules
	"display", "white-space", 
	"min-width", "max-width", "min-height", "max-height",
	"outline-color", "outline-style", "outline-width",
	#display values
	"run-in", "inline-block", "list-item", "block", "inline", "none", "normal", "pre", "nowrap", "table-cell", "table-row", "table-row-group", "table-header-group", "inline-table", "table-column", "table-column-group", "table-cell", "table-caption"
	#list rules
	"list-style", "list-style-type", "list-style-image", "list-style-position",
	#list values
	"disc", "circle", "square", "decimal", "decimal-leading-zero", "none",
	"lower-roman", "upper-roman", "lower-alpha", "upper-alpha", "lower-latin", "upper-latin",
	#table rules
	"border-collapse", "caption-side",
	#table-values
	"empty-cells", "table-layout",
	#misc values/rules
	"counter-increment", "counter-reset",
	"marker-offset", "z-index",
	"cursor", "direction", "marks", "quotes",
	"clip", "content", "orphans", "overflow", "visibility",
	#aural rules
	"pitch", "range", "pitch-during", "cue-after", "pause-after", "cue-before", "pause-before", "speak-header", "speak-numeral", "speak-punctuation", "speed-rate", "play-during", "voice-family",
	#aural values
	"stress", "azimuth", "elevation", "pitch", "richness", "volume",
	"page-break", "page-after", "page-inside"]
	#@nonl
	#@-node:css keywords
	#@+node:elisp keywords
	# EKR: needs more work.
	elisp_keywords = [
		# Maybe...
		"error","princ",
		# More typical of other lisps...
		"apply","eval",
		"t","nil",
		"and","or","not",
		"cons","car","cdr",
		"cond",
		"defconst","defun","defvar",
		"eq","ne","equal","gt","ge","lt","le",
		"if",
		"let",
		"mapcar",
		"prog","progn",
		"set","setq",
		"type-of",
		"unless",
		"when","while"]
	#@nonl
	#@-node:elisp keywords
	#@+node:html keywords
	# No longer used by syntax colorer.
	html_keywords = []
	
	if 0: # Not used at present.
		unused_keywords = [
			# html constructs.
			"a","body","cf",
			"h1","h2","h3","h4","h5","h6",
			"head","html","hr",
			"i","img","li","lu","meta",
			"p","title","ul",
			# Common tags
			"caption","col","colgroup",
			"table","tbody","td","tfoot","th","thead","tr",
			"script","style"]
	
		html_specials = [ "<%","%>" ]
	#@nonl
	#@-node:html keywords
	#@+node:java keywords
	java_keywords = [
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
		"var","void","volatile","while"]
	#@nonl
	#@-node:java keywords
	#@+node:latex keywords
	#If you see two idenitical words, with minor capitalization differences
	#DO NOT ASSUME that they are the same word. For example \vert produces
	#a single vertical line and \Vert produces a double vertical line
	#Marcus A. Martin.
	
	latex_special_keyword_characters = "@(){}%"
	
	latex_keywords = [
		#special keyworlds
		"\\%", # 11/9/03
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
		"\\zeta" ]
	#@nonl
	#@-node:latex keywords
	#@+node:pascal keywords
	pascal_keywords = [
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
		"exports","property","default","write","stored","index","name" ]
	#@nonl
	#@-node:pascal keywords
	#@+node:perl keywords
	perl_keywords = [
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
		"sort","system","syscall","unlink","utime","warn"]
	#@nonl
	#@-node:perl keywords
	#@+node:php keywords
	php_keywords = [ # 08-SEP-2002 DTHEIN
		"__CLASS__", "__FILE__", "__FUNCTION__", "__LINE__",
		"and", "as", "break",
		"case", "cfunction", "class", "const", "continue",
		"declare", "default", "do",
		"else", "elseif", "enddeclare", "endfor", "endforeach",
		"endif", "endswitch",  "endwhile", "eval", "extends",
		"for", "foreach", "function", "global", "if",
		"new", "old_function", "or", "static", "switch",
		"use", "var", "while", "xor" ]
		
	# The following are supposed to be followed by ()
	php_paren_keywords = [
		"array", "die", "echo", "empty", "exit",
		"include", "include_once", "isset", "list",
		"print", "require", "require_once", "return",
		"unset" ]
		
	# The following are handled by special case code:
	# "<?php", "?>"
	#@-node:php keywords
	#@+node:python keywords
	python_keywords = [
		"and",       "del",       "for",       "is",        "raise",    
		"assert",    "elif",      "from",      "lambda",    "return",   
		"break",     "else",      "global",    "not",       "try",      
		"class",     "except",    "if",        "or",        "yield",   
		"continue",  "exec",      "import",    "pass",      "while",
		"def",       "finally",   "in",        "print"]
	#@nonl
	#@-node:python keywords
	#@+node:rapidq keywords
	rapidq_keywords = [
	# Syntax file for RapidQ
	"$APPTYPE","$DEFINE","$ELSE","$ENDIF","$ESCAPECHARS","$IFDEF","$IFNDEF",
	"$INCLUDE","$MACRO","$OPTIMIZE","$OPTION","$RESOURCE","$TYPECHECK","$UNDEF",
	"ABS","ACOS","ALIAS","AND","AS","ASC","ASIN","ATAN","ATN","BIN$","BIND","BYTE",
	"CALL","CALLBACK","CALLFUNC","CASE","CEIL","CHDIR","CHDRIVE","CHR$","CINT",
	"CLNG","CLS","CODEPTR","COMMAND$","COMMANDCOUNT","CONSOLE","CONST","CONSTRUCTOR",
	"CONVBASE$","COS","CREATE","CSRLIN","CURDIR$","DATA","DATE$","DEC","DECLARE",
	"DEFBYTE","DEFDBL","DEFDWORD","DEFINT","DEFLNG","DEFSHORT","DEFSNG","DEFSTR",
	"DEFWORD","DELETE$","DIM","DIR$","DIREXISTS","DO","DOEVENTS","DOUBLE","DWORD",
	"ELSE","ELSEIF","END","ENVIRON","ENVIRON$","EVENT","EXIT","EXP","EXTENDS",
	"EXTRACTRESOURCE","FIELD$","FILEEXISTS","FIX","FLOOR","FOR","FORMAT$","FRAC",
	"FUNCTION","FUNCTIONI","GET$","GOSUB","GOTO","HEX$","IF","INC","INITARRAY",
	"INKEY$","INP","INPUT","INPUT$","INPUTHANDLE","INSERT$","INSTR","INT","INTEGER",
	"INV","IS","ISCONSOLE","KILL","KILLMESSAGE","LBOUND","LCASE$","LEFT$","LEN",
	"LFLUSH","LIB","LIBRARYINST","LOCATE","LOG","LONG","LOOP","LPRINT","LTRIM$",
	"MEMCMP","MESSAGEBOX","MESSAGEDLG","MID$","MKDIR","MOD","MOUSEX","MOUSEY",
	"NEXT","NOT","OFF","ON","OR","OUT","OUTPUTHANDLE","PARAMSTR$","PARAMSTRCOUNT",
	"PARAMVAL","PARAMVALCOUNT","PCOPY","PEEK","PLAYWAV","POKE","POS","POSTMESSAGE",
	"PRINT","PROPERTY","QUICKSORT","RANDOMIZE","REDIM","RENAME","REPLACE$",
	"REPLACESUBSTR$","RESOURCE","RESOURCECOUNT","RESTORE","RESULT","RETURN",
	"REVERSE$","RGB","RIGHT$","RINSTR","RMDIR","RND","ROUND","RTRIM$","RUN",
	"SCREEN","SELECT","SENDER","SENDMESSAGE","SETCONSOLETITLE","SGN","SHELL",
	"SHL","SHORT","SHOWMESSAGE","SHR","SIN","SINGLE","SIZEOF","SLEEP","SOUND",
	"SPACE$","SQR","STACK","STATIC","STEP","STR$","STRF$","STRING","STRING$",
	"SUB","SUBI","SWAP","TALLY","TAN","THEN","TIME$","TIMER","TO","TYPE","UBOUND",
	"UCASE$","UNLOADLIBRARY","UNTIL","VAL","VARIANT","VARPTR","VARPTR$","VARTYPE",
	"WEND","WHILE","WITH","WORD","XOR"]
	#@nonl
	#@-node:rapidq keywords
	#@+node:rebol keywords
	rebol_keywords = [
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
	"email?", "empty?", "equal?", "error?", "even?", "event?", "exists?", "exists-key?",
	"file?", "flag-face?", "found?", "function?",  
	"get-word?", "greater-or-equal?", "greater?",  
	"hash?", "head?",  
	"image?", "in-window?", "index?", "info?", "input?", "inside?", "integer?", "issue?",  
	"length?", "lesser-or-equal?", "lesser?", "library?", "link-app?", "link?", "list?", "lit-path?", "lit-word?", "logic?",  
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
	]
	#@nonl
	#@-node:rebol keywords
	#@+node:shell keywords
	shell_keywords = [
		# reserved keywords
		"case","do","done","elif","else","esac","fi",
		"for","if","in","then",
		"until","while",
		"break","cd","chdir","continue","eval","exec",
		"exit","kill","newgrp","pwd","read","readonly",
		"return","shift","test","trap","ulimit",
		"umask","wait" ]
	#@nonl
	#@-node:shell keywords
	#@+node:tcl/tk keywords
	tcltk_keywords = [ # Only the tcl keywords are here.
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
		"while" ]
	#@nonl
	#@-node:tcl/tk keywords
	#@-others
	
	cweb_keywords = c_keywords
	perlpod_keywords = perl_keywords
	#@nonl
	#@-node:<< define colorizer keywords >> colorizer
	#@nl
	#@	@+others
	#@+node:color.__init__
	def disable (self):
	
		print "disabling all syntax coloring"
		self.enabled=false
	
	def __init__(self,c):
	
		self.c = c
		self.frame = c.frame
		self.body = c.frame.body
	
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
		#@	<< ivars for communication between colorAllDirectives and its allies >>
		#@+node:<< ivars for communication between colorAllDirectives and its allies >>
		# Copies of arguments.
		self.p = None
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
		
		config = g.app.config
		self.latex_cweb_docs     = config.getBoolColorsPref("color_cweb_doc_parts_with_latex")
		self.latex_cweb_comments = config.getBoolColorsPref("color_cweb_comments_with_latex")
		# print "docs,comments",self.latex_cweb_docs,self.latex_cweb_comments
		#@nonl
		#@-node:<< ivars for communication between colorAllDirectives and its allies >>
		#@nl
		#@	<< define dispatch dicts >>
		#@+node:<< define dispatch dicts >>
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
						
			for ch in string.ascii_letters:
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
		#@nonl
		#@-node:<< define dispatch dicts >>
		#@nl
		#@	<< define fonts and data for wiki tags >>
		#@+node:<< define fonts and data for wiki tags >>
		self.bold_font = config.getFontFromParams(
			"body_text_font_family", "body_text_font_size",
			"body_text_font_slant",  "body_text_font_weight",
			config.defaultBodyFontSize)
		
		if self.bold_font:
			self.bold_font.configure(weight="bold")
		
		self.italic_font = config.getFontFromParams(
			"body_text_font_family", "body_text_font_size",
			"body_text_font_slant",  "body_text_font_weight",
			config.defaultBodyFontSize)
			
		if self.italic_font:
			self.italic_font.configure(slant="italic",weight="normal")
		
		self.bolditalic_font = config.getFontFromParams(
			"body_text_font_family", "body_text_font_size",
			"body_text_font_slant",  "body_text_font_weight",
			config.defaultBodyFontSize)
			
		if self.bolditalic_font:
			self.bolditalic_font.configure(weight="bold",slant="italic")
		
		self.color_tags_list = []
		self.image_references = []
		#@-node:<< define fonts and data for wiki tags >>
		#@nl
	#@nonl
	#@-node:color.__init__
	#@+node:colorize & recolor_range
	# The main colorizer entry point.
	
	def colorize(self,p,incremental=false):
	
		if self.enabled:
			# g.trace("incremental",incremental)
			self.incremental=incremental
			self.updateSyntaxColorer(p)
			return self.colorizeAnyLanguage(p)
		else:
			return "ok" # For unit testing.
			
	# Called from incremental undo code.
	# Colorizes the lines between the leading and trailing lines.
			
	def recolor_range(self,p,leading,trailing):
		
		if self.enabled:
			# g.trace("leading,trailing",leading,trailing)
			self.incremental=true
			self.updateSyntaxColorer(p)
			return self.colorizeAnyLanguage(p,leading=leading,trailing=trailing)
		else:
			return "ok" # For unit testing.
	#@nonl
	#@-node:colorize & recolor_range
	#@+node:colorizeAnyLanguage & allies
	def colorizeAnyLanguage (self,p,leading=None,trailing=None):
		
		"""Color the body pane either incrementally or non-incrementally"""
		
		# g.trace("incremental",self.incremental,p)
		try:
			#@		<< initialize ivars & tags >>
			#@+node:<< initialize ivars & tags >> colorizeAnyLanguage
			# Add any newly-added user keywords.
			for d in g.globalDirectiveList:
				name = '@' + d
				if name not in leoKeywords:
					leoKeywords.append(name)
			
			# Copy the arguments.
			self.p = p
			
			# Get the body text, converted to unicode.
			s = self.body.getAllText() # 10/27/03
			self.sel = sel = self.body.getInsertionPoint() # 10/27/03
			start,end = self.body.convertIndexToRowColumn(sel) # 10/27/03
			
			# g.trace(self.language)
			# g.trace(self.count,self.p)
			# g.trace(body.tag_names())
			
			if not self.incremental:
				self.removeAllTags()
				self.removeAllImages()
			
			self.redoColoring = false
			self.redoingColoring = false
			
			#@<< configure tags >>
			#@+node:<< configure tags >>
			config = g.app.config
			assert(config)
			
			for name in default_colors_dict.keys(): # Python 2.1 support.
				option_name,default_color = default_colors_dict[name]
				option_color = config.getColorsPref(option_name)
				color = g.choose(option_color,option_color,default_color)
				# Must use foreground, not fg.
				try:
					self.body.tag_configure(name, foreground=color)
				except: # Recover after a user error.
					self.body.tag_configure(name, foreground=default_color)
			
			underline_undefined = config.getBoolColorsPref("underline_undefined_section_names")
			use_hyperlinks      = config.getBoolColorsPref("use_hyperlinks")
			self.use_hyperlinks = use_hyperlinks
			
			# underline=var doesn't seem to work.
			if 0: # use_hyperlinks: # Use the same coloring, even when hyperlinks are in effect.
				self.body.tag_configure("link",underline=1) # defined
				self.body.tag_configure("name",underline=0) # undefined
			else:
				self.body.tag_configure("link",underline=0)
				if underline_undefined:
					self.body.tag_configure("name",underline=1)
				else:
					self.body.tag_configure("name",underline=0)
					
			# 8/4/02: we only create tags for whitespace when showing invisibles.
			if self.showInvisibles:
				for name,option_name,default_color in (
					("blank","show_invisibles_space_background_color","Gray90"),
					("tab",  "show_invisibles_tab_background_color",  "Gray80")):
					option_color = config.getColorsPref(option_name)
					color = g.choose(option_color,option_color,default_color)
					try:
						self.body.tag_configure(name,background=color)
					except: # Recover after a user error.
						self.body.tag_configure(name,background=default_color)
				
			# 11/15/02: Colors for latex characters.  Should be user options...
			
			if 1: # Alas, the selection doesn't show if a background color is specified.
				self.body.tag_configure("latexModeBackground",foreground="black")
				self.body.tag_configure("latexModeKeyword",foreground="blue")
				self.body.tag_configure("latexBackground",foreground="black")
				self.body.tag_configure("latexKeyword",foreground="blue")
			else: # Looks cool, and good for debugging.
				self.body.tag_configure("latexModeBackground",foreground="black",background="seashell1")
				self.body.tag_configure("latexModeKeyword",foreground="blue",background="seashell1")
				self.body.tag_configure("latexBackground",foreground="black",background="white")
				self.body.tag_configure("latexKeyword",foreground="blue",background="white")
				
			# Tags for wiki coloring.
			if self.showInvisibles:
				self.body.tag_configure("elide",background="yellow")
			else:
				self.body.tag_configure("elide",elide="1")
			self.body.tag_configure("bold",font=self.bold_font)
			self.body.tag_configure("italic",font=self.italic_font)
			self.body.tag_configure("bolditalic",font=self.bolditalic_font)
			for name in self.color_tags_list:
				self.body.tag_configure(name,foreground=name)
			#@nonl
			#@-node:<< configure tags >>
			#@nl
			#@<< configure language-specific settings >>
			#@+node:<< configure language-specific settings >> colorizer
			# Define has_string, keywords, single_comment_start, block_comment_start, block_comment_end.
			
			if self.language == "cweb": # Use C comments, not cweb sentinel comments.
				delim1,delim2,delim3 = g.set_delims_from_language("c")
			elif self.comment_string:
				delim1,delim2,delim3 = g.set_delims_from_string(self.comment_string)
			elif self.language == "plain": # 1/30/03
				delim1,delim2,delim3 = None,None,None
			else:
				delim1,delim2,delim3 = g.set_delims_from_language(self.language)
			
			self.single_comment_start = delim1
			self.block_comment_start = delim2
			self.block_comment_end = delim3
			
			# A strong case can be made for making this code as fast as possible.
			# Whether this is compatible with general language descriptions remains to be seen.
			self.has_string = self.language != "plain"
			if self.language == "plain":
				self.string_delims = ()
			elif self.language in ("elisp","html"):
				self.string_delims = ('"')
			else:
				self.string_delims = ("'",'"')
			self.has_pp_directives = self.language in ("c","csharp","cweb","latex")
			
			# The list of languages for which keywords exist.
			# Eventually we might just use language_delims_dict.keys()
			languages = [
				"actionscript","c","csharp","css","cweb","elisp","html","java","latex",
				"pascal","perl","perlpod","php","python","rapidq","rebol","shell","tcltk"]
			
			self.keywords = []
			if self.language == "cweb":
				for i in self.c_keywords:
					self.keywords.append(i)
				for i in self.cweb_keywords:
					self.keywords.append(i)
			else:
				for name in languages:
					if self.language==name: 
						# g.trace("setting keywords for",name)
						self.keywords = getattr(self, name + "_keywords")
			
			# Color plain text unless we are under the control of @nocolor.
			# state = g.choose(self.flag,"normal","nocolor")
			state = self.setFirstLineState()
			
			if 1: # 10/25/02: we color both kinds of references in cweb mode.
				self.lb = "<<"
				self.rb = ">>"
			else:
				self.lb = g.choose(self.language == "cweb","@<","<<")
				self.rb = g.choose(self.language == "cweb","@>",">>")
			#@nonl
			#@-node:<< configure language-specific settings >> colorizer
			#@nl
			
			self.hyperCount = 0 # Number of hypertext tags
			self.count += 1
			lines = string.split(s,'\n')
			#@nonl
			#@-node:<< initialize ivars & tags >> colorizeAnyLanguage
			#@nl
			g.doHook("init-color-markup",colorer=self,v=self.p)
			self.color_pass = 0
			if self.incremental and (
				#@			<< all state ivars match >>
				#@+node:<< all state ivars match >>
				self.flag == self.last_flag and
				self.last_language == self.language and
				self.comment_string == self.last_comment and
				self.markup_string == self.last_markup
				#@nonl
				#@-node:<< all state ivars match >>
				#@afterref
 ):
				#@			<< incrementally color the text >>
				#@+node:<< incrementally color the text >>
				#@+at  
				#@nonl
				# Each line has a starting state.  The starting state for the 
				# first line is always "normal".
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
				
				# g.trace("incremental")
				
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
					#@	<< compute leading, middle & trailing lines >>
					#@+node:<< compute leading, middle & trailing  lines >>
					#@+at 
					#@nonl
					# The leading lines are the leading matching lines.  The 
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
					#@-node:<< compute leading, middle & trailing  lines >>
					#@nl
					
				middle_lines = new_len - leading_lines - trailing_lines
				# print "middle lines", middle_lines
				
				#@<< clear leading_lines if middle lines involve @color or @recolor  >>
				#@+node:<< clear leading_lines if middle lines involve @color or @recolor  >>
				#@+at 
				#@nonl
				# 11/19/02: Changing @color or @nocolor directives requires we 
				# recolor all leading states as well.
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
						s = g.toUnicode(s,g.app.tkEncoding) # 10/28/03
						i = g.skip_ws(s,0)
						if g.match_word(s,i,"@color") or g.match_word(s,i,"@nocolor"):
							leading_lines = 0
							break
				#@-node:<< clear leading_lines if middle lines involve @color or @recolor  >>
				#@nl
				#@<< initialize new states >>
				#@+node:<< initialize new states >>
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
				first_trailing_line = max(0,new_len - trailing_lines)
				while i < first_trailing_line:
					new_states.append("unknown")
					i += 1
				
				# Copy the trailing states from the old to the new lines.
				i = max(0,old_len - trailing_lines)
				while i < old_len and i < len(old_states):
					new_states.append(old_states[i])
					i += 1
				
				# 1/8/03: complete new_states by brute force.
				while len(new_states) < new_len:
					new_states.append("unknown")
				#@nonl
				#@-node:<< initialize new states >>
				#@nl
				#@<< colorize until the states match >>
				#@+node:<< colorize until the states match >>
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
					# state = g.choose(self.flag,"normal","nocolor")
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
				#@nonl
				#@-node:<< colorize until the states match >>
				#@nl
				#@nonl
				#@-node:<< incrementally color the text >>
				#@nl
			else:
				#@			<< non-incrementally color the text >>
				#@+node:<< non-incrementally color the text >>
				# g.trace("non-incremental",self.language)
				
				self.line_index = 1 # The Tk line number for indices, as in n.i
				for s in lines:
					state = self.colorizeLine(s,state)
					self.line_index += 1
				#@-node:<< non-incrementally color the text >>
				#@nl
			if self.redoColoring:
				#@			<< completely recolor in two passes >>
				#@+node:<< completely recolor in two passes >>
				# This code is executed only if graphics characters will be inserted by user markup code.
				
				# Pass 1:  Insert all graphics characters.
				
				self.removeAllImages()
				s = self.body.getAllText() # 10/27/03
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
					#@	<< kludge: insert a blank in s for every image in the line >>
					#@+node:<< kludge: insert a blank in s for every image in the line >>
					#@+at 
					#@nonl
					# A spectacular kludge.
					# 
					# Images take up a real index, yet the get routine does 
					# not return any character for them!
					# In order to keep the colorer in synch, we must insert 
					# dummy blanks in s at the positions corresponding to each 
					# image.
					#@-at
					#@@c
					
					inserted = 0
					
					for photo,image,line_index,i in self.image_references:
						if self.line_index == line_index:
							n = i+inserted ; 	inserted += 1
							s = s[:n] + ' ' + s[n:]
					#@-node:<< kludge: insert a blank in s for every image in the line >>
					#@nl
					state = self.colorizeLine(s,state)
					self.line_index += 1
				#@-node:<< completely recolor in two passes >>
				#@nl
			#@		<< update state ivars >>
			#@+node:<< update state ivars >>
			self.last_flag = self.flag
			self.last_language = self.language
			self.last_comment = self.comment_string
			self.last_markup = self.markup_string
			#@nonl
			#@-node:<< update state ivars >>
			#@nl
			return "ok" # for testing.
		except:
			#@		<< set state ivars to "unknown" >>
			#@+node:<< set state ivars to "unknown" >>
			self.last_flag = "unknown"
			self.last_language = "unknown"
			self.last_comment = "unknown"
			#@nonl
			#@-node:<< set state ivars to "unknown" >>
			#@nl
			if self.c:
				g.es_exception()
			else:
				import traceback ; traceback.print_exc()
			return "error" # for unit testing.
	#@-node:colorizeAnyLanguage & allies
	#@+node:colorizeLine & allies
	def colorizeLine (self,s,state):
	
		# print "line,inc,state,s:",self.line_index,self.incremental,state,s
		s = g.toUnicode(s,g.app.tkEncoding) # 10/28/03
	
		if self.incremental:
			self.removeTagsFromLine()
	
		i = 0
		while i < len(s):
			self.progress = i
			func = self.state_dict[state]
			i,state = func(s,i)
	
		return state
	#@nonl
	#@-node:colorizeLine & allies
	#@+node:continueBlockComment
	def continueBlockComment (self,s,i):
		
		j = s.find(self.block_comment_end,i)
	
		if j == -1:
			j = len(s) # The entire line is part of the block comment.
			if self.language=="cweb":
				self.doLatexLine(s,i,j)
			else:
				if not g.doHook("color-optional-markup",
					colorer=self,v=self.p,s=s,i=i,j=j,colortag="comment"):
					self.tag("comment",i,j)
			return j,"blockComment" # skip the rest of the line.
	
		else:
			# End the block comment.
			k = len(self.block_comment_end)
			if self.language=="cweb" and self.latex_cweb_comments:
				self.doLatexLine(s,i,j)
				self.tag("comment",j,j+k)
			else:
				if not g.doHook("color-optional-markup",
					colorer=self,v=self.p,s=s,i=i,j=j+k,colortag="comment"):
					self.tag("comment",i,j+k)
			i = j + k
			return i,"normal"
	#@nonl
	#@-node:continueBlockComment
	#@+node:continueSingle/DoubleString
	def continueDoubleString (self,s,i):
		return self.continueString(s,i,'"',"doubleString")
		
	def continueSingleString (self,s,i):
		return self.continueString(s,i,"'","singleString")
	
	# Similar to skip_string.
	def continueString (self,s,i,delim,continueState):
		# g.trace(delim + s[i:])
		continueFlag = g.choose(self.language in ("elisp","html"),true,false)
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
		state = g.choose(continueFlag,continueState,"normal")
		return i,state
	#@nonl
	#@-node:continueSingle/DoubleString
	#@+node:continueDocPart
	def continueDocPart (self,s,i):
		
		state = "doc"
		if self.language == "cweb":
			#@		<< handle cweb doc part >>
			#@+node:<< handle cweb doc part >>
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
			elif g.match(s,i,self.lb):
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
			#@nonl
			#@-node:<< handle cweb doc part >>
			#@nl
		else:
			#@		<< handle noweb doc part >>
			#@+node:<< handle noweb doc part >>
			if i == 0 and g.match(s,i,"<<"):
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
				self.body.tag_remove("docPart",self.index(i),self.index(j)) # 10/27/03
				self.tag("leoKeyword",i,j)
				i = j ; state = "normal"
			else:
				# The entire line is in the doc part.
				j = len(s)
				if not g.doHook("color-optional-markup",
					colorer=self,v=self.p,s=s,i=i,j=j,colortag="docPart"):
					self.tag("docPart",i,j)
				i = j # skip the rest of the line.
			#@-node:<< handle noweb doc part >>
			#@nl
		return i,state
	#@nonl
	#@-node:continueDocPart
	#@+node:continueNocolor
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
	#@nonl
	#@-node:continueNocolor
	#@+node:continueSingle/DoublePythonString
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
				if not g.doHook("color-optional-markup",
					colorer=self,v=self.p,s=s,i=i,j=j,colortag="string"):
					self.tag("string",i,j)
			else:
				self.tag("string",i,j)
			return j,continueState # skip the rest of the line.
	
		else: # End the string
			if continueState == "string3d":
				if not g.doHook("color-optional-markup",
					colorer=self,v=self.p,s=s,i=i,j=j,colortag="string"):
					self.tag("string",i,j+3)
				else:
					self.tag("string",i,j+3)
			else:
				self.tag("string",i,j+3)
			return j+3,"normal"
	#@nonl
	#@-node:continueSingle/DoublePythonString
	#@+node:doAtKeyword: NOT for cweb keywords
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
			if not g.doHook("color-optional-markup",
				colorer=self,v=self.p,s=s,i=j,j=k,colortag="docPart"):
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
	#@nonl
	#@-node:doAtKeyword: NOT for cweb keywords
	#@+node:doLatexLine
	# Colorize the line from i to j.
	
	def doLatexLine (self,s,i,j):
	
		while i < j:
			if g.match(s,i,"\\"):
				k = self.skip_id(s,i+1)
				word = s[i:k]
				if word in self.latex_keywords:
					self.tag("latexModeKeyword",i,k)
				i = k
			else:
				self.tag("latexModeBackground",i,i+1)
				i += 1
	#@nonl
	#@-node:doLatexLine
	#@+node:doNormalState
	## To do: rewrite using dynamically generated tables.
	
	def doNormalState (self,s,i):
	
		ch = s[i] ; state = "normal"
		assert(type(ch)==type(u""))
	
		if ch in string.ascii_letters or ch == '_' or (
			(ch == '\\' and self.language=="latex") or
			(ch in '/&<>' and self.language=="html") or
			(ch == '$' and self.language=="rapidq")
		):
			#@		<< handle possible keyword >>
			#@+node:<< handle possible  keyword >>
			if self.language == "latex":
				#@	<< handle possible latex keyword >>
				#@+node:<< handle possible latex keyword >>
				if g.match(s,i,"\\"):
					j = self.skip_id(s,i+1,chars=self.latex_special_keyword_characters) # 11/9/03
					word = s[i:j]
					if word in self.latex_keywords:
						self.tag("latexKeyword",i,j)
					else:
						self.tag("latexBackground",i,j)
				else:
					self.tag("latexBackground",i,i+1)
					j = i + 1 # skip the character.
				#@nonl
				#@-node:<< handle possible latex keyword >>
				#@nl
			elif self.language == "html":
				#@	<< handle possible html keyword >>
				#@+node:<< handle possible html keyword >>
				if g.match(s,i,"<!---") or g.match(s,i,"<!--"):
					if g.match(s,i,"<!---"): k = 5
					else: k = 4
					self.tag("comment",i,i+k)
					j = i + k ; state = "blockComment"
				elif g.match(s,i,"<"):
					if g.match(s,i,"</"): k = 2
					else: k = 1
					j = self.skip_id(s,i+k)
					self.tag("keyword",i,j)
				elif g.match(s,i,"&"):
					j = self.skip_id(s,i+1,';')
					self.tag("keyword",i,j)
				elif g.match(s,i,"/>"):
					j = i + 2
					self.tag("keyword",i,j)
				elif g.match(s,i,">"):
					j = i + 1
					self.tag("keyword",i,j)
				else:
					j = i + 1
				#@-node:<< handle possible html keyword >>
				#@nl
			else:
				#@	<< handle general keyword >>
				#@+node:<< handle general keyword >>
				if self.language == "rapidq":
					j = self.skip_id(s,i+1,chars="$")
				elif self.language == "rebol":
					j = self.skip_id(s,i+1,chars="-~!?")
				elif self.language in ("elisp","css"):
					j = self.skip_id(s,i+1,chars="-")
				else:
					j = self.skip_id(s,i)
				
				word = s[i:j]
				if word in self.keywords:
					self.tag("keyword",i,j)
				elif self.language == "php":
					if word in self.php_paren_keywords and g.match(s,j,"()"):
						self.tag("keyword",i,j+2)
						j += 2
				#@nonl
				#@-node:<< handle general keyword >>
				#@nl
			i = j
			#@nonl
			#@-node:<< handle possible  keyword >>
			#@nl
		elif g.match(s,i,self.lb):
			i = self.doNowebSecRef(s,i)
		elif ch == '@':
			#@		<< handle at keyword >>
			#@+node:<< handle at keyword >>
			if self.language == "cweb":
				if g.match(s,i,"@(") or g.match(s,i,"@<"):
					#@		<< handle cweb ref or def >>
					#@+node:<< handle cweb ref or def >>
					self.tag("nameBrackets",i,i+2)
					
					# See if the line contains the right name bracket.
					j = s.find("@>=",i+2)
					k = g.choose(j==-1,2,3)
					if j == -1:
						j = s.find("@>",i+2)
					
					if j == -1:
						i += 2
					else:
						self.tag("cwebName",i+2,j)
						self.tag("nameBrackets",j,j+k)
						i = j + k
					#@-node:<< handle cweb ref or def >>
					#@nl
				else:
					word = self.getCwebWord(s,i)
					if word:
						#@			<< Handle cweb control word >>
						#@+node:<< Handle cweb control word >>
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
						#@nonl
						#@-node:<< Handle cweb control word >>
						#@nl
					else:
						i,state = self.doAtKeyword(s,i)
			else:
				i,state = self.doAtKeyword(s,i)
			#@nonl
			#@-node:<< handle at keyword >>
			#@nl
		elif g.match(s,i,self.single_comment_start):
			#@		<< handle single-line comment >>
			#@+node:<< handle single-line comment >>
			# print "single-line comment i,s:",i,s
			
			if self.language == "cweb" and self.latex_cweb_comments:
				j = i + len(self.single_comment_start)
				self.tag("comment",i,j)
				self.doLatexLine(s,j,len(s))
				i = len(s)
			elif self.language == "shell" and (i>0 and s[i-1]=='$'):
				i += 1 # '$#' in shell should not start a comment (DS 040113)
			else:
				j = len(s)
				if not g.doHook("color-optional-markup",
					colorer=self,v=self.p,s=s,i=i,j=j,colortag="comment"):
					self.tag("comment",i,j)
				i = j
			#@nonl
			#@-node:<< handle single-line comment >>
			#@nl
		elif g.match(s,i,self.block_comment_start):
			#@		<< start block comment >>
			#@+node:<< start block comment >>
			k = len(self.block_comment_start)
			
			if not g.doHook("color-optional-markup",
				colorer=self,v=self.p,s=s,i=i,j=i+k,colortag="comment"):
				self.tag("comment",i,i+k)
			
			i += k ; state = "blockComment"
			#@nonl
			#@-node:<< start block comment >>
			#@nl
		elif ch == '%' and self.language=="cweb":
			#@		<< handle latex line >>
			#@+node:<< handle latex line >>
			self.tag("keyword",i,i+1)
			i += 1 # Skip the %
			self.doLatexLine(s,i,len(s))
			i = len(s)
			#@nonl
			#@-node:<< handle latex line >>
			#@nl
		elif self.language=="latex":
			#@		<< handle latex normal character >>
			#@+node:<< handle latex normal character >>
			if self.language=="cweb":
				self.tag("latexModeBackground",i,i+1)
			else:
				self.tag("latexBackground",i,i+1)
			i += 1
			#@nonl
			#@-node:<< handle latex normal character >>
			#@nl
		# ---- From here on self.language != "latex" -----
		elif ch in self.string_delims:
			#@		<< handle string >>
			#@+node:<< handle string >>
			if self.language == "python":
			
				delim = s[i:i+3]
				j, state = self.skip_python_string(s,i)
				if delim == '"""':
					# Only handle wiki items in """ strings.
					if not g.doHook("color-optional-markup",
						colorer=self,v=self.p,s=s,i=i,j=j,colortag="string"):
						self.tag("string",i,j)
				else:
					self.tag("string",i,j)
				i = j
			
			else:
				j, state = self.skip_string(s,i)
				self.tag("string",i,j)
				i = j
			#@-node:<< handle string >>
			#@nl
		elif ch == '#' and self.has_pp_directives:
			#@		<< handle C preprocessor line >>
			#@+node:<< handle C preprocessor line >>
			# 10/17/02: recognize comments in preprocessor lines.
			j = i
			while i < len(s):
				if g.match(s,i,self.single_comment_start) or g.match(s,i,self.block_comment_start):
					break
				else: i += 1
			
			self.tag("pp",j,i)
			#@nonl
			#@-node:<< handle C preprocessor line >>
			#@nl
		elif self.language == "php" and (g.match(s,i,"<") or g.match(s,i,"?")):
			# g.trace("%3d" % i,php_re.match(s,i),s)
			#@		<< handle special php keywords >>
			#@+node:<< handle special php keywords >>
			if g.match(s.lower(),i,"<?php"):
				self.tag("keyword",i,i+5)
				i += 5
			elif g.match(s,i,"?>"):
				self.tag("keyword",i,i+2)
				i += 2
			else:
				i += 1
			
			#@-node:<< handle special php keywords >>
			#@nl
		elif ch == ' ':
			#@		<< handle blank >>
			#@+node:<< handle blank >>
			if self.showInvisibles:
				self.tag("blank",i,i+1)
			i += 1
			#@nonl
			#@-node:<< handle blank >>
			#@nl
		elif ch == '\t':
			#@		<< handle tab >>
			#@+node:<< handle tab >>
			if self.showInvisibles:
				self.tag("tab",i,i+1)
			i += 1
			#@nonl
			#@-node:<< handle tab >>
			#@nl
		else:
			#@		<< handle normal character >>
			#@+node:<< handle normal character >>
			# self.tag("normal",i,i+1)
			i += 1
			#@nonl
			#@-node:<< handle normal character >>
			#@nl
	
		if 0: # This can fail harmlessly when using wxPython plugin.  Don't know exactly why.
			g.trace(self.progress,i,state)
			assert(self.progress < i)
		return i,state
	
	
	#@-node:doNormalState
	#@+node:doNowebSecRef
	def doNowebSecRef (self,s,i):
	
		self.tag("nameBrackets",i,i+2)
		
		# See if the line contains the right name bracket.
		j = s.find(self.rb+"=",i+2)
		k = g.choose(j==-1,2,3)
		if j == -1:
			j = s.find(self.rb,i+2)
		if j == -1:
			return i + 2
		else:
			searchName = self.body.getTextRange(self.index(i),self.index(j+k)) # includes brackets
			ref = g.findReference(searchName,self.p)
			if ref:
				self.tag("link",i+2,j)
				if self.use_hyperlinks:
					#@				<< set the hyperlink >>
					#@+node:<< set the hyperlink >>
					# Set the bindings to vnode callbacks.
					# Create the tag.
					# Create the tag name.
					tagName = "hyper" + str(self.hyperCount)
					self.hyperCount += 1
					self.body.tag_delete(tagName)
					self.tag(tagName,i+2,j)
					
					ref.tagName = tagName
					self.body.tag_bind(tagName,"<Control-1>",ref.OnHyperLinkControlClick)
					self.body.tag_bind(tagName,"<Any-Enter>",ref.OnHyperLinkEnter)
					self.body.tag_bind(tagName,"<Any-Leave>",ref.OnHyperLinkLeave)
					#@nonl
					#@-node:<< set the hyperlink >>
					#@nl
			elif k == 3: # a section definition
				self.tag("link",i+2,j)
			else:
				self.tag("name",i+2,j)
			self.tag("nameBrackets",j,j+k)
			return j + k
	#@nonl
	#@-node:doNowebSecRef
	#@+node:removeAllTags & removeTagsFromLines
	def removeAllTags (self):
		
		# Warning: the following DOES NOT WORK: self.body.tag_delete(self.tags)
		for tag in self.tags:
			self.body.tag_delete(tag) # 10/27/03
	
		for tag in self.color_tags_list:
			self.body.tag_delete(tag) # 10/27/03
		
	def removeTagsFromLine (self):
		
		# print "removeTagsFromLine",self.line_index
		for tag in self.tags:
			self.body.tag_remove(tag,self.index(0),self.index("end")) # 10/27/03
			
		for tag in self.color_tags_list:
			self.body.tag_remove(tag,self.index(0),self.index("end")) # 10/27/03
	#@nonl
	#@-node:removeAllTags & removeTagsFromLines
	#@+node:scanColorDirectives
	def scanColorDirectives(self,p):
		
		"""Scan position p and p's ancestors looking for @color and @nocolor directives,
		setting corresponding colorizer ivars.
		"""
	
		p = p.copy() ; c = self.c
		if c == None: return # self.c may be None for testing.
	
		language = c.target_language
		self.language = language # 2/2/03
		self.comment_string = None
		self.rootMode = None # None, "code" or "doc"
		
		for p in p.self_and_parents_iter():
			# g.trace(p)
			s = p.v.t.bodyString
			dict = g.get_directives_dict(s)
			#@		<< Test for @comment or @language >>
			#@+node:<< Test for @comment or @language >>
			# 10/17/02: @comment and @language may coexist in the same node.
			
			if dict.has_key("comment"):
				k = dict["comment"]
				self.comment_string = s[k:]
			
			if dict.has_key("language"):
				i = dict["language"]
				language,junk,junk,junk = g.set_language(s,i)
				self.language = language # 2/2/03
			
			if dict.has_key("comment") or dict.has_key("language"):
				break
			#@nonl
			#@-node:<< Test for @comment or @language >>
			#@nl
			#@		<< Test for @root, @root-doc or @root-code >>
			#@+node:<< Test for @root, @root-doc or @root-code >>
			if dict.has_key("root") and not self.rootMode:
			
				k = dict["root"]
				if g.match_word(s,k,"@root-code"):
					self.rootMode = "code"
				elif g.match_word(s,k,"@root-doc"):
					self.rootMode = "doc"
				else:
					doc = g.app.config.at_root_bodies_start_in_doc_mode
					self.rootMode = g.choose(doc,"doc","code")
			#@-node:<< Test for @root, @root-doc or @root-code >>
			#@nl
	
		return self.language # For use by external routines.
	#@-node:scanColorDirectives
	#@+node:color.schedule & idle_colorize (not used)
	# At present these are not used.
	
	def schedule(self,p,incremental=0):
	
		if self.enabled:
			self.incremental=incremental
			g.app.gui.setIdleTimeHook(self.idle_colorize,p)
			
	def idle_colorize(self,p):
	
		if p and self.enabled:
			self.colorize(p,self.incremental)
	#@nonl
	#@-node:color.schedule & idle_colorize (not used)
	#@+node:getCwebWord
	def getCwebWord (self,s,i):
		
		# g.trace(g.get_line(s,i))
		if not g.match(s,i,"@"):
			return None
		
		ch1 = ch2 = word = None
		if i + 1 < len(s): ch1 = s[i+1]
		if i + 2 < len(s): ch2 = s[i+2]
	
		if g.match(s,i,"@**"):
			word = "@**"
		elif not ch1:
			word = "@"
		elif not ch2:
			word = s[i:i+2]
		elif (
			(ch1 in string.ascii_letters and not ch2 in string.ascii_letters) or # single-letter control code
			ch1 not in string.ascii_letters # non-letter control code
		):
			word = s[i:i+2]
	
		# if word: g.trace(word)
			
		return word
	#@nonl
	#@-node:getCwebWord
	#@+node:removeAllImages
	def removeAllImages (self):
		
		for photo,image,line_index,i in self.image_references:
			try:
				self.body.deleteCharacter(image) # 10/27/03
			except:
				pass # The image may have been deleted earlier.
		
		self.image_references = []
	#@nonl
	#@-node:removeAllImages
	#@+node:updateSyntaxColorer
	# self.flag is true unless an unambiguous @nocolor is seen.
	
	def updateSyntaxColorer (self,p):
	
		p = p.copy()
		self.flag = self.useSyntaxColoring(p)
		self.scanColorDirectives(p)
	#@-node:updateSyntaxColorer
	#@+node:useSyntaxColoring
	def useSyntaxColoring (self,p):
		
		"""Return true unless p is unambiguously under the control of @nocolor."""
		
		p = p.copy() ; first = p.copy()
		val = true
		for p in p.self_and_parents_iter():
			# g.trace(p)
			s = p.v.t.bodyString
			dict = g.get_directives_dict(s)
			no_color = dict.has_key("nocolor")
			color = dict.has_key("color")
			# A color anywhere in the target enables coloring.
			if color and p == first:
				val = true ; break
			# Otherwise, the @nocolor specification must be unambiguous.
			elif no_color and not color:
				val = false ; break
			elif color and not no_color:
				val = true ; break
	
		return val
	#@-node:useSyntaxColoring
	#@+node:Utils
	#@+at 
	#@nonl
	# These methods are like the corresponding functions in leoGlobals.py 
	# except they issue no error messages.
	#@-at
	#@-node:Utils
	#@+node:index & tag
	def index (self,i):
		
		return self.body.convertRowColumnToIndex(self.line_index,i)
			
	def tag (self,name,i,j):
	
		self.body.tag_add(name,self.index(i),self.index(j))
	#@nonl
	#@-node:index & tag
	#@+node:setFirstLineState
	def setFirstLineState (self):
		
		if self.flag:
			if self.rootMode:
				state = g.choose(self.rootMode=="code","normal","doc")
			else:
				state = "normal"
		else:
			state = "nocolor"
	
		return state
	#@nonl
	#@-node:setFirstLineState
	#@+node:skip_id
	def skip_id(self,s,i,chars=None):
	
		n = len(s)
		while i < n:
			ch = s[i]
			if ch in string.ascii_letters or ch in string.digits or ch == '_':
				i += 1
			elif chars and ch in chars:
				i += 1
			else: break
		return i
	#@-node:skip_id
	#@+node:skip_python_string
	def skip_python_string(self,s,i):
	
		delim = s[i:i+3]
		if delim == "'''" or delim == '"""':
			k = s.find(delim,i+3)
			if k == -1:
				return len(s),g.choose(delim=="'''","string3s","string3d")
			else:
				return k+3, "normal"
		else:
			return self.skip_string(s,i)
	#@nonl
	#@-node:skip_python_string
	#@+node:skip_string
	def skip_string(self,s,i):
	
		delim = s[i] ; i += 1
		assert(delim == '"' or delim == "'")
		n = len(s)
		while i < n and s[i] != delim:
			if s[i:] == "\\":
				return n,g.choose(delim=="'","singleString","doubleString")
			elif s[i] == '\\' :
				i += 2
			else: i += 1
	
		if i >= n:
			if self.language in ("elisp","html"):
				return n,"doubleString"
			else:
				return n, "normal"
		elif s[i] == delim:
			i += 1
		return i,"normal"
	#@-node:skip_string
	#@-others
	
class colorizer (baseColorizer):
	"""Leo's syntax colorer class"""
	pass
#@nonl
#@-node:class colorizer
#@+node:class nullColorizer
class nullColorizer (colorizer):
	
	"""A do-nothing colorer class"""
	
	#@	@+others
	#@+node:__init__
	def __init__ (self,c):
		
		
		self.c = c
	#@-node:__init__
	#@+node:entry points
	def colorize(self,p,incremental=false):
		pass
		
	def idle_colorize(self,p):
		pass
			
	def recolor_range(self,p,leading,trailing):
		pass
	
	def scanColorDirectives(self,p):
		pass
		
	def schedule(self,p,incremental=0):
		pass
	
	def updateSyntaxColorer (self,p):
		pass
	#@nonl
	#@-node:entry points
	#@-others
#@nonl
#@-node:class nullColorizer
#@-others
#@nonl
#@-node:@file leoColor.py
#@-leo
