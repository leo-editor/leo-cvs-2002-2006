#@+leo-ver=4
#@+node:@file open_with.py
"""Create menu for Open With command and handle the resulting commands"""

from leoPlugins import *
from leoGlobals import *

try:
	import Tkinter
except ImportError:
	Tkinter = None

if Tkinter: # Register the handlers...

	#@	@+others
	#@+node:on_idle
	# frame.OnOpenWith creates the dict with the following entries:
	# "body", "c", "encoding", "f", "path", "time" and "v".
	
	def on_idle (tag,keywords):
	
		import os
		a = app()
		for dict in a.openWithFiles:
			path = dict.get("path")
			c = dict.get("c")
			encoding = dict.get("encoding",None)
			v = dict.get("v")
			old_body = dict.get("body")
			if path and os.path.exists(path):
				try:
					time = os.path.getmtime(path)
					if time and time != dict.get("time"):
						dict["time"] = time # inhibit endless dialog loop.
						# The file has changed.
						#@					<< update v's body text >>
						#@+node:<< update v's body text >>
						#@<< set s to the file text >>
						#@+node:<< set s to the file text >>
						try:
							# Update v from the changed temp file.
							f=open(path)
							s=f.read()
							f.close()
						except:
							es("can not open " + shortFileName(path))
							break
						#@-node:<< set s to the file text >>
						#@nl
						
						# Convert body and s to whatever encoding is in effect.
						body = v.bodyString()
						body = toEncodedString(body,encoding,reportErrors=true)
						s = toEncodedString(s,encoding,reportErrors=true) # 10/13/03
						
						conflict = body != old_body and body != s
						
						# Set update if we should update the outline from the file.
						if conflict:
							# See how the user wants to resolve the conflict.
							es("conflict in " + shortFileName(path),color="red")
							message = "Replace changed outline with external changes?"
							result = app.gui.runAskYesNoDialog("Conflict!",message)
							update = result.lower() == "yes"
						else:
							update = s != body
						
						if update:
							es("updated from: " + shortFileName(path),color="blue")
							v.setBodyStringOrPane(s,encoding) # 10/16/03
							c.selectVnode(v)
							dict["body"] = s
						elif conflict:
							es("not updated from: " + shortFileName(path),color="blue")
						#@nonl
						#@-node:<< update v's body text >>
						#@nl
				except:
					es_exception() ## testing
					pass
	#@nonl
	#@-node:on_idle
	#@+node:create_open_with_menu
	def create_open_with_menu (tag,keywords):
	
		if  (tag in ("start2","open2") or
			(tag=="command2" and keywords.get("label")=="new")):
	
			#@		<< create the Open With menu >>
			#@+node:<< create the Open With menu >>
			#@+at 
			#@nonl
			# Entries in the following table are the tuple 
			# (commandName,shortcut,data).
			# 
			# - data is the tuple (command,arg,ext).
			# - command is one of "os.system", "os.startfile", "os.spawnl", 
			# "os.spawnv" or "exec".
			# 
			# Leo executes command(arg+path) where path is the full path to 
			# the temp file.
			# If ext is not None, the temp file has the extension ext,
			# Otherwise, Leo computes an extension based on what @language 
			# directive is in effect.
			#@-at
			#@@c
			
			idle_arg = "c:/python22/tools/idle/idle.py -e "
			
			if 1: # Default table.
				table = (
					# Opening idle this way doesn't work so well.
					# ("&Idle",   "Alt+Shift+I",("os.system",idle_arg,".py")),
					("&Word",   "Alt+Shift+W",("os.startfile",None,".doc")),
					("Word&Pad","Alt+Shift+T",("os.startfile",None,".txt")))
			elif 1: # Test table.
				table = ("&Word","Alt+Shift+W",("os.startfile",None,".doc")),
			else: # David McNab's table.
				table = ("X&Emacs", "Ctrl+E", ("os.spawnl","/usr/bin/gnuclient", None)),
			
			top().frame.menu.createOpenWithMenuFromTable(table)
			#@nonl
			#@-node:<< create the Open With menu >>
			#@nl
			# Enable the idle-time hook so we can check temp files created by Open With.
			from leoGlobals import enableIdleTimeHook
			enableIdleTimeHook(idleTimeDelay=500)
	#@-node:create_open_with_menu
	#@-others

	if app.gui is None:
		app.createTkGui(__file__)

	if app.gui.guiName() == "tkinter":

		app().hasOpenWithMenu = true
		registerHandler("idle", on_idle)
		registerHandler(("start2","open2","command2"), create_open_with_menu)
	
		__version__ = "1.4" # Set version for the plugin handler.
		plugin_signon(__name__)
#@nonl
#@-node:@file open_with.py
#@-leo
