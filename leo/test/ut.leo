<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet ekr_stylesheet?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="3" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="239" left="393" height="600" width="800"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="ekr.20060124194018"><vh>@button Unit Test</vh></v>
<v t="ekr.20051208082927" a="E"><vh>ut.leo</vh>
<v t="ekr.20051208083135"><vh>@asis ut.bat</vh></v>
<v t="ekr.20060124103819"><vh>@asis utw.bat</vh></v>
<v t="ekr.20051208084010"><vh>@thin ut.py</vh></v>
</v>
<v t="ekr.20060129090836" a="E"><vh>@ignore</vh>
<v t="ekr.20051208085841.1" a="E"><vh>@test assert False</vh></v>
<v t="ekr.20060124085038"><vh>New find tests</vh>
<v t="ekr.20060124085038.1"><vh>@test togle find options commands</vh></v>
<v t="ekr.20060124085038.2"><vh>@test set find mode commands</vh></v>
<v t="ekr.20060124193802"><vh>@test minbuffer find commands</vh></v>
<v t="ekr.20060125075332"><vh>@test show-find-options</vh></v>
</v>
</v>
<v t="ekr.20051208082927.1" a="E"><vh>Unit Tests</vh>
<v t="ekr.20051208085841"><vh>@test 1</vh></v>
<v t="ekr.20060129090836.1"><vh>@@test k.strokeFromEvent</vh></v>
<v t="ekr.20060129185431" a="V"><vh>@test k.strokeFromEvent and k.strokeFromSetting</vh></v>
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
<t tx="ekr.20060124085038"># Reference c.k.simulateCommand('command')</t>
<t tx="ekr.20060124085038.1">table = (
    # 'toggle-find-clone-find-all-option',
    'toggle-find-ignore-case-option',
    'toggle-find-in-body-option',
    'toggle-find-in-headline-option',
    'toggle-find-mark-changes-option',
    'toggle-find-mark-finds-option',
    'toggle-find-regex-option',
    'toggle-find-reverse-option',
    'toggle-find-word-option',
    'toggle-find-wrap-around-option',
)

for command in table:
    c.k.simulateCommand(command)
    c.k.simulateCommand(command)
    </t>
<t tx="ekr.20060124085038.2">table = (
    'set-find-everywhere',
    'set-find-node-only',
    'set-find-suboutline-only',
)

# show-find-tab-options     = Ctrl-o
# show-find-options         = o

for command in table:
    c.k.simulateCommand(command)
</t>
<t tx="ekr.20060124103819">cd c:\prog\leoCVS\leo\test
python ..\src\leo.py -script-window ..\test\ut.py</t>
<t tx="ekr.20060124193802">table = (
    're-search-forward',
    're-search-backward',
    'search-forward',
    'search-backward',
    'word-search-forward',
    'word-search-backward',
)

for command in table:
    c.k.simulateCommand(command)</t>
<t tx="ekr.20060124194018"># You can run unit tests by selecting an outline containing unit tests.

import leoTest

leoTest.doTests(c,all=False)</t>
<t tx="ekr.20060125075332">c.k.simulateCommand('show-find-options')</t>
<t tx="ekr.20060129090836"></t>
<t tx="ekr.20060129090836.1">import string
k = c.k ; key = 0 ; shift = 1 ; ctrl = 4 ; alt = 0x20000

# Important: shift is not in this list because Tk (probably) uses case to indicate shift.
# table = (key,alt,ctrl,shift,alt+shift,alt+ctrl,alt+shift+ctrl,ctrl+shift)
table = (key,alt,ctrl,alt,alt+ctrl)
for state in table:
    s = (state &amp; 1) == 1
    ct = (state &amp; 4) == 4
    a = (state &amp; 0x20000) == 0x20000
    
    print '-'*20,g.choose(a,'alt',''),g.choose(ct,'control',''),g.choose(s,'shift','')
 
    for char in string.printable:
        aList = [(a,'Alt+'),(ct,'Ctrl+')]
        keysym = k.tkBindNamesDict.get(char) or char
        event = g.Bunch(char=char,keysym=keysym,state=state)
        stroke,keysym2 = k.strokeFromEvent(event)
        print '%6s' % repr(char),repr(stroke)
        assert keysym2==keysym or ((a or ctrl) and keysym.upper()==keysym2),\
            'expected keysym %s, got %s' % (repr(keysym),repr(keysym2))
        for kind,tag in aList:
            assert kind and tag in stroke or not kind and not tag in stroke,\
                'tag mismatch.  tag: %s, stroke: %s' % (tag,stroke)</t>
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
        stroke2,keysym2 = k.strokeFromEvent(event)
        assert stroke2==stroke,\
            'strokefromSetting: %s, strokeFromEvent: %s' % (repr(stroke),repr(stroke2))</t>
</tnodes>
</leo_file>
