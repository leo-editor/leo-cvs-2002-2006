#! /usr/bin/env python
#@+leo-ver=4-thin
#@+node:EKR.20040519082027.23:@thin createLeoDist.py
#@@first

#@+at
# The main distribution script executes this file as follows:
# 
#     'python createLeoDist.py sdist <args>'
# to create Leo's main distribution file, leo-nn.zip.
# 
# N.B. This file is distributed in the dist directory, but it must be run from 
# the
# leo directory, so the main distribution script copies the file (temporarily) 
# to
# the leo directory before running the command above.
#@-at
#@@c

import leoGlobals as g
import distutils.core
import os,sys

#@+others
#@+node:EKR.20040519082027.26:replacePatterns
def replacePatterns (file,pats):

    try:
        path = os.getcwd()
        name  = g.os_path_join(path,file)
        f = open(name)
    except:
        g.trace(file, "not found")
        return
    try:
        data = f.read()
        f.close()
        changed = False
        for pat1,pat2 in pats:
            newdata = data.replace(pat1,pat2)
            if data != newdata:
                changed = True
                data = newdata
                print file,"replaced",pat1,"by",pat2
        if changed:
            f = open(name,"w")
            f.write(data)
            f.close()
    except:
        import traceback ; traceback.print_exc()
        sys.exit()
#@-node:EKR.20040519082027.26:replacePatterns
#@+node:EKR.20040519082027.27:setDefaultParams
def setDefaultParams():

    print "setDefaultParams"

    pats = (
        ("create_nonexistent_directories = 1","create_nonexistent_directories = 0"),
        ("read_only = 1","read_only = 0"),
        ("use_plugins = 1","use_plugins = 0"))

    replacePatterns(g.os_path_join("config","leoConfig.leo"),pats)
    replacePatterns(g.os_path_join("config","leoConfig.txt"),pats)
#@nonl
#@-node:EKR.20040519082027.27:setDefaultParams
#@-others

if 0: # No longer used.
    setDefaultParams()

modules = []
distutils.core.setup (
    #@    << setup info for createLeoDist.py >>
    #@+node:EKR.20040519082027.28:<< setup info for createLeoDist.py >>
    name="leo",
    version="4.3-alpha-1", # No spaces here!
    author="Edward K. Ream",
    author_email="edreamleo@charter.net",
    url="http://webpages.charter.net/edreamleo/front.html",
    py_modules=modules, # leo*.py also included in manifest
    description = "Leo: Literate Editor with Outlines",
    license="Python", # licence [sic] changed to license in Python 2.3
    platforms=["Windows, Linux, Macintosh"],
    long_description =
    """Leo is a powerful programming and scripting environment, outliner, literate
    programming tool, data organizer and project manager. Cloned nodes make possible
    multiple views of a project within a single Leo outline.
    
    Leo is written in 100% pure Python and works on any platform that supports
    Python 2.2 or above and the Tk toolkit. This version of Leo was developed with
    Python 2.3.3 and Tk 8.4.3.
    
    Download Python from http://python.org/
    Download tcl/Tk from http://tcl.activestate.com/software/tcltk/
    
    Leo features a multi-window outlining editor with powerful outline commands,
    support for the noweb markup language, syntax colorizing for many common
    languages, unlimited Undo/Redo, an integrated Python shell(IDLE) window,
    and many user options including user-definable colors and fonts and user-
    definable shortcuts for all menu commands.
     """
    #@nonl
    #@-node:EKR.20040519082027.28:<< setup info for createLeoDist.py >>
    #@nl
)

print "createLeoDist.py complete"
#@nonl
#@-node:EKR.20040519082027.23:@thin createLeoDist.py
#@-leo
