#@+leo

#@+node:0::@file leoFontPanel.py
#@+body
#@@language python

from leoGlobals import *
from leoUtils import *
import sys,string,Tkinter

class leoFontPanel:

	#@+others
	#@+node:1::fontPanel.__init__
	#@+body
	def __init__ (self,c):
		
		Tk = Tkinter
		self.commands = c
		self.frame = c.frame
		self.sizeVar = Tk.IntVar()
	#@-body
	#@-node:1::fontPanel.__init__
	#@+node:2::run
	#@+body
	def run (self):
		
		
		#@<< Create the font dialog >>
		#@+node:1::<< Create the font dialog >>
		#@+body
		Tk = Tkinter
		
		top = Tk.Toplevel(app().root)
		top.title("Select a font")
		
		# Create the outer frame
		outer = Tk.Frame(top)
		outer.pack(fill="both",expand=1,padx=2,pady=2)
		
		w,ff = create_labeled_frame(outer)
		w.pack(fill="both",expand=1,padx=2,pady=2)
		
		# Create a frame containing the grid of inner boxes.
		g = Tk.Frame(ff)
		g.grid()
		
		# Create the inner frames of the grid.
		family = Tk.Frame(g)
		family.grid(row=1,col=1)
		
		style = Tk.Frame(g)
		style.grid(row=1,col=2)
		
		buttons = Tk.Frame(g)
		buttons.grid(row=1,col=3)
		
		size = Tk.Frame(g)
		size.grid(row=2,col=1,columnspan=3,sticky="news")
		
		sample = Tk.Frame(g)
		sample.grid(row=3,col=1,columnspan=3,sticky="news")
		
		# Create the Family pane.
		w,f = create_labeled_frame(family,caption="Family")
		w.pack(padx=2)
		
		b = Tk.Listbox(f,height=7,width=12)
		b.pack(padx=2)
		
		# Create the Style frame.
		w,f = create_labeled_frame(style,caption="Style")
		w.pack(padx=2)
		
		styles = Tk.Frame(f)
		styles.pack()
		i = 1
		for name in ("Bold","Italic","Underline","OverStrike"):
			b = Tk.Checkbutton(styles,text=name)
			b.pack(anchor="w",pady=1)
			i += 1
		
		# Create the column of buttons.
		buttonFrame = Tk.Frame(buttons)
		buttonFrame.pack(padx=2)
		
		b = Tk.Button(buttonFrame,width=7,text="OK")
		b.pack(side="top")
		b = Tk.Button(buttonFrame,width=7,text="Cancel")
		b.pack(side="top",fill="y",expand=1,pady=10)
		b = Tk.Button(buttonFrame,width=7,text="Apply")
		b.pack(side="bottom")
		
		
		#@<< create the size pane >>
		#@+node:1::<< create the size pane >>
		#@+body
		w,f = create_labeled_frame(size,caption="Size")
		w.pack(padx=2,fill="both",expand=1)
		
		sizes = Tk.Frame(f)
		f.grid(sticky="news")
		
		row = col = 0
		for i in (8,10,12,14,18,24):
			b = Tk.Radiobutton(f,text=`i`,variable=self.sizeVar,value=i)
			if i==12:
				print "b.select"
				b.select()
			b.grid(row=row,column=col,sticky="w")
			row += 1
			if row == 2:
				col += 1 ; row = 0
		
		sizeBox = Tk.Entry(f,width=12)
		sizeBox.grid(row=1,rowspan=2,column=3,padx=10)
		#@-body
		#@-node:1::<< create the size pane >>

		
		# Create the sample pane.
		w,f  = create_labeled_frame(sample,caption="Sample",pady=2)
		w.pack(side="top",fill="both",expand=1,padx=2,pady=2)
		color = f.cget("bg")
		e = Tk.Entry(f,bd=0,bg=color)
		e.insert(0, "Sample Text Here (May be edited)") 
		e.pack(fill="x",expand=1,padx=5,pady=5)
		#@-body
		#@-node:1::<< Create the font dialog >>

		self.sizeVar.set(12)
		
		# This must be done _after_ the dialog has been built!
		center_dialog(top)
		top.resizable(0,0)
		
		# Bring up the modal dialog.
		top.grab_set()
		top.focus_force() # Get all keystrokes.
	
		## To do: set body text font, size based on dialog
	#@-body
	#@-node:2::run
	#@-others
#@-body
#@-node:0::@file leoFontPanel.py
#@-leo
