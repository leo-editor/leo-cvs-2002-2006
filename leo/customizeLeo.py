#@+leo
#@+node:0::@file customizeLeo.py
#@+body
#@+at
#  Leo calls customizeLeo() at various times during execution.  Leo catches 
# all exceptions in this code, so it is safe to hack away on this code.
# 
# The code in customizeLeo() corresponding to each tag is known as the "hook" 
# routine for that tag.
# The keywords argument is a Python dictionary containing information unique 
# to each hook.  For example, keywords["label"] indicates the kind of command 
# for "command1" and "command2" hooks.
# 
# For some hooks, returning anything other than None "overrides" Leo's default action.
# 
# Hooks have full access to all of Leo's source code.  Just import the 
# relevant file.
# For example, top() returns the commander for the topmost Leo window.

#@-at
#@@c

if 1: # Import all symbols from leoGlobals.
	from leoGlobals import *
else: # Import only the essentials.
	from leoGlobals import app,es,top,true,false
	
tagCount = 0


#@+others
#@+node:1::customizeLeo
#@+body
def customizeLeo(tag,keywords): 

	
	
	#@<< sign on (a security precaution) >>
	#@+node:1::<< sign on (a security precaution) >>
	#@+body
	# As a security precaution you should personalize this signon so
	# you can verify when starting Leo that only _your_ code is being run.
	
	if tag == "start2":
		# Announce the presence of this file.
		es("customizeLeo loaded. ",newline=false)
		es("EKR 2/11/03")
	
	#@-body
	#@-node:1::<< sign on (a security precaution) >>


	if 0: # Handy for debugging this code.
		
		#@<< trace tags >>
		#@+node:2::<< trace tags >>
		#@+body
		# Almost all tags have both c and v keys in the keywords dict.
		if tag not in ("start1","end1","open1","open2"):
			c = keywords.get("c")
			v = keywords.get("v")
			if not c:
				print tag, "c = None"
			if not v:
				if tag not in ("select1","select2","unselect1","unselect2"):
					print tag, "v = None"
		
		if tag not in (
			"bodykey1","bodykey2","dragging1","dragging2",
			"headkey1","headkey2","idle"):
		
			global tagCount ; tagCount += 1 # Count all other hooks.
		
			if tag in ("command1","command2"):
				print tagCount,tag,keywords.get("label")
			elif tag in ("open1","open2"):
				print tagCount,tag,keywords.get("fileName")
			else:
				if 1: # Brief
					print tagCount,tag
				else: # Verbose
					keys = keywords.items()
					keys.sort()
					for key,value in keys:
						print tagCount,tag,key,value
					print
		#@-body
		#@-node:2::<< trace tags >>

	
	
	#@<< create and handle the Open With menu >>
	#@+node:3::<< create and handle the Open With menu >>
	#@+body
	if (tag == "start2" or tag == "open2" or
		(tag=="command2" and keywords.get("label")=="new")):
		# print "leoCustomize:creating Open With menu"
		
		#@<< create the Open With menu >>
		#@+node:1::<< create the Open With menu >>
		#@+body
		#@+at
		#  Entries in the following table are the tuple (commandName,shortcut,data).
		# data is the tuple (command,arg,ext).
		# command is one of "os.system", "os.startfile", "os.spawnl", 
		# "os.spawnv" or "exec".
		# Leo executes command(arg+path) where path is the full path to the 
		# temp file.
		# If ext is not None, the temp file has the extension ext,
		# Otherwise, Leo computes an extension based on what @language 
		# directive is in effect.

		#@-at
		#@@c

		idle_arg = "c:/python22/tools/idle/idle.py -e "
		
		if 1: # Default table.
		 table = (
		  ("&Idle",   "Alt+Shift+I",("os.system",idle_arg,".py")),
		  ("&Word",   "Alt+Shift+W",("os.startfile",None,".doc")),
		  ("Word&Pad","Alt+Shift+T",("os.startfile",None,".txt")))
		else: # David McNab's table.
		 table = (
		  ("X&Emacs", "Ctrl+E", ("os.spawnl","/usr/bin/gnuclient", None)))
		
		top().frame.createOpenWithMenuFromTable(table)
		
		#@-body
		#@-node:1::<< create the Open With menu >>

		# Enable the idle-time hook so we can check temp files created by Open With.
		from leoGlobals import enableIdleTimeHook
		enableIdleTimeHook(idleTimeDelay=500)
	
	if tag == "idle":
		
		#@<< check the temp files created by the Open With command >>
		#@+node:2::<< check the temp files created by the Open With command >>
		#@+body
		# frame.OnOpenWith creates the dict as follows:
		# dict = {"c":c, "v":v, "f":f, "path":path, "time":time}
		
		import os
		from leoGlobals import shortFileName
		a = app()
		for dict in a.openWithFiles:
			path = dict.get("path")
			c = dict.get("c")
			v = dict.get("v")
			if path and os.path.exists(path):
				try:
					time = os.path.getmtime(path)
					if time and time != dict.get("time"):
						dict["time"] = time
						
						#@<< update v's body text >>
						#@+node:1::<< update v's body text >>
						#@+body
						
						#@<< set s to the new text >>
						#@+node:1::<< set s to the new text >>
						#@+body
						try:
							# Update v from the changed temp file.
							f=open(path)
							s=f.read()
							f.close()
						except:
							es("can not open " + shortFileName(path))
							break
						
						#@-body
						#@-node:1::<< set s to the new text >>

						body = v.bodyString()
						
						#@<< set conflict flag >>
						#@+node:2::<< set conflict flag >>
						#@+body
						try:
							# The OpenWithOldBody attribute does not normally exist in vnodes.
							old_body = v.OpenWithOldBody
							conflict = body != old_body and body != s
						except:
							conflict = v.isDirty() and body != s
						
						#@-body
						#@-node:2::<< set conflict flag >>

						
						if conflict:
							# Report the conflict & set update.
							import leoDialog
							d = leoDialog.leoDialog()
							message = "Conflict in %s.\n\n" % (v.headString())
							message += "Replace outline with external changes?"
							update = d.askYesNo("Conflict!",message) == "yes"
						else:
							update = s != body
						
						if update:
							h = v.headString()
							es("changed:" + h)
							v.setBodyStringOrPane(s)
							c.selectVnode(v)
							v.OpenWithOldBody = s
						
						#@-body
						#@-node:1::<< update v's body text >>

				except: pass
		#@-body
		#@-node:2::<< check the temp files created by the Open With command >>

	
	#@-body
	#@-node:3::<< create and handle the Open With menu >>


	
	#@<< optional code & contributions from users >>
	#@+node:4::<< optional code & contributions from users >>
	#@+body
	# To enable a set of hooks just change if 0: to if 1: below.
	
	if 0:
		
		#@<< send all output to the log pane >>
		#@+node:5::<< send all output to the log pane >>
		#@+body
		if tag == "start1":
		
			from leoGlobals import redirectStdout,redirectStderr
			redirectStdout()  # Redirect stdout
			redirectStderr() # Redirect stderr
		
		#@-body
		#@-node:5::<< send all output to the log pane >>

		
	if 0: # Contributed by David McNab.
		
		#@<< hooks for xemacs support >>
		#@+node:2::<< hooks for xemacs support >>
		#@+body
		if tag in ("iconclick2","select2"):
		
			# Open node in Emacs.
			self.commands.frame.OnOpenWith(("os.spawnl", "/usr/bin/gnuclient", None))
		
		#@-body
		#@-node:2::<< hooks for xemacs support >>

		
	if 1: # Contributed by Davide Salomoni.
		
		#@<< hook for modified outline export >>
		#@+node:3::<< hook for modified outline export >>
		#@+body
		# modify the way exported outlines are displayed
		
		if tag == "start1":
			
			import leoNodes
			
			#@<< define new moreHead function >>
			#@+node:1::<< define new moreHead function >>
			#@+body
			# Returns the headline string in MORE format.
			
			def newMoreHead (self,firstLevel,useVerticalBar=false):
			
				v = self
				level = self.level() - firstLevel
				if level > 0:
					if useVerticalBar:
						s = " |\t" * level # DS
					else:
						s = "\t"
				else:
					s = ""
				s += choose(v.hasChildren(), "+ ", "- ")
				s += v.headString()
				return s
			
			#@-body
			#@-node:1::<< define new moreHead function >>

			funcToMethod(newMoreHead, leoNodes.vnode, "moreHead")
		
		#@-body
		#@-node:3::<< hook for modified outline export >>

	
	if 0: # Contributed by Davide Salomoni.
		
		#@<< hooks for @read-only nodes >>
		#@+node:4::<< hooks for @read-only nodes >>
		#@+body
		
		#@<< documentation for @read-only nodes >>
		#@+node:1::<< documentation for @read-only nodes >>
		#@+body
		#@+at
		#  Dear Leo users,
		# 
		# Here's my first attempt at customizing leo. I wanted to have the 
		# ability to
		# import files in "read-only" mode, that is, in a mode where files 
		# could only
		# be read by leo (not tangled), and also kept in sync with the content 
		# on the
		# drive.
		# 
		# The reason for this is for example that I have external programs 
		# that generate
		# resource files. I want these files to be part of a leo outline, but 
		# I don't
		# want leo to tangle or in any way modify them. At the same time, I 
		# want them
		# to be up-to-date in the leo outline.
		# 
		# So I coded the directive @read-only in customizeLeo.py. It has the following
		# characteristics:
		# 
		# - It reads the specified file and puts it into the node content.
		# 
		# - If the @read-only directive was in the leo outline already, and 
		# the file content
		# on disk has changed from what is stored in the outline, it marks the 
		# node as
		# changed and prints a "changed" message to the log window; if, on the 
		# other hand,
		# the file content has _not_ changed, the file is simply read and the 
		# node is
		# not marked as changed.
		# 
		# - When you write a @read-only directive, the file content is added 
		# to the node
		# immediately, i.e. as soon as you press Enter (no need to call a menu
		# entry to import the content).
		# 
		# - If you want to refresh/update the content of the file, just edit 
		# the headline
		# and press Enter. The file is reloaded, and if in the meantime it has changed,
		# a "change" message is sent to the log window.
		# 
		# - The body text of a @read-only file cannot be modified in leo.
		# 
		# Davide Salomoni

		#@-at
		#@-body
		#@-node:1::<< documentation for @read-only nodes >>

		
		from leoGlobals import match_word
		
		if tag == "open2":
			
			#@<< scan the outline and process @read-only nodes >>
			#@+node:2::<< scan the outline and process @read-only nodes >>
			#@+body
			c = keywords.get("new_c")
			v = top().rootVnode()
			c.beginUpdate()
			while v:
				h = v.headString()
				if match_word(h,0,"@read-only"):
					changed = insert_read_only_node(c,v,h[11:])
					if changed:
						if not v.isDirty():
							v.setDirty()
						if not c.isChanged():
							c.setChanged(changed)
				v = v.threadNext()
			c.endUpdate()
			#@-body
			#@-node:2::<< scan the outline and process @read-only nodes >>

		
		if tag == "bodykey1":
			
			#@<< override the body key handler if we are in an @read-only node >>
			#@+node:3::<< override the body key handler if we are in an @read-only node >>
			#@+body
			c = keywords.get("c")
			v = keywords.get("v")
			h = v.headString()
			if match_word(h,0,"@read-only"):
				# An @read-only node: do not change its text.
				body = c.frame.body
				body.delete("1.0","end")
				body.insert("1.0",v.bodyString())
				return 1 # Override the body key event handler.
			#@-body
			#@-node:3::<< override the body key handler if we are in an @read-only node >>

		
		if tag == "headkey2":
			
			#@<< update the body text when we press enter >>
			#@+node:4::<< update the body text when we press enter >>
			#@+body
			c = keywords.get("c")
			v = keywords.get("v")
			h = v.headString()
			ch = keywords.get("ch")
			if ch == '\r' and match_word(h,0,"@read-only"):
				# on-the-fly update of @read-only directives
				changed = insert_read_only_node(c,v,h[11:])
				c.setChanged(changed)
			#@-body
			#@-node:4::<< update the body text when we press enter >>

		
		if tag == "select1":
			if 0: # Doesn't work: the cursor doesn't start blinking.
				# Enable the body text so select will work properly.
				c = keywords.get("c")
				enable_body(c.frame.body)
			
		if tag == "select2":
			if 0: # Doesn't work: the cursor permantently stops blinking.
				
				#@<< disable body text for read-only nodes >>
				#@+node:5::<< disable body text for read-only nodes >>
				#@+body
				c = keywords.get("c")
				v = c.currentVnode()
				h = v.headString()
				if match_word(h,0,"@read-only"):
					disable_body(c.frame.body)
				else:
					enable_body(c.frame.body)
				
				#@-body
				#@-node:5::<< disable body text for read-only nodes >>
		#@-body
		#@-node:4::<< hooks for @read-only nodes >>

		
	if 0: # Contributed by Niklas Frykholm. Revised by Gil Shwartz and E.K.Ream.
		
		#@<< create proper outline from empty .leo file >>
		#@+node:6::<< create proper outline from empty .leo file >>
		#@+body
		empty_leo_file = """<?xml version="1.0" encoding="iso-8859-1"?>
		<leo_file>
		<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
		<globals body_outline_ratio="0.5">
			<global_window_position top="145" left="110" height="24" width="80"/>
			<global_log_window_position top="0" left="0" height="0" width="0"/>
		</globals>
		<preferences allow_rich_text="0">
		</preferences>
		<find_panel_settings>
			<find_string></find_string>
			<change_string></change_string>
		</find_panel_settings>
		<vnodes>
		<v a="V"><vh>NewHeadline</vh></v>
		</vnodes>
		<tnodes>
		</tnodes>
		</leo_file>"""
		
		if tag == "open1":
			import os
			file_name = keywords.get('fileName')
			if file_name and os.path.getsize(file_name)==0:
				# Rewrite the file before really opening it.
				es("rewriting empty .leo file: %s" % (file_name))
				file = open(file_name,'w')
				file.write(empty_leo_file)
				file.flush()
				file.close()
		
		#@-body
		#@-node:6::<< create proper outline from empty .leo file >>

		
	if 1: # Contributed by Gil Shwartz.
		
		#@<< image hooks >>
		#@+node:1::<< image hooks >>
		#@+body
		try:
			import Tkinter, os.path
			
			if tag == "unselect1":
				
				#@<< Prepare Params >>
				#@+node:1::<< Prepare Params >>
				#@+body
				a = app()
				c = keywords.get("c")
				old_v = keywords.get("old_v")
				new_v = keywords.get("new_v")
				body = c.frame.body
				
				#@-body
				#@-node:1::<< Prepare Params >>

				
				if not(old_v): # When Leo initializes there is no previous v node
					# A good time to initialize our vars
					a.gsphoto = None # Holds our photo file
					a.gsimage = None # Holds our image instance within the text pane
					return
		
				h = old_v.headString()
					
				if h[:7] == "@image ":
					
					#@<< Unselecting Image >>
					#@+node:2::<< Unselecting Image >>
					#@+body
					# Erase image if it was previously displayed
					if (a.gsimage):
						try:
							c.frame.body.delete(a.gsimage)
						except:
							es("info: no image to erase")
					
					# And forget about it
					a.gsimage = None
					a.gsphoto = None
					
					#@-body
					#@-node:2::<< Unselecting Image >>
					
					
			if tag == "select2":
				
				#@<< Prepare Params >>
				#@+node:1::<< Prepare Params >>
				#@+body
				a = app()
				c = keywords.get("c")
				old_v = keywords.get("old_v")
				new_v = keywords.get("new_v")
				body = c.frame.body
				
				#@-body
				#@-node:1::<< Prepare Params >>

			
				h = new_v.headString()
			
				if h[:7] == "@image ":
				#if match_word(h,0,"@image"):
					
					#@<< Selecting Image >>
					#@+node:3::<< Selecting Image >>
					#@+body
					# Display the image file in the text pane, if you can find the file
					filename = h[7:] # 1/
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
						bodyWidth = body.winfo_width()
						padding = int((bodyWidth - photoWidth - 16) / 2)
						padding = max(0,padding)
						a.gsimage = body.image_create("1.0",image=photo,padx=padding)
					else:
						es("warning: missing image file")
					
					#@-body
					#@-node:3::<< Selecting Image >>

					
		except:
			es("error: exception in image hook")
			es_exception()
		
		#@-body
		#@-node:1::<< image hooks >>

		
	if 0: # This code isn't ready for prime time.
		
		#@<< up/down arrow hooks >>
		#@+node:8::<< up/down arrow hooks >>
		#@+body
		# Warning: the bindings created this way conflict with shift-arrow keys.
		
		if tag == "open2":
		
			c = keywords.get("new_c")
			body = c.frame.body
			tree = c.frame.tree
		
			# Add "hard" bindings to have up/down arrows move by visual lines.
			old_binding = body.bind("<Up>")
			if len(old_binding) == 0:
				body.bind("<Up>",tree.OnUpKey)
		
			old_binding = body.bind("<Down>")
			if len(old_binding) == 0:
				body.bind("<Down>",tree.OnDownKey)
		
		#@-body
		#@-node:8::<< up/down arrow hooks >>

		
	if 0: # Contributed by Korakot Chaovavanich
		
		#@<< synchronize @folder nodes with folders >>
		#@+node:7::<< synchronize @folder nodes with folders >>
		#@+body
		#@+at
		#  Since I met leo, I started to store all my text data in a single 
		# leo file.
		# This include diary, work-log, articles that I read, interesting 
		# websites and
		# addressbook. So far, everything work fine. The problem is that 
		# sometimes I get
		# word files, excel files, powerpoint files, graphics, etc. I could 
		# not directly
		# handle them now easily with leo, so everything would be assessible 
		# easily from
		# a single place.
		# 
		# My first try is to create a folder. And say in my diary/work-log 
		# that I got a
		# new file like 'courses.doc' and I put everything I got in that 
		# folder. When
		# they accumulate, it become difficult to handle them just from that 
		# folder. I
		# would prefer to handle them through leo.
		# 
		# Last week, after Edward release the code that allow 'hook' and
		# 'customizeLeo.py'. I know I could have my second try to solve it. So 
		# this is
		# it, '@folder' node. If a node is named '@folder path_to_folder', the content
		# (filenames) of the folder and the children of that node will be 
		# sync. Whenever
		# a new file is put there, a new node will appear on top of the 
		# children list
		# (with mark). So that I can put my description (ie. annotation) as 
		# the content
		# of that node. In this way, I can find any files much easier from leo.
		# 
		# Moreover, I add another feature to allow you to group files(in leo) into
		# children of another group. This will help when there are many files 
		# in that
		# folder. You can logically group it in leo (or even clone it to many groups),
		# while keep every files in a flat/single directory on your computer.

		#@-at
		#@@c

		if tag == 'select1':
			v = keywords.get("new_v")
			h = v.headString()
			if match_word(h,0,"@folder"):
				sync_node_to_folder(v,h[8:])
		#@-body
		#@-node:7::<< synchronize @folder nodes with folders >>
	#@-body
	#@-node:4::<< optional code & contributions from users >>

	
	if 0:
		if tag == "idle":
			print top().frame.body.index("insert")

	if 0:
		
		#@<< examples of using hooks >>
		#@+node:5::<< examples of using hooks >>
		#@+body
		# Accessing information...
		
		#@<< print the commander for each open window >>
		#@+node:6::<< print the commander for each open window >>
		#@+body
		for w in app().windowList:
			print w.commands # The commander for each open window.
		top().frame.menus.sort()
		for name,menu in top().frame.menus:
			print name,
		print
		#@-body
		#@-node:6::<< print the commander for each open window >>

		
		#@<< dump the various symbol tables >>
		#@+node:3::<< dump the various symbol tables >>
		#@+body
		if tag == "start2":
		
			print "\nglobals..."
			for s in globals():
				if s not in __builtins__:
					print s
			
			print "\nlocals..."
			for s in locals():
				if s not in __builtins__:
					print s
		
		#@-body
		#@-node:3::<< dump the various symbol tables >>

		
		#@<< enable gc checking >>
		#@+node:4::<< enable gc checking >>
		#@+body
		if tag == "start1":
			try:
				import gc
				print "Enabling gc debugging"
				gc.set_debug(gc.DEBUG_LEAK)
			except: pass
		#@-body
		#@-node:4::<< enable gc checking >>

		
		# Commands...
		
		#@<< do something at the start of each command >>
		#@+node:2::<< do something at the start of each command >>
		#@+body
		if tag == "command1":
			print "end  ", keywords.get("label")
		#@-body
		#@-node:2::<< do something at the start of each command >>

		
		#@<< override the Equal Sized panes command >>
		#@+node:5::<< override the Equal Sized panes command >>
		#@+body
		if tag == "command1":
			if keywords.get("label")=="equalsizedpanes":
				print "over-riding Equal Sized Panes"
				return "override" # Anything other than None overrides.
		#@-body
		#@-node:5::<< override the Equal Sized panes command >>

		
		# How to replace _any_ method in Leo's source code!
		
		#@<< redefine frame.put and frame.putnl >>
		#@+node:7::<< redefine frame.put and frame.putnl >>
		#@+body
		#@+at
		#  This code illustrates how to redefine _any_ method of Leo.
		# Python makes this is almost too easy :-)

		#@-at
		#@@c

		if tag == "start1":
		
			import leoFrame
			
			# Replace frame.put with newPut.
			funcToMethod(newPut,leoFrame.LeoFrame,"put")
			
			# Replace frame.putnl with newPutNl.
			funcToMethod(newPutNl,leoFrame.LeoFrame,"putnl")
		
		#@-body
		#@-node:7::<< redefine frame.put and frame.putnl >>

		
		# Menus...
		
		#@<< create Scripts menu for LeoPy.leo >>
		#@+node:1::<< create Scripts menu for LeoPy.leo >>
		#@+body
		if tag == "open2":
			if top().frame.shortFileName() == "LeoPy.leo":
				table = (
					("Show Current Working Directory",None,show_cwd),
					("Import All Python Files From CWD",None,importPythonFiles),
					("Import All Cweb Files From CWD",None,importCwebFiles))
				
				es("creating Scripts menu for LeoPy.leo")
				top().frame.createNewMenu("Scripts","top")
				top().frame.createMenuItemsFromTable("Scripts",table)
		
		#@-body
		#@-node:1::<< create Scripts menu for LeoPy.leo >>

		
		#@<< translate a few menu items into french >>
		#@+node:10::<< translate a few menu items into french >>
		#@+body
		#@+at
		#  12/6/02: The translation table used by setRealMenuNamesFromTable 
		# has entries of the form:
		# 
		# 	("official name","translated name"),
		# 
		# Ampersands in the translated name indicate that the following 
		# character is to be underlined.
		# 
		# The official name can be any name equivalent to the standard English 
		# menu names.  Leo "canonicalizes" the official name by converting to 
		# lower case and removing any non-letters.  Thus, the following are  equivalent:
		# 	("Open...","&Ouvre"),
		# 	("open",   "&Ouvre"),
		# 	("&Open",  "&Ouvre"),

		#@-at
		#@@c
		if tag == "menu1":
			table = (
				("Open...","&Ouvre"),
				("OpenWith","O&uvre Avec..."),
				("close","&Ferme"),
				("Undo Typing","French &Undo Typing"), # Shows you how much French I know ;-)
				("Redo Typing","French &Redo Typing"),
				("Can't Undo", "French Can't Undo"),
				("Can't Redo", "French Can't Redo"))
			# 12/6/02: A new convenience routine.
			app().setRealMenuNamesFromTable(table)
		
		#@-body
		#@-node:10::<< translate a few menu items into french >>

		
		# Events and exceptions...
		
		#@<< trace the key handlers >>
		#@+node:9::<< trace the key handlers >>
		#@+body
		if tag in ("bodykey1","bodykey2","headkey1","headkey2"):
			ch = keywords.get("ch")
			if ch and len(ch) > 0:
				print "customizeLeo",tag,keywords
		#@-body
		#@-node:9::<< trace the key handlers >>

		
		#@<< test how Leo handles exceptions in this file >>
		#@+node:8::<< test how Leo handles exceptions in this file >>
		#@+body
		if tag == "end1":
			print `app().doesNotExist` # Test of exception handling.
		#@-body
		#@-node:8::<< test how Leo handles exceptions in this file >>
		#@-body
		#@-node:5::<< examples of using hooks >>
