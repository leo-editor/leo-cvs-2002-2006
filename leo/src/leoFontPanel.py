#@+leo-ver=4
#@+node:@file leoFontPanel.py
#@@language python

from leoGlobals import *
import exceptions,sys,string,Tkinter,tkFont

class baseLeoFontPanel:
	"""The base class for Leo's font panel."""
	#@	@+others
	#@+node:fontPanel.__init__
	def __init__ (self,c):
		
		Tk = Tkinter
		self.commands = c
		self.frame = c.frame
		self.default_font = "Courier"
		self.last_selected_font = None
		self.setRevertVars()
		# Variables to track values of style checkboxes.
		self.sizeVar = Tk.IntVar()
		self.boldVar = Tk.IntVar()
		self.italVar = Tk.IntVar()
		# Variables to track values of pane checkboxes.
		self.bodyVar = Tk.IntVar()
		self.logVar = Tk.IntVar()
		self.treeVar = Tk.IntVar()
		# Slots for callbacks
		self.listBoxIndex = 0
		self.family_list_box = None
		self.size_entry = None
		self.example_entry = None
		self.outer = None
	#@nonl
	#@-node:fontPanel.__init__
	#@+node:create_outer
	def create_outer(self):
	
		Tk = Tkinter
		top = self.top
		#@	<< Create the organizer frames >>
		#@+node:<< create the organizer frames >>
		self.outer = outer = Tk.Frame(top,bd=2,relief="groove",width="8i")
		outer.pack(padx=2,pady=2,expand=1,fill="both")
		
		upper = Tk.Frame(outer)
		upper.pack(fill="both",expand=1)
		
		lt = Tk.Frame(upper)
		lt.pack(side="left",fill="both",expand=1)
		
		rt = Tk.Frame(upper)
		rt.pack(side="right",anchor="n",padx=4) # Not filling or expanding centers contents.
		
		# Not filling or expanding centers contents.
		# padx=20 gives more room to the Listbox in the lt frame!
		lower = Tk.Frame(outer)
		lower.pack(side="top",anchor="w",padx=20)
		#@nonl
		#@-node:<< create the organizer frames >>
		#@nl
		#@	<< create the font pane >>
		#@+node:<< create the font pane >>
		# Create the list box and its scrollbar.
		self.family_list_box = box = Tk.Listbox(lt,height=7)
		
		# Fill the listbox to set the width.
		names = tkFont.families()
		names = list(names)
		names.sort()
		for name in names:
			box.insert("end", name)
		
		box.pack(padx=4,pady=4,fill="both",expand=1)
		box.bind("<Double-Button-1>", self.update)
		
		bar = Tk.Scrollbar(box)
		bar.pack(side="right", fill="y")
		
		bar.config(command=box.yview)
		box.config(yscrollcommand=bar.set)
		#@nonl
		#@-node:<< create the font pane >>
		#@nl
		#@	<< create the checkboxes >>
		#@+node:<< create the checkboxes >>
		# Create the style checkboxes.
		for text,var in (
			("Bold",self.boldVar),
			("Italic",self.italVar)):
		
			b = Tk.Checkbutton(rt,text=text,variable=var)
			b.pack(side="top",anchor="w")
		
		# Create the size label and entry widget.
		row = Tk.Frame(rt)
		row.pack(side="top")
		
		lab = Tk.Label(row,text="Size:")
		lab.pack(side="left")
		
		self.size_entry = e = Tk.Entry(row,width=4)
		e.pack(side="left")
		e.bind("<Key>",self.onSizeEntryKey)
		
		# Create the pane checkboxes.
		for text,var in (
			("Body",   self.bodyVar),
			("Outline",self.treeVar,),
			("Log",    self.logVar)):
		
			b = Tk.Checkbutton(rt,text=text,variable=var)
			b.pack(side="top",anchor="w")
		#@nonl
		#@-node:<< create the checkboxes >>
		#@nl
		#@	<< create the buttons >>
		#@+node:<< create the buttons >>
		for name,command in (
			("Apply",self.onApply),
			("OK",self.onOk),
			("Cancel",self.onCancel),
			("Revert",self.onRevert)):
				
			b = Tk.Button(lower,width=7,text=name,command=command)
			b.pack(side="left",anchor="w",pady=6,padx=4,expand=0)
		#@nonl
		#@-node:<< create the buttons >>
		#@nl
	#@nonl
	#@-node:create_outer
	#@+node:finishCreate
	def finishCreate (self):
		
		# self.commands.frame.top.resizable(0,0)
		
		# These do not get changed when reverted.
		self.bodyVar.set(1)
		self.logVar.set(0)
		self.treeVar.set(0)
		
		# All other vars do change when reverted.
		self.revertIvars()
		self.update()
	#@nonl
	#@-node:finishCreate
	#@+node:onApply
	def onApply (self):
		
		self.update()
	#@-node:onApply
	#@+node:onCancel
	def onCancel (self):
	
		self.onRevert()
		self.showSettings()
		self.hide()
	#@nonl
	#@-node:onCancel
	#@+node:onOk
	def onOk (self):
	
		c = self.commands
		self.showSettings()
		
		#@	<< update the configuration settings >>
		#@+node:<< update the configuration settings >>
		set = app.config.setWindowPref
		
		fn = c.body.cget("font")
		font = tkFont.Font(font=fn)
		name,size,slant,weight = self.getFontSettings(font)
		set("body_text_font_family",name)
		set("body_text_font_size",size)
		set("body_text_font_slant",slant)
		set("body_text_font_weight",weight)
			
		fn = c.log.cget("font")
		font = tkFont.Font(font=fn)
		name,size,slant,weight = self.getFontSettings(font)
		set("log_text_font_family",name)
		set("log_text_font_size",size)
		set("log_text_font_slant",slant)
		set("log_text_font_weight",weight)
			
		font = c.frame.getFont()
		name,size,slant,weight = self.getFontSettings(font)
		set("headline_text_font_family",name)
		set("headline_text_font_size",size)
		set("headline_text_font_slant",slant)
		set("headline_text_font_weight",weight)
		#@nonl
		#@-node:<< update the configuration settings >>
		#@nl
	
		self.setRevertVars()
		self.hide()
	#@nonl
	#@-node:onOk
	#@+node:onRevert
	def onRevert (self):
	
		c = self.commands
		c.body.configure(font=self.revertBodyFont)
		c.log.configure (font=self.revertLogFont)
		c.frame.setFont (font=self.revertTreeFont)
		c.redraw()
		self.revertIvars()
		# Don't call update here.
	#@nonl
	#@-node:onRevert
	#@+node:selectFont
	def selectFont (self,font):
		
		box = self.family_list_box
		
		# All selections come here.
		self.last_selected_font = font
	
		# The name should be on the list!
		name, size, slant, weight = self.getFontSettings(font)
		for i in xrange(0,box.size()):
			item = box.get(i)
			if name == item:
				box.select_clear(0,"end")
				box.select_set(i)
				box.see(i)
				self.last_selected_font = font
				# trace(name)
				return
		# print "not found:" + name
	#@nonl
	#@-node:selectFont
	#@+node:onSizeEntryKey
	def onSizeEntryKey (self,event=None):
		
		self.size_entry.after_idle(self.idle_entry_key)
		
	def idle_entry_key (self):
		
		size = self.size_entry.get() # Doesn't work until idle time.
		try:
			size = int(size)
			self.sizeVar.set(size)
		except: # The user typed an invalid number.
			return
	#@nonl
	#@-node:onSizeEntryKey
	#@+node:getActiveFont
	#@+at 
	#@nonl
	# Returns a font corresponding to present visual state of the font panel.  
	# As a benign side effect, this routine selects the font in the list box.
	# 
	# Alas, the selection in the list box may have been cleared.  In that 
	# case, we must figure out what it should be. We recreate the family name 
	# (and only the family name!) from self.last_selected_font, or in an 
	# emergency the font returned from getImpliedFont().
	#@-at
	#@@c
	
	def getActiveFont (self):
	
		box = self.family_list_box
		family = font = None
	
		# Get the family name if possible, or font otherwise.
		items = box.curselection()
		if len(items) == 0:
			# Nothing selected.
			if self.last_selected_font:
				font =self.last_selected_font
			else:
				font = self.getImpliedFont()
		else:
			try: # This shouldn't fail now.
				items = map(int, items)
				family = box.get(items[0])
			except:
				es("unexpected exception")
				es_exception()
				font = self.getImpliedFont()
		# At this point we either have family or font.
		assert(font or family)
		if not family:
			# Extract the family from the computed font.
			family,junk,junk,junk = self.getFontSettings(font)
		# At last we have a valid family name!
		# Get all other font settings from the font panel.
		bold = self.boldVar.get()
		ital = self.italVar.get()
		size = self.sizeVar.get()
		# trace(`size`)
		slant=choose(ital,"italic","roman")
		weight=choose(bold,"bold","normal")
		# Compute the font from all the settings.
		font = tkFont.Font(family=family,size=size,slant=slant,weight=weight)
		self.selectFont(font)
		return font
	#@nonl
	#@-node:getActiveFont
	#@+node:getFontSettings
	def getFontSettings (self, font):
	
		name   = font.cget("family")
		size   = font.cget("size")
		slant  = font.cget("slant")
		weight = font.cget("weight")
	
		return name, size, slant, weight
	#@nonl
	#@-node:getFontSettings
	#@+node:getImpliedFont
	# If a single pane's checkbox is checked, select that pane's present font.
	# Otherwise, select the present font of some checked pane, it doesn't much matter which.
	# If none are check, select the body pane's present font.
	
	def getImpliedFont (self):
	
		c = self.commands
	
		body = self.bodyVar.get()
		log  = self.logVar.get()
		tree = self.treeVar.get()
		
		fn = c.body.cget("font")
		bodyFont = tkFont.Font(font=fn)
		fn = c.log.cget("font")
		logFont = tkFont.Font(font=fn)
		treeFont = c.frame.getFont()
		
		if log and not body and not tree:
			font = logFont
		elif tree and not body and not log:
			font = treeFont
		elif body: font = bodyFont
		elif tree: font = treeFont
		elif log:  font = logFont # Exercise for the reader: prove this case will never happen.
		else:      font = bodyFont
		return font
	#@nonl
	#@-node:getImpliedFont
	#@+node:hide
	def hide (self):
		
		"""Hide the font panel."""
		
		c = self.commands
		
		# c.frame.top.resizable(1,1)
		
		if 1: # Hide the window, preserving its position.
			self.top.withdraw()
		else: # works.
			c.frame.fontPanel=None
			self.top.destroy()
	#@nonl
	#@-node:hide
	#@+node:revertIvars
	def revertIvars (self):
		
		c = self.commands
		# Revert the fonts themselves in the various panes.
		font = self.revertBodyFont
		c.body.configure(font=font)
		font = self.revertLogFont
		c.log.configure(font=font)
		font = self.revertTreeFont
		c.frame.setFont(font=font)
		# Revert the setting of the items in the font panel
		self.last_selected_font = None # Use the font for the selected panes.
		font = self.getImpliedFont()
		self.selectFont(font)
		try:
			name, size, slant, weight = self.getFontSettings(font)
			size=int(size)
		except: pass
		self.sizeVar.set(size)
		self.boldVar.set(choose(weight=="bold",1,0))
		self.italVar.set(choose(slant=="italic",1,0))
		
		e = self.size_entry
		e.delete(0,"end")
		e.insert(0,`size`)
	#@nonl
	#@-node:revertIvars
	#@+node:run
	def run (self):
		
		Tk = Tkinter ; c = self.commands
		self.top = top = Tk.Toplevel(app.root)
		attachLeoIcon(top)
		top.title("Fonts for " + shortFileName(c.frame.title))
		top.protocol("WM_DELETE_WINDOW", self.onOk)
		self.create_outer()
		
		# This must be done _after_ the dialog has been built!
		w,h,x,y = center_dialog(top)
		top.wm_minsize(height=h,width=w)
		
		# Finish up after the dialog is frozen.
		self.outer.after_idle(self.finishCreate)
	
		if 0: # The pane now looks decent when resized!
			top.resizable(0,0)
	
		# Bring up the dialog.
		if 0: # It need not be modal: it will go away if the owning window closes!
			top.grab_set()
			top.focus_set() # Get all keystrokes.
	#@nonl
	#@-node:run
	#@+node:setRevertVars
	def setRevertVars (self):
		
		c = self.commands
		
		# Variables for revert.
		fn = c.body.cget("font")
		self.revertBodyFont = tkFont.Font(font=fn)
		
		fn = c.log.cget("font")
		self.revertLogFont = tkFont.Font(font=fn)
		
		self.revertTreeFont = c.frame.getFont()
	#@nonl
	#@-node:setRevertVars
	#@+node:showSettings
	# Write all settings to the log panel.
	# Note that just after a revert all three setting may be different.
	
	def showSettings (self):
		c = self.commands
		es("---------------")
		# Body pane.
		fn = c.body.cget("font")
		font = tkFont.Font(font=fn)
		name,size,slant,weight = self.getFontSettings(font)
		es("body font:" + name + "," + `size` + "," + slant + "," + weight)
		# Log pane.
		fn = c.log.cget("font")
		font = tkFont.Font(font=fn)
		name,size,slant,weight = self.getFontSettings(font)
		es("log font:" + name + "," + `size` + "," + slant + "," + weight)
		# Tree pane.
		font = c.frame.getFont()
		name,size,slant,weight = self.getFontSettings(font)
		es("headline font:" + name + "," + `size` + "," + slant + "," + weight)
	#@nonl
	#@-node:showSettings
	#@+node:update
	def update (self,event=None):
		
		"""Update the body text to show the present settings."""
		
		c = self.commands
		size = self.sizeVar.get()
		#@	<< insert the new text in the size box >>
		#@+node:<< insert the new text in the size box >>
		e = self.size_entry
		e.delete(0,"end")
		e.insert(0,`size`)
		#@nonl
		#@-node:<< insert the new text in the size box >>
		#@nl
		activeFont = self.getActiveFont()
		bodyChecked = self.bodyVar.get()
		logChecked = self.logVar.get()
		treeChecked = self.treeVar.get()
	
		if not bodyChecked and not logChecked and not treeChecked:
			es("no pane selected")
			return
		
	
		# c.frame.body.configure(setgrid=0) # Disable body resizes.
		c.beginUpdate()
		#@	<< set the fonts in all panes >>
		#@+node:<< set the fonts in all panes >>
		font = choose(bodyChecked,activeFont,self.revertBodyFont)
		c.body.configure(font=font)
		
		font = choose(logChecked,activeFont,self.revertLogFont)
		c.log.configure(font=font)
		
		font = choose(treeChecked,activeFont,self.revertTreeFont)
		c.frame.setFont(font=font)
		#@nonl
		#@-node:<< set the fonts in all panes >>
		#@nl
		c.endUpdate()
		# c.frame.body.configure(setgrid=1) # Enable body resizes.
	
		self.top.deiconify()
		self.top.lift()
	#@nonl
	#@-node:update
	#@-others
	
class leoFontPanel (baseLeoFontPanel):
	"""A class that creates Leo's font panel."""
	pass
#@nonl
#@-node:@file leoFontPanel.py
#@-leo
