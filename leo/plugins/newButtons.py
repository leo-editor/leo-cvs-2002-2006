#@+leo-ver=4-thin
#@+node:pap.20051010170720:@thin newButtons.py
#@<< docstring >>
#@+node:pap.20051010170720.1:<< docstring >>
"""Allows the use of template nodes for common tasks

Template nodes can be create for any node. The template can then
be inserted at the click of a button. This is a bit like a permanent
clipboard except that templates can have items in them which can 
be overriden. Nodes can contain any number of child nodes.

For instance you might want to have a template for a unit test method.
The unit test method template includes a name and description. When
you create an instance of the template these items can be specified.

To override items in the template you insert strings with the following
form::
            $$expr$$
            
These strings can be anywhere in the headline or body text. The *expr*
is an expression which will be evaluated in a namespace containing two
existing names,

    name = the name entered into the entry box in the toolbar
    node = the leo Vnode that was selected when the *New* button was pressed
    
You can use this in many way, eg to create a custom file from a template::
    
    @thin $$name$$.py   <- in the headline text
    
Or to create a unit test node (using methods of the *name* object)::
    
    @thin test$$name.lower()$$
    < body text >
       class $$name$$:   <- in a child node
       
The following menu items are available:
    
MakeTemplateFrom
    Create a template from the current node. You will be asked to enter the
    name for the template.
    
UpdateTemplateFrom
    Update a specific template from the current node. You will be asked
    to select the template to update.
    
DeleteTemplate
    Delete a specific template. You will be asked to select the template to delete.
    
AddRawTemplate
    Adds the contents of a template to the outline but doesn't convert the
    $$name$$ values. This is useful for updating a template using UpdateTemplateFrom
    at a later stage.

"""
#@nonl
#@-node:pap.20051010170720.1:<< docstring >>
#@nl

__name__ = "New Buttons"
__version__ = "0.5"

USE_FIXED_SIZES = 1

#@<< version history >>
#@+node:pap.20051010170720.2:<< version history >>
#@@killcolor
#@+at
# 
# # 0.1 Paul Paterson: First version
# # 0.2 EKR: Converted to @file-noref
# # 0.3 EKR: Added 6 new plugin templates.  Added init function.
# # 0.4 EKR: Added importLeoGlobals function.
# # 0.5 Paul Paterson: Rewrite from scratch
#@-at
#@nonl
#@-node:pap.20051010170720.2:<< version history >>
#@nl

#@<< imports >>
#@+node:pap.20051010170720.3:<< imports >>
import leoGlobals as g
import leoPlugins

import os
import glob
import re

# Whatever other imports your plugins uses.
try:
    Tk = g.importExtension('Tkinter',pluginName=__name__,verbose=True)
    Pmw = g.importExtension("Pmw",    pluginName=__name__,verbose=True)    
except ImportError:
    Tk = None
#@-node:pap.20051010170720.3:<< imports >>
#@nl

#@+others
#@+node:pap.20051010170720.4:init
def init ():
    
    ok = True # This might depend on imports, etc.
    
    if ok:
        leoPlugins.registerHandler('after-create-leo-frame',onStart2)
        g.plugin_signon("newButtons")
            
    return ok
#@nonl
#@-node:pap.20051010170720.4:init
#@+node:pap.20051010170720.5:onStart2
def onStart2 (tag, keywords):
    
    """
    Showing how to define a global hook that affects all commanders.
    """

    import leoTkinterFrame
    log = leoTkinterFrame.leoTkinterLog
    
    # Ensure that the templates folder is there
    folder = g.os_path_join(g.app.loadDir,"..","plugins", "templates")
    try:
        os.mkdir(folder)
    except OSError, err:
        pass # Ok if it is there already

    global helper
    helper = UIHelperClass(folder)
    helper.addWidgets(tag, keywords)
    helper.commander = keywords.get("c")
    
    
#@nonl
#@-node:pap.20051010170720.5:onStart2
#@+node:pap.20051011221702:Commands exposed as menus
#@+node:pap.20051010172840:cmd_MakeTemplateFrom
def cmd_MakeTemplateFrom():
    """Make a template from a node"""
    helper.commander = g.top()
    helper.makeTemplate()
#@nonl
#@-node:pap.20051010172840:cmd_MakeTemplateFrom
#@+node:pap.20051011153949:cmd_UpdateTemplateFrom
def cmd_UpdateTemplateFrom():
    """Update a template from a node"""
    helper.commander = g.top()
    helper.updateTemplate()
#@nonl
#@-node:pap.20051011153949:cmd_UpdateTemplateFrom
#@+node:pap.20051011155514:cmd_DeleteTemplate
def cmd_DeleteTemplate():
    """Delete a template"""
    helper.commander = g.top()
    helper.deleteTemplate()
