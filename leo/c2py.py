#! /usr/bin/env python
#@+leo
#@+node:0::@file c2py.py
#@+body
#@@first
#@@language python


#@+at
#  When using c2py as a script to translate entire files, use 
# convertCFileToPython().  When using c2py within Leo, use convertCurrentTree().
# 
# Please set user data in the << specifying user types >> section.

#@-at
#@@c


#@<< what c2py does >>
#@+node:1::Documentation
#@+node:1::<< what c2py does >>
#@+body
#@+at
#  c2py converts C or C++ text into python text.  The conversion is not 
# complete.  Nevertheless, c2py eliminates much of the tedious text 
# manipulation that would otherwise be required.
# 
# The following is a list of the translations performed by c2py.  These 
# transformations are controlled by convertCodeList().
# 
# I.  Prepass
# 
# These translations before removing all curly braces.
# 
# Suppose we are translating:
# 
# 	aTypeSpec aClass::aMethod(t1 v1,...,tn vn)
# 	{
# 		body
# 	}
# 
# 1. Translates the function prototype, i.e., translates:
# 
# 	aTypeSpec aClass::aMethod(t1 v1,...,tn vn)
# to:
# 	def aMethod(v1,...vn):
# 
# As a special case, c2py translates:
# 
# 	aTypeSpec aClass::aClass(t1 v1,...,tn vn)
# to:
# 	aClass.__init__(t1 v1,...,tn vn)
# 
# Yes, I know, aClass.__init__ isn't proper Python, but retaining the class 
# name is useful.
# 
# 2. Let t denote any member of typeList or classList.
# 
# 	a) Removes all casts of the form (t) or (t*) or (t**), etc.
# 	b) Converts t x, t *x, t **x, etc. to x.
# 	c) Converts x = new t(...) to x = t(...)
# 	d) For all i in ivarsDict[aClass] converts this -> i to self.i
# 	e) For all i in ivarsDict[aClass] converts i to self.i
# 
# 3. Converts < < x > > = to @c.  This Leo-specific translation is not done 
# when translating files.
# 
# II.  Main Pass
# 
# This pass does the following simple translations everywhere except in 
# comments and strings.
# 
# Changes all -> to .
# Changes all this.self to self (This corrects problems during the prepass.)
# Removes all curly braces
# Changes all #if to if
# Changes all else if to elif
# Changes all #else to else:
# Changes all else to else:
# Removes all #endif
# Changes all && to and
# Changes all || to or
# Changes all TRUE to true
# Changes all FALSE to false
# Changes all NULL to None
# Changes all this to self
# Changes all @code to @c.  This Leo-specific translation is not done when 
# translating files.
# 
# III.  Complex Pass
# 
# This pass attempts more complex translations.
# 
# Converts if ( x ) to if x:
# Converts elif ( x ) to elif x:
# Converts while ( x ) to while x:
# Converts for ( x ; y ; z ) to for x SEMI y SEMI z:
# 
# remove all semicolons.
# 
# IV.  Final Pass
# 
# This pass completes the translation.
# 
# Removes all semicolons.
# Removes @c if it starts the text.  This Leo-specific translation is not done 
# when translating files.
# Removes all blank lines.
# Removes excess whitespace from all lines, leaving leading whitespace unchanged.
# Replaces C/C++ comments by Python comments.
# Removes trailing whitespace from all lines.

#@-at
#@-body
#@-node:1::<< what c2py does >>
#@-node:1::Documentation


#@<< theory of operation >>
#@+node:1::Documentation
#@+node:2::<< theory of operation >>
#@+body
#@+at
#  Strategy and Performance
# 
# c2py is straightforward.  The speed of c2py is unimportant.  We don't care 
# about the memory used because we translate only small pieces of text at a time.
# 
# We can do body[i:j] = x, regardless of len(x).  We can also do del body[i:j] 
# to delete characters.
# 
# We scan repeatedly through the text.  Using many passes greatly simplifies 
# the code and does not slow down c2py significantly.
# 
# No scans are done within strings or comments.  The idiom to handle such 
# scans is the following:
# 
# def someScan(body):
# 	i = 0
# 	while i < body(len):
# 		if isStringOrComment(body,i):
# 			i = skipStringOrComment(body,i)
# 		elif << found what we are looking for ? >> :
# 			<< convert what we are looking for, setting i >>
# 		else: i += 1
# 
# That's about all there is to it.  The code was remarkably easy to write and 
# seems clear to me.

#@-at
#@-body
#@-node:2::<< theory of operation >>
#@-node:1::Documentation

import string

#@<< specifying user types >>
#@+node:2::<< specifying user types >>
#@+body
#@+at
#  Please change the following lists so they contain the types and classes 
# used by your program.
# 
# c2py removes all type definitions correctly; it converts
# 	new aType(...)
# to
# 	aType(...)

#@-at
#@@c

classList = [
	"vnode", "tnode", "Commands",
	"wxString", "wxTreeCtrl", "wxTextCtrl", "wxSplitterWindow" ]
	
typeList = ["char", "void", "short", "long", "int", "double", "float"]


#@+at
#  Please change ivarsDict so it represents the instance variables (ivars) 
# used by your program's classes.
# 
# ivarsDict is a dictionary used to translate ivar i of class c to self.i.  It 
# also translates this->i to self.i.

#@-at
#@@c
	
