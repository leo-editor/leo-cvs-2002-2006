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
import os
import sys
#@nonl
#@-node:ekr.20050218024153:<< imports >>
#@nl
__version__ = "1.7"
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
# 1.6 MCM
#     - Added sections from Vim mode and some clean-up.
# 1.7 EKR
#     - Select _emacs_cmd using sys.platform.
#@-at
#@nonl
#@-node:ekr.20050218024153.1:<< version history >>
#@nl

useDoubleClick = True

# Full path of emacsclient executable. We need the full path as spawnlp
# is not yet implemented in leoCommands.py

if sys.platform == "win32":
    # This path must not contain blanks in XP.  Sheesh.
    _emacs_cmd = r"c:\XEmacs\XEmacs-21.4.13\i586-pc-win32\xemacs.exe"
else:
    _emacs_cmd = "/Applications/Emacs.app/Contents/MacOS/bin/emacsclient"

#@+others
#@+node:ekr.20050218023308:init
def init ():

    ok = True

    if g.app.unitTesting:
        print "\nEmacs plugin installed: double clicking will start..."

    if useDoubleClick: # Open on double click
        leoPlugins.registerHandler("icondclick2", open_in_emacs)
    else: # Open on single click: interferes with dragging.
        leoPlugins.registerHandler("iconclick2", open_in_emacs,val=True)
    
    
    if g.app.unitTesting:
        os.system(_emacs_cmd)
    
    g.plugin_signon(__name__)
    
    return ok
    

def open_in_emacs (tag,keywords,val=None):
    
    c = g.top()
    if not c: return
    p = keywords.get("p")
    if not p: return
    v = p.v

    # Find dictionary with infos about this node
    this=filter(lambda x: id(x['v'])==id(v),g.app.openWithFiles)
    
    # Retrieve the name of the temporary file (if any).
    if this != []:  path=this[0]['path']
    else:           path=''

    # if the body has changed we need to open a new 
    # temp file containing the new body in emacs
    if  not g.os_path_exists(path) or \
        not hasattr(v,'OpenWithOldBody') or \
        v.bodyString!=v.OpenWithOldBody:
        # if there is an old temp file we need to delete it,
        # remove it from the dictionary and delete the old
        # buffer
        if path != '':
            os.remove(path)
            g.app.openWithFiles=filter(lambda x: x['path']!=path,g.app.openWithFiles)
            os.system(_emacs_cmd)
        # update old body with new contents
        v.OpenWithOldBody=v.bodyString()
        # open the node in emacs (note the space after _emacs_cmd)
        g.top().openWith(("os.spawnl", _emacs_cmd, None),) #mcm 9/III/05
    # else, display the old temp file in vim because other files 
    # may have been opened in the meantime
    else:
        # We reopen the file. if it is still open, the buffer is raised
        # if the changes to the current buffer were not saved, vim will
        # notify the user of that fact at this point
        os.system(_emacs_cmd)
        
    return val
#@nonl
#@-node:ekr.20050218023308:init
#@-others
#@nonl
#@-node:EKR.20040517075715.12:@thin xemacs.py
#@-leo
