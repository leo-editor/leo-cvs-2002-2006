#@+leo-ver=4-thin
#@+node:EKR.20040517080555.2:@thin plugins_menu.py
"""Create a Plugins menu

Adds an item to the plugin menu for each active plugin. Selecting
this menu item will bring up a short About dialog with the details of the
plugin.

Plugins can create additional menu items by defining functions named
"cmd_XZY". These will apear in a sub menu. 

If the plugin requires an INI file then a configure menu item will be
created which will show an INI file editor. the plugin can define an
"applyConfiguration" function, which will be called when the configuration 
changes.

Plugins can also define a top level function to be called instead of
the default "About" dialog by defining a "topLevelMenu" function in
the plugin. This function will be called when the user clicks on the
plugin name in the plugins menu. 

Plugins can define their name by setting the __plugin_name__ property.

Plugins can also attempt to select the order they will apear in the menu
by defining a __plugin_prioriy__. The menu will be created with the
highest priority items first. This behaviour is not guaranteed since
other plugins can define any priority. This priority does not affect
the order of calling handlers.

To change the order select a number outside the range 0-200 since this
range is used internally for sorting alphabetically.

"""

#@@language python
#@@tabwidth -4

# Written by Paul A. Paterson.  Revised by Edward K. Ream.

## To do: add Revert button to each dialog.

import leoGlobals as g
import leoPlugins

import ConfigParser
import glob
import os
import sys

__plugin_name__ = "Plugins Menu"
__plugin_priority__ = -100

try: import Tkinter as Tk
except ImportError: Tk = None

#@+others
#@+node:EKR.20040517080555.3:class Plugin
class PlugIn:

    """A class to hold information about one plugin"""

    #@    @+others
    #@+node:EKR.20040517080555.4:__init__
    def __init__(self, filename):
    
        """Initialize the plug-in"""
    
        # Import the file to find out some interesting stuff
        # Do not use the imp module: we only want to import these files once!
        self.mod = self.doc = self.version = None
        try:
            self.mod = __import__(g.os_path_splitext(g.os_path_basename(filename))[0])
            if not self.mod:
                return
            try:
                self.name = self.mod.__plugin_name__
            except AttributeError:
                self.name = self.mod.__name__
            try:
                self.priority = self.mod.__plugin_priority__
            except AttributeError:
                self.priority = 200 - ord(self.name[0])
            #
            self.doc = self.mod.__doc__
            self.version = self.mod.__dict__.get("__version__") # "<unknown>")
            # if self.version: print self.version,g.shortFileName(filename)
        except: return
    
        #@    << Check if this can be configured >>
        #@+node:EKR.20040517080555.5:<< Check if this can be configured >>
        # Look for a configuration file
        self.configfilename = "%s.ini" % os.path.splitext(filename)[0]
        self.hasconfig = os.path.isfile(self.configfilename)
        #@-node:EKR.20040517080555.5:<< Check if this can be configured >>
        #@nl
        #@    << Check if this has an apply >>
        #@+node:EKR.20040517080555.6:<< Check if this has an apply >>
        #@+at 
        #@nonl
        # Look for an apply function ("applyConfiguration") in the module.
        # 
        # This is used to apply changes in configuration from the properties 
        # window
        #@-at
        #@@c
        
        self.hasapply = hasattr(self.mod, "applyConfiguration")
        #@-node:EKR.20040517080555.6:<< Check if this has an apply >>
        #@nl
        #@    << Look for additional commands >>
        #@+node:EKR.20040517080555.7:<< Look for additional commands >>
        #@+at 
        #@nonl
        # Additional commands can be added to the plugin menu by having 
        # functions in the module called "cmd_whatever". These are added to 
        # the main menu and will be called when clicked
        #@-at
        #@@c
        
        self.othercmds = {}
        
        for item in self.mod.__dict__.keys():
            if item.startswith("cmd_"):
                self.othercmds[item[4:]] = self.mod.__dict__[item]
        #@-node:EKR.20040517080555.7:<< Look for additional commands >>
        #@nl
        #@    << Look for toplevel menu item >>
        #@+node:pap.20041009131822:<< Look for toplevel menu item >>
        #@+at 
        #@nonl
        # Check to see if there is a toplevel menu item - this will be used 
        # instead of the default About
        #@-at
        #@@c
        
        try:
            self.hastoplevel = self.mod.__dict__["topLevelMenu"]
        except KeyError:
            self.hastoplevel = False
        #@nonl
        #@-node:pap.20041009131822:<< Look for toplevel menu item >>
        #@nl
    #@nonl
    #@-node:EKR.20040517080555.4:__init__
    #@+node:EKR.20040517080555.8:about
    def about(self,event=None):
        
        """Put up an "about" dialog for this plugin"""
    
        PluginAbout(self.name, self.version, self.doc)
    #@nonl
    #@-node:EKR.20040517080555.8:about
    #@+node:EKR.20040517080555.9:properties
    def properties(self, event=None):
        
        """Create a modal properties dialog for this plugin"""
    
        PropertiesWindow(self.configfilename, self)
    #@nonl
    #@-node:EKR.20040517080555.9:properties
    #@-others
    
