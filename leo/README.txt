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
