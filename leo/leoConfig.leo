<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet ekr_stylesheet?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="23" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="9" left="92" height="25" width="96"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences allow_rich_text="0">
</preferences>
<find_panel_settings>
	<find_string></find_string>
	<change_string></change_string>
</find_panel_settings>
<vnodes>
<v t="T1" a="E"><vh>leoConfig.leo</vh>
<v t="T2" a="EV"><vh>@root leoConfig.txt</vh>
<v t="T3"><vh>&lt;&lt; general comments and warnings &gt;&gt;</vh></v>
<v t="T4"><vh>&lt;&lt; General configuration options, especially read-only mode &gt;&gt;</vh></v>
<v t="T5"><vh>&lt;&lt; The "Recent Files" menu &gt;&gt;</vh></v>
<v t="T6"><vh>&lt;&lt; Compare Panel settings &gt;&gt;</vh></v>
<v t="T7"><vh>&lt;&lt; Find/Change Panel settings &gt;&gt;</vh></v>
<v t="T8"><vh>&lt;&lt; Keyboard shortcuts settings &gt;&gt;</vh>
<v t="T9"><vh>&lt;&lt; About keyboard shortcuts &gt;&gt;</vh></v>
<v t="T10"><vh>&lt;&lt; Alt and Shift-Alt&gt;&gt;</vh></v>
<v t="T11"><vh>&lt;&lt; Control &gt;&gt;</vh></v>
<v t="T12"><vh>&lt;&lt; Shift-Control &gt;&gt;</vh></v>
<v t="T13"><vh>&lt;&lt; F-keys and others &gt;&gt;</vh></v>
<v t="T14"><vh>&lt;&lt; None &gt;&gt;</vh></v>
</v>
<v t="T15"><vh>&lt;&lt; Preferences Panel settings &gt;&gt;</vh></v>
<v t="T16"><vh>&lt;&lt; Syntax coloring options and colors &gt;&gt;</vh></v>
<v t="T17"><vh>&lt;&lt; Window options &gt;&gt;</vh>
<v t="T18"><vh>&lt;&lt; body pane options &gt;&gt;</vh></v>
<v t="T19"><vh>&lt;&lt; outline pane options&gt;&gt;</vh></v>
<v t="T20"><vh>&lt;&lt; log pane options &gt;&gt;</vh></v>
<v t="T21"><vh>&lt;&lt; Options for new windows &gt;&gt;</vh></v>
<v t="T22"><vh>&lt;&lt; Options for newly opened windows &gt;&gt;</vh></v>
<v t="T23"><vh>&lt;&lt; Options for the bar that separates panes in the Leo window &gt;&gt;</vh></v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="T1">@nocolor

This is the file that creates leoConfig.txt.  We use this file for two reasons:
	
1. It is easier to update this file than a large text file.

2. When read_only = 0, all comments are lost in Leo updates leoConfig.txt, so using this file is a way of keeping these comments.

Note: using @rawfile here would not be so useful, because we would have to remember to do a "Write @file Nodes" command to update leoConfig.txt anyway.

@color</t>
<t tx="T2">@comment #
@ We use an @root node here to suppress automatic untangling, so we don't lose all these nice comments in read-write mode.
@root-code leoConfig.txt

# leoConfig.txt: configuration file for Leo.
# 12/03/2002 by Edward K. Ream

&lt;&lt; general comments and warnings &gt;&gt;

# WARNING: !! Do not place anything except comments before here !!

&lt;&lt; General configuration options, especially read-only mode &gt;&gt;
&lt;&lt; The "Recent Files" menu &gt;&gt;
&lt;&lt; Compare Panel settings &gt;&gt;
&lt;&lt; Find/Change Panel settings &gt;&gt;
&lt;&lt; Keyboard shortcuts settings &gt;&gt;
&lt;&lt; Preferences Panel settings &gt;&gt;
&lt;&lt; Syntax coloring options and colors &gt;&gt;
&lt;&lt; Window options &gt;&gt;
</t>
<t tx="T3">@ Leo looks for this file using the directory in sys.leo_config_directory.
(You would typically set this attribute in sitecustomize.py).
If sys.leo_config_directory does not exist,
Leo attempts to load this file from the directory from which Leo was loaded.

