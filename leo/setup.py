#@+leo

#@+node:0::@file setup.py
#@+body
#@@language python


#@+at
#  Script for creating and installing distributions of leo.py using Python's distutils package.  setup.py is the conventional name 
# for such scripts.
# 
# On Windows, invoke this script using sdist.bat
# On Linux do: cd LeoPy ; python setup.py sdist --force-manifest --formats=gztar,zip

#@-at
#@@c

from distutils.core import setup
import os

print
print "Remember to update version numbers!"
print "Remember to clear Default Tangle Directory!"
print "Distribute both leox-y.zip and leosetup.exe"
print

# Generate the list of modules.
files = os.listdir(os.getcwd())
modules = []
for f in files:
	head,tail = os.path.split(f)
	root,ext = os.path.splitext(tail)
	if tail[0:3]=="leo" and ext==".py":
		modules.append(root)
		
modules.sort()
# print "modules:", `modules`

setup( name="leo",
	version="3.4",
	author="Edward K. Ream",
	author_email="edream@tds.net",
	url="http://personalpages.tds.net/~edream/front.html",
	py_modules=modules, # leo*.py also included in manifest
	description = "Leo: Literate Editor with Outlines",
	licence="Python", # [sic], not license
	platforms=["Windows, Linux, Macintosh"],
	long_description =
"""Leo is an outline-oriented editor written in 100% pure Python.
Leo works on any platform that supports Python 2.x and the Tk toolkit.
This version of Leo was developed with Python 2.2 and Tk 8.3.2.
You may download Python from http://python.org/ and
tcl/Tk from http://tcl.activestate.com/software/tcltk/
Leo features a multi-window outlining editor, Python colorizing,
powerful outline commands and many other things, including
Unlimited Undo/Redo and an integrated Python shell(IDLE) window.""")
#@-body
#@-node:0::@file setup.py
#@-leo
