Important note: See INSTALL.TXT for installation instructions.

Leo is available at:  http://sourceforge.net/projects/leo/
Leo requires Python 2.1 or above and tcl/tk 8.3 or above.
Leo will work on Linux, Windows and MacOs X Jaguar.

Leo 4.1 beta 4                   November 20, 2003

This is the fourth official release of the reorganized 4.1 code base.

Warning: By default Leo 4.1 creates .leo files that can not be read by older versions of Leo.

Beta 4:
  - Fixes several "reorg" bugs, some of which affected plugins.
  - Allows @directives and section references when executing scripts!
  - More than one section reference may now appear on the same line.
  - Uses "utf-8" encoding for filenames under MacOS (Darwin)
  - Allows command or cmnd prefix for menu shortcuts under Darwin.
  - Wraps all os.path calls to that file and directory names can be converted to Unicode.
    This is necessary (but not sufficient?) to support Chinese file and directory names.

Beta 3 completes the reorg: many changes to the code.  Also fixes a LaTeX coloring bug.

Beta 2 fixes a startup problem on Linux: the "mbcs" text encoding is not valid on Linux.

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