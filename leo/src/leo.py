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

# See pycheckrc file in leoDist.leo for a list of erroneous warnings to be suppressed.

if 0: # Set to 1 for lint-like testing.
    try:
        import pychecker.checker
        # This works.  We may want to set options here...
        # from pychecker import Config 
        print ; print "Warning: pychecker.checker running..." ; print
    except:
        pass
#@nonl
#@-node:ekr.20031218072017.2606:<< Import pychecker >>
#@nl

# Suppress import errors.
# This module must do strange things with imports.
__pychecker__ = '--no-import --no-reimportself --no-reimport '

# Warning: do not import any Leo modules here!
# Doing so would make g.app invalid in the imported files.
import os
import string
import sys

#@+others
#@+node:ekr.20031218072017.1934:run & allies
def run(fileName=None,*args,**keywords):
    
    """Initialize and run Leo"""
    
    if not isValidPython(): return
    # Import leoGlobals, but do NOT set g.
    import leoGlobals
    # Create the application object.
    import leoApp ; leoGlobals.app = leoApp.LeoApp()
    g = leoGlobals ; assert(g.app) # NOW we can set g.
    g.app.loadDir = computeLoadDir() # Depends on g.app.tkEncoding: uses utf-8 for now.
    g.app.homeDir = computeHomeDir()
    g.app.globalConfigDir = computeGlobalConfigDir()
    g.app.setLeoID() # Force the user to set g.app.leoID.
    import leoNodes ; g.app.nodeIndices = leoNodes.nodeIndices(g.app.leoID)
    import leoConfig ; g.app.config = leoConfig.config()
    g.app.config.readSettingsFiles() # Must be done after setting g.app.config.
    g.app.setEncoding()
    script = getBatchScript()
    if script:
        createNullGuiWithScript(script)
        fileName = None
    # Load plugins. Plugins may create g.app.gui.
    g.doHook("start1")
    if g.app.killed: return # Support for g.app.forceShutdown.
    # Create the default gui if needed.
    if g.app.gui == None:
        g.app.createTkGui()
    # Initialize tracing and statistics.
    g.init_sherlock(args)
    g.clear_stats()
    #@    << start psycho >>
    #@+node:ekr.20040411081633:<< start psycho >>
    if g.app.use_psyco:
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
    # Create the main frame.  Show it and all queued messages.
    c,frame = createFrame(fileName)
    if not frame: return
    if g.app.disableSave:
        g.es("disabling save commands",color="red")
    g.app.writeWaitingLog()
    p = c.currentPosition()
    g.doHook("start2",c=c,p=p,v=p,fileName=fileName)
    g.enableIdleTimeHook()
    frame.tree.redraw()
    frame.body.setFocus()
    g.app.initing = False # "idle" hooks may now call g.app.forceShutdown.
    g.app.gui.runMainLoop()
#@+node:ekr.20031218072017.1936:isValidPython
def isValidPython():

    message = """\
Leo requires Python 2.2.1 or higher.
You may download Python from http://python.org/download/
"""
    
    try:
        # This will fail if True/False are not defined.
        import leoGlobals as g
    except:
        print message
        return 0
    try:
        ok = g.CheckVersion(sys.version, "2.2.1")
        if not ok:
            g.app.gui.runAskOkDialog("Python version error",message=message,text="Exit")
        return ok
    except:
        print "exception getting Python version"
        import traceback ; traceback.print_exc()
        return False
#@nonl
#@-node:ekr.20031218072017.1936:isValidPython
#@+node:ekr.20041117155521:computeGlobalConfigDir
def computeGlobalConfigDir():
    
    import leoGlobals as g
    
    encoding = startupEncoding()

    try:
        theDir = sys.leo_config_directory
    except AttributeError:
        theDir = g.os_path_join(g.app.loadDir,"..","config")
        
    if theDir:
        theDir = g.os_path_normabs(theDir)
        
    if (
        not theDir or
        not g.os_path_exists(theDir,encoding) or
        not g.os_path_isdir(theDir,encoding)
    ):
        theDir = None

    g.es("global config dir: %s" % (theDir),color="blue")
    
    return theDir
