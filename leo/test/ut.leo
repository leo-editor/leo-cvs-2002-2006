<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="239" left="393" height="600" width="800"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="ekr.20051208082927" a="E"><vh>ut.leo</vh>
<v t="ekr.20051208083135"><vh>@asis ut.bat</vh></v>
<v t="ekr.20051208084010" a="TV"><vh>@thin ut.py</vh></v>
</v>
<v t="ekr.20051208082927.1" a="E"><vh>Unit Tests</vh>
<v t="ekr.20051208085841"><vh>@test 1</vh></v>
<v t="ekr.20051208085841.1"><vh>@test 2</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="ekr.20051208082927">@ This file is called from ut.batch.

It should contain quick unit tests to be run in Leo's batch mode.

It also defines ut.bat itself.</t>
<t tx="ekr.20051208082927.1"></t>
<t tx="ekr.20051208083135">cd c:\prog\leoCVS\leo\test
python ..\src\leo.py -script ..\test\ut.py</t>
<t tx="ekr.20051208085841">assert True</t>
<t tx="ekr.20051208085841.1">assert False,'This should fail'</t>
</tnodes>
</leo_file>
