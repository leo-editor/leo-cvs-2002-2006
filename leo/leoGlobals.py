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

# Internally, lower case is used for all language names.
language_delims_dict = {
	"c" : "// /* */", # C, C++ or objective C.
	"cweb" : "@q @>", 
	"fortran" : "C",
	"fortran90" : "!",
	"html" : "<!-- -->",
	"java" : "/* */",
	"latex" : "%",
	"pascal" : "// { }",
	"perl" : "#",
	"perlpod" : "# __=pod__ __=cut__", # 9/25/02: The perlpod hack.
	"php" : "//",
	"plain" : "#", # We must pick something.
	"python" : "#",
	"shell" : "#",  # shell scripts
	"tcltk" : "#",
	"unknown" : "#" } # Set when @comment is seen.
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
