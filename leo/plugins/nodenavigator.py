#@+leo-ver=4-thin
#@+node:ekr.20040108062655:@file-thin nodenavigator.py
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
        self.c = c = keywords['c'] 
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
        self.updateMarks("tag",{"c":c})
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
    #@+node:ekr.20040108062655.5:onSelect
    def onSelect(self, vnode):
        """Do the navigation"""
    
        self.c.selectVnode(vnode)
    #@nonl
    #@-node:ekr.20040108062655.5:onSelect
    #@+node:ekr.20040108091136:updateRecent
    def updateRecent(self,tag,keywords):
        """Update the marks list"""        
        c = keywords.get("c")
        v = c.rootVnode()
    
        # Clear old marks menu
        try:
            menu = self.recent["menu"]
            menu.delete(0,"end")
        except: return
    
        # Make sure the node still exists.
        # Insert only the last cloned node.
        vnodes = [] ; tnodes = []
        for v in c.visitedList:
            if v.exists(c) and v.t not in tnodes:
                
                def callback(event=None,self=self,v=v):
                    return self.onSelect(v)
    
                menu.add_command(label=v.headString(),command=callback)
                tnodes.append(v.t)
                vnodes.append(v)
    #@nonl
    #@-node:ekr.20040108091136:updateRecent
    #@+node:ekr.20040108062655.6:updateMarks
    def updateMarks(self, tag, keywords):
        """Update the marks list"""        
        c = keywords.get("c")
        v = c.rootVnode()
    
        # Clear old marks menu
        try:
            menu = self.marks["menu"]
            menu.delete(0,"end")
        except: return
    
        # Find all marked nodes
        vnodes = [] ; tnodes = []
        while v:
            if v.isMarked() and v.t not in tnodes:
                
                def callback(event=None,self=self,v=v):
                    return self.onSelect(v)
    
                name = v.headString().strip()
                menu.add_command(label=name,command=callback)
                tnodes.append(v.t)
                vnodes.append(v)
            v = v.threadNext()
    #@nonl
    #@-node:ekr.20040108062655.6:updateMarks
    #@-others
#@-node:ekr.20040108062655.2:class Navigator
#@-others

if Tk: 
    if g.app.gui is None: 
        g.app.createTkGui(__file__) 

    if g.app.gui.guiName() == "tkinter":
        nav = Navigator() 
        leoPlugins.registerHandler("after-create-leo-frame", nav.addWidgets) 
        leoPlugins.registerHandler(("set-mark","clear-mark"),nav.updateMarks)
        leoPlugins.registerHandler("select2",nav.updateRecent)
        g.plugin_signon("nodenavigator")
#@nonl
#@-node:ekr.20040108062655:@file-thin nodenavigator.py
#@-leo
