#@+leo-ver=4-thin
#@+node:EKR.20040517075715.10:@file-thin vim.py
"""vim handler"""

#@@language python

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

import leoPlugins
import leoGlobals as g
from leoGlobals import true,false

# This command is used to communicate with the vim server. If you use gvim
# you can leave the command as is, you do not need to change it to "gvim ..."
# Note: _vim_cmd must end with a space.

_vim_cmd = r"c:\vim\vim61\gvim --servername LEO"
_vim_cmd = "vim --servername LEO "

#@+others
#@+node:EKR.20040517075715.11:open_in_vim
def open_in_vim (tag,keywords):
	if not g.top():
		return

	v=keywords['v']
	# Find dictionary with infos about this node
	this=filter(lambda x: id(x['v'])==id(v), g.app.openWithFiles)
	
	# Retrieve the name of the temporary file (if any).
	if this != []:
		path=this[0]['path']
	else:
		path=''
	
	# if the body has changed we need to open a new 
	# temp file containing the new body in vim
	if  not os.path.exists(path) or \
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
#@-node:EKR.20040517075715.11:open_in_vim
#@-others

# Register the handlers...
leoPlugins.registerHandler("iconclick2", open_in_vim)

# if you want to start a (g)vim server when leo is started
# uncomment this line:
# os.system("gvim --servername LEO")

__version__ = "1.4" # Set version for the plugin handler.
g.plugin_signon(__name__)
#@-node:EKR.20040517075715.10:@file-thin vim.py
#@-leo
