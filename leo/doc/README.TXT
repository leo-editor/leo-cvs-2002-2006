Leo 4.2 Final       September 20, 2004

Leo 4.2 Final is now available at http://sourceforge.net/projects/leo/

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

- Leo draws large outlines more quickly with less memory used.

- A much faster and more robust spell checker plugin. (requires Python 2.3)

- Leo is now much more friendly to using spaces instead of tabs.

- The Execute Script command reports erroneous lines more clearly.

- Dozens of other improvements.