leo.py version 2.0
March 4, 2002

leo.py v2.0 and Borland Leo v2.6 are being released simultaneously.
I urge all users of Leo to upgrade to one or both of these versions.
Note: the Untangle commands of both v2.0 and v2.6 should be considered beta quality.
Please report any problems with Untangle ASAP.

This is an important milestone in Leo's history, for several reasons:

1. For the first time, leo.py (v2.0) and the Borland Leo (v2.6) are functionally identical.
In particular, their respective Tangle commands produce identical output.

2. All "mission critical" aspects of leo.py are now complete:
only the Import commands remain unfinished.
leo.py v2.0 adds unlimited Undo/Redo, Untangle and full syntax coloring.
Unlimited Undo/Redo are reason enough to upgrade to v2.0.

3. leo.py v2.0 and Borland Leo v2.6 introduce an optimized format for derived files:
both versions remove blank lines from between sentinel lines.
This is an upward compatible change in the format of derived files:
leo.py v2.0 and Borland Leo v2.6 can read derived files from all previous versions of Leo,
but previous versions of Leo can not read derived files without blank lines.

Details:

1. leo.py v2.0 removes blanks from between sentinel lines in derived files.

leo.py v2.0 removes blanks lines between sentinels by default.
To cause leo.py not to remove blank lines do the following.
In the section called << initialize atFile ivars >> in leoAtFile.py,
change self.suppress_newlines = true to self.suppress_newlines = false.

Note: leo.py v2.0 can read derived files without blank lines between sentinels
regardless of the setting of self.suppress_newlines.

Removing blank lines requires a new kind of sentinel, the "verbatimAfterRef" sentinel.
This allows Leo to handle comments following section references that would otherwise
be treated as sentinels themselves.  For example:
   
   << section >> #+others

2. leo.py supports unlimited Undo and Redo.
All outline operations and all typing operations may be undone and redone.
Undo state persists even after Saves.  Even the Change All command is undoable.
Only the "Read @file Nodes" command is undoable; it clears the entire undo state.
This command raises a dialog to allow the user to cancel.

Think of the actions that may be Undone or Redone as a string of beads.
A "bead pointer" points to the present bead.
Performing an operation creates a new bead after the present bead and removes
all following beads.
Undoing an operation moves the bead pointer backwards;
redoing an operation moves the bead pointer forwards.
The Undo command is disabled when the bead pointer moves in front of the first bead;
the Redo command is disabled when the bead pointer points to the last bead.

3. leo.py syntax colors all languages mentioned in the Preferences Panel.

4. Fixed several minor syntax coloring bugs.
a) Show Invisibles command works in @nocolor mode.
b) @unit, @root, @nocolor and @color now terminate doc parts.
c) Three characters were colored blue at the start of a section def in: <<name>>=
  This didn't show up if there is a space after the <<.

5. Leo adds extra space at the end of headlines so that headlines now have enough room to show all text.  This works around an apparent Tk bug.

6. Suppressed auto-indent for Python in @nocolor mode.

7. leo.py v2.0 fixes two bugs present in Borland v2.5 and fixed in Borland v2.6:
a) Untangle did not work properly for languages like Perl and Python that do not have block comments. 
b) Untangle did not recognize @ on a line by itself as the start of a doc part.

8. Previous versions of untangle silently trimmed trailing lines from all nodes,
which seems rude.

9. @c now works the same as @code.
This makes the syntax colorers agree with what the Tangle commands actually do.
Previously, the syntax colorers indicated that everything following an @c was code,
while the Tangle commands placed everything following an @c in the doc part!

10. Made some changes for non-Windows users:
a) The font size for code text is now 12 on Linux.
b) Changed code so that the path to the Icons folder is computed correctly on all platforms.
These changes were contributed by Eric S. Johansson.

Edward K. Ream