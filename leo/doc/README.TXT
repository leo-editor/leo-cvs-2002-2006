Leo 4.2 beta 1           June 30, 2004

Beta 1 completes all fundamental work in the 4.2 code base. All essential code
is complete. Dozens of bugs have been fixed since the Alpha 3 release about a
month ago.

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

Still to do:

- Perfect import and @import. These will allow people to use Leo without having
to convert source files.
