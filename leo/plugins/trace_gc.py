#@+leo-ver=4-thin
#@+node:edream.110203113231.735:@file-thin trace_gc.py
"""Trace changes to objects at idle time"""

#@@language python
#@@tabwidth -4

import leoGlobals as g
import leoPlugins

g.debugGC = True # Force debugging on.

def printIdleRefs(tag,keywords):
    g.printGcRefs(verbose=False)
    
gcCount = 0

def printIdleGC(tag,keywords):
    
    # Calling printGc is too expensive to do on every idle call.
    if g.app.killed:
        return # Work around a Tk bug.
    elif if tag == "idle":
        global gcCount ; gcCount += 1
        if (gcCount % 20) == 0:
            g.printGc(tag,onlyPrintChanges=True)
    else:
        g.printGc(tag,onlyPrintChanges=False)

# Register the handlers...
if 1: # Very effective.
    leoPlugins.registerHandler("idle", printIdleGC)
else: # Very precise.
    leoPlugins.registerHandler("all", printIdleGC)
if 0: # Another idea.
    leoPlugins.registerHandler("command2", printIdleRefs)

__version__ = "1.3"
g.plugin_signon(__name__)
#@nonl
#@-node:edream.110203113231.735:@file-thin trace_gc.py
#@-leo