Leo writes settings to the &lt;preferences&gt; and &lt;find_panel_settings&gt;
elements of .leo files if this file does not exist or is read-only.

Leo uses Python's ConfigParser module to parse this file,
with all of ConfigParser's features (and bugs!).

Comments start with a pound character in the leftmost column.
You may specify booleans as 0/1, no/yes, false/true, off/on (case insensitive).
These get converted to 0/1 if the file is not read_only.</t>
<t tx="T4">[config options]

at_root_bodies_start_in_doc_mode = 1

#	1: Body text in @root trees start in doc mode.
#	   (This is the way @root trees always worked prior to version 3.10.)
#	0: Body text in @root trees start in code mode.
#      (This way makes @root trees more compatible with @file trees.)

create_nonexistent_directories = 0
#	1: Leo attempts to create directories if they do not exist.
#	0: Leo never attempts to create directories
#	This option applies to directories specified in filenames in
#	@file, @rawfile, @root and @silentfile trees, and to filenames
#	speicied in the @path directory.

output_initial_comment =
#	Example:
#		Created by Leo at @date
#	A comment to be iserted in derived files just after the initial @+leo line.
#	The comment will appear in an @comment sentinel.
#	Notes:
#	1. Leo replaces @date with the date and time that the derived file was created.
#	2. Use \n to separate lines.
#	3. This must be empty for compatibility with older versions of Leo.
#	4. Please use an empty comment when updating to CVS!

output_newline = nl
#	Valid values for this option:
#	nl or lf:  The default: all lines end with "\n"
#	cr:	 All lines end with "\r"
#	crlf:	All lines end with "\r\n"
#	platform: Lines end in platform-specific way, i.e.,
#	Leo opens output files in "w" mode rather than "wb" mode and writes '\n'
#
#	Please specify nl when uploading files to Leo's CVS site.

read_only = 0
#	0: Leo writes this file, clearing all comments in the process.
#	1: Leo writes nothing to this file.
#	Syntax errors in this file set this file to read-only.

relative_path_base_directory = .
#	The directory to be used as a prefix for &lt;filename&gt; in
#	@path &lt;filename&gt; and @file &lt;filename&gt; and @root &lt;filename&gt;
#	when &lt;filename&gt; is a relative path.
#
#	Valid values for this option:
#		"!" means relative to the location leo.py (the default).
#		"." means relative to the location of the .leo file in the top window.
#		An absolute path (in platform-dependent format).
#
#	Relative paths are not allowed:
#		Relative paths would be dangerous because their meaning
#		would depend on the changing value of the current working directory.

remove_sentinels_extension = .txt
#	The string to be appended to file names resulting from the Remove Sentinels command.
#	If the value starts with . the extension is appended to the original file name.
#	Otherwise, the extension is appended before the file extension.
#	Example 1:
#		File name x.y
#		remove_sentinels_extension = _ns
#		Result: x_ns.y
#	Example 2:
#		File name x.y
#		remove_sentinels_extension = .txt
#		Result: x.y.txt

save_clears_undo_buffer = 0
#	1: Save command clears undo buffer.
#	0: Undo buffer persists across saves.

stylesheet =
#	A string, s.  If present, .leo files will contain an xml-stylesheet line following
#	the opening xml line. 
#	For example:
#		&lt;?xml ....?&gt; 
#		&lt;?xml-stylesheet s?&gt;
#	Note 1: The string s should contain any needed XML escapes.
#	        Leo simply copies this line as given.
#	Note 2: Please set this field empty when uploading to CVS.
#	Note 3: This field must be empty for compatibility with older versions of Leo.

use_customizeLeo_dot_py = 1