#@-body
#@+node:6::Functions called by hooks...
#@+body
#@+others
#@+node:1::enable/disable_body
#@+body
# Alas, these do not seem to work on XP:
# disabling the body text _permanently_ stops the cursor from blinking.

def enable_body(body):
	global insertOnTime,insertOffTime
	if body.cget("state") == "disabled":
		try:
			es("enable")
			print insertOffTime,insertOnTime
			body.configure(state="normal")
			body.configure(insertontime=insertOnTime,insertofftime=insertOffTime)
		except: es_exception()
			
def disable_body(body):
	global insertOnTime,insertOffTime
	if body.cget("state") == "normal":
		try:
			es("disable")
			insertOnTime = body.cget("insertontime")
			insertOffTime = body.cget("insertofftime")
			print insertOffTime,insertOnTime
			body.configure(state="disabled")
		except: es_exception()

#@-body
#@-node:1::enable/disable_body
#@+node:2::funcToMethod
#@+body
#@+at
#  The following is taken from page 188 of the Python Cookbook.
# 
# The following method allows you to add a function as a method of any class.  
# That is, it converts the function to a method of the class.  The method just 
# added is available instantly to all existing instances of the class, and to 
# all instances created in the future.
# 
# The function's first argument should be self.
# 
# The newly created method has the same name as the function unless the 
# optional name argument is supplied, in which case that name is used as the 
# method name.