ivarsDict = {
	"atFile": [ "mCommands", "mErrors", "mStructureErrors",
		"mTargetFileName", "mOutputFileName", "mOutputStream",
		"mStartSentinelComment", "mEndSentinelComment", "mRoot"],

	"vnode": ["mCommands", "mJoinList", "mIconVal", "mTreeID", "mT", "mStatusBits"],

	"tnode": ["mBodyString", "mBodyRTF", "mJoinHead", "mStatusBits", "mFileIndex",
		"mSelectionStart", "mSelectionLength", "mCloneIndex"],
		
	"LeoFrame": ["mNextFrame", "mPrevFrame", "mCommands"],

	"Commands": [
		# public
		"mCurrentVnode", "mLeoFrame", "mInhibitOnTreeChanged", "mMaxTnodeIndex",
		"mTreeCtrl", "mBodyCtrl", "mFirstWindowAndNeverSaved",
		#private
		"mTabWidth", "mChanged", "mOutlineExpansionLevel", "mUsingClipboard",
		"mFileName", "mMemoryInputStream", "mMemoryOutputStream", "mFileInputStream",
		"mInputFile", "mFileOutputStream", "mFileSize", "mTopVnode", "mTagList",
		"mMaxVnodeTag",
		"mUndoType", "mUndoVnode", "mUndoParent", "mUndoBack", "mUndoN",
		"mUndoDVnodes", "mUndoLastChild", "mUndoablyDeletedVnode" ]}
#@-body
#@-node:2::<< specifying user types >>

true = 1 ; false = None
tabWidth = 4 # how many blanks in a tab.
printFlag = false
doLeoTranslations = true ; dontDoLeoTranslations = false

#@<< define testData >>
#@+node:3::<< define testData >>
#@+body
testData = [ "\n@doc\n\
This is a doc part: format, whilest, {};->.\n\
<<\
section def>>=\n\
LeoFrame::LeoFrame(vnode *v, char *s, int i)\n\
{\n\
	// test ; {} /* */.\n\
	#if 0 //comment\n\
		if(gLeoFrameList)gLeoFrameList -> mPrevFrame = this ;\n\
		else\n\
			this -> mNextFrame = gLeoFrameList ;\n\
	#else\n\
		\n\
		vnode *v = new vnode(a,b);\n\
		Commands *commander = (Commands) NULL ; // after cast\n\
		this -> mPrevFrame = NULL ;\n\
	#endif\n\
	if (a==b)\n\
		a = 2;\n\
	else if (a ==c)\n\
		a = 3;\n\
	else return; \n\
	/* Block comment test:\n\
		if(2):while(1): end.*/\n\
	for(int i = 1; i < limit; ++i){\n\
		mVisible = FALSE ;\n\
		mOnTop = TRUE ;\n\
	}\n\
	// trailing ws.	 \n\
	mCommands = new Commands(this, mTreeCtrl, mTextCtrl) ;\n\
	gActiveFrame = this ;\n\
}\n\
	", "<<" +
"vnode methods >>=\n\
\n\
void vnode::OnCopyNode(wxCommandEvent& WXUNUSED(event))\n\
{\n\
	mCommands -> copyOutline();\n\
}\n\
\n@doc\n\
another doc part if, then, else, -> \n<<" +
"vnode methods >>=\n\
void vnode::OnPasteNode(wxCommandEvent& WXUNUSED(event))\n\
{\n\
	mCommands -> pasteOutline();\n\
}\n" ]
#@-body
#@-node:3::<< define testData >>


#@+others
#@+node:1::Documentation
#@-node:1::Documentation
#@+node:4::speedTest
#@+body
def speedTest(passes):

	import time
	file = r"c:\prog\LeoPy\LeoPy.leo"
	f=open(file)
	if not f:
		print "not found: ", file
		return
	s=f.read()
	f.close()
	print "file:", file, " size:", len(s), " passes:", passes
	print "speedTest start"
	time1 = time.clock()
	p = passes
	while p > 0:
		n = len(s) ; i = 0 ; lines = 0
		while -1 < i < n:
			if s[i] == '\n':
				lines += 1 ; i += 1
			else:
				i = s.find('\n',i) # _much_ faster than list-based-find.
			continue
			# match is about 9 times slower than simple test.
			if s[i]=='\n': # match(s,i,'\n'): # 
				i += 1
			else:
				i += 1
		p -= 1
	time2 = time.clock()
	print "lines:", lines
	print "speedTest done:"
	print "elapsed time:", time2-time1
	print "time/pass:", (time2-time1)/passes
#@-body
#@-node:4::speedTest
#@+node:5::leo1to2
#@+node:1::leo1to2
#@+body
def leo1to2():

	import leo
	import leoGlobals
	c=leoGlobals.top()
	v=c.currentVnode()
	convertLeo1to2(v,c)

#@-body
#@-node:1::leo1to2
#@+node:2::convertLeo1to2
#@+body
def convertLeo1to2(v,c):

	after=v.nodeAfterTree()
	while v and v != after:
		s=v.bodyString()
		print "converting:", v.headString()
		s=convertStringLeo1to2(s)
		v.setBodyStringOrPane(s)
		v=v.threadNext()

	c.Repaint() # for backward compatibility
	print "end of leo1to2"
#@-body
#@-node:2::convertLeo1to2
#@+node:3::convertStringLeo1to2
#@+body
def convertStringLeo1to2 (s):

	# print "convertStringLeo1to2:start\n", s
	codeList = stringToList(s) ; outputList = []
	i = 0
	while i < len(codeList):
		j = skipCodePart(codeList,i)
		if j > i:
			code = codeList[i:j]
			convertCodeList1to2(code)
			i = j
			#print "-----code:", listToString(code)
			for item in code:
				outputList.append(item)
		j = skipDocPart(codeList,i)
		if j > i:
			doc = codeList[i:j]
			convertDocList(doc) # same as in c2py
			#print "-----doc:", listToString(doc)
			i = j
			for item in doc:
				outputList.append(item)
	
	result = listToString(outputList)
	global printFlag
	if printFlag: print "-----:\n", result
	return result
