#@+leo-ver=4-thin
#@+node:ekr.20040108062655:@thin nodenavigator.py
"""Add a quick node navigators to the toolbar in Leo 

Adds a node navigator to the toolbar. The navigator allows quick
access to marked nodes. You can either go to the marked node or hoist
the marked node.

"""

#@@language python
#@@tabwidth -4

__name__ = "Node Navigator"
__version__ = "0.3" 

import leoGlobals as g
import leoPlugins

try: import Tkinter as Tk 
except ImportError: Tk = None

# Set this to 0 if the sizing of the toolbar controls doesn't look good on your platform. 
USE_FIXED_SIZES = 1 

#@+others
#@+node:ekr.20040108062655.2:class Navigator
class Navigator:
    
    """A node navigation aid for Leo"""

    #@    @+others
    #@+node:ekr.20040108062655.3:addWidgets
    def addWidgets(self, tag, keywords): 
        """Add the widgets to the navigation bar""" 
        self.c = c = keywords['new_c']
        self.recentTnodes = []
        self.markedTnodes = []
        toolbar = self.c.frame.iconFrame 
        # Main container 
        self.frame = Tk.Frame(toolbar) 
        self.frame.pack(side="left")
        # Marks
        marks = ["Marks"] 
        self.mark_value = Tk.StringVar() 
        self.marks = Tk.OptionMenu(self._getSizer(self.frame,29,70),self.mark_value,*marks)
        self.mark_value.set(marks[0]) 
        self.marks.pack(side="right",fill="both",expand=1)
        # Recent.
        recent = ["Recent"]
        self.recent_value = Tk.StringVar() 
        self.recent = Tk.OptionMenu(self._getSizer(self.frame,29,70),self.recent_value,*recent) 
        self.recent_value.set(recent[0]) 
        self.recent.pack(side="left",fill="both",expand=1)
        # Recreate the menus immediately.
        self.updateRecent("tag",{"c":c})
        self.initMarks("tag",{"c":c})
    #@nonl
    #@-node:ekr.20040108062655.3:addWidgets
    #@+node:ekr.20040108062655.4:_getSizer
    def _getSizer(self, parent, height, width):
        
        """Return a sizer object to force a Tk widget to be the right size""" 
        if USE_FIXED_SIZES: 
            sizer = Tk.Frame(parent,height=height,width=width) 
            sizer.pack_propagate(0) # don't shrink 
            sizer.pack(side="right") 
            return sizer 
        else: 
            return parent 
    #@nonl
    #@-node:ekr.20040108062655.4:_getSizer
    #@+node:ekr.20040108091136:updateRecent
    def updateRecent(self,tag,keywords):
        
        """Update the marks list"""        
        c = keywords.get("c")
    
        # Clear old marks menu
        try:
            menu = self.recent["menu"]
            menu.delete(0,"end")
        except: return
    
        self.recentTnodes = []
        for p in c.visitedList:
            if p.exists(c) and p.v.t not in self.recentTnodes:
                
                def callback(event=None,self=self,c=c,p=p):
                    return self.select(c,p)
    
                menu.add_command(label=p.headString(),command=callback)
                self.recentTnodes.append(p.v.t)
    #@nonl
    #@-node:ekr.20040108091136:updateRecent
    #@+node:ekr.20040730094103:select
    def select(self,c,p):
        
        # g.trace(p.exists(c),p)
    
        if p.exists(c):
            c.beginUpdate()
            c.frame.tree.expandAllAncestors(p)
            c.selectPosition(p)
            c.endUpdate()
    #@nonl
    #@-node:ekr.20040730094103:select
    #@+node:ekr.20040108062655.6:addMark
    def addMark(self, tag, keywords):
        
        """Add a mark to the marks list"""
        
        c = keywords.get("c")
        p = keywords.get("p")
        if not c or not p: return
        
        # g.trace()
    
        if p.v.t in self.markedTnodes: return
        
        try:
            menu = self.marks["menu"]
        except:
            menu = None
            
        if not menu: return
    
        def callback(event=None,self=self,c=c,p=p.copy()):
            self.select(c,p)
    
        name = p.headString().strip()
        menu.add_command(label=name,command=callback)
        self.markedTnodes.append(p.v.t)
    #@-node:ekr.20040108062655.6:addMark
    #@+node:ekr.20040730092357:initMarks
    def initMarks(self, tag, keywords):
        
        """Initialize the marks list."""
        
        c = keywords.get("c")
        if not c : return
    
        # Clear old marks menu
        try:
            menu = self.marks["menu"]
            menu.delete(0,"end")
        except: return
        
        # g.trace()
    
        # Find all marked nodes
        self.markedTnodes = []
        for p in c.all_positions_iter():
            if p.isMarked() and p.v.t not in self.markedTnodes:
                def callback(event=None,self=self,c=c,p=p.copy()):
                    self.select(c,p)
                name = p.headString().strip()
                menu.add_command(label=name,command=callback)
                self.markedTnodes.append(p.v.t)
    #@nonl
    #@-node:ekr.20040730092357:initMarks
    #@+node:ekr.20040730093250:clearMark
    def clearMark(self, tag, keywords):
        
        """Remove a mark to the marks list"""
        
        c = keywords.get("c")
        p = keywords.get("p")
        if not c or not p: return
        
        # g.trace(p)
    
        if not p.v.t in self.markedTnodes: return
        
        try:
            menu = self.marks["menu"]
        except: return
    
        name = p.headString().strip()
        menu.delete(name)
        self.markedTnodes.remove(p.v.t)
    #@nonl
    #@-node:ekr.20040730093250:clearMark
    #@-others
#@-node:ekr.20040108062655.2:class Navigator
#@-others

if Tk: 
    if g.app.gui is None: 
        g.app.createTkGui(__file__) 

    if g.app.gui.guiName() == "tkinter":
        nav = Navigator() 
        leoPlugins.registerHandler(("new","open2"), nav.addWidgets) 
        leoPlugins.registerHandler("set-mark",nav.addMark)
        leoPlugins.registerHandler("clear-mark",nav.clearMark)
        leoPlugins.registerHandler("select2",nav.updateRecent)
        g.plugin_signon("nodenavigator")
#@nonl
#@-node:ekr.20040108062655:@thin nodenavigator.py
#@-leo
