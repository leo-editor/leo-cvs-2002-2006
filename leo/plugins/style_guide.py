#@+leo-ver=4-thin
#@+node:ekr.20040919081244:@thin style_guide.py
"""
This is the plugin's docstring. Leo prints the __version__ variable (see
below) and this docstring when the user selects the plugin in the Plugins menu.
Therefore, this docstring should be a clear, concise description of what the
plugin does and how to use it.
"""

# This node and its decendents form a style guide for plugins.
# NOTE 1: Do NOT include either these initial comments or any of Python comments below.
# Note 2: There is no need to use sections if they are empty.

#@@language python
#@@tabwidth -4

#@<< about this plugin >>
#@+node:ekr.20040919082800:<< about this plugin >>
#@+at
# 
# This node should contain a comment, starting with '@' as shown above.
# 
# Make sure you tell what your plugin does and how to use it. You may include 
# as
# much detail as you like, but please try to be as clear and concise as 
# possible.
# 
# This is not the place for ramblings, snippets of code that didn't work, 
# ideas
# for improvements etc.
#@-at
#@nonl
#@-node:ekr.20040919082800:<< about this plugin >>
#@nl
__version__ = "1.0"
#@<< version history >>
#@+node:ekr.20040919082800.1:<< version history >>
#@+at
# 
# This node should contain a comment, starting with '@' as shown above.
# 
# This comment should discuss what makes each version unique. Some people like 
# to
# include a date. You may do so if you like, but I have never found that
# useful...
# 
# 1.0 EKR:  The initial style guide.
#@-at
#@nonl
#@-node:ekr.20040919082800.1:<< version history >>
#@nl
#@<< imports >>
#@+node:ekr.20040919082800.2:<< imports >>
# The comments in this node would not be part of the actual plugin.
# Most plugins will include the following imports:
import leoGlobals as g
import leoPlugins

# Next would follow imports of Leo's modules.
# Note: it is almost never necessary to import leoNodes.

# Next would follow imports of any standard Python modules.
# Good Python style is to put each import on a separate line.
# Examples:
import os
import sys

# Please do _not_ assume that modules like Tkinter, Pmw, etc. are always available.
# A good way to test for the precence of such modules is as follows:
try:
    import Tkinter as Tk
except ImportError:
    Tk = g.cantImport("Tkinter",__name__)
    
try:
    import Pmw
except ImportError:
    Tk = g.cantImport("Pmw",__name__)
    
# As shown above, I prefer to abbreviate Tkinter as Tk
# Please do NOT abbreviate Pmw or leoPlugins.

# Please do NOT use either of the following kinds of imports.
# from m import *
# from m import x,y,z
#@nonl
#@-node:ekr.20040919082800.2:<< imports >>
#@nl
#@<< globals >>
#@+node:ekr.20040919082800.3:<< globals >>
#@+at
# 
# If your plugin uses lots of module-level globals, you may define them in 
# this
# section. You may also define a few globals in the root node.
# 
# However, having lots of globals is an indication that it might be best to
# recast your code using a class. The ivars of this class would replace the
# globals.
# 
# N.B. If your plugin uses data in an outline, it is almost always a bad idea 
# to
# access the data using g.top(). Instead, your plugin should define an 
# onCreate
# function as shown in nother nodes. onCreate will create a class instance in
# which self.c is bound to a single commander.
#@-at
#@nonl
#@-node:ekr.20040919082800.3:<< globals >>
#@nl

# PLEASE define each function or method in a separate node!
#@+others
#@+node:ekr.20040919084039:onCreate
#@+at
# 
# This is the recommended way of:
# - Avoiding global variables.  The ivars of myClass take the place of 
# globals.
# - Making sure that your plugin always acts on the proper commander.
#   All methods of myClass use self.c to get the command, NOT g.top().
# 
#@-at
#@@c

def onCreate(tag, keywords):
    
    """
    This function is called whenever a new Leo window gets created.
    
    It creates a class instance in which self.c is bound permanently to c.
    """

    c = keywords.get("c")
    
    # Creates a class instance in which self.c is bound permanently to c.
    myClassInstance = myClass(c)
    
    # Now you can reliably bind other events _for c_ to class methods.
    leoPlugins.registerHandler("a-hook-name",myClassInstance.doWhatever)
#@nonl
#@-node:ekr.20040919084039:onCreate
#@+node:ekr.20040919084723:class myClass
class myClass:
    
    """
    A class illustrating how to bind a class instance permanently to a _particular_ window.
    All methods of this class should use self.c rather than c = g.top().
    """
    
    # PLEASE define each method in a separate node!
    #@    @+others
    #@+node:ekr.20040919084723.1:myClass.__init__
    #@+at
    # 
    # Binding c to self.c as shown ensures that this class always acts on the 
    # same commander, regardless of what Leo window is presently on top.  This 
    # is crucial to having your plugin work properly when multiple Leo windows 
    # are open.
    # 
    #@-at
    #@@c
    
    def __init__ (self,c):
        
        self.c = c
    #@nonl
    #@-node:ekr.20040919084723.1:myClass.__init__
    #@+node:ekr.20040919085218:myClass.doWhatever
    def doWhatever (self):
        
        """
        A method showing how to get the proper commander.
        """
        
        # self.c is always the commander this method should use.
        c = self.c
        
        # Now do whatever you want with c.
    #@nonl
    #@-node:ekr.20040919085218:myClass.doWhatever
    #@-others
#@nonl
#@-node:ekr.20040919084723:class myClass
#@+node:ekr.20040919085752:onStart2
def onStart2 (tag, keywords):
    
    """
    Showing how to define a global hook that affects all commanders.
    """

    import leoTkinterFrame
    log = leoTkinterFrame.leoTkinterLog
    
    # Replace frame.put with newPut. (not shown).
    g.funcToMethod(newPut,log,"put")
#@nonl
#@-node:ekr.20040919085752:onStart2
#@-others

# You need this if statement ONLY if your plugin depends on modules that might not be available.
# See the imports section for more discussion.
if Tk and Pmw:
    
    # You need the following three lines ONLY if your plugin uses a gui.
    # If you don't need them, just use the code following these three lines.
    if g.app.gui is None: 
        g.app.createTkGui(__file__)
    if g.app.gui.guiName() == "tkinter":
        # If your plugin needs to access data from a commander, it is almost always a bad
        # idea to use g.top() to get the commander of the presently selected frame.
        # Instead, use the onCreate function to create a class that binds self.c.
        leoPlugins.registerHandler("after-create-leo-frame", onCreate)
        
        # If your plugin acts globally (rather than on particular windows)
        # it is safe to define hook handlers here.  For example:
        leoPlugins.registerHandler("start2", onStart2)
        
        # Note: use g.plugin_signon, NOT leoPlugins.plugin_signon.
        # Please do not set __name__ explicitly.
        g.plugin_signon(__name__)
#@nonl
#@-node:ekr.20040919081244:@thin style_guide.py
#@-leo
