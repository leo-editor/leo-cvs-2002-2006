Leo 4.2 beta 3           August 10, 2004

Leo 4.2 Beta 3 is now available at http://sourceforge.net/projects/leo/

This version of Leo is feature complete.  Leo's core code has been stable for several months.

To do: most plugins work with the new code base, but other plugins need some more work.

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

- A new mod_scripting plugin is a big advance in scripting and testing.
test.leo now uses @test and @script nodes to define unit tests without
explicitly creating subclasses of unittest.TestCase. Converting scripts to unit
tests now takes a few seconds!

- A much faster and more robust spell checker plugin. (requires Python 2.3)

- Leo is now much more friendly to using spaces instead of tabs.

- The Execute Script command reports erroneous lines more clearly.

- The Perfect Import feature guarantee that Leo imports file exactly.

- Dozens of minor improvements.