#	1: Leo calls code "hooks" in configureLeo.py.
#      Naive or hostile hooks may execute HOSTILE CODE contained in .leo files.
#   0: (The default) Leo calls NO hooks in configureLeo.py.
#
#	Very important SECURITY WARNINGS:
#
#   - Setting use_configureLeo_dot_py = 1 enables user code that could,
#     if not well thought out, create SECURITY ISSUES.
#     See the warnings in the @file configureLeo.py node in LeoPy.py.
#	- Neither leoConfigure.leo nor leoConfigure.txt
#	  should EVER be distributed with use_configureLeo_dot_py = 1
#     Please report such distributions to me, Edward K. Ream.
#   - Distributing any copy of configureLeo.py should be considered a HOSTILE ACT.
#	  Please report anyone that distributes configureLeo.py to me.
#	  At no time should an authentic Leo distribution ever contain configureLeo.py.
#	  Please report any such distributions to me.

use_relative_node_indices = 0
#	At present this user option is non-functional.
#	1: Files derived from @file nodes use relative node indices.
#	0: Files derived from @file nodes use absolute node indices.
#	Please specify 1 if you are going to submit files to Leo's CVS site.

write_clone_indices = 0
#	1: Files derived from @file nodes contain clone indices.
#	0: Files derived from @file nodes contain no clone indices.
#	Please specify 0 if you are going to submit files to Leo's CVS site.

xml_version_string = UTF-8
#	The version used at the start of .leo files.
#	Default is UTF-8.  Better may be iso-8859-1 or iso-8859-15.
#	Important:  Use UTF-8 (case is significant) to write leo.py 2.x files.
</t>
<t tx="T5"># The list of files in the "Recent Files" menu at startup.

[recent files]

# file2 = c:\prog\leocvs\leo\leoConfig.leo
# file1 = c:\prog\leocvs\leo\leodocs.leo
# file0 = c:\prog\leocvs\leo\leopy.leo

#	Paths to recent files.
#	Valid option names: file0 through file9.</t>
<t tx="T6"># 	These correspond to the keyword parameters of the leoCompare constructor.
# 	Exception: there are no keywords for compare file names in the constructor.

[compare options]

# ----- Options specifying files for the Compare panel.

compare_file_1 = c:/prog/test/compareTest1/file1.txt
#	Path to the first file or directory to be compared.
#	Directory compares ignore a filename part of the path, if present.
#	E.g., c:/directory1/spam.py is valid for directory compares.

compare_file_2 = c:/prog/test/compareTest2/file2.txt
#	Path to the second file or directory to be compared.
#	Directory compares ignore a filename part of the path, if present.
#	E.g., c:/directory2/spam.py is valid for directory compares

output_file = c:/prog/test/compareResults.txt
#	Path to the output file.
#	Leo will silently write to this file, regardless of whether it already exists.
#	Leo will write to the log pane if this path is empty or invalid.

append_output_to_output_file = 0
#	0: Replace output file with results of compare.
#	1: Append output to output file.

# ----- Options related to directory compares.
#	These options has no effect when comparing files.

limit_directory_search_extension = .py
#	Limit directory searches to files with the given file extension.
# 	Examples:
#		None	Compare all files when comparing directories.
#		.py  	Compare .py files when comparing directories.

# ----- Options related to file compares.
#	These options have no effect when comparing directories.

ignore_blank_lines = 1
#	1: Ignore blanks lines when comparing files.

ignore_first_line_of_file_1 = 0
#	1: Ignore the first line of compare_file_1 when comparing files.

ignore_first_line_of_file_2 = 0
#	1: Ignore the first line of compare_file_2 when comparing files.

ignore_interior_whitespace = 0
#	1: Ignore whitespace after the leading whitespace of a line when comparing files.

ignore_leading_whitespace = 0
#	1: Ignore leading whitespace of each line when comparing files.
#	Not recommended when comparing .py files.

ignore_sentinel_lines = 0
#	1: Ignore sentinel lines when comparing files.
#	Leo sets sentinel comment delimiters from the first line of each file.
#	This option has no effect if the first line is not a @+leo line.

