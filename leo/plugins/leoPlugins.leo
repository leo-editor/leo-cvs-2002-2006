<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="291" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="65" left="188" height="791" width="1037"/>
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
<v t="T4"><vh>Intro to scripts</vh></v>
<v t="T5"><vh>About hooks</vh></v>
<v t="T6"><vh>Hooks should never blindly Python scripts</vh></v>
<v t="T7"><vh>NEVER use this kind of code in a hook!!</vh></v>
</v>
<v t="T8" a="E"><vh>Plugins</vh>
<v t="T9"><vh>Commands</vh>
<v t="T10"><vh> Importing Cisco configuration files</vh>
<v t="T11"><vh>@file import_cisco_config.py</vh>
<v t="T12"><vh>&lt;&lt; about this plugin &gt;&gt;</vh></v>
<v t="T13"><vh>create_import_cisco_menu</vh></v>
<v t="T14"><vh>importCiscoConfig</vh>
<v t="T15"><vh>&lt;&lt; open file &gt;&gt;</vh></v>
<v t="T16"><vh>&lt;&lt; process custom line &gt;&gt;</vh></v>
<v t="T17"><vh>&lt;&lt; process indented block &gt;&gt;</vh></v>
<v t="T18"><vh>&lt;&lt; complete outline &gt;&gt;</vh></v>
</v>
</v>
<v t="T19"><vh> Example of an imported config</vh>
<v t="T20"><vh>plain configuration</vh></v>
<v t="T21"><vh>cisco config: C:/Davide/Leo/CVS Version/example_conf.txt</vh>
<v t="T22"><vh>&lt;&lt;access-list&gt;&gt;</vh></v>
<v t="T23"><vh>&lt;&lt;boot&gt;&gt;</vh></v>
<v t="T24"><vh>&lt;&lt;controller&gt;&gt;</vh>
<v t="T25"><vh>controller E1 5/0/0</vh></v>
<v t="T26"><vh>controller E1 5/0/1</vh></v>
<v t="T27"><vh>controller SONET 1/0/0</vh></v>
</v>
<v t="T28"><vh>&lt;&lt;interface&gt;&gt;</vh>
<v t="T29"><vh>interface Async1</vh></v>
<v t="T30"><vh>interface Dialer0</vh></v>
<v t="T31"><vh>interface FastEthernet0/0/0</vh></v>
<v t="T32"><vh>interface FastEthernet0/0/1</vh></v>
<v t="T33"><vh>interface FastEthernet0/0/1.1</vh></v>
<v t="T34"><vh>interface FastEthernet0/0/1.2</vh></v>
<v t="T35"><vh>interface FastEthernet0/0/1.3</vh></v>
<v t="T36"><vh>interface FastEthernet0/0/1.5</vh></v>
<v t="T37"><vh>interface FastEthernet0/0/1.50</vh></v>
<v t="T38"><vh>interface Loopback0</vh></v>
<v t="T39"><vh>interface POS4/1/0</vh></v>
<v t="T40"><vh>interface Serial5/0/0:1</vh></v>
<v t="T41"><vh>interface Serial5/0/0:2</vh></v>
<v t="T42"><vh>interface Serial5/0/1:0</vh></v>
<v t="T43"><vh>interface Serial5/1/0</vh></v>
<v t="T44"><vh>interface Serial5/1/1</vh></v>
</v>
<v t="T45"><vh>&lt;&lt;ip community-list&gt;&gt;</vh></v>
<v t="T46"><vh>&lt;&lt;ip route&gt;&gt;</vh></v>
<v t="T47"><vh>&lt;&lt;line&gt;&gt;</vh>
<v t="T48"><vh>line aux 0</vh></v>
<v t="T49"><vh>line vty 0 4</vh></v>
</v>
<v t="T50"><vh>&lt;&lt;logging&gt;&gt;</vh></v>
<v t="T51"><vh>&lt;&lt;ntp&gt;&gt;</vh></v>
<v t="T52"><vh>&lt;&lt;route-map&gt;&gt;</vh>
<v t="T53"><vh>route-map only permit 2</vh></v>
<v t="T54"><vh>route-map only1 permit 10</vh></v>
<v t="T55"><vh>route-map only3 permit 10</vh></v>
<v t="T56"><vh>route-map tag_com permit 10</vh></v>
<v t="T57"><vh>route-map tag_com permit 20</vh></v>
</v>
<v t="T58"><vh>&lt;&lt;router&gt;&gt;</vh>
<v t="T59"><vh>router bgp 65001</vh></v>
<v t="T60"><vh>router ospf 1</vh></v>
</v>
<v t="T61"><vh>&lt;&lt;service&gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="T62"><vh> Spell Checking</vh>
<v t="T63"><vh>@silentfile mod_spelling.txt</vh></v>
<v t="T64"><vh>@file mod_spelling.ini</vh></v>
<v t="T65"><vh>@file mod_spelling.py</vh>
<v t="T66"><vh>Functions</vh>
<v t="T67"><vh>createSpellMenu</vh></v>
<v t="T68"><vh>onSelect</vh></v>
<v t="T69"><vh>onCommand</vh></v>
</v>
<v t="T70"><vh>class Aspell</vh>
<v t="T71"><vh>Birth &amp; death</vh>
<v t="T72"><vh>__init__</vh></v>
<v t="T73"><vh>getAspellDirectory</vh></v>
</v>
<v t="T74"><vh>openPipes</vh>
<v t="T75"><vh>&lt;&lt; Ensure local dictionary is present &gt;&gt;</vh></v>
</v>
<v t="T76"><vh>closePipes</vh></v>
<v t="T77"><vh>listAlternates</vh></v>
<v t="T78"><vh>processWord</vh></v>
<v t="T79"><vh>updateDictionary</vh></v>
</v>
<v t="T80"><vh>class spellDialog</vh>
<v t="T81"><vh>Birth &amp; death</vh>
<v t="T82"><vh>spell.__init__</vh>
<v t="T83"><vh>&lt;&lt; set self.dictionary &gt;&gt;</vh></v>
</v>
<v t="T84"><vh>getLocalDictionary</vh></v>
<v t="T85"><vh>getLocalLanguageCode</vh></v>
<v t="T86"><vh>readLocalDictionary</vh></v>
</v>
<v t="T87"><vh>createFrame</vh>
<v t="T88"><vh>&lt;&lt; Create the text and suggestion panes &gt;&gt;</vh></v>
<v t="T89"><vh>&lt;&lt; Create the spelling buttons &gt;&gt;</vh></v>
</v>
<v t="T90"><vh>Buttons</vh>
<v t="T91"><vh>onAddButton</vh></v>
<v t="T92"><vh>onIgnoreButton</vh></v>
<v t="T93"><vh>onChangeButton &amp; onChangeThenFindButton</vh></v>
<v t="T94"><vh>onFindButton</vh></v>
<v t="T95"><vh>onHideButton</vh></v>
<v t="T96"><vh>onRedoButton &amp; onUndoButton</vh></v>
</v>
<v t="T97"><vh>Commands</vh>
<v t="T98"><vh>add</vh></v>
<v t="T99"><vh>change</vh></v>
<v t="T100"><vh>checkSpelling</vh></v>
<v t="T101"><vh>find</vh></v>
<v t="T102"><vh>ignore</vh></v>
</v>
<v t="T103"><vh>Helpers</vh>
<v t="T104"><vh>closePipes</vh></v>
<v t="T105"><vh>fillbox</vh></v>
<v t="T106"><vh>findNextMisspelledWord</vh>
<v t="T107"><vh>&lt;&lt; Skip word if ignored or in local dictionary &gt;&gt;</vh></v>
</v>
<v t="T108"><vh>findNextWord</vh></v>
<v t="T109"><vh>getSuggestion</vh></v>
<v t="T110"><vh>onMap</vh></v>
<v t="T111"><vh>onSelectListBox</vh></v>
<v t="T112"><vh>update</vh></v>
<v t="T113"><vh>updateButtons</vh></v>
</v>
</v>
</v>
</v>
<v t="T114"><vh>@file outline_export.py</vh>
<v t="T115"><vh>newMoreHead</vh></v>
</v>
</v>
<v t="T116"><vh>Debugging</vh>
<v t="T117"><vh>@file dump_globals.py</vh>
<v t="T118"><vh>onStart</vh></v>
</v>
<v t="T119"><vh>@file enable_gc.py</vh>
<v t="T120"><vh>onStart</vh></v>
</v>
<v t="T121"><vh>@file trace_gc.py</vh></v>
<v t="T122"><vh>@file trace_keys.py</vh>
<v t="T123"><vh>onKey</vh></v>
</v>
<v t="T124"><vh>@file trace_tags.py</vh>
<v t="T125"><vh>trace_tags</vh></v>
</v>
</v>
<v t="T126"><vh>Directives</vh>
<v t="T127"><vh>@file add_directives.py</vh>
<v t="T128"><vh>addPluginDirectives</vh></v>
<v t="T129"><vh>scanPluginDirectives</vh></v>
</v>
</v>
<v t="T130"><vh>Drawing, graphics &amp; styled text</vh>
<v t="T131"><vh>@file color_markup.py</vh>
<v t="T132"><vh>initAnyMarkup</vh></v>
<v t="T133"><vh>colorWikiMarkup</vh></v>
<v t="T134"><vh>doWikiText</vh>
<v t="T135"><vh>&lt;&lt; set first to a tuple describing the first tag to be handled &gt;&gt;</vh></v>
<v t="T136"><vh>&lt;&lt; handle the tag using n1,n2,delim1,delim2 &gt;&gt;</vh>
<v t="T137"><vh>&lt;&lt; parse and handle color field &gt;&gt;</vh></v>
</v>
</v>
<v t="T138"><vh>insertWikiPicture</vh></v>
</v>
<v t="T139"><vh>@file image.py</vh>
<v t="T140"><vh>onSelect</vh>
<v t="T141"><vh>&lt;&lt; Select Image &gt;&gt;</vh></v>
</v>
<v t="T142"><vh>onUnselect</vh>
<v t="T143"><vh>&lt;&lt; Unselect Image &gt;&gt;</vh></v>
</v>
</v>
<v t="T144"><vh>@file nav_buttons.py</vh>
<v t="T145"><vh>&lt;&lt; globalInfoClass members &gt;&gt;</vh>
<v t="T146"><vh>__init__ ( globalInfoClass)</vh></v>
<v t="T147"><vh>addNavWidgets</vh></v>
<v t="T148"><vh>destroyFrame, destroyAllFrames, destroyOneFrame</vh></v>
<v t="T149"><vh>updateRecentSections</vh></v>
<v t="T150"><vh>updateMarks</vh></v>
<v t="T151"><vh>updateNavButtons</vh></v>
</v>
<v t="T152"><vh>&lt;&lt; commanderInfoClass members &gt;&gt;</vh>
<v t="T153"><vh>__init__ (commanderInfoClass)</vh></v>
<v t="T154"><vh>addWidgets</vh>
<v t="T155"><vh>&lt;&lt; define callbacks &gt;&gt;</vh></v>
</v>
<v t="T156"><vh>createImage</vh></v>
<v t="T157"><vh>updateNavButtons (nav_buttons.py)</vh></v>
<v t="T158"><vh>Callbacks</vh>
<v t="T159"><vh>marksButtonCallback</vh></v>
<v t="T160"><vh>recentButtonCallback</vh></v>
</v>
</v>
</v>
</v>
<v t="T161"><vh>External editors &amp; Open With</vh>
<v t="T162"><vh>@file open_with.py</vh>
<v t="T163"><vh>on_idle</vh>
<v t="T164"><vh>&lt;&lt; update v's body text &gt;&gt;</vh>
<v t="T165"><vh>&lt;&lt; set s to the file text &gt;&gt;</vh></v>
</v>
</v>
<v t="T166"><vh>create_open_with_menu</vh>
<v t="T167"><vh>&lt;&lt; create the Open With menu &gt;&gt;</vh></v>
</v>
</v>
<v t="T168"><vh>@file vim.py</vh>
<v t="T169"><vh>open_in_vim</vh></v>
</v>
<v t="T170"><vh>@file xemacs.py</vh></v>
</v>
<v t="T171" a="E"><vh>Files</vh>
<v t="T172"><vh>@file empty_leo_file.py</vh>
<v t="T173"><vh>&lt;&lt; define minimal .leo file &gt;&gt;</vh></v>
<v t="T174"><vh>onOpen</vh></v>
</v>
<v t="T175" a="V"><vh>@file open_shell.py</vh>
<v t="T176"><vh>&lt;&lt; about the open shell plugin &gt;&gt;</vh></v>
<v t="T177"><vh>load_menu</vh></v>
<v t="T178"><vh>_getpath</vh></v>
<v t="T179"><vh>_getcurrentnodepath</vh></v>
<v t="T180"><vh>launchCmd</vh></v>
<v t="T181"><vh>launchExplorer</vh></v>
<v t="T182"><vh>launchxTerm</vh></v>
</v>
</v>
<v t="T183"><vh>Foreign languages</vh>
<v t="T184"><vh>@file french.py</vh>
<v t="T185"><vh>onMenu</vh></v>
</v>
<v t="T186"><vh>@file french_fm.py</vh>
<v t="T187"><vh>onMenu</vh></v>
</v>
</v>
<v t="T188"><vh>Key bindings</vh>
<v t="T189"><vh>@file arrows.py</vh>
<v t="T190"><vh>onOpen</vh></v>
</v>
</v>
<v t="T191"><vh>Menus</vh>
<v t="T192"><vh> Plugins menu</vh>
<v t="T193"><vh>@file plugins_menu.py</vh>
<v t="T194"><vh>class Plugin</vh>
<v t="T195"><vh>__init__</vh>
<v t="T196"><vh>&lt;&lt; Check if this can be configured &gt;&gt;</vh></v>
<v t="T197"><vh>&lt;&lt; Check if this has an apply &gt;&gt;</vh></v>
<v t="T198"><vh>&lt;&lt; Look for additional commands &gt;&gt;</vh></v>
</v>
<v t="T199"><vh>about</vh></v>
<v t="T200"><vh>properties</vh></v>
</v>
<v t="T201"><vh>class PropertiesWindow</vh>
<v t="T202"><vh>__init__</vh>
<v t="T203"><vh>&lt;&lt; initialize all ivars &gt;&gt;</vh></v>
<v t="T204"><vh>&lt;&lt; create the frame from the configuration data &gt;&gt;</vh>
<v t="T205"><vh>&lt;&lt; Create the top level and the main frame &gt;&gt;</vh></v>
<v t="T206"><vh>&lt;&lt; Create widgets for each section and option &gt;&gt;</vh></v>
<v t="T207"><vh>&lt;&lt; Create Ok, Cancel and Apply buttons &gt;&gt;</vh></v>
</v>
</v>
<v t="T208"><vh>Event Handlers</vh></v>
<v t="T209"><vh>writeConfiguration</vh></v>
</v>
<v t="T210"><vh>class PluginAbout</vh>
<v t="T211"><vh>__init__</vh>
<v t="T212"><vh>&lt;&lt; Create the contents of the about box &gt;&gt;</vh></v>
<v t="T213"><vh>&lt;&lt; Create the close button &gt;&gt;</vh></v>
</v>
</v>
<v t="T214"><vh>createPluginsMenu</vh>
<v t="T215"><vh>&lt;&lt; add items to the plugins menu &gt;&gt;</vh></v>
</v>
</v>
<v t="T216"><vh>@file test.py</vh>
<v t="T217"><vh>applyConfiguration</vh></v>
<v t="T218"><vh>cmd_fn1/2/3</vh></v>
<v t="T219"><vh>onSelect</vh>
<v t="T220"><vh>&lt;&lt; Select Image &gt;&gt;</vh></v>
</v>
<v t="T221"><vh>onUnselect</vh>
<v t="T222"><vh>&lt;&lt; Unselect Image &gt;&gt;</vh></v>
</v>
</v>
<v t="T223"><vh>Notes re plugins menu</vh>
<v t="T224"><vh> Changes made by E.K.Ream</vh></v>
<v t="T225"><vh> Design</vh></v>
<v t="T226"><vh> Initial suggestion from Paul Paterson</vh></v>
</v>
</v>
<v t="T227"><vh>@file scripts_menu.py</vh>
<v t="T228"><vh>createScriptsMenu</vh>
<v t="T229"><vh>&lt;&lt; Return if no scripts exist anywhere &gt;&gt;</vh></v>
<v t="T230"><vh>&lt;&lt; Create top-level entries for every script in top_scripts &gt;&gt;</vh></v>
<v t="T231"><vh>&lt;&lt; Create a submenu for dir containing each file in files &gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="T232"><vh>New kinds of nodes</vh>
<v t="T233"><vh>@file at_folder.py</vh>
<v t="T234"><vh>&lt;&lt; about this plugin &gt;&gt;</vh></v>
<v t="T235"><vh>sync_node_to_folder</vh></v>
</v>
<v t="T236"><vh>@file read_only_nodes.py</vh>
<v t="T237"><vh>documentation for @read-only nodes</vh>
<v t="T238"><vh>ftp/http access</vh></v>
</v>
<v t="T239"><vh>class FTPurl</vh>
<v t="T240"><vh>__init__</vh></v>
<v t="T241"><vh>Getters</vh>
<v t="T242"><vh>read</vh></v>
<v t="T243"><vh>readline</vh></v>
</v>
<v t="T244"><vh>Setters</vh>
<v t="T245"><vh>write</vh></v>
</v>
<v t="T246"><vh>Utilities</vh>
<v t="T247"><vh>seek</vh></v>
<v t="T248"><vh>flush</vh></v>
<v t="T249"><vh>dir</vh></v>
<v t="T250"><vh>exists</vh></v>
<v t="T251"><vh>checkParams</vh></v>
</v>
<v t="T252"><vh>close</vh></v>
</v>
<v t="T253"><vh>enable/disable_body</vh></v>
<v t="T254"><vh>insert_read_only_node (FTP version)</vh>
<v t="T255"><vh>&lt;&lt; convert HTML to text &gt;&gt;</vh></v>
</v>
<v t="T256"><vh>on_open2</vh></v>
<v t="T257"><vh>on_bodykey1</vh></v>
<v t="T258"><vh>on_headkey2</vh></v>
<v t="T259"><vh>on_select1</vh></v>
<v t="T260"><vh>on_select2</vh></v>
</v>
<v t="T261"><vh>@file rst.py</vh>
<v t="T262"><vh>&lt;&lt;about this plugin &gt;&gt;</vh></v>
<v t="T263"><vh>&lt;&lt; change log &gt;&gt;</vh></v>
<v t="T264"><vh>onIconDoubleClick</vh>
<v t="T265"><vh>&lt;&lt; write rST as HTML &gt;&gt;</vh>
<v t="T266"><vh>&lt;&lt; convert rST to HTML &gt;&gt;</vh></v>
</v>
<v t="T267"><vh>&lt;&lt; write rST file &gt;&gt;</vh></v>
</v>
<v t="T268"><vh>writeTreeAsRst</vh></v>
<v t="T269"><vh>underline</vh></v>
</v>
<v t="T270"><vh>@file startfile.py</vh>
<v t="T271"><vh>&lt;&lt;about this plugin &gt;&gt;</vh></v>
<v t="T272"><vh>&lt;&lt; change log &gt;&gt;</vh></v>
<v t="T273"><vh>onIconDoubleClick</vh>
<v t="T274"><vh>&lt;&lt; find path and start file &gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="T275"><vh>Overriding functions, methods &amp; classes</vh>
<v t="T276"><vh>@file __overrideClasses.py</vh>
<v t="T277"><vh>&lt;&lt; override the LeoFrame class &gt;&gt;</vh></v>
<v t="T278"><vh>&lt;&lt; override methods of the LeoApp class &gt;&gt;</vh></v>
</v>
<v t="T279"><vh>@file override_commands.py</vh>
<v t="T280"><vh>onCommand</vh></v>
</v>
<v t="T281"><vh>@file redefine_put.py</vh>
<v t="T282"><vh>onStart</vh></v>
<v t="T283"><vh>newPut and newPutNl</vh></v>
</v>
<v t="T284"><vh>@file redirect_to_log.py</vh></v>
<v t="T285"><vh>@file script_io_to_body.py</vh>
<v t="T286"><vh>onStart</vh></v>
<v t="T287"><vh>newExecuteScript</vh></v>
<v t="T288"><vh>newPut and newPutNl</vh></v>
<v t="T289"><vh>newEs, etc.</vh></v>
</v>
</v>
</v>
<v t="T290" a="E"><vh>To do</vh>
<v t="T291" a="E"><vh>(Improve Spell Checking)</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="T1"></t>
<t tx="T2"></t>
<t tx="T3">@nocolor

