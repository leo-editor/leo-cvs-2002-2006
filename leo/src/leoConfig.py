#@+leo-ver=4
#@+node:@file leoConfig.py
#@@language python

from leoGlobals import *
import leoFind
import ConfigParser,exceptions,os,string,sys,tkFont

class baseConfig:
	"""The base class for Leo's configuration handler."""
	#@	<< define defaultsDict >>
	#@+node:<< define defaultsDict >>
	#@+at 
	#@nonl
	# This contains only the "interesting" defaults.
	# Ints and bools default to 0, floats to 0.0 and strings to "".
	#@-at
	#@@c
	
	defaultBodyFontSize = choose(sys.platform=="win32",9,12)
	
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
		"body_pane_wraps" : 1,
		"body_text_font_family" : "Courier",
		"body_text_font_size" : defaultBodyFontSize,
		"body_text_font_slant" : "roman",
		"body_text_font_weight" : "normal",
		"headline_text_font_size" : 12,
		"headline_text_font_slant" : "roman",
		"headline_text_font_weight" : "normal",
		"log_text_font_size" : 12,
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
	#@-node:<< define defaultsDict >>
	#@nl
	#@	@+others
	#@+node:config.__init__
	def __init__ (self):
		
		#@	<< get the default font >>
		#@+node:<< get the default font >>
		# Get the default font from a new text widget.
		# This should only be done once.
		
		t = Tkinter.Text()
		fn = t.cget("font")
		font = tkFont.Font(font=fn)
		self.defaultFont = font
		self.defaultFontFamily = font.cget("family")
		#@-node:<< get the default font >>
		#@nl
		self.init()
	
	def init (self):
	
		try:
			self.configDir = sys.leo_config_directory
		except:
			self.configDir = os.path.join(app().loadDir,"..","config")
		self.configFileName = os.path.join(self.configDir,"leoConfig.txt")
		self.configsExist = false # True when we successfully open leoConfig.txt.
		
		#@	<< initialize constant ivars, lists & dicts >>
		#@+node:<< initialize constant ivars, lists & dicts >> (leoConfig)
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
		self.keysDict = {}
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
		#@-node:<< initialize constant ivars, lists & dicts >> (leoConfig)
		#@nl
		#@	<< initialize ivars that may be set by config options >>
		#@+node:<< initialize ivars that may be set by config options >>
		# 10/11/02: Defaults are specified only here.
		
		self.config = None # The current instance of ConfigParser
		self.at_root_bodies_start_in_doc_mode = true # For compatibility with previous versions.
		self.output_initial_comment = "" # "" or None for compatibility with previous versions.
		self.output_newline = "nl"
		self.create_nonexistent_directories = false
		self.default_derived_file_encoding = "utf-8"
		self.load_derived_files_immediately = 0
		self.new_leo_file_encoding = "UTF-8" # Upper case for compatibility with previous versions.
		self.read_only = true # Make sure we don't alter an illegal leoConfig.txt file!
		self.relative_path_base_directory = "!"
		self.remove_sentinels_extension = ".txt"
		self.save_clears_undo_buffer = false
		self.stylesheet = None
		self.thin_at_file_trees = 0
		self.tkEncoding = None # Defaults to None so it doesn't override better defaults.
		self.use_plugins = false # Should never be true here!
		self.write_old_format_derived_files = true # Revert to old format if leoConfig.txt does not exist.
		#@nonl
		#@-node:<< initialize ivars that may be set by config options >>
		#@nl
	
		self.open() # read and process the configuration file.
	#@nonl
	#@-node:config.__init__
	#@+node:get...FromDict & setDict
	def getBoolFromDict (self,name,dict):
		val = self.getIntFromDict(name,dict)
		if val and val != None and val != 0: val = 1
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
		return val
	
	def getIntFromDict (self,name,dict):
		val = self.getFromDict(name,dict)
		if val:
			try: val = int(val)
			except: val = None
		return val
	
	def setDict (self,name,val,dict):
		dict [name] = val
			
	getStringFromDict = getFromDict
	#@-node:get...FromDict & setDict
	#@+node:get/setColors
	def getBoolColorsPref (self,name):
		return self.getBoolFromDict(name,self.colorsDict)
		
	# Basic getters and setters.
	
	def getColorsPref (self,name):
		return self.getFromDict(name,self.colorsDict)
	
	def setColorsPref (self,name,val):
		self.setDict(name,val,self.colorsDict)
		
	getStringColorsPref = getColorsPref
	#@nonl
	#@-node:get/setColors
	#@+node:get/setComparePref
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
	#@-node:get/setComparePref
	#@+node:get/setFindPref
	def getBoolFindPref (self,name):
		return self.getBoolFromDict(name,self.findDict)
	
	# Basic getters and setters.
	
	def getFindPref (self,name):
		return self.getFromDict(name,self.findDict)
	
	def setFindPref (self,name,val):
		self.setDict(name,val,self.findDict)
		
	getStringFindPref = getFindPref
	#@nonl
	#@-node:get/setFindPref
	#@+node:get/setPref
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
	#@-node:get/setPref
	#@+node:get/setRecentFiles
	def getRecentFiles (self):
		
		return self.recentFiles
	
	def setRecentFiles (self,files):
		
		self.recentFiles = files
	#@-node:get/setRecentFiles
	#@+node:get/setWindowPrefs
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
	#@-node:get/setWindowPrefs
	#@+node:config.getFontFromParams
	#@+at 
	#@nonl
	# A convenience method that computes a font from font parameters.
	# Arguments are the names of settings to be use.
	# We return None if there is no family setting so we can use system 
	# default fonts.
	# We default to size=12, slant="roman", weight="normal"
	#@-at
	#@@c
	
	def getFontFromParams(self,family,size,slant,weight):
		
		tag = "getFont..." ; family_name = family
	
		family = self.getWindowPref(family)
		if not family or family == "":
			# print tag,"using default"
			family = self.defaultFontFamily
			
		size = self.getIntWindowPref(size)
		if not size or size == 0: size = 12
		
		slant = self.getWindowPref(slant)
		if not slant or slant == "": slant = "roman"
		
		weight = self.getWindowPref(weight)
		if not weight or weight == "": weight = "normal"
		
		try:
			font = tkFont.Font(family=family,size=size,slant=slant,weight=weight)
		except:
			es("exception setting font from " + `family_name`)
			es("family,size,slant,weight:"+
				`family`+':'+`size`+':'+`slant`+':'+`weight`)
			es_exception()
			return self.defaultFont
		#print family_name,family,size,slant,weight
		#print "actual_name:",font.cget("family")
		return font
	#@nonl
	#@-node:config.getFontFromParams
	#@+node:getShortcut
	def getShortcut (self,name):
		
		val = self.keysDict.get(name)
		
		# 7/19/03: Return "None" if the setting is "None"
		# This allows settings to disable a default shortcut.
		return val
	#@nonl
	#@-node:getShortcut
	#@+node:init/Boolean/ConfigParam
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
	#@-node:init/Boolean/ConfigParam
	#@+node:setCommandsFindIvars
	# Sets ivars of c that can be overridden by leoConfig.txt
	
	def setCommandsFindIvars (self,c):
	
		config = self ; findFrame = app().findFrame
	
		# N.B.: separate c.ivars are much more convenient than a dict.
		for s in findFrame.intKeys:
			val = config.getBoolFindPref(s)
			if val: 
				setattr(c,s+"_flag",val)
				# trace(s+"_flag",val)
				
		val = config.getStringFindPref("change_string")
		if val: c.change_text = val
		
		val = config.getStringFindPref("find_string")
		if val: c.find_text = val
	
		app().findFrame.init(c)
	#@nonl
	#@-node:setCommandsFindIvars
	#@+node:setCommandsIvars
	# Sets ivars of c that can be overridden by leoConfig.txt
	
	def setCommandsIvars (self,c):
	
		config = self ; a = app()
		#@	<< set prefs ivars >>
		#@+node:<< set prefs ivars >>
		val = config.getIntPref("tab_width")
		if val:
			c.tab_width = val
			if 0: # 9/20/02: don't actually redraw.
				c.frame.setTabWidth(c.tab_width)
		
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
				if a.language_delims_dict.get(val):
					c.target_language = val
				
			except: pass
		#@nonl
		#@-node:<< set prefs ivars >>
		#@nl
	#@nonl
	#@-node:setCommandsIvars
	#@+node:setConfigFindIvars
	# Sets config ivars from c.
	
	def setConfigFindIvars (self,c):
		
		findFrame = app().findFrame
	
		# N.B.: separate c.ivars are much more convenient than a dict.
		for s in findFrame.intKeys:
			val = getattr(c,s+"_flag")
			# trace(val,s+"_flag")
			self.setFindPref(s,val)
		
		self.setFindPref("change_string",c.change_text)
		self.setFindPref("find_string",c.find_text)
	#@nonl
	#@-node:setConfigFindIvars
	#@+node:setConfigIvars
	# Sets config ivars from c.
	
	def setConfigIvars (self,c):
		
		a = app()
		
		
		if c.target_language and a.language_delims_dict.get(c.target_language):
			language = c.target_language
		else:
			language = "plain"
		self.setPref("default_tangle_directory",c.tangle_directory)
		self.setPref("default_target_language",language)
		self.setPref("output_doc_chunks",`c.output_doc_flag`)
		self.setPref("page_width",`c.page_width`)
		self.setPref("run_tangle_done.py",`c.tangle_batch_flag`)
		self.setPref("run_untangle_done.py",`c.untangle_batch_flag`)
		self.setPref("tab_width",`c.tab_width`)
		self.setPref("tangle_outputs_header",`c.use_header_flag`)
		
		self.setFindPref("batch",`c.batch_flag`)
		self.setFindPref("ignore_case",`c.ignore_case_flag`)
		self.setFindPref("mark_changes",`c.mark_changes_flag`)
		self.setFindPref("mark_finds",`c.mark_finds_flag`)
		self.setFindPref("pattern_match",`c.pattern_match_flag`)
		self.setFindPref("reverse",`c.reverse_flag`)
		self.setFindPref("search_body",`c.search_body_flag`)
		self.setFindPref("search_headline",`c.search_headline_flag`)
		self.setFindPref("suboutline_only",`c.suboutline_only_flag`)
		self.setFindPref("wrap",`c.wrap_flag`)
		self.setFindPref("whole_word",`c.whole_word_flag`)
		
		self.setFindPref("change_string",c.change_text)
		self.setFindPref("find_string",c.find_text)
	#@nonl
	#@-node:setConfigIvars
	#@+node:open
	def open (self):
		
		config = ConfigParser.ConfigParser()
		self.config = config
		try:
			cf = open(self.configFileName)
			config.readfp(cf)
			#@		<< get config options >>
			#@+node:<< get config options >>
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
				
			self.create_nonexistent_directories = self.initBooleanConfigParam(
				"create_nonexistent_directories",self.create_nonexistent_directories)
				
			encoding = self.initConfigParam(
				"default_derived_file_encoding",self.default_derived_file_encoding)
			
			if isValidEncoding(encoding):
				self.default_derived_file_encoding = encoding
			else:
				es("bad default_derived_file_encoding: " + encoding)
				
			self.load_derived_files_immediately = self.initBooleanConfigParam(
				"load_derived_files_immediately",self.load_derived_files_immediately)
				
			encoding = self.initConfigParam(
				"new_leo_file_encoding",
				self.new_leo_file_encoding)
			
			if isValidEncoding(encoding):
				self.new_leo_file_encoding = encoding
			else:
				es("bad new_leo_file_encoding: " + encoding)
			
			self.output_initial_comment = self.initConfigParam(
				"output_initial_comment",self.output_initial_comment)
			
			self.output_newline = self.initConfigParam(
				"output_newline",self.output_newline)
			
			self.read_only = self.initBooleanConfigParam(
				"read_only",self.read_only)
			
			self.relative_path_base_directory = self.initConfigParam(
				"relative_path_base_directory",self.relative_path_base_directory)
				
			self.remove_sentinels_extension = self.initConfigParam(
				"remove_sentinels_extension",self.remove_sentinels_extension)
			
			self.save_clears_undo_buffer = self.initBooleanConfigParam(
				"save_clears_undo_buffer",self.save_clears_undo_buffer)
				
			self.stylesheet = self.initConfigParam(
				"stylesheet",self.stylesheet)
				
			self.thin_at_file_trees = self.initBooleanConfigParam(
				"thin_at_file_trees",self.thin_at_file_trees)
				
			encoding = self.initConfigParam(
				"tk_encoding",self.tkEncoding)
				
			if encoding and len(encoding) > 0: # May be None.
				if isValidEncoding(encoding):
					self.tkEncoding = encoding
				else:
					es("bad tk_encoding: " + encoding)
				
			self.use_plugins = self.initBooleanConfigParam(
				"use_plugins",self.use_plugins)
				
			self.write_old_format_derived_files = self.initBooleanConfigParam(
				"write_old_format_derived_files",self.write_old_format_derived_files)
			#@nonl
			#@-node:<< get config options >>
			#@nl
			#@		<< get recent files >>
			#@+node:<< get recent files >>
			section = self.recentFilesSection
			
			if 0: # elegant, but may be a security hole.
				self.recentFiles = eval(config.get(section,"recentFiles",raw=1)) # 2/4/03
			else: # easier to read in the config file.
				try:
					for i in xrange(10):
						self.recentFiles.append(config.get(section,"file" + `i`,raw=1)) # 2/4/03
				except: pass
			#@nonl
			#@-node:<< get recent files >>
			#@nl
			for section, dict in self.sectionInfo:
				if dict != None:
					try:
						for opt in config.options(section):
							dict[string.lower(opt)]=config.get(section,opt,raw=1) # 2/4/03
					except: pass
			#@		<< convert find/change options to unicode >>
			#@+node:<< convert find/change options to unicode >>
			find = self.findDict.get("find_string")
			if find:
				# Leo always writes utf-8 encoding, but users may not.
				find = toUnicode(find,"utf-8")
				self.findDict["find_string"] = find
			
			change = self.findDict.get("change_string")
			if change:
				# Leo always writes utf-8 encoding, but users may not.
				change = toUnicode(change,"utf-8")
				self.findDict["change_string"] = change
			#@-node:<< convert find/change options to unicode >>
			#@nl
			#@		<< print options >>
			#@+node:<< print options >>
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
			#@-node:<< print options >>
			#@nl
			cf.close()
			self.configsExist = true
		except IOError:
			pass
		except:
			es("Exception opening " + self.configFileName)
			es_exception()
			pass
		self.config = None
	#@nonl
	#@-node:open
	#@+node:update (config)
	# Rewrites the entire config file from ivars.
	# This is called when a .leo file is written and when the preferences panel changes.
	
	def update (self):
		
		# Do nothing if the file does not exist, or if read_only.
		if self.read_only:
			# print "Read only config file"
			return
		if not os.path.exists(self.configFileName):
			# print "No config file"
			return
		
		config = ConfigParser.ConfigParser()
		self.config = config
		try:
			# 9/1/02: apparently Linux requires w+ and XP requires w.
			mode = choose(sys.platform=="win32","wb","wb+")
			cf = open(self.configFileName,mode)
			config.readfp(cf)
			#@		<< write recent files section >>
			#@+node:<< write recent files section >>
			section = self.recentFilesSection
			files = self.recentFiles
			
			if config.has_section(section):
				config.remove_section(section)
			config.add_section(section)
			
			if 0: # elegant, but may be a security hole.
				config.set(section,"recentFiles",files)
			else: # easier to read in the config file.
				for i in xrange(len(files)):
					config.set(section, "file"+`i`, files[i])
			#@nonl
			#@-node:<< write recent files section >>
			#@nl
			for section,dict in self.sectionInfo:
				if dict:
					self.update_section(config,section,dict)
			config.write(cf)
			cf.flush()
			cf.close()
		except:
			es("exception writing: " + self.configFileName)
			es_exception()
		self.config = None
	#@nonl
	#@-node:update (config)
	#@+node:update_section
	def update_section (self,config,section,dict):
		
		if config.has_section(section):
			config.remove_section(section)
		config.add_section(section)
		
		keys = dict.keys()
		keys.sort() # Not effective.
		for name in keys:
			val = dict [name]
			val = toEncodedString(val,"utf-8")
			config.set(section,name,val)
	#@-node:update_section
	#@-others
	
class config (baseConfig):
	"""A class to manage configuration settings."""
	pass
#@nonl
#@-node:@file leoConfig.py
#@-leo
