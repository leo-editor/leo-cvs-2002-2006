#@+leo
#@+node:0::@file leoDialog.py
#@+body
#@@language python

import leoDialog
from leoGlobals import *
import string,Tkinter

Tk = Tkinter


#@+others
#@+node:1::class leoDialog
#@+body
class leoDialog:
	
	"""A base class for all Leo dialogs"""
	

	#@+others
	#@+node:1::__init__ (leoDialog)
	#@+body
	def __init__(self,title="",resizeable=true):
		
		"""Constructor for base leoDialog class."""
		
		self.answer = None # Value returned from run()
		self.resizeable = resizeable
		self.title = title
		self.modal = None
		
		self.buttonsFrame = None # Frame to hold typical dialog buttons.
		self.defaultButtonCommand = None  # Command to call when user closes the window by clicking the close box.
		self.frame = None # The outermost frame in self.top.
		self.root = None # app().root
		self.top = None # The toplevel Tk widget.
		self.focus_widget = None # The widget to get the first focus.
	#@-body
	#@-node:1::__init__ (leoDialog)
	#@+node:2::cancelButton, noButton, okButton, yesButton
	#@+body
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
	#@-body
	#@-node:2::cancelButton, noButton, okButton, yesButton
	#@+node:3::center
	#@+body
	def center(self):
		
		"""Center any leoDialog."""
		
		center_dialog(self.top)
	
	#@-body
	#@-node:3::center
	#@+node:4::createButtons
	#@+body
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
			bd = choose(isDefault,4,2)
	
			b = Tk.Button(f,width=6,text=text,bd=bd,underline=underline,command=command)
			b.pack(side="left",padx=5,pady=10)
			buttonList.append(b)
			
			if isDefault and command:
				self.defaultButtonCommand = command
			
		return buttonList
	#@-body
	#@-node:4::createButtons
	#@+node:5::createMessageFrame
	#@+body
	def createMessageFrame (self,message):
		
		"""Create a frame containing a Tk.Label widget."""
	
		label = Tk.Label(self.frame,text=message)
		label.pack(pady=10)
	
	#@-body
	#@-node:5::createMessageFrame
	#@+node:6::createTopFrame
	#@+body
	def createTopFrame(self):
		
		"""Create the Tk.Toplevel widget for a leoDialog."""
		
		self.root = app().root
	
		self.top = Tk.Toplevel(self.root)
		attachLeoIcon(self.top)
	
		self.top.title(self.title)
	
		if not self.resizeable:
			self.top.resizable(0,0) # neither height or width is resizable.
	
		self.frame = Tk.Frame(self.top)
		self.frame.pack()
	#@-body
	#@-node:6::createTopFrame
	#@+node:7::run
	#@+body
	def run (self,modal):
		
		"""Run a leoDialog."""
	
		self.modal = modal
		
		self.center() # Do this after all packing complete.
	
		if self.modal:
			self.top.grab_set() # Make the dialog a modal dialog.
			if self.focus_widget == None:
				self.focus_widget = self.top
			self.focus_widget.focus_force() # Get all keystrokes.	
			self.root.wait_window(self.top)
			return self.answer
		else:
			self.root.wait_window(self.top)
			return None
	#@-body
	#@-node:7::run
	#@-others


