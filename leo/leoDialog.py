#@+leo

#@+node:0::@file leoDialog.py
#@+body
#@@language python

from leoGlobals import *
from leoUtils import *
import string, Tkinter

class leoDialog:

	#@+others
	#@+node:1::dialog.__init__
	#@+body
	def __init__(self):
	
		self.answer = ""
		self.top = None
	#@-body
	#@-node:1::dialog.__init__
	#@+node:2::askOk
	#@+body
	def askOk(self, title, message, text="OK"):
	
		Tk = Tkinter ; root = app().root
		self.answer="ok"
		self.top = top = Tk.Toplevel(root)
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
		ok = Tk.Button(center,width=6,text=text,bd=4, # default button
			underline=underline,command=self.okButton)
		ok.pack(side="left",padx=5,pady=10)
		self.center() # Do this after packing.
		top.grab_set() # Make the dialog a modal dialog.
		top.focus_force() # Get all keystrokes.
		root.wait_window(top)
	#@-body
	#@-node:2::askOk
	#@+node:3::askOkCancel
	#@+body
	def askOkCancel(self, title, message):
	
		Tk = Tkinter ; root = app().root
		self.answer="ok"
		self.top = top = Tk.Toplevel(root)
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
	#@-node:3::askOkCancel
	#@+node:4::askYesNo
	#@+body
	def askYesNo(self, title, message):
	
		Tk = Tkinter ; root = app().root
		self.answer="No"
		self.top = top = Tk.Toplevel(root)
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
	#@-node:4::askYesNo
	#@+node:5::askYesNoCancel
	#@+body
	def askYesNoCancel(self, title, message):
	
		Tk = Tkinter ; root = app().root
		self.answer="cancel"
		self.top = top = Tk.Toplevel(root)
		top.title(title)
		top.resizable(0,0) # neither height or width is resizable.
		frame = Tk.Frame(top)
		self.top.bind("<Key>", self.OnYesNoCancelKey)
		frame.pack(padx=6,pady=4)
		label = Tk.Label(frame, text=message)
		label.pack(pady=10)
		center = Tk.Frame(frame)
		center.pack()
		yes = Tk.Button(center,width=6,text="Yes",bd=4, # default button
			underline=0,command=self.yesButton)
		no = Tk.Button(center,width=6,text="No",
			underline=0,command=self.noButton)
		cancel = Tk.Button(center,width=6,text="Cancel",
			underline=0,command=self.cancelButton)
		yes.pack(side="left",padx=5,pady=10)
		no.pack(side="left",padx=5,pady=10)
		cancel.pack(side="left",padx=5,pady=10)
		self.center() # Do this after packing.
		top.grab_set() # Make the dialog a modal dialog.
		top.focus_force() # Get all keystrokes.
		root.wait_window(top)
		return self.answer
	#@-body
	#@-node:5::askYesNoCancel
	#@+node:6::dialog.center
	#@+body
	def center(self):
		
		center_dialog(self.top)
		return
	#@-body
	#@-node:6::dialog.center
	#@+node:7::Event handlers & command handlers
	#@+node:1::cancelButton, noButton, okButton, yesButton
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
	#@-node:1::cancelButton, noButton, okButton, yesButton
	#@+node:2::OnOkCancelKey, OnYesNoKey, OnYesNoCancelKey
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
	#@-body
	#@-node:2::OnOkCancelKey, OnYesNoKey, OnYesNoCancelKey
	#@-node:7::Event handlers & command handlers
	#@-others
#@-body
#@-node:0::@file leoDialog.py
#@-leo