This file contains code for all plugins distributed with Leo.</t>
<t tx="T4">@nocolor

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
<t tx="T5">At startup time Leo looks all files of the form mod_*.py in the plugins
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
<t tx="T6">Naively using hooks can expose you and your .leo files to malicious attacks.

** Hooks should never blindly execute Python scripts in .leo files.

It is safe to import and execute code from Leo itself, provided that you got Leo from Leo's SourceForge site.</t>
<t tx="T7">@color
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
<t tx="T8">@ It is usually best not to catch exceptions in plugins.  doHook catches all exceptions and disables further calls to plugins.
</t>
<t tx="T9"></t>
<t tx="T10"></t>
<t tx="T11">"""Import cisco configuration files"""

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
<t tx="T12">@ This plugin adds a menu item under the File-&gt;Import menu to import
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
<t tx="T13">def create_import_cisco_menu(tag, keywords):
	if	(tag=="open2" or
		(tag=="start2" and not keywords.has_key('c')) or
		(tag=="command2" and keywords.get("label")=="new")):

		c = top()
		importMenu = c.frame.getMenu('import')
		newEntries = (
			("-", None, None),
			("Import C&amp;isco Configuration", "Shift+Ctrl+I", importCiscoConfig))
		
		c.frame.createMenuEntries(importMenu, newEntries)</t>
