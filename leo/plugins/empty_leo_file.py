#@+leo-ver=4-thin
#@+node:EKR.20040517080049.1:@file-thin empty_leo_file.py
"""Open any empty file as a minimal .leo file"""

#@@language python
#@@tabwidth -4

import leoGlobals as g
import leoPlugins

#@<< define minimal .leo file >>
#@+node:EKR.20040517080049.2:<< define minimal .leo file >>
empty_leo_file = """<?xml version="1.0" encoding="iso-8859-1"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5">
    <global_window_position top="145" left="110" height="24" width="80"/>
    <global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences allow_rich_text="0">
</preferences>
<find_panel_settings>
    <find_string></find_string>
    <change_string></change_string>
</find_panel_settings>
<vnodes>
<v a="V"><vh>NewHeadline</vh></v>
</vnodes>
<tnodes>
</tnodes>
</leo_file>"""
#@nonl
#@-node:EKR.20040517080049.2:<< define minimal .leo file >>
#@nl
#@+others
#@+node:EKR.20040517080049.3:onOpen
def onOpen (tag,keywords):

    import os
    file_name = keywords.get('fileName')

    if file_name and os.path.getsize(file_name)==0:
        # Rewrite the file before really opening it.
        g.es("rewriting empty .leo file: %s" % (file_name))
        file = open(file_name,'w')
        file.write(empty_leo_file)
        file.flush()
        file.close()

#@-node:EKR.20040517080049.3:onOpen
#@-others

# Register the handlers...
leoPlugins.registerHandler("open1", onOpen)

__version__ = "1.2"
g.plugin_signon(__name__)
#@nonl
#@-node:EKR.20040517080049.1:@file-thin empty_leo_file.py
#@-leo