#@-at
#@@c

def funcToMethod(f,theClass,name=None):
	setattr(theClass,name or f.__name__,f)
	
# That's all!
#@-body
#@-node:2::funcToMethod
#@+node:3::insert_read_only_node
#@+body
# Sets v's body text from the file with the given name.
# Returns true if the body text changed.
def insert_read_only_node (c,v,name):
	from leoGlobals import es
	try:
		file = open(name,"r")
	except IOError,msg:
		es("error reading %s: %s" % (name, msg))
		v.setBodyStringOrPane("") # Clear the body text.
		return true # Mark the node as changed.
	else:
		es("reading: @read-only %s" % name)
		new = file.read()
		file.close()
		previous = v.t.bodyString
		v.setBodyStringOrPane(new)
		changed = (new != previous)
		if changed and previous != "":
			es("changed: %s" % name) # A real change.
		return changed

#@-body
#@-node:3::insert_read_only_node
#@+node:4::newPut and newPutNl
#@+body
# Contrived examples of how to redefine frame.put and frame.putnl

# Same as frame.put except converts everything to upper case.
def newPut (self,s):
	# print "newPut",s,
	if app().quitting > 0: return
	s = s.upper()
	if self.log:
			self.log.insert("end",s)
			self.log.see("end")
			self.log.update_idletasks()
	else: print s,

