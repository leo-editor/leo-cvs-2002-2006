#@+leo-ver=4
#@+node:@file searchbox.py
#@<< doc string >>
#@+node:<< doc string >>
"""Add a quick search to the toolbar in Leo

A search box which behaves like a web site search is added, along with
a "GO" button to do quick searches right from the main Leo window. All the
current search options are retained except that "search body text" is
explicitely set - mainly because this is by far the most common use case.

Pressing <CR> while editing the text automatically does a search. Repeated
searches can be done by clicking the "GO" button.

The combo box also stores a list of previous searches, which can be
selected to quickly repeat a search. When activating a previous
search the original search mode is used.

Still to do:

- incremental search
- reverse search
- persist recent searches across Leo sessions
- use INI file to set options for list size etc
"""
#@nonl
#@-node:<< doc string >>
#@nl

__version__ = "0.3"

from leoPlugins import *
from leoGlobals import *
import leoFind

try:
	import Tkinter
except ImportError:
	Tkinter = None
Tk = Tkinter

#@<< vars >>
#@+node:<< vars >>
# Set this to 0 if the sizing of the toolbar controls doesn't look good on 
# your platform 
USE_FIXED_SIZES = 1

# Set this to the number of previous searches you want to remember 
SEARCH_LIST_LENGTH = 10

# Define the search option/find option matrix - we define as a list first 
# so we can keep a nice order. You can easily add options here if you 
# know what you are doing ;) 
# If an option is supposed to zero a flag then start the name with a ! 

OPTION_LIST = [
	("Search text", ["search_body_flag", "search_headline_flag", "ignore_case_flag"]), 
	("Search word", ["search_body_flag", "search_headline_flag", "whole_word_flag", "ignore_case_flag"]), 
	("Search headlines", ["search_headline_flag","ignore_case_flag"]), 
	("Search body", ["search_body_flag", "ignore_case_flag"]), 
	("Case sensitive", ["search_body_flag", "search_headline_flag"]), 
]

