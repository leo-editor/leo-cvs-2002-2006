#@+leo-ver=4-thin
#@+node:ekr.20050723062822:@thin __core_emacs.py
''' A plugin to provide Emacs commands.
Will move to Leo's core eventually.'''

#@<< imports >>
#@+node:ekr.20050723062822.1:<< imports >>
import leoGlobals as g
import leoPlugins

if 0:
    #@    << SwingMacs imports >>
    #@+node:ekr.20050724075114:<< SwingMacs imports >>
    from __future__ import generators
    import javax.swing as swing
    import javax.swing.event as sevent
    import javax.swing.text as stext
    import java.awt.event as aevent
    import java.util.regex as regex
    import java.awt as awt
    import java.lang 
    import java.io
    
    from DefCallable import DefCallable
    import LeoUtilities
    #@nonl
    #@-node:ekr.20050724075114:<< SwingMacs imports >>
    #@nl

import leoColor
import leoPlugins
import leoNodes
import leoTkinterFrame

try:
    import Tkinter as Tk
    import ScrolledText
    import tkFileDialog
    import tkFont
except ImportError:
    Tk = None

import ConfigParser
import cPickle
import difflib
import os
import re
import string
import sys
import weakref
#@nonl
#@-node:ekr.20050723062822.1:<< imports >>
#@nl
#@<< modification log >>
#@+node:ekr.20050725074202:<< modification log >>
#@@nocolor

# This discusses changes made to usetemacs/temacs code bases.

#@+others
#@+node:ekr.20050725074202.1:Rewrote buildBufferList
#@+at 
#@nonl
# There may be bugs here.  The old code had definite strange aspects to it.
#@-at
#@nonl
#@-node:ekr.20050725074202.1:Rewrote buildBufferList
#@+node:ekr.20050725074202.2:Removed Emacs_instances class var
#@+at 
#@nonl
# createBindings now sets c.emacs, so modifyOnBodyKey just uses c.emacs.
#@-at
#@nonl
#@-node:ekr.20050725074202.2:Removed Emacs_instances class var
#@+node:ekr.20050725074607:Added c ivar to Emacs class
#@+at 
#@nonl
# This is an important addition:  it guarantees that the proper commander is 
# always used.
#@-at
#@nonl
#@-node:ekr.20050725074607:Added c ivar to Emacs class
#@+node:ekr.20050725075301:Removed labels class var
#@+at 
#@nonl
# This is not needed.  createBindings is called at most once per commander.
#@-at
#@nonl
#@-node:ekr.20050725075301:Removed labels class var
#@+node:ekr.20050725132137:Added baseCommands class
#@+at 
#@nonl
# Subclasses of baseCommands class should implement getPublicCommands.
# 
# This returns a dict whose keys are emacs command names and whose values are 
# bound methods.
#@-at
#@nonl
#@-node:ekr.20050725132137:Added baseCommands class
#@-others
#@nonl
#@-node:ekr.20050725074202:<< modification log >>
#@nl
#@<< to do >>
#@+node:ekr.20050729080859:<< to do >>
#@@nocolor
#@+at
# 
# - Allow redefinitions of emacs command names (so people can use their own 
# unique prefixes).
# 
# - convertCommandName utility converts to and from emacs-style (with '-' 
# chars) to python/leo style (with capitalization).
# 
# - Eliminate all hard constants (except for tables of defaults).
# 
#@-at
#@@c
#@+others
#@+node:ekr.20050729081915:Improve minibuffer
#@+at
# 
# 
# - Allow one (or more?) stoppers that prevent backspacing.
# - Backspacing after tab-completion should go back to previously typed char 
# and remove _that_.
# - Use status line (disable it) for miniBuffer.
# - Create editor helper class.
# 
# Rather than passing an event to commands, masterCommand should globals for 
# state, miniBuffer, etc.
#@-at
#@-node:ekr.20050729081915:Improve minibuffer
#@+node:ekr.20050729081915.1:Improve state handling (simplify masterCommand)
#@+at
# 
# Eliminate state-related tables.
# 
# Master-command shouldn't need them.
#@-at
#@nonl
#@-node:ekr.20050729081915.1:Improve state handling (simplify masterCommand)
#@+node:ekr.20050729081915.2:User options
#@+at
# 
# - 'Emacs Compatibility' option: binds keys as done in present plugin.
# 
# - 'Emacs Menu option':  On by default: adds emacs option.
# 
# - Get keystrokes from user options.
# 
# - User-specified keys for alt-x, control-c, etc.
#@-at
#@-node:ekr.20050729081915.2:User options
#@+node:ekr.20050729120313:altX abbreviations and corresponding commands
#@+at
# 
# fd  find-dialog
# od  options-dialog
# f   find
# fr  find-reverse
# fx  find-regex
# frx find-regex-reverse
# fxr find-regex-reverse
# fw  find-word
# i   incremental-find
# ir  incremental-find-reverse
# ix  incremental-find-regex
# irx incremental-find-regex-reverse
# ixr incremental-find-regex-reverse
# sf  set-find-text
# sr  set-find-replace
# ss  script-search
# ssr script-search-reverse
# tfh  toggle-find-search-headline
# tfb  toggle-find-search-body
# tfw  toggle-find-word
# tfn  toggle-find-node-only
# tfi  toggle-find-ignore-case
# tfmc toggle-find-mark-changes
# tfmf toggle-find-mark-finds
#@-at
#@nonl
#@-node:ekr.20050729120313:altX abbreviations and corresponding commands
#@-others
#@nonl
#@-node:ekr.20050729080859:<< to do >>
#@nl

USE_TEMACS = True  # False:  use SwingMacs code base  (will probably never happen).

if USE_TEMACS:
    #@    << define usetemacs globals >>
    #@+node:ekr.20050724080034:<< define usetemacs globals >>
    haveseen = weakref.WeakKeyDictionary()
    extensions = []
    new_keystrokes = {}
    leocommandnames = None
    
    # For buffer interaction methods.
    tnodestnodes = {} # Keys are commanders.  Values are dicts.
    positions =  {}
    
    # Original versions of methods.
    orig_Bindings = None
    orig_OnBodyKey = None
    #@nonl
    #@-node:ekr.20050724080034:<< define usetemacs globals >>
    #@nl
else:
    extensions = []
    commandsFromPlugins = {}

#@+others
#@+node:ekr.20050723062822.2:init (plugin)
def init ():

    ok = Tk and not g.app.unitTesting

    if ok:
        if g.app.gui is None:
            g.app.createTkGui(__file__)

        ok = g.app.gui.guiName() == "tkinter"
        if ok:
            g.plugin_signon(__name__)
            if USE_TEMACS:
                #@                << override createBindings and onBodyKey >>
                #@+node:ekr.20050724080456:<< override createBindings and onBodyKey >>
                global orig_Bindings, orig_OnBodyKey
                
                orig_Bindings = leoTkinterFrame.leoTkinterBody.createBindings
                leoTkinterFrame.leoTkinterBody.createBindings = createBindings
                
                orig_OnBodyKey = leoTkinterFrame.leoTkinterBody.onBodyKey
                leoTkinterFrame.leoTkinterBody.onBodyKey = modifyOnBodyKey
                #@nonl
                #@-node:ekr.20050724080456:<< override createBindings and onBodyKey >>
                #@nl
                leoPlugins.registerHandler(('open2',"new"),addMenu)
            else:
                global extensions
                extensions = lookForExtensions()
                leoPlugins.registerHandler(('open2',"new"),createEmacs)

    return ok
#@nonl
#@-node:ekr.20050723062822.2:init (plugin)
#@+node:ekr.20050724074642.16:loadConfig (from usetemacs)
def loadConfig ():
    '''Loads Emacs extensions and new keystrokes to be added to Emacs instances'''
    pth = os.path.split(g.app.loadDir)
    aini = pth [0] + r"/plugins/usetemacs.ini"
    if os.path.exists(aini):

        cp = ConfigParser.ConfigParser()
        cp.read(aini)
        section = None
        for z in cp.sections():
            if z.strip() == 'extensions':
                section = z
                break

        if section:
            for z in cp.options(section):
                extension = cp.get(section,z)
                try:
                    ex = __import__(extension)
                    extensions.append(ex)
                except Exception, x:
                    g.es("Could not load %s because of %s" % (extension,x),color='red')

        kstroke_sec = None
        for z in cp.sections():
            if z.strip() == 'newkeystrokes':
                kstroke_sec = z
                break
        if kstroke_sec:
            for z in cp.options(kstroke_sec):
                new_keystrokes [z.capitalize()] = cp.get(kstroke_sec,z)
#@nonl
#@-node:ekr.20050724074642.16:loadConfig (from usetemacs)
#@+node:ekr.20050724074619.1:Birth (From usetemacs)
# Based on version .57 EKR:
#@nonl
#@+node:ekr.20050724074642.17:usetemacs Hooks
#@+node:ekr.20050724074642.18:addMenu
def addMenu (tag,keywords):

    '''Adds the Temacs Help option to Leo's Help menu'''

    c = keywords.get('c')
    if not c: return

    men = c.frame.menu.getMenu('Help')
    men.add_separator()
    men.add_command(label='Temacs Help',command=seeHelp)
#@nonl
#@-node:ekr.20050724074642.18:addMenu
#@+node:ekr.20050724074642.19:seeHelp
def seeHelp ():
    '''Opens a Help dialog that shows the Emac systems commands and keystrokes'''
    tl = Tk.Toplevel()
    ms = tl.maxsize()
    tl.geometry('%sx%s+0+0' % ((ms[0]/3)*2,ms[1]/2)) #half the screen height, half the screen width
    tl.title("Temacs Help")
    fixedFont = tkFont.Font(family='Fixed',size=14)
    tc = ScrolledText.ScrolledText(tl,font=fixedFont,background='white',wrap='word')
    sbar = Tk.Scrollbar(tc.frame,orient='horizontal')
    sbar.configure(command=tc.xview)
    tc.configure(xscrollcommand=sbar.set)
    sbar.pack(side='bottom',fill='x')
    for z in tc.frame.children.values():
        sbar.pack_configure(before=z)
    tc.insert('1.0',Emacs.getHelpText())
    lc = '''\n---------Leo Commands-----------\n'''
    tc.insert('end',lc)
    leocommandnames.sort()
    lstring = '\n'.join(leocommandnames)
    tc.insert('end',lstring)
    #@    << define clz >>
    #@+node:ekr.20050724074642.20:<< define clz >>
    def clz (tl=tl):
        tl.withdraw()
        tl.destroy()
    #@nonl
    #@-node:ekr.20050724074642.20:<< define clz >>
    #@nl
    g = Tk.Frame(tl)
    g.pack(side='bottom')
    tc.pack(side='top',expand=1,fill='both')
    e = Tk.Label(g,text='Search:')
    e.pack(side='left')
    ef = Tk.Entry(g,background='white',foreground='blue')
    ef.pack(side='left')
    #@    << define search >>
    #@+node:ekr.20050724074642.21:<< define search >>
    def search ():
    
        #stext = ef.getvalue()
        stext = ef.get()
        #tc = t.component( 'text' )
        tc.tag_delete('found')
        tc.tag_configure('found',background='red')
        ins = tc.index('insert')
        ind = tc.search(stext,'insert',stopindex='end',nocase=True)
        if not ind:
            ind = tc.search(stext,'1.0',stopindex='end',nocase=True)
        if ind:
            tc.mark_set('insert','%s +%sc' % (ind,len(stext)))
            tc.tag_add('found','insert -%sc' % len(stext),'insert')
            tc.see(ind)
    #@nonl
    #@-node:ekr.20050724074642.21:<< define search >>
    #@nl
    go = Tk.Button(g,text='Go',command=search)
    go.pack(side='left')
    b = Tk.Button(g,text='Close',command=clz)
    b.pack(side='left')
    #@    << define watch >>
    #@+node:ekr.20050724074642.22:<< define watch >>
    def watch (event):
        search()
    #@nonl
    #@-node:ekr.20050724074642.22:<< define watch >>
    #@nl
    ef.bind('<Return>',watch)
#@nonl
#@-node:ekr.20050724074642.19:seeHelp
#@+node:ekr.20050724075352.42:getHelpText TO BE REMOVED
def getHelpText ():
    '''This returns a string that describes what all the
    keystrokes do with a bound Text widget.'''
    help_t =['Buffer Keyboard Commands:', 
    '----------------------------------------\n', 
    '<Control-p>: move up one line', 
    '<Control-n>: move down one line', 
    '<Control-f>: move forward one char', 
    '<Conftol-b>: move backward one char', 
    '<Control-o>: insert newline', 
    '<Control-Alt-o> : insert newline and indent', 
    '<Control-j>: insert newline and tab', 
    '<Alt-<> : move to start of Buffer', 
    '<Alt- >'+' >: move to end of Buffer', 
    '<Control a>: move to start of line', 
    '<Control e> :move to end of line', 
    '<Alt-Up>: move to start of line', 
    '<Alt-Down>: move to end of line', 
    '<Alt b>: move one word backward', 
    '<Alt f> : move one word forward', 
    '<Control - Right Arrow>: move one word forward', 
    '<Control - Left Arrow>: move one word backwards', 
    '<Alt-m> : move to beginning of indentation', 
    '<Alt-g> : goto line number', 
    '<Control-v>: scroll forward one screen', 
    '<Alt-v>: scroll up one screen', 
    '<Alt-a>: move back one sentence', 
    '<Alt-e>: move forward one sentence', 
    '<Alt-}>: move forward one paragraph', 
    '<Alt-{>: move backwards one paragraph', 
    '<Alt-:> evaluate a Python expression in the minibuffer and insert the value in the current buffer', 
    'Esc Esc : evaluate a Python expression in the minibuffer and insert the value in the current buffer', 
    '<Control-x . >: set fill prefix', 
    '<Alt-q>: fill paragraph', 
    '<Alt-h>: select current or next paragraph', 
    '<Control-x Control-@>: pop global mark', 
    '<Control-u>: universal command, repeats the next command n times.', 
    '<Alt -n > : n is a number.  Processes the next command n times.', 
    '<Control-x (>: start definition of kbd macro', 
    '<Control-x ) > : stop definition of kbd macro', 
    '<Control-x e : execute last macro defined', 
    '<Control-u Control-x ( >: execute last macro and edit', 
    '<Control-x Esc Esc >: execute last complex command( last Alt-x command', 
    '<Control-x Control-c >: save buffers kill Emacs', 
    '''<Control-x u > : advertised undo.   This function utilizes the environments.
    If the buffer is not configure explicitly, there is no operation.''', 
    '<Control-_>: advertised undo.  See above', 
    '<Control-z>: iconfify frame', 
    '----------------------------------------\n', 
    '<Delete> : delete previous character', 
    '<Control d>: delete next character', 
    '<Control k> : delete from cursor to end of line. Text goes to kill buffer', 
    '<Alt d>: delete word. Word goes to kill buffer', 
    '<Alt Delete>: delete previous word. Word goes to kill buffer', 
    '<Alt k >: delete current sentence. Sentence goes to kill buffer', 
    '<Control x Delete>: delete previous sentence. Sentence goes to kill buffer', 
    '<Control y >: yank last deleted text segment from\n kill buffer and inserts it.', 
    '<Alt y >: cycle and yank through kill buffer.\n', 
    '<Alt z >: zap to typed letter. Text goes to kill buffer', 
    '<Alt-^ >: join this line to the previous one', 
    '<Alt-\ >: delete surrounding spaces', 
    '<Alt-s> >: center line in current fill column', 
    '<Control-Alt-w>: next kill is appended to kill buffer\n'
    
    '----------------------------------------\n', 
    '<Alt c>: Capitalize the word the cursor is under.', 
    '<Alt u>: Uppercase the characters in the word.', 
    '<Alt l>: Lowercase the characters in the word.', 
    '----------------------------------------\n', 
    '<Alt t>: Mark word for word swapping.  Marking a second\n word will swap this word with the first', 
    '<Control-t>: Swap characters', 
    '<Ctrl-@>: Begin marking region.', 
    '<Ctrl-W>: Kill marked region', 
    '<Alt-W>: Copy marked region', 
    '<Ctrl-x Ctrl-u>: uppercase a marked region', 
    '<Ctrl-x Ctrl-l>: lowercase a marked region', 
    '<Ctrl-x h>: mark entire buffer', 
    '<Alt-Ctrl-backslash>: indent region to indentation of line 1 of the region.', 
    '<Ctrl-x tab> : indent region by 1 tab', 
    '<Control-x Control-x> : swap point and mark', 
    '<Control-x semicolon>: set comment column', 
    '<Alt-semicolon>: indent to comment column', 
    '----------------------------------------\n', 
    'M-! cmd -- Run the shell command line cmd and display the output', 
    'M-| cmd -- Run the shell command line cmd with region contents as input', 
    '----------------------------------------\n', 
    '<Control-x a e>: Expand the abbrev before point (expand-abbrev), even when Abbrev mode is not enabled', 
    '<Control-x a g>: Define an abbreviation for previous word', 
    '<Control-x a i g>: Define a word as abbreviation for word before point, or in point', 
    '----------------------------------------\n', 
    '<Control s>: forward search, using pattern in Mini buffer.\n', 
    '<Control r>: backward search, using pattern in Mini buffer.\n', 
    '<Control s Enter>: search forward for a word, nonincremental\n', 
    '<Control r Enter>: search backward for a word, nonincremental\n', 
    '<Control s Enter Control w>: Search for words, ignoring details of punctuation', 
    '<Control r Enter Control w>: Search backward for words, ignoring details of punctuation', 
    '<Control-Alt s>: forward regular expression search, using pattern in Mini buffer\n', 
    '<Control-Alt r>: backward regular expression search, using pattern in Mini buffer\n', 
    '''<Alt-%>: begin query search/replace. n skips to next match. y changes current match.  
    q or Return exits. ! to replace all remaining matches with no more questions''', 
    '''<Control Alt %> begin regex search replace, like Alt-%''', 
    '<Alt-=>: count lines and characters in regions', 
    '<Alt-( >: insert parentheses()', 
    '<Alt-) >:  move past close', 
    '<Control-x Control-t>: transpose lines.', 
    '<Control-x Control-o>: delete blank lines', 
    '<Control-x r s>: save region to register', 
    '<Control-x r i>: insert to buffer from register', 
    '<Control-x r +>: increment register', 
    '<Control-x r n>: insert number 0 to register', 
    '<Control-x r space > : point insert point to register', 
    '<Control-x r j > : jump to register', 
    '<Control-x x>: save region to register', 
    '<Control-x r r> : save rectangle to register', 
    '<Control-x r o>: open up rectangle', 
    '<Control-x r c> : clear rectangle', 
    '<Control-x r d> : delete rectangle', 
    '<Control-x r t> : replace rectangle with string', 
    '<Control-x r k> : kill rectangle', 
    '<Control-x r y> : yank rectangle', 
    '<Control-g> : keyboard quit\n', 
    '<Control-x = > : position of cursor', 
    '<Control-x . > : set fill prefix', 
    '<Control-x f > : set the fill column', 
    '<Control-x Control-b > : display the buffer list', 
    '<Control-x b > : switch to buffer', 
    '<Control-x k > : kill the specified buffer', 
    '----------------------------------------\n', 
    '<Alt - - Alt-l >: lowercase previous word', 
    '<Alt - - Alt-u>: uppercase previous word', 
    '<Alt - - Alt-c>: capitalise previous word', 
    '----------------------------------------\n', 
    '<Alt-/ >: dynamic expansion', 
    '<Control-Alt-/>: dynamic expansion.  Expands to common prefix in buffer\n'
    '----------------------------------------\n', 
    'Alt-x commands:\n', 
    '(Pressing Tab will result in auto completion of the options if an appropriate match is found', 
    'replace-string  -  replace string with string', 
    'replace-regex - replace python regular expression with string', 
    'append-to-register  - append region to register', 
    'prepend-to-register - prepend region to register\n'
    'sort-lines - sort selected lines', 
    'sort-columns - sort by selected columns', 
    'reverse-region - reverse selected lines', 
    'sort-fields  - sort by fields', 
    'abbrev-mode - toggle abbrev mode on/off', 
    'kill-all-abbrevs - kill current abbreviations', 
    'expand-region-abbrevs - expand all abrevs in region', 
    'read-abbrev-file - read abbreviations from file', 
    'write-abbrev-file - write abbreviations to file', 
    'list-abbrevs   - list abbrevs in minibuffer', 
    'fill-region-as-paragraph - treat region as one paragraph and add fill prefix', 
    'fill-region - fill paragraphs in region with fill prefix', 
    'close-rectangle  - close whitespace rectangle', 
    'how-many - counts occurances of python regular expression', 
    'kill-paragraph - delete from cursor to end of paragraph', 
    'backward-kill-paragraph - delete from cursor to start of paragraph', 
    'backward-kill-sentence - delete from the cursor to the start of the sentence', 
    'name-last-kbd-macro - give the last kbd-macro a name', 
    'insert-keyboard-macro - save macros to file', 
    'load-file - load a macro file', 
    'kill-word - delete the word the cursor is on', 
    'kill-line - delete form the cursor to end of the line', 
    'kill-sentence - delete the sentence the cursor is on', 
    'kill-region - delete a marked region', 
    'yank - restore what you have deleted', 
    'backward-kill-word - delete previous word', 
    'backward-delete-char - delete previous character', 
    'delete-char - delete character under cursor', 
    'isearch-forward - start forward incremental search', 
    'isearch-backward - start backward incremental search', 
    'isearch-forward-regexp - start forward regular expression incremental search', 
    'isearch-backward-regexp - start backward return expression incremental search', 
    'capitalize-word - capitalize the current word', 
    'upcase-word - switch word to upper case', 
    'downcase-word - switch word to lower case', 
    'indent-region - indent region to first line in region', 
    'indent-rigidly - indent region by a tab', 
    'indent-relative - Indent from point to under an indentation point in the previous line', 
    'set-mark-command - mark the beginning or end of a region', 
     'kill-rectangle - kill the rectangle', 
    'delete-rectangle - delete the rectangle', 
    'yank-rectangle - yank the rectangle', 
    'open-rectangle - open the rectangle', 
    'clear-rectangle - clear the rectangle', 
    'copy-to-register - copy selection to register', 
    'insert-register - insert register into buffer', 
    'copy-rectangle-to-register - copy buffer rectangle to register', 
    'jump-to-register - jump to position in register', 
    'point-to-register - insert point into register', 
    'number-to-register - insert number into register', 
    'increment-register - increment number in register', 
    'view-register - view what register contains', 
    'beginning-of-line - move to the beginning of the line', 
    'end-of-line - move to the end of the line', 
    'beginning-of-buffer - move to the beginning of the buffer', 
    'end-of-buffer - move to the end of the buffer', 
    'newline-and-indent - insert a newline and tab', 
    'keyboard-quit - abort current command', 
    'iconify-or-deiconify-frame - iconfiy current frame', 
    'advertised-undo - undo the last operation', 
    'back-to-indentation - move to first non-blank character of line', 
    'delete-indentation - join this line to the previous one', 
    'view-lossage - see the last 100 characters typed', 
    'transpose-chars - transpose two letters', 
    'transpose-words - transpose two words', 
    'transpose-line - transpose two lines', 
    'flush-lines - delete lines that match regex', 
    'keep-lines - keep lines that only match regex', 
    'insert-file - insert file at current position', 
    'save-buffer - save file', 
    'split-line - split line at cursor. indent to column of cursor', 
    'upcase-region - Upper case region', 
    'downcase-region - lower case region', 
    'goto-line - goto a line in the buffer', 
    'what-line - display what line the cursor is on', 
    'goto-char - goto a char in the buffer', 
    'set-fill-column - sets the fill column', 
    'center-line - centers the current line within the fill column', 
    'center-region - centers the current region within the fill column', 
    'forward-char - move the cursor forward one char', 
    'backward-char - move the cursor backward one char', 
    'previous-line - move the cursor up one line', 
    'next-line - move the cursor down one line', 
    'universal-argument - Repeat the next command "n" times', 
    'digit-argument - Repeat the next command "n" times', 
    'set-fill-prefix - Sets the prefix from the insert point to the start of the line', 
    'scroll-up - scrolls up one screen', 
    'scroll-down - scrolls down one screen', 
    'append-to-buffer - Append region to a specified buffer', 
    'prepend-to-buffer - Prepend region to a specified buffer', 
    'copy-to-buffer - Copy region to a specified buffer, deleting the previous contents', 
    'insert-buffer - Insert the contents of a specified buffer into current buffer at point', 
    'list-buffers - Display the buffer list', 
    'switch-to-buffer - switch to a different buffer, if it does not exits, it is created.', 
    'kill-buffer - kill the specified buffer', 
    'rename-buffer - rename the buffer', 
    'query-replace - query buffer for pattern and replace it.  The user will be asked for a pattern, and for text to replace the pattern with.', 
    'query-replace-regex - query buffer with regex and replace it.  The user will be asked for a pattern, and for text to replace the regex matches with.', 
    'inverse-add-global-abbrev - add global abbreviation from previous word.  Will ask user for word to expand to', 
    'expand-abbrev - Expand the abbrev before point. This is effective even when Abbrev mode is not enabled', 
    're-search-forward - do a python regular expression search forward', 
    're-search-backward - do a python regular expression search backward', 
    'diff - compares two files, displaying the differences in an Emacs buffer named *diff*', 
    'make-directory - create a new directory', 
    'remove-directory - remove an existing directory if its empty', 
    'delete-file - remove an existing file', 
    'search-forward - search forward for a word', 
    'search-backward - search backward for a word', 
    'word-search-forward - Search for words, ignoring details of punctuation.', 
    'word-search-backward - Search backward for words, ignoring details of punctuation', 
    'repeat-complex-command - repeat the last Alt-x command', 
    'eval-expression - evaluate a Python expression and put the value in the current buffer', 
    'tabify - turn the selected text\'s spaces into tabs', 
    'untabify - turn the selected text\'s tabs into spaces', 
    'shell-command -Run the shell command line cmd and display the output', 
    'shell-command-on-region -Run the shell command line cmd with region contents as input', 
    ]
    
    return '\n'.join(help_t)

getHelpText = staticmethod(getHelpText)
#@nonl
#@-node:ekr.20050724075352.42:getHelpText TO BE REMOVED
#@-node:ekr.20050724074642.17:usetemacs Hooks
#@+node:ekr.20050724074642.23:Overridden methods
#@+node:ekr.20050724074642.24:modifyOnBodyKey
def modifyOnBodyKey (self,event):
    
    '''stops Return and Tab from being processed if the Emacs instance has state.'''
    
    # Self is an instance of leoTkinterBody, so self.c is defined.
    c = self.c

    if event.char.isspace(): 
        if c.emacs.stateManager.hasState():
           return None
    else:
        return orig_OnBodyKey(self,event)
#@nonl
#@-node:ekr.20050724074642.24:modifyOnBodyKey
#@+node:ekr.20050724074642.25:createBindings & helpers  (Creates Emacs instance)
def createBindings (self,frame):

    c = frame.c

    #@    << create a label for frame >>
    #@+node:ekr.20050724074642.26:<< create a label for frame >>
    group = Tk.Frame(frame.split2Pane2,relief='ridge',borderwidth=3)
    
    f2 = Tk.Frame(group)
    f2.pack(side='top',fill='x')
    
    gtitle = Tk.Label(f2,
        text='mini-buffer',justify='left',anchor='nw',
        foreground='blue',background='white')
    
    group.pack(side='bottom',fill='x',expand=1)
    
    for z in frame.split2Pane2.children.values():
        group.pack_configure(before=z)
    
    label = Tk.Label(group,relief='groove',justify='left',anchor='w')
    label.pack(side='bottom',fill='both',expand=1,padx=2,pady=2)
    
    gtitle.pack(side='left')
    #@nonl
    #@-node:ekr.20050724074642.26:<< create a label for frame >>
    #@nl
    orig_Bindings(self,frame)

    # EKR: set emacs ivar in the commander.
    c.emacs = emacs = Emacs(frame.c,frame.bodyCtrl,label,useGlobalKillbuffer=True,useGlobalRegisters=True)
    emacs.label = label
    emacs.setUndoer(frame.bodyCtrl,self.c.undoer.undo)
    #@    << define utTailEnd >>
    #@+node:ekr.20050724074642.27:<< define utTailEnd >>
    def utTailEnd (buffer,frame=frame):
    
        '''A method that Emacs will call with its _tailEnd method'''
    
        buffer.event_generate('<Key>')
        buffer.update_idletasks()
    
        return 'break'
    #@nonl
    #@-node:ekr.20050724074642.27:<< define utTailEnd >>
    #@nl
    emacs.miniBuffer.setTailEnd(frame.bodyCtrl,utTailEnd)
    emacs.emacsControlCommands.setShutdownHook(self.c.close)
    addTemacsExtensions(emacs)
    addTemacsAbbreviations(emacs)
    changeKeyStrokes(emacs,frame.bodyCtrl)
    ### setBufferInteractionMethods( self.c, emacs, frame.bodyCtrl )
    orig_del = frame.bodyCtrl.delete
    #@    << define watchDelete >>
    #@+node:ekr.20050724074642.28:<< define watchDelete >>
    def watchDelete (i,j=None,emacs=emacs):
    
        '''Watches for complete text deletion.  If it occurs, turns off all state in the Emacs instance.'''
    
        if i == '1.0' and j == 'end':
            # g.trace()
            event = Tk.Event()
            event.widget = frame.bodyCtrl
            emacs.keyboardQuit(event)
    
        return orig_del(i,j)
    #@nonl
    #@-node:ekr.20050724074642.28:<< define watchDelete >>
    #@nl
    frame.bodyCtrl.delete = watchDelete
#@nonl
#@+node:ekr.20050724074642.29:addTemacsAbbreviations:  To do:  get stuff from confic
def addTemacsAbbreviations (Emacs):

    '''Adds abbreviatios and kbd macros to an Emacs instance'''

    pth = os.path.split(g.app.loadDir)
    aini = pth [0] +os.sep+'plugins'+os.sep

    if os.path.exists(aini+r'usetemacs.kbd'):
        f = file(aini+r'usetemacs.kbd','r')
        Emacs._loadMacros(f)

    if os.path.exists(aini+r'usetemacs.abv'):
        f = file(aini+r'usetemacs.abv','r')
        Emacs._readAbbrevs(f)
