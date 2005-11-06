<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet ekr_stylesheet?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="7813" clone_windows="0"/>
<globals body_outline_ratio="0.540216086435">
	<global_window_position top="79" left="313" height="833" width="872"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="ekr.20041001211817" annotate="7d71002e"><vh>Buttons &amp; settings</vh>
<v t="ekr.20051020124457"><vh>Disabled buttons</vh>
<v t="ekr.20041230121429"><vh>@@ button pydoc</vh></v>
<v t="ekr.20050210180937"><vh>@@ button jython</vh></v>
<v t="ekr.20050704170739"><vh>@@button Ipython</vh></v>
<v t="ekr.20050821072028"><vh>@@button Lines Up</vh>
<v t="ekr.20050821072028.1"><vh>moveLinesUp</vh></v>
</v>
<v t="ekr.20050821081021"><vh>@@button Lines Down</vh>
<v t="ekr.20050821081021.1" a="M"><vh>moveLinesDown</vh></v>
</v>
<v t="ekr.20050930124917"><vh>@@button outlineToClipboard</vh></v>
</v>
<v t="ekr.20041001194357"><vh>@button Unit Test</vh></v>
<v t="ekr.20051025070722"><vh>@button Beautify</vh></v>
<v t="ekr.20051105114247"><vh>@button scripts.leo</vh></v>
<v t="ekr.20051025091355"><vh>@button Spell</vh></v>
<v t="ekr.20050911112310"><vh>@button Save</vh></v>
</v>
<v t="ekr.20051104081824"><vh>Tests</vh>
<v t="ekr.20051017093427" a="E"><vh>Test of remove-blank-lines</vh></v>
<v t="ekr.20051103112555"><vh>Test of event_generate</vh></v>
<v t="ekr.20051104052708"><vh>Test of executing a function by name</vh></v>
</v>
<v t="ekr.20051105072540" a="E"><vh>New unit tests</vh>
<v t="ekr.20051105115732"><vh>Reference</vh>
<v t="ekr.20051105115732.1"><vh>manufactureKeyPressForCommandName</vh></v>
<v t="ekr.20051105155853"><vh>simulateCommand</vh></v>
</v>
<v t="ekr.20051105144609" a="E"><vh>Tests that pass</vh>
<v t="ekr.20051106033316"><vh>Test headline abc</vh></v>
<v t="ekr.20051106041531.1"><vh>@test of c.executeMinibufferCommand and @command</vh></v>
<v t="ekr.20051106033316.1"><vh>Redrawing after commands</vh>
<v t="ekr.20051105135920" a="E"><vh>@test Select a node when file is first loaded</vh></v>
<v t="ekr.20051105144920"><vh>@test Save command redraws the screen</vh></v>
<v t="ekr.20051105135429"><vh>@test New command redraws the screen</vh></v>
</v>
<v t="ekr.20051106033449"><vh>Typing and undo tests</vh>
<v t="ekr.20051105094834"><vh>@test return ends editing of headline</vh></v>
<v t="ekr.20051105081113" a="E"><vh>@test editLabel selects entire headline</vh></v>
<v t="ekr.20051105072702"><vh>@test paste at end of headline</vh></v>
<v t="ekr.20051105144713" a="E"><vh>@test typing and undo in headline - at end</vh></v>
<v t="ekr.20051106032745" a="E"><vh>@test paste and undo in headline - at end</vh></v>
<v t="ekr.20051105190211"><vh>@test typing and undo in headline - with selection</vh></v>
<v t="ekr.20051106034108"><vh>@test paste and undo in headline - with selection</vh></v>
<v t="ekr.20051106034342"><vh>@test selecting new node retains typing in headline</vh></v>
<v t="ekr.20051106111820" a="E"><vh>@test paste from menu into body sticks</vh></v>
<v t="ekr.20051106035939.1" a="E"><vh>@test paste from menu into headline sticks</vh></v>
<v t="ekr.20051106034823"><vh>@test paste from menu to body recolors the body</vh></v>
<v t="ekr.20051106034342.4"><vh>@test typing in headline recomputes width</vh></v>
<v t="ekr.20051106114543"><vh>@test paste in headline recomputes width</vh></v>
</v>
</v>
<v t="ekr.20051106043501"><vh>@test paste from minibuffer to body text</vh></v>
<v t="ekr.20051106034342.1"><vh>@test selecting new node retains paste in headline</vh></v>
<v t="ekr.20051106041531"><vh>@command unit-test-command1</vh></v>
<v t="ekr.20051105093945" a="E"><vh>@test Find keeps focus in body</vh></v>
<v t="ekr.20051105093945.1"><vh>@test Find keeps focus in headline</vh></v>
<v t="ekr.20051105165906"><vh>@test return in minibuffer after tab</vh></v>
<v t="ekr.20051106102656"><vh>@test plugins manager stays in front</vh></v>
<v t="ekr.20051106034823.1" a="MTV"><vh>@test inserting a node at the bottom scrolls headline (fails)</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="ekr.20041001194357"># You can run all tests by selecting the Unit Test headline.

