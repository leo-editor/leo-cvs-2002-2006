Leo 4.3 alpha 4                 March 15, 2005

Leo 4.3 is the culmination of more than five months of work. This alpha 4
focuses on plugins: all known plugins are now in leoPlugins.leo. Most plugins
now work with the 4.3 code base. Warning: not all plugins have been tested
thorougly.

This alpha 4 release also adds the requently-requested Add Comments and Delete
Comments commands to Leo's Edit Body menu.

The defining features of Leo 4.3:

1. Leo now stores options in @settings trees, that is, outlines whose headline
is '@settings'. When opening a .leo file, Leo looks for @settings trees not only
in the outline being opened but also in various leoSettings.leo files.

The key design goal of @settings trees was that Leo's user options must be
infinitely flexible. That goal has been accomplished. Indeed, users can create
arbitrarily complex user options with @settings trees. Leo settings outlines
are, in fact, infinitely more flexible and powerful than any scheme based on
flat text.  Readers of Python's configParser shootout take note!

2. The Settings command temporarily replaces the outline pane with an outline
showing all the @settings trees in effect. The Settings command also replaces
the body pane with a "settings pane". This settings pane allows you to change
the settings selected in the outline pane using standard gui widgets. The
settings pane is dynamically created from nodes in the settings tree; it is as
extensible as the @settings tree itself.

3. Leo's read/write code in leoAtFile.py has been rewritten to support user-
defined tangling and untangling.  This is a major cleanup of Leo's core.

4. Leo now boasts a wonderful new Plugins Manager plugin. This plugin enables
and disables plugins automatically. You never have to mess with
pluginsManager.txt again! This plugin also tells you everything you need to know
about each plugin. Finally, this plugin also lets you download plugins from
Leo's cvs site! Many thanks to Paul Patterson for this excellent work.

5. You can install third-party extensions in Leo's extensions directory. Leo
will attempt to import such extensions from the extensions directory if normal
imports fail. Leo is distributed with Pmw (Python Mega Widgets), path.py and
sets.py in this directory.