#@-body
#@-node:1::class leoDialog
#@+node:2::class aboutLeo
#@+body
class aboutLeo (leoDialog):
	
	""" """
	

	#@+others
	#@+node:1::aboutLeo.__init__
	#@+body
	def __init__ (self,version,copyright,url,email):
		
		"""Create an About Leo dialog."""
	
		leoDialog.__init__(self,"About Leo",resizeable=true) # Initialize the base class.
		
		self.copyright = copyright
		self.email = email
		self.url = url
		self.version = version
	
		self.createTopFrame()
		self.createFrame()
	
	#@-body
	#@-node:1::aboutLeo.__init__
	#@+node:2::aboutLeo.createFrame
	#@+body
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
	#@-body
	#@-node:2::aboutLeo.createFrame
	#@+node:3::onAboutLeoEmail
	#@+body
	def onAboutLeoEmail(self,event=None):
		
		"""Handle clicks in the email link in an About Leo dialog."""
		
		try:
			import webbrowser
			webbrowser.open("mailto:" + self.email)
		except:
			es("not found: " + self.email)
	#@-body
	#@-node:3::onAboutLeoEmail
	#@+node:4::onAboutLeoUrl
	#@+body
	def onAboutLeoUrl(self,event=None):
		
		"""Handle clicks in the url link in an About Leo dialog."""
	
		try:
			import webbrowser
			webbrowser.open(self.url)
		except:
			es("not found: " + self.url)
	#@-body
	#@-node:4::onAboutLeoUrl
	#@+node:5::setArrowCursor, setDefaultCursor
	#@+body
	def setArrowCursor (self,event=None):
		
		"""Set the cursor to an arrow in an About Leo dialog."""
		
		self.text.configure(cursor="arrow")
		
	def setDefaultCursor (self,event=None):
		
		"""Set the cursor to the default cursor in an About Leo dialog."""
		
		self.text.configure(cursor="xterm")
	#@-body
	#@-node:5::setArrowCursor, setDefaultCursor
	#@-others


#@-body
#@-node:2::class aboutLeo
#@+node:3::class askLeoID (tested)
#@+body
class askLeoID (leoDialog):
	
	"""A class to create and run a dialog that asks for Id for gnx's."""
	

	#@+others
	#@+node:1::askLeoID.__init__
	#@+body
	def __init__(self):
		
		"""Create the Leo Id dialog."""
		
		leoDialog.__init__(self,"Enter unique id",resizeable=false) # Initialize the base class.
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
			"and must be at least 4 characters in length.")
		self.createFrame(message)
		self.focus_widget = self.id_entry
	
		buttons = {"text":"OK","command":self.onButton,"default":true}, # Singleton tuple.
		buttonList = self.createButtons(buttons)
		self.ok_button = buttonList[0]
	#@-body
	#@-node:1::askLeoID.__init__
	#@+node:2::askLeoID.createFrame
	#@+body
	def createFrame(self,message):
		
		"""Create the frame for the Leo Id dialog."""
		
		f = self.frame
	
		label = Tk.Label(f,text=message)
		label.pack(pady=10)
	
		self.id_entry = text = Tk.Entry(f,width=20)
		text.pack()
	#@-body
	#@-node:2::askLeoID.createFrame
	#@+node:3::onCloseWindow
	#@+body
	def onCloseWindow (self):
		
		"""Prevent the Leo Id dialog from closing by ignoring close events."""
	
		pass
	#@-body
	#@-node:3::onCloseWindow
	#@+node:4::onButton
	#@+body
	def onButton(self):
		
		"""Handle clicks in the Leo Id close button."""
	
		s = self.id_entry.get().strip()
		if len(s) < 4:  # Require at least 4 characters in an id.
			return
	
		self.answer = s
		self.top.destroy() # terminates wait_window
	#@-body
	#@-node:4::onButton
	#@+node:5::onKey
	#@+body
	def onKey(self,event):
		
		"""Handle keystrokes in the Leo Id dialog."""
		
		
		#@<< eliminate invalid characters >>
		#@+node:1::<< eliminate invalid characters >>
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
		#@-node:1::<< eliminate invalid characters >>

		
		#@<< enable the ok button if there are 4 or more valid characters >>
		#@+node:2::<< enable the ok button if there are 4 or more valid characters >>
		#@+body
		e = self.id_entry
		b = self.ok_button
		
		if len(e.get().strip()) >= 4:
			b.configure(state="normal")
		else:
			b.configure(state="disabled")
		#@-body
		#@-node:2::<< enable the ok button if there are 4 or more valid characters >>

		
		ch = event.char.lower()
		if ch in ('\n','\r'):
			self.onButton()
		return "break"
	
	
	#@-body
	#@-node:5::onKey
	#@-others


