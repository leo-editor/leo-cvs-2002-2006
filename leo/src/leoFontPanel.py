#@+leo-ver=4
#@+node:@file leoFontPanel.py
#@@language python

from leoGlobals import *
import exceptions,sys,string,Tkinter,tkFont
	
class leoFontPanel:
	
	"""The base class for Leo's font panel."""

	#@	@+others
	#@+node:fontPanel.__init__
	def __init__ (self,c):
	
		self.c = c
		self.frame = c.frame
		self.default_font = None # Should be set in subclasses.
		self.last_selected_font = None
	#@nonl
	#@-node:fontPanel.__init__
	#@+node:Must be overridden in subclasses
	def bringToFront(self):
		
		self.oops()
		
	def oops(self):
	
		print ("leoTkinterFontPanel oops:",
			callerName(2),
			"should be overridden in subclass")
	#@nonl
	#@-node:Must be overridden in subclasses
	#@-others
#@nonl
#@-node:@file leoFontPanel.py
#@-leo
