Leo 4.4 alpha 5                                             January 6, 2006

This release completes the last major feature of Leo 4.4:

- User-specified key-binding modes.
- Support for multiple key-bindings for individual minibuffer commands.

This will be the last alpha version of Leo 4.4. Beta 1 is coming in about a
week. You should be able to use this version safely; there are no known serious
bugs.

To learn about Leo, see: http://webpages.charter.net/edreamleo/intro.html

The highlights of Leo 4.4:
----------------------------------
- An Emacs-like mini-buffer: you can now execute any command by typing its long
name. Support for tab completion.

- A tabbed log pane. The Find and Spell Check commands now use tabs instead of
dialogs, making those commands much easier to use. Plugins or scripts can easily
create new tabs. The Completion tab shows possible typing completions.

- Support for almost all commands in the Emacs Cmds menu, including cursor
and screen movement, basic character, word and paragraph manipulation, and
commands to manipulate buffers, the kill ring, regions and rectangles.

- Per-pane key bindings. You can bind shortcuts to multiple commands depending
on which of Leo's panes presently has focus. For example, you can use arrow keys
to move nodes in the outline pane, while retaining their defaults in Leo's body
pane. Per-pane key bindings are essential for mouseless Leo.

- @command nodes create minibuffer commands. You can bind key shortcuts to
@button and @command nodes.

- A rewrite of Leo's keystroke handling. In particular, Leo handles key events
immediately rather than queuing them for idle time.

- Leo recovers from crashes much more reliably than in any previous version.

- Leo updates the screen immediately rather than waiting for idle time.
This 'Newer World Order' simplifies the code and improves performance.

- User-specified key-binding modes. This feature makes it possible to emulate all
aspects of Emacs and Vim as far as key bindings are concerned.