#! /usr/bin/env python
#@+leo-ver=4-thin
#@+node:EKR.20040519082027.23:@thin createLeoDist.py
#@@first
#@@color

#@+at 
#@nonl
# The main distribution script executes this file as follows:
# 
#     'python createLeoDist.py sdist <args>'
# 
# to create Leo's main distribution file, leo-nn.zip.
# 
# N.B. This file is distributed in the dist directory, but it must be run from 
# the
# leo directory, so the main distribution script copies the file (temporarily) 
# to
# the leo directory before running the command above.
#@-at
#@@c

import distutils.core

distutils.core.setup (
    #@    << setup info for createLeoDist.py >>
    #@+node:EKR.20040519082027.28:<< setup info for createLeoDist.py >>
    name="leo",
    version="4-4-a7", # No spaces here!
    author="Edward K. Ream",
    author_email="edreamleo@charter.net",
    url="http://webpages.charter.net/edreamleo/front.html",
    py_modules=[], # The manifest specifies everything.
    description = "Leo: Literate Editor with Outlines",
    license="Python", # licence [sic] changed to license in Python 2.3
    platforms=["Windows, Linux, Macintosh"],
    long_description =
    """Leo is a powerful programming and scripting environment, outliner, literate
    programming tool, data organizer and project manager. Cloned nodes make possible
    multiple views of a project within a single Leo outline.
    
    Leo is written in 100% pure Python and works on any platform that supports
    Python 2.2.1 or above and the Tk Tk 8.4 or above.
    
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
