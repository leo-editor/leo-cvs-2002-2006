#@+leo
#@+node:0::@file leoDialog.py
#@+body
#@@language python

from leoGlobals import *
import string,Tkinter

class leoDialog:

	#@+others
	#@+node:1::dialog.__init__
	#@+body
	def __init__(self):
	
		self.answer = ""
		self.number = -1
		self.top = None
		self.email = None
		self.url = None
		self.text = None
	#@-body
	#@-node:1::dialog.__init__
	#@+node:2::aboutLeo
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
			bitmap_name = os.path.join(app().loadDir,"Icons","Leoapp.GIF")
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
			webbrowser.open("mailto:" + self.url)
		except:
			es("not found: " + self.url)
	#@-body
	#@-node:2::onAboutLeoEmail
	#@-node:2::aboutLeo
	#@+node:3::askOk
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
		ok = Tk.Button(center,width=6,text=text,bd=4, # default button
			underline=underline,command=self.okButton)
		ok.pack(side="left",padx=5,pady=10)
		self.center() # Do this after packing.
		top.grab_set() # Make the dialog a modal dialog.
		top.focus_force() # Get all keystrokes.
		root.wait_window(top)
	#@-body
	#@-node:3::askOk
	#@+node:4::askOkCancel
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
	#@-node:4::askOkCancel
	#@+node:5::askOkCancelNumber
	#@+body
	def askOkCancelNumber(self,title,message):
	
		Tk = Tkinter ; root = app().root
		self.number=-1
		self.top = top = Tk.Toplevel(root)
		attachLeoIcon(self.top)
		top.title(title)
		top.resizable(0,0) # neither height or width is resizable.
		frame = Tk.Frame(top)
		self.top.bind("<Key>", self.OnOkCancelKey)
		frame.pack(padx=6,pady=4)
		label = Tk.Label(frame,text=message)
		label.pack(pady=10,side="left")
		self.number_text = txt = Tk.Text(frame,height=1,width=10)
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
		top.focus_force() # Get all keystrokes.
		root.wait_window(top)
		return self.number
	#@-body
	#@-node:5::askOkCancelNumber
	#@+node:6::askYesNo
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
	#@-node:6::askYesNo
	#@+node:7::askYesNoCancel
	#@+body
	def askYesNoCancel(self, title, message):
	
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
	#@-node:7::askYesNoCancel
	#@+node:8::dialog.center
	#@+body
	def center(self):
		
		center_dialog(self.top)
		return
	#@-body
	#@-node:8::dialog.center
	#@+node:9::Event handlers & command handlers
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
	#@+node:3::setArrowCursor, setDefaultCursor
	#@+body
	def setArrowCursor (self,event=None):
		
		if self.text:
			self.text.configure(cursor="arrow")
		
	def setDefaultCursor (self,event=None):
		
		if self.text:
			self.text.configure(cursor="xterm")
	#@-body
	#@-node:3::setArrowCursor, setDefaultCursor
	#@+node:4::okNumberButton, cancelNumberButton
	#@+body
	def okNumberButton(self):
	
		t = self.number_text.get("1.0","end")
		try:
			self.number=int(t)
		except:
			es("invalid line number:" + t)
			self.number=-1
		self.top.destroy() # terminates wait_window
		
	def cancelButton(self):
		self.number=-1
		self.top.destroy() # terminates wait_window
	#@-body
	#@-node:4::okNumberButton, cancelNumberButton
	#@-node:9::Event handlers & command handlers
	#@-others
#@-body
#@-node:0::@file leoDialog.py
#@-leo
