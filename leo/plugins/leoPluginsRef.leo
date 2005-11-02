<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet ekr_stylesheet?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="6178" clone_windows="0"/>
<globals body_outline_ratio="0.434543454345">
	<global_window_position top="18" left="236" height="909" width="841"/>
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
<v t="ekr.20050724100334"><vh>@button Beautify</vh></v>
<v t="ekr.20051025144116"><vh>@button Spell</vh></v>
<v t="ekr.20050819055746"><vh>@button Save</vh></v>
<v t="ekr.20050722075812"><vh>Remove blank trailing lines</vh></v>
</v>
<v t="edream.110203113231.618" a="ETV"><vh>Plugins</vh>
<v t="EKR.20040517090508"><vh>  Enable plugins by changing pluginsManager.txt or using plugin_manager plugin</vh>
<v t="edream.120603093808"><vh>@thin pluginsManager.txt</vh></v>
</v>
<v t="ekr.20050303051035"><vh> Templates: these show recommended ways of defining plugins.</vh>
<v t="ekr.20041114102139"><vh>Notes</vh>
<v t="ekr.20041114103913"><vh>About comments in the style guide</vh></v>
<v t="ekr.20041114102139.1"><vh>About the root node</vh></v>
<v t="ekr.20041114103913.1"><vh>About defining functions in separate nodes</vh></v>
<v t="ekr.20041114102139.2"><vh>About the &lt;&lt; imports &gt;&gt; section</vh></v>
<v t="ekr.20041114103913.2"><vh>About accessing commanders</vh></v>
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
<v t="ekr.20050328092641"><vh>Library</vh>
<v t="ekr.20050328092641.1"><vh>db</vh></v>
<v t="ekr.20050328092641.2" tnodeList="ekr.20050328092641.2"><vh>@nosent Library.ini</vh></v>
<v t="ekr.20050328092641.3"><vh>@string Library_lib1 = default/libraryS.dbm</vh></v>
<v t="ekr.20050328092641.4"><vh>@thin Library.py</vh></v>
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
<v t="edream.110203113231.735"><vh>@thin trace_gc.py</vh></v>
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
<v t="ekr.20050421093045"><vh> dyna plugin 139i</vh>
<v t="ekr.20050421093045.1"><vh>&lt;&lt; insertAplug &gt;&gt;</vh></v>
<v t="ekr.20050421093045.2"><vh>@thin dyna_menu.py</vh></v>
<v t="ekr.20050421093045.103"><vh>@thin dynacommon.py</vh></v>
<v t="ekr.20050421093045.133" tnodeList="ekr.20050421093045.133"><vh>@nosent dyna_menu.ini</vh></v>
<v t="ekr.20050421093045.134"><vh>@thin dyna.txt</vh></v>
</v>
</v>
<v t="edream.110203113231.872"><vh>Enhanced nodes...</vh>
<v t="edream.110203113231.873"><vh>@thin at_folder.py</vh></v>
<v t="ekr.20040915085351"><vh>@thin at_produce.py</vh></v>
<v t="ktenney.20041211072654.1"><vh>@thin at_view.py</vh></v>
<v t="mork.20041020082242.1"><vh>@thin base64Packager.py</vh></v>
<v t="mork.20041018091414.1"><vh>@thin fastGotoNode.py</vh></v>
<v t="ekr.20050301095332"><vh>@thin mod_labels.py</vh></v>
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
<v t="EKR.20040517080517.1"><vh>@thin arrows.py</vh></v>
<v t="edream.110203113231.753"><vh>@thin image.py</vh></v>
<v t="ekr.20040422072343"><vh>@thin rClick.py</vh></v>
<v t="EKR.20040605181725"><vh>Autocompleter</vh>
<v t="EKR.20040605181725.1"><vh>Configuration</vh>
<v t="EKR.20040608070256"><vh>autocompleter.ini</vh></v>
<v t="EKR.20040608070256.1"><vh>.ato files in the autocompleter folder</vh></v>
</v>
<v t="ekr.20041017043622"
marks="ekr.20041017043622.23,"><vh>@thin autocompleter.py</vh></v>
</v>
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
<v t="ekr.20050523073009"><vh> chapters</vh>
<v t="ekr.20050427102121"><vh>Calls to zipfile module in chapters.py</vh>
<v t="mork.20040926105355.29"><vh>newOpen</vh></v>
<v t="mork.20040926105355.9"><vh>openChaptersFile</vh></v>
<v t="mork.20040929090525.1"><vh>zipChapters</vh></v>
</v>
<v t="mork.20040926105355.1"><vh>@thin chapters.py</vh></v>
</v>
<v t="mork.20041018162155.1"><vh>@thin EditAttributes.py</vh></v>
<v t="ekr.20040915073259.1"><vh>@thin maximizeNewWindows.py</vh></v>
<v t="mork.20041022155742.1"><vh>@thin nodebar.py</vh></v>
<v t="edream.110203113231.924"><vh>@thin redirect_to_log.py</vh></v>
<v t="ekr.20040915075530" a="M"><vh>@thin UASearch.py</vh></v>
<v t="ekr.20040831122004"><vh>@thin UniversalScrolling.py</vh></v>
<v t="ekr.20040831115238" a="M"><vh>@thin URLloader.py</vh></v>
</v>
<v t="ekr.20040722141148"><vh>Example code</vh>
<v t="edream.110203113231.916"><vh>@thin __overrideClasses.py</vh></v>
<v t="edream.110203113231.919"><vh>@thin override_commands.py</vh></v>
<v t="edream.110203113231.921"><vh>@thin redefine_put.py</vh></v>
</v>
<v t="ekr.20040722134535"><vh>Experimental/unfinished</vh>
<v t="ekr.20050915064008"
marks="ekr.20050915090544.4,ekr.20050915084416.10,ekr.20050915084416.14,"><vh>@thin __vnx__.py</vh></v>
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
<v t="ekr.20041107165824"><vh>temacs &amp; usetemacs</vh>
<v t="mork.20041013092542.1"><vh>usetemacs.py</vh>
<v t="ekr.20050513171201"><vh>&lt;&lt; docstring &gt;&gt;</vh></v>
<v t="ekr.20041106100326"><vh>&lt;&lt; imports &gt;&gt;</vh></v>
<v t="mork.20041013092542.2"><vh>&lt;&lt; globals &gt;&gt;</vh></v>
<v t="mork.20041101132349"><vh>&lt;&lt;version history&gt;&gt;</vh></v>
<v t="ekr.20041106100326.1"><vh>&lt;&lt; documentation &gt;&gt;</vh>
<v t="mork.20041104100514"><vh>future directions</vh></v>
<v t="mork.20041101204659"><vh>adding Emacs extensions via usetemacs</vh></v>
<v t="mork.20041104100856"><vh>where to put your temacs-Emacs Python extensions</vh></v>
<v t="mork.20041102102111"><vh>change Emacs keystrokes via configuration</vh></v>
<v t="mork.20041102094131"><vh>usetemacs design</vh></v>
<v t="mork.20041102094341"><vh>a note on loading temacs</vh></v>
</v>
<v t="ekr.20050311155753"><vh>init</vh>
<v t="ekr.20041106100326.2"><vh>&lt;&lt; override createBindings and onBodyKey &gt;&gt;</vh></v>
</v>
<v t="mork.20041013092542.3"><vh>utTailEnd</vh></v>
<v t="mork.20041013092542.6"><vh>seeHelp</vh></v>
<v t="mork.20041013092542.5"><vh>addMenu</vh></v>
<v t="mork.20041101124927"><vh>modifyOnBodyKey</vh></v>
<v t="mork.20041101205414"><vh>watchDelete</vh></v>
<v t="mork.20041102094928"><vh>changeKeyStrokes</vh></v>
<v t="mork.20041101210722"><vh>addTemacsAbbreviations</vh></v>
<v t="mork.20041101191351"><vh>loadConfig</vh></v>
<v t="mork.20041101202945"><vh>addTemacsExtensions</vh></v>
<v t="mork.20041103160433"><vh>setBufferGetters and Setters</vh></v>
<v t="mork.20041213112640"><vh>gotoPosition</vh></v>
<v t="mork.20041104145603"><vh>initialise</vh></v>
<v t="mork.20041204141826"><vh>addLeoCommands</vh></v>
<v t="mork.20041102091309"><vh>&lt;&lt;exampleTemacsExtension.py&gt;&gt;</vh></v>
<v t="mork.20041102092057"><vh>&lt;&lt;usetemacs.ini example&gt;&gt;</vh></v>
</v>
<v t="mork.20041030164547"><vh>temacs.py</vh>
<v t="mork.20041101100635"><vh>&lt;&lt;version history&gt;&gt;</vh></v>
<v t="ekr.20041106101311"><vh>&lt;&lt; documentation &gt;&gt;</vh>
<v t="mork.20041101203748"><vh>How to write an Emacs extension</vh></v>
<v t="mork.20041102081834"><vh>Coding convenions</vh></v>
<v t="mork.20041102082911"><vh>Known bugs</vh></v>
<v t="mork.20041102103822"><vh>Future directions</vh></v>
<v t="mork.20041104095745"><vh>A Note on Alt-X</vh></v>
<v t="mork.20041122151944"><vh>A Note on the volume of methods</vh></v>
<v t="mork.20041126091717"><vh>plans for .7</vh></v>
<v t="mork.20041123150836"><vh>the master command is the center of an Emacs instance</vh></v>
<v t="mork.20041122152311"><vh>adding stateful commands to temacs</vh></v>
<v t="mork.20041123150144"><vh>how to mix python regular expressions and the Text widget</vh></v>
</v>
<v t="mork.20041030164547.1"><vh>&lt;&lt; imports &gt;&gt;</vh></v>
<v t="mork.20041104102456"><vh>Emacs helper classes</vh>
<v t="mork.20041031131847"><vh>class ControlXHandler</vh>
<v t="mork.20041031162953"><vh>__init__</vh></v>
<v t="mork.20041031132342"><vh>__call__</vh></v>
<v t="mork.20041031133146"><vh>processKey</vh></v>
<v t="mork.20041031134709"><vh>processRectangle</vh></v>
<v t="mork.20041031135748"><vh>processAbbreviation</vh></v>
</v>
<v t="mork.20041031145157"><vh>class MC_StateManager</vh>
<v t="mork.20041031162857"><vh>__init__</vh>
<v t="mork.20041031150125"><vh>&lt;&lt;statecommands&gt;&gt;</vh></v>
</v>
<v t="mork.20041031162857.1"><vh>setState</vh></v>
<v t="mork.20041031162857.2"><vh>getState</vh></v>
<v t="mork.20041031162857.3"><vh>hasState</vh></v>
<v t="mork.20041124094511"><vh>whichState</vh></v>
<v t="mork.20041031162857.4"><vh>__call__</vh></v>
<v t="mork.20041031162857.5"><vh>clear</vh></v>
</v>
<v t="mork.20041101083527"><vh>class MC_KeyStrokeManager  (hard-coded keystrokes)</vh>
<v t="mork.20041101083527.1"><vh>__init__</vh>
<v t="mork.20041101083527.2"><vh>&lt;&lt;keystrokes&gt;&gt; (hard-coded keystrokes)</vh></v>
</v>
<v t="mork.20041101084148"><vh>hasKeyStroke</vh></v>
<v t="mork.20041101084148.1"><vh>__call__</vh></v>
</v>
<v t="mork.20041102131352"><vh>class Tracker</vh>
<v t="mork.20041102131352.1"><vh>init</vh></v>
<v t="mork.20041102131352.2"><vh>setTabList</vh></v>
<v t="mork.20041102131352.3"><vh>_next</vh></v>
<v t="mork.20041102132710"><vh>next</vh></v>
<v t="mork.20041102160313"><vh>clear</vh></v>
</v>
</v>
<v t="mork.20041030165020"><vh>class Emacs</vh>
<v t="mork.20041030165020.1"><vh>Emacs.__init__</vh></v>
<v t="mork.20041030164547.41"><vh>getHelpText</vh></v>
<v t="mork.20041030164547.43"><vh>masterCommand</vh>
<v t="ekr.20050527112828"><vh>&lt;&lt; old insert code &gt;&gt;</vh></v>
<v t="ekr.20050527084754"><vh>&lt;&lt; old code &gt;&gt;</vh></v>
<v t="ekr.20050527084754.1"><vh>&lt;&lt; old code 2 &gt;&gt;</vh></v>
</v>
<v t="mork.20041102082023"><vh>keyboardQuit</vh></v>
<v t="mork.20041031182258"><vh>add command dictionary methods</vh>
<v t="mork.20041030183331"><vh>addCallBackDict (creates cbDict)</vh></v>
<v t="mork.20041030183633"><vh>addXCommands</vh></v>
<v t="mork.20041030190903"><vh>addAltXCommands</vh></v>
<v t="mork.20041030190729"><vh>addRegisterItems</vh></v>
</v>
<v t="mork.20041031183614"><vh>general utility methods</vh>
<v t="mork.20041031195549"><vh>buffer altering methods</vh>
<v t="mork.20041030164547.31"><vh>moveTo</vh></v>
<v t="mork.20041030164547.33"><vh>moveword</vh></v>
<v t="mork.20041030164547.39"><vh>capitalize</vh></v>
<v t="mork.20041030164547.40"><vh>swapWords</vh></v>
<v t="mork.20041030164547.103"><vh>insertParentheses</vh></v>
<v t="mork.20041123095436"><vh>replace-string and replace-regex</vh>
<v t="mork.20041030164547.115"><vh>replaceString</vh></v>
<v t="mork.20041123095123"><vh>activateReplaceRegex</vh></v>
</v>
<v t="mork.20041030164547.116"><vh>swapCharacters</vh></v>
<v t="mork.20041123095507"><vh>insert new line methods</vh>
<v t="mork.20041030164547.117"><vh>insertNewLine</vh></v>
<v t="mork.20041030164547.131"><vh>insertNewLineIndent</vh></v>
<v t="mork.20041103135515"><vh>insertNewLineAndTab</vh></v>
</v>
<v t="mork.20041030164547.148"><vh>transposeLines</vh></v>
<v t="mork.20041030164547.130"><vh>changePreviousWord</vh></v>
<v t="mork.20041030164547.150"><vh>removeBlankLines</vh></v>
<v t="mork.20041030164547.101"><vh>screenscroll</vh></v>
<v t="mork.20041030164547.22"><vh>exchangePointMark</vh></v>
<v t="mork.20041030164547.96"><vh>backToIndentation</vh></v>
<v t="mork.20041124130434"><vh>indent-relative</vh></v>
<v t="mork.20041030164547.129"><vh>negativeArgument</vh></v>
<v t="mork.20041030164547.114"><vh>movePastClose</vh></v>
<v t="mork.20041030164547.119"><vh>prevNexSentence</vh></v>
<v t="mork.20041031202438"><vh>selectAll</vh></v>
<v t="mork.20041120195951"><vh>suspend</vh></v>
</v>
<v t="mork.20041031195908"><vh>informational methods</vh>
<v t="mork.20041030164547.118"><vh>lineNumber</vh></v>
<v t="mork.20041102161859"><vh>viewLossage</vh></v>
<v t="mork.20041121195816"><vh>whatLine</vh></v>
</v>
<v t="mork.20041031195908.1"><vh>pure utility methods</vh>
<v t="mork.20041102151939"><vh>setEvent</vh></v>
<v t="mork.20041030164547.127"><vh>getWSString</vh></v>
<v t="mork.20041030164547.135"><vh>findPre</vh></v>
<v t="mork.20041030164547.100"><vh>measure</vh></v>
<v t="mork.20041030164547.95"><vh>manufactureKeyPress</vh></v>
<v t="mork.20041030164547.83"><vh>changecbDict</vh></v>
<v t="mork.20041030164547.92"><vh>removeRKeys</vh></v>
<v t="mork.20041030164547.142"><vh>_findMatch2</vh></v>
<v t="mork.20041102133805"><vh>_findMatch</vh></v>
</v>
</v>
<v t="mork.20041120223251"><vh>shutdown methods</vh>
<v t="mork.20041120222336"><vh>shutdown</vh></v>
<v t="mork.20041120223251.1"><vh>setShutdownHook</vh></v>
</v>
<v t="mork.20041031182215"><vh>Label( minibuffer ) and svar methods</vh>
<v t="mork.20041102183901"><vh>label( minibuffer ) methods</vh>
<v t="mork.20041030164547.2"><vh>setLabelGrey</vh></v>
<v t="mork.20041030164547.3"><vh>setLabelBlue</vh></v>
<v t="mork.20041030164547.86"><vh>resetMiniBuffer</vh></v>
</v>
<v t="mork.20041031182943"><vh>svar methods</vh>
<v t="mork.20041030164547.112"><vh>getSvarLabel</vh></v>
<v t="mork.20041030164547.113"><vh>setSvar</vh></v>
</v>
</v>
<v t="mork.20041031194746"><vh>configurable methods</vh>
<v t="mork.20041031182643"><vh>tailEnd methods</vh>
<v t="mork.20041030164547.4"><vh>_tailEnd</vh></v>
<v t="mork.20041030164547.5"><vh>setTailEnd</vh></v>
</v>
<v t="mork.20041031182643.1"><vh>undoer methods</vh>
<v t="mork.20041030164547.6"><vh>setUndoer</vh></v>
<v t="mork.20041030164547.7"><vh>doUndo</vh></v>
</v>
<v t="mork.20041030164547.30"><vh>setBufferStrokes</vh></v>
<v t="mork.20041101190309"><vh>extendAltX</vh></v>
<v t="mork.20041102094716"><vh>reconfigureKeyStroke</vh></v>
<v t="mork.20041103155347"><vh>buffer recognition and alterers</vh>
<v t="mork.20041104094826"><vh>configure buffer methods</vh>
<v t="mork.20041103155347.1"><vh>setBufferGetter</vh></v>
<v t="mork.20041103155347.2"><vh>setBufferSetter</vh></v>
<v t="mork.20041103155347.3"><vh>getBufferDict</vh></v>
<v t="mork.20041103162147"><vh>setBufferData</vh></v>
<v t="mork.20041103191311"><vh>setBufferGoto</vh></v>
<v t="mork.20041104090224"><vh>setBufferDelete</vh></v>
<v t="mork.20041104092349"><vh>setBufferRename</vh></v>
</v>
<v t="mork.20041104094826.1"><vh>buffer operations</vh>
<v t="mork.20041103155347.4"><vh>appendToBuffer</vh></v>
<v t="mork.20041103155347.5"><vh>prependToBuffer</vh></v>
<v t="mork.20041103155347.6"><vh>insertToBuffer</vh></v>
<v t="mork.20041103190332"><vh>listBuffers</vh></v>
<v t="mork.20041103155347.7"><vh>copyToBuffer</vh></v>
<v t="mork.20041103191311.1"><vh>switchToBuffer</vh></v>
<v t="mork.20041104090224.1"><vh>killBuffer</vh></v>
<v t="mork.20041104092058"><vh>renameBuffer</vh></v>
<v t="mork.20041103161202"><vh>chooseBuffer</vh></v>
<v t="mork.20041103161202.1"><vh>setInBufferMode</vh></v>
</v>
</v>
</v>
<v t="mork.20041031155753"><vh>macro methods</vh>
<v t="mork.20041030164547.8"><vh>startKBDMacro</vh></v>
<v t="mork.20041030164547.9"><vh>recordKBDMacro</vh></v>
<v t="mork.20041030164547.10"><vh>stopKBDMacro</vh></v>
<v t="mork.20041030164547.11"><vh>_executeMacro</vh></v>
<v t="mork.20041030164547.12"><vh>executeLastMacro</vh></v>
<v t="mork.20041030164547.13"><vh>nameLastMacro</vh></v>
<v t="mork.20041030164547.14"><vh>_addToDoAltX</vh></v>
<v t="mork.20041030164547.15"><vh>loadMacros</vh></v>
<v t="mork.20041030164547.16"><vh>_loadMacros</vh></v>
<v t="mork.20041030164547.17"><vh>getMacroName</vh></v>
<v t="mork.20041030164547.18"><vh>saveMacros</vh></v>
<v t="mork.20041030164547.19"><vh>_saveMacros</vh></v>
</v>
<v t="mork.20041031194703"><vh>comment column methods</vh>
<v t="mork.20041030164547.20"><vh>setCommentColumn</vh></v>
<v t="mork.20041030164547.21"><vh>indentToCommentColumn</vh></v>
</v>
<v t="mork.20041031182709"><vh>how many methods</vh>
<v t="mork.20041030164547.23"><vh>howMany</vh></v>
<v t="mork.20041030164547.24"><vh>startHowMany</vh></v>
</v>
<v t="mork.20041031155913"><vh>paragraph methods</vh>
<v t="mork.20041030164547.25"><vh>selectParagraph</vh></v>
<v t="mork.20041030164547.26"><vh>_selectParagraph</vh></v>
<v t="mork.20041030164547.27"><vh>killParagraph</vh></v>
<v t="mork.20041030164547.28"><vh>backwardKillParagraph</vh></v>
</v>
<v t="mork.20041031181929"><vh>kill methods</vh>
<v t="mork.20041030164547.34"><vh>kill</vh></v>
<v t="mork.20041030164547.36"><vh>walkKB</vh></v>
<v t="mork.20041030164547.35"><vh>deletelastWord</vh></v>
<v t="mork.20041030164547.37"><vh>killsentence</vh></v>
<v t="mork.20041030164547.91"><vh>killRegion</vh></v>
<v t="mork.20041030164547.42"><vh>addToKillBuffer</vh></v>
<v t="mork.20041030164547.29"><vh>iterateKillBuffer</vh></v>
<v t="mork.20041103120919"><vh>getClipboard</vh></v>
</v>
<v t="mork.20041031155642"><vh>register methods</vh>
<v t="mork.20041030164547.44"><vh>copyToRegister</vh></v>
<v t="mork.20041030164547.45"><vh>copyRectangleToRegister</vh></v>
<v t="mork.20041030164547.46"><vh>prependToRegister</vh></v>
<v t="mork.20041030164547.47"><vh>appendToRegister</vh></v>
<v t="mork.20041030164547.49"><vh>_ToReg</vh></v>
<v t="mork.20041030164547.48"><vh>_chckSel</vh></v>
<v t="mork.20041030164547.50"><vh>_checkIfRectangle</vh></v>
<v t="mork.20041030164547.51"><vh>insertFromRegister</vh></v>
<v t="mork.20041030164547.52"><vh>incrementRegister</vh></v>
<v t="mork.20041030164547.53"><vh>numberToRegister</vh></v>
<v t="mork.20041030164547.54"><vh>pointToRegister</vh></v>
<v t="mork.20041030164547.55"><vh>jumpToRegister</vh></v>
<v t="mork.20041030164547.56"><vh>invalidRegister</vh></v>
<v t="mork.20041030164547.57"><vh>setNextRegister</vh></v>
<v t="mork.20041030164547.58"><vh>executeRegister</vh></v>
<v t="mork.20041030164547.59"><vh>deactivateRegister</vh></v>
<v t="mork.20041102151545"><vh>viewRegister</vh></v>
</v>
<v t="mork.20041031181701"><vh>abbreviation methods</vh>
<v t="mork.20041030164547.60"><vh>abbreviationDispatch</vh></v>
<v t="mork.20041030164547.61"><vh>abbrevCommand1</vh></v>
<v t="mork.20041030164547.62"><vh>expandAbbrev</vh></v>
<v t="mork.20041030164547.63"><vh>regionalExpandAbbrev</vh>
<v t="ekr.20050527111832"><vh>&lt;&lt; define a new generator searchXR &gt;&gt;</vh></v>
</v>
<v t="mork.20041030164547.64"><vh>_setRAvars</vh></v>
<v t="mork.20041030164547.65"><vh>killAllAbbrevs</vh></v>
<v t="mork.20041030164547.66"><vh>toggleAbbrevMode</vh></v>
<v t="mork.20041030164547.67"><vh>listAbbrevs</vh></v>
<v t="mork.20041030164547.68"><vh>readAbbreviations</vh></v>
<v t="mork.20041030164547.69"><vh>_readAbbrevs</vh></v>
<v t="mork.20041030164547.70"><vh>writeAbbreviations</vh></v>
<v t="mork.20041030164547.71"><vh>_writeAbbrevs</vh></v>
</v>
<v t="mork.20041031182137"><vh>paragraph methods</vh>
<v t="mork.20041030164547.72"><vh>movingParagraphs</vh></v>
<v t="mork.20041030164547.74"><vh>fillParagraph</vh></v>
<v t="mork.20041030164547.76"><vh>fillRegionAsParagraph</vh></v>
</v>
<v t="mork.20041031182916"><vh>fill prefix methods</vh>
<v t="mork.20041030164547.73"><vh>setFillPrefix</vh></v>
<v t="mork.20041030164547.75"><vh>_addPrefix</vh></v>
</v>
<v t="mork.20041103085329"><vh>fill column and centering</vh>
<v t="mork.20041103085329.1"><vh>centerLine</vh></v>
<v t="mork.20041103095628"><vh>centerRegion</vh></v>
<v t="mork.20041103085329.2"><vh>setFillColumn</vh></v>
</v>
<v t="mork.20041031183136"><vh>region methods</vh>
<v t="mork.20041030164547.77"><vh>fillRegion</vh></v>
<v t="mork.20041030164547.87"><vh>setRegion</vh></v>
<v t="mork.20041030164547.93"><vh>indentRegion</vh></v>
<v t="mork.20041030164547.94"><vh>tabIndentRegion</vh></v>
<v t="mork.20041030164547.102"><vh>countRegion</vh></v>
<v t="mork.20041030164547.138"><vh>reverseRegion</vh></v>
<v t="mork.20041030164547.149"><vh>upperLowerRegion</vh></v>
</v>
<v t="mork.20041122190403"><vh>searching</vh>
<v t="mork.20041031182837"><vh>incremental search methods</vh>
<v t="mork.20041030164547.79"><vh>startIncremental</vh></v>
<v t="mork.20041030164547.38"><vh>search</vh></v>
<v t="mork.20041030164547.80"><vh>iSearch</vh></v>
<v t="mork.20041030164547.153"><vh>scolorizer</vh></v>
<v t="mork.20041121125455"><vh>useRegex</vh></v>
</v>
<v t="mork.20041122154604"><vh>non-incremental search methods</vh>
<v t="mork.20041122154604.1"><vh>nonincrSearch</vh></v>
<v t="mork.20041122155708"><vh>startNonIncrSearch</vh></v>
</v>
<v t="mork.20041122171601"><vh>word search methods</vh>
<v t="mork.20041122171601.1"><vh>startWordSearch</vh></v>
<v t="mork.20041122171601.2"><vh>wordSearch</vh></v>
</v>
<v t="mork.20041121103034"><vh>re-search methods</vh>
<v t="mork.20041121103034.1"><vh>reStart</vh></v>
<v t="mork.20041121103034.2"><vh>re_search</vh></v>
</v>
</v>
<v t="mork.20041121140620"><vh>diff methods</vh>
<v t="mork.20041121140620.1"><vh>diff</vh></v>
</v>
<v t="mork.20041031182332"><vh>Zap methods</vh>
<v t="mork.20041030164547.81"><vh>startZap</vh></v>
<v t="mork.20041030164547.82"><vh>zapTo</vh></v>
</v>
<v t="mork.20041031181740"><vh>ControlX methods</vh>
<v t="mork.20041030164547.84"><vh>startControlX</vh></v>
<v t="mork.20041030164547.85"><vh>stopControlX</vh></v>
<v t="mork.20041030164547.78"><vh>doControlX</vh></v>
</v>
<v t="mork.20041031183614.1"><vh>range methods</vh>
<v t="mork.20041030164547.88"><vh>inRange</vh></v>
<v t="mork.20041030164547.89"><vh>contRanges</vh></v>
<v t="mork.20041030164547.90"><vh>testinrange</vh></v>
</v>
<v t="mork.20041031182402"><vh>delete methods</vh>
<v t="mork.20041030164547.97"><vh>deleteIndentation</vh></v>
<v t="mork.20041030164547.98"><vh>deleteNextChar</vh></v>
<v t="mork.20041030164547.99"><vh>deleteSpaces</vh></v>
</v>
<v t="mork.20041031181701.1"><vh>query replace methods</vh>
<v t="mork.20041030164547.107"><vh>qreplace</vh></v>
<v t="mork.20041030164547.108"><vh>_qreplace</vh></v>
<v t="mork.20041030164547.109"><vh>getQuery</vh></v>
<v t="mork.20041030164547.110"><vh>getReplace</vh></v>
<v t="mork.20041030164547.111"><vh>masterQR</vh></v>
<v t="mork.20041123113640"><vh>startRegexReplace</vh></v>
<v t="mork.20041031194858"><vh>query search methods</vh>
<v t="mork.20041030164547.104"><vh>listenQR</vh></v>
<v t="mork.20041030164547.105"><vh>qsearch</vh></v>
<v t="mork.20041030164547.106"><vh>quitQSearch</vh></v>
</v>
</v>
<v t="mork.20041031155313"><vh>Rectangles methods</vh>
<v t="mork.20041031202908"><vh>activateRectangleMethods</vh></v>
<v t="mork.20041030164547.120"><vh>openRectangle</vh></v>
<v t="mork.20041030164547.121"><vh>clearRectangle</vh></v>
<v t="mork.20041030164547.122"><vh>deleteRectangle</vh></v>
<v t="mork.20041030164547.123"><vh>stringRectangle</vh></v>
<v t="mork.20041030164547.124"><vh>killRectangle</vh></v>
<v t="mork.20041030164547.125"><vh>closeRectangle</vh></v>
<v t="mork.20041030164547.126"><vh>yankRectangle</vh></v>
<v t="mork.20041030164547.128"><vh>getRectanglePoints</vh></v>
</v>
<v t="mork.20041031181701.2"><vh>dynamic abbreviations methods</vh>
<v t="mork.20041030164547.132"><vh>dynamicExpansion</vh></v>
<v t="mork.20041030164547.133"><vh>dynamicExpansion2</vh></v>
<v t="mork.20041030164547.134"><vh>getDynamicList</vh></v>
</v>
<v t="mork.20041031183018"><vh>sort methods</vh>
<v t="mork.20041030164547.136"><vh>sortLines</vh></v>
<v t="mork.20041030164547.137"><vh>sortColumns</vh></v>
<v t="mork.20041030164547.139"><vh>sortFields</vh></v>
</v>
<v t="mork.20041031181929.1"><vh>Alt_X methods</vh>
<v t="mork.20041030164547.140"><vh>alt_X</vh></v>
<v t="mork.20041030164547.141"><vh>doAlt_X</vh></v>
<v t="mork.20041123093234"><vh>execute last altx methods</vh>
<v t="mork.20041122223754"><vh>executeLastAltX</vh></v>
<v t="mork.20041122225107"><vh>repeatComplexCommand</vh></v>
</v>
</v>
<v t="mork.20041031155455"><vh>universal methods</vh>
<v t="mork.20041030164547.143"><vh>universalDispatch</vh></v>
<v t="mork.20041030164547.144"><vh>universalCommand1</vh></v>
<v t="mork.20041030164547.145"><vh>universalCommand2</vh></v>
<v t="mork.20041030164547.146"><vh>universalCommand3</vh></v>
<v t="mork.20041030164547.147"><vh>numberCommand</vh></v>
</v>
<v t="mork.20041121201041"><vh>line methods</vh>
<v t="mork.20041121201041.1"><vh>alterLines</vh></v>
<v t="mork.20041121210221"><vh>processLines</vh></v>
<v t="mork.20041121201112"><vh>startLines</vh></v>
</v>
<v t="mork.20041031160002"><vh>goto methods</vh>
<v t="mork.20041030164547.154"><vh>startGoto</vh></v>
<v t="mork.20041030164547.155"><vh>Goto</vh></v>
</v>
<v t="mork.20041122110739"><vh>directory methods</vh>
<v t="mork.20041122110739.1"><vh>makeDirectory</vh></v>
<v t="mork.20041122111431"><vh>removeDirectory</vh></v>
</v>
<v t="mork.20041031182449"><vh>file methods</vh>
<v t="mork.20041122112210"><vh>deleteFile</vh></v>
<v t="mork.20041030164547.151"><vh>insertFile</vh></v>
<v t="mork.20041030164547.152"><vh>saveFile</vh></v>
<v t="mork.20041121140620.2"><vh>getReadableFile</vh></v>
</v>
<v t="mork.20041123192555"><vh>Esc methods for Python evaluation</vh>
<v t="mork.20041123192555.1"><vh>watchEscape</vh></v>
<v t="mork.20041124095452"><vh>escEvaluate</vh></v>
<v t="mork.20041124102729"><vh>startEvaluate</vh></v>
</v>
<v t="mork.20041124123825"><vh>tabify/untabify</vh>
<v t="mork.20041124123825.1"><vh>tabify</vh></v>
</v>
<v t="mork.20041208120232"><vh>shell and subprocess</vh>
<v t="mork.20041208120232.1"><vh>def startSubprocess</vh></v>
<v t="mork.20041208120232.2"><vh>subprocess</vh></v>
<v t="mork.20041208121502"><vh>executeSubprocess</vh></v>
</v>
</v>
<v t="ekr.20041106100834"><vh>&lt;&lt; run standalone tests &gt;&gt;</vh></v>
</v>
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
<v t="ekr.20041009165858"><vh>@thin spellpyx.ini</vh></v>
<v t="ekr.20040809151600.1"><vh>@thin spellpyx.py</vh></v>
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
<v t="ekr.20050805162550"><vh>@thin rst3.py</vh></v>
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

import leoGlobals as g
import leoPlugins

import string

c = g.top() ; p = c.currentPosition()

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
<t tx="EKR.20040605181725"></t>
<t tx="EKR.20040605181725.1">@nocolor</t>
<t tx="EKR.20040608070256">The plugin looks in the plugins folder for a file called autocompleter.ini.

This follows the windows .ini file format as used in ConfigParser, see: http://docs.python.org/lib/module-ConfigParser.html

1. Specify options in autocompleter.ini as follows:

[ autocompleter ]

useauto = 0 # turns off autocompletion
usecalltips = 0 # turns of calltips
autopattern = pattern #pattern is a regular expression

The autopattern changes the pattern by which autocompletion options are recognized.
I wouldnt use it unless you understood how the code works though.

2. You can add a language by putting this in autocompleter.ini:

[ yourlanguage ]

pat = put regular expression here

Then the plugin will recognize your language for the calltip system. This only works if Leo currently recognizes your language, since we are getting our info from the colorizer as to what language is in use.</t>
<t tx="EKR.20040608070256.1">The plugin uses specific pattern matching based on the language you are using.

For example, if you are in a node and the language is python, it will only recognize def word(     ) as the calltip.

Support for Python, C, C++, Perl and Java is built-in, other languages may be supported as follows:

