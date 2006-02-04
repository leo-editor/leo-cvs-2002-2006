<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet ekr_stylesheet?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="153" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="134" left="252" height="600" width="800"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="ekr.20060130151821"><vh>Buttons</vh>
<v t="ekr.20060124194018"><vh>@button Unit Test</vh></v>
<v t="ekr.20060130151821.1"><vh>@button Save</vh></v>
</v>
<v t="ekr.20060131110151" annotate="7d71002e"><vh>@command unit-test-command1</vh></v>
<v t="ekr.20051208082927"><vh>ut.leo</vh>
<v t="ekr.20051208083135"><vh>@asis ut.bat</vh></v>
<v t="ekr.20060124103819"><vh>@asis utw.bat</vh></v>
<v t="ekr.20051208084010"><vh>@thin ut.py</vh></v>
</v>
<v t="ekr.20060129090836"><vh>@ignore</vh>
<v t="ekr.20051208085841.1"><vh>@test assert False</vh></v>
<v t="ekr.20060129185431"><vh>@test k.strokeFromEvent and k.strokeFromSetting</vh></v>
</v>
<v t="ekr.20051208082927.1" a="EV"><vh>Unit Tests</vh>
<v t="ekr.20051208085841"><vh>@test 1</vh></v>
<v t="ekr.20060131110108" annotate="7d71002e"><vh>Commands tests</vh>
<v t="ekr.20060131110108.1" annotate="7d71002e"><vh>@test of c.executeMinibufferCommand and @command</vh></v>
<v t="ekr.20060131110108.3" annotate="7d71002e"><vh>@test Save command redraws the screen</vh></v>
<v t="ekr.20060131110108.4" annotate="7d71002e"><vh>@test New command redraws the screen</vh></v>
</v>
<v t="ekr.20060203192029.1" annotate="7d71002e"><vh>Unit tests for typing</vh>
<v t="ekr.20060203192029.2" annotate="7d71002e"><vh>@test make sure the window is visible (Make this the first test)</vh></v>
<v t="ekr.20060203192029.4" annotate="7d71002e"><vh>Test headline abc</vh></v>
<v t="ekr.20060203192029.9" annotate="7d71002e"><vh>Typing and undo tests</vh>
<v t="ekr.20060203192029.10" annotate="7d71002e"><vh>@test return ends editing of headline</vh></v>
<v t="ekr.20060203192029.12" annotate="7d71002e"><vh>@test paste at end of headline</vh></v>
<v t="ekr.20060203192029.13" annotate="7d71002e"><vh>@test typing and undo in headline - at end</vh></v>
<v t="ekr.20060203192029.14" annotate="7d71002e"><vh>@test paste and undo in headline - at end</vh></v>
<v t="ekr.20060203192029.15" annotate="7d71002e"><vh>@test paste and undo in headline - with selection</vh></v>
<v t="ekr.20060203192029.16" annotate="7d71002e"><vh>@test selecting new node retains typing in headline</vh></v>
<v t="ekr.20060203192029.17" annotate="7d71002e"><vh>@test paste from menu into body sticks</vh></v>
<v t="ekr.20060203192029.18" annotate="7d71002e"><vh>@test paste from menu into headline sticks</vh></v>
<v t="ekr.20060203192029.20" annotate="7d71002e"><vh>@test typing in headline recomputes width</vh></v>
<v t="ekr.20060203192029.21" annotate="7d71002e"><vh>@test selecting new node retains paste in headline</vh></v>
<v t="ekr.20060203192029.22" annotate="7d71002e"><vh>@test typing in empty body text redraws the screen (and icon)</vh></v>
<v t="ekr.20060203192029.27" annotate="7d71002e"><vh>@test &lt;Delete&gt; key sticks in body</vh></v>
<v t="ekr.20060203192029.28" annotate="7d71002e"><vh>@test &lt;Delete&gt; key sticks in headline</vh></v>
<v t="ekr.20060203192029.29"><vh>print end of typing and undo tests</vh></v>
</v>
</v>
<v t="ekr.20060203202239" annotate="7d71002e"><vh>@test restore the screen</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="ekr.20051208082927">@ This file is called from ut.batch.

It should contain quick unit tests to be run in Leo's batch mode.

It also defines ut.bat itself.</t>
<t tx="ekr.20051208082927.1"></t>
<t tx="ekr.20051208083135">cd c:\prog\leoCVS\leo\test
python ..\src\leo.py -script ..\test\ut.py</t>
<t tx="ekr.20051208085841">assert True</t>
<t tx="ekr.20051208085841.1">assert False,'This should fail'</t>
<t tx="ekr.20060124103819">cd c:\prog\leoCVS\leo\test
python ..\src\leo.py -script-window ..\test\ut.py</t>
<t tx="ekr.20060124194018"># You can run unit tests by selecting an outline containing unit tests.

