#@+leo-ver=4-thin
#@+node:ekr.20031218072017.3001:@thin leoConfig.py
#@@language python

import leoGlobals as g
from leoGlobals import true,false

import ConfigParser,exceptions,os,string,sys

class baseConfig:
	"""The base class for Leo's configuration handler."""
	#@	<< define defaultsDict >>
	#@+node:ekr.20031218072017.2404:<< define defaultsDict >>
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
		"ignore_blank_lines" : 1,
		"limit_count" : 9,
		"print_mismatching_lines" : 1,
		"print_trailing_lines" : 1,
		# find/change options...
		"search_body" : 1,
		"whole_word" : 1,
		# Prefs panel.
		"default_target_language" : "Python",
		"tab_width" : 4,
		"page_width" : 132,
		"output_doc_chunks" : 1,
		"tangle_outputs_header" : 1,
		# Syntax coloring options...
		# Defaults for colors are handled by leoColor.py.
		"color_directives_in_plain_text" : 1,
		"underline_undefined_section_names" : 1,
		# Window options...
		"allow_clone_drags" : 1,
		"body_pane_wraps" : 1,
		"body_text_font_family" : "Courier",
		"body_text_font_size" : defaultBodyFontSize,
		"body_text_font_slant" : "roman",
		"body_text_font_weight" : "normal",
		"enable_drag_messages" : 1,
		"headline_text_font_size" : defaultTreeFontSize,
		"headline_text_font_slant" : "roman",
		"headline_text_font_weight" : "normal",
		"log_text_font_size" : defaultLogFontSize,
		"log_text_font_slant" : "roman",
		"log_text_font_weight" : "normal",
		"initial_window_height" : 600, # 7/24/03: In pixels.
		"initial_window_width" :  800, # 7/24/03: In pixels.
		"initial_window_left" : 10,
		"initial_window_top" : 10,
		"initial_splitter_orientation" : "vertical",
		"initial_vertical_ratio" : 0.5,
		"initial_horizontal_ratio" : 0.3,
		"initial_horizontal_secondary_ratio" : 0.5,
		"initial_vertical_secondary_ratio" : 0.7,
		"outline_pane_scrolls_horizontally" : 0,
		"split_bar_color" : "LightSteelBlue2",
		"split_bar_relief" : "groove",
		"split_bar_width" : 7 }
	#@nonl
	#@-node:ekr.20031218072017.2404:<< define defaultsDict >>
	#@nl
	#@	@+others
	#@+node:ekr.20031218072017.3002:config.__init__
	def __init__ (self):
	
		self.init()
	
	def init (self):
	
		try:
			self.configDir = sys.leo_config_directory
		except:
			self.configDir = g.os_path_join(g.app.loadDir,"..","config")
	
		self.configFileName = g.os_path_join(self.configDir,"leoConfig.txt")
	
		self.configsExist = false # true when we successfully open leoConfig.txt.
		
		# These are now set in gui.getDefaultConfigFont
		self.defaultFont = None
		self.defaultFontFamily = None
		
		#@	<< initialize constant ivars, lists & dicts >>
		#@+node:ekr.20031218072017.3003:<< initialize constant ivars, lists & dicts >> (leoConfig)
		# Names of sections.
		self.configSection = "config options"
		self.compareSection = "compare options"
		self.findSection = "find/change options"
		self.keysSection = "keyboard shortcuts"
		self.prefsSection = "prefs panel options"
		self.recentFilesSection = "recent files"
		self.colorsSection = "syntax coloring options"
		self.windowSection = "window options"
		
		# List of recent files.
		self.recentFiles = []
		
		# Section dictionaries
		self.compareDict = {}
		self.configDict = {} # 10/11/02: we use a dict even for ivars.
		self.findDict = {}
		self.keysDict = {} ; self.rawKeysDict = {} # 2/8/04
		self.prefsDict = {}
		self.colorsDict = {}
		self.windowDict = {}
		
		# Associations of sections and dictionaries.
		self.sectionInfo = (
			(self.configSection,self.configDict),
			(self.compareSection,self.compareDict),
			(self.findSection,self.findDict),
			(self.keysSection,self.keysDict),
			(self.prefsSection,self.prefsDict),
			(self.recentFilesSection,None),
			(self.colorsSection,self.colorsDict),
			(self.windowSection,self.windowDict) )
		#@nonl
		#@-node:ekr.20031218072017.3003:<< initialize constant ivars, lists & dicts >> (leoConfig)
		#@nl
		#@	<< initialize ivars that may be set by config options >>
		#@+node:ekr.20031218072017.3004:<< initialize ivars that may be set by config options >>
		# 10/11/02: Defaults are specified only here.
		
		self.at_root_bodies_start_in_doc_mode = true # For compatibility with previous versions.
		self.config = None # The current instance of ConfigParser
		self.config_encoding = "utf-8" # Encoding used for leoConfig.txt.
		self.create_nonexistent_directories = false
		self.default_derived_file_encoding = "utf-8"
		self.load_derived_files_immediately = 0
		self.new_leo_file_encoding = "UTF-8" # Upper case for compatibility with previous versions.
		self.output_initial_comment = "" # "" or None for compatibility with previous versions.
		self.output_newline = "nl"
		self.read_only = true # Make sure we don't alter an illegal leoConfig.txt file!
		self.redirect_execute_script_output_to_log_pane = false
		self.relative_path_base_directory = "!"
		self.remove_sentinels_extension = ".txt"
		self.save_clears_undo_buffer = false
		self.stylesheet = None
		self.tkEncoding = None # Defaults to None so it doesn't override better defaults.
		self.use_plugins = false # Should never be true here!
		self.use_psyco = false
		self.undo_granularity = "word" # "char","word","line","node"
		self.write_old_format_derived_files = false # Use new format if leoConfig.txt does not exist.
		#@nonl
		#@-node:ekr.20031218072017.3004:<< initialize ivars that may be set by config options >>
		#@nl
	
		self.open() # read and process the configuration file.
	#@nonl
	#@-node:ekr.20031218072017.3002:config.__init__
	#@+node:ekr.20031218072017.3005:getters/setters
	#@+node:ekr.20031218072017.1932:get...FromDict & setDict
	def getBoolFromDict (self,name,dict):
		val = self.getIntFromDict(name,dict)
		if val != None:
			if val: val = 1
			else: val = 0
		return val
	
	def getFloatFromDict (self,name,dict):
		val = self.getFromDict(name,dict)
		if val:
			try: val = float(val)
			except: val = None
		return val
	
	def getFromDict (self,name,dict):
		val = dict.get(name)
		if val == "ignore":
			val = None
		elif val == None:
			val = self.defaultsDict.get(name)
			val = g.toUnicode(val,self.config_encoding) # 10/31/03
		return val
	
	def getIntFromDict (self,name,dict):
		val = self.getFromDict(name,dict)
		try:
			return int(val)
		except:
			return 0
	
	def setDict (self,name,val,dict):
		dict [name] = val
			
	getStringFromDict = getFromDict
	#@nonl
	#@-node:ekr.20031218072017.1932:get...FromDict & setDict
	#@+node:ekr.20031218072017.3006:get/setColors
	def getBoolColorsPref (self,name):
		return self.getBoolFromDict(name,self.colorsDict)
		
	# Basic getters and setters.
	
	def getColorsPref (self,name):
		return self.getFromDict(name,self.colorsDict)
	
	def setColorsPref (self,name,val):
		self.setDict(name,val,self.colorsDict)
		
	getStringColorsPref = getColorsPref
	#@nonl
	#@-node:ekr.20031218072017.3006:get/setColors
	#@+node:ekr.20031218072017.3007:get/setComparePref
	def getBoolComparePref (self,name):
		return self.getBoolFromDict(name,self.compareDict)
		
	def getIntComparePref (self,name):
		return self.getIntFromDict(name,self.compareDict)
	
	# Basic getters and setters.
	
	def getComparePref (self,name):
		return self.getFromDict(name,self.compareDict)
	
	def setComparePref (self,name,val):
		self.setDict(name,val,self.compareDict)
		
	getStringComparePref = getComparePref
	#@nonl
	#@-node:ekr.20031218072017.3007:get/setComparePref
	#@+node:ekr.20031218072017.3008:get/setFindPref
	def getBoolFindPref (self,name):
		return self.getBoolFromDict(name,self.findDict)
	
	# Basic getters and setters.
	
	def getFindPref (self,name):
		return self.getFromDict(name,self.findDict)
	
	def setFindPref (self,name,val):
		self.setDict(name,val,self.findDict)
		
	getStringFindPref = getFindPref
	#@nonl
	#@-node:ekr.20031218072017.3008:get/setFindPref
	#@+node:ekr.20031218072017.3009:get/setPref
	def getBoolPref (self,name):
		return self.getBoolFromDict(name,self.prefsDict)
	
	def getIntPref (self,name):
		return self.getIntFromDict(name,self.prefsDict)
		
	# Basic getters and setters.
	
	def getPref (self,name):
		return self.getFromDict(name,self.prefsDict)
	
	def setPref (self,name,val):
		self.setDict(name,val,self.prefsDict)
		
	getStringPref = getPref
	#@nonl
	#@-node:ekr.20031218072017.3009:get/setPref
	#@+node:ekr.20031218072017.3010:get/setRecentFiles
	def getRecentFiles (self):
		
		return self.recentFiles
	
	def setRecentFiles (self,files):
	
		self.recentFiles = files
	#@-node:ekr.20031218072017.3010:get/setRecentFiles
	#@+node:ekr.20031218072017.3011:get/setWindowPrefs
	def getBoolWindowPref (self,name):
		return self.getBoolFromDict(name,self.windowDict)
		
	def getFloatWindowPref (self,name):
		return self.getFloatFromDict(name,self.windowDict)
		
	def getIntWindowPref (self,name):
		return self.getIntFromDict(name,self.windowDict)
		
	# Basic getters and setters.
	
	def getWindowPref (self,name):
		return self.getFromDict(name,self.windowDict)
	
	def setWindowPref (self,name,val):
		self.setDict(name,val,self.windowDict)
		
	getStringWindowPref = getWindowPref
	#@nonl
	#@-node:ekr.20031218072017.3011:get/setWindowPrefs
	#@+node:ekr.20031218072017.2174:config.getFontFromParams
	def getFontFromParams(self,family,size,slant,weight,defaultSize=12,tag=""):
	
		"""Compute a font from font parameters.
	
		Arguments are the names of settings to be use.
		We default to size=12, slant="roman", weight="normal".
	
		We return None if there is no family setting so we can use system default fonts."""
	
		family = self.getWindowPref(family)
		if family in (None,""):
			# print tag,"using default"
			family = self.defaultFontFamily
			
		size = self.getIntWindowPref(size)
		if size in (None,0): size = defaultSize
		
		slant = self.getWindowPref(slant)
		if slant in (None,""): slant = "roman"
		
		weight = self.getWindowPref(weight)
		if weight in (None,""): weight = "normal"
		
		# if g.app.trace: g.trace(tag,family,size,slant,weight)
		
		return g.app.gui.getFontFromParams(family,size,slant,weight)
	#@nonl
	#@-node:ekr.20031218072017.2174:config.getFontFromParams
	#@+node:ekr.20031218072017.1722:getShortcut (config)
	def getShortcut (self,name):
		
		if 1: # 2/8/04: allow & in keys.
			val = self.rawKeysDict.get(name.replace('&',''))
			if val:
				rawKey,shortcut = val
				return rawKey,shortcut
			else:
				return None,None
		else:
			val = self.keysDict.get(name)
			
			# 7/19/03: Return "None" if the setting is "None"
			# This allows settings to disable a default shortcut.
			return val
	#@nonl
	#@-node:ekr.20031218072017.1722:getShortcut (config)
	#@+node:ekr.20031218072017.3012:init/Boolean/ConfigParam
	def initConfigParam (self,name,defaultVal):
		try:
			val = self.config.get(self.configSection,name,raw=1) # 2/4/03
		except:
			val = defaultVal
		return val
	
	def initBooleanConfigParam (self,name,defaultVal):
		try:
			val = self.config.getboolean(self.configSection,name)
		except:
			val = defaultVal
		return val
	#@-node:ekr.20031218072017.3012:init/Boolean/ConfigParam
	#@+node:ekr.20031218072017.3013:setCommandsFindIvars
	# Sets ivars of c that can be overridden by leoConfig.txt
	
	def setCommandsFindIvars (self,c):
		
		if g.app.gui.guiName() != "tkinter":
			return
	
		config = self ; findFrame = g.app.findFrame
	
		# N.B.: separate c.ivars are much more convenient than a dict.
		for s in findFrame.intKeys:
			val = config.getBoolFindPref(s)
			if val != None: # 10/2/03
				setattr(c,s+"_flag",val)
				# g.trace(s+"_flag",val)
				
		val = config.getStringFindPref("change_string")
		if val: c.change_text = val
		
		val = config.getStringFindPref("find_string")
		if val: c.find_text = val
	
		g.app.findFrame.init(c)
	#@nonl
	#@-node:ekr.20031218072017.3013:setCommandsFindIvars
	#@+node:ekr.20031218072017.3014:setCommandsIvars
	# Sets ivars of c that can be overridden by leoConfig.txt
	
	def setCommandsIvars (self,c):
	
		config = self
		#@	<< set prefs ivars >>
		#@+node:ekr.20031218072017.3015:<< set prefs ivars >>
		val = config.getIntPref("tab_width")
		if val: c.tab_width = val
		
		val = config.getIntPref("page_width")
		if val: c.page_width = val
		
		val = config.getIntPref("run_tangle_done.py")
		if val: c.tangle_batch_flag = val
		
		val = config.getIntPref("run_untangle_done.py")
		if val: c.untangle_batch_flag = val
		
		val = config.getIntPref("output_doc_chunks")
		if val: c.output_doc_flag = val
		
		val = config.getIntPref("tangle_outputs_header")
		if val: c.use_header_flag = val
		
		val = config.getPref("default_tangle_directory")
		if val: c.tangle_directory = val
		
		val = config.getPref("find_string")
		if val: c.tangle_directory = val
		
		c.target_language = "python" # default
		val = config.getPref("default_target_language")
		if val:
			try:
				val = string.lower(val)
				val = string.replace(val,"/","")
				if g.app.language_delims_dict.get(val):
					c.target_language = val
				
			except: pass
		#@nonl
		#@-node:ekr.20031218072017.3015:<< set prefs ivars >>
		#@nl
	#@nonl
	#@-node:ekr.20031218072017.3014:setCommandsIvars
	#@+node:ekr.20031218072017.3016:setConfigFindIvars
	def setConfigFindIvars (self,c):
		
		"""Set the config ivars from the commander."""
		
		findFrame = g.app.findFrame
	
		# N.B.: separate c.ivars are much more convenient than a dict.
		for s in findFrame.intKeys: # These _are_ gui-independent.
			val = getattr(c,s+"_flag")
			self.setFindPref(s,val)
			# g.trace(s,val)
		
		self.setFindPref("change_string",c.change_text)
		self.setFindPref("find_string",c.find_text)
	#@nonl
	#@-node:ekr.20031218072017.3016:setConfigFindIvars
	#@+node:ekr.20031218072017.3017:c.setConfigIvars
	# Sets config ivars from c.
	
	def setConfigIvars (self,c):
		
		if c.target_language and g.app.language_delims_dict.get(c.target_language):
			language = c.target_language
		else:
			language = "plain"
		self.setPref("default_tangle_directory",c.tangle_directory)
		self.setPref("default_target_language",language)
		self.setPref("output_doc_chunks",str(c.output_doc_flag))
		self.setPref("page_width",str(c.page_width))
		self.setPref("run_tangle_done.py",str(c.tangle_batch_flag))
		self.setPref("run_untangle_done.py",str(c.untangle_batch_flag))
		self.setPref("tab_width",str(c.tab_width))
		self.setPref("tangle_outputs_header",str(c.use_header_flag))
		
		self.setFindPref("batch",str(c.batch_flag))
		self.setFindPref("ignore_case",str(c.ignore_case_flag))
		self.setFindPref("mark_changes",str(c.mark_changes_flag))
		self.setFindPref("mark_finds",str(c.mark_finds_flag))
		self.setFindPref("pattern_match",str(c.pattern_match_flag))
		self.setFindPref("reverse",str(c.reverse_flag))
		self.setFindPref("script_change",str(c.script_change_flag))
		self.setFindPref("script_search",str(c.script_search_flag))
		self.setFindPref("search_body",str(c.search_body_flag))
		self.setFindPref("search_headline",str(c.search_headline_flag))
		self.setFindPref("selection_only",str(c.selection_only_flag)) # 11/9/03
		self.setFindPref("suboutline_only",str(c.suboutline_only_flag))
		self.setFindPref("wrap",str(c.wrap_flag))
		self.setFindPref("whole_word",str(c.whole_word_flag))
		
		self.setFindPref("change_string",c.change_text)
		self.setFindPref("find_string",c.find_text)
	#@nonl
	#@-node:ekr.20031218072017.3017:c.setConfigIvars
	#@-node:ekr.20031218072017.3005:getters/setters
	#@+node:ekr.20031218072017.1929:open
	def open (self):
		
		config = ConfigParser.ConfigParser()
		self.config = config
		try:
			cf = open(self.configFileName)
			config.readfp(cf)
			#@		<< get config options >>
			#@+node:ekr.20031218072017.1421:<< get config options >>
			#@+at 
			#@nonl
			# Rewritten 10/11/02 as follows:
			# 
			# 1. We call initConfigParam and initBooleanConfigParam to get the 
			# values.
			# 
			# The general purpose code will enter all these values into 
			# configDict.  This allows update() to write the configuration 
			# section without special case code.  configDict is not accessible 
			# by the user.  Rather, for greater speed the user access these 
			# values via the ivars of this class.
			# 
			# 2. We pass the ivars themselves as params so that default 
			# initialization is done in the ctor, as would normally be 
			# expected.
			#@-at
			#@@c
			
			self.at_root_bodies_start_in_doc_mode = self.initBooleanConfigParam(
				"at_root_bodies_start_in_doc_mode",self.at_root_bodies_start_in_doc_mode)
				
			encoding = self.initConfigParam(
				"config_encoding",self.config_encoding)
				
			if g.isValidEncoding(encoding):
				self.config_encoding = encoding
			else:
				g.es("bad config_encoding: " + encoding)
				
			self.create_nonexistent_directories = self.initBooleanConfigParam(
				"create_nonexistent_directories",self.create_nonexistent_directories)
				
			encoding = self.initConfigParam(
				"default_derived_file_encoding",self.default_derived_file_encoding)
			
			if g.isValidEncoding(encoding):
				self.default_derived_file_encoding = encoding
			else:
				g.es("bad default_derived_file_encoding: " + encoding)
				
			self.load_derived_files_immediately = self.initBooleanConfigParam(
				"load_derived_files_immediately",self.load_derived_files_immediately)
				
			encoding = self.initConfigParam(
				"new_leo_file_encoding",
				self.new_leo_file_encoding)
			
			if g.isValidEncoding(encoding):
				self.new_leo_file_encoding = encoding
			else:
				g.es("bad new_leo_file_encoding: " + encoding)
			
			self.output_initial_comment = self.initConfigParam(
				"output_initial_comment",self.output_initial_comment)
			
			self.output_newline = self.initConfigParam(
				"output_newline",self.output_newline)
			
			self.read_only = self.initBooleanConfigParam(
				"read_only",self.read_only)
			
			self.relative_path_base_directory = self.initConfigParam(
				"relative_path_base_directory",self.relative_path_base_directory)
				
			self.redirect_execute_script_output_to_log_pane = self.initBooleanConfigParam(
				"redirect_execute_script_output_to_log_pane",
				self.redirect_execute_script_output_to_log_pane)
				
			self.remove_sentinels_extension = self.initConfigParam(
				"remove_sentinels_extension",self.remove_sentinels_extension)
			
			self.save_clears_undo_buffer = self.initBooleanConfigParam(
				"save_clears_undo_buffer",self.save_clears_undo_buffer)
				
			self.stylesheet = self.initConfigParam(
				"stylesheet",self.stylesheet)
				
			encoding = self.initConfigParam(
				"tk_encoding",self.tkEncoding)
				
			if encoding and len(encoding) > 0: # May be None.
				if g.isValidEncoding(encoding):
					self.tkEncoding = encoding
				else:
					g.es("bad tk_encoding: " + encoding)
					
			# g.trace("config.self.tkEncoding",self.tkEncoding)
			
			g.app.use_gnx = self.initBooleanConfigParam(
				"use_gnx",g.app.use_gnx)
			# g.trace("g.app.use_gnx",g.app.use_gnx)
				
			self.use_plugins = self.initBooleanConfigParam(
				"use_plugins",self.use_plugins)
			
			self.use_psyco = self.initBooleanConfigParam(
				"use_psyco",self.use_psyco)
				
			self.undo_granularity = self.initConfigParam(
				"undo_granularity",self.undo_granularity)
				
			self.write_old_format_derived_files = self.initBooleanConfigParam(
				"write_old_format_derived_files",self.write_old_format_derived_files)
			#@-node:ekr.20031218072017.1421:<< get config options >>
			#@nl
			#@		<< get recent files >>
			#@+node:ekr.20031218072017.1930:<< get recent files >>
			section = self.recentFilesSection
			
			if 0: # elegant, but may be a security hole.
				self.recentFiles = eval(config.get(section,"recentFiles",raw=1)) # 2/4/03
			else: # easier to read in the config file.
				try:
					for i in xrange(10):
						f = config.get(section,"file" + str(i),raw=1)
						f = g.toUnicode(f,"utf-8") # 10/31/03
						self.recentFiles.append(f)
				except: pass
			#@nonl
			#@-node:ekr.20031218072017.1930:<< get recent files >>
			#@nl
			for section, dict in self.sectionInfo:
				if dict != None:
					try:
						for opt in config.options(section):
							val = config.get(section,opt,raw=1)
							val = g.toUnicode(val,self.config_encoding) # 10/31/03
							dict[string.lower(opt)]= val
					except: pass
			#@		<< create rawKeysDict without ampersands >>
			#@+node:ekr.20040208104150:<< create rawKeysDict without ampersands >> (config)
			# 2/8/04: New code.
			for key in self.keysDict.keys():
				newKey = key.replace('&','')
				self.rawKeysDict[newKey] = key,self.keysDict[key]
				
			if 0: #trace
				keys = self.rawKeysDict.keys()
				keys.sort()
				for key in keys:
					print self.rawKeysDict[key]
			#@nonl
			#@-node:ekr.20040208104150:<< create rawKeysDict without ampersands >> (config)
			#@nl
			#@		<< convert find/change options to unicode >>
			#@+node:ekr.20031218072017.1422:<< convert find/change options to unicode >>
			find = self.findDict.get("find_string")
			if find:
				# Leo always writes utf-8 encoding, but users may not.
				find = g.toUnicode(find,"utf-8")
				self.findDict["find_string"] = find
			
			change = self.findDict.get("change_string")
			if change:
				# Leo always writes utf-8 encoding, but users may not.
				change = g.toUnicode(change,"utf-8")
				self.findDict["change_string"] = change
			#@-node:ekr.20031218072017.1422:<< convert find/change options to unicode >>
			#@nl
			#@		<< print options >>
			#@+node:ekr.20031218072017.1931:<< print options >>
			if 0:
				print "\n\ncolorsDict:\n" ,self.colorsDict
				print "\n\ncompareDict:\n",self.compareDict
				print "\n\nfindDict:\n"   ,self.findDict
				print "\n\nprefsDict:\n"  ,self.prefsDict
				print "\n\nwindowDict:\n" ,self.windowDict
			if 0:
				print "\n\nkeysDict:\n\n"
				for i in self.keysDict.items():
					print i
			if 0:
				print "\n\nwindowDict:\n\n"
				for i in self.windowDict.keys():
					print i
			#@nonl
			#@-node:ekr.20031218072017.1931:<< print options >>
			#@nl
			cf.close()
			self.configsExist = true
		except IOError:
			pass
		except:
			g.es("Exception opening " + self.configFileName)
			g.es_exception()
			pass
		self.config = None
	#@-node:ekr.20031218072017.1929:open
	#@+node:ekr.20031218072017.1145:update (config)
	# Rewrites the entire config file from ivars.
	# This is called when a .leo file is written and when the preferences panel changes.
	
	def update (self):
		
		# Do nothing if the file does not exist, or if read_only.
		if self.read_only:
			# print "Read only config file"
			return
		if not g.os_path_exists(self.configFileName):
			# print "No config file"
			return
		
		config = ConfigParser.ConfigParser()
		self.config = config
		try:
			# 9/1/02: apparently Linux requires w+ and XP requires w.
			mode = g.choose(sys.platform=="win32","wb","wb+")
			cf = open(self.configFileName,mode)
			config.readfp(cf)
			#@		<< write recent files section >>
			#@+node:ekr.20031218072017.1146:<< write recent files section >>
			section = self.recentFilesSection
			files = self.recentFiles
			
			section = g.toEncodedString(section,"utf-8") # 10/31/03
			
			if config.has_section(section):
				config.remove_section(section)
			config.add_section(section)
			
			if 0: # elegant, but may be a security hole.
				config.set(section,"recentFiles",files)
			else: # easier to read in the config file.
				for i in xrange(len(files)):
					f = g.toEncodedString(files[i],self.config_encoding) # 10/31/03
					config.set(section, "file"+str(i), f)
			#@nonl
			#@-node:ekr.20031218072017.1146:<< write recent files section >>
			#@nl
			for section,dict in self.sectionInfo:
				if dict:
					self.update_section(config,section,dict)
			config.write(cf)
			cf.flush()
			cf.close()
		except:
			g.es("exception writing: " + self.configFileName)
			g.es_exception()
		self.config = None
	#@nonl
	#@-node:ekr.20031218072017.1145:update (config)
	#@+node:ekr.20031218072017.1420:update_section
	def update_section (self,config,section,dict):
		
		section = g.toEncodedString(section,self.config_encoding) # 10/31/03
	
		if config.has_section(section):
			config.remove_section(section)
		config.add_section(section)
		
		keys = dict.keys()
		keys.sort() # Not effective.
		for name in keys:
			val = dict [name]
			val  = g.toEncodedString(val,self.config_encoding)
			name = g.toEncodedString(name,self.config_encoding) # 10/31/03
			config.set(section,name,val)
	#@nonl
	#@-node:ekr.20031218072017.1420:update_section
	#@-others
	
class config (baseConfig):
	"""A class to manage configuration settings."""
	pass
#@nonl
#@-node:ekr.20031218072017.3001:@thin leoConfig.py
#@-leo