You can supply a library of prebuilt calltip definitions and autocompleter info by putting a directory called autocompleter in the plugins directory. It will look for a file(s) of the languages used in the Leo project. The file name must be language.ato.

For java it would be java.ato, which might contain:

dog.eat
burt.you
public static void main( String[] args )

and dog.eat, burt.you would be added to autocompletion and the 3rd line would be added to the calltips section.</t>
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
<t tx="edream.110203113231.930"></t>
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

    if v.edit_text():
        sel1,sel2 = g.app.gui.getTextSelection(v.edit_text())
        if sel1 and sel2 and sel1 != sel2: # 7/7/03
            v.edit_text().delete(sel1,sel2)
        v.edit_text().insert("insert",c.getTime(body=False))
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
    if self.revertHeadline and v.edit_text() and v == self.editVnode:
        
        # g.trace(`self.revertHeadline`)
        v.edit_text().delete("1.0","end")
        v.edit_text().insert("end",self.revertHeadline)
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

    if v and v.edit_text():
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
    c.frame.body.onBodyChanged(v,"Typing")</t>
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
    c.frame.body.onBodyChanged(v,"Typing",oldSel=oldSel)</t>
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

def WriteTreeOfCurrentNode():
    c = g.top() ; f = c.frame
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
def WriteAll():
    c = g.top() ; f = c.frame
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

def WriteAllRoots():
    "Writes @root directive and/or @ascfile directive to log pane."

    patternAscDirectiveFile = re.compile(r'^@ascfile')
    patternRoot = re.compile(r'^@root')

    g.es('Looking for @root or @ascfile.')
    c = g.top() ; f = c.frame
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

    def GetCurrentOptions(self, vnode):
        self.current.clear()
        self.current = self.default.copy()
        c = g.top()
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
def GetAscFilename(vnode):
    'Checks a node for a filename directive.'
    # f is the Leo outline
    c = g.top()
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
            
            g.top().frame.menu.createOpenWithMenuFromTable(table)

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

def OpenTreeInXEmacs ():
    import leoCommands
    #XEmacsCommand = "/usr/bin/gnuclient -q "
    XEmacsCommand = "/mrc2/linux-bin/gnuclient-noshow "
    c = g.top()
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

        c = g.top()
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
<t tx="ekr.20041030092101">@ Notes by EKR:  The enclosed is a remarkable body of work by 'e'.  Have fun with it.

I am enclosing this code as-is; use with reasonable caution.

You may download the latest version at: http://rclick.netfirms.com/dyna_menu.py.html</t>
<t tx="ekr.20041103052443"># Execute this in a script button.

import leoGlobals as g
import string

c = g.top()

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
<t tx="ekr.20041106100326">import leoGlobals as g
import leoNodes
import leoPlugins
import leoTkinterFrame

try:
    import Tkinter as Tk
    import ScrolledText
    import tkFont
except:
    Tk = None

import ConfigParser
import os
import sys
import weakref

try:
    pth = os.path.split( g.app.loadDir ) 
    ppath = pth[ 0 ] + os.sep + 'plugins'
    ext_path = pth[ 0 ] + os.sep + 'plugins' + os.sep + 'temacs_ext'
    try:
        if not os.path.exists( ext_path ):
            os.mkdir( ext_path )
    except Exception, x:
        g.es( "Attempt to create %s failed because of %s" %( ext_path, x ) )
    sys.path.append( ppath )
    sys.path.append( ext_path )
    temacs = __import__( 'temacs', globals(), locals())
except Exception, x:
    g.es( "temacs not loadable. Aborting load of usetemacs because of: " + str( x ))
    temacs = None
</t>
<t tx="ekr.20041106100326.1">@others
@nocolor</t>
<t tx="ekr.20041106100326.2">orig_Bindings = leoTkinterFrame.leoTkinterBody.createBindings
leoTkinterFrame.leoTkinterBody.createBindings = initialise() #createBindings

orig_OnBodyKey = leoTkinterFrame.leoTkinterBody.onBodyKey
leoTkinterFrame.leoTkinterBody.onBodyKey = modifyOnBodyKey</t>
<t tx="ekr.20041106100834">@
This part runs Temacs with a Text widget.
It should be accessible by typing python temacs.py at the command prompt
Note: There is no configuration as to buffers and such, so dont access that functionality.  Just a proof of concept.

@c

Tl = Tkinter.Tk()
Tl.title( 'temacs Emacs test' )
Tx = Tkinter.Text( background = 'white', foreground = 'blue' )
f2 = Tkinter.Frame()
f2.pack( side = 'bottom' )
def onQuit():
    import sys
    sys.exit( 0 )
    
minibuffer = Tkinter.Label( f2 )
minibuffer.pack( side = 'right', expand = 1, fill = 'both' )
quitb = Tkinter.Button( f2, text = 'Quit' , command = onQuit )
quitb.pack( side = 'left' )
Tx.pack( side = 'top' )
emacs = Emacs( Tx, minibuffer, True, True )
Tl.mainloop()</t>
<t tx="ekr.20041106101311">@nocolor

@others</t>
<t tx="ekr.20041107165824"></t>
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
<t tx="ekr.20041114103913.2">It is almost always a bad idea to use g.top() to get the commander of the presently selected frame.
Instead, use the onCreate function and class myClass as shown to create a class that binds self.c.</t>
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

v.edit_text():  ?? instead of pulling it of tree ?

yes.

4.2 it is p.edit_text()


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

Pmw = g.importExtension('Pmw',    pluginName=__name__,verbose=True)
Tk  = g.importExtension('Tkinter',pluginName=__name__,verbose=True)

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
<t tx="ekr.20050311155753">def init ():
    
    ok = temacs and Tk and not g.app.unitTesting
    
    if ok:
        if g.app.gui is None: 
            g.app.createTkGui(__file__)
    
        if g.app.gui.guiName() == "tkinter":
            global orig_Bindings,orig_OnBodyKey
            &lt;&lt; override createBindings and onBodyKey &gt;&gt;
            loadConfig()
            g.plugin_signon(__name__)
            leoPlugins.registerHandler( ('open2', "new") , addMenu )
            
    return ok</t>
<t tx="ekr.20050328092641">from Library.py for Leo4.3
see forum &lt;http://sourceforge.net/forum/forum.php?thread_id=1244564&amp;forum_id=10226&gt;
a better configparser would be nice.
ability to add comments and not have them rearranged
 and to display them in the properties dialog.

using @settings too, 

also potential problems while testing 
if you have this enabled from more than one python/Leo instance?
seems to handle it ok, but might get deadlocked on multiple inserts.

adding some room to catch exceptions
seems to be using dbhash on win py2.4 might be nice to know.
changes to ini thru properties doesn't take effect until you hit apply.
just ok isn't enough to do it?

working out details for multiple leos open, making the dialog follow.
if you click Library again after switching leos, all is well.
more to be done. spellchecker solves this by creating a global window
but it is hooked on each node selection and updated when the body is changed.
that seems a little heavy handed for this application.


adding support for multiple libraries
and or retaining open library handles.


PMW windows don't have the Leo icon, maybe that can be fixed?

thanks to origional author and EKR for working out the important details.
adding config and startup &amp; shutdown trivial by comparason
and of course Paul for plugins, menu and manager.
e

@language python
@tabwidth -4
@killcolor </t>
<t tx="ekr.20050328092641.1">['__cmp__', '__contains__', '__del__', '__delitem__', '__doc__', '__getitem__', '__init__', '__iter__', '__len__', '__module__', '__repr__', '__setitem__', '_checkCursor', '_checkOpen', '_closeCursors', '_cursor_refs', '_gen_cref_cleaner', '_make_iter_cursor', 'clear', 'close', 'db', 'dbc', 'first', 'get', 'has_key', 'isOpen', 'items', 'iteritems', 'iterkeys', 'itervalues', 'keys', 'last', 'next', 'pop', 'popitem', 'previous', 'saved_dbc_key', 'set_location', 'setdefault', 'sync', 'update', 'values']

</t>
<t tx="ekr.20050328092641.2">;default/ is leo/plugins  ~/ is your $HOME env var as seen by leo
; if there is an @setting Library_lib* somewhere it will override the ini
;there are no provisions yet to change the @setting but hitting Preferences apply
; from the plugin_menu will reread the ini and the @setting
; you could even change the setting by script then hit apply for now.
; delete or comment out the ones you won't be using.

; verbosity can be true, True, 1 on, False 0 , turns on extra internal feedback

[Main]
verbosity=0
;lib* = eventually, don't use lib=  it is to be the current lib
; only impliemented lib0..5 for now. lib0 is the opening lib

;lib0 = default/library.dbm
lib1 = default/library1.dbm
;lib2 = default/library22.dbm
;lib3 = default/library23.dbm
;lib4 = default/library24.dbm

;lib5 = ~/libraryMy.dbm
;libLa = C:\c\leo\libraryL.dbm
;libLb = C:/c/leo/libraryL.dbm</t>
<t tx="ekr.20050328092641.3">    """@string Library_lib1 = default/libraryS.dbm
    overrides the plugin and ini defaults
    default/ replaced with leo/plugins dir
    ~/ replaced with g.app.homeDir as Leo sees it.

    put this in an @settings node in a leo or in leoSettings.leo
    in config or your $HOME dir
    
    Note: for now, you still have to pullup the plugin_menu Properties
    and hit apply if you change this after the first leo is on screen.
    and you also before that have to enter settins and hit apply to reread settings.
    later version will have more tools from Leo to handle this better.
    the first library that will be opened is the default 
    unless one or more of lib0 thru lib5 is defined somehow.
    """
#can we just have the list here? like recentfiles and get a list of them back?
lib1</t>
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
<t tx="ekr.20050421093045">@
several plugins of the dyna variety and support files
newer than the version included in Leo4.3 alpha 4, March 15, 2005
exS all but retired, newer dynaclick not ready for distribution.
look in version history for a few minor changes to bring
dyna_menu up to Leo4.3 code. and some cosmetic changes
for htmlize and du_test and their config and a few option flippers.

had to move a few macros to get under my host single filesize limit.
look them up in older versions of dyna menu. pychecker2, leoglobals, etc.

executeScript on this node to insert your plugin path
if it looks ok remove the #comment
@c

&lt;&lt; insertAplug &gt;&gt;
insertAplug()

@language python
@color
@tabwidth -4
</t>
<t tx="ekr.20050421093045.1">def insertAplug(wch= 'i'): #i/r
    """use to insertAt 1.0 #@path plugindir
    """
    import leoGlobals as g
    import os, sys

    k = g.os_path_split(g.app.loadDir)[0]
    #this should fix the slashes and lower cases' it on win9x
    path = g.os_path_normpath(g.os_path_abspath(g.os_path_join(k, "plugins")))

    if not g.os_path_isdir(path):
        print 'give up', path; raise NameError

    if 'i' in wch:
        c = g.top()
        p = c.currentPosition()
        Tx = c.frame.body
        Tx.setInsertionPoint(1.0)
        Tx.insertAtInsertPoint('#@path %s\n'%(path,))
        Tx.onBodyWillChange(p, "Typing")  
</t>
<t tx="ekr.20050421093045.133">;ini may be shortlived in favor of @settings when thats feasible
;leave nosent so it isn't updated on leo open and all comments lost
; but if you change something here, it will overwrite any previous ini on disk.
;
;current properties ini editor will not have enough room for all these.
;pick only about a dozzen of your favorites more if you have more screen size
; True==1 False==0 just like the old days works too, case insensitive
;case sensitive on section names, insensitive on item names
;untested with spaces or Unicode in filenames please report any problem. 


[main]
verbosity=0
;verbosity for du_test and @test
;tempfile used in makatemp and tim1crunch, not active yet, edit dynacommon
;tmpfile = site-packages

;no source print after checks
justPyChecker=1

bugImport=0
tabstrip=4


[htmlize]
;which external colorizer for @language other than python
;leave blank for none or comment out
;hilighter=silvercity
hilighter=source-highlight
;hilighter=

;codefold = False
stripcomments = False
stripsentinals = True
stripnodesents = False
stripdirectives = False
noNUMBER = False
noOP = False
noNAME = True

;filename = c:\temp\htmlize.html
timestring = default

;use leodefault if Leo has one or default for whats hardwired in dyna_menu
;non existant or commented out values use the default in dyna_menu

;have to invent a new node, a clone with languageformatconversion
;hate duplicating here the defaults hardwired in htmlize, but anyways
;colors
;token_NUMBER  =  #483D8B  ;black/darkslateblue
;token_OP      =  #000080  ;black/navy
;token_STRING  =  #00AA00  ;green 00cc66
;token_COMMENT =  #DD0000  ;red cc0033
;token_NAME     = #4B0082  ;black/indigo
;token_ERRORTOKEN= #FF8080  ;redred bare null does it
;token_KEYWORD    =  #0066ff  ;blue
;token_TEXT       =  #000000  ;black /is text fg color too
;token_LeoDir     =  #228B22  ;directive, forest comment
token_LeoSen     =  #BC8F8F  ;sentinal, tan fade comment
token_bg         =  #FFFAFA  ;snow

; comments can be after values but not spaces or commas?
;comments can be between values?
;configparser needs a complete testsuite to answer these questions
;maybe there is one already?


@language elisp
</t>
<t tx="ekr.20050427102121"></t>
<t tx="ekr.20050513171201">'''usetemacs is a Leo plugin that patches the temacs modules Emacs emulation
into the standard Leo Tkinter Text editor.

Create a usetemacs.ini file to rebind shortcuts that conflict with those in your
leoSettings.leo file. There are many such conflicts. For example, Ctrl-s is
incremental search forward here but by default it is Save in Leo. 

See Help-&gt;Temacs Help for a complete listing of commands and keystrokes.
'''</t>
<t tx="ekr.20050523073009"></t>
<t tx="ekr.20050527084754">
#if self.uC:
#    self.previousStroke = stroke
#    return self.universalDispatch( event, stroke )

#if self.controlx:
#    self.previousStroke = stroke
#     return self.doControlX( event, stroke )


#if stroke in ('&lt;Control-s&gt;', '&lt;Control-r&gt;' ): 
#    self.previousStroke = stroke
#    return self.startIncremental( event, stroke )

#if self.isearch:
#   return self.iSearch( event )

#if stroke == '&lt;Alt-g&gt;':
#    self.previousStroke = stroke
#    return self.startGoto( event )
#if self.goto:
#    return self.Goto( event )

#if stroke == '&lt;Alt-z&gt;':
#    self.previousStroke = stroke
#    return self.startZap( event )

#if self.zap:
#    return self.zapTo( event )</t>
<t tx="ekr.20050527084754.1">
    #if self.howM:
    #    return self.howMany( event )
        
    #if self.abbrevMode:
    #    return self.abbrevCommand1( event )
        
    #if self.altx:
    #    return self.doAlt_X( event )

    #if stroke == '&lt;Alt-percent&gt;':
    #    self.previousStroke = stroke
    #    return self.masterQR( event )  
    #if self.qlisten:
    #    return self.masterQR( event )
        
    #if self.rString:
    #    return self.replaceString( event )
     
    #if self.negativeArg:
    #    return self.negativeArgument( event, stroke )
    
    #if stroke == '&lt;Control-Alt-w&gt;':
    #    self.previousStroke = '&lt;Control-Alt-w&gt;'   
    #    return 'break'</t>
<t tx="ekr.20050527111832"># EKR: This is a generator (it contains a yield).
# EKR: To make this work we must define a new generator for each call to regionalExpandAbbrev.
def searchXR( i1 , i2, ins, event ):
    tbuffer.tag_add( 'sXR', i1, i2 )
    while i1:
        tr = tbuffer.tag_ranges( 'sXR' )
        if not tr: break
        i1 = tbuffer.search( r'\w', i1, stopindex = tr[ 1 ] , regexp = True )
        if i1:
            word = tbuffer.get( '%s wordstart' % i1, '%s wordend' % i1 )
            tbuffer.tag_delete( 'found' )
            tbuffer.tag_add( 'found',  '%s wordstart' % i1, '%s wordend' % i1 )
            tbuffer.tag_config( 'found', background = 'yellow' )
            if self.abbrevs.has_key( word ):
                svar, label = self.getSvarLabel( event )
                svar.set( 'Replace %s with %s? y/n' % ( word, self.abbrevs[ word ] ) )
                yield None
                if self.regXKey == 'y':
                    ind = tbuffer.index( '%s wordstart' % i1 )
                    tbuffer.delete( '%s wordstart' % i1, '%s wordend' % i1 )
                    tbuffer.insert( ind, self.abbrevs[ word ] )
            i1 = '%s wordend' % i1
    tbuffer.mark_set( 'insert', ins )
    tbuffer.selection_clear()
    tbuffer.tag_delete( 'sXR' )
    tbuffer.tag_delete( 'found' )
    svar, label = self.getSvarLabel( event )
    svar.set( '' )
    self.setLabelGrey( label )
    self._setRAvars()</t>
<t tx="ekr.20050527112828">Emacs.lossage.reverse()
Emacs.lossage.append( event.char ) #Then we add the new char.  Hopefully this will keep Python from allocating a new array each time.
Emacs.lossage.reverse()

self.keysymhistory.reverse()
self.keysymhistory.append( event.keysym )
self.keysymhistory.reverse()</t>
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
<t tx="mork.20040926105355.9">def openChaptersFile( fileName ):
    zf = zipfile.ZipFile( fileName )
    import cStringIO
    file = cStringIO.StringIO()
    name = zf.namelist()
    csfiles = [ [], [] ]
    for x in name :
        zi = zf.getinfo( x )
        csfiles[ 0 ].append( zi.comment )
        cs = cStringIO.StringIO()
        csfiles[ 1 ].append( cs )           
        cs.write( zf.read( x ) )
        cs.seek( 0 )          
    zf.close()
    csfiles = zip( csfiles[ 0 ], csfiles[ 1 ] )
    return csfiles
</t>
<t tx="mork.20040926105355.29">oldOpen = leoFileCommands.fileCommands.open

def newOpen( self,file,fileName,readAtFileNodesFlag=True,silent=False):

    global iscStringIO
    c = self.c
    
    if zipfile.is_zipfile( fileName ):
        iscStringIO = True
        chapters = openChaptersFile( fileName )
        g.es( str( len( chapters ) ) + " Chapters To Read", color = 'blue' )
        insertChapters( chapters, c.frame, c )
        g.es( "Finished Reading Chapters", color = 'blue' )
        iscStringIO = False
        return True

    return oldOpen(self,file,fileName,readAtFileNodesFlag,silent)</t>
<t tx="mork.20040929090525.1">def zipChapters( fileName, pagenames, c, chapList ):
    #takes list of StringIO instances and zips them to a file
    zf = zipfile.ZipFile( fileName, 'w',  zipfile.ZIP_DEFLATED )
    for x ,fname in enumerate( pagenames ):
        sv = getSV( fname, c )
        zif = zipfile.ZipInfo( str( x ) )
        zif.comment = sv.get()
        zif.compress_type = zipfile.ZIP_DEFLATED
        chapList[ x ].seek( 0 )
        zf.writestr( zif ,chapList[ x ].read() )
    zf.close()</t>
<t tx="mork.20041013092542.1">&lt;&lt; docstring &gt;&gt;

@language python
@tabwidth -4

&lt;&lt; imports &gt;&gt;
&lt;&lt; globals &gt;&gt;
__version__ = '.57'
&lt;&lt;version history&gt;&gt;
&lt;&lt; documentation &gt;&gt;

@others

&lt;&lt;exampleTemacsExtension.py&gt;&gt;
&lt;&lt;usetemacs.ini example&gt;&gt;</t>
<t tx="mork.20041013092542.2">

labels = weakref.WeakKeyDictionary()
editors = weakref.WeakKeyDictionary()
haveseen = weakref.WeakKeyDictionary()
extensions = []
new_keystrokes = {}
leocommandnames = None</t>
<t tx="mork.20041013092542.3">def utTailEnd( buffer , frame ):
    '''A method that Emacs will call with its _tailEnd method'''
    buffer.event_generate( '&lt;Key&gt;' )
    buffer.update_idletasks()
    return 'break'
</t>
<t tx="mork.20041013092542.5">def addMenu( tag, keywords ):
    '''Adds the Temacs Help option to Leo's Help menu'''
    
    c = keywords.get('c')
    if not c: return

    men = c.frame.menu.getMenu( 'Help' )
    men.add_separator()
    men.add_command( label = 'Temacs Help', command = seeHelp )</t>
<t tx="mork.20041013092542.6">def seeHelp():
    '''Opens a Help dialog that shows the Emac systems commands and keystrokes'''
    tl = Tk.Toplevel()
    ms = tl.maxsize()
    tl.geometry( '%sx%s+0+0' % ( ( ms[ 0 ]/3 ) *2 , ms[ 1 ]/2 )) #half the screen height, half the screen width
    tl.title( "Temacs Help" )
    #fixedFont = Pmw.logicalfont( 'Fixed' )
    fixedFont = tkFont.Font( family = 'Fixed', size = 14 )
    #t = Pmw.ScrolledText( tl , text_font = fixedFont , text_background = 'white', hscrollmode = 'static', text_wrap='none')
    tc = ScrolledText.ScrolledText( tl, font = fixedFont, background = 'white', wrap = 'word' )
    sbar = Tk.Scrollbar( tc.frame, orient = 'horizontal' )
    sbar.configure( command = tc.xview )
    tc.configure( xscrollcommand = sbar.set )
    sbar.pack( side = 'bottom', fill = 'x' )
    for z in tc.frame.children.values():
        sbar.pack_configure( before = z )
    #t.settext( temacs.Emacs.getHelpText() )
    tc.insert( '1.0', temacs.Emacs.getHelpText() )
    lc='''\n---------Leo Commands-----------\n'''
    tc.insert( 'end', lc )
    leocommandnames.sort()
    lstring = '\n'.join( leocommandnames )
    tc.insert( 'end', lstring )
    def clz( tl = tl ):
        tl.withdraw()
        tl.destroy()
    #g = Pmw.Group( tl )
    g = Tk.Frame( tl )
    g.pack( side = 'bottom' )
    tc.pack( side = 'top' ,expand = 1, fill = 'both')
    e = Tk.Label( g, text = 'Search:' )
    e.pack( side = 'left' )
    #ef = Pmw.EntryField( g.interior() , 
    #                     labelpos = 'w', 
    #                     label_text = 'Search:' ,
    #                     entry_background = 'white',
    #                     entry_foreground = 'blue')
    #ef.pack( side = 'left' )
    ef = Tk.Entry( g, background = 'white', foreground = 'blue' )
    ef.pack( side = 'left' )
    def search():
        
        #stext = ef.getvalue()
        stext = ef.get()
        #tc = t.component( 'text' )
        tc.tag_delete( 'found' )
        tc.tag_configure( 'found', background = 'red' )
        ins = tc.index( 'insert' )
        ind = tc.search( stext, 'insert', stopindex = 'end', nocase = True )
        if not ind:
            ind = tc.search( stext, '1.0', stopindex = 'end', nocase = True )
        if ind:
            tc.mark_set( 'insert', '%s +%sc' % ( ind , len( stext ) ) )
            tc.tag_add(  'found', 'insert -%sc' % len( stext ) , 'insert' )
            tc.see( ind )
        
    go = Tk.Button( g , text = 'Go', command = search )
    go.pack( side = 'left' )
    b = Tk.Button( g  , text = 'Close' , command = clz )
    b.pack( side = 'left' )
    def watch( event ):
        search()
        
    #ef.component( 'entry' ).bind( '&lt;Return&gt;', watch )
    ef.bind( '&lt;Return&gt;', watch )
    #fixedFont = Pmw.logicalfont( 'Fixed' )
    #t = Pmw.ScrolledText( tl , text_font = fixedFont , text_background = 'white', hscrollmode = 'static', text_wrap='none')
    #t.pack( expand = 1, fill = 'both')
    #t.settext( temacs.Emacs.getHelpText() )
</t>
<t tx="mork.20041030164547">'''temacs is a binding module for the Tkinter Text widget.

Using the setBufferStrokes def will bind callbacks to the widget.'''

@language python
@tabwidth -4

__version__ = ".55"
&lt;&lt; version history &gt;&gt;
&lt;&lt; documentation &gt;&gt;
&lt;&lt; imports &gt;&gt;

@others

if __name__ == '__main__':
    &lt;&lt; run standalone tests &gt;&gt;</t>
<t tx="mork.20041030164547.1"># pretty low level imports. These may be all the imports the module needs

import leoGlobals as g # ekr

import Tkinter
import string
import weakref
import new
import sys
import re
import os
</t>
<t tx="mork.20041030164547.2">def setLabelGrey( self, label ):
    label.configure( background = 'lightgrey' )
</t>
<t tx="mork.20041030164547.3">def setLabelBlue( self ,label ):
    label.configure( background = 'lightblue' ) 
</t>
<t tx="mork.20041030164547.4">def _tailEnd( self, tbuffer ):
    '''This returns the tailEnd function that has been configure for the tbuffer parameter.'''
    if self.tailEnds.has_key( tbuffer ):
        return self.tailEnds[ tbuffer ]( tbuffer )
    else:
        return 'break'
</t>
<t tx="mork.20041030164547.5">#self.tailEnds = {}
def setTailEnd( self, tbuffer , tailCall ):
    '''This method sets a ending call that is specific for a particular Text widget.
       Some environments require that specific end calls be made after a keystroke
       or command is executed.'''
    self.tailEnds[ tbuffer ] = tailCall
</t>
<t tx="mork.20041030164547.6">#self.undoers = {}
def setUndoer( self, tbuffer, undoer ):
    '''This method sets the undoer method for the Emacs instance.'''
    self.undoers[ tbuffer ] = undoer
</t>
<t tx="mork.20041030164547.7">def doUndo(  self, event, amount = 1 ):
    tbuffer = event.widget
    if self.undoers.has_key( tbuffer ):
        for z in xrange( amount ):
            self.undoers[ tbuffer ]()
    return 'break'
</t>
<t tx="mork.20041030164547.8">#self.lastMacro = None
#self.macs = []
#self.macro = []
#self.namedMacros = {}
#self.macroing = False
def startKBDMacro( self, event ):

    svar, label = self.getSvarLabel( event )
    svar.set( 'Recording Keyboard Macro' )
    label.configure( background = 'lightblue' )
    self.macroing = True
    return 'break'
</t>
<t tx="mork.20041030164547.9">def recordKBDMacro( self, event, stroke ):
    if stroke != '&lt;Key&gt;':
        self.macro.append( (stroke, event.keycode, event.keysym, event.char) )
    elif stroke == '&lt;Key&gt;':
        if event.keysym != '??':
            self.macro.append( ( event.keycode, event.keysym ) )
    return
</t>
<t tx="mork.20041030164547.10">def stopKBDMacro( self, event ):
    #global macro, lastMacro, macroing
    if self.macro:
        self.macro = self.macro[ : -4 ]
        self.macs.insert( 0, self.macro )
        self.lastMacro = self.macro
        self.macro = []

    self.macroing = False
    svar, label = self.getSvarLabel( event )
    svar.set( 'Keyboard macro defined' )
    label.configure( background = 'lightgrey' )
    return 'break' 
</t>
<t tx="mork.20041030164547.11">def _executeMacro( self, macro, tbuffer ):
    
    for z in macro:
        if len( z ) == 2:
            tbuffer.event_generate( '&lt;Key&gt;', keycode = z[ 0 ], keysym = z[ 1 ] ) 
        else:
            meth = z[ 0 ].lstrip( '&lt;' ).rstrip( '&gt;' )
            method = self.cbDict[ meth ]
            ev = Tkinter.Event()
            ev.widget = tbuffer
            ev.keycode = z[ 1 ]
            ev.keysym = z[ 2 ]
            ev.char = z[ 3 ]
            self.masterCommand( ev , method, '&lt;%s&gt;' % meth )
    return self._tailEnd( tbuffer )  

</t>
<t tx="mork.20041030164547.12">def executeLastMacro( self, event ):
    tbuffer = event.widget
    if self.lastMacro:
        return self._executeMacro( self.lastMacro, tbuffer )
    return 'break'
</t>
<t tx="mork.20041030164547.13">def nameLastMacro( self, event ):
    '''Names the last macro defined.'''
    #global macroing
    svar, label = self.getSvarLabel( event )    
    if not self.macroing :
        self.macroing = 2
        svar.set( '' )
        self.setLabelBlue( label )
        return 'break'
    if event.keysym == 'Return':
        name = svar.get()
        self._addToDoAltX( name, self.lastMacro )
        svar.set( '' )
        self.setLabelBlue( label )
        self.macroing = False
        self.stopControlX( event )
        return 'break'
    self.setSvar( event, svar )
    return 'break'
</t>
<t tx="mork.20041030164547.14">def _addToDoAltX( self, name, macro ):
    '''Adds macro to Alt-X commands.'''
    if not self.doAltX.has_key( name ):
        def exe( event, macro = macro ):
            self.stopControlX( event )
            return self._executeMacro( macro, event.widget )
        self.doAltX[ name ] = exe
        self.namedMacros[ name ] = macro
        return True
    else:
        return False
</t>
<t tx="mork.20041030164547.15">def loadMacros( self,event ):
    '''Asks for a macro file name to load.'''
    import tkFileDialog
    f = tkFileDialog.askopenfile()
    if f == None: return 'break'
    else:
        return self._loadMacros( f )       
</t>
<t tx="mork.20041030164547.16">def _loadMacros( self, f ):
    '''Loads a macro file into the macros dictionary.'''
    import cPickle
    macros = cPickle.load( f )
    for z in macros:
        self._addToDoAltX( z, macros[ z ] )
    return 'break'
</t>
<t tx="mork.20041030164547.17">def getMacroName( self, event ):
    '''A method to save your macros to file.'''
    #global macroing
    svar, label = self.getSvarLabel( event )
    if not self.macroing:
        self.macroing = 3
        svar.set('')
        self.setLabelBlue( label )
        return 'break'
    if event.keysym == 'Return':
        self.macroing = False
        self.saveMacros( event, svar.get() )
        return 'break'
    if event.keysym == 'Tab':
        svar.set( self._findMatch( svar, self.namedMacros ) )
        return 'break'        
    self.setSvar( event, svar )
    return 'break'    
</t>
<t tx="mork.20041030164547.18">def saveMacros( self, event, macname ):
    '''Asks for a file name and saves it.'''
    import tkFileDialog
    name = tkFileDialog.asksaveasfilename()
    if name:
        f = file( name, 'a+' )
        f.seek( 0 )
        if f:
            self._saveMacros( f, macname ) 
    return 'break'
</t>
<t tx="mork.20041030164547.19">def _saveMacros( self, f , name ):
    '''Saves the macros as a pickled dictionary'''
    import cPickle
    fname = f.name
    try:
        macs = cPickle.load( f )
    except:
        macs = {}
    f.close()
    if self.namedMacros.has_key( name ):
        macs[ name ] = self.namedMacros[ name ]
        f = file( fname, 'w' )
        cPickle.dump( macs, f )
        f.close()   
</t>
<t tx="mork.20041030164547.20">#self.ccolumn = '0'
def setCommentColumn( self, event ):
    #global ccolumn
    cc= event.widget.index( 'insert' )
    cc1, cc2 = cc.split( '.' )
    self.ccolumn = cc2
    return 'break'
</t>
<t tx="mork.20041030164547.21">def indentToCommentColumn( self, event ):
    tbuffer = event.widget
    i = tbuffer.index( 'insert lineend' )
    i1, i2 = i.split( '.' )
    i2 = int( i2 )
    c1 = int( self.ccolumn )
    if i2 &lt; c1:
        wsn = c1 - i2
        tbuffer.insert( 'insert lineend', ' '* wsn )
    if i2 &gt;= c1:
        tbuffer.insert( 'insert lineend', ' ')
    tbuffer.mark_set( 'insert', 'insert lineend' )
    return self._tailEnd( tbuffer ) 
</t>
<t tx="mork.20041030164547.22">def exchangePointMark( self, event ):
    if not self._chckSel( event ):
        return
    tbuffer = event.widget
    s1 = tbuffer.index( 'sel.first' )
    s2 = tbuffer.index( 'sel.last' )
    i = tbuffer.index( 'insert' )
    if i == s1:
        tbuffer.mark_set( 'insert', s2 )
    else:
        tbuffer.mark_set('insert', s1 )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.23">#self.howM = False
def howMany( self, event ):
    #global howM
    svar, label = self.getSvarLabel( event )
    if event.keysym == 'Return':
        tbuffer = event.widget
        txt = tbuffer.get( '1.0', 'end' )
        import re
        reg1 = svar.get()
        reg = re.compile( reg1 )
        i = reg.findall( txt )
        svar.set( '%s occurances found of %s' % (len(i), reg1 ) )
        self.setLabelGrey( label )
        #self.howM = False
        self.mcStateManager.setState( 'howM', False )
        return 'break'
    self.setSvar( event, svar )
    return 'break'
</t>
<t tx="mork.20041030164547.24">def startHowMany( self, event ):
    #global howM
    #self.howM = True
    self.mcStateManager.setState( 'howM', True )
    svar, label = self.getSvarLabel( event )
    svar.set( '' )
    self.setLabelBlue( label )
    return 'break'
</t>
<t tx="mork.20041030164547.25">def selectParagraph( self, event ):
    tbuffer = event.widget
    txt = tbuffer.get( 'insert linestart', 'insert lineend' )
    txt = txt.lstrip().rstrip()
    i = tbuffer.index( 'insert' )
    if not txt:
        while 1:
            i = tbuffer.index( '%s + 1 lines' % i )
            txt = tbuffer.get( '%s linestart' % i, '%s lineend' % i )
            txt = txt.lstrip().rstrip()
            if txt:
                self._selectParagraph( tbuffer, i )
                break
            if tbuffer.index( '%s lineend' % i ) == tbuffer.index( 'end' ):
                return 'break'
    if txt:
        while 1:
            i = tbuffer.index( '%s - 1 lines' % i )
            txt = tbuffer.get( '%s linestart' % i, '%s lineend' % i )
            txt = txt.lstrip().rstrip()
            if not txt or tbuffer.index( '%s linestart' % i ) == tbuffer.index( '1.0' ):
                if not txt:
                    i = tbuffer.index( '%s + 1 lines' % i )
                self._selectParagraph( tbuffer, i )
                break     
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.26">def _selectParagraph( self, tbuffer, start ):
    i2 = start
    while 1:
        txt = tbuffer.get( '%s linestart' % i2, '%s lineend' % i2 )
        if tbuffer.index( '%s lineend' % i2 )  == tbuffer.index( 'end' ):
            break
        txt = txt.lstrip().rstrip()
        if not txt: break
        else:
            i2 = tbuffer.index( '%s + 1 lines' % i2 )
    tbuffer.tag_add( 'sel', '%s linestart' % start, '%s lineend' % i2 )
    tbuffer.mark_set( 'insert', '%s lineend' % i2 )
