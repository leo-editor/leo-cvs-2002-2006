#@+leo-ver=4-thin
#@+node:ekr.20041117062700:@thin leoConfig.py
#@@language python
#@@tabwidth -4
#@@pagewidth 80

#@<< imports >>
#@+node:ekr.20041227063801:<< imports >>
import leoGlobals as g
import leoGui

if 1: # Used by settings controller.
    import leoNodes
    import leoTkinterTree

    Pmw = g.importExtension("Pmw",pluginName="leoConfig.py",verbose=False)

    import Tkinter as Tk
    import tkColorChooser
    import tkFont

import sys
#@nonl
#@-node:ekr.20041227063801:<< imports >>
#@nl

#@<< class parserBaseClass >>
#@+node:ekr.20041119203941.2:<< class parserBaseClass >>
class parserBaseClass:
    
    """The base class for settings parsers."""
    
    #@    << parserBaseClass data >>
    #@+node:ekr.20041121130043:<< parserBaseClass data >>
    # These are the canonicalized names.  Case is ignored, as are '_' and '-' characters.
    
    basic_types = [
        # Headlines have the form @kind name = var
        'bool','color','directory','int','ints',
        'float','path','ratio','shortcut','string','strings']
    
    control_types = [
        'font','if','ifgui','ifplatform','ignore','page',
        'settings','shortcuts']
    
    # Keys are settings names, values are (type,value) tuples.
    settingsDict = {}
    #@nonl
    #@-node:ekr.20041121130043:<< parserBaseClass data >>
    #@nl
    
    #@    @+others
    #@+node:ekr.20041119204700: ctor (parserBaseClass)
    def __init__ (self,c):
        
        self.c = c
        self.recentFiles = [] # List of recent files.
        
        # Keys are canonicalized names.
        self.dispatchDict = {
            'bool':         self.doBool,
            'color':        self.doColor,
            'directory':    self.doDirectory,
            'font':         self.doFont,
            'if':           self.doIf,
            'ifgui':        self.doIfGui,
            'ifplatform':   self.doIfPlatform,
            'ignore':       self.doIgnore,
            'int':          self.doInt,
            'ints':         self.doInts,
            'float':        self.doFloat,
            'path':         self.doPath,
            'page':         self.doPage,
            'ratio':        self.doRatio,
            'shortcut':     self.doShortcut,
            'shortcuts':    self.doShortcuts,
            'string':       self.doString,
            'strings':      self.doStrings,
        }
    #@nonl
    #@-node:ekr.20041119204700: ctor (parserBaseClass)
    #@+node:ekr.20041120103012:error
    def error (self,s):
    
        print s
    
        # Does not work at present because we are using a null Gui.
        g.es(s,color="blue")
    #@nonl
    #@-node:ekr.20041120103012:error
    #@+node:ekr.20041120094940:kind handlers (parserBaseClass)
    #@+node:ekr.20041120094940.1:doBool
    def doBool (self,p,kind,name,val):
    
        if val in ('True','true','1'):
            self.set(p,kind,name,True)
        elif val in ('False','false','0'):
            self.set(p,kind,name,False)
        else:
            self.valueError(p,kind,name,val)
    #@nonl
    #@-node:ekr.20041120094940.1:doBool
    #@+node:ekr.20041120094940.2:doColor
    def doColor (self,p,kind,name,val):
        
        # At present no checking is done.
        self.set(p,kind,name,val)
    #@nonl
    #@-node:ekr.20041120094940.2:doColor
    #@+node:ekr.20041120094940.3:doDirectory & doPath
    def doDirectory (self,p,kind,name,val):
        
        # At present no checking is done.
        self.set(p,kind,name,val)
    
    doPath = doDirectory
    #@nonl
    #@-node:ekr.20041120094940.3:doDirectory & doPath
    #@+node:ekr.20041120094940.6:doFloat
    def doFloat (self,p,kind,name,val):
        
        try:
            val = float(val)
            self.set(p,kind,name,val)
        except ValueError:
            self.valueError(p,kind,name,val)
    #@nonl
    #@-node:ekr.20041120094940.6:doFloat
    #@+node:ekr.20041120094940.4:doFont
    def doFont (self,p,kind,name,val):
        
        __pychecker__ = '--no-argsused' # kind not used.
        
        d = self.parseFont(p)
        
        # Set individual settings.
        for key in ('family','size','slant','weight'):
            data = d.get(key)
            if data is not None:
                name,val = data
                setKind = key
                self.set(p,setKind,name,val)
    #@nonl
    #@-node:ekr.20041120094940.4:doFont
    #@+node:ekr.20041120103933:doIf
    def doIf(self,p,kind,name,val):
        
        __pychecker__ = '--no-argsused' # args not used.
    
        g.trace("'if' not supported yet")
        return None
    #@nonl
    #@-node:ekr.20041120103933:doIf
    #@+node:ekr.20041121125416:doIfGui
    def doIfGui (self,p,kind,name,val):
        
        __pychecker__ = '--no-argsused' # args not used.
        
        # g.trace(repr(name))
        
        if not g.app.gui or not g.app.gui.guiName():
            s = '@if-gui has no effect: g.app.gui not defined yet'
            g.es_print(s,color='blue')
            return "skip"
        elif g.app.gui.guiName().lower() == name.lower():
            return None
        else:
            return "skip"
    #@nonl
    #@-node:ekr.20041121125416:doIfGui
    #@+node:ekr.20041120104215:doIfPlatform
    def doIfPlatform (self,p,kind,name,val):
        
        __pychecker__ = '--no-argsused' # args not used.
        
        # g.trace(sys.platform,repr(name))
    
        if sys.platform.lower() == name.lower():
            return None
        else:
            return "skip"
    #@nonl
    #@-node:ekr.20041120104215:doIfPlatform
    #@+node:ekr.20041120104215.1:doIgnore
    def doIgnore(self,p,kind,name,val):
    
        return "skip"
    #@nonl
    #@-node:ekr.20041120104215.1:doIgnore
    #@+node:ekr.20041120094940.5:doInt
    def doInt (self,p,kind,name,val):
        
        try:
            val = int(val)
            self.set(p,kind,name,val)
        except ValueError:
            self.valueError(p,kind,name,val)
    #@nonl
    #@-node:ekr.20041120094940.5:doInt
    #@+node:ekr.20041217132253:doInts
    def doInts (self,p,kind,name,val):
        
        '''We expect either:
        @ints [val1,val2,...]aName=val
        @ints aName[val1,val2,...]=val'''
    
        name = name.strip() # The name indicates the valid values.
        i = name.find('[')
        j = name.find(']')
        
        # g.trace(kind,name,val)
    
        if -1 < i < j:
            items = name[i+1:j]
            items = items.split(',')
            name = name[:i]+name[j+1:].strip()
            # g.trace(name,items)
            try:
                items = [int(item.strip()) for item in items]
            except ValueError:
                items = []
                self.valueError(p,'ints[]',name,val)
                return
            kind = "ints[%s]" % (','.join([str(item) for item in items]))
            try:
                val = int(val)
            except ValueError:
                self.valueError(p,'int',name,val)
                return
            if val not in items:
                self.error("%d is not in %s in %s" % (val,kind,name))
                return
    
            # g.trace(repr(kind),repr(name),val)
    
            # At present no checking is done.
            self.set(p,kind,name,val)
    #@nonl
    #@-node:ekr.20041217132253:doInts
    #@+node:ekr.20041120104215.2:doPage
    def doPage(self,p,kind,name,val):
    
        pass # Ignore @page this while parsing settings.
    #@nonl
    #@-node:ekr.20041120104215.2:doPage
    #@+node:ekr.20041121125741:doRatio
    def doRatio (self,p,kind,name,val):
        
        try:
            val = float(val)
            if 0.0 <= val <= 1.0:
                self.set(p,kind,name,val)
            else:
                self.valueError(p,kind,name,val)
        except ValueError:
            self.valueError(p,kind,name,val)
    #@nonl
    #@-node:ekr.20041121125741:doRatio
    #@+node:ekr.20041120113848:doShortcut
    def doShortcut(self,p,kind,name,val):
    
        self.set(p,kind,name,val)
        self.setShortcut(name,val)
    #@nonl
    #@-node:ekr.20041120113848:doShortcut
    #@+node:ekr.20041120105609:doShortcuts
    def doShortcuts(self,p,kind,name,val):
        
        __pychecker__ = '--no-argsused' # kind not used.
        
        #g.trace('*'*10,p.headString())
    
        s = p.bodyString()
        lines = g.splitLines(s)
        for line in lines:
            line = line.strip()
            if line and not g.match(line,0,'#'):
                name,val = self.parseShortcutLine(line)
                # g.trace(name,val)
                if val is not None:
                    self.set(p,"shortcut",name,val)
                    self.setShortcut(name,val)
    #@nonl
    #@-node:ekr.20041120105609:doShortcuts
    #@+node:ekr.20041217132028:doString
    def doString (self,p,kind,name,val):
        
        # At present no checking is done.
        self.set(p,kind,name,val)
    #@-node:ekr.20041217132028:doString
    #@+node:ekr.20041120094940.8:doStrings
    def doStrings (self,p,kind,name,val):
        
        '''We expect one of the following:
        @strings aName[val1,val2...]=val
        @strings [val1,val2,...]aName=val'''
        
        name = name.strip()
        i = name.find('[')
        j = name.find(']')
    
        if -1 < i < j:
            items = name[i+1:j]
            items = items.split(',')
            items = [item.strip() for item in items]
            name = name[:i]+name[j+1:].strip()
            kind = "strings[%s]" % (','.join(items))
            # g.trace(repr(kind),repr(name),val)
    
            # At present no checking is done.
            self.set(p,kind,name,val)
    #@nonl
    #@-node:ekr.20041120094940.8:doStrings
    #@-node:ekr.20041120094940:kind handlers (parserBaseClass)
    #@+node:ekr.20041124063257:munge
    def munge(self,s):
        
        return g.app.config.canonicalizeSettingName(s)
    #@nonl
    #@-node:ekr.20041124063257:munge
    #@+node:ekr.20041119204700.2:oops
    def oops (self):
        print ("parserBaseClass oops:",
            g.callerName(2),
            "must be overridden in subclass")
    #@-node:ekr.20041119204700.2:oops
    #@+node:ekr.20041213082558:parsers
    #@+node:ekr.20041213083651:fontSettingNameToFontKind
    def fontSettingNameToFontKind (self,name):
        
        s = name.strip()
        if s:
            for tag in ('_family','_size','_slant','_weight'):
                if s.endswith(tag):
                    return tag[1:]
    
        return None
    #@nonl
    #@-node:ekr.20041213083651:fontSettingNameToFontKind
    #@+node:ekr.20041213082558.1:parseFont
    def parseFont (self,p):
        
        d = {
            'comments': [],
            'family': None,
            'size': None,
            'slant': None,
            'weight': None,
        }
    
        s = p.bodyString()
        lines = g.splitLines(s)
    
        for line in lines:
            self.parseFontLine(line,d)
            
        comments = d.get('comments')
        d['comments'] = '\n'.join(comments)
            
        return d
    #@nonl
    #@-node:ekr.20041213082558.1:parseFont
    #@+node:ekr.20041213082558.2:parseFontLine
    def parseFontLine (self,line,d):
        
        s = line.strip()
        if not s: return
        
        try:
            s = str(s)
        except UnicodeError:
            pass
        
        if g.match(s,0,'#'):
            s = s[1:].strip()
            comments = d.get('comments')
            comments.append(s)
            d['comments'] = comments
        else:
            # name is everything up to '='
            i = s.find('=')
            if i == -1:
                name = s ; val = None
            else:
                name = s[:i].strip() ; val = s[i+1:].strip()
    
            fontKind = self.fontSettingNameToFontKind(name)
            if fontKind:
                d[fontKind] = name,val # Used only by doFont.
    #@nonl
    #@-node:ekr.20041213082558.2:parseFontLine
    #@+node:ekr.20041119205148:parseHeadline
    def parseHeadline (self,s):
        
        """Parse a headline of the form @kind:name=val
        Return (kind,name,val)."""
    
        kind = name = val = None
    
        if g.match(s,0,'@'):
            i = g.skip_id(s,1,chars='-')
            kind = s[1:i].strip()
            if kind:
                # name is everything up to '='
                j = s.find('=',i)
                if j == -1:
                    name = s[i:].strip()
                else:
                    name = s[i:j].strip()
                    # val is everything after the '='
                    val = s[j+1:].strip()
    
        # g.trace("%50s %10s %s" %(name,kind,val))
        return kind,name,val
    #@nonl
    #@-node:ekr.20041119205148:parseHeadline
    #@+node:ekr.20041120112043:parseShortcutLine
    def parseShortcutLine (self,s):
        
        """Return the kind of @settings node indicated by p's headline."""
        
        name = val = None
        i = g.skip_id(s,0)
        name = s[0:i]
        if name:
            i = g.skip_ws(s,i)
            if g.match(s,i,'='):
                i = g.skip_ws(s,i+1)
                val = s[i:]
    
        # g.trace("%30s %s" %(name,val))
        return name,val
    #@nonl
    #@-node:ekr.20041120112043:parseShortcutLine
    #@-node:ekr.20041213082558:parsers
    #@+node:ekr.20041120094940.9:set (parseBaseClass)
    def set (self,p,kind,name,val):
        
        """Init the setting for name to val."""
        
        __pychecker__ = '--no-argsused' # p used in subclasses, not here.
        
        c = self.c ; key = self.munge(name)
        # g.trace("settingsParser %10s %15s %s" %(kind,val,name))
        d = self.settingsDict
        bunch = d.get(key)
        if bunch:
            # g.trace(key,bunch.val,bunch.path)
            path = bunch.path
            if g.os_path_abspath(c.mFileName) != g.os_path_abspath(path):
                g.es("over-riding setting: %s from %s" % (name,path))
    
        # N.B.  We can't use c here: it may be destroyed!
        d[key] = g.Bunch(path=c.mFileName,kind=kind,val=val,tag='setting')
        
        # g.trace('parserBaseClass',g.shortFileName(c.mFileName),key,val)
    #@nonl
    #@-node:ekr.20041120094940.9:set (parseBaseClass)
    #@+node:ekr.20041227071423:setShortcut (ParserBaseClass)
    def setShortcut (self,name,val):
        
        # g.trace(name,val)
        
        c = self.c
        
        # None is a valid value for val.
        key = c.frame.menu.canonicalizeMenuName(name)
        rawKey = key.replace('&','')
        self.set(c,rawKey,"shortcut",val)
    #@nonl
    #@-node:ekr.20041227071423:setShortcut (ParserBaseClass)
    #@+node:ekr.20041119204700.1:traverse (parserBaseClass)
    def traverse (self):
        
        c = self.c
        
        p = g.app.config.settingsRoot(c)
        if not p:
            return None
    
        self.settingsDict = {}
        after = p.nodeAfterTree()
        while p and p != after:
            result = self.visitNode(p)
            # g.trace(result,p.headString())
            if result == "skip":
                s = 'skipping settings in %s' % p.headString()
                g.es_print(s,color='blue')
                p.moveToNodeAfterTree()
            else:
                p.moveToThreadNext()
                
        return self.settingsDict
    #@nonl
    #@-node:ekr.20041119204700.1:traverse (parserBaseClass)
    #@+node:ekr.20041120094940.10:valueError
    def valueError (self,p,kind,name,val):
        
        """Give an error: val is not valid for kind."""
        
        __pychecker__ = '--no-argsused' # p not used, but needed.
        
        self.error("%s is not a valid %s for %s" % (val,kind,name))
    #@nonl
    #@-node:ekr.20041120094940.10:valueError
    #@+node:ekr.20041119204700.3:visitNode (must be overwritten in subclasses)
    def visitNode (self,p):
        
        __pychecker__ = '--no-argsused' # p not used, but needed.
        
        self.oops()
    #@nonl
    #@-node:ekr.20041119204700.3:visitNode (must be overwritten in subclasses)
    #@-others
