#@+leo
#@+node:0::@file leoConfig.py
#@+body
#@@language python

from leoGlobals import *
import exceptions, os, string, sys, traceback, ConfigParser, tkFont

class config:
	
	#@<< define defaultsDict >>
	#@+node:1::<< define defaultsDict >>
	#@+body
	#@+at
	#  This contains only the "interesting" defaults.
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
		"initial_window_height" : 20, # In grid units.  These are just a guess.
		"initial_window_width" :  60,
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
	#@-body
	#@-node:1::<< define defaultsDict >>


	#@+others
	#@+node:2::config.__init__
	#@+body
	def __init__ (self):
		
		
		#@<< get the default font >>
		#@+node:1::<< get the default font >>
		#@+body
		# Get the default font from a new text widget.
		# This should only be done once.
		
		t = Tkinter.Text()
		fn = t.cget("font")
		font = tkFont.Font(font=fn)
		self.defaultFont = font
		self.defaultFontFamily = font.cget("family")
		
		#@-body
		#@-node:1::<< get the default font >>

		self.init()
	
	def init (self):
	
		try:
			self.configDir = sys.leo_config_directory
		except:
			self.configDir = app().loadDir
		self.configFileName = os.path.join(self.configDir,"leoConfig.txt")
		self.configsExist = false # True when we successfully open leoConfig.txt.
		
		
		#@<< initialize constant ivars, lists & dicts >>
		#@+node:2::<< initialize constant ivars, lists & dicts >> (leoConfig)
		#@+body
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
		#@-body
		#@-node:2::<< initialize constant ivars, lists & dicts >> (leoConfig)

		
		#@<< initialize ivars that may be set by config options >>
		#@+node:3::<< initialize ivars that may be set by config options >>
		#@+body
		# 10/11/02: Defaults are specified only here.
		
		self.config = None
			# The current instance of ConfigParser
		self.output_initial_comment = ""
			# Must be "" or None for compatibility with older versions of Leo.
		self.output_newline = "nl"
		self.create_nonexistent_directories = false
		self.read_only = true
			# Make _sure_ we don't alter an illegal leoConfig.txt file!
		self.relative_path_base_directory = "!"
		self.remove_sentinels_extension = ".txt"
		self.save_clears_undo_buffer = false
		self.stylesheet = None
		self.use_relative_node_indices = 1
		self.write_clone_indices = 0
		self.xml_version_string = "UTF-8"
			# Must be upper case for compatibility with older versions of Leo.
		
		#@-body
		#@-node:3::<< initialize ivars that may be set by config options >>

	
		self.open() # read and process the configuration file.
	#@-body
	#@-node:2::config.__init__
	#@+node:3::getters/setters
	#@+node:1::get...FromDict & setDict
	#@+body
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
	
	#@-body
	#@-node:1::get...FromDict & setDict
	#@+node:2::get/setColors
	#@+body
	def getBoolColorsPref (self,name):
		return self.getBoolFromDict(name,self.colorsDict)
		
	# Basic getters and setters.
	
	def getColorsPref (self,name):
		return self.getFromDict(name,self.colorsDict)
	
	def setColorsPref (self,name,val):
		self.setDict(name,val,self.colorsDict)
		
	getStringColorsPref = getColorsPref
	#@-body
	#@-node:2::get/setColors
	#@+node:3::get/setComparePref
	#@+body
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
	#@-body
	#@-node:3::get/setComparePref
	#@+node:4::get/setFindPref
	#@+body
	def getBoolFindPref (self,name):
		return self.getBoolFromDict(name,self.findDict)
	
	# Basic getters and setters.
	
	def getFindPref (self,name):
		return self.getFromDict(name,self.findDict)
	
	def setFindPref (self,name,val):
		self.setDict(name,val,self.findDict)
		
	getStringFindPref = getFindPref
	#@-body
	#@-node:4::get/setFindPref
	#@+node:5::get/setPref
	#@+body
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
	#@-body
	#@-node:5::get/setPref
	#@+node:6::get/setRecentFiles
	#@+body
	def getRecentFiles (self):
		
		return self.recentFiles
	
	def setRecentFiles (self,files):
		
		self.recentFiles = files
	
	#@-body
	#@-node:6::get/setRecentFiles
	#@+node:7::get/setWindowPrefs
	#@+body
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
	#@-body
	#@-node:7::get/setWindowPrefs
	#@+node:8::config.getFontFromParams
	#@+body
	#@+at
	#  A convenience method that computes a font from font parameters.
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
		#print `family_name`,`family`,`size`,`slant`,`weight`
		#print "actual_name:",`font.cget("family")`
		return font
	#@-body
	#@-node:8::config.getFontFromParams
	#@+node:9::getShortcut
	#@+body
	def getShortcut (self,name):
		
		val = self.keysDict.get(name)
		if val == "None":
			return None
		else:
			return val
	#@-body
	#@-node:9::getShortcut
	#@+node:10::init/Boolean/ConfigParam
	#@+body
	def initConfigParam (self,name,defaultVal):
		try:
			val = self.config.get(self.configSection,name)
		except:
			val = defaultVal
		return val
	
	def initBooleanConfigParam (self,name,defaultVal):
		try:
			val = self.config.getboolean(self.configSection,name)
		except:
			val = defaultVal
		return val
	
	#@-body
	#@-node:10::init/Boolean/ConfigParam
	#@+node:11::setCommandsFindIvars
	#@+body
	# Sets ivars of c that can be overridden by leoConfig.txt
	
	def setCommandsFindIvars (self,c):
	
		# print "setCommandsFindIvars"
		config = self
		
		#@<< set find ivars >>
		#@+node:1::<< set find ivars >>
		#@+body
		val = config.getBoolFindPref("batch")
		if val: c.batch_flag = val
		
		val = config.getBoolFindPref("wrap")
		if val: c.wrap_flag = val
		
		val = config.getBoolFindPref("whole_word")
		if val: c.whole_word_flag = val
		
		val = config.getBoolFindPref("ignore_case")
		if val: c.ignore_case_flag = val
		
		val = config.getBoolFindPref("pattern_match")
		if val: c.pattern_match_flag = val
		
		val = config.getBoolFindPref("search_headline")
		if val: c.search_headline_flag = val
		
		val = config.getBoolFindPref("search_body")
		if val: c.search_body_flag = val
		
		val = config.getBoolFindPref("suboutline_only")
		if val: c.suboutline_only_flag = val
		
		val = config.getBoolFindPref("mark_changes")
		if val: c.mark_changes_flag = val
		
		val = config.getBoolFindPref("mark_finds")
		if val: c.mark_finds_flag = val
		
		val = config.getBoolFindPref("reverse")
		if val: c.reverse_flag = val
		
		val = config.getStringFindPref("change_string")
		if val: c.change_text = val
		
		val = config.getStringFindPref("find_string")
		if val: c.find_text = val
		#@-body
		#@-node:1::<< set find ivars >>

		app().findFrame.init(c)
	#@-body
	#@-node:11::setCommandsFindIvars
	#@+node:12::setCommandsIvars
	#@+body
	# Sets ivars of c that can be overridden by leoConfig.txt
	
	def setCommandsIvars (self,c):
	
		config = self
		
		#@<< set prefs ivars >>
		#@+node:1::<< set prefs ivars >>
		#@+body
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
				if 1: # new
					val = string.replace(val,"/","")
					if language_delims_dict.get(val):
						c.target_language = val
				else: #old
					for language,name in self.languageNameDict.items():
						# print `language`, `name`
						if string.lower(name) == val:
							c.target_language = language
			except: pass
		#@-body
		#@-node:1::<< set prefs ivars >>
	#@-body
	#@-node:12::setCommandsIvars
	#@+node:13::setConfigFindIvars
	#@+body
	# Sets config ivars from c.
	
	def setConfigFindIvars (self,c):
		
		# print "setConfigFindIvars"
	
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
	
	#@-body
	#@-node:13::setConfigFindIvars
	#@+node:14::setConfigIvars
	#@+body
	# Sets config ivars from c.
	
	def setConfigIvars (self,c):
		
		if 1: # new 
			if c.target_language and language_delims_dict.get(c.target_language):
				language = c.target_language
			else:
				language = "plain"
		else: # old ???? what does this do ???????
			if c.target_language and c.target_language in self.languageNameDict.keys():
				language = self.languageNameDict[c.target_language]
			else:
				language = "Plain"
	
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
	#@-body
	#@-node:14::setConfigIvars
	#@-node:3::getters/setters
	#@+node:4::open
	#@+body
	def open (self):
		
		config = ConfigParser.ConfigParser()
		self.config = config
		try:
			cf = open(self.configFileName)
			config.readfp(cf)
			
			#@<< get config options >>
			#@+node:1::<< get config options >>
			#@+body
			#@+at
			#  Rewritten 10/11/02 as follows:
			# 
			# 1. We call initConfigParam and initBooleanConfigParam to get the values.
			# 
			# The general purpose code will enter all these values into 
			# configDict.  This allows update() to write the configuration 
			# section without special case code.  configDict is not accessible 
			# by the user.  Rather, for greater speed the user access these 
			# values via the ivars of this class.
			# 
			# 2. We pass the ivars themselves as params so that default 
			# initialization is done in the ctor, as would normally be expected.

			#@-at
			#@@c

			self.output_initial_comment = self.initConfigParam(
				"output_initial_comment",
				self.output_initial_comment)
			
			self.output_newline = self.initConfigParam(
				"output_newline",self.output_newline)
			
			self.create_nonexistent_directories = self.initBooleanConfigParam(
				"create_nonexistent_directories",
				self.create_nonexistent_directories)
			
			self.read_only = self.initBooleanConfigParam(
				"read_only",self.read_only)
			
			self.relative_path_base_directory = self.initConfigParam(
				"relative_path_base_directory",
				self.relative_path_base_directory)
			
			self.save_clears_undo_buffer = self.initBooleanConfigParam(
				"save_clears_undo_buffer",
				self.save_clears_undo_buffer)
				
			self.stylesheet = self.initConfigParam(
				"stylesheet",
				self.stylesheet)
			
			self.xml_version_string = self.initConfigParam(
				"xml_version_string",
				self.xml_version_string)
			
			self.use_relative_node_indices = self.initBooleanConfigParam(
				"use_relative_node_indices",
				self.use_relative_node_indices)
			
			self.remove_sentinels_extension = self.initConfigParam(
				"remove_sentinels_extension",
				self.remove_sentinels_extension)
			
			self.write_clone_indices = self.initBooleanConfigParam(
				"write_clone_indices",
				self.write_clone_indices)
			
			#@-body
			#@-node:1::<< get config options >>

			
			#@<< get recent files >>
			#@+node:2::<< get recent files >>
			#@+body
			section = self.recentFilesSection
			
			if 0: # elegant, but may be a security hole.
				self.recentFiles = eval(config.get(section, "recentFiles"))
			else: # easier to read in the config file.
				try:
					for i in xrange(10):
						self.recentFiles.append(config.get(section, "file" + `i`))
				except: pass
			#@-body
			#@-node:2::<< get recent files >>

			for section, dict in self.sectionInfo:
				if dict != None:
					for opt in config.options(section):
						dict[string.lower(opt)]=config.get(section,opt)
			
			#@<< print options >>
			#@+node:3::<< print options >>
			#@+body
			# print `self.recentFiles`
			if 0:
				print "\n\ncolorsDict:\n\n" + `self.colorsDict`
				print "\n\ncompareDict:\n\n"+ `self.compareDict`
				print "\n\nfindDict:\n\n"   + `self.findDict` 
				print "\n\nprefsDict:\n\n"  + `self.prefsDict`
			if 0:
				print "\n\nwindowDict:\n\n" + `self.windowDict`
			if 0:
				print "\n\nkeysDict:\n\n"
				for i in self.keysDict.items():
					print `i`
			if 0:
				print "\n\nwindowDict:\n\n"
				for i in self.windowDict.keys():
					print i
			#@-body
			#@-node:3::<< print options >>

			cf.close()
			self.configsExist = true
		except exceptions.IOError:
			pass
		except:
			es("Exception opening " + self.configFileName)
			es_exception()
			pass
		self.config = None
	#@-body
	#@-node:4::open
	#@+node:5::update (config)
	#@+body
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
			if cf:
				config.readfp(cf)
				
				#@<< write recent files section >>
				#@+node:1::<< write recent files section >>
				#@+body
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
				#@-body
				#@-node:1::<< write recent files section >>

				for section,dict in self.sectionInfo:
					if dict:
						self.update_section(config,section,dict)
				config.write(cf)
				cf.flush()
				cf.close()
			else:
				es("can not open: " + self.configFileName)
		except:
			es("exception writing: " + self.configFileName)
			es_exception()
		self.config = None
	#@-body
	#@-node:5::update (config)
	#@+node:6::update_section
	#@+body
	def update_section (self,config,section,dict):
		
		if config.has_section(section):
			config.remove_section(section)
		config.add_section(section)
		
		keys = dict.keys()
		keys.sort() # Not effective.
		for name in keys:
			val = dict [name]
			config.set(section,name,val)
	#@-body
	#@-node:6::update_section
	#@-others
#@-body
#@-node:0::@file leoConfig.py
#@-leo
