#! /usr/bin/env python
#@+leo-ver=4
#@+node:EKR.20040502193420:@file-thin ../setup.py
#@@first

import leoGlobals as g
from leoGlobals import true,false

from distutils.core import setup
import distutils,os,sys

#@+others
#@+node:EKR.20040502193420.2:printReminders
def printReminders ():

	print
	print "- Update version numbers"
	print "- Clear Default Tangle Directory"
	print "- Distribute both leox-y.zip and leosetup.exe"
	print
#@nonl
#@-node:EKR.20040502193420.2:printReminders
#@+node:EKR.20040502193420.3:generateModules
# Generate the list of modules in the distribution.

def generateModules():
	
	from leoGlobals import os_path_join,os_path_split,os_path_splitext

	dir = os.getcwd()
	dir = g.os_path_join(dir,"src")
	files = os.listdir(dir)
	modules = []
	for f in files:
		head,tail = g.os_path_split(f)
		root,ext = g.os_path_splitext(tail)
		if tail[0:3]=="leo" and ext==".py":
			modules.append(root)
			
	modules.sort()
	# print "modules:", modules
	return modules
#@-node:EKR.20040502193420.3:generateModules
#@+node:EKR.20040502193420.4:replacePatterns
def replacePatterns (file,pats):

	try:
		path = os.getcwd()
		name  = g.os_path_join(path,file)
		f = open(name)
	except:
		print "*****", file, "not found"
		return
	try:
		data = f.read()
		f.close()
		changed = false
		for pat1,pat2 in pats:
			newdata = data.replace(pat1,pat2)
			if data != newdata:
				changed = true
				data = newdata
				print file,"replaced",pat1,"by",pat2
		if changed:
			f = open(name,"w")
			f.write(data)
			f.close()
	except:
		import traceback ; traceback.print_exc()
		sys.exit()
#@-node:EKR.20040502193420.4:replacePatterns
#@+node:EKR.20040502193420.5:setDefaultParams
def setDefaultParams():

	print "setDefaultParams"

	pats = (
		("create_nonexistent_directories = 1","create_nonexistent_directories = 0"),
		("read_only = 1","read_only = 0"),
		("use_plugins = 1","use_plugins = 0"))

	replacePatterns(g.os_path_join("config","leoConfig.leo"),pats)
	replacePatterns(g.os_path_join("config","leoConfig.txt"),pats)
#@nonl
#@-node:EKR.20040502193420.5:setDefaultParams
#@-others

if 1: # Use this only for final distributions.
	if sys.argv[1] == "sdist":
		setDefaultParams()

# modules = generateModules()
modules = []

setup (
	#@	<< setup info for setup.py >>
	#@+node:EKR.20040502193420.1:<< setup info for setup.py >> UPDATE BY HAND (no spaces)
	name="leo",
	version="4.2-a1",
	author="Edward K. Ream",
	author_email="edream@tds.net",
	url="http://personalpages.tds.net/~edream/front.html",
	py_modules=modules, # leo*.py also included in manifest
	description = "Leo: Literate Editor with Outlines",
	licence="Python", # [sic], not license
	platforms=["Windows, Linux, Macintosh"],
	long_description =
	"""Leo is an outline-oriented editor written in 100% pure Python.
	Leo works on any platform that supports Python 2.2 or above and the Tk toolkit.
	This version of Leo was developed with Python 2.3.3 and Tk 8.4.3.
	
	Download Python from http://python.org/
	Download tcl/Tk from http://tcl.activestate.com/software/tcltk/
	
	Leo features a multi-window outlining editor with powerful outline commands,
	support for literate programming features, syntax colorizing for many common
	languages, unlimited Undo/Redo, an integrated Python shell(IDLE) window,
	and many user options including user-definable colors and fonts and user-
	definable shortcuts for all menu commands.
	
	Leo a unique program editor, outline editor, literate programming tool,
	data manager and project manager. Cloned outlines are a key enabling feature
	that make possible multiple views of a project within a single Leo outline.
	"""
	#@nonl
	#@-node:EKR.20040502193420.1:<< setup info for setup.py >> UPDATE BY HAND (no spaces)
	#@nl
)

if sys.argv[1] == "sdist":
	print "setup complete"
#@nonl
#@-node:EKR.20040502193420:@file-thin ../setup.py
#@-leo
