#! /usr/bin/env python
#@+leo-ver=4-thin
#@+node:ekr.20031218072017.2605:@thin leo.py 
#@@first

"""Entry point for Leo in Python."""

#@@language python
#@@tabwidth -4

#@<< Import pychecker >>
#@+node:ekr.20031218072017.2606:<< Import pychecker >>
#@@color

# __pychecker__ = '--no-argsused'

# See pycheckrc file in leoDist.leo for a list of erroneous warnings to be suppressed.

if 0: # Set to 1 for lint-like testing.
      # Use t23.bat: only on Python 2.3.

    try:
        import pychecker.checker
        # This works.  We may want to set options here...
        # from pychecker import Config 
        # print pychecker
        print ; print "Warning (in leo.py): pychecker.checker running..." ; print
    except:
        print ; print 'Can not import pychecker' ; print
#@nonl
#@-node:ekr.20031218072017.2606:<< Import pychecker >>
#@nl

__pychecker__ = '--no-import --no-reimportself --no-reimport'
    # Suppress import errors: this module must do strange things with imports.

# Warning: do not import any Leo modules here!
# Doing so would make g.app invalid in the imported files.
import os
import string
import sys

#@+others
#@+node:ekr.20031218072017.1934:run & allies
def run(fileName=None,*args,**keywords):
    
    """Initialize and run Leo"""
    
    __pychecker__ = '--no-argsused' # keywords not used.
    
    if not isValidPython(): return
    #@    << import leoGlobals and leoApp >>
    #@+node:ekr.20041219072112:<< import leoGlobals and leoApp >>
    # Import leoGlobals, but do NOT set g.
    try:
        import leoGlobals
    except ImportError:
        print "Error importing leoGlobals.py"
    
    # Create the application object.
    try:
        import leoApp
        leoGlobals.app = leoApp.LeoApp()
    except ImportError:
        print "Error importing leoApp.py"
        
    # NOW we can set g.
    g = leoGlobals
    assert(g.app)
    #@nonl
    #@-node:ekr.20041219072112:<< import leoGlobals and leoApp >>
    #@nl
    g.computeStandardDirectories()
    script, windowFlag = getBatchScript() # Do early so we can compute verbose next.
    verbose = script is None
    g.app.setLeoID(verbose=verbose) # Force the user to set g.app.leoID.
    #@    << import leoNodes and leoConfig >>
    #@+node:ekr.20041219072416.1:<< import leoNodes and leoConfig >>
    try:
        import leoNodes
    except ImportError:
        print "Error importing leoNodes.py"
        import traceback ; traceback.print_exc()
    try:
        import leoConfig
    except ImportError:
        print "Error importing leoConfig.py"
        import traceback ; traceback.print_exc()
    #@nonl
    #@-node:ekr.20041219072416.1:<< import leoNodes and leoConfig >>
    #@nl
    g.app.nodeIndices = leoNodes.nodeIndices(g.app.leoID)
    g.app.config = leoConfig.configClass()
    fileName = completeFileName(fileName)
    reportDirectories(verbose)
    # Read settings *after* setting g.app.config.
    # Read settings *before* opening plugins.  This means if-gui has effect only in per-file settings.
    g.app.config.readSettingsFiles(fileName,verbose)
    g.app.setEncoding()
    if script:
        if windowFlag:
            g.app.createTkGui() # Creates global windows.
            g.app.gui.setScript(script)
            sys.args = []
        else:
            createNullGuiWithScript(script)
        fileName = None
    # Load plugins. Plugins may create g.app.gui.
    g.doHook("start1")
    if g.app.killed: return # Support for g.app.forceShutdown.
    # Create the default gui if needed.
    if g.app.gui == None:
        g.app.createTkGui() # Creates global windows.
    # Initialize tracing and statistics.
    g.init_sherlock(args)
    #@    << start psycho >>
    #@+node:ekr.20040411081633:<< start psycho >>
    if g.app and g.app.use_psyco:
        try:
            import psyco
            if 0:
                theFile = r"c:\prog\test\psycoLog.txt"
                g.es("psyco now logging to",theFile,color="blue")
                psyco.log(theFile)
                psyco.profile()
            psyco.full()
            g.es("psyco now running",color="blue")
        except ImportError:
            pass
        except:
            print "unexpected exception importing psyco"
            g.es_exception()
    #@nonl
    #@-node:ekr.20040411081633:<< start psycho >>
    #@nl
    # New in 4.3: clear g.app.initing _before_ creating the frame.
    g.app.initing = False # "idle" hooks may now call g.app.forceShutdown.
    # Create the main frame.  Show it and all queued messages.
    c,frame = createFrame(fileName)
    if not frame: return
    g.app.trace_gc          = c.config.getBool('trace_gc')
    g.app.trace_gc_calls    = c.config.getBool('trace_gc_calls')
    g.app.trace_gc_verbose  = c.config.getBool('trace_gc_verbose')
    if g.app.disableSave:
        g.es("disabling save commands",color="red")
    g.app.writeWaitingLog()
    p = c.currentPosition()
    g.doHook("start2",c=c,p=p,v=p,fileName=fileName)
    if c.config.getBool('allow_idle_time_hook'):
        g.enableIdleTimeHook()
    if not fileName:
        c.redraw_now()
    c.bodyWantsFocus()
    g.app.gui.runMainLoop()
