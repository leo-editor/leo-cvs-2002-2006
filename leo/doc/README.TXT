Important note: See INSTALL.TXT for installation instructions.

Leo is available at:  http://sourceforge.net/projects/leo/
Leo requires Python 2.1 or above and tcl/tk 8.3 or above.
Leo will work on Linux, Windows and MacOs X Jaguar.

Leo 4.1 alpha 1                   November 2, 2003

1. Implements the use_gnx setting:
	1: tnode indices in .leo files have the form id.timestamp.n (n optional)
       Strongly recommended when using cvs.
 	0: tnode indices in .leo files are integers.
       For compatibility with Leo 3.x file format.

N.B.  It is possible to convert between 3.x and 4.1 file formats by changing the use_gnx setting.  This is tricky, and the present code appears to work.  However, problems might remain: that's why this is an alpha version.

2. Moves gui-dependent code out of Leo's core.  Known bug: the Extract command eat an extra character.  This will be fixed soon.