#@nonl
#@-node:ekr.20050724074642.29:addTemacsAbbreviations:  To do:  get stuff from confic
#@+node:ekr.20050724074642.30:addTemacsExtensions
def addTemacsExtensions (Emacs):

    '''Adds extensions to Emacs parameter.'''
    for z in extensions:
        try:
            if hasattr(z,'getExtensions'):
                ex_meths = z.getExtensions()
                for x in ex_meths.keys():
                    Emacs.extendAltX(x,ex_meths[x])
            else:
                g.es('Module %s does not have a getExtensions function' % z,color='red')

        except Exception, x:
            g.es('Could not add extension because of %s' % x,color='red')
#@nonl
#@-node:ekr.20050724074642.30:addTemacsExtensions
#@+node:ekr.20050724074642.31:changeKeyStrokes
def changeKeyStrokes (Emacs,tbuffer):

    for z in new_keystrokes.keys():

        Emacs.reconfigureKeyStroke(tbuffer,z,new_keystrokes[z])
#@nonl
#@-node:ekr.20050724074642.31:changeKeyStrokes
#@+node:ekr.20050724074642.32:setBufferInteractionMethods & helpers
def setBufferInteractionMethods (c,emacs,buffer):

    '''This function configures the Emacs instance so that
       it can see all the nodes as buffers for its buffer commands.'''

    #@    @+others
    #@+node:ekr.20050724074642.33:OLDbuildBufferList
    def OLDbuildBufferList (): #This builds a buffer list from what is in the outline.  Worked surprisingly fast on LeoPy.
        if not tnodes.has_key(c): #I was worried that speed factors would make it unusable.
            tnodes [c] = {}
        tdict = tnodes [c]
        pos = c.rootPosition()
        utni = pos.allNodes_iter()
        bufferdict = {}
        tdict.clear()
        positions.clear()
        for z in utni:
    
           t = z.v.t
           if positions.has_key(t.headString):
            positions [t.headString].append(z.copy())
           else:
            positions [t.headString] = [z.copy()] #not using a copy seems to have bad results.
           #positions[ t.headString ] = z
    
           bS = ''
           if t.bodyString: bS = t.bodyString
    
    
           bufferdict [t.headString] = bS
           tdict [t.headString] = t
    
        return bufferdict
    #@nonl
    #@-node:ekr.20050724074642.33:OLDbuildBufferList
    #@+node:ekr.20050725070621:buildBufferList  (MAY BE BUGGY)
    def buildBufferList (self):
    
        '''Build a buffer list from an outline.'''
    
        c = self.c ; global positions, tnodes
    
        d = {} ; positions.clear()
    
        for p in c.allNodes_iter():
            t = p.v.t ; h = t.headString()
            theList = positions.get(h,[])
            theList.append(p.copy())
            self.positions [h] = theList
            d [h] = t.bodyString()
    
        tnodes [c] = d
        return d
    #@nonl
    #@-node:ekr.20050725070621:buildBufferList  (MAY BE BUGGY)
    #@+node:ekr.20050724074642.34:setBufferData
    def setBufferData (name,data):
    
        data = unicode(data)
        tdict = tnodes [c]
        if tdict.has_key(name):
            tdict [name].bodyString = data
    #@nonl
    #@-node:ekr.20050724074642.34:setBufferData
    #@+node:ekr.20050724074642.35:gotoNode & gotoPosition
    def gotoNode (name):
    
        c.beginUpdate()
        if positions.has_key(name):
            posis = positions [name]
            if len(posis) > 1:
                tl = Tk.Toplevel()
                #tl.geometry( '%sx%s+0+0' % ( ( ms[ 0 ]/3 ) *2 , ms[ 1 ]/2 ))
                tl.title("Select node by numeric position")
                fr = Tk.Frame(tl)
                fr.pack()
                header = Tk.Label(fr,text='select position')
                header.pack()
                lbox = Tk.Listbox(fr,background='white',foreground='blue')
                lbox.pack()
                for z in xrange(len(posis)):
                    lbox.insert(z,z+1)
                lbox.selection_set(0)
                def setPos (event):
                    cpos = int(lbox.nearest(event.y))
                    tl.withdraw()
                    tl.destroy()
                    if cpos != None:
                        gotoPosition(c,posis[cpos])
                lbox.bind('<Button-1>',setPos)
                geometry = tl.geometry()
                geometry = geometry.split('+')
                geometry = geometry [0]
                width = tl.winfo_screenwidth() / 3
                height = tl.winfo_screenheight() / 3
                geometry = '+%s+%s' % (width,height)
                tl.geometry(geometry)
            else:
                pos = posis [0]
                gotoPosition(c,pos)
        else:
            pos2 = c.currentPosition()
            tnd = leoNodes.tnode('',name)
            pos = pos2.insertAfter(tnd)
            gotoPosition(c,pos)
        #c.frame.tree.expandAllAncestors( pos )
        #c.selectPosition( pos )
        #c.endUpdate()
    #@nonl
    #@+node:ekr.20050724074642.36:gotoPosition
    def gotoPosition (c,pos):
    
        c.frame.tree.expandAllAncestors(pos)
        c.selectPosition(pos)
        c.endUpdate()
    #@nonl
    #@-node:ekr.20050724074642.36:gotoPosition
    #@-node:ekr.20050724074642.35:gotoNode & gotoPosition
    #@+node:ekr.20050724074642.37:deleteNode
    def deleteNode (name):
    
        c.beginUpdate()
        if positions.has_key(name):
            pos = positions [name]
            cpos = c.currentPosition()
            pos.doDelete(cpos)
        c.endUpdate()
    #@nonl
    #@-node:ekr.20050724074642.37:deleteNode
    #@+node:ekr.20050724074642.38:renameNode
    def renameNode (name):
    
        c.beginUpdate()
        pos = c.currentPosition()
        pos.setHeadString(name)
        c.endUpdate()
    #@nonl
    #@-node:ekr.20050724074642.38:renameNode
    #@-others

    # These add Leo-reated capabilities to the emacs instance.
    emacs.bufferCommmands.setBufferListGetter(buffer,buildBufferList)
    emacs.bufferCommmands.setBufferSetter(buffer,setBufferData)
    emacs.bufferCommmands.setBufferGoto(buffer,gotoNode)
    emacs.bufferCommmands.setBufferDelete(buffer,deleteNode)
    emacs.bufferCommmands.setBufferRename(buffer,renameNode)