<t tx="T14">def importCiscoConfig(event=None):
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
<t tx="T15">name = tkFileDialog.askopenfilename(
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
<t tx="T16">if not blocks.has_key(customLine):
	blocks[customLine] = []
	out.append(angleBrackets(customLine))
	# create first-level child
	child = v.insertAsNthChild(0)
	child.setHeadStringOrHeadline(angleBrackets(customLine))
	children.append(child)

blocks[customLine].append(linelist[i])</t>
<t tx="T17">space = linelist[i].find(' ')
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
<t tx="T18"># first print the level-0 text
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
<t tx="T19">@ignore
@language plain
@comment !
@ This node has an example of a flat configuration file (i.e. just the output of a 
'show running' command on a cisco router), and of the same configuration file 
imported by the plugin.
</t>
<t tx="T20">rpr1#sh runn    
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
<t tx="T21">rpr1#sh runn    
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
<t tx="T22">access-list 173 deny   ip 224.0.0.0 31.255.255.255 any
access-list 173 permit ip any any</t>
<t tx="T23">boot system flash rsp-k3pv-mz.120-21.S4.bin
boot system flash rsp-pv-mz.120-21.S1.bin
boot bootldr bootflash:rsp-boot-mz.120-11.S3</t>
<t tx="T24"></t>
<t tx="T25">controller E1 5/0/0
 framing NO-CRC4 
 clock source internal
 channel-group 1 timeslots 1
 channel-group 2 timeslots 2</t>
<t tx="T26">controller E1 5/0/1
 framing NO-CRC4 
 channel-group 0 timeslots 1</t>
<t tx="T27">controller SONET 1/0/0
 framing sdh</t>
<t tx="T28"></t>
<t tx="T29">interface Async1
 no ip address
 no ip directed-broadcast
 async mode interactive
 no peer default ip address</t>
<t tx="T30">interface Dialer0
 no ip address
 no ip directed-broadcast
 pulse-time 0
 no cdp enable</t>
<t tx="T31">interface FastEthernet0/0/0
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
<t tx="T32">interface FastEthernet0/0/1
 description **trunk link**
 no ip address
 no ip directed-broadcast
 no ip route-cache distributed
 no ip mroute-cache
 full-duplex</t>
<t tx="T33">interface FastEthernet0/0/1.1
 encapsulation dot1Q 25
 ip address 192.168.25.1 255.255.255.252
 no ip directed-broadcast</t>
<t tx="T34">interface FastEthernet0/0/1.2
 no ip directed-broadcast</t>
<t tx="T35">interface FastEthernet0/0/1.3
 encapsulation dot1Q 3
 ip address 192.168.4.1 255.255.255.252
 ip access-group 173 in
 no ip directed-broadcast
 ip pim sparse-mode</t>
<t tx="T36">interface FastEthernet0/0/1.5
 encapsulation dot1Q 5
 ip address 192.168.5.1 255.255.255.252
 no ip directed-broadcast</t>
<t tx="T37">interface FastEthernet0/0/1.50
 description to KPN-test
 encapsulation dot1Q 50
 ip address 192.168.40.1 255.255.255.252
 no ip directed-broadcast</t>
<t tx="T38">interface Loopback0
 ip address 192.168.20.1 255.255.255.255
 no ip directed-broadcast</t>
<t tx="T39">interface POS4/1/0
 no ip address
 no ip directed-broadcast
 no ip route-cache distributed
 no ip mroute-cache
 loopback internal</t>
<t tx="T40">interface Serial5/0/0:1
 ip address 10.31.9.1 255.255.255.252
 no ip directed-broadcast
 no ip route-cache distributed</t>
<t tx="T41">interface Serial5/0/0:2
 ip address 10.10.10.1 255.255.255.252
 no ip directed-broadcast
 no ip route-cache distributed</t>
<t tx="T42">interface Serial5/0/1:0
 ip address 10.31.9.5 255.255.255.252
 no ip directed-broadcast
 no ip route-cache distributed</t>
<t tx="T43">interface Serial5/1/0
 no ip address
 no ip directed-broadcast
 no ip route-cache distributed
 no ip mroute-cache
 shutdown
 framing g751
 dsu bandwidth 34010</t>
<t tx="T44">interface Serial5/1/1
 ip address 192.168.6.1 255.255.255.252
 no ip directed-broadcast
 encapsulation frame-relay IETF
 no ip route-cache distributed
 no ip mroute-cache
 loopback local
 framing g751
 dsu bandwidth 34010</t>
<t tx="T45">ip community-list 1 permit 65001:1
ip community-list 100 permit 65001:3</t>
<t tx="T46">ip route 0.0.0.0 0.0.0.0 192.168.3.2 tag 3</t>
<t tx="T47"></t>
<t tx="T48">line aux 0
 transport input all
 stopbits 1
 flowcontrol hardware</t>
<t tx="T49">line vty 0 4
 exec-timeout 0 0
 password 7 somepassword
 logging synchronous
 login
 length 0</t>
<t tx="T50">logging buffered 100000 debugging
logging facility local6
logging 10.10.10.1</t>
<t tx="T51">ntp clock-period 17179348
ntp update-calendar
ntp peer 192.168.3.2 prefer</t>
<t tx="T52"></t>
<t tx="T53">route-map only permit 2
 match community 65001:2
 set origin igp</t>
<t tx="T54">route-map only1 permit 10
 match community 1 65001:1
 set origin igp</t>
<t tx="T55">route-map only3 permit 10
 match community 100</t>
<t tx="T56">route-map tag_com permit 10
 match tag 1
 set community 65001:1</t>
<t tx="T57">route-map tag_com permit 20
 match tag 3
 set community 65001:3</t>
<t tx="T58"></t>
<t tx="T59">router bgp 65001
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
<t tx="T60">router ospf 1
 log-adjacency-changes
 passive-interface FastEthernet0/0/0
 network 192.168.3.1 0.0.0.0 area 0
 network 192.168.4.0 0.0.0.3 area 0</t>
<t tx="T61">no service pad
service timestamps debug datetime localtime show-timezone
service timestamps log datetime localtime show-timezone
service password-encryption
no service single-slot-reload-enable</t>
<t tx="T62"></t>
<t tx="T63">colour
colourful
coloured
</t>
<t tx="T64"># Configuration file for mod_spelling plugin.

[main]

aspell_dir=c:\aspell\bin\aspell.exe

local_leo_dictionary=c:\prog\leoCVS\leo\plugins\mod_spelling.txt

local_language_code=en</t>
<t tx="T65">"""Spell Checker Plugin

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
<t tx="T66"></t>
<t tx="T67">def createSpellMenu(tag,keywords):
	
	"""Create the Check Spelling menu item in the Edit menu."""
	
	c = keywords.get("c")

	table = (
		("-",None,None),
		("Check Spelling","Alt+Shift+A",spellFrame.checkSpelling))

	c.frame.createMenuItemsFromTable("Edit",table)</t>
<t tx="T68">def onSelect (tag,keywords):
	
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
<t tx="T69">def onCommand (tag,keywords):
	
	"""Update the Spell Check window after any command that might change text."""

	global spellFrame
	
	if top() and top().currentVnode():
		
		# print "onCommand",tag
		spellFrame.update(show=false,fill=false)</t>
<t tx="T70">class Aspell:
	
	"""A wrapper class for Aspell spell checker"""
	
	@others
</t>
<t tx="T71"></t>
<t tx="T72">def __init__(self,local_dictionary_file,local_language_code):
	
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
<t tx="T73">def getAspellDirectory(self):
	
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
<t tx="T74">def openPipes (self):
	
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
<t tx="T75">add_dicts = ""

if self.local_dictionary:
	if self.updateDictionary():
		add_dicts = "--add-extra-dicts %s" % self.local_dictionary


</t>
<t tx="T76">def closePipes (self):
	
	"""Close the pipes to aspell.exe"""
	
	# if self.input or self.output: print "closePipes"
	
	if self.input:
		self.input.close()
		self.input = None

	if self.output:
		self.output.close()
		self.output = None</t>
<t tx="T77">def listAlternates(self, aspell_return):
	
	"""Return a list of alternates from aspell."""
	
	match = self.altre.match(aspell_return)

	if match:
		return [item.strip() for item in match.groups()[3].split(",")]
	else:
		return []</t>
<t tx="T78">def processWord(self, word):

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
<t tx="T79">def updateDictionary(self):
	
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
<t tx="T80">class spellDialog (leoFind.leoFindBase):
	
	"""A class to create and manage Leo's Spell Check dialog."""
	
	@others</t>
<t tx="T81"></t>
<t tx="T82">def __init__ (self):
	
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
<t tx="T83">if self.local_dictionary_file:

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
<t tx="T84">def getLocalDictionary(self):
	
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
<t tx="T85">def getLocalLanguageCode(self,defaultLanguageCode):
	
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
<t tx="T86">def readLocalDictionary (self,local_dictionary):
	
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
<t tx="T87">def createFrame (self):
	
	"""Create the Spelling dialog."""
	
	# Create the find panel...
	outer = Tk.Frame(self.frame,relief="groove",bd=2)
	outer.pack(padx=2,pady=2,expand=1,fill="both")

	&lt;&lt; Create the text and suggestion panes &gt;&gt;
	&lt;&lt; Create the spelling buttons &gt;&gt;
</t>
<t tx="T88">f = outer

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
<t tx="T89"># Create the button panes
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
<t tx="T90"></t>
<t tx="T91">def onAddButton (self):
	
	"""Handle a click in the Add button in the Check Spelling dialog."""

	self.add()
	self.closePipes()

</t>
<t tx="T92">def onIgnoreButton (self):

	"""Handle a click in the Ignore button in the Check Spelling dialog."""

	self.ignore()
	self.closePipes()</t>
<t tx="T93">def onChangeButton (self):
	
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
<t tx="T94">def onFindButton (self):
	
	"""Handle a click in the Find button in the Check Spelling dialog."""

	self.find()
	self.updateButtons()
	self.closePipes()</t>
<t tx="T95">def onHideButton (self):
	
	"""Handle a click in the Hide button in the Check Spelling dialog."""

	self.closePipes()
	self.top.withdraw()
</t>
<t tx="T96">def onRedoButton (self):
	
	"""Handle a click in the Redo button in the Check Spelling dialog."""

	self.c.undoer.redo() # Not a command, so command hook doesn't fire.
	self.update(show=false,fill=false)
	self.c.frame.body.focus_force()
	
def onUndoButton (self):
	
	"""Handle a click in the Undo button in the Check Spelling dialog."""

	self.c.undoer.undo() # Not a command, so command hook doesn't fire.
	self.update(show=false,fill=false)
	self.c.frame.body.focus_force()</t>
<t tx="T97"></t>
<t tx="T98">def add (self):

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
<t tx="T99">def change(self):
	
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
<t tx="T100">def checkSpelling (self,event=None):
	
	"""Open the Check Spelling dialog."""

	self.top.deiconify()
	self.top.lift()
	self.update(show=true,fill=false)</t>
<t tx="T101">def find(self):
	
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
<t tx="T102">def ignore (self):
	
	"""Ignore the incorrect word for the duration of this spell check session."""
	
	es("Ignoring ",color="blue",newline=false) ; es('%s' % self.currentWord)
	self.dictionary[self.currentWord.lower()] = 0
	self.onFindButton()</t>
<t tx="T103"></t>
<t tx="T104">def closePipes(self):
	
	self.aspell.closePipes()</t>
<t tx="T105">def fillbox(self,alts,word=None):

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
<t tx="T106">def findNextMisspelledWord(self):
	
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
<t tx="T107">@ We don't bother to call apell if the word is in our dictionary. The dictionary contains both locally 'allowed' words and 'ignored' words. We put the test before aspell rather than after aspell because the cost of checking aspell is higher than the cost of checking our local dictionary. For small local dictionaries this is probably not true and this code could easily be located after the aspell call
@c

if self.dictionary.has_key(word.lower()):
	
	# print "Ignored", word
	continue
	
# print "Didn't ignore '%s'" % word</t>
<t tx="T108">def findNextWord (self,v):
	
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
<t tx="T109">def getSuggestion (self):
	
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
<t tx="T110">def onMap (self,event=None):
	
	"""Respond to a Tk &lt;Map&gt; event."""
	
	self.update(show=false,fill=false)</t>
<t tx="T111">def onSelectListBox (self,event=None):
	
	"""Respond to a click in the selection listBox."""
	
	self.updateButtons()
	self.body.focus_set()
</t>
<t tx="T112">def update (self,show=true,fill=false):
	
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
<t tx="T113">def updateButtons (self):
	
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
<t tx="T114">"""Modify the way exported outlines are displayed"""

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
<t tx="T115"># Returns the headline string in MORE format.

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
<t tx="T116"></t>
<t tx="T117">"""Dump globals at startup"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("start2", onStart)

	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T118">def onStart (tag,keywords):

	print "\nglobals..."
	for s in globals():
		if s not in __builtins__:
			print s
	
	print "\nlocals..."
	for s in locals():
		if s not in __builtins__:
			print s
</t>
<t tx="T119">"""Enable debugging for garbage collector"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("start2", onStart)
	
	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T120">def onStart (tag,keywords):

	try:
		import gc
		gc.set_debug(gc.DEBUG_LEAK)
	except: pass</t>
<t tx="T121">"""Trace changes to objects at idle time"""

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
<t tx="T122">"""Trace keystrokes in the outline and body panes"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler(("bodykey1","bodykey2","headkey1","headkey2"), onKey)
	
	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T123">def onKey (tag,keywords):

	ch = keywords.get("ch")
	if ch and len(ch) &gt; 0:
		es("key",`ch`)</t>
<t tx="T124">"""Trace most comment events, but not key, drag or idle events"""

from leoPlugins import *
from leoGlobals import *

tagCount = 0

@others

if 0: # Register the handlers...
	registerHandler("all", trace_tags)

	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)
</t>
<t tx="T125">def trace_tags (tag,keywords):

	# Almost all tags have both c and v keys in the keywords dict.
	if tag not in ("start1","end1","open1","open2"):
		c = keywords.get("c")
		v = keywords.get("v")
		if not c:
			print tag, "c = None"
		if not v:
			if tag not in ("select1","select2","unselect1","unselect2"):
				print tag, "v = None"
	
	if tag not in (
		"bodykey1","bodykey2","dragging1","dragging2",
		"headkey1","headkey2","idle"):
	
		global tagCount ; tagCount += 1 # Count all other hooks.
	
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
<t tx="T126"></t>
<t tx="T127">"""Support new @direcives"""

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
<t tx="T128">def addPluginDirectives (tag,keywords):
	
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
<t tx="T129">def scanPluginDirectives (tag, keywords):
	
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
<t tx="T130"></t>
<t tx="T131">"""Handle coloring for markup in doc parts and Python triple-double-quoted strings"""

from leoPlugins import *
from leoGlobals import *
import string  # zfill does not exist in Python 2.2.1

@others

if 1: # Register the handlers...

	registerHandler("color-optional-markup", colorWikiMarkup)
	registerHandler("init-color-markup", initAnyMarkup)

	__version__ = "1.1"
	plugin_signon(__name__)</t>
<t tx="T132">def initAnyMarkup (tag,keywords):
	
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
<t tx="T133">colorCount = 0

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
<t tx="T134">def doWikiText (colorer,v,s,i,end,colortag):

	firsti = i ; inserted = 0

	while i &lt; end:
		&lt;&lt; set first to a tuple describing the first tag to be handled &gt;&gt;
		if first:
			tag,n1,n2,delim1,delim2 = first
			i = n2 + len(delim2)
			&lt;&lt; handle the tag using n1,n2,delim1,delim2 &gt;&gt;
		else: i = end
		
	colorer.tag(colortag,firsti,end+inserted)</t>
<t tx="T135">first = None

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
<t tx="T136">if tag =="picture":
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
<t tx="T137"># Parse the color value.
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
<t tx="T138">def insertWikiPicture (colorer,filename,i):
	
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
<t tx="T139">"""Handle images in body text"""

from leoPlugins import *
from leoGlobals import *

@others

if 1: # Register the handlers...
	registerHandler("select2", onSelect)
	registerHandler("unselect1", onUnselect)
	
	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)
</t>
<t tx="T140">def onSelect (tag,keywords):

	import Tkinter,os

	new_v = keywords.get("new_v")
	h = new_v.headString()
	if h[:7] == "@image ":
		filename = h[7:]
		&lt;&lt; Select Image &gt;&gt;</t>
<t tx="T141"># Display the image file in the text pane, if you can find the file
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
<t tx="T142">def onUnselect (tag,keywords):

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
<t tx="T143"># Erase image if it was previously displayed
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
<t tx="T144">"""Adds navigation buttons to icon bar"""

from leoPlugins import *
from leoGlobals import *
import leoDialog
import os, Tkinter

class globalInfoClass:
	&lt;&lt; globalInfoClass members &gt;&gt;

class commanderInfoClass:
	&lt;&lt; commanderInfoClass members &gt;&gt;
	
globalInfo = globalInfoClass()

Tk = Tkinter

if 1: # Register the handlers...

	registerHandler("after-create-leo-frame", globalInfo.addNavWidgets)
	registerHandler("select2",globalInfo.updateRecentSections)
	registerHandler("command2",globalInfo.updateMarks)
	registerHandler("close-frame",globalInfo.destroyFrame)
	registerHandler("destroy-all-global-windows",globalInfo.destroyAllFrames)

	__version__ = "1.1"
	plugin_signon(__name__)</t>
<t tx="T145">@others</t>
<t tx="T146">def __init__ (self):
	
	self.commanderInfo = {} # keys are commanders, values are navCommanderInfo objects
</t>
<t tx="T147">def addNavWidgets(self,tag,keywords):
	
	c = keywords.get("c")
	
	# Create the commanderInfo object.
	d = commanderInfoClass(c,self)
	self.commanderInfo[c] = d
	
	# Add the widgets.
	d.addWidgets()
	
</t>
<t tx="T148">def destroyAllFrames(self,tag,keywords):
	
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
<t tx="T149">def updateRecentSections (self,tag,keywords):
	
	c = keywords.get("c")
	info = self.commanderInfo.get(c)

	if info:
		info.updateNavButtons()
		d = info.recentSectionsDialog
		if d:
			d.fillbox()
</t>
<t tx="T150">def updateMarks (self,tag,keywords):
	
	c = keywords.get("c")
	v = keywords.get("v")
	name = keywords.get("label")
	
	if name.lower() in ("mark","unmark","unmarkall",
		"marksubheads","markchangeditems","markclones"):

		info = self.commanderInfo.get(c)
		if info:
			d = info.marksDialog
			if d:
				d.fillbox()
</t>
<t tx="T151">def updateNavButtons (self,tag,keywords):

	"""Update the colors of c's nav buttons"""
	
	c = keywords.get("c")
	info = self.commanderInfo.get(c)
	
	if info:
		info.updateNavButtons()
</t>
<t tx="T152">@others</t>
<t tx="T153">def __init__ (self,c,globalInfo):
	
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
<t tx="T154">def addWidgets (self):
	
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
<t tx="T155"># These are functions, not methods, so we must bind self at definition time.

def onMarksButton(self=self):

	self.marksButtonCallback()
	
def onRecentButton(self=self):

	self.recentButtonCallback()</t>
<t tx="T156">def createImage (self,path):
	
	path = os.path.join(app().loadDir,path)
	path = os.path.normpath(path)
	
	try:
		image = Tkinter.PhotoImage(master=app().root,file=path)
	except:
		es("can not load icon: " + shortFileName(path))
		image = None
	return image

</t>
<t tx="T157">def updateNavButtons (self):	

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
<t tx="T158"></t>
<t tx="T159">def marksButtonCallback(self,event=None):
	
	c = self.c ; d = self.marksDialog

	if d:
		d.top.deiconify()
	else:
		# Create and run the dialog.
		title = "Marks"
		label = "Marks: " + shortFileName(c.frame.mFileName)
		d = leoDialog.marksDialog(c,title,label)
		self.marksDialog = d
		d.root.wait_window(d.top)
</t>
<t tx="T160">def recentButtonCallback(self,event=None):
	
	c = self.c ; d = self.recentSectionsDialog
	
	if d:
		d.top.deiconify()
		d.fillbox()
	else:
		# Create and run the dialog.]
		title = "Recent Nodes"
		label = "Recent nodes: " + shortFileName(c.frame.mFileName)
		d = leoDialog.recentSectionsDialog(c,self.nav_buttons,title,label)
		self.recentSectionsDialog = d
		d.root.wait_window(d.top)
</t>
<t tx="T161"></t>
<t tx="T162">"""Create menu for Open With command and handle the resulting commands"""

from leoPlugins import *
from leoGlobals import *

@others

if 1: # Register the handlers...

	app().hasOpenWithMenu = true
	registerHandler("idle", on_idle)
	registerHandler(("start2","open2","command2"), create_open_with_menu)

	__version__ = "1.4" # Set version for the plugin handler.
	plugin_signon(__name__)</t>
<t tx="T163"># frame.OnOpenWith creates the dict with the following entries:
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
<t tx="T164">&lt;&lt; set s to the file text &gt;&gt;

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
<t tx="T165">try:
	# Update v from the changed temp file.
	f=open(path)
	s=f.read()
	f.close()
except:
	es("can not open " + shortFileName(path))
	break
</t>
<t tx="T166">def create_open_with_menu (tag,keywords):

	if  (tag in ("start2","open2") or
		(tag=="command2" and keywords.get("label")=="new")):

		&lt;&lt; create the Open With menu &gt;&gt;
		# Enable the idle-time hook so we can check temp files created by Open With.
		from leoGlobals import enableIdleTimeHook
		enableIdleTimeHook(idleTimeDelay=500)
</t>
<t tx="T167">@ Entries in the following table are the tuple (commandName,shortcut,data).

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
<t tx="T168">"""vim handler"""

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
<t tx="T169">def open_in_vim (tag,keywords):
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
<t tx="T170">"""emacs handler"""

from leoPlugins import *
from leoGlobals import *

def open_in_emacs (tag,keywords):
	if top():
		top().frame.OnOpenWith(("os.spawnl", "/usr/bin/gnuclient", None),) # 6/27/03: add comma.

if 0: # Register the handlers...
	registerHandler(("iconclick2","select2"), open_in_emacs)
	
	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)</t>
