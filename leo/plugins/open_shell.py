#@+leo-ver=4-thin
#@+node:EKR.20040517080049.4:@file-thin open_shell.py
"""Opens up cmd and explorer window to same directory 
as @file nodes or children ..."""

#@@language python
#@@tabwidth -4

#@<< about the open shell plugin >>
#@+node:EKR.20040517080049.5:<< about the open shell plugin >>
#@+at 
#@nonl
# Written by Ed Taekema.  Modified by E.K.Ream
# 
# Please submit bugs / feature requests to etaekema@earthlink.net"""
# 
# This is a simple plugin for leo 3.12 that allows the user to open either an 
# xterm on linux or a cmd windows/explorer window on win32 in the directory of 
# the current @file.  This allows quick navigation to facilitate testing and 
# navigating large systems with complex direcgtories.
# 
# Current limitations ...
# 
# 1. Not tested on Mac OS X ...
# 2. On win32, the cmd window will not open in the right directory if the 
# @file location is on a different drive than the .leo file that is being 
# edited.
# 3. On linux, xterm must be in your path.
#@-at
#@-node:EKR.20040517080049.5:<< about the open shell plugin >>
#@nl

import leoGlobals as g
import leoPlugins

import leo
import os
import sys

pathToExplorer = 'c:/windows/explorer.exe'
pathToCmd = 'c:/windows/system32/cmd.exe'

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

    if d == None:

        if v.isAtFileNode():
            filename = v.atFileNodeName()
        if v.isAtNoSentinelsFileNode():
            filename = v.atNoSentinelsFileNodeName()
        if v.isAtRawFileNode():
            filename = v.atRawFileNodeName()
        if v.isAtSilentFileNode():
            filename = v.atSilentFileNodeName()

        d = os.path.dirname(filename)

    d = os.path.normpath(d)
    return d
#@-node:EKR.20040517080049.7:_getpath
#@+node:EKR.20040517080049.8:_getcurrentnodepath
def _getCurrentNodePath():
    c = leo.top()
    v = c.currentVnode()
    f = v.atFileNodeName()
    d = _getpath(c,v)
    return d
#@-node:EKR.20040517080049.8:_getcurrentnodepath
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

# Register the handlers...
leoPlugins.registerHandler("after-create-leo-frame", load_menu)

__version__ = "1.4"
g.plugin_signon(__name__)
#@nonl
#@-node:EKR.20040517080049.4:@file-thin open_shell.py
#@-leo
