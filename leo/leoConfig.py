#@+leo

#@+node:0::@file leoConfig.py
#@+body
#@@language python

from leoGlobals import *
from leoUtils import *
import os, sys, traceback, ConfigParser

class config:

	#@+others
	#@+node:1:C=1:config.__init__
	#@+body
	def __init__ (self):
		
		# Files and directories.
		try:
			self.configDir = sys.leo_config_directory
		except:
			self.configDir = app().loadDir
		self.configFileName = os.path.join(self.configDir,"leoConfig.txt")
		
		#@<< define constants >>
		#@+node:1::<< define constants >>
		#@+body
		# Language names.
		self.languageNameDict = {
			c_language: "C", cweb_language: "CWEB",
			html_language: "HTML", java_language: "Java",
			pascal_language: "Pascal", perl_language: "Perl",
			perlpod_language: "PerlPod", plain_text_language: "Plain",
			python_language: "Python" }
		# Names of sections.
		self.configSection = "config options"
		self.findSection = "find/change prefs"
		self.fontSection = "font prefs"
		self.prefsSection = "prefs panel"
		self.recentFilesSection = "recent files"
		self.syntaxColoringSection = "syntax coloring prefs"
		#@-body
		#@-node:1::<< define constants >>

		# Settings in each section.
		self.read_only = false
		self.xml_version_string = None
		self.findDict = {}
		self.fontDict = {}
		self.prefsDict = {}
		self.recentFiles = []
		self.syntaxColoringDict = {}
		# Initialize the ivars from the config file.
		self.open()
	#@-body
	#@-node:1:C=1:config.__init__
	#@+node:2::get/setFindPref
	#@+body
	# We don't read or write keys whose value is "ignore"
	
	def getIntFindPref (self,name):
		val = self.getFindPref(name)
		if val:
			try: val = int(val)
			except: val = None
		return val
	
	def getFindPref (self,name):
	
		if name in self.findDict:
			val = self.findDict[name]
			if val == "ignore":
				val = None
			# print "get",`name`,`val`
			return val
		else:
			return None
	
	def setFindPref (self,name,val):
	
		# print "set",`name`, `val`
		if name in self.findDict:
			old_val = self.findDict[name]
			if old_val != "ignore":
				self.findDict [name] = val
		else:
			self.findDict [name] = val
	#@-body
	#@-node:2::get/setFindPref
	#@+node:3::get/setFont (todo)
	#@+body
	def getFont (self, fontDict):
		
		pass
		
	def setFont (self):
		
		pass
	#@-body
	#@-node:3::get/setFont (todo)
	#@+node:4::get/setPref
	#@+body
	# We don't read or write keys whose value is "ignore"
	
	def getIntPref (self,name):
		val = self.getPref(name)
		if val:
			try: val = int(val)
			except: val = None
		return val
	
	def getPref (self,name):
	
		if name in self.prefsDict:
			val = self.prefsDict[name]
			if val == "ignore":
				val = None
			return val
		else:
			return None
	
	def setPref (self,name,val):
	
		# print `name`, `val`
		if name in self.prefsDict:
			old_val = self.prefsDict[name]
			if old_val != "ignore":
				self.prefsDict [name] = val
		else:
			self.prefsDict [name] = val
	#@-body
	#@-node:4::get/setPref
	#@+node:5:C=2:get/setRecentFiles
	#@+body
	def getRecentFiles (self):
		
		return self.recentFiles
	
	def setRecentFiles (self,files):
		
		self.recentFiles = files

	#@-body
	#@-node:5:C=2:get/setRecentFiles
	#@+node:6::get/setSyntaxColors (todo)
	#@+body
	def getSyntaxColors (self):
		
		pass
		
	def setSyntaxColors (self, colorsDict):
		
		pass
	#@-body
	#@-node:6::get/setSyntaxColors (todo)
	#@+node:7::open
	#@+body
	def open (self):
		
		config = ConfigParser.ConfigParser()
		try:
			cf = open(self.configFileName)
			config.readfp(cf)
			
			#@<< get config options >>
			#@+node:1::<< get config options >>
			#@+body
			try:
				self.read_only = config.getboolean(self.configSection, "read_only")
			except:
				self.read_only = false # not an error.
				
			try:
				self.xml_version_string = config.get(self.configSection, "xml_version_string")
			except:
				self.xml_version_string = prolog_version_string
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

			
			#@<< get prefs >>
			#@+node:3::<< get prefs >>
			#@+body
			# Names of prefsSection prefs
			boolPrefsNames = [
				"output_doc_chunks",
				"run_tangle_done.py","run_untangle_done.py",
				"tangle_outputs_header" ]
					
			for name in ["page_width","tab_width"]:
				try:
					val = config.getint(self.prefsSection, name)
					self.prefsDict[name] = val
				except: pass # not an error.
				
			stringPrefsDict = [
				"default_tangle_directory",
				"default_target_language"]
			
			for name in stringPrefsDict:
				try:
					val = config.get(self.prefsSection, name)
					self.prefsDict[name] = val
				except: pass # not an error.
				
			for name in boolPrefsNames:
				try:
					val = config.getboolean(self.prefsSection, name)
					self.prefsDict[name] = val
				except: pass # not an error.
			#@-body
			#@-node:3::<< get prefs >>

			
			#@<< get find prefs >>
			#@+node:4::<< get find prefs >>
			#@+body
			# Names of find/change prefs
			boolFindNames = [
					"batch", "ignore_case",
					"mark_changes", "mark_finds",
					"pattern_match", "reverse",
					"search_body", "search_headline",
					"suboutline_only",
					"whole_word", "wrap" ]
			
			for name in ["change_string", "find_string" ]:
				try:
					val = config.get(self.findSection, name)
					self.findDict[name] = val
				except: pass # not an error.
				
			for name in boolFindNames:
				try:
					val = config.getboolean(self.findSection, name)
					self.findDict[name] = val
				except: pass # not an error.
			#@-body
			#@-node:4::<< get find prefs >>

			
			#@<< get font prefs >>
			#@+node:5::<< get font prefs >>
			#@+body
			# Not yet.
			#@-body
			#@-node:5::<< get font prefs >>

			
			#@<< get syntax coloring prefs >>
			#@+node:6::<< get syntax coloring prefs >>
			#@+body
			# Not yet.
			#@-body
			#@-node:6::<< get syntax coloring prefs >>

			# print `self.recentFiles`
			# print `self.prefsDict`
			cf.close()
		except:
			# es("Can not open " + self.configFileName)
			pass
	#@-body
	#@-node:7::open
	#@+node:8::setCommandsFindIvars
	#@+body
	# Sets ivars of c that can be overridden by leoConfig.txt
	
	def setCommandsFindIvars (self,c):
	
		# print "setCommandsFindIvars"
		config = self
		
		#@<< set find ivars >>
		#@+node:1::<< set find ivars >>
		#@+body
		val = config.getIntFindPref("batch")
		if val: c.batch_flag = val
		
		val = config.getIntFindPref("wrap")
		if val: c.wrap_flag = val
		
		val = config.getIntFindPref("whole_word")
		if val: c.whole_word_flag = val
		
		val = config.getIntFindPref("ignore_case")
		if val: c.ignore_case_flag = val
		
		val = config.getIntFindPref("pattern_match")
		if val: c.pattern_match_flag = val
		
		val = config.getIntFindPref("search_headline")
		if val: c.search_headline_flag = val
		
		val = config.getIntFindPref("search_body")
		if val: c.search_body_flag = val
		
		val = config.getIntFindPref("suboutline_only")
		if val: c.suboutline_only_flag = val
		
		val = config.getIntFindPref("mark_changes")
		if val: c.mark_changes_flag = val
		
		val = config.getIntFindPref("mark_finds")
		if val: c.mark_finds_flag = val
		
		val = config.getIntFindPref("reverse")
		if val: c.reverse_flag = val
		
		val = config.getFindPref("change_string")
		if val: c.change_text = val
		
		val = config.getFindPref("find_string")
		if val: c.find_text = val
		#@-body
		#@-node:1::<< set find ivars >>

		app().findFrame.init(c)
	#@-body
	#@-node:8::setCommandsFindIvars
	#@+node:9::setCommandsIvars
	#@+body
	# Sets ivars of c that can be overridden by leoConfig.txt
	
	def setCommandsIvars (self,c):
	
		config = self
		
		#@<< set prefs ivars >>
		#@+node:1::<< set prefs ivars >>
		#@+body
		
		val = config.getIntPref("tab_width")
		if val: c.tab_width = val
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
	#@-node:9::setCommandsIvars
	#@+node:10::setConfigFindIvars
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
	#@-node:10::setConfigFindIvars
	#@+node:11::setConfigIvars
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
	#@-node:11::setConfigIvars
	#@+node:12::update
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
		try:
			cf = open(self.configFileName,"w")
			config.readfp(cf)
			
			#@<< write config section >>
			#@+node:1::<< write config section >>
			#@+body
			section = self.configSection
			
			if config.has_section(section):
				config.remove_section(section)
			config.add_section(section)
			
			config.set(section,"read_only",self.read_only)
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

			
			#@<< write find/change section >>
			#@+node:4::<< write find/change section >>
			#@+body
			self.update_section(config,self.findSection,self.findDict)
			#@-body
			#@-node:4::<< write find/change section >>

			
			#@<< write font section >>
			#@+node:5::<< write font section >>
			#@+body
			self.update_section(config,self.fontSection,self.fontDict)
			#@-body
			#@-node:5::<< write font section >>

			
			#@<< write syntax coloring section >>
			#@+node:6::<< write syntax coloring section >>
			#@+body
			self.update_section(config,self.syntaxColoringSection,self.syntaxColoringDict)
			#@-body
			#@-node:6::<< write syntax coloring section >>

			config.write(cf)
			cf.close()
		except:
			# traceback.print_exc() 
			pass
	#@-body
	#@-node:12::update
	#@+node:13::update_section
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
	#@-node:13::update_section
	#@-others
#@-body
#@-node:0::@file leoConfig.py
#@-leo
