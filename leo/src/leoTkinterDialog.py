#@+leo-ver=4
#@+node:@file leoTkinterDialog.py
#@@language python

import leoGlobals as g
from leoGlobals import true,false
import string,Tkinter

Tk = Tkinter

#@+others
#@+node: class leoTkinterDialog
class leoTkinterDialog:
	"""The base class for all Leo Tkinter dialogs"""
	#@	@+others
	#@+node:__init__ (leoDialog)
	def __init__(self,title="",resizeable=true):
		
		"""Constructor for the leoTkinterDialog class."""
		
		self.answer = None # Value returned from run()
		self.resizeable = resizeable
		self.title = title
		self.modal = None
		
		self.buttonsFrame = None # Frame to hold typical dialog buttons.
		self.defaultButtonCommand = None  # Command to call when user closes the window by clicking the close box.
		self.frame = None # The outermost frame.
		self.root = None # g.app.root
		self.top = None # The toplevel Tk widget.
		self.focus_widget = None # The widget to get the first focus.
	#@nonl
	#@-node:__init__ (leoDialog)
	#@+node:cancelButton, noButton, okButton, yesButton
	def cancelButton(self):
		
		"""Do default click action in cancel button."""
		
		self.answer="cancel"
		self.top.destroy()
		
	def noButton(self):
		
		"""Do default click action in no button."""
		
		self.answer="no"
		self.top.destroy()
		
	def okButton(self):
		
		"""Do default click action in ok button."""
		
		self.answer="ok"
		self.top.destroy()
	
	def yesButton(self):
		
		"""Do default click action in yes button."""
	
		self.answer="yes"
		self.top.destroy()
	#@nonl
	#@-node:cancelButton, noButton, okButton, yesButton
	#@+node:center
	def center(self):
		
		"""Center any leoTkinterDialog."""
		
		g.app.gui.center_dialog(self.top)
	#@-node:center
	#@+node:createButtons
	def createButtons (self,buttons):
		
		"""Create a row of buttons.
		
		buttons is a list of dictionaries containing the properties of each button."""
		
		assert(self.frame)
		self.buttonsFrame = f = Tk.Frame(self.top)
		f.pack(side="top",padx=30)
	
		# Buttons is a list of dictionaries, with an empty dictionary at the end if there is only one entry.
		buttonList = []
		for d in buttons:
			text = d.get("text","<missing button name>")
			isDefault = d.get("default",false)
			underline = d.get("underline",0)
			command = d.get("command",None)
			bd = g.choose(isDefault,4,2)
	
			b = Tk.Button(f,width=6,text=text,bd=bd,underline=underline,command=command)
			b.pack(side="left",padx=5,pady=10)
			buttonList.append(b)
			
			if isDefault and command:
				self.defaultButtonCommand = command
			
		return buttonList
	#@nonl
	#@-node:createButtons
	#@+node:createMessageFrame
	def createMessageFrame (self,message):
		
		"""Create a frame containing a Tk.Label widget."""
	
		label = Tk.Label(self.frame,text=message)
		label.pack(pady=10)
	#@-node:createMessageFrame
	#@+node:createTopFrame
	def createTopFrame(self):
		
		"""Create the Tk.Toplevel widget for a leoTkinterDialog."""
		
		self.root = g.app.root
	
		self.top = Tk.Toplevel(self.root)
		self.top.title(self.title)
	
		if not self.resizeable:
			self.top.resizable(0,0) # neither height or width is resizable.
	
		self.frame = Tk.Frame(self.top)
		self.frame.pack(side="top",expand=1,fill="both")
		
		# Do this at idle time.
		def callback(top=self.top):
			g.app.gui.attachLeoIcon(top)
		
		self.top.after_idle(callback)
	#@nonl
	#@-node:createTopFrame
	#@+node:run
	def run (self,modal):
		
		"""Run a leoTkinterDialog."""
	
		self.modal = modal
		
		self.center() # Do this after all packing complete.
	
		if self.modal:
			self.top.grab_set() # Make the dialog a modal dialog.
			if self.focus_widget == None:
				self.focus_widget = self.top
			self.focus_widget.focus_set() # Get all keystrokes.	
			self.root.wait_window(self.top)
			return self.answer
		else:
			self.root.wait_window(self.top)
			return None
	#@nonl
	#@-node:run
	#@-others
