#@+leo-ver=4-thin
#@+node:EKR.20040517075715.12:@thin xemacs.py
"""emacs handler"""

#@@language python
#@@tabwidth -4

import leoGlobals as g
import leoPlugins

# path = "/usr/bin/gnuclient"
path = r"c:\Program Files\XEmacs\XEmacs-21.4.13\i586-pc-win32\xemacs.exe"

def open_in_emacs (tag,keywords):
    g.top() and g.top().openWith(("os.spawnl",path,None),)

if not g.app.unitTesting: # Register the handlers...

    if 1: # Edit when double-clicking a node's icon.
        leoPlugins.registerHandler("icondclick2", open_in_emacs) # 1/29/03: activate on _double_ click.
    else: # Edit when selecting any node. That's a bit much for my taste.
        leoPlugins.registerHandler("select2", open_in_emacs)
    
    __version__ = "1.4"
    g.plugin_signon(__name__)
#@nonl
#@-node:EKR.20040517075715.12:@thin xemacs.py
#@-leo
