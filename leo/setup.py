#@+leo
#@+node:0::@file setup.py
#@+body
#@@language python


#@+at
#  Script for creating and installing distributions of leo.py using Python's 
# distutils package.  setup.py is the conventional name for such scripts.
# 
# On Windows, invoke this script using sdist.bat
# On Linux do: cd LeoPy ; python setup.py sdist --force-manifest --formats=gztar,zip

#@-at
#@@c

from distutils.core import setup
import os

print
print "Update version numbers"
print "Clear Default Tangle Directory"
print "Recreate leoConfig.txt"
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
# print "modules:", modules

#@<< setup info for setup.py >>
#@+node:1::<< setup info for setup.py >> (version number)
#@+body
setup( name="leo",
	version="3.10",
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
""")
#@-body
#@-node:1::<< setup info for setup.py >> (version number)
#@-body
#@-node:0::@file setup.py
#@-leo
