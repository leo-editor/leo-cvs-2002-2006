Important note: See INSTALL.TXT for installation instructions.

leo.py is available at:  http://sourceforge.net/projects/leo/
leo.py requires Python 2.1 or above and tcl/tk 8.3 or above.
leo.py will work on Linux, Windows and MacOs X Jaguar.

leo.py 4.0 alpha 2                  May 14, 2003

This version contains disabled 4.x read/write code.  It is compatible all 3.x versions of Leo.

- alpha 2 fixes a bad bug when cutting and pasting entire trees.

leo.py 3.11.1                       May 1, 2003

This version fixes two bugs:
	
- Leo threw an exception at startup on some Linux systems.
- Creating clones by control dragging did not always work.

This code contains permanently disabled 4.0 code.

leo.py 3.11                         April 27, 2003

This version of Leo contains many important improvements since 3.10,
especially support for unicode and a new plugin architecture.

The Highlights of 3.11:

** Leo supports unicode properly.
	- New @encoding directives specifies encoding for derived files.
	- New settings specify default encodings for .leo and derived files.
	- Derived files specify encodings used to create them.
** A new plugin architecture for customizing Leo.
- New commands:
	- Toggle Angle Brackets.
	- Insert Time/Date (in headline or body text).
	- Go To First/Last Node, Parent, Next/Previous Sibling.
	- Write Missing @file Nodes.
	- Expand/Contract Node.
- Improved commands:
	- Fixed a huge performance bug that slowed moving nodes left.
	- Expand/Contract commands now operate on the selected tree.
	  ( A major improvement)
	- Sort Siblings command can now sort top-level nodes.
	- Leo now allows multiple writes of cloned nodes.
	  (Useful when different @path directives are in effect.)
- Other improvements:
	- New @lineending directive specifies line endings.
	- Improved syntax coloring for html and xml.
	- Leo scrolls partially visible headlines into full view.
	- Added "Replace tabs with spaces" checkbox in Prefs panel.
- New settings in leoConfig.leo/.txt.
	- Added "tk_encoding" setting and related logic.
	- Colors for Show Invisibibles command and body_insertion_cursor
	- Settings affecting when control-drags start.
	- Defaults for unicode (see above).
- Many other bug fixes and improvements.

leo.py 3.10                             December 14, 2002

This version of Leo corrects bugs, improves Leo's documentation and adds many new features:

- Rewrote Scripting Chapter in Leo's Users Guide.
- Improved the Customization Chapter of the Users Guide.
- Adds several customizations contributed by Leo's users.
  Among these: @read-only nodes. Reading empty .leo files.
  Redirecting stderr and stdout to Leo's log pane.
- New Mark Clones and Go To Next Clone commands.
- New Export Headlines command.
- Control-dragging a node now clones it.
- New "Node Only checkbox in the Find/Change panel.
- @root-code trees start in code mode by default.
  This allows @root trees to work like @file trees.
- @root-doc  trees start in doc  mode by default.
- Converted leoConfig.py to use @root-code
- New at_root_bodies_start_in_doc_mode option in leoConfig.py.
  Specifies whether @root trees work like @root-code or @root-doc.
- New synonyms: @file-asis = @silentfile
  @file-nosent = @nosentinelsfile ; @file-noref = @rawfile.
- Leo now supports navigation of menus using underlined menus.
- Added an easy way to replace any Leo method by a function.
  Hooks can now override part of Leo's code!
- Added routines to redirect stderr and stdout to Leo's log pane.
  These routines can be called from hooks.
- Added "event1" and "event2" hooks for customize event handling.
- Improved Leo's window icon, and improved how that icon is loaded.
- Added contributed code to support @read-only nodes.
  This code show how easy it is to customize Leo.
- The usual assortment of bug fixes and minor improvements.
  Actually, this release fixes more than the usual number of bugs.

leo.py 3.9                               Nov 23, 2002

This is one of the most interesting versions of Leo ever released:

* Major performance improvements:
  - Incremental syntax coloring speeds response when typing.
  - Incremental undo drastically reduces memory used.

* Major improvements in customizing Leo:
  - Leo looks in the file customizeLeo.py for user-specific customizations.
  - Leo calls "hook routines" in customizeLeo.py for all commands and events.
	These hook routines can modify or replace any command or event.
  - New convenience routines simplify creating and modifying menus.
  - Easy translation of menus to other languages using customizeLeo.py.

* Better integration with other tools:
  - The Open With command allows you to communicate back and forth to other editors.
  - The Go To Line Number command converts lines numbers in derived files
	to locations in the outline.
  - Double-clicking the icon of a @url node launches any url in your web browser.
  - The Execute Script command executes Python code in any body pane.
	This is much more convenient than opening Leo's Idle window.
  - Much better support for cweb. At last, Leo has a power user of cweb.
	By default, @space, @* and @** sections are colored as latex text.
	Leo properly generates @q..@> sentinels.
  - @nosentinelfile is like @file except Leo writes no sentinel lines.

