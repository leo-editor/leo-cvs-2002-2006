#! /usr/bin/env python
#@+leo-ver=4-thin
#@+node:EKR.20040519082027.23:@thin ../createLeoDist.py
#@@first

import leoGlobals as g

import distutils.core
import os,sys

#@+others
#@+node:EKR.20040519082027.24:printReminders
def printReminders ():

    print
    print "- Update version numbers"
    print "- Clear Default Tangle Directory"
    print "- Distribute both leox-y.zip and leosetup.exe"
    print
#@nonl
#@-node:EKR.20040519082027.24:printReminders
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

setDefaultParams()

modules = []
distutils.core.setup (
    #@    << setup info for createLeoDist.py >>
    #@+node:EKR.20040519082027.28:<< setup info for createLeoDist.py >> (no spaces in file names)
    name="leo",
    version="4.3-pre-alpha-chipy-talk",
    author="Edward K. Ream",
    author_email="edreamleo@charter.net",
    url="http://webpages.charter.net/edreamleo/front.html",
    py_modules=modules, # leo*.py also included in manifest
    description = "Leo: Literate Editor with Outlines",
    license="Python", # licence [sic] changed to license in Python 2.3
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
    #@-node:EKR.20040519082027.28:<< setup info for createLeoDist.py >> (no spaces in file names)
    #@nl
)

print "createLeoDist.py complete"
#@nonl
#@-node:EKR.20040519082027.23:@thin ../createLeoDist.py
#@-leo