#@nonl
#@-node: class leoTkinterDialog
#@+node:class tkinterAboutLeo
class tkinterAboutLeo (leoTkinterDialog):
	
	"""A class that creates the Tkinter About Leo dialog."""

	#@	@+others
	#@+node:tkinterAboutLeo.__init__
	def __init__ (self,version,copyright,url,email):
		
		"""Create a Tkinter About Leo dialog."""
	
		leoTkinterDialog.__init__(self,"About Leo",resizeable=true) # Initialize the base class.
		
		self.copyright = copyright
		self.email = email
		self.url = url
		self.version = version
	
		self.createTopFrame()
		self.createFrame()
	#@-node:tkinterAboutLeo.__init__
	#@+node:tkinterAboutLeo.createFrame
	def createFrame (self):
		
		"""Create the frame for an About Leo dialog."""
		
		frame = self.frame
		copyright = self.copyright ; email = self.email
		url = self.url ; version = self.version
		
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
			bitmap_name = g.os_path_join(g.app.loadDir,"..","Icons","Leoapp.GIF") # 5/12/03
			image = Tkinter.PhotoImage(file=bitmap_name)
			text.image_create("1.0",image=image,padx=10)
		except:
			g.es("exception getting icon")
			g.es_exception()
	
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
	#@nonl
	#@-node:tkinterAboutLeo.createFrame
	#@+node:tkinterAboutLeo.onAboutLeoEmail
	def onAboutLeoEmail(self,event=None):
		
		"""Handle clicks in the email link in an About Leo dialog."""
		
		try:
			import webbrowser
			webbrowser.open("mailto:" + self.email)
		except:
			g.es("not found: " + self.email)
	#@nonl
	#@-node:tkinterAboutLeo.onAboutLeoEmail
	#@+node:tkinterAboutLeo.onAboutLeoUrl
	def onAboutLeoUrl(self,event=None):
		
		"""Handle clicks in the url link in an About Leo dialog."""
	
		try:
			import webbrowser
			webbrowser.open(self.url)
		except:
			g.es("not found: " + self.url)
	#@nonl
	#@-node:tkinterAboutLeo.onAboutLeoUrl
	#@+node:tkinterAboutLeo: setArrowCursor, setDefaultCursor
	def setArrowCursor (self,event=None):
		
		"""Set the cursor to an arrow in an About Leo dialog."""
		
		self.text.configure(cursor="arrow")
		
	def setDefaultCursor (self,event=None):
		
		"""Set the cursor to the default cursor in an About Leo dialog."""
		
		self.text.configure(cursor="xterm")
	#@nonl
	#@-node:tkinterAboutLeo: setArrowCursor, setDefaultCursor
	#@-others