#@-body
#@-node:3::convertStringLeo1to2
#@+node:4::convertCodeList1to2
#@+body
#@+at
#  We do _not_ replace @root by @file or insert @others as needed.  Inserting 
# @others can be done easily enough by hand, and may take more global 
# knowledge than we can reasonably expect to have.

#@-at
#@@c

def convertCodeList1to2(list):

	if 0: # There isn't much reason to do this.
		removeAtRoot(list)
	safeReplace(list, "@code", "@c")
	replaceSectionDefs(list)
	removeLeadingAtCode(list)

#@-body
#@-node:4::convertCodeList1to2
#@-node:5::leo1to2
#@+node:6::c2py entry points
#@+body
#@+at
#  We separate the processing into two parts, 1) a leo-aware driver that 
# iterates over @file trees and 2) a text-based part that processes one or 
# more files or strings.

#@-at
#@-body
#@+node:1::convertCurrentTree
#@+body
def convertCurrentTree():

	import leo
	import leoGlobals
	c=leoGlobals.top()
	v = c.currentVnode()
	c2py.convertLeoTree(v,c)
#@-body
#@-node:1::convertCurrentTree
#@+node:2::convertLeoTree
#@+body
def convertLeoTree(v,c):

	after=v.nodeAfterTree()
	while v and v != after:
		s=v.bodyString()
		print "converting:", v.headString()
		s=convertCStringToPython(s, doLeoTranslations )
		v.setBodyStringOrPane(s)
		v=v.threadNext()
	c.Repaint() # for backward compatibility.
	print "end of c2py"
#@-body
#@-node:2::convertLeoTree
#@+node:3::convertCFileToPython
#@+body
def convertCFileToPython(file):

	f=open(file, 'r')
	if not f: return
	s = f.read()
	f.close();
	f=open(file + ".py", 'w')
	if not f: return
	s = convertCStringToPython(s, dontDoLeoTranslations )
	f.write(s)
	f.close()
#@-body
#@-node:3::convertCFileToPython
#@-node:6::c2py entry points
#@+node:7::c2py Top Level
#@+node:1::convertCStringToPython
#@+body
def convertCStringToPython(s, leoFlag):

	# print "convertCStringToPython:start\n", s
	firstPart = true
	codeList = stringToList(s)
	
	if not leoFlag:
		convertCodeList(codeList, firstPart, dontDoLeoTranslations)
		return listToString(codeList)

	outputList = []
	i = 0
	while i < len(codeList):
		j = skipCodePart(codeList,i)
		if j > i:
			code = codeList[i:j]
			convertCodeList(code, firstPart, doLeoTranslations)
			i = j
			#print "-----code:", listToString(code)
			for item in code:
				outputList.append(item)
		firstPart = false # don't remove @c from here on.
		j = skipDocPart(codeList,i)
		if j > i:
			doc = codeList[i:j]
			convertDocList(doc)
			#print "-----doc:", listToString(doc)
			i = j
			for item in doc:
				outputList.append(item)
	
	result = listToString(outputList)
	global printFlag
	if printFlag: print "-----:\n", result
	return result
#@-body
#@-node:1::convertCStringToPython
#@+node:2::convertCodeList
#@+body
def convertCodeList(list, firstPart, leoFlag):
	#first
	replace(list, "\r", None)
	convertLeadingBlanks(list)
	if leoFlag:
		replaceSectionDefs(list)
	mungeAllFunctions(list)
	#next
	safeReplace(list, " -> ", '.')
	safeReplace(list, "->", '.')
	safeReplace(list, " . ", '.')
	safeReplace(list, "this.self", "self")
	safeReplace(list, "{", None)
	safeReplace(list, "}", None)
	safeReplace(list, "#if", "if")
	safeReplace(list, "#else", "else")
	safeReplace(list, "#endif", None)
	safeReplace(list, "else if", "elif")
	safeReplace(list, "else", "else:")
	safeReplace(list, "&&", "and")
	safeReplace(list, "||", "or")
	safeReplace(list, "TRUE", "true")
	safeReplace(list, "FALSE", "false")
	safeReplace(list, "NULL", "None")
	safeReplace(list, "this", "self")
	safeReplace(list, "try", "try:")
	safeReplace(list, "catch", "except:")
	if leoFlag:
		safeReplace(list, "@code", "@c")
	#next
	handleAllKeywords(list)
	# after processing for keywords
	removeSemicolonsAtEndOfLines(list)
	#last
	if firstPart and leoFlag: removeLeadingAtCode(list)
	removeBlankLines(list)
	removeExcessWs(list)
	# your taste may vary: in Python I don't like extra whitespace
	safeReplace(list, " :", ":") 
	safeReplace(list, ", ", ",")
	safeReplace(list, " ,", ",")
	safeReplace(list, " (", "(")
	safeReplace(list, "( ", "(")
	safeReplace(list, " )", ")")
	safeReplace(list, ") ", ")")
	replaceComments(list) # should follow all calls to safeReplace
	removeTrailingWs(list)
	safeReplace(list, "\t ", "\t") # happens when deleting declarations.
#@-body
#@-node:2::convertCodeList
#@+node:3::convertDocList
#@+body
def convertDocList(docList):

	# print "convertDocList:", docList
	if matchWord(docList, 0, "@doc"):
		i = skipWs(docList, 4)
		if match(docList, i, "\n"):
			i += 1
		docList[0:i] = list("@ ")