import leoTest

leoTest.doTests(c,all=False)</t>
<t tx="ekr.20060129090836"></t>
<t tx="ekr.20060129185431">import string
k = c.k ; key = 0 ; shift = 1 ; ctrl = 4 ; alt = 0x20000

prefixes = (
    ('',0),('Alt-',alt),('Ctrl-',ctrl),
    ('Shift-',shift),('Alt-Shift-',alt+shift),('Alt-Ctrl-',alt+ctrl),
)

for prefix,state in prefixes:
    for ch in string.printable:
        if prefix.find('Shift-') &gt; -1 and ch not in string.letters:
            continue # The shift would be ignored.
        ch2 = k.tkBindNamesDict.get(ch) or ch
        setting = prefix + ch2
        stroke = k.strokeFromSetting(setting)
        if not stroke: continue
        if (shift &amp; state) != 0: ch = ch.upper()
        event = g.Bunch(char=ch,keysym=ch,state=state)
        stroke2 = k.strokeFromEvent(event)
        assert stroke2==stroke,\
            'strokefromSetting: %s, strokeFromEvent: %s' % (repr(stroke),repr(stroke2))</t>
<t tx="ekr.20060130151821"></t>
<t tx="ekr.20060130151821.1">c.save()</t>
<t tx="ekr.20060131110108"></t>
<t tx="ekr.20060131110108.1">g.app.unitTestDict = {}
c.executeMinibufferCommand('unit-test-command1')
assert g.app.unitTestDict.get('unit-test-command1') == True</t>
<t tx="ekr.20060131110108.3">c.redraw_now() # To make node visible
k = c.k
n = c.frame.tree.redrawCount
k.simulateCommand('save-file')
assert c.frame.tree.redrawCount &gt; n</t>
<t tx="ekr.20060131110108.4">k = c.keyHandler
k.simulateCommand('new')
c2 = k.funcReturn
try:
    assert c2
    assert c and c != c2
    assert c2.frame.tree.redrawCount &gt; 0
finally:
    if c2: c2.close()</t>
<t tx="ekr.20060131110151">g.es_print('Test of @command')
g.app.unitTestDict ['unit-test-command1'] = True</t>
<t tx="ekr.20060203192029.1"></t>
<t tx="ekr.20060203192029.2">c.frame.bringToFront()
c.frame.body.bodyCtrl.update()</t>
<t tx="ekr.20060203192029.4"></t>
<t tx="ekr.20060203192029.9"></t>
<t tx="ekr.20060203192029.10">import leoTest ; u = leoTest.testUtils(c)

h = '@test return ends editing of headline'
p = u.findNodeAnywhere(h)
c.selectPosition(p)
c.redraw_now() # To make node visible
c.frame.tree.editLabel(p)
w = p.edit_widget()
w2 = g.app.gui.get_focus(c.frame)
assert w == w2, 'oops1 %s != %s' % (w,w2)
w.event_generate('&lt;Return&gt;')
assert w != g.app.gui.get_focus(c.frame),'oops2' ##</t>
<t tx="ekr.20060203192029.12">import leoTest ; u = leoTest.testUtils(c)
k = c.keyHandler
frame = c.frame ; tree = frame.tree ; canvas = tree.canvas
h = 'Test headline abc'
p = u.findNodeAnywhere(h)
c.selectPosition(p)
c.redraw_now() # To make node visible
tree.editLabel(p)
w = p.edit_widget()
try:
    assert w,'oops1'
    paste = 'ABC'
    g.app.gui.replaceClipboardWith(paste)
    g.app.gui.setSelectionRange(w,'end','end')
    k.manufactureKeyPressForCommandName(w,'paste-text')
    w.event_generate('&lt;Return&gt;')
    assert p.headString() == h + paste,'oops2'
finally:
    if 1:
        p.initHeadString(h)
        c.redraw_now()</t>