* Other improvements:
  - Optional Emacs-style auto-indent.
  - Reformat Paragraph command.
  - Leo will optionally create nonexistent directories specified in
	@file, @root or @path, including all nonexistent parent directories.
  - Leo will place its own icon in Leo windows provided that you have
	installed Fredrik Lundh's PIL and tkIcon packages.
  - The usual assortment of bug fixes.

leo.py 3.8                                 October 29, 2002

Many major improvements have been made to Leo, all made as the result of user requests:

- New @rawfile and @silentfile trees complement @file trees.
  @rawfile and @silentfile trees create derived files without using sections.
  @rawfile files contain only those sentinels needed to automatically untangle them.
  @silentfile trees contain no sentinels at all.
- New @raw and @end_raw directives allow unformatted code within @file trees.
- Much better support for CWEB.  You may organize .w files using noweb!
- The @comment and @language directives may now apply simultaneously.
- Leo can now read, remember and write <?xml-stylesheet...?> lines,
  under control of the new stylesheet option.
- The new output_newline option specifies the line endings used when writing files.
- The new output_initial_comment option specifies the text to appear
  in an @comment sentinel at the start of each derived file.
- New commands in the help menu make it much easier to change configuration options.
- Dozens of minor improvements and bug fixes.

leo.py 3.7                                 October 9, 2002

Many improvements have been made to Leo.  The highlights:

- Now works with Python 2.1.  Previous versions required Python 2.2.
- Many new user options, including user-definable shortcuts for all commands.
  and colors for all parts of Leo's windows.
  As a result, it is now possible to use arrow keys as you desire.
- Minimal support for Unicode Latin-1 (iso-8859-1) encoding. Better support is coming.
- Improved handling of relative path names.
- The @first directive allows lines to precede the opening @+leo sentinel line.
- The @last  directive allows lines to follow  the closing @-leo sentinel line.
- Better support for Perl+pod.
- Leo now ends all lines with '\n' regardless of platform.
- Leo is now compatible with Python 2.1.
- Simplified sentinels reduce spurious CVS diffs.
- Many other minor improvements and bug fixes.

leo.py 3.6                                   September 11, 2002

Highlights:

- Fixed a large number of bugs, especially bugs that appear only on Linux.
- Leo now remembers the previous insertion point and location of the scrollbar when switching between nodes.
- Added Match Brackets command.
- Added support for MouseWheel (Linux only).
- Added support for LaTex and PHP.
- Improved all aspects of the Help menu.
- Discovered a minor bug involving the Python (Idle) window and documented a workaround.

leo.py 3.5                                    August 14, 2002

The many bugs were reported in 3.4 show that leo.py is being heavily used.  This version corrects all known bugs and adds some new features:

