Leo 4.2 alpha 2           May 18, 2004

This is an important milestone in Leo's history; the two defining features of the 4.2 code base are complete:

1. This is the first stable version using the "shared nodes" code base.

Shared nodes dramatically improve the time needed to insert, delete, and move nodes.  Moreover, the new code base is code compatible with the old.  Indeed, significant parts of Leo still use the old code base.

2. This is the first version to use @file-thin for most derived files.

@file-thin makes it possible to use Leo effectively in a cvs environment.  Indeed, cvs now contains only a "dummy" version of LeoPy.leo.  The idea is that:

- LeoPyRef.leo hardly ever changes.  Developers will download LeoPyRef.leo once from cvs, then rename LeoPyRef.leo to be LeoPy.leo.  LeoPy.leo is private to each developer.

- Developers will commit and update to cvs only thin derived files.  There is no longer any need to keep .leo files and the files derived from them "in synch".

- Similar remarks apply to LeoPlugins.leo.  Cvs contains only LeoPluginsRef.leo, and contributors will need only to submit thin derived files.

I have been using the new code base without incident for weeks now, and I am fairly confident that it is safe to use.  Nevertheless, I would suggest routine caution when dealing with this version until more people have tested it.

Known bugs

- Cutting and pasting an @file-thin node does not work properly.  This will be easy to fix, I think.

- The present algorithm for reading thin derived files probably does not handle properly the situation in which a named node is some kind of grand child of the referencing node rather than being an immediate child of the referencing node.  This is a rare situation, easily avoided, and it doesn't happen at all in LeoPy.leo.  Nevertheless, something must be done.

Other improvements:

- Fixed a number of problems with using Leo on MacOS X.  In particular, Leo now uses the clover key as is usual on the Mac.  More Mac and *nix specific improvements are coming.

Still to do:

- Perfect import and @import.
- Make the Go To Line Number command work with @file-thin files.
- Fix minor bugs and add new features
  See the "To Do: 4.2" node in the leoToDo.txt node in LeoPy.leo.
