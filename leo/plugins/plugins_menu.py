#@+leo-ver=4
#@+node:@file plugins_menu.py
"""Create a Plugins menu"""

#@@language python

# Written by Paul A. Paterson.  Revised by Edward K. Ream.

## To do: add Revert button to each dialog.

from leoPlugins import *
from leoGlobals import *
import ConfigParser,glob,os,sys

try:
	import Tkinter
except ImportError:
	Tkinter = None
Tk = Tkinter

if Tkinter: # Register the handlers...

	#@	@+others
	#@+node:class Plugin
	class PlugIn:
	
		"""A class to hold information about one plugin"""
	
		#@	@+others
		#@+node:__init__
		def __init__(self, filename):
		
			"""Initialize the plug-in"""
		
			# Import the file to find out some interesting stuff
			# Do not use the imp module: we only want to import these files once!
			self.mod = self.doc = self.version = None
			try:
				self.mod = __import__(os.path.splitext(os.path.basename(filename))[0])
				if not self.mod:
					return
				self.name = self.mod.__name__
				self.doc = self.mod.__doc__
				self.version = self.mod.__dict__.get("__version__") # "<unknown>")
				# if self.version: print self.version,shortFileName(filename)
			except: return
		
			#@	<< Check if this can be configured >>
			#@+node:<< Check if this can be configured >>
			# Look for a configuration file
			self.configfilename = "%s.ini" % os.path.splitext(filename)[0]
			self.hasconfig = os.path.isfile(self.configfilename)
			#@-node:<< Check if this can be configured >>
			#@nl
			#@	<< Check if this has an apply >>
			#@+node:<< Check if this has an apply >>
			#@+at 
			#@nonl
			# Look for an apply function ("applyConfiguration") in the module.
			# 
			# This is used to apply changes in configuration from the 
			# properties window
			#@-at
			#@@c
			
			self.hasapply = hasattr(self.mod, "applyConfiguration")
			#@-node:<< Check if this has an apply >>
			#@nl
			#@	<< Look for additional commands >>
			#@+node:<< Look for additional commands >>
			#@+at 
			#@nonl
			# Additional commands can be added to the plugin menu by having 
			# functions in the module called "cmd_whatever". These are added 
			# to the main menu and will be called when clicked
			#@-at
			#@@c
			
			self.othercmds = {}
			
			for item in self.mod.__dict__.keys():
				if item.startswith("cmd_"):
					self.othercmds[item[4:]] = self.mod.__dict__[item]
			#@-node:<< Look for additional commands >>
			#@nl
		#@nonl
		#@-node:__init__
		#@+node:about
		def about(self,event=None):
			
			"""Put up an "about" dialog for this plugin"""
		
			PluginAbout(self.name, self.version, self.doc)
		#@nonl
		#@-node:about
		#@+node:properties
		def properties(self, event=None):
			
			"""Create a modal properties dialog for this plugin"""
		
			PropertiesWindow(self.configfilename, self)
		#@nonl
		#@-node:properties
		#@-others
		
	#@-node:class Plugin
	#@+node:class PropertiesWindow
	class PropertiesWindow:
	
		"""A class to create and run a Properties dialog for a plugin"""
	
		#@	@+others
		#@+node:__init__
		def __init__(self, filename, plugin):
		
			"""Initialize the property window"""
			
			#@	<< initialize all ivars >>
			#@+node:<< initialize all ivars >>
			# config stuff.
			config = ConfigParser.ConfigParser()
			config.read(filename)
			self.filename = filename
			self.config = config
			self.plugin = plugin
			
			# self.entries is a list of tuples (section, option, e),
			# where section and options are strings and e is a Tk.Entry widget.
			# This list is used by writeConfiguration to write all settings.
			self.entries = []
			#@-node:<< initialize all ivars >>
			#@nl
			#@	<< create the frame from the configuration data >>
			#@+node:<< create the frame from the configuration data >>
			root = app.root
			
			#@<< Create the top level and the main frame >>
			#@+node:<< Create the top level and the main frame >>
			self.top = top = Tk.Toplevel(root)
			app.gui.attachLeoIcon(self.top)
			top.title("Properties of "+ plugin.name)
			top.resizable(0,0) # neither height or width is resizable.
				
			self.frame = frame = Tk.Frame(top)
			frame.pack(side="top")
			#@nonl
			#@-node:<< Create the top level and the main frame >>
			#@nl
			#@<< Create widgets for each section and option >>
			#@+node:<< Create widgets for each section and option >>
			# Create all the entry boxes on the screen to allow the user to edit the properties
			sections = config.sections()
			sections.sort()
			for section in sections:
				# Create a frame for the section.
				f = Tk.Frame(top, relief="groove",bd=2)
				f.pack(side="top",padx=5,pady=5)
				Tk.Label(f, text=section.capitalize()).pack(side="top")
				# Create an inner frame for the options.
				b = Tk.Frame(f)
				b.pack(side="top",padx=2,pady=2)
				# Create a Tk.Label and Tk.Entry for each option.
				options = config.options(section)
				options.sort()
				row = 0
				for option in options:
					e = Tk.Entry(b)
					e.insert(0, config.get(section, option))
					Tk.Label(b, text=option).grid(row=row, column=0, sticky="e", pady=4)
					e.grid(row=row, column=1, sticky="ew", pady = 4)
					row += 1
					self.entries.append((section, option, e))
			#@nonl
			#@-node:<< Create widgets for each section and option >>
			#@nl
			#@<< Create Ok, Cancel and Apply buttons >>
			#@+node:<< Create Ok, Cancel and Apply buttons >>
			box = Tk.Frame(top, borderwidth=5)
			box.pack(side="bottom")
			
			list = [("OK",self.onOk),("Cancel",top.destroy)]
			if plugin.hasapply:
				list.append(("Apply",self.onApply),)
			
			for text,f in list:
				Tk.Button(box,text=text,width=6,command=f).pack(side="left",padx=5)
			#@nonl
			#@-node:<< Create Ok, Cancel and Apply buttons >>
			#@nl
			
			app.gui.center_dialog(top) # Do this after packing.
			top.grab_set() # Make the dialog a modal dialog.
			top.focus_force() # Get all keystrokes.
			root.wait_window(top)
			#@nonl
			#@-node:<< create the frame from the configuration data >>
			#@nl
		#@nonl
		#@-node:__init__
		#@+node:Event Handlers
		def onApply(self):
			
			"""Event handler for Apply button"""
			self.writeConfiguration()
			self.plugin.mod.applyConfiguration(self.config)
		
		def onOk(self):
		
			"""Event handler for Ok button"""
			self.writeConfiguration()
			self.top.destroy()
		#@nonl
		#@-node:Event Handlers
		#@+node:writeConfiguration
		def writeConfiguration(self):
			
			"""Write the configuration to disk"""
		
			# Set values back into the config item.
			for section, option, entry in self.entries:
				self.config.set(section, option, entry.get())
		
			# Write out to the file.
			f = open(self.filename, "w")
			self.config.write(f)
			f.close()
		#@-node:writeConfiguration
		#@-others
	#@nonl
	#@-node:class PropertiesWindow
	#@+node:class PluginAbout
	class PluginAbout:
		
		"""A class to create and run an About Plugin dialog"""
		
		#@	@+others
		#@+node:__init__
		def __init__(self, name, version, about):
			
			"""# Create and run a modal dialog giving the name,
			version and description of a plugin.
			"""
		
			root = app.root
			self.top = top = Tk.Toplevel(root)
			app.gui.attachLeoIcon(self.top)
			top.title("About " + name)
			top.resizable(0,0) # neither height or width is resizable.
			
			frame = Tk.Frame(top)
			frame.pack(side="top")
			#@	<< Create the contents of the about box >>
			#@+node:<< Create the contents of the about box >>
			if 0: # The name is now in the window's title.
				Tk.Label(frame, text="Name:").grid(row=0, column=0, sticky="E")
				Tk.Label(frame, text=name).grid(row=0, column=1, sticky="W")
				Tk.Label(frame, text="Version").grid(row=1, column=0, sticky="E")
				Tk.Label(frame, text=version).grid(row=1, column=1, sticky="W")
				Tk.Label(frame, text=about, borderwidth=10, justify="left").grid(columnspan=2)
			else:
				Tk.Label(frame, text="Version " + version).pack()
				Tk.Label(frame, text=about, borderwidth=10).pack()
			#@nonl
			#@-node:<< Create the contents of the about box >>
			#@nl
			#@	<< Create the close button >>
			#@+node:<< Create the close button >>
			buttonbox = Tk.Frame(top, borderwidth=5)
			buttonbox.pack(side="bottom")
			
			self.button = Tk.Button(buttonbox, text="Close", command=top.destroy)
			self.button.pack(side="bottom")
			#@nonl
			#@-node:<< Create the close button >>
			#@nl
			
			app.gui.center_dialog(top) # Do this after packing.
			top.grab_set() # Make the dialog a modal dialog.
			top.focus_force() # Get all keystrokes.
			root.wait_window(top)
		#@nonl
		#@-node:__init__
		#@-others
	#@-node:class PluginAbout
	#@+node:createPluginsMenu
	def createPluginsMenu (tag,keywords):
	
		c = keywords.get("c")
		old_path = sys.path[:] # Make a _copy_ of the path.
	
		path = os.path.join(app.loadDir,"..","plugins")
		sys.path = path
		
		if os.path.exists(path):
			# Create a list of all active plugins.
			files = glob.glob(os.path.join(path,"*.py"))
			files.sort()
			plugins = [PlugIn(file) for file in files]
			items = [(p.name,p) for p in plugins if p.version]
			if items:
				items.sort()
				c.pluginsMenu = pluginMenu = c.frame.menu.createNewMenu("&Plugins")
				#@			<< add items to the plugins menu >>
				#@+node:<< add items to the plugins menu >>
				for name,p in items:
					if p.hasconfig:
						m = c.frame.menu.createNewMenu(p.name, "&Plugins")
						table = [("About...", None, p.about),
								 ("Properties...", None, p.properties)]
						if p.othercmds:
							table.append(("-", None, None))
							items = [(cmd,None,fn) for cmd,fn in p.othercmds.iteritems()]
							items.sort()
							table.extend(items)
						c.frame.menu.createMenuEntries(m, table)
					else:
						table = ((p.name, None, p.about),)
						c.frame.menu.createMenuEntries(pluginMenu, table)
				#@nonl
				#@-node:<< add items to the plugins menu >>
				#@nl
				
		sys.path = old_path
	
	
	#@-node:createPluginsMenu
	#@-others

	if app.gui is None:
		app.createTkGui(__file__)

	if app.gui.guiName() == "tkinter":
		registerHandler("create-optional-menus",createPluginsMenu)
		
		__version__ = "1.2"
		plugin_signon(__name__)
#@nonl
#@-node:@file plugins_menu.py
#@-leo
