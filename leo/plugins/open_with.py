#@+leo-ver=4-thin
#@+node:EKR.20040517075715.4:@thin open_with.py
"""Create menu for Open With command and handle the resulting commands"""

#@@language python
#@@tabwidth -4

#@<< imports >>
#@+node:ekr.20050101090207.8:<< imports >>
import leoGlobals as g
import leoPlugins

Tk = g.importExtension('Tkinter',pluginName=__name__,verbose=True)

try:
    import subprocess   # only available in Python 2.4 and later
except ImportError:
    pass
#@nonl
#@-node:ekr.20050101090207.8:<< imports >>
#@nl

__version__ = '1.5'
#@<< version history >>
#@+node:ekr.20050311110052:<< version history >>
#@@killcolor

#@+at
# 
# 1.5 EKR:
#     - Use only 'new' and 'open2' hooks to create menu.
#@-at
#@nonl
#@-node:ekr.20050311110052:<< version history >>
#@nl

#@+others
#@+node:ekr.20050311090939.8:init
def init():
    
    ok = Tk is not None # Ok for unit testing: creates Open With menu.
    
    if ok:
        if g.app.gui is None:
            g.app.createTkGui(__file__)
    
        if g.app.gui.guiName() == "tkinter":
            g.app.hasOpenWithMenu = True
            leoPlugins.registerHandler("idle", on_idle)
            leoPlugins.registerHandler(('new','open2'), create_open_with_menu)
            g.plugin_signon(__name__)
            
    return ok
#@nonl
#@-node:ekr.20050311090939.8:init
#@+node:EKR.20040517075715.5:on_idle
# frame.OnOpenWith creates the dict with the following entries:
# "body", "c", "encoding", "f", "path", "time" and "p".

def on_idle (tag,keywords):

    import os
    a = g.app
    if a.killed: return
    for dict in a.openWithFiles:
        path = dict.get("path")
        c = dict.get("c")
        encoding = dict.get("encoding",None)
        p = dict.get("p")
        old_body = dict.get("body")
        if path and os.path.exists(path):
            try:
                time = os.path.getmtime(path)
                if time and time != dict.get("time"):
                    dict["time"] = time # inhibit endless dialog loop.
                    # The file has changed.
                    #@                    << set s to the file text >>
                    #@+node:EKR.20040517075715.7:<< set s to the file text >>
                    try:
                        # Update v from the changed temp file.
                        f=open(path)
                        s=f.read()
                        f.close()
                    except:
                        g.es("can not open " + g.shortFileName(path))
                        break
                    #@-node:EKR.20040517075715.7:<< set s to the file text >>
                    #@nl
                    #@                    << update p's body text >>
                    #@+node:EKR.20040517075715.6:<< update p's body text >>
                    # Convert body and s to whatever encoding is in effect.
                    body = p.bodyString()
                    body = g.toEncodedString(body,encoding,reportErrors=True)
                    s = g.toEncodedString(s,encoding,reportErrors=True)
                    
                    conflict = body != old_body and body != s
                    
                    # Set update if we should update the outline from the file.
                    if conflict:
                        # See how the user wants to resolve the conflict.
                        g.es("conflict in " + g.shortFileName(path),color="red")
                        message = "Replace changed outline with external changes?"
                        result = g.app.gui.runAskYesNoDialog(c,"Conflict!",message)
                        update = result.lower() == "yes"
                    else:
                        update = s != body
                    
                    if update:
                        g.es("updated from: " + g.shortFileName(path),color="blue")
                        p.setBodyStringOrPane(s,encoding)
                        c.selectPosition(p)
                        dict["body"] = s
                    elif conflict:
                        g.es("not updated from: " + g.shortFileName(path),color="blue")
                    #@nonl
                    #@-node:EKR.20040517075715.6:<< update p's body text >>
                    #@nl
            except Exception:
                g.es_exception() ## testing
                pass
#@nonl
#@-node:EKR.20040517075715.5:on_idle
#@+node:EKR.20040517075715.8:create_open_with_menu
#@+at 
#@nonl
# Entries in the following table are the tuple (commandName,shortcut,data).
# 
# - data is the tuple (command,arg,ext).
# - command is one of "os.system", "os.startfile", "os.spawnl", "os.spawnv" or 
# "exec".
# 
# Leo executes command(arg+path) where path is the full path to the temp file.
# If ext is not None, the temp file has the extension ext,
# Otherwise, Leo computes an extension based on what @language directive is in 
# effect.
#@-at
#@@c

def create_open_with_menu (tag,keywords):

    c = keywords.get('c')
    if not c: return

    idle_arg = "c:/python22/tools/idle/idle.py -e "
    
    if subprocess:
        if 1: # Default table.
            table = (
                ("Idle", "Alt+Ctrl+I",
                    ("subprocess.Popen",
                        ["pythonw", "C:/Python24/Lib/idlelib/idle.pyw"], ".py")),
                ("Word", "Alt+Ctrl+W",
                    ("subprocess.Popen",
                    "C:/Program Files/Microsoft Office/Office/WINWORD.exe",
                    None)),
                ("WordPad", "Alt+Ctrl+T",
                    ("subprocess.Popen",
                    "C:/Program Files/Windows NT/Accessories/wordpad.exe",
                    None)),
            )
            
        if 0:
            #@            << Jim Sizelove's table >>
            #@+node:ekr.20050909101202:<< Jim Sizelove's table >>
            table = (
                ("Emacs", "Alt+Ctrl+E",
                    ("subprocess.Popen", "C:/Program Files/Emacs/bin/emacs.exe", None)),
                ("Gvim", "Alt+Ctrl+G",
                    ("subprocess.Popen",
                    ["C:/Program Files/Vim/vim63/gvim.exe", 
                    "--servername", "LEO", "--remote-silent"], None)),
                ("Idle", "Alt+Ctrl+I",
                    ("subprocess.Popen",
                    ["pythonw", "C:/Python24/Lib/idlelib/idle.pyw"], ".py")),
                ("NotePad", "Alt+Ctrl+N",
                    ("os.startfile", None, ".txt")),
                ("PythonWin", "Alt+Ctrl+P",
                    ("subprocess.Popen", "C:/Python24/Lib/site-packages/pythonwin/Pythonwin.exe", None)),
                ("WordPad", "Alt+Ctrl+W",
                    ("subprocess.Popen", "C:/Program Files/Windows NT/Accessories/wordpad.exe", None)),
            )
            #@nonl
            #@-node:ekr.20050909101202:<< Jim Sizelove's table >>
            #@nl
    elif 1: # Default table.
        table = (
            # Opening idle this way doesn't work so well.
            # ("&Idle",   "Alt+Shift+I",("os.system",idle_arg,".py")),
            ("&Word",   "Alt+Shift+W",("os.startfile",None,".doc")),
            ("Word&Pad","Alt+Shift+T",("os.startfile",None,".txt")))
    elif 0: # Test table.
        table = ("&Word","Alt+Shift+W",("os.startfile",None,".doc")),
    elif 0: # David McNab's table.
        table = ("X&Emacs", "Ctrl+E", ("os.spawnl","/usr/bin/gnuclient", None)),
    
    c.frame.menu.createOpenWithMenuFromTable(table)
#@nonl
#@-node:EKR.20040517075715.8:create_open_with_menu
#@-others
#@nonl
#@-node:EKR.20040517075715.4:@thin open_with.py
#@-leo
