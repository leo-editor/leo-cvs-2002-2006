#@+leo-ver=4
#@+node:@file __outlineExperiments.py
"""Override outline drawing code to test optimized drawing"""

#@@language python
#@@tabwidth -4

import leoGlobals as g

print "overriding leoTkinterTree class"

#@<< about the tree classes >>
#@+node:<< about the tree classes >>
#@+at 
#@nonl
# This class implements a tree control similar to Windows explorer.  The draw 
# code is based on code found in Python's IDLE program.  Thank you Guido van 
# Rossum!
# 
# The tree class knows about vnodes.  The vnode class could be split into a 
# base class (say a treeItem class) containing the ivars known to the tree 
# class, and a derived class containing everything else, including, e.g., the 
# bodyString ivar.  I haven't chosen to split the vnode class this way because 
# nothing would be gained in Leo.
#@-at
#@-node:<< about the tree classes >>
#@nl

import leoTkinterTree
import leoFrame
import leoNodes
import Tkinter as Tk
import tkFont
import sys

#@<< about drawing >>
#@+node:<< About drawing >>
#@+at 
#@nonl
# Leo must redraw the outline pane when commands are executed and as the 
# result of mouse and keyboard events.  The main challenges are eliminating 
# flicker and handling events properly.
# 
# Eliminating flicker.  Leo must update the outline pane with minimum 
# flicker.  Various versions of Leo have approached this problem in different 
# ways.  The drawing code in leo.py is robust, flexible, relatively simple and 
# should work in almost any conceivable environment.
# 
# Leo assumes that all code that changes the outline pane will be enclosed in 
# matching calls to the c.beginUpdate and c.endUpdate  methods of the Commands 
# class. c.beginUpdate() inhibits drawing until the matching c.endUpdate().  
# These calls may be nested; only the outermost call to c.endUpdate() calls 
# c.redraw() to force a redraw of the outline pane.
# 
# In leo.py, code may call c.endUpdate(flag) instead of c.endUpdate().  Leo 
# redraws the screen only if flag is True.  This allows code to suppress 
# redrawing entirely when needed.  For example, study the idle_body_key event 
# handler to see how Leo conditionally redraws the outline pane.
# 
# The leoTree class redraws all icons automatically when c.redraw() is 
# called.  This is a major simplification compared to previous versions of 
# Leo.  The entire machinery of drawing icons in the vnode class has been 
# eliminated.  The v.computeIcon method tells what the icon should be.  The 
# v.iconVal ivar that tells what the present icon is. The event handler simply 
# compares these two values and sets redraw_flag if they don't match.
#@-at
#@nonl
#@-node:<< About drawing >>
#@nl
#@<< drawing constants >>
#@+node:<< drawing constants >>
# These should be ivars.  Sheesh.

box_padding = 5 # extra padding between box and icon
box_width = 9 + box_padding
icon_width = 20
icon_padding = 2
text_indent = 4 # extra padding between icon and tex
child_indent = 28 # was 20
hline_y = 7 # Vertical offset of horizontal line
root_left = 7 + box_width
root_top = 2
hiding = True # True if we don't reallocate items
line_height = 17 + 2 # To be replaced by Font height
#@nonl
#@-node:<< drawing constants >>
#@nl

if 0: # Doesn't seem to work.
    # override the position class
    class myPositionClass (leoNodes.position):
        #@        << override p.edit_text >>
        #@+node:<< override p.edit_text >>
        def edit_text (self):
            
            p = self
            
            if p:
                return self.c.frame.tree.findEditWidget(p,tag="p.edit_text(new)")
            else:
                return None
        #@nonl
        #@-node:<< override p.edit_text >>
        #@nl
        
    leoNodes.position = myPositionClass

