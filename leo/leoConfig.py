#@+leo

#@+node:0::@file leoConfig.py
#@+body
#@@language python

from leoGlobals import *
from leoUtils import *
import exceptions, os, string, sys, traceback, ConfigParser, tkFont

class config:
	
	#@<< define default tables for settings >>
	#@+node:1::<< define default tables for settings >>
	#@+body
	if 0:
		defaultConfigDict = {
			"path_directive_creates_directories" : 0,
			"read_only" : 1,
			"save_clears_undo_buffer" : 0,
			"xml_version_string" : "UTF-8" } # By default, we write leo.py 2.x files.
	
	defaultRecentFiles = {}
	for i in xrange(0,10):
		defaultRecentFiles ["file" + `i`] = None
		
	defaultCompareDict = {
		"append_output_to_output_file" : 0,
		"compare_file_1" : None,
		"compare_file_2" : None,
		"ignore_blank_lines" : 1,
		"ignore_first_line_of_file_1" : 0,
		"ignore_first_line_of_file_2" : 0,
		"ignore_interior_whitespace" : 0,
		"ignore_leading_whitespace" : 0,
		"ignore_sentinel_lines" : 0,
		"limit_count" : 9,
		"limit_directory_search_extension" : None,
		"make_whitespace_visible" : 0,
		"output_file" : None,
		"print_both_lines_for_matches" : 0,
		"print_matching_lines" : 0,
		"print_mismatching_lines" : 1,
		"print_trailing_lines" : 1 }
	
	defaultFindDict = {
		"change_string" : None,
		"find_string" : None,
		"batch" : 0,
		"ignore_case" : 0,
		"mark_changes" : 0,
		"mark_finds" : 0,
		"pattern_match" : 0,
		"reverse" : 0,
		"search_body" : 1,
		"search_headline" : 0,
		"suboutline_only" : 0,
		"whole_word" : 1,
		"wrap" : 0 }
	
	defaultPrefsDict = {
		"default_tangle_directory" : None,
		"default_target_language" : "Python",
		"tab_width" : 4,
		"page_width" : 132,
		"output_doc_chunks" : 1,
		"tangle_outputs_header" : 1,
		"run_tangle_done.py" : 0,
		"run_untangle_done.py" : 0 }
	
	defaultColorsDict = {
		"color_directives_in_plain_text" : 1,
		"underline_undefined_section_names" : 1,
		"use_hyperlinks" : 0,
		"comment_color" : "firebrick3",
		"cweb_section_name_color" : "red",
		"directive_color" : "blue",
		"doc_part_color" : "firebrick3",
		"keyword_color" : "blue",
		"leo_keyword_color" : "#00aa00",
		"section_name_color" : "red",
		"section_name_brackets_color" : "blue",
		"string_color" : "#00aa00",
		"undefined_section_name_color" : "red" }
		
	defaultBodyFontSize = choose(sys.platform=="win32",9,12)
	
	defaultWindowDict = {
		"body_cursor_foreground_color" : None,
		"body_cursor_background_color" : None,
		"additional_body_text_border" : 0,
		"body_pane_wraps" : 1,
		"body_text_font_family" : "Courier",
		"body_text_foreground_color": None,
		"body_text_background_color": None,
		"body_text_font_size" : defaultBodyFontSize,
		"body_text_font_slant" : "roman",
		"body_text_font_weight" : "normal",
		
		"headline_text_unselected_foreground_color" : None,
		"headline_text_unselected_background_color" : None,
		"headline_text_selected_foreground_color" : None,
		"headline_text_selected_background_color" : None,
		"headline_text_editing_foreground_color" : None,
		"headline_text_editing_background_color" : None,
		"headline_text_editing_selection_foreground_color" : None,
		"headline_text_editing_selection_background_color" : None,
		
		"headline_text_font_family" : None,
		"headline_text_font_size" : 12,
		"headline_text_font_slant" : "roman",
		"headline_text_font_weight" : "normal",
		"outline_pane_background_color" : None,
		"log_pane_wraps" : 0,
		"log_text_foreground_color": None,
		"log_text_background_color": None,
		"log_text_font_family" : None,
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
	#@-node:1::<< define default tables for settings >>

	
	#@<< Define names of settings >>
	#@+node:2::<< Define names of settings >>
	#@+body
	#@+at
	#  Used only by open.  Update just writes whatever is in the various dicts.
	# 
	# These tables seem redundant, and eliminating them would be hard:
	# 1. We need these various tables to indicate types.
	# 2. It won't be easy to split the dicts by type because the set routines 
	# use a single dict.

	#@-at
	#@@c
	
	if 0: # Not used in code.
		boolConfigNames = (
			"path_directive_creates_directories",
			"read_only",
			"save_clears_undo_buffer")
		stringConfigNames = ( "xml_version_string", )
	
	# Compare section
	boolCompareNames = (
		"append_output_to_output_file",
		"ignore_blank_lines",
		"ignore_first_line_of_file_1",
		"ignore_first_line_of_file_2",
		"ignore_interior_whitespace",
		"ignore_leading_whitespace",
		"ignore_sentinel_lines",
		"make_whitespace_visible",
		"print_both_lines_for_matches",
		"print_matching_lines",
		"print_mismatching_lines",
		"print_trailing_lines" )
	
	intCompareNames = ( "limit_count", )
	
	stringCompareNames = (
	"compare_file_1",
	"compare_file_2",
	"limit_directory_search_extension",
	"output_file" )
	
	# Find section...
	boolFindNames = (
	"batch",
	"ignore_case",
	"mark_changes",
	"mark_finds",
	"pattern_match",
	"reverse",
	"search_body",
	"search_headline",
	"suboutline_only",
	"whole_word", "wrap" )
	
	stringFindNames = (
	"change_string",
	"find_string" )
	
	if 0: # We get default shortcuts from the menu code.
		stringKeysNames = ()
	
	# Prefs section...
	boolPrefsNames = (
	"output_doc_chunks",
	"run_tangle_done.py",
	"run_untangle_done.py",
	"tangle_outputs_header" )
	
	intPrefsNames = (
	"page_width",
	"tab_width" )
	
	stringPrefsNames = (
	"default_tangle_directory",
	"default_target_language" )
	
	# Syntax coloring section...
	boolColoringNames = (
	"color_directives_in_plain_text",
	"underline_undefined_section_names",
	"use_hyperlinks" )
	
	stringColoringNames = (
	# Tk color values also allowed.
	"comment_color",
	"cweb_section_name_color",
	"directive_color",
	"doc_part_color",
	"keyword_color",
	"leo_keyword_color",
	"section_name_color",
	"section_name_brackets_color",
	"string_color",
	"undefined_section_name_color" )
	
	# Window section...
	boolWindowNames = (
	"body_pane_wraps",
	"log_pane_wraps",
	"outline_pane_scrolls_horizontally")
	
	intWindowNames = (
	"additional_body_text_border",
	"body_text_font_size",
	"headline_text_font_size",
	"log_text_font_size" )
	
	floatWindowNames = (
	"initial_horizontal_ratio",
	"initial_horizontal_secondary_ratio",
	"initial_vertical_ratio",
	"initial_vertical_secondary_ratio")
	
	stringWindowNames = (
	"body_cursor_foreground_color",
	"body_cursor_background_color",
	"body_text_foreground_color",
	"body_text_background_color",
	"body_text_font_family",
	"body_text_font_slant",
	"body_text_font_weight",
	
	"headline_text_unselected_foreground_color",
	"headline_text_unselected_background_color",
	"headline_text_selected_foreground_color",
	"headline_text_selected_background_color",
	"headline_text_editing_foreground_color",
	"headline_text_editing_background_color",
	"headline_text_editing_selection_foreground_color",
	"headline_text_editing_selection_background_color",
	
	"headline_text_font_family",
	"headline_text_font_slant",
	"headline_text_font_weight",
	
	"initial_splitter_orientation", # "horizontal" or "vertical"
	"initial_window_height",
	"initial_window_left",
	"initial_window_top",
	"initial_window_width",
	
	"log_text_foreground_color",
	"log_text_background_color",
	"log_text_font_family",
	"log_text_font_slant",
	"log_text_font_weight",
	
	"outline_pane_background_color",
	
	"split_bar_color",
	"split_bar_relief",
	"split_bar_width" )
	#@-body
	#@-node:2::<< Define names of settings >>


	#@+others
	#@+node:3::config.__init__
	#@+body
	def __init__ (self):
		
		# Files and directories.
		try:
			self.configDir = sys.leo_config_directory
		except:
			self.configDir = app().loadDir
		self.configFileName = os.path.join(self.configDir,"leoConfig.txt")
		
		#@<< initialize constant ivars >>
		#@+node:1::<< initialize constant ivars >>
		#@+body
		# Language names.
		self.languageNameDict = {
			c_language: "C",
			cweb_language: "CWEB",
			html_language: "HTML",
			java_language: "Java",
			pascal_language: "Pascal",
			perl_language: "Perl",
			perlpod_language: "PerlPod",
			plain_text_language: "Plain",
			python_language: "Python",
			tcltk_language: "tcl/tk",
			php_language: "php" } # 08-SEP-2002 DTHEIN
		
		# Names of sections.
		self.configSection = "config options"
		self.compareSection = "compare options"
		self.findSection = "find/change options"
		self.keysSection = "keyboard shortcuts"
		self.prefsSection = "prefs panel options"
		self.recentFilesSection = "recent files"
		self.colorsSection = "syntax coloring options"
		self.windowSection = "window options"
		#@-body
		#@-node:1::<< initialize constant ivars >>

	
		# Initialize settings in each section.
		self.configsExist = false # True when we successfully open leoConfig.txt.
		self.config = None # The current instance of ConfigParser
		self.read_only = true # Make _sure_ we don't alter an illegal leoConfig.txt file!
		self.path_directive_creates_directories = false
		self.relative_path_base_directory = "!"
		self.save_clears_undo_buffer = false
		self.use_relative_node_indices = 1
		self.write_clone_indices = 0
		self.xml_version_string = None
		self.compareDict = {}
		self.findDict = {}
		self.keysDict = {}
		self.prefsDict = {}
		self.recentFiles = []
		self.colorsDict = {}
		self.windowDict = {}
	
		# Initialize the ivars from the config file.
		self.open()
	#@-body
	#@-node:3::config.__init__
	#@+node:4::get...FromDict & setDict
	#@+body
	def getBoolFromDict (self,name,dict,defaultDict):
		val = self.getIntFromDict(name,dict,defaultDict)
		if val and val != None and val != 0: val = 1
		return val
	
	def getFloatFromDict (self,name,dict,defaultDict):
		val = self.getFromDict(name,dict,defaultDict)
		if val:
			try: val = float(val)
			except: val = None
		return val
	
	def getFromDict (self,name,dict,defaultDict):
		if name in dict.keys(): # Python 2.1 support.
			val = dict[name]
			if val == "ignore":
				val = None
			return val
		elif defaultDict and name in defaultDict.keys(): # Python 2.1 support.
			val = defaultDict[name]
			if val == "ignore":
				val = None
			return val
		else:
			return None
	
	def getIntFromDict (self,name,dict,defaultDict):
		val = self.getFromDict(name,dict,defaultDict)
		if val:
			try: val = int(val)
			except: val = None
		return val
	
	def setDict (self,name,val,dict):
	
		# print `name`, `val`
		dict [name] = val
			
	getStringFromDict = getFromDict
	#@-body
	#@-node:4::get...FromDict & setDict
	#@+node:5::get/setColors
	#@+body
	def getBoolColorsPref (self,name):
		return self.getBoolFromDict(name,self.colorsDict,self.defaultColorsDict)
		
	# Basic getters and setters.
	
	def getColorsPref (self,name):
		return self.getFromDict(name,self.colorsDict,self.defaultColorsDict)
	
	def setColorsPref (self,name,val):
		self.setDict(name,val,self.colorsDict)
		
	getStringColorsPref = getColorsPref
	#@-body
	#@-node:5::get/setColors
	#@+node:6::get/setComparePref
	#@+body
	def getBoolComparePref (self,name):
		return self.getBoolFromDict(name,self.compareDict,self.defaultCompareDict)
		
	def getIntComparePref (self,name):
		return self.getIntFromDict(name,self.compareDict,self.defaultCompareDict)
	
	# Basic getters and setters.
	
	def getComparePref (self,name):
		return self.getFromDict(name,self.compareDict,self.defaultCompareDict)
	
	def setComparePref (self,name,val):
		self.setDict(name,val,self.compareDict)
		
	getStringComparePref = getComparePref
	#@-body
	#@-node:6::get/setComparePref
	#@+node:7::get/setFindPref
	#@+body
	def getBoolFindPref (self,name):
		return self.getBoolFromDict(name,self.findDict,self.defaultFindDict)
	
	# Basic getters and setters.
	
	def getFindPref (self,name):
		return self.getFromDict(name,self.findDict,self.defaultFindDict)
	
	def setFindPref (self,name,val):
		self.setDict(name,val,self.findDict)
		
	getStringFindPref = getFindPref
	#@-body
	#@-node:7::get/setFindPref
	#@+node:8::get/setPref
	#@+body
	def getBoolPref (self,name):
		return self.getBoolFromDict(name,self.prefsDict,self.defaultPrefsDict)
	
	def getIntPref (self,name):
		return self.getIntFromDict(name,self.prefsDict,self.defaultPrefsDict)
		
	# Basic getters and setters.
	
	def getPref (self,name):
		return self.getFromDict(name,self.prefsDict,self.defaultPrefsDict)
	
	def setPref (self,name,val):
		self.setDict(name,val,self.prefsDict)
		
	getStringPref = getPref
	#@-body
	#@-node:8::get/setPref
	#@+node:9::get/setRecentFiles
	#@+body
	def getRecentFiles (self):
		
		return self.recentFiles
	
	def setRecentFiles (self,files):
		
		self.recentFiles = files

	#@-body
	#@-node:9::get/setRecentFiles
	#@+node:10::get/setWindowPrefs
	#@+body
	def getBoolWindowPref (self,name):
		return self.getBoolFromDict(name,self.windowDict,self.defaultWindowDict)
		
	def getFloatWindowPref (self,name):
		return self.getFloatFromDict(name,self.windowDict,self.defaultWindowDict)
		
	def getIntWindowPref (self,name):
		return self.getIntFromDict(name,self.windowDict,self.defaultWindowDict)
		
	# Basic getters and setters.
	
	def getWindowPref (self,name):
		return self.getFromDict(name,self.windowDict,self.defaultWindowDict)
	
	def setWindowPref (self,name,val):
		#print "setWindowPref:", `name`, `val`
		self.setDict(name,val,self.windowDict)
		
	getStringWindowPref = getWindowPref
	#@-body
	#@-node:10::get/setWindowPrefs
	#@+node:11::getFontFromParams
	#@+body
	# A convenience method that computes a font from font parameters.
	# Arguments are the names of settings to be use.
	# We return None if there is no family setting so we can use system default fonts.
	# We default to size=12, slant="roman", weight="normal"
	
	def getFontFromParams(self,family,size,slant,weight):
		
		family = self.getWindowPref(family)
		# print `family`
		if not family:
			return None
		
		size = self.getIntWindowPref(size)
		# print `size`
		if size == None: size = 12
		
		slant = self.getWindowPref(slant)
		# print `slant`
		if not slant: slant = "roman"
		
		weight = self.getWindowPref(weight)
		# print `weight`
		if not weight: weight = "normal"
		
		font = tkFont.Font(family=family,size=size,slant=slant,weight=weight)
		return font
	

	#@-body
	#@-node:11::getFontFromParams
	#@+node:12::getShortcut
	#@+body
	# This code is simple because only the caller knows about defaults.
	
	def getShortcut (self,name):
		
		if self.keysDict.has_key(name):
			val = self.keysDict[name]
			if val == "None":
				return None
			else:
				return val
		else:
			return None

	#@-body
	#@-node:12::getShortcut
	#@+node:13::open
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
			try: self.path_directive_creates_directories = config.get(
				self.configSection, "path_directive_creates_directories")
			except: self.path_directive_creates_directories = false
			
			try: self.read_only = config.getboolean(
				self.configSection,"read_only")
			except: self.read_only = false
			
			try: self.relative_path_base_directory = config.get(
				self.configSection,"relative_path_base_directory")
			except: self.relative_path_base_directory = "!"
				
			try: self.save_clears_undo_buffer = config.getboolean(
				self.configSection,"save_clears_undo_buffer")
			except: self.save_clears_undo_buffer = false
				
			try:self.xml_version_string = config.get(
				self.configSection,"xml_version_string")
			except: self.xml_version_string = prolog_version_string
			
			try: self.use_relative_node_indices = config.getboolean(
				self.configSection,"use_relative_node_indices")
			except: self.use_relative_node_indices = 1
			
			try: self.write_clone_indices = config.getboolean(
				self.configSection,"write_clone_indices")
			except: self.write_clone_indices = 0

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

			
			#@<< get compare prefs >>
			#@+node:3::<< get compare prefs >>
			#@+body
			section = self.compareSection
			dict = self.compareDict
			
			self.setAllDicts(dict,section,
				bools=self.boolCompareNames,
				ints=self.intCompareNames,
				strings=self.stringCompareNames)

			#@-body
			#@-node:3::<< get compare prefs >>

			
			#@<< get keyboard shortcut prefs >>
			#@+node:6::<< get keyboard shortcut prefs >>
			#@+body
			#@+at
			#  Just put all user values in dict.
			# 
			# The menu code knows the defaults, so nothing more needs to be 
			# done here.

			#@-at
			#@@c
			
			section = self.keysSection
			dict = self.keysDict
			config = self.config
			assert(config)
			
			try: # The section may not exist.
				for name in config.options(section):
					try: # The user may have made a syntax error.
						dict[name] = config.get(section,name)
					except: pass
			except: pass

			#@-body
			#@-node:6::<< get keyboard shortcut prefs >>

			
			#@<< get prefs >>
			#@+node:4::<< get prefs >>
			#@+body
			section = self.prefsSection
			dict = self.prefsDict
			
			self.setAllDicts(dict,section,
				bools=self.boolPrefsNames,
				ints=self.intPrefsNames,
				strings=self.stringPrefsNames)

			#@-body
			#@-node:4::<< get prefs >>

			
			#@<< get find prefs >>
			#@+node:5::<< get find prefs >>
			#@+body
			section = self.findSection
			dict = self.findDict
			
			self.setAllDicts(dict,section,
				bools=self.boolFindNames,
				strings=self.stringFindNames)

			#@-body
			#@-node:5::<< get find prefs >>

			
			#@<< get syntax coloring prefs >>
			#@+node:7::<< get syntax coloring prefs >>
			#@+body
			section = self.colorsSection
			dict = self.colorsDict
			
			self.setAllDicts(dict,section,
				bools=self.boolColoringNames,
				strings=self.stringColoringNames)
			#@-body
			#@-node:7::<< get syntax coloring prefs >>

			
			#@<< get window prefs >>
			#@+node:8::<< get window prefs >>
			#@+body
			section = self.windowSection
			dict = self.windowDict
			
			self.setAllDicts(dict,section,
				bools=self.boolWindowNames,
				floats=self.floatWindowNames,
				ints=self.intWindowNames,
				strings=self.stringWindowNames)
			#@-body
			#@-node:8::<< get window prefs >>

			# print `self.recentFiles`
			if 0:
				print "\n\ncolorsDict:\n\n" + `self.colorsDict`
				print "\n\ncompareDict:\n\n"+ `self.compareDict`
				print "\n\nfindDict:\n\n"   + `self.findDict` 
				print "\n\nprefsDict:\n\n"  + `self.prefsDict`
				print "\n\nwindowDict:\n\n" + `self.windowDict`
			if 0:
				print "\n\nkeysDict:\n\n"
				for i in self.keysDict.items():
					print `i`
			if 0:
				print "\n\nwindowDict:\n\n"
				for i in self.windowDict.keys():
					print i
			cf.close()
			self.configsExist = true
		except exceptions.IOError:
			pass
		except:
			es("Exception opening " + self.configFileName)
			traceback.print_exc()
			pass
		self.config = None
	#@-body
	#@-node:13::open
	#@+node:14::setAllDicts
	#@+body
	def setAllDicts (self, dict, section,
		bools=(),floats=(),ints=(),strings=()):
			
		config = self.config
		assert(config)
			
		for name in bools:
			try: dict[name] = config.getboolean(section,name)
			except: pass
		for name in ints:
			try: dict[name] = config.getint(section,name)
			except: pass
		for name in floats:
			try: dict[name] = config.getfloat(section,name)
			except: pass
		for name in strings:
			try: dict[name] = config.get(section,name)
			except: pass
			
		# print "setAllDicts:" + `dict`
	#@-body
	#@-node:14::setAllDicts
	#@+node:15::setCommandsFindIvars
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
	#@-node:15::setCommandsFindIvars
	#@+node:16::setCommandsIvars
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
		
		c.target_language = python_language # default
		val = config.getPref("default_target_language")
		if val:
			try:
				val = string.lower(val)
				for language,name in self.languageNameDict.items():
					# print `language`, `name`
					if string.lower(name) == val:
						c.target_language = language
			except: pass
		#@-body
		#@-node:1::<< set prefs ivars >>
	#@-body
	#@-node:16::setCommandsIvars
	#@+node:17::setConfigFindIvars
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
	#@-node:17::setConfigFindIvars
	#@+node:18::setConfigIvars
	#@+body
	# Sets config ivars from c.
	
	def setConfigIvars (self,c):
		
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
	#@-node:18::setConfigIvars
	#@+node:19::update (config)
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
				
				#@<< write config section >>
				#@+node:1::<< write config section >>
				#@+body
				section = self.configSection
				
				if config.has_section(section):
					config.remove_section(section)
				config.add_section(section)
				
				config.set(section,"read_only",self.read_only)
				config.set(section,"save_clears_undo_buffer",self.save_clears_undo_buffer)
				config.set(section,"xml_version_string",self.xml_version_string)

				#@-body
				#@-node:1::<< write config section >>

				
				#@<< write recent files section >>
				#@+node:2::<< write recent files section >>
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
				#@-node:2::<< write recent files section >>

				
				#@<< write prefs section >>
				#@+node:3::<< write prefs section >>
				#@+body
				self.update_section(config,self.prefsSection,self.prefsDict)
				#@-body
				#@-node:3::<< write prefs section >>

				self.update_section(config,
					self.compareSection,self.compareDict)
				self.update_section(config,
					self.findSection,self.findDict)
				self.update_section(config,
					self.colorsSection,self.colorsDict)
				self.update_section(config,
					self.keysSection,self.keysDict)
				self.update_section(config,
					self.windowSection,self.windowDict)
				config.write(cf)
				cf.flush()
				cf.close()
			else:
				es("can not open: " + self.configFileName)
		except:
			es("exception writing: " + self.configFileName)
			traceback.print_exc()
		self.config = None
	#@-body
	#@-node:19::update (config)
	#@+node:20::update_section
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
	#@-node:20::update_section
	#@-others
#@-body
#@-node:0::@file leoConfig.py
#@-leo
