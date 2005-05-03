#@+leo-ver=4-thin
#@+node:ekr.20050331061925.2:@thin golf.py
#@<< docstring >>
#@+node:ekr.20050331061925.3:<< docstring >>
'''General Outline Language for Formatting

'''
#@nonl
#@-node:ekr.20050331061925.3:<< docstring >>
#@nl

#@@language python
#@@tabwidth -4

#@<< imports >>
#@+node:ekr.20050331061925.4:<< imports >>
import leoGlobals as g
import leoPlugins

if 0: # From rst2

    import os
    import ConfigParser
    from HTMLParser import HTMLParser
    from pprint import pprint
    
    try:
        import sys
        dir = os.path.split(__file__)[0]
        if dir not in sys.path:
            sys.path.append(dir)
        import mod_http
        from mod_http import set_http_attribute, get_http_attribute, reconstruct_html_from_attrs
    except:
        mod_http = None
#@nonl
#@-node:ekr.20050331061925.4:<< imports >>
#@nl

__version__ = '.1'
#@<< version history >>
#@+node:ekr.20050331061925.5:<< version history >>
#@@killcolor
#@+at
# 
# Version .1: Initial version by EKR.
#@-at
#@nonl
#@-node:ekr.20050331061925.5:<< version history >>
#@nl

controllers = {}

#@+others
#@+node:ekr.20050331061925.6:init
def init():

    ok = True

    if ok:
        g.plugin_signon(__name__)
        leoPlugins.registerHandler('after-create-leo-frame',onCreate)
    
    return ok
#@nonl
#@-node:ekr.20050331061925.6:init
#@+node:ekr.20050331062614:onCreate
def onCreate (tag, keys):
    
    c = keys.get('c')
    if c:
        global controllers
        controllers[c] = pluginController(c)
#@nonl
#@-node:ekr.20050331062614:onCreate
#@+node:ekr.20050331062614.1:class pluginController
class pluginController:
    
    #@    @+others
    #@+node:ekr.20050331062614.2: __init__
    def __init__ (self,c):
        
        self.c = c
        
        # These are set by @golf nodes.
        self.directives = {}
        self.options = {}
        self.scripts = {}
        
        # The lines of input.
        self.input = []
        
        # Add Golf command to Outline menu.
        menu = c.frame.menu
        outlineMenu = menu.getMenu('Outline')
        menu.add_command(outlineMenu,label='Golf',command=self.golfCommand)
        
        self.specialNodesDict = {
            '@golf-directive':  self.defineDirective,
            '@golf-options':    self.defineOptions,
            '@golf-script':     self.defineScript,
        }
    #@nonl
    #@-node:ekr.20050331062614.2: __init__
    #@+node:ekr.20050331063332:golfCommand
    def golfCommand (self):
        
        self.pass0() # Scan for user info.
        self.pass1() # Append input lines to self.input.
        self.pass2() # Write output
    #@nonl
    #@-node:ekr.20050331063332:golfCommand
    #@+node:ekr.20050331071121:isSpecialNode
    def isSpecialNode (self,p):
        
        '''Return the key if p's headline starts with a key in specialNodesDict.
        
        Otherwise return None.'''
        
        h = p.headString()
        
        for key in self.specialNodesDict.keys():
            if h.startswith(key):
                return key
        
        return None
    #@nonl
    #@-node:ekr.20050331071121:isSpecialNode
    #@+node:ekr.20050331064504:pass0 & helpers
    def pass0(self):
        
        '''Pre-scan the outline looking for special golf nodes.
        
        Unlike the other passes, this pass can not be over-ridden.'''
        
        for p in self.c.currentPosition().self_and_subtree_iter():
            key = self.isSpecialNode(p)
            if key:
                f = self.specialNodesDict.get(key)
                f(p)
    #@nonl
    #@+node:ekr.20050331064504.1:defineDirective
    def defineDirective (self,p):
        
        g.trace(p.headString())
    #@nonl
    #@-node:ekr.20050331064504.1:defineDirective
    #@+node:ekr.20050331064504.2:defineOptions
    def defineOptions (self,p):
        
        g.trace(p.headString())
    #@nonl
    #@-node:ekr.20050331064504.2:defineOptions
    #@+node:ekr.20050331064504.3:defineScript
    def defineScript (self,p):
        
        g.trace(p.headString())
    #@nonl
    #@-node:ekr.20050331064504.3:defineScript
    #@-node:ekr.20050331064504:pass0 & helpers
    #@+node:ekr.20050331064504.4:pass1
    def pass1(self):
         
        '''Scan the outline appending lines of output to self.input.
        
        This method handles all golf directives and syntax.'''
        
        self.input = []
        
        for p in self.c.currentPosition().self_and_subtree_iter():
            if not self.isSpecialNode(p):
                self.input.extend(g.splitLines(p.bodyString()))
    #@nonl
    #@-node:ekr.20050331064504.4:pass1
    #@+node:ekr.20050331064504.5:pass2
    def pass2 (self):
        
        '''Pass self.input to the chosen document processor.'''
        
        g.trace(g.printList(self.input))
    #@nonl
    #@-node:ekr.20050331064504.5:pass2
    #@-others
#@nonl
#@-node:ekr.20050331062614.1:class pluginController
#@-others
#@nonl
#@-node:ekr.20050331061925.2:@thin golf.py
#@-leo
