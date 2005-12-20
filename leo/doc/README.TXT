Leo 4.4 alpha 5, cvs-snapshot 1                         December 19, 2005

This release is a cvs snapshot release.  It is not the full alpha 5 release.

You should be able to use this version safely; there are no known serious bugs.

All the major features of 4.4 are in place, but but several minibuffer commands
are not ready for prime time. 

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

Coming in later releases of Leo 4.4:
------------------------------------
- An auto-complete command that shows class members in the Completion tab.

- More support for mouseless Leo. There will be commands to manipulate all
aspects of Leo using commands, so your fingers will never have to leave the
keyboard.

- Support for Vim and other 'plain-key' input modes.