#@+leo-ver=4-thin
#@+node:ekr.20040108095351:@file-thin rowcol.py
"""Add row/column indicators to the toolbar."""

#@@language python

__name__ = "Row/Column indicators"
__version__ = "0.1" 

import leoPlugins 
import leoGlobals as g
from leoGlobals import true,false 

try: import Tkinter as Tk
except ImportError: Tk = None 

#@+others
#@+node:ekr.20040108095351.1:class rowColClass
class rowColClass:
	
	"""Class that puts row/column indicators in the status bar."""
	
	#@	@+others
	#@+node:ekr.20040108100040:__init__
	def __init__ (self):
		
		self.lastStatusRow, self.lastStatusCol = -1,-1
		self.c = None # Will be set later.  Needed for idle handling.
	#@nonl
	#@-node:ekr.20040108100040:__init__
	#@+node:ekr.20040108095351.2:addWidgets
	def addWidgets (self,tag,keywords):
	
		self.c = c = keywords.get("c")
		assert(c)
	
		toolbar = self.c.frame.iconFrame
	
		# Main container 
		self.rowColFrame = f = Tk.Frame(toolbar) 
		f.pack(side="left")
		
		text = "line 0, col 0"
		width = len(text) # Setting the width here prevents jitters.
		self.rowColLabel = Tk.Label(f,text=text,width=width,anchor="w")
		self.rowColLabel.pack(side="left")
		
		# Update the row/column indicators immediately to reserve a place.
		self.updateRowColWidget()
	#@nonl
	#@-node:ekr.20040108095351.2:addWidgets
	#@+node:ekr.20040108095351.4:updateRowColWidget
	def updateRowColWidget (self,*args,**keys):
		
		c = self.c
	
		# This is called at idle-time, and there can be problems when closing the window.
		if g.app.killed or not c or c != g.top():
			return
	
		body = c.frame.body.bodyCtrl ; gui = g.app.gui
		tab_width = c.frame.tab_width
	
		index = body.index("insert")
		row,col = gui.getindex(body,index)
		
		if col > 0:
			s = body.get("%d.0" % (row),index)
			s = g.toUnicode(s,g.app.tkEncoding)
			col = g.computeWidth(s,tab_width)
	
		if row != self.lastStatusRow or col != self.lastStatusCol:
			s = "line %d, col %d " % (row,col)
			self.rowColLabel.configure(text=s)
			self.lastStatusRow = row
			self.lastStatusCol = col
	#@nonl
	#@-node:ekr.20040108095351.4:updateRowColWidget
	#@-others
#@nonl
#@-node:ekr.20040108095351.1:class rowColClass
#@-others

if Tk: 

	if g.app.gui is None: 
		g.app.createTkGui(__file__)

	if g.app.gui.guiName() == "tkinter":
		rowCol = rowColClass()
		leoPlugins.registerHandler("after-create-leo-frame",rowCol.addWidgets)
		leoPlugins.registerHandler("idle",rowCol.updateRowColWidget) 
		g.plugin_signon("rowcol")
#@nonl
#@-node:ekr.20040108095351:@file-thin rowcol.py
#@-leo
