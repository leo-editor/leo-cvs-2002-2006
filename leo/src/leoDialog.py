#@+leo
#@+node:0::@file leoDialog.py
#@+body
#@@language python

from leoGlobals import *
import string,Tkinter

Tk = Tkinter

## To do:
##		make leoDialog useful as a base class.
##		derive listBoxDialog from leoDialog.

class leoDialog:
	
	#@<< leoDialog methods >>
	#@+node:1::<< leoDialog methods >>
	#@+body
	#@+others
	#@+node:1::dialog.center
	#@+body
	def center(self):
		
		center_dialog(self.top)
		return
	#@-body
	#@-node:1::dialog.center
	#@+node:2::Event handlers & command handlers
	#@+node:1::OnCloseLeoIDWindow
	#@+body
	def OnCloseLeoIDWindow (self):
		
		# We disallow this window to be closed.
		pass
	#@-body
	#@-node:1::OnCloseLeoIDWindow
	#@+node:2::cancelButton, noButton, okButton, yesButton
	#@+body
	# Command handlers.
	
	def cancelButton(self):
		self.answer="cancel"
		self.top.destroy() # terminates wait_window
		
	def noButton(self):
		self.answer="no"
		self.top.destroy() # terminates wait_window
		
	def okButton(self):
		self.answer="ok"
		self.top.destroy() # terminates wait_window
	
	def yesButton(self):
		self.answer="yes"
		self.top.destroy() # terminates wait_window
	#@-body
	#@-node:2::cancelButton, noButton, okButton, yesButton
	#@+node:3::okLeoIDButton, okNumberButton, cancelNumberButton
	#@+body
	def okLeoIDButton(self):
		s = self.id_entry.get().strip()
		if len(s) < 4:  # Require at least 4 characters in an id.
			return
		self.leoID = s
		self.top.destroy() # terminates wait_window
	
	def okNumberButton(self):
		s = self.number_entry.get().strip()
		try:
			self.number=int(s)
		except:
			self.number=-1 # Cancel the operation.
		self.top.destroy() # terminates wait_window
		
	def cancelButton(self):
		self.number=-1
		self.top.destroy() # terminates wait_window
	#@-body
	#@-node:3::okLeoIDButton, okNumberButton, cancelNumberButton
	#@+node:4::On...Key
	#@+body
	def OnOkCancelKey(self,event):
		ch=string.lower(event.char)
		if ch=='\n' or ch=='\r': self.okButton() # The default
		elif ch=='c': self.cancelButton()
		elif ch=='o': self.okButton()
		return "break"
	
	def OnYesNoKey(self,event):
		ch=string.lower(event.char)
		if ch=='\n' or ch=='\r': self.yesButton() # The default
		elif ch=='n': self.noButton()
		elif ch=='y': self.yesButton()
		return "break"
		
	def OnYesNoCancelKey(self,event):
		ch=string.lower(event.char)
		if ch=='\n' or ch=='\r': self.yesButton() # The default
		elif ch=='c': self.cancelButton()
		elif ch=='n': self.noButton()
		elif ch=='y': self.yesButton()
		return "break"
		
	def OnOkCancelNumberKey(self,event):
		
		#@<< eliminate non-numbers >>
		#@+node:1::<< eliminate non-numbers >>
		#@+body
		e = self.number_entry
		s = e.get().strip()
		i = 0 ; ok = true
		while i < len(s):
			ch = s[i]
			if ch not in string.digits:
				e.delete(`i`)
				s = e.get()
				ok = false
			else:
				i += 1
		if not ok: return
		#@-body
		#@-node:1::<< eliminate non-numbers >>

		ch=string.lower(event.char)
		if ch=='\n' or ch=='\r': self.okNumberButton() # The default
		elif ch=='c': self.cancelButton()
		elif ch=='o': self.okNumberButton()
		return "break"
		
	def OnLeoIDKey(self,event):
		
		#@<< eliminate invalid characters >>
		#@+node:2::<< eliminate invalid characters >>
		#@+body
		e = self.id_entry
		s = e.get().strip()
		i = 0 ; ok = true
		while i < len(s):
			ch = s[i]
			if ch not in string.letters and ch not in string.digits:
				e.delete(`i`)
				s = e.get()
				ok = false
			else:
				i += 1
		if not ok: return
		#@-body
		#@-node:2::<< eliminate invalid characters >>

		
		#@<< enable the ok button if there are 4 or more valid characters >>
		#@+node:3::<< enable the ok button if there are 4 or more valid characters >>
		#@+body
		e = self.id_entry
		b = self.ok_button
		if len(e.get().strip()) >= 4:
			b.configure(state="normal")
		else:
			b.configure(state="disabled")
		#@-body
		#@-node:3::<< enable the ok button if there are 4 or more valid characters >>

		ch=string.lower(event.char)
		if ch=='\n' or ch=='\r': self.okLeoIDButton() # The default
		return "break"
	#@-body
	#@-node:4::On...Key
	#@+node:5::setArrowCursor, setDefaultCursor
	#@+body
	def setArrowCursor (self,event=None):
		
		if self.text:
			self.text.configure(cursor="arrow")
		
	def setDefaultCursor (self,event=None):
		
		if self.text:
			self.text.configure(cursor="xterm")
	#@-body
	#@-node:5::setArrowCursor, setDefaultCursor
	#@-node:2::Event handlers & command handlers
	#@+node:3::dialog.__init__
	#@+body
	def __init__(self):
	
		self.answer = ""
		self.number = -1
		self.top = None
		self.email = None
		self.url = None
		self.text = None
	#@-body
	#@-node:3::dialog.__init__
	#@+node:4::aboutLeo
	#@+body
	def aboutLeo(self, version, copyright, url, email):
	
		Tk = Tkinter ; root = app().root
		self.top = top = Tk.Toplevel(root)
		self.url = url
		self.email = email
	
		top.title("About Leo")
		frame = Tk.Frame(top)
		
		# Calculate the approximate height & width. (There are bugs in Tk here.)
		lines = string.split(copyright,'\n')
		height = len(lines) + 8 # Add lines for version,url,email,spacing.
		width = 0
		for line in lines:
			width = max(width,len(line))
		width = max(width,len(url))
		width += 10 # 9/9/02
	
		frame.pack(padx=6,pady=4)
		
		self.text = text = Tk.Text(frame,height=height,width=width,bd=0,bg=frame.cget("background"))
		text.pack(pady=10)
		
		try:
			bitmap_name = os.path.join(app().loadDir,"..","Icons","Leoapp.GIF") # 5/12/03
			image = Tkinter.PhotoImage(file=bitmap_name)
			text.image_create("1.0",image=image,padx=10)
		except:
			es("exception getting icon")
			es_exception()
	
		text.insert("end",version,"version")
		text.insert("end",copyright,"copyright")
		text.insert("end",'\n')
		text.insert("end",url,"url") # Add "url" tag.
		text.insert("end",'\n')
		text.insert("end",email,"email") # Add "email" tag.
		
		text.tag_config("version",justify="center")
		text.tag_config("copyright",justify="center",spacing1="3")
		
		text.tag_config("url",underline=1,justify="center",spacing1="10")
		text.tag_bind("url","<Button-1>",self.onAboutLeoUrl)
		text.tag_bind("url","<Enter>",self.setArrowCursor)
		text.tag_bind("url","<Leave>",self.setDefaultCursor)
	
		text.tag_config("email",underline=1,justify="center",spacing1="10")
		text.tag_bind("email","<Button-1>",self.onAboutLeoEmail)
		text.tag_bind("email","<Enter>",self.setArrowCursor)
		text.tag_bind("email","<Leave>",self.setDefaultCursor)
	
		text.configure(state="disabled")
	
		self.center() # Do this after packing.
		top.resizable(0,0) # neither height or width is resizable.
		if 0: # No need to make this modal
			top.grab_set() # Make the dialog a modal dialog.
			top.focus_force() # Get all keystrokes.
		root.wait_window(top)
	#@-body
	#@+node:1::onAboutLeoUrl
	#@+body
	def onAboutLeoUrl(self,event=None):
	
		try:
			import webbrowser
			webbrowser.open(self.url)
		except:
			es("not found: " + self.url)
	#@-body
	#@-node:1::onAboutLeoUrl
	#@+node:2::onAboutLeoEmail
	#@+body
	def onAboutLeoEmail(self,event=None):
		
		try:
			import webbrowser
			webbrowser.open("mailto:" + self.email)
		except:
			es("not found: " + self.email)
	#@-body
	#@-node:2::onAboutLeoEmail
	#@-node:4::aboutLeo
	#@+node:5::askOk
	#@+body
	def askOk(self, title, message, text="OK"):
	
		Tk = Tkinter ; root = app().root
		self.answer="ok"
		self.top = top = Tk.Toplevel(root)
		attachLeoIcon(self.top)
		top.title(title)
		top.resizable(0,0) # neither height or width is resizable.
		frame = Tk.Frame(top)
		if text=="OK":
			self.top.bind("<Key>", self.OnOkCancelKey)
		frame.pack(padx=6,pady=4)
		label = Tk.Label(frame, text=message)
		label.pack(pady=10)
		center = Tk.Frame(frame)
		center.pack()
		underline = choose(text=="OK",0,-1) # Underline character 0 if "OK", else no underlining.
		ok = Tk.Button(center,width=6,text=text,bd=4, # bd=4 represents default button
			underline=underline,command=self.okButton)
		ok.pack(side="left",padx=5,pady=10)
		self.center() # Do this after packing.
		top.grab_set() # Make the dialog a modal dialog.
		top.focus_force() # Get all keystrokes.
		root.wait_window(top)
	#@-body
	#@-node:5::askOk
	#@+node:6::askOkCancel
	#@+body
	def askOkCancel(self, title, message):
	
		Tk = Tkinter ; root = app().root
		self.answer="ok"
		self.top = top = Tk.Toplevel(root)
		attachLeoIcon(self.top)
		top.title(title)
		top.resizable(0,0) # neither height or width is resizable.
		frame = Tk.Frame(top)
		self.top.bind("<Key>", self.OnOkCancelKey)
		frame.pack(padx=6,pady=4)
		label = Tk.Label(frame, text=message)
		label.pack(pady=10)
		center = Tk.Frame(frame)
		center.pack()
		ok = Tk.Button(center,width=6,text="OK",bd=4, # default button
			underline=0,command=self.okButton)
		cancel = Tk.Button(center,width=6,text="Cancel",
			underline=0,command=self.cancelButton)
		ok.pack(side="left",padx=5,pady=10)
		cancel.pack(side="left",padx=5,pady=10)
		self.center() # Do this after packing.
		top.grab_set() # Make the dialog a modal dialog.
		top.focus_force() # Get all keystrokes.
		root.wait_window(top)
		return self.answer
	#@-body
	#@-node:6::askOkCancel
	#@+node:7::askOkCancelNumber
	#@+body
	def askOkCancelNumber(self,title,message):
	
		Tk = Tkinter ; root = app().root
		self.number=-1
		self.top = top = Tk.Toplevel(root)
		attachLeoIcon(self.top)
		top.title(title)
		top.resizable(0,0) # neither height or width is resizable.
		frame = Tk.Frame(top)
		self.top.bind("<Key>", self.OnOkCancelNumberKey) # 1/30/03
		frame.pack(padx=6,pady=4)
		label = Tk.Label(frame,text=message)
		label.pack(pady=10,side="left")
		self.number_entry = txt = Tk.Entry(frame,width=10)
		txt.pack(side="left")
	
		center = Tk.Frame(top)
		center.pack(side="top",padx=30)
		ok = Tk.Button(center,width=6,text="OK",bd=4, # default button
			underline=0,command=self.okNumberButton)
		cancel = Tk.Button(center,width=6,text="Cancel",
			underline=0,command=self.cancelButton)
		ok.pack(side="left",padx=5,pady=10)
		cancel.pack(side="left",padx=5,pady=10)
		self.center() # Do this after packing.
		top.grab_set() # Make the dialog a modal dialog.
		txt.focus_force() # Get all keystrokes.
		root.wait_window(top)
		return self.number
	#@-body
	#@-node:7::askOkCancelNumber
	#@+node:8::askLeoID
	#@+body
	def askLeoID(self,title,message):
	
		Tk = Tkinter ; root = app().root
		self.leoID=None
		self.top = top = Tk.Toplevel(root)
		self.top.protocol("WM_DELETE_WINDOW", self.OnCloseLeoIDWindow)
		attachLeoIcon(self.top)
		top.title(title)
		top.resizable(0,0) # neither height or width is resizable.
		frame = Tk.Frame(top)
		self.top.bind("<Key>", self.OnLeoIDKey) # 1/30/03
		frame.pack(padx=6,pady=4)
		label = Tk.Label(frame,text=message)
		label.pack(pady=10)
		self.id_entry = txt = Tk.Entry(frame,width=10)
		txt.pack()
	
		center = Tk.Frame(top)
		center.pack(side="top",padx=30)
		self.ok_button = ok = Tk.Button(center,width=6,text="OK",bd=4, # default button
			underline=0,command=self.okLeoIDButton,state="disabled")
		ok.pack(side="left",padx=5,pady=10)
		self.center() # Do this after packing.
		top.grab_set() # Make the dialog a modal dialog.
		txt.focus_force() # Get all keystrokes.
		root.wait_window(top)
		return self.leoID
	#@-body
	#@-node:8::askLeoID
	#@+node:9::askYesNo
	#@+body
	def askYesNo(self, title, message):
	
		Tk = Tkinter ; root = app().root
		self.answer="No"
		self.top = top = Tk.Toplevel(root)
		attachLeoIcon(self.top)
		top.title(title)
		top.resizable(0,0) # neither height or width is resizable.
		frame = Tk.Frame(top)
		self.top.bind("<Key>", self.OnYesNoKey)
		frame.pack(padx=6,pady=4)
		label = Tk.Label(frame, text=message)
		label.pack(pady=10)
		center = Tk.Frame(frame)
		center.pack()
		yes = Tk.Button(center,width=6,text="Yes",bd=4, # default button
			underline=0,command=self.yesButton)
		no = Tk.Button(center,width=6,text="No",
			underline=0,command=self.noButton)
		yes.pack(side="left",padx=5,pady=10)
		no.pack(side="left",padx=5,pady=10)
		self.center() # Do this after packing.
		top.grab_set() # Make the dialog a modal dialog.
		top.focus_force() # Get all keystrokes.
		root.wait_window(top)
		return self.answer
	#@-body
	#@-node:9::askYesNo
	#@+node:10::askYesNoCancel
	#@+body
	def askYesNoCancel(self, title, message,
		yesMessage = "Yes", noMessage = "No", defaultButton = "Yes"):
	
		Tk = Tkinter ; root = app().root
		self.answer="cancel"
		self.top = top = Tk.Toplevel(root)
		attachLeoIcon(self.top)
		top.title(title)
		top.resizable(0,0) # neither height or width is resizable.
		frame = Tk.Frame(top)
		self.top.bind("<Key>", self.OnYesNoCancelKey)
		frame.pack(padx=6,pady=4)
		label = Tk.Label(frame, text=message)
		label.pack(pady=10)
		center = Tk.Frame(frame)
		center.pack()
		yes = Tk.Button(center,width=6,text=yesMessage,
			underline=0,command=self.yesButton)
		no = Tk.Button(center,width=6,text=noMessage,
			underline=0,command=self.noButton)
		cancel = Tk.Button(center,width=6,text="Cancel",
			underline=0,command=self.cancelButton)
		if 0: # not ready for prime time.
			for button,s in ((yes,"Yes"),(no,"No"),(cancel,"Cancel")):
				if defaultButton == s:
					button.configure(bd=4)  # make it the default button
		yes.pack(side="left",padx=5,pady=10)
		no.pack(side="left",padx=5,pady=10)
		cancel.pack(side="left",padx=5,pady=10)
		self.center() # Do this after packing.
		top.grab_set() # Make the dialog a modal dialog.
		top.focus_force() # Get all keystrokes.
		root.wait_window(top)
		return self.answer
	#@-body
	#@-node:10::askYesNoCancel
	#@-others
	
	#@-body
	#@-node:1::<< leoDialog methods >>

	
