leo.py version 0.08                                                                                     February 3, 2002

Version 0.08 adds important new features and fixes several bugs.
All users of version 0.07 should upgrade to this version.
This code seems solid, and significant bugs may remain.
Note: this code has been tested only on Windows XP.
Please report any problems with Linux or Macintosh.

This is the first version of Leo to feel as smooth as the Borland v2.5.
Indeed, leo.py is now less buggy than v2.5;
the Borland version will soon be upgraded to match leo.py.

Here is a summary of new features.  See LeoDocs.leo for full details.

1. The Find and Change commands are fully functional.
These commands support Tk's "advanced regular expressions" when the
"pattern match" option is checked.
Tk's regular expressions are documented at:
  http://tcl.activestate.com/man/tcl8.4/TclCmd/regexp.htm

2. The Tangle commands work; leo.py now supports @root trees.
The next release will support the Untangle commands.
Converting the Untangle code to Python is almost complete.

3. Leo now ensures that the currently selected headline is always visible,
scrolling the outline pane as needed.

4. Improved Leo's memory management and eliminated several serious bugs.
One bug caused errors while reading @file trees.
Eliminating this is a huge step forward.
This bug exists in the Borland version of Leo and will be fixed soon.

5. Leo now underlines undefined section references.
Added support for hyperlinking, but disabled hyperlinking because it is
not very useful without browser navigation buttons.

Edward K. Ream
February 3, 2002