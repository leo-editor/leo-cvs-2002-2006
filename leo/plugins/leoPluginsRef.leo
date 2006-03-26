<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet ekr_stylesheet?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="6305" clone_windows="0"/>
<globals body_outline_ratio="0.595562130178">
	<global_window_position top="27" left="362" height="850" width="852"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="ekr.20041211035618"><vh>Scripts, buttons &amp; settings</vh>
<v t="EKR.20040517075110"><vh>replaceLeoGlobals</vh>
<v t="EKR.20040517075110.1"><vh>&lt;&lt; set nameList to the list of functions in leoGlobals.py &gt;&gt;</vh></v>
<v t="EKR.20040517075110.2"><vh>findFunctionsInTree</vh></v>
<v t="EKR.20040517075110.3"><vh>findDefs</vh></v>
<v t="EKR.20040517075110.4"><vh>prependNamesInTree</vh>
<v t="EKR.20040517075110.5"><vh>&lt;&lt; look for name followed by '(' &gt;&gt;</vh></v>
<v t="EKR.20040517075110.6"><vh>&lt;&lt; print before and after &gt;&gt;</vh></v>
</v>
</v>
<v t="ekr.20050217093214"><vh>@settings</vh>
<v t="ekr.20050328101812"><vh>@page http plugin</vh>
<v t="ekr.20050328101812.1"><vh>@bool http_active = True</vh></v>
<v t="ekr.20050328101812.2"><vh>@int  port = 8080</vh></v>
<v t="ekr.20050328101812.3"><vh>@string rst_http_attributename = rst_http_attribute</vh></v>
</v>
</v>
<v t="ekr.20041103052443"><vh>Script to find and replace all functions in leoGlobals.py</vh>
<v t="ekr.20041103052443.1"><vh>findFunctionsInTree</vh></v>
<v t="ekr.20041103052443.2"><vh>findDefs</vh></v>
<v t="ekr.20041103052443.3"><vh>prependNamesInTree</vh>
<v t="ekr.20041103052443.4"><vh>&lt;&lt; look for name followed by '(' &gt;&gt;</vh></v>
<v t="ekr.20041103052443.5"><vh>&lt;&lt; print before and after &gt;&gt;</vh></v>
</v>
<v t="ekr.20041103052443.6"><vh>&lt;&lt; set nameList to the list of functions in leoGlobals.py &gt;&gt;</vh></v>
</v>
<v t="ekr.20060109114710"><vh>@button settings.leo</vh></v>
<v t="ekr.20050724100334"><vh>@button Beautify</vh></v>
<v t="ekr.20051025144116"><vh>@button Spell</vh></v>
<v t="ekr.20050819055746"><vh>@button Save</vh></v>
<v t="ekr.20050722075812"><vh>Remove blank trailing lines</vh></v>
</v>
<v t="edream.110203113231.618" a="V"><vh>Plugins</vh>
<v t="EKR.20040517090508"><vh>  Enable plugins by changing pluginsManager.txt or using plugin_manager plugin</vh>
<v t="edream.120603093808"><vh>@thin pluginsManager.txt</vh></v>
</v>
<v t="ekr.20050303051035"><vh> Templates: these show recommended ways of defining plugins.</vh>
<v t="ekr.20041114102139"><vh>Notes</vh>
<v t="ekr.20041114103913"><vh>About comments in the style guide</vh></v>
<v t="ekr.20041114102139.1"><vh>About the root node</vh></v>
<v t="ekr.20041114103913.1"><vh>About defining functions in separate nodes</vh></v>
<v t="ekr.20041114102139.2"><vh>About the &lt;&lt; imports &gt;&gt; section</vh></v>
<v t="ekr.20050306072156"><vh>About exceptions</vh></v>
</v>
<v t="ekr.20050306071629"><vh>Template for plugin that overrides commander methods</vh>
<v t="ekr.20050306071629.1"><vh>&lt;&lt; docstring &gt;&gt;</vh></v>
<v t="ekr.20050306071629.2"><vh>&lt;&lt; version history &gt;&gt;</vh></v>
<v t="ekr.20050306071629.3"><vh>&lt;&lt; imports &gt;&gt;</vh></v>
<v t="ekr.20050306071629.4"><vh>init</vh></v>
<v t="ekr.20050306071540"><vh>onStart2</vh></v>
</v>
<v t="ekr.20050303051035.2"><vh>Template for Tk plugin with per-commander controller class</vh>
<v t="ekr.20050303051035.3"><vh>&lt;&lt; docstring &gt;&gt;</vh></v>
<v t="ekr.20050303051035.4"><vh>&lt;&lt; version history &gt;&gt;</vh></v>
<v t="ekr.20050303051035.5"><vh>&lt;&lt; imports &gt;&gt;</vh></v>
<v t="ekr.20050303051101"><vh>init</vh></v>
<v t="ekr.20050303051150"><vh>onCreate</vh></v>
<v t="ekr.20050303051222"><vh>class pluginController</vh>
<v t="ekr.20050303051222.1"><vh>__init__</vh></v>
</v>
</v>
</v>
<v t="ekr.20060306151759"><vh>Chapters plugin</vh>
<v t="ekr.20060306151759.1"><vh>@thin chapters2.py</vh></v>
</v>
<v t="edream.110203113231.667"><vh>Commands &amp; directives</vh>
<v t="edream.110203113231.668"><vh> Importing Cisco configuration files</vh>
<v t="edream.110203113231.669"><vh>@thin import_cisco_config.py</vh></v>
<v t="edream.110203113231.677"><vh> Example of an imported config</vh>
<v t="edream.110203113231.678"><vh>plain configuration</vh></v>
<v t="edream.110203113231.679"><vh>cisco config: C:/Davide/Leo/CVS Version/example_conf.txt</vh>
<v t="edream.110203113231.680"><vh>&lt;&lt;access-list&gt;&gt;</vh></v>
<v t="edream.110203113231.681"><vh>&lt;&lt;boot&gt;&gt;</vh></v>
<v t="edream.110203113231.682"><vh>&lt;&lt;controller&gt;&gt;</vh>
<v t="edream.110203113231.683"><vh>controller E1 5/0/0</vh></v>
<v t="edream.110203113231.684"><vh>controller E1 5/0/1</vh></v>
<v t="edream.110203113231.685"><vh>controller SONET 1/0/0</vh></v>
</v>
<v t="edream.110203113231.686"><vh>&lt;&lt;interface&gt;&gt;</vh>
<v t="edream.110203113231.687"><vh>interface Async1</vh></v>
<v t="edream.110203113231.688"><vh>interface Dialer0</vh></v>
<v t="edream.110203113231.689"><vh>interface FastEthernet0/0/0</vh></v>
<v t="edream.110203113231.690"><vh>interface FastEthernet0/0/1</vh></v>
<v t="edream.110203113231.691"><vh>interface FastEthernet0/0/1.1</vh></v>
<v t="edream.110203113231.692"><vh>interface FastEthernet0/0/1.2</vh></v>
<v t="edream.110203113231.693"><vh>interface FastEthernet0/0/1.3</vh></v>
<v t="edream.110203113231.694"><vh>interface FastEthernet0/0/1.5</vh></v>
<v t="edream.110203113231.695"><vh>interface FastEthernet0/0/1.50</vh></v>
<v t="edream.110203113231.696"><vh>interface Loopback0</vh></v>
<v t="edream.110203113231.697"><vh>interface POS4/1/0</vh></v>
<v t="edream.110203113231.698"><vh>interface Serial5/0/0:1</vh></v>
<v t="edream.110203113231.699"><vh>interface Serial5/0/0:2</vh></v>
<v t="edream.110203113231.700"><vh>interface Serial5/0/1:0</vh></v>
<v t="edream.110203113231.701"><vh>interface Serial5/1/0</vh></v>
<v t="edream.110203113231.702"><vh>interface Serial5/1/1</vh></v>
</v>
<v t="edream.110203113231.703"><vh>&lt;&lt;ip community-list&gt;&gt;</vh></v>
<v t="edream.110203113231.704"><vh>&lt;&lt;ip route&gt;&gt;</vh></v>
<v t="edream.110203113231.705"><vh>&lt;&lt;line&gt;&gt;</vh>
<v t="edream.110203113231.706"><vh>line aux 0</vh></v>
<v t="edream.110203113231.707"><vh>line vty 0 4</vh></v>
</v>
<v t="edream.110203113231.708"><vh>&lt;&lt;logging&gt;&gt;</vh></v>
<v t="edream.110203113231.709"><vh>&lt;&lt;ntp&gt;&gt;</vh></v>
<v t="edream.110203113231.710"><vh>&lt;&lt;route-map&gt;&gt;</vh>
<v t="edream.110203113231.711"><vh>route-map only permit 2</vh></v>
<v t="edream.110203113231.712"><vh>route-map only1 permit 10</vh></v>
<v t="edream.110203113231.713"><vh>route-map only3 permit 10</vh></v>
<v t="edream.110203113231.714"><vh>route-map tag_com permit 10</vh></v>
<v t="edream.110203113231.715"><vh>route-map tag_com permit 20</vh></v>
</v>
<v t="edream.110203113231.716"><vh>&lt;&lt;router&gt;&gt;</vh>
<v t="edream.110203113231.717"><vh>router bgp 65001</vh></v>
<v t="edream.110203113231.718"><vh>router ospf 1</vh></v>
</v>
<v t="edream.110203113231.719"><vh>&lt;&lt;service&gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="edream.110203113231.741"><vh>@thin add_directives.py</vh></v>
<v t="timo.20050213160555"><vh>@thin bibtex.py</vh></v>
<v t="ekr.20040916073636"><vh>@thin ConceptualSort.py</vh></v>
<v t="ekr.20040915105758.13"><vh>@thin FileActions.py</vh></v>
<v t="mork.20041018131258.1"><vh>@thin groupOperations.py</vh></v>
<v t="ekr.20050328092641.4"><vh>@thin Library.py</vh></v>
<v t="ekr.20040916084945"><vh>@thin macros.py</vh></v>
<v t="ekr.20050301083306"><vh>@thin mod_read_dir_outline.py</vh></v>
<v t="edream.110203113231.727"><vh>@thin mod_timestamp.py</vh></v>
<v t="edream.110203113231.720"><vh>@thin outline_export.py</vh></v>
<v t="ekr.20041021120118"><vh>@thin pretty_print.py</vh></v>
<v t="ekr.20040331153923"><vh>@thin scheduler.py</vh></v>
<v t="mork.20041022090036.1"><vh>@thin templates.py</vh></v>
<v t="ekr.20041215103252"><vh>datenodes</vh>
<v t="gfunch.20041207100416"><vh>@thin datenodes.py</vh></v>
<v t="gfunch.20041209063345.1"><vh>@thin datenodes.ini</vh></v>
</v>
<v t="edream.110203113231.722"><vh>mod_autosave</vh>
<v t="edream.110203113231.723" tnodeList="edream.110203113231.723"><vh>@file-nosent mod_autosave.ini</vh></v>
<v t="edream.110203113231.724"><vh>@thin mod_autosave.py</vh></v>
</v>
<v t="ekr.20041110104350"><vh>table plugin: requires tktable</vh>
<v t="ekr.20041017035937"><vh>@thin table.py</vh></v>
</v>
</v>
<v t="edream.110203113231.729"><vh>Debugging &amp;  testing</vh>
<v t="edream.110203113231.730"><vh>@thin dump_globals.py</vh></v>
<v t="edream.110203113231.732"><vh>@thin enable_gc.py</vh></v>
<v t="ekr.20050130120433"><vh>@thin failed_import.py</vh></v>
<v t="edream.110203113231.734"><vh>@thin quit_leo.py</vh></v>
<v t="ekr.20051016160700"><vh>@thin testRegisterCommand.py</vh></v>
<v t="edream.110203113231.735"><vh>@thin trace_gc_plugin.py</vh></v>
<v t="edream.110203113231.736"><vh>@thin trace_keys.py</vh></v>
<v t="edream.110203113231.738"><vh>@thin trace_tags.py</vh></v>
<v t="ekr.20040205071616"><vh>mnplugins.py</vh>
<v t="ekr.20050101090717"><vh>&lt;&lt; docstring &gt;&gt;</vh></v>
<v t="ekr.20050101090717.1"><vh>&lt;&lt; imports &gt;&gt;</vh></v>
<v t="ekr.20040205071616.1"><vh>mnstamp</vh></v>
<v t="ekr.20040205071616.2"><vh>mnOKstamp</vh></v>
<v t="ekr.20040205071616.3"><vh>onStart</vh></v>
<v t="ekr.20040205071616.4"><vh>setHeadOK</vh></v>
<v t="ekr.20040205071616.5"><vh>insertBodystamp</vh></v>
<v t="ekr.20040205071616.6"><vh>is_subnodesOK</vh></v>
<v t="ekr.20040205071616.7"><vh>onRclick</vh></v>
<v t="ekr.20040205071616.8"><vh>insertOKcmd</vh></v>
<v t="ekr.20040205071616.9"><vh>insertUser</vh></v>
<v t="ekr.20040205071616.10"><vh>create_UserMenu</vh></v>
</v>
</v>
<v t="ekr.20041030092101"><vh>Dyna plugins by e</vh>
<v t="ekr.20060110125615"><vh>@url http://rclick.netfirms.com/dyna_menu.py.html  (dyna plugin)</vh></v>
</v>
<v t="edream.110203113231.872"><vh>Enhanced nodes...</vh>
<v t="edream.110203113231.873"><vh>@thin at_folder.py</vh></v>
<v t="ekr.20040915085351"><vh>@thin at_produce.py</vh></v>
<v t="ktenney.20041211072654.1"><vh>@thin at_view.py</vh></v>
<v t="mork.20041020082242.1"><vh>@thin base64Packager.py</vh></v>
<v t="mork.20041018091414.1"><vh>@thin fastGotoNode.py</vh></v>
<v t="ekr.20050301095332"
expanded="ekr.20050301095332.37,ekr.20050301095332.40,ekr.20050301095332.44,ekr.20050301095332.48,ekr.20050301095332.49,ekr.20050301095332.53,ekr.20050301095332.57,"><vh>@thin mod_labels.py</vh></v>
<v t="edream.110203113231.876"><vh>@thin read_only_nodes.py</vh></v>
<v t="ekr.20040910070811.1"><vh>@thin run_nodes.py</vh></v>
<v t="ekr.20040828103325"><vh>@thin startfile.py</vh></v>
<v t="ekr.20050329082101"><vh>AutoTrees</vh>
<v t="ekr.20050329082101.1"><vh>AutoTrees plugin</vh>
<v t="ekr.20050329082101.2"><vh>Introduction</vh></v>
<v t="ekr.20050329082101.3"><vh>Why use this?</vh></v>
<v t="ekr.20050329082101.4"><vh>Details</vh></v>
<v t="ekr.20050329082101.5"><vh>How do I create my own handlers?</vh></v>
</v>
<v t="ekr.20050329082101.6" annotate="7d71002e"><vh>Example handlers</vh>
<v t="ekr.20050329082101.7"><vh>Testing</vh>
<v t="ekr.20050329082101.8" annotate="7d71002e"><vh>@auto-test something</vh>
<v t="ekr.20050329082101.9"><vh>one</vh></v>
<v t="ekr.20050329082101.10"><vh>two</vh></v>
<v t="ekr.20050329082101.11"><vh>three</vh>
<v t="ekr.20050329082101.12"><vh>three-one</vh></v>
<v t="ekr.20050329082101.13"><vh>three-two</vh></v>
<v t="ekr.20050329082101.14"><vh>three-three</vh></v>
</v>
</v>
</v>
<v t="ekr.20050329082101.15"><vh>RSS</vh>
<v t="ekr.20050329082101.16"><vh>@auto-rss http://news.bbc.co.uk/rss/newsonline_uk_edition/world/rss091.xml</vh>
<v t="ekr.20050329092553"><vh>Hundreds die in Indonesia quake</vh></v>
<v t="ekr.20050329092553.1"><vh>Ousted Kyrgyz president defiant</vh></v>
<v t="ekr.20050329092553.2"><vh>Hair 'good source of stem cells'</vh></v>
<v t="ekr.20050329092553.3"><vh>Ashdown sacks top Bosnian Croat</vh></v>
<v t="ekr.20050329092553.4"><vh>Splits paralyse Iraqi parliament</vh></v>
<v t="ekr.20050329092553.5"><vh>Mongolians protest for new poll</vh></v>
<v t="ekr.20050329092553.6"><vh>Libya's Bulgarian medics appeal</vh></v>
<v t="ekr.20050329092553.7"><vh>Schiavo rivals 'agree to autopsy'</vh></v>
<v t="ekr.20050329092553.8"><vh>Would-be sex tourist, 87, jailed</vh></v>
<v t="ekr.20050329092553.9"><vh>Golf: Funk claims Players title</vh></v>
<v t="ekr.20050329092553.10"><vh>Cricket: Series win for Aussies</vh></v>
<v t="ekr.20050329092553.11"><vh>Angola says virus 'under control'</vh></v>
<v t="ekr.20050329092553.12"><vh>Mugabe criticises MDC 'traitors'</vh></v>
<v t="ekr.20050329092553.13"><vh>Ex-US diplomats round on Bolton</vh></v>
<v t="ekr.20050329092553.14"><vh>Brazil quits loan accord with IMF</vh></v>
<v t="ekr.20050329092553.15"><vh>Japanese economy hit by weak data</vh></v>
<v t="ekr.20050329092553.16"><vh>Donors pledge $40m for KR trials</vh></v>
<v t="ekr.20050329092553.17"><vh>Three Romanians missing in Iraq</vh></v>
<v t="ekr.20050329092553.18"><vh>Wolfowitz 'to meet EU officials'</vh></v>
<v t="ekr.20050329092553.19"><vh>Knesset rejects Gaza referendum</vh></v>
<v t="ekr.20050329092553.20"><vh>Militants to attend PLO meeting</vh></v>
<v t="ekr.20050329092553.21"><vh>South Asia cancels tsunami alerts</vh></v>
<v t="ekr.20050329092553.22"><vh>Devastation as Afghan dam bursts</vh></v>
<v t="ekr.20050329092553.23"><vh>Kyrgyzstan's friendly revolution</vh></v>
</v>
<v t="ekr.20050329082101.40" annotate="7d71002e"><vh>@auto-rss http://slashdot.org/index.rss</vh>
<v t="ekr.20050329092553.24"><vh>Followup on MS and Brazil in NY Times</vh></v>
<v t="ekr.20050329092553.25"><vh>A9.com with Syndicated Search</vh></v>
<v t="ekr.20050329092553.26"><vh>What's Next At Apple</vh></v>
<v t="ekr.20050329092553.27"><vh>Berkeley Grads' Identity Data Stolen</vh></v>
<v t="ekr.20050329092553.28"><vh>South Korean Gov't. Advocates Linux</vh></v>
<v t="ekr.20050329092553.29"><vh>MS, EU Agree on Name for Windows Sans Media Player</vh></v>
<v t="ekr.20050329092553.30"><vh>Blackbox (Finally) Updated</vh></v>
<v t="ekr.20050329092553.31"><vh>Your Face On the Big Screen</vh></v>
<v t="ekr.20050329092553.32"><vh>Ars Technica Builds Make Magazine's Steadicam</vh></v>
<v t="ekr.20050329092553.33"><vh>New Photovoltaics Made with Titanium Foil</vh></v>
</v>
<v t="ekr.20050329082101.51"><vh>@auto-rss http://www.python.org/channews.rdf</vh>
<v t="ekr.20050329082101.52"><vh>Python 2.4.1 (release candidate 1)</vh></v>
<v t="ekr.20050329082101.53"><vh>Greg Stein, of Google and Apache Software Foundation, to deliver keynote at PyCon</vh></v>
<v t="ekr.20050329082101.54"><vh>New RSS feed for python-dev summaries</vh></v>
<v t="ekr.20050329082101.55"><vh>Guido van Rossum speaking in Palo Alto</vh></v>
<v t="ekr.20050329082101.56"><vh>Python 2.3.5 (final)</vh></v>
<v t="ekr.20050329082101.57"><vh>Security advisory for SimpleXMLRPCServer.py.</vh></v>
<v t="ekr.20050329082101.58"><vh>Deadline for OSCON proposals</vh></v>
<v t="ekr.20050329082101.59"><vh>PyCon abstracts now available</vh></v>
<v t="ekr.20050329082101.60"><vh>PyCon preliminary schedule now available</vh></v>
<v t="ekr.20050329082101.61"><vh>PSF has awarded three grants</vh></v>
<v t="ekr.20050329082101.62"><vh>Python for Nokia Series 60 now available</vh></v>
<v t="ekr.20050329082101.63"><vh>Python 2.4 (final)</vh></v>
<v t="ekr.20050329082101.64"><vh>PyZine issue 7</vh></v>
<v t="ekr.20050329082101.65"><vh>PyCon 2005 Call for Proposals</vh></v>
<v t="ekr.20050329082101.66"><vh>Cameron Laird receives the Frank Willison Award</vh></v>
</v>
</v>
<v t="ekr.20050329082101.67"><vh>Remote</vh>
<v t="ekr.20050329082101.68"><vh>@auto-remote http://www.bbc.co.uk/news.html</vh></v>
</v>
<v t="ekr.20050329082101.69"><vh>Documentation</vh>
<v t="ekr.20050329082101.70"><vh>@auto-doc docutils.core</vh>
<v t="ekr.20050329082101.71"><vh>Component</vh>
<v t="ekr.20050329082101.72"><vh>component_type</vh></v>
<v t="ekr.20050329082101.73"><vh>default_transforms</vh></v>
<v t="ekr.20050329082101.74"><vh>supports</vh></v>
</v>
<v t="ekr.20050329082101.75"><vh>ConfigParser</vh>
<v t="ekr.20050329082101.76"><vh>OPTCRE</vh></v>
<v t="ekr.20050329082101.77"><vh>SECTCRE</vh></v>
<v t="ekr.20050329082101.78"><vh>add_section</vh></v>
<v t="ekr.20050329082101.79"><vh>standard_config_files</vh></v>
<v t="ekr.20050329082101.80"><vh>validation</vh></v>
</v>
<v t="ekr.20050329082101.81"><vh>OptionParser</vh>
<v t="ekr.20050329082101.82"><vh>default_error_encoding_error_handler</vh></v>
<v t="ekr.20050329082101.83"><vh>relative_path_settings</vh></v>
<v t="ekr.20050329082101.84"><vh>settings_defaults</vh></v>
<v t="ekr.20050329082101.85"><vh>settings_spec</vh></v>
<v t="ekr.20050329082101.86"><vh>standard_option_list</vh></v>
<v t="ekr.20050329082101.87"><vh>threshold_choices</vh></v>
<v t="ekr.20050329082101.88"><vh>thresholds</vh></v>
<v t="ekr.20050329082101.89"><vh>version_template</vh></v>
</v>
<v t="ekr.20050329082101.90"><vh>Publisher</vh></v>
<v t="ekr.20050329082101.91"><vh>default_description</vh></v>
<v t="ekr.20050329082101.92"><vh>default_usage</vh></v>
<v t="ekr.20050329082101.93"><vh>frontend</vh></v>
<v t="ekr.20050329082101.94"><vh>io</vh></v>
<v t="ekr.20050329082101.95"><vh>parsers</vh></v>
<v t="ekr.20050329082101.96"><vh>publish_cmdline</vh></v>
<v t="ekr.20050329082101.97"><vh>publish_file</vh></v>
<v t="ekr.20050329082101.98"><vh>publish_string</vh></v>
<v t="ekr.20050329082101.99"><vh>readers</vh></v>
<v t="ekr.20050329082101.100"><vh>sys</vh></v>
<v t="ekr.20050329082101.101"><vh>writers</vh></v>
</v>
</v>
<v t="ekr.20050329082101.102"><vh>News Reader</vh>
<v t="ekr.20050329082101.103"><vh>@auto-news news-server.houston.rr.com/comp.lang.python</vh>
<v t="ekr.20050329082101.104"><vh>@auto-newsitem 356970 - Easy way to check modules for python version compatibility?</vh></v>
<v t="ekr.20050329082101.105"><vh>@auto-newsitem 356972 - Q: Module Shared Data</vh></v>
<v t="ekr.20050329082101.106"><vh>@auto-newsitem 356978 - Re: __contains__ inconsistencies between Python 2.2 and 2.3</vh></v>
<v t="ekr.20050329082101.107"><vh>@auto-newsitem 356979 - Re: [Numeric] column vector faster than row vector in mat multiply?</vh></v>
<v t="ekr.20050329082101.108"><vh>@auto-newsitem 356986 - Python 2.4 removes None data type?</vh></v>
<v t="ekr.20050329082101.109"><vh>@auto-newsitem 356987 - Re: Integer From A Float List?!?</vh></v>
<v t="ekr.20050329082101.110"><vh>@auto-newsitem 356988 - Suspicious header</vh></v>
<v t="ekr.20050329082101.111"><vh>@auto-newsitem 356991 - Re: Suspicious header</vh></v>
<v t="ekr.20050329082101.112"><vh>@auto-newsitem 356992 - survey</vh></v>
<v t="ekr.20050329082101.113"><vh>@auto-newsitem 356993 - Re: Python 2.4 removes None data type?</vh></v>
</v>
</v>
</v>
<v t="ekr.20050329082101.114"><vh>AutoTrees Code</vh>
<v t="ekr.20050329082101.115"><vh>@thin autotrees.py</vh></v>
<v t="ekr.20050329082101.145"><vh>@--thin trees\pluginsManager.txt</vh></v>
<v t="ekr.20050329082101.146"><vh>Example tree handlers</vh>
<v t="ekr.20050329082101.147"><vh>@--thin trees\test.py</vh>
<v t="ekr.20050329082101.148"><vh>&lt;&lt; docstring &gt;&gt;</vh></v>
<v t="ekr.20050329082101.149"><vh>&lt;&lt; version history &gt;&gt;</vh></v>
</v>
<v t="ekr.20050329082101.150"><vh>@--thin trees\rss.py</vh>
<v t="ekr.20050329082101.151"><vh>&lt;&lt; docstring &gt;&gt;</vh></v>
<v t="ekr.20050329082101.152"><vh>&lt;&lt; version history &gt;&gt;</vh></v>
</v>
<v t="ekr.20050329082101.153"><vh>@--thin trees\news.py</vh>
<v t="ekr.20050329082101.154"><vh>&lt;&lt; docstring &gt;&gt;</vh></v>
<v t="ekr.20050329082101.155"><vh>&lt;&lt; version history &gt;&gt;</vh></v>
<v t="ekr.20050329082101.156"><vh>Error Classes</vh></v>
<v t="ekr.20050329082101.157"><vh>getConnection</vh></v>
<v t="ekr.20050329082101.158"><vh>class News</vh>
<v t="ekr.20050329082101.159"><vh>initFrom</vh></v>
</v>
<v t="ekr.20050329082101.160"><vh>class NewsItem</vh>
<v t="ekr.20050329082101.161"><vh>initFrom</vh></v>
</v>
</v>
<v t="ekr.20050329082101.162"><vh>@--thin trees\remote.py</vh>
<v t="ekr.20050329082101.163"><vh>&lt;&lt; docstring &gt;&gt;</vh></v>
<v t="ekr.20050329082101.164"><vh>&lt;&lt; version history &gt;&gt;</vh></v>
</v>
<v t="ekr.20050329082101.165"><vh>@--thin trees\doc.py</vh>
<v t="ekr.20050329082101.166"><vh>&lt;&lt; docstring &gt;&gt;</vh></v>
<v t="ekr.20050329082101.167"><vh>&lt;&lt; version history &gt;&gt;</vh></v>
</v>
</v>
</v>
</v>
</v>
<v t="ekr.20040722135402.1"><vh>Enhancing the body pane</vh>
<v t="edream.110203113231.753"><vh>@thin image.py</vh></v>
<v t="ekr.20040422072343"><vh>@thin rClick.py</vh></v>
<v t="edream.110403140857"><vh>color_markup.py (requires add-directives plugin)</vh>
<v t="edream.110403140857.1"><vh>Plugin documentation</vh>
<v t="edream.110403140857.2"><vh>Installation</vh></v>
<v t="edream.110403140857.3"><vh>Use</vh>
<v t="edream.110403140857.4"><vh>Supported markups</vh></v>
<v t="edream.110403140857.5"><vh>Example</vh>
<v t="edream.110403140857.6"><vh>a subnode</vh></v>
</v>
</v>
<v t="edream.110403140857.7"><vh>Release notes</vh></v>
</v>
<v t="edream.110403140857.8"><vh>@thin color_markup.py</vh></v>
</v>
<v t="edream.110203113231.925"><vh>@thin script_io_to_body.py</vh></v>
</v>
<v t="ekr.20040722135402"><vh>Enhancing the icon and status areas</vh>
<v t="edream.110203113231.758"><vh>@thin nav_buttons.py</vh></v>
<v t="pap.20051010170720"><vh>@thin newButtons.py</vh></v>
<v t="ekr.20040331072607"><vh>@thin hoist.py</vh></v>
<v t="ekr.20040108062655"><vh>@thin nodenavigator.py</vh></v>
<v t="ekr.20040108095351"><vh>@thin rowcol.py</vh></v>
<v t="ekr.20040107092135.2"><vh>@thin searchbox.py</vh></v>
<v t="rogererens.20041013082304"><vh>@thin UNL.py</vh></v>
</v>
<v t="ekr.20040915073259"><vh>Enhancing windows</vh>
<v t="ekr.20050227071948" annotate="5404010000376437313030323835353038373037323639366637323639373437393731303132383633363136653665366637343631373436353061353436623530363936333662366336353536363137323061373130323666373130333464306632373632353530343665366636343635373130353238363830323666373130363535303734363635363137343735373236353731303736323535303236323637373130383238363830323666373130393535303037313061363235353039363137323633363836353734373937303635373130623238363830323666373130633638306136323535303236363637373130643238363830323666373130653638306136323735326571002e"><vh> cleo</vh>
<v t="ekr.20050227072121"><vh>Notes</vh>
<v t="ekr.20050227071948.1" annotate="7d71002e"><vh>TODO</vh>
<v t="ekr.20050227071948.2" annotate="7d71002e"><vh>pixmap icons</vh></v>
<v t="ekr.20050227071948.3" annotate="7d71002e"><vh>colour selector</vh></v>
<v t="ekr.20050227071948.4" annotate="55f037643731303032383535303837303732363936663732363937343739373130313238363336313665366536663734363137343635306135343662353036393633366236633635353636313732306137313032366637313033346236343632353530343665366636343635373130353238363830323666373130363535303037313037363235353032363236373731303832383638303236663731303936383037363235353039363137323633363836353734373937303635373130613238363830323666373130623638303736323535303236363637373130633238363830323666373130643638303736323735326571002e"><vh>popup location</vh></v>
<v t="ekr.20050227071948.5" annotate="5592376437313030323835353038373037323639366637323639373437393731303132383633363136653665366637343631373436353061353436623530363936333662366336353536363137323061373130323666373130333462303136323535303936313732363336383635373437393730363537313035323836383032366637313036353530303731303736323735326571002e"><vh>EKR's intentions on @thin nodes</vh>
<v t="ekr.20050227071948.6" annotate="5592376437313030323835353038373037323639366637323639373437393731303132383633363136653665366637343631373436353061353436623530363936333662366336353536363137323061373130323666373130333462303136323535303936313732363336383635373437393730363537313035323836383032366637313036353530303731303736323735326571002e"><vh>No attributes for @thin nodes</vh></v>
</v>
<v t="ekr.20050227071948.7" annotate="7d71002e"><vh>group annotations</vh></v>
<v t="ekr.20050227071948.8" annotate="7d71002e"><vh>archetype based search,navigation</vh></v>
<v t="ekr.20050227071948.9" annotate="7d71002e"><vh>sort by type</vh></v>
<v t="ekr.20050227071948.10" annotate="7d71002e"><vh>fonts</vh></v>
<v t="ekr.20050227071948.11" annotate="55f037643731303032383535303837303732363936663732363937343739373130313238363336313665366536663734363137343635306135343662353036393633366236633635353636313732306137313032366637313033346230323632353530343665366636343635373130353238363830323666373130363535303037313037363235353032363236373731303832383638303236663731303936383037363235353039363137323633363836353734373937303635373130613238363830323666373130623638303736323535303236363637373130633238363830323666373130643638303736323735326571002e"><vh>question marks</vh></v>
</v>
<v t="ekr.20050227071948.12" annotate="54000100003764373130303238353530383730373236393666373236393734373937313031323836333631366536653666373436313734363530613534366235303639363336623663363535363631373230613731303236663731303334623634363235353034366536663634363537313035323836383032366637313036353530303731303736323535303236323637373130383238363830323666373130393535303635303735373237303663363537313061363235353039363137323633363836353734373937303635373130623238363830323666373130633638303736323535303236363637373130643238363830323666373130653638303736323735326571002e"><vh>Done</vh>
<v t="ekr.20050227071948.13" annotate="7d71005509617474656e74696f6e71014930300a732e"><vh>Clear All markings</vh></v>
<v t="ekr.20050227071948.14" annotate="54120100003764373130303238353530343665366636343635373130313238363336313665366536663734363137343635306135343662353036393633366236633635353636313732306137313032366637313033353530303731303536323535303236323637373130363238363830323666373130373638303536323535303936313734373436353665373436393666366537313038343933303331306135353038373037323639366637323639373437393731303932383638303236663731306134623634363235353032363636373731306232383638303236663731306336383035363235353039363137323633363836353734373937303635373130643238363830323666373130653638303536323735326571002e"><vh>autoleo node colouring</vh></v>
<v t="ekr.20050227071948.15" annotate="5592376437313030323835353038373037323639366637323639373437393731303132383633363136653665366637343631373436353061353436623530363936333662366336353536363137323061373130323666373130333462363436323535303936313732363336383635373437393730363537313035323836383032366637313036353530303731303736323735326571002e"><vh>arbitary colouring</vh></v>
<v t="ekr.20050227071948.16" annotate="55f037643731303032383535303837303732363936663732363937343739373130313238363336313665366536663734363137343635306135343662353036393633366236633635353636313732306137313032366637313033346236343632353530343665366636343635373130353238363830323666373130363535303037313037363235353032363236373731303832383638303236663731303936383037363235353039363137323633363836353734373937303635373130613238363830323666373130623638303736323535303236363637373130633238363830323666373130643638303736323735326571002e"><vh>rename to cleo</vh></v>
<v t="ekr.20050227071948.17" annotate="7d71002e"><vh>headline colours</vh></v>
<v t="ekr.20050227071948.18" annotate="7d71005509617474656e74696f6e71014930300a732e"><vh>priority colouring</vh></v>
<v t="ekr.20050227071948.19" annotate="7d71005509617474656e74696f6e71014930300a732e"><vh>archtetype colouring</vh></v>
</v>
<v t="ekr.20050227071948.20" annotate="7d71002e"><vh>Problems</vh>
<v t="ekr.20050227071948.6" annotate="5592376437313030323835353038373037323639366637323639373437393731303132383633363136653665366637343631373436353061353436623530363936333662366336353536363137323061373130323666373130333462303136323535303936313732363336383635373437393730363537313035323836383032366637313036353530303731303736323735326571002e"><vh>No attributes for @thin nodes</vh></v>
<v t="ekr.20050227071948.21" annotate="5592376437313030323835353038373037323639366637323639373437393731303132383633363136653665366637343631373436353061353436623530363936333662366336353536363137323061373130323666373130333462303236323535303936313732363336383635373437393730363537313035323836383032366637313036353530303731303736323735326571002e"><vh>features are not orthogonal</vh></v>
<v t="ekr.20050227071948.22" annotate="7d71002e"><vh>Too many colours !!</vh></v>
</v>
<v t="ekr.20050227071948.23" annotate="5404010000376437313030323835353038373037323639366637323639373437393731303132383633363136653665366637343631373436353061353436623530363936333662366336353536363137323061373130323666373130333464306632373632353530343665366636343635373130353238363830323666373130363535303734363635363137343735373236353731303736323535303236323637373130383238363830323666373130393535303037313061363235353039363137323633363836353734373937303635373130623238363830323666373130633638306136323535303236363637373130643238363830323666373130653638306136323735326571002e"><vh>BUGS</vh>
<v t="ekr.20050227071948.24" annotate="55f037643731303032383535303837303732363936663732363937343739373130313238363336313665366536663734363137343635306135343662353036393633366236633635353636313732306137313032366637313033346236343632353530343665366636343635373130353238363830323666373130363535303037313037363235353032363236373731303832383638303236663731303936383037363235353039363137323633363836353734373937303635373130613238363830323666373130623638303736323535303236363637373130633238363830323666373130643638303736323735326571002e"><vh>popup location</vh></v>
</v>
<v t="ekr.20050227071948.27" annotate="7d71002e"><vh>colour table</vh></v>
<v t="ekr.20050227071948.28" annotate="54060100003764373130303238353530383730373236393666373236393734373937313031323836333631366536653666373436313734363530613534366235303639363336623663363535363631373230613731303236663731303334643066323736323535303436653666363436353731303532383638303236663731303635353038343336663664366436353665373437333731303736323535303236323637373130383238363830323666373130393535303037313061363235353039363137323633363836353734373937303635373130623238363830323666373130633638306136323535303236363637373130643238363830323666373130653638306136323735326571002e"><vh>Notes</vh>
<v t="ekr.20050227071948.29" annotate="7d71002e"><vh>drawing hooks</vh></v>
</v>
</v>
<v t="ekr.20050227071948.33" annotate="540c0100003764373130303238353530383730373236393666373236393734373937313031323836333631366536653666373436313734363530613534366235303639363336623663363535363631373230613731303236663731303334643066323736323535303436653666363436353731303532383638303236663731303635353034363636393663363537313037363235353032363236373731303832383638303236663731303935353030373130613632353530393631373236333638363537343739373036353731306232383638303236663731306335353035346637343638363537323731306436323535303236363637373130653238363830323666373130663638306136323735326571002e"><vh>@thin cleo.py</vh></v>
</v>
<v t="ekr.20050303080042"><vh> footprints</vh>
<v t="ekr.20050303080236"><vh>To do</vh></v>
<v t="ekr.20050303080042.1" tnodeList="ekr.20050303080042.1"><vh>@nosent footprints.ini</vh></v>
<v t="pap.20041020001240"><vh>@thin footprints.py</vh></v>
</v>
<v t="mork.20041018162155.1"><vh>@thin EditAttributes.py</vh></v>
<v t="ekr.20040915073259.1"><vh>@thin maximizeNewWindows.py</vh></v>
<v t="mork.20041022155742.1"><vh>@thin nodebar.py</vh></v>
<v t="edream.110203113231.924"><vh>@thin redirect_to_log.py</vh></v>
<v t="ekr.20040915075530"><vh>@thin UASearch.py</vh></v>
<v t="ekr.20040831122004"><vh>@thin UniversalScrolling.py</vh></v>
<v t="ekr.20040831115238"><vh>@thin URLloader.py</vh></v>
</v>
<v t="ekr.20040722141148"><vh>Example code</vh>
<v t="edream.110203113231.916"><vh>@thin __overrideClasses.py</vh></v>
<v t="edream.110203113231.919"><vh>@thin override_commands.py</vh></v>
<v t="edream.110203113231.921"><vh>@thin redefine_put.py</vh></v>
</v>
<v t="ekr.20040722134535"><vh>Experimental/unfinished</vh>
<v t="ekr.20050915064008"><vh>@thin __vnx__.py</vh></v>
<v t="ekr.20050612074047"><vh>New colorizer</vh>
<v t="ekr.20050529180421"><vh>jEdit docs...</vh>
<v t="ekr.20050530065723"><vh>@url http://www.jedit.org/42docs/users-guide/writing-modes-part.html</vh></v>
<v t="ekr.20050529180421.1"><vh>Rule ordering</vh></v>
<v t="ekr.20050529180421.2"><vh>Attributes</vh>
<v t="ekr.20050529180421.3"><vh> Documentation of attributes</vh>
<v t="ekr.20050529180421.4"><vh> For 'seq', 'span', 'begin', 'end'</vh>
<v t="ekr.20050529180421.5"><vh>AT_LINE_START (bool)</vh></v>
<v t="ekr.20050529180421.6"><vh>AT_WHITESPACE_END (bool)</vh></v>
<v t="ekr.20050529180421.7"><vh>AT_WORD_START (bool)</vh></v>
</v>
<v t="ekr.20050529180421.8"><vh> For 'span' only</vh>
<v t="ekr.20050529180421.9"><vh>NO_WORD_BREAK (bool)</vh></v>
<v t="ekr.20050529180421.10"><vh>NO_LINE_BREAK (bool)</vh></v>
<v t="ekr.20050529180421.11"><vh>NO_ESCAPE (bool)</vh></v>
<v t="ekr.20050529180421.12"><vh>EXCLUDE_MATCH (bool)</vh></v>
</v>
<v t="ekr.20050529180421.13"><vh> For 'rules' only</vh>
<v t="ekr.20050529180421.14"><vh>DEFAULT</vh></v>
<v t="ekr.20050529180421.15"><vh>DIGIT_RE (re) &amp; HIGHLIGHT_DIGITS  (bool)</vh></v>
<v t="ekr.20050529180421.16"><vh>IGNORE_CASE (bool)</vh></v>
<v t="ekr.20050529180421.17"><vh>SET</vh></v>
<v t="ekr.20050529180421.18"><vh>NO_WORD_SEP</vh></v>
</v>
<v t="ekr.20050529180421.19"><vh>AT_CHAR (int) for 'terminate'</vh></v>
<v t="ekr.20050529180421.20"><vh>DELEGATE: for 'import', 'span' &amp; 'seq'</vh></v>
<v t="ekr.20050529180421.21"><vh>HASH_CHAR (char) For 'regx'</vh></v>
<v t="ekr.20050529180421.22"><vh>TYPE (Token Types)</vh></v>
</v>
<v t="ekr.20050529180421.23"><vh>Attributes for 'begin' &amp; 'end'</vh></v>
<v t="ekr.20050529180421.24"><vh>Attributes for 'import': delegate</vh></v>
<v t="ekr.20050529180421.25"><vh>Attributes for 'mark' </vh></v>
<v t="ekr.20050529180421.26"><vh>Attributes for 'property': name, value</vh></v>
<v t="ekr.20050529180421.27"><vh>Attributes for 'rules'</vh></v>
<v t="ekr.20050529180421.28"><vh>Attributes for 'span'</vh></v>
<v t="ekr.20050529180421.29"><vh>Attributes for 'seq' </vh></v>
</v>
<v t="ekr.20050529180421.30"><vh>Elements</vh>
<v t="ekr.20050529220821"><vh>Spans and seqs...</vh>
<v t="ekr.20050529180421.31"><vh>eol_span</vh></v>
<v t="ekr.20050529180421.32"><vh>eol_span_regexp</vh></v>
<v t="ekr.20050529180421.35"><vh>mark_following</vh></v>
<v t="ekr.20050529180421.36"><vh>mark_previous</vh></v>
<v t="ekr.20050529180421.40"><vh>seq</vh></v>
<v t="ekr.20050529180421.41"><vh>seq_regexp</vh></v>
<v t="ekr.20050529180421.42"><vh>span</vh></v>
<v t="ekr.20050529180421.43"><vh>span_regexp</vh></v>
</v>
<v t="ekr.20050529220821.1"><vh>All others...</vh>
<v t="ekr.20050529180421.33"><vh>import</vh></v>
<v t="ekr.20050529180421.34"><vh>keywords</vh></v>
<v t="ekr.20050529180421.37"><vh>mode</vh></v>
<v t="ekr.20050529180421.38"><vh>props &amp; property  (for auto-indent)</vh></v>
<v t="ekr.20050529180421.39"><vh>rules</vh></v>
<v t="ekr.20050529180421.44"><vh>terminate</vh></v>
</v>
</v>
</v>
<v t="ekr.20050529142847"><vh>@thin __jEdit_colorizer__.py</vh></v>
<v t="ekr.20050606214954"><vh>(state methods)</vh>
<v t="ekr.20050529143413.30"><vh>colorize (Main entry point)</vh></v>
<v t="ekr.20050529143413.31"><vh>colorizeAnyLanguage</vh></v>
<v t="ekr.20050602205810.4"><vh>colorRangeWithTag</vh></v>
</v>
<v t="ekr.20050606221357"><vh>(init)</vh>
<v t="ekr.20050602150619"><vh>init_mode</vh></v>
<v t="ekr.20050602152743"><vh>init_keywords</vh>
<v t="ekr.20050607073917"><vh>&lt;&lt; compute extra_word_chars &gt;&gt;</vh></v>
</v>
<v t="ekr.20050530065723.47"><vh>parse_jEdit_file</vh></v>
</v>
<v t="ekr.20050607220512"><vh>(delegate)</vh>
<v t="ekr.20050601105358"><vh>colorOneChunk</vh>
<v t="ekr.20050605130806"><vh>&lt;&lt; queue up this method the first time &gt;&gt;</vh></v>
<v t="ekr.20050601162452.1"><vh>&lt;&lt; queue up this method &gt;&gt;</vh></v>
</v>
<v t="ekr.20050607212958"><vh>colorByDelegate</vh></v>
<v t="ekr.20050602205810.4"><vh>colorRangeWithTag</vh></v>
</v>
</v>
<v t="ekr.20040717133342"><vh>Shadow files plugin</vh>
<v t="ekr.20050126104457"><vh>Notes</vh></v>
<v t="bwmulder.20041017125718"><vh>@thin mod_shadow.py</vh></v>
</v>
<v t="ekr.20040918165427"><vh>To do</vh>
<v t="EKR.20040611044600"><vh>Mulder undo</vh>
<v t="bwmulder.20040601212737"><vh>basic_undo.py</vh>
<v t="bwmulder.20040601212737.1"><vh>class passthrough</vh>
<v t="bwmulder.20040601212737.2"><vh>__init__</vh></v>
<v t="bwmulder.20040601212737.3"><vh>__set__</vh></v>
<v t="bwmulder.20040601212737.4"><vh>__get__</vh></v>
</v>
<v t="bwmulder.20040601212737.5"><vh>class scalar_monitor</vh>
<v t="bwmulder.20040601212737.6"><vh>__init__</vh></v>
<v t="bwmulder.20040601212737.7"><vh>__set__</vh></v>
<v t="bwmulder.20040601212737.8"><vh>__get__</vh></v>
</v>
<v t="bwmulder.20040601212737.9"><vh>class list_monitor</vh>
<v t="bwmulder.20040605231305"><vh>__init__</vh></v>
<v t="bwmulder.20040601212737.10"><vh>set_monitor_object</vh></v>
<v t="bwmulder.20040601212737.11"><vh>__setitem__</vh></v>
<v t="bwmulder.20040601212737.12"><vh>__delitem__</vh></v>
<v t="bwmulder.20040601212737.13"><vh>append</vh></v>
<v t="bwmulder.20040602152548"><vh>pop</vh></v>
</v>
<v t="bwmulder.20040601212737.14"><vh>class list_monitor_in_instance</vh>
<v t="bwmulder.20040601212737.15"><vh>__init__</vh></v>
<v t="bwmulder.20040601212737.16"><vh>__set__</vh></v>
<v t="bwmulder.20040601212737.17"><vh>__get__</vh></v>
</v>
<v t="bwmulder.20040602153618"><vh>class dict_monitor</vh>
<v t="bwmulder.20040605231401"><vh>__init__</vh></v>
<v t="bwmulder.20040602153642"><vh>set_monitor_object</vh></v>
<v t="bwmulder.20040602153723"><vh>__setitem__</vh></v>
<v t="bwmulder.20040602153835"><vh>__delitem__</vh></v>
</v>
<v t="bwmulder.20040602154259"><vh>class  dict_monitor_in_instance</vh>
<v t="bwmulder.20040602154259.1"><vh>__init__</vh></v>
<v t="bwmulder.20040602154259.2"><vh>__set__</vh></v>
<v t="bwmulder.20040602154259.3"><vh>__get__</vh></v>
</v>
<v t="bwmulder.20040601212737.18"><vh>class monitor</vh>
<v t="bwmulder.20040601212737.19"><vh>__init__</vh></v>
<v t="bwmulder.20040601214251"><vh>scalars</vh>
<v t="bwmulder.20040601212737.20"><vh>monitor_scalar</vh></v>
<v t="bwmulder.20040601212737.24"><vh>scalar_set</vh></v>
<v t="bwmulder.20040601212737.25"><vh>scalar_modify</vh></v>
</v>
<v t="bwmulder.20040601215339"><vh>lists</vh>
<v t="bwmulder.20040601212737.21"><vh>monitor_list_attribute_in_class</vh></v>
<v t="bwmulder.20040601212737.26"><vh>list_create</vh></v>
<v t="bwmulder.20040601212737.27"><vh>list_set</vh></v>
<v t="bwmulder.20040601212737.28"><vh>list_del</vh></v>
<v t="bwmulder.20040601212737.29"><vh>list_append</vh></v>
</v>
<v t="bwmulder.20040602165344"><vh>dicts</vh>
<v t="bwmulder.20040602165402"><vh>monitor_dict_attribute_in_class</vh></v>
<v t="bwmulder.20040602165506"><vh>dict_create</vh></v>
<v t="bwmulder.20040602165513"><vh>dict_set</vh></v>
<v t="bwmulder.20040602165553"><vh>dict_del</vh></v>
</v>
<v t="bwmulder.20040601215339.1"><vh>switching on and off</vh>
<v t="bwmulder.20040601212737.22"><vh>enable</vh></v>
<v t="bwmulder.20040602164627"><vh>enable_put_in_removed_functions</vh></v>
<v t="bwmulder.20040602154259.4"><vh>enable_category</vh></v>
<v t="bwmulder.20040602161525"><vh>disable_category</vh></v>
<v t="bwmulder.20040601212737.23"><vh>disable</vh></v>
<v t="bwmulder.20040603081718"><vh>remove_overrides_in_list_and_dict_monitor</vh></v>
</v>
</v>
<v t="bwmulder.20040601222230"><vh>class basic_undomechanism</vh>
<v t="bwmulder.20040601222230.1"><vh>__init__</vh></v>
<v t="bwmulder.20040602171606"><vh>reset</vh></v>
<v t="bwmulder.20040601222230.2"><vh>scalars</vh>
<v t="bwmulder.20040601222230.3"><vh>scalar_set</vh></v>
<v t="bwmulder.20040601222230.4"><vh>scalar_set_undo</vh></v>
<v t="bwmulder.20040601222230.5"><vh>scalar_set_redo</vh></v>
<v t="bwmulder.20040601222230.6"><vh>scalar_modify</vh></v>
<v t="bwmulder.20040601222431"><vh>scalar_modify_undo</vh></v>
</v>
<v t="bwmulder.20040602075341"><vh>lists</vh>
<v t="bwmulder.20040602084701.1"><vh>creation</vh>
<v t="bwmulder.20040602175523"><vh>list_assignment_replace</vh></v>
<v t="bwmulder.20040602175523.1"><vh>list_assignment_replace_undo</vh></v>
<v t="bwmulder.20040602175740"><vh>list_assignment_replace_redo</vh></v>
<v t="bwmulder.20040602183806"><vh>list_assignment_new</vh></v>
<v t="bwmulder.20040602183814"><vh>list_assignment_new_undo</vh></v>
<v t="bwmulder.20040602183911"><vh>list_assignment_new_redo</vh></v>
<v t="bwmulder.20040602075341.1"><vh>list_create</vh></v>
<v t="bwmulder.20040602084701.2"><vh>list_create_undo</vh></v>
<v t="bwmulder.20040602084701.3"><vh>list_create_redo</vh></v>
</v>
<v t="bwmulder.20040602084701.4"><vh>setting</vh>
<v t="bwmulder.20040602085955"><vh>list_set</vh></v>
<v t="bwmulder.20040602085955.1"><vh>list_set_undo</vh></v>
</v>
<v t="bwmulder.20040602085955.2"><vh>deletion</vh>
<v t="bwmulder.20040602085955.3"><vh>list_del</vh></v>
<v t="bwmulder.20040602085955.4"><vh>list_del_undo</vh></v>
<v t="bwmulder.20040602085955.5"><vh>list_del_redo</vh></v>
</v>
<v t="bwmulder.20040602151709"><vh>append</vh>
<v t="bwmulder.20040602152051"><vh>list_append</vh></v>
<v t="bwmulder.20040602152051.1"><vh>list_append_undo</vh></v>
<v t="bwmulder.20040602152051.2"><vh>list_append_redo</vh></v>
</v>
<v t="bwmulder.20040602152548.1"><vh>pop</vh>
<v t="bwmulder.20040602152548.2"><vh>list_pop</vh></v>
</v>
</v>
<v t="bwmulder.20040602171032"><vh>dictionaries</vh>
<v t="bwmulder.20040602171032.1"><vh>creation</vh>
<v t="bwmulder.20040602175801"><vh>dictionary creation</vh></v>
<v t="bwmulder.20040602171032.2"><vh>dict_create</vh></v>
<v t="bwmulder.20040602171032.3"><vh>dict_create_undo</vh></v>
<v t="bwmulder.20040602171032.4"><vh>dict_create_redo</vh></v>
</v>
<v t="bwmulder.20040602171032.5"><vh>setting</vh>
<v t="bwmulder.20040602171032.6"><vh>dict_set</vh></v>
<v t="bwmulder.20040602171032.7"><vh>dict_set_undo</vh></v>
</v>
<v t="bwmulder.20040602171032.8"><vh>deletion</vh>
<v t="bwmulder.20040602171032.9"><vh>dict_del</vh></v>
<v t="bwmulder.20040602171032.10"><vh>dict_del_undo</vh></v>
<v t="bwmulder.20040602171032.11"><vh>dict_del_redo</vh></v>
</v>
</v>
<v t="bwmulder.20040601224447"><vh>the undo machinery</vh>
<v t="bwmulder.20040603211921"><vh>queries</vh>
<v t="bwmulder.20040601224447.5"><vh>canUndo</vh></v>
<v t="bwmulder.20040601224447.6"><vh>canRedo</vh></v>
<v t="bwmulder.20040603212552"><vh>commands</vh></v>
<v t="bwmulder.20040603212612"><vh>commands_to_undo</vh></v>
<v t="bwmulder.20040603212713"><vh>commands_to_redo</vh></v>
<v t="bwmulder.20040604165011"><vh>steps_stored</vh></v>
<v t="bwmulder.20040605220919"><vh>print_commands</vh></v>
</v>
<v t="bwmulder.20040601224447.2"><vh>mark</vh></v>
<v t="bwmulder.20040601224447.3"><vh>undo</vh></v>
<v t="bwmulder.20040601224447.4"><vh>redo</vh></v>
<v t="bwmulder.20040603212934"><vh>rollback</vh></v>
<v t="bwmulder.20040601222649"><vh>run_commands</vh></v>
</v>
</v>
</v>
<v t="bwmulder.20040602221559"><vh>basic_undo_test.py</vh>
<v t="bwmulder.20040602223236"><vh>&lt;&lt; imports &gt;&gt;</vh></v>
<v t="bwmulder.20040602223236.1"><vh>class tracer</vh>
<v t="bwmulder.20040602223236.2"><vh>__getattr__</vh></v>
<v t="bwmulder.20040602223906"><vh>catchall</vh></v>
</v>
<v t="bwmulder.20040602224231"><vh>class delegator</vh>
<v t="bwmulder.20040602224413"><vh>__init__</vh></v>
<v t="bwmulder.20040602224332"><vh>__getattr__</vh></v>
<v t="bwmulder.20040602231914"><vh>catchall</vh></v>
<v t="bwmulder.20040602231934"><vh>enable_category</vh></v>
</v>
<v t="bwmulder.20040602225640"><vh>class basic_scalar_test</vh>
<v t="bwmulder.20040602230124"><vh>test_scalar_basic</vh></v>
<v t="bwmulder.20040604184443"><vh>test_linked_list</vh></v>
</v>
<v t="bwmulder.20040605104941"><vh>class basic_list_test</vh>
<v t="bwmulder.20040605105746"><vh>test_lists_basic</vh></v>
<v t="bwmulder.20040605174728"><vh>test_lists_replace</vh></v>
</v>
<v t="bwmulder.20040605180204"><vh>class basic_dict_test</vh>
<v t="bwmulder.20040605180225"><vh>test_dicts_basic</vh></v>
<v t="bwmulder.20040605180245"><vh>test_dicts_replace</vh></v>
</v>
<v t="bwmulder.20040602230426"><vh>test_main</vh></v>
</v>
</v>
<v t="ekr.20040918165144.9"><vh>Write script to find args to g.es()</vh></v>
<v t="ekr.20040918165427.4"><vh>Autocompletion dictionary files</vh></v>
<v t="ekr.20040918165427.5"><vh>Leo to docbook xml plugin: Leo2AsciiDoc</vh></v>
</v>
<v t="edream.110203113231.233"><vh>wxPython plugin (pre-alpha quality)</vh>
<v t="edream.110203113231.234"><vh> wx Diary</vh>
<v t="edream.111503110300"><vh>11/15/03  Leo becomes usuable (!)</vh></v>
<v t="edream.111403093253"><vh>11/13 &amp; 11/14</vh></v>
<v t="edream.110203113231.235"><vh>10/26 Code works with reorganized core</vh></v>
<v t="edream.110203113231.236"><vh>10/13/03: Added icons (Windows only)</vh></v>
<v t="edream.110203113231.237"><vh>10/12/03: Houston, we have ignition</vh></v>
<v t="edream.110203113231.238"><vh>10/11/03: converted code using c2py, then hand converted code</vh></v>
</v>
<v t="edream.111503111350"><vh>To do</vh>
<v t="edream.111303184347"><vh>(delete_range) doesn't work</vh>
<v t="edream.111303103141.3"><vh>delete_range</vh></v>
</v>
<v t="edream.111303100039"><vh>Gui-dependent commands (to do)</vh>
<v t="edream.111303100039.1"><vh>Edit Menu...</vh>
<v t="edream.111303101257"><vh>abortEditLabelCommand</vh></v>
<v t="edream.111303101257.1"><vh>endEditLabelCommand</vh></v>
<v t="edream.111303100039.6"><vh>insertHeadlineTime</vh></v>
</v>
<v t="edream.111303100039.7"><vh>Window Menu</vh>
<v t="edream.111303100039.8"><vh>cascade</vh></v>
<v t="edream.111303100039.9"><vh>equalSizedPanes</vh></v>
<v t="edream.111303100039.10"><vh>hideLogWindow</vh></v>
<v t="edream.111303100039.11"><vh>minimizeAll</vh></v>
<v t="edream.111303101709"><vh>toggleActivePane</vh></v>
<v t="edream.111303100039.12"><vh>toggleSplitDirection</vh></v>
</v>
<v t="edream.111703103908"><vh>Help Menu...</vh>
<v t="edream.111703103908.2"><vh>leoHelp</vh>
<v t="edream.111703103908.3"><vh>showProgressBar</vh>
<v t="edream.111703103908.4"><vh>&lt;&lt; create the scale widget &gt;&gt;</vh></v>
</v>
</v>
</v>
</v>
</v>
<v t="ekr.20050718142601"><vh>(Changes made 7/05)</vh>
<v t="ekr.20050718142601.1"><vh>Notes</vh></v>
<v t="edream.110203113231.347"><vh>OnInit  (wxLeoApp)</vh></v>
<v t="ekr.20050718151826"><vh>(wxGui Stuff)</vh>
<v t="edream.111303091300"><vh>app.gui.wx birth &amp; death</vh>
<v t="edream.110203113231.307"><vh> wxGui.__init__</vh></v>
<v t="edream.110203113231.308"><vh>createRootWindow &amp; allies</vh>
<v t="edream.110203113231.309"><vh>setDefaultIcon CONTAINS TK CODE</vh></v>
<v t="edream.110203113231.310"><vh>setEncoding</vh></v>
<v t="edream.110203113231.311"><vh>getDefaultConfigFont CONTAINS TK CODE</vh></v>
<v t="edream.110203113231.312"><vh>createGlobalWindows</vh></v>
</v>
<v t="edream.111303085447.1"><vh>destroySelf</vh></v>
<v t="edream.110203113231.317"><vh>runMainLoop</vh></v>
<v t="edream.110203113231.306"><vh>stubs</vh>
<v t="edream.110203113231.314"><vh>finishCreate</vh></v>
<v t="edream.110203113231.315"><vh>killGui</vh></v>
<v t="edream.110203113231.316"><vh>recreateRootWindow</vh></v>
</v>
</v>
<v t="edream.111303092328.4"><vh>createLeoFrame (wxGui panels)</vh></v>
</v>
<v t="edream.110203113231.350"><vh>Birth &amp; death (wxLeoFrame)</vh>
<v t="edream.110203113231.266"><vh>__init__</vh></v>
<v t="edream.110203113231.351"><vh>__repr__</vh></v>
<v t="edream.110203113231.260"><vh>finishCreate (wxLeoFrame)</vh>
<v t="edream.110203113231.261"><vh>&lt;&lt; create the splitters &gt;&gt;</vh></v>
<v t="edream.110203113231.265"><vh>&lt;&lt; set the window icon &gt;&gt;</vh></v>
<v t="edream.110203113231.264"><vh>&lt;&lt; declare event handlers for frame &gt;&gt;</vh></v>
</v>
<v t="edream.111403141810"><vh>initialRatios</vh></v>
<v t="edream.111503105816"><vh>injectCallbacks</vh></v>
<v t="edream.111303141147"><vh>signOnWithVersion</vh></v>
<v t="edream.111503213533"><vh>destroySelf</vh></v>
</v>
<v t="edream.110203113231.540"><vh>Birth &amp; death (wxLeoBody)</vh>
<v t="edream.110203113231.541"><vh>wxLeoBody.__init__</vh></v>
<v t="edream.110203113231.542"><vh>wxLeoBody.createControl</vh></v>
</v>
</v>
<v t="edream.111403093253.1"><vh>Projects</vh>
<v t="edream.111303205442"><vh>(colorizing) (demo only)</vh>
<v t="edream.111303204025"><vh>Indices</vh>
<v t="edream.111303204025.1"><vh>adjustIndex</vh></v>
<v t="edream.111303204025.2"><vh>compareIndices</vh></v>
<v t="edream.111303204025.3"><vh>convertRowColumnToIndex</vh></v>
<v t="edream.111303204025.4"><vh>convertIndexToRowColumn</vh></v>
<v t="edream.111303204025.5"><vh>getImageIndex</vh></v>
<v t="edream.111403080609"><vh>maxWxIndex (internal use)</vh></v>
</v>
<v t="edream.111303204517"><vh>Color tags (hacks for styles)</vh>
<v t="edream.111403082513"><vh>tkColorToWxColor (internal use)</vh></v>
<v t="edream.111303205611"><vh>tag_add</vh></v>
<v t="edream.111303205611.1"><vh>tag_bind</vh></v>
<v t="edream.111303205611.2"><vh>tag_configure (hack for wxStyles)</vh></v>
<v t="edream.111303205611.3"><vh>tag_delete</vh></v>
<v t="edream.111303205611.4"><vh>tag_remove</vh></v>
</v>
</v>
</v>
<v t="edream.110203113231.242"><vh>Unused code</vh>
<v t="ekr.20050718142601.3"><vh>From wxLeoApp.OnInit</vh></v>
<v t="edream.110203113231.257"><vh>updateJoinedHeadlines</vh></v>
<v t="edream.111303202917.1"><vh>Syntax coloring REMOVED: now in base body class</vh></v>
</v>
<v t="edream.110203113231.302"><vh>@thin __wx_gui.py</vh></v>
</v>
<v t="ekr.20051109021852"><vh>Tk Notebook</vh>
<v t="leo4u.20040924131405.1"><vh>@thin Tknotebook.py</vh></v>
<v t="leo4u.20040924130601.1"><vh>@thin TabWindow.py</vh></v>
</v>
</v>
<v t="EKR.20040517075715"><vh>External editors &amp; Open With</vh>
<v t="EKR.20040517075715.1"><vh>@thin mod_tempfname.py</vh></v>
<v t="EKR.20040517080049.4"><vh>@thin open_shell.py</vh></v>
<v t="EKR.20040517075715.4"><vh>@thin open_with.py</vh></v>
<v t="EKR.20040517075715.10"><vh>@thin vim.py</vh></v>
<v t="EKR.20040517075715.12"><vh>@thin xemacs.py</vh></v>
<v t="EKR.20040517075715.13"><vh>Word export</vh>
<v t="EKR.20040517075715.14"><vh>@thin word_export.py</vh></v>
<v t="EKR.20040517075715.20" tnodeList="EKR.20040517075715.20"><vh>@file-nosent word_export.ini</vh></v>
</v>
</v>
<v t="EKR.20040517080049"><vh>Files</vh>
<v t="EKR.20040517080049.1"><vh>@thin empty_leo_file.py</vh></v>
<v t="ekr.20040419105219"><vh>@thin lineNumbers.py</vh></v>
<v t="mork.20041018204908.1"><vh>@thin multifile.py</vh></v>
<v t="ekr.20040331151007"><vh>@thin niceNosent.py</vh></v>
</v>
<v t="ekr.20050402080206"><vh>LeoN</vh>
<v t="ekr.20050402080206.1"><vh>Readme file.</vh></v>
<v t="ekr.20050402080206.2"><vh>Overview</vh>
<v t="ekr.20050402080206.3"><vh>&lt;&lt; Step four, Realtime interaction &gt;&gt;</vh>
<v t="ekr.20050402080206.4"><vh>Design notes</vh>
<v t="ekr.20050402080206.5"><vh>LeoN devellopment status III</vh></v>
<v t="ekr.20050402080206.6"><vh>LeoN devellopment status IV</vh></v>
</v>
<v t="ekr.20050402080206.7"><vh>Notes</vh></v>
</v>
</v>
<v t="ekr.20050402080206.8"><vh>@thin LeoN.py</vh></v>
</v>
<v t="EKR.20040517080555"><vh>Menus &amp; translations</vh>
<v t="ekr.20041019072632"><vh>Chinese:  Must use @file due to problems with cvs</vh>
<v t="ekr.20040828105233" tnodeList="ekr.20040828105233,ekr.20040828105233.1,ekr.20040828105233.2,ekr.20040828105233.3,ekr.20040828105233.4,ekr.20040828105233.5,ekr.20040828105233.6,ekr.20040828105233.7"><vh>@file chinese_menu.py</vh>
<v t="ekr.20040828105233.1"><vh>onMenu</vh>
<v t="ekr.20040828105233.2"><vh>file menu</vh></v>
<v t="ekr.20040828105233.3"><vh>edit menu</vh></v>
<v t="ekr.20040828105233.4"><vh>outline menu</vh></v>
<v t="ekr.20040828105233.5"><vh>plugins menu</vh></v>
<v t="ekr.20040828105233.6"><vh>window menu</vh></v>
<v t="ekr.20040828105233.7"><vh>help menu</vh></v>
</v>
</v>
</v>
<v t="EKR.20040517080202.3"><vh>@thin french_fm.py</vh></v>
<v t="EKR.20040517080555.36"><vh>@thin scripts_menu.py</vh></v>
<v t="ekr.20040828122150"><vh>@thin pie_menus.py</vh></v>
</v>
<v t="ekr.20041009112303"><vh>Plugins manager, updater &amp; menu</vh>
<v t="EKR.20040517080555.1"><vh> Plugins menu</vh>
<v t="EKR.20040517080555.2"><vh>@thin plugins_menu.py</vh></v>
<v t="EKR.20040517080555.25"><vh>@thin pluginsTest.py</vh></v>
<v t="EKR.20040517080555.32"><vh>Notes re plugins menu</vh>
<v t="EKR.20040517080555.33"><vh> Changes made by E.K.Ream</vh></v>
<v t="EKR.20040517080555.34"><vh> Design</vh></v>
<v t="EKR.20040517080555.35"><vh> Initial suggestion from Paul Paterson</vh></v>
</v>
</v>
<v t="pap.20041006184225"><vh>@thin plugin_manager.py</vh></v>
<v t="pap.20050605183206"><vh>@thin leoupdate.py</vh></v>
</v>
<v t="ekr.20041001210557"><vh>Scripting</vh>
<v t="EKR.20040613213623"><vh>@thin mod_scripting.py</vh></v>
</v>
<v t="ekr.20050111122605"><vh>Servers</vh>
<v t="EKR.20040517080250.1"><vh>@thin mod_http.py</vh></v>
</v>
<v t="edream.110203113231.930"><vh>Spell Checking</vh>
<v t="ekr.20040809151600.52"><vh>Notes for creating aspell.pyd</vh>
<v t="ekr.20040809160744"><vh>Notes: e</vh></v>
<v t="ekr.20040809161108"><vh>Notes: Gary Bishop</vh></v>
<v t="ekr.20040809151600.53"><vh>@ file aspell.pyx</vh>
<v t="ekr.20040809160744.1"><vh>spell_checker.__init__</vh></v>
<v t="ekr.20040809160744.2"><vh>check</vh></v>
<v t="ekr.20040809160744.3"><vh>suggest</vh></v>
<v t="ekr.20040809160744.4"><vh>store_replacement</vh></v>
<v t="ekr.20040809160744.5"><vh>add_to_session</vh></v>
<v t="ekr.20040809160744.6"><vh>add_to_personal</vh></v>
</v>
<v t="ekr.20040809151600.54"><vh>@ file setup.py</vh></v>
</v>
</v>
<v t="ekr.20050306081349"><vh>Text formatting</vh>
<v t="mork.20041010095009"><vh>@thin xsltWithNodes.py</vh></v>
<v t="ekr.20040331071919"><vh>Leo to AsciiDoc</vh>
<v t="ekr.20050128070307"><vh>@url http://www.marshallresearch.com/michael-dawson/os/leo.html</vh></v>
<v t="ekr.20040331071919.38"><vh>Leo 2 AsciiDoc Users Guide</vh>
<v t="ekr.20040331071919.2"><vh>About this document</vh>
<v t="ekr.20040331071919.3"><vh>License</vh>
<v t="ekr.20040331071919.4"><vh>License document</vh></v>
</v>
</v>
<v t="ekr.20040331071919.39"><vh>Installation</vh></v>
<v t="ekr.20040331071919.40"><vh>Operation</vh>
<v t="ekr.20040331071919.41"><vh>Directives</vh>
<v t="ekr.20040331071919.42"><vh>Configuration</vh></v>
</v>
<v t="ekr.20040331071919.43"><vh>Markup</vh>
<v t="ekr.20040331071919.44"><vh>Standard AsciiDoc Markup</vh>
<v t="ekr.20040331071919.45"><vh>Headings</vh></v>
<v t="ekr.20040331071919.46"><vh>Lists</vh></v>
<v t="ekr.20040331071919.47"><vh>URLs</vh></v>
</v>
</v>
</v>
</v>
<v t="ekr.20040331071919.1"><vh>Leo 2 AsciiDoc Developers Guide</vh>
<v t="ekr.20040331071919.2"><vh>About this document</vh>
<v t="ekr.20040331071919.3"><vh>License</vh>
<v t="ekr.20040331071919.4"><vh>License document</vh></v>
</v>
</v>
<v t="ekr.20040331071919.5"><vh>Version, Requirements</vh></v>
<v t="ekr.20040331071919.6"><vh>The General Approach</vh>
<v t="ekr.20040331071919.7"><vh>Markup Added</vh></v>
</v>
<v t="ekr.20040331071919.8"><vh>&lt;&lt; root of mod_leo2ascd.py &gt;&gt;</vh>
<v t="ekr.20040331071919.9"><vh>&lt;&lt; Key Functions &gt;&gt;</vh></v>
<v t="ekr.20040331071919.10"><vh>&lt;&lt; Declarations and Utilities &gt;&gt;</vh>
<v t="ekr.20040331071919.11"><vh>&lt;&lt; The Code -- Declarations and Utilities &gt;&gt;</vh></v>
</v>
<v t="ekr.20040331071919.12"><vh>&lt;&lt; Write the outline tree as AsciiDoc file &gt;&gt;</vh>
<v t="ekr.20040331071919.13"><vh>&lt;&lt; Write a node &gt;&gt;</vh></v>
</v>
</v>
<v t="ekr.20040331071919.14"><vh>Other programs</vh></v>
<v t="ekr.20040331071919.15"><vh>&lt;&lt;Appendix: AsciiDoc &gt;&gt;</vh>
<v t="ekr.20040331071919.16"><vh>&lt;&lt; Configuration file &gt;&gt;</vh></v>
<v t="ekr.20040331071919.17"><vh>&lt;&lt; Patches &gt;&gt;</vh></v>
</v>
<v t="ekr.20040331071919.18"><vh>&lt;&lt;Appendix: DocBook&gt;&gt;</vh>
<v t="ekr.20040331071919.19"><vh>&lt;&lt; Tool Chain &gt;&gt;</vh></v>
<v t="ekr.20040331071919.20"><vh>&lt;&lt; Make File &gt;&gt;</vh></v>
<v t="ekr.20040331071919.21"><vh>&lt;&lt; Style Sheets &gt;&gt;</vh>
<v t="ekr.20040331071919.22"><vh>&lt;&lt; General &gt;&gt;</vh></v>
<v t="ekr.20040331071919.23"><vh>&lt;&lt; Customize &gt;&gt;</vh></v>
<v t="ekr.20040331071919.24"><vh>&lt;&lt; HTML: One File &gt;&gt;</vh></v>
<v t="ekr.20040331071919.25"><vh>&lt;&lt; HTML: Individual Pages &gt;&gt;</vh></v>
<v t="ekr.20040331071919.26"><vh>&lt;&lt; HTML: base css style sheet &gt;&gt;</vh></v>
<v t="ekr.20040331071919.27"><vh>&lt;&lt; HTML: css style sheet &gt;&gt;</vh></v>
<v t="ekr.20040331071919.28"><vh>&lt;&lt; HTML: common &gt;&gt;</vh></v>
<v t="ekr.20040331071919.29"><vh>&lt;&lt; PDF &gt;&gt;</vh></v>
</v>
</v>
<v t="ekr.20040331071919.30"><vh>&lt;&lt;Appendix: XEmacs Text Editor&gt;&gt;</vh>
<v t="ekr.20040331071919.31"><vh>&lt;&lt; Open_With Plugin &gt;&gt;</vh></v>
<v t="ekr.20040331071919.32"><vh>&lt;&lt; Open_Tree Plugin &gt;&gt;</vh></v>
<v t="ekr.20040331071919.33"><vh>&lt;&lt; Filename modification &gt;&gt;</vh></v>
<v t="ekr.20040331071919.34"><vh>&lt;&lt; Kill Temporary Buffers &gt;&gt;</vh></v>
<v t="ekr.20040331071919.35"><vh>&lt;&lt; MMM-mode &gt;&gt;</vh></v>
<v t="ekr.20040331071919.36"><vh>&lt;&lt; Insert indexterm &gt;&gt;</vh></v>
<v t="ekr.20040331071919.37"><vh>&lt;&lt; Indent Leo comments &gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="ekr.20050817132814"><vh>rst3</vh>
<v t="ekr.20050817120850.1" tnodeList="ekr.20050817120850.1,ekr.20050817122915,ekr.20050822123348,ekr.20050817124859,ekr.20050817165745,ekr.20050822172321,ekr.20050817124859.1,ekr.20050817165745.1,ekr.20050818033610,ekr.20050818095347,ekr.20050819055746.1,ekr.20050820112549,ekr.20050822065754,ekr.20050822125824,ekr.20050822172321.1,ekr.20050825101903,ekr.20050818103031,ekr.20050817115636.2,ekr.20050825101321,ekr.20050818103441,ekr.20050817115636.4,ekr.20050817115636.5,ekr.20050817115636.6,ekr.20050820092312,ekr.20050817115636.8,ekr.20050817115636.9,ekr.20050817115636.7,ekr.20050820100547,ekr.20050820101355,ekr.20050820103029,ekr.20050820101522,ekr.20050820101355.1,ekr.20050820094818,ekr.20050820092312.1,ekr.20050817120850.10,ekr.20050817120850.11,ekr.20050818094118.2,ekr.20050818090152,ekr.20050818090152.1,ekr.20050817120850.98,ekr.20050817120850.99,ekr.20050817120850.94,ekr.20050817120850.95,ekr.20050817120850.96,ekr.20050817120850.108,ekr.20050817142135.1,ekr.20050817120850.143,ekr.20050817120850.144,ekr.20050817120850.141,ekr.20050817135706.1,ekr.20050817120850.157,ekr.20050817120850.158,ekr.20050818105023,ekr.20050817120850.15,ekr.20050817120850.12,ekr.20050817120850.14,ekr.20050818081715,ekr.20050819072001,ekr.20050819072001.1,ekr.20050817120850.13,ekr.20050818083045,ekr.20050821153838,ekr.20050818022030,ekr.20050818084920,ekr.20050818130249,ekr.20050818090907,ekr.20050817120850.32,ekr.20050817120850.34,ekr.20050817120850.39,ekr.20050817120850.42,ekr.20050817120850.44,ekr.20050817120850.46,ekr.20050817120850.48,ekr.20050817120850.62,ekr.20050817120850.64,ekr.20050817120850.74,ekr.20050817120850.78,ekr.20050817120850.86,ekr.20050817120850.92,ekr.20050817120850.162,ekr.20050817120850.102,ekr.20050817120850.106,ekr.20050817120850.110,ekr.20050817120850.122,ekr.20050817120850.124,ekr.20050817120850.126,ekr.20050817120850.130,ekr.20050817120850.132,ekr.20050817120850.138,ekr.20050817120850.28,ekr.20050817120850.147,ekr.20050817120850.18,ekr.20050817120850.20,ekr.20050817120850.40,ekr.20050817120850.54,ekr.20050817120850.82,ekr.20050817120850.100,ekr.20050817120850.105,ekr.20050817120850.120,ekr.20050817120850.36,ekr.20050817120850.58,ekr.20050817120850.60,ekr.20050817120850.66,ekr.20050817120850.24,ekr.20050817120850.22,ekr.20050817120850.50,ekr.20050817120850.52,ekr.20050817120850.56,ekr.20050818094118.1,ekr.20050817120850.68,ekr.20050817120850.134,ekr.20050817120850.145,ekr.20050817120850.151,ekr.20050817120850.26,ekr.20050817120850.76,ekr.20050817120850.80,ekr.20050817120850.88,ekr.20050817120850.112,ekr.20050817120850.128,ekr.20050817142135,ekr.20050817120850.153,ekr.20050817120850.155,ekr.20050817120850.30,ekr.20050817135706,ekr.20050817120850.160,ekr.20050818094954,ekr.20050818105023.1,ekr.20050817120850.84,ekr.20050817120850.90,ekr.20050818094954.1,ekr.20050817120850.165,ekr.20050817120850.116,ekr.20050817120850.70,ekr.20050817120850.72,ekr.20050817120850.164,ekr.20050817120850.114,ekr.20050817120850.118,ekr.20050817120850.149,ekr.20050817120850.159,ekr.20050817120850.140"><vh>@file leo_pdf.py</vh>
<v t="ekr.20050817122915"><vh>&lt;&lt; docstring &gt;&gt;</vh></v>
<v t="ekr.20050817115636.2"><vh>&lt;&lt; imports &gt;&gt;</vh></v>
<v t="ekr.20050822123348"><vh>&lt;&lt; about this code &gt;&gt;</vh></v>
<v t="ekr.20050817124859"><vh>&lt;&lt; copyright &gt;&gt;</vh></v>
<v t="ekr.20050817165745"><vh>&lt;&lt; version history &gt;&gt;</vh>
<v t="ekr.20050822172321"><vh>Early versions</vh>
<v t="ekr.20050817124859.1"><vh>Initial conversion</vh></v>
<v t="ekr.20050817165745.1"><vh>0.0.1</vh></v>
<v t="ekr.20050818033610"><vh>0.0.2</vh></v>
<v t="ekr.20050818095347"><vh>0.0.3</vh></v>
<v t="ekr.20050819055746.1"><vh>0.0.4</vh></v>
<v t="ekr.20050820112549"><vh>0.0.5</vh></v>
</v>
<v t="ekr.20050822065754"><vh>0.1</vh></v>
<v t="ekr.20050822125824"><vh>0.2</vh></v>
<v t="ekr.20050822172321.1"><vh>0.3</vh></v>
<v t="ekr.20050825101903"><vh>0.4</vh></v>
</v>
<v t="ekr.20050818103031"><vh>&lt;&lt; to do &gt;&gt;</vh></v>
<v t="ekr.20050825101321"><vh>init</vh></v>
<v t="ekr.20050818103441"><vh>class Bunch (object)</vh></v>
<v t="ekr.20050817115636.4"><vh>class Writer (docutils.writers.Writer)</vh>
<v t="ekr.20050817115636.5"><vh>&lt;&lt; class Writer declarations &gt;&gt;</vh></v>
<v t="ekr.20050817115636.6"><vh>__init__ (Writer)</vh></v>
<v t="ekr.20050820092312"><vh>createParagraphsFromIntermediateFile</vh></v>
<v t="ekr.20050817115636.8"><vh>createPDF_usingPlatypus</vh></v>
<v t="ekr.20050817115636.9"><vh>lower</vh></v>
<v t="ekr.20050817115636.7"><vh>translate</vh></v>
</v>
<v t="ekr.20050820100547"><vh>class dummyPDFTranslator (docutils.nodes.NodeVisitor)</vh>
<v t="ekr.20050820101355"><vh>   __init__ (dummyPDFTranslator)</vh></v>
<v t="ekr.20050820103029"><vh>as_what</vh></v>
<v t="ekr.20050820101522"><vh>encode</vh></v>
<v t="ekr.20050820101355.1"><vh>visit/depart_document</vh></v>
<v t="ekr.20050820094818"><vh>buildFromIntermediateFile</vh></v>
<v t="ekr.20050820092312.1"><vh>putParaFromIntermediateFile</vh></v>
</v>
<v t="ekr.20050817120850.10"><vh>class PDFTranslator (docutils.nodes.NodeVisitor)</vh>
<v t="ekr.20050817120850.11"><vh>   __init__ (PDFTranslator)</vh></v>
<v t="ekr.20050818094118.2"><vh>Complex</vh>
<v t="ekr.20050818090152"><vh>footnotes</vh>
<v t="ekr.20050818090152.1"><vh>footnote_reference</vh>
<v t="ekr.20050817120850.98"><vh>visit_footnote_reference</vh></v>
<v t="ekr.20050817120850.99"><vh>depart_footnote_reference</vh></v>
</v>
<v t="ekr.20050817120850.94"><vh>footnote &amp; helpers</vh>
<v t="ekr.20050817120850.95"><vh>footnote_backrefs</vh></v>
<v t="ekr.20050817120850.96"><vh>footnote_backrefs_depart</vh></v>
</v>
<v t="ekr.20050817120850.108"><vh>label</vh></v>
</v>
<v t="ekr.20050817142135.1"><vh>reference...</vh>
<v t="ekr.20050817120850.143"><vh>visit_reference</vh></v>
<v t="ekr.20050817120850.144"><vh>depart_reference</vh></v>
</v>
<v t="ekr.20050817120850.141"><vh>target</vh></v>
<v t="ekr.20050817135706.1"><vh>title</vh>
<v t="ekr.20050817120850.157"><vh>visit_title</vh></v>
<v t="ekr.20050817120850.158"><vh>depart_title</vh></v>
</v>
</v>
<v t="ekr.20050818105023"><vh>Helpers</vh>
<v t="ekr.20050817120850.15"><vh> starttag</vh></v>
<v t="ekr.20050817120850.12"><vh>as_what</vh></v>
<v t="ekr.20050817120850.14"><vh>createParagraph</vh></v>
<v t="ekr.20050818081715"><vh>dumpContext</vh></v>
<v t="ekr.20050819072001"><vh>dumpNode</vh>
<v t="ekr.20050819072001.1"><vh>&lt;&lt; define keys to be printed &gt;&gt;</vh></v>
</v>
<v t="ekr.20050817120850.13"><vh>encode</vh></v>
<v t="ekr.20050818083045"><vh>inContext</vh></v>
<v t="ekr.20050821153838"><vh>pdfMunge</vh></v>
<v t="ekr.20050818022030"><vh>push, pop, peek</vh></v>
<v t="ekr.20050818084920"><vh>putHead &amp; putTail</vh></v>
</v>
<v t="ekr.20050818130249"><vh>Simple...</vh>
<v t="ekr.20050818090907"><vh> do nothings...</vh>
<v t="ekr.20050817120850.32"><vh>authors</vh></v>
<v t="ekr.20050817120850.34"><vh>block_quote</vh></v>
<v t="ekr.20050817120850.39"><vh>caption</vh></v>
<v t="ekr.20050817120850.42"><vh>citation</vh></v>
<v t="ekr.20050817120850.44"><vh>citation_reference</vh></v>
<v t="ekr.20050817120850.46"><vh>classifier</vh></v>
<v t="ekr.20050817120850.48"><vh>colspec</vh></v>
<v t="ekr.20050817120850.62"><vh>definition_list_item</vh></v>
<v t="ekr.20050817120850.64"><vh>description</vh></v>
<v t="ekr.20050817120850.74"><vh>document</vh></v>
<v t="ekr.20050817120850.78"><vh>entry</vh></v>
<v t="ekr.20050817120850.86"><vh>field_argument</vh></v>
<v t="ekr.20050817120850.92"><vh>field_body</vh></v>
<v t="ekr.20050817120850.162"><vh>generated</vh></v>
<v t="ekr.20050817120850.102"><vh>image</vh></v>
<v t="ekr.20050817120850.106"><vh>interpreted</vh></v>
<v t="ekr.20050817120850.110"><vh>legend</vh></v>
<v t="ekr.20050817120850.122"><vh>option</vh></v>
<v t="ekr.20050817120850.124"><vh>option_argument</vh></v>
<v t="ekr.20050817120850.126"><vh>option_group</vh></v>
<v t="ekr.20050817120850.130"><vh>option_list_item</vh></v>
<v t="ekr.20050817120850.132"><vh>option_string</vh></v>
<v t="ekr.20050817120850.138"><vh>problematic</vh></v>
<v t="ekr.20050817120850.28"><vh>system_message</vh></v>
<v t="ekr.20050817120850.147"><vh>visit_row</vh></v>
</v>
<v t="ekr.20050817120850.18"><vh>admonitions...</vh>
<v t="ekr.20050817120850.20"><vh>attention</vh></v>
<v t="ekr.20050817120850.40"><vh>caution</vh></v>
<v t="ekr.20050817120850.54"><vh>danger</vh></v>
<v t="ekr.20050817120850.82"><vh>error</vh></v>
<v t="ekr.20050817120850.100"><vh>hint</vh></v>
<v t="ekr.20050817120850.105"><vh>important</vh></v>
<v t="ekr.20050817120850.120"><vh>note</vh></v>
</v>
<v t="ekr.20050817120850.36"><vh>bullet_list</vh></v>
<v t="ekr.20050817120850.58"><vh>definition</vh></v>
<v t="ekr.20050817120850.60"><vh>definition_list</vh></v>
<v t="ekr.20050817120850.66"><vh>docinfos...</vh>
<v t="ekr.20050817120850.24"><vh>address</vh></v>
<v t="ekr.20050817120850.22"><vh>author</vh></v>
<v t="ekr.20050817120850.50"><vh>contact</vh></v>
<v t="ekr.20050817120850.52"><vh>copyright</vh></v>
<v t="ekr.20050817120850.56"><vh>date</vh></v>
<v t="ekr.20050818094118.1"><vh>docinfo</vh></v>
<v t="ekr.20050817120850.68"><vh>docinfo_item</vh></v>
<v t="ekr.20050817120850.134"><vh>organization</vh></v>
<v t="ekr.20050817120850.145"><vh>revision</vh></v>
<v t="ekr.20050817120850.151"><vh>status</vh></v>
<v t="ekr.20050817120850.26"><vh>version</vh></v>
</v>
<v t="ekr.20050817120850.76"><vh>emphasis</vh></v>
<v t="ekr.20050817120850.80"><vh>enumerated_list</vh></v>
<v t="ekr.20050817120850.88"><vh>field_list</vh></v>
<v t="ekr.20050817120850.112"><vh>list_item</vh></v>
<v t="ekr.20050817120850.128"><vh>option_list</vh></v>
<v t="ekr.20050817142135"><vh>paragraph...</vh></v>
<v t="ekr.20050817120850.153"><vh>strong</vh></v>
<v t="ekr.20050817120850.155"><vh>subtitle</vh></v>
<v t="ekr.20050817120850.30"><vh>term</vh></v>
<v t="ekr.20050817135706"><vh>Text...</vh></v>
<v t="ekr.20050817120850.160"><vh>topic</vh></v>
</v>
<v t="ekr.20050818094954"><vh>Unusual...</vh>
<v t="ekr.20050818105023.1"><vh> Does not set context</vh>
<v t="ekr.20050817120850.84"><vh>field</vh></v>
<v t="ekr.20050817120850.90"><vh>field_name</vh></v>
</v>
<v t="ekr.20050818094954.1"><vh> Raises SkipNode</vh>
<v t="ekr.20050817120850.165"><vh>comment</vh></v>
<v t="ekr.20050817120850.116"><vh> literal_blocks...</vh>
<v t="ekr.20050817120850.70"><vh>doctest_block</vh></v>
<v t="ekr.20050817120850.72"><vh>line_block</vh></v>
</v>
</v>
<v t="ekr.20050817120850.164"><vh>invisible_visit</vh></v>
<v t="ekr.20050817120850.114"><vh>literal (only changes context)</vh></v>
<v t="ekr.20050817120850.118"><vh>meta (appends to self.head)</vh></v>
<v t="ekr.20050817120850.149"><vh>section</vh></v>
<v t="ekr.20050817120850.159"><vh>unimplemented_visit</vh></v>
<v t="ekr.20050817120850.140"><vh>visit_raw</vh></v>
</v>
</v>
</v>
<v t="ekr.20050805162550"
marks="ekr.20050809082854.1,"><vh>@thin rst3.py</vh></v>
</v>
</v>
<v t="ekr.20050830091910"><vh>Zodb</vh>
<v t="ekr.20050825154553"><vh>@thin zodb.py</vh></v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="EKR.20040517075110">"""Script to find and replace all functions in leoGlobals.py."""
@color
@language python
@tabwidth -4

import leoPlugins
import string

@others

if 1:
    &lt;&lt; set nameList to the list of functions in leoGlobals.py &gt;&gt;
else:
    p = g.findNodeAnywhere("@file leoGlobals.py")
    nameList = findFunctionsInTree(p)

    nameList.sort() ; g.enl()
    for name in nameList: g.es("'%s'," % name)
    
    s = "%d functions in leoGlobals.py" % len(nameList)
    print s ; g.es(s)

if 1:
    g.enl() ; g.enl()
    count = prependNamesInTree(p,nameList,"g.",replace=True) # Just prints if replace==False.
    s = "%d --- done --- " % count
    print s ; g.es(s)
</t>
<t tx="EKR.20040517075110.1">nameList = (
'alert',
'angleBrackets',
'appendToList',
'callerName',
'CheckVersion',
'choose',
'clearAllIvars',
'clear_stats',
'collectGarbage',
'computeLeadingWhitespace',
'computeWidth',
'computeWindowTitle',
'createTopologyList',
'create_temp_name',
'disableIdleTimeHook',
'doHook',
'dump',
'ecnl',
'ecnls',
'enableIdleTimeHook',
'enl',
'ensure_extension',
'es',
'esDiffTime',
'es_error',
'es_event_exception',
'es_exception',
'escaped',
'executeScript',
'file_date',
'findNodeAnywhere',
'findNodeInTree',
'findTopLevelNode',
'findReference',
'find_line_start',
'find_on_line',
'flattenList',
'funcToMethod',
'getBaseDirectory',
'getOutputNewline',
'getTime',
'get_Sherlock_args',
'get_directives_dict',
'get_leading_ws',
'get_line',
'get_line_after',
'getpreferredencoding',
'idleTimeHookHandler',
'importFromPath',
'initScriptFind',
'init_sherlock',
'init_trace',
'isUnicode',
'isValidEncoding',
'is_c_id',
'is_nl',
'is_special',
'is_ws',
'is_ws_or_nl',
'joinLines',
'listToString',
'makeAllNonExistentDirectories',
'makeDict',
'match',
'match_c_word',
'match_ignoring_case',
'match_word',
'module_date',
'openWithFileName',
'optimizeLeadingWhitespace',
'os_path_abspath',
'os_path_basename',
'os_path_dirname',
'os_path_exists',
'os_path_getmtime',
'os_path_isabs',
'os_path_isdir',
'os_path_isfile',
'os_path_join',
'os_path_norm',
'os_path_normcase',
'os_path_normpath',
'os_path_split',
'os_path_splitext',
'pause',
'plugin_date',
'plugin_signon',
'printDiffTime',
'printGc',
'printGcRefs',
'printGlobals',
'printLeoModules',
'print_bindings',
'print_stats',
'readlineForceUnixNewline',
'redirectStderr',
'redirectStdout',
'removeLeadingWhitespace',
'removeTrailingWs',
'reportBadChars',
'restoreStderr',
'restoreStdout',
'sanitize_filename',
'scanAtEncodingDirective',
'scanAtFileOptions',
'scanAtLineendingDirective',
'scanAtPagewidthDirective',
'scanAtRootOptions',
'scanAtTabwidthDirective',
'scanDirectives',
'scanError',
'scanf',
'set_delims_from_language',
'set_delims_from_string',
'set_language',
'shortFileName',
'skip_blank_lines',
'skip_block_comment',
'skip_braces',
'skip_c_id',
'skip_heredoc_string',
'skip_leading_ws',
'skip_leading_ws_with_indent',
'skip_line',
'skip_long',
'skip_matching_delims',
'skip_nl',
'skip_non_ws',
'skip_parens',
'skip_pascal_begin_end',
'skip_pascal_block_comment',
'skip_pascal_braces',
'skip_pascal_string',
'skip_php_braces',
'skip_pp_directive',
'skip_pp_if',
'skip_pp_part',
'skip_python_string',
'skip_string',
'skip_to_char',
'skip_to_end_of_line',
'skip_to_semicolon',
'skip_typedef',
'skip_ws',
'skip_ws_and_nl',
'splitLines',
'stat',
'stdErrIsRedirected',
'stdOutIsRedirected',
'toEncodedString',
'toUnicode',
'toUnicodeFileEncoding',
'top',
'trace',
'trace_tag',
'update_file_if_changed',
'utils_rename',
'windows',
'wrap_lines')</t>
<t tx="EKR.20040517075110.2">def findFunctionsInTree(p):
    
    nameList = []
    for p in p.self_and_subtree_iter():
        names = findDefs(p.bodyString())
        if names:
            for name in names:
                if name not in nameList:
                    nameList.append(name)
    return nameList</t>
<t tx="EKR.20040517075110.3">def findDefs(body):
    
    lines = body.split('\n')
    names = []
    for s in lines:
        i = g.skip_ws(s,0)
        if g.match(s,i,"class"):
            return [] # The classes are defined in a single node.
        if g.match(s,i,"def"):
            i = g.skip_ws(s,i+3)
            j = g.skip_c_id(s,i)
            if j &gt; i:
                name = s[i:j]
                if g.match(name,0,"__init__"): 
                    return [] # Disallow other class methods.
                names.append(name)
    return names</t>
<t tx="EKR.20040517075110.4">def prependNamesInTree(p,nameList,prefix,replace=False):
    
    c = p.c
    
    assert(len(prefix) &gt; 0)
    ch1 = string.letters + '_'
    ch2 = string.letters + string.digits + '_'
    def_s = "def " ; def_n = len(def_s)
    prefix_n = len(prefix)
    total = 0
    c.beginUpdate()
    for p in p.self_and_subtree_iter():
        count = 0 ; s = p.bodyString()
        printFlag = False
        if s:
            for name in nameList:
                i = 0 ; n = len(name)
                while 1:
                    &lt;&lt; look for name followed by '(' &gt;&gt;
            if count and replace:
                if 0:
                    &lt;&lt; print before and after &gt;&gt;
                p.setBodyStringOrPane(s)
                p.setDirty()
        g.es("%3d %s" % (count,p.headString()))
        total += count
    c.endUpdate()
    return total</t>
<t tx="EKR.20040517075110.5">i = s.find(name,i)
if i == -1:
    break
elif g.match(s,i-1,'.'):
    i += n # Already an attribute.
elif g.match(s,i-prefix_n,prefix):
    i += n # Already preceded by the prefix.
elif g.match(s,i-def_n,def_s):
    i += n # preceded by "def"
elif i &gt; 0 and s[i-1] in ch1:
    i += n # Not a word match.
elif i+n &lt; len(s) and s[i+n] in ch2:
    i += n # Not a word match.
else:
    j = i + n
    j = g.skip_ws(s,j)
    if j &gt;= len(s) or s[j] != '(':
        i += n
    else: # Replace name by prefix+name
        s = s[:i] + prefix + name + s[i+n:]
        i += n ; count += 1
        # g.es('.',newline=False)
        if 1:
            if not printFlag:
                printFlag = True
                # print p.headString()
            print g.get_line(s,i-n)</t>
<t tx="EKR.20040517075110.6">print "-"*10,count,p.headString()
print "before..."
print p.bodyString()
print "-"*10,"after..."
print s</t>
<t tx="EKR.20040517075715"></t>
<t tx="EKR.20040517075715.13"></t>
<t tx="EKR.20040517075715.20">[Main]
use_styles = Yes
use_section_numbers = Yes
use_current_document = Yes
max_headings = 6
header_style = Heading

</t>
<t tx="EKR.20040517080049"></t>
<t tx="EKR.20040517080555"></t>
<t tx="EKR.20040517080555.1"></t>
<t tx="EKR.20040517080555.32">@nocolor</t>
<t tx="EKR.20040517080555.33">Reorganized the code so I can find various classes more easily.
Used @others to simply the outline.

Sorted all entries in dialogs.
Sorted all entries in Plugins menu, regardless of whether they are configurable.

For all dialogs:
    Added top ivar and removed root/master params and ivars.
    Added Leo icon and title.
    Centered dialogs.

Ctors now run all dialogs as modal dialogs: this could easily be undone.

Used a grid in the properties dialog to align widgets.</t>
<t tx="EKR.20040517080555.34">- We will use a new settings file called leoSettings.txt:
- Each setting will have its _own section_ in leoSettings.txt with the following items (most optional)
    val = present value of settings: Use parent setting if this does not exist.
    help = help string (displayed near setting if it exists)
    prompt = prompt string (defaults to setting name, i.e., the section name)
    group = name of group dialog containing this item (use general section if this does not exist)
    type = one of the following:
        value			meaning
        bool			followed by True/False prompts for radio buttons
        color			color picker
        font			font picker
        parent			name of parent config file (set/get setting in that file)
        entry			followed by arbitrary text in an entry widget
        text			followed by arbitrary text in a text widget
        number			any number, or followed by a range of valid values for an entry widget.
        numberlist  followed by a list valid values for a listbox.
        list			followed by a list of valid strings in a listbox.
Notes:
- We could use yaml or ConfigParser or Pickle.  yaml might be best.
- The options dialog will have a separate frame for each group or subgroup.
- We will want a Create Options file command (useful for converting old leoConfig.txt files)
- All options may have a use parent settings (for all widgets?)
- The separate "Groups" section may indicate which groups are subgroups of other groups for multi-level displays.</t>
<t tx="EKR.20040517080555.35">I wrote myself a plug-in which would automatically save the Leo file every so often and in doing so realized that it would be useful to be able to configure the interval between saves. Anyway, to cut a long story short, I generalized the idea and came up with the attached patch. 
 
All code resides under the "Plug in changes" node. The additions are all under the "create the plug-in menu" node with another couple of lines in "createMenuBar". Structurally this is ugly - but it helps keep all the changes in one place!
 
The basic idea is to allow plug-ins to be configured and also allow them to expose additional functions which can be accessed by a menu item. The advantage is that people don't have to mess with adding menus to Leo. Existing plug-ins don't need to be changed in any way to work with the new patch.
 
Ok, here's what it does	
 
1. A new "Plug-ins" menu item is added
 
2. Each plug-in gets an "About x	" entry.
 
    - clicking on "About x..." brings up an about box which shows name, version and documentation for the plug in
    - name comes from the module name
    - version is the module __version__ if present
    - documentation is the module docstring 
 
3. If the plug-in is configurable then a sub menu is created
 
    - configurable means that a corresponding ".ini" file is found with the same names as the plug-in (ie mod_image.py has mod_image.ini)
    - the sub menu contains
        - the "About x..." as before
        - a "Properties..." menu entry to edit the properties (*)
 
4. A further search is made for plug-in specific commands
 
    - we look for functions called "cmd_*" in the module
    - if found we add them to the plug-in menu
    - when you click on the menu item the function is called with a single parameter
 
(*) How does the property window work,
 
5. The property window reads the ini file which is assumed to be in standard ini file format (ie sections and parameters)
    - each section gets a frame in the window
    - each property gets an entry box
 
6. From the property window the user can "Cancel" or "OK", which saves changes
 
7. If the module contains an "applyConfiguration" function then there is also an "Apply" button on the form. The apply configuration function is called with the current configuration when the "Apply" button is pressed.
</t>
<t tx="EKR.20040517090508">@nocolor

Leo enables those plugins whose filenames appear anywhere in this file without comments.

Warning: make sure plugins appear at most once without comments. Otherwise,
disabling a plugin in the Plugins Manageger plugin will have no effect.

Leo loads plugins in the order they appear in this file.

File names may be indented as desired.

@color</t>
<t tx="EKR.20040611044600"></t>
<t tx="bwmulder.20040601212737">"""
Define a general purpose monitor module.

Can be used for classes derived from "object" to intercept assignment to instance attributes.

For lists and dictionaries, it also offers drop-in replacements which monitor all changes to those list and mappings.

This module also includes a basic undo / redo mechanism.

For this undo / redo mechanism, it is important that the undo / redo steps do not trigger any monitoring calls. 
This module should fullfill that requirement.

For scalars, we put "scalar_monitor" into the attribute slot to intercept accesses to the attribute. The values
themselves live in a differnt, "private" attribute. These private attributes are accessed directly for the
undo / redo steps.

For dictionaries and lists, we extend the base types. The undo / redo mechanism 
uses the methods of the basic type.

If you assign a list or a dictionary to a monitored attribute, the list or mapping is automatically converted to
a monitored list or mapping (but only one level deep).

[Question: do we need a convenience function which does this recursively?]
"""

@language python
@tabwidth -4

@others
</t>
<t tx="bwmulder.20040601212737.1">class passthrough(object):
    """
    Instances of this class are used to disable monitoring.
    The values are just passed through.
    """
    @others

</t>
<t tx="bwmulder.20040601212737.2">def __init__(self, private_attributename):
   self.private_attributename = private_attributename
</t>
<t tx="bwmulder.20040601212737.3">def __set__( self, instance, value):
   setattr(instance, self.private_attributename, value)
</t>
<t tx="bwmulder.20040601212737.4">def __get__(self, instance, owner):
   return getattr(instance, self.private_attributename)
</t>
<t tx="bwmulder.20040601212737.5">   
class scalar_monitor(object):
    """
   Monitor a scalar attribute.
   A scalar attribute is an attribute whose values do not have internal structure.
   Used for Integers and references.
    """
    @others
</t>
<t tx="bwmulder.20040601212737.6">def __init__(self, external_attributename, monitor_object):
    self.external_attributename = external_attributename
    self.private_attributename = '__' + external_attributename
    self.monitor_object = monitor_object
</t>
<t tx="bwmulder.20040601212737.7">def __set__( self, instance, value):
    private_attributename = self.private_attributename
    external_attributename = self.external_attributename
    try:
        oldvalue = getattr(instance, private_attributename)
    except AttributeError:
        self.monitor_object.scalar_set(instance, private_attributename, external_attributename)
    else:
        if oldvalue != value:
            self.monitor_object.scalar_modify(instance, private_attributename, external_attributename, oldvalue)
    setattr(instance, private_attributename, value)

</t>
<t tx="bwmulder.20040601212737.8">def __get__(self, instance, owner):
   return getattr(instance, self.private_attributename)

</t>
<t tx="bwmulder.20040601212737.9">class list_monitor(list):
    """
    Monitor changes to a list.
    
    Calls a "monitor_object" whenever changes are made to a list.
    
    You can use this class whenever you want to track changes to a list.
    """
    @others
</t>
<t tx="bwmulder.20040601212737.10">def set_monitor_object(self, monitor_object):
    """
    All changes to this list will trigger calls to monitor_object methods
    """
    self.monitor_object = monitor_object

</t>
<t tx="bwmulder.20040601212737.11">def __setitem__( self, key, value):
    """
    Intercept the l[key]=value operations.
    Also covers slice assignment.
    """
    try:
        oldvalue = self.__getitem__(key)
    except KeyError:
        self.monitor_object.list_create(self, key)
    else:
        self.monitor_object.list_set(self, key, oldvalue)
    list.__setitem__(self, key, value)
</t>
<t tx="bwmulder.20040601212737.12">def __delitem__( self, key):
   oldvalue = list.__getitem__(self, key)
   self.monitor_object.list_del(self, key, oldvalue)
   list.__delitem__(self, key)
</t>
<t tx="bwmulder.20040601212737.13">def append(self, value):
   self.monitor_object.list_append(self)
   list.append(self, value)


</t>
<t tx="bwmulder.20040601212737.14">class list_monitor_in_instance(object):
    """
    Monitor instance attributes which contain a list as a value.

    Assignments to this attributes, which must be lists, are replaced by instances of 'list_monitor'.
   """
    @others
</t>
<t tx="bwmulder.20040601212737.15">def __init__(self, external_attributename, monitor_object):
    self.external_attributename = external_attributename
    self.internal_attributename = '__' + external_attributename
    self.monitor_object = monitor_object
</t>
<t tx="bwmulder.20040601212737.16">def __set__(self, instance, value):
    """Intercept assignments to the external attribute"""
    assert isinstance(value, type([]))
    if isinstance(value, list_monitor):
        newvalue = value
        # if the value is already a list monitor, assume that this value
        # is already monitored. Do not create a new value.
    else:
        newvalue = list_monitor(value, self.monitor_object)
    internal_attributename = self.internal_attributename
    try:
        oldvalue = getattr(instance, internal_attributename)
    except AttributeError:
        self.monitor_object.list_assignment_new(instance, internal_attributename)
    else:
        self.monitor_object.list_assignment_replace(instance, internal_attributename, oldvalue)
    setattr(instance, self.internal_attributename, newvalue)

</t>
<t tx="bwmulder.20040601212737.17">def __get__(self, instance, owner):
   try:
      return instance.__dict__[self.internal_attributename]
   except KeyError: 
      return instance.__dict__[self.external_attributename]

</t>
<t tx="bwmulder.20040601212737.18">class monitor:
    """
   Monitor changes to (new style) classes.

   To use:
      1. 
            a) Call monitor_scalar(klass, external_attributename, internal_attributename)
                    for each scalar attribute you want to monitor.

                A scalar attribute is an attribute without internal structure (int and reference).

                The normal Python comparison operation (=) is used to check if a new value is stored
                in an instance attribute.
                
            b) Call monitor_list(klass, external_attributename, internal_attributename) for each
               list attribute you want to monitor.
                
           c) Call monitor_dict(klass, external_attributename, internal_attributename) for each
               dict attribute you want to monitor.
         
      2. 
            Call enable / disable to enable / disable monitoring.

   This is an abstract class.
   
   Concrete subclasses are the classes "tracer" and "basic_undomechanism". The latter does most
   (almost all) of the work of a (fairly) general undo mechanism.

   Limitations:
   
      Assumes that instance attributes are used consistently with certain types.
      
   """
    @others
</t>
<t tx="bwmulder.20040601212737.19">def __init__(self):
   self.monitored_scalar_attributes = []
   self.monitored_list_attributes = []
   self.monitored_dict_attributes = []
   self.removed_functions = []
   
   self.monitor_object = self
   # See enable_category.
   
   # Overwriting this one attribute allows
   # Clients of this module to implemente tracing of all
   # calls to this module.
   
</t>
<t tx="bwmulder.20040601212737.20">def monitor_scalar(self, klass, external_attributename):
   """
   Put in a hook so that we can monitor modications to instances of classref'
   with respect to the attribute "attributename".

   It is assumed that the attribute only contains scalar objects. A scalar
   object is an object which is unstructured, and not shared.
   """
   self.monitored_scalar_attributes.append(
      (klass, external_attributename))
</t>
<t tx="bwmulder.20040601212737.21">def monitor_list_attribute_in_class(self, klass, external_attributename):
   self.monitored_list_attributes.append(
      (klass, external_attributename))
</t>
<t tx="bwmulder.20040601212737.22">def enable(self):
    for l, klass in ((self.monitored_scalar_attributes, scalar_monitor),
             (self.monitored_list_attributes, list_monitor_in_instance),
             (self.monitored_dict_attributes, dict_monitor_in_instance)):
        self.enable_category(l, klass)
        
    self.enable_put_in_removed_functions()
    

</t>
<t tx="bwmulder.20040601212737.23">def disable(self):
    """
    Disable monitoring (temporarily).
    """
    for l, klass in ((self.monitored_scalar_attributes, scalar_monitor),
                     (self.monitored_list_attributes, list_monitor_in_instance),
                     (self.monitored_dict_attributes, dict_monitor_in_instance)):
        self.disable_category(l, klass)
    
    self.remove_overrides_in_list_and_dict_monitor()
    
</t>
<t tx="bwmulder.20040601212737.24">def scalar_set(self, instance, private_attributename, external_attributename):
   raise notImplementedError
</t>
<t tx="bwmulder.20040601212737.25">def scalar_modify(self, instance, private_attributename, external_attributename, oldvalue):
   raise notImplementedError
</t>
<t tx="bwmulder.20040601212737.26">def list_create(self, array, key, value):
   raise notImplementedError
</t>
<t tx="bwmulder.20040601212737.27">def list_set(self, array, key, value):
   raise notImplementedError
</t>
<t tx="bwmulder.20040601212737.28">def list_del(self, array, key, oldvalue):
   raise notImplementedError
</t>
<t tx="bwmulder.20040601212737.29">def list_append(self, array, value):
   raise notImplementedError
</t>
<t tx="bwmulder.20040601214251"></t>
<t tx="bwmulder.20040601215339"></t>
<t tx="bwmulder.20040601215339.1">@doc
Delayed activation of the monitor mechanism is probably useful.

Not clear of switching off and on is useful, though.</t>
<t tx="bwmulder.20040601222230">class basic_undomechanism(monitor):
    """
    This class provides the basic operations for undoable operations.
    
    Records a list of changes which it will undo or redo one by one.
    
    The granularity of the undo / redo operations is determined by calls to
    the 'mark' procedure. Only immediately after the 'mark' call can undo be called.
    Redo can only be called after calling undo.
    
    'rollback' is a special case of undo: it is not redoable. The envisioned usage of
    this facility is in error recovery: if a command does not go through, you can call
    this command to undo all your changes (and leave the application in a consistent state).
    
    Uses the monitor_scalar, monitor_list_attribute_in_class and monitor_dict_attribute_in_class
    methods to make assignment to instance variables undoable.
    
    Call 'enable' to activate the undo mechanism, 'disable' to temporarily
    stop the undo mechanism from collecting information about changes.
    
    The individual changes are bundled into "_commands'. The boundaries of
    these _commands are marked by a call to the procedure "mark".
    
    The procedure 'reset' can be called externally to erase all undo information.
    
    Individual lists and dictionaries can also be monitored for change with the
    list_monitor and dict_monitor classes.
    
    Possible optimizations later: special handling for string attributes.
    """
    @others</t>
<t tx="bwmulder.20040601222230.1">def __init__(self):

    monitor.__init__(self)
    self.reset()
    </t>
<t tx="bwmulder.20040601222230.2"></t>
<t tx="bwmulder.20040601222230.3">def scalar_set(self, instance, private_attributename, external_attributename):
   self._steps.append((self.scalar_set_undo, (instance, private_attributename)))
    

</t>
<t tx="bwmulder.20040601222230.4">def scalar_set_undo(self, instance, private_attributename):

    """Undo the changes done by the assignment of an instance"""
    newvalue = getattr(instance, private_attributename)
    delattr(instance, private_attributename)
    return self.scalar_set_redo, (instance, private_attributename, newvalue)
</t>
<t tx="bwmulder.20040601222230.5">def scalar_set_redo(self, instance, private_attributename, newvalue):

    setattr(instance, private_attributename, newvalue)
    return self.scalar_set_undo, (instance, private_attributename)
</t>
<t tx="bwmulder.20040601222230.6">def scalar_modify(self, instance, private_attributename, external_attributename, oldvalue):

  self._steps.append((self.scalar_modify_undo, (instance, private_attributename, oldvalue)))
</t>
<t tx="bwmulder.20040601222431">def scalar_modify_undo(self, instance, private_attributename, oldvalue):

    new_value = getattr(instance, private_attributename)
    setattr(instance, private_attributename, oldvalue)
    return self.scalar_modify_undo, (instance, private_attributename, new_value)</t>
<t tx="bwmulder.20040601222649">def run_commands(self, steps):
    
    """
    Run the undo / redo _steps.
    Returns the list of steps to redo / undo the steps just made.
    """

    steps.reverse()
    return [func(*args) for func, args in steps]
</t>
<t tx="bwmulder.20040601224447"></t>
<t tx="bwmulder.20040601224447.2">def mark(self):
    
    """Mark the end of the current commmand."""

    if self._steps:
        self._commands[self._index+1:] = [self._steps, None]
        self._index += 1
        self._steps = []</t>
<t tx="bwmulder.20040601224447.3">def undo(self):

    assert self.canUndo()
    self._commands[self._index] = self.run_commands(self._commands[self._index])
    self._index -= 1
    
</t>
<t tx="bwmulder.20040601224447.4">def redo(self):

    assert self.canRedo()
    self._commands[self._index+1] = self.run_commands(self._commands[self._index+1])
    self._index += 1</t>
<t tx="bwmulder.20040601224447.5">def canUndo(self):
    
    return self._commands[self._index] is not None and len(self._steps) == 0
</t>
<t tx="bwmulder.20040601224447.6">def canRedo(self):
    return self._commands[self._index+1] is not None and len(self._steps) == 0</t>
<t tx="bwmulder.20040602075341"></t>
<t tx="bwmulder.20040602075341.1">def list_create(self, array, key):
    self._steps.append((self.list_create_undo, (array, key)))

</t>
<t tx="bwmulder.20040602084701.1"></t>
<t tx="bwmulder.20040602084701.2">def list_create_undo(self, array, key):
    value = list.__getitem__(array, key)
    list.__delitem__(array, key)
    return self.list_create_redo, (array, key, value)

</t>
<t tx="bwmulder.20040602084701.3">def list_create_redo(self, array, key, value):
    list.__setitem__(array, key, value)
    return self.list_create_undo, (array, key)</t>
<t tx="bwmulder.20040602084701.4"></t>
<t tx="bwmulder.20040602085955">def list_set(self, array, key, oldvalue):
    self._steps.append((self.list_set_undo, (array, key, oldvalue)))

</t>
<t tx="bwmulder.20040602085955.1">def list_set_undo(self, array, key, value):
    oldvalue = list.__getitem__(array, key)
    list.__setitem__(array, key, value)
    return self.list_set_undo, (array, key, oldvalue)
</t>
<t tx="bwmulder.20040602085955.2"></t>
<t tx="bwmulder.20040602085955.3">def list_del(self, array, key, oldvalue):
   self._steps.append((self.list_del_undo, (array, key, oldvalue)))
   
</t>
<t tx="bwmulder.20040602085955.4">def list_del_undo(self, array, key, oldvalue):
    if type(key) == type(1):
        list.__setitem__(array, slice(key, key), [oldvalue])
    else:
        list.__setitem__(array, key, oldvalue)
    return self.list_del_redo, (array, key, oldvalue)
</t>
<t tx="bwmulder.20040602085955.5">def list_del_redo(self, array, key, oldvalue):
    oldvalue = list.__getitem__(array, key)
    list.__delitem__(array, key)
    return self.list_del_undo, (array, key, oldvalue)
</t>
<t tx="bwmulder.20040602151709"></t>
<t tx="bwmulder.20040602152051">def list_append(self, array):
    self._steps.append((self.list_append_undo, (array,)))
    


</t>
<t tx="bwmulder.20040602152051.1">def list_append_undo(self, array):
    oldvalue = list.pop(array)
    return self.list_append_redo, (array, oldvalue)
</t>
<t tx="bwmulder.20040602152051.2">def list_append_redo(self, array, oldvalue):
    list.append(array, oldvalue)
    return self.list_append_undo, (array,)</t>
<t tx="bwmulder.20040602152548">def pop(self):
    oldvalue = list.pop(self)
    self.monitor_object.list_pop(self, oldvalue)
</t>
<t tx="bwmulder.20040602152548.1"></t>
<t tx="bwmulder.20040602152548.2">def list_pop(self, array, oldvalue):
    self._steps.append((self.list_append_redo, (array, oldvalue)))
</t>
<t tx="bwmulder.20040602153618">class dict_monitor(dict):
    """
    Overwrite dictionaries so that we can monitor them.
    """
    @others
</t>
<t tx="bwmulder.20040602153642">def set_monitor_object(self, monitor_object):
    """
    All changes to this dictionary will trigger calls to monitor_object methods
    """
    self.monitor_object = monitor_object

</t>
<t tx="bwmulder.20040602153723">def __setitem__( self, key, value):
    """
    Intercept the l[key]=value operations.
    Also covers slice assignment.
    """
    try:
        oldvalue = self.__getitem__(key)
    except KeyError:
        self.monitor_object.dict_create(self, key, value)
    else:
        self.monitor_object.dict_set(self, key, oldvalue)
    dict.__setitem__(self, key, value)
</t>
<t tx="bwmulder.20040602153835">def __delitem__( self, key):
   oldvalue = dict.__getitem__(self, key)
   self.monitor_object.dict_del(self, key, oldvalue)
   dict.__delitem__(self, key)
</t>
<t tx="bwmulder.20040602154259">class dict_monitor_in_instance(object):
    """
    Monitor instance attributes which contain a list as a value.

    Assignments to this attributes, which must be lists, are replaced by instances of 'list_monitor'.
   """
    @others
</t>
<t tx="bwmulder.20040602154259.1">def __init__(self, external_attributename, monitor_object):
    self.external_attributename = external_attributename
    self.internal_attributename = '__' + external_attributename
    self.monitor_object = monitor_object
</t>
<t tx="bwmulder.20040602154259.2">def __set__(self, instance, value):
    """Intercept assignments to the external attribute"""
    assert isinstance(value, type({}))
    if isinstance(value, dict_monitor):
        newvalue = value
        # if the value is already a dict_monitor,
        # assume that the value is already monitored.
    else:
        newvalue = dict_monitor(value, self.monitor_object)
    internal_attributename = self.internal_attributename
    try:
        oldvalue = getattr(instance, internal_attributename)
    except AttributeError:
        self.monitor_object.list_assignment_new(instance, internal_attributename)
    else:
        self.monitor_object.list_assignment_replace(instance, internal_attributename, oldvalue)
    setattr(instance, self.internal_attributename, newvalue)
</t>
<t tx="bwmulder.20040602154259.3">def __get__(self, instance, owner):
   try:
      return instance.__dict__[self.internal_attributename]
   except KeyError: 
      return instance.__dict__[self.external_attributename]

</t>
<t tx="bwmulder.20040602154259.4">def enable_category(self, l, monitor_class):
   for klass, external_attributename in l:
      setattr(klass, external_attributename, monitor_class(
         external_attributename, self.monitor_object))
    </t>
<t tx="bwmulder.20040602161525">def disable_category(self, l, monitor_class):
   for klass, external_attributename in l:
      setattr(klass, external_attributename, passthrough (internal_attributename))
    
</t>
<t tx="bwmulder.20040602164627">def enable_put_in_removed_functions(self):
    """
    Reinstate the functions which were removed from list_monitor and dict_monitor.
    """
    for klass, attribute, function in self.removed_functions:
        setattr(klass, attribute, function)
</t>
<t tx="bwmulder.20040602165344"></t>
<t tx="bwmulder.20040602165402">def monitor_dict_attribute_in_class(self, klass, external_attributename):
   self.monitored_dict_attributes.append(
      (klass, external_attributename))
</t>
<t tx="bwmulder.20040602165506">def dict_create(self, array, key, value):
   raise notImplementedError
</t>
<t tx="bwmulder.20040602165513">def dict_set(self, array, key, value):
   raise notImplementedError
</t>
<t tx="bwmulder.20040602165553">def dict_del(self, array, key, oldvalue):
   raise notImplementedError
</t>
<t tx="bwmulder.20040602171032"></t>
<t tx="bwmulder.20040602171032.1"></t>
<t tx="bwmulder.20040602171032.2">def dict_create(self, dictionary, key, value):
    self._steps.append((self.dict_create_undo, (dictionary, key)))

</t>
<t tx="bwmulder.20040602171032.3">def dict_create_undo(self, dictionary, key):
    value = dict.__getitem__(dictionary, key)
    dict.__delitem__(dictionary, key)
    return self.dict_create_redo, (dictionary, key, value)

</t>
<t tx="bwmulder.20040602171032.4">def dict_create_redo(self, dictionary, key, value):
    dict.__setitem__(dictionary, key, value)
    return self.dict_create_undo, (dictionary, key,)
</t>
<t tx="bwmulder.20040602171032.5"></t>
<t tx="bwmulder.20040602171032.6">def dict_set(self, dictionary, key, oldvalue):
    self._steps.append((self.dict_set_undo, (dictionary, key, oldvalue)))

</t>
<t tx="bwmulder.20040602171032.7">def dict_set_undo(self, dictionary, key, value):
    oldvalue = dict.__getitem__(dictionary, key)
    dict.__setitem__(dictionary, key, value)
    return self.dict_set_undo, (dictionary, key, oldvalue)
</t>
<t tx="bwmulder.20040602171032.8"></t>
<t tx="bwmulder.20040602171032.9">def dict_del(self, dictionary, key, oldvalue):
   self._steps.append((self.dict_del_undo, (dictionary, key, oldvalue)))
   
</t>
<t tx="bwmulder.20040602171032.10">def dict_del_undo(self, dictionary, key, oldvalue ):
    dict.__setitem__(dictionary, key, oldvalue)
    return self.dict_del_redo, (dictionary, key, oldvalue)
</t>
<t tx="bwmulder.20040602171032.11">def dict_del_redo(self, dictionary, key, oldvalue ):
    oldvalue = dict.__getitem__(dictionary, key)
    dict.__delitem__(dictionary, key)
    return self.dict_del_undo, (dictionary, key, oldvalue)
</t>
<t tx="bwmulder.20040602171606">def reset(self):

    self._steps = []
    self._commands = [None, None]
    self._index = 0
    


</t>
<t tx="bwmulder.20040602175523">def list_assignment_replace(self, instance, attributename, oldvalue):
    self._steps.append((self.list_assignment_replace_undo, (instance, attributename, oldvalue)))</t>
<t tx="bwmulder.20040602175523.1">def list_assignment_replace_undo(self, instance, attributename, oldvalue):
    newvalue = getattr(instance, attributename)
    setattr(instance, attributename, oldvalue)
    return self.list_assignment_replace_redo, (instance, attributename, newvalue)</t>
<t tx="bwmulder.20040602175740">def list_assignment_replace_redo(self, instance, attributename, newvalue):
    oldvalue = getattr(instance, attributename)
    setattr(instance, attributename, newvalue)
    return self.list_assignment_replace_undo, (instance, attributename, oldvalue)
</t>
<t tx="bwmulder.20040602175801"># Dictionary monitors are are really handled like
# list monitors.
# For now, just use the same methods.
dict_assignment_new = list_assignment_new
dict_assignment_new_undo = list_assignment_new_undo
dict_assignment_new_redo = list_assignment_new_redo

dict_assignment_replace      = list_assignment_replace
dict_assignment_replace_undo = list_assignment_replace_undo
dict_assignment_replace_redo = list_assignment_replace_redo</t>
<t tx="bwmulder.20040602183806">def list_assignment_new(self, instance, attributename):
    self._steps.append((self.list_assignment_new_undo, (instance, attributename)))</t>
<t tx="bwmulder.20040602183814">def list_assignment_new_undo(self, instance, attributename):
    newvalue = getattr(instance, attributename)
    delattr(instance, attributename)
    return self.list_assignment_new_redo, (instance, attributename, newvalue)</t>
<t tx="bwmulder.20040602183911">def list_assignment_new_redo(self, instance, attributename, newvalue):
    setattr(instance, attributename, newvalue)
    return self.list_assignment_new_undo, (instance, attributename)
</t>
<t tx="bwmulder.20040602221559">&lt;&lt; imports &gt;&gt;

undo_tracing = False

@others

if __name__ == '__main__':
    test_main()</t>
<t tx="bwmulder.20040602223236">from basic_undo import monitor, basic_undomechanism, list_monitor, dict_monitor
import unittest
from test import test_support
</t>
<t tx="bwmulder.20040602223236.1">class tracer(monitor):
    
    # The output format could be improved, but this is only for testing.
    """Simple class which can be used to trace all calls made from a monitor."""

    @others

</t>
<t tx="bwmulder.20040602223236.2">def __getattr__(self, attributename):
    self.attributename = attributename
    return self.catchall</t>
<t tx="bwmulder.20040602223906">def catchall(self, *args, **kwrds):

    print "Tracer:", self.attributename, ":", args, kwds</t>
<t tx="bwmulder.20040602224231">class delegator(object):
    """
    Simple class to print all arguments passed to a monitor.
    Allows you to watch the undoer in action...
    """
    @others</t>
<t tx="bwmulder.20040602224332">def __getattr__(self, attributename):
    self.attributename = attributename
    return self.catchall</t>
<t tx="bwmulder.20040602224413">def __init__(self):
    
    self.undoer = basic_undomechanism()
    self.undoer.monitor_object = self
    

</t>
<t tx="bwmulder.20040602225640">class basic_scalar_test_class(object):
    """Simple class for the basic_scalar_test"""
    pass

class basic_scalar_test(unittest.TestCase):
    @others</t>
<t tx="bwmulder.20040602230124">def test_scalar_basic(self):
    """
    Some basic testing for the scalar undoer.
    """
    if undo_tracing:
        self.m = m = delegator()
    else:
        self.m = m = basic_undomechanism()
    m.monitor_scalar(basic_scalar_test_class, "x")
    m.enable()
    # command 1
    c = basic_scalar_test_class()
    c.x = "First value"
    m.mark()
    # command 2	
    c.x = "second value"
    m.mark()
    # command 3
    c.x = "third value"
    m.mark()
    # command 4
    # Check that the second assignment can be undone
    assert c.x == "third value", c.x
    m.undo()
    # command 2
    assert c.x == "second value"
    m.undo()
    # command 1
    assert c.x == "First value", c.x
    m.undo()
    assert not hasattr(c, "x")
</t>
<t tx="bwmulder.20040602230426">def test_main():

    test_support.run_unittest(
        basic_scalar_test,
        basic_list_test,					
        basic_dict_test)</t>
<t tx="bwmulder.20040602231914">def catchall(self, *args, **kwrds):
    print "delegator:", self.attributename, ":", args, kwrds
    getattr(self.undoer, self.attributename) (*args, **kwrds)
</t>
<t tx="bwmulder.20040602231934">def enable_category(self, l, monitor_class):
    
   for klass, external_attributename, internal_attributename in l:
      setattr(klass, external_attributename, monitor_class(
         external_attributename, internal_attributename, self))
    

</t>
<t tx="bwmulder.20040603081718">def remove_overrides_in_list_and_dict_monitor(self):
    """
    Deletes all function definitions in list_monitor and dict_monitor.
    The net effect of this is that instances of these classes should
    behave like regular lists and dictionaries.
    """	
    import inspect
    for klass in (list_monitor, dict_monitor):
        for attribute in dir(klass):
            try:
                entity = getattr(klass, attribute)
            except AttributeError:
                pass
            else:
                if inspect.isfunction(entity):
                    delattr(klass, attribute)
                    self.removed_functions.append(klass, attribute, entity)</t>
<t tx="bwmulder.20040603211921"></t>
<t tx="bwmulder.20040603212552">def commands(self):

    return len(self._commands) - 2</t>
<t tx="bwmulder.20040603212612">def commands_to_undo(self):

    return self._index</t>
<t tx="bwmulder.20040603212713">def commands_to_redo(self):
    return self.commands() - self._index</t>
<t tx="bwmulder.20040603212934">def rollback(self):

    self.run_commands(self._steps)
</t>
<t tx="bwmulder.20040604165011">def steps_stored(self):
    """
    Return the total number of steps stored in the undoer.
    """
    result = 0
    for command in self._commands[1:-1]:
        result += len(command)
    return result</t>
<t tx="bwmulder.20040604184443">def test_linked_list(self):
    """
    Shows that the basic undo mechanism can be used to undo the construction of a linked list.
    """
    if undo_tracing:
        self.m = m = delegator()
    else:
        self.m = m = basic_undomechanism()

    # Create a linked list and check that the link operations can be undone.
    class root_class(object):
        pass
        
    class x(object):
        def __init__(self, name, next=None):
            self.name = name
            self.next = next
    
    def p(root):
        result = []
        r = root.root
        while r:
            result.append(r.name)
            r = r.next
        return result
            
    undoer = basic_undomechanism()
    
    m.monitor_scalar(root_class, "root")
    m.monitor_scalar(x, "name")
    m.monitor_scalar(x, "next")
    m.enable()
    
    root = root_class()
    root.root = x("first")
    root.root.next = x("second")
    m.mark()
    root.root.next.next = x("third")
    root.root.next.next.next = x("fourth")
    m.mark()
    assert p(root) == ["first", "second", "third", "fourth"]
    m.undo()
    assert  p(root) == ["first", "second"]
    m.redo()
    assert p(root) ==["first", "second", "third", "fourth"]
    
    # now try a few things with dictionaries.
    m.monitor_dict_attribute_in_class(root_class, "d")
    m.enable()
    root.d = {}
    m.mark()
    root.d = {'Some dict': 1}
    m.mark()
    root.d[1] = 2
    assert root.d == {'Some dict': 1, 1: 2}, root.d
    m.mark()
    m.undo()
    assert root.d == {'Some dict': 1}, root.d
    m.undo()
    assert root.d == {}, root.d
    
    
    </t>
<t tx="bwmulder.20040605104941">class basic_list_test_class(object):
    """Simple class to test the list undoer"""
    pass

class basic_list_test(unittest.TestCase):
    """
    Test the basic operations of the list class
    """
    @others
        
</t>
<t tx="bwmulder.20040605105746">def test_lists_basic(self):
    """
    Some basic testing for the list undoer.
    
    """
    if undo_tracing:
        self.m = m = delegator()
    else:
        self.m = m = basic_undomechanism()
    m.monitor_list_attribute_in_class(basic_list_test_class, "a")
    m.enable()
    c = basic_list_test_class()
    c.a = [1, 2, 3]
    c.a = c.a
    m.mark()
    assert m.commands_to_undo() == 1, m.commands_to_undo()
    assert m.commands_to_redo() == 0, m.commands_to_redo()
    c.a.append(5)
    m.mark()
    assert m.commands_to_undo() == 2, m.commands_to_undo()
    assert m.commands_to_redo() == 0, m.commands_to_redo()
    assert c.a == [1, 2, 3, 5], c.a
    m.undo()
    assert m.commands_to_undo() == 1, m.commands_to_undo()
    assert m.commands_to_redo() == 1, m.commands_to_redo()
    assert c.a == [1, 2, 3], c.a
    m.redo()
    assert m.commands_to_undo() == 2, m.commands_to_undo()
    assert m.commands_to_redo() == 0, m.commands_to_redo()
    assert c.a == [1, 2, 3, 5], c.a
    m.undo()
    assert m.commands_to_undo() == 1, m.commands_to_undo()
    assert m.commands_to_redo() == 1, m.commands_to_redo()
    m.undo()
    assert m.commands_to_undo() == 0, m.commands_to_undo()
    assert m.commands_to_redo() == 2, m.commands_to_redo()
    assert not hasattr(c, "a"), "A should not exist here"
    assert m.steps_stored() == 3, m.steps_stored()
    m.redo()
    m.redo()
    assert c.a == [1, 2, 3, 5], c.a
    del c.a[2]
    assert c.a == [1, 2, 5], c.a # 1
    m.mark()
    m.undo()
    assert c.a == [1, 2, 3, 5], c.a # 2
    m.redo()
    assert c.a == [1, 2, 5], c.a # 3
    x = c.a.pop()
    m.mark()
    assert c.a == [1, 2]
    m.undo()
    assert c.a == [1, 2, 5]

    

    


</t>
<t tx="bwmulder.20040605174728">def test_lists_replace(self):
    """
    
    Test that list assignment works for an instance attribute that is put under the
    undo mechanism.
    
    """
    if undo_tracing:
        self.m = m = delegator()
    else:
        self.m = m = basic_undomechanism()
    c = basic_list_test_class()
    m.monitor_list_attribute_in_class(basic_list_test_class, "a")
    m.enable()
    c.a = [1, 2, 3]
    m.mark()
    m.undo()
    assert not hasattr(c,"a")
    m.redo()
    c.a.append(4)
    c.a.append(5)
    assert c.a == [1, 2, 3, 4, 5]
    m.mark()
    m.undo()
    assert c.a == [1, 2, 3]
    m.redo()
    assert c.a == [1, 2, 3, 4, 5]
    b = list_monitor(('a', 'b', 'c'), m)
    m.enable()
    b.append('d')
    assert b == ['a', 'b', 'c', 'd']
    m.mark()
    m.undo()
    assert b == ['a', 'b', 'c']
    m.redo()
    assert b == ['a', 'b', 'c', 'd']
    
    
</t>
<t tx="bwmulder.20040605180204">class basic_dict_test_class(object):
    """Simple class to test the list undoer"""
    pass

class basic_dict_test(unittest.TestCase):
    """
    Test the basic operations of the list class
    """
    @others
        

</t>
<t tx="bwmulder.20040605180225">def test_dicts_basic(self):
    """
    Some basic testing for the dict undoer.
    
    """
    trace_commands = False
    if undo_tracing:
        self.m = m = delegator()
    else:
        self.m = m = basic_undomechanism()
    m.monitor_dict_attribute_in_class(basic_dict_test_class, "a")
    m.enable()
    c = basic_dict_test_class()
    c.a = {1:1, 2:2, 3:3}
    c.a = c.a
    m.mark()
    if trace_commands:  print; m.print_commands(1)
    assert m.commands_to_undo() == 1, m.commands_to_undo()
    assert m.commands_to_redo() == 0, m.commands_to_redo()
    c.a[5] = 5
    m.mark()
    if trace_commands: m.print_commands(2)
    assert m.commands_to_undo() == 2, m.commands_to_undo()
    assert m.commands_to_redo() == 0, m.commands_to_redo()
    assert c.a == {1:1, 2:2, 3:3, 5:5}, c.a # 1
    m.undo()
    if trace_commands: m.print_commands(3)
    assert m.commands_to_undo() == 1, m.commands_to_undo()
    assert m.commands_to_redo() == 1, m.commands_to_redo()
    assert c.a == {1:1, 2:2, 3:3}, c.a # 2
    m.redo()
    if trace_commands: m.print_commands(4)
    assert m.commands_to_undo() == 2, m.commands_to_undo()
    assert m.commands_to_redo() == 0, m.commands_to_redo()
    assert c.a == {1:1, 2:2, 3:3, 5:5}, c.a # 3
    m.undo()
    if trace_commands: m.print_commands(5)
    assert m.commands_to_undo() == 1, m.commands_to_undo()
    assert m.commands_to_redo() == 1, m.commands_to_redo()
    assert c.a == {1:1, 2:2, 3:3}, c.a # 4
    m.undo()
    if trace_commands: m.print_commands(6)
    assert m.commands_to_undo() == 0, m.commands_to_undo()
    assert m.commands_to_redo() == 2, m.commands_to_redo()
    assert not hasattr(c, "a"), "A should not exist here"
    assert m.steps_stored() == 3, m.steps_stored()
    m.redo()
    if trace_commands: m.print_commands(7)
    assert c.a == {1:1, 2:2, 3:3}, c.a # 5
    m.redo()
    if trace_commands: m.print_commands(8)
    assert c.a == {1:1, 2:2, 3:3, 5:5}, c.a # 6
    del c.a[5]
    assert c.a == {1:1, 2:2, 3:3}, c.a # 7
    m.mark()
    if trace_commands: m.print_commands(9)
    m.undo()
    if trace_commands: m.print_commands(10)
    assert c.a == {1:1, 2:2, 3:3, 5:5}, c.a # 8
    m.redo()
    if trace_commands: m.print_commands(11)
    assert c.a == {1:1, 2:2, 3:3}, c.a # 9
    del c.a[2]
    m.mark()
    if trace_commands: m.print_commands(12)
    assert c.a == {1:1, 3:3}, c.a # 10
    m.undo()
    if trace_commands: m.print_commands(13)
    assert c.a == {1:1, 2:2, 3:3}, c.a # 11</t>
<t tx="bwmulder.20040605180245">def test_dicts_replace(self):
    """
    
    Test that dict assignment works for an instance attribute that is put under the
    undo mechanism.
    
    """
    if undo_tracing:
        self.m = m = delegator()
    else:
        self.m = m = basic_undomechanism()
    c = basic_dict_test_class()
    m.monitor_dict_attribute_in_class(basic_dict_test_class, "a")
    m.enable()
    c.a = {1:1, 2:2, 3:3}
    m.mark()
    m.undo()
    assert not hasattr(c,"a")
    m.redo()
    c.a[4] = 4
    c.a[5] = 5
    assert c.a == {1:1, 2:2, 3:3, 4:4, 5:5}, c.a # 1
    m.mark()
    m.undo()
    assert c.a == {1:1, 2:2, 3:3}, c.a # 2
    m.redo()
    assert c.a ==  {1:1, 2:2, 3:3, 4:4, 5:5}, c.a # 3
    b = dict_monitor({'a':'a', 'b':'b', 'c':'c'}, m)
    m.enable()
    b['d'] = 'd'
    assert b == {'a':'a', 'b':'b', 'c':'c', 'd':'d'}, b # 4
    m.mark()
    m.undo()
    assert b == {'a':'a', 'b':'b', 'c':'c'}, b # 5
    m.redo()
    assert b == {'a':'a', 'b':'b', 'c':'c', 'd':'d'}, b # 6
    
    </t>
<t tx="bwmulder.20040605220919">def print_commands(self, comment):
    """
    rint a readable list of all commands
    """
    print "===== Commands: %s ========" % comment
    i = 0
    while i &lt; len(self._commands):
        print "Command", i
        steps = self._commands[i]
        if steps:
            for step in steps:
                function, args = step
                print "  ",function.__name__, args
        if i == self._index:
            print "---------------------"
        i += 1
    print "========================"
</t>
<t tx="bwmulder.20040605231305">def __init__(self, value, monitor):
    list.__init__(self, value)
    self.set_monitor_object(monitor)
</t>
<t tx="bwmulder.20040605231401">def __init__(self, value, monitor):
    dict.__init__(self, value)
    self.set_monitor_object(monitor)
</t>
<t tx="edream.110203113231.233">@ To do:
    
     WARNING: problems with locking out event handlers could cause Leo to drop Text!
    - Do not trust this version of Leo with important data !!!
    
- The find logic doesn't properly show the found selection (or the correct body text).
    - Remove traces.

- Replace body widget with something better.

- Update joined headlines when any headline changes.

- Minor:
    - Finish all callbacks.
    - Finish dragging code.
    - Handle exception when starting by double-clicking LeoPy.leo.</t>
<t tx="edream.110203113231.234">@nocolor</t>
<t tx="edream.110203113231.235"></t>
<t tx="edream.110203113231.236">
</t>
<t tx="edream.110203113231.237">

- Almost all events connected properly.
- Code draws the screen (after the file has been read in!)
- Removed idle-time pollution: created onUpdateAllMenus.</t>
<t tx="edream.110203113231.238"></t>
<t tx="edream.110203113231.242"></t>
<t tx="edream.110203113231.257"># This updates the text of joined _headlines_, not body text.

if 0: # no longer used

    def updateJoinedHeadlines(self,text,v):
        guard = 0
        if guard &gt; 0: return
        guard += 1
        v2 = v.joinList()
        while v2 and v2 != v:
            id = v2.treeID()
            assert(id)
            self.tree.SetItemText(id,text)
            v2 = v2.joinList()
        guard -= 1</t>
<t tx="edream.110203113231.260">def finishCreate (self,c):
    
    # g.trace('wxLeoFrame')
    
    frame = self
    frame.c = c
    c.frame = frame
    
    # Init the wxFrame base class.  The leoFrame base class has already been inited.
    wx.wxFrame.__init__(self, None, -1, self.title) # wx.wxNO_3D # hangs.
    #self.outerPanel = wx.wxPanel(self,-1)
    #self.iconPanel = wx.wxPanel(self.outerPanel, -1, "iconPanel")

    self.CreateStatusBar()
    &lt;&lt; create the splitters &gt;&gt;
    frame.tree = wxLeoTree(frame,self.splitter2)
    frame.log = wxLeoLog(frame,self.splitter2)
    frame.body = wxLeoBody(frame,self.splitter1)
    frame.bodyCtrl = frame.body
    g.app.setLog(frame.log,'wxLeoFrame:finishCreate') # writeWaitingLog hangs without this(!)

    # Attach the controls to the splitter.
    self.splitter1.SplitHorizontally(self.splitter2,self.body.bodyCtrl,0)
    self.splitter2.SplitVertically(self.tree.treeCtrl,self.log.logCtrl,cSplitterWidth/2)
    
    self.menu = wxLeoMenu(frame)
    self.menu.createMenuBar()
    
    &lt;&lt; set the window icon &gt;&gt;
    &lt;&lt; declare event handlers for frame &gt;&gt;
    
    if 0: # Not ready yet...
        self.wxApp.SetTopWindow(self.wxFrame)
        self.wxFrame.Show(True)
        if not g.app.root:
            g.app.root = self.wxFrame
            
    self.colorizer = self.body.colorizer
            
    c.initVersion()
    self.signOnWithVersion()
    
    self.injectCallbacks()

    # Add the frame to the global window list.
    g.app.windowList.append(self)
    self.tree.redraw()
    self.Show(True) # required on some platforms: a cross-platform bug.</t>
<t tx="edream.110203113231.261">self.splitter1 = wx.wxSplitterWindow(self,
    const("cSplitterWindow"),
    wx.wxDefaultPosition, wx.wxDefaultSize,
    wx.wxSP_NOBORDER)

# No effect, except to create a red flash.
if 0:
    self.splitter1.SetForegroundColour(wx.wxRED)
    self.splitter1.SetBackgroundColour(wx.wxRED)

self.splitter2 = wx.wxSplitterWindow(self.splitter1, -1,
    wx.wxDefaultPosition, wx.wxDefaultSize,
    wx.wxSP_NOBORDER)
    # wx.wxSP_BORDER | wx.wxSP_3D, "splitterWindow");

self.splitter1.SetMinimumPaneSize(4)
self.splitter2.SetMinimumPaneSize(4)</t>
<t tx="edream.110203113231.264">if wx.wxPlatform == "__WXMSW__": # Activate events exist only on Windows.
    wx.EVT_ACTIVATE(self,self.onActivate)
else:
    wx.EVT_SET_FOCUS(self,self.OnSetFocus)

wx.EVT_CLOSE(self,self.onCloseLeoFrame)

wx.EVT_MENU_OPEN(self,self.updateAllMenus) 

if 0: # Causes problems at present.  The screen isn't drawn properly.
    wx.EVT_SIZE(self,self.onResize)</t>
<t tx="edream.110203113231.265">if wx.wxPlatform == "__WXMSW__":

    path = os.path.join(g.app.loadDir,"..","Icons","LeoApp16.ico")
    icon = wx.wxIcon(path,wx.wxBITMAP_TYPE_ICO,16,16)
    self.SetIcon(icon)
</t>
<t tx="edream.110203113231.266">def __init__ (self,title):
    
    # Init the leoFrame base class.
    # We will init the wxFrame base class in finishCreate.
    leoFrame.leoFrame.__init__(self,g.app.gui)
    
    self.c = None # set in finishCreate.
    self.bodyCtrl = None # set in finishCreate
    self.title = title
    
    # g.trace("wxLeoFrame",title)
    self.activeFrame = None
    self.lockout = 0 # Suppress further events
    self.quitting = False
    self.updateCount = 0
    self.treeIniting = False
    self.drawing = False # Lockout recursive draws.
    self.menuIdDict = {}
    self.menuBar = None
    self.ratio = 0.5
    self.secondary_ratio = 0.5
    self.startupWindow=False
    self.use_coloring = False # set True to enable coloring
    
    # These vars have corresponding getters/setters.
    if 0: # now defined in base tree class.
        self.mDragging = False
        self.mRootVnode = None
        self.mTopVnode = None
        self.mCurrentVnode = None</t>
<t tx="edream.110203113231.306"></t>
<t tx="edream.110203113231.307">def __init__ (self):
    
    # g.trace("wxGui")
    
    # Initialize the base class.
    if 1: # in plugin
        leoGui.leoGui.__init__(self,"wxPython")
    else:
        leoGui.__init__(self,"wxPython")
        
    self.bitmap_name = None
    self.bitmap = None</t>
<t tx="edream.110203113231.308">def createRootWindow(self):

    self.wxApp = wxLeoApp(None) # This redirects stdout &amp; stderr to stupid console.
    self.wxFrame = None

    if 0: # Not ready yet.
        self.setDefaultIcon()
        self.getDefaultConfigFont(g.app.config)
        self.setEncoding()
        self.createGlobalWindows()

    return self.wxFrame</t>
<t tx="edream.110203113231.309">def setDefaultIcon(self):
    
    """Set the icon to be used in all Leo windows.
    
    This code does nothing for Tk versions before 8.4.3."""
    
    gui = self

    try:
        version = gui.root.getvar("tk_patchLevel")
        if g.CheckVersion(version,"8.4.3"):
            # tk 8.4.3 or greater: load a 16 by 16 icon.
            path = os.path.join(g.app.loadDir,"..","Icons")
            if os.path.exists(path):
                file = os.path.join(path,"LeoApp16.ico")
                if os.path.exists(path):
                    self.bitmap = Tk.BitmapImage(file)
                else:
                    g.es("LeoApp16.ico not in Icons directory", color="red")
            else:
                g.es("Icons directory not found: "+path, color="red")
    except:
        g.es_print("exception setting bitmap")
        traceback.print_exc()</t>
<t tx="edream.110203113231.310">@ According to Martin v. Löwis, getdefaultlocale() is broken, and cannot be fixed. The workaround is to copy the g.getpreferredencoding() function from locale.py in Python 2.3a2.  This function is now in leoGlobals.py.
@c

def setEncoding (self):

    for (encoding,src) in (
        (g.app.config.tkEncoding,"config"),
        #(locale.getdefaultlocale()[1],"locale"),
        (g.getpreferredencoding(),"locale"),
        (sys.getdefaultencoding(),"sys"),
        ("utf-8","default")):
    
        if g.isValidEncoding (encoding): # 3/22/03
            g.app.tkEncoding = encoding
            # g.trace(g.app.tkEncoding,src)
            break
        elif encoding and len(encoding) &gt; 0:
            g.trace("ignoring invalid " + src + " encoding: " + `encoding`)
            
    # g.trace(g.app.tkEncoding)</t>
<t tx="edream.110203113231.311">def getDefaultConfigFont(self,config):
    
    """Get the default font from a new text widget."""

    t = Tk.Text()
    fn = t.cget("font")
    font = tkFont.Font(font=fn)
    config.defaultFont = font
    config.defaultFontFamily = font.cget("family")</t>
<t tx="edream.110203113231.312">def createGlobalWindows (self):
    
    """Create the global windows for the application."""
    
    g.app.findFrame = wxFindFrame()
    g.app.findFrame.top.withdraw()
    g.app.globalWindows.append(g.app.findFrame)</t>
<t tx="edream.110203113231.314">def finishCreate (self):

   pass
    
</t>
<t tx="edream.110203113231.315">def killGui(self,exitFlag=True):
    
    """Destroy a gui and terminate Leo if exitFlag is True."""

    pass # Not ready yet.

</t>
<t tx="edream.110203113231.316">def recreateRootWindow(self):
    """A do-nothing base class to create the hidden root window of a gui

    after a previous gui has terminated with killGui(False)."""

    g.trace('wx gui')

</t>
<t tx="edream.110203113231.317">def runMainLoop(self):

    """Run tkinter's main loop."""
    
    # g.trace("wxGui")
    self.wxApp.MainLoop()
    # g.trace("done")</t>
<t tx="edream.110203113231.347">def OnInit(self):

    self.SetAppName("Leo")

    return True</t>
<t tx="edream.110203113231.350"></t>
<t tx="edream.110203113231.351">def __repr__ (self):
    
    return "wxLeoFrame: " + self.title</t>
<t tx="edream.110203113231.540"></t>
<t tx="edream.110203113231.541">def __init__ (self,frame,parentFrame):

    # Init the base class: calls createControl.
    leoFrame.leoBody.__init__(self,frame,parentFrame)
    
    self.bodyCtrl = self.createControl(frame,parentFrame)

    self.colorizer = leoColor.colorizer(self.c)

    self.styles = {} # For syntax coloring.

    wx.EVT_TEXT(self.bodyCtrl,const("cBodyCtrl"),self.onBodyTextUpdated)</t>
<t tx="edream.110203113231.542">def createControl (self,frame,parentFrame):
    
    ctrl = wx.wxTextCtrl(parentFrame,
            const("cBodyCtrl"), "",
            wx.wxDefaultPosition, wx.wxDefaultSize,
            wx.wxTE_RICH | wx.wxTE_RICH2 | wx.wxTE_MULTILINE)

    return ctrl</t>
<t tx="edream.110203113231.618">@ It is usually best _not_ to catch exceptions in plugins:
doHook catches all exceptions and disables further calls to plugins.

If a plugin catches exceptions during startup it should either:
    
- raise the exception again.
- provide an init function at the top level that reports the failure.
@c

@language python
@tabwidth -4
@pagewidth 80
</t>
<t tx="edream.110203113231.667"></t>
<t tx="edream.110203113231.668"></t>
<t tx="edream.110203113231.677">@ignore
@language plain
@comment !
@ This node has an example of a flat configuration file (i.e. just the output of a 
'show running' command on a cisco router), and of the same configuration file 
imported by the plugin.
</t>
<t tx="edream.110203113231.678">rpr1#sh runn    
Building configuration...

Current configuration : 4927 bytes
!
! Last configuration change at 13:28:04 CET Wed Feb 19 2003
! NVRAM config last updated at 16:56:51 CET Fri Feb 14 2003
!
version 12.0
no service pad
service timestamps debug datetime localtime show-timezone
service timestamps log datetime localtime show-timezone
service password-encryption
no service single-slot-reload-enable
!
hostname rpr1
!
boot system flash rsp-k3pv-mz.120-21.S4.bin
boot system flash rsp-pv-mz.120-21.S1.bin
boot bootldr bootflash:rsp-boot-mz.120-11.S3
logging buffered 100000 debugging
enable secret 5 somepassword
!
clock timezone CET 1
ip subnet-zero
ip cef
ip name-server 10.10.10.1
ip multicast-routing
ip ssh time-out 120
ip ssh authentication-retries 3
clns routing
frame-relay switching
!
!
controller SONET 1/0/0
 framing sdh
!
controller E1 5/0/0
 framing NO-CRC4 
 clock source internal
 channel-group 1 timeslots 1
 channel-group 2 timeslots 2
!
controller E1 5/0/1
 framing NO-CRC4 
 channel-group 0 timeslots 1
!
controller E1 5/0/2
!
controller E1 5/0/3
!
controller E1 5/0/4
!
controller E1 5/0/5
!
controller E1 5/0/6
!
controller E1 5/0/7
!
!
interface Loopback0
 ip address 192.168.20.1 255.255.255.255
 no ip directed-broadcast
!
interface FastEthernet0/0/0
 description *to 2600-1 via switch*
 bandwidth 10000
 ip address 192.168.3.1 255.255.255.0
 no ip directed-broadcast
 ip pim sparse-mode
 ip route-cache flow
 no ip route-cache distributed
 no ip mroute-cache
 delay 750
 full-duplex
!
interface FastEthernet0/0/1
 description **trunk link**
 no ip address
 no ip directed-broadcast
 no ip route-cache distributed
 no ip mroute-cache
 full-duplex
!
interface FastEthernet0/0/1.1
 encapsulation dot1Q 25
 ip address 192.168.25.1 255.255.255.252
 no ip directed-broadcast
!
interface FastEthernet0/0/1.2
 no ip directed-broadcast
!
interface FastEthernet0/0/1.3
 encapsulation dot1Q 3
 ip address 192.168.4.1 255.255.255.252
 ip access-group 173 in
 no ip directed-broadcast
 ip pim sparse-mode
!
interface FastEthernet0/0/1.5
 encapsulation dot1Q 5
 ip address 192.168.5.1 255.255.255.252
 no ip directed-broadcast
!
interface FastEthernet0/0/1.50
 description to KPN-test
 encapsulation dot1Q 50
 ip address 192.168.40.1 255.255.255.252
 no ip directed-broadcast
!
interface POS4/1/0
 no ip address
 no ip directed-broadcast
 no ip route-cache distributed
 no ip mroute-cache
 loopback internal
!
interface Serial5/0/0:1
 ip address 10.31.9.1 255.255.255.252
 no ip directed-broadcast
 no ip route-cache distributed
!
interface Serial5/0/0:2
 ip address 10.10.10.1 255.255.255.252
 no ip directed-broadcast
 no ip route-cache distributed
!
interface Serial5/0/1:0
 ip address 10.31.9.5 255.255.255.252
 no ip directed-broadcast
 no ip route-cache distributed
!
interface Serial5/1/0
 no ip address
 no ip directed-broadcast
 no ip route-cache distributed
 no ip mroute-cache
 shutdown
 framing g751
 dsu bandwidth 34010
!
interface Serial5/1/1
 ip address 192.168.6.1 255.255.255.252
 no ip directed-broadcast
 encapsulation frame-relay IETF
 no ip route-cache distributed
 no ip mroute-cache
 loopback local
 framing g751
 dsu bandwidth 34010
!
interface Async1
 no ip address
 no ip directed-broadcast
 async mode interactive
 no peer default ip address
!
interface Dialer0
 no ip address
 no ip directed-broadcast
 pulse-time 0
 no cdp enable
!
router ospf 1
 log-adjacency-changes
 passive-interface FastEthernet0/0/0
 network 192.168.3.1 0.0.0.0 area 0
 network 192.168.4.0 0.0.0.3 area 0
!
router bgp 65001
 no synchronization
 redistribute static
 neighbor 192.168.3.2 remote-as 65000
 neighbor 192.168.3.2 remove-private-AS
 neighbor 192.168.3.3 remote-as 65002
 neighbor 192.168.3.3 next-hop-self
 neighbor 192.168.4.2 remote-as 65001 nlri unicast multicast
 neighbor 192.168.4.2 next-hop-self
 neighbor 192.168.4.2 default-originate
 neighbor 192.168.4.2 soft-reconfiguration inbound
 no auto-summary
!
ip classless
ip route 0.0.0.0 0.0.0.0 192.168.3.2 tag 3
ip bgp-community new-format
ip community-list 1 permit 65001:1
ip community-list 100 permit 65001:3
ip ospf name-lookup
ip pim rp-address 192.168.4.1
ip pim send-rp-discovery scope 1
!
logging facility local6
logging 10.10.10.1
access-list 173 deny   ip 224.0.0.0 31.255.255.255 any
access-list 173 permit ip any any
route-map only permit 2
 match community 65001:2
 set origin igp
!
route-map only1 permit 10
 match community 1 65001:1
 set origin igp
!
route-map only3 permit 10
 match community 100
!
route-map tag_com permit 10
 match tag 1
 set community 65001:1
!
route-map tag_com permit 20
 match tag 3
 set community 65001:3
!
!
tacacs-server host 10.10.10.1
tacacs-server key somepassword
!
line con 0
line aux 0
 transport input all
 stopbits 1
 flowcontrol hardware
line vty 0 4
 exec-timeout 0 0
 password 7 somepassword
 logging synchronous
 login
 length 0
!
ntp clock-period 17179348
ntp update-calendar
ntp peer 192.168.3.2 prefer
end

rpr1#
</t>
<t tx="edream.110203113231.679">rpr1#sh runn    
Building configuration...

Current configuration : 4927 bytes
!
! Last configuration change at 13:28:04 CET Wed Feb 19 2003
! NVRAM config last updated at 16:56:51 CET Fri Feb 14 2003
!
version 12.0
&lt;&lt;service&gt;&gt;
!
hostname rpr1
!
&lt;&lt;boot&gt;&gt;
&lt;&lt;logging&gt;&gt;
enable secret 5 somepassword
!
clock timezone CET 1
ip subnet-zero
ip cef
ip name-server 10.10.10.1
ip multicast-routing
ip ssh time-out 120
ip ssh authentication-retries 3
clns routing
frame-relay switching
!
&lt;&lt;controller&gt;&gt;
!
controller E1 5/0/2
!
controller E1 5/0/3
!
controller E1 5/0/4
!
controller E1 5/0/5
!
controller E1 5/0/6
!
controller E1 5/0/7
!
&lt;&lt;interface&gt;&gt;
!
&lt;&lt;router&gt;&gt;
!
ip classless
&lt;&lt;ip route&gt;&gt;
ip bgp-community new-format
&lt;&lt;ip community-list&gt;&gt;
ip ospf name-lookup
ip pim rp-address 192.168.4.1
ip pim send-rp-discovery scope 1
!
&lt;&lt;access-list&gt;&gt;
&lt;&lt;route-map&gt;&gt;
!
tacacs-server host 10.10.10.1
tacacs-server key somepassword
!
line con 0
&lt;&lt;line&gt;&gt;
!
&lt;&lt;ntp&gt;&gt;
end

rpr1#</t>
<t tx="edream.110203113231.680">access-list 173 deny   ip 224.0.0.0 31.255.255.255 any
access-list 173 permit ip any any</t>
<t tx="edream.110203113231.681">boot system flash rsp-k3pv-mz.120-21.S4.bin
boot system flash rsp-pv-mz.120-21.S1.bin
boot bootldr bootflash:rsp-boot-mz.120-11.S3</t>
<t tx="edream.110203113231.682"></t>
<t tx="edream.110203113231.683">controller E1 5/0/0
 framing NO-CRC4 
 clock source internal
 channel-group 1 timeslots 1
 channel-group 2 timeslots 2</t>
<t tx="edream.110203113231.684">controller E1 5/0/1
 framing NO-CRC4 
 channel-group 0 timeslots 1</t>
<t tx="edream.110203113231.685">controller SONET 1/0/0
 framing sdh</t>
<t tx="edream.110203113231.686"></t>
<t tx="edream.110203113231.687">interface Async1
 no ip address
 no ip directed-broadcast
 async mode interactive
 no peer default ip address</t>
<t tx="edream.110203113231.688">interface Dialer0
 no ip address
 no ip directed-broadcast
 pulse-time 0
 no cdp enable</t>
<t tx="edream.110203113231.689">interface FastEthernet0/0/0
 description *to 2600-1 via switch*
 bandwidth 10000
 ip address 192.168.3.1 255.255.255.0
 no ip directed-broadcast
 ip pim sparse-mode
 ip route-cache flow
 no ip route-cache distributed
 no ip mroute-cache
 delay 750
 full-duplex</t>
<t tx="edream.110203113231.690">interface FastEthernet0/0/1
 description **trunk link**
 no ip address
 no ip directed-broadcast
 no ip route-cache distributed
 no ip mroute-cache
 full-duplex</t>
<t tx="edream.110203113231.691">interface FastEthernet0/0/1.1
 encapsulation dot1Q 25
 ip address 192.168.25.1 255.255.255.252
 no ip directed-broadcast</t>
<t tx="edream.110203113231.692">interface FastEthernet0/0/1.2
 no ip directed-broadcast</t>
<t tx="edream.110203113231.693">interface FastEthernet0/0/1.3
 encapsulation dot1Q 3
 ip address 192.168.4.1 255.255.255.252
 ip access-group 173 in
 no ip directed-broadcast
 ip pim sparse-mode</t>
<t tx="edream.110203113231.694">interface FastEthernet0/0/1.5
 encapsulation dot1Q 5
 ip address 192.168.5.1 255.255.255.252
 no ip directed-broadcast</t>
<t tx="edream.110203113231.695">interface FastEthernet0/0/1.50
 description to KPN-test
 encapsulation dot1Q 50
 ip address 192.168.40.1 255.255.255.252
 no ip directed-broadcast</t>
<t tx="edream.110203113231.696">interface Loopback0
 ip address 192.168.20.1 255.255.255.255
 no ip directed-broadcast</t>
<t tx="edream.110203113231.697">interface POS4/1/0
 no ip address
 no ip directed-broadcast
 no ip route-cache distributed
 no ip mroute-cache
 loopback internal</t>
<t tx="edream.110203113231.698">interface Serial5/0/0:1
 ip address 10.31.9.1 255.255.255.252
 no ip directed-broadcast
 no ip route-cache distributed</t>
<t tx="edream.110203113231.699">interface Serial5/0/0:2
 ip address 10.10.10.1 255.255.255.252
 no ip directed-broadcast
 no ip route-cache distributed</t>
<t tx="edream.110203113231.700">interface Serial5/0/1:0
 ip address 10.31.9.5 255.255.255.252
 no ip directed-broadcast
 no ip route-cache distributed</t>
<t tx="edream.110203113231.701">interface Serial5/1/0
 no ip address
 no ip directed-broadcast
 no ip route-cache distributed
 no ip mroute-cache
 shutdown
 framing g751
 dsu bandwidth 34010</t>
<t tx="edream.110203113231.702">interface Serial5/1/1
 ip address 192.168.6.1 255.255.255.252
 no ip directed-broadcast
 encapsulation frame-relay IETF
 no ip route-cache distributed
 no ip mroute-cache
 loopback local
 framing g751
 dsu bandwidth 34010</t>
<t tx="edream.110203113231.703">ip community-list 1 permit 65001:1
ip community-list 100 permit 65001:3</t>
<t tx="edream.110203113231.704">ip route 0.0.0.0 0.0.0.0 192.168.3.2 tag 3</t>
<t tx="edream.110203113231.705"></t>
<t tx="edream.110203113231.706">line aux 0
 transport input all
 stopbits 1
 flowcontrol hardware</t>
<t tx="edream.110203113231.707">line vty 0 4
 exec-timeout 0 0
 password 7 somepassword
 logging synchronous
 login
 length 0</t>
<t tx="edream.110203113231.708">logging buffered 100000 debugging
logging facility local6
logging 10.10.10.1</t>
<t tx="edream.110203113231.709">ntp clock-period 17179348
ntp update-calendar
ntp peer 192.168.3.2 prefer</t>
<t tx="edream.110203113231.710"></t>
<t tx="edream.110203113231.711">route-map only permit 2
 match community 65001:2
 set origin igp</t>
<t tx="edream.110203113231.712">route-map only1 permit 10
 match community 1 65001:1
 set origin igp</t>
<t tx="edream.110203113231.713">route-map only3 permit 10
 match community 100</t>
<t tx="edream.110203113231.714">route-map tag_com permit 10
 match tag 1
 set community 65001:1</t>
<t tx="edream.110203113231.715">route-map tag_com permit 20
 match tag 3
 set community 65001:3</t>
<t tx="edream.110203113231.716"></t>
<t tx="edream.110203113231.717">router bgp 65001
 no synchronization
 redistribute static
 neighbor 192.168.3.2 remote-as 65000
 neighbor 192.168.3.2 remove-private-AS
 neighbor 192.168.3.3 remote-as 65002
 neighbor 192.168.3.3 next-hop-self
 neighbor 192.168.4.2 remote-as 65001 nlri unicast multicast
 neighbor 192.168.4.2 next-hop-self
 neighbor 192.168.4.2 default-originate
 neighbor 192.168.4.2 soft-reconfiguration inbound
 no auto-summary</t>
<t tx="edream.110203113231.718">router ospf 1
 log-adjacency-changes
 passive-interface FastEthernet0/0/0
 network 192.168.3.1 0.0.0.0 area 0
 network 192.168.4.0 0.0.0.3 area 0</t>
<t tx="edream.110203113231.719">no service pad
service timestamps debug datetime localtime show-timezone
service timestamps log datetime localtime show-timezone
service password-encryption
no service single-slot-reload-enable</t>
<t tx="edream.110203113231.722"></t>
<t tx="edream.110203113231.723">[Main]
active = Yes
interval = 20</t>
<t tx="edream.110203113231.729"></t>
<t tx="edream.110203113231.872"></t>
<t tx="edream.110203113231.930"># The spellpyx plugin has been retired because the Spell Tab is more convenient to use.</t>
<t tx="edream.110403140857"></t>
<t tx="edream.110403140857.1"></t>
<t tx="edream.110403140857.2">@
--How to install the wiki markup plugin--

1) first make sure that the "add_directives" plugin is enabled. This plugin turns on support for @markup directives, and it can be found in leoPlugins.leo under the section "Plugins &amp; scripts" -&gt; Directives. In particular:
    a) check that the plugin code is enabled. You should have a line like (note the "if 1"):
        if 1: # Register the handlers...
    b) generate the plugin file. Right click with the mouse on the outline heading "@file add_directives.py" and select "Write @file nodes".

2) enable the "color_markup.py" plugin:
    a) check that the plugin code is enabled. You should have a line like:
        if Tkinter: # Register the handlers...
    b) generate the plugin file. Right click with the mouse on the outline heading "@file color_markup.py" and select "Write @file nodes".

</t>
<t tx="edream.110403140857.3">@
--How to use the wiki markup plugin--

Make sure first that both the add_directives and color_markup plugins are installed and enabled (see the Installation node for details). Make also sure that coloring is not disabled for your outline (i.e. you should not have @nocolor in an ancestor node).
    
Important: coloring via wiki markups is only supported in doc parts and Python triple-double-quoted strings (not in Python triple-single-quoted strings!).

To use the wiki markup, write

@markup wiki # turn on the wiki markup
@            # start a doc part
(here goes your marked-up text, see below)

To disable the wiki markup, write

@markup      # turn off the wiki markup

You can now use the markups either selecting the Wiki menu entries (or the corresponding keyboard shortcuts) found in the Edit-&gt;Edit Body-&gt;Wiki Tags menu, or manually inserting the tags yourself. 

If you use the menus, you can either select a word and choose the appropriate menu entry to appy styling to that word, or you can just choose a menu entry (e.g. "Bold") and start writing text with the correspongin style. Select the menu entry again to return to normal text.

See the "Supported markups" for the currently supported markups.

See also the "Example" subnode. If you have the add_directives and color_markup plugins enabled, you should see the text in that node displayed as styled text.</t>
<t tx="edream.110403140857.4">@
The currently supported markups are:

''text''                   # write text in italics
__text__                   # write text in bold
~~&lt;color&gt;:text~~           # write text in the color specified by &lt;color&gt; (e.g. blue, grey, etc)
{picture file=&lt;filename&gt;}  # load the picture indicated by &lt;filename&gt;
http://url                 # URL support: double clicking on the url will open it in the default browser.
https://url                # URL support: double clicking on the url will open it in the default browser.

Note 1: italics and bold markups can be nested, e.g.

''__text__''               # write text in italics and bold

Just remember to terminate the tags in the order they were opened.

Note 2: URLs must be terminated by a space.

By default, once the text has been markup up, the actual tags (e.g. __ for bold) are not displayed anymore. You can choose to display them selecting "Show Invisibles" from the Edit menu.
</t>
<t tx="edream.110403140857.5">@color
@markup wiki
@doc (this turns on a doc section; a '@ ' would do too)

This should be ''italic'' text
This should be __bold__ text
This text should be ~~pink:colored in pink~~, ~~blue:this one in blue~~.
This text should be ''__both bold and italic__''.
Leo's homepage is at http://webpages.charter.net/edreamleo/front.html 

You can also have wiki markups in python triple-double-quoted strings:

@c

def __dummy():
    """This is a __very important__ function."""
    return None
</t>
<t tx="edream.110403140857.6">@
Wiki markups are supported ''in subnodes too''.</t>
<t tx="edream.110403140857.7">@
Version 1.2.1, October 29, 2003.

Added documentation.
Added menu entries to tag selected text and to start/end wiki tagging.

Version 1.3, October 29, 2003.

Fixed bug in the creation of the wiki menu.
Added support for clickable http tags.

Version 1.4, November 4, 2003.
Put import tkinter in a try/except block.
Made changes for 4.1 g.app.gui architecture. (More work needed).</t>
<t tx="edream.111303085447.1">def destroySelf(self):
    
    pass # Nothing more needs to be done once all windows have been destroyed.</t>
<t tx="edream.111303091300"></t>
<t tx="edream.111303092328.4">def createLeoFrame(self,title):
    
    """Create a new Leo frame."""

    return wxLeoFrame(title)</t>
<t tx="edream.111303100039"></t>
<t tx="edream.111303100039.1"></t>
<t tx="edream.111303100039.6">def insertHeadlineTime (self):
    
    g.es("insertHeadlineTime not ready yet")
    return

    frame = self ; c = frame.c ; v = c.currentVnode()
    h = v.headString() # Remember the old value.

    if v.edit_widget():
        sel1,sel2 = g.app.gui.getTextSelection(v.edit_widget())
        if sel1 and sel2 and sel1 != sel2: # 7/7/03
            v.edit_widget().delete(sel1,sel2)
        v.edit_widget().insert("insert",c.getTime(body=False))
        frame.idle_head_key(v)

    # A kludge to get around not knowing whether we are editing or not.
    if h.strip() == v.headString().strip():
        g.es("Edit headline to append date/time")</t>
<t tx="edream.111303100039.7"></t>
<t tx="edream.111303100039.8">def cascade(self):
    
    g.es("cascade not ready yet")
    return

    x,y,delta = 10,10,10
    for frame in g.app.windowList:
        top = frame.top
        # Compute w,h
        top.update_idletasks() # Required to get proper info.
        geom = top.geometry() # geom = "WidthxHeight+XOffset+YOffset"
        dim,junkx,junky = string.split(geom,'+')
        w,h = string.split(dim,'x')
        w,h = int(w),int(h)
        # Set new x,y and old w,h
        frame.setTopGeometry(w,h,x,y)
        # Compute the new offsets.
        x += 30 ; y += 30
        if x &gt; 200:
            x = 10 + delta ; y = 40 + delta
            delta += 10</t>
<t tx="edream.111303100039.9">def equalSizedPanes(self):
    
    g.es("equalSizedPanes not ready yet")
    return

    frame = self
    frame.resizePanesToRatio(0.5,frame.secondary_ratio)
</t>
<t tx="edream.111303100039.10">def hideLogWindow (self):
    
    g.es("hideLogWindow not ready yet")
    return
    
    frame = self
    frame.divideLeoSplitter2(0.99, not frame.splitVerticalFlag)</t>
<t tx="edream.111303100039.11">def minimizeAll(self):
    
    g.es("minimizeAll not ready yet")
    return

    self.minimize(g.app.findFrame)
    self.minimize(g.app.pythonFrame)
    for frame in g.app.windowList:
        self.minimize(frame)
    
def minimize(self, frame):

    if frame:
        frame.Show(False)</t>
<t tx="edream.111303100039.12"># The key invariant: self.splitVerticalFlag tells the alignment of the main splitter.
def toggleSplitDirection(self):
    
    g.es("toggleSplitDirection not ready yet")
    return

    # Abbreviations.
    frame = self
    bar1 = self.bar1 ; bar2 = self.bar2
    split1Pane1,split1Pane2 = self.split1Pane1,self.split1Pane2
    split2Pane1,split2Pane2 = self.split2Pane1,self.split2Pane2
    # Switch directions.
    verticalFlag = self.splitVerticalFlag = not self.splitVerticalFlag
    orientation = g.choose(verticalFlag,"vertical","horizontal")
    g.app.config.setWindowPref("initial_splitter_orientation",orientation)
    # Reconfigure the bars.
    bar1.place_forget()
    bar2.place_forget()
    self.configureBar(bar1,verticalFlag)
    self.configureBar(bar2,not verticalFlag)
    # Make the initial placements again.
    self.placeSplitter(bar1,split1Pane1,split1Pane2,verticalFlag)
    self.placeSplitter(bar2,split2Pane1,split2Pane2,not verticalFlag)
    # Adjust the log and body panes to give more room around the bars.
    self.reconfigurePanes()
    # Redraw with an appropriate ratio.
    vflag,ratio,secondary_ratio = frame.initialRatios()
    self.resizePanesToRatio(ratio,secondary_ratio)</t>
<t tx="edream.111303101257">def abortEditLabelCommand (self):

    g.es("abortEditLabelCommand not ready yet")
    return
    
    c = self.c ; v = c.currentVnode ; tree = self.tree
    # g.trace(v)
    if self.revertHeadline and v.edit_widget() and v == self.editVnode:
        
        # g.trace(`self.revertHeadline`)
        v.edit_widget().delete("1.0","end")
        v.edit_widget().insert("end",self.revertHeadline)
        tree.idle_head_key(v) # Must be done immediately.
        tree.revertHeadline = None
        tree.select(v)
        if v and len(v.t.joinList) &gt; 0:
            # 3/26/03: changed redraw_now to force_redraw.
            tree.force_redraw() # force a redraw of joined headlines.</t>
<t tx="edream.111303101257.1">def endEditLabelCommand (self):
    
    g.es("endEditLabelCommand not ready yet")
    return

    c = self.c ; tree = self.tree ; v = self.editVnode

    if v and v.edit_widget():
        tree.select(v)

    if v: # Bug fix 10/9/02: also redraw ancestor headlines.
        # 3/26/03: changed redraw_now to force_redraw.
        tree.force_redraw() # force a redraw of joined headlines.

    gui.set_focus(c,c.frame.bodyCtrl) # 10/14/02</t>
<t tx="edream.111303101709">def toggleActivePane(self):
    
    # This can't work from the menu...
    
    g.es("toggleActivePane not ready yet")
    return

    if self.FindFocus() == self.body.bodyCtrl:
        self.tree.SetFocus()
    else:
        self.body.bodyCtrl.SetFocus()</t>
<t tx="edream.111303103141.3">def delete_range (self,menu,n1,n2):
    
    if not menu:
        g.trace("no menu")
        return
        
    # g.trace(n1,n2,menu.GetTitle())
    
    items = menu.GetMenuItems()
    
    if 0: # debugging
        for item in items:
            id = item.GetId()
            item = menu.FindItemById(id)
            g.trace(item.GetText())
            
    ## Doesn't work:  a problem with wxPython.
    
    if len(items) &gt; n1 and len(items) &gt; n2:
        i = n1
        while i &lt;= n2:
            id = items[i].GetId()
            item = menu.FindItemById(id)
            g.trace("deleting:",item.GetText())
            menu.Delete(id)
            i += 1</t>
<t tx="edream.111303141147">def signOnWithVersion (self):

    c = self.c
    color = c.config.getColor("log_error_color")
    signon = c.getSignOnLine()
    n1,n2,n3,junk,junk=sys.version_info
    
    g.es("Leo Log Window...",color=color)
    g.es(signon)
    g.es("Python %d.%d.%d wxWindows %s" % (n1,n2,n3,wx.wxVERSION_STRING))
    g.enl()</t>
<t tx="edream.111303184347">@ The wxWindows menu code has problems:  changes do not take effect immediately.</t>
<t tx="edream.111303202917.1">def getColorizer(self):

    return self.colorizer

def recolor(self,v,incremental=False):

    if self.use_coloring:
        self.colorizer.colorize(v,incremental)

def recolor_now(self,v,incremental=False):

    if self.use_coloring:
        self.colorizer.colorize(v,incremental)
    
def recolor_range(self,v,leading,trailing):

    if self.use_coloring:
        self.colorizer.recolor_range(v,leading,trailing)
    
def updateSyntaxColorer (self,v):

    return self.colorizer.updateSyntaxColorer(v)</t>
<t tx="edream.111303204025"></t>
<t tx="edream.111303204025.1">def adjustIndex (self,index,offset):
    
    try:
        column, row = index
        return column, row + offset
    except:
        return index + offset</t>
<t tx="edream.111303204025.2">def compareIndices(self,i,rel,j):
    
    try:
        y1,x1 = i
        y2,x2 = j
        pos1 = self.bodyCtrl.XYToPosition(x1,y1)
        pos2 = self.bodyCtrl.XYToPosition(x2,y2)
    except:
        pos1 = i
        pos2 = j
    
    val = eval("%d %s %d" % (pos1,rel,pos2))
    g.trace(i,j,rel,val)
    return val</t>
<t tx="edream.111303204025.3">def convertRowColumnToIndex (self,row,column):
    
    index = self.bodyCtrl.XYToPosition(column,row-1)
    # g.trace(column,row,"-&gt;",index)
    return index</t>
<t tx="edream.111303204025.4">def convertIndexToRowColumn (self,index):
    
    x,y = self.bodyCtrl.PositionToXY(index)
    # g.trace(index,"-&gt;",y+1,x)
    return y+1,x</t>
<t tx="edream.111303204025.5">def getImageIndex (self,image):
    
    g.trace(image)</t>
<t tx="edream.111303204517"></t>
<t tx="edream.111303205442">@ The colorizer isn't ready for prime time:
    
    - It's too slow when selecting long text
    - The screen flashes too much
    - The tkColorToWxColor routine needs much more work.
    
wxLeo should use wxStc rather than wxText!</t>
<t tx="edream.111303205611">def tag_add (self,tagName,index1,index2):
    
    # g.trace(tagName,index1,index2)

    style = self.styles.get(tagName)
    if style:
        self.bodyCtrl.SetStyle(index1,index2,style)</t>
<t tx="edream.111303205611.1">def tag_bind (self,tagName,event,callback):
    
    # g.trace(tagName,event,callback)
    pass
</t>
<t tx="edream.111303205611.2">def tag_configure (self,colorName,**keys):
    
    foreground = keys.get("foreground")
    background = keys.get("background")

    if foreground:
        fcolor = self.tkColorToWxColor (foreground)
        bcolor = self.tkColorToWxColor (background)
        if fcolor and bcolor:
            # g.trace(colorName,foreground,keys)
            style = wx.wxTextAttr(fcolor,bcolor)
            self.styles[colorName] = style
        elif fcolor:
            style = wx.wxTextAttr(fcolor)
            self.styles[colorName] = style</t>
<t tx="edream.111303205611.3">def tag_delete(self,tagName):

    if tagName == "keyword": # A kludge.

        # g.trace(tagName)
        style = wx.wxTextAttr(wx.wxBLACK)
        last = self.maxWxIndex()
        
        if 1: # This may cause the screen flash.
            self.bodyCtrl.SetStyle(0,last,style)</t>
<t tx="edream.111303205611.4">def tag_remove (self,tagName,index1,index2):
    
    g.trace(tagName,index1,index2)
    pass
</t>
<t tx="edream.111403080609">def maxWxIndex (self):
    
    return self.bodyCtrl.GetLastPosition()</t>
<t tx="edream.111403082513">def tkColorToWxColor (self, color):
    
    d = {
        "red": wx.wxRED,
        "blue": wx.wxBLUE,
        "#00aa00": wx.wxGREEN,
        "firebrick3": wx.wxRED }
        
    return d.get(color)</t>
<t tx="edream.111403093253">The new code now works with the new reorg.  This means that wxLeo is using all the code in Leo's core.

In particular:

- wxLeo creates all menus using the base leoMenu class.
- wxLeo uses all commands in the Commands class.
- wxLeoFrame contains only gui-dependent commands.

The syntax colorer is working in demo mode.  Almost certainly wxLeo should use a better control than wxText.</t>
<t tx="edream.111403093253.1"></t>
<t tx="edream.111403141810">def initialRatios (self):

    config = g.app.config
    s = config.getWindowPref("initial_splitter_orientation")
    verticalFlag = s == None or (s != "h" and s != "horizontal")
    
    # Tweaked for tk.  Other tweaks may be best for wx.
    if verticalFlag:
        r = config.getFloatWindowPref("initial_vertical_ratio")
        if r == None or r &lt; 0.0 or r &gt; 1.0: r = 0.5
        r2 = config.getFloatWindowPref("initial_vertical_secondary_ratio")
        if r2 == None or r2 &lt; 0.0 or r2 &gt; 1.0: r2 = 0.8
    else:
        r = config.getFloatWindowPref("initial_horizontal_ratio")
        if r == None or r &lt; 0.0 or r &gt; 1.0: r = 0.3
        r2 = config.getFloatWindowPref("initial_horizontal_secondary_ratio")
        if r2 == None or r2 &lt; 0.0 or r2 &gt; 1.0: r2 = 0.8

    return verticalFlag,r,r2</t>
<t tx="edream.111503105816">def injectCallbacks(self):
    
    import leoNodes
    
    # Some callback is required.
    def doNothingCallback(*args,**keys):
        pass

    for name in (
        "OnBoxClick","OnDrag","OnEndDrag",
        "OnHeadlineClick","OnHeadlineRightClick","OnHeadlineKey",
        "OnHyperLinkControlClick","OnHyperLinkEnter","OnHyperLinkLeave",
        "OnIconClick","OnIconDoubleClick","OnIconRightClick"):

        # g.trace(f)
        g.funcToMethod(doNothingCallback,leoNodes.vnode,name=name)</t>
<t tx="edream.111503110300">At this point, Leo is useable.

What I did:

- Added use_coloring ivar to the wxLeoFrame class.  The body text is syntax colored only if this is True.
    This is set to False at present because the default colors are very poor.
    Also, coloring causes the body pane to scroll for large text.  These are minor problems...

- Got find panel working.  This required creating dummy wxSearchWidget class.  Probably _all_ the search code should be in the base leoFind class, but that would making supporting regexp searches harder.

- Simplified the event handlers in the find panel.  We can use tables to _create_ the event handlers.

- Solved the problem with selecting new nodes: we must lock out further event handling once an event handler starts.  In particular, the syntax colorer generates a lot of other events.  This also prevents the outline from being marked dirty when a new node is selected.

- Added code to insject do-nothing callbacks into vnode class.  This is required by the syntax colorer.

Later:

- Completed Find panel.

- Made sure Leo prompts when closing a window.
    - The new code is very simple: it just calls g.app.closeLeoWindow.
        - Removed some gui dependencies from the g.app.finishQuit logic.
          (They are now in the g.app.tkinterGui.destroySelf routine.)

- Implemented the wx gui dialog code.
    - Only the number dialog remains...

Very little remains to be done, and nothing big.</t>
<t tx="edream.111503111350"></t>
<t tx="edream.111503213533">def destroySelf(self):
    
    self.Destroy()</t>
<t tx="edream.111703103908"></t>
<t tx="edream.111703103908.2">def leoHelp (self):
    
    g.es("leoHelp not ready yet")
    
    return ##
    
    file = os.path.join(g.app.loadDir,"..","doc","sbooks.chm")
    file = g.toUnicode(file,g.app.tkEncoding) # 10/20/03

    if os.path.exists(file):
        os.startfile(file)
    else:	
        answer = g.app.gui.runAskYesNoDialog(c,
            "Download Tutorial?",
            "Download tutorial (sbooks.chm) from SourceForge?")

        if answer == "yes":
            try:
                if 0: # Download directly.  (showProgressBar needs a lot of work)
                    url = "http://umn.dl.sourceforge.net/sourceforge/leo/sbooks.chm"
                    import urllib
                    self.scale = None
                    urllib.urlretrieve(url,file,self.showProgressBar)
                    if self.scale:
                        self.scale.destroy()
                        self.scale = None
                else:
                    url = "http://prdownloads.sourceforge.net/leo/sbooks.chm?download"
                    import webbrowser
                    os.chdir(g.app.loadDir)
                    webbrowser.open_new(url)
            except:
                g.es("exception dowloading sbooks.chm")
                g.es_exception()</t>
<t tx="edream.111703103908.3">def showProgressBar (self,count,size,total):

    # g.trace("count,size,total:" + `count` + "," + `size` + "," + `total`)
    if self.scale == None:
        &lt;&lt; create the scale widget &gt;&gt;
    self.scale.set(count*size)
    self.scale.update_idletasks()</t>
<t tx="edream.111703103908.4">top = Tk.Toplevel()
top.title("Download progress")
self.scale = scale = Tk.Scale(top,state="normal",orient="horizontal",from_=0,to=total)
scale.pack()
top.lift()</t>
<t tx="ekr.20040205071616">&lt;&lt; docstring &gt;&gt;
&lt;&lt; imports &gt;&gt;

OKFLAG='OK '  # Space required.
__version__ = "0.1"

@others

if Tk and not g.app.unitTesting: # Not (yet) for unit testing.

    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":
        leoPlugins.registerHandler("start1", onStart)
        leoPlugins.registerHandler("create-optional-menus",create_UserMenu)
        leoPlugins.registerHandler("iconrclick2", onRclick)
        g.plugin_signon(__name__)
        g.es('mnplug OK+Commands+Menu aktiv',color='green')</t>
<t tx="ekr.20040205071616.1">def mnstamp():

    lt=time.localtime(time.time())
    mndatetime=time.strftime('%y%m%d %H:%M',(lt))
    return '### '+g.app.leoID+mndatetime
</t>
<t tx="ekr.20040205071616.2">def mnOKstamp():

    lt=time.localtime(time.time())
    mndatetime=time.strftime('%y%m%d %H:%M',(lt))
    return '###'+OKFLAG+g.app.leoID+mndatetime
</t>
<t tx="ekr.20040205071616.3">def onStart (tag,keywords):

    # insert function insertUser as method of class Commands at runtime
    g.funcToMethod(insertUser,leoCommands.Commands)
    g.funcToMethod(insertOKcmd,leoCommands.Commands)

</t>
<t tx="ekr.20040205071616.4">def setHeadOK(v):

    s = OKFLAG + v.headString()
    v.setHeadStringOrHeadline(s)

</t>
<t tx="ekr.20040205071616.5">def insertBodystamp(c,v):

    stamp=mnOKstamp()+'\n'

    # insertAtBegin - ??!! workaround ??!! 
    # insertPointFormat is  ('row.column')
    
    oldip=c.frame.body.getInsertionPoint()
    newip=str(int(string.split(oldip,'.')[0])+1)+'.'+string.split(oldip,'.')[1]

    c.frame.body.setInsertionPoint('0.0')
    c.frame.body.insertAtInsertPoint(stamp)
    c.frame.body.setInsertionPoint(newip)
    c.frame.body.onBodyChanged("Typing")</t>
<t tx="ekr.20040205071616.6">def is_subnodesOK(v):

    if not v.hasChildren():
        return True
    else:
        ok = False
        child=v.firstChild()
        while child:
            s=child.headString()
            ok=s[0:len(OKFLAG)]==OKFLAG
            if not ok:break
            child=child.next()
    return ok

</t>
<t tx="ekr.20040205071616.7">def onRclick(tag,keywords):
    
    """Handle right click in body pane."""

    c=keywords.get('c')
    insertOKcmd(c)</t>
<t tx="ekr.20040205071616.8">def insertOKcmd(self,event=None):

    c=self; v=c.currentVnode()  
    
    if is_subnodesOK(v) :
        setHeadOK(v)
        insertBodystamp(c,v)
    else: 
        g.es('OK in child missing')</t>
<t tx="ekr.20040205071616.9">def insertUser (self,event=None):
    
    """Handle the Insert User command."""

    c = self ; v = c.currentVnode()
    
    oldSel = c.frame.body.getTextSelection()
    c.frame.body.deleteTextSelection() # Works if nothing is selected.
    
    s = mnstamp()
    
    c.frame.body.insertAtInsertPoint(s)
    c.frame.body.onBodyChanged("Typing",oldSel=oldSel)</t>
<t tx="ekr.20040205071616.10">def create_UserMenu (tag,keywords):

    c = keywords.get("c")
    
    c.pluginsMenu = c.frame.menu.createNewMenu("UserMenu")

    table = [
        ("insUser", 'Shift+F6', c.insertUser),
        ("insOK",'Ctrl+Shift+O',c.insertOKcmd)]

    c.frame.menu.createMenuEntries(c.pluginMenu,table,dynamicMenu=True)</t>
<t tx="ekr.20040331071919"></t>
<t tx="ekr.20040331071919.1">@language plain
@ascfile "doc/mod_asc_dev.asc"
@doc                
@ascskip # Time-stamp: "Mon, Jan 19 15:30 CST 2004  michael@redpriest Leo_AsciiDoc_Developers_Guide_141612300.txt"
Preface
-------

Leo2AsciiDoc is a small Python program which has been built to be used as
a plugin module for the Leo outlining editor.

This is the Developer Documentation and source code listing of
Leo2AsciiDoc.

Leo2AsciiDoc enables the contents of Leo outlines to be published to
HTML or PDF via the DocBook XML set of publishing tools.  Plain text
from the Leo outline is transformed into a final result that has:

    - typeset body text, in which bulleted and numbered lists,
      variable lists, page numbers, URLs, index terms,and bold and
      italic text are automatically recognized.
    - typeset Headings
    - a Table of Contents
    - an Index containing any items marked by the user, and any
      Python classes or functions.

indexterm:[Literate Programming]
For programmers, Leo2AsciiDoc enables a simplified version of
Literate Programming: all the documentation and code for a program
can be written in a Leo outline, and published with just a few
keystrokes.  As is normal for a Leo outline, Leo can also extract
the source code from the outline and package it into text files,
ready to be run or compiled.

Specifically, what the Leo2AsciiDoc program does is:

    - wait to be called by the Leo menu (File; Export; Export to
      AsciiDoc), and then
    - read a part of a Leo outline, and
    - write the contents to a text file that can be understood by
      the AsciiDoc program.

From there:

    - the xref:AsciiDoc[] program can then convert that text file to
      another text file that is in the DocBook XML format.
    - the standard collection of xref:DocBook[] tools can then format the
      text in HTML (web page) files or as a typeset PDF file.
    - Once set up, the whole process happens quickly and
      automatically, usually with a simple "make" command.

Here are some web locations for the items I've referenced above:

Leo::    
    http://webpages.charter.net/edreamleo/front.html[]
Python::
    http://www.python.org[]
Docbook::    
    http://docbook.org/[]
Literate Programming::
    http://www.literateprogramming.com/[]
AsciiDoc::
    http://www.methods.co.nz/asciidoc/[]
PDF::
    Adobe provides a free program, Adobe Acrobat Reader (Windows &amp;
    Linux), that is used to read and print documents produced in the
    Adobe Portable Document Format.
    http://www.adobe.com/products/acrobat/readermain.html[]

---
Michael Dawson
Marshall Research
michael_dawson at marshallresearch dot com
---
@code</t>
<t tx="ekr.20040331071919.2">@doc
@ascskip # Time-stamp: "Fri, Jan  9 15:19 CST 2004  michael@redpriest About_this_document_140583820.txt"

If you are reading this document in HTML (in a web browser) or as a
PDF file (usually in Adobe Acrobat Reader), it may interest you to
know that this document was generated from a Leo outline.

The Leo outline (in the file mod_leo2ascd.leo) contained the
Leo2AsciiDoc Users Guide, the Leo2AsciiDoc Developers Guide, and all
the Leo2AsciiDoc source code.  All of them were created by simply
typing plain text.

The working source code was exported by Leo using the "File; Tangle;
Tangle" menu selection, which created the Python program file
"mod_leo2ascd.py".

The Users Guide and the Developers Guide were created by exporting
the text from Leo, using the menu selection "File; Export; Export
All to AsciiDoc".  This created the plain text files
"mod_asc_user.asc" and "mod_asc_dev.asc" (which are the file names I
told Leo to use.)

I then typed "make all" at the console in the directory, and the
make program:

    - ran the AsciiDoc program to produce the DocBook XML files.
    - ran the xsltproc program to produce the HTML files from the
      XML files.
    - ran the xsltproc program to produce "fo" files, and ran the
      fop program to produce PDF files from the fo files.

Everything was generated automatically without any further work on
my part.

@code</t>
<t tx="ekr.20040331071919.3">@doc
@ascskip # Time-stamp: "Mon, Jan 19 15:28 CST 2004  michael@redpriest License_141615068.txt"

This is part of the Leo2AsciiDoc software package, which is released
as open source.  

The license is the most "open" I know of, and is sometimes referred
to as the "X11" or "MIT" license.  Boiled down, in non-legal terms:

    - the software is yours for free -- to run, modify and
      distribute as you will
    - I have no legal liability for any of it
    - you may not use my name.

Michael Dawson
Marshall Research
michael_dawson at marshallresearch dot com

NOTE: The following license is often referred to as the "MIT/X
Consortium License", as the "MIT license" and as the "X11" license.
My source for the exact wording is the copy at the Open Source
Initiative:  http://opensource.org/licenses/mit-license.html[]


@code
</t>
<t tx="ekr.20040331071919.4">@doc
@ascskip # Time-stamp: "Fri, Jan  9 09:18 CST 2004  michael@redpriest License_document_140581532.txt"
---
Terms and Conditions
 
COPYRIGHT AND PERMISSION NOTICE

Copyright (c) 1999,2000,2001,2002,2003,2004 Michael W. Dawson

All rights reserved.

Permission is hereby granted, free of charge, to any person
obtaining a copy of this software and associated documentation files
(the "Software"), to deal in the Software without restriction,
including without limitation the rights to use, copy, modify, merge,
publish, distribute, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, provided
that the above copyright notice(s) and this permission notice appear
in all copies of the Software and that both the above copyright
notice(s) and this permission notice appear in supporting
documentation.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
NONINFRINGEMENT OF THIRD PARTY RIGHTS. IN NO EVENT SHALL THE
COPYRIGHT HOLDER OR HOLDERS INCLUDED IN THIS NOTICE BE LIABLE FOR
ANY CLAIM, OR ANY SPECIAL INDIRECT OR CONSEQUENTIAL DAMAGES, OR ANY
DAMAGES WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS,
WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS
ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR PERFORMANCE
OF THIS SOFTWARE.

Except as contained in this notice, the name of a copyright holder
shall not be used in advertising or otherwise to promote the sale,
use or other dealings in this Software without prior written
authorization of the copyright holder.
---
@code</t>
<t tx="ekr.20040331071919.5">@doc
@ascskip # Time-stamp: "Fri, Jan  9 16:13 CST 2004  michael@redpriest Version_Requirements_140584132.txt"

This is version 0.4 of Leo2AsciiDoc.  The major version of zero
indicates that it is an in-house version, not suitable for
production use elsewhere.

It was created and tested using:

    - Leo version 4.1 (release candidate 3).  Leo2AsciiDoc was
      upgraded to use the new features in 4.1 and is no longer
      compatible with previous versions.
    - AsciiDoc version 5.0.2.  Leo2AsciiDoc was upgraded to use the
      new features in 5.0.2, and is no longer compatible with older
      versions of AsciiDoc.
    - DocBook XML DTD version 4.2 and DocBook XSL stylesheets 1.60.1
    - xsltproc 1.0.30
    - fop 0.20.5

The last three items are the DocBook tool chain I'm currently using.
Any working DocBook XML tool chain you may have is likely to work,
since the major Leo2AsciiDoc effort is in producing the XML files
the tool chain uses as input.

@code</t>
<t tx="ekr.20040331071919.6">@language plain
@doc
@ascskip # Time-stamp: "Fri, Jan  9 16:00 CST 2004  michael@redpriest The_General_Approach_140588436.txt"

Leo2AsciiDoc simply copies the text from a portion of a Leo outline
to a text file.  That text file can then be processed by other
programs to produce HTML, PDF's, etc.

The text will be copied from each outline item, in outline order,
though you can skip individual nodes or sub-trees.

The idea is that you write the outline as a book, or series of
books.

If your book contains source code, you can break it up into pieces
that make it convenient to review with the reader.  Additionally,
you can discuss the pieces in any order that you like.  Using the
"tangle" command, Leo will be able to assemble and reorder the
pieces in the order required for a file of compilable source code.

As the text is copied from the outline, Leo2AsciiDoc adds minimal markup,
generally:

    - It marks up node headlines as Titles and Section Headings
      in the AsciiDoc format.
    - Program listings have AsciiDoc section markers inserted before
      and after.

A specific list follows.

@code</t>
<t tx="ekr.20040331071919.7">@language plain
@doc
@ascskip # Time-stamp: "Fri, Jan  9 16:05 CST 2004  michael@redpriest Markup_Added_140589620.txt"

    - headings:
        * By default, all outline node headings are underlined with
          the appropriate section underline character, which
          AsciiDoc will use to transform the headings into titles:
          chapter, section1, section2, etc.
        * code extracts are given an "example" heading.
    - source code sections are marked with delimiters, so that they
      can be assigned to the DocBook "programlisting" element.
    - source code sections are line-wrapped in the document output,
      for convenient html display.
    - wherever source code is exported to a source code file, the
      document with note this with an automatically generated "note"
      element.

@code
</t>
<t tx="ekr.20040331071919.8">@language python
@tabwidth -4

@doc
@ascskip on
 @silent
NB: remove leading space from above silent directive for final clean
code.

@ascskip off
@ascskip # Time-stamp: "Thu, Dec  4 11:58 CST 2003  michael@redpriest _The_Code__140751676.py"

This chapter contains all the source code for the Leo2AsciiDoc program.
The code is arranged in an order that is convenient for discussion.

On its way from the Leo outline to this document, the code has been
reformatted for printing.  Please note that:

    - code lines that are longer than the current publishing limit
      are wrapped.  Wrapped lines end in a "\" character and have
      the remainder of the text on the next line, preceeded by 4
      spaces. The real working code is not changed in this way when
      exported for actual use.
    - Some code has been extracted as Examples, and has a title
      saying something like "Example: Interesting Code".  Rather
      than repeat that code in the main code body, there is simply a
      reference to the name, enclosed in double angle brackets:
      \&lt;&lt;Interesting Code&gt;&gt;. All extracts are indexed, see "Python
      code, extracts used" in the Index at the end of the document.

@ascskip on
@root "mod_leo2ascd.py"
__version__ = ".5" # Set version for the plugin handler.
&lt;&lt; Declarations and Utilities &gt;&gt;
&lt;&lt; Write the outline tree as AsciiDoc file &gt;&gt;
&lt;&lt; Write a node &gt;&gt;
&lt;&lt; Key Functions &gt;&gt;
@code</t>
<t tx="ekr.20040331071919.9">@doc
@ascskip # Time-stamp: "Thu, Dec  4 16:05 CST 2003  michael@redpriest _Key_Functions__141128028.py"

These are the top-level functions that can be called from the Leo menu.

The next function writes the Leo outline tree of the current node to
a text file.  It first checks to see that there is an ascfile
directive in the current node, or above it, and then calls the
WriteTreeAsAsc function to write the tree starting at the ascfile
node.

If you have several documents in one Leo outline, this function will
write out the current one.

@code

def WriteTreeOfCurrentNode(c):
    f = c.frame
    vnode = c.currentVnode() # get the current vnode.
    while vnode:
        ascFileN = GetAscFilename(vnode)
        if ascFileN == None:
            vnode = vnode.parent()
        else:
            break

    if ascFileN == None:
        g.es("Sorry, there was no @ascfile directive in this outline tree.")
    else:
        WriteTreeAsAsc(vnode, ascFileN)

@doc

The next function exports all Leo2AsciiDoc documents in the entire Leo
outline, starting at the top and working through all nodes.

@code
def WriteAll(c):
    f = c.frame
    v = c.rootVnode()
    while v:
        ascFileN = GetAscFilename(v)
        if ascFileN != None:
            WriteTreeAsAsc(v, ascFileN)
            v = v.nodeAfterTree()
        else:
            v = v.threadNext()
@doc

This function is handy to see all the Leo2AsciiDoc sub-trees and source
code sub-trees in a Leo outline.  It prints the results in the log pane.

@code

def WriteAllRoots(c):
    "Writes @root directive and/or @ascfile directive to log pane."

    patternAscDirectiveFile = re.compile(r'^@ascfile')
    patternRoot = re.compile(r'^@root')

    g.es('Looking for @root or @ascfile.')
    f = c.frame
    vnode = c.rootVnode()
    while vnode:
        bodyString = vnode.bodyString()
        lines = bodyString.splitlines()
        printedHeading = False
        for line in lines:
            printLine = False
            containsAscFileDirective = patternAscDirectiveFile.match(line)
            if containsAscFileDirective:
                printLine = True
            containsRootDirective = patternRoot.match(line)
            if containsRootDirective:
                printLine = True
            if printLine:
                if not printedHeading:
                    g.es(vnode.headString())
                    printedHeading = True
                g.es('  ' + line)
        vnode = vnode.threadNext()

@doc

Next, we simply create Leo menu items for the above functions,
assuming Leo is loading this code as a module (i.e. the Python
source has been placed in the Leo plugins directory.)  As a module,
the phrase "if 0:" must be changed to "if 1:" to activate the
module.

But while the "if 0:" is left, this code can be used as a script
from the Leo scripts menu (assuming a copy of the code has been
placed in the Leo scripts directory), implementing the WriteAll
function above. This is useful in testing.

@code
def CreateAscMenu(tag,keywords):

    """Create the Outline to AsciiDoc menu item in the Export menu."""
    
    c = keywords.get('c')
    if not c: return

    exportMenu = c.frame.menu.getMenu('export')
    newEntries = (
        ("-", None, None),
        ("Export all to &amp;AsciiDoc","Alt+Shift+A",WriteAll),
        ("Export current tree to AsciiDoc","Alt+Shift+T",WriteTreeOfCurrentNode),
        ("Log all root and ascfile to log pane","Alt+Shift+L",WriteAllRoots),
    )

    c.frame.menu.createMenuEntries(exportMenu, newEntries,dynamicMenu=True)
    
if 1:
    def init():
        ok = True
        leoPlugins.registerHandler(('new','open2'), CreateAscMenu)
        g.plugin_signon(__name__)
        return ok
else:
    WriteTreeOfCurrentNode()

@doc</t>
<t tx="ekr.20040331071919.10">@doc
@ascskip # Time-stamp: "Tue, Nov 25 11:25 CST 2003  michael@redpriest _Declarations_and_Utilities__140958380.py"

Next, we define new directives to control the way we export the Leo
text, as seen in this extract from the main code.  Directives start
with an "@" character as the first character in the line.

@code
&lt;&lt;New Leo2AsciiDoc directives&gt;&gt;=
patternAscDirectiveConfig = re.compile(r'^@ascconfig\W+(\w+)\s+(\S+)')
patternAscDirectiveFile = re.compile(r'^@ascfile *"*([\w\\/\.]*)"*')
patternAscDirectiveExit = re.compile(r"^@ascexit")
patternAscDirectiveIgnore = re.compile(r"^@ascignore")
patternAscDirectiveSkip = re.compile(r"^@ascskip")
patternAscDirectiveSkipToggle = re.compile(r"^@ascskip\s*(\w+)+.*")
@doc

Next, a class to simulate constants, and make it easy to use
them. We create a class whose variables can be assigned, but not
reassigned inadvertently. As well, the "Next" function gives us an
easy way to acquire a variable of unique value when we don't care
what that value actually is, just that it is unique.

@code
&lt;&lt;Simulate Python constants&gt;&gt;=
class   _AssignUniqueConstantValue:
    """ Provide unique value to be used as a constant """
    def __init__(self):
        self.UniqueInternalValue = 0
        self.Assign_at_start()

    class ConstError(TypeError): pass
    def __setattr__(self,name,value):
        if self.__dict__.has_key(name):
            if name != "UniqueInternalValue":
                raise self.ConstError, "Can't rebind const(%s)"%name
        self.__dict__[name]=value

    def Assign_at_start(self):
        self.END_PROGRAM = self.Next()   # signal abort
        self.LINE_WAS_NONE = self.Next() # describe last line printed
        self.LINE_WAS_CODE = self.Next()
        self.LINE_WAS_DOC  = self.Next()
        self.LINE_WAS_HEAD = self.Next()
        self.LINE_PENDING_NONE  = self.Next() # describe next line to be printed
        self.LINE_PENDING_CODE  = self.Next()
        self.LINE_PENDING_DOC   = self.Next()

    def Next(self):
        self.UniqueInternalValue += 1
        return(self.UniqueInternalValue)
@doc
@ascexit
@code
&lt;&lt;The Code -- Declarations and Utilities&gt;&gt;</t>
<t tx="ekr.20040331071919.11">@
@ascskip # Time-stamp: "Fri, Dec 19 10:42 CST 2003  michael@redpriest _The_Code_Declarations_and_Utilities__140568852.py"

Here we begin the Python program, importing the modules we need, and
signing on as the Leo2AsciiDoc module in the Leo log window.
@c

import leoGlobals as g
import leoPlugins

import re
import os

g.es("---mod_leo2asc 0.4-------")

@
Next, a class to hold our configuration data. Users can change the
Leo2AsciiDoc configuration by including an "@ascconfig" directive in the
body text of a Leo outline, either in the root node or in the same
node as an "@ascfile" directive.  User directives in the root node
override the Leo2AsciiDoc defaults. Further, directives in an ascfile
node not only override the Leo2AsciiDoc defaults, but also any user
directives in the root node.
@c

&lt;&lt;Simulate Python constants&gt;&gt;

class _ConfigOptions:
    """Hold current configuration options."""
    def __init__(self):
        self.current = {}
        self.default = {}
        self.default["maxCodeLineLength"] = '76'
        self.default["delimiterForCodeStart"] = '~-~--- code starts --------'
        self.default["delimiterForCodeEnd"]   = '~-~--- code ends ----------'
        self.default["delimiterForCodeSectionDefinition"] = '*example*'
        self.default["headingUnderlines"] = '=-~^+'
        self.default["asciiDocSectionLevels"] = '5'
        self.default["PrintHeadings"] = "on"

    def __GetNodeOptions(self, vnode):
        bodyString = vnode.bodyString()
        lines = bodyString.splitlines()
        for line in lines:
            containsAscConfigDirective = patternAscDirectiveConfig.match(line)
            if containsAscConfigDirective:
                # Leo uses unicode, convert to plain ascii
                name = str(containsAscConfigDirective.group(1))
                value = str(containsAscConfigDirective.group(2))
                if self.current.has_key(name):
                    self.current[name] = value
                else:
                    g.es(vnode.headString())
                    g.es("  No such config option: %s" % name)

    def GetCurrentOptions(self,c,vnode):
        self.current.clear()
        self.current = self.default.copy()
        v = c.rootVnode()
        self.__GetNodeOptions(v)             # root node
        self.__GetNodeOptions(vnode)         # current node

# ----- assign constants ---------------------------------------------------
CV = _AssignUniqueConstantValue()
CV.NODE_IGNORE = CV.Next()              # demo of adding in code
Conf = _ConfigOptions()

# ----- globals ------------------------------------------------------------
#   compile the patterns we'll be searching for frequently
patternSectionName = re.compile("\&lt;\&lt; *(.+?) *\&gt;\&gt;")
patternSectionDefinition = re.compile("(\&lt;\&lt; *)(.+?)( *\&gt;\&gt;)(=)")
patternDirective = re.compile(r"^@")
patternCodeDirective = re.compile(r"^(@c *$)|(@code)")
patternDocDirective = re.compile(r"^(@ |@doc)(.*)")
patternRootDirective = re.compile(r"^@root\s+(.+)")
patternAscDirective = re.compile(r"^@asc")
&lt;&lt;New Leo2AsciiDoc directives&gt;&gt;
@doc

AsciiDoc recognizes titles and section headings by the underlining (a
line of characters on the next line after the text) with a line
of flag characters.  This function calculates the section level
(considering the ascfile node to be the top or "book" level) and
creates the appropriate string of flag characters.

@code
def SectionUnderline(h,level,v):
    'Return a section underline string.'
    asciiDocSectionLevels = int(Conf.current["asciiDocSectionLevels"])
    if level &lt; 0:
        g.es("Section level is less than 1:\n  %s" % v.headString())
        level = 1
    elif level &gt; asciiDocSectionLevels - 1:
        g.es("Section level is more than maximum Section Levels: %d\n  %s" \
           % (asciiDocSectionLevels, v.headString()))
        level = asciiDocSectionLevels - 1
    str = Conf.current["headingUnderlines"][level]  #'
    return str*max(len(h),1)
@doc

GetAscFilename is a frequently used function that checks a node for
the presence of an "@ascfile" directive, which specifies the name
and location of the Leo2AsciiDoc output file.

Leo2AsciiDoc will not export text without finding a file name. If no path
is given, the file will be created in the same directory as the Leo
outline.

@code
def GetAscFilename(c,vnode):
    'Checks a node for a filename directive.'
    # f is the Leo outline
    ascFileName = None
    bodyString = vnode.bodyString()
    lines = bodyString.splitlines()
    for line in lines:
        containsAscFileDirective = patternAscDirectiveFile.match(line)
        if containsAscFileDirective:
            ascFileName = containsAscFileDirective.group(1)
            if (ascFileName != None):
                base = os.path.split(c.mFileName)[0]  # linux or windows
                if (((base[0]=="/") and (ascFileName[0] != "/")) or 
                   ((base[1]==":") and (ascFileName[1] != ":"))): 
                    # no full pathname specified
                    ascFileName = os.path.join(base, ascFileName)
                Conf.GetCurrentOptions(vnode)
    return ascFileName
        
@doc

CodeChunk splits a line of text into chunks of a maximum length.
This is used in exporting source code sections of the Leo outline
for publication.

@code
def CodeChunk(text, width=72):
    """Split a line of text into a list of chunks not longer
    than width."""
    chunkList = []
    chunkStart = 0
    chunkEnd = 0
    lastSpacePosition = 0
    shortWidth = width - 4
    prefix = ''
    suffix = ' \\'
    textLen = len(text)
    if width &gt; textLen:
        chunkList.append(text)
    else:
        while chunkEnd &lt; textLen:
            if len(chunkList) &gt; 0:
                prefix = '  '
            chunkEnd = chunkStart + shortWidth
            if chunkEnd &gt; textLen:
                chunkList.append(prefix + text[chunkStart:])
                chunkEnd = textLen          # get out of jail
            else:
                lastSpacePosition = text.rfind(' ',chunkStart, chunkEnd +1)
                if lastSpacePosition != -1:  # success
                    chunkList.append(prefix + text[chunkStart:lastSpacePosition] + ' \\')
                    chunkStart = lastSpacePosition + 1
                else:
                    chunkEnd = chunkStart + shortWidth
                    chunkList.append(prefix + text[chunkStart:chunkEnd] + ' \\')
                    chunkStart = chunkEnd
    return chunkList</t>
<t tx="ekr.20040331071919.12">@doc
@ascskip # Time-stamp: "Thu, Dec  4 15:28 CST 2003  michael@redpriest _Write_the_outline_tree_as_AsciiDoc_file__141131100.py"

This function opens the output file and walks the tree of outline
nodes under the node that is passed as the first parameter.  At each
node, it calls our workhorse "WriteNode".


@code
def WriteTreeAsAsc(vnode, ascFileN):
    'Writes the tree under vnode to the file ascFile'
    def CleanUp():
        'Cleanup on exit'
        ascFile.close()

    writeNodeReturnValue = None
    startinglevel = vnode.level()
    try:
        ascFile = file(ascFileN,'w')
    except IOError:
        g.es("Could not open output file: %s" % ascFileN)
        return
    stopHere = vnode.nodeAfterTree()
    v = vnode
    while v != stopHere:
        writeNodeReturnValue = WriteNode(v, startinglevel, ascFile)
        if  writeNodeReturnValue == CV.END_PROGRAM:
            CleanUp()
            return
        elif  writeNodeReturnValue == CV.NODE_IGNORE:
            v = v.nodeAfterTree()       # ran into an @ascignore
        else:
            v = v.threadNext()

    CleanUp()
    g.es('Wrote: '+`ascFileN`)





</t>
<t tx="ekr.20040331071919.13">@doc
@ascskip # Time-stamp: "Fri, Jan  9 13:58 CST 2004  michael@redpriest _Write_a_node__140596620.py"

This is the workhorse of the program, exporting the text in a node
to the output file in a way that the AsciiDoc program will
recognize.

The basic activity is:
    - output the node headline as a DocBook section heading (Book,
      Chapter, Section1, Section2, etc.)
    - scan each line of the body text for directives, and take the
      appropriate action.  Regular expressions do the heavy lifting.
    - mark the code sections and documentation sections, so that
      DocBook can print them in the correct styles.
    - ensure that code lines do not exceed a maximum length.



@code
def WriteNode(v,startinglevel, ascFile):

    'Writes the contents of the node v to the ascFile.'

    containsAscIignore = None          # initialize
    skippingDocLines = False
    startingCodeExtract = False
    inCodeExtract = False
    statusOfWriteOutputLine = None

    def WriteOutputLine(lineString):

        'Writes a line of text to the output file.'
        try:
            ascFile.write("%s\n" % lineString)
        except IOError:
            g.es("Could not write to output file: %s" % ascFile.name)
            statusOfWriteOutputLine = CV.END_PROGRAM


    # ----- get the headline text ------------------------------------------
    h = v.headString()
    markedupAsSection = patternSectionName.match(h)
    if markedupAsSection:
        h = markedupAsSection.group(1) # dump the angle brackets

    # ----- put the body text into a list of lines -------------------------
    bodyString = v.bodyString()
    lines = bodyString.splitlines()

    lastLinePrintedType = CV.LINE_WAS_NONE
    # ----- by default, nodes start with a code section --------------------
    pendinglineType = CV.LINE_PENDING_CODE

    for line in lines:
        containsRootDirective = None

@doc

If this line starts a code extract, called a Section Definition
here, then extract the text to use as the title and set the
"startingCodeExtract" flag to guide further processing.

@code
        containsSectionDefinition = patternSectionDefinition.match(line)
        if containsSectionDefinition:
            # dump the angle brackets, etc.
#             line = containsSectionDefinition.group(2)  + '\n' + \
#                    (SectionUnderline(containsSectionDefinition.group(2),2,v))
            line = '.' + containsSectionDefinition.group(2)
            pendinglineType = CV.LINE_PENDING_CODE
            startingCodeExtract = True
@doc

Check if this line starts a @doc or @code section.

@code
        containsCodeDirective = patternCodeDirective.match(line)
        if containsCodeDirective:
            pendinglineType = CV.LINE_PENDING_CODE
            skippingDocLines = False
            continue                    # don't print this line

        containsDocDirective = patternDocDirective.match(line)
        if containsDocDirective:
            pendinglineType = CV.LINE_PENDING_DOC
            if containsDocDirective.group(2):
                # it is legal to have text on the same line
                # as a doc directive.
                line = containsDocDirective.group(2)
            else:
                continue
@doc

Check line for a Leo2AsciiDoc directive, and if so, act on it.

@code
        containsAscDirective = patternAscDirective.match(line)
        if containsAscDirective:
            containsAscIignore = patternAscDirectiveIgnore.match(line)
            if containsAscIignore:
                break

            containsAscExit = patternAscDirectiveExit.match(line)
            if containsAscExit:
                break

            containsAscSkip = patternAscDirectiveSkip.match(line)
            if containsAscSkip:
                containsAscSkipDirectiveToggle = patternAscDirectiveSkipToggle.match(line)
                if containsAscSkipDirectiveToggle:
                    if containsAscSkipDirectiveToggle.group(1).lower() == "on":
                        skippingDocLines = True
                    elif containsAscSkipDirectiveToggle.group(1).lower() == "off":
                        skippingDocLines = False
                continue

        containsOtherDirective = patternDirective.match(line)
        if containsOtherDirective:
            containsRootDirective = patternRootDirective.match(line)
            if containsRootDirective:
                line = "*note*\nThe code sections that follow, when extracted from a " + \
                       "Leo outline, will be located in: %s\n*note*" % \
                       containsRootDirective.group(1)
            else:
                continue

        # ----- we have something to print, so print heading ---------------
        if lastLinePrintedType == CV.LINE_WAS_NONE:
            if (len(h) &gt; 0) and (Conf.current["PrintHeadings"] == "on"):
                WriteOutputLine("\n\n%s" % h)
                WriteOutputLine(SectionUnderline(h,v.level()-startinglevel,v))
                lastLinePrintedType = CV.LINE_WAS_HEAD
@doc

Here we manage the transitions between code and doc sections.

@code
        if pendinglineType == CV.LINE_PENDING_DOC:
            if lastLinePrintedType != CV.LINE_WAS_DOC and \
               lastLinePrintedType != CV.LINE_WAS_HEAD:
                WriteOutputLine("%s" % Conf.current["delimiterForCodeEnd"])
                if inCodeExtract:
                    WriteOutputLine("\n%s" % Conf.current["delimiterForCodeSectionDefinition"])
                    inCodeExtract = False
                lastLinePrintedType = CV.LINE_WAS_DOC
            if skippingDocLines:
                if not containsRootDirective: # always document a root directive
                    continue

        if pendinglineType == CV.LINE_PENDING_CODE:
            if lastLinePrintedType != CV.LINE_WAS_CODE:
                if startingCodeExtract:
                    WriteOutputLine("\n%s" % line)
                    WriteOutputLine("%s" % Conf.current["delimiterForCodeSectionDefinition"])
                    inCodeExtract = True
                    line = ''
                WriteOutputLine("%s" % Conf.current["delimiterForCodeStart"])
                lastLinePrintedType = CV.LINE_WAS_CODE
                if startingCodeExtract:
                    startingCodeExtract = False
                    continue
@doc

Check for maximum code line length.  Finally, output the text to the
export file.

@code
            maxCodeLineLength = int(Conf.current["maxCodeLineLength"])
            if len(line) &lt;= maxCodeLineLength:
                WriteOutputLine("%s" % line)
            elif len(line.rstrip()) &lt;= maxCodeLineLength:
                WriteOutputLine("%s" % line.rstrip())
            else:
                lineList = CodeChunk(line, maxCodeLineLength)
                for ln in lineList:
                    WriteOutputLine("%s" % ln)
            lastLinePrintedType = CV.LINE_WAS_CODE
        else:
            WriteOutputLine("%s" % line)

        if statusOfWriteOutputLine != None:
            return statusOfWriteOutputLine

@doc

Before we leave, make sure that any ending code section is marked as
ended.

@code
    if lastLinePrintedType == CV.LINE_WAS_CODE:
        WriteOutputLine("%s" % Conf.current["delimiterForCodeEnd"])
        if inCodeExtract:
            WriteOutputLine("\n%s" % Conf.current["delimiterForCodeSectionDefinition"])
            inCodeExtract = False

    if containsAscIignore != None:
        return CV.NODE_IGNORE                        # flag ignore tree to caller

@doc

</t>
<t tx="ekr.20040331071919.14">@doc
@ascskip # Time-stamp: "Tue, Jan 13 11:09 CST 2004  michael@redpriest Other_programs_140636444.txt"

The appendices are about other programs that are used with Leo.
I'm including them because they are examples of how my setup works,
for those who may be interested in setting up something similar.

    - AsciiDoc is the program that processes the output from Leo2AsciiDoc
      into a DocBook-ready XML file.
    - Setting up DocBook is a topic that is far too large for this
      little manual, but the DocBook section which follows contains
      documentation of exactly how my working system is configured.
    - The XEmacs text editor is the one I prefer, but it is not
      necessary for the use of Leo2AsciiDoc.  Others who also use XEmacs
      might find the documentation of my Leo integration and
      multi-mode support to be useful.
@code</t>
<t tx="ekr.20040331071919.15">@language plain
@ascskip Time-stamp: "Thu, Oct 30 10:58 CST 2003  michael@redpriest Appendix_AsciiDoc__140954356.txt"
@doc
anchor:AsciiDoc[AsciiDoc]

The AsciiDoc program is written by Stuart Rackham and has its own
web site at http://www.methods.co.nz/asciidoc/[], with full
documentation.

AsciiDoc is a small program, written in Python, that reads text
which is in the AsciiDoc text format. Generally speaking, ordinary
text (such as you would write in an email message) is already in the
AsciiDoc format.  The AsciiDoc program produces (among other
choices) output in the DocBook XML format.

Text exported from a Leo outline by Leo2AsciiDoc is ready to be processed
by AsciiDoc, once AsciiDoc has been configured to recognize it.

Leo2AsciiDoc comes with an AsciiDoc configuration file that will enable
AsciiDoc to process all Leo2AsciiDoc features.  The following section
describes that configuration file.

Of course, you don't need to read or understand the configuration
file to use it.  Simply put it (leo-docbook.conf) in the same
directory as AsciiDoc's "docbook.conf" file.  When you invoke
AsciiDoc (see the xref:Makefile[] section in the DocBook appendix for
examples), give the "leo-docbook.conf" file as the configuration
parameter ("-f leo-docbook.conf".)

@ascskip on
&lt;&lt; Appendix: AsciiDoc &gt;&gt;
@code
</t>
<t tx="ekr.20040331071919.16">@language python
@tabwidth -4

@doc
@ascskip # Time-stamp: "Tue, Jan 13 11:58 CST 2004  michael@redpriest _Configuration_file__140640380.py"

AsciiDoc is customized through the use of configuration files, which
cascade, so that you can include other configuration files and
then proceed to add your changes.

The main elements of the configuration file below:

    - adds chapter and web site document types
    - switches code listings to use the DocBook "programlisting"
      element 

    *note*

    If you choose to export this configuration file from the Leo
    outline, you will have to remove escape charactersfrom some
    lines after you have exported it.

    Specifically, some lines begin with the character "\".  That
    character should be removed.

    *note*

@ascskip on
@root "other/asciidoc/leo-docbook.conf"
&lt;&lt; Configuration File &gt;&gt;
@code
# Start with the standard docbook back end configuration.
# ensure the next line is uncommented before installing
\include::docbook.conf[]

@doc

I want tabs interpreted as 4 spaces.

@code
[options]
tabsize=4
@doc

Interpret an indented paragraph as a simple paragraph.

@code
[indentedparagraph]
&lt;simpara&gt;|&lt;/simpara&gt;


@doc

For our code listings we invent a new markup that will use the
DocBook programlisting element.

@code
[blockdef-leocode]
delimiter=^\~\-~--- code(.*?)$
section=programlistingblock
presubs=specialcharacters, replacements

[programlistingblock]
&lt;programlisting&gt;
|
&lt;/programlisting&gt;

@doc

We add new markup to signify the DocBook "note" element.  This
predates AsciiDoc 5.0, and is still useful.

@code
[blockdef-note]
delimiter=^ *\*note\*$
section=noteblock
presubs=specialcharacters,quotes,specialwords,replacements,macros,glossary

# Block macro
[noteblock]
&lt;note&gt;
|
&lt;/note&gt;

[blockdef-example]
delimiter=^ *\*example\*$
options=section
section=exampleblock
presubs=replacements

# Block macro
[exampleblock]
&lt;example&gt;
&lt;title&gt;{title}&lt;/title&gt;
|
&lt;/example&gt;


@doc

The following replacements ensure basic Python code indexing.

@code
[replacements]
#----- indexing markup -----------------------------------------------------
# using regular expressions because I don't want to introduce a filter, which
# would slow things down.
#
# index python classes and defs
^(def +)(.+?)(\(.+:)=\1\2\3&lt;indexterm&gt;&lt;primary&gt;Python code, functions&lt;/primary&gt;&lt;secondary&gt;\2&lt;/secondary&gt;&lt;/indexterm&gt; 
^(class +)(.+?)(:)=\1\2\3&lt;indexterm&gt;&lt;primary&gt;Python code, classes&lt;/primary&gt;&lt;secondary&gt;\2&lt;/secondary&gt;&lt;/indexterm&gt; 
^( +def +)(.+?)(\(.+:)=\1\2\3&lt;indexterm&gt;&lt;primary&gt;Python code, methods and nested functions&lt;/primary&gt;&lt;secondary&gt;\2&lt;/secondary&gt;&lt;/indexterm&gt; 

# index code extracts
(\&amp;lt\;\&amp;lt\;)(.+?)(\&amp;gt\;\&amp;gt\;\=)=\2&lt;indexterm&gt;&lt;primary&gt;Python code, extracts explained&lt;/primary&gt;&lt;secondary&gt;\2&lt;/secondary&gt;&lt;/indexterm&gt;
(\&amp;lt\;\&amp;lt\;)(.+?)(\&amp;gt\;\&amp;gt\;)(\s*$)=\1\2\3\4&lt;indexterm&gt;&lt;primary&gt;Python code, extracts used&lt;/primary&gt;&lt;secondary&gt;\2&lt;/secondary&gt;&lt;/indexterm&gt; 

@doc

Change the standard AsciiDoc article, book and manpage definition to
use the DocBook 4.2 DTD.  Add an empty index element to the end of
the book definition so that DocBook will automatically generate an
index.

@code
#---------------------------------------------------------------------------
#----- article -------------------------------------------------------------
#---------------------------------------------------------------------------

# changing to our version of the docbook dtd
\ifdef::doctype-article[]

[header]
&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;!DOCTYPE article
        PUBLIC "-//OASIS//DTD DocBook XML V4.2//EN"
        "http://www.oasis-open.org/docbook/xml/4.0/docbookx.dtd"&gt;

&lt;article lang="en"&gt;
&lt;articleinfo&gt;
    &lt;title&gt;{doctitle}&lt;/title&gt;
    &lt;date&gt;{date}&lt;/date&gt;
    &lt;author&gt;
        &lt;firstname&gt;{firstname}&lt;/firstname&gt;
        &lt;othername&gt;{middlename}&lt;/othername&gt;
        &lt;surname&gt;{lastname}&lt;/surname&gt;
        &lt;affiliation&gt;
            &lt;address&gt;
                &lt;email&gt;{email}&lt;/email&gt;
            &lt;/address&gt;
        &lt;/affiliation&gt;
    &lt;/author&gt;
    &lt;authorinitials&gt;{authorinitials}&lt;/authorinitials&gt;
    &lt;revhistory&gt;&lt;revision&gt;&lt;revnumber&gt;{revision}&lt;/revnumber&gt;&lt;date&gt;{date}&lt;/date&gt;&lt;/revision&gt;&lt;/revhistory&gt;
    &lt;corpname&gt;{companyname}&lt;/corpname&gt;
&lt;/articleinfo&gt;

\endif::doctype-article[]


#---------------------------------------------------------------------------
#----- book ----------------------------------------------------------------
#---------------------------------------------------------------------------
# change to our version of docbook dtd

\ifdef::doctype-book[]

[header]
&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;!DOCTYPE book
        PUBLIC "-//OASIS//DTD DocBook XML V4.2//EN"
        "http://www.oasis-open.org/docbook/xml/4.0/docbookx.dtd"&gt;

&lt;book lang="en"&gt;
&lt;bookinfo&gt;
    &lt;title&gt;{doctitle}&lt;/title&gt;
    &lt;date&gt;{date}&lt;/date&gt;
    &lt;author&gt;
        &lt;firstname&gt;{firstname}&lt;/firstname&gt;
        &lt;othername&gt;{middlename}&lt;/othername&gt;
        &lt;surname&gt;{lastname}&lt;/surname&gt;
        &lt;affiliation&gt;
            &lt;address&gt;
                &lt;email&gt;{email}&lt;/email&gt;
            &lt;/address&gt;
        &lt;/affiliation&gt;
    &lt;/author&gt;
    &lt;authorinitials&gt;{authorinitials}&lt;/authorinitials&gt;
    &lt;revhistory&gt;&lt;revision&gt;&lt;revnumber&gt;{revision}&lt;/revnumber&gt;&lt;date&gt;{date}&lt;/date&gt;&lt;/revision&gt;&lt;/revhistory&gt;
    &lt;corpname&gt;{companyname}&lt;/corpname&gt;
&lt;/bookinfo&gt;


[footer]
&lt;index/&gt;
&lt;/book&gt;

\endif::doctype-book[]

#---------------------------------------------------------------------------
#----- manpage -------------------------------------------------------------
#---------------------------------------------------------------------------
\ifdef::doctype-manpage[]

[header]
&lt;!DOCTYPE refentry
        PUBLIC "-//OASIS//DTD DocBook XML V4.2//EN"
        "http://www.oasis-open.org/docbook/xml/4.0/docbookx.dtd"&gt;
&lt;refentry&gt;
# The refentryinfo element is legal and should not normally be printed.
# Unfortunately some docbook processors do print it.
&lt;refentryinfo&gt;
    &lt;title&gt;{doctitle}&lt;/title&gt;
    &lt;date&gt;{date}&lt;/date&gt;
    &lt;author&gt;
        &lt;firstname&gt;{firstname}&lt;/firstname&gt;
        &lt;othername&gt;{middlename}&lt;/othername&gt;
        &lt;surname&gt;{lastname}&lt;/surname&gt;
        &lt;affiliation&gt;
            &lt;address&gt;
                &lt;email&gt;{email}&lt;/email&gt;
            &lt;/address&gt;
        &lt;/affiliation&gt;
    &lt;/author&gt;
    &lt;authorinitials&gt;{authorinitials}&lt;/authorinitials&gt;
    &lt;revhistory&gt;&lt;revision&gt;&lt;revnumber&gt;{revision}&lt;/revnumber&gt;&lt;date&gt;{date}&lt;/date&gt;&lt;/revision&gt;&lt;/revhistory&gt;
    &lt;corpname&gt;{companyname}&lt;/corpname&gt;
&lt;/refentryinfo&gt;
&lt;refmeta&gt;
&lt;refentrytitle&gt;{mantitle}&lt;/refentrytitle&gt;
&lt;manvolnum&gt;{manvolnum}&lt;/manvolnum&gt;
&lt;/refmeta&gt;
&lt;refnamediv&gt;
    &lt;refname&gt;{manname}&lt;/refname&gt;
    &lt;refpurpose&gt;{manpurpose}&lt;/refpurpose&gt;
&lt;/refnamediv&gt;

\endif::doctype-manpage[]



@doc

Add chapter and website document types.

@code
#---------------------------------------------------------------------------
#----- new: chapter --------------------------------------------------------
#---------------------------------------------------------------------------
\ifdef::doctype-chapter[]

[header]
&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;!DOCTYPE chapter
        PUBLIC "-//OASIS//DTD DocBook XML V4.2//EN"
        "http://www.oasis-open.org/docbook/xml/4.0/docbookx.dtd"&gt;
&lt;chapter&gt;
&lt;title&gt;{doctitle}&lt;/title&gt;

[footer]
&lt;/chapter&gt;


# Section macros
# Using &lt;abstract&gt; semantics restricts preface to &lt;simpara&gt; elements.
[preface]
|

[sect1]
&lt;sect1&gt;
&lt;title&gt;{title}&lt;/title&gt;
|
&lt;/sect1&gt;

[sect2]
&lt;sect2&gt;
&lt;title&gt;{title}&lt;/title&gt;
|
&lt;/sect2&gt;

[sect3]
&lt;sect3&gt;
&lt;title&gt;{title}&lt;/title&gt;
|
&lt;/sect3&gt;

[options]
outfilesuffix=.xml

\endif::doctype-chapter[]

@doc

Website requires a unique id for each page.  I've changed AsciiDoc
to provide the HTML filename as the id, and we use it here. We'll
use the date the XML file was created as the update date.

@code
#---------------------------------------------------------------------------
#----- new: website --------------------------------------------------------
#---------------------------------------------------------------------------
\ifdef::doctype-website[]
[header]
&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;!DOCTYPE webpage SYSTEM "website-full.dtd"&gt;
&lt;webpage id="{infilebase}"&gt;
  &lt;head&gt;
    &lt;title&gt;{doctitle}&lt;/title&gt;
  &lt;/head&gt;
  &lt;config param="rcsdate" value="Updated: {localdate}  {localtime}"/&gt;
[footer]
&lt;/webpage&gt;

[options]
outfilesuffix=.xml

\endif::doctype-website[]

</t>
<t tx="ekr.20040331071919.17">@silent
@doc
@ascskip # Time-stamp: "Tue, Jan 13 14:11 CST 2004  michael@redpriest _Patches__140641532.txt"

I've patched the source code for AsciiDoc (asciidoc.py) with a few
small changes to allow AsciiDoc to process chapters and DocBook
web site documents as well as the DocBook book format.  Since I use
Linux, I also changed the default line-ending code to the Linux
default.

For the exact changes I made, the following output at the end of
this section was created by GNU diff (version 2.8.4) with the
command

---
LC_ALL=C TZ=UTC0 diff -Naur 5.0.2-original 5.0.2-mrc-patched \
    &gt;mrc-asciidoc-5.0.2-patch-diff
---

I include this mainly so that you can see the exact changes I made.
However, you may want to patch a copy of the original in exactly the
same way. 

To patch a copy of the original asciidoc.py (version 5.0.2), one
would use the patch command as follows (when in the same directory
as the copy of asciidoc.py and mrc-asciidoc-5.0.2-patch-diff)

---
patch -Np1 &lt;mrc2-asciidoc-5.0.2-patch-diff
---

@ascskip on
@root "other/asciidoc/mrc-asciidoc-5.0.2-patch-diff"
&lt;&lt; Patches &gt;&gt;
@code
diff -Naur 5.0.2-original/asciidoc.py 5.0.2-mrc-patched/asciidoc.py
--- 5.0.2-original/asciidoc.py	2003-12-16 00:16:28.000000000 +0000
+++ 5.0.2-mrc-patched/asciidoc.py	2004-01-08 17:45:37.000000000 +0000
@@ -838,12 +838,15 @@
         '''Set predefined glossary entries that follow configuration file
         loading.'''
         self.glossary['infile'] = reader.fname
+        # mwd Monday, June 23, 2003 for use in website
+        self.glossary['infilebase'] = os.path.splitext(os.path.split(reader.fname)[1]) [0]
         self.glossary['outfile'] = reader.fname
         s = os.path.splitext(writer.fname)[1][1:]   # Output file extension.
         self.glossary['filetype'] = s
         self.glossary['filetype-'+s] = ''
     def translate(self):
-        assert self.doctype in ('article','manpage','book'), \
+        # mwd 2003-Jun-23 assert self.doctype in ('article','manpage','book'), \
+        assert self.doctype in ('article','chapter','website','manpage', 'book'), \
             'illegal document type'
         assert self.level == 0
         reader.tabsize = config.tabsize
@@ -864,7 +867,8 @@
             if not config.suppress_headers:
                 hdr = config.subs_section('header',{})
                 writer.write(hdr)
-            if self.doctype in ('article','book'):
+            # mwd 2003-Jun-23 if self.doctype in ('article','book'):
+            if self.doctype in ('article','book','chapter','website'):
                 # Translate 'preamble' (untitled elements between header
                 # and first section title).
                 if Lex.next() is not Title:
@@ -952,7 +956,7 @@
                 # Parse revision line.
                 s = reader.read()
                 s = subs_glossary([s])[0]
-                # Match RCS/CVS $Id$ marker format.
+                # Match RCS/CVS $Id$ marker format.
                 mo = re.match(r'^\$Id: \S+ (?P&lt;revision&gt;\S+)' \
                     ' (?P&lt;date&gt;\S+) \S+ \S+ \S+ \$$',s)
                 if not mo:
@@ -2573,7 +2577,8 @@
 
 class Writer:
     '''Writes lines to output file.'''
-    EOL = '\r\n'    # End of line terminator.
+    # mwd 2003-Jun-23 EOL = '\r\n'    # End of line terminator.
+    EOL = '\n'    # End of line terminator.
     f = None        # Output file object.
     fname= None     # Output file name.
     lines_out = 0   # Number of lines written.
@@ -3068,7 +3073,8 @@
     The AsciiDoc document is read from file object src the translated
     DocBook file written to file object dst.'''
     try:
-        if doctype not in ('article','manpage','book'):
+        # mwd-2004-Jan-05 if doctype not in ('article','manpage','book'):
+        if doctype not in ('article','chapter','website','manpage', 'book'):
             raise EAsciiDoc,'illegal document type'
         if backend == 'linuxdoc' and doctype != 'article':
             raise EAsciiDoc,'%s %s documents are not supported' \
</t>
<t tx="ekr.20040331071919.18">@language plain
@ascskip Time-stamp: "Fri, Dec 19 11:48 CST 2003  michael@redpriest Appendix_DocBook_140578660.txt"
@doc

anchor:DocBook[DocBook]
DocBook is a project that provides:

    - a specification for the text markup (DTD) of DocBook XML
      documents, and
    - a set of XSLT stylesheets that can be used by an XSLT engine
      to transform those XML documents to HTML, PDF, etc.
      
If you create your text documents using the rules in the DocBook
DTD, you can use the DocBook XSLT stylesheets to produce various
output formats, such as HTML and PDF.

The DocBook project is designed for the production of computer
documentation, but is actually used for a wide variety of documents.

Some web resources:

    - the official home page for DocBook: The Definitive Guide:
        http://docbook.org/[]
    - DocBook Basics:
        http://www.dpawson.co.uk/docbook/reference.html[]
    - DocBook Open Repository:
        http://sourceforge.net/projects/docbook/[]
    - DocBook XSL: The Complete Guide:
        http://www.sagehill.net/docbookxsl/index.html[]

I include this section as documentation of one setup that works --
it translates Leo2AsciiDoc output to HTML and PDF.

This is not a guide to the installation, setup and operation of
DocBook, just an example of a working system.

@ascskip on
&lt;&lt; Appendix: DocBook &gt;&gt;
@code
</t>
<t tx="ekr.20040331071919.19">@doc
@ascskip # Time-stamp: "Thu, Jan  8 13:57 CST 2004  michael@redpriest _Tool_Chain__140810780.txt"

Documents go through a number of stages in their creation.  Each
stage may involve one or more tools or programs, which form a tool
chain: each performing some processing and handing off to the next.

As a simple example, for this document:


    - text creation was handled by XEmacs, a text
      editor (which functioned as a Leo plugin.)
      indexterm:[XEmacs]
      indexterm:[GNU Make]
      indexterm:[AsciiDoc]
      indexterm:[xsltproc]
      indexterm:[FOP]
    - text storage and organization was handled by Leo, an outlining
      editor.
    - text was exported from Leo to a plain-text file, using the
      Leo2AsciiDoc program.
    - from there, all transformations are automated by the
      GNU Make program.
    - the DocBook XML document was created by the
      AsciiDoc program, which transformed the
      plain-text file to XML.
    - The HTML pages were created by the
      xsltproc program. xsltproc read the XML
      document, and the DocBook XSLT stylesheets, and then created
      each HTML page.
    - To make the PDF file, the xsltproc program used the same
      process as for the HTML pages, except that it created a
      Formatting Objects (FO) file instead.  Then the
      FOP program processed the FO file, producing
      the final PDF file.  This process was also automated.

All I did was type in text for each section, arranging it much as I
usually do for email.  The rest was handled automatically by
clicking on a Leo menu, or entering a short command at the console.
For example: "make all".

There are many, many choices of tools to put in your DocBook tool
chain.  You can even purchase complete packages, from text editing
to PDF generation.

@code</t>
<t tx="ekr.20040331071919.20">@language plain
@tabwidth 4
@doc
@ascskip # Time-stamp: "Thu, Jan 15 15:39 CST 2004  michael@redpriest _Make_File__140651828.txt"

anchor:Makefile[Makefile]
In my case, I use a standard unix-style "make" setup for processing
the text exported from a Leo outline.  It simply automates the
commands which I would otherwise have to type at the command line.

After Leo2AsciiDoc exports the text from the Leo outline to a disk file,
the Make program takes over.  It reads rules in a file named
"Makefile" and calls the necessary programs to make the
requested output.

This Makefile takes over where Leo2AsciiDoc leaves off.  It directs the
AsciiDoc conversion of the Leo2AsciiDoc text file to XML, and then the
DocBook conversion of the XML file to HTML pages or a PDF document.

indexterm:[GNU Make]
I use GNU Make.  For example, assuming I am in xterm and located in
the same directory as the Makefile, I just enter the command

---
make pdf-dev
---
and the make program guides the creation of the PDF version of The
Developers Guide, using the instructions in this Makefile.  The PDF
is available within seconds.

The Makefile instructions, in brief:

    - the AsciiDoc program is called to make an XML file.
    - the xsltproc program is called to process the XML file to
      either HTML or a Formatting Objects file for further
      translation to PDF
        * various XSLT style sheets (html.xsl, man.xsl, etc.) are
          used by xsltproc to guide the transformation of the XML
          file.  Typically, they call the DocBook stylesheets for
          the heavy lifting, and set a few simple options.
    - the FOP program is used to process the intermediate fo file to
      the final PDF file.

This is by no means a model Makefile.  It is included because it
works for me in my office, and may thus be useful as an example for
other people who want to set up Make for this purpose.

@ascskip xemacs-makefile-mode-on
@ascskip on
@root "doc/Makefile"
&lt;&lt; Make File &gt;&gt;
@code
#----- global variables -----------------------------------------
DEVGUIDE=mod_asc_dev
USERGUIDE=mod_asc_user
CSS=dbstyle.css

MAN=${DOC}.1
STYLESHEET_MAN=man.xsl
# default docbook, located by /etc/xml/catalog
STYLESHEET_MAN_HTML=docbook.xsl
MAN_OUTPUT_DIR=man

STYLESHEET_HTML=html.xsl
HTML_DEV_OUTPUT_DIR=html-dev
HTML_USER_OUTPUT_DIR=html-user
STYLESHEET_CHUNK=chunkit.xsl
CHUNK_DEV_OUTPUT_DIR=chunk-dev
CHUNK_USER_OUTPUT_DIR=chunk-user

STYLESHEET_FO_FOP=fo-fop.xsl
PDF_DEV_OUTPUT_DIR=pdf-dev
PDF_USER_OUTPUT_DIR=pdf-user

ASCIIDOC_COMMAND=python asciidoc/asciidoc.py -v -b docbook -d book
ASCIIDOC_CONFIG=asciidoc/leo-docbook.conf

#   $@ target file name
#   $&lt; name of the first prerequisite
#   $* stem that rule matched

#----- pattern rules -------------------------------------------------------
%.xml	:	%.asc
#	asciidoc -b docbook -d book -f ${ASCIIDOC_CONFIG} -o $@ $&lt;
    ${ASCIIDOC_COMMAND}  -f ${ASCIIDOC_CONFIG} -o $@ $&lt;
    xsltproc --output $*.final.xml customize.xsl $@


%.html	:	%.xml css
    xsltproc --xinclude --output ${OUTPUT} ${STYLESHEET}  $*.final.xml
    touch $*.xml

%.pdf	:	%.xml
    xsltproc --xinclude  --output ${OUTPUT}/$*.fo $(STYLESHEET) $*.final.xml
    fop -fo  ${OUTPUT}/$*.fo  -pdf ${OUTPUT}/$*.pdf 
    -$(RM) ${OUTPUT}/$*.fo

#----- usage ---------------------------------------------------------------
usage	:
    @echo; echo "primary make modules: html-dev chunk-dev pdf-dev"
    @echo       "                      html-user chunk-user pdf-user"
    @echo



#---------------------------------------------------------------------------
#----- modules -------------------------------------------------------------
#---------------------------------------------------------------------------

# docbook
#---------------------------------------------------------------------------

all	:	css pdf-dev html-dev sub-chunk-dev html-user sub-chunk-user pdf-user

#----- DocBook html stylesheet ---------------------------------------------
css:
    cat base.css   &gt;  $(CSS)
    cat docstyle.css &gt;&gt; $(CSS)

#----- Developers Guide ----------------------------------------------------
#   #----- one page -----------------------------------------------------
html-dev	:	STYLESHEET=$(STYLESHEET_HTML)
html-dev	:	OUTPUT=${HTML_DEV_OUTPUT_DIR}/$*.html
html-dev	:	mkdirhtmldev ${DEVGUIDE}.html
    cp ${CSS} ${HTML_DEV_OUTPUT_DIR}

mkdirhtmldev	:	cleanhtmldev
    mkdir ${HTML_DEV_OUTPUT_DIR}

#   #----- individual pages ------------------------------------------------
chunk-dev	:	STYLESHEET=$(STYLESHEET_CHUNK)
chunk-dev	:	OUTPUT=$(CHUNK_DEV_OUTPUT_DIR)/
chunk-dev	:	mkdirchunkdev ${DEVGUIDE}.html
    cp chunk-dev-frame*.html ${CHUNK_DEV_OUTPUT_DIR}
    cp ${CSS} ${CHUNK_DEV_OUTPUT_DIR}
    cp frametoc.css ${CHUNK_DEV_OUTPUT_DIR}
    cp -r ../graphics ${CHUNK_DEV_OUTPUT_DIR}
# put in frame target line
    sed -f sed-dev-frame ${CHUNK_DEV_OUTPUT_DIR}/index.html &gt;${CHUNK_DEV_OUTPUT_DIR}/chunk-dev-frame-toc.html

mkdirchunkdev	:	cleanchunkdev
    mkdir ${CHUNK_DEV_OUTPUT_DIR}

sub-chunk-dev	:
    ${MAKE} chunk-dev

#----- Users Guide ---------------------------------------------------------
#   #----- one page -----------------------------------------------------
html-user	:	STYLESHEET=$(STYLESHEET_HTML)
html-user:	OUTPUT=${HTML_USER_OUTPUT_DIR}/$*.html
html-user:	mkdirhtmluser ${USERGUIDE}.html
    cp ${CSS} ${HTML_USER_OUTPUT_DIR}

mkdirhtmluser	:	cleanhtmluser
    mkdir ${HTML_USER_OUTPUT_DIR}

#   #----- individual pages ------------------------------------------------
chunk-user	:	STYLESHEET=$(STYLESHEET_CHUNK)
chunk-user	:	OUTPUT=$(CHUNK_USER_OUTPUT_DIR)/
chunk-user	:	cleanchunkuser ${USERGUIDE}.html
    cp chunk-user-frame*.html ${CHUNK_USER_OUTPUT_DIR}
    cp ${CSS} ${CHUNK_USER_OUTPUT_DIR}
    cp frametoc.css ${CHUNK_USER_OUTPUT_DIR}
    cp -r ../graphics ${CHUNK_USER_OUTPUT_DIR}
# put in frame target line
    sed -f sed-user-frame ${CHUNK_USER_OUTPUT_DIR}/index.html &gt;${CHUNK_USER_OUTPUT_DIR}/chunk-user-frame-toc.html

mkdirchunkuser	:	cleanchunkuser
    mkdir ${CHUNK_USER_OUTPUT_DIR}

sub-chunk-user	:
    ${MAKE} chunk-user

#   #----- pdf -------------------------------------------------------------
pdf-dev		:	STYLESHEET=$(STYLESHEET_FO_FOP)
pdf-dev		:	OUTPUT=$(PDF_DEV_OUTPUT_DIR)
pdf-dev		:	mkdirpdf ${DEVGUIDE}.pdf

pdf-user		:	STYLESHEET=$(STYLESHEET_FO_FOP)
pdf-user		:	OUTPUT=$(PDF_USER_OUTPUT_DIR)
pdf-user		:	mkdirpdf ${USERGUIDE}.pdf

#   mkdirpdf exists only to make an empty directory for the pdf working files
mkdirpdf	:
    -mkdir $(PDF_DEV_OUTPUT_DIR)
    -mkdir $(PDF_USER_OUTPUT_DIR)




#----- clean ---------------------------------------------------------------
clean	: cleanhtml cleanchunk cleanpdf cleanman cleanclutter 

cleanhtml	:	cleanhtmluser cleanhtmldev

cleanhtmluser	:
    -$(RM) -r $(HTML_USER_OUTPUT_DIR)

cleanhtmldev	:
    -$(RM) -r $(HTML_DEV_OUTPUT_DIR)

cleanchunk	:	cleanchunkuser cleanchunkdev

cleanchunkuser	:
    -$(RM) -r $(CHUNK_USER_OUTPUT_DIR)

cleanchunkdev	:
    -$(RM) -r $(CHUNK_DEV_OUTPUT_DIR)

cleanpdf	:
    -$(RM) -r $(PDF_OUTPUT_DIR)

cleanman	:
    -$(RM) -r $(MAN_OUTPUT_DIR)

cleanclutter: 
    -$(RM) -r *.xml

.PRECIOUS	:	%.xml
@doc
@ascskip xemacs-makefile-mode-off
@code
</t>
<t tx="ekr.20040331071919.21">@silent
@doc
@ascskip # Time-stamp: "Wed, Oct  1 15:33 CST 2003  michael@redpriest _Style_Sheets__140741140.txt"

When the Makefile calls the xsltproc program, it gives it the name
of an XSLT stylesheet to guide the production of the result.

Following are simple XSLT stylesheets that are used to:
    - set formatting options, and
    - call the main DocBook XSLT stylesheets.

The stylesheets cascade (each adding its options to the total), with
the original stylesheet including others as needed, and always
calling the main DocBook stylesheets at some point.

@code
</t>
<t tx="ekr.20040331071919.22">@comment &lt;!-- --&gt;
@silent
@doc
@ascskip # Time-stamp: "Thu, Jan  8 14:01 CST 2004  michael@redpriest _General__139758588.txt"

indexterm:[Stylesheets, common-links.xsl]
This is the entire common-links style sheet ("common-links.xsl"),
which sets basic Table of Contents and chapter cross-reference
preferences.

This stylesheet is called by both HTML and PDF stylesheets.

@ascskip on
@ascskip xemacs-xsl-mode-on
@root "doc/common-links.xsl"
&lt;&lt; General &gt;&gt;
@code
&lt;?xml version='1.0'?&gt; 
&lt;xsl:stylesheet  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  version="1.0"&gt; 

&lt;!--===== 
    This changes a chapter cross-reference to include the chapter
    title text. 
--&gt;
&lt;xsl:param name="local.l10n.xml" select="document('')"/&gt; 
&lt;l:i18n xmlns:l="http://docbook.sourceforge.net/xmlns/l10n/1.0"&gt; 
  &lt;l:l10n language="en"&gt; 
    &lt;l:context name="xref"&gt; 
      &lt;l:template name="chapter" text="Chapter %n: &amp;#8220;%t&amp;#8221;"/&gt; 
    &lt;/l:context&gt;   
  &lt;/l:l10n&gt;
&lt;/l:i18n&gt;

&lt;xsl:param name="generate.toc"&gt;
book      toc,title,figure,table,example,equation
chapter   title
&lt;/xsl:param&gt;

&lt;!-- only 1 toc in the doc --&gt;
&lt;xsl:param name="generate.section.toc.level" select="1"/&gt;

&lt;!-- toc shows 3 levels of sections --&gt;
&lt;xsl:param name="toc.section.depth"&gt;3&lt;/xsl:param&gt;

&lt;xsl:param name="generate.index" select="1"&gt;&lt;/xsl:param&gt;

&lt;!--===== omit the title for notes, tips ================================--&gt;
&lt;xsl:param name="admon.textlabel" select="0"&gt;&lt;/xsl:param&gt;

&lt;/xsl:stylesheet&gt;
@doc
@ascskip xemacs-xsl-mode-off


</t>
<t tx="ekr.20040331071919.23">@comment &lt;!-- --&gt;
@silent
@doc
@ascskip # Time-stamp: "Tue, Jan 20 11:42 CST 2004  michael@redpriest _Customize__141637044.txt"


indexterm:[customize.xsl]
This is the entire customize style sheet ("customize.xsl", which is
used by the Makefile to make changes to the standard xml file
produced from the AsciiDoc output.  It results in a file suffixed
".final.xml" which is used by both the HTML and PDF stylesheets.

Currently, the stylesheet copies the xml file:

    - changing any chapter elements that have a title beginning
      with "Appendix: " to DocBook appendix elements.  This is from
      AsciiDoc 3.2 days, when AsciiDoc didn't know about appendix
      elements. I haven't yet modified Leo2AsciiDoc to take
      advantage of the automatic appendix elements in AsciiDoc 5.0.
    - adding custom bookinfo elements

I've used XSLT for this, but it could have been done with python,
AWK, sed, or other tools.

@ascskip on
@ascskip xemacs-xsl-mode-on
@root "doc/customize.xsl"
&lt;&lt; Customize &gt;&gt;
@code
&lt;?xml version="1.0" encoding="utf-8"?&gt;
&lt;xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
                version="1.0"&gt;

&lt;xsl:variable name="AppendBegin"&gt;Appendix: &lt;/xsl:variable&gt;

&lt;!--~~~~~~ copy everything ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~--&gt;
&lt;xsl:template match="@*|node()"&gt;
   &lt;xsl:copy&gt;
      &lt;xsl:apply-templates select="@*|node()"/&gt;
   &lt;/xsl:copy&gt;
&lt;/xsl:template&gt;

&lt;!--~~~~~~ delete the appendix string from the title ~~~~~~~~~~~~~~~~~~~~--&gt;
&lt;xsl:template match="/book/chapter/title[starts-with(text(),$AppendBegin)]"&gt;
  &lt;title&gt;
  &lt;xsl:value-of select="substring-after(text(),$AppendBegin)"/&gt;
  &lt;/title&gt;
  &lt;xsl:apply-templates select="*" /&gt; 
&lt;/xsl:template&gt;

&lt;!--~~~~~~ change appendix chapter element to appendix element ~~~~~~~~~~--&gt;
&lt;xsl:template match="/book/chapter[starts-with(title,$AppendBegin)]"&gt;
  &lt;appendix&gt;
    &lt;xsl:apply-templates select="*" /&gt; 
  &lt;/appendix&gt;
&lt;/xsl:template&gt;

&lt;!--~~~~~~ bookinfo ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~--&gt;
&lt;!--
From Leo2AsciiDoc, only the bookinfo title is filled in, with a
blank author.  Here, we replace the author element with any and all
bookinfo elements we please.
--&gt;
  
&lt;xsl:template match="/book/bookinfo/author"&gt;
  &lt;author&gt;
    &lt;firstname&gt;Michael&lt;/firstname&gt;&lt;surname&gt;Dawson&lt;/surname&gt;
    &lt;affiliation&gt;
      &lt;address&gt;
        &lt;otheraddr&gt;
          &lt;ulink url="http://www.marshallresearch.com/contact.html"&gt;
            at Marshall Research
          &lt;/ulink&gt;
        &lt;/otheraddr&gt;
      &lt;/address&gt;
    &lt;/affiliation&gt;
  &lt;/author&gt;
  &lt;revhistory&gt;
    &lt;revision&gt;
      &lt;revnumber&gt;0.4a&lt;/revnumber&gt;
      &lt;date&gt;Jan 21 2004&lt;/date&gt;
      &lt;authorinitials&gt;mwd&lt;/authorinitials&gt;
      &lt;revremark&gt;Formatting enhancements&lt;/revremark&gt;
    &lt;/revision&gt;
    &lt;revision&gt;
      &lt;revnumber&gt;0.4&lt;/revnumber&gt;
      &lt;date&gt;Jan 19 2004&lt;/date&gt;
      &lt;authorinitials&gt;mwd&lt;/authorinitials&gt;
      &lt;revremark&gt;First release&lt;/revremark&gt;
    &lt;/revision&gt;
  &lt;/revhistory&gt;
&lt;/xsl:template&gt;


&lt;/xsl:stylesheet&gt;

@doc
@ascskip xemacs-xsl-mode-off

</t>
<t tx="ekr.20040331071919.24">@silent
@doc
@ascskip # Time-stamp: "Thu, Jan  8 14:02 CST 2004  michael@redpriest _HTML_One_File__139289780.txt"

indexterm:[Stylesheets,html.xsl]
For one long page of HTML, we simply import the DocBook stylesheets
and our small custom stylesheets that set our standard options.
This is the "html.xsl" stylesheet.

@ascskip on
@ascskip xemacs-xsl-mode-on
@root "doc/html.xsl"
&lt;&lt; HTML: One File &gt;&gt;
@code
&lt;?xml version='1.0'?&gt; 
&lt;xsl:stylesheet  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  version="1.0"&gt; 

&lt;!--===== the catalog (/etx/xml/catalog) will convert this to the local pathname --&gt;
&lt;xsl:import href="docbook.xsl"/&gt;

&lt;xsl:import href="common-links.xsl"/&gt;
&lt;xsl:import href="common-html.xsl"/&gt;

&lt;/xsl:stylesheet&gt; 
@doc
@ascskip xemacs-xsl-mode-off


</t>
<t tx="ekr.20040331071919.25">@silent
@doc
@ascskip # Time-stamp: "Thu, Jan  8 14:40 CST 2004  michael@redpriest _HTML_Individual_Pages__141001292.txt"

For individual section pages of HTML, we import the DocBook stylesheets
and our small custom stylesheets that set our standard options.

Then we set our chunking options, and tell the web pages where to
find the header and footer graphics.

indexterm:[Stylesheets,chunkit.xsl]
The following code is the entire chunkit style sheet
("chunkit.xsl").

@ascskip on
@ascskip xemacs-xsl-mode-on
@root "doc/chunkit.xsl"
&lt;&lt; HTML: Individual Pages &gt;&gt;
@code
&lt;?xml version='1.0'?&gt; 
&lt;xsl:stylesheet  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  version="1.0"&gt; 

&lt;xsl:import href="chunk.xsl"/&gt;

&lt;xsl:import href="common-links.xsl"/&gt;
&lt;xsl:import href="common-html.xsl"/&gt;

&lt;xsl:param name="navig.graphics" select="1"/&gt;
&lt;xsl:param name=
  "navig.graphics.path"&gt;graphics/&lt;/xsl:param&gt;
    &lt;!--  "navig.graphics.path"&gt;/usr/share/xml/docbook/docbook-xsl-1.59.1/images/&lt;/xsl:param&gt;--&gt;
    &lt;!--&lt;xsl:param name="navig.graphics.path"&gt;graphics/dbook/navicons/&lt;/xsl:param&gt;--&gt;
&lt;xsl:param name="navig.graphics.extension"&gt;.png&lt;/xsl:param&gt;
&lt;xsl:param name="navig.showtitles"&gt;1&lt;/xsl:param&gt;

&lt;xsl:param name="chunk.first.sections" select="1"&gt;&lt;/xsl:param&gt;
&lt;xsl:param name="chunk.section.depth" select="2"&gt;&lt;/xsl:param&gt;
&lt;xsl:param name="section.autolabel" select="0"&gt;&lt;/xsl:param&gt;

&lt;xsl:param name="css.decoration"&gt;1&lt;/xsl:param&gt;

&lt;/xsl:stylesheet&gt;

@doc
@ascskip xemacs-xsl-mode-off
</t>
<t tx="ekr.20040331071919.26">@silent
@doc
@ascskip # Time-stamp: "Thu, Jan  8 14:58 CST 2004  michael@redpriest _HTML_base_css_style_sheet__141160708.txt"

css style sheet

@ascskip on
@ascskip xemacs-css-mode-on
@root "doc/base.css"
&lt;&lt; HTML: base css style sheet &gt;&gt;
@code
/* base from http://www.w3.org/TR/CSS21/sample.html */

address,
blockquote,
body, dd, div,
dl, dt, fieldset, form,
frame, frameset,
h1, h2, h3, h4,
h5, h6, noframes,
ol, p, ul, center,
dir, hr, menu, pre   { display: block }
li              { display: list-item }
head            { display: none }
table           { display: table }
tr              { display: table-row }
thead           { display: table-header-group }
tbody           { display: table-row-group }
tfoot           { display: table-footer-group }
col             { display: table-column }
colgroup        { display: table-column-group }
td, th          { display: table-cell; }
caption         { display: table-caption }
th              { font-weight: bolder; text-align: center }
caption         { text-align: center }
body            { padding: 8px; line-height: 1.12em }
h1              { font-size: 2em; margin: .67em 0 }
h2              { font-size: 1.5em; margin: .75em 0 }
h3              { font-size: 1.17em; margin: .83em 0 }
h4, p,
blockquote, ul,
fieldset, form,
ol, dl, dir,
menu            { margin: 1.12em 0 }
h5              { font-size: .83em; margin: 1.5em 0 }
h6              { font-size: .75em; margin: 1.67em 0 }
h1, h2, h3, h4,
h5, h6, b,
strong          { font-weight: bolder }
blockquote      { margin-left: 40px; margin-right: 40px }
i, cite, em,
var, address    { font-style: italic }
pre, tt, code,
kbd, samp       { font-family: monospace }
pre             { white-space: pre }

/            * comment             */
/* http://www.w3.org/TR/CSS21/visuren.html#propdef-display lists inline-block */
button, textarea,
input, object, 
select, img { display:inline-block; }

big             { font-size: 1.17em }
small, sub, sup { font-size: .83em }
sub             { vertical-align: sub }
sup             { vertical-align: super }
s, strike, del  { text-decoration: line-through }
hr              { border: 1px inset }
ol, ul, dir,
menu, dd        { margin-left: 40px }
ol              { list-style-type: decimal }
ol ul, ul ol,
ul ul, ol ol    { margin-top: 0; margin-bottom: 0 }
u, ins          { text-decoration: underline }
/*br:before       { content: "\A" }*/
center          { text-align: center }

/            * changed             */
/*
abbr, acronym   { font-variant: small-caps; letter-spacing: 0.1em }
*/

:link, :visited { text-decoration: underline }
:focus          { outline: thin dotted invert }

/* Begin bidirectionality settings (do not change) */
BDO[DIR="ltr"]  { direction: ltr; unicode-bidi: bidi-override }
BDO[DIR="rtl"]  { direction: rtl; unicode-bidi: bidi-override }

*[DIR="ltr"]    { direction: ltr; unicode-bidi: embed }
*[DIR="rtl"]    { direction: rtl; unicode-bidi: embed }

@media print {
  h1            { page-break-before: always }
  h1, h2, h3,
  h4, h5, h6    { page-break-after: avoid }
  ul, ol, dl    { page-break-before: avoid }
}



@doc
@ascskip xemacs-css-mode-off
</t>
<t tx="ekr.20040331071919.27">@silent
@doc
@ascskip # Time-stamp: "Wed, Jan 21 09:13 CST 2004  michael@redpriest _HTML_css_style_sheet__140659188.txt"

css style sheet

@ascskip on
@ascskip xemacs-css-mode-on
@root "doc/docstyle.css"
&lt;&lt; HTML: css style sheet &gt;&gt;
@code

html, body {
  background-color: #CCCCCC;
  font-family: "Verdana", arial;
}

body {
  font-size: 9pt;
  line-height: 125%;
/*   margin: 1em; */
  padding: 2em;
  margin-top: 1em;
  margin-left: 3em;
/*   width: 39em; */
  min-height: 60em;
/*   margin-right: 0.5em; */
  background-color: white;
  border-top: 1px solid black;
  border-left: 1px solid black;
/*   border-right: 2px solid black; */
/*   border-bottom: 2px solid black; */
}

.strong {
  font-weight: bold;
}

h1, h2, h3, h4, h5, h6,
p
{
  margin-bottom: 0.5em;
  margin-top: 0.5em;
  line-height: 125%;
}

h1 { font-size: 2em;}
h2 { font-size: 1.4em; }
h3 { font-size: 1.2em; }
h4 { font-size: 1.0em; }
h5 { font-size: 1.0em; }
h6 { font-size: 1.0em; }

h1, h2, h3, h4, h5, h6 {
  color: #660000;
  margin-right: 20%;
}

* &gt; h1 {
  padding-top: 0.5em;
}

/* h2, h3 */
/* { */
/*   margin-right: 10em; */
/* } */

h1.title 
{
  margin-top: 3em;
  border-top: 3px solid #660000;
  border-bottom: 3px solid #660000;
  border-color: #660000;
  padding: .4em;
  text-align: center;
}

h2.title 
{
  margin-top: 3em;
  border-top: 3px solid #660000;
  border-bottom: 3px solid #660000;
  border-color: #660000;
  padding: .4em;
}

div.toc {
    line-height: 100%;
}

div.list-of-examples {
    margin-top: 3em;
}

div.sect1 h2 {
  font-size: 1.5em;
  margin-top: 4em;
  margin-left: 0em;
  margin-right: 25%;
  margin-bottom: 1em;
  /* border-color: #660000; */
  border-top: 0em;
  border-bottom: 1px solid;
  padding: 0em;
}

div.sect2 h3 {
  font-size: 1em;
  margin-top: 4em;
  margin-bottom: 1em;
  margin-right: 25%;
  /* border-color: #660000; */
  border-top: 0em;
  border-bottom: 1px solid;
}

div.sect3 h4 {
  font-size: small;
  color: black;
  margin-top: 4em;
  margin-bottom: 1em;
  margin-right: 25%;
  /* border-color: #660000; */
  border-top: 0em;
  border-bottom: 1px solid;
}

div.note
{
  margin-top: 1em;
  margin-bottom: 1em;
}
div.note .title
{
  color: black;
  font-size: x-small;
  margin-top: 0em;
  margin-bottom: 0em;
}
/* ----- links ---------------------------------------------------------- */
:link {
  color: #660000;
  text-decoration: none;
  font-weight: bold;
}

:visited {
  color: #333333;
  text-decoration: none;
  font-weight: bold;
}


div.toc :link, :visited {
  font-weight: normal;
 }

div.list-of-examples :link, :visited {
  font-weight: normal;
 }


a:link img {border-style: none;}
a:visited img {border-style: none;}

div.toc dd, dl
{
  margin-top: 0em;
  margin-bottom: 0em;
}
div.toc dt
{
  margin-top: 0.2em;
}

ul, ol
{
  margin-top: 0.5em;
  margin-bottom: 0.5em;
}

.para {
  margin-top: 0.5em;
  margin-bottom: 0.5em;
}

.sect1,
.toplevel.section
{
  padding-bottom: 0.25em;
}


tt,pre {
    font-family: Courier New,Courier,monospace;
    font-size: smaller;
}

.programlisting {
    margin-top: 8pt;
    margin-bottom: 8pt;
    margin-left: 1em;
    background-color: #FFFFCC;
    white-space: pre;
    border-style: solid;
    border-width: 1pt;
    border-color: #999999;
    padding-left: 6pt;
    padding-top: 2pt;
    padding-bottom: 2pt;
    width: 100%;
    line-height: 100%;
}

table{
    background-color: #FFFFFF;
    width: 99.6%;
}

div.example {
    margin-top: 0pt;
    margin-bottom: 0pt;
    padding-top: 0pt;
    padding-bottom: 0pt;
}

div.example .title {
    color: black;
    margin-top: 0pt;
    margin-bottom: 0pt;
    padding-top: 8pt;
    padding-bottom: 0pt;
}

div.sidebar .title {
  font-weight: bold;
  color: black;
}

div.sidebar  {
  font-size: x-small;
  margin-top: 2em;
  margin-bottom: 0.5em;
  /* margin-left: 1em; */
  margin-right: 33%; 
  padding: 4pt;
  border-top: 1px solid black;
  border-bottom: 1px solid black;
  border-left: 1px solid black;
  border-right: 1px solid black;
}


h1 &gt; a,
h2 &gt; a {
  padding-top: 0.5em;
}

ol.vert, ol.inline {
  list-style-type: none;
  padding-left: 0;
  margin-left: 0;
}

hr, .toc, .title
{ color: #660000 
}


.navfooter
{
  margin-top: 2em;
}
.navheader
{
  margin-bottom: 1em;

}

/* ------ title page ---------------------------------------------------- */
h3.author
{
  padding: 0em;
  margin-top: 0em;
  margin-bottom: -1em;
}

.affiliation
{
  padding: 0em;
  margin-top: 0em;
  margin-bottom: 0em;
  font-size: smaller;
}


div.revhistory table, tr, td
{
  border-collapse: collapse;
  border: hidden;
  font-size: x-small;
 }

div.revhistory table
{
  width: auto;
  }

div.revhistory td[colspan="3"]
{
  padding-left: 2em;  
 }


/* div.draft { */
/*   background-image: url('pics/draft.png'); */
/* } */


@doc
@ascskip xemacs-css-mode-off

</t>
<t tx="ekr.20040331071919.28">@comment &lt;!-- --&gt;
@silent
@doc
@ascskip # Time-stamp: "Thu, Jan  8 14:03 CST 2004  michael@redpriest _HTML_common__140982180.txt"
@ascskip xemacs-xsl-mode-off

indexterm:[Stylesheets,common-html.xsl]
The following section is the entire common-html style sheet
("common-html.xsl"), which sets basic HTML options.

@ascskip on
@ascskip xemacs-xsl-mode-on
@root "doc/common-html.xsl"
&lt;&lt; HTML: common&gt;&gt;
@code
&lt;?xml version='1.0'?&gt; 
&lt;xsl:stylesheet  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  version="1.0"&gt; 
&lt;!--===== ==========================================================--&gt;
&lt;xsl:param name="default.table.width" select="'100%'"&gt;&lt;/xsl:param&gt;
&lt;xsl:param name="html.stylesheet" select="'dbstyle.css'"/&gt;
&lt;xsl:param name="shade.verbatim" select="1"/&gt;
&lt;xsl:attribute-set name="shade.verbatim.style"&gt;
  &lt;xsl:attribute name="border"&gt;0&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="bgcolor"&gt;#F3F3F3&lt;/xsl:attribute&gt;
&lt;/xsl:attribute-set&gt;


&lt;/xsl:stylesheet&gt;
@doc
@ascskip xemacs-xsl-mode-off
</t>
<t tx="ekr.20040331071919.29">@comment &lt;!-- --&gt;
@silent
@doc
@ascskip # Time-stamp: "Thu, Jan  8 14:03 CST 2004  michael@redpriest _PDF__139549436.txt"

indexterm:[Stylesheets, fo-fop.xsl]
This is the Formatting Objects style sheet ("fo-fop.xsl", which sets
the options for all printed output.

The actual output is a file with the ".fo" extension, which will be
used by a Formatting Object processor to produce a PDF file.

@ascskip on
@ascskip xemacs-xsl-mode-on
@root "doc/fo-fop.xsl"
&lt;&lt; PDF &gt;&gt;
@code
&lt;?xml version='1.0'?&gt; 
&lt;xsl:stylesheet  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"  version="1.0"&gt; 
&lt;!--===== ==========================================================--&gt;

&lt;!--===== catalog will convert the url to our file location =========--&gt;
&lt;xsl:import href="fo-docbook.xsl"/&gt;
&lt;xsl:import href="common-links.xsl"/&gt;

&lt;!--===== using the fop pdf processor ===================================--&gt;
&lt;xsl:param name="fop.extensions" select="1"/&gt;

&lt;!--===== single sided pages ============================================--&gt;
&lt;xsl:param name="double.sided" select="0"&gt;&lt;/xsl:param&gt;

&lt;!--===== body print ====================================================--&gt;
&lt;xsl:param name="body.font.master"&gt;12&lt;/xsl:param&gt;
&lt;xsl:param name="alignment"&gt;left&lt;/xsl:param&gt;
&lt;xsl:param name="hyphenate"&gt;true&lt;/xsl:param&gt;

&lt;!--===== set page margins ==============================================--&gt;
&lt;xsl:param name="page.margin.inner"&gt;
  &lt;xsl:choose&gt;
    &lt;xsl:when test="$double.sided != 0"&gt;1.25in&lt;/xsl:when&gt;
    &lt;xsl:otherwise&gt;1.5in&lt;/xsl:otherwise&gt;
  &lt;/xsl:choose&gt;
&lt;/xsl:param&gt;

&lt;xsl:param name="body.margin.top" select="'.75in'"&gt;&lt;/xsl:param&gt;

&lt;!--===== set title fonts ===============================================
     Title fonts require replacing the standard
     titlepage.templates.xsl with a custom version.  This is done
     here by copying the fo/titlepage.templates.xml to
     mrc.titlepage.templates.xsl, editing it, and then processing it
     with
      xsltproc -output mrc.titlepage.templates.xsl \
         /usr/share/xml/docbook/docbook-xsl-1.60.1/template/titlepage.xsl  \
         mrc.titlepage.templates.xml
     Now we replace the old titlepage.templates.xsl with our new
     mrc.titlepage.templates.xsl
--&gt;
&lt;xsl:include href="mrc.titlepage.templates.xsl"/&gt;

&lt;!--===== blank verso titlepage =========================================--&gt;
&lt;xsl:template name="book.titlepage.verso"/&gt;

&lt;!--===== outdent titles ================================================--&gt;
&lt;xsl:param name="title.margin.left" select="'-2pc'"/&gt;

&lt;!--===== set section font, break ======================================--&gt;
&lt;xsl:attribute-set name="section.title.level1.properties"&gt;
  &lt;xsl:attribute name="font-size"&gt;14pt&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="break-before"&gt;page&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="border-bottom"&gt;1pt&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="border-bottom-style"&gt;solid&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="border-bottom-color"&gt;black&lt;/xsl:attribute&gt;  
  &lt;xsl:attribute name="margin-right"&gt;6em&lt;/xsl:attribute&gt;
&lt;/xsl:attribute-set&gt;
&lt;xsl:attribute-set name="section.title.level2.properties"&gt;
  &lt;xsl:attribute name="break-before"&gt;page&lt;/xsl:attribute&gt;
&lt;/xsl:attribute-set&gt;
&lt;xsl:attribute-set name="section.title.level3.properties"&gt;
  &lt;xsl:attribute name="break-before"&gt;page&lt;/xsl:attribute&gt;
&lt;/xsl:attribute-set&gt;

&lt;!--===== Code extract titles are sidebars ==============================--&gt;
&lt;xsl:attribute-set name="sidebar.properties" use-attribute-sets="formal.object.properties"&gt;
  &lt;xsl:attribute name="border-style"&gt;solid&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="border-width"&gt;1pt&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="border-color"&gt;black&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="background-color"&gt;#EDEDED&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="padding-left"&gt;12pt&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="padding-right"&gt;12pt&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="padding-top"&gt;2pt&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="padding-bottom"&gt;4pt&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="margin-left"&gt;0pt&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="margin-right"&gt;4em&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="margin-top"&gt;2pt&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="margin-bottom"&gt;2pt&lt;/xsl:attribute&gt;
&lt;/xsl:attribute-set&gt;
&lt;!--===== code (verbatim) font and spacing ==============================--&gt;
&lt;xsl:attribute-set name="verbatim.properties"&gt;
  &lt;xsl:attribute name="space-before.minimum"&gt;0.1pt&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="space-before.optimum"&gt;2pt&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="space-before.maximum"&gt;3pt&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="space-after.minimum"&gt;0.4em&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="space-after.optimum"&gt;.5em&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="space-after.maximum"&gt;1.2em&lt;/xsl:attribute&gt;
&lt;/xsl:attribute-set&gt;
&lt;xsl:attribute-set name="monospace.verbatim.properties"
    use-attribute-sets="verbatim.properties monospace.properties"&gt;
  &lt;xsl:attribute name="text-align"&gt;start&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="font-size"&gt;9pt&lt;/xsl:attribute&gt;
&lt;/xsl:attribute-set&gt;
    &lt;!--===== 2003-Oct-01 FOP does not appear to support shade.verbatim yet =--&gt;
&lt;xsl:param name="shade.verbatim" select="1"/&gt;
&lt;xsl:attribute-set name="shade.verbatim.style"&gt;
  &lt;xsl:attribute name="border"&gt;1&lt;/xsl:attribute&gt;
  &lt;xsl:attribute name="bgcolor"&gt;#E0E0E0&lt;/xsl:attribute&gt;
&lt;/xsl:attribute-set&gt;

    &lt;!--===== FOP did not like this =========================================--&gt;
&lt;!--&lt;xsl:attribute-set name="xref.properties"&gt;--&gt;
&lt;!--  &lt;xsl:attribute name="font-size"&gt;14pt&lt;/xsl:attribute&gt;--&gt;
&lt;!--  &lt;xsl:attribute name="font-style"&gt;bold&lt;/xsl:attribute&gt;--&gt;
&lt;!--&lt;/xsl:attribute-set&gt;--&gt;

&lt;/xsl:stylesheet&gt;

@doc
@ascskip xemacs-xsl-mode-off




</t>
<t tx="ekr.20040331071919.30">@language plain
@doc
@ascskip # Time-stamp: "Tue, Jan 13 10:21 CST 2004  michael@redpriest Appendix_XEmacs_Text_Editor_140657924.txt"

You can use Leo to enter all the text in an outline, but Leo also
allows you to use your familiar editing environment.  In my case,
that is XEmacs.  Fortunately, Leo integrates with XEmacs quite well.

The following items are code I use, some Leo Python plugins and some
XEmacs elisp functions.  You may find them useful.

@ascskip on
&lt;&lt; Appendix: XEmacs Text Editor &gt;&gt;
@code</t>
<t tx="ekr.20040331071919.31">@language python
@tabwidth -4

@doc
@ascskip # Time-stamp: "Tue, Jan 13 10:10 CST 2004  michael@redpriest _OpenWith_Plugin__140659092.py"

Leo's Open_With plugin can be modified so that the body text of any
outline node can be edited in XEmacs by choosing "File; OpenWith;
XEmacs" or "File; OpenWith; XEmacs - noshow"  from the menu.

What actually happens is that Leo places the text in a temporary
file, and calls XEmacs with the address of that temporary file.  Leo
then watches for changes in the temporary file.  When and if the
temporary file changes, Leo copies the contents to the body text of
the Leo node.
      
Below is the standard open_with.py plugin that came with Leo 4.1-rc3
The only modification I've made is to insert
@code
&lt;&lt;call XEmacs&gt;&gt;=
table = (
    ("X&amp;Emacs", "Alt+Shift+O", ("os.system","/usr/bin/gnuclient -q ", None)),
    ("X&amp;Emacs - noshow", "Ctrl+Shift+O", ("os.system","/mrc2/linux-bin/gnuclient-noshow ", None))
    )
@doc
as noted below.  A similar alteration should work for future
versions.

Note: this alteration is for XEmacs running under Linux, but a
similar command should work in the Windows environment.

I use the "gnuclient-noshow" selection to load the temporary open_with file in
the background.  It is a small bash shell script:
---
#!/bin/bash
gnuclient -eval "(find-file-noselect \"${1}\")"
---

To implement this, edit a copy of the open_with.py file that comes
with your version of Leo.  Move the original copy to a safe place,
and put your edited copy in the Leo plugins directory.  Check to see
it is included in "pluginsManager.txt" in that directory.
@ascskip on
@root "other/xemacs/open_with.py"
&lt;&lt; Open_With Plugin&gt;&gt;
@code
"""Create menu for Open With command and handle the resulting commands"""

import leoGlobals as g
import leoPlugins

Tk = g.importExtension('Tkinter',pluginName=__name__,verbose=True)

import os

if Tk: # Register the handlers...

    def on_idle (tag,keywords):
        a = g.app
        if g.app.killed: return
        for dict in a.openWithFiles:
            path = dict.get("path")
            c = dict.get("c")
            encoding = dict.get("encoding",None)
            v = dict.get("v")
            old_body = dict.get("body")
            if path and os.path.exists(path):
                try:
                    time = os.path.getmtime(path)
                    if time and time != dict.get("time"):
                        dict["time"] = time # inhibit endless dialog loop.
                        # The file has changed.
                        try:
                            # Update v from the changed temp file.
                            f=open(path)
                            s=f.read()
                            f.close()
                        except:
                            g.es("can not open " + g.shortFileName(path))
                            break
                        
                        # Convert body and s to whatever encoding is in effect.
                        body = v.bodyString()
                        body = g.toEncodedString(body,encoding,reportErrors=True)
                        s = g.toEncodedString(s,encoding,reportErrors=True) # 10/13/03
                        
                        conflict = body != old_body and body != s
                        
                        # Set update if we should update the outline from the file.
                        if conflict:
                            # See how the user wants to resolve the conflict.
                            g.es("conflict in " + g.shortFileName(path),color="red")
                            message = "Replace changed outline with external changes?"
                            result = g.app.gui.runAskYesNoDialog(c,"Conflict!",message)
                            update = result.lower() == "yes"
                        else:
                            update = s != body
                        
                        if update:
                            g.es("updated from: " + g.shortFileName(path),color="blue")
                            v.setBodyStringOrPane(s,encoding) # 10/16/03
                            c.selectVnode(v)
                            dict["body"] = s
                        elif conflict:
                            g.es("not updated from: " + g.shortFileName(path),color="blue")
                except:
                    g.es_exception() ## testing
                    pass
    def create_open_with_menu (tag,keywords):
    
        if  (tag in ("start2","open2") or
            (tag=="command2" and keywords.get("label")=="new")):
    
            # Entries in the following table are the tuple 
            # (commandName,shortcut,data).
            # 
            # - data is the tuple (command,arg,ext).
            # - command is one of "os.system", "os.startfile", "os.spawnl", 
            # "os.spawnv" or "exec".
            # 
            # Leo executes command(arg+path) where path is the full path to 
            # the temp file.
            # If ext is not None, the temp file has the extension ext,
            # Otherwise, Leo computes an extension based on what @language 
            # directive is in effect.
            
            idle_arg = "c:/python22/tools/idle/idle.py -e "
            
@doc
Here is where we insert the &lt; Call XEmacs &gt; code fragment defined above:
@code
            if 1: # Default table.


&lt;&lt; Call XEmacs &gt;&gt;
#               table = (
#                   # Opening idle this way doesn't work so well.
#                   # ("&amp;Idle",   "Alt+Shift+I",("os.system",idle_arg,".py")),
#                   ("&amp;Word",   "Alt+Shift+W",("os.startfile",None,".doc")),
#                   ("Word&amp;Pad","Alt+Shift+T",("os.startfile",None,".txt")))
#           elif 1: # Test table.
#               table = ("&amp;Word","Alt+Shift+W",("os.startfile",None,".doc")),
#           else: # David McNab's table.
#               table = ("X&amp;Emacs", "Ctrl+E", ("os.spawnl","/usr/bin/gnuclient", None)),
            
            c.frame.menu.createOpenWithMenuFromTable(table)

    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":

        g.app.hasOpenWithMenu = True
        leoPlugins.registerHandler("idle", on_idle)
        leoPlugins.registerHandler(("start2","open2","command2"), create_open_with_menu)
    
        __version__ = "1.4" # Set version for the plugin handler.
        g.plugin_signon(__name__)

</t>
<t tx="ekr.20040331071919.32">@language python
@tabwidth-4
@doc
@ascskip # Time-stamp: "Tue, Jan 13 10:14 CST 2004  michael@redpriest _OpenTree_Plugin__140660268.py"

This is a module that creates an "Open With" menu item that opens
Leo outline nodes in the tree below the current Leo node in the
XEmacs editor.I frequently have a small tree of Leo nodes which
contain code that is usually edited in the same session.

NOTE: I use the "gnuclient-noshow" selection to load the temporary
open_with file in the background.Leo calls a command with the
temporary file name at the end of the command, but the gnuclient
command needs to receive it enclosed in quotes and parentheses.The
solution is a small intermediary bash shell script called
"gnuclient-noshow":

- - -
#!/bin/bash
gnuclient- eval "(find-file-noselect \"${1}\")"
- - -

I would rather have this operate in the background, but Leo ' s
openWith always operates on the current node, and openWith has much
good error checking that I want to use.So the fast solution was to
have OpenTreeInXEmacs visibly traverse the tree.

@ascskip on
@root "other/xemacs/mod_xemacsopentree.py"
&lt;&lt; Open_Tree Plugin &gt;&gt;
@code

import leoPlugins

def OpenTreeInXEmacs (c):
    import leoCommands
    #XEmacsCommand = "/usr/bin/gnuclient -q "
    XEmacsCommand = "/mrc2/linux-bin/gnuclient-noshow "
    vnode = c.currentVnode() # get the current vnode.
    stopHere = vnode.nodeAfterTree()
    v = vnode
    while v != stopHere:
        c.openWith(data=("os.system",XEmacsCommand,None))
        v = v.threadNext()
        if (not v) or (v==stopHere):
            break
        c.selectVnode(v)
    c.selectVnode(vnode)


def CreateOpenTreeMenu (tag,keywords):

    """Create the 'Xemacs: Open Tree' menu item in the Open With menu."""


    if (tag=="open2" or
        (tag=="start2") or
        (tag=="command2" and keywords.get("label")=="new")):

        c = keyword.get('c')
        exportMenu = c.frame.menu.getMenu('Open With')
        newEntries = (
            ("-",None,None),
            ("XEmacs: Open nodes in sub-tree","None",OpenTreeInXEmacs),
        )
        c.frame.menu.createMenuEntries(exportMenu,newEntries,dynamicMenu=True)

if 1:
    leoPlugins.registerHandler(("start2","open2","command2"),CreateOpenTreeMenu)

    __version__ = ".4" # Set version for the plugin handler.
    g.plugin_signon(__name__)
@doc


@code
</t>
<t tx="ekr.20040331071919.33">@language python
@tabwidth -4
@doc
@ascskip # Time-stamp: "Tue, Jan 13 10:15 CST 2004  michael@redpriest _Filename_modification__140661308.py"

This is a small modification to Leo (via a Python plugin module) so
that Leo will open the temporary files with a name that can be
easily recognized in an XEmacs buffer listing.

On Linux, Leo opens files in the temporary files directory, all
prefixed with "LeoTemp_", which makes the names difficult to tell
apart when you have many different nodes loaded in XEmacs.

This code replaces the openWithTempFilePath method of the LeoFrame
class with code that opens temporary files in a subdirectory of the
temporary files directory, called "username_Leo", and omits the
"LeoTemp" prefix.

For example, I'm now editing this Leo node in XEmacs as
    "/tmp/michael_Leo/_Filename_modification__138976348.py"
In the XEmacs buffer list, the filename is shown as
    "_Filename_modification__138976348.py"
and all the Leo buffer names start with a leading underscore, so
they are grouped together.

For general use, this code should be considerably more robust about
creating the Leo subdirectory and signaling errors, but it is just a
quick hack that works for me on my machines.

This is distributed with Leo version 4.1rc3, so I've updated it with
Ed Ream's modifications to match that distribution.

@ascskip on
@root "other/xemacs/mod_tempfname.py"
&lt;&lt; Filename modification &gt;&gt;
@code

"""Replace Commands.openWithTempFilePath so Leo opens temporary
files with a filename that begins with the headline text, and
located in a 'username_Leo' subdirectory of the temporary
directory. The 'LeoTemp' prefix is omitted.  This makes it easier to
see which temporary file is related to which outline node.""" #'

import leoGlobals as g
import leoPlugins

import leoCommands
import getpass
import os
import tempfile

def onStart (tag,keywords):

    # g.trace("replacing openWithTempFilePath")

    g.funcToMethod(openWithTempFilePath,leoCommands.Commands,"openWithTempFilePath")

def openWithTempFilePath (self,v,ext):

    """Return the path to the temp file corresponding to v and ext.

    Replaces the Commands method."""    

    try:
        leoTempDir = getpass.getuser() + "_" + "Leo"
    except:
        leoTempDir = "LeoTemp"
        g.es("Could not retrieve your user name.")
        g.es("Temporary files will be stored in: %s" % leoTempDir)

    td = os.path.join(os.path.abspath(tempfile.gettempdir()), leoTempDir)
    if not os.path.exists(td):
        os.mkdir(td)

    name = g.sanitize_filename(v.headString()) + '_' + str(id(v.t))  + ext
    path = os.path.join(td,name)
    return path

# Register the handlers...
leoPlugins.registerHandler("start2", onStart)

__version__ = "1.3"
g.plugin_signon(__name__)
</t>
<t tx="ekr.20040331071919.34">@language plain
@silent
@doc
@ascskip # Time-stamp: "Tue, Jan 13 09:58 CST 2004  michael@redpriest _Kill_Temporary_Buffers__140661388.txt"

If you've opened a number of Leo temporary buffers in XEmacs, this
XEmacs function will kill them for you.  Just set the tempdir
variable to whatever matches your local value.

XEmacs will prompt you about any buffers that have unsaved changes.

@ascskip on
@ascskip xemacs-lisp-mode-on
@root "other/xemacs/kill-temporary-buffers.el"
&lt;&lt; Kill Temporary Buffers &gt;&gt;
@code
;;
;;-     mwd-leo-kill-buffers
(defun mwd-leo-kill-buffers ()
  "Kill any buffers for files in my Leo temporary directory."
  (interactive)
  (let ((bl (buffer-list))
        (tempdir "/tmp/michael_Leo" )  ;; change this to your temporary directory.
        )
    (while bl
      (setq test-buffer (car bl))
      (setq bname (buffer-file-name test-buffer))
      (if (and bname (string-match tempdir bname))
          (kill-buffer test-buffer)
        )
      (setq bl (cdr bl))
      )
    )
  )



@doc
@ascskip xemacs-lisp-mode-off
</t>
<t tx="ekr.20040331071919.35">@language plain
@silent
@doc
@ascskip # Time-stamp: "Tue, Jan 13 10:18 CST 2004  michael@redpriest _MMMmode__140663340.txt"

There is an editing mode for XEmacs called Multiple Major Modes,
which allows us to edit the temporary text conveniently: with all
the syntax highlighting, special keymaps, etc. available, even
though Leo nodes may contain both plain text and program code.

When the XEmacs cursor is in a section of plain text, all the plain
text facilities are available, and there is no syntax
highlighting. When the XEmacs cursor is in a section of code
(Python, XSL, whatever) XEmacs invokes the syntax highlighting,
special keymaps, etc. appropriate for that code.

indexterm:[Multiple Major Modes]
indexterm:[Multiple Major Modes,mmm-mode.el]
If you have XEmacs installed, and you have also installed the
Multiple Major Modes mmm-mode.el package, the following code will
customize mmm-mode for use while editing Leo temporary files.

NOTE: mmm-mode is already installed by default in most
distributions.

Installation: Load mmm-leo-config.el from your .init.el file, or
just load it manually to try it out.

I won't go through it all, but for example, when editing a temporary
Leo file that is in XEmacs Python mode, and/or has a ".py" suffix:

    - when your cursor is any text between the @doc and @code
      directives XEmacs will enter text-mode.  Otherwise (e.g. with
      the cursor after the @code directive), XEmacs will be in
      Python mode.
    - when your cursor is between text that says
      "xemacs -makefile-mode-on" and text that says
      "xemacs -makefile-mode-off", XEmacs will enter makefile-mode.
      (You key in those text markers to mark out the area you want
      as makefile-mode.  See the Leo2AsciiDoc.leo outline for examples,
      e.g the "Make File" section in the Leo2AsciiDoc Users Guide.)

      Otherwise, XEmacs will be in Python mode in that buffer.

Similarly, makefile-mode, xsl-mode and emacs-lisp-mode are added to
temporary Leo files that created with a ".txt" extension.      

A future project may be to create a Leo module to use in the
Leo "openWith" function that examines each node for these mmm-mode
markers and creates the temporary file with the proper extension.

@ascskip on
@ascskip xemacs-lisp-mode-on
@root "other/xemacs/mmm-leo-config.el"
&lt;&lt; MMM-mode &gt;&gt;
@code
;;-     mmm-mode                multiple modes
(require 'mmm-auto)
(require 'mmm-vars)

;   mmm-mode-on and mmm-mode-off turn it on and off in a buffer.
;   \c-c % \c-b re-parses the whole buffer

;   set mode to activate on mode or extension
(setq mmm-global-mode 'maybe)

; turn off gray background
(setq mmm-submode-decoration-level 0)

;   add embedded modes in python
(mmm-add-group
 'py-embedded-text
 '(
   (py-leo
    :submode text-mode
    :face mmm-code-submode-face
    :front "^@doc.*"
    :back "^@code"
    :insert ((?l py-leo-tag nil @ "@doc"
                 @ "\n\n" _ "\n\n" @ "@code" @))
    ; \c % l will insert the doc-code pair at point.
    )
   (py-doc
    :submode text-mode
    :face mmm-code-submode-face
    :front "^\"\"\".*"
    :back "^.+\"\"\""
    )
   (py-makefile
    :submode makefile-mode
    :face mmm-code-submode-face
    :front "xemacs-makefile-mode-on"
    :back "xemacs-makefile-mode-off"
    )
   )
 )
;   add embedded modes in text
(mmm-add-group
 'text-embedded
 '(
   (txt-makefile-mode
    :submode makefile-mode
    :face mmm-code-submode-face
    :front "xemacs-makefile-mode-on"
    :back "xemacs-makefile-mode-off"
    :insert ((?l text-embedded-tag nil @ "@doc"
                 @ "\n\n" _ "\n\n" @ "@code" @))
    ; \c % l will insert the doc-code pair at point.
    )
   (txt-xsl-mode
    :submode xsl-mode
    :face mmm-code-submode-face
    :front "xemacs-xsl-mode-on"
    :back "xemacs-xsl-mode-off"
    :insert ((?l text-embedded-tag nil @ "@doc"
                 @ "\n\n" _ "\n\n" @ "@code" @))
    ; \c % l will insert the doc-code pair at point.
    )
   (txt-lisp-mode
    :submode emacs-lisp-mode
    :face mmm-code-submode-face
    :front "xemacs-lisp-mode-on"
    :back "xemacs-lisp-mode-off"
    :insert ((?l text-embedded-tag nil @ "@doc"
                 @ "\n\n" _ "\n\n" @ "@code" @))
    ; \c % l will insert the doc-code pair at point.
    )
   )
 )
(mmm-add-mode-ext-class 'python-mode "\\.py\\'" 'py-embedded-text)
(mmm-add-mode-ext-class 'text-mode "\\.txt\\'" 'text-embedded)

@doc
@ascskip xemacs-lisp-mode-off
</t>
<t tx="ekr.20040331071919.36">@language plain
@silent
@doc
@ascskip # Time-stamp: "Tue, Jan 13 10:20 CST 2004  michael@redpriest _Insert_indexterm__140664580.txt"

indexterm:[XEmacs, Indexing]
Indexing is tedious work, and it interferes with the readability of
the ascii text as well.  However, used sparingly, it helps the
reader.

When editing a Leo node (in an XEmacs buffer), this function copies
a highlighted word or phrase and inserts an AsciiDoc index code on a
new line immediately before the paragraph.  I try to keep markup out
of the way of the reader.  In this case, AsciiDoc requires that the
index code be part of the same block of text, and the first line of
the block is the least annoying place I can find.

For example, if I wanted to index the words "XEmacs buffer" above, I
would highlight them (usually by pressing M-@ a couple of times) and
then call this function (I have it bound to C-k C-h C-i).  At the
beginning of the paragraph, my text would say "\indexterm:[XEmacs
buffer]".

@ascskip on
@ascskip xemacs-lisp-mode-on
@root "other/xemacs/index-leo-region.el"
&lt;&lt; Insert indexterm &gt;&gt;
@code
(defun mwd-index-leo-region (start end)
  "preface paragraph with AsciiDoc index macro of region."
  (interactive "r")
  (save-excursion
    (copy-region-as-kill start end)
    (backward-paragraph)
    (insert "\nindexterm:[")
    (yank)
    (insert "]")
    )
  )

@doc
@ascskip xemacs-lisp-mode-off

</t>
<t tx="ekr.20040331071919.37">@language plain
@silent
@doc
@ascskip # Time-stamp: "Tue, Jan 13 10:56 CST 2004  michael@redpriest _Indent_Leo_comments__141202716.txt"

Leo derived files are sprinkled with comments, which Leo uses as
markers to be able to "untangle" files, i.e. import changes made to
a derived file back into the Leo outline.

Useful as they may be, the comments are an ugly distraction when
reading the source code.  One could have XEmacs flush them from the
file, but then the untangle feature is gone for that file.

This pair of XEmacs elisp functions moves them to the right, where
they aren't so distracting, and moves them back again if you should
want to untangle the file.

@ascskip on
@ascskip xemacs-lisp-mode-on
@root "other/xemacs/indent-leo-comments.el"
&lt;&lt; Indent Leo comments &gt;&gt;
@code
(defun mwd-leo-comments-indent ()
  "Indent Leo comments to make them less distracting."
  (interactive)
  (save-excursion
    (let* (
          (leading-spaces 40)
          (start-string (concat (make-string leading-spaces ? ) "\\1" ))
          (end-string (concat (make-string leading-spaces ? ) "\\1" ))
          )
      (goto-char (point-min))
      (while (search-forward-regexp "\\(^# &lt;&lt;\\)" nil t) (replace-match start-string))
      (goto-char (point-min))
      (while (search-forward-regexp "\\(^# -- end\\)" nil t) (replace-match end-string))
      )
    )
  )

(defun mwd-leo-comments-unindent ()
  "Reverse the effect of mwd-leo-comments-indent."
  (interactive)
  (save-excursion
      (goto-char (point-min))
      (while (search-forward-regexp "^\\(\\s-\\)+\\(# &lt;&lt;\\)" nil t) (replace-match "\\2" ))
      (goto-char (point-min))
      (while (search-forward-regexp "^\\(\\s-\\)+\\(# -- end\\)" nil t) (replace-match "\\2" ))
    )
  )
@doc
@ascskip xemacs-lisp-mode-off
</t>
<t tx="ekr.20040331071919.38">@language plain
@ascfile "doc/mod_asc_user.asc"
@ascconfig maxCodeLineLength 80
@doc
@ascskip # Time-stamp: "Mon, Jan 19 15:29 CST 2004  michael@redpriest Leo_AsciiDoc_Users_Guide_141652036.txt"

Preface
-------

Leo2AsciiDoc is a small Python program which has been
built to be used as a plugin module for the Leo outlining editor.

Leo2AsciiDoc enables the contents of Leo outlines to be published to HTML
or PDF via the DocBook set of publishing tools.  Plain text from the
Leo outline is transformed into a final result that has:

    - typeset body text, in which bulleted and numbered lists,
      variable lists, page numbers, URLs, index terms,and bold and
      italic text are automatically recognized.
    - typeset Headings
    - a Table of Contents
    - an Index containing any items marked by the user, and any
      Python classes or functions.

As you will see, there's not a lot involved in using the
Leo2AsciiDoc module.  It simply copies text from a Leo outline (or a
portion of a Leo outline) to a text file.  In turn that text file can
be automatically converted by the AsciiDoc program and a DocBook
system to properly typeset DocBook HTML, PDF or other formats.

If you keep your text plain, and use a few simple formatting
conventions, the final output can have typeset headings, bulleted
lists, indexing and cross-referencing, as well as many other
features.

---
Michael Dawson
Marshall Research
michael_dawson at marshallresearch dot com
---

*note*

Leo2AsciiDoc is suited for general text documents, most programming
documentation and most business documents.  Leo2AsciiDoc (being based on
DocBook) is not the choice for anyone needing detailed typographic
control of individual words or characters -- for example, typeset
equations.  In general, DocBook typesets blocks of text.

*note*

@code
</t>
<t tx="ekr.20040331071919.39">@doc
@ascskip # Time-stamp: "Mon, Jan 19 11:48 CST 2004  michael@redpriest Installation_140689076.txt"
Installation of this plugin is very straightforward, using Leo
version 4.1:

    - copy the python source code (mod_leo2ascd.py) to your Leo
      plugin directory (a subdirectory called "plugins" under your
      main Leo directory).
    - in that directory should be a text file called
      pluginsManager.txt, containing a list of all plugins that are
      to be loaded when Leo starts.  Add mod_leo2ascd.py to the
      list.
    - start or re-start Leo.
    - in the Leo Log Window you should see the Leo2AsciiDoc sign-on
      message "---mod_leo2asc 0.4-------".
    - in the Leo main menu "File; Export", there should be two menu
      items called something like "Export to AsciiDoc".

@code</t>
<t tx="ekr.20040331071919.40">@language plain
@doc
@ascskip # Time-stamp: "Thu, Oct 16 13:46 CST 2003  michael@redpriest Operation_140791428.txt"

Using Leo2AsciiDoc is as simple as choosing the Leo menu item: "File;
Export; Export All to AsciiDoc".  From there, you have the AsciiDoc
program and the DocBook system automatically convert your outline to
HTML or PDF (or to a manpage or a DocBook website.)

Step by step:

    - You need a Leo outline containing some plain text, or plain
      text and code.
    - You ensure that the top node in the outline (or part of the
      outline tree which you want to be a separate document) must
      have an @ascfile directive in the body text. The @ascfile
      directive is used to specify the filename in which the output
      text will be put.
    - You then use Leo's menu: "File; Export; Export All to
      AsciiDoc" (or one of the other Leo2AsciiDoc menu items) to
      have Leo2AsciiDoc automatically export the outline to a text file.
    - After that, you run the AsciiDoc program on the exported text
      file, and process it as a DocBook document.  Most often,
      people have a Make file set up to do this automatically.

In practice, people often want to use special features:

    - plain text formatting, sometimes referred to as "structured
      text" or "minimal markup"
    - Leo2AsciiDoc configuration options

The following sections cover this.  If you've downloaded the Leo2AsciiDoc
package, the mod_leo2asc.leo outline is available, and illustrates
all the features.  It is the outline from which all the Leo2AsciiDoc HTML
and PDF documentation and code were derived.

@code
</t>
<t tx="ekr.20040331071919.41">@doc
@ascskip # Time-stamp: "Mon, Jan 19 13:19 CST 2004  michael@redpriest Directives_140672364.txt"

The following are non-printing directives that you can insert into
your outline text to control Leo2AsciiDoc behaviour.  All must be at the
beginning of the line.

{amp}commat;ascfile::
    e.g: `@ascfile "doc/mod_asc_user.asc" `

    Ascfile is the equivalent of a Leo @root directive. Ascfile
    signals the start of a document and specifies the file name to
    receive the text.

    The default directory is the directory containing the Leo
    outline.  If you were editing an outline that resided in
    /home/me then the above ascfile directive would create the file
    mod_asc/user.asc in the directory /home/me/doc.

{amp}commat;ascignore::
    Ascignore causes Leo2AsciiDoc to ignore the outline node, and any
    sub-nodes. It must be placed before any line in the node which
    will print.

{amp}commat;ascskip::
    Causes Leo2AsciiDoc to skip the line.  If followed by the word "on",
    causes Leo2AsciiDoc to skip all succeeding document lines until an
    "{amp}commat;ascskip off" directive is read, or a code section is reached.

{amp}commat;ascexit::
    Causes Leo2AsciiDoc to exit the outline node without processing any
    further lines.  Sub-nodes will be processed.

{amp}commat;ascconfig::
    e.g. `{amp}commat;ascconfig maxCodeLineLength 70` -- see
    Configuration below. 
    

@code
</t>
<t tx="ekr.20040331071919.42">@doc
@ascskip # Time-stamp: "Mon, Jan 19 13:20 CST 2004  michael@redpriest Configuration_140673612.txt"

There are a few configuration settings which may be set in an
outline.  To take effect, they must be placed:

    - in the top node of the outline, or
    - the same node as an @ascfile directive.
    
Configuration settings in the top node of the outline are effective
for the whole outline, unless overridden by settings in sub-nodes.

maxCodeLineLength::
    e.g. `{amp}commat;ascconfig maxCodeLineLength 70` -- 
    sets the maximum length of code printout lines to 70 characters.
    Longer lines will be wrapped and a line continuation character
    displayed.

PrintHeadings::    
    e.g. `{amp}commat;ascconfig PrintHeadings off` -- turns off the
    export of outline node headings as section titles.  In that
    case, you must have correctly entered AsciiDoc section titles in
    the body text of your outline.

Readers of the code will note that there are other configuration
settings in the code. These will be used in future, and so I won't
document them yet.


@code</t>
<t tx="ekr.20040331071919.43">@language plain
@doc
@ascskip # Time-stamp: "Mon, Jan 19 13:22 CST 2004  michael@redpriest Markup_140672220.txt"

The point of using a system like AsciiDoc is to get a document that
is properly typeset, while writing only plain text with as little
embedded formatting instruction as possible.

For the most part, you simply write chunks of text, which become
typeset paragraphs.

I've tried to use most commonly used markup in the Leo outline that
contains all the Leo2AsciiDoc source and documentation, so that you
can see exactly how markup may be used.

@code</t>
<t tx="ekr.20040331071919.44">@doc
@ascskip # Time-stamp: "Mon, Jan 19 13:20 CST 2004  michael@redpriest Standard_AsciiDoc_Markup_140676540.txt"

This section illustrates a very small part of the standard AsciiDoc
markup.  However, AsciiDoc comes with extensive documentation of its
own, which any Leo2AsciiDoc user should read.


@code</t>
<t tx="ekr.20040331071919.45">@doc
@ascskip # Time-stamp: "Thu, Jan  8 14:06 CST 2004  michael@redpriest Headings_141020668.txt"

indexterm:[Markup, Headings]
Leo2AsciiDoc will automatically create Headings from the headings of
your Leo outline.  You can turn this off (see Configuration), and
create your own headings in the body text of an outline node.  For
example, a Chapter heading is text at the left margin that has a
following line of dashes.  For example,

@code
 Operation
 ---------

@doc
is the heading of this chapter.  Chapter sub-sections have a
following line of tildes.  For example,

@code

 Markup
 ~~~~~~

@doc

is the heading of Section One of this chapter.  Section Two markup
is a following line of "^".  For example, 

@code

Standard AsciiDoc Markup
^^^^^^^^^^^^^^^^^^^^^^^^
@doc

is the heading of the section, which is a Section Two.

As I say, you normally don't need to do this, since Leo2AsciiDoc does all
this itself from the outline headings.


@code
</t>
<t tx="ekr.20040331071919.46">@doc
@ascskip # Time-stamp: "Thu, Jan  8 14:06 CST 2004  michael@redpriest Lists_141018612.txt"

indexterm:[Markup, lists]
Bulleted lists start with a dash (or asterisk) followed by a space
or tab character.  I've extended this to allow leading spaces.  For
example,
    
@code
    - this is a list item
        * this is a sub-item
    - this is another list item
@doc

produces:

    - this is a list item
        * this is a sub-item
    - this is another list item


@code</t>
<t tx="ekr.20040331071919.47">@doc
@ascskip # Time-stamp: "Thu, Jan  8 14:07 CST 2004  michael@redpriest URLs_140994492.txt"

indexterm:[Markup, URL]
The URL address of a web page will be "hot" in the HTML or PDF
document, when terminated with square brackets:

@code

http://www.docbook.org[The official home page for DocBook: The Definitive  Guide.]

@doc

results in:

http://www.docbook.org[The official home page for DocBook: The Definitive Guide.]


@code</t>
<t tx="ekr.20040717133342"></t>
<t tx="ekr.20040722134535"></t>
<t tx="ekr.20040722135402"></t>
<t tx="ekr.20040722135402.1"></t>
<t tx="ekr.20040722141148">@

You would typically not enable any of the following "plugins".

These plugins contain example code only.</t>
<t tx="ekr.20040809151600.52"># Leo comes with aspell23.pyd and aspell24.pyd pre-made.
# The following notes are for reference only.</t>
<t tx="ekr.20040809151600.53">"""A Pyrex wrapper for the aspell api."""

cdef extern from "aspell.h":
  ctypedef struct AspellConfig
  AspellConfig* new_aspell_config()
  void delete_aspell_config(AspellConfig*)
  int aspell_config_replace(AspellConfig*, char*, char*)
  ctypedef struct AspellCanHaveError
  AspellCanHaveError* new_aspell_speller(AspellConfig*)
  #ctypedef struct AspellManager
  unsigned int aspell_error_number(AspellCanHaveError*)
  char* aspell_error_message(AspellCanHaveError*)
  ctypedef struct AspellSpeller
  AspellSpeller* to_aspell_speller(AspellCanHaveError*)
  int aspell_speller_check(AspellSpeller*, char*, int)
  ctypedef struct AspellWordList
  AspellWordList* aspell_speller_suggest(AspellSpeller*, char*, int)
  ctypedef struct AspellStringEnumeration
  AspellStringEnumeration * aspell_word_list_elements(AspellWordList*)
  char* aspell_string_enumeration_next(AspellStringEnumeration*)
  int aspell_speller_store_replacement(AspellSpeller*, char*, int, char*, int)
  int aspell_speller_add_to_session(AspellSpeller*, char*, int)
  int aspell_speller_add_to_personal(AspellSpeller*, char*, int)
  int aspell_speller_error(AspellSpeller*)
  char* aspell_speller_error_message(AspellSpeller*)
  int aspell_speller_save_all_word_lists(AspellSpeller*)

class Error(Exception):
  pass

cdef class spell_checker:
  '''A simple wrapper for the Aspell API'''
  cdef AspellConfig* config
  cdef AspellSpeller* checker
  
  @others</t>
<t tx="ekr.20040809151600.54">@language python
@tabwidth -4

from distutils.core import setup, Extension
from Pyrex.Distutils import build_ext
import os

if os.name == 'nt':
  #c:/Program Files/Aspell
  aspell_home = './aspell-dev-0-50-3-3'
  libraries = ['aspell-15']
  include_dirs = [aspell_home+'/include']
  library_dirs = [aspell_home+'/lib']
else:
  raise RuntimeError, 'you need to modify setup.py to work with %s' % os.name

ext = Extension('aspell', ['aspell.pyx' ],
                libraries = libraries,
                include_dirs = include_dirs,
                library_dirs = library_dirs,
                )
                
setup(name="aspell", version="1.1",
      ext_modules = [ext],
      cmdclass = {'build_ext': build_ext}
)</t>
<t tx="ekr.20040809160744">@killcolor

You also need from aspell the include and lib dev packages
if on windows the dlls and a sutible dictionary

included here for redistribution as a convience only
unmodifyed except for path to the include &amp; lib path

A Pyrex wrapper for the aspell api.

&lt;http://prdownloads.sourceforge.net/uncpythontools/aspell-1.0.zip?download&gt;
&lt;http://sourceforge.net/project/showfiles.php?group_id=82407&gt;</t>
<t tx="ekr.20040809160744.1">def __init__(self, lang="en_US", prefix="c:/Program Files/Aspell", **kwargs):

    self.config = new_aspell_config()
    aspell_config_replace(self.config, "prefix", prefix)
    aspell_config_replace(self.config, "lang", lang)
    for key,value in kwargs.items():
      aspell_config_replace(self.config, key, value)
    cdef AspellCanHaveError* possible_err
    possible_err = new_aspell_speller(self.config)
    if aspell_error_number(possible_err) != 0:
      msg = aspell_error_message(possible_err)
      raise Error, msg
    else:
      self.checker = to_aspell_speller(possible_err)</t>
<t tx="ekr.20040809160744.2">def check(self, word):
    '''Return 0 if word is misspelled, 1 otherwise.'''
    return aspell_speller_check(self.checker, word, len(word))</t>
<t tx="ekr.20040809160744.3">def suggest(self, word):
    '''Return a list of suggested replacements for a misspelled word.'''
    cdef AspellWordList* suggestions
    # I need a cast here to stop the C compiler from complaining about const mismatch
    suggestions = &lt;AspellWordList*&gt;aspell_speller_suggest(self.checker, word, len(word))
    cdef AspellStringEnumeration* elements
    elements = aspell_word_list_elements(suggestions)
    result = []
    cdef char* suggestion
    while 1:
      # this cast is the hush the C compiler which knows this function is const char*
      suggestion = &lt;char*&gt;aspell_string_enumeration_next(elements)
      if suggestion == NULL:
        break
      result.append(suggestion)
    return result</t>
<t tx="ekr.20040809160744.4">def store_replacement(self, wrongword, rightword):
    '''Tell Aspell about the correction so it can learn about your mistakes.'''
    return aspell_speller_store_replacement(self.checker, wrongword, len(wrongword),
                                            rightword, len(rightword))</t>
<t tx="ekr.20040809160744.5">def add_to_session(self, word):
    '''Tell Aspell to allow word for this session.'''
    return aspell_speller_add_to_session(self.checker, word, len(word))

</t>
<t tx="ekr.20040809160744.6">def add_to_personal(self, word):
    '''Tell Aspell to allow word permanently.'''
    r = aspell_speller_add_to_personal(self.checker, word, len(word))
    aspell_speller_save_all_word_lists(self.checker)
    return r</t>
<t tx="ekr.20040809161108">@killcolor

Pyrex is *SO* great! I wrote this in about 1 hour from the
Aspell doc. I spent most of that hour figuring out that I needed to
set the Aspell "prefix" to get it to work!

Intended usage is:

1) create a spell_checker object for each document.

2) check a word by calling the check method

3) if you get 0 back indicating a misspelling, use the suggest method
   to get a list of possible correct spellings.
   
4) tell aspell about the correct choice so it can learn from your
   errors using the store_replacement method
   
5) add words to either the session dictionary or to your personal
   dictionary using the add_to_session or add_to_personal methods.

import aspell
sc = aspell.spell_checker()
word = 'flarg'
if not sc.check(word):
  print word, 'is incorrect'
  print 'suggestions include:', sc.suggest(word)

To get this to build and work on Windows I downloaded the Windows
version of aspell from http://aspell.net/win32/. I got the Full
Installer, a dictionary, and the libraries for MS VisualC++ as
separate downloads. I let the first two go to their default locations
and I unpacked the zip file for the last into the C:\Program
Files\Aspell top directory. Then I copied the aspell-15.dll from
C:\Program Files\Aspell\bin to a folder on my path.

You will also, of course, need Pyrex from
http://www.cosc.canterbury.ac.nz/~greg/python/Pyrex/.

With the above completed the standard 'python setup.py install' should
build and install the extension.

I believe this should work on Linux with trivial modification.

This software is free for anyone to use for any purpose. If you or your
lawyer are stupid enough to believe that I have any liability for this
code then do not use it.

23 May 2004
Gary Bishop</t>
<t tx="ekr.20040828105233">@first # -*- coding: utf-8 -*-
@language python
@tabwidth -4

"""
Translate a few menu items into Simplified Chinese
本插件将部分Leo菜单翻译成简体中文
   By Zhang Le &lt;ejoy@xinhuanet.com&gt;
   
"""

# Chinese translation completed by Zhang Le, May 2004
# based on the french_fm.py

# NOTE: The accelerated key (&amp;) failed to work on Chinese text, probably because 
# the width of one Chinese character is 2 not 1, which confuses Tk. I'm not sure 
# whether this is a bug of Tk or a bug of Leo. Although I do not use &amp; in the 
# Chinese menu, Tk places an underline below the first character of each menu
# entry. Another bug in Tk?

# Note 2 (EKR):  The menu names themselves did not translate on my XP machine.
# All the headlines appear as "??".

import leoPlugins
import leoGlobals as g

@others

if not g.app.unitTesting: # Unpleasant for unit testing.

    # Register the handlers...
    leoPlugins.registerHandler("menu1", onMenu)
    
    __version__ = "1.1" # Set version for the plugin handler.
    g.plugin_signon(__name__)</t>
<t tx="ekr.20040828105233.1">def onMenu (tag,keywords):

    c = keywords.get("c")
    table = (
        @others
    )

    # Call the convenience routine to do the work.
    c.frame.menu.setRealMenuNamesFromTable(table)</t>
<t tx="ekr.20040828105233.2">("File","File文件"),
    ("New","新建"),
    ("Open...","打开"),
    ("Open With...","用程序打开..."),
    ("Close","关闭"),
    ("Save","保存"),
    ("Save As","另存为..."),
    ("Save To","另存到..."),
    ("Revert To Saved","恢复到保存的文件"),
    ("Recent Files...","最近访问的文件..."),
        ("Clear Recent Files","清除最近访问文件列表"),
    ("Read/Write...", "读取/写入..."),
        ("Read Outline Only", "只读取大纲"),
        ("Read @file Nodes", "读取 @file 结点"),
        ("Write Dirty @file Nodes", "保存改动的 @file 结点"),
        ("Write missing @file Nodes", "保存缺少的(missing) @file 结点"),
        ("Write Outline Only", "仅保存大纲"),
        ("Write @file Nodes", "保存 @file 结点"),
        ("Write 4.x Derived Files", "保存 4.x 版本的文件"),
        ("Write 3.x Derived Files", "保存 3.x 版本的文件"),
    ("Tangle...", "Tangle 操作..."),
        ("Tangle All", "全部 Tangle"),
        ("Tangle Marked", "只 Tangle 书签结点"),
        ("Tangle", "Tangle 当前结点"),
    ("Untangle...", "Untangle 操作..."),
        ("Untangle All", "全部 Untangle"),
        ("Untangle Marked", "只 Untangle 书签结点"),
        ("Untangle", "Untangle 当前结点"),
    ("Import...", "导入..."),
        ("Import Derived File", "导入生成的文件"),
        ("Import To @file", "导入到 @file"),
        ("Import To @root", "导入到 @root"),
        ("Import CWEB Files", "导入 CWEB 文件"),
        ("Import noweb Files", "导入 noweb 文件"),
        ("Import Flattened Outline", "导入平坦 (Flattened) 大纲文件 (MORE 格式)"),
    ("Export...", "导出..."),
        ("Export Headlines", "导出标题 (Headlines)"),
        ("Outline To CWEB", "导出大纲到 CWEB"),
        ("Outline To Noweb", "导出大纲到 Noweb"),
        ("Flatten Outline", "导出平坦 (Flattened) 大纲 (MORE 格式)"),
        ("Remove Sentinels", "删除导出文件中的特殊大纲标记 (Sentinelles)"),
        ("Weave", "导出为 Weave 格式 (Listing)"),
        ("Export all to AsciiDoc", "全部导出为 AsciiDoc 文件"),
        ("Export current tree to AsciiDoc", "将当前树导出为 AsciiDoc 文件"),
    ("Exit","退出"),
</t>
<t tx="ekr.20040828105233.3">("Edit","Edit编辑"),
    ("Undo Typing","撤销键入"),
    ("Undo Cut Node","撤销剪切结点"),
    ("Redo Typing","重做键入"),
    ("Can't Undo", "无法撤销"),
    ("Can't Redo", "无法重做"),
    ("Cut", "剪切"),
    ("Copy", "复制"),
    ("Paste", "粘贴"),
    ("Delete", "删除"),
    ("Select All", "全选"),
    ("Edit Body...", "编辑文本域..."),
        ("Extract Section", "Extract Section"),
        ("Extract Names", "Extract Names"),
        ("Extract", "Extract"),
        ("Convert All Blanks", "Convert All Blanks"),
        ("Convert All Tabs", "Convert All Tabs"),
        ("Convert Blanks", "Convert Blanks"),
        ("Convert Tabs", "Convert Tabs"),
        ("Insert Body Time/Date", "插入当前日期/时间"),
        ("Reformat Paragraph", "重新格式化段落"),
        ("Indent", "增加缩进"),
        ("Unindent", "减少缩进"),
        ("Match Brackets", "括号匹配"), #  &lt;({["), #EKR
    ("Edit Headline...", "编辑标题..."),
        ("Edit Headline", "编辑标题"),
        ("End Edit Headline", "结束编辑标题"),
        ("Abort Edit Headline", "放弃编辑标题"),
        ("Insert Headline Time/Date", "插入当前日期/时间"),
        ("Toggle Angle Brackets", "切换尖括号标记"),
    ("Find...", "查找..."),
        ("Find Panel", "查找对话框"),
        ("Find Next", "查找下一个"),
        ("Find Previous", "查找前一个"),
        ("Replace", "替换"),
        ("Replace, Then Find", "替换后查找"),
    ("Go To Line Number", "跳转到行..."),
    ("Execute Script", "执行Python脚本"),
    ("Set Font...", "设置字体..."),
    ("Set Colors...", "设置颜色..."),
    ("Show Invisibles", "显示不可见域"),
    ("Hide Invisibles", "隐藏不可见域"),
    ("Preferences", "偏好设置"),
</t>
<t tx="ekr.20040828105233.4">("Outline", "Outline大纲"),
    ("Cut Node", "剪切结点"),
    ("Copy Node", "拷贝结点"),
    ("Paste Node", "粘贴结点"),
    ("Delete Node", "删除结点"),
    ("Insert Node", "插入结点"),
    ("Clone Node", "克隆结点"),
    ("Sort Children", "排序孩子结点"),
    ("Sort Siblings", "排序兄弟结点"),
    ("Check Outline", "校验大纲"),
    ("Dump Outline", "大纲转储 (Dump)"),
    ("Hoist", "提升结点 (Hoist)"),
    ("De-Hoist", "下降结点 (De-Hoist)"),
    ("Expand/Contract...", "扩展/收缩"),
        ("Contract All", "全部收缩"),
        ("Contract Node", "收缩当前结点"),
        ("Contract Parent", "收缩父结点"),
        ("Expand Prev Level", "扩展到上一级"),
        ("Expand Next Level", "扩展到下一级"),
        ("Expand To Level 1", "扩展到第1级"),
        ("Expand To Level 2", "扩展到第2级"),
        ("Expand To Level 3", "扩展到第3级"),
        ("Expand To Level 4", "扩展到第4级"),
        ("Expand To Level 5", "扩展到第5级"),
        ("Expand To Level 6", "扩展到第6级"),
        ("Expand To Level 7", "扩展到第7级"),
        ("Expand To Level 8", "扩展到第8级"),
        ("Expand All", "扩展全部"),
        ("Expand Node", "扩展当前结点"),
    ("Move...", "移动..."),
        ("Move Down", "下移"),
        ("Move Left", "左移"),
        ("Move Right", "右移"),
        ("Move Up", "上移"),
        ("Promote", "Promote"),
        ("Demote", "Demote"),
    ("Mark/Unmark...", "书签功能..."),
        ("Mark", "标记书签"),
        ("Unmark", "删除书签"),
        ("Mark Subheads", "标记子标题"),
        ("Mark Changed Items", "标记已修改的结点"),
        ("Mark Changed Roots", "标记已修改的根结点 (Roots)"),
        ("Mark Clones", "标记克隆"),
        ("Unmark All", "删除所有书签"),
    ("Go To...", "跳转到..."),
        ("Go Back", "后退"),
        ("Go Forward", "前进"),
        ("Go To Next Marked", "跳转到下一个书签"),
        ("Go To Next Changed", "跳转到下一个已修改结点"),
        ("Go To Next Clone", "跳转到下一个克隆结点"),
        ("Go To First Node", "跳转到第一个结点"),
        ("Go To Last Node", "跳转到最后一个结点"),
        ("Go To Parent", "跳转到父结点"),
        ("Go To Prev Sibling", "跳转到上一个兄弟结点"),
        ("Go To Next Sibling", "跳转到下一个兄弟结点"),
        ("Go To Prev Visible", "跳转到上一个可见结点"),
        ("Go To Next Visible", "跳转到下一个可见结点"),
        ("Go To Prev Node", "跳转到上一结点"),
        ("Go To Next Node", "跳转到下一结点"),</t>
<t tx="ekr.20040828105233.5">("Plugins", "Plugins插件"),
    ("chinese", "Chinese (汉化)"),
</t>
<t tx="ekr.20040828105233.6">("Window", "Window窗口"),
    ("Equal Sized Panes", "使各面板大小相等"),
    ("Toggle Active Pane", "切换激活面板"),
    ("Toggle Split Direction", "切换面板分割方向"),
    ("Cascade", "级联排列窗体"),
    ("Minimize All", "全部最小化"),
    ("Open Compare Window", "打开文件比较窗口..."),
    ("Open Python Window", "打开Python集成环境(IDLE)..."),
</t>
<t tx="ekr.20040828105233.7">("Help", "Help帮助"),
    ("About Leo...", "关于Leo..."),
    ("Online Home Page", "访问在线主页"),
    ("Open Online Tutorial", "访问在线教程"),
    ("Open Offline Tutorial", "访问离线教程 (CHM文件)"),
    ("Open LeoDocs.leo", "打开 LeoDocs.leo"),
    ("Open LeoConfig.leo", "打开 LeoConfig.leo"),
    ("Apply Settings", "应用设置")</t>
<t tx="ekr.20040915073259"></t>
<t tx="ekr.20040918165144.9"></t>
<t tx="ekr.20040918165427"></t>
<t tx="ekr.20040918165427.4">@nocolor

Developers
By: jasonic ( Jason Cunliffe ) 
 @dictionary   
2003-08-21 07:51

Auto-completion dictionary files would be excellent.
Ideally each Leo language extension could just point to a separate .dict file. 

Hopefully we can build some Leo plugin utilities to generate these .dict files by parsing any file you'd like to use a 'source' for Leo dictionary. They might need manual cleanup, but vcould be big timesaver, especially for XML formats and the like. Great to be able to sahre these easily. 

Interesting uses for Leo dictionaries beyond just autocompletion. 
I am thinking they might open the door to some powerful macro/template behavior. 

For example, you load a special dictionary to help certain kinds of repetitive formatted content. CSS and XSLT could be good candidates, but also any kind of mild databases or lists. Documentation.

So first we need basic dicts for Leo supported languages: Python, Perl, Javascript etc..

Then we need to consider that any Leo Node could have its own dictionary defined inline..

@dictionary filepath-to-custom-leo-dict

With collaborative LeoN this would be very useful because connected Leo sessions could invoke each other's dictionaries!!

- Jason  
</t>
<t tx="ekr.20040918165427.5">http://sourceforge.net/forum/message.php?msg_id=2388444
By: mdawson

I use DocBook XML for my computer documentation, and lately for
publishing just about any text document.  Naturally, I wanted an
easy way to use DocBook to publish Leo outlines.

I've written a small Leo module, called Leo2AsciiDoc, that enables
automatic publication of a plain text Leo outline to HTML or PDF, or
as a web site or man page.  Stuart Rackham's AsciiDoc program (in
Python) is what makes this possible.
    Leo2AsciiDoc exports a Leo outline to a text file, from whence
it can be converted to DocBook XML by AsciiDoc, and then
automatically published via DocBook to HTML or PDF.

One Leo outline can contain any number of documents, or web sites
(via DocBook Website).

I'm also learning Literate Programming, and am happy to be able to
automatically publish (via make) a program's source and
documentation from Leo.

An example of the product is the paged HTML documentation for the
module at:
    http://devguide.leo.marshallresearch.ca

The web page for Leo2AsciiDoc is
at:
    http://leo.marshallresearch.ca

That web site is produced from a Leo outline.

    ----------------------------------------
    Michael Dawson</t>
<t tx="ekr.20041001210557"></t>
<t tx="ekr.20041009112303"></t>
<t tx="ekr.20041019072632"></t>
<t tx="ekr.20041030092101">@ Notes by EKR:  The dyna plugin is a remarkable body of work by 'e'.  Have fun with it.

You may download the latest version at: http://rclick.netfirms.com/dyna_menu.py.html
</t>
<t tx="ekr.20041103052443"># Execute this in a script button.

import string

@others

if 1:
    &lt;&lt; set nameList to the list of functions in leoGlobals.py &gt;&gt;
else:
    p = g.findNodeAnywhere("@file leoGlobals.py")
    nameList = findFunctionsInTree(p)

    nameList.sort() ; g.enl()
    for name in nameList: g.es("'%s'," % name)
    
    s = "%d functions in leoGlobals.py" % len(nameList)
    print s ; g.es(s)


p = c.currentPosition()
g.enl() ; g.enl()
count = prependNamesInTree(p,nameList,"g.",replace=True) # Just prints if replace==False.
s = "%d --- done --- " % count
print s ; g.es(s)</t>
<t tx="ekr.20041103052443.1">def findFunctionsInTree(p):
    
    nameList = []
    for p in p.self_and_subtree_iter():
        names = findDefs(p.bodyString())
        if names:
            for name in names:
                if name not in nameList:
                    nameList.append(name)
    return nameList</t>
<t tx="ekr.20041103052443.2">def findDefs(body):
    
    lines = body.split('\n')
    names = []
    for s in lines:
        i = g.skip_ws(s,0)
        if g.match(s,i,"class"):
            return [] # The classes are defined in a single node.
        if g.match(s,i,"def"):
            i = g.skip_ws(s,i+3)
            j = g.skip_c_id(s,i)
            if j &gt; i:
                name = s[i:j]
                if g.match(name,0,"__init__"): 
                    return [] # Disallow other class methods.
                names.append(name)
    return names</t>
<t tx="ekr.20041103052443.3">def prependNamesInTree(p,nameList,prefix,replace=False):
    
    c = p.c
    
    assert(len(prefix) &gt; 0)
    ch1 = string.letters + '_'
    ch2 = string.letters + string.digits + '_'
    def_s = "def " ; def_n = len(def_s)
    prefix_n = len(prefix)
    total = 0
    c.beginUpdate()
    for p in p.self_and_subtree_iter():
        count = 0 ; s = p.bodyString()
        printFlag = False
        if s:
            for name in nameList:
                i = 0 ; n = len(name)
                while 1:
                    &lt;&lt; look for name followed by '(' &gt;&gt;
            if count and replace:
                if 0:
                    &lt;&lt; print before and after &gt;&gt;
                p.setBodyStringOrPane(s)
                p.setDirty()
        g.es("%3d %s" % (count,p.headString()))
        total += count
    c.endUpdate()
    return total</t>
<t tx="ekr.20041103052443.4">i = s.find(name,i)
if i == -1:
    break
elif g.match(s,i-1,'.'):
    i += n # Already an attribute.
elif g.match(s,i-prefix_n,prefix):
    i += n # Already preceded by the prefix.
elif g.match(s,i-def_n,def_s):
    i += n # preceded by "def"
elif i &gt; 0 and s[i-1] in ch1:
    i += n # Not a word match.
elif i+n &lt; len(s) and s[i+n] in ch2:
    i += n # Not a word match.
else:
    j = i + n
    j = g.skip_ws(s,j)
    if j &gt;= len(s) or s[j] != '(':
        i += n
    else: # Replace name by prefix+name
        s = s[:i] + prefix + name + s[i+n:]
        i += n ; count += 1
        # g.es('.',newline=False)
        if 1:
            if not printFlag:
                printFlag = True
                # print p.headString()
            print g.get_line(s,i-n)</t>
<t tx="ekr.20041103052443.5">print "-"*10,count,p.headString()
print "before..."
print p.bodyString()
print "-"*10,"after..."
print s</t>
<t tx="ekr.20041103052443.6">nameList = (
'alert',
'angleBrackets',
'appendToList',
'callerName',
'CheckVersion',
'choose',
'clearAllIvars',
'clear_stats',
'collectGarbage',
'computeLeadingWhitespace',
'computeWidth',
'computeWindowTitle',
'createTopologyList',
'create_temp_name',
'disableIdleTimeHook',
'doHook',
'dump',
'ecnl',
'ecnls',
'enableIdleTimeHook',
'enl',
'ensure_extension',
'es',
'esDiffTime',
'es_error',
'es_event_exception',
'es_exception',
'escaped',
'executeScript',
'file_date',
'findNodeAnywhere',
'findTopLevelNode',
'findNodeInTree',
'findReference',
'find_line_start',
'find_on_line',
'flattenList',
'funcToMethod',
'getBaseDirectory',
'getOutputNewline',
'getTime',
'get_Sherlock_args',
'get_directives_dict',
'get_leading_ws',
'get_line',
'get_line_after',
'getpreferredencoding',
'idleTimeHookHandler',
'importFromPath',
'initScriptFind',
'init_sherlock',
'init_trace',
'isUnicode',
'isValidEncoding',
'is_c_id',
'is_nl',
'is_special',
'is_ws',
'is_ws_or_nl',
'joinLines',
'listToString',
'makeAllNonExistentDirectories',
'makeDict',
'match',
'match_c_word',
'match_ignoring_case',
'match_word',
'module_date',
'openWithFileName',
'optimizeLeadingWhitespace',
'os_path_abspath',
'os_path_basename',
'os_path_dirname',
'os_path_exists',
'os_path_getmtime',
'os_path_isabs',
'os_path_isdir',
'os_path_isfile',
'os_path_join',
'os_path_norm',
'os_path_normcase',
'os_path_normpath',
'os_path_split',
'os_path_splitext',
'pause',
'plugin_date',
'plugin_signon',
'printDiffTime',
'printGc',
'printGcRefs',
'printGlobals',
'printLeoModules',
'print_bindings',
'print_stats',
'readlineForceUnixNewline',
'redirectStderr',
'redirectStdout',
'removeLeadingWhitespace',
'removeTrailingWs',
'reportBadChars',
'restoreStderr',
'restoreStdout',
'sanitize_filename',
'scanAtEncodingDirective',
'scanAtFileOptions',
'scanAtLineendingDirective',
'scanAtPagewidthDirective',
'scanAtRootOptions',
'scanAtTabwidthDirective',
'scanDirectives',
'scanError',
'scanf',
'set_delims_from_language',
'set_delims_from_string',
'set_language',
'shortFileName',
'skip_blank_lines',
'skip_block_comment',
'skip_braces',
'skip_c_id',
'skip_heredoc_string',
'skip_leading_ws',
'skip_leading_ws_with_indent',
'skip_line',
'skip_long',
'skip_matching_delims',
'skip_nl',
'skip_non_ws',
'skip_parens',
'skip_pascal_begin_end',
'skip_pascal_block_comment',
'skip_pascal_braces',
'skip_pascal_string',
'skip_php_braces',
'skip_pp_directive',
'skip_pp_if',
'skip_pp_part',
'skip_python_string',
'skip_string',
'skip_to_char',
'skip_to_end_of_line',
'skip_to_semicolon',
'skip_typedef',
'skip_ws',
'skip_ws_and_nl',
'splitLines',
'stat',
'stdErrIsRedirected',
'stdOutIsRedirected',
'toEncodedString',
'toUnicode',
'toUnicodeFileEncoding',
'top',
'trace',
'trace_tag',
'update_file_if_changed',
'utils_rename',
'windows',
'wrap_lines')</t>
<t tx="ekr.20041110104350"></t>
<t tx="ekr.20041114102139">@nocolor</t>
<t tx="ekr.20041114102139.1">- Several plugins show the docstring, so please take care to do a good job of
describing what the plugin does and how to use it.

- Please put the following immediately following the plugin's docstring.

    @language python
    @tabwidth -4

- There is no need to use sections if they are empty.

- The code should test whether modules have been imported only if those modules
may not be available on all platforms.

- Use following three lines only if your plugin uses a gui.

    if g.app.gui is None: 
        g.app.createTkGui(__file__)
    if g.app.gui.guiName() == "tkinter":
        ...

- Please use g.plugin_signon as shown, not leoPlugins.signon.</t>
<t tx="ekr.20041114102139.2">Please use the general format as shown in &lt;&lt; imports &gt;&gt;.  In partular:

- Please do _not_ assume that modules like Tkinter, Pmw, etc. are always available.
  Use g.importExtension.

- Good Python style is to put each import on a separate line.

- Please abbreviate Tkinter as Tk.  Please do NOT abbreviate Pmw or leoPlugins.

- Please do NOT use either of the following kinds of imports.
    from m import *
    from m import x,y,z

- Do not import leoNodes unless your plugin creates nodes directly.</t>
<t tx="ekr.20041114103913">Most of the comments in the style guide are comments _about_ the style guide.
You would replace these comments with your own, or eliminate them entirely in
your plugin.</t>
<t tx="ekr.20041114103913.1">PLEASE define each function or method in a separate node! To make this work,
just put @others in the root of your plugin as shown. Note that @others may be
nested, as shown in class myClass.</t>
<t tx="ekr.20041211035618"></t>
<t tx="ekr.20041215103252"></t>
<t tx="ekr.20050101090717">"""
mnplugins.py

mnplugins shows how to :
define new Commands  "insertOK" + "insertUser"
create Usermenu with new Commands

new Commands:
insertOK: 
    insert 'OK' in headline and a stamp in the first bodyline
    are there childnodes without 'OK' verhindern OK in actual node
    (insertOK on iconrclick2 too)

insertUser : Shift-F6
    insert a &lt;user/date/time&gt; stamp at the current location in bodytext
"""</t>
<t tx="ekr.20050101090717.1">import leoGlobals as g
import leoPlugins

import leoCommands
import time

Tk = g.importExtension('Tkinter',pluginName=__name__,verbose=True)</t>
<t tx="ekr.20050111122605"></t>
<t tx="ekr.20050126104457">@nocolor

https://sourceforge.net/forum/message.php?msg_id=2521345
By: bwmulder

I am working on a plugin which works with shadow files in a Leo subdirectory.

This is really the same code posted integrated with Leo. New is that
the goto linenumber command works properly as well.

The new code only kicks in if:
   - A leo subdirectory exists, and
   - both directories contain the file in question.
   
To get things started, create a Leo subdirectory, move the source
files there, and then create zero length strings instead of the moved
files. Whenever you change something in the sourcefile, both files
will be brought up to date automatically.

In the future, I might provide a script which provides this initial
setup automatically.

Implementation notes (relative to 4.1):

In order to use this mechanism to annotate foreign code, I am missing
two pieces:
   
   - The import command should import the source *exactly*.
   - I would like to add comments to the source which are *not* output into
source,
     and live in Leo only (or the shadowfile under Leo sentinel comments).
     
I changed the "message_comment" function to do nothing.

I do not think that this function is a good idea, since Leo can not know
if the line structure in a comment.

There might be more to do in this area.

It seems that I can get around the second limitation by writing "//@"
at the beginning of the line in the code sections, since this is
filtered away by the plugin.

Is there some other way to put comments only in the Leo document, but
not in the derived file?

I had to copy quite a bit of source code for the gotolinenr
command. It probably won't work for the next version of Leo

It seems that Leo somewhat encourages a coding style with long
routines, since complexity can be tugged away into subnodes rather
than creating functions to structure the code.

For the read and write command, I decided to inject a new "open"
function into the global namespace of leoAtFile.py. This function
checks if the caller is the read or write function of leoAtFile.py. In
this case, some special processing for synchronization is done.

I did this strange programming since I did not want to copy large
amounts of code and just add a few lines.

Currently the script works for C and python files. It looks at the
file extension to determine if C or python type annotations are
used. Maybe this information can be centralized.
</t>
<t tx="ekr.20050128070307"></t>
<t tx="ekr.20050217093214">@nocolor</t>
<t tx="ekr.20050227071948"></t>
<t tx="ekr.20050227071948.1">
- move the clone marker to the same place as the blue square
  content indicator. They can overlap.  Make room for annotations.
  



</t>
<t tx="ekr.20050227071948.2">
copy icons from freemind.

expandable box of icons at the head of a headline.
but manipulation vnode's iconx and icony positions.
vnode.computeIcon &amp; setIcon

icons in popup menus too ?

</t>
<t tx="ekr.20050227071948.3">
There seems to be a colour selector in leo.
</t>
<t tx="ekr.20050227071948.4"></t>
<t tx="ekr.20050227071948.5">
He haven't thought about it.
</t>
<t tx="ekr.20050227071948.6"></t>
<t tx="ekr.20050227071948.7"></t>
<t tx="ekr.20050227071948.8"></t>
<t tx="ekr.20050227071948.9"></t>
<t tx="ekr.20050227071948.10">
font
size
style
</t>
<t tx="ekr.20050227071948.11"></t>
<t tx="ekr.20050227071948.12"></t>
<t tx="ekr.20050227071948.13"></t>
<t tx="ekr.20050227071948.14">White or black on some Background
@file
@ignore
features
main branches


Automatically hilight @ nodes

</t>
<t tx="ekr.20050227071948.15"></t>
<t tx="ekr.20050227071948.16"></t>
<t tx="ekr.20050227071948.17">
Store semantics instead of colours.  Semantics then map to colours.


headline colours are reseted by the tree select and unselect methods.
maybe need to override them via the after (re)draw hook.


Offending Methods are all in leoTkinterTree.py
setNormalLabelState (self,v): # selected, editing
setDisabledLabelState (self,v): # selected, disabled
setUnselectedLabelState (self,v): # not selected.


</t>
<t tx="ekr.20050227071948.18">
Different coloured arrows for different priorities.

VeryHigh Red
High Orange
* Medium Green
Low Blue  (whatever)
Done  (tick)
</t>
<t tx="ekr.20050227071948.19">
archtetype based vnode attributes, not colour.
</t>
<t tx="ekr.20050227071948.20"></t>
<t tx="ekr.20050227071948.21">
The colouring conflicts.
</t>
<t tx="ekr.20050227071948.22"></t>
<t tx="ekr.20050227071948.23"></t>
<t tx="ekr.20050227071948.24">Not always predictable.

src/leoTkinterTree.py: menu.post(event.x_root, event.y_root)

</t>
<t tx="ekr.20050227071948.27">
# XXX merge: my model, coad &amp; de luca and holy trinity

# change colours: only foreground !
colour_table = {
    'interface': ["black", "OliveDrab2"],
    'logic':  ("black", "LightSkyBlue2"),
    'data':  ("black", "SandyBrown"),
    }

# Leo nodes.  Background hilite ?
Dead @ignore nodes + Documentat nodes  =&gt; Grey out
@File nodes, sub tree root

# Archetype Colouring

# Holy Trinity
Interface
Logic/Transform Centers/Functions
Data  =&gt; Description

# Coad and De Luca  --- Contrast against their meta-model
# It is a hiearchy going up from Description.
Description/Attributes/Data Catalog:  Purple
Party/Place/Thing:  Green
Role/Participation:  Yellow (Khaki or straw)
Moment/Interval/Event: Pink
Interface: White

# Me
Entity =&gt; Place or thing
  Core  =&gt;  Thing
  Interface =&gt;
  
Relationship (Loading and wiring code) =&gt; Moment(Init)
     =&gt; Special moment
     
* Interaction  =&gt; Moment/Interval + more !

# Unified : 5 Categories Max!!
Attributes, Data, Description, Lookup Tables.   =&gt; Brown
Entity Core, Place, Thing, Party    =&gt; Green
Logic, Pure Functions               =&gt; Blue
Role/Interface/Participation/Trait  =&gt; Straw/Khaki
Dynamic Stuff, Moment/Interaction   =&gt; Pinkish

</t>
<t tx="ekr.20050227071948.28">3. Various drawing hooks. I've restored the drawing hooks that used to exists. These are so-called "stub" hooks. The entries of these hooks in leoDocs.leo and leoPlugins.leo are as follows:
 
 tag argument keys in keywords
 (hook name) overrides when called dictionary argument
 --------- --------- ----------- -------------------
 ...
 "draw-outline-box" yes start of drawBox tree,p,v,x,y (note 6)
 "draw-outline-icon" yes start of tree.drawIcon tree,p,v,x,y (note 6)
 "draw-outline-node" yes start of tree.drawNode tree,p,v,x,y (note 6)
 "draw-outline-text-box" yes start of tree.drawText tree,p,v,x,y (note 6)
 "draw-sub-outline" yes start of tree.drawTree tree,p,v,x,y,h,level (note 6)
 ...
 
 These probably work exactly as the old hooks did, though I didn't use the old (4.0?) code as a base. The only change is the new p keyword argument. In all cases v = p.v. I probably should a p keyword argument to most other hooks, and I'm lazy...
 
 Warning: all these hooks "override" the existing code, which doesn't get executed if the hook returns anything except None. This means that the hook had better return what the "host" code returns, and this has changed recently to support user icons, and may change in the future as needed.
 
 For example, here is the code in drawNode
 
 data = g.doHook("draw-outline-node",tree=tree,p=p,v=v,x=x,y=y)
 if data is not None: return data
 
 At present, drawNode typically returns what return force_draw_node returns, which is a tuple (h,xw). This is needed to support icons of various sizes.
 
 In short, I'm not real sure how useful these hooks are going to be, or how stable.
 

</t>
<t tx="ekr.20050227071948.29">
add the colour menu to rclickhead1


 "draw-outline-box" yes start of drawBox tree,p,v,x,y (note 6)
    It works, but not sure when it is called.

 "draw-outline-icon" yes start of tree.drawIcon tree,p,v,x,y (note 6)
    The box obscures it.  If True is return, rlick wont work anymore.

 "draw-outline-node" yes start of tree.drawNode tree,p,v,x,y (note 6)
    This calls -icon and -box ?
 "draw-outline-text-box" yes start of tree.drawText tree,p,v,x,y (note 6)
    Does not obscure the box area !!

 "draw-sub-outline" yes start of tree.drawTree tree,p,v,x,y,h,level (note 6)
     Use this for head highlighting ? Probally called after the node is draw
     but before drawing the children.
yay ! they work with the CVS version.

@c

#registerHandler("draw-outline-box", draw0)
#registerHandler("draw-outline-node", draw0)
#registerHandler("draw-outline-text-box", draw0)

#registerHandler("iconrclick1",show_colour_menu)
</t>
<t tx="ekr.20050227072121"></t>
<t tx="ekr.20050303051035">@

Note: the newButtons.py now has templates for the following plugin nodes.
    
- init: A generic init function.
- init(tk): An init function for a plugin that uses Tk (or Pmw).
- &lt;&lt; imports &gt;&gt;:  The &lt;&lt;imports&gt;&gt; section.
- &lt;&lt; version history &gt;&gt;: The &lt;&lt;version history&gt;&gt; section.</t>
<t tx="ekr.20050303051035.2">&lt;&lt; docstring &gt;&gt;

__version__ = '0.0'
&lt;&lt; version history &gt;&gt;

&lt;&lt; imports &gt;&gt;

@others</t>
<t tx="ekr.20050303051035.3">'''This docstring should be a clear, concise description of
what the plugin does and how to use it.
'''
</t>
<t tx="ekr.20050303051035.4">@killcolor
@

Put notes about each version here.</t>
<t tx="ekr.20050303051035.5">import leoGlobals as g
import leoPlugins

Pmw = g.importExtension('Pmw',    pluginName=__name__,verbose=True,required=True)
Tk  = g.importExtension('Tkinter',pluginName=__name__,verbose=True,required=True)

# Whatever other imports your plugins uses.</t>
<t tx="ekr.20050303051101">def init ():
    
    ok = Pmw and Tk
    
    if ok:
        if g.app.gui is None:
            g.app.createTkGui(__file__)
            
        ok = g.app.gui.guiName() == "tkinter"

        if ok:
            if 1: # Use this if you want to create the commander class before the frame is fully created.
                leoPlugins.registerHandler('before-create-leo-frame',onCreate)
            else: # Use this if you want to create the commander class after the frame is fully created.
                leoPlugins.registerHandler('after-create-leo-frame',onCreate)
            g.plugin_signon(__name__)
        
    return ok</t>
<t tx="ekr.20050303051150">def onCreate (tag, keys):
    
    c = keys.get('c')
    if not c: return
    
    thePluginController = pluginController(c)</t>
<t tx="ekr.20050303051222">class pluginController:
    
    @others</t>
<t tx="ekr.20050303051222.1">def __init__ (self,c):
    
    self.c = c
    # Warning: hook handlers must use keywords.get('c'), NOT self.c.</t>
<t tx="ekr.20050303080042"></t>
<t tx="ekr.20050303080042.1">[Main]

RefreshInterval = 60
ColdColour = blue
HotColour = red
HitsToHeatUp = 2
</t>
<t tx="ekr.20050303080236">@killcolor

- Crashes if .ini file does not exist.</t>
<t tx="ekr.20050306071540">def onStart2 (tag, keywords):
    
    """
    Showing how to define a global hook that affects all commanders.
    """

    import leoTkinterFrame
    log = leoTkinterFrame.leoTkinterLog
    
    # Replace frame.put with newPut (not shown).
    g.funcToMethod(newPut,log,"put")</t>
<t tx="ekr.20050306071629">&lt;&lt; docstring &gt;&gt;

__version__ = '0.0'
&lt;&lt; version history &gt;&gt;

&lt;&lt; imports &gt;&gt;

@others</t>
<t tx="ekr.20050306071629.1">'''This docstring should be a clear, concise description of
what the plugin does and how to use it.
'''
</t>
<t tx="ekr.20050306071629.2">@killcolor
@

Put notes about each version here.</t>
<t tx="ekr.20050306071629.3">import leoGlobals as g
import leoPlugins

# Whatever other imports your plugins uses.</t>
<t tx="ekr.20050306071629.4">def init ():
    
    ok = True # This might depend on imports, etc.
    
    if ok:
        leoPlugins.registerHandler('start2',onStart2)
        g.plugin_signon(__name__)
        
    return ok</t>
<t tx="ekr.20050306072156">It is usually best _not_ to catch exceptions in plugins:
doHook catches all exceptions and disables further calls to plugins.

If a plugin catches exceptions during startup it should do one of the following:
    
- raise the exception again.
- provide an init function at the top level that reports the failure.</t>
<t tx="ekr.20050306081349"></t>
<t tx="ekr.20050328101812"> 
        
        
        </t>
<t tx="ekr.20050328101812.1"></t>
<t tx="ekr.20050328101812.2"></t>
<t tx="ekr.20050328101812.3"></t>
<t tx="ekr.20050329082101"></t>
<t tx="ekr.20050329082101.1">@nocolor</t>
<t tx="ekr.20050329082101.2">The AutoTrees plugin is a helper plugin designed to make it very easy to write "hanlder" plugins to manage dynamic content in Leo outlines. 

AutoTrees provides 

- convenient handler base classes which can be specialized for particular uses
- a manager to turn handlers on and off
- a set of example handlers to show the kinds of things that are possible

AutoTrees doesn't do anything that you cannot do in other ways, but it does provide a consistent way of adding dynamic content. This means that individual plugin writers don't have to rewrite all the same kinds of code each time and also makes it easier to maintain Leo, since it standardizes the way that certain classes of plugin interact with the Leo core.

</t>
<t tx="ekr.20050329082101.3">I'm a plugin writer and I want to write a plugin to display dynamic content - ie content not directly contained in the .leo or derived files, eg

- email messages 
- news feeds
- news groups
- documentation
- remote files
- statistics
- file system data
- data base records

You can do this as a standard plugin, but as an AutoTrees handler you,

- don't need to write code that interacts with the tree (this is done for you)
- get centralized management
- can still do everything else you could as a normal plugin

</t>
<t tx="ekr.20050329082101.4">AutoTrees is itself a plugin. When it starts it,

1. Scans the leo\plugins\trees folder to find handlers
2. Activates specific handlers (this is managed via a plugin manager type window)
3. Waits for clicks and double-clicks on special nodes

To create an AutoTree node, you add a node with @auto-my_handler. The @auto tells the plugin to go and look for the "my_handler" handler, if it is enabled. The handler is then called and this is then used to populate the node body and child nodes below this node.

eg, for an @auto-rss node, the node headline is "@auto-rss http://myurl/news.xml". The handler goes to the URL mentioned and downloads the news stories. It then creates child nodes for each story and populates the bodies. 

The handler doesn't have to worry about interacting with the Leo tree view, it just returns a tree object. 

</t>
<t tx="ekr.20050329082101.5">The best way is to use the existing examples as templates. Look at the "test" handler first as this is the "Hello world" of trees.

</t>
<t tx="ekr.20050329082101.6">@nocolor</t>
<t tx="ekr.20050329082101.7">Just some simple testing nodes</t>
<t tx="ekr.20050329082101.8"></t>
<t tx="ekr.20050329082101.9">this is one</t>
<t tx="ekr.20050329082101.10">this is two !!!</t>
<t tx="ekr.20050329082101.11">this is three</t>
<t tx="ekr.20050329082101.12"></t>
<t tx="ekr.20050329082101.13"></t>
<t tx="ekr.20050329082101.14"></t>
<t tx="ekr.20050329082101.15">Reads a remote news service.

@auto-rss &lt;url to news service&gt;

Requires feedparser installed:
    http://sourceforge.net/projects/feedparser/</t>
<t tx="ekr.20050329082101.16">title

summary_detail</t>
<t tx="ekr.20050329082101.40">title (slash_section, category)

summary_detail

link</t>
<t tx="ekr.20050329082101.51">title (modified)

link</t>
<t tx="ekr.20050329082101.52">Python 2.4.1 (release candhttp://www.python.org/2.4.1/index.htmlate 1) (2005-03-10)

http://www.python.org/2.4.1/index.html</t>
<t tx="ekr.20050329082101.53">Greg Stein, of Google and Apache Software Foundation, to deliver keynote at PyCon (2005-03-06)

http://www.python.org/pycon/2005/keynotes.html</t>
<t tx="ekr.20050329082101.54">New RSS feed for python-dev summaries (2005-02-24)

http://www.python.org/dev/summary/channews.rdf</t>
<t tx="ekr.20050329082101.55">Guhttp://www.sdforum.org/SDForum/Templates/CalendarEvent.aspx?CID=1547&amp;mo=2&amp;yr=2005o van Rossum speaking in Palo Alto (2005-02-17)

http://www.sdforum.org/SDForum/Templates/CalendarEvent.aspx?CID=1547&amp;mo=2&amp;yr=2005</t>
<t tx="ekr.20050329082101.56">Python 2.3.5 (final) (2005-02-08)

http://www.python.org/2.3.5/index.html</t>
<t tx="ekr.20050329082101.57">Security advisory for SimpleXMLRPCServer.py. (2005-02-03)

http://python.org/security/PSF-2005-001/</t>
<t tx="ekr.20050329082101.58">Deadline for OSCON proposals (2005-02-01)

http://mail.python.org/pipermail/python-announce-list/2005-January/003683.html</t>
<t tx="ekr.20050329082101.59">PyCon abstracts now available (2005-01-23)

http://www.python.org/moin/PyConDC2005/Presentations</t>
<t tx="ekr.20050329082101.60">PyCon preliminary schedule now available (2005-01-20)

http://www.python.org/pycon/2005/schedule.html</t>
<t tx="ekr.20050329082101.61">PSF has awarded three grants (2004-12-30)

http://www.python.org/psf/grants/index.html</t>
<t tx="ekr.20050329082101.62">Python for Nokia Series 60 now available (2004-12-23)

http://www.forum.nokia.com/main/0,,034-821,00.html</t>
<t tx="ekr.20050329082101.63">Python 2.4 (final) (2004-11-30)

http://www.python.org/2.4/index.html</t>
<t tx="ekr.20050329082101.64">PyZine issue 7 (2004-11-23)

http://www.pyzine.com/Issue007/</t>
<t tx="ekr.20050329082101.65">PyCon 2005 Call for Proposals (2004-10-23)

http://www.python.org/pycon/2005/cfp.html</t>
<t tx="ekr.20050329082101.66">Cameron Laird receives the Frank Willison Award (2004-10-18)

http://press.oreilly.com/pub/pr/1237</t>
<t tx="ekr.20050329082101.67">Reads a remote file

@auto-remote &lt;url to file&gt;

Requires pyCurl:
    http://pycurl.sourceforge.net/</t>
<t tx="ekr.20050329082101.68">&lt;!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN"&gt;
&lt;html&gt;
&lt;head&gt;
&lt;title&gt;BBC - Error 404: Page not found&lt;/title&gt;
&lt;meta name="description" content="Error 404 - page not found" /&gt;
&lt;meta name="keywords" content="" /&gt;
&lt;meta name="created" content="20040506" /&gt;
&lt;meta name="updated" content="20040506" /&gt;
&lt;base href="http://www.bbc.co.uk" /&gt;
&lt;style&gt;
body {margin:0; padding:0;}
em {color:#900;}
p, ul {font-size:80%}
h4,h3,h2,h1,p, ul {font-family: verdana,arial,helvetica,sans-serif;}
h4,h3 {font-size:100%}
h4,h1 {margin:0}
div.main {padding:8px;margin:0px;width:770;}
form {margin:0;padding:0;}
&lt;/style&gt;
&lt;/head&gt;
&lt;body bgcolor="#ffffff" link="#333366" text="#000000" vlink="#333366" alink="#000000" marginheight="0" marginwidth="0"&gt;

&lt;!-- toolbar 1.4 toolbar.page 770 666666 --&gt;&lt;table width="100%" cellpadding="0" cellspacing="0" border="0"&gt;&lt;tr&gt;&lt;td colspan="2" style="background-color:#828282;" &gt;&lt;a name="top"&gt;&lt;img src="/f/t.gif" width="590" height="2" alt="" /&gt;&lt;/a&gt;&lt;/td&gt;&lt;td style="background-color:#828282;"&gt;&lt;img src="/f/t.gif" width="1" height="2" alt="" /&gt;&lt;/td&gt;&lt;/tr&gt;&lt;form action="http://www.bbc.co.uk/cgi-bin/search/results.pl"&gt;&lt;tr&gt;&lt;td style="border-left:2px solid #828282;background-color:#999999;" width="54"&gt;&lt;a href="http://www.bbc.co.uk/go/toolbar/-/"&gt;&lt;img src="/images/logo04.gif" width="50" height="20" alt="BBC" border="0" hspace="2" vspace="5" /&gt;&lt;/a&gt;&lt;/td&gt;&lt;td style="background:#999999;" align="right"&gt;&lt;table cellpadding="0" cellspacing="0" border="0" style="float:right;"&gt;&lt;tr&gt;&lt;td style="background:#999999;"&gt;&lt;font size="1"&gt;&lt;b&gt;&lt;a href="http://www.bbc.co.uk/go/toolbar/text/-/" style="color:#ffffff;text-decoration:none;font-family:verdana,arial,helvetica,sans-serif;padding:1px 4px;"&gt;Home&lt;/a&gt;&lt;/b&gt;&lt;/font&gt;&lt;/td&gt;&lt;td style="background:#999999 url(/images/v.gif) repeat-y;" width="6"&gt;&lt;br /&gt;&lt;/td&gt;&lt;td&gt;&lt;font size="1"&gt;&lt;b&gt;&lt;a href="/go/toolbar/-/tv/" style="color:#ffffff;text-decoration:none;font-family:verdana,arial,helvetica,sans-serif;padding:1px 4px;"&gt;TV&lt;/a&gt;&lt;/b&gt;&lt;/font&gt;&lt;/td&gt;&lt;td style="background:#999999 url(/images/v.gif) repeat-y;" width="6"&gt;&lt;br /&gt;&lt;/td&gt;&lt;td&gt;&lt;font size="1"&gt;&lt;b&gt;&lt;a href="/go/toolbar/-/radio/" style="color:#ffffff;text-decoration:none;font-family:verdana,arial,helvetica,sans-serif;padding:1px 4px;"&gt;Radio&lt;/a&gt;&lt;/b&gt;&lt;/font&gt;&lt;/td&gt;&lt;td style="background:#999999 url(/images/v.gif) repeat-y;" width="6"&gt;&lt;br /&gt;&lt;/td&gt;&lt;td&gt;&lt;font size="1"&gt;&lt;b&gt;&lt;a href="/go/toolbar/-/talk/" style="color:#ffffff;text-decoration:none;font-family:verdana,arial,helvetica,sans-serif;padding:1px 4px;"&gt;Talk&lt;/a&gt;&lt;/b&gt;&lt;/font&gt;&lt;/td&gt;&lt;td style="background:#999999 url(/images/v.gif) repeat-y;" width="6"&gt;&lt;br /&gt;&lt;/td&gt;&lt;td&gt;&lt;font size="1"&gt;&lt;b&gt;&lt;a href="/go/toolbar/-/whereilive/" style="color:#ffffff;text-decoration:none;font-family:verdana,arial,helvetica,sans-serif;padding:1px 4px;"&gt;Where&amp;nbsp;I&amp;nbsp;Live&lt;/a&gt;&lt;/b&gt;&lt;/font&gt;&lt;/td&gt;&lt;td style="background:#999999 url(/images/v.gif) repeat-y;" width="6"&gt;&lt;br /&gt;&lt;/td&gt;&lt;td&gt;&lt;nobr&gt;&lt;font size="1"&gt;&lt;b&gt;&lt;a href="/go/toolbar/-/a-z/" style="color:#ffffff;text-decoration:none;font-family:verdana,arial,helvetica,sans-serif;padding:1px 4px;"&gt;A-Z&amp;nbsp;Index&lt;/a&gt;&lt;/b&gt;&lt;/font&gt;&lt;/nobr&gt;&lt;/td&gt;&lt;td style="background:#666666 url(/images/sl3.gif) no-repeat;" width="8"&gt;&lt;br /&gt;&lt;/td&gt;&lt;td style="background:#666666 url(/images/st.gif) repeat-x 0 0;"&gt;&lt;input type="text" id="bbcpageSearchbox" name="q" size="6" style="margin:3px 0 0;font-family:arial,helvetica,sans-serif;width:100px;" title="BBC Search" /&gt;&lt;/td&gt;&lt;td style="background:#666666 url(/images/st.gif) repeat-x;"&gt;&lt;input type="image" src="/images/srchb.gif" name="go" value="go" alt="Search" width="64" height="25" border="0" /&gt;&lt;/td&gt;&lt;td style="background:#999999 url(/images/sra.gif) no-repeat;" width="1"&gt;&lt;img src="/f/t.gif" width="1" height="30" alt="" /&gt;&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;&lt;/td&gt;&lt;td style="background:#999999 url(/images/srb.gif) no-repeat;"&gt;&lt;img src="/f/t.gif" width="1" height="1" alt="" /&gt;&lt;input type="hidden" name="uri" value="/news.html" /&gt;&lt;/td&gt;&lt;/tr&gt;&lt;/form&gt;&lt;tr&gt;&lt;td colspan="2" style="background-color:#000000;"&gt;&lt;img src="/f/t.gif" width="770" height="1" alt="" /&gt;&lt;/td&gt;&lt;td width="100%" style="background-color:#000000;"&gt;&lt;img src="/f/t.gif" width="1" height="1" alt="" /&gt;&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;&lt;!-- end toolbar 1.4 --&gt;

&lt;table cellspacing="0" cellpadding="8" border="0" width="770" bgcolor="#cccccc"&gt;&lt;tr&gt;&lt;td width="335"&gt;&lt;font size="-2" face="arial,helvetica"&gt;TUESDAY&lt;br /&gt;29th March 2005&lt;br /&gt;&lt;a href="/cgi-bin/education/betsie/parser.pl"&gt;Text only&lt;/a&gt; &lt;/font&gt;&lt;/td&gt;&lt;td width="435"&gt;&lt;h1&gt;404&lt;/h1&gt;&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;
&lt;div class="main"&gt;
&lt;div align="center"&gt;
&lt;h2&gt;Page not found&lt;/h2&gt;
&lt;p&gt;Unfortunately the following page was not available:&lt;br /&gt;
&lt;em&gt;http://www.bbc.co.uk/news.html&lt;/em&gt;&lt;/p&gt;
&lt;/div&gt;
&lt;h3&gt;This might be because:&lt;/h3&gt;
&lt;ul&gt;&lt;li&gt;You may have typed the web address incorrectly. Please check the address and spelling ensuring that it does &lt;b&gt;not&lt;/b&gt; contain capital letters or spaces&lt;/li&gt;
&lt;li&gt;It is possible that the page you were looking for may have been moved, updated or deleted.&lt;/li&gt;&lt;/ul&gt;

&lt;h3&gt;Please try the following options instead:&lt;/h3&gt;

&lt;form action="/cgi-bin/search/results.pl"&gt;
&lt;table cellpadding="4" cellspacing="2" border="0" align="center" bgcolor="#000000"&gt;
&lt;tr&gt;&lt;td bgcolor="#99ccff"&gt;&lt;h4&gt;Search bbc.co.uk&lt;/h4&gt;&lt;/td&gt;&lt;/tr&gt;
&lt;tr&gt;&lt;td bgcolor="#ffffcc"&gt;&lt;input type="text" name="q" size="45" /&gt;&amp;nbsp;&lt;input type="submit" value="Go" /&gt;&lt;/td&gt;&lt;/tr&gt;
&lt;/table&gt;
&lt;/form&gt;

&lt;ul&gt;
&lt;li&gt;Return to the &lt;a href="/"&gt;bbc.co.uk Home Page&lt;/a&gt;&lt;/li&gt;
&lt;li&gt;Use our &lt;a href="/a-z/"&gt;site index&lt;/a&gt;&lt;/li&gt;
&lt;li&gt;If you still encounter problems then please try the &lt;a href="/help/"&gt;help&lt;/a&gt; section.&lt;/li&gt;
&lt;/ul&gt;

&lt;/div&gt;
&lt;!-- inc.footer.page --&gt;&lt;br clear="all" /&gt;&lt;table width="770" cellpadding="0" cellspacing="0" border="0"&gt;&lt;tr&gt;&lt;td width="110"&gt;&lt;img src="/furniture/tiny.gif" alt="" width="110" height="1"&gt;&lt;/td&gt;&lt;td width="10"&gt;&lt;img src="/furniture/tiny.gif" alt="" width="10" height="1"&gt;&lt;/td&gt;&lt;td align="center" width="100%"&gt;&lt;font face="arial, helvetica, sans-serif" size="1"&gt;&lt;a href="/terms/"&gt;Terms of Use&lt;/a&gt; | &lt;a href="/privacy/"&gt;Privacy&lt;/a&gt;&lt;/font&gt;&lt;/td&gt;&lt;/tr&gt;&lt;/table&gt;&lt;!-- end inc.footer.page --&gt;

&lt;/body&gt;
&lt;/html&gt;
</t>
<t tx="ekr.20050329082101.69">Produces documentation for a module

@auto-doc &lt;module name&gt;</t>
<t tx="ekr.20050329082101.70"></t>
<t tx="ekr.20050329082101.71">Base class for Docutils components.</t>
<t tx="ekr.20050329082101.72"></t>
<t tx="ekr.20050329082101.73">tuple() -&gt; an empty tuple
tuple(sequence) -&gt; tuple initialized from sequence's items

If the argument is a tuple, the return value is the same object.</t>
<t tx="ekr.20050329082101.74">
        Is `format` supported by this component?

        To be used by transforms to ask the dependent component if it supports
        a certain input context or output format.
        </t>
<t tx="ekr.20050329082101.75"></t>
<t tx="ekr.20050329082101.76">No documentation for OPTCRE</t>
<t tx="ekr.20050329082101.77">No documentation for SECTCRE</t>
<t tx="ekr.20050329082101.78">Create a new section in the configuration.

        Raise DuplicateSectionError if a section by the specified name
        already exists.
        </t>
<t tx="ekr.20050329082101.79">tuple() -&gt; an empty tuple
tuple(sequence) -&gt; tuple initialized from sequence's items

If the argument is a tuple, the return value is the same object.</t>
<t tx="ekr.20050329082101.80">dict() -&gt; new empty dictionary.
dict(mapping) -&gt; new dictionary initialized from a mapping object's
    (key, value) pairs.
dict(seq) -&gt; new dictionary initialized as if via:
    d = {}
    for k, v in seq:
        d[k] = v
dict(**kwargs) -&gt; new dictionary initialized with the name=value pairs
    in the keyword argument list.  For example:  dict(one=1, two=2)</t>
<t tx="ekr.20050329082101.81">
    Parser for command-line and library use.  The `settings_spec`
    specification here and in other Docutils components are merged to build
    the set of command-line options and runtime settings for this process.

    Common settings (defined below) and component-specific settings must not
    conflict.  Short options are reserved for common settings, and components
    are restrict to using long options.
    </t>
<t tx="ekr.20050329082101.82">str(object) -&gt; string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.</t>
<t tx="ekr.20050329082101.83">tuple() -&gt; an empty tuple
tuple(sequence) -&gt; tuple initialized from sequence's items

If the argument is a tuple, the return value is the same object.</t>
<t tx="ekr.20050329082101.84">dict() -&gt; new empty dictionary.
dict(mapping) -&gt; new dictionary initialized from a mapping object's
    (key, value) pairs.
dict(seq) -&gt; new dictionary initialized as if via:
    d = {}
    for k, v in seq:
        d[k] = v
dict(**kwargs) -&gt; new dictionary initialized with the name=value pairs
    in the keyword argument list.  For example:  dict(one=1, two=2)</t>
<t tx="ekr.20050329082101.85">tuple() -&gt; an empty tuple
tuple(sequence) -&gt; tuple initialized from sequence's items

If the argument is a tuple, the return value is the same object.</t>
<t tx="ekr.20050329082101.86">list() -&gt; new list
list(sequence) -&gt; new list initialized from sequence's items</t>
<t tx="ekr.20050329082101.87">list() -&gt; new list
list(sequence) -&gt; new list initialized from sequence's items</t>
<t tx="ekr.20050329082101.88">dict() -&gt; new empty dictionary.
dict(mapping) -&gt; new dictionary initialized from a mapping object's
    (key, value) pairs.
dict(seq) -&gt; new dictionary initialized as if via:
    d = {}
    for k, v in seq:
        d[k] = v
dict(**kwargs) -&gt; new dictionary initialized with the name=value pairs
    in the keyword argument list.  For example:  dict(one=1, two=2)</t>
<t tx="ekr.20050329082101.89">str(object) -&gt; string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.</t>
<t tx="ekr.20050329082101.90">
    A facade encapsulating the high-level logic of a Docutils system.
    </t>
<t tx="ekr.20050329082101.91">str(object) -&gt; string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.</t>
<t tx="ekr.20050329082101.92">str(object) -&gt; string

Return a nice string representation of the object.
If the argument is a string, the return value is the same object.</t>
<t tx="ekr.20050329082101.93">
Command-line and common processing for Docutils front-end tools.

Exports the following classes:

- `OptionParser`: Standard Docutils command-line processing.
- `Values`: Runtime settings; objects are simple structs
  (``object.attribute``).
- `ConfigParser`: Standard Docutils config file processing.
</t>
<t tx="ekr.20050329082101.94">
I/O classes provide a uniform API for low-level input and output.  Subclasses
will exist for a variety of input/output mechanisms.
</t>
<t tx="ekr.20050329082101.95">
This package contains Docutils parser modules.
</t>
<t tx="ekr.20050329082101.96">
    Set up &amp; run a `Publisher`.  For command-line front ends.

    Parameters:

    - `reader`: A `docutils.readers.Reader` object.
    - `reader_name`: Name or alias of the Reader class to be instantiated if
      no `reader` supplied.
    - `parser`: A `docutils.parsers.Parser` object.
    - `parser_name`: Name or alias of the Parser class to be instantiated if
      no `parser` supplied.
    - `writer`: A `docutils.writers.Writer` object.
    - `writer_name`: Name or alias of the Writer class to be instantiated if
      no `writer` supplied.
    - `settings`: Runtime settings object.
    - `settings_spec`: Extra settings specification; a `docutils.SettingsSpec`
      subclass.  Used only if no `settings` specified.
    - `settings_overrides`: A dictionary containing program-specific overrides
      of component settings.
    - `enable_exit`: Boolean; enable exit status at end of processing?
    - `argv`: Command-line argument list to use instead of ``sys.argv[1:]``.
    - `usage`: Usage string, output if there's a problem parsing the command
      line.
    - `description`: Program description, output for the "--help" option
      (along with command-line option descriptions).
    </t>
<t tx="ekr.20050329082101.97">
    Set up &amp; run a `Publisher`.  For programmatic use with file-like I/O.

    Parameters:

    - `source`: A file-like object (must have "read" and "close" methods).
    - `source_path`: Path to the input file.  Opened if no `source` supplied.
      If neither `source` nor `source_path` are supplied, `sys.stdin` is used.
    - `destination`: A file-like object (must have "write" and "close"
      methods).
    - `destination_path`: Path to the input file.  Opened if no `destination`
      supplied.  If neither `destination` nor `destination_path` are supplied,
      `sys.stdout` is used.
    - `reader`: A `docutils.readers.Reader` object.
    - `reader_name`: Name or alias of the Reader class to be instantiated if
      no `reader` supplied.
    - `parser`: A `docutils.parsers.Parser` object.
    - `parser_name`: Name or alias of the Parser class to be instantiated if
      no `parser` supplied.
    - `writer`: A `docutils.writers.Writer` object.
    - `writer_name`: Name or alias of the Writer class to be instantiated if
      no `writer` supplied.
    - `settings`: Runtime settings object.
    - `settings_spec`: Extra settings specification; a `docutils.SettingsSpec`
      subclass.  Used only if no `settings` specified.
    - `settings_overrides`: A dictionary containing program-specific overrides
      of component settings.
    - `enable_exit`: Boolean; enable exit status at end of processing?
    </t>
<t tx="ekr.20050329082101.98">
    Set up &amp; run a `Publisher`, and return the string output.
    For programmatic use with string I/O.

    For encoded string output, be sure to set the "output_encoding" setting to
    the desired encoding.  Set it to "unicode" for unencoded Unicode string
    output.  Here's how::

        publish_string(..., settings_overrides={'output_encoding': 'unicode'})

    Similarly for Unicode string input (`source`)::

        publish_string(..., settings_overrides={'input_encoding': 'unicode'})

    Parameters:

    - `source`: An input string; required.  This can be an encoded 8-bit
      string (set the "input_encoding" setting to the correct encoding) or a
      Unicode string (set the "input_encoding" setting to "unicode").
    - `source_path`: Path to the file or object that produced `source`;
      optional.  Only used for diagnostic output.
    - `destination_path`: Path to the file or object which will receive the
      output; optional.  Used for determining relative paths (stylesheets,
      source links, etc.).
    - `reader`: A `docutils.readers.Reader` object.
    - `reader_name`: Name or alias of the Reader class to be instantiated if
      no `reader` supplied.
    - `parser`: A `docutils.parsers.Parser` object.
    - `parser_name`: Name or alias of the Parser class to be instantiated if
      no `parser` supplied.
    - `writer`: A `docutils.writers.Writer` object.
    - `writer_name`: Name or alias of the Writer class to be instantiated if
      no `writer` supplied.
    - `settings`: Runtime settings object.
    - `settings_spec`: Extra settings specification; a `docutils.SettingsSpec`
      subclass.  Used only if no `settings` specified.
    - `settings_overrides`: A dictionary containing program-specific overrides
      of component settings.
    - `enable_exit`: Boolean; enable exit status at end of processing?
    </t>
<t tx="ekr.20050329082101.99">
This package contains Docutils Reader modules.
</t>
<t tx="ekr.20050329082101.100">This module provides access to some objects used or maintained by the
interpreter and to functions that interact strongly with the interpreter.

Dynamic objects:

argv -- command line arguments; argv[0] is the script pathname if known
path -- module search path; path[0] is the script directory, else ''
modules -- dictionary of loaded modules

displayhook -- called to show results in an interactive session
excepthook -- called to handle any uncaught exception other than SystemExit
  To customize printing in an interactive session or to install a custom
  top-level exception handler, assign other functions to replace these.

exitfunc -- if sys.exitfunc exists, this routine is called when Python exits
  Assigning to sys.exitfunc is deprecated; use the atexit module instead.

stdin -- standard input file object; used by raw_input() and input()
stdout -- standard output file object; used by the print statement
stderr -- standard error object; used for error messages
  By assigning other file objects (or objects that behave like files)
  to these, it is possible to redirect all of the interpreter's I/O.

last_type -- type of last uncaught exception
last_value -- value of last uncaught exception
last_traceback -- traceback of last uncaught exception
  These three are only available in an interactive session after a
  traceback has been printed.

exc_type -- type of exception currently being handled
exc_value -- value of exception currently being handled
exc_traceback -- traceback of exception currently being handled
  The function exc_info() should be used instead of these three,
  because it is thread-safe.

Static objects:

maxint -- the largest supported integer (the smallest is -maxint-1)
maxunicode -- the largest supported character
builtin_module_names -- tuple of module names built into this interpreter
version -- the version of this interpreter as a string
version_info -- version information as a tuple
hexversion -- version information encoded as a single integer
copyright -- copyright notice pertaining to this interpreter
platform -- platform identifier
executable -- pathname of this Python interpreter
prefix -- prefix used to find the Python library
exec_prefix -- prefix used to find the machine-specific Python library
dllhandle -- [Windows only] integer handle of the Python DLL
winver -- [Windows only] version number of the Python DLL
__stdin__ -- the original stdin; don't touch!
__stdout__ -- the original stdout; don't touch!
__stderr__ -- the original stderr; don't touch!
__displayhook__ -- the original displayhook; don't touch!
__excepthook__ -- the original excepthook; don't touch!

Functions:

displayhook() -- print an object to the screen, and save it in __builtin__._
excepthook() -- print an exception and its traceback to sys.stderr
exc_info() -- return thread-safe information about the current exception
exc_clear() -- clear the exception state for the current thread
exit() -- exit the interpreter by raising SystemExit
getdlopenflags() -- returns flags to be used for dlopen() calls
getrefcount() -- return the reference count for an object (plus one :-)
getrecursionlimit() -- return the max recursion depth for the interpreter
setcheckinterval() -- control how often the interpreter checks for events
setdlopenflags() -- set the flags to be used for dlopen() calls
setprofile() -- set the global profiling function
setrecursionlimit() -- set the max recursion depth for the interpreter
settrace() -- set the global debug tracing function
</t>
<t tx="ekr.20050329082101.101">
This package contains Docutils Writer modules.
</t>
<t tx="ekr.20050329082101.102"></t>
<t tx="ekr.20050329082101.103">Reads messages from a news server. Only does the last 10 as this is very slow ... it is only meant as an example. 

@auto-news &lt;news server name&gt;/&lt;news group name&gt;

</t>
<t tx="ekr.20050329082101.104">

Given some Python source, is there any tool which can tell the mimimum 
level of Python required to run that source? If I distribute some code, 
I need to be able to say which level of Python users require to run it.

-- 
Steve Toledo-Brown
Speaking for myself only.
Humans please use domain uk.ibm.com</t>
<t tx="ekr.20050329082101.105">

Disclaimer #1: I am a Python newbie, and I appreciate the vast
documentation at python.org -- some of which I expect has the answer to
my question if I can find it.

I am working on a custom computational fluid dynamics code.  I will
create one or more compiled Python modules in C/C++ to provide new
types and functions for manipulating those types.  I have a *lot* of
data.  Efficiency requires that the new data structures be shared
freely within the scope of the module, without directly exposing the
data to the standard Python runtime environment.

Stated another way, I need the data to persist in virtual memory across
seprate invocations of functions in the module(s) and to be accessible
only through methods explicitly provided by the module(s).

How can I do this?  What are some good examples to study?

Disclaimer #2: I am a aware that strong opinions exist about closing
off data from users.  But it's a requirement for this application.  I
don't like it, but I need the job!

Thanks for your time
CatManDo
</t>
<t tx="ekr.20050329082101.106">

Anand S Bisen wrote:
&gt; Hello
&gt; 
&gt; I have been developing a code that works pretty well on my python 2.3 
&gt; and now when i am running it on my server where it is programmed to run 
&gt; it's giving me errors. I have been using __contains__ method and it 
&gt; fails on python 2.2
&gt; 
&gt; For example
&gt; 
&gt; (Python 2.3)
&gt;  &gt;&gt; x="Hello World"
&gt;  &gt;&gt; print x.__contains__("Hello")
&gt; True
&gt; 
&gt; (Python 2.2)
&gt; 
&gt;  &gt;&gt;&gt; x="Hello world"
&gt;  &gt;&gt;&gt; print x.__contains__("Hello")
&gt; 
&gt; Traceback (most recent call last):
&gt;  File "&lt;stdin&gt;", line 1, in ?
&gt; TypeError: 'in &lt;string&gt;' requires character as left operand
&gt; 
&gt; 
&gt; Is there any woraround for this or what am i doing wrong in 2.2 ?
&gt; 
&gt; Thanks
&gt; 
Any use of double-underscores is an indication that magic is at work. In 
this case the __contains__ method is intended to be called by the 
interpreter when you write

     x in s

The __contains__ method was extended for strings in 2.3 so that 
construct could be used as a test to see whether s contained x as a 
substring. Before that, as the error message explains, it will only test 
to see whether a single character is contained in the string (by analogy 
with

     1 in [3, 4, 5, 2]

in case you are interested).

So you'll need to use the .find() string method and say

     if x.find("Hello") != -1:
         ... you found "Hello"

because your ISP appears to be using an older version of Python than you.

regards
  Steve
-- 
Meet the Python developers and your c.l.py favorites March 23-25
Come to PyCon DC 2005                      http://www.pycon.org/
Steve Holden                           http://www.holdenweb.com/</t>
<t tx="ekr.20050329082101.107">


"Zhang Le" &lt;sigu4wa02@sneakemail.com&gt; wrote in message 
news:1109952846.225378.136210@o13g2000cwo.googlegroups.com...
&gt; Hi,
&gt;  I did a small benchmark of matrix-vector multiply operation using
&gt; Numeric module. I'm a bit suprised to find matrix*col-vector is much
&gt; faster than row-vector*matrix. I wonder whether other people have
&gt; observed this fact too,

Yes, common knowledge in numerical analysis community.  Using the faster 
direction for a particular system as much as possible is part of tuning 
linear algebra software.

&gt; and why?

I presume that Numeric, like Python, stores matrices by row.  So M*v 
multiplies contiguous rows by a contiguous vector.  Multiplying a vector by 
non-contiguous columns requires requires skipping thru the matrix, which 
may require more computation and generate more cache misses and page 
faults.

Terry  J. Reedy


</t>
<t tx="ekr.20050329082101.108">

I just read in the 'What's New in Python 2.4' document that the None
data type was converted to a constant:
http://python.org/doc/2.4/whatsnew/node15.html

"""
# None is now a constant; code that binds a new value to the name
"None" is now a syntax error.
"""

So, what's the implications of this?  I find the lack of explanation a
little puzzling, since I've written code that compares a variable's
type with the 'None' type.  For example, a variable would be
initialized to 'None' and if it went through a loop unchanged, I could
determine this at the end by using a conditional type(var) ==
type(None).  What will type(None) return now?
</t>
<t tx="ekr.20050329082101.109">

On Fri, 4 Mar 2005 22:35:48 +0100, andrea_gavana@tin.it
&lt;andrea_gavana@tin.it&gt; wrote:
&gt; Hello NG,
&gt; 
&gt;     I was wondering if there is a way to obtain, from a list of floats,
&gt; a list of integers without loops. Probably is a basic question, but I can't
&gt; find an answer... I have had my eyes blinded by Matlab for years, but now
&gt; that I discovered Python+wxPython there seems to be no limit on what one
&gt; can do with these 2 tools. Anyway, following the Matlab style, I would like
&gt; to do something like this:
&gt; 
&gt; matrix = [1.5, 4.3, 5.5]
&gt; integer_matrix = int(matrix)       (float for Matlab)

You're going to have to use loops. I don't know how Matlab can do it
without them, unless it maintains the matrix as a list of floats and
simply *views* it as a list of ints. More likely, it simply hides the
loop away from you. Anyway, here's some ways to do it:

preferable: int_matrix = [int(x) for x in matrix]
old way: int_matrix = map(int, matrix)
explicit:
int_matrix = []
for x in matrix:
    int_matrix.append(int(x))

Any of these methods should be neither really slow nor really fast,
but the list comprehension should be the fastest (I think). Anyway, if
you're going to be doing lots of large matrices, and want some of your
old matlab stuff, check out numpy and numarray at
http://numeric.scipy.org/ .

Also, somebody was recently posting on here about a python &lt;-&gt; matlab
bridge that they developed; you should search the archives for that
(it was in february, I think).

And, finally, when doing scientific stuff, I found IPython
(http://ipython.scipy.org/) to be an invaluable tool. It's a much
improved Python interpreter.

Peace
Bill Mill
bill.mill at gmail.com

&gt; 
&gt; (In Matlab, "integer_matrix" is always a double anyway, here I would like
&gt; only to show the vector-matrix operation).
&gt; 
&gt; Obviously, Python complains about:
&gt; 
&gt; Traceback (most recent call last):
&gt;   File "&lt;interactive input&gt;", line 1, in ?
&gt; TypeError: int() argument must be a string or a number
&gt; 
&gt; I would like to avoid loops because, having been blinded by Matlab vector-matrix
&gt; abilities (and corresponding SLOW for-while loops operations), I tend to
&gt; think that also Python will be slow if I use loops.
&gt; 
&gt; Does anyone have a suggestion (or maybe could anyone show me that I'm wrong
&gt; about loops?)
&gt; 
&gt; Thanks you a lot.
&gt; 
&gt; Andrea.
&gt; 
&gt; --
&gt; http://mail.python.org/mailman/listinfo/python-list
&gt;</t>
<t tx="ekr.20050329082101.110">news-server.houston.rr.com/comp.lang.python</t>
<t tx="ekr.20050329082101.111">

This was happening to me for a while but stopped. I think it has to do with 
your mail server. Perhaps you could find another. If you are at a company, 
you might want to talk to your sysadmin and see if he can change the mail 
program. How did you get this latest message through? You know, with the 
proper email client you can have identities and such that have "from" and 
"return addresses" that are completely unrelated to the mail server you are 
using, if you would rather the mail list did not know about your most favored 
address.

James

On Friday 04 March 2005 01:56 pm, phil wrote:
&gt; everything I post to this list bounces awaiting moderator
&gt; approval, due to suspicious header.
&gt; COuld someone tell me what's wrong.  I'm on lots of list
&gt; with no problem.

-- 
James Stroud, Ph.D.
UCLA-DOE Institute for Genomics and Proteomics
Box 951570
Los Angeles, CA 90095</t>
<t tx="ekr.20050329082101.112">news-server.houston.rr.com/comp.lang.python</t>
<t tx="ekr.20050329082101.113">news-server.houston.rr.com/comp.lang.python</t>
<t tx="ekr.20050329082101.114"></t>
<t tx="ekr.20050329082101.145"># This file allows you to turn handlers on and off
doc.py
remote.py
rss.py
test.py
news.py

plugin_manager.py</t>
<t tx="ekr.20050329082101.146"></t>
<t tx="ekr.20050329082101.147">&lt;&lt; docstring &gt;&gt;

from autotrees import BaseTreeHandler, TreeNode

__version__ = "0.1"
__plugin_requires__ = ["autotrees"]
__plugin_group__ = "Test"

&lt;&lt; version history &gt;&gt;


# This module contains multiple handlers for testing only
# This isn't recommended since the Manager dialog cannot
# cope with it very well - it assumes a single handler per
# file.

class Test(BaseTreeHandler):
    """A test handler"""
    
    def initFrom(self, parameter):
        """Initialize the tree"""
        self.children = [
            TreeNode("one", "this is one"),
            TreeNode("two", "this is two !!!"),
            TreeNode("three", "this is three",[
                TreeNode("three-one"),
                TreeNode("three-two"),
                TreeNode("three-three"),
            ])
        ]
        
class Test2(BaseTreeHandler):
    """A test2 handler - wont do much!"""
    
class Test3(Test):
    """A test3 handler - much like Test but the nodes don't get deleted"""
    
    def preprocessNode(self):
        """Override the default deleting of child nodes"""
        pass
        
    </t>
<t tx="ekr.20050329082101.148">"""A Test handler.

This defines
    @auto-test = adds some nodes
    @auto-test2 = doesn't do anything
    @auto-test3 = adds nodes but doesn't delete the old ones
     
"""

</t>
<t tx="ekr.20050329082101.149">@

Version history

0.1 Paul Paterson:
    - Initial version</t>
<t tx="ekr.20050329082101.150">&lt;&lt; docstring &gt;&gt;

from autotrees import BaseTreeHandler, TreeNode
import feedparser
import leoGlobals as g

__version__ = "0.1"
__plugin_requires__ = ["feedparser", "autotrees", "plugin_manager"]
__plugin_group__ = "Network"

&lt;&lt; version history &gt;&gt;

class RSS(BaseTreeHandler):
    """RSS auto tree handler"""
        
    def initFrom(self, parameter):
        """Initialize the tree"""
        node_body = self.node.bodyString().strip()
        self.children = []
        #
        g.es("Starting download", color="blue")
        try:
            feed = feedparser.parse(parameter)
        except Exception, err:
            g.es("Failed: %s" % (err,), color="red")
            self.children.append(TreeNode("error", str(err)))
        #
        else:
            g.es("Done!", color="blue")
            for item in feed['items']:
                if not node_body:
                    content = '\n'.join(['%s:\n%s\n' % (name, item[name]) for name in item.keys()])
                else:
                    content = self.replaceAll(node_body, item)
                self.children.append(TreeNode(
                        item.get('title', 'No title1'),
                        content))
        
    def replaceAll(self, text, dct):
        """Replace all suitable looking names in text with their dictionary values"""
        for name in dct.keys():
            item = dct[name]
            if isinstance(item, dict):
                item = item.get('value', item)
            text = text.replace(name, str(item))
        return text
</t>
<t tx="ekr.20050329082101.151">"""A handler that downloads RSS feeds

The parameter in the @auto-rss headline is the URL to load from. The
body of the node contains the keys to display in the created node
bodies.

To begin with, leave the main body empty - this signifies to use *all*
the data in the bodies of the node. You can then use the keys identified
there to select which things you want to see.

Details will appear as "key:" followed by the content. If you want to 
see the keyed value, then put "key" in the body of the @auto-rss node.
Actually the body text is a series of keywords which will be replaced
by their values in the stream, so the formatting is kept too!

Requires feedparser installed:
    http://sourceforge.net/projects/feedparser/
    
"""
</t>
<t tx="ekr.20050329082101.152">@

Version history

0.1 Paul Paterson:
    - Initial version</t>
<t tx="ekr.20050329082101.153">&lt;&lt; docstring &gt;&gt;

from autotrees import BaseTreeHandler, TreeNode
import feedparser
import leoGlobals as g
import nntplib
import sets

__version__ = "0.1"
__plugin_requires__ = ["autotrees"]
__plugin_group__ = "Network"

&lt;&lt; version history &gt;&gt;

@others</t>
<t tx="ekr.20050329082101.154">"""A handler that downloads messages from a news server

The parameter in the @auto-rss headline is the news server followed
by the group name in the form:
    
    @auto-news newserver.myisp.com/comp.lang.python
    
Messages will be downloaded directly as nodes. Doesn't support threading
but message bodies are downloaded lazily, ie only when you click on the
header. This is achieved by using the @auto-newsitem headline. 
    
"""
</t>
<t tx="ekr.20050329082101.155">@

Version history

0.1 Paul Paterson:
    - Initial version</t>
<t tx="ekr.20050329082101.156">class NewsTreeError(Exception):
    """Something went wrong with the tree"""
    
</t>
<t tx="ekr.20050329082101.157">def getConnection(parameter):
    """Return a connection to a news server group"""
    try:
        server, group = parameter.split(r"/")
    except ValueError:
        g.es("Could not decifer server/group from '%s'" % (parameter,), color="red")
        raise NewsTreeError
    #
    try:
        connection = nntplib.NNTP(server)
    except Exception, err:
        g.es("Unable to connect to '%s': %s" % (server, err), color="red")
        raise NewsTreeError
    #
    try:
        resp, count, first, last, name = connection.group(group)
    except Exception, err:
        g.es("Unable to talk to group '%s': %s" % (group, err), color="red")
        raise NewsTreeError
    #
    return (connection, resp, count, first, last, name)</t>
<t tx="ekr.20050329082101.158">class News(BaseTreeHandler):
    """News auto tree handler"""
        
    @others</t>
<t tx="ekr.20050329082101.159">def initFrom(self, parameter):
    """Initialize the tree"""
    self.children = []
    #
    try:
        connection, resp, count, first, last, name = getConnection(parameter)
    except NewsTreeError:
        return
    #
    resp, subs = connection.xhdr('subject', first + '-' + last)
    #
    for item in subs[:10]: # First 10 articles .... just for testing as this is slooooow!
        id, subject = item
        self.children.append(
            TreeNode("@auto-newsitem %s - %s" % (id, subject),
                     parameter
            )
        )
    
    connection.quit()</t>
<t tx="ekr.20050329082101.160">class NewsItem(BaseTreeHandler):
    """Handlers news item bodies"""
    
    handles = sets.Set(["headclick1"])    
    
    @others
</t>
<t tx="ekr.20050329082101.161">def initFrom(self, parameter):
    """Initialize the tree"""
    self.children = []
    #
    # Get the server name which we conveniently left in the body
    body = self.node.bodyString().splitlines()[0]
    try:
        connection, resp, count, first, last, name = getConnection(body)
    except NewsTreeError:
        return
    #
    # Now get the article 
    id = self.node.headString().split(" - ", 1)[0][15:]
    article = connection.body(id)
    self.node.setBodyTextOrPane("\n".join(article[-1]))
    #
    connection.quit()

</t>
<t tx="ekr.20050329082101.162">&lt;&lt; docstring &gt;&gt;

from autotrees import BaseTreeHandler, TreeNode
import pycurl
import StringIO

import leoGlobals as g

__version__ = "0.1"
__plugin_requires__ = ["pycurl", "autotrees", "plugin_manager"]
__plugin_group__ = "Network"

&lt;&lt; version history &gt;&gt;


class Remote(BaseTreeHandler):
    """A handler for remote files"""
        
    def initFrom(self, parameter):
        """Initialize the tree"""
        self.children = []

        content = StringIO.StringIO()
        #
        g.es("Starting download", color="blue")
        connection = pycurl.Curl()
        connection.setopt(pycurl.URL, str(parameter)) # Cannot take unicode!
        connection.setopt(pycurl.WRITEFUNCTION, content.write)
        #
        try:
            connection.perform()
        except Exception, err:
            g.es("Failed: %s" % (err,), color="red")
            self.children.append(TreeNode("error", str(err)))
        #
        else:
            g.es("Done!", color="blue")
            self.node.setBodyTextOrPane(content.getvalue())
        
</t>
<t tx="ekr.20050329082101.163">"""A handler that downloads remote files

The parameter in the @auto-remote headline is the URL to load from. You
can pass username passwords in the URL, eg
    ftp://username:password@mysite.org/myfile.txt

Requires pyCurl:
    http://pycurl.sourceforge.net/
    
"""
</t>
<t tx="ekr.20050329082101.164">@

Version history

0.1 - Paul Paterson:
      Initial version
</t>
<t tx="ekr.20050329082101.165">&lt;&lt; docstring &gt;&gt;

from autotrees import BaseTreeHandler, TreeNode
import inspect
import sets

import leoGlobals as g

__version__ = "0.1"
__plugin_requires__ = ["autotrees"]
__plugin_group__ = "Coding"

&lt;&lt; version history &gt;&gt;


class Doc(BaseTreeHandler):
    """Handler for documentation nodes"""
        
    def initFrom(self, parameter):
        """Initialize the tree"""
        self.children = []
        self.done = sets.Set()
        try:
            module = __import__(parameter)
        except Exception, err:
            g.es("Failed: %s" % (err,), color="red")
        else:
            components = parameter.split('.')
            for comp in components[1:]:
                module = getattr(module, comp)
            self.children.extend(self.getDocsFor(module))
            
    def getDocsFor(self, object):
        """Return a list of child nodes documenting the object"""
        #print object
        children = []
        for name in dir(object):
            item = getattr(object, name)
            if not name.startswith("_") and not id(item) in self.done:
                self.done.add(id(item))
                if inspect.isclass(item):
                    #print "Class", item.__name__
                    grandchildren = self.getDocsFor(item)
                else:
                    #print "item", item
                    grandchildren = []
                children.append(
                    TreeNode(
                        name,
                        getattr(item, "__doc__", "No documentation for %s" % name),
                        grandchildren
                    )
                )
        return children
            
</t>
<t tx="ekr.20050329082101.166">"""A handler that documents a module

The parameter in the @auto-doc headline is the module to document.
    
"""
</t>
<t tx="ekr.20050329082101.167">@

Version history

0.1 - Paul Paterson:
      Initial version
</t>
<t tx="ekr.20050329092553">Hundreds die in Indonesia quake

Hundreds are believed to have died in Indonesia after a strong earthquake which sparked fears of a tsunami.</t>
<t tx="ekr.20050329092553.1">Ousted Kyrgyz preshttp://news.bbc.co.uk/1/hi/world/asia-pacific/4391139.stment defiant

Ousted Kyrgyz leader Askar Akayev says he remains the "sole legitimate preshttp://news.bbc.co.uk/1/hi/world/asia-pacific/4391139.stment" of his country.</t>
<t tx="ekr.20050329092553.2">Hair 'good source of stem cells'

Scientists have found hair follicles are a plentiful source of stem cells, which can become body tissue.</t>
<t tx="ekr.20050329092553.3">Ashdown sacks top Bosnian Croat

The top administrator in Bosnia, Lord Ashdown, sacks the Croat member of Bosnia's joint preshttp://news.bbc.co.uk/1/hi/world/europe/4390635.stmency.</t>
<t tx="ekr.20050329092553.4">Splits paralyse Iraqi parliament

Iraq's parliament reconvenes, but remains deadlocked over the formation of a new government.</t>
<t tx="ekr.20050329092553.5">Mongolians protest for new poll

Activists in Mongolia call for fresh elections, 
in an action apparently inspired by the situation in Kyrgyzstan.</t>
<t tx="ekr.20050329092553.6">Libya's Bulgarian medics appeal

Six medics appeal against the death sentence imposed in Libya for deliberately infecting children with HIV.</t>
<t tx="ekr.20050329092553.7">Schiavo rivals 'agree to autopsy'

Terri Schiavo's husband and parents seek to discover the extent of her brain-damage after her death.</t>
<t tx="ekr.20050329092553.8">Would-be sex tourist, 87, jailed

An octogenarian US man is jailed for 20 years for trying to travel to the Philippines for sex with young girls.</t>
<t tx="ekr.20050329092553.9">Golf: Funk claims Players title

Fred Funk's final-round 70 gives him victory in the lucrative Players Championship at Sawgrass.</t>
<t tx="ekr.20050329092553.10">Cricket: Series win for Aussies

Australia beat New Zealand by nine wickets in the third Test to wrap up a 2-0 series win.</t>
<t tx="ekr.20050329092553.11">Angola says virus 'under control'

Angola says an outbreak of the deadly Marburg virus is under control as DR Congo takes precautions.</t>
<t tx="ekr.20050329092553.12">Mugabe criticises MDC 'traitors'

Preshttp://news.bbc.co.uk/1/hi/world/africa/4391087.stment Mugabe condemns opposition supporters as traitors, as parliamentary elections draw near.</t>
<t tx="ekr.20050329092553.13">Ex-US diplomats round on Bolton

Dozens of former US diplomats urge Congress to block the appointment of John Bolton as UN ambassador.</t>
<t tx="ekr.20050329092553.14">Brazil quits loan accord with IMF

Brazil announces it will not renew a $41.75bn loan accord with the International Monetary Fund.</t>
<t tx="ekr.20050329092553.15">Japanese economy hit by weak data

An unexpected rise in Japan's jobless rate and falls in household spending and retail sales hit Japanese stocks.</t>
<t tx="ekr.20050329092553.16">Donors pledge $40m for KR trials

A UN-supported Khmer Rouge tribunal, due to try Cambodia's rulers from the 1970s, could open soon.</t>
<t tx="ekr.20050329092553.17">Three Romanians missing in Iraq

Three Romanian journalists are missing, feared khttp://news.bbc.co.uk/1/hi/world/middle_east/4389391.stmnapped, in Iraq after one called on a mobile.</t>
<t tx="ekr.20050329092553.18">Wolfowitz 'to meet EU officials'

Paul Wolfowitz, the US's controversial nomination to head the World Bank, is expected to meet with EU officials on Wednesday, reports say.</t>
<t tx="ekr.20050329092553.19">Knesset rejects Gaza referendum

Israel's parliament rejects an attempt by opponents of the planned Gaza pullout to force a referendum.</t>
<t tx="ekr.20050329092553.20">Militants to attend PLO meeting

Islamic Jihad is to sit in on a meeting of the top Palestinian decision-making body for the first time.</t>
<t tx="ekr.20050329092553.21">South Asia cancels tsunami alerts

India and Sri Lanka withdraw the tsunami alerts issued after an earthquake hit the coast of Indonesia.</t>
<t tx="ekr.20050329092553.22">Devastation as Afghan dam bursts

A dam has burst in south-eastern Afghanistan killing at least six people and causing whttp://news.bbc.co.uk/1/hi/world/south_asia/4391251.stmespread devastation, officials say.</t>
<t tx="ekr.20050329092553.23">Kyrgyzstan's friendly revolution

The BBC's Ian MacWilliam reports from Kyrgyzstan on an unusual people's revolution.</t>
<t tx="ekr.20050329092553.24">Followup on MS and Brazil in NY Times (mainpage, microsoft)

putko was one of dozens to submit a story running on the NY Times about Open Source and Brazil. The choice quote is "We're not going to spend taxpayers' money on a program so that Microsoft can further consolhttp://slashdot.org/article.pl?sid=05/03/29/1359253&amp;from=rssate its monopoly..."

http://slashdot.org/article.pl?shttp://slashdot.org/article.pl?sid=05/03/29/1359253&amp;from=rss=05/03/29/1359253&amp;from=rss</t>
<t tx="ekr.20050329092553.25">A9.com with Syndicated Search (mainpage, internet)

joeykiller writes "Search Engine Watch reports that Amazon now lets you add your own search to their A9 search engine. Users can opt-in to use additional search engines in addition to A9.com's own when searching. Amazon has chosen to use an extension of RSS 2.0 for this, and hopes that this format will enable search syndication in the same way RSS dhttp://slashdot.org/article.pl?sid=05/03/29/1337250&amp;from=rss for content. Several add-on searches are available already, among them New York Times, Wikipedia and NASA."

http://slashdot.org/article.pl?shttp://slashdot.org/article.pl?sid=05/03/29/1337250&amp;from=rss=05/03/29/1337250&amp;from=rss</t>
<t tx="ekr.20050329092553.26">What's Next At Apple (apple, apple)

pinqkandi writes "Business 2.0 is running a fascinating article on what might be coming up in Apple's future. Beshttp://apple.slashdot.org/article.pl?sid=05/03/29/132202&amp;from=rsses speculation, some interesting statistics are included, such as how the iPod should create equal revenue to the Mac for Apple in 2006, if not surpassing it. A good read for the Apple lover or loather."

http://apple.slashdot.org/article.pl?shttp://apple.slashdot.org/article.pl?sid=05/03/29/132202&amp;from=rss=05/03/29/132202&amp;from=rss</t>
<t tx="ekr.20050329092553.27">Berkeley Grads' Identity Data Stolen (yro, privacy)

yali writes "Dhttp://yro.slashdot.org/article.pl?sid=05/03/29/036237&amp;from=rss you get a graduate degree from Berkeley? Or maybe you just applied but dhttp://yro.slashdot.org/article.pl?sid=05/03/29/036237&amp;from=rssn't go there? If so, your http://yro.slashdot.org/article.pl?sid=05/03/29/036237&amp;from=rssentity may have been stolen. A laptop was stolen containing names, social security numbers, birthdates, and addresses of grad students, alumni, and applicants. University police suspect that the thief just wanted the laptop, but the irony of California's mandatory notification law is that the thief may now know they have something even more valuable. Berkeley has set up a website with information on the breach."

http://yro.slashdot.org/article.pl?shttp://yro.slashdot.org/article.pl?sid=05/03/29/036237&amp;from=rss=05/03/29/036237&amp;from=rss</t>
<t tx="ekr.20050329092553.28">South Korean Gov't. Advocates Linux (linux, linuxbiz)

Anonymous Coward writes "Korea has now taken the plunge on the Linux operating system, and is now starting to advocate Linux for use in government and public sector applications. South Korea's Ministry of Information and Communications announced the move today, which will result in decreased Microsoft market share in the region." According to the article, Korea's Ministry of Information and Communication "will provhttp://linux.slashdot.org/article.pl?sid=05/03/29/0322248&amp;from=rsse a total of 3 billion won (US$2.95 million) for government agencies which want to use the Linux and other open-source computer programs this year."

http://linux.slashdot.org/article.pl?shttp://linux.slashdot.org/article.pl?sid=05/03/29/0322248&amp;from=rss=05/03/29/0322248&amp;from=rss</t>
<t tx="ekr.20050329092553.29">MS, EU Agree on Name for Windows Sans Media Player (mainpage, windows)

An anonymous reader writes "Microsoft has agreed with European Union antitrust regulators on a new name for Windows software sold in Europe. Officials at the U.S. software giant sahttp://slashdot.org/article.pl?sid=05/03/28/1951251&amp;from=rss they had accepted the European Union's offer to call the European version of Windows sold without Media Player "Windows XP Home Edition N" - with "N" standing for "not with media player." Microsoft's "XP Professional Edition" will also include the "N" for versions sold without the media player. The prior nme for the OS was Windows XP Reduced Media Edition." News.com also mentions the choice.

http://slashdot.org/article.pl?shttp://slashdot.org/article.pl?sid=05/03/28/1951251&amp;from=rss=05/03/28/1951251&amp;from=rss</t>
<t tx="ekr.20050329092553.30">Blackbox (Finally) Updated (mainpage, gui)

mpeg4codec writes "OSNews reported earlier this month that the lightweight Blackbox window manager has been updated to 0.70. Among the new features are EWMH compliance, anti-aliased fonts, unicode support, and backwards compatibility with previous versions' styles. Of course, it brings you all these new features (well, some are optional) while retaining its small binary size, small memory footprint, and short list of dependencies. I for one think it's about time."

http://slashdot.org/article.pl?shttp://slashdot.org/article.pl?sid=05/03/29/0253245&amp;from=rss=05/03/29/0253245&amp;from=rss</t>
<t tx="ekr.20050329092553.31">Your Face On the Big Screen (mainpage, ent)

blamanj writes "In another case of SciFi becoming reality, you can now star in an animated film as your FutureCast (tm) face-scan is edited into the picture in real-time. John Brunner, in his Hugo-winning novel, Stand on Zanzibar predicted a similar development in television, lampooning people sitting at home while watching travologues of themselves 'on vacation.' Brunner, in addition to being an excellent writer, had some spot-on predictions of a virus-laden Internet in Shockwave Rhttp://slashdot.org/article.pl?sid=05/03/29/0123247&amp;from=rsser. Fortunately, the predictions of his eco-dystopia The Sheep Look Up have not come to pass. Yet."

http://slashdot.org/article.pl?shttp://slashdot.org/article.pl?sid=05/03/29/0123247&amp;from=rss=05/03/29/0123247&amp;from=rss</t>
<t tx="ekr.20050329092553.32">Ars Technica Builds Make Magazine's Steadicam (hardware, hardhack)

An anonymous reader writes "Make magazine has been out for a little over a month now and was given high marks in a Slashdot review. Ars Technica has taken their review one step further by building the $14 steadicam project and testing it out. (be sure to check out the QuickTime vhttp://hardware.slashdot.org/article.pl?sid=05/03/29/0056206&amp;from=rsseo at the end to see their results...)"

http://hardware.slashdot.org/article.pl?shttp://hardware.slashdot.org/article.pl?sid=05/03/29/0056206&amp;from=rss=05/03/29/0056206&amp;from=rss</t>
<t tx="ekr.20050329092553.33">New Photovoltaics Made with Titanium Foil (science, tech)

Memorize writes "A company called Daystartech has released a new type of photovoltaic cell which, unlike almost all the cells currently in use, does not silicon. This is based on a thin titanium film. Given the current shortage of solar-grade silicon, and all-time high oil prices, maybe titanium solar panels are here at the right time. The questions are, will they release it as a consumer solar product, and what will be the price per kilowatt hour?"

http://science.slashdot.org/article.pl?shttp://science.slashdot.org/article.pl?sid=05/03/28/2320211&amp;from=rss=05/03/28/2320211&amp;from=rss</t>
<t tx="ekr.20050402080206">@

This is LeoN-0.0.1 as created by Rodrigo Benenson, very slightly reorganized form.

An important project for Leo's long-term development.

See leo/doc/LeoN for important research papers that form the basis of this project.</t>
<t tx="ekr.20050402080206.1">@killcolor

Read the docustrings in the code.

Run the code LeoN.py to test it. 

You need to read sun98acheiving.pdf to understand what is all this stuff about.  This and other .pdf files are now in the leo/doc/LeoN folder.

Rodrigo Benenson. 2003. LeoN project. &lt;rodrigob@elo.utfsm.cl&gt;</t>
<t tx="ekr.20050402080206.2">@language plain

LeoN is Leo over the Network.

LeoN is Collaborative Leo.

Leo is http://leo.sf.net

@language plain

Leo over network requirements
-----------------------------

This is my résumé of the Requirements and design issues for Leo over the Network. (LeoN).

First in sake of simplicity a N-clients/One server architecture is imposed, being much more easy to design and implement.
Also it's required that the code could be as most Plugin as possible and as most python Modules independent as possible (one and only one instalation required).

Now, the list presented approximately in the logic order of implementation:

&lt;Step one, Merging&gt;

&lt;Step two, Publishing&gt;

&lt;Step three, Interacting by turns&gt;

&lt;&lt;Step four, Realtime interaction&gt;&gt;

Please comment this document.

RodrigoB. </t>
<t tx="ekr.20050402080206.3">Step four, "Realtime interaction":
- There should be a way that multiple online users edit on realtime the same Node.
This is the final step and is truly difficult. Probably this code should be merged from a parallel (but related) project.
(Guy X,Y,Z having a code party.)

- The client should show the editors cursors and edition on realtime.
Adquire the status, of Hydra Open Source, Multiplatform, Clone.
(Guy X,Y,Z enjoying the code party.)

Some features were intentionally omited:
- Versioning system. (there exists better solutions)
- Voice chat. (there exists parallel solutions)


</t>
<t tx="ekr.20050402080206.4">The realtime edition  could be implemented initially on a lock/unlock fashion automatized on a per line basis, very much like an online CVS editor...

The complications should be left to a parallel project, or maybe to another community (search, propose and merge/translate)

@nocolor</t>
<t tx="ekr.20050402080206.5">29/06/03

Hi!

It's time to news again. This last weeks were my final exams weeks but LeoN devellopment is going on as planned.

The last two weeks where focused on the Gui control, intercepting the whole list of actions that the user can do into the collaborative outline. There still some importants events to manage, but I think almost the base code is there. As mentioned this stage is absolutelly non trivial nor little; and is characterised to be some how frustating ("Tk marks are before or bellow a charater? Event occurs before or after effects?", and similars) and slow (because you have to test by hand the gui to debug it). The important elements missing will be done at the time it becomes strictly necessary.


The LeoN code is already pretty big and relativelly complex (3500 raw lines count) and there is a big list of things to do. Anyway no one said it would be easy.
Somes days ago I drafted the code base for Step4, hopefully the more important piece of code, due of it reusability and because I think it will give to LeoN an important sparky effect (near realtime multiuser text edition).


So now the actual plan is:
- Focus the next two weeks on the implementation of Step4 and his unit tests.
- Release the Step4 code. (because it is usefull without Leo and could be used in parallel projects)
- Integrate Step4 and Step(2,3) (one week)
- Move the code over Leo 3.1x  and Twisted 1.0.6 (which unfortunelly changed some classes used in LeoN (cred module)) (horizont: one week)
- After that I will focus strictly on finishing the usability elements and (if everything go fine) will start the releases iterations. This stage will have at least the following milestones:
	- Finish and debug the interface hooks (this can be long...)
	- Implement server persistence (should be easy)
	- Implement the admin interface (should be boring)
	- Implement Clones (two weeks if things go fine)
	- Improve the LeoN web views (implement more than one view  model?)
	- Allow as easy as possible instalations

Of course the releases will be all alpha during a probably long period until the devellopers are happy and then we will switch to beta and when everyone will be happy : the first stable Release !

I'm pretty impacient to finish the vapourware status of LeoN, we have the luck that the timing are acceptable, and Leo has some importants things to do before LeoN will become the first priority. This will give me the time to work on the mentioned plan.

RodrigoB.</t>
<t tx="ekr.20050402080206.6">As said, it is times to news. Briefly.

about step4
-----------

The code is ready and running since wednesday (mercredi) on the morning, but until now I'm  grumbling-grumbling with the code to get it working as supposed; I have found some minor bugs and solved some conceptuals problems and bugs. Debugging code of someelse algorithm is notoriously harder than working on your own ideas but the work give his fruits and each day we are one step nearer to us dreams.
Most of the hard problems are due to some ambiguities or not so clear ideas in the papers, so I have to crunch my brain to guess the correct way to manage the presented abstractions (or apply a 'guess, try, evaluate' strategy).

Due to this problems, and after five days of debugging work I will delay the code release until I get the unit test passed, this should not take more than a week more (I hope so, but you never know if the actual bug is or not the last one).


what is next
------------

- Finish debug of step4
- Implement and test the one server various clients collaborative editing (a special case of the above class)
- move codebase to 3.12b* and twisted 1.0.6
- merge step2, step3, step4 
- start the release of the code snapshots.
- start working on last frozen elements and on the Todo List:
	- hooks installations and debug (starting by node renaming)
	- admin interface
	- server side persistence 
	- clone support
	- cut and paste (with download interface)
	- better web server views
	- design a web plugin system ?
	- debugging, debugging
	- as easy as possible instalations
	- work on the design of LeoN2 features

I will stay working on a two weeks devellopment cycles, and post news at the end of each cycle.


RodrigoB.</t>
<t tx="ekr.20050402080206.7">@nocolor

25/06/03 Copying of the main algorithms into the code. RodrigoB.
01/07/03 Programming. RodrigoB.
02/07/03 Programming. RodrigoB.
05/07/03 Reading about the garbage collector stuff. RodrigoB.
07/07/03 Programming. RodrigoB.
08/07/03 Programming, operations herit from dict, support splitted ops, working on tests, syntax debugging. RodrigoB.
09/07/03 Implementing operations relations, starting debug iterations based on unittests.
		 Added another parameters form for receive_operation. RodrigoB.
10/07/03 Debugging conceptual aspects; management of timestamps on transformed operations. minor bugs fixed. Splitted special cases appears.RodrigoB.
12/07/03 Searching bugs. bugfixes. RodrigoB.
13/07/03 Implementing the garbage collector. Searching bugs. bugfixes. Testing garbage collector. RA problems. RodrigoB.
14/07/03 (vive la France!) Testing an idea (__eq__). Little edit to the root docustring. RodrigoB.
15/07/03 Hunting the Last Bug. Eureka. First successful execution. Code cleanup. Using unittest module. Release 1. RodrigoB.

Todo

- Find a good TestConcurrentEditable2 to test LostInformation cases

- LI is absolutelly not verified
- Find the Recover_LI specifications.
- Find a better way to quit the ambiguities on the 'if else {}' operation pertenence. (save_RA, save_LI conditions ?)

- collect garbage do not work anymore exactly like in the example. (is this a problem ?)

- Implement ConcurrentEditableServer
- Implement the  client-server tests

- Debug.

@color
@language python

</t>
<t tx="ekr.20050529143413.30">def colorize(self,p,incremental=False):
    
    '''The main colorizer entry point.'''
    
    # g.trace(incremental)

    if self.enabled:
        self.incremental=incremental 
        self.updateSyntaxColorer(p)
        return self.colorizeAnyLanguage(p)
    else:
        return "ok" # For unit testing.</t>
<t tx="ekr.20050529143413.31">def colorizeAnyLanguage (self,p,leading=None,trailing=None):
    
    '''Color the body pane.  All coloring starts here.'''
    
    self.init_mode(self.language)
    if self.killcolorFlag or not self.mode:
        self.removeAllTags() ; return
    try:
        c = self.c
        self.p = p
        self.redoColoring = False
        self.redoingColoring = False
        self.was_non_incremental = not self.incremental
        # g.trace('was_non_incremental',self.was_non_incremental)
        if not self.incremental:
            # g.trace('removing tags')
            if 0: # removing tags causes flash at idle time.
                self.removeAllTags()
                self.removeAllImages()
            self.colored_ranges = {}
        self.configure_tags()
        g.doHook("init-color-markup",colorer=self,p=self.p,v=self.p)
        s = self.body.getAllText()
        self.colorAll(s)
        if self.redoColoring: # Set only from plugins.
            self.recolor_all()
        return "ok" # for unit testing.
    except Exception:
        g.es_exception()
        return "error" # for unit testing.</t>
<t tx="ekr.20050529180421">@killcolor</t>
<t tx="ekr.20050529180421.1">You might encounter this very common pitfall when writing your own modes.

Since jEdit checks buffer text against parser rules in the order they appear in
the ruleset, more specific rules must be placed before generalized ones,
otherwise the generalized rules will catch everything.</t>
<t tx="ekr.20050529180421.2"></t>
<t tx="ekr.20050529180421.3"></t>
<t tx="ekr.20050529180421.4"></t>
<t tx="ekr.20050529180421.5">If set to TRUE, the sequence will only be highlighted if it occurs at the beginning of a line.</t>
<t tx="ekr.20050529180421.6">If set to TRUE, the sequence will only be highlighted if it is the first non-whitespace text in the line.</t>
<t tx="ekr.20050529180421.7">If set to TRUE, the sequence will only be highlighted if it occurs at the beginning of a word.</t>
<t tx="ekr.20050529180421.8"></t>
<t tx="ekr.20050529180421.9">If set to TRUE, the span will not cross word breaks.</t>
<t tx="ekr.20050529180421.10">If set to TRUE, the span will not cross line breaks.</t>
<t tx="ekr.20050529180421.11">If set to TRUE, the ruleset's escape character will have no effect before the span's end string. Otherwise, the presence of the escape character will cause that occurrence of the end string to be ignored.

</t>
<t tx="ekr.20050529180421.12">If set to TRUE, the match will not be highlighted, only the text before it will.</t>
<t tx="ekr.20050529180421.13"></t>
<t tx="ekr.20050529180421.14">The token type for text which doesn't match any specific rule. Default is NULL.
See the section called “Token Types” for a list of token types.</t>
<t tx="ekr.20050529180421.15">If the HIGHLIGHT_DIGITS attribute is set to TRUE, jEdit will attempt to highlight numbers in this ruleset.

Any word consisting entirely of digits (0-9) will be highlighted with the DIGIT token type.

A word that contains other letters in addition to digits will be highlighted with the DIGIT token type only if it matches the regular expression specified in the DIGIT_RE attribute. If this attribute is not specified, it will not be highlighted.

Here is an example DIGIT_RE regular expression that highlights Java-style numeric literals (normal numbers, hexadecimals prefixed with 0x, numbers suffixed with various type indicators, and floating point literals containing an exponent):

DIGIT_RE="(0x[[:xdigit:]]+|[[:digit:]]+(e[[:digit:]]*)?)[lLdDfF]?"</t>
<t tx="ekr.20050529180421.16">If set to FALSE, matches will be case sensitive.
Otherwise, case will not matter. Default is TRUE.</t>
<t tx="ekr.20050529180421.17">The name of this ruleset. All rulesets other than the first must have a name.</t>
<t tx="ekr.20050529180421.18">Any non-alphanumeric character not in this list is treated as a word separator for the purposes of syntax highlighting.
</t>
<t tx="ekr.20050529180421.19">The number of characters to terminate after.</t>
<t tx="ekr.20050529180421.20">Text inside the span will be highlighted with the specified ruleset. To delegate
to a ruleset defined in the current mode, just specify its name. To delegate to
a ruleset defined in another mode, specify a name of the form mode::ruleset.
Note that the first (unnamed) ruleset in a mode is called “MAIN”.

One quirk is that the definition of the imported ruleset is not copied to the
location of the IMPORT tag, but rather to the end of the containing ruleset.
This has implications with rule-ordering; see the section called “Rule Ordering
Requirements”.</t>
<t tx="ekr.20050529180421.21">Atribute            Elements used in
--------            ----------------
HASH_CHAR           EOL_SPAN_REGEXP,SPAN_REGEXP,SEQ_REGEXP

It must be set to the first character that the regular expression matches. This
rules out using regular expressions which can match more than one character at
the start position. The regular expression match cannot span more than one line,
either.</t>
<t tx="ekr.20050529180421.22">The token type to highlight the text with.

Parser rules can highlight tokens using any of the following token types:

NULL - no special highlighting
COMMENT1,COMMENT2,COMMENT3,COMMENT4
FUNCTION
KEYWORD1,KEYWORD2,KEYWORD3,KEYWORD4
LABEL
LITERAL1,LITERAL2,LITERAL3,LITERAL4
MARKUP
OPERATOR</t>
<t tx="ekr.20050529180421.23">Atribute            Elements used in
--------            ----------------
AT_LINE_START       BEGIN,END
AT_WHITESPACE_END   BEGIN,END
AT_WORD_START       BEGIN,END</t>
<t tx="ekr.20050529180421.24">The only required attribute DELEGATE must be set to the name of a ruleset. To
import a ruleset defined in the current mode, just specify its name. To import a
ruleset defined in another mode, specify a name of the form mode::ruleset. Note
that the first (unnamed) ruleset in a mode is called “MAIN”.

One quirk is that the definition of the imported ruleset is not copied to the
location of the IMPORT tag, but rather to the end of the containing ruleset.
This has implications with rule-ordering; see the section called “Rule Ordering
Requirements”.</t>
<t tx="ekr.20050529180421.25">Atribute            Elements used in
--------            ----------------
AT_LINE_START       MARK_FOLLOWING,MARK_PREVIOUS
AT_WHITESPACE_END   MARK_FOLLOWING,MARK_PREVIOUS
AT_WORD_START       MARK_FOLLOWING,MARK_PREVIOUS 
EXCLUDE_MATCH       MARK_FOLLOWING,MARK_PREVIOUS
TYPE                MARK_FOLLOWING,MARK_PREVIOUS</t>
<t tx="ekr.20050529180421.26">Atribute            Elements used in
--------            ----------------
NAME                PROPERTY
VALUE               PROPERTY</t>
<t tx="ekr.20050529180421.27">Atribute            Elements used in
--------            ----------------
DEFAULT             RULES
DIGIT_RE            RULES
HIGHLIGHT_DIGITS    RULES
IGNORE_CASE         RULES
SET                 RULES
NO_WORD_SEP         RULES

The RULES tag supports the following attributes, all of which are optional: 

SET the name of this ruleset. All rulesets other than the first must have a
name.

IGNORE_CASE if set to FALSE, matches will be case sensitive. Otherwise, case
will not matter. Default is TRUE.

NO_WORD_SEP Any non-alphanumeric character not in this list is treated as a word
separator for the purposes of syntax highlighting.

DEFAULT The token type for text which doesn't match any specific rule. Default
is NULL. See the section called “Token Types” for a list of token types.

HIGHLIGHT_DIGITS DIGIT_RE

If the HIGHLIGHT_DIGITS attribute is set to TRUE, jEdit will attempt to
highlight numbers in this ruleset.

Any word consisting entirely of digits (0-9) will be highlighted with the DIGIT
token type. A word that contains other letters in addition to digits will be
highlighted with the DIGIT token type only if it matches the regular expression
specified in the DIGIT_RE attribute. If this attribute is not specified, it will
not be highlighted.</t>
<t tx="ekr.20050529180421.28">all_spans   = EOL_SPAN,EOL_SPAN_REGEXP,SPAN,SPAN_REGEXP
plain_spans = SPAN,SPAN_REGEXP
regx_spans  = EOL_SPAN_REGEXP,SPAN_REGEXP

Atribute            Elements used in
--------            ----------------
AT_LINE_START       all_spans
AT_WHITESPACE_END   all_spans
AT_WORD_START       all_spans
DELEGATE            all_spans
EXCLUDE_MATCH       all_spans
HASH_CHAR           regx_spans  (must be specified)
NO_ESCAPE           plain_spans
NO_LINE_BREAK       plain_spans
NO_WORD_BREAK       plain_spans
TYPE                all_spans</t>
<t tx="ekr.20050529180421.29">Atribute            Elements used in
--------            ----------------
AT_LINE_START       SEQ,SEQ_REGEXP
AT_WHITESPACE_END   SEQ,SEQ_REGEXP
AT_WORD_START       SEQ,SEQ_REGEXP
DELEGATE            SEQ,SEQ_REGEXP
HASH_CHAR           SEQ_REGEXP (must be specified)
TYPE                SEQ,SEQ_REGEXP</t>
<t tx="ekr.20050529180421.30">@language html
@color</t>
<t tx="ekr.20050529180421.31">An EOL_SPAN is similar to a SPAN except that highlighting stops at the end of
the line, and no end sequence needs to be specified. The text to match is
specified between the opening and closing EOL_SPAN tags.

The following attributes are supported:

TYPE - The token type to highlight the span with. See the section called “Token
Types” for a list of token types.

AT_LINE_START - If set to TRUE, the span will only be highlighted if the start
sequence occurs at the beginning of a line.

AT_WHITESPACE_END - If set to TRUE, the span will only be highlighted if the
sequence is the first non-whitespace text in the line.

AT_WORD_START - If set to TRUE, the span will only be highlighted if the start
sequence occurs at the beginning of a word.

DELEGATE - text inside the span will be highlighted with the specified ruleset.
To delegate to a ruleset defined in the current mode, just specify its name. To
delegate to a ruleset defined in another mode, specify a name of the form
mode::ruleset. Note that the first (unnamed) ruleset in a mode is called
“MAIN”.

EXCLUDE_MATCH - If set to TRUE, the start and end sequences will not be
highlighted, only the text between them will.

Here is an EOL_SPAN that highlights C++ comments:

&lt;EOL_SPAN TYPE="COMMENT1"&gt;//&lt;/EOL_SPAN&gt;</t>
<t tx="ekr.20050529180421.32">The EOL_SPAN_REGEXP rule is similar to the EOL_SPAN rule except the match
sequence is taken to be a regular expression.

In addition to the attributes supported by the EOL_SPAN tag, the HASH_CHAR
attribute must be specified. It must be set to the first character that the
regular expression matches. This rules out using regular expressions which can
match more than one character at the start position. The regular expression
match cannot span more than one line, either.

Here is an EOL_SPAN_REGEXP that highlights MS-DOS batch file comments, which
start with REM, followed by any whitespace character, and extend until the end
of the line:

&lt;EOL_SPAN_REGEXP AT_WHITESPACE_END="TRUE" HASH_CHAR="R" TYPE="COMMENT1"&gt;REM\s&lt;/EOL_SPAN_REGEXP&gt;</t>
<t tx="ekr.20050529180421.33">The IMPORT tag, which must be placed inside a RULES tag, loads all rules defined
in a given ruleset into the current ruleset; in other words, it has the same
effect as copying and pasting the imported ruleset.

The only required attribute DELEGATE must be set to the name of a ruleset. To
import a ruleset defined in the current mode, just specify its name. To import a
ruleset defined in another mode, specify a name of the form mode::ruleset. Note
that the first (unnamed) ruleset in a mode is called “MAIN”.

One quirk is that the definition of the imported ruleset is not copied to the
location of the IMPORT tag, but rather to the end of the containing ruleset.
This has implications with rule-ordering; see the section called “Rule Ordering
Requirements”.

Here is an example from the PHP mode, which extends the inline JavaScript
highlighting to support embedded PHP:


   &lt;RULES SET="JAVASCRIPT+PHP"&gt;

   &lt;SPAN TYPE="MARKUP" DELEGATE="php::PHP"&gt;
       &lt;BEGIN&gt;&amp;lt;?php&lt;/BEGIN&gt;
       &lt;END&gt;?&amp;gt;&lt;/END&gt;
   &lt;/SPAN&gt;
   
   &lt;SPAN TYPE="MARKUP" DELEGATE="php::PHP"&gt;
       &lt;BEGIN&gt;&amp;lt;?&lt;/BEGIN&gt;
       &lt;END&gt;?&amp;gt;&lt;/END&gt;
   &lt;/SPAN&gt;
   
   &lt;SPAN TYPE="MARKUP" DELEGATE="php::PHP"&gt;
       &lt;BEGIN&gt;&amp;lt;%=&lt;/BEGIN&gt;
       &lt;END&gt;%&amp;gt;&lt;/END&gt;
   &lt;/SPAN&gt;

   &lt;IMPORT DELEGATE="javascript::MAIN"/&gt;
&lt;/RULES&gt;</t>
<t tx="ekr.20050529180421.34">The KEYWORDS tag, which must be placed inside a RULES tag and can only appear
once, specifies a list of keywords to highlight. Keywords are similar to SEQs,
except that SEQs match anywhere in the text, whereas keywords only match whole
words. Words are considered to be runs of text separated by non-alphanumeric
characters.

The KEYWORDS tag does not define any attributes.

Each child element of the KEYWORDS tag is an element whose name is a token type,
and whose content is the keyword to highlight.

&lt;KEYWORDS&gt;
  &lt;KEYWORD1&gt;if&lt;/KEYWORD1&gt;
  &lt;KEYWORD1&gt;else&lt;/KEYWORD1&gt;
  &lt;KEYWORD3&gt;int&lt;/KEYWORD3&gt;
  &lt;KEYWORD3&gt;void&lt;/KEYWORD3&gt;
&lt;/KEYWORDS&gt;</t>
<t tx="ekr.20050529180421.35">The MARK_FOLLOWING rule, which must be placed inside a RULES tag, highlights
from the start of the match to the next syntax token. The text to match is
specified between opening and closing MARK_FOLLOWING tags.

The following attributes are supported:

TYPE - The token type to highlight the text with. See the section called “Token
Types” for a list of token types.

AT_LINE_START - If set to TRUE, the sequence will only be highlighted if it
occurs at the beginning of a line.

AT_WHITESPACE_END - If set to TRUE, the sequence will only be highlighted if it
is the first non-whitespace text in the line.

AT_WORD_START - If set to TRUE, the sequence will only be highlighted if it
occurs at the beginning of a word.

EXCLUDE_MATCH - If set to TRUE, the match will not be highlighted, only the text
after it will.

Here is a rule that highlights variables in Unix shell scripts (“$CLASSPATH”,“$IFS”, etc):

&lt;MARK_FOLLOWING TYPE="KEYWORD2"&gt;$&lt;/MARK_FOLLOWING&gt;</t>
<t tx="ekr.20050529180421.36">The MARK_PREVIOUS rule, which must be placed inside a RULES tag, highlights from
the end of the previous syntax token to the matched text. The text to match is
specified between opening and closing MARK_PREVIOUS tags. The following
attributes are supported:

TYPE - The token type to highlight the text with. See the section called “Token
Types” for a list of token types.

AT_LINE_START - If set to TRUE, the sequence will only be highlighted if it
occurs at the beginning of a line.

AT_WHITESPACE_END - If set to TRUE, the sequence will only be highlighted if it
is the first non-whitespace text in the line.

AT_WORD_START - If set to TRUE, the sequence will only be highlighted if it
occurs at the beginning of a word.

EXCLUDE_MATCH - If set to TRUE, the match will not be highlighted, only the text
before it will.

Here is a rule that highlights labels in Java mode (for example, “XXX:”):

&lt;MARK_PREVIOUS AT_WHITESPACE_END="TRUE" EXCLUDE_MATCH="TRUE"&gt;:&lt;/MARK_PREVIOUS&gt;</t>
<t tx="ekr.20050529180421.37">Each mode definition must begin with the following:

&lt;?xml version="1.0"?&gt;
&lt;!DOCTYPE MODE SYSTEM "xmode.dtd"&gt;

Each mode definition must also contain exactly one MODE tag. All other tags (PROPS, RULES) must be placed inside the MODE tag. The MODE tag does not have any defined attributes. Here is an example:

&lt;MODE&gt;
    ... mode definition goes here ...
&lt;/MODE&gt;</t>
<t tx="ekr.20050529180421.38">The PROPS tag and the PROPERTY tags inside it are used to define mode-specific
properties. Each PROPERTY tag must have a NAME attribute set to the property's
name, and a VALUE attribute with the property's value.

All buffer-local properties listed in the section called “Buffer-Local
Properties” may be given values in edit modes.

The following mode properties specify commenting strings:

* commentEnd - the comment end string, used by the Range Comment command.
* commentStart - the comment start string, used by the Range Comment command.
* lineComment - the line comment string, used by the Line Comment command. 

When performing auto indent, a number of mode properties determine the resulting indent level:

* The line and the one before it are scanned for brackets listed in the
indentCloseBrackets and indentOpenBrackets properties. Opening brackets in the
previous line increase indent.

If lineUpClosingBracket is set to true, then closing brackets on the current
line will line up with the line containing the matching opening bracket. For
example, in Java mode lineUpClosingBracket is set to true, resulting in brackets
being indented like so:

{
    // Code
    {
        // More code
    }
}

If lineUpClosingBracket is set to false, the line after a closing bracket will
be lined up with the line containing the matching opening bracket. For example,
in Lisp mode lineUpClosingBracket is set to false, resulting in brackets being
indented like so:

(foo 'a-parameter
    (crazy-p)
    (bar baz ()))
(print "hello world")

* If the previous line contains no opening brackets, or if the
doubleBracketIndent property is set to true, the previous line is checked
against the regular expressions in the indentNextLine and indentNextLines
properties. If the previous line matches the former, the indent of the current
line is increased and the subsequent line is shifted back again. If the previous
line matches the latter, the indent of the current and subsequent lines is
increased.

In Java mode, for example, the indentNextLine property is set to match control
structures such as “if”, “else”, “while”, and so on.

The doubleBracketIndent property, if set to the default of false, results in code indented like so:

while(objects.hasNext())
{
    Object next = objects.hasNext();
    if(next instanceof Paintable)
        next.paint(g);
}

On the other hand, settings this property to “true” will give the following result:

while(objects.hasNext())
    {
        Object next = objects.hasNext();
        if(next instanceof Paintable)
            next.paint(g);
    }

Here is the complete &lt;PROPS&gt; tag for Java mode:

&lt;PROPS&gt;
    &lt;PROPERTY NAME="commentStart" VALUE="/*" /&gt;
    &lt;PROPERTY NAME="commentEnd" VALUE="*/" /&gt;
    &lt;PROPERTY NAME="lineComment" VALUE="//" /&gt;
    &lt;PROPERTY NAME="wordBreakChars" VALUE=",+-=&amp;lt;&amp;gt;/?^&amp;amp;*" /&gt;

    &lt;!-- Auto indent --&gt;
    &lt;PROPERTY NAME="indentOpenBrackets" VALUE="{" /&gt;
    &lt;PROPERTY NAME="indentCloseBrackets" VALUE="}" /&gt;
    &lt;PROPERTY NAME="indentNextLine"
    	VALUE="\s*(((if|while)\s*\(|else\s*|else\s+if\s*\(|for\s*\(.*\))[^{;]*)" /&gt;
    &lt;!-- set this to 'true' if you want to use GNU coding style --&gt;
    &lt;PROPERTY NAME="doubleBracketIndent" VALUE="false" /&gt;
    &lt;PROPERTY NAME="lineUpClosingBracket" VALUE="true" /&gt;
&lt;/PROPS&gt;</t>
<t tx="ekr.20050529180421.39">RULES tags must be placed inside the MODE tag. Each RULES tag defines a ruleset.
A ruleset consists of a number of parser rules, with each parser rule specifying
how to highlight a specific syntax token. There must be at least one ruleset in
each edit mode. There can also be more than one, with different rulesets being
used to highlight different parts of a buffer (for example, in HTML mode, one
rule set highlights HTML tags, and another highlights inline JavaScript). For
information about using more than one ruleset, see the section called “The SPAN
Tag”.

The RULES tag supports the following attributes, all of which are optional: 

SET the name of this ruleset. All rulesets other than the first must have a
name.

IGNORE_CASE if set to FALSE, matches will be case sensitive. Otherwise, case
will not matter. Default is TRUE.

NO_WORD_SEP Any non-alphanumeric character not in this list is treated as a word
separator for the purposes of syntax highlighting.

DEFAULT The token type for text which doesn't match any specific rule. Default
is NULL. See the section called “Token Types” for a list of token types.

HIGHLIGHT_DIGITS DIGIT_RE

If the HIGHLIGHT_DIGITS attribute is set to TRUE, jEdit will attempt to
highlight numbers in this ruleset.

Any word consisting entirely of digits (0-9) will be highlighted with the DIGIT
token type. A word that contains other letters in addition to digits will be
highlighted with the DIGIT token type only if it matches the regular expression
specified in the DIGIT_RE attribute. If this attribute is not specified, it will
not be highlighted.

Here is an example DIGIT_RE regular expression that highlights Java-style
numeric literals (normal numbers, hexadecimals prefixed with 0x, numbers
suffixed with various type indicators, and floating point literals containing an
exponent):

DIGIT_RE="(0x[[:xdigit:]]+|[[:digit:]]+(e[[:digit:]]*)?)[lLdDfF]?"

Here is an example RULES tag:

&lt;RULES IGNORE_CASE="FALSE" HIGHLIGHT_DIGITS="TRUE"&gt;
    ... parser rules go here ...
&lt;/RULES&gt;</t>
<t tx="ekr.20050529180421.40">The SEQ rule, which must be placed inside a RULES tag, highlights fixed
sequences of text. The text to highlight is specified between opening and
closing SEQ tags. The following attributes are supported:

TYPE - the token type to highlight the sequence with. See the section called
“Token Types” for a list of token types.

AT_LINE_START - If set to TRUE, the sequence will only be highlighted if it
occurs at the beginning of a line.

AT_WHITESPACE_END - If set to TRUE, the sequence will only be highlighted if it
is the first non-whitespace text in the line.

AT_WORD_START - If set to TRUE, the sequence will only be highlighted if it
occurs at the beginning of a word.

DELEGATE - if this attribute is specified, all text after the sequence will be
highlighted using this ruleset. To delegate to a ruleset defined in the current
mode, just specify its name. To delegate to a ruleset defined in another mode,
specify a name of the form mode::ruleset. Note that the first (unnamed) ruleset
in a mode is called “MAIN”.

The following rules highlight a few Java operators:

&lt;SEQ TYPE="OPERATOR"&gt;+&lt;/SEQ&gt;
&lt;SEQ TYPE="OPERATOR"&gt;-&lt;/SEQ&gt;
&lt;SEQ TYPE="OPERATOR"&gt;*&lt;/SEQ&gt;
&lt;SEQ TYPE="OPERATOR"&gt;/&lt;/SEQ&gt;</t>
<t tx="ekr.20050529180421.41">The SEQ_REGEXP rule is similar to the SEQ rule except the match sequence is
taken to be a regular expression.

In addition to the attributes supported by the SEQ tag, the HASH_CHAR attribute
must be specified. It must be set to the first character that the regular
expression matches. This rules out using regular expressions which can match
more than one character at the start position. The regular expression match
cannot span more than one line, either.

Here is an example of a SEQ_REGEXP rule that highlights Perl's matcher
constructions such as m/(.+):(\d+):(.+)/:

&lt;SEQ_REGEXP TYPE="MARKUP"
    HASH_CHAR="m"
    AT_WORD_START="TRUE"
&gt;m([[:punct:]])(?:.*?[^\\])*?\1[sgiexom]*&lt;/SEQ_REGEXP&gt;</t>
<t tx="ekr.20050529180421.42">The SPAN rule, which must be placed inside a RULES tag, highlights text between
a start and end string. The start and end strings are specified inside child
elements of the SPAN tag. The following attributes are supported:

TYPE - The token type to highlight the span with. See the section called “Token
Types” for a list of token types.

AT_LINE_START - If set to TRUE, the span will only be highlighted if the start
sequence occurs at the beginning of a line.

AT_WHITESPACE_END - If set to TRUE, the span will only be highlighted if the
start sequence is the first non-whitespace text in the line.

AT_WORD_START - If set to TRUE, the span will only be highlighted if the start
sequence occurs at the beginning of a word.

DELEGATE - text inside the span will be highlighted with the specified ruleset.
To delegate to a ruleset defined in the current mode, just specify its name. To
delegate to a ruleset defined in another mode, specify a name of the form
mode::ruleset. Note that the first (unnamed) ruleset in a mode is called
“MAIN”.

EXCLUDE_MATCH - If set to TRUE, the start and end sequences will not be
highlighted, only the text between them will.

NO_ESCAPE - If set to TRUE, the ruleset's escape character will have no effect
before the span's end string. Otherwise, the presence of the escape character
will cause that occurrence of the end string to be ignored.

NO_LINE_BREAK - If set to TRUE, the span will not cross line breaks.

NO_WORD_BREAK - If set to TRUE, the span will not cross word breaks.

Note that the AT_LINE_START, AT_WHITESPACE_END and AT_WORD_START attributes can
also be used on the BEGIN and END elements. Setting these attributes to the same
value on both elements has the same effect as setting them on the SPAN element.

Here is a SPAN that highlights Java string literals, which cannot include line breaks:

&lt;SPAN TYPE="LITERAL1" NO_LINE_BREAK="TRUE"&gt;
  &lt;BEGIN&gt;"&lt;/BEGIN&gt;
  &lt;END&gt;"&lt;/END&gt;
&lt;/SPAN&gt;

Here is a SPAN that highlights Java documentation comments by delegating to the “JAVADOC” ruleset defined elsewhere in the current mode:

&lt;SPAN TYPE="COMMENT2" DELEGATE="JAVADOC"&gt;
  &lt;BEGIN&gt;/**&lt;/BEGIN&gt;
  &lt;END&gt;*/&lt;/END&gt;
&lt;/SPAN&gt;

Here is a SPAN that highlights HTML cascading stylesheets inside &lt;STYLE&gt; tags by delegating to the main ruleset in the CSS edit mode:

&lt;SPAN TYPE="MARKUP" DELEGATE="css::MAIN"&gt;
  &lt;BEGIN&gt;&amp;lt;style&amp;gt;&lt;/BEGIN&gt;
  &lt;END&gt;&amp;lt;/style&amp;gt;&lt;/END&gt;
&lt;/SPAN&gt;</t>
<t tx="ekr.20050529180421.43">The SPAN_REGEXP rule is similar to the SPAN rule except the start sequence is
taken to be a regular expression.

In addition to the attributes supported by the SPAN tag, the HASH_CHAR attribute
must be specified. It must be set to the first character that the regular
expression matches. This rules out using regular expressions which can match
more than one character at the start position. The regular expression match
cannot span more than one line, either.

Any text matched by groups in the BEGIN regular expression is substituted in the
END string. See below for an example of where this is useful. 

Here is a SPAN_REGEXP rule that highlights “read-ins” in shell scripts:

&lt;SPAN_REGEXP HASH_CHAR="&lt;" TYPE="LITERAL1" DELEGATE="LITERAL"&gt;
    &lt;BEGIN&gt;&lt;![CDATA[&lt;&lt;[[:space:]'"]*([[:alnum:]_]+)[[:space:]'"]*]]&gt;&lt;/BEGIN&gt;
    &lt;END&gt;$1&lt;/END&gt;
&lt;/SPAN_REGEXP&gt;

Here is a SPAN_REGEXP rule that highlights constructs placed between &lt;#ftl and
&gt;, as long as the &lt;#ftl is followed by a word break:

&lt;SPAN_REGEXP TYPE="KEYWORD1" HASH_CHAR="&amp;lt;" DELEGATE="EXPRESSION"&gt;
    &lt;BEGIN&gt;&amp;lt;#ftl\&amp;gt;&lt;/BEGIN&gt;
    &lt;END&gt;&amp;gt;&lt;/END&gt;
&lt;/SPAN_REGEXP&gt;</t>
<t tx="ekr.20050529180421.44">The TERMINATE rule, which must be placed inside a RULES tag, specifies that
parsing should stop after the specified number of characters have been read from
a line.

The number of characters to terminate after should be specified with the AT_CHAR
attribute. Here is an example:

&lt;TERMINATE AT_CHAR="1" /&gt;

This rule is used in Patch mode, for example, because only the first character
of each line affects highlighting.</t>
<t tx="ekr.20050529220821"></t>
<t tx="ekr.20050529220821.1"></t>
<t tx="ekr.20050530065723"></t>
<t tx="ekr.20050530065723.47">def parse_jEdit_file(self,fileName,verbose=False):
    
    if not fileName:
        return None
    
    if not fileName.endswith('.xml'):
        fileName = fileName + '.xml'

    path = os.path.join(g.app.loadDir,'../','modes',fileName)
    path = os.path.normpath(path)
    
    try: f = open(path)
    except IOError:
        g.trace('can not open %s'%path)
        return None

    try:
        try:
            mode = None
            parser = xml.sax.make_parser()
            # Do not include external general entities.
            # The actual feature name is "http://xml.org/sax/features/external-general-entities"
            parser.setFeature(xml.sax.handler.feature_external_ges,0)
            handler = contentHandler(self.c,fileName,verbose=verbose)
            parser.setContentHandler(handler)
            parser.parse(f)
            # if verbose: handler.printSummary()
            mode = handler.getMode()
        except:
            g.es('unexpected exception parsing %s' % (fileName),color='red')
            g.es_exception()
    finally:
        f.close()
        return mode</t>
<t tx="ekr.20050601105358">def colorOneChunk(self,allowBreak=True):
    '''Colorize a fixed number of tokens.
    If not done, queue this method again to continue coloring later.'''
    s,i = self.chunk_s,self.chunk_i
    count = 0 ; self.chunk_count += 1
    # g.trace('%3d'%(self.chunk_count),self.incremental)
    if not self.incremental:
        self.incremental = True
        &lt;&lt; queue up this method the first time &gt;&gt;
        return
    while i &lt; len(s):
        count += 1
        # Exit only after finishing the row.  This reduces flash.
        if i == 0 or s[i-1] == '\n':
            if self.kill_chunk: return
            if self.incremental and allowBreak:
                if count &gt;= 50:
                    &lt;&lt; queue up this method &gt;&gt;
                    return
        for f,kind,token_type,delegate in self.rulesDict.get(s[i],self.defaultRulesList):
            n = f(self,s,i)
            if n &gt; 0:
                self.doRule(s,i,i+n,kind,token_type,delegate)
                i += n
                break
        else:
            if self.present_ruleset.defaultColor:
                self.colorRangeWithTag(s,i,i+1,self.present_ruleset.defaultColor.lower())
            # g.trace('no match')
            i += 1

    self.removeTagsFromRange(s,self.chunk_last_i,len(s))</t>
<t tx="ekr.20050601162452.1">self.chunk_s,self.chunk_i = s,i
self.c.frame.top.after_idle(self.colorOneChunk)</t>
<t tx="ekr.20050602150619">def init_mode (self,language):
    
    # bunch = self.modes.get(language)
    bunch = self.modes.get(language)
    if bunch:
        self.mode = bunch.mode
        self.defaultRulesList=bunch.defaultRulesList
        self.keywords = bunch.keywords
        self.rulesDict=bunch.rulesDict
        self.word_chars = bunch.word_chars
    else:
        self.mode = mode = self.parse_jEdit_file(language)
        if mode:
            g.trace(language)
            # Handle only the main rulese here.
            rulesets = mode.getRulesets()
            self.present_ruleset = ruleset = rulesets[0]
            # mode.printSummary (printStats=False)
            self.keywords,self.word_chars = self.init_keywords(mode,ruleset)
                # Sets self.word_chars: must be called before createRuleMatchers.
            self.createRuleMatchers(ruleset.rules)
                # Sets self.defaultRulesList &amp; self.rulesDict.
            bunch = g.bunch(mode=mode,
                defaultRulesList=self.defaultRulesList,
                keywords=self.keywords,
                rulesDict=self.rulesDict,
                word_chars=self.word_chars)
            self.modes[language] = bunch
        elif language:
            g.trace('No language description for %s' % language)</t>
<t tx="ekr.20050602152743">def init_keywords (self,mode,ruleset):
    
    '''Initialize the keywords for the present language.
    
     Set word_chars to all non-alpha characters appearing in any keyword'''

    # Add any new user keywords to leoKeywords.
    for d in g.globalDirectiveList:
        name = '@' + d
        if name not in leoKeywords:
            leoKeywords.append(name)
    # Create a single keywords dict.
    keywords = {}
    for key in leoKeywords:
        keywords[key] = 0

    for i in (1,2,3,4):
        keys = mode.getKeywords(i,ruleset)
        for key in keys:
            if keywords.get(key):
                print 'keyword %s defined in multiple places' % key
            keywords[key] = i
    # g.trace(len(keywords.keys()))
    # Create the word_chars list. 
    word_chars = {}
    for ch in string.letters:
        word_chars[ch] = None
    for keys in keywords.keys():
        for word in keys:
            for ch in word:
                word_chars[ch] = None
    if 0: # Testing.
        &lt;&lt; compute extra_word_chars &gt;&gt;
            
    return keywords,word_chars</t>
<t tx="ekr.20050602205810.4">def colorRangeWithTag (self,s,i,j,tag):

    if self.was_non_incremental:
        must_color = True
        self.removeOldTagsFromRange(s,self.chunk_last_i,j)
    elif self.rangeColoredWithTag(i,j,tag):
        must_color = False
        # Remove the old tags to i.
        self.removeTagsFromRange(s,self.chunk_last_i,i)
    else:
        must_color = True
        # Remove the old tags to j.
        self.removeTagsFromRange(s,self.chunk_last_i,j)

    if must_color:
        # Remember the new tags.
        for k in xrange(i,j):
            self.colored_ranges[k] = tag

        # Do the real coloring.
        row,col = g.convertPythonIndexToRowCol(s,i)
        x1 = '%d.%d' % (row+1,col)
        row,col = g.convertPythonIndexToRowCol(s,j)
        x2 = '%d.%d' % (row+1,col)
        self.body.tag_add(tag,x1,x2)

    self.chunk_last_i = j</t>
<t tx="ekr.20050605130806">self.chunk_s,self.chunk_i = s,i
self.c.frame.top.after(50,self.colorOneChunk)</t>
<t tx="ekr.20050606214954"></t>
<t tx="ekr.20050606221357"></t>
<t tx="ekr.20050607073917">extra_word_chars = {}
for ch in word_chars:
    if ch not in string.letters and ch not in extra_word_chars:
        extra_word_chars[ch] = None</t>
<t tx="ekr.20050607212958">def colorByDelegate(self,delegate,s,i,j,token_type):
    
    # g.trace(delegate,repr(s[i:j]))
    
    if -1 == delegate.find('::'):
        # Use the ruleset in the present mode.
        rulesetName = delegate
    else:
        # file::ruleset
        file,rulesetName = delegate.split('::')
        self.init_mode(file)
        
    ruleset = self.mode.getRuleset(name=rulesetName)
    if ruleset:
        # self.mode.printRuleset(ruleset,tag=delegate)
        # Save ivars
        ### Bug: this doesn't handle nested delegates.
        ### Fix: don't save here:  move the ivars to the ruleset class and keep a stack of rulesets.
        self.save_present_ruleset = self.present_ruleset
        self.save_keywords = self.keywords # A bunch.
        self.save_word_chars = self.word_chars.copy()
        self.save_defaultRulesList = self.defaultRulesList[:]
        self.save_rulesDict = self.rulesDict.copy()
        # Set ivars for the delegated string only.
        # Sart at the real zero so row/column numbers are computed properly.
        self.chunk_s = s[0:j+1]
        self.chunk_i = i # Required.
        self.present_ruleset = ruleset
        self.keywords,self.word_chars = self.init_keywords(self.mode,ruleset)
        self.createRuleMatchers(ruleset.rules) # Sets self.defaultRulesList &amp; self.rulesDict.
        # Do the coloring with no break.
        self.colorOneChunk(allowBreak=False) 
        # Restore ivars.
        self.chunk_s = s
        self.chunk_i = j+1
        self.present_ruleset = self.save_present_ruleset
        self.keywords = self.save_keywords
        self.word_chars = self.save_word_chars
        self.defaultRulesList = self.save_defaultRulesList
        self.rulesDict = self.save_rulesDict</t>
<t tx="ekr.20050607220512"># To do: honor default:comment3 attribute of ruleset.</t>
<t tx="ekr.20050612074047"></t>
<t tx="ekr.20050718142601"></t>
<t tx="ekr.20050718142601.1">@nocolor

- The find frame is no longer global, so g.app.findFrame no longer exists.

- Added gui arg in wxLeoFrame ctor.

- Changed trace to g.trace, es to g.es, etc.

- Changed calling sequence of setTopGeometry to (self,w,h,x,y,adjustSize=True):</t>
<t tx="ekr.20050718142601.3"># The find window is no longer global.

g.app.findFrame = wxFindFrame()
g.app.globalWindows.append(g.app.findFrame)</t>
<t tx="ekr.20050718151826"></t>
<t tx="ekr.20050722075812">for p in p.self_and_subtree_iter():
    s = p.bodyString()
    target = s.rstrip()
    if s != target:
        p.setBodyStringOrPane(target)
        g.es(p.headString())</t>
<t tx="ekr.20050724100334">c.prettyPrintPythonNode()</t>
<t tx="ekr.20050817115636.2">import sys
sys.path.append(r'c:\reportlab_1_20') 

if 1: # This dependency could easily be removed.
    # Used only for tracing and error reporting.
    import leoGlobals as g
    
try:
    # from reportlab.lib.enums import *
    # from reportlab.platypus import *
    
    # Formatting imports...
    import docutils
    import reportlab.platypus
    import reportlab.platypus.para
    import stylesheet # To do: get this a better way.
    
    # General imports...
    import StringIO
    import time
    import types
except ImportError:
    pass



</t>
<t tx="ekr.20050817115636.4">class Writer (docutils.writers.Writer):
	
	&lt;&lt; class Writer declarations &gt;&gt;

	@others</t>
<t tx="ekr.20050817115636.5">supported = ('pdf','rlpdf')
"""Formats this writer supports."""

settings_spec = (
    'PDF-Specific Options',
    None,
    (
        # EKR: added this entry.
    (   'Specify a stylesheet URL, used verbatim.  Overrides '
        '--stylesheet-path.  Either --stylesheet or --stylesheet-path '
        'must be specified.',
        ['--stylesheet'],
        {'metavar': '&lt;URL&gt;', 'overrides': 'stylesheet_path'}),
         
    (   'Specify a stylesheet file, relative to the current working '
        'directory.  The path is adjusted relative to the output HTML '
        'file.  Overrides --stylesheet.',
        ['--stylesheet-path'],
        {'metavar': '&lt;file&gt;', 'overrides': 'stylesheet'}),

    (   'Format for footnote references: one of "superscript" or '
        '"brackets".  Default is "brackets".',
        ['--footnote-references'],
        {'choices': ['superscript', 'brackets'], 'default': 'brackets',
        'metavar': '&lt;FORMAT&gt;'}),
    )
)

output = None
"""Final translated form of `document`."""</t>
<t tx="ekr.20050817115636.6">def __init__(self):

    docutils.writers.Writer.__init__(self)

    # self.translator_class = PDFTranslator</t>
<t tx="ekr.20050817115636.7">def translate(self):
    
    '''Do final translation of self.document into self.output.'''
    
    if 1: # Production code.
        visitor = PDFTranslator(self,self.document)
    else: # Use intermediate file, and dummy pdf translator.
        # We can modify the intermediate file by hand to test proposed code generation.
        try:
            filename = 'intermediateFile.txt'
            s = file(filename).read()
            # g.trace('creating .pdf file from %s...' % filename)
            visitor = dummyPDFTranslator(self,self.document,s)
        except IOError:
            # g.trace('can not open %s' % filename)
            return

    # Create a list of paragraphs using Platypus.
    self.document.walkabout(visitor)
    story = visitor.as_what()
    
    if 0: # Not useful: story is a list of reportlab.platypus.para.Para objects.
        # Use the trace in createParagraph instead.
        g.trace('story','*'*40)
        print story        
    
    # Generate self.output.  Gets sent to reportlab.
    self.output = self.createPDF_usingPlatypus(story)
    # Solve the newline problem by brute force.
    self.output = self.output.replace('\n\r','\n')
    self.output = self.output.replace('\r\n','\n')
    if 0: # This is the actual .pdf output returned from doc.build(story)
        # doc is a Platypus (and this reportlab) document.
        g.trace('output','*'*40)
        lines = g.splitLines(self.output)
        g.printList(lines)</t>
<t tx="ekr.20050817115636.8">def createPDF_usingPlatypus (self,story):

    out = StringIO.StringIO()

    doc = reportlab.platypus.SimpleDocTemplate(out,
        pagesize=reportlab.lib.pagesizes.A4)

    doc.build(story)

    return out.getvalue()</t>
<t tx="ekr.20050817115636.9">def lower(self):

    return 'pdf'</t>
<t tx="ekr.20050817120850.1">@first #! /usr/bin/env python

&lt;&lt; docstring &gt;&gt;

# Note: you must copy this file to the Python/Lib/site-packages/docutils/writers folder.

@language python
@tabwidth -4

&lt;&lt; about this code &gt;&gt;
&lt;&lt; copyright &gt;&gt;
&lt;&lt; version history &gt;&gt;
&lt;&lt; to do &gt;&gt;

__version__ = '0.4'
__docformat__ = 'reStructuredText'
&lt;&lt; imports &gt;&gt;

@others</t>
<t tx="ekr.20050817120850.10">class PDFTranslator (docutils.nodes.NodeVisitor):

	@others

    depart_comment = invisible_visit
    visit_substitution_definition = visit_comment
    depart_substitution_definition = depart_comment
    visit_figure = visit_comment
    depart_figure = depart_comment

    visit_sidebar = invisible_visit
    visit_warning = invisible_visit
    visit_tip = invisible_visit
    visit_tbody = invisible_visit
    visit_thead = invisible_visit
    visit_tgroup = invisible_visit
    visit_table = invisible_visit
    visit_title_reference = invisible_visit
    visit_transition = invisible_visit
    visit_pending = invisible_visit
    depart_pending = invisible_visit
    depart_transition = invisible_visit
    depart_title_reference = invisible_visit
    depart_table = invisible_visit
    depart_tgroup = invisible_visit
    depart_thead = invisible_visit
    depart_tbody = invisible_visit
    depart_tip = invisible_visit
    depart_warning = invisible_visit
    depart_sidebar = invisible_visit</t>
<t tx="ekr.20050817120850.11">def __init__(self, writer,doctree):

    self.writer = writer
    self.settings = settings = doctree.settings
    self.styleSheet = stylesheet.getStyleSheet()
    docutils.nodes.NodeVisitor.__init__(self, doctree) # Init the base class.
    self.language = docutils.languages.get_language(doctree.settings.language_code)
    
    self.in_docinfo = False
    self.head = [] # Set only by meta() method.  
    self.body = [] # The body text being accumulated.
    self.foot = []
    self.sectionlevel = 0
    self.context = []
    
    self.story = []
    self.bulletText = '\267'
        # maybe move this into stylesheet.
        # This looks like the wrong glyph.

    if 0: # no longer used.
        self.topic_class = ''
        self.bulletlevel = 0
</t>
<t tx="ekr.20050817120850.12">def as_what(self):

    return self.story
</t>
<t tx="ekr.20050817120850.13">def encode(self, text):

    """Encode special characters in `text` &amp; return."""
    if type(text) is types.UnicodeType:
        text = text.replace(u'\u2020', u' ')
        text = text.replace(u'\xa0', u' ')
        text = text.encode('utf-8')
    #text = text.replace("&amp;", "&amp;amp;")
    #text = text.replace("&lt;", '"')
    #text = text.replace('"', "(quot)")
    #text = text.replace("&gt;", '"')
    # footnotes have character values above 128 ?
    return text
</t>
<t tx="ekr.20050817120850.14">def createParagraph (self,text,style='Normal',bulletText=None):

    if type(text) in (types.ListType,types.TupleType):
        text = ''.join([self.encode(t) for t in text])

    if not style.strip(): ### EKR
        style = 'Normal'
        
    if 0:
        s = text.split('&gt;')
        s = '&gt;\n'.join(s)
        print
        if 1: # just print the text.
            print s
        else:
            g.trace('%8s\n\n%s' % (style,s))
        print

    style = self.styleSheet [style]
    
    try:
        self.story.append(
            reportlab.platypus.para.Paragraph (
                self.encode(text), style,
                bulletText = bulletText,
                context = self.styleSheet))
    except Exception:
        g.es_print('Exception in createParagraph')
        g.es_exception()
        self.dumpContext()
        raise</t>
<t tx="ekr.20050817120850.15"># The suffix is always '\n' except for a cant-happen situation.

def starttag (self,node,tagname,suffix='\n',caller='',**attributes):
    
    # g.trace(repr(attributes))
    atts = {}
    for (name,value) in attributes.items():
        atts [name.lower()] = value
    for att in ('class',): # append to node attribute
        if node.has_key(att):
            if atts.has_key(att):
                atts [att] = node [att] + ' ' + atts [att]
    for att in ('id',): # node attribute overrides
        if node.has_key(att):
            atts [att] = node [att]
    
    attlist = atts.items() ; attlist.sort()
    parts = [tagname]
    # Convert the attributes in attlist to a single string.
    for name, value in attlist:
        # g.trace('attlist element:',repr(name),repr(value))
        if value is None: # boolean attribute
            parts.append(name.lower().strip())
        elif isinstance(value,types.ListType):
            values = [str(v) for v in value]
            val = ' '.join(values).strip()
            parts.append('%s="%s"' % (
                name.lower(), self.encode(val)))
        else:
            parts.append('%s="%s"' % (
                name.lower(),self.encode(str(value).strip())))

    val = '&lt;%s&gt;%s' % (' '.join(parts),suffix)
    # g.trace('%-24s %s' % (caller,val))
    return val</t>
<t tx="ekr.20050817120850.18">def visit_admonition(self, node, name):
    pass

def depart_admonition(self):
    pass
</t>
<t tx="ekr.20050817120850.20">def visit_attention(self, node):

    self.visit_admonition(node, 'attention')

def depart_attention(self, node):

    self.depart_admonition()
</t>
<t tx="ekr.20050817120850.22">def visit_author(self, node):
    self.visit_docinfo_item(node, 'author')

def depart_author(self, node):
    self.depart_docinfo_item()
</t>
<t tx="ekr.20050817120850.24">def visit_address(self, node):
    self.visit_docinfo_item(node, 'address')

def depart_address(self, node):
    self.depart_docinfo_item()
</t>
<t tx="ekr.20050817120850.26">def visit_version(self, node):
    self.visit_docinfo_item(node, 'version')

def depart_version(self, node):
    self.depart_docinfo_item()
</t>
<t tx="ekr.20050817120850.28">def visit_system_message(self, node):
    pass

def depart_system_message(self, node):
    pass
</t>
<t tx="ekr.20050817120850.30">def visit_term (self,node):

    self.push(kind='dt')

    self.body.append(
        self.starttag(node,'dt',suffix='',caller='visit_term'))

def depart_term (self,node):

    self.pop('dt')</t>
<t tx="ekr.20050817120850.32">def visit_authors(self, node):
    pass

def depart_authors(self, node):
    pass
</t>
<t tx="ekr.20050817120850.34">def visit_block_quote(self, node):
    pass
    
def depart_block_quote(self, node):
    pass</t>
<t tx="ekr.20050817120850.36">def visit_bullet_list(self, node):
    
    self.push(kind='ul',start=len(self.body))

    # At present self.bulletText is a constant.
    self.body.append('&lt;ul bulletText="%s"&gt;' % self.bulletText)

def depart_bullet_list(self, node):
    
    b = self.pop('ul')

    self.body.append('&lt;/ul&gt;')
    
    if not self.inContext('ul'):
        self.putTail(b.start)</t>
<t tx="ekr.20050817120850.39">def visit_caption(self, node):
    pass

def depart_caption(self, node):
    pass
</t>
<t tx="ekr.20050817120850.40">def visit_caution(self, node):
    self.visit_admonition(node, 'caution')

def depart_caution(self, node):
    self.depart_admonition()
</t>
<t tx="ekr.20050817120850.42">def visit_citation(self, node):
    pass

def depart_citation(self, node):
    pass
</t>
<t tx="ekr.20050817120850.44">def visit_citation_reference(self, node):
    pass

def depart_citation_reference(self, node):
    pass
</t>
<t tx="ekr.20050817120850.46">def visit_classifier(self, node):
    pass

def depart_classifier(self, node):
    pass
</t>
<t tx="ekr.20050817120850.48">def visit_colspec(self, node):
    pass

def depart_colspec(self, node):
    pass
</t>
<t tx="ekr.20050817120850.50">def visit_contact(self, node):
    
    self.visit_docinfo_item(node, 'contact')

def depart_contact(self, node):

    self.depart_docinfo_item()
</t>
<t tx="ekr.20050817120850.52">def visit_copyright(self, node):
    
    self.visit_docinfo_item(node, 'copyright')

def depart_copyright(self, node):

    self.depart_docinfo_item()
</t>
<t tx="ekr.20050817120850.54">def visit_danger(self, node):
    
    self.visit_admonition(node, 'danger')

def depart_danger(self, node):

    self.depart_admonition()
</t>
<t tx="ekr.20050817120850.56">def visit_date(self, node):
    
    self.visit_docinfo_item(node, 'date')

def depart_date(self, node):
    
    self.depart_docinfo_item()

</t>
<t tx="ekr.20050817120850.58">def visit_definition(self, node):
    
    self.push(kind='dd')

    self.body.append('&lt;/dt&gt;')
    self.body.append(
        self.starttag(node,'dd',caller='visit_destination'))

def depart_definition(self, node):
    
    self.pop('dd')
    self.body.append('&lt;/dd&gt;')</t>
<t tx="ekr.20050817120850.60">def visit_definition_list(self, node):
    
    self.push(kind='dl',start=len(self.body))
    
    self.body.append(self.starttag(node, 'dl'))

def depart_definition_list(self, node):
    
    b = self.pop('dl')

    self.body.append('&lt;/dl&gt;')

    if not self.inContext('dl'):
        self.putTail(b.start)
</t>
<t tx="ekr.20050817120850.62">def visit_definition_list_item(self, node):
    pass

def depart_definition_list_item(self, node):
    pass</t>
<t tx="ekr.20050817120850.64">def visit_description(self, node):
    pass

def depart_description(self, node):
    pass
</t>
<t tx="ekr.20050817120850.66"></t>
<t tx="ekr.20050817120850.68">def visit_docinfo_item(self, node, name):
    
    self.body.append(
        '&lt;para style="DocInfo"&gt;&lt;b&gt;%s: &lt;/b&gt;' % (
            self.language.labels[name]))

def depart_docinfo_item(self):
    
    self.body.append('&lt;/para&gt;')
</t>
<t tx="ekr.20050817120850.70">def visit_doctest_block(self, node):
    
    self.visit_literal_block(node)

def depart_doctest_block(self, node):
    
    self.depart_literal_block(node)

</t>
<t tx="ekr.20050817120850.72">def visit_line_block(self, node):
    self.visit_literal_block(node)

def depart_line_block(self, node):
    self.depart_literal_block(node)
</t>
<t tx="ekr.20050817120850.74">def visit_document(self, node):
    pass
    
def depart_document(self, node):
    pass</t>
<t tx="ekr.20050817120850.76">def visit_emphasis(self, node):
    
    self.push(kind='i')
    
    self.body.append('&lt;i&gt;')

def depart_emphasis(self, node):
    
    self.pop('i')

    self.body.append('&lt;/i&gt;')
</t>
<t tx="ekr.20050817120850.78">def visit_entry(self, node):
    pass

def depart_entry(self, node):
    pass
</t>
<t tx="ekr.20050817120850.80">def visit_enumerated_list(self, node):
    
    self.push(kind='ol',start=len(self.body))

    self.body.append('&lt;ol&gt;')

def depart_enumerated_list(self, node):
    
    b = self.pop('ol')

    self.body.append('&lt;/ol&gt;')

    if not self.inContext('ol'):
        self.putTail(b.start)</t>
<t tx="ekr.20050817120850.82">def visit_error(self, node):
    self.visit_admonition(node, 'error')

def depart_error(self, node):
    self.depart_admonition()</t>
<t tx="ekr.20050817120850.84">def visit_field(self, node):
    
    self.body.append('&lt;para&gt;')

def depart_field(self, node):

    self.body.append('&lt;/para&gt;')
</t>
<t tx="ekr.20050817120850.86">def visit_field_argument(self, node):
    pass

def depart_field_argument(self, node):
    pass
</t>
<t tx="ekr.20050817120850.88">def visit_field_list(self, node):
    
    self.push(kind='&lt;para&gt;',start=len(self.body))

def depart_field_list(self, node):
    
    b = self.pop('&lt;para&gt;')
    
    self.body.append('&lt;/para&gt;')
    
    self.putTail(b.start)</t>
<t tx="ekr.20050817120850.90">def visit_field_name(self, node):

    self.body.append('&lt;b&gt;')

def depart_field_name(self, node):

    self.body.append(': &lt;/b&gt;')</t>
<t tx="ekr.20050817120850.92">def visit_field_body(self, node):
    pass

def depart_field_body(self, node):
    pass
</t>
<t tx="ekr.20050817120850.94">def visit_footnote(self, node):
    
    self.push(kind='footnotes',context=[])

    self.footnote_backrefs(node)

def depart_footnote(self, node):
    
    self.pop('footnotes')

    self.footnote_backrefs_depart(node)
</t>
<t tx="ekr.20050817120850.95">@ Bug fixes, EKR 8/22/05:
    - Get attributes from node.attributes, not node.
    - The proper key is 'ids', not 'id'
Warning: this does not work for auto-numbered footnotes.
@c

def footnote_backrefs (self,node):
    
    '''Create b.link and b.setLink for visit/depart_label.'''
    
    # self.dumpNode(node,tag='backrefs-node')
    
    b = self.peek('footnotes')
    a = node.attributes ; backrefs = a.get('backrefs',[]) # EKR.

    # Set b.setLink.
    b.setLink = self.starttag(
        {},'setLink','',destination=a['ids']) # EKR.

    # Set b.links.
    b.links = []
    if self.settings.footnote_backlinks:
        for backref in backrefs:
            b.links.append(
                self.starttag(
                    {},'link',suffix='',destination=backref))</t>
<t tx="ekr.20050817120850.96">def footnote_backrefs_depart(self, node):

    if not self.context and self.body:
        self.createParagraph(self.body)
        self.body = []
</t>
<t tx="ekr.20050817120850.98">@ Bug fixes, EKR 8/22/05:
    - Get attributes from node.attributes, not node.
    - The proper key is 'ids', not 'id'
@c

def visit_footnote_reference (self,node):
    
    '''Generate code for a footnote reference.'''
    
    # self.dumpNode(node,tag='footnote-ref-node')

    markup = [] # The terminating markup to be supplied by depart_footnote_reference.
    a = node.attributes # EKR.
    if self.settings.footnote_backlinks and a.get('ids'):
        self.body.append(
            self.starttag(node,'setLink','',destination=a['ids']))
        markup.append('&lt;/setLink&gt;')
    
    if   node.hasattr('refid'):   href = a ['refid']
    elif node.hasattr('refname'): href = self.document.nameids [a ['refname']]
    else:                         href = ''
    # g.trace('href:',href)

    format = self.settings.footnote_references
    if format == 'brackets':
        suffix = '[' ; markup.append(']')
    elif format == 'superscript':
        suffix = '&lt;super&gt;' ; markup.append('&lt;/super&gt;')
    else: # shouldn't happen
        suffix = None

    if suffix:
        self.body.append(
            self.starttag(node,'link',suffix,destination=href))
        markup.append('&lt;/link&gt;')

    markup.reverse()
    self.push(kind='footnote-ref',markup=markup)</t>
<t tx="ekr.20050817120850.99">def depart_footnote_reference(self, node):
    
    b = self.pop('footnote-ref')
    
    for z in b.markup:
        self.body.append(z)</t>
<t tx="ekr.20050817120850.100">def visit_hint(self, node):
    self.visit_admonition(node, 'hint')

def depart_hint(self, node):
    self.depart_admonition()
</t>
<t tx="ekr.20050817120850.102">def visit_image(self, node):
    pass

def depart_image(self, node):
    pass
</t>
<t tx="ekr.20050817120850.105">def visit_important(self, node):
    self.visit_admonition(node, 'important')

def depart_important(self, node):
    self.depart_admonition()
</t>
<t tx="ekr.20050817120850.106">def visit_interpreted(self, node):
    pass

def depart_interpreted(self, node):
    pass
</t>
<t tx="ekr.20050817120850.108">def visit_label(self, node):
    
    b = self.inContext('footnotes')
    if b:
        self.body.append(b.setLink)
        self.body.append('&lt;/setLink&gt;')
        # Start all links.
        for link in b.links:
            self.body.append(link)
        self.body.append('[')

def depart_label(self, node):
    
    b = self.inContext('footnotes')
    if b:
        self.body.append(']')
        # End all links.
        for link in b.links:
            self.body.append('&lt;/link&gt;')
        # Who knows why this is here...
        self.body.append('   ')</t>
<t tx="ekr.20050817120850.110">def visit_legend(self, node):
    pass

def depart_legend(self, node):
    pass
</t>
<t tx="ekr.20050817120850.112">def visit_list_item(self, node):
    
    self.push(kind='li')
    
    self.body.append('&lt;li&gt;')

def depart_list_item(self, node):
    
    self.pop('li')

    self.body.append('&lt;/li&gt;')
</t>
<t tx="ekr.20050817120850.114">def visit_literal(self, node):
    
    self.push(kind='literal')
    
def depart_literal(self, node):
    
    self.pop('literal')</t>
<t tx="ekr.20050817120850.116">def visit_literal_block(self, node):
    
    self.story.append(
        reportlab.platypus.Preformatted(
            node.astext(),self.styleSheet['Code']))

    raise docutils.nodes.SkipNode

def depart_literal_block(self, node):
    pass</t>
<t tx="ekr.20050817120850.118">def visit_meta(self, node):
    
    g.trace(**node.attributes)

    self.head.append(
        self.starttag(node, 'meta', **node.attributes))

def depart_meta(self, node):

    pass</t>
<t tx="ekr.20050817120850.120">def visit_note(self, node):
    
    self.visit_admonition(node, 'note')

def depart_note(self, node):

    self.depart_admonition()
</t>
<t tx="ekr.20050817120850.122">def visit_option(self, node):
    pass

def depart_option(self, node):
    pass
</t>
<t tx="ekr.20050817120850.124">def visit_option_argument(self, node):
    pass

def depart_option_argument(self, node):
    pass
</t>
<t tx="ekr.20050817120850.126">def visit_option_group(self, node):
    pass

def depart_option_group(self, node):
    pass
</t>
<t tx="ekr.20050817120850.128">def visit_option_list(self, node):
    
    self.push(kind='option-list',start=len(self.body))

def depart_option_list(self, node):
    
    b = self.pop('option-list')

    if not self.inContext('option_list'):
        self.putTail(b.start)
        </t>
<t tx="ekr.20050817120850.130">def visit_option_list_item(self, node):
    pass

def depart_option_list_item(self, node):
    pass
</t>
<t tx="ekr.20050817120850.132">def visit_option_string(self, node):
    pass

def depart_option_string(self, node):
    pass
</t>
<t tx="ekr.20050817120850.134">def visit_organization(self, node):
    
    self.visit_docinfo_item(node, 'organization')

def depart_organization(self, node):

    self.depart_docinfo_item()
</t>
<t tx="ekr.20050817120850.138">def visit_problematic(self, node):
    pass

def depart_problematic(self, node):
    pass
</t>
<t tx="ekr.20050817120850.140">def visit_raw(self, node):

    if node.has_key('format') and node['format'] == 'html':
        self.body.append(node.astext())

    raise docutils.nodes.SkipNode
</t>
<t tx="ekr.20050817120850.141">def visit_target (self,node):

    if not (
        node.has_key('refuri') or
        node.has_key('refid') or
        node.has_key('refname')
    ):
        href = ''
        if node.has_key('id'):
            href = node ['id']
        elif node.has_key('name'):
            href = node ['name']
        self.body.append("%s%s" % (
            self.starttag(node,'setLink',suffix='',
                destination=href,caller='visit_targtet'),
            '&lt;/setLink&gt;'))
    raise docutils.nodes.SkipNode

def depart_target (self,node):
    pass</t>
<t tx="ekr.20050817120850.143">def visit_reference (self,node):

    markup = [] ; caller = 'visit_reference'

    if node.has_key('refuri'):
        href = node ['refuri']
        self.body.append(
            self.starttag(node,'a',suffix='',href=href,caller=caller))
        markup.append('&lt;/a&gt;')
    else:
        if node.has_key('id'):
            self.body.append(
                self.starttag({},'setLink','',
                    destination=node['id'],caller=caller))
            markup.append('&lt;/setLink&gt;')
        if node.has_key('refid'):
            href = node ['refid']
        elif node.has_key('refname'):
            href = self.document.nameids [node ['refname']]
        self.body.append(
            self.starttag(node,'link','',destination=href,caller=caller))
        markup.append('&lt;/link&gt;')

    self.push(kind='a',markup=markup)
</t>
<t tx="ekr.20050817120850.144">def depart_reference(self, node):
    
    b = self.pop('a')

    for s in b.markup:
        self.body.append(s)</t>
<t tx="ekr.20050817120850.145">def visit_revision(self, node):

    self.visit_docinfo_item(node, 'revision')

def depart_revision(self, node):

    self.depart_docinfo_item()
</t>
<t tx="ekr.20050817120850.147">def visit_row(self, node):
    pass

def depart_row(self, node):
    pass
</t>
<t tx="ekr.20050817120850.149">def visit_section(self, node):
    
    self.sectionlevel += 1

def depart_section(self, node):

    self.sectionlevel -= 1
</t>
<t tx="ekr.20050817120850.151">def visit_status(self, node):
    
    self.visit_docinfo_item(node, 'status')

def depart_status(self, node):

    self.depart_docinfo_item()
</t>
<t tx="ekr.20050817120850.153">def visit_strong(self, node):
    
    self.push(kind='b')

    self.body.append('&lt;b&gt;')

def depart_strong(self, node):
    
    self.pop('b')

    self.body.append('&lt;/b&gt;')

</t>
<t tx="ekr.20050817120850.155">def visit_subtitle(self, node):
    
    self.push(kind='subtitle',start=len(self.body))

def depart_subtitle(self, node):
    
    b = self.pop('subtitle')

    self.putTail(b.start,b.style)
</t>
<t tx="ekr.20050817120850.157">def visit_title (self,node):

    caller='visit_title'
    start = len(self.body) ; markup = []
    isTopic = isinstance(node.parent,docutils.nodes.topic)
    isTitle = self.sectionlevel == 0
    
    # Set the style.
    if isTopic:   style = 'topic-title'
    elif isTitle: style = 'title'
    else:         style = "h%s" % self.sectionlevel

    ## The old code was equivalent to: if style != 'title'.
    if 0:
        self.dumpNode(node.parent,tag='node.parent')
        self.dumpNode(node,tag='node')
    # Bug fix: 8/21/05: changed 'id' to 'ids'.
    if node.parent.hasattr('ids'):
        self.body.append(
        self.starttag({},'setLink','',
            destination=node.parent['ids'],caller=caller))
        markup.append('&lt;/setLink&gt;')
    if node.hasattr('refid'):
        self.body.append(
        self.starttag({},'setLink','',
            destination=node['refid'],caller=caller))
        markup.append('&lt;/setLink&gt;')

    self.push(kind='title',markup=markup,start=start,style=style)</t>
<t tx="ekr.20050817120850.158">def depart_title (self,node):

    b = self.pop('title')

    for z in b.markup:
        self.body.append(z)
        
    self.putTail(b.start,style=b.style)</t>
<t tx="ekr.20050817120850.159">def unimplemented_visit(self, node):
    
    raise NotImplementedError(
        'visiting unimplemented node type: %s' % node.__class__.__name__)
</t>
<t tx="ekr.20050817120850.160">def visit_topic (self,node):

    if node.hasattr('id'):
        self.push(kind='topic-id',markup='&lt;/setLink&gt;')
        self.body.append(self.starttag({},'setLink',
            suffix='',destination=node['id'],caller='visit_topic'))

def depart_topic (self,node):

    if node.hasattr('id'):
        b = self.pop('topic-id')
        self.body.append(b.markup)

</t>
<t tx="ekr.20050817120850.162">def visit_generated(self, node):
    pass

def depart_generated(self, node):
    pass
</t>
<t tx="ekr.20050817120850.164">def invisible_visit(self, node):
    
    """Invisible nodes should be ignored."""
    pass</t>
<t tx="ekr.20050817120850.165">def visit_comment(self, node):

    raise docutils.nodes.SkipNode
</t>
<t tx="ekr.20050817122915">'''This NOT a Leo plugin: this is a docutils writer for .pdf files.  

That file uses the reportlab module to convert html markup to pdf.

The original code written by Engelbert Gruber.

Rewritten by Edward K. Ream for the Leo rst3 plugin.
'''
</t>
<t tx="ekr.20050817124859">#####################################################################################
#
#	Copyright (c) 2000-2001, ReportLab Inc.
#	All rights reserved.
#
#	Redistribution and use in source and binary forms, with or without modification,
#	are permitted provided that the following conditions are met:
#
#		*	Redistributions of source code must retain the above copyright notice,
#			this list of conditions and the following disclaimer. 
#		*	Redistributions in binary form must reproduce the above copyright notice,
#			this list of conditions and the following disclaimer in the documentation
#			and/or other materials provided with the distribution. 
#		*	Neither the name of the company nor the names of its contributors may be
#			used to endorse or promote products derived from this software without
#			specific prior written permission. 
#
#	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#	ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#	WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#	IN NO EVENT SHALL THE OFFICERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#	INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
#	TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#	OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
#	IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
#	IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#	SUCH DAMAGE.
#
#####################################################################################</t>
<t tx="ekr.20050817124859.1">@

- Added 'c:\reportlab_1_20' to sys.path.

- Obtained this file and stylesheet.py from
  http://docutils.sourceforge.net/sandbox/dreamcatcher/rlpdf/

- Put stylesheet.py in docutils/writers directory.
  This is a stylesheet class used by the file.

- Made minor mods to stop crashes.
    - Added support for the '--stylesheet' option.
        - This may be doing more harm than good.
    - Changed the following methods of the PDFTranslator class:
        - createParagraph
        - depart_title</t>
<t tx="ekr.20050817132814"></t>
<t tx="ekr.20050817135706">def visit_Text (self,node):

    self.push(kind='#text')

    self.body.append(node.astext())

def depart_Text (self,node):

    self.pop('#text')</t>
<t tx="ekr.20050817135706.1"></t>
<t tx="ekr.20050817142135">def visit_paragraph(self, node):
    
    self.push(kind='p',start=len(self.body))
    
def depart_paragraph(self, node):
    
    b = self.pop('p')
    
    if not self.context and self.body:
        self.putTail(b.start)</t>
<t tx="ekr.20050817142135.1"></t>
<t tx="ekr.20050817165745">@nocolor
@others</t>
<t tx="ekr.20050817165745.1">@

- Removed '\r' characters in Writer.translate.
- Created self.push and self.pop.
- Rewrote visit/depart_title.  The code now is clear and works properly.

To do:
    The code in several places uses x in self.context.
    This won't work when g.Bunches are on the context stack,
    so we shall need a method that searches the bunches on the stack.</t>
<t tx="ekr.20050818022030">def push (self,**keys):
    
    self.context.append(Bunch(**keys))
    
def pop (self,kind):
    
    bunch = self.context.pop()
    assert bunch.kind == kind,\
        'wrong bunch kind popped.  Expected: %s Got: %s' % (
            kind, bunch.kind)

    return bunch
    
def peek (self,kind):
    
    bunch = self.context[-1]
    assert bunch.kind == kind,\
        'peek at wrong bunch.  Expected: %s Got: %s' % (
            kind, bunch.kind)
    return bunch</t>
<t tx="ekr.20050818033610">@

- Fixed bug in visit_reference: added self.push(b).
- Added putHead, putTail utilities.
- Simplified most of the code.
- Reorganized node handlers so that it is clear what the important methods are.
- Almost all the grunt work is done.</t>
<t tx="ekr.20050818081715">def dumpContext (self):
    
    print ; print '-' * 40
    print 'Dump of context'
        
    i = 0
    for bunch in self.context:
        print '%2d %s' % (i,bunch)
        i += 1</t>
<t tx="ekr.20050818083045">def inContext (self,kind):
    
    '''Return the most recent bunch having the indicated kind, or None.'''
    
    i = len(self.context) - 1

    while i &gt;= 0:
        bunch = self.context[i]
        if bunch.kind == kind:
            return bunch
        i -= 1
        
    return None</t>
<t tx="ekr.20050818084920">def putHead (self,start,style='Normal',bulletText=None):
    
    self.createParagraph(self.body[:start],
        style=style,bulletText=bulletText)

    self.body = self.body[start:]


def putTail (self,start,style='Normal',bulletText=None):
    
    self.createParagraph(self.body[start:],
        style=style,bulletText=bulletText)

    self.body = self.body[:start]
</t>
<t tx="ekr.20050818090152"></t>
<t tx="ekr.20050818090152.1"></t>
<t tx="ekr.20050818090907"></t>
<t tx="ekr.20050818094118.1">def visit_docinfo(self, node):
    
    self.push(kind='docinfo',start=len(self.body))
    self.in_docinfo = True

def depart_docinfo(self, node):
    
    b = self.pop('docinfo')
    self.putHead(b.start)
    self.in_docinfo = False</t>
<t tx="ekr.20050818094118.2"></t>
<t tx="ekr.20050818094954"></t>
<t tx="ekr.20050818094954.1"></t>
<t tx="ekr.20050818095347">@

All grunt work completed:

- Moved Bunch class into this file (so no dependencies on leoGlobals.py).

- Simplified calls to self.push

- Finish all simple methods.

- Better dumps in createParagraph.</t>
<t tx="ekr.20050818103031">@nocolor

@others

@

- Bullets show up as a black 2 ball.

- More flexible handling of style sheets.

- Auto-footnote numbering does not work.

- Test rST raw: pdf feature.</t>
<t tx="ekr.20050818103441">@ From The Python Cookbook:  Often we want to just collect a bunch of stuff together, naming each item of the bunch; a dictionary's OK for that, but a small do-nothing class is even handier, and prettier to use.

Create a Bunch whenever you want to group a few variables:

    point = Bunch(datum=y, squared=y*y, coord=x)

You can read/write the named attributes you just created, add others, del some of them, etc:
    if point.squared &gt; threshold:
        point.isok = True
@c

class Bunch (object):
    
    """A class that represents a colection of things.
    
    Especially useful for representing a collection of related variables."""
    
    def __init__(self,**keywords):
        self.__dict__.update (keywords)
        
    def __repr__(self):
        return self.toString()

    def ivars(self):
        return self.__dict__.keys()
        
    def keys(self):
        return self.__dict__.keys()
        
    def toString(self):
        tag = self.__dict__.get('tag')
        entries = ["%s: %s" % (key,str(self.__dict__.get(key)))
            for key in self.ivars() if key != 'tag']
        if tag:
            return "Bunch(tag=%s)...\n%s\n" % (tag,'\n'.join(entries))
        else:
            return "Bunch...\n%s\n" % '\n'.join(entries)

    # Used by new undo code.
    def __setitem__ (self,key,value):
        '''Support aBunch[key] = val'''
        return operator.setitem(self.__dict__,key,value)
        
    def __getitem__ (self,key):
        '''Support aBunch[key]'''
        return operator.getitem(self.__dict__,key)
        
    def get (self,key,theDefault=None):
        return self.__dict__.get(key,theDefault)
        
bunch = Bunch</t>
<t tx="ekr.20050818105023"></t>
<t tx="ekr.20050818105023.1"></t>
<t tx="ekr.20050818130249"></t>
<t tx="ekr.20050819055746">c.save()</t>
<t tx="ekr.20050819055746.1">@

- Added dummyPDFTranslator class.

- Added support for this dummy class to Writer.translate.</t>
<t tx="ekr.20050819072001">def dumpNode (self,node,tag=''):
    
    &lt;&lt; define keys to be printed &gt;&gt;
    
    d = node.__dict__
    
    nkeys = d.keys() ; nkeys.sort()
    
    print ; print '-' * 30
    print 'dump of node %s\n' % (g.choose(tag,'(%s)' % tag,''))
    
    print 'class',node.__class__
    
    for nkey in nkeys:
        if nkey in keys:
            val = d.get(nkey)
            print nkey,':',g.toString(val,verbose=False,indent='\t')
            
    print ; print 'done', '-' * 25</t>
<t tx="ekr.20050819072001.1">keys = (
    #'anonymous_refs'
    #'anonymous_targets'
    'attributes'
    'autofootnote_refs'
    'autofootnote_start'
    'autofootnotes'
    #'children'
    #'citation_refs'
    #'citations'
    #'current_line'
    #'current_source'
    #'decoration'
    #'document'
    'footnote_refs'
    'footnotes'
    'id_start'
    'ids'  # keys are sectinon names, values are section objects or reference objects.
    'indirect_targets'
    'nameids' # This might be what we want: keys are section names, values are munged names.
    #'nametypes'
    #'parse_messages'
    #'rawsource'
    'refids'
    'refnames'
    #'reporter'
    #'settings'
    #'substitution_defs'
    #'substitution_names'
    #'substitution_refs'
    #'symbol_footnote_refs'
    #'symbol_footnote_start'
    #'symbol_footnotes'
    #'tagname'
    #'transform_messages'
    #'transformer',
)</t>
<t tx="ekr.20050820092312">def createParagraphsFromIntermediateFile (self,s,story,visitor):
    
    if 0: # Not needed now that putParaFromIntermediateFile is in the visitor.
        self.styleSheet = visitor.styleSheet
        self.encode = visitor.encode
    
    out = StringIO.StringIO()

    doc = reportlab.platypus.SimpleDocTemplate(out,
        pagesize=reportlab.lib.pagesizes.A4)

    # The 'real' code is doc.build(story)
    self.buildFromIntermediateFile(s,story,visitor)

    return out.getvalue()</t>
<t tx="ekr.20050820092312.1">def putParaFromIntermediateFile (self,lines,style):

    bulletText = None
    text = '\n'.join(lines)
    
    # g.trace(style,repr(text))
    
    style = self.styleSheet [style]

    self.story.append(
        reportlab.platypus.para.Paragraph (
            self.encode(text), style,
            bulletText = bulletText,
            context = self.styleSheet))</t>
<t tx="ekr.20050820094818">def buildFromIntermediateFile (self):
    
    'Synthesize calls to reportlab.platypus.para.Paragraph from an intermediate file.'
    
    lines = g.splitLines(self.contents)
    para = [] # The lines of the next paragraph.

    for line in lines:
        if line:
            if line.startswith('createParagraph:'):
                if para:
                    self.putParaFromIntermediateFile(para,style)
                    para = []
                style = line[len('createParagraph:'):].strip()
            elif line.startswith('starttag:') or line.startswith('..'):
                pass
            else:
                para.append(line)
    if para:
        self.putParaFromIntermediateFile(para,style)</t>
<t tx="ekr.20050820100547">class dummyPDFTranslator (docutils.nodes.NodeVisitor):

	@others</t>
<t tx="ekr.20050820101355">def __init__(self, writer,doctree,contents):

    self.writer = writer
    self.contents = contents
    self.story = []
    
    # Some of these may be needed, even though they are not referenced directly.
    self.settings = settings = doctree.settings
    self.styleSheet = stylesheet.getStyleSheet()
    docutils.nodes.NodeVisitor.__init__(self, doctree) # Init the base class.
    self.language = docutils.languages.get_language(doctree.settings.language_code)</t>
<t tx="ekr.20050820101355.1">def visit_document(self, node):

    self.buildFromIntermediateFile()
    
    raise docutils.nodes.SkipNode
    
def depart_document(self, node):
    
    pass</t>
<t tx="ekr.20050820101522">def encode(self, text):

    """Encode special characters in `text` &amp; return."""
    
    if type(text) is types.UnicodeType:
        text = text.replace(u'\u2020', u' ')
        text = text.replace(u'\xa0', u' ')
        text = text.encode('utf-8')

    return text

</t>
<t tx="ekr.20050820103029">def as_what(self):

    return self.story
</t>
<t tx="ekr.20050820112549">@

- First working version.

</t>
<t tx="ekr.20050821153838">def pdfMunge (self,s):
    
    '''Duplicate the munging done (somewhere in docutils) of section names.
    
    This allows us to use the nameids attribute in the document element.'''
    
    s = s.lower.replace('\t',' ')

    while s != s.replace('  ',' '):
        s = s.replace('  ',' ')
    
    return s.replace(' ','-')</t>
<t tx="ekr.20050822065754">@

- Completed the conversion to using Bunches on the context stack.
    - Added peek method.
    - In context now searches from top of context stack and returns a Bunch.
    - Rewrote the footnote logic to use bunches:
        - footnote_backrefs sets b.setLink and b.links.  Much clearer code.
        - visit/depart_label uses b.setLink and b.links to generate code.
- The code now passes a minimal test of footnote code.

- WARNING: auto-footnote numbering does not work.  I doubt it ever did.  I feel under no obligation to make it work.</t>
<t tx="ekr.20050822123348">@
I. Bugs and bug fixes

This file, leo_pdf.py, is derived from rlpdf.py. It is intended as a replacement
for it. The copyright below applies only to this file, and to no other part of
Leo.

This code fixes numerous bugs that must have existed in rlpdf.py. That code was
apparently out-of-date. For known bugs in the present code see the 'to do'
section.

II. New and improved code.

This code pushes only Bunch's on the context stack. The Bunch class is slightly
adapted from the Python Cookbook.

Pushing only Bunches greatly simplifies the code and makes it more robust: there
is no longer any need for one part of the code to pop as many entries as another
part pushed. Furthermore, Bunch's can have as much internal structure as needed
without affecting any other part of the code.

The following methods make using Bunch's trivial: push, pop, peek, inContext.
inContext searches the context stack for a Bunch of the indicated 'kind'
attribute, returning the Bunch if found.

The following 'code generator' methods were heavily rewritten:
visit/depart_title, visit/depart_visit_footnote_reference, footnote_backrefs
and visit/depart_label.

III. Passing intermediateFile.txt to reportlab.

You can use an 'intermediate' file as the input to reportlab. This can be highly
useful: you can see what output reportlab will accept before the code generators
can actually generate it.

The way this works is as follows:
1. Run this code as usual, with the trace in PDFTranslator.createParagraph
enabled. This trace will print the contents of each paragraph to be sent to
reportlab, along with the paragraph's style.

2. Take the resulting console output and put it in the file called
intermediateFile.txt, in the same folder as the original document.

3. At the start of Writer.translate, change the 'if 1:' to 'if: 0'. This causes
the code to use the dummyPDFTranslator class instead of the usual PDFTranslator
class.

4. *Rerun* this code. Because of step 3, the code will read
intermediateFile.txt and send it, paragraph by paragraph, to reportlab. The
actual work is done in buildFromIntermediateFile. This method assumes the output
was produced by the trace in PDFTranslator.createParagraph as discussed
in point 2 above.

IV. About tracing and debugging.

As mentioned in the imports section, it is not necessary to import leoGlobals.
This file is part of Leo, and contains debugging stuff such as g.trace and
g.toString. There are also g.splitLines, g.es_exception, etc. used by debugging
code.

The trace in PDFTranslator.createParagraph is extremely useful for figuring out
what happened. Various other calls to g.trace are commented out throughout the
code. These were the way I debugged this code.

Edward K. Ream:  Aug 22, 2005.</t>
<t tx="ekr.20050822125824">@

- Added 'about this code' section.</t>
<t tx="ekr.20050822172321"></t>
<t tx="ekr.20050822172321.1">@ Minor improvements to documentation.</t>
<t tx="ekr.20050825101321">def init ():
    
    '''This file may be distributed in Leo's plugin folder, but this file is NOT
    a Leo plugin!
    
    The init method returns None to tell Leo's plugin manager and unit tests to
    skip this file.'''
    
    return None</t>
<t tx="ekr.20050825101903">@

- Added warning to docstring that this is not a valid Leo plugin.

- Added init function that always returns False.  This helps Leo's unit tests.</t>
<t tx="ekr.20050830091910"></t>
<t tx="ekr.20051025144116">c.spellCommands.openSpellTab()</t>
<t tx="ekr.20051109021852">@ Not ready for prime time yet.</t>
<t tx="ekr.20060109114710">c.openLeoSettings()</t>
<t tx="ekr.20060110125615"></t>
<t tx="ekr.20060306151759"></t>
</tnodes>
</leo_file>
