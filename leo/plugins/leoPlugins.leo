<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="939" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="19" left="287" height="886" width="873"/>
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
<v t="T2"><vh>sept 03</vh>
<v t="T3"><vh>9/18</vh>
<v t="T4"><vh>Fixed some (all?) problems with tnodeList</vh></v>
<v t="T5"><vh>All files now pass the file-compare (semantic test)</vh></v>
<v t="T6"><vh>Fixed @others bug</vh></v>
</v>
<v t="T7"><vh>9/17</vh>
<v t="T8"><vh>Wrote compare script</vh></v>
<v t="T9"><vh>Wrote Import Derived File command</vh></v>
</v>
<v t="T10"><vh>9/16</vh>
<v t="T11"><vh>Changed how @ws sentinel works</vh></v>
<v t="T12"><vh>Properly indent @nl sentinels</vh></v>
<v t="T13"><vh>Fixed bugs in putting doc parts</vh></v>
<v t="T14"><vh>Fixed bugs in readLastDocLine</vh></v>
</v>
<v t="T15"><vh>9/14</vh>
<v t="T16"><vh>Added ignoreOldSentinel to warn about 3.x sentinels</vh></v>
<v t="T17"><vh>Milestone: first successful use of hidden machinery</vh></v>
<v t="T18"><vh>Rewrote createChild and renamed it to findChild</vh></v>
<v t="T19"><vh>Added check to see whether read is the same as the write.</vh></v>
<v t="T20"><vh>Added support for tnodeList</vh></v>
</v>
<v t="T21"><vh>9/13 work on 4.0 read code</vh></v>
</v>
<v t="T22"><vh>7/7 Created leoPlugins.leo</vh></v>
</v>
<v t="T23"><vh>Documentation and security warnings</vh>
<v t="T24"><vh>Overview of plugins and hooks</vh></v>
<v t="T25"><vh>Intro to scripts</vh></v>
<v t="T26"><vh>About hooks</vh></v>
<v t="T27"><vh>Hooks should never blindly Python scripts</vh></v>
<v t="T28"><vh>NEVER use this kind of code in a hook!!</vh></v>
</v>
<v t="T29"><vh>Plugins</vh>
<v t="T30" a="M"><vh> To do</vh>
<v t="T31"><vh>(Improve Spell Checking)</vh></v>
</v>
<v t="T32"><vh>Commands</vh>
<v t="T33"><vh> Importing Cisco configuration files</vh>
<v t="T34"><vh>@file import_cisco_config.py</vh>
<v t="T35"><vh>&lt;&lt; about this plugin &gt;&gt;</vh></v>
<v t="T36"><vh>create_import_cisco_menu</vh></v>
<v t="T37"><vh>importCiscoConfig</vh>
<v t="T38"><vh>&lt;&lt; open file &gt;&gt;</vh></v>
<v t="T39"><vh>&lt;&lt; process custom line &gt;&gt;</vh></v>
<v t="T40"><vh>&lt;&lt; process indented block &gt;&gt;</vh></v>
<v t="T41"><vh>&lt;&lt; complete outline &gt;&gt;</vh></v>
</v>
</v>
<v t="T42"><vh> Example of an imported config</vh>
<v t="T43"><vh>plain configuration</vh></v>
<v t="T44"><vh>cisco config: C:/Davide/Leo/CVS Version/example_conf.txt</vh>
<v t="T45"><vh>&lt;&lt;access-list&gt;&gt;</vh></v>
<v t="T46"><vh>&lt;&lt;boot&gt;&gt;</vh></v>
<v t="T47"><vh>&lt;&lt;controller&gt;&gt;</vh>
<v t="T48"><vh>controller E1 5/0/0</vh></v>
<v t="T49"><vh>controller E1 5/0/1</vh></v>
<v t="T50"><vh>controller SONET 1/0/0</vh></v>
</v>
<v t="T51"><vh>&lt;&lt;interface&gt;&gt;</vh>
<v t="T52"><vh>interface Async1</vh></v>
<v t="T53"><vh>interface Dialer0</vh></v>
<v t="T54"><vh>interface FastEthernet0/0/0</vh></v>
<v t="T55"><vh>interface FastEthernet0/0/1</vh></v>
<v t="T56"><vh>interface FastEthernet0/0/1.1</vh></v>
<v t="T57"><vh>interface FastEthernet0/0/1.2</vh></v>
<v t="T58"><vh>interface FastEthernet0/0/1.3</vh></v>
<v t="T59"><vh>interface FastEthernet0/0/1.5</vh></v>
<v t="T60"><vh>interface FastEthernet0/0/1.50</vh></v>
<v t="T61"><vh>interface Loopback0</vh></v>
<v t="T62"><vh>interface POS4/1/0</vh></v>
<v t="T63"><vh>interface Serial5/0/0:1</vh></v>
<v t="T64"><vh>interface Serial5/0/0:2</vh></v>
<v t="T65"><vh>interface Serial5/0/1:0</vh></v>
<v t="T66"><vh>interface Serial5/1/0</vh></v>
<v t="T67"><vh>interface Serial5/1/1</vh></v>
</v>
<v t="T68"><vh>&lt;&lt;ip community-list&gt;&gt;</vh></v>
<v t="T69"><vh>&lt;&lt;ip route&gt;&gt;</vh></v>
<v t="T70"><vh>&lt;&lt;line&gt;&gt;</vh>
<v t="T71"><vh>line aux 0</vh></v>
<v t="T72"><vh>line vty 0 4</vh></v>
</v>
<v t="T73"><vh>&lt;&lt;logging&gt;&gt;</vh></v>
<v t="T74"><vh>&lt;&lt;ntp&gt;&gt;</vh></v>
<v t="T75"><vh>&lt;&lt;route-map&gt;&gt;</vh>
<v t="T76"><vh>route-map only permit 2</vh></v>
<v t="T77"><vh>route-map only1 permit 10</vh></v>
<v t="T78"><vh>route-map only3 permit 10</vh></v>
<v t="T79"><vh>route-map tag_com permit 10</vh></v>
<v t="T80"><vh>route-map tag_com permit 20</vh></v>
</v>
<v t="T81"><vh>&lt;&lt;router&gt;&gt;</vh>
<v t="T82"><vh>router bgp 65001</vh></v>
<v t="T83"><vh>router ospf 1</vh></v>
</v>
<v t="T84"><vh>&lt;&lt;service&gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="T85"><vh>@file outline_export.py</vh>
<v t="T86"><vh>newMoreHead</vh></v>
</v>
</v>
<v t="T87"><vh>Debugging</vh>
<v t="T88"><vh>@file dump_globals.py</vh>
<v t="T89"><vh>onStart</vh></v>
</v>
<v t="T90"><vh>@file enable_gc.py</vh>
<v t="T91"><vh>onStart</vh></v>
</v>
<v t="T92"><vh>@file trace_gc.py</vh></v>
<v t="T93"><vh>@file trace_keys.py</vh>
<v t="T94"><vh>onKey</vh></v>
</v>
<v t="T95"><vh>@file trace_tags.py</vh>
<v t="T96"><vh>trace_tags</vh></v>
</v>
</v>
<v t="T97"><vh>Directives</vh>
<v t="T98"><vh>@file add_directives.py</vh>
<v t="T99"><vh>addPluginDirectives</vh></v>
<v t="T100"><vh>scanPluginDirectives</vh></v>
</v>
</v>
<v t="T101"><vh>Drawing, graphics &amp; styled text</vh>
<v t="T102"><vh>@file color_markup.py</vh>
<v t="T103"><vh>initAnyMarkup</vh></v>
<v t="T104"><vh>colorWikiMarkup</vh></v>
<v t="T105"><vh>doWikiText</vh>
<v t="T106"><vh>&lt;&lt; set first to a tuple describing the first tag to be handled &gt;&gt;</vh></v>
<v t="T107"><vh>&lt;&lt; handle the tag using n1,n2,delim1,delim2 &gt;&gt;</vh>
<v t="T108"><vh>&lt;&lt; parse and handle color field &gt;&gt;</vh></v>
</v>
</v>
<v t="T109"><vh>insertWikiPicture</vh></v>
</v>
<v t="T110"><vh>@file image.py</vh>
<v t="T111"><vh>onSelect</vh>
<v t="T112"><vh>&lt;&lt; Select Image &gt;&gt;</vh></v>
</v>
<v t="T113"><vh>onUnselect</vh>
<v t="T114"><vh>&lt;&lt; Unselect Image &gt;&gt;</vh></v>
</v>
</v>
<v t="T115"><vh>@file nav_buttons.py</vh>
<v t="T116"><vh>class commanderInfoClass</vh>
<v t="T117"><vh>__init__ (commanderInfoClass)</vh></v>
<v t="T118"><vh>addWidgets</vh>
<v t="T119"><vh>&lt;&lt; define callbacks &gt;&gt;</vh></v>
</v>
<v t="T120"><vh>createImage</vh></v>
<v t="T121"><vh>updateNavButtons (nav_buttons.py)</vh></v>
<v t="T122"><vh>Callbacks</vh>
<v t="T123"><vh>marksButtonCallback</vh></v>
<v t="T124"><vh>recentButtonCallback</vh></v>
</v>
</v>
<v t="T125"><vh>class globalInfoClass</vh>
<v t="T126"><vh>__init__ ( globalInfoClass)</vh></v>
<v t="T127"><vh>addNavWidgets</vh></v>
<v t="T128"><vh>destroyFrame, destroyAllFrames, destroyOneFrame</vh></v>
<v t="T129"><vh>updateRecentSections</vh></v>
<v t="T130"><vh>updateMarks &amp; updateMarksAfterCommand</vh></v>
<v t="T131"><vh>updateNavButtons</vh></v>
</v>
<v t="T132"><vh>class marksDialog (listBoxDialog)</vh>
<v t="T133"><vh>marksDialog.__init__</vh></v>
<v t="T134"><vh>createFrame</vh></v>
<v t="T135"><vh>addbuttons</vh></v>
<v t="T136"><vh>fillbox</vh></v>
</v>
<v t="T137"><vh>class recentSectionsDialog (listBoxDialog)</vh>
<v t="T138"><vh>__init__  recentSectionsDialog</vh></v>
<v t="T139"><vh>addButtons</vh></v>
<v t="T140"><vh>clearAll</vh></v>
<v t="T141"><vh>createFrame</vh></v>
<v t="T142"><vh>deleteEntry</vh></v>
<v t="T143"><vh>destroy</vh></v>
<v t="T144"><vh>fillbox (recent sections)</vh>
<v t="T145"><vh>&lt;&lt; reconstruct the contents of self.box &gt;&gt;&gt;</vh></v>
</v>
<v t="T146"><vh>synchNavButtons</vh></v>
</v>
</v>
</v>
<v t="T147"><vh>External editors &amp; Open With</vh>
<v t="T148"><vh>@file open_with.py</vh>
<v t="T149"><vh>on_idle</vh>
<v t="T150"><vh>&lt;&lt; update v's body text &gt;&gt;</vh>
<v t="T151"><vh>&lt;&lt; set s to the file text &gt;&gt;</vh></v>
</v>
</v>
<v t="T152"><vh>create_open_with_menu</vh>
<v t="T153"><vh>&lt;&lt; create the Open With menu &gt;&gt;</vh></v>
</v>
</v>
<v t="T154"><vh>@file vim.py</vh>
<v t="T155"><vh>open_in_vim</vh></v>
</v>
<v t="T156"><vh>@file xemacs.py</vh></v>
</v>
<v t="T157"><vh>Files</vh>
<v t="T158"><vh>@file empty_leo_file.py</vh>
<v t="T159"><vh>&lt;&lt; define minimal .leo file &gt;&gt;</vh></v>
<v t="T160"><vh>onOpen</vh></v>
</v>
<v t="T161"><vh>@file open_shell.py</vh>
<v t="T162"><vh>&lt;&lt; about the open shell plugin &gt;&gt;</vh></v>
<v t="T163"><vh>load_menu</vh></v>
<v t="T164"><vh>_getpath</vh></v>
<v t="T165"><vh>_getcurrentnodepath</vh></v>
<v t="T166"><vh>launchCmd</vh></v>
<v t="T167"><vh>launchExplorer</vh></v>
<v t="T168"><vh>launchxTerm</vh></v>
</v>
</v>
<v t="T169"><vh>Foreign languages</vh>
<v t="T170"><vh>@file french.py</vh>
<v t="T171"><vh>onMenu</vh></v>
</v>
<v t="T172"><vh>@file french_fm.py</vh>
<v t="T173"><vh>onMenu</vh></v>
</v>
</v>
<v t="T174"><vh>Key bindings</vh>
<v t="T175"><vh>@file arrows.py</vh>
<v t="T176"><vh>onOpen</vh></v>
</v>
</v>
<v t="T177"><vh>Menus</vh>
<v t="T178"><vh> Plugins menu</vh>
<v t="T179"><vh>@file plugins_menu.py</vh>
<v t="T180"><vh>class Plugin</vh>
<v t="T181"><vh>__init__</vh>
<v t="T182"><vh>&lt;&lt; Check if this can be configured &gt;&gt;</vh></v>
<v t="T183"><vh>&lt;&lt; Check if this has an apply &gt;&gt;</vh></v>
<v t="T184"><vh>&lt;&lt; Look for additional commands &gt;&gt;</vh></v>
</v>
<v t="T185"><vh>about</vh></v>
<v t="T186"><vh>properties</vh></v>
</v>
<v t="T187"><vh>class PropertiesWindow</vh>
<v t="T188"><vh>__init__</vh>
<v t="T189"><vh>&lt;&lt; initialize all ivars &gt;&gt;</vh></v>
<v t="T190"><vh>&lt;&lt; create the frame from the configuration data &gt;&gt;</vh>
<v t="T191"><vh>&lt;&lt; Create the top level and the main frame &gt;&gt;</vh></v>
<v t="T192"><vh>&lt;&lt; Create widgets for each section and option &gt;&gt;</vh></v>
<v t="T193"><vh>&lt;&lt; Create Ok, Cancel and Apply buttons &gt;&gt;</vh></v>
</v>
</v>
<v t="T194"><vh>Event Handlers</vh></v>
<v t="T195"><vh>writeConfiguration</vh></v>
</v>
<v t="T196"><vh>class PluginAbout</vh>
<v t="T197"><vh>__init__</vh>
<v t="T198"><vh>&lt;&lt; Create the contents of the about box &gt;&gt;</vh></v>
<v t="T199"><vh>&lt;&lt; Create the close button &gt;&gt;</vh></v>
</v>
</v>
<v t="T200"><vh>createPluginsMenu</vh>
<v t="T201"><vh>&lt;&lt; add items to the plugins menu &gt;&gt;</vh></v>
</v>
</v>
<v t="T202"><vh>@file test.py</vh>
<v t="T203"><vh>applyConfiguration</vh></v>
<v t="T204"><vh>cmd_fn1/2/3</vh></v>
<v t="T205"><vh>onSelect</vh>
<v t="T206"><vh>&lt;&lt; Select Image &gt;&gt;</vh></v>
</v>
<v t="T207"><vh>onUnselect</vh>
<v t="T208"><vh>&lt;&lt; Unselect Image &gt;&gt;</vh></v>
</v>
</v>
<v t="T209"><vh>Notes re plugins menu</vh>
<v t="T210"><vh> Changes made by E.K.Ream</vh></v>
<v t="T211"><vh> Design</vh></v>
<v t="T212"><vh> Initial suggestion from Paul Paterson</vh></v>
</v>
</v>
<v t="T213"><vh>@file scripts_menu.py</vh>
<v t="T214"><vh>createScriptsMenu</vh>
<v t="T215"><vh>&lt;&lt; Return if no scripts exist anywhere &gt;&gt;</vh></v>
<v t="T216"><vh>&lt;&lt; Create top-level entries for every script in top_scripts &gt;&gt;</vh></v>
<v t="T217"><vh>&lt;&lt; Create a submenu for dir containing each file in files &gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="T218"><vh>New kinds of nodes</vh>
<v t="T219"><vh>@file at_folder.py</vh>
<v t="T220"><vh>&lt;&lt; about this plugin &gt;&gt;</vh></v>
<v t="T221"><vh>sync_node_to_folder</vh></v>
</v>
<v t="T222"><vh>@file read_only_nodes.py</vh>
<v t="T223"><vh>documentation for @read-only nodes</vh>
<v t="T224"><vh>ftp/http access</vh></v>
</v>
<v t="T225"><vh>class FTPurl</vh>
<v t="T226"><vh>__init__</vh></v>
<v t="T227"><vh>Getters</vh>
<v t="T228"><vh>read</vh></v>
<v t="T229"><vh>readline</vh></v>
</v>
<v t="T230"><vh>Setters</vh>
<v t="T231"><vh>write</vh></v>
</v>
<v t="T232"><vh>Utilities</vh>
<v t="T233"><vh>seek</vh></v>
<v t="T234"><vh>flush</vh></v>
<v t="T235"><vh>dir</vh></v>
<v t="T236"><vh>exists</vh></v>
<v t="T237"><vh>checkParams</vh></v>
</v>
<v t="T238"><vh>close</vh></v>
</v>
<v t="T239"><vh>enable/disable_body</vh></v>
<v t="T240"><vh>insert_read_only_node (FTP version)</vh>
<v t="T241"><vh>&lt;&lt; convert HTML to text &gt;&gt;</vh></v>
</v>
<v t="T242"><vh>on_open2</vh></v>
<v t="T243"><vh>on_bodykey1</vh></v>
<v t="T244"><vh>on_headkey2</vh></v>
<v t="T245"><vh>on_select1</vh></v>
<v t="T246"><vh>on_select2</vh></v>
</v>
<v t="T247"><vh>@file rst.py</vh>
<v t="T248"><vh>&lt;&lt;about this plugin &gt;&gt;</vh></v>
<v t="T249"><vh>&lt;&lt; change log &gt;&gt;</vh></v>
<v t="T250"><vh>onIconDoubleClick</vh>
<v t="T251"><vh>&lt;&lt; write rST as HTML &gt;&gt;</vh>
<v t="T252"><vh>&lt;&lt; convert rST to HTML &gt;&gt;</vh></v>
</v>
<v t="T253"><vh>&lt;&lt; write rST file &gt;&gt;</vh></v>
</v>
<v t="T254"><vh>writeTreeAsRst</vh></v>
<v t="T255"><vh>underline</vh></v>
</v>
<v t="T256"><vh>@file startfile.py</vh>
<v t="T257"><vh>&lt;&lt;about this plugin &gt;&gt;</vh></v>
<v t="T258"><vh>&lt;&lt; change log &gt;&gt;</vh></v>
<v t="T259"><vh>onIconDoubleClick</vh>
<v t="T260"><vh>&lt;&lt; find path and start file &gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="T261"><vh>Overriding functions, methods &amp; classes</vh>
<v t="T262"><vh>@file __overrideClasses.py</vh>
<v t="T263"><vh>&lt;&lt; override the LeoFrame class &gt;&gt;</vh></v>
<v t="T264"><vh>&lt;&lt; override methods of the LeoApp class &gt;&gt;</vh></v>
</v>
<v t="T265"><vh>@file override_commands.py</vh>
<v t="T266"><vh>onCommand</vh></v>
</v>
<v t="T267"><vh>@file redefine_put.py</vh>
<v t="T268"><vh>onStart</vh></v>
<v t="T269"><vh>newPut and newPutNl</vh></v>
</v>
<v t="T270"><vh>@file redirect_to_log.py</vh></v>
<v t="T271"><vh>@file script_io_to_body.py</vh>
<v t="T272"><vh>onStart</vh></v>
<v t="T273"><vh>newExecuteScript</vh></v>
<v t="T274"><vh>newPut and newPutNl</vh></v>
<v t="T275"><vh>newEs, etc.</vh></v>
</v>
</v>
<v t="T276"><vh>Spell Checking</vh>
<v t="T277"><vh>@silentfile mod_spelling.txt</vh></v>
<v t="T278"><vh>@file mod_spelling.ini</vh></v>
<v t="T279"><vh>@file mod_spelling.py</vh>
<v t="T280"><vh>Functions</vh>
<v t="T281"><vh>createSpellMenu</vh></v>
<v t="T282"><vh>onSelect</vh></v>
<v t="T283"><vh>onCommand</vh></v>
</v>
<v t="T284"><vh>class Aspell</vh>
<v t="T285"><vh>Birth &amp; death</vh>
<v t="T286"><vh>__init__</vh></v>
<v t="T287"><vh>getAspellDirectory</vh></v>
</v>
<v t="T288"><vh>openPipes</vh>
<v t="T289"><vh>&lt;&lt; Ensure local dictionary is present &gt;&gt;</vh></v>
</v>
<v t="T290"><vh>closePipes</vh></v>
<v t="T291"><vh>listAlternates</vh></v>
<v t="T292"><vh>processWord</vh></v>
<v t="T293"><vh>updateDictionary</vh></v>
</v>
<v t="T294"><vh>class spellDialog</vh>
<v t="T295"><vh>Birth &amp; death</vh>
<v t="T296"><vh>spell.__init__</vh>
<v t="T297"><vh>&lt;&lt; set self.dictionary &gt;&gt;</vh></v>
</v>
<v t="T298"><vh>getLocalDictionary</vh></v>
<v t="T299"><vh>getLocalLanguageCode</vh></v>
<v t="T300"><vh>readLocalDictionary</vh></v>
</v>
<v t="T301"><vh>createFrame</vh>
<v t="T302"><vh>&lt;&lt; Create the text and suggestion panes &gt;&gt;</vh></v>
<v t="T303"><vh>&lt;&lt; Create the spelling buttons &gt;&gt;</vh></v>
</v>
<v t="T304"><vh>Buttons</vh>
<v t="T305"><vh>onAddButton</vh></v>
<v t="T306"><vh>onIgnoreButton</vh></v>
<v t="T307"><vh>onChangeButton &amp; onChangeThenFindButton</vh></v>
<v t="T308"><vh>onFindButton</vh></v>
<v t="T309"><vh>onHideButton</vh></v>
<v t="T310"><vh>onRedoButton &amp; onUndoButton</vh></v>
</v>
<v t="T311"><vh>Commands</vh>
<v t="T312"><vh>add</vh></v>
<v t="T313"><vh>change</vh></v>
<v t="T314"><vh>checkSpelling</vh></v>
<v t="T315"><vh>find</vh></v>
<v t="T316"><vh>ignore</vh></v>
</v>
<v t="T317"><vh>Helpers</vh>
<v t="T318"><vh>closePipes</vh></v>
<v t="T319"><vh>fillbox</vh></v>
<v t="T320"><vh>findNextMisspelledWord</vh>
<v t="T321"><vh>&lt;&lt; Skip word if ignored or in local dictionary &gt;&gt;</vh></v>
</v>
<v t="T322"><vh>findNextWord</vh></v>
<v t="T323"><vh>getSuggestion</vh></v>
<v t="T324"><vh>onMap</vh></v>
<v t="T325"><vh>onSelectListBox</vh></v>
<v t="T326"><vh>update</vh></v>
<v t="T327"><vh>updateButtons</vh></v>
</v>
</v>
</v>
</v>
<v t="T328" a="M"><vh>New</vh>
<v t="T329"><vh>mod_autosave</vh>
<v t="T330"><vh>@file mod_autosave.ini</vh></v>
<v t="T331"><vh>@file mod_autosave.py</vh>
<v t="T332"><vh>applyConfiguration</vh></v>
<v t="T333"><vh>autosave</vh></v>
</v>
</v>
<v t="T334"><vh>@file mod_timestamp.py</vh>
<v t="T335"><vh>timestamp</vh></v>
</v>
</v>
</v>
<v t="T336"><vh>(Settings menu)</vh>
<v t="T337"><vh>To do</vh></v>
<v t="T338"><vh>Design of Settings menu</vh></v>
<v t="T339"><vh>@file settings_menu.py</vh>
<v t="T340"><vh>createSettingsMenu</vh></v>
</v>
</v>
<v t="T341"><vh>(wxStuff: not a plugin yet)</vh>
<v t="T342"><vh>wxTests</vh>
<v t="T343"><vh>@file c:\prog\test\wxTest.py</vh></v>
</v>
<v t="T344"><vh>old wxLeo code (imported C++ code)</vh>
<v t="T345"><vh>alert.cpp</vh>
<v t="T346"><vh>alert</vh></v>
<v t="T347"><vh>assertFailedDialog</vh></v>
</v>
<v t="T348"><vh>FindPanel.cpp</vh>
<v t="T349"><vh>&lt;&lt; FindPanel declarations &gt;&gt;</vh></v>
<v t="T350" a="M"><vh>BEGIN_EVENT_TABLE</vh></v>
<v t="T351" a="M"><vh>ctor</vh></v>
<v t="T352"><vh>OnActivateFindFrame</vh></v>
<v t="T353"><vh>OnSetFocus</vh></v>
<v t="T354"><vh>OnCloseFindFrame</vh></v>
<v t="T355"><vh>OnChangeButton</vh></v>
<v t="T356"><vh>OnChangeAllButton</vh></v>
<v t="T357"><vh>OnChangeThenFindButton</vh></v>
<v t="T358"><vh>OnFindButton</vh></v>
<v t="T359"><vh>OnFindAllButton</vh></v>
<v t="T360"><vh>OnBatchCheckBox</vh></v>
<v t="T361"><vh>OnIgnoreCaseCheckBox</vh></v>
<v t="T362"><vh>OnMarkChangesCheckBox</vh></v>
<v t="T363"><vh>OnMarkFindsCheckBox</vh></v>
<v t="T364"><vh>OnPatternMatchCheckBox</vh></v>
<v t="T365"><vh>OnReverseCheckBox</vh></v>
<v t="T366"><vh>OnSearchBodyTextCheckBox</vh></v>
<v t="T367"><vh>OnSearchHeadlineCheckBox</vh></v>
<v t="T368"><vh>OnSuboutlineOnlyCheckBox</vh></v>
<v t="T369"><vh>OnWrapAroundCheckBox</vh></v>
<v t="T370"><vh>OnWholeWordCheckBox</vh></v>
<v t="T371"><vh>OnChangeText</vh></v>
<v t="T372"><vh>OnFindText</vh></v>
<v t="T373"><vh>set_check_boxes</vh></v>
<v t="T374"><vh>FindPanel</vh></v>
</v>
<v t="T375" a="M"><vh>LeoApp.cpp</vh>
<v t="T376" a="M"><vh>Event table</vh></v>
<v t="T377"><vh>OnInit</vh>
<v t="T378"><vh>&lt;&lt; Switch to the other running copy of Leo if one is already open &gt;&gt;</vh></v>
<v t="T379"><vh>&lt;&lt; Set gAppDirectory &gt;&gt;</vh></v>
<v t="T380"><vh>&lt;&lt; Open a file when double-clicking an icon &gt;&gt;</vh></v>
<v t="T381"><vh>&lt;&lt; Create a frame and link it into the global frame list &gt;&gt;</vh></v>
<v t="T382"><vh>&lt;&lt; Initialize Sherlock &gt;&gt;</vh></v>
<v t="T383"><vh>&lt;&lt; Dump the command line &gt;&gt;</vh></v>
</v>
<v t="T384"><vh>OnExit</vh></v>
<v t="T385"><vh>init_args</vh></v>
<v t="T386"><vh>wxFindAppPath</vh></v>
<v t="T387"><vh>log_open</vh></v>
<v t="T388"><vh>put_cstring_to_log_window</vh></v>
</v>
<v t="T389" a="M"><vh>LeoFrame.cpp</vh>
<v t="T390" a="M"><vh>BEGIN_EVENT_TABLE</vh>
<v t="T391"><vh>&lt;&lt; Declare menu events &gt;&gt;</vh></v>
</v>
<v t="T392" a="M"><vh>ctor</vh>
<v t="T393"><vh>&lt;&lt; Initialize the private vars &gt;&gt;</vh></v>
<v t="T394"><vh>&lt;&lt; Initialize the argument settings &gt;&gt;</vh></v>
<v t="T395"><vh>&lt;&lt; Create the splitter windows &gt;&gt;</vh></v>
<v t="T396"><vh>&lt;&lt; Create the accelerator table &gt;&gt;</vh></v>
<v t="T397"><vh>&lt;&lt; Create the status bar &gt;&gt;</vh></v>
<v t="T398"><vh>&lt;&lt; Set the window Icon &gt;&gt;</vh></v>
<v t="T399"><vh>&lt;&lt; Set the caret blink rate &gt;&gt;</vh></v>
<v t="T400"><vh>&lt;&lt; Add root node to the tree view &gt;&gt;</vh></v>
</v>
<v t="T401"><vh>createMenus</vh></v>
<v t="T402"><vh>SetUntitledNumber</vh></v>
<v t="T403"><vh>putToLog</vh></v>
<v t="T404"><vh>getLogText</vh></v>
<v t="T405"><vh>event handlers</vh>
<v t="T406"><vh>onActivate</vh></v>
<v t="T407"><vh>OnSetFocus</vh></v>
<v t="T408"><vh>onResize</vh></v>
<v t="T409"><vh>onBodyTextUpdated</vh></v>
<v t="T410"><vh>onCloseLeoFrame</vh></v>
<v t="T411"><vh>onTreeChanged</vh></v>
<v t="T412"><vh>onTreeChanging</vh></v>
<v t="T413"><vh>onTreeKeyDown</vh></v>
<v t="T414"><vh>onTreeBeginDrag</vh></v>
<v t="T415"><vh>onTreeEndDrag</vh></v>
<v t="T416"><vh>onTreeBeginLabelEdit</vh></v>
<v t="T417"><vh>onTreeEndLabelEdit</vh></v>
<v t="T418"><vh>updateJoinedHeadlines</vh></v>
<v t="T419"><vh>OnUpdateRevert</vh></v>
<v t="T420"><vh>OnNew</vh></v>
<v t="T421"><vh>OnOpen</vh></v>
<v t="T422"><vh>OpenWithFileName</vh></v>
<v t="T423"><vh>OnClose</vh></v>
<v t="T424"><vh>OnSave</vh></v>
<v t="T425"><vh>OnSaveAs</vh></v>
<v t="T426"><vh>OnSaveTo</vh></v>
<v t="T427"><vh>OnRevert</vh></v>
<v t="T428"><vh>OnPageSetup</vh></v>
<v t="T429"><vh>OnPrint</vh></v>
<v t="T430"><vh>OnTangleSubmenu</vh></v>
<v t="T431"><vh>OnUntangleSubmenu</vh></v>
<v t="T432"><vh>OnImportExportSubmenu</vh></v>
<v t="T433"><vh>OnQuit</vh></v>
<v t="T434"><vh>OnReadOutlineOnly</vh></v>
<v t="T435"><vh>readOutlineOnly</vh></v>
<v t="T436"><vh>OnReadAtFileNodes</vh></v>
<v t="T437"><vh>OnWriteOutlineOnly</vh></v>
<v t="T438"><vh>OnWriteAtFileNodes</vh></v>
<v t="T439"><vh>OnTangleAll</vh></v>
<v t="T440"><vh>OnTangleMarked</vh></v>
<v t="T441"><vh>OnTangle</vh></v>
<v t="T442"><vh>OnUntangleAll</vh></v>
<v t="T443"><vh>OnUntangleMarked</vh></v>
<v t="T444"><vh>OnUntangle</vh></v>
<v t="T445"><vh>OnImportFiles</vh></v>
<v t="T446"><vh>OnImportCWEBFiles</vh></v>
<v t="T447"><vh>OnImportNowebFiles</vh></v>
<v t="T448"><vh>OnImportMoreText</vh></v>
<v t="T449"><vh>OnFlattenOutline</vh></v>
<v t="T450"><vh>OnUpdateCopy</vh></v>
<v t="T451"><vh>OnUpdateCut</vh></v>
<v t="T452"><vh>OnUpdateDelete</vh></v>
<v t="T453"><vh>OnUpdateExtract</vh></v>
<v t="T454"><vh>OnUpdateExtractNames</vh></v>
<v t="T455"><vh>OnUpdateExtractSection</vh></v>
<v t="T456"><vh>OnUpdateFind</vh></v>
<v t="T457"><vh>OnUpdatePaste</vh></v>
<v t="T458"><vh>OnUpdateRedo</vh></v>
<v t="T459"><vh>OnUpdateReplace</vh></v>
<v t="T460"><vh>OnUpdateSelectAll</vh></v>
<v t="T461"><vh>OnUpdateUndo</vh></v>
<v t="T462"><vh>hasSelection</vh></v>
<v t="T463"><vh>OnUndo</vh></v>
<v t="T464"><vh>OnRedo</vh></v>
<v t="T465"><vh>OnCut</vh></v>
<v t="T466"><vh>OnCopy</vh></v>
<v t="T467"><vh>OnPaste</vh></v>
<v t="T468"><vh>OnDelete</vh></v>
<v t="T469"><vh>OnSelectAll</vh></v>
<v t="T470"><vh>OnEditHeadline</vh></v>
<v t="T471"><vh>OnFontPanel</vh></v>
<v t="T472"><vh>OnSyntaxColoring</vh></v>
<v t="T473"><vh>OnPreferences</vh></v>
<v t="T474"><vh>OnConvertBlanks</vh></v>
<v t="T475"><vh>OnExtractSection</vh></v>
<v t="T476"><vh>OnExtractNames</vh></v>
<v t="T477"><vh>OnExtract</vh></v>
<v t="T478"><vh>OnFindPanel</vh></v>
<v t="T479"><vh>OnFindNext</vh></v>
<v t="T480"><vh>OnFindPrevious</vh></v>
<v t="T481"><vh>OnReplace</vh></v>
<v t="T482"><vh>OnReplaceThenFind</vh></v>
<v t="T483"><vh>OnUpdateCutNode</vh></v>
<v t="T484"><vh>OnUpdateDeleteNode</vh></v>
<v t="T485"><vh>OnUpdatePasteNode</vh></v>
<v t="T486"><vh>OnUpdateSortNode</vh></v>
<v t="T487"><vh>OnUpdateExpandAll</vh></v>
<v t="T488"><vh>OnUpdateExpandAllChildren</vh></v>
<v t="T489"><vh>OnUpdateExpandChildren</vh></v>
<v t="T490"><vh>OnUpdateContractAll</vh></v>
<v t="T491"><vh>OnUpdateContractAllChildren</vh></v>
<v t="T492"><vh>OnUpdateContractChildren</vh></v>
<v t="T493"><vh>OnUpdateMoveDown</vh></v>
<v t="T494"><vh>OnUpdateMoveLeft</vh></v>
<v t="T495"><vh>OnUpdateMoveRight</vh></v>
<v t="T496"><vh>OnUpdateMoveUp</vh></v>
<v t="T497"><vh>OnUpdatePromote</vh></v>
<v t="T498"><vh>OnUpdateDemote</vh></v>
<v t="T499"><vh>OnUpdateGoPrevVisible</vh></v>
<v t="T500"><vh>OnUpdateGoNextVisible</vh></v>
<v t="T501"><vh>OnUpdateGoBack</vh></v>
<v t="T502"><vh>OnUpdateGoNext</vh></v>
<v t="T503"><vh>OnUpdateMark</vh></v>
<v t="T504"><vh>OnUpdateMarkSubheads</vh></v>
<v t="T505"><vh>OnUpdateMarkChangedItems</vh></v>
<v t="T506"><vh>OnUpdateMarkChangedRoots</vh></v>
<v t="T507"><vh>OnUpdateGoToNextMarked</vh></v>
<v t="T508"><vh>OnUpdateGoToNextChanged</vh></v>
<v t="T509"><vh>OnCutNode</vh></v>
<v t="T510"><vh>OnCopyNode</vh></v>
<v t="T511"><vh>OnPasteNode</vh></v>
<v t="T512"><vh>OnDeleteNode</vh></v>
<v t="T513"><vh>OnInsertNode</vh></v>
<v t="T514"><vh>OnCloneNode</vh></v>
<v t="T515"><vh>OnSortNode</vh></v>
<v t="T516"><vh>OnExpandAll</vh></v>
<v t="T517"><vh>OnExpandAllChildren</vh></v>
<v t="T518"><vh>OnExpandChildren</vh></v>
<v t="T519"><vh>OnContractAll</vh></v>
<v t="T520"><vh>OnContractAllChildren</vh></v>
<v t="T521"><vh>OnContractChildren</vh></v>
<v t="T522"><vh>OnExpandNextLevel</vh></v>
<v t="T523"><vh>OnExpandToLevel1</vh></v>
<v t="T524"><vh>OnExpandToLevel2</vh></v>
<v t="T525"><vh>OnExpandToLevel3</vh></v>
<v t="T526"><vh>OnExpandToLevel4</vh></v>
<v t="T527"><vh>OnExpandToLevel5</vh></v>
<v t="T528"><vh>OnExpandToLevel6</vh></v>
<v t="T529"><vh>OnExpandToLevel7</vh></v>
<v t="T530"><vh>OnExpandToLevel8</vh></v>
<v t="T531"><vh>OnExpandToLevel9</vh></v>
<v t="T532"><vh>OnMoveDown</vh></v>
<v t="T533"><vh>OnMoveLeft</vh></v>
<v t="T534"><vh>OnMoveRight</vh></v>
<v t="T535"><vh>OnMoveUp</vh></v>
<v t="T536"><vh>OnPromote</vh></v>
<v t="T537"><vh>OnDemote</vh></v>
<v t="T538"><vh>OnGoPrevVisible</vh></v>
<v t="T539"><vh>OnGoNextVisible</vh></v>
<v t="T540"><vh>OnGoBack</vh></v>
<v t="T541"><vh>OnGoNext</vh></v>
<v t="T542"><vh>OnMark</vh></v>
<v t="T543"><vh>OnMarkSubheads</vh></v>
<v t="T544"><vh>OnMarkChangedItems</vh></v>
<v t="T545"><vh>OnMarkChangedRoots</vh></v>
<v t="T546"><vh>OnMarkAllAtFileNodesDirty</vh></v>
<v t="T547"><vh>OnMarkAtFileNodesDirty</vh></v>
<v t="T548"><vh>OnUnmarkAll</vh></v>
<v t="T549"><vh>OnGoToNextMarked</vh></v>
<v t="T550"><vh>OnGoToNextChanged</vh></v>
<v t="T551"><vh>OnEqualSizedPanes</vh></v>
<v t="T552"><vh>OnToggleActivePane</vh></v>
<v t="T553"><vh>OnChangeDirection</vh></v>
<v t="T554"><vh>OnCascade</vh></v>
<v t="T555"><vh>OnMinimizeAll</vh></v>
<v t="T556"><vh>OnOpenPythonWindow</vh></v>
<v t="T557"><vh>OnRecentWindows</vh></v>
<v t="T558"><vh>OnAbout</vh></v>
</v>
</v>
<v t="T559"><vh>LeoPrefs.cpp</vh>
<v t="T560"><vh>&lt;&lt; LeoPrefs declarations &gt;&gt;</vh></v>
<v t="T561"><vh>BEGIN_EVENT_TABLE</vh></v>
<v t="T562"><vh>ctor</vh></v>
<v t="T563"><vh>initialize</vh></v>
<v t="T564"><vh>targetToLanguage</vh></v>
<v t="T565"><vh>languageToTarget</vh></v>
<v t="T566"><vh>OnActivatePrefsFrame</vh></v>
<v t="T567"><vh>OnClosePrefsFrame</vh></v>
<v t="T568"><vh>OnPageWidthText</vh></v>
<v t="T569"><vh>OnDoneBatCheckBox</vh></v>
<v t="T570"><vh>OnUnBatCheckBox</vh></v>
<v t="T571"><vh>OnTangleDirectoryText</vh></v>
<v t="T572"><vh>OnHeaderCheckBox</vh></v>
<v t="T573"><vh>OnDocChunksCheckBox</vh></v>
<v t="T574"><vh>OnTargetLanguageRadioBox</vh></v>
<v t="T575"><vh>PrefsPanel</vh></v>
</v>
</v>
<v t="T576"><vh>wxPython docs: local @urls</vh>
<v t="T577"><vh>@url file:///C:/prog/wxDocs/wx26.htm#classref</vh></v>
<v t="T578"><vh>@url file:c:\prog\wxDocs\index.htm</vh></v>
<v t="T579" a="M"><vh>@url file:///C:\Python22\Lib\site-packages\wxPython\docs\wxPythonManual.html</vh></v>
<v t="T580"><vh>app, color, icon, sizer, xmlresource</vh>
<v t="T581"><vh>@url file:///C:/prog/wxDocs/wx30.htm#wxapp</vh></v>
<v t="T582"><vh>@url file:///C:/prog/wxDocs/wx63.htm#wxcolour</vh></v>
<v t="T583"><vh>@url file:///C:/prog/wxDocs/wx216.htm#wxicon</vh></v>
<v t="T584"><vh>@url file:///C:/prog/wxDocs/wx343.htm#wxsizer</vh></v>
<v t="T585"><vh>@url file:///C:/prog/wxDocs/wx418.htm#wxxmlresource</vh></v>
</v>
<v t="T586"><vh>dialog, frame, panel, splitter,window</vh>
<v t="T587"><vh>@url file:///C:/prog/wxDocs/wx109.htm#wxdialog</vh></v>
<v t="T588"><vh>@url file:///C:/prog/wxDocs/wx163.htm#wxframe</vh></v>
<v t="T589"><vh>@url file:///C:/prog/wxDocs/wx291.htm#wxpanel</vh></v>
<v t="T590"><vh>@url file:///C:/prog/wxDocs/wx357.htm#wxsplitterwindow</vh></v>
<v t="T591"><vh>@url file:///C:/prog/wxDocs/wx411.htm#wxwindow</vh></v>
</v>
<v t="T592"><vh>events</vh>
<v t="T593"><vh>@url file:///C:/prog/wxDocs/wx130.htm#wxevent</vh></v>
<v t="T594"><vh>@url file:///C:/prog/wxDocs/wx264.htm#wxmenuevent</vh></v>
<v t="T595"><vh>@url file:///C:/prog/wxDocs/wx356.htm#wxsplitterevent</vh></v>
<v t="T596"><vh>@url file:///C:/prog/wxDocs/wx400.htm#wxtreeevent</vh></v>
</v>
<v t="T597"><vh>menu</vh>
<v t="T598"><vh>@url file:///C:/prog/wxDocs/wx262.htm#wxmenu</vh></v>
<v t="T599"><vh>@url file:///C:/prog/wxDocs/wx263.htm#wxmenubar</vh></v>
<v t="T600"><vh>@url file:///C:/prog/wxDocs/wx265.htm#wxmenuitem</vh></v>
</v>
<v t="T601"><vh>tree</vh>
<v t="T602" a="M"><vh>@url file:///C:/prog/wxDocs/wx399.htm#wxtreectrl</vh></v>
<v t="T603"><vh>@url file:///C:/prog/wxDocs/wx401.htm#wxtreeitemdata</vh></v>
</v>
<v t="T604"><vh>widgets</vh>
<v t="T605"><vh>@url file:///C:/prog/wxDocs/wx46.htm#wxbutton</vh></v>
<v t="T606"><vh>@url file:///C:/prog/wxDocs/wx52.htm#wxcheckbox</vh></v>
<v t="T607"><vh>@url file:///C:/prog/wxDocs/wx212.htm#wxhtmlwindow</vh></v>
<v t="T608"><vh>@url file:///C:/prog/wxDocs/wx357.htm#wxsplitterwindow</vh></v>
<v t="T609" a="M"><vh>@url file:///C:/prog/wxDocs/wx381.htm#wxtextctrl</vh></v>
</v>
<v t="T610"><vh>wx Questions</vh></v>
</v>
<v t="T611"><vh>Leo wx prototype</vh>
<v t="T612"><vh>@file c:\prog\test\wxLeo.py</vh>
<v t="T613"><vh>app</vh>
<v t="T614"><vh>OnInit</vh></v>
</v>
<v t="T615"><vh>frame</vh>
<v t="T616"><vh>__init__</vh></v>
<v t="T617"><vh>createMenus (old code: explicit id's)</vh>
<v t="T618"><vh>&lt;&lt; Create the File menu &gt;&gt;</vh>
<v t="T619"><vh>&lt;&lt; Create the initial items of the file menu &gt;&gt;</vh></v>
<v t="T620"><vh>&lt;&lt; Create the Read/Write submenu &gt;&gt;</vh></v>
<v t="T621"><vh>&lt;&lt; Create the Tangle submenu &gt;&gt;</vh></v>
<v t="T622"><vh>&lt;&lt; Create the Untangle submenu &gt;&gt;</vh></v>
<v t="T623"><vh>&lt;&lt; Create the Import Files submenu &gt;&gt;</vh></v>
</v>
<v t="T624"><vh>&lt;&lt; Create the Edit menu &gt;&gt;</vh>
<v t="T625"><vh>&lt;&lt; Create the initial items of the Edit menu &gt;&gt;</vh></v>
<v t="T626"><vh>&lt;&lt; Create the Find submenu &gt;&gt;</vh></v>
<v t="T627"><vh>&lt;&lt; Create the final items of the Edit menu &gt;&gt;</vh></v>
<v t="T628"><vh>&lt;&lt; Create the Edit Body submenu &gt;&gt;</vh></v>
</v>
<v t="T629"><vh>&lt;&lt; Create the Outline menu &gt;&gt;</vh>
<v t="T630"><vh>&lt;&lt; Create the initial items of the Outline menu &gt;&gt;</vh></v>
<v t="T631"><vh>&lt;&lt; Create the Expand/Contract submenu &gt;&gt;</vh></v>
<v t="T632"><vh>&lt;&lt; Create the Move/Select submenu &gt;&gt;</vh></v>
<v t="T633"><vh>&lt;&lt; Create the Mark/Go To submenu &gt;&gt;</vh></v>
</v>
<v t="T634"><vh>&lt;&lt; Create the Window menu &gt;&gt;</vh></v>
<v t="T635"><vh>&lt;&lt; Create the Help menu &gt;&gt;</vh></v>
</v>
<v t="T636"><vh>createMenuBar</vh>
<v t="T637"><vh>&lt;&lt; create the edit menu &gt;&gt;</vh>
<v t="T638"><vh>&lt;&lt; create the first top-level edit entries &gt;&gt;</vh></v>
<v t="T639"><vh>&lt;&lt; create the edit body submenu &gt;&gt;</vh></v>
<v t="T640"><vh>&lt;&lt; create the edit headline submenu &gt;&gt;</vh></v>
<v t="T641"><vh>&lt;&lt; create the find submenu &gt;&gt;</vh></v>
<v t="T642"><vh>&lt;&lt; create the last top-level edit entries &gt;&gt;</vh></v>
</v>
<v t="T643"><vh>&lt;&lt; create the file menu &gt;&gt;</vh>
<v t="T644"><vh>&lt;&lt; create the top-level file entries &gt;&gt;</vh></v>
<v t="T645"><vh>&lt;&lt; create the recent files submenu &gt;&gt;</vh></v>
<v t="T646"><vh>&lt;&lt; create the read/write submenu &gt;&gt;</vh></v>
<v t="T647"><vh>&lt;&lt; create the tangle submenu &gt;&gt;</vh></v>
<v t="T648"><vh>&lt;&lt; create the untangle submenu &gt;&gt;</vh></v>
<v t="T649"><vh>&lt;&lt; create the import submenu &gt;&gt;</vh></v>
<v t="T650"><vh>&lt;&lt; create the export submenu &gt;&gt;</vh></v>
</v>
<v t="T651"><vh>&lt;&lt; create the outline menu &gt;&gt;</vh>
<v t="T652"><vh>&lt;&lt; create top-level outline menu &gt;&gt;</vh></v>
<v t="T653"><vh>&lt;&lt; create expand/contract submenu &gt;&gt;</vh></v>
<v t="T654"><vh>&lt;&lt; create move submenu &gt;&gt;</vh></v>
<v t="T655"><vh>&lt;&lt; create mark submenu &gt;&gt;</vh></v>
<v t="T656"><vh>&lt;&lt; create goto submenu &gt;&gt;</vh></v>
</v>
<v t="T657"><vh>&lt;&lt; create the window menu &gt;&gt;</vh></v>
<v t="T658"><vh>&lt;&lt; create the help menu &gt;&gt;</vh></v>
</v>
<v t="T659"><vh>createNewMenu</vh></v>
<v t="T660"><vh>createMenuEntries</vh></v>
<v t="T661"><vh>OnAbout</vh></v>
</v>
<v t="T662"><vh>const</vh></v>
</v>
</v>
</v>
<v t="T663" a="E"><vh>(4.0 project)</vh>
<v t="T664"><vh>(Problems with tnode list)</vh>
<v t="T665" a="C"><vh>findChild</vh></v>
<v t="T666" a="C"><vh>putOpenNodeSentinel</vh></v>
<v t="T667" a="C"><vh>putTnodeList (4.0)</vh></v>
</v>
<v t="T668" a="EM"><vh>To do</vh></v>
<v t="T669" a="E"><vh>@file gnx_code.py</vh>
<v t="T670"><vh>onCreateExtraMenus (to do: put in leoFrame class)</vh>
<v t="T671"><vh>&lt;&lt; extend the read/write submenu &gt;&gt;</vh></v>
<v t="T672"><vh>&lt;&lt; extend the import submenu &gt;&gt;</vh></v>
</v>
<v t="T673" a="V"><vh>class myFileCommands</vh>
<v t="T674"><vh>myFileCommands.__init__</vh></v>
<v t="T675"><vh>putVnode (3.x and 4.x)</vh>
<v t="T676"><vh>&lt;&lt; Put tnode index if this vnode has body text &gt;&gt;</vh></v>
<v t="T677"><vh>&lt;&lt; Put attribute bits &gt;&gt;</vh></v>
<v t="T678"><vh>&lt;&lt; write the head text &gt;&gt;</vh></v>
</v>
<v t="T667" a="C"><vh>putTnodeList (4.0)</vh></v>
<v t="T679"><vh>writeAtFileNodes</vh></v>
</v>
<v t="T680"><vh>class topLevelDerivedFile</vh>
<v t="T681"><vh>top_df.__init__</vh></v>
<v t="T682"><vh>Reading</vh>
<v t="T683"><vh> top_df.readAll</vh></v>
<v t="T684"><vh>top_df.error</vh></v>
<v t="T685"><vh>top_df.read</vh>
<v t="T686"><vh>&lt;&lt; set fileName from root and importFileName &gt;&gt;</vh></v>
<v t="T687"><vh>&lt;&lt; open file or return false &gt;&gt;</vh>
<v t="T688"><vh>&lt;&lt; warn on read-only file &gt;&gt;</vh></v>
</v>
<v t="T689"><vh>&lt;&lt; copy ivars to df &gt;&gt;</vh></v>
<v t="T690"><vh>&lt;&lt; warn about non-empty unvisited nodes &gt;&gt;</vh></v>
<v t="T691"><vh>&lt;&lt; copy all tempBodyStrings to tnodes &gt;&gt;</vh></v>
<v t="T692"><vh>&lt;&lt; delete all tempBodyStrings &gt;&gt;</vh></v>
</v>
<v t="T693"><vh>top_df.scanDefaultDirectory</vh>
<v t="T694"><vh>&lt;&lt; Set path from @file node &gt;&gt;</vh></v>
<v t="T695"><vh>&lt;&lt; handle @path &gt;&gt;</vh>
<v t="T696"><vh>&lt;&lt; compute relative path from s[k:] &gt;&gt;</vh></v>
<v t="T697"><vh>&lt;&lt; handle absolute path &gt;&gt;</vh></v>
</v>
<v t="T698"><vh>&lt;&lt; Set current directory &gt;&gt;</vh></v>
</v>
<v t="T699"><vh>top_df.scanHeader</vh>
<v t="T700"><vh>&lt;&lt; skip any non @+leo lines &gt;&gt;</vh></v>
<v t="T701"><vh>&lt;&lt; make sure we have @+leo &gt;&gt;</vh></v>
<v t="T702"><vh>&lt;&lt; read optional version param &gt;&gt;</vh></v>
<v t="T703"><vh>&lt;&lt; read optional encoding param &gt;&gt;</vh></v>
<v t="T704"><vh>&lt;&lt; set the closing comment delim &gt;&gt;</vh></v>
</v>
</v>
<v t="T705"><vh>Writing</vh>
<v t="T706"><vh>top_df.writeAll</vh>
<v t="T707"><vh>&lt;&lt; Clear all orphan bits &gt;&gt;</vh></v>
<v t="T708"><vh>&lt;&lt; handle v's tree &gt;&gt;</vh></v>
<v t="T709"><vh>&lt;&lt; say the command is finished &gt;&gt;</vh></v>
</v>
<v t="T710"><vh>top_df.write, rawWrite, silentWrite</vh></v>
<v t="T711"><vh>top_df.writeOld/NewDerivedFiles</vh></v>
<v t="T712"><vh>top_df.writeMissing</vh>
<v t="T713"><vh>&lt;&lt; set missing if the file does not exist &gt;&gt;</vh></v>
<v t="T714"><vh>&lt;&lt; create df.outputFile &gt;&gt;</vh></v>
<v t="T715"><vh>&lt;&lt; write the @file node &gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="T716"><vh>class oldDerivedFile</vh>
<v t="T717"><vh>  &lt;&lt; atFile constants &gt;&gt;</vh></v>
<v t="T718"><vh> old_df.__init__&amp; initIvars</vh>
<v t="T719"><vh>&lt;&lt; init atFile ivars &gt;&gt;</vh></v>
</v>
<v t="T720"><vh>Reading (3.x)</vh>
<v t="T721"><vh>old_df.readOpenFile</vh></v>
<v t="T722"><vh>completeFirstDirectives</vh></v>
<v t="T723"><vh>completeLastDirectives</vh></v>
<v t="T724"><vh>createNthChild</vh>
<v t="T725"><vh>&lt;&lt; check the headlines &gt;&gt;</vh></v>
</v>
<v t="T726"><vh>handleLinesFollowingSentinel</vh>
<v t="T727"><vh>&lt;&lt; remove the comment delims from s &gt;&gt;</vh></v>
</v>
<v t="T728"><vh>readLine</vh></v>
<v t="T729"><vh>readLinesToNextSentinel</vh></v>
<v t="T730"><vh>scanDoc</vh>
<v t="T731"><vh>&lt;&lt; Skip the opening sentinel &gt;&gt;</vh></v>
<v t="T732"><vh>&lt;&lt; Skip an opening block delim &gt;&gt;</vh></v>
<v t="T733"><vh>&lt;&lt; set kind, nextLine &gt;&gt;</vh></v>
<v t="T734"><vh>&lt;&lt; Skip the leading stuff &gt;&gt;</vh></v>
<v t="T735"><vh>&lt;&lt; Append s to out &gt;&gt;</vh></v>
<v t="T736"><vh>&lt;&lt; Remove a closing block delim from out &gt;&gt;</vh></v>
</v>
<v t="T737"><vh>scanText</vh>
<v t="T738"><vh>&lt;&lt; put the next line into s &gt;&gt;</vh></v>
<v t="T739"><vh>&lt;&lt; set kind, nextKind &gt;&gt;</vh></v>
<v t="T740"><vh>&lt;&lt; Set lineIndent, linep and leading_ws &gt;&gt;</vh></v>
<v t="T741"><vh>&lt;&lt; handle unexpected end of text &gt;&gt;</vh></v>
<v t="T742"><vh>&lt;&lt; handle the line in s &gt;&gt;</vh>
<v t="T743"><vh>&lt;&lt; append non-sentinel line &gt;&gt;</vh></v>
<v t="T744"><vh>&lt;&lt; handle common sentinels &gt;&gt;</vh>
<v t="T745"><vh>&lt;&lt; handle an ending sentinel &gt;&gt;</vh></v>
<v t="T746"><vh>&lt;&lt; scan old ref &gt;&gt; (3.0)</vh></v>
<v t="T747"><vh>&lt;&lt; scan @+at &gt;&gt;</vh></v>
<v t="T748"><vh>&lt;&lt; scan @+body &gt;&gt;</vh></v>
<v t="T749"><vh>&lt;&lt; scan @+doc &gt;&gt;</vh></v>
<v t="T750"><vh>&lt;&lt; scan @+node &gt;&gt;</vh>
<v t="T751"><vh>&lt;&lt; Set childIndex &gt;&gt;</vh></v>
<v t="T752"><vh>&lt;&lt; Set cloneIndex &gt;&gt;</vh></v>
<v t="T753"><vh>&lt;&lt; Set headline and ref &gt;&gt;</vh></v>
<v t="T754"><vh>&lt;&lt; Check the filename in the sentinel &gt;&gt;</vh></v>
<v t="T755"><vh>&lt;&lt; look for sentinels that may follow a reference &gt;&gt;</vh></v>
</v>
<v t="T756"><vh>&lt;&lt; scan @+others &gt;&gt;</vh></v>
</v>
<v t="T757"><vh>&lt;&lt; handle rare sentinels &gt;&gt;</vh>
<v t="T758"><vh>&lt;&lt; scan @+leo &gt;&gt;</vh></v>
<v t="T759"><vh>&lt;&lt; scan @@ &gt;&gt;</vh></v>
<v t="T760"><vh>&lt;&lt; scan @comment &gt;&gt;</vh></v>
<v t="T761"><vh>&lt;&lt; scan @delims &gt;&gt;</vh></v>
<v t="T762"><vh>&lt;&lt; scan @verbatim &gt;&gt;</vh></v>
</v>
<v t="T763"><vh>&lt;&lt; warn about unknown sentinel &gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="T764"><vh>Sentinels (3.x)</vh>
<v t="T765"><vh>nodeSentinelText</vh>
<v t="T766"><vh>&lt;&lt; remove comment delims from h if necessary &gt;&gt;</vh></v>
</v>
<v t="T767"><vh>putCloseNodeSentinel</vh></v>
<v t="T768"><vh>putCloseSentinels</vh></v>
<v t="T769"><vh>putOpenLeoSentinel</vh></v>
<v t="T770"><vh>putOpenNodeSentinel</vh></v>
<v t="T771"><vh>putOpenSentinels</vh></v>
<v t="T772"><vh>putSentinel (applies cweb hack)</vh></v>
<v t="T773"><vh>sentinelKind</vh></v>
<v t="T774"><vh>sentinelName</vh></v>
<v t="T775"><vh>skipSentinelStart</vh></v>
</v>
<v t="T776"><vh>Testing (3.x)</vh>
<v t="T777"><vh>scanAll</vh></v>
<v t="T778"><vh>scanFile</vh>
<v t="T779"><vh>&lt;&lt; open file &gt;&gt;</vh></v>
<v t="T780"><vh>&lt;&lt; Scan the file buffer  &gt;&gt;</vh></v>
</v>
</v>
<v t="T781"><vh>Utilites (3.x)</vh>
<v t="T782"><vh>directiveKind</vh></v>
<v t="T783"><vh>error</vh></v>
<v t="T784"><vh>readError</vh></v>
<v t="T785"><vh>scanAllDirectives</vh>
<v t="T786"><vh>&lt;&lt; Set ivars &gt;&gt;</vh></v>
<v t="T787"><vh>&lt;&lt; Set path from @file node &gt;&gt;</vh></v>
<v t="T788"><vh>&lt;&lt; Test for @comment and @language &gt;&gt;</vh></v>
<v t="T789"><vh>&lt;&lt; Test for @encoding &gt;&gt;</vh></v>
<v t="T790"><vh>&lt;&lt; Test for @header and @noheader &gt;&gt;</vh></v>
<v t="T791"><vh>&lt;&lt; Test for @lineending &gt;&gt;</vh></v>
<v t="T792"><vh>&lt;&lt; Test for @path &gt;&gt;</vh>
<v t="T793"><vh>&lt;&lt; compute relative path from s[k:] &gt;&gt;</vh></v>
<v t="T794"><vh>&lt;&lt; handle absolute path &gt;&gt;</vh></v>
</v>
<v t="T795"><vh>&lt;&lt; Test for @pagewidth &gt;&gt;</vh></v>
<v t="T796"><vh>&lt;&lt; Test for @tabwidth &gt;&gt;</vh></v>
<v t="T797"><vh>&lt;&lt; Set current directory &gt;&gt;</vh></v>
<v t="T798"><vh>&lt;&lt; Set comment Strings from delims &gt;&gt;</vh></v>
</v>
<v t="T799"><vh>skipIndent</vh></v>
<v t="T800"><vh>writeError</vh></v>
</v>
<v t="T801"><vh>Writing (3.x)</vh>
<v t="T802"><vh>Top level</vh>
<v t="T803"><vh>old_df.rawWrite</vh>
<v t="T804"><vh>&lt;&lt; write root's tree &gt;&gt;</vh>
<v t="T805" a="C"><vh>&lt;&lt; put all @first lines in root &gt;&gt;</vh></v>
<v t="T806"><vh>&lt;&lt; put optional @comment sentinel lines &gt;&gt;</vh></v>
<v t="T807"><vh>&lt;&lt; Write v's node &gt;&gt;</vh></v>
<v t="T808" a="C"><vh>&lt;&lt; put all @last lines in root &gt;&gt;</vh></v>
</v>
</v>
<v t="T809"><vh>old_df.silentWrite</vh>
<v t="T810"><vh>&lt;&lt; Write v's headline if it starts with @@ &gt;&gt;</vh></v>
<v t="T811"><vh>&lt;&lt; Write v's body &gt;&gt;</vh></v>
</v>
<v t="T812"><vh>old_df.write</vh>
<v t="T813"><vh>&lt;&lt; initialize &gt;&gt;</vh></v>
<v t="T814"><vh>&lt;&lt; open the file; return on error &gt;&gt;</vh></v>
<v t="T815"><vh>&lt;&lt; write then entire @file tree &gt;&gt; (3.x)</vh>
<v t="T805" a="C"><vh>&lt;&lt; put all @first lines in root &gt;&gt;</vh></v>
<v t="T816"><vh>&lt;&lt; write the derived file&gt;&gt;</vh></v>
<v t="T808" a="C"><vh>&lt;&lt; put all @last lines in root &gt;&gt;</vh></v>
</v>
<v t="T817"><vh>&lt;&lt; Warn about @ignored and orphans  &gt;&gt;</vh></v>
<v t="T818"><vh>&lt;&lt; finish writing &gt;&gt;</vh></v>
</v>
<v t="T819"><vh>Top level write helpers</vh>
<v t="T820"><vh>atFile.closeWriteFile</vh></v>
<v t="T821"><vh>atFile.handleWriteException</vh></v>
<v t="T822"><vh>atFile.openWriteFile</vh></v>
<v t="T823"><vh>atFile.putInitialComment</vh></v>
<v t="T824"><vh>atFile.replaceTargetFileIfDifferent</vh>
<v t="T825"><vh>&lt;&lt; delete the output file &gt;&gt;</vh></v>
<v t="T826"><vh>&lt;&lt; replace the target file with the output file &gt;&gt;</vh></v>
<v t="T827"><vh>&lt;&lt; rename the output file to be the target file &gt;&gt;</vh></v>
</v>
<v t="T828"><vh>atFile.outputStringWithLineEndings</vh></v>
</v>
</v>
<v t="T829"><vh>putBodyPart</vh>
<v t="T830"><vh>&lt;&lt; put code/doc parts and sentinels &gt;&gt;</vh>
<v t="T831"><vh>&lt;&lt; initialize lookingForFirst/Last &amp; initialLastDirective &gt;&gt;</vh></v>
<v t="T832"><vh>&lt;&lt; set lookingForFirst/Last &amp; initialLastDirective &gt;&gt;</vh></v>
<v t="T833"><vh>&lt;&lt; handle misc directives &gt;&gt;</vh></v>
<v t="T834"><vh>&lt;&lt; put out the last directives, if any &gt;&gt;</vh></v>
</v>
</v>
<v t="T835"><vh>putDoc</vh></v>
<v t="T836"><vh>putDocPart (3.x)</vh>
<v t="T837"><vh>&lt;&lt; copy words, splitting the line if needed &gt;&gt;</vh></v>
</v>
<v t="T838"><vh>putCodePart &amp; allies</vh>
<v t="T839"><vh>&lt;&lt; handle the start of a line &gt;&gt;</vh>
<v t="T840"><vh>&lt;&lt; handle @others &gt;&gt;</vh></v>
<v t="T841"><vh>&lt;&lt; handle @raw &gt;&gt;</vh></v>
<v t="T842"><vh>&lt;&lt; handle @end_raw &gt;&gt;</vh></v>
<v t="T843"><vh>&lt;&lt; put @verbatim sentinel if necessary &gt;&gt;</vh></v>
</v>
<v t="T844"><vh>&lt;&lt; put the line &gt;&gt;</vh>
<v t="T845"><vh>&lt;&lt; put possible section reference &gt;&gt;</vh></v>
</v>
<v t="T846"><vh>inAtOthers</vh></v>
<v t="T847"><vh>isSectionName</vh></v>
<v t="T848"><vh>putAtOthers</vh></v>
<v t="T849"><vh>putAtOthersChild</vh></v>
<v t="T850"><vh>putRef</vh>
<v t="T851"><vh>&lt;&lt; Generate the expansion of the reference &gt;&gt;</vh>
<v t="T852"><vh>&lt;&lt; Add @verbatimAfterRef sentinel if required &gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="T853"><vh>Writing Utils</vh>
<v t="T854"><vh>putBuffered</vh></v>
<v t="T855"><vh>os, onl, etc. (leoAtFile)</vh></v>
<v t="T856"><vh>putDirective  (handles @delims)</vh>
<v t="T857"><vh>&lt;&lt; handle @delims &gt;&gt;</vh></v>
</v>
<v t="T858"><vh>putEmptyDirective (Dave Hein)</vh></v>
<v t="T859"><vh>putIndent</vh></v>
</v>
</v>
</v>
<v t="T860"><vh>class newDerivedFile</vh>
<v t="T861"><vh>newDerivedFile.__init__</vh></v>
<v t="T862"><vh>Reading (4.x)</vh>
<v t="T863"><vh>new_df.readOpenFile</vh></v>
<v t="T665" a="C"><vh>findChild</vh></v>
<v t="T864"><vh>scanText &amp; allies</vh>
<v t="T865"><vh>&lt;&lt; init ivars for scanText &gt;&gt;</vh></v>
<v t="T866"><vh>&lt;&lt; report unexpected end of text &gt;&gt;</vh></v>
<v t="T867"><vh>readNormalLine</vh>
<v t="T868"><vh>&lt;&lt; Skip the leading stuff &gt;&gt;</vh></v>
<v t="T869"><vh>&lt;&lt; Append s to docOut &gt;&gt;</vh></v>
</v>
<v t="T870"><vh>start sentinels</vh>
<v t="T871"><vh>readStartAt, readStartDoc &amp; readStartDocLine</vh></v>
<v t="T872"><vh>readStartLeo</vh></v>
<v t="T873"><vh>readStartNode</vh>
<v t="T874"><vh>&lt;&lt; Set headline, undoing the CWEB hack &gt;&gt;</vh></v>
<v t="T875"><vh>&lt;&lt; Check the filename in the sentinel &gt;&gt;</vh></v>
</v>
<v t="T876"><vh>readStartOthers</vh></v>
</v>
<v t="T877"><vh>end sentinels</vh>
<v t="T878"><vh>readEndAt &amp; readEndDoc</vh></v>
<v t="T879"><vh>readEndLeo</vh></v>
<v t="T880"><vh>readEndNode</vh></v>
<v t="T881"><vh>readEndOthers</vh></v>
<v t="T882" a="C"><vh>readLastDocLine</vh></v>
</v>
<v t="T883"><vh>Unpaired sentinels</vh>
<v t="T884"><vh>ignoreOldSentinel</vh></v>
<v t="T885"><vh>readAfterRef</vh></v>
<v t="T886"><vh>readComment</vh></v>
<v t="T887"><vh>readDelims</vh></v>
<v t="T888"><vh>readDirective</vh></v>
<v t="T889"><vh>readNl</vh></v>
<v t="T890"><vh>readNonl</vh></v>
<v t="T891"><vh>readRef</vh></v>
<v t="T892"><vh>readVerbatim</vh></v>
</v>
<v t="T893"><vh>badEndSentinel, push/popSentinelStack</vh></v>
</v>
</v>
<v t="T894"><vh>Sentinels (4.x)</vh>
<v t="T895"><vh>nodeSentinelText</vh>
<v t="T896"><vh>&lt;&lt; remove comment delims from h if necessary &gt;&gt;</vh></v>
</v>
<v t="T897"><vh>putLeadInSentinel</vh></v>
<v t="T898"><vh>putOpenLeoSentinel</vh></v>
<v t="T666" a="C"><vh>putOpenNodeSentinel</vh></v>
<v t="T899"><vh>putSentinel (applies cweb hack)</vh>
<v t="T900"><vh>&lt;&lt; apply the cweb hack to s &gt;&gt;</vh></v>
</v>
<v t="T901"><vh>skipSentinelStart</vh></v>
<v t="T902"><vh>sentinelKind</vh></v>
</v>
<v t="T903"><vh>Writing (4.x)</vh>
<v t="T904"><vh>Top level</vh>
<v t="T905"><vh>new_df.closeWriteFile</vh></v>
<v t="T906"><vh>new_df.write</vh>
<v t="T907"><vh>&lt;&lt; initialize &gt;&gt;</vh></v>
<v t="T908"><vh>&lt;&lt; open the file; return on error &gt;&gt;</vh></v>
<v t="T909"><vh>&lt;&lt; write then entire @file tree &gt;&gt; (4.x)</vh>
<v t="T910"><vh>&lt;&lt; put all @first lines in root &gt;&gt;</vh></v>
<v t="T911"><vh>&lt;&lt; put all @last lines in root &gt;&gt;</vh></v>
</v>
<v t="T912"><vh>&lt;&lt; Warn about @ignored and orphans  &gt;&gt;</vh></v>
<v t="T913"><vh>&lt;&lt; finish writing &gt;&gt;</vh></v>
</v>
<v t="T914"><vh>new_df.rawWrite (needs testing)</vh>
<v t="T915"><vh>&lt;&lt; write root's tree &gt;&gt;</vh>
<v t="T916"><vh>&lt;&lt; put all @first lines in root &gt;&gt;</vh></v>
<v t="T917"><vh>&lt;&lt; put optional @comment sentinel lines &gt;&gt;</vh></v>
<v t="T918"><vh>&lt;&lt; Write v's node &gt;&gt;</vh></v>
<v t="T919"><vh>&lt;&lt; put all @last lines in root &gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="T920"><vh>putBody</vh>
<v t="T921"><vh>&lt;&lt; handle line at s[i]  &gt;&gt;</vh></v>
</v>
<v t="T922"><vh>code lines...</vh>
<v t="T923"><vh>inAtOthers</vh></v>
<v t="T924"><vh>putAtOthersChild</vh></v>
<v t="T925"><vh>putAtOthersLine</vh></v>
<v t="T926"><vh>putCodeLine</vh></v>
<v t="T927"><vh>putRefLine</vh></v>
</v>
<v t="T928"><vh>doc lines...</vh>
<v t="T929"><vh>putBlankDocLine</vh></v>
<v t="T930" a="CM"><vh>putStartDocLine</vh></v>
<v t="T931"><vh>putDocLine</vh>
<v t="T932"><vh>&lt;&lt; append words to pending line, splitting the line if needed &gt;&gt;</vh></v>
</v>
<v t="T933"><vh>putEndDocLine</vh></v>
<v t="T934"><vh>putPending</vh></v>
</v>
<v t="T935"><vh>Writing Utils...</vh>
<v t="T936"><vh>hasSectionName</vh></v>
<v t="T937"><vh>os, onl, etc.</vh></v>
<v t="T938"><vh>directiveKind</vh></v>
</v>
</v>
</v>
</v>
<v t="T939" a="E"><vh>(Problems with doc parts</vh>
<v t="T930" a="C"><vh>putStartDocLine</vh></v>
<v t="T882" a="C"><vh>readLastDocLine</vh></v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="T1">@nocolor</t>
<t tx="T2"></t>
<t tx="T3"></t>
<t tx="T4">tnodeList must be a list of tnodes, _not_ a list of tnode indices.

Indices may be reassigned, tnodes won't.

The _only_ place that an index is proper is in the file format itelf.</t>
<t tx="T5">The script is called "Script to compare 3.x and 4.x derived files" in test.leo.
</t>
<t tx="T6">The bug was in directiveKind.  There are two ways for the code to recognize @others.  After inserting the second way, I mistakenly commented out the first way (by commenting out @others in the table).</t>
<t tx="T7"></t>
<t tx="T8"></t>
<t tx="T9"></t>
<t tx="T10"></t>
<t tx="T11">The new version of putLeadInSentinel works as follows:

1. It calls at.putIndent(at.indent) followed by the leading whitespace in the outline line.

The effect of this is

a) to align the @ws sentinel with the following sentinel and
b) to preserve the "spelling" of the leading whitespace on the line.