import leoTest

leoTest.doTests(all=False)</t>
<t tx="ekr.20041001211817"></t>
<t tx="ekr.20041230121429">import os, sys, threading

python = sys.executable
pythonDir,junk = g.os_path_split(python)
pydoc = g.os_path_join(pythonDir,'Lib','pydoc.py')
command = '%s %s -g' % (python,pydoc)

# Execute the command in a separate thread.
def go():
    os.system(command)
    
threading.Thread(target=go).start()</t>
<t tx="ekr.20050210180937"># **** Change these as needed ***
import os, sys

tempFileName = g.os_path_abspath(
    g.os_path_join(g.app.testDir,'jythonScript.py'))

if sys.platform == 'win32':
    jython = r'C:\Jython-21\jython.bat'
    command = '%s "%s"' % (jython,tempFileName) 
else:
    jython = r'cd ~/jython-2.1 ; ./jython'
    command = '%s "%s" &amp;' % (jython,tempFileName)

script = g.getScript(c,p).strip()
if not script:
    s = "no script in %s" % p.headString()
    g.es(s) ; print s
else:
    f = file(tempFileName,'w')
    f.write(script + '\n')
    f.close()
    print command
    os.system(command)
</t>
<t tx="ekr.20050704170739">from IPython.Shell import IPShellEmbed

ipshell = IPShellEmbed()
ipshell()</t>
<t tx="ekr.20050821072028"># Move selected text of the body up one line.

@others

moveLinesUp(c,p)</t>
<t tx="ekr.20050821072028.1">def moveLinesUp(c,p):
    
    undoType = 'Move Lines Up'
    head,lines,tail,oldSel,oldYview = c.getBodyLines()
    if not head or not lines: return
    # A slight adjustment: lines doesn't end in '\n'.
    head = g.splitLines(head)
    lines = '\n'.join(lines) + '\n'
    lines = g.splitLines(lines)
    # Move the lines up.
    lines.append(head[-1])
    head = head[:-1]
    # Convert back to strings.
    head = ''.join(head)
    lines = ''.join(lines)[:-1] # Undo the adjustment above.
    # Adjust selection.
    sel1,sel2 = oldSel
    row,col = sel1.split('.') ; sel1 = '%d.%s' % (int(row)-1,col)
    row,col = sel2.split('.') ; sel2 = '%d.%s' % (int(row)-1,col)
    newSel = sel1,sel2
    c.updateBodyPane(head,lines,tail,undoType,newSel,oldYview)</t>
<t tx="ekr.20050821081021"># Move selected text of the body down one line.

@others

moveLinesDown(c,p)</t>
<t tx="ekr.20050821081021.1">def moveLinesDown(c,p):
    
    undoType = 'Move Lines Down'
    head,lines,tail,oldSel,oldYview = c.getBodyLines()
    if not tail or not lines: return
    tail = g.splitLines(tail)[1:]
    lines = '\n'.join(lines) + '\n'
    lines = g.splitLines(lines)
    # Move the lines down.
    lines.insert(0,tail[0])
    tail = tail[1:]
    if not tail: lines.insert(1,'\n')
    # Convert back to strings.
    tail = ''.join(tail)
    lines = ''.join(lines)
    # Adjust selection.
    sel1,sel2 = oldSel
    row,col = sel1.split('.') ; sel1 = '%d.%s' % (int(row)+1,col)
    row,col = sel2.split('.') ; sel2 = '%d.%s' % (int(row)+1,col)
    newSel = sel1,sel2
    c.updateBodyPane(head,lines,tail,undoType,newSel,oldYview)</t>
