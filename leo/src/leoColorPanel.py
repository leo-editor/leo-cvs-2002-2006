#@+leo-ver=4
#@+node:@file leoColorPanel.py
import leoGlobals as g
from leoGlobals import true,false

class leoColorPanel:
	
	"""A base class to create Leo's color panel.
	
	Subclasses may create subsidiary panels."""
	
	#@	<< define default color panel data >>
	#@+node:<< define default color panel data >>
	colorPanelData = (
		#Dialog name,                option name,         default color),
		("Brackets",          "section_name_brackets_color", "blue"),
		("Comments",          "comment_color",               "red"),
		("CWEB section names","cweb_section_name_color",     "red"),
		("Directives",        "directive_color",             "blue"),
		("Doc parts",         "doc_part_color",              "red"),
		("Keywords" ,         "keyword_color",               "blue"),
		("Leo Keywords",      "leo_keyword_color",           "blue"),
		("Section Names",     "section_name_color",          "red"),
		("Strings",           "string_color",   "#00aa00"), # Used by IDLE.
		("Undefined Names",   "undefined_section_name_color","red") )
	#@nonl
	#@-node:<< define default color panel data >>
	#@nl

	#@	@+others
	#@+node:leoColorPanels.__init__
	def __init__ (self,c):
		
		self.c = c
		self.frame = c.frame
		self.top = None # Created in subclass.
	
		self.revertColors = {}
		
		config = g.app.config
		for name,option_name,default_color in self.colorPanelData:
			self.revertColors[option_name] = config.getColorsPref(option_name)
	#@nonl
	#@-node:leoColorPanels.__init__
	#@+node:Must be overridden in subclasses
	def bringToFront (self):
		self.oops()
	
	def oops(self):
		print "leoColorPanel oops:", g.callerName(2), "should be overridden in subclass"
	#@nonl
	#@-node:Must be overridden in subclasses
	#@-others
#@nonl
#@-node:@file leoColorPanel.py
#@-leo