class listBoxDialog:
	
	#@<< listBoxDialog methods >>
	#@+node:2::<< listboxDialog methods >>
	#@+body
	#@+others
	#@+node:1::listboxDialog.__init__
	#@+body
	def __init__ (self,c,label):
	
		# trace(`label`)
	
		# Initialize common ivars.
		self.c = c
		self.label = label
		self.vnodeList = []
		self.vnodeList = []
		self.buttonFrame = None
	
		# Create the toplevel.
		self.root = root = app().root
		self.top = top = Tk.Toplevel(root)
		attachLeoIcon(top)
		top.title("")
		
		# Fill in the frame.
		self.createFrame()
		self.fillbox()
		
		# Make the common bindings after creating self.box.
		self.top.protocol("WM_DELETE_WINDOW", self.destroy)
		self.box.bind("<Double-Button-1>",self.go)
	
	#@-body
	#@-node:1::listboxDialog.__init__
	#@+node:2::addStdButtons
	#@+body
	def addStdButtons (self,frame):
		
		"""Add buttons to self.buttonFrame"""
		
		# Create the ok and cancel buttons.
		self.ok = ok = Tk.Button(frame,text="Go",width=6,command=self.go)
		self.hide = hide = Tk.Button(frame,text="Hide",width=6,command=self.hide)
	
		ok.pack(side="left",pady=2,padx=5)
		hide.pack(side="left",pady=2,padx=5)
	#@-body
	#@-node:2::addStdButtons
	#@+node:3::createFrame
	#@+body
	def createFrame(self):
		
		"""Create the essentials of a listBoxDialog frame
		
		Subclasses will add buttons to self.buttonFrame"""
		
		self.outerFrame = f = Tk.Frame(self.top)
		f.pack(expand=1,fill="both")
		
		if self.label:
			labf = Tk.Frame(f)
			labf.pack(pady=2)
			lab = Tk.Label(labf,text=self.label)
			lab.pack()
		
		f2 = Tk.Frame(f)
		f2.pack(expand=1,fill="both")
		
		self.box = box = Tk.Listbox(f2,height=20,width = 20)
		box.pack(side="left",expand=1,fill="both")
		
		bar = Tk.Scrollbar(f2)
		bar.pack(side="left", fill="y")
		
		bar.config(command=box.yview)
		box.config(yscrollcommand=bar.set)
	#@-body
	#@-node:3::createFrame
	#@+node:4::destroy
	#@+body
	def destroy (self,event=None):
		
		"""Hide, do not destroy, a listboxDialog window
		
		subclasses may override to really destroy the window"""
		
		self.top.withdraw() # Don't allow this window to be destroyed.
	
	#@-body
	#@-node:4::destroy
	#@+node:5::hide
	#@+body
	def hide (self):
		
		self.top.withdraw()
	#@-body
	#@-node:5::hide
	#@+node:6::fillbox
	#@+body
	def fillbox(self,event=None):
		
		"""Fill the listbox from information.
		
		Overridden by subclasses"""
		
		pass
	#@-body
	#@-node:6::fillbox
	#@+node:7::go
	#@+body
	def go(self,event=None):
		
		"""callback for the "go" button"""
		
		c = self.c ; box = self.box
		
		# Work around an old Python bug.  Convert strings to ints.
		items = box.curselection()
		try:
			items = map(int, items)
		except ValueError: pass
	
		if items:
			n = items[0]
			v = self.vnodeList[n]
			c.beginUpdate()
			c.tree.expandAllAncestors(v)
			c.selectVnode(v,updateBeadList=true) # A case could be made for updateBeadList=false
			c.endUpdate()
			c.tree.idle_scrollTo(v)
	
	#@-body
	#@-node:7::go
	#@-others
	
	#@-body
	#@-node:2::<< listboxDialog methods >>

	
