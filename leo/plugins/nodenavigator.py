#@+leo-ver=4
#@+node:@file nodenavigator.py
"""Add a quick node navigators to the toolbar in Leo 

Adds a node navigator to the toolbar. The navigator allows quick
access to marked nodes. You can either go to the marked node or hoist
the marked node.

""" 

__name__ = "Node Navigator"
__version__ = "0.3" 

from leoPlugins import * 
from leoGlobals import * 

try:    import Tkinter 
except: Tkinter = None 
Tk = Tkinter 

# Set this to 0 if the sizing of the toolbar controls doesn't look good on your platform. 
USE_FIXED_SIZES = 1 

#@+others
#@+node:class Navigator
class Navigator: 
	"""A node navigation aid for Leo"""
	#@	@+others
	#@+node:addWidgets
	def addWidgets(self, tag, keywords): 
		"""Add the widgets to the navigation bar""" 
		self.c = c = keywords['c'] 
		toolbar = self.c.frame.iconFrame 
		# Main container 
		self.frame = Tkinter.Frame(toolbar) 
		self.frame.pack(side="left")
		# Marks
		marks = ["Marks"] 
		self.mark_value = Tkinter.StringVar() 
		self.marks = Tkinter.OptionMenu(self._getSizer(self.frame,29,70),self.mark_value,*marks)
		self.mark_value.set(marks[0]) 
		self.marks.pack(side="right",fill="both",expand=1)
		# Recent.
		recent = ["Recent"]
		self.recent_value = Tkinter.StringVar() 
		self.recent = Tkinter.OptionMenu(self._getSizer(self.frame,29,70),self.recent_value,*recent) 
		self.recent_value.set(recent[0]) 
		self.recent.pack(side="left",fill="both",expand=1)
		# Recreate the menus immediately.
		self.updateRecent("tag",{"c":c})
		self.updateMarks("tag",{"c":c})
	#@nonl
	#@-node:addWidgets
	#@+node:_getSizer
	def _getSizer(self, parent, height, width):
		
		"""Return a sizer object to force a Tk widget to be the right size""" 
		if USE_FIXED_SIZES: 
			sizer = Tkinter.Frame(parent,height=height,width=width) 
			sizer.pack_propagate(0) # don't shrink 
			sizer.pack(side="right") 
			return sizer 
		else: 
			return parent 
	#@nonl
	#@-node:_getSizer
	#@+node:onSelect
	def onSelect(self, vnode):
		"""Do the navigation"""
	
		self.c.selectVnode(vnode)
	#@nonl
	#@-node:onSelect
	#@+node:updateRecent
	def updateRecent(self,tag,keywords):
		"""Update the marks list"""        
		c = keywords.get("c")
		v = c.rootVnode()
	
		# Clear old marks menu
		try:
			menu = self.recent["menu"]
			menu.delete(0,"end")
		except: return
	
		# Make sure the node still exists.
		# Insert only the last cloned node.
		vnodes = [] ; tnodes = []
		for v in c.visitedList:
			if v.exists(c) and v.t not in tnodes:
				
				def callback(event=None,self=self,v=v):
					return self.onSelect(v)
	
				menu.add_command(label=v.headString(),command=callback)
				tnodes.append(v.t)
				vnodes.append(v)
	#@nonl
	#@-node:updateRecent
	#@+node:updateMarks
	def updateMarks(self, tag, keywords):
		"""Update the marks list"""        
		c = keywords.get("c")
		v = c.rootVnode()
	
		# Clear old marks menu
		try:
			menu = self.marks["menu"]
			menu.delete(0,"end")
		except: return
	
		# Find all marked nodes
		vnodes = [] ; tnodes = []
		while v:
			if v.isMarked() and v.t not in tnodes:
				
				def callback(event=None,self=self,v=v):
					return self.onSelect(v)
	
				name = v.headString().strip()
				menu.add_command(label=name,command=callback)
				tnodes.append(v.t)
				vnodes.append(v)
			v = v.threadNext()
	#@nonl
	#@-node:updateMarks
	#@-others
#@-node:class Navigator
#@-others

if Tkinter: 
	if app.gui is None: 
		app.createTkGui(__file__) 

	if app.gui.guiName() == "tkinter":
		nav = Navigator() 
		registerHandler("after-create-leo-frame", nav.addWidgets) 
		registerHandler(("set-mark","clear-mark"),nav.updateMarks)
		registerHandler("select2",nav.updateRecent)
		plugin_signon("nodenavigator")
#@nonl
#@-node:@file nodenavigator.py
#@-leo