#@-body
#@-node:3::class askLeoID (tested)
#@+node:4::class askOkCancelNumber (tested)
#@+body
class  askOkCancelNumber (leoDialog):
	
	"""Create and run a modal dialog to get a number."""
	

	#@+others
	#@+node:1::askOKCancelNumber.__init__
	#@+body
	def __init__ (self,title,message):
		
		"""Create a number dialog"""
	
		leoDialog.__init__(self,title,resizeable=false) # Initialize the base class.
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
	#@-body
	#@-node:1::askOKCancelNumber.__init__
	#@+node:2::askOKCancelNumber.createFrame
	#@+body
	def createFrame (self,message):
		
		"""Create the frame for a number dialog."""
		
		f = self.frame
		
		lab = Tk.Label(f,text=message)
		lab.pack(pady=10,side="left")
		
		self.number_entry = t = Tk.Entry(f,width=20)
		t.pack(side="left")
	#@-body
	#@-node:2::askOKCancelNumber.createFrame
	#@+node:3::askOKCancelNumber.okButton, cancelButton
	#@+body
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
	#@-body
	#@-node:3::askOKCancelNumber.okButton, cancelButton
	#@+node:4::askOKCancelNumber.onKey
	#@+body
	def onKey (self,event):
		
		
		#@<< eliminate non-numbers >>
		#@+node:1::<< eliminate non-numbers >>
		#@+body
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
		#@-body
		#@-node:1::<< eliminate non-numbers >>

	
		ch = event.char.lower()
	
		if ch in ('o','\n','\r'):
			self.okButton()
		elif ch == 'c':
			self.cancelButton()
	
		return "break"
	#@-body
	#@-node:4::askOKCancelNumber.onKey
	#@-others


#@-body
#@-node:4::class askOkCancelNumber (tested)
#@+node:5::class askOk (tested)
#@+body
class askOk(leoDialog):
	
	""" """
	

	#@+others
	#@+node:1::askOk.__init__
	#@+body
	def __init__ (self,title,message=None,text="Ok",resizeable=false):
	
		"""Create a dialog with one button"""
	
		leoDialog.__init__(self,title,resizeable) # Initialize the base class.
		self.text = text
		self.createTopFrame()
		self.top.bind("<Key>", self.onKey)
	
		if message:
			self.createMessageFrame(message)
	
		buttons = {"text":text,"command":self.okButton,"default":true}, # Singleton tuple.
		self.createButtons(buttons)
	#@-body
	#@-node:1::askOk.__init__
	#@+node:2::askOk.onKey
	#@+body
	def onKey(self,event):
		
		"""Handle Key events in askOk dialogs."""
	
		ch = event.char.lower()
	
		if ch in (self.text[0].lower(),'\n','\r'):
			self.okButton()
	
		return "break"
	
	#@-body
	#@-node:2::askOk.onKey
	#@-others
#@-body
#@-node:5::class askOk (tested)
#@+node:6::class askOkCancel (tested)
#@+body
class askOkCancel (leoDialog):
	
	""" """
	

	#@+others
	#@+node:1::askOkCancel.__init__
	#@+body
	def __init__ (self,title,message=None,resizeable=false):
		
		"""Create a dialog having Ok and Cancel buttons."""
	
		leoDialog.__init__(self,title,resizeable) # Initialize the base class.
		self.createTopFrame()
		self.top.bind("<Key>",self.onKey)
	
		if message:
			self.createMessageFrame(message)
			
		buttons = (
			{"text":"Ok",    "command":self.okButton,     "default":true},
			{"text":"Cancel","command":self.cancelButton} )
		self.createButtons(buttons)
	
	#@-body
	#@-node:1::askOkCancel.__init__
	#@+node:2::askOkCancel.onKey
	#@+body
	def onKey(self,event):
		
		"""Handle keystrokes in a dialog having Ok and Cancel buttons."""
	
		ch = event.char.lower()
		if ch in ('o','\n','\r'):
			self.okButton()
		elif ch == 'c':
			self.cancelButton()
	
		return "break"
	#@-body
	#@-node:2::askOkCancel.onKey
	#@-others