#@-node:class tkinterAboutLeo
#@+node:class tkinterAskLeoID
class tkinterAskLeoID (leoTkinterDialog):
	
	"""A class that creates the Tkinter About Leo dialog."""

	#@	@+others
	#@+node:tkinterAskLeoID.__init__
	def __init__(self):
		
		"""Create the Leo Id dialog."""
		
		leoTkinterDialog.__init__(self,"Enter unique id",resizeable=false) # Initialize the base class.
		self.id_entry = None
		self.answer = None
	
		self.createTopFrame()
		self.top.protocol("WM_DELETE_WINDOW", self.onCloseWindow)
		self.top.bind("<Key>", self.onKey)
		
		message = (
			"leoID.txt not found\n\n" +
			"Please enter an id that identifies you uniquely.\n" +
			"Your cvs login name is a good choice.\n\n" +
			"Your id must contain only letters and numbers\n" +
			"and must be at least 3 characters in length.")
		self.createFrame(message)
		self.focus_widget = self.id_entry
	
		buttons = {"text":"OK","command":self.onButton,"default":true}, # Singleton tuple.
		buttonList = self.createButtons(buttons)
		self.ok_button = buttonList[0]
		self.ok_button.configure(state="disabled")
	#@nonl
	#@-node:tkinterAskLeoID.__init__
	#@+node:tkinterAskLeoID.createFrame
	def createFrame(self,message):
		
		"""Create the frame for the Leo Id dialog."""
		
		f = self.frame
	
		label = Tk.Label(f,text=message)
		label.pack(pady=10)
	
		self.id_entry = text = Tk.Entry(f,width=20)
		text.pack()
	#@nonl
	#@-node:tkinterAskLeoID.createFrame
	#@+node:tkinterAskLeoID.onCloseWindow
	def onCloseWindow (self):
		
		"""Prevent the Leo Id dialog from closing by ignoring close events."""
	
		pass
	#@nonl
	#@-node:tkinterAskLeoID.onCloseWindow
	#@+node:tkinterAskLeoID.onButton
	def onButton(self):
		
		"""Handle clicks in the Leo Id close button."""
	
		s = self.id_entry.get().strip()
		if len(s) < 3:  # Require at least 3 characters in an id.
			return
	
		self.answer = g.app.leoID = s
		self.top.destroy() # terminates wait_window
	#@nonl
	#@-node:tkinterAskLeoID.onButton
	#@+node:tkinterAskLeoID.onKey
	def onKey(self,event):
		
		"""Handle keystrokes in the Leo Id dialog."""
		
		#@	<< eliminate invalid characters >>
		#@+node:<< eliminate invalid characters >>
		e = self.id_entry
		s = e.get().strip()
		i = 0 ; ok = true
		while i < len(s):
			ch = s[i]
			if ch not in string.ascii_letters and ch not in string.digits:
				e.delete(`i`)
				s = e.get()
				ok = false
			else:
				i += 1
		if not ok: return
		#@nonl
		#@-node:<< eliminate invalid characters >>
		#@nl
		#@	<< enable the ok button if there are 3 or more valid characters >>
		#@+node:<< enable the ok button if there are 3 or more valid characters >>
		e = self.id_entry
		b = self.ok_button
		
		if len(e.get().strip()) >= 3:
			b.configure(state="normal")
		else:
			b.configure(state="disabled")
		#@nonl
		#@-node:<< enable the ok button if there are 3 or more valid characters >>
		#@nl
		
		ch = event.char.lower()
		if ch in ('\n','\r'):
			self.onButton()
		return "break"
	
	#@-node:tkinterAskLeoID.onKey
	#@-others
#@nonl
#@-node:class tkinterAskLeoID
#@+node:class tkinterAskOk
class tkinterAskOk(leoTkinterDialog):
	
	"""A class that creates a Tkinter dialog with a single OK button."""

	#@	@+others
	#@+node:class tkinterAskOk.__init__
	def __init__ (self,title,message=None,text="Ok",resizeable=false):
	
		"""Create a dialog with one button"""
	
		leoTkinterDialog.__init__(self,title,resizeable) # Initialize the base class.
		self.text = text
		self.createTopFrame()
		self.top.bind("<Key>", self.onKey)
	
		if message:
			self.createMessageFrame(message)
	
		buttons = {"text":text,"command":self.okButton,"default":true}, # Singleton tuple.
		self.createButtons(buttons)
	#@nonl
	#@-node:class tkinterAskOk.__init__
	#@+node:class tkinterAskOk.onKey
	def onKey(self,event):
		
		"""Handle Key events in askOk dialogs."""
	
		ch = event.char.lower()
	
		if ch in (self.text[0].lower(),'\n','\r'):
			self.okButton()
	
		return "break"
	#@-node:class tkinterAskOk.onKey
	#@-others