2. N.B. The calls to putLeadInSentinel happen _before_ at.indent is changed as the result of the leading whitespace. 

Again, this is so that putLeadInSentinel can preserve the spelling of whitespace.

3. The contribution of the @ws sentinel is the _difference_ between the value of at.indent when the @ws sentinel is being read and the actual whitespace on the line.  Again, we do this to make the derived file look better.</t>
<t tx="T12">This makes the @nl look better, and has no other effect.</t>
<t tx="T13">- Special case code for blank lines.
- Created putBlankDocLine.</t>
<t tx="T14"></t>
<t tx="T15"></t>
<t tx="T16"></t>
<t tx="T17"></t>
<t tx="T18">This method now uses the tnode list to find the indicated tnode.  It also checks the headline.</t>
<t tx="T19"></t>
<t tx="T20">The code that reads the new tnodeList attribute of vnodes is contained in the "main line" code, i.e., in LeoPy.leo.  This means that Leo will always be able to read (and ignore) the tnodeList attribute.

The code that writes the attribute is part of the use_gnx plugin.

The tnodeList returns a tnode, not a vnode, so it makes sense to keep track of at.t not at.v.
</t>
<t tx="T21">- The new code now hanles the basic cases properly.

- Added @nl sentinel to indicate whether a section ref should be followed by a newline.

- The read code now sets v.t.tempBodyString instead of call v.setBodyStringOrPane.  This is a major advance in error recovery:  nothing at all changes if errors happen.

What I did earlier:
	- Removed @+body and @-body
	- Don't write organizer nodes in @others</t>
<t tx="T22"></t>
<t tx="T23">@nocolor

This file contains code for all plugins distributed with Leo.</t>
<t tx="T24">@nocolor

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
<t tx="T25">@nocolor

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
<t tx="T26">At startup time Leo looks all files of the form mod_*.py in the plugins
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
<t tx="T27">Naively using hooks can expose you and your .leo files to malicious attacks.

** Hooks should never blindly execute Python scripts in .leo files.

It is safe to import and execute code from Leo itself, provided that you got Leo from Leo's SourceForge site.</t>
<t tx="T28">@color
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
<t tx="T29">@ It is usually best not to catch exceptions in plugins.  doHook catches all exceptions and disables further calls to plugins.
@c

@ignore
</t>
<t tx="T30">@nocolor</t>
<t tx="T31">- (done) Make sure the selected node is visible.
- (done) Force the focus to the body pane after undo/redo so the selection is visible.

