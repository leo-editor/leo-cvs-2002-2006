Important note: See INSTALL.TXT for installation instructions.

Leo is available at:  http://sourceforge.net/projects/leo/
Leo requires Python 2.1 or above and tcl/tk 8.3 or above.
Leo will work on Linux, Windows and MacOs X Jaguar.

Leo 4.1 beta 5                   November 23, 2003

This is the fifth release of the reorganized 4.1 code base, but please use caution when using this code. Warning: By default Leo 4.1 creates .leo files that can not be read by older versions of Leo.

Note: there have been problems reported with using plugins on Linux.  As far as I know those problems have _not_ been fixed.

Beta 5:
  - Leo will run in batch mode it the command line contains --script scriptFile.
  - Fixed new crashers in the Extract Section and Extract commands.
  - Fixed an old crasher when Undoing a Change All command when searching headlines.
  - Fixed a new crasher when write a file containing an undefined section.
  - Fixed a new problem involving warnings of duplicate bindings in popup menus.
  - Made sure to show Leo's windows in wx gui plugin.

Beta 4:
  - Fixed several "reorg" bugs, some of which affected plugins.
  - Allow @directives and section references when executing scripts!
  - More than one section reference may now appear on the same line.
  - Uses "utf-8" encoding for filenames under MacOS (Darwin)
  - Allow command or cmnd prefix for menu shortcuts under Darwin.
  - Wraped all os.path calls to that file and directory names can be converted to Unicode.
    This is necessary (but not sufficient?) to support Chinese file and directory names.

Beta 3 completed the reorg: many changes to the code.  Also fixes a LaTeX coloring bug.

Beta 2 fixed a startup problem on Linux: the "mbcs" text encoding is not valid on Linux.

Highlights of 4.1:
-----------------

* Leo 4.1 includes several new commands:
  - script-based find/change commands: very powerful and flexible.
  - Hoist & DeHoist commands for viewing parts of an outline.
  - Check Outline command finds user clone mistakes.
* New configuration settings:
  - use_gnx specifies whether .leo files use integers as indices:
    use_gnx = 0 makes .leo files compatible with previous versions of Leo.
    use_gnx = 1 makes .leo files cvs-friendly
  - config_encoding specifies the encoding of leoConfig.txt.
* Several significant code-level changes:
  - The 4.1 code base has been reorganized to support gui plugins.
    An example wx_gui plugin is partly functional.
  - Created a flexible framework for creating & running regression tests.
    This framework takes full advantage of outlines to organize tests.
  - app.forceShutdown now works when called from plugins.
- Fixed several long-standing bugs.  More fixes are coming.