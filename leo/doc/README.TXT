Important note: See INSTALL.TXT for installation instructions.

Leo is available at:  http://sourceforge.net/projects/leo/
Leo requires Python 2.1 or above and tcl/tk 8.3 or above.
Leo will work on Linux, Windows and MacOs X Jaguar.

Leo 4.2 alpha 1            April 14, 2004

This is a "semi-public" release of the new 4.2 code base.  I am releasing this code now to create a snapshot.  In particular, I shall use this snapshot to begin development work on the Macintosh.  This will allow me fix long-standing *nix bugs.

This main feature of this release is that Leo represents clones as nodes that
share trees of vnodes. To make this work Leo introduces _positions_. A position
is a location in the traversal of an outline.

This code appears stable.  I have been using the 4.2 code base for several weeks for all my work with no significant problems.  Nevertheless, this _is_ alpha (or even pre-alpha) quality code.  Use at your own risk.  Make frequent backups.

See the "4.2 Projects" node in LeoPy.leo for details of what has been done so far.  I shall be updating documentation more fully for the first beta release.

Leo 4.1 Final              February 20, 2004

Leo 4.1 Final is the culmination of four months of work. No significant bugs
have been reported since 4.1 rc4. Several people have contributed nifty plugins
recently. See leoPlugins.leo for full details.

The highlights of Leo 4.1:

- Leo runs in batch mode when invoked with --script aScriptFile.py
- Leo supports Unicode characters (e.g. Chinese) in path and file names.
- @directives and section references are now valid when executing scripts.
- @ignored and orphan nodes now valid in @file-nosent trees.
- Script-based find/change commands.
- Check Outline command.
- Hoist & DeHoist commands.
- A new gui-agnostic architecture: useful for batch mode and unit tests.
- Several new configuration settings.
- Many new unit tests.
- Excellent new plugins.
- A host of bug fixes.