<t tx="T171"></t>
<t tx="T172">"""Open any empty file as a minimal .leo file"""

from leoPlugins import *
from leoGlobals import *

&lt;&lt; define minimal .leo file &gt;&gt;
@others

if 0: # Register the handlers...
	registerHandler("open1", onOpen)
	
	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)</t>
<t tx="T173">empty_leo_file = """&lt;?xml version="1.0" encoding="iso-8859-1"?&gt;
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
<t tx="T174">def onOpen (tag,keywords):

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
<t tx="T175">@language python

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
<t tx="T176">@ Written by Ed Taekema.  Modified by E.K.Ream

Please submit bugs / feature requests to etaekema@earthlink.net"""

This is a simple plugin for leo 3.12 that allows the user to open either an xterm on linux or a cmd windows/explorer window on win32 in the directory of the current @file.  This allows quick navigation to facilitate testing and navigating large systems with complex direcgtories.

Current limitations ...

1. Not tested on Mac OS X ...
2. On win32, the cmd window will not open in the right directory if the @file location is on a different drive than the .leo file that is being edited.
3. On linux, xterm must be in your path.
</t>
<t tx="T177">def load_menu(tag,keywords):
	
	if sys.platform=="win32":
		table = (
			("&amp;Open Console Window",None,launchCmd),
			("Open &amp;Explorer",None,launchExplorer)) 
	else:
		table = ( ("Open &amp;xterm",None,launchxTerm), ) 
	
	top().frame.createNewMenu("E&amp;xtensions","top")
	top().frame.createMenuItemsFromTable("Extensions",table)
