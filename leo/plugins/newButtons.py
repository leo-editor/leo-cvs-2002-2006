#@+leo-ver=4
#@+node:@file-noref newButtons.py
'''Automatically add nodes for common tasks'''

# We must use @file-noref because data below might look like section references,
# so ORDER IS IMPORTANT throughout this tree (we can't use @others).

#@language python
#@tabwidth -4

__name__ = "New Buttons"
__version__ = "0.2" # Converted to @file-noref by EKR.
 
import leoGlobals as g
import leoPlugins
import leoFind

Tk = g.importExtension('Tkinter',pluginName=__name__,verbose=True)

# N.B. We can NOT put the top-level code here: we are using @nosent!
#@nonl
#@-node:@file-noref newButtons.py
#@+node:Helper classes
"""Classes to add helpers to the toolbar 
 
A helper is a class that adds a set of preconfigured nodes to the outline. This 
can be used to generate boiler plate code to quickly build an outline. The nodes 
and body text added can have an adjustable parameter, which is defined from 
the text entry box. 
 
"""

USE_FIXED_SIZES = 1
#@nonl
#@-node:Helper classes
#@+node:class FlatOptionMenu
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
        menu.add_command(label=value,
            command=Tk._setit(variable, value, callback))
        for v in values:
            menu.add_command(label=v,
                command=Tk._setit(variable, v, callback))
        self["menu"] = menu
#@nonl
#@-node:class FlatOptionMenu
#@+node:class Node
class Node: 
    """A node to add"""

    def __init__(self, name="", body="", inherit=0, subnodes=None):
        """Initialise the node"""
        self.name = name
        self.body = body
        self.subnodes = subnodes or []
        self.inherit = inherit # Set True to inherit the first line from our immediate sibling 

    def processText(self, text, name):
        """Process some boiler plate text"""
        if name: 
            text = text.replace("XXX", name)
            text = text.replace("xxx", name.lower())
        return text.strip()

    def addTo(self, c, text, parent=None): 
        """Add our nodes etc"""
        if self.inherit:
            header = c.currentVnode().bodyString().split("\n")[0] + "\n"
        else:
            header = ""
        # 
        c.insertHeadline()
        main = c.currentVnode()
        main.setHeadString(self.processText(self.name, text))
        # 
        main.setBodyStringOrPane(self.processText(header+self.body, text))
        if parent: 
            c.currentVnode().moveToNthChildOf(parent, 0) 
        # 
        parent = c.currentVnode()
        for node in self.subnodes:
            node.addTo(c, text, parent)
            parent = None # Only want first node to be moved, others will go automatically 
#@nonl
#@-node:class Node
#@+node:class NodeAdder
class NodeAdder:

    """A Class to add a helper button to the toolbar which adds nodes to the outline""" 

    button_name = "Add"

    nodes = () # Should be set in the subclasses 

    def doIt(self, entry):
        """Create the nodes"""
        c = g.top()
        name = entry.get()
        for node in self.nodes:
            node.addTo(c, name)
#@nonl
#@-node:class NodeAdder
#@+node:class Helper
class Helper:

    """A Class to aid in the creating and maintenance of unit test files"""

    def __init__(self, adders):

        """Initialise with a set of adders"""
    
        self.adders = adders

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
        self.text.bind("<Return>", self.doCallback)
        # 
        self.pseudobutton = Tk.Frame(self._getSizer(self.frame, 24, 142), relief="raised", borderwidth=2) 
        self.pseudobutton.pack(side="right")
        # 
        self.doit = Tk.Button(self._getSizer(self.pseudobutton, 25, 32), text="New", relief="flat", command=self.doCallback)
        self.doit.pack(side="left")
        # 
        options = [adder.button_name for adder in self.adders]
        self.option_value = Tk.StringVar()
        self.options = FlatOptionMenu(self._getSizer(self.pseudobutton, 29, 110), self.option_value, *options)
        self.option_value.set(options[0])
        self.options.pack(side="right", fill="both", expand=1)
        
    def _getSizer(self, parent, height, width, pack="left"):
    
        """Return a sizer object to force a Tk widget to be the right size"""
    
        if USE_FIXED_SIZES:
            sizer = Tk.Frame(parent, height=height, width=width)
            sizer.pack_propagate(0) # don't shrink 
            sizer.pack(side=pack)
            return sizer
        else:
            return parent
            
    def doCallback(self, event=None):

        """Generate a callback to call the specific adder"""
        for adder in self.adders:
            if adder.button_name == self.option_value.get():
                adder.doIt(self.text)
                break
        else:
            raise ValueError("Button name not found: '%s'" % self.option_value.get())
