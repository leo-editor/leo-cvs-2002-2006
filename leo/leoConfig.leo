<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="16" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="86" left="142" height="20" width="77"/>
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
<v t="T2" a="V"><vh>leoConfig.txt</vh>
<v t="T3"><vh>&lt;&lt; general comments and warnings &gt;&gt;</vh></v>
<v t="T4"><vh>&lt;&lt; General configuration options, especially read-only mode &gt;&gt;</vh></v>
<v t="T5"><vh>&lt;&lt; The "Recent Files" menu &gt;&gt;</vh></v>
<v t="T6"><vh>&lt;&lt; Compare Panel settings &gt;&gt;</vh></v>
<v t="T7"><vh>&lt;&lt; Find/Change Panel settings &gt;&gt;</vh></v>
<v t="T8"><vh>&lt;&lt; Preferences Panel settings &gt;&gt;</vh></v>
<v t="T9"><vh>&lt;&lt; Syntax coloring options and colors &gt;&gt;</vh></v>
<v t="T10"><vh>&lt;&lt; Window options &gt;&gt;</vh>
<v t="T11"><vh>&lt;&lt; body pane options &gt;&gt;</vh></v>
<v t="T12"><vh>&lt;&lt; outline pane options&gt;&gt;</vh></v>
<v t="T13"><vh>&lt;&lt; log pane options &gt;&gt;</vh></v>
<v t="T14"><vh>&lt;&lt; Options for new windows &gt;&gt;</vh></v>
<v t="T15"><vh>&lt;&lt; Options for newly opened windows &gt;&gt;</vh></v>
<v t="T16"><vh>&lt;&lt; Options for the bar that separates panes in the Leo window &gt;&gt;</vh></v>
</v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="T1">@nocolor

This is the file that creates leoConfig.txt.  We use this file for two reasons:
	
1. It is easier to update this file than a large text file.

2. When read_only = 0, all comments are lost in Leo updates leoConfig.txt, so using this file is a way of keeping these comments.

@color</t>
<t tx="T2">@comment #
@ We use an @root node here to suppress automatic untangling, so we don't lose all these nice comments in read-write mode.
@root leoConfig.txt

# leoConfig.txt: configuration file for Leo.
# 8/6/2002 by Edward K. Ream

&lt;&lt; general comments and warnings &gt;&gt;

# WARNING: !! Do not place anything except comments before here !!

&lt;&lt; General configuration options, especially read-only mode &gt;&gt;
&lt;&lt; The "Recent Files" menu &gt;&gt;
&lt;&lt; Compare Panel settings &gt;&gt;
&lt;&lt; Find/Change Panel settings &gt;&gt;
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
<t tx="T4">@c

[config options]

read_only = 0
#	0: Leo writes this file, clearing all comments in the process.
#	1: Leo writes nothing to this file.
#	Syntax errors in this file set this file to read-only.

xml_version_string = UTF-8
#	The version used at the start of .leo files.
#	Default is UTF-8.  Better is ISO-8859-1.
#	Use UTF-8 to write leo.py 2.x files.

save_clears_undo_buffer = 0
#	1: Save command clears undo buffer.
#	0: Undo buffer persists across saves.</t>
<t tx="T5">@c

# The list of files in the "Recent Files" menu at startup.

[recent files]

file2 = c:\prog\leocvs\leo\leoConfig.leo
file1 = c:\prog\leocvs\leo\leopy.leo
file0 = c:\prog\leocvs\leo\leodocs.leo
#	Paths to recent files.
#	Valid option names: file0 through file9.</t>
<t tx="T6">@c

# 	These correspond to the keyword parameters of the leoCompare constructor.
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
<t tx="T7">@c

# The initial settings of the Find/Change panel.

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
wrap = 0</t>
<t tx="T8">@c

# The initial settings of the Preferences panel.

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

page_width = 132
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
<t tx="T9">@c

[syntax coloring options]

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
<t tx="T10">@ Options that affect the appearance of windows.

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
<t tx="T11">@c

body_pane_wraps = 1
#	0/1: Wrap body text if 1.

additional_body_text_border = 0
#	Additional border in body text pane, in pixels (must be an integer).

body_text_font_family = Courier
#	Font family for body text.
#	Default is default font for Tk.Text widgets.
#	Invalid font names are translated to a font in a system-dependent way.

body_text_font_size = 9
#	Size of body text. Must be an integer.
#	Default is 9 on Windows, 12 on Linux and all others.

body_text_font_slant = roman
#	The Tk -slant setting: roman or italic.  Default is roman.

body_text_font_weight = normal
#	The Tk -weight setting: normal or bold.  Default is normal.</t>
<t tx="T12">@c

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
<t tx="T13">@c

log_text_font_family =
#	Font family for text in the log pane.
#	Default is default font for Tk.Text widgets.
#	Invalid font names are translated to a font in a system-dependent way.

log_text_font_size =
#	Size of text in the log pane. Must be an integer.
#	Default is 12

log_text_font_slant = roman
#	The Tk -slant setting: roman or italic. Default is roman.

log_text_font_weight = normal
#	The Tk -weight setting: normal or bold.  Default is normal.</t>
<t tx="T14">@ Leo now properly opens windows for existing files where they were last positioned.
@c

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
<t tx="T15">@c

initial_splitter_orientation = v
#	valid values: h or horizontal or v or vertical.
#	(Actually, anything but h or horizontal is considered vertical.)
#	vertical: body pane below outline and log panes.
#	horizontal: body pane to left of outline and log panes.
#	Note This is _not_ saved in .leo files, but the body/outline ratio _is_ saved.
#	This will lead to confusing results when this file is read only:
#	1. Changes to orientation caused by Toggle Split Direction are not changed, but
#	2. Changes to body/outline ratio _are_ changed.

initial_vertical_ratio = 0.5
#	tree pane/body pane size when spitting pane vertically.
#	Applies only to new windows. Overridden by ratio in .leo files.
#	Valid values: 0.0 to 1.0.

initial_horizontal_ratio = 0.3
#	tree pane/body pane size when spitting pane horizontally.
#	Applies only to new windows. Overridden by ratio in .leo files.
#	Valid values: 0.0 to 1.0.</t>
<t tx="T16">@ Leo should save these to .leo files, and it doesn't.
@c

split_bar_color = LightSteelBlue2
#	The color of the split bar.
#	Valid values: Tk color names or Tk color values.

split_bar_relief = groove
#	The Tk -relief option for the split bar.
#	Valid values: raised, sunken, flat, ridge, solid, groove.
	
split_bar_width = 7
#	The width of the split bar, in pixels (must be an integer).</t>
</tnodes>
</leo_file>