# ----- Options affecting how Leo shows the results of file compares.
#	(Leo gathers statistics regardless of these options.)

limit_count = 9
#	0: Show lines regardless of the number of mismatches.
#	n: Stop showing lines after n mismatches.

make_whitespace_visible = 0
#	1: Show blanks as [ ] and tabs as [t]

print_both_lines_for_matches = 0
#	0: Print only the line of compare_file_1 when showing matching lines.
#	1: Print lines of both files when showing matching lines.

print_matching_lines = 0
#	1: Print lines that match using the print_both_lines_for_matches option.

print_mismatching_lines = 1
#	1: Print lines that do not compare equal to each other.

print_trailing_lines = 1
#	1: Print lines all lines in one file after an end-of-file is seen on the other file.</t>
<t tx="T7"># The initial settings of the Find/Change panel.

[find/change options]

change_string = 
# 	The change string (without the quotes unless quotes are part of the string).

find_string = 
# 	The find string (without the quotes unless quotes are part of the string).

# ----- 0/1 settings for checkboxes in the Find/Change panel.

batch = 0
ignore_case = 0
mark_changes = 0
mark_finds = 0
pattern_match = 0
reverse = 0
search_body = 1
search_headline = 0
suboutline_only = 0
whole_word = 1
wrap = 0
node_only = 0</t>
<t tx="T8">@ Keyboard shortcuts for menu commands.

A shortcut specification has the form:
	
commandName = shortcutSpecifier

where commandName is the name of the command in the menu with all non-alphanumeric characters removed.  The shortcut specifier consists of a head followed by a tail.  The head may be empty, or may be a concatenation of the following: Shift+, Alt+, Control+ or Ctrl+.

Case is ignored in commandName, and in the head of the shortcutSpecifier. Case is significant in multi-character tails.  Also, - may be used instead of + in heads.  The following are all equivalent:
	
	Ctrl+A
	Ctrl-a
	Control+A

The following are not equivalent:
	
	Ctrl+-
	Ctrl-+

and the following are not equivalent:

	Ctrl+Tab (may be valid)
	Ctrl+tab (will never be valid)
	
See the section called "About keyboard shortcuts" for a full discussion of what may appear in the tail of a shortcut.
@c

# 
# Values are command names with all whitespace deleted.
# Case is ignored.

[keyboard shortcuts]

&lt;&lt; About keyboard shortcuts &gt;&gt;
&lt;&lt; Alt and Shift-Alt &gt;&gt;
&lt;&lt; Control &gt;&gt;
&lt;&lt; F-keys and others &gt;&gt;
&lt;&lt; Shift-Control &gt;&gt;
&lt;&lt; None &gt;&gt;
</t>
<t tx="T9">@ The following special single characters may be used in the tails of shortcuts.  They are listed along with their associated Tk binding value.  Leo contains special code to handle these characters.  No other single characters may be specified.

For example, you could specify Ctrl+! as a shortcut, and Leo will create a binding for &lt;Control+exclam&gt;.  Some of these values may be invalid on some machines.

