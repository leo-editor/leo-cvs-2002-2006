#@+leo-ver=4-thin
#@+node:ekr.20041117062700:@thin leoConfig.py
#@@language python
#@@tabwidth -4

import leoGlobals as g
import leoGui

import exceptions
import os
import string
import sys

#@+others
#@+node:ekr.20041119203941:class config
class baseConfig:
    """The base class for Leo's configuration handler."""
    #@    << define defaultsDict >>
    #@+node:ekr.20041117062717.1:<< define defaultsDict >>
    #@+at 
    #@nonl
    # This contains only the "interesting" defaults.
    # Ints and bools default to 0, floats to 0.0 and strings to "".
    #@-at
    #@@c
    
    defaultBodyFontSize = g.choose(sys.platform=="win32",9,12)
    defaultLogFontSize  = g.choose(sys.platform=="win32",8,12)
    defaultTreeFontSize = g.choose(sys.platform=="win32",9,12)
    
    defaultsDict = {
        # compare options...
        "ignore_blank_lines" : ("bool",True),
        "limit_count" : ("int",9),
        "print_mismatching_lines" : ("bool",True),
        "print_trailing_lines" : ("bool",True),
        # find/change options...
        "search_body" : ("bool",True),
        "whole_word" : ("bool",True),
        # Prefs panel.
        "default_target_language" : ("language","Python"),
        "tab_width" : ("int",-4),
        "page_width" : ("int",132),
        "output_doc_chunks" : ("bool",True),
        "tangle_outputs_header" : ("bool",True),
        # Syntax coloring options...
        # Defaults for colors are handled by leoColor.py.
        "color_directives_in_plain_text" : ("bool",True),
        "underline_undefined_section_names" : ("bool",True),
        # Window options...
        "allow_clone_drags" : ("bool",True),
        "body_pane_wraps" : ("bool",True),
        "body_text_font_family" : ("family","Courier"),
        "body_text_font_size" : ("int",defaultBodyFontSize),
        "body_text_font_slant" : ("slant","roman"),
        "body_text_font_weight" : ("weight","normal"),
        "enable_drag_messages" : ("bool",True),
        "headline_text_font_size" : ("int",defaultLogFontSize),
        "headline_text_font_slant" : ("slant","roman"),
        "headline_text_font_weight" : ("weight","normal"),
        "log_text_font_size" : ("int",defaultLogFontSize),
        "log_text_font_slant" : ("slant","roman"),
        "log_text_font_weight" : ("weight","normal"),
        "initial_window_height" : ("int",600),
        "initial_window_width" :  ("int",800),
        "initial_window_left" : ("int",10),
        "initial_window_top" : ("int",10),
        "initial_splitter_orientation" : ("orientation","vertical"),
        "initial_vertical_ratio" : ("ratio",0.5),
        "initial_horizontal_ratio" : ("ratio",0.3),
        "initial_horizontal_secondary_ratio" : ("ratio",0.5),
        "initial_vertical_secondary_ratio" : ("ratio",0.7),
        "outline_pane_scrolls_horizontally" : ("bool",False),
        "split_bar_color" : ("color","LightSteelBlue2"),
        "split_bar_relief" : ("relief","groove"),
        "split_bar_width" : ("int",7),
    }
    #@nonl
    #@-node:ekr.20041117062717.1:<< define defaultsDict >>
    #@nl
    #@    << define encodingIvarsDict >>
    #@+node:ekr.20041118062709:<< define encodingIvarsDict >>
    encodingIvarsDict = {
        "default_derived_file_encoding" : ("unicode-encoding","utf-8"),
        "new_leo_file_encoding" : ("unicode-encoding","UTF-8"),
            # Upper case for compatibility with previous versions.
        "tkEncoding" : ("unicode-encoding",None),
            # Defaults to None so it doesn't override better defaults.
    }
    #@-node:ekr.20041118062709:<< define encodingIvarsDict >>
    #@nl
    #@    << define ivarsDict >>
    #@+node:ekr.20041117072055:<< define ivarsDict >>
    # Each of these settings sets the ivar with the same name.
    ivarsDict = {
        "at_root_bodies_start_in_doc_mode" : ("bool",True),
            # For compatibility with previous versions.
        "create_nonexistent_directories" : ("bool",False),
        "output_initial_comment" : ("string",""),
            # "" for compatibility with previous versions.
        "output_newline" : ("newline-type","nl"),
        "read_only" : ("bool",True),
            # Make sure we don't alter an illegal leoConfig.txt file!
        "redirect_execute_script_output_to_log_pane" : ("bool",False),
        "relative_path_base_directory" : ("directory","!"),
        "remove_sentinels_extension" : ("string",".txt"),
        "save_clears_undo_buffer" : ("bool",False),
        "stylesheet" : ("string",None),
        "trailing_body_newlines" : ("newline-type","asis"),
        "use_plugins" : ("bool",False),
            # Should never be True here!
        "use_psyco" : ("bool",False),
        "undo_granularity" : ("undo_granularity","word"),
            # "char","word","line","node"
        "write_strips_blank_lines" : ("bool",False),
    }
    #@nonl
    #@-node:ekr.20041117072055:<< define ivarsDict >>
    #@nl
    keysDict = {}
    rawKeysDict = {}
    dictList = [ivarsDict,encodingIvarsDict,defaultsDict]
    localOptionsDict = {} # Keys are commanders.  Values are optionsDicts.
    #@    @+others
    #@+node:ekr.20041117083202:Birth...
    #@+node:ekr.20041117062717.2:ctor & init
    def __init__ (self):
    
        self.init()
    
    def init (self):
    
        self.configsExist = False # True when we successfully open a setting file.
        self.defaultFont = None # Set in gui.getDefaultConfigFont.
        self.defaultFontFamily = None # Set in gui.getDefaultConfigFont.
        self.dictList = [self.defaultsDict] # List of dictionaries.
        self.inited = False
        self.recentFiles = [] # List of recent files.
    
        self.initIvarsFromSettings()
        self.initSettingsFiles()
        self.initRecentFiles()
        self.initRawKeysDict()
    #@nonl
    #@-node:ekr.20041117062717.2:ctor & init
    #@+node:ekr.20041117065611.1:initEncoding
    def initEncoding (self,encodingName):
        
        data = self.ivarsDict.get(encodingName)
        if data:
            theType,encoding = data
        else:
            encoding = "utf-8" ##  This probably should be none until late in the init process.
            theType = None
    
        # g.trace(encodingName,encoding)
    
        setattr(self,encodingName,encoding)
    
        if encoding and not g.isValidEncoding(encoding):
            g.es("bad %s: %s" % (encodingName,encoding))
    #@nonl
    #@-node:ekr.20041117065611.1:initEncoding
    #@+node:ekr.20041117065611:initIvar
    def initIvar(self,ivarName):
        
        data = self.ivarsDict.get(ivarName)
        
        if data:
            theType,val = data
        else:
            theType,val = None,None
    
        # g.trace(ivarName,val)
    
        setattr(self,ivarName,val)
    #@nonl
    #@-node:ekr.20041117065611:initIvar
    #@+node:ekr.20041117065611.2:initIvarsFromSettings
    def initIvarsFromSettings (self):
        
        for ivar in self.encodingIvarsDict.keys():
            self.initEncoding(ivar)
            
        for ivar in self.ivarsDict.keys():
            self.initIvar(ivar)
            
        self.use_plugins = True ### Testing only.
    #@nonl
    #@-node:ekr.20041117065611.2:initIvarsFromSettings
    #@+node:ekr.20041117062717.24:initRawKeysDict
    def initRawKeysDict (self):
    
        for key in self.keysDict.keys():
            newKey = key.replace('&','')
            self.rawKeysDict[newKey] = key,self.keysDict[key]
    
        if 0: #trace
            keys = self.rawKeysDict.keys()
            keys.sort()
            for key in keys:
                print self.rawKeysDict[key]
    #@nonl
    #@-node:ekr.20041117062717.24:initRawKeysDict
    #@+node:ekr.20041117083202.2:initRecentFiles (revise)
    if 0:
        # Something like this must be done.
        def initRecentFiles (self):
            try:
                for i in xrange(10):
                    f = self.get(section,"file" + str(i),raw=1)
                    f = g.toUnicode(f,"utf-8")
                    self.recentFiles.append(f)
            except: pass
        
    def initRecentFiles (self):
    
        self.recentFiles = []
    #@nonl
    #@-node:ekr.20041117083202.2:initRecentFiles (revise)
    #@+node:ekr.20041117083857:initSettingsFiles
    def initSettingsFiles (self):
        
        """Set self.globalConfigFile, self.homeFile"""
    
        dirs = [] # Directories that have already been searched.
        
        for ivar,dir in (
            ("globalConfigFile",g.app.globalConfigDir),
            ("homeFile",g.app.homeDir),
        ):
    
            if dir not in dirs:
                dirs.append(dir)
                path = g.os_path_join(dir,"leoSettings.leo")
                if g.os_path_exists(path):
                    setattr(self,ivar,path)
                else:
                    setattr(self,ivar,None)
                 
        if 0:   
            g.trace("globalConfigFile",self.globalConfigFile)
            g.trace("homeFile",self.homeFile)
    #@nonl
    #@-node:ekr.20041117083857:initSettingsFiles
    #@-node:ekr.20041117083202:Birth...
    #@+node:ekr.20041117081009:Getters...
    #@+node:ekr.20041117083141:get & allies
    def get (self,c,setting,theType):
        
        """Get the setting and make sure its type matches the expected type."""
        
        found = False
        if c:
            d = self.localOptionsDict.get(c)
            if d:
                val,found = self.getValFromDict(d,setting,theType,found)
                if val is not None: return val
    
        for d in self.dictList:
            val,found = self.getValFromDict(d,setting,theType,found)
            if val is not None: return val
                    
        if 0: # Good for debugging leoSettings.leo.
            # Don't warn if None was specified.
            if not found and self.inited:
                g.trace("Not found:",setting)
    
        return None
    #@nonl
    #@+node:ekr.20041121143823:getValFromDict
    def getValFromDict (self,d,setting,theType,found):
    
        data = d.get(setting)
        if data:
            found = True
            dType,val = data
            
            if 0: # not ready yet.
                if dType != type:
                    g.trace("Expected type %s, got %s for setting %s" % (theType,dType,setting))
    
            if val not in (u'None',u'none','None','none','',None):
                # g.trace(theType,repr(val))
                return val,found
    
        return None,found
    #@nonl
    #@-node:ekr.20041121143823:getValFromDict
    #@-node:ekr.20041117083141:get & allies
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
    #@+node:ekr.20041117093009.2:getLanguage FINISH
    def getLanguage (self,c,setting):
        
        """Return the setting whose value should be a language known to Leo."""
        
        language = self.getString(c,setting)
        
        return language ###
    
        if language in xxx:
            return language
        else:
            return None
    #@nonl
    #@-node:ekr.20041117093009.2:getLanguage FINISH
    #@+node:ekr.20041117062717.11:getRecentFiles
    def getRecentFiles (self,c):
        
        # Must get c's recent files.
        return self.recentFiles
    #@nonl
    #@-node:ekr.20041117062717.11:getRecentFiles
    #@+node:ekr.20041117081009.4:getString
    def getString (self,c,setting):
        
        """Search all dictionaries for the setting & check it's type"""
    
        return self.get(c,setting,"string")
    #@nonl
    #@-node:ekr.20041117081009.4:getString
    #@+node:ekr.20041118055543:getFontDict  FINISH (needed for @settings tree, maybe)
    def getFontDict (self,c,setting):
        
        """Search all dictionaries for the setting & check it's type"""
        
        # To do:
        # - get params from somewhere.
        # - call getFontFromParams.
        # - make a dict and return it.
        
        return self.get(c,setting,"string")
    #@nonl
    #@-node:ekr.20041118055543:getFontDict  FINISH (needed for @settings tree, maybe)
    #@+node:ekr.20041117062717.13:getFontFromParams
    def getFontFromParams(self,c,family,size,slant,weight,defaultSize=12,tag=""):
    
        """Compute a font from font parameters.
    
        Arguments are the names of settings to be use.
        We default to size=12, slant="roman", weight="normal".
    
        We return None if there is no family setting so we can use system default fonts."""
    
        family = self.getString(c,family)
        if family in (None,""):
            family = self.defaultFontFamily
            
        size = self.getInt(c,size)
        if size in (None,0): size = defaultSize
        
        slant = self.getString(c,slant)
        if slant in (None,""): slant = "roman"
    
        weight = self.getString(c,weight)
        if weight in (None,""): weight = "normal"
        
        # if g.app.trace: g.trace(tag,family,size,slant,weight)
        
        return g.app.gui.getFontFromParams(family,size,slant,weight)
    #@nonl
    #@-node:ekr.20041117062717.13:getFontFromParams
    #@+node:ekr.20041117062717.14:getShortcut
    def getShortcut (self,c,name):
        
        # Allow '&' in keys.
        val = self.rawKeysDict.get(name.replace('&',''))
    
        if val:
            rawKey,shortcut = val
            return rawKey,shortcut
        else:
            return None,None
    #@nonl
    #@-node:ekr.20041117062717.14:getShortcut
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
            else:
                setattr(c,setting,val)
    #@nonl
    #@-node:ekr.20041117062717.17:setCommandsIvars
    #@-node:ekr.20041117081009:Getters...
    #@+node:ekr.20041118084146:Setters
    #@+node:ekr.20041118084146.1:set
    def set (self,c,setting,type,val):
        
        """Set the setting and make sure its type matches the given type."""
        
        # g.trace(c,setting,type,val)
    
        return ####
        
        ## To do: also search c's settings dict.
        data = self.defaultsDict.get(setting)
        
        if data:
            theType,val = data
        else:
            theType,val = None,None
    
        if setting is None:
            g.trace(setting,type,val)
        
        return val
    #@-node:ekr.20041118084146.1:set
    #@+node:ekr.20041118084241:setString
    def setString (self,c,setting,val):
        
        self.set(c,setting,"string",val)
    #@nonl
    #@-node:ekr.20041118084241:setString
    #@+node:ekr.20041118123207:setRecentFiles
    def setRecentFiles (self,c,files):
    
        self.recentFiles = files
    #@nonl
    #@-node:ekr.20041118123207:setRecentFiles
    #@-node:ekr.20041118084146:Setters
    #@+node:ekr.20041117093246:Scanning @settings
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
        c,frame = g.app.gui.newLeoCommanderAndFrame(path)
        frame.log.enable(False)
        g.app.setLog(frame.log,"openWithFileName")
        g.app.lockLog()
        frame.c.fileCommands.open(theFile,path) # closes theFile.
        g.app.unlockLog()
        frame.openDirectory = g.os_path_dirname(path)
        g.app.gui = oldGui
        return c
    #@nonl
    #@-node:ekr.20041117085625:openSettingsFile
    #@+node:ekr.20041120064303:readSettingsFiles
    def readSettingsFiles (self):
        
        # Init settings from leoSettings.leo files.
        for path in (self.globalConfigFile, self.homeFile):
            if path:
                g.es("reading settings in %s" % path,color="blue")
                c = self.openSettingsFile(path)
                if c:
                    d = self.readSettings(c)
                    if d:
                        if 0:
                            #@                        << print d >>
                            #@+node:ekr.20041120113116:<< print d >>
                            keys = d.keys()
                            keys.sort()
                            g.trace('-' * 40)
                            for key in keys:
                                data = d.get(key)
                                kind,val = data
                                print "%10s %-20s %s" % (kind,val,key)
                            #@nonl
                            #@-node:ekr.20041120113116:<< print d >>
                            #@nl
                        self.dictList.insert(0,d)
                    else:
                        g.es("No @settings tree in %s",color="red")
                    g.app.destroyWindow(c.frame)
                    
        self.inited = True
    #@nonl
    #@-node:ekr.20041120064303:readSettingsFiles
    #@+node:ekr.20041117083857.1:readSettings
    # Called to read all leoSettings.leo file.
    # Also called when opening an .leo file to read @settings tree.
    
    def readSettings (self,c):
        
        """Read settings from a file that may contain an @settings tree."""
        
        parser = settingsTreeParser(c)
        return parser.traverse()
    #@nonl
    #@-node:ekr.20041117083857.1:readSettings
    #@-node:ekr.20041117093246:Scanning @settings
    #@-others
    
