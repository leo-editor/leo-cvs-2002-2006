#! /usr/bin/env python
#@+leo
#@+node:0::@file setup.py
#@+body
#@@first
#@@language python


#@+at
#  Script for creating distributions of leo.py using Python's distutils package.
# Invoke this script as follows:
# 
# import os
# os.system(r"cd C:\prog\leoCVS\leo")
# os.system("python setup.py sdist --formats=zip")

#@-at
#@@c

true = 1 ; false = 0
from distutils.core import setup
import distutils,os,sys,traceback


#@+others
#@+node:2::printReminders
#@+body
def printReminders ():

	print
	print "- Update version numbers"
	print "- Clear Default Tangle Directory"
	print "- Distribute both leox-y.zip and leosetup.exe"
	print
#@-body
#@-node:2::printReminders
#@+node:3::generateModules
#@+body
# Generate the list of modules in the distribution.

def generateModules():

	files = os.listdir(os.getcwd())
	modules = []
	for f in files:
		head,tail = os.path.split(f)
		root,ext = os.path.splitext(tail)
		if tail[0:3]=="leo" and ext==".py":
			modules.append(root)
			
	modules.sort()
	# print "modules:", modules
	return modules

#@-body
#@-node:3::generateModules
#@+node:4::replacePatterns
#@+body
def replacePatterns (file,pats):

	try:
		path = os.getcwd()
		name  = os.path.join(path,file)
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
		traceback.print_exc()
		sys.exit()
#@-body
#@-node:4::replacePatterns
#@+node:5::setDefaultParams
#@+body
def setDefaultParams():

	print "setDefaultParams"

	pats = (
		("create_nonexistent_directories = 1","create_nonexistent_directories = 0"),
		("read_only = 1","read_only = 0"),
		("use_customizeLeo_dot_py = 1","use_customizeLeo_dot_py = 0"))

	replacePatterns("leoConfig.leo",pats)
	replacePatterns("leoConfig.txt",pats)
#@-body
#@-node:5::setDefaultParams
#@+node:6::unsetDefaultParams
#@+body
def unsetDefaultParams():

	print "unsetDefaultParams"
	
	pats = (
		("use_customizeLeo_dot_py = 0","use_customizeLeo_dot_py = 1"),)

	replacePatterns("leoConfig.leo",pats)
	replacePatterns("leoConfig.txt",pats)
#@-body
#@-node:6::unsetDefaultParams
#@-others


if sys.argv[1] == "sdist":
	printReminders()
	setDefaultParams()

modules = generateModules()
setup (
	
	#@<< setup info for setup.py >>
	#@+node:1::<< setup info for setup.py >> (version number)
	#@+body
	name="leo",
	version="3.11b1",
	author="Edward K. Ream",
	author_email="edream@tds.net",
	url="http://personalpages.tds.net/~edream/front.html",
	py_modules=modules, # leo*.py also included in manifest
	description = "Leo: Literate Editor with Outlines",
	licence="Python", # [sic], not license
	platforms=["Windows, Linux, Macintosh"],
	long_description =
	"""Leo is an outline-oriented editor written in 100% pure Python.
	Leo works on any platform that supports Python 2.1 or 2.2 and the Tk toolkit.
	This version of Leo was developed with Python 2.2.1 and Tk 8.3.2.
	
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
	#@-body
	#@-node:1::<< setup info for setup.py >> (version number)

)

if sys.argv[1] == "sdist":
	unsetDefaultParams()
	print "setup complete"
#@-body
#@-node:0::@file setup.py
#@-leo