#@nonl
#@-node:class tkinterAskOk
#@+node:class tkinterAskOkCancelNumber
class  tkinterAskOkCancelNumber (leoTkinterDialog):
	
	"""Create and run a modal Tkinter dialog to get a number."""
	
	#@	@+others
	#@+node:tkinterAskOKCancelNumber.__init__
	def __init__ (self,title,message):
		
		"""Create a number dialog"""
	
		leoTkinterDialog.__init__(self,title,resizeable=false) # Initialize the base class.
		self.answer = -1
		self.number_entry = None
	
		self.createTopFrame()
		self.top.bind("<Key>", self.onKey)
	
		self.createFrame(message)
		self.focus_widget = self.number_entry
	
		buttons = (
				{"text":"Ok",    "command":self.okButton,     "default":true},
				{"text":"Cancel","command":self.cancelButton} )
		buttonList = self.createButtons(buttons)
		self.ok_button = buttonList[0] # Override the default kind of Ok button.
	#@nonl
	#@-node:tkinterAskOKCancelNumber.__init__
	#@+node:tkinterAskOKCancelNumber.createFrame
	def createFrame (self,message):
		
		"""Create the frame for a number dialog."""
		
		f = self.frame
		
		lab = Tk.Label(f,text=message)
		lab.pack(pady=10,side="left")
		
		self.number_entry = t = Tk.Entry(f,width=20)
		t.pack(side="left")
	#@nonl
	#@-node:tkinterAskOKCancelNumber.createFrame
	#@+node:tkinterAskOKCancelNumber.okButton, cancelButton
	def okButton(self):
		
		"""Handle clicks in the ok button of a number dialog."""
	
		s = self.number_entry.get().strip()
	
		try:
			self.answer=int(s)
		except:
			self.answer=-1 # Cancel the operation.
	
		self.top.destroy()
		
	def cancelButton(self):
		
		"""Handle clicks in the cancel button of a number dialog."""
	
		self.answer=-1
		self.top.destroy()
	#@nonl
	#@-node:tkinterAskOKCancelNumber.okButton, cancelButton
	#@+node:tkinterAskOKCancelNumber.onKey
	def onKey (self,event):
		
		#@	<< eliminate non-numbers >>
		#@+node:<< eliminate non-numbers >>
		e = self.number_entry
		s = e.get().strip()
		
		i = 0
		while i < len(s):
			ch = s[i]
			if ch not in string.digits:
				e.delete(`i`)
				s = e.get()
			else:
				i += 1
		#@nonl
		#@-node:<< eliminate non-numbers >>
		#@nl
	
		ch = event.char.lower()
	
		if ch in ('o','\n','\r'):
			self.okButton()
		elif ch == 'c':
			self.cancelButton()
	
		return "break"
	#@nonl
	#@-node:tkinterAskOKCancelNumber.onKey
	#@-others
#@-node:class tkinterAskOkCancelNumber
#@+node:class tkinterAskYesNo
class tkinterAskYesNo (leoTkinterDialog):

	"""A class that creates a Tkinter dialog with two buttons: Yes and No."""

	#@	@+others
	#@+node:tkinterAskYesNo.__init__
	def __init__ (self,title,message=None,resizeable=false):
		
		"""Create a dialog having yes and no buttons."""
	
		leoTkinterDialog.__init__(self,title,resizeable) # Initialize the base class.
		self.createTopFrame()
		self.top.bind("<Key>",self.onKey)
	
		if message:
			self.createMessageFrame(message)
			
		buttons = (
			{"text":"Yes","command":self.yesButton,  "default":true},
			{"text":"No", "command":self.noButton} )
		self.createButtons(buttons)
	#@-node:tkinterAskYesNo.__init__
	#@+node:tkinterAskYesNo.onKey
	def onKey(self,event):
		
		"""Handle keystroke events in dialogs having yes and no buttons."""
	
		ch = event.char.lower()
	
		if ch in ('y','\n','\r'):
			self.yesButton()
		elif ch == 'n':
			self.noButton()
	
		return "break"
	#@nonl
	#@-node:tkinterAskYesNo.onKey
	#@-others

#@-node:class tkinterAskYesNo
#@+node:class tkinterAskYesNoCancel
class tkinterAskYesNoCancel(leoTkinterDialog):
	
	"""A class to create and run Tkinter dialogs having three buttons.
	
	By default, these buttons are labeled Yes, No and Cancel."""
	
	#@	@+others
	#@+node:askYesNoCancel.__init__
	def __init__ (self,title,
		message=None,
		yesMessage="Yes",
		noMessage="No",
		defaultButton="Yes",
		resizeable=false):
			
		"""Create a dialog having three buttons."""
	
		leoTkinterDialog.__init__(self,title,resizeable) # Initialize the base class.
		self.yesMessage,self.noMessage = yesMessage,noMessage
		self.defaultButton = defaultButton
	
		self.createTopFrame()
		self.top.bind("<Key>",self.onKey)
	
		if message:
			self.createMessageFrame(message)
			
		buttons = (
			{"text":yesMessage,"command":self.yesButton,   "default":yesMessage==defaultButton},
			{"text":noMessage, "command":self.noButton,    "default":noMessage==defaultButton},
			{"text":"Cancel",  "command":self.cancelButton,"default":"Cancel"==defaultButton} )
		self.createButtons(buttons)
	
	#@-node:askYesNoCancel.__init__
	#@+node:askYesNoCancel.onKey
	def onKey(self,event):
		
		"""Handle keystrokes in dialogs with three buttons."""
	
		ch = event.char.lower()
		
		if ch in ('\n','\r'):
			ch = self.defaultButton[0].lower()
	
		if ch == self.yesMessage[0].lower():
			self.yesButton()
		elif ch == self.noMessage[0].lower():
			self.noButton()
		elif ch == 'c':
			self.cancelButton()
	
		return "break"
	#@nonl
	#@-node:askYesNoCancel.onKey
	#@+node:askYesNoCancel.noButton & yesButton
	def noButton(self):
		
		"""Handle clicks in the 'no' (second) button in a dialog with three buttons."""
		
		self.answer=self.noMessage.lower()
		self.top.destroy()
		
	def yesButton(self):
		
		"""Handle clicks in the 'yes' (first) button in a dialog with three buttons."""
		
		self.answer=self.yesMessage.lower()
		self.top.destroy()
	#@-node:askYesNoCancel.noButton & yesButton
	#@-others