- Added new entries in the help menu,
  (Including a link to Joe Orr's excellent ScreenBook tutorial).
- Added configuration options for horizontal scrollbars.
- Added an importFiles script for mass imports.
- Added better warnings for read-only files.
- Removed all '\r' characters when reading derived files.
- Fixed crasher in Read Outline Only command.
- Fixed crasher when leoConfig.txt did not exist.
- Many small improvements and bug fixes.

leo.py 3.4                                     August 11, 2002

This version contains many small improvements and bug fixes:

- Fixed several crashers involving Unicode.
- The Show Invisibles command now makes blanks and tabs look much better.
- Created leoConfig.leo, from which leoConfig.txt is now derived.
- Added save_clears_undo_buffer configuration option.
- Fixed a large number of problems with the configuration code.
- The usual minor improvements and bug fixes.

leo.py 3.3                                     August 3, 2002

This version of Leo:

- Adds support for Unicode.
- Improved the Import commands.
- Fixed numerous bugs related to configuration settings.
- Fixed the "Javadoc" bug and several latent bugs related to it.

leo.py 3.2                                     July 30, 2002

This version generalizes the @others directive, improves the Import command and fixes several bugs.  See the children of this node for full details.

The highlights:

- Nested @others directives are now valid, an important improvement.
  This simplifies files that define more than one class.
- Improved the Import command and squashed several bugs lurking there.
- Made the various Go commands in the Outline-Move/Select menu functional
  by reassigning keyboard shorts
- Fixed a crasher in the Prefs Panel.
- Fixed numerous bugs in the Set Colors command.
- Fixed syntax coloring of C strings that span multiple lines.
- The usual minor improvements and bug fixes.

leo.py 3.1                                     July 20, 2002

This version fixes a blunder that affects only leo.py 3.0.
I recommend that all users of 3.0 upgrade to 3.1.

With this release Leo's to-do list is now empty!
I shall fix bugs as they are reported.
I'll add new features only if convinced that they contribute significantly to Leo.

The highlights:

- Fixed a blunder: Leo 3.0 did nothing when it was opened directly from leo.py.
  (Opening leo using openLeo.py did work.)
- Created a compare panel to control scripts in leoCompare.py.
- Added many new settings in leoConfig.txt to initialize the compare panel.
- The FAQ tells how to add support for new languages.
- The usual minor improvements and bug fixes.

leo.py 3.0                                     July 16, 2002

This version is called 3.0 because it can optionally produce files that
can _not_ be read by the leo.py 2.x or the Borland version of Leo.
By default, leo.py 3.0 _does_ produce files that all previous versions of Leo can read.

As always, see LeoDocs.leo for full details.  The highlights:

- Many new user options in leoConfig.txt, including, among others,
  fonts in all panes, colors for syntax coloring and default window size and position.
- Support for .leo files with XML types like "ISO-8859-1", controlled by a user option.
  Note: by default, Leo writes files compatible with previous versions of Leo.
- Powerful new Color and Font pickers, fully connected to user options.
- Added Toggle Split Direction command, under control of user options.
- Added autoscrolling in the outline pane.
- Windows open at the position in which they were saved.
- The size and position of new windows can be controlled with user options.
- Eliminated drawing problems while opening files.
- Improved syntax coloring for @comment plain.
- The Convert All Blanks and Convert All Tabs commands are now undoable.
- Leo warns and aborts if Python 2.2 or above is not running.
- The usual bug fixes.

leo.py version 2.5.1                           July 7, 2002

This version corrects crashers that affect undo/redo move commands.
Version 2.5 has been withdrawn.

ANYONE USING 2.5 SHOULD IMMEDIATELY SWITCH TO 2.5.1.

leo.py version 2.5                             July 7, 2002

See LeoDocs.leo for full details.  The highlights:

- Leo supports tab widths properly, and negative tab widths cause
  Leo to convert tabs to blanks as you type.
- Three new commands appear in the Edit Body menu:
  Convert Tabs, Convert All Tabs and Convert All Blanks.
  Convert All Tabs and Convert All Spaces convert the entire selected tree.
- Leo now allows you to override selected preferences using a
  configuration file called leoConfig.txt.
  Leo acts as before if this file does not exist.
- The Preferences panel is now contains Ok, Cancel and Revert buttons.
- Cut and paste work properly in all situations.
  You can cut and paste between Leo and other applications,
  or between two different copies of Leo.
- Added the Recent Files submenu to the File menu.
- Fixed several crashers.
- Fixed several bugs in the Import commands.
- Leo will no longer abort reading if it detects an invalid directory name
  in the Default Tangle Directory in the Preferences panel.

leo.py version 2.4                             June 20, 2002

This version fixes some annoying bugs and adds some nice features:

- Leo now properly highlights the headline of a newly created node.
- The Edit Headline command now works properly.
  Double and triple clicking in a headline now works as expected.
- You can now reorganize drag headlines around.
  You must drag from a node's icon and release on another node's icon.
- You can now open .leo files in leo.py by double clicking on .leo files,
  provided that you associate leo.py with .leo files.
- Improved error recovery when there are errors writing .leo files.
- All parts of LeoDocs.leo now match the documentation on Leo's web site.

leo.py version 2.3                             June 12, 2002

This version fixes a minor problem with Leo.

- The code that reads and writes @file nodes now uses the directory containing the
 .leo file as a default when the Default Tangle Directory setting is empty in the Preferences panel.
- The Tangle and Untangle commands have used this convention for a long time.
- This default allows us to distribute LeoPy.leo without specifying
  a directory in the Preferences Panel.

leo.py version 2.2                             June 2, 2002

The version fixes two bugs that happen rarely and can cause loss of data when they do happen.

- In certain circumstances leo.py v2.1 would delete most of an outline when
  a node was moved in front of the previous root node!
- All previous versions of leo.py will crash when saving body text containing unicode characters.
  This could occur as the result of cutting and pasting text from another application into the body pane.
- Leo.py now writes body text containing unicode characters using Python's u-prefixed notation.
  That is, the body text is written as: u'escaped_text', where escaped text replaces unicode characters
  not in the ascii character set by escape sequences of the form \uxxxx.
- The result contains nothing but ascii characters, so leo.py will have no problem reading it.
  Naturally, compilers and other tools may not understand Python's notation,
  so you may have to convert escaped text to something that your tools can understand.

Edward K. Ream
