Important note: See INSTALL.TXT for installation instructions.

Leo is available at:  http://sourceforge.net/projects/leo/
Leo requires Python 2.1 or above and tcl/tk 8.3 or above.
Leo will work on Linux, Windows and MacOs X Jaguar.

Leo 4.1 beta 5                   December 5, 2003

For the first time in months there are no serious bugs outstanding.

Warning: By default Leo 4.1 creates .leo files that can not be read by older versions of Leo.

Warning: Use the __wx_gui.py plugin with _extreme_ caution until further notice:
bugs in this plugin could cause body text to be lost when changing nodes.

Beta 5:
  * Leo runs in batch mode when invoked with --script aScriptFile.py
    - Created "null gui" classes that do not use any gui code.
  * Leo supports Unicode characters (e.g. Chinese) in path and file names.
  * Fixed several long-standing bugs:
    - Fixed several minor problems with the Extract Section and Import commands.
    - Fixed problem that prevent the Find panel from working on the Mac.
    - Improved @url handling so that @url file:\\path\x.leo works properly.
    - Improved support for @lineending platform.
    - Leo honors outline/body pane ratio when opening .leo files.
    - Leo now ensures that newly-opened windows fit entirely on the screen.
    - Fixed a crasher when Undoing a Change All command when searching headlines.
  - Fixed other bugs resulting from the 4.1 reorg:
    - Fixed problem loading plugins on Linux.
    - Fixed crashers in the Extract Section and Extract commands.
    - Fixed a crasher when writing a file containing an undefined section.
    - Removed duplicate bindings in popup menus.
    - Made sure to show Leo's windows in wx gui plugin.

Beta 4:
  - Fixed several "reorg" bugs, some of which affected plugins.
  - Allow @directives and section references when executing scripts!
  - More than one section reference may now appear on the same line.
  - Use "utf-8" encoding for filenames under MacOS (Darwin)
  - Allow command or cmnd prefix for menu shortcuts under Darwin.
	  
Beta 3:
  - Completed the reorg, making _many_ changes to the code base.
  - Fixed a LaTeX coloring bug

Beta 2:
  - Fixed a startup problem on Linux: the "mbcs" text encoding is not valid on Linux.

Beta 1:
  * Script-based find/change commands.
  - Hoist & DeHoist commands for viewing parts of an outline.
  - Check Outline command finds user clone mistakes.
  * New configuration settings:
    - use_gnx specifies whether .leo files use integers as indices:
      use_gnx = 0 makes .leo files compatible with previous versions of Leo.
      use_gnx = 1 makes .leo files cvs-friendly
    - config_encoding specifies the encoding of leoConfig.txt.
  * Several significant code-level changes:
    - The 4.1 code base has been reorganized to support gui plugins.
    - An example wx_gui plugin is partly functional.
    - Created a flexible framework for creating & running regression tests.
    - app.forceShutdown now works when called from plugins.