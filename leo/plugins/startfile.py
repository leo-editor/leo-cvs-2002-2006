#@+leo-ver=4-thin
#@+node:EKR.20040422094618:@thin startfile.py
"""Lauches (starts) a file with the name of the headline on double-clicking it.
Uses the @folder path if the headline is under an @folder headline.
Otherwise the path is relative to the Leo file.
Headlines starting with an '@' are ignored.
This does not work on Linux, because the Python function os.startfile is not
supported under Linux.
"""

# By Josef Dalcolmo: contributed under the same license as Leo.py itself.

import leoGlobals as g
import leoPlugins

import os

#@<< about this plugin >>
#@+node:EKR.20040422094618.1:<<about this plugin >>
#@+at 
#@nonl
# This plugin starts a file with the name of a headline.
#@-at
#@nonl
#@-node:EKR.20040422094618.1:<<about this plugin >>
#@nl
#@<< change log >>
#@+node:EKR.20040422094618.2:<< change log >>
#@+at 
#@nonl
# Change log
# 
# - JD: 2003-03-11 separated out from rst plugin
# - JD: 2004-04-18 change the defaultdir to the folder of the file which is 
# being started.
#@-at
#@nonl
#@-node:EKR.20040422094618.2:<< change log >>
#@nl

#@+others
#@+node:EKR.20040422094618.3:onIconDoubleClick
#@+at
# Models @folder behavior after an idea and sample code by:
# korakot ( Korakot Chaovavanich ) @folder for files annotation 2002-11-27 
# 02:39
# 
# open file (double-click = startfile) behavior added
# nodes with @url, @folder, @rst are treated special
# 
# by Josef Dalcolmo 2003-01-13
# 
# This does not check for proper filename syntax.
# path is the current dir, or the place @folder points to
# this should probably be changed to @path or so.
#@-at
#@@c

def onIconDoubleClick(tag,keywords):

    v = keywords.get("p") or keywords.get("v") # Use p for 4.2 code base, v for 4.1 code base.
    c = keywords.get("c")

    if c and v:
        h = v.headString().strip()
        if len(h)==0 or h[0]=='@':
            return # Let other plugins handle these
        else:
            # open file with associated application
            #@            << find path and start file >>
            #@+node:EKR.20040422094618.4:<< find path and start file >>
            # Set the base directory by searching for @folder directives in ancestors.
            thisdir = os.path.abspath(os.curdir) # remember the current dir
            basedir = thisdir[:]	# use current dir as default.
            parv = v.parent()	# start with parent
            while parv:	# stop when no more parent found
                p = parv.headString().strip()
                if g.match_word(p,0,'@folder'):
                    basedir = p[8:]	# take rest of headline as pathname
                    break	# we found the closest @folder
                else:
                    parv = parv.parent()	# try the parent of the parent
            
            fname = os.path.join(basedir,h) # join path and filename
            startdir, filename = os.path.split(fname)
            try:
                os.chdir(startdir)
                dirfound = 1
            except:
                g.es(startdir+' - folder not found')
                dirfound = 0
            
            if dirfound:
                try:
                    os.startfile(filename)	# Try to open the file; it may not work for all file types.
                except:
                    g.es(filename+' - file not found in '+startdir)
                    # g.es_exception()
            os.chdir(thisdir) # restore the original current dir.
            #@nonl
            #@-node:EKR.20040422094618.4:<< find path and start file >>
            #@nl
#@nonl
#@-node:EKR.20040422094618.3:onIconDoubleClick
#@-others

# Register the handlers...
leoPlugins.registerHandler("icondclick1",onIconDoubleClick)

__version__ = "1.3"
g.plugin_signon(__name__)

def unitTest ():
    pass
#@nonl
#@-node:EKR.20040422094618:@thin startfile.py
#@-leo