#@nonl
#@-node:ekr.20041119203941.2:<< class parserBaseClass >>
#@nl

#@+others
#@+node:ekr.20041119203941:class configClass
class configClass:
    """A class to manage configuration settings."""
    #@    << class data >>
    #@+node:ekr.20041122094813:<<  class data >>
    #@+others
    #@+node:ekr.20041117062717.1:defaultsDict
    #@+at 
    #@nonl
    # This contains only the "interesting" defaults.
    # Ints and bools default to 0, floats to 0.0 and strings to "".
    #@-at
    #@@c
    
    defaultBodyFontSize = g.choose(sys.platform=="win32",9,12)
    defaultLogFontSize  = g.choose(sys.platform=="win32",8,12)
    defaultTreeFontSize = g.choose(sys.platform=="win32",9,12)
    
    defaultsDict = {'_hash':'defaultsDict'}
    
    defaultsData = (
        # compare options...
        ("ignore_blank_lines","bool",True),
        ("limit_count","int",9),
        ("print_mismatching_lines","bool",True),
        ("print_trailing_lines","bool",True),
        # find/change options...
        ("search_body","bool",True),
        ("whole_word","bool",True),
        # Prefs panel.
        ("default_target_language","language","python"),
        ("target_language","language","python"), # Bug fix: 6/20,2005.
        ("tab_width","int",-4),
        ("page_width","int",132),
        ("output_doc_chunks","bool",True),
        ("tangle_outputs_header","bool",True),
        # Syntax coloring options...
        # Defaults for colors are handled by leoColor.py.
        ("color_directives_in_plain_text","bool",True),
        ("underline_undefined_section_names","bool",True),
        # Window options...
        ("allow_clone_drags","bool",True),
        ("body_pane_wraps","bool",True),
        ("body_text_font_family","family","Courier"),
        ("body_text_font_size","size",defaultBodyFontSize),
        ("body_text_font_slant","slant","roman"),
        ("body_text_font_weight","weight","normal"),
        ("enable_drag_messages","bool",True),
        ("headline_text_font_family","string",None),
        ("headline_text_font_size","size",defaultLogFontSize),
        ("headline_text_font_slant","slant","roman"),
        ("headline_text_font_weight","weight","normal"),
        ("log_text_font_family","string",None),
        ("log_text_font_size","size",defaultLogFontSize),
        ("log_text_font_slant","slant","roman"),
        ("log_text_font_weight","weight","normal"),
        ("initial_window_height","int",600),
        ("initial_window_width","int",800),
        ("initial_window_left","int",10),
        ("initial_window_top","int",10),
        ("initial_splitter_orientation","string","vertical"),
        ("initial_vertical_ratio","ratio",0.5),
        ("initial_horizontal_ratio","ratio",0.3),
        ("initial_horizontal_secondary_ratio","ratio",0.5),
        ("initial_vertical_secondary_ratio","ratio",0.7),
        ("outline_pane_scrolls_horizontally","bool",False),
        ("split_bar_color","color","LightSteelBlue2"),
        ("split_bar_relief","relief","groove"),
        ("split_bar_width","int",7),
    )
    #@nonl
    #@-node:ekr.20041117062717.1:defaultsDict
    #@+node:ekr.20041118062709:define encodingIvarsDict
    encodingIvarsDict = {'_hash':'encodingIvarsDict'}
    
    encodingIvarsData = (
        ("default_derived_file_encoding","string","utf-8"),
        ("new_leo_file_encoding","string","UTF-8"),
            # Upper case for compatibility with previous versions.
        ("tkEncoding","string",None),
            # Defaults to None so it doesn't override better defaults.
    )
    #@nonl
    #@-node:ekr.20041118062709:define encodingIvarsDict
    #@+node:ekr.20041117072055:ivarsDict
    # Each of these settings sets the corresponding ivar.
    # Also, the c.configSettings settings class inits the corresponding commander ivar.
    ivarsDict = {'_hash':'ivarsDict'}
    
    ivarsData = (
        ("at_root_bodies_start_in_doc_mode","bool",True),
            # For compatibility with previous versions.
        ("create_nonexistent_directories","bool",False),
        ("output_initial_comment","string",""),
            # "" for compatibility with previous versions.
        ("output_newline","string","nl"),
        ("page_width","int","132"),
        ("read_only","bool",True),
            # Make sure we don't alter an illegal leoConfig.txt file!
        ("redirect_execute_script_output_to_log_pane","bool",False),
        ("relative_path_base_directory","string","!"),
        ("remove_sentinels_extension","string",".txt"),
        ("save_clears_undo_buffer","bool",False),
        ("stylesheet","string",None),
        ("tab_width","int",-4),
        ("target_language","language","python"), # Bug fix: added: 6/20/2005.
        ("trailing_body_newlines","string","asis"),
        ("use_plugins","bool",True),
            # New in 4.3: use_plugins = True by default.
        # use_pysco can not be set by 4.3:  config processing happens too late.
            # ("use_psyco","bool",False),
        ("undo_granularity","string","word"),
            # "char","word","line","node"
        ("write_strips_blank_lines","bool",False),
    )
    #@nonl
    #@-node:ekr.20041117072055:ivarsDict
    #@-others
        
    # List of dictionaries to search.  Order not too important.
    dictList = [ivarsDict,encodingIvarsDict,defaultsDict]
    
    # Keys are commanders.  Values are optionsDicts.
    localOptionsDict = {}
    
    localOptionsList = []
        
    # Keys are setting names, values are type names.
    warningsDict = {} # Used by get() or allies.
    #@nonl
    #@-node:ekr.20041122094813:<<  class data >>
    #@nl
    #@    @+others
    #@+node:ekr.20041117083202:Birth... (g.app.config)
    #@+node:ekr.20041117062717.2:ctor
    def __init__ (self):
        
        self.configsExist = False # True when we successfully open a setting file.
        self.defaultFont = None # Set in gui.getDefaultConfigFont.
        self.defaultFontFamily = None # Set in gui.getDefaultConfigFont.
        self.globalConfigFile = None # Set in initSettingsFiles
        self.homeFile = None # Set in initSettingsFiles
        self.inited = False
        self.recentFilesFiles = [] # List of g.Bunches describing .leoRecentFiles.txt files.
        
        # Inited later...
        self.panes = None
        self.sc = None
        self.tree = None
    
        self.initDicts()
        self.initIvarsFromSettings()
        self.initSettingsFiles()
        self.initRecentFiles()
    #@nonl
    #@-node:ekr.20041117062717.2:ctor
    #@+node:ekr.20041227063801.2:initDicts
    def initDicts (self):
        
        # Only the settings parser needs to search all dicts.
        self.dictList = [self.defaultsDict]
    
        for key,kind,val in self.defaultsData:
            self.defaultsDict[self.munge(key)] = g.Bunch(
                setting=key,kind=kind,val=val,tag='defaults')
            
        for key,kind,val in self.ivarsData:
            self.ivarsDict[self.munge(key)] = g.Bunch(
                ivar=key,kind=kind,val=val,tag='ivars')
    
        for key,kind,val in self.encodingIvarsData:
            self.encodingIvarsDict[self.munge(key)] = g.Bunch(
                ivar=key,kind=kind,encoding=val,tag='encodings')
    #@nonl
    #@-node:ekr.20041227063801.2:initDicts
    #@+node:ekr.20041117065611.2:initIvarsFromSettings & helpers
    def initIvarsFromSettings (self):
        
        for ivar in self.encodingIvarsDict.keys():
            if ivar != '_hash':
                self.initEncoding(ivar)
            
        for ivar in self.ivarsDict.keys():
            if ivar != '_hash':
                self.initIvar(ivar)
    #@nonl
    #@+node:ekr.20041117065611.1:initEncoding
    def initEncoding (self,key):
        
        '''Init g.app.config encoding ivars during initialization.'''
        
        # N.B. The key is munged.
        bunch = self.encodingIvarsDict.get(key)
        encoding = bunch.encoding
        ivar = bunch.ivar
        # g.trace('g.app.config',ivar,encoding)
        setattr(self,ivar,encoding)
     
        if encoding and not g.isValidEncoding(encoding):
            g.es("g.app.config: bad encoding: %s: %s" % (ivar,encoding))
    #@nonl
    #@-node:ekr.20041117065611.1:initEncoding
    #@+node:ekr.20041117065611:initIvar
    def initIvar(self,key):
        
        '''Init g.app.config ivars during initialization.
        
        This does NOT init the corresponding commander ivars.
        
        Such initing must be done in setIvarsFromSettings.'''
        
        # N.B. The key is munged.
        bunch = self.ivarsDict.get(key)
        ivar = bunch.ivar # The actual name of the ivar.
        val = bunch.val
    
        # g.trace('g.app.config',ivar,key,val)
        setattr(self,ivar,val)
    #@nonl
    #@-node:ekr.20041117065611:initIvar
    #@-node:ekr.20041117065611.2:initIvarsFromSettings & helpers
    #@+node:ekr.20041117083202.2:initRecentFiles
    def initRecentFiles (self):
    
        self.recentFiles = []
    #@nonl
    #@-node:ekr.20041117083202.2:initRecentFiles
    #@+node:ekr.20041117083857:initSettingsFiles
    def initSettingsFiles (self):
        
        """Set self.globalConfigFile, self.homeFile"""
    
        dirs = [] # Directories that have already been searched.
        
        for ivar,theDir in (
            ("globalConfigFile",g.app.globalConfigDir),
            ("homeFile",g.app.homeDir),
        ):
    
            if theDir not in dirs:
                dirs.append(theDir)
                path = g.os_path_join(theDir,"leoSettings.leo")
                if g.os_path_exists(path):
                    setattr(self,ivar,path)
                else:
                    setattr(self,ivar,None)
                 
        if 0:   
            g.trace("globalConfigFile",g.app.globalConfigDir)
            g.trace("homeFile",g.app.homeDir)
    #@nonl
    #@-node:ekr.20041117083857:initSettingsFiles
    #@-node:ekr.20041117083202:Birth... (g.app.config)
    #@+node:ekr.20041117081009:Getters... (g.app.config)
    #@+node:ekr.20041123070429:canonicalizeSettingName (munge)
    def canonicalizeSettingName (self,name):
        
        if name is None:
            return None
    
        name = name.lower()
        for ch in ('-','_',' ','\n'):
            name = name.replace(ch,'')
            
        return g.choose(name,name,None)
        
    munge = canonicalizeSettingName
    #@nonl
    #@-node:ekr.20041123070429:canonicalizeSettingName (munge)
    #@+node:ekr.20041123092357:config.findSettingsPosition
    def findSettingsPosition (self,c,setting):
        
        """Return the position for the setting in the @settings tree for c."""
        
        munge = self.munge
        
        root = self.settingsRoot(c)
        if not root:
            return c.nullPosition()
            
        setting = munge(setting)
            
        for p in root.subtree_iter():
            h = munge(p.headString())
            if h == setting:
                return p.copy()
        
        return c.nullPosition()
    #@nonl
    #@-node:ekr.20041123092357:config.findSettingsPosition
    #@+node:ekr.20041117083141:get & allies (g.app.config)
    def get (self,c,setting,kind):
        
        """Get the setting and make sure its type matches the expected type."""
        
        found = False
        if c:
            d = self.localOptionsDict.get(c.hash())
            if d:
                val,found = self.getValFromDict(d,setting,kind,found)
                if val is not None:
                    # g.trace(c.shortFileName(),setting,val)
                    return val
                    
        for d in self.localOptionsList:
            val,found = self.getValFromDict(d,setting,kind,found)
            if val is not None:
                kind = d.get('_hash','<no hash>')
                # g.trace(kind,setting,val)
                return val
    
        for d in self.dictList:
            val,found = self.getValFromDict(d,setting,kind,found)
            if val is not None:
                kind = d.get('_hash','<no hash>')
                # g.trace(kind,setting,val)
                return val
                    
        if 0: # Good for debugging leoSettings.leo.  This is NOT an error.
            # Don't warn if None was specified.
            if not found:
                g.trace("Not found:",setting)
    
        return None
    #@nonl
    #@+node:ekr.20041121143823:getValFromDict
    def getValFromDict (self,d,setting,requestedType,found):
        
        __pychecker__ = '--no-argsused' # reqestedType not used.
    
        bunch = d.get(self.munge(setting))
        if bunch:
            # g.trace(setting,requestedType,bunch.toString())
            found = True ; val = bunch.val
            if val not in (u'None',u'none','None','none','',None):
                # g.trace(setting,val)
                return val,found
    
        # Do NOT warn if not found here.  It may be in another dict.
        return None,found
    #@nonl
    #@-node:ekr.20041121143823:getValFromDict
    #@-node:ekr.20041117083141:get & allies (g.app.config)
    #@+node:ekr.20041117081009.3:getBool
    def getBool (self,c,setting):
        
        """Search all dictionaries for the setting & check it's type"""
        
        val = self.get(c,setting,"bool")
        
        if val in (True,False):
            return val
        else:
            return None
    #@nonl
    #@-node:ekr.20041117081009.3:getBool
    #@+node:ekr.20041122070339:getColor
    def getColor (self,c,setting):
        
        """Search all dictionaries for the setting & check it's type"""
        
        return self.get(c,setting,"color")
    #@nonl
    #@-node:ekr.20041122070339:getColor
    #@+node:ekr.20041117093009.1:getDirectory
    def getDirectory (self,c,setting):
        
        """Search all dictionaries for the setting & check it's type"""
        
        theDir = self.getString(c,setting)
    
        if g.os_path_exists(theDir) and g.os_path_isdir(theDir):
             return theDir
        else:
            return None
    #@nonl
    #@-node:ekr.20041117093009.1:getDirectory
    #@+node:ekr.20041117082135:getFloat
    def getFloat (self,c,setting):
        
        """Search all dictionaries for the setting & check it's type"""
        
        val = self.get(c,setting,"float")
        try:
            val = float(val)
            return val
        except TypeError:
            return None
    #@nonl
    #@-node:ekr.20041117082135:getFloat
    #@+node:ekr.20041117062717.13:getFontFromParams (config)
    def getFontFromParams(self,c,family,size,slant,weight,defaultSize=12,tag="<unknown>"):
    
        """Compute a font from font parameters.
    
        Arguments are the names of settings to be use.
        We default to size=12, slant="roman", weight="normal".
    
        We return None if there is no family setting so we can use system default fonts."""
        
        __pychecker__ = '--no-argsused' # tag used for debugging.
    
        family = self.get(c,family,"family")
        if family in (None,""):
            family = self.defaultFontFamily
    
        size = self.get(c,size,"size")
        if size in (None,0): size = defaultSize
        
        slant = self.get(c,slant,"slant")
        if slant in (None,""): slant = "roman"
    
        weight = self.get(c,weight,"weight")
        if weight in (None,""): weight = "normal"
        
        # g.trace(tag,family,size,slant,weight,g.shortFileName(c.mFileName))
        
        return g.app.gui.getFontFromParams(family,size,slant,weight)
    #@nonl
    #@-node:ekr.20041117062717.13:getFontFromParams (config)
    #@+node:ekr.20041117081513:getInt
    def getInt (self,c,setting):
        
        """Search all dictionaries for the setting & check it's type"""
        
        val = self.get(c,setting,"int")
        try:
            val = int(val)
            return val
        except TypeError:
            return None
    #@nonl
    #@-node:ekr.20041117081513:getInt
    #@+node:ekr.20041117093009.2:getLanguage
    def getLanguage (self,c,setting):
        
        """Return the setting whose value should be a language known to Leo."""
        
        language = self.getString(c,setting)
        # g.trace(setting,language)
        
        return language
    #@nonl
    #@-node:ekr.20041117093009.2:getLanguage
    #@+node:ekr.20041122070752:getRatio
    def getRatio (self,c,setting):
        
        """Search all dictionaries for the setting & check it's type"""
        
        val = self.get(c,setting,"ratio")
        try:
            val = float(val)
            if 0.0 <= val <= 1.0:
                return val
            else:
                return None
        except TypeError:
            return None
    #@nonl
    #@-node:ekr.20041122070752:getRatio
    #@+node:ekr.20041117062717.11:getRecentFiles
    def getRecentFiles (self):
    
        return self.recentFiles
    #@nonl
    #@-node:ekr.20041117062717.11:getRecentFiles
    #@+node:ekr.20041117062717.14:getShortcut (config)
    def getShortcut (self,c,shortcutName):
        
        '''Return rawKey,accel for shortcutName'''
        
        key = c.frame.menu.canonicalizeMenuName(shortcutName)
        rawKey = key.replace('&','') # Allow '&' in names.
        val = self.get(c,rawKey,"shortcut")
        if val is None:
             return rawKey,None
        else:
            # g.trace(key,val)
            return rawKey,val
    #@nonl
    #@-node:ekr.20041117062717.14:getShortcut (config)
    #@+node:ekr.20041117081009.4:getString
    def getString (self,c,setting):
        
        """Search all dictionaries for the setting & check it's type"""
    
        return self.get(c,setting,"string")
    #@nonl
    #@-node:ekr.20041117081009.4:getString
    #@+node:ekr.20041117062717.17:setCommandsIvars
    # Sets ivars of c that can be overridden by leoConfig.txt
    
    def setCommandsIvars (self,c):
    
        data = (
            ("default_tangle_directory","tangle_directory","directory"),
            ("default_target_language","target_language","language"),
            ("output_doc_chunks","output_doc_flag","bool"),
            ("page_width","page_width","int"),
            ("run_tangle_done.py","tangle_batch_flag","bool"),
            ("run_untangle_done.py","untangle_batch_flag","bool"),
            ("tab_width","tab_width","int"),
            ("tangle_outputs_header","use_header_flag","bool"),
        )
        
        for setting,ivar,theType in data:
            val = g.app.config.get(c,setting,theType)
            if val is None:
                if not hasattr(c,setting):
                    setattr(c,setting,None)
                    # g.trace(setting,None)
            else:
                setattr(c,setting,val)
                # g.trace(setting,val)
    #@nonl
    #@-node:ekr.20041117062717.17:setCommandsIvars
    #@+node:ekr.20041120074536:settingsRoot
    def settingsRoot (self,c):
    
        for p in c.allNodes_iter():
            if p.headString().rstrip() == "@settings":
                return p.copy()
        else:
            return c.nullPosition()
    #@nonl
    #@-node:ekr.20041120074536:settingsRoot
    #@-node:ekr.20041117081009:Getters... (g.app.config)
    #@+node:ekr.20041118084146:Setters (g.app.config)
    #@+node:ekr.20041118084146.1:set (g.app.config)
    def set (self,c,setting,kind,val):
        
        '''Set the setting.  Not called during initialization.'''
    
        found = False ;  key = self.munge(setting)
        if c:
            d = self.localOptionsDict.get(c.hash())
            if d: found = True
    
        if not found:
            theHash = c.hash()
            for d in self.localOptionsList:
                hash2 = d.get('_hash')
                if theHash == hash2:
                    found = True ; break
    
        if not found:
            d = self.dictList [0]
    
        d[key] = g.Bunch(setting=setting,kind=kind,val=val,tag='setting')
        # g.trace(d.get(key).toString())
    
        if 0:
            dkind = d.get('_hash','<no hash: %s>' % c.hash())
            g.trace(dkind,setting,kind,val)
    #@nonl
    #@-node:ekr.20041118084146.1:set (g.app.config)
    #@+node:ekr.20041118084241:setString
    def setString (self,c,setting,val):
        
        self.set(c,setting,"string",val)
    #@nonl
    #@-node:ekr.20041118084241:setString
    #@+node:ekr.20041228042224:setIvarsFromSettings (g.app.config)
    def setIvarsFromSettings (self,c):
    
        '''Init g.app.config ivars or c's ivars from settings.
        
        - Called from readSettingsFiles with c = None to init g.app.config ivars.
        - Called from c.__init__ to init corresponding commmander ivars.'''
        
        # Ingore temporary commanders created by readSettingsFiles.
        if not self.inited: return
    
        # g.trace(c)
        d = self.ivarsDict
        for key in d:
            if key != '_hash':
                bunch = d.get(key)
                if bunch:
                    ivar = bunch.ivar # The actual name of the ivar.
                    kind = bunch.kind
                    val = self.get(c,key,kind) # Don't use bunch.val!
                    if c:
                        # g.trace("%20s %s = %s" % (g.shortFileName(c.mFileName),ivar,val))
                        setattr(c,ivar,val)
                    else:
                        # g.trace("%20s %s = %s" % ('g.app.config',ivar,val))
                        setattr(self,ivar,val)
    #@nonl
    #@-node:ekr.20041228042224:setIvarsFromSettings (g.app.config)
    #@+node:ekr.20041201080436:appendToRecentFiles (g.app.config)
    def appendToRecentFiles (self,files):
        
        files = [theFile.strip() for theFile in files]
        
        # g.trace(files)
        
        def munge(name):
            name = name or ''
            return g.os_path_normpath(name).lower()
        
        for name in files:
            # Remove all variants of name.
            for name2 in self.recentFiles:
                if munge(name) == munge(name2):
                    self.recentFiles.remove(name2)
    
            self.recentFiles.append(name)
    #@nonl
    #@-node:ekr.20041201080436:appendToRecentFiles (g.app.config)
    #@-node:ekr.20041118084146:Setters (g.app.config)
    #@+node:ekr.20041117093246:Scanning @settings (g.app.config)
    #@+node:ekr.20041117085625:openSettingsFile
    def openSettingsFile (self,path):
        
        try:
            # Open the file in binary mode to allow 0x1a in bodies & headlines.
            theFile = open(path,'rb')
        except IOError:
            g.es("can not open: " + path, color="blue")
            return None
            
        # Similar to g.openWithFileName except it uses a null gui.
        # Changing g.app.gui here is a major hack.
        oldGui = g.app.gui
        g.app.gui = leoGui.nullGui("nullGui")
        c,frame = g.app.gui.newLeoCommanderAndFrame(path,updateRecentFiles=False)
        frame.log.enable(False)
        g.app.setLog(frame.log,"openWithFileName")
        g.app.lockLog()
        ok = frame.c.fileCommands.open(
            theFile,path,readAtFileNodesFlag=False,silent=True) # closes theFile.
        g.app.unlockLog()
        frame.openDirectory = g.os_path_dirname(path)
        g.app.gui = oldGui
        return ok and c
    #@nonl
    #@-node:ekr.20041117085625:openSettingsFile
    #@+node:ekr.20041120064303:config.readSettingsFiles
    def readSettingsFiles (self,fileName,verbose=True):
        
        seen = []
        
        # Init settings from leoSettings.leo files.
        for path,localFlag in (
            (self.globalConfigFile,False),
            (self.homeFile,False),
            (fileName,True),
        ):
            if path and path.lower() not in seen:
                seen.append(path.lower())
                if verbose:
                    g.es_print('reading settings in %s' % path)
                c = self.openSettingsFile(path)
                if c:
                    d = self.readSettings(c)
                    if d:
                        d['_hash'] = theHash = c.hash()
                        if localFlag:
                            self.localOptionsDict[theHash] = d
                        else:
                            self.localOptionsList.insert(0,d)
                    g.app.destroyWindow(c.frame)
                self.readRecentFilesFile(path)
    
        self.inited = True
        self.setIvarsFromSettings(None)
    #@nonl
    #@-node:ekr.20041120064303:config.readSettingsFiles
    #@+node:ekr.20041117083857.1:readSettings
    # Called to read all leoSettings.leo files.
    # Also called when opening an .leo file to read @settings tree.
    
    def readSettings (self,c):
        
        """Read settings from a file that may contain an @settings tree."""
        
        # g.trace(c.fileName())
        
        # Create a settings dict for c for set()
        if c and self.localOptionsDict.get(c.hash()) is None:
            self.localOptionsDict[c.hash()] = {}
    
        parser = settingsTreeParser(c)
        d = parser.traverse()
    
        return d
    #@nonl
    #@-node:ekr.20041117083857.1:readSettings
    #@-node:ekr.20041117093246:Scanning @settings (g.app.config)
    #@+node:ekr.20050424114937.1:Reading and writing .leoRecentFiles.txt (g.app.config)
    #@+node:ekr.20050424115658:readRecentFilesFile
    def readRecentFilesFile (self,path):
        
        # Set the kind of file for later.
        for path2,kind in (
            (self.globalConfigFile,'global'),
            (self.homeFile,'home'),
        ):
            if path2 and path2 == path: break
        else:
            kind = 'local'
    
        path,junk = g.os_path_split(path)
        fileName = g.os_path_join(path,'.leoRecentFiles.txt')
        
        if not g.os_path_exists(fileName):
            # g.trace('----- no file',kind,fileName)
            return
    
        for bunch in self.recentFilesFiles:
            if bunch.fileName == fileName:
                # g.trace('-----already read',kind,fileName)
                return
                
        # g.trace('-----',kind,fileName)
        self.recentFilesFiles.append(
            g.Bunch(fileName=fileName,kind=kind))
    
        lines = file(fileName).readlines()
        if lines and self.munge(lines[0])=='readonly':
            lines = lines[1:]
        if lines:
            self.appendToRecentFiles(lines)
    #@nonl
    #@-node:ekr.20050424115658:readRecentFilesFile
    #@+node:ekr.20050424114937.2:writeRecentFilesFile & helper
    def writeRecentFilesFile (self,c):
        
        '''Write the appropriate .leoRecentFiles.txt file.'''
        
        tag = '.leoRecentFiles.txt'
        
        localFileName = c.fileName()
        if not localFileName:
            # g.trace('----no file name')
            return
            
        # Create a list of bunches to control the comparison below.
        files = []
        for fileName,kind in (
            (localFileName,'local'),
            (self.homeFile,'home'),
            (self.globalConfigFile,'global'),
        ):
            if fileName:
                path,junk = g.os_path_split(fileName)
                files.append(g.Bunch(
                    fileName=g.os_path_join(path,tag),kind=kind))
    
        # Search local file first, then home and global files.                
        for kind in ('local','home','global'):
            for bunch in files:
                for bunch2 in self.recentFilesFiles:
                    if bunch.kind == bunch2.kind:
                        # g.trace('----- comparing',bunch.kind,bunch.fileName)
                        if bunch.fileName == bunch2.fileName:
                            self.writeRecentFilesFileHelper(bunch.fileName)
                            return
                        
        # g.trace('----- not found:',localFileName)
    #@nonl
    #@+node:ekr.20050424131051:writeRecentFilesFileHelper
    def writeRecentFilesFileHelper (self,fileName):
        # g.trace(fileName)
        
        # Don't update the file if it begins with read-only.
        theFile = None
        try:
            theFile = file(fileName)
            lines = theFile.readlines()
            if lines and self.munge(lines[0])=='readonly':
                # g.trace('read-only: %s' %fileName)
                return
        except IOError:
            # The user may have erased a file.  Not an error.
            if theFile: theFile.close()
    
        theFile = None
        try:
            # g.trace('writing',fileName)
            theFile = file(fileName,'w')
            if self.recentFiles:
                theFile.write('\n'.join(self.recentFiles))
            else:
                theFile.write('\n')
    
        except IOError:
            # The user may have erased a file.  Not an error.
            pass
                
        except Exception:
            g.es('unexpected exception writing %s' % fileName,color='red')
            g.es_exception()
        
        if theFile:
            theFile.close()
    #@nonl
    #@-node:ekr.20050424131051:writeRecentFilesFileHelper
    #@-node:ekr.20050424114937.2:writeRecentFilesFile & helper
    #@-node:ekr.20050424114937.1:Reading and writing .leoRecentFiles.txt (g.app.config)
    #@-others