</t>
<t tx="T178">def _getpath(c,v):
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
<t tx="T179">def _getCurrentNodePath():
	c = leo.top()
	v = c.currentVnode()
	f = v.atFileNodeName()
	d = _getpath(c,v)
	return d
</t>
<t tx="T180">def launchCmd(not_used):
	
	global pathToCmd

	d = _getCurrentNodePath()
	myCmd = 'cd ' + d
	os.spawnl(os.P_NOWAIT, pathToCmd, '/k ', myCmd)</t>
<t tx="T181">def launchExplorer(not_used):
	
	global pathToExplorer

	d = _getCurrentNodePath()
	os.spawnl(os.P_NOWAIT,pathToExplorer, ' ', d)

</t>
<t tx="T182">def launchxTerm(not_used):

	d = _getCurrentNodePath()
	curdir = os.getcwd()
	os.chdir(d)
	os.spawnlp(os.P_NOWAIT, 'xterm', '-title Leo')
	os.chdir(curdir)</t>
<t tx="T183"></t>
<t tx="T184">"""Translate a few menu items into French"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler(("start1","menu1"), onMenu)
	
	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T185">@ The translation table used by setRealMenuNamesFromTable has entries of the form:

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
<t tx="T186">@language python

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
<t tx="T187">def onMenu (tag,keywords):
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
<t tx="T188"></t>
<t tx="T189">"""Rebind up/down arrow keys"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("open2", onOpen)
	
	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)
