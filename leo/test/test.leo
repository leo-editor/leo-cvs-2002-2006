<?xml version="1.0" encoding="UTF-8"?>
<?xml-stylesheet ekr_stylesheet?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="7867" clone_windows="0"/>
<globals body_outline_ratio="0.447779111645">
	<global_window_position top="52" left="284" height="833" width="959"/>
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
<v t="ekr.20051017093427"><vh>Test of remove-blank-lines</vh></v>
<v t="ekr.20051103112555"><vh>Test of event_generate</vh></v>
<v t="ekr.20051104052708"><vh>Test of executing a function by name</vh></v>
<v t="ekr.20051107115327"><vh>Move to root</vh></v>
<v t="ekr.20051109023647"><vh>New tabbed log</vh></v>
<v t="ekr.20051108102719"><vh>Test backward search</vh>
<v t="ekr.20051108102719.1"><vh>a</vh></v>
<v t="ekr.20051108102719.2"><vh>b</vh></v>
<v t="ekr.20051108102719.3"><vh>c</vh></v>
<v t="ekr.20051108111341"><vh>test</vh></v>
</v>
</v>
<v t="ekr.20051111114555" a="E"><vh>Subprocess tests</vh>
<v t="ekr.20051111143349.29"><vh>class debugCommandsClass (not used yet)</vh>
<v t="ekr.20051111143349.30"><vh> ctor</vh></v>
<v t="ekr.20051111143349.31"><vh>getPublicCommands (debugCommandsClass)</vh></v>
<v t="ekr.20051111143349.33"><vh>openDebugTab</vh></v>
<v t="ekr.20051111143349.20"><vh>hideTab</vh></v>
</v>
<v t="ekr.20051111114555.1" a="E"><vh>@thin leoDebugger.py</vh></v>
<v t="ekr.20051111114555.2" a="E"><vh>@button dbProc</vh>
<v t="ekr.20051111145211.1"><vh>openDebugTab</vh></v>
<v t="ekr.20051111143349.1" a="E"><vh>class debugTab</vh>
<v t="ekr.20051111143349.2"><vh>Birth &amp; death</vh>
<v t="ekr.20051111143349.3" a="E"><vh>__init__</vh>
<v t="ekr.20051111143349.7"><vh>&lt;&lt; Create the outer frames &gt;&gt;</vh></v>
<v t="ekr.20051111143922"><vh>&lt;&lt; create buttons &gt;&gt;</vh></v>
</v>
</v>
<v t="ekr.20051111143349.16" a="E"><vh>callbacks</vh>
<v t="ekr.20051111145134"><vh>askButtonCallback</vh></v>
<v t="ekr.20051111145134.1"><vh>killButtonCallback</vh></v>
<v t="ekr.20051111145134.2"><vh>runButtonCallback</vh></v>
<v t="ekr.20051111145134.3"><vh>tellButtonCallback</vh></v>
</v>
<v t="ekr.20051111151132" a="TV"><vh>get &amp; send</vh></v>
<v t="ekr.20051111162912"><vh>nonBlockingRead</vh></v>
<v t="ekr.20051111153206"><vh>stdinClass (not used)</vh></v>
</v>
</v>
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
<t tx="ekr.20050911112310">c.save()
c.redraw_now() # Must be done here.</t>
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
<t tx="ekr.20051104052708">c.executeMinibufferCommand('open-outline')</t>
<t tx="ekr.20051104081824"></t>
<t tx="ekr.20051105114247">name = "scripts.leo"
fileName = g.os_path_join(g.app.loadDir,"..","scripts",name)
ok,frame = g.openWithFileName(fileName,c)
if not ok:
    g.es("not found: %s" % name)</t>
<t tx="ekr.20051107115327">root = c.rootPosition()
if p != root:
    p.moveToRoot(root)
    c.redraw_now()</t>
<t tx="ekr.20051108102719"></t>
<t tx="ekr.20051108102719.1">alpha</t>
<t tx="ekr.20051108102719.2">beta</t>
<t tx="ekr.20051108102719.3">gamma</t>
<t tx="ekr.20051108111341">test a test</t>
<t tx="ekr.20051109023647"># import TabWindow as TabbedLog
# tw = TabbedLog.getPane('abc', c)

import Tknotebook
Tknotebook.test()</t>
<t tx="ekr.20051111114555"></t>
<t tx="ekr.20051111114555.2"># Simulation of debugger process

import subprocess
import sys
import time
import Tkinter as Tk

@others

openDebugTab(c)</t>
<t tx="ekr.20051111143349.1">class debugTab:

    """A class that implements Leo's tkinter debug tab."""

    @others</t>
<t tx="ekr.20051111143349.2"></t>
<t tx="ekr.20051111143349.3">def __init__(self,c,parentFrame):

    self.c = c
    self.db = None

    &lt;&lt; Create the outer frames &gt;&gt;
    &lt;&lt; create buttons &gt;&gt;
    </t>
<t tx="ekr.20051111143349.7">configName = 'log_pane_Debug_tab_background_color'
bg = c.config.getColor(configName) or 'MistyRose1'

parentFrame.configure(background=bg)

