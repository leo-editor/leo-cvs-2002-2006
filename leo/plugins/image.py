#@+leo-ver=4
#@+node:@file image.py
"""Handle images in body text"""

#@@language python

from leoPlugins import *
from leoGlobals import *
try:
	import Tkinter
except ImportError:
	Tkinter = None
import os

if Tkinter: # Register the handlers...

	#@	@+others
	#@+node:onSelect
	def onSelect (tag,keywords):
	
		new_v = keywords.get("new_v")
		h = new_v.headString()
		if h[:7] == "@image ":
			filename = h[7:]
			#@		<< Select Image >>
			#@+node:<< Select Image >>
			# Display the image file in the text pane, if you can find the file
			a = app
			c = keywords.get("c")
			body = c.frame.body
			
			if os.path.isfile(filename):
				try:
					# Note that Tkinter only understands GIF
					photo = Tkinter.PhotoImage(master=a.root, file=filename)
				except:
					es("error: cannot load image")
					return
				# Nicely display the image at the center top and push the text below.
				a.gsphoto = photo # This is soooo important.
				photoWidth = photo.width()
				bodyWidth = body.bodyCtrl.winfo_width()
				padding = int((bodyWidth - photoWidth - 16) / 2)
				padding = max(0,padding)
				a.gsimage = body.bodyCtrl.image_create("1.0",image=photo,padx=padding)
			else:
				es("warning: missing image file")
			#@nonl
			#@-node:<< Select Image >>
			#@nl
	#@nonl
	#@-node:onSelect
	#@+node:onUnselect
	def onUnselect (tag,keywords):
	
		a = app
		old_v = keywords.get("old_v")
		if old_v:
			h = old_v.headString()
			if h[:7] == "@image ":
				#@			<< Unselect Image >>
				#@+node:<< Unselect Image >>
				# Erase image if it was previously displayed
				a = app ; c = keywords.get("c")
				
				if a.gsimage:
					try:
						 c.frame.body.bodyCtrl.delete(a.gsimage)
					except:
						es("info: no image to erase")
				
				# And forget about it
				a.gsimage = None
				a.gsphoto = None
				#@-node:<< Unselect Image >>
				#@nl
		else: # Leo is initializing.
			a.gsphoto = None # Holds our photo file
			a.gsimage = None # Holds our image instance within the text pane
	#@nonl
	#@-node:onUnselect
	#@-others

	if app.gui is None:
		app.createTkGui(__file__)

	if app.gui.guiName() == "tkinter":
		
		registerHandler("select2", onSelect)
		registerHandler("unselect1", onUnselect)
		
		__version__ = "1.2" # Set version for the plugin handler.
		plugin_signon(__name__)
#@-node:@file image.py
#@-leo
