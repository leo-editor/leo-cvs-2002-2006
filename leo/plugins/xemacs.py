#@+leo-ver=4-thin
#@+node:EKR.20040517075715.12:@thin xemacs.py
"""emacs handler

http://www.cs.mu.oz.au/~markn/leo/external_editors.leo"""

#@@language python
#@@tabwidth -4

import leoGlobals as g
import leoPlugins
import sys

if sys.platform == "win32":
    # Modify this pth as needed.
    path = r"c:\Program Files\XEmacs\XEmacs-21.4.13\i586-pc-win32\xemacs.exe"
else: # Linux
    path = "/usr/bin/gnuclient"

def open_in_emacs (tag,keywords):
    g.top() and g.top().openWith(("os.spawnl",path,None),)

# Ok for unit testing, but you might want to disable it.
if 1 or not g.app.unitTesting:
    
    if g.app.unitTesting:
        print '\nxemacs plugin installed: double-clicking icons will start xemacs.'

    if 1: # Edit when double-clicking a node's icon.
        leoPlugins.registerHandler("icondclick2", open_in_emacs) # Activate on _double_ click.
    else: # Edit when selecting any node. That's a bit much for my taste.
        leoPlugins.registerHandler("select2", open_in_emacs)
    
    __version__ = "1.4"
    g.plugin_signon(__name__)
#@nonl
#@-node:EKR.20040517075715.12:@thin xemacs.py
#@-leo