#@-body
#@-node:6::class askOkCancel (tested)
#@+node:7::class askYesNo (tested)
#@+body
class askYesNo (leoDialog):
	
	""" """
	

	#@+others
	#@+node:1::askYesNo.__init__
	#@+body
	def __init__ (self,title,message=None,resizeable=false):
		
		"""Create a dialog having yes and no buttons."""
	
		leoDialog.__init__(self,title,resizeable) # Initialize the base class.
		self.createTopFrame()
		self.top.bind("<Key>",self.onKey)
	
		if message:
			self.createMessageFrame(message)
			
		buttons = (
			{"text":"Yes","command":self.yesButton,  "default":true},
			{"text":"No", "command":self.noButton} )
		self.createButtons(buttons)
	
	#@-body
	#@-node:1::askYesNo.__init__
	#@+node:2::askYesNo.onKey
	#@+body
	def onKey(self,event):
		
		"""Handle keystroke events in dialogs having yes and no buttons."""
	
		ch = event.char.lower()
	
		if ch in ('y','\n','\r'):
			self.yesButton()
		elif ch == 'n':
			self.noButton()
	
		return "break"
	#@-body
	#@-node:2::askYesNo.onKey
	#@-others


#@-body
#@-node:7::class askYesNo (tested)
#@+node:8::class askYesNoCancel (tested)
#@+body
class askYesNoCancel(leoDialog):
	
	"""A class to create and run dialogs having three buttons.
	
	By default, these buttons are labeled yes, no and cancel."""
	

	#@+others
	#@+node:1::askYesNoCancel.__init__
	#@+body
	def __init__ (self,title,
		message=None,
		yesMessage="Yes",
		noMessage="No",
		defaultButton="Yes",
		resizeable=false):
			
		"""Create a dialog having three buttons."""
	
		leoDialog.__init__(self,title,resizeable) # Initialize the base class.
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
	
	
	#@-body
	#@-node:1::askYesNoCancel.__init__
	#@+node:2::askYesNoCancel.onKey
	#@+body
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
	#@-body
	#@-node:2::askYesNoCancel.onKey
	#@+node:3::askYesNoCancel.noButton & yesButton
	#@+body
	def noButton(self):
		
		"""Handle clicks in the 'no' (second) button in a dialog with three buttons."""
		
		self.answer=self.noMessage
		self.top.destroy()
		
	def yesButton(self):
		
		"""Handle clicks in the 'yes' (first) button in a dialog with three buttons."""
		
		self.answer=self.yesMessage
		self.top.destroy()
	
	#@-body
	#@-node:3::askYesNoCancel.noButton & yesButton
	#@-others


#@-body
#@-node:8::class askYesNoCancel (tested)
#@+node:9::class listboxDialog
#@+body
class listBoxDialog (leoDialog):
	
	"""A base class for dialogs containing a Tk Listbox"""


	#@+others
	#@+node:1::listboxDialog.__init__
	#@+body
	def __init__ (self,c,title,label):
		
		"""Constructor for the base listboxDialog class."""
		
		leoDialog.__init__(self,title,resizeable=true) # Initialize the base class.
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
	
	#@-body
	#@-node:1::listboxDialog.__init__
	#@+node:2::addStdButtons
	#@+body
	def addStdButtons (self,frame):
		
		"""Add stanadard buttons to a listBox dialog."""
		
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
		
		"""Hide a list box dialog."""
		
		self.top.withdraw()
	#@-body
	#@-node:5::hide
	#@+node:6::fillbox
	#@+body
	def fillbox(self,event=None):
		
		"""Fill a listbox from information.
		
		Overridden by subclasses"""
		
		pass
	#@-body
	#@-node:6::fillbox
	#@+node:7::go
	#@+body
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
			c.tree.expandAllAncestors(v)
			c.selectVnode(v,updateBeadList=true) # A case could be made for updateBeadList=false
			c.endUpdate()
			c.tree.idle_scrollTo(v)
	
	#@-body
	#@-node:7::go
	#@-others