#@nonl
#@-node:class Helper
#@+node:Modifiable classes to add buttons
# Modify these classes or data as you like to create templates that suit you.
#@nonl
#@-node:Modifiable classes to add buttons
#@+node:body text used by AddTestModule & AddTestClass
TEST_NODE_BODY = '''
import unittest

@others

if __name__ == "__main__":
    unittest.main()
'''

TEST_CLASS_BODY = '''
class TestXXX(unittest.TestCase):

    """Tests for the XXX class"""

    @others
'''

TEST_SETUP_BODY = '''
def setUp(self):

    """Create the test fixture"""

'''
#@nonl
#@-node:body text used by AddTestModule & AddTestClass
#@+node:class AddTestModule
class AddTestModule(NodeAdder):

    """Add unit testing node"""

    button_name = "test module"

    nodes = [
        Node(
            name="testxxx.py",
            body=TEST_NODE_BODY,
            subnodes=[ 
                Node(
                    name="TestXXX",
                    body=TEST_CLASS_BODY,
                    subnodes=[ 
                        Node(name="setUp",
                        body=TEST_SETUP_BODY)])])]
#@nonl
#@-node:class AddTestModule
#@+node:class AddTestClass
class AddTestClass(NodeAdder):

    """Add unit testing class"""

    button_name = "test class"

    nodes = [
        Node(
            name="TestXXX",
            body=TEST_CLASS_BODY,
            subnodes=[
                Node(
                    name="setUp",
                    body=TEST_SETUP_BODY)])]
#@nonl
#@-node:class AddTestClass
#@+node:class AddTestMethod
TEST_METHOD_BODY = '''
def testXXX(self):

    """testXXX: TestDescriptionGoesHere"""

'''

class AddTestMethod(NodeAdder):

    """Add unit testing method"""

    button_name = "test method"

    nodes = [
    Node(
        name="testXXX",
        body=TEST_METHOD_BODY,
        inherit=0)] # EKR: was 1.
#@nonl
#@-node:class AddTestMethod
#@+node:class AddClass
NEW_CLASS_BODY = '''
class XXX:

    """DocStringGoesHere"""

    @others
'''

NEW_INIT_BODY = '''
def __init__(self):

    """Initialise the XXX instance"""

'''

class AddClass(NodeAdder):
    
    """Add new class"""

    button_name = "class"

    nodes = [
        Node(
            name="class XXX",
            body=NEW_CLASS_BODY,
            subnodes=[
                #Node(
                #	name="<< class XXX declarations >>",
                #	body="@c\npass"),
                Node(
                    name="__init__",
                    body=NEW_INIT_BODY)] )]
#@-node:class AddClass
#@+node:class AddClassMethod
CLASS_METHOD_BODY = '''
def XXX(self):

    """MethodDocstringGoesHere"""

'''

class AddClassMethod(NodeAdder):

    """Add class method"""

    button_name = "method"

    nodes = [
        Node(
            name="XXX",
            body=CLASS_METHOD_BODY,
            inherit=0)] # EKR: was 1.
#@nonl
#@-node:class AddClassMethod
#@+node:Top-level code
if Tk: # OK for unit testing.

    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":
    
        g.es("Activating newButtons", color="orange")

        buttonList = [
            AddTestModule(),AddTestClass(),
            AddTestMethod(),AddClass(),AddClassMethod()]
    
        helper = Helper(buttonList)

        leoPlugins.registerHandler("after-create-leo-frame", helper.addWidgets)
        g.plugin_signon("newButtons")
#@nonl
#@-node:Top-level code
#@-leo
