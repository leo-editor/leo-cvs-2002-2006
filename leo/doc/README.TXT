Important note: See INSTALL.TXT for installation instructions.

Leo is available at:  http://sourceforge.net/projects/leo/
Leo requires Python 2.1 or above and tcl/tk 8.3 or above.
Leo will work on Linux, Windows and MacOs X Jaguar.

Leo 4.1 Release Candidate 2              December 18, 2003

This release fixes minor bugs in Leo and its plugins.

There are no known bugs in this version of Leo.

The highlights of 4.1:
----------------------
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
- A host of bug fixes.