#@+leo-ver=4-thin
#@+node:EKR.20040517080049.4:@thin open_shell.py
#@<< docstring >>
#@+node:ekr.20050111112200:<< docstring >>
'''
Creates an 'extensions' menu with commands to open either an xterm on linux
or a cmd windows/explorer window on win32 in the directory of the current @file.
This allows quick navigation to facilitate testing and navigating large systems
with complex direcgtories.

Please submit bugs / feature requests to etaekema@earthlink.net

Current limitations:
- Not tested on Mac OS X ...
- On linux, xterm must be in your path.
'''
#@nonl
#@-node:ekr.20050111112200:<< docstring >>
#@nl

# Written by Ed Taekema.  Modified by EKR

#@@language python
#@@tabwidth -4

__version__ = "0.6"

#@<< version history >>
#@+node:ekr.20040909100119:<< version history >>
#@+at
# 
# 0.5 EKR:
#     - Generalized the code for any kind of @file node.
#     - Changed _getpath so that explicit paths in @file nodes override @path 
# directives.
# 0.6 EKR:
#     - Moved most docs into the docstring.
#@-at
#@nonl
#@-node:ekr.20040909100119:<< version history >>
#@nl
#@<< imports >>
#@+node:ekr.20040909100226:<< imports >>

import leoGlobals as g
import leoPlugins

import leo
import os
import sys
#@nonl
#@-node:ekr.20040909100226:<< imports >>
#@nl

# Changes these as required.
if sys.platform == "win32":
    pathToExplorer = 'c:/windows/explorer.exe'
    pathToCmd = 'c:/windows/system32/cmd.exe'
else:
    # FIXME: Set these...
    pathToExplorer = ''
    pathToCmd = ''

#@+others
#@+node:EKR.20040517080049.6:load_menu
def load_menu(tag,keywords):
    
    if sys.platform=="win32":
        table = (
            ("&Open Console Window",None,launchCmd),
            ("Open &Explorer",None,launchExplorer)) 
    else:
        table = ( ("Open &xterm",None,launchxTerm), ) 
    
    g.top().frame.menu.createNewMenu("E&xtensions","top")
    g.top().frame.menu.createMenuItemsFromTable("Extensions",table)
#@-node:EKR.20040517080049.6:load_menu
#@+node:EKR.20040517080049.7:_getpath
def _getpath(c,v):

    dict = g.scanDirectives(c,p=v)
    d = dict.get("path")
    
    if v.isAnyAtFileNode():
        filename = v.anyAtFileNodeName()
        filename = g.os_path_join(d,filename)
        if filename:
            d = g.os_path_dirname(filename)

    if d is None:
        return ""
    else:
        return g.os_path_normpath(d)
#@nonl
#@-node:EKR.20040517080049.7:_getpath
#@+node:EKR.20040517080049.8:_getCurrentNodePath
def _getCurrentNodePath():

    c = g.top()
    v = c.currentVnode()
    d = _getpath(c,v)
    return d
#@-node:EKR.20040517080049.8:_getCurrentNodePath
#@+node:EKR.20040517080049.9:launchCmd
def launchCmd(event=None):
    
    global pathToCmd

    d = _getCurrentNodePath()
    myCmd = 'cd ' + d
    os.spawnl(os.P_NOWAIT, pathToCmd, '/k ', myCmd)
#@nonl
#@-node:EKR.20040517080049.9:launchCmd
#@+node:EKR.20040517080049.10:launchExplorer
def launchExplorer(event=None):
    
    global pathToExplorer

    d = _getCurrentNodePath()
    os.spawnl(os.P_NOWAIT,pathToExplorer, ' ', d)

#@-node:EKR.20040517080049.10:launchExplorer
#@+node:EKR.20040517080049.11:launchxTerm
def launchxTerm(not_used):

    d = _getCurrentNodePath()
    curdir = os.getcwd()
    os.chdir(d)
    os.spawnlp(os.P_NOWAIT, 'xterm', '-title Leo')
    os.chdir(curdir)
#@nonl
#@-node:EKR.20040517080049.11:launchxTerm
#@-others

if 1: # Ok for unit testing: creates a new menu.

    # Register the handlers...
    leoPlugins.registerHandler("after-create-leo-frame", load_menu)

    g.plugin_signon(__name__)
#@nonl
#@-node:EKR.20040517080049.4:@thin open_shell.py
#@-leo