#@-body
#@-node:3::convertDocList
#@+node:4::skipDocPart
#@+body
def skipDocPart(list, i):
	
	# print "skipDocPart", i
	while i < len(list):
		if matchWord(list, i, "@code") or matchWord(list, i, "@c"):
			break
		elif isSectionDef(list,i):
			break
		else: i = skipPastLine(list, i)
	return i
#@-body
#@-node:4::skipDocPart
#@+node:5::skipCodePart
#@+body
def skipCodePart(codeList, i):
	
	# print "skipCodePart", i
	if matchWord(codeList, i, "@doc") or matchWord(codeList, i, "@"):
		return i
	while i < len(codeList):
		if match(codeList, i, "//"):
			i = skipPastLine(codeList,i)
		elif match(codeList, i, "/*"):
			i = skipCBlockComment(codeList,i)
		elif match(codeList, i, '"') or match(codeList, i, "'"):
			i = skipString(codeList,i)
		elif match(codeList, i, "\n"):
			i += 1
			if matchWord(codeList, i, "@doc") or matchWord(codeList, i, "@"):
				break
		else: i += 1
	return i
#@-body
#@-node:5::skipCodePart
#@-node:7::c2py Top Level
#@+node:8::removeSentinels
#@-node:8::removeSentinels
#@+node:9::Scanning & Replacing
#@+node:1::convertLeadingBlanks
#@+body
def convertLeadingBlanks(list):

	global tabWidth
	if tabWidth < 2: return
	i = 0
	while i < len(list):
		n = 0
		while i < len(list) and list[i] == ' ':
			n += 1 ; i += 1
			if n == tabWidth:
				list[i-tabWidth:i] = ['\t']
				i = i - tabWidth + 1
				n = 0
		i = skipPastLine(list, i)
#@-body
#@-node:1::convertLeadingBlanks
#@+node:2::findInList
#@+body
def findInList(list, i, findStringOrList):

	findList = stringToList(findStringOrList)
	
	while i < len(list):
		if match(list, i, findList): return i
		else: i += 1
	return -1
#@-body
#@-node:2::findInList
#@+node:3::findInCode
#@+body
def findInCode(codeList, i, findStringOrList):

	findList = stringToList(findStringOrList)
	
	while i < len(codeList):
		if isStringOrComment(codeList,i):
			i = skipStringOrComment(codeList,i)
		elif match(codeList, i, findList):
			return i
		else: i += 1
	return -1
#@-body
#@-node:3::findInCode
#@+node:4::mungeAllFunctions
#@+body
# We scan for a '{' at the top level that is preceeded by ')'
# @code and < < x > > = have been replaced by @c
def mungeAllFunctions(codeList):

	prevSemi = 0 # Previous semicolon: header contains all previous text
	i = 0
	firstOpen = None
	while i < len(codeList):
		if isStringOrComment(codeList,i):
			i = skipStringOrComment(codeList,i)
			prevSemi = i
		elif match(codeList, i, '('):
			if not firstOpen:
				firstOpen = i
			i += 1
		elif match(codeList, i, '#'):
			i = skipPastLine(codeList, i)
			prevSemi = i
		elif match(codeList, i, ';'):
			i += 1
			prevSemi = i
		elif matchWord(codeList, i, "@code"):
			i += 5
			prevSemi = i # restart the scan
		elif matchWord(codeList, i, "@c"):
			i += 2 ; prevSemi = i # restart the scan
		elif match(codeList, i, "{"):
			i = handlePossibleFunctionHeader(codeList,i,prevSemi,firstOpen)
			prevSemi = i ; firstOpen = None # restart the scan
		else: i += 1
#@-body
#@+node:1::handlePossibleFunctionHeader
#@+body
# converts function header lines from c++ format to python format.
# That is, converts
# x1..nn w::y ( t1 z1,..tn zn) {
# to
# def y (z1,..zn): {

def handlePossibleFunctionHeader(codeList, i, prevSemi, firstOpen):

	assert(match(codeList,i,"{"))
	prevSemi = skipWsAndNl(codeList, prevSemi)
	close = prevNonWsOrNlChar(codeList, i)
	if close < 0 or codeList[close] != ')':
		return 1 + skipToMatchingBracket(codeList, i)
	if not firstOpen:
		return 1 + skipToMatchingBracket(codeList, i)
	close2 = skipToMatchingBracket(codeList, firstOpen)
	if close2 != close:
		return 1 + skipToMatchingBracket(codeList, i)
	open = firstOpen
	assert(codeList[open]=='(')
	head = codeList[prevSemi:open]
	# do nothing if the head starts with "if", "for" or "while"
	k = skipWs(head,0)
	if k >= len(head) or not head[k] in string.letters:
		return 1 + skipToMatchingBracket(codeList, i)
	kk = skipPastWord(head,k)
	if kk > k:
		headString = listToString(head[k:kk])
		# C keywords that might be followed by '{'
		# print "headString:", headString
		if headString in [ "class", "do", "for", "if", "struct", "switch", "while"]:
			return 1 + skipToMatchingBracket(codeList, i)
	args = codeList[open:close+1]
	k = 1 + skipToMatchingBracket(codeList,i)
	body = codeList[i:k]
	#print "head:", listToString(head)
	#print "args:", listToString(args)
	#print "body:", listToString(body)
	#print "tot: ", listToString(codeList[prevSemi:k])
	head = massageFunctionHead(head)
	args = massageFunctionArgs(args)
	body = massageFunctionBody(body)
	#print "head2:", listToString(head)
	#print "args2:", listToString(args)
	#print "body2:", listToString(body)
	#print "tot2: ", listToString(codeList[prevSemi:k])
	result = []
	for item in head:
		result.append(item)
	for item in args:
		result.append(item)
	for item in body:
		result.append(item)
	codeList[prevSemi:k] = result
	return k