<t tx="ekr.20050911112310">c.save()</t>
<t tx="ekr.20050930124917">result = []
firstLevel = p.level()

for p in p.self_and_subtree_iter():
    head = p.moreHead(firstLevel)
    head = g.toEncodedString(head,'ascii',reportErrors=True)
    result.append(head)
    body = p.moreBody() # Inserts escapes for '+' and '-' characters.
    if body:
        body = g.toEncodedString(body,'ascii',reportErrors=True)
        result.append(body)

result = '\n'.join(result) + '\n'
# print result
w = c.frame.body.bodyCtrl
w.clipboard_clear()
w.clipboard_append(result)</t>
<t tx="ekr.20051017093427">a
 
b

c
d

e

This is a test of navigation.</t>
<t tx="ekr.20051020124457"></t>
<t tx="ekr.20051025070722">c.prettyPrintPythonNode()</t>
<t tx="ekr.20051025091355">c.spellCommands.openSpellTab()
</t>
<t tx="ekr.20051103112555">#w = event and event.widget
k = c.keyHandler

commandName = 'open-find-tab'
w = c.frame.body.bodyCtrl
    
shortcut = k.getShortcutForCommandName(commandName)
bind_shortcut, menu_shortcut = c.frame.menu.canonicalizeShortcut(shortcut)

g.trace(repr(shortcut),repr(bind_shortcut))
    
# w.event_generate('&lt;Key&gt;',keysym=bind_shortcut)</t>
<t tx="ekr.20051104052708">if 0:
    k = c.keyHandler ; event = None
    commandName = 'about-leo'
    func = c.commandsDict.get(commandName)
    forceFocus = func.__name__ != 'leoCallback'
    if forceFocus: k.forceFocusToBody()
    func(event)
    k.endCommand(event,commandName)
else:
    commandName = 'about-leo'
    func = c.commandsDict.get(commandName)
    func(event=None)</t>
<t tx="ekr.20051104081824"></t>
<t tx="ekr.20051105072540">
</t>
<t tx="ekr.20051105072702">import leoTest ; u = leoTest.testUtils()
k = c.keyHandler
frame = c.frame ; tree = frame.tree ; canvas = tree.canvas
h = 'Test headline abc'
p = u.findNodeAnywhere(c,h)
c.selectPosition(p)
c.redraw_now() # To make node visible
tree.editLabel(p)
w = p.edit_widget()
try:
    assert w
    paste = 'ABC'
    g.app.gui.replaceClipboardWith(paste)
    g.app.gui.setSelectionRange(w,'end','end')
    k.manufactureKeyPressForCommandName(w,'paste-text')
    w.event_generate('&lt;Return&gt;')
    assert p.headString() == h + paste
finally:
    p.initHeadString(h)
    c.redraw_now()</t>
<t tx="ekr.20051105081113">import leoTest ; u = leoTest.testUtils()

k = c.keyHandler
frame = c.frame ; tree = frame.tree ; canvas = tree.canvas
h = '@test editLabel selects entire headline'
p = u.findNodeAnywhere(c,h)
c.selectPosition(p)
c.redraw_now() # To make node visible
tree.editLabel(p)
w = p.edit_widget()
assert w
i,j = g.app.gui.getSelectionRange(w)
assert i == '1.0'
assert j == w.index('end')</t>
<t tx="ekr.20051105093945"></t>
<t tx="ekr.20051105093945.1"></t>
<t tx="ekr.20051105094834">import leoTest ; u = leoTest.testUtils()