</t>
<t tx="T190"># Warning: the bindings created this way conflict with shift-arrow keys.

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
<t tx="T191"></t>
<t tx="T192"></t>
<t tx="T193">"""Create a Plugins menu"""

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
<t tx="T194">class PlugIn:

	"""A class to hold information about one plugin"""

	@others
	
</t>
<t tx="T195">def __init__(self, filename):

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
<t tx="T196"># Look for a configuration file
self.configfilename = "%s.ini" % os.path.splitext(filename)[0]
self.hasconfig = os.path.isfile(self.configfilename)
</t>
<t tx="T197">@ Look for an apply function ("applyConfiguration") in the module.

This is used to apply changes in configuration from the properties window
@c

self.hasapply = hasattr(self.mod, "applyConfiguration")
</t>
<t tx="T198">@ Additional commands can be added to the plugin menu by having functions in the module called "cmd_whatever". These are added to the main menu and will be called when clicked
@c

self.othercmds = {}

for item in self.mod.__dict__.keys():
	if item.startswith("cmd_"):
		self.othercmds[item[4:]] = self.mod.__dict__[item]
</t>
<t tx="T199">def about(self, arg):
	
	"""Put up an "about" dialog for this plugin"""

	PluginAbout(self.name, self.version, self.doc)</t>