- Bind Fkeys to buttons.
- Is there a problem with "__init__" ?
- words like "and" aren't in the dictionary?????
</t>
<t tx="T32"></t>
<t tx="T33"></t>
<t tx="T34">"""Import cisco configuration files"""

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
<t tx="T35">@ This plugin adds a menu item under the File-&gt;Import menu to import
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
<t tx="T36">def create_import_cisco_menu(tag, keywords):
	if	(tag=="open2" or
		(tag=="start2" and not keywords.has_key('c')) or
		(tag=="command2" and keywords.get("label")=="new")):

		c = top()
		importMenu = c.frame.getMenu('import')
		newEntries = (
			("-", None, None),
			("Import C&amp;isco Configuration", "Shift+Ctrl+I", importCiscoConfig))
		
		c.frame.createMenuEntries(importMenu, newEntries)</t>
<t tx="T37">def importCiscoConfig(event=None):
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
<t tx="T38">name = tkFileDialog.askopenfilename(
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
<t tx="T39">if not blocks.has_key(customLine):
	blocks[customLine] = []
	out.append(angleBrackets(customLine))
	# create first-level child
	child = v.insertAsNthChild(0)
	child.setHeadStringOrHeadline(angleBrackets(customLine))
	children.append(child)

blocks[customLine].append(linelist[i])</t>
<t tx="T40">space = linelist[i].find(' ')
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
<t tx="T41"># first print the level-0 text
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
<t tx="T42">@ignore
@language plain
@comment !
@ This node has an example of a flat configuration file (i.e. just the output of a 
'show running' command on a cisco router), and of the same configuration file 
imported by the plugin.
</t>
<t tx="T43">rpr1#sh runn    
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
<t tx="T44">rpr1#sh runn    
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
<t tx="T45">access-list 173 deny   ip 224.0.0.0 31.255.255.255 any
access-list 173 permit ip any any</t>
<t tx="T46">boot system flash rsp-k3pv-mz.120-21.S4.bin
boot system flash rsp-pv-mz.120-21.S1.bin
boot bootldr bootflash:rsp-boot-mz.120-11.S3</t>
<t tx="T47"></t>
<t tx="T48">controller E1 5/0/0
 framing NO-CRC4 
 clock source internal
 channel-group 1 timeslots 1
 channel-group 2 timeslots 2</t>
<t tx="T49">controller E1 5/0/1
 framing NO-CRC4 
 channel-group 0 timeslots 1</t>
<t tx="T50">controller SONET 1/0/0
 framing sdh</t>
<t tx="T51"></t>
<t tx="T52">interface Async1
 no ip address
 no ip directed-broadcast
 async mode interactive
 no peer default ip address</t>
<t tx="T53">interface Dialer0
 no ip address
 no ip directed-broadcast
 pulse-time 0
 no cdp enable</t>
<t tx="T54">interface FastEthernet0/0/0
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
<t tx="T55">interface FastEthernet0/0/1
 description **trunk link**
 no ip address
 no ip directed-broadcast
 no ip route-cache distributed
 no ip mroute-cache
 full-duplex</t>
<t tx="T56">interface FastEthernet0/0/1.1
 encapsulation dot1Q 25
 ip address 192.168.25.1 255.255.255.252
 no ip directed-broadcast</t>
<t tx="T57">interface FastEthernet0/0/1.2
 no ip directed-broadcast</t>
<t tx="T58">interface FastEthernet0/0/1.3
 encapsulation dot1Q 3
 ip address 192.168.4.1 255.255.255.252
 ip access-group 173 in
 no ip directed-broadcast
 ip pim sparse-mode</t>
<t tx="T59">interface FastEthernet0/0/1.5
 encapsulation dot1Q 5
 ip address 192.168.5.1 255.255.255.252
 no ip directed-broadcast</t>
<t tx="T60">interface FastEthernet0/0/1.50
 description to KPN-test
 encapsulation dot1Q 50
 ip address 192.168.40.1 255.255.255.252
 no ip directed-broadcast</t>
<t tx="T61">interface Loopback0
 ip address 192.168.20.1 255.255.255.255
 no ip directed-broadcast</t>
<t tx="T62">interface POS4/1/0
 no ip address
 no ip directed-broadcast
 no ip route-cache distributed
 no ip mroute-cache
 loopback internal</t>
<t tx="T63">interface Serial5/0/0:1
 ip address 10.31.9.1 255.255.255.252
 no ip directed-broadcast
 no ip route-cache distributed</t>
<t tx="T64">interface Serial5/0/0:2
 ip address 10.10.10.1 255.255.255.252
 no ip directed-broadcast
 no ip route-cache distributed</t>
<t tx="T65">interface Serial5/0/1:0
 ip address 10.31.9.5 255.255.255.252
 no ip directed-broadcast
 no ip route-cache distributed</t>
<t tx="T66">interface Serial5/1/0
 no ip address
 no ip directed-broadcast
 no ip route-cache distributed
 no ip mroute-cache
 shutdown
 framing g751
 dsu bandwidth 34010</t>
<t tx="T67">interface Serial5/1/1
 ip address 192.168.6.1 255.255.255.252
 no ip directed-broadcast
 encapsulation frame-relay IETF
 no ip route-cache distributed
 no ip mroute-cache
 loopback local
 framing g751
 dsu bandwidth 34010</t>
<t tx="T68">ip community-list 1 permit 65001:1
ip community-list 100 permit 65001:3</t>
<t tx="T69">ip route 0.0.0.0 0.0.0.0 192.168.3.2 tag 3</t>
<t tx="T70"></t>
<t tx="T71">line aux 0
 transport input all
 stopbits 1
 flowcontrol hardware</t>
<t tx="T72">line vty 0 4
 exec-timeout 0 0
 password 7 somepassword
 logging synchronous
 login
 length 0</t>
<t tx="T73">logging buffered 100000 debugging
logging facility local6
logging 10.10.10.1</t>
<t tx="T74">ntp clock-period 17179348
ntp update-calendar
ntp peer 192.168.3.2 prefer</t>
<t tx="T75"></t>
<t tx="T76">route-map only permit 2
 match community 65001:2
 set origin igp</t>
<t tx="T77">route-map only1 permit 10
 match community 1 65001:1
 set origin igp</t>
<t tx="T78">route-map only3 permit 10
 match community 100</t>
<t tx="T79">route-map tag_com permit 10
 match tag 1
 set community 65001:1</t>
<t tx="T80">route-map tag_com permit 20
 match tag 3
 set community 65001:3</t>
<t tx="T81"></t>
<t tx="T82">router bgp 65001
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
<t tx="T83">router ospf 1
 log-adjacency-changes
 passive-interface FastEthernet0/0/0
 network 192.168.3.1 0.0.0.0 area 0
 network 192.168.4.0 0.0.0.3 area 0</t>
<t tx="T84">no service pad
service timestamps debug datetime localtime show-timezone
service timestamps log datetime localtime show-timezone
service password-encryption
no service single-slot-reload-enable</t>
<t tx="T85">"""Modify the way exported outlines are displayed"""

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
<t tx="T86"># Returns the headline string in MORE format.

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
<t tx="T87"></t>
<t tx="T88">"""Dump globals at startup"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("start2", onStart)

	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T89">def onStart (tag,keywords):

	print "\nglobals..."
	for s in globals():
		if s not in __builtins__:
			print s
	
	print "\nlocals..."
	for s in locals():
		if s not in __builtins__:
			print s
</t>
<t tx="T90">"""Enable debugging for garbage collector"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("start2", onStart)
	
	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T91">def onStart (tag,keywords):

	try:
		import gc
		gc.set_debug(gc.DEBUG_LEAK)
	except: pass</t>
<t tx="T92">"""Trace changes to objects at idle time"""

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
<t tx="T93">"""Trace keystrokes in the outline and body panes"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler(("bodykey1","bodykey2","headkey1","headkey2"), onKey)
	
	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T94">def onKey (tag,keywords):

	ch = keywords.get("ch")
	if ch and len(ch) &gt; 0:
		es("key",`ch`)</t>
<t tx="T95">"""Trace most comment events, but not key, drag or idle events"""

from leoPlugins import *
from leoGlobals import *

tagCount = 0

@others

if 0: # Register the handlers...
	registerHandler("all", trace_tags)

	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)
</t>
<t tx="T96">def trace_tags (tag,keywords):
	
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
<t tx="T97"></t>
<t tx="T98">"""Support new @direcives"""

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
<t tx="T99">def addPluginDirectives (tag,keywords):
	
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
<t tx="T100">def scanPluginDirectives (tag, keywords):
	
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
<t tx="T101"></t>
<t tx="T102">"""Handle coloring for markup in doc parts and Python triple-double-quoted strings"""

from leoPlugins import *
from leoGlobals import *
import string  # zfill does not exist in Python 2.2.1

@others

if 1: # Register the handlers...

	registerHandler("color-optional-markup", colorWikiMarkup)
	registerHandler("init-color-markup", initAnyMarkup)

	__version__ = "1.1"
	plugin_signon(__name__)</t>
<t tx="T103">def initAnyMarkup (tag,keywords):
	
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
<t tx="T104">colorCount = 0

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
<t tx="T105">def doWikiText (colorer,v,s,i,end,colortag):

	firsti = i ; inserted = 0

	while i &lt; end:
		&lt;&lt; set first to a tuple describing the first tag to be handled &gt;&gt;
		if first:
			tag,n1,n2,delim1,delim2 = first
			i = n2 + len(delim2)
			&lt;&lt; handle the tag using n1,n2,delim1,delim2 &gt;&gt;
		else: i = end
		
	colorer.tag(colortag,firsti,end+inserted)</t>
<t tx="T106">first = None

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
<t tx="T107">if tag =="picture":
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
<t tx="T108"># Parse the color value.
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
<t tx="T109">def insertWikiPicture (colorer,filename,i):
	
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
<t tx="T110">"""Handle images in body text"""

from leoPlugins import *
from leoGlobals import *

@others

if 1: # Register the handlers...
	registerHandler("select2", onSelect)
	registerHandler("unselect1", onUnselect)
	
	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)
</t>
<t tx="T111">def onSelect (tag,keywords):

	import Tkinter,os

	new_v = keywords.get("new_v")
	h = new_v.headString()
	if h[:7] == "@image ":
		filename = h[7:]
		&lt;&lt; Select Image &gt;&gt;</t>
<t tx="T112"># Display the image file in the text pane, if you can find the file
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
<t tx="T113">def onUnselect (tag,keywords):

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
<t tx="T114"># Erase image if it was previously displayed
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
<t tx="T115">"""Adds navigation buttons to icon bar"""

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
<t tx="T116">class commanderInfoClass:
	@others</t>
<t tx="T117">def __init__ (self,c,globalInfo):
	
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
<t tx="T118">def addWidgets (self):
	
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
<t tx="T119"># These are functions, not methods, so we must bind self at definition time.

def onMarksButton(self=self):

	self.marksButtonCallback()
	
def onRecentButton(self=self):

	self.recentButtonCallback()</t>
<t tx="T120">def createImage (self,path):
	
	path = os.path.join(app().loadDir,path)
	path = os.path.normpath(path)
	
	try:
		image = Tkinter.PhotoImage(master=app().root,file=path)
	except:
		es("can not load icon: " + shortFileName(path))
		image = None
	return image

</t>
<t tx="T121">def updateNavButtons (self):	

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
<t tx="T122"></t>
<t tx="T123">def marksButtonCallback(self,event=None):
	
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
<t tx="T124">def recentButtonCallback(self,event=None):
	
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
<t tx="T125">class globalInfoClass:
	@others</t>
<t tx="T126">def __init__ (self):
	
	self.commanderInfo = {} # keys are commanders, values are navCommanderInfo objects
</t>
<t tx="T127">def addNavWidgets(self,tag,keywords):
	
	c = keywords.get("c")
	
	# Create the commanderInfo object.
	d = commanderInfoClass(c,self)
	self.commanderInfo[c] = d
	
	# Add the widgets.
	d.addWidgets()
	
</t>
<t tx="T128">def destroyAllFrames(self,tag,keywords):
	
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
<t tx="T129">def updateRecentSections (self,tag,keywords):
	
	c = keywords.get("c")
	info = self.commanderInfo.get(c)

	if info:
		info.updateNavButtons()
		d = info.recentSectionsDialog
		if d:
			d.fillbox()
</t>
<t tx="T130">def updateMarksAfterCommand (self,tag,keywords):
	
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
<t tx="T131">def updateNavButtons (self,tag,keywords):

	"""Update the colors of c's nav buttons"""
	
	c = keywords.get("c")
	info = self.commanderInfo.get(c)
	
	if info:
		info.updateNavButtons()
</t>
<t tx="T132">class marksDialog (listBoxDialog):
	
	"""A class to create the marks dialog"""

	@others</t>
<t tx="T133">def __init__ (self,c,title,label):
	
	"""Create a Marks listbox dialog."""

	listBoxDialog.__init__(self,c,title,label)
</t>
<t tx="T134">def createFrame(self):
	
	"""Create the frame for a Marks listbox dialog."""

	listBoxDialog.createFrame(self)
	self.addButtons()</t>
<t tx="T135">def addButtons (self):
	
	"""Add buttons to a Marks listbox dialog."""
	
	f = Tk.Frame(self.outerFrame)
	f.pack()
	self.addStdButtons(f)</t>
<t tx="T136">def fillbox(self,event=None):

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
<t tx="T137">class recentSectionsDialog (listBoxDialog):
	
	"""A class to create the recent sections dialog"""

	@others</t>
<t tx="T138">def __init__ (self,c,buttons,title,label):
	
	"""Create a Recent Sections listbox dialog."""
	
	self.lt_nav_iconFrame_button, self.rt_nav_iconFrame_button = buttons

	listBoxDialog.__init__(self,c,title,label)

</t>
<t tx="T139">def addButtons (self):
	
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
<t tx="T140">def clearAll (self,event=None):

	"""Handle clicks in the "Delete" button of the Recent Sections listbox dialog."""

	self.c.visitedList = []
	self.vnodeList = []
	self.fillbox()
</t>
<t tx="T141">def createFrame(self):
	
	"""Create the frame of a Recent Sections listbox dialog."""
	
	listBoxDialog.createFrame(self)	
	self.addButtons()
</t>
<t tx="T142">def deleteEntry (self,event=None):

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
<t tx="T143">def destroy (self,event=None):
	
	"""Hide a Recent Sections listbox dialog and mark it inactive.
	
	This is an escape from possible performace penalties"""
		
	# This is enough to disable fillbox.
	self.top.withdraw()
</t>
<t tx="T144">def fillbox(self,event=None):

	"""Update a Recent Sections listbox dialog and update vnodeList &amp; tnodeList ivars"""

	# Only fill the box if the dialog is visible.
	# This is an important protection against bad performance.

	if self.top.state() == "normal":
		&lt;&lt; reconstruct the contents of self.box &gt;&gt;
		self.synchButtons()</t>
<t tx="T145">c = self.c

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
<t tx="T146">def synchButtons (self):
	
	"""Synchronize the arrow boxes of a Recent Sections listbox dialog."""

	image = self.lt_nav_iconFrame_button.cget("image")
	self.lt_nav_button.configure(image=image)
	
	image = self.rt_nav_iconFrame_button.cget("image")
	self.rt_nav_button.configure(image=image)</t>
<t tx="T147"></t>
<t tx="T148">"""Create menu for Open With command and handle the resulting commands"""

from leoPlugins import *
from leoGlobals import *

@others

if 1: # Register the handlers...

	app().hasOpenWithMenu = true
	registerHandler("idle", on_idle)
	registerHandler(("start2","open2","command2"), create_open_with_menu)

	__version__ = "1.4" # Set version for the plugin handler.
	plugin_signon(__name__)</t>
<t tx="T149"># frame.OnOpenWith creates the dict with the following entries:
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
<t tx="T150">&lt;&lt; set s to the file text &gt;&gt;

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
<t tx="T151">try:
	# Update v from the changed temp file.
	f=open(path)
	s=f.read()
	f.close()
except:
	es("can not open " + shortFileName(path))
	break
</t>
<t tx="T152">def create_open_with_menu (tag,keywords):

	if  (tag in ("start2","open2") or
		(tag=="command2" and keywords.get("label")=="new")):

		&lt;&lt; create the Open With menu &gt;&gt;
		# Enable the idle-time hook so we can check temp files created by Open With.
		from leoGlobals import enableIdleTimeHook
		enableIdleTimeHook(idleTimeDelay=500)
</t>
<t tx="T153">@ Entries in the following table are the tuple (commandName,shortcut,data).

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
<t tx="T154">"""vim handler"""

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
<t tx="T155">def open_in_vim (tag,keywords):
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
<t tx="T156">"""emacs handler"""

from leoPlugins import *
from leoGlobals import *

def open_in_emacs (tag,keywords):
	if top():
		top().frame.OnOpenWith(("os.spawnl", "/usr/bin/gnuclient", None),) # 6/27/03: add comma.

if 0: # Register the handlers...
	registerHandler(("iconclick2","select2"), open_in_emacs)
	
	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)</t>
<t tx="T157"></t>
<t tx="T158">"""Open any empty file as a minimal .leo file"""

from leoPlugins import *
from leoGlobals import *

&lt;&lt; define minimal .leo file &gt;&gt;
@others

if 0: # Register the handlers...
	registerHandler("open1", onOpen)
	
	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)</t>
<t tx="T159">empty_leo_file = """&lt;?xml version="1.0" encoding="iso-8859-1"?&gt;
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
<t tx="T160">def onOpen (tag,keywords):

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
<t tx="T161">@language python

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
<t tx="T162">@ Written by Ed Taekema.  Modified by E.K.Ream

Please submit bugs / feature requests to etaekema@earthlink.net"""

This is a simple plugin for leo 3.12 that allows the user to open either an xterm on linux or a cmd windows/explorer window on win32 in the directory of the current @file.  This allows quick navigation to facilitate testing and navigating large systems with complex direcgtories.

Current limitations ...

1. Not tested on Mac OS X ...
2. On win32, the cmd window will not open in the right directory if the @file location is on a different drive than the .leo file that is being edited.
3. On linux, xterm must be in your path.
</t>
<t tx="T163">def load_menu(tag,keywords):
	
	if sys.platform=="win32":
		table = (
			("&amp;Open Console Window",None,launchCmd),
			("Open &amp;Explorer",None,launchExplorer)) 
	else:
		table = ( ("Open &amp;xterm",None,launchxTerm), ) 
	
	top().frame.createNewMenu("E&amp;xtensions","top")
	top().frame.createMenuItemsFromTable("Extensions",table)
</t>
<t tx="T164">def _getpath(c,v):
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
<t tx="T165">def _getCurrentNodePath():
	c = leo.top()
	v = c.currentVnode()
	f = v.atFileNodeName()
	d = _getpath(c,v)
	return d
</t>
<t tx="T166">def launchCmd(not_used):
	
	global pathToCmd

	d = _getCurrentNodePath()
	myCmd = 'cd ' + d
	os.spawnl(os.P_NOWAIT, pathToCmd, '/k ', myCmd)</t>
<t tx="T167">def launchExplorer(not_used):
	
	global pathToExplorer

	d = _getCurrentNodePath()
	os.spawnl(os.P_NOWAIT,pathToExplorer, ' ', d)

</t>
<t tx="T168">def launchxTerm(not_used):

	d = _getCurrentNodePath()
	curdir = os.getcwd()
	os.chdir(d)
	os.spawnlp(os.P_NOWAIT, 'xterm', '-title Leo')
	os.chdir(curdir)</t>
<t tx="T169">In Python 2.3 the source files should declare the encoding.

See http://www.python.org/peps/pep-0263.html for full details.</t>
<t tx="T170">@first # -*- coding: utf-8 -*-

"""Translate a few menu items into French"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler(("start1","menu1"), onMenu)
	
	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T171">@ The translation table used by setRealMenuNamesFromTable has entries of the form:

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
<t tx="T172">@first # -*- coding: utf-8 -*-
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
<t tx="T173">def onMenu (tag,keywords):
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
<t tx="T174"></t>
<t tx="T175">"""Rebind up/down arrow keys"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("open2", onOpen)
	
	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)
</t>
<t tx="T176"># Warning: the bindings created this way conflict with shift-arrow keys.

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
<t tx="T177"></t>
<t tx="T178"></t>
<t tx="T179">"""Create a Plugins menu"""

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
<t tx="T180">class PlugIn:

	"""A class to hold information about one plugin"""

	@others
	
</t>
<t tx="T181">def __init__(self, filename):

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
<t tx="T182"># Look for a configuration file
self.configfilename = "%s.ini" % os.path.splitext(filename)[0]
self.hasconfig = os.path.isfile(self.configfilename)
</t>
<t tx="T183">@ Look for an apply function ("applyConfiguration") in the module.

This is used to apply changes in configuration from the properties window
@c

self.hasapply = hasattr(self.mod, "applyConfiguration")
</t>
<t tx="T184">@ Additional commands can be added to the plugin menu by having functions in the module called "cmd_whatever". These are added to the main menu and will be called when clicked
@c

self.othercmds = {}

for item in self.mod.__dict__.keys():
	if item.startswith("cmd_"):
		self.othercmds[item[4:]] = self.mod.__dict__[item]
</t>
<t tx="T185">def about(self, arg):
	
	"""Put up an "about" dialog for this plugin"""

	PluginAbout(self.name, self.version, self.doc)</t>
<t tx="T186">def properties(self, arg):
	
	"""Create a modal properties dialog for this plugin"""

	PropertiesWindow(self.configfilename, self)
</t>
<t tx="T187">class PropertiesWindow:

	"""A class to create and run a Properties dialog for a plugin"""

	@others</t>
<t tx="T188">def __init__(self, filename, plugin):

	"""Initialize the property window"""
	
	&lt;&lt; initialize all ivars &gt;&gt;
	&lt;&lt; create the frame from the configuration data &gt;&gt;</t>
<t tx="T189"># config stuff.
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
<t tx="T190">root = app().root

&lt;&lt; Create the top level and the main frame &gt;&gt;
&lt;&lt; Create widgets for each section and option &gt;&gt;
&lt;&lt; Create Ok, Cancel and Apply buttons &gt;&gt;

center_dialog(top) # Do this after packing.
top.grab_set() # Make the dialog a modal dialog.
top.focus_force() # Get all keystrokes.
root.wait_window(top)</t>
<t tx="T191">self.top = top = Tk.Toplevel(root)
attachLeoIcon(self.top)
top.title("Properties of "+ plugin.name)
top.resizable(0,0) # neither height or width is resizable.
	
self.frame = frame = Tk.Frame(top)
frame.pack(side="top")</t>
<t tx="T192"># Create all the entry boxes on the screen to allow the user to edit the properties
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
<t tx="T193">box = Tk.Frame(top, borderwidth=5)
box.pack(side="bottom")

list = [("OK",self.onOk),("Cancel",top.destroy)]
if plugin.hasapply:
	list.append(("Apply",self.onApply),)

for text,f in list:
	Tk.Button(box,text=text,width=6,command=f).pack(side="left",padx=5)</t>
<t tx="T194">def onApply(self):
	
	"""Event handler for Apply button"""
	self.writeConfiguration()
	self.plugin.mod.applyConfiguration(self.config)

def onOk(self):

	"""Event handler for Ok button"""
	self.writeConfiguration()
	self.top.destroy()</t>
<t tx="T195">def writeConfiguration(self):
	
	"""Write the configuration to disk"""

	# Set values back into the config item.
	for section, option, entry in self.entries:
		self.config.set(section, option, entry.get())

	# Write out to the file.
	f = open(self.filename, "w")
	self.config.write(f)
	f.close()
</t>
<t tx="T196">class PluginAbout:
	
	"""A class to create and run an About Plugin dialog"""
	
	@others
</t>
<t tx="T197">def __init__(self, name, version, about):
	
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
<t tx="T198">if 0: # The name is now in the window's title.
	Tk.Label(frame, text="Name:").grid(row=0, col=0, sticky="E")
	Tk.Label(frame, text=name).grid(row=0, col=1, sticky="W")
	Tk.Label(frame, text="Version").grid(row=1, col=0, sticky="E")
	Tk.Label(frame, text=version).grid(row=1, col=1, sticky="W")
	Tk.Label(frame, text=about, borderwidth=10, justify="left").grid(columnspan=2)
else:
	Tk.Label(frame, text="Version " + version).pack()
	Tk.Label(frame, text=about, borderwidth=10).pack()</t>
<t tx="T199">buttonbox = Tk.Frame(top, borderwidth=5)
buttonbox.pack(side="bottom")

self.button = Tk.Button(buttonbox, text="Close", command=top.destroy)
self.button.pack(side="bottom")</t>
<t tx="T200">def createPluginsMenu (tag,keywords):

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
<t tx="T201">for name,p in items:
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
<t tx="T202">@ignore
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
<t tx="T203">def applyConfiguration(config):
	
	sections = config.sections()
	sections.sort()

	for section in sections:
		options = config.options(section)
		options.sort()
		for option in options:
			print section, option, config.get(section, option)
</t>
<t tx="T204">def cmd_fn1(x):
	es("Fn1",color="blue")

def cmd_fn2(x):
	es("Fn2",color="blue")

def cmd_fn3(x):
	es("Fn3",color="blue")
</t>
<t tx="T205">def onSelect (tag,keywords):

	import Tkinter,os

	new_v = keywords.get("new_v")
	h = new_v.headString()
	if h[:7] == "@image ":
		filename = h[7:]
		&lt;&lt; Select Image &gt;&gt;</t>
<t tx="T206"># Display the image file in the text pane, if you can find the file
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
<t tx="T207">def onUnselect (tag,keywords):

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
<t tx="T208"># Erase image if it was previously displayed
if a.gsimage:
	try:
		 c.frame.body.delete(a.gsimage)
	except:
		es("info: no image to erase")

# And forget about it
a.gsimage = None
a.gsphoto = None
</t>
<t tx="T209">@nocolor</t>
<t tx="T210">Reorganized the code so I can find various classes more easily.
Used @others to simply the outline.

Sorted all entries in dialogs.
Sorted all entries in Plugins menu, regardless of whether they are configurable.

For all dialogs:
	Added top ivar and removed root/master params and ivars.
	Added Leo icon and title.
	Centered dialogs.

Ctors now run all dialogs as modal dialogs: this could easily be undone.

Used a grid in the properties dialog to align widgets.</t>
<t tx="T211">- We will use a new settings file called leoSettings.txt:
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
<t tx="T212">I wrote myself a plug-in which would automatically save the Leo file every so often and in doing so realized that it would be useful to be able to configure the interval between saves. Anyway, to cut a long story short, I generalized the idea and came up with the attached patch. 
 
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
<t tx="T213">"""Create a Scripts menu for LeoPy.leo"""

from leoPlugins import *
from leoGlobals import *
import glob,os

@others

if 1: # Register the handlers...
	registerHandler("create-optional-menus",createScriptsMenu)
	
	__version__ = "1.4"
	plugin_signon(__name__)</t>
<t tx="T214">def createScriptsMenu (tag,keywords):

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
<t tx="T215">if not top_scripts:
	found = false
	for dir in dirs:
		scripts = glob.glob(os.path.join(dir,"*.py"))
		if scripts:
			found = true ; break
	if not found:
		return
</t>
<t tx="T216">table = []
top_scripts.sort()
for script in top_scripts:
	name = shortFileName(script)
	def doScript(event=None,name=name):
		executeScript(name)
	table.append((name,None,doScript),)
	
c.frame.createMenuEntries(scriptsMenu, table)
</t>
<t tx="T217"># Create the submenu.
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
<t tx="T218"></t>
<t tx="T219">"""Synchronize @folder nodes with folders"""

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
<t tx="T220">@ If a node is named '@folder path_to_folder', the content (filenames) of the
folder and the children of that node will be sync. Whenever a new file is put
there, a new node will appear on top of the children list (with mark). So that
I can put my description (ie. annotation) as the content of that node. In this
way, I can find any files much easier from leo.

Moreover, I add another feature to allow you to group files(in leo) into
children of another group. This will help when there are many files in that
folder. You can logically group it in leo (or even clone it to many groups),
while keep every files in a flat/single directory on your computer.
</t>
<t tx="T221">def sync_node_to_folder(parent,d):

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
<t tx="T222">"""Inhibit changes to @read-only nodes"""

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
<t tx="T223">@ Dear Leo users,

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
<t tx="T224">@ The syntax to access files in @read-only via ftp/http is the following:

@read-only http://www.ietf.org/rfc/rfc0791.txt
@read-only ftp://ftp.someserver.org/filepath

If FTP authentication (username/password) is required, it can be specified as follows:

@read-only ftp://username:password@ftp.someserver.org/filepath

For more details, see the doc string for the class FTPurl.
</t>
<t tx="T225">class FTPurl:
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
<t tx="T226">def __init__(self, ftpURL, mode=''):
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
<t tx="T227"></t>
<t tx="T228">def read(self):
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
<t tx="T229">def readline(self):
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
<t tx="T230"></t>
<t tx="T231">def write(self, s):
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
<t tx="T232"></t>
<t tx="T233">def seek(offset=0):
	self.currentLine = 0  # we don't support fancy seeking via FTP
</t>
<t tx="T234">def flush():
	pass # no fancy stuff here.</t>
<t tx="T235">def dir(self, path=None):
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
<t tx="T236">def exists(self, path=None):
	"""Return 1 if the specified path exists. If path is omitted, the current file name is tried."""
	if path == None:
		path = self.filename

	s = self.dir(path)
	if s.lower().find('no such file') == -1:
		return 1
	else:
		return 0
</t>
<t tx="T237">def checkParams(self):
	if self.mode not in ('','b'):
		raise IOError, 'invalid mode: %s' % self.mode
	if not self.isConnectionOpen:
		raise IOError, 'ftp connection closed'
</t>
<t tx="T238">def close(self):
	"""Close an existing FTPurl connection."""
	try:
		self.ftp.quit()
	except:
		self.ftp.close()
	del self.ftp
	self.isConnectionOpen = 0</t>
<t tx="T239"># Alas, these do not seem to work on XP:
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
<t tx="T240"># Sets v's body text from the file with the given name.
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
<t tx="T241">fh = cStringIO.StringIO()
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
<t tx="T242">#  scan the outline and process @read-only nodes.
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
<t tx="T243"># override the body key handler if we are in an @read-only node.

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
<t tx="T244"># update the body text when we press enter

def on_headkey2 (tag,keywords):

	c = keywords.get("c")
	v = keywords.get("v")
	h = v.headString()
	ch = keywords.get("ch")
	if ch == '\r' and match_word(h,0,"@read-only"):
		# on-the-fly update of @read-only directives
		changed = insert_read_only_node(c,v,h[11:])
		c.setChanged(changed)</t>
<t tx="T245">def on_select1 (tag,keywords):

	# Doesn't work: the cursor doesn't start blinking.
	# Enable the body text so select will work properly.
	c = keywords.get("c")
	enable_body(c.frame.body)
</t>
<t tx="T246">def on_select2 (tag,keywords):

	c = keywords.get("c")
	v = c.currentVnode()
	h = v.headString()
	if match_word(h,0,"@read-only"):
		disable_body(c.frame.body)
	else:
		enable_body(c.frame.body)
</t>
<t tx="T247">"""If a headline starts with @rst &lt;filename&gt;, double-clicking on it will 
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
<t tx="T248">@ This plugin writes out @rst nodes as a reStructuredText file.

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
<t tx="T249">@ Change log:

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
<t tx="T250"># by Josef Dalcolmo 2003-01-13
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
<t tx="T251">try:
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
<t tx="T252"># this code snipped has been taken from code contributed by Paul Paterson 2002-12-05
from docutils.core import Publisher
from docutils.io import StringOutput, StringInput

pub = Publisher()
# Initialize the publisher
pub.source = StringInput(pub.settings, source=rstText)
pub.destination = StringOutput(pub.settings, encoding="utf-8")
pub.set_reader('standalone', None, 'restructuredtext')
pub.set_writer('html')
output = pub.publish()</t>
<t tx="T253">rstFile = file(fname,'w')
writeTreeAsRst(rstFile, fname, v, commands)
rstFile.close()
es('written: '+`fname`)</t>
<t tx="T254">def writeTreeAsRst(rstFile, fname, vnode, commands):
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
<t tx="T255"># note the first character is intentionally unused, to serve as the underline
# character in a title (in the body of the @rst node)
def underline(h,level):
	str = """#=+*^~"'`-:&gt;&lt;_"""[level]
	return str*max(len(h),4)+'\n'</t>
<t tx="T256">"""Lauches (starts) a file with the name of the headline on double-clicking it.
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
<t tx="T257">@ This plugin starts a file with the name of a headline.


</t>
<t tx="T258">@ Change log

- JD: 2003-03-11 separated out from rst plugin



</t>
<t tx="T259"># @folder behavior after an idea and sample code by:
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
<t tx="T260"># Set the base directory by searching for @folder directives in ancestors.
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
<t tx="T261"></t>
<t tx="T262">from leoPlugins import *
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
<t tx="T263"># print "overriding LeoFrame class"

import leoFrame

assert(leoFrame.leoCoreFrame.instances==0)

class myLeoFrame(leoFrame.leoCoreFrame):
	
	pass
	
	if 0:
		def __init__(self,title=None):
			print "myLeoFrame ctor",title
			leoFrame.leoCoreFrame.__init__(self,title)

leoFrame.LeoFrame = myLeoFrame</t>
<t tx="T264">import leoApp

# print "overriding app.closeLeoWindow"

oldAppCloseLeoWindow = app().closeLeoWindow

def myAppCloseLeoWindow(self,frame):
	
	global oldAppCloseLeoWindow

	oldAppCloseLeoWindow(frame)
	print "after closeLeoWindow"

funcToMethod(myAppCloseLeoWindow,leoApp.LeoApp,"closeLeoWindow")</t>
<t tx="T265">"""Override the Equal Sized Pane command"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("command1", onCommand)
	
	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T266">def onCommand (tag,keywords):

	if keywords.get("label")=="equalsizedpanes":
		es("over-riding Equal Sized Panes")
		return "override" # Anything other than None overrides.</t>
<t tx="T267">"""Redefine the "put" and "put_nl" methods"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("start2", onStart)
	
	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T268">@ This code illustrates how to redefine _any_ method of Leo.
Python makes this is almost too easy :-)
@c

def onStart (tag,keywords):

	import leoFrame
	
	# Replace frame.put with newPut.
	funcToMethod(newPut,leoFrame.LeoFrame,"put")
	
	# Replace frame.putnl with newPutNl.
	funcToMethod(newPutNl,leoFrame.LeoFrame,"putnl")
</t>
<t tx="T269"># Contrived examples of how to redefine frame.put and frame.putnl

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
<t tx="T270">"""Send all output to the log pane"""

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
<t tx="T271">"""Send output from the Execute Script command to the end of the body pane"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("start1", onStart)

	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)
</t>
<t tx="T272">def onStart (tag,keywords):
	
	import leoFrame
	
	# Replace frame.put with newPut.
	funcToMethod(newExecuteScript,leoFrame.LeoFrame,"OnExecuteScript")
</t>
<t tx="T273"># Execute the _selected_ body text as a Python script and sends the output to the end of the body pane.

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
<t tx="T274"># Same as frame.put except sends output to the end of the body text.
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
<t tx="T275">def newEnl():
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
<t tx="T276"></t>
<t tx="T277">colour
colourful
coloured
</t>
<t tx="T278"># Configuration file for mod_spelling plugin.

[main]

aspell_dir=c:\aspell\bin\aspell.exe

local_leo_dictionary=c:\prog\leoCVS\leo\plugins\mod_spelling.txt

local_language_code=en</t>
<t tx="T279">"""Spell Checker Plugin

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
<t tx="T280"></t>
<t tx="T281">def createSpellMenu(tag,keywords):
	
	"""Create the Check Spelling menu item in the Edit menu."""
	
	c = keywords.get("c")

	table = (
		("-",None,None),
		("Check Spelling","Alt+Shift+A",spellFrame.checkSpelling))

	c.frame.createMenuItemsFromTable("Edit",table)</t>
<t tx="T282">def onSelect (tag,keywords):
	
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
<t tx="T283">def onCommand (tag,keywords):
	
	"""Update the Spell Check window after any command that might change text."""

	global spellFrame
	
	if top() and top().currentVnode():
		
		# print "onCommand",tag
		spellFrame.update(show=false,fill=false)</t>
<t tx="T284">class Aspell:
	
	"""A wrapper class for Aspell spell checker"""
	
	@others
</t>
<t tx="T285"></t>
<t tx="T286">def __init__(self,local_dictionary_file,local_language_code):
	
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
<t tx="T287">def getAspellDirectory(self):
	
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
<t tx="T288">def openPipes (self):
	
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
<t tx="T289">add_dicts = ""

if self.local_dictionary:
	if self.updateDictionary():
		add_dicts = "--add-extra-dicts %s" % self.local_dictionary


</t>
<t tx="T290">def closePipes (self):
	
	"""Close the pipes to aspell.exe"""
	
	# if self.input or self.output: print "closePipes"
	
	if self.input:
		self.input.close()
		self.input = None

	if self.output:
		self.output.close()
		self.output = None</t>
<t tx="T291">def listAlternates(self, aspell_return):
	
	"""Return a list of alternates from aspell."""
	
	match = self.altre.match(aspell_return)

	if match:
		return [item.strip() for item in match.groups()[3].split(",")]
	else:
		return []</t>
<t tx="T292">def processWord(self, word):

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
<t tx="T293">def updateDictionary(self):
	
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
<t tx="T294">class spellDialog (leoFind.leoFindBase):
	
	"""A class to create and manage Leo's Spell Check dialog."""
	
	@others</t>