#@nonl
#@+node:ekr.20031218072017.1936:isValidPython
def isValidPython():

    message = """\
Leo requires Python 2.2.1 or higher.
You may download Python from http://python.org/download/
"""
    try:
        # This will fail if True/False are not defined.
        import leoGlobals as g
    except ImportError:
        print "isValidPython: can not import leoGlobals"
        return 0
    except:
        print "isValidPytyhon: unexpected exception: import leoGlobals.py as g"
        import traceback ; traceback.print_exc()
        return 0
    try:
        ok = g.CheckVersion(sys.version, "2.2.1")
        if not ok:
            print message
            g.app.gui.runAskOkDialog(None,"Python version error",message=message,text="Exit")
        return ok
    except:
        print "isValidPython: unexpected exception: g.CheckVersion"
        import traceback ; traceback.print_exc()
        return 0
#@nonl
#@-node:ekr.20031218072017.1936:isValidPython
#@+node:ekr.20041124083125:completeFileName (leo.py)
def completeFileName (fileName):
    
    import leoGlobals as g
    
    if not fileName:
        return None
        
    # This does not depend on config settings.
    fileName = g.os_path_join(os.getcwd(),fileName)

    head,ext = g.os_path_splitext(fileName)
    if not ext:
        fileName = fileName + ".leo"

    return fileName
#@nonl
#@-node:ekr.20041124083125:completeFileName (leo.py)
#@+node:ekr.20031218072017.1624:createFrame (leo.py)
def createFrame (fileName):
    
    """Create a LeoFrame during Leo's startup process."""
    
    import leoGlobals as g

    # Try to create a frame for the file.
    if fileName:
        if g.os_path_exists(fileName):
            ok, frame = g.openWithFileName(fileName,None)
            if ok:
                return frame.c,frame

    # Create a _new_ frame & indicate it is the startup window.
    c,frame = g.app.newLeoCommanderAndFrame(fileName=fileName)
    frame.setInitialWindowGeometry()
    frame.resizePanesToRatio(frame.ratio,frame.secondary_ratio)
    frame.startupWindow = True
    # 3/2/05: Call the 'new' hook for compatibility with plugins.
    g.doHook("new",old_c=None,c=c,new_c=c)

    # Report the failure to open the file.
    if fileName:
        g.es("File not found: " + fileName)

    return c,frame
#@nonl
#@-node:ekr.20031218072017.1624:createFrame (leo.py)
#@+node:ekr.20031218072017.1938:createNullGuiWithScript (leo.py)
def createNullGuiWithScript (script):
    
    import leoGlobals as g
    import leoGui
    
    g.app.batchMode = True
    g.app.gui = leoGui.nullGui("nullGui")
    if not g.app.root:
        g.app.root = g.app.gui.createRootWindow()
    g.app.gui.finishCreate()
    g.app.gui.setScript(script)
#@-node:ekr.20031218072017.1938:createNullGuiWithScript (leo.py)
#@+node:ekr.20031218072017.1939:getBatchScript
def getBatchScript ():
    
    import leoGlobals as g
    windowFlag = False
    
    name = None ; i = 1 # Skip the dummy first arg.
    while i + 1 < len(sys.argv):
        arg = sys.argv[i].strip().lower()
        if arg in ("--script","-script"):
            name = sys.argv[i+1].strip() ; break
        if arg in ("--script-window","-script-window"):
            name = sys.argv[i+1].strip() ; windowFlag = True ; break
        i += 1

    if not name:
        return None, windowFlag
    name = g.os_path_join(g.app.loadDir,name)
    try:
        f = None
        try:
            f = open(name,'r')
            script = f.read()
            # g.trace("script",script)
        except IOError:
            g.es_print("can not open script file: " + name, color="red")
            script = None
    finally:
        if f: f.close()
        return script, windowFlag
#@nonl
#@-node:ekr.20031218072017.1939:getBatchScript
#@+node:ekr.20041130093254:reportDirectories
def reportDirectories(verbose):
    
    import leoGlobals as g
   
    if verbose:
        for kind,theDir in (
            ("global config",g.app.globalConfigDir),
            ("home",g.app.homeDir),
        ):
            g.es("%s dir: %s" % (kind,theDir),color="blue")
#@nonl
#@-node:ekr.20041130093254:reportDirectories
#@-node:ekr.20031218072017.1934:run & allies
#@+node:ekr.20031218072017.2607:profile
#@+at 
#@nonl
# To gather statistics, do the following in a Python window, not idle:
# 
#     import leo
#     leo.profile()  (this runs leo)
#     load leoDocs.leo (it is very slow)
#     quit Leo.
#@-at
#@@c

def profile ():
    
    """Gather and print statistics about Leo"""

    import profile, pstats
    
    name = "c:/prog/test/leoProfile.txt"
    profile.run('leo.run()',name)

    p = pstats.Stats(name)
    p.strip_dirs()
    p.sort_stats('cum','file','name')
    p.print_stats()
#@nonl
#@-node:ekr.20031218072017.2607:profile
#@-others

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.platform=="win32": # Windows
            fileName = string.join(sys.argv[1:],' ')
        else:
            fileName = sys.argv[1]
        run(fileName)
    else:
        run()
#@nonl
#@-node:ekr.20031218072017.2605:@thin leo.py 
#@-leo