#@-body
#@-node:1::handlePossibleFunctionHeader
#@+node:2::massageFunctionArgs
#@+body
def massageFunctionArgs(args):
	global gClassName
	assert(args[0]=='(')
	assert(args[-1]==')')

	result = ['('] ; lastWord = []
	if gClassName:
		for item in list("self,"): result.append(item) #can put extra comma

	i = 1
	while i < len(args):
		i = skipWsAndNl(args, i)
		c = args[i]
		if c in string.letters:
			j = skipPastWord(args,i)
			lastWord = args[i:j]
			i = j
		elif c == ',' or c == ')':
			for item in lastWord:
				result.append(item)
			if lastWord != [] and c == ',':
				result.append(',')
			lastWord = []
			i += 1
		else: i += 1
	if result[-1] == ',':
		del result[-1]
	result.append(')')
	result.append(':')
	# print "new args:", listToString(result)
	return result
#@-body
#@-node:2::massageFunctionArgs
#@+node:3::massageFunctionHead (sets gClassName)
#@+body
def massageFunctionHead(head):

	# print "head:", listToString(head)
	result = []
	prevWord = []
	global gClassName ; gClassName = []
	i = 0
	while i < len(head):
		i = skipWsAndNl(head, i)
		if i < len(head) and head[i] in string.letters:
			result = []
			j = skipPastWord(head,i)
			prevWord = head[i:j]
			i = j
			# look for ::word2
			i = skipWs(head,i)
			if match(head,i,"::"):
				# Set the global to the class name.
				gClassName = listToString(prevWord)
				# print "class name:", gClassName
				i = skipWs(head, i+2)
			 	if i < len(head) and (head[i]=='~' or head[i] in string.letters):
					j = skipPastWord(head,i)
					if head[i:j] == prevWord:
						for item in list("__init__"): result.append(item)
					elif head[i]=='~' and head[i+1:j] == prevWord:
						for item in list("__del__"): result.append(item)
					else:
						# for item in "::": result.append(item)
						for item in head[i:j]: result.append(item)
					i = j
			else:
				for item in prevWord:result.append(item)
		else: i += 1
		
	finalResult = list("def ")
	for item in result: finalResult.append(item)
	# print "new head:", listToString(finalResult)
	return finalResult
#@-body
#@-node:3::massageFunctionHead (sets gClassName)
#@+node:4::massageFunctionBody
#@+body
def massageFunctionBody(body):

	body = massageIvars(body)
	body = removeCasts(body)
	body = removeTypeNames(body)
	return body
#@-body
#@+node:1::massageIvars
#@+body
def massageIvars(body):

	if gClassName and ivarsDict.has_key(gClassName):
		ivars = ivarsDict [ gClassName ]
	else:
		ivars = []
	# print "key:ivars=", gClassName, ':', `ivars`

	i = 0
	while i < len(body):
		if isStringOrComment(body,i):
			i = skipStringOrComment(body,i)
		elif body[i] in string.letters:
			j = skipPastWord(body,i)
			word = listToString(body[i:j])
			# print "looking up:", word
			if word in ivars:
				# replace word by self.word
				# print "replacing", word, " by self.", word
				word = "self." + word
				word = list(word)
				body[i:j] = word
				delta = len(word)-(j-i)
				i = j + delta
			else: i = j
		else: i += 1
	return body
#@-body
#@-node:1::massageIvars
#@+node:2::removeCasts
#@+body
def removeCasts(body):

	i = 0
	while i < len(body):
		if isStringOrComment(body,i):
			i = skipStringOrComment(body,i)
		elif match(body, i, '('):
			start = i
			i = skipWs(body, i+1)
			if body[i] in string.letters:
				j = skipPastWord(body,i)
				word = listToString(body[i:j])
				i = j
				if word in classList or word in typeList:
					i = skipWs(body, i)
					while match(body,i,'*'):
						i += 1
					i = skipWs(body, i)
					if match(body,i,')'):
						i += 1
						# print "removing cast:", listToString(body[start:i])
						del body[start:i]
						i = start
		else: i += 1
	return body
#@-body
#@-node:2::removeCasts
#@+node:3::removeTypeNames
#@+body
# Do _not_ remove type names when preceeded by new.

def removeTypeNames(body):

	i = 0
	while i < len(body):
		if isStringOrComment(body,i):
			i = skipStringOrComment(body,i)
		elif matchWord(body, i, "new"):
			i = skipPastWord(body,i)
			i = skipWs(body,i)
			# don't remove what follows new.
			if body[i] in string.letters:
				i = skipPastWord(body,i)
		elif body[i] in string.letters:
			j = skipPastWord(body,i)
			word = listToString(body[i:j])
			if word in classList or word in typeList:
				k = skipWs(body, j)
				while match(body,k,'*'):
					k += 1 ; j = k
				# print "Deleting type name:", listToString(body[i:j])
				del body[i:j]
			else:
				i = j
		else: i += 1
	return body