#@nonl
#@-node:ekr.20041117155521:computeGlobalConfigDir
#@+node:ekr.20041117151301:computeHomeDir
def computeHomeDir():
    
    """Returns the user's home directory."""
    
    import leoGlobals as g

    encoding = startupEncoding()
    dotDir = g.os_path_normabs('./',encoding)
    home = os.getenv('HOME',default=dotDir)
    home = g.os_path_normabs(home,encoding)
    
    if (
        not home or
        not g.os_path_exists(home,encoding) or
        not g.os_path_isdir(home,encoding)
    ):
        home = None

    g.es("home dir: %s" % (home),color="blue")
    return home
#@nonl
#@-node:ekr.20041117151301:computeHomeDir
#@+node:ekr.20031218072017.1937:computeLoadDir
def computeLoadDir():
    
    """Returns the directory containing leo.py."""
    
    import leoGlobals as g

    try:
        import leo
        encoding = startupEncoding()
        path = g.os_path_normabs(leo.__file__,encoding)
        if path:
            loadDir = g.os_path_dirname(path,encoding)
        else: loadDir = None
            
        if (
            not loadDir or
            not g.os_path_exists(loadDir,encoding) or
            not g.os_path_isdir(loadDir,encoding)
        ):
            loadDir = os.getcwd()
            print "Using emergency loadDir:",repr(loadDir)
        
        loadDir = g.os_path_normabs(loadDir,encoding)
        # g.es("load dir: %s" % (loadDir),color="blue")
        return loadDir
    except:
        print "Exception getting load directory"
        import traceback ; traceback.print_exc()
        return None
#@nonl
#@-node:ekr.20031218072017.1937:computeLoadDir
#@+node:ekr.20041117151301.1:startupEncoding
def startupEncoding ():
    
    import sys
    
    if sys.platform=="win32": # "mbcs" exists only on Windows.
        encoding = "mbcs"
    elif sys.platform=="dawwin":
        encoding = "utf-8"
    else:
        encoding = g.app.tkEncoding
        
    return encoding
#@nonl
#@-node:ekr.20041117151301.1:startupEncoding
#@+node:ekr.20031218072017.1624:createFrame (leo.py)
def createFrame (fileName):
    
    """Create a LeoFrame during Leo's startup process."""
    
    import leoGlobals as g
    
    # g.trace(g.app.tkEncoding,fileName)

    # Try to create a frame for the file.
    if fileName:
        fileName = g.os_path_join(os.getcwd(),fileName)
        fileName = g.os_path_normpath(fileName)
        head,ext = g.os_path_splitext(fileName)
        if not ext:fileName = fileName + ".leo"
        if g.os_path_exists(fileName):
            ok, frame = g.openWithFileName(fileName,None)
            if ok:
                return frame.c,frame
    
    # Create a new frame & indicate it is the startup window.
    c,frame = g.app.gui.newLeoCommanderAndFrame(fileName=fileName)
    frame.setInitialWindowGeometry()
    frame.startupWindow = True
    
    # Report the failure to open the file.
    if fileName:
        g.es("File not found: " + fileName)

    return c,frame
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
    
    name = None ; i = 1 # Skip the dummy first arg.
    while i + 1 < len(sys.argv):
        arg = sys.argv[i].strip().lower()
        if arg in ("--script","-script"):
            name = sys.argv[i+1].strip() ; break
        i += 1

    if not name: return None	
    name = g.os_path_join(g.app.loadDir,name)
    try:
        f = None
        try:
            f = open(name,'r')
            script = f.read()
            # g.trace("script",script)
        except IOError:
            g.es("can not open script file: " + name, color="red")
            script = None
    finally:
        if f: f.close()
        return script
#@nonl
#@-node:ekr.20031218072017.1939:getBatchScript
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
