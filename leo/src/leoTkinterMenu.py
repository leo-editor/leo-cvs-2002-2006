#@+leo-ver=4
#@+node:@file leoTkinterMenu.py
"""Tkinter menu handling for Leo."""

from leoGlobals import *

import leoMenu
import Tkinter

class leoTkinterMenu (leoMenu.leoMenu):
	"""A class that represents a Leo window."""
	#@	@+others
	#@+node:leoTkinterMenu.__init__
	def __init__ (self,frame):
		
		# Init the base class.
		leoMenu.leoMenu.__init__(self,frame)
		
		self.top = frame.top
		self.c = frame.c
		self.frame = frame
	#@nonl
	#@-node:leoTkinterMenu.__init__
	#@+node:Tkinter menu bindings
	# See the Tk docs for what these routines are to do
	#@nonl
	#@-node:Tkinter menu bindings
	#@+node:add_cascade
	def add_cascade (self,parent,label,menu,underline):
		
		"""Wrapper for the Tkinter add_cascade menu method."""
		
		return parent.add_cascade(label=label,menu=menu,underline=underline)
	
	#@-node:add_cascade
	#@+node:add_command
	def add_command (self,menu,**keys):
		
		"""Wrapper for the Tkinter add_command menu method."""
	
		return menu.add_command(**keys)
		
	#@-node:add_command
	#@+node:add_separator
	def add_separator(self,menu):
		
		"""Wrapper for the Tkinter add_separator menu method."""
	
		menu.add_separator()
		
	#@-node:add_separator
	#@+node:bind
	def bind (self,bind_shortcut,callback):
		
		"""Wrapper for the Tkinter bind menu method."""
	
		return self.top.bind(bind_shortcut,callback)
		
	#@-node:bind
	#@+node:delete
	def delete (self,menu,realItemName):
		
		"""Wrapper for the Tkinter delete menu method."""
	
		return menu.delete(realItemName)
	#@nonl
	#@-node:delete
	#@+node:delete_range
	def delete_range (self,menu,n1,n2):
		
		"""Wrapper for the Tkinter delete menu method."""
	
		return menu.delete(n1,n2)
	
	#@-node:delete_range
	#@+node:destroy
	def destroy (self,menu):
		
		"""Wrapper for the Tkinter destroy menu method."""
	
		return menu.destroy()
	
	#@-node:destroy
	#@+node:insert_cascade
	def insert_cascade (self,parent,index,label,menu,underline):
		
		"""Wrapper for the Tkinter insert_cascade menu method."""
		
		return parent.insert_cascade(
			index=index,label=label,
			menu=menu,underline=underline)
	
	
	#@-node:insert_cascade
	#@+node:new_menu
	def new_menu(self,parent,tearoff=false):
		
		"""Wrapper for the Tkinter new_menu menu method."""
	
		return Tkinter.Menu(parent,tearoff=tearoff)
	#@nonl
	#@-node:new_menu
	#@+node:createMenuBar
	def createMenuBar(self,frame):
	
		top = frame.top
		topMenu = Tkinter.Menu(top,postcommand=self.updateAllMenus)
		
		# Do gui-independent stuff.
		self.setMenu("top",topMenu)
		self.createMenusFromTables()
		
		top.config(menu=topMenu) # Display the menu.
	#@nonl
	#@-node:createMenuBar
	#@+node:createOpenWithMenuFromTable
	#@+at 
	#@nonl
	# Entries in the table passed to createOpenWithMenuFromTable are
	# tuples of the form (commandName,shortcut,data).
	# 
	# - command is one of "os.system", "os.startfile", "os.spawnl", 
	# "os.spawnv" or "exec".
	# - shortcut is a string describing a shortcut, just as for 
	# createMenuItemsFromTable.
	# - data is a tuple of the form (command,arg,ext).
	# 
	# Leo executes command(arg+path) where path is the full path to the temp 
	# file.
	# If ext is not None, the temp file has the given extension.
	# Otherwise, Leo computes an extension based on the @language directive in 
	# effect.
	#@-at
	#@@c
	
	def createOpenWithMenuFromTable (self,table):
	
		app.openWithTable = table # Override any previous table.
		# Delete the previous entry.
		parent = self.getMenu("File")
		label = self.getRealMenuName("Open &With...")
		amp_index = label.find("&")
		label = label.replace("&","")
		try:
			index = parent.index(label)
			parent.delete(index)
		except:
			try:
				index = parent.index("Open With...")
				parent.delete(index)
			except: return
		# Create the "Open With..." menu.
		openWithMenu = Tkinter.Menu(parent,tearoff=0)
		self.setMenu("Open With...",openWithMenu)
		parent.insert_cascade(index,label=label,menu=openWithMenu,underline=amp_index)
		# Populate the "Open With..." menu.
		shortcut_table = []
		for triple in table:
			if len(triple) == 3: # 6/22/03
				shortcut_table.append(triple)
			else:
				es("createOpenWithMenuFromTable: invalid data",color="red")
				return
				
		# for i in shortcut_table: print i
		self.createMenuItemsFromTable("Open &With...",shortcut_table,openWith=1)
	#@-node:createOpenWithMenuFromTable
	#@+node:defineMenuCallback
	def defineMenuCallback(self,command,name):
		
		# The first parameter must be event, and it must default to None.
		def callback(event=None,self=self,command=command,label=name):
			return self.c.doCommand(command,label,event)
	
		return callback
	#@nonl
	#@-node:defineMenuCallback
	#@+node:defineOpenWithMenuCallback
	def defineOpenWithMenuCallback(self,command):
		
		# The first parameter must be event, and it must default to None.
		def callback(event=None,self=self,data=command):
			return self.c.openWith(data=data)
	
		return callback
	#@nonl
	#@-node:defineOpenWithMenuCallback
	#@+node:disableMenu
	def disableMenu (self,menu,name):
		
		try:
			menu.entryconfig(name,state="disabled")
		except: 
			try:
				realName = self.getRealMenuName(name)
				realName = realName.replace("&","")
				menu.entryconfig(realName,state="disabled")
			except:
				print "disableMenu menu,name:",menu,name
				es_exception()
				pass
	#@-node:disableMenu
	#@+node:enableMenu
	# Fail gracefully if the item name does not exist.
	
	def enableMenu (self,menu,name,val):
		
		state = choose(val,"normal","disabled")
		try:
			menu.entryconfig(name,state=state)
		except:
			try:
				realName = self.getRealMenuName(name)
				realName = realName.replace("&","")
				menu.entryconfig(realName,state=state)
			except:
				print "enableMenu menu,name,val:",menu,name,val
				es_exception()
				pass
	#@nonl
	#@-node:enableMenu
	#@+node:setMenuLabel
	def setMenuLabel (self,menu,name,label,underline=-1):
	
		try:
			if type(name) == type(0):
				# "name" is actually an index into the menu.
				menu.entryconfig(name,label=label,underline=underline)
			else:
				# Bug fix: 2/16/03: use translated name.
				realName = self.getRealMenuName(name)
				realName = realName.replace("&","")
				# Bug fix: 3/25/03" use tranlasted label.
				label = self.getRealMenuName(label)
				label = label.replace("&","")
				menu.entryconfig(realName,label=label,underline=underline)
		except:
			print "setMenuLabel menu,name,label:",menu,name,label
			es_exception()
			pass
	#@nonl
	#@-node:setMenuLabel
	#@-others
#@nonl
#@-node:@file leoTkinterMenu.py
#@-leo
