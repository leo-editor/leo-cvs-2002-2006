#@+leo

#@+node:0::@file leoGlobals.py
#@+body
#@@language python


#@+at
#  Global constants and variables used throughout Leo2.
# Most modules should do from leoGlobals import *
# NB: Use app().ivar instead of using global variables

#@-at
#@@c
	

#@<< define global constants >>
#@+node:1::<< define global constants >>
#@+body
# General constants...
true = 1
false = 0 # Better than None
body_newline = '\n'
body_ignored_newline = '\r'
prolog_string = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"

# New in leo.py 3.0
prolog_prefix_string = "<?xml version=\"1.0\" encoding="
prolog_version_string1 = "UTF-8" # for leo.py 2.x
prolog_version_string2 = "ISO-8859-1" # for leo.py 3.x
prolog_postfix_string = "?>"

# These are set by the @langauge directive.
# Used by Tangle, Untangle and syntax coloring.
ada_language =		 1
c_language =		 2  # C, C++ or objective C.
cweb_language =		 3  # CWEB syntax coloring
cobol_language =	 4  # literate cobol??
fortran_language =	 5  # Comments start with C
fortran90_language =	 6  # Comments start with !
html_language =		 7
java_language =		 8
latex_language =	 9
lisp_language =		10
pascal_language =	11
plain_text_language =	12
perl_language =		13  # just ##
perlpod_language =	14  # ## and =pod and =cut
python_language =	15
shell_language =	16  # shell scripts
tcltk_language =	17
unknown_language =	18  # Set when @comment is seen.
php_language = 19 # 08-SEP-2002 DTHEIN

# Synonyms for the bits returned by is_special_bits...
color_bits =    0x00001
comment_bits =	 0x00002
cweb_bits =     0x00004
header_bits =   0x00008
ignore_bits =   0x00010
language_bits = 0x00020
nocolor_bits =	 0x00040
noheader_bits = 0x00080
noweb_bits =    0x00100
#               0x00200 #unused
page_width_bits=0x00400
path_bits =	    0x00800
root_bits =	    0x01000 # Also represents < < * > > =
silent_bits =	  0x02000
tab_width_bits =0x04000
terse_bits = 	  0x08000
unit_bits = 	   0x10000
verbose_bits =	 0x20000
#@-body
#@-node:1::<< define global constants >>



#@+others
#@+node:2::alert
#@+body
def alert(message):

	es(message)

	import tkMessageBox
	tkMessageBox.showwarning("Alert", message)

#@-body
#@-node:2::alert
#@+node:3::app, setApp
#@+body
# gApp is the only global in the application, and gApp is accessed only via app().

def app():
	global gApp
	return gApp
	
def setApp(app):
	global gApp
	gApp = app
#@-body
#@-node:3::app, setApp
#@+node:4::choose
#@+body
def choose(cond, a, b): # warning: evaluates all arguments

	if cond: return a
	else: return b
#@-body
#@-node:4::choose
#@+node:5::es, enl, ecnl
#@+body
def ecnl():
	ecnls(1)

def ecnls(n):
	log = app().log
	if log:
		while log.es_newlines < n:
			enl()

def enl():
	log = app().log
	if log:
		log.es_newlines += 1
		log.putnl()

def es(s):
	if s == None or len(s) == 0: return
	log = app().log
	if log:
		log.put(s) # No change needed for Unicode!
		# 6/2/02: This logic will fail if log is None.
		for ch in s:
			if ch == '\n': log.es_newlines += 1
			else: log.es_newlines = 0
		ecnl() # only valid here
	else:
		print "Null log:", s
#@-body
#@-node:5::es, enl, ecnl
#@+node:6::print_stack
#@+body
def print_stack():

	import traceback
	traceback.print_stack()
#@-body
#@-node:6::print_stack
#@+node:7::top
#@+body
def top():

	frame = app().log # the current frame
	return frame.commands
#@-body
#@-node:7::top
#@-others
#@-body
#@-node:0::@file leoGlobals.py
#@-leo
