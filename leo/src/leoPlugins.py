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

#@@language python
#@@tabwidth -4
#@@pagewidth 80

import leoGlobals as g

handlers = {}
loadedModules = {} # Keys are module names, values are modules.

#@+others
#@+node:ekr.20050102094729:callTagHandler
def callTagHandler (handler,tag,keywords):
    
    if tag == 'idle':
        
        if 0:
            c = keywords.get('c')
            g.trace(c.shortFileName(),handler)

        # Make sure all commanders exist.
        for key in ('c','old_c','new_c'):
            c = keywords.get(key)
            if c:
                try:
                    if c.frame not in g.app.windowList:
                        return None # c has (or will be) destroyed.
                except AttributeError:
                    # c has been destroyed: c.frame ivar does not exist.
                    return None

    return handler(tag,keywords)
#@nonl
#@-node:ekr.20050102094729:callTagHandler
#@+node:ekr.20041001161108:doPlugins
def doPlugins(tag,keywords):
    if g.app.killed:
        return
    if tag == "start1":
        loadHandlers()

    return doHandlersForTag(tag,keywords)
#@nonl
#@-node:ekr.20041001161108:doPlugins
#@+node:ekr.20031218072017.3440:loadHandlers
def loadHandlers(loadAllFlag=False):

    """Load all enabled plugins from the plugins directory"""
    import glob

    plugins_path = g.os_path_join(g.app.loadDir,"..","plugins")
    manager_path = g.os_path_join(plugins_path,"pluginsManager.txt")
    
    files = glob.glob(g.os_path_join(plugins_path,"*.py"))
    files = [g.os_path_abspath(theFile) for theFile in files]

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
            theFile = open(manager_path)
            lines = theFile.readlines()
            for s in lines:
                s = s.strip()
                if s and not g.match(s,0,"#"):
                    path = g.os_path_join(plugins_path,s)
                    if path not in enabled_files:
                        enabled_files.append(path)
            theFile.close()
        except IOError:
            g.es("Can not open: " + manager_path)
            # Don't import leoTest initially.  It causes problems.
            import leoTest ; leoTest.fail()
            return
        #@nonl
        #@-node:ekr.20031218072017.3441:<< set enabled_files from pluginsManager.txt >>
        #@nl
        enabled_files = [g.os_path_abspath(theFile) for theFile in enabled_files]
    
    # Load plugins in the order they appear in the enabled_files list.
    if files and enabled_files:
        for theFile in enabled_files:
            if theFile in files:
                loadOnePlugin(theFile)
                
    # Note: g.plugin_signon adds module names to g.app.loadedPlugins 
    if g.app.loadedPlugins and not loadAllFlag:
        g.es("%d plugins loaded" % (len(g.app.loadedPlugins)), color="blue")
#@nonl
#@-node:ekr.20031218072017.3440:loadHandlers
#@+node:ekr.20041113113140:loadOnePlugin
def loadOnePlugin (moduleOrFileName, verbose=False):
    
    global loadedModules
    
    if moduleOrFileName [-3:] == ".py":
        moduleName = moduleOrFileName [:-3]
    else:
        moduleName = moduleOrFileName

    if isLoaded(moduleName):
        module = loadedModules.get(moduleName)
        return module

    plugins_path = g.os_path_join(g.app.loadDir,"..","plugins")
    moduleName = g.toUnicode(moduleName,g.app.tkEncoding)
    result = g.importFromPath(moduleName,plugins_path)
    if result:
        loadedModules[moduleName] = result
    
    if verbose:
        if result is None:
            g.es("can not load %s plugin" % moduleName,color="blue")
        else:
            g.es("loaded %s plugin" % moduleName,color="blue")
    
    return result
#@nonl
#@-node:ekr.20041113113140:loadOnePlugin
#@+node:ekr.20031218072017.3442:doHandlersForTag
def doHandlersForTag (tag,keywords):
    
    """Execute all handlers for a given tag, in alphabetical order.
    
    All exceptions are caught by the caller, doHook."""

    global handlers

    if g.app.killed:
        return None

    if handlers.has_key(tag):
        fns = handlers.get(tag)
        # Execute hooks in some random order.
        # Return if one of them returns a non-None result.
        for fn in fns:
            val = callTagHandler(fn,tag,keywords)
            if val is not None:
                return val

    if handlers.has_key("all"):
        fns = handlers.get("all")
        for fn in fns:
            callTagHandler(fn,tag,keywords)

    return None
#@nonl
#@-node:ekr.20031218072017.3442:doHandlersForTag
#@+node:ekr.20041001160216:isLoaded
def isLoaded (name):
    
    return name in g.app.loadedPlugins
#@nonl
#@-node:ekr.20041001160216:isLoaded
#@+node:ekr.20041111124831:getHandlersForTag
def getHandlersForTag(tags):
    
    import types

    if type(tags) in (types.TupleType,types.ListType):
        result = []
        for tag in tags:
            fn = getHandlersForOneTag(tag)
            result.append((tag,fn),)
        return result
    else:
        return getHandlersForOneTag(tags)

def getHandlersForOneTag (tag):

    global handlers
    
    return handlers.get(tag)
#@nonl
#@-node:ekr.20041111124831:getHandlersForTag
#@+node:ekr.20041114113029:getPluginModule
def getPluginModule (moduleName):
    
    global loadedModules
    
    return loadedModules.get(moduleName)
#@nonl
#@-node:ekr.20041114113029:getPluginModule
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
    
    items = handlers.get(tag,[])
    if fn not in items:
        items.append(fn)
        
    # g.trace(tag) ; g.printList(items)
    handlers[tag] = items
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
#@nonl
#@-node:ekr.20031218072017.3444:registerExclusiveHandler
#@+node:ekr.20041111123313:unregisterHandler
def unregisterHandler(tags,fn):
    
    import types

    if type(tags) in (types.TupleType,types.ListType):
        for tag in tags:
            unregisterOneHandler(tag,fn)
    else:
        unregisterOneHandler(tags,fn)

def unregisterOneHandler (tag,fn):

    global handlers

    fn_list = handlers.get(tag)
    if fn_list:
        while fn in fn_list:
            fn_list.remove(fn)
        handlers[tag] = fn_list
        # g.trace(handlers.get(tag))
#@nonl
#@-node:ekr.20041111123313:unregisterHandler
#@-others
#@-node:ekr.20031218072017.3439:@thin leoPlugins.py
#@-leo
