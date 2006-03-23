#@+leo-ver=4-thin
#@+node:ekr.20040803072955:@thin leoTkinterTree.py
"""Override outline drawing code to test optimized drawing"""

"""This class implements a tree control similar to Windows explorer.

The code is based on code found in Python's IDLE program."""

#@@language python
#@@tabwidth -4
#@@pagewidth 80

#@<< about drawing >>
#@+node:ekr.20040803072955.1:  << About drawing >>
#@+at
# 
# New in Leo 4.4a3: The 'Newer World Order':
# 
# - c.redraw_now() redraws the screen immediately by calling 
# c.frame.tree.redraw_now().
# 
# - c.beginUpdate() and c.endUpdate() work as always.  They are the preferred 
# way of doing redraws.
# 
# - No drawing is done at idle time.
# 
# c.redraw_now and c.endUpdate redraw all icons automatically. v.computeIcon
# method tells what the icon should be. The v.iconVal tells what the present 
# icon
# is. The body key handler simply compares these two values and sets 
# redraw_flag
# if they don't match.
#@-at
#@nonl
#@-node:ekr.20040803072955.1:  << About drawing >>
#@nl
#@<< imports >>
#@+node:ekr.20040928101836:<< imports >>
import leoGlobals as g

if g.app and g.app.use_psyco:
    # print "enabled psyco classes",__file__
    try: from psyco.classes import *
    except ImportError: pass
    
Pmw = g.importExtension("Pmw",pluginName='LeoTkinterTree',verbose=True,required=True)

import leoFrame
import leoNodes
import Tkinter as Tk
import tkFont
import sys
#@nonl
#@-node:ekr.20040928101836:<< imports >>
#@nl