class recentSectionsDialog (listBoxDialog):
	
	#@<< recentSectionsDialog methods >>
	#@+node:3::<< recentSectionsDialog methods >>
	#@+body
	#@+others
	#@+node:1::__init__  recentSectionsDialog
	#@+body
	def __init__ (self,c,buttons,label):
		
		self.lt_nav_iconFrame_button, self.rt_nav_iconFrame_button = buttons
		self.active = true
		
		listBoxDialog.__init__(self,c,label)
	
	#@-body
	#@-node:1::__init__  recentSectionsDialog
	#@+node:2::addButtons
	#@+body
	def addButtons (self):
	
		self.buttonFrame = f = Tk.Frame(self.outerFrame)
		f.pack()
		
		row1 = Tk.Frame(f)
		row1.pack()
		
		# Create the back and forward buttons, cloning the images & commands of the already existing buttons.
		image   = self.lt_nav_iconFrame_button.cget("image")
		command = self.lt_nav_iconFrame_button.cget("command")
	
		self.lt_nav_button = b = Tk.Button(row1,image=image,command=command)
		b.pack(side="left",pady=2,padx=5)
		
		image   = self.rt_nav_iconFrame_button.cget("image")
		command = self.rt_nav_iconFrame_button.cget("command")
	
		self.rt_nav_button = b = Tk.Button(row1,image=image,command=command)
		b.pack(side="left",pady=2,padx=5)
		
		row2 = Tk.Frame(f)
		row2.pack()
		self.addStdButtons(row2)
		
		row3 = Tk.Frame(f)
		row3.pack()
		
		self.clear_button = b =  Tk.Button(row3,text="Clear All",
			width=6,command=self.clearAll)
		b.pack(side="left",pady=2,padx=5)
		
		self.delete_button = b =  Tk.Button(row3,text="Delete",
			width=6,command=self.deleteEntry)
		b.pack(side="left",pady=2,padx=5)
	
	#@-body
	#@-node:2::addButtons
	#@+node:3::clearAll
	#@+body
	def clearAll (self,event=None):
	
		"""callback for the "Delete" button"""
	
		self.c.visitedList = []
		self.vnodeList = []
		self.fillbox()
	
	#@-body
	#@-node:3::clearAll
	#@+node:4::createFrame
	#@+body
	def createFrame(self):
		
		listBoxDialog.createFrame(self)	
		self.addButtons()
	
	#@-body
	#@-node:4::createFrame
	#@+node:5::deleteEntry
	#@+body
	def deleteEntry (self,event=None):
	
		"""callback for the "Delete" button"""
		
		c = self.c ; box = self.box
		
		# Work around an old Python bug.  Convert strings to ints.
		items = box.curselection()
		try:
			items = map(int, items)
		except ValueError: pass
	
		if items:
			n = items[0]
			v = self.vnodeList[n]
			del self.vnodeList[n]
			if v in c.visitedList:
				c.visitedList.remove(v)
			self.fillbox()
	
	#@-body
	#@-node:5::deleteEntry
	#@+node:6::destroy
	#@+body
	def destroy (self,event=None):
		
		"""Hide a recentSectionsDialog and mark it inactive
		
		This is an escape from possible performace penalties"""
			
		self.active = false
		self.top.withdraw()
		
	
	#@-body
	#@-node:6::destroy
	#@+node:7::fillbox (recent sections)
	#@+body
	def fillbox(self,event=None):
	
		"""Update the listbox and update vnodeList & tnodeList ivars"""
		
		
		# Only fill the box if the dialog is visible and the dialog is active.
		if self.top.state() == "normal" and self.active:
			
			#@<< reconstruct the contents of self.box >>
			#@+node:1::<< reconstruct the contents of self.box >>>
			#@+body
			c = self.c
			
			self.box.delete(0,"end")
			self.vnodeList = []
			self.tnodeList = []
			
			# Make sure the node still exists.
			# Insert only the last cloned node.
			i = 0
			for v in c.visitedList:
				if v.exists(self.c) and v.t not in self.tnodeList:
					self.box.insert(i,v.headString().strip())
					self.tnodeList.append(v.t)
					self.vnodeList.append(v)
					i += 1
			
			#@-body
			#@-node:1::<< reconstruct the contents of self.box >>>

			self.synchButtons()
	#@-body
	#@-node:7::fillbox (recent sections)
	#@+node:8::synchNavButtons
	#@+body
	def synchButtons (self):
	
		# Keep the arrow boxes in synch.
		image = self.lt_nav_iconFrame_button.cget("image")
		self.lt_nav_button.configure(image=image)
		
		image = self.rt_nav_iconFrame_button.cget("image")
		self.rt_nav_button.configure(image=image)
	#@-body
	#@-node:8::synchNavButtons
	#@-others
	
	#@-body
	#@-node:3::<< recentSectionsDialog methods >>

	