OPTION_DICT = dict(OPTION_LIST)
#@nonl
#@-node:<< vars >>
#@nl
#@+others
#@+node:class SearchBox
class SearchBox:
	"""A search box for Leo"""
	#@	@+others
	#@+node:_getSizer
	def _getSizer(self, parent, height, width):
		"""Return a sizer object to force a Tk widget to be the right size"""
		if USE_FIXED_SIZES: 
			sizer = Tkinter.Frame(parent, height=height, width=width)
			sizer.pack_propagate(0) # don't shrink 
			sizer.pack(side="right")
			return sizer
		else:
			return parent
	#@nonl
	#@-node:_getSizer
	#@+node:addWidgets
	def addWidgets(self, tags, keywords):
		"""Add the widgets to the navigation bar"""
		self.c = keywords['c'] 
		toolbar = self.c.frame.iconFrame
		# Button.
		self.go = Tkinter.Button(self._getSizer(toolbar, 25, 32), text="GO", command=self.doSearch)
		self.go.pack(side="right", fill="both", expand=1)
		# Search options.
		options = [name for name, flags in OPTION_LIST]
		self.option_value = Tkinter.StringVar() 
		self.options = Tkinter.OptionMenu(
			self._getSizer(toolbar, 29, 130), self.option_value, *options)
		self.option_value.set(options[0]) 
		self.options.pack(side="right", fill="both", expand=1)
		# Text entry.
		self.search = Tkinter.Entry(self._getSizer(toolbar, 24, 130))
		self.search.pack(side="right", padx=3, fill="both", expand=1)
		self.search.bind("<Return>", self.onKey)
		# Store a list of the last searches.
		self.search_list = []
	
	#@-node:addWidgets
	#@+node:doSearch
	def doSearch(self,*args,**keys):
		
		"""Do the actual search"""
		# import pdb; pdb.set_trace()
		text = self.search.get()
		# Remove the old find frame so its options don't compete with ours.
		search_mode = self.option_value.get() 
		new_find = QuickFind(text,search_mode)
		old_find, app.findFrame = app.findFrame, new_find
		# Do the search.
		self.c.findNext()
		# Restore the find frame.
		app.findFrame = old_find
		# Remember this list 
		self.updateRecentList(text, search_mode) 
		if 0: # This doesn't work yet: the user can't see the match.
			self.search.focus_set()
	#@nonl
	#@-node:doSearch
	#@+node:onBackSpace
	def onBackSpace (self,event=None):
		trace()
	#@-node:onBackSpace
	#@+node:onKey
	def onKey (self,event=None): 
		"""Called when the user presses Return in the text entry box"""
		self.search.after_idle(self.doSearch)
	
	#@-node:onKey
	#@+node:searchRecent
	def searchRecent(self, *args, **kw):
		"""Do a search on a recently used item"""
		# Find the item.
		name = self.option_value.get() 
		for item_name, mode in self.search_list:
			if item_name == name: 
				# Ok, so set mode and text and then do the search 
				self.option_value.set(mode)
				self.search.delete(0, "end")
				self.search.insert(0, name)
				self.doSearch() 
				break
		else:
			print name, self.search_list 
			es("Recent search item not found! Looks like a bug ...", color="red")
	#@nonl
	#@-node:searchRecent
	#@+node:updateRecentList
	def updateRecentList(self, text, search_mode):
		"""Update the list of recently searched items"""
	
		# First update the menu - delete all the options if there are any
		menu = self.options["menu"]
		if self.search_list:
			menu.delete(len(OPTION_LIST),"end")
	
		menu.add_command(label="-------------", command=lambda:0) 
	
		# Update and prune list to remove a previous search for this text 
		self.search_list = [(text, search_mode)] +  [
			(name, mode) for name, mode in self.search_list[:SEARCH_LIST_LENGTH] if name <> text] 
	
		# Now update the menu 
		for name, mode in self.search_list:
			menu.add_command(
				label=name,command=Tkinter._setit(self.option_value,name,self.searchRecent))
	#@nonl
	#@-node:updateRecentList
	#@-others
#@nonl
#@-node:class SearchBox
#@+node:class QuickFind
class QuickFind(leoFind.leoFind):
	
	"""A class for quick searching"""
	
	#@	@+others
	#@+node:__init__
	def __init__(self, text, search_option=""):
		
		"""Initialize the finder"""
	
		# Init the base class.
		leoFind.leoFind.__init__(self)
		
		self.s_text = Tk.Text() # Used by find.search()
		self.__find_text = text
		self.search_option = search_option
	#@-node:__init__
	#@+node:set_ivars
	def set_ivars(self, c):
	
		"""Set the ivars for the find"""
	
		# Modified from leoTkinterFind.set_ivars
		for key in self.intKeys:
			setattr(c, key + "_flag", 0)
		c.change_text = ""
		c.find_text = self.__find_text
		
		# Set options
		for flag_name in OPTION_DICT[self.search_option]: 
			if flag_name.startswith("!"): 
				value = 0 
				name = flag_name[1:] 
			else: 
				value = 1 
				name = flag_name 
			setattr(c, name, value) 
	#@-node:set_ivars
	#@+node:init_s_text
	def init_s_text (self,s):
	
		c = self.c ; t = self.s_text	
		t.delete("1.0","end")
		t.insert("end",s)
		t.mark_set("insert",choose(c.reverse_flag,"end","1.0"))
		return t
	#@-node:init_s_text
	#@+node:gui_search
	def gui_search (self,t,*args,**keys):
	
		return t.search(*args,**keys)
	#@nonl
	#@-node:gui_search
	#@-others
#@-node:class QuickFind
#@-others

if Tkinter:
	search = SearchBox()
	
	if app.gui is None:
		app.createTkGui(__file__)

	if app.gui.guiName() == "tkinter":
		# es("Starting searchbox", color="orange")
		registerHandler("after-create-leo-frame", search.addWidgets)
		plugin_signon(__name__)
#@nonl
#@-node:@file searchbox.py
#@-leo
