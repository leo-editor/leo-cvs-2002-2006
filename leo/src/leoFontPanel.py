#@+leo
#@+node:0::@file leoFontPanel.py
#@+body
#@@language python

from leoGlobals import *
import exceptions,sys,string,Tkinter,tkFont

class baseLeoFontPanel:
	"""The base class for Leo's font panel."""

	#@+others
	#@+node:1::Birth & Death
	#@+node:1::fontPanel.__init__
	#@+body
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
	#@-body
	#@-node:1::fontPanel.__init__
	#@+node:2::create_outer
	#@+body
	def create_outer(self):
	
		Tk = Tkinter
		top = self.top
		
		#@<< Create the organizer frames >>
		#@+node:1::<< create the organizer frames >>
		#@+body
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
		#@-body
		#@-node:1::<< create the organizer frames >>

		
		#@<< create the font pane >>
		#@+node:2::<< create the font pane >>
		#@+body
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
		#@-body
		#@-node:2::<< create the font pane >>

		
		#@<< create the checkboxes >>
		#@+node:3::<< create the checkboxes >>
		#@+body
		# Create the style checkboxes.
		for text,var in (
			("Bold",self.boldVar),
			("Italic",self.italVar)):
		
			b = Tk.Checkbutton(rt,text=text,variable=var) # ,command=self.update)
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
		#@-body
		#@-node:3::<< create the checkboxes >>

		
		#@<< create the buttons >>
		#@+node:4::<< create the buttons >>
		#@+body
		for name,command in (
			("Apply",self.onApply),
			("OK",self.onOk),
			("Cancel",self.onCancel),
			("Revert",self.onRevert)):
				
			b = Tk.Button(lower,width=7,text=name,command=command)
			b.pack(side="left",anchor="w",pady=6,padx=4,expand=0)
		#@-body
		#@-node:4::<< create the buttons >>
	#@-body
	#@-node:2::create_outer
	#@+node:3::finishCreate
	#@+body
	def finishCreate (self):
		
		# self.commands.frame.top.resizable(0,0)
		
		# These do not get changed when reverted.
		self.bodyVar.set(1)
		self.logVar.set(0)
		self.treeVar.set(0)
		
		# All other vars do change when reverted.
		self.revertIvars()
		self.update()
	#@-body
	#@-node:3::finishCreate
	#@-node:1::Birth & Death
	#@+node:2::Buttons
	#@+node:1::onApply
	#@+body
	def onApply (self):
		
		self.update()
	
	#@-body
	#@-node:1::onApply
	#@+node:2::onCancel
	#@+body
	def onCancel (self):
	
		c = self.commands
		self.onRevert()
		self.showSettings()
		self.hide()
	#@-body
	#@-node:2::onCancel
	#@+node:3::onOk
	#@+body
	def onOk (self):
	
		c = self.commands
		self.showSettings()
		
		
		#@<< update the configuration settings >>
		#@+node:1::<< update the configuration settings >>
		#@+body
		set = app().config.setWindowPref
		
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
			
		font = c.tree.getFont()
		name,size,slant,weight = self.getFontSettings(font)
		set("headline_text_font_family",name)
		set("headline_text_font_size",size)
		set("headline_text_font_slant",slant)
		set("headline_text_font_weight",weight)
		#@-body
		#@-node:1::<< update the configuration settings >>

	
		self.setRevertVars()
		self.hide()
	#@-body
	#@-node:3::onOk
	#@+node:4::onRevert
	#@+body
	def onRevert (self):
	
		c = self.commands
		c.body.configure(font=self.revertBodyFont)
		c.log.configure (font=self.revertLogFont)
		c.tree.setFont  (font=self.revertTreeFont)
		c.redraw()
		self.revertIvars()
		# Don't call update here.
	#@-body
	#@-node:4::onRevert
	#@-node:2::Buttons
	#@+node:3::Events
	#@+node:1::selectFont
	#@+body
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
	#@-body
	#@-node:1::selectFont
	#@+node:2::onSizeEntryKey
	#@+body
	def onSizeEntryKey (self,event=None):
		
		self.size_entry.after_idle(self.idle_entry_key)
		
	def idle_entry_key (self):
		
		size = self.size_entry.get() # Doesn't work until idle time.
		try:
			size = int(size)
			self.sizeVar.set(size)
		except: # The user typed an invalid number.
			return
	
		if 0: # This is too upsetting.
			# trace(`size`)
			if 0 < size < 100: # Choosing very small or large fonts drives Tk crazy.
				self.update()
	#@-body
	#@-node:2::onSizeEntryKey
	#@-node:3::Events
	#@+node:4::Helpers
	#@+node:1::getActiveFont
	#@+body
	#@+at
	#  Returns a font corresponding to present visual state of the font 
	# panel.  As a benign side effect, this routine selects the font in the 
	# list box.
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
	#@-body
	#@-node:1::getActiveFont
	#@+node:2::getFontSettings
	#@+body
	def getFontSettings (self, font):
	
		name   = font.cget("family")
		size   = font.cget("size")
		slant  = font.cget("slant")
		weight = font.cget("weight")
	
		return name, size, slant, weight
	#@-body
	#@-node:2::getFontSettings
	#@+node:3::getImpliedFont
	#@+body
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
		treeFont = c.tree.getFont()
		
		if log and not body and not tree:
			font = logFont
		elif tree and not body and not log:
			font = treeFont
		elif body: font = bodyFont
		elif tree: font = treeFont
		elif log:  font = logFont # Exercise for the reader: prove this case will never happen.
		else:      font = bodyFont
		return font
	#@-body
	#@-node:3::getImpliedFont
	#@+node:4::hide
	#@+body
	def hide (self):
		
		"""Hide the font panel."""
		
		c = self.commands
		
		# c.frame.top.resizable(1,1)
		
		if 1: # Hide the window, preserving its position.
			self.top.withdraw()
		else: # works.
			c.frame.fontPanel=None
			self.top.destroy()
	#@-body
	#@-node:4::hide
	#@+node:5::revertIvars
	#@+body
	def revertIvars (self):
		
		c = self.commands
		# Revert the fonts themselves in the various panes.
		font = self.revertBodyFont
		c.body.configure(font=font)
		font = self.revertLogFont
		c.log.configure(font=font)
		font = self.revertTreeFont
		c.tree.setFont(font=font)
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
	#@-body
	#@-node:5::revertIvars
	#@+node:6::run
	#@+body
	def run (self):
		
		Tk = Tkinter ; c = self.commands
		self.top = top = Tk.Toplevel(app().root)
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
			top.focus_force() # Get all keystrokes.
	#@-body
	#@-node:6::run
	#@+node:7::setRevertVars
	#@+body
	def setRevertVars (self):
		
		c = self.commands
		
		# Variables for revert.
		fn = c.body.cget("font")
		self.revertBodyFont = tkFont.Font(font=fn)
		
		fn = c.log.cget("font")
		self.revertLogFont = tkFont.Font(font=fn)
		
		self.revertTreeFont = c.tree.getFont()
	#@-body
	#@-node:7::setRevertVars
	#@+node:8::showSettings
	#@+body
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
		font = c.tree.getFont()
		name,size,slant,weight = self.getFontSettings(font)
		es("headline font:" + name + "," + `size` + "," + slant + "," + weight)
	#@-body
	#@-node:8::showSettings
	#@+node:9::update
	#@+body
	def update (self,event=None):
		
		"""Update the body text to show the present settings."""
		
		c = self.commands
		size = self.sizeVar.get()
		
		#@<< insert the new text in the size box >>
		#@+node:1::<< insert the new text in the size box >>
		#@+body
		e = self.size_entry
		e.delete(0,"end")
		e.insert(0,`size`)
		#@-body
		#@-node:1::<< insert the new text in the size box >>

		activeFont = self.getActiveFont()
		bodyChecked = self.bodyVar.get()
		logChecked = self.logVar.get()
		treeChecked = self.treeVar.get()
	
		if not bodyChecked and not logChecked and not treeChecked:
			es("no pane selected")
			return
	
		c.frame.body.configure(setgrid=0) # Disable body resizes.
		c.beginUpdate()
		
		#@<< set the fonts in all panes >>
		#@+node:2::<< set the fonts in all panes >>
		#@+body
		font = choose(bodyChecked,activeFont,self.revertBodyFont)
		c.body.configure(font=font)
		
		font = choose(logChecked,activeFont,self.revertLogFont)
		c.log.configure(font=font)
		
		font = choose(treeChecked,activeFont,self.revertTreeFont)
		c.tree.setFont(font=font)
		#@-body
		#@-node:2::<< set the fonts in all panes >>

		c.endUpdate()
		c.frame.body.configure(setgrid=1) # Enable body resizes.
		self.top.deiconify()
		self.top.lift()
	#@-body
	#@-node:9::update
	#@-node:4::Helpers
	#@-others

	
class leoFontPanel (baseLeoFontPanel):
	"""A class that creates Leo's font panel."""
	pass
#@-body
#@-node:0::@file leoFontPanel.py
#@-leo