</t>
<t tx="mork.20041030164547.27">def killParagraph( self, event ):   
    tbuffer = event.widget
    i = tbuffer.index( 'insert' )
    txt = tbuffer.get( 'insert linestart', 'insert lineend' )
    if not txt.rstrip().lstrip():
        i = tbuffer.search( r'\w', i, regexp = True, stopindex = 'end' )
    self._selectParagraph( tbuffer, i )
    i2 = tbuffer.index( 'insert' )
    self.kill( event, i, i2 )
    tbuffer.mark_set( 'insert', i )
    tbuffer.selection_clear()
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.28">def backwardKillParagraph( self, event ):   
    tbuffer = event.widget
    i = tbuffer.index( 'insert' )
    i2 = i
    txt = tbuffer.get( 'insert linestart', 'insert lineend' )
    if not txt.rstrip().lstrip():
        self.movingParagraphs( event, -1 )
        i2 = tbuffer.index( 'insert' )
    self.selectParagraph( event )
    i3 = tbuffer.index( 'sel.first' )
    self.kill( event, i3, i2 )
    tbuffer.mark_set( 'insert', i )
    tbuffer.selection_clear()
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.29">#self.reset = False
def iterateKillBuffer( self ):
    #global reset
    while 1:
        if self.killbuffer:
            self.last_clipboard = None
            for z in self.killbuffer:
                if self.reset:
                    self.reset = False
                    break        
                yield z
        
            
</t>
<t tx="mork.20041030164547.30">#mbuffers = {}
#svars = {}
def setBufferStrokes( self, tbuffer, label ):
        '''setBufferStrokes takes a Tk Text widget called 'tbuffer'. 'stext' is a function or method
        that when called will return the value of the search text. 'rtext' is a function or method
        that when called will return the value of the replace text.  It is this method and
        getHelpText that users of the temacs module should call.  The rest are callback functions
        that enable the Emacs emulation.'''
        
        g.trace(tbuffer,label)
    
        Emacs.Emacs_instances[ tbuffer ] = self
        def cb( evstring ):
            _cb = None
            if self.cbDict.has_key( evstring ):
                _cb = self.cbDict[ evstring ]
            evstring = '&lt;%s&gt;' % evstring
            if evstring != '&lt;Key&gt;':
                # g.trace(evstring)
                tbuffer.bind( evstring,  lambda event, meth = _cb: self.masterCommand( event, meth , evstring) )
            else:
                # g.trace('+',evstring)
                tbuffer.bind( evstring,  lambda event, meth = _cb: self.masterCommand( event, meth , evstring), '+' )

        # EKR: create one binding for each entry in cbDict.
        for z in self.cbDict:
            cb( z )
        
        self.mbuffers[ tbuffer ] = label
        self.svars[ tbuffer ] = Tkinter.StringVar()
        def setVar( event ):
            label = self.mbuffers[ event.widget ]
            svar = self.svars[ event.widget ]
            label.configure( textvariable = svar )
        tbuffer.bind( '&lt;FocusIn&gt;', setVar, '+' )
        def scrollTo( event ):
            event.widget.see( 'insert' )
        
        #tbuffer.bind( '&lt;Enter&gt;', scrollTo, '+' )
        
        # EKR: This _adds_ a binding for all &lt;Key&gt; events, so _all_ key events go through masterCommand.
        cb( 'Key' )
</t>
<t tx="mork.20041030164547.31">def moveTo( self, event, spot ):
    tbuffer = event.widget
    tbuffer.mark_set( Tkinter.INSERT, spot )
    tbuffer.see( spot )
    return 'break'
</t>
<t tx="mork.20041030164547.33">def moveword( self, event, way  ):
    '''This function moves the cursor to the next word, direction dependent on the way parameter'''
    
    tbuffer = event.widget
    #i = way
    
    ind = tbuffer.index( 'insert' )
    if way == 1:
         ind = tbuffer.search( '\w', 'insert', stopindex = 'end', regexp=True )
         if ind:
            nind = '%s wordend' % ind
         else:
            nind = 'end'
    else:
         ind = tbuffer.search( '\w', 'insert -1c', stopindex= '1.0', regexp = True, backwards = True )
         if ind:
            nind = '%s wordstart' % ind 
         else:
            nind = '1.0'
    tbuffer.mark_set( 'insert', nind )
    tbuffer.see( 'insert' )
    tbuffer.event_generate( '&lt;Key&gt;' )
    tbuffer.update_idletasks()
    return 'break'</t>
<t tx="mork.20041030164547.34">def kill( self, event, frm, to  ):
    tbuffer = event.widget
    text = tbuffer.get( frm, to )
    self.addToKillBuffer( text )
    tbuffer.clipboard_clear()
    tbuffer.clipboard_append( text )    
    if frm == 'insert' and to =='insert lineend' and tbuffer.index( frm ) == tbuffer.index( to ):
        tbuffer.delete( 'insert', 'insert lineend +1c' )
        self.addToKillBuffer( '\n' )
    else:
        tbuffer.delete( frm, to )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.35">def deletelastWord( self, event ):
    #tbuffer = event.widget
    #i = tbuffer.get( 'insert' )
    self.moveword( event, -1 )
    self.kill( event, 'insert', 'insert wordend')
    self.moveword( event ,1 )
    return 'break'
</t>
<t tx="mork.20041030164547.36">def walkKB( self, event, frm, which ):# kb = self.iterateKillBuffer() ):
        #if not kb1:
        #    kb1.append( self.iterateKillBuffer() )
        #kb = kb1[ 0 ]
        #global reset
    tbuffer = event.widget
    i = tbuffer.index( 'insert' )
    t , t1 = i.split( '.' )
    clip_text = self.getClipboard( tbuffer )    
    if self.killbuffer or clip_text:
        if which == 'c':
            self.reset = True
            if clip_text:
                txt = clip_text
            else:
                txt = self.kbiterator.next()
            tbuffer.tag_delete( 'kb' )
            tbuffer.insert( frm, txt, ('kb') )
            tbuffer.mark_set( 'insert', i )
        else:
            if clip_text:
                txt = clip_text
            else:
                txt = self.kbiterator.next()
            t1 = str( int( t1 ) + len( txt ) )
            r = tbuffer.tag_ranges( 'kb' )
            if r and r[ 0 ] == i:
                tbuffer.delete( r[ 0 ], r[ -1 ] )
            tbuffer.tag_delete( 'kb' )
            tbuffer.insert( frm, txt, ('kb') )
            tbuffer.mark_set( 'insert', i )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.37">def killsentence( self, event, back = False ):
    tbuffer = event.widget
    i = tbuffer.search( '.' , 'insert', stopindex = 'end' )
    if back:
        i = tbuffer.search( '.' , 'insert', backwards = True, stopindex = '1.0' ) 
        if i == '':
            return 'break'
        i2 = tbuffer.search( '.' , i, backwards = True , stopindex = '1.0' )
        if i2 == '':
            i2 = '1.0'
        return self.kill( event, i2, '%s + 1c' % i )
        #return self.kill( event , '%s +1c' % i, 'insert' )
    else:
        i = tbuffer.search( '.' , 'insert', stopindex = 'end' )
        i2 = tbuffer.search( '.', 'insert', backwards = True, stopindex = '1.0' )
    if i2 == '':
       i2 = '1.0'
    else:
       i2 = i2 + ' + 1c '
    if i == '': return 'break'
    return self.kill( event, i2, '%s + 1c' % i )
</t>
<t tx="mork.20041030164547.38">def search( self, event, way , useregex=False):
    '''This method moves the insert spot to position that matches the pattern in the minibuffer'''
    tbuffer = event.widget
    svar, label = self.getSvarLabel( event )
    stext = svar.get()
    if stext == '': return 'break'
    try:
        if way == 'bak': #Means search backwards.
            i = tbuffer.search( stext, 'insert', backwards = True,  stopindex = '1.0' , regexp = useregex )
            if not i: #If we dont find one we start again at the bottom of the buffer. 
                i = tbuffer.search( stext, 'end', backwards = True, stopindex = 'insert', regexp = useregex)
        else: #Since its not 'bak' it means search forwards.
            i = tbuffer.search(  stext, "insert + 1c", stopindex = 'end', regexp = useregex ) 
            if not i: #If we dont find one we start at the top of the buffer. 
                i = tbuffer.search( stext, '1.0', stopindex = 'insert', regexp = useregex )
    except:
        return 'break'
    if not i or i.isspace(): return 'break'
    tbuffer.mark_set( 'insert', i )
    tbuffer.see( 'insert' )
</t>
<t tx="mork.20041030164547.39">def capitalize( self, event, which ):
    tbuffer = event.widget
    text = tbuffer.get( 'insert wordstart', 'insert wordend' )
    i = tbuffer.index( 'insert' )
    if text == ' ': return 'break'
    tbuffer.delete( 'insert wordstart', 'insert wordend' )
    if which == 'cap':
        text = text.capitalize() 
    if which == 'low':
        text = text.lower()
    if which == 'up':
        text = text.upper()
    tbuffer.insert( 'insert', text )
    tbuffer.mark_set( 'insert', i )    
    return 'break' 
</t>
<t tx="mork.20041030164547.40">def swapWords( self, event , swapspots ):
    tbuffer = event.widget
    txt = tbuffer.get( 'insert wordstart', 'insert wordend' )
    if txt == ' ' : return 'break'
    i = tbuffer.index( 'insert wordstart' )
    if len( swapspots ) != 0:
        def swp( find, ftext, lind, ltext ):
            tbuffer.delete( find, '%s wordend' % find )
            tbuffer.insert( find, ltext )
            tbuffer.delete( lind, '%s wordend' % lind )
            tbuffer.insert( lind, ftext )
            swapspots.pop()
            swapspots.pop()
            return 'break'
        if tbuffer.compare( i , '&gt;', swapspots[ 1 ] ):
            return swp( i, txt, swapspots[ 1 ], swapspots[ 0 ] )
        elif tbuffer.compare( i , '&lt;', swapspots[ 1 ] ):
            return swp( swapspots[ 1 ], swapspots[ 0 ], i, txt )
        else:
            return 'break'
    else:
        swapspots.append( txt )
        swapspots.append( i )
        return 'break'
</t>
<t tx="mork.20041030164547.41">def getHelpText():
    '''This returns a string that describes what all the
    keystrokes do with a bound Text widget.'''
    help_t = [ 'Buffer Keyboard Commands:',
    '----------------------------------------\n',
    '&lt;Control-p&gt;: move up one line',
    '&lt;Control-n&gt;: move down one line',
    '&lt;Control-f&gt;: move forward one char',
    '&lt;Conftol-b&gt;: move backward one char',
    '&lt;Control-o&gt;: insert newline',
    '&lt;Control-Alt-o&gt; : insert newline and indent',
    '&lt;Control-j&gt;: insert newline and tab',
    '&lt;Alt-&lt;&gt; : move to start of Buffer',
    '&lt;Alt- &gt;' +' &gt;: move to end of Buffer',
    '&lt;Control a&gt;: move to start of line',
    '&lt;Control e&gt; :move to end of line',
    '&lt;Alt-Up&gt;: move to start of line',
    '&lt;Alt-Down&gt;: move to end of line',
    '&lt;Alt b&gt;: move one word backward',
    '&lt;Alt f&gt; : move one word forward',
    '&lt;Control - Right Arrow&gt;: move one word forward',
    '&lt;Control - Left Arrow&gt;: move one word backwards',
    '&lt;Alt-m&gt; : move to beginning of indentation',
    '&lt;Alt-g&gt; : goto line number',
    '&lt;Control-v&gt;: scroll forward one screen',
    '&lt;Alt-v&gt;: scroll up one screen',
    '&lt;Alt-a&gt;: move back one sentence',
    '&lt;Alt-e&gt;: move forward one sentence',
    '&lt;Alt-}&gt;: move forward one paragraph',
    '&lt;Alt-{&gt;: move backwards one paragraph',
    '&lt;Alt-:&gt; evaluate a Python expression in the minibuffer and insert the value in the current buffer',
    'Esc Esc : evaluate a Python expression in the minibuffer and insert the value in the current buffer',
    '&lt;Control-x . &gt;: set fill prefix',
    '&lt;Alt-q&gt;: fill paragraph',
    '&lt;Alt-h&gt;: select current or next paragraph',
    '&lt;Control-x Control-@&gt;: pop global mark',
    '&lt;Control-u&gt;: universal command, repeats the next command n times.',
    '&lt;Alt -n &gt; : n is a number.  Processes the next command n times.',
    '&lt;Control-x (&gt;: start definition of kbd macro',
    '&lt;Control-x ) &gt; : stop definition of kbd macro',
    '&lt;Control-x e : execute last macro defined',
    '&lt;Control-u Control-x ( &gt;: execute last macro and edit',
    '&lt;Control-x Esc Esc &gt;: execute last complex command( last Alt-x command',
    '&lt;Control-x Control-c &gt;: save buffers kill Emacs',
    '''&lt;Control-x u &gt; : advertised undo.   This function utilizes the environments.
    If the buffer is not configure explicitly, there is no operation.''',
    '&lt;Control-_&gt;: advertised undo.  See above',
    '&lt;Control-z&gt;: iconfify frame',
    '----------------------------------------\n',
    '&lt;Delete&gt; : delete previous character',
    '&lt;Control d&gt;: delete next character',
    '&lt;Control k&gt; : delete from cursor to end of line. Text goes to kill buffer',
    '&lt;Alt d&gt;: delete word. Word goes to kill buffer',
    '&lt;Alt Delete&gt;: delete previous word. Word goes to kill buffer',
    '&lt;Alt k &gt;: delete current sentence. Sentence goes to kill buffer',
    '&lt;Control x Delete&gt;: delete previous sentence. Sentence goes to kill buffer',
    '&lt;Control y &gt;: yank last deleted text segment from\n kill buffer and inserts it.',
    '&lt;Alt y &gt;: cycle and yank through kill buffer.\n',
    '&lt;Alt z &gt;: zap to typed letter. Text goes to kill buffer',
    '&lt;Alt-^ &gt;: join this line to the previous one',
    '&lt;Alt-\ &gt;: delete surrounding spaces',
    '&lt;Alt-s&gt; &gt;: center line in current fill column',
    '&lt;Control-Alt-w&gt;: next kill is appended to kill buffer\n'
    
    '----------------------------------------\n',
    '&lt;Alt c&gt;: Capitalize the word the cursor is under.',
    '&lt;Alt u&gt;: Uppercase the characters in the word.',
    '&lt;Alt l&gt;: Lowercase the characters in the word.',
    '----------------------------------------\n',
    '&lt;Alt t&gt;: Mark word for word swapping.  Marking a second\n word will swap this word with the first',
    '&lt;Control-t&gt;: Swap characters',
    '&lt;Ctrl-@&gt;: Begin marking region.',
    '&lt;Ctrl-W&gt;: Kill marked region',
    '&lt;Alt-W&gt;: Copy marked region',
    '&lt;Ctrl-x Ctrl-u&gt;: uppercase a marked region',
    '&lt;Ctrl-x Ctrl-l&gt;: lowercase a marked region',
    '&lt;Ctrl-x h&gt;: mark entire buffer',
    '&lt;Alt-Ctrl-backslash&gt;: indent region to indentation of line 1 of the region.',
    '&lt;Ctrl-x tab&gt; : indent region by 1 tab',
    '&lt;Control-x Control-x&gt; : swap point and mark',
    '&lt;Control-x semicolon&gt;: set comment column',
    '&lt;Alt-semicolon&gt;: indent to comment column',
    '----------------------------------------\n',
    'M-! cmd -- Run the shell command line cmd and display the output',
    'M-| cmd -- Run the shell command line cmd with region contents as input',
    '----------------------------------------\n',
    '&lt;Control-x a e&gt;: Expand the abbrev before point (expand-abbrev). This is effective even when Abbrev mode is not enabled',
    '&lt;Control-x a g&gt;: Define an abbreviation for previous word',
    '&lt;Control-x a i g&gt;: Define a word as abbreviation for word before point, or in point',                        
    '----------------------------------------\n',
    '&lt;Control s&gt;: forward search, using pattern in Mini buffer.\n',
    '&lt;Control r&gt;: backward search, using pattern in Mini buffer.\n' ,
    '&lt;Control s Enter&gt;: search forward for a word, nonincremental\n',
    '&lt;Control r Enter&gt;: search backward for a word, nonincremental\n',
    '&lt;Control s Enter Control w&gt;: Search for words, ignoring details of punctuation',
    '&lt;Control r Enter Control w&gt;: Search backward for words, ignoring details of punctuation',
    '&lt;Control-Alt s&gt;: forward regular expression search, using pattern in Mini buffer\n',
    '&lt;Control-Alt r&gt;: backward regular expression search, using pattern in Mini buffer\n',
    '''&lt;Alt-%&gt;: begin query search/replace. n skips to next match. y changes current match.  
    q or Return exits. ! to replace all remaining matches with no more questions''',
    '''&lt;Control Alt %&gt; begin regex search replace, like Alt-%''',
    '&lt;Alt-=&gt;: count lines and characters in regions',
    '&lt;Alt-( &gt;: insert parentheses()',
    '&lt;Alt-) &gt;:  move past close',
    '&lt;Control-x Control-t&gt;: transpose lines.',
    '&lt;Control-x Control-o&gt;: delete blank lines' ,
    '&lt;Control-x r s&gt;: save region to register',
    '&lt;Control-x r i&gt;: insert to buffer from register',
    '&lt;Control-x r +&gt;: increment register',
    '&lt;Control-x r n&gt;: insert number 0 to register',
    '&lt;Control-x r space &gt; : point insert point to register',
    '&lt;Control-x r j &gt; : jump to register',
    '&lt;Control-x x&gt;: save region to register',
    '&lt;Control-x r r&gt; : save rectangle to register',
    '&lt;Control-x r o&gt;: open up rectangle',
    '&lt;Control-x r c&gt; : clear rectangle',
    '&lt;Control-x r d&gt; : delete rectangle',
    '&lt;Control-x r t&gt; : replace rectangle with string',
    '&lt;Control-x r k&gt; : kill rectangle',
    '&lt;Control-x r y&gt; : yank rectangle',
    '&lt;Control-g&gt; : keyboard quit\n',
    '&lt;Control-x = &gt; : position of cursor',
    '&lt;Control-x . &gt; : set fill prefix',
    '&lt;Control-x f &gt; : set the fill column',
    '&lt;Control-x Control-b &gt; : display the buffer list',
    '&lt;Control-x b &gt; : switch to buffer',
    '&lt;Control-x k &gt; : kill the specified buffer',
    '----------------------------------------\n',
    '&lt;Alt - - Alt-l &gt;: lowercase previous word',
    '&lt;Alt - - Alt-u&gt;: uppercase previous word',
    '&lt;Alt - - Alt-c&gt;: capitalise previous word',
    '----------------------------------------\n',
    '&lt;Alt-/ &gt;: dynamic expansion',
    '&lt;Control-Alt-/&gt;: dynamic expansion.  Expands to common prefix in buffer\n'
    '----------------------------------------\n',
    'Alt-x commands:\n',
    '(Pressing Tab will result in auto completion of the options if an appropriate match is found',
    'replace-string  -  replace string with string',
    'replace-regex - replace python regular expression with string',
    'append-to-register  - append region to register',
    'prepend-to-register - prepend region to register\n'
    'sort-lines - sort selected lines',
    'sort-columns - sort by selected columns',
    'reverse-region - reverse selected lines',
    'sort-fields  - sort by fields',
    'abbrev-mode - toggle abbrev mode on/off',
    'kill-all-abbrevs - kill current abbreviations',
    'expand-region-abbrevs - expand all abrevs in region',
    'read-abbrev-file - read abbreviations from file',
    'write-abbrev-file - write abbreviations to file',
    'list-abbrevs   - list abbrevs in minibuffer',
    'fill-region-as-paragraph - treat region as one paragraph and add fill prefix',
    'fill-region - fill paragraphs in region with fill prefix',
    'close-rectangle  - close whitespace rectangle',
    'how-many - counts occurances of python regular expression',
    'kill-paragraph - delete from cursor to end of paragraph',
    'backward-kill-paragraph - delete from cursor to start of paragraph',
    'backward-kill-sentence - delete from the cursor to the start of the sentence',
    'name-last-kbd-macro - give the last kbd-macro a name',
    'insert-keyboard-macro - save macros to file',
    'load-file - load a macro file',
    'kill-word - delete the word the cursor is on',
    'kill-line - delete form the cursor to end of the line', 
    'kill-sentence - delete the sentence the cursor is on',
    'kill-region - delete a marked region',
    'yank - restore what you have deleted',
    'backward-kill-word - delete previous word',
    'backward-delete-char - delete previous character',
    'delete-char - delete character under cursor' , 
    'isearch-forward - start forward incremental search',
    'isearch-backward - start backward incremental search',
    'isearch-forward-regexp - start forward regular expression incremental search',
    'isearch-backward-regexp - start backward return expression incremental search',
    'capitalize-word - capitalize the current word',
    'upcase-word - switch word to upper case',
    'downcase-word - switch word to lower case',
    'indent-region - indent region to first line in region',
    'indent-rigidly - indent region by a tab',
    'indent-relative - Indent from point to under an indentation point in the previous line',
    'set-mark-command - mark the beginning or end of a region',
     'kill-rectangle - kill the rectangle',
    'delete-rectangle - delete the rectangle',
    'yank-rectangle - yank the rectangle',
    'open-rectangle - open the rectangle',
    'clear-rectangle - clear the rectangle',
    'copy-to-register - copy selection to register',
    'insert-register - insert register into buffer',
    'copy-rectangle-to-register - copy buffer rectangle to register',
    'jump-to-register - jump to position in register',
    'point-to-register - insert point into register',
    'number-to-register - insert number into register',
    'increment-register - increment number in register',
    'view-register - view what register contains',
    'beginning-of-line - move to the beginning of the line',
    'end-of-line - move to the end of the line',
    'beginning-of-buffer - move to the beginning of the buffer',
    'end-of-buffer - move to the end of the buffer',
    'newline-and-indent - insert a newline and tab',
    'keyboard-quit - abort current command',
    'iconify-or-deiconify-frame - iconfiy current frame',
    'advertised-undo - undo the last operation',
    'back-to-indentation - move to first non-blank character of line',
    'delete-indentation - join this line to the previous one',
    'view-lossage - see the last 100 characters typed',
    'transpose-chars - transpose two letters',
    'transpose-words - transpose two words',
    'transpose-line - transpose two lines',
    'flush-lines - delete lines that match regex',
    'keep-lines - keep lines that only match regex',
    'insert-file - insert file at current position',
    'save-buffer - save file',
    'split-line - split line at cursor. indent to column of cursor',
    'upcase-region - Upper case region',
    'downcase-region - lower case region',
    'goto-line - goto a line in the buffer',
    'what-line - display what line the cursor is on',
    'goto-char - goto a char in the buffer',
    'set-fill-column - sets the fill column',
    'center-line - centers the current line within the fill column',
    'center-region - centers the current region within the fill column',   
    'forward-char - move the cursor forward one char',
    'backward-char - move the cursor backward one char',
    'previous-line - move the cursor up one line',
    'next-line - move the cursor down one line',
    'universal-argument - Repeat the next command "n" times',
    'digit-argument - Repeat the next command "n" times',
    'set-fill-prefix - Sets the prefix from the insert point to the start of the line',
    'scroll-up - scrolls up one screen',
    'scroll-down - scrolls down one screen',
    'append-to-buffer - Append region to a specified buffer',
    'prepend-to-buffer - Prepend region to a specified buffer',
    'copy-to-buffer - Copy region to a specified buffer, deleting the previous contents',
    'insert-buffer - Insert the contents of a specified buffer into current buffer at point',
    'list-buffers - Display the buffer list',
    'switch-to-buffer - switch to a different buffer, if it does not exits, it is created.',
    'kill-buffer - kill the specified buffer',
    'rename-buffer - rename the buffer',
    'query-replace - query buffer for pattern and replace it.  The user will be asked for a pattern, and for text to replace the pattern with.',
    'query-replace-regex - query buffer with regex and replace it.  The user will be asked for a pattern, and for text to replace the regex matches with.',
    'inverse-add-global-abbrev - add global abbreviation from previous word.  Will ask user for word to expand to',
    'expand-abbrev - Expand the abbrev before point. This is effective even when Abbrev mode is not enabled',
    're-search-forward - do a python regular expression search forward',
    're-search-backward - do a python regular expression search backward',
    'diff - compares two files, displaying the differences in an Emacs buffer named *diff*',
    'make-directory - create a new directory',
    'remove-directory - remove an existing directory if its empty',
    'delete-file - remove an existing file',
    'search-forward - search forward for a word',
    'search-backward - search backward for a word',
    'word-search-forward - Search for words, ignoring details of punctuation.', 
    'word-search-backward - Search backward for words, ignoring details of punctuation',
    'repeat-complex-command - repeat the last Alt-x command',
    'eval-expression - evaluate a Python expression and put the value in the current buffer',
    'tabify - turn the selected text\'s spaces into tabs',
    'untabify - turn the selected text\'s tabs into spaces',
    'shell-command -Run the shell command line cmd and display the output',
    'shell-command-on-region -Run the shell command line cmd with region contents as input',
    ]
    
    return '\n'.join( help_t )

getHelpText = staticmethod( getHelpText )











</t>
<t tx="mork.20041030164547.42">#self.killbuffer = []
def addToKillBuffer( self, text ):
    #global reset
    self.reset = True 
    if self.previousStroke in ( '&lt;Control-k&gt;', '&lt;Control-w&gt;' ,
     '&lt;Alt-d&gt;', '&lt;Alt-Delete', '&lt;Alt-z&gt;', '&lt;Delete&gt;',
     '&lt;Control-Alt-w&gt;' ) and len( self.killbuffer):
        self.killbuffer[ 0 ] = self.killbuffer[ 0 ] + text
        return
    self.killbuffer.insert( 0, text )
</t>
<t tx="mork.20041030164547.43">#self.controlx = False
#self.csr = { '&lt;Control-s&gt;': 'for', '&lt;Control-r&gt;':'bak' }
#self.pref = None
#self.zap = False
#self.goto = False
#self.previousStroke = ''
def masterCommand( self, event, method , stroke):
    '''The masterCommand is the central routing method of the Emacs method.
       All commands and keystrokes pass through here.'''
       
    special = event.keysym in ('Control_L','Control_R','Alt_L','Alt-R','Shift_L','Shift_R')
    inserted = not special or len(self.keysymhistory) == 0 or self.keysymhistory[0] != event.keysym

    # Don't add multiple special characters to history.
    if inserted:
        self.keysymhistory.insert(0,event.keysym)
        if len(event.char) &gt; 0:
            if len(Emacs.lossage) &gt; 99: Emacs.lossage.pop()
            Emacs.lossage.insert(0,event.char)
        
        if 1: # traces
            print event.keysym,stroke
            g.trace(self.keysymhistory)
            g.trace(Emacs.lossage)
        
    if 0:
        &lt;&lt; old insert code &gt;&gt;
    
            
    if self.macroing:
        if self.macroing == 2 and stroke != '&lt;Control-x&gt;':
            return self.nameLastMacro( event )
        elif self.macroing == 3 and stroke != '&lt;Control-x&gt;':
            return self.getMacroName( event )
        else:
           self.recordKBDMacro( event, stroke )
         
    if  stroke == '&lt;Control-g&gt;':
        self.previousStroke = stroke
        return self.keyboardQuit( event )
        
    if self.mcStateManager.hasState():
        self.previousStroke = stroke
        return self.mcStateManager( event, stroke ) # EKR: Invoke the __call__ method.
        
    if self.kstrokeManager.hasKeyStroke( stroke ):
        self.previousStroke = stroke
        return self.kstrokeManager( event, stroke ) # EKR: Invoke the __call__ method.

    &lt;&lt; old code &gt;&gt;
    if self.regXRpl: # EKR: a generator.
        try:
            self.regXKey = event.keysym
            self.regXRpl.next() # EKR: next() may throw StopIteration.
        finally:
            return 'break'

    &lt;&lt; old code 2 &gt;&gt;
    if self.abbrevOn:
        if self.expandAbbrev( event ) :
            return 'break'       

    if method:
        rt = method( event )
        self.previousStroke = stroke
        return rt</t>
<t tx="mork.20041030164547.44">#self.registers = {}

def copyToRegister( self, event ):

    if not self._chckSel( event ):
        return
    if event.keysym in string.letters:
        event.keysym = event.keysym.lower()
        tbuffer = event.widget
        txt = tbuffer.get( 'sel.first', 'sel.last' )
        self.registers[ event.keysym ] = txt
        return 
    self.stopControlX( event )
</t>
<t tx="mork.20041030164547.45">def copyRectangleToRegister( self, event ):
    if not self._chckSel( event ):
        return
    if event.keysym in string.letters:
        event.keysym = event.keysym.lower()
        tbuffer = event.widget
        r1, r2, r3, r4 = self.getRectanglePoints( event )
        rect = []
        while r1 &lt;= r3:
            txt = tbuffer.get( '%s.%s' %( r1, r2 ), '%s.%s' %( r1, r4 ) )
            rect.append( txt )
            r1 = r1 +1
        self.registers[ event.keysym ] = rect
    self.stopControlX( event )        
</t>
<t tx="mork.20041030164547.46">def prependToRegister( self, event ):
    #global regMeth, registermode, controlx, registermode
    event.keysym = 'p'
    self.setNextRegister( event )
    self.mcStateManager.setState( 'controlx', False )
    #self.controlx = True
</t>
<t tx="mork.20041030164547.47">def appendToRegister( self, event ):
    #global regMeth, registermode, controlx
    event.keysym = 'a'
    self.setNextRegister( event )
    self.mcStateManager.setState( 'controlx', True )
    #self.controlx = True
</t>
<t tx="mork.20041030164547.48">def _chckSel( self, event ):
     if not 'sel' in event.widget.tag_names():
        return False
     if not event.widget.tag_ranges( 'sel' ):
        return False  
     return True
</t>
<t tx="mork.20041030164547.49">def _ToReg( self, event , which):
    if not self._chckSel( event ):
        return
    if self._checkIfRectangle( event ):
        return
    if event.keysym in string.letters:
        event.keysym = event.keysym.lower()
        tbuffer = event.widget
        if not self.registers.has_key( event.keysym ):
            self.registers[ event.keysym ] = ''
        txt = tbuffer.get( 'sel.first', 'sel.last' )
        rtxt = self.registers[ event.keysym ]
        if self.which == 'p':
            txt = txt + rtxt
        else:
            txt = rtxt + txt
        self.registers[ event.keysym ] = txt
        return
</t>
<t tx="mork.20041030164547.50">def _checkIfRectangle( self, event ):
    if self.registers.has_key( event.keysym ):
        if isinstance( self.registers[ event.keysym ], list ):
            svar, label = self.getSvarLabel( event )
            self.stopControlX( event )
            svar.set( "Register contains Rectangle, not text" )
            return True
    return False           
</t>
<t tx="mork.20041030164547.51">def insertFromRegister( self, event ):
    tbuffer = event.widget
    if self.registers.has_key( event.keysym ):
        if isinstance( self.registers[ event.keysym ], list ):
            self.yankRectangle( event, self.registers[ event.keysym ] )
        else:
            tbuffer.insert( 'insert', self.registers[ event.keysym ] )
            tbuffer.event_generate( '&lt;Key&gt;' )
            tbuffer.update_idletasks()
    self.stopControlX( event )
</t>
<t tx="mork.20041030164547.52">def incrementRegister( self, event ):
    if self.registers.has_key( event.keysym ):
        if self._checkIfRectangle( event ):
            return
        if self.registers[ event.keysym ] in string.digits:
            i = self.registers[ event.keysym ]
            i = str( int( i ) + 1 )
            self.registers[ event.keysym ] = i
        else:
            self.invalidRegister( event, 'number' )
            return
    self.stopControlX( event )
</t>
<t tx="mork.20041030164547.53">def numberToRegister( self, event ):
    if event.keysym in string.letters:
        self.registers[ event.keysym.lower() ] = str( 0 )
    self.stopControlX( event )
</t>
<t tx="mork.20041030164547.54">def pointToRegister( self, event ):
    if event.keysym in string.letters:
        tbuffer = event.widget
        self.registers[ event.keysym.lower() ] = tbuffer.index( 'insert' )
    self.stopControlX( event )
</t>
<t tx="mork.20041030164547.55">def jumpToRegister( self, event ):
    if event.keysym in string.letters:
        if self._checkIfRectangle( event ):
            return
        tbuffer = event.widget
        i = self.registers[ event.keysym.lower() ]
        i2 = i.split( '.' )
        if len( i2 ) == 2:
            if i2[ 0 ].isdigit() and i2[ 1 ].isdigit():
                pass
            else:
                self.invalidRegister( event, 'index' )
                return
        else:
            self.invalidRegister( event, 'index' )
            return
        tbuffer.mark_set( 'insert', i )
        tbuffer.event_generate( '&lt;Key&gt;' )
        tbuffer.update_idletasks() 
    self.stopControlX( event ) 
</t>
<t tx="mork.20041030164547.56">def invalidRegister( self, event, what ):
    self.deactivateRegister( event )
    svar, label = self.getSvarLabel( event )
    svar.set( 'Register does not contain valid %s'  % what)
    return    
</t>
<t tx="mork.20041030164547.57">def setNextRegister( self, event ):
    #global regMeth, registermode
    if event.keysym == 'Shift':
        return
    if self.regMeths.has_key( event.keysym ):
        self.mcStateManager.setState( 'controlx', True )
        self.regMeth = self.regMeths[ event.keysym ]
        self.registermode = 2
        svar = self.svars[ event.widget ]
        svar.set( self.regText[ event.keysym ] )
        return
    self.stopControlX( event )
</t>
<t tx="mork.20041030164547.58">def executeRegister( self, event ):
    self.regMeth( event )
    if self.registermode: 
        self.stopControlX( event )
    return
</t>
<t tx="mork.20041030164547.59">def deactivateRegister( self, event ):
    #global registermode, regMeth
    svar, label = self.getSvarLabel( event )
    svar.set( '' )
    self.setLabelGrey( label )
    self.registermode = False
    self.regMeth = None
</t>
<t tx="mork.20041030164547.60">#self.abbrevMode = False
#self.abbrevOn = False
#self.abbrevs = {}
def abbreviationDispatch( self, event, which ):
    #global abbrevMode
    #if not self.abbrevMode:
    aM = self.mcStateManager.getState( 'abbrevMode' )
    if not aM:
        #self.abbrevMode = which
        self.mcStateManager.setState( 'abbrevMode', which )
        svar, label = self.getSvarLabel( event )
        svar.set( '' )
        self.setLabelBlue( label )
        return 'break'
    if aM:
        self.abbrevCommand1( event )
    return 'break'