#@-body
#@-node:9::class listboxDialog
#@+node:10::class recentSectionsDialog (listBoxDialog)
#@+body
class recentSectionsDialog (listBoxDialog):
	
	"""A class to create the recent sections dialog"""


	#@+others
	#@+node:1::__init__  recentSectionsDialog
	#@+body
	def __init__ (self,c,buttons,title,label):
		
		"""Create a Recent Sections listbox dialog."""
		
		self.lt_nav_iconFrame_button, self.rt_nav_iconFrame_button = buttons
	
		listBoxDialog.__init__(self,c,title,label)
	
	
	#@-body
	#@-node:1::__init__  recentSectionsDialog
	#@+node:2::addButtons
	#@+body
	def addButtons (self):
		
		"""Add buttons for a Recent Sections listbox dialog."""
	
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
	
		"""Handle clicks in the "Delete" button of the Recent Sections listbox dialog."""
	
		self.c.visitedList = []
		self.vnodeList = []
		self.fillbox()
	
	#@-body
	#@-node:3::clearAll
	#@+node:4::createFrame
	#@+body
	def createFrame(self):
		
		"""Create the frame of a Recent Sections listbox dialog."""
		
		listBoxDialog.createFrame(self)	
		self.addButtons()
	
	#@-body
	#@-node:4::createFrame
	#@+node:5::deleteEntry
	#@+body
	def deleteEntry (self,event=None):
	
		"""Handle clicks in the "Delete" button of a Recent Sections listbox dialog."""
		
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
		
		"""Hide a Recent Sections listbox dialog and mark it inactive.
		
		This is an escape from possible performace penalties"""
			
		# This is enough to disable fillbox.
		self.top.withdraw()
	
	#@-body
	#@-node:6::destroy
	#@+node:7::fillbox (recent sections)
	#@+body
	def fillbox(self,event=None):
	
		"""Update a Recent Sections listbox dialog and update vnodeList & tnodeList ivars"""
	
		# Only fill the box if the dialog is visible.
		# This is an important protection against bad performance.
	
		if self.top.state() == "normal":
			
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
		
		"""Synchronize the arrow boxes of a Recent Sections listbox dialog."""
	
		image = self.lt_nav_iconFrame_button.cget("image")
		self.lt_nav_button.configure(image=image)
		
		image = self.rt_nav_iconFrame_button.cget("image")
		self.rt_nav_button.configure(image=image)
	#@-body
	#@-node:8::synchNavButtons
	#@-others
#@-body
#@-node:10::class recentSectionsDialog (listBoxDialog)
#@+node:11::class marksDialog methods (listBoxDialog)
#@+body
class marksDialog (listBoxDialog):
	
	"""A class to create the marks dialog"""


	#@+others
	#@+node:1::marksDialog.__init__
	#@+body
	def __init__ (self,c,title,label):
		
		"""Create a Marks listbox dialog."""
	
		listBoxDialog.__init__(self,c,title,label)
	
	#@-body
	#@-node:1::marksDialog.__init__
	#@+node:2::createFrame
	#@+body
	def createFrame(self):
		
		"""Create the frame for a Marks listbox dialog."""
	
		listBoxDialog.createFrame(self)
		self.addButtons()
	#@-body
	#@-node:2::createFrame
	#@+node:3::addbuttons
	#@+body
	def addButtons (self):
		
		"""Add buttons to a Marks listbox dialog."""
		
		f = Tk.Frame(self.outerFrame)
		f.pack()
		self.addStdButtons(f)
	#@-body
	#@-node:3::addbuttons
	#@+node:4::fillbox
	#@+body
	def fillbox(self,event=None):
	
		"""Update a Marks listbox dialog and update the listbox and update vnodeList & tnodeList ivars"""
	
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
#@-node:11::class marksDialog methods (listBoxDialog)
#@-others
#@-body
#@-node:0::@file leoDialog.py
#@-leo