<t tx="ekr.20060203192029.13">import leoTest ; u = leoTest.testUtils(c)
k = c.keyHandler
frame = c.frame ; tree = frame.tree ; canvas = tree.canvas
h = 'Test headline abc'
p = u.findNodeAnywhere(h)
c.selectPosition(p)
c.redraw_now() # To make node visible
tree.editLabel(p)
w = p.edit_widget()
try:
    assert w
    g.app.gui.setSelectionRange(w,'end','end')
    w.event_generate('X')
    w.event_generate('Y')
    w.event_generate('Z')
    w.event_generate('&lt;Return&gt;')
    assert p.headString() == h + 'XYZ'
    assert c.undoer.undoMenuLabel == 'Undo Typing'
    k.manufactureKeyPressForCommandName(w,'undo')
    assert c.undoer.redoMenuLabel == 'Redo Typing'
    assert p.headString() == h
finally:
    if 1:
        p.initHeadString(h)
        c.redraw_now()</t>
<t tx="ekr.20060203192029.14">import leoTest ; u = leoTest.testUtils(c)
k = c.keyHandler
frame = c.frame ; tree = frame.tree ; canvas = tree.canvas
h = 'Test headline abc'
p = u.findNodeAnywhere(h)
c.selectPosition(p)
c.redraw_now() # To make node visible
tree.editLabel(p)
w = p.edit_widget()
try:
    assert w
    g.app.gui.setSelectionRange(w,'end','end')
    paste = 'ABC'
    g.app.gui.replaceClipboardWith(paste)
    g.app.gui.setSelectionRange(w,'end','end')
    k.manufactureKeyPressForCommandName(w,'paste-text')
    w.event_generate('&lt;Return&gt;')
    assert p.headString() == h + paste
    k.manufactureKeyPressForCommandName(w,'undo')
    assert p.headString() == h
finally:
    if 1:
        p.initHeadString(h)
        c.redraw_now()</t>
<t tx="ekr.20060203192029.15">import leoTest ; u = leoTest.testUtils(c)
k = c.keyHandler
frame = c.frame ; tree = frame.tree ; canvas = tree.canvas
h = 'Test headline abc'
p = u.findNodeAnywhere(h)
c.selectPosition(p)
c.redraw_now() # To make node visible
tree.editLabel(p)
w = p.edit_widget()
try:
    assert w
    paste = 'ABC'
    g.app.gui.replaceClipboardWith(paste)
    g.app.gui.setSelectionRange(w,'1.1','1.2')
    k.manufactureKeyPressForCommandName(w,'paste-text')
    w.event_generate('&lt;Return&gt;')
    assert p.headString() == h[0] + paste + h[2:]
    k.manufactureKeyPressForCommandName(w,'undo')
    assert p.headString() == h
finally:
    if 1:
        p.initHeadString(h)
        c.redraw_now()</t>
<t tx="ekr.20060203192029.16">import leoTest ; u = leoTest.testUtils(c)
k = c.keyHandler
frame = c.frame ; tree = frame.tree ; canvas = tree.canvas
h = 'Test headline abc'
p = u.findNodeAnywhere(h)
c.selectPosition(p)
c.redraw_now() # To make node visible
tree.editLabel(p)
w = p.edit_widget()
try:
    assert w
    g.app.gui.setSelectionRange(w,'end','end')
    w.event_generate('X')
    w.event_generate('Y')
    w.event_generate('Z')
    w.event_generate('&lt;Return&gt;')
    assert p.headString() == h + 'XYZ'
    k.manufactureKeyPressForCommandName(w,'undo')
    assert p.headString() == h
finally:
    if 1:
        p.initHeadString(h)
        c.redraw_now()</t>
<t tx="ekr.20060203192029.17">import leoTest ; u = leoTest.testUtils(c)
h = 'Test headline abc'
p = u.findNodeAnywhere(h)
assert p,'oops: no p'
# Post by hand.
menu = c.frame.menu.getMenu('Edit')
i = menu.index('Paste')
c.selectPosition(p)
c.frame.bodyWantsFocus()
paste = 'ABC'
g.app.gui.replaceClipboardWith(paste)
menu.invoke(i)
# Move around and and make sure it doesn't change.
try:
    assert p.bodyString() == paste,'oops1'
    c.selectPosition(p.threadBack())
    assert p.bodyString() == paste,'oops2'
    c.selectPosition(p)
    assert p.bodyString() == paste,'oops3'
finally:
    if 1:
        p.setBodyString('')
        c.redraw_now()
</t>
<t tx="ekr.20060203192029.18">import leoTest ; u = leoTest.testUtils(c)
h = 'Test headline abc'
p = u.findNodeAnywhere(h)
# Post by hand.
menu = c.frame.menu.getMenu('Edit')
i = menu.index('Paste')
c.selectPosition(p)
c.frame.tree.editLabel(p)
w = p.edit_widget()
g.app.gui.setSelectionRange(w,'end','end')
paste = 'ABC'
g.app.gui.replaceClipboardWith(paste)
menu.invoke(i)
# Move around and and make sure it doesn't change.
try:
    c.selectPosition(p.threadBack())
    assert p.headString() == h + paste
    c.selectPosition(p)
    assert p.headString() == h + paste