</t>
<t tx="mork.20041030164547.61">def abbrevCommand1( self, event ):
    #global abbrevMode
    if event.keysym == 'Return':
        tbuffer = event.widget
        word = tbuffer.get( 'insert -1c wordstart', 'insert -1c wordend' )
        if word == ' ': return
        svar, label = self.getSvarLabel( event )
        aM = self.mcStateManager.getState( 'abbrevMode' )
        if aM == 1:
            self.abbrevs[ svar.get() ] = word
        elif aM == 2:
            self.abbrevs[ word ] = svar.get()
        #self.abbrevMode = False
        #self.mcStateManager.setState( 'abbrevMode', False )
        self.keyboardQuit( event )
        self.resetMiniBuffer( event )
        return 'break'
    svar, label = self.getSvarLabel( event )
    self.setSvar( event, svar )
    return 'break'
</t>
<t tx="mork.20041030164547.62">def expandAbbrev( self,event ):
    tbuffer = event.widget
    word = tbuffer.get( 'insert -1c wordstart', 'insert -1c wordend' )
    c = event.char.strip()
    if c: #We have to do this because this method is called from Alt-x and Control-x, we get two differnt types of data and tbuffer states.
        word = '%s%s' %( word, event.char )
    if self.abbrevs.has_key( word ):
        tbuffer.delete( 'insert -1c wordstart', 'insert -1c wordend' )
        tbuffer.insert( 'insert', self.abbrevs[ word ] ) 
        return self._tailEnd( tbuffer )
        #return True
    else: return False
</t>
<t tx="mork.20041030164547.63">#self.regXRpl = None
#self.regXKey = None
def regionalExpandAbbrev( self, event ):
    #global regXRpl
    if not self._chckSel( event ):
        return
    tbuffer = event.widget
    i1 = tbuffer.index( 'sel.first' )
    i2 = tbuffer.index( 'sel.last' ) 
    ins = tbuffer.index( 'insert' )
    &lt;&lt; define a new generator searchXR &gt;&gt;
    # EKR: the 'result' of calling searchXR is a generator object.
    self.regXRpl = searchXR( i1, i2, ins, event)
    self.regXRpl.next() # Call it the first time.
    return 'break' </t>
<t tx="mork.20041030164547.64">def _setRAvars( self ):
    #global regXRpl, regXKey
    self.regXRpl = self.regXKey = None 
</t>
<t tx="mork.20041030164547.65">def killAllAbbrevs( self, event ):
    #global abbrevs
    self.abbrevs = {}
    return self.keyboardQuit( event )
</t>
<t tx="mork.20041030164547.66">def toggleAbbrevMode( self, event ):
    #global abbrevOn
    #aO = self.mcStateManager.getState( 'abbrevOn' )
    svar, label = self.getSvarLabel( event )
    if self.abbrevOn:
        self.abbrevOn = False
        self.keyboardQuit( event )
        svar.set( "Abbreviations are Off" )  
        #self.mcStateManager.setState( 'abbrevOn', False ) #This doesnt work too well with the mcStateManager
    else:
        self.abbrevOn = True
        self.keyboardQuit( event )
        svar.set( "Abbreviations are On" )
        #self.mcStateManager.setState( 'abbrevOn', True )
</t>
<t tx="mork.20041030164547.67">def listAbbrevs( self, event ):
    svar, label = self.getSvarLabel( event )
    txt = ''
    for z in self.abbrevs:
        txt = '%s%s=%s\n' %( txt, z, self.abbrevs[ z ] )
    svar.set( '' )
    svar.set( txt )
    return 'break'
</t>
<t tx="mork.20041030164547.68">def readAbbreviations( self, event ):
    import tkFileDialog
    f = tkFileDialog.askopenfile()
    if f == None: return 'break'        
    return self._readAbbrevs( f )
</t>
<t tx="mork.20041030164547.69">def _readAbbrevs( self, f ):
    for x in f:
        a, b = x.split( '=' )
        b = b[ : -1 ]
        self.abbrevs[ a ] = b
    f.close()        
    return 'break'
</t>
<t tx="mork.20041030164547.70">def writeAbbreviations( self, event ):
    import tkFileDialog
    f = tkFileDialog.asksaveasfile() 
    if f == None: return 'break' 
    return self._writeAbbrevs( f )
</t>
<t tx="mork.20041030164547.71">def _writeAbbrevs( self, f ):
    for x in self.abbrevs:
        f.write( '%s=%s\n' %( x, self.abbrevs[ x ] ) )
    f.close()    
    return 'break'
</t>
<t tx="mork.20041030164547.72">def movingParagraphs( self, event, way ):
    tbuffer = event.widget
    i = tbuffer.index( 'insert' )
    
    if way == 1:
        while 1:
            txt = tbuffer.get( '%s linestart' % i, '%s lineend' %i )
            txt = txt.rstrip().lstrip()
            if not txt:
                i = tbuffer.search( r'\w', i, regexp = True, stopindex = 'end' )
                i = '%s' %i
                break
            else:
                i = tbuffer.index( '%s + 1 lines' % i )
                if tbuffer.index( '%s linestart' % i ) == tbuffer.index( 'end' ):
                    i = tbuffer.search( r'\w', 'end', backwards = True, regexp = True, stopindex = '1.0' )
                    i = '%s + 1c' % i
                    break
    else:
        while 1:
            txt = tbuffer.get( '%s linestart' % i, '%s lineend' %i )
            txt = txt.rstrip().lstrip()
            if not txt:
                i = tbuffer.search( r'\w', i, backwards = True, regexp = True, stopindex = '1.0' )
                i = '%s +1c' %i
                break
            else:
                i = tbuffer.index( '%s - 1 lines' % i )
                if tbuffer.index( '%s linestart' % i ) == '1.0':
                    i = tbuffer.search( r'\w', '1.0', regexp = True, stopindex = 'end' )
                    break
    if i : 
        tbuffer.mark_set( 'insert', i )
        tbuffer.see( 'insert' )
        return self._tailEnd( tbuffer )
    return 'break'
</t>
<t tx="mork.20041030164547.73">#self.fillPrefix = ''
def setFillPrefix( self, event ):
    #global fillPrefix
    tbuffer = event.widget
    txt = tbuffer.get( 'insert linestart', 'insert' )
    self.fillPrefix = txt
    return 'break'
</t>
<t tx="mork.20041030164547.74">def fillParagraph( self, event ):
    tbuffer = event.widget
    txt = tbuffer.get( 'insert linestart', 'insert lineend' )
    txt = txt.lstrip().rstrip()
    if txt:
        i = tbuffer.index( 'insert' )
        i2 = i
        txt2 = txt
        while txt2:
            pi2 = tbuffer.index( '%s - 1 lines' % i2)
            txt2 = tbuffer.get( '%s linestart' % pi2, '%s lineend' % pi2 )
            if tbuffer.index( '%s linestart' % pi2 ) == '1.0':
                i2 = tbuffer.search( '\w', '1.0', regexp = True, stopindex = 'end' )
                break
            if txt2.lstrip().rstrip() == '': break
            i2 = pi2
        i3 = i
        txt3 = txt
        while txt3:
            pi3 = tbuffer.index( '%s + 1 lines' %i3 )
            txt3 = tbuffer.get( '%s linestart' % pi3, '%s lineend' % pi3 )
            if tbuffer.index( '%s lineend' % pi3 ) == tbuffer.index( 'end' ):
                i3 = tbuffer.search( '\w', 'end', backwards = True, regexp = True, stopindex = '1.0' )
                break
            if txt3.lstrip().rstrip() == '': break
            i3 = pi3
        ntxt = tbuffer.get( '%s linestart' %i2, '%s lineend' %i3 )
        ntxt = self._addPrefix( ntxt )
        tbuffer.delete( '%s linestart' %i2, '%s lineend' % i3 )
        tbuffer.insert( i2, ntxt )
        tbuffer.mark_set( 'insert', i )
        return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.75">def _addPrefix( self, ntxt ):
        ntxt = ntxt.split( '.' )
        ntxt = map( lambda a: self.fillPrefix+a, ntxt )
        ntxt = '.'.join( ntxt )               
        return ntxt
</t>
<t tx="mork.20041030164547.76">def fillRegionAsParagraph( self, event ):
    if not self._chckSel( event ):
        return
    tbuffer = event.widget
    i1 = tbuffer.index( 'sel.first linestart' )
    i2 = tbuffer.index( 'sel.last lineend' )
    txt = tbuffer.get(  i1,  i2 )
    txt = self._addPrefix( txt )
    tbuffer.delete( i1, i2 )
    tbuffer.insert( i1, txt )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.77">def fillRegion( self, event ):
    if not self._chckSel( event ):
        return
    tbuffer = event.widget
    #i = tbuffer.index( 'insert' ) 
    s1 = tbuffer.index( 'sel.first' )
    s2 = tbuffer.index( 'sel.last' )
    tbuffer.mark_set( 'insert', s1 )
    self.movingParagraphs( event, -1 )
    if tbuffer.index( 'insert linestart' ) == '1.0':
        self.fillParagraph( event )
    while 1:
        self.movingParagraphs( event, 1 )
        if tbuffer.compare( 'insert', '&gt;', s2 ):
            break
        self.fillParagraph( event )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.78">#self.registermode = False
def doControlX( self, event, stroke, previous = [] ):
    #global registermode
    """previous.insert( 0, event.keysym )
    if len( previous ) &gt; 10: previous.pop()
    if stroke == '&lt;Key&gt;':
        if event.keysym in ( 'Shift_L', 'Shift_R' ):
            return
        if event.keysym == 'period':
            self.stopControlX( event )
            return self.setFillPrefix( event )
        if event.keysym == 'parenleft':
            self.stopControlX( event )
            return self.startKBDMacro( event )
        if event.keysym == 'parenright':
            self.stopControlX( event )
            return self.stopKBDMacro( event )
        if event.keysym == 'semicolon':
            self.stopControlX( event )
            return self.setCommentColumn( event )
        if event.keysym == 'Tab':
            self.stopControlX( event )
            return self.tabIndentRegion( event )
        if self.sRect:
            self.stringRectangle( event )
            return 'break'
        if event.keysym in ( 'a', 'i' , 'e'):
            svar, label = self.getSvarLabel( event )
            if svar.get() != 'a' and event.keysym == 'a':
                svar.set( 'a' )
                return 'break'
            elif svar.get() == 'a':
                if event.char == 'i':
                    svar.set( 'a i' )
                elif event.char == 'e':
                    self.stopControlX( event )
                    event.char = ''
                    self.expandAbbrev( event )
                return 'break'
        if event.keysym == 'g':
            svar, label = self.getSvarLabel( event )
            l = svar.get()
            if l == 'a':
                self.stopControlX( event )
                return self.abbreviationDispatch( event, 1 )
            elif l == 'a i':
                self.stopControlX( event )
                return self.abbreviationDispatch( event, 2 )
        if event.keysym == 'e':
            self.stopControlX( event )
            return self.executeLastMacro( event )
        if event.keysym == 'x' and previous[ 1 ] not in ( 'Control_L', 'Control_R'):
            event.keysym = 's' 
            self.setNextRegister( event )
            return 'break'
        if event.keysym == 'o' and self.registermode == 1:
            self.openRectangle( event )
            return 'break'
        if event.keysym == 'c' and self.registermode == 1:
            self.clearRectangle( event )
            return 'break'
        if event.keysym == 't' and self.registermode == 1:
            self.stringRectangle( event )
            return 'break'
        if event.keysym == 'y' and self.registermode == 1:
            self.yankRectangle( event )
            return 'break'
        if event.keysym == 'd' and self.registermode == 1:
            self.deleteRectangle( event )
            return 'break'
        if event.keysym == 'k' and self.registermode == 1:
            self.killRectangle( event )
            return 'break'       
        if self.registermode == 1:
            self.setNextRegister( event )
            return 'break'
        elif self.registermode == 2:
            self.executeRegister( event )
            return 'break'
        if event.keysym == 'r':
            self.registermode = 1
            svar = self.svars[ event.widget ]
            svar.set( 'C - x r' )
            return 'break'
        if event.keysym== 'h':
           self.stopControlX( event )
           event.widget.tag_add( 'sel', '1.0', 'end' )
           return 'break' 
        if event.keysym == 'equal':
            self.lineNumber( event )
            return 'break'
        if event.keysym == 'u':
            self.stopControlX( event )
            return self.doUndo( event, 2 )
    if stroke in self.xcommands:
        self.xcommands[ stroke ]( event )
        self.stopControlX( event )
    return 'break' """
    return self.cxHandler( event, stroke )
</t>
<t tx="mork.20041030164547.79">def startIncremental( self, event, stroke, which='normal' ):
    #global isearch, pref
    #widget = event.widget
    #if self.isearch:
    isearch = self.mcStateManager.getState( 'isearch' )
    if isearch:
        self.search( event, way = self.csr[ stroke ], useregex = self.useRegex() )
        self.pref = self.csr[ stroke ]
        self.scolorizer( event )
        return 'break'
    else:
        svar, label = self.getSvarLabel( event )
        #self.isearch = True'
        self.mcStateManager.setState( 'isearch', which )
        self.pref = self.csr[ stroke ]
        label.configure( background = 'lightblue' )
        label.configure( textvariable = svar )
        return 'break'
</t>
<t tx="mork.20041030164547.80">def iSearch( self, event, stroke ):
    if len( event.char ) == 0: return
    
    if stroke in self.csr: return self.startIncremental( event, stroke )
    svar, label = self.getSvarLabel( event )
    if event.keysym == 'Return':
          if svar.get() == '':
              return self.startNonIncrSearch( event, self.pref )
          else:
            return self.stopControlX( event )
          #return self._tailEnd( event.widget )
    widget = event.widget
    label.configure( textvariable = svar )
    #if event.keysym == 'Return':
    #      return self.stopControlX( event )
    self.setSvar( event, svar )
    if event.char != '\b':
       stext = svar.get()
       z = widget.search( stext , 'insert' , stopindex = 'insert +%sc' % len( stext ) )
       if not z:
           self.search( event, self.pref, useregex= self.useRegex() )
    self.scolorizer( event )
    return 'break'
</t>
<t tx="mork.20041030164547.81">def startZap( self, event ):
    #global zap
    #self.zap = True
    self.mcStateManager.setState( 'zap', True )
    svar, label = self.getSvarLabel( event )
    label.configure( background = 'lightblue' )
    svar.set( 'Zap To Character' )
    return 'break'
</t>
<t tx="mork.20041030164547.82">def zapTo( self, event ):
        #global zap

        widget = event.widget
        s = string.ascii_letters + string.digits + string.punctuation
        if len( event.char ) != 0 and event.char in s:
            #self.zap = False
            self.mcStateManager.setState( 'zap', False )
            i = widget.search( event.char , 'insert',  stopindex = 'end' )
            self.resetMiniBuffer( event )
            if i:
                t = widget.get( 'insert', '%s+1c'% i )
                self.addToKillBuffer( t )
                widget.delete( 'insert', '%s+1c' % i)
                return 'break'
        else:
            return 'break'
</t>
<t tx="mork.20041030164547.83">def changecbDict( self, changes ):
    for z in changes:
        if self.cbDict.has_key( z ):
            self.cbDict[ z ] = self.changes[ z ]
</t>
<t tx="mork.20041030164547.84">def startControlX( self, event ):
    '''This method starts the Control-X command sequence.'''  
    #global controlx
    #self.controlx = True
    self.mcStateManager.setState( 'controlx', True )
    svar, label = self.getSvarLabel( event )
    svar.set( 'Control - X' )
    label.configure( background = 'lightblue' )
    return 'break'
</t>
<t tx="mork.20041030164547.85">def stopControlX( self, event ):  #This will all be migrated to keyboardQuit eventually.
    '''This method clears the state of the Emacs instance'''
    #global controlx, rstring, isearch, sRect,negativeArg, uC, howM, altx
    #self.altx = False
    #self.howM = False
    #self.controlx = False
    #self.isearch = False
    if self.shuttingdown: return
    self.sRect = False
    #self.uC = False
    #self.negativeArg = False
    self.mcStateManager.clear()
    event.widget.tag_delete( 'color' )
    event.widget.tag_delete( 'color1' )
    if self.registermode:
        self.deactivateRegister( event )
    self.rectanglemode = 0
    self.bufferMode = None
    #self.rString = False
    self.resetMiniBuffer( event )
    event.widget.update_idletasks()     
    return 'break'

</t>
<t tx="mork.20041030164547.86">def resetMiniBuffer( self, event ):
    svar, label = self.getSvarLabel( event )
    svar.set( '' )
    label.configure( background = 'lightgrey' )
</t>
<t tx="mork.20041030164547.87">def setRegion( self, event ):   
    mrk = 'sel'
    tbuffer = event.widget
    def extend( event ):
        widget = event.widget
        widget.mark_set( 'insert', 'insert + 1c' )
        if self.inRange( widget, mrk ):
            widget.tag_remove( mrk, 'insert -1c' )
        else:
            widget.tag_add( mrk, 'insert -1c' )
            widget.tag_configure( mrk, background = 'lightgrey' )
            self.testinrange( widget )
        return 'break'
        
    def truncate( event ):
        widget = event.widget
        widget.mark_set( 'insert', 'insert -1c' )
        if self.inRange( widget, mrk ):
            self.testinrange( widget )
            widget.tag_remove( mrk, 'insert' )
        else:
            widget.tag_add( mrk, 'insert' )
            widget.tag_configure( mrk, background = 'lightgrey' )
            self.testinrange( widget  )
        return 'break'
        
    def up( event ):
        widget = event.widget
        if not self.testinrange( widget ):
            return 'break'
        widget.tag_add( mrk, 'insert linestart', 'insert' )
        i = widget.index( 'insert' )
        i1, i2 = i.split( '.' )
        i1 = str( int( i1 ) - 1 )
        widget.mark_set( 'insert', i1+'.'+i2)
        widget.tag_add( mrk, 'insert', 'insert lineend + 1c' )
        if self.inRange( widget, mrk ,l = '-1c', r = '+1c') and widget.index( 'insert' ) != '1.0':
            widget.tag_remove( mrk, 'insert', 'end' )  
        return 'break'
        
    def down( event ):
        widget = event.widget
        if not self.testinrange( widget ):
            return 'break'
        widget.tag_add( mrk, 'insert', 'insert lineend' )
        i = widget.index( 'insert' )
        i1, i2 = i.split( '.' )
        i1 = str( int( i1 ) + 1 )
        widget.mark_set( 'insert', i1 +'.'+i2 )
        widget.tag_add( mrk, 'insert linestart -1c', 'insert' )
        if self.inRange( widget, mrk , l = '-1c', r = '+1c' ): 
            widget.tag_remove( mrk, '1.0', 'insert' )
        return 'break'
        
    extend( event )   
    tbuffer.bind( '&lt;Right&gt;', extend, '+' )
    tbuffer.bind( '&lt;Left&gt;', truncate, '+' )
    tbuffer.bind( '&lt;Up&gt;', up, '+' )
    tbuffer.bind( '&lt;Down&gt;', down, '+' )
    return 'break'
</t>
<t tx="mork.20041030164547.88">def inRange( self, widget, range, l = '', r = '' ):
    ranges = widget.tag_ranges( range )
    #i = widget.index( 'insert' )
    for z in xrange( 0,  len( ranges) , 2 ):
        z1 = z + 1
        l1 = 'insert%s' %l
        r1 = 'insert%s' % r
        if widget.compare( l1, '&gt;=', ranges[ z ]) and widget.compare( r1, '&lt;=', ranges[ z1] ):
            return True
    return False
</t>
<t tx="mork.20041030164547.89">def contRanges( self, widget, range ):
    ranges = widget.tag_ranges( range)
    t1 = widget.get( ranges[ 0 ], ranges[ -1 ] )
    t2 = []
    for z in xrange( 0,  len( ranges) , 2 ):
        z1 = z + 1
        t2.append( widget.get( ranges[ z ], ranges[ z1 ] ) )
    t2 = '\n'.join( t2 )
    return t1 == t2
</t>
<t tx="mork.20041030164547.90">def testinrange( self, widget ):
    mrk = 'sel'
    #ranges = widget.tag_ranges( mrk)
    if not self.inRange( widget , mrk) or not self.contRanges( widget, mrk ):
        self.removeRKeys( widget )
        return False
    return True
</t>
<t tx="mork.20041030164547.91">def killRegion( self, event, which ):
    mrk = 'sel'
    tbuffer = event.widget
    trange = tbuffer.tag_ranges( mrk )
    if len( trange ) != 0:
        txt = tbuffer.get( trange[ 0 ] , trange[ -1 ] )
        if which == 'd':
            tbuffer.delete( trange[ 0 ], trange[ -1 ] )   
        self.addToKillBuffer( txt )
        tbuffer.clipboard_clear()
        tbuffer.clipboard_append( txt )
    self.removeRKeys( tbuffer )
    return 'break'
</t>
<t tx="mork.20041030164547.92">def removeRKeys( self, widget ):
    mrk = 'sel'
    widget.tag_delete( mrk )
    widget.unbind( '&lt;Left&gt;' )
    widget.unbind( '&lt;Right&gt;' )
    widget.unbind( '&lt;Up&gt;' )
    widget.unbind( '&lt;Down&gt;' )
</t>
<t tx="mork.20041030164547.93">def indentRegion( self, event ):
    tbuffer = event.widget
    mrk = 'sel'
    trange = tbuffer.tag_ranges( mrk )
    if len( trange ) != 0:
        ind = tbuffer.search( '\w', '%s linestart' % trange[ 0 ], stopindex = 'end', regexp = True )
        if not ind : return
        text = tbuffer.get( '%s linestart' % ind ,  '%s lineend' % ind)
        sstring = text.lstrip()
        sstring = sstring[ 0 ]
        ws = text.split( sstring )
        if len( ws ) &gt; 1:
            ws = ws[ 0 ]
        else:
            ws = ''
        s , s1 = trange[ 0 ].split( '.' )
        e , e1 = trange[ -1 ].split( '.' )
        s = int( s )
        s = s + 1
        e = int( e ) + 1
        for z in xrange( s , e ):
            t2 = tbuffer.get( '%s.0' %z ,  '%s.0 lineend'%z)
            t2 = t2.lstrip()
            t2 = ws + t2
            tbuffer.delete( '%s.0' % z ,  '%s.0 lineend' %z)
            tbuffer.insert( '%s.0' % z, t2 )
        tbuffer.event_generate( '&lt;Key&gt;' )
        tbuffer.update_idletasks()
    self.removeRKeys( tbuffer )
    return 'break'
</t>
<t tx="mork.20041030164547.94">def tabIndentRegion( self,event ):
    tbuffer = event.widget
    if not self._chckSel( event ):
        return
    i = tbuffer.index( 'sel.first' )
    i2 = tbuffer.index( 'sel.last' )
    i = tbuffer.index( '%s linestart' %i )
    i2 = tbuffer.index( '%s linestart' % i2)
    while 1:
        tbuffer.insert( i, '\t' )
        if i == i2: break
        i = tbuffer.index( '%s + 1 lines' % i )    
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.95">def manufactureKeyPress( self, event, which ):
    tbuffer = event.widget
    tbuffer.event_generate( '&lt;Key&gt;',  keysym = which  )
    tbuffer.update_idletasks()
    return 'break'</t>
<t tx="mork.20041030164547.96">def backToIndentation( self, event ):
    tbuffer = event.widget
    i = tbuffer.index( 'insert linestart' )
    i2 = tbuffer.search( r'\w', i, stopindex = '%s lineend' % i, regexp = True )
    tbuffer.mark_set( 'insert', i2 )
    tbuffer.update_idletasks()
    return 'break'
</t>
<t tx="mork.20041030164547.97">def deleteIndentation( self, event ):
    tbuffer = event.widget
    txt = tbuffer.get( 'insert linestart' , 'insert lineend' )
    txt = ' %s' % txt.lstrip()
    tbuffer.delete( 'insert linestart' , 'insert lineend +1c' )    
    i  = tbuffer.index( 'insert - 1c' )
    tbuffer.insert( 'insert -1c', txt )
    tbuffer.mark_set( 'insert', i )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.98">def deleteNextChar( self,event ):
    tbuffer = event.widget
    i = tbuffer.index( 'insert' )
    tbuffer.delete( i, '%s +1c' % i )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.99">def deleteSpaces( self, event , insertspace = False):
    tbuffer = event.widget
    char = tbuffer.get( 'insert', 'insert + 1c ' )
    if char.isspace():
        i = tbuffer.index( 'insert' )
        wf = tbuffer.search( r'\w', i, stopindex = '%s lineend' % i, regexp = True )
        wb = tbuffer.search( r'\w', i, stopindex = '%s linestart' % i, regexp = True, backwards = True )
        if '' in ( wf, wb ):
            return 'break'
        tbuffer.delete( '%s +1c' %wb, wf )
        if insertspace:
            tbuffer.insert( 'insert', ' ' )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.100">def measure( self, tbuffer ):
    i = tbuffer.index( 'insert' )
    i1, i2 = i.split( '.' )
    start = int( i1 )
    watch = 0
    ustart = start
    pone = 1
    top = i
    bottom = i
    while pone:
        ustart = ustart - 1
        if ustart &lt; 0:
            break
        ds = '%s.0' % ustart
        pone = tbuffer.dlineinfo( ds )
        if pone:
            top = ds
            watch = watch  + 1
    
    pone = 1
    ustart = start
    while pone:
        ustart = ustart +1
        ds = '%s.0' % ustart
        pone = tbuffer.dlineinfo( ds )
        if pone:
            bottom = ds
            watch = watch + 1
            
    return watch , top, bottom
</t>
<t tx="mork.20041030164547.101">def screenscroll( self, event, way = 'north' ):
    tbuffer = event.widget
    chng = self.measure( tbuffer )
    i = tbuffer.index( 'insert' )
    
    if way == 'north':
        #top = chng[ 1 ]
        i1, i2 = i.split( '.' )
        i1 = int( i1 ) - chng[ 0 ]
    else:
        #bottom = chng[ 2 ]
        i1, i2 = i.split( '.' )
        i1 = int( i1 ) + chng[ 0 ]
        
    tbuffer.mark_set( 'insert', '%s.%s' % ( i1, i2 ) )
    tbuffer.see( 'insert' )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.102">def countRegion( self, event ):
    tbuffer = event.widget
    txt = tbuffer.get( 'sel.first', 'sel.last')
    svar = self.svars[ tbuffer ]
    lines = 1
    chars = 0
    for z in txt:
        if z == '\n': lines = lines + 1
        else:
            chars = chars + 1       
    svar.set( 'Region has %s lines, %s characters' %( lines, chars ) )
    return 'break'
</t>
<t tx="mork.20041030164547.103">def insertParentheses( self, event ):
    tbuffer = event.widget
    tbuffer.insert( 'insert', '()' )
    tbuffer.mark_set( 'insert', 'insert -1c' )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.104">#self.qQ = None
#self.qR = None
#self.qlisten = False
#self.lqR = Tkinter.StringVar()
#self.lqR.set( 'Query with: ' )
def listenQR( self, event ):
    #global qgetQuery, qlisten
    #self.qlisten = True
    self.mcStateManager.setState( 'qlisten', 'replace-caption' )
    #tbuffer = event.widget
    svar, label = self.getSvarLabel( event )
    self.setLabelBlue( label )
    if self.querytype == 'regex':
        svar.set( "Regex Query with:" )
    else:
        svar.set( "Query with:" )
    #label.configure( background = 'lightblue' , textvariable = self.lqR)
    self.qgetQuery = True
</t>
<t tx="mork.20041030164547.105">def qsearch( self, event ):
    if self.qQ:
        tbuffer = event.widget
        tbuffer.tag_delete( 'qR' )
        svar, label = self.getSvarLabel( event )
        if self.querytype == 'regex':
            try:
                regex = re.compile( self.qQ )
            except:
                self.keyboardQuit( event )
                svar.set( "Illegal regular expression" )
                
            txt = tbuffer.get( 'insert', 'end' )
            match = regex.search( txt )
            if match:
                start = match.start()
                end = match.end()
                length = end - start
                tbuffer.mark_set( 'insert', 'insert +%sc' % start )
                tbuffer.update_idletasks()
                tbuffer.tag_add( 'qR', 'insert', 'insert +%sc' % length )
                tbuffer.tag_config( 'qR', background = 'lightblue' )
                txt = tbuffer.get( 'insert', 'insert +%sc' % length )
                svar.set( "Replace %s with %s? y/n(! for all )" % ( txt, self.qR ) )
                return True
        else:
            i = tbuffer.search( self.qQ, 'insert', stopindex = 'end' )
            if i:
                tbuffer.mark_set( 'insert', i )
                tbuffer.update_idletasks()
                tbuffer.tag_add( 'qR', 'insert', 'insert +%sc'% len( self.qQ ) )
                tbuffer.tag_config( 'qR', background = 'lightblue' )
                self._tailEnd( tbuffer )
                return True
        self.quitQSearch( event )
        return False

</t>
<t tx="mork.20041030164547.106">def quitQSearch( self,event ):
    #global qQ, qR, qlisten, qrexecute
    event.widget.tag_delete( 'qR' )
    self.qQ = None
    self.qR = None
    #self.qlisten = False
    self.mcStateManager.setState( 'qlisten', False )
    self.qrexecute = False
    svar, label = self.getSvarLabel( event )
    svar.set( '' )
    label.configure( background = 'lightgrey' )
    #self.keyboardQuit( event )
    self.querytype = 'normal'
    self._tailEnd( event.widget )
    #event.widget.event_generate( '&lt;Key&gt;' )
    #event.widget.update_idletasks()
</t>
<t tx="mork.20041030164547.107">def qreplace( self, event ):

    if event.keysym == 'y':
        self._qreplace( event )
        return
    elif event.keysym in ( 'q', 'Return' ):
        self.quitQSearch( event )
    elif event.keysym == 'exclam':
        while self.qrexecute:
            self._qreplace( event )
    elif event.keysym in ( 'n', 'Delete'):
        #i = event.widget.index( 'insert' )
        event.widget.mark_set( 'insert', 'insert +%sc' % len( self.qQ ) )
        self.qsearch( event )
    event.widget.see( 'insert' )
</t>
<t tx="mork.20041030164547.108">def _qreplace( self, event ):
    i = event.widget.tag_ranges( 'qR' )
    event.widget.delete( i[ 0 ], i[ 1 ] )
    event.widget.insert( 'insert', self.qR )
    self.qsearch( event )
</t>
<t tx="mork.20041030164547.109">#self.qgetQuery = False
#self.lqQ = Tkinter.StringVar()
#self.lqQ.set( 'Replace with:' )      
def getQuery( self, event ):
    #global qQ, qgetQuery, qgetReplace
    l = event.keysym
    svar, label = self.getSvarLabel( event )
    label.configure( textvariable = svar )
    if l == 'Return':
        self.qgetQuery = False
        self.qgetReplace = True
        self.qQ = svar.get()
        svar.set( "Replace with:" )
        self.mcStateManager.setState( 'qlisten', 'replace-caption' )
        #label.configure( textvariable = self.lqQ)
        return
    if self.mcStateManager.getState( 'qlisten' ) == 'replace-caption':
        svar.set( '' )
        self.mcStateManager.setState( 'qlisten', True )
    self.setSvar( event, svar )
</t>
<t tx="mork.20041030164547.110">#self.qgetReplace = False
def getReplace( self, event ):
    #global qR, qgetReplace, qrexecute
    l = event.keysym
    svar, label = self.getSvarLabel( event )
    label.configure( textvariable = svar )
    if l == 'Return':
        self.qgetReplace = False
        self.qR = svar.get()
        self.qrexecute = True
        ok = self.qsearch( event )
        if self.querytype == 'regex' and ok:
            tbuffer = event.widget
            range = tbuffer.tag_ranges( 'qR' )
            txt = tbuffer.get( range[ 0 ], range[ 1 ] )
            svar.set( 'Replace %s with %s y/n(! for all )' %( txt, self.qR ) )
        elif ok:
            svar.set( 'Replace %s with %s y/n(! for all )' %( self.qQ, self.qR ) )
        #self.qrexecute = True
        #ok = self.qsearch( event )
        return
    if self.mcStateManager.getState( 'qlisten' ) == 'replace-caption':
        svar.set( '' )
        self.mcStateManager.setState( 'qlisten', True )
    self.setSvar( event, svar )
</t>
<t tx="mork.20041030164547.111">#self.qrexecute = False   
def masterQR( self, event ):

    if self.qgetQuery:
        self.getQuery( event )
    elif self.qgetReplace:
        self.getReplace( event )
    elif self.qrexecute:
        self.qreplace( event )
    else:
        #svar, label = self.getSvarLabel( event )
        #svar.set( '' )
        self.listenQR( event )
    return 'break'
</t>
<t tx="mork.20041030164547.112">def getSvarLabel( self, event ):
    
    '''returns the StringVar and Label( minibuffer ) for a specific Text editor'''
    svar = self.svars[ event.widget ]
    label = self.mbuffers[ event.widget ]
    return svar, label

</t>
<t tx="mork.20041030164547.113">def setSvar( self, event, svar ):
    '''Alters the StringVar svar to represent the change in the event.
       It mimics what would happen with the keyboard and a Text editor
       instead of plain accumalation.''' 
    t = svar.get()  
    if event.char == '\b':
           if len( t ) == 1:
               t = ''
           else:
               t = t[ 0 : -1 ]
           svar.set( t )
    else:
            t = t + event.char
            svar.set( t )