class leoTkinterTree (leoFrame.leoTree):
    
    callbacksInjected = False

    """Leo tkinter tree class."""
    
    #@    @+others
    #@+node:ekr.20040803072955.2:  Notes
    #@@killcolor
    #@nonl
    #@+node:ekr.20040803072955.3:Changes made since first update
    #@+at
    # 
    # - disabled drawing of user icons.  They weren't being hidden, which 
    # messed up scrolling.
    # 
    # - Expanded clickBox so all clicks fall inside it.
    # 
    # - Added binding for plugBox so it doesn't interfere with the clickBox.  
    # Another weirdness.
    # 
    # - Re-enabled code in drawText that sets the headline state.
    # 
    # - eventToPosition now returns p.copy, which means that nobody can change 
    # the list.
    # 
    # - Likewise, clear self.iconIds so old icon id's don't confuse 
    # findVnodeWithIconId.
    # 
    # - All drawing methods must do p = p.copy() at the beginning if they make 
    # any changes to p.
    #     - This ensures neither they nor their allies can change the caller's 
    # position.
    #     - In fact, though, only drawTree changes position.  It makes a copy 
    # before calling drawNode.
    #     *** Therefore, all positions in the drawing code are immutable!
    # 
    # - Fixed the race conditions that caused drawing sometimes to fail.  The 
    # essential idea is that we must not call w.config if we are about to do a 
    # redraw.  For full details, see the Notes node in the Race Conditions 
    # section.
    #@-at
    #@nonl
    #@-node:ekr.20040803072955.3:Changes made since first update
    #@+node:ekr.20040803072955.4:Changes made since second update
    #@+at
    # 
    # - Removed duplicate code in tree.select.  The following code was being 
    # called twice (!!):
    #     self.endEditLabel()
    #     self.setUnselectedLabelState(old_p)
    # 
    # - Add p.copy() instead of p when inserting nodes into data structures in 
    # select.
    # 
    # - Fixed a _major_ bug in Leo's core.  c.setCurrentPosition must COPY the 
    # position given to it!  It's _not_ enough to return a copy of position: 
    # it may already have changed!!
    # 
    # - Fixed a another (lesser??) bug in Leo's core.  handleUserClick should 
    # also make a copy.
    # 
    # - Fixed bug in mod_scripting.py.  The callback was failing if the script 
    # was empty.
    # 
    # - Put in the self.recycle ivar AND THE CODE STILL FAILS.
    #     It seems to me that this shows there is a bug in my code somewhere, 
    # but where ???????????????????
    #@-at
    #@nonl
    #@-node:ekr.20040803072955.4:Changes made since second update
    #@+node:ekr.20040803072955.5:Most recent changes
    #@+at
    # 
    # - Added generation count.
    #     - Incremented on each redraw.
    #     - Potentially a barrior to race conditions, but it never seemed to 
    # do anything.
    #     - This code is a candidate for elimination.
    # 
    # - Used vnodes rather than positions in several places.
    #     - I actually don't think this was involved in the real problem, and 
    # it doesn't hurt.
    # 
    # - Added much better traces: the beginning of the end for the bugs :-)
    #     - Added self.verbose option.
    #     - Added align keyword option to g.trace.
    #     - Separate each set of traces by a blank line.
    #         - This makes clear the grouping of id's.
    # 
    # - Defensive code: Disable dragging at start of redraw code.
    #     - This protects against race conditions.
    # 
    # - Fixed blunder 1: Fixed a number of bugs in the dragging code.
    #     - I had never looked at this code!
    #     - Eliminating false drags greatly simplifies matters.
    # 
    # - Fixed blunder 2: Added the following to eventToPosition:
    #         x = canvas.canvasx(x)
    #         y = canvas.canvasy(y)
    #     - Apparently this was the cause of false associations between icons 
    # and id's.
    #     - It's amazing that the code didn't fail earlier without these!
    # 
    # - Converted all module-level constants to ivars.
    # 
    # - Lines no longer interfere with eventToPosition.
    #     - The problem was that find_nearest or find_overlapping don't depend 
    # on stacking order!
    #     - Added p param to horizontal lines, but not vertical lines.
    #     - EventToPosition adds 1 to the x coordinate of vertical lines, then 
    # recomputes the id.
    # 
    # - Compute indentation only in forceDrawNode.  Removed child_indent 
    # constant.
    # 
    # - Simplified drawTree to use indentation returned from forceDrawNode.
    # 
    # - setText now ensures that state is "normal" before attempting to set 
    # the text.
    #     - This is the robust way.
    # 
    # 7/31/04: newText must call setText for all nodes allocated, even if p 
    # matches.
    #@-at
    #@nonl
    #@-node:ekr.20040803072955.5:Most recent changes
    #@-node:ekr.20040803072955.2:  Notes
    #@+node:ekr.20040803072955.15: Birth... (tkTree)
    #@+node:ekr.20040803072955.16:__init__ (tkTree)
    def __init__(self,c,frame,canvas):
        
        # Init the base class.
        leoFrame.leoTree.__init__(self,frame)
        
        trace = c.config.getBool('trace_chapters') and not g.app.unitTesting
        if trace: g.trace('tkTree')
        
        # Configuration and debugging settings.
        self.expanded_click_area    = c.config.getBool('expanded_click_area')
        self.gc_before_redraw       = c.config.getBool('gc_before_redraw')
        self.stayInTree             = c.config.getBool('stayInTreeAfterSelect')
    
        self.trace                  = c.config.getBool('trace_tree')
        self.trace_alloc            = c.config.getBool('trace_tree_alloc')
        self.trace_edit             = c.config.getBool('trace_tree_edit')
        self.trace_redraw_now       = c.config.getBool('trace_redraw_now')
        self.trace_select           = c.config.getBool('trace_select')
        self.trace_stats            = c.config.getBool('show_tree_stats')
     
        # Objects associated with this tree.
        self.canvas = canvas
        
        #@    << define drawing constants >>
        #@+node:ekr.20040803072955.17:<< define drawing constants >>
        self.box_padding = 5 # extra padding between box and icon
        self.box_width = 9 + self.box_padding
        self.icon_width = 20
        self.text_indent = 4 # extra padding between icon and tex
        
        self.hline_y = 7 # Vertical offset of horizontal line
        self.root_left = 7 + self.box_width
        self.root_top = 2
        
        self.default_line_height = 17 + 2 # default if can't set line_height from font.
        self.line_height = self.default_line_height
        #@nonl
        #@-node:ekr.20040803072955.17:<< define drawing constants >>
        #@nl
        #@    << old ivars >>
        #@+node:ekr.20040803072955.18:<< old ivars >>
        # Miscellaneous info.
        self.iconimages = {} # Image cache set by getIconImage().
        self.active = False # True if tree is active
        self._editPosition = None # Returned by leoTree.editPosition()
        self.lineyoffset = 0 # y offset for this headline.
        self.lastClickFrameId = None # id of last entered clickBox.
        self.lastColoredText = None # last colored text widget.
        
        # Set self.font and self.fontName.
        self.setFontFromConfig()
        self.setColorFromConfig()
        
        # Drag and drop
        self.drag_p = None
        self.controlDrag = False # True: control was down when drag started.
        
        # Keep track of popup menu so we can handle behavior better on Linux Context menu
        self.popupMenu = None
        
        # Incremental redraws:
        self.allocateOnlyVisibleNodes = False # True: enable incremental redraws.
        self.prevMoveToFrac = None
        self.visibleArea = None
        self.expandedVisibleArea = None
        
        if self.allocateOnlyVisibleNodes:
            self.frame.bar1.bind("<B1-ButtonRelease>", self.redraw_now)
        #@nonl
        #@-node:ekr.20040803072955.18:<< old ivars >>
        #@nl
        #@    << inject callbacks into the position class >>
        #@+node:ekr.20040803072955.19:<< inject callbacks into the position class >>
        # The new code injects 3 callbacks for the colorizer.
        
        if not leoTkinterTree.callbacksInjected: # Class var.
            leoTkinterTree.callbacksInjected = True
            self.injectCallbacks()
        #@nonl
        #@-node:ekr.20040803072955.19:<< inject callbacks into the position class >>
        #@nl
        
        self.dragging = False
        self.generation = 0
        self.prevPositions = 0
        self.redrawing = False # Used only to disable traces.
        self.redrawCount = 0 # Count for debugging.
        self.revertHeadline = None # Previous headline text for abortEditLabel.
        
        # New in 4.4: We should stay in the tree to use per-pane bindings.
        self.textBindings = [] # Set in setBindings.
        self.textNumber = 0 # To make names unique.
        self.updateCount = 0 # Drawing is enabled only if self.updateCount <= 0
        self.verbose = True
        
        self.setEditPosition(None) # Set positions returned by leoTree.editPosition()
        
        # Keys are id's, values are positions...
        self.ids = {}
        self.iconIds = {}
    
        # Lists of visible (in-use) widgets...
        self.visibleBoxes = []
        self.visibleClickBoxes = []
        self.visibleIcons = []
        self.visibleLines = []
        self.visibleText  = {}
            # Pre 4.4b2: Keys are vnodes, values are Tk.Text widgets.
            #     4.4b2: Keys are p.key(), values are Tk.Text widgets.
        self.visibleUserIcons = []
    
        # Lists of free, hidden widgets...
        self.freeBoxes = []
        self.freeClickBoxes = []
        self.freeIcons = []
        self.freeLines = []
        self.freeText = [] # New in 4.4b2: a list of free Tk.Text widgets
       
        self.freeUserIcons = []
    #@nonl
    #@-node:ekr.20040803072955.16:__init__ (tkTree)
    #@+node:ekr.20051024102724:tkTtree.setBindings
    def setBindings (self):
        
        '''Create master bindings for all headlines.'''
        
        tree = self ; k = self.c.k
        
        #@    << make bindings for a common binding widget >>
        #@+node:ekr.20060131173440:<< make bindings for a common binding widget >>
        self.bindingWidget = t = Tk.Text(self.canvas,name='bindingWidget')
        
        t.bind('<Key>',k.masterKeyHandler)
        
        table = (
            ('<Button-1>',       k.masterClickHandler,          tree.onHeadlineClick),
            ('<Button-3>',       k.masterClick3Handler,         tree.onHeadlineRightClick),
            ('<Double-Button-1>',k.masterDoubleClickHandler,    tree.onHeadlineClick),
            ('<Double-Button-3>',k.masterDoubleClick3Handler,   tree.onHeadlineRightClick),
        )
        
        for a,handler,func in table:
            def treeBindingCallback(event,handler=handler,func=func):
                return handler(event,func)
            t.bind(a,treeBindingCallback)
            
        self.textBindings = t.bindtags()
        #@nonl
        #@-node:ekr.20060131173440:<< make bindings for a common binding widget >>
        #@nl
    
        self.canvas.bind('<Key>',k.masterKeyHandler)
        self.canvas.bind('<Button-1>',self.onTreeClick)
    
        #@    << make bindings for tagged items on the canvas >>
        #@+node:ekr.20060131173440.2:<< make bindings for tagged items on the canvas >>
        where = g.choose(self.expanded_click_area,'clickBox','plusBox')
        
        table = (
            (where,    '<Button-1>',self.onClickBoxClick),
            ('iconBox','<Button-1>',self.onIconBoxClick),
            ('iconBox','<Double-1>',self.onIconBoxDoubleClick),
            ('iconBox','<Button-3>',self.onIconBoxRightClick),
            ('iconBox','<Double-3>',self.onIconBoxRightClick),
            ('iconBox','<B1-Motion>',self.onDrag),
            ('iconBox','<Any-ButtonRelease-1>',self.onEndDrag),
        )
        for tag,event,callback in table:
            self.canvas.tag_bind(tag,event,callback)
        #@-node:ekr.20060131173440.2:<< make bindings for tagged items on the canvas >>
        #@nl
        #@    << create baloon bindings for tagged items on the canvas >>
        #@+node:ekr.20060307080642:<< create baloon bindings for tagged items on the canvas >>
        if 0: # I find these very irritating.
            for tag,text in (
                # ('plusBox','plusBox'),
                ('iconBox','Icon Box'),
                ('selectBox','Click to select'),
                ('clickBox','Click to expand or contract'),
                # ('textBox','Headline'),
            ):
                # A fairly long wait is best.
                balloon = Pmw.Balloon(self.canvas,initwait=700)
                balloon.tagbind(self.canvas,tag,balloonHelp=text)
        #@nonl
        #@-node:ekr.20060307080642:<< create baloon bindings for tagged items on the canvas >>
        #@nl
    #@nonl
    #@-node:ekr.20051024102724:tkTtree.setBindings
    #@+node:ekr.20040803072955.21:injectCallbacks
    def injectCallbacks(self):
        
        #@    << define tkinter callbacks to be injected in the position class >>
        #@+node:ekr.20040803072955.22:<< define tkinter callbacks to be injected in the position class >>
        # N.B. These vnode methods are entitled to know about details of the leoTkinterTree class.
        
        #@+others
        #@+node:ekr.20040803072955.23:OnHyperLinkControlClick
        def OnHyperLinkControlClick (self,event):
            
            """Callback injected into position class."""
            
            p = self ; c = p.c
            try:
                if not g.doHook("hypercclick1",c=c,p=p,v=p,event=event):
                    c.beginUpdate()
                    try:
                        c.selectPosition(p)
                    finally:
                        c.endUpdate()
                    c.frame.bodyCtrl.mark_set("insert","1.0")
                g.doHook("hypercclick2",c=c,p=p,v=p,event=event)
            except:
                g.es_event_exception("hypercclick")
        #@nonl
        #@-node:ekr.20040803072955.23:OnHyperLinkControlClick
        #@+node:ekr.20040803072955.24:OnHyperLinkEnter
        def OnHyperLinkEnter (self,event=None):
            
            """Callback injected into position class."""
        
            try:
                p = self ; c = p.c
                if not g.doHook("hyperenter1",c=c,p=p,v=p,event=event):
                    if 0: # This works, and isn't very useful.
                        c.frame.bodyCtrl.tag_config(p.tagName,background="green")
                g.doHook("hyperenter2",c=c,p=p,v=p,event=event)
            except:
                g.es_event_exception("hyperenter")
        #@nonl
        #@-node:ekr.20040803072955.24:OnHyperLinkEnter
        #@+node:ekr.20040803072955.25:OnHyperLinkLeave
        def OnHyperLinkLeave (self,event=None):
            
            """Callback injected into position class."""
        
            try:
                p = self ; c = p.c
                if not g.doHook("hyperleave1",c=c,p=p,v=p,event=event):
                    if 0: # This works, and isn't very useful.
                        c.frame.bodyCtrl.tag_config(p.tagName,background="white")
                g.doHook("hyperleave2",c=c,p=p,v=p,event=event)
            except:
                g.es_event_exception("hyperleave")
        #@nonl
        #@-node:ekr.20040803072955.25:OnHyperLinkLeave
        #@-others
        
        #@-node:ekr.20040803072955.22:<< define tkinter callbacks to be injected in the position class >>
        #@nl
    
        for f in (OnHyperLinkControlClick,OnHyperLinkEnter,OnHyperLinkLeave):
            
            g.funcToMethod(f,leoNodes.position)
    #@nonl
    #@-node:ekr.20040803072955.21:injectCallbacks
    #@-node:ekr.20040803072955.15: Birth... (tkTree)
    #@+node:ekr.20040803072955.6:Allocation...
    #@+node:ekr.20040803072955.7:newBox
    def newBox (self,p,x,y,image):
        
        canvas = self.canvas ; tag = "plusBox"
    
        if self.freeBoxes:
            theId = self.freeBoxes.pop(0)
            canvas.coords(theId,x,y)
            canvas.itemconfigure(theId,image=image)
        else:
            theId = canvas.create_image(x,y,image=image,tag=tag)
            
        if self.trace_alloc:
            g.trace("%3d %3d %3d %8s" % (theId,x,y,' '),p.headString(),align=-20)
    
        assert(theId not in self.visibleBoxes)
        self.visibleBoxes.append(theId)
    
        # assert(not self.ids.get(theId))
        # assert(p)
        self.ids[theId] = p
    
        return theId
    #@nonl
    #@-node:ekr.20040803072955.7:newBox
    #@+node:ekr.20040803072955.8:newClickBox
    def newClickBox (self,p,x1,y1,x2,y2):
        
        canvas = self.canvas ; defaultColor = ""
        tag = g.choose(p.hasChildren(),'clickBox','selectBox')
    
        if self.freeClickBoxes:
            theId = self.freeClickBoxes.pop(0)
            canvas.coords(theId,x1,y1,x2,y2)
            canvas.itemconfig(theId,tag=tag)
        else:
            theId = self.canvas.create_rectangle(x1,y1,x2,y2,tag=tag)
            canvas.itemconfig(theId,fill=defaultColor,outline=defaultColor)
            
        if self.trace_alloc:
            g.trace("%3d %3d %3d %3d %3d" % (theId,x1,y1,x2,y2),p.headString(),align=-20)
    
        assert(theId not in self.visibleClickBoxes)
        self.visibleClickBoxes.append(theId)
        
        # assert(p)
        # assert(not self.ids.get(theId))
        self.ids[theId] = p
        
        return theId
    #@nonl
    #@-node:ekr.20040803072955.8:newClickBox
    #@+node:ekr.20040803072955.9:newIcon
    def newIcon (self,p,x,y,image):
        
        canvas = self.canvas ; tag = "iconBox"
    
        if self.freeIcons:
            theId = self.freeIcons.pop(0)
            canvas.itemconfigure(theId,image=image)
            canvas.coords(theId,x,y)
        else:
            theId = canvas.create_image(x,y,image=image,anchor="nw",tag=tag)
            # assert(not self.ids.get(theId))
    
        # assert(theId not in self.visibleIcons)
        self.visibleIcons.append(theId)
        
        # assert(p)
        # assert(not self.iconIds.get(theId))
        # assert(not self.ids.get(theId))
        data = p,self.generation
        self.iconIds[theId] = data # Remember which vnode belongs to the icon.
        self.ids[theId] = p
    
        return theId
    #@nonl
    #@-node:ekr.20040803072955.9:newIcon
    #@+node:ekr.20040803072955.10:newLine
    def newLine (self,p,x1,y1,x2,y2):
        
        canvas = self.canvas
        
        if self.freeLines:
            theId = self.freeLines.pop(0)
            canvas.coords(theId,x1,y1,x2,y2)
        else:
            theId = canvas.create_line(x1,y1,x2,y2,tag="lines",fill="gray50") # stipple="gray25")
            # assert(not self.ids.get(theId))
    
        # assert(not self.ids.get(theId))
        self.ids[theId] = p
        self.visibleLines.append(theId)
    
        return theId
    #@nonl
    #@-node:ekr.20040803072955.10:newLine
    #@+node:ekr.20040803072955.11:newText (leoTkinterTree)
    def newText (self,p,x,y):
        
        canvas = self.canvas ; tag = "textBox"
        c = self.c ;  k = c.k
    
        found = len(self.freeText) > 0
        if found:
            t,theId = self.freeText.pop()
            if self.trace_alloc: g.trace('%4d' % (theId),self.textAddr(t),'recycled')
            canvas.coords(theId,x,y) # Make the window visible again.
                # theId is the id of the *window* not the text.
    
        else:
            # Tags are not valid in Tk.Text widgets.
            self.textNumber += 1
            t = Tk.Text(canvas,name='head-%d' % self.textNumber,
                state="normal",font=self.font,bd=0,relief="flat",height=1)
            t.bindtags(self.textBindings) # Set the bindings for this widget.
    
            if 0: # Crashes on XP.
                #@            << patch by Maciej Kalisiak to handle scroll-wheel events >>
                #@+node:ekr.20050618045715:<< patch by Maciej Kalisiak  to handle scroll-wheel events >>
                def PropagateButton4(e):
                    canvas.event_generate("<Button-4>")
                    return "break"
                
                def PropagateButton5(e):
                    canvas.event_generate("<Button-5>")
                    return "break"
                
                def PropagateMouseWheel(e):
                    canvas.event_generate("<MouseWheel>")
                    return "break"
                
                instance_tag = t.bindtags()[0]
                t.bind_class(instance_tag, "<Button-4>", PropagateButton4)
                t.bind_class(instance_tag, "<Button-5>", PropagateButton5)
                t.bind_class(instance_tag, "<MouseWheel>",PropagateMouseWheel)
                #@nonl
                #@-node:ekr.20050618045715:<< patch by Maciej Kalisiak  to handle scroll-wheel events >>
                #@nl
        
            theId = canvas.create_window(x,y,anchor="nw",window=t,tag=tag)
            t.leo_window_id = theId # Never changes.
            
            if self.trace_alloc:
                g.trace('%4d' % (theId),self.textAddr(t),'** new')
                
        # Common configuration.
        if 0: # Doesn't seem to work.
            balloon = Pmw.Balloon(canvas,initwait=700)
            balloon.tagbind(canvas,theId,balloonHelp='Headline')
                
        self.ids[theId] = p # Add the id of the *window*
        self.setText(theId,t,p.headString())
        t.configure(width=self.headWidth(p=p))
        t.leo_position = p # This p never changes.
            # *Required*: onHeadlineClick uses w.leo_position to get p.
    
        # Keys are p.key().  Entries are (t,theId)
        self.visibleText [p.key()] = t,theId
        
        return t
    #@nonl
    #@-node:ekr.20040803072955.11:newText (leoTkinterTree)
    #@+node:ekr.20040803072955.12:recycleWidgets
    def recycleWidgets (self):
        
        canvas = self.canvas
        
        for theId in self.visibleBoxes:
            # assert(theId not in self.freeBoxes)
            self.freeBoxes.append(theId)
            canvas.coords(theId,-100,-100)
        self.visibleBoxes = []
        
        for theId in self.visibleClickBoxes:
            # assert(theId not in self.freeClickBoxes)
            self.freeClickBoxes.append(theId)
            canvas.coords(theId,-100,-100,-100,-100)
        self.visibleClickBoxes = []
        
        for theId in self.visibleIcons:
            # assert(theId not in self.freeIcons)
            self.freeIcons.append(theId)
            canvas.coords(theId,-100,-100)
        self.visibleIcons = []
            
        for theId in self.visibleLines:
            # assert(theId not in self.freeLines)
            self.freeLines.append(theId)
            canvas.coords(theId,-100,-100,-100,-100)
        self.visibleLines = []
        
       
        aList = self.visibleText.values()
        for t,theId in aList:
            # assert theId == t.leo_window_id
            canvas.coords(theId,-100,-100)
            t.leo_position = None # Allow the position to be freed.
        self.freeText.extend(aList)
        self.visibleText = {}
    
        for theId in self.visibleUserIcons:
            # The present code does not recycle user Icons.
            self.canvas.delete(theId)
        self.visibleUserIcons = []
    #@nonl
    #@-node:ekr.20040803072955.12:recycleWidgets
    #@+node:ekr.20040803072955.13:destroyWidgets
    def destroyWidgets (self):
    
        self.ids = {}
    
        self.visibleBoxes = []
        self.visibleClickBoxes = []
        self.visibleIcons = []
        self.visibleLines = []
        self.visibleUserIcons = []
    
        self.visibleText = {}
        
        self.freeText = []
        self.freeBoxes = []
        self.freeClickBoxes = []
        self.freeIcons = []
        self.freeLines = []
        
        self.canvas.delete("all")
    #@nonl
    #@-node:ekr.20040803072955.13:destroyWidgets
    #@+node:ekr.20060202125419:showStats
    def showStats (self):
    
        z = []
        for kind,a,b in (
            ('boxes',self.visibleBoxes,self.freeBoxes),
            ('clickBoxes',self.visibleClickBoxes,self.freeClickBoxes),
            ('icons',self.visibleIcons,self.freeIcons),
            ('lines',self.visibleLines,self.freeLines),
            ('tesxt',self.visibleText.values(),self.freeText),
        ):
            z.append('%10s used: %4d free: %4d' % (kind,len(a),len(b)))
            
        g.es_print('\n' + '\n'.join(z))
    #@nonl
    #@-node:ekr.20060202125419:showStats
    #@-node:ekr.20040803072955.6:Allocation...
    #@+node:ekr.20040803072955.26:Config & Measuring...
    #@+node:ekr.20040803072955.27:tree.getFont,setFont,setFontFromConfig
    def getFont (self):
    
        return self.font
    
    def setFont (self,font=None, fontName=None):
        
        # ESSENTIAL: retain a link to font.
        if fontName:
            self.fontName = fontName
            self.font = tkFont.Font(font=fontName)
        else:
            self.fontName = None
            self.font = font
            
        self.setLineHeight(self.font)
        
    # Called by ctor and when config params are reloaded.
    def setFontFromConfig (self):
        c = self.c
        font = c.config.getFontFromParams(
            "headline_text_font_family", "headline_text_font_size",
            "headline_text_font_slant",  "headline_text_font_weight",
            c.config.defaultTreeFontSize)
        
        self.setFont(font)
    #@nonl
    #@-node:ekr.20040803072955.27:tree.getFont,setFont,setFontFromConfig
    #@+node:ekr.20040803072955.28:headWidth & widthInPixels
    def headWidth(self,p=None,s=''):
    
        """Returns the proper width of the entry widget for the headline."""
        
        if p: s = p.headString()
    
        return self.font.measure(s)/self.font.measure('0')+1
    
        
    def widthInPixels(self,s):
    
        s = g.toEncodedString(s,g.app.tkEncoding)
        
        return self.font.measure(s)
    #@nonl
    #@-node:ekr.20040803072955.28:headWidth & widthInPixels
    #@+node:ekr.20040803072955.29:setLineHeight
    def setLineHeight (self,font):
        
        try:
            metrics = font.metrics()
            linespace = metrics ["linespace"]
            self.line_height = linespace + 5 # Same as before for the default font on Windows.
            # print metrics
        except:
            self.line_height = self.default_line_height
            g.es("exception setting outline line height")
            g.es_exception()
    #@nonl
    #@-node:ekr.20040803072955.29:setLineHeight
    #@+node:ekr.20040803072955.30:tkTree.setColorFromConfig
    def setColorFromConfig (self):
        
        c = self.c
    
        bg = c.config.getColor("outline_pane_background_color") or 'white'
    
        try:
            self.canvas.configure(bg=bg)
        except:
            g.es("exception setting outline pane background color")
            g.es_exception()
    #@nonl
    #@-node:ekr.20040803072955.30:tkTree.setColorFromConfig
    #@-node:ekr.20040803072955.26:Config & Measuring...
    #@+node:ekr.20040803072955.31:Debugging...
    #@+node:ekr.20040803072955.32:setText
    def setText (self,theId,t,s):
        
        """All changes to text widgets should come here."""
    
        if self.trace_alloc: g.trace('%4d' % (theId), self.textAddr(t),s)
                
        state = t.cget("state")
        if state != "normal":
            t.configure(state="normal")
        t.delete("1.0","end")
        t.insert("end",s)
        if state != "normal":
            t.configure(state=state)
    #@nonl
    #@-node:ekr.20040803072955.32:setText
    #@+node:ekr.20040803072955.33:textAddr
    def textAddr(self,t):
        
        """Return the address part of repr(Tk.Text)."""
        
        return repr(t)[-9:-1].lower()
    #@nonl
    #@-node:ekr.20040803072955.33:textAddr
    #@+node:ekr.20040803072955.34:traceIds (Not used)
    # Verbose tracing is much more useful than this because we can see the recent past.
    
    def traceIds (self,full=False):
        
        tree = self
        
        for theDict,tag,flag in ((tree.ids,"ids",True),(tree.iconIds,"icon ids",False)):
            print '=' * 60
            print ; print "%s..." % tag
            keys = theDict.keys()
            keys.sort()
            for key in keys:
                p = tree.ids.get(key)
                if p is None: # For lines.
                    print "%3d None" % key
                else:
                    print "%3d" % key,p.headString()
            if flag and full:
                print '-' * 40
                values = theDict.values()
                values.sort()
                seenValues = []
                for value in values:
                    if value not in seenValues:
                        seenValues.append(value)
                        for item in theDict.items():
                            key,val = item
                            if val and val == value:
                                print "%3d" % key,val.headString()  
    #@nonl
    #@-node:ekr.20040803072955.34:traceIds (Not used)
    #@-node:ekr.20040803072955.31:Debugging...
    #@+node:ekr.20040803072955.35:Drawing... (tkTree)
    #@+node:ekr.20051216155728:tree.begin/endUpdate
    def beginUpdate (self):
        
        self.updateCount += 1
        # g.trace('tree',id(self),self.updateCount,g.callers())
        
    def endUpdate (self,flag,scroll=False):
        
        self.updateCount -= 1
        # g.trace('  tree',id(self),self.updateCount,g.callers())
        
        if self.updateCount <= 0:
            if flag:
                self.redraw_now(scroll=scroll)
            if self.updateCount < 0:
                g.trace("Can't happen: negative updateCount",g.callers())
    #@nonl
    #@-node:ekr.20051216155728:tree.begin/endUpdate
    #@+node:ekr.20040803072955.58:redraw_now & helper
    # Redraws immediately: used by Find so a redraw doesn't mess up selections in headlines.
    
    # New in 4.4b2: suppress scrolling by default.
    
    def redraw_now (self,scroll=False):
    
        if g.app.quitting or self.drag_p or self.frame not in g.app.windowList:
            return
            
        c = self.c ;  self.redrawCount += 1
        
        if not g.app.unitTesting:
            if self.gc_before_redraw:
                g.collectGarbage()
            if g.app.trace_gc_verbose:
                if (self.redrawCount % 5) == 0:
                    g.printGcSummary(trace=True)
            if self.trace_redraw_now or self.trace_alloc:
                # g.trace(self.redrawCount,g.callers())
                g.trace(c.rootPosition().headString(),'canvas:',id(self.canvas),g.callers())
                if self.trace_stats:
                    g.print_stats()
                    g.clear_stats()
                    
        # New in 4.4b2: Call endEditLabel, but suppress the redraw.
        self.beginUpdate()
        try:
            self.endEditLabel()
        finally:
            self.endUpdate(False)
    
        # Do the actual redraw.
        self.expandAllAncestors(c.currentPosition())
        self.redrawHelper(scroll=scroll)
        self.canvas.update_idletasks() # Important for unit tests.
        c.masterFocusHandler()
        
    redraw = redraw_now # Compatibility
    #@nonl
    #@+node:ekr.20040803072955.59:redrawHelper
    def redrawHelper (self,scroll=True):
        
        c = self.c
        oldcursor = self.canvas['cursor']
        self.canvas['cursor'] = "watch"
    
        if not g.doHook("redraw-entire-outline",c=c):
            c.setTopVnode(None)
            self.setVisibleAreaToFullCanvas()
            self.drawTopTree()
            # Set up the scroll region after the tree has been redrawn.
            x0, y0, x1, y1 = self.canvas.bbox("all")
            self.canvas.configure(scrollregion=(0, 0, x1, y1))
            if scroll:
                self.canvas.update_idletasks() # Essential.
                self.scrollTo()
                
        g.doHook("after-redraw-outline",c=c)
    
        self.canvas['cursor'] = oldcursor
    #@nonl
    #@-node:ekr.20040803072955.59:redrawHelper
    #@-node:ekr.20040803072955.58:redraw_now & helper
    #@+node:ekr.20040803072955.61:idle_second_redraw
    def idle_second_redraw (self):
        
        c = self.c
            
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
            g.trace(self.redrawCount)
    #@nonl
    #@-node:ekr.20040803072955.61:idle_second_redraw
    #@+node:ekr.20051105073850:drawX...
    #@+node:ekr.20040803072955.36:drawBox
    def drawBox (self,p,x,y):
    
        tree = self ; c = self.c
        y += 7 # draw the box at x, y+7
        
        theId = g.doHook("draw-outline-box",tree=tree,c=c,p=p,v=p,x=x,y=y)
            
        if theId is None:
            iconname = g.choose(p.isExpanded(),"minusnode.gif", "plusnode.gif")
            image = self.getIconImage(iconname)
            theId = self.newBox(p,x,y+self.lineyoffset,image)
            return theId
        else:
            return theId
    #@nonl
    #@-node:ekr.20040803072955.36:drawBox
    #@+node:ekr.20040803072955.37:drawClickBox
    def drawClickBox (self,p,y):
    
        h = self.line_height
        
        # Define a slighly larger rect to catch clicks.
        if self.expanded_click_area:
            self.newClickBox(p,0,y,1000,y+h-2)
    #@nonl
    #@-node:ekr.20040803072955.37:drawClickBox
    #@+node:ekr.20040803072955.39:drawIcon
    def drawIcon(self,p,x=None,y=None):
        
        """Draws icon for position p at x,y, or at p.v.iconx,p.v.icony if x,y = None,None"""
    
        c = self.c
        #@    << compute x,y and iconVal >>
        #@+node:ekr.20040803072955.40:<< compute x,y and iconVal >>
        v = p.v
        
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
        #@-node:ekr.20040803072955.40:<< compute x,y and iconVal >>
        #@nl
    
        if not g.doHook("draw-outline-icon",tree=self,c=c,p=p,v=p,x=x,y=y):
    
            # Get the image.
            imagename = "box%02d.GIF" % val
            image = self.getIconImage(imagename)
            self.newIcon(p,x,y+self.lineyoffset,image)
            
        return 0,self.icon_width # dummy icon height,width
    #@nonl
    #@-node:ekr.20040803072955.39:drawIcon
    #@+node:ekr.20040803072955.41:drawLine
    def drawLine (self,p,x1,y1,x2,y2):
        
        theId = self.newLine(p,x1,y1,x2,y2)
        
        return theId
    #@-node:ekr.20040803072955.41:drawLine
    #@+node:ekr.20040803072955.42:drawNode & force_draw_node (good trace)
    def drawNode(self,p,x,y):
        
        c = self.c
        
        # g.trace(x,y,p,id(self.canvas))
        
        data = g.doHook("draw-outline-node",tree=self,c=c,p=p,v=p,x=x,y=y)
        if data is not None: return data
    
        if 1:
            self.lineyoffset = 0
        else:
            if hasattr(p.v.t,"unknownAttributes"):
                self.lineyoffset = p.v.t.unknownAttributes.get("lineYOffset",0)
            else:
                self.lineyoffset = 0
        
        # Draw the horizontal line.
        self.drawLine(p,
            x,y+7+self.lineyoffset,
            x+self.box_width,y+7+self.lineyoffset)
        
        if self.inVisibleArea(y):
            return self.force_draw_node(p,x,y)
        else:
            return self.line_height,0
    #@nonl
    #@+node:ekr.20040803072955.43:force_draw_node
    def force_draw_node(self,p,x,y):
    
        h = 0 # The total height of the line.
        indent = 0 # The amount to indent this line.
        
        h2,w2 = self.drawUserIcons(p,"beforeBox",x,y)
        h = max(h,h2) ; x += w2 ; indent += w2
    
        if p.hasChildren():
            self.drawBox(p,x,y)
    
        indent += self.box_width
        x += self.box_width # even if box isn't drawn.
    
        h2,w2 = self.drawUserIcons(p,"beforeIcon",x,y)
        h = max(h,h2) ; x += w2 ; indent += w2
    
        h2,w2 = self.drawIcon(p,x,y)
        h = max(h,h2) ; x += w2 ; indent += w2/2
        
        # Nothing after here affects indentation.
        h2,w2 = self.drawUserIcons(p,"beforeHeadline",x,y)
        h = max(h,h2) ; x += w2
    
        h2 = self.drawText(p,x,y)
        h = max(h,h2)
        x += self.widthInPixels(p.headString())
    
        h2,w2 = self.drawUserIcons(p,"afterHeadline",x,y)
        h = max(h,h2)
        
        self.drawClickBox(p,y)
    
        return h,indent
    #@nonl
    #@-node:ekr.20040803072955.43:force_draw_node
    #@-node:ekr.20040803072955.42:drawNode & force_draw_node (good trace)
    #@+node:ekr.20040803072955.44:drawText
    def drawText(self,p,x,y):
        
        """draw text for position p at nominal coordinates x,y."""
        
        assert(p)
    
        c = self.c
        x += self.text_indent
        
        data = g.doHook("draw-outline-text-box",tree=self,c=c,p=p,v=p,x=x,y=y)
        if data is not None: return data
        
        self.newText(p,x,y+self.lineyoffset)
       
        self.configureTextState(p)
    
        return self.line_height
    #@nonl
    #@-node:ekr.20040803072955.44:drawText
    #@+node:ekr.20040803072955.46:drawUserIcons
    def drawUserIcons(self,p,where,x,y):
        
        """Draw any icons specified by p.v.t.unknownAttributes["icons"]."""
        
        h,w = 0,0 ; t = p.v.t
        
        if not hasattr(t,"unknownAttributes"):
            return h,w
        
        iconsList = t.unknownAttributes.get("icons")
        if not iconsList:
            return h,w
        
        try:
            for theDict in iconsList:
                h2,w2 = self.drawUserIcon(p,where,x,y,w,theDict)
                h = max(h,h2) ; w += w2
        except:
            g.es_exception()
            
        # g.trace(where,h,w)
    
        return h,w
    #@nonl
    #@-node:ekr.20040803072955.46:drawUserIcons
    #@+node:ekr.20040803072955.47:drawUserIcon
    def drawUserIcon (self,p,where,x,y,w2,theDict):
        
        h,w = 0,0
    
        if where != theDict.get("where","beforeHeadline"):
            return h,w
    
        # g.trace(where,x,y,theDict)
        
        #@    << set offsets and pads >>
        #@+node:ekr.20040803072955.48:<< set offsets and pads >>
        xoffset = theDict.get("xoffset")
        try:    xoffset = int(xoffset)
        except: xoffset = 0
        
        yoffset = theDict.get("yoffset")
        try:    yoffset = int(yoffset)
        except: yoffset = 0
        
        xpad = theDict.get("xpad")
        try:    xpad = int(xpad)
        except: xpad = 0
        
        ypad = theDict.get("ypad")
        try:    ypad = int(ypad)
        except: ypad = 0
        #@nonl
        #@-node:ekr.20040803072955.48:<< set offsets and pads >>
        #@nl
        theType = theDict.get("type")
        if theType == "icon":
            if 0: # not ready yet.
                s = theDict.get("icon")
                #@            << draw the icon in string s >>
                #@+node:ekr.20040803072955.49:<< draw the icon in string s >>
                pass
                #@nonl
                #@-node:ekr.20040803072955.49:<< draw the icon in string s >>
                #@nl
        elif theType == "file":
            theFile = theDict.get("file")
            #@        << draw the icon at file >>
            #@+node:ekr.20040803072955.50:<< draw the icon at file >>
            try:
                image = self.iconimages[theFile]
                # Get the image from the cache if possible.
            except KeyError:
                try:
                    fullname = g.os_path_join(g.app.loadDir,"..","Icons",theFile)
                    fullname = g.os_path_normpath(fullname)
                    image = Tk.PhotoImage(master=self.canvas,file=fullname)
                    self.iconimages[fullname] = image
                except:
                    #g.es("Exception loading: " + fullname)
                    #g.es_exception()
                    image = None
                    
            if image:
                theId = self.canvas.create_image(
                    x+xoffset+w2,y+yoffset,
                    anchor="nw",image=image,tag="userIcon")
                self.ids[theId] = p
                # assert(theId not in self.visibleIcons)
                self.visibleUserIcons.append(theId)
            
                h = image.height() + yoffset + ypad
                w = image.width()  + xoffset + xpad
            
            #@-node:ekr.20040803072955.50:<< draw the icon at file >>
            #@nl
        elif theType == "url":
            ## url = theDict.get("url")
            #@        << draw the icon at url >>
            #@+node:ekr.20040803072955.51:<< draw the icon at url >>
            pass
            #@nonl
            #@-node:ekr.20040803072955.51:<< draw the icon at url >>
            #@nl
            
        # Allow user to specify height, width explicitly.
        h = theDict.get("height",h)
        w = theDict.get("width",w)
    
        return h,w
    #@nonl
    #@-node:ekr.20040803072955.47:drawUserIcon
    #@+node:ekr.20040803072955.52:drawTopTree
    def drawTopTree (self):
        
        """Draws the top-level tree, taking into account the hoist state."""
        
        c = self.c ; canvas = self.canvas
    
        self.redrawing = True
        
        # Recycle all widgets.
        self.recycleWidgets()
        # Clear all ids so invisible id's don't confuse eventToPosition & findPositionWithIconId
        self.ids = {}
        self.iconIds = {}
        self.generation += 1
        self.drag_p = None # Disable drags across redraws.
        self.dragging = False
        if self.trace:
            self.redrawCount += 1
            # print ; print
            delta = g.app.positions - self.prevPositions
            # g.trace("**** gen: %-3d positions: %5d +%4d" % (
                # self.generation,g.app.positions,delta),g.callers())
            
        self.prevPositions = g.app.positions
    
        if c.hoistStack:
            bunch = c.hoistStack[-1]
            self.drawTree(bunch.p,self.root_left,self.root_top,0,0,hoistFlag=True)
        else:
            self.drawTree(c.rootPosition(),self.root_left,self.root_top,0,0)
    
        if self.trace_stats: self.showStats()
        
        canvas.lower("lines")  # Lowest.
        canvas.lift("textBox") # Not the Tk.Text widget: it should be low.
        canvas.lift("userIcon")
        canvas.lift("plusBox")
        canvas.lift("clickBox")
        canvas.lift("clickExpandBox")
        canvas.lift("iconBox") # Higest.
    
        self.redrawing = False
    #@nonl
    #@-node:ekr.20040803072955.52:drawTopTree
    #@+node:ekr.20040803072955.53:drawTree
    def drawTree(self,p,x,y,h,level,hoistFlag=False):
    
        tree = self ; c = self.c
        yfirst = ylast = y
        h1 = None
        
        data = g.doHook("draw-sub-outline",tree=tree,
            c=c,p=p,v=p,x=x,y=y,h=h,level=level,hoistFlag=hoistFlag)
        if data is not None: return data
        
        while p: # Do not use iterator.
            # N.B. This is the ONLY copy of p that needs to be made.
            # No other drawing routine calls any p.moveTo method.
            const_p = p.copy()
            h,indent = self.drawNode(const_p,x,y)
            if h1 is None: h1 = h
            y += h ; ylast = y
            if p.isExpanded() and p.hasFirstChild():
                # Must make an additional copy here by calling firstChild.
                y = self.drawTree(p.firstChild(),x+indent,y,h,level+1)
            if hoistFlag: break
            else:         p = p.next()
            # g.trace(p)
            
        # Draw the vertical line.
        if level==0: # Special case to get exposed first line exactly right.
            self.drawLine(None,x,yfirst+(h1-1)/2,x,ylast+self.hline_y-h)
        else:
            self.drawLine(None,x,yfirst-h1/2-1,x,ylast+self.hline_y-h)
        return y
    #@nonl
    #@-node:ekr.20040803072955.53:drawTree
    #@-node:ekr.20051105073850:drawX...
    #@+node:ekr.20040803072955.62:Helpers...
    #@+node:ekr.20040803072955.63:inVisibleArea & inExpandedVisibleArea
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
    #@-node:ekr.20040803072955.63:inVisibleArea & inExpandedVisibleArea
    #@+node:ekr.20040803072955.64:getIconImage
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
    #@-node:ekr.20040803072955.64:getIconImage
    #@+node:ekr.20040803072955.65:scrollTo
    def scrollTo(self,p=None):
    
        """Scrolls the canvas so that p is in view."""
        
        __pychecker__ = '--no-argsused' # event not used.
    
        c = self.c ; frame = c.frame
        if not p or not p.exists(c):
            p = c.currentPosition()
        if not p or not p.exists(c):
            # g.trace('current p does not exist',p)
            p = c.rootPosition()
        if not p or not p.exists(c):
            # g.trace('no position')
            return
        try:
            last = p.lastVisible()
            nextToLast = last.visBack()
            h1 = self.yoffset(p)
            h2 = self.yoffset(last)
            #@        << compute approximate line height >>
            #@+node:ekr.20040803072955.66:<< compute approximate line height >>
            if nextToLast: # 2/2/03: compute approximate line height.
                lineHeight = h2 - self.yoffset(nextToLast)
            else:
                lineHeight = 20 # A reasonable default.
            #@nonl
            #@-node:ekr.20040803072955.66:<< compute approximate line height >>
            #@nl
            #@        << Compute the fractions to scroll down/up >>
            #@+node:ekr.20040803072955.67:<< Compute the fractions to scroll down/up >>
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
            #@-node:ekr.20040803072955.67:<< Compute the fractions to scroll down/up >>
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
            # g.trace("%3d %3d %1.3f %1.3f %1.3f %1.3f" % (h1,h2,frac,frac2,lo,hi))
        except:
            g.es_exception()
            
    idle_scrollTo = scrollTo # For compatibility.
    #@nonl
    #@-node:ekr.20040803072955.65:scrollTo
    #@+node:ekr.20040803072955.68:numberOfVisibleNodes
    def numberOfVisibleNodes(self):
        
        n = 0 ; p = self.c.rootPosition()
        while p:
            n += 1
            p.moveToVisNext()
        return n
    #@nonl
    #@-node:ekr.20040803072955.68:numberOfVisibleNodes
    #@+node:ekr.20040803072955.70:yoffset
    #@+at 
    #@nonl
    # We can't just return icony because the tree hasn't been redrawn yet.
    # For the same reason we can't rely on any TK canvas methods here.
    #@-at
    #@@c
    
    def yoffset(self,p1):
        # if not p1.isVisible(): print "yoffset not visible:",p1
        root = self.c.rootPosition()
        h,flag = self.yoffsetTree(root,p1)
        # flag can be False during initialization.
        # if not flag: print "yoffset fails:",h,v1
        return h
    
    def yoffsetTree(self,p,p1):
        h = 0
        if not p.exists(self.c):
            # g.trace('does not exist',p.headString())
            return h,False # An extra precaution.
        p = p.copy()
        for p2 in p.siblings_iter():
            # print "yoffsetTree:", p2
            if p2 == p1:
                return h, True
            h += self.line_height
            if p2.isExpanded() and p2.hasChildren():
                child = p2.firstChild()
                h2, flag = self.yoffsetTree(child,p1)
                h += h2
                if flag: return h, True
        return h, False
    #@nonl
    #@-node:ekr.20040803072955.70:yoffset
    #@-node:ekr.20040803072955.62:Helpers...
    #@-node:ekr.20040803072955.35:Drawing... (tkTree)
    #@+node:ekr.20040803072955.71:Event handlers (tkTree)
    #@+node:ekr.20051105103233:Helpers
    #@+node:ekr.20040803072955.72:checkWidgetList
    def checkWidgetList (self,tag):
        
        return True # This will fail when the headline actually changes!
        
        for t in self.visibleText:
            
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
    #@-node:ekr.20040803072955.72:checkWidgetList
    #@+node:ekr.20040803072955.73:dumpWidgetList
    def dumpWidgetList (self,tag):
        
        print
        print "checkWidgetList: %s" % tag
        
        for t in self.visibleText:
            
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
    #@-node:ekr.20040803072955.73:dumpWidgetList
    #@+node:ekr.20040803072955.75:edit_widget
    def edit_widget (self,p):
        
        """Returns the Tk.Edit widget for position p."""
    
        return self.findEditWidget(p)
        
    edit_text = edit_widget # For compatibility.
    #@nonl
    #@-node:ekr.20040803072955.75:edit_widget
    #@+node:ekr.20040803072955.74:eventToPosition
    def eventToPosition (self,event):
    
        canvas = self.canvas
        x,y = event.x,event.y
        x = canvas.canvasx(x) 
        y = canvas.canvasy(y)
        if self.trace: g.trace(x,y)
        item = canvas.find_overlapping(x,y,x,y)
        if not item: return None
    
        # Item may be a tuple, possibly empty.
        try:    theId = item[0]
        except: theId = item
        if not theId: return None
    
        p = self.ids.get(theId)
        
        # A kludge: p will be None for vertical lines.
        if not p:
            item = canvas.find_overlapping(x+1,y,x+1,y)
            try:    theId = item[0]
            except: theId = item
            if not theId:
                g.es_print('oops: eventToPosition failed')
                return None
            p = self.ids.get(theId)
            # g.trace("was vertical line",p)
        
        if self.trace and self.verbose:
            if p:
                w = self.findEditWidget(p)
                g.trace("%3d %3d %3d %d" % (theId,x,y,id(w)),p.headString())
            else:
                g.trace("%3d %3d %3d" % (theId,x,y),None)
            
        # defensive programming: this copy is not needed.
        if p: return p.copy() # Make _sure_ nobody changes this table!
        else: return None
    #@nonl
    #@-node:ekr.20040803072955.74:eventToPosition
    #@+node:ekr.20040803072955.76:findEditWidget
    def findEditWidget (self,p):
        
        """Return the Tk.Text item corresponding to p."""
    
        c = self.c
    
        if p and c:
            aTuple = self.visibleText.get(p.key())
            if aTuple:
                t,theId = aTuple
                # if self.trace: g.trace('%4d' % (theId),self.textAddr(t),p.headString())
                return t
            else:
                # g.trace('oops: not found',p)
                return None
    
        # g.trace(not found',p.headString())
        return None
    #@nonl
    #@-node:ekr.20040803072955.76:findEditWidget
    #@+node:ekr.20040803072955.109:findVnodeWithIconId
    def findPositionWithIconId (self,theId):
        
        # Due to an old bug, theId may be a tuple.
        try:
            data = self.iconIds.get(theId[0])
        except:
            data = self.iconIds.get(theId)
    
        if data:
            p,generation = data
            if generation==self.generation:
                if self.trace and self.verbose:
                    g.trace(theId,p.headString())
                return p
            else:
                if self.trace and self.verbose:
                    g.trace("*** wrong generation: %d ***" % theId)
                return None
        else:
            if self.trace and self.verbose: g.trace(theId,None)
            return None
    #@nonl
    #@-node:ekr.20040803072955.109:findVnodeWithIconId
    #@-node:ekr.20051105103233:Helpers
    #@+node:ekr.20040803072955.78:Click Box...
    #@+node:ekr.20040803072955.79:onClickBoxClick
    def onClickBoxClick (self,event,p=None):
        
        c = self.c ; p1 = c.currentPosition()
        
        if not p: p = self.eventToPosition(event)
        if not p: return
        
        c.setLog()
    
        c.beginUpdate()
        try:
            if p and not g.doHook("boxclick1",c=c,p=p,v=p,event=event):
                c.endEditing()
                self.active = True
                if p == p1 or c.config.getBool('initialClickExpandsOrContractsNode'):
                    if p.isExpanded(): p.contract()
                    else:              p.expand()
                self.select(p)
                if c.frame.findPanel:
                    c.frame.findPanel.handleUserClick(p)
                if self.stayInTree:
                    c.treeWantsFocus()
                else:
                    c.bodyWantsFocus()
            g.doHook("boxclick2",c=c,p=p,v=p,event=event)
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20040803072955.79:onClickBoxClick
    #@-node:ekr.20040803072955.78:Click Box...
    #@+node:ekr.20040803072955.99:Dragging
    #@+node:ekr.20041111115908:endDrag
    def endDrag (self,event):
        
        """The official helper of the onEndDrag event handler."""
    
        c = self.c ; p = self.drag_p
        c.setLog()
        canvas = self.canvas
        if not event: return
    
        c.beginUpdate()
        try:
            #@        << set vdrag, childFlag >>
            #@+node:ekr.20040803072955.104:<< set vdrag, childFlag >>
            x,y = event.x,event.y
            canvas_x = canvas.canvasx(x)
            canvas_y = canvas.canvasy(y)
            
            theId = self.canvas.find_closest(canvas_x,canvas_y)
            # theId = self.canvas.find_overlapping(canvas_x,canvas_y,canvas_x,canvas_y)
            
            vdrag = self.findPositionWithIconId(theId)
            childFlag = vdrag and vdrag.hasChildren() and vdrag.isExpanded()
            #@nonl
            #@-node:ekr.20040803072955.104:<< set vdrag, childFlag >>
            #@nl
            if c.config.getBool("allow_clone_drags"):
                if not c.config.getBool("look_for_control_drag_on_mouse_down"):
                    self.controlDrag = c.frame.controlKeyIsDown
        
            if vdrag and vdrag.v.t != p.v.t: # Disallow drag to joined node.
                #@            << drag p to vdrag >>
                #@+node:ekr.20041111114148:<< drag p to vdrag >>
                # g.trace("*** end drag   ***",theId,x,y,p.headString(),vdrag.headString())
                
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
                #@nonl
                #@-node:ekr.20041111114148:<< drag p to vdrag >>
                #@nl
            elif self.trace and self.verbose:
                g.trace("Cancel drag")
            
            # Reset the old cursor by brute force.
            self.canvas['cursor'] = "arrow"
            self.dragging = False
            self.drag_p = None
        finally:
            # Must set self.drag_p = None first.
            c.endUpdate()
            c.recolor_now() # Dragging can affect coloring.
    #@nonl
    #@-node:ekr.20041111115908:endDrag
    #@+node:ekr.20041111114944:startDrag
    # This precomputes numberOfVisibleNodes(), a significant optimization.
    # We also indicate where findPositionWithIconId() should start looking for tree id's.
    
    def startDrag (self,event,p=None):
        
        """The official helper of the onDrag event handler."""
        
        c = self.c ; canvas = self.canvas
        
        if not p:
            assert(not self.drag_p)
            x = canvas.canvasx(event.x)
            y = canvas.canvasy(event.y)
            theId = canvas.find_closest(x,y)
            # theId = canvas.find_overlapping(canvas_x,canvas_y,canvas_x,canvas_y)
            if theId is None: return
            try: theId = theId[0]
            except: pass
            p = self.ids.get(theId)
        if not p: return
        c.setLog()
        self.drag_p = p.copy() # defensive programming: not needed.
        self.dragging = True
        # g.trace("*** start drag ***",theId,self.drag_p.headString())
        # Only do this once: greatly speeds drags.
        self.savedNumberOfVisibleNodes = self.numberOfVisibleNodes()
        if c.config.getBool("allow_clone_drags"):
            self.controlDrag = c.frame.controlKeyIsDown
            if c.config.getBool("look_for_control_drag_on_mouse_down"):
                if c.config.getBool("enable_drag_messages"):
                    if self.controlDrag:
                        g.es("dragged node will be cloned")
                    else:
                        g.es("dragged node will be moved")
        else: self.controlDrag = False
        self.canvas['cursor'] = "hand2" # "center_ptr"
    #@nonl
    #@-node:ekr.20041111114944:startDrag
    #@+node:ekr.20040803072955.100:onContinueDrag
    def onContinueDrag(self,event):
        
        p = self.drag_p
        if not p: return
    
        try:
            canvas = self.canvas ; frame = self.c.frame
            if event:
                x,y = event.x,event.y
            else:
                x,y = frame.top.winfo_pointerx(),frame.top.winfo_pointery()
                # Stop the scrolling if we go outside the entire window.
                if x == -1 or y == -1: return 
            if self.dragging: # This gets cleared by onEndDrag()
                #@            << scroll the canvas as needed >>
                #@+node:ekr.20040803072955.101:<< scroll the canvas as needed >>
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
                        canvas.after_idle(self.onContinueDrag,None) # Don't propagate the event.
                #@nonl
                #@-node:ekr.20040803072955.101:<< scroll the canvas as needed >>
                #@nl
        except:
            g.es_event_exception("continue drag")
    #@nonl
    #@-node:ekr.20040803072955.100:onContinueDrag
    #@+node:ekr.20040803072955.102:onDrag
    def onDrag(self,event):
        
        c = self.c ; p = self.drag_p
        if not event: return
    
        c.setLog()
        
        if not self.dragging:
            if not g.doHook("drag1",c=c,p=p,v=p,event=event):
                self.startDrag(event)
            g.doHook("drag2",c=c,p=p,v=p,event=event)
            
        if not g.doHook("dragging1",c=c,p=p,v=p,event=event):
            self.onContinueDrag(event)
        g.doHook("dragging2",c=c,p=p,v=p,event=event)
    #@nonl
    #@-node:ekr.20040803072955.102:onDrag
    #@+node:ekr.20040803072955.103:onEndDrag
    def onEndDrag(self,event):
        
        """Tree end-of-drag handler called from vnode event handler."""
        
        c = self.c ; p = self.drag_p
        if not p: return
    
        c.setLog()
        
        if not g.doHook("enddrag1",c=c,p=p,v=p,event=event):
            self.endDrag(event)
        g.doHook("enddrag2",c=c,p=p,v=p,event=event)
    #@nonl
    #@-node:ekr.20040803072955.103:onEndDrag
    #@-node:ekr.20040803072955.99:Dragging
    #@+node:ekr.20040803072955.90:head key handlers
    #@+node:ekr.20040803072955.88:onHeadlineKey
    def onHeadlineKey (self,event):
        
        '''Handle a key event in a headline.'''
    
        w = event and event.widget or None
        ch = event and event.char or ''
        
        # g.trace(g.callers())
    
        # Testing for ch here prevents flashing in the headline
        # when the control key is held down.
        if ch:
            # g.trace(repr(ch),g.callers())
            self.updateHead(event,w)
    
        return 'break' # Required
    #@-node:ekr.20040803072955.88:onHeadlineKey
    #@+node:ekr.20051026083544.2:updateHead
    def updateHead (self,event,w):
        
        '''Update a headline from an event.
        
        The headline officially changes only when editing ends.'''
        
        c = self.c ; ch = event and event.char or ''
        i,j = g.app.gui.getTextSelection(w)
        
        # g.trace(repr(ch))
        
        if ch == '\b':
            if i != j:
                w.delete(i,j)
            else:
                w.delete('insert-1c')
        elif ch and ch not in ('\n','\r'):
            if i != j:
                w.delete(i,j)
            i = w.index('insert')
            w.insert(i,ch)
    
        s = w.get('1.0','end')
        if s.endswith('\n'):
            s = s[:-1]
        w.configure(width=self.headWidth(s=s))
    
        if ch in ('\n','\r'):
            self.endEditLabel() # Now calls self.onHeadChanged.
    #@-node:ekr.20051026083544.2:updateHead
    #@+node:ekr.20040803072955.91:onHeadChanged
    # Tricky code: do not change without careful thought and testing.
    
    def onHeadChanged (self,p,undoType='Typing'):
        
        '''Officially change a headline.
        Set the old undo text to the previous revert point.'''
        
        c = self.c ; u = c.undoer ; w = self.edit_widget(p)
        if not w: return
        
        ch = '\r' # New in 4.4: we only report the final keystroke.
        if g.doHook("headkey1",c=c,p=p,v=p,ch=ch):
            return # The hook claims to have handled the event.
    
        s = w.get('1.0','end')
        #@    << truncate s if it has multiple lines >>
        #@+node:ekr.20040803072955.94:<< truncate s if it has multiple lines >>
        # Remove one or two trailing newlines before warning of truncation.
        for i in (0,1):
            if s and s[-1] == '\n':
                if len(s) > 1: s = s[:-1]
                else: s = ''
        
        # Warn if there are multiple lines.
        i = s.find('\n')
        if i > -1:
            # g.trace(i,len(s),repr(s))
            g.es("Truncating headline to one line",color="blue")
            s = s[:i]
        
        limit = 1000
        if len(s) > limit:
            g.es("Truncating headline to %d characters" % (limit),color="blue")
            s = s[:limit]
        
        s = g.toUnicode(s or '',g.app.tkEncoding)
        #@nonl
        #@-node:ekr.20040803072955.94:<< truncate s if it has multiple lines >>
        #@nl
        c.beginUpdate()
        try:
            # Make the change official, but undo to the *old* revert point.
            oldRevert = self.revertHeadline
            changed = s != oldRevert
            self.revertHeadline = s
            p.initHeadString(s)
            if self.trace_edit and not g.app.unitTesting:
                if changed:
                    g.trace('changed: old',repr(oldRevert),'new',repr(s))
            if changed:
                undoData = u.beforeChangeNodeContents(p,oldHead=oldRevert)
                if not c.changed: c.setChanged(True)
                dirtyVnodeList = p.setDirty()
                u.afterChangeNodeContents(p,undoType,undoData,
                    dirtyVnodeList=dirtyVnodeList)
        finally:
            c.endUpdate()
            if changed:
                if self.stayInTree:
                    c.treeWantsFocus()
                else:
                    c.bodyWantsFocus()
       
        g.doHook("headkey2",c=c,p=p,v=p,ch=ch)
    #@-node:ekr.20040803072955.91:onHeadChanged
    #@-node:ekr.20040803072955.90:head key handlers
    #@+node:ekr.20040803072955.80:Icon Box...
    #@+node:ekr.20040803072955.81:onIconBoxClick
    def onIconBoxClick (self,event,p=None):
        
        c = self.c ; tree = self
        
        if not p: p = self.eventToPosition(event)
        if not p: return
        
        c.setLog()
        
        if self.trace and self.verbose: g.trace()
        
        if not g.doHook("iconclick1",c=c,p=p,v=p,event=event):
            if event:
                self.onDrag(event)
            tree.endEditLabel()
            tree.select(p)
            if c.frame.findPanel:
                c.frame.findPanel.handleUserClick(p)
        g.doHook("iconclick2",c=c,p=p,v=p,event=event)
            
        return "break" # disable expanded box handling.
    #@nonl
    #@-node:ekr.20040803072955.81:onIconBoxClick
    #@+node:ekr.20040803072955.89:onIconBoxRightClick
    def onIconBoxRightClick (self,event,p=None):
        
        """Handle a right click in any outline widget."""
    
        c = self.c
        
        if not p: p = self.eventToPosition(event)
        if not p: return
        
        c.setLog()
    
        try:
            if not g.doHook("iconrclick1",c=c,p=p,v=p,event=event):
                self.OnActivateHeadline(p)
                self.endEditLabel()
                self.OnPopup(p,event)
            g.doHook("iconrclick2",c=c,p=p,v=p,event=event)
        except:
            g.es_event_exception("iconrclick")
            
        return 'break'
    #@-node:ekr.20040803072955.89:onIconBoxRightClick
    #@+node:ekr.20040803072955.82:onIconBoxDoubleClick
    def onIconBoxDoubleClick (self,event,p=None):
        
        c = self.c
    
        if not p: p = self.eventToPosition(event)
        if not p: return
        
        c.setLog()
        
        if self.trace and self.verbose: g.trace()
        
        try:
            if not g.doHook("icondclick1",c=c,p=p,v=p,event=event):
                self.endEditLabel() # Bug fix: 11/30/05
                self.OnIconDoubleClick(p) # Call the method in the base class.
            g.doHook("icondclick2",c=c,p=p,v=p,event=event)
        except:
            g.es_event_exception("icondclick")
    #@nonl
    #@-node:ekr.20040803072955.82:onIconBoxDoubleClick
    #@-node:ekr.20040803072955.80:Icon Box...
    #@+node:ekr.20040803072955.105:OnActivateHeadline (tkTree)
    def OnActivateHeadline (self,p,event=None):
        
        '''Handle common process when any part of a headline is clicked.'''
        
        # g.trace(p.headString())
        
        returnVal = 'break' # Default: do nothing more.
    
        try:
            c = self.c
            c.setLog()
            #@        << activate this window >>
            #@+node:ekr.20040803072955.106:<< activate this window >>
            if p == c.currentPosition():
                # g.trace("is current")
                # The *second* click in the headline starts editing.
                if self.active:
                    self.editLabel(p)
                    returnVal = 'continue'
                else:
                    # Set the focus immediately.  This is essential for proper editing.
                    c.treeWantsFocusNow()
                    returnVal = 'break'
            else:
                # g.trace("not current")
                self.select(p)
                if c.frame.findPanel:
                    c.frame.findPanel.handleUserClick(p)
                if p.v.t.insertSpot != None:
                    c.frame.bodyCtrl.mark_set("insert",p.v.t.insertSpot)
                    c.frame.bodyCtrl.see(p.v.t.insertSpot)
                else:
                    c.frame.bodyCtrl.mark_set("insert","1.0")
                    
                if self.stayInTree:
                    c.treeWantsFocusNow()
                else:
                    c.bodyWantsFocusNow()
                returnVal = 'break'
            
            # The next click *in the same headline* will start editing.
            self.active = True
            #@nonl
            #@-node:ekr.20040803072955.106:<< activate this window >>
            #@nl
        except:
            g.es_event_exception("activate tree")
            
        return returnVal
    #@nonl
    #@-node:ekr.20040803072955.105:OnActivateHeadline (tkTree)
    #@+node:ekr.20040803072955.84:Text Box...
    #@+node:ekr.20040803072955.85:configureTextState
    def configureTextState (self,p):
        
        if not p: return
        
        # g.trace(p.headString(),self.c._currentPosition)
        
        if p.isCurrentPosition():
            if p == self.editPosition():
                self.setEditLabelState(p) # selected, editing.
            else:
                self.setSelectedLabelState(p) # selected, not editing.
        else:
            self.setUnselectedLabelState(p) # unselected
    #@nonl
    #@-node:ekr.20040803072955.85:configureTextState
    #@+node:ekr.20040803072955.86:onCtontrolT
    # This works around an apparent Tk bug.
    
    def onControlT (self,event=None):
    
        # If we don't inhibit further processing the Tx.Text widget switches characters!
        return "break"
    #@nonl
    #@-node:ekr.20040803072955.86:onCtontrolT
    #@+node:ekr.20040803072955.87:onHeadlineClick
    def onHeadlineClick (self,event,p=None):
        
        c = self.c ; w = event.widget
        
        if not p:
            try:
                p = w.leo_position
            except AttributeError:
                g.trace('*'*20,'oops')
        if not p: return 'break'
            
        # g.trace(p.headString())
        
        c.setLog()
    
        try:
            if not g.doHook("headclick1",c=c,p=p,v=p,event=event):
                returnVal = self.OnActivateHeadline(p)
            g.doHook("headclick2",c=c,p=p,v=p,event=event)
        except:
            returnVal = 'break'
            g.es_event_exception("headclick")
    
        # 'continue' is sometimes correct here.
        # 'break' would make it impossible to unselect the headline text.
        # g.trace('returnVal',returnVal,'stayInTree',self.stayInTree)
        return returnVal
    #@nonl
    #@-node:ekr.20040803072955.87:onHeadlineClick
    #@+node:ekr.20040803072955.83:onHeadlineRightClick
    def onHeadlineRightClick (self,event):
    
        """Handle a right click in any outline widget."""
    
        c = self.c ; w = event.widget
        
        try:
            p = w.leo_position
        except AttributeError:
            g.trace('*'*20,'oops')
            return 'break'
            
        c.setLog()
    
        try:
            if not g.doHook("headrclick1",c=c,p=p,v=p,event=event):
                self.OnActivateHeadline(p)
                self.endEditLabel()
                self.OnPopup(p,event)
            g.doHook("headrclick2",c=c,p=p,v=p,event=event)
        except:
            g.es_event_exception("headrclick")
            
        # 'continue' *is* correct here.
        # 'break' would make it impossible to unselect the headline text.
        return 'continue'
    #@-node:ekr.20040803072955.83:onHeadlineRightClick
    #@-node:ekr.20040803072955.84:Text Box...
    #@+node:ekr.20040803072955.108:tree.OnDeactivate
    def OnDeactivate (self,event=None):
        
        """Deactivate the tree pane, dimming any headline being edited."""
        
        __pychecker__ = '--no-argsused' # event not used.
    
        tree = self ; c = self.c
        
        # g.trace(g.callers())
       
        c.beginUpdate()
        try:
            tree.endEditLabel()
            tree.dimEditLabel()
        finally:
            c.endUpdate(False)
    #@nonl
    #@-node:ekr.20040803072955.108:tree.OnDeactivate
    #@+node:ekr.20040803072955.110:tree.OnPopup & allies
    def OnPopup (self,p,event):
        
        """Handle right-clicks in the outline.
        
        This is *not* an event handler: it is called from other event handlers."""
        
        # Note: "headrclick" hooks handled by vnode callback routine.
    
        if event != None:
            c = self.c
            c.setLog()
    
            if not g.doHook("create-popup-menu",c=c,p=p,v=p,event=event):
                self.createPopupMenu(event)
            if not g.doHook("enable-popup-menu-items",c=c,p=p,v=p,event=event):
                self.enablePopupMenuItems(p,event)
            if not g.doHook("show-popup-menu",c=c,p=p,v=p,event=event):
                self.showPopupMenu(event)
    
        return "break"
    #@nonl
    #@+node:ekr.20040803072955.111:OnPopupFocusLost
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
        
        __pychecker__ = '--no-argsused' # event not used.
    
        self.popupMenu.unpost()
    #@nonl
    #@-node:ekr.20040803072955.111:OnPopupFocusLost
    #@+node:ekr.20040803072955.112:createPopupMenu
    def createPopupMenu (self,event):
        
        __pychecker__ = '--no-argsused' # event not used.
        
        c = self.c ; frame = c.frame
        
        # If we are going to recreate it, we had better destroy it.
        if self.popupMenu:
            self.popupMenu.destroy()
            self.popupMenu = None
        
        self.popupMenu = menu = Tk.Menu(g.app.root, tearoff=0)
        
        # Add the Open With entries if they exist.
        if g.app.openWithTable:
            frame.menu.createOpenWithMenuItemsFromTable(menu,g.app.openWithTable)
            table = (("-",None,None),)
            frame.menu.createMenuEntries(menu,table)
            
        #@    << Create the menu table >>
        #@+node:ekr.20040803072955.113:<< Create the menu table >>
        table = (
            ("&Read @file Nodes",c.readAtFileNodes),
            ("&Write @file Nodes",c.fileCommands.writeAtFileNodes),
            ("-",None),
            ("&Tangle",c.tangle),
            ("&Untangle",c.untangle),
            ("-",None),
            ("Toggle Angle &Brackets",c.toggleAngleBrackets),
            ("-",None),
            ("Cut Node",c.cutOutline),
            ("Copy Node",c.copyOutline),
            ("&Paste Node",c.pasteOutline),
            ("&Delete Node",c.deleteOutline),
            ("-",None),
            ("&Insert Node",c.insertHeadline),
            ("&Clone Node",c.clone),
            ("Sort C&hildren",c.sortChildren),
            ("&Sort Siblings",c.sortSiblings),
            ("-",None),
            ("Contract Parent",c.contractParent),
        )
        #@nonl
        #@-node:ekr.20040803072955.113:<< Create the menu table >>
        #@nl
        
        # New in 4.4.  There is no need for a dontBind argument because
        # Bindings from tables are ignored.
        frame.menu.createMenuEntries(menu,table)
    #@nonl
    #@-node:ekr.20040803072955.112:createPopupMenu
    #@+node:ekr.20040803072955.114:enablePopupMenuItems
    def enablePopupMenuItems (self,v,event):
        
        """Enable and disable items in the popup menu."""
        
        __pychecker__ = '--no-argsused' # event not used.
        
        c = self.c ; menu = self.popupMenu
    
        #@    << set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>
        #@+node:ekr.20040803072955.115:<< set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>
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
        #@-node:ekr.20040803072955.115:<< set isAtRoot and isAtFile if v's tree contains @root or @file nodes >>
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
    #@-node:ekr.20040803072955.114:enablePopupMenuItems
    #@+node:ekr.20040803072955.116:showPopupMenu
    def showPopupMenu (self,event):
        
        """Show a popup menu."""
        
        c = self.c ; menu = self.popupMenu
    
        if sys.platform == "linux2": # 20-SEP-2002 DTHEIN: not needed for Windows
            menu.bind("<FocusOut>",self.OnPopupFocusLost)
        
        menu.post(event.x_root, event.y_root)
    
        # Set the focus immediately so we know when we lose it.
        c.widgetWantsFocus(menu)
    #@nonl
    #@-node:ekr.20040803072955.116:showPopupMenu
    #@-node:ekr.20040803072955.110:tree.OnPopup & allies
    #@+node:ekr.20051022141020:onTreeClick
    def onTreeClick (self,event=None):
        
        '''Handle an event in the tree canvas, outside of any tree widget.'''
        
        c = self.c
    
        c.treeWantsFocusNow()
        
        return 'break'
    #@nonl
    #@-node:ekr.20051022141020:onTreeClick
    #@-node:ekr.20040803072955.71:Event handlers (tkTree)
    #@+node:ekr.20040803072955.118:Incremental drawing...
    #@+node:ekr.20040803072955.119:allocateNodes
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
        self.updateTree(self.c.rootPosition(),self.root_left,self.root_top,0,0)
        # if self.updatedNodeCount: print "updatedNodeCount:", self.updatedNodeCount
    #@-node:ekr.20040803072955.119:allocateNodes
    #@+node:ekr.20040803072955.120:allocateNodesBeforeScrolling
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
    #@-node:ekr.20040803072955.120:allocateNodesBeforeScrolling
    #@+node:ekr.20040803072955.121:updateNode
    def updateNode (self,v,x,y):
        
        """Draw a node that may have become visible as a result of a scrolling operation"""
    
        if self.inExpandedVisibleArea(y):
            # This check is a major optimization.
            if not v.edit_widget():
                return self.force_draw_node(v,x,y)
            else:
                return self.line_height
    
        return self.line_height
    #@nonl
    #@-node:ekr.20040803072955.121:updateNode
    #@+node:ekr.20040803072955.122:setVisibleAreaToFullCanvas
    def setVisibleAreaToFullCanvas(self):
        
        if self.visibleArea:
            y1,y2 = self.visibleArea
            y2 = max(y2,y1 + self.canvas.winfo_height())
            self.visibleArea = y1,y2
    #@nonl
    #@-node:ekr.20040803072955.122:setVisibleAreaToFullCanvas
    #@+node:ekr.20040803072955.123:setVisibleArea
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
    #@-node:ekr.20040803072955.123:setVisibleArea
    #@+node:ekr.20040803072955.124:tree.updateTree
    def updateTree (self,v,x,y,h,level):
    
        yfirst = y
        if level==0: yfirst += 10
        while v:
            # g.trace(x,y,v)
            h,indent = self.updateNode(v,x,y)
            y += h
            if v.isExpanded() and v.firstChild():
                y = self.updateTree(v.firstChild(),x+indent,y,h,level+1)
            v = v.next()
        return y
    #@-node:ekr.20040803072955.124:tree.updateTree
    #@-node:ekr.20040803072955.118:Incremental drawing...
    #@+node:ekr.20040803072955.125:Selecting & editing... (tkTree)
    #@+node:ekr.20040803072955.142:dimEditLabel, undimEditLabel
    # Convenience methods so the caller doesn't have to know the present edit node.
    
    def dimEditLabel (self):
        
        p = self.c.currentPosition()
        self.setSelectedLabelState(p)
    
    def undimEditLabel (self):
    
        p = self.c.currentPosition()
        self.setSelectedLabelState(p)
    #@nonl
    #@-node:ekr.20040803072955.142:dimEditLabel, undimEditLabel
    #@+node:ekr.20040803072955.127:editLabel
    def editLabel (self,p):
        
        """Start editing p's headline."""
        
        c = self.c
    
        if self.editPosition() and p != self.editPosition():
            c.beginUpdate()
            try:
                self.endEditLabel()
            finally:
                c.endUpdate(False)
    
        self.setEditPosition(p) # That is, self._editPosition = p
        
        if self.trace_edit and not g.app.unitTesting:
            g.trace(p.headString(),g.choose(p.edit_widget(),'','no edit widget'))
    
        if p and p.edit_widget():
            self.revertHeadline = p.headString() # New in 4.4b2: helps undo.
            self.setEditLabelState(p) # Sets the focus immediately.
            c.headlineWantsFocus(p) # Make sure the focus sticks.
    #@nonl
    #@-node:ekr.20040803072955.127:editLabel
    #@+node:ekr.20040803072955.126:tree.endEditLabel
    def endEditLabel (self):
        
        '''End editing of a headline and update p.headString().'''
    
        c = self.c ; k = c.k ; p = c.currentPosition()
    
        self.setEditPosition(None) # That is, self._editPosition = None
        
        if k:
            k.setDefaultUnboundKeyAction()
            # k.showStateAndMode() # Destroys UNL info.
        
        # Important: this will redraw if necessary.
        self.onHeadChanged(p)
    #@nonl
    #@-node:ekr.20040803072955.126:tree.endEditLabel
    #@+node:ekr.20040803072955.143:tree.expandAllAncestors
    def expandAllAncestors (self,p):
        
        '''Expand all ancestors without redrawing.
        
        Return a flag telling whether a redraw is needed.'''
        
        c = self.c ; redraw_flag = False
    
        c.beginUpdate()
        try:
            for p in p.parents_iter():
                if not p.isExpanded():
                    p.expand()
                    redraw_flag = True
        finally:
            c.endUpdate(False)
    
        return redraw_flag
    #@nonl
    #@-node:ekr.20040803072955.143:tree.expandAllAncestors
    #@+node:ekr.20040803072955.128:tree.select
    #  Do **not** try to "optimize" this by returning if p==tree.currentPosition.
    
    def select (self,p,updateBeadList=True):
        
        '''Select a node.  Never redraws outline, but may change coloring of individual headlines.'''
        
        c = self.c ; frame = c.frame ; body = frame.bodyCtrl
        old_p = c.currentPosition()
        if not p or not p.exists(c):
            # g.trace('does not exist',p.headString())
            return # Not an error.
        
        if self.trace_select and not g.app.unitTesting: g.trace(g.callers())
    
        if not g.doHook("unselect1",c=c,new_p=p,old_p=old_p,new_v=p,old_v=old_p):
            if old_p:
                #@            << unselect the old node >>
                #@+node:ekr.20040803072955.129:<< unselect the old node >>
                # Remember the position of the scrollbar before making any changes.
                yview=body.yview()
                insertSpot = c.frame.body.getInsertionPoint()
                
                if old_p != p:
                    self.endEditLabel() # sets editPosition = None
                    self.setUnselectedLabelState(old_p) # 12/17/04
                
                if old_p.edit_widget():
                    old_p.v.t.scrollBarSpot = yview
                    old_p.v.t.insertSpot = insertSpot
                #@nonl
                #@-node:ekr.20040803072955.129:<< unselect the old node >>
                #@nl
    
        g.doHook("unselect2",c=c,new_p=p,old_p=old_p,new_v=p,old_v=old_p)
        
        if not g.doHook("select1",c=c,new_p=p,old_p=old_p,new_v=p,old_v=old_p):
            #@        << select the new node >>
            #@+node:ekr.20040803072955.130:<< select the new node >>
            # Bug fix: we must always set this, even if we never edit the node.
            self.revertHeadline = p.headString()
            
            frame.setWrap(p)
                
            # Always do this.  Otherwise there can be problems with trailing hewlines.
            s = g.toUnicode(p.v.t.bodyString,"utf-8")
            self.setText(0,body,s)
            
            # We must do a full recoloring: we may be changing context!
            self.frame.body.recolor_now(p) # recolor now uses p.copy(), so this is safe.
            
            if p.v and p.v.t.scrollBarSpot != None:
                first,last = p.v.t.scrollBarSpot
                body.yview("moveto",first)
            
            if p.v and p.v.t.insertSpot != None:
                c.frame.bodyCtrl.mark_set("insert",p.v.t.insertSpot)
                c.frame.bodyCtrl.see(p.v.t.insertSpot)
            else:
                c.frame.bodyCtrl.mark_set("insert","1.0")
                
            # g.trace("select:",p.headString())
            #@nonl
            #@-node:ekr.20040803072955.130:<< select the new node >>
            #@nl
            if p and p != old_p: # Suppress duplicate call.
                try: # may fail during initialization.
                    # p is NOT c.currentPosition() here!
                    self.canvas.update_idletasks() # Essential.
                    self.scrollTo(p)
                except Exception: pass
            #@        << update c.beadList or c.beadPointer >>
            #@+node:ekr.20040803072955.131:<< update c.beadList or c.beadPointer >>
            # c.beadList is the list of nodes for the back and forward commands.
            
            if updateBeadList:
                
                if c.beadPointer > -1:
                    present_p = c.beadList[c.beadPointer]
                else:
                    present_p = c.nullPosition()
                
                if p != present_p:
                    # Replace the tail of c.beadList by p and make p the present node.
                    c.beadPointer += 1
                    c.beadList[c.beadPointer:] = []
                    c.beadList.append(p.copy())
                    
                    # New in Leo 4.4: limit this list to 100 items.
                    if 0: # Doesn't work yet.
                        c.beadList = c.beadList [-100:]
                        g.trace('len(c.beadList)',len(c.beadList))
                    
                # g.trace(c.beadPointer,p,present_p)
            #@nonl
            #@-node:ekr.20040803072955.131:<< update c.beadList or c.beadPointer >>
            #@nl
            #@        << update c.visitedList >>
            #@+node:ekr.20040803072955.132:<< update c.visitedList >>
            # The test 'p in c.visitedList' calls p.__cmp__, so this code *is* valid.
            
            # Make p the most recently visited position on the list.
            if p in c.visitedList:
                c.visitedList.remove(p)
            
            c.visitedList.insert(0,p.copy())
            
            # g.trace('len(c.visitedList)',len(c.visitedList))
            # g.trace([z.headString()[:10] for z in c.visitedList]) # don't assign to p!
            #@nonl
            #@-node:ekr.20040803072955.132:<< update c.visitedList >>
            #@nl
    
        c.setCurrentPosition(p)
        #@    << set the current node >>
        #@+node:ekr.20040803072955.133:<< set the current node >>
        self.setSelectedLabelState(p)
        
        frame.scanForTabWidth(p) #GS I believe this should also get into the select1 hook
        
        if self.stayInTree:
            c.treeWantsFocus()
        else:
            c.bodyWantsFocus()
        #@nonl
        #@-node:ekr.20040803072955.133:<< set the current node >>
        #@nl
        
        g.doHook("select2",c=c,new_p=p,old_p=old_p,new_v=p,old_v=old_p)
        g.doHook("select3",c=c,new_p=p,old_p=old_p,new_v=p,old_v=old_p)
        
        return 'break' # Supresses unwanted selection.
    #@nonl
    #@-node:ekr.20040803072955.128:tree.select
    #@+node:ekr.20040803072955.134:tree.set...LabelState
    #@+node:ekr.20040803072955.135:setEditLabelState
    def setEditLabelState (self,p): # selected, editing
    
        c = self.c ; w = p.edit_widget()
    
        if p and w:
            c.widgetWantsFocusNow(w)
            self.setEditHeadlineColors(p)
            w.tag_remove("sel","1.0","end")
            w.tag_add("sel","1.0","end")
        else:
            g.trace('no edit_widget')
            
    setNormalLabelState = setEditLabelState # For compatibility.
    #@nonl
    #@-node:ekr.20040803072955.135:setEditLabelState
    #@+node:ekr.20040803072955.136:setSelectedLabelState
    def setSelectedLabelState (self,p): # selected, disabled
    
        # g.trace(p.headString(),g.callers())
    
        if p and p.edit_widget():
            self.setDisabledHeadlineColors(p)
    #@nonl
    #@-node:ekr.20040803072955.136:setSelectedLabelState
    #@+node:ekr.20040803072955.138:setUnselectedLabelState
    def setUnselectedLabelState (self,p): # not selected.
    
        if p and p.edit_widget():
            self.setUnselectedHeadlineColors(p)
    #@nonl
    #@-node:ekr.20040803072955.138:setUnselectedLabelState
    #@+node:ekr.20040803072955.139:setDisabledHeadlineColors
    def setDisabledHeadlineColors (self,p):
    
        c = self.c ; w = p.edit_widget()
    
        if self.trace and self.verbose:
            if not self.redrawing:
                g.trace("%10s %d %s" % ("disabled",id(w),p.headString()))
                # import traceback ; traceback.print_stack(limit=6)
    
        fg = c.config.getColor("headline_text_selected_foreground_color") or 'black'
        bg = c.config.getColor("headline_text_selected_background_color") or 'grey80'
        
        selfg = c.config.getColor("headline_text_editing_selection_foreground_color")
        selbg = c.config.getColor("headline_text_editing_selection_background_color")
    
        try:
            w.configure(state="disabled",highlightthickness=0,fg=fg,bg=bg,
                selectbackground=bg,selectforeground=fg,highlightbackground=bg)
        except:
            g.es_exception()
    #@nonl
    #@-node:ekr.20040803072955.139:setDisabledHeadlineColors
    #@+node:ekr.20040803072955.140:setEditHeadlineColors
    def setEditHeadlineColors (self,p):
    
        c = self.c ; w = p.edit_widget()
        
        if self.trace and self.verbose:
            if not self.redrawing:
                print "%10s %d %s" % ("edit",id(2),p.headString())
        
        fg    = c.config.getColor("headline_text_editing_foreground_color") or 'black'
        bg    = c.config.getColor("headline_text_editing_background_color") or 'white'
        selfg = c.config.getColor("headline_text_editing_selection_foreground_color") or 'white'
        selbg = c.config.getColor("headline_text_editing_selection_background_color") or 'black'
        
        try: # Use system defaults for selection foreground/background
            w.configure(state="normal",highlightthickness=1,
            fg=fg,bg=bg,selectforeground=selfg,selectbackground=selbg)
        except:
            g.es_exception()
    #@nonl
    #@-node:ekr.20040803072955.140:setEditHeadlineColors
    #@+node:ekr.20040803072955.141:setUnselectedHeadlineColors
    def setUnselectedHeadlineColors (self,p):
        
        c = self.c ; w = p.edit_widget()
        
        if self.trace and self.verbose:
            if not self.redrawing:
                print "%10s %d %s" % ("unselect",id(w),p.headString())
                # import traceback ; traceback.print_stack(limit=6)
        
        fg = c.config.getColor("headline_text_unselected_foreground_color") or 'black'
        bg = c.config.getColor("headline_text_unselected_background_color") or 'white'
        
        try:
            w.configure(state="disabled",highlightthickness=0,fg=fg,bg=bg,
                selectbackground=bg,selectforeground=fg,highlightbackground=bg)
        except:
            g.es_exception()
    #@nonl
    #@-node:ekr.20040803072955.141:setUnselectedHeadlineColors
    #@-node:ekr.20040803072955.134:tree.set...LabelState
    #@+node:ekr.20060207101443:tree.setHeadline (new in 4.4b2)
    def setHeadline (self,p,s):
        
        '''Set the actual text of the headline widget.
        
        This is called from the undo/redo logic to change the text before redrawing.'''
        
        w = self.edit_widget(p)
        if w:
            w.configure(state='normal')
            w.delete('1.0','end')
            if s.endswith('\n') or s.endswith('\r'):
                s = s[:-1]
            w.insert('1.0',s)
            self.revertHeadline = s
            # g.trace(repr(s),w.get('1.0','end'))
        else:
            g.trace('-'*20,'oops')
    #@nonl
    #@-node:ekr.20060207101443:tree.setHeadline (new in 4.4b2)
    #@-node:ekr.20040803072955.125:Selecting & editing... (tkTree)
    #@-others
#@nonl
#@-node:ekr.20040803072955:@thin leoTkinterTree.py
#@-leo
