<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="2344" clone_windows="0"/>
<globals body_outline_ratio="0.44343434343434346">
	<global_window_position top="17" left="196" height="990" width="1071"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences>
</preferences>
<find_panel_settings>
	<find_string></find_string>
	<change_string></change_string>
</find_panel_settings>
<vnodes>
<v t="ekr.20040301204729"><vh>Root</vh></v>
<v t="ekr.20040126105605" a="E"><vh>Clone test</vh>
<v t="ekr.20040126105605.1"><vh>moving last b up destroys the outline!!</vh></v>
<v t="ekr.20040126105605.2" a="E"><vh>a</vh>
<v t="ekr.20040126105605.3" a="E"><vh>b</vh>
<v t="ekr.20040301191933"><vh>c</vh></v>
</v>
<v t="ekr.20040126105605.3"><vh>b</vh>
<v t="ekr.20040301191933"><vh>c</vh></v>
</v>
</v>
<v t="ekr.20040301191933.1" a="E"><vh>d</vh>
<v t="ekr.20040126105605.2"><vh>a</vh>
<v t="ekr.20040126105605.3"><vh>b</vh>
<v t="ekr.20040301191933"><vh>c</vh></v>
</v>
<v t="ekr.20040126105605.3"><vh>b</vh>
<v t="ekr.20040301191933"><vh>c</vh></v>
</v>
</v>
</v>
<v t="ekr.20040301191933.2"><vh>e</vh></v>
</v>
<v t="ekr.20040301162657" a="E"><vh>Tests position code first</vh>
<v t="ekr.20040301162657.1"><vh>test moveToThreadNext</vh></v>
<v t="ekr.20040301164036"><vh>test vnodeList &amp; clones</vh></v>
<v t="ekr.20040301203156" a="TV"><vh>test only clone area</vh></v>
<v t="ekr.20040301214206"><vh>override save commands</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="ekr.20040126105605"></t>
<t tx="ekr.20040126105605.1"></t>
<t tx="ekr.20040126105605.2"></t>
<t tx="ekr.20040126105605.3"></t>
<t tx="ekr.20040301162657"></t>
<t tx="ekr.20040301162657.1"></t>
<t tx="ekr.20040301164036"></t>
<t tx="ekr.20040301191933"></t>
<t tx="ekr.20040301191933.1"></t>
<t tx="ekr.20040301191933.2"></t>
<t tx="ekr.20040301203156">import leoApp
from leoGlobals import *

c = top()
c.convertTreeToSharedNodes()
c.disableSaveCommands()

print ; print "start"

p = c.rootPosition()
while p and p.v.headString().strip().lower() != "clone test":
	p.moveToThreadNext()
	
after = p.copy().moveToNodeAfterTree()
while p and p != after:
	print p.level(), p.v.headString()
	p.moveToThreadNext()
		
print ; print "done"

</t>
<t tx="ekr.20040301204729"></t>
<t tx="ekr.20040301214206">from leoGlobals import *

c = top()
c.disableSaveCommands()</t>
</tnodes>
</leo_file>