#@nonl
#@-node:pap.20051011155514:cmd_DeleteTemplate
#@+node:pap.20051011160100:cmd_AddRawTemplate
def cmd_AddRawTemplate():
    """Add a raw template"""
    helper.commander = g.top()
    helper.addRawTemplate()
#@nonl
#@-node:pap.20051011160100:cmd_AddRawTemplate
#@-node:pap.20051011221702:Commands exposed as menus
#@+node:pap.20051010171746:UI
#@+node:pap.20051010171746.1:FlatOptionMenu
class FlatOptionMenu(Tk.OptionMenu):
    """Flat version of OptionMenu which allows the user to select a value from a menu."""

    def __init__(self, master, variable, value, *values, **kwargs):
        """Construct an optionmenu widget with the parent MASTER, with 
        the resource textvariable set to VARIABLE, the initially selected 
        value VALUE, the other menu values VALUES and an additional 
        keyword argument command.""" 
        kw = {
            "borderwidth": 2, "textvariable": variable,
            "indicatoron": 1, "relief": "flat", "anchor": "c",
            "highlightthickness": 2}
        Tk.Widget.__init__(self, master, "menubutton", kw)
        self.widgetName = 'tk_optionMenu' 
        menu = self.__menu = Tk.Menu(self, name="menu", tearoff=0)
        self.menuname = menu._w
        # 'command' is the only supported keyword 
        callback = kwargs.get('command')
        if kwargs.has_key('command'):
            del kwargs['command']
        if kwargs:
            raise TclError, 'unknown option -'+kwargs.keys()[0]
        self["menu"] = menu
        self.__variable = variable
        self.__callback = callback
        self.addMenuItem(value)
        for v in values:
            self.addMenuItem(v)
    
    def addMenuItem(self, name):
        """Add an item to the menu"""
        self.__menu.add_command(label=name,
                command=Tk._setit(self.__variable, name, self.__callback))
#@-node:pap.20051010171746.1:FlatOptionMenu
#@+node:pap.20051010171746.2:UIHelper
class UIHelperClass:
    """Helper class to collect all UI functions"""
    
    #@    @+others
    #@+node:pap.20051010173622:__init__
    def __init__(self, folder):
        """Initialize the helper"""
        self.folder = folder
        self.templates = TemplateCollection(folder)
    #@nonl
    #@-node:pap.20051010173622:__init__
    #@+node:pap.20051010171746.3:addWidgets
    def addWidgets(self, tags, keywords):
        """Add the widgets to Leo"""
        self.commander = keywords['c']
        toolbar = self.commander.frame.iconFrame
        # 
        self.frame = Tk.Frame(toolbar)
        self.frame.pack(side="right", padx=2)
        # 
        self.text = Tk.Entry(self._getSizer(self.frame, 24, 130))
        self.text.pack(side="left", padx=3, fill="both", expand=1)
        self.text.bind("<Return>", self.newItemClicked)
        # 
        self.pseudobutton = Tk.Frame(self._getSizer(self.frame, 24, 142),
            relief="raised", borderwidth=2) 
        self.pseudobutton.pack(side="right")
        # 
        self.doit = Tk.Button(self._getSizer(self.pseudobutton, 25, 32),
            text="New", relief="flat", command=self.newItemClicked)
        self.doit.pack(side="left")
        # 
        options = [template.name for template in self.templates] or ["Template?"]
        options.sort()
        self.option_value = Tk.StringVar()
        self.options = FlatOptionMenu(self._getSizer(self.pseudobutton, 29, 110),
            self.option_value, *options)
        self.option_value.set(options[0])
        self.options.pack(side="right", fill="both", expand=1)
    #@-node:pap.20051010171746.3:addWidgets
    #@+node:pap.20051010171746.4:newItemClicked
    def newItemClicked(self, event=None):
        """Generate a callback to call the specific adder"""
        nodename = self.option_value.get()
        if nodename == "Template?":
            pass
        else:
            self.addTemplate(nodename, self.text.get())
    #@-node:pap.20051010171746.4:newItemClicked
    #@+node:pap.20051011160416:addTemplate
    def addTemplate(self, name, parameter=None):
        """Add a template node"""
        self.commander = g.top()
        node = self.commander.currentVnode()
        template = self.templates.find(name)
        if template:
            template.addNodes(self.commander, node, parameter)
    #@-node:pap.20051011160416:addTemplate
    #@+node:pap.20051010175537:makeTemplate
    def makeTemplate(self):
        """Make a template from the current node"""
        def makeit(result):
            if result is not None:
                node = self.commander.currentVnode()
                template = Template.fromNode(node, name=result)
                template.save()
                self.templates.append(template)
                self.options.addMenuItem(template.name)
                        
        form = MakeTemplateForm(makeit)
        
    #@-node:pap.20051010175537:makeTemplate
    #@+node:pap.20051011155041:updateTemplate
    def updateTemplate(self):
        """Update a template from the current node"""
        def updateit(result):
            if result is not None:
                # Remove old one
                self.templates.remove(self.templates.find(result))
                # Now create a new one
                node = self.commander.currentVnode()
                newtemplate = Template.fromNode(node, name=result)
                newtemplate.save()
                self.templates.append(newtemplate)
                         
        form = SelectTemplateForm(updateit, "Update template")
        
    #@-node:pap.20051011155041:updateTemplate
    #@+node:pap.20051011160416.1:addRawTemplate
    def addRawTemplate(self):
        """Add a template but don't convert the text"""
        def addraw(result):
            if result is not None:
                self.addTemplate(result)
                         
        form = SelectTemplateForm(addraw, "Add raw template")
        
    #@-node:pap.20051011160416.1:addRawTemplate
    #@+node:pap.20051011155642:deleteTemplate
    def deleteTemplate(self):
        """Delete a template"""
        def deleteit(result):
            if result is not None:
                # Remove old one
                self.templates.remove(self.templates.find(result))
                os.remove(g.os_path_join(self.folder, "%s.tpl" % result))
                         
        form = SelectTemplateForm(deleteit, "Delete template")
        
    #@-node:pap.20051011155642:deleteTemplate
    #@+node:pap.20051010172432:_getSizer
    def _getSizer(self, parent, height, width, pack="left"):
        """Return a sizer object to force a Tk widget to be the right size"""
        if USE_FIXED_SIZES:
            sizer = Tk.Frame(parent, height=height, width=width)
            sizer.pack_propagate(0) # don't shrink 
            sizer.pack(side=pack)
            return sizer
        else:
            return parent
    #@-node:pap.20051010172432:_getSizer
    #@-others
    
    
