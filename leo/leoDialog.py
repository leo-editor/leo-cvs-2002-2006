#@+leo

#@+node:0::@file leoDialog.py

#@+body
from leoGlobals import *
import string, Tkinter

class leoDialog:

	#@+others

	#@+node:1::__init__

	#@+body
	def __init__(self):
	
		self.answer = ""
		self.top = None

	#@-body

	#@-node:1::__init__

	#@+node:2::askYesNoCancel

	#@+body
	def askYesNoCancel(self, title, message):
	
		Tk = Tkinter ; root = app().root
		self.answer="cancel"
		self.top = top = Tk.Toplevel(root)
		top.title(title)
		top.resizable(0,0) # neither height or width is resizable.
		frame = Tk.Frame(top)
		self.top.bind("<Key>", self.OnKey)
		frame.pack()
		label = Tk.Label(frame, text=message)
		label.pack(pady=10)
		center = Tk.Frame(frame)
		center.pack()
		yes = Tk.Button(center,width=6,text="Yes",bd=4,
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

	#@-node:2::askYesNoCancel

	#@+node:3::askYesNo

	#@+body
	def askYesNo(self, title, message):
	
		Tk = Tkinter ; root = app().root
		self.answer="No"
		self.top = top = Tk.Toplevel(root)
		top.title(title)
		top.resizable(0,0) # neither height or width is resizable.
		frame = Tk.Frame(top)
		self.top.bind("<Key>", self.OnKey)
		frame.pack()
		label = Tk.Label(frame, text=message)
		label.pack(pady=10)
		center = Tk.Frame(frame)
		center.pack()
		yes = Tk.Button(center,width=6,text="Yes",bd=4,
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

	#@-node:3::askYesNo

	#@+node:4::cancelButton, noButton, yesButton

	#@+body
	def cancelButton(self):
	
		self.answer="cancel"
		self.top.destroy() # terminates wait_window
		
	def noButton(self):
	
		self.answer="no"
		self.top.destroy() # terminates wait_window
		
	def yesButton(self):
	
		self.answer="yes"
		self.top.destroy() # terminates wait_window
	#@-body

	#@-node:4::cancelButton, noButton, yesButton

	#@+node:5::dialog.center

	#@+body
	# Center the dialog on the screen.
	
	def center(self):
	
		top = self.top
		top.update_idletasks() # Required to get proper info.
	
		# Get the information about top and the screen.
		sw = top.winfo_screenwidth()
		sh = top.winfo_screenheight()
		g = top.geometry() # g = "WidthxHeight+XOffset+YOffset"
		dim,x,y = string.split(g,'+')
		w,h = string.split(dim,'x')
		w,h,x,y = int(w),int(h),int(x),int(y)
		
		# Set the new window coordinates, leaving w and h unchanged.
		x = (sw - w)/2
		y = (sh - h)/2
		top.geometry("%dx%d%+d%+d" % (w,h,x,y))

	#@-body

	#@-node:5::dialog.center

	#@+node:6::OnKey

	#@+body
	def OnKey(self,event):
	
		ch=event.char
		ch=string.lower(ch)
		if ch=='\n' or ch=='\r': self.yesButton() # The default
		elif ch=='y': self.yesButton()
		elif ch=='n': self.noButton()
		elif ch=='c': self.cancelButton()
	#@-body

	#@-node:6::OnKey

	#@-others

#@-body

#@-node:0::@file leoDialog.py

#@-leo