#@-body
#@-node:3::removeTypeNames
#@-node:4::massageFunctionBody
#@-node:4::mungeAllFunctions
#@+node:5::handleAllKeywords
#@+body
# converts if ( x ) to if x:
# converts while ( x ) to while x:
def handleAllKeywords(codeList):

	# print "handAllKeywords:", listToString(codeList)
	i = 0
	while i < len(codeList):
		if isStringOrComment(codeList,i):
			i = skipStringOrComment(codeList,i)
		elif ( matchWord(codeList,i,"if") or
			matchWord(codeList,i,"while") or
			matchWord(codeList,i,"for") or
			matchWord(codeList,i,"elif") ):
			i = handleKeyword(codeList,i)
		else:
			i += 1
	# print "handAllKeywords2:", listToString(codeList)
#@-body
#@+node:1::handleKeyword
#@+body
def handleKeyword(codeList,i):

	isFor = false
	if (matchWord(codeList,i,"if")):
		i += 2
	elif (matchWord(codeList,i,"elif")):
		i += 4
	elif (matchWord(codeList,i,"while")):
		i += 5
	elif (matchWord(codeList,i,"for")):
		i += 3
		isFor = true
	else: assert(0)
	# Make sure one space follows the keyword
	k = i
	i = skipWs(codeList,i)
	if k == i:
		c = codeList[i]
		codeList[i:i+1] = [ ' ', c ]
		i += 1
	# Remove '(' and matching ')' and add a ':'
	if codeList[i] == "(":
		j = removeMatchingBrackets(codeList,i)
		if j > i and j < len(codeList):
			c = codeList[j]
			codeList[j:j+1] = [":", " ", c]
			j = j + 2
		return j
	return i
#@-body
#@-node:1::handleKeyword
#@-node:5::handleAllKeywords
#@+node:6::isWs and isWOrNl
#@+body
def isWs(c):
	return c == ' ' or c == '\t'
	
def isWsOrNl(c):
	return c == ' ' or c == '\t' or c == '\n'
#@-body
#@-node:6::isWs and isWOrNl
#@+node:7::isSectionDef
#@+body
# returns the ending index if i points to < < x > > =
def isSectionDef(list, i):

	i = skipWs(list,i)
	if not match(list,i,"<<"): return false
	while i < len(list) and list[i] != '\n':
		if match(list,i,">>="): return i+3
		else: i += 1
	return false
#@-body
#@-node:7::isSectionDef
#@+node:8::isStringOrComment
#@+body
def isStringOrComment(list, i):

	return match(list,i,"'") or match(list,i,'"') or match(list,i,"//") or match(list,i,"/*")
#@-body
#@-node:8::isStringOrComment
#@+node:9::match
#@+body
# returns true if findList matches starting at codeList[i]

def match (codeList, i, findStringOrList):

	findList = stringToList(findStringOrList)
	n = len(findList)
	j = 0
	while i+j < len(codeList) and j < len(findList):
		if codeList[i+j] != findList[j]:
			return false
		else:
			j += 1
			if j == n:
				return i+j
	return false
#@-body
#@-node:9::match
#@+node:10::matchWord
#@+body
def matchWord (codeList, i, findStringOrList):

	j = match(codeList,i,findStringOrList)
	if not j:
		return false
	elif j >= len(codeList):
		return true
	else:
		c = codeList[j]
		return not (c in string.letters or c in string.digits or c == '_')
#@-body
#@-node:10::matchWord
#@+node:11::prevNonWsChar and prevNonWsOrNlChar
#@+body
def prevNonWsChar(list, i):

	i -= 1
	while i >= 0 and isWs(list[i]):
		i -= 1
	return i

def prevNonWsOrNlChar(list, i):

	i -= 1
	while i >= 0 and isWsOrNl(list[i]):
		i -= 1
	return i
#@-body
#@-node:11::prevNonWsChar and prevNonWsOrNlChar
#@+node:12::removeAllCComments
#@+body
def removeAllCComments(list, delim):

	i = 0
	while i < len(list):
		if match(list,i,"'") or match(list,i,'"'):
			i = skipString(list,i)
		elif match(list,i,"//"):
			j = skipPastLine(list,i)
			print "deleting single line comment:", listToString(list[i:j])
			del list[i:j]
		elif match(list,i,"/*"):
			j = skipCBlockComment(list,i)
			print "deleting block comment:", listToString(list[i:j])
			del list[i:j]
		else:
			i += 1
#@-body
#@-node:12::removeAllCComments
#@+node:13::removeAllCSentinels
#@+body
def removeAllCSentinels(list, delim):

	i = 0
	while i < len(list):
		if match(list,i,"'") or match(list,i,'"'):
			# string starts a line.
			i = skipString(list,i)
			i = skipPastLine(list,i)
		elif match(list,i,"/*"):
			# block comment starts a line
			i = skipCBlockComment(list,i)
			i = skipPastLine(line,i)
		elif match(list,i,"//@"):
			j = skipPastLine(list,i)
			print "deleting sentinel:", listToString(list[i:j])
			del list[i:j]
		else:
			i = skipPastLine(list,i)
#@-body
#@-node:13::removeAllCSentinels
#@+node:14::removeAllPythonComments
#@+body
def removeAllPythonComments(list, delim):

	i = 0
	while i < len(list):
		if match(list,i,"'") or match(list,i,'"'):
			i = skipString(list,i)
		elif match(list,i,"#"):
			j = skipPastLine(list,i)
			print "deleting comment:", listToString(list[i:j])
			del list[i:j]
		else:
			i += 1
#@-body
#@-node:14::removeAllPythonComments
#@+node:15::removeAllPythonSentinels
#@+body
def removeAllPythonSentinels(list, delim):

	i = 0
	while i < len(list):
		if match(list,i,"'") or match(list,i,'"'):
			# string starts a line.
			i = skipString(list,i)
			i = skipPastLine(list,i)
		elif match(list,i,"#@"):
			j = skipPastLine(list,i)
			print "deleting sentinel:", listToString(list[i:j])
			del list[i:j]
		else:
			i = skipPastLine(list,i)