#@-node:EKR.20040517080555.3:class Plugin
#@+node:EKR.20040517080555.10:class PropertiesWindow
class PropertiesWindow:

    """A class to create and run a Properties dialog for a plugin"""

    #@    @+others
    #@+node:EKR.20040517080555.11:__init__
    def __init__(self, filename, plugin):
    
        """Initialize the property window"""
        
        #@    << initialize all ivars >>
        #@+node:EKR.20040517080555.12:<< initialize all ivars >>
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
        #@-node:EKR.20040517080555.12:<< initialize all ivars >>
        #@nl
        #@    << create the frame from the configuration data >>
        #@+node:EKR.20040517080555.13:<< create the frame from the configuration data >>
        root = g.app.root
        
        #@<< Create the top level and the main frame >>
        #@+node:EKR.20040517080555.14:<< Create the top level and the main frame >>
        self.top = top = Tk.Toplevel(root)
        g.app.gui.attachLeoIcon(self.top)
        top.title("Properties of "+ plugin.name)
        top.resizable(0,0) # neither height or width is resizable.
            
        self.frame = frame = Tk.Frame(top)
        frame.pack(side="top")
        #@nonl
        #@-node:EKR.20040517080555.14:<< Create the top level and the main frame >>
        #@nl
        #@<< Create widgets for each section and option >>
        #@+node:EKR.20040517080555.15:<< Create widgets for each section and option >>
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
                e.insert(0, unicode(config.get(section,option))) # 6/8/04
                Tk.Label(b, text=option).grid(row=row, column=0, sticky="e", pady=4)
                e.grid(row=row, column=1, sticky="ew", pady = 4)
                row += 1
                self.entries.append((section, option, e))
        #@nonl
        #@-node:EKR.20040517080555.15:<< Create widgets for each section and option >>
        #@nl
        #@<< Create Ok, Cancel and Apply buttons >>
        #@+node:EKR.20040517080555.16:<< Create Ok, Cancel and Apply buttons >>
        box = Tk.Frame(top, borderwidth=5)
        box.pack(side="bottom")
        
        list = [("OK",self.onOk),("Cancel",top.destroy)]
        if plugin.hasapply:
            list.append(("Apply",self.onApply),)
        
        for text,f in list:
            Tk.Button(box,text=text,width=6,command=f).pack(side="left",padx=5)
        #@nonl
        #@-node:EKR.20040517080555.16:<< Create Ok, Cancel and Apply buttons >>
        #@nl
        
        g.app.gui.center_dialog(top) # Do this after packing.
        top.grab_set() # Make the dialog a modal dialog.
        top.focus_force() # Get all keystrokes.
        root.wait_window(top)
        #@nonl
        #@-node:EKR.20040517080555.13:<< create the frame from the configuration data >>
        #@nl
    #@nonl
    #@-node:EKR.20040517080555.11:__init__
    #@+node:EKR.20040517080555.17:Event Handlers
    def onApply(self):
        
        """Event handler for Apply button"""
        self.writeConfiguration()
        self.plugin.mod.applyConfiguration(self.config)
    
    def onOk(self):
    
        """Event handler for Ok button"""
        self.writeConfiguration()
        self.top.destroy()
    #@nonl
    #@-node:EKR.20040517080555.17:Event Handlers
    #@+node:EKR.20040517080555.18:writeConfiguration
    def writeConfiguration(self):
        
        """Write the configuration to disk"""
    
        # Set values back into the config item.
        for section, option, entry in self.entries:
            s = entry.get()
            s = g.toEncodedString(s,"ascii",reportErrors=True) # Config params had better be ascii.
            self.config.set(section,option,s)
    
        # Write out to the file.
        f = open(self.filename, "w")
        self.config.write(f)
        f.close()
    #@nonl
    #@-node:EKR.20040517080555.18:writeConfiguration
    #@-others
