Important note: See INSTALL.TXT for installation instructions.

Leo is available at:  http://sourceforge.net/projects/leo/
Leo requires Python 2.1 or above and tcl/tk 8.3 or above.
Leo will work on Linux, Windows and MacOs X Jaguar.

Leo 4.0 beta 3                      October 9, 2003

This is the third public release of Leo 4.0. There are no known serious bugs in
this version of Leo. This will likely be the last beta release before 4.0 final.

Highlights of 4.0 beta 3
------------------------

- Fixed problems with setting Leo's window icons.
- Plugins may now save their own information in <v> and <t> elements in .leo files.
- The usual assortment of bug fixes and minor improvements.

Leo 4.0 beta 2                      October 3, 2003

This is the second public release of Leo 4.0. There are no known serious bugs
in this version of Leo.  Version 4.0 is the culmination of over a year of
collaborative design work and several months of actual implementation.

Highlights of 4.0 beta 2
------------------------
* Fixed several bugs:
  - Fixed several problems with reading and writing 4.0 derived files.
  - Fixed several Unicode-related bugs.
  - Fixed a crasher in the Go To Line Number command.
  - Fixed a problem with Importing Python files.
* Important improvements:
  - Added allow_clone_drags setting.  N.B. Allows Leo to be used with Aqua.
  - When running Python 2.3 Leo can now create window icons without third-party packages.
- The usual minor improvements and bug fixes.

Highlights of 4.0 beta 1
------------------------
** Improved and simplified format of derived files.
  - Eliminated child indices, extraneous blank lines and @body sentinels.
  - Eliminated @node sentinels that indicate outline structure.
  - New @nl and @nonl sentinels indicate where newlines are and aren't.
  - These changes will largely eliminate unwanted cvs conflicts.
** Greatly improved error handling.
  - Reading derived files _never_ alter outline structure or links.
  - Read errors leave the outline completely unchanged.
  - Broken clone links are gone forever.
  - As a result, using 4.0 is much safer than all previous versions.
** Full compatibility will previous versions of Leo.
  - Leo reads all derived files properly, regardless of version.
  - Leo writes new-format derived files by default, and this default may be changed.
* New commands:
  - Write 3.x Derived File command and Write 4.x Derived File command.
  - Import Derived File.
  - Clear Recent Files.

- Several new plugins.
- Several minor bug fixes.