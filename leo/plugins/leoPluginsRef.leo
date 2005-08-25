<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet ekr_stylesheet?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="5874" clone_windows="0"/>
<globals body_outline_ratio="0.471882640587">
	<global_window_position top="14" left="237" height="842" width="899"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="edream.110203113231"><vh>@thin pluginsNotes.txt</vh></v>
<v t="ekr.20041211035618"><vh>Scripts, buttons &amp; settings</vh>
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
<v t="ekr.20041113110210"><vh>@button Spelling...</vh></v>
<v t="ekr.20050724100334"><vh>@button Beautify</vh></v>
<v t="ekr.20050819055746"><vh>@button Save</vh></v>
<v t="ekr.20050722075812"><vh>Remove blank trailing lines</vh></v>
</v>
<v t="edream.110203113231.618" a="TV"><vh>Plugins</vh>
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
<v t="ekr.20050130120433"><vh>@thin failed_import.py</vh></v>
<v t="edream.110203113231.730"><vh>@thin dump_globals.py</vh></v>
<v t="edream.110203113231.732"><vh>@thin enable_gc.py</vh></v>
<v t="edream.110203113231.734"><vh>@thin quit_leo.py</vh></v>
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
<v t="ekr.20050329082101.147"><vh>@thin trees\test.py</vh></v>
<v t="ekr.20050329082101.150"><vh>@thin trees\rss.py</vh></v>
<v t="ekr.20050329082101.153"><vh>@thin trees\news.py</vh></v>
<v t="ekr.20050329082101.162"><vh>@thin trees\remote.py</vh></v>
<v t="ekr.20050329082101.165"><vh>@thin trees\doc.py</vh></v>
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
<v t="ekr.20041017043622"><vh>@thin autocompleter.py</vh></v>
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
<v t="EKR.20040517075915" tnodeList="EKR.20040517075915,EKR.20040517075915.1,EKR.20040517075915.2,EKR.20040517075915.3,EKR.20040517075915.4,EKR.20040517075915.5,ekr.20050313123322,ekr.20050313123600,ekr.20050313124016,ekr.20050313123322.1,ekr.20050329033007,ekr.20050313123322.2,ekr.20050313124016.1,ekr.20050313123322.3,ekr.20050313124619,ekr.20050313124954,ekr.20050313125536,ekr.20050313123322.4,EKR.20040517075915.6,EKR.20040517075915.7,EKR.20040517075915.11,EKR.20040517075915.12,ekr.20050313123322.5,ekr.20050329033007.1,ekr.20050313120714,ekr.20050313120345,ekr.20050313115107,ekr.20050313121102,EKR.20040517075915.9,EKR.20040517075915.10,EKR.20040517075915.8,ekr.20050313124212,ekr.20050313120113"><vh>@file-noref newButtons.py</vh>
<v t="EKR.20040517075915.1"><vh>Helper classes</vh>
<v t="EKR.20040517075915.2"><vh>class FlatOptionMenu</vh></v>
<v t="EKR.20040517075915.3"><vh>class Node</vh></v>
<v t="EKR.20040517075915.4"><vh>class NodeAdder</vh></v>
<v t="EKR.20040517075915.5"><vh>class Helper</vh></v>
</v>
<v t="ekr.20050313123322"><vh>text definitions used in plugins templates</vh>
<v t="ekr.20050313123600"><vh>DOCSTRING_BODY</vh></v>
<v t="ekr.20050313124016"><vh>GENERIC_IMPORTS_BODY</vh></v>
<v t="ekr.20050313123322.1"><vh>GENERIC_INIT_FUNCTION_BODY</vh></v>
<v t="ekr.20050329033007"><vh>IMPORT_LEO_GLOBALS_BODY</vh></v>
<v t="ekr.20050313123322.2"><vh>PLUGIN_ROOT_BODY</vh></v>
<v t="ekr.20050313124016.1"><vh>TK_IMPORTS_BODY</vh></v>
<v t="ekr.20050313123322.3"><vh>TK_INIT_FUNCTION_BODY</vh></v>
<v t="ekr.20050313124619"><vh>TK_ON_CREATE_FUNCTION</vh></v>
<v t="ekr.20050313124954"><vh>TK_PLUGIN_CONTROLLER</vh></v>
<v t="ekr.20050313125536"><vh>TK_PLUGIN_CONTROLLER_INIT</vh></v>
<v t="ekr.20050313123322.4"><vh>VERSION_HISTORY_BODY</vh></v>
</v>
<v t="EKR.20040517075915.6"><vh> Casses to add buttons</vh>
<v t="EKR.20040517075915.7"><vh>body text used by AddTestModule &amp; AddTestClass</vh></v>
<v t="EKR.20040517075915.11"><vh>class AddClass</vh></v>
<v t="EKR.20040517075915.12"><vh>class AddClassMethod</vh></v>
<v t="ekr.20050313123322.5"><vh>class AddGenericPlugin</vh></v>
<v t="ekr.20050329033007.1"><vh>class AddImportLeoGlobalsFunction</vh></v>
<v t="ekr.20050313120714"><vh>class AddPluginImportsSection</vh></v>
<v t="ekr.20050313120345"><vh>class AddPluginInitFunction</vh></v>
<v t="ekr.20050313115107"><vh>class AddPluginTkInitFunction</vh></v>
<v t="ekr.20050313121102"><vh>class AddPluginVersionHistorySection</vh></v>
<v t="EKR.20040517075915.9"><vh>class AddTestClass</vh></v>
<v t="EKR.20040517075915.10"><vh>class AddTestMethod</vh></v>
<v t="EKR.20040517075915.8"><vh>class AddTestModule</vh></v>
<v t="ekr.20050313124212"><vh>class AddTkPlugin</vh></v>
</v>
<v t="ekr.20050313120113"><vh>init</vh></v>
</v>
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
<v t="ekr.20040915073637"><vh>@thin TabbedLog.py</vh></v>
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
<v t="ekr.20041002162608"><vh>Status Line (Experimental)</vh>
<v t="ekr.20040201060959"><vh>@thin status_line.py</vh></v>
</v>
<v t="ekr.20040717133342"><vh>Shadow files plugin</vh>
<v t="ekr.20050126104457"><vh>Notes</vh></v>
<v t="bwmulder.20041017125718"><vh>@thin mod_shadow.py</vh></v>
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
<v t="ekr.20050723062822"><vh>@thin __core_emacs.py</vh></v>
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
<v t="ekr.20050730194215"><vh>New Emacs Projects &amp; Notes</vh>
<v t="ekr.20050726081113"><vh>Comparing SwingMacs &amp; temacs classes</vh>
<v t="ekr.20050726081152"><vh>kill buffer</vh>
<v t="ekr.20050724075352.161"><vh>class killBufferCommandsClass</vh>
<v t="ekr.20050725115600"><vh> ctor</vh></v>
<v t="ekr.20050725121247"><vh>getPublicCommands</vh></v>
<v t="ekr.20050725120303"><vh>Entry points</vh></v>
<v t="ekr.20050724075352.162"><vh>kill</vh></v>
<v t="ekr.20050724075352.163"><vh>walkKB</vh></v>
<v t="ekr.20050724075352.164"><vh>deletelastWord</vh></v>
<v t="ekr.20050724075352.165"><vh>_killSentence</vh></v>
<v t="ekr.20050724075352.166"><vh>_killRegion</vh></v>
<v t="ekr.20050724075352.167"><vh>addToKillBuffer</vh></v>
<v t="ekr.20050724075352.168"><vh>iterateKillBuffer</vh></v>
<v t="ekr.20050724075352.169"><vh>getClipboard</vh></v>
</v>
<v t="orkman.20050210202559"><vh>killbuffer (SwingMacs)</vh>
<v t="orkman.20050212113553"><vh>kill</vh></v>
<v t="orkman.20050212114641"><vh>insertIntoKillbuffer</vh></v>
<v t="orkman.20050210202559.1"><vh>killToEndOfLine</vh></v>
<v t="orkman.20050212115022"><vh>copyRegion</vh></v>
<v t="orkman.20050212114308"><vh>killRegion</vh></v>
<v t="orkman.20050212115022.1"><vh>getRegion</vh></v>
<v t="orkman.20050212095512"><vh>walkKB</vh></v>
<v t="orkman.20050210203511"><vh>yank</vh></v>
<v t="orkman.20050212100715"><vh>iterateKillBuffer</vh></v>
<v t="orkman.20050212100208"><vh>doesClipboardOfferNewData</vh></v>
</v>
</v>
<v t="ekr.20050726081815.2"><vh>registers</vh>
<v t="ekr.20050724075352.170"><vh>class registerCommandsClass</vh>
<v t="ekr.20050725134243"><vh> ctor</vh></v>
<v t="ekr.20050725135621.1"><vh> Entry points</vh>
<v t="ekr.20050724075352.174"><vh>appendToRegister</vh></v>
<v t="ekr.20050724075352.173"><vh>prependToRegister</vh></v>
<v t="ekr.20050724075352.172"><vh>_copyRectangleToRegister</vh></v>
<v t="ekr.20050724075352.171"><vh>_copyToRegister</vh></v>
<v t="ekr.20050724075352.179"><vh>_incrementRegister</vh></v>
<v t="ekr.20050724075352.178"><vh>_insertRegister</vh></v>
<v t="ekr.20050724075352.182"><vh>_jumpToRegister</vh></v>
<v t="ekr.20050724075352.180"><vh>_numberToRegister</vh></v>
<v t="ekr.20050724075352.181"><vh>_pointToRegister</vh></v>
<v t="ekr.20050724075352.187"><vh>_viewRegister</vh></v>
</v>
<v t="ekr.20050725134243.1"><vh> getPublicCommands </vh></v>
<v t="ekr.20050726043333.1"><vh>Helpers</vh>
<v t="ekr.20050724075352.176"><vh>_chckSel</vh></v>
<v t="ekr.20050724075352.177"><vh>_checkIfRectangle</vh></v>
<v t="ekr.20050724075352.175"><vh>_ToReg</vh></v>
<v t="ekr.20050724075352.52"><vh>addRegisterItems (registerCommandsClass)</vh></v>
<v t="ekr.20050724075352.186"><vh>deactivateRegister</vh></v>
<v t="ekr.20050724075352.183"><vh>invalidRegister</vh></v>
<v t="ekr.20050724075352.184"><vh>setNextRegister</vh></v>
<v t="ekr.20050724075352.185"><vh>executeRegister</vh></v>
</v>
</v>
<v t="zorcanda!.20050312155939"><vh>registers (SwingMacs)</vh>
<v t="ekr.20050726081815"><vh>  __init__</vh></v>
<v t="ekr.20050726081815.1"><vh> __call__</vh></v>
<v t="zorcanda!.20050312160220"><vh>copy-to-register</vh></v>
<v t="zorcanda!.20050312160220.1"><vh>insert-register</vh></v>
<v t="zorcanda!.20050312171820"><vh>append-to-register</vh></v>
<v t="zorcanda!.20050312171820.1"><vh>prepend-to-register</vh></v>
</v>
</v>
<v t="ekr.20050726091527"><vh>State managers</vh>
<v t="ekr.20050724075352.43"><vh>masterCommand</vh>
<v t="ekr.20050729150051.1"><vh>&lt;&lt; handle macro &gt;&gt;</vh></v>
<v t="ekr.20050731084644"><vh>&lt;&lt; add character to history &gt;&gt;</vh></v>
</v>
<v t="orkman.20050213110511"><vh>helper classes (SwingMacs)</vh>
<v t="orkman.20050207162016"><vh>stateManager</vh></v>
<v t="orkman.20050213105021"><vh>KeyProcessor</vh>
<v t="orkman.20050213105021.1"><vh>__init__</vh></v>
<v t="zorcanda!.20050411132747"><vh>addCompleter</vh></v>
<v t="zorcanda!.20050604091924"><vh>removeCompleter</vh></v>
<v t="orkman.20050213105021.2"><vh>keyReleased</vh></v>
<v t="orkman.20050213105021.3"><vh>keyTyped</vh></v>
<v t="orkman.20050213105021.4"><vh>keyPressed</vh>
<v t="ekr.20050726094804"><vh>&lt;&lt; create the command &gt;&gt;</vh></v>
<v t="ekr.20050726094804.1"><vh>&lt;&lt; handle auto completion &gt;&gt;</vh></v>
<v t="ekr.20050726094804.2"><vh>&lt;&lt; handle auto-tabbing &gt;&gt;</vh></v>
</v>
<v t="orkman.20050213105513"><vh>insertPreviousLeadAndNewline -- for autoindentation on newline</vh>
<v t="orkman.20050213105513.1"><vh>&lt;&lt; why is this code here? &gt;&gt;</vh></v>
</v>
<v t="zorcanda!.20050522115325"><vh>calculateExtraSpaces</vh></v>
</v>
<v t="zorcanda!.20050520221746"><vh>TagMatcher</vh>
<v t="ekr.20050727082959"><vh>keyPressed</vh></v>
</v>
<v t="zorcanda!.20050310170120"><vh>TabCompleter</vh>
<v t="ekr.20050727083243"><vh>extend</vh></v>
<v t="ekr.20050727083243.1"><vh>lookFor</vh></v>
<v t="ekr.20050727083243.2"><vh>getNext</vh></v>
</v>
</v>
<v t="orkman.20050213110803"><vh>masterCommand (SwingMacs)</vh></v>
</v>
</v>
<v t="orkman.20050207150858"><vh>SwingMacs.py (as of 7/21) STUDY ONLY</vh>
<v t="zorcanda!.20050313115453"><vh>&lt;&lt; addCommand &gt;&gt;</vh></v>
<v t="orkman.20050210125253"><vh>What is SwingMacs?</vh></v>
<v t="orkman.20050213110948"><vh>constructor: __init__</vh></v>
<v t="zorcanda!.20050604091242"><vh>management listening</vh>
<v t="zorcanda!.20050604091242.1"><vh>addCompleters</vh></v>
<v t="zorcanda!.20050604091242.2"><vh>managementListener</vh></v>
</v>
<v t="zorcanda!.20050313142453"><vh>lookForExtensions</vh></v>
<v t="zorcanda!.20050411132825"><vh>addCompleter</vh></v>
<v t="zorcanda!.20050314142845"><vh>How to write an extension( alpha doc level )</vh></v>
<v t="orkman.20050213110511"><vh>helper classes (SwingMacs)</vh>
<v t="orkman.20050207162016"><vh>stateManager</vh></v>
<v t="orkman.20050213105021"><vh>KeyProcessor</vh>
<v t="orkman.20050213105021.1"><vh>__init__</vh></v>
<v t="zorcanda!.20050411132747"><vh>addCompleter</vh></v>
<v t="zorcanda!.20050604091924"><vh>removeCompleter</vh></v>
<v t="orkman.20050213105021.2"><vh>keyReleased</vh></v>
<v t="orkman.20050213105021.3"><vh>keyTyped</vh></v>
<v t="orkman.20050213105021.4"><vh>keyPressed</vh>
<v t="ekr.20050726094804"><vh>&lt;&lt; create the command &gt;&gt;</vh></v>
<v t="ekr.20050726094804.1"><vh>&lt;&lt; handle auto completion &gt;&gt;</vh></v>
<v t="ekr.20050726094804.2"><vh>&lt;&lt; handle auto-tabbing &gt;&gt;</vh></v>
</v>
<v t="orkman.20050213105513"><vh>insertPreviousLeadAndNewline -- for autoindentation on newline</vh>
<v t="orkman.20050213105513.1"><vh>&lt;&lt; why is this code here? &gt;&gt;</vh></v>
</v>
<v t="zorcanda!.20050522115325"><vh>calculateExtraSpaces</vh></v>
</v>
<v t="zorcanda!.20050520221746"><vh>TagMatcher</vh>
<v t="ekr.20050727082959"><vh>keyPressed</vh></v>
</v>
<v t="zorcanda!.20050310170120"><vh>TabCompleter</vh>
<v t="ekr.20050727083243"><vh>extend</vh></v>
<v t="ekr.20050727083243.1"><vh>lookFor</vh></v>
<v t="ekr.20050727083243.2"><vh>getNext</vh></v>
</v>
</v>
<v t="ekr.20050722082741"><vh>Strategy stuff...</vh>
<v t="orkman.20050213110235"><vh>defineStrategyObjects</vh></v>
<v t="orkman.20050213110404"><vh>defineStrategiesForKeystrokes</vh></v>
<v t="zorcanda!.20050417172712"><vh>addCommands</vh></v>
</v>
<v t="orkman.20050213110803"><vh>masterCommand (SwingMacs)</vh></v>
<v t="orkman.20050223114739"><vh>setCommandText</vh></v>
<v t="orkman.20050210204001"><vh>help</vh></v>
<v t="zorcanda!.20050418121158"><vh>add*Help</vh></v>
<v t="orkman.20050207164014"><vh>keyboardQuit</vh></v>
<v t="zorcanda!.20050311123715"><vh>beep</vh></v>
<v t="zorcanda!.20050311140549"><vh>determineLanguage</vh></v>
<v t="zorcanda!.20050312123359"><vh>getTabWidth</vh></v>
<v t="orkman.20050207164550"><vh>eventToMinibuffer</vh></v>
<v t="orkman.20050209165908"><vh>text operations</vh></v>
<v t="orkman.20050209170444"><vh>word operations</vh></v>
<v t="orkman.20050210105230"><vh>findPre</vh></v>
<v t="orkman.20050209180255"><vh>attribute and highlight operations</vh></v>
<v t="zorcanda!.20050528101434"><vh>addToKillBuffer</vh></v>
<v t="orkman.20050210110555"><vh>Stategies for keystroke and commands</vh>
<v t="orkman.20050207152619"><vh>incremental search</vh>
<v t="orkman.20050210110734"><vh>startIncremental</vh></v>
<v t="orkman.20050210110734.1"><vh>incrementalSearch</vh></v>
<v t="orkman.20050223124157"><vh>forward and backward search</vh></v>
<v t="zorcanda!.20050720215058"><vh>class deferedHighlight</vh></v>
</v>
<v t="orkman.20050209165307"><vh>dynamic-abbrevs</vh>
<v t="orkman.20050209165621"><vh>dynamicExpansion</vh></v>
<v t="orkman.20050209165627"><vh>dynamicExpansion2</vh></v>
<v t="orkman.20050209165908.1"><vh>getDynamicList</vh></v>
<v t="orkman.20050209215951"><vh>clearDynamic</vh></v>
<v t="zorcanda!.20050720141603"><vh>createDynamicList</vh></v>
</v>
<v t="zorcanda!.20050527190231"><vh>symbolcompletion</vh></v>
<v t="orkman.20050210201413"><vh>formatter</vh>
<v t="orkman.20050210201413.1"><vh>indent-region</vh></v>
<v t="zorcanda!.20050312121738"><vh>indent-rigidly</vh></v>
<v t="zorcanda!.20050312173225"><vh>indent-relative</vh></v>
<v t="zorcanda!.20050523140526"><vh>deleteSurroundingSpaces</vh></v>
<v t="zorcanda!.20050523141645"><vh>joinLineToPrevious</vh></v>
<v t="zorcanda!.20050523143816"><vh>deleteBlankLines</vh></v>
<v t="zorcanda!.20050312183416"><vh>definePreviousLine</vh></v>
</v>
<v t="orkman.20050210202559"><vh>killbuffer (SwingMacs)</vh>
<v t="orkman.20050212113553"><vh>kill</vh></v>
<v t="orkman.20050212114641"><vh>insertIntoKillbuffer</vh></v>
<v t="orkman.20050210202559.1"><vh>killToEndOfLine</vh></v>
<v t="orkman.20050212115022"><vh>copyRegion</vh></v>
<v t="orkman.20050212114308"><vh>killRegion</vh></v>
<v t="orkman.20050212115022.1"><vh>getRegion</vh></v>
<v t="orkman.20050212095512"><vh>walkKB</vh></v>
<v t="orkman.20050210203511"><vh>yank</vh></v>
<v t="orkman.20050212100715"><vh>iterateKillBuffer</vh></v>
<v t="orkman.20050212100208"><vh>doesClipboardOfferNewData</vh></v>
</v>
<v t="orkman.20050212120210"><vh>deleter</vh>
<v t="orkman.20050212120210.1"><vh>deletePreviousChar</vh></v>
<v t="orkman.20050212120620"><vh>deleteNextChar</vh></v>
</v>
<v t="orkman.20050212121301"><vh>alt_x_handler</vh>
<v t="zorcanda!.20050310184934"><vh>getCommandHelp</vh></v>
</v>
<v t="zorcanda!.20050523143029"><vh>ctrl_x_handler</vh></v>
<v t="zorcanda!.20050528193454"><vh>ctrl_u handler</vh></v>
<v t="zorcanda!.20050310144300"><vh>rectangles</vh>
<v t="zorcanda!.20050310172920"><vh>definePoints</vh></v>
<v t="zorcanda!.20050311121612"><vh>insertText</vh></v>
<v t="zorcanda!.20050310153830"><vh>open-rectangle</vh></v>
<v t="zorcanda!.20050310182257"><vh>clear-rectangle</vh></v>
<v t="zorcanda!.20050311102520"><vh>kill-rectangle</vh></v>
<v t="zorcanda!.20050311102817"><vh>yank-rectangle</vh></v>
<v t="zorcanda!.20050310172646"><vh>delete-rectangle</vh></v>
<v t="zorcanda!.20050310183117"><vh>delete-whitespace-rectangle</vh></v>
<v t="zorcanda!.20050311102030"><vh>string-rectangle</vh></v>
<v t="zorcanda!.20050311095932"><vh>string-insert-rectangle</vh></v>
</v>
<v t="zorcanda!.20050311123122"><vh>zap</vh>
<v t="zorcanda!.20050311123122.1"><vh>zap</vh></v>
</v>
<v t="zorcanda!.20050311140549.1"><vh>comment</vh>
<v t="zorcanda!.20050311140549.2"><vh>comment-region</vh></v>
<v t="zorcanda!.20050311143148"><vh>comment-kill</vh></v>
</v>
<v t="zorcanda!.20050311150743"><vh>movement</vh>
<v t="zorcanda!.20050311150743.1"><vh>beginning-of-buffer</vh></v>
<v t="zorcanda!.20050311150743.2"><vh>end-of-buffer</vh></v>
<v t="zorcanda!.20050311151807"><vh>beginning-of-line</vh></v>
<v t="zorcanda!.20050311151807.1"><vh>end-of-line</vh></v>
<v t="zorcanda!.20050311154238"><vh>goto</vh></v>
<v t="zorcanda!.20050311154238.1"><vh>gotoChar</vh></v>
<v t="zorcanda!.20050512112449"><vh>startOfWord</vh></v>
<v t="zorcanda!.20050512112449.1"><vh>endOfWord</vh></v>
<v t="zorcanda!.20050523135303"><vh>beginning of indentation</vh></v>
<v t="zorcanda!.20050512113820"><vh>isWord</vh></v>
</v>
<v t="zorcanda!.20050528093036"><vh>balanced parenthesis or sexp</vh>
<v t="zorcanda!.20050528100638"><vh>killSexpForward and Backward</vh></v>
</v>
<v t="zorcanda!.20050528154411"><vh>tags</vh>
<v t="zorcanda!.20050531130856"><vh>__defineLanguageRecognizers</vh></v>
<v t="zorcanda!.20050528154411.1"><vh>gotoTag</vh></v>
<v t="zorcanda!.20050528193932"><vh>alternativeDefinition</vh></v>
<v t="zorcanda!.20050531101443"><vh>popBack</vh></v>
<v t="zorcanda!.20050528154425"><vh>defineTagsTable</vh></v>
<v t="zorcanda!.20050528154749"><vh>scanForTags</vh>
<v t="zorcanda!.20050531112641"><vh>&lt;&lt;java&gt;&gt;</vh></v>
</v>
<v t="zorcanda!.20050528154749.1"><vh>valueChanged</vh></v>
<v t="zorcanda!.20050528155247"><vh>run</vh></v>
<v t="zorcanda!.20050528185814"><vh>class DeferedGotoLine</vh></v>
</v>
<v t="zorcanda!.20050311160343"><vh>transpose</vh>
<v t="zorcanda!.20050311160343.1"><vh>transpose-lines</vh></v>
<v t="zorcanda!.20050311215703"><vh>reverse-region</vh></v>
<v t="zorcanda!.20050524093817"><vh>transpose-words</vh></v>
</v>
<v t="zorcanda!.20050311163509"><vh>capitalization</vh>
<v t="zorcanda!.20050311163509.1"><vh>capitalize-region</vh></v>
<v t="zorcanda!.20050311163509.2"><vh>upcase-region</vh></v>
<v t="zorcanda!.20050311163509.3"><vh>downcase-region</vh></v>
<v t="zorcanda!.20050312111617"><vh>capitalize-word</vh></v>
<v t="zorcanda!.20050312111617.1"><vh>upcase-word</vh></v>
<v t="zorcanda!.20050312111617.2"><vh>downcase-word</vh></v>
</v>
<v t="zorcanda!.20050311165606"><vh>replacement</vh>
<v t="zorcanda!.20050311165606.1"><vh>query-replace</vh></v>
<v t="zorcanda!.20050311165606.2"><vh>query-replace-regexp</vh></v>
<v t="zorcanda!.20050311165732"><vh>replace-string</vh></v>
<v t="zorcanda!.20050311170911"><vh>doReplacement</vh></v>
<v t="zorcanda!.20050311205755"><vh>replaceAll</vh></v>
</v>
<v t="zorcanda!.20050311214332"><vh>sorters</vh>
<v t="zorcanda!.20050311214332.1"><vh>sort-lines</vh></v>
</v>
<v t="zorcanda!.20050312114506"><vh>lines</vh>
<v t="zorcanda!.20050312114506.1"><vh>keep-lines</vh></v>
<v t="zorcanda!.20050312114506.2"><vh>flush-lines</vh></v>
</v>
<v t="zorcanda!.20050312122805"><vh>tabs</vh>
<v t="zorcanda!.20050312122805.1"><vh>tabify</vh></v>
<v t="zorcanda!.20050312122805.2"><vh>untabify</vh></v>
</v>
<v t="zorcanda!.20050312155939"><vh>registers (SwingMacs)</vh>
<v t="ekr.20050726081815"><vh>  __init__</vh></v>
<v t="ekr.20050726081815.1"><vh> __call__</vh></v>
<v t="zorcanda!.20050312160220"><vh>copy-to-register</vh></v>
<v t="zorcanda!.20050312160220.1"><vh>insert-register</vh></v>
<v t="zorcanda!.20050312171820"><vh>append-to-register</vh></v>
<v t="zorcanda!.20050312171820.1"><vh>prepend-to-register</vh></v>
</v>
<v t="zorcanda!.20050519094216"><vh>selection</vh></v>
</v>
<v t="zorcanda!.20050704092406.1"><vh>class vi_emulation (a strategy)</vh>
<v t="zorcanda!.20050704092406.2"><vh>&lt;&lt;define vi keystrokes&gt;&gt;</vh></v>
<v t="zorcanda!.20050704092406.3"><vh>cut</vh></v>
<v t="zorcanda!.20050704092406.4"><vh>deleteLine</vh></v>
<v t="zorcanda!.20050704092406.5"><vh>insert</vh></v>
</v>
</v>
<v t="ekr.20050723063811"><vh>class editCommands ( do not delete)</vh>
<v t="ekr.20050723063811.1"><vh>ctor</vh></v>
<v t="ekr.20050723063811.2"><vh>Options...</vh>
<v t="ekr.20050723063811.3"><vh>setDefaultOptions</vh></v>
<v t="ekr.20050723063811.4"><vh>getOption</vh></v>
</v>
<v t="ekr.20050723063811.5"><vh>Word stuff...</vh>
<v t="ekr.20050723063811.6"><vh>findWordStart</vh></v>
<v t="ekr.20050723063811.7"><vh>insideWord</vh></v>
<v t="ekr.20050723063811.8"><vh>skipWord</vh></v>
<v t="ekr.20050723063811.9"><vh>startsWord</vh></v>
<v t="ekr.20050723063811.10"><vh>setDefaultWordChars</vh></v>
</v>
<v t="ekr.20050723063811.11"><vh>Cursor movement</vh>
<v t="ekr.20050723063811.12"><vh>moveBackwardChar</vh></v>
<v t="ekr.20050723063811.13"><vh>moveBackwardWord (Finish)</vh></v>
<v t="ekr.20050723063811.14"><vh>moveForwardChar</vh></v>
<v t="ekr.20050723063811.15"><vh>moveForwardWord</vh></v>
<v t="ekr.20050723063811.16"><vh>selectWord</vh></v>
<v t="ekr.20050723063811.17"><vh>selectForwordWord</vh></v>
</v>
</v>
<v t="ekr.20050723060629"><vh>(keystroke stuff)</vh>
<v t="ekr.20050724102409"><vh>From SwingMacs</vh>
<v t="ekr.20050723062822.14"><vh>stateManager</vh></v>
<v t="ekr.20050723062822.34"><vh>masterCommand (SwingMacs) all processing goes through here</vh></v>
<v t="ekr.20050723062822.38"><vh>keyboardQuit</vh></v>
</v>
<v t="ekr.20050724103251"><vh>From temacs</vh>
<v t="ekr.20050724075352.43"><vh>masterCommand</vh>
<v t="ekr.20050729150051.1"><vh>&lt;&lt; handle macro &gt;&gt;</vh></v>
<v t="ekr.20050731084644"><vh>&lt;&lt; add character to history &gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="ekr.20050730204402"><vh>&lt;&lt; to do &gt;&gt;</vh></v>
<v t="ekr.20050724075352.41"><vh> ctor (Emacs)</vh></v>
<v t="ekr.20050727162112"><vh> ctor (miniBuffer)</vh></v>
<v t="ekr.20050728195531"><vh>State machines</vh>
<v t="ekr.20050730074556.3"><vh>getArg</vh></v>
<v t="ekr.20050724075352.61"><vh>replaceString</vh>
<v t="ekr.20050730074556.1"><vh>&lt;&lt; do the replace &gt;&gt;</vh></v>
</v>
</v>
<v t="ekr.20050724075352.285"><vh>doAlt_X &amp; helpers</vh>
<v t="ekr.20050724075352.92"><vh>_findMatch</vh></v>
<v t="ekr.20050729094213"><vh>&lt;&lt; handle tab completion &gt;&gt;</vh></v>
<v t="ekr.20050730194026"><vh>&lt;&lt; dispatch the function &gt;&gt;</vh></v>
<v t="ekr.20050730204051"><vh>&lt;&lt; cut back to previous prefix and update prefix &gt;&gt;</vh></v>
</v>
<v t="ekr.20050731084644.1"><vh>Dispatching commands...</vh>
<v t="ekr.20050724075352.43"><vh>masterCommand</vh>
<v t="ekr.20050729150051.1"><vh>&lt;&lt; handle macro &gt;&gt;</vh></v>
<v t="ekr.20050731084644"><vh>&lt;&lt; add character to history &gt;&gt;</vh></v>
</v>
<v t="ekr.20050724075352.32"><vh>__call__ (keyStrokeManagerClass)</vh></v>
<v t="ekr.20050724075352.14"><vh>class controlX_handlerClass</vh>
<v t="ekr.20050724075352.15"><vh>__init__</vh></v>
<v t="ekr.20050724075352.16"><vh>__call__</vh></v>
<v t="ekr.20050728103627.2"><vh>finishCreate (controlX_handlerClass)  MUST BE GENERALIZED</vh></v>
<v t="ekr.20050724075352.17"><vh>processKey</vh></v>
<v t="ekr.20050724075352.18"><vh>processRectangle</vh></v>
<v t="ekr.20050724075352.19"><vh>processAbbreviation</vh></v>
</v>
</v>
<v t="ekr.20050724075352.221"><vh>class searchCommandsClass</vh>
<v t="ekr.20050725091822.2"><vh> ctor</vh></v>
<v t="ekr.20050725093156"><vh>getPublicCommands</vh></v>
<v t="ekr.20050725093537"><vh>Entry points</vh></v>
<v t="ekr.20050724075352.222"><vh>incremental search methods</vh>
<v t="ekr.20050724075352.223"><vh>startIncremental</vh></v>
<v t="ekr.20050724075352.224"><vh>search</vh></v>
<v t="ekr.20050724075352.225"><vh>iSearch</vh></v>
<v t="ekr.20050724075352.226"><vh>scolorizer</vh></v>
<v t="ekr.20050724075352.227"><vh>useRegex</vh></v>
</v>
<v t="ekr.20050724075352.228"><vh>non-incremental search methods</vh>
<v t="ekr.20050724075352.229"><vh>nonincrSearch</vh></v>
<v t="ekr.20050724075352.230"><vh>startNonIncrSearch</vh></v>
</v>
<v t="ekr.20050724075352.231"><vh>word search methods</vh>
<v t="ekr.20050724075352.232"><vh>startWordSearch</vh></v>
<v t="ekr.20050724075352.233"><vh>wordSearch</vh></v>
</v>
<v t="ekr.20050724075352.234"><vh>re-search methods</vh>
<v t="ekr.20050724075352.235"><vh>reStart</vh></v>
<v t="ekr.20050724075352.236"><vh>re_search</vh></v>
</v>
</v>
<v t="ekr.20050731092507"><vh>Bindings</vh>
<v t="ekr.20050729150051.2"><vh>add_ekr_altx_commands</vh>
<v t="ekr.20050729150804"><vh>&lt;&lt; define dict d of abbreviations &gt;&gt;</vh></v>
</v>
<v t="ekr.20050724075352.49"><vh>addCallBackDict (miniBufferClass) MUST BE GENERALIZED</vh></v>
<v t="ekr.20050724075352.52"><vh>addRegisterItems (registerCommandsClass)</vh></v>
<v t="ekr.20050728103627.2"><vh>finishCreate (controlX_handlerClass)  MUST BE GENERALIZED</vh></v>
<v t="ekr.20050728103627.1"><vh>finishCreate (keyStrokeManagerClass) MUST BE GENERALIZED</vh></v>
<v t="ekr.20050728093027.1"><vh>finishCreate (miniBufferClass) MUST BE GENERALIZED</vh></v>
<v t="ekr.20050725112958"><vh>finishCreate (stateManagerClass) MUST BE GENERALIZED</vh></v>
<v t="ekr.20050724075352.116"><vh>reconfigureKeyStroke  Not tested -- why is it needed?</vh></v>
<v t="ekr.20050724075352.91"><vh>removeRKeys (baseCommandsClass)</vh></v>
</v>
<v t="ekr.20050731101651"><vh>All xemacs commands</vh>
<v t="ekr.20050731102358"><vh>B</vh></v>
<v t="ekr.20050731102651.1"><vh>C, E, F, H</vh></v>
<v t="ekr.20050731102651.3"><vh>I</vh></v>
<v t="ekr.20050731102651.4"><vh>L, M, R, T, V</vh></v>
<v t="ekr.20050731101651.1"><vh>a append- appropos- auto-</vh></v>
<v t="ekr.20050731101651.2"><vh>b: backward- beginning- bookmark- br- browse- buffer- build- byte-</vh></v>
<v t="ekr.20050731101651.3"><vh>c: c calc-, call- capitalize- center- checkdoc- command- completion- count- customize- cvs-</vh></v>
<v t="ekr.20050731101651.4"><vh>d dabbrev- define- delete- describe- dired- downcase-</vh></v>
<v t="ekr.20050731101651.5"><vh>e ediff- edit- emerge- end- exchange- expand-</vh></v>
<v t="ekr.20050731101651.6"><vh>f fill- find- format- forward-</vh></v>
<v t="ekr.20050731101651.7"><vh>g global- goto- grep-</vh></v>
<v t="ekr.20050731102358.1"><vh>h help- html- hyper-</vh></v>
<v t="ekr.20050731102358.2"><vh>i isearch- ispell- iswitchb itimer-</vh></v>
<v t="ekr.20050731102358.3"><vh>j</vh></v>
<v t="ekr.20050731102358.4"><vh>k kill- kimport-</vh></v>
<v t="ekr.20050731102358.5"><vh>l list- load-</vh></v>
<v t="ekr.20050731102358.6"><vh>m mouse- move-</vh></v>
<v t="ekr.20050731102358.7"><vh>n narrow- newline- next-</vh></v>
<v t="ekr.20050731102358.8"><vh>o open- other-</vh></v>
<v t="ekr.20050731102358.9"><vh>p package- paren- pcomplete- pending- pop- popup- pp- prepend- prettyexapnd- previous- profile- ps-</vh></v>
<v t="ekr.20050731102358.10"><vh>q query-</vh></v>
<v t="ekr.20050731102358.11"><vh>r re- read- recentf- recover- recursive- rename- repeat- replace- reverse- run-</vh></v>
<v t="ekr.20050731102358.12"><vh>s save- scroll- search- set- shell- sort- speedbar spell- strokes- suspend- switch- symbol-</vh></v>
<v t="ekr.20050731102358.13"><vh>t tab tags- toggle- toolbar- turn-off turn-on</vh></v>
<v t="ekr.20050731102358.14"><vh>u universal- upcase- url-</vh></v>
<v t="ekr.20050731102358.15"><vh>v view- vm-</vh></v>
<v t="ekr.20050731102358.16"><vh>w win32- winring- word- write-</vh></v>
<v t="ekr.20050731102358.17"><vh>x xwem-</vh></v>
<v t="ekr.20050731102358.18"><vh>y yank-</vh></v>
<v t="ekr.20050731102358.19"><vh>z zap- </vh></v>
</v>
<v t="ekr.20050731115541"><vh>Goals</vh></v>
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
<v t="pap.20041006184225"
expanded="pap.20041006184225.6,pap.20041006190817,"><vh>@thin plugin_manager.py</vh></v>
<v t="pap.20050605183206"><vh>@thin leoupdate.py</vh></v>
</v>
<v t="ekr.20041001210557"><vh>Scripting</vh>
<v t="EKR.20040613213623"><vh>@thin mod_scripting.py</vh></v>
</v>
<v t="ekr.20050111122605"><vh>Servers</vh>
<v t="EKR.20040517080250.1"><vh>@thin mod_http.py</vh></v>
</v>
<v t="edream.110203113231.930"><vh>Spell Checking</vh>
<v t="ekr.20040809165421"><vh>Read me or suffer</vh></v>
<v t="ekr.20050518064900"><vh>Installing apell on Linux systems</vh></v>
<v t="edream.110203113231.932"><vh>@thin mod_spelling.ini</vh></v>
<v t="edream.110203113231.933"><vh>@thin mod_spelling.py</vh></v>
<v t="ekr.20050216110126"><vh>Spelling to do</vh></v>
<v t="ekr.20040809151600"><vh>spellpyx</vh>
<v t="ekr.20040809165421.1"><vh>Installing this plugin</vh></v>
<v t="ekr.20040809151600.4"><vh>Links</vh></v>
<v t="ekr.20041009165858"><vh>@thin spellpyx.ini</vh></v>
<v t="ekr.20040809151600.1"><vh>@thin spellpyx.py</vh></v>
<v t="ekr.20040809151600.52"><vh>aspell-1.1</vh>
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
</v>
<v t="ekr.20041107165824"><vh>temacs &amp; usetemacs</vh>
<v t="ekr.20050527081321"><vh>EKR Notes</vh>
<v t="ekr.20050710094310.2"><vh>@url http://vimdoc.sourceforge.net/htmldoc/usr_03.html (must do all these)</vh></v>
<v t="ekr.20050514095136"><vh>ekr usetemacs.ini (doesn't solve the problem I was trying to solve)</vh></v>
<v t="ekr.20050514095136.1"><vh>Key references</vh></v>
</v>
<v t="mork.20041013092542.1"><vh>@thin usetemacs.py</vh></v>
<v t="mork.20041030164547"><vh>@thin temacs.py</vh></v>
<v t="ekr.20050518085205"><vh>@thin usetemacs.ini</vh></v>
</v>
<v t="ekr.20050306081349"><vh>Text formatting</vh>
<v t="edream.111803100242"><vh>@thin rst.py</vh></v>
<v t="ekr.20040331071319"
marks="ekr.20040331071319.7,"><vh>@thin rst2.py</vh></v>
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
<v t="ekr.20050818103031" a="E"><vh>&lt;&lt; to do &gt;&gt;</vh></v>
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
<v t="ekr.20050818094954.1" a="E"><vh> Raises SkipNode</vh>
<v t="ekr.20050817120850.165"><vh>comment</vh></v>
<v t="ekr.20050817120850.116" a="E"><vh> literal_blocks...</vh>
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
marks="ekr.20050816094344,ekr.20050811101550.1,"><vh>@thin rst3.py</vh></v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="EKR.20040517075715"></t>
<t tx="EKR.20040517075715.13"></t>
<t tx="EKR.20040517075715.20">[Main]
use_styles = Yes
use_section_numbers = Yes
use_current_document = Yes
max_headings = 6
header_style = Heading

</t>
<t tx="EKR.20040517075915">'''Automatically add nodes for common tasks'''

# We must use @file-noref because data below might look like section references,
# so ORDER IS IMPORTANT throughout this tree.

# Directives are not valid in @nosent files.
#@language python
#@tabwidth -4

__name__ = "New Buttons"
__version__ = "0.3"
# 0.2 EKR: Converted to @file-noref
# 0.3 EKR: Added 6 new plugin templates.  Added init function.
# 0.4 EKR: Added importLeoGlobals function.
 
import leoGlobals as g
import leoPlugins
import leoFind

Tk = g.importExtension('Tkinter',pluginName=__name__,verbose=True)

# We can not use @others in an @nosent tree.</t>
<t tx="EKR.20040517075915.1">"""Classes to add helpers to the toolbar 
 
A helper is a class that adds a set of preconfigured nodes to the outline. This 
can be used to generate boiler plate code to quickly build an outline. The nodes 
and body text added can have an adjustable parameter, which is defined from 
the text entry box. 
 
"""

USE_FIXED_SIZES = 1</t>
<t tx="EKR.20040517075915.2">class FlatOptionMenu(Tk.OptionMenu):

    """Flat version of OptionMenu which allows the user to select a value from a menu."""

    def __init__(self, master, variable, value, *values, **kwargs):
        """Construct an optionmenu widget with the parent MASTER, with 
        the resource textvariable set to VARIABLE, the initially selected 
        value VALUE, the other menu values VALUES and an additional 
        keyword argument command.""" 
        kw = {
            "borderwidth": 2, "textvariable": variable,
            "indicatoron": 1, "relief": "flat", "anchor": "c",
            "highlightthickness": 2}
        Tk.Widget.__init__(self, master, "menubutton", kw)
        self.widgetName = 'tk_optionMenu' 
        menu = self.__menu = Tk.Menu(self, name="menu", tearoff=0)
        self.menuname = menu._w
        # 'command' is the only supported keyword 
        callback = kwargs.get('command')
        if kwargs.has_key('command'):
            del kwargs['command']
        if kwargs:
            raise TclError, 'unknown option -'+kwargs.keys()[0]
        menu.add_command(label=value,
            command=Tk._setit(variable, value, callback))
        for v in values:
            menu.add_command(label=v,
                command=Tk._setit(variable, v, callback))
        self["menu"] = menu</t>
<t tx="EKR.20040517075915.3">class Node: 
    """A node to add"""

    def __init__(self, name="", body="", inherit=0, subnodes=None):
        """Initialise the node"""
        self.name = name
        self.body = body
        self.subnodes = subnodes or []
        self.inherit = inherit # Set True to inherit the first line from our immediate sibling 

    def processText(self, text, name):
        """Process some boiler plate text"""
        if name: 
            text = text.replace("XXX", name)
            text = text.replace("xxx", name.lower())
        return text.strip()

    def addTo(self, c, text, parent=None): 
        """Add our nodes etc"""
        if self.inherit:
            header = c.currentVnode().bodyString().split("\n")[0] + "\n"
        else:
            header = ""
        # 
        c.insertHeadline()
        main = c.currentVnode()
        main.setHeadString(self.processText(self.name, text))
        # 
        main.setBodyStringOrPane(self.processText(header+self.body, text))
        if parent: 
            c.currentVnode().moveToNthChildOf(parent, 0) 
        # 
        parent = c.currentVnode()
        for node in self.subnodes:
            node.addTo(c, text, parent)
            parent = None # Only want first node to be moved, others will go automatically </t>
<t tx="EKR.20040517075915.4">class NodeAdder:

    """A Class to add a helper button to the toolbar which adds nodes to the outline""" 

    button_name = "Add"

    nodes = () # Should be set in the subclasses 

    def doIt(self, entry):
        """Create the nodes"""
        c = g.top()
        name = entry.get()
        for node in self.nodes:
            node.addTo(c, name)</t>
<t tx="EKR.20040517075915.5">class Helper:

    """A Class to aid in the creating and maintenance of unit test files"""

    def __init__(self, adders):

        """Initialise with a set of adders"""
    
        self.adders = adders

    def addWidgets(self, tags, keywords):

        """Add the widgets to Leo"""
        self.commander = keywords['c']
        toolbar = self.commander.frame.iconFrame
        # 
        self.frame = Tk.Frame(toolbar)
        self.frame.pack(side="right", padx=2)
        # 
        self.text = Tk.Entry(self._getSizer(self.frame, 24, 130))
        self.text.pack(side="left", padx=3, fill="both", expand=1)
        self.text.bind("&lt;Return&gt;", self.doCallback)
        # 
        self.pseudobutton = Tk.Frame(self._getSizer(self.frame, 24, 142),
            relief="raised", borderwidth=2) 
        self.pseudobutton.pack(side="right")
        # 
        self.doit = Tk.Button(self._getSizer(self.pseudobutton, 25, 32),
            text="New", relief="flat", command=self.doCallback)
        self.doit.pack(side="left")
        # 
        options = [adder.button_name for adder in self.adders]
        self.option_value = Tk.StringVar()
        self.options = FlatOptionMenu(self._getSizer(self.pseudobutton, 29, 110),
            self.option_value, *options)
        self.option_value.set(options[0])
        self.options.pack(side="right", fill="both", expand=1)
        
    def _getSizer(self, parent, height, width, pack="left"):
    
        """Return a sizer object to force a Tk widget to be the right size"""
    
        if USE_FIXED_SIZES:
            sizer = Tk.Frame(parent, height=height, width=width)
            sizer.pack_propagate(0) # don't shrink 
            sizer.pack(side=pack)
            return sizer
        else:
            return parent
            
    def doCallback(self, event=None):

        """Generate a callback to call the specific adder"""
        for adder in self.adders:
            if adder.button_name == self.option_value.get():
                adder.doIt(self.text)
                break
        else:
            raise ValueError("Button name not found: '%s'" % self.option_value.get())</t>
<t tx="EKR.20040517075915.6"># (Note to myself: we can't use @doc in @nosent trees.)
#
# Modify these classes or data as you like to create templates that suit you.
#
# You can add new classes as follows:
# 1. Create your new class using an existing AddXXX class as a guide. Your new
#    class should be in a child node of this node.
#
# 2. Add the name of the new class to the buttonList tuple in the init function.</t>
<t tx="EKR.20040517075915.7">TEST_NODE_BODY = '''
import unittest

@others

if __name__ == "__main__":
    unittest.main()
'''

TEST_CLASS_BODY = '''
class TestXXX(unittest.TestCase):

    """Tests for the XXX class"""

    @others
'''

TEST_SETUP_BODY = '''
def setUp(self):

    """Create the test fixture"""

'''</t>
<t tx="EKR.20040517075915.8">class AddTestModule(NodeAdder):

    """Add unit testing node"""

    button_name = "test module"

    nodes = [
        Node(
            name="testxxx.py",
            body=TEST_NODE_BODY,
            subnodes=[ 
                Node(
                    name="TestXXX",
                    body=TEST_CLASS_BODY,
                    subnodes=[ 
                        Node(name="setUp",
                        body=TEST_SETUP_BODY)])])]</t>
<t tx="EKR.20040517075915.9">class AddTestClass(NodeAdder):

    """Add unit testing class"""

    button_name = "test class"

    nodes = [
        Node(
            name="TestXXX",
            body=TEST_CLASS_BODY,
            subnodes=[
                Node(
                    name="setUp",
                    body=TEST_SETUP_BODY)])]</t>
<t tx="EKR.20040517075915.10">TEST_METHOD_BODY = '''
def testXXX(self):

    """testXXX: TestDescriptionGoesHere"""

'''

class AddTestMethod(NodeAdder):

    """Add unit testing method"""

    button_name = "test method"

    nodes = [
    Node(
        name="testXXX",
        body=TEST_METHOD_BODY,
        inherit=0)] # EKR: was 1.</t>
<t tx="EKR.20040517075915.11">NEW_CLASS_BODY = '''
class XXX:

    """DocStringGoesHere"""

    @others
'''

NEW_INIT_BODY = '''
def __init__(self):

    """Initialise the XXX instance"""

'''

class AddClass(NodeAdder):
    
    """Add new class"""

    button_name = "class"

    nodes = [
        Node(
            name="class XXX",
            body=NEW_CLASS_BODY,
            subnodes=[
                #Node(
                #	name="&lt;&lt; class XXX declarations &gt;&gt;",
                #	body="@c\npass"),
                Node(
                    name="__init__",
                    body=NEW_INIT_BODY)] )]
</t>
<t tx="EKR.20040517075915.12">CLASS_METHOD_BODY = '''
def XXX(self):

    """MethodDocstringGoesHere"""

'''

class AddClassMethod(NodeAdder):

    """Add class method"""

    button_name = "method"

    nodes = [
        Node(
            name="XXX",
            body=CLASS_METHOD_BODY,
            inherit=0)] # EKR: was 1.</t>
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

    c.frame.menu.createMenuEntries(c.pluginMenu,table)</t>
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

    c.frame.menu.createMenuEntries(exportMenu, newEntries)
    
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
@tabwidth -4
@doc
@ascskip # Time-stamp: "Tue, Jan 13 10:14 CST 2004  michael@redpriest _OpenTree_Plugin__140660268.py"

This is a module that creates an "Open With" menu item that opens
Leo outline nodes in the tree below the current Leo node in the
XEmacs editor.  I frequently have a small tree of Leo nodes which
contain code that is usually edited in the same session.

NOTE: I use the "gnuclient-noshow" selection to load the temporary
open_with file in the background.  Leo calls a command with the
temporary file name at the end of the command, but the gnuclient
command needs to receive it enclosed in quotes and parentheses.  The
solution is a small intermediary bash shell script called
"gnuclient-noshow":

---
#!/bin/bash
gnuclient -eval "(find-file-noselect \"${1}\")"
---

I would rather have this operate in the background, but Leo's
openWith always operates on the current node, and openWith has much
good error checking that I want to use. So the fast solution was to
have OpenTreeInXEmacs visibly traverse the tree.

@ascskip on
@root "other/xemacs/mod_xemacsopentree.py"
&lt;&lt; Open_Tree Plugin &gt;&gt;
@code

import leoPlugins

def OpenTreeInXEmacs():
    import leoCommands
    #XEmacsCommand = "/usr/bin/gnuclient -q "
    XEmacsCommand = "/mrc2/linux-bin/gnuclient-noshow "
    c = g.top()
    vnode = c.currentVnode() # get the current vnode.
    stopHere = vnode.nodeAfterTree()
    v = vnode
    while v != stopHere:
        c.openWith(data=("os.system", XEmacsCommand, None))
        v = v.threadNext()
        if (not v) or (v == stopHere):
            break
        c.selectVnode(v)
    c.selectVnode(vnode)


def CreateOpenTreeMenu(tag,keywords):

    """Create the 'Xemacs: Open Tree' menu item in the Open With menu."""


    if  (tag=="open2" or
        (tag=="start2") or
        (tag=="command2" and keywords.get("label")=="new")):

        c = g.top()
        exportMenu = c.frame.menu.getMenu('Open With')
        newEntries = (
            ("-", None, None),
            ("XEmacs: Open nodes in sub-tree","None",OpenTreeInXEmacs),
            )

        c.frame.menu.createMenuEntries(exportMenu, newEntries)

if 1:
    leoPlugins.registerHandler(("start2","open2","command2"), CreateOpenTreeMenu)

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
<t tx="ekr.20040809151600"></t>
<t tx="ekr.20040809151600.4">@killcolor

Links:

&lt;http://aspell.net&gt;
&lt;http://aspell.net/win32/&gt;
get the dll's and headers if you will compile your own.

A Pyrex wrapper for the aspell api.
&lt;http://prdownloads.sourceforge.net/uncpythontools/aspell-1.0.zip?download&gt;
&lt;http://sourceforge.net/project/showfiles.php?group_id=82407&gt;

if you want to compile it get
&lt;http://www.cosc.canterbury.ac.nz/~greg/python/Pyrex/&gt;
works with the latest pyrex and mingw gcc .
you can just copy the python*.dll and *aspell.dll
to mingw/lib now instead of the grueling lib building steps. &lt;http://www.mingw.org&gt;

http://sourceforge.net/forum/forum.php?thread_id=1107275&amp;forum_id=10226
</t>
<t tx="ekr.20040809151600.52"></t>
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
<t tx="ekr.20040809165421">@killcolor

spellpyx.py is the new spell checker.  It is much faster, but requires Python 2.3 and a recent version of Aspell.

spellpyx.py uses the file aspell.pyd.  You can use files aspell.pyx and setup.py to recreate aspell.pyd.  To generate these files, change @(blank)file to @file.

mod_spelling.py is the older spell checker.  It is slower, but will work with all versions of Python and most recent versions of Aspell.  Warning: you must _remove_ aspell.pyd if you are going to use mod_spelling.py.  I have not been able to get mod_spelling.py to work with Leo 4.2.

Both spelling plugins use a configuration files and a dictionary.  The configuration files are mod_spelling.ini and spellpyx.ini respectively.  The .ini files contain a few configuration settings.  One of these settings is the name of the dictionary.  By default, the names of the dictionary are mod_spelling.txt and spellpyx.txt.

It would be quite dangerous to create a dictionary in an @asis node here: only the plugin code should typically change this file.  You may, of course, edit mod_spelling.txt and spellpyx.txt yourself: just make sure that Leo isn't running when you do this.</t>
<t tx="ekr.20040809165421.1">@nocolor

Notes for version 0.10

1.  Each aspell.pyd is specific to a particular Python (and aspell?) version.

    - This code has been tested only with Python 2.4 and the dll given to me by 'e'.

2. On XP, aspell.pyd must be in the apell\bin folder, presumably so it can find aspell-15.dll.

3.  In the &lt;&lt; spellpx imports &gt;&gt; section in spellpyx.py, do the following

    - Set aspell_dir to the top-level Aspell directory.

    - Set aspell_bin_dir to the bin subdirectory.</t>
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
<t tx="ekr.20041002162608"># Note: this work has been superceded by the temacs plugin.</t>
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
<t tx="ekr.20041107165824"></t>
<t tx="ekr.20041110104350"></t>
<t tx="ekr.20041113110210">import leoGlobals as g
import leoPlugins
c = g.top()

spellpyx = leoPlugins.getPluginModule("spellpyx")
createMenu = spellpyx is None
keys = {'c':c}

if not spellpyx:
    print 'loading spellpyx plugin'
    spellpyx = leoPlugins.loadOnePlugin("spellpyx",verbose=True)
    if spellpyx:
        spellpyx.onCreate('tag',keys)

if spellpyx:
    # g.trace(g.dictToString(spellpyx.spellFrames,tag='spellFrames'))
    spellFrame = spellpyx.spellFrames.get(c)
    if spellFrame and createMenu:
        spellFrame.createSpellMenu('tag',keys)
    if spellFrame:
        spellFrame.checkSpelling()</t>
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

- Please do _not_ assume that modules like Tkinter, Pmw, etc. are always available.  Use the code as shown.

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
<t tx="ekr.20050216110126">@nocolor

- Set use visible_initially setting from .ini file rather than visibleInitially.

- Simplify the directory settings.</t>
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
<t tx="ekr.20050313115107">class AddPluginTkInitFunction(NodeAdder):

    '''Add plugin init(tk).'''

    button_name = "plugin init(tk)"

    nodes = [
        Node(
            name="init",
            body=TK_INIT_FUNCTION_BODY,
            inherit=0
    )]</t>
<t tx="ekr.20050313120113">def init():
    
    # The list of buttons to insert.  
    buttonList = (
        AddTestModule(),
        AddTestClass(),
        AddTestMethod(),
        AddClass(),
        AddClassMethod(),
        # EKR, v0.3...
        AddGenericPlugin(),
        AddTkPlugin(),
        AddPluginInitFunction(),
        AddPluginTkInitFunction(),
        AddPluginImportsSection(),
        AddPluginVersionHistorySection(),
        # EKR, v0.4...
        AddImportLeoGlobalsFunction(),
    )

    ok = Tk is not None

    if ok:
        if g.app.gui is None:
            g.app.createTkGui(__file__)
            
        ok = g.app.gui.guiName() == "tkinter"
        if ok:
            # g.es("Activating newButtons", color="orange")
            helper = Helper(buttonList)
            leoPlugins.registerHandler("after-create-leo-frame", helper.addWidgets)
            g.plugin_signon("newButtons")
        
    return ok</t>
<t tx="ekr.20050313120345">class AddPluginInitFunction(NodeAdder):

    '''Add plugin init.'''

    button_name = "plugin init"

    nodes = [
        Node(
            name="init",
            body=GENERIC_INIT_FUNCTION_BODY,
            inherit=0
    )]</t>
<t tx="ekr.20050313120714">class AddPluginImportsSection(NodeAdder):

    '''Add Tk plugin imports section.'''

    button_name = "&lt;&lt;imports&gt;&gt;"

    nodes = [
        Node(
            name="&lt;&lt; imports &gt;&gt;",
            body=TK_IMPORTS_BODY,
            inherit=0
    )]</t>
<t tx="ekr.20050313121102">class AddPluginVersionHistorySection(NodeAdder):

    '''Add plugin version history section.'''

    button_name = "&lt;&lt;version history&gt;&gt;"

    nodes = [
        Node(
            name="&lt;&lt; version history &gt;&gt;",
            body=VERSION_HISTORY_BODY,
            inherit=0
    )]</t>
<t tx="ekr.20050313123322"></t>
<t tx="ekr.20050313123322.1">GENERIC_INIT_FUNCTION_BODY = '''
def init():

    ok = True # May depend on imports.

    if ok:
        # Register any hooks here.
        # See the Tk init function for an example of using per-commander classes.

        g.plugin_signon(__name__)
    
    return ok
'''</t>
<t tx="ekr.20050313123322.2">PLUGIN_ROOT_BODY = '''
&lt;&lt; docstring &gt;&gt;

@language python
@tabwidth -4

&lt;&lt; imports &gt;&gt;

__version__ = '.1'
&lt;&lt; version history &gt;&gt;

@others
'''
</t>
<t tx="ekr.20050313123322.3">TK_INIT_FUNCTION_BODY = '''
def init():

    ok = True # Pmw or Tk

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
        
    return ok
'''</t>
<t tx="ekr.20050313123322.4">VERSION_HISTORY_BODY = '''
@killcolor
@

Version .1: Initial version by (your name here)
'''
</t>
<t tx="ekr.20050313123322.5">class AddGenericPlugin(NodeAdder):

    """Add tree for generic plugin"""

    button_name = "generic plugin"

    nodes = [
        Node(
            name="@thin myGenericPlugin.py",
            body=PLUGIN_ROOT_BODY,
            subnodes=[
                Node(
                    name="&lt;&lt; docstring &gt;&gt;",
                    body=DOCSTRING_BODY),
                 Node(
                    name="&lt;&lt; imports &gt;&gt;",
                    body=GENERIC_IMPORTS_BODY),
                Node(
                    name="&lt;&lt; version history &gt;&gt;",
                    body=VERSION_HISTORY_BODY),
                Node(
                    name="init",
                    body=GENERIC_INIT_FUNCTION_BODY),
            ]
        )
    ]</t>
<t tx="ekr.20050313123600">DOCSTRING_BODY ="""
'''This docstring should be a clear, concise description of
what the plugin does and how to use it.
'''
"""
</t>
<t tx="ekr.20050313124016">GENERIC_IMPORTS_BODY = '''
import leoGlobals as g
import leoPlugins
'''</t>
<t tx="ekr.20050313124016.1">TK_IMPORTS_BODY = '''
import leoGlobals as g
import leoPlugins

Tk = g.importExtension('Tkinter',pluginName=__name__,verbose=True)
'''</t>
<t tx="ekr.20050313124212">class AddTkPlugin(NodeAdder):

    """Add tree for Tk plugin"""

    button_name = "Tk plugin"
    nodes = [
        Node(
            name="@thin myTkPlugin.py",
            body=PLUGIN_ROOT_BODY,
            subnodes=[
                Node(
                    name="&lt;&lt; docstring &gt;&gt;",
                    body=DOCSTRING_BODY),
                Node(
                    name="&lt;&lt; imports &gt;&gt;",
                    body=TK_IMPORTS_BODY),
                Node(
                    name="&lt;&lt; version history &gt;&gt;",
                    body=VERSION_HISTORY_BODY),
                Node(
                    name="init",
                    body=TK_INIT_FUNCTION_BODY),
                Node(
                    name="onCreate",
                    body=TK_ON_CREATE_FUNCTION),
                Node(
                    name="class pluginController",
                    body=TK_PLUGIN_CONTROLLER,
                    subnodes=[
                        Node(
                            name="__init__",
                            body=TK_PLUGIN_CONTROLLER_INIT),
                    ]
                )
            ]
        )
    ]</t>
<t tx="ekr.20050313124619">TK_ON_CREATE_FUNCTION = '''
def onCreate (tag, keys):
    
    c = keys.get('c')
    if not c: return
    
    thePluginController = pluginController(c)
'''</t>
<t tx="ekr.20050313124954">TK_PLUGIN_CONTROLLER = """

class pluginController:
    
    @others

"""</t>
<t tx="ekr.20050313125536">TK_PLUGIN_CONTROLLER_INIT = '''
def __init__ (self,c):
    
    self.c = c
'''</t>
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
<t tx="ekr.20050329033007">IMPORT_LEO_GLOBALS_BODY = """def importLeoGlobals():
    
    '''
    Try to import leoGlobals from the leo/src directory, assuming that
    the script using this function is in a subdirectory of the leo directory.
    '''
    
    plugins_path = os.path.abspath(
        os.path.join(os.path.dirname(__file__),'..','src'))
    
    if plugins_path in sys.path:
        return None
    else:
        sys.path.append(plugins_path)
        try:
            import leoGlobals as g
            return g
        except ImportError:
            print 'can not import leoGlobals from %s' % (plugins_path)
            return None
"""
</t>
<t tx="ekr.20050329033007.1">class AddImportLeoGlobalsFunction(NodeAdder):

    '''Add importLeoGlobals function.'''

    button_name = "&lt;&lt;importLeoGlobals&gt;&gt;"

    nodes = [
        Node(
            name="&lt;&lt; define importLeoGlobals &gt;&gt;",
            body=IMPORT_LEO_GLOBALS_BODY,
            inherit=0
    )]</t>
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
<t tx="ekr.20050514095136">[ newkeystrokes ]

#Alt-q=Alt-f # rebind Alt-q to what Alt-f does.
# Cut and paste first
Alt-Ctrl-x = Ctrl-x
Alt-Ctrl-x ( =Ctrl-x (
Alt-Ctrl-x ) =Ctrl-x )
Alt-Ctrl-x e =Ctrl-x e

Alt-Ctrl-z=Ctrl-z

Alt-Ctrl-x Ctrl-u=Ctrl-x Ctrl-u
Alt-Ctrl-x Ctrl-l=Ctrl-x Ctrl-l
Alt-Ctrl-x h=Ctrl-x

Alt-Ctrl-x tab=Ctrl-x tab
Alt-Ctrl-x Ctrl-x=Ctrl-x Ctrl-x
Alt-Ctrl-x semicolon=Ctrl-x semicolon

Alt-Ctrl-x a e=Ctrl-x a e
Alt-Ctrl-x a g=Ctrl-x a g
Alt-Ctrl-x a i g=Ctrl-x a i g

Alt-Ctrl s=Ctrl s
Alt-Ctrl r=Ctrl r

# Alt-Ctrl XXX=

Alt-Ctrl-s Enter=Ctrl-s Enter
Alt-Ctrl-r Enter=Ctrl-r Enter
Alt-Ctrl-s Enter Ctrl-w=Ctrl-s Enter Ctrl-w
Alt-Ctrl-r Enter Ctrl-w=Ctrl-r Enter Ctrl-w
 
# Ctrl-Alt s
# Ctrl-Alt r
Alt-Ctrl-%=Alt-%
#&lt;Ctrl Alt %
Alt-Ctrl-==Alt-=
Alt-Ctrl-(=Alt-(
Alt-Ctrl-)=&lt;Alt-)

Alt-Ctrl-x Ctrl-t=Ctrl-x Ctrl-t
Alt-Ctrl-x Ctrl-o=Ctrl-x Ctrl-o
Alt-Ctrl-x r s=Ctrl-x r s
Alt-Ctrl-x r i=Ctrl-x r i
Alt-Ctrl-x r +=Ctrl-x r +
Alt-Ctrl-x r n=Ctrl-x r n
Alt-Ctrl-x r space=Ctrl-x r space
Alt-Ctrl-x r j=Ctrl-x r j
Alt-Ctrl-x x=Ctrl-x x
Alt-Ctrl-x r r=Ctrl-x r r
Alt-Ctrl-x r o=Ctrl-x r o
Alt-Ctrl-x r c=Ctrl-x r c
Alt-Ctrl-x r d=Ctrl-x r d
Alt-Ctrl-x r t=Ctrl-x r t
Alt-Ctrl-x r k=Ctrl-x r k
Alt-Ctrl-x r y=Ctrl-x r y

Alt-Ctrl-x = =Ctrl-x =
Alt-Ctrl-x . =Ctrl-x .
Alt-Ctrl-x f =Ctrl-x f
Alt-Ctrl-x Ctrl-b =Ctrl-x Ctrl-b
Alt-Ctrl-x b =Ctrl-x b
Alt-Ctrl-x k =Ctrl-x k

Alt-Ctrl-g=Ctrl-g

Alt-Ctrl - - Alt-l =Alt - - Alt-l
Alt-Ctrl - - Alt-u =Alt - - Alt-u
Alt-Ctrl - - Alt-c =Alt - - Alt-c

Alt-Ctrl-/=Alt-/</t>
<t tx="ekr.20050514095136.1">Buffer Keyboard Commands:
----------------------------------------

&lt;Control-p&gt;: move up one line
&lt;Control-n&gt;: move down one line
&lt;Control-f&gt;: move forward one char
&lt;Conftol-b&gt;: move backward one char
&lt;Control-o&gt;: insert newline
&lt;Control-Alt-o&gt; : insert newline and indent
&lt;Control-j&gt;: insert newline and tab
&lt;Alt-&lt;&gt; : move to start of Buffer
&lt;Alt- &gt; &gt;: move to end of Buffer
&lt;Control a&gt;: move to start of line
&lt;Control e&gt; :move to end of line
&lt;Alt-Up&gt;: move to start of line
&lt;Alt-Down&gt;: move to end of line
&lt;Alt b&gt;: move one word backward
&lt;Alt f&gt; : move one word forward
&lt;Control - Right Arrow&gt;: move one word forward
&lt;Control - Left Arrow&gt;: move one word backwards
&lt;Alt-m&gt; : move to beginning of indentation
&lt;Alt-g&gt; : goto line number
&lt;Control-v&gt;: scroll forward one screen
&lt;Alt-v&gt;: scroll up one screen
&lt;Alt-a&gt;: move back one sentence
&lt;Alt-e&gt;: move forward one sentence
&lt;Alt-}&gt;: move forward one paragraph
&lt;Alt-{&gt;: move backwards one paragraph
&lt;Alt-:&gt; evaluate a Python expression in the minibuffer and insert the value in the current buffer
Esc Esc : evaluate a Python expression in the minibuffer and insert the value in the current buffer
&lt;Control-x . &gt;: set fill prefix
&lt;Alt-q&gt;: fill paragraph
&lt;Alt-h&gt;: select current or next paragraph
&lt;Control-x Control-@&gt;: pop global mark
&lt;Control-u&gt;: universal command, repeats the next command n times.
&lt;Alt -n &gt; : n is a number.  Processes the next command n times.
&lt;Control-x (&gt;: start definition of kbd macro
&lt;Control-x ) &gt; : stop definition of kbd macro
&lt;Control-x e : execute last macro defined
&lt;Control-u Control-x ( &gt;: execute last macro and edit
&lt;Control-x Esc Esc &gt;: execute last complex command( last Alt-x command
&lt;Control-x Control-c &gt;: save buffers kill Emacs
&lt;Control-x u &gt; : advertised undo.   This function utilizes the environments.
        If the buffer is not configure explicitly, there is no operation.
&lt;Control-_&gt;: advertised undo.  See above
&lt;Control-z&gt;: iconfify frame
----------------------------------------

&lt;Delete&gt; : delete previous character
&lt;Control d&gt;: delete next character
&lt;Control k&gt; : delete from cursor to end of line. Text goes to kill buffer
&lt;Alt d&gt;: delete word. Word goes to kill buffer
&lt;Alt Delete&gt;: delete previous word. Word goes to kill buffer
&lt;Alt k &gt;: delete current sentence. Sentence goes to kill buffer
&lt;Control x Delete&gt;: delete previous sentence. Sentence goes to kill buffer
&lt;Control y &gt;: yank last deleted text segment from
 kill buffer and inserts it.
&lt;Alt y &gt;: cycle and yank through kill buffer.

&lt;Alt z &gt;: zap to typed letter. Text goes to kill buffer
&lt;Alt-^ &gt;: join this line to the previous one
&lt;Alt-\ &gt;: delete surrounding spaces
&lt;Alt-s&gt; &gt;: center line in current fill column
&lt;Control-Alt-w&gt;: next kill is appended to kill buffer
----------------------------------------

&lt;Alt c&gt;: Capitalize the word the cursor is under.
&lt;Alt u&gt;: Uppercase the characters in the word.
&lt;Alt l&gt;: Lowercase the characters in the word.
----------------------------------------

&lt;Alt t&gt;: Mark word for word swapping.  Marking a second
 word will swap this word with the first
&lt;Control-t&gt;: Swap characters
&lt;Ctrl-@&gt;: Begin marking region.
&lt;Ctrl-W&gt;: Kill marked region
&lt;Alt-W&gt;: Copy marked region
&lt;Ctrl-x Ctrl-u&gt;: uppercase a marked region
&lt;Ctrl-x Ctrl-l&gt;: lowercase a marked region
&lt;Ctrl-x h&gt;: mark entire buffer
&lt;Alt-Ctrl-backslash&gt;: indent region to indentation of line 1 of the region.
&lt;Ctrl-x tab&gt; : indent region by 1 tab
&lt;Control-x Control-x&gt; : swap point and mark
&lt;Control-x semicolon&gt;: set comment column
&lt;Alt-semicolon&gt;: indent to comment column
----------------------------------------

M-! cmd -- Run the shell command line cmd and display the output
M-| cmd -- Run the shell command line cmd with region contents as input
----------------------------------------

&lt;Control-x a e&gt;: Expand the abbrev before point (expand-abbrev). This is effective even when Abbrev mode is not enabled
&lt;Control-x a g&gt;: Define an abbreviation for previous word
&lt;Control-x a i g&gt;: Define a word as abbreviation for word before point, or in point
----------------------------------------

&lt;Control s&gt;: forward search, using pattern in Mini buffer.

&lt;Control r&gt;: backward search, using pattern in Mini buffer.

&lt;Control s Enter&gt;: search forward for a word, nonincremental

&lt;Control r Enter&gt;: search backward for a word, nonincremental

&lt;Control s Enter Control w&gt;: Search for words, ignoring details of punctuation
&lt;Control r Enter Control w&gt;: Search backward for words, ignoring details of punctuation
&lt;Control-Alt s&gt;: forward regular expression search, using pattern in Mini buffer

&lt;Control-Alt r&gt;: backward regular expression search, using pattern in Mini buffer

&lt;Alt-%&gt;: begin query search/replace. n skips to next match. y changes current match.  
        q or Return exits. ! to replace all remaining matches with no more questions
&lt;Control Alt %&gt; begin regex search replace, like Alt-%
&lt;Alt-=&gt;: count lines and characters in regions
&lt;Alt-( &gt;: insert parentheses()
&lt;Alt-) &gt;:  move past close
&lt;Control-x Control-t&gt;: transpose lines.
&lt;Control-x Control-o&gt;: delete blank lines
&lt;Control-x r s&gt;: save region to register
&lt;Control-x r i&gt;: insert to buffer from register
&lt;Control-x r +&gt;: increment register
&lt;Control-x r n&gt;: insert number 0 to register
&lt;Control-x r space &gt; : point insert point to register
&lt;Control-x r j &gt; : jump to register
&lt;Control-x x&gt;: save region to register
&lt;Control-x r r&gt; : save rectangle to register
&lt;Control-x r o&gt;: open up rectangle
&lt;Control-x r c&gt; : clear rectangle
&lt;Control-x r d&gt; : delete rectangle
&lt;Control-x r t&gt; : replace rectangle with string
&lt;Control-x r k&gt; : kill rectangle
&lt;Control-x r y&gt; : yank rectangle
&lt;Control-g&gt; : keyboard quit

&lt;Control-x = &gt; : position of cursor
&lt;Control-x . &gt; : set fill prefix
&lt;Control-x f &gt; : set the fill column
&lt;Control-x Control-b &gt; : display the buffer list
&lt;Control-x b &gt; : switch to buffer
&lt;Control-x k &gt; : kill the specified buffer
----------------------------------------

&lt;Alt - - Alt-l &gt;: lowercase previous word
&lt;Alt - - Alt-u&gt;: uppercase previous word
&lt;Alt - - Alt-c&gt;: capitalise previous word
----------------------------------------

&lt;Alt-/ &gt;: dynamic expansion
&lt;Control-Alt-/&gt;: dynamic expansion.  Expands to common prefix in buffer
----------------------------------------

Alt-x commands:

(Pressing Tab will result in auto completion of the options if an appropriate match is found</t>
<t tx="ekr.20050518064900">@killcolor

The following steps must be done to get the aspell plugin to load:

1. Install aspell-python from
    http://www.republika.pl/wmula/proj/aspell-python/

2. Make a symbolic link to aspell.so:
    cd /other/leo/lib/leo/plugins/
    ln -s /other/aspell-python/lib/python2.4/site-packages/aspell.so .

3. Edit /other/leo/lib/leo/plugins/spellpyx.py to replace the paths
    at lines 63 and 65:
    aspell_dir = r'/other/leo/lib/leo/plugins'
    aspell_bin_dir = r'/other/leo/lib/leo/plugins'</t>
<t tx="ekr.20050523073009"></t>
<t tx="ekr.20050527081321"></t>
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
<t tx="ekr.20050710094310.2"></t>
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
<t tx="ekr.20050722082741"></t>
<t tx="ekr.20050723060629"></t>
<t tx="ekr.20050723062822.14">class stateManager:
    
    def __init__( self, emacs):
        self.state = None
        self.emacs = emacs

    def hasState( self ):
        return self.state
        
    def setState( self, state ):
        self.state = state
        
    def filterTo( self, event, command ):
        return self.emacs.strategyObjects[ self.state ]( event, command )
        
    def clear( self ):
        self.state = None</t>
<t tx="ekr.20050723062822.34">def masterCommand( self, event, command ):
    '''All processing goes through here.  'consume' is a flag to the
       KeyProcessor instance indicating if it should stop the event from
       propagating by consuming the event'''

    consume = False

    if command == 'Ctrl G':  ### To do; make configurable.
        return self.keyboardQuit( event )
      
    if self._stateManager.hasState():
        return self._stateManager.filterTo( event, command )
        
    if self.callbacks.has_key( command ):
        consume = self.callbacks[ command ]( event, command )
        
    if self._stateManager2.hasState():
        self._stateManager2.filterTo( event, command )
    
    return consume</t>
<t tx="ekr.20050723062822.38">def keyboardQuit( self, event=None ):
    
    self._stateManager.clear()
    self._stateManager2.clear()
    self.minibuffer.setText( '' )
    self.clearHighlights()
    sa = stext.SimpleAttributeSet()
    sa.addAttribute( 'dy-ab', 'dy-ab' )
    sa.addAttribute( 'kb', 'kb' )
    self.clearAttributes( sa )
    self.setCommandText( "" )
    for z in self.modeStrategies:
        z.mode = None
    
    cp = self.editor.getCaretPosition()
    self.editor.setCaretPosition( cp )
    return True</t>
<t tx="ekr.20050723063811">class editCommands:

    @others</t>
<t tx="ekr.20050723063811.1">def __init__ (self,c):
    
    self.c = c

    self.mode = 'default'
    self.modeStack = []
    
    self.defaultWordChars1, self.defaultWordChars2 = self.setDefaultWordChars()
    self.wordChars1 = self.defaultWordChars1
    self.wordChars2 = self.defaultWordChars2

    self.setDefaultOptions()</t>
<t tx="ekr.20050723063811.2"></t>
<t tx="ekr.20050723063811.3">def setDefaultOptions(self):
    
    self.options = {
        'extendMovesForward':   True,  # True: moving forward may cross node boundaries.
        'extendMovesBack':      True,  # True: moving back may cross node boundaries.
        'extendFindsForward':   True,   # True: find forward may cross node boundaries.
        'extendFindsBack':      True,   # True: find back may cross node boundaries.
    }</t>
<t tx="ekr.20050723063811.4">def getOption (self,optionName):
    
    # This may change when modes get put in.
    return self.options.get(optionName)</t>
<t tx="ekr.20050723063811.5"></t>
<t tx="ekr.20050723063811.6">def findWordStart(self,s,i):
    
    while i &lt; len(s):
        if s[i] in self.wordChars1:
            return i
        else:
            i += 1
    return i</t>
<t tx="ekr.20050723063811.7">def insideWord (self,s,i):
    
    '''Return True if the char at s[i] is inside a word but does not start the word.'''
    
    return (
        0 &lt; i &lt; len(s) and
        s[i] in self.wordChars2 and
        s[i-1] in self.wordChars2
    )</t>
<t tx="ekr.20050723063811.8">def skipWord(self,s,i):
    
    while i &lt; len(s) and s[i] in self.wordChars2:
        i += 1
    return i</t>
<t tx="ekr.20050723063811.9">def startsWord (self,s,i):
    
    '''Return True if the char at s[i] is inside a word but does not start the word.'''
    
    return (
        i &lt; len(s) and 
        s[i] in self.wordChars1 and
        (i == 0 or s[i-1] not in self.wordChars1)
    )</t>
<t tx="ekr.20050723063811.10">def setDefaultWordChars (self):
    
    chars1 = '_' + string.letters
    chars2 = '_' + string.letters + string.digits
    return chars1, chars2</t>
<t tx="ekr.20050723063811.11"></t>
<t tx="ekr.20050723063811.12">def moveBackwardChar (self):
    
    c = self.c ; b = c.frame.body ; s = b.getAllText()
    i = b.getPythonInsertionPoint(s=s)
    i -= 1
    if i &gt;= 0:
        b.setPythonInsertionPoint(i)
        return True
    elif self.getOption('extendMovesBackward'): # Recursively look for words in previous nodes.
        p = c.currentPosition().moveToThreadBack()
        while p:
            s = p.bodyString()
            if len(s) &gt; 0:
                c.selectPosition(p)
                b.setPythonInsertionPoint(len(s)-1)
                return True
            else:
                p.moveToThreadBack()
        return False
    else:
        return False</t>
<t tx="ekr.20050723063811.13">def moveBackwardWord (self,i=None):
    
    c = self.c ; b = c.frame.body ; s = b.getAllText()
    if i is None: i = b.getPythonInsertionPoint(s=s)

    if self.startsWord(s,i) or self.insideWord(s,i):
        i = self.findWordStart(s,i)
    i = self.findWordStart(s,i) ###
    if self.startsWord(s,i): ###
        b.setPythonInsertionPoint(i)
        return True
    elif self.getOption('extendMovesBackward'): # Recursively look for words in previous nodes.
        p = c.currentPosition().moveToThreadBack()
        while p:
            c.selectPosition(p)
            if self.moveBackwardWord(0):
                return True
            p.moveToThreadBack()
        return False
    else:
        return False</t>
<t tx="ekr.20050723063811.14">def moveForwardChar (self):
    
    c = self.c ; b = c.frame.body ; s = b.getAllText()
    i = b.getPythonInsertionPoint(s=s)
    i += 1
    if i &lt; len(s):
        b.setPythonInsertionPoint(i)
        return True
    elif self.getOption('extendMovesForward'): # Recursively look for words in following nodes.
        p = c.currentPosition().moveToThreadNext()
        while p:
            if len(p.bodyString()) &gt; 0:
                c.selectPosition(p)
                b.setPythonInsertionPoint(0)
                return True
            else:
                p.moveToThreadNext()
        return False
    else:
        return False</t>
<t tx="ekr.20050723063811.15">def moveForwardWord (self,i=None):
    
    c = self.c ; b = c.frame.body ; s = b.getAllText()
    if i is None: i = b.getPythonInsertionPoint(s=s)

    if self.startsWord(s,i) or self.insideWord(s,i):
        i = self.skipWord(s,i)
    i = self.findWordStart(s,i)
    if self.startsWord(s,i):
        b.setPythonInsertionPoint(i)
        return True
    elif self.getOption('extendMovesForward'): # Recursively look for words in following nodes.
        p = c.currentPosition().moveToThreadNext()
        while p:
            c.selectPosition(p)
            if self.moveForwardWord(0):
                return True
            p.moveToThreadNext()
        return False
    else:
        return False</t>
<t tx="ekr.20050723063811.16"></t>
<t tx="ekr.20050723063811.17">def selectForwardWord (self):
    
    c = self ; b = c.frame.body ; s = b.getAllText()

    i = i1 = b.getPythonInsertionPoint()
    
    if i &lt; len(s) and g.is_c_id(s[i]):
        i = g.skip_c_id(s,i+1)
    
    while i &lt; len(s) and not g.is_c_id(s[i]):
        i += 1
        
    if i &lt; len(s) and g.is_c_id(s[i]):
        # b.setPythonTextSelection(i1,i)
        pass ### TODO</t>
<t tx="ekr.20050724075352.14">class controlX_handlerClass:

    '''The ControlXHandler manages how the Control-X based commands operate on the
       Emacs instance.'''    
    
    @others</t>
<t tx="ekr.20050724075352.15">def __init__ (self,emacs):

    self.emacs = emacs
    self.previous = []

    # These are set in miniBuffer.finishCreate.
    self.rect_commands = {}
    self.variety_commands = {}
    self.abbreviationDispatch = {}
    self.register_commands = {}</t>
<t tx="ekr.20050724075352.16">def __call__ (self,event,stroke):

    emacs = self.emacs

    self.previous.insert(0,event.keysym)

    if len(self.previous) &gt; 10:
        self.previous.pop()

    if stroke in ('&lt;Key&gt;','&lt;Escape&gt;'):
        return self.processKey(event)  # Weird command-specific stuff.

    if stroke in emacs.xcommands:
        emacs.xcommands [stroke](event)
        if stroke != '&lt;Control-b&gt;':
            emacs.keyboardQuit(event)

    return 'break'
</t>
<t tx="ekr.20050724075352.17">def processKey (self,event):

    b = self ; emacs = self.emacs
    previous = self.previous
    if event.keysym in ('Shift_L','Shift_R'):
        return

    if emacs.sRect:
        return emacs.stringRectangle(event)

    if (
        event.keysym == 'r' and
        emacs.rectangleCommands.rectanglemode == 0
        and not emacs.registerCommands.registermode
    ):
        return self.processRectangle(event)

    if (
        self.rect_commands.has_key(event.keysym) and
        emacs.rectangleCommands.rectanglemode == 1
    ):
        return self.processRectangle(event)

    if self.register_commands.has_key(emacs.registerCommands.registermode):
        self.register_commands [emacs.registerCommands.registermode] (event)
        return 'break'

    func = self.variety_commands.get(event.keysym)
    if func:
        emacs.stopControlX(event)
        return func(event)

    if event.keysym in ('a','i','e'):
        if self.processAbbreviation(event): return 'break'

    if event.keysym == 'g':
        l = b.get()
        if self.abbreviationDispatch.has_key(l):
            emacs.stopControlX(event)
            return self.abbreviationDispatch [l](event)

    if event.keysym == 'e':
        emacs.stopControlX(event)
        return emacs.macroCommands.executeLastMacro(event)

    if event.keysym == 'x' and previous [1] not in ('Control_L','Control_R'):
        event.keysym = 's'
        emacs.setNextRegister(event)
        return 'break'

    if event.keysym == 'Escape':
        if len(previous) &gt; 1:
            if previous [1] == 'Escape':
                return emacs.repeatComplexCommand(event)
</t>
<t tx="ekr.20050724075352.18">if 0: # Reference: actually defined in finishCreate.
    self.rect_commands = {
        'o': emacs.rectangleCommands.openRectangle,
        'c': emacs.rectangleCommands.clearRectangle,
        't': emacs.rectangleCommands.stringRectangle,
        'y': emacs.rectangleCommands.yankRectangle,
        'd': emacs.rectangleCommands.deleteRectangle,
        'k': emacs.rectangleCommands.killRectangle,
        'r': emacs.rectangleCommands.activateRectangleMethods,
    }

def processRectangle (self,event):
    
    func = self.rect_commands.get(event.keysym)
    func(event)
    return 'break'
</t>
<t tx="ekr.20050724075352.19">def processAbbreviation (self,event):

    b = self ; char = event.char

    if b.get() != 'a' and event.keysym == 'a':
        b.set('a')
        return 'break'

    elif b.get() == 'a':
        if char == 'i':
            b.set('a i')
        elif char == 'e':
            b.stopControlX(event)
            event.char = ''
            self.emacs.expandAbbrev(event)
        return 'break'</t>
<t tx="ekr.20050724075352.32">def __call__ (self,event,stroke):

    numberOfArgs, func = self.keystrokes [stroke]

    if numberOfArgs == 1:
        return func(event)
    else:
        return func(event,stroke)</t>
<t tx="ekr.20050724075352.41">def __init__ (self,c,
    tbuffer=None,miniBufferWidget=None,
    useGlobalKillbuffer=False,useGlobalRegisters=False):
    '''Sets up Emacs instance.
    
    Use tbuffer (a Tk Text widget) and miniBufferWidget (a Tk Label) if provided.
    Otherwise, the caller must call setBufferStrokes.
    
    useGlobalRegisters and useGlobalKillbuffer indicate whether to use
    global (class vars) or per-instance (ivars) for kill buffers and registers.'''
    
    self.c = c
    self.undoers = {} # Emacs instance tracks undoers given to it.
    self.useGlobalKillbuffer = useGlobalKillbuffer
    self.useGlobalRegisters = useGlobalRegisters

    # For communication between keystroke handlers and other classes.
    self.regXRpl = None # EKR: a generator: calling self.regXRpl.next() get the next value.
    self.regXKey = None
   
    # Create helper classes.  Order is important here...
    self.miniBuffer   = self.miniBufferClass(self,miniBufferWidget)
    altX_commandsDict = self.createCommandsClasses()

    # Define delegators before calling finishCreate.
    self.stateManager = self.miniBuffer.stateManager
    self.kstrokeManager = self.miniBuffer.kstrokeManager
    self.keyboardQuit   = self.miniBuffer.keyboardQuit
    self.setEvent       = self.miniBuffer.setEvent

    # Last.
    self.miniBuffer.finishCreate(altX_commandsDict)
  
    if tbuffer and miniBufferWidget:
        self.miniBuffer.setBufferStrokes(tbuffer)</t>
<t tx="ekr.20050724075352.43">def masterCommand (self,event,method,stroke):
    '''This is the central routing method of the Emacs class.
    All commands and keystrokes pass through here.'''

    special = event.keysym in ('Control_L','Control_R','Alt_L','Alt-R','Shift_L','Shift_R')
    inserted = not special or len(self.keysymhistory) == 0 or self.keysymhistory [0] != event.keysym

    if inserted:
        &lt;&lt; add character to history &gt;&gt;

    if self.emacs.macroCommands.macroing:
        &lt;&lt; handle macro &gt;&gt;

    if stroke == '&lt;Control-g&gt;':
        self.previousStroke = stroke
        return self.keyboardQuit(event)

    # Important: This effectively over-rides the handling of most keystrokes with a state.
    if self.stateManager.hasState():
        self.previousStroke = stroke
        return self.stateManager(event,stroke) # Invoke the __call__ method.

    if self.kstrokeManager.hasKeyStroke(stroke):
        self.previousStroke = stroke
        return self.kstrokeManager(event,stroke) # Invoke the __call__ method.

    if self.emacs.regXRpl: # EKR: a generator.
        try:
            self.emacs.regXKey = event.keysym
            self.emacs.regXRpl.next() # EKR: next() may throw StopIteration.
        finally:
            return 'break'

    if self.emacs.abbrevOn:
        if self.emacs.abbrevCommands._expandAbbrev(event):
            return 'break'

    if method:
        rt = method(event)
        self.previousStroke = stroke
        return rt</t>
<t tx="ekr.20050724075352.49">def addCallBackDict (self):

    '''Create callback dictionary for masterCommand.'''

    b = self ; emacs = self.emacs

    cbDict = {
    'Alt-less':     lambda event, spot = '1.0': emacs.editCommands.moveTo(event,spot),
    'Alt-greater':  lambda event, spot = 'end': emacs.editCommands.moveTo(event,spot),
    'Control-Right': lambda event, way = 1: emacs.editCommands.moveword(event,way),
    'Control-Left': lambda event, way = -1: emacs.editCommands.moveword(event,way),
    'Control-a':    lambda event, spot = 'insert linestart': emacs.editCommands.moveTo(event,spot),
    'Control-e':    lambda event, spot = 'insert lineend': emacs.editCommands.moveTo(event,spot),
    'Alt-Up':       lambda event, spot = 'insert linestart': emacs.editCommands.moveTo(event,spot),
    'Alt-Down':     lambda event, spot = 'insert lineend': emacs.editCommands.moveTo(event,spot),
    'Alt-f':        lambda event, way = 1: emacs.editCommands.moveword(event,way),
    'Alt-b':        lambda event, way = -1: emacs.editCommands.moveword(event,way),
    'Control-o':    emacs.editCommands.insertNewLine,
    'Control-k':    lambda event, frm = 'insert', to = 'insert lineend': emacs.kill(event,frm,to),
    'Alt-d':        lambda event, frm = 'insert wordstart', to = 'insert wordend': emacs.kill(event,frm,to),
    'Alt-Delete':   lambda event: emacs.deletelastWord(event),
    "Control-y":    lambda event, frm = 'insert', which = 'c': emacs.walkKB(event,frm,which),
    "Alt-y":        lambda event, frm = "insert", which = 'a': emacs.walkKB(event,frm,which),
    "Alt-k":        lambda event: emacs.killsentence(event),
    'Control-s':    None,
    'Control-r':    None,
    'Alt-c':        lambda event, which = 'cap': emacs.editCommands.capitalize(event,which),
    'Alt-u':        lambda event, which = 'up': emacs.editCommands.capitalize(event,which),
    'Alt-l':        lambda event, which = 'low': emacs.editCommands.capitalize(event,which),
    'Alt-t':        lambda event, sw = emacs.editCommands.swapSpots: emacs.editCommands.swapWords(event,sw),
    'Alt-x':        self.alt_X,
    'Control-x':    self.startControlX,
    'Control-g':    b.keyboardQuit,
    'Control-Shift-at': emacs.editCommands.setRegion,
    'Control-w':    lambda event, which = 'd': emacs.editCommands.killRegion(event,which),
    'Alt-w':        lambda event, which = 'c': emacs.editCommands.killRegion(event,which),
    'Control-t':    emacs.editCommands.swapCharacters,
    'Control-u':    None,
    'Control-l':    None,
    'Alt-z':        None,
    'Control-i':    None,
    'Alt-Control-backslash': emacs.editCommands.indentRegion,
    'Alt-m':            emacs.editCommands.backToIndentation,
    'Alt-asciicircum':  emacs.editCommands.deleteIndentation,
    'Control-d':        emacs.editCommands.deleteNextChar,
    'Alt-backslash':    emacs.editCommands.deleteSpaces,
    'Alt-g':        None,
    'Control-v':    lambda event, way = 'south': emacs.editCommands.screenscroll(event,way),
    'Alt-v':        lambda event, way = 'north': emacs.editCommands.screenscroll(event,way),
    'Alt-equal':    emacs.editCommands.countRegion,
    'Alt-parenleft':    emacs.editCommands.insertParentheses,
    'Alt-parenright':   emacs.editCommands.movePastClose,
    'Alt-percent':  None,
    'Control-c':    None,
    'Delete':       lambda event, which = 'BackSpace': self.manufactureKeyPress(event,which),
    'Control-p':    lambda event, which = 'Up': self.manufactureKeyPress(event,which),
    'Control-n':    lambda event, which = 'Down': self.manufactureKeyPress(event,which),
    'Control-f':    lambda event, which = 'Right': self.manufactureKeyPress(event,which),
    'Control-b':    lambda event, which = 'Left': self.manufactureKeyPress(event,which),
    'Control-Alt-w': None,
    'Alt-a':        emacs.editCommands.backSentence,
    'Alt-e':        emacs.editCommands.forwardSentence,
    'Control-Alt-o': emacs.editCommands.insertNewLineIndent,
    'Control-j':    emacs.editCommands.insertNewLineAndTab,
    'Alt-minus':    self.negativeArgument,
    'Alt-slash':    emacs.editCommands.dynamicExpansion,
    'Control-Alt-slash':    emacs.editCommands.dynamicExpansion2,
    'Control-u':        lambda event, keystroke = '&lt;Control-u&gt;': self.universalDispatch(event,keystroke),
    'Alt-braceright':   lambda event, which = 1: emacs.movingParagraphs(event,which),
    'Alt-braceleft':    lambda event, which = 0: emacs.movingParagraphs(event,which),
    'Alt-q':        emacs.editCommands.fillParagraph,
    'Alt-h':        emacs.editCommands.selectParagraph,
    'Alt-semicolon': emacs.editCommands.indentToCommentColumn,
    'Alt-0': lambda event, stroke = '&lt;Alt-0&gt;', number = 0: self.numberCommand(event,stroke,number),
    'Alt-1': lambda event, stroke = '&lt;Alt-1&gt;', number = 1: self.numberCommand(event,stroke,number),
    'Alt-2': lambda event, stroke = '&lt;Alt-2&gt;', number = 2: self.numberCommand(event,stroke,number),
    'Alt-3': lambda event, stroke = '&lt;Alt-3&gt;', number = 3: self.numberCommand(event,stroke,number),
    'Alt-4': lambda event, stroke = '&lt;Alt-4&gt;', number = 4: self.numberCommand(event,stroke,number),
    'Alt-5': lambda event, stroke = '&lt;Alt-5&gt;', number = 5: self.numberCommand(event,stroke,number),
    'Alt-6': lambda event, stroke = '&lt;Alt-6&gt;', number = 6: self.numberCommand(event,stroke,number),
    'Alt-7': lambda event, stroke = '&lt;Alt-7&gt;', number = 7: self.numberCommand(event,stroke,number),
    'Alt-8': lambda event, stroke = '&lt;Alt-8&gt;', number = 8: self.numberCommand(event,stroke,number),
    'Alt-9': lambda event, stroke = '&lt;Alt-9&gt;', number = 9: self.numberCommand(event,stroke,number),
    'Control-underscore': emacs.doUndo,
    'Alt-s':            emacs.editCommands.centerLine,
    'Control-z':        emacs.emacsControlCommands.suspend,
    'Control-Alt-s': emacs.searchCommands.isearchForwardRegexp,
        ### Hmmm.  the lambda doesn't call keyboardQuit
        # lambda event, stroke = '&lt;Control-s&gt;': emacs.startIncremental(event,stroke,which='regexp'),
    'Control-Alt-r': emacs.searchCommands.isearchBackwardRegexp,
        # lambda event, stroke = '&lt;Control-r&gt;': emacs.startIncremental(event,stroke,which='regexp'),
    'Control-Alt-percent': lambda event: emacs.startRegexReplace()and emacs.masterQR(event),
    'Escape':       emacs.editCommands.watchEscape,
    'Alt-colon':    emacs.editCommands.startEvaluate,
    'Alt-exclam':   emacs.emacsControlCommands.startSubprocess,
    'Alt-bar':      lambda event: emacs.emacsControlCommands.startSubprocess(event,which=1),
    }

    return cbDict
</t>
<t tx="ekr.20050724075352.52">def addRegisterItems( self ):
    
    methodDict = {
        's':        self._copyToRegister,
        'i':        self._insertRegister,
        'n':        self._numberToRegister,
        'plus':     self._incrementRegister,
        'space':    self._pointToRegister,
        'j':        self._jumpToRegister,
        'a':        lambda event,which='a': self._ToReg(event,which), # _appendToRegister
        'p':        lambda event,which='p': self._ToReg(event,which), # _prependToRegister
        'r':        self._copyRectangleToRegister,
        'view' :    self._viewRegister,
    }    
    
    helpDict = {
        's':    'copy to register',
        'i':    'insert from register',
        'plus': 'increment register',
        'n':    'number to register',
        'p':    'prepend to register',
        'a':    'append to register',
        'space':'point to register',
        'j':    'jump to register',
        'r':    'rectangle to register',
        'view': 'view register',
    }

    return methodDict, helpDict</t>
<t tx="ekr.20050724075352.61">def replaceString (self,event): # event IS used
    
    b = self.miniBuffer ; tbuffer = event.widget
    stateKind = 'rString'
    # This should not be here.
    if event.keysym in ('Control_L','Control_R'): return
    state = b.getState(stateKind)
    regex = self._useRegex
    prompt = 'Replace ' + g.choose(regex,'Regex','String')
    if state == 0:
        self._sString = self._rpString = ''
        s = '%s: ' % prompt
        b.set(s)
        # Get arg and enter state 1.
        return b.getArg(event,stateKind,1) 
    elif state == 1:
        self._sString = b.arg
        s = '%s: %s With: ' % (prompt,self._sString)
        b.set(s)
        # Get arg and enter state 2.
        return b.getArg(event,stateKind,2)
    elif state == 2:
        self._rpString = b.arg
        &lt;&lt; do the replace &gt;&gt;
        s = 'Replaced %s occurances' % count
        b.set(s)
        b.setLabelGrey()
        b.stateManager.clear()
        self._useRegex = False
        return b._tailEnd(tbuffer)</t>
<t tx="ekr.20050724075352.91">def removeRKeys (self,widget):

    mrk = 'sel'
    widget.tag_delete(mrk)
    widget.unbind('&lt;Left&gt;')
    widget.unbind('&lt;Right&gt;')
    widget.unbind('&lt;Up&gt;')
    widget.unbind('&lt;Down&gt;')</t>
<t tx="ekr.20050724075352.92">def _findMatch (self,fdict=None):
    
    '''This method returns a sorted list of matches.'''

    if not fdict:
        fdict = self.altX_commandsDict

    s = self.get().strip()
    if s:
        # pmatches = filter(lambda a: a.startswith(s),fdict)
        pmatches = [a for a in fdict if a.startswith(s)]
    else:
        pmatches = []

    pmatches.sort()
    return pmatches</t>
<t tx="ekr.20050724075352.116">def reconfigureKeyStroke (self,tbuffer,keystroke,set_to):

    '''This method allows the user to reconfigure what a keystroke does.
       This feature is alpha at best, and untested.'''

    if self.cbDict.has_key(set_to):
        command = self.cbDict [set_to]
        self.cbDict [keystroke] = command
        evstring = '&lt;%s&gt;' % keystroke
        tbuffer.bind(evstring,lambda event,meth=command: self.miniBuffer.masterCommand(event,meth,evstring))</t>
<t tx="ekr.20050724075352.161">class killBufferCommandsClass (baseCommandsClass):
    
    '''A class to manage the kill buffer.'''

    @others</t>
<t tx="ekr.20050724075352.162">def kill( self, event, frm, to  ):

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

    return self.miniBuffer._tailEnd( tbuffer )</t>
<t tx="ekr.20050724075352.163">def walkKB( self, event, frm, which ):# kb = self.iterateKillBuffer() ):

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
    return self.miniBuffer._tailEnd( tbuffer )</t>
<t tx="ekr.20050724075352.164">def deletelastWord( self, event ):
    
    #tbuffer = event.widget
    #i = tbuffer.get( 'insert' )
    self.editCommands.moveword( event, -1 )
    self.kill( event, 'insert', 'insert wordend')
    self.editCommands.moveword( event ,1 )
    return 'break'
</t>
<t tx="ekr.20050724075352.165">def killsentence( self, event, back = False ):
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
    return self.kill( event, i2, '%s + 1c' % i )</t>
<t tx="ekr.20050724075352.166">def killRegion( self, event, which ):
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
    return 'break'</t>
<t tx="ekr.20050724075352.167">def addToKillBuffer( self, text ):
    
    self.reset = True 
    
    if (
        self.miniBuffer.previousStroke in (
            '&lt;Control-k&gt;', '&lt;Control-w&gt;' ,
            '&lt;Alt-d&gt;', '&lt;Alt-Delete', '&lt;Alt-z&gt;', '&lt;Delete&gt;',
            '&lt;Control-Alt-w&gt;' )
        and len(self.killbuffer)
    ):
        self.killbuffer[ 0 ] = self.killbuffer[ 0 ] + text
        return

    self.killbuffer.insert( 0, text )</t>
<t tx="ekr.20050724075352.168">def iterateKillBuffer( self ):
    
    while 1:
        if self.killbuffer:
            self.last_clipboard = None
            for z in self.killbuffer:
                if self.reset:
                    self.reset = False
                    break        
                yield z
</t>
<t tx="ekr.20050724075352.169">def getClipboard (self,tbuffer):

    try:
        ctxt = tbuffer.selection_get(selection='CLIPBOARD')
        if not self.killbuffer or ctxt != self.last_clipboard:
            self.last_clipboard = ctxt
            if not self.killbuffer or self.killbuffer [0] != ctxt:
                return ctxt
    except: pass

    return None</t>
<t tx="ekr.20050724075352.170">class registerCommandsClass (baseCommandsClass):

    '''A class to represent registers a-z and the corresponding Emacs commands.'''

    @others</t>
<t tx="ekr.20050724075352.171">def _copyToRegister (self,event):

    if not self._chckSel(event):
        return 

    if event.keysym in string.letters:
        event.keysym = event.keysym.lower()
        tbuffer = event.widget 
        txt = tbuffer.get('sel.first','sel.last')
        self.registers[event.keysym] = txt 
        return 

    self.stopControlX(event)</t>
<t tx="ekr.20050724075352.172">def _copyRectangleToRegister (self,event):
    
    if not self._chckSel(event):
        return 
    if event.keysym in string.letters:
        event.keysym = event.keysym.lower()
        tbuffer = event.widget 
        r1, r2, r3, r4 = self.getRectanglePoints(event)
        rect =[]
        while r1&lt;=r3:
            txt = tbuffer.get('%s.%s'%(r1,r2),'%s.%s'%(r1,r4))
            rect.append(txt)
            r1 = r1+1
        self.registers[event.keysym] = rect 
    self.stopControlX(event)
</t>
<t tx="ekr.20050724075352.173">def prependToRegister (self,event):

    b = self.miniBuffer
    event.keysym = 'p'
    self.setNextRegister(event)
    b.setState('controlx',False)
</t>
<t tx="ekr.20050724075352.174">def appendToRegister (self,event):

    b = self.miniBuffer
    event.keysym = 'a'
    self.setNextRegister(event)
    b.setState('controlx',True)</t>
<t tx="ekr.20050724075352.175">def _ToReg( self, event , which):

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
        return</t>
<t tx="ekr.20050724075352.176">def _chckSel (self,event):
    
    w = event.widget

    return 'sel' in w.tag_names() and w.tag_ranges('sel')

    if 0: # old code
        if not 'sel' in event.widget.tag_names():
            return False
        if not event.widget.tag_ranges('sel'):
            return False
        return True</t>
<t tx="ekr.20050724075352.177">def _checkIfRectangle (self,event):

    b = self.miniBuffer

    if self.registers.has_key(event.keysym):
        if isinstance(self.registers[event.keysym],list):
            b.stopControlX(event)
            b.set("Register contains Rectangle, not text")
            return True

    return False</t>
<t tx="ekr.20050724075352.178">def _insertRegister (self,event):
    
    tbuffer = event.widget 
    if self.registers.has_key(event.keysym):
        if isinstance(self.registers[event.keysym],list):
            self.yankRectangle(event,self.registers[event.keysym])
        else:
            tbuffer.insert('insert',self.registers[event.keysym])
            tbuffer.event_generate('&lt;Key&gt;')
            tbuffer.update_idletasks()

    self.stopControlX(event)</t>
<t tx="ekr.20050724075352.179">def _incrementRegister (self,event):
    
    if self.registers.has_key(event.keysym):
        if self._checkIfRectangle(event):
            return 
        if self.registers[event.keysym]in string.digits:
            i = self.registers[event.keysym]
            i = str(int(i)+1)
            self.registers[event.keysym] = i 
        else:
            self.invalidRegister(event,'number')
            return 
    self.stopControlX(event)
</t>
<t tx="ekr.20050724075352.180">def _numberToRegister (self,event):
    if event.keysym in string.letters:
        self.registers[event.keysym.lower()] = str(0)
    self.stopControlX(event)</t>
<t tx="ekr.20050724075352.181">def _pointToRegister (self,event):
    if event.keysym in string.letters:
        tbuffer = event.widget 
        self.registers[event.keysym.lower()] = tbuffer.index('insert')
    self.stopControlX(event)</t>
<t tx="ekr.20050724075352.182">def _jumpToRegister (self,event):
    if event.keysym in string.letters:
        if self._checkIfRectangle(event):
            return 
        tbuffer = event.widget 
        i = self.registers[event.keysym.lower()]
        i2 = i.split('.')
        if len(i2)==2:
            if i2[0].isdigit()and i2[1].isdigit():
                pass 
            else:
                self.invalidRegister(event,'index')
                return 
        else:
            self.invalidRegister(event,'index')
            return 
        tbuffer.mark_set('insert',i)
        tbuffer.event_generate('&lt;Key&gt;')
        tbuffer.update_idletasks()
    self.stopControlX(event)</t>
<t tx="ekr.20050724075352.183">def invalidRegister (self,event,what):

    b = self.miniBuffer

    self.deactivateRegister(event)
    b.set('Register does not contain valid %s' % what)</t>
<t tx="ekr.20050724075352.184">def setNextRegister (self,event):
    
    b = self.miniBuffer

    if event.keysym=='Shift':
        return 

    if self.methodDict.has_key(event.keysym):
        b.setState('controlx',True)
        self.method = self.methodDict[event.keysym]
        self.registermode = 2
        b.set(self.helpDict[event.keysym])
    else:
        b.stopControlX(event)</t>
<t tx="ekr.20050724075352.185">def executeRegister( self, event ):

    self.method( event )
    if self.registermode: 
        self.stopControlX( event )
    return</t>
<t tx="ekr.20050724075352.186">def deactivateRegister (self,event):

    b = self.miniBuffer

    b.set('')
    b.setLabelGrey()

    self.registermode = False
    self.method = None</t>
<t tx="ekr.20050724075352.187">def _viewRegister (self,event):
    
    b = self.miniBuffer
    
    b.stopControlX(event)

    if event.keysym in string.letters:
        s = self.registers[event.keysym.lower()]
        b.set(s)</t>
<t tx="ekr.20050724075352.221">class searchCommandsClass (baseCommandsClass):
    
    '''Implements many kinds of searches.'''

    @others</t>
<t tx="ekr.20050724075352.222"></t>
<t tx="ekr.20050724075352.223">def startIncremental (self,event,stroke,which='normal'):

    b = self.miniBuffer

    state = b.getState('isearch')
    g.trace(stroke)
    
    if state == 0:
        ## ref: self.csr = { '&lt;Control-s&gt;': 'for', '&lt;Control-r&gt;':'bak' }
        self.pref = self.csr [stroke]
        b.set('isearch:',protect=True)
        b.setLabelBlue()
        b.setState('isearch',which)
    else:
        self.search(event,way=self.csr[stroke],useregex=self.useRegex())
        self.pref = self.csr [stroke]
        self.scolorizer(event)

    return 'break'</t>
<t tx="ekr.20050724075352.224">def search (self,event,way,useregex=False):

    '''This method moves the insert spot to position that matches the pattern in the miniBuffer'''

    b = self.miniBuffer ; tbuffer = event.widget
    s = b.get(ignorePrompt=True)
    if s:
        try:
            if way == 'bak': # Search backwards.
                i = tbuffer.search(s,'insert',backwards=True,stopindex='1.0',regexp=useregex)
                if not i:
                    # Start again at the bottom of the buffer.
                    i = tbuffer.search(s,'end',backwards=True,stopindex='insert',regexp=useregex)
            else: # Search forwards.
                i = tbuffer.search(s,"insert + 1c",stopindex='end',regexp=useregex)
                if not i:
                    # Start again at the top of the buffer.
                    i = tbuffer.search(s,'1.0',stopindex='insert',regexp=useregex)
        except: pass

        if i and not i.isspace():
            tbuffer.mark_set('insert',i)
            tbuffer.see('insert')

    return 'break'</t>
<t tx="ekr.20050724075352.225"># Called when from the state manager when the state is 'isearch'

def iSearch (self,event,stroke):
    
    g.trace(stroke)

    b = self.miniBuffer ; tbuffer = event.widget
    if not event.char: return

    if stroke in self.csr:
        return self.startIncremental(event,stroke)

    if event.keysym == 'Return':
        s = b.get(ignorePrompt=True)
        if s:
            return b.stopControlX(event)
        else:
            return self.startNonIncrSearch(event,self.pref)

    b.update(event)
    if event.char != '\b':
       s = b.get(ignorePrompt=True)
       z = tbuffer.search(s,'insert',stopindex='insert +%sc' % len(s))
       if not z:
           self.search(event,self.pref,useregex=self.useRegex())
    self.scolorizer(event)

    return 'break'</t>
<t tx="ekr.20050724075352.226">def scolorizer (self,event):

    b = self.miniBuffer ; tbuffer = event.widget

    stext = b.get(ignorePrompt=True)
    tbuffer.tag_delete('color')
    tbuffer.tag_delete('color1')
    if stext == '': return 'break'
    ind = '1.0'
    while ind:
        try:
            ind = tbuffer.search(stext,ind,stopindex='end',regexp=self.useRegex())
        except:
            break
        if ind:
            i, d = ind.split('.')
            d = str(int(d)+len(stext))
            index = tbuffer.index('insert')
            if ind == index:
                tbuffer.tag_add('color1',ind,'%s.%s' % (i,d))
            tbuffer.tag_add('color',ind,'%s.%s' % (i,d))
            ind = i + '.' + d
    tbuffer.tag_config('color',foreground='red')
    tbuffer.tag_config('color1',background='lightblue')</t>
<t tx="ekr.20050724075352.227">def useRegex (self):

    b = self.miniBuffer

    return b.getState('isearch') != 'normal'</t>
<t tx="ekr.20050724075352.228">@
Accessed by Control-s Enter or Control-r Enter.
Alt-x forward-search or backward-search, just looks for words...</t>
<t tx="ekr.20050724075352.229">def nonincrSearch (self,event,stroke):

    b = self.miniBuffer ; tbuffer = event.widget

    if event.keysym in ('Control_L','Control_R'): return
    state = b.getState('nonincr-search')
    if state.startswith('start'):
        state = state [5:]
        b.setState('nonincr-search',state)
        b.set('')

    if b.get() == '' and stroke == '&lt;Control-w&gt;':
        return self.startWordSearch(event,state)

    if event.keysym == 'Return':
        i = tbuffer.index('insert')
        word = b.get()
        if state == 'for':
            s = tbuffer.search(word,i,stopindex='end')
            if s: s = tbuffer.index('%s +%sc' % (s,len(word)))
        else: s = tbuffer.search(word,i,stopindex='1.0',backwards=True)
        if s: tbuffer.mark_set('insert',s)
        b.keyboardQuit(event)
        return b._tailEnd(tbuffer)
    else:
        b.update(event)
        return 'break'</t>
<t tx="ekr.20050724075352.230">def startNonIncrSearch (self,event,which):

    b = self.miniBuffer

    b.keyboardQuit(event)
    b.setState('nonincr-search','start%s' % which)
    b.setLabelBlue()
    b.set('Search:')

    return 'break'</t>
<t tx="ekr.20050724075352.231">@

Control-s(r) Enter Control-w words Enter, pattern entered is treated as a regular expression.

for example in the buffer we see:
    cats......................dogs

if we are after this and we enter the backwards look, search for 'cats dogs' if will take us to the match.</t>
<t tx="ekr.20050724075352.232">def startWordSearch (self,event,which):

    b = self.miniBuffer

    b.keyboardQuit(event)
    b.setState('word-search','start%s' % which)
    b.setLabelBlue()
    b.set('Word Search %s:' % g.choose(which=='bak','Backward','Forward'))

    return 'break'</t>
<t tx="ekr.20050724075352.233">def wordSearch (self,event):

    b = self.miniBuffer ; tbuffer = event.widget
    state = b.getState('word-search')
    if state.startswith('start'):
        state = state [5:]
        b.setState('word-search',state)
        b.set('')
    if event.keysym == 'Return':
        i = tbuffer.index('insert')
        words = b.get().split()
        sep = '[%s%s]+' % (string.punctuation,string.whitespace)
        pattern = sep.join(words)
        cpattern = re.compile(pattern)
        if state == 'for':
            txt = tbuffer.get('insert','end')
            match = cpattern.search(txt)
            if not match: return b.keyboardQuit(event)
            end = match.end()
        else:
            txt = tbuffer.get('1.0','insert') #initially the reverse words formula for Python Cookbook was going to be used.
            a = re.split(pattern,txt) #that didnt quite work right.  This one apparently does.
            if len(a) &gt; 1:
                b = re.findall(pattern,txt)
                end = len(a[-1]) + len(b[-1])
            else: return b.keyboardQuit(event)
        wdict = {'for': 'insert +%sc', 'bak': 'insert -%sc'}
        tbuffer.mark_set('insert',wdict[state] % end)
        tbuffer.see('insert')
        b.keyboardQuit(event)
        return b._tailEnd(tbuffer)
    else:
        b.update(event)
        return 'break'</t>
<t tx="ekr.20050724075352.234"># For the re-search-backward and re-search-forward Alt-x commands</t>
<t tx="ekr.20050724075352.235">def reStart (self,event,which='forward'):

    b = self.miniBuffer

    b.keyboardQuit(event)
    b.setState('re_search','start%s' % which)
    b.setLabelBlue()
    b.set('RE Search:')

    return 'break'

reSearchForward = reStart</t>
<t tx="ekr.20050724075352.236">def re_search( self, event ):

    b = self.miniBuffer ; tbuffer = event.widget
    state = b.getState( 're_search' )
    if state.startswith( 'start' ):
        state = state[ 5: ]
        b.setState( 're_search', state )
        b.set( '' )
    if event.keysym == 'Return':
        pattern = b.get()
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
            b._tailEnd( tbuffer )
            tbuffer.see( 'insert' )
        return b.keyboardQuit( event )    
    else:
        b.update( event )
        return 'break'</t>
<t tx="ekr.20050724075352.285">def doAlt_X (self,event):

    '''This method executes the correct Alt-X command'''
    
    b = self ; keysym = event.keysym

    if b.get().endswith('M-x:'):
        b.axTabList.clear() # Clear the list, new Alt-x command is in effect.
        b.set('')
    if keysym == 'Return':
        &lt;&lt; dispatch the function &gt;&gt;
    elif keysym == 'Tab':
        &lt;&lt; handle tab completion &gt;&gt;
    elif keysym == 'BackSpace':
        &lt;&lt; cut back to previous prefix and update prefix &gt;&gt;
    else:
        # Clear the list, any other character besides tab indicates that a new prefix is in effect.
        b.axTabList.clear() 
        b.update(event)

    return 'break'</t>
<t tx="ekr.20050724100334">c.prettyPrintPythonNode()</t>
<t tx="ekr.20050724102409"></t>
<t tx="ekr.20050724103251"></t>
<t tx="ekr.20050725091822.2">def __init__ (self,emacs):

    Emacs.baseCommandsClass.__init__(self,emacs) # init the base class.
    
    self.csr = { '&lt;Control-s&gt;': 'for', '&lt;Control-r&gt;':'bak' }
    self.pref = None
    
    self.qQ = None
    self.qR = None
    self.qgetQuery = False
    self.qgetReplace = False
    self.qrexecute = False
    self.querytype = 'normal'

    # For replace-string and replace-regex
    self._sString = ''
    self._rpString = ''</t>
<t tx="ekr.20050725093156">def getPublicCommands (self):
    
    return {
        'isearch-forward':          self.isearchForward,
        'isearch-backward':         self.isearchBackward,
        'isearch-forward-regexp':   self.isearchForwardRegexp,
        'isearch-backward-regexp':  self.isearchBackwardRegexp,
        
        're-search-forward':        self.reSearchForward,
        're-search-backward':       self.reSearchBackward,
        
        'search-forward':           self.searchForward,
        'search-backward':          self.searchBackward,
        'word-search-forward':      self.wordSearchForward,
        'word-search-backward':     self.wordSearchBackward,
    }</t>
<t tx="ekr.20050725093537"># Incremental...
def isearchForward (self,event):
    g.trace()
    return self.miniBuffer.keyboardQuit(event) and self.startIncremental(event,'&lt;Control-s&gt;')
    
def isearchBackward (self,event):
    g.trace()
    return self.miniBuffer.keyboardQuit(event) and self.startIncremental(event,'&lt;Control-r&gt;')
    
def isearchForwardRegexp (self,event):
    g.trace()
    return self.miniBuffer.keyboardQuit(event) and self.startIncremental(event,'&lt;Control-s&gt;',which='regexp')
    
def isearchBackwardRegexp (self,event):
    g.trace()
    return self.miniBuffer.keyboardQuit(event) and self.startIncremental(event,'&lt;Control-r&gt;',which='regexp')

# Non-incremental...
def reSearchBackward (self,event):
    return self.reStart(event,which='backward')

def searchForward (self,event):
    return self.startNonIncrSearch(event,'for')
    
def searchBackward (self,event):
    return self.startNonIncrSearch(event,'bak')
    
def wordSearchForward (self,event):
    return self.startWordSearch(event,'for')
    
def wordSearchBackward (self,event):
    return self.startWordSearch(event,'bak')</t>
<t tx="ekr.20050725112958">def finishCreate (self):

    emacs = self.emacs

    # EKR: used only below.
    def eA (event):
        if self.emacs.expandAbbrev(event):
            return 'break'

    self.stateCommands = { 
        # 1 == one parameter, 2 == all
        
        # Utility states...
        'getArg':    (2,emacs.miniBuffer.getArg),
        
        # Command states...
        'uC':               (2,emacs.miniBuffer.universalDispatch),
        'controlx':         (2,emacs.miniBuffer.doControlX),
        'isearch':          (2,emacs.searchCommands.iSearch),
        'goto':             (1,emacs.editCommands.Goto),
        'zap':              (1,emacs.editCommands.zapTo),
        'howM':             (1,emacs.editCommands.howMany),
        'abbrevMode':       (1,emacs.abbrevCommands.abbrevCommand1),
        'altx':             (1,emacs.miniBuffer.doAlt_X),
        'qlisten':          (1,emacs.queryReplaceCommands.masterQR),
        'rString':          (1,emacs.editCommands.replaceString),
        'negativeArg':      (2,emacs.miniBuffer.negativeArgument),
        'abbrevOn':         (1,eA),
        'set-fill-column':  (1,emacs.editCommands.setFillColumn),
        'chooseBuffer':     (1,emacs.bufferCommands.chooseBuffer),
        'renameBuffer':     (1,emacs.bufferCommands.renameBuffer),
        're_search':        (1,emacs.searchCommands.re_search),
        'alterlines':       (1,emacs.editCommands.processLines),
        'make_directory':   (1,emacs.fileCommands.makeDirectory),
        'remove_directory': (1,emacs.fileCommands.removeDirectory),
        'delete_file':      (1,emacs.fileCommands.deleteFile),
        'nonincr-search':   (2,emacs.searchCommands.nonincrSearch),
        'word-search':      (1,emacs.searchCommands.wordSearch),
        'last-altx':        (1,emacs.miniBuffer.executeLastAltX),
        'escape':           (1,emacs.editCommands.watchEscape),
        'subprocess':       (1,emacs.emacsControlCommands.subprocesser),
    }
</t>
<t tx="ekr.20050725115600">def __init__ (self,emacs):

    Emacs.baseCommandsClass.__init__(self,emacs) # init the base class.
    
    if emacs.useGlobalKillbuffer:
        self.killbuffer = Emacs.global_killbuffer 
    else:
        self.killbuffer = []
        
    self.kbiterator = self.iterateKillBuffer()
    self.last_clipboard = None # For interacting with system clipboard.
    self.reset = False 
</t>
<t tx="ekr.20050725120303"># backwardKillParagraph is in paragraph class.

def backwardKillSentence (self,event):
    return self.miniBuffer.keyboardQuit(event) and self._killSentence(event,back=True)
    
def backwardKillWord (self,event):
    return self.deletelastWord(event) and self.miniBuffer.keyboardQuit(event)
    
def killLine (self,event):
    self.kill(event,frm='insert',to='insert lineend') and self.miniBuffer.keyboardQuit(event)
    
def killRegion (self,event):
    return self._killRegion(event,which='d') and self.miniBuffer.keyboardQuit(event)
    
# killParagraph is in paragraph class.

def killSentence (self,event):
    return self.killsentence(event) and self.miniBuffer.keyboardQuit(event)
    
def killWord (self,event):
    return self.kill(event,frm='insert wordstart',to='insert wordend') and self.miniBuffer.keyboardQuit(event)
    
def yank (self,event):
    return self.walkKB(event,frm='insert',which='c') and self.miniBuffer.keyboardQuit(event)
    
def yankPop (self,event):
    return self.walkKB(event,frm="insert",which='a') and self.miniBuffer.keyboardQuit(event)</t>
<t tx="ekr.20050725121247">def getPublicCommands (self):
    
    return {
        'backward-kill-sentence':   self.backwardKillSentence,
        'backward-kill-word':       self.backwardKillWord,
        'kill-line':                self.killLine,
        'kill-word':                self.killWord,
        'kill-sentence':            self.killSentence,
        'kill-region':              self.killRegion,
        'yank':                     self.yank,
        'yank-pop':                 self.yankPop,
    }</t>
<t tx="ekr.20050725134243">def __init__ (self,emacs):
    
    Emacs.baseCommandsClass.__init__(self,emacs) # init the base class.

    if emacs.useGlobalRegisters:
        self.registers = Emacs.global_registers 
    else:
        self.registers = {}

    self.method = None 
    self.methodDict, self.helpDict = self.addRegisterItems()
    
    self.registermode = False # For rectangles and registers</t>
<t tx="ekr.20050725134243.1">def getPublicCommands (self):
    
    return {
        'append-to-register':           self.appendToRegister,
        'copy-rectangle-to-register':   self.copyRectangleToRegister,
        'copy-to-register':             self.copyToRegister,
        'increment-register':           self.incrementRegister,
        'insert-register':              self.insertRegister,
        'jump-to-register':             self.jumpToRegister,
        'number-to-register':           self.numberToRegister,
        'point-to-register':            self.pointToRegister,
        'prepend-to-register':          self.prependToRegister,
        'view-register':                self.viewRegister,
    }</t>
<t tx="ekr.20050725135621.1">def copyToRegister (self,event):
    return self.miniBuffer.setEvent(event,'s') and self.setNextRegister(event)
def copyRectangleToRegister (self,event):
    return self.miniBuffer.setEvent(event,'r') and self.setNextRegister(event)
def incrementRegister (self,event):
    return self.miniBuffer.setEvent(event,'plus') and self.setNextRegister(event)
def insertRegister (self,event):
    return self.miniBuffer.setEvent(event,'i') and self.setNextRegister(event)
def jumpToRegister (self,event):
    return self.miniBuffer.setEvent(event,'j') and self.setNextRegister(event)
def numberToRegister (self,event):
    return self.miniBuffer.setEvent(event,'n') and self.setNextRegister(event)
def pointToRegister (self,event):
    return self.miniBuffer.setEvent(event,'space') and self.setNextRegister(event)
def viewRegister (self,event):
    return self.miniBuffer.setEvent(event,'view') and self.setNextRegister(event)</t>
<t tx="ekr.20050726043333.1"></t>
<t tx="ekr.20050726081113"></t>
<t tx="ekr.20050726081152"></t>
<t tx="ekr.20050726081815">def __init__ (self,emacs):
    
    self.emacs = emacs 
    self.mode = None 
    self.submode = None 
    emacs.modeStrategies.append(self)
    self.registers = {}
    self.commands = {
        'copy-to-register':self.copyToRegister, 
        'insert-register':self.insertRegister, 
        'append-to-register':self.appendToRegister, 
        'prepend-to-register':self.prependToRegister, 
    }
    self.mode_command = {  # The keys should command names, not numbers.
        1:self.copyToRegister, 
        3:self.appendToRegister, 
        4:self.prependToRegister, 
    }</t>
<t tx="ekr.20050726081815.1">def __call__ (self,event,command):
    if self.mode:
        if self.mode in (1,3,4): # ('copy-to-register','append-to-register','prepend-to-register'):
            self.emacs.eventToMinibuffer(event)
            message = self.mode_command[self.mode]()
            if message and message not in (True,False):
                self.emacs.keyboardQuit(event)
                self.emacs.setCommandText(message)
                return True 
            else:
                return self.emacs.keyboardQuit(event)
        elif self.mode == 2: # 'insert-register'
            self.emacs.eventToMinibuffer(event)
            message = self.insertRegister()
            if message not in(True,False)and message:
                self.emacs.keyboardQuit(event)
                self.emacs.setCommandText(message)
                return True 
            return self.emacs.keyboardQuit(event)
    
    return self.commands[command]()</t>
<t tx="ekr.20050726081815.2"></t>
<t tx="ekr.20050726091527"></t>
<t tx="ekr.20050726094804">modifiers = event.getModifiers()
mtxt = event.getKeyModifiersText(modifiers)
ktxt = event.getKeyText(event.getKeyCode())

if mtxt == ktxt:
    command = mtxt
else:
    command = '%s %s' % (mtxt,ktxt).strip()
</t>
<t tx="ekr.20050726094804.1">editor = self.emacs.editor
doc = editor.getDocument()
pos = editor.getCaretPosition()
try:
    pc = doc.getText(pos-1,1)
    if pc in('"',"'"): return
except: pass

event.consume()
self.kTconsume = True
self.kRconsume = True
ac = self.completers [kc]
doc.insertString(pos,'%s%s' % (kc,ac),None)
editor.setCaretPosition(pos+1)
if hasattr(self.emacs.c.frame.body.editor,"autocompleter"):
    self.emacs.c.frame.body.editor.autocompleter.hideAutoBox()</t>
<t tx="ekr.20050726094804.2">self.kTconsume = True
self.kRconsume = True
event.consume()
editor = self.emacs.editor
doc = editor.getDocument()
pos = editor.getCaretPosition()
try:
    doc.insertString(pos," " * 4,None)
except: pass</t>
<t tx="ekr.20050727082959">def keyPressed (self,event):

    if not self.on and event.getKeyChar() == "&gt;":
        return

    editor = self.emacs.editor
    pos = editor.getCaretPosition()
    start = stext.Utilities.getRowStart(editor,pos)
    doc = editor.getDocument()
    txt = doc.getText(start,pos-start)
    txt = list(txt) ; txt.reverse()
    matchone = 0 ; matchtwo = 0 ; data = []
    if not text or text [0] == '/':
        return

    for z in txt:
        if z == "&lt;" and not matchone:
            matchone = 1
            data.append(z)
            continue
        elif z == "&lt;" and matchone:
            matchtwo = 1
            break
        elif matchone:
            break
        if not matchone:
            data.append(z)

    if not data: return
    elif len(data) == 1and data [0] == "&lt;": return
    elif len(data) &gt; 1and not data [-2].isalpha(): return

    if matchone and not matchtwo:
        data.reverse()
        data.insert(1,"/")
        element = ''.join(data)
        pieces = element.split()
        endelement = "%s%s" % (pieces[0],"&gt;")
        doc.insertString(pos,endelement,None)
        editor.setCaretPosition(pos)</t>
<t tx="ekr.20050727083243">def extend (self,data):

    for z in data:
        if z in self.data: continue
        self.data.append(z)
</t>
<t tx="ekr.20050727083243.1">def lookFor (self,txt):

    nwdata = []
    for z in self.data:
        if z.startswith(txt):
            nwdata.append(z)

    if len(nwdata) &gt; 0:
        nwdata.sort()
        self.current = nwdata
        self.current_iter = iter(nwdata)
        return True
    else:
        return False</t>
<t tx="ekr.20050727083243.2">def getNext (self):

    try:
        return self.current_iter.next()
    except Exception:
        self.current_iter = iter(self.current)
        return self.getNext()</t>
<t tx="ekr.20050727162112">def __init__ (self,emacs,widget):

    self.emacs = emacs
    self.c = emacs.c
    self.widget = widget # A Tk Label widget.
    # Permanently associate a Tk.StringVar with the widget.
    self.svar = Tk.StringVar()
    self.widget.configure(textvariable=self.svar)

    # Ivars.
    self.altx_history = []
    self.altX_prefix = ''
    self.keysymhistory = []
    self.previousStroke = ''
    self.svars = {}
    self.tailEnds = {} # functions to execute at the end of many Emac methods.  Configurable by environment.
    
    # For accumlated args...
    self.arg = ''
    self.afterGetArgState = None
    self.argPromptLen = 0

    # For negative arguments...
    self.negativeArg = False
    self.negArgs = {} # Set in finishCreate.

    # For alt-X commands...
    self.xcommands = None       # Done in finishCreate.
    self.altX_commandsDict = {} # Set later by finishCreate.
    self.axTabList = Tracker()
    self.x_hasNumeric = ['sort-lines','sort-fields']

    # For universal commands...
    self.uCstring = string.digits + '\b'
    self.uCdict = {
        '&lt;Alt-x&gt;': self.alt_X
    }

    self.stateManager = self.stateManagerClass(emacs) # Manages state for the master command
    self.kstrokeManager = self.keyStrokeManagerClass(emacs) # Manages some keystroke state for the master command.
    self.cxHandler = self.controlX_handlerClass(emacs) # Create the handler for Control-x commands
    
    # Delegators.  These will go away if the state helper class goes away.
    self.getState = self.stateManager.getState
    self.setState = self.stateManager.setState
    self.hasState = self.stateManager.hasState
    self.whichState = self.stateManager.whichState</t>
<t tx="ekr.20050728093027.1">def finishCreate (self,altX_commandsDict):

    emacs = self.emacs

    # Finish creating the helper classes.
    self.stateManager.finishCreate()
    self.kstrokeManager.finishCreate()
    self.cxHandler.finishCreate()

    # Finish this class.
    self.altX_commandsDict = altX_commandsDict

    self.add_ekr_altx_commands()

    # Command bindings.
    self.cbDict = self.addCallBackDict() # Creates callback dictionary, primarily used in the master command

    self.negArgs = {
        '&lt;Alt-c&gt;': self.emacs.editCommands.changePreviousWord,
        '&lt;Alt-u&gt;': self.emacs.editCommands.changePreviousWord,
        '&lt;Alt-l&gt;': self.emacs.editCommands.changePreviousWord,
    }

    self.xcommands = {
        '&lt;Control-t&gt;': emacs.editCommands.transposeLines,
        '&lt;Control-u&gt;': lambda event, way = 'up': emacs.upperLowerRegion(event,way),
        '&lt;Control-l&gt;': lambda event, way = 'low': emacs.upperLowerRegion(event,way),
        '&lt;Control-o&gt;': emacs.editCommands.removeBlankLines,
        '&lt;Control-i&gt;': emacs.fileCommands.insertFile,
        '&lt;Control-s&gt;': emacs.fileCommands.saveFile,
        '&lt;Control-x&gt;': emacs.editCommands.exchangePointMark,
        '&lt;Control-c&gt;': emacs.emacsControlCommands.shutdown,
        '&lt;Control-b&gt;': emacs.bufferCommands.listBuffers,
        '&lt;Control-Shift-at&gt;': lambda event: event.widget.selection_clear(),
        '&lt;Delete&gt;': lambda event, back = True: emacs.editCommands.killsentence(event,back),
    }</t>
<t tx="ekr.20050728103627.1">def finishCreate (self):
    
    emacs = self.emacs
    
    self.keystrokes = {
        '&lt;Control-s&gt;':      ( 2, emacs.searchCommands.startIncremental ),
        '&lt;Control-r&gt;':      ( 2, emacs.searchCommands.startIncremental ),
        '&lt;Alt-g&gt;':          ( 1, emacs.editCommands.startGoto ),
        '&lt;Alt-z&gt;':          ( 1, emacs.editCommands.startZap ),
        '&lt;Alt-percent&gt;':    ( 1, emacs.queryReplaceCommands.masterQR ),
        '&lt;Control-Alt-w&gt;':  ( 1, lambda event: 'break' ),
    }</t>
<t tx="ekr.20050728103627.2">def finishCreate (self):

    emacs = self.emacs

    self.abbreviationDispatch = {
        'a':    lambda event: emacs.abbreviationDispatch(event,1),
        'a i':  lambda event: emacs.abbreviationDispatch(event,2),
    }

    self.rect_commands = {
        'o': emacs.rectangleCommands.openRectangle,
        'c': emacs.rectangleCommands.clearRectangle,
        't': emacs.rectangleCommands.stringRectangle,
        'y': emacs.rectangleCommands.yankRectangle,
        'd': emacs.rectangleCommands.deleteRectangle,
        'k': emacs.rectangleCommands.killRectangle,
        'r': emacs.rectangleCommands.activateRectangleMethods,
    }

    self.register_commands = {
        1: emacs.registerCommands.setNextRegister,
        2: emacs.registerCommands.executeRegister,
    }

    self.variety_commands = {
        'period':       emacs.editCommands.setFillPrefix,
        'parenleft':    emacs.macroCommands.startKBDMacro,
        'parenright':   emacs.macroCommands.stopKBDMacro,
        'semicolon':    emacs.editCommands.setCommentColumn,
        'Tab':          emacs.editCommands.tabIndentRegion,
        'u':            lambda event: emacs.doUndo(event,2),
        'equal':        emacs.editCommands.lineNumber,
        'h':            emacs.editCommands.selectAll,
        'f':            emacs.editCommands.setFillColumn,
        'b':            lambda event, which = 'switch-to-buffer': emacs.setInBufferMode(event,which),
        'k':            lambda event, which = 'kill-buffer': emacs.setInBufferMode(event,which),
    }</t>
<t tx="ekr.20050728195531"></t>
<t tx="ekr.20050729094213">s = b.get().strip()

if b.axTabList.prefix and s.startswith(b.axTabList.prefix):
    b.set(b.axTabList.next()) # get next in iteration
else:
    self.altX_prefix = prefix = b.get()
    pmatches = b._findMatch()
    b.axTabList.setTabList(prefix,pmatches)
    b.set(b.axTabList.next()) # begin iteration on new list</t>
<t tx="ekr.20050729150051.1">if self.emacs.macroCommands.macroing == 2 and stroke != '&lt;Control-x&gt;':
    return self.nameLastMacro(event)
    
elif self.emacs.macroCommands.macroing == 3 and stroke != '&lt;Control-x&gt;':
    return self.getMacroName(event)
    
else:
   self.recordKBDMacro(event,stroke)
</t>
<t tx="ekr.20050729150051.2">def add_ekr_altx_commands (self):

    &lt;&lt; define dict d of abbreviations &gt;&gt;

    keys = d.keys()
    keys.sort()
    for key in keys:
        val = d.get(key)
        func = self.altX_commandsDict.get(val)
        if func:
            g.trace(('%-4s' % key),val)
            self.altX_commandsDict [key] = func
</t>
<t tx="ekr.20050729150804">d = {
    'i':    'isearch-forward', 
    'ib':   'isearch-backward',      
    'ix':   'isearch-forward-regexp',
    'irx':  'isearch-backward-regexp',
    'ixr':  'isearch-backward-regexp',
    
    'r':    'replace-string',
    'rx':   'replace-regex',

    's':    'search-forward',
    'sb':   'search-backward',
    
    'sw':   'word-search-forward',    
    'sbw':  'word-search-backward',
    'swb':  'word-search-backward',
    
    #
    # 'a1'  'abbrev-on'
    # 'a0'  'abbrev-off'
 
    ## Don't put these in: they might conflict with other abbreviatsions.
    # 'fd':   'find-dialog',
    # 'od':   'options-dialog',
    
    # At present these would be Leo Find stuff.
    # 'f':    'find',
    # 'fr':   'find-reverse',
    # 'fx':   'find-regex',
    # 'frx':  'find-regex-reverse',
    # 'fxr':  'find-regex-reverse',
    # 'fw':   'find-word',
    # 'sf':   'set-find-text',
    # 'sr':   'set-find-replace',
    # 'ss':   'script-search',
    # 'ssr':  'script-search-reverse',
    
    ## These could be shared...
    # 'tfh':  'toggle-find-search-headline',
    # 'tfb':  'toggle-find-search-body',
    # 'tfw':  'toggle-find-word',
    # 'tfn':  'toggle-find-node-only',
    # 'tfi':  'toggle-find-ignore-case',
    # 'tfmc': 'toggle-find-mark-changes',
    # 'tfmf': 'toggle-find-mark-finds',
}</t>
<t tx="ekr.20050730074556.1"># g.es('%s %s by %s' % (prompt,repr(self._sString),repr(self._rpString)),color='blue')
i = 'insert' ; end = 'end' ; count = 0
if tbuffer.tag_ranges('sel'):
    i = tbuffer.index('sel.first')
    end = tbuffer.index('sel.last')
if regex:
    txt = tbuffer.get(i,end)
    try:
        pattern = re.compile(self._sString)
    except:
        b.keyboardQuit(event)
        b.set("Illegal regular expression")
        return 'break'
    count = len(pattern.findall(txt))
    if count:
        ntxt = pattern.sub(self._rpString,txt)
        tbuffer.delete(i,end)
        tbuffer.insert(i,ntxt)
else:
    # Problem: adds newline at end of text.
    txt = tbuffer.get(i,end)
    count = txt.count(self._sString)
    if count:
        ntxt = txt.replace(self._sString,self._rpString)
        tbuffer.delete(i,end)
        tbuffer.insert(i,ntxt)</t>
<t tx="ekr.20050730074556.3">def getArg (self,event,returnStateKind=None,returnState=None):
    
    '''Accumulate an argument until the user hits return (or control-g).
    Enter the 'return' state when done.'''
    
    b = self ; stateKind = 'getArg'
    state = b.getState(stateKind)
    if not state:
        b.argPromptLen = len(b.get()) ; b.arg = ''
        b.afterGetArgState = (returnStateKind,returnState)
        b.setState(stateKind,1)
    elif event.keysym == 'Return':
        # Compute the actual arg.
        s = b.get() ; b.arg = s[b.argPromptLen:]
        # Immediately enter the caller's requested state.
        b.stateManager.clear()
        stateKind,state = self.afterGetArgState
        b.setState(stateKind,state)
        b.stateManager(event,None) # Invoke the stateManager __call__ method.
    else:
        b.update(event)
    return 'break'</t>
<t tx="ekr.20050730194026">s = b.get()
func = b.altX_commandsDict.get(s)
if func:
    if s != 'repeat-complex-command': b.altx_history.insert(0,s)
    aX = b.getState('altx')
    if (type(aX) == type(1) or aX.isdigit()) and s in b.x_hasNumeric:
        func(event,aX)
    else:
        func(event)
else:
    b.keyboardQuit(event)
    b.set('Command does not exist')</t>
<t tx="ekr.20050730194215"></t>
<t tx="ekr.20050730204051">s = self.altX_prefix

b.set(s)

if len(s) &gt; 1:
    self.altX_prefix = s[:-1]
else:
    self.altX_prefix = ''</t>
<t tx="ekr.20050730204402">@nocolor
@

- Remove all module globals except those used to redefine core classes.

** Bind emacs keystroks in Leo's core.
    - That is, modify Leo's core to uses temacs-style masterCommand method for all keystrokes.

* Complete menu work.

* Eliminate state-related tables.

* Test all commands and make unit tests.

- convertCommandName utility converts to and from emacs-style (with '-' chars) to python/leo style (with capitalization).

- Eliminate all hard constants (except for tables of defaults).

- User options:
    - 'Emacs Compatibility' option: binds keys as done in present plugin.
    - 'Emacs Menu option':  On by default: adds emacs option.
    - Get keystrokes from user options.
    - User-specified keys for alt-x, control-c, etc.</t>
<t tx="ekr.20050731084644"># Don't add multiple special characters to history.

self.keysymhistory.insert(0,event.keysym)

if len(event.char) &gt; 0:
    if len(Emacs.lossage) &gt; 99:
        Emacs.lossage.pop()
    Emacs.lossage.insert(0,event.char)

if 0: # traces
    g.trace(event.keysym,stroke)
    g.trace(self.keysymhistory)
    g.trace(Emacs.lossage)</t>
<t tx="ekr.20050731084644.1"></t>
<t tx="ekr.20050731092507"></t>
<t tx="ekr.20050731101651">@killcolor
</t>
<t tx="ekr.20050731101651.1">abbrev-mode
abbrev-prefix-mark
abort-recursive-edit
about-xemacs
activate-region
ada-make-filename-from-adaname
ada-mode
add-change-log-entry
add-change-log-entry-other-window
add-global-abbrev
add-log-convert
add-mode-abbrev
add-name-to-file
advertised-switch-to-completions
advertised-undo
align
align-current
align-entire
align-highlight-rule
align-newline-and-indent
align-regexp
align-unhighlight-rule
all-hail-emacs
all-hail-xemacs
ams-tex-mode
ansi-color-for-comint-mode-on
apache-mode
append-next-kill
append-to-buffer
append-to-file
append-to-register
apply-macro-to-region-lines
appt-add
appt-delete
apropos
apropos-command
apropos-documentation
apropos-value
apropos-zippy
arp
asm-mode
assign-last-kbd-macro-to-key
auto-compression-mode
auto-fill-mode
auto-insert
auto-revert-mode
auto-save-mode
auto-show-make-point-visible
auto-show-mode
autoconf-mode
awk-mode</t>
<t tx="ekr.20050731101651.2">back-to-indentation
background
backtrace
backward-block-of-lines
backward-char
backward-char-command
backward-delete-char
backward-delete-char-untabify
backward-kill-line
backward-kill-paragraph
backward-kill-sentence
backward-kill-sexp
backward-kill-word
backward-list
backward-or-forward-delete-char
backward-or-forward-kill-sentence
backward-or-forward-kill-sexp
backward-or-forward-kill-word
backward-other-window
backward-page
backward-paragraph
backward-sentence
backward-sexp
backward-to-indentation
backward-up-list
backward-word
balance-windows
balloon-help-minor-mode
balloon-help-mode
base64-decode-region
base64-encode-region
basic-save-buffer
bbdb
bbdb-add-or-remove-mail-alias
bbdb-apply-next-command-to-all-records
bbdb-changed
bbdb-company
bbdb-complete-name
bbdb-create
bbdb-create-ftp-site
bbdb-creation-newer
bbdb-creation-no-change
bbdb-creation-older
bbdb-delete-current-field-or-record
bbdb-delete-current-record
bbdb-dial
bbdb-display-all-records-completely
bbdb-display-record-completely
bbdb-edit-current-field
bbdb-finger
bbdb-fontify-buffer
bbdb-force-record-create
bbdb-ftp
bbdb-help
bbdb-info
bbdb-insert-new-field
bbdb-load-touchtones
bbdb-menu
bbdb-merge-file
bbdb-name
bbdb-net
bbdb-notes
bbdb-omit-record
bbdb-print
bbdb-record-edit-notes
bbdb-record-edit-property
bbdb-refile-record
bbdb-send-mail
bbdb-show-all-recipients
bbdb-snarf
bbdb-snarf-region
bbdb-submit-bug-report
bbdb-timestamp-newer
bbdb-timestamp-older
bbdb-toggle-all-records-display-layout
bbdb-toggle-records-display-layout
bbdb-transpose-fields
bbdb-whois
bbdb-www
bbdb-www-grab-homepage
bbdb-yank
bbdb/gnus-annotate-sender
bbdb/gnus-show-all-recipients
bbdb/gnus-show-records
bbdb/gnus-snarf-signature
bbdb/mh-annotate-sender
bbdb/mh-show-sender
bbdb/rmail-annotate-sender
bbdb/rmail-show-sender
bbdb/vm-annotate-sender
bbdb/vm-set-auto-folder-alist
bbdb/vm-show-all-recipients
bbdb/vm-show-records
bbdb/vm-show-sender
beginning-of-buffer
beginning-of-buffer-other-window
beginning-of-defun
beginning-of-defun-raw
beginning-of-line
beginning-of-line-text
bib-cite-minor-mode
bib-mode
bibtex-mode
binary-overwrite-mode
blackbox
blink-cursor-mode
blink-matching-open
blink-paren
bnf-mode
bookmark-bmenu-list
bookmark-delete
bookmark-insert
bookmark-insert-location
bookmark-jump
bookmark-load
bookmark-locate
bookmark-menu-delete
bookmark-menu-insert
bookmark-menu-jump
bookmark-menu-locate
bookmark-menu-rename
bookmark-relocate
bookmark-rename
bookmark-save
bookmark-set
bookmark-write
br-complete-symbol
br-env-browse
br-env-load
br-three-button-mouse
br-to-from-viewer
br-two-button-mouse
browse-url
browse-url-at-mouse
browse-url-at-point
browse-url-cci
browse-url-firefox
browse-url-galeon
browse-url-generic
browse-url-gnome-moz
browse-url-grail
browse-url-iximosaic
browse-url-kde
browse-url-lynx-emacs
browse-url-lynx-xterm
browse-url-mail
browse-url-mmm
browse-url-mosaic
browse-url-mozilla
browse-url-netscape
browse-url-of-buffer
browse-url-of-dired-file
browse-url-of-file
browse-url-of-region
browse-url-opera
browse-url-w3
browse-url-w3-gnudoit
browse-url-w3m
browse-url-w3m-gnudoit
bsh-script-help
buffer-disable-undo
buffer-enable-undo
buffer-flush-undo
buffer-menu
buffer-menu-other-window
build
build-report
build-version
bury-buffer
byte-compile-and-load-file
byte-compile-buffer
byte-compile-file
byte-force-recompile
byte-recompile-directory
byte-recompile-file</t>
<t tx="ekr.20050731101651.3">c++-browse
c++-mode
c-add-style
c-comment-edit
c-macro-expand
c-mode
c-set-offset
c-set-style
calc
calc-dispatch
calc-embedded
calc-embedded-activate
calc-grab-rectangle
calc-grab-region
calc-keypad
calc-tutorial
calendar
call-last-kbd-macro
call-tree
caml-mode
camldebug
cancel-debug-on-entry
canonically-space-region
capitalize-region
capitalize-region-as-title
capitalize-region-or-word
capitalize-word
cd
cde-start-drag
cde-start-drag-region
center-line
center-paragraph
center-region
center-to-window-line
change-log-merge
change-log-mode
change-log-redate
check-ispell-version
checkdoc
checkdoc-continue
checkdoc-current-buffer
checkdoc-defun
checkdoc-eval-current-buffer
checkdoc-eval-defun
checkdoc-interactive
checkdoc-ispell
checkdoc-ispell-comments
checkdoc-ispell-continue
checkdoc-ispell-current-buffer
checkdoc-ispell-defun
checkdoc-ispell-interactive
checkdoc-ispell-message-interactive
checkdoc-ispell-message-text
checkdoc-ispell-start
checkdoc-message-interactive
checkdoc-message-text
checkdoc-minor-mode
checkdoc-rogue-spaces
checkdoc-start
choose-completion
clear-profiling-info
clear-rectangle
clearcase-install
clearcase-integrate
clearcase-unintegrate
clos-browse
column-number-mode
comint-dynamic-complete
comint-mode
comint-run
command-apropos
command-history-mode
comment-region
compare-windows
compilation-minor-mode
compilation-mode
compilation-shell-minor-mode
compile
compile-defun
complete
completion-do-in-minibuffer
completion-list-mode
completion-list-mode-quit
completion-switch-to-minibuffer
compose-mail
compose-mail-other-frame
compose-mail-other-window
consing-since-gc
context-en-mode
context-nl-mode
conx
conx-buffer
conx-load
conx-region
copy-file
copy-from-above-command
copy-primary-selection
copy-rectangle-to-register
copy-region-as-kill
copy-to-buffer
copy-to-register
count-lines-buffer
count-lines-page
count-lines-region
count-matches
count-words-buffer
count-words-region
cperl-mode
cperl-perldoc
cperl-perldoc-at-point
css-mode
ctypes-all-buffers
ctypes-auto-parse-mode
ctypes-buffer
ctypes-define-type
ctypes-define-type-in-mode
ctypes-dir
ctypes-file
ctypes-read-file
ctypes-tags
customize
customize-apropos
customize-apropos-faces
customize-apropos-groups
customize-apropos-options
customize-browse
customize-changed-options
customize-customized
customize-face
customize-face-other-window
customize-group
customize-group-other-window
customize-option
customize-option-other-window
customize-other-window
customize-save-customized
customize-save-variable
customize-saved
customize-set-value
customize-set-variable
customize-variable
customize-variable-other-window
cvs-checkout
cvs-examine
cvs-log-mode
cvs-quickdir
cvs-status
cvs-status-mode
cvs-update</t>
<t tx="ekr.20050731101651.4">dabbrev-completion
dabbrev-expand
dbx
debug
debug-on-entry
decipher
decipher-mode
decrease-left-margin
decrease-right-margin
define-abbrevs
define-global-abbrev
define-mail-alias
define-mode-abbrev
defining-kbd-macro
delete-backward-char
delete-blank-lines
delete-char
delete-completion-window
delete-directory
delete-file
delete-frame
delete-horizontal-space
delete-indentation
delete-matching-lines
delete-non-matching-lines
delete-other-frames
delete-other-windows
delete-primary-selection
delete-rectangle
delete-region
delete-selection-mode
delete-window
delete-windows-on
deprecated-help-command
describe-beta
describe-bindings
describe-buffer-case-table
describe-class
describe-copying
describe-current-display-table
describe-distribution
describe-function
describe-function-arglist
describe-function-at-point
describe-generic
describe-installation
describe-key
describe-key-briefly
describe-last-error
describe-method
describe-mode
describe-no-warranty
describe-pointer
describe-prefix-bindings
describe-project
describe-stroke
describe-syntax
describe-variable
describe-variable-at-point
desktop-entry-mode
desktop-read
diary
diary-mail-entries
dictionary
dictionary-lookup-definition
dictionary-match-words
dictionary-mouse-popup-matching-words
dictionary-popup-matching-words
dictionary-search
diff
diff-backup
diff-minor-mode
diff-mode
digit-argument
directory-tree-thing
dired
dired-apropos
dired-backup-diff
dired-cleanup
dired-compress-subdir-files
dired-describe-mode
dired-diff
dired-do-background-shell-command
dired-do-compress
dired-do-copy-regexp
dired-do-grep
dired-do-hardlink-regexp
dired-do-igrep
dired-do-igrep-find
dired-do-print
dired-do-relsymlink-regexp
dired-do-rename-regexp
dired-do-shell-command
dired-do-symlink-regexp
dired-do-uucode
dired-downcase
dired-ediff
dired-emerge
dired-emerge-with-ancestor
dired-epatch
dired-flag-extension
dired-flag-files-regexp
dired-jump-back
dired-jump-back-other-frame
dired-jump-back-other-window
dired-mark-extension
dired-mark-files-compilation-buffer
dired-mark-files-from-other-dired-buffer
dired-mark-files-regexp
dired-mark-sexp
dired-other-frame
dired-other-window
dired-read-mail
dired-report-bug
dired-rmail
dired-summary
dired-upcase
dired-virtual
dired-vm
disable-command
disassemble
display-buffer
display-call-tree
display-column-mode
display-time
dissociated-press
dns-mode
dns-mode-soa-increment-serial
do-auto-save
docbook-grep
docbook-mode
docref-setup
doctor
down-list
downcase-region
downcase-region-or-word
downcase-word
drag-window-divider
dsssl-mode
dunnet</t>
<t tx="ekr.20050731101651.5">ebuffers
ebuffers3
ecb-activate
ecb-byte-compile
ecb-minor-mode
ecb-show-help
edebug-defun
edebug-eval-top-level-form
ediff
ediff-backup
ediff-buffers
ediff-buffers3
ediff-customize
ediff-directories
ediff-directories3
ediff-directory-revisions
ediff-documentation
ediff-files
ediff-files3
ediff-merge
ediff-merge-buffers
ediff-merge-buffers-with-ancestor
ediff-merge-directories
ediff-merge-directories-with-ancestor
ediff-merge-directory-revisions
ediff-merge-directory-revisions-with-ancestor
ediff-merge-files
ediff-merge-files-with-ancestor
ediff-merge-revisions
ediff-merge-revisions-with-ancestor
ediff-merge-with-ancestor
ediff-patch-buffer
ediff-patch-file
ediff-regions-linewise
ediff-regions-wordwise
ediff-revision
ediff-show-registry
ediff-toggle-multiframe
ediff-toggle-use-toolbar
ediff-version
ediff-windows-linewise
ediff-windows-wordwise
ediff3
edir-merge-revisions
edir-merge-revisions-with-ancestor
edir-revisions
edirs
edirs-merge
edirs-merge-with-ancestor
edirs3
edit-abbrevs
edit-abbrevs-mode
edit-abbrevs-redefine
edit-bookmarks
edit-faces
edit-itimers
edit-kbd-macro
edit-last-kbd-macro
edit-mime
edit-named-kbd-macro
edit-picture
edit-pr
edit-tab-stops
edit-tab-stops-note-changes
edit-toolbar
edt-emulation-on
edt-set-scroll-margins
efs-display-ftp-activity
efs-nslookup-host
efs-report-bug
efs-set-passwd
efs-set-user
eieio-class-tree
eieio-describe-class
eieio-describe-generic
eieio-describe-method
eif-browse
eiffel-mode
eldoc-mode
electric-buffer-list
electric-command-history
electric-nroff-mode
elp-instrument-function
elp-instrument-list
elp-instrument-package
elp-results
emacs-lisp-byte-compile
emacs-lisp-byte-compile-and-load
emacs-lisp-mode
emacs-version
emerge
emerge-buffers
emerge-buffers-with-ancestor
emerge-files
emerge-files-with-ancestor
emerge-merge-directories
emerge-revisions
emerge-revisions-with-ancestor
enable-command
enable-flow-control
encrypt-insert-file-contents
end-kbd-macro
end-of-buffer
end-of-buffer-other-window
end-of-defun
end-of-line
enlarge-window
enlarge-window-horizontally
enlarge-window-pixels
enriched-mode
epatch
epatch-buffer
erase-buffer
erc-add-dangerous-host
erc-add-fool
erc-add-keyword
erc-add-pal
erc-autojoin-mode
erc-button-mode
erc-chanlist
erc-cmd-LIST
erc-complete
erc-completion-mode
erc-delete-dangerous-host
erc-delete-fool
erc-delete-keyword
erc-delete-pal
erc-fill-mode
erc-log-mode
erc-nickserv-identify
erc-nickserv-identify-mode
erc-notify-mode
erc-ring-mode
erc-save-buffer-in-logs
erc-select
erc-server-select
erc-services-mode
erc-spelling-mode
erc-timestamp-mode
erc-track-mode
erc-track-when-inactive-mode
erc-truncate-buffer
erc-truncate-mode
erc-xdcc-add-file
eregistry
erevision
escreen-install
eshell
eshell-command
eshell-report-bug
eshell-test
eshell-toggle
eshell-toggle-cd
eudc-edit-hotlist
eudc-expand-inline
eudc-get-email
eudc-get-phone
eudc-insert-record-at-point-into-bbdb
eudc-load-eudc
eudc-query-form
eudc-set-server
eudc-try-bbdb-insert
eval-buffer
eval-current-buffer
eval-defun
eval-expr
eval-expr-install
eval-expression
eval-last-sexp
eval-print-last-sexp
eval-region
exchange-dot-and-mark
exchange-point-and-mark
executable-self-display
executable-set-magic
execute-extended-command
exit-minibuffer
exit-recursive-edit
expand-abbrev
expand-region-abbrevs</t>
<t tx="ekr.20050731101651.6">f90-mode
facemenu-make-larger
facemenu-make-much-larger
facemenu-make-much-smaller
facemenu-make-smaller
facemenu-remove-props
facemenu-remove-special
facemenu-set-background
facemenu-set-face
facemenu-set-face-from-menu
facemenu-set-foreground
facemenu-set-intangible
facemenu-set-invisible
facemenu-set-read-only
facemenu-set-size-default
fast-lock-mode
feedmail-queue-reminder
feedmail-run-the-queue
feedmail-run-the-queue-global-prompt
feedmail-run-the-queue-no-prompts
ffap
ffap-at-mouse
ffap-menu
ffap-next
fill-individual-paragraphs
fill-nonuniform-paragraphs
fill-paragraph
fill-paragraph-or-region
fill-region
fill-region-as-paragraph
find-alternate-file
find-alternate-file-other-window
find-file
find-file-at-point
find-file-other-frame
find-file-other-window
find-file-read-only
find-file-read-only-other-frame
find-file-read-only-other-window
find-function
find-function-at-point
find-function-on-key
find-function-other-frame
find-function-other-window
find-library
find-library-other-frame
find-library-other-window
find-tag
find-tag-at-point
find-tag-other-window
find-variable
find-variable-at-point
find-variable-other-frame
find-variable-other-window
finder-by-keyword
finder-commentary
finger
first-error
fixup-whitespace
flame
floating-toolbar
floating-toolbar-from-extent-or-popup-mode-menu
floating-toolbar-or-popup-mode-menu
flush-lines
flyspell-buffer
flyspell-mode
flyspell-prog-mode
flyspell-region
flyspell-version
folding-mode
folding-mode-add-find-file-hook
font-lock-fontify-buffer
font-lock-mode
footnote-mode
format-decode-buffer
format-decode-region
format-encode-buffer
format-encode-region
format-find-file
format-insert-file
format-write-file
forms-find-file
forms-find-file-other-window
forms-mode
fortran-mode
forward-block-of-lines
forward-char
forward-char-command
forward-line
forward-list
forward-page
forward-paragraph
forward-sentence
forward-sexp
forward-to-indentation
forward-word
frame-configuration-to-register
ftelnet
ftp
full-calc
full-calc-keypad
fume-mode
fume-setup-buffer
function-menu
fundamental-mode
fusion-mode</t>
<t tx="ekr.20050731101651.7">garbage-collect
gdb
gdb-with-core
gdbsrc
generate-file-autoloads
generic-page-setup
generic-print-buffer
getenv
global-auto-revert-mode
global-semantic-auto-parse-mode
global-semantic-show-dirty-mode
global-semantic-show-unmatched-syntax-mode
global-semantic-summary-mode
global-semanticdb-minor-mode
global-senator-minor-mode
global-set-key
global-set-stroke
global-unset-key
gnats:edit-pr
gnats:query-pr
gnats:summ-pr
gnats:view-pr
gnuserv-start
gomoku
google-query
google-query-region
goto-address
goto-address-at-mouse
goto-address-at-point
goto-char
goto-line
grep
grep-all-files-in-current-directory
grep-all-files-in-current-directory-and-below
grep-find
gtk-start-drag
gtk-start-drag-region</t>
<t tx="ekr.20050731102358">Buffer-menu-1-window
Buffer-menu-2-window
Buffer-menu-backup-unmark
Buffer-menu-delete
Buffer-menu-delete-backwards
Buffer-menu-execute
Buffer-menu-igrep
Buffer-menu-mark
Buffer-menu-maybe-mouse-select
Buffer-menu-mouse-select
Buffer-menu-not-modified
Buffer-menu-other-window
Buffer-menu-popup-menu
Buffer-menu-quit
Buffer-menu-save
Buffer-menu-select
Buffer-menu-switch-other-window
Buffer-menu-this-window
Buffer-menu-toggle-read-only
Buffer-menu-unmark
Buffer-menu-visit-tags-table</t>
<t tx="ekr.20050731102358.1">hanoi
haskell-doc-mode
haskell-doc-show-type
haskell-mode
help
help-for-help
help-mode
help-mode-bury
help-mode-quit
help-next-section
help-next-symbol
help-prev-section
help-prev-symbol
help-quit
help-with-tutorial
hexl-find-file
hexl-mode
hexlify-buffer
hide-copyleft-region
hide-ifdef-mode
highlight-headers-follow-url
highlight-headers-follow-url-kfm
highlight-headers-follow-url-mosaic
highlight-headers-follow-url-netscape
highline-customize
highline-local-mode
highline-mode
highline-mode-off
highline-mode-on
highline-off
highline-on
highline-view-mode
highline-view-off
highline-view-on
hippie-expand
hm--html-minor-mode
hm--html-mode
hmail:compose
holidays
how-many
hs-minor-mode
html-mode
html-quote-region
html-view-get-display
html-view-goto-url
html-view-start-mosaic
html-view-view-buffer
html-view-view-file
htmlize-buffer
htmlize-file
htmlize-many-files
htmlize-many-files-dired
htmlize-region
hyper-apropos
hyper-apropos-popup-menu
hyper-apropos-set-variable
hyper-describe-face
hyper-describe-function
hyper-describe-key
hyper-describe-key-briefly
hyper-describe-variable
hyper-set-variable
hyper-where-is
hyperb:customize
hyperb:find-file-urls-mode
hyperb:init-menubar
hyperbole
hypropos-popup-menu
hypropos-set-variable</t>
<t tx="ekr.20050731102358.2">ibuffer
ibuffer-add-saved-filters
ibuffer-add-to-tmp-hide
ibuffer-add-to-tmp-show
ibuffer-auto-mode
ibuffer-backward-filter-group
ibuffer-backwards-next-marked
ibuffer-bs-show
ibuffer-clear-filter-groups
ibuffer-copy-filename-as-kill
ibuffer-customize
ibuffer-decompose-filter
ibuffer-delete-saved-filter-groups
ibuffer-delete-saved-filters
ibuffer-diff-with-file
ibuffer-do-kill-lines
ibuffer-do-occur
ibuffer-exchange-filters
ibuffer-filter-disable
ibuffer-filters-to-filter-group
ibuffer-forward-next-marked
ibuffer-invert-sorting
ibuffer-jump-to-buffer
ibuffer-jump-to-filter-group
ibuffer-kill-filter-group
ibuffer-kill-line
ibuffer-list-buffers
ibuffer-mark-by-file-name-regexp
ibuffer-mark-by-mode
ibuffer-mark-by-mode-regexp
ibuffer-mark-by-name-regexp
ibuffer-mark-dired-buffers
ibuffer-mark-dissociated-buffers
ibuffer-mark-help-buffers
ibuffer-mark-modified-buffers
ibuffer-mark-old-buffers
ibuffer-mark-read-only-buffers
ibuffer-mark-special-buffers
ibuffer-mark-unsaved-buffers
ibuffer-negate-filter
ibuffer-or-filter
ibuffer-other-window
ibuffer-pop-filter
ibuffer-pop-filter-group
ibuffer-save-filter-groups
ibuffer-save-filters
ibuffer-set-filter-groups-by-mode
ibuffer-switch-to-saved-filter-groups
ibuffer-switch-to-saved-filters
ibuffer-toggle-sorting-mode
ibuffer-yank
icomplete-mode
icon-mode
iconify-emacs
iconify-frame
id-select-and-copy-thing
id-select-and-kill-thing
id-select-goto-matching-tag
id-select-install
id-select-thing
id-select-thing-with-mouse
idl-mode
idlwave-mode
idlwave-shell
ielm
ifconfig
ignore
igrep
igrep-find
igrep-insinuate
igrep-visited-files
ilisp-imenu-add-menubar-index
image-mode
imenu
imenu-add-menubar-index
imenu-add-to-menubar
increase-left-margin
increase-right-margin
increment-register
indent-according-to-mode
indent-code-rigidly
indent-for-comment
indent-for-tab-command
indent-new-comment-line
indent-region
indent-relative
indent-relative-maybe
indent-rigidly
indent-sexp
indent-to
indent-to-column
indented-text-mode
inferior-prolog-mode
inferior-tcl
info
info-browse
info-complete-file
info-complete-symbol
info-lookup-file
info-lookup-reset
info-lookup-symbol
insert-abbrevs
insert-buffer
insert-file
insert-kbd-macro
insert-key-binding
insert-parentheses
insert-register
insert-selection
insert-zippyism
install-where-was-i
inverse-add-global-abbrev
inverse-add-mode-abbrev
invert-face
ipconfig
isearch-*-char
isearch-abort
isearch-backward
isearch-backward-regexp
isearch-cancel
isearch-complete
isearch-complete-edit
isearch-delete-char
isearch-edit-string
isearch-exit
isearch-forward
isearch-forward-exit-minibuffer
isearch-forward-regexp
isearch-help-or-delete-char
isearch-mode-help
isearch-nonincremental-exit-minibuffer
isearch-printing-char
isearch-quote-char
isearch-repeat-backward
isearch-repeat-forward
isearch-return-char
isearch-reverse-exit-minibuffer
isearch-ring-advance
isearch-ring-advance-edit
isearch-ring-retreat
isearch-ring-retreat-edit
isearch-toggle-case-fold
isearch-toggle-regexp
isearch-whitespace-chars
isearch-yank-clipboard
isearch-yank-kill
isearch-yank-line
isearch-yank-selection
isearch-yank-sexp
isearch-yank-word
isearch-yank-x-clipboard
isearch-yank-x-selection
isearch-|-char
iso-accents-mode
ispell
ispell-buffer
ispell-change-dictionary
ispell-comments-and-strings
ispell-complete-word
ispell-complete-word-interior-frag
ispell-continue
ispell-kill-ispell
ispell-message
ispell-minor-mode
ispell-pdict-save
ispell-region
ispell-word
iswitchb-buffer
iswitchb-buffer-other-frame
iswitchb-buffer-other-window
iswitchb-default-keybindings
iswitchb-display-buffer
itimer-edit-delete-itimer
itimer-edit-help
itimer-edit-next-field
itimer-edit-previous-field
itimer-edit-quit
itimer-edit-set-field</t>
<t tx="ekr.20050731102358.3">japanese-latex-mode
japanese-plain-tex-mode
java-browse
java-mode
javascript-mode
javascript-shell
jde-ant-build
jde-ant-projecthelp
jde-ant-show-options
jde-bug-debug-app
jde-build
jde-checkstyle
jde-checkstyle-customize
jde-compile
jde-compile-jde
jde-create-new-project
jde-db-set-app-args
jde-db-set-args
jde-db-set-debugger
jde-ejb-entity-bean-buffer
jde-ejb-session-bean-buffer
jde-gen-buffer
jde-gen-class-buffer
jde-gen-console-buffer
jde-gen-interface-buffer
jde-gen-jfc-app-buffer
jde-gen-junit-test-class-buffer
jde-help-browse-jdk-doc
jde-import-organize
jde-java-font-lock-setup-keywords
jde-javadoc-autodoc-at-line
jde-javadoc-checkdoc
jde-javadoc-checkdoc-at-line
jde-javadoc-checker-fix
jde-javadoc-checker-next
jde-javadoc-checker-previous
jde-javadoc-checker-quit
jde-javadoc-customize
jde-javadoc-make
jde-jdb
jde-jdb-applet
jde-make
jde-make-show-options
jde-mode
jde-open-project-file
jde-package-update
jde-run
jde-run-applet
jde-run-set-app
jde-run-set-app-args
jde-run-set-applet-doc
jde-run-set-applet-viewer
jde-run-set-args
jde-save-project
jde-set-compile-options
jde-set-global-classpath
jde-show-help
jde-stat-loc-report
jde-stat-loc-report-directory
jde-stat-loc-report-project
jde-xref-customize
jde-xref-display-call-tree
jde-xref-first-caller
jde-xref-list-uncalled-functions
jde-xref-make-xref-db
jde-xref-next-caller
jde-xref-update
join-line
jump-to-register
just-one-space
justify-current-line</t>
<t tx="ekr.20050731102358.4">kbd-macro-query
keep-lines
keyboard-escape-quit
keyboard-quit
kfile:find
kfile:view
kill-all-abbrevs
kill-buffer
kill-buffer-and-window
kill-comment
kill-console-local-variable
kill-emacs
kill-entire-line
kill-line
kill-local-variable
kill-paragraph
kill-primary-selection
kill-rectangle
kill-region
kill-ring-save
kill-sentence
kill-sexp
kill-some-buffers
kill-this-buffer
kill-word
kimport:aug-post-outline
kimport:file
kimport:star-outline
kimport:text
klink:create
kotl-mode
kotl-mode:example
ksh-mode</t>
<t tx="ekr.20050731102358.5">latex-mode
lazy-lock-mode
lazy-shot-mode
ledit-mode
liece
life
line-number-mode
linuxdoc-sgml-mode
lisp-complete-symbol
lisp-fill-paragraph
lisp-indent-for-comment
lisp-indent-line
lisp-interaction-mode
lisp-mode
lisp-send-defun
list-abbrevs
list-bookmarks
list-buffers
list-colors-display
list-command-history
list-directory
list-faces-display
list-holidays
list-itimers
list-load-path-shadows
list-matches-in-buffers
list-matching-lines
list-mode
list-mode-item-keyboard-selected
list-mode-item-mouse-selected
list-packages
list-processes
list-strokes
list-tags
list-text-properties-at
list-yahrzeit-dates
literate-haskell-mode
load-default-sounds
load-file
load-library
load-sound-file
load-user-strokes
local-set-key
local-unset-key
locate-library
lock-buffer
lower-frame
lpr-buffer
lpr-region
lua-mode</t>
<t tx="ekr.20050731102358.6">m4-mode
macroexpand-all-sexp
macroexpand-sexp
mail
mail-mode
mail-other-frame
mail-other-window
make-command-summary
make-compatible
make-compatible-variable
make-directory
make-directory-path
make-face-bold
make-face-bold-italic
make-face-italic
make-face-larger
make-face-smaller
make-face-unbold
make-face-unitalic
make-file-part
make-frame
make-indirect-buffer
make-local-variable
make-obsolete
make-obsolete-variable
make-search-dialog
make-symbolic-link
make-variable-buffer-local
makefile-mode
manual-entry
map-query-replace-regexp
mark-beginning-of-buffer
mark-bob
mark-defun
mark-end-of-buffer
mark-end-of-line
mark-end-of-sentence
mark-eob
mark-page
mark-paragraph
mark-sexp
mark-whole-buffer
mark-word
maybe-unmigrate-user-init-file
mchat
mchat-other-frame
metamail-buffer
metamail-interpret-body
metamail-interpret-header
metamail-region
mew
mew-send
mh-letter-mode
mh-nmail
mh-rmail
mh-smail
mh-smail-other-window
mh-version
migrate-user-init-file
mime-decode-region
mime-encode-region
mime-insert-encoded-file
mime/editor-mode
minibuffer-complete
minibuffer-complete-and-exit
minibuffer-complete-word
minibuffer-completion-help
minibuffer-electric-separator
minibuffer-electric-tilde
minibuffer-keyboard-quit
minibuffer-smart-maybe-select-highlighted-completion
minibuffer-smart-select-highlighted-completion
mode-compile
mode-compile-kill
mode-compile-submit-bug-report
modeline-buffers-menu
modeline-menu
modeline-minor-mode-menu
modeline-toggle-read-only
modify-syntax-entry
modula-2-mode
morse-region
mouse-avoidance-mode
mouse-bury-buffer
mouse-choose-completion
mouse-consolidated-yank
mouse-del-char
mouse-delete-window
mouse-drag-modeline
mouse-eval-last-sexpr
mouse-eval-sexp
mouse-ignore
mouse-keep-one-window
mouse-kill-line
mouse-line-length
mouse-me
mouse-scroll
mouse-select
mouse-select-and-split
mouse-set-mark
mouse-set-point
mouse-track
mouse-track-adjust
mouse-track-adjust-default
mouse-track-default
mouse-track-delete-and-insert
mouse-track-do-rectangle
mouse-track-insert
mouse-unbury-buffer
mouse-window-to-region
mouse-yank
move-past-close-and-reindent
move-to-left-margin
move-to-tab-stop
move-to-window-line
mpuz
mswindows-paste-clipboard
mwheel-install</t>
<t tx="ekr.20050731102358.7">name-last-kbd-macro
narrow-stack-mode
narrow-to-defun
narrow-to-page
narrow-to-region
narrow-window-to-region
negative-argument
netstat
network-connection
network-connection-to-service
new-frame
newline
newline-and-indent
next-complete-history-element
next-error
next-file
next-history-element
next-line
next-list-mode-item
next-matching-history-element
next-multiframe-window
normal-mode
not-modified
nroff-mode
nslookup
nslookup-host
nuke-nroff-bs
nuke-selective-display
number-to-register</t>
<t tx="ekr.20050731102358.8">objc-browse
objc-mode
occur
occur-mode-goto-occurrence
occur-mode-mouse-goto
offix-start-drag
offix-start-drag-region
old-whitespace-incremental-mode
old-whitespace-mode
oo-browser
open-dribble-file
open-line
open-rectangle
open-termscript
other-frame
other-window
outl-mouse-minor-mode
outl-mouse-mode
outline-minor-mode
outline-mode
overstrike-region
overwrite-mode
own-selection</t>
<t tx="ekr.20050731102358.9">package-admin-add-binary-package
package-admin-add-single-file-package
package-get
package-get-all
package-get-custom
package-get-delete-package
package-get-package-provider
package-get-save-base
package-get-update-all
package-get-update-base
package-get-update-base-from-buffer
paragraph-indent-text-mode
paren-activate
paren-backward-sexp
paren-deactivate
paren-forward-sexp
paren-set-mode
paren-toggle-matching-paired-delimiter
paren-toggle-matching-quoted-paren
paren-toggle-open-paren-context
pascal-mode
patch-to-change-log
patcher-mail
patcher-mail-subproject
patcher-version
pcomplete
pcomplete-continue
pcomplete-expand
pcomplete-expand-and-complete
pcomplete-help
pcomplete-list
pcomplete-reverse
pdb
pending-delete
pending-delete-mode
pending-delete-off
pending-delete-on
perl-mode
perldb
permanent-buffers-mode
pgg-decrypt
pgg-decrypt-region
pgg-encrypt
pgg-encrypt-region
pgg-insert-key
pgg-sign
pgg-sign-region
pgg-snarf-keys
pgg-snarf-keys-region
pgg-verify
pgg-verify-region
phases-of-moon
php-mode
picture-mode
pike-mode
ping
plain-TeX-mode
plain-tex-mode
play-sound-file
point-to-register
pop-global-mark
pop-tag-mark
pop-window-configuration
popper-install
popup-buffer-menu
popup-menubar-menu
popup-mode-menu
posix-search-backward
posix-search-forward
postscript-mode
pp-eval-expression
pp-eval-last-sexp
pp-function
pp-plist
pp-variable
praise-be-unto-emacs
praise-be-unto-xemacs
prefer-coding-system
prefix-region
prepend-to-buffer
prepend-to-register
press-toolbar-button
prettyexpand-all-sexp
prettyexpand-sexp
previous-complete-history-element
previous-error
previous-history-element
previous-line
previous-list-mode-item
previous-matching-history-element
previous-multiframe-window
print-buffer
print-region
profile-command
profile-expression
profile-key-sequence
profile-results
prolog-mode
ps
ps-despool
ps-line-lengths
ps-nb-pages-buffer
ps-nb-pages-region
ps-print-buffer
ps-print-buffer-with-faces
ps-print-customize
ps-print-region
ps-print-region-with-faces
ps-spool-buffer
ps-spool-buffer-with-faces
ps-spool-region
ps-spool-region-with-faces
psychoanalyze-pinhead
pui-add-install-directory
pui-list-packages
push-window-configuration
pwd
py-shell
pydoc-apropos
pydoc-commands
pydoc-help
pydoc-keywords
pydoc-modules
pydoc-packages
pydoc-topics
pydoc-xrefs
pymacs-eval
pymacs-load
python-browse
python-mode</t>
<t tx="ekr.20050731102358.10">query-pr
query-replace
query-replace-regexp
quick-calc
quoted-insert</t>
<t tx="ekr.20050731102358.11">raise-frame
re-builder
re-search-backward
re-search-forward
read-abbrev-file
read-kbd-macro
read-library-name
recent-files-initialize
recent-files-visit-file
recenter
recentf-cancel-dialog
recentf-cleanup
recentf-dialog-mode
recentf-edit-list
recentf-mode
recentf-open-files
recentf-open-more-files
recentf-rebuild-virtual-pathes
recentf-save-list
recover-all-files
recover-file
recover-session
recover-session-finish
recursive-edit
reftex-citation
reftex-index-phrases-mode
reftex-mode
regexp-builder
register-to-point
reindent-then-newline-and-indent
release-and-activate-toolbar-button
release-toolbar-button
remote-compile
remove-directory
rename-buffer
rename-file
rename-uniquely
repeat-complex-command
repeat-matching-complex-command
replace-buffer-in-windows
replace-rectangle
replace-regexp
replace-string
report-emacs-bug
report-xemacs-bug
reposition-window
resize-minibuffer-mode
restore-initial-toolbar
resume-console
reverse-region
revert-buffer
rexx-mode
riece
rlogin
rmail
rmail-input
rmail-mode
rolo-add
rolo-display-matches
rolo-edit
rolo-fgrep
rolo-fgrep-logical
rolo-grep
rolo-kill
rolo-sort
rolo-toggle-datestamps
rolo-yank
rot13-other-window
rotate-yank-pointer
route
rpm
rpm-spec-mode
rsh
rtf-clip-buffer
rtf-clip-region
rtf-export
rtf-export-region
rtf-spool-buffer
rtf-spool-region
ruby-mode
rubydb
run-at-time
run-caml
run-ediff-from-cvs-buffer
run-prolog
run-ruby
run-scheme
run-scsh
run-sml
run-with-idle-timer
run-with-timer</t>
<t tx="ekr.20050731102358.12">s-region-bind
s-region-bind-cua
save-buffer
save-buffers-kill-emacs
save-some-buffers
savehist-load
savehist-save
scheme-mode
scribe-mode
scroll-down
scroll-down-command
scroll-down-one
scroll-left
scroll-other-window
scroll-other-window-down
scroll-right
scroll-up
scroll-up-command
scroll-up-one
sdb
search-backward
search-backward-regexp
search-forward
search-forward-regexp
self-insert-and-exit
self-insert-command
semantic-analyze-current-context
semantic-auto-parse-mode
semantic-bnf-mode
semantic-cb-speedbar-mode
semantic-chart-database-size
semantic-chart-nonterminal-complexity-token
semantic-chart-nonterminals-by-token
semantic-show-dirty-mode
semantic-show-unmatched-syntax-mode
semantic-summary-mode
senator-complete-symbol
senator-completion-menu-popup
senator-jump
senator-jump-regexp
senator-minor-mode
senator-next-token
senator-previous-token
senator-re-search-backward
senator-re-search-forward
senator-search-backward
senator-search-forward
senator-word-search-backward
senator-word-search-forward
send-pr
send-pr-mode
send-pr:send-pr
send-pr:send-pr-mode
set-buffer-file-coding-system
set-buffer-file-coding-system-for-read
set-buffer-process-coding-system
set-comment-column
set-default-buffer-file-coding-system
set-default-file-coding-system
set-face-background
set-face-background-pixmap
set-face-blinking-p
set-face-dim-p
set-face-display-table
set-face-doc-string
set-face-font
set-face-foreground
set-face-highlight-p
set-face-reverse-p
set-face-strikethru-p
set-face-underline-p
set-file-coding-system
set-file-coding-system-for-read
set-fill-column
set-fill-prefix
set-goal-column
set-justification
set-justification-center
set-justification-full
set-justification-left
set-justification-none
set-justification-right
set-keyboard-coding-system
set-left-margin
set-mark-command
set-pathname-coding-system
set-right-margin
set-selective-display
set-terminal-coding-system
set-variable
set-visited-file-name
setenv
setnu-mode
sgml-mode
sh-mode
shell
shell-command
shell-command-on-region
shell-script-mode
show-message-log
shrink-window
shrink-window-horizontally
shrink-window-if-larger-than-buffer
shrink-window-pixels
sieve-manage
sieve-mode
sieve-upload
sieve-upload-and-bury
signal-process
simula-mode
skeleton-pair-insert-maybe
skeleton-proxy
skeleton-proxy-new
smart-c++
smart-info
smart-info-assist
smart-java
smart-objc
smerge
sml-mode
smt-browse
snake
sokoban
sort-columns
sort-fields
sort-float-fields
sort-lines
sort-numeric-fields
sort-pages
sort-paragraphs
sort-regexp-fields
sort-regexp-fields-numerically
speedbar
speedbar-frame-mode
speedbar-get-focus
spell-buffer
spell-region
spell-string
spell-word
split-line
split-window
split-window-horizontally
split-window-vertically
spook
sql-db2
sql-help
sql-informix
sql-ingres
sql-interbase
sql-linter
sql-mode
sql-ms
sql-mysql
sql-oracle
sql-postgres
sql-product-interactive
sql-solid
sql-sqlite
sql-sybase
ssh
standard-display-european
start-itimer
start-kbd-macro
startup-presentation-hack
string-rectangle
strokes-compose-complex-stroke
strokes-decode-buffer
strokes-describe-stroke
strokes-do-complex-stroke
strokes-do-stroke
strokes-global-set-stroke
strokes-help
strokes-list-strokes
strokes-load-user-strokes
strokes-mode
style-format
summ-pr
sunrise-sunset
suspend-console
suspend-emacs
suspend-emacs-or-iconify-frame
suspend-or-iconify-emacs
switch-to-buffer
switch-to-buffer-other-frame
switch-to-buffer-other-window
switch-to-completions
switch-to-other-buffer
symbol-file
symbol-near-point</t>
<t tx="ekr.20050731102358.13">tab-to-tab-stop
tabify
tag-complete-symbol
tags-apropos
tags-loop-continue
tags-query-replace
tags-search
tcl-help-on-word
tcl-mode
tdbx
teco-command
telnet
term
terminal-emulator
tetris
tex-mode
texi2info
texinfo-format-buffer
texinfo-format-region
texinfo-mode
texmathp
text-mode
tgdb
time-stamp
time-stamp-toggle-active
tmpl-expand-templates-in-buffer
tmpl-expand-templates-in-region
tmpl-insert-template-file
tmpl-insert-template-file-from-fixed-dirs
tmpl-minor-mode
toggle-auto-compression
toggle-buffer-file-coding-system
toggle-debug-on-error
toggle-debug-on-quit
toggle-debug-on-signal
toggle-profiling
toggle-read-only
toggle-rot13-mode
toggle-text-mode-auto-fill
toggle-truncate-lines
toggle-viper-mode
toggle-where-was-i
toolbar-add-button-on-the-fly
toolbar-add-execute-macro-button
toolbar-add-kbd-macro
toolbar-compile
toolbar-copy
toolbar-cut
toolbar-debug
toolbar-dired
toolbar-external
toolbar-gnus
toolbar-info
toolbar-ispell
toolbar-ispell-internal
toolbar-mail
toolbar-news
toolbar-not-configured
toolbar-open
toolbar-paste
toolbar-print
toolbar-redo
toolbar-replace
toolbar-save
toolbar-search
toolbar-undo
top-level
tperldb
tpu-edt
tpu-edt-mode
tpu-edt-on
tpu-set-cursor-bound
tpu-set-cursor-free
tpu-set-scroll-margins
tpum-global-mode
tpum-minor-mode
trace-function
trace-function-background
traceroute
transpose-chars
transpose-line-down
transpose-line-up
transpose-lines
transpose-paragraphs
transpose-preceding-chars
transpose-sentences
transpose-sexps
transpose-words
tree-test-it-all
tsdb
tshell
turn-off-font-lock
turn-off-haskell-doc-mode
turn-off-pending-delete
turn-on-auto-fill
turn-on-eldoc-mode
turn-on-font-lock
turn-on-fume-mode
turn-on-haskell-doc-mode
turn-on-pending-delete
turn-on-permanent-buffers
txdb</t>
<t tx="ekr.20050731102358.14">uil-mode
undefined
underline-region
undo
unexpand-abbrev
unhide-copyleft-region
universal-argument
universal-argument-minus
universal-argument-more
universal-argument-other-key
universal-coding-system-argument
unix-sync
unload-feature
unlock-buffer
unmigrate-user-init-file
unmorse-region
unoverstrike-region
unpop-window-configuration
unrmail
untabify
ununderline-and-unoverstrike-region
ununderline-region
up-list
upcase-initials-region
upcase-region
upcase-region-or-word
upcase-word
update-autoloads-from-directory
update-autoloads-here
update-file-autoloads
url-gateway-nslookup-host
url-mail
url-setup-save-timer
use-hard-newlines
user-mail-address</t>
<t tx="ekr.20050731102358.15">vc-annotate
vc-cancel-version
vc-create-snapshot
vc-diff
vc-directory
vc-insert-headers
vc-load-vc-hooks
vc-merge
vc-next-action
vc-print-log
vc-register
vc-rename-file
vc-resolve-conflicts
vc-retrieve-snapshot
vc-revert-buffer
vc-update-change-log
vc-version-diff
vc-version-other-window
verilog-customize
verilog-mode
verilog-version
version
vertical-mode
vhdl-mode
view-buffer
view-buffer-other-window
view-emacs-news
view-file
view-file-other-window
view-lossage
view-major-mode
view-minor-mode
view-mode
view-pr
view-register
view-sample-init-el
viper-mode
visit-tags-table
vm
vm-compose-mail
vm-folders-summarize
vm-mail
vm-mail-other-frame
vm-mail-other-window
vm-mode
vm-other-frame
vm-other-window
vm-submit-bug-report
vm-visit-folder
vm-visit-folder-other-frame
vm-visit-folder-other-window
vm-visit-imap-folder
vm-visit-imap-folder-other-frame
vm-visit-imap-folder-other-window
vm-visit-pop-folder
vm-visit-pop-folder-other-frame
vm-visit-pop-folder-other-window
vm-visit-virtual-folder
vm-visit-virtual-folder-other-frame
vm-visit-virtual-folder-other-window
vrml-mode</t>
<t tx="ekr.20050731102358.16">w3
w3-display-stylesheet
w3-fetch
w3-fetch-other-frame
w3-find-file
w3-follow-link
w3-follow-url-at-point
w3-follow-url-at-point-other-frame
w3-hotindex-add-key
w3-hotindex-query
w3-hotindex-rm-key
w3-hotlist-add-document
w3-hotlist-add-document-at-point
w3-hotlist-append
w3-hotlist-apropos
w3-hotlist-delete
w3-hotlist-refresh
w3-hotlist-rename-entry
w3-maybe-follow-link
w3-maybe-follow-link-mouse
w3-next-document
w3-open-local
w3-prev-document
w3-preview-this-buffer
w3-print-this-url
w3-print-url-under-point
w3-read-html-bookmarks
w3-region
w3-show-dvi
w3-table-speak-current-table-column
w3-use-hotlist
w3-version
wconfig-add-by-name
wconfig-delete-by-name
wconfig-delete-pop
wconfig-restore-by-name
wconfig-ring-save
wconfig-yank-pop
webjump
what-coding-system
what-cursor-position
what-domain
what-line
what-page
where-is
whitespace-buffer
whitespace-cleanup
whitespace-cleanup-region
whitespace-global-mode
whitespace-region
whitespace-toggle-ateol-check
whitespace-toggle-indent-check
whitespace-toggle-leading-check
whitespace-toggle-spacetab-check
whitespace-toggle-trailing-check
whitespace-visual-incremental-mode
whitespace-visual-mode
whitespace-write-file-hook
whois
whois-reverse-lookup
widen
widget-backward
widget-beginning-of-line
widget-browse
widget-browse-at
widget-browse-other-window
widget-button-click
widget-button-press
widget-button1-click
widget-complete
widget-end-of-line
widget-field-activate
widget-file-complete
widget-forward
widget-kill-line
widget-minor-mode
widget-transpose-chars
win32-get-current-locale-id
win32-get-default-locale-id
win32-get-locale-info
win32-get-valid-locale-ids
win32-long-file-name
win32-set-current-locale
win32-set-process-priority
win32-short-file-name
window-configuration-to-register
winmgr-mode
winring-delete-configuration
winring-duplicate-configuration
winring-jump-to-configuration
winring-new-configuration
winring-next-configuration
winring-prev-configuration
winring-rename-configuration
word-search-backward
word-search-forward
wordstar-mode
write-abbrev-file
write-file
write-region
write-region-internal
wrolo-popup-menu</t>
<t tx="ekr.20050731102358.17">x-symbol-decode
x-symbol-decode-recode
x-symbol-encode
x-symbol-encode-recode
x-symbol-fontify
x-symbol-grid
x-symbol-image-editor
x-symbol-image-parse-buffer
x-symbol-init-language-interactive
x-symbol-initialize
x-symbol-key-autoload
x-symbol-map-autoload
x-symbol-mode
x-symbol-modify-key
x-symbol-package-bug
x-symbol-package-info
x-symbol-package-reply-to-report
x-symbol-package-web
x-symbol-rotate-key
x-symbol-unalias
xdb
xemacs-local-faq
xemacs-splash-buffer
xemacs-www-faq
xemacs-www-page
xetla
xetla-add-log-entry
xetla-apply-changeset
xetla-archives
xetla-bookmarks
xetla-browse
xetla-changelog
xetla-changes
xetla-changes-against
xetla-changes-last-revision
xetla-commit
xetla-conflicts-finish
xetla-delta
xetla-ediff-add-log-entry
xetla-edit-log
xetla-file-diff
xetla-file-ediff
xetla-file-ediff-revisions
xetla-file-view-original
xetla-get-changeset
xetla-help
xetla-id-tagging-method
xetla-inventory
xetla-inventory-file-mode
xetla-log-edit-mode
xetla-logs
xetla-make-archive
xetla-missing
xetla-my-id
xetla-my-revision-library
xetla-prepare-patch-submission
xetla-revisions
xetla-rm
xetla-start-project
xetla-submit-bug-report
xetla-tag-insert
xetla-tag-regenerate
xetla-tree-lint
xetla-tree-version
xetla-version
xetla-view-conflicts
xmine
xmine-mode
xml-mode
xpm-mode
xrdb-mode
xsl-grep
xsl-mode
xslt-process-mode
xt-check-xlib
xwem-attach-client
xwem-backward-application
xwem-balance-windows
xwem-battery
xwem-battery-popup-menu
xwem-battery-status
xwem-cl-pop-to-client
xwem-cl-set-title
xwem-cl-switch-other-frame
xwem-cl-switch-other-win
xwem-cl-switch-to-other
xwem-cl-switch-to-other-in-other-win
xwem-cl-transpose
xwem-clgen-toggle-other-on-split
xwem-clgen-turn-off-other-on-split
xwem-clgen-turn-on-other-on-split
xwem-client-demanage-others
xwem-client-exchange-selected-and-mark
xwem-client-iconify
xwem-client-idestroy
xwem-client-imove
xwem-client-info
xwem-client-iresize
xwem-client-kill
xwem-client-query-kill
xwem-client-run-copy
xwem-client-run-copy-other-frame
xwem-client-run-copy-other-win
xwem-client-set-mark
xwem-client-unset-mark
xwem-clswi-next
xwem-clswi-next-other-window
xwem-clswi-prev
xwem-clswi-prev-other-window
xwem-copy-cutbuffer
xwem-copy-region-as-cutbuffer
xwem-describe-prefix-bindings
xwem-desktop-load
xwem-desktop-load-onetime
xwem-desktop-save
xwem-desktop-save-onetime
xwem-edit-client-properties
xwem-edmacro-edit-kbd-macro
xwem-eval-expression
xwem-execute-extended-command
xwem-fini
xwem-focus-click-on
xwem-forward-application
xwem-frame-destroy
xwem-frame-fit-screen
xwem-frame-goto-next
xwem-frame-goto-next-hor
xwem-frame-goto-next-vert
xwem-frame-goto-prev
xwem-frame-goto-prev-hor
xwem-frame-goto-prev-vert
xwem-frame-hide
xwem-frame-imove
xwem-frame-iresize
xwem-frame-lower
xwem-frame-next
xwem-frame-on-delim-menu
xwem-frame-on-delim-resize
xwem-frame-previous
xwem-frame-raise
xwem-frame-sbs-hor-split
xwem-frame-sbs-vert-split
xwem-frame-set-name
xwem-frame-showroot
xwem-frame-split-sbs
xwem-frame-switch
xwem-frame-switch-nth
xwem-frame-switch-nth-linkage
xwem-frame-transparency
xwem-frame-transpose
xwem-framei-dockapp-popup-alt-menu
xwem-framei-dockapp-popup-menu
xwem-fullscreen-mode
xwem-help
xwem-help-clients
xwem-help-cutbuffers
xwem-help-describe-bindings
xwem-help-describe-key
xwem-help-describe-key1
xwem-help-for-help
xwem-help-frames
xwem-help-mode
xwem-help-where-is
xwem-help-wins
xwem-ignore-command
xwem-kbd-quit
xwem-kbd-quote-command
xwem-keyboard-quit
xwem-keymacro-begin
xwem-keymacro-end
xwem-keymacro-exit-recursive-edit
xwem-keymacro-recursive-edit
xwem-keymacro-undefined
xwem-keytt-minor-mode
xwem-kill-cl-and-window
xwem-launch-dock-down
xwem-launch-dock-launch
xwem-launch-dock-menu
xwem-launch-lupe
xwem-launch-lupe-other-frame
xwem-launch-lupe-other-win
xwem-launch-program
xwem-launch-program-other-frame
xwem-launch-program-other-win
xwem-launch-xlock
xwem-launch-xterm
xwem-launch-xterm-other-frame
xwem-launch-xterm-other-win
xwem-launcher-toggle-frame-type
xwem-launcher-toggle-split-type
xwem-launcher-turn-on-embedded-frame-type
xwem-launcher-turn-on-horizontal-split-type
xwem-launcher-turn-on-normal-frame-type
xwem-launcher-turn-on-vertical-split-type
xwem-make-frame
xwem-mini-calc
xwem-minib-resize-mode
xwem-minibuffer-activate
xwem-misc-make-screenshot
xwem-misc-pause
xwem-misc-profiling-results
xwem-misc-start-profiling
xwem-modeline-disable
xwem-modeline-enable
xwem-open-file
xwem-other-window
xwem-pager
xwem-pager-move-down
xwem-pager-move-left
xwem-pager-move-right
xwem-pager-move-up
xwem-paste-cutbuffer
xwem-popup-auto-menu
xwem-popup-clients-menu
xwem-recover-do-recover
xwem-recover-toggle
xwem-recover-turn-off
xwem-recover-turn-on
xwem-register-client
xwem-register-frame-config
xwem-register-jump
xwem-register-win-config
xwem-report-bug
xwem-rooter-lower
xwem-rooter-raise
xwem-run-program
xwem-self-insert-or-undefined
xwem-shell-command
xwem-show-message-log
xwem-sm-global-mode
xwem-sm-mode
xwem-strokes-begin
xwem-strokes-cmplx-begin
xwem-strokes-define
xwem-strokes-ibutton1
xwem-strokes-ibutton1up
xwem-strokes-ibutton3
xwem-strokes-idescribe
xwem-strokes-list
xwem-strokes-nocmd
xwem-strokes-unset-last-stroke
xwem-switch-client
xwem-switch-other-client
xwem-switch-to-fullscreen-cl
xwem-tabber-popup-cl-menu
xwem-tabber-switch-cl
xwem-theme-set
xwem-time
xwem-toggle-fullscreen
xwem-transpose-frames
xwem-turn-off-keytt
xwem-turn-off-vline
xwem-turn-on-keytt
xwem-turn-on-vline
xwem-undefined-command
xwem-universal-argument
xwem-universal-command
xwem-universal-digit
xwem-universal-minus
xwem-universal-more
xwem-vline-minor-mode
xwem-weather-popup-menu
xwem-weather-popup-remove
xwem-weather-show-details
xwem-weather-update
xwem-window-delete
xwem-window-delete-others
xwem-window-enlarge-horizontally
xwem-window-enlarge-vertically
xwem-window-split-horizontally
xwem-window-split-vertically
xwem-winmove-down
xwem-winmove-left
xwem-winmove-right
xwem-winmove-up
xwem-worklog-login
xwem-worklog-logout</t>
<t tx="ekr.20050731102358.18">yank
yank-clipboard-selection
yank-pop
yank-rectangle
yow
</t>
<t tx="ekr.20050731102358.19">zap-to-char
zap-up-to-char
zenirc</t>
<t tx="ekr.20050731102651.1">Custom-buffer-done
Custom-goto-parent
Custom-make-dependencies
Custom-mode-menu
Custom-reset-current
Custom-reset-saved
Custom-reset-standard
Custom-save
Custom-set

Electric-command-history-redo-expression

Footnote-add-footnote

Helper-describe-bindings
Helper-help

</t>
<t tx="ekr.20050731102651.3">Info-elisp-ref
Info-emacs-command
Info-emacs-key
Info-goto-emacs-command-node
Info-goto-emacs-key-command-node
Info-goto-node
Info-query
Info-search
Info-speedbar-browser
Info-split
Info-tagify
Info-validate
Info-visit-file</t>
<t tx="ekr.20050731102651.4">LaTeX-install-toolbar
LaTeX-mode

Manual-nuke-nroff-bs

Rd-mode

TeX-auto-generate
TeX-auto-generate-global
TeX-insert-quote
TeX-mode
TeX-submit-bug-report

View-process-status</t>
<t tx="ekr.20050731115541">@nocolor

1.  Get present emacs functionality integrated into Leo asap.
    - Working prototype by Aug 7.
    - Next release by Sept. 1.
    - Add a single emacs menu containing submenus for each of the following main emacs menu:
        View, Cmds, Tools, Options, Buffers (but not Lisp yet)
    - Possibly add items in existing File &amp; Edit menus.
    - Dim unimplemented items.
    - Get important Emacs items from settings dialog.
        (Try not to change this too much in the future.)

Subgoals:
    
- Allow future improvements without changing user options greatly.
    - Allow for customizeEmacs plugin.
- Implement all essential emacs commands:  cursor commands, find commands, etc.
- Extend emacs commands to handler Leo improvements.
- Integrate Leo commands with emacs commands.

Other goals:
    
- Define all present xemacs names in Leo for the future.
- emacs class should not know any details of 'interior modes'.
- pushMode, popMode, setMode, clearMode commands.
- Each important Leo widget should capture all &lt;key&gt; events.
    - Send them to master key handler commander, widgetKind args.
      (This makes it unnecessary to call possibly unreliable (or non-existent) gui methods.
- (Optional?)  Don't bind menu items: let the key handler dispatch the menu commands.</t>
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
<t tx="orkman.20050207150858">from __future__ import generators
import javax.swing as swing
import javax.swing.event as sevent
import javax.swing.text as stext
import java.awt.event as aevent
import java.util.regex as regex
import java.awt as awt
import java.lang 
import java.io
import string    
import re  
import leoGlobals as g
from DefCallable import DefCallable
import LeoUtilities

True =1
False = 0
extensions = None

&lt;&lt; addCommand &gt;&gt;

class SwingMacs:
    '''A class that adds Emac derived commands and keystrokes to a JTextPane'''    

    @others</t>
<t tx="orkman.20050207152619">class incremental:
    
    def __init__( self, emacs ):
        self.emacs = emacs
        self.iway = None
        i = java.lang.Integer.decode( '#63c6de' )
        self.highlight = awt.Color( i )
    
    def __call__( self, event, command ):
        
        component = event.getSource()
        stxt = component.getText()
        pos = component.getCaretPosition()
        if command in ( 'Ctrl S', 'Ctrl R' ):
            self.startIncremental( command )
            if not self.emacs.minibuffer.getText():
                return True
        elif command == 'Enter':
            return self.emacs.keyboardQuit( event )
        else:
            self.setMiniBuffer( event )
        

        if event.getKeyChar() == aevent.KeyEvent.CHAR_UNDEFINED :
            return True
        
        source = event.getSource()
        wcursor = java.awt.Cursor.getPredefinedCursor( java.awt.Cursor.WAIT_CURSOR )
        source.setCursor( wcursor )
        dc = DefCallable( lambda : self.incrementalSearch( event , command, stxt, pos) )
        swing.SwingUtilities.invokeLater( dc.wrappedAsFutureTask() )  
        #return self.incrementalSearch( event , command, stxt, pos)
        return True
        
    def setMiniBuffer( self, event ):
        self.emacs.eventToMinibuffer( event )
        
    @others</t>
<t tx="orkman.20050207162016">class stateManager:

    def __init__ (self,emacs):
        self.state = None
        self.emacs = emacs

    def hasState (self):
        return self.state

    def setState (self,state):
        self.state = state

    def filterTo (self,event,command):
        return self.emacs.strategyObjects [self.state](event,command)

    def clear (self):
        self.state = None</t>
<t tx="orkman.20050207164014">def keyboardQuit( self, event=None ):
    
    self._stateManager.clear()
    self._stateManager2.clear()
    self.minibuffer.setText( '' )
    self.clearHighlights()
    sa = stext.SimpleAttributeSet()
    sa.addAttribute( 'dy-ab', 'dy-ab' )
    sa.addAttribute( 'kb', 'kb' )
    self.clearAttributes( sa )
    self.setCommandText( "" )
    for z in self.modeStrategies:
        z.mode = None
    
    cp = self.editor.getCaretPosition()
    self.editor.setCaretPosition( cp )
    return True</t>
<t tx="orkman.20050207164550">def eventToMinibuffer( self, event ):
    
    code = event.getKeyCode()
    code = event.getKeyText( code )
    txt = self.minibuffer.getText()
    if code == 'Backspace':
        txt = txt[ : -1 ]
    else:
        char = event.getKeyChar()
        #if java.lang.Character.isLetterOrDigit( char ) or java.lang.Character.isWhitespace( char ):
        if java.lang.Character.isDefined( char ):
            txt = '%s%s' %( txt, char )
    self.minibuffer.setText( txt )
    return txt</t>
<t tx="orkman.20050209165307">class dynamicabbrevs:

    def __init__( self, emacs ):
        self.emacs = emacs
        self.dynaregex = re.compile( r'[%s%s\-_]+' %( string.ascii_letters, string.digits ) ) #for dynamic abbreviations
        self.searchtext = None
        self.returnlist = []
        self.ind = 0 #last spot wordindex returned
        self.dynamiclist = java.util.TreeSet()
        self.createDynamicList()
        
    def __call__( self, event, command ):
    
        if command == 'Alt Slash':
            self.dynamicExpansion( event )
        if command == 'Ctrl+Alt Slash':
            self.dynamicExpansion2( event )

    @others</t>
<t tx="orkman.20050209165621">def dynamicExpansion( self, event ):#, store = {'rlist': [], 'stext': ''} ):
    
    tag = 'dy-ab'
    word = self.emacs.getWordStart()
    ind = self.emacs.getWordStartIndex()
    
    if not word:
        self.clearDynamic( tag )
        return   
    elif word and self.searchtext == None:
        self.searchtext = word
        self.ind = ind
    elif not word.startswith( self.searchtext ) or self.ind != ind:

        self.clearDynamic( tag )
        self.searchtext = word
        self.ind = ind

    
    if self.emacs.getAttributeRanges( tag ): #indicates that expansion has started
        self.emacs.removeTextWithAttribute( tag )
        if self.returnlist:
            txt = self.returnlist.pop()
            self.emacs.insertTextWithAttribute( txt, tag )
        else:
            self.getDynamicList( self.searchtext, self.returnlist )#rebuild
            self.emacs.insertTextWithAttribute( self.searchtext , tag )
        return   
    elif self.searchtext:
        self.getDynamicList( self.searchtext, self.returnlist )
        if self.returnlist:
            start = self.emacs.getWordStartIndex()
            ntxt = self.returnlist.pop()
            self.emacs.replaceText( start, start + len( word ), ntxt )
            self.emacs.addAttributeToRange( tag, tag, start, len( ntxt ) )
            

    #tbuffer = event.widget
    #rlist = self.store[ 'rlist' ]
    #stext = self.store[ 'stext' ]
    #i = tbuffer.index( 'insert -1c wordstart' )
    #i2 = tbuffer.index( 'insert -1c wordend' )
    #txt = tbuffer.get( i, i2 )
    #dA = tbuffer.tag_ranges( 'dA' )
    #tbuffer.tag_delete( 'dA' )
    #def doDa( txt, from_ = 'insert -1c wordstart', to_ = 'insert -1c wordend' ):
    #
    #    tbuffer.delete( from_, to_ ) 
    #    tbuffer.insert( 'insert', txt, 'dA' )
    #    return self._tailEnd( tbuffer )
        
    #if dA:
    #    dA1, dA2 = dA
    #    dtext = tbuffer.get( dA1, dA2 )
    #    if dtext.startswith( stext ) and i2 == dA2: #This seems reasonable, since we cant get a whole word that has the '-' char in it, we do a good guess
    #        if rlist:
    #            txt = rlist.pop()
    #        else:
    #            txt = stext
    #            tbuffer.delete( dA1, dA2 )
    #            dA2 = dA1 #since the text is going to be reread, we dont want to include the last dynamic abbreviation
    #            self.getDynamicList( tbuffer, txt, rlist )
    #        return doDa( txt, dA1, dA2 )
    #    else:
    #        dA = None
            
    #if not dA:
    #    self.store[ 'stext' ] = txt
    #    self.store[ 'rlist' ] = rlist = []
    #    self.getDynamicList( tbuffer, txt, rlist )
    #    if not rlist:
    #        return 'break'
    #    txt = rlist.pop()
    #    return doDa( txt )</t>
<t tx="orkman.20050209165627">def dynamicExpansion2( self, event ):

    #i = tbuffer.index( 'insert -1c wordstart' )
    #i2 = tbuffer.index( 'insert -1c wordend' )
    i = self.emacs.getWordStartIndex()
    i2 = self.emacs.getWordEndIndex()
    #txt = tbuffer.get( i, i2 )   
    txt = self.emacs.getTextSlice( i, i2 )
    rlist = []
    self.getDynamicList( txt, rlist )
    dEstring = reduce( self.emacs.findPre, rlist )
    if dEstring:
        self.emacs.replaceText( i, i2, dEstring )
        #tbuffer.delete( i , i2 )
        #tbuffer.insert( i, dEstring )    
        #return self._tailEnd( tbuffer )</t>
<t tx="orkman.20050209165908">def getText( self ):
    
    doc = self.editor.getDocument()
    txt = doc.getText( 0, doc.getLength() )
    return txt
    
def getTextSlice( self, frm, to ):
    
    txt = self.getText()
    return txt[ frm: to ]
    
def replaceText( self, frm, to, txt ):
    
    doc = self.editor.getStyledDocument()
    doc.replace( frm, to - frm, txt, None )</t>
<t tx="orkman.20050209165908.1">def getDynamicList( self, txt , rlist ):

     ttext = self.emacs.getText()
     items = self.dynaregex.findall( ttext )
     for z in items:
        self.dynamiclist.add( z )    
            
               
                
     started = 0
     for z in self.dynamiclist:
        if z.startswith( txt ):
             if not started:
                 started = 1
             rlist.append( z)
             continue
        if started:
            break
     
     return rlist

@
     ttext = self.emacs.getText()
     items = self.dynaregex.findall( ttext ) #make a big list of what we are considering a 'word'
     if items:
         for word in items:
             if not word.startswith( txt ) or word == txt: continue #dont need words that dont match or == the pattern
             if word not in rlist:
                 rlist.append( word )
             else:
                 rlist.remove( word )
                 rlist.append( word )</t>
<t tx="orkman.20050209170444">def getWordStart( self ):
    
    pos = self.editor.getCaretPosition()
    #start = stext.Utilities.getWordStart( self.editor, pos ) --this method acts screwy
    doc = self.editor.getStyledDocument()
    txt = doc.getText( 0, pos )
    txtlines = txt.splitlines()
    try:
        line = txtlines[ -1 ]
        chunks = line.split()
        c2 = []
        for z in chunks[ : ]:
            [ c2.append( x ) for x in z.split( '.' ) ]
        chunks = c2
        word = chunks[ -1 ]
        for z in xrange( len( word ) ):
            w = word[ z ]
            if w.isalnum() or w=='_': break
        
        word = word[ z: ]
    except:
        return None
    return word
    
def getWordStartIndex( self, i = None ):
    
    pos = self.editor.getCaretPosition()
    doc = self.editor.getStyledDocument()
    txt = doc.getText( 0, pos )
    tlist = list( txt )
    tlist.reverse()
    for z in xrange( len( tlist ) ):
        if tlist[ z ] not in ( '_', '-' ) and ( tlist[ z ].isspace() or not tlist[ z ].isalnum() ):
            break
    return pos - z
    #start = stext.Utilities.getWordStart( self.editor, pos ) ---this method acts screwy, thats why Im not using it.
    
    
def getWordEndIndex( self, i = None ):
    pos = self.editor.getCaretPosition()
    doc = self.editor.getStyledDocument()
    txt = doc.getText( 0, doc.getLength())
    txt = txt[ pos: ]
    tlist = list( txt )
    z = 0
    for z in xrange( len( tlist ) ):
        if tlist[ z ] != '_' and ( tlist[ z ].isspace() or not tlist[ z ].isalnum() ):
            break
    
    if z == 0:
        z = 1
    return pos + z</t>
<t tx="orkman.20050209180255">def getAttributeRanges( self, name ):
    
    dsd = self.editor.getStyledDocument()
    alen = dsd.getLength()
    range = []
    for z in xrange( alen ):
        element = dsd.getCharacterElement( z )
        as = element.getAttributes()
        if as.containsAttribute( name, name ):
            range.append( z )
            
    return range
    
def addAttributeToRange( self, name, value, offset, length, color = None ):

    dsd = self.editor.getStyledDocument()
    sa = stext.SimpleAttributeSet()
    sa.addAttribute( name, value )
    dsd.setCharacterAttributes( offset, length, sa, True )
    if color != None:
        self.addHighlight( offset, length+offset, color )

def clearAttributes( self, attrset ):
    dsd = self.editor.getStyledDocument()
    alen = dsd.getLength()
    for z in xrange( alen ):
        element = dsd.getCharacterElement( z )
        as = element.getAttributes()
        if as.containsAttributes( attrset ):
            mas = stext.SimpleAttributeSet() #We have to make a clean one and copy the data into it!  The one returned is immutable
            mas.addAttributes( as )
            mas.removeAttributes( attrset ) #we remove the tag from here.
            amount = as.getEndOffset() - as.getStartOffset() #very important to do it like this, giving each character an attribute caused colorization problems/doing the whole thing at once seems to have cleared those problems up.
            dsd.setCharacterAttributes( z, amount, mas, True )            
    
def clearAttribute( self, name ):
    dsd = self.editor.getStyledDocument()
    alen = dsd.getLength()
    for z in xrange( alen ):
        element = dsd.getCharacterElement( z )
        as = element.getAttributes()
        if as.containsAttribute( name, name ):
            mas = stext.SimpleAttributeSet() #We have to make a clean one and copy the data into it!  The one returned is immutable
            mas.addAttributes( as )
            mas.removeAttribute( name ) #we remove the tag from here.
            amount = as.getEndOffset() - as.getStartOffset() #very important to do it like this, giving each character an attribute caused colorization problems
            dsd.setCharacterAttributes( z, amount, mas, True )
    
def clearHighlights( self ):
    
    self.editor.getHighlighter().removeAllHighlights()    
    

def addHighlight( self, start, end, color ):
    
    highlighter = self.editor.getHighlighter()
    painter = stext.DefaultHighlighter.DefaultHighlightPainter( color )
    highlighter.addHighlight( start, end, painter )
    
def getHighlights( self ):
    
    highlighter = self.editor.getHighlighter()
    return highlighter.getHighlights()
    
    
def removeTextWithAttribute( self, name ):
    
    arange = self.getAttributeRanges( name )
    dsd = self.editor.getStyledDocument()
    alen = len( arange )
    if alen:
        dsd.remove( arange[ 0 ], alen )
    
def insertTextWithAttribute( self, txt, name ):
    
    sa = stext.SimpleAttributeSet()
    sa.addAttribute( name, name )
    pos = self.editor.getCaretPosition()
    dsd = self.editor.getStyledDocument()
    dsd.insertString( pos, txt, sa )</t>
<t tx="orkman.20050209215951">def clearDynamic( self, tag  ):

    self.emacs.clearAttribute( tag )
    self.returnlist = []
    self.searchtext = None
    self.ind = None</t>
<t tx="orkman.20050210105230">def findPre( self, a, b ):
    st = ''
    for z in a:
        st1 = st + z
        if b.startswith( st1 ):
            st = st1
        else:
            return st
    return st</t>
<t tx="orkman.20050210110555">@
This node organizes the classes that implement a rough cut of the Strategy pattern for the keystrokes.
Each recognized keystroke goes to the masterCommand, but the masterCommand just decides on the code that
should be executed, in this case it delegates the call to a Strategy object that decides upon what methods
to process the key stroke.  This has these benefits:
1. State is broken further from the container Object( Emacs ).
2. Changes to the processing methods no longer has global consequences.  It is conceivable that a different Strategy could
be swapped in by configuration or some other means.  All a strategy has to do is implement the __call__ operator to have
the event and keystroke passed into it.

This design is based off of the lessons learned in the temacs plugin for CPython Leo.  Its evolution followed this pattern:
1. It started as a flat function based module.  Though a useful learning experiment this grew too large and became
    hard to think about.  Changes were becoming difficult.
2. At this point it became apparent that more structure was needed.  It was refactored( in Refactoring this is a 'Big Refactoring')
into a class, with some helper classes.  This eased the ability to reason about and modify the code.
3. After working with this big class, it became apparent again that a further restructuring was needed.  The idea of breaking
the methods that were grouped under one rubric into further classes arose; the Strategy pattern seemed to be what was called for.
And here we are in SwingMacs making the first cut at this new decomposed design for the Jython port.


@c




@others</t>
<t tx="orkman.20050210110734">def startIncremental( self, command ):
    if command == 'Ctrl S':
        self.iway = 'forward'
    else:
        self.iway = 'backward'
    self.emacs._stateManager.setState( 'incremental' )  
    self.emacs.setCommandText( "I-Search:" )</t>
<t tx="orkman.20050210110734.1">def incrementalSearch( self, event, command, stxt, pos ):
        
        #self.emacs.clearAttribute( 'incremental' ) 
        self.emacs.clearHighlights()
        txt = self.emacs.minibuffer.getText()
        c = self.emacs.c
        source = event.getSource()
        #cursor = source.getCursor()
        #wcursor = java.awt.Cursor.getPredefinedCursor( java.awt.Cursor.WAIT_CURSOR )
        #source.setCursor( wcursor )
        # opos = source.getCaretPosition() 

        if self.iway == 'forward':
            if command != 'Ctrl S' and pos &gt;= len( txt ):
                    pos = pos - len( txt )
            i = self.forwardSearch( pos, txt, stxt )
            if i != -1:
                pos = pos + i + len( txt )
            else: #start from beginning again
                #i = self.forwardSearch( 0, txt, stxt )
                #if i != -1:
                #    pos = i + len( txt )
                cp = c.currentPosition()
                for z in c.currentPosition().fromSelfAllNodes_iter( copy = 1 ):
                    if z == cp: continue
                    i = self.forwardSearch( 0, txt, z.bodyString() )
                    if i != -1:
                        pos = i + len( txt )
                        c.beginUpdate()
                        c.setCurrentPosition( z )
                        c.endUpdate()
                        break
        else:
            if command != 'Ctrl R' and ( pos + len( txt ) ) &lt;= len( stxt ):
                    pos = pos + len( txt )
            i = self.backwardSearch( pos, txt, stxt )
            if i != -1:
                pos = i
            else: #start from the back again
                #i = self.backwardSearch( source.getDocument().getLength(), txt , stxt )
                #if i != -1:
                #    pos = i
                cp = c.currentPosition()
                for z in c.currentPosition().fromSelfBackAllNodes_iter( copy = 1 ):
                    if z == cp: continue
                    i = self.backwardSearch( len( z.bodyString() ), txt, z.bodyString() )
                    if i != -1:
                        pos = i
                        c.beginUpdate()
                        c.setCurrentPosition( z )
                        c.endUpdate()
                        break    
        
        #source.setCursor( self.old_cursor )
        if i == -1: 
            tcursor = java.awt.Cursor.getPredefinedCursor( java.awt.Cursor.TEXT_CURSOR )
            source.setCursor( tcursor )
            swing.JOptionPane.showMessageDialog( None, "Can't find %s" % txt )
            return True
        dhl = self.deferedHighlight( source, pos, self.iway, self.highlight, len( txt ), self.emacs )   
        swing.SwingUtilities.invokeLater( dhl )  
        #source.setCaretPosition( pos )
        #if self.iway == 'forward':
        #    start = pos - len( txt )
        #    self.emacs.addHighlight( start, start + len( txt ), self.highlight ) 
        #else:
        #    self.emacs.addHighlight( pos, pos + len( txt ), self.highlight )
        return True</t>
<t tx="orkman.20050210125253">@
The answer is simple: SwingMacs is a component of the jython Leo port.  It is derived from the CPython
Leo plugins temacs and usetemacs.  Though it would be wonderful just to use those plugins, they
were targeted at the Tk and its Text widget( hence the 't' in temacs ).  The two technologies are different enough to warrent a new implementation.  Though as much reuse as possible is going to be attempted.

The implementation strategy is:
    
1. Copy and Paste a node from temacs into SwingMacs.
2. Analyze the node and begin the transition to Java/Jython/Swing.
    
Tags being absent from the JTextPane leads to the emulation of Tags through character Attributes.  The main
SwingMacs Emacs object shall contain these tag emulator methods.  The developer should not have to think in Attributes
when implementing a method that needs the simplicity of tags.  He will be able to use the SwingMacs virtual tag
methods -- tags whose only existence is in a concept.
@c</t>
<t tx="orkman.20050210201413">class formatter:
    
    def __init__( self, emacs ):
        
        self.emacs = emacs
        self.commands = {
        
        'Ctrl+Alt Back Slash': self.indentRegionToFirstLine,
        'indent-region': self.indentRegionToFirstLine,
        'indent-rigidly': self.indentRigidly,  
        'indent-relative': self.indentRelative,
        'Alt Back Slash': self.deleteSurroundingSpaces,
        'Alt+Shift 6': self.joinLineToPrevious,
        'Ctrl O': self.deleteBlankLines,
        
        }
        
        
    def __call__( self, event, command ):
        
        
        rval = self.commands[ command ]()        
        self.emacs.keyboardQuit( event )
        return rval
                
    @others</t>
<t tx="orkman.20050210201413.1">def indentRegionToFirstLine( self ):
    
    editor = self.emacs.editor
    start = editor.getSelectionStart()
    end = editor.getSelectionEnd()
    if start != end:
        
        sstart = stext.Utilities.getRowStart( editor, start )
        send = stext.Utilities.getRowEnd( editor, end )
        doc = editor.getStyledDocument()
        txt = doc.getText( sstart, send - sstart )
        lines = txt.splitlines()
        firstline = lines[ 0 ]
        ws_start = []
        for z in firstline:
            if z.isspace():
                ws_start.append( z )
            else:
                break
                
        ws_segment = ''.join( ws_start )
        nwlines = [ firstline, ]
        for x in lines[ 1: ]:
            x_nws = x.lstrip()
            x_new = '%s%s' % ( ws_segment, x_nws )
            nwlines.append( x_new )
            
        new_txt = '\n'.join( nwlines )
        pos = editor.getCaretPosition()
        doc.replace( sstart, send - sstart, new_txt, None )
        
    return True</t>
<t tx="orkman.20050210202559">class killbuffer:
    
    def __init__( self, emacs ):
        self.emacs = emacs
        self.killbuffer = []
        self.cliptext = None
        
        #for killbuffer
        self.last_clipboard = None
        self.kbiterator = self.iterateKillBuffer()
        self.reset = False
        self.lastKBSpot = None
        
        
    def __call__( self, event, command ):
        
        if command == 'Ctrl K':
            self.killToEndOfLine()
        if command == 'Alt Y':
            self.walkKB()
        if command == 'Ctrl Y':
            self.yank()
        if command == 'Ctrl W':
            self.killRegion()
        if command == 'Alt W':
            self.copyRegion()
           
        self.emacs.keyboardQuit( event )
        return True    
        
    @others</t>
<t tx="orkman.20050210202559.1">def killToEndOfLine( self ):
    
    editor = self.emacs.editor
    pos = editor.getCaretPosition()
    end = stext.Utilities.getRowEnd( editor, pos )
    self.kill( pos, end  )    
    return True</t>
<t tx="orkman.20050210203511">def yank( self ):
    self.reset = True
    return self.walkKB()</t>
<t tx="orkman.20050210204001">def getHelp( self ):
    
    helptext ='''
    
    keystrokes:
    
    keyboard quit:
        Ctrl-g: quits any current command. 
    
    selecting:
        Ctrl-Spacebar : starts selecting.  To stop Ctrl-g.
    
    kill and yanking:
        Ctrl-k : kills to end of line and inserts data into killbuffer
        Ctrl-w: kills region and inserts data into killbuffer
        Alt-w: copys region and inserts data into killbuffer   
        Ctrl-y: inserts first item in the killbuffer
        Alt-y: inserts next item in the killbuffer; allows the user to cycle 
           through the killbuffer, selecting the desired 'killed' text.
           
           
    deleting:    
        Ctrl-d: deletes next character.
        Delete: deletes previous character.
    
    
    dynamic abbreviations:
        Alt-/ : cycles through all words that match the starting word, which is used as a prefix.
        Ctrl-Alt-/ : takes current word, using it as a prefix and finds the common 
                    prefix among the matching prefix words. 'ea' with the words ( eat,
                    eats, eater ) will become 'eat' upon execution of this command.
                    
    symbol completion:
        Alt Ctrl I : takes the start of the current word and completes it if it matches a keyword
                     of the current language in effect.  The user can cycle through the matches if there
                     are multiple matches.  For example:
                         d( Alt Ctrl I )
                         del
                         del( Alt Ctrl I )
                         def
                 
                 
    incremental search:
        Ctrl-s : starts incremental search forward
        Ctrl-r : starts incremental search backward
    
    
    formating:
        Ctrl-Alt-\ : takes the current selection and formats each line so that it has the same indentation
                 as the first line in the selection.
        Alt-\: deletes the surrounding whitespace
        Alt-^: joins line to previous line. 
        
    transposing:
        Alt-t: marks a word for moving.  2nd execution on word, trades positions of 1rst word with 2nd word. 
                 
    movement:
        Alt-&lt; (less then sign ): move to the beginning of buffer
        Alt-&gt; (greater then sign ): move to the end of the buffer
        Ctrl a: move to the beginning of line
        Ctrl e: move to end of the line
        Alt m: move to the end of the indentation on the current line.
        
    balanced parentheses or sexps:
        Ctrl Alt f: moves forward to matching parentheses.
        Ctrl Alt b: moves backwards to matching parentheses 
        Ctrl Alt k: kills the sexp forward. Can subsequently be yanked
        Ctrl Alt Delete: kills the sexp backward. Can subsequently be yanked
    
    
    zapping:
        Alt-z: zaps to the character specified by the user.
    
    Ctrl x: This keystroke prepares SwingMacs for another keystroke.  These are:
        Ctrl o: This deletes blanklines surrounding the current line. 
        
    tags:
        tags are definitions of language constructs.  Language specific tags:
            Python: def and class
            Java: class and methods
            
        keystrokes:
            Alt-. : queries the user for the tag they wish to goto.  If Enter is typed
                    the current word is used for the tag
            Ctrl-U Alt-. : goes to the next definition of a tag.  Useful if there are multiple
                           definitions for a tag.
            Alt-* : pops the buffer/node back to the last place Alt-. and friends were executed.
                    This can be executed multiple times, if Alt-. was executed multiple times,
                    taking the user back to where he started jumping.
    
    
    '''
    
    addstring = "\n".join( self.keystroke_help )
    
    helptext += addstring
    
    return helptext</t>
<t tx="orkman.20050212095512">def walkKB( self ): #, event , frm, which ):# kb = self.iterateKillBuffer() ):

    #tbuffer = event.widget
    #i = tbuffer.index( 'insert' )
    #t , t1 = i.split( '.' )
    pos = self.emacs.editor.getCaretPosition()
    if pos != self.lastKBSpot:
        self.emacs.clearAttribute( 'kb' )
    self.lastKBSpot = pos
    clip_text = self.doesClipboardOfferNewData() #  self.getClipboard()  
    #clip_txt = g.app.gui.getTextFromClipboard().   
    if self.killbuffer or clip_text:
            #if which == 'c':
            #self.reset = True
            if clip_text:
                txt = clip_text
            else:
                txt = self.kbiterator.next()
            self.emacs.removeTextWithAttribute( 'kb' )
            self.emacs.insertTextWithAttribute( txt, 'kb' )
            self.emacs.editor.setCaretPosition( pos )
            #tbuffer.tag_delete( 'kb' )
            #tbuffer.insert( frm, txt, ('kb') )
            #tbuffer.mark_set( 'insert', i )
            #else:
            #if clip_text:
            #    txt = clip_text
            #else:
            #    txt = self.kbiterator.next()
            #t1 = str( int( t1 ) + len( txt ) )
            #r = tbuffer.tag_ranges( 'kb' )
            #if r and r[ 0 ] == i:
            #    tbuffer.delete( r[ 0 ], r[ -1 ] )
            #tbuffer.tag_delete( 'kb' )
            #tbuffer.insert( frm, txt, ('kb') )
            #tbuffer.mark_set( 'insert', i )
            #return self._tailEnd( tbuffer )
            
    return True</t>
<t tx="orkman.20050212100208">def doesClipboardOfferNewData( self  ):
    
    ctxt = None
    try:
        #ctxt = tbuffer.selection_get( selection='CLIPBOARD' )
        ctxt = g.app.gui.getTextFromClipboard()
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
<t tx="orkman.20050212100715">def iterateKillBuffer( self ):

    while 1:
        if self.killbuffer:
            self.last_clipboard = None
            for z in self.killbuffer:
                if self.reset:
                    self.reset = False
                    break        
                yield z</t>
<t tx="orkman.20050212113553">def kill( self, frm, end ):
    
    editor = self.emacs.editor
    doc = editor.getStyledDocument()
    if frm != end:
        txt = doc.getText( frm, end - frm )
        doc.replace( frm, end - frm, "", None )
        self.insertIntoKillbuffer( txt )
        g.app.gui.replaceClipboardWith( txt )
    else:
        if frm != doc.getLength():
            doc.replace( frm, 1, "", None )</t>
<t tx="orkman.20050212114308">def killRegion( self ):
    
    region = self.getRegion()
    if region:
        self.kill( *region )
    return True</t>
<t tx="orkman.20050212114641">def insertIntoKillbuffer( self, txt ):
    
    self.killbuffer.insert( 0, txt )
    self.reset = True</t>
<t tx="orkman.20050212115022">def copyRegion( self ):

    region = self.getRegion()
    if region:
        editor = self.emacs.editor
        doc = editor.getStyledDocument()
        start = region[ 0 ]
        end = region[ 1 ]
        txt = doc.getText( start, end-start )
        self.insertIntoKillbuffer( txt )
    return True</t>
<t tx="orkman.20050212115022.1">def getRegion( self ):

    editor = self.emacs.editor
    start = editor.getSelectionStart()
    end = editor.getSelectionEnd()
    if end == start: return None
    else:
        return start, end</t>
<t tx="orkman.20050212120210">class deleter:
    
    def __init__( self, emacs ):
        self.emacs = emacs
        
        
    def __call__( self, event, command ):
        
        
        if command == 'Delete':
            return self.deletePreviousChar()
        if command == 'Ctrl D':
            return self.deleteNextChar()
            
    @others</t>
<t tx="orkman.20050212120210.1">def deletePreviousChar( self ):
    
    editor = self.emacs.editor
    pos = editor.getCaretPosition()
    if pos != 0:
        doc = editor.getStyledDocument()
        spos = pos -1
        doc.replace( spos, 1 , "", None )
    return True</t>
<t tx="orkman.20050212120620">def deleteNextChar( self ):
    
    editor = self.emacs.editor
    pos = editor.getCaretPosition()
    doc = editor.getStyledDocument()
    if pos != doc.getLength():
        doc.replace( pos, 1 , "", None )
    return True</t>
<t tx="orkman.20050212121301">class alt_x_handler:
    
    def __init__( self, emacs ):
        self.emacs = emacs
        self.defineCommands()
        self.last_command = None
        self.keys = []
        
    def defineCommands( self ):
        
        sO = self.emacs.strategyObjects
        self.commands = {
        
        'open-rectangle': sO[ 'rectangles' ],        
        'delete-rectangle': sO[ 'rectangles' ],
        'clear-rectangle': sO[ 'rectangles' ],
        'delete-whitespace-rectangle': sO[ 'rectangles' ],
        'string-insert-rectangle': sO[ 'rectangles' ],
        'string-rectangle': sO[ 'rectangles' ],
        'kill-rectangle': sO[ 'rectangles' ],
        'yank-rectangle': sO[ 'rectangles' ],
        'zap-to-char': sO[ 'zap' ],
        'comment-region': sO[ 'comment' ],
        'comment-kill': sO[ 'comment' ],
        'goto-line': sO[ 'movement' ],
        'goto-char': sO[ 'movement' ],
        'transpose-lines': sO[ 'transpose' ],
        'upcase-region': sO[ 'capitalization' ],
        'downcase-region': sO[ 'capitalization' ],
        'capitalize-region': sO[ 'capitalization' ],
        'capitalize-word': sO[ 'capitalization' ],
         'downcase-word': sO[ 'capitalization' ],
         'upcase-word': sO[ 'capitalization' ],
        'query-replace': sO[ 'replacement' ],
        'query-replace-regexp': sO[ 'replacement' ],
        'replace-string': sO[ 'replacement' ],
        'sort-lines': sO[ 'sorters' ],
        'reverse-region': sO[ 'transpose' ],
        'keep-lines': sO[ 'lines' ],
        'flush-lines': sO[ 'lines' ],
        'indent-rigidly': sO[ 'formatter' ],
        'indent-region': sO[ 'formatter' ],
        'indent-relative': sO[ 'formatter' ],
        'tabify': sO[ 'tabs' ],
        'untabify': sO[ 'tabs' ],
        'copy-to-register': sO[ 'registers' ],
        'insert-register': sO[ 'registers' ],
        'append-to-register': sO[ 'registers' ],
        'prepend-to-register': sO[ 'registers' ],
        
        } 
     
            
        
        
    def createTabCompleter( self ):
        self.keys = self.commands.keys()
        self.tbCompleter = self.emacs.TabCompleter( self.keys )
       
    def __call__( self, event, command ):
        
        if command == 'Alt X':
            self.tbCompleter.reset()
            self.last_command = None
            self.emacs._stateManager.setState( 'xcommand' ) 
            self.emacs.setCommandText( "Alt-x:" )
            return True
        
        if command == 'Tab':
            
            txt = self.emacs.minibuffer.getText()
            if self.last_command == None or not txt.startswith( self.last_command ):
                txt = self.emacs.minibuffer.getText()
                fnd = self.tbCompleter.lookFor( txt )
                if fnd:
                    self.last_command = txt
                    self.emacs.minibuffer.setText( self.tbCompleter.getNext() )
            else :
                self.emacs.minibuffer.setText( self.tbCompleter.getNext() )
            return True
        
        if command == 'Enter':
            return self.execute( event, command )
        else:
            self.emacs.eventToMinibuffer( event )
            return True    
    
    def execute( self, event, command ):
        
        txt = self.emacs.minibuffer.getText()
        if self.commands.has_key( txt ):
            return self.commands[ txt ]( event, txt )
        else:
            self.emacs.keyboardQuit( event )
            self.emacs.setCommandText( "Command Not Defined" )
     

    @others</t>
<t tx="orkman.20050213105021">class KeyProcessor(aevent.KeyListener):

    '''KeyListener calls and newline analyzer.'''

    @others</t>
<t tx="orkman.20050213105021.1">def __init__ (self,emacs):

    self.emacs = emacs
    self.kRconsume = False # True: consume the event for key-released eveants.
    self.kTconsume = False # True: consume the event for key events.
    self.completers = {}
    self.tab_for_colon = False
    self.tab_width = g.app.config.getInt(emacs.c,"tab_width")</t>
<t tx="orkman.20050213105021.2">def keyReleased (self,event):

    if self.kRconsume:
        self.kRconsume = False
        event.consume()</t>
<t tx="orkman.20050213105021.3">def keyTyped (self,event):

    if self.kTconsume:
        self.kTconsume = False
        event.consume()</t>
<t tx="orkman.20050213105021.4">def keyPressed (self,event):

    &lt;&lt; create the command &gt;&gt;
    self.kTconsume = self.kRconsume = consume = self.emacs.masterCommand(event,command)
    if consume:
        # Block the event from going elsewhere, like the DocumentModel.
        event.consume()
        return

    kc = event.getKeyChar()
    if self.tab_for_colon and kc == '\n':
        event.consume()
        self.insertPreviousLeadAndNewline()
    if self.completers.has_key(kc):
        &lt;&lt; handle auto completion &gt;&gt;
    elif kc == '\t' and self.tab_width == -4:
        &lt;&lt; handle auto-tabbing &gt;&gt;
</t>
<t tx="orkman.20050213105513">def insertPreviousLeadAndNewline (self):
    &lt;&lt; why is this code here       ? &gt;&gt;

    editor = self.emacs.editor
    doc = editor.getDocument()
    pos = editor.getCaretPosition()
    start_text = doc.getText(0,pos)
    ind = start_text.rfind('\n')

    if ind &gt; 0:
        line = start_text [ind:].strip('\n')
    else:
        line = start_text.strip('\n')

    i = len(line.lstrip())

    if i == 0:
        instring = line
    else:
        instring = line [:-i]

    instring = '\n%s' % instring
    #printspaces
    #instring = "%s%s" %( spaces, instring )
    if line.strip().endswith(":"):
        if self.tab_width == -4:
            instring += " " * 4
        else:
            instring += "\t"
    doc.insertString(pos,instring,None)</t>
<t tx="orkman.20050213105513.1">'''
Originally this was in the leoSwingBody class.  This seemed right, it is core functionaliy.  But
In light of SwingMacs I reconsidered where it should go.  Temacs was a plugin, SwingMacs is core.
SwingMacs is responsible for processing key presses and such, consuming them if they are not to get
to the DocumentModel.  By placing this method in leoSwingBody, the Key processing responsibilities get
spread out.  Hence it makes more sense to move this method here, the responsibilites stay clearer.
'''</t>
<t tx="orkman.20050213110235">def defineStrategyObjects( self ):
        
    self.strategyObjects = {
        
    'incremental': self.incremental( self ),
    'dynamic-abbrev' : self.dynamicabbrevs( self ),
    'formatter' : self.formatter( self ),
    'killbuffer': self.killbuffer( self ),
    'deleter': self.deleter( self ),
     #'xcommand': self.alt_x_handler( self ),
    'rectangles': self.rectangles( self ),
    'zap': self.zap( self ),
    'comment': self.comment( self ),
    'movement': self.movement( self ),
    'transpose': self.transpose( self ),
    'capitalization': self.capitalization( self ),
    'replacement': self.replacement( self ),
    'sorters': self.sorters( self ),
    'lines': self.lines( self ),
    'tabs': self.tabs( self ),
    'registers': self.registers( self ),
    'selection': self.selection( self ),
    'completion': self.symbolcompletion( self ),
    'sexps': self.balanced_parentheses( self ),
    'tags': self.tags( self ),
     
    }
    
    self.strategyObjects[ 'xcommand' ] = self.alt_x_handler( self )
    self.strategyObjects[ 'ctrlx' ] = self.ctrl_x_handler( self )
    self.strategyObjects[ 'ctrlu' ] = self.ctrl_u_handler( self )
    
    for z in extensions:
        try:
            add = z.getCommands()
            for z in add.keys():
                try:
                    sO = add[ z ]( self )
                    self.strategyObjects[ z ] = sO
                    ncommands = sO.addToAltX()
                    for z in ncommands:
                        self.strategyObjects[ 'xcommand' ].commands[ z ] = sO
                finally:
                    pass
        finally:
            pass    

    self.strategyObjects[ 'xcommand' ].createTabCompleter()</t>
<t tx="orkman.20050213110404">def defineStrategiesForKeystrokes( self ):
    
    cmds = self.strategyObjects
    callbacks = {
        'Ctrl S': cmds[ 'incremental' ],
        'Ctrl R': cmds[ 'incremental' ],
        'Alt Slash': cmds[ 'dynamic-abbrev' ],
        'Ctrl+Alt Slash': cmds[ 'dynamic-abbrev' ],
        'Ctrl+Alt Back Slash': cmds[ 'formatter' ],
        'Alt Back Slash': cmds[ 'formatter' ],
        'Alt+Shift 6': cmds[ 'formatter' ],
        'Ctrl K': cmds[ 'killbuffer' ],
        'Alt Y': cmds[ 'killbuffer' ],
        'Ctrl Y': cmds[ 'killbuffer' ],
        'Ctrl W': cmds[ 'killbuffer' ],
        'Alt W': cmds[ 'killbuffer' ],
        'Delete': cmds[ 'deleter' ],
        'Ctrl D': cmds[ 'deleter' ],
        'Alt X': cmds[ 'xcommand' ],
        'Alt+Shift Period': cmds[ 'movement' ],
        'Alt+Shift Comma': cmds[ 'movement' ],
        'Ctrl Left': cmds[ 'movement'],
        'Ctrl Right': cmds[ 'movement'],
        'Alt M': cmds[ 'movement' ],
        'Ctrl A': cmds[ 'movement' ],
        'Ctrl E': cmds[ 'movement' ],
        'Alt Z': cmds[ 'zap' ],
        'Ctrl Space': cmds[ 'selection' ],
        'Ctrl X': cmds[ 'ctrlx' ],
        'Alt T': cmds[ 'transpose' ],
        'Ctrl+Alt I': cmds[ 'completion' ],
        'Ctrl+Alt F': cmds[ 'sexps' ],
        'Ctrl+Alt B': cmds[ 'sexps' ],
        'Ctrl+Alt K': cmds[ 'sexps' ],
        'Ctrl+Alt Delete': cmds[ 'sexps' ],
        'Alt Period': cmds[ 'tags' ],
        'Alt+Shift 8': cmds[ 'tags' ],
        'Ctrl U': cmds[ 'ctrlu' ],
        
        }
        
    for z in cmds.keys():
        sO = cmds[ z ]
        if hasattr( sO, 'addToKeyStrokes' ):
            nstrokes = sO.addToKeyStrokes()
            if nstrokes:
                for z in nstrokes.keys():
                    callbacks[ z ] = nstrokes[ z ]
        
    self.callbacks = callbacks</t>
<t tx="orkman.20050213110511">@others</t>
<t tx="orkman.20050213110803">def masterCommand (self,event,command):
    '''
    All processing goes through here.
    Return True if the KeyProcessor should consume the event, thereby stopping its propagation.
    '''

    consume = False

    if command == 'Ctrl G':
        return self.keyboardQuit(event)

    if self._stateManager.hasState():
        # This handles the follow-on states of multi-state commands.
        return self._stateManager.filterTo(event,command)

    if self.callbacks.has_key(command):
        # This handles the initial state of multi-state commands.
        consume = self.callbacks [command] (event,command)

    if self._stateManager2.hasState():
        self._stateManager2.filterTo(event,command)

    return consume
</t>
<t tx="orkman.20050213110948">def __init__( self, editor, minibuffer, commandlabel, c , extracommands = None ):
    global extensions
    if extensions == None:
        x = self.lookForExtensions()
        extensions = x
        
    self.editor = editor
    self.minibuffer = minibuffer
    self.commandlabel = commandlabel
    self.c = c
    self.modeStrategies = []
    self.defineStrategyObjects()
    self.defineStrategiesForKeystrokes()
    
    self.kcb = self.KeyProcessor( self )
    self.editor.addKeyListener( self.kcb )
    #if g.app.config.getBool( c, "complete_tags" ):
    tm = self.TagMatcher( self )
    self.editor.addKeyListener( tm )
    
    self._stateManager = self.stateManager( self )
    self._stateManager2 = self.stateManager( self )
    self.command_help = []
    self.keystroke_help = []
    self.addCompleters()</t>
<t tx="orkman.20050223114739">def setCommandText( self, txt ):
    
    self.commandlabel.setText( txt )</t>
<t tx="orkman.20050223124157">def forwardSearch( self, pos, txt, stxt ):
    
    _stxt = stxt[ pos : ]
    return _stxt.find( txt )
    

def backwardSearch( self, pos, txt, stxt ):

    end = len( stxt ) - pos
    if end != 0:
        stxt = stxt[ : -end ]

    return stxt.rfind( txt )</t>
<t tx="zorcanda!.20050310144300">class rectangles:
    
    
    def __init__( self, emacs ):
        self.emacs = emacs
        self.commands = {
        
        'open-rectangle': self.openRectangle,
        'delete-rectangle': self.deleteRectangle,
        'clear-rectangle': self.clearRectangle,
        'delete-whitespace-rectangle': self.deleteWhiteSpaceRectangle,
        'string-insert-rectangle': self.stringInsertRectangle,
        'string-rectangle': self.stringRectangle,
        'kill-rectangle': self.killRectangle,
        'yank-rectangle': self.yankRectangle,
        
        }
        
        self.mode = None
        emacs.modeStrategies.append( self )
        self.last_killed_rectangle = None      
        
    def __call__( self, event, command ):
        
        if self.mode:
            if command == 'Enter':
                if self.mode == 1:
                    self.stringInsertRectangle()
                    return self.emacs.keyboardQuit( event )
                elif self.mode == 2:
                    self.stringRectangle()
                    return self.emacs.keyboardQuit( event )
            else:
                return  self.emacs.eventToMinibuffer( event )
        
        if command in self.commands:
            quit = self.commands[ command ]()
            if quit:
                return self.emacs.keyboardQuit( event )
            else: return True
        
    @others</t>
<t tx="zorcanda!.20050310153830">def openRectangle( self ):
        
    editor = self.emacs.editor
    start = editor.getSelectionStart()
    end = editor.getSelectionEnd()
    if start &gt; -1:
        
        txt = editor.getText()
        
        pos, pos2, rl_start, rl_end = self.definePoints( start, end )  
        txt = txt[ rl_start: end ]
    
        
        insert = ' ' * ( pos2  - pos )

        txtline = txt.split( '\n' )

        ntxtlines = [  ]
        for z in txtline[ : ]:
            if( len( z ) - 1 ) &lt; pos:
                ntxtlines.append( z )
            else:
                nwline = '%s%s%s' %( z[ :pos ], insert, z[ pos : ] )
                ntxtlines.append( nwline )
        
        if txt[ -1 ] == '\n': ntxtlines.append( '\n' )            
        ntxt = '\n'.join( ntxtlines ) 
        
        return self.insertText( rl_start, end, ntxt )
        #sd = editor.getStyledDocument()
        #sd.remove( rl_start, end - rl_start )
        #sd.insertString( rl_start, ntxt, None ) 
        #return True</t>
<t tx="zorcanda!.20050310170120">class TabCompleter:

    def __init__ (self,data):
        self.data = data
        self.current = None
        self.current_iter = None

    def reset (self):
        self.current = None





</t>
<t tx="zorcanda!.20050310172646">def deleteRectangle( self ):
    
    editor = self.emacs.editor
    start = editor.getSelectionStart()
    end = editor.getSelectionEnd()
    if start &gt; -1:
        
        txt = editor.getText()
        
        pos, pos2, rl_start, rl_end = self.definePoints( start, end )
        txt = txt[ rl_start: end ]
    

        txtline = txt.split( '\n' )

        ntxtlines = [  ]
        for z in txtline[ : ]:
            if( len( z ) - 1 ) &lt; pos:
                ntxtlines.append( z )
            else:
                nwline = '%s%s' %( z[ :pos ], z[ pos2 : ] )
                ntxtlines.append( nwline )
        
        if txt[ -1 ] == '\n': ntxtlines.append( '\n' )            
        ntxt = '\n'.join( ntxtlines ) 
        
        #sd = editor.getStyledDocument()
        #sd.remove( rl_start, end - rl_start )
        #sd.insertString( rl_start, ntxt, None )     
        #return True 
        return self.insertText( rl_start, end, ntxt )</t>
<t tx="zorcanda!.20050310172920">def definePoints( self, start, end ):

    txt = self.emacs.editor.getText()
    rl_start = txt.rfind( '\n', 0, start )
    if rl_start == -1: rl_start = 0
    else: 
        rl_start = rl_start + 1
        
    pos = start - rl_start
        
    rl_end = txt.rfind( '\n', 0, end )
    if rl_end == -1: rl_end = 0
    else:
        rl_end = rl_end + 1  
        
    pos2 = end - rl_end
    
    return pos, pos2, rl_start, rl_end</t>
<t tx="zorcanda!.20050310182257">def clearRectangle( self ):
    
    
    editor = self.emacs.editor
    start = editor.getSelectionStart()
    end = editor.getSelectionEnd()
    if start &gt; -1:
        
        txt = editor.getText()
        
        pos, pos2, rl_start, rl_end = self.definePoints( start, end )
        txt = txt[ rl_start: end ]
    
        replace = ' ' * ( pos2  - pos )
        txtline = txt.split( '\n' )

        ntxtlines = [  ]
        for z in txtline[ : ]:
            if( len( z ) - 1 ) &lt; pos:
                ntxtlines.append( z )
            else:
                nwline = '%s%s%s' %( z[ :pos ], replace, z[ pos2 : ] )
                ntxtlines.append( nwline )
        
        if txt[ -1 ] == '\n': ntxtlines.append( '\n' )            
        ntxt = '\n'.join( ntxtlines ) 
        
        return self.insertText( rl_start, end, txt )
        #sd = editor.getStyledDocument()
        #sd.remove( rl_start, end - rl_start )
        #sd.insertString( rl_start, ntxt, None )     
        #return True</t>
<t tx="zorcanda!.20050310183117">def deleteWhiteSpaceRectangle( self ):
    
    editor = self.emacs.editor
    start = editor.getSelectionStart()
    end = editor.getSelectionEnd()
    if start &gt; -1:
        
        txt = editor.getText()
        
        pos, pos2, rl_start, rl_end = self.definePoints( start, end )
        txt = txt[ rl_start: end ]
        txtline = txt.split( '\n' )

        ntxtlines = [  ]
        for z in txtline[ : ]:
            if( len( z ) - 1 ) &lt; pos:
                ntxtlines.append( z )
            else:
                if z[ pos ].isspace():
                    space_text = z[ pos: pos2 ]
                    space_text = space_text.lstrip()
                    nwline = '%s%s%s' % ( z[ :pos ], space_text, z[ pos2 : ] )
                else:
                    nwline = z
                ntxtlines.append( nwline )
        
        if txt[ -1 ] == '\n': ntxtlines.append( '\n' )            
        ntxt = '\n'.join( ntxtlines ) 
        
        return self.insertText( tl_start, end, ntxt )
        #sd = editor.getStyledDocument()
        #sd.remove( rl_start, end - rl_start )
        #sd.insertString( rl_start, ntxt, None )      
        #return True</t>
<t tx="zorcanda!.20050310184934">def getCommandHelp( self ):
    
    commands = '''
    Commands are accessed by the Alt-X keystroke.  This will put the system in command mode.
    The user can type in the name of the command in the minibuffer and execute it with an Enter keypress.
    
    A shortcut to accessing commands is to type a prefix of the command in the minibuffer and hit Tab.
    
    For example:
    op(Tab press )
    could become:
    open-rectangle
    
    the user then just has to type Enter and the open-rectangle command is executed.  Also by repeatedly
    typing Tab the user will cycle through all commands that start with the entered prefix.  So if there
    were 5 commands, for example, that started with 'op' the user could cycle through them and choose the
    one that he wanted to execute.
    
    
    Rectangles
    -----------
    A Rectangle is defined by connecting 4 parallel points derived from
    the begining of the selction and the end of the selction.
    
    These commands operate on Rectangles:
    
    open-rectangle: inserts a whitespace equal to the rectangles width into each rectangle line.
    clear-rectangle: wipes out character content within the rectangle and replaces it with whitespace.
    delete-rectangle: removes characters within the rectangle.
    kill-rectangle: removes characters within the rectangle and stores the data in the kill rectangle
    yank-rectangle: inserts the data last stored by the kill-rectangle command
    delete-whitespace-rectangle: removes whitespace from the begining of each line in the rectangle.
    string-rectangle: replaces each section of the rectangle with a user specified string.
    string-insert-rectangle: inserts a user specified string into each section of the rectangle.
    
    
    Registers:
    ------------
    Registers are places, defined by the letters a-z, where the user can store data temporarily.  There
    are a variety of register commands:
        
    copy-to-register: copy the selected text to a register specified by the user.
    append-to-register: copy the selected text to the end of a register.
    prepend-to-register: copy the selected text to the beginning of a register.
    insert-register: insert a register into the current buffer.
    
    Zapping
    --------
    Zapping queries for a character from the current caret position.  If it finds the character,
    all data between the caret and including that character is removed.
    
    commands:
    zap-to-char: zaps to the specified character.
    
    Comments:
    ---------
    
    commands:
    comment-region: comments the selected region with the comment character for the current language.  If a line
                    within the region is commented, it will remove the comments instead of commenting.
    comment-kill: removes the comment on the current line
    
    Movement:
    ---------
    goto-line: moves the caret to the line specified by the user.
    goto-char: moves the caret to the character specified by the user.
    
    
    Transposition:
    --------------
    
    transpose-lines: swaps the current line with the line above it.
    reverse-region: takes region and reverses the ordering of the lines, last becomes first, first last.
    
    
    Capitalization:
    ---------------
    
    upcase-region: Upper cases all the text in the selection.
    downcase-region: Lower cases all the text in the selection.
    capitalize-region: Capitalizes all the text in the selection.
    upcase-word: Upper cases the current word.
    downcase-word: Lower cases the current word.
    capitalize-word: Capitalizes the current word. 
    
    Querying and Replacing:
    -----------------------
    SwingMacs has several different query and replace commands.  Each asks the user
    for a search string/pattern and text to replace matches with.  Each has different
    levels of interactivity.
    
    commands:
    query-replace: asks the user for a string to match and a string to replace.  Is asked for each individual word
                   if replacement is desired. '!' replaces all.
    query-replace-regexp: asks the user for a regular expression to match and a string to replace.  Is asked for each individual word
                   if replacement is desired. '!' replaces all.  The regular expressions are executed from the java.util.regex
                   package, see details in javadoc.
    replace-string: asks user for a string to match and a replacement string.  Upon execution all matches are replaced.
    
    Sorting:
    --------
    
    sort-lines: sorts the selected lines of text. 
    
    Lines:
    ------
    
    flush-lines: removes lines that match a regular expression. The regular expressions are executed from the java.util.regex
                   package, see details in javadoc.
                   
    keep-lines: keeps lines that match a regular expression.  Same regular expression details as flush-lines.
    
    Indenting:
    ----------
    
    indent-region: indents region to the indentation of the first line in the region.
    indent-rigidly: indents region by a tab   
    indent-relative: indents by these rules:
        1. If no previous line, indents by a tab
        2. If a previous line, will indent to the first word of that line.  This process
        continues from word to word on the previous line.
    
    Tabs:
    -----
    
    tabify: changes spaces in selected region into tabs.
    untabify: changes tabs in selected region into spaces.          
    
    '''
    
    more_help = '\n'.join( self.emacs.command_help )
    
    commands += more_help
    
    return commands</t>
<t tx="zorcanda!.20050311095932">def stringInsertRectangle( self ):
    
    if self.mode == None:
        self.mode = 1
        self.emacs.setCommandText( "string-insert-rectangle" )
        self.emacs.minibuffer.setText( "" )
        self.emacs._stateManager.setState( 'rectangles' )
        return False
        
        
    self.mode = None
    string_txt = self.emacs.minibuffer.getText()
    
    editor = self.emacs.editor
    start = editor.getSelectionStart()
    end = editor.getSelectionEnd()
    if start &gt; -1:
        
        txt = editor.getText()
        
        pos, pos2, rl_start, rl_end = self.definePoints( start, end )
        txt = txt[ rl_start: end ]
        txtline = txt.split( '\n' )

        ntxtlines = [  ]
        for z in txtline[ : ]:
            if( len( z ) - 1 ) &lt; pos:
                ntxtlines.append( z )
            else:
                nwline = '%s%s%s' % ( z[ :pos ], string_txt , z[ pos : ] )
                ntxtlines.append( nwline )
        
        if txt[ -1 ] == '\n': ntxtlines.append( '\n' )            
        ntxt = '\n'.join( ntxtlines ) 
        
        return self.insertText( rl_start, end, ntxt )
        #sd = editor.getStyledDocument()
        #sd.remove( rl_start, end - rl_start )
        #sd.insertString( rl_start, ntxt, None )         
        #return True</t>
<t tx="zorcanda!.20050311102030">def stringRectangle( self ):
    
    if self.mode == None:
        self.mode = 2
        self.emacs.setCommandText( "string-rectangle" )
        self.emacs.minibuffer.setText( "" )
        self.emacs._stateManager.setState( 'rectangles' )
        return False
        
        
    self.mode = None
    string_txt = self.emacs.minibuffer.getText()
    
    editor = self.emacs.editor
    start = editor.getSelectionStart()
    end = editor.getSelectionEnd()
    if start &gt; -1:
        
        txt = editor.getText()
        
        pos, pos2, rl_start, rl_end = self.definePoints( start, end )
        txt = txt[ rl_start: end ]
        txtline = txt.split( '\n' )

        ntxtlines = [  ]
        for z in txtline[ : ]:
            if( len( z ) - 1 ) &lt; pos:
                ntxtlines.append( z )
            else:
                nwline = '%s%s%s' % ( z[ :pos ], string_txt , z[ pos2 : ] )
                ntxtlines.append( nwline )
        
        if txt[ -1 ] == '\n': ntxtlines.append( '\n' )            
        ntxt = '\n'.join( ntxtlines ) 
        
        return self.insertText( rl_start, end, ntxt )
        #sd = editor.getStyledDocument()
        #sd.remove( rl_start, end - rl_start )
        #sd.insertString( rl_start, ntxt, None )         
        #return True</t>
<t tx="zorcanda!.20050311102520">def killRectangle( self ):
    
    editor = self.emacs.editor
    start = editor.getSelectionStart()
    end = editor.getSelectionEnd()
    if start &gt; -1:
        
        txt = editor.getText()
        
        pos, pos2, rl_start, rl_end = self.definePoints( start, end )
        txt = txt[ rl_start: end ]
    

        txtline = txt.split( '\n' )

        ntxtlines = [  ]
        oldlines = []
        for z in txtline[ : ]:
            if( len( z ) - 1 ) &lt; pos:
                ntxtlines.append( z )
                oldlines.append( z )
            else:
                nwline = '%s%s' %( z[ :pos ], z[ pos2 : ] )
                ntxtlines.append( nwline )
                oldlines.append( z[ pos: pos2 ] )
        
        if txt[ -1 ] == '\n': ntxtlines.append( '\n' )            
        ntxt = '\n'.join( ntxtlines ) 
        
        #sd = editor.getStyledDocument()
        #sd.remove( rl_start, end - rl_start )
        #sd.insertString( rl_start, ntxt, None )
        self.last_killed_rectangle = oldlines  
        return self.insertText( rl_start, end, ntxt )   
        #return True</t>
<t tx="zorcanda!.20050311102817">def yankRectangle( self ):
    
    if self.last_killed_rectangle == None: return True
    
    editor = self.emacs.editor
    start = editor.getCaretPosition()
    
    if start &gt; -1:
        
        txt = editor.getText()
        
        rl_start = txt.rfind( '\n', 0, start )
        if rl_start == -1: rl_start = 0
        else: 
            rl_start = rl_start + 1
            
        
        pos = start - rl_start
        
        sd = editor.getStyledDocument()
        start2 = rl_start
        for itext in self.last_killed_rectangle:
            
            if sd.getLength() &lt; start2:
                sd.insertString( sd.getLength(), '%s%s' %( itext, '\n' ), None )
                start2 += len( itext ) + 1
            else:
                if( sd.getText( start2 , 1 ) == '\n' ):
                    sd.insertString( start2, itext, None )
                    nspot = start2 + len( itext )
                else:
                    sd.insertString( start2 + pos, itext, None )
                    nspot = start2 + pos + len( itext )
      
                ftxt = sd.getText( 0, sd.getLength() )
                where = ftxt.find( '\n', nspot )
                if where == -1:
                    sd.insertString( sd.getLength(), '\n', None )
                    start2 = sd.getLength() + 1
                else:
                    start2 = where + 1   
            
        
        return True</t>
<t tx="zorcanda!.20050311121612">def insertText( self, rl_start, end, ntxt ):
 
    sd = self.emacs.editor.getStyledDocument()
    sd.remove( rl_start, end - rl_start )
    sd.insertString( rl_start, ntxt, None ) 
    return True</t>
<t tx="zorcanda!.20050311123122">class zap:
    
    def __init__( self, emacs ):
        
        self.emacs = emacs
        self.mode = None
        emacs.modeStrategies.append( self )
        
    def __call__( self, event, command ):
        
        if self.mode == None:
            
            self.mode = 1
            self.emacs._stateManager.setState( 'zap' )
            self.emacs.setCommandText( "Zap To Character:" )
            self.emacs.minibuffer.setText( "" )
            return True
            
        if command == 'Enter':
            c = self.emacs.minibuffer.getText()
            if len( c ) &gt; 1:
                self.emacs.keyboardQuit( event )
                self.emacs.setCommandText( "Text longer than one Character" )
                return True
            
            self.zap( c )
            return self.emacs.keyboardQuit( event )
        
        else:
            kc = event.getKeyChar()
            if java.lang.Character.isDefined( kc ):
                message = self.zap( kc )
                self.emacs.keyboardQuit( event )
                if message:
                    self.emacs.setCommandText( message )
                return True
            else:
                return True
            
            
    @others</t>
<t tx="zorcanda!.20050311123122.1">def zap( self, c ):
    
    editor = self.emacs.editor
    doc = editor.getStyledDocument()
    pos = editor.getCaretPosition()
    txt = editor.getText( pos, ( doc.getLength() - 1 ) - pos  )
    ind = txt.find( c )
    if ind == -1:
        self.emacs.beep()
        return "Search Failed: '%s'" % c
    else:
        doc.remove( pos, ind + 1 )</t>
<t tx="zorcanda!.20050311123715">def beep( self ):
    
    tk = awt.Toolkit.getDefaultToolkit()
    tk.beep()</t>
<t tx="zorcanda!.20050311140549">def determineLanguage( self ):
    
    pos = self.c.currentPosition()
    language = g.scanForAtLanguage( self.c, pos )
    return language</t>
<t tx="zorcanda!.20050311140549.1">class comment:

    def __init__( self, emacs ):
        self.emacs = emacs
        self.commands ={
            'comment-region': self.commentRegion,
            'comment-kill': self.commentKill,
        }
        
    def __call__( self, event, command ):
        
        message = self.commands[ command ]()
        if message:
            self.emacs.keyboardQuit( event )
            self.emacs.setCommandText( message )
            self.emacs.beep()
            return True
        else:
            return self.emacs.keyboardQuit( event )

    @others</t>
<t tx="zorcanda!.20050311140549.2">def commentRegion( self ):
    
    language = self.emacs.determineLanguage()
    delim1,delim2, delim3 = g.set_delims_from_language( language )
    
    editor = self.emacs.editor
    sel = editor.getSelectedText()
    if sel == None: return
    
    lines = sel.splitlines( True )
    nwlines = []
    for z in lines:
        
        if z.find( delim1 ) != -1:
            nwline = z.replace( delim1, "" )
            nwlines.append( nwline )
        else:
            z2 = z.lstrip()
            ins = ( len( z ) - len( z2 ) )
            if ins == -1: ins = 0
            nwline = '%s%s%s' %( z[ : ins ], delim1, z[ ins: ] )
            nwlines.append( nwline )
        
    
    nwtext = ''.join( nwlines )
    editor.replaceSelection( nwtext )</t>
<t tx="zorcanda!.20050311143148">def commentKill( self ):
    
    
    editor = self.emacs.editor
    pos = editor.getCaretPosition()
    if pos == -1: return "Invalid Caret position"
    else:
        txt = editor.getText()
        i = txt.rfind( '\n', 0, pos )
        if i == -1: i = 0
        else: i += 1
        
        i2 = txt.find( '\n', pos )
        if i2 == -1: i2 = len( txt )
        
        line = txt[ i: i2 ]
        language = self.emacs.determineLanguage()
        delim1,delim2, delim3 = g.set_delims_from_language( language )
        
        where = line.find( delim1 )
        if where == -1: return "No comment found"
        
        else:
            nline = line[ :where ]
            
            sdoc = editor.getStyledDocument()
            sdoc.replace( i, len( line ), nline, None )
            if ( pos - i ) &lt; where: editor.setCaretPosition( pos )
            return</t>
<t tx="zorcanda!.20050311150743">class movement:
    
    def __init__( self, emacs ):
        
        self.emacs = emacs
        self.commands = {
            'Alt+Shift Comma': self.beginningOfBuffer,
            'Alt+Shift Period': self.endOfBuffer,
            'Ctrl A': self.beginningOfLine,
            'Ctrl E': self.endOfLine,
            'Ctrl Left': self.startOfWord,
            'Ctrl Right': self.endOfWord,
            'goto-line': self.goto,
            'goto-char': self.gotoChar,
            'Alt M': self.moveToIndentStart
        }
        self.mode = None
        self.emacs.modeStrategies.append ( self )
        
    def __call__( self, event, command ):
        
        if self.mode:
            if command == 'Enter':
                if self.mode == 1:
                    message = self.goto()
                else:
                    message = self.gotoChar()
                    
                if message:
                    self.emacs.keyboardQuit( event )
                    self.emacs.setCommandText( message )
                    self.emacs.beep()
                    return True
                else:
                    return self.emacs.keyboardQuit( event )
                
            else:
                return self.emacs.eventToMinibuffer( event )
        self.commands[ command ]()
        return True
        
    @others</t>
<t tx="zorcanda!.20050311150743.1">def beginningOfBuffer( self ):

    editor = self.emacs.editor
    editor.setCaretPosition( 0 )</t>
<t tx="zorcanda!.20050311150743.2">def endOfBuffer( self ):
    
    editor = self.emacs.editor
    sdoc = editor.getStyledDocument()
    editor.setCaretPosition( sdoc.getLength() -1 )</t>
<t tx="zorcanda!.20050311151807">def beginningOfLine( self ):
    
    editor = self.emacs.editor
    pos = editor.getCaretPosition()
    if pos != -1:
        
        txt = editor.getText()
        where = txt.rfind( '\n', 0, pos )
        if where == -1: where = 0
        else: where +=1
        #print stext.Utilities.getRowStart( editor, pos )
        #print where
        spot = stext.Utilities.getRowStart( editor, pos )
        editor.setCaretPosition( spot )
        
        #editor.setCaretPosition( where )</t>
<t tx="zorcanda!.20050311151807.1">def endOfLine( self ):
    
    editor = self.emacs.editor
    pos = editor.getCaretPosition()
    if pos != -1:
        
        txt = editor.getText()
        where = txt.find( '\n', pos )
        if where == -1: where = len( txt )
        #elif where != 0:
        #    where -= 1
        #print stext.Utilities.getRowEnd( editor, pos )
        #print where
        spot = stext.Utilities.getRowEnd( editor, pos )
        editor.setCaretPosition( spot )
        
        #editor.setCaretPosition( where )</t>
<t tx="zorcanda!.20050311154238">def goto( self ):
    
    if self.mode == None:
        self.mode = 1
        self.emacs._stateManager.setState( 'movement' )
        self.emacs.minibuffer.setText( "" )
        self.emacs.setCommandText( "Goto Line:" )
        return True
        
        
        
    line = self.emacs.minibuffer.getText()
    if not line.isdigit(): 
        return "Is Not a Number"
       
    line = int( line )
    editor = self.emacs.editor
    
    txt = editor.getText()
    txtlines = txt.splitlines( True )
    if len( txtlines ) &lt; line:
        editor.setCaretPosition( len( txt ) )
    else:
        txtlines = txtlines[ : line ]
        length =  len( ''.join( txtlines ) )
        editor.setCaretPosition( length - len( txtlines[ -1 ] ) )</t>
<t tx="zorcanda!.20050311154238.1">def gotoChar( self ):
    
    if self.mode == None:
        self.mode = 2
        self.emacs._stateManager.setState( 'movement' )
        self.emacs.minibuffer.setText( "" )
        self.emacs.setCommandText( "Goto Char:" )
        return True
        
    line = self.emacs.minibuffer.getText()
    if not line.isdigit(): 
        return "Is Not a Number"
        
        
    number = int( line )
    editor = self.emacs.editor
    ltxt = len( editor.getText() )
    if ltxt &lt; number:
        editor.setCaretPosition( ltxt )
    else:
        editor.setCaretPosition( number )</t>
<t tx="zorcanda!.20050311160343">class transpose:
    
    def __init__( self, emacs ):
        
        self.emacs = emacs
        self.commands = {
            'transpose-lines': self.transposeLines,
            'reverse-region': self.reverseRegion,
            'Alt T': self.transposeWords,
        }
        
    def __call__( self, event, command ):
        
    
        if not self.commands[ command ]():
            return self.emacs.keyboardQuit( event )  
        return True
        
        
    @others</t>
<t tx="zorcanda!.20050311160343.1">def transposeLines( self ):
    
    editor = self.emacs.editor
    pos = editor.getCaretPosition()
    if pos != -1:
        
        txt = editor.getText()
        start = txt.rfind( '\n', 0, pos )
        if start == -1: start = 0
        else:
            if start != 0:
                start = txt.rfind( '\n', 0, start )
                if start == -1: start = 0
                else: 
                    start += 1
        
        end = txt.find( '\n', pos )
        if end == -1: end = len( txt )
           
    
        lines = txt[ start: end ]
        lines_split = lines.split( '\n' )
        if not len( lines_split ) == 2: return
        l1, l2 = lines_split[ 0 ], lines_split[ 1 ]
        
        nwlines = '%s\n%s' %( l2, l1 )
        sdoc = editor.getStyledDocument()
        sdoc.replace( start, len( lines ), nwlines, None )</t>
<t tx="zorcanda!.20050311163509">class capitalization:
    
    def __init__( self, emacs ):
        self.emacs = emacs
        self.commands ={
            'capitalize-region': self.capitalizeRegion,
            'upcase-region': self.upcaseRegion,
            'downcase-region': self.downcaseRegion,
            'capitalize-word': self.capitalizeWord,
            'downcase-word': self.downcaseWord,
            'upcase-word': self.upcaseWord,
        }
        
    def __call__( self, event, command ):
        
        message = self.commands[ command ]()
        if message:
            self.emacs.keyboardQuit( event )
            self.emacs.setCommandText( message )
            self.emacs.beep()
            return True
            
        return self.emacs.keyboardQuit( event )

    @others</t>
<t tx="zorcanda!.20050311163509.1">def capitalizeRegion( self ):

    editor = self.emacs.editor
    stext = editor.getSelectedText()
    if stext == None:
        return "Region not selected"
        
    ntext = []
    lc = ' '
    for z in stext:
        if lc.isspace():
            z2 = z.capitalize()
            ntext.append( z2 )
        else:
            ntext.append( z )
        lc = z
        
    ntext = ''.join( ntext )
    editor.replaceSelection( ntext )</t>
<t tx="zorcanda!.20050311163509.2">def upcaseRegion( self ):
    
    editor = self.emacs.editor
    stext = editor.getSelectedText()
    if stext == None:
        return "Region not selected"
        
    ntext = stext.upper()
    editor.replaceSelection( ntext )</t>
<t tx="zorcanda!.20050311163509.3">def downcaseRegion( self ):

    editor = self.emacs.editor
    stext = editor.getSelectedText()
    if stext == None:
        return "Region not selected"
        
    ntext = stext.lower()
    editor.replaceSelection( ntext )</t>
<t tx="zorcanda!.20050311165606">class replacement:
    import java.util.regex as regex
    
    def __init__( self, emacs ):
        
        self.emacs = emacs
        self.commands = {
            'query-replace': self.queryReplace,
            'query-replace-regexp': self.queryReplaceRegexp,
            'replace-string': self.replaceString,
        }

        self.mode = None
        self.submode = None
        
        self.search = None
        self.replacement = None
        
        emacs.modeStrategies.append( self )
        
        
    def __call__( self, event, command ):
        
        if self.mode:
            if self.mode in( 1, 2 ):
                qcommand = g.choose( self.mode == 1, self.queryReplace, self.queryReplaceRegexp )
                if self.submode in( 1, 2 ):
                    if command == 'Enter':
                        return qcommand()
                    else:
                        return self.emacs.eventToMinibuffer( event )   
                if self.submode == 3:
                    message = self.doReplacement( event )
                    if message == None:
                        message = qcommand()
                    if message not in( True, False ) and message:
                        self.emacs.keyboardQuit( event )
                        self.emacs.minibuffer.setText( "" )
                        self.emacs.setCommandText( message )
                        return True
                    return True
            elif self.mode == 3:
                if command == 'Enter':
                    message = self.replaceString()
                    if message not in ( True, False ) and message:
                        self.emacs.keyboardQuit( event )
                        self.emacs.minibuffer.setText( "" )
                        self.emacs.setCommandText( message )
                        return True
                    else: return True
                else:
                    return self.emacs.eventToMinibuffer( event )
        
        return self.commands[ command ]()
        
        
    @others</t>
<t tx="zorcanda!.20050311165606.1">def queryReplace( self ):
    
    if self.mode == None:
        self.mode = 1
        self.submode = 1
        self.emacs.setCommandText( "Query For:" )
        self.emacs.minibuffer.setText( "" )
        self.emacs._stateManager.setState( "replacement" )
        return True
    
    if self.submode == 1:
        
        self.search = self.emacs.minibuffer.getText()
        self.emacs.minibuffer.setText( "" )
        self.emacs.setCommandText( "Replace With:" )
        self.submode = 2
        return True
        
    if self.submode == 2:
        
        self.replacement = self.emacs.minibuffer.getText()
        self.emacs.minibuffer.setText( "" )
        self.submode = 3
        
        
    if self.submode == 3:
        
        editor = self.emacs.editor
        pos = editor.getCaretPosition()
        txt = editor.getText()
        where = txt.find( self.search, pos )
        if where == -1:
            editor.setCaretPosition( editor.getSelectionEnd() )
            return "No more matches found"
        else:
            editor.setSelectionStart( where )
            editor.setSelectionEnd( where + len( self.search ) )
            self.emacs.setCommandText( "Replace %s with %s ? y/n(! replaces all)" %( self.search, self.replacement ) )
            return True</t>
<t tx="zorcanda!.20050311165606.2">def queryReplaceRegexp( self ):
    
    if self.mode == None:
        self.mode = 2
        self.submode = 1
        self.emacs.setCommandText( "Query For:" )
        self.emacs.minibuffer.setText( "" )
        self.emacs._stateManager.setState( "replacement" )
        return True
    
    if self.submode == 1:
        
        search = self.emacs.minibuffer.getText()
        import java.util.regex
        self.search = java.util.regex.Pattern.compile( search )
        self.emacs.minibuffer.setText( "" )
        self.emacs.setCommandText( "Replace With:" )
        self.submode = 2
        return True
        
    if self.submode == 2:
        
        self.replacement = self.emacs.minibuffer.getText()
        self.emacs.minibuffer.setText( "" )
        self.submode = 3
        
        
    if self.submode == 3:
        
        editor = self.emacs.editor
        pos = editor.getCaretPosition()
        txt = editor.getText()
        
        import java.lang.String
        match = self.search.matcher( java.lang.String( txt[ pos: ] ) )
        found = match.find()
        if found:
            start = match.start()
            end = match.end()
        else:
            start = end = -1
        if start == -1:
            editor.setCaretPosition( editor.getSelectionEnd() )
            return "No more matches found"
        else:
            editor.setSelectionStart( pos + start )
            editor.setSelectionEnd( pos + end )
            self.emacs.setCommandText( "Replace %s with %s ? y/n(! replaces all)" %( editor.getSelectedText(), self.replacement ) )
            return True</t>
<t tx="zorcanda!.20050311165732">def replaceString( self ):

    if self.mode == None:
        self.mode = 3
        self.submode = 1
        self.emacs.setCommandText( "Replace String:" )
        self.emacs.minibuffer.setText( "" )
        self.emacs._stateManager.setState( "replacement" )
        return True
    
    if self.submode == 1:
        
        self.search = self.emacs.minibuffer.getText()
        self.emacs.minibuffer.setText( "" )
        self.emacs.setCommandText( "Replace %s With:" % self.search )
        self.submode = 2
        return True    
        
    if self.submode == 2:
        
        replacement = self.emacs.minibuffer.getText()
        editor = self.emacs.editor
        pos = editor.getCaretPosition()
        txt = editor.getText()[ pos: ]
        amount = txt.count( self.search )
        ntxt = txt.replace( self.search, replacement )
        sd = editor.getStyledDocument()
        sd.replace( pos, len( txt ), ntxt, None )
        editor.setCaretPosition( pos )
        return "%s occurances of %s replaced with %s" %( amount, self.search, replacement )</t>
<t tx="zorcanda!.20050311170911">def doReplacement( self, event ):
    
    
    kc = event.getKeyChar()
    
    if not java.lang.Character.isDefined( kc ): return False
    elif kc == 'y':
        self.emacs.editor.replaceSelection( self.replacement )
        
    elif kc =='!':
        return self.replaceAll()
        
    else:
        pass</t>
<t tx="zorcanda!.20050311205755">def replaceAll( self ):
    
    editor = self.emacs.editor
    spos = editor.getSelectionStart()
    editor.setCaretPosition( spos )
    cp = editor.getCaretPosition()
    txt = editor.getText()[ cp : ]
    sd = editor.getStyledDocument()
    
    if self.mode == 1:
        amount = txt.count( self.search )
        ntxt = txt.replace( self.search, self.replacement )
        sd.replace( cp, len( txt ), ntxt, None )
        editor.setCaretPosition( spos )
        return '%s instances of %s replaced with %s' %( amount, self.search, self.replacement )
    else:
        import java.lang.String
        txt_s = java.lang.String( txt )
        scount = txt.count( self.replacement )
        #natxt = self.search.split( txt_s )
        #print "natxt len is %s" % len( natxt )
        matcher = self.search.matcher( txt_s )
        ntxt = matcher.replaceAll( self.replacement )
        ncount = ntxt.count( self.replacement )
        #ntxt = self.replacement.join( natxt )
        sd.replace( cp, len( txt ), ntxt, None )
        editor.setCaretPosition( spos )
        return '%s instances of %s replaced with %s' %( ncount - scount, self.search.pattern(), self.replacement )</t>
<t tx="zorcanda!.20050311214332">class sorters:
    
    def __init__( self, emacs ):
        self.emacs = emacs
        self.commands ={
        'sort-lines': self.sortLines
        }
        
    def __call__( self, event, command ):
        
        self.commands[ command ]()
        return self.emacs.keyboardQuit( event )
        
    @others</t>
<t tx="zorcanda!.20050311214332.1">def sortLines( self ):
    
    editor = self.emacs.editor
    txt = editor.getSelectedText()
    if txt == None: return
    txtlines = txt.splitlines()
    txtlines.sort()
    ntxt = '\n'.join( txtlines )
    if txt[ -1 ] == '\n': ntxt = '%s\n' % ntxt
    editor.replaceSelection( ntxt )</t>
<t tx="zorcanda!.20050311215703">def reverseRegion( self ):
    
    editor = self.emacs.editor
    txt = editor.getSelectedText()
    if txt == None: return
    txtlines = txt.splitlines( True )
    txtlines.reverse()
    if not txt.endswith( '\n' ):
        txtlines[ 0 ] = '%s\n' % txtlines[ 0 ]
    ntxt = ''.join( txtlines )
    editor.replaceSelection( ntxt )</t>
<t tx="zorcanda!.20050312111617">def capitalizeWord( self ):
    
    start, end = self.emacs.getWordStartIndex(), self.emacs.getWordEndIndex()
    
    if start != -1:
        
        sdoc = self.emacs.editor.getStyledDocument()
        txt = sdoc.getText( start, end - start )
        txt = txt.capitalize()
        pos = self.emacs.editor.getCaretPosition()
        sdoc.replace( start, len( txt ), txt, None )  
        self.emacs.editor.setCaretPosition( pos )</t>
<t tx="zorcanda!.20050312111617.1">def upcaseWord( self ):
    
    start, end = self.emacs.getWordStartIndex(), self.emacs.getWordEndIndex()
    
    if start != -1:
        
        sdoc = self.emacs.editor.getStyledDocument()
        txt = sdoc.getText( start, end - start )
        txt = txt.upper()
        pos = self.emacs.editor.getCaretPosition()
        sdoc.replace( start, len( txt ), txt, None )
        self.emacs.editor.setCaretPosition( pos )</t>
<t tx="zorcanda!.20050312111617.2">def downcaseWord( self ):

    start, end = self.emacs.getWordStartIndex(), self.emacs.getWordEndIndex()
    
    if start != -1:
        
        sdoc = self.emacs.editor.getStyledDocument()
        txt = sdoc.getText( start, end - start )
        txt = txt.lower()
        pos = self.emacs.editor.getCaretPosition()
        sdoc.replace( start, len( txt ), txt, None )
        self.emacs.editor.setCaretPosition( pos )</t>
<t tx="zorcanda!.20050312114506">class lines:
    import java.util.regex as regexp
    
    def __init__( self, emacs ):
        
        self.emacs = emacs
        self.mode = None
        self.commands= {
            'keep-lines': self.keepLines,
            'flush-lines': self.flushLines,
        }
        emacs.modeStrategies.append( self )
        
    def __call__( self, event, command ):
        
        if self.mode:
            if self.mode in ( 1, 2 ):
                if command == 'Enter':
                    if self.mode == 1:
                        self.keepLines()
                    else:
                        self.flushLines()
                    self.emacs.keyboardQuit( event )
                    return True
                else:
                    return self.emacs.eventToMinibuffer( event )

        return self.commands[ command ]()
        
    @others</t>
<t tx="zorcanda!.20050312114506.1">def keepLines( self ):
    import java.util.regex as regexp
    if self.mode == None:
        self.mode = 1
        self.emacs.setCommandText( "Keep lines( containing match for regexp ):" )
        self.emacs.minibuffer.setText( "" )
        self.emacs._stateManager.setState( "lines" )
        return True
    
    

    pattern = self.emacs.minibuffer.getText()
    regex = regexp.Pattern.compile( java.lang.String( pattern ) )
    
    editor = self.emacs.editor
    pos = editor.getCaretPosition()
    txt = editor.getText()
    start = txt.rfind( '\n', 0, pos )
    if start == -1: start = 0
    else: start += 1
    
    
    ntxt = txt[ start: ]
    ntxt_lines = ntxt.splitlines( True )

    matcher = regex.matcher( java.lang.String( ntxt_lines[ 0 ] ) )
    keepers = []
    for z in ntxt_lines:
        matcher.reset( java.lang.String( z ) )
        found = matcher.find()
        if found: keepers.append( z )
        
        
    keeptxt = ''.join( keepers )
    
    sdoc = editor.getStyledDocument()
    sdoc.replace( start, len( ntxt ), keeptxt, None )
    if ( sdoc.getLength() - 1 ) &gt;= pos:
        editor.setCaretPosition( pos )</t>
<t tx="zorcanda!.20050312114506.2">def flushLines( self ):

    import java.util.regex as regexp
    if self.mode == None:
        self.mode = 2
        self.emacs.setCommandText( "Flush lines( containing match for regexp ):" )
        self.emacs.minibuffer.setText( "" )
        self.emacs._stateManager.setState( "lines" )
        return True
    
    

    pattern = self.emacs.minibuffer.getText()
    regex = regexp.Pattern.compile( java.lang.String( pattern ) )
    
    editor = self.emacs.editor
    pos = editor.getCaretPosition()
    txt = editor.getText()
    start = txt.rfind( '\n', 0, pos )
    if start == -1: start = 0
    else: start += 1
    
    
    ntxt = txt[ start: ]
    ntxt_lines = ntxt.splitlines( True )

    matcher = regex.matcher( java.lang.String( ntxt_lines[ 0 ] ) )
    keepers = []
    for z in ntxt_lines:
        matcher.reset( java.lang.String( z ) )
        found = matcher.find()
        if found: continue
        keepers.append( z )
        
        
    keeptxt = ''.join( keepers )
    
    sdoc = editor.getStyledDocument()
    sdoc.replace( start, len( ntxt ), keeptxt, None )
    if ( sdoc.getLength() - 1 ) &gt;= pos:
        editor.setCaretPosition( pos )</t>
<t tx="zorcanda!.20050312121738">def indentRigidly( self ):
    
    editor = self.emacs.editor
    txt = editor.getSelectedText()
    if txt == None: return True
    
    txtlines = txt.splitlines( True )
    ntxtlines = []
    for z in txtlines:
        
        nline = '\t%s' % z
        ntxtlines.append( nline )
        
    
    ntxt = ''.join( ntxtlines )
    pos = editor.getCaretPosition()
    editor.replaceSelection( ntxt )
    editor.setCaretPosition( pos )
    return True</t>
<t tx="zorcanda!.20050312122805">class tabs:
    
    def __init__( self, emacs ):
        
        self.emacs = emacs
        self.commands ={
        
            'tabify': self.tabify,
            'untabify': self.untabify,
        
        
        
        }
        
    def __call__( self, event, command ):
        
        
        rval = self.commands[ command ]()
        self.emacs.keyboardQuit( event )
        return rval
        
    @others</t>
<t tx="zorcanda!.20050312122805.1">def tabify( self ):

    #tw = self.emacs.getTabWidth()
    editor = self.emacs.editor
    txt = editor.getSelectedText()
    if txt == None: return True
    
    #space_replace = ' ' * tw
    ntxt = txt.replace( ' ', '\t' )
    pos = editor.getCaretPosition()
    editor.replaceSelection( ntxt )
    editor.setCaretPosition( pos )
    return True</t>
<t tx="zorcanda!.20050312122805.2">def untabify( self ):
    
    #tw = self.emacs.getTabWidth()
    editor = self.emacs.editor
    txt = editor.getSelectedText()
    if txt == None: return True
    
    #space_replace = ' ' * tw
    ntxt = txt.replace( '\t', ' ' )
    pos = editor.getCaretPosition()
    editor.replaceSelection( ntxt )
    editor.setCaretPosition( pos )
    return True</t>
<t tx="zorcanda!.20050312123359">def getTabWidth( self ):
    
    return abs( self.c.tab_width )</t>
<t tx="zorcanda!.20050312155939">class registers:
        
    @others </t>
<t tx="zorcanda!.20050312160220">def copyToRegister (self):
 
    if not self.mode:
        self.mode = 1 # 'copy-to-register'
        self.emacs.minibuffer.setText("")
        self.emacs._stateManager.setState("registers")
        self.emacs.setCommandText("Copy To Which Register( a-z )?")
        return True 

    register = self.emacs.minibuffer.getText()
    self.emacs.minibuffer.setText("")
    if not java.lang.Character.isLetter(register):
        return 'Character is not a Letter'

    register = register.lower()
    txt = self.emacs.editor.getSelectedText()
    if txt==None:
        return 'Region not defined'

    self.registers [register] = txt
    self.emacs.editor.setCaretPosition(self.emacs.editor.getCaretPosition())</t>
<t tx="zorcanda!.20050312160220.1">def insertRegister (self):
 
    if self.mode == None:
        self.mode = 2
        self.emacs.minibuffer.setText("")
        self.emacs._stateManager.setState("registers")
        self.emacs.setCommandText("Insert From Which Register( a-z )?")
        return True 

    register = self.emacs.minibuffer.getText()
    if not java.lang.Character.isLetter(register):
        return 'Character is not a Letter'

    register = register.lower()
    if not self.registers.has_key(register):
        return 'Register %s empty'%register 

    data = self.registers[register]
    sdoc = self.emacs.editor.getStyledDocument()
    sdoc.insertString(self.emacs.editor.getCaretPosition(),data,None)</t>
<t tx="zorcanda!.20050312171820">def appendToRegister (self):

    if self.mode == None:
        self.mode = 3
        self.emacs.minibuffer.setText("")
        self.emacs._stateManager.setState("registers")
        self.emacs.setCommandText("Append To Which Register(a-z)?")
        return True 

    register = self.emacs.minibuffer.getText()
    self.emacs.minibuffer.setText("")
    if not java.lang.Character.isLetter(register):
        return 'Character is not a Letter'
        
    register = register.lower()
    txt = self.emacs.editor.getSelectedText()
    if txt==None:
        return 'Region not defined'
        
    if self.registers.has_key(register):
        data = self.registers[register]
        ndata = '%s%s'%(data,txt)
        self.registers[register] = ndata 
    else:
        self.registers[register] = txt 
        
    self.emacs.editor.setCaretPosition(self.emacs.editor.getCaretPosition())</t>
<t tx="zorcanda!.20050312171820.1">def prependToRegister (self):

    if self.mode == None:
        self.mode = 4
        self.emacs.minibuffer.setText("")
        self.emacs._stateManager.setState("registers")
        self.emacs.setCommandText("Prepend To Which Register(a-z)?")
        return True 
        
    register = self.emacs.minibuffer.getText()
    self.emacs.minibuffer.setText("")
    if not java.lang.Character.isLetter(register):
        return 'Character is not a Letter'
        
    register = register.lower()
    txt = self.emacs.editor.getSelectedText()
    if txt==None:
        return 'Region not defined'
        
    if self.registers.has_key(register):
        data = self.registers[register]
        ndata = '%s%s'%(txt,data)
        self.registers[register] = ndata 
    else:
        self.registers[register] = txt 
        
    self.emacs.editor.setCaretPosition(self.emacs.editor.getCaretPosition())</t>
<t tx="zorcanda!.20050312173225">def indentRelative( self ):

    editor = self.emacs.editor
    sd = editor.getStyledDocument()
    pos = editor.getCaretPosition()
    
    txt = editor.getText()
    
    
    plstart, plend = self.definePreviousLine()
    
    if plstart == -1 or plend == -1:
        sd.insertString( pos, '\t', None )
        return True         
       

    ltxt = txt[ plstart: plend ]

    
    find = txt.rfind( '\n', 0, pos )
    find += 1
    rlpos = pos - find
    
    if rlpos &gt; ( len( ltxt ) -1 ):
        sd.insertString( pos, '\t', None )
        return True
        
    addon = []
    for z in ltxt[ : rlpos ]:
        if z.isspace():
            addon.append( z )
        else:
            addon.append( ' ' )
            
    add = ''.join( addon )
    
    if ltxt[ rlpos ].isspace():
        addon = []
        for z in ltxt[ rlpos: ]:
            if z.isspace():
                addon.append( z )
            else:
                break
        add = add + ''.join( addon )
    else:
        addon = []
        for z in ltxt[ rlpos: ]:
            if z.isspace(): break
            else:
                addon.append( ' ' )
        
        add = add + ''.join( addon )
        rlpos += len( addon )
        addon = []
        for z in ltxt[ rlpos: ]:
            if z.isspace():
                addon.append( z )
            else:
                break
        add = add + ''.join( addon )
    if txt[ find: pos ].isspace():               
        sd.replace( find, pos - find, '' , None )
        sd.insertString( find, add, None )
    else:
        atext = txt[ find: pos ]
        atext = atext.rstrip()
        atext = atext + add[ len( atext ) -1 : ]
        sd.replace( find, pos - find, '', None )
        sd.insertString( find, atext, None )
         
    return True</t>
<t tx="zorcanda!.20050312183416">def definePreviousLine( self ):
    
    editor = self.emacs.editor
    pos = editor.getCaretPosition()
    
    txt = editor.getText()
    find = txt.rfind( '\n', 0, pos )
    if find == -1:
        return -1, -1
    else:
        find2 = txt.rfind( '\n', 0, find )
        if ( find2 - 1 ) == find:
            return -1, -1
        elif find2 == -1:
            find2 = 0
        else:
            find2 += 1    

    return find2, find</t>
<t tx="zorcanda!.20050313115453">def addCommand(  name, command ):
    commandsFromPlugins[ name ] = command</t>
<t tx="zorcanda!.20050313142453">def lookForExtensions( self ):

    import sys    
    path,file = g.os_path_split(g.app.loadDir)
    try:    
        tlevel = java.io.File( path )
        directories = tlevel.listFiles()
        exts = []
        for z in directories:
            if z.isDirectory() and z.getName() == 'swingmacs_exts':
            
                sys.path.append( z.getAbsolutePath() )
                files = z.listFiles()
                for z1 in files:
                    if z1.isFile() and z1.getName().endswith( '.py' ):
                        exts.append( z1 ) 
                break
    finally: pass
            
    mods = []
    for z in exts:
        try:
            name = z.getName()
            name = name[ : -3 ]
            mod = __import__( name )
            mods.append( mod )
        finally: pass
            
    return mods</t>
<t tx="zorcanda!.20050314142845">@
An extension is defined like so:
1. a function called:
    getCommands()
returns a dictionary of command names and command classes, an example:
    return {  "j-library": JLibrary_Loc }
this in turn causes an instance of the command class to be instatiated.
Instantiation involves passing the emacs instance to the command via
the costructor

    returned_dict[ "akey" ]( self )   #self is the emacs instance

the instance is then asked for new commands via a call to its 'addToAltX' method,
which returns a list of commands:
    return [ 'zoom-to-home', 'release-window' ]
after this the command is queried to see if it has an 'addToKeyStrokes' method.  If so
it is called.  This is to return keystrokes that activate the command:
    return [ 'Ctrl W', ]
all commands and keystrokes that are bound to the command object result in a call to
its __call__ method which should be defined like so:
    def __call__( self, event, command ):
        ....code....</t>
<t tx="zorcanda!.20050411132747">def addCompleter (self,ch,ch2):
    self.completers [ch] = ch2

def addTabForColon (self,torf):
    self.tab_for_colon = torf</t>
<t tx="zorcanda!.20050411132825">def addCompleter( self, ch, ch2 ):
    self.kcb.addCompleter( ch, ch2 )
    
def addTabForColon( self, torf ):
    self.kcb.addTabForColon( torf )</t>
<t tx="zorcanda!.20050417172712">def addCommands( self, command, commands ):
    
    xcommand = self.strategyObjects[ 'xcommand' ]

    for z in commands:
        xcommand.commands[ z ] = command
        xcommand.keys.append( z )

    self.strategyObjects[ command.getName() ] = command</t>
<t tx="zorcanda!.20050418121158">def addCommandHelp( self, chelp ):

    self.command_help.append( chelp )
    
def addKeyStrokeHelp( self, kshelp ):
    
    self.keystroke_help.append( kshelp )</t>
<t tx="zorcanda!.20050512112449">def startOfWord( self):
    
    doc = self.emacs.editor.getDocument()
    cpos = self.emacs.editor.getCaretPosition()
    txt = doc.getText( 0, cpos )
    txt = list( txt)
    txt.reverse()
    if len( txt) == 0: return
    i = 0
    if not self.isWordCharacter( txt[ 0 ]):
        for z in txt:
            if not self.isWordCharacter( z ):
                i += 1
            else:
                break
    
    for z in txt[ i: ]:
        if not self.isWordCharacter( z ):
            break
        else:
            i += 1

    cpos -= i
    self.emacs.editor.setCaretPosition( cpos )</t>
<t tx="zorcanda!.20050512112449.1">def endOfWord( self ):
    
    doc = self.emacs.editor.getDocument()
    cpos = self.emacs.editor.getCaretPosition()
    txt = doc.getText( cpos, doc.getLength() - cpos )
    txt = list( txt)
    #txt.reverse()
    if len( txt) == 0: return
    i = 0
    if not self.isWordCharacter( txt[ 0 ]):
        for z in txt:
            if not self.isWordCharacter( z ):
                i += 1
            else:
                break
    
    for z in txt[ i: ]:
        if not self.isWordCharacter( z ):
            break
        else:
            i += 1

    cpos += i
    self.emacs.editor.setCaretPosition( cpos )</t>
<t tx="zorcanda!.20050512113820">def isWordCharacter( self, c ):
    
    if c in string.ascii_letters:
        return True
    elif c in string.digits:
        return True
    elif c in ( "_"):
        return True
    return False</t>
<t tx="zorcanda!.20050519094216">class selection( sevent.DocumentListener ):

    def __init__( self, emacs ):
        self.emacs = emacs
        self.emacs.editor.getDocument().addDocumentListener( self )
        self.start = None
        self.commands = {
            "Ctrl Space": self.startSelection,       
        }
        
    def __call__( self, event, command ):
        if self.commands.has_key( command ):
            return self.commands[ command ]()
        elif self.emacs._stateManager2.hasState() == "selection":
            self.select()
        
    def startSelection( self ):
        self.start = self.emacs.editor.getCaretPosition()
        self.emacs._stateManager2.setState( "selection" )
        return True
    
    def executeSelection( self ):
        if self.start != -1:
            editor = self.emacs.editor
            cp = editor.getCaretPosition()
            editor.setCaretPosition( self.start )
            editor.moveCaretPosition( cp )
        else:
            self.emacs.keyboardQuit()    

    def select( self ):
        dc = DefCallable( self.executeSelection )
        ft = dc.wrappedAsFutureTask()
        java.awt.EventQueue.invokeLater( ft )
        
    def changedUpdate( self, event ):
        pass
        
    def insertUpdate( self, event ):
        pass
        
    def removeUpdate( self, event ):
        self.start = -1</t>
<t tx="zorcanda!.20050520221746">class TagMatcher(aevent.KeyAdapter):

    '''A class to match html/xml style tags.'''

    def __init__ (self,emacs):

        aevent.KeyAdapter.__init__(self)
        self.emacs = emacs
        self.configureMatching()
        g.app.config.manager.addNotificationDef("complete_tags",self.configureMatching)

    def configureMatching (self,notification=None,handback=None):

        self.on = g.app.config.getBool(self.emacs.c,"complete_tags")</t>
<t tx="zorcanda!.20050522115325">def calculateExtraSpaces (self,line):

    endsWithColon = False
    hasUncompleteBracket = False

    count1 = 0
    for z in line:
        if z == '[': count += 1
        elif z == ']': count -= 1

    count2 = 0 ; last2 = None ; ll = len(line) -1
    while ll &gt;= 0:
        char = line [ll]
        if char == '(':
            count2 += 1 ; last2 = ll
        elif char == ')':
            count2 -= 1
        ll -= 1

    if count2 &gt; 0:
        nwline = line [:last2]
        ws = [g.choose(z.isspace(),z,' ')for z in nwline]
        print "WS len is %s" % len(ws)
        return ''.join(ws)

    return ''</t>
<t tx="zorcanda!.20050523135303">def moveToIndentStart( self ):

    editor = self.emacs.editor
    pos = editor.getCaretPosition()
    if pos != -1:
        
        #txt = editor.getText()
        start = stext.Utilities.getRowStart( editor, pos )
        end = stext.Utilities.getRowEnd( editor, pos )
        doc = editor.getDocument()
        txt = doc.getText( start, end - start )
        add = 0
        for z in txt:
            if not z.isspace():
                break
            else:
                add +=1
                        
        editor.setCaretPosition( start + add )</t>
<t tx="zorcanda!.20050523140526">def deleteSurroundingSpaces( self ):
    
    editor = self.emacs.editor
    pos = editor.getCaretPosition()    
    if pos != -1:
        
        start = stext.Utilities.getRowStart( editor, pos )
        end = stext.Utilities.getRowEnd( editor, pos )
        doc = editor.getDocument()
        txt = doc.getText( start, end - start )
        rpos = pos - start
        part1 = txt[ : rpos ]
        part1 = part1.rstrip()
        part2 = txt[ rpos: ]
        part2 = part2.lstrip()
        doc.replace( start, end - start, "%s%s" %( part1, part2 ), None )
        editor.setCaretPosition( start + len( part1 ) )</t>
<t tx="zorcanda!.20050523141645">def joinLineToPrevious( self ):
    
    plstart, plend = self.definePreviousLine()
    if plstart == -1 or plend == -1:
        return
        
    editor = self.emacs.editor
    pos = editor.getCaretPosition() 
    if pos != -1:
        
        doc = editor.getDocument()
        start = stext.Utilities.getRowStart( editor, pos )
        end = stext.Utilities.getRowEnd( editor, pos )
        txt = doc.getText( start, end - start )
        txt = ' %s' % txt.lstrip()
        doc.remove( start, end - start )
        doc.insertString( plend, txt, None )
        editor.setCaretPosition( plend )</t>
<t tx="zorcanda!.20050523143029">class ctrl_x_handler:
    
    def __init__( self, emacs ):
        self.emacs = emacs
        self.defineCommands()
        self.last_command = None
        self.keys = []
        
    def defineCommands( self ):
        
        sO = self.emacs.strategyObjects
        self.commands = {
        
            'Ctrl O': sO[ 'formatter' ],
            
            
            }
        
    def __call__( self, event, command ):
        
        if command == 'Ctrl X':
            #self.tbCompleter.reset()
            self.last_command = None
            self.emacs._stateManager.setState( 'ctrlx' ) 
            self.emacs.setCommandText( "Ctrl-x:" )
            return True
            
        if command in self.commands:
            return self.commands[ command ]( event, command )</t>
<t tx="zorcanda!.20050523143816">def deleteBlankLines( self ):

    editor = self.emacs.editor
    pos = editor.getCaretPosition()
    if pos != -1:
        
        doc = editor.getDocument()
        start = stext.Utilities.getRowStart( editor, pos )
        end = stext.Utilities.getRowEnd( editor, pos )
        txt = doc.getText( 0, doc.getLength() )
        cline = txt[ start: end ] + '\n'
        
        first = txt[ : start ]
        lines = first.splitlines( 1 )
        lines.reverse()
        #line = lines[ 0 ]
        #del lines[ 0 ]
        #line = lines.pop()
        cpos_minus = 0
        if cline.isspace():
            for z in xrange( len( lines )):
                if lines[ 0 ].isspace() or lines[ 0 ] == "":                    
                    cpos_minus += len( lines[ 0 ] )
                    del lines[ 0 ]
                else:
                    break
        lines.reverse()
        #lines.append( line )
        
        
        end = txt[ end: ]
        lines2 = end.splitlines( 1 )
        #line = lines2[ 0 ]
        #del lines2[ 0 ]
        for z in xrange( len( lines2 ) ):
            if lines2[ 0 ].isspace() or lines2[ 0 ] == "":
                #lines2.pop()
                del lines2[ 0 ]
            else:
                break
        #lines2.insert( 0, line )
        fpart = ''.join( lines )
        spart = ''.join( lines2 )
        nwtext = '%s%s%s' %( fpart, cline, spart )
        doc.replace( 0, doc.getLength(), nwtext, None )
        editor.setCaretPosition( pos - cpos_minus )
        return True</t>
<t tx="zorcanda!.20050524093817">def transposeWords( self ):
    
    editor = self.emacs.editor
    pos = editor.getCaretPosition()
    if pos != -1:
        
        ranges = self.emacs.getAttributeRanges( "trans-word" )
        if ranges:
            start = self.emacs.getWordStartIndex()
            end = self.emacs.getWordEndIndex()
            doc = editor.getDocument()
            w1 = doc.getText( start, end - start )
            w2 = doc.getText( ranges[ 0 ], ranges[ -1 ] - ranges[ 0 ] )
            doc.replace( ranges[ 0 ], ranges[ -1 ] - ranges[ 0 ], w1, None )
            start = self.emacs.getWordStartIndex()
            end = self.emacs.getWordEndIndex()
            doc.replace( start, end - start, w2, None )
            self.emacs.clearAttribute( "trans-word" )
            return
        
        else:
            start = self.emacs.getWordStartIndex()
            end = self.emacs.getWordEndIndex()
            self.emacs.addAttributeToRange( 'trans-word', "trans-word" , start, end-start, color = java.awt.Color.YELLOW )

        return True</t>
<t tx="zorcanda!.20050527190231">class symbolcompletion:
    
    def __init__( self, emacs ):
        self.emacs = emacs
        self.start = -1
        self.end = -1
        self.segment = None
        self.commands = {
            
            "Ctrl+Alt I" : self.complete
        
        
        }
        
        import leoColor
        c_dict = dir( leoColor.baseColorizer )
        self.languages = {}
        for z in c_dict:
            if z.endswith( '_keywords' ):
                language = z.rstrip( '_keywords' )
                self.languages[ language ] = getattr( leoColor.baseColorizer, z )
        
        
    def __call__( self, event, command ):

        self.commands[ command ]()
        return True
        
        
    def complete( self ):
        
        language = self.emacs.determineLanguage()
        if language == None or language not in self.languages:
            m = self.languages[ 'python' ]
        else:
            m = self.languages[ language ]
    
        editor = self.emacs.editor
        doc = editor.getDocument()
        cp = editor.getCaretPosition()
        word = self.emacs.getWordStart()
        if not word:
            self.start = self.end = -1; self.segment = None
            return
        lastword = word
        if self.start != -1:

            if self.start == cp - len( word ):
                word2 = doc.getText( self.start, self.end - self.start )
                if word2 == self.segment:
                    word = word2
                    doc.replace( cp - len( lastword ), len( lastword ), word, None )
                    cp = editor.getCaretPosition()
            
        self.start = self.end = -1; self.segment = None
        if word:
            words = []
            for z in m:
                if z.startswith( word ):
                    words.append( z )
                
            if not words: return
            if lastword in m:
                spot = words.index( lastword )
    
                if spot == 0 and len( words ) == 1:
                    pass 
                elif spot + 1 == len( words ):
                    spot = 0
                else:
                    spot += 1
                  
                nword = words[ spot ]
            else:
                nword = words[ 0 ]
            
            doc.replace( cp - len( word ), len( word ), nword, None )
            self.start = cp - len( word )
            self.end = cp
            self.segment = word</t>
<t tx="zorcanda!.20050528093036">class balanced_parentheses:
    
    def __init__( self, emacs ):
        self.emacs = emacs
        self.sexps = {
        
            '(': ')',
            ')':'(',
            '[':']',
            ']':'[',
            '&lt;':'&gt;',
            '&gt;':'&lt;',
            '{':'}',
            '}':'{',
        }
        
        self.forwards = ( "(", "&lt;", "{", "[" )
        self.backwards = ( ")", "&gt;", "}", "]" )
        
        self.commands = {
            'Ctrl+Alt F': self.forwardSexp,
            'Ctrl+Alt B': self.backwardSexp,
            'Ctrl+Alt K': self.killSexpForward,
            'Ctrl+Alt Delete': self.killSexpBackward,
        }
        
    def __call__( self, event , command ):
        
        self.commands[ command ]()
        return True

    def forwardSexp( self ):
        
        editor = self.emacs.editor
        doc = editor.getDocument()
        cp = editor.getCaretPosition()
        if cp + 1 == doc.getLength(): return
        txt = doc.getText( cp, doc.getLength() - cp )
        sp = txt[ 0 ]
        if sp not in self.forwards or len( txt ) == 1: return
        matcher = self.sexps[ sp ]
        i = 1
        i2 = 0
        for z in txt[ 1: ]:
            i2 += 1
            if z == sp:
                i += 1
                continue
            elif z == matcher:
                i -= 1
            if i == 0: break
        if i == 0:
            editor.setCaretPosition( cp + i2 )
    
    def backwardSexp( self ):
        
        editor = self.emacs.editor
        doc = editor.getDocument()
        cp = editor.getCaretPosition()
        txt = doc.getText( 0, cp + 1 )
        sexp = txt[ -1 ]
        if sexp not in self.backwards or len( txt ) == 1: return
        matcher = self.sexps[ sexp ]
        i = 1
        i2 = 0
        t2 = list( txt )
        t2.reverse()
        for z in t2[ 1: ]:
            i2 += 1
            if z == sexp:
                i += 1
                continue
            elif z == matcher:
                i -= 1
            if i == 0:
                break
        
        if i == 0:
            editor.setCaretPosition( cp - i2 )
 
    @others</t>
<t tx="zorcanda!.20050528100638">def killSexpForward( self ):
    
    editor = self.emacs.editor
    doc = editor.getDocument()
    cp = editor.getCaretPosition()
    self.forwardSexp()
    cp2 = editor.getCaretPosition()
    if cp != cp2:
        txt = doc.getText( cp, ( cp2 - cp ) + 1 )
        self.emacs.addToKillbuffer( txt )
        doc.remove( cp, ( cp2 - cp ) + 1)
        
def killSexpBackward( self ):
    
    editor = self.emacs.editor
    doc = editor.getDocument()
    cp = editor.getCaretPosition()
    self.backwardSexp()
    cp2 = editor.getCaretPosition()
    if cp != cp2:
        txt = doc.getText( cp2, ( cp - cp2 ) + 1)
        self.emacs.addToKillbuffer( txt )
        doc.remove( cp2, ( cp - cp2 ) + 1)</t>
<t tx="zorcanda!.20050528101434">def addToKillbuffer( self, text ):
    
    self.strategyObjects[ 'killbuffer' ].insertIntoKillbuffer( text )</t>
<t tx="zorcanda!.20050528154411">class tags( java.lang.Runnable ):
    
    #tags_table = {}
    
    def __init__( self, emacs ):
        
        self.emacs = emacs
        #self.emacs.c.frame.tree.jtree.addTreeSelectionListener( self )
        self.last_tag = None
        self.pop_back = []
        self.positions = []
        self.tag_table = {}
        self.last_command = None
        self.__defineLanguageRecognizers()
        self.__defineLanguageMatchers()
        self.xs = java.util.concurrent.Executors.newSingleThreadScheduledExecutor()
        import leoPlugins
        leoPlugins.registerHandler( "select1", self.valueChanged )
        self.mode = None
        emacs.modeStrategies.append( self )
        self.commands = {
            'Alt Period': self.gotoTag,
            'Ctrl U Alt Period': self.alternativeDefinition,
            'Alt+Shift 8': self.popBack,
        
        }
        self.tab_completer = self.emacs.TabCompleter( [] )
        dc = DefCallable( self.defineTagsTable )
        g.app.gui.addStartupTask( dc )
    
    def __defineLanguageMatchers( self ):
        
        reg1 = java.util.regex.Pattern.compile( java.lang.String( "^\s*(def\s+\w+\s*)" ) )
        reg2 = java.util.regex.Pattern.compile( java.lang.String(  "^\s*(class\s+\w+\s*)" ) )
        self.python_matchers = ( reg1.matcher( java.lang.String( "" ) ), reg2.matcher( java.lang.String( "" ) ) )
        
    
    def __call__( self, event, command ):
        
        if self.mode:
            if command == 'Enter':
                self.gotoTag()
                return self.emacs.keyboardQuit( event )
            elif command == 'Tab':
            
                txt = self.emacs.minibuffer.getText()
                if self.last_command == None or not txt.startswith( self.last_command ):
                    txt = self.emacs.minibuffer.getText()                
                    fnd = self.tab_completer.lookFor( txt )
                    if fnd:
                        self.last_command = txt
                        self.emacs.minibuffer.setText( self.tab_completer.getNext() )
                else :
                    self.emacs.minibuffer.setText( self.tab_completer.getNext() )
                return True
            else:
                return self.emacs.eventToMinibuffer( event )   
        
        rv = self.commands[ command ]()
        self.tab_completer.reset()
        self.last_command = None
        if rv:
            self.emacs.keyboardQuit( event )
        return True
        
        
    @others</t>
<t tx="zorcanda!.20050528154411.1">def gotoTag( self ):
    
    if self.mode == None:
        self.emacs.setCommandText( "Goto tag:" )
        self.emacs.minibuffer.setText( "" )
        self.emacs._stateManager.setState( "tags" )    
        self.mode = 1
        return
        
    if self.mode == 1:
        
        tag = self.emacs.minibuffer.getText()
        if not tag:
            wsi = self.emacs.getWordStartIndex()
            wse = self.emacs.getWordEndIndex()
            tag = self.emacs.getTextSlice( wsi, wse )
        if tag in self.tag_table:
            td = self.tag_table[ tag ]
            self.last_tag = ( tag, td[ 0 ] )
            p = td[ 0 ][ -1 ]
            c = self.emacs.c
            cp = c.currentPosition()
            self.pop_back.append( cp.copy() )
            c.beginUpdate()
            c.selectPosition( p.copy() )
            c.endUpdate()
            dgl = self.DeferedGotoLine( self.emacs.c, p, td[ 0 ][ 0 ] )
            dc = DefCallable( dgl )
            ft = dc.wrappedAsFutureTask()
            java.awt.EventQueue.invokeLater( ft )
            #self.emacs.keyboardQuit( event )
            return True
        else:
            g.es( "Could not find definition for %s" % tag )
            #self.emacs.keyboardQuit( event)
            return True</t>
<t tx="zorcanda!.20050528154425">def defineTagsTable( self ):

    c = self.emacs.c
    cp = c.rootPosition()
    for z in cp.allNodes_iter( copy = True ):
        tags = self.scanForTags( z )
        if tags:
            for x in tags:
                if self.tag_table.has_key( x[ 1 ] ):
                    self.tag_table[ x[ 1 ] ].append( x )
                else:                    
                    self.tag_table[ x[ 1 ] ] = []
                    self.tag_table[ x[ 1 ] ].append( x )
                    
    self.tab_completer.extend( self.tag_table.keys() ) 
    g.es( "tag table built" )
    self.xs.scheduleAtFixedRate( self, 30000, 30000, java.util.concurrent.TimeUnit.MILLISECONDS )</t>
<t tx="zorcanda!.20050528154749">def scanForTags( self, p ):
    #print "SCANNING FOR TAGS!"
    #language = g.scanForAtLanguage( self.emacs.c, p )
    language = LeoUtilities.scanForLanguage( p )
    if language == None: language = 'python'
    if language == 'python':
        tags = []
        try:
            #reg1 = "^\s*(def\s+\w+\s*)"
            #reg2 = "^\s*(class\s+\w+\s*)"
            #regs = ( reg1, reg2 )
            tnt = p.v.t._bodyString
            matches = LeoUtilities.scanFor( self.python_matchers , tnt )
            #print matches
            for z in matches:
                tags.append( ( z[ 0 ], z[ 1 ], p ) )
            #bs = p.bodyString()
            #data = bs.split( '\n' )
            # tags = []
            #for z in data:
            #    txt = z.lstrip()
            #    txtpieces = txt.split()
            #    if len( txtpieces )&gt; 1 and txtpieces[ 0 ] in ( "class", "def" ):
            #        ntxt = txtpieces[ 1 ]
            #        i1 = ntxt.find( "(" )
            #        i2 = ntxt.find( ":" )
            #        if i1 != -1: 
            #            ntxt = ntxt[ : i1 ]
            #        elif i2 != -1:
            #            ntxt = ntxt[ : i2 ]
            #        
            #        tags.append( ( txt, ntxt, p ) )
        except Exception, x:
            print x
        except java.lang.Exception, r:
            print r            
             
        return tags
    elif language == 'java':
        &lt;&lt;java&gt;&gt;
    else:
        return None</t>
<t tx="zorcanda!.20050528154749.1">def valueChanged( self, *args ):
    
    values = args[ 1 ]
    self.positions.append( values[ 'new_p' ].copy() )</t>
<t tx="zorcanda!.20050528155247">def run( self ):
    
    cp = self.emacs.c.currentPosition().copy()
    if cp not in self.positions:
        self.positions.append( cp )
        
    for z in self.positions:
        tags = self.scanForTags( z )
        if tags:
            for x in tags:   
                if self.tag_table.has_key( x[ 1 ] ):
                    self.tag_table[ x[ 1 ] ].append( x ) 
                else:
                    self.tag_table[ x[ 1 ] ] = []
                    self.tag_table[ x[ 1 ] ].append( x )
                self.tab_completer.extend( x[ 1 ] )
                    
    self.positions = []</t>
<t tx="zorcanda!.20050528185814">class DeferedGotoLine:
    
    def __init__( self, c, pos, tag ):
        self.c = c
        self.pos = pos
        self.tag = tag
        
    def __call__( self ):
        
        bs = self.pos.bodyString()
        where = bs.find( self.tag )
        if where != -1:
            self.c.frame.body.editor.editor.setCaretPosition( where )</t>
<t tx="zorcanda!.20050528193454">class ctrl_u_handler:
    
    def __init__( self, emacs ):
        self.emacs = emacs
        self.defineCommands()
        self.last_command = None
        self.keys = []
        
    def defineCommands( self ):
        
        sO = self.emacs.strategyObjects
        self.commands = {
        
            'Alt Period': sO[ 'tags' ],
            
            
            }
        
    def __call__( self, event, command ):
        
        if command == 'Ctrl U':
            #self.tbCompleter.reset()
            self.last_command = None
            self.emacs._stateManager.setState( 'ctrlu' ) 
            self.emacs.setCommandText( "Ctrl-u:" )
            return True
            
        if command in self.commands:
            return self.commands[ command ]( event, "Ctrl U %s" % command )</t>
<t tx="zorcanda!.20050528193932">def alternativeDefinition( self ):
    
    if self.last_tag:
        
        tag , td = self.last_tag
        tags = self.tag_table[ tag ]
        i = tags.index( td )
        if i + 1 == len( tags ):
            i = 0
        else:
            i += 1
        
        td = tags[ i ]
        self.last_tag = ( tag, td )
        p = td[ -1 ]
        c = self.emacs.c
        cp = c.currentPosition()
        self.pop_back.append( cp.copy() )
        c.beginUpdate()
        c.selectPosition( p.copy() )
        c.endUpdate()
        dgl = self.DeferedGotoLine( self.emacs.c, p, td[ 0 ] )
        dc = DefCallable( dgl )
        ft = dc.wrappedAsFutureTask()
        java.awt.EventQueue.invokeLater( ft )
        #self.emacs.keyboardQuit( event )
        return True</t>
<t tx="zorcanda!.20050531101443">def popBack( self ):

    if self.pop_back:
        p = self.pop_back.pop()
        c = self.emacs.c
        c.beginUpdate()
        c.selectPosition( p )
        c.endUpdate()</t>
<t tx="zorcanda!.20050531112641">bs = p.bodyString()
data = bs.split( '\n' )
tags = []
for z in data:
    #regex looking for methods
    #regular scan for looking for class and interface
    #class interface takes precedence over methods
    try:
        stxt = z.lstrip()
        txt = java.lang.String( stxt )
        self.java_class.reset( txt )
        self.java_method.reset( txt )
        start = end = -1
        if self.java_class.find():
            gc = self.java_class.groupCount()
            ntxt = self.java_class.group( gc )
        elif self.java_method.find():
            gc = self.java_method.groupCount()
            ntxt = self.java_method.group( gc )
        else:
            gc = 0
        
        if gc:
            tags.append( (stxt, ntxt, p ) ) 
    except Exception, x:
        print x


return tags</t>
<t tx="zorcanda!.20050531130856">def __defineLanguageRecognizers( self ):
    
    sstring = java.lang.String( "" )
    pattern = regex.Pattern.compile( "(class|interface)\s*(\w+)" )
    self.java_class = pattern.matcher( sstring )
    pattern = regex.Pattern.compile( "((public|private|protected)\s+)?(final\s+)?(static\s+)?(new\s+){0}\w+\s*(\w+)\s*\\(" )
    self.java_method = pattern.matcher( sstring )</t>
<t tx="zorcanda!.20050604091242">@others</t>
<t tx="zorcanda!.20050604091242.1">def addCompleters( self ):
    
    manager = g.app.config.manager
    manager.addNotificationDef( "complete-&lt;", self.managementListener )
    manager.addNotificationDef( "complete-(", self.managementListener )
    manager.addNotificationDef( "complete-[", self.managementListener )
    manager.addNotificationDef( "complete-{", self.managementListener )
    manager.addNotificationDef( "complete-'", self.managementListener )
    manager.addNotificationDef( 'complete-"', self.managementListener )

@
    if config.getBool( self.c, "complete-&lt;" ):
        self.swingmacs.addCompleter( "&lt;", "&gt;" )
    if config.getBool( self.c, "complete-(" ):
        self.swingmacs.addCompleter( "(", ")" )
    if config.getBool( self.c, "complete-[" ):
        self.swingmacs.addCompleter( "[", "]" )
    if config.getBool( self.c, "complete-{"):
        self.swingmacs.addCompleter( "{", "}" )
    if config.getBool( self.c, "complete-'" ):
        self.swingmacs.addCompleter( "'", "'" )
    if config.getBool( self.c, 'complete-"' ):
        self.swingmacs.addCompleter( '"', '"' )
    if config.getBool( self.c, "add_tab_for-:" ):
        self.swingmacs.addTabForColon( True )</t>
<t tx="zorcanda!.20050604091242.2">def managementListener( self, notification= None, handback = None ):
    
    source = notification.getSource().toString()
    source = source.lstrip( "MBean:name=" )
    use = g.app.config.getBool( self.c, source )
    completer = source[ -1 ]
    if use:
        completions = {
            '(': ')',
            '{': '}',
            '&lt;': '&gt;',
            '[':']',
            '"': '"',
            "'" : "'",        
        }
        self.kcb.addCompleter( completer, completions[ completer ] )
    else:
        self.kcb.removeCompleter( completer )</t>
<t tx="zorcanda!.20050604091924">def removeCompleter (self,ch):

    del self.completers [ch]</t>
<t tx="zorcanda!.20050704092406.1">class vi_emulation:
    
    def __init__( self, c ):
        self.c = c
        self.mode = None
        &lt;&lt;define vi keystrokes&gt;&gt;
        
    def __call__( self, event, command ):

        if self.mode:
            return self.mode( event, command )
        else:
            return self.vi_keystrokes[ command ]( event, command )</t>
<t tx="zorcanda!.20050704092406.2">self.vi_keystrokes = {
    'dd': self.deleteLine,
    'i': self.insert,
}</t>
<t tx="zorcanda!.20050704092406.3">def cut( self, event ):
    pass</t>
<t tx="zorcanda!.20050704092406.4">def deleteLine( self, event, command ):
    pass</t>
<t tx="zorcanda!.20050704092406.5">def insert( self, event, command ):
    pass</t>
<t tx="zorcanda!.20050720141603">def createDynamicList( self ):
    
    c = self.emacs.c
    class _buildDynamicList:
        
        def __init__( self, c, da ):
            self.c = c
            self.da = da
            
        def __call__( self ):
            
            rp = self.c.rootPosition().copy()
            for z in rp.allNodes_iter( copy = 1 ):
                btx = z.bodyString()
                items = self.da.dynaregex.findall( btx )
                self.da.dynamiclist.addAll( items )

            g.es( "dynamic list built: dynamic abbreviations online" )
            
    
    dc = DefCallable( _buildDynamicList( c, self ) )
    self.emacs.c.frame.gui.addStartupTask( dc.wrappedAsFutureTask() )</t>
<t tx="zorcanda!.20050720215058">class deferedHighlight( java.lang.Runnable ):
    
    def __init__( self, source, pos, iway, highlight, length, emacs ):
        self.source = source
        self.pos = pos
        self.iway = iway
        self.highlight = highlight
        self.length = length
        self.emacs = emacs

    def run( self ):
        source = self.source; pos = self.pos
        source.setCaretPosition( pos )
        if self.iway == 'forward':
            start = pos - self.length
            self.emacs.addHighlight( start, start + self.length, self.highlight ) 
        else:
            self.emacs.addHighlight( pos, pos + self.length, self.highlight )
        tcursor = java.awt.Cursor.getPredefinedCursor( java.awt.Cursor.TEXT_CURSOR )
        source.setCursor( tcursor )</t>
</tnodes>
</leo_file>