<t tx="T200">def properties(self, arg):
	
	"""Create a modal properties dialog for this plugin"""

	PropertiesWindow(self.configfilename, self)
</t>
<t tx="T201">class PropertiesWindow:

	"""A class to create and run a Properties dialog for a plugin"""

	@others</t>
<t tx="T202">def __init__(self, filename, plugin):

	"""Initialize the property window"""
	
	&lt;&lt; initialize all ivars &gt;&gt;
	&lt;&lt; create the frame from the configuration data &gt;&gt;</t>
<t tx="T203"># config stuff.
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
<t tx="T204">root = app().root

&lt;&lt; Create the top level and the main frame &gt;&gt;
&lt;&lt; Create widgets for each section and option &gt;&gt;
&lt;&lt; Create Ok, Cancel and Apply buttons &gt;&gt;

center_dialog(top) # Do this after packing.
top.grab_set() # Make the dialog a modal dialog.
top.focus_force() # Get all keystrokes.
root.wait_window(top)</t>
<t tx="T205">self.top = top = Tk.Toplevel(root)
attachLeoIcon(self.top)
top.title("Properties of "+ plugin.name)
top.resizable(0,0) # neither height or width is resizable.
	
self.frame = frame = Tk.Frame(top)
frame.pack(side="top")</t>
<t tx="T206"># Create all the entry boxes on the screen to allow the user to edit the properties
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
<t tx="T207">box = Tk.Frame(top, borderwidth=5)
box.pack(side="bottom")

list = [("OK",self.onOk),("Cancel",top.destroy)]
if plugin.hasapply:
	list.append(("Apply",self.onApply),)

for text,f in list:
	Tk.Button(box,text=text,width=6,command=f).pack(side="left",padx=5)</t>
<t tx="T208">def onApply(self):
	
	"""Event handler for Apply button"""
	self.writeConfiguration()
	self.plugin.mod.applyConfiguration(self.config)

def onOk(self):

	"""Event handler for Ok button"""
	self.writeConfiguration()
	self.top.destroy()</t>
<t tx="T209">def writeConfiguration(self):
	
	"""Write the configuration to disk"""

	# Set values back into the config item.
	for section, option, entry in self.entries:
		self.config.set(section, option, entry.get())

	# Write out to the file.
	f = open(self.filename, "w")
	self.config.write(f)
	f.close()
</t>
<t tx="T210">class PluginAbout:
	
	"""A class to create and run an About Plugin dialog"""
	
	@others
</t>
<t tx="T211">def __init__(self, name, version, about):
	
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
<t tx="T212">if 0: # The name is now in the window's title.
	Tk.Label(frame, text="Name:").grid(row=0, col=0, sticky="E")
	Tk.Label(frame, text=name).grid(row=0, col=1, sticky="W")
	Tk.Label(frame, text="Version").grid(row=1, col=0, sticky="E")
	Tk.Label(frame, text=version).grid(row=1, col=1, sticky="W")
	Tk.Label(frame, text=about, borderwidth=10, justify="left").grid(columnspan=2)
else:
	Tk.Label(frame, text="Version " + version).pack()
	Tk.Label(frame, text=about, borderwidth=10).pack()</t>
<t tx="T213">buttonbox = Tk.Frame(top, borderwidth=5)
buttonbox.pack(side="bottom")

self.button = Tk.Button(buttonbox, text="Close", command=top.destroy)
self.button.pack(side="bottom")</t>
<t tx="T214">def createPluginsMenu (tag,keywords):

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
<t tx="T215">for name,p in items:
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
<t tx="T216">@ignore
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
<t tx="T217">def applyConfiguration(config):
	
	sections = config.sections()
	sections.sort()

	for section in sections:
		options = config.options(section)
		options.sort()
		for option in options:
			print section, option, config.get(section, option)
</t>
<t tx="T218">def cmd_fn1(x):
	es("Fn1",color="blue")

def cmd_fn2(x):
	es("Fn2",color="blue")

def cmd_fn3(x):
	es("Fn3",color="blue")
</t>
<t tx="T219">def onSelect (tag,keywords):

	import Tkinter,os

	new_v = keywords.get("new_v")
	h = new_v.headString()
	if h[:7] == "@image ":
		filename = h[7:]
		&lt;&lt; Select Image &gt;&gt;</t>
<t tx="T220"># Display the image file in the text pane, if you can find the file
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
<t tx="T221">def onUnselect (tag,keywords):

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
<t tx="T222"># Erase image if it was previously displayed
if a.gsimage:
	try:
		 c.frame.body.delete(a.gsimage)
	except:
		es("info: no image to erase")

# And forget about it
a.gsimage = None
a.gsphoto = None
</t>
<t tx="T223">@nocolor</t>
<t tx="T224">Reorganized the code so I can find various classes more easily.
Used @others to simply the outline.

Sorted all entries in dialogs.
Sorted all entries in Plugins menu, regardless of whether they are configurable.

For all dialogs:
	Added top ivar and removed root/master params and ivars.
	Added Leo icon and title.
	Centered dialogs.

Ctors now run all dialogs as modal dialogs: this could easily be undone.

Used a grid in the properties dialog to align widgets.</t>
<t tx="T225">- We will use a new settings file called leoSettings.txt:
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
<t tx="T226">I wrote myself a plug-in which would automatically save the Leo file every so often and in doing so realized that it would be useful to be able to configure the interval between saves. Anyway, to cut a long story short, I generalized the idea and came up with the attached patch. 
 
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
<t tx="T227">"""Create a Scripts menu for LeoPy.leo"""

from leoPlugins import *
from leoGlobals import *
import glob,os

@others

if 1: # Register the handlers...
	registerHandler("create-optional-menus",createScriptsMenu)
	
	__version__ = "1.4"
	plugin_signon(__name__)</t>
<t tx="T228">def createScriptsMenu (tag,keywords):

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
<t tx="T229">if not top_scripts:
	found = false
	for dir in dirs:
		scripts = glob.glob(os.path.join(dir,"*.py"))
		if scripts:
			found = true ; break
	if not found:
		return
</t>
<t tx="T230">table = []
top_scripts.sort()
for script in top_scripts:
	name = shortFileName(script)
	def doScript(event=None,name=name):
		executeScript(name)
	table.append((name,None,doScript),)
	
c.frame.createMenuEntries(scriptsMenu, table)
</t>
<t tx="T231"># Create the submenu.
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
<t tx="T232"></t>
<t tx="T233">"""Synchronize @folder nodes with folders"""

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
<t tx="T234">@ If a node is named '@folder path_to_folder', the content (filenames) of the
folder and the children of that node will be sync. Whenever a new file is put
there, a new node will appear on top of the children list (with mark). So that
I can put my description (ie. annotation) as the content of that node. In this
way, I can find any files much easier from leo.