class config (baseConfig):
    """A class to manage configuration settings."""
    pass
#@nonl
#@-node:ekr.20041119203941:class config
#@+node:ekr.20041119205325:parser classes
#@<< class parserBaseClass >>
#@+node:ekr.20041119203941.2:<< class parserBaseClass >>
class parserBaseClass:
    
    """The base class for settings parsers."""
    
    #@    << parserBaseClass data >>
    #@+node:ekr.20041121130043:<< parserBaseClass data >>
    basic_types = [
        'bool','color','directory','font','int',
        'float','path','ratio','shortcut','string']
    
    control_types = ['if','if-gui','if-platform','ignore','page','shortcuts']
    
    # Keys are settings names, values are (type,value) tuples.
    settingsDict = {}
    
    type_dict = {}
    #@nonl
    #@-node:ekr.20041121130043:<< parserBaseClass data >>
    #@nl
    
    #@    @+others
    #@+node:ekr.20041119204700:ctor
    def __init__ (self,c):
        
        self.c = c
        
        self.dispatchDict = {
            'bool':         self.doBool,
            'color':        self.doColor,
            'directory':    self.doDirectory,
            'font':         self.doFont,
            'if':           self.doIf,
            'if-gui':       self.doIfGui,
            'if-platform':  self.doIfPlatform,
            'ignore':       self.doIgnore,
            'int':          self.doInt,
            'float':        self.doFloat,
            'path':         self.doPath,
            'page':         self.doPage,
            'ratio':        self.doRatio,
            'shortcuts':    self.doShortcuts,
            'string':       self.doString,
        }
    #@nonl
    #@-node:ekr.20041119204700:ctor
    #@+node:ekr.20041120103012:error
    def error (self,s):
    
        print s
    
        # Does not work at present because we are using a null Gui.
        g.es(s,color="blue")
    #@nonl
    #@-node:ekr.20041120103012:error
    #@+node:ekr.20041120094940:kind handlers
    #@+node:ekr.20041120094940.1:doBool
    def doBool (self,p,kind,name,val):
    
        if val in ('True','true','1'):
            self.set(kind,name,True)
        elif val in ('False','false','0'):
            self.set(kind,name,False)
        else:
            self.valueError(p,kind,name,val)
    #@nonl
    #@-node:ekr.20041120094940.1:doBool
    #@+node:ekr.20041120094940.2:doColor
    def doColor (self,p,kind,name,val):
        
        # At present no checking is done.
        self.set(kind,name,val)
    #@nonl
    #@-node:ekr.20041120094940.2:doColor
    #@+node:ekr.20041120103933:doIf
    def doIf(self,p,kind,name,val):
    
        g.trace("'if' not supported yet")
        return None
    #@nonl
    #@-node:ekr.20041120103933:doIf
    #@+node:ekr.20041121125416:doIfGui
    def doIfGui (self,p,kind,name,val):
    
        if g.app.gui == name:
            return None
        else:
            return "skip"
    #@nonl
    #@-node:ekr.20041121125416:doIfGui
    #@+node:ekr.20041120104215:doIfPlatform
    def doIfPlatform (self,p,kind,name,val):
    
        if sys.platform == name:
            return None
        else:
            return "skip"
    #@nonl
    #@-node:ekr.20041120104215:doIfPlatform
    #@+node:ekr.20041120094940.3:doDirectory & doPath
    def doDirectory (self,p,kind,name,val):
        
        # At present no checking is done.
        self.set(kind,name,val)
        
    doPath = doDirectory
    #@nonl
    #@-node:ekr.20041120094940.3:doDirectory & doPath
    #@+node:ekr.20041120094940.4:doFont
    def doFont (self,p,kind,name,val):
        
        # At present no checking is done.
        self.set(kind,name,val)
    #@nonl
    #@-node:ekr.20041120094940.4:doFont
    #@+node:ekr.20041120104215.1:doIgnore
    def doIgnore(self,p,kind,name,val):
    
        return "skip"
    #@nonl
    #@-node:ekr.20041120104215.1:doIgnore
    #@+node:ekr.20041120094940.5:doInt
    def doInt (self,p,kind,name,val):
        
        try:
            val = int(val)
            self.set(kind,name,val)
        except ValueError:
            self.valueError(p,kind,name,val)
    #@nonl
    #@-node:ekr.20041120094940.5:doInt
    #@+node:ekr.20041120094940.6:doFloat
    def doFloat (self,p,kind,name,val):
        
        try:
            val = float(val)
            self.set(kind,name,val)
        except ValueError:
            self.valueError(p,kind,name,val)
    #@nonl
    #@-node:ekr.20041120094940.6:doFloat
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
                self.set(kind,name,val)
            else:
                self.valueError(p,kind,name,val)
        except ValueError:
            self.valueError(p,kind,name,val)
    #@nonl
    #@-node:ekr.20041121125741:doRatio
    #@+node:ekr.20041120113848:doShortcut
    def doShortcut(self,p,kind,name,val):
        
        # At present no checking is done.
        self.set(kind,name,val)
    #@nonl
    #@-node:ekr.20041120113848:doShortcut
    #@+node:ekr.20041120105609:doShortcuts
    def doShortcuts(self,p,kind,name,val):
        
        #g.trace('*'*10,p.headString())
    
        s = p.bodyString()
        lines = g.splitLines(s)
        for line in lines:
            line = line.strip()
            if line and not g.match(line,0,'#'):
                name,val = self.parseShortcutLine(line)
                # g.trace(name,val)
                if val is not None:
                    self.set("shortcut",name,val)
    #@nonl
    #@-node:ekr.20041120105609:doShortcuts
    #@+node:ekr.20041120094940.8:doString
    def doString (self,p,kind,name,val):
        
        # At present no checking is done.
        self.set(kind,name,val)
    #@nonl
    #@-node:ekr.20041120094940.8:doString
    #@-node:ekr.20041120094940:kind handlers
    #@+node:ekr.20041119204700.2:oops
    def oops (self):
        print ("parserBaseClass oops:",
            g.callerName(2),
            "must be overridden in subclass")
    #@-node:ekr.20041119204700.2:oops
    #@+node:ekr.20041119205148:parseHeadline
    def parseHeadline (self,s):
        
        """Return the kind of @settings node indicated by p's headline."""
        
        kind = name = val = None
    
        if g.match(s,0,'@'):
            i = g.skip_id(s,1,chars='-')
            kind = s[1:i]
            
            if kind:
                i = g.skip_ws(s,i)
                j = g.skip_id(s,i)
                name = s[i:j]
                if name:
                    i = g.skip_ws(s,j)
                    if g.match(s,i,'='):
                        i = g.skip_ws(s,i+1)
                        val = s[i:]
    
        # g.trace("%50s %10s %s" %(name,kind,val))
        return kind,name,val
    #@nonl
    #@-node:ekr.20041119205148:parseHeadline
    #@+node:ekr.20041120112043:parseShortcutLine
    def parseShortcutLine (self,s):
        
        """Return the kind of @settings node indicated by p's headline."""
        
        kind = name = val = None
    
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
    #@+node:ekr.20041120074536:settingsRoot
    def settingsRoot (self):
        
        c = self.c
        
        for p in c.allNodes_iter():
            if p.headString().rstrip() == "@settings":
                return p.copy()
        else:
            return c.nullPosition()
    #@nonl
    #@-node:ekr.20041120074536:settingsRoot
    #@+node:ekr.20041120094940.9:settingsParser.set
    def set (self,kind,name,val):
        
        """Init the setting for name to val."""
        
        # g.trace("%10s %15s %s" %(kind,val,name))
        
        d = self.settingsDict
    
        if d.get(name):
            g.es("overriding setting: %s" % (name))
        
        d[name] = kind,val
    #@nonl
    #@-node:ekr.20041120094940.9:settingsParser.set
    #@+node:ekr.20041119204700.1:traverse
    def traverse (self):
        
        c = self.c
        
        p = self.settingsRoot()
        if not p:
            return None
    
        while p:
            result = self.visitNode(p)
            if result == "skip":
                p.moveToNodeAfterTree()
            else:
                p.moveToThreadNext()
                
        return self.settingsDict
    #@nonl
    #@-node:ekr.20041119204700.1:traverse
    #@+node:ekr.20041120094940.10:valueError
    def valueError (self,p,kind,name,val):
        
        """Give an error: val is not valid for kind."""
        
        self.error("%s is not a valid %s for %s" % (val,kind,name))
    #@nonl
    #@-node:ekr.20041120094940.10:valueError
    #@+node:ekr.20041119204700.3:visitNode (must be overwritten in subclasses)
    def visitNode (self,p):
        
        self.oops()
    #@nonl
    #@-node:ekr.20041119204700.3:visitNode (must be overwritten in subclasses)
    #@-others
