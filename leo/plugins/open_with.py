#@+leo-ver=4-thin
#@+node:EKR.20040517075715.4:@thin open_with.py
"""Create menu for Open With command and handle the resulting commands"""

#@@language python
#@@tabwidth -4

import leoGlobals as g
import leoPlugins

try: import Tkinter as Tk
except ImportError: Tk = None

#@+others
#@+node:EKR.20040517075715.5:on_idle
# frame.OnOpenWith creates the dict with the following entries:
# "body", "c", "encoding", "f", "path", "time" and "v".

def on_idle (tag,keywords):

    import os
    a = g.app
    if a.killed: return
    for dict in a.openWithFiles:
        path = dict.get("path")
        c = dict.get("c")
        encoding = dict.get("encoding",None)
        v = dict.get("v")
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
                    #@                    << update v's body text >>
                    #@+node:EKR.20040517075715.6:<< update v's body text >>
                    
                    
                    
                    # Convert body and s to whatever encoding is in effect.
                    body = v.bodyString()
                    body = g.toEncodedString(body,encoding,reportErrors=True)
                    s = g.toEncodedString(s,encoding,reportErrors=True) # 10/13/03
                    
                    conflict = body != old_body and body != s
                    
                    # Set update if we should update the outline from the file.
                    if conflict:
                        # See how the user wants to resolve the conflict.
                        g.es("conflict in " + g.shortFileName(path),color="red")
                        message = "Replace changed outline with external changes?"
                        result = g.app.gui.runAskYesNoDialog("Conflict!",message)
                        update = result.lower() == "yes"
                    else:
                        update = s != body
                    
                    if update:
                        g.es("updated from: " + g.shortFileName(path),color="blue")
                        v.setBodyStringOrPane(s,encoding) # 10/16/03
                        c.selectVnode(v)
                        dict["body"] = s
                    elif conflict:
                        g.es("not updated from: " + g.shortFileName(path),color="blue")
                    #@nonl
                    #@-node:EKR.20040517075715.6:<< update v's body text >>
                    #@nl
            except:
                g.es_exception() ## testing
                pass
#@nonl
#@-node:EKR.20040517075715.5:on_idle
#@+node:EKR.20040517075715.8:create_open_with_menu
def create_open_with_menu (tag,keywords):

    if  (tag in ("start2","open2") or
        (tag=="command2" and keywords.get("label")=="new")):

        #@        << create the Open With menu >>
        #@+node:EKR.20040517075715.9:<< create the Open With menu >>
        #@+at 
        #@nonl
        # Entries in the following table are the tuple 
        # (commandName,shortcut,data).
        # 
        # - data is the tuple (command,arg,ext).
        # - command is one of "os.system", "os.startfile", "os.spawnl", 
        # "os.spawnv" or "exec".
        # 
        # Leo executes command(arg+path) where path is the full path to the 
        # temp file.
        # If ext is not None, the temp file has the extension ext,
        # Otherwise, Leo computes an extension based on what @language 
        # directive is in effect.
        #@-at
        #@@c
        
        idle_arg = "c:/python22/tools/idle/idle.py -e "
        
        if 1: # Default table.
            table = (
                # Opening idle this way doesn't work so well.
                # ("&Idle",   "Alt+Shift+I",("os.system",idle_arg,".py")),
                ("&Word",   "Alt+Shift+W",("os.startfile",None,".doc")),
                ("Word&Pad","Alt+Shift+T",("os.startfile",None,".txt")))
        elif 1: # Test table.
            table = ("&Word","Alt+Shift+W",("os.startfile",None,".doc")),
        else: # David McNab's table.
            table = ("X&Emacs", "Ctrl+E", ("os.spawnl","/usr/bin/gnuclient", None)),
        
        g.top().frame.menu.createOpenWithMenuFromTable(table)
        #@nonl
        #@-node:EKR.20040517075715.9:<< create the Open With menu >>
        #@nl
#@nonl
#@-node:EKR.20040517075715.8:create_open_with_menu
#@-others

if Tk and not g.app.unitTesting: # Register the handlers...

    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":

        g.app.hasOpenWithMenu = True
        leoPlugins.registerHandler("idle", on_idle)
        leoPlugins.registerHandler(("start2","open2","command2"), create_open_with_menu)
    
        __version__ = "1.4" # Set version for the plugin handler.
        g.plugin_signon(__name__)
#@-node:EKR.20040517075715.4:@thin open_with.py
#@-leo
