#@+leo-ver=4
#@+node:@file rowcol.py
"""Add row/column indicators to the toolbar.""" 

__name__ = "Row/Column indicators"
__version__ = "0.1" 

from leoPlugins import * 
from leoGlobals import * 

try:    import Tkinter 
except: Tkinter = None 
Tk = Tkinter

#@+others
#@+node:class rowColClass
class rowColClass:
	
	"""Class that puts row/column indicators in the status bar."""
	
	#@	@+others
	#@+node:__init__
	def __init__ (self):
		
		self.lastStatusRow, self.lastStatusCol = -1,-1
	#@nonl
	#@-node:__init__
	#@+node:addWidgets
	def addWidgets (self,tag,keywords):
		
		self.c = keywords['c']
	
		toolbar = self.c.frame.iconFrame
	
		# Main container 
		self.rowColFrame = f = Tkinter.Frame(toolbar) 
		f.pack(side="left")
		
		text = "line 0, col 0"
		width = len(text) # Setting the width here prevents jitters.
		self.rowColLabel = Tk.Label(f,text=text,width=width,anchor="w")
		self.rowColLabel.pack(side="left")
		
		# Update the row/column indicators immediately to reserve a place.
		self.updateRowColWidget()
	#@nonl
	#@-node:addWidgets
	#@+node:updateRowColWidget
	def updateRowColWidget (self):
		
		c = self.c ; body = c.frame.body.bodyCtrl ; gui = app.gui
		tab_width = c.frame.tab_width
		
		# New for Python 2.3: may be called during shutdown.
		if app.killed:
			return
	
		index = body.index("insert")
		row,col = gui.getindex(body,index)
		
		if col > 0:
			if 0: # new code
				s = c.frame.body.getRange(index1,index2)
			else:
				s = body.get("%d.0" % (row),index)
			s = toUnicode(s,app.tkEncoding)
			col = computeWidth(s,tab_width)
	
		if row != self.lastStatusRow or col != self.lastStatusCol:
			s = "line %d, col %d " % (row,col)
			self.rowColLabel.configure(text=s)
			self.lastStatusRow = row
			self.lastStatusCol = col
			
		# Reschedule this routine 100 ms. later.
		# Don't use after_idle: it hangs Leo.
		self.rowColFrame.after(100,self.updateRowColWidget)
	#@nonl
	#@-node:updateRowColWidget
	#@-others
#@nonl
#@-node:class rowColClass
#@-others

if Tkinter: 

	if app.gui is None: 
		app.createTkGui(__file__)

	if app.gui.guiName() == "tkinter":
		rowCol = rowColClass() 
		registerHandler("after-create-leo-frame",rowCol.addWidgets) 
		plugin_signon("rowcol")
#@nonl
#@-node:@file rowcol.py
#@-leo
