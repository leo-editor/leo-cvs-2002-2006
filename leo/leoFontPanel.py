#@+leo
#@+node:0::@file leoFontPanel.py
#@+body
#@@language python

from leoGlobals import *
import exceptions,sys,string,Tkinter,tkFont

class leoFontPanel:

	#@+others
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
		
			b = Tk.Checkbutton(rt,text=text,variable=var,command=self.update)
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
		for text,var,command in (
			("Body",self.bodyVar,self.onBodyBoxChanged),
			("Outline",self.treeVar,self.onTreeBoxChanged),
			("Log",self.logVar,self.onLogBoxChanged)):
				
			b = Tk.Checkbutton(rt,text=text,variable=var,command=command)
			b.pack(side="top",anchor="w")
		#@-body
		#@-node:3::<< create the checkboxes >>

		
		#@<< create Ok, Cancel and Revert buttons >>
		#@+node:4::<< create Ok, Cancel and Revert buttons >>
		#@+body
		for name,command in (
			("OK",self.onOk),
			("Cancel",self.onCancel),
			("Revert",self.onRevert)):
				
			b = Tk.Button(lower,width=7,text=name,command=command)
			b.pack(side="left",anchor="w",pady=6,padx=4,expand=0) #,fill="y")
		#@-body
		#@-node:4::<< create Ok, Cancel and Revert buttons >>
	#@-body
	#@-node:2::create_outer
	#@+node:3::finishCreate
	#@+body
	def finishCreate (self):
		
		# These do not get changed when reverted.
		self.bodyVar.set(1)
		self.logVar.set(0)
		self.treeVar.set(0)
		
		# All other vars do change when reverted.
		self.revertIvars()
		self.update()
	
	#@-body
	#@-node:3::finishCreate
	#@+node:4::getActiveFont
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
	#@-node:4::getActiveFont
	#@+node:5::getFontSettings
	#@+body
	def getFontSettings (self, font):
	
		name   = font.cget("family")
		size   = font.cget("size")
		slant  = font.cget("slant")
		weight = font.cget("weight")
	
		return name, size, slant, weight
	#@-body
	#@-node:5::getFontSettings
	#@+node:6::getImpliedFont
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
	#@-node:6::getImpliedFont
	#@+node:7::on...BoxChanged
	#@+body
	#@+at
	#  We define these routines so that changing one pane box affects only 
	# that pane.
	# 
	# When we turn a box on, we expect that the present font will instantly 
	# apply to the new pane, and when we turn a box off we call implied font 
	# to see which font should be highlighted and we revert the pane's font. 
	# It is crucial that unchecking a box be equivalent to a "small revert".  
	# This is the _only_ scheme that isn't confusing to the user.
	# 
	# Note: if we just called update instead of these routines we could do 
	# something unexpected after after a revert.  For example, suppose all 
	# three pane boxes are checked and we do a revert.  If we then uncheck a 
	# box, we expect only that pane to change, but if we call update the other 
	# two panes might also change...

	#@-at
	#@@c
	def onBodyBoxChanged(self):
		font = choose(self.bodyVar.get(),
			self.getActiveFont(),self.revertBodyFont)
		self.commands.body.configure(font=font)
	
	def onLogBoxChanged(self):
		font = choose(self.logVar.get(),
			self.getActiveFont(),self.revertLogFont)
		self.commands.log.configure(font=font)
			
	def onTreeBoxChanged(self):
		c = self.commands
		font = choose(self.treeVar.get(),
			self.getActiveFont(),self.revertTreeFont)
		c.tree.setFont(font=font)
		c.redraw()
	#@-body
	#@-node:7::on...BoxChanged
	#@+node:8::leoFont.onOk, onCancel, onRevert
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
		if 1: # Hide the window, preserving its position.
			self.top.withdraw()
		else: # works.
			self.commands.frame.fontPanel=None
			self.top.destroy()
	
	def onCancel (self):
		c = self.commands
		self.onRevert()
		self.showSettings()
		if 1: # Hide the window, preserving its position.
			self.top.withdraw()
		else: # works.
			c.frame.fontPanel=None
			self.top.destroy()
		
	def onRevert (self):
		c = self.commands
		c.body.configure(font=self.revertBodyFont)
		c.log.configure (font=self.revertLogFont)
		c.tree.setFont  (font=self.revertTreeFont)
		c.redraw()
		self.revertIvars()
		# Don't call update here.
	#@-body
	#@-node:8::leoFont.onOk, onCancel, onRevert
	#@+node:9::onSizeEntryKey
	#@+body
	def onSizeEntryKey (self,event=None):
		
		self.size_entry.after_idle(self.idle_entry_key)
		
	def idle_entry_key (self):
		
		size = self.size_entry.get() # Doesn't work until idle time.
		try:
			size = int(size)
		except: # This just means the user didn't type a valid number.
			return
		# trace(`size`)
		self.sizeVar.set(size)
		if 0 < size < 100: # Choosing very small or large fonts drives Tk crazy.
			self.update()
	#@-body
	#@-node:9::onSizeEntryKey
	#@+node:10::revertIvars
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
	#@-node:10::revertIvars
	#@+node:11::run
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
	#@-node:11::run
	#@+node:12::selectFont
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
	#@-node:12::selectFont
	#@+node:13::setRevertVars
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
	#@-node:13::setRevertVars
	#@+node:14::showSettings
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
	#@-node:14::showSettings
	#@+node:15::update
	#@+body
	# Updates size box and example box when something changes.
	
	def update (self,event=None):
		
		c = self.commands
		size = self.sizeVar.get()
		
		# Insert the new text in the size box.
		e = self.size_entry
		e.delete(0,"end")
		e.insert(0,`size`)
		
		font = self.getActiveFont()
		
		if not self.bodyVar.get() and not self.logVar.get() and not self.treeVar.get():
			es("no pane selected")
	
		f = choose(self.bodyVar.get(),font,self.revertBodyFont)
		self.commands.body.configure(font=f)
		
		f = choose(self.logVar.get(),font,self.revertLogFont)
		self.commands.log.configure(font=f)
		
		f = choose(self.treeVar.get(),font,self.revertTreeFont)
		c.tree.setFont(font=f)
		c.redraw()
	#@-body
	#@-node:15::update
	#@-others
#@-body
#@-node:0::@file leoFontPanel.py
#@-leo
