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
    #@    << baseConfig data >>
    #@+node:ekr.20041122094813:<<  baseConfig data >>
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
        ("default_target_language","language","Python"),
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
        ("initial_splitter_orientation","orientation","vertical"),
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
        ("default_derived_file_encoding","unicode-encoding","utf-8"),
        ("new_leo_file_encoding","unicode-encoding","UTF-8"),
            # Upper case for compatibility with previous versions.
        ("tkEncoding","unicode-encoding",None),
            # Defaults to None so it doesn't override better defaults.
    )
    #@nonl
    #@-node:ekr.20041118062709:define encodingIvarsDict
    #@+node:ekr.20041117072055:ivarsDict
    # Each of these settings sets the ivar with the same name.
    ivarsDict = {'_hash':'ivarsDict'}
    
    if 0: # From c.__init__
        # Global options
        c.tangle_batch_flag = False
        c.untangle_batch_flag = False
        # Default Tangle options
        c.tangle_directory = ""
        c.use_header_flag = False
        c.output_doc_flag = False
        # Default Target Language
        c.target_language = "python" # Required if leoConfig.txt does not exist.
    
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
        ("trailing_body_newlines","string","asis"),
        ("use_plugins","bool",False),
            # Should never be True here!
        # use_pysco can not be set by 4.3:  config processing happens too late.
            # ("use_psyco","bool",False),
        ("undo_granularity","string","word"),
            # "char","word","line","node"
        ("write_strips_blank_lines","bool",False),
    )
    #@nonl
    #@-node:ekr.20041117072055:ivarsDict
    #@-others
    
    # Shortcut stuff.
    keysDict = {}
    rawKeysDict = {}
        
    # List of dictionaries to search.  Order not too important.
    dictList = [ivarsDict,encodingIvarsDict,defaultsDict]
        
    # Keys are commanders.  Values are optionsDicts.
    localOptionsDict = {}
    
    localOptionsList = []
        
    # Keys are setting names, values are type names.
    warningsDict = {} # Used by get() or allies.
    #@nonl
    #@-node:ekr.20041122094813:<<  baseConfig data >>
    #@nl
    #@    @+others
    #@+node:ekr.20041117083202:Birth...
    #@+node:ekr.20041117062717.2:ctor & init
    def __init__ (self):
    
        for key,type,val in self.defaultsData:
            self.defaultsDict[self.munge(key)] = type,val
            
        for key,type,val in self.ivarsData:
            self.ivarsDict[self.munge(key)] = key,type,val
    
        for key,type,val in self.encodingIvarsData:
            self.encodingIvarsDict[self.munge(key)] = key,type,val
    
        self.init()
    
    def init (self):
    
        self.configsExist = False # True when we successfully open a setting file.
        self.defaultFont = None # Set in gui.getDefaultConfigFont.
        self.defaultFontFamily = None # Set in gui.getDefaultConfigFont.
        self.dictList = [self.defaultsDict]
            ### self.ivarsDict,self.encodingIvarsDict,self.defaultsDict] # List of dictionaries.
        self.inited = False
    
        self.initIvarsFromSettings()
        self.initSettingsFiles()
        self.initRecentFiles()
        self.initRawKeysDict()
        
        self.use_plugins = True ### Testing??
    #@nonl
    #@-node:ekr.20041117062717.2:ctor & init
    #@+node:ekr.20041117065611.1:initEncoding
    def initEncoding (self,encodingName):
        
        data = self.encodingIvarsDict.get(self.munge(encodingName))
        ivarName,theType,encoding = data
    
        # g.trace(ivarName,encodingName,encoding)
        
        if ivarName:
            setattr(self,ivarName,encoding)
    
        if encoding and not g.isValidEncoding(encoding):
            g.es("bad %s: %s" % (encodingName,encoding))
    #@nonl
    #@-node:ekr.20041117065611.1:initEncoding
    #@+node:ekr.20041117065611:initIvar
    def initIvar(self,ivarName):
        
        data = self.ivarsDict.get(self.munge(ivarName))
        ivarName,theType,val = data
    
        # g.trace(ivarName,val)
    
        setattr(self,ivarName,val)
    #@nonl
    #@-node:ekr.20041117065611:initIvar
    #@+node:ekr.20041117065611.2:initIvarsFromSettings
    def initIvarsFromSettings (self):
        
        for ivar in self.encodingIvarsDict.keys():
            if ivar != '_hash':
                self.initEncoding(ivar)
            
        for ivar in self.ivarsDict.keys():
            if ivar != '_hash':
                self.initIvar(ivar)
    #@nonl
    #@-node:ekr.20041117065611.2:initIvarsFromSettings
    #@+node:ekr.20041117062717.24:initRawKeysDict
    def initRawKeysDict (self):
    
        for key in self.keysDict.keys():
            if key != '_hash':
                newKey = key.replace('&','')
                self.rawKeysDict[newKey] = key,self.keysDict[key]
    
        if 0: #trace
            keys = self.rawKeysDict.keys()
            keys.sort()
            for key in keys:
                print self.rawKeysDict[key]
    #@nonl
    #@-node:ekr.20041117062717.24:initRawKeysDict
    #@+node:ekr.20041117083202.2:initRecentFiles
    def initRecentFiles (self):
    
        self.recentFiles = []
    #@nonl
    #@-node:ekr.20041117083202.2:initRecentFiles
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
    #@+node:ekr.20041117083141:get & allies
    def get (self,c,setting,theType):
        
        """Get the setting and make sure its type matches the expected type."""
        
        found = False
        if c:
            d = self.localOptionsDict.get(c.hash())
            if d:
                val,found = self.getValFromDict(d,setting,theType,found)
                if val is not None:
                    # g.trace(c.hash())
                    return val
                    
        for d in self.localOptionsList:
            val,found = self.getValFromDict(d,setting,theType,found)
            if val is not None:
                dType = d.get('_hash','<no hash>')
                # g.trace(dType,val)
                return val
    
        for d in self.dictList:
            val,found = self.getValFromDict(d,setting,theType,found)
            if val is not None:
                dType = d.get('_hash','<no hash>')
                # g.trace(dType,setting,val)
                return val
                    
        if 1: # Good for debugging leoSettings.leo.  This is NOT an error.
            # Don't warn if None was specified.
            if not found and self.inited:
                g.trace("Not found:",setting)
    
        return None
    #@nonl
    #@+node:ekr.20041121143823:getValFromDict
    def getValFromDict (self,d,setting,requestedType,found):
    
        data = d.get(self.munge(setting))
        if data:
            # g.trace(setting,requestedType,data)
            found = True
            if len(data) == 2:
                path = None ; dType,val = data
            elif len(data) == 3:
                path,dType,val = data
            else:
                g.trace("bad tuple",data)
                return None,found
            if val not in (u'None',u'none','None','none','',None):
                # g.trace(setting,val)
                return val,found
    
        # Do NOT warn if not found here.  It may be in another dict.
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
    def getRecentFiles (self,c):
        
        # Must get c's recent files.
        return self.recentFiles
    #@nonl
    #@-node:ekr.20041117062717.11:getRecentFiles
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
            else:
                setattr(c,setting,val)
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
    #@-node:ekr.20041117081009:Getters...
    #@+node:ekr.20041118084146:Setters
    #@+node:ekr.20041118084146.1:set (g.app.config)
    def set (self,c,setting,kind,val):
        
        """Set the setting and make sure its type matches the given type."""
    
        found = False
        if c:
            d = self.localOptionsDict.get(c.hash())
            if d: found = True
            
        if not found:
            hash = c.hash()
            for d in self.localOptionsList:
                hash2 = d.get('_hash')
                if hash == hash2:
                    found = True ; break
                    
        if not found:
            d = self.dictList [0]
    
        d[self.munge(setting)] = kind,val
    
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
    #@+node:ekr.20041201080436:config.appendToRecentFiles
    def appendToRecentFiles (self,files):
        
        for file in files:
            if file in self.recentFiles:
                self.recentFiles.remove(file)
            # g.trace(file)
            self.recentFiles.append(file)
    #@nonl
    #@-node:ekr.20041201080436:config.appendToRecentFiles
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
        c,frame = g.app.gui.newLeoCommanderAndFrame(path,updateRecentFiles=False)
        frame.log.enable(False)
        g.app.setLog(frame.log,"openWithFileName")
        g.app.lockLog()
        frame.c.fileCommands.open(theFile,path,readAtFileNodesFlag=False) # closes theFile.
        g.app.unlockLog()
        frame.openDirectory = g.os_path_dirname(path)
        g.app.gui = oldGui
        return c
    #@nonl
    #@-node:ekr.20041117085625:openSettingsFile
    #@+node:ekr.20041120064303:config.readSettingsFiles
    def readSettingsFiles (self,fileName,verbose=True):
        
        munge = self.munge
        
        seen = []
        
        # Init settings from leoSettings.leo files.
        for path,setOptionsFlag in (
            (self.globalConfigFile,False),
            (self.homeFile,False),
            (fileName,True),
        ):
            if path and path.lower() not in seen:
                seen.append(path.lower())
                if verbose:
                    # A print statement here is clearest.
                    print "reading settings in %s" % path
                c = self.openSettingsFile(path)
                if c:
                    d = self.readSettings(c)
                    if d:
                        hash = c.hash()
                        d['_hash'] = hash
                        # g.trace('*****',hash)
                        if setOptionsFlag:
                            self.localOptionsDict[hash] = d
                            #@                        << update recent files from d >>
                            #@+node:ekr.20041201081440:<< update recent files from d >>
                            for key in d.keys():
                                if munge(key) == "recentfiles":
                                    data = d.get(key)
                                    # Entries were created by parserBaseClass.set.
                                    # They have the form: path,kind,val
                                    path,kind,files = data
                                    files = [file.strip() for file in files]
                                    if 0:
                                        print "config.readSettingsFiles.  recent files..."
                                        for file in files:
                                            print file
                                    self.appendToRecentFiles(files)
                            #@nonl
                            #@-node:ekr.20041201081440:<< update recent files from d >>
                            #@nl
                        else:
                            self.localOptionsList.insert(0,d)
                    else:
                        g.es("No @settings tree in %s",color="red")
                    g.app.destroyWindow(c.frame)
    
        self.inited = True
    #@-node:ekr.20041120064303:config.readSettingsFiles
    #@+node:ekr.20041117083857.1:readSettings
    # Called to read all leoSettings.leo files.
    # Also called when opening an .leo file to read @settings tree.
    
    def readSettings (self,c):
        
        """Read settings from a file that may contain an @settings tree."""
        
        # g.trace(c.mFileName)
        
        # Create a settings dict for c for set()
        if c and self.localOptionsDict.get(c.hash()) is None:
            self.localOptionsDict[c.hash()] = {}
    
        parser = settingsTreeParser(c)
        d = parser.traverse()
    
        return d
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
    # These are the canonicalized names.  Case is ignored, as are '_' and '-' characters.
    
    basic_types = [
        # Headlines have the form @kind name = var
        'bool','color','directory','int','ints',
        'float','path','ratio','shortcut','string','strings']
    
    control_types = [
        'font','if','ifgui','ifplatform','ignore','page',
        'recentfiles','settings','shortcuts']
    
    # Keys are settings names, values are (type,value) tuples.
    settingsDict = {}
    #@nonl
    #@-node:ekr.20041121130043:<< parserBaseClass data >>
    #@nl
    
    #@    @+others
    #@+node:ekr.20041119204700: ctor
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
            'recentfiles':  self.doRecentFiles,
            'shortcuts':    self.doShortcuts,
            'string':       self.doString,
            'strings':      self.doStrings,
        }
    #@nonl
    #@-node:ekr.20041119204700: ctor
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
    
        name = name.strip()
        i = name.find('[')
        j = name.find(']')
    
        if -1 < i < j:
            items = name[i+1:j]
            items = items.split(',')
            try:
                items = [int(item.strip()) for item in items]
            except ValueError:
                items = []
                self.valueError(p,kind,name,val)
        
            name = name[j+1:].strip()
            kind = "ints[%s]" % (','.join([str(item) for item in items]))
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
    #@+node:ekr.20041121151924:doRecentFiles
    def doRecentFiles (self,p,kind,name,val):
        
        s = p.bodyString().strip()
        if s:
            lines = g.splitLines(s)
            self.set(p,"recent-files","recent-files",lines)
    #@nonl
    #@-node:ekr.20041121151924:doRecentFiles
    #@+node:ekr.20041120113848:doShortcut
    def doShortcut(self,p,kind,name,val):
        
        # At present no checking is done.
        self.set(p,kind,name,val)
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
                    self.set(p,"shortcut",name,val)
    #@nonl
    #@-node:ekr.20041120105609:doShortcuts
    #@+node:ekr.20041217132028:doString
    def doString (self,p,kind,name,val):
        
        # At present no checking is done.
        self.set(p,kind,name,val)
    #@-node:ekr.20041217132028:doString
    #@+node:ekr.20041120094940.8:doStrings
    def doStrings (self,p,kind,name,val):
        
        name = name.strip()
        i = name.find('[')
        j = name.find(']')
    
        if -1 < i < j:
            items = name[i+1:j]
            items = items.split(',')
            items = [item.strip() for item in items]
    
            name = name[j+1:].strip()
            kind = "strings[%s]" % (','.join(items))
            # g.trace(repr(kind),repr(name),val)
    
            # At present no checking is done.
            self.set(p,kind,name,val)
    #@nonl
    #@-node:ekr.20041120094940.8:doStrings
    #@-node:ekr.20041120094940:kind handlers
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
            self.parseFontLine(p,line,d)
            
        comments = d.get('comments')
        d['comments'] = '\n'.join(comments)
            
        return d
    #@nonl
    #@-node:ekr.20041213082558.1:parseFont
    #@+node:ekr.20041213082558.2:parseFontLine
    def parseFontLine (self,p,line,d):
        
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
            kind = s[1:i]
            if kind:
                # name is everything up to '='
                j = s.find('=',i)
                if j == -1:
                    name = s[i:]
                else:
                    name = s[i:j]
                    # val is everything after the '='
                    val = s[j+1:].strip()
    
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
    #@-node:ekr.20041213082558:parsers
    #@+node:ekr.20041120094940.9:set (settingsParser)
    def set (self,p,kind,name,val):
        
        """Init the setting for name to val."""
        
        # p used in subclasses, not here.
        
        c = self.c
        
        # g.trace("settingsParser %10s %15s %s" %(kind,val,name))
        
        d = self.settingsDict
    
        data = d.get(self.munge(name))
        if data:
            if len(data) == 2: path2 = None
            else: path2 = data[0]
            if g.os_path_abspath(c.mFileName) != g.os_path_abspath(path2):
                g.es("over-riding setting: %s from %s" % (name,path2))
    
        # N.B.  We can't use c here: it may be destroyed!
        d[self.munge(name)] = c.mFileName,kind,val
        
        data = g.app.config.ivarsDict.get(self.munge(name))
        if data:
            ivarName = data[0]
            # g.trace("g.app.%s = %s" % (ivarName,val))
            setattr(g.app.config,ivarName,val)
    #@nonl
    #@-node:ekr.20041120094940.9:set (settingsParser)
    #@+node:ekr.20041119204700.1:traverse
    def traverse (self):
        
        c = self.c
        
        p = g.app.config.settingsRoot(c)
        if not p:
            return None
    
        self.settingsDict = {}
        after = p.nodeAfterTree()
        while p and p != after:
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
                f(p,kind,name,val)
            except TypeError:
                g.es_exception()
                print "*** no handler",kind
        elif name:
            # self.error("unknown type %s for setting %s" % (kind,name))
            # Just assume the type is a string.
            self.set(p,kind,name,val)
    #@nonl
    #@-node:ekr.20041119204714:visitNode
    #@-others
#@nonl
#@-node:ekr.20041119203941.3:class settingsTreeParser (parserBaseClass)
#@-others
#@nonl
#@-node:ekr.20041119205325:parser classes
#@-others
#@-node:ekr.20041117062700:@thin leoConfig.py
#@-leo