# Same as frame.putnl except writes two newlines.
def newPutNl (self):
	# print "newPutNl"
	if app().quitting > 0: return
	if self.log:
		self.log.insert("end","\n\n")
		self.log.see("end")
		self.log.update_idletasks()
	else: print
#@-body
#@-node:4::newPut and newPutNl
#@+node:5::sync_node_to_folder
#@+body
def sync_node_to_folder(parent,d):

	oldlist = {}
	newlist = []
	#get children info
	v = parent
	after_v = parent.nodeAfterTree()
	while v != after_v:
		if not v.hasChildren():
			oldlist[v.headString()] = v.bodyString()
		v = v.threadNext()
	#compare folder content to children
	for name in os.listdir(d):
		if name in oldlist:
			del oldlist[name]
		else:
			newlist.append(name)
	#insert newlist
	newlist.sort()
	newlist.reverse()
	for name in newlist:
		v = parent.insertAsNthChild(0)
		v.setHeadStringOrHeadline(name)
		v.setMarked()
	#warn for orphan oldlist
	if len(oldlist)>0:
		es('missing: '+','.join(oldlist.keys()))

#@-body
#@-node:5::sync_node_to_folder
#@-others
#@-body
#@-node:6::Functions called by hooks...
#@-node:1::customizeLeo
#@-others
#@-body
#@-node:0::@file customizeLeo.py
#@-leo