class marksDialog (listBoxDialog):
	
	#@<< marksDialog methods >>
	#@+node:4::<< marksDialog methods >>
	#@+body
	#@+others
	#@+node:1::marksDialog.__init__
	#@+body
	def __init__ (self,c,label):
		
		listBoxDialog.__init__(self,c,label)
	
	#@-body
	#@-node:1::marksDialog.__init__
	#@+node:2::createFrame
	#@+body
	def createFrame(self):
		
		c = self.c
		
		listBoxDialog.createFrame(self)
		self.addButtons()
	#@-body
	#@-node:2::createFrame
	#@+node:3::addbuttons
	#@+body
	def addButtons (self):
		
		f = Tk.Frame(self.outerFrame)
		f.pack()
	
		self.addStdButtons(f)
	#@-body
	#@-node:3::addbuttons
	#@+node:4::fillbox
	#@+body
	def fillbox(self,event=None):
	
		"""Update the listbox and update vnodeList & tnodeList ivars"""
	
		self.box.delete(0,"end")
		self.vnodeList = []
		self.tnodeList = []
	
		# Make sure the node still exists.
		# Insert only the last cloned node.
		
		c = self.c ; v = c.rootVnode()
		i = 0
		while v:
			if v.isMarked() and v.t not in self.tnodeList:
				self.box.insert(i,v.headString().strip())
				self.tnodeList.append(v.t)
				self.vnodeList.append(v)
				i += 1
			v = v.threadNext()
	#@-body
	#@-node:4::fillbox
	#@-others
	
	#@-body
	#@-node:4::<< marksDialog methods >>




#@-body
#@-node:0::@file leoDialog.py
#@-leo