#@nonl
#@-node:pap.20051010171746.2:UIHelper
#@+node:pap.20051011154233:HelperForm
class HelperForm:
    """Base class for all forms"""
    
    #@    @+others
    #@+node:pap.20051011154400:__init__
    def __init__(self, callback, title):
        """Initialise the form"""
        self.root = root = g.app.root
        self.callback = callback
        
        self.dialog = dialog = Pmw.Dialog(root,
                buttons = ('OK', 'Cancel'),
                defaultbutton = 'OK',
                title = title,
                command = self.formCommit,
        )
        
    #@-node:pap.20051011154400:__init__
    #@+node:pap.20051011154642:formCommit
    def formCommit(self, name):
        """The user closed the form"""
        if name == "OK":
            result = self.getResult()
        else:
            result = None
        self.dialog.destroy() 
        self.callback(result)
           
    #@nonl
    #@-node:pap.20051011154642:formCommit
    #@-others
#@nonl
#@-node:pap.20051011154233:HelperForm
#@+node:pap.20051010195044:MakeTemplateForm
class MakeTemplateForm(HelperForm):
    """A form to initialize a template"""
    
    #@    @+others
    #@+node:pap.20051010195044.1:__init__
    def __init__(self, callback):
        """Initialise the form"""
        HelperForm.__init__(self, callback, "Add new template")
        
        parent = self.dialog.interior()
        
        def isvalid(x):
            if len(x) > 1:
                return 1
            else:
                return -1
                
        self.name = Pmw.EntryField(parent,
                labelpos = 'w',
                label_text = 'Template name:',
                validate = isvalid,
        )
        
        self.getResult = self.name.getvalue
        
        entries = (self.name, )
        
        for entry in entries:
            entry.pack(fill='x', expand=1, padx=10, pady=5)
        
        Pmw.alignlabels(entries)
    
    #@-node:pap.20051010195044.1:__init__
    #@-others
    
    
#@-node:pap.20051010195044:MakeTemplateForm
#@+node:pap.20051011153949.1:SelectTemplateForm
class SelectTemplateForm(HelperForm):
    """A form to select a template"""
    
    #@    @+others
    #@+node:pap.20051011154233.1:__init__
    def __init__(self, callback, title):
        """Initialise the form"""
        HelperForm.__init__(self, callback, title)
                
        self.name = Pmw.OptionMenu(self.dialog.interior(),
                labelpos = 'w',
                label_text = 'Template name:',
                items = [template.name for template in helper.templates] or ["Template?"],
                menubutton_width = 10,
        )
        
        self.getResult = self.name.getvalue
        
        entries = (self.name, )
        
        for entry in entries:
            entry.pack(fill='x', expand=1, padx=10, pady=5)
        
        Pmw.alignlabels(entries)
    #@-node:pap.20051011154233.1:__init__
    #@-others