<t tx="T295"></t>
<t tx="T296">def __init__ (self):
	
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
<t tx="T297">if self.local_dictionary_file:

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
<t tx="T298">def getLocalDictionary(self):
	
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
<t tx="T299">def getLocalLanguageCode(self,defaultLanguageCode):
	
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
<t tx="T300">def readLocalDictionary (self,local_dictionary):
	
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
<t tx="T301">def createFrame (self):
	
	"""Create the Spelling dialog."""
	
	# Create the find panel...
	outer = Tk.Frame(self.frame,relief="groove",bd=2)
	outer.pack(padx=2,pady=2,expand=1,fill="both")

	&lt;&lt; Create the text and suggestion panes &gt;&gt;
	&lt;&lt; Create the spelling buttons &gt;&gt;
</t>
<t tx="T302">f = outer

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
<t tx="T303"># Create the button panes
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
<t tx="T304"></t>
<t tx="T305">def onAddButton (self):
	
	"""Handle a click in the Add button in the Check Spelling dialog."""

	self.add()
	self.closePipes()

</t>
<t tx="T306">def onIgnoreButton (self):

	"""Handle a click in the Ignore button in the Check Spelling dialog."""

	self.ignore()
	self.closePipes()</t>
<t tx="T307">def onChangeButton (self):
	
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
<t tx="T308">def onFindButton (self):
	
	"""Handle a click in the Find button in the Check Spelling dialog."""

	self.find()
	self.updateButtons()
	self.closePipes()</t>
<t tx="T309">def onHideButton (self):
	
	"""Handle a click in the Hide button in the Check Spelling dialog."""

	self.closePipes()
	self.top.withdraw()
</t>
<t tx="T310">def onRedoButton (self):
	
	"""Handle a click in the Redo button in the Check Spelling dialog."""

	self.c.undoer.redo() # Not a command, so command hook doesn't fire.
	self.update(show=false,fill=false)
	self.c.frame.body.focus_force()
	
def onUndoButton (self):
	
	"""Handle a click in the Undo button in the Check Spelling dialog."""

	self.c.undoer.undo() # Not a command, so command hook doesn't fire.
	self.update(show=false,fill=false)
	self.c.frame.body.focus_force()</t>
<t tx="T311"></t>
<t tx="T312">def add (self):

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
<t tx="T313">def change(self):
	
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
<t tx="T314">def checkSpelling (self,event=None):
	
	"""Open the Check Spelling dialog."""

	self.top.deiconify()
	self.top.lift()
	self.update(show=true,fill=false)</t>
<t tx="T315">def find(self):
	
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
<t tx="T316">def ignore (self):
	
	"""Ignore the incorrect word for the duration of this spell check session."""
	
	es("Ignoring ",color="blue",newline=false) ; es('%s' % self.currentWord)
	self.dictionary[self.currentWord.lower()] = 0
	self.onFindButton()</t>
<t tx="T317"></t>
<t tx="T318">def closePipes(self):
	
	self.aspell.closePipes()</t>
<t tx="T319">def fillbox(self,alts,word=None):

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
<t tx="T320">def findNextMisspelledWord(self):
	
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
<t tx="T321">@ We don't bother to call apell if the word is in our dictionary. The dictionary contains both locally 'allowed' words and 'ignored' words. We put the test before aspell rather than after aspell because the cost of checking aspell is higher than the cost of checking our local dictionary. For small local dictionaries this is probably not true and this code could easily be located after the aspell call
@c

if self.dictionary.has_key(word.lower()):
	
	# print "Ignored", word
	continue
	
# print "Didn't ignore '%s'" % word</t>
<t tx="T322">def findNextWord (self,v):
	
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
<t tx="T323">def getSuggestion (self):
	
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
<t tx="T324">def onMap (self,event=None):
	
	"""Respond to a Tk &lt;Map&gt; event."""
	
	self.update(show=false,fill=false)</t>
<t tx="T325">def onSelectListBox (self,event=None):
	
	"""Respond to a click in the selection listBox."""
	
	self.updateButtons()
	self.body.focus_set()
</t>
<t tx="T326">def update (self,show=true,fill=false):
	
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
<t tx="T327">def updateButtons (self):
	
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
<t tx="T328"></t>
<t tx="T329"></t>
<t tx="T330">[Main]
active = Yes
interval = 600

</t>
<t tx="T331">"""Autosave the Leo document every so often"""

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
<t tx="T332">def applyConfiguration(config=None):
	
	"""Called when the user presses the "Apply" button on the Properties form"""

	global LAST_AUTOSAVE, ACTIVE, AUTOSAVE_INTERVAL

	if config is None:
		fileName = os.path.join(app().loadDir,"../","plugins","mod_autosave.ini")
		config = ConfigParser.ConfigParser()
		config.read(fileName)

	ACTIVE = config.get("Main", "Active")
	AUTOSAVE_INTERVAL = int(config.get("Main", "Interval"))</t>
<t tx="T333">def autosave(tag, keywords):
	
	"""Save the current document if it has a name"""

	global LAST_AUTOSAVE

	if ACTIVE == "Yes":
		if time.time() - LAST_AUTOSAVE &gt; AUTOSAVE_INTERVAL:
			f = top().frame
			if f.mFileName and f.commands.changed:
				es("Autosave: %s" % time.ctime())
				f.commands.fileCommands.save(f.mFileName)
			LAST_AUTOSAVE = time.time()</t>
<t tx="T334">"""Timestamp all save operations to show when they occur"""

# By Paul Paterson.

from leoPlugins import *
from leoGlobals import *

import time
	
@others

if 0: # Register the handlers...

	registerHandler("command1", timestamp)

	__version__ = "0.1" # Set version for the plugin handler.
	plugin_signon(__name__)</t>
<t tx="T335">def timestamp(tag=None, keywords=None):
	
	cmd = keywords.get('label', 'save')

	if cmd.startswith("save") or cmd.startswith("tangle"):
		es("%s: %s" % (cmd, time.ctime()))
</t>
<t tx="T336"></t>
<t tx="T337">@nocolor

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
<t tx="T338"></t>
<t tx="T339">"""Create a settings menu to replace LeoConfig.leo"""

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
<t tx="T340">def createSettingsMenu (tag,keywords):

	c = keywords.get("c")
	
	global settingsMenu
	settingsMenu = c.frame.createNewMenu("&amp;Settings")</t>
<t tx="T341">@ignore

@ This code will soon become a plugin replaces Tk widgets with wxPython widgets.

To do:
	
- Convert the code in wxLeo.py to a plugin that overrides Leo's actual code.

- Override all of Leo's classes that contain Tk code, replacing Tk code with equivalent wxWindows code.

This will include the LeoDialog, LeoFrame and leoTree classes, and many others.  In particular, the colorizer will have to be rewritten.</t>
<t tx="T342"># Executing the following script executes some example wxWindows code.
# Just do the Execute Script command from here.
# For this to work the path to wxTest.py must be in sys.path.

# The first time you do this the window is created twice: once for the import and once for the reload.
# Thereafter only the reload takes effect, so only one window gets created.
# The purpose of reload is so you can change the code without restarting Leo.

import wxTest
reload(wxTest)</t>
<t tx="T343">from wxPython.wx import *

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
<t tx="T344">@language c

@ For reference only: I have deleted the C++ cruft such as importing .h files.

To do:
- convert wxWindows code to wxPython code.
- move the wxPython code to the wx plugin that doesn't exist yet.</t>
<t tx="T345">@others</t>
<t tx="T346">void alert ( const char * message )
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
<t tx="T347">void assertFailedDialog ( const char * message )
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
<t tx="T348">&lt;&lt; FindPanel declarations &gt;&gt;

@others
</t>
<t tx="T349">// &lt;&lt; FindPanel public globals &gt;&gt;
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
<t tx="T350">BEGIN_EVENT_TABLE(FindFrame, wxFrame)

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
<t tx="T351">FindFrame::FindFrame()

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
<t tx="T352">@ &lt;&lt; FindPanel methods &gt;&gt; (2 of 23)
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
<t tx="T353">
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
<t tx="T354">
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
<t tx="T355">@ &lt;&lt; FindPanel methods &gt;&gt; (4 of 23)
@c

void FindFrame::OnChangeButton (wxCommandEvent&amp; WXUNUSED(event))
{
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; doChangeButton() ;
}
</t>
<t tx="T356">@ &lt;&lt; FindPanel methods &gt;&gt; (5 of 23)
@c

void FindFrame::OnChangeAllButton (wxCommandEvent&amp; WXUNUSED(event))
{
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; doChangeAllButton() ;
}
</t>
<t tx="T357">@ &lt;&lt; FindPanel methods &gt;&gt; (6 of 23)
@c

void FindFrame::OnChangeThenFindButton (wxCommandEvent&amp; WXUNUSED(event))
{
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; doChangeThenFindButton() ;
}
</t>
<t tx="T358">@ &lt;&lt; FindPanel methods &gt;&gt; (7 of 23)
@c

void FindFrame::OnFindButton (wxCommandEvent&amp; WXUNUSED(event))
{
	// This is the default button, so make sure there is find text.
	if ( gActiveFrame &amp;&amp; find_text.Length() &gt; 0 )
		gActiveFrame -&gt; mCommands -&gt; doFindButton() ;
}
</t>
<t tx="T359">@ &lt;&lt; FindPanel methods &gt;&gt; (8 of 23)
@c

void FindFrame::OnFindAllButton (wxCommandEvent&amp; WXUNUSED(event))
{
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; doFindAllButton() ;
}
</t>
<t tx="T360">@ &lt;&lt; FindPanel methods &gt;&gt; (9 of 23)
@c

void FindFrame::OnBatchCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	batch_flag = box -&gt; GetValue();
}
</t>
<t tx="T361">@ &lt;&lt; FindPanel methods &gt;&gt; (10 of 23)
@c

void FindFrame::OnIgnoreCaseCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	ignore_case_flag = box -&gt; GetValue();
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; setup (TRUE) ; // reset the search.
}
</t>
<t tx="T362">@ &lt;&lt; FindPanel methods &gt;&gt; (11 of 23)
@c

void FindFrame::OnMarkChangesCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	mark_changes_flag = box -&gt; GetValue();
}
</t>
<t tx="T363">@ &lt;&lt; FindPanel methods &gt;&gt; (12 of 23)
@c

void FindFrame::OnMarkFindsCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	mark_finds_flag = box -&gt; GetValue();
}
</t>
<t tx="T364">@ &lt;&lt; FindPanel methods &gt;&gt; (13 of 23)
@c

void FindFrame::OnPatternMatchCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	pattern_match_flag = box -&gt; GetValue();
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; setup (TRUE) ; // reset the search.
}
</t>
<t tx="T365">@ &lt;&lt; FindPanel methods &gt;&gt; (14 of 23)
@c

void FindFrame::OnReverseCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	reverse_flag = box -&gt; GetValue();
}
</t>
<t tx="T366">@ &lt;&lt; FindPanel methods &gt;&gt; (15 of 23)
@c

void FindFrame::OnSearchBodyTextCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	search_body_flag = box -&gt; GetValue();
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; setup (TRUE) ; // reset the search.
}
</t>
<t tx="T367">@ &lt;&lt; FindPanel methods &gt;&gt; (16 of 23)
@c

void FindFrame::OnSearchHeadlineCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	search_headline_flag = box -&gt; GetValue();
}
</t>
<t tx="T368">@ &lt;&lt; FindPanel methods &gt;&gt; (17 of 23)
@c

void FindFrame::OnSuboutlineOnlyCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	suboutline_only_flag = box -&gt; GetValue();
}
</t>
<t tx="T369">@ &lt;&lt; FindPanel methods &gt;&gt; (18 of 23)
@c

void FindFrame::OnWrapAroundCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	wrap_flag = box -&gt; GetValue();
}
</t>
<t tx="T370">@ &lt;&lt; FindPanel methods &gt;&gt; (19 of 23)
@c

void FindFrame::OnWholeWordCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	whole_word_flag = box -&gt; GetValue();
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; setup (TRUE) ; // reset the search.
}
</t>
<t tx="T371">@ &lt;&lt; FindPanel methods &gt;&gt; (20 of 23)
@c

void FindFrame::OnChangeText (wxCommandEvent&amp; event)
{
	wxTextCtrl * text = (wxTextCtrl *) event.GetEventObject() ;
	change_text = text -&gt; GetValue();
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; setup (TRUE) ; // reset the search.
}
</t>
<t tx="T372">@ &lt;&lt; FindPanel methods &gt;&gt; (21 of 23)
@c

void FindFrame::OnFindText (wxCommandEvent&amp; event)
{
	wxTextCtrl * text = (wxTextCtrl *) event.GetEventObject() ;
	find_text = text -&gt; GetValue();
	if ( gActiveFrame )
		gActiveFrame -&gt; mCommands -&gt; setup (TRUE) ; // reset the search.
}
</t>
<t tx="T373">@ &lt;&lt; FindPanel methods &gt;&gt; (22 of 23)
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
<t tx="T374">@ &lt;&lt; FindPanel methods &gt;&gt; (23 of 23)
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
<t tx="T375">@others
</t>
<t tx="T376">BEGIN_EVENT_TABLE( LeoApp, wxApp)

// EVT_EXIT ( LeoApp::OnExit )

END_EVENT_TABLE()</t>
<t tx="T377">bool LeoApp::OnInit()
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
<t tx="T378">#if 0 //// Not yet: compiles, but lpCmdLine is a dummy !!!!

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
<t tx="T379">wxString cwd = ::wxGetCwd();
gAppDirectory = wxFindAppPath( cwd ) ;

// Make sure the directory does not end with a directory separator.
size_t len = gAppDirectory.Length() ;
if ( len &gt; 0 &amp;&amp; gAppDirectory.Last() == wxFILE_SEP_PATH)
	gAppDirectory = gAppDirectory.Truncate(len - 1);</t>
<t tx="T380">gIniting = TRUE ; // Disable error message if file not found.

for ( int i = 1 ; i &lt; argc ; ++ i ) {
	wxString arg = wxTheApp -&gt; argv[i] ;
	LeoFrame *frame = LeoFrame::OpenWithFileName( arg );
	if (frame) ++filesLoaded;
}

gIniting = FALSE ;</t>
<t tx="T381">LeoFrame *frame = new LeoFrame();

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
<t tx="T382">#ifdef SHERLOCK
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
<t tx="T383">TRACEP("dump_argv", 
	ecnl(); es("argc: "); elong(argc); enl();
	for ( int i = 0 ; i &lt;= argc ; ++ i ) {
		wxString arg = wxTheApp -&gt; argv[i] ;
		es("argv["); elong(i); es("]: "); es(arg.c_str()); enl();
	}
);</t>
<t tx="T384">@ &lt;&lt; LeoApp methods &gt;&gt; (2 of 2)
@c

int LeoApp::OnExit()
{
	return TRUE ;
}
</t>
<t tx="T385">@ Initialize the argv vector from a file. This routine is declared in sl.h. init_arg_parse is defined in sl.c.
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
<t tx="T386">@ &lt;&lt; LeoApp functions &gt;&gt; (2 of 2)
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
<t tx="T387">@ -- end -- &lt;&lt; LeoApp functions &gt;&gt;
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
<t tx="T388">@ &lt;&lt; log bridge functions &gt;&gt; (2 of 2)
@c

void put_cstring_to_log_window ( const char * s )
{
	if ( gActiveFrame )
		gActiveFrame -&gt; putToLog(s);
	//// else this -&gt; bufferLogMessage(s) ;
}
</t>
<t tx="T389">@others</t>
<t tx="T390">BEGIN_EVENT_TABLE(LeoFrame, wxFrame)

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
<t tx="T391">// Menu enablers...
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
<t tx="T392">LeoFrame::LeoFrame()
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
<t tx="T393">mTextChanging = 0 ;
mCopying = 0 ;
mDraggedItem =  0L ;
mReverting = FALSE ;</t>
<t tx="T394">mOutputDocFlag = TRUE ;
mTangleBatchFlag = FALSE ;
mUntangleBatchFlag = FALSE ;
mUseHeaderFlag = TRUE ;
mPageWidth = 132 ;
mTabWidth = 4;
mPresentLanguage = c_language ;
mTargetLanguage = c_language ;</t>
<t tx="T395">mSplitter1 = new wxSplitterWindow(this, cSplitterWindow,
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
<t tx="T396">#ifdef __WXGTK__ // Windows version handles shortcuts properly

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
<t tx="T397">CreateStatusBar(2);
SetStatusText("");</t>
<t tx="T398">#ifdef __WXMSW__
  this -&gt;SetIcon(wxIcon("LeoIcon"));
#endif</t>
<t tx="T399">/*
	Blinking happens on Windows without a problem.  Furthermore, setting the rate here affects _all_ windows.
*/
#ifdef __WXGTK__ // Doesn't seem to work.
	wxCaret * caret = mBodyCtrl -&gt; GetCaret();
	caret -&gt; SetBlinkTime (500) ;
#endif</t>
<t tx="T400">wxTreeItemId root = mTreeCtrl -&gt; AddRoot( "untitled" ) ;
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
<t tx="T401">@ &lt;&lt; LeoFrame methods &gt;&gt; (2 of 157)
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
<t tx="T402">@ &lt;&lt; LeoFrame methods &gt;&gt; (3 of 157)
@c

void LeoFrame::SetUntitledNumber ( long n )
{
	wxString s ( "untitled") ;
	if ( n &gt; 0 )
		s += wxString::Format("%d",n);
	this -&gt; SetTitle(s) ;
}
</t>
<t tx="T403">@ &lt;&lt; LeoFrame methods &gt;&gt; (4 of 157)
@c

void LeoFrame::putToLog ( const char * s )
{
	mLogCtrl -&gt; AppendText(s);
}
</t>
<t tx="T404">@ &lt;&lt; LeoFrame methods &gt;&gt; (5 of 157)
@c

wxString LeoFrame::getLogText ( void )
{
	return mLogCtrl -&gt; GetValue();
}
</t>
<t tx="T405"></t>
<t tx="T406">@ &lt;&lt; LeoFrame methods &gt;&gt; (6 of 157)
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
<t tx="T407">
#else

void LeoFrame::OnSetFocus(wxFocusEvent&amp; WXUNUSED(event))
{
	gActiveFrame = this ;
	if ( this -&gt; mCommands )
		this -&gt; mCommands -&gt; checkAllFileDates();
}
</t>
<t tx="T408">
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
<t tx="T409">@ &lt;&lt; LeoFrame methods &gt;&gt; (8 of 157)
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
<t tx="T410">@ &lt;&lt; LeoFrame methods &gt;&gt; (9 of 157)
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
<t tx="T411">@ &lt;&lt; LeoFrame methods &gt;&gt; (10 of 157)
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
<t tx="T412">@ &lt;&lt; LeoFrame methods &gt;&gt; (11 of 157)
@c

void LeoFrame::onTreeChanging(wxTreeEvent&amp; WXUNUSED(event))
{
	// No recursion should be possible here.
	assert(mTextChanging == 0);
	assert(mCopying == 0);
}
</t>
<t tx="T413">@ &lt;&lt; LeoFrame methods &gt;&gt; (12 of 157)
@c

void LeoFrame::onTreeKeyDown(wxTreeEvent&amp; WXUNUSED(event))
{

}
</t>
<t tx="T414">@ &lt;&lt; LeoFrame methods &gt;&gt; (13 of 157)
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
<t tx="T415">@ &lt;&lt; LeoFrame methods &gt;&gt; (14 of 157)
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
<t tx="T416">@ &lt;&lt; LeoFrame methods &gt;&gt; (15 of 157)
Editing will not be allowed if this routine does not exist.
@c

void LeoFrame::onTreeBeginLabelEdit(wxTreeEvent&amp; WXUNUSED(event))
{
	// Doing nothing is is enough to enable the edit.
}
</t>
<t tx="T417">@ &lt;&lt; LeoFrame methods &gt;&gt; (16 of 157)
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
<t tx="T418">@ &lt;&lt; LeoFrame methods &gt;&gt; (17 of 157)
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
<t tx="T419">
#endif
// &lt;&lt; LeoFrame methods &gt;&gt; (18 of 157)
void LeoFrame::OnUpdateRevert( wxUpdateUIEvent &amp;event )
{
	event.Enable(mCommands -&gt; canRevert()) ;
}
</t>
<t tx="T420">@ &lt;&lt; LeoFrame methods &gt;&gt; (19 of 157)
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
<t tx="T421">@ &lt;&lt; LeoFrame methods &gt;&gt; (20 of 157)
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
<t tx="T422">@ &lt;&lt; LeoFrame methods &gt;&gt; (21 of 157)
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
<t tx="T423">@ &lt;&lt; LeoFrame methods &gt;&gt; (22 of 157)
@c

void LeoFrame::OnClose(wxCommandEvent&amp; WXUNUSED(event))
{
	// Close the frame, giving the close handler a chance to veto.
	this -&gt; Close();
}
</t>
<t tx="T424">@ &lt;&lt; LeoFrame methods &gt;&gt; (23 of 157)
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
<t tx="T425">@ &lt;&lt; LeoFrame methods &gt;&gt; (24 of 157)
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
<t tx="T426">@ &lt;&lt; LeoFrame methods &gt;&gt; (25 of 157)
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
<t tx="T427">@ &lt;&lt; LeoFrame methods &gt;&gt; (26 of 157)
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
<t tx="T428">@ &lt;&lt; LeoFrame methods &gt;&gt; (27 of 157)
@c

void LeoFrame::OnPageSetup(wxCommandEvent&amp; WXUNUSED(event))
{
	////
}
</t>
<t tx="T429">@ &lt;&lt; LeoFrame methods &gt;&gt; (28 of 157)
@c

void LeoFrame::OnPrint(wxCommandEvent&amp; WXUNUSED(event))
{
	////
}
</t>
<t tx="T430">@ &lt;&lt; LeoFrame methods &gt;&gt; (29 of 157)
@c

void LeoFrame::OnTangleSubmenu(wxCommandEvent&amp; WXUNUSED(event))
{

}
</t>
<t tx="T431">@ &lt;&lt; LeoFrame methods &gt;&gt; (30 of 157)
@c

void LeoFrame::OnUntangleSubmenu(wxCommandEvent&amp; WXUNUSED(event))
{

}
</t>
<t tx="T432">@ &lt;&lt; LeoFrame methods &gt;&gt; (31 of 157)
@c

void LeoFrame::OnImportExportSubmenu(wxCommandEvent&amp; WXUNUSED(event))
{

}
</t>
<t tx="T433">@ &lt;&lt; LeoFrame methods &gt;&gt; (32 of 157)
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
<t tx="T434">@ &lt;&lt; LeoFrame methods &gt;&gt; (33 of 157)
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
<t tx="T435">@ &lt;&lt; LeoFrame methods &gt;&gt; (34 of 157)
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
<t tx="T436">@ &lt;&lt; LeoFrame methods &gt;&gt; (35 of 157)
@c

void LeoFrame::OnReadAtFileNodes(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; readAtFileNodes();
}
</t>
<t tx="T437">@ &lt;&lt; LeoFrame methods &gt;&gt; (36 of 157)
@c

void LeoFrame::OnWriteOutlineOnly(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; writeOutlineOnly();
}
</t>
<t tx="T438">@ &lt;&lt; LeoFrame methods &gt;&gt; (37 of 157)
@c

void LeoFrame::OnWriteAtFileNodes(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; writeAtFileNodes();
}
</t>
<t tx="T439">@ &lt;&lt; LeoFrame methods &gt;&gt; (38 of 157)
@c

void LeoFrame::OnTangleAll(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; tangleAll();
}
</t>
<t tx="T440">@ &lt;&lt; LeoFrame methods &gt;&gt; (39 of 157)
@c

void LeoFrame::OnTangleMarked(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; tangleMarked();
}
</t>
<t tx="T441">@ &lt;&lt; LeoFrame methods &gt;&gt; (40 of 157)
@c

void LeoFrame::OnTangle(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; tangle();
}
</t>
<t tx="T442">@ &lt;&lt; LeoFrame methods &gt;&gt; (41 of 157)
@c

void LeoFrame::OnUntangleAll(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; untangleAll();
}
</t>
<t tx="T443">@ &lt;&lt; LeoFrame methods &gt;&gt; (42 of 157)
@c

void LeoFrame::OnUntangleMarked(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; untangleMarked();
}
</t>
<t tx="T444">@ &lt;&lt; LeoFrame methods &gt;&gt; (43 of 157)
@c

void LeoFrame::OnUntangle(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; untangle();
}
</t>
<t tx="T445">@ &lt;&lt; LeoFrame methods &gt;&gt; (44 of 157)
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
<t tx="T446">@ &lt;&lt; LeoFrame methods &gt;&gt; (45 of 157)
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
<t tx="T447">@ &lt;&lt; LeoFrame methods &gt;&gt; (46 of 157)
@c

void LeoFrame::OnImportNowebFiles(wxCommandEvent&amp; WXUNUSED(event))
{
	////
}
</t>
<t tx="T448">@ &lt;&lt; LeoFrame methods &gt;&gt; (47 of 157)
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
<t tx="T449">@ &lt;&lt; LeoFrame methods &gt;&gt; (48 of 157)
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
<t tx="T450">@ &lt;&lt; LeoFrame methods &gt;&gt; (49 of 157)
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
<t tx="T451">@ &lt;&lt; LeoFrame methods &gt;&gt; (50 of 157)
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
<t tx="T452">@ &lt;&lt; LeoFrame methods &gt;&gt; (51 of 157)
@c

void LeoFrame::OnUpdateDelete ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mBodyCtrl &amp;&amp; mBodyCtrl -&gt; CanCut( ) ) ;
}
</t>
<t tx="T453">@ &lt;&lt; LeoFrame methods &gt;&gt; (52 of 157)
@c

void LeoFrame::OnUpdateExtract ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canExtract() ) ;
}
</t>
<t tx="T454">@ &lt;&lt; LeoFrame methods &gt;&gt; (53 of 157)
@c

void LeoFrame::OnUpdateExtractNames ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canExtractSectionNames() ) ;
}
</t>
<t tx="T455">@ &lt;&lt; LeoFrame methods &gt;&gt; (54 of 157)
@c

void LeoFrame::OnUpdateExtractSection ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canExtractSection() ) ;
}
</t>
<t tx="T456">@ &lt;&lt; LeoFrame methods &gt;&gt; (55 of 157)
@c

void LeoFrame::OnUpdateFind ( wxUpdateUIEvent&amp; event )
{
	event.Enable( find_text . Length() &gt; 0 ) ;
}
</t>
<t tx="T457">@ &lt;&lt; LeoFrame methods &gt;&gt; (56 of 157)
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
<t tx="T458">@ &lt;&lt; LeoFrame methods &gt;&gt; (57 of 157)
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
<t tx="T459">@ &lt;&lt; LeoFrame methods &gt;&gt; (58 of 157)
@c

void LeoFrame::OnUpdateReplace ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; changeIsEnabled() ) ;
}
</t>
<t tx="T460">@ &lt;&lt; LeoFrame methods &gt;&gt; (59 of 157)
@c

void LeoFrame::OnUpdateSelectAll ( wxUpdateUIEvent&amp; event )
{
	wxWindow * w = this -&gt; FindFocus();

	event.Enable( w &amp;&amp; ( w == mBodyCtrl || w == mLogCtrl ) ) ;
}
</t>
<t tx="T461">@ &lt;&lt; LeoFrame methods &gt;&gt; (60 of 157)
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
<t tx="T462">@ &lt;&lt; LeoFrame methods &gt;&gt; (61 of 157)
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
<t tx="T463">@ &lt;&lt; LeoFrame methods &gt;&gt; (62 of 157)
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
<t tx="T464">@ &lt;&lt; LeoFrame methods &gt;&gt; (63 of 157)
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
<t tx="T465">@ &lt;&lt; LeoFrame methods &gt;&gt; (64 of 157)
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
<t tx="T466">@ &lt;&lt; LeoFrame methods &gt;&gt; (65 of 157)
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
<t tx="T467">@ &lt;&lt; LeoFrame methods &gt;&gt; (66 of 157)
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
<t tx="T468">@ &lt;&lt; LeoFrame methods &gt;&gt; (67 of 157)
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
<t tx="T469">@ &lt;&lt; LeoFrame methods &gt;&gt; (68 of 157)
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
<t tx="T470">@ &lt;&lt; LeoFrame methods &gt;&gt; (69 of 157)
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
<t tx="T471">@ &lt;&lt; LeoFrame methods &gt;&gt; (70 of 157)
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
<t tx="T472">@ &lt;&lt; LeoFrame methods &gt;&gt; (71 of 157)
@c

void LeoFrame::OnSyntaxColoring(wxCommandEvent&amp; WXUNUSED(event))
{
	////
}
</t>
<t tx="T473">@ &lt;&lt; LeoFrame methods &gt;&gt; (72 of 157)
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
<t tx="T474">@ &lt;&lt; LeoFrame methods &gt;&gt; (73 of 157)
@c

void LeoFrame::OnConvertBlanks(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; convertBlanks();
}
</t>
<t tx="T475">@ &lt;&lt; LeoFrame methods &gt;&gt; (74 of 157)
@c

void LeoFrame::OnExtractSection(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; extractSection();
}
</t>
<t tx="T476">@ &lt;&lt; LeoFrame methods &gt;&gt; (75 of 157)
@c

void LeoFrame::OnExtractNames(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; extractSectionNames();
}
</t>
<t tx="T477">@ &lt;&lt; LeoFrame methods &gt;&gt; (76 of 157)
@c

void LeoFrame::OnExtract(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; extract();
}
</t>
<t tx="T478">@ &lt;&lt; LeoFrame methods &gt;&gt; (77 of 157)
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
<t tx="T479">@ &lt;&lt; LeoFrame methods &gt;&gt; (78 of 157)
@c

void LeoFrame::OnFindNext(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; doFindNextCommand();
}
</t>
<t tx="T480">@ &lt;&lt; LeoFrame methods &gt;&gt; (79 of 157)
@c

void LeoFrame::OnFindPrevious(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; doFindPreviousCommand();
}
</t>
<t tx="T481">@ &lt;&lt; LeoFrame methods &gt;&gt; (80 of 157)
@c

void LeoFrame::OnReplace(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; doChangeCommand();
}
</t>
<t tx="T482">@ &lt;&lt; LeoFrame methods &gt;&gt; (81 of 157)
@c

void LeoFrame::OnReplaceThenFind(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; doChangeThenFindCommand();
}
</t>
<t tx="T483">@ &lt;&lt; LeoFrame methods &gt;&gt; (82 of 157)
@c

void LeoFrame::OnUpdateCutNode ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canCutOutline() ) ;
}
</t>
<t tx="T484">@ &lt;&lt; LeoFrame methods &gt;&gt; (83 of 157)
@c

void LeoFrame::OnUpdateDeleteNode ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canDeleteHeadline() ) ;
}
</t>
<t tx="T485">@ &lt;&lt; LeoFrame methods &gt;&gt; (84 of 157)
@c

void LeoFrame::OnUpdatePasteNode ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canPasteOutline() ) ;
}
</t>
<t tx="T486">@ &lt;&lt; LeoFrame methods &gt;&gt; (85 of 157)
@c

void LeoFrame::OnUpdateSortNode ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canSort() ) ;
}
</t>
<t tx="T487">@ &lt;&lt; LeoFrame methods &gt;&gt; (86 of 157)
@c

void LeoFrame::OnUpdateExpandAll ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canExpandAllHeadlines() ) ;
}
</t>
<t tx="T488">@ &lt;&lt; LeoFrame methods &gt;&gt; (87 of 157)
@c

void LeoFrame::OnUpdateExpandAllChildren ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canExpandAllSubheads() ) ;
}
</t>
<t tx="T489">@ &lt;&lt; LeoFrame methods &gt;&gt; (88 of 157)
@c

void LeoFrame::OnUpdateExpandChildren ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canExpandAllSubheads() ) ;
}
</t>
<t tx="T490">@ &lt;&lt; LeoFrame methods &gt;&gt; (89 of 157)
@c

void LeoFrame::OnUpdateContractAll ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canContractAllHeadlines() ) ;
}
</t>
<t tx="T491">@ &lt;&lt; LeoFrame methods &gt;&gt; (90 of 157)
@c

void LeoFrame::OnUpdateContractAllChildren ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canContractAllSubheads() ) ;
}
</t>
<t tx="T492">@ &lt;&lt; LeoFrame methods &gt;&gt; (91 of 157)
@c

void LeoFrame::OnUpdateContractChildren ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canContractSubheads() ) ;
}
</t>
<t tx="T493">@ &lt;&lt; LeoFrame methods &gt;&gt; (92 of 157)
@c

void LeoFrame::OnUpdateMoveDown ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canMoveOutlineDown() ) ;
}
</t>
<t tx="T494">@ &lt;&lt; LeoFrame methods &gt;&gt; (93 of 157)
@c

void LeoFrame::OnUpdateMoveLeft ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canMoveOutlineLeft() ) ;
}
</t>
<t tx="T495">@ &lt;&lt; LeoFrame methods &gt;&gt; (94 of 157)
@c

void LeoFrame::OnUpdateMoveRight ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canMoveOutlineRight() ) ;
}
</t>
<t tx="T496">@ &lt;&lt; LeoFrame methods &gt;&gt; (95 of 157)
@c

void LeoFrame::OnUpdateMoveUp ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canMoveOutlineUp() ) ;
}
</t>
<t tx="T497">@ &lt;&lt; LeoFrame methods &gt;&gt; (96 of 157)
@c

void LeoFrame::OnUpdatePromote ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canPromote() ) ;
}
</t>
<t tx="T498">@ &lt;&lt; LeoFrame methods &gt;&gt; (97 of 157)
@c

void LeoFrame::OnUpdateDemote ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canDemote() ) ;
}
</t>
<t tx="T499">@ &lt;&lt; LeoFrame methods &gt;&gt; (98 of 157)
@c

void LeoFrame::OnUpdateGoPrevVisible ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canSelectVisBack() ) ;
}
</t>
<t tx="T500">@ &lt;&lt; LeoFrame methods &gt;&gt; (99 of 157)
@c

void LeoFrame::OnUpdateGoNextVisible ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canSelectVisNext() ) ;
}
</t>
<t tx="T501">@ &lt;&lt; LeoFrame methods &gt;&gt; (100 of 157)
@c

void LeoFrame::OnUpdateGoBack ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canSelectThreadBack() ) ;
}
</t>
<t tx="T502">@ &lt;&lt; LeoFrame methods &gt;&gt; (101 of 157)
@c

void LeoFrame::OnUpdateGoNext ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canSelectThreadNext() ) ;
}
</t>
<t tx="T503">@ &lt;&lt; LeoFrame methods &gt;&gt; (102 of 157)
@c

void LeoFrame::OnUpdateMark ( wxUpdateUIEvent&amp; event )
{
	vnode * v = mCommands -&gt; currentVnode();
	event.SetText( ( v &amp;&amp; v-&gt;isMarked()) ? "Unmark" : "Mark") ;
}
</t>
<t tx="T504">@ &lt;&lt; LeoFrame methods &gt;&gt; (103 of 157)
@c

void LeoFrame::OnUpdateMarkSubheads ( wxUpdateUIEvent&amp; event )
{
	vnode * v = mCommands -&gt; currentVnode();
	event.Enable( v &amp;&amp; v -&gt; hasChildren() ) ;
}
</t>
<t tx="T505">@ &lt;&lt; LeoFrame methods &gt;&gt; (104 of 157)
@c

void LeoFrame::OnUpdateMarkChangedItems ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canMarkChangedHeadlines() ) ;
}
</t>
<t tx="T506">@ &lt;&lt; LeoFrame methods &gt;&gt; (105 of 157)
@c

void LeoFrame::OnUpdateMarkChangedRoots ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canMarkChangedRoots() ) ;
}
</t>
<t tx="T507">@ &lt;&lt; LeoFrame methods &gt;&gt; (106 of 157)
@c

void LeoFrame::OnUpdateGoToNextMarked ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canGoToNextMarkedHeadline() ) ;
}
</t>
<t tx="T508">@ &lt;&lt; LeoFrame methods &gt;&gt; (107 of 157)
@c

void LeoFrame::OnUpdateGoToNextChanged ( wxUpdateUIEvent&amp; event )
{
	event.Enable( mCommands -&gt; canGoToNextDirtyHeadline() ) ;
}
</t>
<t tx="T509">@ &lt;&lt; LeoFrame methods &gt;&gt; (108 of 157)
@c

void LeoFrame::OnCutNode(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; cutOutline();
}
</t>
<t tx="T510">@ &lt;&lt; LeoFrame methods &gt;&gt; (109 of 157)
@c

void LeoFrame::OnCopyNode(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; copyOutline();
}
</t>
<t tx="T511">@ &lt;&lt; LeoFrame methods &gt;&gt; (110 of 157)
@c

void LeoFrame::OnPasteNode(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; pasteOutline();
}
</t>
<t tx="T512">@ &lt;&lt; LeoFrame methods &gt;&gt; (111 of 157)
@c

void LeoFrame::OnDeleteNode(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; deleteHeadline();
}
</t>
<t tx="T513">@ &lt;&lt; LeoFrame methods &gt;&gt; (112 of 157)
@c

void LeoFrame::OnInsertNode(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; insertHeadline();
}
</t>
<t tx="T514">@ &lt;&lt; LeoFrame methods &gt;&gt; (113 of 157)
@c

void LeoFrame::OnCloneNode(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; clone();
}
</t>
<t tx="T515">@ &lt;&lt; LeoFrame methods &gt;&gt; (114 of 157)
@c

void LeoFrame::OnSortNode(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; sort();
}
</t>
<t tx="T516">@ &lt;&lt; LeoFrame methods &gt;&gt; (115 of 157)
@c

void LeoFrame::OnExpandAll(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandAllHeadlines();
}
</t>
<t tx="T517">@ &lt;&lt; LeoFrame methods &gt;&gt; (116 of 157)
@c

void LeoFrame::OnExpandAllChildren(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandAllSubheads();
}
</t>
<t tx="T518">@ &lt;&lt; LeoFrame methods &gt;&gt; (117 of 157)
@c