</t>
<t tx="mork.20041030164547.114">def movePastClose( self, event ):
    tbuffer = event.widget
    i = tbuffer.search( '(', 'insert' , backwards = True ,stopindex = '1.0' )
    icheck = tbuffer.search( ')', 'insert',  backwards = True, stopindex = '1.0' )
    if ''  ==  i:
        return 'break'
    if icheck:
        ic = tbuffer.compare( i, '&lt;', icheck )
        if ic: 
            return 'break'
    i2 = tbuffer.search( ')', 'insert' ,stopindex = 'end' )
    i2check = tbuffer.search( '(', 'insert', stopindex = 'end' )
    if '' == i2:
        return 'break'
    if i2check:
        ic2 = tbuffer.compare( i2, '&gt;', i2check )
        if ic2:
            return 'break'
    ib = tbuffer.index( 'insert' )
    tbuffer.mark_set( 'insert', '%s lineend +1c' % i2 )
    if tbuffer.index( 'insert' ) == tbuffer.index( '%s lineend' % ib ):
        tbuffer.insert( 'insert' , '\n')
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.115">#self.rString = False
#self._sString = ''
#self._rpString = ''
def replaceString( self, event ):
    
    svar, label = self.getSvarLabel( event )
    if event.keysym in ( 'Control_L', 'Control_R' ):
        return
    rS = self.mcStateManager.getState( 'rString' )
    regex = self._useRegex
    if not rS:
        #self.rString = 1
        self.mcStateManager.setState( 'rString', 1 )
        self._sString = ''
        self._rpString = ''
        if regex:
            svar.set( 'Replace Regex' )
        else:
            svar.set( 'Replace String' )
        return
    if event.keysym == 'Return':
        #self.rString = self.rString + 1
        rS = rS + 1
        self.mcStateManager.setState( 'rString', rS  )
        #return 'break'
    if rS == 1:
        svar.set( '' )
        #self.rString = self.rString + 1
        rS = rS + 1
        self.mcStateManager.setState( 'rString', rS )
    if rS == 2:
        self.setSvar( event, svar )
        self._sString = svar.get()
        return 'break'
    if rS == 3:
        if regex:
            svar.set( 'Replace regex %s with:' % self._sString )
        else:
            svar.set( 'Replace string %s with:' % self._sString )
        self.mcStateManager.setState( 'rString',rS + 1 )
        #self.rString = self.rString + 1
        return 'break'
    if rS == 4:
        svar.set( '' )
        #self.rString = self.rString + 1
        rS = rS + 1
        self.mcStateManager.setState( 'rString', rS )
    if rS == 5:
        self.setSvar( event, svar )
        self._rpString = svar.get()
        return 'break'
    if rS == 6:
        tbuffer = event.widget
        i = 'insert'
        end = 'end'
        ct = 0
        if tbuffer.tag_ranges( 'sel' ):
            i = tbuffer.index( 'sel.first' )
            end = tbuffer.index( 'sel.last' )
        if regex:
            txt = tbuffer.get( i, end )
            try:
                pattern = re.compile( self._sString )
            except:
                self.keyboardQuit( event )
                svar.set( "Illegal regular expression" )
                return 'break'
            ct = len( pattern.findall( txt ) )
            if ct:
                ntxt = pattern.sub( self._rpString, txt )
                tbuffer.delete( i, end )
                tbuffer.insert( i, ntxt )
        else:
            txt = tbuffer.get( i, end )
            ct = txt.count( self._sString )
            if ct:
                ntxt = txt.replace( self._sString, self._rpString )
                tbuffer.delete( i, end )
                tbuffer.insert( i, ntxt )
                
        svar.set( 'Replaced %s occurances' % ct )
        #label.configure( background = 'lightgrey' )
        self.setLabelGrey( label ) 
        #self.rString = False
        self.mcStateManager.clear()
        self._useRegex = False
        #self.mcStateManager.setState( 'rString', False )
        return self._tailEnd( tbuffer )

</t>
<t tx="mork.20041030164547.116">def swapCharacters( self, event ):
    tbuffer = event.widget
    i = tbuffer.index( 'insert' )
    c1 = tbuffer.get( 'insert', 'insert +1c' )
    c2 = tbuffer.get( 'insert -1c', 'insert' )
    tbuffer.delete( 'insert -1c', 'insert' )
    tbuffer.insert( 'insert', c1 )
    tbuffer.delete( 'insert', 'insert +1c' )
    tbuffer.insert( 'insert', c2 )
    tbuffer.mark_set( 'insert', i )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.117">def insertNewLine( self,event ):
    tbuffer = event.widget
    i = tbuffer.index( 'insert' )
    tbuffer.insert( 'insert', '\n' )
    tbuffer.mark_set( 'insert', i )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.118">def lineNumber( self, event ):
    self.stopControlX( event )
    svar, label = self.getSvarLabel( event )
    tbuffer = event.widget
    i = tbuffer.index( 'insert' )
    i1, i2 = i.split( '.' )
    c = tbuffer.get( 'insert', 'insert + 1c' )
    txt = tbuffer.get( '1.0', 'end' )
    txt2 = tbuffer.get( '1.0', 'insert' )
    perc = len( txt ) * .01
    perc = int( len( txt2 ) / perc )
    svar.set( 'Char: %s point %s of %s(%s%s)  Column %s' %( c, len( txt2), len( txt), perc,'%', i1 ) )
    return 'break'
</t>
<t tx="mork.20041030164547.119">def prevNexSentence( self, event , way ):
    tbuffer = event.widget
    if way == 'bak':
        i = tbuffer.search( '.', 'insert', backwards = True, stopindex = '1.0' )
        if i:
            i2 = tbuffer.search( '.', i, backwards = True, stopindex = '1.0' )
            if not i2:
                i2 = '1.0'
            if i2:
                i3 = tbuffer.search( '\w', i2, stopindex = i, regexp = True )
                if i3:
                    tbuffer.mark_set( 'insert', i3 )
        else:
            tbuffer.mark_set( 'insert', '1.0' )
    else:
        i = tbuffer.search( '.', 'insert', stopindex = 'end' )
        if i:
            tbuffer.mark_set( 'insert', '%s +1c' %i )
        else:
            tbuffer.mark_set( 'insert', 'end' )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.120">def openRectangle( self, event ):
    if not self._chckSel( event ):
        return
    tbuffer = event.widget
    r1, r2, r3, r4 = self.getRectanglePoints( event )
    lth = ' ' * ( r4 - r2 )
    self.stopControlX( event )
    while r1 &lt;= r3:
        tbuffer.insert( '%s.%s' % ( r1, r2 ) , lth)
        r1 = r1 + 1
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.121">def clearRectangle( self, event ):
    if not self._chckSel( event ):
        return
    tbuffer = event.widget
    r1, r2, r3, r4 = self.getRectanglePoints( event )
    lth = ' ' * ( r4 - r2 )
    self.stopControlX( event )
    while r1 &lt;= r3:
        tbuffer.delete( '%s.%s' % ( r1, r2 ) , '%s.%s' % ( r1, r4 )  )
        tbuffer.insert( '%s.%s' % ( r1, r2 ) , lth)
        r1 = r1 + 1
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.122">def deleteRectangle( self, event ):
    if not self._chckSel( event ):
        return
    tbuffer = event.widget
    r1, r2, r3, r4 = self.getRectanglePoints( event )
    #lth = ' ' * ( r4 - r2 )
    self.stopControlX( event )
    while r1 &lt;= r3:
        tbuffer.delete( '%s.%s' % ( r1, r2 ) , '%s.%s' % ( r1, r4 )  )
        r1 = r1 + 1
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.123">#self.sRect = False   
def stringRectangle( self, event ):
    #global sRect
    svar, label = self.getSvarLabel( event )
    if not self.sRect:
        self.sRect = 1
        svar.set( 'String rectangle :' )
        self.setLabelBlue( label )
        return 'break'
    if event.keysym == 'Return':
        self.sRect = 3
    if self.sRect == 1:
        svar.set( '' )
        self.sRect = 2
    if self.sRect == 2:
        self.setSvar( event, svar )
        return 'break'
    if self.sRect == 3:
        if not self._chckSel( event ):
            self.stopControlX( event )
            return
        tbuffer = event.widget
        r1, r2, r3, r4 = self.getRectanglePoints( event )
        lth = svar.get()
        #self.stopControlX( event )
        while r1 &lt;= r3:
            tbuffer.delete( '%s.%s' % ( r1, r2 ),  '%s.%s' % ( r1, r4 ) )
            tbuffer.insert( '%s.%s' % ( r1, r2 ) , lth )
            r1 = r1 + 1
        #i = tbuffer.index( 'insert' )
        #tbuffer.mark_set( 'insert', 'insert wordend' )
        #tbuffer.tag_remove( 'sel', '1.0', 'end' )
        #return self._tailEnd( tbuffer )
        self.stopControlX( event )
        return self._tailEnd( tbuffer )
        #return 'break'
        #return 'break'
        #tbuffer.mark_set( 'insert', i )
        #return 'break'
</t>
<t tx="mork.20041030164547.124">#self.krectangle = None       
def killRectangle( self, event ):
    #global krectangle
    if not self._chckSel( event ):
        return
    tbuffer = event.widget
    r1, r2, r3, r4 = self.getRectanglePoints( event )
    #lth = ' ' * ( r4 - r2 )
    self.stopControlX( event )
    self.krectangle = []
    while r1 &lt;= r3:
        txt = tbuffer.get( '%s.%s' % ( r1, r2 ) , '%s.%s' % ( r1, r4 )  )
        self.krectangle.append( txt )
        tbuffer.delete( '%s.%s' % ( r1, r2 ) , '%s.%s' % ( r1, r4 )  )
        r1 = r1 + 1
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.125">def closeRectangle( self, event ):
    if not self._chckSel( event ):
        return
    tbuffer = event.widget
    r1, r2, r3, r4 = self.getRectanglePoints( event ) 
    ar1 = r1
    txt = []
    while ar1 &lt;= r3:
        txt.append( tbuffer.get( '%s.%s' %( ar1, r2 ), '%s.%s' %( ar1, r4 ) ) )
        ar1 = ar1 + 1 
    for z in txt:
        if z.lstrip().rstrip():
            return
    while r1 &lt;= r3:
        tbuffer.delete( '%s.%s' %(r1, r2 ), '%s.%s' %( r1, r4 ) )
        r1 = r1 + 1
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.126">def yankRectangle( self, event , krec = None ):
    self.stopControlX( event )
    if not krec:
        krec = self.krectangle
    if not krec:
        return 'break'
    tbuffer = event.widget
    txt = tbuffer.get( 'insert linestart', 'insert' )
    txt = self.getWSString( txt )
    i = tbuffer.index( 'insert' )
    i1, i2 = i.split( '.' )
    i1 = int( i1 )
    for z in krec:        
        txt2 = tbuffer.get( '%s.0 linestart' % i1, '%s.%s' % ( i1, i2 ) )
        if len( txt2 ) != len( txt ):
            amount = len( txt ) - len( txt2 )
            z = txt[ -amount : ] + z
        tbuffer.insert( '%s.%s' %( i1, i2 ) , z )
        if tbuffer.index( '%s.0 lineend +1c' % i1 ) == tbuffer.index( 'end' ):
            tbuffer.insert( '%s.0 lineend' % i1, '\n' )
        i1 = i1 + 1
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.127">def getWSString( self, txt ):
    ntxt = []
    for z in txt:
        if z == '\t':
            ntxt.append( z )
        else:
            ntxt.append( ' ' )
    return ''.join( ntxt )
</t>
<t tx="mork.20041030164547.128">def getRectanglePoints( self, event ):
    tbuffer = event.widget
    i = tbuffer.index( 'sel.first' )
    i2 = tbuffer.index( 'sel.last' )
    r1, r2 = i.split( '.' )
    r3, r4 = i2.split( '.' )
    r1 = int( r1 )
    r2 = int( r2 )
    r3 = int( r3 )
    r4 = int( r4 )
    return r1, r2, r3, r4
</t>
<t tx="mork.20041030164547.129">#self.negativeArg = False
def negativeArgument( self, event, stroke = None ):
    #global negativeArg
    svar, label = self.getSvarLabel( event )
    svar.set( "Negative Argument" )
    label.configure( background = 'lightblue' )
    nA = self.mcStateManager.getState( 'negativeArg' )
    if not nA:
        self.mcStateManager.setState( 'negativeArg', True )
        #self.negativeArg = True
    if nA:
        if self.negArgs.has_key( stroke ):
            self.negArgs[ stroke ]( event , stroke)
    return 'break'
</t>
<t tx="mork.20041030164547.130">def changePreviousWord( self, event, stroke ):
    tbuffer = event.widget
    i = tbuffer.index( 'insert' )
    self.moveword( event, -1  )
    if stroke == '&lt;Alt-c&gt;': 
        self.capitalize( event, 'cap' )
    elif stroke =='&lt;Alt-u&gt;':
         self.capitalize( event, 'up' )
    elif stroke == '&lt;Alt-l&gt;': 
        self.capitalize( event, 'low' )
    tbuffer.mark_set( 'insert', i )
    self.stopControlX( event )
    return self._tailEnd( tbuffer )    
</t>
<t tx="mork.20041030164547.131">#self.negArgs = { '&lt;Alt-c&gt;': changePreviousWord,
#'&lt;Alt-u&gt;' : changePreviousWord,
#'&lt;Alt-l&gt;': changePreviousWord }



def insertNewLineIndent( self, event ):
    tbuffer =  event.widget
    txt = tbuffer.get( 'insert linestart', 'insert lineend' )
    txt = self.getWSString( txt )
    i = tbuffer.index( 'insert' )
    tbuffer.insert( i, txt )
    tbuffer.mark_set( 'insert', i )    
    return self.insertNewLine( event )
</t>
<t tx="mork.20041030164547.132">def dynamicExpansion( self, event ):#, store = {'rlist': [], 'stext': ''} ):
    tbuffer = event.widget
    rlist = self.store[ 'rlist' ]
    stext = self.store[ 'stext' ]
    i = tbuffer.index( 'insert -1c wordstart' )
    i2 = tbuffer.index( 'insert -1c wordend' )
    txt = tbuffer.get( i, i2 )
    dA = tbuffer.tag_ranges( 'dA' )
    tbuffer.tag_delete( 'dA' )
    def doDa( txt, from_ = 'insert -1c wordstart', to_ = 'insert -1c wordend' ):

        tbuffer.delete( from_, to_ ) 
        tbuffer.insert( 'insert', txt, 'dA' )
        return self._tailEnd( tbuffer )
        
    if dA:
        dA1, dA2 = dA
        dtext = tbuffer.get( dA1, dA2 )
        if dtext.startswith( stext ) and i2 == dA2: #This seems reasonable, since we cant get a whole word that has the '-' char in it, we do a good guess
            if rlist:
                txt = rlist.pop()
            else:
                txt = stext
                tbuffer.delete( dA1, dA2 )
                dA2 = dA1 #since the text is going to be reread, we dont want to include the last dynamic abbreviation
                self.getDynamicList( tbuffer, txt, rlist )
            return doDa( txt, dA1, dA2 )
        else:
            dA = None
            
    if not dA:
        self.store[ 'stext' ] = txt
        self.store[ 'rlist' ] = rlist = []
        self.getDynamicList( tbuffer, txt, rlist )
        if not rlist:
            return 'break'
        txt = rlist.pop()
        return doDa( txt )
</t>
<t tx="mork.20041030164547.133">def dynamicExpansion2( self, event ):
    tbuffer = event.widget
    i = tbuffer.index( 'insert -1c wordstart' )
    i2 = tbuffer.index( 'insert -1c wordend' )
    txt = tbuffer.get( i, i2 )   
    rlist = []
    self.getDynamicList( tbuffer, txt, rlist )
    dEstring = reduce( self.findPre, rlist )
    if dEstring:
        tbuffer.delete( i , i2 )
        tbuffer.insert( i, dEstring )    
        return self._tailEnd( tbuffer )          
</t>
<t tx="mork.20041030164547.134">def getDynamicList( self, tbuffer, txt , rlist ):

     ttext = tbuffer.get( '1.0', 'end' )
     items = self.dynaregex.findall( ttext ) #make a big list of what we are considering a 'word'
     if items:
         for word in items:
             if not word.startswith( txt ) or word == txt: continue #dont need words that dont match or == the pattern
             if word not in rlist:
                 rlist.append( word )
             else:
                 rlist.remove( word )
                 rlist.append( word )
                 
        


</t>
<t tx="mork.20041030164547.135">def findPre( self, a, b ):
    st = ''
    for z in a:
        st1 = st + z
        if b.startswith( st1 ):
            st = st1
        else:
            return st
    return st  
</t>
<t tx="mork.20041030164547.136">def sortLines( self, event , which = None ):
    tbuffer = event.widget  
    if not self._chckSel( event ):
        return self.keyboardQuit( event )

    i = tbuffer.index( 'sel.first' )
    i2 = tbuffer.index( 'sel.last' )
    is1 = i.split( '.' )
    is2 = i2.split( '.' )
    txt = tbuffer.get( '%s.0' % is1[ 0 ], '%s.0 lineend' % is2[ 0 ] )
    ins = tbuffer.index( 'insert' )
    txt = txt.split( '\n' )
    tbuffer.delete( '%s.0' % is1[ 0 ], '%s.0 lineend' % is2[ 0 ] )
    txt.sort()
    if which:
        txt.reverse()
    inum = int(is1[ 0 ])
    for z in txt:
        tbuffer.insert( '%s.0' % inum, '%s\n' % z ) 
        inum = inum + 1
    tbuffer.mark_set( 'insert', ins )
    self.keyboardQuit( event )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.137">def sortColumns( self, event ):
    tbuffer = event.widget
    if not self._chckSel( event ):
        return self.keyboardQuit( event )
        
    ins = tbuffer.index( 'insert' )
    is1 = tbuffer.index( 'sel.first' )
    is2 = tbuffer.index( 'sel.last' )   
    sint1, sint2 = is1.split( '.' )
    sint2 = int( sint2 )
    sint3, sint4 = is2.split( '.' )
    sint4 = int( sint4 )
    txt = tbuffer.get( '%s.0' % sint1, '%s.0 lineend' % sint3 )
    tbuffer.delete( '%s.0' % sint1, '%s.0 lineend' % sint3 )
    columns = []
    i = int( sint1 )
    i2 = int( sint3 )
    while i &lt;= i2:
        t = tbuffer.get( '%s.%s' %( i, sint2 ), '%s.%s' % ( i, sint4 ) )
        columns.append( t )
        i = i + 1
    txt = txt.split( '\n' )
    zlist = zip( columns, txt )
    zlist.sort()
    i = int( sint1 )      
    for z in xrange( len( zlist ) ):
         tbuffer.insert( '%s.0' % i, '%s\n' % zlist[ z ][ 1 ] ) 
         i = i + 1
    tbuffer.mark_set( 'insert', ins )
    return self._tailEnd( tbuffer ) 

</t>
<t tx="mork.20041030164547.138">def reverseRegion( self, event ):
    tbuffer = event.widget
    if not self._chckSel( event ):
        return
    ins = tbuffer.index( 'insert' )
    is1 = tbuffer.index( 'sel.first' )
    is2 = tbuffer.index( 'sel.last' )    
    txt = tbuffer.get( '%s linestart' % is1, '%s lineend' %is2 )
    tbuffer.delete( '%s linestart' % is1, '%s lineend' %is2  )
    txt = txt.split( '\n' )
    txt.reverse()
    istart = is1.split( '.' )
    istart = int( istart[ 0 ] )
    for z in txt:
        tbuffer.insert( '%s.0' % istart, '%s\n' % z )
        istart = istart + 1
    tbuffer.mark_set( 'insert', ins )
    self.mcStateManager.clear()
    self.resetMiniBuffer( event )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.139">def sortFields( self, event, which = None ):
    tbuffer = event.widget
    if not self._chckSel( event ):
        return self.keyboardQuit( event )

    ins = tbuffer.index( 'insert' )
    is1 = tbuffer.index( 'sel.first' )
    is2 = tbuffer.index( 'sel.last' )
    
    txt = tbuffer.get( '%s linestart' % is1, '%s lineend' % is2 )
    txt = txt.split( '\n' )
    fields = []
    import re
    fn = r'\w+'
    frx = re.compile( fn )
    for z in txt:
        f = frx.findall( z )
        if not which:
            fields.append( f[ 0 ] )
        else:
            i =  int( which )
            if len( f ) &lt; i:
                return self._tailEnd( tbuffer )
            i = i - 1            
            fields.append( f[ i ] )
    nz = zip( fields, txt )
    nz.sort()
    tbuffer.delete( '%s linestart' % is1, '%s lineend' % is2 )
    i = is1.split( '.' )
    #i2 = is2.split( '.' )
    int1 = int( i[ 0 ] )
    for z in nz:
        tbuffer.insert( '%s.0' % int1, '%s\n'% z[1] )
        int1 = int1 + 1
    tbuffer.mark_set( 'insert' , ins )
    return self._tailEnd( tbuffer )

</t>
<t tx="mork.20041030164547.140">#self.altx = False
def alt_X( self, event , which = None):
    #global altx
    if which:
        self.mcStateManager.setState( 'altx', which )
    else:
        self.mcStateManager.setState( 'altx', 'True' )

    svar, label = self.getSvarLabel( event )
    if which:
        svar.set( '%s M-x:' % which )
    else:
        svar.set( 'M-x:' )
    self.setLabelBlue( label )
    return 'break'
</t>
<t tx="mork.20041030164547.141">def doAlt_X( self, event ):
    '''This method executes the correct Alt-X command'''
    svar, label = self.getSvarLabel( event )
    if svar.get().endswith( 'M-x:' ): 
        self.axTabList.clear() #clear the list, new Alt-x command is in effect
        svar.set( '' )
    if event.keysym == 'Return':
        txt = svar.get()
        if self.doAltX.has_key( txt ):
            if txt != 'repeat-complex-command':
                self.altx_history.reverse()
                self.altx_history.append( txt )
                self.altx_history.reverse()
            aX = self.mcStateManager.getState( 'altx' )
            if aX.isdigit() and txt in self.x_hasNumeric:
                self.doAltX[ txt]( event, aX )
            else:
                self.doAltX[ txt ]( event )
        else:
            self.keyboardQuit( event )
            svar.set('Command does not exist' )

        #self.altx = False
        #self.mcStateManager.setState( 'altx', False )
        return 'break'
    if event.keysym == 'Tab':
        
        stext = svar.get().strip()
        if self.axTabList.prefix and stext.startswith( self.axTabList.prefix ):
            svar.set( self.axTabList.next() ) #get next in iteration
        else:
            prefix = svar.get()
            pmatches = self._findMatch2( svar )
            self.axTabList.setTabList( prefix, pmatches )
            svar.set( self.axTabList.next() ) #begin iteration on new lsit
        return 'break'   
    else:
        self.axTabList.clear() #clear the list, any other character besides tab indicates that a new prefix is in effect.    
    self.setSvar( event, svar )
    return 'break'
</t>
<t tx="mork.20041030164547.142">def _findMatch2( self, svar, fdict = None ):#, fdict = self.doAltX ):
    '''This method returns a sorted list of matches.'''
    if not fdict:
        fdict = self.doAltX
    txt = svar.get()
    if not txt.isspace() and txt != '':
        txt = txt.strip()
        pmatches = filter( lambda a : a.startswith( txt ), fdict )
    else:
        pmatches = []
    pmatches.sort()
    return pmatches
    #if pmatches:
    #    #mstring = reduce( self.findPre, pmatches )
    #    #return mstring
    #return txt
</t>
<t tx="mork.20041030164547.143">#self.uC = False
def universalDispatch( self, event, stroke ):
    #global uC    
    uC = self.mcStateManager.getState( 'uC' )
    if not uC:
        #self.uC = 1
        self.mcStateManager.setState( 'uC', 1 )
        svar, label = self.getSvarLabel( event )
        svar.set( '' )
        self.setLabelBlue( label ) 
    elif uC == 1:
        self.universalCommand1( event, stroke )
    elif uC == 2:
        self.universalCommand3( event, stroke )
    return 'break'
</t>
<t tx="mork.20041030164547.144">#import string
#self.uCstring = string.digits + '\b'

def universalCommand1( self, event, stroke ):
    #global uC
    if event.char not in self.uCstring:
        return self.universalCommand2( event, stroke )
    svar, label = self.getSvarLabel( event )
    self.setSvar( event, svar )
    if event.char != '\b':
        svar.set( '%s ' %svar.get() )
</t>
<t tx="mork.20041030164547.145">def universalCommand2(  self, event , stroke ):
    #global uC
    #self.uC = False
    #self.mcStateManager.setState( 'uC', False )
    svar, label = self.getSvarLabel( event )
    txt = svar.get()
    self.keyboardQuit( event )
    txt = txt.replace( ' ', '' )
    self.resetMiniBuffer( event )
    if not txt.isdigit(): #This takes us to macro state.  For example Control-u Control-x (  will execute the last macro and begin editing of it.
        if stroke == '&lt;Control-x&gt;':
            #self.uC = 2
            self.mcStateManager.setState( 'uC', 2 )
            return self.universalCommand3( event, stroke )
        return self._tailEnd( event.widget )
    if self.uCdict.has_key( stroke ): #This executes the keystroke 'n' number of times.
            self.uCdict[ stroke ]( event , txt )
    else:
        tbuffer = event.widget
        i = int( txt )
        stroke = stroke.lstrip( '&lt;' ).rstrip( '&gt;' )
        if self.cbDict.has_key( stroke ):
            for z in xrange( i ):
                method = self.cbDict[ stroke ]
                ev = Tkinter.Event()
                ev.widget = event.widget
                ev.keysym = event.keysym
                ev.keycode = event.keycode
                ev.char = event.char
                self.masterCommand( ev , method, '&lt;%s&gt;' % stroke )
        else:
            for z in xrange( i ):
                tbuffer.event_generate( '&lt;Key&gt;', keycode = event.keycode, keysym = event.keysym )
                self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.146">#self.uCdict = { '&lt;Alt-x&gt;' : alt_X }
def universalCommand3( self, event, stroke ):
    svar, label = self.getSvarLabel( event )
    svar.set( 'Control-u %s' % stroke.lstrip( '&lt;' ).rstrip( '&gt;' ) )
    self.setLabelBlue( label )
    if event.keysym == 'parenleft':
        self.keyboardQuit( event )
        self.startKBDMacro( event )
        self.executeLastMacro( event )
        return 'break'
</t>
<t tx="mork.20041030164547.147">def numberCommand( self, event, stroke, number ):
    self.universalDispatch( event, stroke )
    tbuffer = event.widget
    tbuffer.event_generate( '&lt;Key&gt;', keysym = number )
    return 'break'       
</t>
<t tx="mork.20041030164547.148">def transposeLines( self, event ):
    tbuffer = event.widget
    i = tbuffer.index( 'insert' )
    i1, i2 = i.split( '.' )
    i1 = str( int( i1 ) -1 )
    if i1 != '0':
        l2 = tbuffer.get( 'insert linestart', 'insert lineend' )
        tbuffer.delete( 'insert linestart-1c', 'insert lineend' )
        tbuffer.insert( i1+'.0', l2 +'\n')
    else:
        l2 = tbuffer.get( '2.0', '2.0 lineend' )
        tbuffer.delete( '2.0', '2.0 lineend' )
        tbuffer.insert( '1.0', l2 + '\n' )
    return self._tailEnd( tbuffer )         
</t>
<t tx="mork.20041030164547.149">def upperLowerRegion( self, event, way ):
    tbuffer = event.widget
    mrk = 'sel'
    trange = tbuffer.tag_ranges( mrk )
    if len( trange ) != 0:
        text = tbuffer.get( trange[ 0 ] , trange[ -1 ] )
        i = tbuffer.index( 'insert' )
        if text == ' ': return 'break'
        tbuffer.delete( trange[ 0 ], trange[ -1 ] )
        if way == 'low':
            text = text.lower()
        if way == 'up':
            text = text.upper()
        tbuffer.insert( 'insert', text )
        tbuffer.mark_set( 'insert', i ) 
    self.removeRKeys( tbuffer )
    return 'break'
</t>
<t tx="mork.20041030164547.150">def removeBlankLines (self,event):
    tbuffer = event.widget
    i = tbuffer.index('insert')
    i1, i2 = i.split('.')
    i1 = int(i1)
    dindex = []
    if tbuffer.get('insert linestart','insert lineend').strip() == '':
        while 1:
            if str(i1) + '.0' == '1.0':
                break
            i1 = i1-1
            txt = tbuffer.get('%s.0' % i1,'%s.0 lineend' % i1)
            txt = txt.strip()
            if len(txt) == 0:
                dindex.append('%s.0' % i1)
                dindex.append('%s.0 lineend' % i1)
            elif dindex:
                tbuffer.delete('%s-1c' % dindex[-2],dindex[1])
                tbuffer.event_generate('&lt;Key&gt;')
                tbuffer.update_idletasks()
                break
            else:
                break
    i = tbuffer.index('insert')
    i1, i2 = i.split('.')
    i1 = int(i1)
    dindex = []
    while 1:
        if tbuffer.index('%s.0 lineend' % i1) == tbuffer.index('end'):
            break
        i1 = i1 + 1
        txt = tbuffer.get('%s.0' % i1,'%s.0 lineend' % i1)
        txt = txt.strip()
        if len(txt) == 0:
            dindex.append('%s.0' % i1)
            dindex.append('%s.0 lineend' % i1)
        elif dindex:
            tbuffer.delete('%s-1c' % dindex[0],dindex[-1])
            tbuffer.event_generate('&lt;Key&gt;')
            tbuffer.update_idletasks()
            break
        else:
            break</t>
<t tx="mork.20041030164547.151">def insertFile( self, event ):
    tbuffer = event.widget
    f, name = self.getReadableTextFile()
    if not f: return None
    txt = f.read()
    f.close()
    tbuffer.insert( 'insert', txt )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041030164547.152">def saveFile( self, event ):
    tbuffer = event.widget
    import tkFileDialog
    txt = tbuffer.get( '1.0', 'end' )
    f = tkFileDialog.asksaveasfile()
    if f == None : return None
    f.write( txt )
    f.close()
</t>
<t tx="mork.20041030164547.153">def scolorizer( self, event ):

    tbuffer = event.widget
    svar, label = self.getSvarLabel( event )
    stext = svar.get()
    tbuffer.tag_delete( 'color' )
    tbuffer.tag_delete( 'color1' )
    if stext == '': return 'break'
    ind = '1.0'
    while ind:
        try:
            ind = tbuffer.search( stext, ind, stopindex = 'end', regexp = self.useRegex() )
        except:
            break
        if ind:
            i, d = ind.split('.')
            d = str(int( d ) + len( stext ))
            index = tbuffer.index( 'insert' )
            if ind == index:
                tbuffer.tag_add( 'color1', ind, '%s.%s' % (i,d) )
            tbuffer.tag_add( 'color', ind, '%s.%s' % (i, d) )
            ind = i +'.'+d
    tbuffer.tag_config( 'color', foreground = 'red' ) 
    tbuffer.tag_config( 'color1', background = 'lightblue' ) 
</t>
<t tx="mork.20041030164547.154">def startGoto( self, event , ch = False):
    #global goto
    #self.goto = True
    if not ch:
        self.mcStateManager.setState( 'goto', 1 )
    else:
        self.mcStateManager.setState( 'goto', 2 )
    #label = self.mbuffers[ event.widget ] 
    svar , label = self.getSvarLabel( event )
    svar.set( '' )
    label.configure( background = 'lightblue' )
    return 'break'
</t>
<t tx="mork.20041030164547.155">def Goto( self, event ):
    #global goto
    widget = event.widget
    svar, label = self.getSvarLabel( event )
    if event.keysym == 'Return':
          i = svar.get()
          self.resetMiniBuffer( event )
          #self.goto = False
          state = self.mcStateManager.getState( 'goto' )
          self.mcStateManager.setState( 'goto', False )
          if i.isdigit():
              
              if state == 1:
                widget.mark_set( 'insert', '%s.0' % i )
              elif state == 2:
                widget.mark_set( 'insert', '1.0 +%sc' % i )
              widget.event_generate( '&lt;Key&gt;' )
              widget.update_idletasks()
              widget.see( 'insert' )
          return 'break'
    t = svar.get()
    if event.char == '\b':
           if len( t ) == 1:
               t = ''
           else:
               t = t[ 0 : -1 ]
           svar.set( t )
    else:
            t = t + event.char
            svar.set( t )
    return 'break'
</t>
<t tx="mork.20041030165020">class Emacs:
    '''The Emacs class binds to a Tkinter Text widget and adds Emac derived keystrokes and commands
       to it.'''
    
    Emacs_instances = weakref.WeakKeyDictionary()
    global_killbuffer = []
    global_registers = {}
    lossage = [] ### EKR: list( ' ' * 100 )
    @others</t>
<t tx="mork.20041030165020.1">def __init__( self , tbuffer = None , minibuffer = None, useGlobalKillbuffer = False, useGlobalRegisters = False):
    '''Sets up Emacs instance.
    
    If a Tkinter Text widget and Tkinter Label are passed in
    via the tbuffer and minibuffer parameters, these are bound to.
    Otherwise an explicit call to setBufferStrokes must be done.
    useGlobalRegisters set to True indicates that the Emacs instance should use a class attribute that functions
    as a global register.
    useGlobalKillbuffer set to True indicates that the Emacs instances should use a class attribute that functions
    as a global killbuffer.'''
    
    self.mbuffers = {} 
    self.svars = {}
    
    
    #self.isearch = False
    self.tailEnds = {} #functions to execute at the end of many Emac methods.  Configurable by environment.
    self.undoers = {} #Emacs instance tracks undoers given to it.
    
    
    self.store = {'rlist': [], 'stext': ''} 
    
    #macros
    self.lastMacro = None 
    self.macs = []
    self.macro = []
    self.namedMacros = {}
    self.macroing = False
    self.dynaregex = re.compile( r'[%s%s\-_]+' %( string.ascii_letters, string.digits ) ) #for dynamic abbreviations
    self.altx_history = []
    self.keysymhistory = [] 
    
    #This section sets up the buffer data structures
    self.bufferListGetters = {}
    self.bufferSetters = {}
    self.bufferGotos = {}
    self.bufferDeletes = {}
    self.renameBuffers = {}
    self.bufferDict = None
    self.bufferTracker = Tracker()
    self.bufferCommands = {
    
    'append-to-buffer': self.appendToBuffer,
    'prepend-to-buffer': self.prependToBuffer,
    'copy-to-buffer': self.copyToBuffer,
    'insert-buffer': self.insertToBuffer,
    'switch-to-buffer': self.switchToBuffer,
     'kill-buffer': self.killBuffer,   
    }
    
    self.swapSpots = []
    self.ccolumn = '0'
    #self.howM = False
    self.reset = False
    if useGlobalKillbuffer:
        self.killbuffer = Emacs.global_killbuffer
    else:
        self.killbuffer = []
    self.kbiterator = self.iterateKillBuffer()
    
    #self.controlx = False
    self.csr = { '&lt;Control-s&gt;': 'for', '&lt;Control-r&gt;':'bak' }
    self.pref = None
    #self.zap = False
    #self.goto = False
    self.previousStroke = ''
    if useGlobalRegisters:
        self.registers = Emacs.global_registers
    else:
        self.registers = {}
    
    #registers
    self.regMeth = None
    self.regMeths, self.regText = self.addRegisterItems()

    #Abbreviations
    self.abbrevMode = False 
    self.abbrevOn = False # determines if abbreviations are on for masterCommand and toggle abbreviations
    self.abbrevs = {}
    
    self.regXRpl = None # EKR: a generator: calling self.regXRpl.next() get the next value.
    self.regXKey = None
    
    self.fillPrefix = '' #for fill prefix functions
    self.fillColumn = 70 #for line centering
    self.registermode = False #for rectangles and registers
    
    self.qQ = None
    self.qR = None
    #self.qlisten = False
    #self.lqR = Tkinter.StringVar()
    #self.lqR.set( 'Query with: ' ) # replaced with using the svar and self.mcStateManager
    self.qgetQuery = False
    #self.lqQ = Tkinter.StringVar()
    #self.lqQ.set( 'Replace with:' )# replaced with using the svar and self.mcStateManager
    self.qgetReplace = False
    self.qrexecute = False
    self.querytype = 'normal'
    
    #self.rString = False
    #These attributes are for replace-string and replace-regex
    self._sString = ''
    self._rpString = ''
    self._useRegex = False
    
    self.sRect = False  #State indicating string rectangle.  May be moved to MC_StateManager
    self.krectangle = None #The kill rectangle
    self.rectanglemode = 0 #Determines what state the rectangle system is in.
    
    self.last_clipboard = None #For interacting with system clipboard.
    
    self.negativeArg = False 
    self.negArgs = { '&lt;Alt-c&gt;': self.changePreviousWord,
    '&lt;Alt-u&gt;' : self.changePreviousWord,
    '&lt;Alt-l&gt;': self.changePreviousWord } #For negative argument functionality
    
    #self.altx = False
    #Alt-X commands.
    self.doAltX = self.addAltXCommands()
    self.axTabList = Tracker()
    self.x_hasNumeric = [ 'sort-lines' , 'sort-fields']
    
    #self.uC = False
    #These attributes are for the universal command functionality.
    self.uCstring = string.digits + '\b'
    self.uCdict = { '&lt;Alt-x&gt;' : self.alt_X }
    
    self.cbDict = self.addCallBackDict()# Creates callback dictionary, primarily used in the master command
    self.xcommands = self.addXCommands() # Creates the X commands dictionary
    self.cxHandler = ControlXHandler( self ) #Creates the handler for Control-x commands
    self.mcStateManager = MC_StateManager( self ) #Manages state for the master command
    self.kstrokeManager = MC_KeyStrokeManager( self ) #Manages some keystroke state for the master command.
    self.shutdownhook = None #If this is set via setShutdownHook, it is executed instead of sys.exit when Control-x Control-c is fired
    self.shuttingdown = False #indicates that the Emacs instance is shutting down and no work needs to be done.
    
    if tbuffer and minibuffer:
        self.setBufferStrokes( tbuffer, minibuffer )

