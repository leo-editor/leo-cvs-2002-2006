#@+leo-ver=4-thin
#@+node:ekr.20031218072017.3897:@thin leoTkinterFind.py
import leoGlobals as g
from leoGlobals import true,false

import leoFind, leoTkinterDialog
import string,sys,Tkinter,types

Tk=Tkinter

class leoTkinterFind (leoFind.leoFind,leoTkinterDialog.leoTkinterDialog):

	"""A class that implements Leo's tkinter find dialog."""

	#@	@+others
	#@+node:ekr.20031218072017.3898:Birth & death
	#@+node:ekr.20031218072017.3899:__init__
	def __init__(self,title="Leo Find/Change",resizeable=false):
		
		# Init the base classes...
	
		leoFind.leoFind.__init__(self)
		leoTkinterDialog.leoTkinterDialog.__init__(self,title,resizeable)
	
		#@	<< init the tkinter ivars >>
		#@+node:ekr.20031218072017.3900:<< init the tkinter ivars >>
		self.dict = {}
		
		for key in self.intKeys:
			self.dict[key] = Tk.IntVar()
		
		for key in self.newStringKeys:
			self.dict[key] = Tk.StringVar()
			
		self.s_text = Tk.Text() # Used by find.search()
		#@nonl
		#@-node:ekr.20031218072017.3900:<< init the tkinter ivars >>
		#@nl
		
		self.createTopFrame() # Create the outer tkinter dialog frame.
		self.createFrame()
	#@nonl
	#@-node:ekr.20031218072017.3899:__init__
	#@+node:ekr.20031218072017.3901:destroySelf
	def destroySelf (self):
		
		self.top.destroy()
	#@nonl
	#@-node:ekr.20031218072017.3901:destroySelf
	#@+node:ekr.20031218072017.3902:find.createFrame
	def createFrame (self):
	
		# Create the find panel...
		outer = Tk.Frame(self.frame,relief="groove",bd=2)
		outer.pack(padx=2,pady=2)
	
		#@	<< Create the Find and Change panes >>
		#@+node:ekr.20031218072017.3904:<< Create the Find and Change panes >>
		fc = Tk.Frame(outer, bd="1m")
		fc.pack(anchor="n", fill="x", expand=1)
		
		# Removed unused height/width params: using fractions causes problems in some locales!
		fpane = Tk.Frame(fc, bd=1)
		cpane = Tk.Frame(fc, bd=1)
		
		fpane.pack(anchor="n", expand=1, fill="x")
		cpane.pack(anchor="s", expand=1, fill="x")
		
		# Create the labels and text fields...
		flab = Tk.Label(fpane, width=8, text="Find:")
		clab = Tk.Label(cpane, width=8, text="Change:")
		
		# Use bigger boxes for scripts.
		self.find_text   = ftxt = Tk.Text(fpane,bd=1,relief="groove",height=4,width=20)
		self.change_text = ctxt = Tk.Text(cpane,bd=1,relief="groove",height=4,width=20)
		
		fBar = Tk.Scrollbar(fpane,name='findBar')
		cBar = Tk.Scrollbar(cpane,name='changeBar')
		
		# Add scrollbars.
		for bar,txt in ((fBar,ftxt),(cBar,ctxt)):
			txt['yscrollcommand'] = bar.set
			bar['command'] = txt.yview
			bar.pack(side="right", fill="y")
		
		flab.pack(side="left")
		clab.pack(side="left")
		ctxt.pack(side="right", expand=1, fill="both")
		ftxt.pack(side="right", expand=1, fill="both")
		#@nonl
		#@-node:ekr.20031218072017.3904:<< Create the Find and Change panes >>
		#@nl
		#@	<< Create four columns of radio and checkboxes >>
		#@+node:ekr.20031218072017.3903:<< Create four columns of radio and checkboxes >>
		columnsFrame = Tk.Frame(outer,relief="groove",bd=2)
		columnsFrame.pack(anchor="e",expand=1,padx="7p",pady="2p") # Don't fill.
		
		numberOfColumns = 4 # Number of columns
		columns = [] ; radioLists = [] ; checkLists = []
		for i in xrange(numberOfColumns):
			columns.append(Tk.Frame(columnsFrame,bd=1))
			radioLists.append([])
			checkLists.append([])
		
		for i in xrange(numberOfColumns):
			columns[i].pack(side="left",padx="1p") # fill="y" Aligns to top. padx expands columns.
		
		radioLists[0] = [
			(self.dict["radio-find-type"],"Plain Search","plain-search"),  
			(self.dict["radio-find-type"],"Pattern Match Search","pattern-search"),
			(self.dict["radio-find-type"],"Script Search","script-search")]
		checkLists[0] = [
			("Script Change",self.dict["script_change"])]
		checkLists[1] = [
			("Whole Word",  self.dict["whole_word"]),
			("Ignore Case", self.dict["ignore_case"]),
			("Wrap Around", self.dict["wrap"]),
			("Reverse",     self.dict["reverse"])]
		radioLists[2] = [
			(self.dict["radio-search-scope"],"Entire Outline","entire-outine"),
			(self.dict["radio-search-scope"],"Suboutline Only","suboutline-only"),  
			(self.dict["radio-search-scope"],"Node Only","node-only"),    
			(self.dict["radio-search-scope"],"Selection Only","selection-only")] # 11/9/03
		checkLists[2] = []
		checkLists[3] = [
			("Search Headline Text", self.dict["search_headline"]),
			("Search Body Text",     self.dict["search_body"]),
			("Mark Finds",           self.dict["mark_finds"]),
			("Mark Changes",         self.dict["mark_changes"])]
		
		for i in xrange(numberOfColumns):
			for var,name,val in radioLists[i]:
				box = Tk.Radiobutton(columns[i],anchor="w",text=name,variable=var,value=val)
				box.pack(fill="x")
				box.bind("<1>", self.resetWrap)
				if val == None: box.configure(state="disabled")
			for name, var in checkLists[i]:
				box = Tk.Checkbutton(columns[i],anchor="w",text=name,variable=var)
				box.pack(fill="x")
				box.bind("<1>", self.resetWrap)
				if var == None: box.configure(state="disabled")
		#@-node:ekr.20031218072017.3903:<< Create four columns of radio and checkboxes >>
		#@nl
		#@	<< Create two rows of buttons >>
		#@+node:ekr.20031218072017.3905:<< Create two rows of buttons >>
		# Create the button panes
		buttons  = Tk.Frame(outer,bd=1)
		buttons2 = Tk.Frame(outer,bd=1)
		buttons.pack (anchor="n",expand=1,fill="x")
		buttons2.pack(anchor="n",expand=1,fill="x")
		
		# Create the first row of buttons
		findButton=Tk.Button(buttons,width=8,text="Find",bd=4,command=self.findButton) # The default.
		contextBox=Tk.Checkbutton(buttons,anchor="w",text="Show Context",variable=self.dict["batch"])
		findAllButton=Tk.Button(buttons,width=8,text="Find All",command=self.findAllButton)
		
		findButton.pack   (pady="1p",padx="25p",side="left")
		contextBox.pack   (pady="1p",           side="left",expand=1)
		findAllButton.pack(pady="1p",padx="25p",side="right",fill="x",)
		
		# Create the second row of buttons
		changeButton    =Tk.Button(buttons2,width=8,text="Change",command=self.changeButton)
		changeFindButton=Tk.Button(buttons2,        text="Change, Then Find",command=self.changeThenFindButton)
		changeAllButton =Tk.Button(buttons2,width=8,text="Change All",command=self.changeAllButton)
		
		changeButton.pack    (pady="1p",padx="25p",side="left")
		changeFindButton.pack(pady="1p",           side="left",expand=1)
		changeAllButton.pack (pady="1p",padx="25p",side="right")
		#@nonl
		#@-node:ekr.20031218072017.3905:<< Create two rows of buttons >>
		#@nl
		
		for widget in (self.find_text, self.change_text):
			widget.bind ("<1>",  self.resetWrap)
			widget.bind("<Key>", self.resetWrap)
		
		for widget in (outer, self.find_text, self.change_text):
			widget.bind("<Key-Return>", self.findButton)
			widget.bind("<Key-Escape>", self.onCloseWindow)
		
		self.top.protocol("WM_DELETE_WINDOW", self.onCloseWindow)
	#@nonl
	#@-node:ekr.20031218072017.3902:find.createFrame
	#@+node:ekr.20031218072017.2059:find.init
	def init (self,c):
	
		# N.B.: separate c.ivars are much more convenient than a dict.
		for key in self.intKeys:
			val = getattr(c, key + "_flag")
			val = g.choose(val,1,0) # 2/1/04: work around major Tk problem.
			self.dict[key].set(val)
			# g.trace(key,val)
	
		#@	<< set find/change widgets >>
		#@+node:ekr.20031218072017.2060:<< set find/change widgets >>
		self.find_text.delete("1.0","end")
		self.find_text.insert("end",c.find_text)
		
		self.change_text.delete("1.0","end")
		self.change_text.insert("end",c.change_text)
		#@nonl
		#@-node:ekr.20031218072017.2060:<< set find/change widgets >>
		#@nl
		#@	<< set radio buttons from ivars >>
		#@+node:ekr.20031218072017.2061:<< set radio buttons from ivars >>
		found = false
		for var,setting in (
			("pattern_match","pattern-search"),
			("script_search","script-search")):
			val = self.dict[var].get()
			if val:
				self.dict["radio-find-type"].set(setting)
				found = true ; break
		if not found:
			self.dict["radio-find-type"].set("plain-search")
			
		found = false
		for var,setting in (
			("suboutline_only","suboutline-only"),
			("node_only","node-only"),
			("selection_only","selection-only")): # 11/9/03
			val = self.dict[var].get()
			if val:
				self.dict["radio-search-scope"].set(setting)
				found = true ; break
		if not found:
			self.dict["radio-search-scope"].set("entire-outine")
		#@nonl
		#@-node:ekr.20031218072017.2061:<< set radio buttons from ivars >>
		#@nl
	#@nonl
	#@-node:ekr.20031218072017.2059:find.init
	#@+node:ekr.20031218072017.1460:find.set_ivars
	def set_ivars (self,c):
		
		# N.B.: separate c.ivars are much more convenient than a dict.
		for key in self.intKeys:
			val = self.dict[key].get()
			setattr(c, key + "_flag", val)
			# g.trace(key,val)
	
		# Set ivars from radio buttons. 10/2/01: convert these to 1 or 0.
		find_type = self.dict["radio-find-type"].get()
		c.pattern_match_flag = g.choose(find_type == "pattern-search",1,0)
		c.script_search_flag = g.choose(find_type == "script-search",1,0)
	
		search_scope = self.dict["radio-search-scope"].get()
		c.suboutline_only_flag = g.choose(search_scope == "suboutline-only",1,0)
		c.node_only_flag       = g.choose(search_scope == "node-only",1,0)
		c.selection_only_flag  = g.choose(search_scope == "selection-only",1,0) # 11/9/03
	
		s = self.find_text.get("1.0","end - 1c") # Remove trailing newline
		s = g.toUnicode(s,g.app.tkEncoding) # 2/25/03
		c.find_text = s
	
		s = self.change_text.get("1.0","end - 1c") # Remove trailing newline
		s = g.toUnicode(s,g.app.tkEncoding) # 2/25/03
		c.change_text = s
	#@nonl
	#@-node:ekr.20031218072017.1460:find.set_ivars
	#@-node:ekr.20031218072017.3898:Birth & death
	#@+node:ekr.20031218072017.3906:onCloseWindow
	def onCloseWindow(self,event=None):
	
		self.top.withdraw()
	#@nonl
	#@-node:ekr.20031218072017.3906:onCloseWindow
	#@+node:ekr.20031218072017.3907:bringToFront
	def bringToFront (self):
		
		"""Bring the tkinter Find Panel to the front."""
		
		c = g.top() ; t = self.find_text ; gui = g.app.gui
		        
		self.top.withdraw() # Helps bring the window to the front.
		self.top.deiconify()
		self.top.lift()
	
		gui.set_focus(c,t)
		gui.setTextSelection (t,"1.0","end") # Thanks Rich.
	#@nonl
	#@-node:ekr.20031218072017.3907:bringToFront
	#@+node:ekr.20031218072017.3908:Tkinter wrappers (leoTkinterFind)
	def gui_search (self,t,*args,**keys):
		return t.search(*args,**keys)
	
	def init_s_text (self,s):
		c = self.c ; t = self.s_text	
		t.delete("1.0","end")
		t.insert("end",s)
		t.mark_set("insert",g.choose(c.reverse_flag,"end","1.0"))
		return t
	#@-node:ekr.20031218072017.3908:Tkinter wrappers (leoTkinterFind)
	#@-others
#@nonl
#@-node:ekr.20031218072017.3897:@thin leoTkinterFind.py
#@-leo
