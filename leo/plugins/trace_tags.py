#@+leo-ver=4-thin
#@+node:edream.110203113231.738:@file-thin trace_tags.py
"""Trace most comment events, but not key, drag or idle events"""

#@@language python
#@@tabwidth -4

import leoGlobals as g
import leoPlugins

tagCount = 0

#@+others
#@+node:edream.110203113231.739:trace_tags
def trace_tags (tag,keywords):
    
    global tagCount # 8/28/03

    # Almost all tags have both c and v keys in the keywords dict.
    if tag not in ("start1","end1","open1","open2"):
        c = keywords.get("c")
        v = keywords.get("v")
        if not c:
            print tagCount,tag, "c = None"
        if not v:
            if tag not in ("select1","select2","unselect1","unselect2"):
                print tagCount,tag, "v = None"
    
    if tag not in (
        "bodykey1","bodykey2","dragging1","dragging2",
        "headkey1","headkey2","idle"):
    
        tagCount += 1 # Count all other hooks.
    
        if tag in ("command1","command2"):
            print tagCount,tag,keywords.get("label")
        elif tag in ("open1","open2"):
            print tagCount,tag,keywords.get("fileName")
        else:
            if 1: # Brief
                print tagCount,tag
            else: # Verbose
                keys = keywords.items()
                keys.sort()
                for key,value in keys:
                    print tagCount,tag,key,value
                print
#@nonl
#@-node:edream.110203113231.739:trace_tags
#@-others

# Register the handlers...
leoPlugins.registerHandler("all", trace_tags)

__version__ = "1.2" # Set version for the plugin handler.
g.plugin_signon(__name__)
#@nonl
#@-node:edream.110203113231.738:@file-thin trace_tags.py
#@-leo