#@nonl
#@-node:ekr.20041119203941:class configClass
#@+node:ekr.20041225063637.96:class settingsDialogParserClass (parserBaseClass)
class settingsDialogParserClass (parserBaseClass):
    
    '''A class that traverses the settings tree creating
    a list of widgets to show in the settings dialog.'''
    
    #@    @+others
    #@+node:ekr.20041225063637.97:ctor
    # There is no need to call the base class ctor.
    __pychecker__ = '--no-callinit'
    
    def __init__ (self,c,p,controller):
        self.c = c
        self.controller = controller
        self.root = p.copy()
        self.widgets = [] # A list of widgets to create in the setter pane.
    
        # Keys are canonicalized names.
        self.dispatchDict = {
            'bool':         self.set,
            'color':        self.set,
            'directory':    self.doDirectory,
            'font':         self.doFont,
            'if':           self.doIf,
            'ifgui':        None,
            'ifplatform':   None,
            'ignore':       None,
            'int':          self.set,
            'ints':         self.doInts,
            'float':        self.set,
            'font':         self.doFont,
            'path':         self.doPath,
            'page':         self.doPage,
            'ratio':        self.set,
            'shortcut':     None,
            'shortcuts':    self.doShortcuts,
            'string':       self.set,
            'strings':      self.doStrings,
        }
    #@nonl
    #@-node:ekr.20041225063637.97:ctor
    #@+node:ekr.20041225063637.98:set (settingsDialogParserClass)
    def set (self,p,kind,name,val):
        
        self.widgets.append((p.copy(),kind,name,val),)
    #@nonl
    #@-node:ekr.20041225063637.98:set (settingsDialogParserClass)
    #@+node:ekr.20041225063637.99:visitNode (settingsDialogParserClass)
    def visitNode (self,p):
        
        """Visit a node, and possibly append a widget description to self.widgets."""
        
        munge = g.app.config.munge
        h = p.headString().strip() or ''
        kind,name,val = self.parseHeadline(h)
        
        # g.trace(kind,name,val)
    
        f = self.dispatchDict.get(munge(kind)) or self.doComment
        if f is not None:
            try:
                return f(p,kind,name,val)
            except TypeError:
                g.es_exception()
                print "*** no handler",kind
                return None
    #@nonl
    #@-node:ekr.20041225063637.99:visitNode (settingsDialogParserClass)
    #@+node:ekr.20041225063637.100:kind handlers (settingsDialogParserClass)
    # Most of the work is done by base class methods.
    #@nonl
    #@+node:ekr.20050603065400:doComment
    def doComment (self,p,kind,name,val):
        
        __pychecker__ = '--no-argsused' # args not used, but required.
    
        self.set(p,'comment',None,None)
    #@nonl
    #@-node:ekr.20050603065400:doComment
    #@+node:ekr.20041225063637.101:doFont
    def doFont (self,p,kind,name,val):
        
        __pychecker__ = '--no-argsused' # args not used, but required.
    
        d = self.parseFont(p)
        # g.trace("\n\nfont dict...\n%s" % g.dictToString(d))
        self.set(p,kind,name,d)
    #@-node:ekr.20041225063637.101:doFont
    #@+node:ekr.20041225063637.102:doPage
    def doPage(self,p,kind,name,val):
        
        """Create a widget for each setting in the subtree."""
        
        __pychecker__ = '--no-argsused' # args not used, but required.
    
        for p in p.subtree_iter():
            self.visitNode(p)
    #@nonl
    #@-node:ekr.20041225063637.102:doPage
    #@+node:ekr.20041225063637.103:doRecentFiles & doBodyPaneList
    def doBodyPaneList (self,p,kind,name,val):
        
        __pychecker__ = '--no-argsused' # val not used, but required.
    
        s = p.bodyString()
        lines = g.splitLines(s)
    
        vals = []
        for line in lines:
            line = line.strip()
            if line and not g.match(line,0,'#'):
                vals.append(line)
                    
        self.set(p,kind,name,vals)
    #@-node:ekr.20041225063637.103:doRecentFiles & doBodyPaneList
    #@+node:ekr.20041225063637.104:doShortcuts
    def doShortcuts(self,p,kind,name,val):
        
        __pychecker__ = '--no-argsused' # val not used, but required.
    
        s = p.bodyString()
        self.set(p,kind,name,s)
        self.controller.suppressComments=p.copy()
    #@nonl
    #@-node:ekr.20041225063637.104:doShortcuts
    #@-node:ekr.20041225063637.100:kind handlers (settingsDialogParserClass)
    #@-others
