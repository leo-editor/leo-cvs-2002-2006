#@+leo

#@+node:0::@file setup.py

#@+body

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
	version="0.9beta",
	author="Edward K. Ream",
	author_email="edream@tds.net",
	url="http://personalpages.tds.net/~edream/front.html",
	py_modules=modules, # leo*.py also included in manifest
	description = "Leo: Literate Editor with Outlines",
	licence="Python", # [sic], not license
	platforms=["Windows, Linux, Macintosh"],
	long_description =
"""Leo is an outline-oriented editor written in 100% pure Python.
Leo works on all platforms that support Python and the Tk toolkit.
Leo features a multi-window outlining editor, Python colorizing,
powerful outline commands and many other things, including an
integrated Python shell(IDLE) window.""")
#@-body

#@-node:0::@file setup.py

#@-leo