#@nonl
#@-node:EKR.20040517080555.10:class PropertiesWindow
#@+node:EKR.20040517080555.19:class PluginAbout
class PluginAbout:
    
    """A class to create and run an About Plugin dialog"""
    
    #@    @+others
    #@+node:EKR.20040517080555.20:__init__
    def __init__(self, name, version, about):
        
        """# Create and run a modal dialog giving the name,
        version and description of a plugin.
        """
    
        root = g.app.root
        self.top = top = Tk.Toplevel(root)
        g.app.gui.attachLeoIcon(self.top)
        top.title("About " + name)
        top.resizable(0,0) # neither height or width is resizable.
        
        frame = Tk.Frame(top)
        frame.pack(side="top")
        #@    << Create the contents of the about box >>
        #@+node:EKR.20040517080555.21:<< Create the contents of the about box >>
        Tk.Label(frame, text="Version " + version).pack()
        
        Tk.Label(frame, text=about, borderwidth=10,justify="left").pack()
        #@nonl
        #@-node:EKR.20040517080555.21:<< Create the contents of the about box >>
        #@nl
        #@    << Create the close button >>
        #@+node:EKR.20040517080555.22:<< Create the close button >>
        buttonbox = Tk.Frame(top, borderwidth=5)
        buttonbox.pack(side="bottom")
        
        self.button = Tk.Button(buttonbox, text="Close", command=top.destroy)
        self.button.pack(side="bottom")
        #@nonl
        #@-node:EKR.20040517080555.22:<< Create the close button >>
        #@nl
        
        g.app.gui.center_dialog(top) # Do this after packing.
        top.grab_set() # Make the dialog a modal dialog.
        top.focus_force() # Get all keystrokes.
        root.wait_window(top)
    #@nonl
    #@-node:EKR.20040517080555.20:__init__
    #@-others
#@-node:EKR.20040517080555.19:class PluginAbout
#@+node:EKR.20040517080555.23:createPluginsMenu
def createPluginsMenu (tag,keywords):

    c = keywords.get("c")
    old_path = sys.path[:] # Make a _copy_ of the path.

    path = os.path.join(g.app.loadDir,"..","plugins")
    sys.path = path
    
    if os.path.exists(path):
        # Create a list of all active plugins.
        files = glob.glob(os.path.join(path,"*.py"))
        files.sort()
        plugins = [PlugIn(file) for file in files]
        items = [(p.name,p) for p in plugins if p.version]
        if items:
            #@            << Sort items >>
            #@+node:pap.20041009133925:<< sort items >>
            dec = [(item[1].priority, item) for item in items]
            dec.sort()
            dec.reverse()
            items = [item[1] for item in dec]
            #@nonl
            #@-node:pap.20041009133925:<< sort items >>
            #@nl
            c.pluginsMenu = pluginMenu = c.frame.menu.createNewMenu("&Plugins")
            #@            << add items to the plugins menu >>
            #@+node:EKR.20040517080555.24:<< add items to the plugins menu >>
            for name,p in items:
                if p.hastoplevel:
                    table = ((p.name, None, p.hastoplevel),)
                    c.frame.menu.createMenuEntries(pluginMenu, table)
                elif p.hasconfig or p.othercmds:
                    m = c.frame.menu.createNewMenu(p.name, "&Plugins")
                    table = [("About...", None, p.about)]
                    if p.hasconfig:
                        table.append(("Properties...", None, p.properties))
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
            #@-node:EKR.20040517080555.24:<< add items to the plugins menu >>
            #@nl
            
    sys.path = old_path


#@-node:EKR.20040517080555.23:createPluginsMenu
#@-others

if Tk and not g.app.unitTesting: # Register the handlers...

    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":
        leoPlugins.registerHandler("create-optional-menus",createPluginsMenu)
        
        __version__ = "1.4"
        g.plugin_signon(__name__)
#@nonl
#@-node:EKR.20040517080555.2:@thin plugins_menu.py
#@-leo
