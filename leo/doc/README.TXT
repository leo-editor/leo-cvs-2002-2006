Leo 4.2 beta 2           July 5, 2004
Leo 4.2 beta 1           June 30, 2004

The highlights of 4.2 beta 2:

- Leo now writes the entire contents of @ignore'd @thin trees to the .leo file.
This change ensures that users can create and remove @ignore directives without
any chance of losing data inadvertently.

- Leo now saves and restores marks and the expansion state of nodes in @thin trees.

- Leo marks @thin nodes as dirty whenever they become "newly unignored", i.e.,
when an @thin node no longer falls in the range of an @ignore directive.

Beta 1 completes all fundamental work in the 4.2 code base. All essential code
is complete. Dozens of bugs have been fixed since the Alpha 3 release about a
month ago.

Known bugs in 4.2 beta 2:

- Not all plugins work correctly.
- Some plugins leak memory very slightly.

The highlights of Leo 4.2:

- @thin trees make Leo much more friendly to cvs. Files derived from @thin can
be committed to cvs and updated from cvs without having to commit or update the
corresponding .leo file. There is no longer any need to keep .leo files and
derived files in synch.

- Leo's data structures have been reorganized. As a result, all outline
operations are much faster. To support this organization, scripts that traverse
Leo's data structures must now use a positions rather than vnodes. Old scripts
that appear to use vnodes will still work because methods like c.currentVnode
that appear to return vnodes actually return positions.

Other features of 4.2:

- Leo is now much more friendly to using spaces instead of tabs.
- The Execute Script command reports erroneous lines more clearly.
- The usual assortment of bug features and minor features.

Coming soon in 4.2:

- Perfect Import will guarantee that Leo imports file perfectly.
- @import will allow you to study files using Leo without changing those files.