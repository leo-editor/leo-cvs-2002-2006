#@+leo-ver=4-thin
#@+node:ekr.20040331151007:@thin niceNosent.py
"""Preprocess @file-nosent nodes: make sure each subnode ends
with exactly one newline, replace all tabs with spaces, and
add a newline before class and functions in the derived file.
"""

#@@language python
#@@tabwidth -4

__version__ = "0.2" # Use 
#@<< version history >>
#@+node:ekr.20040909122647:<< version history >>
#@+at
# 
# 0.2 EKR:
#     - Use isAtNoSentinelsFileNode and atNoSentinelsFileNodeName.
#     - Use g.os_path_x methods for better unicode support.
#@-at
#@nonl
#@-node:ekr.20040909122647:<< version history >>
#@nl


#@<< imports >>
#@+node:ekr.20040909122647.1:<< imports >>
import leoGlobals as g
import leoPlugins
import os
#@nonl
#@-node:ekr.20040909122647.1:<< imports >>
#@nl
 


NSPACES = ' '*4
nosentNodes = []

#@+others
#@+node:ekr.20040331151007.1:onPreSave
def onPreSave(tag=None, keywords=None):
    """Before saving a nosentinels file, make sure that all nodes have a blank line at the end."""

    global nosentNodes

    v = g.top().rootVnode()
    while v:
        if v.isAtNoSentinelsFileNode() and v.isDirty():
            nosentNodes.append(v)
            after = v.nodeAfterTree()
            while v and v != after:
                text = v.t.bodyString
                lastline = text.split("\n")[-1]
                if lastline.strip() != "":
                    # add a blank line if necessary
                    v.setBodyStringOrPane(text+"\n")
                v = v.threadNext()
        else:
            v = v.threadNext()
#@-node:ekr.20040331151007.1:onPreSave
#@+node:ekr.20040331151007.2:onPostSave
def onPostSave(tag=None, keywords=None):
    """After saving a nosentinels file, replace all tabs with spaces."""

    global nosentNodes

    for v in nosentNodes:
        #g.es("node %s found" % h, color="red")
        df = v.c.atFileCommands.new_df
        df.scanAllDirectives(v)
        name = v.atNoSentinelsFileNodeName()
        fname = g.os_path_join(df.default_directory,name)
        fh = open(fname,"r")
        lines = fh.readlines()
        fh.close()
        #@        << add a newline before def or class >>
        #@+node:ekr.20040331151007.3:<< add a newline before def or class >>
        for i in range(len(lines)):
            ls = lines[i].lstrip()
            if ls.startswith("def ") or ls.startswith("class "):
                try:
                    if lines[i-1].strip() != "":
                        lines[i] = "\n" + lines[i]
                except IndexError:
                    pass
        #@nonl
        #@-node:ekr.20040331151007.3:<< add a newline before def or class >>
        #@nl
        #@        << replace tabs with spaces >>
        #@+node:ekr.20040331151007.4:<< replace tabs with spaces >>
        s = ''.join(lines)
        fh = open(fname,"w")
        fh.write(s.replace("\t",NSPACES))
        fh.close()
        #@nonl
        #@-node:ekr.20040331151007.4:<< replace tabs with spaces >>
        #@nl

    nosentNodes = []
#@-node:ekr.20040331151007.2:onPostSave
#@-others

if not g.app.unitTesting:

    leoPlugins.registerHandler("save1",onPreSave)
    leoPlugins.registerHandler("save2",onPostSave)
    
   
    g.plugin_signon(__name__)
#@nonl
#@-node:ekr.20040331151007:@thin niceNosent.py
#@-leo
