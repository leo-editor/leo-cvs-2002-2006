Leo 4.4 alpha 1                                      October 15, 2005

Leo 4.4 alpha 1 is now available at:

http://sourceforge.net/project/showfiles.php?group_id=3458&package_id=29106

Leo 4.4 adds an Emacs-like minibuffer and support for all frequently-used Emacs
commands. Emacs users will be able to choose key bindings compatible with their
present finger habits. Eventually, Vim users will be able to do the same.

The new code in Leo 4.4 is a complete rewrite of most of the temacs and
usetemacs plugins. Those plugins have now been retired. Besides many code-level
improvements, it is now possible to specify key bindings for all commands
(including the new Emacs-style commands) using @shortcuts nodes in
leoSettings.leo.

This is definitely an alpha release. Several of the new Emacs-style commands are
buggy. However, improvements to Leo's error-handling logic mean that you should
be able to recover from the odd crash much more reliably than previously. I have
used this code for about a week with no significant problems at all.

To learn about Leo, see: http://webpages.charter.net/edreamleo/intro.html

The highlights of Leo 4.4 alpha 1:
----------------------------------
- Support for all frequently-used Emacs commands, including cursor and screen
movement, basic character, word and paragraph manipulation, and commands to
manipulate buffers, the kill ring, regions and rectangles. Almost all commands
found in the Emacs Cmds menu are implemented.

- An Emacs-like mini-buffer: you can now execute any command by name, both the
new Emacs-style commands and the traditional Leo commands.

- You can define key bindings using @shortcuts nodes in leoSettings.leo files.
You can define multiple sets of key bindings and switch between those sets
easily.

- Several fixes made to the 4.3 code base.