</t>
<t tx="mork.20041030183331">def addCallBackDict( self ):
    '''This method adds a dictionary to the Emacs instance through which the masterCommand can
       call the specified method.'''
    cbDict = {
    'Alt-less' : lambda event, spot = '1.0' : self.moveTo( event, spot ),
    'Alt-greater': lambda event, spot = 'end' : self.moveTo( event, spot ),
    'Control-Right': lambda event, way = 1: self.moveword( event, way ),
    'Control-Left': lambda event, way = -1: self.moveword( event, way ),
    'Control-a': lambda event, spot = 'insert linestart': self.moveTo( event, spot ),
    'Control-e': lambda event, spot = 'insert lineend': self.moveTo( event, spot ),
    'Alt-Up': lambda event, spot = 'insert linestart': self.moveTo( event, spot ),
    'Alt-Down': lambda event, spot = 'insert lineend': self.moveTo( event, spot ),
    'Alt-f': lambda event, way = 1: self.moveword( event, way ),
    'Alt-b' : lambda event, way = -1: self.moveword( event, way ),
    'Control-o': self.insertNewLine,
    'Control-k': lambda event, frm = 'insert', to = 'insert lineend': self.kill( event, frm, to) ,
    'Alt-d': lambda event, frm = 'insert wordstart', to = 'insert wordend': self.kill( event,frm, to ),
    'Alt-Delete': lambda event: self.deletelastWord( event ),
    "Control-y": lambda event, frm = 'insert', which = 'c': self.walkKB( event, frm, which),
    "Alt-y": lambda event , frm = "insert", which = 'a': self.walkKB( event, frm, which ),
    "Alt-k": lambda event : self.killsentence( event ),
    'Control-s' : None,
    'Control-r' : None,
    'Alt-c': lambda event, which = 'cap' : self.capitalize( event, which ),
    'Alt-u': lambda event, which = 'up' : self.capitalize( event, which ),
    'Alt-l': lambda event, which = 'low' : self.capitalize( event, which ),
    'Alt-t': lambda event, sw = self.swapSpots: self.swapWords( event, sw ),
    'Alt-x': self.alt_X,
    'Control-x': self.startControlX,
    'Control-g': self.keyboardQuit,
    'Control-Shift-at': self.setRegion,
    'Control-w': lambda event, which = 'd' :self.killRegion( event, which ),
    'Alt-w': lambda event, which = 'c' : self.killRegion( event, which ),
    'Control-t': self.swapCharacters,
    'Control-u': None,
    'Control-l': None,
    'Alt-z': None,
    'Control-i': None,
    'Alt-Control-backslash': self.indentRegion,
    'Alt-m' : self.backToIndentation,
    'Alt-asciicircum' : self.deleteIndentation,
    'Control-d': self.deleteNextChar,
    'Alt-backslash': self.deleteSpaces, 
    'Alt-g': None,
    'Control-v' : lambda event, way = 'south': self.screenscroll( event, way ),
    'Alt-v' : lambda event, way = 'north' : self.screenscroll( event, way ),
    'Alt-equal': self.countRegion,
    'Alt-parenleft': self.insertParentheses,
    'Alt-parenright': self.movePastClose,
    'Alt-percent' : None,
    'Control-c': None,
    'Delete': lambda event, which = 'BackSpace': self.manufactureKeyPress( event, which ),
    'Control-p': lambda event, which = 'Up': self.manufactureKeyPress( event, which ),
    'Control-n': lambda event, which = 'Down': self.manufactureKeyPress( event, which ),
    'Control-f': lambda event, which = 'Right':self.manufactureKeyPress( event, which ),
    'Control-b': lambda event, which = 'Left': self.manufactureKeyPress( event, which ),
    'Control-Alt-w': None,
    'Alt-a': lambda event, which = 'bak': self.prevNexSentence( event, which ),
    'Alt-e': lambda event, which = 'for': self.prevNexSentence( event, which ),
    'Control-Alt-o': self.insertNewLineIndent,
    'Control-j': self.insertNewLineAndTab,
    'Alt-minus': self.negativeArgument,
    'Alt-slash': self.dynamicExpansion,
    'Control-Alt-slash': self.dynamicExpansion2,
    'Control-u': lambda event, keystroke = '&lt;Control-u&gt;': self.universalDispatch( event, keystroke ),
    'Alt-braceright': lambda event, which = 1: self.movingParagraphs( event, which ),
    'Alt-braceleft': lambda event , which = 0: self.movingParagraphs( event, which ),
    'Alt-q': self.fillParagraph,
    'Alt-h': self.selectParagraph,
    'Alt-semicolon': self.indentToCommentColumn,
    'Alt-0': lambda event, stroke = '&lt;Alt-0&gt;', number = 0: self.numberCommand( event, stroke, number ) ,
    'Alt-1': lambda event, stroke = '&lt;Alt-1&gt;', number = 1: self.numberCommand( event, stroke, number ) ,
    'Alt-2': lambda event, stroke = '&lt;Alt-2&gt;', number = 2: self.numberCommand( event, stroke, number ) ,
    'Alt-3': lambda event, stroke = '&lt;Alt-3&gt;', number = 3: self.numberCommand( event, stroke, number ) ,
    'Alt-4': lambda event, stroke = '&lt;Alt-4&gt;', number = 4: self.numberCommand( event, stroke, number ) ,
    'Alt-5': lambda event, stroke = '&lt;Alt-5&gt;', number = 5: self.numberCommand( event, stroke, number ) ,
    'Alt-6': lambda event, stroke = '&lt;Alt-6&gt;', number = 6: self.numberCommand( event, stroke, number ) ,
    'Alt-7': lambda event, stroke = '&lt;Alt-7&gt;', number = 7: self.numberCommand( event, stroke, number ) ,
    'Alt-8': lambda event, stroke = '&lt;Alt-8&gt;', number = 8: self.numberCommand( event, stroke, number ) ,
    'Alt-9': lambda event, stroke = '&lt;Alt-9&gt;', number = 9: self.numberCommand( event, stroke, number ) ,
    'Control-underscore': self.doUndo,
    'Alt-s': self.centerLine,
    'Control-z': self.suspend, 
    'Control-Alt-s': lambda event, stroke='&lt;Control-s&gt;': self.startIncremental( event, stroke, which='regexp' ),
    'Control-Alt-r': lambda event, stroke='&lt;Control-r&gt;': self.startIncremental( event, stroke, which='regexp' ),
    'Control-Alt-percent': lambda event: self.startRegexReplace() and self.masterQR( event ),
    'Escape': self.watchEscape,
    'Alt-colon': self.startEvaluate,
    'Alt-exclam': self.startSubprocess,
    'Alt-bar': lambda event: self.startSubprocess( event, which = 1 ),
    }
    
    return cbDict</t>
<t tx="mork.20041030183633">def addXCommands( self ):
    
    xcommands = {
    '&lt;Control-t&gt;': self.transposeLines, 
    '&lt;Control-u&gt;': lambda event , way ='up': self.upperLowerRegion( event, way ),
    '&lt;Control-l&gt;':  lambda event , way ='low': self.upperLowerRegion( event, way ),
    '&lt;Control-o&gt;': self.removeBlankLines,
    '&lt;Control-i&gt;': self.insertFile,
    '&lt;Control-s&gt;': self.saveFile,
    '&lt;Control-x&gt;': self.exchangePointMark,
    '&lt;Control-c&gt;': self.shutdown,
    '&lt;Control-b&gt;': self.listBuffers,
    '&lt;Control-Shift-at&gt;': lambda event: event.widget.selection_clear(),
    '&lt;Delete&gt;' : lambda event, back = True: self.killsentence( event, back ),
    }
    
    return xcommands</t>
<t tx="mork.20041030190729">def addRegisterItems( self ):
    
    regMeths = {
    's' : self.copyToRegister,
    'i' : self.insertFromRegister,
    'n': self.numberToRegister,
    'plus': self.incrementRegister,
    'space': self.pointToRegister,
    'j': self.jumpToRegister,
    'a': lambda event , which = 'a': self._ToReg( event, which ),
    'p': lambda event , which = 'p': self._ToReg( event, which ),
    'r': self.copyRectangleToRegister,
    'view' : self.viewRegister,
    }    
    
    regText = {
    's' : 'copy to register',
    'i' : 'insert from register',
    'plus': 'increment register',
    'n' : 'number to register',
    'p' : 'prepend to register',
    'a' : 'append to register',
    'space' : 'point to register',
    'j': 'jump to register',
    'r': 'rectangle to register',
    'view': 'view register',
    }
    
    return regMeths, regText</t>
<t tx="mork.20041030190903">def addAltXCommands( self ):
    
    #many of the simpler methods need self.keyboardQuit( event ) appended to the end to stop the Alt-x mode.
    doAltX= {
    'prepend-to-register': self.prependToRegister,
    'append-to-register': self.appendToRegister,
    'replace-string': self.replaceString,
    'replace-regex': lambda event:  self.activateReplaceRegex() and self.replaceString( event ),
    'sort-lines': self.sortLines,
    'sort-columns': self.sortColumns,
    'reverse-region': self.reverseRegion,
    'sort-fields': self.sortFields,
    'abbrev-mode': self.toggleAbbrevMode,
    'kill-all-abbrevs': self.killAllAbbrevs,
    'expand-region-abbrevs': self.regionalExpandAbbrev,
    'write-abbrev-file': self.writeAbbreviations,
    'read-abbrev-file': self.readAbbreviations,
    'fill-region-as-paragraph': self.fillRegionAsParagraph,
    'fill-region': self.fillRegion,
    'close-rectangle': self.closeRectangle,
    'how-many': self.startHowMany,
    'kill-paragraph': self.killParagraph,
    'backward-kill-paragraph': self.backwardKillParagraph,
    'backward-kill-sentence': lambda event: self.keyboardQuit( event ) and self.killsentence( event, back = True ),
    'name-last-kbd-macro': self.nameLastMacro,
    'load-file': self.loadMacros,
    'insert-keyboard-macro' : self.getMacroName,
    'list-abbrevs': self.listAbbrevs,
    'kill-word': lambda event, frm = 'insert wordstart', to = 'insert wordend': self.kill( event,frm, to ) and self.keyboardQuit( event ),
    'kill-line': lambda event, frm = 'insert', to = 'insert lineend': self.kill( event, frm, to) and self.keyboardQuit( event ), 
    'kill-sentence': lambda event : self.killsentence( event ) and self.keyboardQuit( event ),
    'kill-region': lambda event, which = 'd' :self.killRegion( event, which ) and self.keyboardQuit( event ),
    'yank': lambda event, frm = 'insert', which = 'c': self.walkKB( event, frm, which) and self.keyboardQuit( event ),
    'yank-pop' : lambda event , frm = "insert", which = 'a': self.walkKB( event, frm, which ) and self.keyboardQuit( event ),
    'backward-kill-word': lambda event: self.deletelastWord( event ) and self.keyboardQuit( event ),
    'backward-delete-char':lambda event, which = 'BackSpace': self.manufactureKeyPress( event, which ) and self.keyboardQuit( event ),
    'delete-char': lambda event: self.deleteNextChar( event ) and self.keyboardQuit( event ) , 
    'isearch-forward': lambda event: self.keyboardQuit( event ) and self.startIncremental( event, '&lt;Control-s&gt;' ),
    'isearch-backward': lambda event: self.keyboardQuit( event ) and self.startIncremental( event, '&lt;Control-r&gt;' ),
    'isearch-forward-regexp': lambda event: self.keyboardQuit( event ) and self.startIncremental( event, '&lt;Control-s&gt;', which = 'regexp' ),
    'isearch-backward-regexp': lambda event: self.keyboardQuit( event ) and self.startIncremental( event, '&lt;Control-r&gt;', which = 'regexp' ),
    'capitalize-word': lambda event, which = 'cap' : self.capitalize( event, which ) and self.keyboardQuit( event ),
    'upcase-word': lambda event, which = 'up' : self.capitalize( event, which ) and self.keyboardQuit( event ),
    'downcase-word': lambda event, which = 'low' : self.capitalize( event, which ) and self.keyboardQuit( event ),
    'indent-region': lambda event: self.indentRegion( event ) and self.keyboardQuit( event ),
    'indent-rigidly': lambda event: self.tabIndentRegion( event ) and self.keyboardQuit( event ),
    'indent-relative': self.indent_relative,
    'set-mark-command': lambda event: self.setRegion( event ) and self.keyboardQuit( event ),
    'kill-rectangle': lambda event: self.killRectangle( event ),
    'delete-rectangle': lambda event: self.deleteRectangle( event ),
    'yank-rectangle': lambda event: self.yankRectangle( event ),
    'open-rectangle': lambda event: self.openRectangle( event ),
    'clear-rectangle': lambda event: self.clearRectangle( event ),
    'copy-to-register': lambda event: self.setEvent( event, 's' ) and self.setNextRegister( event ),
    'insert-register': lambda event: self.setEvent( event, 'i' ) and self.setNextRegister( event ),
    'copy-rectangle-to-register': lambda event: self.setEvent( event, 'r' ) and self.setNextRegister( event ),
    'jump-to-register': lambda event: self.setEvent( event, 'j' ) and self.setNextRegister( event ),
    'point-to-register': lambda event: self.setEvent( event, 'space' ) and self.setNextRegister( event ),
    'number-to-register': lambda event: self.setEvent( event, 'n' ) and self.setNextRegister( event ),
    'increment-register': lambda event: self.setEvent( event, 'plus' ) and self.setNextRegister( event ),
    'view-register': lambda event: self.setEvent( event, 'view' ) and self.setNextRegister( event ),
    'beginning-of-line': lambda event, spot = 'insert linestart': self.moveTo( event, spot ) and self.keyboardQuit( event ),
    'end-of-line': lambda event, spot = 'insert lineend': self.moveTo( event, spot ) and self.keyboardQuit( event ),
    'keyboard-quit': lambda event: self.keyboardQuit( event ),
    'advertised-undo': lambda event: self.doUndo( event ) and self.keyboardQuit( event ),
    'back-to-indentation': lambda event: self.backToIndentation( event ) and self.keyboardQuit( event ),
    'delete-indentation': lambda event: self.deleteIndentation( event ) and self.keyboardQuit( event ),    
    'view-lossage': lambda event: self.viewLossage( event ),
     'transpose-chars': lambda event : self.swapCharacters( event ) and self.keyboardQuit( event ),
     'transpose-words': lambda event, sw = self.swapSpots: self.swapWords( event, sw ) and self.keyboardQuit( event ),
     'transpose-lines': lambda event: self.transposeLines( event ) and self.keyboardQuit( event ),
     'insert-file' : lambda event: self.insertFile( event ) and self.keyboardQuit( event ),
     'save-buffer' : lambda event: self.saveFile( event ) and self.keyboardQuit( event ),
     'split-line' : lambda event: self.insertNewLineIndent( event ) and self.keyboardQuit( event ),
     'upcase-region': lambda event: self.upperLowerRegion( event, 'up' ) and self.keyboardQuit( event ),
     'downcase-region': lambda event: self.upperLowerRegion( event , 'low' ) and self.keyboardQuit( event ),
     'dabbrev-expands': lambda event: self.dynamicExpansion( event ) and self.keyboardQuit( event ),
     'dabbrev-completion': lambda event: self.dynamicExpansion2( event ) and self.keyboardQuit( event ),
     'goto-line': lambda event: self.startGoto( event ),
     'goto-char': lambda event: self.startGoto( event, True ),
     'set-fill-prefix': lambda event: self.setFillPrefix( event ) and self.keyboardQuit( event ),
     'set-fill-column': lambda event: self.setFillColumn( event ),
     'center-line': lambda event: self.centerLine( event ) and self.keyboardQuit( event ),
     'center-region': lambda event: self.centerRegion( event ) and self.keyboardQuit( event ),
     'forward-char': lambda event, which = 'Right': self.keyboardQuit( event ) and self.manufactureKeyPress( event, which ),
     'backward-char': lambda event, which = 'Left': self.keyboardQuit( event ) and self.manufactureKeyPress( event, which ),
     'previous-line': lambda event, which = 'Up': self.keyboardQuit( event ) and self.manufactureKeyPress( event, which ),
     'next-line': lambda event, which = 'Down': self.keyboardQuit( event ) and self.manufactureKeyPress( event, which ),
     'digit-argument': lambda event: self.universalDispatch( event, '' ),
     'universal-argument': lambda event: self.universalDispatch( event, '' ),   
     'newline-and-indent': lambda event: self.insertNewLineAndTab( event ) and self.keyboardQuit( event ),
     'beginning-of-buffer': lambda event, spot = '1.0' : self.moveTo( event, spot ) and self.keyboardQuit( event ),
     'end-of-buffer': lambda event, spot = 'end' : self.moveTo( event, spot ) and self.keyboardQuit( event ),
     'scroll-up': lambda event, way = 'north' : self.screenscroll( event, way ) and self.keyboardQuit( event ),
     'scroll-down': lambda event, way = 'south': self.screenscroll( event, way ) and self.keyboardQuit( event ),
     'copy-to-buffer': lambda event, which = 'copy-to-buffer': self.setInBufferMode( event, which ),
     'insert-buffer': lambda event, which = 'insert-buffer': self.setInBufferMode( event, which ),
     'append-to-buffer': lambda event , which = 'append-to-buffer':  self.setInBufferMode( event, which ),
     'prepend-to-buffer': lambda event, which = 'prepend-to-buffer': self.setInBufferMode( event, which ),
     'switch-to-buffer': lambda event, which = 'switch-to-buffer': self.setInBufferMode( event, which ),
     'list-buffers' : lambda event: self.listBuffers( event ),
     'kill-buffer' : lambda event, which = 'kill-buffer': self.setInBufferMode( event, which ),
     'rename-buffer': lambda event: self.renameBuffer( event ),
     'query-replace': lambda event: self.masterQR( event ), 
     'query-replace-regex': lambda event: self.startRegexReplace() and self.masterQR( event ),
     'inverse-add-global-abbrev': lambda event: self.abbreviationDispatch( event, 2 ) ,  
     'expand-abbrev': lambda event : self.keyboardQuit( event ) and self.expandAbbrev( event ), 
     'iconfify-or-deiconify-frame': lambda event: self.suspend( event ) and self.keyboardQuit( event ),
     'save-buffers-kill-emacs': lambda event: self.keyboardQuit( event ) and self.shutdown( event ),
     're-search-forward': lambda event: self.reStart( event ),
     're-search-backward': lambda event: self.reStart( event, which = 'backward' ),
     'diff': self.diff, 
     'what-line': self.whatLine,
     'flush-lines': lambda event: self.startLines( event ),
     'keep-lines': lambda event: self.startLines( event, which = 'keep' ),
     'make-directory': lambda event: self.makeDirectory( event ),
     'remove-directory': lambda event: self.removeDirectory( event ),
     'delete-file': lambda event: self.deleteFile( event ),
     'search-forward': lambda event: self.startNonIncrSearch( event, 'for' ),
     'search-backward': lambda event: self.startNonIncrSearch( event, 'bak' ),
     'word-search-forward': lambda event : self.startWordSearch( event, 'for' ),
     'word-search-backward': lambda event: self.startWordSearch( event, 'bak' ),
     'repeat-complex-command': lambda event: self.repeatComplexCommand( event ),
     'eval-expression': self.startEvaluate,
     'tabify': self.tabify,
     'untabify': lambda event: self.tabify( event, which = 'untabify' ),
     'shell-command': self.startSubprocess,
     'shell-command-on-region': lambda event: self.startSubprocess( event, which=1 ),
    }    
    #Note: if we are reusing some of the cbDict lambdas we need to alter many by adding: self.keyboardQuit( event )
    #Otherwise the darn thing just sits in Alt-X land.  Putting the 'and self.keyboardQuit( event )' part in the killbuffer
    #and yanking it out for each new item, works well.  Adding it to a register might be good to.
    return doAltX






 </t>
<t tx="mork.20041031131847">class ControlXHandler:
    '''The ControlXHandler manages how the Control-X based commands operate on the
       Emacs instance.'''    
    
    @others

</t>
<t tx="mork.20041031132342">def __call__( self, event , stroke ):
    
    self.previous.insert( 0, event.keysym )
    emacs = self.emacs 
    if len( self.previous ) &gt; 10: self.previous.pop()
    if stroke in ('&lt;Key&gt;', '&lt;Escape&gt;' ):
        return self.processKey( event )
    if stroke in emacs.xcommands:
        emacs.xcommands[ stroke ]( event )
        if stroke != '&lt;Control-b&gt;': emacs.keyboardQuit( event )
    return 'break'</t>
<t tx="mork.20041031133146">def processKey( self, event ):
        
    emacs = self.emacs 
    previous = self.previous
    if event.keysym in ( 'Shift_L', 'Shift_R' ):
        return
        
    if emacs.sRect:
        return emacs.stringRectangle( event )
        
    if ( event.keysym == 'r' and emacs.rectanglemode == 0 ) and not emacs.registermode:
        return self.processRectangle( event )
    elif self.rect_commands.has_key( event.keysym ) and emacs.rectanglemode == 1:
        return self.processRectangle( event )
        
    if self.register_commands.has_key( emacs.registermode ):
        self.register_commands[ emacs.registermode ]( event )
        return 'break'
    
    if self.variety_commands.has_key( event.keysym ):
        emacs.stopControlX( event )
        return self.variety_commands[ event.keysym ]( event )
        
    
    #if emacs.sRect:
    #    return emacs.stringRectangle( event )
    #    #return 'break'
    if event.keysym in ( 'a', 'i' , 'e'):
        if self.processAbbreviation( event ): return 'break'

    if event.keysym == 'g':
        svar, label = emacs.getSvarLabel( event )
        l = svar.get()
        if self.abbreviationDispatch.has_key( l ):
            emacs.stopControlX( event )
            return self.abbreviationDispatch[ l ]( event )
        #if l == 'a':
        #    emacs.stopControlX( event )
        #    return emacs.abbreviationDispatch( event, 1 )
        #elif l == 'a i':
        #    emacs.stopControlX( event )
        #    return emacs.abbreviationDispatch( event, 2 )
    if event.keysym == 'e':
        emacs.stopControlX( event )
        return emacs.executeLastMacro( event )
    if event.keysym == 'x' and previous[ 1 ] not in ( 'Control_L', 'Control_R'):
        event.keysym = 's' 
        emacs.setNextRegister( event )
        return 'break'
    
    if event.keysym == 'Escape':
        if len( previous ) &gt; 1:
            if previous[ 1 ] == 'Escape':
                return emacs.repeatComplexCommand( event )
    #if event.keysym == 'r':
    #    return emacs.activateRectangleMethods( event )
    #if self.rect_commands.has_key( event.keysym ):# and emacs.registermode == 1:
    #    return self.processRectangle( event )
     
    #if emacs.registermode == 1:
    #    emacs.setNextRegister( event )
    #    return 'break'
    #elif emacs.registermode == 2:
    #    emacs.executeRegister( event )
    #    return 'break'
    #if self.register_commands.has_key( emacs.registermode ):
    #    print 'register commands'
    #    self.register_commands[ emacs.registermode ]( event )
    #    return 'break'
    #if event.keysym == 'r':
    #    return emacs.activateRectangleMethods( event )
    #    emacs.registermode = 1
    #    svar = emacs.svars[ event.widget ]
    #    svar.set( 'C - x r' )
    #    return 'break'
    #if event.keysym== 'h':
    #    emacs.stopControlX( event )
    #    event.widget.tag_add( 'sel', '1.0', 'end' )
    #tag_add( 'sel', '1.0', 'end' )    return 'break' 
    #if event.keysym == 'equal':
    #    emacs.lineNumber( event )
    #    return 'break'
    #if event.keysym == 'u':
    #    emacs.stopControlX( event )
    #    return emacs.doUndo( event, 2 )   
        
         



</t>
<t tx="mork.20041031134709">def processRectangle( self, event ):
    
    self.rect_commands[ event.keysym ]( event )
    return 'break'
    #if event.keysym == 'o':
    #    emacs.openRectangle( event )
    #    return 'break'
    #if event.keysym == 'c':
    #    emacs.clearRectangle( event )
    #    return 'break'
    #if event.keysym == 't':
    #    emacs.stringRectangle( event )
    #    return 'break'
    #if event.keysym == 'y':
    #    emacs.yankRectangle( event )
    #    return 'break'
    #if event.keysym == 'd':
    #    emacs.deleteRectangle( event )
    #    return 'break'
    #if event.keysym == 'k':
    #    emacs.killRectangle( event )
    #    return 'break'       
</t>
<t tx="mork.20041031135748">def processAbbreviation( self, event ):
    
    emacs = self.emacs
    svar, label = emacs.getSvarLabel( event )
    if svar.get() != 'a' and event.keysym == 'a':
        svar.set( 'a' )
        return 'break'
    elif svar.get() == 'a':
        if event.char == 'i':
            svar.set( 'a i' )
        elif event.char == 'e':
            emacs.stopControlX( event )
            event.char = ''
            emacs.expandAbbrev( event )
        return 'break'</t>
<t tx="mork.20041031145157">class MC_StateManager:
    
    '''MC_StateManager manages the state that the Emacs instance has entered and
       routes key events to the right method, dependent upon the state in the MC_StateManager'''
       
    @others



</t>
<t tx="mork.20041031150125"># EKR: used only below.
def eA( event ):
    if self.emacs.expandAbbrev( event ) :
        return 'break'

self.stateCommands = { #1 == one parameter, 2 == all
    'uC': ( 2, emacs.universalDispatch ),
    'controlx': ( 2, emacs.doControlX ),
    'isearch':( 2, emacs.iSearch ),
    'goto': ( 1, emacs.Goto ),
    'zap': ( 1, emacs.zapTo ),
    'howM': ( 1, emacs.howMany ),
    'abbrevMode': ( 1, emacs.abbrevCommand1 ),
    'altx': ( 1, emacs.doAlt_X ),
    'qlisten': ( 1, emacs.masterQR ),
    'rString': ( 1, emacs.replaceString ),
    'negativeArg':( 2, emacs.negativeArgument ),
    'abbrevOn': ( 1, eA ),
    'set-fill-column': ( 1, emacs.setFillColumn ),
    'chooseBuffer': ( 1, emacs.chooseBuffer ),
    'renameBuffer': ( 1, emacs.renameBuffer ),
    're_search': ( 1, emacs.re_search ),
    'alterlines': ( 1, emacs.processLines ),
    'make_directory': ( 1, emacs.makeDirectory ),
    'remove_directory': ( 1, emacs.removeDirectory ),
    'delete_file': ( 1, emacs.deleteFile ),
    'nonincr-search': ( 2, emacs.nonincrSearch ),
    'word-search':( 1, emacs.wordSearch ),
    'last-altx': ( 1, emacs.executeLastAltX ),
    'escape': ( 1, emacs.watchEscape ),
    'subprocess': ( 1, emacs.subprocesser ),
    }</t>
<t tx="mork.20041031155313">@others</t>
<t tx="mork.20041031155455">@others</t>
<t tx="mork.20041031155642">@
These methods add things to the registers( a-z )

@c

@others</t>
<t tx="mork.20041031155753">@
general macro methods.

@c


@others</t>
<t tx="mork.20041031155913">@others</t>
<t tx="mork.20041031160002">@
These methods take the user to a specific line or a specific character in the buffer


@c

@others</t>
<t tx="mork.20041031162857">def __init__( self, emacs ):
        
    self.emacs = emacs
    self.state = None
    self.states = {}
    &lt;&lt;statecommands&gt;&gt;</t>
<t tx="mork.20041031162857.1">def setState( self, state, value ):
        
    self.state = state
    self.states[ state ] = value</t>
<t tx="mork.20041031162857.2">def getState( self, state ):
    
    return self.states.get(state,False)</t>
<t tx="mork.20041031162857.3">def hasState( self ):

    if self.state:
        return self.states[ self.state ]
</t>
<t tx="mork.20041031162857.4">def __call__( self, *args ):
        
    if self.state:
        which = self.stateCommands[ self.state ]
        
        # EKR: which[0] is a flag: 1 == one parameter, 2 == all
        # EKR: which[1] is the function.
        
        if which[ 0 ] == 1:
            return which[ 1 ]( args[ 0 ] )
        else:
            return which[ 1 ]( *args )
</t>
<t tx="mork.20041031162857.5">def clear( self ):
        
    self.state = None

    for z in self.states.keys():
        self.states[ z ] = False</t>
<t tx="mork.20041031162953">def __init__( self, emacs ):
        
    self.emacs = emacs
    self.previous = []
    self.rect_commands = {
    'o': emacs.openRectangle,
    'c': emacs.clearRectangle,
    't': emacs.stringRectangle,
    'y': emacs.yankRectangle,
    'd': emacs.deleteRectangle,
    'k': emacs.killRectangle,
    'r': emacs.activateRectangleMethods,             
    }
    
    self.variety_commands = {
    'period': emacs.setFillPrefix,
    'parenleft': emacs.startKBDMacro,
    'parenright' : emacs.stopKBDMacro,
    'semicolon': emacs.setCommentColumn,
    'Tab': emacs.tabIndentRegion,
    'u': lambda event: emacs.doUndo( event, 2 ),
    'equal': emacs.lineNumber,
    'h': emacs.selectAll,
    'f': emacs.setFillColumn,
    'b': lambda event, which = 'switch-to-buffer': emacs.setInBufferMode( event, which ),
    'k': lambda event, which = 'kill-buffer': emacs.setInBufferMode( event, which ),
    }
    
    self.abbreviationDispatch = {    
    'a': lambda event: emacs.abbreviationDispatch( event, 1 ),
    'a i': lambda event: emacs.abbreviationDispatch( event, 2 ),    
    }
    
    self.register_commands ={    
    1: emacs.setNextRegister,
    2: emacs.executeRegister,        
    }
</t>
<t tx="mork.20041031181701">@

type some text, set its abbreviation with Control-x a i g, type the text for abbreviation expansion
type Control-x a e ( or Alt-x expand-abbrev ) to expand abbreviation
type Alt-x abbrev-on to turn on automatic abbreviation expansion
Alt-x abbrev-on to turn it off

an example:
type:
frogs
after typing 's' type Control-x a i g.  This will turn the minibuffer blue, type in your definition. For example: turtles.

Now in the buffer type:
frogs
after typing 's' type Control-x a e.  This will turn the 'frogs' into:
turtles



@c

@others</t>
<t tx="mork.20041031181701.1">@
These methods handle the query-replace and query-replace-regex commands.  They need to be fully migrated
to the self.mcStateManager mechanism, which should simplify things greatly, or at least the amount of variables its required
so far.

@c


@others</t>
<t tx="mork.20041031181701.2">@others</t>
<t tx="mork.20041031181740">@others</t>
<t tx="mork.20041031181929">@
These methods add text to the killbuffer.
@c

@others</t>
<t tx="mork.20041031181929.1">@
These methods control the Alt-x command functionality.

@c


@others</t>
<t tx="mork.20041031182137">@

untested as of yet for .5 conversion.

@c


@others</t>
<t tx="mork.20041031182215">@
Two closely related categories under this one heading.  Svars are the internals of the minibuffer
and the labels are the presentation of those internals

@c

@others</t>
<t tx="mork.20041031182258">@
These methods create the dispatch dictionarys that the
Emacs instance uses to execute specific keystrokes and commands.
Dont mess with it if you dont understand this section, without these dictionarys
the Emacs system cant work.

@c


@others</t>
<t tx="mork.20041031182332">@
These methods start and execute the Zap to functionality.
@c



@others</t>
<t tx="mork.20041031182402">@others</t>
<t tx="mork.20041031182449">@
These methods load files into buffers and save buffers to files

@c


@others</t>
<t tx="mork.20041031182643">@others</t>
<t tx="mork.20041031182643.1">@
Emacs requires an undo mechanism be added from the environment.
If there is no undo mechanism added, there will be no undo functionality in the instance.
@c



@others</t>
<t tx="mork.20041031182709">@others</t>
<t tx="mork.20041031182837">@
These methods enable the incremental search functionality.

@c

@others</t>
<t tx="mork.20041031182916">@others</t>
<t tx="mork.20041031182943">@
These methods get and alter the Svar variable which is a Tkinter
StringVar.  This StringVar contains what is displayed in the minibuffer.
@c


@others</t>
<t tx="mork.20041031183018">@others</t>
<t tx="mork.20041031183136">@others</t>
<t tx="mork.20041031183614">@
These methods currently do not have a specific class that they belong to.

@c


@others</t>
<t tx="mork.20041031183614.1">@others</t>
<t tx="mork.20041031194703">@others</t>
<t tx="mork.20041031194746">@
These methods contain methods by which an Emacs instance is extended, changed, added to , etc...

@c


