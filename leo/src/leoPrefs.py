#@+leo-ver=4
#@+node:@file leoPrefs.py
#@@language python

import leoGlobals as g
from leoGlobals import true,false

import string
	
class leoPrefs:
	
	#@	<< define leoPrefs constants >>
	#@+node:<< define leoPrefs constants >>
	# Constants used for defaults when leoConfig.txt can not be read.
	default_page_width = 132
	default_tab_width = 4
	default_target_language = "python"
	
	# Corresponding ivars in the Commands class and this class.
	ivars = [
		"tangle_batch_flag", "untangle_batch_flag",
		"use_header_flag", "output_doc_flag",
		"tangle_directory", "page_width", "tab_width",
		"target_language" ]
	#@nonl
	#@-node:<< define leoPrefs constants >>
	#@nl

	"""A base class that creates Leo's preferenes panel."""
	#@	@+others
	#@+node:prefs.__init__
	def __init__ (self,c):
	
		self.c = c
	
		# Global options...
		self.page_width = self.default_page_width
		self.tab_width = self.default_tab_width
		self.tangle_batch_flag = 0
		self.untangle_batch_flag = 0
		
		# Default Tangle options...
		self.tangle_directory = ""
		self.use_header_flag = 0
		self.output_doc_flag = 0
		
		# Default Target Language...
		self.target_language = self.default_target_language
	
		self.init(c)
		# g.es("Prefs.__init__")
	#@nonl
	#@-node:prefs.__init__
	#@+node:prefs.init
	# Initializes prefs ivars and widgets from c's ivars.
	
	def init(self,c):
	
		self.c = c
		#g.trace(c.tab_width)
	
		for var in self.ivars:
			val = getattr(c,var)
			setattr(self,var,val)
			# g.trace(val,var)
	
		#@	<< remember values for revert >>
		#@+node:<< remember values for revert >>
		# Global options
		self.revert_tangle_batch_flag = c.tangle_batch_flag
		self.revert_untangle_batch_flag = c.untangle_batch_flag
		self.revert_page_width = c.page_width
		self.revert_tab_width = c.tab_width
		
		# Default Tangle Options
		self.revert_tangle_directory = c.tangle_directory
		self.revert_output_doc_flag = c.output_doc_flag
		self.revert_use_header_flag = c.use_header_flag
		
		# Default Target Language
		if c.target_language == None:
			c.target_language = "python"
		self.revert_target_language = c.target_language
		#@nonl
		#@-node:<< remember values for revert >>
		#@nl
	#@nonl
	#@-node:prefs.init
	#@+node:restoreOptions
	def restoreOptions (self):
		
		c = self.c
		
		# Global options
		c.tangle_batch_flag = self.revert_tangle_batch_flag
		c.untangle_batch_flag = self.revert_untangle_batch_flag
		c.page_width = self.revert_page_width
		c.tab_width = self.revert_tab_width
		
		# Default Tangle Options
		c.tangle_directory = self.revert_tangle_directory
		c.output_doc_flag = self.revert_output_doc_flag
		c.use_header_flag = self.revert_use_header_flag
		
		# Default Target Language
		c.target_language = self.revert_target_language
	#@nonl
	#@-node:restoreOptions
	#@+node:Must be overridden in subclasses
	def bringToFront (self):
		self.oops()
		
	def oops(self):
		print ("leoPrefs oops:",
			g.callerName(2),
			"should be overridden in subclass")
			
	def setWidgets(self):
		self.oops()
	#@-node:Must be overridden in subclasses
	#@+node:printIvars
	def print_ivars (self):
		
		"""Debugging routine for Prefs panel."""
		
		for var in self.ivars:
			g.trace(var, getattr(self,var))
	#@nonl
	#@-node:printIvars
	#@-others
#@nonl
#@-node:@file leoPrefs.py
#@-leo