h = '@test return ends editing of headline'
p = u.findNodeAnywhere(c,h)
c.selectPosition(p)
c.redraw_now() # To make node visible
c.frame.tree.editLabel(p)
w = p.edit_widget()
w2 = g.app.gui.get_focus(c.frame)
assert w == w2, 'oops1 %s != %s' % (w,w2)
w.event_generate('&lt;Return&gt;')
assert w != g.app.gui.get_focus(c.frame),'oops2'</t>
<t tx="ekr.20051105114247">name = "scripts.leo"
fileName = g.os_path_join(g.app.loadDir,"..","scripts",name)
ok,frame = g.openWithFileName(fileName,c)
if not ok:
    g.es("not found: %s" % name)</t>
<t tx="ekr.20051105115732"></t>
<t tx="ekr.20051105115732.1">def manufactureKeyPressForCommandName (self,w,commandName):
    
    '''Implement a command by passing a keypress to Tkinter.'''

    k = self
    
    shortcut = k.getShortcutForCommandName(commandName)
    
    if shortcut and w:
        w.event_generate(shortcut)
    else:
         g.trace('no shortcut for %s' % (commandName),color='red')</t>
<t tx="ekr.20051105135429">k = c.keyHandler
k.simulateCommand('new')
c2 = k.funcReturn
try:
    assert c and c != c2
    assert c2.frame.tree.redrawCount &gt; 0
finally:
    c2.close()</t>
<t tx="ekr.20051105135920">c.redraw_now() # To make node visible

c2 = c.new()
p2 = c2.currentPosition()
assert p.edit_widget()
c2.close()</t>
<t tx="ekr.20051105144609"></t>
<t tx="ekr.20051105144713">import leoTest ; u = leoTest.testUtils()
k = c.keyHandler
frame = c.frame ; tree = frame.tree ; canvas = tree.canvas
h = 'Test headline abc'
p = u.findNodeAnywhere(c,h)
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
    p.initHeadString(h)
    c.redraw_now()</t>
<t tx="ekr.20051105144920">c.redraw_now() # To make node visible

k = c.keyHandler
n = c.frame.tree.redrawCount
k.simulateCommand('save-file')
assert c.frame.tree.redrawCount &gt; n</t>
<t tx="ekr.20051105155853">def simulateCommand (self,commandName):
    
    k = self ; c = k.c
    
    func = c.commandsDict.get(commandName)
    
    if func:
        event = stroke = None
        k.masterCommand(event,func,stroke)
    else:
        g.trace('no command for %s' % (commandName),color='red')
        raise AttributeError</t>
<t tx="ekr.20051105165906"></t>
<t tx="ekr.20051105190211">import leoTest ; u = leoTest.testUtils()
k = c.keyHandler
frame = c.frame ; tree = frame.tree ; canvas = tree.canvas
h = 'Test headline abc'
p = u.findNodeAnywhere(c,h)
c.selectPosition(p)
c.redraw_now() # To make node visible
tree.editLabel(p)
w = p.edit_widget()
try:
    assert w
    g.app.gui.setSelectionRange(w,'1.1','1.2')
    w.event_generate('X')
    w.event_generate('Y')
    w.event_generate('Z')
    w.event_generate('&lt;Return&gt;')
    assert p.headString() == h[0] + 'XYZ' + h[2:]
    k.manufactureKeyPressForCommandName(w,'undo')
    assert p.headString() == h
finally:
    p.initHeadString(h)
    c.redraw_now()</t>
<t tx="ekr.20051106032745">import leoTest ; u = leoTest.testUtils()
k = c.keyHandler
frame = c.frame ; tree = frame.tree ; canvas = tree.canvas
h = 'Test headline abc'
p = u.findNodeAnywhere(c,h)
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
    p.initHeadString(h)
    c.redraw_now()</t>
<t tx="ekr.20051106033316"></t>
<t tx="ekr.20051106033316.1"></t>
<t tx="ekr.20051106033449"></t>
<t tx="ekr.20051106034108">import leoTest ; u = leoTest.testUtils()
k = c.keyHandler
frame = c.frame ; tree = frame.tree ; canvas = tree.canvas
h = 'Test headline abc'
p = u.findNodeAnywhere(c,h)
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
    p.initHeadString(h)
    c.redraw_now()</t>
<t tx="ekr.20051106034342">import leoTest ; u = leoTest.testUtils()
k = c.keyHandler
frame = c.frame ; tree = frame.tree ; canvas = tree.canvas
h = 'Test headline abc'
p = u.findNodeAnywhere(c,h)
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
    p.initHeadString(h)
    c.redraw_now()</t>
