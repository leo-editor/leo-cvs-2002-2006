<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet ekr_stylesheet?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="179" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="112" left="469" height="600" width="800"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="ekr.20060301122644" a="V"><vh>Buttons</vh>
<v t="ekr.20060301122618"><vh>@button Unit Test</vh></v>
<v t="ekr.20060301122644.1"><vh>@button Save</vh></v>
</v>
<v t="ekr.20051208082927"><vh>ut.leo</vh>
<v t="ekr.20051208083135"><vh>@asis ut.bat</vh></v>
<v t="ekr.20060124103819"><vh>@asis utw.bat</vh></v>
<v t="ekr.20051208084010"><vh>@thin ut.py</vh></v>
</v>
<v t="ekr.20060129090836"><vh>@ignore</vh>
<v t="ekr.20051208085841.1"><vh>@test assert False</vh></v>
<v t="ekr.20060129185431"><vh>@test k.strokeFromEvent and k.strokeFromSetting</vh></v>
<v t="ekr.20051208085841"><vh>@test 1</vh></v>
<v t="ekr.20060208071636"><vh>Test headline abc</vh></v>
</v>
<v t="ekr.20051208082927.1"><vh>Unit Tests</vh>
<v t="ekr.20060301122407"><vh>NewHeadline</vh></v>
<v t="ekr.20060203202239" annotate="7d71002e"><vh>@test restore the screen</vh></v>
</v>
<v t="ekr.20060301122407.1" a="E"><vh>Mini tests of chapters</vh>
<v t="ekr.20060301120746"><vh>@ test addChapter</vh></v>
<v t="ekr.20060301121525"><vh>@@test removeOneChapter</vh></v>
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
<t tx="ekr.20060208071636"></t>
<t tx="ekr.20060301120746">import chapters2
cc = chapters2.controllers.get(c)
cc.addChapter()</t>
<t tx="ekr.20060301121525">import chapters2 as ch
cc = ch.controllers.get(c)

oldLast = cc.nb.pagenames()[-1]
cc.addChapter()
name = cc.nb.pagenames()[-1]
cc.removeOneChapter(name=name)
assert oldLast == cc.nb.pagenames()[-1]</t>
<t tx="ekr.20060301122407"></t>
<t tx="ekr.20060301122407.1">The chapters code does nothing for unit tests, so we can't use @test here.</t>
<t tx="ekr.20060301122618"># You can run unit tests by selecting an outline containing unit tests.

import leoTest

leoTest.doTests(c,all=False)</t>
<t tx="ekr.20060301122644"></t>
<t tx="ekr.20060301122644.1">c.save()
c.redraw_now() # Must be done here.</t>
</tnodes>
</leo_file>
