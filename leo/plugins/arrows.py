#@+leo-ver=4-thin
#@+node:EKR.20040517080517.1:@file-thin arrows.py
"""Rebind up/down arrow keys"""

#@@language python

import leoPlugins
import leoGlobals as g
from leoGlobals import true,false

try: import Tkinter as Tk
except ImportError: Tk = None

if Tk: # Register the handlers...

	#@	@+others
	#@+node:EKR.20040517080517.2:onOpen
	# Warning: the bindings created this way conflict with shift-arrow keys.
	
	def onOpen (tag,keywords):
	
		c = keywords.get("new_c")
		body = c.frame.body
		tree = c.frame.tree
	
		# Add "hard" bindings to have up/down arrows move by visual lines.
		old_binding = body.bodyCtrl.bind("<Up>")
		if len(old_binding) == 0:
			body.bodyCtrl.bind("<Up>",tree.OnUpKey)
	
		old_binding = body.bodyCtrl.bind("<Down>")
		if len(old_binding) == 0:
			body.bodyCtrl.bind("<Down>",tree.OnDownKey)
	#@-node:EKR.20040517080517.2:onOpen
	#@-others

	if g.app.gui is None:
		g.app.createTkGui(__file__)

	if g.app.gui.guiName() == "tkinter":

		leoPlugins.registerHandler("open2", onOpen)
	
		__version__ = "1.3"
		g.plugin_signon(__name__)
#@nonl
#@-node:EKR.20040517080517.1:@file-thin arrows.py
#@-leo