void LeoFrame::OnExpandChildren(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandSubheads();
}
</t>
<t tx="T519">@ &lt;&lt; LeoFrame methods &gt;&gt; (118 of 157)
@c

void LeoFrame::OnContractAll(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; contractAllHeadlines();
}
</t>
<t tx="T520">@ &lt;&lt; LeoFrame methods &gt;&gt; (119 of 157)
@c

void LeoFrame::OnContractAllChildren(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; contractAllSubheads();
}
</t>
<t tx="T521">@ &lt;&lt; LeoFrame methods &gt;&gt; (120 of 157)
@c

void LeoFrame::OnContractChildren(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; contractSubheads();
}
</t>
<t tx="T522">@ &lt;&lt; LeoFrame methods &gt;&gt; (121 of 157)
@c

void LeoFrame::OnExpandNextLevel(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandNextLevel();
}
</t>
<t tx="T523">@ &lt;&lt; LeoFrame methods &gt;&gt; (122 of 157)
@c

void LeoFrame::OnExpandToLevel1(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel1();
}
</t>
<t tx="T524">@ &lt;&lt; LeoFrame methods &gt;&gt; (123 of 157)
@c

void LeoFrame::OnExpandToLevel2(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel2();
}
</t>
<t tx="T525">@ &lt;&lt; LeoFrame methods &gt;&gt; (124 of 157)
@c

void LeoFrame::OnExpandToLevel3(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel3();
}
</t>
<t tx="T526">@ &lt;&lt; LeoFrame methods &gt;&gt; (125 of 157)
@c

void LeoFrame::OnExpandToLevel4(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel4();
}
</t>
<t tx="T527">@ &lt;&lt; LeoFrame methods &gt;&gt; (126 of 157)
@c

void LeoFrame::OnExpandToLevel5(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel5();
}
</t>
<t tx="T528">@ &lt;&lt; LeoFrame methods &gt;&gt; (127 of 157)
@c

void LeoFrame::OnExpandToLevel6(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel6();
}
</t>
<t tx="T529">@ &lt;&lt; LeoFrame methods &gt;&gt; (128 of 157)
@c

void LeoFrame::OnExpandToLevel7(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel7();
}
</t>
<t tx="T530">@ &lt;&lt; LeoFrame methods &gt;&gt; (129 of 157)
@c

void LeoFrame::OnExpandToLevel8(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel8();
}
</t>
<t tx="T531">@ &lt;&lt; LeoFrame methods &gt;&gt; (130 of 157)
@c

void LeoFrame::OnExpandToLevel9(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; expandLevel9();
}
</t>
<t tx="T532">@ &lt;&lt; LeoFrame methods &gt;&gt; (131 of 157)
@c

void LeoFrame::OnMoveDown(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; moveOutlineDown();
}
</t>
<t tx="T533">@ &lt;&lt; LeoFrame methods &gt;&gt; (132 of 157)
@c

void LeoFrame::OnMoveLeft(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; moveOutlineLeft();
}
</t>
<t tx="T534">@ &lt;&lt; LeoFrame methods &gt;&gt; (133 of 157)
@c

void LeoFrame::OnMoveRight(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; moveOutlineRight();
}
</t>
<t tx="T535">@ &lt;&lt; LeoFrame methods &gt;&gt; (134 of 157)
@c

void LeoFrame::OnMoveUp(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; moveOutlineUp();
}
</t>
<t tx="T536">@ &lt;&lt; LeoFrame methods &gt;&gt; (135 of 157)
@c

void LeoFrame::OnPromote(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; promote();
}
</t>
<t tx="T537">@ &lt;&lt; LeoFrame methods &gt;&gt; (136 of 157)
@c

void LeoFrame::OnDemote(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; demote();
}
</t>
<t tx="T538">@ &lt;&lt; LeoFrame methods &gt;&gt; (137 of 157)
@c

void LeoFrame::OnGoPrevVisible(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; moveOutlineUp();
}
</t>
<t tx="T539">@ &lt;&lt; LeoFrame methods &gt;&gt; (138 of 157)
@c

void LeoFrame::OnGoNextVisible(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; selectVisNext();
}
</t>
<t tx="T540">@ &lt;&lt; LeoFrame methods &gt;&gt; (139 of 157)
@c

void LeoFrame::OnGoBack(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; selectThreadBack();
}
</t>
<t tx="T541">@ &lt;&lt; LeoFrame methods &gt;&gt; (140 of 157)
@c

void LeoFrame::OnGoNext(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; selectThreadNext();
}
</t>
<t tx="T542">@ &lt;&lt; LeoFrame methods &gt;&gt; (141 of 157)
@c

void LeoFrame::OnMark(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; markHeadline();
}
</t>
<t tx="T543">@ &lt;&lt; LeoFrame methods &gt;&gt; (142 of 157)
@c

void LeoFrame::OnMarkSubheads(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; markSubheads();
}
</t>
<t tx="T544">@ &lt;&lt; LeoFrame methods &gt;&gt; (143 of 157)
@c

void LeoFrame::OnMarkChangedItems(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; markChangedHeadlines();
}
</t>
<t tx="T545">@ &lt;&lt; LeoFrame methods &gt;&gt; (144 of 157)
@c

void LeoFrame::OnMarkChangedRoots(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; markChangedRoots();
}
</t>
<t tx="T546">@ &lt;&lt; LeoFrame methods &gt;&gt; (145 of 157)
@c

void LeoFrame::OnMarkAllAtFileNodesDirty(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; markAllAtFileNodesDirty();
}
</t>
<t tx="T547">@ &lt;&lt; LeoFrame methods &gt;&gt; (146 of 157)
@c

void LeoFrame::OnMarkAtFileNodesDirty(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; markAtFileNodesDirty();
}
</t>
<t tx="T548">@ &lt;&lt; LeoFrame methods &gt;&gt; (147 of 157)
@c

void LeoFrame::OnUnmarkAll(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; unmarkAll();
}
</t>
<t tx="T549">@ &lt;&lt; LeoFrame methods &gt;&gt; (148 of 157)
@c

void LeoFrame::OnGoToNextMarked(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; goToNextMarkedHeadline();
}
</t>
<t tx="T550">@ &lt;&lt; LeoFrame methods &gt;&gt; (149 of 157)
@c

void LeoFrame::OnGoToNextChanged(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; goToNextDirtyHeadline();
}
</t>
<t tx="T551">@ &lt;&lt; LeoFrame methods &gt;&gt; (150 of 157)
@c

void LeoFrame::OnEqualSizedPanes(wxCommandEvent&amp; WXUNUSED(event))
{
	mCommands -&gt; equalSizedPanes();
}
</t>
<t tx="T552">@ &lt;&lt; LeoFrame methods &gt;&gt; (151 of 157)
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
<t tx="T553">@ &lt;&lt; LeoFrame methods &gt;&gt; (152 of 157)
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
<t tx="T554">@ &lt;&lt; LeoFrame methods &gt;&gt; (153 of 157)
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
<t tx="T555">@ &lt;&lt; LeoFrame methods &gt;&gt; (154 of 157)
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
<t tx="T556">@ &lt;&lt; LeoFrame methods &gt;&gt; (155 of 157)
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
<t tx="T557">#endif // __WXMSW__
// &lt;&lt; LeoFrame methods &gt;&gt; (156 of 157)
void LeoFrame::OnRecentWindows(wxCommandEvent&amp; WXUNUSED(event))
{
	//// Not ready yet.
}
</t>
<t tx="T558">@ &lt;&lt; LeoFrame methods &gt;&gt; (157 of 157)
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
<t tx="T559">&lt;&lt; LeoPrefs declarations &gt;&gt;

@others
</t>
<t tx="T560">// &lt;&lt; LeoPrefs private constants &gt;&gt;
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
<t tx="T561">BEGIN_EVENT_TABLE(PrefsFrame, wxFrame)

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
<t tx="T562">PrefsFrame::PrefsFrame()

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
<t tx="T563">@ &lt;&lt; LeoPrefs methods &gt;&gt; (2 of 14)
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
<t tx="T564">@ &lt;&lt; LeoPrefs methods &gt;&gt; (3 of 14)
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
<t tx="T565">@ &lt;&lt; LeoPrefs methods &gt;&gt; (4 of 14)
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
<t tx="T566">@ &lt;&lt; LeoPrefs methods &gt;&gt; (5 of 14)
@c

void PrefsFrame::OnActivatePrefsFrame(wxActivateEvent&amp; event)
{
	if ( gPrefsFrame &amp;&amp; event.GetActive() )
		gPrefsFrame -&gt; initialize();
}
</t>
<t tx="T567">@ &lt;&lt; LeoPrefs methods &gt;&gt; (6 of 14)
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
<t tx="T568">@ &lt;&lt; LeoPrefs methods &gt;&gt; (7 of 14)
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
<t tx="T569">@ &lt;&lt; LeoPrefs methods &gt;&gt; (8 of 14)
@c

void PrefsFrame::OnDoneBatCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	arg_tangle_batch = default_tangle_batch = box -&gt; GetValue() ;
	if ( gActiveFrame ) gActiveFrame -&gt; mTangleBatchFlag = arg_tangle_batch ;
}
</t>
<t tx="T570">@ &lt;&lt; LeoPrefs methods &gt;&gt; (9 of 14)
@c

void PrefsFrame::OnUnBatCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	arg_untangle_batch = default_untangle_batch = box -&gt; GetValue() ;
	if ( gActiveFrame ) gActiveFrame -&gt; mUntangleBatchFlag = arg_untangle_batch ;
}
</t>
<t tx="T571">@ &lt;&lt; LeoPrefs methods &gt;&gt; (10 of 14)
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
<t tx="T572">@ &lt;&lt; LeoPrefs methods &gt;&gt; (11 of 14)
@c

void PrefsFrame::OnHeaderCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	arg_use_header_flag = default_use_header_flag = box -&gt; GetValue() ;
	if ( gActiveFrame ) gActiveFrame -&gt; mUseHeaderFlag = arg_use_header_flag ;
}
</t>
<t tx="T573">@ &lt;&lt; LeoPrefs methods &gt;&gt; (12 of 14)
@c

void PrefsFrame::OnDocChunksCheckBox (wxCommandEvent&amp; event)
{
	wxCheckBox * box = (wxCheckBox *)event.GetEventObject() ;
	arg_output_doc_flag = default_output_doc_flag = box -&gt; GetValue();
	if ( gActiveFrame ) gActiveFrame -&gt; mOutputDocFlag = arg_output_doc_flag ;
}
</t>
<t tx="T574">@ &lt;&lt; LeoPrefs methods &gt;&gt; (13 of 14)
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
<t tx="T575">@ &lt;&lt; LeoPrefs methods &gt;&gt; (14 of 14)
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
<t tx="T576">@ You may have to change the paths to the wxWindows docs by hand:  find/change doesn't work in headlines.
</t>
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
<t tx="T590"></t>
<t tx="T591"></t>
<t tx="T592"></t>
<t tx="T593"></t>
<t tx="T594"></t>
<t tx="T595"></t>
<t tx="T596"></t>
<t tx="T597"></t>
<t tx="T598"></t>
<t tx="T599"></t>
<t tx="T600"></t>
<t tx="T601"></t>
<t tx="T602"></t>
<t tx="T603"></t>
<t tx="T604"></t>
<t tx="T605"></t>
<t tx="T606"></t>
<t tx="T607"></t>
<t tx="T608"></t>
<t tx="T609"></t>
<t tx="T610">Will I ever have to use wxArray, wxList, wxStream, wxString.

In particular, can I use Python strings instead of wxStrings?

Can I create multiple windows without using the wxDoc classes?</t>
<t tx="T611"># Executing the following script creates a wxWindows prototype of Leo.
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
<t tx="T612">from wxPython import wx

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
<t tx="T613">class leoApp (wx.wxApp):
	
	@others
</t>
<t tx="T614">def OnInit(self):
	# print "leoApp:OnInit"
	return true</t>
<t tx="T615">class leoFrame(wx.wxFrame):
	@others</t>
<t tx="T616">def __init__ (self):
	
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
<t tx="T617">def createMenus(self):

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
<t tx="T618">fileMenu = wx.wxMenu()
&lt;&lt; Create the initial items of the file menu &gt;&gt;
&lt;&lt; Create the Read/Write submenu &gt;&gt;
&lt;&lt; Create the Tangle submenu &gt;&gt;
&lt;&lt; Create the Untangle submenu &gt;&gt;
&lt;&lt; Create the Import Files submenu &gt;&gt;

fileMenu.AppendSeparator()

