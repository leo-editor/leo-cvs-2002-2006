leo.py version 1.0                             February 10, 2002

Version 1.0 adds many new features and fixes several bugs.
I recommend that all users of leo.py upgrade to this version.
This version deserves the number 1.0; it has no known bugs.
	
Here are the highlights of this release.  See the release notes in LeoDocs.leo for details.

1. Fixed bugs: the Tangle All and Tangle Marked commands didn't work at all.
Fixed several bugs in the Find and Change commands. 
The "Suboutline Only" option now applies to the Search All and Change All commands.
Settings in the Preferences Panel now "stick" properly to the currently selected window.
Fixed many minor bugs.

2. leo.py now re-marks @file trees as dirty if errors are found while writing those trees.
This makes it difficult to write derived files that will be out-of-synch when read again.

3. New commands and features:  Added the Revert, Select All, Delete, Sort Children,
Sort Siblings, Contract Parent (very useful!) and Toggle Active Pane commands,
and all commands in the Edit Body menu,
and all the Go To commands in the Move/Select menu.
The Show Invisibles commands is ugly, and useful nonetheless.

The Edit Body commands work much more reliably than the similar commands in the Borland version of Leo.
You may now specify Python scripts rather than .bat files in the Preferences panel.
Added a way, albeit clumsy, to cut and paste nodes between Borland Leo and leo.py.
When syntax coloring Python text, leo.py increments the auto-indentation by one tab after a trailing colon.
This provides a subtle reminder to add such colons.

4. leo.py handles events and shortcuts properly.
The shortcut for the Insert Node command is now Control-I, as it is in the Borland version of Leo.
Worked around a TK bug that prevented double-clicks from properly selecting words.
leo.py enables and disables all menu items properly.

Edward K. Ream
February 10, 2002