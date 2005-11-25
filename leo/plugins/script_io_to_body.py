#@+leo-ver=4-thin
#@+node:edream.110203113231.925:@thin script_io_to_body.py
"""Send output from the Execute Script command to the end of the body pane"""

#@@language python
#@@tabwidth -4

#@<< imports >>
#@+node:ekr.20050101090207.4:<< imports >>
import leoGlobals as g
import leoPlugins

Tk = g.importExtension('Tkinter',pluginName=__name__,verbose=True)
#@nonl
#@-node:ekr.20050101090207.4:<< imports >>
#@nl

#@+others
#@+node:edream.110203113231.926:onStart
def onStart (tag,keywords):
    
    # Replace frame.put with newPut.
    import leoTkinterFrame
    g.funcToMethod(newExecuteScript,leoTkinterFrame.leoTkinterFrame,"OnExecuteScript")
#@-node:edream.110203113231.926:onStart
#@+node:edream.110203113231.927:newExecuteScript
# Execute the selected body text as a Python script and sends the output to the end of the body pane.

def newExecuteScript(self,event=None,v=None):
    
    c = self.c ; body = self.body ; s = None
    if v == None:
        v = c.currentVnode() 

    # Assume any selected body text is a script.
    start,end = body.getTextSelection() # EKR: 11/04/03
    if start and end and start != end: # 7/7/03
        s = body.bodyCtrl.get(start,end)
    else:
        s = body.bodyCtrl.get("1.0","end")
    s = s.strip()
    if s and len(s) > 0:
        s += '\n' # Make sure we end the script properly.
        # Switch output.
        import leoTkinterFrame,leoGlobals
        oldput = leoTkinterFrame.leoTkinterLog.put # 11/7/03
        oldputnl = leoTkinterFrame.leoTkinterLog.putnl # 11/7/03
        oldes = leoGlobals.es
        oldenl = leoGlobals.enl
        oldecnl = leoGlobals.ecnl
        oldecnls = leoGlobals.ecnls
        leoGlobals.es = newEs
        leoGlobals.enl = newEnl
        leoGlobals.ecnl = newEcnl
        leoGlobals.ecnls = newEcnls
        g.funcToMethod(newPut,leoTkinterFrame.leoTkinterLog,"put") #  11/7/03
        g.funcToMethod(newPutNl,leoTkinterFrame.leoTkinterLog,"putNl") # 11/7/03
        g.redirectStderr()
        g.redirectStdout()
        try:
            exec s in {} # Use {} to get a pristine environment!
            ok = True
        except:
            ok = False
        # Restore output.
        g.funcToMethod(oldput,leoTkinterFrame.leoTkinterLog,"put") # 11/7/03
        g.funcToMethod(oldputnl,leoTkinterFrame.leoTkinterLog,"putNl") # 11/7/03
        leoGlobals.es = oldes
        leoGlobals.enl = oldenl
        leoGlobals.ecnl = oldecnl
        leoGlobals.ecnls = oldecnls
        g.restoreStderr()
        g.restoreStdout()
        if not ok:
            g.es("newExecuteScript: exception executing script")
            g.es_exception(full=False)
    else:
        g.es("newExecuteScript: empty script")
#@nonl
#@-node:edream.110203113231.927:newExecuteScript
#@+node:edream.110203113231.928:newPut and newPutNl
# Same as frame.put except sends output to the end of the body text.
def newPut (self,s):
    c = self.frame.c
    bodyCtrl = self.frame.body.bodyCtrl
    if bodyCtrl:
        bodyCtrl.insert("end",s)
        # bodyCtrl.see("end")
        self.frame.tree.onBodyChanged("Typing")
    else: print s,

# Same as frame.putnl exceptsends output to the end of the body text.
def newPutNl (self):
    newPut (self,'\n')
#@nonl
#@-node:edream.110203113231.928:newPut and newPutNl
#@+node:edream.110203113231.929:newEs, etc.
def newEnl():
    print
    
def newEcnl():
    print
    
def newEcnls(n):
    while n > 0:
        n -= 1
        print

def newEs(s,*args,**keys):
    newline = keys.get("newline",True)
    if type(s) != type("") and type(s) != type(u""):
        s = repr(s)
    for arg in args:
        if type(arg) != type("") and type(arg) != type(u""):
            arg = repr(arg)
        s = s + ", " + arg
    if newline:
        print s
    else:
        print s,
#@-node:edream.110203113231.929:newEs, etc.
#@-others

if Tk and not g.app.unitTesting: # Not for unit testing: modifies core classes.

    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":

        leoPlugins.registerHandler("start1", onStart)
    
        __version__ = "1.3" # Contains Tk-specific code.
        g.plugin_signon(__name__)
#@nonl
#@-node:edream.110203113231.925:@thin script_io_to_body.py
#@-leo
