<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="1105" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="21" left="421" height="886" width="818"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences allow_rich_text="0">
</preferences>
<find_panel_settings>
	<find_string></find_string>
	<change_string></change_string>
</find_panel_settings>
<vnodes>
<v t="T1"><vh>Diary</vh>
<v t="T2"><vh>7/7/03 Created leoPlugins.leo</vh></v>
</v>
<v t="T3"><vh>Documentation and security warnings</vh>
<v t="T4"><vh>Overview of plugins and hooks</vh></v>
<v t="T5"><vh>Intro to scripts</vh></v>
<v t="T6"><vh>About hooks</vh></v>
<v t="T7"><vh>Hooks should never blindly Python scripts</vh></v>
<v t="T8"><vh>NEVER use this kind of code in a hook!!</vh></v>
</v>
<v t="T9"><vh>Plugins</vh>
<v t="T10" a="M"><vh> To do</vh>
<v t="T11"><vh>(Improve Spell Checking)</vh></v>
</v>
<v t="T12"><vh>Commands</vh>
<v t="T13"><vh> Importing Cisco configuration files</vh>
<v t="T14"><vh>@file import_cisco_config.py</vh>
<v t="T15"><vh>&lt;&lt; about this plugin &gt;&gt;</vh></v>
<v t="T16"><vh>create_import_cisco_menu</vh></v>
<v t="T17"><vh>importCiscoConfig</vh>
<v t="T18"><vh>&lt;&lt; open file &gt;&gt;</vh></v>
<v t="T19"><vh>&lt;&lt; process custom line &gt;&gt;</vh></v>
<v t="T20"><vh>&lt;&lt; process indented block &gt;&gt;</vh></v>
<v t="T21"><vh>&lt;&lt; complete outline &gt;&gt;</vh></v>
</v>
</v>
<v t="T22"><vh> Example of an imported config</vh>
<v t="T23"><vh>plain configuration</vh></v>
<v t="T24"><vh>cisco config: C:/Davide/Leo/CVS Version/example_conf.txt</vh>
<v t="T25"><vh>&lt;&lt;access-list&gt;&gt;</vh></v>
<v t="T26"><vh>&lt;&lt;boot&gt;&gt;</vh></v>
<v t="T27"><vh>&lt;&lt;controller&gt;&gt;</vh>
<v t="T28"><vh>controller E1 5/0/0</vh></v>
<v t="T29"><vh>controller E1 5/0/1</vh></v>
<v t="T30"><vh>controller SONET 1/0/0</vh></v>
</v>
<v t="T31"><vh>&lt;&lt;interface&gt;&gt;</vh>
<v t="T32"><vh>interface Async1</vh></v>
<v t="T33"><vh>interface Dialer0</vh></v>
<v t="T34"><vh>interface FastEthernet0/0/0</vh></v>
<v t="T35"><vh>interface FastEthernet0/0/1</vh></v>
<v t="T36"><vh>interface FastEthernet0/0/1.1</vh></v>
<v t="T37"><vh>interface FastEthernet0/0/1.2</vh></v>
<v t="T38"><vh>interface FastEthernet0/0/1.3</vh></v>
<v t="T39"><vh>interface FastEthernet0/0/1.5</vh></v>
<v t="T40"><vh>interface FastEthernet0/0/1.50</vh></v>
<v t="T41"><vh>interface Loopback0</vh></v>
<v t="T42"><vh>interface POS4/1/0</vh></v>
<v t="T43"><vh>interface Serial5/0/0:1</vh></v>
<v t="T44"><vh>interface Serial5/0/0:2</vh></v>
<v t="T45"><vh>interface Serial5/0/1:0</vh></v>
<v t="T46"><vh>interface Serial5/1/0</vh></v>
<v t="T47"><vh>interface Serial5/1/1</vh></v>
</v>
<v t="T48"><vh>&lt;&lt;ip community-list&gt;&gt;</vh></v>
<v t="T49"><vh>&lt;&lt;ip route&gt;&gt;</vh></v>
<v t="T50"><vh>&lt;&lt;line&gt;&gt;</vh>
<v t="T51"><vh>line aux 0</vh></v>
<v t="T52"><vh>line vty 0 4</vh></v>
</v>
<v t="T53"><vh>&lt;&lt;logging&gt;&gt;</vh></v>
<v t="T54"><vh>&lt;&lt;ntp&gt;&gt;</vh></v>
<v t="T55"><vh>&lt;&lt;route-map&gt;&gt;</vh>
<v t="T56"><vh>route-map only permit 2</vh></v>
<v t="T57"><vh>route-map only1 permit 10</vh></v>
<v t="T58"><vh>route-map only3 permit 10</vh></v>
<v t="T59"><vh>route-map tag_com permit 10</vh></v>
<v t="T60"><vh>route-map tag_com permit 20</vh></v>
</v>
<v t="T61"><vh>&lt;&lt;router&gt;&gt;</vh>
<v t="T62"><vh>router bgp 65001</vh></v>
<v t="T63"><vh>router ospf 1</vh></v>
</v>
<v t="T64"><vh>&lt;&lt;service&gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="T65"><vh>@file outline_export.py</vh>
<v t="T66"><vh>newMoreHead</vh></v>
</v>
</v>
<v t="T67"><vh>Debugging</vh>
<v t="T68"><vh>@file dump_globals.py</vh>
<v t="T69"><vh>onStart</vh></v>
</v>
<v t="T70"><vh>@file enable_gc.py</vh>
<v t="T71"><vh>onStart</vh></v>
</v>
<v t="T72"><vh>@file trace_gc.py</vh></v>
<v t="T73"><vh>@file trace_keys.py</vh>
<v t="T74"><vh>onKey</vh></v>
</v>
<v t="T75"><vh>@file trace_tags.py</vh>
<v t="T76"><vh>trace_tags</vh></v>
</v>
</v>
<v t="T77"><vh>Directives</vh>
<v t="T78"><vh>@file add_directives.py</vh>
<v t="T79"><vh>addPluginDirectives</vh></v>
<v t="T80"><vh>scanPluginDirectives</vh></v>
</v>
</v>
<v t="T81"><vh>Drawing, graphics &amp; styled text</vh>
<v t="T82"><vh>@file color_markup.py</vh>
<v t="T83"><vh>initAnyMarkup</vh></v>
<v t="T84"><vh>colorWikiMarkup</vh></v>
<v t="T85"><vh>doWikiText</vh>
<v t="T86"><vh>&lt;&lt; set first to a tuple describing the first tag to be handled &gt;&gt;</vh></v>
<v t="T87"><vh>&lt;&lt; handle the tag using n1,n2,delim1,delim2 &gt;&gt;</vh>
<v t="T88"><vh>&lt;&lt; parse and handle color field &gt;&gt;</vh></v>
</v>
</v>
<v t="T89"><vh>insertWikiPicture</vh></v>
</v>
<v t="T90"><vh>@file image.py</vh>
<v t="T91"><vh>onSelect</vh>
<v t="T92"><vh>&lt;&lt; Select Image &gt;&gt;</vh></v>
</v>
<v t="T93"><vh>onUnselect</vh>
<v t="T94"><vh>&lt;&lt; Unselect Image &gt;&gt;</vh></v>
</v>
</v>
<v t="T95"><vh>@file nav_buttons.py</vh>
<v t="T96"><vh>class commanderInfoClass</vh>
<v t="T97"><vh>__init__ (commanderInfoClass)</vh></v>
<v t="T98"><vh>addWidgets</vh>
<v t="T99"><vh>&lt;&lt; define callbacks &gt;&gt;</vh></v>
</v>
<v t="T100"><vh>createImage</vh></v>
<v t="T101"><vh>updateNavButtons (nav_buttons.py)</vh></v>
<v t="T102"><vh>Callbacks</vh>
<v t="T103"><vh>marksButtonCallback</vh></v>
<v t="T104"><vh>recentButtonCallback</vh></v>
</v>
</v>
<v t="T105"><vh>class globalInfoClass</vh>
<v t="T106"><vh>__init__ ( globalInfoClass)</vh></v>
<v t="T107"><vh>addNavWidgets</vh></v>
<v t="T108"><vh>destroyFrame, destroyAllFrames, destroyOneFrame</vh></v>
<v t="T109"><vh>updateRecentSections</vh></v>
<v t="T110"><vh>updateMarks &amp; updateMarksAfterCommand</vh></v>
<v t="T111"><vh>updateNavButtons</vh></v>
</v>
<v t="T112"><vh>class marksDialog (listBoxDialog)</vh>
<v t="T113"><vh>marksDialog.__init__</vh></v>
<v t="T114"><vh>createFrame</vh></v>
<v t="T115"><vh>addbuttons</vh></v>
<v t="T116"><vh>fillbox</vh></v>
</v>
<v t="T117"><vh>class recentSectionsDialog (listBoxDialog)</vh>
<v t="T118"><vh>__init__  recentSectionsDialog</vh></v>
<v t="T119"><vh>addButtons</vh></v>
<v t="T120"><vh>clearAll</vh></v>
<v t="T121"><vh>createFrame</vh></v>
<v t="T122"><vh>deleteEntry</vh></v>
<v t="T123"><vh>destroy</vh></v>
<v t="T124"><vh>fillbox (recent sections)</vh>
<v t="T125"><vh>&lt;&lt; reconstruct the contents of self.box &gt;&gt;&gt;</vh></v>
</v>
<v t="T126"><vh>synchNavButtons</vh></v>
</v>
</v>
</v>
<v t="T127"><vh>External editors &amp; Open With</vh>
<v t="T128"><vh>@file open_with.py</vh>
<v t="T129"><vh>on_idle</vh>
<v t="T130"><vh>&lt;&lt; update v's body text &gt;&gt;</vh>
<v t="T131"><vh>&lt;&lt; set s to the file text &gt;&gt;</vh></v>
</v>
</v>
<v t="T132"><vh>create_open_with_menu</vh>
<v t="T133"><vh>&lt;&lt; create the Open With menu &gt;&gt;</vh></v>
</v>
</v>
<v t="T134"><vh>@file vim.py</vh>
<v t="T135"><vh>open_in_vim</vh></v>
</v>
<v t="T136"><vh>@file xemacs.py</vh></v>
</v>
<v t="T137"><vh>Files</vh>
<v t="T138"><vh>@file empty_leo_file.py</vh>
<v t="T139"><vh>&lt;&lt; define minimal .leo file &gt;&gt;</vh></v>
<v t="T140"><vh>onOpen</vh></v>
</v>
<v t="T141"><vh>@file open_shell.py</vh>
<v t="T142"><vh>&lt;&lt; about the open shell plugin &gt;&gt;</vh></v>
<v t="T143"><vh>load_menu</vh></v>
<v t="T144"><vh>_getpath</vh></v>
<v t="T145"><vh>_getcurrentnodepath</vh></v>
<v t="T146"><vh>launchCmd</vh></v>
<v t="T147"><vh>launchExplorer</vh></v>
<v t="T148"><vh>launchxTerm</vh></v>
</v>
</v>
<v t="T149"><vh>Foreign languages</vh>
<v t="T150"><vh>@file french.py</vh>
<v t="T151"><vh>onMenu</vh></v>
</v>
<v t="T152"><vh>@file french_fm.py</vh>
<v t="T153"><vh>onMenu</vh></v>
</v>
</v>
<v t="T154"><vh>Key bindings</vh>
<v t="T155"><vh>@file arrows.py</vh>
<v t="T156"><vh>onOpen</vh></v>
</v>
</v>
<v t="T157"><vh>Menus</vh>
<v t="T158"><vh> Plugins menu</vh>
<v t="T159"><vh>@file plugins_menu.py</vh>
<v t="T160"><vh>class Plugin</vh>
<v t="T161"><vh>__init__</vh>
<v t="T162"><vh>&lt;&lt; Check if this can be configured &gt;&gt;</vh></v>
<v t="T163"><vh>&lt;&lt; Check if this has an apply &gt;&gt;</vh></v>
<v t="T164"><vh>&lt;&lt; Look for additional commands &gt;&gt;</vh></v>
</v>
<v t="T165"><vh>about</vh></v>
<v t="T166"><vh>properties</vh></v>
</v>
<v t="T167"><vh>class PropertiesWindow</vh>
<v t="T168"><vh>__init__</vh>
<v t="T169"><vh>&lt;&lt; initialize all ivars &gt;&gt;</vh></v>
<v t="T170"><vh>&lt;&lt; create the frame from the configuration data &gt;&gt;</vh>
<v t="T171"><vh>&lt;&lt; Create the top level and the main frame &gt;&gt;</vh></v>
<v t="T172"><vh>&lt;&lt; Create widgets for each section and option &gt;&gt;</vh></v>
<v t="T173"><vh>&lt;&lt; Create Ok, Cancel and Apply buttons &gt;&gt;</vh></v>
</v>
</v>
<v t="T174"><vh>Event Handlers</vh></v>
<v t="T175"><vh>writeConfiguration</vh></v>
</v>
<v t="T176"><vh>class PluginAbout</vh>
<v t="T177"><vh>__init__</vh>
<v t="T178"><vh>&lt;&lt; Create the contents of the about box &gt;&gt;</vh></v>
<v t="T179"><vh>&lt;&lt; Create the close button &gt;&gt;</vh></v>
</v>
</v>
<v t="T180"><vh>createPluginsMenu</vh>
<v t="T181"><vh>&lt;&lt; add items to the plugins menu &gt;&gt;</vh></v>
</v>
</v>
<v t="T182"><vh>@file test.py</vh>
<v t="T183"><vh>applyConfiguration</vh></v>
<v t="T184"><vh>cmd_fn1/2/3</vh></v>
<v t="T185"><vh>onSelect</vh>
<v t="T186"><vh>&lt;&lt; Select Image &gt;&gt;</vh></v>
</v>
<v t="T187"><vh>onUnselect</vh>
<v t="T188"><vh>&lt;&lt; Unselect Image &gt;&gt;</vh></v>
</v>
</v>
<v t="T189"><vh>Notes re plugins menu</vh>
<v t="T190"><vh> Changes made by E.K.Ream</vh></v>
<v t="T191"><vh> Design</vh></v>
<v t="T192"><vh> Initial suggestion from Paul Paterson</vh></v>
</v>
</v>
<v t="T193"><vh>@file scripts_menu.py</vh>
<v t="T194"><vh>createScriptsMenu</vh>
<v t="T195"><vh>&lt;&lt; Return if no scripts exist anywhere &gt;&gt;</vh></v>
<v t="T196"><vh>&lt;&lt; Create top-level entries for every script in top_scripts &gt;&gt;</vh></v>
<v t="T197"><vh>&lt;&lt; Create a submenu for dir containing each file in files &gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="T198"><vh>New kinds of nodes</vh>
<v t="T199"><vh>@file at_folder.py</vh>
<v t="T200"><vh>&lt;&lt; about this plugin &gt;&gt;</vh></v>
<v t="T201"><vh>sync_node_to_folder</vh></v>
</v>
<v t="T202"><vh>@file read_only_nodes.py</vh>
<v t="T203"><vh>documentation for @read-only nodes</vh>
<v t="T204"><vh>ftp/http access</vh></v>
</v>
<v t="T205"><vh>class FTPurl</vh>
<v t="T206"><vh>__init__</vh></v>
<v t="T207"><vh>Getters</vh>
<v t="T208"><vh>read</vh></v>
<v t="T209"><vh>readline</vh></v>
</v>
<v t="T210"><vh>Setters</vh>
<v t="T211"><vh>write</vh></v>
</v>
<v t="T212"><vh>Utilities</vh>
<v t="T213"><vh>seek</vh></v>
<v t="T214"><vh>flush</vh></v>
<v t="T215"><vh>dir</vh></v>
<v t="T216"><vh>exists</vh></v>
<v t="T217"><vh>checkParams</vh></v>
</v>
<v t="T218"><vh>close</vh></v>
</v>
<v t="T219"><vh>enable/disable_body</vh></v>
<v t="T220"><vh>insert_read_only_node (FTP version)</vh>
<v t="T221"><vh>&lt;&lt; convert HTML to text &gt;&gt;</vh></v>
</v>
<v t="T222"><vh>on_open2</vh></v>
<v t="T223"><vh>on_bodykey1</vh></v>
<v t="T224"><vh>on_headkey2</vh></v>
<v t="T225"><vh>on_select1</vh></v>
<v t="T226"><vh>on_select2</vh></v>
</v>
<v t="T227"><vh>@file rst.py</vh>
<v t="T228"><vh>&lt;&lt;about this plugin &gt;&gt;</vh></v>
<v t="T229"><vh>&lt;&lt; change log &gt;&gt;</vh></v>
<v t="T230"><vh>onIconDoubleClick</vh>
<v t="T231"><vh>&lt;&lt; write rST as HTML &gt;&gt;</vh>
<v t="T232"><vh>&lt;&lt; convert rST to HTML &gt;&gt;</vh></v>
</v>
<v t="T233"><vh>&lt;&lt; write rST file &gt;&gt;</vh></v>
</v>
<v t="T234"><vh>writeTreeAsRst</vh></v>
<v t="T235"><vh>underline</vh></v>
</v>
<v t="T236"><vh>@file startfile.py</vh>
<v t="T237"><vh>&lt;&lt;about this plugin &gt;&gt;</vh></v>
<v t="T238"><vh>&lt;&lt; change log &gt;&gt;</vh></v>
<v t="T239"><vh>onIconDoubleClick</vh>
<v t="T240"><vh>&lt;&lt; find path and start file &gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="T241"><vh>Overriding functions, methods &amp; classes</vh>
<v t="T242"><vh>@file __overrideClasses.py</vh>
<v t="T243"><vh>&lt;&lt; override the LeoFrame class &gt;&gt;</vh></v>
<v t="T244"><vh>&lt;&lt; override methods of the LeoApp class &gt;&gt;</vh></v>
</v>
<v t="T245"><vh>@file override_commands.py</vh>
<v t="T246"><vh>onCommand</vh></v>
</v>
<v t="T247"><vh>@file redefine_put.py</vh>
<v t="T248"><vh>onStart</vh></v>
<v t="T249"><vh>newPut and newPutNl</vh></v>
</v>
<v t="T250"><vh>@file redirect_to_log.py</vh></v>
<v t="T251"><vh>@file script_io_to_body.py</vh>
<v t="T252"><vh>onStart</vh></v>
<v t="T253"><vh>newExecuteScript</vh></v>
<v t="T254"><vh>newPut and newPutNl</vh></v>
<v t="T255"><vh>newEs, etc.</vh></v>
</v>
</v>
<v t="T256"><vh>Spell Checking</vh>
<v t="T257"><vh>@silentfile mod_spelling.txt</vh></v>
<v t="T258"><vh>@file mod_spelling.ini</vh></v>
<v t="T259"><vh>@file mod_spelling.py</vh>
<v t="T260"><vh>Functions</vh>
<v t="T261"><vh>createSpellMenu</vh></v>
<v t="T262"><vh>onSelect</vh></v>
<v t="T263"><vh>onCommand</vh></v>
</v>
<v t="T264"><vh>class Aspell</vh>
<v t="T265"><vh>Birth &amp; death</vh>
<v t="T266"><vh>__init__</vh></v>
<v t="T267"><vh>getAspellDirectory</vh></v>
</v>
<v t="T268"><vh>openPipes</vh>
<v t="T269"><vh>&lt;&lt; Ensure local dictionary is present &gt;&gt;</vh></v>
</v>
<v t="T270"><vh>closePipes</vh></v>
<v t="T271"><vh>listAlternates</vh></v>
<v t="T272"><vh>processWord</vh></v>
<v t="T273"><vh>updateDictionary</vh></v>
</v>
<v t="T274"><vh>class spellDialog</vh>
<v t="T275"><vh>Birth &amp; death</vh>
<v t="T276"><vh>spell.__init__</vh>
<v t="T277"><vh>&lt;&lt; set self.dictionary &gt;&gt;</vh></v>
</v>
<v t="T278"><vh>getLocalDictionary</vh></v>
<v t="T279"><vh>getLocalLanguageCode</vh></v>
<v t="T280"><vh>readLocalDictionary</vh></v>
</v>
<v t="T281"><vh>createFrame</vh>
<v t="T282"><vh>&lt;&lt; Create the text and suggestion panes &gt;&gt;</vh></v>
<v t="T283"><vh>&lt;&lt; Create the spelling buttons &gt;&gt;</vh></v>
</v>
<v t="T284"><vh>Buttons</vh>
<v t="T285"><vh>onAddButton</vh></v>
<v t="T286"><vh>onIgnoreButton</vh></v>
<v t="T287"><vh>onChangeButton &amp; onChangeThenFindButton</vh></v>
<v t="T288"><vh>onFindButton</vh></v>
<v t="T289"><vh>onHideButton</vh></v>
<v t="T290"><vh>onRedoButton &amp; onUndoButton</vh></v>
</v>
<v t="T291"><vh>Commands</vh>
<v t="T292"><vh>add</vh></v>
<v t="T293"><vh>change</vh></v>
<v t="T294"><vh>checkSpelling</vh></v>
<v t="T295"><vh>find</vh></v>
<v t="T296"><vh>ignore</vh></v>
</v>
<v t="T297"><vh>Helpers</vh>
<v t="T298"><vh>closePipes</vh></v>
<v t="T299"><vh>fillbox</vh></v>
<v t="T300"><vh>findNextMisspelledWord</vh>
<v t="T301"><vh>&lt;&lt; Skip word if ignored or in local dictionary &gt;&gt;</vh></v>
</v>
<v t="T302"><vh>findNextWord</vh></v>
<v t="T303"><vh>getSuggestion</vh></v>
<v t="T304"><vh>onMap</vh></v>
<v t="T305"><vh>onSelectListBox</vh></v>
<v t="T306"><vh>update</vh></v>
<v t="T307"><vh>updateButtons</vh></v>
</v>
</v>
</v>
</v>
<v t="T308" a="M"><vh>New</vh>
<v t="T309"><vh>mod_autosave</vh>
<v t="T310"><vh>@file mod_autosave.ini</vh></v>
<v t="T311"><vh>@file mod_autosave.py</vh>
<v t="T312"><vh>applyConfiguration</vh></v>
<v t="T313"><vh>autosave</vh></v>
</v>
</v>
<v t="T314"><vh>@file mod_timestamp.py</vh>
<v t="T315"><vh>timestamp</vh></v>
</v>
</v>
</v>
<v t="T316"><vh>(Settings menu)</vh>
<v t="T317"><vh>To do</vh></v>
<v t="T318"><vh>Design of Settings menu</vh></v>
<v t="T319"><vh>@file settings_menu.py</vh>
<v t="T320"><vh>createSettingsMenu</vh></v>
</v>
</v>
<v t="T321"><vh>(wxStuff: not a plugin yet)</vh>
<v t="T322"><vh>wxTests</vh>
<v t="T323"><vh>@file c:\prog\test\wxTest.py</vh></v>
</v>
<v t="T324"><vh>old wxLeo code (imported C++ code)</vh>
<v t="T325"><vh>alert.cpp</vh>
<v t="T326"><vh>alert</vh></v>
<v t="T327"><vh>assertFailedDialog</vh></v>
</v>
<v t="T328"><vh>FindPanel.cpp</vh>
<v t="T329"><vh>&lt;&lt; FindPanel declarations &gt;&gt;</vh></v>
<v t="T330" a="M"><vh>BEGIN_EVENT_TABLE</vh></v>
<v t="T331" a="M"><vh>ctor</vh></v>
<v t="T332"><vh>OnActivateFindFrame</vh></v>
<v t="T333"><vh>OnSetFocus</vh></v>
<v t="T334"><vh>OnCloseFindFrame</vh></v>
<v t="T335"><vh>OnChangeButton</vh></v>
<v t="T336"><vh>OnChangeAllButton</vh></v>
<v t="T337"><vh>OnChangeThenFindButton</vh></v>
<v t="T338"><vh>OnFindButton</vh></v>
<v t="T339"><vh>OnFindAllButton</vh></v>
<v t="T340"><vh>OnBatchCheckBox</vh></v>
<v t="T341"><vh>OnIgnoreCaseCheckBox</vh></v>
<v t="T342"><vh>OnMarkChangesCheckBox</vh></v>
<v t="T343"><vh>OnMarkFindsCheckBox</vh></v>
<v t="T344"><vh>OnPatternMatchCheckBox</vh></v>
<v t="T345"><vh>OnReverseCheckBox</vh></v>
<v t="T346"><vh>OnSearchBodyTextCheckBox</vh></v>
<v t="T347"><vh>OnSearchHeadlineCheckBox</vh></v>
<v t="T348"><vh>OnSuboutlineOnlyCheckBox</vh></v>
<v t="T349"><vh>OnWrapAroundCheckBox</vh></v>
<v t="T350"><vh>OnWholeWordCheckBox</vh></v>
<v t="T351"><vh>OnChangeText</vh></v>
<v t="T352"><vh>OnFindText</vh></v>
<v t="T353"><vh>set_check_boxes</vh></v>
<v t="T354"><vh>FindPanel</vh></v>
</v>
<v t="T355" a="M"><vh>LeoApp.cpp</vh>
<v t="T356" a="M"><vh>Event table</vh></v>
<v t="T357"><vh>OnInit</vh>
<v t="T358"><vh>&lt;&lt; Switch to the other running copy of Leo if one is already open &gt;&gt;</vh></v>
<v t="T359"><vh>&lt;&lt; Set gAppDirectory &gt;&gt;</vh></v>
<v t="T360"><vh>&lt;&lt; Open a file when double-clicking an icon &gt;&gt;</vh></v>
<v t="T361"><vh>&lt;&lt; Create a frame and link it into the global frame list &gt;&gt;</vh></v>
<v t="T362"><vh>&lt;&lt; Initialize Sherlock &gt;&gt;</vh></v>
<v t="T363"><vh>&lt;&lt; Dump the command line &gt;&gt;</vh></v>
</v>
<v t="T364"><vh>OnExit</vh></v>
<v t="T365"><vh>init_args</vh></v>
<v t="T366"><vh>wxFindAppPath</vh></v>
<v t="T367"><vh>log_open</vh></v>
<v t="T368"><vh>put_cstring_to_log_window</vh></v>
</v>
<v t="T369" a="M"><vh>LeoFrame.cpp</vh>
<v t="T370" a="M"><vh>BEGIN_EVENT_TABLE</vh>
<v t="T371"><vh>&lt;&lt; Declare menu events &gt;&gt;</vh></v>
</v>
<v t="T372" a="M"><vh>ctor</vh>
<v t="T373"><vh>&lt;&lt; Initialize the private vars &gt;&gt;</vh></v>
<v t="T374"><vh>&lt;&lt; Initialize the argument settings &gt;&gt;</vh></v>
<v t="T375"><vh>&lt;&lt; Create the splitter windows &gt;&gt;</vh></v>
<v t="T376"><vh>&lt;&lt; Create the accelerator table &gt;&gt;</vh></v>
<v t="T377"><vh>&lt;&lt; Create the status bar &gt;&gt;</vh></v>
<v t="T378"><vh>&lt;&lt; Set the window Icon &gt;&gt;</vh></v>
<v t="T379"><vh>&lt;&lt; Set the caret blink rate &gt;&gt;</vh></v>
<v t="T380"><vh>&lt;&lt; Add root node to the tree view &gt;&gt;</vh></v>
</v>
<v t="T381"><vh>createMenus</vh></v>
<v t="T382"><vh>SetUntitledNumber</vh></v>
<v t="T383"><vh>putToLog</vh></v>
<v t="T384"><vh>getLogText</vh></v>
<v t="T385"><vh>event handlers</vh>
<v t="T386"><vh>onActivate</vh></v>
<v t="T387"><vh>OnSetFocus</vh></v>
<v t="T388"><vh>onResize</vh></v>
<v t="T389"><vh>onBodyTextUpdated</vh></v>
<v t="T390"><vh>onCloseLeoFrame</vh></v>
<v t="T391"><vh>onTreeChanged</vh></v>
<v t="T392"><vh>onTreeChanging</vh></v>
<v t="T393"><vh>onTreeKeyDown</vh></v>
<v t="T394"><vh>onTreeBeginDrag</vh></v>
<v t="T395"><vh>onTreeEndDrag</vh></v>
<v t="T396"><vh>onTreeBeginLabelEdit</vh></v>
<v t="T397"><vh>onTreeEndLabelEdit</vh></v>
<v t="T398"><vh>updateJoinedHeadlines</vh></v>
<v t="T399"><vh>OnUpdateRevert</vh></v>
<v t="T400"><vh>OnNew</vh></v>
<v t="T401"><vh>OnOpen</vh></v>
<v t="T402"><vh>OpenWithFileName</vh></v>
<v t="T403"><vh>OnClose</vh></v>
<v t="T404"><vh>OnSave</vh></v>
<v t="T405"><vh>OnSaveAs</vh></v>
<v t="T406"><vh>OnSaveTo</vh></v>
<v t="T407"><vh>OnRevert</vh></v>
<v t="T408"><vh>OnPageSetup</vh></v>
<v t="T409"><vh>OnPrint</vh></v>
<v t="T410"><vh>OnTangleSubmenu</vh></v>
<v t="T411"><vh>OnUntangleSubmenu</vh></v>
<v t="T412"><vh>OnImportExportSubmenu</vh></v>
<v t="T413"><vh>OnQuit</vh></v>
<v t="T414"><vh>OnReadOutlineOnly</vh></v>
<v t="T415"><vh>readOutlineOnly</vh></v>
<v t="T416"><vh>OnReadAtFileNodes</vh></v>
<v t="T417"><vh>OnWriteOutlineOnly</vh></v>
<v t="T418"><vh>OnWriteAtFileNodes</vh></v>
<v t="T419"><vh>OnTangleAll</vh></v>
<v t="T420"><vh>OnTangleMarked</vh></v>
<v t="T421"><vh>OnTangle</vh></v>
<v t="T422"><vh>OnUntangleAll</vh></v>
<v t="T423"><vh>OnUntangleMarked</vh></v>
<v t="T424"><vh>OnUntangle</vh></v>
<v t="T425"><vh>OnImportFiles</vh></v>
<v t="T426"><vh>OnImportCWEBFiles</vh></v>
<v t="T427"><vh>OnImportNowebFiles</vh></v>
<v t="T428"><vh>OnImportMoreText</vh></v>
<v t="T429"><vh>OnFlattenOutline</vh></v>
<v t="T430"><vh>OnUpdateCopy</vh></v>
<v t="T431"><vh>OnUpdateCut</vh></v>
<v t="T432"><vh>OnUpdateDelete</vh></v>
<v t="T433"><vh>OnUpdateExtract</vh></v>
<v t="T434"><vh>OnUpdateExtractNames</vh></v>
<v t="T435"><vh>OnUpdateExtractSection</vh></v>
<v t="T436"><vh>OnUpdateFind</vh></v>
<v t="T437"><vh>OnUpdatePaste</vh></v>
<v t="T438"><vh>OnUpdateRedo</vh></v>
<v t="T439"><vh>OnUpdateReplace</vh></v>
<v t="T440"><vh>OnUpdateSelectAll</vh></v>
<v t="T441"><vh>OnUpdateUndo</vh></v>
<v t="T442"><vh>hasSelection</vh></v>
<v t="T443"><vh>OnUndo</vh></v>
<v t="T444"><vh>OnRedo</vh></v>
<v t="T445"><vh>OnCut</vh></v>
<v t="T446"><vh>OnCopy</vh></v>
<v t="T447"><vh>OnPaste</vh></v>
<v t="T448"><vh>OnDelete</vh></v>
<v t="T449"><vh>OnSelectAll</vh></v>
<v t="T450"><vh>OnEditHeadline</vh></v>
<v t="T451"><vh>OnFontPanel</vh></v>
<v t="T452"><vh>OnSyntaxColoring</vh></v>
<v t="T453"><vh>OnPreferences</vh></v>
<v t="T454"><vh>OnConvertBlanks</vh></v>
<v t="T455"><vh>OnExtractSection</vh></v>
<v t="T456"><vh>OnExtractNames</vh></v>
<v t="T457"><vh>OnExtract</vh></v>
<v t="T458"><vh>OnFindPanel</vh></v>
<v t="T459"><vh>OnFindNext</vh></v>
<v t="T460"><vh>OnFindPrevious</vh></v>
<v t="T461"><vh>OnReplace</vh></v>
<v t="T462"><vh>OnReplaceThenFind</vh></v>
<v t="T463"><vh>OnUpdateCutNode</vh></v>
<v t="T464"><vh>OnUpdateDeleteNode</vh></v>
<v t="T465"><vh>OnUpdatePasteNode</vh></v>
<v t="T466"><vh>OnUpdateSortNode</vh></v>
<v t="T467"><vh>OnUpdateExpandAll</vh></v>
<v t="T468"><vh>OnUpdateExpandAllChildren</vh></v>
<v t="T469"><vh>OnUpdateExpandChildren</vh></v>
<v t="T470"><vh>OnUpdateContractAll</vh></v>
<v t="T471"><vh>OnUpdateContractAllChildren</vh></v>
<v t="T472"><vh>OnUpdateContractChildren</vh></v>
<v t="T473"><vh>OnUpdateMoveDown</vh></v>
<v t="T474"><vh>OnUpdateMoveLeft</vh></v>
<v t="T475"><vh>OnUpdateMoveRight</vh></v>
<v t="T476"><vh>OnUpdateMoveUp</vh></v>
<v t="T477"><vh>OnUpdatePromote</vh></v>
<v t="T478"><vh>OnUpdateDemote</vh></v>
<v t="T479"><vh>OnUpdateGoPrevVisible</vh></v>
<v t="T480"><vh>OnUpdateGoNextVisible</vh></v>
<v t="T481"><vh>OnUpdateGoBack</vh></v>
<v t="T482"><vh>OnUpdateGoNext</vh></v>
<v t="T483"><vh>OnUpdateMark</vh></v>
<v t="T484"><vh>OnUpdateMarkSubheads</vh></v>
<v t="T485"><vh>OnUpdateMarkChangedItems</vh></v>
<v t="T486"><vh>OnUpdateMarkChangedRoots</vh></v>
<v t="T487"><vh>OnUpdateGoToNextMarked</vh></v>
<v t="T488"><vh>OnUpdateGoToNextChanged</vh></v>
<v t="T489"><vh>OnCutNode</vh></v>
<v t="T490"><vh>OnCopyNode</vh></v>
<v t="T491"><vh>OnPasteNode</vh></v>
<v t="T492"><vh>OnDeleteNode</vh></v>
<v t="T493"><vh>OnInsertNode</vh></v>
<v t="T494"><vh>OnCloneNode</vh></v>
<v t="T495"><vh>OnSortNode</vh></v>
<v t="T496"><vh>OnExpandAll</vh></v>
<v t="T497"><vh>OnExpandAllChildren</vh></v>
<v t="T498"><vh>OnExpandChildren</vh></v>
<v t="T499"><vh>OnContractAll</vh></v>
<v t="T500"><vh>OnContractAllChildren</vh></v>
<v t="T501"><vh>OnContractChildren</vh></v>
<v t="T502"><vh>OnExpandNextLevel</vh></v>
<v t="T503"><vh>OnExpandToLevel1</vh></v>
<v t="T504"><vh>OnExpandToLevel2</vh></v>
<v t="T505"><vh>OnExpandToLevel3</vh></v>
<v t="T506"><vh>OnExpandToLevel4</vh></v>
<v t="T507"><vh>OnExpandToLevel5</vh></v>
<v t="T508"><vh>OnExpandToLevel6</vh></v>
<v t="T509"><vh>OnExpandToLevel7</vh></v>
<v t="T510"><vh>OnExpandToLevel8</vh></v>
<v t="T511"><vh>OnExpandToLevel9</vh></v>
<v t="T512"><vh>OnMoveDown</vh></v>
<v t="T513"><vh>OnMoveLeft</vh></v>
<v t="T514"><vh>OnMoveRight</vh></v>
<v t="T515"><vh>OnMoveUp</vh></v>
<v t="T516"><vh>OnPromote</vh></v>
<v t="T517"><vh>OnDemote</vh></v>
<v t="T518"><vh>OnGoPrevVisible</vh></v>
<v t="T519"><vh>OnGoNextVisible</vh></v>
<v t="T520"><vh>OnGoBack</vh></v>
<v t="T521"><vh>OnGoNext</vh></v>
<v t="T522"><vh>OnMark</vh></v>
<v t="T523"><vh>OnMarkSubheads</vh></v>
<v t="T524"><vh>OnMarkChangedItems</vh></v>
<v t="T525"><vh>OnMarkChangedRoots</vh></v>
<v t="T526"><vh>OnMarkAllAtFileNodesDirty</vh></v>
<v t="T527"><vh>OnMarkAtFileNodesDirty</vh></v>
<v t="T528"><vh>OnUnmarkAll</vh></v>
<v t="T529"><vh>OnGoToNextMarked</vh></v>
<v t="T530"><vh>OnGoToNextChanged</vh></v>
<v t="T531"><vh>OnEqualSizedPanes</vh></v>
<v t="T532"><vh>OnToggleActivePane</vh></v>
<v t="T533"><vh>OnChangeDirection</vh></v>
<v t="T534"><vh>OnCascade</vh></v>
<v t="T535"><vh>OnMinimizeAll</vh></v>
<v t="T536"><vh>OnOpenPythonWindow</vh></v>
<v t="T537"><vh>OnRecentWindows</vh></v>
<v t="T538"><vh>OnAbout</vh></v>
</v>
</v>
<v t="T539"><vh>LeoPrefs.cpp</vh>
<v t="T540"><vh>&lt;&lt; LeoPrefs declarations &gt;&gt;</vh></v>
<v t="T541"><vh>BEGIN_EVENT_TABLE</vh></v>
<v t="T542"><vh>ctor</vh></v>
<v t="T543"><vh>initialize</vh></v>
<v t="T544"><vh>targetToLanguage</vh></v>
<v t="T545"><vh>languageToTarget</vh></v>
<v t="T546"><vh>OnActivatePrefsFrame</vh></v>
<v t="T547"><vh>OnClosePrefsFrame</vh></v>
<v t="T548"><vh>OnPageWidthText</vh></v>
<v t="T549"><vh>OnDoneBatCheckBox</vh></v>
<v t="T550"><vh>OnUnBatCheckBox</vh></v>
<v t="T551"><vh>OnTangleDirectoryText</vh></v>
<v t="T552"><vh>OnHeaderCheckBox</vh></v>
<v t="T553"><vh>OnDocChunksCheckBox</vh></v>
<v t="T554"><vh>OnTargetLanguageRadioBox</vh></v>
<v t="T555"><vh>PrefsPanel</vh></v>
</v>
</v>
<v t="T556"><vh>wxPython docs: local @urls</vh>
<v t="T557"><vh>@url file:///C:/prog/wxDocs/wx26.htm#classref</vh></v>
<v t="T558"><vh>@url file:c:\prog\wxDocs\index.htm</vh></v>
<v t="T559" a="M"><vh>@url file:///C:\Python22\Lib\site-packages\wxPython\docs\wxPythonManual.html</vh></v>
<v t="T560"><vh>app, color, icon, sizer, xmlresource</vh>
<v t="T561"><vh>@url file:///C:/prog/wxDocs/wx30.htm#wxapp</vh></v>
<v t="T562"><vh>@url file:///C:/prog/wxDocs/wx63.htm#wxcolour</vh></v>
<v t="T563"><vh>@url file:///C:/prog/wxDocs/wx216.htm#wxicon</vh></v>
<v t="T564"><vh>@url file:///C:/prog/wxDocs/wx343.htm#wxsizer</vh></v>
<v t="T565"><vh>@url file:///C:/prog/wxDocs/wx418.htm#wxxmlresource</vh></v>
</v>
<v t="T566"><vh>dialog, frame, panel, splitter,window</vh>
<v t="T567"><vh>@url file:///C:/prog/wxDocs/wx109.htm#wxdialog</vh></v>
<v t="T568"><vh>@url file:///C:/prog/wxDocs/wx163.htm#wxframe</vh></v>
<v t="T569"><vh>@url file:///C:/prog/wxDocs/wx291.htm#wxpanel</vh></v>
<v t="T570"><vh>@url file:///C:/prog/wxDocs/wx357.htm#wxsplitterwindow</vh></v>
<v t="T571"><vh>@url file:///C:/prog/wxDocs/wx411.htm#wxwindow</vh></v>
</v>
<v t="T572"><vh>events</vh>
<v t="T573"><vh>@url file:///C:/prog/wxDocs/wx130.htm#wxevent</vh></v>
<v t="T574"><vh>@url file:///C:/prog/wxDocs/wx264.htm#wxmenuevent</vh></v>
<v t="T575"><vh>@url file:///C:/prog/wxDocs/wx356.htm#wxsplitterevent</vh></v>
<v t="T576"><vh>@url file:///C:/prog/wxDocs/wx400.htm#wxtreeevent</vh></v>
</v>
<v t="T577"><vh>menu</vh>
<v t="T578"><vh>@url file:///C:/prog/wxDocs/wx262.htm#wxmenu</vh></v>
<v t="T579"><vh>@url file:///C:/prog/wxDocs/wx263.htm#wxmenubar</vh></v>
<v t="T580"><vh>@url file:///C:/prog/wxDocs/wx265.htm#wxmenuitem</vh></v>
</v>
<v t="T581"><vh>tree</vh>
<v t="T582" a="M"><vh>@url file:///C:/prog/wxDocs/wx399.htm#wxtreectrl</vh></v>
<v t="T583"><vh>@url file:///C:/prog/wxDocs/wx401.htm#wxtreeitemdata</vh></v>
</v>
<v t="T584"><vh>widgets</vh>
<v t="T585"><vh>@url file:///C:/prog/wxDocs/wx46.htm#wxbutton</vh></v>
<v t="T586"><vh>@url file:///C:/prog/wxDocs/wx52.htm#wxcheckbox</vh></v>
<v t="T587"><vh>@url file:///C:/prog/wxDocs/wx212.htm#wxhtmlwindow</vh></v>
<v t="T588"><vh>@url file:///C:/prog/wxDocs/wx357.htm#wxsplitterwindow</vh></v>
<v t="T589" a="M"><vh>@url file:///C:/prog/wxDocs/wx381.htm#wxtextctrl</vh></v>
</v>
<v t="T590"><vh>wx Questions</vh></v>
</v>
<v t="T591"><vh>Leo wx prototype</vh>
<v t="T592"><vh>@file c:\prog\test\wxLeo.py</vh>
<v t="T593"><vh>app</vh>
<v t="T594"><vh>OnInit</vh></v>
</v>
<v t="T595"><vh>frame</vh>
<v t="T596"><vh>__init__</vh></v>
<v t="T597"><vh>createMenus (old code: explicit id's)</vh>
<v t="T598"><vh>&lt;&lt; Create the File menu &gt;&gt;</vh>
<v t="T599"><vh>&lt;&lt; Create the initial items of the file menu &gt;&gt;</vh></v>
<v t="T600"><vh>&lt;&lt; Create the Read/Write submenu &gt;&gt;</vh></v>
<v t="T601"><vh>&lt;&lt; Create the Tangle submenu &gt;&gt;</vh></v>
<v t="T602"><vh>&lt;&lt; Create the Untangle submenu &gt;&gt;</vh></v>
<v t="T603"><vh>&lt;&lt; Create the Import Files submenu &gt;&gt;</vh></v>
</v>
<v t="T604"><vh>&lt;&lt; Create the Edit menu &gt;&gt;</vh>
<v t="T605"><vh>&lt;&lt; Create the initial items of the Edit menu &gt;&gt;</vh></v>
<v t="T606"><vh>&lt;&lt; Create the Find submenu &gt;&gt;</vh></v>
<v t="T607"><vh>&lt;&lt; Create the final items of the Edit menu &gt;&gt;</vh></v>
<v t="T608"><vh>&lt;&lt; Create the Edit Body submenu &gt;&gt;</vh></v>
</v>
<v t="T609"><vh>&lt;&lt; Create the Outline menu &gt;&gt;</vh>
<v t="T610"><vh>&lt;&lt; Create the initial items of the Outline menu &gt;&gt;</vh></v>
<v t="T611"><vh>&lt;&lt; Create the Expand/Contract submenu &gt;&gt;</vh></v>
<v t="T612"><vh>&lt;&lt; Create the Move/Select submenu &gt;&gt;</vh></v>
<v t="T613"><vh>&lt;&lt; Create the Mark/Go To submenu &gt;&gt;</vh></v>
</v>
<v t="T614"><vh>&lt;&lt; Create the Window menu &gt;&gt;</vh></v>
<v t="T615"><vh>&lt;&lt; Create the Help menu &gt;&gt;</vh></v>
</v>
<v t="T616"><vh>createMenuBar</vh>
<v t="T617"><vh>&lt;&lt; create the edit menu &gt;&gt;</vh>
<v t="T618"><vh>&lt;&lt; create the first top-level edit entries &gt;&gt;</vh></v>
<v t="T619"><vh>&lt;&lt; create the edit body submenu &gt;&gt;</vh></v>
<v t="T620"><vh>&lt;&lt; create the edit headline submenu &gt;&gt;</vh></v>
<v t="T621"><vh>&lt;&lt; create the find submenu &gt;&gt;</vh></v>
<v t="T622"><vh>&lt;&lt; create the last top-level edit entries &gt;&gt;</vh></v>
</v>
<v t="T623"><vh>&lt;&lt; create the file menu &gt;&gt;</vh>
<v t="T624"><vh>&lt;&lt; create the top-level file entries &gt;&gt;</vh></v>
<v t="T625"><vh>&lt;&lt; create the recent files submenu &gt;&gt;</vh></v>
<v t="T626"><vh>&lt;&lt; create the read/write submenu &gt;&gt;</vh></v>
<v t="T627"><vh>&lt;&lt; create the tangle submenu &gt;&gt;</vh></v>
<v t="T628"><vh>&lt;&lt; create the untangle submenu &gt;&gt;</vh></v>
<v t="T629"><vh>&lt;&lt; create the import submenu &gt;&gt;</vh></v>
<v t="T630"><vh>&lt;&lt; create the export submenu &gt;&gt;</vh></v>
</v>
<v t="T631"><vh>&lt;&lt; create the outline menu &gt;&gt;</vh>
<v t="T632"><vh>&lt;&lt; create top-level outline menu &gt;&gt;</vh></v>
<v t="T633"><vh>&lt;&lt; create expand/contract submenu &gt;&gt;</vh></v>
<v t="T634"><vh>&lt;&lt; create move submenu &gt;&gt;</vh></v>
<v t="T635"><vh>&lt;&lt; create mark submenu &gt;&gt;</vh></v>
<v t="T636"><vh>&lt;&lt; create goto submenu &gt;&gt;</vh></v>
</v>
<v t="T637"><vh>&lt;&lt; create the window menu &gt;&gt;</vh></v>
<v t="T638"><vh>&lt;&lt; create the help menu &gt;&gt;</vh></v>
</v>
<v t="T639"><vh>createNewMenu</vh></v>
<v t="T640"><vh>createMenuEntries</vh></v>
<v t="T641"><vh>OnAbout</vh></v>
</v>
<v t="T642"><vh>const</vh></v>
</v>
</v>
</v>
<v t="T643" a="E"><vh>(4.0 project)(Not ready yet)</vh>
<v t="T644"><vh>To do</vh></v>
<v t="T645"><vh>Notes (do not delete)</vh>
<v t="T646"><vh>9/4 code notes</vh></v>
<v t="T647"><vh>9/4 Design of new file format</vh></v>
<v t="T648"><vh>9/3 design notes</vh>
<v t="T649"><vh>problems to be solved</vh></v>
<v t="T650"><vh>things to keep in mind</vh></v>
<v t="T651"><vh>strategy</vh></v>
<v t="T652"><vh>Request for diffs</vh></v>
</v>
<v t="T653"><vh>Notes</vh>
<v t="T654"><vh>About Consistency Summary posting</vh>
<v t="T655"><vh> Summary &amp; to do</vh>
<v t="T656"><vh>From 5. A new 4.0?  Owned &amp; unowned clones</vh></v>
<v t="T657"><vh>From 6: Handling multiply included @file nodes</vh></v>
</v>
<v t="T658"><vh>1. A new 4.0?  Consistency</vh></v>
<v t="T659"><vh>2. A new 4.0?  Ironical gnx's</vh></v>
<v t="T660"><vh>3. A new 4.0?  Derived files can be the SUM</vh></v>
<v t="T661"><vh>4. A new 4.0?  .leo files must be disjoint unions</vh></v>
<v t="T662"><vh>5. A new 4.0?  Owned &amp; unowned clones</vh></v>
<v t="T663"><vh>6. A new 4.0?  Acid tests</vh></v>
<v t="T664"><vh>7. A new 4.0?  Primary &amp; secondary data</vh></v>
<v t="T665"><vh>8. A new 4.0?  gnx's redux</vh></v>
</v>
<v t="T666"><vh>After transition</vh></v>
<v t="T667"><vh>Design Notes</vh>
<v t="T668"><vh> Examples: new file format</vh></v>
<v t="T669"><vh>Discussions</vh>
<v t="T670"><vh>Conflicting clones</vh>
<v t="T671"><vh>Jonathon 1</vh></v>
<v t="T672"><vh>Jonathan 2</vh></v>
<v t="T673"><vh>Gil 1</vh></v>
<v t="T674"><vh>Gil 2</vh></v>
</v>
<v t="T675"><vh>clone somewhere else</vh></v>
<v t="T676"><vh>Handling errors: Gil Shwartz</vh></v>
<v t="T677"><vh>save as surprise</vh>
<v t="T678"><vh>Reply</vh></v>
</v>
<v t="T679"><vh>Open derived file as outline</vh></v>
</v>
<v t="T680"><vh> Design Notes</vh>
<v t="T681"><vh>About gti's</vh></v>
<v t="T682"><vh>No childIndices</vh></v>
<v t="T683"><vh>Keep essential info together</vh></v>
<v t="T684"><vh>Clones are properties of outlines</vh></v>
<v t="T685"><vh>@include</vh></v>
<v t="T686"><vh>cvs may still corrupt derived files</vh></v>
<v t="T687"><vh>Blank lines can't be elimintated</vh></v>
<v t="T688"><vh>Goals for derived files</vh></v>
<v t="T689"><vh>Code won't change much</vh></v>
</v>
<v t="T690"><vh> Examples: whitespace</vh></v>
<v t="T691"><vh>posting: sentinels</vh></v>
<v t="T692"><vh>posting: whitespace</vh></v>
</v>
</v>
</v>
<v t="T693" a="M"><vh>Reference code</vh>
<v t="T694"><vh>Old code</vh>
<v t="T695"><vh>From leoConfig (Can be done after everything works)</vh>
<v t="T696"><vh>from config.__init__</vh></v>
<v t="T697"><vh>&lt;&lt; get config options &gt;&gt;</vh></v>
</v>
<v t="T698"><vh>From leoFileCommands.py</vh>
<v t="T699"><vh>From getGlobals</vh></v>
<v t="T700"><vh>From getLeoFile &amp; also getLeoOutline</vh></v>
<v t="T701"><vh>From getTnode</vh>
<v t="T702"><vh>From &lt;&lt; handle read from file &gt;&gt;</vh></v>
</v>
<v t="T703"><vh>From getVnode</vh></v>
<v t="T704"><vh>From assignFileIndices &amp; compactFileIndices</vh></v>
<v t="T705"><vh>From putGlobals</vh>
<v t="T706"><vh>&lt;&lt; put default gnx &gt;&gt;</vh></v>
</v>
<v t="T707"><vh>From putTnodes</vh>
<v t="T708"><vh>&lt;&lt; write all visited tnodes &gt;&gt;</vh></v>
</v>
<v t="T709"><vh>From putTnode</vh></v>
<v t="T710"><vh>From putVnode</vh>
<v t="T711"><vh>&lt;&lt; Put v.t.gnx &gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="T712"><vh>leoFileCommands.py</vh>
<v t="T713"><vh>leoFileCommands._init_</vh></v>
<v t="T714"><vh>Reading</vh>
<v t="T715"><vh>createVnode</vh></v>
<v t="T716"><vh>finishPaste (changed from 3.11.1)  (calls initAllCloneBits)</vh>
<v t="T717"><vh>&lt;&lt; Create join lists of all pasted vnodes &gt;&gt;</vh></v>
<v t="T718"><vh>&lt;&lt; Recompute clone bits for pasted vnodes &gt;&gt;</vh></v>
</v>
<v t="T719"><vh>get routines</vh>
<v t="T720"><vh>get &amp; match (basic)(leoFileCommands)</vh>
<v t="T721"><vh>get routines</vh></v>
<v t="T722"><vh>match routines</vh></v>
</v>
<v t="T723"><vh>getClipboardHeader</vh></v>
<v t="T724"><vh>getCloneWindows</vh></v>
<v t="T725"><vh>getEscapedString</vh></v>
<v t="T726"><vh>getFindPanelSettings</vh>
<v t="T727"><vh>&lt;&lt; Set defaults of all flags &gt;&gt;</vh></v>
</v>
<v t="T728"><vh>getGlobals (changed for 4.0)</vh></v>
<v t="T729"><vh>getLeoFile (calls setAllJoinLinks, initAllCloneBits)</vh>
<v t="T730"><vh>&lt;&lt; warn on read-only files &gt;&gt;</vh></v>
<v t="T731"><vh>&lt;&lt; scan all the xml elements &gt;&gt;</vh></v>
<v t="T732"><vh>&lt;&lt; raise an alert &gt;&gt;</vh></v>
</v>
<v t="T733"><vh>getLeoHeader</vh></v>
<v t="T734"><vh>getLeoOutline (from clipboard) (changed from 3.11.1)</vh></v>
<v t="T735"><vh>getPosition</vh></v>
<v t="T736"><vh>getPrefs</vh>
<v t="T737"><vh>&lt;&lt; check for syntax coloring prefs &gt;&gt; (getPrefs)</vh></v>
</v>
<v t="T738"><vh>getSize</vh></v>
<v t="T739"><vh>getTnode (no change from 3.11.1)(changed 6/11)</vh>
<v t="T740"><vh>&lt;&lt; handle read from file &gt;&gt;</vh></v>
<v t="T741"><vh>&lt;&lt; handle read from clipboard &gt;&gt;</vh></v>
</v>
<v t="T742"><vh>getTnodes (no change from 3.11.1)</vh></v>
<v t="T743"><vh>getVnode (changed from 3.11.1)</vh>
<v t="T744"><vh>&lt;&lt; Handle vnode attribute bits  &gt;&gt;</vh></v>
<v t="T745"><vh>&lt;&lt; Set the remembered status bits &gt;&gt;</vh></v>
</v>
<v t="T746"><vh>getVnodes  (no change from 3.11.1)</vh></v>
<v t="T747"><vh>getXmlStylesheetTag</vh></v>
<v t="T748"><vh>getXmlVersionTag</vh></v>
<v t="T749"><vh>skipWs</vh></v>
<v t="T750"><vh>skipWsAndNl</vh></v>
</v>
<v t="T751"><vh>newTnode</vh></v>
<v t="T752"><vh>readAtFileNodes</vh></v>
<v t="T753"><vh>fileCommands.readOutlineOnly</vh>
<v t="T754" a="C"><vh>&lt;&lt; Set the default directory &gt;&gt;</vh></v>
</v>
<v t="T755"><vh>fileCommands.open</vh>
<v t="T754" a="C"><vh>&lt;&lt; Set the default directory &gt;&gt;</vh></v>
</v>
<v t="T756"><vh>fileCommands.setAllJoinLinks</vh></v>
<v t="T757"><vh>xmlUnescape</vh></v>
</v>
<v t="T758"><vh>Writing</vh>
<v t="T759"><vh>assignFileIndices (no change from 3.11.1)</vh></v>
<v t="T760"><vh>compactFileIndices (changed from 3.11.1)</vh></v>
<v t="T761"><vh>put routines</vh>
<v t="T762"><vh>putClipboardHeader</vh>
<v t="T763"><vh>&lt;&lt; count the number of tnodes &gt;&gt;</vh></v>
</v>
<v t="T764"><vh>put (basic)(leoFileCommands)</vh></v>
<v t="T765"><vh>putEscapedString</vh></v>
<v t="T766"><vh>putFindSettings</vh>
<v t="T767"><vh>&lt;&lt; put find settings that may exist in leoConfig.txt &gt;&gt;</vh></v>
</v>
<v t="T768"><vh>putGlobals (changed for 4.0)</vh>
<v t="T769"><vh>&lt;&lt; put the body/outline ratio &gt;&gt;</vh></v>
<v t="T770"><vh>&lt;&lt; put the position of this frame &gt;&gt;</vh></v>
<v t="T771"><vh>&lt;&lt; put the position of the log window &gt;&gt;</vh></v>
</v>
<v t="T772"><vh>putHeader</vh></v>
<v t="T773"><vh>putLeoOutline (to clipboard) (no change from 3.11.1)</vh></v>
<v t="T774"><vh>putPrefs</vh>
<v t="T775"><vh>&lt;&lt; put prefs that may exist in leoConfig.txt &gt;&gt; (putPrefs)</vh>
<v t="T776"><vh>&lt;&lt; put default directory &gt;&gt;</vh></v>
</v>
</v>
<v t="T777"><vh>putProlog</vh>
<v t="T778"><vh>&lt;&lt; Put the &lt;?xml...?&gt; line &gt;&gt;</vh></v>
<v t="T779"><vh>&lt;&lt; Put the optional &lt;?xml-stylesheet...?&gt; line &gt;&gt;</vh></v>
</v>
<v t="T780"><vh>putPostlog</vh></v>
<v t="T781"><vh>putTnodes (reverted to 3.11.1)</vh>
<v t="T782"><vh>&lt;&lt; write only those tnodes that were referenced &gt;&gt;</vh></v>
</v>
<v t="T783"><vh>putTnode (no change from 3.11.1)</vh></v>
<v t="T784"><vh>putVnodes (reverted 3.11.1)</vh></v>
<v t="T785"><vh>putVnode (no change from 3.11.1) (generates error)</vh>
<v t="T786"><vh>&lt;&lt; Put tnode index if this vnode has body text &gt;&gt;</vh></v>
<v t="T787"><vh>&lt;&lt; Put attribute bits &gt;&gt;</vh></v>
<v t="T788"><vh>&lt;&lt; write the head text &gt;&gt;</vh></v>
</v>
</v>
<v t="T789"><vh>save</vh></v>
<v t="T790"><vh>saveAs</vh></v>
<v t="T791"><vh>saveTo</vh></v>
<v t="T792"><vh>setDefaultDirectoryForNewFiles</vh></v>
<v t="T793"><vh>xmlEscape</vh></v>
<v t="T794"><vh>writeAtFileNodes</vh></v>
<v t="T795"><vh>writeDirtyAtFileNodes</vh></v>
<v t="T796"><vh>writeMissingAtFileNodes</vh></v>
<v t="T797"><vh>writeOutlineOnly</vh></v>
<v t="T798"><vh>write_LEO_file</vh>
<v t="T799"><vh>&lt;&lt; create backup file &gt;&gt;</vh></v>
<v t="T800"><vh>&lt;&lt; delete backup file &gt;&gt;</vh></v>
<v t="T801"><vh>&lt;&lt; erase filename and rename backupName to fileName &gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="T802"><vh>leoNodes.py</vh>
<v t="T803"><vh>&lt;&lt; About clones &gt;&gt;</vh></v>
<v t="T804"><vh>&lt;&lt; About the vnode and tnode classes &gt;&gt;</vh></v>
<v t="T805"><vh>class tnode</vh>
<v t="T806"><vh>&lt;&lt; tnode constants &gt;&gt;</vh></v>
<v t="T807"><vh>t.__init__</vh></v>
<v t="T808"><vh>Getters</vh>
<v t="T809"><vh>hasBody</vh></v>
<v t="T810"><vh>loadBodyPaneFromTnode</vh></v>
<v t="T811"><vh>Status bits</vh>
<v t="T812"><vh>isDirty</vh></v>
<v t="T813"><vh>isRichTextBit</vh></v>
<v t="T814"><vh>isVisited</vh></v>
</v>
</v>
<v t="T815"><vh>Setters</vh>
<v t="T816"><vh>Setting body text</vh>
<v t="T817"><vh>saveBodyPaneToTnode</vh></v>
<v t="T818"><vh>setTnodeText</vh></v>
<v t="T819"><vh>setSelection</vh></v>
</v>
<v t="T820"><vh>Status bits</vh>
<v t="T821"><vh>clearDirty</vh></v>
<v t="T822"><vh>clearRichTextBit</vh></v>
<v t="T823"><vh>clearVisited</vh></v>
<v t="T824"><vh>setDirty</vh></v>
<v t="T825"><vh>setRichTextBit</vh></v>
<v t="T826"><vh>setVisited</vh></v>
</v>
<v t="T827"><vh>setCloneIndex</vh></v>
<v t="T828"><vh>setFileIndex</vh></v>
</v>
</v>
<v t="T829"><vh>class vnode</vh>
<v t="T830"><vh>&lt;&lt; vnode constants &gt;&gt;  ### Warning: changes meaning of visitedBit</vh></v>
<v t="T831"><vh>Birth &amp; death</vh>
<v t="T832"><vh>v.__cmp__ (not used)</vh></v>
<v t="T833"><vh>v.__init__</vh>
<v t="T834"><vh>&lt;&lt; initialize vnode data members &gt;&gt;</vh></v>
</v>
<v t="T835"><vh>v.__repr__ &amp; v.__str__</vh></v>
</v>
<v t="T836"><vh>v.Callbacks (handles event hooks)</vh>
<v t="T837"><vh>OnBoxClick</vh></v>
<v t="T838"><vh>OnDrag</vh></v>
<v t="T839"><vh>v.OnEndDrag</vh></v>
<v t="T840"><vh>v.OnHeadlineClick &amp; OnHeadlineRightClick</vh></v>
<v t="T841"><vh>OnHeadlineKey</vh></v>
<v t="T842"><vh>OnHyperLinkControlClick</vh></v>
<v t="T843"><vh>OnHyperLinkEnter</vh></v>
<v t="T844"><vh>OnHyperLinkLeave</vh></v>
<v t="T845"><vh>OnIconClick &amp; OnIconRightClick</vh></v>
<v t="T846"><vh>OnIconDoubleClick</vh></v>
</v>
<v t="T847"><vh>Comparisons (vnode)</vh>
<v t="T848"><vh>afterHeadlineMatch</vh></v>
<v t="T849"><vh>at/../NodeName</vh></v>
<v t="T850"><vh>isAt/../Node</vh></v>
<v t="T851"><vh>isAnyAtFileNode &amp; isAnyAtFileNodeName</vh></v>
<v t="T852"><vh>isAtIgnoreNode</vh></v>
<v t="T853"><vh>isAtOthersNode</vh></v>
<v t="T854"><vh>matchHeadline</vh></v>
</v>
<v t="T855"><vh>File Conversion (vnode)</vh>
<v t="T856"><vh>convertTreeToString</vh></v>
<v t="T857"><vh>moreHead</vh></v>
<v t="T858"><vh>v.moreBody</vh></v>
</v>
<v t="T859"><vh>Getters</vh>
<v t="T860"><vh>Children</vh>
<v t="T861"><vh>childIndex</vh></v>
<v t="T862"><vh>firstChild</vh></v>
<v t="T863"><vh>hasChildren</vh></v>
<v t="T864"><vh>lastChild</vh></v>
<v t="T865"><vh>nthChild</vh></v>
<v t="T866"><vh>numberOfChildren (n)</vh></v>
</v>
<v t="T867"><vh>Status Bits</vh>
<v t="T868"><vh>isCloned</vh></v>
<v t="T869"><vh>isDirty</vh></v>
<v t="T870"><vh>isExpanded</vh></v>
<v t="T871"><vh>isMarked</vh></v>
<v t="T872"><vh>isOrphan</vh></v>
<v t="T873"><vh>isSelected</vh></v>
<v t="T874"><vh>isTopBitSet</vh></v>
<v t="T875"><vh>isVisible</vh></v>
<v t="T876"><vh>isVisited</vh></v>
<v t="T877"><vh>status</vh></v>
</v>
<v t="T878"><vh>bodyString</vh></v>
<v t="T879"><vh>currentVnode (vnode)</vh></v>
<v t="T880"><vh>edit_text</vh></v>
<v t="T881"><vh>findRoot</vh></v>
<v t="T882"><vh>headString &amp; cleanHeadString</vh></v>
<v t="T883"><vh>isAncestorOf</vh></v>
<v t="T884"><vh>isRoot</vh></v>
<v t="T885"><vh>v.exists</vh></v>
</v>
<v t="T886"><vh>Setters</vh>
<v t="T887"><vh>Head and body text</vh>
<v t="T888"><vh>appendStringToBody</vh></v>
<v t="T889"><vh>setBodyStringOrPane &amp; setBodyTextOrPane</vh></v>
<v t="T890"><vh>setHeadString &amp; initHeadString</vh></v>
<v t="T891"><vh>setHeadStringOrHeadline</vh></v>
</v>
<v t="T892"><vh>computeIcon &amp; setIcon</vh></v>
<v t="T893"><vh>Status bits</vh>
<v t="T894"><vh>clearAllVisited</vh></v>
<v t="T895"><vh>clearAllVisitedInTree</vh></v>
<v t="T896"><vh>clearClonedBit</vh></v>
<v t="T897"><vh>clearDirty &amp; clearDirtyJoined (redundant code)</vh></v>
<v t="T898"><vh>clearMarked</vh></v>
<v t="T899"><vh>clearOrphan</vh></v>
<v t="T900"><vh>clearVisited</vh></v>
<v t="T901"><vh>clearVisitedInTree</vh></v>
<v t="T902"><vh>contract &amp; expand &amp; initExpandedBit</vh></v>
<v t="T903"><vh>initStatus</vh></v>
<v t="T904"><vh>setAncestorsOfClonedNodesInTreeDirty</vh></v>
<v t="T905"><vh>setAncestorAtFileNodeDirty</vh></v>
<v t="T906"><vh>setClonedBit &amp; initClonedBit</vh></v>
<v t="T907"><vh>setDirty, setDirtyDeleted &amp; initDirtyBit (redundant code)</vh></v>
<v t="T908"><vh>setMarked &amp; initMarkedBit</vh></v>
<v t="T909"><vh>setOrphan</vh></v>
<v t="T910"><vh>setSelected (vnode, new)</vh></v>
<v t="T911"><vh>setVisited</vh></v>
</v>
<v t="T912"><vh>setSelection</vh></v>
<v t="T913"><vh>setT</vh></v>
<v t="T914"><vh>trimTrailingLines</vh></v>
</v>
<v t="T915"><vh>Tree Traversal (vnode)</vh>
<v t="T916"><vh>back</vh></v>
<v t="T917"><vh>lastNode</vh></v>
<v t="T918"><vh>level</vh></v>
<v t="T919"><vh>next</vh></v>
<v t="T920"><vh>nodeAfterTree</vh></v>
<v t="T921"><vh>parent</vh></v>
<v t="T922"><vh>threadBack</vh></v>
<v t="T923"><vh>threadNext</vh></v>
<v t="T924"><vh>visBack</vh></v>
<v t="T925"><vh>visNext</vh></v>
</v>
<v t="T926"><vh>Moving, Inserting, Deleting, Cloning, Sorting (vnode)</vh>
<v t="T927"><vh>Entry Points (vnode)</vh>
<v t="T928"><vh>doDelete</vh></v>
<v t="T929"><vh>insertAfter</vh></v>
<v t="T930"><vh>insertAsLastChild</vh></v>
<v t="T931"><vh>insertAsNthChild</vh></v>
<v t="T932"><vh>moveToRoot</vh></v>
<v t="T933"><vh>restoreOutlineFromDVnodes (test)</vh></v>
<v t="T934"><vh>v.clone</vh></v>
<v t="T935"><vh>v.linkAfter</vh></v>
<v t="T936"><vh>v.linkAsNthChild</vh></v>
<v t="T937"><vh>v.linkAsRoot</vh></v>
<v t="T938"><vh>v.moveAfter</vh></v>
<v t="T939"><vh>v.moveToNthChildOf</vh></v>
<v t="T940"><vh>v.sortChildren</vh></v>
</v>
<v t="T941"><vh>Helper functions</vh>
<v t="T942"><vh>v.addTreeToJoinLists (new in 3.12 beta 2)</vh></v>
<v t="T943"><vh>v.cloneTree</vh></v>
<v t="T944"><vh>v.copyCloneBitsTo</vh></v>
<v t="T945"><vh>v.copyTree</vh></v>
<v t="T946"><vh>v.copyTreeWithNewTnodes (new after 3.11.1) (not used at present)</vh></v>
<v t="T947"><vh>v.createDependents</vh></v>
<v t="T948"><vh>v.destroyDependents</vh></v>
<v t="T949"><vh>v.destroyTree (does nothing!)(Called only from destroy dependents)</vh></v>
<v t="T950"><vh>v.invalidOutline</vh></v>
<v t="T951"><vh>v.joinNodeTo (rewritten for 4.0)</vh></v>
<v t="T952"><vh>v.joinTreeTo</vh></v>
<v t="T953"><vh>v.shouldBeClone</vh></v>
<v t="T954"><vh>v.unjoinTree</vh></v>
<v t="T955"><vh>v.unlink</vh></v>
<v t="T956"><vh>validateOutlineWithParent</vh>
<v t="T957"><vh>&lt;&lt; validate parent ivar &gt;&gt;</vh></v>
<v t="T958"><vh>&lt;&lt; validate childIndex ivar &gt;&gt;</vh></v>
<v t="T959"><vh>&lt;&lt; validate x ivar &gt;&gt;</vh></v>
</v>
</v>
</v>
</v>
</v>
</v>
<v t="T960"><vh>Unused code</vh>
<v t="T961"><vh>atFile.newRead</vh>
<v t="T962"><vh>&lt;&lt; init read vars &gt;&gt;</vh></v>
<v t="T963"><vh>&lt;&lt; open file &gt;&gt;</vh>
<v t="T964"><vh>&lt;&lt; warn on read-only file &gt;&gt;</vh></v>
</v>
<v t="T965"><vh>&lt;&lt; Scan the file buffer  &gt;&gt;</vh>
<v t="T966"><vh>&lt;&lt; unlink all children of root &gt;&gt;</vh></v>
</v>
<v t="T967"><vh>&lt;&lt; Bump mStructureErrors if any vnodes are unvisited &gt;&gt;</vh></v>
<v t="T968"><vh>&lt;&lt; quickly delete root's tree and body text &gt;&gt;</vh></v>
</v>
<v t="T969"><vh>oldScanDoc (no longer used)</vh>
<v t="T970"><vh>&lt;&lt; Skip the opening sentinel &gt;&gt;</vh></v>
<v t="T971"><vh>&lt;&lt; Skip an opening block delim &gt;&gt;</vh></v>
<v t="T972"><vh>&lt;&lt; Skip the leading stuff &gt;&gt;</vh></v>
<v t="T973"><vh>&lt;&lt; Append s to out &gt;&gt;</vh></v>
<v t="T974"><vh>&lt;&lt; Remove a closing block delim from out &gt;&gt;</vh></v>
</v>
</v>
<v t="T975" a="V"><vh>@file gnx_code.py</vh>
<v t="T976"><vh>functions called by hooks</vh>
<v t="T977"><vh>onAfterFinishCreate</vh></v>
<v t="T978"><vh>onCreateExtraMenus (will be part of leoFrame class eventually)</vh>
<v t="T979"><vh>&lt;&lt; extend the read/write submenu &gt;&gt;</vh></v>
<v t="T980"><vh>&lt;&lt; extend the export submenu &gt;&gt;</vh></v>
</v>
</v>
<v t="T981"><vh>Other classes, etc.</vh>
<v t="T982"><vh>app.setLeoID</vh>
<v t="T983"><vh>&lt;&lt; return if we can set self.leoID from sys.leoID&gt;&gt;</vh></v>
<v t="T984"><vh>&lt;&lt; return if we can set self.leoID from "leoID.txt" &gt;&gt;</vh></v>
<v t="T985"><vh>&lt;&lt; put up a dialog requiring a valid id &gt;&gt;</vh></v>
<v t="T986"><vh>&lt;&lt; attempt to create leoID.txt &gt;&gt;</vh></v>
</v>
<v t="T987"><vh>class askLeoID</vh>
<v t="T988"><vh>askLeoID.__init__</vh></v>
<v t="T989"><vh>askLeoID.createFrame</vh></v>
<v t="T990"><vh>onCloseWindow</vh></v>
<v t="T991"><vh>onButton</vh></v>
<v t="T992"><vh>onKey</vh>
<v t="T993"><vh>&lt;&lt; eliminate invalid characters &gt;&gt;</vh></v>
<v t="T994"><vh>&lt;&lt; enable the ok button if there are 4 or more valid characters &gt;&gt;</vh></v>
</v>
</v>
<v t="T995"><vh>class myFileCommands</vh>
<v t="T996"><vh>myFileCommands.__init__</vh></v>
<v t="T997"><vh>assignAllGnx</vh></v>
</v>
<v t="T998"><vh>class myFrame</vh>
<v t="T999"><vh>myFrame.__init__</vh></v>
<v t="T1000"><vh>OnClearAllNodeIndices</vh></v>
<v t="T1001"><vh>OnWriteGnxFile</vh></v>
<v t="T1002"><vh>OnReadGnxFile</vh></v>
<v t="T1003"><vh>OnWriteOldOutline (not used?)</vh></v>
</v>
<v t="T1004"><vh>class myTnode</vh>
<v t="T1005"><vh>myTnode.__init__</vh></v>
<v t="T1006"><vh>t.getGnx</vh></v>
</v>
<v t="T1007"><vh>class nodeIndices</vh>
<v t="T1008"><vh>nodeIndices.__init__</vh></v>
<v t="T1009"><vh>areEqual</vh></v>
<v t="T1010"><vh>get/setDefaultId</vh></v>
<v t="T1011"><vh>getNewIndex</vh></v>
<v t="T1012"><vh>scanGnx</vh></v>
<v t="T1013"><vh>setTimeString</vh></v>
<v t="T1014"><vh>toString</vh></v>
</v>
<v t="T1015"><vh>class myAtFile</vh>
<v t="T1016"><vh>myAtFile.__init__</vh></v>
<v t="T1017"><vh>scanHeader (compatible with 3.x and 4.x)</vh>
<v t="T1018"><vh>&lt;&lt; skip any non @+leo lines &gt;&gt;</vh></v>
<v t="T1019"><vh>&lt;&lt; make sure we have @+leo &gt;&gt;</vh></v>
<v t="T1020"><vh>&lt;&lt; read optional version param &gt;&gt;</vh></v>
<v t="T1021"><vh>&lt;&lt; read optional encoding param &gt;&gt;</vh></v>
<v t="T1022"><vh>&lt;&lt; set the closing comment delim &gt;&gt;</vh></v>
</v>
<v t="T1023" a="E"><vh>atFile.read (compatible with 3.x and 4.x)</vh>
<v t="T1024"><vh>&lt;&lt; set self.targetFileName &gt;&gt;</vh></v>
<v t="T1025"><vh>&lt;&lt; open file &gt;&gt;</vh>
<v t="T1026"><vh>&lt;&lt; warn on read-only file &gt;&gt;</vh></v>
</v>
<v t="T1027"><vh>&lt;&lt; Scan the file buffer  &gt;&gt;</vh></v>
<v t="T1028"><vh>&lt;&lt; Bump mStructureErrors if any vnodes are unvisited &gt;&gt;</vh></v>
<v t="T1029"><vh>&lt;&lt; quickly delete root's tree and body text &gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="T1030" a="E"><vh>class atFile2</vh>
<v t="T1031"><vh>&lt;&lt; how this code handles whitespace and newlines &gt;&gt;</vh></v>
<v t="T1032"><vh>atFile2.__init__</vh></v>
<v t="T1033" a="E"><vh>Top level</vh>
<v t="T1034"><vh>atFile2.readOpenFile</vh>
<v t="T1035"><vh>&lt;&lt; Scan the file buffer  &gt;&gt;</vh></v>
</v>
<v t="T1036"><vh>atFile2.newWrite</vh>
<v t="T1037"><vh>&lt;&lt; initialize &gt;&gt;</vh></v>
<v t="T1038"><vh>&lt;&lt; open the file; return on error &gt;&gt;</vh></v>
<v t="T1039"><vh>&lt;&lt; write then entire @file tree &gt;&gt;</vh></v>
<v t="T1040"><vh>&lt;&lt; Warn about @ignored and orphans  &gt;&gt;</vh></v>
<v t="T1041"><vh>&lt;&lt; finish writing &gt;&gt;</vh></v>
</v>
<v t="T1042"><vh>atFile2.closeWriteFile</vh></v>
</v>
<v t="T1043"><vh>Writing...</vh>
<v t="T1044"><vh>getAtFirstLastLines</vh></v>
<v t="T1045" a="E"><vh>putBody</vh>
<v t="T1046"><vh>&lt;&lt; handle line at s[i]  &gt;&gt;</vh></v>
</v>
<v t="T1047" a="E"><vh>code lines...</vh>
<v t="T1048"><vh>putAtOthersLine</vh></v>
<v t="T1049"><vh>putCodeLine</vh></v>
<v t="T1050"><vh>putRefLine</vh></v>
</v>
<v t="T1051" a="E"><vh>doc lines...</vh>
<v t="T1052"><vh>putStartDocLine</vh></v>
<v t="T1053" a="E"><vh>putDocLine</vh>
<v t="T1054"><vh>&lt;&lt; append words to pending line, splitting the line if needed &gt;&gt;</vh></v>
</v>
<v t="T1055"><vh>putEndDocLine</vh></v>
<v t="T1056"><vh>putPending</vh></v>
</v>
</v>
<v t="T1057"><vh>Utils...</vh>
<v t="T1058"><vh>hasSectionName</vh></v>
<v t="T1059"><vh>os, onl, etc.</vh></v>
<v t="T1060"><vh>directiveKind</vh></v>
</v>
<v t="T1061"><vh>Sentinels...</vh>
<v t="T1062"><vh>nodeSentinelText</vh>
<v t="T1063"><vh>&lt;&lt; remove comment delims from h if necessary &gt;&gt;</vh></v>
</v>
<v t="T1064"><vh>putCloseSentinels</vh></v>
<v t="T1065"><vh>putLeadInSentinel</vh></v>
<v t="T1066"><vh>putOpenLeoSentinel</vh></v>
<v t="T1067"><vh>putOpenNodeSentinel</vh></v>
<v t="T1068"><vh>putOpenSentinels</vh></v>
<v t="T1069"><vh>putSentinel (applies cweb hack)</vh>
<v t="T1070"><vh>&lt;&lt; apply the cweb hack to s &gt;&gt;</vh></v>
</v>
<v t="T1071"><vh>sentinelKind</vh></v>
<v t="T1072"><vh>skipSentinelStart</vh></v>
</v>
<v t="T1073" a="EM"><vh>Reading...</vh>
<v t="T1074"><vh>createChild: TO DO: create proper tnode using root.tnodeList</vh></v>
<v t="T1075" a="E"><vh>scanText &amp; allies</vh>
<v t="T1076"><vh>&lt;&lt; init ivars for scanText &gt;&gt;</vh></v>
<v t="T1077"><vh>&lt;&lt; report unexpected end of text &gt;&gt;</vh></v>
<v t="T1078"><vh>start sentinels</vh>
<v t="T1079" a="E"><vh>readStartAt, readStartDoc &amp; readStartDocLine</vh></v>
<v t="T1080"><vh>readStartLeo</vh></v>
<v t="T1081" a="E"><vh>readStartNode</vh>
<v t="T1082"><vh>&lt;&lt; Set headline, undoing the CWEB hack &gt;&gt;</vh></v>
<v t="T1083"><vh>&lt;&lt; Check the filename in the sentinel &gt;&gt;</vh></v>
</v>
<v t="T1084"><vh>readStartOthers</vh></v>
</v>
<v t="T1085"><vh>end sentinels</vh>
<v t="T1086"><vh>readEndAt &amp; readEndDoc</vh></v>
<v t="T1087"><vh>readEndLeo</vh></v>
<v t="T1088"><vh>readEndNode</vh></v>
<v t="T1089"><vh>readEndOthers</vh></v>
<v t="T1090" a="E"><vh>readLastDocLine</vh></v>
</v>
<v t="T1091" a="E"><vh>Unpaired sentinesl</vh>
<v t="T1092"><vh> readAfterRef</vh></v>
<v t="T1093"><vh>readComment</vh></v>
<v t="T1094"><vh>readDelims</vh></v>
<v t="T1095"><vh>readDirective</vh></v>
<v t="T1096"><vh>readNl</vh></v>
<v t="T1097"><vh>readNonl</vh></v>
<v t="T1098"><vh>readNormalLine</vh>
<v t="T1099"><vh>&lt;&lt; Skip the leading stuff &gt;&gt;</vh></v>
<v t="T1100"><vh>&lt;&lt; Append s to docOut &gt;&gt;</vh></v>
</v>
<v t="T1101"><vh>readRef</vh></v>
<v t="T1102"><vh>readVerbatim</vh></v>
<v t="T1103"><vh>readWs</vh></v>
</v>
<v t="T1104"><vh>badEndSentinel, push/popSentinelStack</vh></v>
<v t="T1105"><vh>getWsAfterIndentation (not used)</vh></v>
</v>
</v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="T1"></t>
<t tx="T2"></t>
<t tx="T3">@nocolor

This file contains code for all plugins distributed with Leo.</t>
<t tx="T4">@nocolor

What is a plugin?

A plugin is a .py file that appears in Leo's plugin subdirectory. Leo tries to
import all such files while starting up. This is done at "start1" time, that
is, in the call to doHook("start1") in the run function in leo.py. Plugins
exist to define "hook code".

What is hook code?

Leo automatically calls hook code at various times during Leo's execution.
Typical hooks are:

- "start2", called at the end of Leo's startup process,
- "command1", called before executing any of Leo's commands
- "idle", called at Tk's idle time, when nothing else is happening,

See the documentation for hooks in this file for full details.

N.B. Plugins can use "start2" hooks to override any of Leo's classes. See
"Overriding functions, methods &amp; classes" in leoPlugins.leo for several
examples of how to do this.

How do plugins work?

Plugins register themselves when Leo imports them using the following code,
which should appear as the outer level of the .py file:

@color

"""A description of this plugin"""

if 1: # 1 to enable the plugin, 0 to disable the plugin:
	registerHandler("xxx", onXXX)
	__version__ = "1.2"
	plugin_signon(__name__)
	
@nocolor

Line by line:

1) """A description of this plugin"""

This is a Python doc string describing the plugin. This string becomes the
value of the __name__ attribute for the module (.py file).

2) if 1: # 1 to enable the plugin, 0 to disable the plugin:

This line enables or disables the code that registers the plugin. Plugins do
nothing unless they are actually registered when Leo first imports them.

3) registerHandler("xxx", onXXX)

This line registers a handler called onXXX for the hook called "xxx". See the
documentation for hooks for a complete list of hook names that you can use
instead of "xxx". onXXX is the name of a function or method, presumably defined
in the plugin file, that Leo will call at "xxx" time. For example:

registerHandler("idle",onIdle)

will cause Leo to call the onIdle function at "idle" time.

You can pass a list of hook names as the first argument to registerHandler. For
example:

registerHandler(("bodykey1","bodykey2","headkey1","headkey2"), onKey)

4) __version__ = "1.2"

This assigns a version attribute to module. At present this attribute is used
by the plugin code that creates Leo's Plugins menu.

5) plugin_signon(__name__)

This line increases the count of loaded modules. The present code for
plugin_signon does not actually print separate signons--it seems to verbose.

About hook handlers

See the "About hooks" section of leoPlugins.leo for full documentation about
how to write hook handler routines, like onXXX or onKey in the examples above.
Basically, each hook should have this pattern:
	
@color

def onXXX (tag,keywords):
	c = keywords.get("c")
	otherKeyword = keywords.get("otherKeyword")
	&lt;&lt; do something with c and otherKeyword, etc. &gt;&gt;
	
@nocolor

In other words, keywords is a Python dictionary containing the keyword
arguments passed to the hook handler. See the See the "About hooks" section of
leoPlugins.leo for a list of the keywords passed to each hook handler.

The tag is the name of the hook. For example, tag would one of
"bodykey1","bodykey2","headkey1","headkey2", for the onKey hook handler in the
example above.

What's next?

It's one thing to know how to create a plugin. It's another to know how to
actually change Leo. Obviously, some study is needed. The place to start your
study is LeoPy.leo. In particular, study very carefully the section called
"Overview of code". Leo is a highly modular program, and Python is ideally
suited to this style of programming.</t>
<t tx="T5">@nocolor

Scripting is fully documented in Leo's Users Guide, and the following should be enough to get you started:

@color

top() # The commander of the top (current) windows.
top().rootVnode() # The root vnode of the outline.
top().currentVnode() # The presently selected vnode.

@nocolor

If v is any vnode:
	
@color

v.headString() # is the headline of v.
v.bodyString() # is the body of v.
v.threadNext() # is node after v in outline order.

@nocolor

For example, this prints every headline of an outline:
	
@color

v = top().rootVnode()
while v:
	print v.headString()
	v = v.threadNext()
</t>
<t tx="T6">At startup time Leo looks all files of the form mod_*.py in the plugins
directory. Leo assumes that these files are "plugins" containing Python modules
that customizes Leo's operation. Leo attempts to import each file.

Each module should register routines that are called at various times during
execution. Such times are identified by strings known as "tags". The code in in
one or more plugins corresponding to each tag are known as the "hook" routines
for that tag. Leo catches exceptions (including syntax errors) in hook
routines, so it is safe to hack away on this code.

Leo passes two argument to all hook routines: the tag and a keywords dictionary
containing additional information. For example, keywords["label"] indicates the
kind of command for "command1" and "command2" hooks.

For some hooks, returning anything other than None "overrides" Leo's default
action. Hooks have full access to all of Leo's source code. Just import the
relevant file. For example, top() returns the commander for the topmost Leo
window.

The following table summarizes the arguments passed to hooks: ( Overrides is
"yes" if returning anything other than None overrides Leo's normal command or
event processing.)

tag argument                                              keys in keywords
(hook name)  overrides       when called                  dictionary argument
---------    ---------       -----------                  -------------------
"bodyclick1"   yes      before normal click in body       c,v,event 
"bodyclick2"            after  normal click in body       c,v,event 
"bodydclick1"  yes      before double click in body       c,v,event 
"bodydclick2"           after  double click in body       c,v,event 
"bodykey1"     yes      before body keystrokes            c,v,ch,oldSel,undoType
"bodykey2"              after  body keystrokes            c,v,ch,oldSel,undoType
"bodyrclick1"  yes      before right click in body        c,v,event 
"bodyrclick2"           after  right click in body        c,v,event 
"boxclick1"    yes      before click in +- box            c,v,event 
"boxclick2"             after  click in +- box            c,v,event 
"command1"     yes      before each command               c,v,label (note 2)
"command2"              after  each command               c,v,label (note 2)
"drag1"        yes      before start of drag              c,v,event 
"drag2"                 after  start of drag              c,v,event 
"dragging1"    yes      before continuing to drag         c,v,event 
"dragging2"             after  continuing to drag         c,v,event 
"end1"                  start of app.quit()
"enddrag1"     yes      before end of drag                c,v,event 
"enddrag2"              after  end of drag                c,v,event 
"headkey1"     yes      before headline keystrokes        c,v,ch
"headkey2"              after  headline keystrokes        c,v,ch
"headclick1"   yes      before normal click in headline   c,v,event 
"headclick2"            after  normal click in headline   c,v,event 
"headrclick1"  yes      before right click in headline    c,v,event 
"headrclick2"           after  right click in headline    c,v,event 
"hypercclick1" yes      before control click in hyperlink c,v,event 
"hypercclick2"          after  control click in hyperlink c,v,event 
"hyperenter1"  yes      before entering hyperlink         c,v,event 
"hyperenter2"           after  entering hyperlink         c,v,event 
"hyperleave1"  yes      before leaving  hyperlink         c,v,event 
"hyperleave2"           after  leaving  hyperlink         c,v,event 
"iconclick1"   yes      before single click in icon box   c,v,event 
"iconclick2"            after  single click in icon box   c,v,event 
"iconrclick1"  yes      before right click in icon box    c,v,event 
"iconrclick2"           after  right click in icon box    c,v,event 
"icondclick1"  yes      before double click in icon box   c,v,event 
"icondclick2"           after  double click in icon box   c,v,event 
"idle"                  periodically (at idle time)       c,v
"menu1"        yes      before creating menus             c,v (note 3)
"menu2"        yes      before updating menus             c,v
"new"          no       during New command                old_c,new_c
"open1"        yes      before opening any file           old_c,new_c,fileName (note 4)
"open2"                 after  opening any file           old_c,new_c,fileName (note 4)
"openwith1"    yes      before Open With command          c,v,openType,arg,ext
"openwith2"             after  Open With command          c,v,openType,arg,ext
"recentfiles1" yes      before Recent Files command       c,v,fileName,closeFlag
"recentfiles2"          after  Recent Files command       c,v,fileName,closeFlag
"save1"        yes      before any Save command           c,v,fileName
"save2"                 after  any Save command           c,v,fileName
"select1"      yes      before selecting a vnode          c,new_v,old_v
"select2"               after  selecting a vnode          c,new_v,old_v
"start1"       no       after app.finishCreate()
"start2"                after opening first Leo window    c,v,fileName
"unselect1"    yes      before unselecting a vnode        c,new_v,old_v 
"unselect2"             after  unselecting a vnode        c,old_v,old_v 
"@url1"        yes      before double-click @url node     c,v (note 5)
"@url2"                 after  double-click @url node     c,v (note 5)

The following hooks are a new breed of hook, called "stub hooks". Conceptually,
these hooks are like calls to stub routines that can be filled in by code in
plugins.

tag argument                                                   keys in keywords
(hook name)             overrides    when called               dictionary argument
---------               ---------    -----------               -------------------

"create-optional-menus"  no          (note 8)                  (note 8)

"draw-outine-box"        yes         start of drawBox          tree,v,x,y (note 6)
"draw-outline-icon"      yes         start of tree.drawIcon    tree,v,x,y (note 6)
"draw-outline-node"      yes         start of tree.drawNode    tree,v,x,y (note 6)
"draw-outline-text-box"  yes         start of tree.drawText    tree,v,x,y (note 6)
"draw-sub-outline"       yes         start of tree.drawTree    tree,v,x,y,h,level (note 6)
"redraw-entire-outline"  yes         start of tree.redraw      c (note 6)

"color-optional-markup"  yes *       (note 7)                  colorer,v (note 7)
"init-color-markup"      no          (note 7)                  colorer,v,s,i,j,colortag (note 7)

"new"                    no          start of New command      old_c,new_c (note 9)

"scan-directives"        no          in scanDirectives         c,v,s,old_dict,dict,pluginsList (note 10)

Notes:

(1) "activate" and "deactivate" hooks: These have been removed because they do
not work as expected.

(2) "commands" hooks: The label entry in the keywords dict contains the
"canonicalized" form of the command, that is, the lowercase name of the command
with all non-alphabetic characters removed.

Commands hooks now set the label for undo and redo commands "undo" and "redo"
rather than "cantundo" and "cantredo".

(3) "menu1" hook: Setting app().realMenuNameDict in this hook is an easy way of
translating menu names to other languages. Note: the "new" names created this
way affect only the actual spelling of the menu items, they do _not_ affect how
you specify shortcuts in leoConfig.txt, nor do they affect the "official"
command names passed in app().commandName. For example, suppose you set
app().realMenuNameDict["Open..."] = "Ouvre".

(4) "open1" and "open2" hooks: These are called with a keywords dict containing
the following entries:

old_c: The commander of the previously open window.
new_c: The commander of the newly opened window.
fileName: The name of the file being opened.

You can use old_c.currentVnode() and new_c.currentVnode() to get the current
vnode in the old and new windows.

Leo calls the "open1" and "open2" hooks only if the file is already open.
Leo will also call the "open1" and "open2" hooks if:
a) a file is opened using the Recent Files menu and
b) the file is not already open.

(5) "@url1" and "@url2" hooks are only executed if "icondclick1" hook returns
None.

(6) These stub hooks allow plugins to revise or completely replace how Leo
draws outlines. For example, you could change tree.drawIcon to add additional
icons. These stub hooks are really methods of the leoTree class, with the
"tree" keyword corresponding to the "self" parameter. These stub hooks are
called at the beginning of the indicated method. See the method themselves for
a description of the paramters.

(7) These stub hooks allow plugins to parse and handle markup withing doc
parts, comments and Python """ strings. Note that these hooks are _not_ called
in Python ''' strings. See the color_markup plugin for a complete example of
how to use these hooks.

(8) The "create-optional-menus" stub hook is called when Leo is creating menus,
at the place at which creating new menus is appropriate. Therefore, this hook
need only create new menus in the correct order, without worrying about the
placement of the menus in the menu bar. See the plugins_menu and scripts_menu
plugins for examples of how to use this hook. Leo now executes hooks in
alphabetical order, so that the Plugins menu will be created before the Scripts
menu.

(9) The "new" stub hook is called at the beginning of the code that implements
the New command. This provides a much easier way of recognizing when Leo is
about to create a new Leo window.

(10) The "scan-directives" stub hooks is called inside the scanDirectives
global function. The dictionary returned by scanDirectives now contains an item
whose key is "pluginsList". The value of this item is a list of tuples
(d,v,s,k) where:

- d is the spelling of the @directive, without the leading @.
- v is the vnode containing the directive, _not_ the original vnode.
- s[k:] is a string containing whatever follows the @directive. k has already
been moved past any whitespace that follows the @directive.

See the add_directives plugins directive for a complete example of how to use
the "scan-directives" stub hook.</t>
<t tx="T7">Naively using hooks can expose you and your .leo files to malicious attacks.

** Hooks should never blindly execute Python scripts in .leo files.

It is safe to import and execute code from Leo itself, provided that you got Leo from Leo's SourceForge site.</t>
<t tx="T8">@color
@ WARNING ***** Using the following routine exposes you malicious code in .leo files! *****

Do not EVER use code that blindly executes code in .leo files!
Someone could send you malicious code embedded in the .leo file.

WARNING 1: Changing "@onloadpythonscript" to something else will NOT protect
           you if you EVER share either your files with anyone else.

WARNING 2: Replacing exec by rexec below provides NO additional protection!
           A malicious rexec script could trash your .leo file in subtle ways.
@c
if 0: # WRONG: This blindly execute scripts found in an .leo file! NEVER DO THIS!
	def onLoadFile():
		v = top().rootVnode()
		while v:
			h = v.headString().lower()
			if match_word(h,0,"@onloadpythonscript"):
				s = v.bodyString()
				if s and len(s) &gt; 0:
					try: # SECURITY BREACH: s may be malicious!
						exec s + '\n' in {}
					except:
						es_exception()
			v = v.threadNext()</t>
<t tx="T9">@ It is usually best not to catch exceptions in plugins.  doHook catches all exceptions and disables further calls to plugins.
@c

@ignore
</t>
<t tx="T10">@nocolor</t>
<t tx="T11">- (done) Make sure the selected node is visible.
- (done) Force the focus to the body pane after undo/redo so the selection is visible.

- Bind Fkeys to buttons.
- Is there a problem with "__init__" ?
- words like "and" aren't in the dictionary?????
</t>
<t tx="T12"></t>
<t tx="T13"></t>
<t tx="T14">"""Import cisco configuration files"""

from leoPlugins import *
from leoGlobals import *
import tkFileDialog

&lt;&lt; about this plugin &gt;&gt;
@others

if 0:
	registerHandler(("start2","open2","command2"), create_import_cisco_menu)
	
	__version__ = "1.3" # Set version for the plugin handler.
	plugin_signon(__name__)
</t>
<t tx="T15">@ This plugin adds a menu item under the File-&gt;Import menu to import
Cisco configuration files.

The plugin will:

1) create a new node, under the current node, where the configuration will be
written. This node will typically have references to several sections (see below).

2) create sections (child nodes) for the indented blocks present in the original
config file. These child nodes will have sub-nodes grouping similar blocks (e.g.
there will be an 'interface' child node, with as many sub-nodes as there are real
interfaces in the configuration file).

3) create sections for the custom keywords specified in the customBlocks[] list in
importCiscoConfig(). You can modify this list to specify different keywords. DO
NOT put keywords that are followed by indented blocks (these are taken care of by
point 2 above). The negated form of the keywords (for example, if the keyword is
'service', the negated form is 'no service') is also included in the sections.

4) not display consecutive empty comment lines (lines with only a '!').

All created sections are alphabetically ordered.

Feedback on this plugin can be sent to Davide Salomoni (dsalomoni@yahoo.com).
</t>
<t tx="T16">def create_import_cisco_menu(tag, keywords):
	if	(tag=="open2" or
		(tag=="start2" and not keywords.has_key('c')) or
		(tag=="command2" and keywords.get("label")=="new")):

		c = top()
		importMenu = c.frame.getMenu('import')
		newEntries = (
			("-", None, None),
			("Import C&amp;isco Configuration", "Shift+Ctrl+I", importCiscoConfig))
		
		c.frame.createMenuEntries(importMenu, newEntries)</t>
<t tx="T17">def importCiscoConfig(event=None):
	c = top(); current = c.currentVnode()
	if current == None: return
	&lt;&lt; open file &gt;&gt;

	# define which additional child nodes will be created
	# these keywords must NOT be followed by indented blocks
	customBlocks = ['aaa','ip as-path','ip prefix-list','ip route',
					'ip community-list','access-list','snmp-server','ntp',
					'boot','service','logging']
	out = []
	blocks = {}
	children = []
	lines = len(linelist)
	i = 0
	skipToNextLine = 0
	# create level-0 and level-1 children
	while i&lt;(lines-1):
		for customLine in customBlocks:
			if (linelist[i].startswith(customLine) or
				linelist[i].startswith('no %s' % customLine)):
				&lt;&lt; process custom line &gt;&gt;
				skipToNextLine = 1
				break
		if skipToNextLine:
			skipToNextLine = 0
		else:
			if linelist[i+1].startswith(' '):
				&lt;&lt; process indented block &gt;&gt;
			else:
				out.append(linelist[i])
		i=i+1
	# process last line
	out.append(linelist[i])
	
	&lt;&lt; complete outline &gt;&gt;</t>
<t tx="T18">name = tkFileDialog.askopenfilename(
	title="Import Cisco Configuration File",
	filetypes=[("All files", "*")]
	)
if name == "":	return

v = current.insertAsNthChild(0)
c.beginUpdate()
v.setHeadString("cisco config: %s" % name)
c.endUpdate()

try:
	fh = open(name)
	es("importing: %s" % name)
	linelist = fh.read().splitlines()
	fh.close()
except IOError,msg:
	es("error reading %s: %s" % (name, msg))
	return</t>
<t tx="T19">if not blocks.has_key(customLine):
	blocks[customLine] = []
	out.append(angleBrackets(customLine))
	# create first-level child
	child = v.insertAsNthChild(0)
	child.setHeadStringOrHeadline(angleBrackets(customLine))
	children.append(child)

blocks[customLine].append(linelist[i])</t>
<t tx="T20">space = linelist[i].find(' ')
if space == -1:
	space = len(linelist[i])
key = linelist[i][:space]
if not blocks.has_key(key):
	blocks[key] = []
	out.append(angleBrackets(key))
	# create first-level child
	child = v.insertAsNthChild(0)
	child.setHeadStringOrHeadline(angleBrackets(key))
	children.append(child)

value = [linelist[i]]
# loop through the indented lines
i = i+1
try:
	while linelist[i].startswith(' '):
		value.append(linelist[i])
		i = i+1
except:
	# EOF
	pass
i = i-1 # restore index
# now add the value to the dictionary
blocks[key].append(value)</t>
<t tx="T21"># first print the level-0 text
outClean = []
prev = ''
for line in out:
	if line=='!' and prev=='!':
		pass # skip repeated comment lines
	else:
		outClean.append(line)
	prev = line
v.setBodyStringOrPane('\n'.join(outClean))

# scan through the created outline and add children
for child in children:
	# extract the key from the headline. Uhm... :)
	key = child.headString().split('&lt;&lt;'
		)[1].split('&gt;&gt;')[0].strip()
	if blocks.has_key(key):
		if type(blocks[key][0]) == type(''):
			# it's a string, no sub-children, so just print the text
			child.setBodyStringOrPane('\n'.join(blocks[key]))
		else:
			# it's a multi-level node
			for value in blocks[key]:
				# each value is a list containing the headline and then the text
				subchild = child.insertAsNthChild(0)
				subchild.setHeadStringOrHeadline(value[0])
				subchild.setBodyStringOrPane('\n'.join(value))
		child.sortChildren()
	else:
		# this should never happen
		es("Unknown key: %s" % key)
v.sortChildren()</t>
<t tx="T22">@ignore
@language plain
@comment !
@ This node has an example of a flat configuration file (i.e. just the output of a 
'show running' command on a cisco router), and of the same configuration file 
imported by the plugin.
</t>
<t tx="T23">rpr1#sh runn    
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
<t tx="T24">rpr1#sh runn    
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
<t tx="T25">access-list 173 deny   ip 224.0.0.0 31.255.255.255 any
access-list 173 permit ip any any</t>
<t tx="T26">boot system flash rsp-k3pv-mz.120-21.S4.bin
boot system flash rsp-pv-mz.120-21.S1.bin
boot bootldr bootflash:rsp-boot-mz.120-11.S3</t>
<t tx="T27"></t>
<t tx="T28">controller E1 5/0/0
 framing NO-CRC4 
 clock source internal
 channel-group 1 timeslots 1
 channel-group 2 timeslots 2</t>
<t tx="T29">controller E1 5/0/1
 framing NO-CRC4 
 channel-group 0 timeslots 1</t>
<t tx="T30">controller SONET 1/0/0
 framing sdh</t>
<t tx="T31"></t>
<t tx="T32">interface Async1
 no ip address
 no ip directed-broadcast
 async mode interactive
 no peer default ip address</t>
<t tx="T33">interface Dialer0
 no ip address
 no ip directed-broadcast
 pulse-time 0
 no cdp enable</t>
<t tx="T34">interface FastEthernet0/0/0
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
<t tx="T35">interface FastEthernet0/0/1
 description **trunk link**
 no ip address
 no ip directed-broadcast
 no ip route-cache distributed
 no ip mroute-cache
 full-duplex</t>
<t tx="T36">interface FastEthernet0/0/1.1
 encapsulation dot1Q 25
 ip address 192.168.25.1 255.255.255.252
 no ip directed-broadcast</t>
<t tx="T37">interface FastEthernet0/0/1.2
 no ip directed-broadcast</t>
<t tx="T38">interface FastEthernet0/0/1.3
 encapsulation dot1Q 3
 ip address 192.168.4.1 255.255.255.252
 ip access-group 173 in
 no ip directed-broadcast
 ip pim sparse-mode</t>
<t tx="T39">interface FastEthernet0/0/1.5
 encapsulation dot1Q 5
 ip address 192.168.5.1 255.255.255.252
 no ip directed-broadcast</t>
<t tx="T40">interface FastEthernet0/0/1.50
 description to KPN-test
 encapsulation dot1Q 50
 ip address 192.168.40.1 255.255.255.252
 no ip directed-broadcast</t>
<t tx="T41">interface Loopback0
 ip address 192.168.20.1 255.255.255.255
 no ip directed-broadcast</t>
<t tx="T42">interface POS4/1/0
 no ip address
 no ip directed-broadcast
 no ip route-cache distributed
 no ip mroute-cache
 loopback internal</t>
<t tx="T43">interface Serial5/0/0:1
 ip address 10.31.9.1 255.255.255.252
 no ip directed-broadcast
 no ip route-cache distributed</t>
<t tx="T44">interface Serial5/0/0:2
 ip address 10.10.10.1 255.255.255.252
 no ip directed-broadcast
 no ip route-cache distributed</t>
<t tx="T45">interface Serial5/0/1:0
 ip address 10.31.9.5 255.255.255.252
 no ip directed-broadcast
 no ip route-cache distributed</t>
<t tx="T46">interface Serial5/1/0
 no ip address
 no ip directed-broadcast
 no ip route-cache distributed
 no ip mroute-cache
 shutdown
 framing g751
 dsu bandwidth 34010</t>
<t tx="T47">interface Serial5/1/1
 ip address 192.168.6.1 255.255.255.252
 no ip directed-broadcast
 encapsulation frame-relay IETF
 no ip route-cache distributed
 no ip mroute-cache
 loopback local
 framing g751
 dsu bandwidth 34010</t>
<t tx="T48">ip community-list 1 permit 65001:1
ip community-list 100 permit 65001:3</t>
<t tx="T49">ip route 0.0.0.0 0.0.0.0 192.168.3.2 tag 3</t>
<t tx="T50"></t>
<t tx="T51">line aux 0
 transport input all
 stopbits 1
 flowcontrol hardware</t>
<t tx="T52">line vty 0 4
 exec-timeout 0 0
 password 7 somepassword
 logging synchronous
 login
 length 0</t>
<t tx="T53">logging buffered 100000 debugging
logging facility local6
logging 10.10.10.1</t>
<t tx="T54">ntp clock-period 17179348
ntp update-calendar
ntp peer 192.168.3.2 prefer</t>
<t tx="T55"></t>
<t tx="T56">route-map only permit 2
 match community 65001:2
 set origin igp</t>
<t tx="T57">route-map only1 permit 10
 match community 1 65001:1
 set origin igp</t>
<t tx="T58">route-map only3 permit 10
 match community 100</t>
<t tx="T59">route-map tag_com permit 10
 match tag 1
 set community 65001:1</t>
<t tx="T60">route-map tag_com permit 20
 match tag 3
 set community 65001:3</t>
<t tx="T61"></t>
<t tx="T62">router bgp 65001
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
<t tx="T63">router ospf 1
 log-adjacency-changes
 passive-interface FastEthernet0/0/0
 network 192.168.3.1 0.0.0.0 area 0
 network 192.168.4.0 0.0.0.3 area 0</t>
<t tx="T64">no service pad
service timestamps debug datetime localtime show-timezone
service timestamps log datetime localtime show-timezone
service password-encryption
no service single-slot-reload-enable</t>
<t tx="T65">"""Modify the way exported outlines are displayed"""

from leoPlugins import *
from leoGlobals import *

def onStart (tag,keywords):
	import leoNodes
	funcToMethod(newMoreHead,leoNodes.vnode,"moreHead")

@others

if 0: # Register the handlers...
	registerHandler("start2", onStart)
	
	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)</t>
<t tx="T66"># Returns the headline string in MORE format.

def newMoreHead (self,firstLevel,useVerticalBar=true):

	useVerticalBar = true # Force the vertical bar

	v = self
	level = self.level() - firstLevel
	if level &gt; 0:
		if useVerticalBar:
			s = " |\t" * level
		else:
			s = "\t"
	else:
		s = ""
	s += choose(v.hasChildren(), "+ ", "- ")
	s += v.headString()
	return s
</t>
<t tx="T67"></t>
<t tx="T68">"""Dump globals at startup"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("start2", onStart)

	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T69">def onStart (tag,keywords):

	print "\nglobals..."
	for s in globals():
		if s not in __builtins__:
			print s
	
	print "\nlocals..."
	for s in locals():
		if s not in __builtins__:
			print s
</t>
<t tx="T70">"""Enable debugging for garbage collector"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("start2", onStart)
	
	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T71">def onStart (tag,keywords):

	try:
		import gc
		gc.set_debug(gc.DEBUG_LEAK)
	except: pass</t>
<t tx="T72">"""Trace changes to objects at idle time"""

from leoPlugins import *
from leoGlobals import *

count = 0

def printIdleRefs(tag,keywords):
	printGcRefs(verbose=false)

def printIdleGC(tag,keywords):
	
	# Calling printGc is too expensive to do on every idle call.
	# Note: printGc only works if debugGc is true in leoGlobals.py.
	# At present, this code does _not_ set that constant.
	if tag == "idle":
		global count ; count += 1
		if (count % 20) == 0:
			# collectGarbage() # Has no effect.
			printGc(tag,onlyPrintChanges=true)
	else:
		printGc(tag,onlyPrintChanges=false)
		
if 0:
	registerHandler("command2", printIdleRefs)

if 0: # Register the handlers...
	if 1: # Very effective.
		registerHandler("idle", printIdleGC)
	else: # Very precise.
		registerHandler("all", printIdleGC)
	
	__version__ = "1.2"
	plugin_signon(__name__)
</t>
<t tx="T73">"""Trace keystrokes in the outline and body panes"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler(("bodykey1","bodykey2","headkey1","headkey2"), onKey)
	
	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T74">def onKey (tag,keywords):

	ch = keywords.get("ch")
	if ch and len(ch) &gt; 0:
		es("key",`ch`)</t>
<t tx="T75">"""Trace most comment events, but not key, drag or idle events"""

from leoPlugins import *
from leoGlobals import *

tagCount = 0

@others

if 0: # Register the handlers...
	registerHandler("all", trace_tags)

	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)
</t>
<t tx="T76">def trace_tags (tag,keywords):
	
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
				print</t>
<t tx="T77"></t>
<t tx="T78">"""Support new @direcives"""

from leoPlugins import *
from leoGlobals import *

if 1:
	directives = "markup", # A tuple with one string.
else:
	directives = ("markup","markup2")
	
@others

if 1: # Register the handlers...

	registerHandler("start1",addPluginDirectives)
	registerHandler("scan-directives",scanPluginDirectives)
	
	__version__ = "1.1"
	plugin_signon(__name__)</t>
<t tx="T79">def addPluginDirectives (tag,keywords):
	
	"""Add all new directives to globalDirectivesList"""
	
	global directives

	if 0:
		s = ""
		for d in directives:
			s += '@' + d + ' '
		es(s,color="blue")

	for d in directives:
		if d not in globalDirectiveList:
			globalDirectiveList.append(d)</t>
<t tx="T80">def scanPluginDirectives (tag, keywords):
	
	"""Add a tuple (d,v,s,k) to list for every directive d found"""
	
	global directives

	keys = ("c","v","s","old_dict","dict","pluginsList")
	c,v,s,old_dict,dict,pluginsList = [keywords.get(key) for key in keys]

	for d in directives:
		if not old_dict.has_key(d) and dict.has_key(d):
			# Point k at whatever follows the directive.
			k = dict[d]
			k += 1 + len(d) # Skip @directive
			k = skip_ws(s,k) # Skip whitespace
			# trace(`d`,`k`)
			pluginsList.append((d,v,s,k),)
</t>
<t tx="T81"></t>
<t tx="T82">"""Handle coloring for markup in doc parts and Python triple-double-quoted strings"""

from leoPlugins import *
from leoGlobals import *
import string  # zfill does not exist in Python 2.2.1

@others

if 1: # Register the handlers...

	registerHandler("color-optional-markup", colorWikiMarkup)
	registerHandler("init-color-markup", initAnyMarkup)

	__version__ = "1.1"
	plugin_signon(__name__)</t>
<t tx="T83">def initAnyMarkup (tag,keywords):
	
	"""initialize colorer.markup_string
	
	The colorer completely recolors the body pane when this changes"""
	
	keys = ("colorer","v")
	colorer,v = [keywords.get(key) for key in keys]

	c = colorer.commands
	if not c or not v or not top(): return

	# trace()
	dict = scanDirectives(c,v=v) # v arg is essential.
	pluginsList = dict.get("pluginsList")
	
	if pluginsList:
		for d,v,s,k in pluginsList:
			if d == "markup":
				kind = s[k:]
				if kind:
					colorer.markup_string = kind
					return
					
	colorer.markup_string = "unknown" # default</t>
<t tx="T84">colorCount = 0

def colorWikiMarkup (tag,keywords):

	keys = ("colorer","v","s","i","j","colortag")
	colorer,v,s,i,j,colortag = [keywords.get(key) for key in keys]

	global colorCount ; colorCount += 1
	
	c = colorer.commands
	dict = scanDirectives(c,v=v) # v arg is essential.
	pluginsList = dict.get("pluginsList")
	
	if pluginsList:
		for d,v,s2,k in pluginsList:
			if d == "markup":
				# trace(`colorCount`,`d`)
				if match_word(s2,k,"wiki"):
					doWikiText(colorer,v,s,i,j,colortag)
					return true # We have colored the text.
			
	# trace(`colorCount`,"no markup")
	return None # We have not colored the text.</t>
<t tx="T85">def doWikiText (colorer,v,s,i,end,colortag):

	firsti = i ; inserted = 0

	while i &lt; end:
		&lt;&lt; set first to a tuple describing the first tag to be handled &gt;&gt;
		if first:
			tag,n1,n2,delim1,delim2 = first
			i = n2 + len(delim2)
			&lt;&lt; handle the tag using n1,n2,delim1,delim2 &gt;&gt;
		else: i = end
		
	colorer.tag(colortag,firsti,end+inserted)</t>
<t tx="T86">first = None

for tag,delim1,delim2 in (
	("bold","__","__"),
	("italic","''","''"),
	("picture","{picture file=","}"),
	("color","~~","~~")):
	n1 = s.find(delim1,i,end)
	if n1 &gt; -1:
		n2 = s.find(delim2,n1+len(delim1),end)
		if n2 &gt; -1:
			if not first or (first and n1 &lt; first[1]):
				first = tag,n1,n2,delim1,delim2
</t>
<t tx="T87">if tag =="picture":
	colorer.tag("elide",n1,n2+len(delim2)) # Elide everything.
	filename = s[n1+len(delim1):n2]
	filename = os.path.join(app().loadDir,filename)
	filename = os.path.normpath(filename)
	inserted += insertWikiPicture(colorer,filename,n2+len(delim2))
elif tag == "color":
	&lt;&lt; parse and handle color field &gt;&gt;
else:
	# look for nested bold or italic.
	if tag == "bold":
		delim3,delim4 = "''","''" # Look for nested italic.
	else:
		delim3,delim4 = "__","__" # Look for nested bold.
	n3 = s.find(delim3,n1+len(delim1),n2) ; n4 = -1
	if n3 &gt; -1:
		n4 = s.find(delim4,n3+len(delim3),n2+len(delim2))
	if n3 &gt; -1 and n4 &gt; -1:
		colorer.tag("elide",n1,n1+len(delim1))
		colorer.tag("elide",n2,n2+len(delim2))
		colorer.tag("elide",n3,n3+len(delim3))
		colorer.tag("elide",n4,n4+len(delim4))
		colorer.tag(tag,n1+len(delim1),n3)
		colorer.tag("bolditalic",n3+len(delim3),n4)
		colorer.tag(tag,n4+len(delim4),n2)
	else:
		# No nested tag.
		colorer.tag("elide",n1,n1+len(delim1))
		colorer.tag("elide",n2,n2+len(delim2))
		colorer.tag(tag,n1+len(delim1),n2)</t>
<t tx="T88"># Parse the color value.
j = n1+len(delim1)
n = s.find(":",j,n2)
if n2 &gt; n &gt; j &gt; -1:
	name = s[j:n]
	if name[0] == '#' and len(name) &gt; 1:
		name = '#' + string.zfill(name[1:],6)
	if name in colorer.color_tags_list:
		colorer.tag("elide",n1,n+1)
		colorer.tag(name,n+1,n2)
		colorer.tag("elide",n2,n2+len(delim2))
	else:
		try:
			# print "entering", name
			colorer.body.tag_configure(name,foreground=name)
			colorer.color_tags_list.append(name)
			colorer.tag("elide",n1,n+1)
			colorer.tag(name,n+1,n2)
			colorer.tag("elide",n2,n2+len(delim2))
		except: # an invalid color name: elide nothing.
			pass # es_exception()</t>
<t tx="T89">def insertWikiPicture (colorer,filename,i):
	
	"""Try to insert a picture with the give filename.
	
	Returns the number of characters actually inserted"""
	
	# trace(`colorer.color_pass`)
	if colorer.color_pass == 0:
		colorer.redoColoring = true # schedule a two-pass recoloring.
		return 0
		
	if colorer.color_pass == 2:
		return 0 # The second redo pass.
		
	# trace(`filename`,`v`)
	if not os.path.exists(filename):
		return 0

	try:
		# Create the image
		photo = Tkinter.PhotoImage(master=app().root, file=filename)
		image = colorer.body.image_create(colorer.index(i),image=photo,padx=0)
		
		# Keep references so images stay on the canvas.
		colorer.image_references.append((photo,image,colorer.line_index,i),)
		return 1
	except:
		es_exception()
		return 0</t>
<t tx="T90">"""Handle images in body text"""

from leoPlugins import *
from leoGlobals import *

@others

if 1: # Register the handlers...
	registerHandler("select2", onSelect)
	registerHandler("unselect1", onUnselect)
	
	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)
</t>
<t tx="T91">def onSelect (tag,keywords):

	import Tkinter,os

	new_v = keywords.get("new_v")
	h = new_v.headString()
	if h[:7] == "@image ":
		filename = h[7:]
		&lt;&lt; Select Image &gt;&gt;</t>
<t tx="T92"># Display the image file in the text pane, if you can find the file
a = app()
c = keywords.get("c")
body = c.frame.body

if os.path.isfile(filename):
	try:
		# Note that Tkinter only understands GIF
		photo = Tkinter.PhotoImage(master=a.root, file=filename)
	except:
		es("error: cannot load image")
		return
	# Nicely display the image at the center top and push the text below.
	a.gsphoto = photo # This is soooo important.
	photoWidth = photo.width()
	bodyWidth = body.winfo_width()
	padding = int((bodyWidth - photoWidth - 16) / 2)
	padding = max(0,padding)
	a.gsimage = body.image_create("1.0",image=photo,padx=padding)
else:
	es("warning: missing image file")</t>
<t tx="T93">def onUnselect (tag,keywords):

	import Tkinter, os.path

	a = app()
	old_v = keywords.get("old_v")
	if old_v:
		h = old_v.headString()
		if h[:7] == "@image ":
			&lt;&lt; Unselect Image &gt;&gt;					
	else: # Leo is initializing.
		a.gsphoto = None # Holds our photo file
		a.gsimage = None # Holds our image instance within the text pane</t>
<t tx="T94"># Erase image if it was previously displayed
a = app() ; c = keywords.get("c")

if a.gsimage:
	try:
		 c.frame.body.delete(a.gsimage)
	except:
		es("info: no image to erase")

# And forget about it
a.gsimage = None
a.gsphoto = None
</t>
<t tx="T95">"""Adds navigation buttons to icon bar"""

from leoPlugins import *
from leoGlobals import *
from leoDialog import listBoxDialog
import os, Tkinter

@others
	
globalInfo = globalInfoClass()

Tk = Tkinter

if 1: # Register the handlers...

	registerHandler("after-create-leo-frame", globalInfo.addNavWidgets)
	registerHandler("select2",globalInfo.updateRecentSections)
	registerHandler("command2",globalInfo.updateMarksAfterCommand)
	registerHandler(("set-mark","clear-mark"),globalInfo.updateMarks)
	registerHandler("close-frame",globalInfo.destroyFrame)
	registerHandler("destroy-all-global-windows",globalInfo.destroyAllFrames)

	# 7/12/03: Moved marksDialog and recentSectionsDialog into this plugin.
	# 7/12/03: Handled "set-mark" and "clear-mark" hooks.
	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T96">class commanderInfoClass:
	@others</t>
<t tx="T97">def __init__ (self,c,globalInfo):
	
	self.c = c
	self.globalInfo = globalInfo
	
	# The icon frame in c.
	self.iconFrame = c.frame.iconFrame
	
	# Dialogs.
	self.marksDialog = None
	self.recentSectionsDialog = None

	# Images for arrow buttons.
	self.lt_nav_disabled_image = self.lt_nav_enabled_image = None
	self.rt_nav_disabled_image = self.rt_nav_enabled_image = None
	
	# The arrow and text buttons.
	self.lt_nav_button = self.rt_nav_button = None
	sections_button = self.marks_button = None
	
	self.nav_buttons = None
</t>
<t tx="T98">def addWidgets (self):
	
	c = self.c ; d = self
	
	d.lt_nav_disabled_image = self.createImage("../Icons/lt_arrow_disabled.gif")
	d.lt_nav_enabled_image  = self.createImage("../Icons/lt_arrow_enabled.gif")
	
	d.rt_nav_disabled_image = self.createImage("../Icons/rt_arrow_disabled.gif")
	d.rt_nav_enabled_image  = self.createImage("../Icons/rt_arrow_enabled.gif")
	
	for image in (
		self.lt_nav_disabled_image, self.lt_nav_enabled_image,
		self.rt_nav_disabled_image, self.rt_nav_enabled_image):
		if not image:
			return
	
	# It's so nice to be able to add ivars to classes at any time!
	self.lt_nav_button = c.frame.addIconButton(
		image=self.lt_nav_disabled_image,
		command=c.frame.OnGoPrevVisitedNode)
		
	&lt;&lt; define callbacks &gt;&gt;

	self.sections_button = c.frame.addIconButton(
		text="Recent",command=onRecentButton)
		
	self.marks_button = c.frame.addIconButton(
		text="Marks",command=onMarksButton)
	
	self.rt_nav_button = c.frame.addIconButton(
		image=self.rt_nav_disabled_image,
		command=c.frame.OnGoNextVisitedNode)
		
	# Don't dim the button when it is inactive.
	for b in (self.lt_nav_button,self.rt_nav_button):
		fg = b.cget("foreground")
		b.configure(disabledforeground=fg)
		
	# Package these buttons for the recentSectionsDialog class in leoDialog.py
	self.nav_buttons = (self.lt_nav_button, self.rt_nav_button)</t>
<t tx="T99"># These are functions, not methods, so we must bind self at definition time.

def onMarksButton(self=self):

	self.marksButtonCallback()
	
def onRecentButton(self=self):

	self.recentButtonCallback()</t>
<t tx="T100">def createImage (self,path):
	
	path = os.path.join(app().loadDir,path)
	path = os.path.normpath(path)
	
	try:
		image = Tkinter.PhotoImage(master=app().root,file=path)
	except:
		es("can not load icon: " + shortFileName(path))
		image = None
	return image

</t>
<t tx="T101">def updateNavButtons (self):	

	d = self ; c = self.c
	
	# Make sure we have initialized properly.
	if not hasattr(d,"lt_nav_button") or not hasattr(d,"rt_nav_button"):
		return
		
	if not d.lt_nav_button or not d.rt_nav_button: # 6/30/03
		return
	
	b = d.lt_nav_button
	if c.beadPointer &gt; 0:
		image = self.lt_nav_enabled_image
		state = "normal"
	else:
		image = d.lt_nav_disabled_image
		state = "normal" # "disabled" makes the icon look bad.
	b.configure(image=image,state=state)
	
	b = d.rt_nav_button
	if c.beadPointer + 1 &lt; len(c.beadList):
		image =self.rt_nav_enabled_image
		state = "normal"
	else:
		image = self.rt_nav_disabled_image
		state = "normal" # "disabled" makes the icon look bad.
	b.configure(image=image,state=state)
</t>
<t tx="T102"></t>
<t tx="T103">def marksButtonCallback(self,event=None):
	
	c = self.c ; d = self.marksDialog

	if d:
		d.top.deiconify()
	else:
		# Create and run the dialog.
		title = "Marks"
		label = "Marks: " + shortFileName(c.frame.mFileName)
		d = marksDialog(c,title,label)
		self.marksDialog = d
		d.root.wait_window(d.top)
</t>
<t tx="T104">def recentButtonCallback(self,event=None):
	
	c = self.c ; d = self.recentSectionsDialog
	
	if d:
		d.top.deiconify()
		d.fillbox()
	else:
		# Create and run the dialog.]
		title = "Recent Nodes"
		label = "Recent nodes: " + shortFileName(c.frame.mFileName)
		d = recentSectionsDialog(c,self.nav_buttons,title,label)
		self.recentSectionsDialog = d
		d.root.wait_window(d.top)
</t>
<t tx="T105">class globalInfoClass:
	@others</t>
<t tx="T106">def __init__ (self):
	
	self.commanderInfo = {} # keys are commanders, values are navCommanderInfo objects
</t>
<t tx="T107">def addNavWidgets(self,tag,keywords):
	
	c = keywords.get("c")
	
	# Create the commanderInfo object.
	d = commanderInfoClass(c,self)
	self.commanderInfo[c] = d
	
	# Add the widgets.
	d.addWidgets()
	
</t>
<t tx="T108">def destroyAllFrames(self,tag,keywords):
	
	for d in self.commanderInfo.values():
		self.destroyOneFrame(d)
		
def destroyFrame(self,tag,keywords):

	c = keywords.get("c")
	d = self.commanderInfo.get(c)
	if d:
		self.destroyOneFrame(d)
		
def destroyOneFrame(self,d):

	if d.marksDialog:
		d.marksDialog.top.destroy()
	if d.recentSectionsDialog:
		d.recentSectionsDialog.top.destroy()
	del self.commanderInfo[d.c]</t>
<t tx="T109">def updateRecentSections (self,tag,keywords):
	
	c = keywords.get("c")
	info = self.commanderInfo.get(c)

	if info:
		info.updateNavButtons()
		d = info.recentSectionsDialog
		if d:
			d.fillbox()
</t>
<t tx="T110">def updateMarksAfterCommand (self,tag,keywords):
	
	"""Update the marks dialog when a new window is opened."""
	
	name = keywords.get("label")
	
	if name and name.lower() in ("open","new"):
		self.updateMarks(tag,keywords)
	
def updateMarks (self,tag,keywords):
	
	"""Update the marks dialog."""
	
	c = keywords.get("c")
	# trace()
	info = self.commanderInfo.get(c)
	if info and info.marksDialog:
		info.marksDialog.fillbox()</t>
<t tx="T111">def updateNavButtons (self,tag,keywords):

	"""Update the colors of c's nav buttons"""
	
	c = keywords.get("c")
	info = self.commanderInfo.get(c)
	
	if info:
		info.updateNavButtons()
</t>
<t tx="T112">class marksDialog (listBoxDialog):
	
	"""A class to create the marks dialog"""

	@others</t>
<t tx="T113">def __init__ (self,c,title,label):
	
	"""Create a Marks listbox dialog."""

	listBoxDialog.__init__(self,c,title,label)
</t>
<t tx="T114">def createFrame(self):
	
	"""Create the frame for a Marks listbox dialog."""

	listBoxDialog.createFrame(self)
	self.addButtons()</t>
<t tx="T115">def addButtons (self):
	
	"""Add buttons to a Marks listbox dialog."""
	
	f = Tk.Frame(self.outerFrame)
	f.pack()
	self.addStdButtons(f)</t>
<t tx="T116">def fillbox(self,event=None):

	"""Update a Marks listbox dialog and update the listbox and update vnodeList &amp; tnodeList ivars"""

	self.box.delete(0,"end")
	self.vnodeList = []
	self.tnodeList = []

	# Make sure the node still exists.
	# Insert only the last cloned node.
	c = self.c ; v = c.rootVnode()
	i = 0
	while v:
		if v.isMarked() and v.t not in self.tnodeList:
			self.box.insert(i,v.headString().strip())
			self.tnodeList.append(v.t)
			self.vnodeList.append(v)
			i += 1
		v = v.threadNext()</t>
<t tx="T117">class recentSectionsDialog (listBoxDialog):
	
	"""A class to create the recent sections dialog"""

	@others</t>
<t tx="T118">def __init__ (self,c,buttons,title,label):
	
	"""Create a Recent Sections listbox dialog."""
	
	self.lt_nav_iconFrame_button, self.rt_nav_iconFrame_button = buttons

	listBoxDialog.__init__(self,c,title,label)

</t>
<t tx="T119">def addButtons (self):
	
	"""Add buttons for a Recent Sections listbox dialog."""

	self.buttonFrame = f = Tk.Frame(self.outerFrame)
	f.pack()
	
	row1 = Tk.Frame(f)
	row1.pack()
	
	# Create the back and forward buttons, cloning the images &amp; commands of the already existing buttons.
	image   = self.lt_nav_iconFrame_button.cget("image")
	command = self.lt_nav_iconFrame_button.cget("command")

	self.lt_nav_button = b = Tk.Button(row1,image=image,command=command)
	b.pack(side="left",pady=2,padx=5)
	
	image   = self.rt_nav_iconFrame_button.cget("image")
	command = self.rt_nav_iconFrame_button.cget("command")

	self.rt_nav_button = b = Tk.Button(row1,image=image,command=command)
	b.pack(side="left",pady=2,padx=5)
	
	row2 = Tk.Frame(f)
	row2.pack()
	self.addStdButtons(row2)
	
	row3 = Tk.Frame(f)
	row3.pack()
	
	self.clear_button = b =  Tk.Button(row3,text="Clear All",
		width=6,command=self.clearAll)
	b.pack(side="left",pady=2,padx=5)
	
	self.delete_button = b =  Tk.Button(row3,text="Delete",
		width=6,command=self.deleteEntry)
	b.pack(side="left",pady=2,padx=5)
</t>
<t tx="T120">def clearAll (self,event=None):

	"""Handle clicks in the "Delete" button of the Recent Sections listbox dialog."""

	self.c.visitedList = []
	self.vnodeList = []
	self.fillbox()
</t>
<t tx="T121">def createFrame(self):
	
	"""Create the frame of a Recent Sections listbox dialog."""
	
	listBoxDialog.createFrame(self)	
	self.addButtons()
</t>
<t tx="T122">def deleteEntry (self,event=None):

	"""Handle clicks in the "Delete" button of a Recent Sections listbox dialog."""
	
	c = self.c ; box = self.box
	
	# Work around an old Python bug.  Convert strings to ints.
	items = box.curselection()
	try:
		items = map(int, items)
	except ValueError: pass

	if items:
		n = items[0]
		v = self.vnodeList[n]
		del self.vnodeList[n]
		if v in c.visitedList:
			c.visitedList.remove(v)
		self.fillbox()
</t>
<t tx="T123">def destroy (self,event=None):
	
	"""Hide a Recent Sections listbox dialog and mark it inactive.
	
	This is an escape from possible performace penalties"""
		
	# This is enough to disable fillbox.
	self.top.withdraw()
</t>
<t tx="T124">def fillbox(self,event=None):

	"""Update a Recent Sections listbox dialog and update vnodeList &amp; tnodeList ivars"""

	# Only fill the box if the dialog is visible.
	# This is an important protection against bad performance.

	if self.top.state() == "normal":
		&lt;&lt; reconstruct the contents of self.box &gt;&gt;
		self.synchButtons()</t>
<t tx="T125">c = self.c

self.box.delete(0,"end")
self.vnodeList = []
self.tnodeList = []

# Make sure the node still exists.
# Insert only the last cloned node.
i = 0
for v in c.visitedList:
	if v.exists(self.c) and v.t not in self.tnodeList:
		self.box.insert(i,v.headString().strip())
		self.tnodeList.append(v.t)
		self.vnodeList.append(v)
		i += 1
</t>
<t tx="T126">def synchButtons (self):
	
	"""Synchronize the arrow boxes of a Recent Sections listbox dialog."""

	image = self.lt_nav_iconFrame_button.cget("image")
	self.lt_nav_button.configure(image=image)
	
	image = self.rt_nav_iconFrame_button.cget("image")
	self.rt_nav_button.configure(image=image)</t>
<t tx="T127"></t>
<t tx="T128">"""Create menu for Open With command and handle the resulting commands"""

from leoPlugins import *
from leoGlobals import *

@others

if 1: # Register the handlers...

	app().hasOpenWithMenu = true
	registerHandler("idle", on_idle)
	registerHandler(("start2","open2","command2"), create_open_with_menu)

	__version__ = "1.4" # Set version for the plugin handler.
	plugin_signon(__name__)</t>
<t tx="T129"># frame.OnOpenWith creates the dict with the following entries:
# "body", "c", "encoding", "f", "path", "time" and "v".

def on_idle (tag,keywords):

	import os
	a = app()
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
					&lt;&lt; update v's body text &gt;&gt;
			except:
				es_exception() ## testing
				pass</t>
<t tx="T130">&lt;&lt; set s to the file text &gt;&gt;

# Convert body to whatever encoding is in effect.
body = v.bodyString()
body = toEncodedString(body,encoding,reportErrors=true)

conflict = body != old_body and body != s

# Set update if we should update the outline from the file.
if conflict:
	# See how the user wants to resolve the conflict.
	import leoDialog
	es("conflict in " + shortFileName(path),color="red")
	message = "Replace changed outline with external changes?"
	result = leoDialog.askYesNo("Conflict!",message).run(modal=true)
	update = result.lower() == "yes"
else:
	update = s != body

if update:
	es("updated from: " + shortFileName(path),color="blue")
	v.setBodyStringOrPane(s)
	c.selectVnode(v)
	dict["body"] = s
elif conflict:
	es("not updated from: " + shortFileName(path),color="blue")</t>
<t tx="T131">try:
	# Update v from the changed temp file.
	f=open(path)
	s=f.read()
	f.close()
except:
	es("can not open " + shortFileName(path))
	break
</t>
<t tx="T132">def create_open_with_menu (tag,keywords):

	if  (tag in ("start2","open2") or
		(tag=="command2" and keywords.get("label")=="new")):

		&lt;&lt; create the Open With menu &gt;&gt;
		# Enable the idle-time hook so we can check temp files created by Open With.
		from leoGlobals import enableIdleTimeHook
		enableIdleTimeHook(idleTimeDelay=500)
</t>
<t tx="T133">@ Entries in the following table are the tuple (commandName,shortcut,data).

- data is the tuple (command,arg,ext).
- command is one of "os.system", "os.startfile", "os.spawnl", "os.spawnv" or "exec".

Leo executes command(arg+path) where path is the full path to the temp file.
If ext is not None, the temp file has the extension ext,
Otherwise, Leo computes an extension based on what @language directive is in effect.
@c

idle_arg = "c:/python22/tools/idle/idle.py -e "

if 1: # Default table.
	table = (
		# Opening idle this way doesn't work so well.
		# ("&amp;Idle",   "Alt+Shift+I",("os.system",idle_arg,".py")),
		("&amp;Word",   "Alt+Shift+W",("os.startfile",None,".doc")),
		("Word&amp;Pad","Alt+Shift+T",("os.startfile",None,".txt")))
elif 1: # Test table.
	table = ("&amp;Word","Alt+Shift+W",("os.startfile",None,".doc")),
else: # David McNab's table.
	table = ("X&amp;Emacs", "Ctrl+E", ("os.spawnl","/usr/bin/gnuclient", None)),

top().frame.createOpenWithMenuFromTable(table)</t>
<t tx="T134">"""vim handler"""

# Contributed by Andrea Galimberti.

#  To use this plugin do the following:
#
# - Start VIM as server: vim --servername "VIM"
#   The name of the server *must* be "VIM".
#
# - Single-click on a node's icon to open that node in VIM.
#
# - Leo will update the node in the outline when you save the file in VIM.

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("iconclick2", open_in_vim)
	
	__version__ = "1.3" # Set version for the plugin handler.
	plugin_signon(__name__)
</t>
<t tx="T135">def open_in_vim (tag,keywords):
	if not top():
		return

	v=keywords['v']
	# Find dictionary with infos about this node
	this=filter(lambda x: id(x['v'])==id(v), app().openWithFiles)
	
	# Retrieve the name of the temporary file (if any).
	if this != []:
		path=this[0]['path']
	else:
		path=''

	if os.path.exists(path):
		# Get previous node contents.
		try:
			old=v.OpenWithOldBody
		except AttributeError:
			old=''

	if v.bodyString() != old:
		# delete old temp file
		os.remove(path)
		# remove old temp file from list
		app().openWithFiles=filter(lambda x: x['path']!=path,app().openWithFiles)
		# update old body with new contents
		v.OpenWithOldBody=v.bodyString()
		# open the node in vim (note the space after --remote)
		top().frame.OnOpenWith(("os.system", "vim --remote ", None),) # 6/27/03: add comma.</t>
<t tx="T136">"""emacs handler"""

from leoPlugins import *
from leoGlobals import *

def open_in_emacs (tag,keywords):
	if top():
		top().frame.OnOpenWith(("os.spawnl", "/usr/bin/gnuclient", None),) # 6/27/03: add comma.

if 0: # Register the handlers...
	registerHandler(("iconclick2","select2"), open_in_emacs)
	
	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)</t>
<t tx="T137"></t>
<t tx="T138">"""Open any empty file as a minimal .leo file"""

from leoPlugins import *
from leoGlobals import *

&lt;&lt; define minimal .leo file &gt;&gt;
@others

if 0: # Register the handlers...
	registerHandler("open1", onOpen)
	
	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)</t>
<t tx="T139">empty_leo_file = """&lt;?xml version="1.0" encoding="iso-8859-1"?&gt;
&lt;leo_file&gt;
&lt;leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/&gt;
&lt;globals body_outline_ratio="0.5"&gt;
	&lt;global_window_position top="145" left="110" height="24" width="80"/&gt;
	&lt;global_log_window_position top="0" left="0" height="0" width="0"/&gt;
&lt;/globals&gt;
&lt;preferences allow_rich_text="0"&gt;
&lt;/preferences&gt;
&lt;find_panel_settings&gt;
	&lt;find_string&gt;&lt;/find_string&gt;
	&lt;change_string&gt;&lt;/change_string&gt;
&lt;/find_panel_settings&gt;
&lt;vnodes&gt;
&lt;v a="V"&gt;&lt;vh&gt;NewHeadline&lt;/vh&gt;&lt;/v&gt;
&lt;/vnodes&gt;
&lt;tnodes&gt;
&lt;/tnodes&gt;
&lt;/leo_file&gt;"""</t>
<t tx="T140">def onOpen (tag,keywords):

	import os
	file_name = keywords.get('fileName')

	if file_name and os.path.getsize(file_name)==0:
		# Rewrite the file before really opening it.
		es("rewriting empty .leo file: %s" % (file_name))
		file = open(file_name,'w')
		file.write(empty_leo_file)
		file.flush()
		file.close()

</t>
<t tx="T141">@language python

"""Opens up cmd and explorer window to same directory 
as @file nodes or children ..."""

&lt;&lt; about the open shell plugin &gt;&gt;

import leo,os,os.path,sys
from leoPlugins import *
from leoGlobals import *

pathToExplorer = 'c:/windows/explorer.exe'
pathToCmd = 'c:/windows/system32/cmd.exe'

@others

if 0: # Register the plugin

	registerHandler("after-create-leo-frame", load_menu)
	__version__ = "1.3"
	plugin_signon(__name__)</t>
<t tx="T142">@ Written by Ed Taekema.  Modified by E.K.Ream

Please submit bugs / feature requests to etaekema@earthlink.net"""

This is a simple plugin for leo 3.12 that allows the user to open either an xterm on linux or a cmd windows/explorer window on win32 in the directory of the current @file.  This allows quick navigation to facilitate testing and navigating large systems with complex direcgtories.

Current limitations ...

1. Not tested on Mac OS X ...
2. On win32, the cmd window will not open in the right directory if the @file location is on a different drive than the .leo file that is being edited.
3. On linux, xterm must be in your path.
</t>
<t tx="T143">def load_menu(tag,keywords):
	
	if sys.platform=="win32":
		table = (
			("&amp;Open Console Window",None,launchCmd),
			("Open &amp;Explorer",None,launchExplorer)) 
	else:
		table = ( ("Open &amp;xterm",None,launchxTerm), ) 
	
	top().frame.createNewMenu("E&amp;xtensions","top")
	top().frame.createMenuItemsFromTable("Extensions",table)
</t>
<t tx="T144">def _getpath(c,v):
	dict = scanDirectives(c,v)
	d = dict.get("path")

	if d == None:

		if v.isAtFileNode():
			filename = v.atFileNodeName()
		if v.isAtNoSentinelsFileNode():
			filename = v.atNoSentinelsFileNodeName()
		if v.isAtRawFileNode():
			filename = v.atRawFileNodeName()
		if v.isAtSilentFileNode():
			filename = v.atSilentFileNodeName()

		d = os.path.dirname(filename)

	d = os.path.normpath(d)
	return d
</t>
<t tx="T145">def _getCurrentNodePath():
	c = leo.top()
	v = c.currentVnode()
	f = v.atFileNodeName()
	d = _getpath(c,v)
	return d
</t>
<t tx="T146">def launchCmd(not_used):
	
	global pathToCmd

	d = _getCurrentNodePath()
	myCmd = 'cd ' + d
	os.spawnl(os.P_NOWAIT, pathToCmd, '/k ', myCmd)</t>
<t tx="T147">def launchExplorer(not_used):
	
	global pathToExplorer

	d = _getCurrentNodePath()
	os.spawnl(os.P_NOWAIT,pathToExplorer, ' ', d)

</t>
<t tx="T148">def launchxTerm(not_used):

	d = _getCurrentNodePath()
	curdir = os.getcwd()
	os.chdir(d)
	os.spawnlp(os.P_NOWAIT, 'xterm', '-title Leo')
	os.chdir(curdir)</t>
<t tx="T149">In Python 2.3 the source files should declare the encoding.

See http://www.python.org/peps/pep-0263.html for full details.</t>
<t tx="T150">@first # -*- coding: utf-8 -*-

"""Translate a few menu items into French"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler(("start1","menu1"), onMenu)
	
	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T151">@ The translation table used by setRealMenuNamesFromTable has entries of the form:

	("official name","translated name"),

Ampersands in the translated name indicate that the following character is to be underlined.

The official name can be any name equivalent to the standard English menu names.  Leo "canonicalizes" the official name by converting to lower case and removing any non-letters.  Thus, the following are  equivalent:
	("Open...","&amp;Ouvre"),
	("open",   "&amp;Ouvre"),
	("&amp;Open",  "&amp;Ouvre"),
@c
def onMenu (tag,keywords):
	table = (
		("Open...","&amp;Ouvre"),
		("OpenWith","O&amp;uvre Avec..."),
		("close","&amp;Ferme"),
		("Undo Typing","French &amp;Undo Typing"), # Shows you how much French I know ;-)
		("Redo Typing","French &amp;Redo Typing"),
		("Can't Undo", "French Can't Undo"),
		("Can't Redo", "French Can't Redo"))
	# Call the convenience routine to do the work.
	app().setRealMenuNamesFromTable(table)
</t>
<t tx="T152">@first # -*- coding: utf-8 -*-
@language python

"""traduit les menus en Français"""

# French translation completed by Frédéric Momméja, Spring 2003

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler(("start1","menu1"), onMenu)
	
	__version__ = "1.4" # Set version for the plugin handler.
	plugin_signon(__name__)
</t>
<t tx="T153">def onMenu (tag,keywords):
	table = (
		("File","&amp;Fichier"),
			("New","&amp;Nouveau"),
			("Open...","&amp;Ouvrir"),
			("OpenWith","Ouvrir Ave&amp;c..."),
			("Close","&amp;Fermer"),
			("Save","Enregi&amp;strer"),
			("Save As","Enre&amp;gistrer sous..."),
			("Save To","Enregistrer une co&amp;pie..."),
			("Revert To Saved","&amp;Version Enregistrée"),
			("Recent Files...","&amp;Fichiers récents..."),
			("Read/Write...", "&amp;Lire/Écrire..."),
				("Read Outline Only", "Relire &amp;Arborescence seule"),
				("Read @file Nodes", "Relire Structure @&amp;file seule"),
				("Write missing @file Nodes", "Écrire @file &amp;manquants sur Disque"),
				("Write Outline Only", "Écrire Arborescence &amp;seule"),
				("Write @file Nodes", "Écrire &amp;Noeuds @file seuls"),
			("Tangle...", "&amp;Transférer (Tangle)..."),
				("Tangle All", "&amp;Tout"),
				("Tangle Marked", "Noeuds &amp;Marqués"),
				("Tangle", "&amp;Sélection"),
			("Untangle...", "&amp;Ramener (Untangle)..."),
				("Untangle All", "&amp;Tout"),
				("Untangle Marked", "Noeuds &amp;Marqués"),
				("Untangle", "&amp;Sélection"),
			("Import...", "&amp;Importer..."),
				("Import To @file", "Dans Structure @&amp;file"),
				("Import To @root", "Dans Structure @&amp;root"),
				("Import CWEB Files", "Fichier &amp;CWEB"),
				("Import noweb Files", "Fichier &amp;Noweb"),
				("Import Flattened Outline", "Fichier &amp;MORE"),
			("Export...", "&amp;Exporter..."),
				("Export Headlines", "&amp;Entêtes Noeuds descendants vers .txt"),
				("Outline To CWEB", "Arborescence vers &amp;CWEB"),
				("Outline To Noweb", "Arborescence vers &amp;Noweb"),
				("Flatten Outline", "Arborescence vers &amp;MORE"),
				("Remove Sentinels", "En supprimant &amp;Sentinelles"),
				("Weave", "&amp;Arborescence descendante vers .txt"),
			("Exit","&amp;Quitter"),
		("Edit","&amp;Edition"),
			("Undo Typing","Ann&amp;uler saisie"),
			("Redo Typing","&amp;Répèter saisie"),
			("Can't Undo", "Impossible d'annuler"),
			("Can't Redo", "Impossible de répéter"),
			("Cut", "C&amp;ouper"),
			("Copy", "Co&amp;pier"),
			("Paste", "Co&amp;ller"),
			("Delete", "&amp;Supprimer"),
			("Select All", "&amp;Tout Sélectionner"),
			("Edit Body...", "Éditer &amp;Contenu..."),
				("Extract Section", "E&amp;xtraire Section"),
				("Extract Names", "Extraire &amp;Noms de Sections"),
				("Extract", "&amp;Extraire Sélection"),
				("Convert All Blanks", "Convertir Espaces &amp;Arborescence"),
				("Convert All Tabs", "Convertir Tabulations Ar&amp;borescence"),
				("Convert Blanks", "Convertir &amp;Espaces"),
				("Convert Tabs", "Convertir &amp;Tabulations"),
				("Insert Body Time/Date", "Insérer la &amp;Date/Heure"),
				("Reformat Paragraph", "Reformater &amp;Paragraphe"),
				("Indent", "&amp;Indenter"),
				("Unindent", "Dé&amp;sindenter"),
				("Match Brackets", "&amp;Vérifier Parité des Signes"), #  &lt;({["), #EKR
			("Edit Headline...", "Éditer &amp;Entête..."),
				("Edit Headline", "&amp;Modifier l'Entête"),
				("End Edit Headline", "Modification &amp;Terminée"),
				("Abort Edit Headline", "&amp;Annuler Modification"),
				("Insert Headline Time/Date", "Insérer la &amp;Date/Heure"),
				("Toggle Angle Brackets", "Ajouter/supprimer Marques de &amp;Section"),
			("Find...", "C&amp;hercher..."),
				("Find Panel", "Dialogue de Re&amp;cherche"),
				("Find Next", "Chercher &amp;Suivant"),
				("Find Previous", "Chercher &amp;Précédent"),
				("Replace", "&amp;Remplacer"),
				("Replace, Then Find", "Remplacer Chercher à &amp;Nouveau"),
			("Go To Line Number", "&amp;Atteindre Ligne No..."),
			("Execute Script", "E&amp;xécuter un Script Python"),
			("Set Font...", "&amp;Définir les Polices..."),
			("Set Colors...", "Dé&amp;finir les Couleurs..."),
			("Show Invisibles", "Afficher Caractères &amp;invisibles"),
			("Hide Invisibles", "Masquer Caractères &amp;invisibles"),
			("Preferences", "Préfére&amp;nces"),
		("Outline", "Arb&amp;orescence"),
			("Cut Node", "Co&amp;uper le Noeud"),
			("Copy Node", "C&amp;opier le Noeud"),
			("Paste Node", "Co&amp;ller le Noeud"),
			("Delete Node", "&amp;Supprimer le Noeud"),
			("Insert Node", "Insé&amp;rer un Noeud"),
			("Clone Node", "Clo&amp;ner le Noeud"),
			("Sort Children", "&amp;Trier les Noeuds Enfants"),
			("Sort Siblings", "Trier le Ni&amp;veau"),
			("Expand/Contract...", "&amp;Déployer/Refermer"),
				("Contract All", "&amp;Tout Refermer"),
				("Contract Node", "&amp;Refermer Noeud"),
				("Contract Parent", "Refermer Noeud &amp;Parent"),
				("Expand Prev Level", "Déployer Niveau pré&amp;cédent"),
				("Expand Next Level", "Déployer Niveau &amp;suivant"),
				("Expand To Level 1", "Déployer &amp;1 Niveau"),
				("Expand To Level 2", "Déployer &amp;2 Niveaux"),
				("Expand To Level 3", "Déployer &amp;3 Niveaux"),
				("Expand To Level 4", "Déployer &amp;4 Niveaux"),
				("Expand To Level 5", "Déployer &amp;5 Niveaux"),
				("Expand To Level 6", "Déployer &amp;6 Niveaux"),
				("Expand To Level 7", "Déployer &amp;7 Niveaux"),
				("Expand To Level 8", "Déployer &amp;8 Niveaux"),
				("Expand All", "Tout &amp;Déployer"),
				("Expand Node", "Déplo&amp;yer Noeud"),
			("Move...", "Dé&amp;placer..."),
				("Move Down", "Vers le &amp;Bas"),
				("Move Left", "Vers la &amp;Gauche"),
				("Move Right", "Vers la &amp;Droite"),
				("Move Up", "Vers le &amp;Haut"),
				("Promote", "&amp;Enfants vers la Gauche"),
				("Demote", "&amp;Noeuds suivants vers la Droite"),
			("Mark/Unmark...", "Mar&amp;quage..."),
				("Mark", "&amp;Marquer/Effacer Marque"),
				("Mark Subheads", "Marquer En&amp;fants"),
				("Mark Changed Items", "Marquer &amp;Noeuds modifiés"),
				("Mark Changed Roots", "Marquer @&amp;root modifiés"),
				("Mark Clones", "Marquer &amp;Clones"),
				("Unmark All", "&amp;Effacer toutes les Marques"),
			("Go To...", "Se Dépla&amp;cer vers..."),
				("Go To Next Marked", "&amp;Marque suivante"),
				("Go To Next Changed", "M&amp;odification suivante"),
				("Go To Next Clone", "&amp;Clone suivant"),
				("Go To First Node", "&amp;Premier Noeud"),
				("Go To Last Node", "&amp;Dernier Noeud"),
				("Go To Parent", "&amp;Noeud Parent"),
				("Go To Prev Sibling", "Noe&amp;ud précédent"),
				("Go To Next Sibling", "Noeud &amp;suivant"),
				("Go To Prev Visible", "Noeud &amp;Visible précédent"),
				("Go To Next Visible", "Noeud V&amp;isible suivant"),
				("Go Back", "De&amp;rnière Position"),
				("Go Next", "Posi&amp;tion suivante"),
		("Window", "Fenê&amp;tre"),
			("Equal Sized Panes", "Panneaux de &amp;même taille"),
			("Toggle Active Pane", "&amp;Bascule Panneau actif"),
			("Toggle Split Direction", "Bascule &amp;Horiz/Vert"),
			("Cascade", "Fenêtres Leo en &amp;Cascade"),
			("Minimize All", "&amp;Réduit toutes les Fenêtres"),
			("Open Compare Window", "Ouvrir Fenêtre de Com&amp;paraison..."),
			("Open Python Window", "Ouvrir Fenêtre Python (IDLE)..."),
		("Help", "&amp;Aide"),
			("About Leo...", "Au &amp;sujet de Leo..."),
			("Online Home Page", "&amp;Page d'Accueil en ligne"),
			("Open Online Tutorial", "Ouvrir &amp;Tutoriel en ligne"),
			("Open LeoDocs.leo", "Ouvrir Leo&amp;Docs.leo"),
			("Open LeoConfig.leo", "Ouvrir Leo&amp;Config.leo"),
			("Apply Settings", "Appliquer les &amp;Réglages"))
	# Call the convenience routine to do the work.
	app().setRealMenuNamesFromTable(table)
</t>
<t tx="T154"></t>
<t tx="T155">"""Rebind up/down arrow keys"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("open2", onOpen)
	
	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)
</t>
<t tx="T156"># Warning: the bindings created this way conflict with shift-arrow keys.

def onOpen (tag,keywords):

	c = keywords.get("new_c")
	body = c.frame.body
	tree = c.frame.tree

	# Add "hard" bindings to have up/down arrows move by visual lines.
	old_binding = body.bind("&lt;Up&gt;")
	if len(old_binding) == 0:
		body.bind("&lt;Up&gt;",tree.OnUpKey)

	old_binding = body.bind("&lt;Down&gt;")
	if len(old_binding) == 0:
		body.bind("&lt;Down&gt;",tree.OnDownKey)
</t>
<t tx="T157"></t>
<t tx="T158"></t>
<t tx="T159">"""Create a Plugins menu"""

# Written by Paul A. Paterson.  Revised by Edward K. Ream.

## To do: confine the imports to the plugins directory.
## This does _not_ happen now!  import test gets a module from the Python directory!

## To do: add Revert button to each dialog.

from leoPlugins import *
from leoGlobals import *
import ConfigParser,glob,os,sys,Tkinter

Tk = Tkinter

@others

if 1: # Register the handlers...
	registerHandler("create-optional-menus",createPluginsMenu)
	
	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T160">class PlugIn:

	"""A class to hold information about one plugin"""

	@others
	
</t>
<t tx="T161">def __init__(self, filename):

	"""Initialize the plug-in"""

	# Import the file to find out some interesting stuff
	# Do not use the imp module: we only want to import these files once!
	self.mod = self.doc = self.version = None
	try:
		self.mod = __import__(os.path.splitext(os.path.basename(filename))[0])
		if not self.mod:
			return
		self.name = self.mod.__name__
		self.doc = self.mod.__doc__
		self.version = self.mod.__dict__.get("__version__") # "&lt;unknown&gt;")
		# if self.version: print self.version,shortFileName(filename)
	except: return

	&lt;&lt; Check if this can be configured &gt;&gt;
	&lt;&lt; Check if this has an apply &gt;&gt;
	&lt;&lt; Look for additional commands &gt;&gt;</t>
<t tx="T162"># Look for a configuration file
self.configfilename = "%s.ini" % os.path.splitext(filename)[0]
self.hasconfig = os.path.isfile(self.configfilename)
</t>
<t tx="T163">@ Look for an apply function ("applyConfiguration") in the module.

This is used to apply changes in configuration from the properties window
@c

self.hasapply = hasattr(self.mod, "applyConfiguration")
</t>
<t tx="T164">@ Additional commands can be added to the plugin menu by having functions in the module called "cmd_whatever". These are added to the main menu and will be called when clicked
@c

self.othercmds = {}

for item in self.mod.__dict__.keys():
	if item.startswith("cmd_"):
		self.othercmds[item[4:]] = self.mod.__dict__[item]
</t>
<t tx="T165">def about(self, arg):
	
	"""Put up an "about" dialog for this plugin"""

	PluginAbout(self.name, self.version, self.doc)</t>
<t tx="T166">def properties(self, arg):
	
	"""Create a modal properties dialog for this plugin"""

	PropertiesWindow(self.configfilename, self)
</t>
<t tx="T167">class PropertiesWindow:

	"""A class to create and run a Properties dialog for a plugin"""

	@others</t>
<t tx="T168">def __init__(self, filename, plugin):

	"""Initialize the property window"""
	
	&lt;&lt; initialize all ivars &gt;&gt;
	&lt;&lt; create the frame from the configuration data &gt;&gt;</t>
<t tx="T169"># config stuff.
config = ConfigParser.ConfigParser()
config.read(filename)
self.filename = filename
self.config = config
self.plugin = plugin

# self.entries is a list of tuples (section, option, e),
# where section and options are strings and e is a Tk.Entry widget.
# This list is used by writeConfiguration to write all settings.
self.entries = []
</t>
<t tx="T170">root = app().root

&lt;&lt; Create the top level and the main frame &gt;&gt;
&lt;&lt; Create widgets for each section and option &gt;&gt;
&lt;&lt; Create Ok, Cancel and Apply buttons &gt;&gt;

center_dialog(top) # Do this after packing.
top.grab_set() # Make the dialog a modal dialog.
top.focus_force() # Get all keystrokes.
root.wait_window(top)</t>
<t tx="T171">self.top = top = Tk.Toplevel(root)
attachLeoIcon(self.top)
top.title("Properties of "+ plugin.name)
top.resizable(0,0) # neither height or width is resizable.
	
self.frame = frame = Tk.Frame(top)
frame.pack(side="top")</t>
<t tx="T172"># Create all the entry boxes on the screen to allow the user to edit the properties
sections = config.sections()
sections.sort()
for section in sections:
	# Create a frame for the section.
	f = Tk.Frame(top, relief="groove",bd=2)
	f.pack(side="top",padx=5,pady=5)
	Tk.Label(f, text=section.capitalize()).pack(side="top")
	# Create an inner frame for the options.
	b = Tk.Frame(f)
	b.pack(side="top",padx=2,pady=2)
	# Create a Tk.Label and Tk.Entry for each option.
	options = config.options(section)
	options.sort()
	row = 0
	for option in options:
		e = Tk.Entry(b)
		e.insert(0, config.get(section, option))
		Tk.Label(b, text=option).grid(row=row, col=0, sticky="e", pady=4)
		e.grid(row=row, col=1, sticky="ew", pady = 4)
		row += 1
		self.entries.append((section, option, e))</t>
<t tx="T173">box = Tk.Frame(top, borderwidth=5)
box.pack(side="bottom")

list = [("OK",self.onOk),("Cancel",top.destroy)]
if plugin.hasapply:
	list.append(("Apply",self.onApply),)

for text,f in list:
	Tk.Button(box,text=text,width=6,command=f).pack(side="left",padx=5)</t>
<t tx="T174">def onApply(self):
	
	"""Event handler for Apply button"""
	self.writeConfiguration()
	self.plugin.mod.applyConfiguration(self.config)

def onOk(self):

	"""Event handler for Ok button"""
	self.writeConfiguration()
	self.top.destroy()</t>
<t tx="T175">def writeConfiguration(self):
	
	"""Write the configuration to disk"""

	# Set values back into the config item.
	for section, option, entry in self.entries:
		self.config.set(section, option, entry.get())

	# Write out to the file.
	f = open(self.filename, "w")
	self.config.write(f)
	f.close()
</t>
<t tx="T176">class PluginAbout:
	
	"""A class to create and run an About Plugin dialog"""
	
	@others
</t>
<t tx="T177">def __init__(self, name, version, about):
	
	"""# Create and run a modal dialog giving the name,
	version and description of a plugin.
	"""

	root = app().root
	self.top = top = Tk.Toplevel(root)
	attachLeoIcon(self.top)
	top.title("About " + name)
	top.resizable(0,0) # neither height or width is resizable.
	
	frame = Tk.Frame(top)
	frame.pack(side="top")
	&lt;&lt; Create the contents of the about box &gt;&gt;
	&lt;&lt; Create the close button &gt;&gt;
	
	center_dialog(top) # Do this after packing.
	top.grab_set() # Make the dialog a modal dialog.
	top.focus_force() # Get all keystrokes.
	root.wait_window(top)</t>
<t tx="T178">if 0: # The name is now in the window's title.
	Tk.Label(frame, text="Name:").grid(row=0, col=0, sticky="E")
	Tk.Label(frame, text=name).grid(row=0, col=1, sticky="W")
	Tk.Label(frame, text="Version").grid(row=1, col=0, sticky="E")
	Tk.Label(frame, text=version).grid(row=1, col=1, sticky="W")
	Tk.Label(frame, text=about, borderwidth=10, justify="left").grid(columnspan=2)
else:
	Tk.Label(frame, text="Version " + version).pack()
	Tk.Label(frame, text=about, borderwidth=10).pack()</t>
<t tx="T179">buttonbox = Tk.Frame(top, borderwidth=5)
buttonbox.pack(side="bottom")

self.button = Tk.Button(buttonbox, text="Close", command=top.destroy)
self.button.pack(side="bottom")</t>
<t tx="T180">def createPluginsMenu (tag,keywords):

	c = keywords.get("c")
	old_path = sys.path[:] # Make a _copy_ of the path.

	path = os.path.join(app().loadDir,"..","plugins")
	sys.path = path
	
	if os.path.exists(path):
		# Create a list of all active plugins.
		files = glob.glob(os.path.join(path,"*.py"))
		files.sort()
		plugins = [PlugIn(file) for file in files]
		items = [(p.name,p) for p in plugins if p.version]
		if items:
			items.sort()
			c.pluginsMenu = pluginMenu = c.frame.createNewMenu("&amp;Plugins")
			&lt;&lt; add items to the plugins menu &gt;&gt;
			
	sys.path = old_path


</t>
<t tx="T181">for name,p in items:
	if p.hasconfig:
		m = c.frame.createNewMenu(p.name, "&amp;Plugins")
		table = [("About...", None, p.about),
				 ("Properties...", None, p.properties)]
		if p.othercmds:
			table.append(("-", None, None))
			items = [(cmd,None,fn) for cmd,fn in p.othercmds.iteritems()]
			items.sort()
			table.extend(items)
		c.frame.createMenuEntries(m, table)
	else:
		table = ((p.name, None, p.about),)
		c.frame.createMenuEntries(pluginMenu, table)</t>
<t tx="T182">@ignore
@language python

"""Test file for Plugins menu protocols"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...

	registerHandler("select2", onSelect)
	registerHandler("unselect1", onUnselect)
	
	__version__ = "1.1"
	plugin_signon(__name__)</t>
<t tx="T183">def applyConfiguration(config):
	
	sections = config.sections()
	sections.sort()

	for section in sections:
		options = config.options(section)
		options.sort()
		for option in options:
			print section, option, config.get(section, option)
</t>
<t tx="T184">def cmd_fn1(x):
	es("Fn1",color="blue")

def cmd_fn2(x):
	es("Fn2",color="blue")

def cmd_fn3(x):
	es("Fn3",color="blue")
</t>
<t tx="T185">def onSelect (tag,keywords):

	import Tkinter,os

	new_v = keywords.get("new_v")
	h = new_v.headString()
	if h[:7] == "@image ":
		filename = h[7:]
		&lt;&lt; Select Image &gt;&gt;</t>
<t tx="T186"># Display the image file in the text pane, if you can find the file
a = app()
c = keywords.get("c")
body = c.frame.body

if os.path.isfile(filename):
	try:
		# Note that Tkinter only understands GIF
		photo = Tkinter.PhotoImage(master=a.root, file=filename)
	except:
		es("error: cannot load image")
		return
	# Nicely display the image at the center top and push the text below.
	a.gsphoto = photo # This is soooo important.
	photoWidth = photo.width()
	bodyWidth = body.winfo_width()
	padding = int((bodyWidth - photoWidth - 16) / 2)
	padding = max(0,padding)
	a.gsimage = body.image_create("1.0",image=photo,padx=padding)
else:
	es("warning: missing image file")</t>
<t tx="T187">def onUnselect (tag,keywords):

	import Tkinter, os.path
	a = app()
	c = keywords.get("c")
	old_v = keywords.get("old_v")

	if old_v:
		h = old_v.headString()
		if h[:7] == "@image ":
			&lt;&lt; Unselect Image &gt;&gt;
	else: # Leo is initializing.
		a.gsphoto = None # Holds our photo file
		a.gsimage = None # Holds our image instance within the text pane</t>
<t tx="T188"># Erase image if it was previously displayed
if a.gsimage:
	try:
		 c.frame.body.delete(a.gsimage)
	except:
		es("info: no image to erase")

# And forget about it
a.gsimage = None
a.gsphoto = None
</t>
<t tx="T189">@nocolor</t>
<t tx="T190">Reorganized the code so I can find various classes more easily.
Used @others to simply the outline.

Sorted all entries in dialogs.
Sorted all entries in Plugins menu, regardless of whether they are configurable.

For all dialogs:
	Added top ivar and removed root/master params and ivars.
	Added Leo icon and title.
	Centered dialogs.

Ctors now run all dialogs as modal dialogs: this could easily be undone.

Used a grid in the properties dialog to align widgets.</t>
<t tx="T191">- We will use a new settings file called leoSettings.txt:
- Each setting will have its _own section_ in leoSettings.txt with the following items (most optional)
	val = present value of settings: Use parent setting if this does not exist.
	help = help string (displayed near setting if it exists)
	prompt = prompt string (defaults to setting name, i.e., the section name)
	group = name of group dialog containing this item (use general section if this does not exist)
	type = one of the following:
		value			meaning
		bool			followed by true/false prompts for radio buttons
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
<t tx="T192">I wrote myself a plug-in which would automatically save the Leo file every so often and in doing so realized that it would be useful to be able to configure the interval between saves. Anyway, to cut a long story short, I generalized the idea and came up with the attached patch. 
 
All code resides under the "Plug in changes" node. The additions are all under the "create the plug-in menu" node with another couple of lines in "createMenuBar". Structurally this is ugly - but it helps keep all the changes in one place!
 
The basic idea is to allow plug-ins to be configured and also allow them to expose additional functions which can be accessed by a menu item. The advantage is that people don't have to mess with adding menus to Leo. Existing plug-ins don't need to be changed in any way to work with the new patch.
 
Ok, here's what it does....
 
1. A new "Plug-ins" menu item is added
 
2. Each plug-in gets an "About x...." entry.
 
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
<t tx="T193">"""Create a Scripts menu for LeoPy.leo"""

from leoPlugins import *
from leoGlobals import *
import glob,os

@others

if 1: # Register the handlers...
	registerHandler("create-optional-menus",createScriptsMenu)
	
	__version__ = "1.4"
	plugin_signon(__name__)</t>
<t tx="T194">def createScriptsMenu (tag,keywords):

	c = keywords.get("c")
	path = os.path.join(app().loadDir,"..","scripts")
	
	if os.path.exists(path):

		# Create lists of scripts and subdirectories.
		entries = glob.glob(os.path.join(path,"*"))
		top_scripts = glob.glob(os.path.join(path,"*.py"))
		dirs = [f for f in entries if os.path.isdir(f)]
		&lt;&lt; Return if no scripts exist anywhere &gt;&gt;
	
		scriptsMenu = c.frame.createNewMenu("&amp;Scripts")
		table = []
		&lt;&lt; Create top-level entries for every script in top_scripts &gt;&gt;
		for dir in dirs:
			files = glob.glob(os.path.join(dir,"*.py"))
			if files:
				&lt;&lt; Create a submenu for dir containing each file in files &gt;&gt;</t>
<t tx="T195">if not top_scripts:
	found = false
	for dir in dirs:
		scripts = glob.glob(os.path.join(dir,"*.py"))
		if scripts:
			found = true ; break
	if not found:
		return
</t>
<t tx="T196">table = []
top_scripts.sort()
for script in top_scripts:
	name = shortFileName(script)
	def doScript(event=None,name=name):
		executeScript(name)
	table.append((name,None,doScript),)
	
c.frame.createMenuEntries(scriptsMenu, table)
</t>
<t tx="T197"># Create the submenu.
name = os.path.join("scripts",shortFileName(dir))
menu = c.frame.createNewMenu(name,"&amp;Scripts")

# Populate the submenu.
table = []
for file in files:
	name = shortFileName(file)
	def doScript(event=None,name=name):
		from leoGlobals import executeScript
		executeScript(name)
	table.append((name,None,doScript),)

c.frame.createMenuEntries(menu, table)</t>
<t tx="T198"></t>
<t tx="T199">"""Synchronize @folder nodes with folders"""

from leoPlugins import *
from leoGlobals import *

&lt;&lt; about this plugin &gt;&gt;
@others

def onSelect (tag,keywords):
	v = keywords.get("new_v")
	h = v.headString()
	if match_word(h,0,"@folder"):
		sync_node_to_folder(v,h[8:])

if 0: # Register the handlers...
	registerHandler("select1", onSelect)

	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)</t>
<t tx="T200">@ If a node is named '@folder path_to_folder', the content (filenames) of the
folder and the children of that node will be sync. Whenever a new file is put
there, a new node will appear on top of the children list (with mark). So that
I can put my description (ie. annotation) as the content of that node. In this
way, I can find any files much easier from leo.

Moreover, I add another feature to allow you to group files(in leo) into
children of another group. This will help when there are many files in that
folder. You can logically group it in leo (or even clone it to many groups),
while keep every files in a flat/single directory on your computer.
</t>
<t tx="T201">def sync_node_to_folder(parent,d):

	oldlist = {}
	newlist = []
	#get children info
	v = parent
	after_v = parent.nodeAfterTree()
	while v != after_v:
		if not v.hasChildren():
			oldlist[v.headString()] = v.bodyString()
		v = v.threadNext()
	#compare folder content to children
	for name in os.listdir(d):
		if name in oldlist:
			del oldlist[name]
		else:
			newlist.append(name)
	#insert newlist
	newlist.sort()
	newlist.reverse()
	for name in newlist:
		v = parent.insertAsNthChild(0)
		v.setHeadStringOrHeadline(name)
		v.setMarked()
	#warn for orphan oldlist
	if len(oldlist)&gt;0:
		es('missing: '+','.join(oldlist.keys()))
</t>
<t tx="T202">"""Inhibit changes to @read-only nodes"""

# Contributed by Davide Salomoni &lt;dsalomoni@yahoo.com&gt;

from leoPlugins import *
from leoGlobals import *
import ftplib, urllib, urlparse, os, cStringIO, tkFileDialog
from formatter import AbstractFormatter, DumbWriter
from htmllib import HTMLParser

@others

if 0: # Register the handlers...
	registerHandler(("start2","open2"), on_open2)
	registerHandler("bodykey1", on_bodykey1)
	registerHandler("headkey2", on_headkey2)
	if 0: # doesn't work: the cursor stops blinking.
		registerHandler("select1", on_select1)
		registerHandler("select2", on_select2)

	__version__ = "1.5" # Set version for the plugin handler.
	plugin_signon(__name__)
</t>
<t tx="T203">@ Dear Leo users,

Here's my first attempt at customizing leo. I wanted to have the ability to
import files in "read-only" mode, that is, in a mode where files could only
be read by leo (not tangled), and also kept in sync with the content on the
drive.

The reason for this is for example that I have external programs that generate
resource files. I want these files to be part of a leo outline, but I don't
want leo to tangle or in any way modify them. At the same time, I want them
to be up-to-date in the leo outline.

So I coded the directive plugin. It has the following characteristics:

- It reads the specified file and puts it into the node content.

- If the @read-only directive was in the leo outline already, and the file content
on disk has changed from what is stored in the outline, it marks the node as
changed and prints a "changed" message to the log window; if, on the other hand,
the file content has _not_ changed, the file is simply read and the node is
not marked as changed.

- When you write a @read-only directive, the file content is added to the node
immediately, i.e. as soon as you press Enter (no need to call a menu
entry to import the content).

- If you want to refresh/update the content of the file, just edit the headline
and press Enter. The file is reloaded, and if in the meantime it has changed,
a "change" message is sent to the log window.

- The body text of a @read-only file cannot be modified in leo.

Davide Salomoni
</t>
<t tx="T204">@ The syntax to access files in @read-only via ftp/http is the following:

@read-only http://www.ietf.org/rfc/rfc0791.txt
@read-only ftp://ftp.someserver.org/filepath

If FTP authentication (username/password) is required, it can be specified as follows:

@read-only ftp://username:password@ftp.someserver.org/filepath

For more details, see the doc string for the class FTPurl.
</t>
<t tx="T205">class FTPurl:
	"""An FTP wrapper class to store/retrieve files using an FTP URL.

    To create a connection, call the class with the constructor:

        FTPurl(url[, mode])

    The url should have the following syntax:
    
        ftp://[username:password@]remotehost/filename
    
    If username and password are left out, the connection is made using
    username=anonymous and password=realuser@host (for more information,
    see the documentation of module ftplib).
    
    The mode can be '' (default, for ASCII mode) or 'b' (for binary mode).
	This class raises an IOError exception if something goes wrong.
	"""
	
	@others
</t>
<t tx="T206">def __init__(self, ftpURL, mode=''):
	parse = urlparse.urlparse(ftpURL)
	if parse[0] != 'ftp':
		raise IOError, "error reading %s: malformed ftp URL" % ftpURL

	# ftp URL; syntax: ftp://[username:password@]hostname/filename
	self.mode = mode
	authIndex = parse[1].find('@')
	if authIndex == -1:
		auth = None
		ftphost = parse[1]
	else:
		auth = parse[1][:authIndex]
		ftphost = parse[1][authIndex+1:]
	self.ftp = ftplib.FTP(ftphost)
	if auth == None:
		self.ftp.login()
	else:
		# the URL has username/password
		pwdIndex = auth.find(':')
		if pwdIndex == -1:
			raise IOError, "error reading %s: malformed ftp URL" % ftpURL
		user = auth[:pwdIndex]
		password = auth[pwdIndex+1:]
		self.ftp.login(user, password)
	self.path = parse[2][1:]
	self.filename = os.path.basename(self.path)
	self.dirname = os.path.dirname(self.path)
	self.isConnectionOpen = 1
	self.currentLine = 0
</t>
<t tx="T207"></t>
<t tx="T208">def read(self):
	"""Read the filename specified in the constructor and return it as a string.
    If the constructor specifies no filename, or if the URL ends with '/',
    return the list of files in the URL directory.
	"""
	self.checkParams()
	if self.filename=='' or self.path[-1]=='/':
		return self.dir()

	try:
		if self.mode == '':  # mode='': ASCII mode
			slist = []
			self.ftp.retrlines('RETR %s' % self.path, slist.append)
			s = '\n'.join(slist)
		else: # mode='b': binary mode
			file = cStringIO.StringIO()
			self.ftp.retrbinary('RETR %s' % self.path, file.write)
			s = file.getvalue()
			file.close()
		return s
	except:
		exception, msg, tb = sys.exc_info()
		raise IOError, msg

</t>
<t tx="T209">def readline(self):
	"""Read one entire line from the remote file."""
	try:
		self.lst
	except AttributeError:
		self.lst = self.read().splitlines(1)
	
	if self.currentLine &lt; len(self.lst):
		s = self.lst[self.currentLine]
		self.currentLine = self.currentLine + 1
		return s
	else:
		return ''
</t>
<t tx="T210"></t>
<t tx="T211">def write(self, s):
	"""write(s) stores the string s to the filename specified in the
    constructor."""
	self.checkParams()
	if self.filename == '':
		raise IOError, 'filename not specified'
	
	try:
		file = cStringIO.StringIO(s)
		if self.mode == '':  # mode='': ASCII mode
			self.ftp.storlines('STOR %s' % self.path, file)
		else: # mode='b': binary mode
			self.ftp.storbinary('STOR %s' % self.path, file)
		file.close()
	except:
		exception, msg, tb = sys.exc_info()
		raise IOError, msg
</t>
<t tx="T212"></t>
<t tx="T213">def seek(offset=0):
	self.currentLine = 0  # we don't support fancy seeking via FTP
</t>
<t tx="T214">def flush():
	pass # no fancy stuff here.</t>
<t tx="T215">def dir(self, path=None):
	"""Issue a LIST command passing the specified argument and return output as a string."""
	s = []

	if path == None:
		path = self.dirname
	try:
		listcmd = 'LIST %s' % path
		self.ftp.retrlines(listcmd.rstrip(), s.append)
		return '\n'.join(s)
	except:
		exception, msg, tb = sys.exc_info()
		raise IOError, msg
</t>
<t tx="T216">def exists(self, path=None):
	"""Return 1 if the specified path exists. If path is omitted, the current file name is tried."""
	if path == None:
		path = self.filename

	s = self.dir(path)
	if s.lower().find('no such file') == -1:
		return 1
	else:
		return 0
</t>
<t tx="T217">def checkParams(self):
	if self.mode not in ('','b'):
		raise IOError, 'invalid mode: %s' % self.mode
	if not self.isConnectionOpen:
		raise IOError, 'ftp connection closed'
</t>
<t tx="T218">def close(self):
	"""Close an existing FTPurl connection."""
	try:
		self.ftp.quit()
	except:
		self.ftp.close()
	del self.ftp
	self.isConnectionOpen = 0</t>
<t tx="T219"># Alas, these do not seem to work on XP:
# disabling the body text _permanently_ stops the cursor from blinking.

def enable_body(body):
	global insertOnTime,insertOffTime
	if body.cget("state") == "disabled":
		try:
			es("enable")
			print insertOffTime,insertOnTime
			body.configure(state="normal")
			body.configure(insertontime=insertOnTime,insertofftime=insertOffTime)
		except: es_exception()
			
def disable_body(body):
	global insertOnTime,insertOffTime
	if body.cget("state") == "normal":
		try:
			es("disable")
			insertOnTime = body.cget("insertontime")
			insertOffTime = body.cget("insertofftime")
			print insertOffTime,insertOnTime
			body.configure(state="disabled")
		except: es_exception()
</t>
<t tx="T220"># Sets v's body text from the file with the given name.
# Returns true if the body text changed.
def insert_read_only_node (c,v,name):
	if name=="":
		name = tkFileDialog.askopenfilename(
			title="Open",
			filetypes=[("All files", "*")]
			)
		c.beginUpdate()
		v.setHeadString("@read-only %s" % name)
		c.endUpdate()
	parse = urlparse.urlparse(name)
	try:
		if parse[0] == 'ftp':
			file = FTPurl(name)  # FTP URL
		elif parse[0] == 'http':
			file = urllib.urlopen(name)  # HTTP URL
		else:
			file = open(name,"r")  # local file
		# es("..." + name)
		new = file.read()
		file.close()
	except IOError,msg:
		# es("error reading %s: %s" % (name, msg))
		# es("...not found: " + name)
		v.setBodyStringOrPane("") # Clear the body text.
		return true # Mark the node as changed.
	else:
		ext = os.path.splitext(parse[2])[1]
		if ext.lower() in ['.htm', '.html']:
			&lt;&lt; convert HTML to text &gt;&gt;
		previous = v.t.bodyString
		v.setBodyStringOrPane(new)
		changed = (toUnicode(new,'ascii') != toUnicode(previous,'ascii'))
		if changed and previous != "":
			es("changed: %s" % name) # A real change.
		return changed


</t>
<t tx="T221">fh = cStringIO.StringIO()
fmt = AbstractFormatter(DumbWriter(fh))
# the parser stores parsed data into fh (file-like handle)
parser = HTMLParser(fmt)

# send the HTML text to the parser
parser.feed(new)
parser.close()

# now replace the old string with the parsed text
new = fh.getvalue()
fh.close()

# finally, get the list of hyperlinks and append to the end of the text
hyperlinks = parser.anchorlist
numlinks = len(hyperlinks)
if numlinks &gt; 0:
	hyperlist = ['\n\n--Hyperlink list follows--']
	for i in xrange(numlinks):
		hyperlist.append("\n[%d]: %s" % (i+1,hyperlinks[i])) # 3/26/03: was i.
	new = new + ''.join(hyperlist)</t>
<t tx="T222">#  scan the outline and process @read-only nodes.
def on_open2 (tag,keywords):
	
	
	if tag == "start2":
		c = top()
	else:
		c = keywords.get("new_c")

	v = c.rootVnode()
	es("scanning for @read-only nodes...",color="blue")
	c.beginUpdate()
	while v:
		h = v.headString()
		if match_word(h,0,"@read-only"):
			changed = insert_read_only_node(c,v,h[11:])
			if changed:
				if not v.isDirty():
					v.setDirty()
				if not c.isChanged():
					c.setChanged(changed)
		v = v.threadNext()
	c.endUpdate()
</t>
<t tx="T223"># override the body key handler if we are in an @read-only node.

def on_bodykey1 (tag,keywords):

	c = keywords.get("c")
	v = keywords.get("v")
	h = v.headString()
	if match_word(h,0,"@read-only"):
		# The following code causes problems with scrolling and syntax coloring.
		# Its advantage is that it makes clear that the text can't be changed,
		# but perhaps that is obvious anyway...
		if 0: # Davide Salomoni requests that this code be eliminated.
			# An @read-only node: do not change its text.
			body = c.frame.body
			body.delete("1.0","end")
			body.insert("1.0",v.bodyString())
		return 1 # Override the body key event handler.</t>
<t tx="T224"># update the body text when we press enter

def on_headkey2 (tag,keywords):

	c = keywords.get("c")
	v = keywords.get("v")
	h = v.headString()
	ch = keywords.get("ch")
	if ch == '\r' and match_word(h,0,"@read-only"):
		# on-the-fly update of @read-only directives
		changed = insert_read_only_node(c,v,h[11:])
		c.setChanged(changed)</t>
<t tx="T225">def on_select1 (tag,keywords):

	# Doesn't work: the cursor doesn't start blinking.
	# Enable the body text so select will work properly.
	c = keywords.get("c")
	enable_body(c.frame.body)
</t>
<t tx="T226">def on_select2 (tag,keywords):

	c = keywords.get("c")
	v = c.currentVnode()
	h = v.headString()
	if match_word(h,0,"@read-only"):
		disable_body(c.frame.body)
	else:
		enable_body(c.frame.body)
</t>
<t tx="T227">"""If a headline starts with @rst &lt;filename&gt;, double-clicking on it will 
write a file in outline order, with the headlines converted to reStructuredText 
section headings.
If the name of the &lt;filename&gt; has the extension .html or .htm, and if you have
docutils installed, it will generate HTML."""

# By Josef Dalcolmo: contributed under the same licensed as Leo.py itself.

# EKR: The code now lets other plugins handle @folder and @url nodes.

from leoPlugins import *
from leoGlobals import *

&lt;&lt; about this plugin &gt;&gt;
&lt;&lt; change log &gt;&gt;

@others

if 0: # Register the handlers...
	registerHandler("icondclick1",onIconDoubleClick)
	
	__version__ = "1.5" # Set version for the plugin handler.
	plugin_signon(__name__)
</t>
<t tx="T228">@ This plugin writes out @rst nodes as a reStructuredText file.

If the filename ends in .html or .htm and if you have docutils_ (a Python
module) installed, then it will be written as HTML. The HTML converter is far
from bug-free, but remember, docutils is alpha software. (Perhaps a future
version will allow automatic translation to other formats, like OpenOffice.org
as well).

Headlines are translated into reStructuredText headlines, e.g. underlined
depending on the level and empty line separated from body text otherwise, text
is written as it is. The "#" character is not used for underlining, so it may
be used for a title as in::

	#####
	Title
	#####

Otherwise, section underlining is discouraged, since it is automatically generated.

.. _docutils: http://docutils.sourceforge.net
</t>
<t tx="T229">@ Change log:

- New tree types: @rst has been added.

- EKR: The code now lets other plugins handle @folder and @url nodes.

- HTML generation: @rst nodes can now generate HTML, if Python docutils_ are
  installed. Simply give the filename an extension .htm or .html. You can try
  this out by renaming the filename in this @rst tree.

- underlines: I changed the order of the underline characters again. The "&gt;" is
  doesn't really look good as an underline in my opinion, so I moved it to a very
  low level.

- JD 2003-03-10 (rev 1.3): some more corrections to the unicode-&gt; encoding translation.
  No only check for missing docutils (doesn't mask other errors any more).

- JD 2003-03-11 (rev 1.4): separated out the file launching code to a different pluging.



</t>
<t tx="T230"># by Josef Dalcolmo 2003-01-13
#
# this does not check for proper filename syntax.
# path is the current dir, or the place @folder points to
# this should probably be changed to @path or so.

def onIconDoubleClick(tag,keywords):

	import os
	v = keywords.get("v")
	commands = keywords.get("c")
	h = v.headString().strip()
	if match_word(h,0,"@rst"):
		fname = h[5:]
		ext = os.path.splitext(fname)[1].lower()
		if ext in ('.htm','.html'):
			&lt;&lt; write rST as HTML &gt;&gt;
		else:
			&lt;&lt; write rST file &gt;&gt;
</t>
<t tx="T231">try:
	import docutils
except:
	docutils = None
	es('HTML generation requires docutils')
if docutils:
	import StringIO
	rstFile = StringIO.StringIO()
	writeTreeAsRst(rstFile, fname, v, commands)
	rstText = rstFile.getvalue()
	&lt;&lt; convert rST to HTML &gt;&gt;
	htmlFile = file(fname,'w')
	htmlFile.write(output)
	htmlFile.close()
	rstFile.close()
	es('written: '+`fname`)</t>
<t tx="T232"># this code snipped has been taken from code contributed by Paul Paterson 2002-12-05
from docutils.core import Publisher
from docutils.io import StringOutput, StringInput

pub = Publisher()
# Initialize the publisher
pub.source = StringInput(pub.settings, source=rstText)
pub.destination = StringOutput(pub.settings, encoding="utf-8")
pub.set_reader('standalone', None, 'restructuredtext')
pub.set_writer('html')
output = pub.publish()</t>
<t tx="T233">rstFile = file(fname,'w')
writeTreeAsRst(rstFile, fname, v, commands)
rstFile.close()
es('written: '+`fname`)</t>
<t tx="T234">def writeTreeAsRst(rstFile, fname, vnode, commands):
	'Writes the tree under vnode to the file rstFile (fname is the filename)'
	# we don't write a title, so the titlepage can be customized
	# use '#' for title under/overline
	# 3/7/03
	dict = scanDirectives(commands,v=vnode)
	encoding = dict.get("encoding",None)
	if encoding == None:
		encoding = app().config.default_derived_file_encoding
	# 3/7/03
	s = toEncodedString(fname,encoding,reportErrors=true)
	rstFile.write('.. filename: '+s+'\n')
	rstFile.write('\n')
	# 3/7/03
	s = vnode.bodyString()
	s = toEncodedString(s,encoding,reportErrors=true)
	rstFile.write(s+'\n')		# write body of titlepage
	rstFile.write('\n')
	
	toplevel = vnode.level()
	stopHere = vnode.nodeAfterTree()
	v = vnode.threadNext()
	# repeat for all nodes in this tree
	while v != stopHere:
		# 3/7/03
		h = v.headString()
		h = toEncodedString(h,encoding,reportErrors=true)
		rstFile.write(h+'\n')
		rstFile.write(underline(h,v.level()-toplevel))
		rstFile.write('\n')
		# 3/7/03
		s = v.bodyString()
		s = toEncodedString(s,encoding,reportErrors=true)
		rstFile.write(s+'\n')
		rstFile.write('\n')
		v = v.threadNext()</t>
<t tx="T235"># note the first character is intentionally unused, to serve as the underline
# character in a title (in the body of the @rst node)
def underline(h,level):
	str = """#=+*^~"'`-:&gt;&lt;_"""[level]
	return str*max(len(h),4)+'\n'</t>
<t tx="T236">"""Lauches (starts) a file with the name of the headline on double-clicking it.
Uses the @folder path if the headline is under an @folder headline.
Otherwise the path is relative to the Leo file.
Headlines starting with an '@' are ignored.
This does not work on Linux (yet)."""

# By Josef Dalcolmo: contributed under the same license as Leo.py itself.

from leoPlugins import *
from leoGlobals import *

&lt;&lt; about this plugin &gt;&gt;
&lt;&lt; change log &gt;&gt;

@others

if 0: # Register the handlers...
	registerHandler("icondclick1",onIconDoubleClick)
	
	__version__ = "1.1" # Set version for the plugin handler.
	plugin_signon(__name__)</t>
<t tx="T237">@ This plugin starts a file with the name of a headline.


</t>
<t tx="T238">@ Change log

- JD: 2003-03-11 separated out from rst plugin



</t>
<t tx="T239"># @folder behavior after an idea and sample code by:
# korakot ( Korakot Chaovavanich ) @folder for files annotation 2002-11-27 02:39
# 
# open file (double-click = startfile) behavior added 
# nodes with @url, @folder, @rst are treated special
#
# by Josef Dalcolmo 2003-01-13
#
# this does not check for proper filename syntax.
# path is the current dir, or the place @folder points to
# this should probably be changed to @path or so.

def onIconDoubleClick(tag,keywords):

	import os
	v = keywords.get("v")
	commands = keywords.get("c")
	h = v.headString().strip()
	if len(h)==0 or h[0]=='@':
		return # Let other plugins handle these
	else:
		# open file with associated application
		&lt;&lt; find path and start file &gt;&gt;</t>
<t tx="T240"># Set the base directory by searching for @folder directives in ancestors.
try:
	basedir = os.curdir	# use current dir as default.
	parv = v.parent()	# start with parent
	while parv:	# stop when no more parent found
		p = parv.headString().strip()
		if match_word(p,0,'@folder'):
			basedir = p[8:]	# take rest of headline as pathname
			break	# we found the closest @folder
		else:
			parv = parv.parent()	# try the parent of the parent
	fname = os.path.join(basedir,h) # join path and filename
	os.startfile(fname)	# Try to open the file; it may not work for all file types.
except:
	es(os.path.join(os.getcwd(),fname)+' - file or application not found')
	es_exception()
</t>
<t tx="T241"></t>
<t tx="T242">from leoPlugins import *
from leoGlobals import *

Tk = Tkinter

@others

if 0: # Override classes &amp; methods...

	if 0:
		&lt;&lt; override the LeoFrame class &gt;&gt;

	if 0:
		&lt;&lt; override methods of the LeoApp class &gt;&gt;

	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T243"># print "overriding LeoFrame class"

import leoFrame

assert(leoFrame.leoCoreFrame.instances==0)

class myLeoFrame(leoFrame.leoCoreFrame):
	
	pass
	
	if 0:
		def __init__(self,title=None):
			print "myLeoFrame ctor",title
			leoFrame.leoCoreFrame.__init__(self,title)

leoFrame.LeoFrame = myLeoFrame</t>
<t tx="T244">import leoApp

# print "overriding app.closeLeoWindow"

oldAppCloseLeoWindow = app().closeLeoWindow

def myAppCloseLeoWindow(self,frame):
	
	global oldAppCloseLeoWindow

	oldAppCloseLeoWindow(frame)
	print "after closeLeoWindow"

funcToMethod(myAppCloseLeoWindow,leoApp.LeoApp,"closeLeoWindow")</t>
<t tx="T245">"""Override the Equal Sized Pane command"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("command1", onCommand)
	
	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T246">def onCommand (tag,keywords):

	if keywords.get("label")=="equalsizedpanes":
		es("over-riding Equal Sized Panes")
		return "override" # Anything other than None overrides.</t>
<t tx="T247">"""Redefine the "put" and "put_nl" methods"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("start2", onStart)
	
	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T248">@ This code illustrates how to redefine _any_ method of Leo.
Python makes this is almost too easy :-)
@c

def onStart (tag,keywords):

	import leoFrame
	
	# Replace frame.put with newPut.
	funcToMethod(newPut,leoFrame.LeoFrame,"put")
	
	# Replace frame.putnl with newPutNl.
	funcToMethod(newPutNl,leoFrame.LeoFrame,"putnl")
</t>
<t tx="T249"># Contrived examples of how to redefine frame.put and frame.putnl

# Same as frame.put except converts everything to upper case.
def newPut (self,s,color="black"):
	# print "newPut",s,
	if app().quitting &gt; 0: return
	s = s.upper()
	if self.log:
			self.log.insert("end",s)
			self.log.see("end")
			self.log.update_idletasks()
	else: print s,

# Same as frame.putnl except writes two newlines.
def newPutNl (self):
	# print "newPutNl"
	if app().quitting &gt; 0: return
	if self.log:
		self.log.insert("end","\n\n")
		self.log.see("end")
		self.log.update_idletasks()
	else: print</t>
<t tx="T250">"""Send all output to the log pane"""

from leoPlugins import *
from leoGlobals import *

def onStart (tag,keywords):
	from leoGlobals import redirectStdout,redirectStderr
	redirectStdout() # Redirect stdout
	redirectStderr() # Redirect stderr

if 0: # Register the handlers...
	registerHandler("start2", onStart)

	__version__ = "1.3" # Set version for the plugin handler.
	plugin_signon(__name__)

</t>
<t tx="T251">"""Send output from the Execute Script command to the end of the body pane"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("start1", onStart)

	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)
</t>
<t tx="T252">def onStart (tag,keywords):
	
	import leoFrame
	
	# Replace frame.put with newPut.
	funcToMethod(newExecuteScript,leoFrame.LeoFrame,"OnExecuteScript")
</t>
<t tx="T253"># Execute the _selected_ body text as a Python script and sends the output to the end of the body pane.

def newExecuteScript(self,event=None,v=None):
	
	c = self.commands ; body = self.body ; s = None
	if v == None:
		v = c.currentVnode() 

	# Assume any selected body text is a script.
	start,end = getTextSelection(body)
	if start and end and start != end: # 7/7/03
		s = body.get(start,end)
	else:
		s = ""
	s = s.strip()
	if s and len(s) &gt; 0:
		s += '\n' # Make sure we end the script properly.
		try:
			# Switch output.
			import leoFrame,leoGlobals
			oldput = leoFrame.LeoFrame.put
			oldputnl = leoFrame.LeoFrame.putnl
			oldes = leoGlobals.es
			oldenl = leoGlobals.enl
			oldecnl = leoGlobals.ecnl
			oldecnls = leoGlobals.ecnls
			leoGlobals.es = newEs
			leoGlobals.enl = newEnl
			leoGlobals.ecnl = newEcnl
			leoGlobals.ecnls = newEcnls
			funcToMethod(newPut,leoFrame.LeoFrame,"put")
			funcToMethod(newPutNl,leoFrame.LeoFrame,"putNl")
			redirectStderr()
			redirectStdout()
			exec s in {} # Use {} to get a pristine environment!
			# Restore output.
			funcToMethod(oldput,leoFrame.LeoFrame,"put")
			funcToMethod(oldputnl,leoFrame.LeoFrame,"putNl")
			leoGlobals.es = oldes
			leoGlobals.enl = oldenl
			leoGlobals.ecnl = oldecnl
			leoGlobals.ecnls = oldecnls
			restoreStderr()
			restoreStdout()
		except:
			es("exception executing script")
			es_exception(full=false)
	else:
		es("no script selected")
</t>
<t tx="T254"># Same as frame.put except sends output to the end of the body text.
def newPut (self,s):
	if self.body:
			self.body.insert("end",s)
			# self.body.see("end")
			c = self.commands ; v = c.currentVnode()
			self.tree.onBodyChanged(v,"Typing")
	else: print s,

# Same as frame.putnl exceptsends output to the end of the body text.
def newPutNl (self):
	newPut (self,'\n')</t>
<t tx="T255">def newEnl():
	print
	
def newEcnl():
	print
	
def newEcnls(n):
	while n &gt; 0:
		n -= 1
		print

def newEs(s,*args,**keys):
	newline = keys.get("newline",true)
	if type(s) != type("") and type(s) != type(u""):
		s = repr(s)
	for arg in args:
		if type(arg) != type("") and type(arg) != type(u""):
			arg = repr(arg)
		s = s + ", " + arg
	if newline:
		print s
	else:
		print s,
</t>
<t tx="T256"></t>
<t tx="T257">colour
colourful
coloured
</t>
<t tx="T258"># Configuration file for mod_spelling plugin.

[main]

aspell_dir=c:\aspell\bin\aspell.exe

local_leo_dictionary=c:\prog\leoCVS\leo\plugins\mod_spelling.txt

local_language_code=en</t>
<t tx="T259">"""Spell Checker Plugin

- Perfoms spell checking on nodes within a Leo document.
- Uses aspell.exe to do the checking and suggest alternatives."""

import leoFind,os,popen2,re,sys,Tkinter,traceback
from leoPlugins import *
from leoGlobals import *

Tk = Tkinter

@others

if 1: # Register the handlers...

	spellFrame = spellDialog()
	spellFrame.top.withdraw()
	app().globalWindows.append(spellFrame)
	
	registerHandler("create-optional-menus",createSpellMenu)
	registerHandler("select2",onSelect)
	registerHandler("command2",onCommand) # For any command that might change the text.
	registerHandler("bodykey2",onSelect) # For updating buttons.
	registerHandler(("bodyclick2","bodydclick2","bodyrclick2"),onSelect) # These affect selection.
	
	__version__ = "0.2.0"
	plugin_signon(__name__)</t>
<t tx="T260"></t>
<t tx="T261">def createSpellMenu(tag,keywords):
	
	"""Create the Check Spelling menu item in the Edit menu."""
	
	c = keywords.get("c")

	table = (
		("-",None,None),
		("Check Spelling","Alt+Shift+A",spellFrame.checkSpelling))

	c.frame.createMenuItemsFromTable("Edit",table)</t>
<t tx="T262">def onSelect (tag,keywords):
	
	"""A new vnode has just been selected.  Update the Spell Check window."""

	c = keywords.get("c")
	v = keywords.get("new_v")
	global spellFrame
	
	if top() and c and c.currentVnode():
		if c.currentVnode() != spellFrame.v:
			# print "onSelect",tag,`c.currentVnode()`,`spellFrame.v`
			spellFrame.update(show=false,fill=true)
		else:
			spellFrame.updateButtons()</t>
<t tx="T263">def onCommand (tag,keywords):
	
	"""Update the Spell Check window after any command that might change text."""

	global spellFrame
	
	if top() and top().currentVnode():
		
		# print "onCommand",tag
		spellFrame.update(show=false,fill=false)</t>
<t tx="T264">class Aspell:
	
	"""A wrapper class for Aspell spell checker"""
	
	@others
</t>
<t tx="T265"></t>
<t tx="T266">def __init__(self,local_dictionary_file,local_language_code):
	
	"""Ctor for the Aspell class."""
	
	self.altre = re.compile(".\s(.+)\s(\d+)\s(\d+):(.*)")
	self.attached = None
	self.input,self.output = None,None
	self.signonGiven = false
	
	self.aspell_exe_loc = self.getAspellDirectory()
	self.local_language_code = local_language_code
	
	if local_dictionary_file:
		self.local_dictionary_file = local_dictionary_file
		self.local_dictionary = "%s.wl" % os.path.splitext(local_dictionary_file)[0]
	else:
		print "failed to set aspell.local_dictionary"
		self.local.dictionary_file = None
		self.local_dictionary = None</t>
<t tx="T267">def getAspellDirectory(self):
	
	"""Get the directory containing aspell.exe from mod_spelling.ini"""

	import ConfigParser

	try:
		fileName = os.path.join(app().loadDir,"../","plugins","mod_spelling.ini")
		config = ConfigParser.ConfigParser()
		config.read(fileName)
		return config.get("main","aspell_dir")
	except:
		es_exception()
		return None</t>
<t tx="T268">def openPipes (self):
	
	"""Open the pipes to aspell.exe"""
	
	if self.input or self.output:
		print "pipes already open!"
		self.closePipes()
	
	&lt;&lt; Ensure local dictionary is present &gt;&gt;
	cmd = "%s pipe %s" % (self.aspell_exe_loc, add_dicts)
	if not self.local_dictionary:
		print "openPipes: command = " + cmd
	
	try:
		self.input, self.output = popen2.popen2(cmd)
	except:
		print "exception opening pipe"
		self.input = self.output = None
	
	if self.input:
		self.attached = self.input.readline()
	else:
		self.attached = None
		
	if not self.signonGiven:
		self.signonGiven = true
		if self.attached:
			print self.attached
			es(self.attached,color="blue")
		else:
			print "can not open aspell"
			es("can not open aspell",color="red")</t>
<t tx="T269">add_dicts = ""

if self.local_dictionary:
	if self.updateDictionary():
		add_dicts = "--add-extra-dicts %s" % self.local_dictionary


</t>
<t tx="T270">def closePipes (self):
	
	"""Close the pipes to aspell.exe"""
	
	# if self.input or self.output: print "closePipes"
	
	if self.input:
		self.input.close()
		self.input = None

	if self.output:
		self.output.close()
		self.output = None</t>
<t tx="T271">def listAlternates(self, aspell_return):
	
	"""Return a list of alternates from aspell."""
	
	match = self.altre.match(aspell_return)

	if match:
		return [item.strip() for item in match.groups()[3].split(",")]
	else:
		return []</t>
<t tx="T272">def processWord(self, word):

	"""Pass a word to aspell and return the list of alternatives."""
	
	if not self.attached:
		return None

	# print "processWord",`word`,`self.output`
	
	self.output.write("%s\n" % word)
	
	ret,junk = self.input.readline(),self.input.readline()

	if ret == "*\n":
		return None
	else:
		return self.listAlternates(ret)</t>
<t tx="T273">def updateDictionary(self):
	
	"""Update the aspell dictionary from a list of words.
	
	Return true if the dictionary was update correctly."""

	try:
		# Create master list
		basename = os.path.splitext(self.local_dictionary)[0]
		cmd = (
			"%s --lang=%s create master %s.wl &lt; %s.txt" %
			(self.aspell_exe_loc,self.local_language_code,basename,basename))
		os.popen(cmd)
		return true

	except Exception, err:
		es("Unable to update local aspell dictionary: %s" % err)
		print err
		add_dicts = ""
		return false</t>
<t tx="T274">class spellDialog (leoFind.leoFindBase):
	
	"""A class to create and manage Leo's Spell Check dialog."""
	
	@others</t>
<t tx="T275"></t>
<t tx="T276">def __init__ (self):
	
	"""Ctor for the Leo Spelling dialog."""
	
	# Call the base ctor to create the dialog.
	leoFind.leoFindBase.__init__(self,"Leo Spell Checking",resizeable=false)
	
	self.local_dictionary_file = self.getLocalDictionary()
	self.local_language_code = self.getLocalLanguageCode("en")
	self.aspell = Aspell(self.local_dictionary_file,self.local_language_code)
	&lt;&lt; set self.dictionary &gt;&gt;
	
	self.createFrame()
	self.fillbox([])
	
	# State variables.
	self.currentWord = None
	self.suggestions = []
	self.c = None
	self.v = None
	self.body = None
	self.work = Tk.Text(None) # A text widget for scanning.

	self.listBox.bind("&lt;Double-Button-1&gt;",self.onChangeThenFindButton)
	self.listBox.bind("&lt;Button-1&gt;",self.onSelectListBox)
	self.listBox.bind("&lt;Map&gt;",self.onMap)</t>
<t tx="T277">if self.local_dictionary_file:

	self.dictionary = self.readLocalDictionary(self.local_dictionary_file)
	if self.dictionary:
		# print "Local dictionary:", self.local_dictionary_file
		es("Local dictionary: %s" % shortFileName(self.local_dictionary_file),color="blue")
		if 0:
			keys = self.dictionary.keys()
			keys.sort()
			print "local dict:", keys
	else:
		self.dictionary = {}
		self.local_dictionary_file = None
else:
	self.dictionary = {}</t>
<t tx="T278">def getLocalDictionary(self):
	
	"""Get the dictionaries containing words not in the standard dictionary from mod_spelling.ini"""

	import ConfigParser

	try:
		fileName = os.path.join(app().loadDir,"../","plugins","mod_spelling.ini")
		config = ConfigParser.ConfigParser()
		config.read(fileName)
		return config.get("main","local_leo_dictionary",None)
	except:
		es_exception()
		return None</t>
<t tx="T279">def getLocalLanguageCode(self,defaultLanguageCode):
	
	"""Get the dictionaries containing words not in the standard dictionary from mod_spelling.ini"""

	import ConfigParser

	try:
		fileName = os.path.join(app().loadDir,"../","plugins","mod_spelling.ini")
		config = ConfigParser.ConfigParser()
		config.read(fileName)
		return config.get("main","local_language_code",defaultLanguageCode)
	except:
		es_exception()
		return defaultLanguageCode</t>
<t tx="T280">def readLocalDictionary (self,local_dictionary):
	
	"""Read the dictionary of words which we use as a local dictionary
	
	Although Aspell itself has the functionality to handle this kind of things
	we duplicate it here so that we can also use it for the "ignore" functionality
	and so that in future a Python only solution could be developed."""

	try:
		f = open(local_dictionary,"r")
	except IOError:
		es("Unable to open local dictionary '%s' - using a blank one instead" % local_dictionary)
		return None
	
	try:
		# Create the dictionary - there are better ways to do this
		# in later Python's but we stick with this method for compatibility
		dct = {}
		for word in f.readlines():
			dct[word.strip().lower()] = 0
	finally:
		f.close()

	return dct</t>
<t tx="T281">def createFrame (self):
	
	"""Create the Spelling dialog."""
	
	# Create the find panel...
	outer = Tk.Frame(self.frame,relief="groove",bd=2)
	outer.pack(padx=2,pady=2,expand=1,fill="both")

	&lt;&lt; Create the text and suggestion panes &gt;&gt;
	&lt;&lt; Create the spelling buttons &gt;&gt;
</t>
<t tx="T282">f = outer

f2 = Tk.Frame(f)
f2.pack(expand=1,fill="x")
self.wordLabel = Tk.Label(f2, text="Suggestions for:")
self.wordLabel.pack(side="left")

fpane = Tk.Frame(f,bd=2)
fpane.pack(side="top", expand=1, fill="x")

self.listBox = Tk.Listbox(fpane,height=30,selectmode="single")
self.listBox.pack(side="left", expand=1, fill="both")

listBoxBar = Tk.Scrollbar(fpane,name='listBoxBar')

for bar,txt in ((listBoxBar,self.listBox),):
	txt['yscrollcommand'] = bar.set
	bar['command'] = txt.yview
	bar.pack(side="right", fill="y")
</t>
<t tx="T283"># Create the button panes
buttons1  = Tk.Frame(outer,bd=1)
buttons1.pack (anchor="n",expand=1,fill="x")

buttons2  = Tk.Frame(outer,bd=1)
buttons2.pack (anchor="n",expand=1,fill="none")

buttonList = []
for text,command in (
	("Find",self.onFindButton),
	("Change",self.onChangeButton),
	("Change, Find",self.onChangeThenFindButton),
	("Add",self.onAddButton)):
	width = max(6,len(text))
	b=Tk.Button(buttons1,width=width,text=text,command=command)
	b.pack(side="left",fill="none",expand=1)
	buttonList.append(b)
		
for text,command in (
	("Undo",self.onUndoButton),
	("Redo",self.onRedoButton),
	("Ignore",self.onIgnoreButton),
	("Hide",self.onHideButton)):
	width = max(6,len(text))
	b=Tk.Button(buttons2,width=width,text=text,command=command)
	b.pack(side="left",fill="none",expand=0)
	buttonList.append(b)

# We need these to enable or disable buttons.
(self.findButton, self.changeButton,
 self.changeFindButton, self.addButton, 
 self.undoButton, self.redoButton,
 self.ignoreButton, self.hideButton) = buttonList</t>
<t tx="T284"></t>
<t tx="T285">def onAddButton (self):
	
	"""Handle a click in the Add button in the Check Spelling dialog."""

	self.add()
	self.closePipes()

</t>
<t tx="T286">def onIgnoreButton (self):

	"""Handle a click in the Ignore button in the Check Spelling dialog."""

	self.ignore()
	self.closePipes()</t>
<t tx="T287">def onChangeButton (self):
	
	"""Handle a click in the Change button in the Check Spelling dialog."""

	self.change()
	self.closePipes()
	self.updateButtons()
	
# Event needed for double-click event.
def onChangeThenFindButton (self,event=None): 
		
	"""Handle a click in the "Change, Find" button in the Check Spelling dialog."""

	if self.change():
		self.find()
	self.closePipes()
	self.updateButtons()</t>
<t tx="T288">def onFindButton (self):
	
	"""Handle a click in the Find button in the Check Spelling dialog."""

	self.find()
	self.updateButtons()
	self.closePipes()</t>
<t tx="T289">def onHideButton (self):
	
	"""Handle a click in the Hide button in the Check Spelling dialog."""

	self.closePipes()
	self.top.withdraw()
</t>
<t tx="T290">def onRedoButton (self):
	
	"""Handle a click in the Redo button in the Check Spelling dialog."""

	self.c.undoer.redo() # Not a command, so command hook doesn't fire.
	self.update(show=false,fill=false)
	self.c.frame.body.focus_force()
	
def onUndoButton (self):
	
	"""Handle a click in the Undo button in the Check Spelling dialog."""

	self.c.undoer.undo() # Not a command, so command hook doesn't fire.
	self.update(show=false,fill=false)
	self.c.frame.body.focus_force()</t>
<t tx="T291"></t>
<t tx="T292">def add (self):

	"""Add the selected suggestion to the dictionary."""
	
	if not self.local_dictionary_file:
		return
	
	try:
		f = None
		try:
			# Rewrite the dictionary in alphabetical order.
			f = open(self.local_dictionary_file,"r")
			words = f.readlines()
			f.close()
			words = [word.strip() for word in words]
			words.append(self.currentWord)
			words.sort()
			f = open(self.local_dictionary_file,"w")
			for word in words:
				f.write("%s\n" % word)
			f.flush()
			f.close()
			es("Adding ",color="blue",newline=false) ; es('%s' % self.currentWord)
		except IOError:
			es("Can not add %s to dictionary" % self.currentWord,color="red")
	finally:
		if f: f.close()
		
	self.dictionary[self.currentWord.lower()] = 0
	
	# Restart aspell so that it re-reads its dictionary.
	self.aspell.closePipes()
	self.aspell.openPipes()
	
	self.onFindButton()</t>
<t tx="T293">def change(self):
	
	"""Make the selected change to the text"""

	c = self.c ; v = self.v ; t = self.body
	
	selection = self.getSuggestion()
	if selection:
		start,end = oldSel = getTextSelection(t)
		if start:
			if t.compare(start, "&gt;", end):
				start,end = end,start
			t.delete(start,end)
			t.insert(start,selection)
			setTextSelection(t,start,start + "+%dc" % (len(selection)))
			newSel = getTextSelection(t)

			# update node, undo status, dirty flag, changed mark &amp; recolor
			c.beginUpdate()
			c.tree.onBodyChanged(v,"Change",oldSel=oldSel,newSel=newSel)
			c.endUpdate(true)
			t.focus_set()
			return true

	# The focus must never leave the body pane.
	t.focus_set()
	return false</t>
<t tx="T294">def checkSpelling (self,event=None):
	
	"""Open the Check Spelling dialog."""

	self.top.deiconify()
	self.top.lift()
	self.update(show=true,fill=false)</t>
<t tx="T295">def find(self):
	
	"""Find the next unknown word."""
	
	# Reload the work pane from the present node.
	s = self.body.get("1.0","end").rstrip()
	self.work.delete("1.0","end")
	self.work.insert("end",s)
	
	# Reset the insertion point of the work widget.
	ins = self.body.index("insert")
	self.work.mark_set("insert",ins)

	alts,word = self.findNextMisspelledWord()
	self.currentWord = word # Need to remember this for 'add' and 'ignore'
	
	if alts:
		self.fillbox(alts,word)
		self.body.focus_set()
					
		# Copy the working selection range to the body pane
		start,end = getTextSelection (self.work)
		setTextSelection (self.body,start,end)
	else:
		es("no more misspellings")
		self.fillbox([])</t>
<t tx="T296">def ignore (self):
	
	"""Ignore the incorrect word for the duration of this spell check session."""
	
	es("Ignoring ",color="blue",newline=false) ; es('%s' % self.currentWord)
	self.dictionary[self.currentWord.lower()] = 0
	self.onFindButton()</t>
<t tx="T297"></t>
<t tx="T298">def closePipes(self):
	
	self.aspell.closePipes()</t>
<t tx="T299">def fillbox(self,alts,word=None):

	"""Update the suggestions listbox in the Check Spelling dialog."""
	
	self.suggestions = alts
	
	if not word:
		word = ""

	self.wordLabel.configure(text = "Suggestions for: " + word)
	self.listBox.delete(0,"end")

	for i in xrange(len(self.suggestions)):
		self.listBox.insert(i,self.suggestions[i])
	
	if len(self.suggestions):
		self.listBox.select_set(1) # This doesn't show up because we don't have focus.</t>
<t tx="T300">def findNextMisspelledWord(self):
	
	"""Find the next unknown word."""
	
	aspell = self.aspell ; alts = None ; word = None
	c = self.c ; v = self.v
	try:
		aspell.openPipes()
		try:
			while 1:
				v,word = self.findNextWord(v) 
				if not v or not word:
					alts = None
					break
				&lt;&lt; Skip word if ignored or in local dictionary &gt;&gt;
				alts = aspell.processWord(word)
				if alts:
					self.v = v
					c.beginUpdate()
					c.tree.expandAllAncestors(v)
					c.selectVnode(v)
					c.endUpdate()
					break
		except:
			es_exception()
	finally:
		aspell.closePipes()
		return alts, word</t>
<t tx="T301">@ We don't bother to call apell if the word is in our dictionary. The dictionary contains both locally 'allowed' words and 'ignored' words. We put the test before aspell rather than after aspell because the cost of checking aspell is higher than the cost of checking our local dictionary. For small local dictionaries this is probably not true and this code could easily be located after the aspell call
@c

if self.dictionary.has_key(word.lower()):
	
	# print "Ignored", word
	continue
	
# print "Didn't ignore '%s'" % word</t>
<t tx="T302">def findNextWord (self,v):
	
	"""Scan for the next word, leaving the result in the work widget"""

	t = self.work
	word_start = string.letters + '_'
	t.mark_set("insert","insert wordend + 1c")
	while 1:
		# print `t.index("insert")`,`t.index("end-1c")`
		if t.compare("insert","&gt;=","end - 1c"):
			v = v.threadNext()
			if not v: return None,None
			t.delete("1.0","end")
			t.insert("end",v.bodyString())
			t.mark_set("insert","1.0")
		elif t.compare("insert","&gt;=","insert lineend - 1c"):
			t.mark_set("insert","insert lineend + 1line")
		else:
			ch = t.get("insert")
			if ch in word_start:
				word = t.get("insert wordstart","insert wordend")
				setTextSelection(t,"insert wordstart","insert wordend")
				# print "findNextWord:",`word`
				return v,word
			elif ch:
				t.mark_set("insert","insert + 1c")</t>
<t tx="T303">def getSuggestion (self):
	
	"""Return the selected suggestion from the listBox."""
	
	# Work around an old Python bug.  Convert strings to ints.
	items = self.listBox.curselection()
	try:
		items = map(int, items)
	except ValueError: pass

	if items:
		n = items[0]
		suggestion = self.suggestions[n]
		return suggestion
	else:
		return None</t>
<t tx="T304">def onMap (self,event=None):
	
	"""Respond to a Tk &lt;Map&gt; event."""
	
	self.update(show=false,fill=false)</t>
<t tx="T305">def onSelectListBox (self,event=None):
	
	"""Respond to a click in the selection listBox."""
	
	self.updateButtons()
	self.body.focus_set()
</t>
<t tx="T306">def update (self,show=true,fill=false):
	
	"""Update the Spell Check dialog."""
	
	# print "update(show=%d,fill=%d)" % (show,fill)
	
	# Always assume that the user has changed text.
	self.c = c = top()
	self.v = c.currentVnode()
	self.body = c.frame.body
	if fill:
		self.fillbox([])
	self.updateButtons()
	if show:
		self.top.deiconify()
		# Don't interfere with Edit Headline commands.
		self.body.focus_set()
		
	# Give the signon if it hasn't been given yet.
	if not self.aspell.signonGiven:
		self.aspell.openPipes()
		self.aspell.closePipes()</t>
<t tx="T307">def updateButtons (self):
	
	"""Enable or disable buttons in the Check Spelling dialog."""
	
	start,end = getTextSelection(self.body)
	state = choose(self.suggestions and start,"normal","disabled")
	
	self.changeButton.configure(state=state)
	self.changeFindButton.configure(state=state)

	state = choose(self.c.undoer.canRedo(),"normal","disabled")
	self.redoButton.configure(state=state)
	
	state = choose(self.c.undoer.canUndo(),"normal","disabled")
	self.undoButton.configure(state=state)
	
	state = choose(self.local_dictionary_file,"normal","disabled")
	self.addButton.configure(state=state)

	self.ignoreButton.configure(state="normal")</t>
<t tx="T308"></t>
<t tx="T309"></t>
<t tx="T310">[Main]
active = Yes
interval = 600

</t>
<t tx="T311">"""Autosave the Leo document every so often"""

# By Paul Paterson.

from leoPlugins import *
from leoGlobals import *

import ConfigParser
import time, os

@others

if 0: # Register the handlers...

	AUTOSAVE_INTERVAL = 600
	ACTIVE = "Yes"
	LAST_AUTOSAVE = time.time()
	applyConfiguration()

	__version__ = "0.1"
	registerHandler("idle", autosave)
	es("auto save")
</t>
<t tx="T312">def applyConfiguration(config=None):
	
	"""Called when the user presses the "Apply" button on the Properties form"""

	global LAST_AUTOSAVE, ACTIVE, AUTOSAVE_INTERVAL

	if config is None:
		fileName = os.path.join(app().loadDir,"../","plugins","mod_autosave.ini")
		config = ConfigParser.ConfigParser()
		config.read(fileName)

	ACTIVE = config.get("Main", "Active")
	AUTOSAVE_INTERVAL = int(config.get("Main", "Interval"))</t>
<t tx="T313">def autosave(tag, keywords):
	
	"""Save the current document if it has a name"""

	global LAST_AUTOSAVE

	if ACTIVE == "Yes":
		if time.time() - LAST_AUTOSAVE &gt; AUTOSAVE_INTERVAL:
			f = top().frame
			if f.mFileName and f.commands.changed:
				es("Autosave: %s" % time.ctime())
				f.commands.fileCommands.save(f.mFileName)
			LAST_AUTOSAVE = time.time()</t>
<t tx="T314">"""Timestamp all save operations to show when they occur"""

# By Paul Paterson.

from leoPlugins import *
from leoGlobals import *

import time
	
@others

if 0: # Register the handlers...

	registerHandler("command1", timestamp)

	__version__ = "0.1" # Set version for the plugin handler.
	plugin_signon(__name__)</t>
<t tx="T315">def timestamp(tag=None, keywords=None):
	
	cmd = keywords.get('label', 'save')

	if cmd.startswith("save") or cmd.startswith("tangle"):
		es("%s: %s" % (cmd, time.ctime()))
</t>
<t tx="T316"></t>
<t tx="T317">@nocolor

Allow different default types for each section.
Create _all_ menus from settings ?

[plugins]

pluginName = 1/0 # enables or disables plugin

# option = type (overrides defaults)

	[types]

__default_type = bool
page_width = int
tab_width = int
default_tangle_directory = string

	use type name in option?
	
	_color: color
	
	_font: font
	_key: keystroke
	_flag: bool
	everything else: bool
	
	bool: checkmark
	color: picker (or use dialog)

[menus]
child = parent</t>
<t tx="T318"></t>
<t tx="T319">"""Create a settings menu to replace LeoConfig.leo"""

from leoPlugins import *
from leoGlobals import *

import leoApp,leoAtFile,leoDialog,leoFileCommands,leoFrame,leoNodes

if 0: # Register the handlers...

	settingsMenu = None

	@others
	
	# registerHandler("start1",onAfterFinishCreate)
	registerHandler("create-optional-menus",createSettingsMenu)

	__version__ = "0.1"
	plugin_signon(__name__)</t>
<t tx="T320">def createSettingsMenu (tag,keywords):

	c = keywords.get("c")
	
	global settingsMenu
	settingsMenu = c.frame.createNewMenu("&amp;Settings")</t>
<t tx="T321">@ignore

@ This code will soon become a plugin replaces Tk widgets with wxPython widgets.

To do:
	
- Convert the code in wxLeo.py to a plugin that overrides Leo's actual code.

- Override all of Leo's classes that contain Tk code, replacing Tk code with equivalent wxWindows code.

This will include the LeoDialog, LeoFrame and leoTree classes, and many others.  In particular, the colorizer will have to be rewritten.</t>
<t tx="T322"># Executing the following script executes some example wxWindows code.
# Just do the Execute Script command from here.
# For this to work the path to wxTest.py must be in sys.path.

# The first time you do this the window is created twice: once for the import and once for the reload.
# Thereafter only the reload takes effect, so only one window gets created.
# The purpose of reload is so you can change the code without restarting Leo.

import wxTest
reload(wxTest)</t>
<t tx="T323">from wxPython.wx import *

class Form1(wxPanel):
    def __init__(self, parent, id):
        wxPanel.__init__(self, parent, -1)
        self.quote = wxStaticText(self, -1, "Your quote :",wxPoint(20, 30))

        # A multiline TextCtrl
        self.logger = wxTextCtrl(self,5, "",wxPoint(300,20), wxSize(200,300),wxTE_MULTILINE | wxTE_READONLY)

        # A button
        self.button =wxButton(self, 10, "Save", wxPoint(200, 300))
        EVT_BUTTON(self, 10, self.OnClick)

        # the edit control - one line version.
        self.lblname = wxStaticText(self, -1, "Your name :",wxPoint(20,60))
        self.editname = wxTextCtrl(self, 20, "Enter here your name", wxPoint(150, 60), wxSize(150, -1))
        EVT_TEXT(self, 20, self.EvtText)
        EVT_CHAR(self.editname, self.EvtChar)

        # the combobox Control
        self.sampleList = ['friends', 'advetising', 'Websearch', 'yellowpages']
        self.lblhear = wxStaticText(self,-1,"How did you hear from us ?",wxPoint(20, 90))
        self.edithear=wxComboBox(self, 30, "", wxPoint(150, 90), wxSize(95, -1),
                   self.sampleList, wxCB_DROPDOWN)
        EVT_COMBOBOX(self, 30, self.EvtComboBox)
        EVT_TEXT(self, 30, self.EvtText)
        # Checkbox
        self.insure = wxCheckBox(self, 40, "Do you want Insured Shipment ?",wxPoint(20,180))
        EVT_CHECKBOX(self, 40,   self.EvtCheckBox)
        # Radio Boxes
        self.radioList = ['blue', 'red', 'yellow', 'orange', 'green', 'purple',
                      'navy blue', 'black', 'gray']

        rb = wxRadioBox(self, 50, "What color would you like ?", wxPoint(20, 210), wxDefaultSize,
                        self.radioList, 3, wxRA_SPECIFY_COLS)
        EVT_RADIOBOX(self, 50, self.EvtRadioBox)
    def EvtRadioBox(self, event):
        self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())
    def EvtComboBox(self, event):
        self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())
    def OnClick(self,event):
        self.logger.AppendText(" Click on object with Id %d\n" %event.GetId())
    def EvtText(self, event):
        self.logger.AppendText('EvtText: %s\n' % event.GetString())
    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()
    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())

class Form2(wxPanel):
    def __init__(self, parent, id):
        wxPanel.__init__(self, parent, -1)
        self.sampleList = ['friends', 'advetising', 'Websearch', 'yellowpages']
        self.radioList = ['blue', 'red', 'yellow', 'orange', 'green', 'purple',
                      'navy blue', 'black', 'gray']
        gs = wxFlexGridSizer(5,2,5,5)
        gs.Add(wxStaticText(self, -1, "Your name :"),0,wxEXPAND)
        self.editname=wxTextCtrl(self, 20, "Enter here your name")
        gs.Add(self.editname,0,wxEXPAND)
        EVT_TEXT(self, 20, self.EvtText)
        EVT_CHAR(self.editname, self.EvtChar)
        gs.Add(wxStaticText(self,-1,"How did you hear from us ?"),0,wxEXPAND)
        gs.Add(wxComboBox(self, 30, "", wxPoint(-1,-1),wxSize(-1,-1), self.sampleList, wxCB_DROPDOWN),0,wxEXPAND)
        EVT_COMBOBOX(self, 30, self.EvtComboBox)
        EVT_TEXT(self, 30, self.EvtText)
        gs.Add(60, 20, 0, wxEXPAND)
        gs.Add(wxCheckBox(self, 40, "Do you want Insured Shipment ?"),0,wxEXPAND)
        EVT_CHECKBOX(self, 40,   self.EvtCheckBox)
        gs.Add(60, 20, 0, wxEXPAND)
        gs.Add(wxRadioBox(self, 50, "What color would you like ?", wxPoint(-1,-1),wxDefaultSize,
                        self.radioList, 3, wxRA_SPECIFY_COLS),0,wxEXPAND)
        EVT_RADIOBOX(self, 50, self.EvtRadioBox)
        gs.Add(60, 20, 0, wxEXPAND)
        gs.Add(wxButton(self, 10, "Save"),0,wxALIGN_CENTER)
        EVT_BUTTON(self, 10, self.OnClick)
        # gs.AddGrowableRow(0)
        boxh = wxBoxSizer(wxHORIZONTAL)
        boxh.Add(gs,0,wxEXPAND)

        self.logger=wxTextCtrl(self,5, "",wxPoint(-1,-1),wxSize(-1,-1),wxTE_MULTILINE | wxTE_READONLY)
        boxh.Add( self.logger
                  ,1,wxEXPAND)

        self.sizer = boxh
        self.sizer.Fit(self)
        self.SetAutoLayout(true)
        self.SetSizer(self.sizer)
    def EvtRadioBox(self, event):
        self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())
    def EvtComboBox(self, event):
        self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())
    def OnClick(self,event):
        self.logger.AppendText(" Click on object with Id %d\n" %event.GetId())
    def EvtText(self, event):
        self.logger.AppendText('EvtText: %s\n' % event.GetString())
    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\n' % event.GetKeyCode())
        event.Skip()
    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox: %d\n' % event.Checked())


app = wxPySimpleApp()
frame = wxFrame(None,-1," Demo with Notebook")
nb = wxNotebook(frame,-1)
form1=Form1(nb, -1)
form2=Form2(nb,-1)
nb.AddPage(form1, "Absolute Positionning")
nb.AddPage(form2, "Sizers")
frame.Show(True)
app.MainLoop()</t>
<t tx="T324">@language c

@ For reference only: I have deleted the C++ cruft such as importing .h files.

To do:
- convert wxWindows code to wxPython code.
- move the wxPython code to the wx plugin that doesn't exist yet.</t>
<t tx="T325">@others</t>
<t tx="T326">void alert ( const char * message )
{
	wxMessageDialog * d = new wxMessageDialog( (wxWindow*) NULL,
		message,
		"Alert",
		wxOK |wxCENTRE,
		wxDefaultPosition);

	d -&gt; ShowModal();
	delete d;
}
</t>
<t tx="T327">void assertFailedDialog ( const char * message )
{
	wxMessageDialog * d = new wxMessageDialog( (wxWindow*) NULL,
		message,
		"Leo assert failed",
		wxOK |wxCENTRE,
		wxDefaultPosition);

	d -&gt; ShowModal();
	delete d;
}
</t>
<t tx="T328">&lt;&lt; FindPanel declarations &gt;&gt;

@others
</t>
<t tx="T329">// &lt;&lt; FindPanel public globals &gt;&gt;
bool reset_search_flag ;
bool batch_flag ;
bool wrap_flag ;
bool whole_word_flag ;
bool ignore_case_flag ;
bool pattern_match_flag ;
bool search_headline_flag ;
bool search_body_flag ;
bool suboutline_only_flag ;
bool mark_changes_flag ;
bool mark_finds_flag ;
bool reverse_flag ;
wxString find_text ("")  ;
wxString change_text ("") ;
</t>
<t tx="T330">BEGIN_EVENT_TABLE(FindFrame, wxFrame)

	#ifdef __WXMSW__ // Activate events exist only on windows.
		EVT_ACTIVATE( FindFrame::OnActivateFindFrame )
	#else
		EVT_SET_FOCUS( FindFrame::OnSetFocus )
	#endif

	EVT_CLOSE( FindFrame::OnCloseFindFrame)

	EVT_BUTTON( cChangeButton,			FindFrame::OnChangeButton )
	EVT_BUTTON( cChangeAllButton,		FindFrame::OnChangeAllButton )
	EVT_BUTTON( cChangeThenFindButton,	FindFrame::OnChangeThenFindButton )
	EVT_BUTTON( cFindButton,			FindFrame::OnFindButton )
	EVT_BUTTON( cFindAllButton,			FindFrame::OnFindAllButton )

	EVT_CHECKBOX ( cBatchCheckBox,		FindFrame::OnBatchCheckBox )
	EVT_CHECKBOX ( cIgnoreCaseCheckBox, FindFrame::OnIgnoreCaseCheckBox )
	EVT_CHECKBOX ( cMarkChangesCheckBox,FindFrame::OnMarkChangesCheckBox )
	EVT_CHECKBOX ( cMarkFindsCheckBox, 	FindFrame::OnMarkFindsCheckBox )
	EVT_CHECKBOX ( cPatternMatchCheckBox, FindFrame::OnPatternMatchCheckBox )
	EVT_CHECKBOX ( cReverseCheckBox, 	FindFrame::OnReverseCheckBox )
	EVT_CHECKBOX ( cSearchHeadlineCheckBox,	FindFrame::OnSearchHeadlineCheckBox )
	EVT_CHECKBOX ( cSearchBodyTextCheckBox, FindFrame::OnSearchBodyTextCheckBox )
	EVT_CHECKBOX ( cSuboutlineOnlyCheckBox, FindFrame::OnSuboutlineOnlyCheckBox )
	EVT_CHECKBOX ( cWrapAroundCheckBox,	FindFrame::OnWrapAroundCheckBox )
	EVT_CHECKBOX ( cWholeWordCheckBox,	FindFrame::OnWholeWordCheckBox )

	EVT_TEXT ( cFindTextCtrl,	FindFrame::OnFindText )
	EVT_TEXT ( cChangeTextCtrl, FindFrame::OnChangeText )

END_EVENT_TABLE()</t>
<t tx="T331">FindFrame::FindFrame()

	: wxFrame((wxFrame *)NULL, -1, "Leo Find/Change",
		wxPoint(50, 50), wxDefaultSize,
		wxMINIMIZE_BOX | wxTHICK_FRAME | wxSYSTEM_MENU | wxCAPTION)
{
	mFindPanel = new FindPanel(this);

	// Resize to fit the panel.
	wxBoxSizer * sizer = new wxBoxSizer(wxVERTICAL);
	sizer -&gt; Add ( mFindPanel );
	SetAutoLayout( TRUE );  // tell dialog to use sizer
	SetSizer( sizer );  // actually set the sizer
	sizer -&gt; Fit( this ); // set size to minimum size as calculated by the sizer
	sizer -&gt; SetSizeHints( this ); // set size hints to honour mininum size

	// Set the window icon.
	#ifdef __WXMSW__
	  this -&gt;SetIcon(wxIcon("LeoIcon"));
	#endif

	// Set the focus.
	if (mFindPanel &amp;&amp; mFindPanel -&gt; mFindText )
		mFindPanel -&gt; mFindText -&gt; SetFocus();
}
</t>
<t tx="T332">@ &lt;&lt; FindPanel methods &gt;&gt; (2 of 23)
@c

#ifdef __WXMSW__ // This event exists only on Windows.

void FindFrame::OnActivateFindFrame(wxActivateEvent&amp; event)
{
	if ( event . GetActive() ) {
		this -&gt; set_check_boxes();
		assert(mFindPanel &amp;&amp; mFindPanel -&gt; mFindText);
		wxTextCtrl *c = mFindPanel -&gt; mFindText ;
		wxString s = c -&gt; GetValue() ;
			c -&gt; SetFocus();
		c -&gt; SetSelection ( 0, s.Length() ) ;
	}
}
</t>
<t tx="T333">
#else

void FindFrame::OnSetFocus (wxFocusEvent&amp; WXUNUSED(event))
{
	this -&gt; set_check_boxes();
	assert(mFindPanel &amp;&amp; mFindPanel -&gt; mFindText);
	wxTextCtrl *c = mFindPanel -&gt; mFindText ;
	wxString s = c -&gt; GetValue() ;
		c -&gt; SetFocus();
	c -&gt; SetSelection ( 0, s.Length() ) ;
}
</t>
<t tx="T334">
#endif
// &lt;&lt; FindPanel methods &gt;&gt; (3 of 23)
/*
	This is an event handler function called when the user has tried to close a frame or dialog box. It is called via the 
	wxWindow::Close function, so that the application can also invoke the handler programmatically.
	
	You should check whether the application is forcing the deletion of the window using CanVeto. If CanVeto returns FALSE, it is 
	not possible to skip window deletion; destroy the window using wxWindow::Destroy. If not, it is up to you whether you respond 
	by destroying the window.
	
	If you don't destroy the window, you should call wxCloseEvent::Veto to let the calling code know that you did not destroy the 
	window. This allows the wxWindow::Close function to return TRUE or FALSE depending on whether the close instruction was 
	honoured or not.
*/
void FindFrame::OnCloseFindFrame(wxCloseEvent&amp; event)
{
	if ( event.CanVeto() ) {
		event.Veto();  // Did not destroy the window.
		this -&gt; Show(FALSE);  // Just hide the window.
	}
	else {
		this -&gt; Destroy();
		gFindFrame = NULL ;
	}
}
</t>
<t tx="T335">@ &lt;&lt; FindPanel methods &gt;&gt; (4 of 23)
@c

void FindFrame::OnChangeButton (wxCommandEvent&amp; WXUNUSED(event))
{
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; doChangeButton() ;
}
</t>
<t tx="T336">@ &lt;&lt; FindPanel methods &gt;&gt; (5 of 23)
@c

void FindFrame::OnChangeAllButton (wxCommandEvent&amp; WXUNUSED(event))
{
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; doChangeAllButton() ;
}
</t>
<t tx="T337">@ &lt;&lt; FindPanel methods &gt;&gt; (6 of 23)
@c

void FindFrame::OnChangeThenFindButton (wxCommandEvent&amp; WXUNUSED(event))
{
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; doChangeThenFindButton() ;
}
</t>
<t tx="T338">@ &lt;&lt; FindPanel methods &gt;&gt; (7 of 23)
@c

void FindFrame::OnFindButton (wxCommandEvent&amp; WXUNUSED(event))
{
	// This is the default button, so make sure there is find text.
	if ( gActiveFrame &amp;&amp; find_text.Length() &gt; 0 )
		gActiveFrame -&gt; mCommands -&gt; doFindButton() ;
}
</t>
<t tx="T339">@ &lt;&lt; FindPanel methods &gt;&gt; (8 of 23)
@c

void FindFrame::OnFindAllButton (wxCommandEvent&amp; WXUNUSED(event))
{
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; doFindAllButton() ;
}
</t>
<t tx="T340">@ &lt;&lt; FindPanel methods &gt;&gt; (9 of 23)
@c

void FindFrame::OnBatchCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	batch_flag = box -&gt; GetValue();
}
</t>
<t tx="T341">@ &lt;&lt; FindPanel methods &gt;&gt; (10 of 23)
@c

void FindFrame::OnIgnoreCaseCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	ignore_case_flag = box -&gt; GetValue();
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; setup (TRUE) ; // reset the search.
}
</t>
<t tx="T342">@ &lt;&lt; FindPanel methods &gt;&gt; (11 of 23)
@c

void FindFrame::OnMarkChangesCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	mark_changes_flag = box -&gt; GetValue();
}
</t>
<t tx="T343">@ &lt;&lt; FindPanel methods &gt;&gt; (12 of 23)
@c

void FindFrame::OnMarkFindsCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	mark_finds_flag = box -&gt; GetValue();
}
</t>
<t tx="T344">@ &lt;&lt; FindPanel methods &gt;&gt; (13 of 23)
@c

void FindFrame::OnPatternMatchCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	pattern_match_flag = box -&gt; GetValue();
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; setup (TRUE) ; // reset the search.
}
</t>
<t tx="T345">@ &lt;&lt; FindPanel methods &gt;&gt; (14 of 23)
@c

void FindFrame::OnReverseCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	reverse_flag = box -&gt; GetValue();
}
</t>
<t tx="T346">@ &lt;&lt; FindPanel methods &gt;&gt; (15 of 23)
@c

void FindFrame::OnSearchBodyTextCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	search_body_flag = box -&gt; GetValue();
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; setup (TRUE) ; // reset the search.
}
</t>
<t tx="T347">@ &lt;&lt; FindPanel methods &gt;&gt; (16 of 23)
@c

void FindFrame::OnSearchHeadlineCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	search_headline_flag = box -&gt; GetValue();
}
</t>
<t tx="T348">@ &lt;&lt; FindPanel methods &gt;&gt; (17 of 23)
@c

void FindFrame::OnSuboutlineOnlyCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	suboutline_only_flag = box -&gt; GetValue();
}
</t>
<t tx="T349">@ &lt;&lt; FindPanel methods &gt;&gt; (18 of 23)
@c

void FindFrame::OnWrapAroundCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	wrap_flag = box -&gt; GetValue();
}
</t>
<t tx="T350">@ &lt;&lt; FindPanel methods &gt;&gt; (19 of 23)
@c

void FindFrame::OnWholeWordCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	whole_word_flag = box -&gt; GetValue();
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; setup (TRUE) ; // reset the search.
}
</t>
<t tx="T351">@ &lt;&lt; FindPanel methods &gt;&gt; (20 of 23)
@c

void FindFrame::OnChangeText (wxCommandEvent&amp; event)
{
	wxTextCtrl * text = (wxTextCtrl *) event.GetEventObject() ;
	change_text = text -&gt; GetValue();
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; setup (TRUE) ; // reset the search.
}
</t>
<t tx="T352">@ &lt;&lt; FindPanel methods &gt;&gt; (21 of 23)
@c

void FindFrame::OnFindText (wxCommandEvent&amp; event)
{
	wxTextCtrl * text = (wxTextCtrl *) event.GetEventObject() ;
	find_text = text -&gt; GetValue();
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; setup (TRUE) ; // reset the search.
}
</t>
<t tx="T353">@ &lt;&lt; FindPanel methods &gt;&gt; (22 of 23)
@c

void FindFrame::set_check_boxes ( void )
{
	assert(mFindPanel);
	mFindPanel -&gt; mBatchCheckBox -&gt; SetValue(batch_flag);
	mFindPanel -&gt; mWrapAroundCheckBox -&gt; SetValue(wrap_flag);
	mFindPanel -&gt; mWholeWordCheckBox -&gt; SetValue(whole_word_flag);
	mFindPanel -&gt; mIgnoreCaseCheckBox -&gt; SetValue(ignore_case_flag);
	mFindPanel -&gt; mPatternMatchCheckBox -&gt; SetValue(pattern_match_flag);
	mFindPanel -&gt; mSearchHeadlineCheckBox -&gt; SetValue(search_headline_flag);
	mFindPanel -&gt; mSearchBodyTextCheckBox -&gt; SetValue(search_body_flag);
	mFindPanel -&gt; mSuboutlineOnlyCheckBox -&gt; SetValue(suboutline_only_flag);
	mFindPanel -&gt; mMarkChangesCheckBox -&gt; SetValue(mark_changes_flag);
	mFindPanel -&gt; mMarkFindsCheckBox -&gt; SetValue(mark_finds_flag);
	mFindPanel -&gt; mReverseCheckBox -&gt; SetValue(reverse_flag);
	mFindPanel -&gt; mFindText -&gt; SetValue(find_text);
	mFindPanel -&gt; mChangeText -&gt; SetValue(change_text);
}
</t>
<t tx="T354">@ &lt;&lt; FindPanel methods &gt;&gt; (23 of 23)
@c

FindPanel::FindPanel(wxFrame *frame)
	   : wxPanel(frame, -1)
{
	// &lt;&lt; Create the find controls &gt;&gt;
	wxBoxSizer * topSizer = new wxBoxSizer(wxVERTICAL);

	topSizer -&gt; Add ( 0, 10 ) ;
	// &lt;&lt; Create the find text box &gt;&gt;
	wxBoxSizer * findSizer = new wxBoxSizer(wxHORIZONTAL);

	findSizer -&gt; Add ( 5, 5 ) ; // Extra space.

	// Label.
	findSizer -&gt; Add (
		new wxStaticText(this, -1, "Find:",
			wxPoint(-1,10), wxSize(50,25), 0, ""),
		0, wxBORDER | wxTOP, 15);  // Vertical offset.

	findSizer -&gt; Add ( 10, 0 ) ; // Width.

	// Text.
	mFindText = new wxTextCtrl(this,
		cFindTextCtrl, "",
		wxDefaultPosition, wxSize(300,60),
		wxTE_PROCESS_TAB | wxTE_MULTILINE,
		wxDefaultValidator, "") ;
	findSizer -&gt; Add ( mFindText );
	findSizer -&gt; Add ( 5, 0 ) ; // Width.

	topSizer -&gt; Add ( findSizer );
	topSizer -&gt; Add ( 0, 10 );
	// -- end -- &lt;&lt; Create the find text box &gt;&gt;
	// &lt;&lt; Create the change text box &gt;&gt;
	wxBoxSizer * changeSizer = new wxBoxSizer(wxHORIZONTAL);

	changeSizer -&gt; Add ( 5, 5 ) ; // Extra space.

	// Label.
	changeSizer -&gt; Add (
		new wxStaticText(this, -1, "Change:",
			wxPoint(-1,10), wxSize(50,25), 0, ""),
		0, wxBORDER | wxTOP, 15);  // Vertical offset.
	changeSizer -&gt; Add ( 10, 0 ) ; // Width.

	// Text.
	mChangeText = new wxTextCtrl(this,
		cChangeTextCtrl, "",
		wxDefaultPosition, wxSize(300,60),
		wxTE_PROCESS_TAB | wxTE_MULTILINE,
		wxDefaultValidator, "") ;
	changeSizer -&gt; Add ( mChangeText ) ;
	changeSizer -&gt; Add ( 5, 0 ) ; // Width.

	topSizer -&gt; Add ( changeSizer );
	topSizer -&gt; Add ( 0, 10 );
	// -- end -- &lt;&lt; Create the change text box &gt;&gt;
	// &lt;&lt; Create all the find check boxes &gt;&gt;
	wxBoxSizer * col1Sizer = new wxBoxSizer(wxVERTICAL);
	// &lt;&lt; Create the first column of check boxes &gt;&gt;
	mBatchCheckBox = new wxCheckBox(this,
		cBatchCheckBox,
		"Batch",
		wxDefaultPosition, wxSize(150,25), 0,
		wxDefaultValidator, "") ;
	col1Sizer -&gt; Add ( mBatchCheckBox,
		0, wxBORDER | wxLEFT, 50);

	mWrapAroundCheckBox = new wxCheckBox(this,
		cWrapAroundCheckBox,
		"Wrap Around",
		wxDefaultPosition, wxSize(150,25), 0,
		wxDefaultValidator, "") ;
	col1Sizer -&gt; Add ( mWrapAroundCheckBox,
		0, wxBORDER | wxLEFT, 50);

	mWholeWordCheckBox = new wxCheckBox(this,
		cWholeWordCheckBox,
		"Whole Word",
		wxDefaultPosition, wxSize(150,25), 0,
		wxDefaultValidator, "") ;
	col1Sizer -&gt; Add ( mWholeWordCheckBox,
		0, wxBORDER | wxLEFT, 50);

	mIgnoreCaseCheckBox = new wxCheckBox(this,
		cIgnoreCaseCheckBox,
		"Ignore Case",
		wxDefaultPosition, wxSize(150,25), 0,
		wxDefaultValidator, "") ;
	col1Sizer -&gt; Add ( mIgnoreCaseCheckBox,
		0, wxBORDER | wxLEFT, 50);

	mPatternMatchCheckBox = new wxCheckBox(this,
		cPatternMatchCheckBox,
		"Pattern Match",
		wxDefaultPosition, wxSize(150,25), 0,
		wxDefaultValidator, "") ;
	col1Sizer -&gt; Add ( mPatternMatchCheckBox,
		0, wxBORDER | wxLEFT, 50);
	// -- end -- &lt;&lt; Create the first column of check boxes &gt;&gt;
	wxBoxSizer * col2Sizer = new wxBoxSizer(wxVERTICAL);
	// &lt;&lt; Create the second column of check boxes &gt;&gt;
	mSearchHeadlineCheckBox = new wxCheckBox(this,
		cSearchHeadlineCheckBox,
		"Search Headline Text",
		wxDefaultPosition, wxSize(150,25),
		0, wxDefaultValidator, "") ;
	col2Sizer -&gt; Add ( mSearchHeadlineCheckBox ) ;

	mSearchBodyTextCheckBox = new wxCheckBox(this,
		cSearchBodyTextCheckBox,
		"Search Body Text",
		wxDefaultPosition, wxSize(150,25), 0,
		wxDefaultValidator, "") ;
	col2Sizer -&gt; Add ( mSearchBodyTextCheckBox );

	mSuboutlineOnlyCheckBox = new wxCheckBox(this,
		cSuboutlineOnlyCheckBox,
		"Suboutline Only",
		wxDefaultPosition, wxSize(150,25), 0,
		wxDefaultValidator, "") ;
	col2Sizer -&gt; Add ( mSuboutlineOnlyCheckBox );

	mMarkChangesCheckBox = new wxCheckBox(this,
		cMarkChangesCheckBox,
		"Mark Changes",
		wxDefaultPosition, wxSize(150,25), 0,
		wxDefaultValidator, "") ;
	col2Sizer -&gt; Add ( mMarkChangesCheckBox );

	mMarkFindsCheckBox = new wxCheckBox(this,
		cMarkFindsCheckBox,
		"Mark Finds",
		wxDefaultPosition, wxSize(150,25), 0,
		wxDefaultValidator, "") ;
	col2Sizer -&gt; Add ( mMarkFindsCheckBox );
	// -- end -- &lt;&lt; Create the second column of check boxes &gt;&gt;

	// Pack the two columns
	wxBoxSizer * checkBoxSizer = new wxBoxSizer(wxHORIZONTAL);

	checkBoxSizer -&gt; Add (col1Sizer);
	checkBoxSizer -&gt; Add (col2Sizer);
	topSizer -&gt; Add(checkBoxSizer);
	topSizer -&gt; Add ( 0, 10 );
	// -- end -- &lt;&lt; Create all the find check boxes &gt;&gt;
	// &lt;&lt; Create all the find buttons &gt;&gt;
	/*
		The row sizers are a bit dim:  they should distribute the buttons automatically.
	*/
	wxBoxSizer * row1Sizer = new wxBoxSizer(wxHORIZONTAL);
	// &lt;&lt; Create the first row of buttons &gt;&gt;
	row1Sizer -&gt; Add (20,0);

	mFindButton = new wxButton(this,
		cFindButton, "Find",
		wxDefaultPosition, wxSize(80,25), 0,
		wxDefaultValidator, "") ;
	row1Sizer -&gt; Add ( mFindButton );
	row1Sizer -&gt; Add (24 + 22 ,0);

	mReverseCheckBox = new wxCheckBox(this,
		cReverseCheckBox, "Reverse",
		wxDefaultPosition, wxSize(100,25), 0,
		wxDefaultValidator, "") ;
	row1Sizer -&gt; Add ( mReverseCheckBox );
	row1Sizer -&gt; Add (24,0);

	mFindAllButton = new wxButton(this,
		cFindAllButton, "Find All",
		wxDefaultPosition, wxSize(80,25), 0,
		wxDefaultValidator, "") ;
	row1Sizer -&gt; Add ( mFindAllButton );
	// -- end -- &lt;&lt; Create the first row of buttons &gt;&gt;
	wxBoxSizer * row2Sizer = new wxBoxSizer(wxHORIZONTAL);
	// &lt;&lt; Create the second row of buttons &gt;&gt;
	row2Sizer -&gt; Add (20,0);

	mChangeButton = new wxButton(this,
		cChangeButton, "Change",
		wxDefaultPosition, wxSize(80,25), 0,
		wxDefaultValidator, "") ;
	row2Sizer -&gt; Add ( mChangeButton );
	row2Sizer -&gt; Add (24,0);

	mChangeThenFindButton = new wxButton(this,
		cChangeThenFindButton, "Change, Then Find",
		wxDefaultPosition, wxSize(122,25), 0,
		wxDefaultValidator, "") ;
	row2Sizer -&gt; Add ( mChangeThenFindButton );
	row2Sizer -&gt; Add (24,0);

	mChangeAllButton = new wxButton(this,
		cChangeAllButton, "Change All",
		wxDefaultPosition, wxSize(80,25), 0,
		wxDefaultValidator, "") ;
	row2Sizer -&gt; Add ( mChangeAllButton );
	// -- end -- &lt;&lt; Create the second row of buttons &gt;&gt;

	// Pack the two rows
	wxBoxSizer * buttonSizer = new wxBoxSizer(wxVERTICAL);

	buttonSizer -&gt; Add (row1Sizer);
	buttonSizer -&gt; Add (0, 10);
	buttonSizer -&gt; Add (row2Sizer);
	topSizer -&gt; Add(buttonSizer);
	topSizer -&gt; Add ( 0, 10 );
	// -- end -- &lt;&lt; Create all the find buttons &gt;&gt;

	SetAutoLayout( TRUE );  // tell dialog to use sizer
	SetSizer( topSizer );  // actually set the sizer
	topSizer -&gt; Fit( this ); // set size to minimum size as calculated by the sizer
	topSizer -&gt; SetSizeHints( this ); // set size hints to honour mininum size
	// -- end -- &lt;&lt; Create the find controls &gt;&gt;
}
</t>
<t tx="T355">@others
</t>
<t tx="T356">BEGIN_EVENT_TABLE( LeoApp, wxApp)

// EVT_EXIT ( LeoApp::OnExit )

END_EVENT_TABLE()</t>
<t tx="T357">bool LeoApp::OnInit()
{
	long argc = wxTheApp -&gt; argc ;
	long filesLoaded = 0 ;

	this -&gt; SetAppName("LeoWx");
	&lt;&lt; Set gAppDirectory &gt;&gt;
	&lt;&lt; Switch to the other running copy of Leo if one is already open &gt;&gt;
	&lt;&lt; Open a file when double-clicking an icon &gt;&gt;
	if ( filesLoaded == 0 ) {
		&lt;&lt; Create a frame and link it into the global frame list &gt;&gt;
	}
	# Create the find panel, but do not show it &gt;&gt;
	gFindFrame = new FindFrame ();
	&lt;&lt; Initialize Sherlock &gt;&gt;
	&lt;&lt; Dump the command line &gt;&gt;
	TRACEP("assert_test", assert(0));
	return TRUE;
}</t>
<t tx="T358">#if 0 //// Not yet: compiles, but lpCmdLine is a dummy !!!!

	LPSTR lpCmdLine = NULL ;  //// Was param to main routine...

	// Try to open the mutex.
	HANDLE hMutex = OpenMutex(MUTEX_ALL_ACCESS, 0, "LeoWxApp");

	// If hMutex is 0 then the mutex doesn't exist. Create it.
	if (!hMutex)
		hMutex = CreateMutex(0, 0, "LeoWxApp");
	else {
		// This is a second instance. Bring the original
		// instance to the top.
		HWND hWnd = FindWindow(0, "LeoWx");
		if (hWnd == 0 ) return 0 ;  ////

		SetForegroundWindow(hWnd);

		// Send the command line in a WM_COPYDATA message.
		if (strlen(lpCmdLine) != 0) {
			COPYDATASTRUCT cds;
			cds.cbData = strlen(lpCmdLine) + 1;
			cds.lpData = lpCmdLine;
			SendMessage(hWnd, WM_COPYDATA, 0, (LPARAM)&amp;cds);
		}
		return 0; ////
	}
#endif //// not yet</t>
<t tx="T359">wxString cwd = ::wxGetCwd();
gAppDirectory = wxFindAppPath( cwd ) ;

// Make sure the directory does not end with a directory separator.
size_t len = gAppDirectory.Length() ;
if ( len &gt; 0 &amp;&amp; gAppDirectory.Last() == wxFILE_SEP_PATH)
	gAppDirectory = gAppDirectory.Truncate(len - 1);</t>
<t tx="T360">gIniting = TRUE ; // Disable error message if file not found.

for ( int i = 1 ; i &lt; argc ; ++ i ) {
	wxString arg = wxTheApp -&gt; argv[i] ;
	LeoFrame *frame = LeoFrame::OpenWithFileName( arg );
	if (frame) ++filesLoaded;
}

gIniting = FALSE ;</t>
<t tx="T361">LeoFrame *frame = new LeoFrame();

++gNumberOfUntitledWindows ;
frame -&gt; SetTitle("untitled");
frame -&gt; Show(TRUE);
SetTopWindow(frame);
gCommands = frame -&gt; mCommands ;
gActiveFrame = frame ; // Allow writes to log pane.

// Set the current node in the _new_ form!.
vnode *v = frame -&gt; mCommands -&gt; rootVnode();
assert(v);
frame -&gt; mCommands -&gt; setCurrentVnode ( v ) ;
frame -&gt; mCommands -&gt; editVnode( v ) ;
frame -&gt; mCommands -&gt; mFirstWindowAndNeverSaved = TRUE ;</t>
<t tx="T362">#ifdef SHERLOCK
	gIniting = TRUE ; // Disable auto open of window during signon.
		SL_INIT () ;
		wxString path("./LeoArgs");
		if ( gAppDirectory.Length() &gt; 0 )
			path = gAppDirectory + "/LeoArgs" ;
		init_args ( &amp;sArgc, &amp;sArgv, (char *) path.c_str() ) ;

		// argv will still be NULL if LeoArgs can not be found.
		if ( sArgv ) {
			SL_PARSE ( sArgc, (char **) sArgv , "++" , "--" ) ;
		}
	gIniting = FALSE ;
#endif</t>
<t tx="T363">TRACEP("dump_argv", 
	ecnl(); es("argc: "); elong(argc); enl();
	for ( int i = 0 ; i &lt;= argc ; ++ i ) {
		wxString arg = wxTheApp -&gt; argv[i] ;
		es("argv["); elong(i); es("]: "); es(arg.c_str()); enl();
	}
);</t>
<t tx="T364">@ &lt;&lt; LeoApp methods &gt;&gt; (2 of 2)
@c

int LeoApp::OnExit()
{
	return TRUE ;
}
</t>
<t tx="T365">@ Initialize the argv vector from a file. This routine is declared in sl.h. init_arg_parse is defined in sl.c.
@c

void init_args ( int *argc, char ***argvp, char *file_name )
{
	// Open the file.  The ctor may throw an exception if it fails, so we test first.
	if ( ! wxFileExists ( file_name ) ) return ;
	wxFile file ( file_name, wxFile::read ) ;
	if ( ! file . IsOpened() ) return ;

	// Allocate the buffer.
	long file_size = file . Length() ;
	char * file_buf = ( char * ) calloc ( 1, file_size + 2 ) ;
	if (file_buf == NULL) return ;

	// Read the open file into file_buf.
	long count = file . Read ( file_buf, file_size ) ;
	if ( count != file_size ) return ;

	// End the buffer with a zero byte.
	file_buf [ file_size ] = '\0';

	// Create and return the arguments in a made-up argv vector.
	init_massage ( file_buf ) ;
	*argc = init_arg_parse ( argvp, file_buf ) ;
}
</t>
<t tx="T366">@ &lt;&lt; LeoApp functions &gt;&gt; (2 of 2)
Returns the absolute path containing this app, or an empty string if the path can not be determined.  cwd should be the current working directory at startup, _not_ the present current working directory.
@c

wxString wxFindAppPath(wxString&amp; cwd)
{
	// 1. Try the environment variable.
	wxString s = wxGetenv("Leo");
	if (!s.IsEmpty()) return s ;

	// 2. Try the path in argv0.
	wxString argv0 = wxTheApp -&gt; argv[0] ;
	if ( argv0.IsEmpty() ) return wxEmptyString ;

	if (wxIsAbsolutePath(argv0))
		return wxPathOnly(argv0);
	else {
		// Resolve the relative path.
		if (cwd.Last() != wxFILE_SEP_PATH)
			cwd += wxFILE_SEP_PATH;
		cwd += argv0;
		if (wxFileExists(cwd)) return wxPathOnly(cwd);
	}

	// 3. Search the PATH  var for the path in argv0.
	wxPathList pathList;
	pathList.AddEnvList(wxT("PATH"));
	s = pathList.FindAbsoluteValidPath(argv0);
	if ( s.IsEmpty() )
			return wxEmptyString ;
	else
			return wxPathOnly(s) ;
}
</t>
<t tx="T367">@ -- end -- &lt;&lt; LeoApp functions &gt;&gt;
@c

#include "LIBes.h"
// &lt;&lt; log bridge functions &gt;&gt; (1 of 2)
void log_open ( const char * filename )
{
	// Carefull: the Log window may not exist during startup or shutdown.
	#if 0 // no longer needed.
	if ( gLogFrame )
		gLogFrame -&gt; open(filename);
	#endif
}
</t>
<t tx="T368">@ &lt;&lt; log bridge functions &gt;&gt; (2 of 2)
@c

void put_cstring_to_log_window ( const char * s )
{
	if ( gActiveFrame )
		gActiveFrame -&gt; putToLog(s);
	//// else this -&gt; bufferLogMessage(s) ;
}
</t>
<t tx="T369">@others</t>
<t tx="T370">BEGIN_EVENT_TABLE(LeoFrame, wxFrame)

@ The following commands are processed by default event handlers in wxTextCtrl:
wxID_CUT, wxID_COPY, wxID_PASTE, wxID_UNDO, wxID_REDO.
The associated UI update events are also processed automatically, when the control has the focus.
@c

// General window events...
#ifdef __WXMSW__ // Activate events exist only on Windows.
	EVT_ACTIVATE( LeoFrame::onActivate )
#else
	EVT_SET_FOCUS ( LeoFrame::OnSetFocus )
#endif

EVT_CLOSE( LeoFrame::onCloseLeoFrame)
EVT_SIZE( LeoFrame::onResize)

// Events in the text control...
EVT_TEXT( cBodyCtrl, LeoFrame::onBodyTextUpdated)
	// Fires whenever text changes.

// Events in the tree control...
EVT_TREE_KEY_DOWN(cTreeCtrl, LeoFrame::onTreeKeyDown)
	// Control keys do not fire this event.

EVT_TREE_SEL_CHANGED(cTreeCtrl, LeoFrame::onTreeChanged) 
EVT_TREE_SEL_CHANGING(cTreeCtrl, LeoFrame::onTreeChanging)

EVT_TREE_BEGIN_DRAG(cTreeCtrl, LeoFrame::onTreeBeginDrag)
EVT_TREE_END_DRAG(cTreeCtrl, LeoFrame::onTreeEndDrag)

EVT_TREE_BEGIN_LABEL_EDIT(cTreeCtrl, LeoFrame::onTreeBeginLabelEdit)
EVT_TREE_END_LABEL_EDIT(cTreeCtrl, LeoFrame::onTreeEndLabelEdit)
&lt;&lt; Declare menu events &gt;&gt;

END_EVENT_TABLE()</t>
<t tx="T371">// Menu enablers...
EVT_UPDATE_UI(cRevertMenuItem, LeoFrame::OnUpdateRevert )

// Command handlers...
EVT_MENU(cNewMenuItem,		LeoFrame::OnNew)
EVT_MENU(cOpenMenuItem,		LeoFrame::OnOpen)
EVT_MENU(cCloseMenuItem,	LeoFrame::OnClose)
EVT_MENU(cSaveMenuItem,		LeoFrame::OnSave)
EVT_MENU(cSaveAsMenuItem,	LeoFrame::OnSaveAs)
EVT_MENU(cSaveToMenuItem,	LeoFrame::OnSaveTo)
EVT_MENU(cRevertMenuItem,	LeoFrame::OnRevert)

EVT_MENU(cPageSetupMenuItem,LeoFrame::OnPageSetup)
EVT_MENU(cPrintMenuItem,  	LeoFrame::OnPrint)

// Read/Write submenu

	EVT_MENU(cReadOutlineOnlyMenuItem,		LeoFrame::OnReadOutlineOnly)
	EVT_MENU(cReadAtFileNodesMenuItem,		LeoFrame::OnReadAtFileNodes)
	EVT_MENU(cWriteOutlineOnlyMenuItem,		LeoFrame::OnWriteOutlineOnly)
	EVT_MENU(cWriteAtFileNodesMenuItem,		LeoFrame::OnWriteAtFileNodes)

// EVT_MENU(cTangleSubmenuItem,	LeoFrame::OnTangleSubmenu)

	EVT_MENU(cTangleAllMenuItem,		LeoFrame::OnTangleAll)
	EVT_MENU(cTangleMarkedMenuItem,		LeoFrame::OnTangleMarked)
	EVT_MENU(cTangleMenuItem,			LeoFrame::OnTangle)

// EVT_MENU(cUntangleSubmenuItem,  LeoFrame::OnUntangleSubmenu)

	EVT_MENU(cUntangleAllMenuItem,		LeoFrame::OnUntangleAll)
	EVT_MENU(cUntangleMarkedMenuItem,	LeoFrame::OnUntangleMarked)
	EVT_MENU(cUntangleMenuItem,			LeoFrame::OnUntangle)

// EVT_MENU(cImportExportSubmenuItem,  LeoFrame::OnImportExportSubmenu)

	EVT_MENU(cImportFilesMenuItem,		LeoFrame::OnImportFiles)
	EVT_MENU(cImportCWEBFilesMenuItem,	LeoFrame::OnImportCWEBFiles)
	EVT_MENU(cImportNowebFilesMenuItem,	LeoFrame::OnImportNowebFiles)
	EVT_MENU(cImportMORETextMenuItem,	LeoFrame::OnImportMoreText)
	EVT_MENU(cFlattenOutlineMenuItem,	LeoFrame::OnFlattenOutline)

EVT_MENU(cQuitMenuItem,  LeoFrame::OnQuit)

// Menu enablers...
EVT_UPDATE_UI(cUndoMenuItem,	LeoFrame::OnUpdateUndo )

#ifndef __WXGTK__ // For now, neither tree nor text controls support Redo.
EVT_UPDATE_UI(cRedoMenuItem,	LeoFrame::OnUpdateRedo )
#endif

EVT_UPDATE_UI(cCutMenuItem,		LeoFrame::OnUpdateCut )
EVT_UPDATE_UI(cCopyMenuItem,	LeoFrame::OnUpdateCopy )
EVT_UPDATE_UI(cPasteMenuItem,	LeoFrame::OnUpdatePaste )
EVT_UPDATE_UI(cDeleteMenuItem,	LeoFrame::OnUpdateDelete )
EVT_UPDATE_UI(cDeleteMenuItem,	LeoFrame::OnUpdateSelectAll )

EVT_UPDATE_UI(cExtractMenuItem,	LeoFrame::OnUpdateExtract )
EVT_UPDATE_UI(cExtractSectionMenuItem,	LeoFrame::OnUpdateExtractSection )
EVT_UPDATE_UI(cExtractNamesMenuItem,	LeoFrame::OnUpdateExtractNames )

EVT_UPDATE_UI(cFindNextMenuItem,		LeoFrame::OnUpdateFind) 
EVT_UPDATE_UI(cFindNextMenuItem2,		LeoFrame::OnUpdateFind)
EVT_UPDATE_UI(cFindPreviousMenuItem,	LeoFrame::OnUpdateFind)
EVT_UPDATE_UI(cReplaceMenuItem,			LeoFrame::OnUpdateReplace) 
EVT_UPDATE_UI(cReplaceThenFindMenuItem,	LeoFrame::OnUpdateReplace) 

// Command handlers...

// Top level
EVT_MENU(cUndoMenuItem,			LeoFrame::OnUndo)
EVT_MENU(cRedoMenuItem,			LeoFrame::OnRedo)
EVT_MENU(cCutMenuItem,			LeoFrame::OnCut)
EVT_MENU(cCopyMenuItem,			LeoFrame::OnCopy)
EVT_MENU(cPasteMenuItem,		LeoFrame::OnPaste)
EVT_MENU(cDeleteMenuItem,		LeoFrame::OnDelete)
EVT_MENU(cSelectAllMenuItem,	LeoFrame::OnSelectAll)
EVT_MENU(cEditHeadlineMenuItem,	LeoFrame::OnEditHeadline)
EVT_MENU(cFontPanelMenuItem,		LeoFrame::OnFontPanel)
EVT_MENU(cSyntaxColoringMenuItem,	LeoFrame::OnSyntaxColoring)
EVT_MENU(cPreferencesMenuItem,		LeoFrame::OnPreferences)

// Edit Body submenu
EVT_MENU(cExtractSectionMenuItem,	LeoFrame::OnExtractSection)
EVT_MENU(cExtractNamesMenuItem,		LeoFrame::OnExtractNames)
EVT_MENU(cExtractMenuItem,			LeoFrame::OnExtract)
EVT_MENU(cConvertBlanksMenuItem,	LeoFrame::OnConvertBlanks)

// Find submenu
EVT_MENU(cFindPanelMenuItem,		LeoFrame::OnFindPanel)
EVT_MENU(cFindNextMenuItem,			LeoFrame::OnFindNext)
EVT_MENU(cFindNextMenuItem2,		LeoFrame::OnFindNext)
EVT_MENU(cFindPreviousMenuItem,		LeoFrame::OnFindPrevious)
EVT_MENU(cReplaceMenuItem,			LeoFrame::OnReplace)
EVT_MENU(cReplaceThenFindMenuItem,	LeoFrame::OnReplaceThenFind)

// Menu enablers...
// Top level
EVT_UPDATE_UI(cCutNodeMenuItem,		LeoFrame::OnUpdateCutNode)
EVT_UPDATE_UI(cDeleteNodeMenuItem,	LeoFrame::OnUpdateDeleteNode)
EVT_UPDATE_UI(cPasteNodeMenuItem,	LeoFrame::OnUpdatePasteNode)
EVT_UPDATE_UI(cSortNodeMenuItem,	LeoFrame::OnUpdateSortNode)

// Expand/Contract submenu
EVT_UPDATE_UI(cExpandAllMenuItem,			LeoFrame::OnUpdateExpandAll)
EVT_UPDATE_UI(cExpandAllChildrenMenuItem,	LeoFrame::OnUpdateExpandAllChildren)
EVT_UPDATE_UI(cExpandChilrenMenuItem,		LeoFrame::OnUpdateExpandChildren)
EVT_UPDATE_UI(cContractAllMenuItem,			LeoFrame::OnUpdateContractAll)
EVT_UPDATE_UI(cContractAllChildrenMenuItem,	LeoFrame::OnUpdateContractAllChildren)
EVT_UPDATE_UI(cContractChilrenMenuItem,		LeoFrame::OnUpdateContractChildren)

// Move/Select submenu
EVT_UPDATE_UI(cMoveDownMenuItem,	LeoFrame::OnUpdateMoveDown)
EVT_UPDATE_UI(cMoveLeftMenuItem,	LeoFrame::OnUpdateMoveLeft)
EVT_UPDATE_UI(cMoveRightMenuItem,	LeoFrame::OnUpdateMoveRight)
EVT_UPDATE_UI(cMoveUpMenuItem,		LeoFrame::OnUpdateMoveUp)
EVT_UPDATE_UI(cPromoteMenuItem,		LeoFrame::OnUpdatePromote)
EVT_UPDATE_UI(cDemoteMenuItem,		LeoFrame::OnUpdateDemote)
EVT_UPDATE_UI(cGoPrevVisibleMenuItem,LeoFrame::OnUpdateGoPrevVisible)
EVT_UPDATE_UI(cGoNextVisibleMenuItem,LeoFrame::OnUpdateGoNextVisible)
EVT_UPDATE_UI(cGoBackMenuItem,		LeoFrame::OnUpdateGoBack)
EVT_UPDATE_UI(cGoNextMenuItem,		LeoFrame::OnUpdateGoNext)

// Mark/Go To submenu
EVT_UPDATE_UI(cMarkMenuItem,			LeoFrame::OnUpdateMark)
EVT_UPDATE_UI(cMarkSubheadsMenuItem,	LeoFrame::OnUpdateMarkSubheads)
EVT_UPDATE_UI(cMarkChangedItemsMenuItem,LeoFrame::OnUpdateMarkChangedItems)
EVT_UPDATE_UI(cMarkChangedRootsMenuItem,LeoFrame::OnUpdateMarkChangedRoots)
EVT_UPDATE_UI(cGoToNextMarkedMenuItem,	LeoFrame::OnUpdateGoToNextMarked)
EVT_UPDATE_UI(cGoToNextChangedMenuItem,	LeoFrame::OnUpdateGoToNextChanged)

// Command handlers...
EVT_MENU(cCutNodeMenuItem,		LeoFrame::OnCutNode)
EVT_MENU(cCopyNodeMenuItem,		LeoFrame::OnCopyNode)
EVT_MENU(cPasteNodeMenuItem,	LeoFrame::OnPasteNode)
EVT_MENU(cDeleteNodeMenuItem,	LeoFrame::OnDeleteNode)

EVT_MENU(cInsertNodeMenuItem,	LeoFrame::OnInsertNode)
EVT_MENU(cCloneNodeMenuItem,	LeoFrame::OnCloneNode)
EVT_MENU(cSortNodeMenuItem,		LeoFrame::OnSortNode)

// Expand/Contract submenu
EVT_MENU(cExpandAllMenuItem,			LeoFrame::OnExpandAll)
EVT_MENU(cExpandAllChildrenMenuItem,	LeoFrame::OnExpandAllChildren)
EVT_MENU(cExpandChilrenMenuItem,		LeoFrame::OnExpandChildren)
EVT_MENU(cContractAllMenuItem,			LeoFrame::OnContractAll)
EVT_MENU(cContractAllChildrenMenuItem,	LeoFrame::OnContractAllChildren)
EVT_MENU(cContractChilrenMenuItem,		LeoFrame::OnContractChildren)

EVT_MENU(cExpandNextLevelMenuItem,	LeoFrame::OnExpandNextLevel)
EVT_MENU(cExpandToLevel1MenuItem,	LeoFrame::OnExpandToLevel1)
EVT_MENU(cExpandToLevel2MenuItem,	LeoFrame::OnExpandToLevel2)
EVT_MENU(cExpandToLevel3MenuItem,	LeoFrame::OnExpandToLevel3)
EVT_MENU(cExpandToLevel4MenuItem,	LeoFrame::OnExpandToLevel4)
EVT_MENU(cExpandToLevel5MenuItem,	LeoFrame::OnExpandToLevel5)
EVT_MENU(cExpandToLevel6MenuItem,	LeoFrame::OnExpandToLevel6)
EVT_MENU(cExpandToLevel7MenuItem,	LeoFrame::OnExpandToLevel7)
EVT_MENU(cExpandToLevel8MenuItem,	LeoFrame::OnExpandToLevel8)
EVT_MENU(cExpandToLevel9MenuItem,	LeoFrame::OnExpandToLevel9)

// Move/Select submenu
EVT_MENU(cMoveDownMenuItem,		LeoFrame::OnMoveDown)
EVT_MENU(cMoveLeftMenuItem,		LeoFrame::OnMoveLeft)
EVT_MENU(cMoveRightMenuItem,	LeoFrame::OnMoveRight)
EVT_MENU(cMoveUpMenuItem,		LeoFrame::OnMoveUp)
EVT_MENU(cPromoteMenuItem,		LeoFrame::OnPromote)
EVT_MENU(cDemoteMenuItem,		LeoFrame::OnDemote)
EVT_MENU(cGoPrevVisibleMenuItem,	LeoFrame::OnGoPrevVisible)
EVT_MENU(cGoNextVisibleMenuItem,	LeoFrame::OnGoNextVisible)
EVT_MENU(cGoBackMenuItem,	LeoFrame::OnGoBack)
EVT_MENU(cGoNextMenuItem,	LeoFrame::OnGoNext)

// Mark/Go To submenu
EVT_MENU(cMarkMenuItem,				LeoFrame::OnMark)
EVT_MENU(cMarkSubheadsMenuItem,		LeoFrame::OnMarkSubheads)
EVT_MENU(cMarkChangedItemsMenuItem,	LeoFrame::OnMarkChangedItems)
EVT_MENU(cMarkChangedRootsMenuItem,	LeoFrame::OnMarkChangedRoots)

EVT_MENU(cMarkAllAtFileNodesDirtyMenuItem,	LeoFrame::OnMarkAllAtFileNodesDirty)
EVT_MENU(cMarkAtFileNodesDirtyMenuItem,	LeoFrame::OnMarkAtFileNodesDirty)

EVT_MENU(cUnmarkAllMenuItem,		LeoFrame::OnUnmarkAll)
EVT_MENU(cGoToNextMarkedMenuItem,	LeoFrame::OnGoToNextMarked)
EVT_MENU(cGoToNextChangedMenuItem,	LeoFrame::OnGoToNextChanged)

// Command handlers...
EVT_MENU(cEqualSizedPanesMenuItem,	LeoFrame::OnEqualSizedPanes)
EVT_MENU(cToggleActivePaneMenuItem,	LeoFrame::OnToggleActivePane)
EVT_MENU(cSplitPaneDirectionMenuItem, LeoFrame::OnChangeDirection)

EVT_MENU(cCascadeMenuItem, 		LeoFrame::OnCascade)
EVT_MENU(cMinimizeAllMenuItem,	LeoFrame::OnMinimizeAll)

#ifdef __WXMSW__
EVT_MENU(cOpenPythonWindowMenuItem,LeoFrame::OnOpenPythonWindow)
#endif

EVT_MENU(cRecentWindowsMenuItem,LeoFrame::OnRecentWindows)

EVT_MENU(cAboutLeoMenuItem, LeoFrame::OnAbout)</t>
<t tx="T372">LeoFrame::LeoFrame()
	: wxFrame((wxFrame *)NULL, -1, "LeoWX", wxDefaultPosition, wxSize(550, 600)),
	mFileName ( "" ),
	mDefaultDirectory ( "" ),
	mOpenDirectory ( "" )
{
	// Link the new frame into the list of frames.
	mIniting = TRUE ; // Lock out resize events.
	long width = 600 ; // initial size
	if ( gLeoFrameList ) gLeoFrameList -&gt; mPrevFrame = this ;
	this -&gt; mNextFrame = gLeoFrameList ;
	this -&gt; mPrevFrame = NULL ;
	gLeoFrameList = this ;
	&lt;&lt; Initialize the private vars &gt;&gt;
	&lt;&lt; Initialize the argument settings &gt;&gt;
	this -&gt; createMenus() ;
	&lt;&lt; Create the splitter windows &gt;&gt;
	&lt;&lt; Create the accelerator table &gt;&gt;
	&lt;&lt; Create the status bar &gt;&gt;
	&lt;&lt; Set the window Icon &gt;&gt;
	&lt;&lt; Set the caret blink rate &gt;&gt;

	mCommands = new Commands(this, mTreeCtrl, mBodyCtrl) ;
	&lt;&lt; Add root node to the tree view &gt;&gt;
	gActiveFrame = this ;
	mIniting = FALSE ; // allow resize events.
	es("Leo Log Window...\n\n");
}</t>
<t tx="T373">mTextChanging = 0 ;
mCopying = 0 ;
mDraggedItem =  0L ;
mReverting = FALSE ;</t>
<t tx="T374">mOutputDocFlag = TRUE ;
mTangleBatchFlag = FALSE ;
mUntangleBatchFlag = FALSE ;
mUseHeaderFlag = TRUE ;
mPageWidth = 132 ;
mTabWidth = 4;
mPresentLanguage = c_language ;
mTargetLanguage = c_language ;</t>
<t tx="T375">mSplitter1 = new wxSplitterWindow(this, cSplitterWindow,
	wxDefaultPosition,  wxDefaultSize,
	wxSP_BORDER | wxSP_3D, 
	"splitterWindow");

mSplitter2 = new wxSplitterWindow( mSplitter1, -1,
	wxDefaultPosition,  wxDefaultSize,
	wxSP_BORDER | wxSP_3D, "splitterWindow");

mSplitter1 -&gt; SetMinimumPaneSize(4);
mSplitter2 -&gt; SetMinimumPaneSize(4);

mTreeCtrl = new wxTreeCtrl (mSplitter2, cTreeCtrl,
	wxDefaultPosition,  wxDefaultSize,
	wxTR_HAS_BUTTONS | wxTR_EDIT_LABELS, wxDefaultValidator, "treeCtrl");

// &lt;&lt; Set the image list &gt;&gt;
/*
	Warning: the width and height must match the underlying .bmp files.
*/
// width: 20, height: 11, mask:TRUE, count:16
#if defined(__WXMSW__) || defined(__WXGTK__)
	wxImageList * im = new wxImageList(20, 11, TRUE, 16);
	wxBitmap box(20,11);

	// Add 16 bitmaps to the image list.
	for ( int i = 0 ; i &lt; 16 ; ++ i ) {

		#if  defined(__WXMSW__)
			wxString s("box");
			s &lt;&lt; i;
			box.LoadFile(s, wxBITMAP_TYPE_BMP_RESOURCE);
		#elif defined(__WXGTK__)
			wxString s("./Icons/box");  // Assume we are launched from ./ directory.
			if ( gAppDirectory.Length() &gt; 0 )
				s = gAppDirectory + "/Icons/box" ;
			if ( i &lt; 10 ) s &lt;&lt; "0" ;
			s &lt;&lt; i;
			s &lt;&lt; ".bmp" ;
			box.LoadFile(s, wxBITMAP_TYPE_BMP);
		#endif
		im -&gt; Add ( box );
	}
	mTreeCtrl -&gt; SetImageList(im);
#endif
// -- end -- &lt;&lt; Set the image list &gt;&gt;

mBodyCtrl = new wxTextCtrl( mSplitter1, cBodyCtrl, "",
	wxDefaultPosition,  wxDefaultSize, wxTE_MULTILINE );

mLogCtrl = new wxTextCtrl( mSplitter2, cLogCtrl, "",
	wxDefaultPosition,  wxDefaultSize, wxTE_MULTILINE );

// &lt;&lt; Set the body font &gt;&gt;
#ifdef __WXMSW__  // This is a fixed-width font and works well.

	// size, family, style, weight.
	wxFont font (9, wxMODERN, wxNORMAL, wxNORMAL) ; 

#else

	// size, family, style, weight.
	// wxFont font (9, wxMODERN, wxNORMAL, wxNORMAL) ; 

	// Try to use lucidatypewriter.
	wxFont font (12, wxFONTFAMILY_DEFAULT, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_NORMAL, FALSE,
		"lucidatypewriter", wxFONTENCODING_ISO8859_1);

	#if 0 // none of these work
		wxFont font(14, 74, 90, 90, FALSE,
		"terminal",
		// "-bitstream-terminal-medium-r-normal-*-*-140-*-*-c-*-iso8859-1",
		// "-Bitstream-Terminal-Medium-R-Normal--18-140-100-100-C-*-ISO8859-1",
		wxFONTENCODING_ISO8859_1);
	#endif
#endif

TRACEP("font_info",
	es("face: "); es( font . GetFaceName() . c_str() ) ; ecs();
	es("family: "); es( font . GetFamilyString() . c_str() ) ; enl();
	es("size: "); eint( font . GetPointSize() ) ; ecs();
	es("style: "); es( font. GetStyleString() . c_str() ) ; ecs();
	es("weight: "); es( font . GetWeightString() . c_str() ) ; enl();
);

mBodyCtrl -&gt; SetFont ( font ) ;
// -- end -- &lt;&lt; Set the body font &gt;&gt;

// Attach the controls to the splitter.
mSplitter1 -&gt; SplitHorizontally(mSplitter2, mBodyCtrl, 0);
mSplitter2 -&gt; SplitVertically(mTreeCtrl, mLogCtrl, width/2);</t>
<t tx="T376">#ifdef __WXGTK__ // Windows version handles shortcuts properly

enum {
	// &lt;&lt; accelerator constants &gt;&gt;
	alt = wxACCEL_ALT,
	normal = wxACCEL_NORMAL,
	ctrl = wxACCEL_CTRL,
	shift = wxACCEL_SHIFT,
	shift_alt = (wxACCEL_ALT | wxACCEL_SHIFT),
	shift_ctrl = (wxACCEL_CTRL | wxACCEL_SHIFT),
	// -- end -- &lt;&lt; accelerator constants &gt;&gt;
	cFirstEntry = -1, // So first real index starts at 0.
	// &lt;&lt; accelerator indices &gt;&gt; (1 of 12)
	cQuit,
	// &lt;&lt; accelerator indices &gt;&gt; (2 of 12)
	cNew,

	// cOpen, cClose, cSave, cSaveAs,
	// &lt;&lt; accelerator indices &gt;&gt; (3 of 12)
	cTangleAll, cTangleMarked, cTangle,
	// &lt;&lt; accelerator indices &gt;&gt; (4 of 12)
	cUntangle,
	// &lt;&lt; accelerator indices &gt;&gt; (5 of 12)
	cImportFiles,
	// &lt;&lt; accelerator indices &gt;&gt; (6 of 12)
	cEditHeadline,
	// &lt;&lt; accelerator indices &gt;&gt; (7 of 12)
	cExtractSection, cExtractNames, cExtract, cConvertBlanks,
	// &lt;&lt; accelerator indices &gt;&gt; (8 of 12)
	cFindPanel, cFindNext, cFindPrev, cReplace, cReplaceThenFind,
	// &lt;&lt; accelerator indices &gt;&gt; (9 of 12)
	// cFontPanel, cSyntaxColoring, cPreferences,
	// &lt;&lt; accelerator indices &gt;&gt; (10 of 12)
	// cInsertNode, cCloneNode,
	// &lt;&lt; accelerator indices &gt;&gt; (11 of 12)
	#ifdef __WXMSW__
		cGoPrevVisibleMenuItem, cGoNextVisibleMenuItem,
	#endif
	// &lt;&lt; accelerator indices &gt;&gt; (12 of 12)
	// Conflicts with Extract command.
	// cEqualSizedPanes,

	cToggleActivePane,
	// -- end -- &lt;&lt; accelerator indices &gt;&gt;
	cAcceleratorEntries // one more than the largest index.
};

assert(cQuit==0);

wxAcceleratorEntry entries [cAcceleratorEntries];

// &lt;&lt; accelerator entries &gt;&gt; (1 of 12)
entries[cQuit].	Set( ctrl, (int)'Q', cQuitMenuItem );
// &lt;&lt; accelerator entries &gt;&gt; (2 of 12)
entries[cNew].   Set( ctrl, (int)'N', cNewMenuItem);

#if 0 // Not needed, and might conflict with Outline menu
entries[cOpen].  Set( ctrl, (int)'O', cOpenMenuItem );
entries[cClose]. Set( ctrl, (int)'W', cCloseMenuItem );
entries[cSave].	 Set( ctrl, (int)'S', cSaveMenuItem );
#endif

#if 0 // Conflicts with Outline menu.
entries[cSaveAs].Set( shift-ctrl, (int)'S', cSaveAsMenuItem );
#endif
// &lt;&lt; accelerator entries &gt;&gt; (3 of 12)
entries[cTangleAll].	Set( shift_ctrl, (int)'A', cTangleAllMenuItem );
entries[cTangleMarked].	Set( shift_ctrl, (int)'M', cTangleMarkedMenuItem );
entries[cTangle].		Set( shift_ctrl, (int)'T', cTangleMenuItem );
// &lt;&lt; accelerator entries &gt;&gt; (4 of 12)
entries[cUntangle].Set( shift_ctrl, (int)'U', cUntangleMenuItem );
// &lt;&lt; accelerator entries &gt;&gt; (5 of 12)
entries[cImportFiles].Set( shift_ctrl, (int)'F', cImportFilesMenuItem );
// &lt;&lt; accelerator entries &gt;&gt; (6 of 12)
entries[cEditHeadline].	Set( shift-ctrl, (int)'H', cEditHeadlineMenuItem );
// &lt;&lt; accelerator entries &gt;&gt; (7 of 12)
entries[cExtractSection].	Set( shift-ctrl, (int)'E', cExtractSectionMenuItem );
entries[cExtractNames].	Set( shift-ctrl, (int)'N', cExtractNamesMenuItem );
entries[cExtract].	Set( shift-ctrl, (int)'D', cExtractMenuItem );
entries[cConvertBlanks].	Set( shift-ctrl, (int)'B', cConvertBlanksMenuItem );
// &lt;&lt; accelerator entries &gt;&gt; (8 of 12)
entries[cFindPanel].Set( ctrl,   (int) 'F', cFindPanelMenuItem );

#if 1 // shift F-keys don't seem to work on Linux
	entries[cFindNext].	Set( normal, (int) WXK_F3, cFindNextMenuItem );
	entries[cFindPrev].	Set( shift,  (int) WXK_F4, cFindPreviousMenuItem );
	entries[cReplace].	Set( normal, (int) WXK_F5, cReplaceMenuItem );
  entries[cReplaceThenFind].Set( normal, (int) WXK_F6, cReplaceThenFindMenuItem );
#else
	entries[cFindNext].	Set( normal, (int) WXK_F3, cFindNextMenuItem );
	entries[cFindPrev].	Set( shift,  (int) WXK_F3, cFindPreviousMenuItem );
	entries[cReplace].	Set( normal, (int) WXK_F4, cReplaceMenuItem );
  entries[cReplaceThenFind].Set( shift,  (int) WXK_F4, cReplaceThenFindMenuItem );
#endif
// &lt;&lt; accelerator entries &gt;&gt; (9 of 12)
#if 0 // works now, and would conflict with other settings.
	entries[cFontPanel].     Set( shift-alt, (int)'T', cFontPanelMenuItem );
	entries[cSyntaxColoring].Set( shift-alt, (int)'S', cSyntaxColoringMenuItem );
	entries[cPreferences].	 Set(      ctrl, (int)'Y', cPreferencesMenuItem );
#endif
// &lt;&lt; accelerator entries &gt;&gt; (10 of 12)
#if 0 // Conflicts with Outline pane.
entries[cInsertNode].Set( ctrl,       (int) 'I', cInsertNodeMenuItem );
entries[cCloneNode] .Set( shift_ctrl, (int) 'I', cCloneNodeMenuItem );
#endif
// &lt;&lt; accelerator entries &gt;&gt; (11 of 12)
#ifdef __WXMSW__
	// Without these wxTreeCtrl handles the up/down keys itself, wrongly.
	entries[cGoPrevVisibleMenuItem].Set( normal, WXK_UP,   cGoPrevVisibleMenuItem );
	entries[cGoNextVisibleMenuItem].Set( normal, WXK_DOWN, cGoNextVisibleMenuItem );
#endif
// &lt;&lt; accelerator entries &gt;&gt; (12 of 12)
// Show log works without accel
// Conflicts with Extract command.
// entries[cEqualSizedPanes].Set( ctrl, (int) 'E', cEqualSizedPanesMenuItem );
entries[cToggleActivePane].Set( ctrl, (int) 'T', cToggleActivePaneMenuItem );
// -- end -- &lt;&lt; accelerator entries &gt;&gt;

wxAcceleratorTable accel(cAcceleratorEntries, entries);

this -&gt; SetAcceleratorTable(accel);
mBodyCtrl -&gt; SetAcceleratorTable(accel);
mTreeCtrl -&gt; SetAcceleratorTable(accel);
mSplitter1 -&gt; SetAcceleratorTable(accel);

#endif</t>
<t tx="T377">CreateStatusBar(2);
SetStatusText("");</t>
<t tx="T378">#ifdef __WXMSW__
  this -&gt;SetIcon(wxIcon("LeoIcon"));
#endif</t>
<t tx="T379">/*
	Blinking happens on Windows without a problem.  Furthermore, setting the rate here affects _all_ windows.
*/
#ifdef __WXGTK__ // Doesn't seem to work.
	wxCaret * caret = mBodyCtrl -&gt; GetCaret();
	caret -&gt; SetBlinkTime (500) ;
#endif</t>
<t tx="T380">wxTreeItemId root = mTreeCtrl -&gt; AddRoot( "untitled" ) ;
tnode *t = new tnode() ;
vnode *v = new vnode( mCommands, t );
v -&gt; setTreeID ( root ) ;
mCommands -&gt; mCurrentVnode = v ;
mTreeCtrl -&gt; SetItemData(root, (wxTreeItemData *) v);

// Set icons: it appears to be necessary to set all here.
// Otherwise, we might take an exception...
v -&gt; setIconVal(0);

#if defined(__WXMSW__)
	// Workaround bug in wxTreectrl.
	mTreeCtrl -&gt; SetItemImage(root, 0, wxTreeItemIcon_Normal);
	mTreeCtrl -&gt; SetItemImage(root, 0, wxTreeItemIcon_Selected);
#elif defined(__WXGTK__)
	mTreeCtrl -&gt; SetItemImage(root, 0, wxTreeItemIcon_Normal);
	mTreeCtrl -&gt; SetItemImage(root, 0, wxTreeItemIcon_Selected);
	mTreeCtrl -&gt; SetItemImage(root, 0, wxTreeItemIcon_Expanded);
	mTreeCtrl -&gt; SetItemImage(root, 0, wxTreeItemIcon_SelectedExpanded);
#endif</t>
<t tx="T381">@ &lt;&lt; LeoFrame methods &gt;&gt; (2 of 157)
@c

void LeoFrame::createMenus ( void )
{
	wxMenuBar *menuBar = new wxMenuBar;
	// &lt;&lt; Create the File menu &gt;&gt;
	wxMenu *fileMenu = new wxMenu;

	// &lt;&lt; Create the initial items of the file menu &gt;&gt;
	fileMenu -&gt; Append ( cNewMenuItem, "&amp;New\tCtrl-N",
		"Open new Leo window" );
	fileMenu -&gt; Append ( cOpenMenuItem,
		"&amp;Open\tCtrl-O", "Open Leo file");

	fileMenu -&gt; AppendSeparator();

	fileMenu -&gt; Append ( cCloseMenuItem,
		"&amp;Close\tCtrl-W", "Close window" );
	fileMenu -&gt; Append ( cSaveMenuItem,
		"&amp;Save\tCtrl-S", "Save window" );
	fileMenu -&gt; Append ( cSaveAsMenuItem,
		"Save &amp;As\tShift-Ctrl-S", "Save window as" );
	fileMenu -&gt; Append ( cSaveToMenuItem,
		"Save &amp;To", "Save window to" );
	fileMenu -&gt; Append ( cRevertMenuItem,
		"&amp;Revert", "Revert window to saved" );

	fileMenu -&gt; AppendSeparator();

	fileMenu -&gt; Append ( cPageSetupMenuItem,
		"Page S&amp;etup\tShift-Ctrl-P", "Specify printer settings" );
	fileMenu -&gt; Append ( cPrintMenuItem,
		"&amp;Print\tCtrl-P", "Print (Weave) window" );

	// Disabled unused items
	fileMenu -&gt; Enable(cPrintMenuItem, FALSE);
	fileMenu -&gt; Enable(cPageSetupMenuItem, FALSE);

	fileMenu -&gt; AppendSeparator();
	// -- end -- &lt;&lt; Create the initial items of the file menu &gt;&gt;
	// &lt;&lt; Create the Read/Write submenu &gt;&gt;
	wxMenu *readWriteMenu = new wxMenu;

	readWriteMenu -&gt; Append (cReadOutlineOnlyMenuItem,
		"Read Outline Only", "Read outline only");
	readWriteMenu -&gt; Append (cReadAtFileNodesMenuItem,
		"Read @file Nodes", "Read @file nodes");
	readWriteMenu -&gt; Append (cWriteOutlineOnlyMenuItem,
		"Write Outline Only", "Write outline only");
	readWriteMenu -&gt; Append (cWriteAtFileNodesMenuItem,
		"Write @file Nodes", "Write @file nodes");

	fileMenu -&gt; Append(cReadWriteSubmenuItem, "Read/Write...", readWriteMenu, "");
	// -- end -- &lt;&lt; Create the Read/Write submenu &gt;&gt;
	// &lt;&lt; Create the Tangle submenu &gt;&gt;
	wxMenu *tangleMenu = new wxMenu;

	tangleMenu -&gt; Append (cTangleAllMenuItem,
		"Tangle &amp;All\tShift-Ctrl-A", "Tangle all roots");
	tangleMenu -&gt; Append (cTangleMarkedMenuItem,
		"Tangle &amp;Marked\tShift-Ctrl-M", "Tangle all marked roots");
	tangleMenu -&gt; Append (cTangleMenuItem,
		"&amp;Tangle\tShift-Ctrl-T", "Tangle selected headline");

	fileMenu -&gt; Append(cTangleSubmenuItem, "&amp;Tangle...", tangleMenu, "");

	// Doesn't work either.
	fileMenu -&gt; SetHelpString(cTangleSubmenuItem, "Tangle commands...");
	// -- end -- &lt;&lt; Create the Tangle submenu &gt;&gt;
	// &lt;&lt; Create the Untangle submenu &gt;&gt;
	wxMenu *untangleMenu = new wxMenu;

	untangleMenu -&gt; Append (cUntangleAllMenuItem,
		"Untangle &amp;All", "Tangle all roots");
	untangleMenu -&gt; Append (cUntangleMarkedMenuItem,
		"Untangle &amp;Marked", "Tangle all marked roots");
	untangleMenu -&gt; Append (cUntangleMenuItem,
		"&amp;Untangle\tShift-Ctrl-U", "Tangle selected headline");

	fileMenu -&gt; Append(cUntangleSubmenuItem, "&amp;Untangle...", untangleMenu, "");
	// -- end -- &lt;&lt; Create the Untangle submenu &gt;&gt;
	// &lt;&lt; Create the Import Files submenu &gt;&gt;
	wxMenu *importMenu = new wxMenu;

	importMenu -&gt; Append (cImportFilesMenuItem,
		"Import Files\tShift-Ctrl-F", "Convert source files to outline" );
	importMenu -&gt; Append (cImportCWEBFilesMenuItem,
		"Import CWEB Files", "Convert CWEB file to outline");
	importMenu -&gt; Append (cImportNowebFilesMenuItem,
		"Import noweb Files", "Convert noweb file to outline");

	importMenu -&gt; Enable(cImportNowebFilesMenuItem, FALSE);

	importMenu -&gt; Append (cImportMORETextMenuItem,
		"Import MORE Text", "Convert MORE file to outline");
	importMenu -&gt; Append (cFlattenOutlineMenuItem,
		"Flatten Outline", "Write Leo outline to text file");

	fileMenu -&gt; Append(cImportExportSubmenuItem,
		"&amp;Import Files...", importMenu, "Import commands");
	// -- end -- &lt;&lt; Create the Import Files submenu &gt;&gt;
	fileMenu -&gt; AppendSeparator();

	fileMenu -&gt; Append(cQuitMenuItem, "E&amp;xit\tCtrl-Q", "Quit Leo");
	// -- end -- &lt;&lt; Create the File menu &gt;&gt;
	// &lt;&lt; Create the Edit menu &gt;&gt;
	wxMenu *editMenu = new wxMenu;

	// &lt;&lt; Create the initial items of the Edit menu &gt;&gt;
	editMenu -&gt; Append ( cUndoMenuItem, "&amp;Undo\tCtrl-Z", "Undo last operation" );

	#ifndef __WXGTK__ // For now, neither tree nor text controls support Redo.
		editMenu -&gt; Append ( cRedoMenuItem,
			"&amp;Redo\tShift-Ctrl-Z", "Redo previous operation" );
	#endif

	editMenu -&gt; AppendSeparator();

	editMenu -&gt; Append ( cCutMenuItem,
		"Cu&amp;t\tCtrl-X", "Cut text" );
	editMenu -&gt; Append ( cCopyMenuItem,
		"&amp;Copy\tCtrl-C", "Copy text" );
	editMenu -&gt; Append ( cPasteMenuItem,
		"&amp;Paste\tCtrl-V", "Paste text" );
	editMenu -&gt; Append ( cDeleteMenuItem,
		"&amp;Delete", "Delete text" );
	editMenu -&gt; Append ( cSelectAllMenuItem,
		"Select A&amp;ll\tCtrl-A", "Select all" );

	editMenu -&gt; AppendSeparator();

	editMenu -&gt; Append ( cEditHeadlineMenuItem,
		"Edit &amp;Headline\tShift-Ctrl-H", "Edit headline text" );
	// -- end -- &lt;&lt; Create the initial items of the Edit menu &gt;&gt;
	// &lt;&lt; Create the Edit Body submenu &gt;&gt;
	wxMenu *editBodyMenu = new wxMenu;

	editBodyMenu -&gt; Append ( cExtractSectionMenuItem,
		"&amp;Extract Section\tShift-Ctrl-E",
		"Extract section to child" );
	editBodyMenu -&gt; Append ( cExtractNamesMenuItem,
		"Extract Section &amp;Names\tShift-Ctrl-N",
		"Extract section names to children" );
	editBodyMenu -&gt; Append ( cExtractMenuItem,
		"Extract\tShift-Ctrl-D",
		"Extract section text to child" );
	editBodyMenu -&gt; Append ( cConvertBlanksMenuItem,
		"&amp;Convert Blanks\tShift-Ctrl-B", "Convert blanks" );

	editMenu -&gt; Append(cEditBodySubmenuItem, "&amp;Edit Body...", editBodyMenu, "");
	// -- end -- &lt;&lt; Create the Edit Body submenu &gt;&gt;
	// &lt;&lt; Create the Find submenu &gt;&gt;
	wxMenu *findMenu = new wxMenu;

	findMenu -&gt; Append ( cFindPanelMenuItem,
		"&amp;Find Panel\tCtrl-F", "Open Find panel" );

	findMenu -&gt; AppendSeparator();

	#ifdef __WXGTK__  // bugs: can't recognize shift-F keys
		findMenu -&gt; Append ( cFindNextMenuItem,
			"Find &amp;Next\tF3", "Find next" );
		findMenu -&gt; Append ( cFindPreviousMenuItem,
			"Find &amp;Prev\tF4", "Find previous" );
		findMenu -&gt; Append ( cReplaceMenuItem,
			"&amp;Replace\tF5", "Replace" );
		findMenu -&gt; Append ( cReplaceThenFindMenuItem,
			"Replace &amp;Then Find\tF6", "Replace, then find again" );
	#else
		findMenu -&gt; Append ( cFindNextMenuItem,
			"Find &amp;Next\tF3", "Find next" );
		findMenu -&gt; Append ( cFindPreviousMenuItem,
			"Find &amp;Prev\tShift-F3", "Find previous" );
		findMenu -&gt; Append ( cReplaceMenuItem,
			"&amp;Replace\tF4", "Replace" );
		findMenu -&gt; Append ( cReplaceThenFindMenuItem,
			"Replace &amp;Then Find\tShift-F4", "Replace, then find again" );
	#endif

	editMenu -&gt; Append( cFindSubmenuItem,
		"&amp;Find...", findMenu, "");
	// -- end -- &lt;&lt; Create the Find submenu &gt;&gt;
	// &lt;&lt; Create the final items of the Edit menu &gt;&gt;
	editMenu -&gt; Append ( cFontPanelMenuItem,
		"&amp;Font Panel\tAlt-Shift-T", "Open Font panel" );

	editMenu -&gt; Append ( cSyntaxColoringMenuItem,
		"&amp;Syntax Coloring...\tAlt-Shift-S", "Set syntax coloring options" );

	editMenu -&gt; Enable(cSyntaxColoringMenuItem, FALSE);

	editMenu -&gt; AppendSeparator();

	editMenu -&gt; Append ( cPreferencesMenuItem,
		"Preferences\tCtrl-Y", "Open Preferences panel" );
	// -- end -- &lt;&lt; Create the final items of the Edit menu &gt;&gt;
	// -- end -- &lt;&lt; Create the Edit menu &gt;&gt;
	// &lt;&lt; Create the Outline menu &gt;&gt;
	wxMenu *outlineMenu = new wxMenu;

	// &lt;&lt; Create the initial items of the Outline menu &gt;&gt;
	outlineMenu -&gt; Append ( cCutNodeMenuItem,
		"Cu&amp;t Node\tShift-Ctrl-X", "Cut node");
	outlineMenu -&gt; Append ( cCopyNodeMenuItem,
		"&amp;Copy Node\tShift-Ctrl-C", "Copy node" );
	outlineMenu -&gt; Append ( cPasteNodeMenuItem,
		"&amp;Paste Node\tShift-Ctrl-V", "Paste node" );
	outlineMenu -&gt; Append ( cDeleteNodeMenuItem,
		// Shift-Ctrl-BkSp not validcPreferencesMenuItem
		"&amp;Delete Node", "Delete node" );

	outlineMenu -&gt; AppendSeparator();

	outlineMenu -&gt; Append ( cInsertNodeMenuItem,
		"&amp;Insert Node\tCtrl-I", "Insert new node" );

	outlineMenu -&gt; Append ( cCloneNodeMenuItem,
		"&amp;Clone Node\tShift-Ctrl-I", "Clone node" );

	outlineMenu -&gt; Append ( cSortNodeMenuItem,
		"&amp;Sort Node", "Sort node's childdren" );

	outlineMenu -&gt; AppendSeparator();
	// -- end -- &lt;&lt; Create the initial items of the Outline menu &gt;&gt;
	// &lt;&lt; Create the Expand/Contract submenu &gt;&gt;
	wxMenu *expandContractMenu = new wxMenu;

	expandContractMenu -&gt; Append ( cExpandAllChildrenMenuItem,
		"Expand All Children", "Expand node fully" );
	expandContractMenu -&gt; Append ( cExpandChilrenMenuItem,
		"Expand Children", "Expand node" );

	expandContractMenu -&gt; AppendSeparator();

	expandContractMenu -&gt; Append ( cContractAllChildrenMenuItem,
		"Contract All Children", "Contract node fully" );
	expandContractMenu -&gt; Append ( cContractChilrenMenuItem,
		"Contract Children", "Contract node" );

	expandContractMenu -&gt; AppendSeparator();

	expandContractMenu -&gt; Append ( cExpandNextLevelMenuItem,
		"Expand &amp;Next Level\tAlt-N", "Expand outline another level" );
	expandContractMenu -&gt; Append ( cExpandToLevel1MenuItem,  // better than contract all
		"Contract All\tAlt-1", "Contract all" );
	expandContractMenu -&gt; Append ( cExpandToLevel2MenuItem,
		"Expand To Level 2\tAlt-2", "Expand to level 2" );
	expandContractMenu -&gt; Append ( cExpandToLevel3MenuItem,
		"Expand To Level 3\tAlt-3", "Expand to level 3" );
	expandContractMenu -&gt; Append ( cExpandToLevel4MenuItem,
		"Expand To Level 4\tAlt-4", "Expand to level 4" );
	expandContractMenu -&gt; Append ( cExpandToLevel5MenuItem,
		"Expand To Level 5\tAlt-5", "Expand to level 5" );
	expandContractMenu -&gt; Append ( cExpandToLevel6MenuItem,
		"Expand To Level 6\tAlt-6", "Expand to level 6" );
	expandContractMenu -&gt; Append ( cExpandToLevel7MenuItem,
		"Expand To Level 7\tAlt-7", "Expand to level 7" );
	expandContractMenu -&gt; Append ( cExpandToLevel8MenuItem,
		"Expand To Level 8\tAlt-8", "Expand to level 8" );
	expandContractMenu -&gt; Append ( cExpandAllMenuItem,
		"Expand All\tAlt-9", "Expand all" );

	outlineMenu -&gt; Append(cExpandContractSubmenuItem,
		"Expand/Contract...", expandContractMenu, "");
	// -- end -- &lt;&lt; Create the Expand/Contract submenu &gt;&gt;
	// &lt;&lt; Create the Move/Select submenu &gt;&gt;
	wxMenu *moveSelectMenu = new wxMenu;

	moveSelectMenu -&gt; Append ( cMoveDownMenuItem,
		"Move &amp;Down\tCtrl-D", "Move node down" );
	moveSelectMenu -&gt; Append ( cMoveLeftMenuItem,
		"Move &amp;Left\tCtrl-L", "Move node left" );
	moveSelectMenu -&gt; Append ( cMoveRightMenuItem,
		"Move &amp;Right\tCtrl-R", "Move node right" );
	moveSelectMenu -&gt; Append ( cMoveUpMenuItem,
		"Move &amp;Up\tCtrl-U", "Move node up" );

	moveSelectMenu -&gt; AppendSeparator();

	// Can't use control-] and control-[ anywhere.
	moveSelectMenu -&gt; Append ( cPromoteMenuItem,
		"&amp;Promote", "Promote children" );

	moveSelectMenu -&gt; Append ( cDemoteMenuItem,
		"&amp;Demote", "Demote following siblings" );

	moveSelectMenu -&gt; AppendSeparator();

	#ifdef __WXMSW__  // Up and down keys handled by tree &amp; text control
		moveSelectMenu -&gt; Append ( cGoPrevVisibleMenuItem,
			"Go Prev Visible\tUp", "Select previous visible node" );
		moveSelectMenu -&gt; Append ( cGoNextVisibleMenuItem,
			"Go Next Visible\tDown", "Select next visible node" );
	#else
	 	moveSelectMenu -&gt; Append ( cGoPrevVisibleMenuItem,
			"Go Prev Visible", "Select previous visible node" );
		moveSelectMenu -&gt; Append ( cGoNextVisibleMenuItem,
			"Go Next Visible", "Select next visible node" );
	#endif

	moveSelectMenu -&gt; AppendSeparator();

	moveSelectMenu -&gt; Append ( cGoBackMenuItem,
		"Go Prev", "Select previous node" );
	moveSelectMenu -&gt; Append ( cGoNextMenuItem,
		"Go Next", "Select next node" );

	outlineMenu -&gt; Append(cMoveSelectSubmenuItem,
		"Move/&amp;Select...", moveSelectMenu, "");
	// -- end -- &lt;&lt; Create the Move/Select submenu &gt;&gt;
	// &lt;&lt; Create the Mark/Go To submenu &gt;&gt;
	wxMenu *markGoToMenu = new wxMenu;

	markGoToMenu -&gt; Append ( cMarkMenuItem,
		"&amp;Mark\tCtrl-M", "Mark node" );
	markGoToMenu -&gt; Append ( cMarkSubheadsMenuItem,
		"Mark &amp;Subheads\tAlt-S", "Mark children of node" );
	markGoToMenu -&gt; Append ( cMarkChangedItemsMenuItem,
		"Mark &amp;Changed Items\tAlt-C", "Mark all changed nodes" );
	markGoToMenu -&gt; Append ( cMarkChangedRootsMenuItem,
		"Mark Changed &amp;Roots\tAlt-R", "Mark all changed root nodes" );
	markGoToMenu -&gt; Append ( cMarkAllAtFileNodesDirtyMenuItem,
		"Mark All @file Nodes Dirty", "Mark all @file nodes" );
	markGoToMenu -&gt; Append ( cMarkAtFileNodesDirtyMenuItem,
		"Mark @file Nodes Dirty", "Mark @file nodes" );

	markGoToMenu -&gt; AppendSeparator();

	markGoToMenu -&gt; Append ( cUnmarkAllMenuItem,
		"&amp;Unmark All\tAlt-U", "Unmark all nodes" );
	markGoToMenu -&gt; Append ( cGoToNextMarkedMenuItem,
		"&amp;Go To Next Marked\tAlt-M", "Select next marked node" );
	markGoToMenu -&gt; Append ( cGoToNextChangedMenuItem,
		"Go To Next Changed\tAlt-D", "Select next changed node" );

	outlineMenu -&gt; Append(cMarkGotoSubmenuItem,
		"&amp;Mark/Go To...", markGoToMenu, "");
	// -- end -- &lt;&lt; Create the Mark/Go To submenu &gt;&gt;
	// -- end -- &lt;&lt; Create the Outline menu &gt;&gt;
	// &lt;&lt; Create the Window menu &gt;&gt;
	wxMenu *windowMenu = new wxMenu;

	windowMenu -&gt; Append ( cEqualSizedPanesMenuItem,
		#ifdef __WXGTK__  // Control-E conflicts with shift-control-E
			"&amp;Equal Sized Panes", "Make each pane the same size");
		#else
			"&amp;Equal Sized Panes\tCtrl-E", "Make each pane the same size");
		#endif

	windowMenu -&gt; Append ( cToggleActivePaneMenuItem,
		"&amp;Toggle Active Pane\tCtrl-T", "Switch the active pane");

	#ifdef __WXGTK__
		windowMenu -&gt; Enable(cToggleActivePaneMenuItem, FALSE);
	#endif

	windowMenu -&gt; Append ( cSplitPaneDirectionMenuItem,
		"&amp;Split Pane Vertically", "Change orientation of pane");

	windowMenu -&gt; AppendSeparator();

	windowMenu -&gt; Append ( cCascadeMenuItem,
		"&amp;Cascade Windows", "Cascade all open windows");

	windowMenu -&gt; Append ( cMinimizeAllMenuItem,
		"Minimize &amp;All Windows", "Minimize all open windows");

	windowMenu -&gt; AppendSeparator();

	#ifdef __WXMSW__
	windowMenu -&gt; Append ( cOpenPythonWindowMenuItem,
		"Open &amp;Python Window\tAlt-P", "Open the Python window");
	#endif

	#if 0 // Not ready yet: use wxFileHistory
		windowMenu -&gt; AppendSeparator();

		windowMenu -&gt; Append ( cRecentWindowsMenuItem,
			"Recent Windows", "List of recent windows");
	#endif
	// -- end -- &lt;&lt; Create the Window menu &gt;&gt;
	// &lt;&lt; Create the Help menu &gt;&gt;
	wxMenu *helpMenu = new wxMenu;

	helpMenu -&gt; Append(cAboutLeoMenuItem,
		"&amp;About Leo...",
		"Show about dialog");
	// -- end -- &lt;&lt; Create the Help menu &gt;&gt;
	menuBar-&gt;Append(fileMenu, "&amp;File");
	menuBar-&gt;Append(editMenu, "&amp;Edit");
	menuBar-&gt;Append(outlineMenu, "&amp;Outline");
	menuBar-&gt;Append(windowMenu, "&amp;Window");
	menuBar-&gt;Append(helpMenu, "&amp;Help");
	SetMenuBar(menuBar);  // attach the menu bar to the frame
}
</t>
<t tx="T382">@ &lt;&lt; LeoFrame methods &gt;&gt; (3 of 157)
@c

void LeoFrame::SetUntitledNumber ( long n )
{
	wxString s ( "untitled") ;
	if ( n &gt; 0 )
		s += wxString::Format("%d",n);
	this -&gt; SetTitle(s) ;
}
</t>
<t tx="T383">@ &lt;&lt; LeoFrame methods &gt;&gt; (4 of 157)
@c

void LeoFrame::putToLog ( const char * s )
{
	mLogCtrl -&gt; AppendText(s);
}
</t>
<t tx="T384">@ &lt;&lt; LeoFrame methods &gt;&gt; (5 of 157)
@c

wxString LeoFrame::getLogText ( void )
{
	return mLogCtrl -&gt; GetValue();
}
</t>
<t tx="T385"></t>
<t tx="T386">@ &lt;&lt; LeoFrame methods &gt;&gt; (6 of 157)
@c

#ifdef __WXMSW__

void LeoFrame::onActivate(wxActivateEvent &amp;event)
{
	if ( event . GetActive() ) {
		gActiveFrame = this ;
		if ( this -&gt; mCommands )
			this -&gt; mCommands -&gt; checkAllFileDates();
	}
}
</t>
<t tx="T387">
#else

void LeoFrame::OnSetFocus(wxFocusEvent&amp; WXUNUSED(event))
{
	gActiveFrame = this ;
	if ( this -&gt; mCommands )
		this -&gt; mCommands -&gt; checkAllFileDates();
}
</t>
<t tx="T388">
#endif
// &lt;&lt; LeoFrame methods &gt;&gt; (7 of 157)
void LeoFrame::onResize(wxSizeEvent&amp; WXUNUSED(event))
{
	if ( mIniting )
		return ; // Can be called during initialization.

	// Resize splitter1 with equal sized panes.
	wxSize size = this -&gt; GetClientSize();
	mSplitter1 -&gt; SetClientSize(size);
	long w = size.GetWidth();
	long h = size.GetHeight();
	if ( mSplitter1 -&gt; GetSplitMode() == wxSPLIT_VERTICAL )
		mSplitter1 -&gt; SetSashPosition(w/2, TRUE);
	else
		mSplitter1 -&gt; SetSashPosition(h/2, TRUE);

	// Resize splitter2 with equal sized panes.
	size = mSplitter2 -&gt; GetClientSize();
	w = size.GetWidth();
	h = size.GetHeight();
	if ( mSplitter2 -&gt; GetSplitMode() == wxSPLIT_VERTICAL )
		mSplitter2 -&gt; SetSashPosition((3*w)/5, TRUE);
	else
		mSplitter2 -&gt; SetSashPosition((3*h)/5, TRUE);
}
</t>
<t tx="T389">@ &lt;&lt; LeoFrame methods &gt;&gt; (8 of 157)
@c

static long sDisableTextUpdates = 0 ;

void LeoFrame::onBodyTextUpdated(wxCommandEvent&amp; WXUNUSED(event))
{
	// Changing text should never cause a recursive entry.
	assert(mTextChanging == 0);
	assert(mCopying == 0);

	if ( sDisableTextUpdates &gt; 0 ) return ; // 3/19/01
	if ( mCommands == NULL ) return ;
	vnode * v = mCommands -&gt; currentVnode();
	if ( v == NULL ) return ;

	TRACEP("events", es("OnBodyTextUpdated"); enl());
	++ mTextChanging ;

	// &lt;&lt; Set the dirty bit and/or the file-changed mark if the text has changed &gt;&gt;
	if (
		! v -&gt; isDirty() &amp;&amp;
		mBodyCtrl -&gt; GetValue() != v -&gt; bodyString()
	) {
		v -&gt; initDirtyBit () ;  // Avoid calling setIcon.
		if ( ! mCommands -&gt; isChanged() )
			mCommands -&gt; setChanged (TRUE) ;
	}
	// -- end -- &lt;&lt; Set the dirty bit and/or the file-changed mark if the text has changed &gt;&gt;

	// Update the tnode so nodes are always synched.
	v -&gt; t() -&gt; saveBodyPaneToTnode ( mBodyCtrl ) ;
	v -&gt; setAncestorAtFileNodeDirty();

	// Update the syntax colorer if needed.
	mCommands -&gt; updateSyntaxColorer ( v );

	// &lt;&lt; Update icons &gt;&gt;
	/*
		It is very important to eliminate flicker here.
	*/
	long val = v -&gt; computeIcon();
	bool repaint = FALSE ;

	if ( ! mCommands -&gt; isChanged() ) {
		mCommands -&gt; setChanged (TRUE);
		repaint = TRUE ;
	}

	if ( val &gt;= 0 &amp;&amp; val != v -&gt; iconVal() ) {
		repaint = TRUE ;

		v -&gt; setIconWithVal(val);

		// Update all joined nodes.
		for (
			vnode * v2 = v -&gt; joinList();
			v2 &amp;&amp; v2 != v ;
			v2 = v2 -&gt; joinList()
		)
			v2 -&gt; setIconWithVal(val);
	}

	if (repaint)
		mTreeCtrl -&gt; Refresh();
	// -- end -- &lt;&lt; Update icons &gt;&gt;
	-- mTextChanging ;
}
</t>
<t tx="T390">@ &lt;&lt; LeoFrame methods &gt;&gt; (9 of 157)
@c

void LeoFrame::onCloseLeoFrame(wxCloseEvent&amp; event)
{
	// Veto the close if the Frame has been changed and the user cancels.

	if ( mCommands -&gt; isChanged() ) {
		bool veto = FALSE ;
		if ( ! mReverting ) {
			// &lt;&lt; Prompt for change.  Set veto if the user cancels &gt;&gt;
			// Use the window title:  mFileName may not exist.
			wxString title = this -&gt; GetTitle();
			if ( title.Length() &gt; 0 &amp;&amp; title[0UL] == '*')
				title = title.Mid(1);

			wxString message("Save changes to \"");
			message += title ;

			if ( gQuitting )
				message += "\" before quitting?" ;
			else
				message += "\" before closing?"  ;

			wxMessageDialog * dialog = new wxMessageDialog(
				this, message, "LeoWX", wxYES_NO|wxCANCEL);
			int answer = dialog-&gt;ShowModal();
			dialog-&gt;Destroy();

			switch (answer)
			{
			case wxID_YES:
				// The user want's to save the file before closing.
				if ( mFileName == wxString("") ) {
					// Put up the save dialog.
					wxFileDialog d (
						NULL, "Save",
						"", // default directory
						title + ".leo", // default file
						"*.leo", // wildcard
						wxSAVE | wxOVERWRITE_PROMPT,  // style of dialog.
						wxDefaultPosition);

					if ( d.ShowModal() == wxID_OK ) {
						wxArrayString paths;
						d.GetPaths(paths);
						if ( paths.Count() == 1 ) {
							wxString path = paths.Item(0);
							mFileName = path ;
							this -&gt; SetTitle(path);
							mCommands -&gt; save (path);
						}
						else veto = TRUE ;
					}
					else veto = TRUE ;
				}
				else mCommands -&gt; save( mFileName ) ;
				break;

			case wxID_NO:
				// The user does not want to save the frame.
				break;

				// The user want's to cancel the close.
			case wxID_CANCEL:
			default:
				veto = TRUE ;
				break;
			}
			// -- end -- &lt;&lt; Prompt for change.  Set veto if the user cancels &gt;&gt;
		}
		if ( veto &amp;&amp; event.CanVeto() ) {
				event.Veto();  // veto the close.
				return ;
			}
	}

	// Unlink this frame from the list of frames.
	if ( mNextFrame )
		mNextFrame -&gt; mPrevFrame = mPrevFrame ;
	if ( mPrevFrame )
		mPrevFrame -&gt; mNextFrame = mNextFrame ;
	else
		gLeoFrameList = mNextFrame ;

	if ( gLeoFrameList == NULL ) {
		// &lt;&lt; Close the permanent frames &gt;&gt;
		if ( gPrefsFrame ) {
			gPrefsFrame -&gt; Destroy();
			gPrefsFrame = NULL ;
		}

		if ( gFindFrame ) {
			gFindFrame -&gt; Destroy();
			gFindFrame = NULL ;
		}

		#ifdef __WXMSW__
		wxPythonFrame::destroy();
		#endif
		// -- end -- &lt;&lt; Close the permanent frames &gt;&gt;
	}

	// Clear the active form.  It will be set on the next activate event.
	gActiveFrame = NULL ;
	gCommands = NULL ;

	// Set all vnodes to NULL so they are not destroyed.
	#if 0 ///// why shouldn't they be destroyed ?????
	  wxTreeCtrl * tree = mTreeCtrl;
	  vnode * v = mCommands -&gt; rootVnode();
	  while ( v ) {
		  vnode * next = v -&gt; threadNext();
		  wxTreeItemId id = v -&gt; treeID();
		  assert(id);
		  tree -&gt; SetItemData(id, NULL);
		  v = next ;
	  }
	#endif

	this -&gt; Destroy();
}
</t>
<t tx="T391">@ &lt;&lt; LeoFrame methods &gt;&gt; (10 of 157)
@c

void LeoFrame::onTreeChanged(wxTreeEvent&amp; event)
{
 	TRACEP("events", es("onTreeChanged"); enl());
	assert(mTreeCtrl);
	assert(mCommands);
	if (mCommands -&gt; mInhibitOnTreeChanged) return ;
	// &lt;&lt; Define old_id, new_id, old_v, new_v &gt;&gt;
	/*
		I used to think that new_id and old_id had to exist, but that is not so: either might be 0 depending on circumstances.
	*/
	wxTreeItemId new_id = event.GetItem();
	TRACEP("events", es("new item: "); elong( long(new_id) ) ; enl() ) ;

	if ( ! new_id.IsOk() ) return ;
	vnode * new_v = (vnode *)( mTreeCtrl -&gt; GetItemData(new_id) ) ;
	if ( new_v == NULL ) return ;

	#if 0 // no longer used

		// old_id may not exist if we are activating the first node.
		wxTreeItemId old_id = event.GetOldItem();
		TRACEP("events", es("old item: "); elong( long(old_id) ) ; enl() ) ;
		vnode * old_v = NULL ;

		if ( old_id.IsOk() ) {
			old_v = (vnode *) ( mTreeCtrl -&gt; GetItemData(old_id) ) ;
			#ifdef __WXMSW__
				assert(old_v);
			#endif
		}

	#endif
	// -- end -- &lt;&lt; Define old_id, new_id, old_v, new_v &gt;&gt;
	// &lt;&lt; Put the new text into the body pane &gt;&gt;
	/*
		Apparently in wxWindows this does _not_ fire the text changed event! But in wxGTK it does.  We must prevent the update 
		event handler from messing with the old text!
	*/
	++ sDisableTextUpdates ;
		// Clear the old text.
		mBodyCtrl -&gt; Clear();

		// Put the text of the new node into the body pane.
		new_v -&gt; t() -&gt; loadBodyPaneFromTnode ( mBodyCtrl ) ;

		// Clear the undo stack.
		mBodyCtrl -&gt; DiscardEdits();
	-- sDisableTextUpdates ;

	// Update the Commander's idea of the current node.
	mCommands -&gt; mCurrentVnode = new_v ;

	// Update the syntax colorer if needed.
	mCommands -&gt; updateSyntaxColorer ( new_v ) ;
	// -- end -- &lt;&lt; Put the new text into the body pane &gt;&gt;
}
</t>
<t tx="T392">@ &lt;&lt; LeoFrame methods &gt;&gt; (11 of 157)
@c

void LeoFrame::onTreeChanging(wxTreeEvent&amp; WXUNUSED(event))
{
	// No recursion should be possible here.
	assert(mTextChanging == 0);
	assert(mCopying == 0);
}
</t>
<t tx="T393">@ &lt;&lt; LeoFrame methods &gt;&gt; (12 of 157)
@c

void LeoFrame::onTreeKeyDown(wxTreeEvent&amp; WXUNUSED(event))
{

}
</t>
<t tx="T394">@ &lt;&lt; LeoFrame methods &gt;&gt; (13 of 157)
@c

void LeoFrame::onTreeBeginDrag(wxTreeEvent&amp; event)
{
	assert(mTreeCtrl);
	if ( event.GetItem() != mTreeCtrl -&gt; GetRootItem() ) {
		mDraggedItem = event.GetItem();
		event.Allow();
	}
}
</t>
<t tx="T395">@ &lt;&lt; LeoFrame methods &gt;&gt; (14 of 157)
@c

void LeoFrame::onTreeEndDrag(wxTreeEvent&amp; event)
{
	// &lt;&lt; Define onTreeEndDrag vars &gt;&gt;
	assert(mTreeCtrl);
	assert(mCommands);

	wxTreeItemId dst = event.GetItem();
	wxTreeItemId src = mDraggedItem;
	mDraggedItem = 0L;
	if ( ! dst.IsOk() || ! src.IsOk() ) return ;

	vnode * src_v = (vnode *) ( mTreeCtrl -&gt; GetItemData(src) );
	if (src_v == NULL) return ;

	vnode * dst_v = (vnode *) ( mTreeCtrl -&gt; GetItemData(dst) );
	if (dst_v == NULL) return ;

	wxTreeItemId parent = mTreeCtrl -&gt; GetParent(dst);
	vnode * parent_v = NULL ;
	// -- end -- &lt;&lt; Define onTreeEndDrag vars &gt;&gt;
	if ( src == 0 || dst == 0 ) return ;
	long cookie;
	if (
		// dst is the root
		!parent.IsOk() ||
		// dst has visible children and dst isn't the first child.
		mTreeCtrl -&gt; ItemHasChildren(dst) &amp;&amp; mTreeCtrl -&gt; IsExpanded(dst) &amp;&amp;
		mTreeCtrl -&gt; GetFirstChild(dst, cookie) != src ||
		// back(src) == dst (would otherwise be a do-nothing)
		mTreeCtrl -&gt; GetPrevSibling(src) == dst
	) {
		// &lt;&lt; Insert src as the first child of dst &gt;&gt;
		// Make sure the drag will be valid.
		parent_v = (vnode *) ( mTreeCtrl -&gt; GetItemData(dst) );
		if ( ! mCommands -&gt; checkMoveWithParentWithWarning ( src_v, parent_v, TRUE ) ) return ;

		src_v -&gt; moveToNthChildOf( dst_v, 0);
		// -- end -- &lt;&lt; Insert src as the first child of dst &gt;&gt;
	}
	else {
		// Not the root and no visible children.
		// &lt;&lt; Insert src after dst &gt;&gt;
		// Do nothing if dst is a child of src.
		for (wxTreeItemId p = parent; p.IsOk(); p = mTreeCtrl -&gt; GetParent(p) )
			if ( p == src )
				return ;

		// Do nothing if dst is joined to src.
		if ( dst_v -&gt; isJoinedTo(src_v) )
			return ;

		// Make sure the drag will be valid.
		parent_v = (vnode *) ( mTreeCtrl -&gt; GetItemData(parent) );
		if ( ! mCommands -&gt; checkMoveWithParentWithWarning ( src_v, parent_v, TRUE ) ) return ;

		src_v -&gt; moveAfter(dst_v);
		// -- end -- &lt;&lt; Insert src after dst &gt;&gt;
	}

	mCommands -&gt; selectVnode(src_v);
	mCommands -&gt; setChanged(TRUE);
}
</t>
<t tx="T396">@ &lt;&lt; LeoFrame methods &gt;&gt; (15 of 157)
Editing will not be allowed if this routine does not exist.
@c

void LeoFrame::onTreeBeginLabelEdit(wxTreeEvent&amp; WXUNUSED(event))
{
	// Doing nothing is is enough to enable the edit.
}
</t>
<t tx="T397">@ &lt;&lt; LeoFrame methods &gt;&gt; (16 of 157)
Editing will not be allowed if this routine does not exist.
@c

void LeoFrame::onTreeEndLabelEdit(wxTreeEvent&amp; event)
{
	// Doing nothing is enough to enable the edit.

	wxString s = event.GetLabel();
	wxTreeItemId item = event.GetItem();
	vnode * v = (vnode *) ( mTreeCtrl -&gt; GetItemData(item) );

	// Set the dirty bit and the file-changed mark if the headline has changed.
	if ( ! v -&gt; isDirty() &amp;&amp; s != v -&gt; headString() ) {
		v -&gt; setDirty () ;
		if ( ! mCommands -&gt; isChanged() )
			mCommands -&gt; setChanged (TRUE) ;
	}

	// Update all joined headlines.
	for ( vnode * j = v -&gt; joinList(); j &amp;&amp; j != v; j = j -&gt; joinList() )
		j -&gt; setHeadString(s);
}
</t>
<t tx="T398">@ &lt;&lt; LeoFrame methods &gt;&gt; (17 of 157)
This updates the text of joined _headlines_, not body text.
@c

#if 0 // no longer used

void LeoFrame::updateJoinedHeadlines ( wxString text, vnode * v )
{
	static long guard = 0 ;
	if ( guard &gt; 0 ) return ;
	++ guard ;
		for (
			vnode * v2 = v -&gt; joinList() ;
			v2 &amp;&amp; v2 != v ;
			v2 = v2 -&gt; joinList()
		)  {
			wxTreeItemId id = v2 -&gt; treeID();
			assert(id);
			mTreeCtrl -&gt; SetItemText(id, text) ;
		}
	-- guard ;
}
</t>
<t tx="T399">
#endif
// &lt;&lt; LeoFrame methods &gt;&gt; (18 of 157)
void LeoFrame::OnUpdateRevert( wxUpdateUIEvent &amp;event )
{
	event.Enable(mCommands -&gt; canRevert()) ;
}
</t>
<t tx="T400">@ &lt;&lt; LeoFrame methods &gt;&gt; (19 of 157)
@c

void LeoFrame::OnNew(wxCommandEvent&amp; WXUNUSED(event))
{
	// Create a frame and link it into the global frame list.
	LeoFrame *frame = new LeoFrame();
	wxString s("untitled");
	if ( ++gNumberOfUntitledWindows &gt; 1 )
		s += wxString::Format("%d", gNumberOfUntitledWindows);
	frame -&gt; SetTitle(s);
	frame -&gt; mFileName = wxString("") ;  // No real file associated with this window.
	frame -&gt; Show(TRUE);

	// Set the current node in the _new_ form!.
	vnode *v = frame -&gt; mCommands -&gt; rootVnode();
	assert(v);
	frame -&gt; mCommands -&gt; setCurrentVnode ( v ) ;
	frame -&gt; mCommands -&gt; editVnode( v ) ;
}
</t>
<t tx="T401">@ &lt;&lt; LeoFrame methods &gt;&gt; (20 of 157)
@c

void LeoFrame::OnOpen(wxCommandEvent&amp; WXUNUSED(event))
{
	// Create the Open dialog.
	wxFileDialog d (
		NULL, "Choose a Leo file",
		"", // default directory
		"", // default file
		"*.leo", // wildcard
		wxOPEN | wxMULTIPLE ,  // style of dialog.
		wxDefaultPosition);

	if ( d.ShowModal() == wxID_OK ) {
		wxArrayString paths;
		d.GetPaths(paths);
		long count = paths.Count();
		for ( long i = 0 ; i &lt; count ; ++ i )
			LeoFrame::OpenWithFileName ( paths.Item(i) ) ;
	}
}
</t>
<t tx="T402">@ &lt;&lt; LeoFrame methods &gt;&gt; (21 of 157)
@c

LeoFrame * LeoFrame::OpenWithFileName( wxString fileName )
{
	// If the file is already open just bring its window to the front.
	LeoFrame * frame = gLeoFrameList ;
	while ( frame ) {
		if ( frame -&gt; mFileName == fileName ) {
			frame -&gt; Show();
			gActiveFrame = frame ;
			return frame ;
		}
		frame = frame -&gt; mNextFrame ;
	}

	// Don't take an exception if the file doesn't exist.
	if ( ! ::wxFileExists ( fileName ) ) {
		wxString m("Can not open: ") ;
		m += fileName ;
		alert ( m.c_str() ) ;
		return NULL ;
	}

	try {
		// &lt;&lt; Set closeEmptyFrameFlag if the only open window is empty &gt;&gt;
		#if 0 // not used at present.
		LeoFrame * closeFrame = gLeoFrameList ;

		bool closeEmptyFrameFlag =
			// There is only one window open at present.
			gNumberOfUntitledWindows == 1 &amp;&amp;

			// The window was opened on startup and has never been saved.
			closeFrame &amp;&amp;
			closeFrame -&gt; mCommands -&gt; mFirstWindowAndNeverSaved &amp;&amp;

			// The window is empty.
			! ( closeFrame -&gt; mCommands-&gt; isChanged() ) ;
		#endif
		// -- end -- &lt;&lt; Set closeEmptyFrameFlag if the only open window is empty &gt;&gt;
		LeoFrame * frame = new LeoFrame ();
		#if 0 // Don't show frame until it has been fully opened.
			frame -&gt; Show(TRUE);
		#endif
		frame -&gt; mCommands -&gt; open( fileName ) ;
		frame -&gt; mFileName = fileName ;
		// Automatically close an empty frame that was created on entry.
		#if 0 //// There is still something wrong here!
		if ( closeEmptyFrameFlag &amp;&amp; closeFrame )
			closeFrame -&gt; Close ( ) ;
		#endif
		gActiveFrame = frame ;
		return frame ;
	}
	catch ( ... )
	{
		wxString m("Error opening: ") ;
		m += fileName ;
		alert ( m.c_str() ) ;
		return NULL ;
	}
}
</t>
<t tx="T403">@ &lt;&lt; LeoFrame methods &gt;&gt; (22 of 157)
@c

void LeoFrame::OnClose(wxCommandEvent&amp; WXUNUSED(event))
{
	// Close the frame, giving the close handler a chance to veto.
	this -&gt; Close();
}
</t>
<t tx="T404">@ &lt;&lt; LeoFrame methods &gt;&gt; (23 of 157)
@c

void LeoFrame::OnSave(wxCommandEvent&amp; WXUNUSED(event))
{
	if ( mFileName == wxString("") ) {
		// Create the Save dialog.
		wxFileDialog d (
			NULL, "Save",
			wxString(""), // default directory
			mFileName, // default file
			wxString("*.leo"), // wildcard
			wxSAVE | wxOVERWRITE_PROMPT,  // style of dialog.
			wxDefaultPosition);

		if ( d.ShowModal() == wxID_OK ) {
			wxString path = d.GetPath();
			mFileName = path ;
			this -&gt; SetLabel(path);
			mCommands -&gt; save (path);
		}
	}
	else mCommands -&gt; save ( mFileName ) ;
}
</t>
<t tx="T405">@ &lt;&lt; LeoFrame methods &gt;&gt; (24 of 157)
@c

void LeoFrame::OnSaveAs(wxCommandEvent&amp; WXUNUSED(event))
{
	// Create the Save dialog.
	wxFileDialog d (
		NULL, "Save As",
		wxString(""), // default directory
		mFileName, // default file
		wxString("*.leo"), // wildcard
		wxSAVE | wxOVERWRITE_PROMPT,  // style of dialog.
		wxDefaultPosition);

	if ( d.ShowModal() == wxID_OK ) {
		wxString path = d.GetPath();
		mFileName = path ;
		this -&gt; SetLabel(path);
		mCommands -&gt; saveAs (path);
	}
}
</t>
<t tx="T406">@ &lt;&lt; LeoFrame methods &gt;&gt; (25 of 157)
@c

void LeoFrame::OnSaveTo(wxCommandEvent&amp; WXUNUSED(event))
{
	// Create the Save dialog.
	wxFileDialog d (
		NULL, "Save To",
		wxString(""), // default directory
		mFileName, // default file
		wxString("*.leo"), // wildcard
		wxSAVE | wxOVERWRITE_PROMPT,  // style of dialog.
		wxDefaultPosition);

	if ( d.ShowModal() == wxID_OK ) {
		wxString fileName = d.GetPath();
		mCommands -&gt; saveACopyAs(fileName);
	}
}
</t>
<t tx="T407">@ &lt;&lt; LeoFrame methods &gt;&gt; (26 of 157)
@c

void LeoFrame::OnRevert(wxCommandEvent&amp; WXUNUSED(event))
{
   // Make sure the user wants to Revert.
	wxString prompt ("Revert to previous version of ");
	prompt += mFileName + "?" ;
	int answer = wxMessageBox( prompt, "Revert to saved?", wxYES_NO ) ;
	if (answer == wxNO) return ;

	// Kludge: rename this frame so OpenWithFileName won't think it is open.
	wxString fileName = mFileName ;
	mFileName = wxString("") ;

	// Create a new frame before deleting this frame.
	LeoFrame * frame = LeoFrame::OpenWithFileName( fileName );

	// Delete the form.
	mReverting = TRUE ; // Indicate that no prompt is needed.
	this -&gt; Close();
	mReverting = FALSE ;

	// Bring the already-opened frame to the front.
	frame -&gt; Show(FALSE);
	frame -&gt; Show(TRUE);
}
</t>
<t tx="T408">@ &lt;&lt; LeoFrame methods &gt;&gt; (27 of 157)
@c

void LeoFrame::OnPageSetup(wxCommandEvent&amp; WXUNUSED(event))
{
	////
}
</t>
<t tx="T409">@ &lt;&lt; LeoFrame methods &gt;&gt; (28 of 157)
@c

void LeoFrame::OnPrint(wxCommandEvent&amp; WXUNUSED(event))
{
	////
}
</t>
<t tx="T410">@ &lt;&lt; LeoFrame methods &gt;&gt; (29 of 157)
@c

void LeoFrame::OnTangleSubmenu(wxCommandEvent&amp; WXUNUSED(event))
{

}
</t>
<t tx="T411">@ &lt;&lt; LeoFrame methods &gt;&gt; (30 of 157)
@c

void LeoFrame::OnUntangleSubmenu(wxCommandEvent&amp; WXUNUSED(event))
{

}
</t>
<t tx="T412">@ &lt;&lt; LeoFrame methods &gt;&gt; (31 of 157)
@c

void LeoFrame::OnImportExportSubmenu(wxCommandEvent&amp; WXUNUSED(event))
{

}
</t>
<t tx="T413">@ &lt;&lt; LeoFrame methods &gt;&gt; (32 of 157)
@c

void LeoFrame::OnQuit(wxCommandEvent&amp; WXUNUSED(event))
{
	gQuitting = TRUE ;

		// Closing all windows terminates Leo.  Stop if the user aborts.
		while ( gLeoFrameList )
			if ( ! gLeoFrameList -&gt; Close() )
				break ; // User cancelled a close.

	gQuitting = FALSE ;
}
</t>
<t tx="T414">@ &lt;&lt; LeoFrame methods &gt;&gt; (33 of 157)
@c

void LeoFrame::OnReadOutlineOnly(wxCommandEvent&amp; WXUNUSED(event))
{
	// Create the Open dialog.
	wxFileDialog d (
		NULL, "Choose a Leo file",
		"", // default directory
		"", // default file
		"*.leo", // wildcard
		wxOPEN | wxMULTIPLE ,  // style of dialog.
		wxDefaultPosition);

	if ( d.ShowModal() == wxID_OK ) {
		wxArrayString paths;
		d.GetPaths(paths);
		long count = paths.Count();
		for ( long i = 0 ; i &lt; count ; ++ i )
			this -&gt; readOutlineOnly ( paths.Item(i) ) ;
	}
}
</t>
<t tx="T415">@ &lt;&lt; LeoFrame methods &gt;&gt; (34 of 157)
@c

void LeoFrame::readOutlineOnly ( wxString fileName )
{
	// If the file is already open just bring its window to the front.
	LeoFrame * frame = gLeoFrameList ;
	while ( frame ) {
		if ( frame -&gt; mFileName == fileName ) {
			frame -&gt; Show();
			gActiveFrame = frame ;
		}
		frame = frame -&gt; mNextFrame ;
	}

	// Don't take an exception if the file doesn't exist.
	if ( ! ::wxFileExists ( fileName ) ) {
		wxString m("Can not open: ") ;
		m += fileName ;
		alert ( m.c_str() ) ;
		return ;
	}

	try {
		LeoFrame * frame = new LeoFrame ();
		frame -&gt; mCommands -&gt; readOutlineOnly( fileName ) ;
		frame -&gt; Show(TRUE);
		frame -&gt; mFileName = fileName ;
		gActiveFrame = frame ;
	}
	catch ( ... )
	{
		wxString m("Error opening: ") ;
		m += fileName ;
		alert ( m.c_str() ) ;
	}
}
</t>
<t tx="T416">@ &lt;&lt; LeoFrame methods &gt;&gt; (35 of 157)
@c

void LeoFrame::OnReadAtFileNodes(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; readAtFileNodes();
}
</t>
<t tx="T417">@ &lt;&lt; LeoFrame methods &gt;&gt; (36 of 157)
@c

void LeoFrame::OnWriteOutlineOnly(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; writeOutlineOnly();
}
</t>
<t tx="T418">@ &lt;&lt; LeoFrame methods &gt;&gt; (37 of 157)
@c

void LeoFrame::OnWriteAtFileNodes(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; writeAtFileNodes();
}
</t>
<t tx="T419">@ &lt;&lt; LeoFrame methods &gt;&gt; (38 of 157)
@c

void LeoFrame::OnTangleAll(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; tangleAll();
}
</t>
<t tx="T420">@ &lt;&lt; LeoFrame methods &gt;&gt; (39 of 157)
@c

void LeoFrame::OnTangleMarked(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; tangleMarked();
}
</t>
<t tx="T421">@ &lt;&lt; LeoFrame methods &gt;&gt; (40 of 157)
@c

void LeoFrame::OnTangle(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; tangle();
}
</t>
<t tx="T422">@ &lt;&lt; LeoFrame methods &gt;&gt; (41 of 157)
@c

void LeoFrame::OnUntangleAll(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; untangleAll();
}
</t>
<t tx="T423">@ &lt;&lt; LeoFrame methods &gt;&gt; (42 of 157)
@c

void LeoFrame::OnUntangleMarked(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; untangleMarked();
}
</t>
<t tx="T424">@ &lt;&lt; LeoFrame methods &gt;&gt; (43 of 157)
@c

void LeoFrame::OnUntangle(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; untangle();
}
</t>
<t tx="T425">@ &lt;&lt; LeoFrame methods &gt;&gt; (44 of 157)
@c

void LeoFrame::OnImportFiles(wxCommandEvent&amp; WXUNUSED(event))
{
	// Create the Open dialog.
	wxFileDialog d (
		NULL, "Import Files",
		"", // default directory
		"", // default file
		"*.*", // wildcard
		wxOPEN | wxMULTIPLE | wxFILE_MUST_EXIST,  // style of dialog.
		wxDefaultPosition);

	if ( d.ShowModal() == wxID_OK ) {
		wxArrayString paths;
		d.GetPaths(paths);
		mCommands -&gt; ImportFilesCommand (&amp;paths);
	}
}
</t>
<t tx="T426">@ &lt;&lt; LeoFrame methods &gt;&gt; (45 of 157)
@c

void LeoFrame::OnImportCWEBFiles(wxCommandEvent&amp; WXUNUSED(event))
{
	// Create the Open dialog.
	wxFileDialog d (
		NULL, "Import CWEB Files",
		"", // default directory
		"", // default file
		"*.*", // wildcard
		wxOPEN | wxMULTIPLE | wxFILE_MUST_EXIST,  // style of dialog.
		wxDefaultPosition);

	if ( d.ShowModal() == wxID_OK ) {
		wxArrayString paths;
		d.GetPaths(paths);
		mCommands -&gt; CWEBToOutlineCommand (&amp;paths);
	}
}
</t>
<t tx="T427">@ &lt;&lt; LeoFrame methods &gt;&gt; (46 of 157)
@c

void LeoFrame::OnImportNowebFiles(wxCommandEvent&amp; WXUNUSED(event))
{
	////
}
</t>
<t tx="T428">@ &lt;&lt; LeoFrame methods &gt;&gt; (47 of 157)
@c

void LeoFrame::OnImportMoreText(wxCommandEvent&amp; WXUNUSED(event))
{
	// Create the Open dialog.
	wxFileDialog d (
		NULL, "Import MORE Text",
		"", // default directory
		"", // default file
		"*.*", // wildcard
		wxOPEN | wxFILE_MUST_EXIST,  // style of dialog.
		wxDefaultPosition);

	if ( d.ShowModal() == wxID_OK ) {
		wxArrayString paths;
		d.GetPaths(paths);
		mCommands -&gt; importMoreText (&amp;paths);
	}
}
</t>
<t tx="T429">@ &lt;&lt; LeoFrame methods &gt;&gt; (48 of 157)
@c

void LeoFrame::OnFlattenOutline(wxCommandEvent&amp; WXUNUSED(event))
{
	// Create the Open dialog.
	wxFileDialog d (
		NULL, "Flatten Outline",
		"", // default directory
		"flat.txt", // default file
		"*.*", // wildcard
		wxSAVE | wxOVERWRITE_PROMPT,  // style of dialog.
		wxDefaultPosition);

	if ( d.ShowModal() == wxID_OK ) {
		wxArrayString paths;
		d.GetPaths(paths);
		mCommands -&gt; flattenOutline (&amp;paths);
	}
}
</t>
<t tx="T430">@ &lt;&lt; LeoFrame methods &gt;&gt; (49 of 157)
@c

void LeoFrame::OnUpdateCopy ( wxUpdateUIEvent&amp; event )
{
	wxWindow * w = this -&gt; FindFocus();

	if ( w &amp;&amp; w == mBodyCtrl )
		event.Enable( mBodyCtrl-&gt; CanCopy( ) ) ;
	else if ( w &amp;&amp; w == mLogCtrl )
		event.Enable( mLogCtrl-&gt; CanCopy( ) ) ;
	else
		event.Enable( FALSE ) ;
}
</t>
<t tx="T431">@ &lt;&lt; LeoFrame methods &gt;&gt; (50 of 157)
@c

void LeoFrame::OnUpdateCut ( wxUpdateUIEvent&amp; event )
{
	wxWindow * w = this -&gt; FindFocus();

	if ( w &amp;&amp; w == mBodyCtrl )
		event.Enable( mBodyCtrl-&gt; CanCut( ) ) ;
	else if ( w &amp;&amp; w == mLogCtrl )
		event.Enable( mLogCtrl-&gt; CanCut( ) ) ;
	else
		event.Enable( FALSE ) ;
}
</t>
<t tx="T432">@ &lt;&lt; LeoFrame methods &gt;&gt; (51 of 157)
@c

void LeoFrame::OnUpdateDelete ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mBodyCtrl &amp;&amp; mBodyCtrl -&gt; CanCut( ) ) ;
}
</t>
<t tx="T433">@ &lt;&lt; LeoFrame methods &gt;&gt; (52 of 157)
@c

void LeoFrame::OnUpdateExtract ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canExtract() ) ;
}
</t>
<t tx="T434">@ &lt;&lt; LeoFrame methods &gt;&gt; (53 of 157)
@c

void LeoFrame::OnUpdateExtractNames ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canExtractSectionNames() ) ;
}
</t>
<t tx="T435">@ &lt;&lt; LeoFrame methods &gt;&gt; (54 of 157)
@c

void LeoFrame::OnUpdateExtractSection ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canExtractSection() ) ;
}
</t>
<t tx="T436">@ &lt;&lt; LeoFrame methods &gt;&gt; (55 of 157)
@c

void LeoFrame::OnUpdateFind ( wxUpdateUIEvent&amp; event )
{
	event.Enable( find_text . Length() &gt; 0 ) ;
}
</t>
<t tx="T437">@ &lt;&lt; LeoFrame methods &gt;&gt; (56 of 157)
@c

void LeoFrame::OnUpdatePaste ( wxUpdateUIEvent&amp; event )
{
	#ifdef __WXMSW__ // apparent bug.
		event.Enable(TRUE);
	#else
		wxWindow * w = this -&gt; FindFocus();

		if ( w &amp;&amp; w == mBodyCtrl )
			event.Enable( mBodyCtrl-&gt; CanPaste( ) ) ;
		else if ( w &amp;&amp; w == mLogCtrl )
			event.Enable( mLogCtrl-&gt; CanPaste( ) ) ;
		else
			event.Enable( FALSE ) ;
	#endif
}
</t>
<t tx="T438">@ &lt;&lt; LeoFrame methods &gt;&gt; (57 of 157)
@c

void LeoFrame::OnUpdateRedo ( wxUpdateUIEvent&amp; event )
{
	bool enabled = FALSE ;

	// The Tree view does not support redo.

	#ifdef __WXGTK__ // text control does not support undo/redo on wxGTK
		enabled = FALSE ;
	#else
		enabled = ( mBodyCtrl &amp;&amp; mBodyCtrl -&gt; CanRedo() ) ;
	#endif

	event.Enable( enabled ) ;
}
</t>
<t tx="T439">@ &lt;&lt; LeoFrame methods &gt;&gt; (58 of 157)
@c

void LeoFrame::OnUpdateReplace ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; changeIsEnabled() ) ;
}
</t>
<t tx="T440">@ &lt;&lt; LeoFrame methods &gt;&gt; (59 of 157)
@c

void LeoFrame::OnUpdateSelectAll ( wxUpdateUIEvent&amp; event )
{
	wxWindow * w = this -&gt; FindFocus();

	event.Enable( w &amp;&amp; ( w == mBodyCtrl || w == mLogCtrl ) ) ;
}
</t>
<t tx="T441">@ &lt;&lt; LeoFrame methods &gt;&gt; (60 of 157)
@c

void LeoFrame::OnUpdateUndo ( wxUpdateUIEvent&amp; event )
{
	wxWindow * w = this -&gt; FindFocus();
	bool enabled = FALSE ;

	// FindFocus seems to be a bit flakey, so use it only when absolutely needed.

	if ( w == mTreeCtrl )
		enabled = mCommands -&gt; canUndo() ;
	else
		// Don't use FindFocus.
		#ifdef __WXGTK__ // text control does not support undo/redo on wxGTK
			enabled = FALSE ;
		#else
			enabled = ( mBodyCtrl &amp;&amp; mBodyCtrl -&gt; CanUndo() ) ;
		#endif

	event.Enable( enabled ) ;
}
</t>
<t tx="T442">@ &lt;&lt; LeoFrame methods &gt;&gt; (61 of 157)
@c

bool LeoFrame::hasSelection ( void )
{

	 if ( mBodyCtrl ) {
		long from, to ;
		mBodyCtrl  -&gt; GetSelection(&amp;from, &amp;to);
		return from != to ;
	}
	else return FALSE ;

#if 0 // old code:  now we just test mBodyCtrl.
	wxWindow * w = this -&gt; FindFocus();
	if ( w == NULL )
		return FALSE ;
	else if ( w == mBodyCtrl ) {
		long from, to ;
		mBodyCtrl  -&gt; GetSelection(&amp;from, &amp;to);
		return from != to ;
	}
	else if ( w == mTreeCtrl ) {
		#ifdef __WXMSW__
		wxTextCtrl * text = mTreeCtrl -&gt; GetEditControl() ;
		if ( text ) {
				long from, to ;
				text  -&gt; GetSelection(&amp;from, &amp;to);
				return from != to ;
		}
		#endif
	}

	return FALSE ;
#endif

}
</t>
<t tx="T443">@ &lt;&lt; LeoFrame methods &gt;&gt; (62 of 157)
@c

void LeoFrame::OnUndo(wxCommandEvent&amp; WXUNUSED(event))
{
	wxWindow * w = this -&gt; FindFocus();

	// FindFocus seems to be a bit flakey, so use it only when absolutely needed.

	if ( w == mTreeCtrl )
		mCommands -&gt; undo();

#ifndef __WXGTK__ // text control does not support undo/redo on wxGTK
	else if ( mBodyCtrl &amp;&amp; mBodyCtrl -&gt; CanUndo() )
		mBodyCtrl -&gt; Undo();
#endif

}
</t>
<t tx="T444">@ &lt;&lt; LeoFrame methods &gt;&gt; (63 of 157)
@c

void LeoFrame::OnRedo(wxCommandEvent&amp; WXUNUSED(event))
{
	// The tree control does not support redo.

#ifndef __WXGTK__ // text control does not support undo/redo on wxGTK
	if ( mBodyCtrl &amp;&amp; mBodyCtrl -&gt; CanRedo() )
		mBodyCtrl -&gt; Redo();
#endif

}
</t>
<t tx="T445">@ &lt;&lt; LeoFrame methods &gt;&gt; (64 of 157)
@c

void LeoFrame::OnCut(wxCommandEvent&amp; WXUNUSED(event))
{
	wxWindow * w = this -&gt; FindFocus();

	if ( w &amp;&amp; w == mBodyCtrl )
		mBodyCtrl-&gt; Cut( ) ;
	else if ( w &amp;&amp; w == mLogCtrl )
		mLogCtrl-&gt; Cut( ) ;
}
</t>
<t tx="T446">@ &lt;&lt; LeoFrame methods &gt;&gt; (65 of 157)
@c

void LeoFrame::OnCopy(wxCommandEvent&amp; WXUNUSED(event))
{
	wxWindow * w = this -&gt; FindFocus();

	if ( w &amp;&amp; w == mBodyCtrl )
		mBodyCtrl-&gt; Copy( ) ;
	else if ( w &amp;&amp; w == mLogCtrl )
		mLogCtrl-&gt; Copy( ) ;
}
</t>
<t tx="T447">@ &lt;&lt; LeoFrame methods &gt;&gt; (66 of 157)
@c

void LeoFrame::OnPaste(wxCommandEvent&amp; WXUNUSED(event))
{
	wxWindow * w = this -&gt; FindFocus();

	if ( w &amp;&amp; w == mBodyCtrl )
		mBodyCtrl-&gt; Paste( ) ;
	else if ( w &amp;&amp; w == mLogCtrl )
		mLogCtrl-&gt; Paste( ) ;
}
</t>
<t tx="T448">@ &lt;&lt; LeoFrame methods &gt;&gt; (67 of 157)
@c

void LeoFrame::OnDelete(wxCommandEvent&amp; WXUNUSED(event))
{
	if ( mBodyCtrl ) {
		long from, to ;
		mBodyCtrl -&gt; GetSelection(&amp;from, &amp;to);
		if ( from &lt; to )
			mBodyCtrl -&gt; Remove(from, to);
		else
			mBodyCtrl -&gt; Remove(to, from);
	}
}
</t>
<t tx="T449">@ &lt;&lt; LeoFrame methods &gt;&gt; (68 of 157)
@c

void LeoFrame::OnSelectAll(wxCommandEvent&amp; WXUNUSED(event))
{
	wxWindow * w = this -&gt; FindFocus();

	if ( w == mBodyCtrl ) {
		long to = mBodyCtrl -&gt; GetLastPosition();
		mBodyCtrl -&gt; SetSelection(0, to);
	}
	else if ( w == mLogCtrl ) {
		long to = mLogCtrl -&gt; GetLastPosition();
		mLogCtrl -&gt; SetSelection(0, to);
	}
}
</t>
<t tx="T450">@ &lt;&lt; LeoFrame methods &gt;&gt; (69 of 157)
@c

void LeoFrame::OnEditHeadline(wxCommandEvent&amp; WXUNUSED(event))
{
#ifndef __WXMSW__ // EditLabel is buggy.  Hitting a control key or tab will crash.
	wxTreeItemId item = mTreeCtrl-&gt;GetSelection();
	if ( item )
		mTreeCtrl-&gt;EditLabel( item );
#endif
}
</t>
<t tx="T451">@ &lt;&lt; LeoFrame methods &gt;&gt; (70 of 157)
@c

void LeoFrame::OnFontPanel(wxCommandEvent&amp; WXUNUSED(event))
{
	wxFontData data;
	data.SetInitialFont(mBodyCtrl -&gt; GetFont());
	data.SetColour(mBodyCtrl -&gt; GetForegroundColour());

	wxFontDialog dialog(this, &amp;data);
	#ifndef __WXGTK__  // Causes problems on GTK+ version of wxWindows.
		dialog.CentreOnScreen();
	#endif

	if (dialog.ShowModal() != wxID_OK)  return ;

	wxFontData retData = dialog.GetFontData();
	wxFont font = retData.GetChosenFont();
	wxColour color = retData.GetColour();

	// On Linux, SetFont apparently clears the text control's text string!

	#ifdef __WXGTK__
		wxString contents = mBodyCtrl -&gt; GetValue();
		mBodyCtrl -&gt; SetFont ( font ) ;
		mBodyCtrl -&gt; SetForegroundColour(color);
		mBodyCtrl -&gt; SetValue(contents);
	#else
		mBodyCtrl -&gt; SetFont ( font ) ;
		mBodyCtrl -&gt; SetForegroundColour(color);
	#endif

	this -&gt; Refresh();

	TRACEP("font_info",
		es("face: "); es( font . GetFaceName() . c_str() ) ; ecs();
		es("family: "); es( font . GetFamilyString() . c_str() ) ; enl();
		es("size: "); eint( font . GetPointSize() ) ; ecs();
		es("style: "); es( font. GetStyleString() . c_str() ) ; ecs();
		es("weight: "); es( font . GetWeightString() . c_str() ) ; enl();
	);
}
</t>
<t tx="T452">@ &lt;&lt; LeoFrame methods &gt;&gt; (71 of 157)
@c

void LeoFrame::OnSyntaxColoring(wxCommandEvent&amp; WXUNUSED(event))
{
	////
}
</t>
<t tx="T453">@ &lt;&lt; LeoFrame methods &gt;&gt; (72 of 157)
@c

void LeoFrame::OnPreferences(wxCommandEvent&amp; WXUNUSED(event))
{
	if ( gPrefsFrame == NULL ) {
		gPrefsFrame = new PrefsFrame ();
		gPrefsFrame -&gt; initialize();
	}

	gPrefsFrame -&gt; CenterOnScreen();
	gPrefsFrame -&gt; Show(TRUE);
	gPrefsFrame -&gt; Raise();
}
</t>
<t tx="T454">@ &lt;&lt; LeoFrame methods &gt;&gt; (73 of 157)
@c

void LeoFrame::OnConvertBlanks(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; convertBlanks();
}
</t>
<t tx="T455">@ &lt;&lt; LeoFrame methods &gt;&gt; (74 of 157)
@c

void LeoFrame::OnExtractSection(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; extractSection();
}
</t>
<t tx="T456">@ &lt;&lt; LeoFrame methods &gt;&gt; (75 of 157)
@c

void LeoFrame::OnExtractNames(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; extractSectionNames();
}
</t>
<t tx="T457">@ &lt;&lt; LeoFrame methods &gt;&gt; (76 of 157)
@c

void LeoFrame::OnExtract(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; extract();
}
</t>
<t tx="T458">@ &lt;&lt; LeoFrame methods &gt;&gt; (77 of 157)
@c

void LeoFrame::OnFindPanel(wxCommandEvent&amp; WXUNUSED(event))
{
	if ( gFindFrame == NULL )
		gFindFrame = new FindFrame ();

	// On windows, this activates the frame.
	gFindFrame -&gt; Show();
	gFindFrame -&gt; Raise();
}
</t>
<t tx="T459">@ &lt;&lt; LeoFrame methods &gt;&gt; (78 of 157)
@c

void LeoFrame::OnFindNext(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; doFindNextCommand();
}
</t>
<t tx="T460">@ &lt;&lt; LeoFrame methods &gt;&gt; (79 of 157)
@c

void LeoFrame::OnFindPrevious(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; doFindPreviousCommand();
}
</t>
<t tx="T461">@ &lt;&lt; LeoFrame methods &gt;&gt; (80 of 157)
@c

void LeoFrame::OnReplace(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; doChangeCommand();
}
</t>
<t tx="T462">@ &lt;&lt; LeoFrame methods &gt;&gt; (81 of 157)
@c

void LeoFrame::OnReplaceThenFind(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; doChangeThenFindCommand();
}
</t>
<t tx="T463">@ &lt;&lt; LeoFrame methods &gt;&gt; (82 of 157)
@c

void LeoFrame::OnUpdateCutNode ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canCutOutline() ) ;
}
</t>
<t tx="T464">@ &lt;&lt; LeoFrame methods &gt;&gt; (83 of 157)
@c

void LeoFrame::OnUpdateDeleteNode ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canDeleteHeadline() ) ;
}
</t>
<t tx="T465">@ &lt;&lt; LeoFrame methods &gt;&gt; (84 of 157)
@c

void LeoFrame::OnUpdatePasteNode ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canPasteOutline() ) ;
}
</t>
<t tx="T466">@ &lt;&lt; LeoFrame methods &gt;&gt; (85 of 157)
@c

void LeoFrame::OnUpdateSortNode ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canSort() ) ;
}
</t>
<t tx="T467">@ &lt;&lt; LeoFrame methods &gt;&gt; (86 of 157)
@c

void LeoFrame::OnUpdateExpandAll ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canExpandAllHeadlines() ) ;
}
</t>
<t tx="T468">@ &lt;&lt; LeoFrame methods &gt;&gt; (87 of 157)
@c

void LeoFrame::OnUpdateExpandAllChildren ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canExpandAllSubheads() ) ;
}
</t>
<t tx="T469">@ &lt;&lt; LeoFrame methods &gt;&gt; (88 of 157)
@c

void LeoFrame::OnUpdateExpandChildren ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canExpandAllSubheads() ) ;
}
</t>
<t tx="T470">@ &lt;&lt; LeoFrame methods &gt;&gt; (89 of 157)
@c

void LeoFrame::OnUpdateContractAll ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canContractAllHeadlines() ) ;
}
</t>
<t tx="T471">@ &lt;&lt; LeoFrame methods &gt;&gt; (90 of 157)
@c

void LeoFrame::OnUpdateContractAllChildren ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canContractAllSubheads() ) ;
}
</t>
<t tx="T472">@ &lt;&lt; LeoFrame methods &gt;&gt; (91 of 157)
@c

void LeoFrame::OnUpdateContractChildren ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canContractSubheads() ) ;
}
</t>
<t tx="T473">@ &lt;&lt; LeoFrame methods &gt;&gt; (92 of 157)
@c

void LeoFrame::OnUpdateMoveDown ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canMoveOutlineDown() ) ;
}
</t>
<t tx="T474">@ &lt;&lt; LeoFrame methods &gt;&gt; (93 of 157)
@c

void LeoFrame::OnUpdateMoveLeft ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canMoveOutlineLeft() ) ;
}
</t>
<t tx="T475">@ &lt;&lt; LeoFrame methods &gt;&gt; (94 of 157)
@c

void LeoFrame::OnUpdateMoveRight ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canMoveOutlineRight() ) ;
}
</t>
<t tx="T476">@ &lt;&lt; LeoFrame methods &gt;&gt; (95 of 157)
@c

void LeoFrame::OnUpdateMoveUp ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canMoveOutlineUp() ) ;
}
</t>
<t tx="T477">@ &lt;&lt; LeoFrame methods &gt;&gt; (96 of 157)
@c

void LeoFrame::OnUpdatePromote ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canPromote() ) ;
}
</t>
<t tx="T478">@ &lt;&lt; LeoFrame methods &gt;&gt; (97 of 157)
@c

void LeoFrame::OnUpdateDemote ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canDemote() ) ;
}
</t>
<t tx="T479">@ &lt;&lt; LeoFrame methods &gt;&gt; (98 of 157)
@c

void LeoFrame::OnUpdateGoPrevVisible ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canSelectVisBack() ) ;
}
</t>
<t tx="T480">@ &lt;&lt; LeoFrame methods &gt;&gt; (99 of 157)
@c

void LeoFrame::OnUpdateGoNextVisible ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canSelectVisNext() ) ;
}
</t>
<t tx="T481">@ &lt;&lt; LeoFrame methods &gt;&gt; (100 of 157)
@c

void LeoFrame::OnUpdateGoBack ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canSelectThreadBack() ) ;
}
</t>
<t tx="T482">@ &lt;&lt; LeoFrame methods &gt;&gt; (101 of 157)
@c

void LeoFrame::OnUpdateGoNext ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canSelectThreadNext() ) ;
}
</t>
<t tx="T483">@ &lt;&lt; LeoFrame methods &gt;&gt; (102 of 157)
@c

void LeoFrame::OnUpdateMark ( wxUpdateUIEvent&amp; event )
{
	vnode * v = mCommands -&gt; currentVnode();
	event.SetText( ( v &amp;&amp; v-&gt;isMarked()) ? "Unmark" : "Mark") ;
}
</t>
<t tx="T484">@ &lt;&lt; LeoFrame methods &gt;&gt; (103 of 157)
@c

void LeoFrame::OnUpdateMarkSubheads ( wxUpdateUIEvent&amp; event )
{
	vnode * v = mCommands -&gt; currentVnode();
	event.Enable( v &amp;&amp; v -&gt; hasChildren() ) ;
}
</t>
<t tx="T485">@ &lt;&lt; LeoFrame methods &gt;&gt; (104 of 157)
@c

void LeoFrame::OnUpdateMarkChangedItems ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canMarkChangedHeadlines() ) ;
}
</t>
<t tx="T486">@ &lt;&lt; LeoFrame methods &gt;&gt; (105 of 157)
@c

void LeoFrame::OnUpdateMarkChangedRoots ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canMarkChangedRoots() ) ;
}
</t>
<t tx="T487">@ &lt;&lt; LeoFrame methods &gt;&gt; (106 of 157)
@c

void LeoFrame::OnUpdateGoToNextMarked ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canGoToNextMarkedHeadline() ) ;
}
</t>
<t tx="T488">@ &lt;&lt; LeoFrame methods &gt;&gt; (107 of 157)
@c

void LeoFrame::OnUpdateGoToNextChanged ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canGoToNextDirtyHeadline() ) ;
}
</t>
<t tx="T489">@ &lt;&lt; LeoFrame methods &gt;&gt; (108 of 157)
@c

void LeoFrame::OnCutNode(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; cutOutline();
}
</t>
<t tx="T490">@ &lt;&lt; LeoFrame methods &gt;&gt; (109 of 157)
@c

void LeoFrame::OnCopyNode(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; copyOutline();
}
</t>
<t tx="T491">@ &lt;&lt; LeoFrame methods &gt;&gt; (110 of 157)
@c

void LeoFrame::OnPasteNode(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; pasteOutline();
}
</t>
<t tx="T492">@ &lt;&lt; LeoFrame methods &gt;&gt; (111 of 157)
@c

void LeoFrame::OnDeleteNode(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; deleteHeadline();
}
</t>
<t tx="T493">@ &lt;&lt; LeoFrame methods &gt;&gt; (112 of 157)
@c

void LeoFrame::OnInsertNode(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; insertHeadline();
}
</t>
<t tx="T494">@ &lt;&lt; LeoFrame methods &gt;&gt; (113 of 157)
@c

void LeoFrame::OnCloneNode(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; clone();
}
</t>
<t tx="T495">@ &lt;&lt; LeoFrame methods &gt;&gt; (114 of 157)
@c

void LeoFrame::OnSortNode(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; sort();
}
</t>
<t tx="T496">@ &lt;&lt; LeoFrame methods &gt;&gt; (115 of 157)
@c

void LeoFrame::OnExpandAll(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandAllHeadlines();
}
</t>
<t tx="T497">@ &lt;&lt; LeoFrame methods &gt;&gt; (116 of 157)
@c

void LeoFrame::OnExpandAllChildren(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandAllSubheads();
}
</t>
<t tx="T498">@ &lt;&lt; LeoFrame methods &gt;&gt; (117 of 157)
@c

void LeoFrame::OnExpandChildren(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandSubheads();
}
</t>
<t tx="T499">@ &lt;&lt; LeoFrame methods &gt;&gt; (118 of 157)
@c

void LeoFrame::OnContractAll(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; contractAllHeadlines();
}
</t>
<t tx="T500">@ &lt;&lt; LeoFrame methods &gt;&gt; (119 of 157)
@c

void LeoFrame::OnContractAllChildren(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; contractAllSubheads();
}
</t>
<t tx="T501">@ &lt;&lt; LeoFrame methods &gt;&gt; (120 of 157)
@c

void LeoFrame::OnContractChildren(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; contractSubheads();
}
</t>
<t tx="T502">@ &lt;&lt; LeoFrame methods &gt;&gt; (121 of 157)
@c

void LeoFrame::OnExpandNextLevel(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandNextLevel();
}
</t>
<t tx="T503">@ &lt;&lt; LeoFrame methods &gt;&gt; (122 of 157)
@c

void LeoFrame::OnExpandToLevel1(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel1();
}
</t>
<t tx="T504">@ &lt;&lt; LeoFrame methods &gt;&gt; (123 of 157)
@c

void LeoFrame::OnExpandToLevel2(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel2();
}
</t>
<t tx="T505">@ &lt;&lt; LeoFrame methods &gt;&gt; (124 of 157)
@c

void LeoFrame::OnExpandToLevel3(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel3();
}
</t>
<t tx="T506">@ &lt;&lt; LeoFrame methods &gt;&gt; (125 of 157)
@c

void LeoFrame::OnExpandToLevel4(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel4();
}
</t>
<t tx="T507">@ &lt;&lt; LeoFrame methods &gt;&gt; (126 of 157)
@c

void LeoFrame::OnExpandToLevel5(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel5();
}
</t>
<t tx="T508">@ &lt;&lt; LeoFrame methods &gt;&gt; (127 of 157)
@c

void LeoFrame::OnExpandToLevel6(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel6();
}
</t>
<t tx="T509">@ &lt;&lt; LeoFrame methods &gt;&gt; (128 of 157)
@c

void LeoFrame::OnExpandToLevel7(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel7();
}
</t>
<t tx="T510">@ &lt;&lt; LeoFrame methods &gt;&gt; (129 of 157)
@c

void LeoFrame::OnExpandToLevel8(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel8();
}
</t>
<t tx="T511">@ &lt;&lt; LeoFrame methods &gt;&gt; (130 of 157)
@c

void LeoFrame::OnExpandToLevel9(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel9();
}
</t>
<t tx="T512">@ &lt;&lt; LeoFrame methods &gt;&gt; (131 of 157)
@c

void LeoFrame::OnMoveDown(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; moveOutlineDown();
}
</t>
<t tx="T513">@ &lt;&lt; LeoFrame methods &gt;&gt; (132 of 157)
@c

void LeoFrame::OnMoveLeft(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; moveOutlineLeft();
}
</t>
<t tx="T514">@ &lt;&lt; LeoFrame methods &gt;&gt; (133 of 157)
@c

void LeoFrame::OnMoveRight(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; moveOutlineRight();
}
</t>
<t tx="T515">@ &lt;&lt; LeoFrame methods &gt;&gt; (134 of 157)
@c

void LeoFrame::OnMoveUp(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; moveOutlineUp();
}
</t>
<t tx="T516">@ &lt;&lt; LeoFrame methods &gt;&gt; (135 of 157)
@c

void LeoFrame::OnPromote(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; promote();
}
</t>
<t tx="T517">@ &lt;&lt; LeoFrame methods &gt;&gt; (136 of 157)
@c

void LeoFrame::OnDemote(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; demote();
}
</t>
<t tx="T518">@ &lt;&lt; LeoFrame methods &gt;&gt; (137 of 157)
@c

void LeoFrame::OnGoPrevVisible(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; moveOutlineUp();
}
</t>
<t tx="T519">@ &lt;&lt; LeoFrame methods &gt;&gt; (138 of 157)
@c

void LeoFrame::OnGoNextVisible(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; selectVisNext();
}
</t>
<t tx="T520">@ &lt;&lt; LeoFrame methods &gt;&gt; (139 of 157)
@c

void LeoFrame::OnGoBack(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; selectThreadBack();
}
</t>
<t tx="T521">@ &lt;&lt; LeoFrame methods &gt;&gt; (140 of 157)
@c

void LeoFrame::OnGoNext(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; selectThreadNext();
}
</t>
<t tx="T522">@ &lt;&lt; LeoFrame methods &gt;&gt; (141 of 157)
@c

void LeoFrame::OnMark(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; markHeadline();
}
</t>
<t tx="T523">@ &lt;&lt; LeoFrame methods &gt;&gt; (142 of 157)
@c

void LeoFrame::OnMarkSubheads(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; markSubheads();
}
</t>
<t tx="T524">@ &lt;&lt; LeoFrame methods &gt;&gt; (143 of 157)
@c

void LeoFrame::OnMarkChangedItems(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; markChangedHeadlines();
}
</t>
<t tx="T525">@ &lt;&lt; LeoFrame methods &gt;&gt; (144 of 157)
@c

void LeoFrame::OnMarkChangedRoots(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; markChangedRoots();
}
</t>
<t tx="T526">@ &lt;&lt; LeoFrame methods &gt;&gt; (145 of 157)
@c

void LeoFrame::OnMarkAllAtFileNodesDirty(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; markAllAtFileNodesDirty();
}
</t>
<t tx="T527">@ &lt;&lt; LeoFrame methods &gt;&gt; (146 of 157)
@c

void LeoFrame::OnMarkAtFileNodesDirty(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; markAtFileNodesDirty();
}
</t>
<t tx="T528">@ &lt;&lt; LeoFrame methods &gt;&gt; (147 of 157)
@c

void LeoFrame::OnUnmarkAll(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; unmarkAll();
}
</t>
<t tx="T529">@ &lt;&lt; LeoFrame methods &gt;&gt; (148 of 157)
@c

void LeoFrame::OnGoToNextMarked(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; goToNextMarkedHeadline();
}
</t>
<t tx="T530">@ &lt;&lt; LeoFrame methods &gt;&gt; (149 of 157)
@c

void LeoFrame::OnGoToNextChanged(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; goToNextDirtyHeadline();
}
</t>
<t tx="T531">@ &lt;&lt; LeoFrame methods &gt;&gt; (150 of 157)
@c

void LeoFrame::OnEqualSizedPanes(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; equalSizedPanes();
}
</t>
<t tx="T532">@ &lt;&lt; LeoFrame methods &gt;&gt; (151 of 157)
@c

void LeoFrame::OnToggleActivePane(wxCommandEvent&amp; WXUNUSED(event))
{
	wxWindow * w = this -&gt; FindFocus();

	if ( w == NULL || w == mTreeCtrl )
		mBodyCtrl -&gt; SetFocus();
	else
		mTreeCtrl -&gt; SetFocus();
}
</t>
<t tx="T533">@ &lt;&lt; LeoFrame methods &gt;&gt; (152 of 157)
@c

void LeoFrame::OnChangeDirection(wxCommandEvent&amp; WXUNUSED(event))
{
	int mode = mSplitter1 -&gt; GetSplitMode();
	mSplitter1 -&gt; Unsplit(); // Hides the text control.

	if ( mode == wxSPLIT_VERTICAL )
		mSplitter1 -&gt; SplitHorizontally(mTreeCtrl, mBodyCtrl, 0);
	else
		mSplitter1 -&gt; SplitVertically(mTreeCtrl, mBodyCtrl, 0);

	mBodyCtrl -&gt; Show();
	mBodyCtrl -&gt; SetFocus();
}
</t>
<t tx="T534">@ &lt;&lt; LeoFrame methods &gt;&gt; (153 of 157)
@c

void LeoFrame::OnCascade(wxCommandEvent&amp; WXUNUSED(event))
{
	wxPoint p ( 10, 10 ) ;

	for ( LeoFrame * f = gLeoFrameList ; f ; f = f -&gt; mNextFrame ) {
		f -&gt; Move ( p ) ;
		p.x += 30 ;
		p.y += 30 ;
		if ( p.x &gt; 200 ) {
			p.x = 10 ;
			p.y = 40 ;
		}
	}
}
</t>
<t tx="T535">@ &lt;&lt; LeoFrame methods &gt;&gt; (154 of 157)
@c

void LeoFrame::OnMinimizeAll(wxCommandEvent&amp; WXUNUSED(event))
{
	if ( gPrefsFrame )
		gPrefsFrame -&gt; Iconize();
	if ( gFindFrame )
		gFindFrame -&gt; Iconize();
	if ( gPythonFrame )
		gPythonFrame -&gt; Iconize();

	for ( LeoFrame * f = gLeoFrameList ; f ; f = f -&gt; mNextFrame )
		f -&gt; Iconize();

}
</t>
<t tx="T536">@ &lt;&lt; LeoFrame methods &gt;&gt; (155 of 157)
@c

#ifdef __WXMSW__
#define SWIGEXPORT(a,b) a _export b
extern "C" SWIGEXPORT(void,initleoc)();
#else
extern "C" void initleoc();
#endif

#ifdef __WXMSW__
void LeoFrame::OnOpenPythonWindow(wxCommandEvent&amp; WXUNUSED(event))
{
	gPythonFrame = wxPythonFrame::create((char *)"leoc", (char *)"leo", (void (*)()) initleoc);
	gPythonFrame -&gt; Show(TRUE);
}
</t>
<t tx="T537">#endif // __WXMSW__
// &lt;&lt; LeoFrame methods &gt;&gt; (156 of 157)
void LeoFrame::OnRecentWindows(wxCommandEvent&amp; WXUNUSED(event))
{
	//// Not ready yet.
}
</t>
<t tx="T538">@ &lt;&lt; LeoFrame methods &gt;&gt; (157 of 157)
@c

void LeoFrame::OnAbout(wxCommandEvent&amp; WXUNUSED(event))
{
	wxString message =
"wxLeo Version 0.08 (beta), October 24, 2001\n\
Copyright © 2001 by Edward K. Ream\n\
All Rights Reserved \n\
Leo is distributed under the Python License";

	wxMessageBox(
		message,"About Leo",
		wxCenter,
		this);
}
</t>
<t tx="T539">&lt;&lt; LeoPrefs declarations &gt;&gt;

@others
</t>
<t tx="T540">// &lt;&lt; LeoPrefs private constants &gt;&gt;
/*
	These must match the order of items in the wxRadioBox.
	These are _not_ the same as vars in args.h.
*/
enum {
	c_target = 0,
	cweb_target,
	html_target,
	java_target,
	pascal_target,
	perl_target,
	perlpod_target,
	plain_text_target,
	python_target,
	bad_last_target
} ;
</t>
<t tx="T541">BEGIN_EVENT_TABLE(PrefsFrame, wxFrame)

	EVT_ACTIVATE ( PrefsFrame::OnActivatePrefsFrame)
	EVT_CLOSE( PrefsFrame::OnClosePrefsFrame)

	// Global options panel...
	EVT_TEXT ( cPrefsPageWidthText, PrefsFrame::OnPageWidthText )
	EVT_CHECKBOX ( cPrefsDoneBatCheckBox, PrefsFrame::OnDoneBatCheckBox )
	EVT_CHECKBOX ( cPrefsUnBatCheckBox, PrefsFrame::OnUnBatCheckBox )

	// Tangle options panel...
	EVT_TEXT ( cPrefsTangleDirectoryText, PrefsFrame::OnTangleDirectoryText )
	EVT_CHECKBOX ( cPrefsHeaderCheckBox, PrefsFrame::OnHeaderCheckBox )
	EVT_CHECKBOX ( cPrefsDocChunksCheckBox, PrefsFrame::OnDocChunksCheckBox )

	// Target language panel...
	EVT_RADIOBOX ( cPrefsTargetLanguageRadioBox, PrefsFrame::OnTargetLanguageRadioBox )

END_EVENT_TABLE()

BEGIN_EVENT_TABLE(PrefsPanel, wxPanel)

END_EVENT_TABLE()</t>
<t tx="T542">PrefsFrame::PrefsFrame()

	: wxFrame((wxFrame *)NULL, -1, "Leo Preferences",
		wxPoint(50, 50), wxDefaultSize,
		wxMINIMIZE_BOX | wxTHICK_FRAME | wxSYSTEM_MENU | wxCAPTION)
{
	mPrefsPanel = new PrefsPanel(this);

	// Resize to fit the panel.
	wxBoxSizer * sizer = new wxBoxSizer(wxVERTICAL);
	sizer -&gt; Add ( mPrefsPanel );
	SetAutoLayout( TRUE );  // tell dialog to use sizer
	SetSizer( sizer );  // actually set the sizer
	sizer -&gt; Fit( this ); // set size to minimum size as calculated by the sizer
	sizer -&gt; SetSizeHints( this ); // set size hints to honour mininum size

	// Set the window icon.
	#ifdef __WXMSW__
	  this -&gt;SetIcon(wxIcon("LeoIcon"));
	#endif
}
</t>
<t tx="T543">@ &lt;&lt; LeoPrefs methods &gt;&gt; (2 of 14)
@c

void PrefsFrame::initialize( void )
{
	// This may be called during construction.
	if ( ! gPrefsFrame ) return ;

	wxString s("");

	if ( gActiveFrame ) {
		s += wxString::Format("%d", gActiveFrame -&gt; mPageWidth);
		mPrefsPanel -&gt; mPrefsPageWidthText -&gt;
			SetValue(s) ;
		mPrefsPanel -&gt; mPrefsDoneBatCheckBox -&gt;
			SetValue(gActiveFrame -&gt; mTangleBatchFlag) ;
		mPrefsPanel -&gt; mPrefsUnBatCheckBox -&gt;
			SetValue(gActiveFrame -&gt; mUntangleBatchFlag) ;

		mPrefsPanel -&gt; mPrefsTangleDirectoryText -&gt;
			SetValue(gActiveFrame -&gt; mDefaultDirectory) ;
		mPrefsPanel -&gt; mPrefsHeaderCheckBox -&gt;
			SetValue(gActiveFrame -&gt; mUseHeaderFlag) ;
		mPrefsPanel -&gt; mPrefsDocChunksCheckBox -&gt;
			SetValue(gActiveFrame -&gt; mOutputDocFlag) ;

		mPrefsPanel -&gt; mTargetLanguageRadioBox -&gt;
			SetSelection(languageToTarget(gActiveFrame -&gt; mTargetLanguage)) ;
	}
	else {
		s += wxString::Format("%d", arg_page_width);
		mPrefsPanel -&gt; mPrefsPageWidthText -&gt; SetValue(s) ;
		mPrefsPanel -&gt; mPrefsDoneBatCheckBox -&gt; SetValue(arg_tangle_batch) ;
		mPrefsPanel -&gt; mPrefsUnBatCheckBox -&gt; SetValue(arg_untangle_batch) ;

		// No global setting for director.
		mPrefsPanel -&gt; mPrefsHeaderCheckBox -&gt; SetValue(arg_use_header_flag) ;
		mPrefsPanel -&gt; mPrefsDocChunksCheckBox -&gt; SetValue(arg_output_doc_flag) ;

		mPrefsPanel -&gt; mTargetLanguageRadioBox -&gt;
			SetSelection(languageToTarget(arg_target_language)) ;
	}
}
</t>
<t tx="T544">@ &lt;&lt; LeoPrefs methods &gt;&gt; (3 of 14)
@c

long PrefsFrame::targetToLanguage ( long target )
{
	switch ( target ) {
	case c_target :     return c_language ;
	case cweb_target:   return cweb_language ;
	case html_target:   return html_language ;
	case java_target:   return java_language ;
	case perl_target:   return perl_language ;
	case perlpod_target: return perlpod_language ;
	case pascal_target: return pascal_language ;
	case plain_text_target: return plain_text_language ;
	case python_target: return python_language ;
	default:            return plain_text_language ;
	}
}
</t>
<t tx="T545">@ &lt;&lt; LeoPrefs methods &gt;&gt; (4 of 14)
@c

long PrefsFrame::languageToTarget ( long language )
{
	switch ( language ) {
	case c_language:      return c_target ;
	case cweb_language:   return cweb_target ;
	case html_language:   return html_target ;
	case java_language:   return java_target ;
	case pascal_language: return pascal_target ;
	case perl_language:   return perl_target ;
	case perlpod_language: return perlpod_target ;
	case plain_text_language: return plain_text_target ;
	case python_language: return python_target ;
	default:              return plain_text_target ;
	}
}
</t>
<t tx="T546">@ &lt;&lt; LeoPrefs methods &gt;&gt; (5 of 14)
@c

void PrefsFrame::OnActivatePrefsFrame(wxActivateEvent&amp; event)
{
	if ( gPrefsFrame &amp;&amp; event.GetActive() )
		gPrefsFrame -&gt; initialize();
}
</t>
<t tx="T547">@ &lt;&lt; LeoPrefs methods &gt;&gt; (6 of 14)
This is an event handler function called when the user has tried to close a frame or dialog box. It is called via the  wxWindow::Close function, so that the application can also invoke the handler programmatically.  You should check whether the application is forcing the deletion of the window using CanVeto. If CanVeto returns FALSE, it is  not possible to skip window deletion; destroy the window using wxWindow::Destroy. If not, it is up to you whether you respond  by destroying the window.  If you don't destroy the window, you should call wxCloseEvent::Veto to let the calling code know that you did not destroy the  window. This allows the wxWindow::Close function to return TRUE or FALSE depending on whether the close instruction was  honoured or not.
@c

void PrefsFrame::OnClosePrefsFrame(wxCloseEvent&amp; event)
{
	if ( event.CanVeto() ) {
		event.Veto();  // Did not destroy the window.
		this -&gt; Show(FALSE);  // Just hide the window.
	}
	else {
		this -&gt; Destroy();
		gPrefsFrame = NULL ;
	}
}
</t>
<t tx="T548">@ &lt;&lt; LeoPrefs methods &gt;&gt; (7 of 14)
@c

void PrefsFrame::OnPageWidthText (wxCommandEvent&amp; event)
{
	wxTextCtrl * text = (wxTextCtrl *) event.GetEventObject() ;
	wxString s = text -&gt; GetValue();
	long n = 0 ;
	if ( s.ToLong(&amp;n) ) {
		arg_page_width = default_page_width = n ;
		if ( gActiveFrame )
			gActiveFrame -&gt; mPageWidth = arg_page_width ;
	}
}
</t>
<t tx="T549">@ &lt;&lt; LeoPrefs methods &gt;&gt; (8 of 14)
@c

void PrefsFrame::OnDoneBatCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	arg_tangle_batch = default_tangle_batch = box -&gt; GetValue() ;
	if ( gActiveFrame ) gActiveFrame -&gt; mTangleBatchFlag = arg_tangle_batch ;
}
</t>
<t tx="T550">@ &lt;&lt; LeoPrefs methods &gt;&gt; (9 of 14)
@c

void PrefsFrame::OnUnBatCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	arg_untangle_batch = default_untangle_batch = box -&gt; GetValue() ;
	if ( gActiveFrame ) gActiveFrame -&gt; mUntangleBatchFlag = arg_untangle_batch ;
}
</t>
<t tx="T551">@ &lt;&lt; LeoPrefs methods &gt;&gt; (10 of 14)
@c

void PrefsFrame::OnTangleDirectoryText (wxCommandEvent&amp; event)
{
	wxTextCtrl * text = (wxTextCtrl *) event.GetEventObject() ;
	wxString s = text -&gt; GetValue();
	if ( gActiveFrame ) {
		gActiveFrame -&gt; mDefaultDirectory = s ;
		if ( gActiveFrame -&gt; mDefaultDirectory . Length() &gt; 0 )
			wxSetWorkingDirectory ( gActiveFrame -&gt; mDefaultDirectory ) ;
		else if ( gActiveFrame -&gt; mOpenDirectory . Length() &gt; 0 )
			wxSetWorkingDirectory ( gActiveFrame -&gt; mOpenDirectory ) ;
	}
}
</t>
<t tx="T552">@ &lt;&lt; LeoPrefs methods &gt;&gt; (11 of 14)
@c

void PrefsFrame::OnHeaderCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	arg_use_header_flag = default_use_header_flag = box -&gt; GetValue() ;
	if ( gActiveFrame ) gActiveFrame -&gt; mUseHeaderFlag = arg_use_header_flag ;
}
</t>
<t tx="T553">@ &lt;&lt; LeoPrefs methods &gt;&gt; (12 of 14)
@c

void PrefsFrame::OnDocChunksCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	arg_output_doc_flag = default_output_doc_flag = box -&gt; GetValue();
	if ( gActiveFrame ) gActiveFrame -&gt; mOutputDocFlag = arg_output_doc_flag ;
}
</t>
<t tx="T554">@ &lt;&lt; LeoPrefs methods &gt;&gt; (13 of 14)
@c

void PrefsFrame::OnTargetLanguageRadioBox (wxCommandEvent&amp; event)
{
	wxRadioBox * box = (wxRadioBox *)event.GetEventObject() ;
	long targetIndex = box -&gt; GetSelection();
	default_target_language = arg_target_language = targetToLanguage(targetIndex );

	// Careful:  The @language or @nocolor will override this.
	if ( gActiveFrame ) {
		gActiveFrame -&gt; mTargetLanguage = arg_target_language ;
		Commands * commands = gActiveFrame -&gt; mCommands ;
		vnode * v = commands -&gt; currentVnode();
		gActiveFrame -&gt; mCommands -&gt; scanAllDirectives( v,
			cDontRequirePath, cDontIssueErrors );

		#if 0 //// syntax coloring
		TSyntaxMemoParser * parser = NULL ;
		if ( commands -&gt; useSyntaxColoring(v) )
			parser = commands -&gt; TSMParser ( arg_present_language ) ;
		else
			parser = commands -&gt; TSMParser ( plain_text_language )  ;

		commands -&gt; mSyntaxMemo -&gt; Parser1 = parser ;
		gActiveFrame -&gt; mParser = parser ;
		#endif
	}
}
</t>
<t tx="T555">@ &lt;&lt; LeoPrefs methods &gt;&gt; (14 of 14)
@c

PrefsPanel::PrefsPanel(wxFrame *frame)
	   : wxPanel(frame, -1)
{
	// &lt;&lt; Create the preferences controls &gt;&gt;
	wxBoxSizer * topSizer = new wxBoxSizer(wxVERTICAL);

	// &lt;&lt; Create the Global Options static box &gt;&gt;
	wxStaticBox * globalOptionsBox = new wxStaticBox(this, -1,
		"Global Options",
		wxPoint(10,10), wxSize(250,110), 0, "" );

	wxStaticBoxSizer * sizer = new wxStaticBoxSizer(globalOptionsBox, wxVERTICAL);
	wxBoxSizer * lineSizer = new wxBoxSizer(wxHORIZONTAL);
	sizer -&gt; Add ( 0, 5 ) ; // Extra vertical space.

	// Text control.
	mPrefsPageWidthText = new wxTextCtrl(this,
		cPrefsPageWidthText, "132",
		wxDefaultPosition, wxSize(50,25), 0,
		wxDefaultValidator, "") ;
	lineSizer -&gt; Add ( mPrefsPageWidthText );
	lineSizer -&gt; Add ( 20, 0 ) ; // Width.

	// Label for text control.
	lineSizer -&gt; Add (
		new wxStaticText(this, -1, "Page Width",
			wxPoint(-1,10), wxSize(100,25), 0, "") ,
		0, wxBORDER | wxTOP, 5);  // Vertical offset 5.
	sizer -&gt; Add ( lineSizer );

	mPrefsDoneBatCheckBox = new wxCheckBox(this,
		cPrefsDoneBatCheckBox,
		"Execute Leo_done.bat after Tangle",
		wxDefaultPosition, wxSize(235,25), 0,
		wxDefaultValidator, "") ;
	sizer -&gt; Add ( mPrefsDoneBatCheckBox );

	mPrefsUnBatCheckBox = new wxCheckBox(this,
		cPrefsUnBatCheckBox,
		"Execute Leo_un.bat after Untangle",
		wxDefaultPosition, wxSize(235,25), 0,
		wxDefaultValidator, "") ;
	sizer -&gt; Add ( mPrefsUnBatCheckBox );
	// -- end -- &lt;&lt; Create the Global Options static box &gt;&gt;
	topSizer -&gt; Add ( sizer );
	topSizer -&gt; Add ( 0, 10 );
	// &lt;&lt; Create the Default Tangle Options static box &gt;&gt;
	wxStaticBox * optionsBox = new wxStaticBox(this, -1,
		"Default Tangle Options",
		wxDefaultPosition, wxSize(250,210),
		0, "zzzz" );

	wxStaticBoxSizer * sizer2 = new wxStaticBoxSizer(optionsBox, wxVERTICAL);
	sizer2 -&gt; Add ( 0, 10 ) ;  // Vertical space.

	// Label.
	sizer2 -&gt; Add (
		new wxStaticText(this, -1,
			"Default Tangle directory",
			wxDefaultPosition, wxSize(165,25), 0, ""),
		0, wxBORDER | wxLEFT, 30);  // Indent 30.

	mPrefsTangleDirectoryText = new wxTextCtrl(this,
		cPrefsTangleDirectoryText, "",
		wxDefaultPosition, wxSize(230,25), 0,
		wxDefaultValidator, "") ;
	sizer2 -&gt; Add ( mPrefsTangleDirectoryText );

	mPrefsHeaderCheckBox = new wxCheckBox(this,
		cPrefsHeaderCheckBox,
		"Tangle outputs header line",
		wxDefaultPosition, wxSize(235,25), 0,
		wxDefaultValidator, "") ;
	sizer2 -&gt; Add ( mPrefsHeaderCheckBox );

	mPrefsDocChunksCheckBox = new wxCheckBox(this,
		cPrefsDocChunksCheckBox,
		"Tangle outputs document chunks",
		wxDefaultPosition, wxSize(235,25), 0,
		wxDefaultValidator, "") ;
	sizer2 -&gt; Add ( mPrefsDocChunksCheckBox );
	// -- end -- &lt;&lt; Create the Default Tangle Options static box &gt;&gt;
	topSizer -&gt; Add ( sizer2 );
	topSizer -&gt; Add ( 0, 10 );
	// &lt;&lt; Create the Default Target Language radio buttons &gt;&gt;
	wxString targetLanguageChoices[] = {
		"C/C++", "CWEB", "HTML", "Java",
		"Pascal", "Perl", "Perl + POD", "Plain text", "Python",
	};

	// We specify rows so that items will be sorted down the columns.
	mTargetLanguageRadioBox = new wxRadioBox( this,
		cPrefsTargetLanguageRadioBox,
		"Default Target Language",
		wxDefaultPosition, wxSize( 245, 145 ),
		WXSIZEOF(targetLanguageChoices),
		targetLanguageChoices,
		5, wxRA_SPECIFY_ROWS);
	// -- end -- &lt;&lt; Create the Default Target Language radio buttons &gt;&gt;
	topSizer -&gt; Add ( mTargetLanguageRadioBox );

	SetAutoLayout( TRUE );  // tell dialog to use sizer
	SetSizer( topSizer );  // actually set the sizer
	topSizer -&gt; Fit( this ); // set size to minimum size as calculated by the sizer
	topSizer -&gt; SetSizeHints( this ); // set size hints to honour mininum size
	// -- end -- &lt;&lt; Create the preferences controls &gt;&gt;
}
</t>
<t tx="T556">@ You may have to change the paths to the wxWindows docs by hand:  find/change doesn't work in headlines.
</t>
<t tx="T557"></t>
<t tx="T558"></t>
<t tx="T559"></t>
<t tx="T560"></t>
<t tx="T561"></t>
<t tx="T562"></t>
<t tx="T563"></t>
<t tx="T564"></t>
<t tx="T565"></t>
<t tx="T566"></t>
<t tx="T567"></t>
<t tx="T568"></t>
<t tx="T569"></t>
<t tx="T570"></t>
<t tx="T571"></t>
<t tx="T572"></t>
<t tx="T573"></t>
<t tx="T574"></t>
<t tx="T575"></t>
<t tx="T576"></t>
<t tx="T577"></t>
<t tx="T578"></t>
<t tx="T579"></t>
<t tx="T580"></t>
<t tx="T581"></t>
<t tx="T582"></t>
<t tx="T583"></t>
<t tx="T584"></t>
<t tx="T585"></t>
<t tx="T586"></t>
<t tx="T587"></t>
<t tx="T588"></t>
<t tx="T589"></t>
<t tx="T590">Will I ever have to use wxArray, wxList, wxStream, wxString.

In particular, can I use Python strings instead of wxStrings?

Can I create multiple windows without using the wxDoc classes?</t>
<t tx="T591"># Executing the following script creates a wxWindows prototype of Leo.
# Just do the Execute Script command from here.
# For this to work the path to wxLeo.py must be in sys.path.

# The first time you do this the window is created twice: once for the import and once for the reload.
# Thereafter only the reload takes effect, so only one window gets created.
# The purpose of reload is so you can change the prototype code without restarting Leo.

# To do:
# - convert this to a plugin that overrides Leo's actual code.
# - Create an icons area and put row/column numbers in the status area.
	

import wxLeo
reload(wxLeo)
</t>
<t tx="T592">from wxPython import wx

true  = 1==1
false = 1==0

cSplitterWindow = 101
cTreeCtrl = 102
cBodyCtrl = 103
cLogCtrl = 104
cOuterFrame = 105
cIconFrame = 106

cAboutLeoMenuItem = 1001

width = 600 

@others

def trace(): print "trace"

app = leoApp()
frame = leoFrame()
app.SetTopWindow(frame)
frame.Show(true)
app.MainLoop()</t>
<t tx="T593">class leoApp (wx.wxApp):
	
	@others
</t>
<t tx="T594">def OnInit(self):
	# print "leoApp:OnInit"
	return true</t>
<t tx="T595">class leoFrame(wx.wxFrame):
	@others</t>
<t tx="T596">def __init__ (self):
	
	wx.wxFrame.__init__(self, None, -1, "leoFrame")
		# wx.wxDefaultPosition, wx.wxDefaultSize,
		#wx.wxSUNKEN_BORDER,
		#wx.wxNO_3D # hangs.
		#"leoFrame")

	#self.outerPanel = wx.wxPanel(self,-1)
	
	##self.iconPanel = wx.wxPanel(self.outerPanel, -1, "iconPanel")
	
	self.CreateStatusBar()
	#self.createMenus()
	self.createMenuBar()
	
	self.splitter1 = wx.wxSplitterWindow(self,
		cSplitterWindow,
		wx.wxDefaultPosition, wx.wxDefaultSize,
		wx.wxSP_NOBORDER)
		
	# No effect.
	self.splitter1.SetForegroundColour(wx.wxRED)
	self.splitter1.SetBackgroundColour(wx.wxRED)

	self.splitter2 = wx.wxSplitterWindow(self.splitter1, -1,
		wx.wxDefaultPosition, wx.wxDefaultSize,
		wx.wxSP_NOBORDER)
		# wx.wxSP_BORDER | wx.wxSP_3D, "splitterWindow");
	
	self.splitter1.SetMinimumPaneSize(4)
	self.splitter2.SetMinimumPaneSize(4)
	
	self.tree = wx.wxTreeCtrl(self.splitter2, cTreeCtrl,
		wx.wxDefaultPosition, wx.wxDefaultSize,
		wx.wxTR_HAS_BUTTONS | wx.wxTR_EDIT_LABELS, wx.wxDefaultValidator, "treeCtrl")

	self.body = wx.wxTextCtrl(self.splitter1, cBodyCtrl, "",
		wx.wxDefaultPosition, wx.wxDefaultSize,
		wx.wxTE_MULTILINE)
	
	self.log = wx.wxTextCtrl(self.splitter2, cLogCtrl, "",
		wx.wxDefaultPosition, wx.wxDefaultSize, wx.wxTE_MULTILINE )
	
	# Attach the controls to the splitter.
	self.splitter1.SplitHorizontally(self.splitter2, self.body, 0)
	self.splitter2.SplitVertically(self.tree, self.log, width/2)</t>
<t tx="T597">def createMenus(self):

	menuBar = wx.wxMenuBar()
	if 0: # Constants not defined yet.
		&lt;&lt; Create the File menu &gt;&gt;
		&lt;&lt; Create the Edit menu &gt;&gt;
		&lt;&lt; Create the Outline menu &gt;&gt;
		&lt;&lt; Create the Window menu &gt;&gt;
	&lt;&lt; Create the Help menu &gt;&gt;
	if 0:
		menuBar.Append(fileMenu, "&amp;File")
		menuBar.Append(editMenu, "&amp;Edit")
		menuBar.Append(outlineMenu, "&amp;Outline")
		menuBar.Append(windowMenu, "&amp;Window")
		
	menuBar.Append(helpMenu, "&amp;Help")
	self.SetMenuBar(menuBar)  # attach the menu bar to the frame</t>
<t tx="T598">fileMenu = wx.wxMenu()
&lt;&lt; Create the initial items of the file menu &gt;&gt;
&lt;&lt; Create the Read/Write submenu &gt;&gt;
&lt;&lt; Create the Tangle submenu &gt;&gt;
&lt;&lt; Create the Untangle submenu &gt;&gt;
&lt;&lt; Create the Import Files submenu &gt;&gt;

fileMenu.AppendSeparator()

fileMenu.Append(cQuitMenuItem, "E&amp;xit\tCtrl-Q", "Quit Leo")</t>
<t tx="T599">fileMenu.Append ( cNewMenuItem, "&amp;New\tCtrl-N",
	"Open new Leo window" )
fileMenu.Append ( cOpenMenuItem,
	"&amp;Open\tCtrl-O", "Open Leo file")

fileMenu.AppendSeparator()

fileMenu.Append ( cCloseMenuItem,
	"&amp;Close\tCtrl-W", "Close window" )
fileMenu.Append ( cSaveMenuItem,
	"&amp;Save\tCtrl-S", "Save window" )
fileMenu.Append ( cSaveAsMenuItem,
	"Save &amp;As\tShift-Ctrl-S", "Save window as" )
fileMenu.Append ( cSaveToMenuItem,
	"Save &amp;To", "Save window to" )
fileMenu.Append ( cRevertMenuItem,
	"&amp;Revert", "Revert window to saved" )

fileMenu.AppendSeparator()

fileMenu.Append ( cPageSetupMenuItem,
	"Page S&amp;etup\tShift-Ctrl-P", "Specify printer settings" )
fileMenu.Append ( cPrintMenuItem,
	"&amp;Print\tCtrl-P", "Print (Weave) window" )

# Disabled unused items
fileMenu.Enable(cPrintMenuItem, FALSE)
fileMenu.Enable(cPageSetupMenuItem, FALSE)

fileMenu.AppendSeparator()</t>
<t tx="T600">readWriteMenu = wx.wxMenu()

readWriteMenu.Append (cReadOutlineOnlyMenuItem,
	"Read Outline Only", "Read outline only")
readWriteMenu.Append (cReadAtFileNodesMenuItem,
	"Read @file Nodes", "Read @file nodes")
readWriteMenu.Append (cWriteOutlineOnlyMenuItem,
	"Write Outline Only", "Write outline only")
readWriteMenu.Append (cWriteAtFileNodesMenuItem,
	"Write @file Nodes", "Write @file nodes")

fileMenu.Append(cReadWriteSubmenuItem, "Read/Write...", readWriteMenu, "")</t>
<t tx="T601">tangleMenu = wx.wxMenu()

tangleMenu.Append (cTangleAllMenuItem,
	"Tangle &amp;All\tShift-Ctrl-A", "Tangle all roots")
tangleMenu.Append (cTangleMarkedMenuItem,
	"Tangle &amp;Marked\tShift-Ctrl-M", "Tangle all marked roots")
tangleMenu.Append (cTangleMenuItem,
	"&amp;Tangle\tShift-Ctrl-T", "Tangle selected headline")

fileMenu.Append(cTangleSubmenuItem, "&amp;Tangle...", tangleMenu, "")

# Doesn't work either.
fileMenu.SetHelpString(cTangleSubmenuItem, "Tangle commands...")</t>
<t tx="T602">untangleMenu = wx.wxMenu()

untangleMenu.Append (cUntangleAllMenuItem,
	"Untangle &amp;All", "Tangle all roots")
untangleMenu.Append (cUntangleMarkedMenuItem,
	"Untangle &amp;Marked", "Tangle all marked roots")
untangleMenu.Append (cUntangleMenuItem,
	"&amp;Untangle\tShift-Ctrl-U", "Tangle selected headline")

fileMenu.Append(cUntangleSubmenuItem, "&amp;Untangle...", untangleMenu, "")</t>
<t tx="T603">importMenu = wx.wxMenu()

importMenu.Append (cImportFilesMenuItem,
	"Import Files\tShift-Ctrl-F", "Convert source files to outline" )
importMenu.Append (cImportCWEBFilesMenuItem,
	"Import CWEB Files", "Convert CWEB file to outline")
importMenu.Append (cImportNowebFilesMenuItem,
	"Import noweb Files", "Convert noweb file to outline")

importMenu.Enable(cImportNowebFilesMenuItem, FALSE)

importMenu.Append (cImportMORETextMenuItem,
	"Import MORE Text", "Convert MORE file to outline")
importMenu.Append (cFlattenOutlineMenuItem,
	"Flatten Outline", "Write Leo outline to text file")

fileMenu.Append(cImportExportSubmenuItem,
	"&amp;Import Files...", importMenu, "Import commands")</t>
<t tx="T604">editMenu = wx.wxMenu()
&lt;&lt; Create the initial items of the Edit menu &gt;&gt;
&lt;&lt; Create the Edit Body submenu &gt;&gt;
&lt;&lt; Create the Find submenu &gt;&gt;
&lt;&lt; Create the final items of the Edit menu &gt;&gt;</t>
<t tx="T605">editMenu.Append ( cUndoMenuItem, "&amp;Undo\tCtrl-Z", "Undo last operation" )

if 0: #ifndef __WXGTK__ # For now, neither tree nor text controls support Redo.
	editMenu.Append ( cRedoMenuItem,
		"&amp;Redo\tShift-Ctrl-Z", "Redo previous operation" )

editMenu.AppendSeparator()

editMenu.Append ( cCutMenuItem,
	"Cu&amp;t\tCtrl-X", "Cut text" )
editMenu.Append ( cCopyMenuItem,
	"&amp;Copy\tCtrl-C", "Copy text" )
editMenu.Append ( cPasteMenuItem,
	"&amp;Paste\tCtrl-V", "Paste text" )
editMenu.Append ( cDeleteMenuItem,
	"&amp;Delete", "Delete text" )
editMenu.Append ( cSelectAllMenuItem,
	"Select A&amp;ll\tCtrl-A", "Select all" )

editMenu.AppendSeparator()

editMenu.Append ( cEditHeadlineMenuItem,
	"Edit &amp;Headline\tShift-Ctrl-H", "Edit headline text" )</t>
<t tx="T606">findMenu = wx.wxMenu()

findMenu.Append ( cFindPanelMenuItem,
	"&amp;Find Panel\tCtrl-F", "Open Find panel" )

findMenu.AppendSeparator()

if 0: #ifdef __WXGTK__  # bugs: can't recognize shift-F keys
	findMenu.Append ( cFindNextMenuItem,
		"Find &amp;Next\tF3", "Find next" )
	findMenu.Append ( cFindPreviousMenuItem,
		"Find &amp;Prev\tF4", "Find previous" )
	findMenu.Append ( cReplaceMenuItem,
		"&amp;Replace\tF5", "Replace" )
	findMenu.Append ( cReplaceThenFindMenuItem,
		"Replace &amp;Then Find\tF6", "Replace, then find again" )
else:
	findMenu.Append ( cFindNextMenuItem,
		"Find &amp;Next\tF3", "Find next" )
	findMenu.Append ( cFindPreviousMenuItem,
		"Find &amp;Prev\tShift-F3", "Find previous" )
	findMenu.Append ( cReplaceMenuItem,
		"&amp;Replace\tF4", "Replace" )
	findMenu.Append ( cReplaceThenFindMenuItem,
		"Replace &amp;Then Find\tShift-F4", "Replace, then find again" )

editMenu.Append( cFindSubmenuItem,
	"&amp;Find...", findMenu, "")</t>
<t tx="T607">editMenu.Append ( cFontPanelMenuItem,
	"&amp;Font Panel\tAlt-Shift-T", "Open Font panel" )

editMenu.Append ( cSyntaxColoringMenuItem,
	"&amp;Syntax Coloring...\tAlt-Shift-S", "Set syntax coloring options" )

editMenu.Enable(cSyntaxColoringMenuItem, FALSE)

editMenu.AppendSeparator()

editMenu.Append ( cPreferencesMenuItem,
	"Preferences\tCtrl-Y", "Open Preferences panel" )</t>
<t tx="T608">editBodyMenu = wx.wxMenu()

editBodyMenu.Append ( cExtractSectionMenuItem,
	"&amp;Extract Section\tShift-Ctrl-E",
	"Extract section to child" )
editBodyMenu.Append ( cExtractNamesMenuItem,
	"Extract Section &amp;Names\tShift-Ctrl-N",
	"Extract section names to children" )
editBodyMenu.Append ( cExtractMenuItem,
	"Extract\tShift-Ctrl-D",
	"Extract section text to child" )
editBodyMenu.Append ( cConvertBlanksMenuItem,
	"&amp;Convert Blanks\tShift-Ctrl-B", "Convert blanks" )

editMenu.Append(cEditBodySubmenuItem, "&amp;Edit Body...", editBodyMenu, "")</t>
<t tx="T609">outlineMenu = wx.wxMenu()
&lt;&lt; Create the initial items of the Outline menu &gt;&gt;
&lt;&lt; Create the Expand/Contract submenu &gt;&gt;
&lt;&lt; Create the Move/Select submenu &gt;&gt;
&lt;&lt; Create the Mark/Go To submenu &gt;&gt;
</t>
<t tx="T610">outlineMenu.Append ( cCutNodeMenuItem,
	"Cu&amp;t Node\tShift-Ctrl-X", "Cut node")
outlineMenu.Append ( cCopyNodeMenuItem,
	"&amp;Copy Node\tShift-Ctrl-C", "Copy node" )
outlineMenu.Append ( cPasteNodeMenuItem,
	"&amp;Paste Node\tShift-Ctrl-V", "Paste node" )
outlineMenu.Append ( cDeleteNodeMenuItem,
	# Shift-Ctrl-BkSp not validcPreferencesMenuItem
	"&amp;Delete Node", "Delete node" )

outlineMenu.AppendSeparator()

outlineMenu.Append ( cInsertNodeMenuItem,
	"&amp;Insert Node\tCtrl-I", "Insert new node" )

outlineMenu.Append ( cCloneNodeMenuItem,
	"&amp;Clone Node\tShift-Ctrl-I", "Clone node" )

outlineMenu.Append ( cSortNodeMenuItem,
	"&amp;Sort Node", "Sort node's childdren" )

outlineMenu.AppendSeparator()</t>
<t tx="T611">expandContractMenu = wx.wxMenu()

expandContractMenu.Append ( cExpandAllChildrenMenuItem,
	"Expand All Children", "Expand node fully" )
expandContractMenu.Append ( cExpandChilrenMenuItem,
	"Expand Children", "Expand node" )

expandContractMenu.AppendSeparator()

expandContractMenu.Append ( cContractAllChildrenMenuItem,
	"Contract All Children", "Contract node fully" )
expandContractMenu.Append ( cContractChilrenMenuItem,
	"Contract Children", "Contract node" )

expandContractMenu.AppendSeparator()

expandContractMenu.Append ( cExpandNextLevelMenuItem,
	"Expand &amp;Next Level\tAlt-N", "Expand outline another level" )
expandContractMenu.Append ( cExpandToLevel1MenuItem,  # better than contract all
	"Contract All\tAlt-1", "Contract all" )
expandContractMenu.Append ( cExpandToLevel2MenuItem,
	"Expand To Level 2\tAlt-2", "Expand to level 2" )
expandContractMenu.Append ( cExpandToLevel3MenuItem,
	"Expand To Level 3\tAlt-3", "Expand to level 3" )
expandContractMenu.Append ( cExpandToLevel4MenuItem,
	"Expand To Level 4\tAlt-4", "Expand to level 4" )
expandContractMenu.Append ( cExpandToLevel5MenuItem,
	"Expand To Level 5\tAlt-5", "Expand to level 5" )
expandContractMenu.Append ( cExpandToLevel6MenuItem,
	"Expand To Level 6\tAlt-6", "Expand to level 6" )
expandContractMenu.Append ( cExpandToLevel7MenuItem,
	"Expand To Level 7\tAlt-7", "Expand to level 7" )
expandContractMenu.Append ( cExpandToLevel8MenuItem,
	"Expand To Level 8\tAlt-8", "Expand to level 8" )
expandContractMenu.Append ( cExpandAllMenuItem,
	"Expand All\tAlt-9", "Expand all" )

outlineMenu.Append(cExpandContractSubmenuItem,
	"Expand/Contract...", expandContractMenu, "")</t>
<t tx="T612">moveSelectMenu = wx.wxMenu()

moveSelectMenu.Append ( cMoveDownMenuItem,
	"Move &amp;Down\tCtrl-D", "Move node down" )
moveSelectMenu.Append ( cMoveLeftMenuItem,
	"Move &amp;Left\tCtrl-L", "Move node left" )
moveSelectMenu.Append ( cMoveRightMenuItem,
	"Move &amp;Right\tCtrl-R", "Move node right" )
moveSelectMenu.Append ( cMoveUpMenuItem,
	"Move &amp;Up\tCtrl-U", "Move node up" )

moveSelectMenu.AppendSeparator()

# Can't use control-] and control-[ anywhere.
moveSelectMenu.Append ( cPromoteMenuItem,
	"&amp;Promote", "Promote children" )

moveSelectMenu.Append ( cDemoteMenuItem,
	"&amp;Demote", "Demote following siblings" )

moveSelectMenu.AppendSeparator()

if 1: #ifdef __WXMSW__  # Up and down keys handled by tree &amp; text control
	moveSelectMenu.Append ( cGoPrevVisibleMenuItem,
		"Go Prev Visible\tUp", "Select previous visible node" )
	moveSelectMenu.Append ( cGoNextVisibleMenuItem,
		"Go Next Visible\tDown", "Select next visible node" )
else:
 	moveSelectMenu.Append ( cGoPrevVisibleMenuItem,
		"Go Prev Visible", "Select previous visible node" )
	moveSelectMenu.Append ( cGoNextVisibleMenuItem,
		"Go Next Visible", "Select next visible node" )

moveSelectMenu.AppendSeparator()

moveSelectMenu.Append ( cGoBackMenuItem,
	"Go Prev", "Select previous node" )
moveSelectMenu.Append ( cGoNextMenuItem,
	"Go Next", "Select next node" )

outlineMenu.Append(cMoveSelectSubmenuItem,
	"Move/&amp;Select...", moveSelectMenu, "")</t>
<t tx="T613">markGoToMenu = wx.wxMenu()

markGoToMenu.Append ( cMarkMenuItem,
	"&amp;Mark\tCtrl-M", "Mark node" )
markGoToMenu.Append ( cMarkSubheadsMenuItem,
	"Mark &amp;Subheads\tAlt-S", "Mark children of node" )
markGoToMenu.Append ( cMarkChangedItemsMenuItem,
	"Mark &amp;Changed Items\tAlt-C", "Mark all changed nodes" )
markGoToMenu.Append ( cMarkChangedRootsMenuItem,
	"Mark Changed &amp;Roots\tAlt-R", "Mark all changed root nodes" )
markGoToMenu.Append ( cMarkAllAtFileNodesDirtyMenuItem,
	"Mark All @file Nodes Dirty", "Mark all @file nodes" )
markGoToMenu.Append ( cMarkAtFileNodesDirtyMenuItem,
	"Mark @file Nodes Dirty", "Mark @file nodes" )

markGoToMenu.AppendSeparator()

markGoToMenu.Append ( cUnmarkAllMenuItem,
	"&amp;Unmark All\tAlt-U", "Unmark all nodes" )
markGoToMenu.Append ( cGoToNextMarkedMenuItem,
	"&amp;Go To Next Marked\tAlt-M", "Select next marked node" )
markGoToMenu.Append ( cGoToNextChangedMenuItem,
	"Go To Next Changed\tAlt-D", "Select next changed node" )

outlineMenu.Append(cMarkGotoSubmenuItem,
	"&amp;Mark/Go To...", markGoToMenu, "")</t>
<t tx="T614">windowMenu = wx.wxMenu()

if 0: #ifdef __WXGTK__  # Control-E conflicts with shift-control-E

	windowMenu.Append ( cEqualSizedPanesMenuItem,
		"&amp;Equal Sized Panes", "Make each pane the same size")
else:
	windowMenu.Append ( cEqualSizedPanesMenuItem,
		"&amp;Equal Sized Panes\tCtrl-E", "Make each pane the same size")

windowMenu.Append ( cToggleActivePaneMenuItem,
	"&amp;Toggle Active Pane\tCtrl-T", "Switch the active pane")

if 0: #ifdef __WXGTK__
	windowMenu.Enable(cToggleActivePaneMenuItem, FALSE)

windowMenu.Append ( cSplitPaneDirectionMenuItem,
	"&amp;Split Pane Vertically", "Change orientation of pane")

windowMenu.AppendSeparator()

windowMenu.Append ( cCascadeMenuItem,
	"&amp;Cascade Windows", "Cascade all open windows")

windowMenu.Append ( cMinimizeAllMenuItem,
	"Minimize &amp;All Windows", "Minimize all open windows")

windowMenu.AppendSeparator()

if 1: #ifdef __WXMSW__
	windowMenu.Append ( cOpenPythonWindowMenuItem,
		"Open &amp;Python Window\tAlt-P", "Open the Python window")

if 0: # Not ready yet: use wxFileHistory
	windowMenu.AppendSeparator()

	windowMenu.Append ( cRecentWindowsMenuItem,
		"Recent Windows", "List of recent windows")</t>
<t tx="T615">helpMenu = wx.wxMenu()

helpMenu.Append(cAboutLeoMenuItem,
	"&amp;About Leo...",
	"Show about dialog")</t>
<t tx="T616">def createMenuBar(self):
	
	menuBar = wx.wxMenuBar()
	
	self.menuShortcuts = []
	if 0: # not ready yet: methods in tables must be defined
		&lt;&lt; create the file menu &gt;&gt;
		&lt;&lt; create the edit menu &gt;&gt;
		&lt;&lt; create the outline menu &gt;&gt;
		doHook("create-optional-menus",c=c)
		&lt;&lt; create the window menu &gt;&gt;
	&lt;&lt; create the help menu &gt;&gt;

	if 0:
		menuBar.Append(fileMenu, "&amp;File")
		menuBar.Append(editMenu, "&amp;Edit")
		menuBar.Append(outlineMenu, "&amp;Outline")
		menuBar.Append(windowMenu, "&amp;Window")
		
	menuBar.Append(helpMenu, "&amp;Help")
	self.SetMenuBar(menuBar)  # attach the menu bar to the frame
	
	# app().menuWarningsGiven = true</t>
<t tx="T617">editMenu = self.createNewMenu("&amp;Edit")
&lt;&lt; create the first top-level edit entries &gt;&gt;
&lt;&lt; create the edit body submenu &gt;&gt;
&lt;&lt; create the edit headline submenu &gt;&gt;
&lt;&lt; create the find submenu &gt;&gt;
&lt;&lt; create the last top-level edit entries &gt;&gt;
</t>
<t tx="T618">table = (
	("Can't Undo","Ctrl+Z",self.OnUndo), # &amp;U reserved for Undo
	("Can't Redo","Shift+Ctrl+Z",self.OnRedo), # &amp;R reserved for Redo
	("-",None,None),
	("Cu&amp;t","Ctrl+X",self.OnCutFromMenu), 
	("Cop&amp;y","Ctrl+C",self.OnCopyFromMenu),
	("&amp;Paste","Ctrl+V",self.OnPasteFromMenu),
	("&amp;Delete",None,self.OnDelete),
	("Select &amp;All","Ctrl+A",self.OnSelectAll),
	("-",None,None))

self.createMenuEntries(editMenu,table)
</t>
<t tx="T619">editBodyMenu = self.createNewMenu("Edit &amp;Body...","Edit")

table = (
	("Extract &amp;Section","Shift+Ctrl+E",self.OnExtractSection),
	("Extract &amp;Names","Shift+Ctrl+N",self.OnExtractNames),
	("&amp;Extract","Shift+Ctrl+D",self.OnExtract),
	("-",None,None),
	("Convert All B&amp;lanks",None,self.OnConvertAllBlanks),
	("Convert All T&amp;abs",None,self.OnConvertAllTabs),
	("Convert &amp;Blanks","Shift+Ctrl+B",self.OnConvertBlanks),
	("Convert &amp;Tabs","Shift+Ctrl+J",self.OnConvertTabs),
	("Insert Body Time/&amp;Date","Shift+Ctrl+G",self.OnInsertBodyTime),
	("&amp;Reformat Paragraph","Shift+Ctrl+P",self.OnReformatParagraph),
	("-",None,None),
	("&amp;Indent","Ctrl+]",self.OnIndent),
	("&amp;Unindent","Ctrl+[",self.OnDedent),
	("&amp;Match Brackets","Ctrl+K",self.OnFindMatchingBracket))
	
self.createMenuEntries(editBodyMenu,table)

</t>
<t tx="T620">editHeadlineMenu = self.createNewMenu("Edit &amp;Headline...","Edit")

table = (
	("Edit &amp;Headline","Ctrl+H",self.OnEditHeadline),
	("&amp;End Edit Headline","Escape",self.OnEndEditHeadline),
	("&amp;Abort Edit Headline","Shift-Escape",self.OnAbortEditHeadline),
	("Insert Headline Time/&amp;Date","Shift+Ctrl+H",self.OnInsertHeadlineTime))
	
	# 5/16/03 EKR: I dislike this command.
	#("Toggle Angle Brackets","Ctrl+B",self.OnToggleAngleBrackets)
	
self.createMenuEntries(editHeadlineMenu,table)

</t>
<t tx="T621">findMenu = self.createNewMenu("&amp;Find...","Edit")

table = (
	("&amp;Find Panel","Ctrl+F",self.OnFindPanel),
	("-",None,None),
	("Find &amp;Next","F3",self.OnFindNext),
	("Find &amp;Previous","F4",self.OnFindPrevious),
	("&amp;Replace","Ctrl+=",self.OnReplace),
	("Replace, &amp;Then Find","Ctrl+-",self.OnReplaceThenFind))

self.createMenuEntries(findMenu,table)
</t>
<t tx="T622">label = choose(c.tree.colorizer.showInvisibles,"Hide In&amp;visibles","Show In&amp;visibles")

table = (
	("&amp;Go To Line Number","Alt+G",self.OnGoToLineNumber),
	("&amp;Execute Script","Alt+Shift+E",self.OnExecuteScript),
	("Set Fon&amp;t...","Shift+Alt+T",self.OnFontPanel),
	("Set &amp;Colors...","Shift+Alt+C",self.OnColorPanel),
	(label,"Alt+V",self.OnViewAllCharacters),
	("-",None,None),
	("Prefere&amp;nces","Ctrl+Y",self.OnPreferences))

self.createMenuEntries(editMenu,table)</t>
<t tx="T623">fileMenu = self.createNewMenu("&amp;File")
&lt;&lt; create the top-level file entries &gt;&gt;
&lt;&lt; create the recent files submenu &gt;&gt;
fileMenu.add_separator()
&lt;&lt; create the read/write submenu &gt;&gt;
&lt;&lt; create the tangle submenu &gt;&gt;
&lt;&lt; create the untangle submenu &gt;&gt;
&lt;&lt; create the import submenu &gt;&gt;
&lt;&lt; create the export submenu &gt;&gt;
fileMenu.add_separator()
# Create the last entries.
exitTable = (("E&amp;xit","Ctrl-Q",self.OnQuit),)
self.createMenuEntries(fileMenu,exitTable)

</t>
<t tx="T624">@ leo.py will probably never have a Print command.  Instead, export text files that may be formatted and printed as desired.
@c

table = (
	("&amp;New","Ctrl+N",self.OnNew),
	("&amp;Open...","Ctrl+O",self.OnOpen))
self.createMenuEntries(fileMenu,table)

# 7/1/03: Create a new menu rather than call OnOpenWith.
self.createNewMenu("Open &amp;With...","File")

table = (
	("-",None,None),
	("&amp;Close","Ctrl+W",self.OnClose),
	("&amp;Save","Ctrl+S",self.OnSave),
	("Save &amp;As","Shift+Ctrl+S",self.OnSaveAs),
	("Save To",None,self.OnSaveTo), # &amp;Tangle
	("Re&amp;vert To Saved",None,self.OnRevert)) # &amp;Read/Write
self.createMenuEntries(fileMenu,table)</t>
<t tx="T625">recentFilesMenu = self.createNewMenu("Recent &amp;Files...","File")
self.recentFiles = app().config.getRecentFiles()
self.createRecentFilesMenuItems()

</t>
<t tx="T626">readWriteMenu = self.createNewMenu("&amp;Read/Write...","File")

table = [
		("&amp;Read Outline Only","Shift+Ctrl+R",self.OnReadOutlineOnly),
		("Read @file &amp;Nodes",None,self.OnReadAtFileNodes),
		("-",None,None),
		("Write &amp;Dirty @file Nodes","Shift+Ctrl+Q",self.OnWriteDirtyAtFileNodes),
		("Write &amp;Missing @file Nodes",None,self.OnWriteMissingAtFileNodes),
		("Write &amp;Outline Only",None,self.OnWriteOutlineOnly),
		("&amp;Write @file Nodes","Shift+Ctrl+W",self.OnWriteAtFileNodes)]

self.createMenuEntries(readWriteMenu,table)</t>
<t tx="T627">tangleMenu = self.createNewMenu("&amp;Tangle...","File")

table = (
	("Tangle &amp;All","Shift+Ctrl+A",self.OnTangleAll),
	("Tangle &amp;Marked","Shift+Ctrl+M",self.OnTangleMarked),
	("&amp;Tangle","Shift+Ctrl+T",self.OnTangle))

self.createMenuEntries(tangleMenu,table)

</t>
<t tx="T628">untangleMenu = self.createNewMenu("&amp;Untangle...","File")

table = (
	("Untangle &amp;All",None,self.OnUntangleAll),
	("Untangle &amp;Marked",None,self.OnUntangleMarked),
	("&amp;Untangle","Shift+Ctrl+U",self.OnUntangle))
	
self.createMenuEntries(untangleMenu,table)

</t>
<t tx="T629">importMenu = self.createNewMenu("&amp;Import...","File")

table = (
	("Import To @&amp;file","Shift+Ctrl+F",self.OnImportAtFile),
	("Import To @&amp;root",None,self.OnImportAtRoot),
	("Import &amp;CWEB Files",None,self.OnImportCWEBFiles),
	("Import &amp;noweb Files",None,self.OnImportNowebFiles),
	("Import Flattened &amp;Outline",None,self.OnImportFlattenedOutline))

self.createMenuEntries(importMenu,table)

</t>
<t tx="T630">exportMenu = self.createNewMenu("&amp;Export...","File")

table = [
	("Export &amp;Headlines",None,self.OnExportHeadlines),
	("Outline To &amp;CWEB",None,self.OnOutlineToCWEB),
	("Outline To &amp;Noweb",None,self.OnOutlineToNoweb),
	("&amp;Flatten Outline",None,self.OnFlattenOutline),
	("&amp;Remove Sentinels",None,self.OnRemoveSentinels),
	("&amp;Weave",None,self.OnWeave)]

self.createMenuEntries(exportMenu,table)
</t>
<t tx="T631">outlineMenu = self.createNewMenu("&amp;Outline")
&lt;&lt; create top-level outline menu &gt;&gt;
&lt;&lt; create expand/contract submenu &gt;&gt;
&lt;&lt; create move submenu &gt;&gt;
&lt;&lt; create mark submenu &gt;&gt;
&lt;&lt; create goto submenu &gt;&gt;</t>
<t tx="T632">table = (
	("C&amp;ut Node","Shift+Ctrl+X",self.OnCutNode),
	("C&amp;opy Node","Shift+Ctrl+C",self.OnCopyNode),
	("&amp;Paste Node","Shift+Ctrl+V",self.OnPasteNode),
	("&amp;Delete Node","Shift+Ctrl+BkSp",self.OnDeleteNode),
	("-",None,None),
	("&amp;Insert Node","Ctrl+I",self.OnInsertNode),
	("&amp;Clone Node","Ctrl+`",self.OnCloneNode),
	("Sort C&amp;hildren",None,self.OnSortChildren),
	("&amp;Sort Siblings","Alt-A",self.OnSortSiblings),
	("-",None,None))

self.createMenuEntries(outlineMenu,table)</t>
<t tx="T633">expandMenu = self.createNewMenu("&amp;Expand/Contract...","Outline")

table = (
	("&amp;Contract All","Alt+-",self.OnContractAll),
	("Contract &amp;Node","Alt+[",self.OnContractNode),
	("Contract &amp;Parent","Alt+0",self.OnContractParent),
	("-",None,None),
	("Expand P&amp;rev Level","Alt+.",self.OnExpandPrevLevel),
	("Expand N&amp;ext Level","Alt+=",self.OnExpandNextLevel),
	("-",None,None),
	("Expand To Level &amp;1","Alt+1",self.OnExpandToLevel1),
	("Expand To Level &amp;2","Alt+2",self.OnExpandToLevel2),
	("Expand To Level &amp;3","Alt+3",self.OnExpandToLevel3),
	("Expand To Level &amp;4","Alt+4",self.OnExpandToLevel4),
	("Expand To Level &amp;5","Alt+5",self.OnExpandToLevel5),
	("Expand To Level &amp;6","Alt+6",self.OnExpandToLevel6),
	("Expand To Level &amp;7","Alt+7",self.OnExpandToLevel7),
	("Expand To Level &amp;8","Alt+8",self.OnExpandToLevel8),
	# ("Expand To Level &amp;9","Alt+9",self.OnExpandToLevel9),
	("-",None,None),
	("Expand &amp;All","Alt+9",self.OnExpandAll),
	("Expand N&amp;ode","Alt+]",self.OnExpandNode))


self.createMenuEntries(expandMenu,table)</t>
<t tx="T634">moveSelectMenu = self.createNewMenu("&amp;Move...","Outline")

table = (
	("Move &amp;Down", "Ctrl+D",self.OnMoveDown),
	("Move &amp;Left", "Ctrl+L",self.OnMoveLeft),
	("Move &amp;Right","Ctrl+R",self.OnMoveRight),
	("Move &amp;Up",   "Ctrl+U",self.OnMoveUp),
	("-",None,None),
	("&amp;Promote","Ctrl+{",self.OnPromote),
	("&amp;Demote", "Ctrl+}",self.OnDemote))
	
self.createMenuEntries(moveSelectMenu,table)
</t>
<t tx="T635">markMenu = self.createNewMenu("M&amp;ark/Unmark...","Outline")

table = (
	("&amp;Mark","Ctrl-M",self.OnMark),
	("Mark &amp;Subheads","Alt+S",self.OnMarkSubheads),
	("Mark Changed &amp;Items","Alt+C",self.OnMarkChangedItems),
	("Mark Changed &amp;Roots","Alt+R",self.OnMarkChangedRoots),
	("Mark &amp;Clones","Alt+K",self.OnMarkClones),
	("&amp;Unmark All","Alt+U",self.OnUnmarkAll))
	
self.createMenuEntries(markMenu,table)
</t>
<t tx="T636">gotoMenu = self.createNewMenu("&amp;Go To...","Outline")

table = (
	("Go Back",None,self.OnGoPrevVisitedNode), # Usually use buttons for this.
	("Go Forward",None,self.OnGoNextVisitedNode),
	("-",None,None),
	("Go To Next &amp;Marked","Alt+M",self.OnGoToNextMarked),
	("Go To Next C&amp;hanged","Alt+D",self.OnGoToNextChanged),
	("Go To Next &amp;Clone","Alt+N",self.OnGoToNextClone),
	("-",None,None),
	("Go To &amp;First Node","Alt+Shift+G",self.OnGoToFirstNode),
	("Go To &amp;Last Node","Alt+Shift+H",self.OnGoToLastNode),
	("Go To &amp;Parent","Alt+Shift+P",self.OnGoToParent),
	("Go To P&amp;rev Sibling","Alt+Shift+R",self.OnGoToPrevSibling),
	("Go To Next &amp;Sibling","Alt+Shift+S",self.OnGoToNextSibling),
	("-",None,None),
	("Go To Prev V&amp;isible","Alt-UpArrow",self.OnGoPrevVisible),
	("Go To Next &amp;Visible","Alt-DnArrow",self.OnGoNextVisible),
	("Go To Prev Node","Alt-Shift+UpArrow",self.OnGoBack),
	("Go To Next Node","Alt-Shift-DnArrow",self.OnGoNext))
	
self.createMenuEntries(gotoMenu,table)
</t>
<t tx="T637">windowMenu = self.createNewMenu("&amp;Window")

table = (
	("&amp;Equal Sized Panes","Ctrl-E",self.OnEqualSizedPanes),
	("Toggle &amp;Active Pane","Ctrl-T",self.OnToggleActivePane),
	("Toggle &amp;Split Direction",None,self.OnToggleSplitDirection),
	("-",None,None),
	("Casca&amp;de",None,self.OnCascade),
	("&amp;Minimize All",None,self.OnMinimizeAll),
	("-",None,None),
	("Open &amp;Compare Window",None,self.OnOpenCompareWindow),
	("Open &amp;Python Window","Alt+P",self.OnOpenPythonWindow))

self.createMenuEntries(windowMenu,table)
</t>
<t tx="T638">helpMenu = self.createNewMenu("&amp;Help")

table = (
	("&amp;About Leo...",None,self.OnAbout),)
	#("Online &amp;Home Page",None,self.OnLeoHome),
	#("-",None,None),
	#("Open Online &amp;Tutorial",None,self.OnLeoTutorial))

self.createMenuEntries(helpMenu,table)

if 0: # not ready yet.

	if sys.platform=="win32":
		table = (("Open &amp;Offline Tutorial",None,self.OnLeoHelp),)
		self.createMenuEntries(helpMenu,table)
	
	table = (
		("Open Leo&amp;Docs.leo",None,self.OnLeoDocumentation),
		("-",None,None),
		("Open Leo&amp;Config.leo",None,self.OnLeoConfig),
		("Apply &amp;Settings",None,self.OnApplyConfig))

	self.createMenuEntries(helpMenu,table)</t>
<t tx="T639">def createNewMenu(self,name):
	
	return wx.wxMenu()</t>
<t tx="T640">@ The old, non-user-configurable code bound shortcuts in createMenuBar.  The new user-configurable code binds shortcuts here.

Centralized tables of shortscuts no longer exist as they did in createAccelerators.  To check for duplicates, (possibly arising from leoConfig.txt) we add entries to a central dictionary here, and report duplicates if an entry for a canonicalized shortcut already exists.
@c

def createMenuEntries (self,menu,table,openWith=0):
	
	for label,accel,command in table:
		id = const(label)
		menu.Append(id,label,label)
		
		if 1:
			wx.EVT_MENU(self,id,command)

		else: # Doesn't help: methods must be defined in the table.
			def generalCommand(event=None,label=label):
				print "generalCommand",label # ,event
			wx.EVT_MENU(self,id,generalCommand)</t>
<t tx="T641">def OnAbout (self,event=None):
	
	print "OnAbout" # ,event</t>
<t tx="T642">const_dict = {}
const_lastVal = 100
	
def const(name):
	
	"""Return the wx id associated with name"""
	
	# Should this canonicalize the label?  Just remove '&amp;' ??
	
	id = const_dict.get(name)
	if id != None:
		return id
	else:
		global const_lastVal
		const_lastVal += 1
		return const_lastVal</t>
<t tx="T643"></t>
<t tx="T644">@nocolor

- Test handling of block comments.
- handle @ws properly.
- Handle @first and @last lines.
- Test @delims, @comment sentinels.
- Add ignoreSentinel routine for 3.x sentinels.

- Support for root.tnodeList
	- Write tnodeList attribute in .leo files.
	- Read tnodeList attribute in .leo files.

Eventually:
	- Remove bozo error recovery from _old_ read code.

What I did:
	- Removed @+body and @-body
	- Don't write organizer nodes in @others</t>
<t tx="T645">@nocolor</t>
<t tx="T646">* Must rewrite the read/write code to eliminate blank lines.

	- The write code would like to start all sentinels with newlines.
		But this creates extra blank lines!
	- The read code would like to end all sentinels with newlines.

* The rule that sentinels begin and end with newlines causes too many problems.

* Use @nl directive to clarify what the original outline contained.

	- By default, sentinels only _end_ with newline.
	- @nonl begins _and_ ends with a newline.
	- Use @nl to indicate that @ref appears directly after a newline.
		- typically an @ref directive deletes preceding newline.
	- Use @nl to indicate that node text ends in a newline.
		- typically @-body deletes preceding newline
		
	- Sentinels that start a line cause no problem.
		The newline that preceeds the sentinel is _not_ part of the sentinel.
	- Sentinels that appear in the middle of the line need a preceding nonl sentinel.
		The whitespace that preceeds the nonl sentinel is _not_ deleted.

* Runs of sentinels start only with references or @others.  Any others??</t>
<t tx="T647">Here is a summary of the new derived file format.

- In all cases, the "In" code starts a line.
- [ws] indicates non-empty whitespace.
- [ws*] indicates possibly empty whitespace.
- [in] indicates present whitespace corresponding to self.indent
- [in2] indicates new values of self.indent
- [[in]@nonl] indicates @nonl sentinel if body text doesn't end in NL.
- x,y indicate non-whitespaces.
- sentinels do *not* start with NL in general.
	- @ws and @nonl sentinels allows write logic make sure sentinels start on separate lines.
- except for @ws sentinels, whitespace in sentinel lines is ignored by read logic.

In             Out              Notes

&lt;&lt;ref&gt;&gt;        [in]@ref         Leading ws before sentinels is ignored.
                                NL before sentinels is written to output stream.

[ws]&lt;&lt;ref&gt;&gt;    [in][ws]#@ws     [ws] is *not* ignored	for @ws sentinels.
               [in2]@ref        self.indent changes.

[ws*]x&lt;&lt;ref&gt;&gt;  [in][ws*]x
               [in2]nonl        nonl sentinel deletes previous NL
               [in2]@ref        (assert(out and out[-1]=='\n')

&lt;&lt;ref&gt;&gt;x       [in]@ref
               [in]@+node
               ...
               [[in]@nonl]      (only if body text doesn't end in nl)
               [in]@-node       @-node changes indentation to [in2]
               [in2]@verbatim
               [in2]x           x has no extra indentation.

[ws]&lt;&lt;ref&gt;&gt;x   [in][ws]#@ws
               [in2]@ref
               [in2]@+node
               ...
               [[in2]@nonl]     (only if body text doesn't end in nl)
               [in2]@-node      @-node changes indentation to [in2]
               [in]@verbatim
               [in]x            x has no extra indentation .

[ws*]x&lt;&lt;ref&gt;&gt;  [in][ws*]x
               [in2]nonl        nonl sentinel deletes previous NL
               [in2]@ref        (assert(out and out[-1]=='\n')
               [in2]@+node
               ...
               [[in2]@nonl]    (only if body text doesn't end in nl)
               [in2]@-node      @-node changes indentation to [in2]
               [in]@verbatim
               [in]x            x has no extra indentation.

@others        [in]@+others     no change to self.indent
               ...
               [in]@+others

[ws]@others    [in][ws]#ws
               [in2]@others
               ...
               [in2]@others     restores self.indent
</t>
<t tx="T648"></t>
<t tx="T649">* Converting to 4.0 code without "eating the elephant" in one byte.

* Preserve old 3.x read/write code unchanged.

* Allow minor mods to the sentinel code.

* Improve new read code works:
	- no recursion
	- use helper functions and new ivars.

* All flavors of write code must eventually work properly.

* The code should show diffs if possible</t>
<t tx="T650">1. The .leo file will _always_ contain outline structure, even if @file-thin actually happens.

a) Therefore, the hidden machinery is just a list of vnode indices.

b) The read code will create a dictionary associating vnodes with indices.

c) The read call will call findNthWrittenNode instead of createNthChild.

2. The synchronization property (and the hidden machinery) _require_ that node indices in the .leo file match correspond to the order in which nodes are written to derived file.

a) The write code will assign all file indices (to vnodes and tnodes) before writing derived files.

b) The .leo file must become dirty when file indices change.

3. A new attribute (the hidden machinery) is needed for v elements for @file nodes.

	order="list of tnode indices"

4. We want the derived file to contain @+node, @-node, @+others and @-others for best clarity.

5. The write code for sentinels does a good job of removing redundant newlines.  There is probably no good reason to alter this code.

6. The read code probably can be much simplified using look-behind rather than look-ahead.

7. Avoid recursive calls to newScanText.</t>
<t tx="T651">* Test 4.0 code using new testing commands at first.</t>
<t tx="T652">`@nocolor

A suggestion (a UI issue, really): when such a case occurs, namely that a derived
file is modified by a foreign editor (human or otherwise) without creating an
out-of-synch condition, and then re-read by us Leo-savvy users, it would be
very nice if Leo would:

- flag the file as modified and, above all,
- flag (underline, color, diff, whatever) the parts that were modified. This
is not a CVS conflict diff -type-of window, since we're not talking here about
a conflict, it's just a way of helping leonine users to find out what was legally
modified by others.
</t>
<t tx="T653">@nocolor</t>
<t tx="T654"></t>
<t tx="T655"></t>
<t tx="T656">Every node in a .leo file should be "owned" by exactly one file: either the .leo file itself or a single derived file.   It is easy to enforce this property as follows:

- When writing derived files, Leo will check to see that no clone in that derived file is used in any other @file node.  This restriction is similar to the present restrictions on "orphan" and "ignored" nodes.

- When writing .leo files, Leo will distinguish between "owned clones" (clones contained in exactly one derived file) and "unowned clones" (clones contained in no derived files).  Leo will write unowned clones and their subtrees as usual.  Leo _not_ write the subtrees of owned clones.  Instead those owned clones completely depend on the derived file for their existence and meaning.

An unowned clone may have an owned clone in its subtree.  That's not a problem: Leo will simply not write the subtree of owned clones, even if the owned clone appears as a subtree of an unowned clone.

- When reading, Leo will attempt to recreate owned clones from derived files.  To do this, Leo will use links within the .leo file that point at the derived file.  Once again, gnx's should not be used.

It is quite possible that links from owned clones to derived files may be broken.  This is _absolutely essential_ if derived files are to be the smallest unit of meaning.  In other words, we must put "meaning" in a _single_ place to ensure consistency, and if we do that there must _necessarily_ be the possibility that the links to "that place" will be broken.

- Derived files become primary data; .leo files are secondary.  This is true for both @file-thin and @file-thick trees.</t>
<t tx="T657">what if two .leo files "share" the same derived file?  Leo can easily handle this situation as follows.  When Leo reads a derived file, it will simply create a cloned @file node if Leo has already read the file.

For example:

@file f.py
@file x.leo
 ....@file f.py

When Leo handles the @file f.py node in x.leo, Leo will see that it has already read f.py.  Leo will simply create a clone of f.py.  Linking these two trees ensures data consistency.  Note that both clones are owned, and owned by the same derived file.  The code that checks the ownership of cloned nodes will have to take this complication into account.
</t>
<t tx="T658">The overriding requirement for 4.0 is that Leo must preserve the _meaning_, _consistency_ and _intention_ of code in all situations.  I know from experience that this does not happen automatically.  In particular, I am haunted by the ill-fated concept (and implementation) of "backup" .leo files.  Such files did not contain all the information typically found in .leo files.  Backup .leo files were truly dangerous.  It was way too easy to unwittingly revert to previous versions of code using such backup files.

The meaning, consistency and intention of code is not a property of individual nodes; it is a property of all nodes of a group. But which group?  A derived file?  An entire .leo file?  Some other group? 

I am most interested in this question:  what is the "smallest unit of meaning" (SUM) in a .leo file?   I believe there is a way to make derived files the smallest unit of meaning.  This will have important consequences.

P.S.  Cvs treats files as the smallest unit of meaning.  Yes, cvs reports conflicts in parts of files, but ultimately cvs requires humans to resolve conflicts at the file level.  In other words, cvs does the best it can to create accurate diffs, and CVS DOES NOT RELY ON THE ACCURACY OF DIFFS.  Whatever the diffs, in essence cvs relies on humans to keep _files_ consistent.</t>
<t tx="T659">gnx's are a tool in search of a problem to solve.  Individual nodes are not, and never can be, the smallest unit of meaning in a program.  The proof is immediate:  the meaning, consistency and intention of code is a property of _all_ the nodes of some group.  Therefore, gnx's are not _any part_ of a solution to the fundamental problem.

Indeed, I have adopted the following ironical rule of thumb: any solution requiring gnx's is the wrong solution.  I'll state this rule of thumb without any proof or justification except this:  it has turned out to be useful and valid.</t>
<t tx="T660">Without clones, the smallest unit of meaning (SUM) in a .leo file would be a derived file.  Without clones, we could manage projects as usual--we would have to be careful about old copies of code lying around, and that is nothing new.

Clones complicate matters.  The problem is this: clones create copies of code _in the same .leo file_ that may be used in different contexts.  Indeed, in the present implementation clones may be used in arbitrarily many derived files.  What happens if some, but not all, of those clones change in the derived file?  How can Leo know what to do?  In particular, there would be no automatic way for Leo to read .leo files containing such conflicts.

This suggests the following strategy:

1.  Make it the goal of 4.0 to make derived files the "smallest unit of meaning".

2.  Restrict clones (very slightly!) so this goal is possible.

The next several postings show how to do this.</t>
<t tx="T661">At present clones can affect any part of a Leo outline and a .leo file is a mass of interrelated information.  We must disentangle these relationships if we are to make derived files the smallest unit of meaning.  

In mathematical terms, we want a .leo file to be a _disjoint union_ of sets.  In other words, every node of a .leo file must be associated with exactly one _owning file_: either a derived file or the .leo file itself.  The union of these files "covers" all the nodes of the .leo file.  This union is disjoint:  the intersection of any of the files that cover the .leo file is empty.

I hope this picture is clear:  a .leo file becomes a jigsaw puzzle such that _no pieces overlap_.  This is the property we must have if derived files are to be the smallest unit of meaning: we must _never_ have two derived files associated with the same node.</t>
<t tx="T662">In the last posting I suggest that every node in a .leo file should be associated with a single "owning" file: either the .leo file itself or a single derived file.   It is easy to enforce this property as follows:

1. When writing derived files, Leo will check to see that no clone in that derived file is used in any other @file node.  This restriction is similar to the present restrictions on "orphan" and "ignored" nodes.

2.  When writing .leo files, Leo will distinguish between "owned clones" (clones contained in exactly one derived file) and "unowned clones" (clones contained in no derived files).  Leo will write unowned clones and their subtrees as usual.  Leo _not_ write the subtrees of owned clones.  Instead those owned clones completely depend on the derived file for their existence and meaning.

3.  When reading, Leo will attempt to recreate owned clones from derived files.  To do this, Leo will use links within the .leo file that point at the derived file.  Once again, gnx's should not be used.

Notes:

1.  An unowned clone may have an owned cloned in its subtree.  That's not a problem: Leo will simply not write the subtree of owned clones, even if the owned clone appears as a subtree of an unowned clone.

2. The look, feel and operation of Leo's clones will remain almost completely unchanged with these new restrictions.

3.  It is quite possible that links from owned clones to derived files may be broken.  This is _absolutely essential_ if derived files are to be the smallest unit of meaning.  In other words, we must put "meaning" in a _single_ place to ensure consistency, and if we do that there must _necessarily_ be the possibility that the links to "that place" will be broken.

4. Derived files become primary data; .leo files are secondary.  This is true for both @file-thin and @file-thick trees.</t>
<t tx="T663">Let us suppose that every clone in a .leo file is "owned" by exactly one file: either the .leo file itself or exactly one derived file.  The following are the "acid tests" of this scheme:

1.  Is putting nodes in "an attic" completely safe?

The answer is clearly yes.  If the attic is a separate file the cloned nodes in the attic can have _no effect_ on any derived file.  It doesn't matter how "out of date" nodes in the attic get; they aren't shared by any other derived file.  Because we _don't_ use gnx's there can never be improper linking between old and new nodes.

2.  Can @file-thin be made completely safe?

At long last the answer is an unequivocal yes.  Because a .leo file is a disjoint union of separate files, the _temporal_ or _semantic_ relationships between different derived files _does not really matter_.  Sure, one would like to keep all derived files together "in time", and the integrity of the .leo file will not be affected even if that is not so! This is a hugely important result.

3. Can @include x.leo be made completely safe?

Again, the answer is finally yes.  The subsidiary question is: what if two .leo files "share" the same derived file?  Leo can easily handle this situation as follows.  When Leo reads a derived file, it will simply create a cloned @file node if Leo has already read the file.

For example:

@file f.py
@file x.leo
 ....@file f.py

When Leo handles the @file f.py node in x.leo, Leo will see that it has already read f.py.  Leo will simply create a clone of f.py.  Linking these two trees ensures data consistency.  Note that both clones are owned, and owned by the same derived file.  The code that checks the ownership of cloned nodes will have to take this complication into account.

Significantly and ironically, gnx's need not and should not be [used] to implement @include.  In this context it is even _more_ essential that there be the possibility of broken links into derived files.  Indeed, the _last_ things we want are permanent unbreakable links!</t>
<t tx="T664">To summarize the preceding posts:

- Derived files can be made the smallest unit of meaning.
- Derived files are the "primary data" from which Leo recreates outlines when reading .leo files.
- Because derived files contain all primary data, links from owned cloned nodes to derived files might break.

There are a few minor details left to handle:

1.  We don't want to change derived files just because "secondary" data like marks change in the outline.  Therefore, .leo files should contain "mark bits" even for @file-thick nodes.  These bits will be held in new xml elements somewhere in the .leo files.

2. For the same reason w don't want derived files to contain information sufficient to recreate full node order.  We don't need that information at all for @file-thick trees.  For @file-thin trees we shall again resort to adding the information somewhere in the .leo file.

The crucial point is this:  marks and ordering information are inessential (secondary) data, so file no real harm is done if such data becomes inconsistent with the derived file.</t>
<t tx="T665">Now that gnx's are no essential part of the new 4.0 we can consider adding them back for convenience.  The new gnx's would be used to complete the link from an owned clone to a node in a derived file.   In most cases it would suffice to use the filename:headline combination to make this link.  However, it might turn out to be convenient to use a timestame.index scheme similar to the old gnx's.  No need for a "creator" field: we are not requiring that links be absolutely unique.  In any case, the new gnx will be augmented by a virtual pointer from the owned cloned node to a single derived file.

P.S.  The exact details don't matter much now that we aren't asking  the new gnx's to do much.

P.P.S  Many clone links might break when the .leo files and derived files are out of synch.  This really is the same situation as happens now.  Indeed, the announcement that links have been broken will serve as a useful warning that not everything is in synch.  In any event, there is no way to deal with this kind of situation automatically, and no real danger in this situation either.</t>
<t tx="T666">Other
	- Update version number in header.
	- Write marks and order elements.
	- read marks/order elements when reading .leo file.
	- create child uses order elements.
	- use marks elements to mark nodes.
Options
	- Support old,wait,now,thin,fat options when parsing @file nodes.
	- Deprecate @rawfile, @silentfile, @nosentinelfile.
	- Write entire tree only if fat or old option.
New commands
	- Write Pre-4.0 Outline (Dangerous: removes all gnx fields!)
	- Write Fat (Backup) Outline
Later
	- @file x.leo (@include)
</t>
<t tx="T667"></t>
<t tx="T668">@language plain
@comment ; ( )

; Typical...

@+ref
	# text of ref      (on a single line)
@+v gvi
	# text of headline (on a single line)
@+t gti
	body text...       (what about trailing whitespace?)
@-t gti
@-v gvi
@afterref
	text following ref (indented the same as body)
@-ref

@+others
@+v gvi
	# text of headline
@+t gti
	body text... 
@-t gti
@-v gvi
@-others

; General...

@+ref
	# text of ref 
@+v gvi 1
	# text of headline 1
@+v gvi 2
	# text of headline 2
@+v gvi 3
	# text of headline 3
@+t gti
	body text...
@-t gti
@-v gvi 3
@-v gvi 2
@-v gvi 1
@afterref
	text following ref
@-ref

@+others
	# similar nesting of gvi, gti nodes
@-others</t>
<t tx="T669">@nocolor</t>
<t tx="T670"></t>
<t tx="T671">https://sourceforge.net/forum/message.php?msg_id=1803722
By: jmgilligan

What is the intended behavior when foo.leo has a cloned node that appears several
times in a derived (or multiple derived files) and the user edits this file
or files to change two or more instances of the cloned node in different ways.

Example:

@file foo.py
****begin tnode
@others
****end tnode
...definition of procedure a
***begin tnode
def a:
...print "a:", &lt;&lt;bar&gt;&gt;
***end tnode
...&lt;&lt;bar&gt;&gt;
****begin tnode
"bar"
****end tnode

...definition of procedure b
***begin tnode
def b:
...print "b:", &lt;&lt;bar&gt;&gt;
***end tnode
...&lt;&lt;bar&gt;&gt;
****begin tnode
"bar"
****end tnode

...definition of procedure c
***begin tnode
def c:
...print "a:", &lt;&lt;bar&gt;&gt;
***end tnode
...&lt;&lt;bar&gt;&gt;
****begin tnode
"bar"
****end tnode

In the .leo, if I edit &lt;&lt;bar&gt;&gt;, it will change simultaneously in each place,
always in synch. However, suppose I edit foo.py in a text editor and change
foo.py to read:

#@+leo
#@+node:0::@file foo.py
#@+body
#@+others
#@+node:1::definition of a
#@+body
print "a:", 
#@&lt;&lt;bar&gt;&gt;
#@+node:1::&lt;&lt;bar&gt;&gt;
#@+body
"bar"
#@-body
#@-node:1::&lt;&lt;bar&gt;&gt;
#@-body
#@-node:1::definition of a
#@+node:2::definition of b
#@+body
print "b:", 
#@&lt;&lt;bar&gt;&gt;
#@+node:1::&lt;&lt;bar&gt;&gt;
#@+body
"variation b"
#@-body
#@-node:1::&lt;&lt;bar&gt;&gt;
#@-body
#@-node:2::definition of b
#@+node:3::definition of c
#@+body
print "c:", 
#@&lt;&lt;bar&gt;&gt;
#@+node:1::&lt;&lt;bar&gt;&gt;
#@+body
"variation c"
#@-body
#@-node:1::&lt;&lt;bar&gt;&gt;
#@-body
#@-node:3::definition of c
#@-others
#@-body
#@-node:0::@file foo.py
#@-leo

Now what is supposed to happen when leo tries to read foo.py back in? It seems
that there are three possible behaviors:

1) leo reports a conflict that the user needs to resolve.
2) leo breaks the clone: the three nodes become separate vnodes, not clones
of the same one.
3) leo arbitrarily takes one of the tnodes to be the new tnode for all of the
clones. This is currently what happens. It creates something like a race condition,
where the last node in the derived file determines what the final result will
be. In this case, all three tnodes get text "variation c".

This general question of how Leo should deal with conflicts in clone nodes seems
to me that it needs to be addressed, particularly with respect to trying to
avoid cvs conflicts via thick/thin modes.

Note that this can become quite a subtle question because the same node can
be cloned across several different derived files, in which case a serious race
condition may pertain.

At the least, I would like to see leo perform consistency checking on cloned
nodes when it reads a derived file back in and warn the user if cloned nodes
are inconsistent.

Note that the issue also occurs with OpenWith: I can open each instance of a
cloned node as a separate file in the external text editor. Which version is
read back into leo depends on the order in which I save them from the external
editor.
</t>
<t tx="T672">By: jmgilligan ( Jonathan M. Gilligan ) 
 Possible solution   
2003-01-13 20:55  
One possible solution for the conflicting clones problem is to have Leo, when it detects a conflicting clone, generate a text file (perhaps named LeoConflict_NNNN.leo, where NNNN is the gid of the node in question), which contains all the different versions of the node in question, output in leo XML format. 

The vnode would then be marked with a "conflict" flag that would prevent the user from opening it in Leo until the conflict is resolved. See below for how the user resolves the conflict. 

What I have in mind is something similar to the CVS conflict file, where a conflict between two versions is marked 

&lt;&lt;&lt;&lt;&lt;&lt;&lt; 
blah blah blah? 
======= 
blah blah blah! 
&gt;&gt;&gt;&gt;&gt;&gt;&gt; 

Except that we would output this file in Leo XML format. The reason for XML format would be to avoid problems of how to generically delimit the different sections (different versions of the cloned node). Here leo's XML tags can unambiguously delimit the sections. 

The user would then edit the conflict file and delete all but the desired version. Then he would tell leo to resolve the conflict by reading the corrected file in and replacing the contents of the conflicting node with the contents of the LeoConflict_NNNN.leo file. 

On the down side, this may well be too baroque a fix for a problem that most users may never encounter. If so, perhaps it's best left alone until more pressing problems are solved. I know what I am doing with Leo and am always careful NOT to generate conflicting clones when I edit in an external text editor, so I don't absolutely need a resolution to this problem. I raised it because it's good for a program to have well-defined behavior when presented with anomalous input. 

In this sense, perhaps the best thing is to allow users to generate code from clones (what Allan Holub referred to as "enough rope to shoot yourself in the foot"), but to tell them that this practice is frowned upon.  

 
</t>
<t tx="T673">Read and respond to this message at: 
https://sourceforge.net/forum/message.php?msg_id=1836117
By: gilshwartz

Edward, now that conflicting clones may not be the result of bad style, I would
like to propose yet another solution that I have been thinking of for a while.

My basic approach is that cloning is not just a convenience tool, it may also
reflect some of the properties of the code/code set. Therefore my goal is for
clone links to remain even if they are conflicting, and let the user resolve
them at any convenient time. I also think that Leo's user interface is the best
tool to resolve such conflicts.

Thus here is my view of clone management and resolution inside Leo. Anytime
content is loaded into Leo, if a clone set agrees (i.e. have the same content)
all clone copies are marked "green". When one green clone is edited, all green
clones are changed. This is Leo as it is now.

If at some point conflicting clones are loaded, Leo decides on some representing
content (may be based on policies like most occurring content, or latest timestamp,
etc.) and provides visual clues for the conflict. The visual clue is give by
a double node box, e.g.

+---------------+
+ clone org +
+---------------+
+ resolution +
+---------------+

such that it is a single node in the tree, but has two content node, the original
text, and the possibly arbitrary resolution.

The resolution pseudo node is marked "blue", while the original text is either
"green", if it is identical to the blue node, or "red", if it is not. To emphasis,
the red/green nodes contain the specific (possibly) unique code associated with
the derived file, while the pseudo blue node contains the shared clone content.
During save to derived files, only the red/green content is saved, so effectively
the file is not changed and the conflict is not resolved until the user chooses
to do so. However, the clone relationship (via the gti) remains.

During editing, changes to red/green clones are local and do not propagate to
other clone copies (actually any change to a green node would turn it red).
Changes to the blue nodes do propagate since it is a single view of the clone.
A node pair may be converted to a regular node, effectively getting a new gti
and eliminating the blue copy. Or, it may be converted to the shared copy,
effectively forgetting its original content (leaving only the blue node). Once
there are no more red nodes in a clone set, all its nodes become green again
and the conflict is resolved.

Some additional clone actions I think are useful are:

1. Go to next/prev clone.
2. Go to next/prev green clone (useful when there are red ones).
3. Convert all green copies to a new clone group (useful when some clone copies
needs to remain clones, but break from the original clone set, thus getting
a new clone gti)

Action 3 enables the user to partition its clone set to several clone groups
by copying a clone's original content to its blue copy and finding matching
(green) clones.

What do we gain by all this?

1. We can have conflicting clones without catastrophes.
2. We get tools to handle conflicts and resolve them.
3. We keep on working is Leo's environment, which is the most supportive one
we can expect.

Gil

(By the way, I have a feeling that it would be useful to include along with
the gti a hash of its node content, which could tell Leo is a node was changed
outside of it. Also, including a timestamp in the opening sentinel, indicating
when Leo last saved it. These may help having intelligent decisions by Leo in
cases like conflicting clones.)
</t>
<t tx="T674">Read and respond to this message at: 
https://sourceforge.net/forum/message.php?msg_id=1804169
By: gilshwartz

Another thing to think about is what should happen when close heading is changing.
Right now, if you are inside Leo, all headings will be changed, and if you try
to change by hand it in the derived file, clone links are removed (after some
error reporting). This is quite reasonable in the current scheme of things,
where one is not really expected to mess up with Leo sentinels.

However, if/when @include is implemented, one would probably edit some files
with clones that may extend to other files and changing the clone node name
(via Leo) is quite feasible. Note that the gti for the cloned node would probably
not change. So

1. Do Leo resync the clone content based on the gti?
2. Does it break cloning and allocates a new gti for one (arbitrary?) clone
set?
3. Let the user resolve manually, offer undoable auto-resolution with reporting,
other?

More things to think about.

Gil
</t>
<t tx="T675">By: derwisch ( Johannes Hüsing ) 
 Cloning somewhere else   
2002-11-22 12:41  
Hi there, 

is there any method to have a clone somewhere very distant from the original node, other than having to hold the Ctrl+U(D) keys after cloning and wait till it is at the desired position? 

Similar to Copy&amp;Paste but with the recognition of the clone's cloneness? 


Johannes  </t>
<t tx="T676">Read and respond to this message at: 
https://sourceforge.net/forum/message.php?msg_id=1845268
By: gilshwartz

I am using Leo to manage a set of HTML pages in my site. There are several pages
named index.html in different paths. I have been using @path directive instead
of specifying path and filename in the @file heading.

By accident, one @file node was not under the node it should have been (the
one with the @path directive), and therefore one of the index.html files was
written twice during save. I got no warning and obviously did not notice. When
I restarted Leo I was surprised to see a read error. Of course the content and
layout of the first index.html did not correspond to the content and layout
of the second. Leo therefore reread the file and built the entire node structure
of the first file the same as the second one. Luckily I could just remove the
bad file and reload Leo.

Now for the troubling thought: had this been in the planned thin Leo file scenario,
I could not recover at all. Conclusion: Leo should warn of writing the same
file via different @file nodes. Possibly even to keep these files data within
the .leo file until the situation is resolved.

I think that since it is handling many files in parallel and auto tangling and
untangling, Leo needs to be very aware, careful, and responsible in foreseeing
and avoiding users' mistakes or unreasonable actions, especially in a thin .leo
environment were we loose our (auto) backup.</t>
<t tx="T677">Read and respond to this message at: 
https://sourceforge.net/forum/message.php?msg_id=1819498
By: nobody

A related, but nastier bug is: When I open a leo file in a directory containing
non-sentinalized versions of files in @file nodes, Leo tries to read these
files and the read fails - resulting in empty nodes. On saving the file, all
the original files are eaten away (emptied).

Even if the original Leo file contained the proper @file nodes, they are emptied.

Sure, the status pane gives 'read failure' messages, but it is easy to miss
those if only a few files failed. Can we have such serious messages in red or
better yet, pop up an error dialog box needing attention? (Or not touch the
original node contents in case the read fails?)

- Rajiv Bhagwat

</t>
<t tx="T678">At present Leo declares a "read error" if the derived files being read does not have the
structure and headlines as the corresponding part of the outline. I think there is a
simpler way that will simplify matters and be more reliable. What I am thinking of is
this: 

1. Leo will keep the outline from the .leo around while the corresponding derived file is
being read, but will make no changes to it. 

2. Leo will create a node following the actual @file node in the outline. This node will be
the root of the tree that is to be read in. 

3. Leo will use the createNthChild routine to create the outline. Unlike the present
version, createNthChild will not compare the tree being created with the old tree. It will
simply create the nodes as required, creating dummy nodes as needed. Also unlike the
present version, createNthChild will never declare any read errors. 

4. At the end of the read pass, we simply check that all nodes of the newly created tree
have been "filled in". This will almost certainly be the case, and even if it is not, we
need only issue a mild warning. 

5. In this scheme, only serious errors in the sentinel structure in the derived file will
cause the read to fail. If that happens we simply delete the newly created tree and keep
the old tree. There will no longer be an "error recovery" pass: we either retain the tree
from the outline or the replace it with the tree from the derived file. 

The problem with this scheme is that it doesn't provide any "mirroring", so some other
way must be found to remember marks and clone links. But this can be done in 4.0. 

There are a number of advantages to this scheme. 

1. It is less picky. At present createNthChild is a bit of a busy-body; it presumes to
require that the derived file structure matches the outline structure. It must do this now
in order to recreate clone links. 

2. When errors are found Leo presently trashes the old outline info and reloads the
derived file, thereby invalidating all clone links. This is a very weak kind of "recovery".
The alternative scheme will, in 4.0, ensure that data is preserved, either from the outline
or from the derived file. So the new scheme will do no error recovery at all: it will simply
choose between two sources of data. 

In short, 4.0 provides us with a way of simplifying the read process while at the same
time improving error recovery and reducing the chance for true "data tragedies". 

This new scheme can't be used in all its glory until 4.0. Until then I am not inclined to
mess with a more complex and still-dubious scheme. In other words, the problem isn't
serious enough, IMO, that it can't wait until 4.0.</t>
<t tx="T679">By: korakot ( Korakot Chaovavanich ) 
 RE: 4.0 design summary   
2003-02-22 05:58  
For 4.0, can leo open a 'derived file' as a standalone 
leo file? 

My idea comes from that 
1. Now the master leo file will contain no info on 
a @file node 
2. @include dont contain repeat information as well. 

This 2 observations make me feel that a 'derived file' 
from an @file node is actually equivalent to a .leo file 
and that they should be treated as equivalent. 
That is, it should be open independently from a 
master file (that contain the derived file). 
 
</t>
<t tx="T680">@nocolor

A note to myself:  Python dictionaries will simplify both the read and write code. 
</t>
<t tx="T681">Global Tnode Indices (gti's) are the defining feature of 4.0.

A "full" gti is a string of the form: "userid:location:timestamp:index" where userid is a cvs name, like edream or dthein, location identifies a location, timestamp denotes a time, and index is an integer used to disambiguate gti's that would otherwise be identical.  The user will specify userid and location strings in a file, say leoID.txt. This file is private: it will not be part of any distribution nor will it be part of cvs.  I'm not sure what Leo should do if it can't find leoID.txt.

Derived files will specify defaults for the userid and location strings.  A minimal gti is a string of the form "::timestamp", where the userid, location and index strings are taken to be the defaults.
</t>
<t tx="T682">Leo does not need childIndex values in sentinels in order to reconstruct the outline.

Leo can deduce the order of nodes introduced in the derived file by the @others directive.  The order for nodes introduced in the derived file by section references is inessential. Therefore, we may store order information separately in .leo files.  .leo files will have &lt;marks&gt; and &lt;order&gt; elements containing this inessential information.  The &lt;marks&gt; and &lt;order&gt; elements will be a list of gti's of nodes.
</t>
<t tx="T683">All essential information (structure and content) of an @file tree must be kept together.  Therefore, derived files must be fat.

@file trees in outlines can be thin. We no longer need information in the .leo file to recreate clone links.

@file-asis and @file-nosent trees in outlines must be thick.  The corresponding derived files contain no sentinels.  The _only_ way to create a thin derived file is to use @file-nosent or @file-asis. This way all essential information is in one place, namely in the outline. 
</t>
<t tx="T684">Whether a node is clone or not is a property of the outline in which the node resides; it is _not_ an intrinsic property of a node.  There can be no such thing as a clone index.

Unanswered question:  what happens if a node is used in several derived files and has different text in each?  This issues may happen more now that outlines don't mirror structure in derived files. This can't be a show-stopper, and it must be handled somehow, if only to warn people away from certain practices...</t>
<t tx="T685">Gti's should allow Leo to handle included .leo files in an outline.

These will probably be represented in an outline as @file x.leo, though perhaps @include x.leo would be more accurate and less likely to cause confusion with the various flavors of @file nodes.</t>
<t tx="T686">There is still the possibility of cvs corrupting the structure of derived files.

The format of derived files should be designed so that Leo can recover from corrupted derived files.  @+nodes will contain only the gti, and to have the headline _follow_ the @+node.  This scheme may be expanded in order to facilitate recovering from cvs interference.</t>
<t tx="T687">There is nowhere to put the info that would be needed.</t>
<t tx="T688">The following are the goals of the new format for derived files:

- The minimum of sentinels needed to properly recreate the outline.
- A robust way of telling whether newlines belong to sentinels or not.
- A minimum of intrusion and ugliness.
</t>
<t tx="T689">The code in leoAtFile.py will follow the present model (except that routines may be dispatched using a dispatching dict as in the syntax colorer).  The code in leoFileCommands.py will change slightly (mainly to handle &lt;marks&gt; and &lt;order&gt; elements.

It would be possible to use Python's xmllib or similar modules, and this is a fairly low priority, and not really connected with any other 4.0 design issues.</t>
<t tx="T690">@language plain
@comment ;

@+ref (or @+others)
	# text of ref      (on a single line)
@tnode gti
	# text of headline (on a single line)
@+body gti
	body text...
@-body gti
@-ref

The problems:

- We do _not_ want to alter sentinels to indicate whitespace!
  That would invite cvs to invite sentinels.
- If we add a newline before all sentinels then we will insert blank lines!
- If we don't add a newline before all sentinels then how will we represent sentinels?

* We could _optionally_ remove trailing whitespace from all nodes, and end all nodes with a single newline.
- Is this a leoConfig setting or a directive (very ugly)?</t>
<t tx="T691">@nocolor

I have been designing what the sentinels should look like using gti's.  Here are examples of my present thinking:

The typical expansions of section references and the @others directives will be as follows:

@+ref
	# text of ref      (on a single line)
@tnode gti
	# text of headline (on a single line)
@+body gti
	body text...
@-body gti
@afterref (generated only if text follows reference)
	text following ref (on a single line)
@-ref

@+others
@tnode gti
	# text of headline (again, on a single line)
@+body gti
	body text... 
@-body gti
...
@-others

Unlike previous versions, the @ref and @body sentinels do not contain reference or headline text.  This has two purposes:

1. These sentinels will _never_ change (because gti's never do).  Therefore, cvs is not likely ever to change these sentinels.  In fact, these sentinels should provide a stable starting point for cvs's diff.

2. If cvs does changes the text of a derived file, those changes should occur _between_ sentinels, either between the @+ref sentinel and the @tnode sentinel, or between the @tnode sentinel and the @+body sentinel, or between the @afterref sentinel and the @-body sentinel.  Because Leo only writes a single line in those places Leo can detect when cvs has indicated a conflict.  BTW: all other conflicts should show up in body text in the outline.

The @afterref sentinel explicitly represents any text that may follow a section reference.  This should allow Leo to eliminate spurious blank lines in some cases.

In general, there may be zero or more organizing nodes between an @others node or a referencing node and the nodes containing the definitions of sections.  As in previous version, Leo must indicate those intermediate nodes in the derived file.  Leo will represent these intermediate nodes using @parent sentinels. Unlike previous versions, Leo will not write child indices anywhere in derived files.

So the most general format of derived files will be something like this:

@+ref
	# text of ref 
@+parent gti 1  (parent nodes...)
@+parent gti 2
@tnode gti
	# text of headline
@+body gti
	body text...
@-body gti
@-parent gti 2
@-parent gti 1
@afterref
	text following ref
@-ref

@+others
@+parent gti 1
@tnode gti
	# text of headline
@+body gti
	body text...
@-body gti
...
@-parent gti 1
@+parent gti 2
@tnode gti
	# text of headline 
@+body gti
	body text...
@-body gti
...
@-parent gti 2
@-others

There will be changes to the @+leo sentinel so that Leo can know what format is being used for each derived file. This will allow Leo to read derived files created with previous versions of Leo.

Edward</t>
<t tx="T692">@nocolor

While designing the new sentinels for 4.0 I turned my attention to eliminating "extra" blank lines in derived files.  This seems like a reasonable and fairly straightforward project.  Not so: the problem is intractible.

Recall from my previous posting that in 4.0 a typical section reference will create the following sentinels:

@+ref (or @+others)
	# text of ref      (on a single line)
@tnode gti
	# text of headline (on a single line)
@+body gti
	body text...
@-body gti
@afterref (generated only if text follows reference)
	text following ref (on a single line)
@-ref

The fundamental problem is figuring out whether newlines that start and end sentinel lines should be included in body text.  Previous versions of Leo used information in the sentinels themselves to help deal with trailing whitespace in the body text.  However, after going to all the trouble to make sure that 4.0 sentinels never change we definitely don't want to alter sentinels to indicated whitepace!

So the problem of eliminating "extra" blanks lines around sentinels is intractible.  The proof is simple: we don't want to alter sentinels, there is no other place to carry the information that extra newlines were inserted before or after a sentinel.

Just for completeness, let us review why extra blank lines arise in derived files:

1. Conceptually all sentinels _must_ begin and end with newlines.  This can never change, as I have often stated before.  All sentinels must begin with a newline because otherwise there would be no way to recognize when they started.  All sentinels must end with a newline because otherwise there would be no way to know when a sentinel ended.  The reason that these statements are true (in general) is that sentinels are represented by single-line comments.  Without newlines there would be no way to know where user comments end and sentinels begin.

Yes, Leo does eliminate double newlines between adjacent sentinels, but in general the first sentinel of a group of sentinels must start with a newline and the last sentinel of a group of sentinels must end with a newline.

2. Therefore, if body text preceding a sentinel ends with a newline (or blank line), the derived file will have an "extra" blank line preceding the sentinel.  Similarly for body text that follows a sentinel.

The only way around this dilemma is to automatically remove trailing whitespace from the end of body text.  But that doesn't work in general: the "extra" blank lines can appear anywhere in body text.  So even if we were willing to mess with body text (a bad idea) we can't solve the general problem.

Finally, the only solution I can see to the "extra" newline problem is to write a script to munge derived files.  This could be done in a hook, but clearly this should not be how Leo operates in general: it is equivalent to elminating blanks lines in the original source code, and Leo will remove those lines when reading the derived file.  Another workaround would be to use @file-asis or @file-nosent trees...
</t>
<t tx="T693">@ignore
@color</t>
<t tx="T694">@ignore
@color</t>
<t tx="T695"># We can enable and disable the gnx_code plugin, so these don't really matter.</t>
<t tx="T696">self.use_pre_4pt0_file_formats = false # Should not be true here!</t>
<t tx="T697">self.use_pre_4pt0_file_formats = self.initBooleanConfigParam(
	"use_pre_4pt0_file_formats",self.use_pre_4pt0_file_formats)

if self.use_pre_4pt0_file_formats:
	if app().use_gnx == true:
		es("using pre 4.0 format",color="red")
	app().use_gnx = false # Never set use_gnx here!</t>
<t tx="T698"></t>
<t tx="T699"># New in 4.0.
if self.matchTag("&lt;default_gnx_id="):
	id = self.getDqString() ; self.getTag("/&gt;")
	if self.a.use_gnx:
		es("default id = " + id,color="blue")
	self.a.nodeIndices.setDefaultId(id)</t>
<t tx="T700">if not self.a.use_gnx: # 5/30/03: file indices can not be assumed to be distinct!
	self.tnodesDict = {}</t>
<t tx="T701">gnxString = None

if self.matchTag("tnx="): # New in 4.0
	index = gnxString = self.getDqString()
elif self.matchTag("tx=\"T"): # Pre 4.0
	# tx overrides tnx for compatibility with pre 4.0 files.
	index = self.getIndex() ; self.getDquote()
	# if self.usingClipboard: trace(index)</t>
<t tx="T702">if gnxString and self.a.use_gnx: # New in 4.0.
	gnx = self.nodeIndices.scanGnx(gnxString,0)
	if t.gnx:
		if not self.nodeIndices.areEqual(gnx,t.gnx):
			print "conflicting gnx values",
			print gnxString, self.nodeIndices.toString(t.gnx)
	else:
		# print "tnode gnx from .leo file:", gnxString
		t.gnx = gnx
</t>
<t tx="T703">if self.matchTag("tnx="): # New in 4.0
	tref = self.getDqString()
elif
		</t>
<t tx="T704">if self.a.use_gnx:
	self.assignAllGnx(root=root)
else:</t>
<t tx="T705">&lt;&lt; put default gnx &gt;&gt;</t>
<t tx="T706"># New in 4.0.
if self.a.use_gnx:
	id = self.nodeIndices.getDefaultId()
	if id and len(id) &gt; 0:
		self.put_tab()
		self.put("&lt;default_gnx_id=")
		self.put_in_dquotes(id) ; self.put("/&gt;") ; self.put_nl()</t>
<t tx="T707">if self.a.use_gnx:
	&lt;&lt; write all visited tnodes &gt;&gt;
else:</t>
<t tx="T708"># putVnodes sets the visited bit in all tnodes that should be written.
while v and v != after:
	t = v.t
	if t.isVisited():
		self.putTnode(t)
		t.clearVisited() # Don't write the tnode again.
	v = v.threadNext()
</t>
<t tx="T709">if self.a.use_gnx:
	assert(t.gnx) # assignAllGnx has set all indices.
	gnxString = self.nodeIndices.toString(t.gnx,removeDefaultId=true)
	self.put(" tnx=") ; self.put_in_dquotes(gnxString)
else:</t>
<t tx="T710">if self.a.use_gnx:
	&lt;&lt; put v.t.gnx &gt;&gt;
else:</t>
<t tx="T711">t = v.t
assert(t.gnx)
tnxString = self.nodeIndices.toString(t.gnx,removeDefaultId=true)
self.put(" tnx=") ; self.put_in_dquotes(tnxString)

t.setVisited() # Indicate we wrote the body text.</t>
<t tx="T712">@language python

from leoGlobals import *
import leoDialog,leoNodes
import os,os.path,time

@ The list of language names that are written differently from the names in language_delims_dict in leoGlobals.py.  This is needed for compatibility with the borland version of Leo.

We convert from names in xml_language_names to names in language_delims_dict by converting the name to lowercase and by removing slashes.
@c

xml_language_names = (
	"CWEB","C","HTML","Java","LaTeX",
	"Pascal","PerlPod","Perl","Plain","Python","tcl/tk")

class BadLeoFile(Exception):
	def __init__(self, message):
		self.message = message
		Exception.__init__(self,message) # 4/26/03: initialize the base class.
	def __str__(self):
		return "Bad Leo File:" + self.message

class baseFileCommands:
	"""A base class for the fileCommands subcommander."""
	@others
	
class fileCommands (baseFileCommands):
	"""A class creating the fileCommands subcommander."""
	pass</t>
<t tx="T713">def __init__(self,commands):

	# trace("__init__", "fileCommands.__init__")
	self.commands = commands
	self.frame = commands.frame
	self.initIvars()

def initIvars(self):

	# General
	self.maxTnodeIndex = 0
	self.numberOfTnodes = 0
	self.topVnode = None
	self.mFileName = ""
	self.fileDate = -1
	self.leo_file_encoding = app().config.new_leo_file_encoding
	# For reading
	self.fileFormatNumber = 0
	self.ratio = 0.5
	self.fileBuffer = None ; self.fileIndex = 0
	# For writing
	self.read_only = false
	self.outputFile = None # File for normal writing
	self.outputString = None # String for pasting
	self.openDirectory = None
	self.usingClipboard = false
	# New in 3.12
	self.a = app()
	self.copiedTree = None
	self.tnodesDict = {}
</t>
<t tx="T714"></t>
<t tx="T715">def createVnode(self,parent,back,tref,headline):
	
	# trace(`headline` + ", parent:" + `parent` + ", back:" + `back`)
	v = None ; c = self.commands
	# Shared tnodes are placed in the file even if empty.
	if tref == -1:
		t = leoNodes.tnode()
	else:
		t = self.tnodesDict.get(tref)
		if not t:
			t = self.newTnode(tref)
	if back: # create v after back.
		v = back.insertAfter(t)
	elif parent: # create v as the parent's first child.
		v = parent.insertAsNthChild(0,t)
	else: # create a root vnode
		v = leoNodes.vnode(c,t)
		v.moveToRoot()
		c.tree.rootVnode = v
	v.initHeadString(headline,encoding=self.leo_file_encoding)
	return v</t>
<t tx="T716"># This method finishes pasting the outline from the clipboard.
def finishPaste(self):

	c=self.commands
	current = c.currentVnode()
	after = current.nodeAfterTree()
	c.beginUpdate()
	if 1: # inside update...
		if 0: # Warning: this will only join pasted clones, and is very dangerous.
			&lt;&lt; Create join lists of all pasted vnodes &gt;&gt;
		&lt;&lt; Recompute clone bits for pasted vnodes &gt;&gt;
		self.compactFileIndices()
		c.selectVnode(current)
	c.endUpdate()
	return current</t>
<t tx="T717">v = c.currentVnode()

while v and v != after:
	if v not in v.t.joinList:
		v.t.joinList.append(v)
	v = v.threadNext()
</t>
<t tx="T718">@ This must be done after the join lists have been created.  The saved clone bit is unreliable for pasted nodes.
@c

v = c.currentVnode()
while v and v != after:
	v.initClonedBit(v.shouldBeClone())
	v.clearDirty()
	v = v.threadNext()</t>
<t tx="T719"></t>
<t tx="T720"></t>
<t tx="T721">def getBool (self):
	self.skipWs() # guarantees at least one more character.
	ch = self.fileBuffer[self.fileIndex]
	if ch == '0':
		self.fileIndex += 1 ; return false
	elif ch == '1':
		self.fileIndex += 1 ; return true
	else:
		raise BadLeoFile("expecting bool constant")
		
def getDqBool (self):
	self.getDquote() ; val = self.getBool() ; self.getDquote()
	return val
	
def getDqString (self): # 7/10/02
	self.getDquote()
	i = self.fileIndex
	self.fileIndex = j = string.find(self.fileBuffer,'"',i)
	if j == -1: raise BadLeoFile("unterminated double quoted string")
	s = self.fileBuffer[i:j]
	self.getDquote()
	return s

def getDouble (self):
	self.skipWs()
	i = self.fileIndex ; buf = self.fileBuffer
	floatChars = string.digits + 'e' + 'E' + '.' + '+' + '-'
	n = len(buf)
	while i &lt; n and buf[i] in floatChars:
		i += 1
	if i == self.fileIndex:
		raise BadLeoFile("expecting float constant")
	val = float(buf[self.fileIndex:i])
	self.fileIndex = i
	return val

def getDquote (self):
	self.getTag('"')
	
def getIndex (self):
	val = self.getLong()
	if val &lt; 0: raise BadLeoFile("expecting index")
	return val
	
def getLong (self):
	self.skipWs() # guarantees at least one more character.
	i = self.fileIndex
	if self.fileBuffer[i] == '-':
		i += 1
	n = len(self.fileBuffer)
	while i &lt; n and self.fileBuffer[i] in string.digits:
		i += 1
	if i == self.fileIndex:
		raise BadLeoFile("expecting int constant")
	val = int(self.fileBuffer[self.fileIndex:i])
	self.fileIndex = i
	return val
		
def getStringToTag (self,tag):
	buf = self.fileBuffer
	blen = len(buf) ; tlen = len(tag)
	i = j = self.fileIndex
	while i &lt; blen:
		if tag == buf[i:i+tlen]:
			self.fileIndex = i
			return buf[j:i]
		else: i += 1
	raise BadLeoFile("expecting string terminated by " + tag)
	return ""
	
# Look ahead for collapsed tag: tag may or may not end in "&gt;"
# Skips tag and /&gt; if found, otherwise does not alter index.
def getOpenTag (self,tag):
	if tag[-1] == "&gt;":
		# Only the tag itself or a collapsed tag are valid.
		if self.matchTag(tag):
			return false # Not a collapsed tag.
		elif self.matchTag(tag[:-1]):
			# It must be a collapsed tag.
			self.skipWs()
			if self.matchTag("/&gt;"):
				return true
		print "getOpenTag(", tag, ") failed:"
		raise BadLeoFile("expecting" + tag)
	else:
		# The tag need not be followed by "/&gt;"
		if self.matchTag(tag):
			old_index = self.fileIndex
			self.skipWs()
			if self.matchTag("/&gt;"):
				return true
			else:
				self.fileIndex = old_index
				return false
		else:
			print "getOpenTag(", tag, ") failed:"
			raise BadLeoFile("expecting" + tag)
	
# 11/24/02: Look ahead for closing /&gt;
# Return true if found.
def getTag (self,tag):
	if self.matchTag(tag):
		return
	else:
		print "getTag(", tag, ") failed:"
		raise BadLeoFile("expecting" + tag)
</t>
<t tx="T722">def matchChar (self,ch):
	self.skipWs() # guarantees at least one more character.
	if ch == self.fileBuffer[self.fileIndex]:
		self.fileIndex += 1 ; return true
	else: return false

# Warning: does not check for end-of-word,
# so caller must match prefixes first.
def matchTag (self,tag):
	self.skipWsAndNl() # guarantees at least one more character.
	i = self.fileIndex
	if tag == self.fileBuffer[i:i+len(tag)]:
		self.fileIndex += len(tag)
		return true
	else:
		return false

def matchTagWordIgnoringCase (self,tag):
	self.skipWsAndNl() # guarantees at least one more character.
	i = self.fileIndex
	tag = string.lower(tag)
	j = skip_c_id(self.fileBuffer,i)
	word = self.fileBuffer[i:j]
	word = string.lower(word)
	if tag == word:
		self.fileIndex += len(tag)
		return true
	else:
		return false
</t>
<t tx="T723">def getClipboardHeader (self):

	if self.getOpenTag("&lt;leo_header"):
		return # 11/24/02

	while 1:
		if self.matchTag("file_format="):
			self.getDquote() ; self.fileFormatNumber = self.getLong() ; self.getDquote()
		elif self.matchTag("tnodes="):
			self.getDquote() ; self.getLong() ; self.getDquote() # no longer used
		elif self.matchTag("max_tnode_index="):
			self.getDquote() ; self.getLong() ; self.getDquote() # no longer used
		else:
			self.getTag("/&gt;")
			break</t>
<t tx="T724"># For compatibility with old file formats.

def getCloneWindows (self):

	if not self.matchTag("&lt;clone_windows&gt;"):
		return

	while self.matchTag("&lt;clone_window vtag=\"V"):
		self.getLong() ; self.getDquote() ; self.getTag("&gt;")
		if not self.getOpenTag("&lt;global_window_position"):
			self.getTag("&lt;global_window_position")
			self.getPosition()
			self.getTag("/&gt;")
		self.getTag("&lt;/clone_window&gt;")
	self.getTag("&lt;/clone_windows&gt;")</t>
<t tx="T725">def getEscapedString (self):

	# The next '&lt;' begins the ending tag.
	i = self.fileIndex
	self.fileIndex = j = string.find(self.fileBuffer,'&lt;',i)
	if j == -1:
		raise BadLeoFile("unterminated escaped string")
	else:
		# Allocates memory
		return self.xmlUnescape(self.fileBuffer[i:j])</t>
<t tx="T726">def getFindPanelSettings (self):

	c = self.commands ; config = app().config ; findFrame = app().findFrame
	&lt;&lt; Set defaults of all flags &gt;&gt;
	if not self.getOpenTag("&lt;find_panel_settings"):
		while 1:
			if   self.matchTag("batch="): c.batch_flag = self.getDqBool()
			elif self.matchTag("wrap="): c.wrap_flag = self.getDqBool()
			elif self.matchTag("whole_word="): c.whole_word_flag = self.getDqBool()
			elif self.matchTag("ignore_case="): c.ignore_case_flag = self.getDqBool()
			elif self.matchTag("pattern_match="): c.pattern_match_flag = self.getDqBool()
			elif self.matchTag("search_headline="): c.search_headline_flag = self.getDqBool()
			elif self.matchTag("search_body="): c.search_body_flag = self.getDqBool()
			elif self.matchTag("suboutline_only="): c.suboutline_only_flag = self.getDqBool()
			elif self.matchTag("mark_changes="): c.mark_changes_flag = self.getDqBool()
			elif self.matchTag("mark_finds="): c.mark_finds_flag = self.getDqBool()
			elif self.matchTag("reverse="): c.reverse_flag = self.getDqBool()
			elif self.matchTag("node_only="): c.node_only_flag = self.getDqBool()
			else: break
					
		self.getTag("&gt;")
		#
		self.getTag("&lt;find_string&gt;")
		c.find_text = self.getEscapedString()
		self.getTag("&lt;/find_string&gt;")
		#
		self.getTag("&lt;change_string&gt;")
		c.change_text = self.getEscapedString()
		self.getTag("&lt;/change_string&gt;")
		#
		self.getTag("&lt;/find_panel_settings&gt;")
	
	# Override .leo file's preferences if settings are in leoConfig.txt.
	config.setCommandsFindIvars(c)
	# Update the settings immediately.
	app().findFrame.init(c)</t>
<t tx="T727">for var in findFrame.intKeys:
	attr = "%s_flag" % (var)
	setattr(c,attr,false)
</t>
<t tx="T728">def getGlobals (self):

	if self.getOpenTag("&lt;globals"):
		return

	self.getTag("body_outline_ratio=\"")
	self.ratio = self.getDouble() ; self.getDquote() ; self.getTag("&gt;")

	self.getTag("&lt;global_window_position")
	y,x,h,w = self.getPosition() ; self.getTag("/&gt;")
	# print ("y,x,h,w:" + `y` + "," + `x` + "," + `h` + "," + `w`)
	
	# Bug fix: 7/15/02: use max, not min!!!
	y = max(y,0) ; x = max(x,0)
	geom = "%dx%d%+d%+d" % (w,h,x,y)
	self.frame.top.geometry(geom)
	# 7/15/02: Redraw the window before writing into it.
	self.frame.top.deiconify()
	self.frame.top.lift()
	self.frame.top.update()

	self.getTag("&lt;global_log_window_position")
	self.getPosition() ;
	self.getTag("/&gt;") # no longer used.

	self.getTag("&lt;/globals&gt;")</t>
<t tx="T729"># The caller should enclose this in begin/endUpdate.

def getLeoFile (self,frame,fileName,atFileNodesFlag=true):

	c=self.commands
	&lt;&lt; warn on read-only files &gt;&gt;
	self.mFileName = frame.mFileName
	self.tnodesDict = {}
	ok = true
	try:
		c.tree.initing = true # inhibit endEditLabel from marking the file changed.
		## import time ; start = time.clock()
		&lt;&lt; scan all the xml elements &gt;&gt;
		## print "read time" + "%6.3f" % (time.clock()-start)
	except BadLeoFile, message:
		&lt;&lt; raise an alert &gt;&gt;
		ok = false
	if ok and atFileNodesFlag:
		c.atFileCommands.readAll(c.rootVnode(),partialFlag=false)
	if not c.tree.currentVnode:
		c.tree.currentVnode = c.tree.rootVnode
	self.setAllJoinLinks() # 5/3/03
	c.initAllCloneBits() # 5/3/03
	c.selectVnode(c.tree.currentVnode) # load body pane
	c.tree.initing = false # Enable changes in endEditLabel
	self.tnodesDict = {}
	return ok, self.ratio</t>
<t tx="T730">try:
	self.read_only = false
	self.read_only = not os.access(fileName,os.W_OK)
	if self.read_only:
		es("read only: " + fileName,color="red")
		leoDialog.askOk("Read-only ouline",
			"Warning: the outline: " + fileName + " is read-only.").run(modal=true)
except:
	if 0: # testing only: access may not exist on all platforms.
		es("exception getting file access")
		es_exception()</t>
<t tx="T731">self.getXmlVersionTag()
self.getXmlStylesheetTag()
self.getTag("&lt;leo_file&gt;")
self.getLeoHeader()
self.getGlobals()
self.getPrefs()
self.getFindPanelSettings()

# Causes window to appear.
c.frame.resizePanesToRatio(c.frame.ratio,c.frame.secondary_ratio) 
es("reading: " + fileName)

self.getVnodes()
self.getTnodes()
self.getCloneWindows()
self.getTag("&lt;/leo_file&gt;")</t>
<t tx="T732"># All other exceptions are Leo bugs.

# es_exception()
alert(self.mFileName + " is not a valid Leo file: " + `message`)</t>
<t tx="T733">def getLeoHeader (self):

	# Set defaults.
	self.maxTnodeIndex = 0
	self.numberOfTnodes = 0
	if self.getOpenTag("&lt;leo_header"):
		return

	# New in version 1.7: attributes may appear in any order.
	while 1:
		if self.matchTag("file_format="):
			self.getDquote() ; self.fileFormatNumber = self.getLong() ; self.getDquote()
		elif self.matchTag("tnodes="):
			self.getDquote() ; self.numberOfTnodes = self.getLong() ; self.getDquote()
		elif self.matchTag("max_tnode_index="):
			self.getDquote() ; self.maxTnodeIndex = self.getLong() ; self.getDquote()
		elif self.matchTag("clone_windows="):
			self.getDquote() ; self.getLong() ; self.getDquote() # no longer used.
		else:
			self.getTag("/&gt;")
			break</t>
<t tx="T734"># This method reads a Leo outline from string s in clipboard format.
def getLeoOutline (self,s):

	self.usingClipboard = true
	self.fileBuffer = s ; self.fileIndex = 0
	self.tnodesDict = {}

	try:
		self.getXmlVersionTag() # leo.py 3.0
		self.getXmlStylesheetTag() # 10/25/02
		self.getTag("&lt;leo_file&gt;")
		self.getClipboardHeader()
		self.getVnodes()
		self.getTnodes()
		self.getTag("&lt;/leo_file&gt;")
		v = self.finishPaste()
	except BadLeoFile:
		v = None

	# Clean up.
	self.fileBuffer = None ; self.fileIndex = 0
	self.usingClipboard = false
	self.tnodesDict = {}
	return v</t>
<t tx="T735">def getPosition (self):

	top = left = height = width = 0
	# New in version 1.7: attributes may appear in any order.
	while 1:
		if self.matchTag("top=\""):
			top = self.getLong() ; self.getDquote()
		elif self.matchTag("left=\""):
			left = self.getLong() ; self.getDquote()
		elif self.matchTag("height=\""):
			height = self.getLong() ; self.getDquote()
		elif self.matchTag("width=\""):
			width = self.getLong() ; self.getDquote()
		else: break
	return top, left, height, width</t>
<t tx="T736">def getPrefs (self):

	a = app() ; c = self.commands ; config = a.config
	
	if self.getOpenTag("&lt;preferences"):
		return

	while 1:
		if self.matchTag("allow_rich_text="):
			self.getDquote() ; self.getBool() ; self.getDquote() #ignored
		elif self.matchTag("tab_width="):
			self.getDquote() ; c.tab_width = self.getLong() ; self.getDquote()
		elif self.matchTag("page_width="):
			self.getDquote() ; c.page_width = self.getLong() ; self.getDquote()
		elif self.matchTag("tangle_bat="):
			self.getDquote() ; c.tangle_batch_flag = self.getBool() ; self.getDquote()
		elif self.matchTag("untangle_bat="):
			self.getDquote() ; c.untangle_batch_flag = self.getBool() ; self.getDquote()
		# New in version 0.10
		elif self.matchTag("output_doc_chunks="):
			self.getDquote() ; c.output_doc_flag = self.getBool() ; self.getDquote()
		elif self.matchTag("noweb_flag="):
			# New in version 0.19: Ignore this flag.
			self.getDquote() ; self.getBool() ; self.getDquote()
		elif self.matchTag("extended_noweb_flag="):
			# New in version 0.19: Ignore this flag.
			self.getDquote() ; self.getBool() ; self.getDquote()
		elif self.matchTag("defaultTargetLanguage="):
			# New in version 0.15
			self.getDquote()
			&lt;&lt; check for syntax coloring prefs &gt;&gt;
		elif self.matchTag("use_header_flag="):
			self.getDquote() ; c.use_header_flag = self.getBool() ; self.getDquote()
		else: break
	self.getTag("&gt;")
	while 1:
		if self.matchTag("&lt;defaultDirectory&gt;"):
			# New in version 0.16.
			c.tangle_directory = self.getEscapedString()
			self.getTag("&lt;/defaultDirectory&gt;")
			if not os.path.exists(c.tangle_directory):
				es("default tangle directory not found:" + c.tangle_directory)
		elif self.matchTag("&lt;TSyntaxMemo_options&gt;"):
			self.getEscapedString() # ignored
			self.getTag("&lt;/TSyntaxMemo_options&gt;")
		else: break
	self.getTag("&lt;/preferences&gt;")
	
	# Override .leo file's preferences if settings are in leoConfig.txt.
	if config.configsExist:
		config.setCommandsIvars(c)</t>
<t tx="T737"># Must match longer tags before short prefixes.

language = "c" # default

for name in a.language_delims_dict.keys():
	if self.matchTagWordIgnoringCase(name):
		s = string.lower(name)
		language = string.replace(name,"/","")
		self.getDquote()
		break

c.target_language = language</t>
<t tx="T738">def getSize (self):

	# New in version 1.7: attributes may appear in any order.
	height = 0 ; width = 0
	while 1:
		if self.matchTag("height=\""):
			height = self.getLong() ; self.getDquote()
		elif self.matchTag("width=\""):
			width = self.getLong() ; self.getDquote()
		else: break
	return height, width</t>
<t tx="T739">def getTnode (self):

	# we have already matched &lt;t.
	index = -1
	# New in version 1.7: attributes may appear in any order.
	while 1:
		if self.matchTag("tx=\"T"):
			index = self.getIndex() ; self.getDquote()
			# if self.usingClipboard: trace(index)
		elif self.matchTag("rtf=\"1\""): pass # ignored
		elif self.matchTag("rtf=\"0\""): pass # ignored
		else: break
	self.getTag("&gt;")
	t = self.tnodesDict.get(index)
	if t:
		if self.usingClipboard:
			&lt;&lt; handle read from clipboard &gt;&gt;
		else:
			&lt;&lt; handle read from file &gt;&gt;
	else:
		es("no tnode with index: " + `index` + ".  The text will be discarded")
	self.getTag("&lt;/t&gt;")</t>
<t tx="T740">s = self.getEscapedString()
t.setTnodeText(s,encoding=self.leo_file_encoding)</t>
<t tx="T741">if t:
	s = self.getEscapedString()
	t.setTnodeText(s,encoding=self.leo_file_encoding)
	# trace(`index`,`len(s)`)</t>
<t tx="T742">def getTnodes (self):

	# A slight change: we require a tnode element.  But Leo always writes this.
	if self.getOpenTag("&lt;tnodes&gt;"):
		return
		
	while self.matchTag("&lt;t"):
		self.getTnode()
	self.getTag("&lt;/tnodes&gt;")
</t>
<t tx="T743">def getVnode (self,parent,back):

	# trace("parent:" + `parent` + ", back:" + `back`)
	c = self.commands
	setCurrent = setExpanded = setMarked = setOrphan = setTop = false
	tref = -1 ; headline = "" ; gnxString = None
	# we have already matched &lt;v.
	while 1:
		if self.matchTag("a=\""):
			&lt;&lt; Handle vnode attribute bits &gt;&gt;
		elif self.matchTag("t=\"T"):
			tref = self.getIndex() ; self.getDquote()
		elif self.matchTag("vtag=\"V"):
			self.getIndex() ; self.getDquote() # ignored
		else: break
	self.getTag("&gt;")
	# Headlines are optional.
	if self.matchTag("&lt;vh&gt;"):
		headline = self.getEscapedString() ; self.getTag("&lt;/vh&gt;")
	# Link v into the outline using parent and back.
	v = self.createVnode(parent,back,tref,headline)
	&lt;&lt; Set the remembered status bits &gt;&gt;
	# Recursively create all nested nodes.
	parent = v ; back = None
	while self.matchTag("&lt;v"):
		back = self.getVnode(parent,back)
	# End this vnode.
	self.getTag("&lt;/v&gt;")
	return v</t>
<t tx="T744"># The a=" has already been seen.
while 1:
	if   self.matchChar('C'): pass # Not used: clone bits are recomputed later.
	elif self.matchChar('D'): pass # Not used.
	elif self.matchChar('E'): setExpanded = true
	elif self.matchChar('M'): setMarked = true
	elif self.matchChar('O'): setOrphan = true
	elif self.matchChar('T'): setTop = true
	elif self.matchChar('V'): setCurrent = true
	else: break
self.getDquote()</t>
<t tx="T745">if setCurrent:
	c.tree.currentVnode = v

if setExpanded:
	v.initExpandedBit()

if setMarked:
	v.setMarked()

if setOrphan:
	v.setOrphan()

if setTop:
	c.mTopVnode = v  # Not used at present.
</t>
<t tx="T746">def getVnodes (self):

	c=self.commands
	if  self.usingClipboard:
		# Paste after the current vnode.
		back = c.currentVnode() ; parent = back.parent()
	else:
		back = None ; parent = None

	if self.getOpenTag("&lt;vnodes&gt;"):
		return

	while self.matchTag("&lt;v"):
		back = self.getVnode(parent,back)

	self.getTag("&lt;/vnodes&gt;")</t>
<t tx="T747">@ Parses the optional xml stylesheet string, and sets the corresponding config option.

For example, given: &lt;?xml_stylesheet s?&gt;
the config option is s.
@c

def getXmlStylesheetTag (self):
	
	c = self.commands
	tag = "&lt;?xml-stylesheet "

	if self.matchTag(tag):
		s = self.getStringToTag("?&gt;")
		# print "reading:", tag + s + "?&gt;"
		c.frame.stylesheet = s
		self.getTag("?&gt;")
</t>
<t tx="T748"># Parses the encoding string, and sets self.leo_file_encoding.

def getXmlVersionTag (self):
	
	a = app() ; config = a.config

	self.getTag(a.prolog_prefix_string)
	encoding = self.getDqString()
	self.getTag(a.prolog_postfix_string)

	if isValidEncoding(encoding):
		self.leo_file_encoding = encoding
	else:
		es("invalid encoding in .leo file: " + encoding)
</t>
<t tx="T749">def skipWs (self):

	while self.fileIndex &lt; len(self.fileBuffer):
		ch = self.fileBuffer[self.fileIndex]
		if ch == ' ' or ch == '\t':
			self.fileIndex += 1
		else: break

	# The caller is entitled to get the next character.
	if  self.fileIndex &gt;= len(self.fileBuffer):
		raise BadLeoFile("")</t>
<t tx="T750">def skipWsAndNl (self):

	while self.fileIndex &lt; len(self.fileBuffer):
		ch = self.fileBuffer[self.fileIndex]
		if ch == ' ' or ch == '\t' or ch == '\r' or ch == '\n':
			self.fileIndex += 1
		else: break

	# The caller is entitled to get the next character.
	if  self.fileIndex &gt;= len(self.fileBuffer):
		raise BadLeoFile("")</t>
<t tx="T751">def newTnode(self,index):

	if self.tnodesDict.has_key(index):
		es("bad tnode index: " + `index` + ". Using empty text.")
		return leoNodes.tnode()
	else:
		t = leoNodes.tnode()
		t.setFileIndex(index)
		self.tnodesDict[index] = t
		return t</t>
<t tx="T752">def readAtFileNodes (self):

	c = self.commands ; current = c.currentVnode()
	c.atFileCommands.readAll(current,partialFlag=true)
	self.setAllJoinLinks(current) # 5/3/03
	c.initAllCloneBits() # 5/3/03
	c.redraw() # 4/4/03
	
	# 7/8/03: force an update of the body pane.
	current.setBodyStringOrPane(current.bodyString())
	c.tree.onBodyChanged(current,undoType=None)</t>
<t tx="T753">def readOutlineOnly (self,file,fileName):

	c=self.commands
	# Read the entire file into the buffer
	self.fileBuffer = file.read() ; file.close()
	self.fileIndex = 0
	&lt;&lt; Set the default directory &gt;&gt;
	c.beginUpdate()
	ok, ratio = self.getLeoFile(self.frame,fileName,atFileNodesFlag=false)
	c.endUpdate()
	c.frame.top.deiconify()
	c.setChanged(false)
	vflag,junk,secondary_ratio = self.frame.initialRatios()
	c.frame.resizePanesToRatio(ratio,secondary_ratio)
	# This should be done after the pane size has been set.
	if 0: # This can not be done at present.
		if self.topVnode:
			c.tree.scrollTo(self.topVnode)
			c.tree.Refresh()
	# delete the file buffer
	self.fileBuffer = ""
	return ok</t>
<t tx="T754">@ The most natural default directory is the directory containing the .leo file that we are about to open.  If the user has specified the "Default Directory" preference that will over-ride what we are about to set.
@c

dir = os.path.dirname(fileName) 
if len(dir) &gt; 0:
	c.openDirectory = dir</t>
<t tx="T755">def open(self,file,fileName):

	c=self.commands
	# Read the entire file into the buffer
	# t = getTime()
	self.fileBuffer = file.read() ; file.close()
	self.fileIndex = 0
	&lt;&lt; Set the default directory &gt;&gt;
	# esDiffTime("open:read all", t)

	c.beginUpdate()
	if 1: # inside update...
		c.loading = true # disable c.changed
		ok, ratio = self.getLeoFile(self.frame,fileName,atFileNodesFlag=true)
		c.loading = false # reenable c.changed
		c.setChanged(false)
		if 0: # This can't be done directly.
			# This should be done after the pane size has been set.
			top = c.tree.topVnode
			if top: c.tree.scrollTo(top)
	c.endUpdate()
	# delete the file buffer
	self.fileBuffer = ""
	# esDiffTime("open: exit",t)
	return ok</t>
<t tx="T756">def setAllJoinLinks (self,root=None):
	
	"""Update all join links in the tree"""
	
	# trace(root)

	if root: # Only update the subtree.
		v = root # 6/3/03
		after = root.nodeAfterTree()
		while v and v != after:
			if v not in v.t.joinList:
				v.t.joinList.append(v)
			v = v.threadNext()
	else: # Update everything.
		v = self.commands.rootVnode()
		while v:
			if v not in v.t.joinList:
				v.t.joinList.append(v)
			v = v.threadNext()</t>
<t tx="T757">def xmlUnescape(self,s):

	if s:
		s = string.replace(s, '\r', '')
		s = string.replace(s, "&amp;lt;", '&lt;')
		s = string.replace(s, "&amp;gt;", '&gt;')
		s = string.replace(s, "&amp;amp;", '&amp;')
	return s</t>
<t tx="T758"></t>
<t tx="T759">def assignFileIndices (self,root=None):
	
	"""Assign a file index to all tnodes"""
	
	c=self.commands
	
	if root == None:
		root = c.rootVnode()
	v = root
	while v:
		t = v.t

		# 8/28/99.  Write shared tnodes even if they are empty.
		if t.hasBody() or len(v.t.joinList) &gt; 0:
			if t.fileIndex == 0:
				self.maxTnodeIndex += 1
				t.setFileIndex(self.maxTnodeIndex)
		else:
			t.setFileIndex(0)
			
		# if self.usingClipboard: trace(t.fileIndex)
		v = v.threadNext()</t>
<t tx="T760">def compactFileIndices (self):
	
	"""Assign a file index to all tnodes, compacting all file indices"""
	
	c = self.commands ; root = c.rootVnode()
	
	v = root
	self.maxTnodeIndex = 0
	while v: # Clear all indices.
		v.t.setFileIndex(0)
		v = v.threadNext()

	v = c.rootVnode()
	while v: # Set indices for all tnodes that will be written.
		t = v.t
		#### old code was: if t.hasBody() or v.getJoinList():
		if t.hasBody() or len(v.t.joinList) &gt; 0: # Write shared tnodes even if they are empty.
			if t.fileIndex == 0:
				self.maxTnodeIndex += 1
				t.setFileIndex(self.maxTnodeIndex)
		v = v.threadNext()</t>
<t tx="T761"></t>
<t tx="T762">def putClipboardHeader (self):

	tnodes = 0
	&lt;&lt; count the number of tnodes &gt;&gt;
	self.put('&lt;leo_header file_format="1" tnodes=')
	self.put_in_dquotes(`tnodes`)
	self.put(" max_tnode_index=")
	self.put_in_dquotes(`tnodes`)
	self.put("/&gt;") ; self.put_nl()</t>
<t tx="T763">c=self.commands
c.clearAllVisited()

# Count the vnode and tnodes.
v = c.currentVnode()
after = v.nodeAfterTree()
while v and v != after:
	t = v.t
	if t and not t.isVisited() and (t.hasBody() or len(v.t.joinList) &gt; 0):
		t.setVisited()
		tnodes += 1
	v = v.threadNext()</t>
<t tx="T764"># All output eventually comes here.
def put (self,s):
	if s and len(s) &gt; 0:
		if self.outputFile:
			s = toEncodedString(s,self.leo_file_encoding,reportErrors=true)
			self.outputFile.write(s)
		elif self.outputString != None: # Write to a string
			self.outputString += s

def put_dquote (self):
	self.put('"')
		
def put_dquoted_bool (self,b):
	if b: self.put('"1"')
	else: self.put('"0"')
		
def put_flag (self,a,b):
	if a:
		self.put(" ") ; self.put(b) ; self.put('="1"')
		
def put_in_dquotes (self,a):
	self.put('"')
	if a: self.put(a) # will always be true if we use backquotes.
	else: self.put('0')
	self.put('"')

def put_nl (self):
	self.put("\n")
	
def put_tab (self):
	self.put("\t")
	
def put_tabs (self,n):
	while n &gt; 0:
		self.put("\t")
		n -= 1</t>
<t tx="T765">@ Surprisingly, the call to xmlEscape here is _much_ faster than calling put for each characters of s.
@c

def putEscapedString (self,s):

	if s and len(s) &gt; 0:
		self.put(self.xmlEscape(s))</t>
<t tx="T766">def putFindSettings (self):

	c = self.commands ; config = app().config

	self.put("&lt;find_panel_settings")
	
	&lt;&lt; put find settings that may exist in leoConfig.txt &gt;&gt;
	
	self.put("&lt;/find_panel_settings&gt;") ; self.put_nl()</t>
<t tx="T767">if config.configsExist and not config.read_only: # 8/6/02
	pass # config.update has already been called.
else:
	self.put_flag(c.batch_flag,"batch")
	self.put_flag(c.ignore_case_flag,"ignore_case")
	self.put_flag(c.mark_changes_flag,"mark_changes")
	self.put_flag(c.mark_finds_flag,"mark_finds")
	self.put_flag(c.pattern_match_flag,"pattern_match")
	self.put_flag(c.reverse_flag,"reverse")
	self.put_flag(c.search_headline_flag,"search_headline")
	self.put_flag(c.search_body_flag,"search_body")
	self.put_flag(c.suboutline_only_flag,"suboutline_only")
	self.put_flag(c.whole_word_flag,"whole_word")
	self.put_flag(c.wrap_flag,"wrap")
	self.put_flag(c.node_only_flag,"node_only")

self.put("&gt;") ; self.put_nl()

if config.configsExist and not config.read_only: # 8/6/02
	self.put_tab()
	self.put("&lt;find_string&gt;&lt;/find_string&gt;") ; self.put_nl()
else:
	self.put_tab()
	self.put("&lt;find_string&gt;") ; self.putEscapedString(c.find_text)
	self.put("&lt;/find_string&gt;") ; self.put_nl()

if config.configsExist and not config.read_only: # 8/6/02
	self.put_tab()
	self.put("&lt;change_string&gt;&lt;/change_string&gt;") ; self.put_nl()
else:
	self.put_tab()
	self.put("&lt;change_string&gt;") ; self.putEscapedString(c.change_text)
	self.put("&lt;/change_string&gt;") ; self.put_nl()</t>
<t tx="T768">def putGlobals (self):

	c=self.commands
	self.put("&lt;globals")
	&lt;&lt; put the body/outline ratio &gt;&gt;
	self.put("&gt;") ; self.put_nl()
	&lt;&lt; put the position of this frame &gt;&gt;
	&lt;&lt; put the position of the log window &gt;&gt;

	self.put("&lt;/globals&gt;") ; self.put_nl()</t>
<t tx="T769"># Puts an innumerate number of digits

self.put(" body_outline_ratio=") ; self.put_in_dquotes(`c.frame.ratio`)</t>
<t tx="T770">width,height,left,top = get_window_info(self.frame.top)
#print ("t,l,h,w:" + `top` + ":" + `left` + ":" + `height` + ":" + `width`)

self.put_tab()
self.put("&lt;global_window_position")
self.put(" top=") ; self.put_in_dquotes(`top`)
self.put(" left=") ; self.put_in_dquotes(`left`)
self.put(" height=") ; self.put_in_dquotes(`height`)
self.put(" width=") ; self.put_in_dquotes(`width`)
self.put("/&gt;") ; self.put_nl()</t>
<t tx="T771">top = left = height = width = 0 # no longer used
self.put_tab()
self.put("&lt;global_log_window_position")
self.put(" top=") ; self.put_in_dquotes(`top`)
self.put(" left=") ; self.put_in_dquotes(`left`)
self.put(" height=") ; self.put_in_dquotes(`height`)
self.put(" width=") ; self.put_in_dquotes(`width`)
self.put("/&gt;") ; self.put_nl()</t>
<t tx="T772">def putHeader (self):

	tnodes = 0 ; clone_windows = 0 # Always zero in Leo2.

	self.put("&lt;leo_header")
	self.put(" file_format=") ; self.put_in_dquotes("2")
	self.put(" tnodes=") ; self.put_in_dquotes(`tnodes`)
	self.put(" max_tnode_index=") ; self.put_in_dquotes(`self.maxTnodeIndex`)
	self.put(" clone_windows=") ; self.put_in_dquotes(`clone_windows`)
	self.put("/&gt;") ; self.put_nl()</t>
<t tx="T773"># Writes a Leo outline to s in a format suitable for pasting to the clipboard.

def putLeoOutline (self):

	self.outputString = "" ; self.outputFile = None
	self.usingClipboard = true
	self.assignFileIndices() # 6/11/03: Must do this for 3.x code.
	self.putProlog()
	self.putClipboardHeader()
	self.putVnodes()
	self.putTnodes()
	self.putPostlog()
	s = self.outputString
	self.outputString = None
	self.usingClipboard = false
	return s</t>
<t tx="T774">def putPrefs (self):

	c = self.commands ; config = app().config

	self.put("&lt;preferences")
	self.put(" allow_rich_text=") ; self.put_dquoted_bool(0) # no longer used
	
	&lt;&lt; put prefs that may exist in leoConfig.txt &gt;&gt;
	
	self.put("&lt;/preferences&gt;") ; self.put_nl()</t>
<t tx="T775">language = c.target_language
for name in xml_language_names:
	s = string.lower(name)
	s = string.replace(s,"/","")
	if s == language:
		language = name ; break

if config.configsExist and not config.read_only: # 8/6/02
	pass # config.update has already been called.
else:
	self.put(" tab_width=") ; self.put_in_dquotes(`c.tab_width`)
	self.put(" page_width=") ; self.put_in_dquotes(`c.page_width`)
	self.put(" tangle_bat=") ; self.put_dquoted_bool(c.tangle_batch_flag)
	self.put(" untangle_bat=") ; self.put_dquoted_bool(c.untangle_batch_flag)
	self.put(" output_doc_chunks=") ; self.put_dquoted_bool(c.output_doc_flag)
	self.put(" use_header_flag=") ; self.put_dquoted_bool(c.use_header_flag)
	self.put(" defaultTargetLanguage=") ; self.put_in_dquotes(language) # 10/11/02: fix reversion.

self.put("&gt;") ; self.put_nl()
# New in version 0.16
&lt;&lt; put default directory &gt;&gt;</t>
<t tx="T776">if config.configsExist:
	pass # Has been done earlier.
elif len(c.tangle_directory) &gt; 0:
	self.put_tab()
	self.put("&lt;defaultDirectory&gt;")
	self.putEscapedString(c.tangle_directory)
	self.put("&lt;/defaultDirectory&gt;")
	self.put_nl()</t>
<t tx="T777">def putProlog (self):

	a = app() ; c = self.commands ; config = a.config

	&lt;&lt; Put the &lt;?xml...?&gt; line &gt;&gt;
	&lt;&lt; Put the optional &lt;?xml-stylesheet...?&gt; line &gt;&gt;

	self.put("&lt;leo_file&gt;") ; self.put_nl()</t>
<t tx="T778"># 1/22/03: use self.leo_file_encoding encoding.
self.put(a.prolog_prefix_string)
self.put_dquote() ; self.put(self.leo_file_encoding) ; self.put_dquote()
self.put(a.prolog_postfix_string) ; self.put_nl()</t>
<t tx="T779">if config.stylesheet or c.frame.stylesheet:
	
	# The stylesheet in the .leo file takes precedence over the default stylesheet.
	if c.frame.stylesheet:
		s = c.frame.stylesheet
	else:
		s = config.stylesheet
		
	tag = "&lt;?xml-stylesheet "
	# print "writing:", tag + s + "?&gt;"
	self.put(tag) ; self.put(s) ; self.put("?&gt;") ; self.put_nl()
</t>
<t tx="T780">def putPostlog (self):

	self.put("&lt;/leo_file&gt;") ; self.put_nl()</t>
<t tx="T781">def putTnodes (self):
	
	"""Puts all tnodes as required for copy or save commands"""

	c=self.commands
	if self.usingClipboard: # write the current tree.
		v = c.currentVnode() ; after = v.nodeAfterTree()
	else: # write everything
		v = c.rootVnode() ; after = None

	self.put("&lt;tnodes&gt;") ; self.put_nl()
	&lt;&lt; write only those tnodes that were referenced &gt;&gt;
	self.put("&lt;/tnodes&gt;") ; self.put_nl()</t>
<t tx="T782"># Populate tnodes
tnodes = {}
while v and v != after:
	index = v.t.fileIndex
	if index &gt; 0 and not tnodes.has_key(index):
		tnodes[index] = v.t
	v = v.threadNext()

# Put all tnodes in index order.
keys = tnodes.keys() ; keys.sort()
for index in keys:
	t = tnodes[index]
	assert(t)
	# Write only those tnodes whose vnodes were written.
	if t.isVisited(): self.putTnode(t)</t>
<t tx="T783">def putTnode (self,t):
	
	# if self.usingClipboard: trace(t.fileIndex)

	self.put("&lt;t")
	self.put(" tx=") ; self.put_in_dquotes("T" + `t.fileIndex`)
	self.put("&gt;")

	if t.bodyString and len(t.bodyString) &gt; 0:
		self.putEscapedString(t.bodyString)

	self.put("&lt;/t&gt;") ; self.put_nl()</t>
<t tx="T784">@ This method puts all vnodes by starting the recursion.  putVnode will write all vnodes in the order in which they appear in the outline.
@c
def putVnodes (self):

	c=self.commands
	c.clearAllVisited()

	self.put("&lt;vnodes&gt;") ; self.put_nl()
	if self.usingClipboard:
		self.putVnode(
			c.currentVnode(), # Write only current tree.
			None) # Don't write top vnode status bit.
	else: 
		v = c.rootVnode()
		while v:
			self.putVnode(
				v, # Write the next top-level node.
				c.tree.topVnode) # Write the top-vnode status bit.
			v = v.next()
	self.put("&lt;/vnodes&gt;") ; self.put_nl()</t>
<t tx="T785">@ This writes full headline and body text for all vnodes, even orphan and @ignored nodes.  This allows all Leo outlines to be used as backup files.
@c

def putVnode (self,v,topVnode):

	c = self.commands
	self.put("&lt;v")
	&lt;&lt; Put tnode index if this vnode has body text &gt;&gt;
	&lt;&lt; Put attribute bits &gt;&gt;
	self.put("&gt;")
	&lt;&lt; write the head text &gt;&gt;
	child = v.firstChild()
	if child:
		self.put_nl()
		while child:
			self.putVnode(child,topVnode)
			child = child.next()
	self.put("&lt;/v&gt;") ; self.put_nl()</t>
<t tx="T786">t = v.t
if t and (t.hasBody() or len(v.t.joinList) &gt; 0):
	if t.fileIndex &gt; 0:
		self.put(" t=") ; self.put_in_dquotes("T" + `t.fileIndex`)
		v.t.setVisited() # Indicate we wrote the body text.
	else:
		es("error writing file(bad vnode)!")
		es("try using the Save To command")</t>
<t tx="T787"># Dummy vnodes carry all attributes.
current = c.currentVnode()
top = topVnode
if ( v.isCloned() or v.isExpanded() or v.isMarked() or
	v == current or v == top ):
	self.put(" a=") ; self.put_dquote()
	if v.isCloned(): self.put("C")
	if v.isExpanded(): self.put("E")
	if v.isMarked(): self.put("M")
	if v.isOrphan(): self.put("O")
	if v == top: self.put("T")
	if v == current: self.put("V")
	self.put_dquote()</t>
<t tx="T788">headString = v.headString()
if len(headString) &gt; 0:
	self.put("&lt;vh&gt;")
	self.putEscapedString(headString)
	self.put("&lt;/vh&gt;")</t>
<t tx="T789">def save(self,fileName):

	c = self.commands ; v = c.currentVnode()

	if not doHook("save1",c=c,v=v,fileName=fileName):
		c.beginUpdate()
		c.endEditing()# Set the current headline text.
		self.compactFileIndices()
		self.setDefaultDirectoryForNewFiles(fileName)
		if self.write_LEO_file(fileName,false): # outlineOnlyFlag
			c.setChanged(false) # Clears all dirty bits.
			es("saved: " + shortFileName(fileName))
			if app().config.save_clears_undo_buffer:
				es("clearing undo")
				c.undoer.clearUndoState()
		c.endUpdate()
	doHook("save2",c=c,v=v,fileName=fileName)</t>
<t tx="T790">def saveAs(self,fileName):

	c = self.commands ; v = c.currentVnode()

	if not doHook("save1",c=c,v=v,fileName=fileName):
		c.beginUpdate()
		c.endEditing() # Set the current headline text.
		self.compactFileIndices()
		self.setDefaultDirectoryForNewFiles(fileName)
		if self.write_LEO_file(fileName,false): # outlineOnlyFlag
			c.setChanged(false) # Clears all dirty bits.
			es("saved: " + shortFileName(fileName))
		c.endUpdate()
	doHook("save2",c=c,v=v,fileName=fileName)
</t>
<t tx="T791">def saveTo (self,fileName):

	c = self.commands ; v = c.currentVnode()

	if not doHook("save1",c=c,v=v,fileName=fileName):
		c.beginUpdate()
		c.endEditing()# Set the current headline text.
		self.compactFileIndices()
		self.setDefaultDirectoryForNewFiles(fileName)
		if self.write_LEO_file(fileName,false): # outlineOnlyFlag
			es("saved: " + shortFileName(fileName))
		c.endUpdate()
	doHook("save2",c=c,v=v,fileName=fileName)
</t>
<t tx="T792">def setDefaultDirectoryForNewFiles (self,fileName):
	
	"""Set c.openDirectory for new files for the benefit of leoAtFile.scanAllDirectives."""
	
	c = self.commands

	if not c.openDirectory or len(c.openDirectory) == 0:
		dir = os.path.dirname(fileName)
		if len(dir) &gt; 0 and os.path.isabs(dir) and os.path.exists(dir):
			c.openDirectory = dir</t>
<t tx="T793"># Surprisingly, this is a time critical routine.

def xmlEscape(self,s):

	assert(s and len(s) &gt; 0) # check is made in putEscapedString
	s = string.replace(s, '\r', '')
	s = string.replace(s, '&amp;', "&amp;amp;")
	s = string.replace(s, '&lt;', "&amp;lt;")
	s = string.replace(s, '&gt;', "&amp;gt;")
	return s</t>
<t tx="T794">def writeAtFileNodes (self):

	self.commands.atFileCommands.writeAll(writeAtFileNodesFlag=true)</t>
<t tx="T795">def writeDirtyAtFileNodes (self): # fileCommands

	"""The Write Dirty @file Nodes command"""

	self.commands.atFileCommands.writeAll(writeDirtyAtFileNodesFlag=true)</t>
<t tx="T796">def writeMissingAtFileNodes (self):

	c = self.commands ; v = c.currentVnode()
	if v:
		at = c.atFileCommands
		at.writeMissing(v)</t>
<t tx="T797">def writeOutlineOnly (self):

	c=self.commands
	c.endEditing()
	self.compactFileIndices()
	self.write_LEO_file(self.mFileName,true) # outlineOnlyFlag</t>
<t tx="T798">def write_LEO_file(self,fileName,outlineOnlyFlag):

	c=self.commands ; config = app().config

	if not outlineOnlyFlag:
		try:
			# Leo2: write all @file nodes and set orphan bits.
			at = c.atFileCommands
			at.writeAll()
		except:
			es_error("exception writing derived files")
			es_exception()
			return false
			
	if self.read_only:
		es_error("read only: " + fileName)
		return false

	try:
		&lt;&lt; create backup file &gt;&gt;
		self.mFileName = fileName
		self.outputFile = open(fileName, 'wb') # 9/18/02
		if not self.outputFile:
			es("can not open " + fileName)
			&lt;&lt; delete backup file &gt;&gt;
			return false
		
		# 8/6/02: Update leoConfig.txt completely here.
		c.setIvarsFromFind()
		config.setConfigFindIvars(c)
		c.setIvarsFromPrefs()
		config.setCommandsIvars(c)
		config.update()
		
		self.putProlog()
		self.putHeader()
		self.putGlobals()
		self.putPrefs()
		self.putFindSettings()
		self.putVnodes()
		self.putTnodes()
		self.putPostlog()
		# raise BadLeoFile # testing
	except:
		es("exception writing: " + fileName)
		es_exception() 
		if self.outputFile:
			try:
				self.outputFile.close()
				self.outputFile = None
			except:
				es("exception closing: " + fileName)
				es_exception()
		&lt;&lt; erase filename and rename backupName to fileName &gt;&gt;
		return false

	if self.outputFile:
		try:
			self.outputFile.close()
			self.outputFile = None
		except:
			es("exception closing: " + fileName)
			es_exception()
		&lt;&lt; delete backup file &gt;&gt;
		return true
	else: # This probably will never happen because errors should raise exceptions.
		&lt;&lt; erase filename and rename backupName to fileName &gt;&gt;
		return false</t>
<t tx="T799"># rename fileName to fileName.bak if fileName exists.
if os.path.exists(fileName):
	try:
		backupName = os.path.join(app().loadDir,fileName)
		backupName = fileName + ".bak"
		if os.path.exists(backupName):
			os.unlink(backupName)
		# os.rename(fileName,backupName)
		utils_rename(fileName,backupName)
	except:
		es("exception creating " + backupName)
		es_exception()
		backupName = None
else:
	backupName = None</t>
<t tx="T800">if backupName and os.path.exists(backupName):
	try:
		os.unlink(backupName)
	except:
		es("exception deleting " + backupName)
		es_exception()
</t>
<t tx="T801">es("error writing " + fileName)

if fileName and os.path.exists(fileName):
	try:
		os.unlink(fileName)
	except:
		es("exception deleting " + fileName)
		es_exception()
		
if backupName:
	es("restoring " + fileName + " from " + backupName)
	try:
		# os.rename(backupName, fileName)
		utils_rename(backupName, fileName)
	except:
		es("exception renaming " + backupName + " to " + fileName)
		es_exception()
</t>
<t tx="T802">@language python

&lt;&lt; About the vnode and tnode classes &gt;&gt;
&lt;&lt; About clones &gt;&gt;

from leoGlobals import *
import types

@others</t>
<t tx="T803">@ This is the design document for clones in Leo. It covers all important aspects of clones. Clones are inherently complex, and this paper will include several different definitions of clones and related concepts.

The following is a definition of clones from the user's point of view.

Definition 1

A clone node is a copy of a node that changes when the original changes. Changes to the children, grandchildren, etc. of a node are simultaneously made to the corresponding nodes contained in all cloned nodes. Clones are marked by a small clone arrow by its leader character.

As we shall see, this definition glosses over a number of complications. Note that all cloned nodes (including the original node) are equivalent. There is no such thing as a "master" node from which all clones are derived. When the penultimate cloned node is deleted, the remaining node becomes an ordinary node again.

Internally, the clone arrow is represented by a clone bit in the status field of the vnode. The Clone Node command sets the clone bits of the original and cloned vnodes when it creates the clone. Setting and clearing clone bits properly when nodes are inserted, deleted or moved, is non-trivial. We need the following machinery to do the job properly.

Two vnodes are joined if a) they share the same tnode (body text) and b) changes to any subtree of either joined vnodes are made to the corresponding nodes in all joined nodes.  For example, Definition 1 defines clones as joined nodes that are marked with a clone arrow.  Leo links all vnodes joined to each other in a circular list, called the join list. For any vnode n, let J(n) denote the join list of n, that is, the set of all vnodes joined to n. Again, maintaining the join lists in an outline is non-trivial.

The concept of structurally similar nodes provides an effective way of determining when two joined nodes should also have their cloned bit set.  Two joined nodes are structurally similar if a) their parents are distinct but joined and b) they are both the nth child of their (distinct) parents.  We can define cloned nodes using the concept of structurally similar nodes as follows:

Definition 2

Clones are joined vnodes such that at least two of the vnodes of J(n) are not structurally similar to each other. Non-cloned vnodes are vnodes such that all of the vnodes of J(n) are structurally similar. In particular, n is a non-cloned vnode if J(n) is empty.

Leo ensures that definitions 1 and 2 are consistent. Definition 1 says that changes to the children, grandchildren, etc. of a node are simultaneously made to the corresponding nodes contained in all cloned nodes. Making "corresponding changes" to the non-cloned descendents of all cloned nodes insures that the non-cloned joined nodes will be structurally similar. On the other hand, cloned nodes are never structurally similar. They are created as siblings, so they have the same parent with different "child indices."  To see how this works in practice, let's look at some examples.

Example 1

+ root
	+ a' (1)
	+ a' (2)

This example shows the simplest possible clone. A prime (') indicates a cloned node.  Node a in position (1) has just been cloned to produce a' in position (2). Clearly, these two cloned nodes are not structurally similar because their parents are not distinct and they occupy different positions relative to their common parent.

Example 2

If we add a node b to either a' node we get the following tree:

+ root
	+ a'
		+ b
	+ a'
		+ b

The b nodes are structurally similar because the a' nodes are joined and each b node is the first child of its parent.

Example 3

If we now clone either b, we will get:

+ root
	+ a'
		+ b' (1)
		+ b' (2)
	+ a'
		+ b' (1)
		+ b' (2)

All b' nodes must be clones because the nodes marked (1) are not structurally similar to the nodes marked (2).

Dependent nodes are nodes created or destroyed when corresponding linked nodes are created or destroyed in another tree. For example, going from example 1 to example 2 above, adding node b to either node a' causes another (dependent) node to be created as the ancestor of the other node a'. Similarly, going from example 2 to example 1, deleting node b from either node a' causes the other (dependent) node b to be deleted from the other node a'.  Cloned nodes may also be dependent nodes. In Example 3, all the b' nodes are dependent on any of the other b' nodes.

We can now give simple rules for inserting and deleting dependent vnodes when other vnodes are created, moved or destroyed. For the purposes of this discussion, moving a node is handled exactly like deleting the node then inserting the node; we need not consider moving nodes further.  We insert a new node n as the nth child of a parent node p as follows. We insert n, then for every node pi linked to p, we insert a dependent node ni as the nth child of pi. Each ni is linked to n. Clearly, each ni is structurally similar to n.  Similarly, it is easy to delete a node n that is the nth child of a parent node p. We delete each dependent node ni that is the nth child of any node pi linked to p. We then delete n.  When inserting or deleting any vnode n we must update its join list, J(n). Updating the join list is easy because the join list is circular: the entire list is accessible from any of its members.

Inserting or deleting nodes can cause the clone bits of all joined nodes to change in non-trivial ways. To see the problems that can arise, consider deleting any of the b' nodes from Example 3. We would be left with the tree in Example 2. There are two remaining b nodes, each with the clone bit set. Unless we know that both b nodes are structurally similar, there would be no way to conclude that we should clear the clone bits in each node. In order to update clone links properly we could examine many special cases, but there is an easier way. Because of definition 2, we can define a shouldBeCloned function that checks J(n) to see whether all nodes of J(n) are structurally similar.

Leo's XML file format does not contain join lists. This makes it easy to change a Leo file "by hand." If join lists were a part of the file, as they are in the Mac version of Leo, corrupting a join list would corrupt the entire file. It is easy to recreate the join lists when reading a file using a dedicated field in the tnode.  This field is the head of a list of all vnodes that points to the tnode. After reading all nodes, Leo creates this list with one pass through the vnodes.  Leo then converts each list to a circular list with one additional pass through the tnodes.
</t>
<t tx="T804">@ The vnode and tnode classes represent most of the data contained in the outline. These classes are Leo's fundamental Model classes.

A vnode (visual node) represents a headline at a particular location on the screen. When a headline is cloned, vnodes must be copied. vnodes persist even if they are not drawn on the screen. Commanders call vnode routines to insert, delete and move headlines.

The vnode contains data associated with a headline, except the body text data which is contained in tnodes. A vnode contains headline text, a link to its tnode and other information. In leo.py, vnodes contain structure links: parent, firstChild, next and back ivars. To insert, delete, move or clone a vnode the vnode class just alters those links. The Commands class calls the leoTree class to redraw the outline pane whenever it changes. The leoTree class knows about these structure links; in effect, the leoTree and vnode classes work together. The implementation of vnodes is quite different in the Borland version of Leo. This does not affect the rest of the Leo. Indeed, vnodes are designed to shield Leo from such implementation details.

A tnode, (text node) represents body text: a tnode is shared by all vnodes that are clones of each other. In other words, tnodes are the unit of sharing of body text. The tnode class is more private than the vnode class. Most commanders deal only with vnodes, though there are exceptions.

Because leo.py has unlimited Undo commands, vnodes and tnodes can be deleted only when the window containing them is closed. Nodes are deleted indirectly.

Leo uses several kinds of node indices. Leo's XML file format uses tnode indices to indicate which tnodes (t elements) belong to which vnodes (v elements). Such indices are required. Even if we duplicated the body text of shared tnodes within the file, the file format would still need an unambiguous way to denote that tnodes are shared.

Present versions of Leo recompute these tnodes indices whenever Leo writes any .leo file. Earlier versions of Leo remembered tnode indices and rewrote the same indices whenever possible. Those versions of Leo recomputed indices when executing the Save As and Save To commands, so using these commands was a way of "compacting" indices. The main reason for not wanting to change tnode indices in .leo files was to reduce the number of changes reported by CVS and other Source Code Control Systems. I finally abandoned this goal in the interest of simplifying the code. Also, CVS will likely report many differences between two versions of the same .leo file, regardless of whether tnode indices are conserved.

A second kind of node index is the clone index used in @+node sentinels in files derived from @file trees. As with indices in .leo files, indices in derived files are required so that Leo can know unambiguously which nodes are cloned to each other.

It is imperative that clone indices be computed correctly, that is, that tnode @+node sentinels have the same index if and only if the corresponding vnodes are cloned. Early versions of leo.py had several bugs involving these clone indices. Such bugs are extremely serious because they corrupt the derived file and cause read errors when Leo reads the @file tree. Leo must guarantee that clone indices are always recomputed properly. This is not as simple as it might appear at first. In particular, Leo's commands must ensure that @file trees are marked dirty whenever any changed is made that affects cloned nodes within the tree. For example, a change made outside any @file tree may make several @file trees dirty if the change is made to a node with clones in those @file trees.
</t>
<t tx="T805">class baseTnode:
	"""The base class of the tnode class."""
	&lt;&lt; tnode constants &gt;&gt;
	@others
	
class tnode (baseTnode):
	"""A class that implements tnodes."""
	pass</t>
<t tx="T806">dirtyBit =		0x01
richTextBit =	0x02 # Determines whether we use &lt;bt&gt; or &lt;btr&gt; tags.
visitedBit =	0x04</t>
<t tx="T807"># All params have defaults, so t = tnode() is valid.

def __init__ (self,index=0,bodyString=None,headString=None):

	a = app()
	self.bodyString = choose(bodyString, bodyString, "")
	self.statusBits = 0 # status bits
	self.selectionStart = 0 # The start of the selected body text.
	self.selectionLength = 0 # The length of the selected body text.
	self.insertSpot = None # Location of previous insert point.
	self.scrollBarSpot = None # Previous value of scrollbar position.
	# For Pre-3.12 files.  These must always exist.
	self.fileIndex = index # The immutable file index for self tnode.
	self.cloneIndex = 0 # Zero for @file nodes
	# New in 3.12
	self.joinList = [] # vnodes on the same joinlist are updated together.
	self.headString = headString
</t>
<t tx="T808"></t>
<t tx="T809">def hasBody (self):

	return self.bodyString and len(self.bodyString) &gt; 0</t>
<t tx="T810">def loadBodyPaneFromTnode(self, body):

	s = self.bodyString
	if s and len(s) &gt; 0:
		body.delete(1,"end")
		body.insert(1,s)
	else:
		body.delete(1,"end")</t>
<t tx="T811"></t>
<t tx="T812">def isDirty (self):

	return (self.statusBits &amp; self.dirtyBit) != 0</t>
<t tx="T813">def isRichTextBit (self):

	return (self.statusBits &amp; self.richTextBit) != 0</t>
<t tx="T814">def isVisited (self):

	return (self.statusBits &amp; self.visitedBit) != 0</t>
<t tx="T815"></t>
<t tx="T816"></t>
<t tx="T817">def saveBodyPaneToTnode (self,body): # No need for an encoding param.

	self.setTnodeText(body.GetValue()) # 1/20/03

	# Set the selection.
	i,j = body.GetSelection()
	if i &gt; j:
		i,j = j,i
	self.selectionStart = i
	self.selectionLength = j - i
</t>
<t tx="T818"># This sets the text in the tnode from the given string.

def setTnodeText (self,s,encoding="utf-8"):
	
	s = toUnicode(s,encoding,reportErrors=true)
	self.bodyString = s
</t>
<t tx="T819">def setSelection (self, start, length):

	self.selectionStart = start
	self.selectionLength = length</t>
<t tx="T820"></t>
<t tx="T821">def clearDirty (self):

	self.statusBits &amp;= ~ self.dirtyBit</t>
<t tx="T822">def clearRichTextBit (self):

	self.statusBits &amp;= ~ self.richTextBit</t>
<t tx="T823">def clearVisited (self):

	self.statusBits &amp;= ~ self.visitedBit</t>
<t tx="T824">def setDirty (self):

	self.statusBits |= self.dirtyBit</t>
<t tx="T825">def setRichTextBit (self):

	self.statusBits |= self.richTextBit</t>
<t tx="T826">def setVisited (self):

	self.statusBits |= self.visitedBit</t>
<t tx="T827">def setCloneIndex (self, index):

	self.cloneIndex = index</t>
<t tx="T828">def setFileIndex (self, index):

	self.fileIndex = index</t>
<t tx="T829">class baseVnode:
	"""The base class of the vnode class."""
	&lt;&lt; vnode constants &gt;&gt;
	@others
	
class vnode (baseVnode):
	"""A class that implements vnodes."""
	pass</t>
<t tx="T830"># Define the meaning of status bits in new vnodes.

# Archived...
clonedBit	  = 0x01 # true: vnode has clone mark.
# not used	 = 0x02
expandedBit = 0x04 # true: vnode is expanded.
markedBit	  = 0x08 # true: vnode is marked
orphanBit	  = 0x10 # true: vnode saved in .leo file, not derived file.
selectedBit = 0x20 # true: vnode is current vnode.
topBit		    = 0x40 # true: vnode was top vnode when saved.

# Not archived...
dirtyBit    =	0x060
richTextBit =	0x080 # Determines whether we use &lt;bt&gt; or &lt;btr&gt; tags.
visitedBit	 = 0x100
</t>
<t tx="T831"></t>
<t tx="T832">if 0: # not used
	def __cmp__(self,other):
		
		trace(`self` + "," + `other`)
		return not (self is other) # Must return 0, 1 or -1</t>
<t tx="T833">def __init__ (self,commands,t):

	a = app()
	assert(t)
	
	# commands may be None for testing.
	# assert(commands)

	&lt;&lt; initialize vnode data members &gt;&gt;
</t>
<t tx="T834">self.commands = commands # The commander for this vnode.
self.t = t # The tnode, i.e., the body text.
self.statusBits = 0 # status bits

# Structure links
self.mParent = self.mFirstChild = self.mNext = self.mBack = None

# To be moved to vxnodes...

self.iconVal = -1 # The icon index.  -1 forces an update of icon.
self.iconx, self.icony = 0,0 # Coords of icon so icon can be redrawn separately.</t>
<t tx="T835">def __repr__ (self):
	
	if self.t:
		return "&lt;vnode %d:%s&gt;" % (id(self),`self.t.headString`)
	else:
		return "&lt;vnode %d:NULL tnode&gt;" % (id(self))
		
__str__ = __repr__
</t>
<t tx="T836">@ These callbacks are vnode methods so we can pass the vnode back to the tree class.
</t>
<t tx="T837"># Called when the box is clicked.

def OnBoxClick(self,event=None):

	try:
		v = self ; c = v.commands
		if not doHook("boxclick1",c=c,v=v,event=event):
			self.commands.tree.OnBoxClick(self)
		doHook("boxclick2",c=c,v=v,event=event)
	except:
		es_event_exception("boxclick")</t>
<t tx="T838">def OnDrag(self,event=None):
	
	# trace()
	
	try:
		v = self ; c = v.commands
		if c.frame.tree.dragging:
			if not doHook("dragging1",c=c,v=v,event=event):
				self.commands.tree.OnDrag(self,event)
			doHook("dragging2",c=c,v=v,event=event)
		else:
			if not doHook("drag1",c=c,v=v,event=event):
				self.commands.tree.OnDrag(self,event)
			doHook("drag2",c=c,v=v,event=event)
	except:
		es_event_exception("drag")</t>
<t tx="T839">def OnEndDrag(self,event=None):
	
	"""Vnode end-drag handler."""
	
	# trace()

	try:
		v = self ; c = v.commands
		# 7/10/03: Always call tree.OnEndDrag, regardless of state.
		if not doHook("enddrag1",c=c,v=v,event=event):
			self.commands.tree.OnEndDrag(self,event)
		doHook("enddrag2",c=c,v=v,event=event)
	except:
		es_event_exception("enddrag")</t>
<t tx="T840">def OnHeadlineClick(self,event=None):
	try:
		v = self ; c = v.commands
		if not doHook("headclick1",c=c,v=v,event=event):
			self.commands.tree.OnActivate(self)
		doHook("headclick2",c=c,v=v,event=event)
	except:
		es_event_exception("headclick")
	
def OnHeadlineRightClick(self,event=None):
	try:
		v = self ; c = v.commands
		if not doHook("headrclick1",c=c,v=v,event=event):
			self.commands.tree.OnActivate(self)
			self.commands.tree.OnPopup(self,event)
		doHook("headrclick2",c=c,v=v,event=event)
	except:
		es_event_exception("headrclick")</t>
<t tx="T841">def OnHeadlineKey (self,event=None):

	try:
		v = self ; c = v.commands
		if not doHook("headkey1",c=c,v=v,event=event):
			self.commands.tree.OnHeadlineKey(self,event)
		doHook("headkey2",c=c,v=v,event=event)
	except:
		es_event_exception("headkey")</t>
<t tx="T842">def OnHyperLinkControlClick (self,event):

	try:
		v = self ; c = v.commands
		if not doHook("hypercclick1",c=c,v=v,event=event):
			c.beginUpdate()
			c.selectVnode(v)
			c.endUpdate()
			c.body.mark_set("insert","1.0")
		doHook("hypercclick2",c=c,v=v,event=event)
	except:
		es_event_exception("hypercclick")</t>
<t tx="T843">def OnHyperLinkEnter (self,event=None):

	try:
		v = self ; c = v.commands
		if not doHook("hyperenter1",c=c,v=v,event=event):
			if 0: # This works, and isn't very useful.
				c.body.tag_config(v.tagName,background="green")
		doHook("hyperenter2",c=c,v=v,event=event)
	except:
		es_event_exception("hyperenter")</t>
<t tx="T844">def OnHyperLinkLeave (self,event=None):

	try:
		v = self ; c = v.commands
		if not doHook("hyperleave1",c=c,v=v,event=event):
			if 0: # This works, and isn't very useful.
				c.body.tag_config(v.tagName,background="white")
		doHook("hyperleave2",c=c,v=v,event=event)
	except:
		es_event_exception("hyperleave")</t>
<t tx="T845">def OnIconClick(self,event=None):
	try:
		v = self ; c = v.commands
		if not doHook("iconclick1",c=c,v=v,event=event):
			self.commands.tree.OnIconClick(self,event)
		doHook("iconclick2",c=c,v=v,event=event)
	except:
		es_event_exception("iconclick")
	
def OnIconRightClick(self,event=None):
	try:
		v = self ; c = v.commands
		if not doHook("iconrclick1",c=c,v=v,event=event):
			self.commands.tree.OnIconRightClick(self,event)
		doHook("iconrclick2",c=c,v=v,event=event)
	except:
		es_event_exception("iconrclick")
</t>
<t tx="T846">def OnIconDoubleClick(self,event=None):

	try:
		v = self ; c = v.commands
		if not doHook("icondclick1",c=c,v=v,event=event):
			self.commands.tree.OnIconDoubleClick(self)
		doHook("icondclick2",c=c,v=v,event=event)
	except:
		es_event_exception("icondclick")
</t>
<t tx="T847"></t>
<t tx="T848"># 12/03/02: We now handle @file options here.

def afterHeadlineMatch(self,s):
	
	h = self.headString()

	if s != "@file" and match_word(h,0,s):
		# No options are valid.
		return string.strip(h[len(s):])
	elif match(h,0,"@file"):
		i,atFileType,junk = scanAtFileOptions(h)
		if s == atFileType:
			# print "s,h:",s,h
			return string.strip(h[i:])
		else: return ""
	else: return ""
</t>
<t tx="T849">@ Returns the filename following @file or @rawfile, in the receivers's headline, or the empty string if the receiver is not an @file node.
@c

def atFileNodeName (self):
	return self.afterHeadlineMatch("@file")
	
def atNoSentinelsFileNodeName (self):
	return self.afterHeadlineMatch("@nosentinelsfile")
	
def atRawFileNodeName (self):
	return self.afterHeadlineMatch("@rawfile")
	
def atSilentFileNodeName (self):
	return self.afterHeadlineMatch("@silentfile")
</t>
<t tx="T850"># Returns true if the receiver's headline starts with @file.
def isAtFileNode (self):
	s = self.atFileNodeName()
	return len(s) &gt; 0
	
# Returns true if the receiver's headline starts with @rawfile.
def isAtNoSentinelsFileNode (self):
	s = self.atNoSentinelsFileNodeName()
	return len(s) &gt; 0
	
# Returns true if the receiver's headline starts with @rawfile.
def isAtRawFileNode (self):
	s = self.atRawFileNodeName()
	return len(s) &gt; 0

# Returns true if the receiver's headline starts with @silentfile.
def isAtSilentFileNode (self):
	s = self.atSilentFileNodeName()
	return len(s) &gt; 0
</t>
<t tx="T851">def isAnyAtFileNode (self):

	return (
		self.isAtFileNode() or
		self.isAtNoSentinelsFileNode() or
		self.isAtRawFileNode() or
		self.isAtSilentFileNode())
		
def anyAtFileNodeName (self):

	if self.isAtFileNode():
		return self.atFileNodeName()
	elif self.isAtNoSentinelsFileNode():
		return self.atNoSentinelsFileNodeName()
	elif self.isAtRawFileNode():
		return self.atRawFileNodeName()
	elif self.isAtSilentFileNode():
		return self.atSilentFileNodeName()
	else:
		return ""
</t>
<t tx="T852">@ Returns true if the receiver contains @ignore in its body at the start of a line.
@c

def isAtIgnoreNode (self):

	flag, i = is_special(self.t.bodyString, 0, "@ignore")
	return flag</t>
<t tx="T853">@ Returns true if the receiver contains @others in its body at the start of a line.
@c

def isAtOthersNode (self):

	flag, i = is_special(self.t.bodyString,0,"@others")
	return flag</t>
<t tx="T854">@ Returns true if the headline matches the pattern ignoring whitespace and case.  The headline may contain characters following the successfully matched pattern.
@c

def matchHeadline (self,pattern):

	h = string.lower(self.headString())
	h = string.replace(h,' ','')
	h = string.replace(h,'\t','')

	p = string.lower(pattern)
	p = string.replace(p,' ','')
	p = string.replace(p,'\t','')

	# ignore characters in the headline following the match
	return p == h[0:len(p)]</t>
<t tx="T855"></t>
<t tx="T856"># Converts the outline to a string in "MORE" format

def convertTreeToString (self):

	v = self
	level1 = v.level()
	after = v.nodeAfterTree()
	s = ""
	while v and v != after:
		s += v.moreHead(level1) + "\n"
		body = v.moreBody()
		if len(body) &gt; 0:
			s += body + "\n"
		v = v.threadNext()
	return s</t>
<t tx="T857"># Returns the headline string in MORE format.

def moreHead (self, firstLevel,useVerticalBar=false):

	v = self
	level = self.level() - firstLevel
	if level &gt; 0: s = "\t" * level
	else: s = ""
	s += choose(v.hasChildren(), "+ ", "- ")
	s += v.headString()
	return s</t>
<t tx="T858">@ Returns the body string in MORE format.  It inserts a backslash before any leading plus, minus or backslash.

+ test line
- test line
\ test line
test line +
test line -
test line \

More lines...
@c

def moreBody (self):

	v = self ; list = []
	
	if 1: # new code: only escape the first non-blank character of the line.
		s =  v.t.bodyString ; result = []
		lines = string.split(s,'\n')
		for s in lines:
			i = skip_ws(s,0)
			if i &lt; len(s):
				ch = s[i]
				if ch == '+' or ch == '-' or ch == '\\':
					s = s[:i] + '\\' + s[i:]
			result.append(s)
		return string.join(result,'\n')

	else: # pre 3.1 code.
		for ch in v.t.bodyString:
			if ch == '+' or ch == '-' or ch == '\\':
				list.append('\\')
			list.append(ch)
		return string.join(list,'')</t>
<t tx="T859"></t>
<t tx="T860"></t>
<t tx="T861"># childIndex and nthChild are zero-based.

def childIndex (self):

	parent=self.parent()
	if not parent: return 0

	child = parent.firstChild()
	n = 0
	while child:
		if child == self: return n
		n += 1 ; child = child.next()
	assert(false)</t>
<t tx="T862"># Compatibility routine for scripts

def firstChild (self):

	return self.mFirstChild</t>
<t tx="T863">def hasChildren (self):

	return self.firstChild() != None</t>
<t tx="T864"># Compatibility routine for scripts

def lastChild (self):

	child = self.firstChild()
	while child and child.next():
		child = child.next()
	return child</t>
<t tx="T865"># childIndex and nthChild are zero-based.

def nthChild (self, n):

	child = self.firstChild()
	if not child: return None
	while n &gt; 0 and child:
		n -= 1
		child = child.next()
	return child</t>
<t tx="T866">def numberOfChildren (self):

	n = 0
	child = self.firstChild()
	while child:
		n += 1
		child = child.next()
	return n</t>
<t tx="T867"></t>
<t tx="T868">def isCloned (self):

	return ( self.statusBits &amp; vnode.clonedBit ) != 0</t>
<t tx="T869">def isDirty (self):

	return self.t.isDirty()</t>
<t tx="T870">def isExpanded (self):

	return ( self.statusBits &amp; self.expandedBit ) != 0</t>
<t tx="T871">def isMarked (self):

	return ( self.statusBits &amp; vnode.markedBit ) != 0</t>
<t tx="T872">def isOrphan (self):

	return ( self.statusBits &amp; vnode.orphanBit ) != 0</t>
<t tx="T873">def isSelected (self):

	return ( self.statusBits &amp; vnode.selectedBit ) != 0</t>
<t tx="T874">def isTopBitSet (self):

	return ( self.statusBits &amp; self.topBit ) != 0</t>
<t tx="T875"># Returns true if all parents are expanded.

def isVisible (self):

	v = self.parent()
	while v:
		if not v.isExpanded():
			return false
		v = v.parent()
	return true</t>
<t tx="T876">def isVisited (self):

	return ( self.statusBits &amp; vnode.visitedBit ) != 0</t>
<t tx="T877">def status (self):

	return self.statusBits</t>
<t tx="T878"># Compatibility routine for scripts

def bodyString (self):

	return self.t.bodyString</t>
<t tx="T879"># Compatibility routine for scripts

def currentVnode (self):

	return self.commands.tree.currentVnode</t>
<t tx="T880">def edit_text (self):
	
	return self.commands.tree.edit_text_dict.get(self)</t>
<t tx="T881"># Compatibility routine for scripts

def findRoot (self):

	return self.commands.tree.rootVnode
</t>
<t tx="T882">def headString (self):

	if self.t.headString:
		return self.t.headString
	else:
		return ""
		
def cleanHeadString (self):
	
	s = self.headString()
	s = toEncodedString(s,"ascii") # Replaces non-ascii characters by '?'
	return s</t>
<t tx="T883">def isAncestorOf (self, v):

	if not v:
		return false
	v = v.parent()
	while v:
		if v == self:
			return true
		v = v.parent()
	return false</t>
<t tx="T884">def isRoot (self):

	return not self.parent() and not self.back()</t>
<t tx="T885">def exists(self,c):
	
	"""Return true if v exists in c's tree"""
	
	v = self ; c = v.commands
	
	# This code must be fast.
	root = c.rootVnode()
	while v:
		if v == root:
			return true
		p = v.parent()
		if p:
			v = p
		else:
			v = v.back()
		
	return false</t>
<t tx="T886"></t>
<t tx="T887"></t>
<t tx="T888">def appendStringToBody (self,s,encoding="utf-8"):

	if len(s) == 0: return
	body = self.t.bodyString + s
	self.setBodyStringOrPane(body,encoding)
</t>
<t tx="T889">def setBodyStringOrPane (self,s,encoding="utf-8"):

	v = self ; c = v.commands
	if not c or not v: return
	
	s = toUnicode(s,encoding)
	if v == c.currentVnode():
		# This code destoys all tags, so we must recolor.
		c.frame.body.delete("1.0","end")
		c.frame.body.insert("1.0",s) # Replace the body text with s.
		c.recolor()
		
	# Keep the body text in the tnode up-to-date.
	if v.t.bodyString != s:
		v.t.setTnodeText(s)
		v.t.setSelection(0,0)
		v.setDirty()
		if not c.isChanged():
			c.setChanged(true)

setBodyTextOrPane = setBodyStringOrPane # Compatibility with old scripts</t>
<t tx="T890">def setHeadString (self,s,encoding="utf-8"):

	self.initHeadString(s,encoding) # 6/28/03
	self.setDirty()

def initHeadString (self,s,encoding="utf-8"):

	s = toUnicode(s,encoding,reportErrors=true)
	self.t.headString = s
</t>
<t tx="T891"># Compatibility routine for scripts

def setHeadStringOrHeadline (self,s,encoding="utf-8"):

	c = self.commands
	c.endEditing()
	self.setHeadString(s,encoding)
</t>
<t tx="T892">def computeIcon (self):

	val = 0 ; v = self
	if v.t.hasBody(): val += 1
	if v.isMarked(): val += 2
	if v.isCloned(): val += 4
	if v.isDirty(): val += 8
	return val
	
def setIcon (self):

	pass # Compatibility routine for old scripts</t>
<t tx="T893"></t>
<t tx="T894"># Compatibility routine for scripts

def clearAllVisited (self):
	
	self.commands.clearAllVisited()
</t>
<t tx="T895">def clearAllVisitedInTree (self):

	v = self ; c = v.commands
	after = v.nodeAfterTree()
	
	c.beginUpdate()
	while v and v != after:
		v.clearVisited()
		v.t.clearVisited()
		v = v.threadNext()
	c.endUpdate()
</t>
<t tx="T896">def clearClonedBit (self):

	self.statusBits &amp;= ~ self.clonedBit</t>
<t tx="T897">def clearDirty (self):

	v = self
	v.t.clearDirty()

def clearDirtyJoined (self):

	# trace()
	v = self ; c = v.commands
	c.beginUpdate()
	v.t.clearDirty()
	c.endUpdate() # recomputes all icons</t>
<t tx="T898">def clearMarked (self):

	self.statusBits &amp;= ~ self.markedBit
	doHook("clear-mark",c=self.commands,v=self)</t>
<t tx="T899">def clearOrphan (self):

	self.statusBits &amp;= ~ self.orphanBit</t>
<t tx="T900">def clearVisited (self):

	self.statusBits &amp;= ~ self.visitedBit</t>
<t tx="T901">def clearVisitedInTree (self):

	after = self.nodeAfterTree()
	v = self
	while v and v != after:
		v.clearVisited()
		v = v.threadNext()</t>
<t tx="T902">def contract(self):

	self.statusBits &amp;= ~ self.expandedBit

def expand(self):

	self.statusBits |= self.expandedBit

def initExpandedBit (self):

	self.statusBits |= self.expandedBit</t>
<t tx="T903">def initStatus (self, status):

	self.statusBits = status</t>
<t tx="T904">@ This is called from the key-event handler, so we must not force a redraw of the screen here. We avoid redraw in most cases by passing redraw_flag to the caller.

This marks v dirty and all cloned nodes in v's tree.

2/1/03: I don't see how this can possibly be correct.
Why is it needed?? If it is needed, what about undo??
@c
def setAncestorsOfClonedNodesInTreeDirty(self):

	# Look up the tree for an ancestor @file node.
	v = self ; redraw_flag = false
	
	if v == None:
		return redraw_flag
		
	flag = v.setAncestorAtFileNodeDirty()
	if flag: redraw_flag = true
		
	next = v.nodeAfterTree()
	v = v.threadNext()
	while v and v != next:
		if v.isCloned() and not v.isDirty():
			flag = v.setAncestorAtFileNodeDirty()
			if flag: redraw_flag = true
			for v2 in v.t.joinList:
				if v2 != v:
					flag = v2.setAncestorAtFileNodeDirty()
					if flag: redraw_flag = true
		v = v.threadNext()

	return redraw_flag</t>
<t tx="T905">@ This is called from the key-event handler, so we must not force a redraw of the screen here. We avoid redraw in most cases by passing redraw_flag to c.endUpdate().

This is called from v.setDirty, so we avoid further calls to v.setDirty here.  The caller, that is, v.setDirty itself, handles all clones.

@c
def setAncestorAtFileNodeDirty(self):

	# Look up the tree for an ancestor @file node.
	v = self ; c = v.commands
	redraw_flag = false
	c.beginUpdate()
	while v:
		if not v.isDirty() and v.isAnyAtFileNode():
			redraw_flag = true
			v.t.setDirty() # Do not call v.setDirty here!
		v = v.parent()
	c.endUpdate(redraw_flag) # A crucial optimization: does nothing if inside nested begin/endUpdate.
	return redraw_flag # Allow caller to do the same optimization.</t>
<t tx="T906">def setClonedBit (self):

	self.statusBits |= self.clonedBit

def initClonedBit (self, val):

	if val:
		self.statusBits |= self.clonedBit
	else:
		self.statusBits &amp;= ~ self.clonedBit</t>
<t tx="T907">@ v.setDirty now ensures that all cloned nodes are marked dirty and that all ancestor @file nodes are marked dirty.  It is much safer to do it this way.

v.setDirtyDeleted is used only when a node is deleted.  (And why is it even needed????)
@c

def setDirty (self):

	v = self ; c = v.commands
	# trace(`v`)
	changed = false
	c.beginUpdate()
	if not v.t.isDirty():
		v.t.setDirty()
		changed = true
	# This must _always_ be called, even if v is already dirty.
	if v.setAncestorAtFileNodeDirty():
		changed = true
	for v2 in v.t.joinList:
		if v2 != v:
			assert(v2.t.isDirty())
			# Again, must always be called.
			if v2.setAncestorAtFileNodeDirty():
				changed = true
	c.endUpdate(changed)
	return changed
	
def setDirtyDeleted (self):
	
	self.setDirty()
	return
	
	## This code is bizarre and unnecessary.

	v = self ; c = v.commands
	# trace(`v`)
	changed = false
	c.beginUpdate()
	if not v.t.isDirty():
		v.t.setDirty()
		changed = true
	# This must _always_ be called, even if v is already dirty.
	if v.setAncestorsOfClonedNodesInTreeDirty():
		changed = true
	for v2 in v.t.joinList:
		if v2 != v:
			assert(v2.t.isDirty())
			# Again, must always be called.
			if v2.setAncestorsOfClonedNodesInTreeDirty():
				changed = true
	c.endUpdate(changed)
	return changed

def initDirtyBit (self):
	self.t.setDirty()</t>
<t tx="T908">def setMarked (self):

	self.statusBits |= self.markedBit
	doHook("set-mark",c=self.commands,v=self)

def initMarkedBit (self):

	self.statusBits |= self.markedBit</t>
<t tx="T909">def setOrphan (self):

	self.statusBits |= self.orphanBit</t>
<t tx="T910"># This only sets the selected bit.

def setSelected (self):

	self.statusBits |= self.selectedBit</t>
<t tx="T911"># Compatibility routine for scripts

def setVisited (self):

	self.statusBits |= self.visitedBit</t>
<t tx="T912">def setSelection (self, start, length):

	self.t.setSelection ( start, length )</t>
<t tx="T913">def setT (self, t):

	if t != self:
		del self.t
		self.t = t</t>
<t tx="T914">@ This trims trailing blank lines from a node.  It is surprising difficult to do this during Untangle.
@c

def trimTrailingLines (self):

	v = self
	body = v.bodyString()
	# trace(`body`)
	lines = string.split(body,'\n')
	i = len(lines) - 1 ; changed = false
	while i &gt;= 0:
		line = lines[i]
		j = skip_ws(line,0)
		if j + 1 == len(line):
			del lines[i]
			i -= 1 ; changed = true
		else: break
	if changed:
		body = string.join(body,'') + '\n' # Add back one last newline.
		# trace(`body`)
		v.setBodyStringOrPane(body)
		# Don't set the dirty bit: it would just be annoying.</t>
<t tx="T915"></t>
<t tx="T916"># Compatibility routine for scripts

def back (self):

	return self.mBack</t>
<t tx="T917">def lastNode (self):

	v = self
	level = self.level()
	result = None

	while v:
		result = v
		v = v.threadNext()
		if not v or v.level() &lt;= level:
			break

	return result</t>
<t tx="T918">@ This function returns the indentation level of the receiver. The root nodes have level 0, their children have level 1, and so on.
@c

def level (self):

	level = 0 ; parent = self.parent()
	while parent:
		level += 1
		parent = parent.parent()
	return level</t>
<t tx="T919"># Compatibility routine for scripts

def next (self):

	return self.mNext</t>
<t tx="T920"># Returns the vnode following the tree whose root is the receiver.

def nodeAfterTree (self):

	next = self.next()
	p = self.parent()

	while not next and p:
		next = p.next()
		p = p.parent()

	return next</t>
<t tx="T921"># Compatibility routine for scripts

def parent (self):

	return self.mParent</t>
<t tx="T922">def threadBack (self):
	
	"""Returns the previous element of the outline, or None if at the start of the outline"""

	back = self.back()
	if back:
		lastChild = back.lastChild()
		if lastChild:
			return lastChild.lastNode()
		else:
			return back
	else:
		return self.parent()</t>
<t tx="T923">def threadNext (self):

	"""Returns node following the receiver in "threadNext" order"""

	# stat()
	v = self
	if v.firstChild():
		return v.firstChild()
	elif v.next():
		return v.next()
	else:
		p = v.parent()
		while p:
			if p.next():
				return p.next()
			p = p.parent()
		return None</t>
<t tx="T924">def visBack (self):

	v = self.threadBack()
	while v and not v.isVisible():
		v = v.threadBack()
	return v</t>
<t tx="T925">def visNext (self):

	v = self.threadNext()
	while v and not v.isVisible():
		v = v.threadNext()
	return v</t>
<t tx="T926"></t>
<t tx="T927"></t>
<t tx="T928">@ This is the main delete routine.  It deletes the receiver's entire tree from the screen.  Because of the undo command we never actually delete vnodes or tnodes.
@c

def doDelete (self, newVnode):

	"""Unlinks the receiver, but does not destroy it. May be undone"""

	v = self ; c = v.commands
	v.setDirty() # 1/30/02: mark @file nodes dirty!
	v.destroyDependents()
	v.unjoinTree()
	v.unlink()
	# Bug fix: 1/18/99: we must set the currentVnode here!
	c.selectVnode(newVnode)
	# Update all clone bits.
	c.initAllCloneBits()
	return self # We no longer need dvnodes: vnodes contain all needed info.</t>
<t tx="T929">def insertAfter (self,t=None):

	"""Inserts a new vnode after the receiver"""

	if not t:
		t = tnode(headString="NewHeadline")
	v = vnode(self.commands,t)
	v.iconVal = 0
	v.linkAfter(self)
	return v</t>
<t tx="T930">def insertAsLastChild (self,t=None):

	"""Inserts a new vnode as the last child of the receiver"""

	n = self.numberOfChildren()
	if not t:
		t = tnode(headString="NewHeadline")
	return self.insertAsNthChild(n,t)</t>
<t tx="T931">def insertAsNthChild (self,n,t=None):

	"""Inserts a new node as the the nth child of the receiver.
	The receiver must have at least n-1 children"""
	
	# trace(`n` + `self`)
	if not t:
		t = tnode(headString="NewHeadline")
	v = vnode(self.commands,t)
	v.iconVal = 0
	v.linkAsNthChild(self,n)
	return v</t>
<t tx="T932">def moveToRoot (self, oldRoot = None):

	"""Moves the receiver to the root position"""

	v = self
	v.destroyDependents()
	v.unlink()
	v.linkAsRoot(oldRoot)
	v.createDependents()</t>
<t tx="T933"># Restores (relinks) the dv tree in the position described by back and parent.

def restoreOutlineFromDVnodes (self, dv, parent, back):

	if back:
		dv.linkAfter(back)
	elif parent:
		dv.linkAsNthChild(parent, 0)
	else:
		dv.linkAsRoot()
	return dv</t>
<t tx="T934"># Creates a clone of back and insert it as the next sibling of back.

def clone (self,back):
	
	clone = self.cloneTree(back)
	clone.createDependents()

	# Set the clone bit in all nodes joined to back.
	clone.setClonedBit()
	back.setClonedBit()
	for v in back.t.joinList:
		v.setClonedBit()

	return clone</t>
<t tx="T935"># Links the receiver after v.

def linkAfter (self,v):

	# stat()
	self.mParent = v.mParent
	self.mBack = v
	self.mNext = v.mNext
	v.mNext = self
	if self.mNext:
		self.mNext.mBack = self</t>
<t tx="T936">def linkAsNthChild (self, p, n):

	"""Links the receiver as the n'th child of p"""

	v = self
	# stat() ; # trace(`v` + ", " + `p` + ", " + `n`)
	v.mParent = p
	if n == 0:
		v.mBack = None
		v.mNext = p.mFirstChild
		if p.mFirstChild:
			p.mFirstChild.mBack = v
		p.mFirstChild = v
	else:
		prev = p.nthChild(n-1) # zero based
		assert(prev)
		v.mBack = prev
		v.mNext = prev.mNext
		prev.mNext = v
		if v.mNext:
			v.mNext.mBack = v</t>
<t tx="T937">@ Bug fix: 5/27/02.  We link in the rest of the tree only when oldRoot != None.  Otherwise, we are calling this routine from init code and we want to start with a pristine tree.
@c
def linkAsRoot(self, oldRoot = None):

	v = self ; c = v.commands ; tree = c.tree
	# stat() ; # trace(`v`)
	# Bug fix 3/16/02:
	# Clear all links except the child link.
	# This allows a node with children to be moved up properly to the root position.
	# v.mFirstChild = None
	v.mParent = None
	v.mBack = None
	# 5/27/02
	if oldRoot: oldRoot.mBack = v
	v.mNext = oldRoot
	tree.rootVnode = v
</t>
<t tx="T938"># Used by scripts

def moveAfter (self,a):

	"""Moves the receiver after a"""

	v = self ; c = self.commands
	v.destroyDependents()
	v.unlink()
	v.linkAfter(a)
	v.createDependents()
	
	# 5/27/02: Moving a node after another node can create a new root node.
	if not a.parent() and not a.back():
		c.tree.rootVnode = a</t>
<t tx="T939"># Compatibility routine for scripts

def moveToNthChildOf (self, p, n):

	"""Moves the receiver to the nth child of p"""

	v = self ; c = self.commands

	v.destroyDependents()
	v.unlink()
	v.linkAsNthChild(p, n)
	v.createDependents()
	
	# 5/27/02: Moving a node can create a new root node.
	if not p.parent() and not p.back():
		c.tree.rootVnode = p</t>
<t tx="T940">def sortChildren (self):

	# Create a list of (headline,vnode) tuples
	v = self ; pairs = []
	child = v.firstChild()
	if not child: return
	while child:
		pairs.append((string.lower(child.headString()), child))
		child = child.next()
	# Sort the list on the headlines.
	pairs.sort()
	# Move the children.
	index = 0
	for headline,child in pairs:
		child.moveToNthChildOf(v,index)
		index += 1</t>
<t tx="T941"></t>
<t tx="T942">def addTreeToJoinLists (self):
	
	"""Add each v of v's entire tree to v.t.joinList."""
	
	v = self ; after = v.nodeAfterTree()
	
	while v and v != after:
		if not v in v.t.joinList:
			v.t.joinList.append(v)
		v = v.threadNext()</t>
<t tx="T943">def cloneTree (self, oldTree):
	
	"""Create a cloned tree after oldTree."""

	# Create a new tree following oldTree.
	newTree = oldTree.copyTree()
	newTree.linkAfter(oldTree)
	# Join the trees and copy clone bits.
	oldTree.joinTreeTo(newTree)
	oldTree.copyCloneBitsTo(newTree)
	return newTree</t>
<t tx="T944"># This methods propagates clone bits from the receiver's tree to tree2.

def copyCloneBitsTo (self, tree2):

	tree1 = self
	assert(tree2)
	# Set the bit in the root.
	if tree1.isCloned():
		tree2.setClonedBit()
	else:
		tree2.clearClonedBit()
	# Recursively set the bits in all subtrees.
	child1 = tree1.firstChild()
	child2 = tree2.firstChild()
	while child1:
		assert(child2)
		if child1.isCloned():
			child2.setClonedBit()
		else:
			child2.clearClonedBit()
		child1 = child1.next()
		child2 = child2.next()
	assert(child2 == None)</t>
<t tx="T945"># Rewritten 7/11/03.

def copyTree (self):
	
	"""Returns a free-standing copy of a vnode and all its descendents.
	
	The new tree uses the same tnodes as the old,
	but the new vnodes are _not_ joined to the old nodes.
	That is, the new vnodes v do not appear on v.t.joinList."""
	
	c = self.commands ; old_v = self
	
	# trace(self)
	
	# Copy all fields of the root.
	new_v = vnode(c,old_v.t)
	new_v.t.headString = old_v.t.headString
	new_v.iconVal = old_v.iconVal
	assert(new_v not in new_v.t.joinList)

	# Recursively copy and link all children.
	old_child = old_v.firstChild()
	n = 0
	while old_child:
		new_child = old_child.copyTree()
		new_child.linkAsNthChild(new_v,n)
		assert(new_child not in new_child.t.joinList)
		n += 1
		old_child = old_child.next()
		
	return new_v
</t>
<t tx="T946">def copyTreeWithNewTnodes (self):
	
	"""Return a copy of self with all new tnodes"""
	
	c = self.commands
	# trace(`self`)
	
	# Create the root node.
	old_v = self
	new_v = vnode(c,tnode())
	new_v.t.headString = old_v.t.headString
	new_v.t.bodyString = old_v.t.bodyString
	
	# Recursively create all descendents.
	old_child = old_v.firstChild() ; n = 0
	while old_child:
		new_child = old_child.copyTreeWithNewTnodes()
		new_child.linkAsNthChild (new_v, n)
		n += 1
		old_child = old_child.next()
		
	# Return the root of the new tree.
	return new_v</t>
<t tx="T947"># This method creates all nodes that depend on the receiver.
def createDependents (self):

	v = self ; t = v.t ; parent = v.parent()
	if not parent: return

	# Copy v as the nth child of all nodes joined to parent.
	n = v.childIndex()
	
	# 7/11/03: work on copy of join list.
	joinList = parent.t.joinList[:]
	if parent in joinList:
		joinList.remove(parent)

	for p in joinList:
		# trace(n,p)
		copy = v.copyTree()
		copy.linkAsNthChild(p,n)
		v.joinTreeTo(copy)</t>
<t tx="T948"># Destroys all dependent vnodes and tree nodes associated with the receiver.

def destroyDependents (self):
	
	"""Destroy the nth child of all nodes joined to the receiver's parent.."""

	parent = self.parent()
	if not parent:
		# trace("no parent",self)
		return

	n = self.childIndex()
	
	# 7/11/03: work on copy of join list.
	joinList = parent.t.joinList[:]
	if parent in joinList:
		joinList.remove(parent)
	#trace(parent,joinList)

	for join in joinList:
		# trace(n,join)
		child = join.nthChild(n)
		if child:
			child.unjoinTree()
			child.unlink()
			child.destroyTree()</t>
<t tx="T949">@ This method destroys (irrevocably deletes) a vnode tree.

This code should be called only when it is no longer possible to undo a previous delete.  It is always valid to destroy dependent trees.
@c

def destroyTree (self):

	pass</t>
<t tx="T950">def invalidOutline (self, message):

	s = "invalid outline: " + message + "\n"
	parent = self.parent()

	if parent:
		s += `parent`
	else:
		s += `self`

	alert ( s )</t>
<t tx="T951">def joinNodeTo (self, v2):
	
	"""Add self or v2 to their common join list"""

	v1 = self
	assert(v1.t==v2.t)
	j = v1.t.joinList
	
	if v1 not in j:
		j.append(v1)
		
	if v2 not in j:
		j.append(v2)</t>
<t tx="T952">@ This function joins all nodes in the receiver and tree2.  This code makes no assumptions about the two trees, and some or all of the nodes may already have been joined.  The assert's guarantee that both trees have the same topology.
@c

def joinTreeTo (self, tree2):

	tree1 = self
	assert(tree2)
	# Join the roots.
	tree1.joinNodeTo ( tree2 )
	# Recursively join all subtrees.
	child1 = tree1.firstChild()
	child2 = tree2.firstChild()
	while child1:
		assert(child2)
		child1.joinTreeTo(child2)
		child1 = child1.next()
		child2 = child2.next()
	assert(child2 == None)</t>
<t tx="T953">@ The receiver is a clone if and only it is structurally _dissimilar_ to a node joined to it.

Structurally _similar_ joined nodes have non-null, distinct and joined parents, and have the same child indices.
@c

def shouldBeClone (self):
	
	"""Returns True if the receiver should be a clone"""
	p = self.parent()
	n = self.childIndex()

	for v in self.t.joinList:
		if v != self:
			vp = v.parent()
			# self and v are structurally dissimilar if...
			if( (not p or not vp) or  # they are at the top level, or
				vp == p or  # have the same parent, or
				p.t != vp.t or  # have unjoined parents, or
				(v.childIndex() != n)): # have different child indices.

				# trace("true",v)
				return true

	# The receiver is structurally similar to all nodes joined to it.
	# trace("false",v)
	return false</t>
<t tx="T954">def unjoinTree (self):

	"""Remove all v and all its descendents v from v.t.joinList."""

	v = self
	after = self.nodeAfterTree()
	while v and v != after:
		if v in v.t.joinList:
			v.t.joinList.remove(v)
		v = v.threadNext()</t>
<t tx="T955">def unlink (self):

	"""Unlinks the receiver from the tree before moving or deleting.
	
	The mFistChild link is not affected in the receiver."""

	v = self ; c = v.commands ; tree = c.tree

	# stat() # trace(`v.mParent`+", child:"+`v.mFirstChild`+", back:"+`v.mBack`+", next:"+`v.mNext`)
	
	# Special case the root
	if v == tree.rootVnode:
		if not v.mNext: return # Should never happen.
		tree.rootVnode = v.mNext

	# Clear the links in other nodes
	if v.mBack:
		v.mBack.mNext = v.mNext
	if v.mNext:
		v.mNext.mBack = v.mBack
	if v.mParent and v == v.mParent.mFirstChild:
		v.mParent.mFirstChild = v.mNext

	# Clear the links in this node
	v.mParent = v.mNext = v.mBack = None</t>
<t tx="T956"># This routine checks the structure of the receiver's tree.

def validateOutlineWithParent (self, p):

	result = true # optimists get only unpleasant surprises.
	parent = self.parent()
	childIndex = self.childIndex()
	&lt;&lt; validate parent ivar &gt;&gt;
	&lt;&lt; validate childIndex ivar &gt;&gt;
	&lt;&lt; validate x ivar &gt;&gt;

	# Recursively validate all the children.
	child = self.firstChild()
	while child:
		r = child.validateOutlineWithParent ( self )
		if not r: result = false
		child = child.next()
	return result</t>
<t tx="T957">if parent != p:
	self.invalidOutline ( "Invalid parent link: " + parent.description() )</t>
<t tx="T958">if p:
	if childIndex &lt; 0:
		self.invalidOutline ( "missing childIndex" + childIndex )
	elif childIndex &gt;= p.numberOfChildren():
		self.invalidOutline ( "missing children entry for index: " + childIndex )
elif childIndex &lt; 0:
	self.invalidOutline ( "negative childIndex" + childIndex )</t>
<t tx="T959">if not self.t and p:
	self.invalidOutline ( "Empty t" )</t>
<t tx="T960"></t>
<t tx="T961">@ This is the entry point to the read code.  The root vnode should be an @file node.  If doErrorRecoveryFlag is false we are doing an update.  In that case it would be very unwise to do any error recovery which might clear clone links.  If doErrorRecoveryFlag is true and there are structure errors during the first pass we delete root's children and its body text, then rescan.  All other errors indicate potentially serious problems with sentinels.

The caller has enclosed this code in beginUpdate/endUpdate.
@c
def newRead(self,root):
	
	return false #### not ready yet: requires new findNthWrittenNode
	&lt;&lt; init read vars &gt;&gt;
	&lt;&lt; open file &gt;&gt;
	if self.errors &gt; 0: return 0
	es("reading: " + root.headString())
	&lt;&lt; Scan the file buffer &gt;&gt;
	if not (app().use_gnx and self.using_gnx):
		#### All this is going away for good ####
		&lt;&lt; Bump mStructureErrors if any vnodes are unvisited &gt;&gt;
		if self.structureErrors &gt; 0:
			self.readError("-- Rereading file.  Clone links into this file will be lost.") ;
			self.errors = 0
			&lt;&lt; quickly delete root's tree and body text &gt;&gt;
			file.seek(0)
			&lt;&lt; Scan the file buffer &gt;&gt;
	file.close()
	if self.errors &gt; 0:
		# A serious error has occured that has not been corrected.
		self.readError("----- File may have damaged sentinels!")
		root.unjoinTree();
	else: root.clearDirty()
	return self.errors == 0</t>
<t tx="T962">c = self.commands
self.root = root
self.raw = false
self.root_seen = false
self.readChildIndex = 0
self.errors = self.structureErrors = 0

# set self.targetFileName
if root.isAtFileNode():
	self.targetFileName = root.atFileNodeName()
else:
	self.targetFileName = root.atRawFileNodeName()</t>
<t tx="T963">self.scanAllDirectives(root) # 1/30/02

if not self.targetFileName or len(self.targetFileName) == 0:
	self.readError("Missing file name.  Restoring @file tree from .leo file.")
else:

	# print self.default_directory, self.targetFileName
	fn = os.path.join(self.default_directory, self.targetFileName)
	fn = os.path.normpath(fn)
	fn = toUnicode(fn,"ascii")
	
	try:
		file = open(fn,'r')
		if file:
			&lt;&lt; warn on read-only file &gt;&gt;
	except:
		self.readError("Can not open: " + '"@file ' + fn + '"')</t>
<t tx="T964">try:
	read_only = not os.access(fn,os.W_OK)
	if read_only:
		es("read only: " + fn,color="red")
except:
	pass # os.access() may not exist on all platforms.
</t>
<t tx="T965">firstLines = self.scanHeader(file)
self.indent = 0
self.root_seen = false
out = []
	
root.clearVisitedInTree() # Clear the list of nodes for orphans logic.

if app().use_gnx and self.using_gnx: # 4.0 code: delete all children of root.
	print "reading 4.0 file:", self.targetFileName
	self.unlinkedChildren = []
	&lt;&lt; unlink all children of root &gt;&gt;

lastLines = self.newScanText(file,root) ## ,out,atFile.endLeo)

# 18-SEP-2002 DTHEIN: update the bodyString directly, because
# out no longer holds body text of node.
if root.t.hasBody:
	bodyLines = root.t.bodyString.split('\n')
	self.completeFirstDirectives(bodyLines,firstLines)
	self.completeLastDirectives(bodyLines,lastLines)
	bodyText = '\n'.join(bodyLines)
	bodyText = bodyText.replace('\r', '')
	root.t.setTnodeText(bodyText)</t>
<t tx="T966">if 1: # New code: remember the unlinked children for the simulated Read Outline Only command.
	child = root.firstChild()
	while child:
		self.unlinkedChildren.append(child)
		next = child.next()
		child.unlink()
		child = next
	c.selectVnode(root)

else: # old code: we must not delete anything here.
	# Calling v.doDelete is way too slow here because it repeatedly calls c.initAllCloneBits.
	child = root.firstChild()
	while child:
		next = child.next()
		# The guts of doDelete
		child.destroyDependents()
		child.unjoinTree()
		child.unlink()
		child = next
	c.selectVnode(root)</t>
<t tx="T967">@ createNthNode marks all nodes in the derived file as visited.  Any unvisited nodes are either dummies or nodes that don't exist in the derived file.
@c

next = root.nodeAfterTree()
v = root.threadNext()
while v and v != next:
	if not v.isVisited():
		if 0: # CVS produces to many errors for this to be useful.
			es("unvisited node: " + v.headString())
		self.structureErrors += 1
	v = v.threadNext()
</t>
<t tx="T968">@ Calling v.doDelete is _way_ too slow here because it repeatedly calls c.initAllCloneBits.
@c

child = root.firstChild()
while child:
	next = child.next()
	# The guts of doDelete
	child.destroyDependents()
	child.unjoinTree()
	child.unlink()
	child = next
c.selectVnode(root)

root.setBodyStringOrPane("")</t>
<t tx="T969"># Scans the doc part and appends the text to at.out.
# s,i point to the present line on entry.

def oldScanDoc(self,s,i):
	
	at = self
	endKind = kind = at.endSentinelStack[-1]
	single = len(at.endSentinelComment) == 0
	&lt;&lt; Skip the opening sentinel &gt;&gt;
	&lt;&lt; Skip an opening block delim &gt;&gt;
	nextLine = None ; kind = at.noSentinel
	while len(s) &gt; 0:
		trace(s)
		kind = at.sentinelKind(s)
		if kind == endKind: break
		&lt;&lt; Skip the leading stuff &gt;&gt;
		&lt;&lt; Append s to out &gt;&gt;
		s = at.readLine(at.file)
	if kind != endKind:
		at.readError("Missing " + at.sentinelName(endKind) + " sentinel")
	&lt;&lt; Remove a closing block delim from out &gt;&gt;</t>
<t tx="T970">assert(match(s,i,choose(kind == at.startDoc, "+doc", "+at")))

at.out.append(choose(kind == at.startDoc, "@doc", "@"))
s = at.readLine(at.file)
</t>
<t tx="T971">if not single:
	j = skip_ws(s,0)
	if match(s,j,at.startSentinelComment):
		s = at.readLine(at.file)</t>
<t tx="T972"># Point i to the start of the real line.

if single: # Skip the opening comment delim and a blank.
	i = skip_ws(s,0)
	if match(s,i,at.startSentinelComment):
		i += len(at.startSentinelComment)
		if match(s,i," "): i += 1
else:
	i = at.skipIndent(s,0, at.indent)
</t>
<t tx="T973"># Append the line with a newline if it is real

line = s[i:-1] # remove newline for rstrip.

if line == line.rstrip():
	# no trailing whitespace: the newline is real.
	at.out.append(line + '\n')
else:
	# trailing whitespace: the newline is not real.
	at.out.append(line)
</t>
<t tx="T974"># This code will typically only be executed for HTML files.

if not single:

	delim = at.endSentinelComment
	n = len(delim)
	
	# Remove delim and possible a leading newline.
	s = string.join(at.out,"")
	s = s.rstrip()
	if s[-n:] == delim:
		s = s[:-n]
	if s[-1] == '\n':
		s = s[:-1]
		
	# Rewrite out in place.
	at.out = [s]</t>
<t tx="T975">"""New code for 4.0"""

from leoPlugins import *
from leoGlobals import *

import leoApp,leoAtFile,leoColor,leoDialog,leoFileCommands,leoFrame,leoNodes

# Warning: this code is pre-alpha.  See todo list.

if 0: # Register the handlers...

	@others
	
	registerHandler("start1",onAfterFinishCreate)
	registerHandler("create-optional-menus",onCreateExtraMenus)
	print "4.0 plugin"

	__version__ = "0.1a1"
	plugin_signon(__name__)</t>
<t tx="T976"></t>
<t tx="T977">def onAfterFinishCreate (tag,keywords):
	
	"""Handle processing that should be added to app.finishCreate."""
	
	a = app()

	a.use_gnx = true # true: enable 4.x code.

	# Add setLeoID to the LeoApp class and call it.
	funcToMethod(setLeoID,leoApp.LeoApp)
	a.setLeoID()

	# Create the single nodeIndices class.
	a.nodeIndices = leoNodes.nodeIndices()</t>
<t tx="T978">def onCreateExtraMenus (tag,keywords):
	
	c = keywords.get("c")
	self = c.frame # This code should really be part of the leoFrame class.
	
	&lt;&lt; extend the read/write submenu &gt;&gt;
	&lt;&lt; extend the export submenu &gt;&gt;
</t>
<t tx="T979">if app().use_gnx: # Testing.

	table2 = (
		("-",None,None),
		("Read 4.0 Derived File",None,self.OnReadGnxFile),
		("Write 4.0 Derived File",None,self.OnWriteGnxFile),
		("Clear All Node Indices",None,self.OnClearAllNodeIndices))

	if 1: # pluging code.
		readWriteMenu = self.getMenu("ReadWrite")
		self.createMenuEntries (readWriteMenu,table2)
	else: # native code.
		table.extend(table2)</t>
<t tx="T980">if app().use_gnx:
	
	table2 = (
		("-",None,None),
		("Write Old Format Outline",None,self.OnWriteOldOutline))
	
	if 1: # pluging code.
		exportMenu = self.getMenu("Export")
		self.createMenuEntries(exportMenu,table2)
	else: # native code.
		table.extend(table2)</t>
<t tx="T981"></t>
<t tx="T982">def setLeoID (self):
	
	print "setLeoID"
	
	if not self.use_gnx:
		return # Used only in 4.x.
		
	tag = ".leoID.txt"
	loadDir = app().loadDir
	configDir = app().config.configDir
	&lt;&lt; return if we can set self.leoID from sys.leoID &gt;&gt;
	&lt;&lt; return if we can set self.leoID from "leoID.txt" &gt;&gt;
	&lt;&lt; put up a dialog requiring a valid id &gt;&gt;
	&lt;&lt; attempt to create leoID.txt &gt;&gt;</t>
<t tx="T983"># This would be set by in Python's sitecustomize.py file.
try:
	self.leoID = sys.leoID
	es("leoID = " + self.leoID, color="blue")
	return
except:
	self.leoID = None</t>
<t tx="T984">for dir in (configDir,loadDir):
	try:
		fn = os.path.join(dir, tag)
		f = open(fn,'r')
		if f:
			s = f.readline()
			f.close()
			if s and len(s) &gt; 0:
				self.leoID = s
				es("leoID = " + self.leoID, color="blue")
				return
			else:
				es("empty " + tag + " in " + dir, color = "red")
	except: self.leoID = None
		
if configDir == loadDir:
	es(tag + " not found in " + loadDir, color="red")
else:
	es(tag + " not found in " + configDir + " or " + loadDir, color="red")
</t>
<t tx="T985">self.leoID = leoDialog.askLeoID().run(modal=true)

es("leoID = " + `self.leoID`, color="blue")</t>
<t tx="T986">for dir in (configDir,loadDir):
	try:
		# Look in configDir first.
		fn = os.path.join(dir, tag)
		f = open(fn,'w')
		if f:
			f.write(self.leoID)
			f.close()
			es("created leoID.txt in " + dir, color="red")
			return
	except: pass
	
if configDir == loadDir:
	es("can not create leoID.txt in " + loadDir, color="red")
else:
	es("can not create leoID.txt in " + configDir + " or " + loadDir, color="red")

</t>
<t tx="T987">class askLeoID (leoDialog.leoDialog):
	
	"""A class to create and run a dialog that asks for Id for gnx's."""
	
	@others

leoDialog.askLeoID = askLeoID</t>
<t tx="T988">def __init__(self):
	
	"""Create the Leo Id dialog."""
	
	leoDialog.__init__(self,"Enter unique id",resizeable=false) # Initialize the base class.
	self.id_entry = None
	self.answer = None

	self.createTopFrame()
	self.top.protocol("WM_DELETE_WINDOW", self.onCloseWindow)
	self.top.bind("&lt;Key&gt;", self.onKey)
	
	message = (
		"leoID.txt not found\n\n" +
		"Please enter an id that identifies you uniquely.\n" +
		"Your cvs login name is a good choice.\n\n" +
		"Your id must contain only letters and numbers\n" +
		"and must be at least 4 characters in length.")
	self.createFrame(message)
	self.focus_widget = self.id_entry

	buttons = {"text":"OK","command":self.onButton,"default":true}, # Singleton tuple.
	buttonList = self.createButtons(buttons)
	self.ok_button = buttonList[0]</t>
<t tx="T989">def createFrame(self,message):
	
	"""Create the frame for the Leo Id dialog."""
	
	f = self.frame

	label = Tk.Label(f,text=message)
	label.pack(pady=10)

	self.id_entry = text = Tk.Entry(f,width=20)
	text.pack()</t>
<t tx="T990">def onCloseWindow (self):
	
	"""Prevent the Leo Id dialog from closing by ignoring close events."""

	pass</t>
<t tx="T991">def onButton(self):
	
	"""Handle clicks in the Leo Id close button."""

	s = self.id_entry.get().strip()
	if len(s) &lt; 4:  # Require at least 4 characters in an id.
		return

	self.answer = s
	self.top.destroy() # terminates wait_window</t>
<t tx="T992">def onKey(self,event):
	
	"""Handle keystrokes in the Leo Id dialog."""
	
	&lt;&lt; eliminate invalid characters &gt;&gt;
	&lt;&lt; enable the ok button if there are 4 or more valid characters &gt;&gt;
	
	ch = event.char.lower()
	if ch in ('\n','\r'):
		self.onButton()
	return "break"

</t>
<t tx="T993">e = self.id_entry
s = e.get().strip()
i = 0 ; ok = true
while i &lt; len(s):
	ch = s[i]
	if ch not in string.letters and ch not in string.digits:
		e.delete(`i`)
		s = e.get()
		ok = false
	else:
		i += 1
if not ok: return</t>
<t tx="T994">e = self.id_entry
b = self.ok_button

if len(e.get().strip()) &gt;= 4:
	b.configure(state="normal")
else:
	b.configure(state="disabled")</t>
<t tx="T995">class myFileCommands(leoFileCommands.baseFileCommands):
	@others

leoFileCommands.fileCommands = myFileCommands</t>
<t tx="T996">def __init__(self,theCommander):
	
	"""Ctor for myFileCommands class (gnx code)."""
	
	# print "myFileCommands ctor",self
	leoFileCommands.baseFileCommands.__init__(self,theCommander) # Initialize the base class.
	
	self.a = app()
	self.nodeIndices = self.a.nodeIndices</t>
<t tx="T997">def assignAllGnx (self,root=None):
	
	"""Assign a gnx to tnodes that don't have one"""
	
	c = self.commands ; v = c.rootVnode()
	nodeIndices = self.nodeIndices
	
	# Set the time for all tnodes requiring a new gnx field.
	nodeIndices.setTimestamp()

	while v:
		if not v.t.gnx:
			v.t.gnx = nodeIndices.getNewIndex()
		v = v.threadNext()</t>
<t tx="T998">class myFrame(leoFrame.baseLeoFrame):
	@others

leoFrame.LeoFrame = myFrame</t>
<t tx="T999">def __init__(self, title = None):
	
	"""Ctor for myFrame class (gnx code)."""

	leoFrame.baseLeoFrame.__init__(self,title) # Initialize the base class.</t>
<t tx="T1000">def OnClearAllNodeIndices (self,event=None):
	
	c = self.commands ; root = c.rootVnode()
	v = root
	while v:
		v.t.gnx = None
		v = v.threadNext()
	es("all tnode indices cleared",color="red")</t>
<t tx="T1001">def OnWriteGnxFile (self,event=None):
	
	c = self.commands ; v = c.currentVnode()
	at = atFile2(c) # Create a temporary subcommander.
	at.using_gnx = true
	at.newWrite(v)
	at.using_gnx = false
	es("finished")</t>
<t tx="T1002">def OnReadGnxFile (self,event=None):
	
	c = self.commands ; v = c.currentVnode()
	
	c.atFileCommands.read(v)
	
	if 0: # no longer used
		c.beginUpdate()
		at.newRead(v)
		c.initAllCloneBits() # Must be done after all reads.
		c.endUpdate()
	
		c.recolor()
		es("finished")</t>
<t tx="T1003"># Based on the Save As code.

def OnWriteOldOutline (self,event=None):
	
	"""Saves a pre-4.0 outline"""
	a = app()

	# Make sure we never pass None to the ctor.
	if not self.mFileName:
		self.title = ""

	# set local fileName, _not_ self.mFileName
	fileName = tkFileDialog.asksaveasfilename(
		initialfile = self.mFileName,
		title="Write Pre 4.0 Outline",
		filetypes=[("Leo files", "*.leo")],
		defaultextension=".leo")

	if len(fileName) &gt; 0:
		fileName = ensure_extension(fileName, ".leo")
		old = a.use_gnx ; a.use_gnx = false
		self.commands.fileCommands.saveTo(fileName)
		self.updateRecentFiles(self.mFileName)
		a.use_gnx = old</t>
<t tx="T1004">class myTnode(leoNodes.baseTnode):
	@others
	
leoNodes.tnode = myTnode</t>
<t tx="T1005">def __init__ (self,index=0,bodyString=None,headString=None):
	
	leoNodes.baseTnode.__init__(self,index,bodyString,headString)
	self.gnx = None #  Will be set later.</t>
<t tx="T1006">def getGnx(self):
	
	return self.gnx
</t>
<t tx="T1007"># Indices are Python dicts containing 'id','loc','time' and 'n' keys.

import time

class nodeIndices:
	@others
	
leoNodes.nodeIndices = nodeIndices</t>
<t tx="T1008">def __init__ (self):
	
	"""ctor for nodeIndices class"""
	
	self.userId = app().leoID # 5/1/03: This never changes.
	self.defaultId = app().leoID # This probably will change.
	self.lastIndex = None
	self.timeString = None</t>
<t tx="T1009">def areEqual (self,gnx1,gnx2):
	
	"""Return True if all fields of gnx1 and gnx2 are equal"""

	id1,time1,n1 = gnx1
	id2,time2,n2 = gnx2
	return id1==id2 and time1==time2 and n1==n2</t>
<t tx="T1010"># These are used by the fileCommands read/write code.

def getDefaultId (self):
	
	"""Return the id to be used by default in all gnx's"""
	return self.defaultId
	
def setDefaultId (self,id):
	
	"""Set the id to be used by default in all gnx's"""
	self.defaultId = id
</t>
<t tx="T1011">def getNewIndex (self):
	
	"""Create a new gnx using self.timeString and self.lastIndex"""
	
	id = self.userId # Bug fix 5/1/03: always use the user's id for new ids!
	t = self.timeString
	assert(t)
	n = None

	# Set n if id and time match the previous index.
	last = self.lastIndex
	if last:
		lastId,lastTime,lastN = last
		if id==lastId and t==lastTime:
			if lastN == None: n = 1
			else: n = lastN + 1

	d = (id,t,n)
	self.lastIndex = d
	trace(d)
	return d</t>
<t tx="T1012">def scanGnx (self,s,i):
	
	"""Create a gnx from its string representation"""

	if len(s) &gt; 0 and s[-1] == '\n':
		s = s[:-1]

	id,t,n=None,None,None
	i,id = skip_to_char(s,i,'.')
	if match(s,i,'.'):
		i,t = skip_to_char(s,i+1,'.')
		if match(s,i,'.'):
			i,n = skip_to_char(s,i+1,'.')
	# Use self.defaultId for missing id entries.
	if id == None or len(id) == 0:
		id = self.defaultId
	# Convert n to int.
	if n:
		try: n = int(n)
		except: pass
	d = (id,t,n)

	return d</t>
<t tx="T1013">def setTimestamp (self):

	"""Set the timestamp string to be used by getNewIndex until further notice"""

	self.timeString = time.strftime(
		"%m%d%y%H%M%S",  # compact timestamp is best
		time.localtime())</t>
<t tx="T1014">def toString (self,index,removeDefaultId=false):
	
	"""Convert a gnx (a tuple) to its string representation"""

	id,t,n = index

	if removeDefaultId and id == self.defaultId:
		id = ""

	if n == None:
		return "%s.%s" % (id,t)
	else:
		return "%s.%s.%d" % (id,t,n)</t>
<t tx="T1015">class myAtFile(leoAtFile.baseAtFile):
	@others

leoAtFile.atFile = myAtFile

atFile = myAtFile</t>
<t tx="T1016">def __init__(self,theCommander):
	
	"""Ctor for myAtFile class (gnx code)."""
	
	# print "myAtFile ctor",self
	leoAtFile.baseAtFile.__init__(self,theCommander) # Initialize the base class.
	
	# For interface between 3.x and 4.x read code.
	self.using_gnx = false
	self.file = None
	
</t>
<t tx="T1017">@ This method sets self.startSentinelComment and self.endSentinelComment based on the first @+leo sentinel line of the file.  We can not call sentinelKind here because that depends on the comment delimiters we set here.  @first lines are written "verbatim", so nothing more needs to be done!

7/8/02: Leading whitespace is now significant here before the @+leo.  This is part of the "REM hack".  We do this so that sentinelKind need not skip whitespace following self.startSentinelComment.  This is correct: we want to be as restrictive as possible about what is recognized as a sentinel.  This minimizes false matches.

14-SEP-2002 DTHEIN:  Queue up the lines before the @+leo.  These will be used to add as parameters to the @first directives, if any.  Empty lines are ignored (because empty @first directives are ignored). NOTE: the function now returns a list of the lines before @+leo.
@c
def scanHeader(self,file):
	
	at = self
	# trace()
	at.using_gnx = false # 4.0
	version_tag = "-ver="
	valid = true
	tag = "@+leo"
	encoding_tag = "-encoding="
	&lt;&lt; skip any non @+leo lines &gt;&gt;
	&lt;&lt; make sure we have @+leo &gt;&gt;
	&lt;&lt; read optional version param &gt;&gt;
	&lt;&lt; read optional encoding param &gt;&gt;
	&lt;&lt; set the closing comment delim &gt;&gt;
	if not valid:
		at.readError("Bad @+leo sentinel in " + at.targetFileName)
	return firstLines</t>
<t tx="T1018">firstLines = [] # The lines before @+leo.
s = at.readLine(file)
while len(s) &gt; 0:
	j = s.find(tag)
	if j != -1: break
	firstLines.append(s) # Queue the line
	s = at.readLine(file)
n = len(s)
valid = n &gt; 0
# s contains the tag
i = j = skip_ws(s,0)
# The opening comment delim is the initial non-whitespace.
# 7/8/02: The opening comment delim is the initial non-tag
while i &lt; n and not match(s,i,tag) and not is_nl(s,i):
	i += 1
if j &lt; i:
	at.startSentinelComment = s[j:i]
else: valid = false</t>
<t tx="T1019">if 0:# 7/8/02: make leading whitespace significant.
	i = skip_ws(s,i)

if match(s,i,tag):
	i += len(tag)
else: valid = false</t>
<t tx="T1020">at.using_gnx = match(s,i,version_tag)

if at.using_gnx:
	trace("reading gnx file")
	i += len(version_tag)
	# Skip to the next minus sign or end-of-line
	j = i
	while i &lt; len(s) and not is_nl(s,i) and s[i] != '-':
		i += 1
	if j &lt; i:
		version = s[j:i]
	else:
		valid = false

	
</t>
<t tx="T1021"># 1/20/03: EKR: Read optional encoding param, e.g., -encoding=utf-8,

# Set the default encoding
at.encoding = app().config.default_derived_file_encoding

if match(s,i,encoding_tag):
	i += len(encoding_tag)
	# Skip to the next comma
	j = i
	while i &lt; len(s) and not is_nl(s,i) and s[i] not in (',','.'):
		i += 1
	if match(s,i,',') or match(s,i,'.'):
		encoding = s[j:i]
		i += 1
		# print "@+leo-encoding=",encoding
		if isValidEncoding(encoding):
			at.encoding = encoding
		else:
			es("bad encoding in derived file:",encoding)
	else:
		valid = false
</t>
<t tx="T1022"># The closing comment delim is the trailing non-whitespace.
i = j = skip_ws(s,i)
while i &lt; n and not is_ws(s[i]) and not is_nl(s,i):
	i += 1
at.endSentinelComment = s[j:i]</t>
<t tx="T1023">@ This is the entry point to the read code.  The root vnode should be an @file node.  If doErrorRecoveryFlag is false we are doing an update.  In that case it would be very unwise to do any error recovery which might clear clone links.  If doErrorRecoveryFlag is true and there are structure errors during the first pass we delete root's children and its body text, then rescan.  All other errors indicate potentially serious problems with sentinels.

The caller has enclosed this code in beginUpdate/endUpdate.
@c
def read(self,root):

	at = self ; c = at.commands
	&lt;&lt; set self.targetFileName &gt;&gt;
	at.root = root ; at.raw = false
	at.errors = at.structureErrors = 0
	&lt;&lt; open file &gt;&gt;
	if at.errors &gt; 0: return 0
	es("reading: " + root.headString())
	&lt;&lt; Scan the file buffer &gt;&gt;
	&lt;&lt; Bump mStructureErrors if any vnodes are unvisited &gt;&gt;
	if at.structureErrors &gt; 0:
		at.readError("-- Rereading file.  Clone links into this file will be lost.") ;
		at.errors = 0
		&lt;&lt; quickly delete root's tree and body text &gt;&gt;
		file.seek(0)
		&lt;&lt; Scan the file buffer &gt;&gt;
	file.close()
	if at.errors &gt; 0:
		# A serious error has occured that has not been corrected.
		at.readError("----- File may have damaged sentinels!")
		root.unjoinTree();
	else: root.clearDirty()
	return at.errors == 0</t>
<t tx="T1024">if root.isAtFileNode():
	at.targetFileName = root.atFileNodeName()
else:
	at.targetFileName = root.atRawFileNodeName()</t>
<t tx="T1025">at.scanAllDirectives(root) # 1/30/02

if not at.targetFileName or len(at.targetFileName) == 0:
	at.readError("Missing file name.  Restoring @file tree from .leo file.")
else:
	# print at.default_directory, at.targetFileName
	fn = os.path.join(at.default_directory, at.targetFileName)
	fn = os.path.normpath(fn)
	fn = toUnicode(fn,"ascii")
	
	try:
		file = open(fn,'r')
		if file:
			&lt;&lt; warn on read-only file &gt;&gt;
	except:
		at.readError("Can not open: " + '"@file ' + fn + '"')</t>
<t tx="T1026">try:
	read_only = not os.access(fn,os.W_OK)
	if read_only:
		es("read only: " + fn,color="red")
except:
	pass # os.access() may not exist on all platforms.
</t>
<t tx="T1027">firstLines = at.scanHeader(file)

# Reading 4.0 files is not ready yet.
if at.using_gnx:
	at2 = atFile2(c) # Create a temporary subcommander.
	at2.targetFileName = at.targetFileName
	at2.startSentinelComment = at.startSentinelComment # Set by scanHeader
	at2.endSentinelComment = at.endSentinelComment # Set by scanHeader
	at2.file = file
	at2.tab_width = at.tab_width
	return at2.readOpenFile(root,file,firstLines) # Use the new code to read the file.
else:
	at.indent = 0
	at.root_seen = false
	out = []
		
	root.clearVisitedInTree() # Clear the list of nodes for orphans logic.
	lastLines = at.scanText(file,root,out,at.endLeo)
	
	# 18-SEP-2002 DTHEIN: update the bodyString directly, because
	# out no longer holds body text of node.
	if root.t.hasBody:
		bodyLines = root.t.bodyString.split('\n')
		at.completeFirstDirectives(bodyLines,firstLines)
		at.completeLastDirectives(bodyLines,lastLines)
		bodyText = '\n'.join(bodyLines)
		bodyText = bodyText.replace('\r', '')
		root.t.setTnodeText(bodyText)</t>
<t tx="T1028">@ createNthNode marks all nodes in the derived file as visited.  Any unvisited nodes are either dummies or nodes that don't exist in the derived file.
@c

next = root.nodeAfterTree()
v = root.threadNext()
while v and v != next:
	if not v.isVisited():
		if 0: # CVS produces to many errors for this to be useful.
			es("unvisited node: " + v.headString())
		at.structureErrors += 1
	v = v.threadNext()
</t>
<t tx="T1029">@ Calling v.doDelete is _way_ too slow here because it repeatedly calls c.initAllCloneBits.
@c

child = root.firstChild()
while child:
	next = child.next()
	# The guts of doDelete
	child.destroyDependents()
	child.unjoinTree()
	child.unlink()
	child = next
c.selectVnode(root)

root.setBodyStringOrPane("")</t>
<t tx="T1030">&lt;&lt; how this code handles whitespace and newlines &gt;&gt;

class atFile2(leoAtFile.baseAtFile):
	
	"""A class to read and write 4.x derived files."""

	@others</t>
<t tx="T1031">@ Getting whitespace and newlines correct is crucial to the proper working of the read and write code.  Moreover, it should be easy for the read code to determine what the original outline was that was written by the write code.

Here is how the write code handles newlines:

- The main write code is found in putBody.  This method scans body text line by line.

- Each line of the body text, except possibly the last line, ends in a newline character.

** For each line of body text, the corresponding text written to the output file will _always_ end in a newline.  This is a crucial simplifying assumption.  It means that we don't have to keep track of what was written previously.  Indeed, the new code doesn't use any "state" ivars such as suppress_newlines or newline_pending.

- The putBody sets the trailingNewlineFlag ivar.  If this is set, eventually putBody will generate an @nonl sentinel to cancel the effect of an extra newline written to the derived file.  Code may indicate that @nonl has already been written by clearing the trailingNewlineFlag ivar.

- The putSentinel routine does nothing if we aren't generating sentinels.  Otherwise, if putLeadingNewlineFlag is true putSentinel will output a leading newline.  This is purely a convenience so callers don't have to test whether self.sentinels is true or not.

- @+doc and @+at sentinels may be followed by an @nonl sentinel to indicate that no newline should appear between the @doc or @ directive and the following line.  In other words, the contribution of the @+doc and @+at sentinels _does_ include a newline.
</t>
<t tx="T1032">def __init__(self,theCommander):
	
	"""Ctor for 4.x atFile class."""
	
	at = self

	# Initialize the base class.
	leoAtFile.baseAtFile.__init__(self,theCommander) 

	# For 4.x reading &amp; writing...
	at.inCode = true
	at.nodeIndices = app().nodeIndices
	at.readChildIndex = 0 # Index into at.root.tnodeList.
	at.using_gnx = false # true: present derived file uses gnxs.

	# For 4.x writing...
	at.docKind = None
	at.pending = [] # Doc part that remains to be written.

	# For 4.0 reading...
	at.docOut = [] # The doc part being accumulated.
	at.done = false # true when @-leo seen.
	at.endSentinelStack = []
	at.indent = 0 ; at.indentStack = []
	at.lastLines = [] # The lines after @-leo
	at.leading_ws = ""
	at.out = None ; at.outStack = []
	at.root_seen = false # true: root vnode has been handled in this file.
	at.v = None ; at.vStack = []

	# The dispatch dictionary used by scanText.
	at.dispatch_dict = {
		# Plain line.
		at.noSentinel: at.readNormalLine,
		# Starting sentinels...
		at.startAt:     at.readStartAt,
		at.startDoc:    at.readStartDoc,
		at.startLeo:    at.readStartLeo,
		at.startNode:   at.readStartNode,
		at.startOthers: at.readStartOthers,
		# Ending sentinels...
		at.endAt:     at.readEndAt,
		at.endDoc:    at.readEndDoc,
		at.endLeo:    at.readEndLeo,
		at.endNode:   at.readEndNode,
		at.endOthers: at.readEndOthers,
		# Non-paired sentinels.
		at.startAfterRef:  at.readAfterRef,
		at.startComment:   at.readComment,
		at.startDelims:    at.readDelims,
		at.startDirective: at.readDirective,
		at.startNl:        at.readNl,
		at.startNonl:      at.readNonl,
		at.startRef:       at.readRef,
		at.startVerbatim:  at.readVerbatim,
		at.startWs:        at.readWs }</t>
<t tx="T1033"></t>
<t tx="T1034">def readOpenFile (self,root,file,firstLines):
	
	trace()
	
	at = self
	
	# Similar to atFile.read
	at.using_gnx = true
	at.root = root ; at.raw = false
	at.errors = 0
	at.structureErrors = 0 ## Not used??
	&lt;&lt; Scan the file buffer &gt;&gt;
	file.close()

	if at.errors &gt; 0:
		# A serious error has occured that has not been corrected.
		at.readError("----- File may have damaged sentinels!")
		root.unjoinTree();
	else:
		root.clearDirty()

	return at.errors == 0
</t>
<t tx="T1035">at.indent = 0
at.root_seen = false

## out = []
	
root.clearVisitedInTree() # Clear the list of nodes for orphans logic.

lastLines = at.scanText(file,root) ## ,out,at.endLeo)

# 18-SEP-2002 DTHEIN: update the bodyString directly, because
# out no longer holds body text of node.
if root.t.hasBody:
	bodyLines = root.t.bodyString.split('\n')
	at.completeFirstDirectives(bodyLines,firstLines)
	at.completeLastDirectives(bodyLines,lastLines)
	bodyText = '\n'.join(bodyLines)
	bodyText = bodyText.replace('\r', '')
	root.t.setTnodeText(bodyText)</t>
<t tx="T1036"># This is the entry point to the write code.  root should be an @file vnode.

def newWrite(self,root,nosentinels=false):

	at = self
	trace('*' * 20)
	c = at.commands
	at.sentinels = not nosentinels
	&lt;&lt; initialize &gt;&gt;
	try:
		&lt;&lt; open the file; return on error &gt;&gt;
		&lt;&lt; write then entire @file tree &gt;&gt;
		at.closeWriteFile()
		if 0: ### Not yet
			&lt;&lt; warn about @ignored and orphans &gt;&gt;
		&lt;&lt; finish writing &gt;&gt;
	except:
		at.handleWriteException()</t>
<t tx="T1037">at.errors = 0
c.setIvarsFromPrefs()
at.root = root
at.raw = false
c.endEditing() # Capture the current headline.
at.root.tnodeList = [] # Will get this from the .leo file.

at.nodeIndices.setTimestamp() # Set the time for all gnx fields.</t>
<t tx="T1038">if nosentinels:
	at.targetFileName = root.atNoSentinelsFileNodeName()
else:
	at.targetFileName = root.atFileNodeName()

ok = at.openWriteFile(root)
if not ok: return</t>
<t tx="T1039"># unvisited nodes will be orphans, except in cweb trees.
root.clearVisitedInTree()
next = root.nodeAfterTree()

# Put @first lines.
junk, firstLines, lastLines = at.getAtFirstLastLines(root.bodyString())
for line in firstLines:
	at.os(line) ; at.onl()

# Put the main part of the file.
tag1 = choose(at.using_gnx,"@+leo-ver=2","@+leo")
at.putOpenLeoSentinel(tag1)
at.putInitialComment()
at.putBody(root)
at.putSentinel("@-leo")

# Put @last lines.
for line in lastLines:
	at.os(line) ; at.onl()

root.setVisited()</t>
<t tx="T1040"># 10/26/02: Always warn, even when language=="cweb"

next = root.nodeAfterTree()
v = root
while v and v != next:
	if not v.isVisited():
		at.writeError("Orphan node:  " + v.headString())
	if v.isAtIgnoreNode():
		at.writeError("@ignore node: " + v.headString())
	v = v.threadNext()
</t>
<t tx="T1041">@ We set the orphan and dirty flags if there are problems writing the file to force Commands::write_LEO_file to write the tree to the .leo file.
@c

if at.errors &gt; 0 or at.root.isOrphan():
	root.setOrphan()
	root.setDirty() # 2/9/02: make _sure_ we try to rewrite this file.
	os.remove(at.outputFileName) # Delete the temp file.
	es("Not written: " + at.outputFileName)
else:
	root.clearOrphan()
	root.clearDirty()
	at.replaceTargetFileIfDifferent()</t>
<t tx="T1042"># 4.0: Don't use newline-pending logic.

def closeWriteFile (self):
	
	at = self
	if at.outputFile:
		at.outputFile.flush()
		at.outputFile.close()
		at.outputFile = None</t>
<t tx="T1043"></t>
<t tx="T1044">@ New for 4.0:

1. @first and @lines may appear anywhere in the body text.  Only the order of @first lines relative to each other and the order of @last lines relative to each other matters.

2. This code always returns a trailing newline in s.
@c

def getAtFirstLastLines (self,s):
	
	"""Remove @first and @last lines from s.

	Return s, firstLines, lastLines."""
	
	if not s:
		return s,[],[]
	
	firstLines = [] ; lastLines = []
	lines = s.split('\n') ; i = 0
	while i &lt; len(lines):
		s = lines[i]
		if match_word(s,0,"@first"):
			j = skip_ws(s,6)
			s = s[j:]
			firstLines.append(s)
			del lines[i]
		elif match_word(s,0,"@last"):
			j = skip_ws(s,5)
			s = s[j:]
			lastLines.append(s)
			del lines[i]
		else:
			i += 1

	s = string.join(lines,'\n')
	return s,firstLines,lastLines</t>
<t tx="T1045">def putBody(self,v):
	
	""" Generate the body enclosed in sentinel lines."""

	at = self ; s = v.bodyString()
	if not s: return

	inCode = true
	if v == at.root:
		s,junk,junk = at.getAtFirstLastLines(s)
		if not s: return

	# Make _sure_ all lines end in a newline.
	trailingNewlineFlag = s and s[-1] == '\n'
	if not trailingNewlineFlag:
		s = s + '\n'
	
	at.putOpenNodeSentinel(v)
	i = 0
	while i &lt; len(s):
		next_i = skip_line(s,i)
		assert(next_i &gt; i)
		kind = at.directiveKind(s,i)
		&lt;&lt; handle line at s[i] &gt;&gt;
		i = next_i
	if not inCode:
		at.putEndDocLine()
	if not trailingNewlineFlag:
		at.putSentinel("@nonl")
	at.putCloseNodeSentinel(v)
</t>
<t tx="T1046">if kind == at.noDirective:
	if inCode:
		hasRef,n1,n2 = at.findSectionName(s,i)
		if hasRef:
			at.putRefLine(s,i,n1,n2,v)
		else:
			at.putCodeLine(s,i)
	else:
		at.putDocLine(s,i)
elif kind in (at.docDirective, at.atDirective):
	assert(not at.pending)
	at.putStartDocLine(s,i,kind)
	inCode = false
elif kind in (at.cDirective, at.codeDirective):
	# Only @c and @code end a doc part.
	if not inCode:
		at.putEndDocLine() 
	at.putDirective(s,i)
	inCode = true
elif kind == at.othersDirective:
	inCode = true
	at.putAtOthersLine(s,i,v)
elif kind == at.rawDirective:
	at.raw = true
	at.putSentinel("@@raw")
elif kind == at.endRawDirective:
	at.raw = false
	at.putSentinel("@@end_raw")
	i = skip_line(s,i)
elif kind == at.miscDirective:
	at.putDirective(s,i)
else:
	assert(not "unknown directive")
</t>
<t tx="T1047"></t>
<t tx="T1048">def putAtOthersLine (self,s,i,v):
	
	"""Put the expansion of @others."""
	
	at = self
	j,delta = skip_leading_ws_with_indent(s,i,at.tab_width)
	at.indent += delta
	at.putLeadInSentinel(s,i,j)
	at.putSentinel("@+others")
	after = v.nodeAfterTree()
	child = v.threadNext()
	while child and child != after:
		if at.inAtOthers(child):
			child.setVisited() # Make sure it is never expanded again.
			at.putBody(child)
		child = child.threadNext()
	at.putSentinel("@-others")
	at.indent -= delta</t>
<t tx="T1049">def putCodeLine (self,s,i):
	
	at = self
	
	j = skip_line(s,i)
	at.putIndent(at.indent)
	line = s[i:j]
	# trace(`line`)
	at.os(line)</t>
<t tx="T1050">def putRefLine(self,s,i,n1,n2,v):
	
	"""Put a reference at s[n1:n2+2] from v."""
	
	at = self ; name = s[n1:n2+2]

	ref = findReference(name,v)
	# trace(`name`,`ref`)
	if not ref:
		at.writeError(
			"undefined section: %s\n\treferenced from: %s" %
			( name,v.headString()))
		return
	
	# Expand the ref.
	j,delta = skip_leading_ws_with_indent(s,i,at.tab_width)
	at.indent += delta
	at.putLeadInSentinel(s,i,n1)
	at.putSentinel("@%s" % name)
	at.putBody(ref)
	at.indent -= delta
	
	# Handle whatever follows the ref.
	j = skip_ws(s,n2+2)
	if j &lt; len(s) and s[j] != '\n':
		i = skip_to_end_of_line(s,i)
		after = s[n2+2:i]
		at.putSentinel("@afterref")
		at.os(after) ; at.onl()
	else:
		at.putSentinel("@nl")</t>
<t tx="T1051"></t>
<t tx="T1052">def putStartDocLine (self,s,i,kind):
	
	at = self ; at.docKind = kind
	
	# j = skip_line(s,0) ; trace(`s[:j]`)
	
	# put the opening doc sentinel
	sentinel = choose(kind == at.docDirective,"@+doc","@+at")
	at.putSentinel(sentinel)
	
	# Put the opening comment.
	if at.endSentinelComment:
		at.putIndent(at.indent)
		at.os(at.startSentinelComment) ; at.onl()

	# Skip past the directive
	directive = choose(kind == at.docDirective,"@doc","@")
	i += len(directive)
	i = skip_ws(s,i)
	
	# Put an @nonl sentinel if there is significant text following @doc or @.
	if not is_nl(s,i):
		at.putSentinel("@nonl")
		at.putDocLine(s,i)</t>
<t tx="T1053">def putDocLine (self,s,i):
	
	"""Handle one line of a doc part.
	
	Output complete lines and split long lines and queue pending lines.
	Inserted newlines are always preceded by whitespace."""
	
	at = self
	j = skip_line(s,i)
	s = s[i:j]
	# trace(s)

	if at.endSentinelComment:
		leading = at.indent
	else:
		leading = at.indent + len(at.startSentinelComment) + 1
		
	&lt;&lt; append words to pending line, splitting the line if needed &gt;&gt;</t>
<t tx="T1054">@ All inserted newlines are preceeded by whitespace:
we remove trailing whitespace from lines that have not been split.
@c

i = 0
while i &lt; len(s):

	# Scan to the next word.
	word1 = i # Start of the current word.
	word2 = i = skip_ws(s,i)
	while i &lt; len(s) and s[i] not in (' ','\t'):
		i += 1
	word3 = i = skip_ws(s,i)
	
	# trace(s[word1:i])
	
	if leading + word3 - word1 + len(at.pending) &gt;= at.page_width:
		if at.pending:
			# trace("long line",s[word2:word3])
			# Ouput the pending line, and start a new line.
			at.putPending(split=true)
			at.pending = [s[word2:word3]]
		else:
			# Output a long word on a line by itself.
			# trace("long word",s[word2:word3])
			at.pending = [s[word2:word3]]
			at.putPending(split=true)
	else:
		# Append the entire word to the pending line.
		# trace("appending",s[word1:word3])
		at.pending.append(s[word1:word3])
			
# Output the remaining line: no more is left.
at.putPending(split=false)</t>
<t tx="T1055">def putEndDocLine (self):
	
	at = self
	
	at.putPending(split=false)
	
	# Put the closing delimiter if we are using block comments.
	if at.endSentinelComment:
		at.putIndent(at.indent)
		at.os(at.endSentinelComment)
		at.onl() # Note: no trailing whitespace.

	sentinel = choose(at.docKind == at.docDirective,"@-doc","@-at")
	at.putSentinel(sentinel)</t>
<t tx="T1056">def putPending (self,split):
	
	at = self ; s = string.join(at.pending,'') ; at.pending = []
	
	if s and s[-1] == '\n':
		s = s[:-1]
	if not split:
		s = s.rstrip()
	if not s:
		return
		
	#trace(`s`)

	at.putIndent(at.indent)

	if not at.endSentinelComment:
		at.os(at.startSentinelComment) ; at.oblank()

	at.os(s)
	at.onl()</t>
<t tx="T1057"></t>
<t tx="T1058">def findSectionName(self,s,i):
	
	end = s.find('\n',i)
	if end == -1:
		n1 = s.find("&lt;&lt;",i)
		n2 = s.find("&gt;&gt;",i)
	else:
		n1 = s.find("&lt;&lt;",i,end)
		n2 = s.find("&gt;&gt;",i,end)

	return -1 &lt; n1 &lt; n2, n1, n2</t>
<t tx="T1059">def oblank(self):
	self.os(' ')

def oblanks(self,n):
	self.os(' ' * abs(n))

def onl(self):
	self.os(self.output_newline)
	
def os (self,s):
	if s and self.outputFile:
		try:
			s = toEncodedString(s,self.encoding,reportErrors=true)
			self.outputFile.write(s)
		except:
			es("exception writing:" + `s`)
			es_exception()

def otabs(self,n):
	self.os('\t' * abs(n))</t>
<t tx="T1060"># Returns the kind of at-directive or noDirective.

def directiveKind(self,s,i):

	at = self
	n = len(s)
	if i &gt;= n or s[i] != '@':
		j = skip_ws(s,i)
		if match_word(s,j,"@others"):
			return at.othersDirective
		else:
			return at.noDirective

	table = (
		("@c",at.cDirective),
		("@code",at.codeDirective),
		("@doc",at.docDirective),
		("@end_raw",at.endRawDirective),
		#("@others",at.othersDirective), # Now handled above.
		("@raw",at.rawDirective))

	# This code rarely gets executed, so simple code suffices.
	if i+1 &gt;= n or match(s,i,"@ ") or match(s,i,"@\t") or match(s,i,"@\n"):
		# 10/25/02: @space is not recognized in cweb mode.
		# 11/15/02: Noweb doc parts are _never_ scanned in cweb mode.
		return choose(at.language=="cweb",
			at.noDirective,at.atDirective)

	# 10/28/02: @c and @(nonalpha) are not recognized in cweb mode.
	# We treat @(nonalpha) separately because @ is in the colorizer table.
	if at.language=="cweb" and (
		match_word(s,i,"@c") or
		i+1&gt;= n or s[i+1] not in string.letters):
		return at.noDirective

	for name,directive in table:
		if match_word(s,i,name):
			return directive

	# 10/14/02: return miscDirective only for real directives.
	for name in leoColor.leoKeywords:
		if match_word(s,i,name):
			return at.miscDirective

	return at.noDirective</t>
<t tx="T1061"></t>
<t tx="T1062">def nodeSentinelText(self,v):
	
	at = self ; t = v.t ; h = v.headString()
	&lt;&lt; remove comment delims from h if necessary &gt;&gt;
	
	if app().use_gnx and at.using_gnx:
		# Derived files will no longer use gnx's
		#	if t.gnx == None:
		#		t.gnx = at.nodeIndices.getNewIndex()
		#	gnx = at.nodeIndices.toString(t.gnx)
		return h
	else:
		if v == at.root or not v.parent():
			index = str(0)
		else:
			index = str(v.childIndex() + 1)
		return "%s::%s" % (index,h)</t>
<t tx="T1063">@ Bug fix 1/24/03:

If the present @language/@comment settings do not specify a single-line comment we remove all block comment delims from h.  This prevents headline text from interfering with the parsing of node sentinels.
@c

start = at.startSentinelComment
end = at.endSentinelComment

if end and len(end) &gt; 0:
	h = h.replace(start,"")
	h = h.replace(end,"")</t>
<t tx="T1064"># Not used in 4.0 because of findNextWrittenNode.

def putCloseSentinels(self,root,v):
	
	"""Generate @-node sentinels for v up to, but not including, root.
	
	root is an ancestor of v, or root == v."""
	
	at = self

	if not at.using_gnx:
		at.putCloseNodeSentinel(v)
		while 1:
			v = v.parent()
			assert(v) # root must be an ancestor of v.
			if  v == root: break
			at.putCloseNodeSentinel(v)</t>
<t tx="T1065">def putLeadInSentinel (self,s,i,j):
	
	"""Generate @ws or @nonl sentinels as needed to ensure a newline before a group of sentinels.
	The caller must update at.indent before calling this routine:
	This routine skips all leading whitespace!

	i points at the start of a line.
	j points at @others or a section reference."""

	at = self
	# trace(i,j,`s[i:j]`)

	if i == j:
		return # The @others or ref starts a line.

	k = skip_ws(s,i)
	if j == k:
		# Only whitespace before the @others or ref.
		# Unlike other sentinels, the @ws sentinel contributs the whitespace that precedes it.
		at.putSentinel("@ws",putLeadingNewlineFlag=false)
	else:
		at.os(s[k:j])
		at.putSentinel("@nonl",putLeadingNewlineFlag=true)</t>
<t tx="T1066">@ This method is the same as putSentinel except we don't put an opening newline and leading whitespace.
@c
def putOpenLeoSentinel(self,s):
	
	at = self
	
	if not at.sentinels:
		return # Handle @nosentinelsfile.
		
	encoding = at.encoding.lower()
	if encoding != "utf-8":
		s = s + "-encoding=%s." % (encoding)
	
	at.putSentinel(s)</t>
<t tx="T1067">def putOpenNodeSentinel(self,v):
	
	"""Generate @+node sentinel for v."""
	
	at = self

	if v.isAtFileNode() and v != at.root:
		at.writeError("@file not valid in: " + v.headString())
		return
	
	s = at.nodeSentinelText(v)
	at.putSentinel("@+node:" + s)

	# Append the n'th tnode to the root's tnode list.
	if at.using_gnx:
		at.root.tnodeList.append(v.t)</t>
<t tx="T1068"># Not used in 4.0 because of findNextWrittenNode.

def putOpenSentinels(self,root,v):
	
	"""Generate @+node sentinels for v up to, but not including, root.
	
	root is an ancestor of v, or root == v."""
	
	at = self
	
	# trace(at.using_gnx)
	if not at.using_gnx:
		last = root
		while last != v:
			# Set node to v or the ancestor of v that is a child of last.
			node = v
			while node and node.parent() != last:
				node = node.parent()
			assert(node)
			at.putOpenNodeSentinel(node)
			last = node</t>
<t tx="T1069"># This method outputs all sentinels.

def putSentinel(self,s,putLeadingNewlineFlag=false):

	"Put a sentinel whose text is s, applying the CWEB hack if needed."
	
	at = self

	if not at.sentinels:
		return # Handle @file-nosent

	if putLeadingNewlineFlag:
		at.onl()
	at.putIndent(at.indent)
	at.os(at.startSentinelComment)
	&lt;&lt; apply the cweb hack to s &gt;&gt;
	at.os(s)
	if at.endSentinelComment:
		at.os(at.endSentinelComment)
	at.onl()</t>
<t tx="T1070">@ The cweb hack:

If the opening comment delim ends in '@', double all '@' signs except the first, which is "doubled" by the trailing '@' in the opening comment delimiter.
@c

start = at.startSentinelComment
if start and start[-1] == '@':
	assert(s and s[0]=='@')
	s = s.replace('@','@@')[1:]</t>
<t tx="T1071">def sentinelKind(self,s):
	
	at = self
	
	sentinelDict = {
		# Unpaired sentinels: 3.x and 4.x.
		"@comment" : at.startComment,
		"@delims" :  at.startDelims,
		"@verbatim": at.startVerbatim,
		# Unpaired sentinels: 4.x.
		"@afterref" : at.startAfterRef,
		"@nl"       : at.startNl,
		"@nonl"     : at.startNonl,
		"@ws"       : at.startWs,
		# Paired sentinels.
		"@+at":     at.startAt,     "@-at":     at.endAt,
		"@+doc":    at.startDoc,    "@-doc":    at.endDoc,
		"@+leo":    at.startLeo,    "@-leo":    at.endLeo,
		"@+node":   at.startNode,   "@-node":   at.endNode,
		"@+others": at.startOthers, "@-others": at.endOthers }
	
	i = skip_ws(s,0)
	if match(s,i,at.startSentinelComment): 
		i += len(at.startSentinelComment)
	else:
		return at.noSentinel

	# 10/30/02: locally undo cweb hack here
	start = at.startSentinelComment
	if start and len(start) &gt; 0 and start[-1] == '@':
		s = s[:i] + string.replace(s[i:],'@@','@')

	# Do not skip whitespace here!
	if match(s,i,"@&lt;&lt;"): return at.startRef
	if match(s,i,"@@"):   return at.startDirective
	if not match(s,i,'@'): return at.noSentinel
	j = i # start of lookup
	i += 1 # skip the at sign.
	if match(s,i,'+') or match(s,i,'-'):
		i += 1
	i = skip_c_id(s,i)
	key = s[j:i]
	if len(key) &gt; 0 and sentinelDict.has_key(key):
		# trace("found:",key)
		return sentinelDict[key]
	else:
		# trace("not found:",key)
		return at.noSentinel</t>
<t tx="T1072">def skipSentinelStart(self,s,i):

	start = self.startSentinelComment
	assert(start and len(start)&gt;0)

	i = skip_ws(s,i)
	assert(match(s,i,start))
	i += len(start)
	# 7/8/02: Support for REM hack
	i = skip_ws(s,i)
	assert(i &lt; len(s) and s[i] == '@')
	return i + 1
</t>
<t tx="T1073"></t>
<t tx="T1074">### For now: just search the outline for any matching headline.

def createChild (self,headline):
	
	"""Return the vnode whose headline is given."""

	at = self
	headline.strip()

	v = at.root
	after = v.nodeAfterTree()
	while v and v != after:
		h = v.headString().strip()
		if h == headline:
			break
		v = v.threadNext()
			
	if v and v != after:
		# trace(`v`)
		return v
	else:
		at.readError("No node matching headine: %s" % headline)
		return None</t>
<t tx="T1075">def scanText (self,file,v):
	
	"""The new 4.x read code.."""

	at = self
	&lt;&lt; init ivars for scanText &gt;&gt;
	while not at.done:
		s = at.readLine(file)
		if len(s) == 0: break
		# trace(s)
		kind = at.sentinelKind(s)
		if kind == at.noSentinel:
			i = 0
		else:
			i = at.skipSentinelStart(s,0)
		func = at.dispatch_dict[kind]
		func(s,i)

	if not at.done:
		&lt;&lt; report unexpected end of text &gt;&gt;

	return at.lastLines</t>
<t tx="T1076"># Unstacked ivars...
at.done = false
at.inCode = true
at.lastLines = [] # The lines after @-leo
at.leading_ws = ""
at.indent = 0 # Changed only for sentinels.
at.readChildIndex = 0
at.rootSeen = false

# Stacked ivars...
at.endSentinelStack = [at.endLeo] # We have already handled the @+leo sentinel.
at.out = []
at.outStack = []
at.v = v
at.vStack = []</t>
<t tx="T1077">assert(at.endSentinelStack)

at.readError(
	"Unexpected end of file. Expecting %s sentinel" %
	at.sentinelName(at.endSentinelStack[-1]))</t>
<t tx="T1078"></t>
<t tx="T1079">def readStartAt (self,s,i):
	
	"""Read an @+at sentinel."""
	
	at = self ; assert(match(s,i,"+at"))
	at.readStartDocLine(s,i,at.endAt,"@ ")
	
def readStartDoc (self,s,i):
	
	"""Read an @+doc sentinel."""

	at = self ; assert(match(s,i,"+doc"))
	at.readStartDocLine(s,i,at.endDoc,"@doc ")
		
def readStartDocLine (self,s,i,kind,text):
	
	"""Handle common logic for @+at and @+doc sentinels."""
	
	at = self
	at.endSentinelStack.append(kind)
	at.inCode = false
	at.docOut = [text + '\n'] # This newline may be removed by a following @nonl</t>
<t tx="T1080">def readStartLeo (self,s,i):
	
	"""Read an unexpected @+leo sentinel."""

	at = self
	assert(match(s,i,"+leo"))
	at.readError("Ignoring unexpected @+leo sentinel")</t>
<t tx="T1081">def readStartNode (self,s,i):
	
	"""Read an @node sentinel."""
	
	at = self ; assert(match(s,i,"+node:"))
	i += 6
	
	&lt;&lt; Set headline, undoing the CWEB hack &gt;&gt;
	if not at.root_seen:
		at.root_seen = true
		&lt;&lt; Check the filename in the sentinel &gt;&gt;
		newV = at.v
	else:
		newV = at.createChild(headline)
		
	newIndent = skip_leading_ws_with_indent(s,0,at.tab_width)

	at.indentStack.append(at.indent) ; at.indent = newIndent
	at.outStack.append(at.out) ; at.out = []
	at.vStack.append(at.v) ; at.v = newV
	
	at.endSentinelStack.append(at.endNode)</t>
<t tx="T1082"># Set headline to the rest of the line.
# Don't strip leading whitespace."

if len(at.endSentinelComment) == 0:
	headline = s[i:-1].rstrip()
else:
	k = s.rfind(at.endSentinelComment,i)
	headline = s[i:k].rstrip() # works if k == -1

# Undo the CWEB hack: undouble @ signs if the opening comment delim ends in '@'.
if at.startSentinelComment[-1:] == '@':
	headline = headline.replace('@@','@')</t>
<t tx="T1083">h = headline.strip()

if h[:5] == "@file":
	i,junk,junk = scanAtFileOptions(h)
	fileName = string.strip(h[i:])
	if fileName != at.targetFileName:
		at.readError("File name in @node sentinel does not match file's name")
elif h[:8] == "@rawfile":
	fileName = string.strip(h[8:])
	if fileName != at.targetFileName:
		at.readError("File name in @node sentinel does not match file's name")
else:
	at.readError("Missing @file in root @node sentinel")</t>
<t tx="T1084">def readStartOthers (self,s,i):
	
	"""Read an @+others sentinel."""

	at = self
	assert(match(s,i,"+others"))

	# Make sure that the generated at-others is properly indented.
	at.out.append(at.leading_ws + "@others\n")
	
	at.endSentinelStack.append(at.endOthers)</t>
<t tx="T1085"></t>
<t tx="T1086">def readEndAt (self,s,i):
	
	"""Read an @-at sentinel."""

	at = self
	at.readLastDocLine()
	at.popSentinelStack(at.endAt)
	at.inCode = true
		
def readEndDoc (self,s,i):
	
	"""Read an @-doc sentinel."""

	at = self
	at.readLastDocLine()
	at.popSentinelStack(at.endDoc)
	at.inCode = true</t>
<t tx="T1087">def readEndLeo (self,s,i):
	
	"""Read an @-leo sentinel."""
	
	at = self

	# Ignore everything after @-leo.
	# Such lines were presumably written by @last.
	while 1:
		s = at.readLine(at.file)
		if len(s) == 0: break
		at.lastLines.append(s) # Capture all trailing lines, even if empty.

	at.done = true</t>
<t tx="T1088">def readEndNode (self,s,i):
	
	"""Handle end-of-node processing for @-others and @-ref sentinels."""

	at = self
	
	# End raw mode.
	at.raw = false
	
	# End the previous node sentinel.
	s = ''.join(at.out)
	at.v.setBodyStringOrPane(s)

	at.indent = at.indentStack.pop()
	at.out = at.outStack.pop()
	at.v = at.vStack.pop()

	at.popSentinelStack(at.endNode)</t>
<t tx="T1089">def readEndOthers (self,s,i):
	
	"""Read an @-others sentinel."""
	
	at = self
	at.popSentinelStack(at.endOthers)</t>
<t tx="T1090"># This code will typically only be executed for HTML files.

def readLastDocLine (self):
	
	at = self ; end = at.endSentinelComment
	s = ''.join(at.docOut)

	if end:
		s = s.rstrip()	
		# Remove opening block delim.
		
		# Remove closing block delim and maybe a newline from out.
		if s[-n:] == end:
			s = s[:-n]
		if s[-1] == '\n':
			s = s[:-1]
			
	at.out.append(s)
	at.docOut = []</t>
<t tx="T1091"></t>
<t tx="T1092">def  readAfterRef (self,s,i):
	
	"""Read an @afterref sentinel."""
	
	at = self
	assert(match(s,i,"afterref"))
	
	# Append the next line to the text.
	s = at.readLine(at.file)
	at.out.append(s)</t>
<t tx="T1093">def readComment (self,s,i):
	
	"""Read an @comment sentinel."""

	assert(match(s,i,"comment"))

	# Just ignore the comment line!
</t>
<t tx="T1094">def readDelims (self,s,i):
	
	"""Read an @delims sentinel."""
	
	at = self
	assert(match(s,i-1,"@delims"));

	# Skip the keyword and whitespace.
	i0 = i-1
	i = skip_ws(s,i-1+7)
		
	# Get the first delim.
	j = i
	while i &lt; len(s) and not is_ws(s[i]) and not is_nl(s,i):
		i += 1
	
	if j &lt; i:
		at.startSentinelComment = s[j:i]
		# print "delim1:", at.startSentinelComment
	
		# Get the optional second delim.
		j = i = skip_ws(s,i)
		while i &lt; len(s) and not is_ws(s[i]) and not is_nl(s,i):
			i += 1
		end = choose(j&lt;i,s[j:i],"")
		i2 = skip_ws(s,i)
		if end == at.endSentinelComment and (i2 &gt;= len(s) or is_nl(s,i2)):
			at.endSentinelComment = "" # Not really two params.
			line = s[i0:j]
			line = line.rstrip()
			at.out.append(line+'\n')
		else:
			at.endSentinelComment = end
			# print "delim2:",end
			line = s[i0:i]
			line = line.rstrip()
			at.out.append(line+'\n')
	else:
		at.readError("Bad @delims")
		# Append the bad @delims line to the body text.
		at.out.append("@delims")</t>
<t tx="T1095">def readDirective (self,s,i):
	
	"""Read an @@sentinel."""
	
	at = self
	assert(match(s,i,"@")) # The first '@' has already been eaten.
	
	if match_word(s,i,"@raw"):
		at.raw = true
	elif match_word(s,i,"@end_raw"):
		at.raw = false
	
	e = at.endSentinelComment
	s2 = s[i:]
	if len(e) &gt; 0:
		k = s.rfind(e,i)
		if k != -1:
			s2 = s[i:k] + '\n'
		
	start = at.startSentinelComment
	if start and len(start) &gt; 0 and start[-1] == '@':
		s2 = s2.replace('@@','@')

	at.out.append(s2)</t>
<t tx="T1096">def readNl (self,s,i):
	
	"""Handle an @nonl sentinel."""
	
	at = self
	assert(match(s,i,"nl"))
	
	if at.inCode:
		at.out.append('\n')
	else:
		at.docOut.append('\n')</t>
<t tx="T1097">def readNonl (self,s,i):
	
	"""Handle an @nonl sentinel."""
	
	at = self
	assert(match(s,i,"nonl"))
	
	if at.inCode:
		s = ''.join(at.out)
		if s and s[-1] == '\n':
			at.out = [s[:-1]]
		else:
			trace("out:",`s`)
			at.readError("unexpected @nonl directive")
			
	else:
		s = ''.join(at.docOut)
		if s and s[-1] == '\n':
			at.docOut = [s[:-1]]
		else:
			trace("docOut:",`s`)
			at.readError("unexpected @nonl directive")</t>
<t tx="T1098">def readNormalLine (self,s,i):

	at = self
	
	if at.inCode:
		if at.raw:
			i = 0
		else:
			i = at.skipIndent(s,0,at.indent)
		at.out.append(s[i:])
	else:
		&lt;&lt; Skip the leading stuff &gt;&gt;
		&lt;&lt; Append s to docOut &gt;&gt;</t>
<t tx="T1099">if len(at.endSentinelComment) == 0: # Skip the single comment delim and a blank.
	i = skip_ws(s,0)
	if match(s,i,at.startSentinelComment):
		i += len(at.startSentinelComment)
		if match(s,i," "): i += 1
else:
	i = at.skipIndent(s,0, at.indent)
</t>
<t tx="T1100">line = s[i:-1] # remove newline for rstrip.

if line == line.rstrip():
	# no trailing whitespace: the newline is real.
	at.docOut.append(line + '\n')
else:
	# trailing whitespace: the newline is fake.
	at.docOut.append(line)</t>
<t tx="T1101">@ The sentinel contains an @ followed by a section name in angle brackets.  This code is different from the code for the @@ sentinel: the expansion of the reference does not include a trailing newline.
@c

def readRef (self,s,i):
	
	"""Handle an @&lt;&lt; sentinel."""
	
	at = self
	assert(match(s,i,"&lt;&lt;"))
	
	if len(at.endSentinelComment) == 0:
		line = s[i:-1] # No trailing newline
	else:
		k = s.find(at.endSentinelComment,i)
		line = s[i:k] # No trailing newline, whatever k is.
			
	# 10/30/02: undo cweb hack here
	start = at.startSentinelComment
	if start and len(start) &gt; 0 and start[-1] == '@':
		line = line.replace('@@','@')

	at.out.append(line)</t>
<t tx="T1102">def readVerbatim (self,s,i):
	
	"""Read an @verbatim sentinel."""
	
	at = self
	assert(match(s,i,"verbatim"))
	
	# Skip the sentinel.
	s = at.readLine(at.file) 
	
	# Append the next line to the text.
	i = at.skipIndent(s,0,at.indent)
	at.out.append(s[i:])</t>
<t tx="T1103">def readWs (self,s,i):
	
	"""Handle an @nonl sentinel."""
	
	at = self
	assert(match(s,i,"ws"))
	
	i = skip_ws(s,0)
	ws = s[0:i]

	if ws:
		if at.inCode:
			at.out.append(ws)
		else:
			at.docOut.append(ws)</t>
<t tx="T1104">def badEndSentinel (self,expectedKind):
	
	"""Handle a mismatched ending sentinel."""

	at = self
	assert(at.endSentinelStack)
	at.readError("Ignoring %s sentinel.  Expecting %s" %
		(at.sentinelName(at.endSentinelStack[-1]),
		 at.sentinelName(expectedKind)))
		 
def popSentinelStack (self,expectedKind):
	
	"""Pop an entry from endSentinelStack and check it."""
	
	at = self
	if at.endSentinelStack and at.endSentinelStack[-1] == expectedKind:
		at.endSentinelStack.pop()
	else:
		at.badEndSentinel(expectedKind)</t>
<t tx="T1105">def getWsAfterIndentation (self,s,i):
	
	"""Return the whitespace following indention whitespace."""
	
	at = self
	
	j = skip_ws(s,0)

	if at.raw:
		i = 0
	else:
		i = at.skipIndent(s,0,at.indent)

	return s[i:j]</t>
</tnodes>
</leo_file>