#@-node:ekr.20041225063637.96:class settingsDialogParserClass (parserBaseClass)
#@+node:ekr.20041225063637.78:class settingsTree (leoTkinterTree)
class settingsTree (leoTkinterTree.leoTkinterTree):

    #@    @+others
    #@+node:ekr.20041225063637.79:ctor
    def __init__(self,c,frame,canvas,controller):
        
        # Init the base class.
        leoTkinterTree.leoTkinterTree.__init__(self,c,frame,canvas)
        
        self.controller = controller
        self.old_p = None
    #@nonl
    #@-node:ekr.20041225063637.79:ctor
    #@+node:ekr.20041225063637.80:Selecting & editing...
    # This code is different because this class has a different current position.
    
    #@+node:ekr.20041225123250:configureTextState
    def configureTextState (self,p):
        
        if p:
            t = self.getTextWidget(p)
            if t:
                if p.isCurrentPosition():
                    self.setSelectColors(t)
                else:
                    self.setUnselectColors(t)
    #@nonl
    #@+node:ekr.20041225063637.89:setSelectColors
    def setSelectColors (self,textWidget): 
        
        c = self.c
    
        fg = c.config.getColor("headline_text_selected_foreground_color") or 'black'
        bg = c.config.getColor("headline_text_selected_background_color") or 'white'
    
        try:
            textWidget.configure(state="disabled",
            highlightthickness=0,fg=fg,bg=bg,
            selectforeground=fg,selectbackground=bg)
        except:
            g.es_exception()
    #@nonl
    #@-node:ekr.20041225063637.89:setSelectColors
    #@+node:ekr.20041225063637.90:setUnselectColors
    def setUnselectColors (self,textWidget): 
        
        c = self.c
        
        fg = c.config.getColor("headline_text_unselected_foreground_color") or 'black'
        bg = c.config.getColor("headline_text_unselected_background_color") or 'white'
    
        try:
            textWidget.configure(state="disabled",highlightthickness=0,fg=fg,bg=bg)
        except:
            g.es_exception()
    #@nonl
    #@-node:ekr.20041225063637.90:setUnselectColors
    #@-node:ekr.20041225123250:configureTextState
    #@+node:ekr.20041225063637.81:endEditLabel
    def endEditLabel (self):
        
        pass # Editing is not allowed.
    #@nonl
    #@-node:ekr.20041225063637.81:endEditLabel
    #@+node:ekr.20041225063637.82:editLabel
    def editLabel (self,p):
        
        pass # Editing is not allowed.
    #@nonl
    #@-node:ekr.20041225063637.82:editLabel
    #@+node:ekr.20041225063637.83:tree.select
    def select (self,p,updateBeadList=True):
        
        __pychecker__ = '--no-argsused' # updateBeadList required for compatibility.
    
        old_p = self.old_p
        
        # g.trace(p.headString())
    
        # Unselect the old
        if old_p:
            t = self.getTextWidget(old_p)
            if t: self.setUnselectColors(t)
    
        # Select the new
        t = self.getTextWidget(p)
        if t: self.setSelectColors(t)
        
        # N.B. Do not change the commander's notion of the present position.
        self.old_p = p
    
        self.controller.onTreeClick(p)
        
        # For the UNL plugin.
        g.doHook("select2",c=p.c,new_p=p,old_p=old_p,new_v=p,old_v=old_p)
    #@nonl
    #@-node:ekr.20041225063637.83:tree.select
    #@+node:ekr.20041225063637.91:getTextWidget
    def getTextWidget (self,p):
        
        # The data is create in newText.
        data = self.visibleText.get(p.v)
        if data:
            data = data[0] # A list of one element.
            # g.trace(len(data),data)
            p2,t,theId = data
            return t
        else:
            return None
    #@nonl
    #@-node:ekr.20041225063637.91:getTextWidget
    #@-node:ekr.20041225063637.80:Selecting & editing...
    #@+node:ekr.20041225063637.92:Event handlers...
    #@+node:ekr.20041225063637.93:expandAllAncestors
    def expandAllAncestors (self,p):
        
        # This would be harmful because p is always c.currentPosition().
    
        return False # redraw_flag
    #@nonl
    #@-node:ekr.20041225063637.93:expandAllAncestors
    #@+node:ekr.20041225063637.94:onClickBoxClick
    def onClickBoxClick (self,event):
        
        tree = self
    
        p = self.eventToPosition(event)
        if not p: return
    
        # g.trace(p.isExpanded(),p.headString())
    
        if p.isExpanded(): p.contract()
        else:              p.expand()
    
        tree.active = True
        tree.redraw()
        tree.select(p)
    #@nonl
    #@-node:ekr.20041225063637.94:onClickBoxClick
    #@-node:ekr.20041225063637.92:Event handlers...
    #@+node:ekr.20041225063637.95:drawTopTree
    def drawTopTree (self):
        
        """Draw the settings tree, i.e., the tree rooted at self.controller.settingsPosition()."""
        
        canvas = self.canvas
        p = self.controller.settingsPosition()
        self.redrawing = True
        # Recycle all widgets.
        self.recycleWidgets()
        # Clear all ids so invisible id's don't confuse eventToPosition & findPositionWithIconId
        self.ids = {}
        self.iconIds = {}
        self.generation += 1
        self.drag_p = None # Disable drags across redraws.
        self.dragging = False
        self.prevPositions = g.app.positions
        
        # Draw only the settings tree
        self.drawTree(p,self.root_left,self.root_top,0,0)
    
        canvas.lower("lines")  # Lowest.
        canvas.lift("textBox") # Not the Tk.Text widget: it should be low.
        canvas.lift("userIcon")
        canvas.lift("plusBox")
        canvas.lift("clickBox")
        canvas.lift("iconBox") # Higest.
        self.redrawing = False
    #@nonl
    #@-node:ekr.20041225063637.95:drawTopTree
    #@-others
#@nonl
#@-node:ekr.20041225063637.78:class settingsTree (leoTkinterTree)
#@+node:ekr.20041119203941.3:class settingsTreeParser (parserBaseClass)
class settingsTreeParser (parserBaseClass):
    
    '''A class that inits settings found in an @settings tree.
    
    Used by read settings logic.'''
    
    #@    @+others
    #@+node:ekr.20041119204103:ctor
    def __init__ (self,c):
    
        # Init the base class.
        parserBaseClass.__init__(self,c)
    #@nonl
    #@-node:ekr.20041119204103:ctor
    #@+node:ekr.20041119204714:visitNode (settingsTreeParser)
    def visitNode (self,p):
        
        """Init any settings found in node p."""
        
        # g.trace(p.headString())
        
        munge = g.app.config.munge
    
        kind,name,val = self.parseHeadline(p.headString())
        kind = munge(kind)
    
        if kind == "settings":
            pass
        elif kind not in self.control_types and val in (u'None',u'none','None','none','',None):
            # None is valid for all data types.
            self.set(p,kind,name,None)
        elif kind in self.control_types or kind in self.basic_types:
            f = self.dispatchDict.get(kind)
            try:
                return f(p,kind,name,val)
            except TypeError:
                g.es_exception()
                print "*** no handler",kind
        elif name:
            # self.error("unknown type %s for setting %s" % (kind,name))
            # Just assume the type is a string.
            self.set(p,kind,name,val)
        
        return None
    #@nonl
    #@-node:ekr.20041119204714:visitNode (settingsTreeParser)
    #@-others