#@nonl
#@-node:ekr.20050724074642.32:setBufferInteractionMethods & helpers
#@-node:ekr.20050724074642.25:createBindings & helpers  (Creates Emacs instance)
#@-node:ekr.20050724074642.23:Overridden methods
#@-node:ekr.20050724074619.1:Birth (From usetemacs)
#@+node:ekr.20050724075352.40:class Emacs
class Emacs:
    
    '''A class to support emacs commands.  Creates a Tk Text widget for the minibufer.'''

    # Define class vars...
    global_killbuffer = []
        # Used only if useGlobalKillbuffer arg to Emacs ctor is True.
        # Otherwise, each Emacs instance has its own local kill buffer.

    global_registers = {}
        # Used only if useGlobalRegisters arg to Emacs ctor is True.
        # Otherwise each Emacs instance has its own set of registers.

    lossage = []
        # A case could be made for per-instance lossage, but this is not supported.

    #@    @+others
    #@+node:ekr.20050728093027:Birth
    #@+node:ekr.20050724075352.41:Emacs.__init__
    def __init__ (self,c,tbuffer=None,miniBufferWidget=None,useGlobalKillbuffer=False,useGlobalRegisters=False):
        '''Sets up Emacs instance.
        
        Use tbuffer (a Tk Text widget) and miniBufferWidget (a Tk Label) if provided.
        Otherwise, the caller must call setBufferStrokes.
        
        useGlobalRegisters and useGlobalKillbuffer indicate whether to use
        global (class vars) or per-instance (ivars) for kill buffers and registers.'''
        
        self.c = c
        self.useGlobalKillbuffer = useGlobalKillbuffer
        self.useGlobalRegisters = useGlobalRegisters
        
        self.undoers = {} # Emacs instance tracks undoers given to it.
    
        # For communication between keystroke handlers and other classes.
        self.regXRpl = None # EKR: a generator: calling self.regXRpl.next() get the next value.
        self.regXKey = None
       
        # Create helper classes.  Order is important here...
        self.miniBuffer   = self.miniBufferClass(self,miniBufferWidget)
        altX_commandsDict = self.createCommandsClasses()
    
        # define delegators.
        self.stateManager = self.miniBuffer.stateManager
        self.kstrokeManager = self.miniBuffer.kstrokeManager
        self.keyboardQuit   = self.miniBuffer.keyboardQuit
        self.setEvent       = self.miniBuffer.setEvent
    
        # Last.
        self.miniBuffer.finishCreate(altX_commandsDict)
        
        # This section sets up the buffer data structures
        self.bufferListGetters ={}
        self.bufferSetters ={}
        self.bufferGotos ={}
        self.bufferDeletes ={}
        self.renameBuffers ={}
        self.bufferDict = None 
        self.bufferTracker = self.Tracker()
        
        self.last_clipboard = None #For interacting with system clipboard.
      
        if tbuffer and miniBufferWidget:
            self.miniBuffer.setBufferStrokes(tbuffer)
    #@nonl
    #@-node:ekr.20050724075352.41:Emacs.__init__
    #@+node:ekr.20050725094519:createCommandsClasses
    def createCommandsClasses (self):
        
        self.commandClasses = [
            ('abbrevCommands',      self.abbrevCommandsClass),
            ('bufferCommands',      self.bufferCommandsClass),
            ('editCommands',        self.editCommandsClass),
            ('emacsControlCommands',self.emacsControlCommandsClass),
            ('fileCommands',        self.fileCommandsClass),
            ('keyHandlerCommands',  self.keyHandlerCommandsClass),
            ('killBufferCommands',  self.killBufferCommandsClass),
            ('leoCommands',         self.leoCommandsClass),
            ('macroCommands',       self.macroCommandsClass),
            ('queryReplaceCommands',self.queryReplaceCommandsClass),
            ('rectangleCommands',   self.rectangleCommandsClass),
            ('registerCommands',    self.registerCommandsClass),
            ('searchCommands',      self.searchCommandsClass),
        ]
        
        altX_commandsDict = {}
    
        for name, theClass in self.commandClasses:
            theInstance = theClass(self)# Create the class.
            setattr(self,name,theInstance)
            # g.trace(getattr(self,name))
            d = theInstance.getPublicCommands()
            if d:
                altX_commandsDict.update(d)
                if 0:
                    keys = d.keys()
                    keys.sort()
                    print '----- %s' % name
                    for key in keys: print key
                    
        return altX_commandsDict
    #@nonl
    #@-node:ekr.20050725094519:createCommandsClasses
    #@+node:ekr.20050724075352.116:reconfigureKeyStroke  WILL PROBABLY GO AWAY
    def reconfigureKeyStroke (self,tbuffer,keystroke,set_to):
    
        '''This method allows the user to reconfigure what a keystroke does.
           This feature is alpha at best, and untested.'''
    
        if self.cbDict.has_key(set_to):
            command = self.cbDict [set_to]
            self.cbDict [keystroke] = command
            evstring = '<%s>' % keystroke
            tbuffer.bind(evstring,lambda event,meth=command: self.miniBuffer.masterCommand(event,meth,evstring))
    #@nonl
    #@-node:ekr.20050724075352.116:reconfigureKeyStroke  WILL PROBABLY GO AWAY
    #@+node:ekr.20050724075352.109:undoer methods
    #@+at
    # Emacs requires an undo mechanism be added from the environment.
    # If there is no undo mechanism added, there will be no undo functionality 
    # in the instance.
    #@-at
    #@@c
    
    #@+others
    #@+node:ekr.20050724075352.110:setUndoer
    def setUndoer (self,tbuffer,undoer):
        '''This method sets the undoer method for the Emacs instance.'''
        self.undoers [tbuffer] = undoer
    #@nonl
    #@-node:ekr.20050724075352.110:setUndoer
    #@+node:ekr.20050724075352.111:doUndo
    def doUndo (self,event,amount=1):
        tbuffer = event.widget
        if self.undoers.has_key(tbuffer):
            for z in xrange(amount):
                self.undoers [tbuffer] ()
        return 'break'
    #@nonl
    #@-node:ekr.20050724075352.111:doUndo
    #@-others
    #@nonl
    #@-node:ekr.20050724075352.109:undoer methods
    #@-node:ekr.20050728093027:Birth
    #@+node:ekr.20050725091822:Commands classes...
    #@<< define class baseCommandsClass >>
    #@+node:ekr.20050725091822.1:<< define class baseCommandsClass >>
    class baseCommandsClass:
    
        '''The base class for all emacs command classes'''
    
        #@    @+others
        #@+node:ekr.20050726044533: ctor
        def __init__ (self,emacs):
        
            self.c = emacs.c
            
        
            # Class delegators.
            self.emacs = emacs
            self.miniBuffer = emacs.miniBuffer
        #@nonl
        #@-node:ekr.20050726044533: ctor
        #@+node:ekr.20050729095537:__call__
        if 0:
            def __call__ (self,*args,**keys):
        
                g.trace(*args,**keys)
        
                return 'break'
        #@nonl
        #@-node:ekr.20050729095537:__call__
        #@+node:ekr.20050724075352.87:findPre
        def findPre (self,a,b):
            st = ''
            for z in a:
                st1 = st + z
                if b.startswith(st1):
                    st = st1
                else:
                    return st
            return st
        #@nonl
        #@-node:ekr.20050724075352.87:findPre
        #@+node:ekr.20050726044533.2:getPublicCommands
        def getPublicCommands (self):
            '''Return a dict describing public commands implemented in the subclass.
            Keys are untranslated command names.  Values are methods of the subclass.'''
        
            self.oops()
            return {}
        #@nonl
        #@-node:ekr.20050726044533.2:getPublicCommands
        #@+node:ekr.20050724075352.86:getWSString
        def getWSString (self,txt):
        
            if 1:
                ntxt = [g.choose(ch=='\t',ch,' ') for ch in txt]
            else:
                ntxt = []
                for z in txt:
                    if z == '\t':
                        ntxt.append(z)
                    else:
                        ntxt.append(' ')
        
            return ''.join(ntxt)
        #@nonl
        #@-node:ekr.20050724075352.86:getWSString
        #@+node:ekr.20050726044533.1:oops
        def oops (self):
            print("emacs baseCommandsClass oops:",
                g.callerName(2),
                "must be overridden in subclass")
        #@nonl
        #@-node:ekr.20050726044533.1:oops
        #@+node:ekr.20050724075352.246:range utilities
        #@+node:ekr.20050724075352.247:inRange
        def inRange (self,widget,range,l='',r=''):
        
            ranges = widget.tag_ranges(range)
            for z in xrange(0,len(ranges),2):
                z1 = z + 1
                l1 = 'insert%s' % l
                r1 = 'insert%s' % r
                if widget.compare(l1,'>=',ranges[z]) and widget.compare(r1,'<=',ranges[z1]):
                    return True
            return False
        #@nonl
        #@-node:ekr.20050724075352.247:inRange
        #@+node:ekr.20050724075352.248:contRanges
        def contRanges (self,widget,range):
        
            ranges = widget.tag_ranges(range)
            t1 = widget.get(ranges[0],ranges[-1])
            t2 = []
            for z in xrange(0,len(ranges),2):
                z1 = z + 1
                t2.append(widget.get(ranges[z],ranges[z1]))
            t2 = '\n'.join(t2)
            return t1 == t2
        #@-node:ekr.20050724075352.248:contRanges
        #@+node:ekr.20050724075352.249:testinrange
        def testinrange (self,widget):
        
            if not self.inRange(widget,'sel') or not self.contRanges(widget,'sel'):
                self.removeRKeys(widget)
                return False
            else:
                return True
        #@nonl
        #@-node:ekr.20050724075352.249:testinrange
        #@-node:ekr.20050724075352.246:range utilities
        #@+node:ekr.20050724075352.91:removeRKeys
        def removeRKeys (self,widget):
        
            mrk = 'sel'
            widget.tag_delete(mrk)
            widget.unbind('<Left>')
            widget.unbind('<Right>')
            widget.unbind('<Up>')
            widget.unbind('<Down>')
        #@nonl
        #@-node:ekr.20050724075352.91:removeRKeys
        #@-others
    #@nonl
    #@-node:ekr.20050725091822.1:<< define class baseCommandsClass >>
    #@nl
    
    #@+others
    #@+node:ekr.20050724075352.188:class abbrevCommandsClass
    #@+at
    # 
    # type some text, set its abbreviation with Control-x a i g, type the text 
    # for abbreviation expansion
    # type Control-x a e ( or Alt-x expand-abbrev ) to expand abbreviation
    # type Alt-x abbrev-on to turn on automatic abbreviation expansion
    # Alt-x abbrev-on to turn it off
    # 
    # an example:
    # type:
    # frogs
    # after typing 's' type Control-x a i g.  This will turn the miniBuffer 
    # blue, type in your definition. For example: turtles.
    # 
    # Now in the buffer type:
    # frogs
    # after typing 's' type Control-x a e.  This will turn the 'frogs' into:
    # turtles
    #@-at
    #@@c
    
    class abbrevCommandsClass (baseCommandsClass):
    
        #@    @+others
        #@+node:ekr.20050725125153: ctor
        def __init__ (self,emacs):
            
            Emacs.baseCommandsClass.__init__(self,emacs) # init the base class.
        
            # Set ivars in emacs.
            self.emacs.abbrevMode = False 
            self.emacs.abbrevOn = False # determines if abbreviations are on for masterCommand and toggle abbreviations.
        
            # Set local ivars.
            self.abbrevs ={}
        #@nonl
        #@-node:ekr.20050725125153: ctor
        #@+node:ekr.20050725130925.1: getPublicCommands
        def getPublicCommands (self):
            
            return {
                'abbrev-mode':              self.toggleAbbrevMode,
                'expand-abbrev':            self.expandAbbrev,
                'expand-region-abbrevs':    self.regionalExpandAbbrev,
                'kill-all-abbrevs':         self.killAllAbbrevs,
                'list-abbrevs':             self.listAbbrevs,
                'read-abbrev-file':         self.readAbbreviations,
                'write-abbrev-file':        self.writeAbbreviations,
            }
        #@nonl
        #@-node:ekr.20050725130925.1: getPublicCommands
        #@+node:ekr.20050725130925: Entry points
        #@+node:ekr.20050725135621:expandAbbrev
        def expandAbbrev (self,event):
            
            b = self.miniBuffer
        
            return b.keyboardQuit(event) and self._expandAbbrev(event)
        
        #@-node:ekr.20050725135621:expandAbbrev
        #@+node:ekr.20050724075352.195:killAllAbbrevs
        def killAllAbbrevs (self,event):
        
            b = self.miniBuffer
            self.abbrevs = {}
            return b.keyboardQuit(event)
        #@nonl
        #@-node:ekr.20050724075352.195:killAllAbbrevs
        #@+node:ekr.20050724075352.197:listAbbrevs
        def listAbbrevs (self,event):
        
            b = self.miniBuffer
            txt = ''
            for z in self.abbrevs:
                txt = '%s%s=%s\n' % (txt,z,self.abbrevs[z])
            b.set(txt)
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.197:listAbbrevs
        #@+node:ekr.20050724075352.198:readAbbreviations
        def readAbbreviations (self,event):
        
            f = tkFileDialog.askopenfile()
            if f == None:
                return 'break'
            else:
                return self._readAbbrevs(f)
        #@nonl
        #@-node:ekr.20050724075352.198:readAbbreviations
        #@+node:ekr.20050724075352.192:regionalExpandAbbrev
        def regionalExpandAbbrev( self, event ):
            
            if not self._chckSel( event ):
                return
            
            tbuffer = event.widget
            i1 = tbuffer.index( 'sel.first' )
            i2 = tbuffer.index( 'sel.last' ) 
            ins = tbuffer.index( 'insert' )
            #@    << define a new generator searchXR >>
            #@+node:ekr.20050724075352.193:<< define a new generator searchXR >>
            # EKR: This is a generator (it contains a yield).
            # EKR: To make this work we must define a new generator for each call to regionalExpandAbbrev.
            def searchXR( i1 , i2, ins, event ):
            
                b = self.miniBuffer ; tbuffer = event.widget
                tbuffer.tag_add( 'sXR', i1, i2 )
                while i1:
                    tr = tbuffer.tag_ranges( 'sXR' )
                    if not tr: break
                    i1 = tbuffer.search( r'\w', i1, stopindex = tr[ 1 ] , regexp = True )
                    if i1:
                        word = tbuffer.get( '%s wordstart' % i1, '%s wordend' % i1 )
                        tbuffer.tag_delete( 'found' )
                        tbuffer.tag_add( 'found',  '%s wordstart' % i1, '%s wordend' % i1 )
                        tbuffer.tag_config( 'found', background = 'yellow' )
                        if self.abbrevs.has_key( word ):
                            b.set( 'Replace %s with %s? y/n' % ( word, self.abbrevs[ word ] ) )
                            yield None
                            if self.regXKey == 'y':
                                ind = tbuffer.index( '%s wordstart' % i1 )
                                tbuffer.delete( '%s wordstart' % i1, '%s wordend' % i1 )
                                tbuffer.insert( ind, self.abbrevs[ word ] )
                        i1 = '%s wordend' % i1
                tbuffer.mark_set( 'insert', ins )
                tbuffer.selection_clear()
                tbuffer.tag_delete( 'sXR' )
                tbuffer.tag_delete( 'found' )
                b.set( '' )
                b.setLabelGrey()
                self._setRAvars()
            #@nonl
            #@-node:ekr.20050724075352.193:<< define a new generator searchXR >>
            #@nl
            # EKR: the 'result' of calling searchXR is a generator object.
            self.emacs.regXRpl = searchXR( i1, i2, ins, event)
            self.emacs.regXRpl.next() # Call it the first time.
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.192:regionalExpandAbbrev
        #@+node:ekr.20050724075352.196:toggleAbbrevMode
        def toggleAbbrevMode (self,event):
         
            b = self.miniBuffer
            self.emacs.abbrevOn = not self.emacs.abbrevOn 
            b.keyboardQuit(event)
            b.set('Abbreviations are ' + g.choose(self.emacs.abbrevOn,'On','Off'))
        #@nonl
        #@-node:ekr.20050724075352.196:toggleAbbrevMode
        #@+node:ekr.20050724075352.200:writeAbbreviations
        def writeAbbreviations (self,event):
        
            f = tkFileDialog.asksaveasfile()
            if f == None:
                return 'break'
            else:
                return self._writeAbbrevs(f)
        #@nonl
        #@-node:ekr.20050724075352.200:writeAbbreviations
        #@-node:ekr.20050725130925: Entry points
        #@+node:ekr.20050724075352.189:abbreviationDispatch
        def abbreviationDispatch (self,event,which):
            
            b = self.miniBuffer
        
            state = b.getState('abbrevMode')
        
            if state == 0:
                b.setState('abbrevMode',which)
                b.set('')
                b.setLabelBlue()
            else:
                self.abbrevCommand1(event)
                
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.189:abbreviationDispatch
        #@+node:ekr.20050724075352.190:abbrevCommand1
        def abbrevCommand1 (self,event):
        
            b = self.miniBuffer ; tbuffer = event.widget
        
            if event.keysym == 'Return':
                word = tbuffer.get('insert -1c wordstart','insert -1c wordend')
                if word == ' ': return
                state = b.getState('abbrevMode')
                if state == 1:
                    self.abbrevs [b.get()] = word
                elif state == 2:
                    self.abbrevs [word] = b.get()
                b.keyboardQuit(event)
                b.reset()
            else:
                b.update(event)
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.190:abbrevCommand1
        #@+node:ekr.20050724075352.191:_expandAbbrev
        def _expandAbbrev (self,event):
        
            b = self.miniBuffer ; tbuffer = event.widget 
            word = tbuffer.get('insert -1c wordstart','insert -1c wordend')
            ch = event.char.strip()
        
            if ch: # We must do this: expandAbbrev is called from Alt-x and Control-x, we get two differnt types of data and tbuffer states.
                word = '%s%s'% (word,event.char)
                
            if self.abbrevs.has_key(word):
                tbuffer.delete('insert -1c wordstart','insert -1c wordend')
                tbuffer.insert('insert',self.abbrevs[word])
                return b._tailEnd(tbuffer)
            else:
                return False 
        #@-node:ekr.20050724075352.191:_expandAbbrev
        #@+node:ekr.20050724075352.194:_setRAvars
        def _setRAvars( self ):
        
            self.emacs.regXRpl = self.emacs.regXKey = None
        #@nonl
        #@-node:ekr.20050724075352.194:_setRAvars
        #@+node:ekr.20050724075352.199:_readAbbrevs
        def _readAbbrevs (self,f):
        
            for x in f:
                a, b = x.split('=')
                b = b[:-1]
                self.abbrevs[a] = b 
            f.close()
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.199:_readAbbrevs
        #@+node:ekr.20050724075352.201:_writeAbbrevs
        def _writeAbbrevs( self, f ):
        
            for x in self.abbrevs:
                f.write( '%s=%s\n' %( x, self.abbrevs[ x ] ) )
            f.close()
         
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.201:_writeAbbrevs
        #@-others
    #@nonl
    #@-node:ekr.20050724075352.188:class abbrevCommandsClass
    #@+node:ekr.20050724075352.117:class bufferCommandsClass
    #@+at 
    #@nonl
    # An Emacs instance does not have knowledge of what is considered a buffer 
    # in the environment.
    # 
    # The call to setBufferInteractionMethods calls the buffer configuration 
    # methods.
    #@-at
    #@@c
    
    class bufferCommandsClass  (baseCommandsClass):
    
        #@    @+others
        #@+node:ekr.20050726044533.4: ctor
        def __init__ (self,emacs):
            
            Emacs.baseCommandsClass.__init__(self,emacs) # init the base class.
            
            self.bufferListGetters = {} # Set by buffer configuration methods.
            
            # Used by chooseBuffer.
            self.commandsDict = {
                'append-to-buffer': self._appendToBuffer,
                'copy-to-buffer':   self._copyToBuffer,
                'insert-buffer':    self._insertToBuffer,
                'kill-buffer':     self._killBuffer, 
                'prepend-to-buffer':self._prependToBuffer, 
                'switch-to-buffer': self._switchToBuffer, 
            }
        #@nonl
        #@-node:ekr.20050726044533.4: ctor
        #@+node:ekr.20050726045343: getPublicCommands
        def getPublicCommands (self):
        
            return {
                'append-to-buffer':     self.appendToBuffer,
                'copy-to-buffer':       self.copyToBuffer,
                'insert-buffer':        self.insertBuffer,
                'kill-buffer' :         self.killBuffer,
                'list-buffers' :        self.listBuffers,
                'prepend-to-buffer':    self.prependToBuffer,
                'rename-buffer':        self.renameBuffer,
                'switch-to-buffer':     self.switchToBuffer,
            }
        #@nonl
        #@-node:ekr.20050726045343: getPublicCommands
        #@+node:ekr.20050726045343.1:Entry points
        def appendToBuffer (self,event):
            return self.setInBufferMode(event,which='append-to-buffer')
        
        def copyToBuffer (self,event):
            return self.setInBufferMode(event,which='copy-to-buffer')
        
        def insertBuffer (self,event):
            return self.setInBufferMode(event,which= 'insert-buffer')
        
        def killBuffer (self,event):
            return self.setInBufferMode(event,which='kill-buffer')
        
        def prependToBuffer (self,event):
            return self.setInBufferMode(event,which='prepend-to-buffer')
        
        def switchToBuffer (self,event):
            return self.setInBufferMode(event,which='switch-to-buffer')
        #@nonl
        #@+node:ekr.20050724075352.127:_appendToBuffer
        def _appendToBuffer (self,event,name): # event IS used.
        
            b = self.miniBuffer ; tbuffer = event.widget
            
            try:
                txt = tbuffer.get('sel.first','sel.last')
                bdata = self.bufferDict[name]
                bdata = '%s%s'%(bdata,txt)
                self.setBufferData(event,name,bdata)
            except Exception:
                pass 
        
            return b.keyboardQuit(event)
        #@nonl
        #@-node:ekr.20050724075352.127:_appendToBuffer
        #@+node:ekr.20050724075352.131:_copyToBuffer
        def _copyToBuffer (self,event,name): # event IS used.
            
            b = self.miniBuffer ; tbuffer = event.widget 
            try:
                txt = tbuffer.get('sel.first','sel.last')
                self.setBufferData(event,name,txt)
            except Exception:
                pass 
            
            return b.keyboardQuit(event)
        #@nonl
        #@-node:ekr.20050724075352.131:_copyToBuffer
        #@+node:ekr.20050724075352.129:_insertToBuffer
        def _insertToBuffer (self,event,name):
        
            b = self.miniBuffer ; tbuffer = event.widget 
            bdata = self.bufferDict[name]
            tbuffer.insert('insert',bdata)
            b._tailEnd(tbuffer)
        
            return b.keyboardQuit(event)
        #@nonl
        #@-node:ekr.20050724075352.129:_insertToBuffer
        #@+node:ekr.20050724075352.133:_killBuffer
        def _killBuffer (self,event,name):
            
            b = self.miniBuffer
            method = self.bufferDeletes[event.widget]
            b.keyboardQuit(event)
            method(name)
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.133:_killBuffer
        #@+node:ekr.20050724075352.128:_prependToBuffer
        def _prependToBuffer (self,event,name):
            
            b = self.miniBuffer ; tbuffer = event.widget
        
            try:
                txt = tbuffer.get('sel.first','sel.last')
                bdata = self.bufferDict[name]
                bdata = '%s%s'%(txt,bdata)
                self.setBufferData(event,name,bdata)
            except Exception:
                pass 
        
            return b.keyboardQuit(event)
        #@nonl
        #@-node:ekr.20050724075352.128:_prependToBuffer
        #@+node:ekr.20050724075352.132:_switchToBuffer
        def _switchToBuffer (self,event,name):
            
            b = self.miniBuffer
            method = self.bufferGotos[event.widget]
            b.keyboardQuit(event)
            method(name)
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.132:_switchToBuffer
        #@+node:ekr.20050724075352.135:chooseBuffer
        def chooseBuffer (self,event):
            
            b = self.miniBuffer
            state = b.getState('chooseBuffer')
            if state.startswith('start'):
                state = state[5:]
                b.setState('chooseBuffer',state)
                b.set('')
            if event.keysym=='Tab':
                stext = b.get().strip()
                if self.bufferTracker.prefix and stext.startswith(self.bufferTracker.prefix):
                    b.set(self.bufferTracker.next())#get next in iteration
                else:
                    prefix = b.get()
                    pmatches =[]
                    for z in self.bufferDict.keys():
                        if z.startswith(prefix):
                            pmatches.append(z)
                    self.bufferTracker.setTabList(prefix,pmatches)
                    b.set(self.bufferTracker.next())#begin iteration on new lsit
                return 'break'
            elif event.keysym=='Return':
               bMode = b.getState('chooseBuffer')
               return self.commandsDict[bMode](event,b.get())
            else:
                self.update(event)
                return 'break'
        #@nonl
        #@-node:ekr.20050724075352.135:chooseBuffer
        #@+node:ekr.20050724075352.130:listBuffers
        def listBuffers (self,event):
            
            b = self.miniBuffer ; tbuffer = event.widget
        
            bdict = self.getBufferDict(event)
            list = bdict.keys()
            list.sort()
            data = '\n'.join(list)
            b.keyboardQuit(event)
            b.set(data)
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.130:listBuffers
        #@+node:ekr.20050724075352.134:renameBuffer
        def renameBuffer (self,event):
            
            b = self.miniBuffer ; tbuffer = event.widget
        
            if not b.getState('renameBuffer'):
                b.setState('renameBuffer',True)
                b.set('')
                b.setLabelBlue()
                return 'break'
            elif event.keysym=='Return':
               nname = b.get()
               b.keyboardQuit(event)
               self.renameBuffers[tbuffer](nname)
            else:
                b.update(event)
                return 'break'
        #@nonl
        #@-node:ekr.20050724075352.134:renameBuffer
        #@-node:ekr.20050726045343.1:Entry points
        #@+node:ekr.20050724075352.136:setInBufferMode
        def setInBufferMode (self,event,which):
            
            b = self.miniBuffer ; tbuffer = event.widget
            b.keyboardQuit(event)
            b.setState('chooseBuffer','start%s' % which)
            b.setLabelBlue()
            b.set('Choose Buffer Name:')
            self.bufferDict = self.getBufferDict(event)
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.136:setInBufferMode
        #@+node:ekr.20050724075352.118:Buffer configuration methods
        #@+node:ekr.20050724075352.119:setBufferListGetter
        def setBufferListGetter( self, buffer, method ):
            #Sets a method that returns a buffer name and its text, and its insert position.
            self.bufferListGetters[ buffer ] = method
        #@nonl
        #@-node:ekr.20050724075352.119:setBufferListGetter
        #@+node:ekr.20050724075352.120:setBufferSetter
        def setBufferSetter( self, buffer, method ):
            #Sets a method that takes a buffer name and the new contents.
            self.bufferSetters[ buffer ] = method
        #@nonl
        #@-node:ekr.20050724075352.120:setBufferSetter
        #@+node:ekr.20050724075352.121:getBufferDict
        def getBufferDict( self, event ):
            
            tbuffer = event.widget
            meth = self.bufferListGetters[ tbuffer ]
            return meth()
        #@nonl
        #@-node:ekr.20050724075352.121:getBufferDict
        #@+node:ekr.20050724075352.122:setBufferData
        def setBufferData( self, event, name, data ):
            
            tbuffer = event.widget
            meth = self.bufferSetters[ tbuffer ]
            meth( name, data )
        #@nonl
        #@-node:ekr.20050724075352.122:setBufferData
        #@+node:ekr.20050724075352.123:setBufferGoto
        def setBufferGoto( self, tbuffer, method ):
            self.bufferGotos[ tbuffer ] = method
        #@nonl
        #@-node:ekr.20050724075352.123:setBufferGoto
        #@+node:ekr.20050724075352.124:setBufferDelete
        def setBufferDelete( self, tbuffer, method ):
            
            self.bufferDeletes[ tbuffer ] = method
        #@nonl
        #@-node:ekr.20050724075352.124:setBufferDelete
        #@+node:ekr.20050724075352.125:setBufferRename
        def setBufferRename( self, buffer, method ):
            
            self.renameBuffers[ buffer ] = method
        #@nonl
        #@-node:ekr.20050724075352.125:setBufferRename
        #@-node:ekr.20050724075352.118:Buffer configuration methods
        #@-others
    #@nonl
    #@-node:ekr.20050724075352.117:class bufferCommandsClass
    #@+node:ekr.20050724075352.54:class editCommandsClass
    class editCommandsClass (baseCommandsClass):
        
        '''Contains editing commands with little or no state.'''
    
        #@    @+others
        #@+node:ekr.20050727092854: ctor
        def __init__ (self,emacs):
        
            Emacs.baseCommandsClass.__init__(self,emacs) # init the base class.
            
            self.ccolumn = '0'   # For comment column functions.
            self.dynaregex = re.compile(r'[%s%s\-_]+'%(string.ascii_letters,string.digits))
                # For dynamic abbreviations
            self.fillPrefix = '' # For fill prefix functions.
            self.fillColumn = 70 # For line centering.
            self.store ={'rlist':[], 'stext':''} # For dynamic expansion.
            self.swapSpots = []
            self._useRegex = False # For replace-string and replace-regex
        #@nonl
        #@-node:ekr.20050727092854: ctor
        #@+node:ekr.20050727093829: getPublicCommands
        def getPublicCommands (self):
        
            b = self.miniBuffer
        
            return {
                'back-to-indentation': lambda event: self.backToIndentation(event) and b.keyboardQuit(event),
                'backward-delete-char': lambda event, which = 'BackSpace': self.manufactureKeyPress(event,which) and b.keyboardQuit(event),
                'backward-char': lambda event, which = 'Left': b.keyboardQuit(event) and self.manufactureKeyPress(event,which),
                'backward-kill-paragraph': self.backwardKillParagraph,
                'beginning-of-buffer': lambda event, spot = '1.0': self.moveTo(event,spot) and b.keyboardQuit(event),
                'beginning-of-line': lambda event, spot = 'insert linestart': self.moveTo(event,spot) and b.keyboardQuit(event),
                'capitalize-word': lambda event, which = 'cap': self.capitalize(event,which) and b.keyboardQuit(event),
                'center-line': lambda event: self.centerLine(event) and b.keyboardQuit(event),
                'center-region': lambda event: self.centerRegion(event) and b.keyboardQuit(event),
                'dabbrev-completion': lambda event: self.dynamicExpansion2(event) and b.keyboardQuit(event),
                'dabbrev-expands': lambda event: self.dynamicExpansion(event) and b.keyboardQuit(event),
                'delete-char': lambda event: self.deleteNextChar(event) and b.keyboardQuit(event),
                'delete-indentation': lambda event: self.deleteIndentation(event) and b.keyboardQuit(event),
                'downcase-region': lambda event: self.upperLowerRegion(event,'low') and b.keyboardQuit(event),
                'downcase-word': lambda event, which = 'low': self.capitalize(event,which) and b.keyboardQuit(event),
                'end-of-buffer': lambda event, spot = 'end': self.moveTo(event,spot) and b.keyboardQuit(event),
                'end-of-line': lambda event, spot = 'insert lineend': self.moveTo(event,spot) and b.keyboardQuit(event),
                'eval-expression': self.startEvaluate,
                'fill-region-as-paragraph': self.fillRegionAsParagraph,
                'fill-region': self.fillRegion,
                'flush-lines': lambda event: self.flushLines,
                'forward-char': lambda event, which = 'Right': b.keyboardQuit(event) and self.manufactureKeyPress(event,which),
                'goto-char': lambda event: self.startGoto(event,True),
                'goto-line': lambda event: self.startGoto(event),
                'how-many': self.startHowMany, ### Change name?
                'indent-region': lambda event: self.indentRegion(event) and b.keyboardQuit(event),
                'indent-rigidly': lambda event: self.tabIndentRegion(event) and b.keyboardQuit(event),
                'indent-relative': self.indentRelative,
                'insert-file': lambda event: self.insertFile(event) and b.keyboardQuit(event),
                'keep-lines': self.keepLines,
                'kill-paragraph': self.killParagraph,
                'newline-and-indent': lambda event: self.insertNewLineAndTab(event) and b.keyboardQuit(event),
                'next-line': lambda event, which = 'Down': b.keyboardQuit(event) and self.manufactureKeyPress(event,which),
                'previous-line': lambda event, which = 'Up': b.keyboardQuit(event) and self.manufactureKeyPress(event,which),
                'replace-regex': lambda event: self.activateReplaceRegex() and self.replaceString(event),
                'replace-string': self.replaceString,
                'reverse-region': self.reverseRegion,
                'save-buffer': lambda event: self.saveFile(event) and b.keyboardQuit(event),
                'scroll-down': lambda event, way = 'south': self.screenscroll(event,way) and b.keyboardQuit(event),
                'scroll-up': lambda event, way = 'north': self.screenscroll(event,way) and b.keyboardQuit(event),
                'set-fill-column': self.setFillColumn,
                'set-fill-prefix': self.setFillPrefix,
                'set-mark-command': lambda event: self.setRegion(event) and b.keyboardQuit(event),
                'sort-columns': self.sortColumns,
                'sort-fields': self.sortFields,
                'sort-lines': self.sortLines,
                'split-line': lambda event: self.insertNewLineIndent(event) and b.keyboardQuit(event),
                'tabify': self.tabify,
                'transpose-chars': lambda event: self.swapCharacters(event) and b.keyboardQuit(event),
                'transpose-words': lambda event, sw = self.swapSpots: self.swapWords(event,sw) and b.keyboardQuit(event),
                'transpose-lines': lambda event: self.transposeLines(event) and b.keyboardQuit(event),
                'untabify': self.untabify,
                'upcase-region': lambda event: self.upperLowerRegion(event,'up') and b.keyboardQuit(event),
                'upcase-word': lambda event, which = 'up': self.capitalize(event,which) and b.keyboardQuit(event),
                'view-lossage': self.viewLossage,
                'what-line': self.whatLine,
        
                # Added by EKR:
                'back-sentence': self.backSentence,
                'delete-spaces': self.deleteSpaces,
                'forward-sentence': self.forwardSentence,
                'exchange-point-mark': self.exchangePointMark,
                'indent-to-comment-column': self.indentToCommentColumn,
                'insert-newline': self.insertNewline,
                'insert-parentheses': self.insertParentheses,
                'line-number': self.lineNumber,
                'move-past-close': self.movePastClose,
                'remove-blank-lines': self.removeBlankLines,
                'select-all': self.selectAll,
                'set-comment-column': self.setCommentColumn,
            }
        #@nonl
        #@-node:ekr.20050727093829: getPublicCommands
        #@+node:ekr.20050727093829.1: Entry points
        #@+node:ekr.20050724075352.57:capitalize
        def capitalize( self, event, which ):
            tbuffer = event.widget
            text = tbuffer.get( 'insert wordstart', 'insert wordend' )
            i = tbuffer.index( 'insert' )
            if text == ' ': return 'break'
            tbuffer.delete( 'insert wordstart', 'insert wordend' )
            if which == 'cap':
                text = text.capitalize() 
            if which == 'low':
                text = text.lower()
            if which == 'up':
                text = text.upper()
            tbuffer.insert( 'insert', text )
            tbuffer.mark_set( 'insert', i )    
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.57:capitalize
        #@+node:ekr.20050724075352.275:dynamic abbreviation...
        #@+node:ekr.20050724075352.276:dynamicExpansion
        def dynamicExpansion( self, event ):#, store = {'rlist': [], 'stext': ''} ):
            
            b = self.miniBuffer ; tbuffer = event.widget
            rlist = self.store[ 'rlist' ]
            stext = self.store[ 'stext' ]
            i = tbuffer.index( 'insert -1c wordstart' )
            i2 = tbuffer.index( 'insert -1c wordend' )
            txt = tbuffer.get( i, i2 )
            dA = tbuffer.tag_ranges( 'dA' )
            tbuffer.tag_delete( 'dA' )
            def doDa( txt, from_ = 'insert -1c wordstart', to_ = 'insert -1c wordend' ):
                tbuffer.delete( from_, to_ ) 
                tbuffer.insert( 'insert', txt, 'dA' )
                return b._tailEnd( tbuffer )
                
            if dA:
                dA1, dA2 = dA
                dtext = tbuffer.get( dA1, dA2 )
                if dtext.startswith( stext ) and i2 == dA2:
                    #This seems reasonable, since we cant get a whole word that has the '-' char in it, we do a good guess
                    if rlist:
                        txt = rlist.pop()
                    else:
                        txt = stext
                        tbuffer.delete( dA1, dA2 )
                        dA2 = dA1 #since the text is going to be reread, we dont want to include the last dynamic abbreviation
                        self.getDynamicList( tbuffer, txt, rlist )
                    return doDa( txt, dA1, dA2 )
                else:
                    dA = None
                    
            if not dA:
                self.store[ 'stext' ] = txt
                self.store[ 'rlist' ] = rlist = []
                self.getDynamicList( tbuffer, txt, rlist )
                if not rlist:
                    return 'break'
                txt = rlist.pop()
                return doDa( txt )
        #@nonl
        #@-node:ekr.20050724075352.276:dynamicExpansion
        #@+node:ekr.20050724075352.277:dynamicExpansion2
        def dynamicExpansion2( self, event ):
            
            b = self.miniBuffer ; tbuffer = event.widget
        
            i = tbuffer.index( 'insert -1c wordstart' )
            i2 = tbuffer.index( 'insert -1c wordend' )
            txt = tbuffer.get( i, i2 )   
            rlist = []
            self.getDynamicList( tbuffer, txt, rlist )
            dEstring = reduce( self.findPre, rlist )
            if dEstring:
                tbuffer.delete( i , i2 )
                tbuffer.insert( i, dEstring )    
                return b._tailEnd( tbuffer )
        #@-node:ekr.20050724075352.277:dynamicExpansion2
        #@+node:ekr.20050724075352.278:getDynamicList (helper)
        def getDynamicList( self, tbuffer, txt , rlist ):
        
             ttext = tbuffer.get( '1.0', 'end' )
             items = self.dynaregex.findall( ttext ) #make a big list of what we are considering a 'word'
             if items:
                 for word in items:
                     if not word.startswith( txt ) or word == txt: continue #dont need words that dont match or == the pattern
                     if word not in rlist:
                         rlist.append( word )
                     else:
                         rlist.remove( word )
                         rlist.append( word )
        #@nonl
        #@-node:ekr.20050724075352.278:getDynamicList (helper)
        #@-node:ekr.20050724075352.275:dynamic abbreviation...
        #@+node:ekr.20050724075352.310:esc methods for Python evaluation
        #@+node:ekr.20050724075352.311:watchEscape
        def watchEscape (self,event):
        
            b = self.miniBuffer ; tbuffer = event.widget
            if not b.hasState():
                b.setState('escape','start')
                b.setLabelBlue()
                b.set('Esc')
                return 'break'
            if b.whichState() == 'escape':
                state = b.getState('escape')
                hi1 = self.keysymhistory [0]
                hi2 = self.keysymhistory [1]
                if state == 'esc esc' and event.keysym == 'colon':
                    return self.startEvaluate(event)
                elif state == 'evaluate':
                    return self.escEvaluate(event)
                elif hi1 == hi2 == 'Escape':
                    b.setState('escape','esc esc')
                    b.set('Esc Esc -')
                    return 'break'
                elif event.keysym in ('Shift_L','Shift_R'):
                    return
                else:
                    return b.keyboardQuit(event)
        #@nonl
        #@-node:ekr.20050724075352.311:watchEscape
        #@+node:ekr.20050724075352.312:escEvaluate
        def escEvaluate (self,event):
        
            b = self.miniBuffer ; tbuffer = event.widget
        
            if b.get() == 'Eval:':
                b.set('')
        
            if event.keysym == 'Return':
                expression = b.get()
                try:
                    ok = False
                    result = eval(expression,{},{})
                    result = str(result)
                    tbuffer.insert('insert',result)
                    ok = True
                finally:
                    b.keyboardQuit(event)
                    if not ok:
                        b.set('Error: Invalid Expression')
                    return b._tailEnd(tbuffer)
            else:
                b.update(event)
                return 'break'
        #@nonl
        #@-node:ekr.20050724075352.312:escEvaluate
        #@+node:ekr.20050724075352.313:startEvaluate
        def startEvaluate (self,event):
        
            b = self.miniBuffer
            b.setLabelBlue()
            b.set('Eval:')
            b.setState('escape','evaluate')
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.313:startEvaluate
        #@-node:ekr.20050724075352.310:esc methods for Python evaluation
        #@+node:ekr.20050724075352.209:fill column and centering
        #@+at
        # These methods are currently just used in tandem to center the line 
        # or region within the fill column.
        # for example, dependent upon the fill column, this text:
        # 
        # cats
        # raaaaaaaaaaaats
        # mats
        # zaaaaaaaaap
        # 
        # may look like
        # 
        #                                  cats
        #                            raaaaaaaaaaaats
        #                                  mats
        #                              zaaaaaaaaap
        # after an center-region command via Alt-x.
        # 
        # 
        #@-at
        #@@c
        
        
        #@+others
        #@+node:ekr.20050724075352.210:centerLine
        def centerLine( self, event ):
            '''Centers line within current fillColumn'''
            
            b = self.miniBuffer ; tbuffer = event.widget
            ind = tbuffer.index( 'insert linestart' )
            txt = tbuffer.get( 'insert linestart', 'insert lineend' )
            txt = txt.strip()
            if len( txt ) >= self.fillColumn: return b._tailEnd( tbuffer )
            amount = ( self.fillColumn - len( txt ) ) / 2
            ws = ' ' * amount
            col, nind = ind.split( '.' )
            ind = tbuffer.search( '\w', 'insert linestart', regexp = True, stopindex = 'insert lineend' )
            if not ind: return 'break'
            tbuffer.delete( 'insert linestart', '%s' % ind )
            tbuffer.insert( 'insert linestart', ws )
            return b._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.210:centerLine
        #@+node:ekr.20050724075352.212:setFillColumn
        def setFillColumn (self,event):
        
            b = self.miniBuffer
        
            if b.getState('set-fill-column'):
                if event.keysym == 'Return':
                    value = b.get()
                    if value.isdigit():
                        self.fillColumn = int(value)
                    return b.keyboardQuit(event)
                elif event.char.isdigit() or event.char == '\b':
                    b.update(event)
            else:
                b.setState('set-fill-column',1)
                b.set('')
                b.setLabelBlue()
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.212:setFillColumn
        #@+node:ekr.20050724075352.211:centerRegion
        def centerRegion( self, event ):
        
            '''This method centers the current region within the fill column'''
        
            b = self.miniBuffer ; tbuffer = event.widget
            start = tbuffer.index( 'sel.first linestart' )
            sindex , x = start.split( '.' )
            sindex = int( sindex )
            end = tbuffer.index( 'sel.last linestart' )
            eindex , x = end.split( '.' )
            eindex = int( eindex )
            while sindex <= eindex:
                txt = tbuffer.get( '%s.0 linestart' % sindex , '%s.0 lineend' % sindex )
                txt = txt.strip()
                if len( txt ) >= self.fillColumn:
                    sindex = sindex + 1
                    continue
                amount = ( self.fillColumn - len( txt ) ) / 2
                ws = ' ' * amount
                ind = tbuffer.search( '\w', '%s.0' % sindex, regexp = True, stopindex = '%s.0 lineend' % sindex )
                if not ind: 
                    sindex = sindex + 1
                    continue
                tbuffer.delete( '%s.0' % sindex , '%s' % ind )
                tbuffer.insert( '%s.0' % sindex , ws )
                sindex = sindex + 1
            return b._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.211:centerRegion
        #@+node:ekr.20050724075352.207:setFillPrefix
        def setFillPrefix( self, event ):
        
            tbuffer = event.widget
            txt = tbuffer.get( 'insert linestart', 'insert' )
            self.fillPrefix = txt
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.207:setFillPrefix
        #@+node:ekr.20050724075352.208:_addPrefix
        def _addPrefix( self, ntxt ):
                ntxt = ntxt.split( '.' )
                ntxt = map( lambda a: self.fillPrefix+a, ntxt )
                ntxt = '.'.join( ntxt )               
                return ntxt
        #@nonl
        #@-node:ekr.20050724075352.208:_addPrefix
        #@-others
        #@nonl
        #@-node:ekr.20050724075352.209:fill column and centering
        #@+node:ekr.20050727152153:goto...
        #@+node:ekr.20050724075352.300:startGoto
        def startGoto (self,event,ch=False):
        
            b = self.miniBuffer
        
            b.setState('goto',b.getState()+1)
            b.set('')
            b.setLabelBlue()
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.300:startGoto
        #@-node:ekr.20050727152153:goto...
        #@+node:ekr.20050727152153.1:indent...
        #@+node:ekr.20050724075352.73:backToIndentation
        def backToIndentation( self, event ):
        
            tbuffer = event.widget
            i = tbuffer.index( 'insert linestart' )
            i2 = tbuffer.search( r'\w', i, stopindex = '%s lineend' % i, regexp = True )
            tbuffer.mark_set( 'insert', i2 )
            tbuffer.update_idletasks()
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.73:backToIndentation
        #@+node:ekr.20050724075352.251:deleteIndentation
        def deleteIndentation( self, event ):
        
            b = self.miniBuffer ; tbuffer = event.widget
            txt = tbuffer.get( 'insert linestart' , 'insert lineend' )
            txt = ' %s' % txt.lstrip()
            tbuffer.delete( 'insert linestart' , 'insert lineend +1c' )    
            i  = tbuffer.index( 'insert - 1c' )
            tbuffer.insert( 'insert -1c', txt )
            tbuffer.mark_set( 'insert', i )
            return b._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.251:deleteIndentation
        #@+node:ekr.20050724075352.66:insertNewLineIndent
        def insertNewLineIndent( self, event ):
            tbuffer =  event.widget
            txt = tbuffer.get( 'insert linestart', 'insert lineend' )
            txt = self.getWSString( txt )
            i = tbuffer.index( 'insert' )
            tbuffer.insert( i, txt )
            tbuffer.mark_set( 'insert', i )    
            return self.insertNewLine( event )
        #@nonl
        #@-node:ekr.20050724075352.66:insertNewLineIndent
        #@+node:ekr.20050724075352.74:indentRelative
        def indentRelative( self, event ):
            
            b = self.miniBuffer ; tbuffer = event.widget
            i = tbuffer.index( 'insert' )
            l,c = i.split( '.' )
            c2 = int( c )
            l2 = int( l ) - 1
            if l2 < 1: return b.keyboardQuit( event )
            txt = tbuffer.get( '%s.%s' % (l2, c2 ), '%s.0 lineend' % l2 )
            if len( txt ) <= len( tbuffer.get( 'insert', 'insert lineend' ) ):
                tbuffer.insert(  'insert', '\t' )
            else:
                reg = re.compile( '(\s+)' )
                ntxt = reg.split( txt )
                replace_word = re.compile( '\w' )
                for z in ntxt:
                    if z.isspace():
                        tbuffer.insert( 'insert', z )
                        break
                    else:
                        z = replace_word.subn( ' ', z )
                        tbuffer.insert( 'insert', z[ 0 ] )
                        tbuffer.update_idletasks()
                
                
            b.keyboardQuit( event )
            return b._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.74:indentRelative
        #@-node:ekr.20050727152153.1:indent...
        #@+node:ekr.20050724075352.153:info...
        #@+node:ekr.20050724075352.154:howMany
        def howMany (self,event):
        
            b = self.miniBuffer ; tbuffer = event.widget
        
            if event.keysym == 'Return':
                txt = tbuffer.get('1.0','end')
                reg1 = b.get()
                reg = re.compile(reg1)
                i = reg.findall(txt)
                b.set('%s occurances found of %s' % (len(i),reg1))
                b.setLabelGrey()
                b.setState('howM',False)
            else:
                b.update(event)
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.154:howMany
        #@+node:ekr.20050724075352.81:lineNumber
        def lineNumber (self,event):
        
            b = self.miniBuffer ; tbuffer = event.widget
        
            b.stopControlX(event)
            i = tbuffer.index('insert')
            i1, i2 = i.split('.')
            c = tbuffer.get('insert','insert + 1c')
            txt = tbuffer.get('1.0','end')
            txt2 = tbuffer.get('1.0','insert')
            perc = len(txt) * .01
            perc = int(len(txt2)/perc)
            b.set('Char: %s point %s of %s(%s%s)  Column %s' % (c,len(txt2),len(txt),perc,'%',i1))
        
            return 'break'
        
        #@-node:ekr.20050724075352.81:lineNumber
        #@+node:ekr.20050724075352.155:startHowMany
        def startHowMany (self,event):
        
            b = self.miniBuffer
        
            b.setState('howM',1)
            b.set('')
            b.setLabelBlue()
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.155:startHowMany
        #@+node:ekr.20050724075352.82:viewLossage
        def viewLossage (self,event):
        
            b = self.miniBuffer
            loss = ''.join(Emacs.lossage)
            b.keyboardQuit(event)
            b.set(loss)
        #@nonl
        #@-node:ekr.20050724075352.82:viewLossage
        #@+node:ekr.20050724075352.83:whatLine
        def whatLine (self,event):
        
            b = self.miniBuffer ; tbuffer = event.widget
            i = tbuffer.index('insert')
            i1, i2 = i.split('.')
            b.keyboardQuit(event)
            b.set("Line %s" % i1)
        #@nonl
        #@-node:ekr.20050724075352.83:whatLine
        #@-node:ekr.20050724075352.153:info...
        #@+node:ekr.20050727152153.2:Insert/delete...
        #@+node:ekr.20050724075352.67:insertNewLineAndTab
        def insertNewLineAndTab( self, event ):
            
            '''Insert a newline and tab'''
            
            b = self.miniBuffer ;tbuffer = event.widget
            self.insertNewLine( event )
            i = tbuffer.index( 'insert +1c' )
            tbuffer.insert( i, '\t' )
            tbuffer.mark_set( 'insert', '%s lineend' % i )
            return b._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.67:insertNewLineAndTab
        #@+node:ekr.20050724075352.252:deleteNextChar
        def deleteNextChar( self,event ):
        
            b = self.miniBuffer ; tbuffer = event.widget
            i = tbuffer.index( 'insert' )
            tbuffer.delete( i, '%s +1c' % i )
            return b._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.252:deleteNextChar
        #@-node:ekr.20050727152153.2:Insert/delete...
        #@+node:ekr.20050724075352.295:line...
        #@+node:ekr.20050727111709: Entries
        #@+node:ekr.20050727111709.1:flushLines
        def flushLines (self,event):
        
            '''Delete each line that contains a match for regexp, operating on the text after point.
        
            In Transient Mark mode, if the region is active, the command operates on the region instead.'''
        
            return self.startLines(event,which='flush')
        #@nonl
        #@-node:ekr.20050727111709.1:flushLines
        #@+node:ekr.20050727111709.2:keepLines
        def keepLines (self,event):
        
            '''Delete each line that does not contain a match for regexp, operating on the text after point.
        
            In Transient Mark mode, if the region is active, the command operates on the region instead.'''
        
            return self.startLines(event,which='keep')
        #@nonl
        #@-node:ekr.20050727111709.2:keepLines
        #@-node:ekr.20050727111709: Entries
        #@+node:ekr.20050724075352.296:alterLines
        def alterLines( self, event, which ):
            
            b = self.miniBuffer ; tbuffer = event.widget
            i = tbuffer.index( 'insert' )
            end = 'end'
            if tbuffer.tag_ranges( 'sel' ):
                i = tbuffer.index( 'sel.first' )
                end = tbuffer.index( 'sel.last' )
            txt = tbuffer.get( i, end )
            tlines = txt.splitlines( True )
            if which == 'flush':    keeplines = list( tlines )
            else:                   keeplines = []
            pattern = b.get()
            try:
                regex = re.compile( pattern )
                for n , z in enumerate( tlines ):
                    f = regex.findall( z )
                    if which == 'flush' and f:
                        keeplines[ n ] = None
                    elif f:
                        keeplines.append( z )
            except Exception,x:
                return
            if which == 'flush':
                keeplines = [ x for x in keeplines if x != None ]
            tbuffer.delete( i, end )
            tbuffer.insert( i, ''.join( keeplines ) )
            tbuffer.mark_set( 'insert', i )
            b._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.296:alterLines
        #@+node:ekr.20050724075352.297:processLines
        def processLines (self,event):
        
            b = self.miniBuffer
            state = b.getState('alterlines')
        
            if state.startswith('start'):
                state = state [5:]
                b.setState('alterlines',state)
                b.set('')
        
            if event.keysym == 'Return':
                self.alterLines(event,state)
                return b.keyboardQuit(event)
            else:
                b.update(event)
                return 'break'
        #@nonl
        #@-node:ekr.20050724075352.297:processLines
        #@+node:ekr.20050724075352.298:startLines
        def startLines (self,event,which='flush'):
        
            b = self.miniBuffer
            b.keyboardQuit(event)
            b.setState('alterlines','start%s' % which)
            b.setLabelBlue()
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.298:startLines
        #@-node:ekr.20050724075352.295:line...
        #@+node:ekr.20050724075352.156:paragraph...
        #@+others
        #@+node:ekr.20050724075352.157:selectParagraph
        def selectParagraph( self, event ):
        
            b = self.miniBuffer ; tbuffer = event.widget
            txt = tbuffer.get( 'insert linestart', 'insert lineend' )
            txt = txt.lstrip().rstrip()
            i = tbuffer.index( 'insert' )
            if not txt:
                while 1:
                    i = tbuffer.index( '%s + 1 lines' % i )
                    txt = tbuffer.get( '%s linestart' % i, '%s lineend' % i )
                    txt = txt.lstrip().rstrip()
                    if txt:
                        self._selectParagraph( tbuffer, i )
                        break
                    if tbuffer.index( '%s lineend' % i ) == tbuffer.index( 'end' ):
                        return 'break'
            if txt:
                while 1:
                    i = tbuffer.index( '%s - 1 lines' % i )
                    txt = tbuffer.get( '%s linestart' % i, '%s lineend' % i )
                    txt = txt.lstrip().rstrip()
                    if not txt or tbuffer.index( '%s linestart' % i ) == tbuffer.index( '1.0' ):
                        if not txt:
                            i = tbuffer.index( '%s + 1 lines' % i )
                        self._selectParagraph( tbuffer, i )
                        break     
            return b._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.157:selectParagraph
        #@+node:ekr.20050724075352.158:_selectParagraph
        def _selectParagraph( self, tbuffer, start ):
            i2 = start
            while 1:
                txt = tbuffer.get( '%s linestart' % i2, '%s lineend' % i2 )
                if tbuffer.index( '%s lineend' % i2 )  == tbuffer.index( 'end' ):
                    break
                txt = txt.lstrip().rstrip()
                if not txt: break
                else:
                    i2 = tbuffer.index( '%s + 1 lines' % i2 )
            tbuffer.tag_add( 'sel', '%s linestart' % start, '%s lineend' % i2 )
            tbuffer.mark_set( 'insert', '%s lineend' % i2 )
        #@nonl
        #@-node:ekr.20050724075352.158:_selectParagraph
        #@+node:ekr.20050724075352.159:killParagraph
        def killParagraph( self, event ):
            
            b = self.miniBuffer ; tbuffer = event.widget
            i = tbuffer.index( 'insert' )
            txt = tbuffer.get( 'insert linestart', 'insert lineend' )
            if not txt.rstrip().lstrip():
                i = tbuffer.search( r'\w', i, regexp = True, stopindex = 'end' )
            self._selectParagraph( tbuffer, i )
            i2 = tbuffer.index( 'insert' )
            self.kill( event, i, i2 )
            tbuffer.mark_set( 'insert', i )
            tbuffer.selection_clear()
            return b._tailEnd( tbuffer )
        #@-node:ekr.20050724075352.159:killParagraph
        #@+node:ekr.20050724075352.160:backwardKillParagraph
        def backwardKillParagraph( self, event ):
         
            b = self.miniBuffer ; tbuffer = event.widget
            i = tbuffer.index( 'insert' )
            i2 = i
            txt = tbuffer.get( 'insert linestart', 'insert lineend' )
            if not txt.rstrip().lstrip():
                self.movingParagraphs( event, -1 )
                i2 = tbuffer.index( 'insert' )
            self.selectParagraph( event )
            i3 = tbuffer.index( 'sel.first' )
            self.kill( event, i3, i2 )
            tbuffer.mark_set( 'insert', i )
            tbuffer.selection_clear()
            return b._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.160:backwardKillParagraph
        #@+node:ekr.20050724075352.214:fillRegion
        def fillRegion (self,event):
        
            b = self.miniBuffer ; tbuffer = event.widget
            if not self._chckSel(event):
                return
            s1 = tbuffer.index('sel.first')
            s2 = tbuffer.index('sel.last')
            tbuffer.mark_set('insert',s1)
            self.movingParagraphs(event,-1)
            if tbuffer.index('insert linestart') == '1.0':
                self.fillParagraph(event)
            while 1:
                self.movingParagraphs(event,1)
                if tbuffer.compare('insert','>',s2):
                    break
                self.fillParagraph(event)
            return b._tailEnd(tbuffer)
        #@nonl
        #@-node:ekr.20050724075352.214:fillRegion
        #@+node:ekr.20050724075352.202:UNTESTED
        #@+at
        # 
        # untested as of yet for .5 conversion.
        # 
        #@-at
        #@@c
        
        
        #@+others
        #@+node:ekr.20050724075352.203:movingParagraphs
        def movingParagraphs( self, event, way ):
            b = self.miniBuffer ; tbuffer = event.widget
            i = tbuffer.index( 'insert' )
            if way == 1:
                while 1:
                    txt = tbuffer.get( '%s linestart' % i, '%s lineend' %i )
                    txt = txt.rstrip().lstrip()
                    if not txt:
                        i = tbuffer.search( r'\w', i, regexp = True, stopindex = 'end' )
                        i = '%s' %i
                        break
                    else:
                        i = tbuffer.index( '%s + 1 lines' % i )
                        if tbuffer.index( '%s linestart' % i ) == tbuffer.index( 'end' ):
                            i = tbuffer.search( r'\w', 'end', backwards = True, regexp = True, stopindex = '1.0' )
                            i = '%s + 1c' % i
                            break
            else:
                while 1:
                    txt = tbuffer.get( '%s linestart' % i, '%s lineend' %i )
                    txt = txt.rstrip().lstrip()
                    if not txt:
                        i = tbuffer.search( r'\w', i, backwards = True, regexp = True, stopindex = '1.0' )
                        i = '%s +1c' %i
                        break
                    else:
                        i = tbuffer.index( '%s - 1 lines' % i )
                        if tbuffer.index( '%s linestart' % i ) == '1.0':
                            i = tbuffer.search( r'\w', '1.0', regexp = True, stopindex = 'end' )
                            break
            if i : 
                tbuffer.mark_set( 'insert', i )
                tbuffer.see( 'insert' )
                return b._tailEnd( tbuffer )
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.203:movingParagraphs
        #@+node:ekr.20050724075352.204:fillParagraph
        def fillParagraph( self, event ):
            b = self.miniBuffer ; tbuffer = event.widget
            txt = tbuffer.get( 'insert linestart', 'insert lineend' )
            txt = txt.lstrip().rstrip()
            if txt:
                i = tbuffer.index( 'insert' )
                i2 = i
                txt2 = txt
                while txt2:
                    pi2 = tbuffer.index( '%s - 1 lines' % i2)
                    txt2 = tbuffer.get( '%s linestart' % pi2, '%s lineend' % pi2 )
                    if tbuffer.index( '%s linestart' % pi2 ) == '1.0':
                        i2 = tbuffer.search( '\w', '1.0', regexp = True, stopindex = 'end' )
                        break
                    if txt2.lstrip().rstrip() == '': break
                    i2 = pi2
                i3 = i
                txt3 = txt
                while txt3:
                    pi3 = tbuffer.index( '%s + 1 lines' %i3 )
                    txt3 = tbuffer.get( '%s linestart' % pi3, '%s lineend' % pi3 )
                    if tbuffer.index( '%s lineend' % pi3 ) == tbuffer.index( 'end' ):
                        i3 = tbuffer.search( '\w', 'end', backwards = True, regexp = True, stopindex = '1.0' )
                        break
                    if txt3.lstrip().rstrip() == '': break
                    i3 = pi3
                ntxt = tbuffer.get( '%s linestart' %i2, '%s lineend' %i3 )
                ntxt = self._addPrefix( ntxt )
                tbuffer.delete( '%s linestart' %i2, '%s lineend' % i3 )
                tbuffer.insert( i2, ntxt )
                tbuffer.mark_set( 'insert', i )
                return b._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.204:fillParagraph
        #@+node:ekr.20050724075352.205:fillRegionAsParagraph
        def fillRegionAsParagraph( self, event ):
            
            b = self.miniBuffer ; tbuffer = event.widget
            if not self._chckSel( event ):
                return
            i1 = tbuffer.index( 'sel.first linestart' )
            i2 = tbuffer.index( 'sel.last lineend' )
            txt = tbuffer.get(  i1,  i2 )
            txt = self._addPrefix( txt )
            tbuffer.delete( i1, i2 )
            tbuffer.insert( i1, txt )
            return b._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.205:fillRegionAsParagraph
        #@-others
        #@nonl
        #@-node:ekr.20050724075352.202:UNTESTED
        #@-others
        #@nonl
        #@-node:ekr.20050724075352.156:paragraph...
        #@+node:ekr.20050724075352.213:region...
        #@+others
        #@+node:ekr.20050724075352.215:setRegion
        def setRegion( self, event ):
        
            mrk = 'sel'
            tbuffer = event.widget
            def extend( event ):
                widget = event.widget
                widget.mark_set( 'insert', 'insert + 1c' )
                if self.inRange( widget, mrk ):
                    widget.tag_remove( mrk, 'insert -1c' )
                else:
                    widget.tag_add( mrk, 'insert -1c' )
                    widget.tag_configure( mrk, background = 'lightgrey' )
                    self.testinrange( widget )
                return 'break'
                
            def truncate( event ):
                widget = event.widget
                widget.mark_set( 'insert', 'insert -1c' )
                if self.inRange( widget, mrk ):
                    self.testinrange( widget )
                    widget.tag_remove( mrk, 'insert' )
                else:
                    widget.tag_add( mrk, 'insert' )
                    widget.tag_configure( mrk, background = 'lightgrey' )
                    self.testinrange( widget  )
                return 'break'
                
            def up( event ):
                widget = event.widget
                if not self.testinrange( widget ):
                    return 'break'
                widget.tag_add( mrk, 'insert linestart', 'insert' )
                i = widget.index( 'insert' )
                i1, i2 = i.split( '.' )
                i1 = str( int( i1 ) - 1 )
                widget.mark_set( 'insert', i1+'.'+i2)
                widget.tag_add( mrk, 'insert', 'insert lineend + 1c' )
                if self.inRange( widget, mrk ,l = '-1c', r = '+1c') and widget.index( 'insert' ) != '1.0':
                    widget.tag_remove( mrk, 'insert', 'end' )  
                return 'break'
                
            def down( event ):
                widget = event.widget
                if not self.testinrange( widget ):
                    return 'break'
                widget.tag_add( mrk, 'insert', 'insert lineend' )
                i = widget.index( 'insert' )
                i1, i2 = i.split( '.' )
                i1 = str( int( i1 ) + 1 )
                widget.mark_set( 'insert', i1 +'.'+i2 )
                widget.tag_add( mrk, 'insert linestart -1c', 'insert' )
                if self.inRange( widget, mrk , l = '-1c', r = '+1c' ): 
                    widget.tag_remove( mrk, '1.0', 'insert' )
                return 'break'
                
            extend( event )   
            tbuffer.bind( '<Right>', extend, '+' )
            tbuffer.bind( '<Left>', truncate, '+' )
            tbuffer.bind( '<Up>', up, '+' )
            tbuffer.bind( '<Down>', down, '+' )
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.215:setRegion
        #@+node:ekr.20050724075352.216:indentRegion
        def indentRegion( self, event ):
            tbuffer = event.widget
            mrk = 'sel'
            trange = tbuffer.tag_ranges( mrk )
            if len( trange ) != 0:
                ind = tbuffer.search( '\w', '%s linestart' % trange[ 0 ], stopindex = 'end', regexp = True )
                if not ind : return
                text = tbuffer.get( '%s linestart' % ind ,  '%s lineend' % ind)
                sstring = text.lstrip()
                sstring = sstring[ 0 ]
                ws = text.split( sstring )
                if len( ws ) > 1:
                    ws = ws[ 0 ]
                else:
                    ws = ''
                s , s1 = trange[ 0 ].split( '.' )
                e , e1 = trange[ -1 ].split( '.' )
                s = int( s )
                s = s + 1
                e = int( e ) + 1
                for z in xrange( s , e ):
                    t2 = tbuffer.get( '%s.0' %z ,  '%s.0 lineend'%z)
                    t2 = t2.lstrip()
                    t2 = ws + t2
                    tbuffer.delete( '%s.0' % z ,  '%s.0 lineend' %z)
                    tbuffer.insert( '%s.0' % z, t2 )
                tbuffer.event_generate( '<Key>' )
                tbuffer.update_idletasks()
            self.removeRKeys( tbuffer )
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.216:indentRegion
        #@+node:ekr.20050724075352.217:tabIndentRegion
        def tabIndentRegion( self,event ):
        
            b = self.miniBuffer ; tbuffer = event.widget
            if not self._chckSel( event ):
                return
            i = tbuffer.index( 'sel.first' )
            i2 = tbuffer.index( 'sel.last' )
            i = tbuffer.index( '%s linestart' %i )
            i2 = tbuffer.index( '%s linestart' % i2)
            while 1:
                tbuffer.insert( i, '\t' )
                if i == i2: break
                i = tbuffer.index( '%s + 1 lines' % i )    
            return b._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.217:tabIndentRegion
        #@+node:ekr.20050724075352.218:countRegion
        def countRegion (self,event):
        
            b = self.miniBuffer ; tbuffer = event.widget
            txt = tbuffer.get('sel.first','sel.last')
            lines = 1 ; chars = 0
            for z in txt:
                if z == '\n':   lines = lines + 1
                else:           chars = chars + 1
        
            b.set('Region has %s lines, %s characters' % (lines,chars))
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.218:countRegion
        #@+node:ekr.20050724075352.219:reverseRegion
        def reverseRegion (self,event):
        
            b = self.miniBuffer ; tbuffer = event.widget
        
            if not self._chckSel(event): return
            ins = tbuffer.index('insert')
            is1 = tbuffer.index('sel.first')
            is2 = tbuffer.index('sel.last')
            txt = tbuffer.get('%s linestart' % is1,'%s lineend' % is2)
            tbuffer.delete('%s linestart' % is1,'%s lineend' % is2)
            txt = txt.split('\n')
            txt.reverse()
            istart = is1.split('.')
            istart = int(istart[0])
            for z in txt:
                tbuffer.insert('%s.0' % istart,'%s\n' % z)
                istart = istart + 1
            tbuffer.mark_set('insert',ins)
            b.stateManager.clear()
            b.reset()
            return b._tailEnd(tbuffer)
        #@nonl
        #@-node:ekr.20050724075352.219:reverseRegion
        #@+node:ekr.20050724075352.220:upperLowerRegion
        def upperLowerRegion( self, event, way ):
        
            tbuffer = event.widget
            mrk = 'sel'
            trange = tbuffer.tag_ranges( mrk )
            if len( trange ) != 0:
                text = tbuffer.get( trange[ 0 ] , trange[ -1 ] )
                i = tbuffer.index( 'insert' )
                if text == ' ': return 'break'
                tbuffer.delete( trange[ 0 ], trange[ -1 ] )
                if way == 'low':
                    text = text.lower()
                if way == 'up':
                    text = text.upper()
                tbuffer.insert( 'insert', text )
                tbuffer.mark_set( 'insert', i ) 
            self.removeRKeys( tbuffer )
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.220:upperLowerRegion
        #@-others
        #@nonl
        #@-node:ekr.20050724075352.213:region...
        #@+node:ekr.20050724075352.60:replace...
        #@+node:ekr.20050724075352.61:replaceString
        def replaceString (self,event): # event IS used
            
            b = self.miniBuffer ; tbuffer = event.widget
            stateKind = 'rString'
            # This should not be here.
            if event.keysym in ('Control_L','Control_R'): return
            state = b.getState(stateKind)
            regex = self._useRegex
            prompt = 'Replace ' + g.choose(regex,'Regex','String')
            if state == 0:
                self._sString = self._rpString = ''
                s = '%s: ' % prompt
                b.set(s)
                # Get arg and enter state 1.
                return b.getArg(event,stateKind,1) 
            elif state == 1:
                self._sString = b.arg
                s = '%s: %s With: ' % (prompt,self._sString)
                b.set(s)
                # Get arg and enter state 2.
                return b.getArg(event,stateKind,2)
            elif state == 2:
                self._rpString = b.arg
                #@        << do the replace >>
                #@+node:ekr.20050730074556.1:<< do the replace >>
                # g.es('%s %s by %s' % (prompt,repr(self._sString),repr(self._rpString)),color='blue')
                i = 'insert' ; end = 'end' ; count = 0
                if tbuffer.tag_ranges('sel'):
                    i = tbuffer.index('sel.first')
                    end = tbuffer.index('sel.last')
                if regex:
                    txt = tbuffer.get(i,end)
                    try:
                        pattern = re.compile(self._sString)
                    except:
                        b.keyboardQuit(event)
                        b.set("Illegal regular expression")
                        return 'break'
                    count = len(pattern.findall(txt))
                    if count:
                        ntxt = pattern.sub(self._rpString,txt)
                        tbuffer.delete(i,end)
                        tbuffer.insert(i,ntxt)
                else:
                    # Problem: adds newline at end of text.
                    txt = tbuffer.get(i,end)
                    count = txt.count(self._sString)
                    if count:
                        ntxt = txt.replace(self._sString,self._rpString)
                        tbuffer.delete(i,end)
                        tbuffer.insert(i,ntxt)
                #@nonl
                #@-node:ekr.20050730074556.1:<< do the replace >>
                #@nl
                s = 'Replaced %s occurances' % count
                b.set(s)
                b.setLabelGrey()
                b.stateManager.clear()
                self._useRegex = False
                return b._tailEnd(tbuffer)
        #@nonl
        #@-node:ekr.20050724075352.61:replaceString
        #@+node:ekr.20050724075352.62:activateReplaceRegex
        def activateReplaceRegex( self ):
            '''This method turns regex replace on for replaceString'''
            self._useRegex = True
            return True
        #@nonl
        #@-node:ekr.20050724075352.62:activateReplaceRegex
        #@-node:ekr.20050724075352.60:replace...
        #@+node:ekr.20050724075352.71:screenscroll
        def screenscroll (self,event,way='north'):
        
            b = self.miniBuffer ; tbuffer = event.widget
            chng = self.measure(tbuffer)
            i = tbuffer.index('insert')
        
            if way == 'north':
                i1, i2 = i.split('.')
                i1 = int(i1) - chng [0]
            else:
                i1, i2 = i.split('.')
                i1 = int(i1) + chng [0]
        
            tbuffer.mark_set('insert','%s.%s' % (i1,i2))
            tbuffer.see('insert')
            return b._tailEnd(tbuffer)
        #@nonl
        #@-node:ekr.20050724075352.71:screenscroll
        #@+node:ekr.20050724075352.279:sort...
        #@+node:ekr.20050724075352.280:sortLines
        def sortLines( self, event , which = None ): # event IS used.
        
            b = self.miniBuffer ; tbuffer = event.widget  
            if not self._chckSel( event ):
                return b.keyboardQuit( event )
            i = tbuffer.index( 'sel.first' )
            i2 = tbuffer.index( 'sel.last' )
            is1 = i.split( '.' )
            is2 = i2.split( '.' )
            txt = tbuffer.get( '%s.0' % is1[ 0 ], '%s.0 lineend' % is2[ 0 ] )
            ins = tbuffer.index( 'insert' )
            txt = txt.split( '\n' )
            tbuffer.delete( '%s.0' % is1[ 0 ], '%s.0 lineend' % is2[ 0 ] )
            txt.sort()
            if which:
                txt.reverse()
            inum = int(is1[ 0 ])
            for z in txt:
                tbuffer.insert( '%s.0' % inum, '%s\n' % z ) 
                inum = inum + 1
            tbuffer.mark_set( 'insert', ins )
            b.keyboardQuit( event )
            return b._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.280:sortLines
        #@+node:ekr.20050724075352.281:sortColumns
        def sortColumns( self, event ):
        
            b = self.miniBuffer ; tbuffer = event.widget
            if not self._chckSel( event ):
                return b.keyboardQuit( event )
                
            ins = tbuffer.index( 'insert' )
            is1 = tbuffer.index( 'sel.first' )
            is2 = tbuffer.index( 'sel.last' )   
            sint1, sint2 = is1.split( '.' )
            sint2 = int( sint2 )
            sint3, sint4 = is2.split( '.' )
            sint4 = int( sint4 )
            txt = tbuffer.get( '%s.0' % sint1, '%s.0 lineend' % sint3 )
            tbuffer.delete( '%s.0' % sint1, '%s.0 lineend' % sint3 )
            columns = []
            i = int( sint1 )
            i2 = int( sint3 )
            while i <= i2:
                t = tbuffer.get( '%s.%s' %( i, sint2 ), '%s.%s' % ( i, sint4 ) )
                columns.append( t )
                i = i + 1
            txt = txt.split( '\n' )
            zlist = zip( columns, txt )
            zlist.sort()
            i = int( sint1 )      
            for z in xrange( len( zlist ) ):
                 tbuffer.insert( '%s.0' % i, '%s\n' % zlist[ z ][ 1 ] ) 
                 i = i + 1
            tbuffer.mark_set( 'insert', ins )
            return b._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.281:sortColumns
        #@+node:ekr.20050724075352.282:sortFields
        def sortFields( self, event, which = None ):
            
            b = self.miniBuffer ; tbuffer = event.widget
            if not self._chckSel( event ):
                return b.keyboardQuit( event )
            ins = tbuffer.index( 'insert' )
            is1 = tbuffer.index( 'sel.first' )
            is2 = tbuffer.index( 'sel.last' )
            txt = tbuffer.get( '%s linestart' % is1, '%s lineend' % is2 )
            txt = txt.split( '\n' )
            fields = []
            import re
            fn = r'\w+'
            frx = re.compile( fn )
            for z in txt:
                f = frx.findall( z )
                if not which:
                    fields.append( f[ 0 ] )
                else:
                    i =  int( which )
                    if len( f ) < i:
                        return b._tailEnd( tbuffer )
                    i = i - 1            
                    fields.append( f[ i ] )
            nz = zip( fields, txt )
            nz.sort()
            tbuffer.delete( '%s linestart' % is1, '%s lineend' % is2 )
            i = is1.split( '.' )
            int1 = int( i[ 0 ] )
            for z in nz:
                tbuffer.insert( '%s.0' % int1, '%s\n'% z[1] )
                int1 = int1 + 1
            tbuffer.mark_set( 'insert' , ins )
            return b._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.282:sortFields
        #@-node:ekr.20050724075352.279:sort...
        #@+node:ekr.20050727152153.3:swap/transpose...
        #@+node:ekr.20050724075352.68:transposeLines
        def transposeLines( self, event ):
        
            b = self.miniBuffer ; tbuffer = event.widget
            i = tbuffer.index( 'insert' )
            i1, i2 = i.split( '.' )
            i1 = str( int( i1 ) -1 )
            if i1 != '0':
                l2 = tbuffer.get( 'insert linestart', 'insert lineend' )
                tbuffer.delete( 'insert linestart-1c', 'insert lineend' )
                tbuffer.insert( i1+'.0', l2 +'\n')
            else:
                l2 = tbuffer.get( '2.0', '2.0 lineend' )
                tbuffer.delete( '2.0', '2.0 lineend' )
                tbuffer.insert( '1.0', l2 + '\n' )
            return b._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.68:transposeLines
        #@+node:ekr.20050724075352.58:swapWords
        def swapWords( self, event , swapspots ):
            tbuffer = event.widget
            txt = tbuffer.get( 'insert wordstart', 'insert wordend' )
            if txt == ' ' : return 'break'
            i = tbuffer.index( 'insert wordstart' )
            if len( swapspots ) != 0:
                def swp( find, ftext, lind, ltext ):
                    tbuffer.delete( find, '%s wordend' % find )
                    tbuffer.insert( find, ltext )
                    tbuffer.delete( lind, '%s wordend' % lind )
                    tbuffer.insert( lind, ftext )
                    swapspots.pop()
                    swapspots.pop()
                    return 'break'
                if tbuffer.compare( i , '>', swapspots[ 1 ] ):
                    return swp( i, txt, swapspots[ 1 ], swapspots[ 0 ] )
                elif tbuffer.compare( i , '<', swapspots[ 1 ] ):
                    return swp( swapspots[ 1 ], swapspots[ 0 ], i, txt )
                else:
                    return 'break'
            else:
                swapspots.append( txt )
                swapspots.append( i )
                return 'break'
        #@nonl
        #@-node:ekr.20050724075352.58:swapWords
        #@+node:ekr.20050724075352.63:swapCharacters
        def swapCharacters( self, event ):
        
            b = self.miniBuffer ; tbuffer = event.widget
            i = tbuffer.index( 'insert' )
            c1 = tbuffer.get( 'insert', 'insert +1c' )
            c2 = tbuffer.get( 'insert -1c', 'insert' )
            tbuffer.delete( 'insert -1c', 'insert' )
            tbuffer.insert( 'insert', c1 )
            tbuffer.delete( 'insert', 'insert +1c' )
            tbuffer.insert( 'insert', c2 )
            tbuffer.mark_set( 'insert', i )
            return b._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.63:swapCharacters
        #@-node:ekr.20050727152153.3:swap/transpose...
        #@+node:ekr.20050724075352.314:tabify...
        def tabify (self,event):
            return self._tabify (event,which='tabify')
            
        def untabify (self,event):
            return self._tabify (event,which='untabify')
        #@nonl
        #@+node:ekr.20050724075352.315:_tabify
        def _tabify (self,event,which='tabify'):
        
            b = self.miniBuffer ; tbuffer = event.widget
            if tbuffer.tag_ranges('sel'):
                i = tbuffer.index('sel.first')
                end = tbuffer.index('sel.last')
                txt = tbuffer.get(i,end)
                if which == 'tabify':
                    pattern = re.compile(' {4,4}')
                    ntxt = pattern.sub('\t',txt)
                else:
                    pattern = re.compile('\t')
                    ntxt = pattern.sub('    ',txt)
                tbuffer.delete(i,end)
                tbuffer.insert(i,ntxt)
                b.keyboardQuit(event)
                return b._tailEnd(tbuffer)
        
            b.keyboardQuit(event)
        #@nonl
        #@-node:ekr.20050724075352.315:_tabify
        #@-node:ekr.20050724075352.314:tabify...
        #@+node:ekr.20050724075352.239:zap...
        #@+node:ekr.20050724075352.240:startZap
        def startZap (self,event):
        
            b = self.miniBuffer
        
            b.setState('zap',1)
            b.setLabelBlue()
            b.set('Zap To Character')
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.240:startZap
        #@+node:ekr.20050724075352.241:zapTo
        def zapTo (self,event):
        
            b = self.miniBuffer ; tbuffer = event.widget
            s = string.ascii_letters+string.digits+string.punctuation
        
            if len(event.char) != 0 and event.char in s:
                b.setState('zap',False)
                i = tbuffer.search(event.char,'insert',stopindex='end')
                b.reset()
                if i:
                    t = tbuffer.get('insert','%s+1c' % i)
                    self.killBufferCommands.addToKillBuffer(t)
                    tbuffer.delete('insert','%s+1c' % i)
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.241:zapTo
        #@-node:ekr.20050724075352.239:zap...
        #@-node:ekr.20050727093829.1: Entry points
        #@+node:ekr.20050727100634:New Entry points
        #@+node:ekr.20050727104740:backSentence
        def backSentence (self,event):
        
            tbuffer = event.widget
            i = tbuffer.search('.','insert',backwards=True,stopindex='1.0')
        
            if i:
                i2 = tbuffer.search('.',i,backwards=True,stopindex='1.0')
                if not i2:
                    i2 = '1.0'
                if i2:
                    i3 = tbuffer.search('\w',i2,stopindex=i,regexp=True)
                    if i3:
                        tbuffer.mark_set('insert',i3)
            else:
                tbuffer.mark_set('insert','1.0')
        
            return self.miniBuffer._tailEnd(tbuffer)
        #@nonl
        #@-node:ekr.20050727104740:backSentence
        #@+node:ekr.20050724075352.150:comment column methods
        #@+node:ekr.20050724075352.151:setCommentColumn
        def setCommentColumn (self,event):
        
            cc = event.widget.index('insert')
            cc1, cc2 = cc.split('.')
            self.ccolumn = cc2
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.151:setCommentColumn
        #@+node:ekr.20050724075352.152:indentToCommentColumn
        def indentToCommentColumn (self,event):
        
            tbuffer = event.widget
            i = tbuffer.index('insert lineend')
            i1, i2 = i.split('.')
            i2 = int(i2)
            c1 = int(self.ccolumn)
        
            if i2 < c1:
                wsn = c1- i2
                tbuffer.insert('insert lineend',' '*wsn)
            if i2 >= c1:
                tbuffer.insert('insert lineend',' ')
            tbuffer.mark_set('insert','insert lineend')
        
            return self.miniBuffer._tailEnd(tbuffer)
        #@-node:ekr.20050724075352.152:indentToCommentColumn
        #@-node:ekr.20050724075352.150:comment column methods
        #@+node:ekr.20050724075352.253:deleteSpaces
        def deleteSpaces (self,event,insertspace=False):
        
            tbuffer = event.widget
            char = tbuffer.get('insert','insert + 1c ')
        
            if char.isspace():
                i = tbuffer.index('insert')
                wf = tbuffer.search(r'\w',i,stopindex='%s lineend' % i,regexp=True)
                wb = tbuffer.search(r'\w',i,stopindex='%s linestart' % i,regexp=True,backwards=True)
                if '' in (wf,wb):
                    return 'break'
                tbuffer.delete('%s +1c' % wb,wf)
                if insertspace:
                    tbuffer.insert('insert',' ')
        
            return self.miniBuffer._tailEnd(tbuffer)
        
        #@-node:ekr.20050724075352.253:deleteSpaces
        #@+node:ekr.20050724075352.72:exchangePointMark
        def exchangePointMark (self,event):
        
            if not self._chckSel(event): return
            tbuffer = event.widget
            s1 = tbuffer.index('sel.first')
            s2 = tbuffer.index('sel.last')
            i = tbuffer.index('insert')
        
            if i == s1:
                tbuffer.mark_set('insert',s2)
            else:
                tbuffer.mark_set('insert',s1)
        
            return self.miniBuffer._tailEnd(tbuffer)
        #@nonl
        #@-node:ekr.20050724075352.72:exchangePointMark
        #@+node:ekr.20050727104740.1:forwardSentence
        def forwardSentence (self,event,way):
        
            tbuffer = event.widget
        
            i = tbuffer.search('.','insert',stopindex='end')
            if i:
                tbuffer.mark_set('insert','%s +1c' % i)
            else:
                tbuffer.mark_set('insert','end')
        
            return self.miniBuffer._tailEnd(tbuffer)
        #@-node:ekr.20050727104740.1:forwardSentence
        #@+node:ekr.20050724075352.65:insertNewLine
        def insertNewLine (self,event):
        
            tbuffer = event.widget
            i = tbuffer.index('insert')
            tbuffer.insert('insert','\n')
            tbuffer.mark_set('insert',i)
            return self.miniBuffer._tailEnd(tbuffer)
        
        insertNewline = insertNewLine
        #@-node:ekr.20050724075352.65:insertNewLine
        #@+node:ekr.20050724075352.59:insertParentheses
        def insertParentheses (self,event):
        
            tbuffer = event.widget
            tbuffer.insert('insert','()')
            tbuffer.mark_set('insert','insert -1c')
            return self.miniBuffer._tailEnd(tbuffer)
        #@-node:ekr.20050724075352.59:insertParentheses
        #@+node:ekr.20050724075352.76:movePastClose
        def movePastClose (self,event):
        
            tbuffer = event.widget
            i = tbuffer.search('(','insert',backwards=True,stopindex='1.0')
            icheck = tbuffer.search(')','insert',backwards=True,stopindex='1.0')
        
            if '' == i:
                return 'break'
            if icheck:
                ic = tbuffer.compare(i,'<',icheck)
                if ic:
                    return 'break'
            i2 = tbuffer.search(')','insert',stopindex='end')
            i2check = tbuffer.search('(','insert',stopindex='end')
            if '' == i2:
                return 'break'
            if i2check:
                ic2 = tbuffer.compare(i2,'>',i2check)
                if ic2:
                    return 'break'
            ib = tbuffer.index('insert')
            tbuffer.mark_set('insert','%s lineend +1c' % i2)
            if tbuffer.index('insert') == tbuffer.index('%s lineend' % ib):
                tbuffer.insert('insert','\n')
        
            return self.miniBuffer._tailEnd(tbuffer)
        #@nonl
        #@-node:ekr.20050724075352.76:movePastClose
        #@+node:ekr.20050724075352.70:removeBlankLines
        def removeBlankLines( self, event ):
            tbuffer = event.widget
            i = tbuffer.index( 'insert' )
            i1, i2 = i.split( '.' )
            i1 = int( i1 )
            dindex = []
            if tbuffer.get( 'insert linestart', 'insert lineend' ).strip() == '':
                while 1:
                    if str( i1 )+ '.0'  == '1.0' :
                        break 
                    i1 = i1 - 1
                    txt = tbuffer.get( '%s.0' % i1, '%s.0 lineend' % i1 )
                    txt = txt.strip()
                    if len( txt ) == 0:
                        dindex.append( '%s.0' % i1)
                        dindex.append( '%s.0 lineend' % i1 )
                    elif dindex:
                        tbuffer.delete( '%s-1c' % dindex[ -2 ], dindex[ 1 ] )
                        tbuffer.event_generate( '<Key>' )
                        tbuffer.update_idletasks()
                        break
                    else:
                        break
            i = tbuffer.index( 'insert' )
            i1, i2 = i.split( '.' )
            i1 = int( i1 )
            dindex = []
            while 1:
                if tbuffer.index( '%s.0 lineend' % i1 ) == tbuffer.index( 'end' ):
                    break
                i1 = i1 + 1
                txt = tbuffer.get( '%s.0' % i1, '%s.0 lineend' % i1 )
                txt = txt.strip() 
                if len( txt ) == 0:
                    dindex.append( '%s.0' % i1 )
                    dindex.append( '%s.0 lineend' % i1 )
                elif dindex:
                    tbuffer.delete( '%s-1c' % dindex[ 0 ], dindex[ -1 ] )
                    tbuffer.event_generate( '<Key>' )
                    tbuffer.update_idletasks()
                    break
                else:
                    break
        #@nonl
        #@-node:ekr.20050724075352.70:removeBlankLines
        #@+node:ekr.20050724075352.78:selectAll
        def selectAll( event ):
        
            event.widget.tag_add( 'sel', '1.0', 'end' )
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.78:selectAll
        #@+node:ekr.20050724075352.301:Goto
        def Goto (self,event):
        
            b = self.miniBuffer ; tbuffer = event.widget
        
            if event.keysym == 'Return':
                i = b.get()
                b.reset()
                state = b.getState('goto')
                b.setState('goto',0)
                if i.isdigit():
                    if state == 1:
                        widget.mark_set('insert','%s.0' % i)
                    elif state == 2:
                        widget.mark_set('insert','1.0 +%sc' % i)
                    widget.event_generate('<Key>')
                    widget.update_idletasks()
                    widget.see('insert')
            else:
                b.update(event)
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.301:Goto
        #@-node:ekr.20050727100634:New Entry points
        #@+node:ekr.20050727102142:Used by neg argss
        #@+node:ekr.20050724075352.69:changePreviousWord
        def changePreviousWord (self,event,stroke):
        
            tbuffer = event.widget
            i = tbuffer.index('insert')
        
            self.moveword(event,-1)
            if stroke == '<Alt-c>':
                self.capitalize(event,'cap')
            elif stroke == '<Alt-u>':
                 self.capitalize(event,'up')
            elif stroke == '<Alt-l>':
                self.capitalize(event,'low')
            tbuffer.mark_set('insert',i)
            self.stopControlX(event)
        
            return self.miniBuffer._tailEnd(tbuffer)
        #@-node:ekr.20050724075352.69:changePreviousWord
        #@-node:ekr.20050727102142:Used by neg argss
        #@+node:ekr.20050727152153.4:Utilities
            
        #@nonl
        #@+node:ekr.20050724075352.88:measure
        def measure( self, tbuffer ):
            i = tbuffer.index( 'insert' )
            i1, i2 = i.split( '.' )
            start = int( i1 )
            watch = 0
            ustart = start
            pone = 1
            top = i
            bottom = i
            while pone:
                ustart = ustart - 1
                if ustart < 0:
                    break
                ds = '%s.0' % ustart
                pone = tbuffer.dlineinfo( ds )
                if pone:
                    top = ds
                    watch = watch  + 1
            
            pone = 1
            ustart = start
            while pone:
                ustart = ustart +1
                ds = '%s.0' % ustart
                pone = tbuffer.dlineinfo( ds )
                if pone:
                    bottom = ds
                    watch = watch + 1
                    
            return watch , top, bottom
        #@nonl
        #@-node:ekr.20050724075352.88:measure
        #@+node:ekr.20050724075352.55:moveTo
        def moveTo( self, event, spot ):
            tbuffer = event.widget
            tbuffer.mark_set( Tk.INSERT, spot )
            tbuffer.see( spot )
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.55:moveTo
        #@+node:ekr.20050724075352.56:moveword (used by many entires)  TO DO: split into forward/backward versions
        def moveword( self, event, way  ):
            
            '''This function moves the cursor to the next word, direction dependent on the way parameter'''
            
            tbuffer = event.widget
            ind = tbuffer.index( 'insert' )
        
            if way == 1:
                 ind = tbuffer.search( '\w', 'insert', stopindex = 'end', regexp=True )
                 if ind:
                    nind = '%s wordend' % ind
                 else:
                    nind = 'end'
            else:
                 ind = tbuffer.search( '\w', 'insert -1c', stopindex= '1.0', regexp = True, backwards = True )
                 if ind:
                    nind = '%s wordstart' % ind 
                 else:
                    nind = '1.0'
            tbuffer.mark_set( 'insert', nind )
            tbuffer.see( 'insert' )
            tbuffer.event_generate( '<Key>' )
            tbuffer.update_idletasks()
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.56:moveword (used by many entires)  TO DO: split into forward/backward versions
        #@-node:ekr.20050727152153.4:Utilities
        #@-others
    #@nonl
    #@-node:ekr.20050724075352.54:class editCommandsClass
    #@+node:ekr.20050727152153.5:class emacsControlCommandsClass
    class emacsControlCommandsClass (baseCommandsClass):
        
        #@    @+others
        #@+node:ekr.20050727152914: ctor
        def __init__ (self,emacs):
        
            Emacs.baseCommandsClass.__init__(self,emacs) # init the base class.
            
            self.shutdownhook = None # If this is set via setShutdownHook, it is executed instead of sys.exit on Control-x Control-c.
            self.shuttingdown = False # Indicates that the Emacs instance is shutting down and no work needs to be done.
        #@nonl
        #@-node:ekr.20050727152914: ctor
        #@+node:ekr.20050727153020: getPublicCommands
        def getPublicCommands (self):
            
            b = self.miniBuffer
        
            return {
                'advertised-undo':              lambda event: self.doUndo( event ) and b.keyboardQuit( event ),
                'iconfify-or-deiconify-frame':  lambda event: self.suspend( event ) and b.keyboardQuit( event ),
                'keyboard-quit':                b.keyboardQuit,
                'save-buffers-kill-emacs':      lambda event: b.keyboardQuit( event ) and self.shutdown( event ),
                'shell-command':                self.startSubprocess,
                'shell-command-on-region':      lambda event: self.startSubprocess( event, which=1 ),
                
                # Added by ekr.
                'suspend':                      lambda event: self.suspend( event ) and b.keyboardQuit( event ),
            }
        #@nonl
        #@-node:ekr.20050727153020: getPublicCommands
        #@+node:ekr.20050724075352.79:suspend
        def suspend( self, event ):
            
            widget = event.widget
            widget.winfo_toplevel().iconify()
        #@nonl
        #@-node:ekr.20050724075352.79:suspend
        #@+node:ekr.20050724075352.94:shutdown methods
        #@+node:ekr.20050724075352.95:shutdown
        def shutdown( self, event ):
            
            self.shuttingdown = True
        
            if self.shutdownhook:
                self.shutdownhook()
            else:
                sys.exit( 0 )
        #@nonl
        #@-node:ekr.20050724075352.95:shutdown
        #@+node:ekr.20050724075352.96:setShutdownHook
        def setShutdownHook( self, hook ):
                
            self.shutdownhook = hook
        #@nonl
        #@-node:ekr.20050724075352.96:setShutdownHook
        #@-node:ekr.20050724075352.94:shutdown methods
        #@+node:ekr.20050724075352.316:subprocess
        #@+node:ekr.20050724075352.317:startSubprocess
        def startSubprocess (self,event,which=0):
        
            b = self.miniBuffer ; tbuffer = event.widget
            statecontents = {'state': 'start', 'payload': None}
            b.setState('subprocess',statecontents)
            if which:
                b.set("Shell command on region:")
                is1 = is2 = None
                try:
                    is1 = tbuffer.index('sel.first')
                    is2 = tbuffer.index('sel.last')
                finally:
                    if is1:
                        ### Does nothing
                        statecontents ['payload'] = tbuffer.get(is1,is2)
                        ### ??? b.setState('subprocess',statecontents)
                    else:
                        return b.keyboardQuit(event)
            else:
                b.set("Alt - !:")
        
            self.setLabelBlue()
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.317:startSubprocess
        #@+node:ekr.20050724075352.318:subprocess
        def subprocesser (self,event):
        
            b = self.miniBuffer
            state = b.getState('subprocess')
        
            if state ['state'] == 'start':
                state ['state'] = 'watching'
                b.set('')
        
            if event.keysym == "Return":
                cmdline = b.get()
                return self.executeSubprocess(event,cmdline,input=state['payload'])
            else:
                b.update(event)
                return 'break'
        #@nonl
        #@-node:ekr.20050724075352.318:subprocess
        #@+node:ekr.20050724075352.319:executeSubprocess
        def executeSubprocess (self,event,command,input=None):
            import subprocess
            b = self.miniBuffer
            try:
                try:
                    out, err = os.tmpnam(), os.tmpnam()
                    ofile = open(out,'wt+')
                    efile = open(err,'wt+')
                    process = subprocess.Popen(command,bufsize=-1,
                        stdout = ofile.fileno(), stderr = ofile.fileno(),
                        stdin = subprocess.PIPE, shell = True)
                    if input:
                        process.communicate(input)
                    process.wait()
                    tbuffer = event.widget
                    efile.seek(0)
                    errinfo = efile.read()
                    if errinfo:
                        tbuffer.insert('insert',errinfo)
                    ofile.seek(0)
                    okout = ofile.read()
                    if okout:
                        tbuffer.insert('insert',okout)
                except Exception, x:
                    tbuffer = event.widget
                    tbuffer.insert('insert',x)
            finally:
                os.remove(out)
                os.remove(err)
            b.keyboardQuit(event)
        
            return self.miniBuffer._tailEnd(tbuffer)
        #@nonl
        #@-node:ekr.20050724075352.319:executeSubprocess
        #@-node:ekr.20050724075352.316:subprocess
        #@-others
    #@nonl
    #@-node:ekr.20050727152153.5:class emacsControlCommandsClass
    #@+node:ekr.20050727155227:class fileCommandsClass
    class fileCommandsClass (baseCommandsClass):
        
        '''A class to load files into buffers and save buffers to files.'''
        
        #@    @+others
        #@+node:ekr.20050727155340: ctor
        def __init__ (self,emacs):
        
            Emacs.baseCommandsClass.__init__(self,emacs) # init the base class.
        #@nonl
        #@-node:ekr.20050727155340: ctor
        #@+node:ekr.20050727155451: getPublicCommands
        def getPublicCommands (self):
            
            b = self.miniBuffer
        
            return {
                'delete-file':      self.deleteFile,
                'diff':             self.diff, 
                'insert-file':      lambda event: self.insertFile( event ) and b.keyboardQuit( event ),
                'make-directory':   self.makeDirectory,
                'remove-directory': self.removeDirectory,
                'save-file':        self.saveFile
            }
        #@nonl
        #@-node:ekr.20050727155451: getPublicCommands
        #@+node:ekr.20050724075352.306:deleteFile
        def deleteFile (self,event):
        
            b = self.miniBuffer
            state = b.getState('delete_file')
        
            if state == 0:
                b.setState('delete_file',1)
                b.setLabelBlue()
                directory = os.getcwd()
                b.set('%s%s' % (directory,os.sep))
            elif event.keysym == 'Return':
                dfile = b.get()
                b.keyboardQuit(event)
                try:
                    os.remove(dfile)
                except:
                    b.set("Could not delete %s%" % dfile)
            else:
                b.update(event)
            
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.306:deleteFile
        #@+node:ekr.20050724075352.238:diff
        def diff( self, event ):
            
            '''the diff command, accessed by Alt-x diff.
            Creates a buffer and puts the diff between 2 files into it..'''
            
            b = self.miniBuffer ; tbuffer = event.widget
        
            try:
                f, name = self.getReadableTextFile()
                txt1 = f.read()
                f.close()
                
                f2, name2 = self.getReadableTextFile()
                txt2 = f2.read()
                f2.close()
            except:
                return b.keyboardQuit( event )
        
            self.switchToBuffer( event, "*diff* of ( %s , %s )" %( name, name2 ) )
            data = difflib.ndiff( txt1, txt2 )
            idata = []
            for z in data:
                idata.append( z )
            tbuffer.delete( '1.0', 'end' )
            tbuffer.insert( '1.0', ''.join( idata ) )
            b._tailEnd( tbuffer )
        
            return b.keyboardQuit( event )
        #@nonl
        #@-node:ekr.20050724075352.238:diff
        #@+node:ekr.20050724075352.309:getReadableFile
        def getReadableTextFile( self ):
            
            fname = tkFileDialog.askopenfilename()
            if fname == None: return None, None
            f = open( fname, 'rt' )
            return f, fname
        #@nonl
        #@-node:ekr.20050724075352.309:getReadableFile
        #@+node:ekr.20050724075352.307:insertFile
        def insertFile (self,event):
        
            tbuffer = event.widget
            f, name = self.getReadableTextFile()
            if not f: return None
            txt = f.read()
            f.close()
            tbuffer.insert('insert',txt)
        
            return self.miniBuffer._tailEnd(tbuffer)
        #@nonl
        #@-node:ekr.20050724075352.307:insertFile
        #@+node:ekr.20050724075352.303:makeDirectory
        def makeDirectory (self,event):
        
            b = self.miniBuffer
            state = b.getState('make_directory')
        
            if state == 0:
                b.setState('make_directory',1)
                b.setLabelBlue()
                directory = os.getcwd()
                b.set('%s%s' % (directory,os.sep))
                return 'break'
        
            if event.keysym == 'Return':
                ndirectory = b.get()
                b.keyboardQuit(event)
                try:
                    os.mkdir(ndirectory)
                except:
                    b.set("Could not make %s%" % ndirectory)
                return 'break'
            else:
                b.update(event)
                return 'break'
        #@nonl
        #@-node:ekr.20050724075352.303:makeDirectory
        #@+node:ekr.20050724075352.304:removeDirectory
        def removeDirectory (self,event):
        
            b = self.miniBuffer
            state = b.getState('remove_directory')
        
            if not state:
                b.setState('remove_directory',True)
                b.setLabelBlue()
                directory = os.getcwd()
                b.set('%s%s' % (directory,os.sep))
                return 'break'
        
            if event.keysym == 'Return':
                ndirectory = b.get()
                b.keyboardQuit(event)
                try:
                    os.rmdir(ndirectory)
                except:
                    b.set("Could not remove %s%" % ndirectory)
                return 'break'
            else:
                b.update(event)
                return 'break'
        #@nonl
        #@-node:ekr.20050724075352.304:removeDirectory
        #@+node:ekr.20050724075352.308:saveFile
        def saveFile( self, event ):
            tbuffer = event.widget
            txt = tbuffer.get( '1.0', 'end' )
            f = tkFileDialog.asksaveasfile()
            if f == None : return None
            f.write( txt )
            f.close()
        #@nonl
        #@-node:ekr.20050724075352.308:saveFile
        #@-others
    #@nonl
    #@-node:ekr.20050727155227:class fileCommandsClass
    #@+node:ekr.20050728090026:class keyHandlerCommandsClass
    class keyHandlerCommandsClass (baseCommandsClass):
        
        '''User commands to access the keyHandler class.'''
        
        #@    @+others
        #@+node:ekr.20050728090026.1: ctor
        def __init__ (self,emacs):
        
            Emacs.baseCommandsClass.__init__(self,emacs) # init the base class.
        #@-node:ekr.20050728090026.1: ctor
        #@+node:ekr.20050728090827:getPublicCommands
        def getPublicCommands (self):
            
            return {
                'digit-argument':           self.miniBuffer.digitArgument,
                'repeat-complex-command':   self.miniBuffer.repeatComplexCommand,
                'universal-argument':       self.miniBuffer.universalArgument,
            }
        #@nonl
        #@-node:ekr.20050728090827:getPublicCommands
        #@-others
    #@nonl
    #@-node:ekr.20050728090026:class keyHandlerCommandsClass
    #@+node:ekr.20050724075352.161:class killBufferCommandsClass
    class killBufferCommandsClass (baseCommandsClass):
        
        '''A class to manage the kill buffer.'''
    
        #@    @+others
        #@+node:ekr.20050725115600: ctor
        def __init__ (self,emacs):
        
            Emacs.baseCommandsClass.__init__(self,emacs) # init the base class.
            
            if emacs.useGlobalKillbuffer:
                self.killbuffer = Emacs.global_killbuffer 
            else:
                self.killbuffer = []
                
            self.kbiterator = self.iterateKillBuffer()
            self.reset = False 
        #@-node:ekr.20050725115600: ctor
        #@+node:ekr.20050725121247:getPublicCommands
        def getPublicCommands (self):
            
            return {
                'backward-kill-sentence':   self.backwardKillSentence,
                'backward-kill-word':       self.backwardKillWord,
                'kill-line':                self.killLine,
                'kill-word':                self.killWord,
                'kill-sentence':            self.killSentence,
                'kill-region':              self.killRegion,
                'yank':                     self.yank,
                'yank-pop':                 self.yankPop,
            }
        #@nonl
        #@-node:ekr.20050725121247:getPublicCommands
        #@+node:ekr.20050725120303:Entry points
        # backwardKillParagraph is in paragraph class.
        
        def backwardKillSentence (self,event):
            return self.miniBuffer.keyboardQuit(event) and self._killSentence(event,back=True)
            
        def backwardKillWord (self,event):
            return self.deletelastWord(event) and self.miniBuffer.keyboardQuit(event)
            
        def killLine (self,event):
            self.kill(event,frm='insert',to='insert lineend') and self.miniBuffer.keyboardQuit(event)
            
        def killRegion (self,event):
            return self._killRegion(event,which='d') and self.miniBuffer.keyboardQuit(event)
            
        # killParagraph is in paragraph class.
        
        def killSentence (self,event):
            return self.killsentence(event) and self.miniBuffer.keyboardQuit(event)
            
        def killWord (self,event):
            return self.kill(event,frm='insert wordstart',to='insert wordend') and self.miniBuffer.keyboardQuit(event)
            
        def yank (self,event):
            return self.walkKB(event,frm='insert',which='c') and self.miniBuffer.keyboardQuit(event)
            
        def yankPop (self,event):
            return self.walkKB(event,frm="insert",which='a') and self.miniBuffer.keyboardQuit(event)
        #@nonl
        #@-node:ekr.20050725120303:Entry points
        #@+node:ekr.20050724075352.162:kill
        def kill( self, event, frm, to  ):
        
            tbuffer = event.widget
            text = tbuffer.get( frm, to )
            self.addToKillBuffer( text )
            tbuffer.clipboard_clear()
            tbuffer.clipboard_append( text )   
         
            if frm == 'insert' and to =='insert lineend' and tbuffer.index( frm ) == tbuffer.index( to ):
                tbuffer.delete( 'insert', 'insert lineend +1c' )
                self.addToKillBuffer( '\n' )
            else:
                tbuffer.delete( frm, to )
        
            return self.miniBuffer._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.162:kill
        #@+node:ekr.20050724075352.163:walkKB
        def walkKB( self, event, frm, which ):# kb = self.iterateKillBuffer() ):
        
            tbuffer = event.widget
            i = tbuffer.index( 'insert' )
            t , t1 = i.split( '.' )
            clip_text = self.getClipboard( tbuffer )    
            if self.killbuffer or clip_text:
                if which == 'c':
                    self.reset = True
                    if clip_text:
                        txt = clip_text
                    else:
                        txt = self.kbiterator.next()
                    tbuffer.tag_delete( 'kb' )
                    tbuffer.insert( frm, txt, ('kb') )
                    tbuffer.mark_set( 'insert', i )
                else:
                    if clip_text:
                        txt = clip_text
                    else:
                        txt = self.kbiterator.next()
                    t1 = str( int( t1 ) + len( txt ) )
                    r = tbuffer.tag_ranges( 'kb' )
                    if r and r[ 0 ] == i:
                        tbuffer.delete( r[ 0 ], r[ -1 ] )
                    tbuffer.tag_delete( 'kb' )
                    tbuffer.insert( frm, txt, ('kb') )
                    tbuffer.mark_set( 'insert', i )
            return self.miniBuffer._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.163:walkKB
        #@+node:ekr.20050724075352.164:deletelastWord
        def deletelastWord( self, event ):
            
            #tbuffer = event.widget
            #i = tbuffer.get( 'insert' )
            self.editCommands.moveword( event, -1 )
            self.kill( event, 'insert', 'insert wordend')
            self.editCommands.moveword( event ,1 )
            return 'break'
        #@-node:ekr.20050724075352.164:deletelastWord
        #@+node:ekr.20050724075352.165:_killSentence
        def killsentence( self, event, back = False ):
            tbuffer = event.widget
            i = tbuffer.search( '.' , 'insert', stopindex = 'end' )
            if back:
                i = tbuffer.search( '.' , 'insert', backwards = True, stopindex = '1.0' ) 
                if i == '':
                    return 'break'
                i2 = tbuffer.search( '.' , i, backwards = True , stopindex = '1.0' )
                if i2 == '':
                    i2 = '1.0'
                return self.kill( event, i2, '%s + 1c' % i )
                #return self.kill( event , '%s +1c' % i, 'insert' )
            else:
                i = tbuffer.search( '.' , 'insert', stopindex = 'end' )
                i2 = tbuffer.search( '.', 'insert', backwards = True, stopindex = '1.0' )
            if i2 == '':
               i2 = '1.0'
            else:
               i2 = i2 + ' + 1c '
            if i == '': return 'break'
            return self.kill( event, i2, '%s + 1c' % i )
        #@nonl
        #@-node:ekr.20050724075352.165:_killSentence
        #@+node:ekr.20050724075352.166:_killRegion
        def killRegion( self, event, which ):
            mrk = 'sel'
            tbuffer = event.widget
            trange = tbuffer.tag_ranges( mrk )
            if len( trange ) != 0:
                txt = tbuffer.get( trange[ 0 ] , trange[ -1 ] )
                if which == 'd':
                    tbuffer.delete( trange[ 0 ], trange[ -1 ] )   
                self.addToKillBuffer( txt )
                tbuffer.clipboard_clear()
                tbuffer.clipboard_append( txt )
            self.removeRKeys( tbuffer )
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.166:_killRegion
        #@+node:ekr.20050724075352.167:addToKillBuffer
        def addToKillBuffer( self, text ):
            
            self.reset = True 
            
            if (
                self.miniBuffer.previousStroke in (
                    '<Control-k>', '<Control-w>' ,
                    '<Alt-d>', '<Alt-Delete', '<Alt-z>', '<Delete>',
                    '<Control-Alt-w>' )
                and len(self.killbuffer)
            ):
                self.killbuffer[ 0 ] = self.killbuffer[ 0 ] + text
                return
        
            self.killbuffer.insert( 0, text )
        #@nonl
        #@-node:ekr.20050724075352.167:addToKillBuffer
        #@+node:ekr.20050724075352.168:iterateKillBuffer
        def iterateKillBuffer( self ):
            
            while 1:
                if self.killbuffer:
                    self.last_clipboard = None
                    for z in self.killbuffer:
                        if self.reset:
                            self.reset = False
                            break        
                        yield z
        #@-node:ekr.20050724075352.168:iterateKillBuffer
        #@+node:ekr.20050724075352.169:getClipboard
        def getClipboard (self,tbuffer):
            
            ctxt = None 
            
            try:
                ctxt = tbuffer.selection_get(selection='CLIPBOARD')
                if ctxt!=self.last_clipboard or not self.killbuffer:
                    self.last_clipboard = ctxt 
                    if self.killbuffer and self.killbuffer[0]==ctxt:
                        return None 
                    return ctxt 
                else:
                    return None 
                
            except:
                return None 
                
            return None 
        #@-node:ekr.20050724075352.169:getClipboard
        #@-others
    #@nonl
    #@-node:ekr.20050724075352.161:class killBufferCommandsClass
    #@+node:ekr.20050727164709:class leoCommandsClass
    class leoCommandsClass (baseCommandsClass):
        
        #@    @+others
        #@+node:ekr.20050727164724: ctor
        def __init__ (self,emacs):
        
            Emacs.baseCommandsClass.__init__(self,emacs) # init the base class.
        #@nonl
        #@-node:ekr.20050727164724: ctor
        #@+node:ekr.20050727165133:getPublicCommands
        def getPublicCommands (self):
            
            leoCommandsDict = {}
            
            #@    << define dictionary d of names and Leo commands >>
            #@+node:ekr.20050728111312:<< define dictionary d of names and Leo commands >>
            c = self.c ; f = c.frame
            
            d = {
                'new':                  c.new,
                'open':                 c.open,
                'openWith':             c.openWith,
                'close':                c.close,
                'save':                 c.save,
                'saveAs':               c.saveAs,
                'saveTo':               c.saveTo,
                'revert':               c.revert,
                'readOutlineOnly':      c.readOutlineOnly,
                'readAtFileNodes':      c.readAtFileNodes,
                'importDerivedFile':    c.importDerivedFile,
                #'writeNewDerivedFiles': c.writeNewDerivedFiles,
                #'writeOldDerivedFiles': c.writeOldDerivedFiles,
                'tangle':               c.tangle,
                'tangle all':           c.tangleAll,
                'tangle marked':        c.tangleMarked,
                'untangle':             c.untangle,
                'untangle all':         c.untangleAll,
                'untangle marked':      c.untangleMarked,
                'export headlines':     c.exportHeadlines,
                'flatten outline':      c.flattenOutline,
                'import AtRoot':        c.importAtRoot,
                'import AtFile':        c.importAtFile,
                'import CWEB Files':    c.importCWEBFiles,
                'import Flattened Outline': c.importFlattenedOutline,
                'import Noweb Files':   c.importNowebFiles,
                'outline to Noweb':     c.outlineToNoweb,
                'outline to CWEB':      c.outlineToCWEB,
                'remove sentinels':     c.removeSentinels,
                'weave':                c.weave,
                'delete':               c.delete,
                'execute script':       c.executeScript,
                'go to line number':    c.goToLineNumber,
                'set font':             c.fontPanel,
                'set colors':           c.colorPanel,
                'show invisibles':      c.viewAllCharacters,
                'preferences':          c.preferences,
                'convert all blanks':   c.convertAllBlanks,
                'convert all tabs':     c.convertAllTabs,
                'convert blanks':       c.convertBlanks,
                'convert tabs':         c.convertTabs,
                'indent':               c.indentBody,
                'unindent':             c.dedentBody,
                'reformat paragraph':   c.reformatParagraph,
                'insert time':          c.insertBodyTime,
                'extract section':      c.extractSection,
                'extract names':        c.extractSectionNames,
                'extract':              c.extract,
                'match bracket':        c.findMatchingBracket,
                'find panel':           c.showFindPanel, ## c.findPanel,
                'find next':            c.findNext,
                'find previous':        c.findPrevious,
                'replace':              c.replace,
                'replace then find':    c.replaceThenFind,
                'edit headline':        c.editHeadline,
                'toggle angle brackets': c.toggleAngleBrackets,
                'cut node':             c.cutOutline,
                'copy node':            c.copyOutline,
                'paste node':           c.pasteOutline,
                'paste retaining clone': c.pasteOutlineRetainingClones,
                'hoist':                c.hoist,
                'de-hoist':             c.dehoist,
                'insert node':          c.insertHeadline,
                'clone node':           c.clone,
                'delete node':          c.deleteOutline,
                'sort children':        c.sortChildren,
                'sort siblings':        c.sortSiblings,
                'demote':               c.demote,
                'promote':              c.promote,
                'move right':           c.moveOutlineRight,
                'move left':            c.moveOutlineLeft,
                'move up':              c.moveOutlineUp,
                'move down':            c.moveOutlineDown,
                'unmark all':           c.unmarkAll,
                'mark clones':          c.markClones,
                'mark':                 c.markHeadline,
                'mark subheads':        c.markSubheads,
                'mark changed items':   c.markChangedHeadlines,
                'mark changed roots':   c.markChangedRoots,
                'contract all':         c.contractAllHeadlines,
                'contract node':        c.contractNode,
                'contract parent':      c.contractParent,
                'expand to level 1':    c.expandLevel1,
                'expand to level 2':    c.expandLevel2,
                'expand to level 3':    c.expandLevel3,
                'expand to level 4':    c.expandLevel4,
                'expand to level 5':    c.expandLevel5,
                'expand to level 6':    c.expandLevel6,
                'expand to level 7':    c.expandLevel7,
                'expand to level 8':    c.expandLevel8,
                'expand to level 9':    c.expandLevel9,
                'expand prev level':    c.expandPrevLevel,
                'expand next level':    c.expandNextLevel,
                'expand all':           c.expandAllHeadlines,
                'expand node':          c.expandNode,
                'check outline':        c.checkOutline,
                'dump outline':         c.dumpOutline,
                'check python code':    c.checkPythonCode,
                'check all python code': c.checkAllPythonCode,
                'pretty print python code': c.prettyPrintPythonCode,
                'pretty print all python code': c.prettyPrintAllPythonCode,
                'goto parent':          c.goToParent,
                'goto next sibling':    c.goToNextSibling,
                'goto previous sibling': c.goToPrevSibling,
                'goto next clone':      c.goToNextClone,
                'goto next marked':     c.goToNextMarkedHeadline,
                'goto next changed':    c.goToNextDirtyHeadline,
                'goto first':           c.goToFirstNode,
                'goto last':            c.goToLastNode,
                "go to prev visible":   c.selectVisBack,
                "go to next visible":   c.selectVisNext,
                "go to prev node":      c.selectThreadBack,
                "go to next node":      c.selectThreadNext,
                'about leo...':         c.about,
                #'apply settings':      c.applyConfig,
                'open LeoConfig.leo':   c.leoConfig,
                'open LeoDocs.leo':     c.leoDocumentation,
                'open online home':     c.leoHome,
                'open online tutorial': c.leoTutorial,
                'open compare window':  c.openCompareWindow,
                'open Python window':   c.openPythonWindow,
                "equal sized panes":    f.equalSizedPanes,
                "toggle active pane":   f.toggleActivePane,
                "toggle split direction": f.toggleSplitDirection,
                "resize to screen":     f.resizeToScreen,
                "cascade":              f.cascade,
                "minimize all":         f.minimizeAll,
            }
            #@nonl
            #@-node:ekr.20050728111312:<< define dictionary d of names and Leo commands >>
            #@nl
            
            # Create a callback for each item in d.
            for key in d.keys():
                f = d.get(key)
                def leoCallback (event,f=f):
                    f()
                leoCommandsDict [key] = leoCallback
                ### To do: not all these keys are valid Python function names.
                setattr(self,key,f) # Make the key available.
                
            return leoCommandsDict
        #@nonl
        #@-node:ekr.20050727165133:getPublicCommands
        #@-others
    #@nonl
    #@-node:ekr.20050727164709:class leoCommandsClass
    #@+node:ekr.20050724075352.137:class macroCommandsClass
    class macroCommandsClass (baseCommandsClass):
    
        #@    @+others
        #@+node:ekr.20050727084241: ctor
        def __init__ (self,emacs):
            
            Emacs.baseCommandsClass.__init__(self,emacs) # init the base class.
        
            self.lastMacro = None 
            self.macs =[]
            self.macro =[]
            self.namedMacros ={}
            self.macroing = False
        #@nonl
        #@-node:ekr.20050727084241: ctor
        #@+node:ekr.20050727085306: getPublicCommands
        def getPublicCommands (self):
        
            return {
                'name-last-kbd-macro':      self.nameLastMacro,
                'load-file':                self.loadMacros,
                'insert-keyboard-macro' :   self.getMacroName,
            }
        #@nonl
        #@-node:ekr.20050727085306: getPublicCommands
        #@+node:ekr.20050727085306.1:Entry points
        #@+node:ekr.20050724075352.147:getMacroName (calls saveMacros)
        def getMacroName (self,event):
        
            '''A method to save your macros to file.'''
        
            b = self.miniBuffer
        
            if not self.macroing:
                self.macroing = 3
                b.set('')
                b.setLabelBlue()
            elif event.keysym == 'Return':
                self.macroing = False
                self.saveMacros(event,b.get())
            elif event.keysym == 'Tab':
                b.set(self._findMatch(self.namedMacros))
            else:
                b.update(event)
        
            return 'break'
        #@+node:ekr.20050724075352.93:_findMatch
        def _findMatch (self,fdict=None):
        
            '''This method finds the first match it can find in a sorted list'''
        
            b = self.miniBuffer
        
            if not fdict:
                fdict = self.miniBuffer.altX_commandsDict
        
            s = b.get()
            pmatches = filter(lambda a: a.startswith(s),fdict)
            pmatches.sort()
            if pmatches:
                mstring = reduce(self.findPre,pmatches)
                return mstring
        
            return s
        
        #@-node:ekr.20050724075352.93:_findMatch
        #@-node:ekr.20050724075352.147:getMacroName (calls saveMacros)
        #@+node:ekr.20050724075352.145:loadMacros & helpers
        def loadMacros (self,event):
        
            '''Asks for a macro file name to load.'''
        
            f = tkFileDialog.askopenfile()
        
            if f:
                return self._loadMacros(f)
            else:
                return 'break'
        #@nonl
        #@+node:ekr.20050724075352.146:_loadMacros
        def _loadMacros( self, f ):
        
            '''Loads a macro file into the macros dictionary.'''
        
            macros = cPickle.load( f )
            for z in macros:
                self.miniBuffer.addToDoAltX( z, macros[ z ] )
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.146:_loadMacros
        #@-node:ekr.20050724075352.145:loadMacros & helpers
        #@+node:ekr.20050724075352.143:nameLastMacro
        def nameLastMacro (self,event):
        
            '''Names the last macro defined.'''
        
            b = self.miniBuffer
        
            if not self.macroing:
                self.macroing = 2
                b.set('')
                b.setLabelBlue()
            elif event.keysym == 'Return':
                name = b.get()
                b.addToDoAltX(name,self.lastMacro)
                b.set('')
                b.setLabelBlue()
                self.macroing = False
                b.stopControlX(event)
            else:
                b.update(event)
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.143:nameLastMacro
        #@+node:ekr.20050724075352.148:saveMacros & helper
        def saveMacros( self, event, macname ):
            
            '''Asks for a file name and saves it.'''
        
            name = tkFileDialog.asksaveasfilename()
            if name:
                f = file( name, 'a+' )
                f.seek( 0 )
                if f:
                    self._saveMacros( f, macname )
        
            return 'break'
        #@nonl
        #@+node:ekr.20050724075352.149:_saveMacros
        def _saveMacros( self, f , name ):
            '''Saves the macros as a pickled dictionary'''
            import cPickle
            fname = f.name
            try:
                macs = cPickle.load( f )
            except:
                macs = {}
            f.close()
            if self.namedMacros.has_key( name ):
                macs[ name ] = self.namedMacros[ name ]
                f = file( fname, 'w' )
                cPickle.dump( macs, f )
                f.close()
        #@nonl
        #@-node:ekr.20050724075352.149:_saveMacros
        #@-node:ekr.20050724075352.148:saveMacros & helper
        #@-node:ekr.20050727085306.1:Entry points
        #@+node:ekr.20050727085306.2:Called from keystroke handlers
        #@+node:ekr.20050724075352.142:executeLastMacro & helper (called from universal command)
        def executeLastMacro( self, event ):
        
            tbuffer = event.widget
            if self.lastMacro:
                return self._executeMacro( self.lastMacro, tbuffer )
            return 'break'
        #@nonl
        #@+node:ekr.20050724075352.141:_executeMacro
        def _executeMacro( self, macro, tbuffer ):
            
            for z in macro:
                if len( z ) == 2:
                    tbuffer.event_generate( '<Key>', keycode = z[ 0 ], keysym = z[ 1 ] ) 
                else:
                    meth = z[ 0 ].lstrip( '<' ).rstrip( '>' )
                    method = self.cbDict[ meth ]
                    ev = Tk.Event()
                    ev.widget = tbuffer
                    ev.keycode = z[ 1 ]
                    ev.keysym = z[ 2 ]
                    ev.char = z[ 3 ]
                    self.masterCommand( ev , method, '<%s>' % meth )
        
            return self.miniBuffer._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.141:_executeMacro
        #@-node:ekr.20050724075352.142:executeLastMacro & helper (called from universal command)
        #@+node:ekr.20050724075352.138:startKBDMacro
        def startKBDMacro( self, event ):
        
            b = self.miniBuffer
        
            b.set( 'Recording Keyboard Macro' )
            b.setLabelBlue()
            self.macroing = True
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.138:startKBDMacro
        #@+node:ekr.20050724075352.139:recordKBDMacro
        def recordKBDMacro( self, event, stroke ):
            if stroke != '<Key>':
                self.macro.append( (stroke, event.keycode, event.keysym, event.char) )
            elif stroke == '<Key>':
                if event.keysym != '??':
                    self.macro.append( ( event.keycode, event.keysym ) )
            return
        #@nonl
        #@-node:ekr.20050724075352.139:recordKBDMacro
        #@+node:ekr.20050724075352.140:stopKBDMacro
        def stopKBDMacro (self,event):
        
            b = self.miniBuffer
        
            if self.macro:
                self.macro = self.macro [: -4]
                self.macs.insert(0,self.macro)
                self.lastMacro = self.macro
                self.macro = []
        
            self.macroing = False
            b.set('Keyboard macro defined')
            b.setLabelBlue()
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.140:stopKBDMacro
        #@-node:ekr.20050727085306.2:Called from keystroke handlers
        #@-others
    #@nonl
    #@-node:ekr.20050724075352.137:class macroCommandsClass
    #@+node:ekr.20050724075352.254:class queryReplaceCommandsClass
    class queryReplaceCommandsClass (baseCommandsClass):
        
        '''A class to handle query replace commands.'''
    
        #@    @+others
        #@+node:ekr.20050727085936: ctor
        def __init__ (self,emacs):
            
            Emacs.baseCommandsClass.__init__(self,emacs) # init the base class.
            
        #@nonl
        #@-node:ekr.20050727085936: ctor
        #@+node:ekr.20050727090028: getPublicCommands
        def getPublicCommands (self):
        
            return {
                'query-replace':                self.queryReplace,
                'query-replace-regex':          self.queryReplaceRegex,
                'inverse-add-global-abbrev':    self.inverseAddGlobalAbbrev,
            }
        #@nonl
        #@-node:ekr.20050727090028: getPublicCommands
        #@+node:ekr.20050727090504:Entry points
        def queryReplace (self,event):
            return self.masterQR(event)
        
        def queryReplaceRegex (self,event):
            return self.startRegexReplace() and self.masterQR(event)
        
        def inverseAddGlobalAbbrev (self,event):
            return self.abbreviationDispatch(event,2)
        #@nonl
        #@-node:ekr.20050727090504:Entry points
        #@+node:ekr.20050724075352.255:qreplace
        def qreplace( self, event ):
        
            if event.keysym == 'y':
                self._qreplace( event )
                return
            elif event.keysym in ( 'q', 'Return' ):
                self.quitQSearch( event )
            elif event.keysym == 'exclam':
                while self.qrexecute:
                    self._qreplace( event )
            elif event.keysym in ( 'n', 'Delete'):
                #i = event.widget.index( 'insert' )
                event.widget.mark_set( 'insert', 'insert +%sc' % len( self.qQ ) )
                self.qsearch( event )
            event.widget.see( 'insert' )
        #@nonl
        #@-node:ekr.20050724075352.255:qreplace
        #@+node:ekr.20050724075352.256:_qreplace
        def _qreplace( self, event ):
            i = event.widget.tag_ranges( 'qR' )
            event.widget.delete( i[ 0 ], i[ 1 ] )
            event.widget.insert( 'insert', self.qR )
            self.qsearch( event )
        #@nonl
        #@-node:ekr.20050724075352.256:_qreplace
        #@+node:ekr.20050724075352.257:getQuery
        def getQuery (self,event):
        
            b = self.miniBuffer
        
            if event.keysym == 'Return':
                self.qgetQuery = False
                self.qgetReplace = True
                self.qQ = b.get()
                b.set("Replace with:")
                b.setState('qlisten','replace-caption')
                return
        
            if b.getState('qlisten') == 'replace-caption':
                b.set('')
                b.setState('qlisten',True)
        
            b.update(event)
        #@nonl
        #@-node:ekr.20050724075352.257:getQuery
        #@+node:ekr.20050724075352.258:getReplace
        def getReplace (self,event):
        
            b = self.miniBuffer ; tbuffer = event.widget
            prompt = 'Replace %s with %s y/n(! for all )'
        
            if event.keysym == 'Return':
                self.qgetReplace = False
                self.qR = b.get()
                self.qrexecute = True
                ok = self.qsearch(event)
                if self.querytype == 'regex' and ok:
                    range = tbuffer.tag_ranges('qR')
                    s = tbuffer.get(range[0],range[1])
                    b.set(prompt % (s,self.qR))
                elif ok:
                    b.set(prompt % (self.qQ,self.qR))
                return
        
            if b.getState('qlisten') == 'replace-caption':
                b.set('')
                b.setState('qlisten',True)
        
            b.update(event)
        #@nonl
        #@-node:ekr.20050724075352.258:getReplace
        #@+node:ekr.20050724075352.259:masterQR
        def masterQR (self,event):
        
            if self.qgetQuery:
                self.getQuery(event)
            elif self.qgetReplace:
                self.getReplace(event)
            elif self.qrexecute:
                self.qreplace(event)
            else:
                self.listenQR(event)
        
            return 'break'
        #@-node:ekr.20050724075352.259:masterQR
        #@+node:ekr.20050724075352.260:startRegexReplace
        def startRegexReplace( self ):
            
            self.querytype = 'regex'
            return True
        #@nonl
        #@-node:ekr.20050724075352.260:startRegexReplace
        #@+node:ekr.20050724075352.261:query search methods
        #@+others
        #@+node:ekr.20050724075352.262:listenQR
        def listenQR (self,event):
        
            b = self.miniBuffer
        
            b.setState('qlisten','replace-caption')
            b.setLabelBlue()
            b.set(
                g.choose(self.querytype=='regex',
                    'Regex Query with:'
                    'Query with:'))
        
            self.qgetQuery = True
        #@nonl
        #@-node:ekr.20050724075352.262:listenQR
        #@+node:ekr.20050724075352.263:qsearch
        def qsearch( self, event ):
            
            b = self.miniBuffer ; tbuffer = event.widget
            if self.qQ:
                tbuffer.tag_delete( 'qR' )
                if self.querytype == 'regex':
                    try:
                        regex = re.compile( self.qQ )
                    except:
                        b.keyboardQuit( event )
                        b.set( "Illegal regular expression" )
                        
                    txt = tbuffer.get( 'insert', 'end' )
                    match = regex.search( txt )
                    if match:
                        start = match.start()
                        end = match.end()
                        length = end - start
                        tbuffer.mark_set( 'insert', 'insert +%sc' % start )
                        tbuffer.update_idletasks()
                        tbuffer.tag_add( 'qR', 'insert', 'insert +%sc' % length )
                        tbuffer.tag_config( 'qR', background = 'lightblue' )
                        txt = tbuffer.get( 'insert', 'insert +%sc' % length )
                        b.set( "Replace %s with %s? y/n(! for all )" % ( txt, self.qR ) )
                        return True
                else:
                    i = tbuffer.search( self.qQ, 'insert', stopindex = 'end' )
                    if i:
                        tbuffer.mark_set( 'insert', i )
                        tbuffer.update_idletasks()
                        tbuffer.tag_add( 'qR', 'insert', 'insert +%sc'% len( self.qQ ) )
                        tbuffer.tag_config( 'qR', background = 'lightblue' )
                        self.miniBuffer._tailEnd( tbuffer )
                        return True
                self.quitQSearch( event )
                return False
        #@-node:ekr.20050724075352.263:qsearch
        #@+node:ekr.20050724075352.264:quitQSearch
        def quitQSearch (self,event):
        
            b = self.miniBuffer ; tbuffer = event.widget
        
            tbuffer.tag_delete('qR')
            self.qQ = None
            self.qR = None
            b.setState('qlisten',0)
            self.qrexecute = False
            b.set('')
            b.setLabelGrey()
            self.querytype = 'normal'
            b._tailEnd(event.widget)
        #@nonl
        #@-node:ekr.20050724075352.264:quitQSearch
        #@-others
        #@nonl
        #@-node:ekr.20050724075352.261:query search methods
        #@-others
    #@nonl
    #@-node:ekr.20050724075352.254:class queryReplaceCommandsClass
    #@+node:ekr.20050724075352.265:class rectangleCommandsClass
    class rectangleCommandsClass (baseCommandsClass):
    
        #@    @+others
        #@+node:ekr.20050727091613: ctor
        def __init__ (self,emacs):
        
            Emacs.baseCommandsClass.__init__(self,emacs) # init the base class.
        
            self.sRect = False # State indicating string rectangle.  May be moved to stateManagerClass
            self.krectangle = None # The kill rectangle
            self.rectanglemode = 0 # Determines what state the rectangle system is in.
        #@nonl
        #@-node:ekr.20050727091613: ctor
        #@+node:ekr.20050727091421:getPublicCommands
        def getPublicCommands (self):
        
            return {
                'clear-rectangle':  self.clearRectangle,
                'close-rectangle':  self.closeRectangle,
                'delete-rectangle': self.deleteRectangle,
                'kill-rectangle':   self.killRectangle,
                'open-rectangle':   self.openRectangle,
                'yank-rectangle':   self.yankRectangle,
            }
        #@nonl
        #@-node:ekr.20050727091421:getPublicCommands
        #@+node:ekr.20050727091421.1:Entry points
        #@+node:ekr.20050724075352.268:clearRectangle
        def clearRectangle( self, event ):
            
            if not self._chckSel( event ):
                return
            tbuffer = event.widget
            r1, r2, r3, r4 = self.getRectanglePoints( event )
            lth = ' ' * ( r4 - r2 )
            self.stopControlX( event )
            while r1 <= r3:
                tbuffer.delete( '%s.%s' % ( r1, r2 ) , '%s.%s' % ( r1, r4 )  )
                tbuffer.insert( '%s.%s' % ( r1, r2 ) , lth)
                r1 = r1 + 1
        
            return self.miniBuffer._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.268:clearRectangle
        #@+node:ekr.20050724075352.272:closeRectangle
        def closeRectangle (self,event):
        
            if not self._chckSel(event): return
            tbuffer = event.widget
            r1, r2, r3, r4 = self.getRectanglePoints(event)
            ar1 = r1
            txt = []
            while ar1 <= r3:
                txt.append(tbuffer.get('%s.%s' % (ar1,r2),'%s.%s' % (ar1,r4)))
                ar1 = ar1 + 1
            for z in txt:
                if z.lstrip().rstrip():
                    return
            while r1 <= r3:
                tbuffer.delete('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
                r1 = r1 + 1
        
            return self.miniBuffer._tailEnd(tbuffer)
        #@nonl
        #@-node:ekr.20050724075352.272:closeRectangle
        #@+node:ekr.20050724075352.269:deleteRectangle
        def deleteRectangle (self,event):
        
            if not self._chckSel(event): return
            tbuffer = event.widget
            r1, r2, r3, r4 = self.getRectanglePoints(event)
            #lth = ' ' * ( r4 - r2 )
            self.stopControlX(event)
            while r1 <= r3:
                tbuffer.delete('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
                r1 = r1 + 1
        
            return self.miniBuffer._tailEnd(tbuffer)
        #@nonl
        #@-node:ekr.20050724075352.269:deleteRectangle
        #@+node:ekr.20050724075352.271:killRectangle
        def killRectangle (self,event):
        
            if not self._chckSel(event): return
            tbuffer = event.widget
            r1, r2, r3, r4 = self.getRectanglePoints(event)
        
            self.stopControlX(event)
            self.krectangle = []
            while r1 <= r3:
                txt = tbuffer.get('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
                self.krectangle.append(txt)
                tbuffer.delete('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
                r1 = r1 + 1
        
            return self.miniBuffer._tailEnd(tbuffer)
        #@nonl
        #@-node:ekr.20050724075352.271:killRectangle
        #@+node:ekr.20050724075352.273:yankRectangle
        def yankRectangle( self, event , krec = None ):
            self.stopControlX( event )
            if not krec:
                krec = self.krectangle
            if not krec:
                return 'break'
            tbuffer = event.widget
            txt = tbuffer.get( 'insert linestart', 'insert' )
            txt = self.getWSString( txt )
            i = tbuffer.index( 'insert' )
            i1, i2 = i.split( '.' )
            i1 = int( i1 )
            for z in krec:        
                txt2 = tbuffer.get( '%s.0 linestart' % i1, '%s.%s' % ( i1, i2 ) )
                if len( txt2 ) != len( txt ):
                    amount = len( txt ) - len( txt2 )
                    z = txt[ -amount : ] + z
                tbuffer.insert( '%s.%s' %( i1, i2 ) , z )
                if tbuffer.index( '%s.0 lineend +1c' % i1 ) == tbuffer.index( 'end' ):
                    tbuffer.insert( '%s.0 lineend' % i1, '\n' )
                i1 = i1 + 1
            return self.miniBuffer._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.273:yankRectangle
        #@+node:ekr.20050724075352.267:openRectangle
        def openRectangle( self, event ):
            if not self._chckSel( event ):
                return
            tbuffer = event.widget
            r1, r2, r3, r4 = self.getRectanglePoints( event )
            lth = ' ' * ( r4 - r2 )
            self.stopControlX( event )
            while r1 <= r3:
                tbuffer.insert( '%s.%s' % ( r1, r2 ) , lth)
                r1 = r1 + 1
            return self.miniBuffer._tailEnd( tbuffer )
        #@nonl
        #@-node:ekr.20050724075352.267:openRectangle
        #@-node:ekr.20050727091421.1:Entry points
        #@+node:ekr.20050724075352.266:activateRectangleMethods
        def activateRectangleMethods (self,event):
        
            b = self.miniBuffer
        
            self.rectanglemode = 1
            b.set('C - x r')
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.266:activateRectangleMethods
        #@+node:ekr.20050724075352.270:stringRectangle (called from processKey)
        def stringRectangle (self,event):
        
            b = self.miniBuffer ; tbuffer = event.widget
            if not self.sRect:
                self.sRect = 1
                b.set('String rectangle :')
                b.setLabelBlue()
                return 'break'
            if event.keysym == 'Return':
                self.sRect = 3
            if self.sRect == 1:
                b.set('')
                self.sRect = 2
            if self.sRect == 2:
                b.update(event)
                return 'break'
            if self.sRect == 3:
                if not self._chckSel(event):
                    b.stopControlX(event)
                    return
                r1, r2, r3, r4 = self.getRectanglePoints(event)
                lth = b.get()
                while r1 <= r3:
                    tbuffer.delete('%s.%s' % (r1,r2),'%s.%s' % (r1,r4))
                    tbuffer.insert('%s.%s' % (r1,r2),lth)
                    r1 = r1 + 1
                b.stopControlX(event)
                return b._tailEnd(tbuffer)
        #@nonl
        #@-node:ekr.20050724075352.270:stringRectangle (called from processKey)
        #@+node:ekr.20050724075352.274:getRectanglePoints
        def getRectanglePoints (self,event):
        
            tbuffer = event.widget
            i = tbuffer.index('sel.first')
            i2 = tbuffer.index('sel.last')
            r1, r2 = i.split('.')
            r3, r4 = i2.split('.')
            return int(r1), int(r2), int(r3), int(r4)
        #@nonl
        #@-node:ekr.20050724075352.274:getRectanglePoints
        #@-others
    #@nonl
    #@-node:ekr.20050724075352.265:class rectangleCommandsClass
    #@+node:ekr.20050724075352.170:class registerCommandsClass
    class registerCommandsClass (baseCommandsClass):
    
        '''A class to represent registers a-z and the corresponding Emacs commands.'''
    
        #@    @+others
        #@+node:ekr.20050725134243: ctor
        def __init__ (self,emacs):
            
            Emacs.baseCommandsClass.__init__(self,emacs) # init the base class.
        
            if emacs.useGlobalRegisters:
                self.registers = Emacs.global_registers 
            else:
                self.registers = {}
        
            self.method = None 
            self.methodDict, self.helpDict = self.addRegisterItems()
            
            self.registermode = False # For rectangles and registers
        #@nonl
        #@-node:ekr.20050725134243: ctor
        #@+node:ekr.20050725135621.1: Entry points
        def copyToRegister (self,event):
            return self.miniBuffer.setEvent(event,'s') and self.setNextRegister(event)
        def copyRectangleToRegister (self,event):
            return self.miniBuffer.setEvent(event,'r') and self.setNextRegister(event)
        def incrementRegister (self,event):
            return self.miniBuffer.setEvent(event,'plus') and self.setNextRegister(event)
        def insertRegister (self,event):
            return self.miniBuffer.setEvent(event,'i') and self.setNextRegister(event)
        def jumpToRegister (self,event):
            return self.miniBuffer.setEvent(event,'j') and self.setNextRegister(event)
        def numberToRegister (self,event):
            return self.miniBuffer.setEvent(event,'n') and self.setNextRegister(event)
        def pointToRegister (self,event):
            return self.miniBuffer.setEvent(event,'space') and self.setNextRegister(event)
        def viewRegister (self,event):
            return self.miniBuffer.setEvent(event,'view') and self.setNextRegister(event)
        #@nonl
        #@+node:ekr.20050724075352.174:appendToRegister
        def appendToRegister (self,event):
        
            b = self.miniBuffer
            event.keysym = 'a'
            self.setNextRegister(event)
            b.setState('controlx',True)
        #@nonl
        #@-node:ekr.20050724075352.174:appendToRegister
        #@+node:ekr.20050724075352.173:prependToRegister
        def prependToRegister (self,event):
        
            b = self.miniBuffer
            event.keysym = 'p'
            self.setNextRegister(event)
            b.setState('controlx',False)
        #@-node:ekr.20050724075352.173:prependToRegister
        #@+node:ekr.20050724075352.172:_copyRectangleToRegister
        def _copyRectangleToRegister (self,event):
            
            if not self._chckSel(event):
                return 
            if event.keysym in string.letters:
                event.keysym = event.keysym.lower()
                tbuffer = event.widget 
                r1, r2, r3, r4 = self.getRectanglePoints(event)
                rect =[]
                while r1<=r3:
                    txt = tbuffer.get('%s.%s'%(r1,r2),'%s.%s'%(r1,r4))
                    rect.append(txt)
                    r1 = r1+1
                self.registers[event.keysym] = rect 
            self.stopControlX(event)
        #@-node:ekr.20050724075352.172:_copyRectangleToRegister
        #@+node:ekr.20050724075352.171:_copyToRegister
        def _copyToRegister (self,event):
        
            if not self._chckSel(event):
                return 
        
            if event.keysym in string.letters:
                event.keysym = event.keysym.lower()
                tbuffer = event.widget 
                txt = tbuffer.get('sel.first','sel.last')
                self.registers[event.keysym] = txt 
                return 
        
            self.stopControlX(event)
        #@nonl
        #@-node:ekr.20050724075352.171:_copyToRegister
        #@+node:ekr.20050724075352.179:_incrementRegister
        def _incrementRegister (self,event):
            
            if self.registers.has_key(event.keysym):
                if self._checkIfRectangle(event):
                    return 
                if self.registers[event.keysym]in string.digits:
                    i = self.registers[event.keysym]
                    i = str(int(i)+1)
                    self.registers[event.keysym] = i 
                else:
                    self.invalidRegister(event,'number')
                    return 
            self.stopControlX(event)
        #@-node:ekr.20050724075352.179:_incrementRegister
        #@+node:ekr.20050724075352.178:_insertRegister
        def _insertRegister (self,event):
            
            tbuffer = event.widget 
            if self.registers.has_key(event.keysym):
                if isinstance(self.registers[event.keysym],list):
                    self.yankRectangle(event,self.registers[event.keysym])
                else:
                    tbuffer.insert('insert',self.registers[event.keysym])
                    tbuffer.event_generate('<Key>')
                    tbuffer.update_idletasks()
        
            self.stopControlX(event)
        #@nonl
        #@-node:ekr.20050724075352.178:_insertRegister
        #@+node:ekr.20050724075352.182:_jumpToRegister
        def _jumpToRegister (self,event):
            if event.keysym in string.letters:
                if self._checkIfRectangle(event):
                    return 
                tbuffer = event.widget 
                i = self.registers[event.keysym.lower()]
                i2 = i.split('.')
                if len(i2)==2:
                    if i2[0].isdigit()and i2[1].isdigit():
                        pass 
                    else:
                        self.invalidRegister(event,'index')
                        return 
                else:
                    self.invalidRegister(event,'index')
                    return 
                tbuffer.mark_set('insert',i)
                tbuffer.event_generate('<Key>')
                tbuffer.update_idletasks()
            self.stopControlX(event)
        #@nonl
        #@-node:ekr.20050724075352.182:_jumpToRegister
        #@+node:ekr.20050724075352.180:_numberToRegister
        def _numberToRegister (self,event):
            if event.keysym in string.letters:
                self.registers[event.keysym.lower()] = str(0)
            self.stopControlX(event)
        #@nonl
        #@-node:ekr.20050724075352.180:_numberToRegister
        #@+node:ekr.20050724075352.181:_pointToRegister
        def _pointToRegister (self,event):
            if event.keysym in string.letters:
                tbuffer = event.widget 
                self.registers[event.keysym.lower()] = tbuffer.index('insert')
            self.stopControlX(event)
        #@nonl
        #@-node:ekr.20050724075352.181:_pointToRegister
        #@+node:ekr.20050724075352.187:_viewRegister
        def _viewRegister (self,event):
            
            b = self.miniBuffer
            
            b.stopControlX(event)
        
            if event.keysym in string.letters:
                s = self.registers[event.keysym.lower()]
                b.set(s)
        #@nonl
        #@-node:ekr.20050724075352.187:_viewRegister
        #@-node:ekr.20050725135621.1: Entry points
        #@+node:ekr.20050725134243.1: getPublicCommands 
        def getPublicCommands (self):
            
            return {
                'append-to-register':           self.appendToRegister,
                'copy-rectangle-to-register':   self.copyRectangleToRegister,
                'copy-to-register':             self.copyToRegister,
                'increment-register':           self.incrementRegister,
                'insert-register':              self.insertRegister,
                'jump-to-register':             self.jumpToRegister,
                'number-to-register':           self.numberToRegister,
                'point-to-register':            self.pointToRegister,
                'prepend-to-register':          self.prependToRegister,
                'view-register':                self.viewRegister,
            }
        #@nonl
        #@-node:ekr.20050725134243.1: getPublicCommands 
        #@+node:ekr.20050726043333.1:Helpers
        #@+node:ekr.20050724075352.176:_chckSel
        def _chckSel( self, event ):
             if not 'sel' in event.widget.tag_names():
                return False
             if not event.widget.tag_ranges( 'sel' ):
                return False  
             return True
        #@nonl
        #@-node:ekr.20050724075352.176:_chckSel
        #@+node:ekr.20050724075352.177:_checkIfRectangle
        def _checkIfRectangle (self,event):
        
            b = self.miniBuffer
        
            if self.registers.has_key(event.keysym):
                if isinstance(self.registers[event.keysym],list):
                    b.stopControlX(event)
                    b.set("Register contains Rectangle, not text")
                    return True
        
            return False
        #@nonl
        #@-node:ekr.20050724075352.177:_checkIfRectangle
        #@+node:ekr.20050724075352.175:_ToReg
        def _ToReg( self, event , which):
        
            if not self._chckSel( event ):
                return
            if self._checkIfRectangle( event ):
                return
        
            if event.keysym in string.letters:
                event.keysym = event.keysym.lower()
                tbuffer = event.widget
                if not self.registers.has_key( event.keysym ):
                    self.registers[ event.keysym ] = ''
                txt = tbuffer.get( 'sel.first', 'sel.last' )
                rtxt = self.registers[ event.keysym ]
                if self.which == 'p':
                    txt = txt + rtxt
                else:
                    txt = rtxt + txt
                self.registers[ event.keysym ] = txt
                return
        #@nonl
        #@-node:ekr.20050724075352.175:_ToReg
        #@+node:ekr.20050724075352.52:addRegisterItems
        def addRegisterItems( self ):
            
            methodDict = {
                's':       self._copyToRegister,
                'i':       self._insertRegister,
                'n':        self._numberToRegister,
                'plus':     self._incrementRegister,
                'space':    self._pointToRegister,
                'j':        self._jumpToRegister,
                'a':        lambda event,which='a': self._ToReg(event,which), # _appendToRegister
                'p':        lambda event,which='p': self._ToReg(event,which), # _prependToRegister
                'r':        self._copyRectangleToRegister,
                'view' :    self._viewRegister,
            }    
            
            helpDict = {
                's':    'copy to register',
                'i':    'insert from register',
                'plus': 'increment register',
                'n':    'number to register',
                'p':    'prepend to register',
                'a':    'append to register',
                'space':'point to register',
                'j':    'jump to register',
                'r':    'rectangle to register',
                'view': 'view register',
            }
        
            return methodDict, helpDict
        #@nonl
        #@-node:ekr.20050724075352.52:addRegisterItems
        #@+node:ekr.20050724075352.186:deactivateRegister
        def deactivateRegister (self,event):
        
            b = self.miniBuffer
        
            b.set('')
            b.setLabelGrey()
        
            self.registermode = False
            self.method = None
        #@nonl
        #@-node:ekr.20050724075352.186:deactivateRegister
        #@+node:ekr.20050724075352.183:invalidRegister
        def invalidRegister (self,event,what):
        
            b = self.miniBuffer
        
            self.deactivateRegister(event)
            b.set('Register does not contain valid %s' % what)
        #@nonl
        #@-node:ekr.20050724075352.183:invalidRegister
        #@+node:ekr.20050724075352.184:setNextRegister
        def setNextRegister (self,event):
            
            b = self.miniBuffer
        
            if event.keysym=='Shift':
                return 
        
            if self.methodDict.has_key(event.keysym):
                b.setState('controlx',True)
                self.method = self.methodDict[event.keysym]
                self.registermode = 2
                b.set(self.helpDict[event.keysym])
            else:
                b.stopControlX(event)
        #@nonl
        #@-node:ekr.20050724075352.184:setNextRegister
        #@+node:ekr.20050724075352.185:executeRegister
        def executeRegister( self, event ):
        
            self.method( event )
            if self.registermode: 
                self.stopControlX( event )
            return
        #@nonl
        #@-node:ekr.20050724075352.185:executeRegister
        #@-node:ekr.20050726043333.1:Helpers
        #@-others
    #@nonl
    #@-node:ekr.20050724075352.170:class registerCommandsClass
    #@+node:ekr.20050724075352.221:class searchCommandsClass
    class searchCommandsClass (baseCommandsClass):
        
        '''Implements many kinds of searches.'''
    
        #@    @+others
        #@+node:ekr.20050725091822.2: ctor
        def __init__ (self,emacs):
        
            Emacs.baseCommandsClass.__init__(self,emacs) # init the base class.
            
            self.csr = { '<Control-s>': 'for', '<Control-r>':'bak' }
            self.pref = None
            
            self.qQ = None
            self.qR = None
            self.qgetQuery = False
            self.qgetReplace = False
            self.qrexecute = False
            self.querytype = 'normal'
        
            # For replace-string and replace-regex
            self._sString = ''
            self._rpString = ''
        #@nonl
        #@-node:ekr.20050725091822.2: ctor
        #@+node:ekr.20050725093156:getPublicCommands
        def getPublicCommands (self):
            
            return {
                'isearch-forward':          self.isearchForward,
                'isearch-backward':         self.isearchBackward,
                'isearch-forward-regexp':   self.isearchForwardRegexp,
                'isearch-backward-regexp':  self.isearchBackwardRegexp,
                
                're-search-forward':        self.reSearchForward,
                're-search-backward':       self.reSearchBackward,
                
                'search-forward':           self.searchForward,
                'search-backward':          self.searchBackward,
                'word-search-forward':      self.wordSearchForward,
                'word-search-backward':     self.wordSearchBackward,
            }
        #@nonl
        #@-node:ekr.20050725093156:getPublicCommands
        #@+node:ekr.20050725093537:Entry points
        # Incremental...
        def isearchForward (self,event):
            return self.miniBuffer.keyboardQuit(event) and self.startIncremental(event,'<Control-s>')
            
        def isearchBackward (self,event):
            return self.miniBuffer.keyboardQuit(event) and self.startIncremental(event,'<Control-r>')
            
        def isearchForwardRegexp (self,event):
            return self.miniBuffer.keyboardQuit(event) and self.startIncremental(event,'<Control-s>',which='regexp')
            
        def isearchBackwardRegexp (self,event):
            return self.miniBuffer.keyboardQuit(event) and self.startIncremental(event,'<Control-r>',which='regexp')
        
        # Non-incremental...
        def reSearchBackward (self,event):
            return self.reStart(event,which='backward')
        
        def searchForward (self,event):
            return self.startNonIncrSearch(event,'for')
            
        def searchBackward (self,event):
            return self.startNonIncrSearch(event,'bak')
            
        def wordSearchForward (self,event):
            return self.startWordSearch(event,'for')
            
        def wordSearchBackward (self,event):
            return self.startWordSearch(event,'bak')
        #@nonl
        #@-node:ekr.20050725093537:Entry points
        #@+node:ekr.20050724075352.222:incremental search methods
        #@+node:ekr.20050724075352.223:startIncremental
        def startIncremental (self,event,stroke,which='normal'):
        
            b = self.miniBuffer
        
            state = b.getState('isearch')
            
            g.trace(stroke)
            
            if state == 0:
                self.pref = self.csr [stroke]
                if 0: # Interferes with code in isearch. isearch take account of the search arg.
                    b.set('isearch:',protect=True)
                b.setLabelBlue()
                b.setState('isearch',which)
            else:
                self.search(event,way=self.csr[stroke],useregex=self.useRegex())
                self.pref = self.csr [stroke]
                self.scolorizer(event)
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.223:startIncremental
        #@+node:ekr.20050724075352.224:search
        def search (self,event,way,useregex=False):
            '''This method moves the insert spot to position that matches the pattern in the miniBuffer'''
        
            b = self.miniBuffer ; tbuffer = event.widget
            s = b.get()
            if s:
                try:
                    if way == 'bak': # Search backwards.
                        i = tbuffer.search(s,'insert',backwards=True,stopindex='1.0',regexp=useregex)
                        if not i:
                            # Start again at the bottom of the buffer.
                            i = tbuffer.search(s,'end',backwards=True,stopindex='insert',regexp=useregex)
                    else: # Search forwards.
                        i = tbuffer.search(s,"insert + 1c",stopindex='end',regexp=useregex)
                        if not i:
                            # Start again at the top of the buffer.
                            i = tbuffer.search(s,'1.0',stopindex='insert',regexp=useregex)
                except: pass
        
                if i and not i.isspace():
                    tbuffer.mark_set('insert',i)
                    tbuffer.see('insert')
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.224:search
        #@+node:ekr.20050724075352.225:iSearch
        def iSearch (self,event,stroke):
            
            g.trace(stroke)
        
            b = self.miniBuffer ; tbuffer = event.widget
            if not event.char: return
        
            if stroke in self.csr:
                return self.startIncremental(event,stroke)
        
            if event.keysym == 'Return':
                  if b.get() == '':
                      return self.startNonIncrSearch(event,self.pref)
                  else:
                    return self.stopControlX(event)
            b.update(event)
            if event.char != '\b':
               stext = b.get()
               z = tbuffer.search(stext,'insert',stopindex='insert +%sc' % len(stext))
               if not z:
                   self.search(event,self.pref,useregex=self.useRegex())
            self.scolorizer(event)
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.225:iSearch
        #@+node:ekr.20050724075352.226:scolorizer
        def scolorizer (self,event):
        
            b = self.miniBuffer ; tbuffer = event.widget
        
            stext = b.get()
            tbuffer.tag_delete('color')
            tbuffer.tag_delete('color1')
            if stext == '': return 'break'
            ind = '1.0'
            while ind:
                try:
                    ind = tbuffer.search(stext,ind,stopindex='end',regexp=self.useRegex())
                except:
                    break
                if ind:
                    i, d = ind.split('.')
                    d = str(int(d)+len(stext))
                    index = tbuffer.index('insert')
                    if ind == index:
                        tbuffer.tag_add('color1',ind,'%s.%s' % (i,d))
                    tbuffer.tag_add('color',ind,'%s.%s' % (i,d))
                    ind = i + '.' + d
            tbuffer.tag_config('color',foreground='red')
            tbuffer.tag_config('color1',background='lightblue')
        #@nonl
        #@-node:ekr.20050724075352.226:scolorizer
        #@+node:ekr.20050724075352.227:useRegex
        def useRegex (self):
        
            b = self.miniBuffer
        
            return b.getState('isearch') != 'normal'
        #@nonl
        #@-node:ekr.20050724075352.227:useRegex
        #@-node:ekr.20050724075352.222:incremental search methods
        #@+node:ekr.20050724075352.228:non-incremental search methods
        #@+at
        # Accessed by Control-s Enter or Control-r Enter.
        # Alt-x forward-search or backward-search, just looks for words...
        #@-at
        #@nonl
        #@+node:ekr.20050724075352.229:nonincrSearch
        def nonincrSearch (self,event,stroke):
        
            b = self.miniBuffer ; tbuffer = event.widget
        
            if event.keysym in ('Control_L','Control_R'): return
            state = b.getState('nonincr-search')
            if state.startswith('start'):
                state = state [5:]
                b.setState('nonincr-search',state)
                b.set('')
        
            if b.get() == '' and stroke == '<Control-w>':
                return self.startWordSearch(event,state)
        
            if event.keysym == 'Return':
                i = tbuffer.index('insert')
                word = b.get()
                if state == 'for':
                    s = tbuffer.search(word,i,stopindex='end')
                    if s: s = tbuffer.index('%s +%sc' % (s,len(word)))
                else: s = tbuffer.search(word,i,stopindex='1.0',backwards=True)
                if s: tbuffer.mark_set('insert',s)
                b.keyboardQuit(event)
                return b._tailEnd(tbuffer)
            else:
                b.update(event)
                return 'break'
        #@nonl
        #@-node:ekr.20050724075352.229:nonincrSearch
        #@+node:ekr.20050724075352.230:startNonIncrSearch
        def startNonIncrSearch (self,event,which):
        
            b = self.miniBuffer
        
            b.keyboardQuit(event)
            b.setState('nonincr-search','start%s' % which)
            b.setLabelBlue()
            b.set('Search:')
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.230:startNonIncrSearch
        #@-node:ekr.20050724075352.228:non-incremental search methods
        #@+node:ekr.20050724075352.231:word search methods
        #@+at
        # 
        # Control-s(r) Enter Control-w words Enter, pattern entered is treated 
        # as a regular expression.
        # 
        # for example in the buffer we see:
        #     cats......................dogs
        # 
        # if we are after this and we enter the backwards look, search for 
        # 'cats dogs' if will take us to the match.
        #@-at
        #@nonl
        #@+node:ekr.20050724075352.232:startWordSearch
        def startWordSearch (self,event,which):
        
            b = self.miniBuffer
        
            b.keyboardQuit(event)
            b.setState('word-search','start%s' % which)
            b.setLabelBlue()
            b.set('Word Search %s:' % g.choose(which=='bak','Backward','Forward'))
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.232:startWordSearch
        #@+node:ekr.20050724075352.233:wordSearch
        def wordSearch (self,event):
        
            b = self.miniBuffer ; tbuffer = event.widget
            state = b.getState('word-search')
            if state.startswith('start'):
                state = state [5:]
                b.setState('word-search',state)
                b.set('')
            if event.keysym == 'Return':
                i = tbuffer.index('insert')
                words = b.get().split()
                sep = '[%s%s]+' % (string.punctuation,string.whitespace)
                pattern = sep.join(words)
                cpattern = re.compile(pattern)
                if state == 'for':
                    txt = tbuffer.get('insert','end')
                    match = cpattern.search(txt)
                    if not match: return b.keyboardQuit(event)
                    end = match.end()
                else:
                    txt = tbuffer.get('1.0','insert') #initially the reverse words formula for Python Cookbook was going to be used.
                    a = re.split(pattern,txt) #that didnt quite work right.  This one apparently does.
                    if len(a) > 1:
                        b = re.findall(pattern,txt)
                        end = len(a[-1]) + len(b[-1])
                    else: return b.keyboardQuit(event)
                wdict = {'for': 'insert +%sc', 'bak': 'insert -%sc'}
                tbuffer.mark_set('insert',wdict[state] % end)
                tbuffer.see('insert')
                b.keyboardQuit(event)
                return b._tailEnd(tbuffer)
            else:
                b.update(event)
                return 'break'
        #@nonl
        #@-node:ekr.20050724075352.233:wordSearch
        #@-node:ekr.20050724075352.231:word search methods
        #@+node:ekr.20050724075352.234:re-search methods
        # For the re-search-backward and re-search-forward Alt-x commands
        #@nonl
        #@+node:ekr.20050724075352.235:reStart
        def reStart (self,event,which='forward'):
        
            b = self.miniBuffer
        
            b.keyboardQuit(event)
            b.setState('re_search','start%s' % which)
            b.setLabelBlue()
            b.set('RE Search:')
        
            return 'break'
        
        reSearchForward = reStart
        #@nonl
        #@-node:ekr.20050724075352.235:reStart
        #@+node:ekr.20050724075352.236:re_search
        def re_search( self, event ):
        
            b = self.miniBuffer ; tbuffer = event.widget
            state = b.getState( 're_search' )
            if state.startswith( 'start' ):
                state = state[ 5: ]
                b.setState( 're_search', state )
                b.set( '' )
            if event.keysym == 'Return':
                pattern = b.get()
                cpattern = re.compile( pattern )
                end = None
                if state == 'forward':
                    txt = tbuffer.get( 'insert', 'end' )
                    match = cpattern.search( txt )
                    end = match.end()
                else:
                    txt = tbuffer.get( '1.0', 'insert' ) #initially the reverse words formula for Python Cookbook was going to be used.
                    a = re.split( pattern, txt )         #that didnt quite work right.  This one apparently does.   
                    if len( a ) > 1:
                        b = re.findall( pattern, txt )
                        end = len( a[ -1 ] ) + len( b[ -1 ] )
                if end:
                    wdict ={ 'forward': 'insert +%sc', 'backward': 'insert -%sc' }
                    tbuffer.mark_set( 'insert', wdict[ state ] % end )                                
                    b._tailEnd( tbuffer )
                    tbuffer.see( 'insert' )
                return b.keyboardQuit( event )    
            else:
                b.update( event )
                return 'break'
        #@nonl
        #@-node:ekr.20050724075352.236:re_search
        #@-node:ekr.20050724075352.234:re-search methods
        #@-others
    #@nonl
    #@-node:ekr.20050724075352.221:class searchCommandsClass
    #@-others
    #@nonl
    #@-node:ekr.20050725091822:Commands classes...
    #@+node:ekr.20050727161004:class miniBufferClass 
    class miniBufferClass:
    
        #@    @+others
        #@+node:ekr.20050728103627: Birth
        #@+node:ekr.20050727162112: ctor
        def __init__ (self,emacs,widget):
        
            self.emacs = emacs
            self.c = emacs.c
            self.widget = widget # A Tk Label widget.
            
            self.svar = Tk.StringVar()
            self.widget.configure(textvariable=self.svar)
        
            # Ivars.
            self.altx_history = []
            self.keysymhistory = []
            self.previousStroke = ''
            self.svars = {}
            self.tailEnds = {} # functions to execute at the end of many Emac methods.  Configurable by environment.
            
            # For accumlated args...
            self.arg = ''
            self.afterGetArgState = None
            self.argPromptLen = 0
        
            # For negative arguments...
            self.negativeArg = False
            self.negArgs = {} # Set in finishCreate.
        
            # For alt-X commands...
            self.xcommands = None       # Done in finishCreate.
            self.altX_commandsDict = {} # Set later by finishCreate.
            self.axTabList = emacs.Tracker()
            self.x_hasNumeric = ['sort-lines','sort-fields']
        
            # For universal commands...
            self.uCstring = string.digits + '\b'
            self.uCdict = {
                '<Alt-x>': self.alt_X
            }
        
            self.stateManager = self.stateManagerClass(emacs) # Manages state for the master command
            self.kstrokeManager = self.keyStrokeManagerClass(emacs) # Manages some keystroke state for the master command.
            self.cxHandler = self.controlX_handlerClass(emacs) # Create the handler for Control-x commands
            
            # Delegators.  These will go away if the state helper class goes away.
            self.getState = self.stateManager.getState
            self.setState = self.stateManager.setState
            self.hasState = self.stateManager.hasState
            self.whichState = self.stateManager.whichState
        #@nonl
        #@-node:ekr.20050727162112: ctor
        #@+node:ekr.20050729150051.2:add_ekr_altx_commands
        def add_ekr_altx_commands (self):
        
            #@    << define dict d of abbreviations >>
            #@+node:ekr.20050729150804:<< define dict d of abbreviations >>
            d = {
                'i':    'isearch-forward', 
                'ib':   'isearch-backward',      
                'ix':   'isearch-forward-regexp',
                'irx':  'isearch-backward-regexp',
                'ixr':  'isearch-backward-regexp',
                
                'r':    'replace-string',
                'rx':   'replace-regex',
            
                's':    'search-forward',
                'sb':   'search-backward',
                
                'sw':   'word-search-forward',    
                'sbw':  'word-search-backward',
                'swb':  'word-search-backward',
                
                #
                # 'a1'  'abbrev-on'
                # 'a0'  'abbrev-off'
             
                ## Don't put these in: they might conflict with other abbreviatsions.
                # 'fd':   'find-dialog',
                # 'od':   'options-dialog',
                
                # At present these would be Leo Find stuff.
                # 'f':    'find',
                # 'fr':   'find-reverse',
                # 'fx':   'find-regex',
                # 'frx':  'find-regex-reverse',
                # 'fxr':  'find-regex-reverse',
                # 'fw':   'find-word',
                # 'sf':   'set-find-text',
                # 'sr':   'set-find-replace',
                # 'ss':   'script-search',
                # 'ssr':  'script-search-reverse',
                
                ## These could be shared...
                # 'tfh':  'toggle-find-search-headline',
                # 'tfb':  'toggle-find-search-body',
                # 'tfw':  'toggle-find-word',
                # 'tfn':  'toggle-find-node-only',
                # 'tfi':  'toggle-find-ignore-case',
                # 'tfmc': 'toggle-find-mark-changes',
                # 'tfmf': 'toggle-find-mark-finds',
            }
            #@nonl
            #@-node:ekr.20050729150804:<< define dict d of abbreviations >>
            #@nl
        
            keys = d.keys()
            keys.sort()
            for key in keys:
                val = d.get(key)
                func = self.altX_commandsDict.get(val)
                if func:
                    g.trace(('%-4s' % key),val)
                    self.altX_commandsDict [key] = func
        #@-node:ekr.20050729150051.2:add_ekr_altx_commands
        #@+node:ekr.20050724075352.49:addCallBackDict (creates cbDict) TO BE REMOVED
        ### This could be replaced by Leo's normal menu-creation logic.
        
        def addCallBackDict (self):
        
            '''Create callback dictionary for masterCommand.'''
        
            b = self ; emacs = self.emacs
        
            cbDict = {
            'Alt-less':     lambda event, spot = '1.0': emacs.editCommands.moveTo(event,spot),
            'Alt-greater':  lambda event, spot = 'end': emacs.editCommands.moveTo(event,spot),
            'Control-Right': lambda event, way = 1: emacs.editCommands.moveword(event,way),
            'Control-Left': lambda event, way = -1: emacs.editCommands.moveword(event,way),
            'Control-a':    lambda event, spot = 'insert linestart': emacs.editCommands.moveTo(event,spot),
            'Control-e':    lambda event, spot = 'insert lineend': emacs.editCommands.moveTo(event,spot),
            'Alt-Up':       lambda event, spot = 'insert linestart': emacs.editCommands.moveTo(event,spot),
            'Alt-Down':     lambda event, spot = 'insert lineend': emacs.editCommands.moveTo(event,spot),
            'Alt-f':        lambda event, way = 1: emacs.editCommands.moveword(event,way),
            'Alt-b':        lambda event, way = -1: emacs.editCommands.moveword(event,way),
            'Control-o':    emacs.editCommands.insertNewLine,
            'Control-k':    lambda event, frm = 'insert', to = 'insert lineend': emacs.kill(event,frm,to),
            'Alt-d':        lambda event, frm = 'insert wordstart', to = 'insert wordend': emacs.kill(event,frm,to),
            'Alt-Delete':   lambda event: emacs.deletelastWord(event),
            "Control-y":    lambda event, frm = 'insert', which = 'c': emacs.walkKB(event,frm,which),
            "Alt-y":        lambda event, frm = "insert", which = 'a': emacs.walkKB(event,frm,which),
            "Alt-k":        lambda event: emacs.killsentence(event),
            'Control-s':    None,
            'Control-r':    None,
            'Alt-c':        lambda event, which = 'cap': emacs.editCommands.capitalize(event,which),
            'Alt-u':        lambda event, which = 'up': emacs.editCommands.capitalize(event,which),
            'Alt-l':        lambda event, which = 'low': emacs.editCommands.capitalize(event,which),
            'Alt-t':        lambda event, sw = emacs.editCommands.swapSpots: emacs.editCommands.swapWords(event,sw),
            'Alt-x':        self.alt_X,
            'Control-x':    self.startControlX,
            'Control-g':    b.keyboardQuit,
            'Control-Shift-at': emacs.editCommands.setRegion,
            'Control-w':    lambda event, which = 'd': emacs.editCommands.killRegion(event,which),
            'Alt-w':        lambda event, which = 'c': emacs.editCommands.killRegion(event,which),
            'Control-t':    emacs.editCommands.swapCharacters,
            'Control-u':    None,
            'Control-l':    None,
            'Alt-z':        None,
            'Control-i':    None,
            'Alt-Control-backslash': emacs.editCommands.indentRegion,
            'Alt-m':            emacs.editCommands.backToIndentation,
            'Alt-asciicircum':  emacs.editCommands.deleteIndentation,
            'Control-d':        emacs.editCommands.deleteNextChar,
            'Alt-backslash':    emacs.editCommands.deleteSpaces,
            'Alt-g':        None,
            'Control-v':    lambda event, way = 'south': emacs.editCommands.screenscroll(event,way),
            'Alt-v':        lambda event, way = 'north': emacs.editCommands.screenscroll(event,way),
            'Alt-equal':    emacs.editCommands.countRegion,
            'Alt-parenleft':    emacs.editCommands.insertParentheses,
            'Alt-parenright':   emacs.editCommands.movePastClose,
            'Alt-percent':  None,
            'Control-c':    None,
            'Delete':       lambda event, which = 'BackSpace': self.manufactureKeyPress(event,which),
            'Control-p':    lambda event, which = 'Up': self.manufactureKeyPress(event,which),
            'Control-n':    lambda event, which = 'Down': self.manufactureKeyPress(event,which),
            'Control-f':    lambda event, which = 'Right': self.manufactureKeyPress(event,which),
            'Control-b':    lambda event, which = 'Left': self.manufactureKeyPress(event,which),
            'Control-Alt-w': None,
            'Alt-a':        emacs.editCommands.backSentence,
            'Alt-e':        emacs.editCommands.forwardSentence,
            'Control-Alt-o': emacs.editCommands.insertNewLineIndent,
            'Control-j':    emacs.editCommands.insertNewLineAndTab,
            'Alt-minus':    self.negativeArgument,
            'Alt-slash':    emacs.editCommands.dynamicExpansion,
            'Control-Alt-slash':    emacs.editCommands.dynamicExpansion2,
            'Control-u':        lambda event, keystroke = '<Control-u>': self.universalDispatch(event,keystroke),
            'Alt-braceright':   lambda event, which = 1: emacs.movingParagraphs(event,which),
            'Alt-braceleft':    lambda event, which = 0: emacs.movingParagraphs(event,which),
            'Alt-q':        emacs.editCommands.fillParagraph,
            'Alt-h':        emacs.editCommands.selectParagraph,
            'Alt-semicolon': emacs.editCommands.indentToCommentColumn,
            'Alt-0': lambda event, stroke = '<Alt-0>', number = 0: self.numberCommand(event,stroke,number),
            'Alt-1': lambda event, stroke = '<Alt-1>', number = 1: self.numberCommand(event,stroke,number),
            'Alt-2': lambda event, stroke = '<Alt-2>', number = 2: self.numberCommand(event,stroke,number),
            'Alt-3': lambda event, stroke = '<Alt-3>', number = 3: self.numberCommand(event,stroke,number),
            'Alt-4': lambda event, stroke = '<Alt-4>', number = 4: self.numberCommand(event,stroke,number),
            'Alt-5': lambda event, stroke = '<Alt-5>', number = 5: self.numberCommand(event,stroke,number),
            'Alt-6': lambda event, stroke = '<Alt-6>', number = 6: self.numberCommand(event,stroke,number),
            'Alt-7': lambda event, stroke = '<Alt-7>', number = 7: self.numberCommand(event,stroke,number),
            'Alt-8': lambda event, stroke = '<Alt-8>', number = 8: self.numberCommand(event,stroke,number),
            'Alt-9': lambda event, stroke = '<Alt-9>', number = 9: self.numberCommand(event,stroke,number),
            'Control-underscore': emacs.doUndo,
            'Alt-s':            emacs.editCommands.centerLine,
            'Control-z':        emacs.emacsControlCommands.suspend,
            'Control-Alt-s':    lambda event, stroke = '<Control-s>': emacs.startIncremental(event,stroke,which='regexp'),
            'Control-Alt-r':    lambda event, stroke = '<Control-r>': emacs.startIncremental(event,stroke,which='regexp'),
            'Control-Alt-percent': lambda event: emacs.startRegexReplace()and emacs.masterQR(event),
            'Escape':       emacs.editCommands.watchEscape,
            'Alt-colon':    emacs.editCommands.startEvaluate,
            'Alt-exclam':   emacs.emacsControlCommands.startSubprocess,
            'Alt-bar':      lambda event: emacs.emacsControlCommands.startSubprocess(event,which=1),
            }
        
            return cbDict
        #@-node:ekr.20050724075352.49:addCallBackDict (creates cbDict) TO BE REMOVED
        #@+node:ekr.20050724075352.144:addToDoAltX
        def addToDoAltX (self,name,macro):
        
            '''Adds macro to Alt-X commands.'''
        
            if self.altX_commandsDict.has_key(name):
                return False
        
            def exe (event,macro=macro):
                self.stopControlX(event)
                return self._executeMacro(macro,event.widget)
        
            self.altX_commandsDict [name] = exe
            self.namedMacros [name] = macro
            return True
        #@nonl
        #@-node:ekr.20050724075352.144:addToDoAltX
        #@+node:ekr.20050724075352.90:changecbDict NOT USED
        def changecbDict (self,changes):
            for z in changes:
                if self.cbDict.has_key(z):
                    self.cbDict [z] = self.changes [z]
        #@nonl
        #@-node:ekr.20050724075352.90:changecbDict NOT USED
        #@+node:ekr.20050728093027.1:finishCreate TO DO: remove these tables?
        def finishCreate (self,altX_commandsDict):
        
            emacs = self.emacs
        
            # Finish creating the helper classes.
            self.stateManager.finishCreate()
            self.kstrokeManager.finishCreate()
            self.cxHandler.finishCreate()
        
            # Finish this class.
            self.altX_commandsDict = altX_commandsDict
        
            self.add_ekr_altx_commands()
        
            # Command bindings.
            self.cbDict = self.addCallBackDict() # Creates callback dictionary, primarily used in the master command
        
            self.negArgs = {
                '<Alt-c>': self.emacs.editCommands.changePreviousWord,
                '<Alt-u>': self.emacs.editCommands.changePreviousWord,
                '<Alt-l>': self.emacs.editCommands.changePreviousWord,
            }
        
            self.xcommands = {
                '<Control-t>': emacs.editCommands.transposeLines,
                '<Control-u>': lambda event, way = 'up': emacs.upperLowerRegion(event,way),
                '<Control-l>': lambda event, way = 'low': emacs.upperLowerRegion(event,way),
                '<Control-o>': emacs.editCommands.removeBlankLines,
                '<Control-i>': emacs.fileCommands.insertFile,
                '<Control-s>': emacs.fileCommands.saveFile,
                '<Control-x>': emacs.editCommands.exchangePointMark,
                '<Control-c>': emacs.emacsControlCommands.shutdown,
                '<Control-b>': emacs.bufferCommands.listBuffers,
                '<Control-Shift-at>': lambda event: event.widget.selection_clear(),
                '<Delete>': lambda event, back = True: emacs.editCommands.killsentence(event,back),
            }
        #@nonl
        #@-node:ekr.20050728093027.1:finishCreate TO DO: remove these tables?
        #@+node:ekr.20050724075352.112:setBufferStrokes  (creates svars & <key> bindings
        def setBufferStrokes (self,tbuffer):
        
            '''Sets key bindings for a Tk Text widget.'''
        
            # Create one binding for each entry in cbDict.
            for key in self.cbDict:
                self.bindKey(tbuffer,key)
        
            # Add a binding for <Key> events, so _all_ key events go through masterCommand.
            self.bindKey(tbuffer,'Key')
        #@nonl
        #@+node:ekr.20050724075352.113:bindKey
        def bindKey (self,tbuffer,evstring):
        
            callback = self.cbDict.get(evstring)
            evstring = '<%s>' % evstring
        
            def f (event):
                return self.masterCommand(event,callback,evstring)
        
            if evstring != '<Key>':
                tbuffer.bind(evstring,f)
            else:
                tbuffer.bind(evstring,f,'+')
        #@nonl
        #@-node:ekr.20050724075352.113:bindKey
        #@-node:ekr.20050724075352.112:setBufferStrokes  (creates svars & <key> bindings
        #@-node:ekr.20050728103627: Birth
        #@+node:ekr.20050728092044: Entry points
        # These are user commands accessible via alt-x.
        
        def digitArgument (self,event):
            return self.universalDispatch(event,'')
        
        def universalArgument (self,event):
            return self.universalDispatch(event,'')
        #@nonl
        #@-node:ekr.20050728092044: Entry points
        #@+node:ekr.20050730113639: Getters & Setters
        #@+node:ekr.20050724075352.85:setEvent
        def setEvent (self,event,l):
        
            event.keysym = l
            return event
        #@nonl
        #@-node:ekr.20050724075352.85:setEvent
        #@+node:ekr.20050724075352.99:setLabelGrey
        def setLabelGrey (self):
        
            self.widget.configure(background='lightgrey')
        #@nonl
        #@-node:ekr.20050724075352.99:setLabelGrey
        #@+node:ekr.20050724075352.100:setLabelBlue
        def setLabelBlue (self):
        
            self.widget.configure(background='lightblue')
        #@nonl
        #@-node:ekr.20050724075352.100:setLabelBlue
        #@+node:ekr.20050724075352.101:reset
        def reset (self):
            
            b = self
        
            b.set('')
            b.setLabelGrey()
        #@nonl
        #@-node:ekr.20050724075352.101:reset
        #@+node:ekr.20050724075352.104:update
        def update (self,event):
        
            '''
            Alters the StringVar svar to represent the change in the event.
            This has the effect of changing the miniBuffer contents.
        
            It mimics what would happen with the keyboard and a Text editor
            instead of plain accumalation.'''
            
            b = self ; s = b.get() ; ch = event.char
        
            if ch == '\b': # Handle backspace.
                # Don't backspace over the prompt.
                if len(s) <= self.argPromptLen:
                    return 
                elif len(s) == 1: s = ''
                else: s = s [0:-1]
            else:
                # Add the character.
                s = s + ch
        
            b.set(s)
        #@nonl
        #@-node:ekr.20050724075352.104:update
        #@+node:ekr.20050730121359:get & set
        def get (self):
            
            return self.svar.get()
            
        def set (self,s,protect=False):
            
            self.svar.set(s)
            if protect:
                self.argPromptLen = len(s)
        #@nonl
        #@-node:ekr.20050730121359:get & set
        #@-node:ekr.20050730113639: Getters & Setters
        #@+node:ekr.20050724075352.283:Alt_X methods
        #@+node:ekr.20050724075352.285:doAlt_X & helpers
        def doAlt_X (self,event):
        
            '''This method executes the correct Alt-X command'''
            
            b = self
        
            if b.get().endswith('M-x:'):
                b.axTabList.clear() # Clear the list, new Alt-x command is in effect.
                b.set('')
            if event.keysym == 'Return':
                s = b.get()
                func = b.altX_commandsDict.get(s)
                if func:
                    if s != 'repeat-complex-command': b.altx_history.insert(0,s)
                    aX = b.getState('altx')
                    if (type(aX) == type(1) or aX.isdigit()) and s in b.x_hasNumeric:
                        func(event,aX)
                    else:
                        func(event)
                else:
                    b.keyboardQuit(event)
                    b.set('Command does not exist')
            elif event.keysym == 'Tab':
                #@        << handle tab completion >>
                #@+node:ekr.20050729094213:<< handle tab completion >>
                s = b.get().strip()
                
                if b.axTabList.prefix and s.startswith(b.axTabList.prefix):
                    b.set(b.axTabList.next()) # get next in iteration
                else:
                    prefix = b.get()
                    pmatches = b._findMatch()
                    b.axTabList.setTabList(prefix,pmatches)
                    b.set(b.axTabList.next()) # begin iteration on new lsit
                #@nonl
                #@-node:ekr.20050729094213:<< handle tab completion >>
                #@nl
            else:
                b.axTabList.clear() #clear the list, any other character besides tab indicates that a new prefix is in effect.
                b.update(event)
            return 'break'
        #@nonl
        #@+node:ekr.20050724075352.92:_findMatch
        def _findMatch (self,fdict=None):
            
            '''This method returns a sorted list of matches.'''
        
            if not fdict:
                fdict = self.altX_commandsDict
        
            s = self.get()
            if not s.isspace() and s != '':
                s = s.strip()
                pmatches = filter(lambda a: a.startswith(s),fdict)
            else:
                pmatches = []
        
            pmatches.sort()
            return pmatches
        #@nonl
        #@-node:ekr.20050724075352.92:_findMatch
        #@-node:ekr.20050724075352.285:doAlt_X & helpers
        #@+node:ekr.20050724075352.284:alt_X
        def alt_X (self,event=None,which=None):
        
            b = self
        
            b.setState('altx',g.choose(which,which,1))
            b.set(g.choose(which,'%s M-x:' % which,'M-x:'))
            b.setLabelBlue()
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.284:alt_X
        #@+node:ekr.20050724075352.286:execute last altx methods
        #@+node:ekr.20050724075352.287:executeLastAltX
        def executeLastAltX (self,event):
            
            b = self
        
            if event.keysym == 'Return' and b.altx_history:
                last = self.altx_history [0]
                b.altX_commandsDict [last](event)
                return 'break'
            else:
                return b.keyboardQuit(event)
        #@nonl
        #@-node:ekr.20050724075352.287:executeLastAltX
        #@+node:ekr.20050724075352.288:repeatComplexCommand
        def repeatComplexCommand (self,event=None):
        
            b = self
        
            b.keyboardQuit(event)
        
            if self.altx_history:
                self.setLabelBlue()
                b.set("Redo: %s" % b.altx_history[0])
                b.setState('last-altx',True)
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.288:repeatComplexCommand
        #@-node:ekr.20050724075352.286:execute last altx methods
        #@-node:ekr.20050724075352.283:Alt_X methods
        #@+node:ekr.20050724075352.14:class controlX_handlerClass
        class controlX_handlerClass:
        
            '''The ControlXHandler manages how the Control-X based commands operate on the
               Emacs instance.'''    
            
            #@    @+others
            #@+node:ekr.20050724075352.15:__init__
            def __init__ (self,emacs):
            
                self.emacs = emacs
                self.previous = []
            
                # These are set in miniBuffer.finishCreate.
                self.rect_commands = {}
                self.variety_commands = {}
                self.abbreviationDispatch = {}
                self.register_commands = {}
            #@nonl
            #@-node:ekr.20050724075352.15:__init__
            #@+node:ekr.20050724075352.16:__call__
            def __call__ (self,event,stroke):
            
                emacs = self.emacs
            
                self.previous.insert(0,event.keysym)
            
                if len(self.previous) > 10:
                    self.previous.pop()
            
                if stroke in ('<Key>','<Escape>'):
                    return self.processKey(event)
            
                if stroke in emacs.xcommands:
                    emacs.xcommands [stroke](event)
                    if stroke != '<Control-b>': emacs.keyboardQuit(event)
            
                return 'break'
            #@nonl
            #@-node:ekr.20050724075352.16:__call__
            #@+node:ekr.20050728103627.2:finishCreate
            def finishCreate (self):
            
                emacs = self.emacs
            
                self.abbreviationDispatch = {
                    'a':    lambda event: emacs.abbreviationDispatch(event,1),
                    'a i':  lambda event: emacs.abbreviationDispatch(event,2),
                }
            
                self.rect_commands = {
                    'o': emacs.rectangleCommands.openRectangle,
                    'c': emacs.rectangleCommands.clearRectangle,
                    't': emacs.rectangleCommands.stringRectangle,
                    'y': emacs.rectangleCommands.yankRectangle,
                    'd': emacs.rectangleCommands.deleteRectangle,
                    'k': emacs.rectangleCommands.killRectangle,
                    'r': emacs.rectangleCommands.activateRectangleMethods,
                }
            
                self.register_commands = {
                    1: emacs.registerCommands.setNextRegister,
                    2: emacs.registerCommands.executeRegister,
                }
            
                self.variety_commands = {
                    'period':       emacs.editCommands.setFillPrefix,
                    'parenleft':    emacs.macroCommands.startKBDMacro,
                    'parenright':   emacs.macroCommands.stopKBDMacro,
                    'semicolon':    emacs.editCommands.setCommentColumn,
                    'Tab':          emacs.editCommands.tabIndentRegion,
                    'u':            lambda event: emacs.doUndo(event,2),
                    'equal':        emacs.editCommands.lineNumber,
                    'h':            emacs.editCommands.selectAll,
                    'f':            emacs.editCommands.setFillColumn,
                    'b':            lambda event, which = 'switch-to-buffer': emacs.setInBufferMode(event,which),
                    'k':            lambda event, which = 'kill-buffer': emacs.setInBufferMode(event,which),
                }
            #@nonl
            #@-node:ekr.20050728103627.2:finishCreate
            #@+node:ekr.20050724075352.17:processKey
            def processKey (self,event):
            
                b = self ; emacs = self.emacs
                previous = self.previous
                if event.keysym in ('Shift_L','Shift_R'):
                    return
            
                if emacs.sRect:
                    return emacs.stringRectangle(event)
            
                if (
                    event.keysym == 'r' and
                    emacs.rectangleCommands.rectanglemode == 0
                    and not emacs.registerCommands.registermode
                ):
                    return self.processRectangle(event)
            
                if (
                    self.rect_commands.has_key(event.keysym) and
                    emacs.rectangleCommands.rectanglemode == 1
                ):
                    return self.processRectangle(event)
            
                if self.register_commands.has_key(emacs.registerCommands.registermode):
                    self.register_commands [emacs.registerCommands.registermode] (event)
                    return 'break'
            
                if self.variety_commands.has_key(event.keysym):
                    emacs.stopControlX(event)
                    return self.variety_commands [event.keysym](event)
            
                if event.keysym in ('a','i','e'):
                    if self.processAbbreviation(event): return 'break'
            
                if event.keysym == 'g':
                    l = b.get()
                    if self.abbreviationDispatch.has_key(l):
                        emacs.stopControlX(event)
                        return self.abbreviationDispatch [l](event)
            
                if event.keysym == 'e':
                    emacs.stopControlX(event)
                    return emacs.macroCommands.executeLastMacro(event)
            
                if event.keysym == 'x' and previous [1] not in ('Control_L','Control_R'):
                    event.keysym = 's'
                    emacs.setNextRegister(event)
                    return 'break'
            
                if event.keysym == 'Escape':
                    if len(previous) > 1:
                        if previous [1] == 'Escape':
                            return emacs.repeatComplexCommand(event)
            #@-node:ekr.20050724075352.17:processKey
            #@+node:ekr.20050724075352.18:processRectangle
            def processRectangle (self,event):
            
                self.rect_commands [event.keysym] (event)
                return 'break'
                #if event.keysym == 'o':
                #    emacs.openRectangle( event )
                #    return 'break'
                #if event.keysym == 'c':
                #    emacs.clearRectangle( event )
                #    return 'break'
                #if event.keysym == 't':
                #    emacs.stringRectangle( event )
                #    return 'break'
                #if event.keysym == 'y':
                #    emacs.yankRectangle( event )
                #    return 'break'
                #if event.keysym == 'd':
                #    emacs.deleteRectangle( event )
                #    return 'break'
                #if event.keysym == 'k':
                #    emacs.killRectangle( event )
                #    return 'break'
            #@nonl
            #@-node:ekr.20050724075352.18:processRectangle
            #@+node:ekr.20050724075352.19:processAbbreviation
            def processAbbreviation (self,event):
            
                b = self ; char = event.char
            
                if b.get() != 'a' and event.keysym == 'a':
                    b.set('a')
                    return 'break'
            
                elif b.get() == 'a':
                    if char == 'i':
                        b.set('a i')
                    elif char == 'e':
                        b.stopControlX(event)
                        event.char = ''
                        self.emacs.expandAbbrev(event)
                    return 'break'
            #@nonl
            #@-node:ekr.20050724075352.19:processAbbreviation
            #@-others
        #@nonl
        #@-node:ekr.20050724075352.14:class controlX_handlerClass
        #@+node:ekr.20050724075352.29:class keyStrokeManagerClass
        class keyStrokeManagerClass:
        
            #@    @+others
            #@+node:ekr.20050724075352.30:__init__
            def __init__ (self,emacs):
            
                self.emacs = emacs
            
                self.keystrokes = {} # Defined later by finishCreate.
            #@nonl
            #@-node:ekr.20050724075352.30:__init__
            #@+node:ekr.20050724075352.32:__call__ (keyboard manager)
            def __call__ (self,event,stroke):
            
                numberOfArgs, func = self.keystrokes [stroke]
            
                if numberOfArgs == 1:
                    return func(event)
                else:
                    return func(event,stroke)
            #@nonl
            #@-node:ekr.20050724075352.32:__call__ (keyboard manager)
            #@+node:ekr.20050728103627.1:finishCreate TO BE REMOVED
            def finishCreate (self):
                
                emacs = self.emacs
                
                self.keystrokes = {
                    '<Control-s>':      ( 2, emacs.searchCommands.startIncremental ),
                    '<Control-r>':      ( 2, emacs.searchCommands.startIncremental ),
                    '<Alt-g>':          ( 1, emacs.editCommands.startGoto ),
                    '<Alt-z>':          ( 1, emacs.editCommands.startZap ),
                    '<Alt-percent>':    ( 1, emacs.queryReplaceCommands.masterQR ),
                    '<Control-Alt-w>':  ( 1, lambda event: 'break' ),
                }
            #@nonl
            #@-node:ekr.20050728103627.1:finishCreate TO BE REMOVED
            #@+node:ekr.20050724075352.33:hasKeyStroke
            def hasKeyStroke (self,stroke):
            
                return self.keystrokes.has_key(stroke)
            #@nonl
            #@-node:ekr.20050724075352.33:hasKeyStroke
            #@-others
        #@nonl
        #@-node:ekr.20050724075352.29:class keyStrokeManagerClass
        #@+node:ekr.20050724075352.20:class stateManagerClass
        class stateManagerClass:
            
            '''This class manages the state that the Emacs instance has entered and
               routes key events to the right method, dependent upon the state in the stateManagerClass'''
               
            #@    @+others
            #@+node:ekr.20050724075352.21:__init__
            def __init__ (self,emacs):
            
                self.emacs = emacs
                self.state = None
                self.states = {}
            #@nonl
            #@-node:ekr.20050724075352.21:__init__
            #@+node:ekr.20050724075352.23:__call__(state manager)
            def __call__ (self,*args):
            
                if self.state:
                    flag, func = self.stateCommands [self.state]
            
                    if flag == 1:
                        return func(args[0])
                    else:
                        return func(*args)
            #@nonl
            #@-node:ekr.20050724075352.23:__call__(state manager)
            #@+node:ekr.20050725112958:finishCreate TO BE REMOVED
            def finishCreate (self):
            
                emacs = self.emacs
            
                # EKR: used only below.
                def eA (event):
                    if self.emacs.expandAbbrev(event):
                        return 'break'
            
                self.stateCommands = { 
                    # 1 == one parameter, 2 == all
                    
                    # Utility states...
                    'getArg':    (2,emacs.miniBuffer.getArg),
                    
                    # Command states...
                    'uC':               (2,emacs.miniBuffer.universalDispatch),
                    'controlx':         (2,emacs.miniBuffer.doControlX),
                    'isearch':          (2,emacs.searchCommands.iSearch),
                    'goto':             (1,emacs.editCommands.Goto),
                    'zap':              (1,emacs.editCommands.zapTo),
                    'howM':             (1,emacs.editCommands.howMany),
                    'abbrevMode':       (1,emacs.abbrevCommands.abbrevCommand1),
                    'altx':             (1,emacs.miniBuffer.doAlt_X),
                    'qlisten':          (1,emacs.queryReplaceCommands.masterQR),
                    'rString':          (1,emacs.editCommands.replaceString),
                    'negativeArg':      (2,emacs.miniBuffer.negativeArgument),
                    'abbrevOn':         (1,eA),
                    'set-fill-column':  (1,emacs.editCommands.setFillColumn),
                    'chooseBuffer':     (1,emacs.bufferCommands.chooseBuffer),
                    'renameBuffer':     (1,emacs.bufferCommands.renameBuffer),
                    're_search':        (1,emacs.searchCommands.re_search),
                    'alterlines':       (1,emacs.editCommands.processLines),
                    'make_directory':   (1,emacs.fileCommands.makeDirectory),
                    'remove_directory': (1,emacs.fileCommands.removeDirectory),
                    'delete_file':      (1,emacs.fileCommands.deleteFile),
                    'nonincr-search':   (2,emacs.searchCommands.nonincrSearch),
                    'word-search':      (1,emacs.searchCommands.wordSearch),
                    'last-altx':        (1,emacs.miniBuffer.executeLastAltX),
                    'escape':           (1,emacs.editCommands.watchEscape),
                    'subprocess':       (1,emacs.emacsControlCommands.subprocesser),
                }
            #@-node:ekr.20050725112958:finishCreate TO BE REMOVED
            #@+node:ekr.20050724075352.24:setState
            def setState (self,state,value):
            
                self.state = state
                self.states [state] = value
            #@nonl
            #@-node:ekr.20050724075352.24:setState
            #@+node:ekr.20050724075352.25:getState
            def getState (self,state):
            
                return self.states.get(state,False)
            #@nonl
            #@-node:ekr.20050724075352.25:getState
            #@+node:ekr.20050724075352.26:hasState
            def hasState (self):
            
                if self.state:
                    return self.states [self.state]
            #@nonl
            #@-node:ekr.20050724075352.26:hasState
            #@+node:ekr.20050724075352.27:whichState
            def whichState (self):
            
                return self.state
            #@nonl
            #@-node:ekr.20050724075352.27:whichState
            #@+node:ekr.20050724075352.28:clear
            def clear (self):
            
                self.state = None
            
                for z in self.states.keys():
                    self.states [z] = 0 # More useful than False.
            #@nonl
            #@-node:ekr.20050724075352.28:clear
            #@-others
        #@nonl
        #@-node:ekr.20050724075352.20:class stateManagerClass
        #@+node:ekr.20050724075352.242:ControlX methods
        #@+node:ekr.20050724075352.243:startControlX
        def startControlX (self,event):
        
            '''This method starts the Control-X command sequence.'''
            
            b = self
        
            b.setState('controlx',True)
            b.set('Control - X')
            b.setLabelBlue()
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.243:startControlX
        #@+node:ekr.20050724075352.244:stopControlX
        def stopControlX (self,event): # event IS used.
        
            '''This method clears the state of the Emacs instance'''
            
            b = self ; emacs = self.emacs ; widget = event.widget
        
            # This will all be migrated to keyboardQuit eventually.
            if emacs.emacsControlCommands.shuttingdown:
                return
        
            emacs.rectangleCommands.sRect = False
            emacs.registerCommands.rectanglemode = 0
            
            b.stateManager.clear()
            widget.tag_delete('color')
            widget.tag_delete('color1')
        
            if emacs.registerCommands.registermode:
                emacs.registerCommands.deactivateRegister(event)
        
            self.bufferMode = None ### Correct???
            b.reset()
            widget.update_idletasks()
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.244:stopControlX
        #@+node:ekr.20050724075352.245:doControlX
        def doControlX (self,event,stroke,previous=[]):
        
            return self.cxHandler(event,stroke)
        #@nonl
        #@-node:ekr.20050724075352.245:doControlX
        #@-node:ekr.20050724075352.242:ControlX methods
        #@+node:ekr.20050724075352.115:extendAltX
        def extendAltX (self,name,function):
        
            '''A simple method that extends the functions Alt-X offers.'''
        
            # Important: f need not be a method of the emacs class.
            
            b = self
        
            def f (event,aX=None,self=self,command=function):
                # g.trace(event,self,command)
                command()
                b.keyboardQuit(event)
        
            b.altX_commandsDict [name] = f
        #@nonl
        #@-node:ekr.20050724075352.115:extendAltX
        #@+node:ekr.20050730074556.3:getArg
        def getArg (self,event,returnStateKind=None,returnState=None):
            
            '''Handle key state while accumulating an argument. Enter given state when done'''
            
            b = self ; stateKind = 'getArg'
            state = b.getState(stateKind)
            if not state:
                b.argPromptLen = len(b.get()) ; b.arg = ''
                b.afterGetArgState = (returnStateKind,returnState)
                b.setState(stateKind,1)
            elif event.keysym == 'Return':
                # Compute the actual arg.
                s = b.get() ; b.arg = s[b.argPromptLen:]
                # Immediately enter the caller's requested state.
                b.stateManager.clear()
                stateKind,state = self.afterGetArgState
                b.setState(stateKind,state)
                b.stateManager(event,None) # Invoke the stateManager __call__ method.
            else:
                b.update(event)
            return 'break'
        #@nonl
        #@-node:ekr.20050730074556.3:getArg
        #@+node:ekr.20050724075352.47:keyboardQuit
        def keyboardQuit (self,event):  # The event arg IS used.
        
            '''This method cleans the Emacs instance of state and ceases current operations.'''
        
            return self.stopControlX(event) # This method will eventually contain the stopControlX code.
        #@nonl
        #@-node:ekr.20050724075352.47:keyboardQuit
        #@+node:ekr.20050724075352.89:manufactureKeyPress
        def manufactureKeyPress (self,event,which): # event IS used.
        
            tbuffer = event.widget
            tbuffer.event_generate('<Key>',keysym=which)
            tbuffer.update_idletasks()
            
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.89:manufactureKeyPress
        #@+node:ekr.20050724075352.43:masterCommand
        def masterCommand (self,event,method,stroke):
            '''The masterCommand is the central routing method of the Emacs method.
               All commands and keystrokes pass through here.'''
        
            special = event.keysym in ('Control_L','Control_R','Alt_L','Alt-R','Shift_L','Shift_R')
            inserted = not special or len(self.keysymhistory) == 0 or self.keysymhistory [0] != event.keysym
        
            # Don't add multiple special characters to history.
            if inserted:
                self.keysymhistory.insert(0,event.keysym)
                if len(event.char) > 0:
                    if len(Emacs.lossage) > 99: Emacs.lossage.pop()
                    Emacs.lossage.insert(0,event.char)
                #@        << traces >>
                #@+node:ekr.20050729150051:<< traces >>
                if 0: # traces
                    g.trace(event.keysym,stroke)
                    #g.trace(self.keysymhistory)
                    #g.trace(Emacs.lossage)
                #@nonl
                #@-node:ekr.20050729150051:<< traces >>
                #@nl
        
            if self.emacs.macroCommands.macroing:
                #@        << handle macro >>
                #@+node:ekr.20050729150051.1:<< handle macro >>
                if self.emacs.macroCommands.macroing == 2 and stroke != '<Control-x>':
                    return self.nameLastMacro(event)
                elif self.emacs.macroCommands.macroing == 3 and stroke != '<Control-x>':
                    return self.getMacroName(event)
                else:
                   self.recordKBDMacro(event,stroke)
                #@nonl
                #@-node:ekr.20050729150051.1:<< handle macro >>
                #@nl
        
            if stroke == '<Control-g>':
                self.previousStroke = stroke
                return self.keyboardQuit(event)
        
            if self.stateManager.hasState():
                self.previousStroke = stroke
                return self.stateManager(event,stroke) # EKR: Invoke the __call__ method.
        
            if self.kstrokeManager.hasKeyStroke(stroke):
                self.previousStroke = stroke
                return self.kstrokeManager(event,stroke) # EKR: Invoke the __call__ method.
        
            if self.emacs.regXRpl: # EKR: a generator.
                try:
                    self.emacs.regXKey = event.keysym
                    self.emacs.regXRpl.next() # EKR: next() may throw StopIteration.
                finally:
                    return 'break'
        
            if self.emacs.abbrevOn:
                if self.emacs.abbrevCommands._expandAbbrev(event):
                    return 'break'
        
            if method:
                rt = method(event)
                self.previousStroke = stroke
                return rt
        #@nonl
        #@-node:ekr.20050724075352.43:masterCommand
        #@+node:ekr.20050724075352.75:negativeArgument
        def negativeArgument (self,event,stroke=None):
        
            b = self
            
            b.set("Negative Argument")
            b.setLabelBlue()
        
            state = b.getState('negativeArg')
            if state == 0:
                b.setState('negativeArg',1)
            else:
                if self.negArgs.has_key(stroke):
                    self.negArgs [stroke](event,stroke)
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.75:negativeArgument
        #@+node:ekr.20050724075352.106:tailEnd methods
        #@+node:ekr.20050724075352.107:_tailEnd
        def _tailEnd (self,tbuffer):
            
            '''This returns the tailEnd function that has been configure for the tbuffer parameter.'''
            
            func = self.tailEnds.get(tbuffer)
            if func:
                # g.trace(func)
                return func(tbuffer)
            else:
                return 'break'
        #@-node:ekr.20050724075352.107:_tailEnd
        #@+node:ekr.20050724075352.108:setTailEnd
        def setTailEnd (self,tbuffer,tailCall):
        
            '''This method sets a ending call that is specific for a particular Text widget.
               Some environments require that specific end calls be made after a keystroke
               or command is executed.'''
        
            self.tailEnds [tbuffer] = tailCall
        #@-node:ekr.20050724075352.108:setTailEnd
        #@-node:ekr.20050724075352.106:tailEnd methods
        #@+node:ekr.20050724075352.289:universal dispatch methods
        #@+others
        #@+node:ekr.20050724075352.290:universalDispatch
        def universalDispatch (self,event,stroke):
        
            b = self
            
            state = b.getState('uC')
            if state == 0:
                b.setState('uC',1)
                b.set('')
                b.setLabelBlue()
            elif state == 1:
                b.universalCommand1(event,stroke)
            elif state == 2:
                b.universalCommand3(event,stroke)
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.290:universalDispatch
        #@+node:ekr.20050724075352.291:universalCommand1
        def universalCommand1 (self,event,stroke):
            
            b = self
        
            if event.char not in b.uCstring:
                return b.universalCommand2(event,stroke)
         
            b.update(event)
        
            if event.char != '\b':
                b.set('%s ' % b.get())
        #@nonl
        #@-node:ekr.20050724075352.291:universalCommand1
        #@+node:ekr.20050724075352.292:universalCommand2
        def universalCommand2 (self,event,stroke):
            
            b = self ; tbuffer = event.widget # event IS used.
            txt = b.get()
            b.keyboardQuit(event)
            txt = txt.replace(' ','')
            b.reset()
            if not txt.isdigit():
                # This takes us to macro state.
                # For example Control-u Control-x ( will execute the last macro and begin editing of it.
                if stroke == '<Control-x>':
                    b.setState('uC',2)
                    return b.universalCommand3(event,stroke)
                return b._tailEnd(event.widget)
            if b.uCdict.has_key(stroke): # This executes the keystroke 'n' number of times.
                b.uCdict [stroke](event,txt)
            else:
                i = int(txt)
                stroke = stroke.lstrip('<').rstrip('>')
                if b.cbDict.has_key(stroke):
                    for z in xrange(i):
                        method = self.cbDict [stroke]
                        ev = Tk.Event()
                        ev.widget = event.widget
                        ev.keysym = event.keysym
                        ev.keycode = event.keycode
                        ev.char = event.char
                        b.masterCommand(ev,method,'<%s>' % stroke)
                else:
                    for z in xrange(i):
                        tbuffer.event_generate('<Key>',keycode=event.keycode,keysym=event.keysym)
                        b._tailEnd(tbuffer)
        #@-node:ekr.20050724075352.292:universalCommand2
        #@+node:ekr.20050724075352.293:universalCommand3
        def universalCommand3 (self,event,stroke):
            
            b = self
            b.set('Control-u %s' % stroke.lstrip('<').rstrip('>'))
            b.setLabelBlue()
        
            if event.keysym == 'parenleft':
                b.keyboardQuit(event)
                b.emacs.macroCommands.startKBDMacro(event)
                b.emacs.macroCommands.executeLastMacro(event)
                return 'break'
        #@nonl
        #@-node:ekr.20050724075352.293:universalCommand3
        #@+node:ekr.20050724075352.294:numberCommand
        def numberCommand (self,event,stroke,number): # event IS used.
        
            self.universalDispatch(event,stroke)
            event.widget.event_generate('<Key>',keysym=number)
        
            return 'break'
        #@nonl
        #@-node:ekr.20050724075352.294:numberCommand
        #@-others
        #@nonl
        #@-node:ekr.20050724075352.289:universal dispatch methods
        #@-others
    #@nonl
    #@-node:ekr.20050727161004:class miniBufferClass 
    #@+node:ekr.20050724075352.34:class Tracker (an iterator)
    class Tracker:
    
        '''A class designed to allow the user to cycle through a list
           and to change the list as deemed appropiate.'''
    
        #@    @+others
        #@+node:ekr.20050724075352.35:init
        def __init__ (self):
            
            self.tablist = []
            self.prefix = None 
            self.ng = self._next()
        #@nonl
        #@-node:ekr.20050724075352.35:init
        #@+node:ekr.20050724075352.36:setTabList
        def setTabList (self,prefix,tlist):
            
            self.prefix = prefix 
            self.tablist = tlist 
        #@nonl
        #@-node:ekr.20050724075352.36:setTabList
        #@+node:ekr.20050724075352.37:_next
        def _next (self):
            
            while 1:
                tlist = self.tablist 
                if not tlist:yield ''
                for z in self.tablist:
                    if tlist!=self.tablist:
                        break 
                    yield z 
        #@nonl
        #@-node:ekr.20050724075352.37:_next
        #@+node:ekr.20050724075352.38:next
        def next (self):
            
            return self.ng.next()
        #@nonl
        #@-node:ekr.20050724075352.38:next
        #@+node:ekr.20050724075352.39:clear
        def clear (self):
        
            self.tablist = []
            self.prefix = None
        #@nonl
        #@-node:ekr.20050724075352.39:clear
        #@-others
    #@nonl
    #@-node:ekr.20050724075352.34:class Tracker (an iterator)
    #@-others
#@nonl
#@-node:ekr.20050724075352.40:class Emacs
#@-others
#@nonl
#@-node:ekr.20050723062822:@thin __core_emacs.py
#@-leo
