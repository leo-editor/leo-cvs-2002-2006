Leo 4.3 alpha 2 is now available at http://sourceforge.net/projects/leo/

Leo 4.3 is the culmination of more than five months of work. In spite
of its status, I recommend this release over any 4.2 release.

This alpha 2 release corrects various bugs and distribution problems.
It also adds these new features:

- Adds 'word', 'line' and 'node' undo granularities.
- Predefines 'c','g', and 'p' in scripts and unit tests.
- Added support for top-level init functions in plugins.
- Buttons can remove themselves when their scripts fail.

The defining features of Leo 4.3:
---------------------------------
1. Leo now stores options in @settings trees, that is, outlines whose
headline is '@settings'. When opening a .leo file, Leo looks for
@settings trees not only in the outline being opened but also in
various leoSettings.leo files.

Users can create arbitrarily complex user options with @settings
trees. Leo settings outlines are, in fact, infinitely more flexible
and powerful than any scheme based on flat text. Readers of Python's
configParser shootout take note.

2. The Preferences command temporarily replaces the outline pane with
an outline showing all the @settings trees in effect. The Preferences
command also replaces the body pane with a "settings pane". This
settings pane allows you to change the settings selected in the
outline pane using standard gui widgets.

3. Leo's read/write code in leoAtFile.py has been rewritten to support
user-defined tangling and untangling. This is a major cleanup of
Leo's core.

4. Leo now boasts an excellent Plugins Manager plugin. This plugin
enables and disables plugins automatically and tells you everything
you need to know about each plugin. This plugin also lets you download
plugins from Leo's cvs site.

5. You can install third-party extensions in Leo's extensions
directory. Leo will attempt to import such extensions from the
extensions directory when normal imports fail. The distribution contains
Python Mega Widgets in the extensions directory.