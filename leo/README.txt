leo.py version 2.4                             June 20, 2002

This version fixes some annoying bugs and adds some nice features:

1. Leo now properly highlights the headline of a newly created node and
the Edit Headline command now works properly.
Double and triple clicking in a headline now selects a word or the entire headline.

2. Drag and drop.  You can now reorganize outlines by dragging nodes around.
You must drag from a node's headline and release on another node's headline.
See LeoDocs.leo or Leo's web site for complete details.

3. You can now open .leo files in leo.py by double cliking on .leo files
provided that you associate leo.py with .leo files.
See LeoDocs.leo for detailed instructions about how to do this.

4. Improves error recovery when there are errors writing .leo files.

5. All parts of LeoDocs.leo now match the documentation on Leo's web site.
At long last, Leo's documentation is complete.


leo.py version 2.3                             June 12, 2002

This version fixes a minor problem with Leo.

1.  The code that reads and writes @file nodes now uses the directory containing the
.leo file as a default when the Default Tangle Directory setting is empty in the Prefrences panel.
This is a reasonable default because derived files are most often created in the same directory as
the .leo file.
BTW, the Tangle and Untangle commands have used this convention for a long time.

Note: This default allows us to distribute LeoPy.leo without specifying
a directory in the Preferences Panel.


leo.py version 2.2                             June 2, 2002

The version fixes two bugs that happen rarely and can cause loss of data when they do happen.

1. In certain circumstances leo.py v2.1 would delete most of an outline when
a node was moved in front of the previous root node!

2. All previous versions of leo.py will crash when saving body text containing unicode characters.
This could occur as the result of cutting and pasting text from another application into the body pane.
Leo.py now writes body text containing unicode characters using Python's u-prefixed notation.
That is, the body text is written as: u'escaped_text', where escaped text replaces unicode characters
not in the ascii character set by escape sequences of the form \uxxxx.
The result contains nothing but ascii characters, so leo.py will have no problem reading it.
Naturally, compilers and other tools may not understand Python's notation,
so you may have to convert escaped text to something that your tools can understand.

Also, the file LeoDocs.leo now more closely matches the documentation on Leo's web site.

Edward K. Ream
