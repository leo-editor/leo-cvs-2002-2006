#@+leo-ver=4-thin
#@+node:EKR.20040517075715.10:@thin vim.py
#@<< docstring >>
#@+node:ekr.20050226184411:<< docstring >>
'''A plugin that communicates with VIM.

To use this plugin do the following:

- Start VIM as server:
    
    vim --servername "LEO"
    
The name of the server *must* be "LEO". If you wish to use a different server
with LEO, change the variable _vim_cmd below. If you want Leo to start the VIM
server uncomment the corresponding line below.

- By default, double clickin on a node's icon opens that node in VIM. You can
open nodes in VIM with a single-click if you set useDoubleClick = False.
However, that interfere's with Leo's dragging logic.

- Leo will update the node in the outline when you save the file in VIM.
'''
#@nonl
#@-node:ekr.20050226184411:<< docstring >>
#@nl

#@@language python
#@@tabwidth -4

__version__ = "1.6"
#@<< version history >>
#@+node:ekr.20050226184411.1:<< version history >>
#@@killcolor

#@+at
# 
# Contributed by Andrea Galimberti.
# Edited by Felix Breuer.
# 
# 1.5 EKR:
#     - Added new sections.
#     - Move most comments into docstring.
#     - Added useDoubleClick variable.
#     - Added init function.
#     - Init _vim_cmd depending on sys.platform.
# 
# 1.6 EKR:
#     - Use keywords to get c, not g.top().
#     - Don't use during unit testing: prefer xemacs instead.
#     - Added _vim_exe
#     - Use "os.spawnv" instead of os.system.
#     - Simplified the search of g.app.openWithFiles.
#     - Fixed bug in open_in_vim: hanged v.bodyString to v.bodyString()
#@-at
#@nonl
#@-node:ekr.20050226184411.1:<< version history >>
#@nl
#@<< imports >>
#@+node:ekr.20050226184411.2:<< imports >>
import leoGlobals as g
import leoPlugins
import os
import sys
#@nonl
#@-node:ekr.20050226184411.2:<< imports >>
#@nl

useDoubleClick = True # True: double-click opens VIM.  False: single-click opens VIM.

# This command is used to communicate with the vim server. If you use gvim
# you can leave the command as is, you do not need to change it to "gvim ..."

if sys.platform == 'win32':
    # Works on XP with vim in the folder indicated.
    _vim_cmd = r"c:\vim\vim63\gvim --servername LEO"
    _vim_exe = r"c:\vim\vim63\gvim"
else: 
    _vim_cmd = "vim --servername LEO"
    _vim_exe = "vim"

#@+others
#@+node:ekr.20050226184624:init
def init ():
    
    ok = not g.app.unitTesting # Don't conflict with xemacs plugin.
    
    if ok:
        # Register the handlers...
        if useDoubleClick:
            # Open on double click
            leoPlugins.registerHandler("icondclick2", open_in_vim)
        else:
            # Open on single click: interferes with dragging.
            leoPlugins.registerHandler("iconclick2",open_in_vim,val=True)
        
        # Enable the os.system call if you want to start a (g)vim server when Leo starts.
        if 0:
            os.system(_vim_cmd)
        
        g.plugin_signon(__name__)
    
    return ok
#@nonl
#@-node:ekr.20050226184624:init
#@+node:EKR.20040517075715.11:open_in_vim
def open_in_vim (tag,keywords,val=None):
    
    c = keywords.get('c')
    p = keywords.get("p")
    if not c or not p: return
    v = p.v
    
    # Search g.app.openWithFiles for a file corresponding to v.
    for d in g.app.openWithFiles:
        if d.get('v') == id(v):
            path = d.get('path','') ; break
    else: path = ''

    # if the body has changed we need to open a new 
    # temp file containing the new body in vim
    if (
        not g.os_path_exists(path) or 
        not hasattr(v,'OpenWithOldBody') or
        v.bodyString() != v.OpenWithOldBody
    ):
        # Open a new temp file.
        if path:
            # Remove the old file and the entry in g.app.openWithFiles.
            os.remove(path)
            g.app.openWithFiles = [d for d in g.app.openWithFiles if d.get('path') != path]
            os.system(_vim_cmd+"--remote-send '<C-\\><C-N>:bd! "+path+"<CR>'")
        v.OpenWithOldBody=v.bodyString() # Remember the previous contents.
        # open the node in vim (note the space after --remote)
        if 0: # Works, but hangs Leo until vim exits on XP.
            # Note space after --remote.
            c.openWith(("os.system", _vim_cmd+"--remote ", None),)
        else: # Works, but gives weird error message on first open of Vim.
            c.openWith(("os.spawnv", [_vim_exe,"--servername LEO ","--remote "], None),)
    else:
        # Reopen the old temp file.
        os.system(_vim_cmd+"--remote-send '<C-\\><C-N>:e "+path+"<CR>'")
        
    return val
#@nonl
#@-node:EKR.20040517075715.11:open_in_vim
#@-others
#@nonl
#@-node:EKR.20040517075715.10:@thin vim.py
#@-leo