#@nonl
#@-node:ekr.20041119203941.3:class settingsTreeParser (parserBaseClass)
#@+node:ekr.20041225063637.10:class settingsController
class settingsController:
    
    #@    @+others
    #@+node:ekr.20041225063637.13: ctor (settingsController)
    def __init__ (self,c,replaceBody=True):
        
        self.createSummaryNode = True # Works either way.
    
        #@    << init ivars >>
        #@+node:ekr.20050123194330:<< init ivars >>
        self._settingsPosition = None
        self.alterComments = None # position for which to alter comments.
        self.alteredCommentsString = None
        self.c = c
        self.buttonNames = ('OK', 'Cancel','Apply','Revert')
        self.colorSettingDict = {} # Contains entries for all changed colors.
        self.commentWidget = None
        self.commonBackground = None
        self.dialog = None
        self.initValueDict = {} # Initial value of settings in present pane.
        self.fileValueDict = {} # Values of settings written to file.
        self.filesInfoDict = {} # Info about all settings file in the settings outline.
            # Keys are positions, values are dicts giving info for a setting file.
        self.fontRefs = {} # A dict to retain references to fonts.
        self.modal = False
        self.old_p = c.currentPosition()
        self.old_root = c.rootPosition()
        self.p = None # Used to revert settings.
        self.panes = {}
        self.parser = None
        self.replaceBody = replaceBody
        self.sc = None
        self.setterLabel = None
        self.suppressComments = None # position for which to suppress comments.
        self.title = "Settings for %s" % g.shortFileName(c.fileName())
        self.top = None
        self.tree = None
        #@nonl
        #@-node:ekr.20050123194330:<< init ivars >>
        #@nl
        #@    << define Tk color names>>
        #@+node:ekr.20050129111522:<< define Tk color names >>
        self.colorNamesList = (
            "gray60", "gray70", "gray80", "gray85", "gray90", "gray95",
            "snow1", "snow2", "snow3", "snow4", "seashell1", "seashell2",
            "seashell3", "seashell4", "AntiqueWhite1", "AntiqueWhite2", "AntiqueWhite3",
            "AntiqueWhite4", "bisque1", "bisque2", "bisque3", "bisque4", "PeachPuff1",
            "PeachPuff2", "PeachPuff3", "PeachPuff4", "NavajoWhite1", "NavajoWhite2",
            "NavajoWhite3", "NavajoWhite4", "LemonChiffon1", "LemonChiffon2",
            "LemonChiffon3", "LemonChiffon4", "cornsilk1", "cornsilk2", "cornsilk3",
            "cornsilk4", "ivory1", "ivory2", "ivory3", "ivory4", "honeydew1", "honeydew2",
            "honeydew3", "honeydew4", "LavenderBlush1", "LavenderBlush2",
            "LavenderBlush3", "LavenderBlush4", "MistyRose1", "MistyRose2",
            "MistyRose3", "MistyRose4", "azure1", "azure2", "azure3", "azure4",
            "SlateBlue1", "SlateBlue2", "SlateBlue3", "SlateBlue4", "RoyalBlue1",
            "RoyalBlue2", "RoyalBlue3", "RoyalBlue4", "blue1", "blue2", "blue3", "blue4",
            "DodgerBlue1", "DodgerBlue2", "DodgerBlue3", "DodgerBlue4", "SteelBlue1",
            "SteelBlue2", "SteelBlue3", "SteelBlue4", "DeepSkyBlue1", "DeepSkyBlue2",
            "DeepSkyBlue3", "DeepSkyBlue4", "SkyBlue1", "SkyBlue2", "SkyBlue3",
            "SkyBlue4", "LightSkyBlue1", "LightSkyBlue2", "LightSkyBlue3",
            "LightSkyBlue4", "SlateGray1", "SlateGray2", "SlateGray3", "SlateGray4",
            "LightSteelBlue1", "LightSteelBlue2", "LightSteelBlue3",
            "LightSteelBlue4", "LightBlue1", "LightBlue2", "LightBlue3",
            "LightBlue4", "LightCyan1", "LightCyan2", "LightCyan3", "LightCyan4",
            "PaleTurquoise1", "PaleTurquoise2", "PaleTurquoise3", "PaleTurquoise4",
            "CadetBlue1", "CadetBlue2", "CadetBlue3", "CadetBlue4", "turquoise1",
            "turquoise2", "turquoise3", "turquoise4", "cyan1", "cyan2", "cyan3", "cyan4",
            "DarkSlateGray1", "DarkSlateGray2", "DarkSlateGray3",
            "DarkSlateGray4", "aquamarine1", "aquamarine2", "aquamarine3",
            "aquamarine4", "DarkSeaGreen1", "DarkSeaGreen2", "DarkSeaGreen3",
            "DarkSeaGreen4", "SeaGreen1", "SeaGreen2", "SeaGreen3", "SeaGreen4",
            "PaleGreen1", "PaleGreen2", "PaleGreen3", "PaleGreen4", "SpringGreen1",
            "SpringGreen2", "SpringGreen3", "SpringGreen4", "green1", "green2",
            "green3", "green4", "chartreuse1", "chartreuse2", "chartreuse3",
            "chartreuse4", "OliveDrab1", "OliveDrab2", "OliveDrab3", "OliveDrab4",
            "DarkOliveGreen1", "DarkOliveGreen2", "DarkOliveGreen3",
            "DarkOliveGreen4", "khaki1", "khaki2", "khaki3", "khaki4",
            "LightGoldenrod1", "LightGoldenrod2", "LightGoldenrod3",
            "LightGoldenrod4", "LightYellow1", "LightYellow2", "LightYellow3",
            "LightYellow4", "yellow1", "yellow2", "yellow3", "yellow4", "gold1", "gold2",
            "gold3", "gold4", "goldenrod1", "goldenrod2", "goldenrod3", "goldenrod4",
            "DarkGoldenrod1", "DarkGoldenrod2", "DarkGoldenrod3", "DarkGoldenrod4",
            "RosyBrown1", "RosyBrown2", "RosyBrown3", "RosyBrown4", "IndianRed1",
            "IndianRed2", "IndianRed3", "IndianRed4", "sienna1", "sienna2", "sienna3",
            "sienna4", "burlywood1", "burlywood2", "burlywood3", "burlywood4", "wheat1",
            "wheat2", "wheat3", "wheat4", "tan1", "tan2", "tan3", "tan4", "chocolate1",
            "chocolate2", "chocolate3", "chocolate4", "firebrick1", "firebrick2",
            "firebrick3", "firebrick4", "brown1", "brown2", "brown3", "brown4", "salmon1",
            "salmon2", "salmon3", "salmon4", "LightSalmon1", "LightSalmon2",
            "LightSalmon3", "LightSalmon4", "orange1", "orange2", "orange3", "orange4",
            "DarkOrange1", "DarkOrange2", "DarkOrange3", "DarkOrange4", "coral1",
            "coral2", "coral3", "coral4", "tomato1", "tomato2", "tomato3", "tomato4",
            "OrangeRed1", "OrangeRed2", "OrangeRed3", "OrangeRed4", "red1", "red2", "red3",
            "red4", "DeepPink1", "DeepPink2", "DeepPink3", "DeepPink4", "HotPink1",
            "HotPink2", "HotPink3", "HotPink4", "pink1", "pink2", "pink3", "pink4",
            "LightPink1", "LightPink2", "LightPink3", "LightPink4", "PaleVioletRed1",
            "PaleVioletRed2", "PaleVioletRed3", "PaleVioletRed4", "maroon1",
            "maroon2", "maroon3", "maroon4", "VioletRed1", "VioletRed2", "VioletRed3",
            "VioletRed4", "magenta1", "magenta2", "magenta3", "magenta4", "orchid1",
            "orchid2", "orchid3", "orchid4", "plum1", "plum2", "plum3", "plum4",
            "MediumOrchid1", "MediumOrchid2", "MediumOrchid3", "MediumOrchid4",
            "DarkOrchid1", "DarkOrchid2", "DarkOrchid3", "DarkOrchid4", "purple1",
            "purple2", "purple3", "purple4", "MediumPurple1", "MediumPurple2",
            "MediumPurple3", "MediumPurple4", "thistle1", "thistle2", "thistle3",
            "thistle4" )
        #@nonl
        #@-node:ekr.20050129111522:<< define Tk color names >>
        #@nl
    
        if not Pmw:
            s = 'Setting dialog requires Pmw: see http://pmw.sourceforge.net'
            g.es_print(s,color='red')
            return
        
        # Reread the settings files so any changes will take effect.
        g.app.config.readSettingsFiles(c.fileName(),verbose=True)
        self._settingsPosition = p = self.createSettingsTree()
        self.parser = settingsDialogParserClass(c,p,self)
        #@    << set background color for widgets >>
        #@+node:ekr.20050121105232:<< set background color for widgets >>
        if 0:
            # Get the color from the background color of the body text widget.
            self.commonBackground = c.frame.body.bodyCtrl.cget('background')
            
        else:
            # 'LightSteelBlue1' # too blue.
            # 'gray80' # too dark.
            # 'gray90' # Possible: very light.
            # '#f2fdff' # Same as log window.  Too cute.
            
            self.commonBackground = 'gray90'
        #@nonl
        #@-node:ekr.20050121105232:<< set background color for widgets >>
        #@nl
        c.disableCommandsMessage = 'All commands disabled while settings dialog is open'
        if self.replaceBody:
            self.replaceBodyWithDialog()
            self.log = g.app.log
            self.tree.redraw_now() # To allocate widgets.
            self.tree.select(p)
        else:
            d = self.createStandAloneDialog()
            self.log = self.logClass(self.logText)
            self.tree.redraw_now() # To allocate widgets.
            self.tree.select(p)
            self.center()
            g.app.gui.widgetWantsFocus(None,None)
            if self.modal: d.activate()
    #@nonl
    #@-node:ekr.20041225063637.13: ctor (settingsController)
    #@+node:ekr.20050212153515:replaceBodyWithDialog
    def replaceBodyWithDialog (self):
        
        c = self.c ; bg = self.commonBackground
        
        #@    << replace the body pane with the outer dialog frame >>
        #@+node:ekr.20041225071604:<< replace the body pane with the outer dialog frame >>
        body = c.frame.component('body')
        packer = body.getPacker()
        unpacker = body.getUnpacker()
        
        # The new frame must be a child of splitter1Frame.
        parentFrame = c.frame.component('splitter1Frame').getFrame()
        self.top = interior = Tk.Frame(parentFrame,background=bg)
        
        c.frame.componentClass(c,'settingDialogFrame',interior,self,packer,unpacker)
        c.frame.replaceBodyPaneWithComponent('settingDialogFrame')
        #@nonl
        #@-node:ekr.20041225071604:<< replace the body pane with the outer dialog frame >>
        #@nl
        #@    << replace tree pane with settings tree >>
        #@+node:ekr.20041225090725:<< replace tree pane with settings tree >>
        tree = c.frame.component('tree')
        
        # The new frame must be a child of splitter2Frame.
        splitter2Frame = c.frame.component('splitter2Frame').getFrame()
        
        # Create a Pmw scrolled canvas.
        scrolledTreeCanvas = Pmw.ScrolledCanvas(splitter2Frame,
            hscrollmode='none',borderframe=3)
        
        treeCanvas = scrolledTreeCanvas.component('canvas')
        treeCanvas.configure(background='white')
        
        # Set canvas.name ivar for chapters.py plugin.
        # This must be a tab number.  The number '1' should work well enough.
        treeCanvas.name = '1'
        
        # Create the settingsTree component.
        c.frame.componentClass(c,'settingsTree',scrolledTreeCanvas,self,
            tree.getPacker(),tree.getUnpacker())
        
        c.frame.replaceTreePaneWithComponent('settingsTree')
        
        self.tree = settingsTree(c,c.frame,treeCanvas,self)
        self.tree.setColorFromConfig()
        #@nonl
        #@-node:ekr.20041225090725:<< replace tree pane with settings tree >>
        #@nl
        #@    << add buttons and label to interior >>
        #@+node:ekr.20041225074713:<< add buttons and label to interior >>
        # Put the label on the same line as the buttons.
        labelButtonFrame = Tk.Frame(interior,background=bg)
        labelButtonFrame.pack(side='top',expand=0,fill='x',pady=4)
        buttonFrame = Tk.Frame(labelButtonFrame,background=bg)
        buttonFrame.pack(side='left',padx=10)
        labelFrame = Tk.Frame(labelButtonFrame,background=bg)
        labelFrame.pack(side='left')
        self.setterLabel = label = Tk.Label(labelFrame,anchor='w',background=bg)
        label.pack(side='right')
        
        w = 6
        for name in self.buttonNames:
            w = max(w,len(name))
        
        for name in self.buttonNames:
        
            def buttonCallback(name=name):
                self.onAnyButton(name)
        
            b = Tk.Button(buttonFrame,text=name,command=buttonCallback,width=w)
            b.pack(side='left',padx=4)
        #@nonl
        #@-node:ekr.20041225074713:<< add buttons and label to interior >>
        #@nl
        #@    << add setterCanvas to interior >>
        #@+node:ekr.20041225073207.1:<< add setterCanvas to interior>>
        self.sc = sc = Pmw.ScrolledCanvas(interior,
            hscrollmode='dynamic',vscrollmode='dynamic',
            canvas_background = bg,
            borderframe=1,
            # A fixed size here works best.
            # Pmw does not handle the changes to the canvas very well.
            usehullsize = 1,
            hull_height = 400,
            hull_width = 800,
        )
        
        sc.pack(side='top',expand=1,fill="both")
        #@nonl
        #@-node:ekr.20041225073207.1:<< add setterCanvas to interior>>
        #@nl
    #@nonl
    #@-node:ekr.20050212153515:replaceBodyWithDialog
    #@+node:ekr.20050212153646:createStandAloneDialog
    def createStandAloneDialog (self):
        
        c = self.c ; title = self.title
        bg = self.commonBackground
        
        #@    << create the dialog d >>
        #@+node:ekr.20041225063637.14:<< create the dialog d >>
        self.dialog = d = Pmw.Dialog(
            c.frame.top,
            title=title,
            buttons=self.buttonNames,
            # It's too upsetting to have a dialog go away on a return key.
            # defaultbutton = 'OK',
            command = self.onAnyButton
        )
        
        self.top = hull = d.component('hull')
        hull.minsize(800,800)
        
        interior = d.interior()
        
        if 0: # Do immediately
            g.app.gui.attachLeoIcon(hull)
        else: # Do at idle time.
            def setIcont(top=hull):
                g.app.gui.attachLeoIcon(top)
            hull.after_idle(setIcont)
        #@nonl
        #@-node:ekr.20041225063637.14:<< create the dialog d >>
        #@nl
        #@    << create paneFrame, a paned widget >>
        #@+node:ekr.20041225063637.15:<< create paneFrame, a paned widget >>
        self.paneFrame = paneFrame = Pmw.PanedWidget(interior,
            separatorthickness = 4, # default is 2
            handlesize = 8, # default is 8
            command = self.onPaneResize
        )
        paneFrame.pack(expand = 1, fill='both')
        
        for name,minsize,size,label,isSetterLabel in (
            ("splitter2",50,300,None,False),
            ("setter",50,300,"",False),
            ("comments",50,200,None,False),
        ):
            self.panes[name] = pane = paneFrame.add(name,min=minsize,size=size)
            if label is not None:
                label = Tk.Label(pane,text=label,background=bg)
                label.pack(side = 'top', expand = 0)
                if isSetterLabel:
                    self.setterLabel = label
        
        # Set the colors of the separator and handle.
        for i in (1,2):
            bar = paneFrame.component('separator-%d' % i)
            bar.configure(background='LightSteelBlue2')
            handle = paneFrame.component('handle-%d' % i)
            handle.configure(background='SteelBlue2')
        
        # g.printDict(self.panes)
        #@nonl
        #@-node:ekr.20041225063637.15:<< create paneFrame, a paned widget >>
        #@nl
        #@    << create paneFrame2, a second paned widget >>
        #@+node:ekr.20041225063637.16:<< create paneFrame2, a second paned widget >>
        splitter2 = self.panes.get('splitter2')
        
        self.paneFrame2 = paneFrame2 = Pmw.PanedWidget(splitter2,
            separatorthickness = 4, # default is 2
            handlesize = 8, # default is 8
            orient='horizontal',
            command = self.onPaneResize
        )
        paneFrame2.pack(expand = 1, fill='both')
        
        for name,minsize,size, in (
            ('outline',50,500),
            ('log',50,300),
        ):
            self.panes[name] = pane = paneFrame2.add(name,min=minsize,size=size)
            
        # Set the colors of the separator and handle.
        i = 1
        bar = paneFrame2.component('separator-%d' % i)
        bar.configure(background='LightSteelBlue2')
        handle = paneFrame2.component('handle-%d' % i)
        handle.configure(background='SteelBlue2')
        #@nonl
        #@-node:ekr.20041225063637.16:<< create paneFrame2, a second paned widget >>
        #@nl
        #@    << create outline and log panes in paneFrame2 >>
        #@+node:ekr.20041225063637.17:<< create outline and log panes in paneFrame2 >>
        outline = self.panes.get('outline')
        
        # Create the widget.
        self.scrolledTreeCanvas = scrolledTreeCanvas = Pmw.ScrolledCanvas(outline,
            hscrollmode='none',borderframe=3)
            
        # Configure the canvas component.
        scrolledTreeCanvas.pack(side='top',expand=1,fill="both")
        
        treeCanvas = scrolledTreeCanvas.component('canvas')
        treeCanvas.configure(background='white')
        
        # Create the tree.
        self.tree = settingsTree(c,c.frame,treeCanvas,self)
        
        logPane = self.panes.get('log')
        self.logText = logText = Tk.Text(logPane)
        logText.pack(expand=1,fill="both")
        #@nonl
        #@-node:ekr.20041225063637.17:<< create outline and log panes in paneFrame2 >>
        #@nl
        #@    << put setterCanvas in paneFrame's setter pane>>
        #@+node:ekr.20041225063637.18:<< put setterCanvas in paneFrame's setter pane>>
        # Create the widget in the 'setter' pane.
        setter = self.panes.get('setter')
        
        self.sc = sc = Pmw.ScrolledCanvas(setter,
            hscrollmode='none',vscrollmode='dynamic',
            labelpos = 'n',label_text = '')
            
        sc.pack(side='top',expand=1,fill="both")
        
        sc.component('canvas')
        self.setterLabel = sc.component('label')
        #@nonl
        #@-node:ekr.20041225063637.18:<< put setterCanvas in paneFrame's setter pane>>
        #@nl
        #@    << put a Text widget in the comment pane >>
        #@+node:ekr.20041225063637.19:<< put a Text widget in the comment pane >>
        commentFrame = self.paneFrame.pane('comments')
        
        self.commentWidget = commentWidget = Pmw.ScrolledText(commentFrame)
        commentWidget.pack(expand=1,fill="both")
        
        self.commentText = text = commentWidget.component('text')
        
        background = commentFrame.cget('background')
        text.configure(background=background,borderwidth=0)
        #@nonl
        #@-node:ekr.20041225063637.19:<< put a Text widget in the comment pane >>
        #@nl
        
        return d
    #@nonl
    #@-node:ekr.20050212153646:createStandAloneDialog
    #@+node:ekr.20041225063637.21:createSettingsTree & helpers
    def createSettingsTree (self):
        
        """Create a tree of vnodes representing all settings."""
    
        createEmptyRootNodes = False
        c = self.c ; config = g.app.config
        root_p = None ; last_p = None
        for kind,path,otherFileFlag in (
            ("Global",config.globalConfigFile,True),
            ("Home",config.homeFile,True),
            ("Local",c.fileName(),False),
        ):
            if path:
                if otherFileFlag: c2 = config.openSettingsFile(path)
                else: c2 = c
                root2 = g.app.config.settingsRoot(c2)
            else:
                root2 = None
            if root2 or createEmptyRootNodes:
                #@            << create a node p for kind & root2 >>
                #@+node:ekr.20041225063637.22:<< create a node p for  kind & root2 >>
                if not root_p:
                    t = leoNodes.tnode()
                    root_v = leoNodes.vnode(c,t) # Using c2 --> oops: nullTree.
                    root_p = leoNodes.position(root_v,[])
                    if self.createSummaryNode:
                        root_p.initHeadString("All settings")
                        root_p.scriptSetBodyString(self.rootNodeComments())
                        p = root_p.insertAsLastChild()
                    else:
                        p = root_p.copy()
                    last_p = p.copy()
                else:
                    # Pychecker may complain, but last_p _is_ defined here!
                    p = last_p.insertAfter()
                    last_p = p.copy()
                
                if root2:
                    root2.copyTreeFromSelfTo(p)  # replace p by root2.
                
                self.copyExpansionState(root2,p)
                # g.trace(p.isExpanded(),p.headString())
                
                #@<< add entry for p to filesInfoDict >>
                #@+node:ekr.20041225063637.23:<< add entry for p to filesInfoDict >>
                self.filesInfoDict[p] = {
                    'c': c2,
                    'changes': [],
                    'p': p.copy(),
                    'path': path,
                    'isLocal':  not otherFileFlag,
                }
                #@nonl
                #@-node:ekr.20041225063637.23:<< add entry for p to filesInfoDict >>
                #@nl
                
                path2 = g.choose(otherFileFlag,path,g.shortFileName(path))
                p.initHeadString("%s settings: %s" % (kind,path2))
                #@nonl
                #@-node:ekr.20041225063637.22:<< create a node p for  kind & root2 >>
                #@nl
        if self.createSummaryNode: root_p.expand()
        return root_p
    #@nonl
    #@+node:ekr.20041225063637.24:rootNodeComments
    def rootNodeComments(self):
        
        c = self.c ; fileName = g.shortFileName(c.mFileName)
        
        s = """This tree shows Leo's global and home settings, as well as the local settings in %s."""\
            % (fileName)
        
        return s
    #@nonl
    #@-node:ekr.20041225063637.24:rootNodeComments
    #@-node:ekr.20041225063637.21:createSettingsTree & helpers
    #@+node:ekr.20041225063637.25:createWidgets & helpers
    def createWidgets (self,widgets,parent,p):
    
        munge = g.app.config.munge
    
        #@    << define creatorDispatchDict >>
        #@+node:ekr.20041225063637.26:<< define creatorDispatchDict >>
        creatorDispatchDict = {
            'bool':         self.createBool,
            'color':        self.createColor,
            'comment':      self.createOnlyComments, # New in 4.3.1
            'directory':    self.createDirectory,
            'font':         self.createFont,
            'int':          self.createInt,
            'ints':         self.createInts,
            'float':        self.createFloat,
            'path':         self.createPath,
            'ratio':        self.createRatio,
            'shortcut':     self.createShortcut,
            'shortcuts':    self.createShortcuts,
            'string':       self.createString,
            'strings':      self.createStrings,
        }
        #@nonl
        #@-node:ekr.20041225063637.26:<< define creatorDispatchDict >>
        #@nl
        
        # g.trace(p.headString())
        
        # self.printWidgets(widgets)
        
        self.h = 0 # Offset from top of pane for first widget.
        self.createSpacerFrame(parent,size=15)
        
        if p != self.suppressComments:
            self.createComments(parent,p.copy())
    
        for data in widgets:
            p,kind,name,vals = data
            if kind.startswith('ints'):
                self.createInts(parent,p,kind,name,vals)
            if kind.startswith('strings'):
                self.createStrings(parent,p,kind,name,vals)
            else:
                f = creatorDispatchDict.get(munge(kind))
                if f is not None:
                    try:
                        f(parent,p,kind,name,vals)
                    except TypeError:
                        g.es_exception()
                        g.trace("***No handler***",kind)
    #@nonl
    #@+node:ekr.20041225063637.27:createBool
    def createBool (self,parent,p,kind,name,val):
        
        val = g.choose(val.lower()=='true',1,0)
    
        # Inits the checkbutton widget. 
        var = Tk.IntVar()
        var.set(val)
    
        def boolCallback():
            val2 = g.choose(var.get(),True,False)
            # g.trace(name,val2)
            return val2
        
        val = g.choose(val,True,False)
        self.initValue(p,name,kind,val,boolCallback)
    
        box = Tk.Checkbutton(parent,text=name,variable=var,background=self.commonBackground)
    
        self.sc.create_window(10,self.h,anchor='w',window=box)
        self.h += 30
    #@nonl
    #@-node:ekr.20041225063637.27:createBool
    #@+node:ekr.20041225063637.28:createColor
    def createColor (self,parent,p,kind,name,val):
        
        munge = g.app.config.munge
        noColor = "<no color>"
        colorNamesList = list(self.colorNamesList)
        
        f = Tk.Frame(parent,background=self.commonBackground) # No need to pack.
        #@    << munge val and add val to colorNamesList >>
        #@+node:ekr.20041225063637.29:<< munge val and add val to colorNamesList >>
        if val in ("None",None): val = noColor
        val = str(val) # Get rid of unicode.
        
        if noColor in colorNamesList:
            colorNamesList.remove(val)
        if val is not noColor and val not in colorNamesList:
             colorNamesList.append(val)
        colorNamesList.sort()
        colorNamesList.insert(0,noColor)
        
        initVal = val
        if val is noColor: val = None
        #@nonl
        #@-node:ekr.20041225063637.29:<< munge val and add val to colorNamesList >>
        #@nl
        #@    << create optionMenu and callback >>
        #@+node:ekr.20041225063637.30:<< create optionMenu and callback >>
        colorBox = Pmw.ComboBox(f,scrolledlist_items=colorNamesList)
        colorBox.selectitem(initVal)
        colorBox.pack(side="left",padx=2)
        
        color = g.choose(val is None,f.cget('background'),val)
        colorSample = Tk.Button(f,width=8,background=color)
        colorSample.pack(side='left',padx=2)
        
        def colorCallback (newName):
            # g.trace(repr(newName))
            if not newName or newName.lower() in ('none','<none>','<no color>'):
                self.colorSettingDict[munge(name)] = None
                color = f.cget('background')
                colorSample.configure(background=color)
            else:
                try:
                    colorSample.configure(background=newName)
                    self.colorSettingDict[munge(name)] = g.choose(newName is noColor,None,newName)
                except: pass # Ignore invalid names.
        
        colorBox.configure(selectioncommand=colorCallback)
        #@nonl
        #@-node:ekr.20041225063637.30:<< create optionMenu and callback >>
        #@nl
        #@    << create picker button and callback >>
        #@+node:ekr.20041225063637.31:<< create picker button and callback >>
        def pickerCallback (color=val):
        
            rgb,val = tkColorChooser.askcolor(parent=parent,color=color)
            if rgb or val:
                # g.trace(rgb,val)
                self.colorSettingDict[munge(name)] = val
                colorSample.configure(background=val,activebackground=val,text=val)
        
        b = Tk.Button(f,text="Color Picker...",command=pickerCallback,background=self.commonBackground)
        b.pack(side="left")
        #@nonl
        #@-node:ekr.20041225063637.31:<< create picker button and callback >>
        #@nl
        Tk.Label(f,text=name,background=self.commonBackground).pack(side='left')
        
        self.colorSettingDict [munge(name)] = val
    
        def getColorCallback ():
            return self.colorSettingDict.get(munge(name))
    
        self.initValue(p,name,kind,val,getColorCallback)
    
        self.sc.create_window(15,self.h+8,anchor='w',window=f)
        self.h += 30
    #@nonl
    #@-node:ekr.20041225063637.28:createColor
    #@+node:ekr.20050121131613:createComments
    def createComments (self,parent,p):
        
        # g.trace(p.headString())
        
        bg = self.commonBackground
    
        s = p.bodyString().strip()
        if not s: return
        
        f = Tk.Frame(parent,background=bg) # No need to pack.
    
        scrolled_text = Pmw.ScrolledText(f,
            labelpos = 'ew',label_text='comments',
            hull_background=bg,
            hull_bd=2,hull_relief='groove',
            hull_padx=6,hull_pady=6,
            text_background=bg,
            text_padx=6,text_pady=6,
            text_bd=2,text_relief='sunken',
            label_background=bg,
            text_height=5,text_width=80)
        scrolled_text.pack(side='left',pady=6,padx=6,expand=1,fill='x')
        t = scrolled_text.component('text')
        t.insert('end',s)
        t.configure(state='disabled')
        scrolled_text.component('hull')
    
        self.sc.create_window(10-2,self.h,anchor='w',window=f)
        self.h += 70
    #@nonl
    #@-node:ekr.20050121131613:createComments
    #@+node:ekr.20050603065744:createOnlyComments
    def createOnlyComments (self,parent,p,kind,name,val):
        
        pass # The existence of the 'comments' widget is enough.
    #@nonl
    #@-node:ekr.20050603065744:createOnlyComments
    #@+node:ekr.20041225063637.32:createDirectory
    def createDirectory (self,parent,p,kind,name,val):
        
        self.createString(parent,p,kind,name,val)
    #@nonl
    #@-node:ekr.20041225063637.32:createDirectory
    #@+node:ekr.20041225063637.33:createFloat
    def createFloat (self,parent,p,kind,name,val):
        
        bg = self.commonBackground
    
        # Inits the entry widget.
        var = Tk.StringVar()
        var.set(val)
    
        f = Tk.Frame(parent,background=bg)
        Tk.Entry(f,textvariable=var,background=bg).pack(side='left')
        Tk.Label(f,text=name,background=bg).pack(side='left')
        
        def floatCallback():
            val2 = var.get()
            # g.trace(name,val2)
            try:
                float(val2)
                return val2
            except TypeError:
                g.trace("bad val:",val2)
                return val
                
        self.initValue(p,name,kind,val,floatCallback)
        
        self.sc.create_window(10,self.h,anchor='w',window=f)
        self.h += 30
    #@nonl
    #@-node:ekr.20041225063637.33:createFloat
    #@+node:ekr.20041225063637.34:createFont
    def createFont (self,parent,p,kind,fontName,val):
        
        """Create a font picker.  val is a dict containing the specified values."""
        bg = self.commonBackground
        d = val
        munge = g.app.config.munge
        f = Tk.Frame(parent,background=bg) # No need to pack.
        self.alterComments = p.copy()
        self.alteredCommentsString = d.get('comments')
        #@    << create the family combo box >>
        #@+node:ekr.20041225063637.35:<< create the family combo box >>
        names = tkFont.families()
        names = list(names)
        names.sort()
        names.insert(0,'<None>')
        
        data = d.get('family')
        initialitem = 0
        if data:
            name2,val = data
            if val and val in names:
                initialitem = names.index(val)
        
        familyBox = Pmw.ComboBox(f,
            labelpos="we",label_text='Family:',
            label_background=bg,
            arrowbutton_background=bg,
            scrolledlist_items=names)
        
        familyBox.selectitem(initialitem)
        familyBox.pack(side="left",padx=2)
        #@nonl
        #@-node:ekr.20041225063637.35:<< create the family combo box >>
        #@nl
        #@    << create the size entry >>
        #@+node:ekr.20041225063637.36:<< create the size entry >>
        Tk.Label(f,text="Size:",background=bg).pack(side="left")
        
        sizeEntry = Tk.Entry(f,width=4)
        sizeEntry.pack(side="left")
        
        data = d.get('size')
        if data:
            kind,val = data
            if val not in (None,'None','none'):
                try:
                    int(val)
                    sizeEntry.insert('end',val)
                except ValueError:
                    s = "invalid size: %s" % val
                    print s ; self.es(s,color="blue")
        #@nonl
        #@-node:ekr.20041225063637.36:<< create the size entry >>
        #@nl
        #@    << create the weight combo box >>
        #@+node:ekr.20041225063637.37:<< create the weight combo box >>
        initialitem = 0
        values = ['<None>','normal','bold']
        data = d.get('weight')
        if data:
            kind,val = data
            if val in values:
                initialitem = values.index(val)
        
        weightBox = Pmw.ComboBox(f,
            labelpos="we",label_text="Weight:",
            label_background=bg,
            arrowbutton_background=bg,
            scrolledlist_items=values)
        
        weightBox.selectitem(initialitem)
        weightBox.pack(side="left",padx=2)
        #@nonl
        #@-node:ekr.20041225063637.37:<< create the weight combo box >>
        #@nl
        #@    << create the slant combo box >>
        #@+node:ekr.20041225063637.38:<< create the slant combo box>>
        initialitem = 0
        values=['<None>','roman','italic']
        data = d.get('slant')
        if data:
            kind,val = data
            if val in values:
                initialitem = values.index(val)
        
        slantBox = Pmw.ComboBox(f,
            labelpos="we",label_text="Slant:",
            label_background=bg,
            arrowbutton_background=bg,
            scrolledlist_items=values)
        
        slantBox.selectitem(initialitem)
        slantBox.pack(side="left",padx=2)
        #@nonl
        #@-node:ekr.20041225063637.38:<< create the slant combo box>>
        #@nl
        Tk.Label(f,text=fontName,background=bg).pack(side='left')
        #@    << define fontCallback >>
        #@+node:ekr.20041225063637.39:<< define fontCallback >>
        def fontCallback(*args,**keys):
            
            __pychecker__ = '--no-argsused' # not used, but needed.
            
            d2 = d.copy() # The update logic must compare distinct dicts.
            
            for box,key in (
                (familyBox, 'family'),
                (None,      'size'),
                (slantBox,  'slant'),
                (weightBox, 'weight'),
            ):
                if box: val = box.get()
                else:   val = sizeEntry.get().strip()
                if not val or  val.lower() in ('none','<none>',): val = None
        
                data = d.get(key)
                name,oldval = data
                d2[key] = name,val
            
            return d2
        #@nonl
        #@-node:ekr.20041225063637.39:<< define fontCallback >>
        #@nl
    
        familyBox.configure(selectioncommand=fontCallback)
        slantBox.configure(selectioncommand=fontCallback)
        weightBox.configure(selectioncommand=fontCallback)
    
        self.initValue(p,munge(fontName),'font',d,fontCallback)
    
        self.sc.create_window(15,self.h,anchor='w',window = f)
        self.h += 30
    #@nonl
    #@-node:ekr.20041225063637.34:createFont
    #@+node:ekr.20041225063637.40:createInt
    def createInt (self,parent,p,kind,name,val):
        
        bg = self.commonBackground
    
        # Inits the entry widget.
        var = Tk.StringVar()
        var.set(val)
    
        f = Tk.Frame(parent)
        Tk.Entry(f,textvariable=var).pack(side='left')
        Tk.Label(f,text=name,background=bg).pack(side='left')
    
        def intCallback():
            val2 = var.get()
            # g.trace(name,val2)
            try:
                int(val2)
                return val2
            except TypeError:
                g.trace("bad val:",val2)
                return val
        
        self.initValue(p,name,kind,val,intCallback)
        
        self.sc.create_window(10,self.h,anchor='w',window=f)
        self.h += 30
    #@nonl
    #@-node:ekr.20041225063637.40:createInt
    #@+node:ekr.20041225063637.41:createInts
    def createInts (self,parent,p,kind,name,val):
        
        # g.trace(repr(kind),repr(name),val)
        
        bg = self.commonBackground
        
        i = kind.find('[')
        j = kind.find(']')
        if not (-1 < i < j):
            return
        
        items = kind[i+1:j].split(',')
        items.sort()
        items.insert(0,'<none>')
        
        if val in items:
            initialitem = items.index(val)
        else:
            initialitem = 0
            
        f = Tk.Frame(parent)
    
        intsBox = Pmw.ComboBox(f,
            labelpos="ew",label_text=name,
            label_background=bg,
            scrolledlist_items=items)
    
        intsBox.selectitem(initialitem)
        intsBox.pack(side="left",padx=2)
        
        def intsCallback():
            val2 = intsBox.get()
            try:
                int(val2)
                return val2
            except TypeError:
                g.trace("bad val:",val2)
                return val
    
        self.initValue(p,name,kind,val,intsCallback)
    
        self.sc.create_window(10,self.h,anchor='w',window=f)
        self.h += 30
    #@nonl
    #@-node:ekr.20041225063637.41:createInts
    #@+node:ekr.20041225063637.42:createPath
    def createPath (self,parent,p,kind,name,val):
        
        self.createString(parent,p,kind,name,val)
    #@nonl
    #@-node:ekr.20041225063637.42:createPath
    #@+node:ekr.20041225063637.43:createRatio
    def createRatio (self,parent,p,kind,name,val):
        
        bg = self.commonBackground
        
        # Inits the entry widget.
        var = Tk.StringVar()
        var.set(val)
    
        f = Tk.Frame(parent)
        Tk.Entry(f,textvariable=var).pack(side='left')
        Tk.Label(f,text=name,background=bg).pack(side='left')
        
        def ratioCallback():
            val2 = var.get()
            # g.trace(name,val2)
            try:
                val2 = float(val2)
                if 0.0 <= val2 <= 1.0:
                    return val2
            except TypeError:
                pass
            g.trace("bad val:",val2)
            return val
                
        self.initValue(p,name,kind,val,ratioCallback)
        
        self.sc.create_window(10,self.h,anchor='w',window=f)
        self.h += 30
    #@nonl
    #@-node:ekr.20041225063637.43:createRatio
    #@+node:ekr.20041225063637.45:createShortcut
    def createShortcut (self,parent,p,kind,name,val):
        
        g.trace(name,val)
        
        if name:
            self.createString(parent,p,kind,name,val)
    #@nonl
    #@-node:ekr.20041225063637.45:createShortcut
    #@+node:ekr.20041225063637.46:createShortcuts
    def createShortcuts (self,parent,p,kind,name,vals):
        
        __pychecker__ = '--no-argsused' # vals not used.
        
        t = self.createText(parent,p)
        
        def shortcutsCallback():
            val = t.get('1.0','end').rstrip()
            return val
    
        self.initValue(p,name,kind,vals,shortcutsCallback)
    #@nonl
    #@-node:ekr.20041225063637.46:createShortcuts
    #@+node:ekr.20041225063637.47:createSpacerFrame
    def createSpacerFrame (self,parent,size=10):
        
        f = Tk.Frame(parent)
        self.sc.create_window(10,self.h,anchor='w',window=f)
        self.h += size
    #@nonl
    #@-node:ekr.20041225063637.47:createSpacerFrame
    #@+node:ekr.20041225063637.48:createString
    def createString (self,parent,p,kind,name,val):
        
        bg = self.commonBackground
    
        if val in (None,'None'): val = ""
        
        # Inits the Entry widget.
        var = Tk.StringVar()
        var.set(val)
        
        f = Tk.Frame(parent) # No need to pack.
        Tk.Entry(f,textvariable=var,width=40).pack(side='left')
        Tk.Label(f,text=name,background=bg).pack(side='left')
        
        def stringCallback():
            val = var.get()
            # g.trace(name,val)
            return val
    
        self.initValue(p,name,kind,val,stringCallback)
        
        self.sc.create_window(15,self.h,anchor='w',window=f)
        self.h += 30
    #@nonl
    #@-node:ekr.20041225063637.48:createString
    #@+node:ekr.20041225063637.49:createStrings
    def createStrings (self,parent,p,kind,name,val):
        
        bg = self.commonBackground
        
        # g.trace(repr(kind),repr(name),val)
        i = kind.find('[')
        j = kind.find(']')
        if not (-1 < i < j):
            return
        
        items = kind[i+1:j].split(',')
        items.sort()
        items.insert(0,'<none>')
        if val in items:
            initialitem = items.index(val)
        else:
            initialitem = 0
            
        f = Tk.Frame(parent,background=bg)
    
        stringsBox = Pmw.ComboBox(f,
            labelpos="ew",label_text=name,
            label_background = bg,
            scrolledlist_items=items)
    
        stringsBox.selectitem(initialitem)
        stringsBox.pack(side="left",padx=2)
        
        def stringsCallback():
            return stringsBox.get()
    
        self.initValue(p,name,kind,val,stringsCallback)
    
        self.sc.create_window(10,self.h,anchor='w',window=f)
        self.h += 30
    #@nonl
    #@-node:ekr.20041225063637.49:createStrings
    #@+node:ekr.20050512134219:createText
    def createText (self,parent,p):
        
        bg = self.commonBackground
        f = Tk.Frame(parent,background=bg) # No need to pack.
    
        scrolled_text = Pmw.ScrolledText(f,
            labelpos = 'ew',label_text='shortcuts',
            hull_background=bg,
            hull_bd=2,hull_relief='groove',
            hull_padx=6,hull_pady=6,
            text_background='white',
            text_padx=6,text_pady=6,
            text_bd=2,text_relief='sunken',
            label_background=bg,
            text_height=10,text_width=80)
        scrolled_text.pack(side='left',pady=6,padx=6,expand=1,fill='x')
        t = scrolled_text.component('text')
        t.insert('end',p.bodyString().strip())
        t.configure(state='normal')
        scrolled_text.component('hull')
    
        self.sc.create_window(10-2,self.h,anchor='w',window=f)
        self.h += 140
        
        return t
    #@nonl
    #@-node:ekr.20050512134219:createText
    #@-node:ekr.20041225063637.25:createWidgets & helpers
    #@+node:ekr.20041225063637.50:callbacks...
    #@+node:ekr.20041225063637.51:onAnyButton
    def onAnyButton(self,name):
        
        c = self.c
        endDialog = name in (None,"OK","Cancel")
        
        # g.trace(name)
        
        dispatchDict = {
            "Apply":    self.writeChangedVars,
            "Cancel":   None, # Do nothing.
            "OK":       self.writeChangedVars,
            "Revert":   self.revert,
        }
        
        f = dispatchDict.get(name)
        if f: f()
            
        if self.replaceBody:
            if endDialog:
                c.frame.replaceTreePaneWithComponent('tree')
                c.frame.replaceBodyPaneWithComponent('body')
                c.disableCommandsMessage = '' # Re-enable all commands.
        else:
            if endDialog:
                self.dialog.destroy()
                c.disableCommandsMessage = '' # Re-enable all commands.
            else:
                self.dialog.withdraw()
                self.dialog.deiconify()
    #@nonl
    #@-node:ekr.20041225063637.51:onAnyButton
    #@+node:ekr.20041225063637.52:revert
    def revert (self):
        
        """Restores written vars to initial value and re-inits all widgets."""
        
        iDict = self.initValueDict
        fDict = self.fileValueDict
        munge = g.app.config.munge
        
        changedList = []
        for key in fDict.keys():
    
            fData = fDict.get(key)
            fp,fname,fkind,fval,getValueCallback = fData
            
            iData = iDict.get(key)
            ip,iname,ikind,ival,getValueCallback = iData
    
            assert(ip==fp and iname==fname and ikind==fkind)
            # print "revert",key,"ival",ival,"fval",fval
            
            if ival != fval:
                # print "revert %10s -> %10s %s" % (str(fval),str(ival),fname)
                self.fileValueDict [munge(iname)] = ip,iname,ikind,ival,getValueCallback
                changedList.append((ip,iname,ikind,fval,ival),)
    
        self.updateSetter(self.p,updateDicts=False)
        self.writeChangedList(changedList,"revert")
        self.updateSetter(self.p) # Redraw the widgets in the pane.
    #@nonl
    #@-node:ekr.20041225063637.52:revert
    #@+node:ekr.20041225063637.53:onPaneResize
    def onPaneResize (self,sizes=None):
        
        __pychecker__ = '--no-argsused' # sizes not used, but needed.
    
        self.sc.resizescrollregion()
    #@nonl
    #@-node:ekr.20041225063637.53:onPaneResize
    #@+node:ekr.20041225063637.54:handleTreeClick
    def onTreeClick (self,p):
        
        self.p = p.copy()
        self.updateSetter(p)
    #@nonl
    #@-node:ekr.20041225063637.54:handleTreeClick
    #@-node:ekr.20041225063637.50:callbacks...
    #@+node:ekr.20041225063637.55:getters...
    #@+node:ekr.20041225063637.56:findCorrespondingNode
    def findCorrespondingNode (self,root1,root2,p1):
        
        """Return the node corresponding to p1 (in root1) in the root2's tree."""
        
        if p1 == root1: return root2
    
        # Go up tree 1, computing child indices.
        childIndices = []
        for p in p1.self_and_parents_iter():
            #g.trace(p)
            if p == root1: break
            childIndices.append(p.childIndex())
            
        childIndices.reverse()
        # g.trace(childIndices)
        
        # Go down tree 2, moving to the n'th child.
        p2 = root2.copy()
        for n in childIndices:
            # g.trace(p2)
            p2.moveToNthChild(n)
    
        # g.trace(p2)
        return p2
    #@nonl
    #@-node:ekr.20041225063637.56:findCorrespondingNode
    #@+node:ekr.20041225063637.57:findSettingsRoot
    def findSettingsRoot (self,p):
        
        first_p = p.copy()
        
        # Get the list of root positions.
        roots = self.filesInfoDict.keys()
    
        for p in p.self_and_parents_iter():
            for root in roots:
                if p == root:
                    # g.trace("root of %s is %s" % (first_p.headString(),p.headString()))
                    return root # Used as key.  Must NOT return a copy.
                    
        g.trace("Can't happen: %s has no root node" % (first_p.headString()))
        return None
    #@nonl
    #@-node:ekr.20041225063637.57:findSettingsRoot
    #@+node:ekr.20041225063637.58:settingsPosition
    def settingsPosition (self):
        
        return self._settingsPosition.copy()
    #@nonl
    #@-node:ekr.20041225063637.58:settingsPosition
    #@-node:ekr.20041225063637.55:getters...
    #@+node:ekr.20041225063637.59:redrawing...
    #@+node:ekr.20041225063637.60:updateSetter
    def updateSetter (self,p,updateDicts=True):
        
        """Create a setter pane for position p."""
    
        sc = self.sc ; interior = sc.interior()
        
        if updateDicts:
            self.fileValueDict = {}
            self.initValueDict = {}
            self.colorSettingDict = {}
        
        # Destroy the previous widgets
        for w in interior.winfo_children():
            w.destroy()
    
        # Visit the node, and possibly its subtree, looking for widgets to create.
        self.parser.widgets = []
        self.suppressComments = None # May be set in parser.
        self.parser.visitNode(p)
        if self.parser.widgets:
            self.createWidgets(self.parser.widgets,interior,p)
            
        self.sc.resizescrollregion()
        self.sc.yview('moveto',0)
        self.updateSetterLabel(p)
        g.app.gui.widgetWantsFocus(None,None)
    #@nonl
    #@-node:ekr.20041225063637.60:updateSetter
    #@+node:ekr.20041225063637.62:updateSetterLabel
    def updateSetterLabel (self,p):
        
        if self.setterLabel:
    
            h = p.headString().strip() or ''
    
            for name in ('@page','@font','@ignore','@'):
                if g.match(h,0,name):
                    h = h[len(name):].strip()
                    i = h.find('=')
                    if i > -1:
                        h = h[:i].strip()
                    break
    
            self.setterLabel.configure(text=h)
            return h
            
        else:
            return None
    #@nonl
    #@-node:ekr.20041225063637.62:updateSetterLabel
    #@-node:ekr.20041225063637.59:redrawing...
    #@+node:ekr.20041225063637.63:value handlers...
    #@+at 
    #@nonl
    # These keep track of the original and changed values of all items in the 
    # present setter pane.
    #@-at
    #@nonl
    #@+node:ekr.20041225063637.64:initValue
    def initValue (self,p,name,kind,val,getValueCallback):
        
        munge = g.app.config.munge
        
        # g.trace(name,kind,val)
        
        self.initValueDict [munge(name)] = (p,name,kind,val,getValueCallback)
    #@nonl
    #@-node:ekr.20041225063637.64:initValue
    #@+node:ekr.20041225063637.65:writeChangedVars & helpers
    def writeChangedVars (self):
        
        """Create per-file changes lists from diffs between what has been inited and written.
        
        Call writeChangedList to update each file from items in this list."""
    
        changedList = []
        fDict = self.fileValueDict
        iDict = self.initValueDict
        munge = g.app.config.munge
        
        for key in iDict.keys():
    
            iData = iDict.get(key)
            ip,iname,ikind,ival,getValueCallback = iData
            newVal = getValueCallback()
            fData = fDict.get(key)
            if fData:
                fp,fname,fkind,fval,junk = fData
                assert(ip==fp and iname==fname and ikind==fkind)
                changed = fval != newVal ; oldVal = fval
            else:
                changed = ival != newVal ; oldVal = ival
                fval = '<none>'
    
            if changed:
                # print "write","key","ival",ival,"fval",fval
                if type(oldVal) == type({}):
                    s = "write  %s" % (iname)
                elif ikind == 'shortcuts':
                    s = 'updating shortcuts in %s' % ip.headString()
                else:
                    # Convert unicode strings to strings safe for printing.
                    # The calls to str are needed because g.toEncodedString only changes unicode strings.
                    strOldVal = str(g.toEncodedString(oldVal,'ascii'))
                    strNewVal = str(g.toEncodedString(newVal,'ascii'))
                    strIname  = str(g.toEncodedString(iname,'ascii'))
                    s = "write  %10s -> %10s %s" % (strOldVal,strNewVal,strIname)
                g.es_print(s,color='blue')
                self.fileValueDict [munge(iname)] = ip,iname,ikind,newVal,getValueCallback
                changedList.append((ip,iname,ikind,oldVal,newVal),)
                
        self.writeChangedList(changedList,"write")
    #@nonl
    #@+node:ekr.20041225063637.66:updateConfig
    def updateConfig(self,c,changes):
        
        """Update the core config settings from the changes list."""
        
        munge = g.app.config.munge
    
        for data in changes:
            p,name,kind,oldval,val = data
            if munge(kind) == 'font':
                for key in ('family','size','slant','weight'):
                    data2 = val.get(key)
                    if data2:
                        name2,val2 = data2
                        kind2 = g.choose(key=='size','int','string')
                        g.app.config.set(c,name2,kind2,val2)
                # Update the visible fonts: c may not be the same as self.c.
                for c2 in (c,self.c):
                    c2.frame.body.setFontFromConfig()
                    c2.frame.body.colorizer.setFontFromConfig()
                    c2.frame.log.setFontFromConfig()
                    c2.frame.tree.setFontFromConfig()
                    c2.redraw()
            elif munge(kind) == "color":
                # g.trace("setting colors")
                g.app.config.set(c,name,kind,val)
                for c2 in (c,self.c):
                    c2.frame.tree.setColorFromConfig()
                    c2.frame.log.setColorFromConfig()
                    c2.frame.body.setColorFromConfig()
            else:
                # g.trace(name,kind,val)
                g.app.config.set(c,name,kind,val)
    #@nonl
    #@-node:ekr.20041225063637.66:updateConfig
    #@+node:ekr.20041225063637.67:updateOneNode & helper
    def updateOneNode (self,c,data):
        
        """Update the node in c corresponding to p = data[0]."""
        
        p,name,kind,oldVal,val = data
        munge = g.app.config.munge
        name = name.strip() ; kind = munge(kind.strip())
    
        # Root1 is the root of the dialog's outline.
        p1 = p
        root1 = self.findSettingsRoot(p1.copy())
        c1 = root1.c
        
        # Root2 is the root of the settings outline in the file.
        root2 = g.app.config.settingsRoot(c) # c is NOT self.c
        p2 = self.findCorrespondingNode(root1.copy(),root2.copy(),p1.copy())
        if p2:
            c2 = p2.c ; filename = c2.mFileName
        else:
            g.trace("can't happen: can't find node in root2:",root2.c.mFileName)
            g.trace('root1',root1)
            g.trace('root2',root2)
            g.trace('p1',p1)
            c2 = None ; filename = None
    
        # Update the outline in the dialog and the target file.
        for p,c,where in ((p1,c1,"dialog"),(p2,c2,filename)):
            if p:
                # g.trace("updating %s in %s" % (name,where))
                if kind == 'shortcuts':
                    # Just put the new the values in the body.
                    p.setBodyStringOrPane(val)
                elif kind == 'font':
                    body = self.computeBodyFromFontDict(val)
                    p.setBodyStringOrPane(body)
                else:
                    # Put everything in the headline.
                    p.initHeadString("@%s %s = %s" % (kind,name,val))
    #@nonl
    #@+node:ekr.20041225063637.68:computeBodyFromFontDict
    def computeBodyFromFontDict(self,d):
    
        lines = []
        comments = d.get('comments')
        if comments:
            comment_lines = g.splitLines(comments)
            comment_lines = ["# %s" % (line) for line in comment_lines]
            lines.extend(comment_lines)
            lines.extend('\n\n')
            
        for key in ('family','size','slant','weight'):
            data = d.get(key)
            if data:
                name,val = data
                if val in (None,'<none>'):
                    val = "None"
                line = "%s = %s\n" % (name,val)
                lines.extend(line)
    
        body = ''.join(lines)
        return body
    #@nonl
    #@-node:ekr.20041225063637.68:computeBodyFromFontDict
    #@-node:ekr.20041225063637.67:updateOneNode & helper
    #@+node:ekr.20041225063637.69:writeChangedList
    def writeChangedList (self,changedList,tag):
        
        __pychecker__ = '--no-argsused' # tag used for debugging.
        
        filesInfoDict = self.filesInfoDict
        if 0:
            #@        << dump all the dicts in filesInfoDict >>
            #@+node:ekr.20041225063637.70:<< dump all the dicts in filesInfoDict >>
            for key in filesInfoDict.keys():
                print ; print
                print "key",key
                g.printDict(filesInfoDict.get(key))
            print ; print
            #@nonl
            #@-node:ekr.20041225063637.70:<< dump all the dicts in filesInfoDict >>
            #@nl
    
        # Accumulate the changes for each file in a 'changes' list for each root.
        for data in changedList:
            p,name,kind,oldVal,newVal = data
            # print "%6s %6s %10s -> %10s %s" % (tag,kind,str(oldVal),str(newVal),name)
            root = self.findSettingsRoot(p)
            d = filesInfoDict.get(root)
            changes = d.get('changes')
            changes.append(data)
            d['changes'] = changes
    
        for root in filesInfoDict.keys():
            d = filesInfoDict.get(root)
            # Keys are 'c','changes','path','islocal' (unused)
            c = d.get('c')
            changes = d.get('changes')
            path = d.get('path')
            # Always write the file so as to preserve expansion state.
            self.writeChangesToFile(c,changes,path)
            self.updateConfig(c,changes)
            d['changes'] = []
    #@nonl
    #@-node:ekr.20041225063637.69:writeChangedList
    #@+node:ekr.20041225063637.71:writeChangesToFile
    def writeChangesToFile (self,c,changes,path):
    
        # Write the individual changes.
        for data in changes:
            self.updateOneNode(c,data)
            
        # Copy the expansion state of the dialog to the file.
        for d in self.filesInfoDict.values():
            c2 = d.get('c')
            if c2 and c2 == c:
                p2 = d.get('p')
                p = g.app.config.settingsRoot(c)
                # g.trace(c,p)
                if p and p2:
                    p = p.copy() ; p2 = p2.copy()
                    # Defensive programming: don't assume p and p2 are in synch.
                    while p and p2:
                        if p2.isExpanded(): p.expand()
                        else: p.contract()
                        p.moveToThreadNext()
                        p2.moveToThreadNext()
                break
    
        if c.fileName():
            self.es("writing " + g.shortFilename(path))
            # Save the file corresponding to c.
            # Non-local files aren't open otherwise!
            c.fileCommands.save(c.fileName())
            c.redraw() # This should work for non-local files too.
            self.tree.redraw()
        else:
            print "no settings saved.  local file not named."
    #@nonl
    #@-node:ekr.20041225063637.71:writeChangesToFile
    #@-node:ekr.20041225063637.65:writeChangedVars & helpers
    #@-node:ekr.20041225063637.63:value handlers...
    #@+node:ekr.20041225063637.72:utilities...
    #@+node:ekr.20041225063637.11:class logClass
    class logClass:
        
        def __init__ (self,textWidget):
            self.textWidget = textWidget
            self.colorTags = []
            
        def put(self,s,color=None):
            w = self.textWidget
            #@        << put s to w >>
            #@+node:ekr.20041225063637.12:<< put s to w >>
            if type(s) == type(u""):
                s = g.toEncodedString(s,g.app.tkEncoding)
            
            if color:
                if color not in self.colorTags:
                    self.colorTags.append(color)
                    w.tag_config(color,foreground=color)
                w.insert("end",s)
                w.tag_add(color,"end-%dc" % (len(s)+1),"end-1c")
                if "black" not in self.colorTags:
                    self.colorTags.append("black")
                    w.tag_config("black",foreground="black")
                w.tag_add("black","end")
            else:
                w.insert("end",s)
            
            w.see("end")
            w.update_idletasks()
            #@nonl
            #@-node:ekr.20041225063637.12:<< put s to w >>
            #@nl
            
        def putnl (self):
            w = self.textWidget
            if sys.platform == "darwin": print
            w.insert("end",'\n')
            w.see("end")
            w.update_idletasks()
    #@nonl
    #@-node:ekr.20041225063637.11:class logClass
    #@+node:ekr.20041225063637.20:center
    def center(self):
        
        top = self.top
    
        """Center the dialog on the screen.
    
        WARNING: Call this routine _after_ creating a dialog.
        (This routine inhibits the grid and pack geometry managers.)"""
    
        sw = top.winfo_screenwidth()
        sh = top.winfo_screenheight()
        w,h,x,y = self.get_window_info()
        
        # Set the new window coordinates, leaving w and h unchanged.
        x = (sw - w)/2
        y = (sh - h)/2
        top.geometry("%dx%d%+d%+d" % (w,h,x,y))
        
        return w,h,x,y
    #@nonl
    #@-node:ekr.20041225063637.20:center
    #@+node:ekr.20041225063637.73:settingsController.es
    def es(self,*args,**keys):
        
        old_log = g.app.log
        g.app.log = self.log
        g.es(*args,**keys)
        g.app.log = old_log
    #@nonl
    #@-node:ekr.20041225063637.73:settingsController.es
    #@+node:ekr.20041225063637.74:copyExpansionState
    def copyExpansionState(self,p1,p2):
     
        # Don't depend on p.nodeAfterTree, etc.
        if p1.isExpanded():
            # g.trace("p1",p1)
            # g.trace("p2",p2)
            p2.expand()
            child1 = p1.firstChild()
            child2 = p2.firstChild()
            while child1:
                self.copyExpansionState(child1,child2)
                child1 = child1.next()
                child2 = child2.next()
    #@nonl
    #@-node:ekr.20041225063637.74:copyExpansionState
    #@+node:ekr.20041225063637.75:get_window_info
    # WARNING: Call this routine _after_ creating a dialog.
    # (This routine inhibits the grid and pack geometry managers.)
    
    def get_window_info (self):
        
        top = self.top
        
        top.update_idletasks() # Required to get proper info.
    
        # Get the information about top and the screen.
        geom = top.geometry() # geom = "WidthxHeight+XOffset+YOffset"
        dim,x,y = geom.split('+')
        w,h = dim.split('x')
        w,h,x,y = int(w),int(h),int(x),int(y)
        
        return w,h,x,y
    #@nonl
    #@-node:ekr.20041225063637.75:get_window_info
    #@+node:ekr.20041225063637.76:printChangedVars
    def printChangedVars (self):
    
        d = self.initValueDict
        
        for key in d.keys():
            
            data = d.get(key)
            p,name,kind,val,getValueCallback = data
            newVal = getValueCallback()
            
            if val != newVal:
                print "%10s -> %10s %s" % (str(val),str(newVal),name)
    #@nonl
    #@-node:ekr.20041225063637.76:printChangedVars
    #@+node:ekr.20041225063637.77:printWidgets
    def printWidgets (self,widgets):
    
        print '-'*20
    
        for data in widgets:
            p,kind,name,vals = data
            if type(vals) == type([]):
                print "%s %s..." % (name,kind)
                for val in vals:
                    print val
            else:
                print "%45s %8s %s" % (name,kind,vals)
    #@nonl
    #@-node:ekr.20041225063637.77:printWidgets
    #@-node:ekr.20041225063637.72:utilities...
    #@-others
#@nonl
#@-node:ekr.20041225063637.10:class settingsController
#@-others
#@nonl
#@-node:ekr.20041117062700:@thin leoConfig.py
#@-leo