self.top = Tk.Frame(parentFrame,background=bg)
self.frame = Tk.Frame(self.top,background=bg)
self.outerFrame = outer = Tk.Frame(self.frame,background=bg)

self.top.pack   (side='top',expand=0,fill='x',pady=5)
    # Don't expand, so the frame goes to the top.

self.frame.pack (side="top",expand=1,fill='x')
outer.pack      (side='top',expand=1,fill='x',padx=2,pady=2,)</t>
<t tx="ekr.20051111143349.16"></t>
<t tx="ekr.20051111143349.20">def hideTab (self,event=None):
    
    c = self.c
    c.frame.log.selectTab('Log')
    c.frame.bodyWantsFocus()</t>
<t tx="ekr.20051111143349.29">if 0:
    class debugCommandsClass (baseEditCommandsClass):
    
        '''Implements debug commands.'''
    
        @others</t>
<t tx="ekr.20051111143349.30">def __init__ (self,c):

    baseEditCommandsClass.__init__(self,c) # init the base class.
    
    self.debugTabHandler = None</t>
<t tx="ekr.20051111143349.31">def getPublicCommands (self):
    
    return {
        # The new find tab replaces the find dialog.
        'hide-find-tab':    self.hideDebugTab,
        'open-debug-tab':   self.openDebugTab,
    }</t>
<t tx="ekr.20051111143349.33">def openDebugTab (self,event=None):

    c = self.c ; log = c.frame.log ; tabName = 'Debug'

    if log.frameDict.get(tabName):
        log.selectTab(tabName)
    else:
        log.selectTab(tabName)
        f = log.frameDict.get(tabName)
        t = log.textDict.get(tabName)
        t.pack_forget()
        self.debugTabHandler = debugTab(c,f)</t>
<t tx="ekr.20051111143922">buttons  = Tk.Frame(outer,background=bg)
buttons.pack(side='top',expand=1)

width = 10

for text,callback in (
    ('Run', self.runButtonCallback),
    ('Kill',self.killButtonCallback),
    ('Ask', self.askButtonCallback),
    ('Tell',self.tellButtonCallback),
):
    w = Tk.Button(buttons,text=text,command=callback)
    w.configure(width=width)
    w.pack(side='left',anchor='w',pady=2,padx=2)</t>
<t tx="ekr.20051111145134">def askButtonCallback (self,event=None):

    __pychecker__ = '--no-argsused'

    self.send('ask')
    print 'ask returns', self.get()

    return 'break'</t>
<t tx="ekr.20051111145134.1">def killButtonCallback (self,event=None):

    __pychecker__ = '--no-argsused'

    self.send('kill')

    if self.db:
        self.db.wait()
        self.db = None
        print ; print 'done!'

    return 'break'</t>
<t tx="ekr.20051111145134.2">def runButtonCallback (self,event=None):

    __pychecker__ = '--no-argsused'

    g.trace()

    dbPath = g.os_path_join('..','test','leoDebugger.py')
    args = [r"c:\python24\python", dbPath]
    pipe = subprocess.PIPE
    
    if self.db:
        g.trace('already running')
    else:
        self.db = subprocess.Popen(args,
            stdin=pipe,
            stdout=pipe, ## sys.stdout
            stderr=sys.stderr,
        )
        # stdout, stderr = self.db.communicate(s)

    return 'break'
</t>
<t tx="ekr.20051111145134.3">def tellButtonCallback(self,event=None):
    
    __pychecker__ = '--no-argsused'
    
    self.send('tell')

    return 'break'</t>
<t tx="ekr.20051111145211.1">def openDebugTab (c):

    log = c.frame.log ; tabName = 'Debug'

    if log.frameDict.get(tabName):
        log.selectTab(tabName)
    else:
        log.selectTab(tabName)
        f = log.frameDict.get(tabName)
        t = log.textDict.get(tabName)
        t.pack_forget()
        debugTab(c,f)</t>
<t tx="ekr.20051111151132">if 0: # Communicate waits for the process to terminate!
    stdout, stderr = self.db.communicate(s)

def get(self):
    
    if self.db:
        # Busy waiting:
        while 1:
            time.sleep(0.4)
            s = self.nonBlockingRead(self.db.stdout)
            if s:
                return s
            else:
                g.trace('waiting for ask')
    else:
        g.trace('not running')
        return ''

def send(self,s):

    if self.db:
       self.db.stdin.write(s)
    else:
        g.trace('not running')</t>
<t tx="ekr.20051111153206">class stdinClass:
    
    '''A class for controlled stdin.'''
    
    def __init__ (self):
        self.s = ''
        
    def write (self,s):
        self.s = s
        
    def readline(self):
        s = self.s
        self.s = ''
        return s</t>
<t tx="ekr.20051111162912">def nonBlockingRead(self,f):
    
    f.seek(0,0) ; p1 = f.tell() # p1 is present position.
    f.seek(0,2) ; p2 = f.tell() # p2 is end position.

    if p2 &gt; p1:
        f.seek(p1,0) # Restore point
        s = f.read(p2-p1)
        f.seek(0,2) # Move to the end.
    else:
        s = ''

    return s</t>
</tnodes>
</leo_file>