<t tx="ekr.20051106034342.1"></t>
<t tx="ekr.20051106034342.4">import leoTest ; u = leoTest.testUtils()
k = c.keyHandler
h = 'Test headline abc'
p = u.findNodeAnywhere(c,h)
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
    assert n2 &gt; n, '%s %s' % (n2,n1)
    # g.trace(n,n2)
finally:
    if 1:
        p.initHeadString(h)
        c.redraw_now()</t>
<t tx="ekr.20051106034823">import leoTest ; u = leoTest.testUtils()
h = 'Test headline abc'
p = u.findNodeAnywhere(c,h)
# Post by hand.
menu = c.frame.menu.getMenu('Edit')
i = menu.index('Paste')
c.selectPosition(p)
c.frame.bodyWantsFocus(later=False)
paste = '# Should be a comment'
g.app.gui.replaceClipboardWith(paste)
n = c.frame.body.colorizer.count
menu.invoke(i)
# Move around and and make sure it doesn't change.
try:
    assert c.frame.body.colorizer.count &gt; n
finally:
    if 1:
        p.setBodyString('')
        c.redraw_now()</t>
<t tx="ekr.20051106034823.1"></t>
<t tx="ekr.20051106035939.1">import leoTest ; u = leoTest.testUtils()
h = 'Test headline abc'
p = u.findNodeAnywhere(c,h)
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
<t tx="ekr.20051106041531">g.es_print('Test of @command')
g.app.unitTestDict ['unit-test-command1'] = True</t>
<t tx="ekr.20051106041531.1">g.app.unitTestDict = {}
c.executeMinibufferCommand('unit-test-command1')
assert g.app.unitTestDict.get('unit-test-command1') == True</t>
<t tx="ekr.20051106043501">import leoTest ; u = leoTest.testUtils()
k = c.keyHandler ; bodyCtrl = c.frame.body.bodyCtrl
h = 'Test headline abc'
p = u.findNodeAnywhere(c,h)
c.selectPosition(p)
c.redraw_now() # To make node visible
try:
    paste = 'ABC'
    g.app.gui.replaceClipboardWith(paste)
    # g.app.gui.setSelectionRange(w,'1.1','1.2')
    c.executeMinibufferCommand('paste-text')
    assert p.bodyString() == paste
    k.manufactureKeyPressForCommandName(bodyCtrl,'undo')
    assert not p.bodyString()
finally:
    p.setBodyString('')
    c.redraw_now()</t>
<t tx="ekr.20051106102656"></t>
<t tx="ekr.20051106111820">import leoTest ; u = leoTest.testUtils()
h = 'Test headline abc'
p = u.findNodeAnywhere(c,h)
# Post by hand.
menu = c.frame.menu.getMenu('Edit')
i = menu.index('Paste')
c.selectPosition(p)
c.frame.bodyWantsFocus(later=False)
paste = 'ABC'
g.app.gui.replaceClipboardWith(paste)
menu.invoke(i)
# Move around and and make sure it doesn't change.
try:
    assert p.bodyString() == paste
    c.selectPosition(p.threadBack())
    assert p.bodyString() == paste
    c.selectPosition(p)
    assert p.bodyString() == paste
finally:
    if 1:
        p.setBodyString('')
        c.redraw_now()</t>
<t tx="ekr.20051106114543">import leoTest ; u = leoTest.testUtils()
k = c.keyHandler
h = 'Test headline abc'
p = u.findNodeAnywhere(c,h)
c.selectPosition(p)
c.redraw_now() # To make node visible
c.frame.tree.editLabel(p)
w = p.edit_widget()
paste = 'ABC'
g.app.gui.replaceClipboardWith(paste)
try:
    assert w, 'no w'
    g.app.gui.setSelectionRange(w,'end','end')
    g.app.unitTestDict = {}
    k.manufactureKeyPressForCommandName(w,'paste-text')
    assert g.app.unitTestDict.get('headWidth') == True
finally:
    if 1:
        p.initHeadString(h)
        c.redraw_now()</t>
</tnodes>
</leo_file>