#@nonl
#@-node:ekr.20041119203941.2:<< class parserBaseClass >>
#@nl

#@+others
#@+node:ekr.20041119203941.3:class settingsTreeParser (parserBaseClass)
class settingsTreeParser (parserBaseClass):
    
    """A class that inits settings found in an @settings tree."""
    
    #@    @+others
    #@+node:ekr.20041119204103:ctor
    def __init__ (self,c):
    
        # Init the base class.
        parserBaseClass.__init__(self,c)
    #@nonl
    #@-node:ekr.20041119204103:ctor
    #@+node:ekr.20041119204714:visitNode
    def visitNode (self,p):
        
        """Init any settings found in node p."""
        
        # g.trace(p.headString())
    
        kind,name,val = self.parseHeadline(p.headString())
    
        if kind == "settings":
            pass
        if kind not in self.control_types and val in (u'None',u'none','None','none','',None):
            # None is valid for all data types.
            self.set(kind,name,None)
        elif kind in self.control_types or kind in self.basic_types:
            f = self.dispatchDict.get(kind)
            try:
                f(p,kind,name,val)
            except TypeError:
                print "*** no handler",kind
        elif name:
            # self.error("unknown type %s for setting %s" % (kind,name))
            # Just assume the type is a string.
            self.set(kind,name,val)
    #@nonl
    #@-node:ekr.20041119204714:visitNode
    #@-others