finally:
    if 1:
        p.setHeadString(h)
        c.redraw_now()</t>
<t tx="ekr.20060203192029.20">import leoTest ; u = leoTest.testUtils(c)
k = c.keyHandler
h = 'Test headline abc'
p = u.findNodeAnywhere(h)
c.selectPosition(p)
c.redraw_now() # To make node visible
c.frame.tree.editLabel(p)
w = p.edit_widget()
try:
    assert w
    g.app.gui.setSelectionRange(w,'end','end')
    n = w.cget('width')
    w.event_generate('X')
    w.event_generate('Y')
    w.event_generate('Z')
    n2 = w.cget('width')
    assert n2 &gt; n, '%s %s' % (n2,n)
    # g.trace(n,n2)
finally:
    if 1:
        p.initHeadString(h)
        c.redraw_now()</t>
<t tx="ekr.20060203192029.21">import leoTest ; u = leoTest.testUtils(c)
k = c.keyHandler
frame = c.frame ; tree = frame.tree ; canvas = tree.canvas
h = 'Test headline abc'
p = u.findNodeAnywhere(h)
c.selectPosition(p)
c.redraw_now() # To make node visible
tree.editLabel(p)
w = p.edit_widget()
try:
    assert w
    g.app.gui.setSelectionRange(w,'end','end')
    paste = 'ABC'
    g.app.gui.replaceClipboardWith(paste)
    g.app.gui.setSelectionRange(w,'end','end')
    k.manufactureKeyPressForCommandName(w,'paste-text')
    c.selectPosition(p.visBack())
    assert p.headString() == h + paste
    k.manufactureKeyPressForCommandName(w,'undo')
    assert p.headString() == h
finally:
    if 1:
        p.initHeadString(h)
        c.redraw_now()</t>
<t tx="ekr.20060203192029.22">import leoTest ; u = leoTest.testUtils(c)

h = 'Test headline abc'
p = u.findNodeAnywhere(h)
c.selectPosition(p)
c.redraw_now() # To make node visible
n = c.frame.tree.redrawCount
c.frame.bodyWantsFocus()
try:
    c.frame.body.bodyCtrl.event_generate('a')
    n2 = c.frame.tree.redrawCount
    assert n2 == n + 1,'too many or too few redraws: %d' % (n2-n)
finally:
    if 1:
        p.setBodyString('')
        c.redraw_now()</t>
<t tx="ekr.20060203192029.27">import leoTest ; u = leoTest.testUtils(c)
h = 'Test headline abc'
p = u.findNodeAnywhere(h)
assert(p)
c.selectPosition(p)
s = 'ABC'
p.setBodyString(s)
try:
    c.frame.bodyWantsFocus()
    w = c.frame.body.bodyCtrl
    w.mark_set('insert','1.2')
    w.event_generate('&lt;Delete&gt;')
    assert p.bodyString() == s[:-1]
    c.selectPosition(p.threadBack())
    c.selectPosition(p)
    assert p.bodyString() == s[:-1]
finally:
    if 1:
        p.setBodyString('')
        c.redraw_now()

</t>
<t tx="ekr.20060203192029.28">import leoTest ; u = leoTest.testUtils(c)
h = 'Test headline abc'
p = u.findNodeAnywhere(h)
c.selectPosition(p)
c.redraw_now() # To make node visible
c.frame.tree.editLabel(p)
w = p.edit_widget()
try:
    assert w
    g.app.gui.setSelectionRange(w,'end','end')
    # w.event_generate('X')
finally:
    if 1:
        p.initHeadString(h)
        c.redraw_now()</t>
<t tx="ekr.20060203192029.29">print ; print 'End of typing and undo tests'</t>
<t tx="ekr.20060203202239"># This is **not** a real unit test.
# It simply restores the screen to a more convenient state.
import leoTest ; u = leoTest.testUtils(c)

c.contractAllHeadlines()
h = 'Unit tests'
p = u.findNodeAnywhere(h)
if p:
    c.beginUpdate()
    try:
        p.expand()
        g.app.unitTestDict['restoreSelectedNode']=False
        c.selectPosition(p)
    finally:
        c.endUpdate()</t>
</tnodes>
</leo_file>