#@nonl
#@-node:pap.20051011153949.1:SelectTemplateForm
#@-node:pap.20051010171746:UI
#@+node:pap.20051010173800:Implementation
#@+node:pap.20051010173800.1:TemplateCollection
class TemplateCollection(list):
    """Represents a collection of templates"""
    
    #@    @+others
    #@+node:pap.20051010173800.2:__init__
    def __init__(self, folder):
        """Initialize the collection"""
        self.folder = folder
        for name in glob.glob(g.os_path_join(folder, "*.tpl")):
            self.append(Template.fromFile(name))
    #@-node:pap.20051010173800.2:__init__
    #@+node:pap.20051010183939:find
    def find(self, name):
        """Return the named template"""
        for item in self:
            if item.name == name:
                return item
        return None
    #@nonl
    #@-node:pap.20051010183939:find
    #@-others
#@nonl
#@-node:pap.20051010173800.1:TemplateCollection
#@+node:pap.20051010174103:Template
class Template:
    """Represents a template"""
    
    #@    @+others
    #@+node:pap.20051010180444:__init__
    def __init__(self, headline="", body="", children=None, name=None):
        """Initialize the template"""
        self.name = name
        self.headline = headline
        self.body = body
        if children is None:
            self.children = []
        else:
            self.children = children
    #@nonl
    #@-node:pap.20051010180444:__init__
    #@+node:pap.20051010174103.1:fromFile
    def fromFile(filename):
        """Return a new tempalte from a file"""
        text = file(filename, "r").read()
        return eval(text)
        
    fromFile = staticmethod(fromFile)    
    #@nonl
    #@-node:pap.20051010174103.1:fromFile
    #@+node:pap.20051010180304:fromNode
    def fromNode(node, name=None):
        """Return a new template from a node"""
        template = Template()
        template.name = name
        template.headline = node.headString()
        template.body = node.bodyString()
        #
        # Find children
        template.children = children = []
        child = node.getFirstChild()
        while child:
            children.append(Template.fromNode(child))
            child = child.getNext()
        #
        return template
            
    fromNode = staticmethod(fromNode)    
    #@nonl
    #@-node:pap.20051010180304:fromNode
    #@+node:pap.20051010184315:addNodes
    def addNodes(self, commander, parent=None, parameter=""):
        """Add this template to the current"""
        #
        # Add this new node
        commander.insertHeadline()
        newnode = commander.currentVnode()
        newnode.setHeadString(self.convert(self.headline, parameter, parent))
        newnode.setBodyString(self.convert(self.body, parameter, parent))
        #
        # Make it the child of its parent
        if parent:
            newnode.moveToNthChildOf(parent, 0)
        #
        # Now add the children - go in reverse so we can add them as child 0 (above)
        children = self.children[:]
        children.reverse()
        for child in children:
            child.addNodes(commander, newnode, parameter)
        
    
    #@-node:pap.20051010184315:addNodes
    #@+node:pap.20051010182048:save
    def save(self):
        """Save this template"""
        filename = g.os_path_join(g.app.loadDir,"..","plugins", "templates", 
                    "%s.tpl" % self.name)
        f = file(filename, "w")
        try:
            f.write(repr(self))
        finally:
            f.close()
    #@-node:pap.20051010182048:save
    #@+node:pap.20051010181808:repr
    def __repr__(self):
        """Return representation of this node"""
        return "Template(%s, %s, %s, %s)" % (
                repr(self.headline), 
                repr(self.body), 
                repr(self.children),
                repr(self.name))            
    #@nonl
    #@-node:pap.20051010181808:repr
    #@+node:pap.20051010205823:convert
    def convert(self, text, parameter, node):
        """Return the converted text"""
        if parameter is None:
            return text
            
        matcher = re.compile("(.*)\$\$(.+?)\$\$(.*)", re.DOTALL+re.MULTILINE)
        namespace = {
            "name" : parameter,
            "node" : node,
        }
        
        def replacer(match):
            try:
                result = eval(match.groups()[1], namespace)
            except Exception, err:
                g.es("Unable to replace '%s': %s" % (match.groups()[1], err), color="red")
                result = "*ERROR*"
            return "%s%s%s" % (match.groups()[0], result, match.groups()[2])
        oldtext = text    
        while True:
            text = matcher.sub(replacer, text)
            if text == oldtext: break
            oldtext = text
    
        return text
        
    
    #@-node:pap.20051010205823:convert
    #@-others
#@nonl
#@-node:pap.20051010174103:Template
#@-node:pap.20051010173800:Implementation
#@-others
#@nonl
#@-node:pap.20051010170720:@thin newButtons.py
#@-leo
