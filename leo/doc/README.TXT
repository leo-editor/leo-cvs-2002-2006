Important note: See INSTALL.TXT for installation instructions.

Leo is available at:  http://sourceforge.net/projects/leo/
Leo requires Python 2.1 or above and tcl/tk 8.3 or above.
Leo will work on Linux, Windows and MacOs X Jaguar.

Leo 4.0 final                     October 17, 2003

More than a year in the making, Leo 4.0 is finally here.

Highlights of 4.0 final:
-----------------------

** Improved and simplified format of derived files.
	- Eliminated child indices, extraneous blank lines and @body sentinels.
	- Eliminated @node sentinels that indicate outline structure.
	- New @nl and @nonl sentinels indicate where newlines are and aren't.
	- These changes will largely eliminate unwanted cvs conflicts.

** Greatly improved error handling.
	- Reading derived files _never_ alter outline structure or links.
	- Read errors leave the outline completely unchanged.
	- Broken clone links are gone forever.
	- As a result, 4.0 is much safer than all previous versions.

** Full compatibility will previous versions of Leo.
	- Leo 4.0 reads all derived files properly, regardless of version.
	- Leo writes new-format derived files by default, and this default may be changed.
	- New commands in the read/write menu allow you to explicitly specify the format of derived files.

* New commands:
	- Write 3.x Derived File and Write 4.x Derived File.
	- Import Derived File.
	- Clear Recent Files.

* Dozens of other improvements, including:
	- Better Unicode support.
	- New configuration settings.
	- Several new plugins.

See the notes for the various beta releases for full details.