@others</t>
<t tx="mork.20041031194858">@others</t>
<t tx="mork.20041031195549">@others</t>
<t tx="mork.20041031195908">@others</t>
<t tx="mork.20041031195908.1">@others</t>
<t tx="mork.20041031202438">def selectAll( event ):

    event.widget.tag_add( 'sel', '1.0', 'end' )
    return 'break'
    
</t>
<t tx="mork.20041031202908">def activateRectangleMethods( self, event ):
    
    self.rectanglemode = 1
    svar = self.svars[ event.widget ]
    svar.set( 'C - x r' )
    return 'break'
</t>
<t tx="mork.20041101083527">class MC_KeyStrokeManager:
    
    @others</t>
<t tx="mork.20041101083527.1">def __init__( self, emacs ):
    
    self.emacs = emacs

    &lt;&lt;keystrokes&gt;&gt;
</t>
<t tx="mork.20041101083527.2">self.keystrokes = {

    '&lt;Control-s&gt;': ( 2, emacs.startIncremental ), 
    '&lt;Control-r&gt;': ( 2, emacs.startIncremental ),
    '&lt;Alt-g&gt;': ( 1, emacs.startGoto ),
    '&lt;Alt-z&gt;': ( 1, emacs.startZap ),
    '&lt;Alt-percent&gt;': ( 1,  emacs.masterQR ) ,
    '&lt;Control-Alt-w&gt;': ( 1, lambda event: 'break' ),
}</t>
<t tx="mork.20041101084148">def hasKeyStroke( self, stroke ):
    
    return self.keystrokes.has_key( stroke )</t>
<t tx="mork.20041101084148.1">def __call__( self, event, stroke ):
    
    kstroke = self.keystrokes[ stroke ]
    
    if 0: # EKR: this would be better:
        numberOfArgs,func = self.keystrokes[ stroke ]
        if numberOfArgs == 1:
            return func(event)
        else:
            return func(event,stroke)
    
    # EKR: which[0] is the number of params.
    # EKR: which[1] is the function.

    if kstroke[ 0 ] == 1:
        return kstroke[ 1 ]( event )
    else:
        return kstroke[ 1 ]( event, stroke )
        
    </t>
<t tx="mork.20041101100635">@

