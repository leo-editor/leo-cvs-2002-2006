#@+leo-ver=4-thin
#@+node:EKR.20040517075715.12:@thin xemacs.py
'''This plugin allows you to edit nodes in emacs/xemacs.

Depending on your preference, selecting or double-clicking a node will pass the
body text of that node to emacs. You may edit the node in the emacs buffer and
changes will appear in Leo. '''

#@@language python
#@@tabwidth -4

#@<< imports >>
#@+node:ekr.20050218024153:<< imports >>
import leoGlobals as g
import leoPlugins
import sys
#@nonl
#@-node:ekr.20050218024153:<< imports >>
#@nl
__version__ = "1.5"
#@<< version history >>
#@+node:ekr.20050218024153.1:<< version history >>
#@@killcolor
#@+at
# 
# Initial version: http://www.cs.mu.oz.au/~markn/leo/external_editors.leo
# 
# 1.5 EKR:
#     - Added commander-specific callback in onCreate.
#     - Added init method.
#@-at
#@nonl
#@-node:ekr.20050218024153.1:<< version history >>
#@nl

use_double_click = True
    # True:  Edit when double-clicking a node's icon.
    # False: Edit when selecting any node (a bit much for my taste).

# Set this to the path to emacs/xemacs.
if sys.platform == "win32":
    # N.B.  This path must not contain blanks in XP.  Sheesh.
    path_to_emacs = r"c:\XEmacs\XEmacs-21.4.13\i586-pc-win32\xemacs.exe"
    #g.trace('norm',g.os_path_normpath(path_to_emacs))
    #g.trace('abs ',g.os_path_abspath(path_to_emacs))
else:
    path_to_emacs = "/usr/bin/gnuclient"

#@+others
#@+node:ekr.20050218023308:init
def init ():
    
    ok = g.os_path_exists(g.os_path_abspath(path_to_emacs))

    if ok:
        if g.app.unitTesting: # Probably will never happen now...
            print '\nxemacs plugin installed: double-clicking icons will start xemacs.'

        leoPlugins.registerHandler("after-create-leo-frame",onCreate)
        g.plugin_signon(__name__)
        
    else:
        print 'bad path to emacs:',path_to_emacs

    return ok
#@nonl
#@-node:ekr.20050218023308:init
#@+node:ekr.20050218023308.1:onCreate
def onCreate (tag,keywords):

    c = keywords.get("c")
    if not c: return
    
    # Define a commander-specific callback.
    def open_in_emacs_callback(*args):
        open_in_emacs(c)
        
    handler = g.choose(use_double_click,'icondclick2','select2')
    
    leoPlugins.registerHandler(handler,open_in_emacs_callback)
#@nonl
#@-node:ekr.20050218023308.1:onCreate
#@+node:ekr.20050218032201:open_in_emacs
def open_in_emacs(c):

    p = c.currentPosition()
    if not p: return

    if 0:
        # Path must end in a blank!
        c.openWith(('os.system',path_to_emacs+' ',None),)
    else:
        c.openWith(("os.spawnl",path_to_emacs,None),)
#@nonl
#@-node:ekr.20050218032201:open_in_emacs
#@-others
#@nonl
#@-node:EKR.20040517075715.12:@thin xemacs.py
#@-leo