#@-node:class tkinterAskYesNoCancel
#@+node:class tkinterListboxDialog
class tkinterListBoxDialog (leoTkinterDialog):

	"""A base class for Tkinter dialogs containing a Tk Listbox"""

	#@	@+others
	#@+node:tkinterListboxDialog.__init__
	def __init__ (self,c,title,label):
		
		"""Constructor for the base listboxDialog class."""
		
		leoTkinterDialog.__init__(self,title,resizeable=true) # Initialize the base class.
		self.createTopFrame()
		self.top.protocol("WM_DELETE_WINDOW", self.destroy)
	
		# Initialize common ivars.
		self.c = c
		self.label = label
		self.vnodeList = []
		self.vnodeList = []
		self.buttonFrame = None
		
		# Fill in the frame.
		self.createFrame()
		self.fillbox()
		
		# Make the common bindings after creating self.box.
		
		self.box.bind("<Double-Button-1>",self.go)
	#@-node:tkinterListboxDialog.__init__
	#@+node:addStdButtons
	def addStdButtons (self,frame):
		
		"""Add stanadard buttons to a listBox dialog."""
		
		# Create the ok and cancel buttons.
		self.ok = ok = Tk.Button(frame,text="Go",width=6,command=self.go)
		self.hide = hide = Tk.Button(frame,text="Hide",width=6,command=self.hide)
	
		ok.pack(side="left",pady=2,padx=5)
		hide.pack(side="left",pady=2,padx=5)
	#@nonl
	#@-node:addStdButtons
	#@+node:createFrame
	def createFrame(self):
		
		"""Create the essentials of a listBoxDialog frame
		
		Subclasses will add buttons to self.buttonFrame"""
		
		self.outerFrame = f = Tk.Frame(self.frame)
		f.pack(expand=1,fill="both")
		
		if self.label:
			labf = Tk.Frame(f)
			labf.pack(pady=2)
			lab = Tk.Label(labf,text=self.label)
			lab.pack()
		
		f2 = Tk.Frame(f)
		f2.pack(expand=1,fill="both")
		
		self.box = box = Tk.Listbox(f2,height=20,width=30)
		box.pack(side="left",expand=1,fill="both")
		
		bar = Tk.Scrollbar(f2)
		bar.pack(side="left", fill="y")
		
		bar.config(command=box.yview)
		box.config(yscrollcommand=bar.set)
	#@nonl
	#@-node:createFrame
	#@+node:destroy
	def destroy (self,event=None):
		
		"""Hide, do not destroy, a listboxDialog window
		
		subclasses may override to really destroy the window"""
		
		self.top.withdraw() # Don't allow this window to be destroyed.
	#@-node:destroy
	#@+node:hide
	def hide (self):
		
		"""Hide a list box dialog."""
		
		self.top.withdraw()
	#@nonl
	#@-node:hide
	#@+node:fillbox
	def fillbox(self,event=None):
		
		"""Fill a listbox from information.
		
		Overridden by subclasses"""
		
		pass
	#@nonl
	#@-node:fillbox
	#@+node:go
	def go(self,event=None):
		
		"""Handle clicks in the "go" button in a list box dialog."""
		
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
			c.frame.tree.expandAllAncestors(v)
			c.selectVnode(v,updateBeadList=true) # A case could be made for updateBeadList=false
			c.endUpdate()
			c.frame.tree.idle_scrollTo(v)
	#@-node:go
	#@-others
#@nonl
#@-node:class tkinterListboxDialog
#@-others
#@nonl
#@-node:@file leoTkinterDialog.py
#@-leo
