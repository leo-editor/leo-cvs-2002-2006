#@+leo-ver=4-thin
#@+node:EKR.20040517075715.10:@thin vim.py
"""vim handler"""

#@@language python
#@@tabwidth -4

# Contributed by Andrea Galimberti.
# Edited by Felix Breuer.

#  To use this plugin do the following:
#
# - Start VIM as server: vim --servername "LEO"
#   The name of the server *must* be "LEO".
#   If you wish to use a different server with LEO, change the
#   variable _vim_cmd below. If you want Leo to start the VIM server
#   uncomment the corresponding line below.
#
# - Single-click on a node's icon to open that node in VIM.
#
# - Leo will update the node in the outline when you save the file in VIM.

import leoGlobals as g
import leoPlugins
import os

# This command is used to communicate with the vim server. If you use gvim
# you can leave the command as is, you do not need to change it to "gvim ..."

if 1:
    # Works for xp with vim in the folder indicated.
    _vim_cmd = r"c:\vim\vim61\gvim --servername LEO"
    
else: 
    _vim_cmd = "vim --servername LEO"
   

#@+others
#@+node:EKR.20040517075715.11:open_in_vim
def open_in_vim (tag,keywords,val=None):
    
    c = g.top()
    if not c: return
    p = keywords.get("p")
    if not p: return
    v = p.v

    # Find dictionary with infos about this node
    this=filter(lambda x: id(x['v'])==id(v), g.app.openWithFiles)
    
    # Retrieve the name of the temporary file (if any).
    if this != []:  path=this[0]['path']
    else:           path=''

    # if the body has changed we need to open a new 
    # temp file containing the new body in vim
    if  not g.os_path_exists(path) or \
        not hasattr(v,'OpenWithOldBody') or \
        v.bodyString!=v.OpenWithOldBody:
        # if there is an old temp file we need to delete it,
        # remove it from the dictionary and delete the old
        # buffer from vim
        if path != '':
            os.remove(path)
            g.app.openWithFiles=filter(lambda x: x['path']!=path,g.app.openWithFiles)
            os.system(_vim_cmd+"--remote-send '<C-\\><C-N>:bd! "+path+"<CR>'")
        # update old body with new contents
        v.OpenWithOldBody=v.bodyString()
        # open the node in vim (note the space after --remote)
        g.top().openWith(("os.system", _vim_cmd+"--remote ", None),) # 6/27/03: add comma.
    # else, display the old temp file in vim because other files 
    # may have been opened in the meantime
    else:
        # We reopen the file. if it is still open, the buffer is raised
        # if the changes to the current buffer were not saved, vim will
        # notify the user of that fact at this point
        os.system(_vim_cmd+"--remote-send '<C-\\><C-N>:e "+path+"<CR>'")
        
    return val
#@-node:EKR.20040517075715.11:open_in_vim
#@-others

if 1 and not g.app.unitTesting: # Ok for unit testing, but you might want to disable it.
    
    if g.app.unitTesting:
        print '\nvim plugin installed: double-clicking icons will start vim.'

    # Register the handlers...
    if 1: # Open on double click
        leoPlugins.registerHandler("icondclick2", open_in_vim)
    else: # Open on single click: interferes with dragging.
        leoPlugins.registerHandler("iconclick2", open_in_vim,val=True)
    
    # Enable the os.system call if you want to start a (g)vim server.
    if g.app.unitTesting:
        os.system(_vim_cmd)

    __version__ = "1.4" # Set version for the plugin handler.
    g.plugin_signon(__name__)
    
#@nonl
#@-node:EKR.20040517075715.10:@thin vim.py
#@-leo