#@nonl
#@-node:ekr.20041119203941.3:class settingsTreeParser (parserBaseClass)
#@+node:ekr.20041119203941.4:class dialogCreator (parserBaseClass)
class dialogCreator (parserBaseClass):
    
    """A class that creates a dialog for view and changing settings.
    
    This class creates this dialog using an @settings tree."""
    
    #@    @+others
    #@+node:ekr.20041119204700.4:ctor
    def __init__ (self,c):
        
        # Init the base class.
        parserBaseClass.__init__(self,c)
    #@nonl
    #@-node:ekr.20041119204700.4:ctor
    #@+node:ekr.20041119205753:createDialog
    def createDialog (self):
        
        # Traverse the @settings tree, creating data used to create the dialogs.
        self.traverse()
        
        # Create the dialog from the data.
        self.createDialogFromData()
    #@nonl
    #@-node:ekr.20041119205753:createDialog
    #@+node:ekr.20041119205753.1:createDialogFromData
    def createDialogFromData (self):
        
        pass
    #@nonl
    #@-node:ekr.20041119205753.1:createDialogFromData
    #@+node:ekr.20041119205148.2:visitNode
    def visitNode (self,p):
        
        """Save data in node p if p will contribute any item to the dialog."""
        
        g.trace(p)
    #@nonl
    #@-node:ekr.20041119205148.2:visitNode
    #@-others
#@nonl
#@-node:ekr.20041119203941.4:class dialogCreator (parserBaseClass)
#@-others
#@nonl
#@-node:ekr.20041119205325:parser classes
#@-others
#@-node:ekr.20041117062700:@thin leoConfig.py
#@-leo