#@-body
#@-node:15::removeAllPythonSentinels
#@+node:16::removeAtRoot
#@+body
def removeAtRoot (codeList):

	i = skipWs(codeList, 0)
	if matchWord(codeList,i,"@root"):
		j = skipPastLine(codeList,i)
		del codeList[i:j]

	while i < len(codeList):
		if isStringOrComment(codeList,i):
			i = skipStringOrComment(codeList,i)
		elif match(codeList,i,"\n"):
			i = skipWs(codeList, i+1)
			if matchWord (codeList,i,"@root"):
				j = skipPastLine(codeList,i)
				del codeList[i:j]
		else: i += 1

#@-body
#@-node:16::removeAtRoot
#@+node:17::removeBlankLines
#@+body
def removeBlankLines(codeList):

	i = 0
	while i < len(codeList):
		j = i
		while j < len(codeList) and (codeList[j]==" " or codeList[j]=="\t"):
			j += 1
		if j== len(codeList) or codeList[j] == '\n':
			del codeList[i:j+1]
		else:
			oldi = i
			i = skipPastLine(codeList,i)
#@-body
#@-node:17::removeBlankLines
#@+node:18::removeExcessWs
#@+body
def removeExcessWs(codeList):

	i = 0
	i = removeExcessWsFromLine(codeList,i)
	while i < len(codeList):
		if isStringOrComment(codeList,i):
			i = skipStringOrComment(codeList,i)
		elif match(codeList,i,'\n'):
			i += 1
			i = removeExcessWsFromLine(codeList,i)
		else: i += 1
#@-body
#@+node:1::removeExessWsFromLine
#@+body
def removeExcessWsFromLine(codeList,i):

	assert(i==0 or codeList[i-1] == '\n')
	i = skipWs(codeList,i)
	while i < len(codeList):
		if isStringOrComment(codeList,i): break # safe
		elif match(codeList, i, '\n'): break
		elif match(codeList, i, ' ') or match(codeList, i, '\t'):
			# Replace all whitespace by one blank.
			k = i
			i = skipWs(codeList,i)
			codeList[k:i] = [' ']
			i = k + 1 # make sure we don't go past a newline!
		else: i += 1
	return i
#@-body
#@-node:1::removeExessWsFromLine
#@-node:18::removeExcessWs
#@+node:19::removeLeadingAtCode
#@+body
def removeLeadingAtCode(codeList):

	i = skipWsAndNl(codeList,0)
	if matchWord(codeList,i,"@code"):
		i = skipWsAndNl(codeList,5)
		del codeList[0:i]
	elif matchWord(codeList,i,"@c"):
		i = skipWsAndNl(codeList,2)
		del codeList[0:i]
#@-body
#@-node:19::removeLeadingAtCode
#@+node:20::removeMatchingBrackets
#@+body
def removeMatchingBrackets(codeList, i):

	j = skipToMatchingBracket(codeList, i)
	if j > i and j < len(codeList):
		# print "del brackets:", listToString(codeList[i:j+1])
		c = codeList[j]
		if c == ')' or c == ']' or c == '}':
			del codeList[j:j+1]
			del codeList[i:i+1]
			# print "returning:", listToString(codeList[i:j])
			return j - 1
		else: return j + 1
	else: return j
#@-body
#@-node:20::removeMatchingBrackets
#@+node:21::removeSemicolonsAtEndOfLines
#@+body
def removeSemicolonsAtEndOfLines(list):

	i = 0
	while i < len(list):
		if isStringOrComment(list,i):
			i = skipStringOrComment(list,i)
		elif list[i] == ';':
			j = skipWs(list,i+1)
			if j >= len(list) or match(list,j,'\n') or match(list,j,'#') or match(list,j,"//"):
				del list[i]
			else: i += 1
		else: i += 1
#@-body
#@-node:21::removeSemicolonsAtEndOfLines
#@+node:22::removeTrailingWs
#@+body
def removeTrailingWs(list):

	i = 0
	while i < len(list):
		if isWs(list[i]):
			j = i
			i = skipWs(list,i)
			assert(j < i)
			if i >= len(list) or list[i] == '\n':
				# print "removing trailing ws:", `i-j`
				del list[j:i]
				i = j
		else: i += 1
#@-body
#@-node:22::removeTrailingWs
#@+node:23::replace
#@+body
# Replaces all occurances of findString by changeString.
# Deletes all occurances if change is None
def replace(codeList, findString, changeString):

	if len(findString)==0: return
	findList = stringToList(findString)
	changeList = stringToList(changeString)

	i = 0
	while i < len(codeList):
		if match(codeList, i, findList):
			codeList[i:i+len(findList)] = changeList
			i += len(changeList)
		else: i += 1
#@-body
#@-node:23::replace
#@+node:24::replaceComments
#@+body
# For Leo we expect few block comments; doc parts are much more common.

def replaceComments(codeList):

	i = 0
	if match(codeList, i, "//"):
		codeList[0:2] = ['#']
	while i < len(codeList):
		if match(codeList, i, "//"):
			codeList[i:i+2] = ['#']
			i = skipPastLine(codeList,i)
		elif match(codeList, i, "/*"):
			j = skipCBlockComment(codeList,i)
			del codeList[j-2:j]
			codeList[i:i+2] = ['#']
			j -= 2 ; k = i ; delta = -1
			while k < j + delta :
				if codeList[k]=='\n':
					codeList[k:k+1] = ['\n', '#', ' ']
					delta += 2 ; k += 3 # progress!
				else: k += 1
			i = j + delta
		elif match(codeList, i, '"') or match(codeList, i, "'"):
			i = skipString(codeList,i)
		else: i += 1