.5
       This was a fairly major shift for temacs.
   -- Changed structure from pure functional to Object Oriented.  Emacs is the central class in the temacs package now.
      The changes wrought by this are quite extensive.
   -- worked on complicated control logic, turned some parts into Objects that are state Handlers and Managers
   -- fixed a bug in block indentation.  If the first line was blank it throw an Exception.  It now finds the first text line.
   -- added the ability to add extensions.  see 'how to write an Emacs extension' section.  Also look at exampleTemacsExtension.py
      for a simple example as to how this works.
   -- fixed control-left control-right up so they do what Emacs does.  This has ramifications for delete previous word as well,
      since that command relies on the control-left command to do its work.
   -- added the ability to change the keystrokes via the reconfigureKeyStroke method.  This method is largely untested.
   -- last count: at around 204 keystrokes and commands( note some commands and keystrokes are the same,
      just different ways of accesing the functionality.
   -- enhanced incremental search so that if the search doesnt find anything it will start again either at the top or bottom, depending
      on which direction it is going.  This is a nice little enhancement.
   -- enhanced Tabing with alt-x, so that the user can cycle through the matches. Added Tracker class to accomplish this.
      This will speed up the use of the Alt-x commands and expose functionality that is hard for a user to remember by keystroke.
   -- added Control-x and regular keystroke commands to Alt-x commands.  Ive focused on the ones Ive found most usefull.  This might be
      the best way to access rectangle functionality and registers.
   -- Created a better organized Outline.  There are several organizing nodes now.  Its easier to find things when looking for them.
   -- Added killing append to system clipboard.  The clipboard gets set with every kill.  Control - y will return the fresh clipboard kill as well as Alt-y.  This will be very nice to have.
   -- Added ability to test standalone.  Just type: python temacs.py and a simple Editor will appear.
   -- New commands and keystrokes:
       Control-j ( insert newline and tab )
       added goto-char
       added set-fill-column ( Control-x f )
       added center-line  ( Alt- s )
       added center-region ( see node 'fill column and centering' to see what these do )
       ( these buffer ops have to be configured so the Emacs instance knows what is a 'buffer' in the environment,
       see 'buffer recognition and alterers' node )
       append-to-buffer
       prepend-to-buffer
       copy-to-buffer
       insert-buffer
       list-buffer ( aka Control-x Control-b )
       switch-to-buffer ( aka Control-x b )
       kill-buffer ( aka Control-x k )
       rename-buffer


0.51 EKR:  Minor stylistic changes.

0.55:
    added:
    Control-z or 'iconify-or-deiconfify-frame'
    Control-x Esc Esc - executes last Alt-x command( repeat-complex-command )
    Control-x Control-c shutdown code, as well as a replacement hook if configured to do so.
    re-search-forward, re-search-backward - simple Alt-x regular expression commands
    Control-Alt-s, Control-Alt-r - regular expression cousins of incremental search( which makes me think that I need to change isearch to python based searches instead of the Tcl way..
    diff - does a diff on 2 files and adds it as a buffer
    what-line
    keep-lines and flush-lines, two fun new text manipulation commands!(see help text )
    make-directory and remove-directory, two commands that remove and add directories.
    delete-file - removes a file
    search-forward search-backward, searchs backward and forward for a word, non-incrementally.  Accessed by Conrtrol-s Enter and Control-r
    word-search-forward and word-search-backward, incredible!  You search for a group of words ignoring punctuation.  This is mighty stuff, dont know if Ill use it, but I like what I see.
    replace-regex - like replace-string but uses a python regular expression for the match.
    query-replace-regex( Control-Alt-% ) -like query-replace but with a python regular expression
    Esc Esc :, Alt-:, eval-expression  - these evaluate a Python expression in the minibuffer and puts the value in the current buffer.  This I think is different than what Emacs does, but I think it makes the value more accessible if its in the current buffer.  Nice little calculator too.
    tabify, untabify - turns spaces to tabs and tabs into spaces( current does it on 4 spaces to one tab ).
    indent-relative - a very nice command that indents from the insert point until it matches the indentation of a word in the above line.
    changed:
    replace-string command now will operate on a selection if there is one.  Also the function now uses string functionality to replace the
    strings instead of using the Tk Text widget to do the job.
    dynamic expansion now will expand with the '-' character, which helps greatly in some cases.  Alot of work for a what will hopefully be a long term gain.  Also will now use quoted strings as actual completion targets, thank goodness.
    fixed:
    sort-lines will now clear its state after sorting the lines.
    Alt-!(shell-command, Alt-|(shell-command-on-region) --now temacs allows one to execute shell commands.  I dont see a shell being added to temacs, so thats one area where it will probably not stray.
    total 26 new commands added
    fixed up: sort-lines and its cousins, if nothing is selected the command is deactivated.
</t>
<t tx="mork.20041101124927">def modifyOnBodyKey( self, event ):
    '''stops Return and Tab from being processed if the Emacs instance has state.'''
    if event.char.isspace(): 
        Emacs = temacs.Emacs.Emacs_instances[ event.widget ]   
        if Emacs.mcStateManager.hasState():
           return None
    return orig_OnBodyKey( self, event )
</t>
<t tx="mork.20041101132349">@ 

.5 -- fixed problem with spurious whitespace being added in some of the paste commands when Return was entered.  This was
      because Leo is programmed to indent after Enter is pressed.  We decorate the OnBodyKey with usetemacs modifyOnBodyKey.
   -- made transitions to temacs.Emacs class
   -- Help text can now be searched.  Search is initiated by either typing Return in the Entry or pressing the go button.
   -- Set it up so when the Text widget has all of its text deleted via a call to delete '1.0', 'end', this calls
      the StopControlX method of the Emacs object.  This is equivilant of pressing Control-G.
   -- Added ability to load temacs.Emacs extensions
   -- Added ability to change default key bindings( in alpha stage ).
   -- Created example Emacs extension.
   -- Added ability for user to see each node in the outline as a buffer.  There are methods in temacs such as
      append-to-buffer, copy-to-buffer, etc... that needs a name and some supplied functionality to do its work.
      usetemacs does this for the Emacs instance.  Note: if a group of nodes have the same name, then only one will be viewable
      by the Emacs instance.  This might be enhanced in the future to include all headlines.
      I would not recommend 'list-buffers' if you have a large outline.  This will have to be enhanced in the future as well.
   -- Removed all references to Pmw in code( still exists in comments ).  Reports of some weirdness with the string.atoi and how
      it was behaving in Pmw.  This helps lower the bar of entry to this.  I have replaced the megawidgets with items like
      ScrolledText and a minibuffer composed of a Frame, a Frame in this Frame, and 2 labels.
   -- folded in changes from .4 that could be detected

.51
.52 EKR: Minor style changes.
.53 EKR: Use __name__ in .plugin_signon
.55
    --added a def that adds all the Leo Commands to the Emacs instance, in command addLeoCommands.  I no longer need to
    remember how to summon the find panel, its done via Alt-x 'find panel'.  This was a very good use of the extension mechanism
    that was put into place in .5.  I should note that there are a couple I left out like Recent Files, and End Edit Headline,
    since they didnt seem to functional( i.e. no good way to use them within the Alt-x mechanism).
    --changed the location of where text appears in the minibuffer, it now always starts from the left instead of the center.
    This is what Emacs does, and its less disorienting.
    --added a dialog to show up if there are multiple nodes with the same name.  This gives the user the ability to select a node
    in its numerical position in the graph, from 1 to N.  Im still surprised that this works as quick as it does, more power to the
    graph!
    --added Leo Commands to Temacs Help, good to see which Leo commands you can execute.
.56 EKR:
    - Removed 'start2' hook and haveseen dict.
    - Added init function.
.57 EKR:
    - Added global orig_Bindings,orig_OnBodyKey to init().
    - Removed writeNewDerivedFiles writeOldDerivedFiles and 'apply settings' commands.
    - Changed c.findPanel to c.showFindPanel.
    - Changed leoConfig.txt to leoSettings.leo in docstring.
</t>
<t tx="mork.20041101190309">def extendAltX( self, name, function ):
    '''A simple method that extends the functions Alt-X offers.'''
    
    nfunction = new.instancemethod( function, self, Emacs ) #making it an instance method allows the function to be passed 'self'.
    self.doAltX[ name ] = nfunction
    

</t>
<t tx="mork.20041101191351">def loadConfig():
    '''Loads Emacs extensions and new keystrokes to be added to Emacs instances'''
    pth = os.path.split(g.app.loadDir)   
    aini = pth[0]+r"/plugins/usetemacs.ini"
    if os.path.exists( aini ):
        
        cp = ConfigParser.ConfigParser()
        cp.read( aini )
        section = None
        for z in cp.sections():
            if z.strip() == 'extensions':
                section = z
                break
        
        if section:
            for z in cp.options( section ):
                extension = cp.get( section, z )
                try:
                    ex = __import__( extension )
                    extensions.append( ex )
                except Exception, x:
                    g.es( "Could not load %s because of %s" % ( extension, x ), color = 'red' )
                
        kstroke_sec = None
        for z in cp.sections():
            if z.strip() == 'newkeystrokes':
                kstroke_sec = z
                break
        if kstroke_sec:
            for z in cp.options( kstroke_sec ):
                new_keystrokes[ z.capitalize() ] = cp.get( kstroke_sec, z )




</t>
<t tx="mork.20041101202945">def addTemacsExtensions( Emacs ):
    '''Adds extensions to Emacs parameter.'''
    for z in extensions:
            try:
                if hasattr( z, 'getExtensions' ):
                    ex_meths = z.getExtensions()
                    for x in ex_meths.keys():
                        Emacs.extendAltX( x, ex_meths[ x ] )
                else:
                    g.es( 'Module %s does not have a getExtensions function' % z , color = 'red' )
            except Exception, x:
                g.es( 'Could not add extension because of %s' % x, color = 'red' )
</t>
<t tx="mork.20041101203748">@
Emacs instances offer the user the ability to add functionality
to itself.  This is accomplished through the Emacs extendAltX method.  Functions passed in should not be methods
but just plain functions.

An example:
def burp( self, event ):
    print 'burp %s' % self     #This will print info about the Emacs instance
    self.stopControlX( event ) #every extension should call this or the function will be called for each keystroke.
                               #To be more precise, it should be called when the function has completely cycled through.
ei.extendAltX( 'burp', burp ) #burp has been added as an Alt-x command and the burp function has become
                              #a method of the Emacs instance.  self, will now reflect this.

accessing it through the Alt-X interface will be done like so
Alt-x
burp ( Hit return , alternatively the user could type b and hit the tab button )

Each function/method will be called with two parameters:
    self -- which is the Emacs instance
    event -- which is an Tkinter Event instance.
    self gives the extension writer the ability to access the Emacs intances functionality
    event gives the user the ability to access the Text widget that the Emacs instance is bound to.
    the preferred way to do so is like this:
    tbuffer = event.widget</t>
<t tx="mork.20041101204659">@

to begin to understand how to write an Emacs extension see temacs.py section 'how to write an Emacs extension'.

usetemacs will look for a file called usetemacs.ini

It will open this file and look for a sections called [ extensions ]

every option under this section will act as an indicator to import a module.

For example:
[ extensions ]
1=anExtension

The module anExtension.py must be importable by usetemacs.

-----
usetemacs will load anExtension as a module.  For each Emacs object created it will
call the modules getExtensions() method which should return a dictionary containing:
    a. keys that are strings.  These are the names that will be added to the Alt-x command in Emacs.
    b. functions.  These should not be methods, as they become methods when added to Emacs.
    for example:
        module test.py:
        def power( self, event ):
            print 'power'
        def getExtensions():
            return { 'power' : power }
    upon loading by usetemacs, every Emacs instance will have 'power' added as an Alt-x command which will call
    the power function( method after adding ).  The extension write should not worry about the name of the function,
    they should only worry about the name that they want to access the function-method by.  It is possible to overwrite
    a default Alt-x method if the same name is used.
-----

To test an Emacs extensions try out the exampleTemacsExtension.py with this mechanism.

</t>
<t tx="mork.20041101205414">def watchDelete(  i, j = None, Emacs = None , orig_del = None , Text = None ):
    '''Watches for complete text deletion.  If it occurs, turns off all state in the Emacs instance.'''
    if j:
        if i == '1.0' and j == 'end':
            event = Tk.Event()
            event.widget = Text
            Emacs.keyboardQuit( event )
    return orig_del( i, j )</t>
<t tx="mork.20041101210722">def addTemacsAbbreviations( Emacs ):
    '''Adds abbreviatios and kbd macros to an Emacs instance'''
    pth = os.path.split( g.app.loadDir ) 
    aini = pth[ 0 ] + os.sep + 'plugins' + os.sep
    if os.path.exists( aini + r'usetemacs.kbd' ):
        f = file( aini +  r'usetemacs.kbd', 'r' )
        Emacs._loadMacros( f )
    if os.path.exists( aini + r'usetemacs.abv' ):
        f = file( aini + r'usetemacs.abv', 'r' )
        Emacs._readAbbrevs( f )
        

</t>
<t tx="mork.20041102081834">@ 

tbuffer - a Tkinter Text widget.  Would be called buffer, but this shadows a Python builin.  This is the widget carried
by the events in the Emacs instancs.  Can be accessed like so 'event.widget'
svar - a Tkinter StringVar widget.  This should hold what the minibuffer is showing currently.  Can
be acquired by 'self.getSvarLabel'.



</t>
<t tx="mork.20041102082023">def keyboardQuit( self, event ):
    '''This method cleans the Emacs instance of state and ceases current operations.'''
    return self.stopControlX( event )#This method will eventually contain the stopControlX code.
    
</t>
<t tx="mork.20041102082911">@ 

.5

- control-u seems kinda flaky.  Will enhance in the next iteration and make less flaky. :)
- digit-arguments seem pretty flaky as well.
--- These are no longer flaky.  A simple change to calling self.keyboardQuit, has eliminated the flakiness Ive seen. :)
    This was centered on using a command that wasnt a commadn like typing 99a, made it burp!  You can also see the commands
    as they are done in the Editor.  For example 'Control-u 99 a'  will type 'a' 99 times in the editor.  Or
    'Control-u 99 Control-_'  will undo the last 99 changes, thats if the Emacs instance has been configure with an undoer.</t>
<t tx="mork.20041102091309">@

'''An example of a temacs Extension.  To test example:
    1. Create usetemacs.ini file.
    2. Make an [ extensions ] section.
    3. put:
       1=exampleTemacsExtension
    When Leo starts,
    select a set of lines
    type Alt-x
    the format-selection-as-list and hit Enter( or type format and hit tab, the autocompletion will work ).
    After typing Enter you should see you selection indented and each line prefixed with an ascending number.'''


def formatSelectionAsList( self, event ):
    '''This function indents and prepends a number to a selection of text'''
    try: #We guard against there not being anything selected, which throws an Exception in this block.
        tbuffer = event.widget # call the Text instance tbuffer as in Emacs class.
        self.indentRegion( event ) # use the Emacs instances indentRegion method to do initial formatting.
        start = tbuffer.index( 'sel.first linestart' )
        start = tbuffer.search( '\w', start, regexp = True, stopindex = '%s lineend' % 'sel.last' )
        if not start:
            return self.keyboardQuit( event )
        end = tbuffer.index( 'sel.last' )
    except Exception, x:
        return self.keyboardQuit( event )
    r1, c1 = start.split( '.' )
    r1, c1 = int( r1 ), int( c1 )
    r2, c2 = end.split( '.' )
    r2 = int( r2 )
    amount = r2 - r1
    for z in xrange( amount + 1 ):
        tbuffer.insert( '%s.%s' % ( r1, c1 ), '%s. ' % ( z + 1 ))
        r1 = r1 + 1
    self.keyboardQuit( event ) # this turns off the state and sets things to normal
    return self._tailEnd( tbuffer ) # this calls the _tailEnd method, which when used with usetemacs will ensure that the text sticks.

def getExtensions():

    return { 'format-selection-as-list': formatSelectionAsList } #We return the one function in this module.</t>
<t tx="mork.20041102092057">@

#An example usetemacs .ini file
[ extensions ]
1=exampleTemacsExtension

[ newkeystrokes ]
#Alt-q=Alt-f</t>
<t tx="mork.20041102094131">@ 

usetemacs depends on temacs and Leo like so:
temacs.py  &lt;------ usetemacs.py -------&gt; Leo

temacs can function by itself.
Leo can function by itself.

usetemacs brings the two together.

Its the glue between the temacs module and Leo.  Leo doesn't need usetemacs to function, temacs doesn't need usetemacs to be used.
But if temacs.py and Leo are to work together usetemacs.py must be employed as a plugin for Leo.

It performs several helpful functions for temacs and Leo:

1. Protects against bad whitespace being added because of a Return key press.
2. Does a keyboardQuit if a new node is selected.
3. Configures temacs with temacs extensions.
4. Adds abbreviations and macros to Emacs instances
5. Configures Emac instances with functions that allow it to treat nodes as buffers.</t>
<t tx="mork.20041102094341">@ 

temacs.py prior to the .4 version needed to be installed so that it could be loaded anywhere from a python instance.
Now all the user needs to do is have temacs.py in the same plugins directory of the usetemacs plugin.  The plugin should
be able to load the module if done in this way.</t>
<t tx="mork.20041102094716">def reconfigureKeyStroke( self, tbuffer, keystroke , set_to ):
    
    '''This method allows the user to reconfigure what a keystroke does.
       This feature is alpha at best, and untested.'''

    if self.cbDict.has_key( set_to ):
        
        command = self.cbDict[ set_to ]
        self.cbDict[ keystroke ] = command
        evstring = '&lt;%s&gt;' % keystroke
        tbuffer.bind( evstring,  lambda event, meth = command: self.masterCommand( event, meth , evstring)  )</t>
<t tx="mork.20041102094928">def changeKeyStrokes( Emacs, tbuffer ):
    
    for z in new_keystrokes.keys():
        Emacs.reconfigureKeyStroke( tbuffer, z, new_keystrokes[ z ] )
</t>
<t tx="mork.20041102102111">@

usetemacs allows the user to change keystrokes in the Emacs instances via the ustemacs.ini file.

the section should be called [ newkeystrokes ].

To reconfigure a keystroke or add a keystroke, under the section add for example:
Alt-q=Alt-f



this will rebind Alt-q to what Alt-f does.

------
note this feature is largely untested and will most likely need work.

</t>
<t tx="mork.20041102103822">@

1. Continue adding the keystroke command names to the Alt-x mechanism.  Much of this has already been done.
2. Maybe make it possible for the user to add state to the MC_StateManager instance.  This could allow the extension writer
to create specific state based extension functions.  They may already be able to do this.
3. When python 2.4 is official, look at subprocess module and decide if it can be used to run exterior commands.  Pythons current
cross platform process commands, dont seem too cross platform at this point.  subprocess hopefully will fix this.
4. Continue migrating statefull commands to the MC_StateManager class.
5. Add ability for a user to learn the keystroke for a command.  The Help Text should be considered a definitive source of
information, but it may be quicker for the user to just ask.  This will be accomplished by adding the 'where-is' command or
'Control-h w'.  Not essential at this point, and will be done when we are entering a polish iteration.
6. Maybe add the ability for the user to evaluate Python expressions.  Vanilla Emacs has the ability to do something with
Lisp expressions, so it may make sense to do this with Python since Python is what this is built out of.
7. Maybe add Emacs variables for the commands.  Ive noticed that you can set Emac variables to change some of the behavior
in subtle ways.  A dictionary should be used to implement this, adding 1000 attributes to the Emacs class doesnt seem like a good idea.
8 Maybe add local abbreviations 'Control-x a i l'</t>
<t tx="mork.20041102131352">class Tracker:
    '''A class designed to allow the user to cycle through a list
       and to change the list as deemed appropiate.'''

    @others</t>
<t tx="mork.20041102131352.1">def __init__( self ):
    
    self.tablist = []
    self.prefix = None
    self.ng = self._next()</t>
<t tx="mork.20041102131352.2">def setTabList( self, prefix, tlist ):
    
    self.prefix = prefix
    self.tablist = tlist
    

</t>
<t tx="mork.20041102131352.3">def _next( self ):
    
    while 1:
        
        tlist = self.tablist
        if not tlist: yield ''
        for z in self.tablist:
            if tlist != self.tablist:
                break
            yield z
</t>
<t tx="mork.20041102132710">def next( self ):
    
    return self.ng.next()
</t>
<t tx="mork.20041102133805">def _findMatch( self, svar, fdict = None ):#, fdict = self.doAltX ):
    '''This method finds the first match it can find in a sorted list'''
    if not fdict:
        fdict = self.doAltX
    txt = svar.get()
    pmatches = filter( lambda a : a.startswith( txt ), fdict )
    pmatches.sort()
    if pmatches:
        mstring = reduce( self.findPre, pmatches )
        return mstring
    return txt
</t>
<t tx="mork.20041102151545">def viewRegister( self, event ):
    
    self.stopControlX( event )
    if event.keysym in string.letters:
        text = self.registers[ event.keysym.lower() ]
        svar, label = self.getSvarLabel( event )
        svar.set( text )</t>
<t tx="mork.20041102151939">def setEvent( self, event, l ):
    event.keysym = l
    return event
    
</t>
<t tx="mork.20041102160313">def clear( self ):

    self.tablist = []
    self.prefix = None
</t>
<t tx="mork.20041102161859">def viewLossage( self, event ):
    
    svar, label = self.getSvarLabel( event )
    loss = ''.join( Emacs.lossage )
    self.keyboardQuit( event )
    svar.set( loss )</t>
<t tx="mork.20041102183901"></t>
<t tx="mork.20041103085329">@
These methods are currently just used in tandem to center the line or region within the fill column.
for example, dependent upon the fill column, this text:

cats
raaaaaaaaaaaats
mats
zaaaaaaaaap

may look like

                                 cats
                           raaaaaaaaaaaats
                                 mats
                             zaaaaaaaaap
after an center-region command via Alt-x.


@c


@others

</t>
<t tx="mork.20041103085329.1">def centerLine( self, event ):
    '''Centers line within current fillColumn'''
    
    tbuffer = event.widget
    ind = tbuffer.index( 'insert linestart' )
    txt = tbuffer.get( 'insert linestart', 'insert lineend' )
    txt = txt.strip()
    if len( txt ) &gt;= self.fillColumn: return self._tailEnd( tbuffer )
    amount = ( self.fillColumn - len( txt ) ) / 2
    ws = ' ' * amount
    col, nind = ind.split( '.' )
    ind = tbuffer.search( '\w', 'insert linestart', regexp = True, stopindex = 'insert lineend' )
    if not ind: return 'break'
    tbuffer.delete( 'insert linestart', '%s' % ind )
    tbuffer.insert( 'insert linestart', ws )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041103085329.2">def setFillColumn( self, event ):
    
    if self.mcStateManager.getState( 'set-fill-column' ):
        
        if event.keysym == 'Return':
            svar, label = self.getSvarLabel( event )
            value = svar.get()
            if value.isdigit():
                self.fillColumn = int( value )
            return self.keyboardQuit( event )
        elif event.char.isdigit() or event.char == '\b':
            svar, label = self.getSvarLabel( event )
            self.setSvar( event, svar )
            return 'break'
        return 'break'
        
        
        
    else:
        self.mcStateManager.setState( 'set-fill-column', 1 )
        svar, label = self.getSvarLabel( event )
        svar.set( '' )
        label.configure( background = 'lightblue' )
        return 'break'
</t>
<t tx="mork.20041103095628">def centerRegion( self, event ):
    '''This method centers the current region within the fill column'''
    tbuffer = event.widget
    start = tbuffer.index( 'sel.first linestart' )
    sindex , x = start.split( '.' )
    sindex = int( sindex )
    end = tbuffer.index( 'sel.last linestart' )
    eindex , x = end.split( '.' )
    eindex = int( eindex )
    while sindex &lt;= eindex:
        txt = tbuffer.get( '%s.0 linestart' % sindex , '%s.0 lineend' % sindex )
        txt = txt.strip()
        if len( txt ) &gt;= self.fillColumn:
            sindex = sindex + 1
            continue
        amount = ( self.fillColumn - len( txt ) ) / 2
        ws = ' ' * amount
        ind = tbuffer.search( '\w', '%s.0' % sindex, regexp = True, stopindex = '%s.0 lineend' % sindex )
        if not ind: 
            sindex = sindex + 1
            continue
        tbuffer.delete( '%s.0' % sindex , '%s' % ind )
        tbuffer.insert( '%s.0' % sindex , ws )
        sindex = sindex + 1
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041103120919">def getClipboard( self, tbuffer ):
    
    ctxt = None
    try:
        ctxt = tbuffer.selection_get( selection='CLIPBOARD' )
        if ctxt != self.last_clipboard or not self.killbuffer:
            self.last_clipboard = ctxt
            if self.killbuffer and self.killbuffer[ 0 ] == ctxt:
                return None
            return ctxt
        else:
            return None
        
    except:
        return None
        
    return None</t>
<t tx="mork.20041103135515">def insertNewLineAndTab( self, event ):
    '''Insert a newline and tab'''
    tbuffer = event.widget
    self.insertNewLine( event )
    i = tbuffer.index( 'insert +1c' )
    tbuffer.insert( i, '\t' )
    tbuffer.mark_set( 'insert', '%s lineend' % i )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041103155347">@
an Emacs instance does not have knowledge of what is considered a buffer in the environment.
It must be configured by the user so that it can operate on the other buffers.  Otherwise
these methods will be useless.

@c


@others</t>
<t tx="mork.20041103155347.1">def setBufferListGetter( self, buffer, method ):
    #Sets a method that returns a buffer name and its text, and its insert position.
    self.bufferListGetters[ buffer ] = method
</t>
<t tx="mork.20041103155347.2">def setBufferSetter( self, buffer, method ):
    #Sets a method that takes a buffer name and the new contents.
    self.bufferSetters[ buffer ] = method</t>
<t tx="mork.20041103155347.3">def getBufferDict( self, event ):
    
    tbuffer = event.widget
    meth = self.bufferListGetters[ tbuffer ]
    return meth()</t>
<t tx="mork.20041103155347.4">def appendToBuffer( self, event, name ):

    tbuffer = event.widget
    try:
        txt = tbuffer.get( 'sel.first', 'sel.last' )
        bdata = self.bufferDict[ name ]
        bdata = '%s%s' % ( bdata, txt )
        self.setBufferData( event, name, bdata )
    except Exception, x:
        pass
    return self.keyboardQuit( event )</t>
<t tx="mork.20041103155347.5">def prependToBuffer( self, event, name ):
    
    tbuffer = event.widget
    try:
        txt = tbuffer.get( 'sel.first', 'sel.last' )
        bdata = self.bufferDict[ name ]
        bdata = '%s%s' % ( txt, bdata )
        self.setBufferData( event, name, bdata )
    except Exception, x:
        pass
    return self.keyboardQuit( event )</t>
<t tx="mork.20041103155347.6">def insertToBuffer( self, event, name ):

    tbuffer = event.widget
    bdata = self.bufferDict[ name ]
    tbuffer.insert( 'insert', bdata )
    self._tailEnd( tbuffer )
    return self.keyboardQuit( event )
</t>
<t tx="mork.20041103155347.7">def copyToBuffer( self, event, name ):
    
    tbuffer = event.widget
    try:
        txt = tbuffer.get( 'sel.first', 'sel.last' )
        self.setBufferData( event, name, txt )
    except Exception, x:
        pass
    return self.keyboardQuit( event )
    
</t>
<t tx="mork.20041103160433">tnodes = {}
positions =  {}
def setBufferInteractionMethods( c, emacs, buffer ):
    '''This function configures the Emacs instance so that
       it can see all the nodes as buffers for its buffer commands.'''
    def buildBufferList(): #This builds a buffer list from what is in the outline.  Worked surprisingly fast on LeoPy.
        if not tnodes.has_key( c ): #I was worried that speed factors would make it unusable.
            tnodes[ c ] = {}
        tdict = tnodes[ c ]
        pos = c.rootPosition()
        utni = pos.allNodes_iter()
        bufferdict = {}
        tdict.clear()
        positions.clear()
        for z in utni:
        
           t = z.v.t
           if positions.has_key( t.headString ):
            positions[ t.headString ].append( z.copy() )
           else:
            positions[ t.headString ] = [ z.copy() ]#not using a copy seems to have bad results.
           #positions[ t.headString ] = z
        
           bS = ''
           if t.bodyString: bS = t.bodyString
 
           
           bufferdict[ t.headString ] = bS
           tdict[ t.headString ] = t 
        
        return bufferdict
        
    def setBufferData( name, data ):
        
        data = unicode( data )
        tdict = tnodes[ c ]
        if tdict.has_key( name ):
            tdict[ name ].bodyString = data
            
    def gotoNode( name ):
        
        c.beginUpdate()
        if positions.has_key( name ):
            posis = positions[ name ]
            if len( posis ) &gt; 1:
                tl = Tk.Toplevel()
                #tl.geometry( '%sx%s+0+0' % ( ( ms[ 0 ]/3 ) *2 , ms[ 1 ]/2 ))
                tl.title( "Select node by numeric position" )
                fr = Tk.Frame( tl )
                fr.pack()
                header = Tk.Label( fr, text='select position' )
                header.pack()
                lbox = Tk.Listbox( fr, background='white', foreground='blue' )
                lbox.pack()
                for z in xrange( len( posis ) ):
                    lbox.insert( z, z + 1 )
                lbox.selection_set( 0 )
                def setPos( event ):
                    cpos = int( lbox.nearest( event.y ) )
                    tl.withdraw()
                    tl.destroy()
                    if cpos != None:
                        gotoPosition( c, posis[ cpos ] )
                lbox.bind( '&lt;Button-1&gt;', setPos )
                geometry = tl.geometry()
                geometry = geometry.split( '+' )
                geometry = geometry[ 0 ]
                width = tl.winfo_screenwidth()/3
                height = tl.winfo_screenheight()/3
                geometry= '+%s+%s' %( width,height )
                tl.geometry( geometry )
            else:
                pos = posis[ 0 ]
                gotoPosition( c, pos )
        else:
            pos2 = c.currentPosition()
            tnd = leoNodes.tnode( '', name )
            pos = pos2.insertAfter( tnd )
            gotoPosition( c, pos )
        #c.frame.tree.expandAllAncestors( pos )
        #c.selectPosition( pos )
        #c.endUpdate()
    
    def deleteNode( name ):
        
        c.beginUpdate()
        if positions.has_key( name ):
            pos = positions[ name ]
            cpos = c.currentPosition()
            pos.doDelete( cpos )
        c.endUpdate()
    
    def renameNode( name ):
    
        c.beginUpdate()
        pos = c.currentPosition()
        pos.setHeadString( name )
        c.endUpdate()

        
    emacs.setBufferListGetter( buffer, buildBufferList ) #This gives the Emacs instance the ability to get a buffer list
    emacs.setBufferSetter( buffer, setBufferData )# This gives the Emacs instance the ability to set a tnodes bodyString
    emacs.setBufferGoto( buffer, gotoNode )# This gives the Emacs instance the ability to jump to a node
    emacs.setBufferDelete( buffer, deleteNode )# This gives the Emacs instance the ability to delete a node
    emacs.setBufferRename( buffer, renameNode )# This gives the Emacs instance the ability to rename the current node

</t>
<t tx="mork.20041103161202">def chooseBuffer( self, event ):
    
    svar, label = self.getSvarLabel( event )

    state = self.mcStateManager.getState( 'chooseBuffer' )
    if state.startswith( 'start' ):
        state = state[ 5: ]
        self.mcStateManager.setState( 'chooseBuffer', state )
        svar.set( '' )
    if event.keysym == 'Tab':
        
        stext = svar.get().strip()
        if self.bufferTracker.prefix and stext.startswith( self.bufferTracker.prefix ):
            svar.set( self.bufferTracker.next() ) #get next in iteration
        else:
            prefix = svar.get()
            pmatches = []
            for z in self.bufferDict.keys():
                if z.startswith( prefix ):
                    pmatches.append( z )
            self.bufferTracker.setTabList( prefix, pmatches )
            svar.set( self.bufferTracker.next() ) #begin iteration on new lsit
        return 'break'        

        
    elif event.keysym == 'Return':
       
       bMode = self.mcStateManager.getState( 'chooseBuffer' )
       return self.bufferCommands[ bMode ]( event, svar.get() )
        
        
    else:
        self.setSvar( event, svar )
        return 'break'

</t>
<t tx="mork.20041103161202.1">def setInBufferMode( self, event, which ):
    
    self.keyboardQuit( event )
    tbuffer = event.widget
    self.mcStateManager.setState( 'chooseBuffer', 'start%s' % which )
    svar, label = self.getSvarLabel( event )
    label.configure( background = 'lightblue' )
    svar.set( 'Choose Buffer Name:' )
    self.bufferDict = self.getBufferDict( event )
    return 'break'</t>
<t tx="mork.20041103162147">def setBufferData( self, event, name, data ):
    
    tbuffer = event.widget
    meth = self.bufferSetters[ tbuffer ]
    meth( name, data )</t>
<t tx="mork.20041103190332">def listBuffers( self, event ):
    
    bdict  = self.getBufferDict( event )
    list = bdict.keys()
    list.sort()
    svar, label = self.getSvarLabel( event )
    data = '\n'.join( list )
    self.keyboardQuit( event )
    svar.set( data )
    return 'break'
    </t>
<t tx="mork.20041103191311">def setBufferGoto( self, tbuffer, method ):
    self.bufferGotos[ tbuffer ] = method </t>
<t tx="mork.20041103191311.1">def switchToBuffer( self, event, name ):
    
    method = self.bufferGotos[ event.widget ]
    self.keyboardQuit( event )
    method( name )
    return 'break'
</t>
<t tx="mork.20041104090224">def setBufferDelete( self, tbuffer, method ):
    
    self.bufferDeletes[ tbuffer ] = method
    

</t>
<t tx="mork.20041104090224.1">def killBuffer( self, event, name ):
    
    method = self.bufferDeletes[ event.widget ]
    self.keyboardQuit( event )
    method( name )
    return 'break'
    

</t>
<t tx="mork.20041104092058">def renameBuffer( self, event ):
    
    svar, label = self.getSvarLabel( event )
    if not self.mcStateManager.getState( 'renameBuffer' ):
        self.mcStateManager.setState( 'renameBuffer', True )
        svar.set( '' )
        label.configure( background = 'lightblue' )
        return 'break'
    if event.keysym == 'Return':
       
       nname = svar.get()
       self.keyboardQuit( event )
       self.renameBuffers[ event.widget ]( nname )
        
        
    else:
        self.setSvar( event, svar )
        return 'break'</t>
<t tx="mork.20041104092349">def setBufferRename( self, buffer, method ):
    
    self.renameBuffers[ buffer ] = method</t>
<t tx="mork.20041104094826">@others</t>
<t tx="mork.20041104094826.1">@others</t>
<t tx="mork.20041104095745">@
Alt-x is the mechanism by which the user should be able to access any command in the Emacs instance.
The first steps in developing temacs was focused on the keystrokes.  Though in reality the keystrokes
are just ways to access the commands.

To initiate a command type Alt-x
Start typing the command name
Press Tab.  If the command does not come up, continue pressing Tab.
If you placed the correct prefix in the minibuffer, eventually the command will appear.


This will help a user to quickly cycle through commands and select the one they want, even if they can somewhat remember what
the spelling is.</t>
<t tx="mork.20041104100514">@

Hard to say at this point.  usetemacs is essentially the glue between Leo and temacs.py.  Anytime
temacs needs some machinery from the surrounding environment, usetemacs.py is supposed to supply it.
temacs development drives this development.
</t>
<t tx="mork.20041104100856">@
In the plugins directory there should be a subdirectory called: temacs_ext.
usetemacs will add that directory to the import list.


This keeps temacs extensions separate from regular plugins.

usetemacs creates this directory for the user if it doesn't alread exist upon startup.

</t>
<t tx="mork.20041104102456">@others
</t>
<t tx="mork.20041104145603">def initialise():
    '''This fuction sets up the module'''
    def createBindings (self,frame): 
     
        if not labels.has_key( frame ):
            #group = Pmw.Group( frame.split2Pane2, tag_text = 'mini buffer' )
            group = Tk.Frame( frame.split2Pane2 , 
                              relief = 'ridge', 
                              borderwidth = 3 )
            f2 = Tk.Frame( group )
            f2.pack( side = 'top', fill = 'x' )
            gtitle = Tk.Label( f2, 
                               text = 'mini-buffer' , 
                               justify = 'left' , 
                               anchor = 'nw',
                               foreground = 'blue',
                               background = 'white' )
            #gtitle.pack( side = 'top', fill ='x' )
            #gtitle.place( x = 5, y = 10 )
            group.pack( side = 'bottom', fill = 'x', expand = 1 )
            #gtitle.place( x = 0, y = 0 , relwidth = 1.0, relheight = 1.0 )
            #gtitle.grid( columnspan = 5 )
            for z in frame.split2Pane2.children.values():
                group.pack_configure( before = z )
            label = Tk.Label( group , 
                              relief = 'groove',
                              justify = 'left',
                              anchor='w',
                               )
            label.pack( side = 'bottom', fill = 'both', expand = 1, padx = 2, pady = 2 )   
            gtitle.pack( side = 'left' ) #, fill ='x' )
            #label.place( x = 10, y = 10 )
            #label.grid( column =2, columnspan = 15, rowspan = 3 )
            labels[ frame ] = label  
        else:
            label = labels[ frame ]
            
        orig_Bindings( self, frame )
        Emacs = temacs.Emacs( frame.bodyCtrl, label, useGlobalKillbuffer = True, useGlobalRegisters = True )
        Emacs.setUndoer( frame.bodyCtrl, self.c.undoer.undo ) 
        Emacs.setTailEnd( frame.bodyCtrl, lambda buffer, frame = frame: utTailEnd( buffer, frame ) )
        Emacs.setShutdownHook( self.c.close )
        addTemacsExtensions( Emacs )
        addTemacsAbbreviations( Emacs )
        addLeoCommands( self.c, Emacs )
        changeKeyStrokes( Emacs, frame.bodyCtrl )
        setBufferInteractionMethods( self.c, Emacs, frame.bodyCtrl )
                
        orig_del = frame.bodyCtrl.delete
        def wD( i, j = None, Emacs = Emacs, orig_del = orig_del, Text = frame.bodyCtrl ):
                return watchDelete( i,j, Emacs, orig_del, Text )
        frame.bodyCtrl.delete = wD

    return createBindings</t>
<t tx="mork.20041120195951">def suspend( self, event ):
    
    widget = event.widget
    widget.winfo_toplevel().iconify()
</t>
<t tx="mork.20041120222336">def shutdown( self, event ):
    
    self.shuttingdown = True
    if self.shutdownhook:
        self.shutdownhook()
    else:
        sys.exit( 0 )</t>
<t tx="mork.20041120223251">@others</t>
<t tx="mork.20041120223251.1">def setShutdownHook( self, hook ):
        
    self.shutdownhook = hook</t>
<t tx="mork.20041121103034">@
For the re-search-backward and re-search-forward Alt-x commands

@c



@others</t>
<t tx="mork.20041121103034.1">def reStart( self, event, which='forward' ):
    self.keyboardQuit( event )
    tbuffer = event.widget
    self.mcStateManager.setState( 're_search', 'start%s' % which )
    svar, label = self.getSvarLabel( event )
    label.configure( background = 'lightblue' )
    svar.set( 'RE Search:' )
    return 'break'
</t>
<t tx="mork.20041121103034.2">def re_search( self, event ):
    svar, label = self.getSvarLabel( event )

    state = self.mcStateManager.getState( 're_search' )
    if state.startswith( 'start' ):
        state = state[ 5: ]
        self.mcStateManager.setState( 're_search', state )
        svar.set( '' )
       

        
    if event.keysym == 'Return':
       
        tbuffer = event.widget
        pattern = svar.get()
        cpattern = re.compile( pattern )
        end = None
        if state == 'forward':
            
            txt = tbuffer.get( 'insert', 'end' )
            match = cpattern.search( txt )
            end = match.end()
        
        else:

            txt = tbuffer.get( '1.0', 'insert' ) #initially the reverse words formula for Python Cookbook was going to be used.
            a = re.split( pattern, txt )         #that didnt quite work right.  This one apparently does.   
            if len( a ) &gt; 1:
                b = re.findall( pattern, txt )
                end = len( a[ -1 ] ) + len( b[ -1 ] )
        
        if end:
            
            wdict ={ 'forward': 'insert +%sc', 'backward': 'insert -%sc' }
                
            tbuffer.mark_set( 'insert', wdict[ state ] % end )                                
            self._tailEnd( tbuffer )
            tbuffer.see( 'insert' )
            
        return self.keyboardQuit( event )    
        
        
    else:
        self.setSvar( event, svar )
        return 'break'

</t>
<t tx="mork.20041121125455">def useRegex( self ):

    isearch = self.mcStateManager.getState( 'isearch' )
    risearch = False
    if isearch != 'normal':
        risearch=True
    return risearch</t>
<t tx="mork.20041121140620">@
the diff command, accessed by Alt-x diff.  Creates a buffer and puts the diff between 2 files into it.

@c


@others</t>
<t tx="mork.20041121140620.1">def diff( self, event ):
    
    try:
        f, name = self.getReadableTextFile()
        txt1 = f.read()
        f.close()
        
        f2, name2 = self.getReadableTextFile()
        txt2 = f2.read()
        f2.close()
    except:
        return self.keyboardQuit( event )
    
    
    self.switchToBuffer( event, "*diff* of ( %s , %s )" %( name, name2 ) )
    import difflib
    data = difflib.ndiff( txt1, txt2 )
    idata = []
    for z in data:
        idata.append( z )
    tbuffer = event.widget
    tbuffer.delete( '1.0', 'end' )
    tbuffer.insert( '1.0', ''.join( idata ) )
    self._tailEnd( tbuffer )
    return self.keyboardQuit( event )
</t>
<t tx="mork.20041121140620.2">def getReadableTextFile( self ):
    
    import tkFileDialog
    fname = tkFileDialog.askopenfilename()
    if fname == None: return None, None
    f = open( fname, 'rt' )
    return f, fname
</t>
<t tx="mork.20041121195816">def whatLine( self, event ):
    
    tbuffer = event.widget
    svar, label = self.getSvarLabel( event )
    i = tbuffer.index( 'insert' )
    i1, i2 = i.split( '.' )
    self.keyboardQuit( event )
    svar.set( "Line %s" % i1 )
</t>
<t tx="mork.20041121201041">@

flush-lines
Delete each line that contains a match for regexp, operating on the text after point. In Transient Mark mode, if the region is active, the command operates on the region instead.


keep-lines
Delete each line that does not contain a match for regexp, operating on the text after point. In Transient Mark mode, if the region is active, the command operates on the region instead.

@c

@others</t>
<t tx="mork.20041121201041.1">def alterLines( self, event, which ):
    
    tbuffer = event.widget
    i = tbuffer.index( 'insert' )
    end = 'end'
    if tbuffer.tag_ranges( 'sel' ):
        i = tbuffer.index( 'sel.first' )
        end = tbuffer.index( 'sel.last' )
        
    txt = tbuffer.get( i, end )
    tlines = txt.splitlines( True )
    if which == 'flush':
        keeplines = list( tlines )
    else:
        keeplines = []
    svar, label = self.getSvarLabel( event )
    pattern = svar.get()
    try:
        regex = re.compile( pattern )
        for n , z in enumerate( tlines ):
            f = regex.findall( z )
            if which == 'flush' and f:
                keeplines[ n ] = None
            elif f:
                keeplines.append( z )
    except Exception,x:
        return
    
    if which == 'flush':
        keeplines = [ x for x in keeplines if x != None ]
    tbuffer.delete( i, end )
    tbuffer.insert( i, ''.join( keeplines ) )
    tbuffer.mark_set( 'insert', i )
    self._tailEnd( tbuffer )
        
    



</t>
<t tx="mork.20041121201112">def startLines( self , event, which = 'flush' ):

    self.keyboardQuit( event )
    tbuffer = event.widget
    self.mcStateManager.setState( 'alterlines', 'start%s' % which )
    svar, label = self.getSvarLabel( event )
    label.configure( background = 'lightblue' )
    return 'break'
    
</t>
<t tx="mork.20041121210221">def processLines( self, event ):
    svar, label = self.getSvarLabel( event )

    state = self.mcStateManager.getState( 'alterlines' )
    if state.startswith( 'start' ):
        state = state[ 5: ]
        self.mcStateManager.setState( 'alterlines', state )
        svar.set( '' )
       

        
    if event.keysym == 'Return':
       
        self.alterLines( event, state )
            
        return self.keyboardQuit( event )    
        
        
    else:
        self.setSvar( event, svar )
        return 'break'</t>
<t tx="mork.20041122110739">@others</t>
<t tx="mork.20041122110739.1">def makeDirectory( self, event ):
    
    svar,label = self.getSvarLabel( event )
    state = self.mcStateManager.getState( 'make_directory' )
    if not state:
        self.mcStateManager.setState( 'make_directory', True )
        self.setLabelBlue( label )
        directory = os.getcwd()
        svar.set( '%s%s' %( directory, os.sep ) )
        return 'break'
    
    if event.keysym == 'Return':
        
        ndirectory = svar.get()
        self.keyboardQuit( event )
        try:
            os.mkdir( ndirectory )
        except:
            svar.set( "Could not make %s%" % ndirectory  )
        return 'break'
    else:
        self.setSvar( event, svar )
        return 'break'</t>
<t tx="mork.20041122111431">def removeDirectory( self, event ):
    
    svar,label = self.getSvarLabel( event )
    state = self.mcStateManager.getState( 'remove_directory' )
    if not state:
        self.mcStateManager.setState( 'remove_directory', True )
        self.setLabelBlue( label )
        directory = os.getcwd()
        svar.set( '%s%s' %( directory, os.sep ) )
        return 'break'
    
    if event.keysym == 'Return':
        
        ndirectory = svar.get()
        self.keyboardQuit( event )
        try:
            os.rmdir( ndirectory )
        except:
            svar.set( "Could not remove %s%" % ndirectory  )
        return 'break'
    else:
        self.setSvar( event, svar )
        return 'break'</t>
<t tx="mork.20041122112210">def deleteFile( self, event ):

    svar,label = self.getSvarLabel( event )
    state = self.mcStateManager.getState( 'delete_file' )
    if not state:
        self.mcStateManager.setState( 'delete_file', True )
        self.setLabelBlue( label )
        directory = os.getcwd()
        svar.set( '%s%s' %( directory, os.sep ) )
        return 'break'
    
    if event.keysym == 'Return':
        
        dfile = svar.get()
        self.keyboardQuit( event )
        try:
            os.remove( dfile )
        except:
            svar.set( "Could not delete %s%" % dfile  )
        return 'break'
    else:
        self.setSvar( event, svar )
        return 'break'
</t>
<t tx="mork.20041122151944">@
originally when this project started it was not envisioned that there would be that many emacs like commands and stuff implemented.
But then things changed, it grew.  At one point there were too many functions for the module to be flexible and understandable anymore.

The first reaction in the development was to decompose the pure module approach to an object approach.  This has helped immensely in
making temacs more manageable.  But, an Emacs instance now has over 200+ methods in it.  If it continues to grow, there may be
the need to decompose the families of methods into their own objects.  This could have two benefits:
1. More intellectually managable.
2. Swapable functionality.  Though its possible to do so now with python, this could be made much easier by having all
calls to a certain family be made through the __call__ operator.  Then swaping could be simply done by changing the object
the call is made to.


We will see if this approach may be taken.  At this point I can say for certain that the original pure functional design was a mistake, but one that was correctable by using Leo and pychecker.  Without these 2 tools, I think it may have been better to start over from scratch.
</t>
<t tx="mork.20041122152311">@
Ive noticed a general strategy that works for adding commands that need state to develop.

1. Create a start method.  This sets the mcStateManager into a specific state
2. Create a process method.  This watches events as they happen in the state
3. Create endpoint methods. These perform the final steps in processing the stateful command.


This general strategy works well so far.  A whole family of methods can be created in this manner.  Steps 1 and 2
could be combined but at a cost of more complexity, so Id recommend keeping them separate.
</t>
<t tx="mork.20041122154604">@
Accessed by Control-s Enter or Control-r Enter.  Alt-x forward-search or backward-search, just looks for words...


@c


@others</t>
<t tx="mork.20041122154604.1">def nonincrSearch( self, event, stroke ):
    
    if event.keysym in ('Control_L', 'Control_R' ): return
    state = self.mcStateManager.getState( 'nonincr-search' )
    svar, label = self.getSvarLabel( event )
    if state.startswith( 'start' ):
        state = state[ 5: ]
        self.mcStateManager.setState( 'nonincr-search', state )
        svar.set( '' )
        
    if svar.get() == '' and stroke=='&lt;Control-w&gt;':
        return self.startWordSearch( event, state )
    
    if event.keysym == 'Return':
        
        tbuffer = event.widget
        i = tbuffer.index( 'insert' )
        word = svar.get()
        if state == 'for':
            s = tbuffer.search( word, i , stopindex = 'end' )
            if s:
                s = tbuffer.index( '%s +%sc' %( s, len( word ) ) )
        else:            
            s = tbuffer.search( word,i, stopindex = '1.0', backwards = True )
            
        if s:
            tbuffer.mark_set( 'insert', s )    
        self.keyboardQuit( event )
        return self._tailEnd( tbuffer )        
            
    else:
        self.setSvar( event, svar )
        return 'break'


</t>
<t tx="mork.20041122155708">def startNonIncrSearch( self, event, which ):
    
    self.keyboardQuit( event )
    tbuffer = event.widget
    self.mcStateManager.setState( 'nonincr-search', 'start%s' % which )
    svar, label = self.getSvarLabel( event )
    self.setLabelBlue( label )
    svar.set( 'Search:' )
    return 'break'
</t>
<t tx="mork.20041122171601">@

Control-s(r) Enter Control-w words Enter, pattern entered is treated as a regular expression.

for example in the buffer we see:
    cats......................dogs
if we are after this and we enter the backwards look, search for 'cats dogs' if will take us to the match.

@c

@others</t>
<t tx="mork.20041122171601.1">def startWordSearch( self, event, which ):

    self.keyboardQuit( event )
    tbuffer = event.widget
    self.mcStateManager.setState( 'word-search', 'start%s' % which )
    svar, label = self.getSvarLabel( event )
    self.setLabelBlue( label )
    if which == 'bak':
        txt = 'Backward'
    else:
        txt = 'Forward'
    svar.set( 'Word Search %s:' % txt ) 
    return 'break'
</t>
<t tx="mork.20041122171601.2">def wordSearch( self, event ):

    state = self.mcStateManager.getState( 'word-search' )
    svar, label = self.getSvarLabel( event )
    if state.startswith( 'start' ):
        state = state[ 5: ]
        self.mcStateManager.setState( 'word-search', state )
        svar.set( '' )
        
    
    if event.keysym == 'Return':
        
        tbuffer = event.widget
        i = tbuffer.index( 'insert' )
        words = svar.get().split()
        sep = '[%s%s]+' %( string.punctuation, string.whitespace )
        pattern = sep.join( words )
        cpattern = re.compile( pattern )
        if state == 'for':
            
            txt = tbuffer.get( 'insert', 'end' )
            match = cpattern.search( txt )
            if not match: return self.keyboardQuit( event )
            end = match.end()
            
        else:            
            txt = tbuffer.get( '1.0', 'insert' ) #initially the reverse words formula for Python Cookbook was going to be used.
            a = re.split( pattern, txt )         #that didnt quite work right.  This one apparently does.   
            if len( a ) &gt; 1:
                b = re.findall( pattern, txt )
                end = len( a[ -1 ] ) + len( b[ -1 ] )
            else:
                return self.keyboardQuit( event )
            
        wdict ={ 'for': 'insert +%sc', 'bak': 'insert -%sc' }
        
        tbuffer.mark_set( 'insert', wdict[ state ] % end )                                
        tbuffer.see( 'insert' )    
        self.keyboardQuit( event )
        return self._tailEnd( tbuffer )        
            
    else:
        self.setSvar( event, svar )
        return 'break'</t>
<t tx="mork.20041122190403">@
A tremendous variety of searching methods are available.

@c


@others</t>
<t tx="mork.20041122223754">def executeLastAltX( self, event ):
    
    if event.keysym == 'Return' and self.altx_history:
        last = self.altx_history[ 0 ]
        self.doAltX[ last ]( event )
        return 'break'
    else:
        return self.keyboardQuit( event )
</t>
<t tx="mork.20041122225107">def repeatComplexCommand( self, event ):

    self.keyboardQuit( event )
    if self.altx_history:
        svar, label = self.getSvarLabel( event )
        self.setLabelBlue( label )
        svar.set( "Redo: %s" % self.altx_history[ 0 ] )
        self.mcStateManager.setState( 'last-altx', True )
    return 'break'
</t>
<t tx="mork.20041123093234">@others</t>
<t tx="mork.20041123095123">def activateReplaceRegex( self ):
    '''This method turns regex replace on for replaceString'''
    self._useRegex = True
    return True
    

</t>
<t tx="mork.20041123095436">@
both commands use the replaceString method, differentiated by a state variable

@c


@others</t>
<t tx="mork.20041123095507">@others</t>
<t tx="mork.20041123113640">def startRegexReplace( self ):
    
    self.querytype = 'regex'
    return True
</t>
<t tx="mork.20041123150144">@
Using python regular expressions and the Text widget may seem difficult but in reality it is very easy.
A simple formula:
1. get the text you are interested in from the Text widget.
2. Do a python regex on it, get the start value from the match object: match.start()
3. This gives you the position in the text widget where the regex matched.  Change the 'insert' point
in the Text like so:

tbuffer.mark_set( 'insert', 'insert +%sc' % match.start() )


this will change the insert point to where the match started.  Since you can move forward in the Text widget
by the character amount, bridging python regexes and Text is a simple operation.
  Need to go after the match, just use
match.end() instead of match.start().

I puzzled over this for awhile, so this note is a reminder that it is easy.  See the implementation for query-replace-regex for
an example.  Doing this with just plain string can follow a similar pattern.

@c</t>
<t tx="mork.20041123150836">@

just a short note to anyone, including myself, that is working on temacs.  Currently all( well all the ones that we have registered interest in ) key events get
routed through:

def masterCommand( self, event, method , stroke):


to understand the flow of the Emacs class, you need to understand this method.  Everything goes through it, there are no sidecuts or anything.  This offers the implementor complete control over what happens, and for the stateful commands it is essential to
keep states from being corrupted.


dont mess with this method lightly.
</t>
<t tx="mork.20041123192555">@others</t>
<t tx="mork.20041123192555.1">def watchEscape( self, event ):
    
    svar, label = self.getSvarLabel( event )
    if not self.mcStateManager.hasState():
        self.mcStateManager.setState( 'escape' , 'start' )
        self.setLabelBlue( label )
        svar.set( 'Esc' )
        return 'break'
    if self.mcStateManager.whichState() == 'escape':
        
        state = self.mcStateManager.getState( 'escape' )
        hi1 = self.keysymhistory[ 0 ]
        hi2 = self.keysymhistory[ 1 ]
        if state == 'esc esc' and event.keysym == 'colon':
            return self.startEvaluate( event )
        elif state == 'evaluate':
            return self.escEvaluate( event )    
        elif hi1 == hi2 == 'Escape':
            self.mcStateManager.setState( 'escape', 'esc esc' )
            svar.set( 'Esc Esc -' )
            return 'break'
        elif event.keysym in ( 'Shift_L', 'Shift_R' ):
            return
        else:
            return self.keyboardQuit( event )
    


</t>
<t tx="mork.20041124094511">def whichState( self ):
    
    return self.state
</t>
<t tx="mork.20041124095452">def escEvaluate( self, event ):
    
    svar, label = self.getSvarLabel( event )
    if svar.get() == 'Eval:':
        svar.set( '' )
    
    if event.keysym =='Return':
    
        expression = svar.get()
        try:
            ok = False
            tbuffer = event.widget
            result = eval( expression, {}, {} )
            result = str( result )
            tbuffer.insert( 'insert', result )
            ok = True
        finally:
            self.keyboardQuit( event )
            if not ok:
                svar.set( 'Error: Invalid Expression' )
            return self._tailEnd( tbuffer )
        
        
    else:
        
        self.setSvar( event, svar )
        return 'break'
    
</t>
<t tx="mork.20041124102729">def startEvaluate( self, event ):
    
    svar, label = self.getSvarLabel( event )
    self.setLabelBlue( label )
    svar.set( 'Eval:' )
    self.mcStateManager.setState( 'escape', 'evaluate' )
    return 'break'
</t>
<t tx="mork.20041124123825">@
For the tabify and untabify Alt-x commands.  Turns tabs to spaces and spaces to tabs in the selection

@c


@others</t>
<t tx="mork.20041124123825.1">def tabify( self, event, which='tabify' ):
    
    tbuffer = event.widget
    if tbuffer.tag_ranges( 'sel' ):
        i = tbuffer.index( 'sel.first' )
        end = tbuffer.index( 'sel.last' )
        txt = tbuffer.get( i, end )
        if which == 'tabify':
            
            pattern = re.compile( ' {4,4}' )
            ntxt = pattern.sub( '\t', txt )

        else:
            
            pattern = re.compile( '\t' )
            ntxt = pattern.sub( '    ', txt )
        tbuffer.delete( i, end )
        tbuffer.insert( i , ntxt )
        self.keyboardQuit( event )
        return self._tailEnd( tbuffer )
    self.keyboardQuit( event )

</t>
<t tx="mork.20041124130434">def indent_relative( self, event ):
    
    tbuffer = event.widget
    i = tbuffer.index( 'insert' )
    l,c = i.split( '.' )
    c2 = int( c )
    l2 = int( l ) - 1
    if l2 &lt; 1: return self.keyboardQuit( event )
    txt = tbuffer.get( '%s.%s' % (l2, c2 ), '%s.0 lineend' % l2 )
    if len( txt ) &lt;= len( tbuffer.get( 'insert', 'insert lineend' ) ):
        tbuffer.insert(  'insert', '\t' )
    else:
        reg = re.compile( '(\s+)' )
        ntxt = reg.split( txt )
        replace_word = re.compile( '\w' )
        for z in ntxt:
            if z.isspace():
                tbuffer.insert( 'insert', z )
                break
            else:
                z = replace_word.subn( ' ', z )
                tbuffer.insert( 'insert', z[ 0 ] )
                tbuffer.update_idletasks()
        
        
    self.keyboardQuit( event )
    return self._tailEnd( tbuffer )
</t>
<t tx="mork.20041126091717">@

I believe in .7 the transition from one big Emacs object to an Emacs object composed of many method-family objects
will begin.  This may be as a big as a transition as the change from the flat module structure to the Emacs class based
structure.  The .6 cycle Ill reserve for improving the functionality and documentation.  The current command crop may be
froze in that cycle.</t>
<t tx="mork.20041204141826">def addLeoCommands( c, emacs ):
    
    global leocommandnames
    f = c.frame
    
    commands = {
    'new': c.new,
    'open': c.open,
    'openWith': c.openWith,
    'close': c.close,
    'save': c.save,
    'saveAs': c.saveAs,
    'saveTo': c.saveTo,
    'revert': c.revert,
    'readOutlineOnly': c.readOutlineOnly,
    'readAtFileNodes': c.readAtFileNodes,
    'importDerivedFile': c.importDerivedFile,
    #'writeNewDerivedFiles': c.writeNewDerivedFiles,
    #'writeOldDerivedFiles': c.writeOldDerivedFiles,
    'tangle': c.tangle,
    'tangle all': c.tangleAll,
    'tangle marked': c.tangleMarked,
    'untangle': c.untangle,
    'untangle all': c.untangleAll,
    'untangle marked': c.untangleMarked,
    'export headlines': c.exportHeadlines,
    'flatten outline': c.flattenOutline,
    'import AtRoot': c.importAtRoot,
    'import AtFile': c.importAtFile,
    'import CWEB Files': c.importCWEBFiles,
    'import Flattened Outline': c.importFlattenedOutline,
    'import Noweb Files': c.importNowebFiles,
    'outline to Noweb': c.outlineToNoweb,
    'outline to CWEB': c.outlineToCWEB,
    'remove sentinels': c.removeSentinels,
    'weave': c.weave,
    'delete': c.delete,
    'execute script': c.executeScript,
    'go to line number': c.goToLineNumber,
    'set font': c.fontPanel,
    'set colors': c.colorPanel,
    'show invisibles': c.viewAllCharacters,
    'preferences': c.preferences,
    'convert all blanks': c.convertAllBlanks,
    'convert all tabs': c.convertAllTabs,
    'convert blanks': c.convertBlanks,
    'convert tabs': c.convertTabs,
    'indent': c.indentBody,
    'unindent': c.dedentBody,
    'reformat paragraph': c.reformatParagraph,
    'insert time': c.insertBodyTime,
    'extract section': c.extractSection,
    'extract names': c.extractSectionNames,
    'extract': c.extract,
    'match bracket': c.findMatchingBracket,
    'find panel': c.showFindPanel, ## c.findPanel,
    'find next': c.findNext,
    'find previous': c.findPrevious,
    'replace': c.replace,
    'replace then find': c.replaceThenFind,
    'edit headline': c.editHeadline,
    'toggle angle brackets': c.toggleAngleBrackets,
    'cut node': c.cutOutline,
    'copy node': c.copyOutline,
    'paste node': c.pasteOutline,
    'paste retaining clone': c.pasteOutlineRetainingClones,
    'hoist': c.hoist,
    'de-hoist': c.dehoist,
    'insert node': c.insertHeadline,
    'clone node': c.clone,
    'delete node': c.deleteOutline,
    'sort children': c.sortChildren,
    'sort siblings': c.sortSiblings,
    'demote': c.demote,
    'promote': c.promote,
    'move right': c.moveOutlineRight,
    'move left': c.moveOutlineLeft,
    'move up': c.moveOutlineUp,
    'move down': c.moveOutlineDown,
    'unmark all': c.unmarkAll,
    'mark clones': c.markClones,
    'mark': c.markHeadline,
    'mark subheads': c.markSubheads,
    'mark changed items': c.markChangedHeadlines,
    'mark changed roots': c.markChangedRoots,
    'contract all': c.contractAllHeadlines,
    'contract node': c.contractNode,
    'contract parent': c.contractParent,
    'expand to level 1': c.expandLevel1,
    'expand to level 2': c.expandLevel2,
    'expand to level 3': c.expandLevel3,
    'expand to level 4': c.expandLevel4,
    'expand to level 5': c.expandLevel5,
    'expand to level 6': c.expandLevel6,
    'expand to level 7': c.expandLevel7,
    'expand to level 8': c.expandLevel8,
    'expand to level 9': c.expandLevel9,
    'expand prev level': c.expandPrevLevel,
    'expand next level': c.expandNextLevel,
    'expand all': c.expandAllHeadlines,
    'expand node': c.expandNode,
    'check outline': c.checkOutline,
    'dump outline': c.dumpOutline,
    'check python code': c.checkPythonCode,
    'check all python code': c.checkAllPythonCode,
    'pretty print python code': c.prettyPrintPythonCode,
    'pretty print all python code': c.prettyPrintAllPythonCode,
    'goto parent': c.goToParent,
    'goto next sibling': c.goToNextSibling,
    'goto previous sibling': c.goToPrevSibling,
    'goto next clone': c.goToNextClone,
    'goto next marked': c.goToNextMarkedHeadline,
    'goto next changed': c.goToNextDirtyHeadline,
    'goto first': c.goToFirstNode,
    'goto last': c.goToLastNode,
    "go to prev visible":c.selectVisBack,
    "go to next visible" : c.selectVisNext,
    "go to prev node" : c.selectThreadBack,
    "go to next node" : c.selectThreadNext,
    'about leo...': c.about,
    #'apply settings': c.applyConfig,
    'open LeoConfig.leo': c.leoConfig,
    'open LeoDocs.leo': c.leoDocumentation,
    'open online home': c.leoHome,
    'open online tutorial': c.leoTutorial,
    'open compare window': c.openCompareWindow,
    'open Python window': c.openPythonWindow,
    "equal sized panes": f.equalSizedPanes,
    "toggle active pane": f.toggleActivePane,
    "toggle split direction": f.toggleSplitDirection,
    "resize to screen": f.resizeToScreen,
    "cascade": f.cascade,
    "minimize all": f.minimizeAll,
    }
    
    for z in commands.keys():
        #z2 = 'leo-%s' % z -- no need to do this, Leos command names dont clash with temacs so far
        def coverdef( self, event, command=commands[ z ] ):
            command()
            emacs.keyboardQuit( event )
            
        emacs.extendAltX( z, coverdef )
    leocommandnames = commands.keys()
    
    






























































</t>
<t tx="mork.20041208120232">@others</t>
<t tx="mork.20041208120232.1">def startSubprocess( self, event, which = 0 ):
    
    svar, label = self.getSvarLabel( event )
    statecontents = { 'state':'start', 'payload': None }
    self.mcStateManager.setState( 'subprocess', statecontents )
    if which:
        tbuffer = event.widget
        svar.set( "Shell command on region:" )
        is1 = is2 = None
        try:
            is1 = tbuffer.index( 'sel.first' )
            is2 = tbuffer.index( 'sel.last' )
        finally:
            if is1:
                statecontents[ 'payload' ] = tbuffer.get( is1, is2 )
            else:
                return self.keyboardQuit( event )
    else:
        svar.set( "Alt - !:" )
    self.setLabelBlue( label )
    return 'break'    
</t>
<t tx="mork.20041208120232.2">def subprocesser( self, event ):
    
    state = self.mcStateManager.getState( 'subprocess' )
    svar, label = self.getSvarLabel( event )
    if state[ 'state' ] == 'start':
        state[ 'state' ] = 'watching'
        svar.set( "" )
    
    if event.keysym == "Return":
        #cmdline = svar.get().split()
        cmdline = svar.get()
        return self.executeSubprocess( event, cmdline, input=state[ 'payload' ] )
       
    else:
        self.setSvar(  event, svar )
        return 'break'
</t>
<t tx="mork.20041208121502">def executeSubprocess( self, event, command  ,input = None ):
    import subprocess
    try:
        try:
            out ,err = os.tmpnam(), os.tmpnam()
            ofile = open( out, 'wt+' ) 
            efile = open( err, 'wt+' )
            process = subprocess.Popen( command, bufsize=-1, 
                                        stdout = ofile.fileno(), 
                                        stderr= ofile.fileno(), 
                                        stdin=subprocess.PIPE,
                                        shell=True )
            if input:
                process.communicate( input )
            process.wait()   
            tbuffer = event.widget
            efile.seek( 0 )
            errinfo = efile.read()
            if errinfo:
                tbuffer.insert( 'insert', errinfo )
            ofile.seek( 0 )
            okout = ofile.read()
            if okout:
                tbuffer.insert( 'insert', okout )
        except Exception, x:
            tbuffer = event.widget
            tbuffer.insert( 'insert', x )
    finally:
        os.remove( out )
        os.remove( err )
    self.keyboardQuit( event )
    return self._tailEnd( tbuffer )



</t>
<t tx="mork.20041213112640">def gotoPosition( c, pos ):
    c.frame.tree.expandAllAncestors( pos )
    c.selectPosition( pos )
    c.endUpdate()
    
</t>
</tnodes>
</leo_file>