fileMenu.Append(cQuitMenuItem, "E&amp;xit\tCtrl-Q", "Quit Leo")</t>
<t tx="T619">fileMenu.Append ( cNewMenuItem, "&amp;New\tCtrl-N",
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
<t tx="T620">readWriteMenu = wx.wxMenu()

readWriteMenu.Append (cReadOutlineOnlyMenuItem,
	"Read Outline Only", "Read outline only")
readWriteMenu.Append (cReadAtFileNodesMenuItem,
	"Read @file Nodes", "Read @file nodes")
readWriteMenu.Append (cWriteOutlineOnlyMenuItem,
	"Write Outline Only", "Write outline only")
readWriteMenu.Append (cWriteAtFileNodesMenuItem,
	"Write @file Nodes", "Write @file nodes")

fileMenu.Append(cReadWriteSubmenuItem, "Read/Write...", readWriteMenu, "")</t>
<t tx="T621">tangleMenu = wx.wxMenu()

tangleMenu.Append (cTangleAllMenuItem,
	"Tangle &amp;All\tShift-Ctrl-A", "Tangle all roots")
tangleMenu.Append (cTangleMarkedMenuItem,
	"Tangle &amp;Marked\tShift-Ctrl-M", "Tangle all marked roots")
tangleMenu.Append (cTangleMenuItem,
	"&amp;Tangle\tShift-Ctrl-T", "Tangle selected headline")

fileMenu.Append(cTangleSubmenuItem, "&amp;Tangle...", tangleMenu, "")

# Doesn't work either.
fileMenu.SetHelpString(cTangleSubmenuItem, "Tangle commands...")</t>
<t tx="T622">untangleMenu = wx.wxMenu()

untangleMenu.Append (cUntangleAllMenuItem,
	"Untangle &amp;All", "Tangle all roots")
untangleMenu.Append (cUntangleMarkedMenuItem,
	"Untangle &amp;Marked", "Tangle all marked roots")
untangleMenu.Append (cUntangleMenuItem,
	"&amp;Untangle\tShift-Ctrl-U", "Tangle selected headline")

fileMenu.Append(cUntangleSubmenuItem, "&amp;Untangle...", untangleMenu, "")</t>
<t tx="T623">importMenu = wx.wxMenu()

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
<t tx="T624">editMenu = wx.wxMenu()
&lt;&lt; Create the initial items of the Edit menu &gt;&gt;
&lt;&lt; Create the Edit Body submenu &gt;&gt;
&lt;&lt; Create the Find submenu &gt;&gt;
&lt;&lt; Create the final items of the Edit menu &gt;&gt;</t>
<t tx="T625">editMenu.Append ( cUndoMenuItem, "&amp;Undo\tCtrl-Z", "Undo last operation" )

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
<t tx="T626">findMenu = wx.wxMenu()

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
<t tx="T627">editMenu.Append ( cFontPanelMenuItem,
	"&amp;Font Panel\tAlt-Shift-T", "Open Font panel" )

editMenu.Append ( cSyntaxColoringMenuItem,
	"&amp;Syntax Coloring...\tAlt-Shift-S", "Set syntax coloring options" )

editMenu.Enable(cSyntaxColoringMenuItem, FALSE)

editMenu.AppendSeparator()

editMenu.Append ( cPreferencesMenuItem,
	"Preferences\tCtrl-Y", "Open Preferences panel" )</t>
<t tx="T628">editBodyMenu = wx.wxMenu()

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
<t tx="T629">outlineMenu = wx.wxMenu()
&lt;&lt; Create the initial items of the Outline menu &gt;&gt;
&lt;&lt; Create the Expand/Contract submenu &gt;&gt;
&lt;&lt; Create the Move/Select submenu &gt;&gt;
&lt;&lt; Create the Mark/Go To submenu &gt;&gt;
</t>
<t tx="T630">outlineMenu.Append ( cCutNodeMenuItem,
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
<t tx="T631">expandContractMenu = wx.wxMenu()

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
<t tx="T632">moveSelectMenu = wx.wxMenu()

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
<t tx="T633">markGoToMenu = wx.wxMenu()

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
<t tx="T634">windowMenu = wx.wxMenu()

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
<t tx="T635">helpMenu = wx.wxMenu()

helpMenu.Append(cAboutLeoMenuItem,
	"&amp;About Leo...",
	"Show about dialog")</t>
<t tx="T636">def createMenuBar(self):
	
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
<t tx="T637">editMenu = self.createNewMenu("&amp;Edit")
&lt;&lt; create the first top-level edit entries &gt;&gt;
&lt;&lt; create the edit body submenu &gt;&gt;
&lt;&lt; create the edit headline submenu &gt;&gt;
&lt;&lt; create the find submenu &gt;&gt;
&lt;&lt; create the last top-level edit entries &gt;&gt;
</t>
<t tx="T638">table = (
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
<t tx="T639">editBodyMenu = self.createNewMenu("Edit &amp;Body...","Edit")

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
<t tx="T640">editHeadlineMenu = self.createNewMenu("Edit &amp;Headline...","Edit")

table = (
	("Edit &amp;Headline","Ctrl+H",self.OnEditHeadline),
	("&amp;End Edit Headline","Escape",self.OnEndEditHeadline),
	("&amp;Abort Edit Headline","Shift-Escape",self.OnAbortEditHeadline),
	("Insert Headline Time/&amp;Date","Shift+Ctrl+H",self.OnInsertHeadlineTime))
	
	# 5/16/03 EKR: I dislike this command.
	#("Toggle Angle Brackets","Ctrl+B",self.OnToggleAngleBrackets)
	
self.createMenuEntries(editHeadlineMenu,table)

</t>
<t tx="T641">findMenu = self.createNewMenu("&amp;Find...","Edit")

table = (
	("&amp;Find Panel","Ctrl+F",self.OnFindPanel),
	("-",None,None),
	("Find &amp;Next","F3",self.OnFindNext),
	("Find &amp;Previous","F4",self.OnFindPrevious),
	("&amp;Replace","Ctrl+=",self.OnReplace),
	("Replace, &amp;Then Find","Ctrl+-",self.OnReplaceThenFind))

self.createMenuEntries(findMenu,table)
</t>
<t tx="T642">label = choose(c.tree.colorizer.showInvisibles,"Hide In&amp;visibles","Show In&amp;visibles")

table = (
	("&amp;Go To Line Number","Alt+G",self.OnGoToLineNumber),
	("&amp;Execute Script","Alt+Shift+E",self.OnExecuteScript),
	("Set Fon&amp;t...","Shift+Alt+T",self.OnFontPanel),
	("Set &amp;Colors...","Shift+Alt+C",self.OnColorPanel),
	(label,"Alt+V",self.OnViewAllCharacters),
	("-",None,None),
	("Prefere&amp;nces","Ctrl+Y",self.OnPreferences))

self.createMenuEntries(editMenu,table)</t>
<t tx="T643">fileMenu = self.createNewMenu("&amp;File")
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
<t tx="T644">@ leo.py will probably never have a Print command.  Instead, export text files that may be formatted and printed as desired.
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
<t tx="T645">recentFilesMenu = self.createNewMenu("Recent &amp;Files...","File")
self.recentFiles = app().config.getRecentFiles()
self.createRecentFilesMenuItems()

</t>
<t tx="T646">readWriteMenu = self.createNewMenu("&amp;Read/Write...","File")

table = [
		("&amp;Read Outline Only","Shift+Ctrl+R",self.OnReadOutlineOnly),
		("Read @file &amp;Nodes",None,self.OnReadAtFileNodes),
		("-",None,None),
		("Write &amp;Dirty @file Nodes","Shift+Ctrl+Q",self.OnWriteDirtyAtFileNodes),
		("Write &amp;Missing @file Nodes",None,self.OnWriteMissingAtFileNodes),
		("Write &amp;Outline Only",None,self.OnWriteOutlineOnly),
		("&amp;Write @file Nodes","Shift+Ctrl+W",self.OnWriteAtFileNodes)]

self.createMenuEntries(readWriteMenu,table)</t>
<t tx="T647">tangleMenu = self.createNewMenu("&amp;Tangle...","File")

table = (
	("Tangle &amp;All","Shift+Ctrl+A",self.OnTangleAll),
	("Tangle &amp;Marked","Shift+Ctrl+M",self.OnTangleMarked),
	("&amp;Tangle","Shift+Ctrl+T",self.OnTangle))

self.createMenuEntries(tangleMenu,table)

</t>
<t tx="T648">untangleMenu = self.createNewMenu("&amp;Untangle...","File")

table = (
	("Untangle &amp;All",None,self.OnUntangleAll),
	("Untangle &amp;Marked",None,self.OnUntangleMarked),
	("&amp;Untangle","Shift+Ctrl+U",self.OnUntangle))
	
self.createMenuEntries(untangleMenu,table)

</t>
<t tx="T649">importMenu = self.createNewMenu("&amp;Import...","File")

table = (
	("Import To @&amp;file","Shift+Ctrl+F",self.OnImportAtFile),
	("Import To @&amp;root",None,self.OnImportAtRoot),
	("Import &amp;CWEB Files",None,self.OnImportCWEBFiles),
	("Import &amp;noweb Files",None,self.OnImportNowebFiles),
	("Import Flattened &amp;Outline",None,self.OnImportFlattenedOutline))

self.createMenuEntries(importMenu,table)

</t>
<t tx="T650">exportMenu = self.createNewMenu("&amp;Export...","File")

table = [
	("Export &amp;Headlines",None,self.OnExportHeadlines),
	("Outline To &amp;CWEB",None,self.OnOutlineToCWEB),
	("Outline To &amp;Noweb",None,self.OnOutlineToNoweb),
	("&amp;Flatten Outline",None,self.OnFlattenOutline),
	("&amp;Remove Sentinels",None,self.OnRemoveSentinels),
	("&amp;Weave",None,self.OnWeave)]

self.createMenuEntries(exportMenu,table)
</t>
<t tx="T651">outlineMenu = self.createNewMenu("&amp;Outline")
&lt;&lt; create top-level outline menu &gt;&gt;
&lt;&lt; create expand/contract submenu &gt;&gt;
&lt;&lt; create move submenu &gt;&gt;
&lt;&lt; create mark submenu &gt;&gt;
&lt;&lt; create goto submenu &gt;&gt;</t>
<t tx="T652">table = (
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
<t tx="T653">expandMenu = self.createNewMenu("&amp;Expand/Contract...","Outline")

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
<t tx="T654">moveSelectMenu = self.createNewMenu("&amp;Move...","Outline")

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
<t tx="T655">markMenu = self.createNewMenu("M&amp;ark/Unmark...","Outline")

table = (
	("&amp;Mark","Ctrl-M",self.OnMark),
	("Mark &amp;Subheads","Alt+S",self.OnMarkSubheads),
	("Mark Changed &amp;Items","Alt+C",self.OnMarkChangedItems),
	("Mark Changed &amp;Roots","Alt+R",self.OnMarkChangedRoots),
	("Mark &amp;Clones","Alt+K",self.OnMarkClones),
	("&amp;Unmark All","Alt+U",self.OnUnmarkAll))
	
self.createMenuEntries(markMenu,table)
</t>
<t tx="T656">gotoMenu = self.createNewMenu("&amp;Go To...","Outline")

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
<t tx="T657">windowMenu = self.createNewMenu("&amp;Window")

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
<t tx="T658">helpMenu = self.createNewMenu("&amp;Help")

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
<t tx="T659">def createNewMenu(self,name):
	
	return wx.wxMenu()</t>
<t tx="T660">@ The old, non-user-configurable code bound shortcuts in createMenuBar.  The new user-configurable code binds shortcuts here.

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
<t tx="T661">def OnAbout (self,event=None):
	
	print "OnAbout" # ,event</t>
<t tx="T662">const_dict = {}
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
<t tx="T663"></t>
<t tx="T664">@ tnodeList must be converted from indices (in the .leo file) to tnodes while the .leo file is being read because tnode indices may change when derived files are written.</t>
<t tx="T665">def findChild (self,headline):
	
	"""Return the next tnode in the at.tnodeList."""

	at = self ; c = at.commands ; fc = c.fileCommands

	if at.importing:
		moveRight = c.currentVnode() == at.importRoot
		c.insertHeadline() # op_name="Insert Outline"
		if moveRight:
			c.moveOutlineRight()
		v = c.currentVnode()
		v.initHeadString(headline)
		t.setVisited() # Supress warning about unvisited node.
		return v.t

	if not hasattr(at.root,"tnodeList"):
		at.readError("no tnodeList for " + `at.root`)
		trace("no tnodeList for ",at.root)
		return None
		
	if at.tnodeListIndex &gt;= len(at.root.tnodeList):
		at.readError("bad tnodeList index: %d, %s" % (at.tnodeListIndex,`at.root`))
		trace("bad tnodeList index",at.tnodeListIndex,len(at.root.tnodeList),at.root)
		return None
		
	t = at.root.tnodeList[at.tnodeListIndex]
	assert(t)
	at.tnodeListIndex += 1

	# Check the headline.
	v = t.joinList[0]
	if headline.strip() == v.headString().strip():
		# trace(t)
		t.setVisited() # Supress warning about unvisited node.
		return t
	else:
		at.readError(
			"Mismatched headline.\nExpecting: %s\ngot: %s" %
			(headline,v.headString()))
		trace("Mismatched headline",headline,v.headString())
		trace(at.tnodeListIndex,len(at.root.tnodeList))
		return None
</t>
<t tx="T666">def putOpenNodeSentinel(self,v):
	
	"""Write @+node sentinel for v."""
	
	at = self

	if v.isAtFileNode() and v != at.root:
		at.writeError("@file not valid in: " + v.headString())
		return
	
	s = at.nodeSentinelText(v)
	at.putSentinel("@+node:" + s)

	# Append the n'th tnode to the root's tnode list.

	# trace("%3d %3d" % (len(at.root.tnodeList),v.t.fileIndex),v)
	at.root.tnodeList.append(v.t)</t>
<t tx="T667">def putTnodeList (self,v):
	
	"""Put the optional tnodeList attribute of a vnode."""

	fc = self
	if v.tnodeList:
		trace("%4d" % len(v.tnodeList),v)
		fc.put(" tnodeList=") ; fc.put_dquote()
		s = ','.join([str(t.fileIndex) for t in v.tnodeList])
		fc.put(s) ; fc.put_dquote()</t>
<t tx="T668">@nocolor

Transition:
	* Move myFileCommands class into LeoPy.leo
	*** Move myAtFile class into LeoPy.leo

Tests:
	- Test new read routines. All pass.
	- Test new write routines All pass.

Next:
	- Test @delims.
	- Test @raw, @endraw.
	- Test @file-nosent, etc.

- Read Me or suffer.
	- Must enable plugins, use_gnx plugin, and write_old_format_derived_files in leoConfig.txt.</t>
<t tx="T669">"""New code for 4.0"""

from leoPlugins import *
from leoGlobals import *

import leoApp,leoAtFile,leoColor,leoDialog,leoFileCommands,leoFrame,leoNodes
import filecmp,os,os.path,time

# Warning: this code is pre-alpha.  See todo list.t

if 1: # Register the handlers...

	@others
	
	registerHandler("create-optional-menus",onCreateExtraMenus)
	print "4.0 plugin"

	__version__ = "0.2"
	plugin_signon(__name__)</t>
<t tx="T670">def onCreateExtraMenus (tag,keywords):
	
	c = keywords.get("c")
	self = c.frame # This code should really be part of the leoFrame class.
	
	&lt;&lt; extend the read/write submenu &gt;&gt;
	&lt;&lt; extend the import submenu &gt;&gt;
</t>
<t tx="T671">table2 = (
	("-",None,None),
	("Write 4.x Derived Files",None,self.OnWriteNewDerivedFiles),
	("Write 3.x Derived Files",None,self.OnWriteOldDerivedFiles),
	("Write 3.x Outline",None,self.OnWriteOldOutline))

if 1: # pluging code.
	readWriteMenu = self.getMenu("ReadWrite")
	self.createMenuEntries (readWriteMenu,table2)
else: # native code.
	table.extend(table2)</t>
<t tx="T672">table2 = (
	("-",None,None),
	("Import 4.0 Derived File",None,self.OnImportDerivedFile))

if 1: # pluging code.
	importMenu = self.getMenu("Import")
	self.createMenuEntries(importMenu,table2)
else: # native code.
	table.extend(table2)</t>
<t tx="T673">class myFileCommands(leoFileCommands.baseFileCommands):
	@others

leoFileCommands.fileCommands = myFileCommands</t>
<t tx="T674">def __init__(self,theCommander):
	
	"""Ctor for myFileCommands class (gnx code)."""
	
	leoFileCommands.baseFileCommands.__init__(self,theCommander) # Initialize the base class.
	
	if 0: # gnx's not used
		self.a = app()
		self.nodeIndices = self.a.nodeIndices</t>
<t tx="T675">@ This writes full headline and body text for all vnodes, even orphan and @ignored nodes.  This allows all Leo outlines to be used as backup files.
@c

def putVnode (self,v,topVnode):

	fc = self ; c = fc.commands
	fc.put("&lt;v")
	&lt;&lt; Put tnode index if this vnode has body text &gt;&gt;
	&lt;&lt; Put attribute bits &gt;&gt;
	if hasattr(v,"tnodeList") and len(v.tnodeList) &gt; 0:
		fc.putTnodeList(v) # New in 4.0
	fc.put("&gt;")
	&lt;&lt; write the head text &gt;&gt;
	child = v.firstChild()
	if child:
		fc.put_nl()
		while child:
			fc.putVnode(child,topVnode)
			child = child.next()
	fc.put("&lt;/v&gt;") ; fc.put_nl()</t>
<t tx="T676">t = v.t
if t and (t.hasBody() or len(v.t.joinList) &gt; 0):
	if t.fileIndex &gt; 0:
		fc.put(" t=") ; fc.put_in_dquotes("T" + `t.fileIndex`)
		v.t.setVisited() # Indicate we wrote the body text.
	else:
		es("error writing file(bad vnode)!")
		es("try using the Save To command")</t>
<t tx="T677">current = c.currentVnode()
top = topVnode
if ( v.isCloned() or v.isExpanded() or v.isMarked() or
	v == current or v == top ):
	fc.put(" a=") ; fc.put_dquote()
	if v.isCloned(): fc.put("C")
	if v.isExpanded(): fc.put("E")
	if v.isMarked(): fc.put("M")
	if v.isOrphan(): fc.put("O")
	if v == top: fc.put("T")
	if v == current: fc.put("V")
	fc.put_dquote()</t>
<t tx="T678">headString = v.headString()
if len(headString) &gt; 0:
	fc.put("&lt;vh&gt;")
	fc.putEscapedString(headString)
	fc.put("&lt;/vh&gt;")</t>
<t tx="T679">def writeAtFileNodes (self):
	
	c = self.commands

	c.atFileCommands.writeAll(writeAtFileNodesFlag=true)
	
	if not app().config.write_old_format_derived_files:
		es("auto-saving outline",color="blue")
		c.frame.OnSave() # Must be done to preserve tnodeList.</t>
<t tx="T680">class topLevelDerivedFile(leoAtFile.baseAtFile):
	@others

leoAtFile.atFile = topLevelDerivedFile

atFile = topLevelDerivedFile</t>
<t tx="T681">def __init__(self,theCommander): 

	# trace("topLevelDerivedFile.__init__")
	
	at = self
	at.commands = theCommander
	at.fileCommands = self.commands.fileCommands
	
	# Create subcommanders to handler old and new format derived files.
	at.old_df = oldDerivedFile(theCommander)
	at.new_df = newDerivedFile(theCommander)
	
	# Set by scanDefaultDirectory.
	at.default_directory = None
	at.errors = 0

	# Set by scanHeader when reading. Set by scanAllDirectives...
	at.encoding = None
	at.endSentinelComment = None
	at.startSentinelComment = None</t>
<t tx="T682"></t>
<t tx="T683">def readAll(self,root,partialFlag=false):
	
	"""Scan vnodes, looking for @file nodes to read."""

	at = self ; c = at.commands
	c.endEditing() # Capture the current headline.
	anyRead = false
	at.initIvars()
	v = root
	if partialFlag: after = v.nodeAfterTree()
	else: after = None
	while v and v != after:
		if v.isAtIgnoreNode():
			v = v.nodeAfterTree()
		elif v.isAtFileNode() or v.isAtRawFileNode():
			anyRead = true
			if partialFlag:
				# We are forcing the read.
				at.read(v)
			else:
				# if v is an orphan, we don't expect to see a derived file,
				# and we shall read a derived file if it exists.
				wasOrphan = v.isOrphan()
				ok = at.read(v)
				if wasOrphan and not ok:
					# Remind the user to fix the problem.
					v.setDirty()
					c.setChanged(true)
			v = v.nodeAfterTree()
		else: v = v.threadNext()
	# Clear all orphan bits.
	v = root
	while v:
		v.clearOrphan()
		v = v.threadNext()
		
	if partialFlag and not anyRead:
		es("no @file nodes in the selected tree")</t>
<t tx="T684">def error(self,message):

	es(message,color="red")
	print message
	self.errors += 1</t>
<t tx="T685"># The caller has enclosed this code in beginUpdate/endUpdate.

def read(self,root,importFileName=None):
	
	"""Common read logic for any derived file."""
	
	at = self ; c = at.commands
	at.errors = 0
	at.scanDefaultDirectory(root)
	if at.errors: return
	&lt;&lt; set fileName from root and importFileName &gt;&gt;
	&lt;&lt; open file or return false &gt;&gt;
	es("reading: " + root.headString())
	firstLines,read_new = at.scanHeader(file,fileName)
	df = choose(read_new,at.new_df,at.old_df)
	&lt;&lt; copy ivars to df &gt;&gt;
	root.clearVisitedInTree()
	df.readOpenFile(root,file,fileName,firstLines)
	file.close()
	after = root.nodeAfterTree()
	&lt;&lt; warn about non-empty unvisited nodes &gt;&gt;
	if df.errors == 0:
		if not df.importing:
			&lt;&lt; copy all tempBodyStrings to tnodes &gt;&gt;
	&lt;&lt; delete all tempBodyStrings &gt;&gt;
	root.clearDirty()
	return df.errors == 0</t>
<t tx="T686">if importFileName:
	fileName = importFileName
elif root.isAtFileNode():
	fileName = root.atFileNodeName()
else:
	fileName = root.atRawFileNodeName()
	
if not fileName:
	at.error("Missing file name.  Restoring @file tree from .leo file.")
	return false</t>
<t tx="T687">fn = os.path.join(at.default_directory,fileName)
fn = os.path.normpath(fn)
fn = toUnicode(fn,"ascii")

try:
	file = open(fn,'r')
	if file:
		&lt;&lt; warn on read-only file &gt;&gt;
	else: return false
except:
	at.error("Can not open: " + '"@file ' + fn + '"')
	return false</t>
<t tx="T688">try:
	read_only = not os.access(fn,os.W_OK)
	if read_only:
		es("read only: " + fn,color="red")
except:
	pass # os.access() may not exist on all platforms.</t>
<t tx="T689">if importFileName:
	df.importing = true
	df.importRoot = c.currentVnode()
	
else:
	df.importing = false
	df.importRoot = None

# Set by scanHeader.
df.encoding = at.encoding
df.endSentinelComment = at.endSentinelComment
df.startSentinelComment = at.startSentinelComment

# Set other common ivars.
df.errors = 0
df.file = file
df.targetFileName = fileName
df.indent = 0
df.raw = false
df.root = root
df.root_seen = false
</t>
<t tx="T690">v = root
while v and v != after:
	try: s = v.t.tempBodyString
	except: s = ""
	if s and not v.t.isVisited():
		at.error("Not in derived file:" + v.headString())
		v.t.setVisited() # One message is enough.
	v = v.threadNext()</t>
<t tx="T691">v = root
while v and v != after:
	try: s = v.t.tempBodyString
	except: s = ""
	if s != v.bodyString():
		es("changed: " + v.headString(),color="blue")
		if 0: # For debugging.
			print ; print "changed: " + v.headString()
			print ; print "new:",`s`
			print ; print "old:",`v.bodyString()`
		v.setBodyStringOrPane(s)
		v.setDirty()
	v = v.threadNext()</t>
<t tx="T692">v = root
while v and v != after:
	if hasattr(v.t,"tempBodyString"):
		delattr(v.t,"tempBodyString")
	v = v.threadNext()</t>
<t tx="T693">def scanDefaultDirectory(self,v):
	
	"""Set default_directory ivar by looking for @path directives."""

	at = self ; c = at.commands
	at.default_directory = None
	&lt;&lt; Set path from @file node &gt;&gt;
	if at.default_directory:
		return

	while v:
		s = v.t.bodyString
		dict = get_directives_dict(s)
		if dict.has_key("path"):
			&lt;&lt; handle @path &gt;&gt;
			return
		v = v.parent()

	&lt;&lt; Set current directory &gt;&gt;
	if not at.default_directory:
		# This should never happen: c.openDirectory should be a good last resort.
		at.error("No absolute directory specified anywhere.")
		at.default_directory = ""</t>
<t tx="T694"># An absolute path in an @file node over-rides everything else.
# A relative path gets appended to the relative path by the open logic.

# Bug fix: 10/16/02
if v.isAtFileNode():
	name = v.atFileNodeName()
elif v.isAtRawFileNode():
	name = v.atRawFileNodeName()
elif v.isAtNoSentinelsFileNode():
	name = v.atNoSentinelsFileNodeName()
else:
	name = ""

dir = choose(name,os.path.dirname(name),None)
if dir and os.path.isabs(dir):
	if os.path.exists(dir):
		at.default_directory = dir
	else:
		at.default_directory = makeAllNonExistentDirectories(dir)
		if not at.default_directory:
			at.error("Directory \"" + dir + "\" does not exist")</t>
<t tx="T695"># We set the current director to a path so future writes will go to that directory.

k = dict["path"]
&lt;&lt; compute relative path from s[k:] &gt;&gt;

if path and len(path) &gt; 0:
	base = getBaseDirectory() # returns "" on error.
	path = os.path.join(base,path)
	if os.path.isabs(path):
		&lt;&lt; handle absolute path &gt;&gt;
	else:
		at.error("ignoring bad @path: " + path)
else:
	at.error("ignoring empty @path")</t>
<t tx="T696">j = i = k + len("@path")
i = skip_to_end_of_line(s,i)
path = string.strip(s[j:i])

# Remove leading and trailing delims if they exist.
if len(path) &gt; 2 and (
	(path[0]=='&lt;' and path[-1] == '&gt;') or
	(path[0]=='"' and path[-1] == '"') ):
	path = path[1:-1]

path = path.strip()</t>
<t tx="T697"># path is an absolute path.

if os.path.exists(path):
	at.default_directory = path
else:
	at.default_directory = makeAllNonExistentDirectories(path)
	if not at.default_directory:
		at.error("invalid @path: " + path)</t>
<t tx="T698"># This code is executed if no valid absolute path was specified in the @file node or in an @path directive.

assert(not at.default_directory)

if c.frame :
	base = getBaseDirectory() # returns "" on error.
	for dir in (c.tangle_directory,c.frame.openDirectory,c.openDirectory):
		if dir and len(dir) &gt; 0:
			dir = os.path.join(base,dir)
			if os.path.isabs(dir): # Errors may result in relative or invalid path.
				if os.path.exists(dir):
					at.default_directory = dir ; break
				else:
					at.default_directory = makeAllNonExistentDirectories(dir)</t>
<t tx="T699">def scanHeader(self,file,fileName):
	
	"""Scan the @+leo sentinel.
	
	Sets self.encoding, and self.start/endSentinelComment.
	
	Returns (firstLines,new_df) where:
	firstLines contains all @first lines,
	new_df is true if we are reading a new-format derived file."""
	
	at = self
	new_df = false # Set default.
	firstLines = [] # The lines before @+leo.
	version_tag = "-ver=" ; gnx_tag = "-gnx="
	tag = "@+leo" ; encoding_tag = "-encoding="
	valid = true
	&lt;&lt; skip any non @+leo lines &gt;&gt;
	&lt;&lt; make sure we have @+leo &gt;&gt;
	&lt;&lt; read optional version param &gt;&gt;
	&lt;&lt; read optional encoding param &gt;&gt;
	&lt;&lt; set the closing comment delim &gt;&gt;
	if not valid:
		at.error("Bad @+leo sentinel in " + fileName)
	return firstLines, new_df</t>
<t tx="T700">@ Queue up the lines before the @+leo.  These will be used to add as parameters to the @first directives, if any.  Empty lines are ignored (because empty @first directives are ignored). NOTE: the function now returns a list of the lines before @+leo.

We can not call sentinelKind here because that depends on the comment delimiters we set here.  @first lines are written "verbatim", so nothing more needs to be done!
@c

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
<t tx="T701">@ REM hack: leading whitespace is significant before the @+leo.  We do this so that sentinelKind need not skip whitespace following self.startSentinelComment.  This is correct: we want to be as restrictive as possible about what is recognized as a sentinel.  This minimizes false matches.
@c

if 0:# 7/8/02: make leading whitespace significant.
	i = skip_ws(s,i)

if match(s,i,tag):
	i += len(tag)
else: valid = false</t>
<t tx="T702">new_df = match(s,i,version_tag)

if new_df:
	# Skip to the next minus sign or end-of-line
	i += len(version_tag)
	j = i
	while i &lt; len(s) and not is_nl(s,i) and s[i] != '-':
		i += 1

	if j &lt; i:
		version = s[j:i]
	else:
		valid = false
</t>
<t tx="T703"># Set the default encoding
at.encoding = app().config.default_derived_file_encoding

if match(s,i,encoding_tag):
	# Read optional encoding param, e.g., -encoding=utf-8,
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
			print "bad encoding in derived file:",encoding
			es("bad encoding in derived file:",encoding)
	else:
		valid = false
</t>
<t tx="T704"># The closing comment delim is the trailing non-whitespace.
i = j = skip_ws(s,i)
while i &lt; n and not is_ws(s[i]) and not is_nl(s,i):
	i += 1
at.endSentinelComment = s[j:i]</t>
<t tx="T705"></t>
<t tx="T706">def writeAll(self,writeAtFileNodesFlag=false,writeDirtyAtFileNodesFlag=false):
	
	"""Write @file nodes in all or part of the outline"""

	at = self ; c = at.commands
	write_new = not app().config.write_old_format_derived_files
	df = choose(write_new,at.new_df,at.old_df)
	df.initIvars()
	writtenFiles = [] # Files that might be written again.

	if writeAtFileNodesFlag:
		# Write all nodes in the selected tree.
		v = c.currentVnode()
		after = v.nodeAfterTree()
	else:
		# Write dirty nodes in the entire outline.
		v = c.rootVnode()
		after = None

	&lt;&lt; Clear all orphan bits &gt;&gt;
	while v and v != after:
		# trace(`v`)
		if v.isAnyAtFileNode() or v.isAtIgnoreNode():
			&lt;&lt; handle v's tree &gt;&gt;
			v = v.nodeAfterTree()
		else:
			v = v.threadNext()

	&lt;&lt; say the command is finished &gt;&gt;</t>
<t tx="T707">@ We must clear these bits because they may have been set on a previous write.  Calls to atFile::write may set the orphan bits in @file nodes.  If so, write_LEO_file will write the entire @file tree.
@c

v2 = v
while v2 and v2 != after:
	v2.clearOrphan()
	v2 = v2.threadNext()</t>
<t tx="T708"># This code is a little tricky: @ignore not recognised in @silentfile nodes.

if v.isDirty() or writeAtFileNodesFlag or v.t in writtenFiles:

	if v.isAtSilentFileNode():
		at.silentWrite(v)
	elif v.isAtIgnoreNode():
		pass
	elif v.isAtRawFileNode():
		at.rawWrite(v)
	elif v.isAtNoSentinelsFileNode():
		at.write(v,nosentinels=true)
	elif v.isAtFileNode():
		at.write(v)

	if not v.isAtIgnoreNode():
		writtenFiles.append(v.t)</t>
<t tx="T709">if writeAtFileNodesFlag or writeDirtyAtFileNodesFlag:
	if len(writtenFiles) &gt; 0:
		es("finished")
	elif writeAtFileNodesFlag:
		es("no @file nodes in the selected tree")
	else:
		es("no dirty @file nodes")</t>
<t tx="T710">def rawWrite (self,v):
	
	at = self
	write_new = not app().config.write_old_format_derived_files
	df = choose(write_new,at.new_df,at.old_df)
	df.rawWrite(v)
	
def silentWrite (self,v):

	self.old_df.silentWrite(v) # No new_df.silentWrite method.
	
def write (self,v,nosentinels=false):
	
	at = self
	write_new = not app().config.write_old_format_derived_files
	df = choose(write_new,at.new_df,at.old_df)
	df.write(v,nosentinels)
	
</t>
<t tx="T711">def writeOldDerivedFiles (self,v):
	
	self.writeDerivedFiles(v,write_old=true)

def writeNewDerivedFiles (self,v,nosentinels=false):

	self.writeDerivedFiles(v,write_old=false)
	
def writeDerivedFiles (self,v,write_old):
	
	a = app() ; config = a.config
	old = config.write_old_format_derived_files
	config.write_old_format_derived_files = write_old
	self.writeAll(writeAtFileNodesFlag=true)
	config.write_old_format_derived_files = old</t>
<t tx="T712">def writeMissing(self,v):
	
	trace("old_df",v)

	at = self
	write_new = not app().config.write_old_format_derived_files
	df = choose(write_new,at.new_df,at.old_df)
	df.initIvars()
	writtenFiles = false
	after = v.nodeAfterTree()
	while v and v != after:
		if v.isAtSilentFileNode() or (v.isAnyAtFileNode() and not v.isAtIgnoreNode()):
			missing = false ; valid = true
			df.targetFileName = v.anyAtFileNodeName()
			&lt;&lt; set missing if the file does not exist &gt;&gt;
			if valid and missing:
				&lt;&lt; create df.outputFile &gt;&gt;
				if at.outputFile:
					&lt;&lt; write the @file node &gt;&gt;
			v = v.nodeAfterTree()
		elif v.isAtIgnoreNode():
			v = v.nodeAfterTree()
		else:
			v = v.threadNext()
	
	if writtenFiles &gt; 0:
		es("finished")
	else:
		es("no missing @file node in the selected tree")</t>
<t tx="T713"># This is similar, but not the same as, the logic in openWriteFile.

valid = df.targetFileName and len(df.targetFileName) &gt; 0

if valid:
	try:
		# Creates missing directives if option is enabled.
		df.scanAllDirectives(v)
		valid = df.errors == 0
	except:
		es("exception in atFile.scanAllDirectives")
		es_exception()
		valid = false

if valid:
	try:
		fn = df.targetFileName
		df.shortFileName = fn # name to use in status messages.
		df.targetFileName = os.path.join(df.default_directory,fn)
		df.targetFileName = os.path.normpath(df.targetFileName)
		path = df.targetFileName # Look for the full name, not just the directory.
		valid = path and len(path) &gt; 0
		if valid:
			missing = not os.path.exists(path)
	except:
		es("exception creating path:" + fn)
		es_exception()
		valid = false</t>
<t tx="T714">try:
	df.outputFileName = df.targetFileName + ".leotmp"
	df.outputFile = open(df.outputFileName,'wb')
	if df.outputFile == None:
		es("can not open " + df.outputFileName)
except:
	es("exception opening:" + df.outputFileName)
	es_exception()
	df.outputFile = None
</t>
<t tx="T715">if v.isAtSilentFileNode():
	at.silentWrite(v)
elif v.isAtRawFileNode():
	at.rawWrite(v)
elif v.isAtNoSentinelsFileNode():
	at.write(v,nosentinels=true)
elif v.isAtFileNode():
	at.write(v)
else: assert(0)

writtenFiles = true
</t>
<t tx="T716">class baseOldDerivedFile:
	
	&lt;&lt; atFile constants &gt;&gt;
	
	"""A class to read and write 3.x derived files."""

	@others
	
class oldDerivedFile(baseOldDerivedFile):
	pass</t>
<t tx="T717"># The kind of at_directives.
noDirective		   =  1 # not an at-directive.
delimsDirective =  2 # @delims (not used!)
docDirective	   =  3 # @doc.
atDirective		   =  4 # @&lt;space&gt; or @&lt;newline&gt;
codeDirective	  =  5 # @code
cDirective		    =  6 # @c&lt;space&gt; or @c&lt;newline&gt;
othersDirective	=  7 # at-others
miscDirective	  =  8 # All other directives
rawDirective    =  9 # @raw
endRawDirective = 10 # @end_raw

# The kind of sentinel line.
noSentinel		 = 20 # Not a sentinel
# not used   = 21
endAt			 = 22 # @-at
endBody			 = 23 # @-body
endDoc			 = 24 # @-doc
endLeo			 = 25 # @-leo
endNode			 = 26 # @-node
endOthers		  = 27 # @-others

# not used     = 40
startAt			   = 41 # @+at
startBody		    = 42 # @+body
startDoc		     = 43 # @+doc
startLeo		     = 44 # @+leo
startNode		    = 45 # @+node
startOthers		  = 46 # @+others

startComment   = 60 # @comment
startDelims		  = 61 # @delims
startDirective	= 62 # @@
startRef		     = 63 # @&lt; &lt; ... &gt; &gt; (3.0)
startVerbatim	 = 64 # @verbatim
startVerbatimAfterRef = 65 # @verbatimAfterRef (3.0)

# New in 4.0...
startAfterRef  = 70 # @afterref (4.0)
startNl        = 71 # @nl (4.0)
startNonl      = 72 # @nonl (4.0)
</t>
<t tx="T718">def __init__(self,theCommander): 

	# trace("oldDerivedFile.__init__")

	self.commands = theCommander # The commander for the current window.
	self.fileCommands = self.commands.fileCommands

	self.initIvars()

def initIvars(self):

	&lt;&lt; init atFile ivars &gt;&gt;
</t>
<t tx="T719"># errors is the number of errors seen while reading and writing.
self.errors = 0

# Initialized by atFile.scanAllDirectives.
self.default_directory = None
self.page_width = None
self.tab_width  = None
self.startSentinelComment = None
self.endSentinelComment = None
self.language = None

@ The files used by the output routines.  When tangling, we first write to a temporary output file.  After tangling is temporary file.  Otherwise we delete the old target file and rename the temporary file to be the target file.
@c
self.shortFileName = "" # short version of file name used for messages.
self.targetFileName = u"" # EKR 1/21/03: now a unicode string
self.outputFileName = u"" # EKR 1/21/03: now a unicode string
self.outputFile = None # The temporary output file.

@ The indentation used when outputting section references or at-others sections.  We add the indentation of the line containing the at-node directive and restore the old value when the
expansion is complete.
@c
self.indent = 0  # The unit of indentation is spaces, not tabs.

# The root of tree being written.
self.root = None

# Ivars used to suppress newlines between sentinels.
self.suppress_newlines = true # true: enable suppression of newlines.
self.newline_pending = false # true: newline is pending on read or write.

# Support of output_newline option
self.output_newline = getOutputNewline()

# Support of @raw
self.raw = false # true: in @raw mode
self.sentinels = true # true: output sentinels while expanding refs.

# Enables tracing (debugging only).
self.trace = false

# The encoding used to convert from unicode to a byte stream.
self.encoding = app().config.default_derived_file_encoding

# For interface between 3.x and 4.x read code.
self.file = None
self.importing = false
self.importRoot = None</t>
<t tx="T720"></t>
<t tx="T721">def readOpenFile(self,root,file,fileName,firstLines):
	
	"""Read an open 3.x derived file."""
	
	trace("old_df",root)

	at = self ; c = at.commands

	# Scan the file buffer
	at.scanAllDirectives(root)
	lastLines = at.scanText(file,root,[],at.endLeo)
	root.t.setVisited() # Disable warning about set nodes.

	# Handle first and last lines.
	try: body = root.t.tempBodyString
	except: body = ""
	lines = body.split('\n')
	at.completeFirstDirectives(lines,firstLines)
	at.completeLastDirectives(lines,lastLines)
	s = '\n'.join(lines).replace('\r', '')
	## root.t.setTnodeText(s)
	root.t.tempBodyString = s</t>
<t tx="T722"># 14-SEP-2002 DTHEIN: added for use by atFile.read()

# this function scans the lines in the list 'out' for @first directives
# and appends the corresponding line from 'firstLines' to each @first 
# directive found.  NOTE: the @first directives must be the very first
# lines in 'out'.
def completeFirstDirectives(self,out,firstLines):

	tag = "@first"
	foundAtFirstYet = 0
	outRange = range(len(out))
	j = 0
	for k in outRange:
		# skip leading whitespace lines
		if (not foundAtFirstYet) and (len(out[k].strip()) == 0): continue
		# quit if something other than @first directive
		i = 0
		if not match(out[k],i,tag): break;
		foundAtFirstYet = 1
		# quit if no leading lines to apply
		if j &gt;= len(firstLines): break
		# make the new @first directive
		#18-SEP-2002 DTHEIN: remove trailing newlines because they are inserted later
		# 21-SEP-2002 DTHEIN: no trailing whitespace on empty @first directive
		leadingLine = " " + firstLines[j]
		out[k] = tag + leadingLine.rstrip() ; j += 1
</t>
<t tx="T723"># 14-SEP-2002 DTHEIN: added for use by atFile.read()

# this function scans the lines in the list 'out' for @last directives
# and appends the corresponding line from 'lastLines' to each @last 
# directive found.  NOTE: the @last directives must be the very last
# lines in 'out'.
def completeLastDirectives(self,out,lastLines):

	tag = "@last"
	foundAtLastYet = 0
	outRange = range(-1,-len(out),-1)
	j = -1
	for k in outRange:
		# skip trailing whitespace lines
		if (not foundAtLastYet) and (len(out[k].strip()) == 0): continue
		# quit if something other than @last directive
		i = 0
		if not match(out[k],i,tag): break;
		foundAtLastYet = 1
		# quit if no trailing lines to apply
		if j &lt; -len(lastLines): break
		# make the new @last directive
		#18-SEP-2002 DTHEIN: remove trailing newlines because they are inserted later
		# 21-SEP-2002 DTHEIN: no trailing whitespace on empty @last directive
		trailingLine = " " + lastLines[j]
		out[k] = tag + trailingLine.rstrip() ; j -= 1
</t>
<t tx="T724">@ Sections appear in the derived file in reference order, not tree order.  Therefore, when we insert the nth child of the parent there is no guarantee that the previous n-1 children have already been inserted. And it won't work just to insert the nth child as the last child if there aren't n-1 previous siblings.  For example, if we insert the third child followed by the second child followed by the first child the second and third children will be out of order.

To ensure that nodes are placed in the correct location we create "dummy" children as needed as placeholders.  In the example above, we would insert two dummy children when inserting the third child.  When inserting the other two children we replace the previously inserted dummy child with the actual children.

vnode child indices are zero-based.  Here we use 1-based indices.

With the "mirroring" scheme it is a structure error if we ever have to create dummy vnodes.  Such structure errors cause a second pass to be made, with an empty root.  This second pass will generate other structure errors, which are ignored.
@c
def createNthChild(self,n,parent,headline):

	assert(n &gt; 0)

	# Create any needed dummy children.
	dummies = n - parent.numberOfChildren() - 1
	if dummies &gt; 0:
		if 0: # CVS produces to many errors for this to be useful.
			es("dummy created")
		self.errors += 1
	while dummies &gt; 0:
		dummies -= 1
		dummy = parent.insertAsLastChild(leoNodes.tnode())
		# The user should never see this headline.
		dummy.initHeadString("Dummy")

	if n &lt;= parent.numberOfChildren():
		&lt;&lt; check the headlines &gt;&gt;
	else:
		# This is using a dummy; we should already have bumped errors.
		result = parent.insertAsLastChild(leoNodes.tnode())
	result.initHeadString(headline)
	
	result.setVisited() # Suppress all other errors for this node.
	result.t.setVisited() # Suppress warnings about unvisited nodes.
	return result</t>
<t tx="T725"># 1/24/03: A kludgy fix to the problem of headlines containing comment delims.

result = parent.nthChild(n-1)
resulthead = result.headString()

if headline.strip() != resulthead.strip():
	start = self.startSentinelComment
	end = self.endSentinelComment
	if end and len(end) &gt; 0:
		# 1/25/03: The kludgy fix.
		# Compare the headlines without the delims.
		h1 =   headline.replace(start,"").replace(end,"")
		h2 = resulthead.replace(start,"").replace(end,"")
		if h1.strip() == h2.strip():
			# 1/25/03: Another kludge: use the headline from the outline, not the derived file.
			headline = resulthead
		else:
			self.errors += 1
	else:
		self.errors += 1
</t>
<t tx="T726">def handleLinesFollowingSentinel (self,lines,sentinel,comments = true):
	
	"""convert lines following a sentinel to a single line"""
	
	m = " following" + sentinel + " sentinel"
	start = self.startSentinelComment
	end   = self.endSentinelComment
	
	if len(lines) == 1: # The expected case.
		s = lines[0]
	elif len(lines) == 5:
		self.readError("potential cvs conflict" + m)
		s = lines[1]
		es("using " + s)
	else:
		self.readError("unexpected lines" + m)
		es(len(lines), " lines" + m)
		s = "bad " + sentinel
		if comments: s = start + ' ' + s

	if comments:
		&lt;&lt; remove the comment delims from s &gt;&gt;
		
	# Undo the cweb hack: undouble @ signs if the opening comment delim ends in '@'.
	if start[-1:] == '@':
		s = s.replace('@@','@')

	return s</t>
<t tx="T727"># Remove the starting comment and the blank.
# 5/1/03: The starting comment now looks like a sentinel, to warn users from changing it.
comment = start + '@ '
if match(s,0,comment):
	s = s[len(comment):]
else:
	self.readError("expecting comment" + m)

# Remove the trailing comment.
if len(end) == 0:
	s = string.strip(s[:-1])
else:
	k = s.rfind(end)
	s = string.strip(s[:k]) # works even if k == -1</t>
<t tx="T728">def readLine (self,file):
	"""Reads one line from file using the present encoding"""
	
	s = readlineForceUnixNewline(file)
	u = toUnicode(s,self.encoding)
	return u

</t>
<t tx="T729"># We expect only a single line, and more may exist if cvs detects a conflict.
# We accept the first line even if it looks like a sentinel.
# 5/1/03: The starting comment now looks like a sentinel, to warn users from changing it.

def readLinesToNextSentinel (self,file):
	
	"""	read lines following multiline sentinels"""
	
	lines = []
	start = self.startSentinelComment + '@ '
	nextLine = self.readLine(file)
	while nextLine and len(nextLine) &gt; 0:
		if len(lines) == 0:
			lines.append(nextLine)
			nextLine = self.readLine(file)
		else:
			# 5/1/03: looser test then calling sentinelKind.
			s = nextLine ; i = skip_ws(s,0)
			if match(s,i,start):
				lines.append(nextLine)
				nextLine = self.readLine(file)
			else: break

	return nextLine,lines</t>
<t tx="T730"># Scans the doc part and appends the text out.
# s,i point to the present line on entry.

def scanDoc(self,file,s,i,out,kind):

	endKind = choose(kind == atFile.startDoc, atFile.endDoc, atFile.endAt)
	single = len(self.endSentinelComment) == 0
	&lt;&lt; Skip the opening sentinel &gt;&gt;
	&lt;&lt; Skip an opening block delim &gt;&gt;
	nextLine = None ; kind = atFile.noSentinel
	while len(s) &gt; 0:
		&lt;&lt; set kind, nextLine &gt;&gt;
		if kind == endKind: break
		&lt;&lt; Skip the leading stuff &gt;&gt;
		&lt;&lt; Append s to out &gt;&gt;
		if nextLine:
			s = nextLine ; nextLine = None
		else: s = self.readLine(file)
	if kind != endKind:
		self.readError("Missing " + self.sentinelName(endKind) + " sentinel")
	&lt;&lt; Remove a closing block delim from out &gt;&gt;</t>
<t tx="T731">assert(match(s,i,choose(kind == atFile.startDoc, "+doc", "+at")))

out.append(choose(kind == atFile.startDoc, "@doc", "@"))
s = self.readLine(file)
</t>
<t tx="T732">if not single:
	j = skip_ws(s,0)
	if match(s,j,self.startSentinelComment):
		s = self.readLine(file)</t>
<t tx="T733">@ For non-sentinel lines we look ahead to see whether the next line is a sentinel.
@c

assert(nextLine==None)

kind = self.sentinelKind(s)

if kind == atFile.noSentinel:
	j = skip_ws(s,0)
	blankLine = s[j] == '\n'
	nextLine = self.readLine(file)
	nextKind = self.sentinelKind(nextLine)
	if blankLine and nextKind == endKind:
		kind = endKind # stop the scan now
</t>
<t tx="T734"># Point i to the start of the real line.

if single: # Skip the opening comment delim and a blank.
	i = skip_ws(s,0)
	if match(s,i,self.startSentinelComment):
		i += len(self.startSentinelComment)
		if match(s,i," "): i += 1
else:
	i = self.skipIndent(s,0, self.indent)
</t>
<t tx="T735"># Append the line with a newline if it is real

line = s[i:-1] # remove newline for rstrip.

if line == line.rstrip():
	# no trailing whitespace: the newline is real.
	out.append(line + '\n')
else:
	# trailing whitespace: the newline is not real.
	out.append(line)
</t>
<t tx="T736"># This code will typically only be executed for HTML files.

if not single:

	delim = self.endSentinelComment
	n = len(delim)
	
	# Remove delim and possible a leading newline.
	s = string.join(out,"")
	s = s.rstrip()
	if s[-n:] == delim:
		s = s[:-n]
	if s[-1] == '\n':
		s = s[:-1]
		
	# Rewrite out in place.
	del out[:]
	out.append(s)
</t>
<t tx="T737">@ This method is the read code.

scanText reads lines from the file until the given ending sentinel is found, and warns if any other ending sentinel is found instead.  It calls itself recursively to handle most nested sentinels.

@c
def scanText (self,file,v,out,endSentinelKind,nextLine=None):

	a = app() ; c = self.commands ; config = a.config
	lastLines = [] # The lines after @-leo
	lineIndent = 0 ; linep = 0 # Changed only for sentinels.
	while 1:
		&lt;&lt; put the next line into s &gt;&gt;
		&lt;&lt; set kind, nextKind &gt;&gt;
		if kind != atFile.noSentinel:
			&lt;&lt; set lineIndent, linep and leading_ws &gt;&gt;
			i = self.skipSentinelStart(s,0)
		&lt;&lt; handle the line in s &gt;&gt;
	&lt;&lt; handle unexpected end of text &gt;&gt;
	assert(len(s)==0 and nextLine==None) # We get here only if readline fails.
	return lastLines # We get here only if there are problems.</t>
<t tx="T738">if nextLine:
	s = nextLine ; nextLine = None
else:
	s = self.readLine(file)
	if len(s) == 0: break

# trace(`s`)</t>
<t tx="T739">@ For non-sentinel lines we look ahead to see whether the next line is a sentinel.  If so, the newline that ends a non-sentinel line belongs to the next sentinel.
@c

assert(nextLine==None)

kind = self.sentinelKind(s)

if kind == atFile.noSentinel:
	nextLine = self.readLine(file)
	nextKind = self.sentinelKind(nextLine)
else:
	nextLine = nextKind = None

# nextLine != None only if we have a non-sentinel line.
# Therefore, nextLine == None whenever scanText returns.</t>
<t tx="T740">@ lineIndent is the total indentation on a sentinel line.  The first "self.indent" portion of that must be removed when recreating text.  leading_ws is the remainder of the leading whitespace.  linep points to the first "real" character of a line, the character following the "indent" whitespace.
@c

# Point linep past the first self.indent whitespace characters.
if self.raw: # 10/15/02
	linep =0
else:
	linep = self.skipIndent(s,0,self.indent)

# Set lineIndent to the total indentation on the line.
lineIndent = 0 ; i = 0
while i &lt; len(s):
	if s[i] == '\t': lineIndent += (abs(self.tab_width) - (lineIndent % abs(self.tab_width)))
	elif s[i] == ' ': lineIndent += 1
	else: break
	i += 1
# trace("lineIndent:" +`lineIndent` + ", " + `s`)

# Set leading_ws to the additional indentation on the line.
leading_ws = s[linep:i]</t>
<t tx="T741"># Issue the error.
name = self.sentinelName(endSentinelKind)
self.readError("Unexpected end of file. Expecting " + name + "sentinel" )
</t>
<t tx="T742">if kind == atFile.noSentinel:
	&lt;&lt; append non-sentinel line &gt;&gt;
&lt;&lt; handle common sentinels &gt;&gt;
&lt;&lt; handle rare sentinels &gt;&gt;
else:
	&lt;&lt; warn about unknown sentinel &gt;&gt;</t>
<t tx="T743"># We don't output the trailing newline if the next line is a sentinel.
if self.raw: # 10/15/02
	i = 0
else:
	i = self.skipIndent(s,0,self.indent)

assert(nextLine != None)

if nextKind == atFile.noSentinel:
	line = s[i:]
	out.append(line)
else:
	line = s[i:-1] # don't output the newline
	out.append(line)
</t>
<t tx="T744">elif kind in (
	atFile.endAt,  atFile.endBody, atFile.endDoc,
	atFile.endLeo, atFile.endNode, atFile.endOthers):
		&lt;&lt; handle an ending sentinel &gt;&gt;
elif kind == atFile.startBody:
	&lt;&lt; scan @+body &gt;&gt;
elif kind == atFile.startNode:
	&lt;&lt; scan @+node &gt;&gt;
elif kind == atFile.startRef:
	&lt;&lt; scan old ref &gt;&gt;
elif kind == atFile.startAt:
	&lt;&lt; scan @+at &gt;&gt;
elif kind == atFile.startDoc:
	&lt;&lt; scan @+doc &gt;&gt;
elif kind == atFile.startOthers:
	&lt;&lt; scan @+others &gt;&gt;</t>
<t tx="T745"># trace("end sentinel:", self.sentinelName(kind))

if kind == endSentinelKind:
	if kind == atFile.endLeo:
		# Ignore everything after @-leo.
		# Such lines were presumably written by @last.
		while 1:
			s = self.readLine(file)
			if len(s) == 0: break
			lastLines.append(s) # Capture all trailing lines, even if empty.
	elif kind == atFile.endBody:
		self.raw = false
	# nextLine != None only if we have a non-sentinel line.
	# Therefore, nextLine == None whenever scanText returns.
	assert(nextLine==None)
	return lastLines # End the call to scanText.
else:
	# Tell of the structure error.
	name = self.sentinelName(kind)
	expect = self.sentinelName(endSentinelKind)
	self.readError("Ignoring " + name + " sentinel.  Expecting " + expect)</t>
<t tx="T746">@ The sentinel contains an @ followed by a section name in angle brackets.  This code is different from the code for the @@ sentinel: the expansion of the reference does not include a trailing newline.
@c

assert(match(s,i,"&lt;&lt;"))

if len(self.endSentinelComment) == 0:
	line = s[i:-1] # No trailing newline
else:
	k = s.find(self.endSentinelComment,i)
	line = s[i:k] # No trailing newline, whatever k is.
		
# 10/30/02: undo cweb hack here
start = self.startSentinelComment
if start and len(start) &gt; 0 and start[-1] == '@':
	line = line.replace('@@','@')

out.append(line)</t>
<t tx="T747">assert(match(s,i,"+at"))
self.scanDoc(file,s,i,out,kind)</t>
<t tx="T748">assert(match(s,i,"+body"))

child_out = [] ; child = v # Do not change out or v!
oldIndent = self.indent ; self.indent = lineIndent
self.scanText(file,child,child_out,atFile.endBody)

if 0:
	if child.isOrphan():
		self.readError("Replacing body text of orphan: " + child.headString())

# Set the body, removing cursed newlines.
# This must be done here, not in the @+node logic.
body = string.join(child_out, "")
body = body.replace('\r', '')
## child.t.setTnodeText(body)
child.t.tempBodyString = body
self.indent = oldIndent</t>
<t tx="T749">assert(match(s,i,"+doc"))
self.scanDoc(file,s,i,out,kind)</t>
<t tx="T750">assert(match(s,i,"+node:"))
i += 6

childIndex = 0 ; cloneIndex = 0
&lt;&lt; Set childIndex &gt;&gt;
&lt;&lt; Set cloneIndex &gt;&gt;
headline = ""
&lt;&lt; Set headline and ref &gt;&gt;

# print childIndex,headline

if childIndex == 0: # The root node.
	&lt;&lt; Check the filename in the sentinel &gt;&gt;
	# Put the text of the root node in the current node.
	self.scanText(file,v,out,atFile.endNode)
	v.t.setCloneIndex(cloneIndex)
	# if cloneIndex &gt; 0: trace("clone index:" + `cloneIndex` + ", " + `v`)
else:
	# NB: this call to createNthChild is the bottleneck!
	child = self.createNthChild(childIndex,v,headline)
	child.t.setCloneIndex(cloneIndex)
	# if cloneIndex &gt; 0: trace("clone index:" + `cloneIndex` + ", " + `child`)
	self.scanText(file,child,out,atFile.endNode)

&lt;&lt; look for sentinels that may follow a reference &gt;&gt;</t>
<t tx="T751">i = skip_ws(s,i) ; j = i
while i &lt; len(s) and s[i] in string.digits:
	i += 1

if j == i:
	self.readError("Implicit child index in @+node")
	childIndex = 0
else:
	childIndex = int(s[j:i])

if match(s,i,':'):
	i += 1 # Skip the ":".
else:
	self.readError("Bad child index in @+node")</t>
<t tx="T752">while i &lt; len(s) and s[i] != ':' and not is_nl(s,i):
	if match(s,i,"C="):
		# set cloneIndex from the C=nnn, field
		i += 2 ; j = i
		while i &lt; len(s) and s[i] in string.digits:
			i += 1
		if j &lt; i:
			cloneIndex = int(s[j:i])
	else: i += 1 # Ignore unknown status bits.

if match(s,i,":"):
	i += 1
else:
	self.readError("Bad attribute field in @+node")</t>
<t tx="T753"># Set headline to the rest of the line.
# 6/22/03: don't strip leading whitespace.
if len(self.endSentinelComment) == 0:
	headline = s[i:-1].rstrip()
else:
	# 10/24/02: search from the right, not the left.
	k = s.rfind(self.endSentinelComment,i)
	headline = s[i:k].rstrip() # works if k == -1
	
# 10/23/02: The cweb hack: undouble @ signs if the opening comment delim ends in '@'.
if self.startSentinelComment[-1:] == '@':
	headline = headline.replace('@@','@')

# Set reference if it exists.
i = skip_ws(s,i)

if 0: # no longer used
	if match(s,i,"&lt;&lt;"):
		k = s.find("&gt;&gt;",i)
		if k != -1: ref = s[i:k+2]</t>
<t tx="T754">h = headline.strip()

if h[:5] == "@file":
	i,junk,junk = scanAtFileOptions(h)
	fileName = string.strip(h[i:])
	if fileName != self.targetFileName:
		self.readError("File name in @node sentinel does not match file's name")
elif h[:8] == "@rawfile":
	fileName = string.strip(h[8:])
	if fileName != self.targetFileName:
		self.readError("File name in @node sentinel does not match file's name")
else:
	self.readError("Missing @file in root @node sentinel")
</t>
<t tx="T755">s = self.readLine(file)
kind = self.sentinelKind(s)

if len(s) &gt; 1 and kind == atFile.startVerbatimAfterRef:
	s = self.readLine(file)
	# trace("verbatim:"+`s`)
	out.append(s)
elif len(s) &gt; 1 and self.sentinelKind(s) == atFile.noSentinel:
	out.append(s)
else:
	nextLine = s # Handle the sentinel or blank line later.
</t>
<t tx="T756">assert(match(s,i,"+others"))

# Make sure that the generated at-others is properly indented.
out.append(leading_ws + "@others")

self.scanText(file,v,out,atFile.endOthers)</t>
<t tx="T757">elif kind == atFile.startComment:
	&lt;&lt; scan @comment &gt;&gt;
elif kind == atFile.startDelims:
	&lt;&lt; scan @delims &gt;&gt;
elif kind == atFile.startDirective:
	&lt;&lt; scan @@ &gt;&gt;
elif kind == atFile.startLeo:
	&lt;&lt; scan @+leo &gt;&gt;
elif kind == atFile.startVerbatim:
	&lt;&lt; scan @verbatim &gt;&gt;</t>
<t tx="T758">assert(match(s,i,"+leo"))
self.readError("Ignoring unexpected @+leo sentinel")</t>
<t tx="T759"># The first '@' has already been eaten.
assert(match(s,i,"@"))

if match_word(s,i,"@raw"):
	self.raw = true
elif match_word(s,i,"@end_raw"):
	self.raw = false

e = self.endSentinelComment
s2 = s[i:]
if len(e) &gt; 0:
	k = s.rfind(e,i)
	if k != -1:
		s2 = s[i:k] + '\n'
	
start = self.startSentinelComment
if start and len(start) &gt; 0 and start[-1] == '@':
	s2 = s2.replace('@@','@')
out.append(s2)
# trace(`s2`)</t>
<t tx="T760">assert(match(s,i,"comment"))

# We need do nothing more to ignore the comment line!
</t>
<t tx="T761">assert(match(s,i-1,"@delims"));

# Skip the keyword and whitespace.
i0 = i-1
i = skip_ws(s,i-1+7)
	
# Get the first delim.
j = i
while i &lt; len(s) and not is_ws(s[i]) and not is_nl(s,i):
	i += 1

if j &lt; i:
	self.startSentinelComment = s[j:i]
	# print "delim1:", self.startSentinelComment

	# Get the optional second delim.
	j = i = skip_ws(s,i)
	while i &lt; len(s) and not is_ws(s[i]) and not is_nl(s,i):
		i += 1
	end = choose(j&lt;i,s[j:i],"")
	i2 = skip_ws(s,i)
	if end == self.endSentinelComment and (i2 &gt;= len(s) or is_nl(s,i2)):
		self.endSentinelComment = "" # Not really two params.
		line = s[i0:j]
		line = line.rstrip()
		out.append(line+'\n')
	else:
		self.endSentinelComment = end
		# print "delim2:",end
		line = s[i0:i]
		line = line.rstrip()
		out.append(line+'\n')
else:
	self.readError("Bad @delims")
	# Append the bad @delims line to the body text.
	out.append("@delims")</t>
<t tx="T762">assert(match(s,i,"verbatim"))

# Skip the sentinel.
s = self.readLine(file) 

# Append the next line to the text.
i = self.skipIndent(s,0,self.indent)
out.append(s[i:])
</t>
<t tx="T763">j = i
i = skip_line(s,i)
line = s[j:i]
self.readError("Unknown sentinel: " + line)</t>
<t tx="T764"></t>
<t tx="T765"># 4/5/03: config.write_clone_indices no longer used.

def nodeSentinelText(self,v):
	
	if v == self.root or not v.parent():
		index = 0
	else:
		index = v.childIndex() + 1

	h = v.headString()
	&lt;&lt; remove comment delims from h if necessary &gt;&gt;

	return str(index) + '::' + h</t>
<t tx="T766">@ Bug fix 1/24/03:

If the present @language/@comment settings do not specify a single-line comment we remove all block comment delims from h.  This prevents headline text from interfering with the parsing of node sentinels.
@c

start = self.startSentinelComment
end = self.endSentinelComment

if end and len(end) &gt; 0:
	h = h.replace(start,"")
	h = h.replace(end,"")</t>
<t tx="T767">def putCloseNodeSentinel(self,v):

	s = self.nodeSentinelText(v)
	self.putSentinel("@-node:" + s)</t>
<t tx="T768">@ root is an ancestor of v, or root == v.  We call putCloseSentinel for v up to, but not including, root.
@c
def putCloseSentinels(self,root,v):

	self.putCloseNodeSentinel(v)
	while 1:
		v = v.parent()
		assert(v) # root must be an ancestor of v.
		if  v == root: break
		self.putCloseNodeSentinel(v)</t>
<t tx="T769">@ This method is the same as putSentinel except we don't put an opening newline and leading whitespace.
@c
def putOpenLeoSentinel(self,s):
	
	if not self.sentinels:
		return # Handle @nosentinelsfile.

	self.os(self.startSentinelComment)
	self.os(s)
	encoding = self.encoding.lower()
	if encoding != "utf-8":
		self.os("-encoding=")
		self.os(encoding)
		self.os(".")
	self.os(self.endSentinelComment)
	if self.suppress_newlines: # 9/27/02
		self.newline_pending = true # Schedule a newline.
	else:
		self.onl() # End of sentinel.
</t>
<t tx="T770">@ This method puts an open node sentinel for node v.
@c
def putOpenNodeSentinel(self,v):

	if v.isAtFileNode() and v != self.root:
		self.writeError("@file not valid in: " + v.headString())
		return
	
	s = self.nodeSentinelText(v)
	self.putSentinel("@+node:" + s)</t>
<t tx="T771">@ root is an ancestor of v, or root == v.  We call putOpenNodeSentinel on all the descendents of root which are the ancestors of v.
@c
def putOpenSentinels(self,root,v):

	last = root
	while last != v:
		# Set node to v or the ancestor of v that is a child of last.
		node = v
		while node and node.parent() != last:
			node = node.parent()
		assert(node)
		self.putOpenNodeSentinel(node)
		last = node</t>
<t tx="T772">@ All sentinels are eventually output by this method.

Sentinels include both the preceding and following newlines. This rule greatly simplies the code and has several important benefits:

1. Callers never have to generate newlines before or after sentinels.  Similarly, routines that expand code and doc parts never have to add "extra" newlines.
2. There is no need for a "no-newline" directive.  If text follows a section reference, it will appear just after the newline that ends sentinel at the end of the expansion of the reference.  If no significant text follows a reference, there will be two newlines following the ending sentinel.

The only exception is that no newline is required before the opening "leo" sentinel. The putLeoSentinel and isLeoSentinel routines handle this minor exception.
@c
def putSentinel(self,s):
	
	if not self.sentinels:
		return # Handle @nosentinelsfile.

	self.newline_pending = false # discard any pending newline.
	self.onl() ; self.putIndent(self.indent) # Start of sentinel.
	self.os(self.startSentinelComment)

	# 11/1/02: The cweb hack: if the opening comment delim ends in '@',
	# double all '@' signs except the first, which is "doubled" by the
	# trailing '@' in the opening comment delimiter.
	start = self.startSentinelComment
	if start and len(start) &gt; 0 and start[-1] == '@':
		assert(s and len(s)&gt;0 and s[0]=='@')
		s = s.replace('@','@@')[1:]

	self.os(s)
	self.os(self.endSentinelComment)
	if self.suppress_newlines:
		self.newline_pending = true # Schedule a newline.
	else:
		self.onl() # End of sentinel.</t>
<t tx="T773">@ This method tells what kind of sentinel appears in line s.  Typically s will be an empty line before the actual sentinel, but it is also valid for s to be an actual sentinel line.

Returns (kind, s, emptyFlag), where emptyFlag is true if kind == noSentinel and s was an empty line on entry.
@c

sentinelDict = {
	"@comment" : startComment,
	"@delims" :  startDelims,
	"@verbatim": startVerbatim,
	"@verbatimAfterRef": startVerbatimAfterRef,
	"@+at":     startAt,     "@-at":     endAt,
	"@+body":   startBody,   "@-body":   endBody,
	"@+doc":    startDoc,    "@-doc":    endDoc,
	"@+leo":    startLeo,    "@-leo":    endLeo,
	"@+node":   startNode,   "@-node":   endNode,
	"@+others": startOthers, "@-others": endOthers }

def sentinelKind(self,s):

	# trace(s)
	i = skip_ws(s,0)
	if match(s,i,self.startSentinelComment): 
		i += len(self.startSentinelComment)
	else:
		return atFile.noSentinel

	# 10/30/02: locally undo cweb hack here
	start = self.startSentinelComment
	if start and len(start) &gt; 0 and start[-1] == '@':
		s = s[:i] + string.replace(s[i:],'@@','@')

	# Do not skip whitespace here!
	if match(s,i,"@&lt;&lt;"): return atFile.startRef
	if match(s,i,"@@"):   return atFile.startDirective
	if not match(s,i,'@'): return atFile.noSentinel
	j = i # start of lookup
	i += 1 # skip the at sign.
	if match(s,i,'+') or match(s,i,'-'):
		i += 1
	i = skip_c_id(s,i)
	key = s[j:i]
	if len(key) &gt; 0 and atFile.sentinelDict.has_key(key):
		# trace("found:",key)
		return atFile.sentinelDict[key]
	else:
		# trace("not found:",key)
		return atFile.noSentinel</t>
<t tx="T774"># Returns the name of the sentinel for warnings.

sentinelNameDict = {
	noSentinel: "&lt;no sentinel&gt;",
	startAt:     "@+at",     endAt:     "@-at",
	startBody:   "@+body",   endBody:   "@-body",
	startDoc:    "@+doc",    endDoc:    "@-doc",
	startLeo:    "@+leo",    endLeo:    "@-leo",
	startNode:   "@+node",   endNode:   "@-node",
	startOthers: "@+others", endOthers: "@-others",
	startComment:   "@comment",
	startDelims:    "@delims",
	startDirective: "@@",
	startRef:       "@&lt;&lt;",
	startVerbatim:  "@verbatim",
	startVerbatimAfterRef: "@verbatimAfterRef" }

def sentinelName(self, kind):
	if atFile.sentinelNameDict.has_key(kind):
		return atFile.sentinelNameDict[kind]
	else:
		return "&lt;unknown sentinel!&gt;"</t>
<t tx="T775">def skipSentinelStart(self,s,i):

	start = self.startSentinelComment
	assert(start and len(start)&gt;0)

	if is_nl(s,i): i = skip_nl(s,i)
	i = skip_ws(s,i)
	assert(match(s,i,start))
	i += len(start)
	# 7/8/02: Support for REM hack
	i = skip_ws(s,i)
	assert(i &lt; len(s) and s[i] == '@')
	return i + 1
</t>
<t tx="T776"></t>
<t tx="T777">def scanAll (self):

	c = self.commands ; v = c.rootVnode()
	while v:
		if v.isAtIgnoreNode():
			v = v.nodeAfterTree()
		elif v.isAtFileNode():
			self.scanFile(v)
			v = v.nodeAfterTree()
		else: v = v.threadNext()</t>
<t tx="T778">def scanFile(self,root):

	es("scanning: " + root.headString())
	self.targetFileName = root.atFileNodeName()
	self.root = root
	self.errors = 0
	&lt;&lt; open file &gt;&gt;
	if self.errors &gt; 0: return 0
	&lt;&lt; Scan the file buffer &gt;&gt;
	return self.errors == 0</t>
<t tx="T779">if len(self.targetFileName) == 0:
	self.readError("Missing file name")
else:
	try:
		file = open(self.targetFileName,'r')
	except:
		self.readError("Error reading file")
</t>
<t tx="T780">self.indent = 0
out = []
self.scanHeader(file)
self.scanText(file,root,out,atFile.endLeo)
s = string.join(out, "")
root.setBodyStringOrPane(s)</t>
<t tx="T781"></t>
<t tx="T782"># Returns the kind of at-directive or noDirective.

def directiveKind(self,s,i):

	n = len(s)
	if i &gt;= n or s[i] != '@':
		return atFile.noDirective

	table = (
		("@c",atFile.cDirective),
		("@code",atFile.codeDirective),
		("@doc",atFile.docDirective),
		("@end_raw",atFile.endRawDirective),
		("@others",atFile.othersDirective),
		("@raw",atFile.rawDirective))

	# This code rarely gets executed, so simple code suffices.
	if i+1 &gt;= n or match(s,i,"@ ") or match(s,i,"@\t") or match(s,i,"@\n"):
		# 10/25/02: @space is not recognized in cweb mode.
		# 11/15/02: Noweb doc parts are _never_ scanned in cweb mode.
		return choose(self.language=="cweb",
			atFile.noDirective,atFile.atDirective)

	# 10/28/02: @c and @(nonalpha) are not recognized in cweb mode.
	# We treat @(nonalpha) separately because @ is in the colorizer table.
	if self.language=="cweb" and (
		match_word(s,i,"@c") or
		i+1&gt;= n or s[i+1] not in string.letters):
		return atFile.noDirective

	for name,directive in table:
		if match_word(s,i,name):
			return directive
	# 10/14/02: return miscDirective only for real directives.
	for name in leoColor.leoKeywords:
		if match_word(s,i,name):
			return atFile.miscDirective

	return atFile.noDirective</t>
<t tx="T783">def error(self,message):

	es_error(message)
	self.errors += 1
</t>
<t tx="T784">def readError(self,message):

	# This is useful now that we don't print the actual messages.
	if self.errors == 0:
		es_error("----- error reading @file " + self.targetFileName)
		self.error(message) # 9/10/02: we must increment self.errors!
		
	print message

	if 0: # CVS conflicts create too many messages.
		self.error(message)
	
	self.root.setOrphan()
	self.root.setDirty()</t>
<t tx="T785">@ Once a directive is seen, no other related directives in nodes further up the tree have any effect.  For example, if an @color directive is seen in node v, no @color or @nocolor directives are examined in any ancestor of v.

This code is similar to Commands::scanAllDirectives, but it has been modified for use by the atFile class.
@c

def scanAllDirectives(self,v):
	
	"""Scan vnode v and v's ancestors looking for directives,
	setting corresponding atFile ivars.
	"""

	c = self.commands
	&lt;&lt; Set ivars &gt;&gt;
	&lt;&lt; Set path from @file node &gt;&gt;
	old = {}
	while v:
		s = v.t.bodyString
		dict = get_directives_dict(s)
		&lt;&lt; Test for @path &gt;&gt;
		&lt;&lt; Test for @encoding &gt;&gt;
		&lt;&lt; Test for @comment and @language &gt;&gt;
		&lt;&lt; Test for @header and @noheader &gt;&gt;
		&lt;&lt; Test for @lineending &gt;&gt;
		&lt;&lt; Test for @pagewidth &gt;&gt;
		&lt;&lt; Test for @tabwidth &gt;&gt;
		old.update(dict)
		v = v.parent()
	&lt;&lt; Set current directory &gt;&gt;
	&lt;&lt; Set comment Strings from delims &gt;&gt;</t>
<t tx="T786">self.page_width = self.commands.page_width
self.tab_width  = self.commands.tab_width

self.default_directory = None # 8/2: will be set later.

delim1, delim2, delim3 = set_delims_from_language(c.target_language)
self.language = c.target_language

self.encoding = app().config.default_derived_file_encoding
self.output_newline = getOutputNewline() # 4/24/03: initialize from config settings.</t>
<t tx="T787"># An absolute path in an @file node over-rides everything else.
# A relative path gets appended to the relative path by the open logic.

# Bug fix: 10/16/02
if v.isAtFileNode():
	name = v.atFileNodeName()
elif v.isAtRawFileNode():
	name = v.atRawFileNodeName()
elif v.isAtNoSentinelsFileNode():
	name = v.atNoSentinelsFileNodeName()
else:
	name = ""

dir = choose(name,os.path.dirname(name),None)
if dir and len(dir) &gt; 0 and os.path.isabs(dir):
	if os.path.exists(dir):
		self.default_directory = dir
	else: # 9/25/02
		self.default_directory = makeAllNonExistentDirectories(dir)
		if not self.default_directory:
			self.error("Directory \"" + dir + "\" does not exist")
			
</t>
<t tx="T788"># 10/17/02: @language and @comment may coexist in @file trees.
# For this to be effective the @comment directive should follow the @language directive.

if not old.has_key("comment") and dict.has_key("comment"):
	k = dict["comment"]
	# 11/14/02: Similar to fix below.
	delim1, delim2, delim3 = set_delims_from_string(s[k:])

# Reversion fix: 12/06/02: We must use elif here, not if.
elif not old.has_key("language") and dict.has_key("language"):
	k = dict["language"]
	# 11/14/02: Fix bug reported by J.M.Gilligan.
	self.language,delim1,delim2,delim3 = set_language(s,k)</t>
<t tx="T789">if not old.has_key("encoding") and dict.has_key("encoding"):
	
	e = scanAtEncodingDirective(s,dict)
	if e:
		self.encoding = e</t>
<t tx="T790"># EKR: 10/10/02: perform the sames checks done by tangle.scanAllDirectives.
if dict.has_key("header") and dict.has_key("noheader"):
	es("conflicting @header and @noheader directives")</t>
<t tx="T791">if not old.has_key("lineending") and dict.has_key("lineending"):
	
	lineending = scanAtLineendingDirective(s,dict)
	if lineending:
		self.output_newline = lineending
</t>
<t tx="T792"># We set the current director to a path so future writes will go to that directory.

loadDir = app().loadDir

if not self.default_directory and not old.has_key("path") and dict.has_key("path"):

	k = dict["path"]
	&lt;&lt; compute relative path from s[k:] &gt;&gt;
	if path and len(path) &gt; 0:
		base = getBaseDirectory() # returns "" on error.
		path = os.path.join(base,path)
		if os.path.isabs(path):
			&lt;&lt; handle absolute path &gt;&gt;
		else:
			self.error("ignoring bad @path: " + path)
	else:
		self.error("ignoring empty @path")</t>
<t tx="T793">j = i = k + len("@path")
i = skip_to_end_of_line(s,i)
path = string.strip(s[j:i])

# Remove leading and trailing delims if they exist.
if len(path) &gt; 2 and (
	(path[0]=='&lt;' and path[-1] == '&gt;') or
	(path[0]=='"' and path[-1] == '"') ):
	path = path[1:-1]
path = path.strip()

if 0: # 11/14/02: we want a _relative_ path, not an absolute path.
	path = os.path.join(loadDir,path)</t>
<t tx="T794"># path is an absolute path.

if os.path.exists(path):
	self.default_directory = path
else: # 9/25/02
	self.default_directory = makeAllNonExistentDirectories(path)
	if not self.default_directory:
		self.error("invalid @path: " + path)
</t>
<t tx="T795">if dict.has_key("pagewidth") and not old.has_key("pagewidth"):
	
	w = scanAtPagewidthDirective(s,dict,issue_error_flag=true)
	if w and w &gt; 0:
		self.page_width = w</t>
<t tx="T796">if dict.has_key("tabwidth") and not old.has_key("tabwidth"):
	
	w = scanAtTabwidthDirective(s,dict,issue_error_flag=true)
	if w and w != 0:
		self.tab_width = w

</t>
<t tx="T797"># This code is executed if no valid absolute path was specified in the @file node or in an @path directive.

if c.frame and not self.default_directory:
	base = getBaseDirectory() # returns "" on error.
	for dir in (c.tangle_directory,c.frame.openDirectory,c.openDirectory):
		if dir and len(dir) &gt; 0:
			dir = os.path.join(base,dir)
			if os.path.isabs(dir): # Errors may result in relative or invalid path.
				if os.path.exists(dir):
					self.default_directory = dir ; break
				else: # 9/25/02
					self.default_directory = makeAllNonExistentDirectories(dir)

if not self.default_directory:
	# This should never happen: c.openDirectory should be a good last resort.
	self.error("No absolute directory specified anywhere.")
	self.default_directory = ""</t>
<t tx="T798"># Use single-line comments if we have a choice.
# 8/2/01: delim1,delim2,delim3 now correspond to line,start,end
if delim1:
	self.startSentinelComment = delim1
	self.endSentinelComment = "" # Must not be None.
elif delim2 and delim3:
	self.startSentinelComment = delim2
	self.endSentinelComment = delim3
else: # Emergency!
	# assert(0)
	es("Unknown language: using Python comment delimiters")
	es("c.target_language:"+`c.target_language`)
	es("delim1,delim2,delim3:" + `delim1`+":"+`delim2`+":"+`delim3`)
	self.startSentinelComment = "#" # This should never happen!
	self.endSentinelComment = ""</t>
<t tx="T799"># Skip past whitespace equivalent to width spaces.

def skipIndent(self,s,i,width):

	ws = 0 ; n = len(s)
	while i &lt; n and ws &lt; width:
		if   s[i] == '\t': ws += (abs(self.tab_width) - (ws % abs(self.tab_width)))
		elif s[i] == ' ':  ws += 1
		else: break
		i += 1
	return i</t>
<t tx="T800">def writeError(self,message):

	if self.errors == 0:
		es_error("errors writing: " + self.targetFileName)

	self.error(message)
	self.root.setOrphan()
	self.root.setDirty()</t>
<t tx="T801"></t>
<t tx="T802"></t>
<t tx="T803">def rawWrite(self,root):

	trace("old_df",root)
	
	c = self.commands ; self.root = root
	self.errors = 0
	c.endEditing() # Capture the current headline.
	try:
		self.targetFileName = root.atRawFileNodeName()
		ok = self.openWriteFile(root)
		if not ok: return
		next = root.nodeAfterTree()
		&lt;&lt; write root's tree &gt;&gt;
		self.closeWriteFile()
		self.replaceTargetFileIfDifferent()
		root.clearOrphan() ; root.clearDirty()
	except:
		self.handleWriteException(root)
</t>
<t tx="T804">next = root.nodeAfterTree()

if 0: # Clone indices are no longer used.
	self.updateCloneIndices(root, next)

&lt;&lt; put all @first lines in root &gt;&gt;
self.putOpenLeoSentinel("@+leo")
&lt;&lt; put optional @comment sentinel lines &gt;&gt;

v = root
while v and v != next:
	&lt;&lt; Write v's node &gt;&gt;
	v = v.threadNext()

self.putSentinel("@-leo")
&lt;&lt; put all @last lines in root &gt;&gt;</t>
<t tx="T805">@ Write any @first lines.  These lines are also converted to @verbatim lines, so the read logic simply ignores lines preceding the @+leo sentinel.
@c

s = root.t.bodyString
tag = "@first"
i = 0
while match(s,i,tag):
	i += len(tag)
	i = skip_ws(s,i)
	j = i
	i = skip_to_end_of_line(s,i)
	# 21-SEP-2002 DTHEIN: write @first line, whether empty or not
	line = s[j:i]
	self.putBuffered(line) ; self.onl()
	i = skip_nl(s,i)</t>
<t tx="T806">s2 = app().config.output_initial_comment
if s2:
	lines = string.split(s2,"\\n")
	for line in lines:
		line = line.replace("@date",time.asctime())
		if len(line)&gt; 0:
			self.putSentinel("@comment " + line)
</t>
<t tx="T807">self.putOpenNodeSentinel(v)
	
s = v.bodyString()
if s and len(s) &gt; 0:
	self.putSentinel("@+body")
	if self.newline_pending:
		self.newline_pending = false
		self.onl()
	s = toEncodedString(s,self.encoding,reportErrors=true) # 3/7/03
	self.outputStringWithLineEndings(s)
	self.putSentinel("@-body")
	
self.putCloseNodeSentinel(v)
</t>
<t tx="T808">@ Write any @last lines.  These lines are also converted to @verbatim lines, so the read logic simply ignores lines following the @-leo sentinel.
@c

tag = "@last"
lines = string.split(root.t.bodyString,'\n')
n = len(lines) ; j = k = n - 1
# Don't write an empty last line.
if j &gt;= 0 and len(lines[j])==0:
	j = k = n - 2
# Scan backwards for @last directives.
while j &gt;= 0:
	line = lines[j]
	if match(line,0,tag): j -= 1
	else: break
# Write the @last lines.
for line in lines[j+1:k+1]:
	i = len(tag) ; i = skip_ws(line,i)
	self.putBuffered(line[i:]) ; self.onl()</t>
<t tx="T809">def silentWrite(self,root):

	trace("old_df",root)

	c = self.commands ; self.root = root
	self.errors = 0
	c.endEditing() # Capture the current headline.
	try:
		self.targetFileName = root.atSilentFileNodeName()
		ok = self.openWriteFile(root)
		if not ok: return
		next = root.nodeAfterTree()
		v = root
		while v and v != next:
			&lt;&lt; Write v's headline if it starts with @@ &gt;&gt;
			&lt;&lt; Write v's body &gt;&gt;
			v = v.threadNext()
		self.closeWriteFile()
		self.replaceTargetFileIfDifferent()
		root.clearOrphan() ; root.clearDirty()
	except:
		self.handleWriteException(root)</t>
<t tx="T810">s = v.headString()
if match(s,0,"@@"):
	s = s[2:]
	if s and len(s) &gt; 0:
		s = toEncodedString(s,self.encoding,reportErrors=true) # 3/7/03
		self.outputFile.write(s)
</t>
<t tx="T811">s = v.bodyString()
if s and len(s) &gt; 0:
	s = toEncodedString(s,self.encoding,reportErrors=true) # 3/7/03
	self.outputStringWithLineEndings(s)</t>
<t tx="T812"># This is the entry point to the write code.  root should be an @file vnode.

def write(self,root,nosentinels=false):
	
	trace("old_df",root)
	
	# Remove any old tnodeList.
	if hasattr(root,"tnodeList"):
		trace("removing tnodeList for " + `root`)
		delattr(root,"tnodeList")

	c = self.commands
	self.sentinels = not nosentinels
	&lt;&lt; initialize &gt;&gt;
	try:
		&lt;&lt; open the file; return on error &gt;&gt;
		root.clearVisitedInTree()
		&lt;&lt; write then entire @file tree &gt;&gt;
		self.closeWriteFile()
		&lt;&lt; warn about @ignored and orphans &gt;&gt;
		&lt;&lt; finish writing &gt;&gt;
	except:
		self.handleWriteException()
</t>
<t tx="T813">self.errors = 0 # 9/26/02
c.setIvarsFromPrefs()
self.root = root
self.raw = false
c.endEditing() # Capture the current headline.</t>
<t tx="T814">if nosentinels:
	self.targetFileName = root.atNoSentinelsFileNodeName()
else:
	self.targetFileName = root.atFileNodeName()

ok = self.openWriteFile(root)
if not ok: return</t>
<t tx="T815">next = root.nodeAfterTree()

&lt;&lt; put all @first lines in root &gt;&gt;
&lt;&lt; write the derived file &gt;&gt;
&lt;&lt; put all @last lines in root &gt;&gt;

root.setVisited()</t>
<t tx="T816">tag1 = "@+leo"

self.putOpenLeoSentinel(tag1)
self.putInitialComment()
self.putOpenNodeSentinel(root)
self.putBodyPart(root)
self.putCloseNodeSentinel(root)
self.putSentinel("@-leo")</t>
<t tx="T817"># 10/26/02: Always warn, even when language=="cweb"

next = root.nodeAfterTree()
v = root
while v and v != next:
	if not v.isVisited():
		self.writeError("Orphan node:  " + v.headString())
	if v.isAtIgnoreNode():
		self.writeError("@ignore node: " + v.headString())
	v = v.threadNext()
</t>
<t tx="T818">@ We set the orphan and dirty flags if there are problems writing the file to force Commands::write_LEO_file to write the tree to the .leo file.
@c

if self.errors &gt; 0 or self.root.isOrphan():
	root.setOrphan()
	root.setDirty() # 2/9/02: make _sure_ we try to rewrite this file.
	os.remove(self.outputFileName) # Delete the temp file.
	es("Not written: " + self.outputFileName)
else:
	root.clearOrphan()
	root.clearDirty()
	self.replaceTargetFileIfDifferent()</t>
<t tx="T819"></t>
<t tx="T820">def closeWriteFile (self):
	
	if self.outputFile:
		if self.suppress_newlines and self.newline_pending:
			self.newline_pending = false
			self.onl() # Make sure file ends with a newline.
		self.outputFile.flush()
		self.outputFile.close()
		self.outputFile = None
</t>
<t tx="T821">def handleWriteException (self,root=None):
	
	es("exception writing:" + self.targetFileName)
	es_exception()
	
	if self.outputFile:
		self.outputFile.flush()
		self.outputFile.close()
		self.outputFile = None
	
	if self.outputFileName != None:
		try: # Just delete the temp file.
			os.remove(self.outputFileName)
		except:
			es("exception deleting:" + self.outputFileName)
			es_exception()

	if root:
		# Make sure we try to rewrite this file.
		root.setOrphan()
		root.setDirty()</t>
<t tx="T822"># Open files.  Set root.orphan and root.dirty flags and return on errors.

def openWriteFile (self,root):

	try:
		self.scanAllDirectives(root)
		valid = self.errors == 0
	except:
		es("exception in atFile.scanAllDirectives")
		es_exception()
		valid = false
	
	if valid:
		try:
			fn = self.targetFileName
			self.shortFileName = fn # name to use in status messages.
			self.targetFileName = os.path.join(self.default_directory,fn)
			self.targetFileName = os.path.normpath(self.targetFileName)
			path = os.path.dirname(self.targetFileName)
			if path and len(path) &gt; 0:
				valid = os.path.exists(path)
				if not valid:
					self.writeError("path does not exist: " + path)
			else:
				valid = false
		except:
			es("exception creating path:" + fn)
			es_exception()
			valid = false
	
	if valid:
		if os.path.exists(self.targetFileName):
			try:
				read_only = not os.access(self.targetFileName,os.W_OK)
				if read_only:
					es("read only: " + self.targetFileName)
					valid = false
			except:
				pass # os.access() may not exist on all platforms.
		
	if valid:
		try:
			self.outputFileName = self.targetFileName + ".tmp"
			self.outputFile = open(self.outputFileName,'wb')
			valid = self.outputFile != None
			if not valid:
				self.writeError("can not open " + self.outputFileName)
		except:
			es("exception opening:" + self.outputFileName)
			es_exception()
			valid = false
	
	if not valid:
		root.setOrphan()
		root.setDirty()
	
	return valid</t>
<t tx="T823">def putInitialComment (self):
	
	s2 = app().config.output_initial_comment
	if s2:
		lines = string.split(s2,"\\n")
		for line in lines:
			line = line.replace("@date",time.asctime())
			if len(line)&gt; 0:
				self.putSentinel("@comment " + line)</t>
<t tx="T824">def replaceTargetFileIfDifferent (self):
	
	assert(self.outputFile == None)
	
	if os.path.exists(self.targetFileName):
		if filecmp.cmp(self.outputFileName,self.targetFileName):
			&lt;&lt; delete the output file &gt;&gt;
		else:
			&lt;&lt; replace the target file with the output file &gt;&gt;
	else:
		&lt;&lt; rename the output file to be the target file &gt;&gt;
</t>
<t tx="T825">try: # Just delete the temp file.
	os.remove(self.outputFileName)
except:
	es("exception deleting:" + self.outputFileName)
	es_exception()

es("unchanged: " + self.shortFileName)</t>
<t tx="T826">try:
	# 10/6/02: retain the access mode of the previous file,
	# removing any setuid, setgid, and sticky bits.
	mode = (os.stat(self.targetFileName))[0] &amp; 0777
except:
	mode = None

try: # Replace target file with temp file.
	os.remove(self.targetFileName)
	try:
		utils_rename(self.outputFileName,self.targetFileName)
		if mode != None: # 10/3/02: retain the access mode of the previous file.
			try:
				os.chmod(self.targetFileName,mode)
			except:
				es("exception in os.chmod(%s)" % (self.targetFileName))
		es("writing: " + self.shortFileName)
	except:
		# 6/28/03
		self.writeError("exception renaming: %s to: %s" % (self.outputFileName,self.targetFileName))
		es_exception()
except:
	self.writeError("exception removing:" + self.targetFileName)
	es_exception()
	try: # Delete the temp file when the deleting the target file fails.
		os.remove(self.outputFileName)
	except:
		es("exception deleting:" + self.outputFileName)
		es_exception()</t>
<t tx="T827">try:
	utils_rename(self.outputFileName,self.targetFileName)
	es("creating: " + self.targetFileName)
except:
	self.writeError("exception renaming:" + self.outputFileName +
		" to " + self.targetFileName)
	es_exception()</t>
<t tx="T828"># Write the string s as-is except that we replace '\n' with the proper line ending.

def outputStringWithLineEndings (self,s):

	# Calling self.onl() runs afoul of queued newlines.
	self.os(s.replace('\n',self.output_newline))</t>
<t tx="T829">def putBodyPart(self,v):
	
	""" Generate the body enclosed in sentinel lines."""

	# trace(`v`)
	s = v.t.bodyString
	i = skip_ws_and_nl(s, 0)
	if i &gt;= len(s): return

	s = removeTrailingWs(s) # don't use string.rstrip!
	self.putSentinel("@+body")
	&lt;&lt; put code/doc parts and sentinels &gt;&gt;
	self.putSentinel("@-body")</t>
<t tx="T830">i = 0 ; n = len(s)
firstLastHack = 1

if firstLastHack:
	&lt;&lt; initialize lookingForFirst/Last &amp; initialLastDirective &gt;&gt;
while i &lt; n:
	kind = self.directiveKind(s,i)
	if firstLastHack:
		&lt;&lt; set lookingForFirst/Last &amp; initialLastDirective &gt;&gt;
	j = i
	if kind == atFile.docDirective or kind == atFile.atDirective:
		i = self.putDoc(s,i,kind)
	elif ( # 10/16/02
		kind == atFile.miscDirective or
		kind == atFile.rawDirective or
		kind == atFile.endRawDirective ):
		if firstLastHack:
			&lt;&lt; handle misc directives &gt;&gt;
		else:
			i = self.putDirective(s,i)
	elif kind == atFile.noDirective or kind == atFile.othersDirective:
		i = self.putCodePart(s,i,v)
	elif kind == atFile.cDirective or kind == atFile.codeDirective:
		i = self.putDirective(s,i)
		i = self.putCodePart(s,i,v)
	else: assert(false) # We must handle everything that directiveKind returns
	assert(n == len(s))
	assert(j &lt; i) # We must make progress.

if firstLastHack:
	&lt;&lt; put out the last directives, if any &gt;&gt;</t>
<t tx="T831"># 14-SEP-2002 DTHEIN: If this is the root node, then handle all @first directives here
lookingForLast = 0
lookingForFirst = 0
initialLastDirective = -1
lastDirectiveCount = 0
if (v == self.root):
	lookingForLast = 1
	lookingForFirst = 1</t>
<t tx="T832"># 14-SEP-2002 DTHEIN: If first directive isn't @first, then stop looking for @first
if lookingForFirst:
	if kind != atFile.miscDirective:
		lookingForFirst = 0
	elif not match_word(s,i,"@first"):
		lookingForFirst = 0

if lookingForLast:
	if initialLastDirective == -1:
		if (kind == atFile.miscDirective) and match_word(s,i,"@last"):
			# mark the point where the last directive was found
			initialLastDirective = i
	else:
		if (kind != atFile.miscDirective) or (not match_word(s,i,"@last")):
			# found something after @last, so process the @last directives
			# in 'ignore them' mode
			i, initialLastDirective = initialLastDirective, -1
			lastDirectiveCount = 0
			kind = self.directiveKind(s,i)</t>
<t tx="T833">if lookingForFirst: # DTHEIN: can only be true if it is @first directive
	i = self.putEmptyDirective(s,i)
elif (initialLastDirective != -1) and match_word(s,i,"@last"):
	# DTHEIN: can only be here if lookingForLast is true
	# skip the last directive ... we'll output it at the end if it
	# is truly 'last'
	lastDirectiveCount += 1
	i = skip_line(s,i)
else:
	i = self.putDirective(s,i)</t>
<t tx="T834"># 14-SEP-2002 DTHEIN
if initialLastDirective != -1:
	d = initialLastDirective
	for k in range(lastDirectiveCount):
		d = self.putEmptyDirective(s,d)</t>
<t tx="T835">@ This method outputs a doc section terminated by @code or end-of-text.  All other interior directives become part of the doc part.
@c
def putDoc(self,s,i,kind):

	if kind == atFile.atDirective:
		i += 1 ; tag = "at"
	elif kind == atFile.docDirective:
		i += 4 ; tag = "doc"
	else: assert(false)
	# Set j to the end of the doc part.
	n = len(s) ; j = i
	while j &lt; n:
		j = skip_line(s, j)
		kind = self.directiveKind(s, j)
		if kind == atFile.codeDirective or kind == atFile.cDirective:
			break
	self.putSentinel("@+" + tag)
	self.putDocPart(s[i:j])
	self.putSentinel("@-" + tag)
	return j</t>
<t tx="T836"># Puts a comment part in comments.
# Note: this routine is _never_ called in cweb mode,
# so noweb section references are _valid_ in cweb doc parts!

def putDocPart(self,s):

	# j = skip_line(s,0) ; trace(`s[:j]`)
	c = self.commands
	single = len(self.endSentinelComment) == 0
	if not single:
		self.putIndent(self.indent)
		self.os(self.startSentinelComment) ; self.onl()
	# Put all lines.
	i = 0 ; n = len(s)
	while i &lt; n:
		self.putIndent(self.indent)
		leading = self.indent
		if single:
			self.os(self.startSentinelComment) ; self.oblank()
			leading += len(self.startSentinelComment) + 1
		&lt;&lt; copy words, splitting the line if needed &gt;&gt;
	if not single:
		# This comment is like a sentinel.
		self.onl() ; self.putIndent(self.indent)
		self.os(self.endSentinelComment)
		self.onl() # Note: no trailing whitespace.</t>
<t tx="T837">@ We remove trailing whitespace from lines that have _not_ been split so that a newline has been inserted by this routine if and only if it is preceded by whitespace.
@c

line = i # Start of the current line.
while i &lt; n:
	word = i # Start of the current word.
	# Skip the next word and trailing whitespace.
	i = skip_ws(s, i)
	while i &lt; n and not is_nl(s,i) and not is_ws(s[i]):
		i += 1
	i = skip_ws(s,i)
	# Output the line if no more is left.
	if i &lt; n and is_nl(s,i):
		break
	# Split the line before the current word if needed.
	lineLen = i - line
	if line == word or leading + lineLen &lt; self.page_width:
		word = i # Advance to the next word.
	else:
		# Write the line before the current word and insert a newline.
		theLine = s[line:word]
		self.os(theLine)
		self.onl() # This line must contain trailing whitespace.
		line = i = word  # Put word on the next line.
		break
# Remove trailing whitespace and output the remainder of the line.
theLine = string.rstrip(s[line:i]) # from right.
self.os(theLine)
if i &lt; n and is_nl(s,i):
	i = skip_nl(s,i)
	self.onl() # No inserted newline and no trailing whitespace.</t>
<t tx="T838">@ This method expands a code part, terminated by any at-directive except at-others.  It expands references and at-others and outputs @verbatim sentinels as needed.
@c
def putCodePart(self,s,i,v):

	c = self.commands
	atOthersSeen = false # true: at-others has been expanded.
	while i &lt; len(s):
		&lt;&lt; handle the start of a line &gt;&gt;
		&lt;&lt; put the line &gt;&gt;

	# Raw code parts can only end at the end of body text.
	self.raw = false
	return i</t>
<t tx="T839">@ The at-others directive is the only directive that is recognized following leading whitespace, so it is just a little tricky to recognize it.
@c

leading_nl = (s[i] == body_newline) # 9/27/02: look ahead before outputting newline.
if leading_nl:
	i = skip_nl(s,i)
	self.onl() # 10/15/02: simpler to do it here.

#leading_ws1 = i # 1/27/03
j,delta = skip_leading_ws_with_indent(s,i,self.tab_width)
#leading_ws2 = j # 1/27/03
kind1 = self.directiveKind(s,i)
kind2 = self.directiveKind(s,j)
if self.raw:
	if kind1 == atFile.endRawDirective:
		&lt;&lt; handle @end_raw &gt;&gt;
else:
	if kind1 == atFile.othersDirective or kind2 == atFile.othersDirective:
		&lt;&lt; handle @others &gt;&gt;
	elif kind1 == atFile.rawDirective:
		&lt;&lt; handle @raw &gt;&gt;
	elif kind1 == atFile.noDirective:
		&lt;&lt; put @verbatim sentinel if necessary &gt;&gt;
	else:
		break # all other directives terminate the code part.</t>
<t tx="T840"># This skips all indent and delta whitespace, so putAtOthers must generate it all.

if 0: # 9/27/02: eliminates the newline preceeding the @+others sentinel.
	# This does not seem to be a good idea.
	i = skip_line(s,i) 
else:
	i = skip_to_end_of_line(s,i)

if atOthersSeen:
	self.writeError("@others already expanded in: " + v.headString())
else:
	atOthersSeen = true
	self.putAtOthers(v, delta)
	
	# 12/8/02: Skip the newline _after_ the @others.
	if not self.sentinels and is_nl(s,i):
		i = skip_nl(s,i)
</t>
<t tx="T841">self.raw = true
self.putSentinel("@@raw")
i = skip_line(s,i)</t>
<t tx="T842">self.raw = false
self.putSentinel("@@end_raw")
i = skip_line(s,i)</t>
<t tx="T843">if match (s,i,self.startSentinelComment + '@'):
	self.putSentinel("@verbatim") # Bug fix (!!): 9/20/03</t>
<t tx="T844">if not self.raw:
	# 12/8/02: Don't write trailing indentation if not writing sentinels.
	if self.sentinels or j &lt; len(s):
		self.putIndent(self.indent)

newlineSeen = false
# 12/8/02: we buffer characters here for two reasons:
# 1) to make traces easier to read and 2) to increase speed.
buf = i # Indicate the start of buffered characters.
while i &lt; len(s) and not newlineSeen:
	ch = s[i]
	if ch == body_newline:
		break
	elif ch == body_ignored_newline:
		i += 1
	elif ch == '&lt;' and not self.raw:
		&lt;&lt; put possible section reference &gt;&gt;
	else:
		i += 1
# Output any buffered characters.
self.putBuffered(s[buf:i])</t>
<t tx="T845">isSection, j = self.isSectionName(s, i)

if isSection:
	# Output the buffered characters and clear the buffer.
	s2 = s[buf:i] ; buf = i
	# 7/9/03: don't output trailing indentation if we aren't generating sentinels.
	if not self.sentinels:
		while len(s2) and s2[-1] in (' ','\t'):
			s2 = s2[:-1]
	self.putBuffered(s2)
	# Output the expansion.
	name = s[i:j]
	j,newlineSeen = self.putRef(name,v,s,j,delta)
	assert(j &gt; i) # isSectionName must have made progress
	i = j ; buf = i
else:
	# This is _not_ an error.
	i += 1</t>
<t tx="T846">@ Returns true if v should be included in the expansion of the at-others directive in the body text of v's parent.

7/30/02: v will not be included if it is a definition node or if its body text contains an @ignore directive. Previously, a "nested" @others directive would also inhibit the inclusion of v.
@c
def inAtOthers(self,v):

	# Return false if this has been expanded previously.
	if  v.isVisited(): return false
	# Return false if this is a definition node.
	h = v.headString()
	i = skip_ws(h,0)
	isSection, j = self.isSectionName(h,i)
	if isSection: return false
	# Return false if v's body contains an @ignore or at-others directive.
	if 1: # 7/29/02: New code.  Amazingly, this appears to work!
		return not v.isAtIgnoreNode()
	else: # old &amp; reliable code
		return not v.isAtIgnoreNode() and not v.isAtOthersNode()</t>
<t tx="T847"># returns (flag, end). end is the index of the character after the section name.

def isSectionName(self,s,i):

	if not match(s,i,"&lt;&lt;"):
		return false, -1
	i = find_on_line(s,i,"&gt;&gt;")
	if i:
		return true, i + 2
	else:
		return false, -1</t>
<t tx="T848">@ The at-others directive is recognized only at the start of the line.  This code must generate all leading whitespace for the opening sentinel.
@c
def putAtOthers(self,v,delta):

	self.indent += delta
	self.putSentinel("@+others")

	child = v.firstChild()
	while child:
		if self.inAtOthers( child ):
			self.putAtOthersChild( child )
		child = child.next()

	self.putSentinel("@-others")
	self.indent -= delta</t>
<t tx="T849">def putAtOthersChild(self,v):
	
	# trace("%d %s" % (self.indent,`v`))
	self.putOpenNodeSentinel(v)
	
	# Insert the expansion of v.
	v.setVisited() # Make sure it is never expanded again.
	self.putBodyPart(v)

	# Insert expansions of all children.
	child = v.firstChild()
	while child:
		if self.inAtOthers( child ):
			self.putAtOthersChild( child )
		child = child.next()

	self.putCloseNodeSentinel(v)
</t>
<t tx="T850">def putRef (self,name,v,s,i,delta):

	newlineSeen = false
	ref = findReference(name, v)
	if not ref:
		self.writeError("undefined section: " + name +
			"\n\treferenced from: " + v.headString())
		return i,newlineSeen

	# trace(self.indent,delta,s[i:])
	&lt;&lt; Generate the expansion of the reference &gt;&gt;

	# The newlineSeen allows the caller to break out of the loop.
	return i,newlineSeen</t>
<t tx="T851"># Adjust indent here so sentinel looks better.
self.indent += delta

self.putSentinel("@" + name)
self.putOpenSentinels(v,ref)
self.putBodyPart(ref)
self.putCloseSentinels(v,ref)
&lt;&lt; Add @verbatimAfterRef sentinel if required &gt;&gt;

self.indent -= delta
ref.setVisited()</t>
<t tx="T852">j = skip_ws(s,i)
if j &lt; len(s) and match(s,j,self.startSentinelComment + '@'):
	self.putSentinel("@verbatimAfterRef")
	# 9/27/02: Put the line immediately, before the @-node sentinel.
	k = skip_to_end_of_line(s,i)
	self.putBuffered(s[i:k])
	i = k ; newlineSeen = false</t>
<t tx="T853"></t>
<t tx="T854">def putBuffered (self,s):
	
	"""Put s, converting all tabs to blanks as necessary."""
	
	if s:
		w = self.tab_width
		if w &lt; 0:
			#trace(s)
			lines = s.split('\n')
			for i in xrange(len(lines)):
				line = lines[i]
				line2 = ""
				for j in xrange(len(line)):
					ch = line[j]
					if ch == '\t':
						w2 = computeWidth(s[:j],w)
						w3 = (abs(w) - (w2 % abs(w)))
						line2 += ' ' * w3
					else:
						line2 += ch
				lines[i] = line2
			s = string.join(lines,'\n')
		#trace(s)
		self.os(s)</t>
<t tx="T855">def oblank(self):
	self.os(' ')

def oblanks(self,n):
	self.os(' ' * abs(n))

def onl(self):
	self.os(self.output_newline)

def os(self,s):
	if s is None or len(s) == 0: return
	if self.suppress_newlines and self.newline_pending:
		self.newline_pending = false
		s = self.output_newline + s
	if self.outputFile:
		try:
			s = toEncodedString(s,self.encoding,reportErrors=true)
			self.outputFile.write(s)
		except:
			es("exception writing:" + `s`)
			es_exception()

def otabs(self,n):
	self.os('\t' * abs(n))</t>
<t tx="T856"># This method outputs s, a directive or reference, in a sentinel.

def putDirective(self,s,i):

	tag = "@delims"
	assert(i &lt; len(s) and s[i] == '@')
	k = i
	j = skip_to_end_of_line(s,i)
	directive = s[i:j]

	if match_word(s,k,tag):
		&lt;&lt; handle @delims &gt;&gt;
	else:
		self.putSentinel("@" + directive)

	i = skip_line(s,k)
	return i</t>
<t tx="T857"># Put a space to protect the last delim.
self.putSentinel(directive + " ") # 10/23/02: put @delims, not @@delims

# Skip the keyword and whitespace.
j = i = skip_ws(s,k+len(tag))

# Get the first delim.
while i &lt; len(s) and not is_ws(s[i]) and not is_nl(s,i):
	i += 1
if j &lt; i:
	self.startSentinelComment = s[j:i]
	# Get the optional second delim.
	j = i = skip_ws(s,i)
	while i &lt; len(s) and not is_ws(s[i]) and not is_nl(s,i):
		i += 1
	self.endSentinelComment = choose(j&lt;i, s[j:i], "")
else:
	self.writeError("Bad @delims directive")</t>
<t tx="T858"># 14-SEP-2002 DTHEIN
# added for use by putBodyPart()

# This method outputs the directive without the parameter text
def putEmptyDirective(self,s,i):

	assert(i &lt; len(s) and s[i] == '@')
	
	endOfLine = s.find('\n',i)
	# 21-SEP-2002 DTHEIN: if no '\n' then just use line length
	if endOfLine == -1:
		endOfLine = len(s)
	token = s[i:endOfLine].split()
	directive = token[0]
	self.putSentinel("@" + directive)

	i = skip_line(s,i)
	return i</t>
<t tx="T859">def putIndent(self,n):
	
	"""Put tabs and spaces corresponding to n spaces, assuming that we are at the start of a line."""

	if n != 0:
		# trace(n)
		w = self.tab_width
		if w &gt; 1:
			q,r = divmod(n,w) 
			self.otabs(q) 
			self.oblanks(r)
		else:
			self.oblanks(n)</t>
<t tx="T860">class baseNewDerivedFile(oldDerivedFile):
	
	"""A class to read and write 4.x derived files."""

	@others
	
class newDerivedFile(baseNewDerivedFile):
	pass</t>
<t tx="T861">def __init__(self,theCommander):
	
	"""Ctor for 4.x atFile class."""
	
	at = self
	
	# trace("newDerivedFile.__init__")

	# Initialize the base class.
	oldDerivedFile.__init__(self,theCommander) 

	# For 4.x reading &amp; writing...
	at.inCode = true
	## at.nodeIndices = app().nodeIndices

	# For 4.x writing...
	at.docKind = None
	at.pending = [] # Doc part that remains to be written.

	# For 4.x reading...
	at.docOut = [] # The doc part being accumulated.
	at.done = false # true when @-leo seen.
	at.endSentinelStack = []
	at.importing = false
	at.importRoot = None
	at.indent = 0 ; at.indentStack = []
	at.lastLines = [] # The lines after @-leo
	at.leadingWs = ""
	at.out = None ; at.outStack = []
	at.root_seen = false # true: root vnode has been handled in this file.
	at.tnodeList = [] ; at.tnodeListIndex = 0
	at.t = None ; at.tStack = []

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
		# Ignored 3.x sentinels
		at.endBody:               at.ignoreOldSentinel,
		at.startBody:             at.ignoreOldSentinel,
		at.startVerbatimAfterRef: at.ignoreOldSentinel }</t>
<t tx="T862"></t>
<t tx="T863">def readOpenFile(self,root,file,fileName,firstLines):
	
	"""Read an open 4.x derived file."""
	
	trace("new_df",root)

	at = self ; c = at.commands
	
	# Scan the 4.x file.
	at.scanAllDirectives(root)
	at.tnodeListIndex = 0
	lastLines = at.scanText(file,root)
	root.t.setVisited() # Disable warning about set nodes.
	
	# Handle first and last lines.
	try: body = root.t.tempBodyString
	except: body = ""
	lines = body.split('\n')
	at.completeFirstDirectives(lines,firstLines)
	at.completeLastDirectives(lines,lastLines)
	s = '\n'.join(lines).replace('\r', '')
	## root.t.setTnodeText(s)
	root.t.tempBodyString = s</t>
<t tx="T864">def scanText (self,file,v):
	
	"""The new 4.x read code.."""

	at = self
	&lt;&lt; init ivars for scanText &gt;&gt;
	while at.errors == 0 and not at.done:
		s = at.readLine(file)
		if len(s) == 0: break
		kind = at.sentinelKind(s)
		# trace(at.sentinelName(kind),`s`)
		if kind == at.noSentinel:
			i = 0
		else:
			i = at.skipSentinelStart(s,0)
		func = at.dispatch_dict[kind]
		func(s,i)

	if at.errors == 0 and not at.done:
		&lt;&lt; report unexpected end of text &gt;&gt;

	return at.lastLines</t>
<t tx="T865"># Unstacked ivars...
at.done = false
at.inCode = true
at.lastLines = [] # The lines after @-leo
at.leadingWs = ""
at.indent = 0 # Changed only for sentinels.
at.rootSeen = false

# Stacked ivars...
at.endSentinelStack = [at.endLeo] # We have already handled the @+leo sentinel.
at.out = [] ; at.outStack = []
at.t = v.t ; at.tStack = []

if 0: # Useful for debugging.
	if hasattr(v,"tnodeList"):
		trace("len(v.tnodeList)",len(v.tnodeList),v)
	else:
		trace("no tnodeList",v)</t>
<t tx="T866">assert(at.endSentinelStack)

at.readError(
	"Unexpected end of file. Expecting %s sentinel" %
	at.sentinelName(at.endSentinelStack[-1]))</t>
<t tx="T867">def readNormalLine (self,s,i):

	at = self
	
	if at.inCode:
		if not at.raw:
			s = removeLeadingWhitespace(s,at.indent,at.tab_width)
		# trace(`s`)
		at.out.append(s)
	else:
		&lt;&lt; Skip the leading stuff &gt;&gt;
		&lt;&lt; Append s to docOut &gt;&gt;</t>
<t tx="T868">if len(at.endSentinelComment) == 0:
	# Skip the single comment delim and a blank.
	i = skip_ws(s,0)
	if match(s,i,at.startSentinelComment):
		i += len(at.startSentinelComment)
		if match(s,i," "): i += 1
else:
	i = at.skipIndent(s,0,at.indent)

</t>
<t tx="T869">line = s[i:-1] # remove newline for rstrip.

if line == line.rstrip():
	# no trailing whitespace: the newline is real.
	at.docOut.append(line + '\n')
else:
	# trailing whitespace: the newline is fake.
	at.docOut.append(line)</t>
<t tx="T870"></t>
<t tx="T871">def readStartAt (self,s,i):
	
	"""Read an @+at sentinel."""
	
	at = self ; assert(match(s,i,"+at"))
	at.endSentinelStack.append(at.endAt)
	at.docOut = ["@ \n"] # This newline may be removed by a following @nonl
	at.inCode = false
	
def readStartDoc (self,s,i):
	
	"""Read an @+doc sentinel."""

	at = self ; assert(match(s,i,"+doc"))
	at.endSentinelStack.append(at.endDoc)
	at.docOut = ["@doc \n"] # This newline may be removed by a following @nonl
	at.inCode = false</t>
<t tx="T872">def readStartLeo (self,s,i):
	
	"""Read an unexpected @+leo sentinel."""

	at = self
	assert(match(s,i,"+leo"))
	at.readError("Ignoring unexpected @+leo sentinel")</t>
<t tx="T873">def readStartNode (self,s,i):
	
	"""Read an @node sentinel."""
	
	at = self ; assert(match(s,i,"+node:"))
	i += 6
	
	&lt;&lt; Set headline, undoing the CWEB hack &gt;&gt;
	if not at.root_seen:
		at.root_seen = true
		&lt;&lt; Check the filename in the sentinel &gt;&gt;

	i,newIndent = skip_leading_ws_with_indent(s,0,at.tab_width)
	at.indentStack.append(at.indent) ; at.indent = newIndent
	
	at.outStack.append(at.out) ; at.out = []
	at.tStack.append(at.t) ; at.t = at.findChild(headline)
	
	at.endSentinelStack.append(at.endNode)</t>
<t tx="T874"># Set headline to the rest of the line.
# Don't strip leading whitespace."

if len(at.endSentinelComment) == 0:
	headline = s[i:-1].rstrip()
else:
	k = s.rfind(at.endSentinelComment,i)
	headline = s[i:k].rstrip() # works if k == -1

# Undo the CWEB hack: undouble @ signs if the opening comment delim ends in '@'.
if at.startSentinelComment[-1:] == '@':
	headline = headline.replace('@@','@')</t>
<t tx="T875">h = headline.strip()

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
<t tx="T876">def readStartOthers (self,s,i):
	
	"""Read an @+others sentinel."""

	at = self
	j = skip_ws(s,i)
	leadingWs = s[i:j]
	if leadingWs:
		assert(match(s,j,"@+others"))
	else:
		assert(match(s,j,"+others"))

	# Make sure that the generated at-others is properly indented.
	at.out.append(leadingWs + "@others\n")
	
	at.endSentinelStack.append(at.endOthers)</t>
<t tx="T877"></t>
<t tx="T878">def readEndAt (self,s,i):
	
	"""Read an @-at sentinel."""

	at = self
	at.readLastDocLine("@ ")
	at.popSentinelStack(at.endAt)
	at.inCode = true
		
def readEndDoc (self,s,i):
	
	"""Read an @-doc sentinel."""

	at = self
	at.readLastDocLine("@doc ")
	at.popSentinelStack(at.endDoc)
	at.inCode = true</t>
<t tx="T879">def readEndLeo (self,s,i):
	
	"""Read an @-leo sentinel."""
	
	at = self

	# Ignore everything after @-leo.
	# Such lines were presumably written by @last.
	while 1:
		s = at.readLine(at.file)
		if len(s) == 0: break
		at.lastLines.append(s) # Capture all trailing lines, even if empty.

	at.done = true</t>
<t tx="T880">def readEndNode (self,s,i):
	
	"""Handle end-of-node processing for @-others and @-ref sentinels."""

	at = self
	
	# End raw mode.
	at.raw = false
	
	# Set the temporary body text.
	s = ''.join(at.out)
	if s:
		# trace(`at.t`,`s`)
		if at.importing:
			at.t.bodyString = s
		else:
			at.t.tempBodyString = s
			
	# Indicate that the tnode has been set in the derived file.
	at.t.setVisited()

	# End the previous node sentinel.
	at.indent = at.indentStack.pop()
	at.out = at.outStack.pop()
	at.t = at.tStack.pop()

	at.popSentinelStack(at.endNode)</t>
<t tx="T881">def readEndOthers (self,s,i):
	
	"""Read an @-others sentinel."""
	
	at = self
	at.popSentinelStack(at.endOthers)</t>
<t tx="T882">def readLastDocLine (self,tag):
	
	at = self
	end = at.endSentinelComment
	start = at.startSentinelComment
	s = ''.join(at.docOut)
	
	# Remove the @doc or @space.  We'll add it back at the end.
	if match(s,0,tag):
		s = s[len(tag):]
	else:
		at.readError("Missing start of doc part")
		return
	
	# Skip leading newline if it exists.
	if 0: # This should only be done as a result of @nonl
		if s and s[0] == '\n':
			s = s[1:]

	if end:
		# Remove opening block delim.
		if match(s,0,start):
			s = s[len(start):]
		else:
			at.readError("Missing open block comment")
			return
			
		# Remove trailing newline.
		if s[-1] == '\n':
			s = s[:-1]
	
		# Remove closing block delim.
		if s[-len(end):] == end:
			s = s[:-len(end)]
		else:
			at.readError("Missing close block comment")
			return

	at.out.append(tag + s)
	at.docOut = []</t>
<t tx="T883"></t>
<t tx="T884">def  ignoreOldSentinel (self,s,i):
	
	"""Ignore an 3.x sentinel."""
	
	es("Ignoring 3.x sentinel: " + s.strip(), color="blue")</t>
<t tx="T885">def  readAfterRef (self,s,i):
	
	"""Read an @afterref sentinel."""
	
	at = self
	assert(match(s,i,"afterref"))
	
	# Append the next line to the text.
	s = at.readLine(at.file)
	at.out.append(s)</t>
<t tx="T886">def readComment (self,s,i):
	
	"""Read an @comment sentinel."""

	assert(match(s,i,"comment"))

	# Just ignore the comment line!
</t>
<t tx="T887">def readDelims (self,s,i):
	
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
<t tx="T888">def readDirective (self,s,i):
	
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
<t tx="T889">def readNl (self,s,i):
	
	"""Handle an @nonl sentinel."""
	
	at = self
	assert(match(s,i,"nl"))
	
	if at.inCode:
		at.out.append('\n')
	else:
		at.docOut.append('\n')</t>
<t tx="T890">def readNonl (self,s,i):
	
	"""Handle an @nonl sentinel."""
	
	at = self
	assert(match(s,i,"nonl"))
	
	if at.inCode:
		s = ''.join(at.out)
		if s and s[-1] == '\n':
			at.out = [s[:-1]]
		else:
			trace("out:",`s`)
			at.readError("unexpected @nonl directive in code part")	
	else:
		s = ''.join(at.pending)
		if s:
			if s and s[-1] == '\n':
				at.pending = [s[:-1]]
			else:
				trace("docOut:",`s`)
				at.readError("unexpected @nonl directive in pending doc part")
		else:
			s = ''.join(at.docOut)
			if s and s[-1] == '\n':
				at.docOut = [s[:-1]]
			else:
				trace("docOut:",`s`)
				at.readError("unexpected @nonl directive in doc part")</t>
<t tx="T891">@ The sentinel contains an @ followed by a section name in angle brackets.  This code is different from the code for the @@ sentinel: the expansion of the reference does not include a trailing newline.
@c

def readRef (self,s,i):
	
	"""Handle an @&lt;&lt; sentinel."""
	
	at = self
	j = skip_ws(s,i)
	assert(match(s,j,"&lt;&lt;"))
	
	if len(at.endSentinelComment) == 0:
		line = s[i:-1] # No trailing newline
	else:
		k = s.find(at.endSentinelComment,i)
		line = s[i:k] # No trailing newline, whatever k is.
			
	# Undo the cweb hack.
	start = at.startSentinelComment
	if start and len(start) &gt; 0 and start[-1] == '@':
		line = line.replace('@@','@')

	at.out.append(line)</t>
<t tx="T892">def readVerbatim (self,s,i):
	
	"""Read an @verbatim sentinel."""
	
	at = self
	assert(match(s,i,"verbatim"))
	
	# Append the next line to the text.
	s = at.readLine(at.file) 
	i = at.skipIndent(s,0,at.indent)
	at.out.append(s[i:])</t>
<t tx="T893">def badEndSentinel (self,expectedKind):
	
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
<t tx="T894"></t>
<t tx="T895">def nodeSentinelText(self,v):
	
	"""Return the text of a @+node or @-node sentinel for v."""
	
	at = self ; t = v.t ; h = v.headString()
	&lt;&lt; remove comment delims from h if necessary &gt;&gt;
	return h</t>
<t tx="T896">@ Bug fix 1/24/03:

If the present @language/@comment settings do not specify a single-line comment we remove all block comment delims from h.  This prevents headline text from interfering with the parsing of node sentinels.
@c

start = at.startSentinelComment
end = at.endSentinelComment

if end and len(end) &gt; 0:
	h = h.replace(start,"")
	h = h.replace(end,"")</t>
<t tx="T897">def putLeadInSentinel (self,s,i,j,delta):
	
	"""Generate @nonl sentinels as needed to ensure a newline before a group of sentinels.
	
	Set at.leadingWs as needed for @+others and @+&lt;&lt; sentinels.

	i points at the start of a line.
	j points at @others or a section reference.
	delta is the change in at.indent that is about to happen and hasn't happened yet."""

	at = self
	at.leadingWs = "" # Set the default.
	if i == j:
		return # The @others or ref starts a line.

	k = skip_ws(s,i)
	if j == k:
		# Only whitespace before the @others or ref.
		if 1: # new code
			at.leadingWs = s[i:j] # Remember the leading whitespace, including its spelling.
		else:
			# The @ws sentinel contributs the _delta_ of the whitespace that precedes it.
			at.putIndent(at.indent) ; at.os(s[i:j]) # Put the whitespace, preserving its spelling.
			oldIndent = at.indent ; at.indent = 0 # Put the @ws sentinel with no more leading whitespace.
			at.putSentinel("@ws",putLeadingNewlineFlag=false)
			at.indent = oldIndent
	else:
		at.os(s[k:j]) ; at.onl()
		at.indent += delta # Align the @nonl with the following line.
		at.putSentinel("@nonl")
		at.indent -= delta # Let the caller set at.indent permanently.</t>
<t tx="T898">def putOpenLeoSentinel(self,s):
	
	"""Write @+leo sentinel."""

	at = self
	
	if not at.sentinels:
		return # Handle @nosentinelsfile.

	encoding = at.encoding.lower()
	if encoding != "utf-8":
		s = s + "-encoding=%s." % (encoding)
	
	at.putSentinel(s)</t>
<t tx="T899"># This method outputs all sentinels.

def putSentinel(self,s,putLeadingNewlineFlag=false):

	"Write a sentinel whose text is s, applying the CWEB hack if needed."
	
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
<t tx="T900">@ The cweb hack:

If the opening comment delim ends in '@', double all '@' signs except the first, which is "doubled" by the trailing '@' in the opening comment delimiter.
@c

start = at.startSentinelComment
if start and start[-1] == '@':
	assert(s and s[0]=='@')
	s = s.replace('@','@@')[1:]</t>
<t tx="T901">def skipSentinelStart(self,s,i):
	
	"""Skip the start of a sentinel."""

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
<t tx="T902">def sentinelKind(self,s):
	
	"""Return the kind of sentinel at s."""
	
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

	# Locally undo cweb hack here
	start = at.startSentinelComment
	if start and len(start) &gt; 0 and start[-1] == '@':
		s = s[:i] + string.replace(s[i:],'@@','@')
		
	# 4.0: Look ahead for @[ws]@others and @[ws]&lt;&lt;
	if match(s,i,"@"):
		j = skip_ws(s,i+1)
		if j &gt; i+1:
			# trace(`ws`,`s`)
			if match(s,j,"@+others"):
				return at.startOthers
			elif match(s,j,"&lt;&lt;"):
				return at.startRef
			else:
				# No other sentinels allow whitespace following the '@'
				return at.noSentinel

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
		return sentinelDict[key]
	else:
		return at.noSentinel</t>
<t tx="T903"></t>
<t tx="T904"></t>
<t tx="T905"># 4.0: Don't use newline-pending logic.

def closeWriteFile (self):
	
	at = self
	if at.outputFile:
		at.outputFile.flush()
		at.outputFile.close()
		at.outputFile = None</t>
<t tx="T906"># This is the entry point to the write code.  root should be an @file vnode.

def write(self,root,nosentinels=false):
	
	"""Write a 4.x derived file."""
	
	trace("new_df",root)

	at = self ; c = at.commands
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
<t tx="T907">at.errors = 0
c.setIvarsFromPrefs()
at.root = root
at.root.tnodeList = []
at.raw = false
c.endEditing() # Capture the current headline.</t>
<t tx="T908">if nosentinels:
	at.targetFileName = root.atNoSentinelsFileNodeName()
else:
	at.targetFileName = root.atFileNodeName()

ok = at.openWriteFile(root)
if not ok: return</t>
<t tx="T909"># unvisited nodes will be orphans, except in cweb trees.
root.clearVisitedInTree()
next = root.nodeAfterTree()

&lt;&lt; put all @first lines in root &gt;&gt;

# Put the main part of the file.
at.putOpenLeoSentinel("@+leo-ver=4")
at.putInitialComment()
at.putBody(root)
at.putSentinel("@-leo")
root.setVisited()

&lt;&lt; put all @last lines in root &gt;&gt;


</t>
<t tx="T910">@ Write any @first lines.  These lines are also converted to @verbatim lines, so the read logic simply ignores lines preceding the @+leo sentinel.
@c

s = root.t.bodyString
tag = "@first"
i = 0
while match(s,i,tag):
	i += len(tag)
	i = skip_ws(s,i)
	j = i
	i = skip_to_end_of_line(s,i)
	# Write @first line, whether empty or not
	line = s[j:i]
	self.os(line) ; self.onl()
	i = skip_nl(s,i)</t>
<t tx="T911">@ Write any @last lines.  These lines are also converted to @verbatim lines, so the read logic simply ignores lines following the @-leo sentinel.
@c

tag = "@last"
lines = string.split(root.t.bodyString,'\n')
n = len(lines) ; j = k = n - 1
# Don't write an empty last line.
if j &gt;= 0 and len(lines[j])==0:
	j = k = n - 2
# Scan backwards for @last directives.
while j &gt;= 0:
	line = lines[j]
	if match(line,0,tag): j -= 1
	else: break
# Write the @last lines.
for line in lines[j+1:k+1]:
	i = len(tag) ; i = skip_ws(line,i)
	self.os(line[i:]) ; self.onl()</t>
<t tx="T912"># 10/26/02: Always warn, even when language=="cweb"

next = root.nodeAfterTree()
v = root
while v and v != next:
	if not v.isVisited():
		at.writeError("Orphan node:  " + v.headString())
	if v.isAtIgnoreNode():
		at.writeError("@ignore node: " + v.headString())
	v = v.threadNext()
</t>
<t tx="T913">@ We set the orphan and dirty flags if there are problems writing the file to force Commands::write_LEO_file to write the tree to the .leo file.
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
<t tx="T914">def rawWrite(self,root):

	trace("new_df",root)

	at = self
	c = at.commands ; at.root = root
	at.errors = 0
	c.endEditing() # Capture the current headline.
	try:
		at.targetFileName = root.atRawFileNodeName()
		ok = at.openWriteFile(root)
		if not ok: return
		next = root.nodeAfterTree()
		&lt;&lt; write root's tree &gt;&gt;
		at.closeWriteFile()
		at.replaceTargetFileIfDifferent()
		root.clearOrphan() ; root.clearDirty()
	except:
		at.handleWriteException(root)</t>
<t tx="T915">next = root.nodeAfterTree()

&lt;&lt; put all @first lines in root &gt;&gt;
at.putOpenLeoSentinel()
&lt;&lt; put optional @comment sentinel lines &gt;&gt;

v = root
while v and v != next:
	&lt;&lt; Write v's node &gt;&gt;
	v = v.threadNext()

at.putSentinel()
&lt;&lt; put all @last lines in root &gt;&gt;</t>
<t tx="T916">@ Write any @first lines.  These lines are also converted to @verbatim lines, so the read logic simply ignores lines preceding the @+leo sentinel.
@c

s = root.t.bodyString
tag = "@first"
i = 0
while match(s,i,tag):
	i += len(tag)
	i = skip_ws(s,i)
	j = i
	i = skip_to_end_of_line(s,i)
	# Write @first line, whether empty or not
	line = s[j:i]
	at.putBuffered(line) ; at.onl()
	i = skip_nl(s,i)</t>
<t tx="T917">s2 = app().config.output_initial_comment
if s2:
	lines = string.split(s2,"\\n")
	for line in lines:
		line = line.replace("@date",time.asctime())
		if len(line)&gt; 0:
			at.putSentinel("@comment " + line)
</t>
<t tx="T918">at.putOpenNodeSentinel(v)

s = v.bodyString()
if s and len(s) &gt; 0:
	
	s = toEncodedString(s,at.encoding,reportErrors=true) # 3/7/03
	at.outputStringWithLineEndings(s)
	
at.putCloseNodeSentinel(v)
</t>
<t tx="T919">@ Write any @last lines.  These lines are also converted to @verbatim lines, so the read logic simply ignores lines following the @-leo sentinel.
@c

tag = "@last"
lines = string.split(root.t.bodyString,'\n')
n = len(lines) ; j = k = n - 1
# Don't write an empty last line.
if j &gt;= 0 and len(lines[j])==0:
	j = k = n - 2
# Scan backwards for @last directives.
while j &gt;= 0:
	line = lines[j]
	if match(line,0,tag): j -= 1
	else: break
# Write the @last lines.
for line in lines[j+1:k+1]:
	i = len(tag) ; i = skip_ws(line,i)
	at.putBuffered(line[i:]) ; at.onl()</t>
<t tx="T920">def putBody(self,v):
	
	""" Generate the body enclosed in sentinel lines."""

	at = self ; s = v.bodyString()
	if not s: return

	inCode = true
	
	# Make _sure_ all lines end in a newline.
	# If we add a trailing newline, we'll generate an @nonl sentinel below.
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
	at.putCloseNodeSentinel(v)</t>
<t tx="T921">if kind == at.noDirective:
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
<t tx="T922"></t>
<t tx="T923">def inAtOthers(self,v):
	
	"""Returns true if v should be included in the expansion of the at-others directive
	
	in the body text of v's parent."""

	# Return false if this has been expanded previously.
	if  v.isVisited():
		# trace("previously visited",v)
		return false
	
	# Return false if this is a definition node.
	h = v.headString() ; i = skip_ws(h,0)
	isSection,junk = self.isSectionName(h,i)
	if isSection:
		# trace("is section",v)
		return false

	# Return false if v's body contains an @ignore directive.
	if v.isAtIgnoreNode():
		# trace("is @ignore",v)
		return false
	else:
		# trace("ok",v)
		return true</t>
<t tx="T924">def putAtOthersChild(self,v):

	v.setVisited() # Make sure v is never expanded again.
	self.putBody(v) # Insert the expansion of v.

	# Insert expansions of all children.
	child = v.firstChild()
	while child:
		if self.inAtOthers( child ):
			self.putAtOthersChild( child )
		child = child.next()
</t>
<t tx="T925">def putAtOthersLine (self,s,i,v):
	
	"""Put the expansion of @others."""
	
	at = self
	j,delta = skip_leading_ws_with_indent(s,i,at.tab_width)
	at.putLeadInSentinel(s,i,j,delta)

	at.indent += delta
	if at.leadingWs:
		at.putSentinel("@" + at.leadingWs + "@+others")
	else:
		at.putSentinel("@+others")
	
	child = v.firstChild()
	while child:
		if at.inAtOthers(child):
			at.putAtOthersChild(child)
		child = child.next()

	at.putSentinel("@-others")
	at.indent -= delta</t>
<t tx="T926">def putCodeLine (self,s,i):
	
	"""Put a normal code line."""
	
	at = self
	
	# Put @verbatim sentinel if required.
	k = skip_ws(s,i)
	if match(s,k,self.startSentinelComment + '@'):
		self.putSentinel("@verbatim")

	j = skip_line(s,i)
	at.putIndent(at.indent)
	line = s[i:j]
	# trace(`line`)
	at.os(line)</t>
<t tx="T927">def putRefLine(self,s,i,n1,n2,v):
	
	"""Put a reference at s[n1:n2+2] from v."""
	
	at = self ; name = s[n1:n2+2]

	ref = findReference(name,v)
	if not ref:
		at.writeError(
			"undefined section: %s\n\treferenced from: %s" %
			( name,v.headString()))
		return
	
	# Expand the ref.
	j,delta = skip_leading_ws_with_indent(s,i,at.tab_width)
	at.putLeadInSentinel(s,i,n1,delta)
	at.indent += delta
	if at.leadingWs:
		at.putSentinel("@" + at.leadingWs + name)
	else:
		at.putSentinel("@" + name)
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
		# Temporarily readjust delta to make @nl look better.
		at.indent += delta
		at.putSentinel("@nl")
		at.indent -= delta</t>
<t tx="T928"></t>
<t tx="T929">def putBlankDocLine (self):
	
	at = self
	
	at.putPending(split=false)

	if not at.endSentinelComment:
		at.putIndent(at.indent)
		at.os(at.startSentinelComment) ; at.oblank()

	at.onl()</t>
<t tx="T930">def putStartDocLine (self,s,i,kind):
	
	"""Write the start of a doc part."""
	
	at = self ; at.docKind = kind
	
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
	
	# 9/21/03: Looking ahead here helps preserve intended whitespace.
	if match(s,i,' ') or match(s,i,'\t'):
		i += 1
	j = skip_ws(s,i)
	
	# Put an @nonl sentinel if there is significant text following @doc or @.
	if not is_nl(s,j):
		at.putSentinel("@nonl")
		at.putDocLine(s,i)</t>
<t tx="T931">def putDocLine (self,s,i):
	
	"""Handle one line of a doc part.
	
	Output complete lines and split long lines and queue pending lines.
	Inserted newlines are always preceded by whitespace."""
	
	at = self
	j = skip_line(s,i)
	s = s[i:j]
	# trace(`s`)

	if at.endSentinelComment:
		leading = at.indent
	else:
		leading = at.indent + len(at.startSentinelComment) + 1

	if not s or s[0] == '\n':
		# A blank line.
		at.putBlankDocLine()
	else:
		&lt;&lt; append words to pending line, splitting the line if needed &gt;&gt;</t>
<t tx="T932">@ All inserted newlines are preceeded by whitespace:
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
	
	if leading + word3 - word1 + len(''.join(at.pending)) &gt;= at.page_width:
		if at.pending:
			# trace("splitting long line.")
			# Ouput the pending line, and start a new line.
			at.putPending(split=true)
			at.pending = [s[word2:word3]]
		else:
			# Output a long word on a line by itself.
			# trace("long word:",s[word2:word3])
			at.pending = [s[word2:word3]]
			at.putPending(split=true)
	else:
		# Append the entire word to the pending line.
		# trace("appending",s[word1:word3])
		at.pending.append(s[word1:word3])
			
# Output the remaining line: no more is left.
at.putPending(split=false)</t>
<t tx="T933">def putEndDocLine (self):
	
	"""Write the conclusion of a doc part."""
	
	at = self
	
	at.putPending(split=false)
	
	# Put the closing delimiter if we are using block comments.
	if at.endSentinelComment:
		at.putIndent(at.indent)
		at.os(at.endSentinelComment)
		at.onl() # Note: no trailing whitespace.

	sentinel = choose(at.docKind == at.docDirective,"@-doc","@-at")
	at.putSentinel(sentinel)</t>
<t tx="T934">def putPending (self,split):
	
	"""Write the pending part of a doc part.
	
	We retain trailing whitespace iff the split flag is true."""
	
	at = self ; s = ''.join(at.pending) ; at.pending = []
	
	# trace("split",`s`)
	
	# Remove trailing newline temporarily.  We'll add it back later.
	if s and s[-1] == '\n':
		s = s[:-1]

	if not split:
		s = s.rstrip()
		if not s:
			return

	at.putIndent(at.indent)

	if not at.endSentinelComment:
		at.os(at.startSentinelComment) ; at.oblank()

	at.os(s) ; at.onl()</t>
<t tx="T935"></t>
<t tx="T936">def findSectionName(self,s,i):
	
	end = s.find('\n',i)
	if end == -1:
		n1 = s.find("&lt;&lt;",i)
		n2 = s.find("&gt;&gt;",i)
	else:
		n1 = s.find("&lt;&lt;",i,end)
		n2 = s.find("&gt;&gt;",i,end)

	return -1 &lt; n1 &lt; n2, n1, n2</t>
<t tx="T937">def oblank(self):
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
<t tx="T938"># Returns the kind of at-directive or noDirective.

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
		("@others",at.othersDirective),
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
<t tx="T939"></t>
</tnodes>
</leo_file>