! exclam
" quotedbl
# numbersign
$ dollar
% percent
&amp; ampersand
' quoteright
( parenleft
) parenright
* asterisk
+ plus
, comma
- minus
. period
/ slash
: colon
; semicolon
&lt; less
= equal
&gt; greater
? question
@ at
[ bracketleft
\ backslash
] bracketright
^ asciicircum
_ underscore
` quoteleft
{ braceleft
| bar
} braceright
~ asciitilde

Leo recognizes the following mult-character names, and translates the indicated strings in the menu items:
	
"bksp"     : "BkSp"
"dnarrow"  : "DnArrow"
"ltarrow" 	: "LtArrow"
"rtarrow" 	: "RtArrow"
"uparrow"  : "UpArrow"
"pageup"   : "PgUp"),
"pagedn"   : "PgDn")

For example, "Ctrl-uparrow"  will appear as "Ctrl+UpArrow" in the menu.

Leo passes all other mult-character names verbatim to Tk, so on some platforms you may be able to use any of the following.  Most appear on the numeric keypad. For example, the following may work on some systems:
	
"Ctrl+BackSpace"

Don't use these if you want to be sure that the binding work on all platforms. The complete list of names may be found at: http://tcl.activestate.com/man/tcl8.4/TkCmd/keysyms.htm.
	
F1, F2, F3, F4, F5, F6, F7, F8, F9, F10,
BackSpace, Break, Clear, Delete, Escape, Linefeed, Return, Tab, 
Down, Left, Right, Up,
Begin, End, Home, Next, Prior,
Num_Lock, Pause, Scroll_Lock, Sys_Req,
KP_Add, KP_Decimal, KP_Divide, KP_Enter, KP_Equal,
KP_Multiply, KP_Separator, KP_Space, KP_Subtract, KP_Tab,
KP_F1, KP_F2, KP_F3, KP_F4,
KP_0, KP_1, KP_2, KP_3, KP_4, KP_5, KP_6, KP_7, KP_8, KP_9</t>
<t tx="T10">ExpandNextLevel   = Alt+=
ContractParent    = Alt+0
ContractAll       = Alt+1
ExpandToLevel2    = Alt+2
ExpandToLevel3    = Alt+3
ExpandToLevel4    = Alt+4
ExpandToLevel5    = Alt+5
ExpandToLevel6    = Alt+6
ExpandToLevel7    = Alt+7
ExpandToLevel8    = Alt+8
ExpandAll         = Alt+9

SortSiblings     = Alt-A
MarkChangedItems = Alt+C
GoToNextChanged  = Alt+D
ExecuteScript    = Alt+E
GoToLineNumber   = Alt+G
MarkClones       = Alt+K
GoToNextMarked   = Alt+M
GoToNextCloned   = Alt+N
OpenPythonWindow = Alt+P
MarkChangedRoots = Alt+R
MarkSubheads     = Alt+S
UnmarkAll        = Alt+U
ShowInvisibles   = Alt+V

# EKR: I set the following in customizeLeo.py
# Idle           = Alt+Shift+I
# Word           = Alt+Shift+W
# WordPad        = Alt+Shift+T
SetColors        = Alt+Shift+C
SetFont          = Alt+Shift+F

GoNextVisible    = Alt+DnArrow
GoPrevVisible    = Alt+UpArrow
GoBack           = Alt+Shift+UpArrow
GoNext           = Alt+Shift+DnArrow</t>
<t tx="T11">CloneNode        = Ctrl+`
Replace          = Ctrl+=
ReplaceThenFind  = Ctrl+-
Indent           = Ctrl+]
Unindent         = Ctrl+[
Promote          = Ctrl+{
Demote           = Ctrl+}

SelectAll        = Ctrl+A
# Unused         = Ctrl+B
Copy             = Ctrl+C
MoveDown         = Ctrl+D
EqualSizedPanes  = Ctrl+E
FindPanel        = Ctrl+F
# It is no longer possible to specify two shortcuts for the same command.
# Unused         = Ctrl+G
EditHeadline     = Ctrl+H
InsertNode       = Ctrl+I
# Unused         = Ctrl+J
MatchBrackets    = Ctrl+K
MoveLeft         = Ctrl+L
Mark             = Ctrl+M
New              = Ctrl+N
Open             = Ctrl+O
# Unused         = Ctrl+P
Exit             = Ctrl-Q
MoveRight        = Ctrl+R
Save             = Ctrl+S
ToggleActivePane = Ctrl+T
MoveUp           = Ctrl+U
Paste            = Ctrl+V
Close            = Ctrl+W
Cut              = Ctrl+X
Preferences      = Ctrl+Y
CantUndo         = Ctrl+Z</t>
<t tx="T12">DeleteNode      = Shift+Ctrl+BkSp

TangleAll       = Shift+Ctrl+A
ConvertBlanks   = Shift+Ctrl+B
CopyNode        = Shift+Ctrl+C
Extract         = Shift+Ctrl+D
ExtractSection  = Shift+Ctrl+E
ImportTofile    = Shift+Ctrl+F
# Unused        = Shift+Ctrl+G
# Unused        = Shift+Ctrl+H
# Unused        = Shift+Ctrl+I
ConvertTabs     = Shift+Ctrl+J
# Unused        = Shift+Ctrl+K
# Unused        = Shift+Ctrl+L
TangleMarked    = Shift+Ctrl+M
ExtractNames    = Shift+Ctrl+N
OpenWith        = Shift+Ctrl+O
ReformatParagraph = Shift+Ctrl+P
# Unused        = Shift+Ctrl+Q
ReadOutlineOnly = Shift+Ctrl+R
SaveAs          = Shift+Ctrl+S
Tangle          = Shift+Ctrl+T
Untangle        = Shift+Ctrl+U
PasteNode       = Shift+Ctrl+V
WritefileNodes  = Shift+Ctrl+W
CutNode         = Shift+Ctrl+X
CantRedo        = Shift+Ctrl+Z</t>
<t tx="T13">FindNext     = F3
FindPrevious = F4

AbortEditHeadline = Shift+Esc
EndEditHeadline = Esc
</t>
<t tx="T14">@ These are all comments...

AboutLeo                = None
ApplySettings           = None
Cascade                 = None
ContractAllChildren     = None
ContractChildren        = None
ExpandAllChildren       = None
ExpandChildren          = None
ExpandToLevel1          = None
FlattenOutline          = None
ImportCWEBFiles         = None
ImportFlattenedOutline  = None
ImportNowebFiles        = None
ImportToroot            = None
MinimizeAll             = None
OnlineHomePage          = None
OpenLeoConfigLeo        = None
OpenLeoDocsLeo          = None
OpenOfflineTutorial     = None
OpenOnlineTutorial      = None
OpenCompareWindow       = None
OpenfileWith            = None
OutlineToCWEB           = None
OutlineToNoweb          = None
ReadfileNodes           = None
ReferenceLeoDocsleo     = None
RemoveSentinels         = None
RevertToSaved           = None
SaveTo                  = None
SortChildren            = None
ToggleSplitDirection    = None
UntangleAll             = None
UntangleMarked          = None
Weave                   = None
WriteOutlineOnly        = None</t>
<t tx="T15"># The initial settings of the Preferences panel.

[prefs panel options]

default_tangle_directory = 
# 	(Deprecated)
# 	The default directory used if no directory specified
# 	in @path, @root or @file directives.

default_target_language = Python
# 	The default language if no @language or @comment is in effect.

tab_width = 4
# 	The width of tabs on the screen.
# 	This setting is also used when writing doc parts.
# 	Valid values: A nonzero positive or negative integer.
# 	Negative tab widths cause Leo to convert tabs to blanks when typing.

page_width = 80
# 	The page width for wrapping doc parts in derived files.
# 	Valid values: any nonzero positive integer.

output_doc_chunks = 1
# 	1/0: Explicit Tangle commands output doc parts.

tangle_outputs_header = 1
# 	1/0: Explicit Tangle commands output file header.

run_tangle_done.py = 0
# 	1/0: Run tangle_done.py after explicit Tangle commands.

run_untangle_done.py = 0
# 	1/0: Run tangle_done.py after explicit Untangle commands.</t>
<t tx="T16">[syntax coloring options]

color_cweb_doc_parts_with_latex = 1
#	1: @space, @* and @** sections in cweb mode are colored black with LaTeX keywords highlighted.
#	0: @space, @* and @** sections in cweb mode are colored as comments (default is red).
#	Note: in either case, _noweb_ section references and defintions are colored as usualy.

color_cweb_comments_with_latex = 1
#	1: C language comments in cweb mode are colored black with LaTeX keywords highlighted.
#	0: C language comments in cweb mode are colored as comments (default red).
#	Note: in either case, _noweb_ section references and defintions are colored as usualy.

color_directives_in_plain_text = 1
# 	1/0: Color Leo directives for @language plain

underline_undefined_section_names = 1
# 	1/0: Underline undefined section names
#	Only functional if use_hyperlinks = 0

use_hyperlinks = 0
# 	1: use hyperlinks.       Underline "live" links.
#		Cute, but disorienting and _not_ recommended.
#		Control-clicking moves to indicated node.
#	0: don't use hyperlinks and allow underlining of undefined section names.

# The following may be any valid Tk color name or color value.
# 	For example, #00aa00 is the dark green used by IDLE.
# 	For Tk color names see: http://www.tcl.tk/man/tcl8.3/TkCmd/colors.htm
# 	These names are case sensitive, for example: BlanchedAlmond

comment_color = firebrick3
#	The color of comments in code parts.

cweb_section_name_color = red
#	The color of name in @&lt;name@&gt;

directive_color = blue
#	The color of C/C++ preprocessor directive lines.

doc_part_color = firebrick3
#	The color of text in doc parts.

keyword_color = blue
#	The color of keywords of the present language.
#	For example, the color of "if", "try" and "except" in Python.

leo_keyword_color = #00aa00
#	The color of Leo keywords.
#	For example, the color of @ignore, @color, etc.

section_name_color = red
#	The color of name in &lt; &lt; name &gt; &gt; when name is defined.

section_name_brackets_color = blue
#	The color of the double angle brackets in &lt; &lt; name &gt; &gt;

string_color = #00aa00
#	The color of strings and their delimiters.

undefined_section_name_color = red
#	The color of name in &lt; &lt; name &gt; &gt; when name is undefined.</t>
<t tx="T17">@ Options that affect the appearance of windows.

Options that require pixel values can be any Python expression that yields an int.
Warning: the number of pixels per inch varies...
@c

[window options]

&lt;&lt; body pane options &gt;&gt;
&lt;&lt; outline pane options &gt;&gt;
&lt;&lt; log pane options &gt;&gt;
&lt;&lt; Options for new windows &gt;&gt;
&lt;&lt; Options for newly opened windows &gt;&gt;
&lt;&lt; Options for the bar that separates panes in the Leo window &gt;&gt;</t>
<t tx="T18">body_pane_wraps = 1
#	0/1: Wrap body text if 1.

additional_body_text_border = 0
#	Additional border in body text pane, in pixels (must be an integer).

body_text_foreground_color =
body_text_background_color =
#	Foreground and background colors of body text.

body_cursor_foreground_color =
body_cursor_background_color =
# 	Foreground and background colors for the cursor in body text.

body_text_font_family = Courier New
#	Font family for body text.
#	Default is default font for Tk.Text widgets.
#	Invalid font names are translated to a font in a system-dependent way.

body_text_font_size = 9
#	Size of body text. Must be an integer.
#	Default is 12.

body_text_font_slant = roman
#	The Tk -slant setting: roman or italic.  Default is roman.

body_text_font_weight = normal
#	The Tk -weight setting: normal or bold.  Default is normal.

smart_auto_indent = 0
#	1: auto-indent aligns with open ({[ brackets
#	0: auto-indent increases indentation by one tab for Python only.</t>
<t tx="T19">outline_pane_scrolls_horizontally = 0
#	0/1: 1: Use horizontal scrollbar in outline pane.

headline_text_unselected_foreground_color = black
headline_text_unselected_background_color = white
#	Foreground and background colors of unselected headline text.
#	Both must be specified for either to take effect.

headline_text_selected_foreground_color = black
headline_text_selected_background_color = gray80
#	Foreground and background colors of selected headline text that is not being edited.
#	Both must be specified for either to take effect.

headline_text_editing_foreground_color = black
headline_text_editing_background_color = white
#	Foreground and background colors of unselected headline text in a headline that is being edited.
#	Both must be specified for either to take effect.

headline_text_editing_selection_foreground_color = white
headline_text_editing_selection_background_color = DarkBlue
#	Foreground and background colors of selected text headline text in a headline that is being edited.
#	Both must be specified for either to take effect.

outline_pane_background_color =
#	Background color of outline pane itself.

headline_text_font_family =
#	Font family for headline text.
#	Default is default font for Tk.Text widgets.
#	Invalid font names are translated to a font in a system-dependent way.

headline_text_font_size = 9
#	Size of headline text. Must be an integer.
#	Default is 12

headline_text_font_slant = roman
#	The Tk -slant setting: roman or italic. Default is roman.

headline_text_font_weight = normal
#	The Tk -weight setting: normal or bold.  Default is normal.</t>
<t tx="T20">log_pane_wraps = 0
#	0/1: Wrap body text if 1.

log_text_foreground_color =
log_text_background_color =
#	Foreground and background colors of log text.

log_text_font_family =
#	Font family for text in the log pane.
#	Default is default font for Tk.Text widgets.
#	Invalid font names are translated to a font in a system-dependent way.

log_text_font_size = 9
#	Size of text in the log pane. Must be an integer.
#	Default is 12

log_text_font_slant = roman
#	The Tk -slant setting: roman or italic. Default is roman.

log_text_font_weight = normal
#	The Tk -weight setting: normal or bold.  Default is normal.</t>
<t tx="T21"># Leo now properly opens windows for existing files where they were last positioned.

initial_window_height = 20
#	Height of window, Tk grid units (must be an integer).
#	Grid units must be specified because Leo windows are gridded.
	
initial_window_width = 60
#	Width window, in Tk grid units (must be an integer).
#	Grid units must be specified because Leo windows are gridded.

initial_window_left = 10
#	Distance from left of screen of window, in pixels (must be an integer).

initial_window_top = 10
#	Distance from top of screen of window, in pixels (must be an integer).</t>
<t tx="T22">initial_splitter_orientation = v
#	Defines the primary splitter orientation.
#	The primary panes are the body pane and the secondary pane.
#	The secondary pane contains the outline and log panes.

#	valid values: h or horizontal or v or vertical.
#	(Actually, anything but h or horizontal is considered vertical.)
#	vertical: body pane below outline and log panes.
#	horizontal: body pane to left of outline and log panes.

#	Note: this is _not_ saved in .leo files, but the body/outline ratio _is_ saved.
#	This will lead to confusing results when this file is read only:
#	1. Changes to orientation caused by Toggle Split Direction are not changed, but
#	2. Changes to body/outline ratio _are_ changed.

initial_vertical_ratio = 0.5
#	The ratio of tree pane size to body pane size when splitting primary panes vertically.
#	Applies only to new windows. Overridden by ratio in .leo files.
#	Valid values: 0.0 to 1.0.

initial_horizontal_ratio = 0.3
#	The ratio of tree pane size to body pane size when
#	splitting primary panes horizontally.

#	Applies only to new windows. Overridden by ratio in .leo files.
#	Valid values: 0.0 to 1.0.

initial_horizontal_secondary_ratio = 0.5
#	The ratio of outline pane size to log pane size when
#	splitting the primary panes horizontally.

#	Applies to all newly opened windows.
#	Valid values: 0.0 to 1.0.

initial_vertical_secondary_ratio = 0.7
#	The ratio of tree pane size to body pane size when
#	splitting the primary panes vertically.

#	Applies to all newly opened windows.
#	Valid values: 0.0 to 1.0.</t>
<t tx="T23"># Leo should save these to .leo files, and it doesn't.

split_bar_color = LightSteelBlue2
#	gray90 also looks good.
#	The color of the split bar.
#	Valid values: Tk color names or Tk color values.

split_bar_relief = groove
#	The Tk -relief option for the split bar.
#	Valid values: raised, sunken, flat, ridge, solid, groove.
	
split_bar_width = 6
#	The width of the split bar, in pixels (must be an integer).</t>
</tnodes>
</leo_file>
