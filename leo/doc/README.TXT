Leo 4.4 alpha 2                                      November 2, 2005

Leo 4.4 alpha 2 is now available at:

http://sourceforge.net/project/showfiles.php?group_id=3458&package_id=29106
To learn about Leo, see: http://webpages.charter.net/edreamleo/intro.html

Leo 4.4a2 contains some of the most important changes to Leo's look
(tabbed log) and feel (per-pane key bindings) in Leo's history. This
release is a big step forward in meeting the following goals:

- To allow Emacs and Vim users to retain their present 'finger habits'.
- To support an emacs-like minibuffer, complete with typing completion.
- To make Leo usable without a mouse (mouseless Leo).

This is an alpha release: there are known bugs (see below). However, you should
be able to use this version safely. In particular, the Leo 4.4 code base
recovers from errors more reliably than all previous versions.

The highlights of Leo 4.4:
----------------------------------
- An Emacs-like mini-buffer: you can now execute any command by typing its long
name. Support for tab completion.

- A tabbed log pane. The Find and Spell Check commands now use tabs instead of
dialogs, making those commands much easier to use. Plugins or scripts can easily
create new tabs. The 'Completion' tab shows possible typing completions. 

- Support for almost all commands in the Emacs Cmds menu, including cursor
and screen movement, basic character, word and paragraph manipulation, and
commands to manipulate buffers, the kill ring, regions and rectangles.

- Per-pane key bindings. You can bind shortcuts to multiple commands depending
on which of Leo's panes presently has focus. For example, you can use arrow keys
to move nodes in the outline pane, while retaining their defaults in Leo's body
pane. Per-pane key binds are essential for mouseless Leo.

- @command nodes create minibuffer commands. You can bind key shortcuts to
@button and @command nodes.

- A rewrite of Leo's keystroke handling. In particular, Leo handles key events
immediately rather than queuing them for idle time.

- Several fixes made to the 4.3 code base. In particular, Leo 4.4 continues
after crashes much more reliably than in any previous version.

Known bugs in Leo 4.4a2
-----------------------
- Typing in the minibuffer doesn't work if the focus is 'in limbo', that is, not
in the outline, body or log panes. Leo usually forces the focus to the body pane
in such cases, but the code doesn't always work and sometimes causes other
problems. This *minor* annoyance will be fixed completely in Leo 4.4a3.

- Several minibuffer commands do not work; many new features lack unit tests.

Coming in later releases of Leo 4.4:
------------------------------------
- More support for mouseless Leo. There will be commands to manipulate all
aspects of Leo using commands, so your fingers will never have to leave the
keyboard.

- Support for Vim and other 'plain-key' input modes.