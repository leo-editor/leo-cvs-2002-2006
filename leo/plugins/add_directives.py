#@+leo-ver=4-thin
#@+node:edream.110203113231.741:@thin add_directives.py
"""Support new @direcives"""

#@@language python
#@@tabwidth -4

import leoGlobals as g
import leoPlugins

if 1:
    directives = "markup", # A tuple with one string.
else:
    directives = ("markup","markup2")
    
#@+others
#@+node:edream.110203113231.742:addPluginDirectives
def addPluginDirectives (tag,keywords):
    
    """Add all new directives to g.globalDirectiveList"""
    
    global directives

    if 0:
        s = ""
        for d in directives:
            s += '@' + d + ' '
        g.es(s,color="blue")

    for d in directives:
        if d not in g.globalDirectiveList:
            g.globalDirectiveList.append(d)
#@nonl
#@-node:edream.110203113231.742:addPluginDirectives
#@+node:edream.110203113231.743:scanPluginDirectives
def scanPluginDirectives (tag, keywords):
    
    """Add a tuple (d,v,s,k) to list for every directive d found"""
    
    global directives

    keys = ("c","v","s","old_dict","dict","pluginsList")
    c,v,s,old_dict,dict,pluginsList = [keywords.get(key) for key in keys]

    for d in directives:
        if not old_dict.has_key(d) and dict.has_key(d):
            # Point k at whatever follows the directive.
            k = dict[d]
            k += 1 + len(d) # Skip @directive
            k = g.skip_ws(s,k) # Skip whitespace
            # g.trace(`d`,`k`)
            pluginsList.append((d,v,s,k),)
#@-node:edream.110203113231.743:scanPluginDirectives
#@-others

if not g.app.unitTesting:

    # Register the handlers...
    leoPlugins.registerHandler("start1",addPluginDirectives)
    leoPlugins.registerHandler("scan-directives",scanPluginDirectives)
    
    __version__ = "1.1"
    g.plugin_signon(__name__)
#@nonl
#@-node:edream.110203113231.741:@thin add_directives.py
#@-leo
