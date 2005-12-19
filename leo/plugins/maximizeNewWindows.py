#@+leo-ver=4-thin
#@+node:ekr.20040915073259.1:@thin maximizeNewWindows.py
"""Maximizes all new windows."""

#@@language python
#@@tabwidth -4

__version__ = "1.0"
#@<< version history >>
#@+node:ekr.20040915073259.2:<< version history >>
#@+at
# 
# Original written by Jaakko Kourula.
# 
# 1.0 EKR:
#     - Enabled only for windows platform.
#     - Minor style changes.
#@-at
#@nonl
#@-node:ekr.20040915073259.2:<< version history >>
#@nl

import leoGlobals as g
import leoPlugins
import sys

def maximize_window(tag, keywords):
    c = keywords["c"]
    c.frame.top.state("zoomed")

# Works only on Windows platform.
if not g.app.unitTesting: # Too annoying.
    if sys.platform == "win32": # Ok for unit test.
        leoPlugins.registerHandler("after-create-leo-frame", maximize_window)
        g.plugin_signon(__name__)
#@nonl
#@-node:ekr.20040915073259.1:@thin maximizeNewWindows.py
#@-leo