Moreover, I add another feature to allow you to group files(in leo) into
children of another group. This will help when there are many files in that
folder. You can logically group it in leo (or even clone it to many groups),
while keep every files in a flat/single directory on your computer.
</t>
<t tx="T235">def sync_node_to_folder(parent,d):

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
<t tx="T236">"""Inhibit changes to @read-only nodes"""

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
<t tx="T237">@ Dear Leo users,

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
<t tx="T238">@ The syntax to access files in @read-only via ftp/http is the following:

@read-only http://www.ietf.org/rfc/rfc0791.txt
@read-only ftp://ftp.someserver.org/filepath

If FTP authentication (username/password) is required, it can be specified as follows:

@read-only ftp://username:password@ftp.someserver.org/filepath

For more details, see the doc string for the class FTPurl.
</t>
<t tx="T239">class FTPurl:
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
<t tx="T240">def __init__(self, ftpURL, mode=''):
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
<t tx="T241"></t>
<t tx="T242">def read(self):
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
<t tx="T243">def readline(self):
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
<t tx="T244"></t>
<t tx="T245">def write(self, s):
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
<t tx="T246"></t>
<t tx="T247">def seek(offset=0):
	self.currentLine = 0  # we don't support fancy seeking via FTP
</t>
<t tx="T248">def flush():
	pass # no fancy stuff here.</t>
<t tx="T249">def dir(self, path=None):
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
<t tx="T250">def exists(self, path=None):
	"""Return 1 if the specified path exists. If path is omitted, the current file name is tried."""
	if path == None:
		path = self.filename

	s = self.dir(path)
	if s.lower().find('no such file') == -1:
		return 1
	else:
		return 0
</t>
<t tx="T251">def checkParams(self):
	if self.mode not in ('','b'):
		raise IOError, 'invalid mode: %s' % self.mode
	if not self.isConnectionOpen:
		raise IOError, 'ftp connection closed'
</t>
<t tx="T252">def close(self):
	"""Close an existing FTPurl connection."""
	try:
		self.ftp.quit()
	except:
		self.ftp.close()
	del self.ftp
	self.isConnectionOpen = 0</t>
<t tx="T253"># Alas, these do not seem to work on XP:
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
<t tx="T254"># Sets v's body text from the file with the given name.
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
<t tx="T255">fh = cStringIO.StringIO()
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
<t tx="T256">#  scan the outline and process @read-only nodes.
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
<t tx="T257"># override the body key handler if we are in an @read-only node.

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
<t tx="T258"># update the body text when we press enter

def on_headkey2 (tag,keywords):

	c = keywords.get("c")
	v = keywords.get("v")
	h = v.headString()
	ch = keywords.get("ch")
	if ch == '\r' and match_word(h,0,"@read-only"):
		# on-the-fly update of @read-only directives
		changed = insert_read_only_node(c,v,h[11:])
		c.setChanged(changed)</t>
<t tx="T259">def on_select1 (tag,keywords):

	# Doesn't work: the cursor doesn't start blinking.
	# Enable the body text so select will work properly.
	c = keywords.get("c")
	enable_body(c.frame.body)
</t>
<t tx="T260">def on_select2 (tag,keywords):

	c = keywords.get("c")
	v = c.currentVnode()
	h = v.headString()
	if match_word(h,0,"@read-only"):
		disable_body(c.frame.body)
	else:
		enable_body(c.frame.body)
</t>
<t tx="T261">"""If a headline starts with @rst &lt;filename&gt;, double-clicking on it will 
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
<t tx="T262">@ This plugin writes out @rst nodes as a reStructuredText file.

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
<t tx="T263">@ Change log:

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
<t tx="T264"># by Josef Dalcolmo 2003-01-13
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
<t tx="T265">try:
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
<t tx="T266"># this code snipped has been taken from code contributed by Paul Paterson 2002-12-05
from docutils.core import Publisher
from docutils.io import StringOutput, StringInput

pub = Publisher()
# Initialize the publisher
pub.source = StringInput(pub.settings, source=rstText)
pub.destination = StringOutput(pub.settings, encoding="utf-8")
pub.set_reader('standalone', None, 'restructuredtext')
pub.set_writer('html')
output = pub.publish()</t>
<t tx="T267">rstFile = file(fname,'w')
writeTreeAsRst(rstFile, fname, v, commands)
rstFile.close()
es('written: '+`fname`)</t>
<t tx="T268">def writeTreeAsRst(rstFile, fname, vnode, commands):
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
<t tx="T269"># note the first character is intentionally unused, to serve as the underline
# character in a title (in the body of the @rst node)
def underline(h,level):
	str = """#=+*^~"'`-:&gt;&lt;_"""[level]
	return str*max(len(h),4)+'\n'</t>
<t tx="T270">"""Lauches (starts) a file with the name of the headline on double-clicking it.
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
<t tx="T271">@ This plugin starts a file with the name of a headline.


</t>
<t tx="T272">@ Change log

- JD: 2003-03-11 separated out from rst plugin



</t>
<t tx="T273"># @folder behavior after an idea and sample code by:
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
<t tx="T274"># Set the base directory by searching for @folder directives in ancestors.
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
<t tx="T275"></t>
<t tx="T276">from leoPlugins import *
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
<t tx="T277"># print "overriding LeoFrame class"

import leoFrame

assert(leoFrame.leoCoreFrame.instances==0)

class myLeoFrame(leoFrame.leoCoreFrame):
	
	pass
	
	if 0:
		def __init__(self,title=None):
			print "myLeoFrame ctor",title
			leoFrame.leoCoreFrame.__init__(self,title)

leoFrame.LeoFrame = myLeoFrame</t>
<t tx="T278">import leoApp

# print "overriding app.closeLeoWindow"

oldAppCloseLeoWindow = app().closeLeoWindow

def myAppCloseLeoWindow(self,frame):
	
	global oldAppCloseLeoWindow

	oldAppCloseLeoWindow(frame)
	print "after closeLeoWindow"

funcToMethod(myAppCloseLeoWindow,leoApp.LeoApp,"closeLeoWindow")</t>
<t tx="T279">"""Override the Equal Sized Pane command"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("command1", onCommand)
	
	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T280">def onCommand (tag,keywords):

	if keywords.get("label")=="equalsizedpanes":
		es("over-riding Equal Sized Panes")
		return "override" # Anything other than None overrides.</t>
<t tx="T281">"""Redefine the "put" and "put_nl" methods"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("start2", onStart)
	
	__version__ = "1.2"
	plugin_signon(__name__)</t>
<t tx="T282">@ This code illustrates how to redefine _any_ method of Leo.
Python makes this is almost too easy :-)
@c

def onStart (tag,keywords):

	import leoFrame
	
	# Replace frame.put with newPut.
	funcToMethod(newPut,leoFrame.LeoFrame,"put")
	
	# Replace frame.putnl with newPutNl.
	funcToMethod(newPutNl,leoFrame.LeoFrame,"putnl")
</t>
<t tx="T283"># Contrived examples of how to redefine frame.put and frame.putnl

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
<t tx="T284">"""Send all output to the log pane"""

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
<t tx="T285">"""Send output from the Execute Script command to the end of the body pane"""

from leoPlugins import *
from leoGlobals import *

@others

if 0: # Register the handlers...
	registerHandler("start1", onStart)

	__version__ = "1.2" # Set version for the plugin handler.
	plugin_signon(__name__)
</t>
<t tx="T286">def onStart (tag,keywords):
	
	import leoFrame
	
	# Replace frame.put with newPut.
	funcToMethod(newExecuteScript,leoFrame.LeoFrame,"OnExecuteScript")
</t>
<t tx="T287"># Execute the _selected_ body text as a Python script and sends the output to the end of the body pane.

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
<t tx="T288"># Same as frame.put except sends output to the end of the body text.
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
<t tx="T289">def newEnl():
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
<t tx="T290">@nocolor</t>
<t tx="T291">- (done) Make sure the selected node is visible.
- (done) Force the focus to the body pane after undo/redo so the selection is visible.

- Bind Fkeys to buttons.
- Is there a problem with "__init__" ?
- words like "and" aren't in the dictionary?????
</t>
</tnodes>
</leo_file>