# class leoTkinterTree (leoFrame.leoTree):
class myLeoTkinterTree(leoFrame.leoTree):

    callbacksInjected = False
    
    #@    @+others
    #@+node:Birth & death
    #@+node:__init__
    def __init__(self,c,frame,canvas):
        
        # Init the base class.
        leoFrame.leoTree.__init__(self,frame)
    
        # Objects associated with this tree.
        self.canvas = canvas
        
        #@    << old ivars >>
        #@+node:<< old ivars >>
        # Miscellaneous info.
        self.iconimages = {} # Image cache set by getIconImage().
        self.active = False # True if tree is active
        self._editPosition = None # Returned by leoTree.editPosition()
        self.lineyoffset = 0 # y offset for this headline.
        self.disableRedraw = False # True: reschedule a redraw for later.
        self.lastClickFrameId = None # id of last entered clickBox.
        self.lastColoredText = None # last colored text widget.
        
        # Set self.font and self.fontName.
        self.setFontFromConfig()
        
        # Recycling bindings.
        if 0: # no longer used
            self.bindings = [] # List of bindings to be unbound when redrawing.
            self.tagBindings = [] # List of tag bindings to be unbound when redrawing.
            self.widgets = [] # Widgets that must be destroyed when redrawing.
        
        # Drag and drop
        self.drag_p = None
        self.controlDrag = False # True: control was down when drag started.
        self.drag_id = None # To reset bindings after drag
        
        # Keep track of popup menu so we can handle behavior better on Linux Context menu
        self.popupMenu = None
        
        # Incremental redraws:
        self.allocateOnlyVisibleNodes = False # True: enable incremental redraws.
        self.trace = False # True enabling of various traces.
        self.prevMoveToFrac = None
        self.visibleArea = None
        self.expandedVisibleArea = None
        
        if self.allocateOnlyVisibleNodes:
            self.frame.bar1.bind("<B1-ButtonRelease>", self.redraw)
        #@nonl
        #@-node:<< old ivars >>
        #@nl
        #@    << inject callbacks into the position class >>
        #@+node:<< inject callbacks into the position class >>
        # The new code injects 3 callbacks for the colorizer.
        
        if not myLeoTkinterTree.callbacksInjected: # Class var.
            leoTkinterTree.callbacksInjected = True
            self.injectCallbacks()
        #@nonl
        #@-node:<< inject callbacks into the position class >>
        #@nl
        
        self.useBindtags = False
        
        self.createPermanentBindings()
        self.setEditPosition(None) # Set positions returned by leoTree.editPosition()
        
        self.editWidgets = []
            # List of Tk.Text widgets containing t.leo_position attributes.
        self.ids = {}
            # Keys are id's, values are unchanging positions.
        self.iconIds = {}
            # Keys are icon id's, values are unchanging positions.
        
        # Lists of visible (in-use) widgets...
        self.visibleBoxes = []
        self.visibleClickBoxes = []
        self.visibleIcons = []
        self.visibleLines = []
        self.visibleText  = []
        
        # Lists of newly freed, not-yet-hidden widgets...
        self.newlyFreedBoxes = []
        self.newlyFreedClickBoxes = []
        self.newlyFreedIcons = []
        self.newlyFreedLines = []
        self.newlyFreedText = []
    
        # Lists of free, hidden widgets...
        self.freeBoxes = []
        self.freeClickBoxes = []
        self.freeIcons = []
        self.freeLines = []
        self.freeText = []
    #@nonl
    #@-node:__init__
    #@+node:createPermanentBindings
    def createPermanentBindings (self):
        
        canvas = self.canvas
        
        canvas.tag_bind('clickBox','<Button-1>',   self.onClickBoxClick)
    
        canvas.tag_bind('iconBox','<Button-1>', self.onIconBoxClick)
        canvas.tag_bind('iconBox','<Double-1>', self.onIconBoxDoubleClick)
        canvas.tag_bind('iconBox','<Button-3>', self.onIconBoxRightClick)
        
        canvas.tag_bind('iconBox','<B1-Motion>',            self.onDrag)
        canvas.tag_bind('iconBox','<Any-ButtonRelease-1>',  self.onEndDrag)
    
        if self.useBindtags: # Create a dummy widget to hold all bindings.
            t = Tk.Text() # This _must_ be a Text widget.
            if 1: # This doesn't seem to matter.
                t.bind("<Button-1>", self.onHeadlineClick)
                t.bind("<Button-3>", self.onHeadlineRightClick)
                t.bind("<Key>",      self.onHeadlineKey)
            else:
                t.bind("<Button-1>", self.onHeadlineClick, '+')
                t.bind("<Button-3>", self.onHeadlineRightClick, '+')
                t.bind("<Key>",      self.onHeadlineKey, '+')
            t.bind("<Control-t>",self.onControlT)
        
            # newText() attaches these bindings to all headlines.
            self.textBindings = t.bindtags()
            print t.bindtags()
    #@nonl
    #@-node:createPermanentBindings
    #@+node:textRepr
    def textAddr(self,t):
        
        """Return the address part of repr(Tk.Text)."""
        
        return repr(t)[-9:-1].lower()
    #@nonl
    #@-node:textRepr
    #@+node:injectCallbacks
    def injectCallbacks(self):
        
        import leoNodes
        
        #@    << define tkinter callbacks to be injected in the position class >>
        #@+node:<< define tkinter callbacks to be injected in the position class >>
        # N.B. These vnode methods are entitled to know about details of the leoTkinterTree class.
        
        #@+others
        #@+node:onHyperLinkControlClick
        def OnHyperLinkControlClick (self,event):
            
            """Callback injected into position class."""
        
            g.trace(self)
            try:
                p = self ; c = p.c
                if not g.doHook("hypercclick1",c=c,p=p,event=event):
                    c.beginUpdate()
                    c.selectVnode(p)
                    c.endUpdate()
                    c.frame.bodyCtrl.mark_set("insert","1.0")
                g.doHook("hypercclick2",c=c,p=p,event=event)
            except:
                g.es_event_exception("hypercclick")
                
        onHyperLinkControlClick = OnHyperLinkControlClick
        #@nonl
        #@-node:onHyperLinkControlClick
        #@+node:onHyperLinkEnter
        def OnHyperLinkEnter (self,event=None):
            
            """Callback injected into position class."""
        
            g.trace(self)
            try:
                p = self ; c = p.c
                if not g.doHook("hyperenter1",c=c,p=p,event=event):
                    if 0: # This works, and isn't very useful.
                        c.frame.bodyCtrl.tag_config(p.tagName,background="green")
                g.doHook("hyperenter2",c=c,p=p,event=event)
            except:
                g.es_event_exception("hyperenter")
                
        onHyperLinkEnter = OnHyperLinkEnter
        #@nonl
        #@-node:onHyperLinkEnter
        #@+node:onHyperLinkLeave
        def OnHyperLinkLeave (self,event=None):
            
            """Callback injected into position class."""
        
            g.trace(self)
            try:
                p = self ; c = p.c
                if not g.doHook("hyperleave1",c=c,p=p,event=event):
                    if 0: # This works, and isn't very useful.
                        c.frame.bodyCtrl.tag_config(p.tagName,background="white")
                g.doHook("hyperleave2",c=c,p=p,event=event)
            except:
                g.es_event_exception("hyperleave")
                
        onHyperLinkLeave = OnHyperLinkLeave
        #@nonl
        #@-node:onHyperLinkLeave
        #@-others
        
        #@-node:<< define tkinter callbacks to be injected in the position class >>
        #@nl
    
        for f in (OnHyperLinkControlClick,OnHyperLinkEnter,OnHyperLinkLeave):
            
            g.funcToMethod(f,leoNodes.position)
    #@nonl
    #@-node:injectCallbacks
    #@-node:Birth & death
    #@+node:Config & Measuring
    #@+node:tree.getFont,setFont,setFontFromConfig
    def getFont (self):
    
        return self.font
            
    # Called by leoFontPanel.
    def setFont (self, font=None, fontName=None):
        
        if fontName:
            self.fontName = fontName
            self.font = tkFont.Font(font=fontName)
        else:
            self.fontName = None
            self.font = font
            
        self.setLineHeight(self.font)
        
    # Called by ctor and when config params are reloaded.
    def setFontFromConfig (self):
    
        font = g.app.config.getFontFromParams(
            "headline_text_font_family", "headline_text_font_size",
            "headline_text_font_slant",  "headline_text_font_weight",
            g.app.config.defaultTreeFontSize)
    
        self.setFont(font)
    #@nonl
    #@-node:tree.getFont,setFont,setFontFromConfig
    #@+node:headWidth & widthInPixels
    def headWidth(self,v):
    
        """Returns the proper width of the entry widget for the headline."""
    
        return max(10,5 + len(v.headString()))
        
    def widthInPixels(self,s):
    
        s = g.toEncodedString(s,g.app.tkEncoding)
        
        width = self.font.measure(s)
        
        # g.trace(width,s)
        
        return width
    #@nonl
    #@-node:headWidth & widthInPixels
    #@+node:setLineHeight
    def setLineHeight (self,font):
        
        try:
            metrics = font.metrics()
            linespace = metrics ["linespace"]
            self.line_height = linespace + 5 # Same as before for the default font on Windows.
            # print metrics
        except:
            self.line_height = line_height # was 17 + 2
            g.es("exception setting outline line height")
            g.es_exception()
    #@nonl
    #@-node:setLineHeight
    #@+node:setTreeColorsFromConfig
    def setTreeColorsFromConfig (self):
    
        bg = g.app.config.getWindowPref("outline_pane_background_color")
        if bg:
            try: self.canvas.configure(bg=bg)
            except: pass
    #@-node:setTreeColorsFromConfig
    #@-node:Config & Measuring
    #@+node:Drawing
    #@+node:drawBox
    def drawBox (self,p,x,y):
        
        tree = self ; canvas = self.canvas
        y += 7 # draw the box at x, y+7
        
        if not g.doHook("draw-outline-box",tree=tree,p=p,v=p,x=x,y=y):
    
            iconname = g.choose(p.isExpanded(),"minusnode.gif", "plusnode.gif")
            image = self.getIconImage(iconname)
            id = self.newBox()
            canvas.itemconfigure(id,image=image)
            canvas.coords(id,x,y+self.lineyoffset)
    
            assert(not self.ids.get(id))
            self.ids[id] = p.copy()
            
            return id
    #@-node:drawBox
    #@+node:drawClickBox
    def drawClickBox (self,p,y):
        
        canvas = self.canvas
        h = self.line_height
        defaultColor = ""
        
        # Define a slighly larger rect to catch clicks.
        id = self.newClickBox()
    
        canvas.coords(id,0,y,1000,y+h-3)
        canvas.itemconfig(id,fill=defaultColor,outline=defaultColor)
    
        self.ids[id] = p.copy()
        
        if 0: # A major change to the user interface.
            #@        << change the appearance of headlines >>
            #@+node:<< change the appearance of headlines >>
            
            # Define a slighly smaller rect to colorize.
            color_rect = self.canvas.create_rectangle(0,y,1000,y+h-4,tag="colorBox")
            self.canvas.itemconfig(color_rect,fill=defaultColor,outline=defaultColor)
            
            # Color the click box or the headline
            def enterRect(event,id=color_rect,p=p,t=self.lastText):
                if 1: # Color or underline the headline
                    t2 = self.lastColoredText
                    if t2: # decolor the old headline.
                        if 1: # deunderline
                            t2.tag_delete('underline')
                        else: # decolor
                            t2.configure(background="white")
                    if t and p != self.editPosition():
                        if 1: # underline
                            t.tag_add('underline','1.0','end')
                            t.tag_configure('underline',underline=True)
                        else: # color
                            t.configure(background="LightSteelBlue1")
                        self.lastColoredText = t
                    else: self.lastColoredText = None
                else: # Color the click box.
                    if self.lastClickFrameId:
                        self.canvas.itemconfig(self.lastClickFrameId,fill=defaultColor,outline=defaultColor)
                    self.lastClickFrameId = id
                    color = "LightSteelBlue1"
                    self.canvas.itemconfig(id,fill=color,outline=color)
            
            bind_id = self.canvas.tag_bind(click_rect, "<Enter>", enterRect) # , '+')
            self.tagBindings.append((click_rect,bind_id,"<Enter>"),)
            #@nonl
            #@-node:<< change the appearance of headlines >>
            #@nl
    #@nonl
    #@-node:drawClickBox
    #@+node:drawIcon
    def drawIcon(self,p,x=None,y=None):
        
        """Draws icon for position p at x,y, or at p.v.iconx,p.v.icony if x,y = None,None"""
    
        tree = self ; canvas = self.canvas
        v = p.v # Make sure the bindings refer to the _present_ position.
    
        #@    << compute x,y and iconVal >>
        #@+node:<< compute x,y and iconVal >>
        
        if x is None and y is None:
            try:
                x,y = v.iconx, v.icony
            except:
                # Inject the ivars.
                x,y = v.iconx, v.icony = 0,0
        else:
            # Inject the ivars.
            v.iconx, v.icony = x,y
        
        y += 2 # draw icon at y + 2
        
        # Always recompute v.iconVal.
        # This is an important drawing optimization.
        val = v.iconVal = v.computeIcon()
        assert(0 <= val <= 15)
        #@nonl
        #@-node:<< compute x,y and iconVal >>
        #@nl
    
        if not g.doHook("draw-outline-icon",tree=tree,p=p,v=v,x=x,y=y):
    
            # Get the image.
            imagename = "box%02d.GIF" % val
            image = self.getIconImage(imagename)
            id = self.newIcon()
            canvas.itemconfigure(id,image=image)
            canvas.coords(id,x,y+self.lineyoffset)
            
            p = p.copy()
            self.iconIds[id] = p # Remember which vnode belongs to the icon.
            self.ids[id] = p
    
        return 0,icon_width # dummy icon height,width
    #@nonl
    #@-node:drawIcon
    #@+node:drawLine
    def drawLine (self,x1,y1,x2,y2):
        
        id = self.newLine()
        
        self.canvas.coords(id,x1,y1,x2,y2)
        
        return id
    #@-node:drawLine
    #@+node:drawNode & force_draw_node (good trace)
    def drawNode(self,p,x,y):
        
        tree = self ; canvas = self.canvas ; 
        
        p = p.copy() ; v = p.v
        
        data = g.doHook("draw-outline-node",tree=tree,p=p,v=v,x=x,y=y)
        if data is not None: return data
    
        if 1:
            self.lineyoffset = 0
        else:
            if hasattr(p.v.t,"unknownAttributes"):
                self.lineyoffset = p.v.t.unknownAttributes.get("lineYOffset",0)
            else:
                self.lineyoffset = 0
        
        # Draw the horizontal line.
        self.drawLine(
            x,y+7+self.lineyoffset,
            x+box_width,y+7+self.lineyoffset)
        
        if self.inVisibleArea(y):
            return self.force_draw_node(p,x,y)
        else:
            return self.line_height,0
    #@nonl
    #@+node:force_draw_node (new)
    def force_draw_node(self,p,x,y):
    
        h,w = self.drawUserIcons(p,"beforeBox",x,y)
        xw = w # The extra indentation before the icon box.
        if p.hasChildren():
            box_id = self.drawBox(p,x+w,y)
        else:
            box_id = None
    
        w += box_width # even if box isn't drawn.
    
        h2,w2 = self.drawUserIcons(p,"beforeIcon",x+w,y)
        h = max(h,h2) ; w += w2 ; xw += w2
    
        h2,w2 = self.drawIcon(p,x+w,y)
        h = max(h,h2) ; w += w2
    
        h2,w2 = self.drawUserIcons(p,"beforeHeadline",x+w,y)
        h = max(h,h2) ; w += w2
    
        expand_x = x+w # save this for later.
        h2 = self.drawText(p,x+w,y,box_id)
        h = max(h,h2)
        w += self.widthInPixels(p.headString())
    
        h2,w2 = self.drawUserIcons(p,"afterHeadline",x+w,y)
        h = max(h,h2)
        
        self.drawClickBox(p,y)
    
        return h,xw
    #@nonl
    #@-node:force_draw_node (new)
    #@+node:force_draw_node (old)
    def force_draw_nodeOLD(self,p,x,y):
    
        if p.hasChildren():
            box_id = self.drawBox(p,x,y)
        w = box_width # Even if the box isn't drawn.
    
        h2,w2 = self.drawIcon(p,x+w,y)
        w += w2
    
        h = self.drawText(p,x+w,y)
        
        return h,0
    #@-node:force_draw_node (old)
    #@-node:drawNode & force_draw_node (good trace)
    #@+node:drawText
    def drawText(self,p,x,y,box_id=None):
        
        """draw text for position p at nominal coordinates x,y."""
        
        assert(p)
    
        c = self.c ; canvas = self.canvas
        h = self.line_height
        x += text_indent
        
        data = g.doHook("draw-outline-text-box",tree=self,p=p,v=p.v,x=x,y=y)
        if data is not None: return data
        
        id,t = self.newText()
        
        # g.trace("%3d" % id,self.textAddr(t),p.headString())
    
        # This does not seem to be working reliably!
        t.delete("1.0","end")
        t.insert("end",p.headString())
        s = t.get("1.0","end")
        
        if s.strip() != p.headString().strip():
            g.trace("***** get new widget ***")
            # g.trace("%3d" % id,self.textAddr(t),s.strip(),p.headString().strip())
            
            # Hide the item, and move it from the visible list to the free list.  Jeeze.
            canvas.coords(id,-100,-100)
            data = id,t
            self.visibleText.remove(data)
            self.freeText.append(data)
        
            # Try again with a brand new widget.
            id,t = self.newText(forceAllocate=True)
            
            t.delete("1.0","end")
            t.insert("end",p.headString())
            s = t.get("1.0","end")
            if s.strip() != p.headString().strip():
                g.trace("***** second assignment failed ****")
    
        self.ids[id] = p.copy()
        t.configure(width=self.headWidth(p))
        canvas.coords(id,x,y+self.lineyoffset)
    
        if 0:
            #@        << highlight text widget on enter events >>
            #@+node:<< highlight text widget on enter events >>
            if 0: # Define a rect to colorize.
            
                color_rect = self.canvas.create_rectangle(0,y,1000,y+h-4,tag="colorBox")
                self.canvas.itemconfig(color_rect,fill="",outline="")
            
                def enterRect(event,id=color_rect):
                    if self.lastClickFrameId:
                        self.canvas.itemconfig(self.lastClickFrameId,fill="",outline="")
                    self.lastClickFrameId = id
                    color = "LightSteelBlue1"
                    self.canvas.itemconfig(id,fill=color,outline=color)
                
                bind_enter = t.bind( '<Enter>', enterRect, '+' )
                self.bindings.append((t,bind_enter,"<Enter>"),)
                
            if 0: # Colorize only the headline.
            
                def enterRect(event,p=p,t=t):
                    t2 = self.lastColoredText
                    if t2:
                        if 1: # deunderline
                            t2.tag_delete('underline')
                        else: # color
                            t2.configure(background="white")
                    if p == self.editPosition():
                        self.lastColoredText = None
                    else:
                        self.lastColoredText = t
                        if 1: # underline
                            t.tag_add('underline','1.0', 'end')
                            t.tag_configure('underline',underline = True)
                        else: #color
                            t.configure(background="LightSteelBlue1")
                
                bind_enter = t.bind( '<Enter>', enterRect, '+' )
                self.bindings.append((t,bind_enter,"<Enter>"),)
            #@nonl
            #@-node:<< highlight text widget on enter events >>
            #@nl
    
        t.leo_position = p.copy()
        self.editWidgets.append(t)
       
        if 0: # Something very bizarre is going on.
            self.configureTextState(p)
        
        return self.line_height
    #@nonl
    #@-node:drawText
    #@+node:drawTopTree
    def drawTopTree (self):
        
        """Draws the top-level tree, taking into account the hoist state."""
        
        c = self.c ; canvas = self.canvas
        
        if 0:
            try: self.redrawCount += 1
            except: self.radrawCount = 1
            g.trace(self.redrawCount)
        
        self.lastClickFrameId = None # id of last entered clickBox.
        self.lastColoredText = None # last colored text widget.
    
        self.checkWidgetList("drawTopTree: before")
        
        # Recycle widgets and clear all state arrays.
        self.recycleWidgets()
        self.editWidgets = []
        self.ids = {}
        self.iconIds = {}
        
        g.trace("begin %s" % self.getTextStats())
        
        if c.hoistStack:
            p,junk = c.hoistStack[-1]
            self.drawTree(p.copy(),root_left,root_top,0,0,hoistFlag=True)
        else:
            self.drawTree(c.rootPosition(),root_left,root_top,0,0)
    
        self.hideNewlyFreedWidgets()
        
        canvas.lower("textBox") # This is not the Tk.Text widget, so it should be low.
        canvas.lower("plusBox") 
        canvas.lower("lines")   # Lowest.
        canvas.lift("clickBox")
        canvas.lift("iconBox") # Higest.
        
        canvas.update_idletasks() # So recent changes will take.
        
        self.checkWidgetList("drawTopTree: after")
        g.trace("end   %s" % self.getTextStats())
        # self.traceIds()
    #@nonl
    #@-node:drawTopTree
    #@+node:drawTree
    def drawTree(self,p,x,y,h,level,hoistFlag=False):
    
        tree = self ; v = p.v
        yfirst = ylast = y
        if level==0: yfirst += 10
        w = 0
        
        data = g.doHook("draw-sub-outline",tree=tree,p=p,v=v,x=x,y=y,h=h,level=level,hoistFlag=hoistFlag)
        if data is not None: return data
        
        while p: # Do not use iterator.
            h,w = self.drawNode(p,x,y)
            y += h ; ylast = y
            if p.isExpanded() and p.hasFirstChild():
                # Must make an additional copy here by calling firstChild.
                y,w2 = self.drawTree(p.firstChild(),x+child_indent+w,y,h,level+1)
                x += w2 ; w += w2
            if hoistFlag: break
            else:         p = p.next()
            
        # Draw the virtical line.
        self.drawLine(x, yfirst-hline_y,x, ylast+hline_y-h)
        return y,w
    #@nonl
    #@-node:drawTree
    #@+node:Unchanged
    #@+node:drawUserIcon
    def drawUserIcon (self,where,x,y,dict):
        
        h,w = 0,0
    
        if where != dict.get("where","beforeHeadline"):
            return h,w
            
        # g.trace(where,x,y,dict)
        
        #@    << set offsets and pads >>
        #@+node:<< set offsets and pads >>
        xoffset = dict.get("xoffset")
        try:    xoffset = int(xoffset)
        except: xoffset = 0
        
        yoffset = dict.get("yoffset")
        try:    yoffset = int(yoffset)
        except: yoffset = 0
        
        xpad = dict.get("xpad")
        try:    xpad = int(xpad)
        except: xpad = 0
        
        ypad = dict.get("ypad")
        try:    ypad = int(ypad)
        except: ypad = 0
        #@nonl
        #@-node:<< set offsets and pads >>
        #@nl
        type = dict.get("type")
        if type == "icon":
            s = dict.get("icon")
            #@        << draw the icon in string s >>
            #@+node:<< draw the icon in string s >>
            pass
            #@nonl
            #@-node:<< draw the icon in string s >>
            #@nl
        elif type == "file":
            file = dict.get("file")
            #@        << draw the icon at file >>
            #@+node:<< draw the icon at file >>
            try:
                image = self.iconimages[file]
                # Get the image from the cache if possible.
            except KeyError:
                try:
                    fullname = g.os_path_join(g.app.loadDir,"..","Icons",file)
                    fullname = g.os_path_normpath(fullname)
                    image = Tk.PhotoImage(master=self.canvas,file=fullname)
                    self.iconimages[fullname] = image
                except:
                    #g.es("Exception loading: " + fullname)
                    #g.es_exception()
                    image = None
                    
            if image:
                id = self.canvas.create_image(x+xoffset,y+yoffset,anchor="nw",image=image)
                self.canvas.lift(id)
                h = image.height() + yoffset + ypad
                w = image.width()  + xoffset + xpad
            #@nonl
            #@-node:<< draw the icon at file >>
            #@nl
        elif type == "url":
            url = dict.get("url")
            #@        << draw the icon at url >>
            #@+node:<< draw the icon at url >>
            pass
            #@nonl
            #@-node:<< draw the icon at url >>
            #@nl
            
        # Allow user to specify height, width explicitly.
        h = dict.get("height",h)
        w = dict.get("width",w)
    
        return h,w
    #@nonl
    #@-node:drawUserIcon
    #@+node:drawUserIcons
    def drawUserIcons(self,p,where,x,y):
        
        """Draw any icons specified by p.v.t.unknownAttributes["icons"]."""
        
        h,w = 0,0 ; t = p.v.t
        
        if not hasattr(t,"unknownAttributes"):
            return h,w
        
        iconsList = t.unknownAttributes.get("icons")
        if not iconsList:
            return h,w
        
        try:
            for dict in iconsList:
                h2,w2 = self.drawUserIcon(where,x+w,y,dict)
                h = max(h,h2) ; w += w2
        except:
            g.es_exception()
    
        return h,w
    #@nonl
    #@-node:drawUserIcons
    #@+node:inVisibleArea & inExpandedVisibleArea
    def inVisibleArea (self,y1):
        
        if self.allocateOnlyVisibleNodes:
            if self.visibleArea:
                vis1,vis2 = self.visibleArea
                y2 = y1 + self.line_height
                return y2 >= vis1 and y1 <= vis2
            else: return False
        else:
            return True # This forces all nodes to be allocated on all redraws.
            
    def inExpandedVisibleArea (self,y1):
        
        if self.expandedVisibleArea:
            vis1,vis2 = self.expandedVisibleArea
            y2 = y1 + self.line_height
            return y2 >= vis1 and y1 <= vis2
        else:
            return False
    #@nonl
    #@-node:inVisibleArea & inExpandedVisibleArea
    #@+node:getIconImage
    def getIconImage (self, name):
    
        # Return the image from the cache if possible.
        if self.iconimages.has_key(name):
            return self.iconimages[name]
            
        try:
            fullname = g.os_path_join(g.app.loadDir,"..","Icons",name)
            fullname = g.os_path_normpath(fullname)
            image = Tk.PhotoImage(master=self.canvas,file=fullname)
            self.iconimages[name] = image
            return image
        except:
            g.es("Exception loading: " + fullname)
            g.es_exception()
            return None
    #@nonl
    #@-node:getIconImage
    #@+node:idle_scrollTo
    def idle_scrollTo(self,p=None):
    
        """Scrolls the canvas so that v is in view.
        
        This is done at idle time after a redraw so that treeBar.get() will return proper values."""
    
        c = self.c ; frame = c.frame
        if not p: p = self.c.currentPosition()
        if not p: p = self.c.rootPosition() # 4/8/04.
        try:
            last = p.lastVisible()
            nextToLast = last.visBack()
            h1 = self.yoffset(p)
            h2 = self.yoffset(last)
            #@        << compute approximate line height >>
            #@+node:<< compute approximate line height >>
            if nextToLast: # 2/2/03: compute approximate line height.
                lineHeight = h2 - self.yoffset(nextToLast)
            else:
                lineHeight = 20 # A reasonable default.
            #@nonl
            #@-node:<< compute approximate line height >>
            #@nl
            #@        << Compute the fractions to scroll down/up >>
            #@+node:<< Compute the fractions to scroll down/up >>
            data = frame.treeBar.get()
            try: lo, hi = data
            except: lo,hi = 0.0,1.0
            if h2 > 0.1:
                frac = float(h1)/float(h2) # For scrolling down.
                frac2 = float(h1+lineHeight/2)/float(h2) # For scrolling up.
                frac2 = frac2 - (hi - lo)
            else:
                frac = frac2 = 0.0 # probably any value would work here.
                
            frac =  max(min(frac,1.0),0.0)
            frac2 = max(min(frac2,1.0),0.0)
            #@nonl
            #@-node:<< Compute the fractions to scroll down/up >>
            #@nl
            if frac <= lo:
                if self.prevMoveToFrac != frac:
                    self.prevMoveToFrac = frac
                    self.canvas.yview("moveto",frac)
            elif frac2 + (hi - lo) >= hi:
                if self.prevMoveToFrac != frac2:
                    self.prevMoveToFrac = frac2
                    self.canvas.yview("moveto",frac2)
    
            if self.allocateOnlyVisibleNodes:
                self.canvas.after_idle(self.idle_second_redraw)
                
            c.setTopVnode(p) # 1/30/04: remember a pseudo "top" node.
            # print "%3d %3d %1.3f %1.3f %1.3f %1.3f" % (h1,h2,frac,frac2,lo,hi)
        except:
            g.es_exception()
    #@nonl
    #@-node:idle_scrollTo
    #@+node:numberOfVisibleNodes
    def numberOfVisibleNodes(self):
        
        n = 0 ; p = self.c.rootPosition()
        while p:
            n += 1
            p.moveToVisNext()
        return n
    #@nonl
    #@-node:numberOfVisibleNodes
    #@+node:scrollTo
    def scrollTo (self,p):
        
        def scrollToCallback(event=None,self=self,p=p):
            g.trace(event,self,p)
            self.idle_scrollTo(p)
        
        self.canvas.after_idle(scrollToCallback)
    #@nonl
    #@-node:scrollTo
    #@+node:yoffset
    #@+at 
    #@nonl
    # We can't just return icony because the tree hasn't been redrawn yet.  
    # For the same reason we can't rely on any TK canvas methods here.
    #@-at
    #@@c
    
    def yoffset(self, v1):
    
        # if not v1.isVisible(): print "yoffset not visible:",v1
        root = self.c.rootPosition()
        h, flag = self.yoffsetTree(root,v1)
        # flag can be False during initialization.
        # if not flag: print "yoffset fails:",h,v1
        return h
    
    # Returns the visible height of the tree and all sibling trees, stopping at p1
    
    def yoffsetTree(self,p,p1):
    
        h = 0
        for p in p.siblings_iter():
            # print "yoffsetTree:", p
            if p == p1:
                return h, True
            h += self.line_height
            if p.isExpanded() and p.hasChildren():
                child = p.firstChild()
                h2, flag = self.yoffsetTree(child,p1)
                h += h2
                if flag: return h, True
        
        return h, False
    #@nonl
    #@-node:yoffset
    #@-node:Unchanged
    #@-node:Drawing
    #@+node:Event handlers
    #@+node:checkWidgetList
    def checkWidgetList (self,tag):
        
        for t in self.editWidgets:
            
            p = t.leo_position
            if p:
                s = t.get("1.0","end").strip()
                h = p.headString().strip()
                
                if h != s:
                    self.dumpWidgetList(tag)
                    return False
            else:
                self.dumpWidgetList(tag)
                return False
                
        return True
    #@nonl
    #@-node:checkWidgetList
    #@+node:dumpWidgetList
    def dumpWidgetList (self,tag):
        
        print
        print "checkWidgetList: %s" % tag
        
        for t in self.editWidgets:
            
            p = t.leo_position
            if p:
                s = t.get("1.0","end").strip()
                h = p.headString().strip()
        
                addr = self.textAddr(t)
                print "p:",addr,h
                if h != s:
                    print "t:",'*' * len(addr),s
            else:
                print "t.leo_position == None",t
    #@nonl
    #@-node:dumpWidgetList
    #@+node:eventToPosition
    def eventToPosition (self,event):
    
        canvas = self.canvas
        x,y = event.x,event.y
        
        # import traceback ; traceback.print_stack()
        
        # This won't work when we are doing a redraw!
        item = canvas.find_overlapping(x,y,x,y)
    
        # Item may be a tuple.
        try:    id = item[0]
        except: id = item
    
        p = self.ids.get(id)
        
        # g.trace(id,p)
    
        return p
    #@nonl
    #@-node:eventToPosition
    #@+node:edit_text
    def edit_text (self,p):
        
        # g.trace(p)
        
        if self.editPosition:
            return self.findEditWidget(p,tag="tree:edit_text")
        else:
            return None
    #@nonl
    #@-node:edit_text
    #@+node:findEditWidget
    # Search the widget list for widget t with t.leo_position == p.
    
    def findEditWidget (self,p,tag=""):
        
        """Return the Tk.Text item corresponding to p."""
    
        if not p: return None
        
        ok = self.checkWidgetList("findEditWidget")
        if not ok: return None
    
        for t in self.editWidgets:
            assert(t.leo_position)
                
            if t.leo_position == p:
                s = t.get("1.0","end")
                # checkWidgetList should have caught this.
                assert(p.headString().strip() == s.strip()) 
                return t
    
        return None
    #@nonl
    #@-node:findEditWidget
    #@+node:Click Box...
    #@+node:onClickBoxClick
    def onClickBoxClick (self,event):
        
        c = self.c ; gui = g.app.gui
        
        p = self.eventToPosition(event)
        
        # g.trace(p)
    
        if p:
            if p.isExpanded(): p.contract()
            else:              p.expand()
        
            self.active = True
            self.select(p)
            g.app.findFrame.handleUserClick(p)
            gui.set_focus(c,c.frame.bodyCtrl)
            self.redraw()
    #@nonl
    #@-node:onClickBoxClick
    #@+node:OnBoxClick ORIGINAL
    # Called on click in box and double-click in headline.
    
    def ORIGINAL_OnBoxClick (self,p):
        
        # g.trace(p)
    
        # Note: "boxclick" hooks handled by vnode callback routine.
        c = self.c ; gui = g.app.gui
    
        if p.isExpanded(): p.contract()
        else:              p.expand()
    
        self.active = True
        self.select(p)
        g.app.findFrame.handleUserClick(p) # 4/3/04
        gui.set_focus(c,c.frame.bodyCtrl) # 7/12/03
        self.redraw()
    #@nonl
    #@-node:OnBoxClick ORIGINAL
    #@-node:Click Box...
    #@+node:Icon Box...
    #@+node:onIconBoxClick
    def onIconBoxClick (self,event):
        
        c = self.c ; gui = g.app.gui
        tree = self ; canvas = tree.canvas
        
        p = self.eventToPosition(event)
        if not p: return
    
        # g.trace(p)
    
        p = p.copy() # Make sure callbacks use the _present_ position.
    
        if event:
            canvas_x = canvas.canvasx(event.x)
            canvas_y = canvas.canvasy(event.y)
            id = canvas.find_closest(canvas_x,canvas_y)
            # id = canvas.find_overlapping(canvas_x,canvas_y,canvas_x,canvas_y)
            if id != None:
                try: id = id[0]
                except: pass
                self.drag_p = p
                self.drag_id = id
                
                if 0:
                    # Create the bindings.
                    id4 = canvas.tag_bind(id,"<B1-Motion>", self.onDrag)
                    id5 = canvas.tag_bind(id,"<Any-ButtonRelease-1>", self.onEndDrag)
                    
                    # Remember the bindings so deleteBindings can delete them.
                    self.tagBindings.append((id,id4,"<B1-Motion>"),)
                    self.tagBindings.append((id,id5,"<Any-ButtonRelease-1>"),)
        tree.select(p)
        g.app.findFrame.handleUserClick(p) # 4/3/04
        return "break" # disable expanded box handling.
    #@nonl
    #@-node:onIconBoxClick
    #@+node:onIconBoxDoubleClick
    def onIconBoxDoubleClick (self,event):
        
        c = self.c
    
        p = self.eventToPosition(event)
        if not p: return
    
        g.trace(p)
        
        try:
            if not g.doHook("icondclick1",c=c,p=p,event=event):
                self.OnIconDoubleClick(p) # Call the method in the base class.
            g.doHook("icondclick2",c=c,p=p,event=event)
        except:
            g.es_event_exception("icondclick")
    #@-node:onIconBoxDoubleClick
    #@+node:onIconBoxRightClick
    def onIconBoxRightClick (self,event):
    
        p = self.eventToPosition(event)
        g.trace(p)
        
        if p:
            self.select(p)
            g.app.findFrame.handleUserClick(p)
    
        return "break" # disable expanded box handling.
    #@nonl
    #@-node:onIconBoxRightClick
    #@-node:Icon Box...
    #@+node:Text Box...
    #@+node:configureTextState
    def configureTextState (self,p):
        
        c = self.c
        
        if not p: return # should never happen...
        
        if p == c.currentPosition():
            if p == self.editPosition():
                self.setNormalLabelState(p)
            else:
                self.setDisabledLabelState(p) # selected, disabled
        else:
            self.setUnselectedLabelState(p) # unselected
    #@nonl
    #@-node:configureTextState
    #@+node:onCtontrolT
    # This works around an apparent Tk bug.
    
    def onControlT (self,event=None):
    
        # If we don't inhibit further processing the Tx.Text widget switches characters!
        return "break"
    #@nonl
    #@-node:onCtontrolT
    #@+node:onHeadlineClick
    def onHeadlineClick (self,event):
        
        c = self.c ; w = event.widget
        
        try:
            p = w.leo_position
        except AttributeError:
            return "continue"
        
        try:
            if not g.doHook("headclick1",c=c,p=p,event=event):
                self.OnActivate(p)
            g.doHook("headclick2",c=c,p=p,event=event)
        except:
            g.es_event_exception("headclick")
            
        return "continue"
    #@nonl
    #@-node:onHeadlineClick
    #@+node:onHeadlineKey
    def onHeadlineKey (self,event):
        
        """Handle a key event in a headline."""
        
        w = event.widget ; ch = event.char
    
        try:
            p = w.leo_position
        except AttributeError:
            return "continue"
    
        self.c.frame.bodyCtrl.after_idle(self.idle_head_key,p,ch)
        
        return "continue"
    #@nonl
    #@-node:onHeadlineKey
    #@+node:onHeadlineRightClick
    def onHeadlineRightClick (self,event):
    
        c = self.c ; w = event.widget
        
        try:
            p = w.leo_position
        except AttributeError:
            return "continue"
    
        try:
            if not g.doHook("headrclick1",c=c,p=p,event=event):
                self.OnActivate(p)
                self.OnPopup(p,event)
            g.doHook("headrclick2",c=c,p=p,event=event)
        except:
            g.es_event_exception("headrclick")
            
        return "continue"
    #@nonl
    #@-node:onHeadlineRightClick
    #@+node:virtual event handlers: called from core
    #@+node:idle_head_key
    def idle_head_key (self,p,ch=None):
        
        """Update headline text at idle time."""
        
        g.trace()
        
        c = self.c ; v = p.v
    
        if not p or p != c.currentPosition():
            return "break"
            
        edit_text = self.edit_text(p)
        index = edit_text.index("insert")
    
        if g.doHook("headkey1",c=c,p=p,ch=ch):
            return "break" # The hook claims to have handled the event.
            
        #@    << set head to vnode text >>
        #@+node:<< set head to vnode text >>
        head = p.headString()
        if head == None:
            head = u""
        head = g.toUnicode(head,"utf-8")
        #@nonl
        #@-node:<< set head to vnode text >>
        #@nl
        done = ch in ('\r','\n')
        if done:
            #@        << set the widget text to head >>
            #@+node:<< set the widget text to head >>
            edit_text.delete("1.0","end")
            edit_text.insert("end",head)
            edit_text.mark_set("insert",index)
            #@nonl
            #@-node:<< set the widget text to head >>
            #@nl
        #@    << set s to the widget text >>
        #@+node:<< set s to the widget text >>
        s = edit_text.get("1.0","end")
        
        # Don't truncate if the user is hitting return.
        # That should just end editing.
        if 1:
            # Truncate headline text to workaround Tk problems...
            # Another kludge: remove one or two trailing newlines before warning of truncation.
            if s and s[-1] == '\n': s = s[:-1]
            if s and s[-1] == '\n': s = s[:-1]
            i = s.find('\n')
            if i > -1:
                # g.trace(i,len(s),repr(s))
                g.es("Truncating headline to one line",color="blue")
                s = s[:i]
            if len(s) > 250:
                g.es("Truncating headline to 250 characters",color="blue")
                s = s[:250]
        
        s = g.toUnicode(s,g.app.tkEncoding)
        
        if not s:
            s = u""
            
        if 0: # 6/10/04: No longer needed.  This was stressing Tk needlessly.
            s = s.replace('\n','')
            s = s.replace('\r','')
        #@nonl
        #@-node:<< set s to the widget text >>
        #@nl
        changed = s != head
        if changed:
            c.undoer.setUndoParams("Change Headline",p,newText=s,oldText=head)
            #@        << update v and all nodes joined to v >>
            #@+node:<< update v and all nodes joined to v >>
            c.beginUpdate()
            if 1: # update...
                # Update changed bit.
                if not c.changed:
                    c.setChanged(True)
                # Update all dirty bits.
                if not p.isDirty():
                    p.setDirty()
                # Update v.
                v.initHeadString(s)
                edit_text.delete("1.0","end")
                edit_text.insert("end",s)
                edit_text.mark_set("insert",index)
            c.endUpdate(False) # do not redraw now.
            #@nonl
            #@-node:<< update v and all nodes joined to v >>
            #@nl
        if done or changed:
            #@        << reconfigure v and all nodes joined to v >>
            #@+node:<< reconfigure v and all nodes joined to v >>
            # Reconfigure v's headline.
            if done:
                self.setDisabledLabelState(p)
            
            edit_text.configure(width=self.headWidth(v))
            #@nonl
            #@-node:<< reconfigure v and all nodes joined to v >>
            #@nl
            #@        << update the screen >>
            #@+node:<< update the screen >>
            if done:
                c.beginUpdate()
                self.endEditLabel()
                c.endUpdate()
            
            elif changed:
                # Update v immediately.  Joined nodes are redrawn later by endEditLabel.
                # Redrawing the whole screen now messes up the cursor in the headline.
                self.drawIcon(p) # just redraw the icon.
            #@nonl
            #@-node:<< update the screen >>
            #@nl
    
        g.doHook("headkey2",c=c,p=p,ch=ch)
        return "break"
    #@nonl
    #@-node:idle_head_key
    #@+node:onHeadChanged
    # The <Key> event generates the event before the headline text is changed!
    # We register an idle-event handler to do the work later.
    
    def onHeadChanged (self,p):
    
        """Handle a change to headline text."""
        
        g.trace()
        
        self.c.frame.bodyCtrl.after_idle(self.idle_head_key,p)
    #@nonl
    #@-node:onHeadChanged
    #@-node:virtual event handlers: called from core
    #@-node:Text Box...
    #@+node:Dragging
    #@+node:tree.onContinueDrag
    def onContinueDrag(self,event):
        
        canvas = self.canvas ; frame = self.c.frame
    
        p = self.drag_p
        if not p: return
    
        try:
            if event:
                x,y = event.x,event.y
            else:
                x,y = frame.top.winfo_pointerx(),frame.top.winfo_pointery()
                # Stop the scrolling if we go outside the entire window.
                if x == -1 or y == -1: return 
            
            # OnEndDrag() halts the scrolling by clearing self.drag_id when the mouse button goes up.
            if self.drag_id: # This gets cleared by onEndDrag()
                #@            << scroll the canvas as needed >>
                #@+node:<< scroll the canvas as needed >>
                # Scroll the screen up or down one line if the cursor (y) is outside the canvas.
                h = canvas.winfo_height()
                if y < 0 or y > h:
                    lo, hi = frame.treeBar.get()
                    n = self.savedNumberOfVisibleNodes
                    line_frac = 1.0 / float(n)
                    frac = g.choose(y < 0, lo - line_frac, lo + line_frac)
                    frac = min(frac,1.0)
                    frac = max(frac,0.0)
                    # g.es("lo,hi,frac:",lo,hi,frac)
                    canvas.yview("moveto", frac)
                    
                    # Queue up another event to keep scrolling while the cursor is outside the canvas.
                    lo, hi = frame.treeBar.get()
                    if (y < 0 and lo > 0.1) or (y > h and hi < 0.9):
                        canvas.after_idle(self.OnContinueDrag,p,None) # Don't propagate the event.
                #@nonl
                #@-node:<< scroll the canvas as needed >>
                #@nl
        except:
            g.es_event_exception("continue drag")
    #@nonl
    #@-node:tree.onContinueDrag
    #@+node:tree.onDrag
    # This precomputes numberOfVisibleNodes(), a significant optimization.
    # We also indicate where findVnodeWithIconId() should start looking for tree id's.
    
    def onDrag(self,event):
    
        # Note: "drag" hooks handled by vnode callback routine.
        
        c = self.c ; p = self.drag_p
        if not event or not p: return
        v = p.v
    
        if not self.dragging():
            windowPref = g.app.config.getBoolWindowPref
            # Only do this once: greatly speeds drags.
            self.savedNumberOfVisibleNodes = self.numberOfVisibleNodes()
            self.setDragging(True)
            if windowPref("allow_clone_drags"):
                self.controlDrag = c.frame.controlKeyIsDown
                if windowPref("look_for_control_drag_on_mouse_down"):
                    if windowPref("enable_drag_messages"):
                        if self.controlDrag:
                            g.es("dragged node will be cloned")
                        else:
                            g.es("dragged node will be moved")
            else: self.controlDrag = False
            self.canvas['cursor'] = "hand2" # "center_ptr"
    
        self.onContinueDrag(event)
    #@nonl
    #@-node:tree.onDrag
    #@+node:tree.onEndDrag
    def onEndDrag(self,event):
        
        """Tree end-of-drag handler called from vnode event handler."""
        
        c = self.c ; canvas = self.canvas ; config = g.app.config
        p = self.drag_p
        if not p: return
        v = p.v
    
        if event:
            #@        << set vdrag, childFlag >>
            #@+node:<< set vdrag, childFlag >>
            x,y = event.x,event.y
            canvas_x = canvas.canvasx(x)
            canvas_y = canvas.canvasy(y)
            
            id = self.canvas.find_closest(canvas_x,canvas_y)
            # id = self.canvas.find_overlapping(canvas_x,canvas_y,canvas_x,canvas_y)
            
            vdrag = self.findVnodeWithIconId(id)
            childFlag = vdrag and vdrag.hasChildren() and vdrag.isExpanded()
            #@nonl
            #@-node:<< set vdrag, childFlag >>
            #@nl
            if config.getBoolWindowPref("allow_clone_drags"):
                if not config.getBoolWindowPref("look_for_control_drag_on_mouse_down"):
                    self.controlDrag = c.frame.controlKeyIsDown
    
            if vdrag and vdrag.v.t != p.v.t: # 6/22/04: Disallow drag to joined node.
                if self.controlDrag: # Clone p and move the clone.
                    if childFlag:
                        c.dragCloneToNthChildOf(p,vdrag,0)
                    else:
                        c.dragCloneAfter(p,vdrag)
                else: # Just drag p.
                    if childFlag:
                        c.dragToNthChildOf(p,vdrag,0)
                    else:
                        c.dragAfter(p,vdrag)
            else:
                if p and self.dragging():
                    pass # g.es("not dragged: " + p.headString())
                if 0: # Don't undo the scrolling we just did!
                    self.idle_scrollTo(p)
        
        # 1216/02: Reset the old cursor by brute force.
        self.canvas['cursor'] = "arrow"
    
        if self.drag_id:
            canvas.tag_unbind(self.drag_id,"<B1-Motion>")
            canvas.tag_unbind(self.drag_id,"<Any-ButtonRelease-1>")
            self.drag_id = None
            
        self.setDragging(False)
        self.drag_p = None
    #@nonl
    #@-node:tree.onEndDrag
    #@-node:Dragging
    #@+node:Unchanged Event handers
    #@+at 
    #@nonl
    # Important note: most hooks are created in the vnode callback routines, 
    # _not_ here.
    #@-at
    #@+node:OnActivate
    def OnActivate (self,p,event=None):
    
        try:
            c = self.c ; gui = g.app.gui
            #@        << activate this window >>
            #@+node:<< activate this window >>
            current = c.currentPosition()
            
            if p == current:
                g.trace("is current")
                if self.active:
                    self.editLabel(p)
                else:
                    self.undimEditLabel()
                    gui.set_focus(c,self.canvas) # Essential for proper editing.
            else:
                g.trace("not current")
                self.select(p)
                g.app.findFrame.handleUserClick(p) # 4/3/04
                if p.v.t.insertSpot != None: # 9/1/02
                    c.frame.bodyCtrl.mark_set("insert",p.v.t.insertSpot)
                    c.frame.bodyCtrl.see(p.v.t.insertSpot)
                else:
                    c.frame.bodyCtrl.mark_set("insert","1.0")
                gui.set_focus(c,c.frame.bodyCtrl)
            
            self.active = True
            #@nonl
            #@-node:<< activate this window >>
            #@nl
        except:
            g.es_event_exception("activate tree")
    #@nonl
    #@-node:OnActivate
    #@+node:tree.OnDeactivate (caused double-click problem)
    def OnDeactivate (self,event=None):
        
        """Deactivate the tree pane, dimming any headline being edited."""
    
        tree = self ; c = self.c
        focus = g.app.gui.get_focus(c.frame)
    
        # Bug fix: 7/13/03: Only do this as needed.
        # Doing this on every click would interfere with the double-clicking.
        if not c.frame.log.hasFocus() and focus != c.frame.bodyCtrl:
            try:
                # g.trace(focus)
                tree.endEditLabel()
                tree.dimEditLabel()
            except:
                g.es_event_exception("deactivate tree")
    #@nonl
    #@-node:tree.OnDeactivate (caused double-click problem)
    #@+node:tree.findVnodeWithIconId
    def findVnodeWithIconId (self,id):
        
        # Due to an old bug, id may be a tuple.
        try:
            return self.iconIds.get(id[0])
        except:
            return self.iconIds.get(id)
    #@nonl
    #@-node:tree.findVnodeWithIconId
    #@+node:tree.OnPopup & allies
    def OnPopup (self,p,event):
        
        """Handle right-clicks in the outline."""
        
        # Note: "headrclick" hooks handled by vnode callback routine.
    
        if event != None:
            c = self.c
            if not g.doHook("create-popup-menu",c=c,p=p,event=event):
                self.createPopupMenu(event)
            if not g.doHook("enable-popup-menu-items",c=c,p=p,event=event):
                self.enablePopupMenuItems(p,event)
            if not g.doHook("show-popup-menu",c=c,p=p,event=event):
                self.showPopupMenu(event)
    
        return "break"
    #@nonl
    #@+node:OnPopupFocusLost
    #@+at 
    #@nonl
    # On Linux we must do something special to make the popup menu "unpost" if 
    # the mouse is clicked elsewhere.  So we have to catch the <FocusOut> 
    # event and explicitly unpost.  In order to process the <FocusOut> event, 
    # we need to be able to find the reference to the popup window again, so 
    # this needs to be an attribute of the tree object; hence, 
    # "self.popupMenu".
    # 
    # Aside: though Tk tries to be muli-platform, the interaction with 
    # different window managers does cause small differences that will need to 
    # be compensated by system specific application code. :-(
    #@-at
    #@@c
    
    # 20-SEP-2002 DTHEIN: This event handler is only needed for Linux.
    
    def OnPopupFocusLost(self,event=None):
    
        self.popupMenu.unpost()
        
    #@-node:OnPopupFocusLost
    #@+node:createPopupMenu
    def createPopupMenu (self,event):
        
        c = self.c ; frame = c.frame
        
        # If we are going to recreate it, we had better destroy it.
        if self.popupMenu:
            self.popupMenu.destroy()
            self.popupMenu = None
        
        self.popupMenu = menu = Tk.Menu(g.app.root, tearoff=0)
        
        # Add the Open With entries if they exist.
        if g.app.openWithTable:
            frame.menu.createMenuEntries(menu,g.app.openWithTable,openWith=1)
            table = (("-",None,None),)
            frame.menu.createMenuEntries(menu,table)
            
        #@    << Create the menu table >>
        #@+node:<< Create the menu table >>
        table = (
            ("&Read @file Nodes",None,c.readAtFileNodes),
            ("&Write @file Nodes",None,c.fileCommands.writeAtFileNodes),
            ("-",None,None),
            ("&Tangle","Shift+Ctrl+T",c.tangle),
            ("&Untangle","Shift+Ctrl+U",c.untangle),
            ("-",None,None),
            # 2/16/04: Remove shortcut for Toggle Angle Brackets command.
            ("Toggle Angle &Brackets",None,c.toggleAngleBrackets),
            ("-",None,None),
            ("Cut Node","Shift+Ctrl+X",c.cutOutline),
            ("Copy Node","Shift+Ctrl+C",c.copyOutline),
            ("&Paste Node","Shift+Ctrl+V",c.pasteOutline),
            ("&Delete Node","Shift+Ctrl+BkSp",c.deleteOutline),
            ("-",None,None),
            ("&Insert Node","Ctrl+I",c.insertHeadline),
            ("&Clone Node","Ctrl+`",c.clone),
            ("Sort C&hildren",None,c.sortChildren),
            ("&Sort Siblings","Alt-A",c.sortSiblings),
            ("-",None,None),
            ("Contract Parent","Alt+0",c.contractParent))
        #@nonl
        #@-node:<< Create the menu table >>
        #@nl
        
        # 11/27/03: Don't actually set binding: it would conflict with previous.
        frame.menu.createMenuEntries(menu,table,dontBind=True)
    #@nonl
    #@-node:createPopupMenu
    #@+node:enablePopupMenuItems
    def enablePopupMenuItems (self,v,event):
        
        """Enable and disable items in the popup menu."""
        
        c = self.c ; menu = self.popupMenu
    
        #@    << set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>
        #@+node:<< set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>
        isAtFile = False
        isAtRoot = False
        
        for v2 in v.self_and_subtree_iter():
            if isAtFile and isAtRoot:
                break
            if (v2.isAtFileNode() or
                v2.isAtNorefFileNode() or
                v2.isAtAsisFileNode() or
                v2.isAtNoSentFileNode()
            ):
                isAtFile = True
                
            isRoot,junk = g.is_special(v2.bodyString(),0,"@root")
            if isRoot:
                isAtRoot = True
        #@nonl
        #@-node:<< set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>
        #@nl
        isAtFile = g.choose(isAtFile,1,0)
        isAtRoot = g.choose(isAtRoot,1,0)
        canContract = v.parent() != None
        canContract = g.choose(canContract,1,0)
        
        enable = self.frame.menu.enableMenu
        
        for name in ("Read @file Nodes", "Write @file Nodes"):
            enable(menu,name,isAtFile)
        for name in ("Tangle", "Untangle"):
            enable(menu,name,isAtRoot)
    
        enable(menu,"Cut Node",c.canCutOutline())
        enable(menu,"Delete Node",c.canDeleteHeadline())
        enable(menu,"Paste Node",c.canPasteOutline())
        enable(menu,"Sort Children",c.canSortChildren())
        enable(menu,"Sort Siblings",c.canSortSiblings())
        enable(menu,"Contract Parent",c.canContractParent())
    #@nonl
    #@-node:enablePopupMenuItems
    #@+node:showPopupMenu
    def showPopupMenu (self,event):
        
        """Show a popup menu."""
        
        c = self.c ; menu = self.popupMenu ; gui = g.app.gui
    
        if sys.platform == "linux2": # 20-SEP-2002 DTHEIN: not needed for Windows
            menu.bind("<FocusOut>",self.OnPopupFocusLost)
        
        menu.post(event.x_root, event.y_root)
    
        # Make certain we have focus so we know when we lose it.
        # I think this is OK for all OSes.
        gui.set_focus(c,menu)
    #@nonl
    #@-node:showPopupMenu
    #@-node:tree.OnPopup & allies
    #@+node:tree.OnIconClick & OnIconRightClick
    def OnIconClick (self,p,event):
        
        # g.trace(p)
        
        p = p.copy() # Make sure callbacks use the _present_ position.
    
        tree = self ; canvas = tree.canvas
        if event:
            canvas_x = canvas.canvasx(event.x)
            canvas_y = canvas.canvasy(event.y)
            id = canvas.find_closest(canvas_x,canvas_y)
            # id = canvas.find_overlapping(canvas_x,canvas_y,canvas_x,canvas_y)
            if id != None:
                try: id = id[0]
                except: pass
                self.drag_p = p
                self.drag_id = id
                
                # Create the bindings.
                id4 = canvas.tag_bind(id,"<B1-Motion>", p.OnDrag)
                id5 = canvas.tag_bind(id,"<Any-ButtonRelease-1>", p.OnEndDrag)
                
                # Remember the bindings so deleteBindings can delete them.
                self.tagBindings.append((id,id4,"<B1-Motion>"),)
                self.tagBindings.append((id,id5,"<Any-ButtonRelease-1>"),)
        tree.select(p)
        g.app.findFrame.handleUserClick(p) # 4/3/04
        return "break" # disable expanded box handling.
        
    def OnIconRightClick (self,p,event):
    
        self.select(p)
        g.app.findFrame.handleUserClick(p) # 4/3/04
        return "break" # disable expanded box handling.
    #@nonl
    #@-node:tree.OnIconClick & OnIconRightClick
    #@-node:Unchanged Event handers
    #@-node:Event handlers
    #@+node:Incremental drawing
    #@+node:allocateNodes
    def allocateNodes(self,where,lines):
        
        """Allocate Tk widgets in nodes that will become visible as the result of an upcoming scroll"""
        
        assert(where in ("above","below"))
    
        # print "allocateNodes: %d lines %s visible area" % (lines,where)
        
        # Expand the visible area: a little extra delta is safer.
        delta = lines * (self.line_height + 4)
        y1,y2 = self.visibleArea
    
        if where == "below":
            y2 += delta
        else:
            y1 = max(0.0,y1-delta)
    
        self.expandedVisibleArea=y1,y2
        # print "expandedArea:   %5.1f %5.1f" % (y1,y2)
        
        # Allocate all nodes in expanded visible area.
        self.updatedNodeCount = 0
        self.updateTree(self.c.rootPosition(),root_left,root_top,0,0)
        # if self.updatedNodeCount: print "updatedNodeCount:", self.updatedNodeCount
    #@-node:allocateNodes
    #@+node:allocateNodesBeforeScrolling
    def allocateNodesBeforeScrolling (self, args):
        
        """Calculate the nodes that will become visible as the result of an upcoming scroll.
    
        args is the tuple passed to the Tk.Canvas.yview method"""
    
        if not self.allocateOnlyVisibleNodes: return
    
        # print "allocateNodesBeforeScrolling:",self.redrawCount,args
    
        assert(self.visibleArea)
        assert(len(args)==2 or len(args)==3)
        kind = args[0] ; n = args[1]
        lines = 2 # Update by 2 lines to account for rounding.
        if len(args) == 2:
            assert(kind=="moveto")
            frac1,frac2 = args
            if float(n) != frac1:
                where = g.choose(n<frac1,"above","below")
                self.allocateNodes(where=where,lines=lines)
        else:
            assert(kind=="scroll")
            linesPerPage = self.canvas.winfo_height()/self.line_height + 2
            n = int(n) ; assert(abs(n)==1)
            where = g.choose(n == 1,"below","above")
            lines = g.choose(args[2] == "pages",linesPerPage,lines)
            self.allocateNodes(where=where,lines=lines)
    #@nonl
    #@-node:allocateNodesBeforeScrolling
    #@+node:updateNode
    def updateNode (self,v,x,y):
        
        """Draw a node that may have become visible as a result of a scrolling operation"""
    
        if self.inExpandedVisibleArea(y):
            # This check is a major optimization.
            if not v.edit_text():
                return self.force_draw_node(v,x,y)
            else:
                return self.line_height
    
        return self.line_height
    #@nonl
    #@-node:updateNode
    #@+node:setVisibleAreaToFullCanvas
    def setVisibleAreaToFullCanvas(self):
        
        if self.visibleArea:
            y1,y2 = self.visibleArea
            y2 = max(y2,y1 + self.canvas.winfo_height())
            self.visibleArea = y1,y2
    #@nonl
    #@-node:setVisibleAreaToFullCanvas
    #@+node:setVisibleArea
    def setVisibleArea (self,args):
    
        r1,r2 = args
        r1,r2 = float(r1),float(r2)
        # print "scroll ratios:",r1,r2
    
        try:
            s = self.canvas.cget("scrollregion")
            x1,y1,x2,y2 = g.scanf(s,"%d %d %d %d")
            x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
        except:
            self.visibleArea = None
            return
            
        scroll_h = y2-y1
        # print "height of scrollregion:", scroll_h
    
        vy1 = y1 + (scroll_h*r1)
        vy2 = y1 + (scroll_h*r2)
        self.visibleArea = vy1,vy2
        # print "setVisibleArea: %5.1f %5.1f" % (vy1,vy2)
    #@-node:setVisibleArea
    #@+node:tree.updateTree
    def updateTree (self,v,x,y,h,level):
    
        yfirst = ylast = y
        if level==0: yfirst += 10
        while v:
            # g.trace(x,y,v)
            h = self.updateNode(v,x,y)
            y += h ; ylast = y
            if v.isExpanded() and v.firstChild():
                y = self.updateTree(v.firstChild(),x+child_indent,y,h,level+1)
            v = v.next()
        return y
    #@-node:tree.updateTree
    #@-node:Incremental drawing
    #@+node:Selecting & editing (tree)
    #@+node:endEditLabel ORIGINAL
    def endEditLabel (self):
        
        """End editing for self.editText."""
    
        c = self.c ; gui = g.app.gui
        
        p = self.editPosition()
    
        if p and p.edit_text():
            self.setUnselectedLabelState(p)
            self.setEditPosition(None)
    
            # force a redraw of joined and ancestor headlines.
            self.force_redraw() 
    
        gui.set_focus(c,c.frame.bodyCtrl) # 10/14/02
    #@nonl
    #@-node:endEditLabel ORIGINAL
    #@+node:editLabel ORIGINAL
    def editLabel (self,p):
        
        """Start editing p.edit_text."""
        
        # g.trace(p)
    
        if self.editPosition() and p != self.editPosition():
            self.endEditLabel()
            self.frame.revertHeadline = None
            
        self.setEditPosition(p)
    
        # Start editing
        if p and p.edit_text():
            self.setNormalLabelState(p)
            self.frame.revertHeadline = p.headString()
            self.setEditPosition(p)
    #@nonl
    #@-node:editLabel ORIGINAL
    #@+node:tree.select (ORIGINAL)
    # Warning: do not try to "optimize" this by returning if v==tree.currentVnode.
    
    def select (self,p,updateBeadList=True):
    
        if not p: return
        
        #@    << define vars and stop editing >>
        #@+node:<< define vars and stop editing >>
        c = self.c
        frame = c.frame ; body = frame.bodyCtrl
        
        old_p = c.currentPosition()
        
        # Unselect any previous selected but unedited label.
        self.endEditLabel()
        self.setUnselectedLabelState(old_p)
        #@nonl
        #@-node:<< define vars and stop editing >>
        #@nl
        
        # g.trace(p)
        # g.printGc()
    
        if not g.doHook("unselect1",c=c,new_v=p,old_v=old_p):
            #@        << unselect the old node >>
            #@+node:<< unselect the old node >> (changed in 4.2)
            # Remember the position of the scrollbar before making any changes.
            yview=body.yview()
            insertSpot = c.frame.body.getInsertionPoint()
            
            if old_p and old_p != p:
                # g.trace("different node")
                self.endEditLabel()
                self.setUnselectedLabelState(old_p)
            
            if old_p and old_p.edit_text():
                old_p.v.t.scrollBarSpot = yview
                old_p.v.t.insertSpot = insertSpot
            #@nonl
            #@-node:<< unselect the old node >> (changed in 4.2)
            #@nl
    
        g.doHook("unselect2",c=c,new_v=p,old_v=old_p)
        
        if not g.doHook("select1",c=c,new_v=p,old_v=old_p):
            #@        << select the new node >>
            #@+node:<< select the new node >>
            frame.setWrap(p)
            
            # 6/14/04: Always do this.  Otherwise there can be problems with trailing hewlines.
            s = g.toUnicode(p.v.t.bodyString,"utf-8")
            body.delete("1.0","end")
            body.insert("1.0",s)
            
            # We must do a full recoloring: we may be changing context!
            self.frame.body.recolor_now(p)
            
            if p.v and p.v.t.scrollBarSpot != None:
                first,last = p.v.t.scrollBarSpot
                body.yview("moveto",first)
            
            if p.v.t.insertSpot != None: # 9/21/02: moved from c.selectVnode
                c.frame.bodyCtrl.mark_set("insert",p.v.t.insertSpot)
                c.frame.bodyCtrl.see(p.v.t.insertSpot)
            else:
                c.frame.bodyCtrl.mark_set("insert","1.0")
            #@nonl
            #@-node:<< select the new node >>
            #@nl
            if p and p != old_p: # 3/26/03: Suppress duplicate call.
                try: # may fail during initialization
                    self.idle_scrollTo(p)
                except: pass
            #@        << update c.beadList or c.beadPointer >>
            #@+node:<< update c.beadList or c.beadPointer >>
            if updateBeadList:
                
                if c.beadPointer > -1:
                    present_p = c.beadList[c.beadPointer]
                else:
                    present_p = c.nullPosition()
                
                if p != present_p:
                    # Replace the tail of c.beadList by c and make c the present node.
                    # print "updating c.beadList"
                    c.beadPointer += 1
                    c.beadList[c.beadPointer:] = []
                    c.beadList.append(p)
                    
                # g.trace(c.beadPointer,p,present_p)
            #@nonl
            #@-node:<< update c.beadList or c.beadPointer >>
            #@nl
            #@        << update c.visitedList >>
            #@+node:<< update c.visitedList >>
            # Make p the most recently visited position on the list.
            if p in c.visitedList:
                c.visitedList.remove(p)
            
            c.visitedList.insert(0,p)
            #@nonl
            #@-node:<< update c.visitedList >>
            #@nl
    
        #@    << set the current node >>
        #@+node:<< set the current node >>
        self.c.setCurrentPosition(p)
        self.setSelectedLabelState(p)
        self.frame.scanForTabWidth(p) #GS I believe this should also get into the select1 hook
        g.app.gui.set_focus(c,c.frame.bodyCtrl)
        #@nonl
        #@-node:<< set the current node >>
        #@nl
        
        g.doHook("select2",c=c,new_v=p,old_v=old_p)
        g.doHook("select3",c=c,new_v=p,old_v=old_p)
        
        # g.printGc()
    #@nonl
    #@-node:tree.select (ORIGINAL)
    #@+node:tree.set...LabelState (ORIGINAL)
    def setNormalLabelState (self,p): # selected, editing
    
        # g.trace(p)
        if p and p.edit_text():
            #@        << set editing headline colors >>
            #@+node:<< set editing headline colors >>
            config = g.app.config
            fg   = config.getWindowPref("headline_text_editing_foreground_color")
            bg   = config.getWindowPref("headline_text_editing_background_color")
            selfg = config.getWindowPref("headline_text_editing_selection_foreground_color")
            selbg = config.getWindowPref("headline_text_editing_selection_background_color")
            
            if not fg or not bg:
                fg,bg = "black","white"
            
            try:
                if selfg and selbg:
                    p.edit_text().configure(
                        selectforeground=selfg,selectbackground=selbg,
                        state="normal",highlightthickness=1,fg=fg,bg=bg)
                else:
                    p.edit_text().configure(
                        state="normal",highlightthickness=1,fg=fg,bg=bg)
            except:
                g.es_exception()
            #@nonl
            #@-node:<< set editing headline colors >>
            #@nl
            p.edit_text().tag_remove("sel","1.0","end")
            p.edit_text().tag_add("sel","1.0","end")
            g.app.gui.set_focus(self.c,p.edit_text())
    
    def setDisabledLabelState (self,p): # selected, disabled
    
        # g.trace(p,g.callerName(2),g.callerName(3))
        if p and p.edit_text():
            #@        << set selected, disabled headline colors >>
            #@+node:<< set selected, disabled headline colors >>
            config = g.app.config
            fg = config.getWindowPref("headline_text_selected_foreground_color")
            bg = config.getWindowPref("headline_text_selected_background_color")
            
            if not fg or not bg:
                fg,bg = "black","gray80"
            
            try:
                p.edit_text().configure(
                    state="disabled",highlightthickness=0,fg=fg,bg=bg)
            except:
                g.es_exception()
            #@nonl
            #@-node:<< set selected, disabled headline colors >>
            #@nl
    
    def setSelectedLabelState (self,p): # selected, not editing
    
        # g.trace(p)
        self.setDisabledLabelState(p)
    
    def setUnselectedLabelState (self,p): # not selected.
    
        # g.trace(p)
        if p and p.edit_text():
            #@        << set unselected headline colors >>
            #@+node:<< set unselected headline colors >>
            config = g.app.config
            fg = config.getWindowPref("headline_text_unselected_foreground_color")
            bg = config.getWindowPref("headline_text_unselected_background_color")
            
            if not fg or not bg:
                fg,bg = "black","white"
            
            try:
                p.edit_text().configure(
                    state="disabled",highlightthickness=0,fg=fg,bg=bg)
            except:
                g.es_exception()
            #@nonl
            #@-node:<< set unselected headline colors >>
            #@nl
    #@-node:tree.set...LabelState (ORIGINAL)
    #@+node:dimEditLabel, undimEditLabel
    # Convenience methods so the caller doesn't have to know the present edit node.
    
    def dimEditLabel (self):
        
        p = self.c.currentPosition()
        self.setDisabledLabelState(p)
    
    def undimEditLabel (self):
    
        p = self.c.currentPosition()
        self.setSelectedLabelState(p)
    #@nonl
    #@-node:dimEditLabel, undimEditLabel
    #@+node:tree.expandAllAncestors
    def expandAllAncestors (self,p):
        
        redraw_flag = False
    
        for p in p.parents_iter():
            if not p.isExpanded():
                p.expand()
                redraw_flag = True
    
        return redraw_flag
    
    #@-node:tree.expandAllAncestors
    #@-node:Selecting & editing (tree)
    #@+node:tree.moveUpDown
    def OnUpKey   (self,event=None): return self.moveUpDown("up")
    def OnDownKey (self,event=None): return self.moveUpDown("down")
    
    def moveUpDown (self,upOrDown):
        c = self.c ; body = c.frame.bodyCtrl
        # Make the insertion cursor visible so bbox won't return an empty list.
        body.see("insert")
        # Find the coordinates of the cursor and set the new height.
        # There may be roundoff errors because character postions may not match exactly.
        ins =  body.index("insert")
        lines,char = g.scanf(ins,"%d.%d")
        x,y,junk,textH = body.bbox("insert")
        bodyW,bodyH = body.winfo_width(),body.winfo_height()
        junk,maxy,junk,junk = body.bbox("@%d,%d" % (bodyW,bodyH))
        # Make sure y is within text boundaries.
        if upOrDown == "up":
            if y <= textH:
                body.yview("scroll",-1,"units")
            else: y = max(y-textH,0)
        else:
            if y >= maxy:
                body.yview("scroll",1,"units")
            else: y = min(y+textH,maxy)
        # Position the cursor on the proper side of the characters.
        newx,newy,width,junk = body.bbox("@%d,%d" % (x,y))
        if x > newx + width/2:
            x = newx + width + 1
        result = body.index("@%d,%d" % (x,y))
        body.mark_set("insert",result)
        # g.trace("entry:  %s.%s" % (lines,char))
        # g.trace("result:",result)
        # g.trace("insert:",body.index("insert"))
        return "break" # Inhibit further bindings.
    #@nonl
    #@-node:tree.moveUpDown
    #@+node:Updating routines (tree)...
    #@+node:tree.redraw
    # Calling redraw inside c.beginUpdate()/c.endUpdate() does nothing.
    # This _is_ useful when a flag is passed to c.endUpdate.
    
    def redraw (self,event=None):
        
        # g.trace(self.updateCount,self.redrawScheduled)
        
        if self.updateCount == 0 and not self.redrawScheduled:
            self.redrawScheduled = True
            self.canvas.after_idle(self.idle_redraw)
    #@nonl
    #@-node:tree.redraw
    #@+node:tkTree.redrawAfterException
    #@+at 
    #@nonl
    # This is called only from doCommand.  The implicit assumption is that 
    # doCommand itself is not contained in a beginUpdate/endUpdate pair.
    #@-at
    #@@c
    
    def redrawAfterException (self):
        
        """Make sure drawing is enabled following an exception."""
            
        if not self.redrawScheduled:
            self.redrawScheduled = True
            self.canvas.after_idle(self.idle_redraw)
            self.updateCount = 0 # would not work if we are in a beginUpdate/endUpdate pair.
    #@nonl
    #@-node:tkTree.redrawAfterException
    #@+node:force_redraw
    # Schedules a redraw even if inside beginUpdate/endUpdate
    def force_redraw (self):
        
        # g.trace(self.redrawScheduled)
        # import traceback ; traceback.print_stack()
    
        if not self.redrawScheduled:
            self.redrawScheduled = True
            self.canvas.after_idle(self.idle_redraw)
    #@nonl
    #@-node:force_redraw
    #@+node:redraw_now
    # Redraws immediately: used by Find so a redraw doesn't mess up selections in headlines.
    
    def redraw_now (self,scroll=True):
        
        # g.trace()
        
        # Bug fix: 4/24/04: cancel any pending redraw "by hand".
        # Make _sure_ that no other redraws take place after this.
        self.disableRedraw = True
        self.canvas.update_idletasks()
        self.disableRedraw = False
            
        # Now do the actual redraw.
        self.idle_redraw(scroll=scroll)
    #@nonl
    #@-node:redraw_now
    #@+node:idle_redraw
    def idle_redraw (self,scroll=True):
        
        c = self.c ; frame = c.frame
    
        self.redrawScheduled = False # Always do this here.
    
        #@    << return if disabled, or quitting or dragging >>
        #@+node:<< return if disabled, or quitting or dragging >>
        if self.disableRedraw:
            # We have been called as the result of an update_idletasks in the log pane.
            # Don't do anything now.
            return
        
        if frame not in g.app.windowList or g.app.quitting:
            # g.trace("no frame")
            return
        
        if self.drag_p:
            # g.trace("dragging",self.drag_p)
            return
        #@-node:<< return if disabled, or quitting or dragging >>
        #@nl
    
        # g.print_bindings("canvas",self.canvas)
    
        self.expandAllAncestors(c.currentPosition())
    
        oldcursor = self.canvas['cursor']
        self.canvas['cursor'] = "watch"
    
        if not g.doHook("redraw-entire-outline",c=self.c):
            c.setTopVnode(None)
            self.setVisibleAreaToFullCanvas()
            self.drawTopTree()
            # Set up the scroll region after the tree has been redrawn.
            x0, y0, x1, y1 = self.canvas.bbox("all")
            self.canvas.configure(scrollregion=(0, 0, x1, y1))
            # Do a scrolling operation after the scrollbar is redrawn
            if scroll:
                self.canvas.after_idle(self.idle_scrollTo)
            if self.trace:
                self.redrawCount += 1
                print "idle_redraw allocated:",self.redrawCount
        g.doHook("after-redraw-outline",c=self.c)
    
        self.canvas['cursor'] = oldcursor
    #@nonl
    #@-node:idle_redraw
    #@+node:idle_second_redraw
    def idle_second_redraw (self):
        
        c = self.c
        
        g.trace()
            
        # Erase and redraw the entire tree the SECOND time.
        # This ensures that all visible nodes are allocated.
        c.setTopVnode(None)
        args = self.canvas.yview()
        self.setVisibleArea(args)
        
        if 0:
            self.deleteBindings()
            self.canvas.delete("all")
        self.drawTopTree()
        
        if self.trace:
            print "idle_second_redraw allocated:",self.redrawCount
    #@nonl
    #@-node:idle_second_redraw
    #@-node:Updating routines (tree)...
    #@+node:Widget allocation...
    #@+node:newBox
    def newBox (self):
        
        if self.newlyFreedBoxes:
            id = self.newlyFreedBoxes.pop()
    
        elif self.freeBoxes:
            id = self.freeBoxes.pop()
    
        else:
            id = self.canvas.create_image(0,0,tag="plusBox")
            assert(not self.ids.get(id))
            
        self.visibleBoxes.append(id)
        
        return id
    #@nonl
    #@-node:newBox
    #@+node:newClickBox
    def newClickBox (self):
    
        if self.newlyFreedClickBoxes:
            id = self.newlyFreedClickBoxes.pop()
    
        elif self.freeClickBoxes:
            id = self.freeClickBoxes.pop()
    
        else:
            id = self.canvas.create_rectangle(0,0,0,0,tag="clickBox")
            assert(not self.ids.get(id))
            
        self.visibleClickBoxes.append(id)
        return id
    #@nonl
    #@-node:newClickBox
    #@+node:newIcon
    def newIcon (self):
    
        if self.newlyFreedIcons:
            id = self.newlyFreedIcons.pop()
    
        elif self.freeIcons:
            id = self.freeIcons.pop()
    
        else:
            id = self.canvas.create_image(0,0,anchor="nw",tag="iconBox")
            assert(not self.ids.get(id))
            
        self.visibleIcons.append(id)
        return id
            
        
    #@nonl
    #@-node:newIcon
    #@+node:newLine
    def newLine (self):
        
        if self.newlyFreedLines:
            id = self.newlyFreedLines.pop()
    
        elif self.freeLines:
            id = self.freeLines.pop()
        
        else:
            id = self.canvas.create_line(0,0,0,0,tag="lines",fill="gray50") # stipple="gray25")
            assert(not self.ids.get(id))
            
        self.visibleLines.append(id)
        return id
    #@nonl
    #@-node:newLine
    #@+node:newText
    def newText (self,forceAllocate=False):
        
        # Never allocate newly-free widgets...
        if not forceAllocate and self.newlyFreedText:
                    data = self.newlyFreedText.pop()
                    id,t = data
                    # t.configure(bg="blue")
        elif not forceAllocate and self.freeText:
            data = self.freeText.pop()
            id,t = data
            # t.configure(bg="red")
        else:
            # Tags are not valid in Tk.Text widgets, so we use class bindings instead.
            t = Tk.Text(self.canvas,state="normal",font=self.font,bd=0,relief="flat",height=1)
            # t.configure(bg="yellow")
            if self.useBindtags:
                t.bindtags(self.textBindings)
            else:
                t.bind("<Button-1>", self.onHeadlineClick)
                t.bind("<Button-3>", self.onHeadlineRightClick)
                t.bind("<Key>",      self.onHeadlineKey)
                t.bind("<Control-t>",self.onControlT)
            
            id = self.canvas.create_window(0,0,anchor="nw",window=t,tag="textBox")
            assert(not self.ids.get(id))
    
        data = id,t
        self.visibleText.append(data)
        return id,t
    #@nonl
    #@-node:newText
    #@+node:recycleWidgets
    def recycleWidgets (self):
        
        for id in self.visibleBoxes:
            self.newlyFreedBoxes.append(id)
        self.visibleBoxes = []
    
        for id in self.visibleClickBoxes:
            self.newlyFreedClickBoxes.append(id)
        self.visibleClickBoxes = []
        
        for id in self.visibleIcons:
            self.newlyFreedIcons.append(id)
        self.visibleIcons = []
            
        for id in self.visibleLines:
            self.newlyFreedLines.append(id)
        self.visibleLines = []
        
        for data in self.visibleText:
            id,t = data
            t.leo_position = None
            self.newlyFreedText.append(data)
        self.visibleText  = []
        
        if 0:
            g.trace("boxes",len(self.newlyFreedBoxes))
            g.trace("boxes",len(self.newlyFreedClickBoxes))
            g.trace("icons",len(self.newlyFreedIcons))
            g.trace("lines",len(self.newlyFreedLines))
            g.trace("text",len(self.newlyFreedText))
    #@nonl
    #@-node:recycleWidgets
    #@+node:hideNewlyFreedWidgets
    def hideNewlyFreedWidgets (self):
        
        """Hide all newly-freed widgets and move them to the free lists."""
        
        canvas = self.canvas
        
        #@    << hide all the newly-freed widgets >>
        #@+node:<< hide all the newly-freed widgets >>
        for id in self.newlyFreedBoxes:
            canvas.coords(id,-100,-100)
            
        for id in self.newlyFreedClickBoxes:
            canvas.coords(id,-100,-100,-100,-100)
        
        for id in self.newlyFreedIcons:
            canvas.coords(id,-100,-100)
        
        for id in self.newlyFreedLines:
            canvas.coords(id,-100,-100,-100,-100)
            
        for data in self.newlyFreedText:
            id,t = data
            canvas.coords(id,-100,-100)
            t.leo_position = None # Remove the reference immediately.
        #@nonl
        #@-node:<< hide all the newly-freed widgets >>
        #@nl
        #@    << move all newly-freed widgets to the free lists >>
        #@+node:<< move all newly-freed widgets to the free lists >>
        for id in self.newlyFreedBoxes:
            self.freeBoxes.append(id)
        self.newlyFreedBoxes = []
            
        for id in self.newlyFreedClickBoxes:
            self.freeClickBoxes.append(id)
        self.newlyFreedClickBoxes = []
            
        for id in self.newlyFreedIcons:
            self.freeIcons.append(id)
        self.newlyFreedIcons = []
            
        for id in self.newlyFreedLines:
            self.freeLines.append(id)
        self.newlyFreedLines = []
        
        for data in self.newlyFreedText:
            self.freeText.append(data)
        self.newlyFreedText = []
        #@nonl
        #@-node:<< move all newly-freed widgets to the free lists >>
        #@nl
        
        # g.trace(len(self.freeBoxes)+len(self.freeIcons)+len(self.freeLines)+len(self.freeText))
        
        if 0:
            g.trace("boxes",len(self.freeBoxes))
            g.trace("icons",len(self.freeIcons))
            g.trace("lines",len(self.freeLines))
            g.trace("text",len(self.freeText))
    #@nonl
    #@-node:hideNewlyFreedWidgets
    #@+node:totalTextWidgets
    def totalTextWidgets (self):
        
        n = len(self.visibleText) + len(self.newlyFreedText) + len(self.freeText)
        return n # Each item is a 2-tuple.
    #@nonl
    #@-node:totalTextWidgets
    #@+node:getTextStats
    def getTextStats (self):
        
        return "%3d %3d %3d tot: %4d" % (
            len(self.visibleText),
            len(self.newlyFreedText),
            len(self.freeText),
    
            len(self.visibleText) +
            len(self.newlyFreedText) +
            len(self.freeText)
        )
    #@nonl
    #@-node:getTextStats
    #@+node:traceIds
    def traceIds (self):
        
        keys = self.ids.keys()
        keys.sort
        for key in keys:
            p = self.ids.get(key)
            print key,p.headString()
    #@nonl
    #@-node:traceIds
    #@-node:Widget allocation...
    #@-others

leoTkinterTree.leoTkinterTree = myLeoTkinterTree
#@nonl
#@-node:@file __outlineExperiments.py
#@-leo
