#@+leo-ver=4-thin
#@+node:ekr.20031218072017.3439:@thin leoPlugins.py
"""Install and run Leo plugins.

On startup:
- doPlugins() calls loadHandlers() to import all
  mod_XXXX.py files in the Leo directory.

- Imported files should register hook handlers using the
  registerHandler and registerExclusiveHandler functions.
  Only one "exclusive" function is allowed per hook.

After startup:
- doPlugins() calls doHandlersForTag() to handle the hook.
- The first non-None return is sent back to Leo.
"""

import leoGlobals as g

handlers = {}

def doPlugins(tag,keywords):
    if g.app.killed:
        return
    if tag == "start1":
        loadHandlers()
    return doHandlersForTag(tag,keywords)
        
#@+others
#@+node:ekr.20031218072017.3440:loadHandlers
def loadHandlers(loadAllFlag=False):

    """Load all enabled plugins from the plugins directory"""
    import glob,os
    
    plugins_path = g.os_path_join(g.app.loadDir,"..","plugins")
    manager_path = g.os_path_join(plugins_path,"pluginsManager.txt")
    
    files = glob.glob(g.os_path_join(plugins_path,"*.py"))
    files = [g.os_path_abspath(file) for file in files]

    if loadAllFlag:
        files.sort()
        enabled_files = files
    else:
        #@        << set enabled_files from pluginsManager.txt >>
        #@+node:ekr.20031218072017.3441:<< set enabled_files from pluginsManager.txt >>
        if not g.os_path_exists(manager_path):
            return
        
        enabled_files = []
        try:
            file = open(manager_path)
            lines = file.readlines()
            for s in lines:
                s = s.strip()
                if s and not g.match(s,0,"#"):
                    enabled_files.append(g.os_path_join(plugins_path,s))
            file.close()
        except:
            g.es("Can not open: " + manager_path)
            import leoTest ; leoTest.fail()
            return
        #@nonl
        #@-node:ekr.20031218072017.3441:<< set enabled_files from pluginsManager.txt >>
        #@nl
        enabled_files = [g.os_path_abspath(file) for file in enabled_files]
    
    # Load plugins in the order they appear in the enabled_files list.
    g.app.loadedPlugins = []
    if files and enabled_files:
        for file in enabled_files:
            if file in files:
                file = g.toUnicode(file,g.app.tkEncoding)
                g.importFromPath(file,plugins_path)
    if g.app.loadedPlugins and not loadAllFlag:
        g.es("%d plugins loaded" % (len(g.app.loadedPlugins)), color="blue")
        if 0:
            for name in g.app.loadedPlugins:
                print name
#@nonl
#@-node:ekr.20031218072017.3440:loadHandlers
#@+node:ekr.20031218072017.3442:doHandlersForTag
def doHandlersForTag (tag,keywords):
    
    """Execute all handlers for a given tag, in alphabetical order"""

    global handlers
    
    # g.trace(g.app.killed)
    
    if g.app.killed:
        return None

    if handlers.has_key(tag):
        handle_fns = handlers[tag]
        handle_fns.sort()
        for handle_fn in handle_fns:
            ret = handle_fn(tag,keywords)
            if ret is not None:
                return ret

    if handlers.has_key("all"):
        handle_fns = handlers["all"]
        handle_fns.sort()
        for handle_fn in handle_fns:
            ret = handle_fn(tag,keywords)
            if ret is not None:
                return ret
    return None
#@-node:ekr.20031218072017.3442:doHandlersForTag
#@+node:ekr.20031218072017.3443:registerHandler
def registerHandler(tags,fn):
    
    """ Register one or more handlers"""
    
    import types

    if type(tags) in (types.TupleType,types.ListType):
        for tag in tags:
            registerOneHandler(tag,fn)
    else:
        registerOneHandler(tags,fn)

def registerOneHandler(tag,fn):
    
    """Register one handler"""

    global handlers

    existing = handlers.setdefault(tag,[])
    existing.append(fn)
#@nonl
#@-node:ekr.20031218072017.3443:registerHandler
#@+node:ekr.20031218072017.3444:registerExclusiveHandler
def registerExclusiveHandler(tags, fn):
    
    """ Register one or more exclusive handlers"""
    
    import types
    
    if type(tags) in (types.TupleType,types.ListType):
        for tag in tags:
            registerOneExclusiveHandler(tag,fn)
    else:
        registerOneExclusiveHandler(tags,fn)
            
def registerOneExclusiveHandler(tag, fn):
    
    """Register one exclusive handler"""
    
    global handlers
    
    if handlers.has_key(tag):
        g.es("*** Two exclusive handlers for '%s'" % tag)
    else:
        handlers[tag] = (fn,)
#@-node:ekr.20031218072017.3444:registerExclusiveHandler
#@-others
#@-node:ekr.20031218072017.3439:@thin leoPlugins.py
#@-leo