#@-body
#@-node:24::replaceComments
#@+node:25::replaceSectionDefs
#@+body
# Replaces < < x > > = by @c (at the start of lines).
def replaceSectionDefs(codeList):

	i = 0
	j = isSectionDef(codeList,i)
	if j > 0: codeList[i:j] = list("@c ")

	while i < len(codeList):
		if isStringOrComment(codeList,i):
			i = skipStringOrComment(codeList,i)
		elif match(codeList,i,"\n"):
			i += 1
			j = isSectionDef(codeList,i)
			if j > i: codeList[i:j] = list("@c ")
		else: i += 1
#@-body
#@-node:25::replaceSectionDefs
#@+node:26::safeReplace
#@+body
# Replaces occurances of findString by changeString outside of C comments and strings.
# Deletes all occurances if change is None.
def safeReplace(codeList, findString, changeString):

	if len(findString)==0: return
	findList = stringToList(findString)
	changeList = stringToList(changeString)
	i = 0
	if findList[0] in string.letters: #use matchWord
		while i < len(codeList):
			if isStringOrComment(codeList,i):
				i = skipStringOrComment(codeList,i)
			elif matchWord(codeList, i, findList):
				codeList[i:i+len(findList)] = changeList
				i += len(changeList)
			else: i += 1
	else: #use match
		while i < len(codeList):
			if match(codeList, i, findList):
				codeList[i:i+len(findList)] = changeList
				i += len(changeList)
			else: i += 1
#@-body
#@-node:26::safeReplace
#@+node:27::skipCBlockComment
#@+body
def skipCBlockComment(codeList, i):

	assert(match(codeList, i, "/*"))
	i += 2

	while i < len(codeList):
		if match(codeList, i, "*/"): return i + 2
		else: i += 1
	return i
#@-body
#@-node:27::skipCBlockComment
#@+node:28::skipPastLine
#@+body
def skipPastLine(codeList, i):

	while i < len(codeList) and codeList[i] != '\n':
		i += 1
	if i < len(codeList) and codeList[i] == '\n':
		i += 1
	return i
#@-body
#@-node:28::skipPastLine
#@+node:29::skipPastWord
#@+body
def skipPastWord(list, i):

	assert(list[i] in string.letters or list[i]=='~')
	
	# Kludge: this helps recognize dtors.
	if list[i]=='~':
		i += 1
	
	while i < len(list) and (
		list[i] in string.letters or
		list[i] in string.digits or
		list[i]=='_'):
		i += 1
	return i
#@-body
#@-node:29::skipPastWord
#@+node:30::skipString
#@+body
def skipString(codeList, i):

	delim = codeList[i] # handle either single or double-quoted strings
	assert(delim == '"' or delim == "'")
	i += 1

	while i < len(codeList):
		if codeList[i] == delim: return i + 1
		elif codeList[i] == '\\': i += 2
		else: i += 1
	return i
#@-body
#@-node:30::skipString
#@+node:31::skipStringOrComment
#@+body
def skipStringOrComment(list,i):

	if match(list,i,"'") or match(list,i,'"'):
		return skipString(list,i)
	if match(list, i, "//"):
		return skipPastLine(list,i)
	elif match(list, i, "/*"):
		return skipCBlockComment(list,i)
	else: assert(0)
#@-body
#@-node:31::skipStringOrComment
#@+node:32::skipToMatchingBracket
#@+body
def skipToMatchingBracket(codeList, i):

	c = codeList[i]
	if   c == '(': delim = ')'
	elif c == '{': delim = '}'
	elif c == '[': delim = ']'
	else: assert(0)

	i += 1
	while i < len(codeList):
		c = codeList[i]
		if isStringOrComment(codeList,i):
			i = skipStringOrComment(codeList,i)
		elif c == delim:
			return i
		elif c == '(' or c == '[' or c == '{':
			i = skipToMatchingBracket(codeList,i)
			i += 1 # skip the closing bracket.
		else: i += 1
	return i
#@-body
#@-node:32::skipToMatchingBracket
#@+node:33::skipWs and skipWsAndNl
#@+body
def skipWs(list, i):

	while i < len(list):
		c = list[i]
		if c == ' ' or c == '\t':
			i += 1
		else: break
	return i
	
def skipWsAndNl(list, i):

	while i < len(list):
		c = list[i]
		if c == ' ' or c == '\t' or c == '\n':
			i += 1
		else: break
	return i
#@-body
#@-node:33::skipWs and skipWsAndNl
#@+node:34::stringToList
#@+body
# converts a string to a list containing one item per character of the list.
# converts None to the empty string and leaves other types alone.

# list(string) does not work on none.
def stringToList(string):

	if string:
		return list(string)
	else:
		return []
#@-body
#@-node:34::stringToList
#@+node:35::listToString
#@+body
def listToString(list):

	return string.join(list,"")
#@-body
#@-node:35::listToString
#@-node:9::Scanning & Replacing
#@-others


gClassName = "" # The class name for the present function.  Used to modify ivars.
gIvars = [] # List of ivars to be converted to self.ivar

def test():
	global printFlag ; printFlag = true
	for s in testData:
		convertCStringToPython(s, doLeoTranslations)
		
def go():
	test()

if __name__ == "__main__":
	speedTest(2)
#@-body
#@-node:0::@file c2py.py
#@-leo
