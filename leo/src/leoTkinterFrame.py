# -*- coding: utf-8 -*-
#@+leo-ver=4-thin
#@+node:ekr.20031218072017.3939:@thin leoTkinterFrame.py
#@@first

# To do: Use config params for window height, width and bar color, relief and width.

#@@language python
#@@tabwidth -4

import leoGlobals as g

import leoColor,leoFrame,leoNodes
import leoTkinterMenu
import leoTkinterTree
import Tkinter as Tk
import tkFont

import os
import string
import sys

#@+others
#@+node:ekr.20031218072017.3940:class leoTkinterFrame
class leoTkinterFrame (leoFrame.leoFrame):
    
    """A class that represents a Leo window."""

    #@    @+others
    #@+node:ekr.20031218072017.3941: frame.Birth & Death
    #@+node:ekr.20031218072017.1801:f.__init__
    def __init__(self,title):
    
        # Init the base class.
        leoFrame.leoFrame.__init__(self)
    
        self.title = title
        leoTkinterFrame.instances += 1
        self.c = None # Set in finishCreate.
    
        #@    << set the leoTkinterFrame ivars >>
        #@+node:ekr.20031218072017.1802:<< set the leoTkinterFrame ivars >>
        # Created in createLeoFrame and its allies.
        self.top = None
        self.tree = None
        self.f1 = self.f2 = None
        self.log = None  ; self.logBar = None
        self.body = None ; self.bodyCtrl = None ; self.bodyBar = None ; self.bodyXBar = None
        self.canvas = None ; self.treeBar = None
        self.splitter1 = self.splitter2 = None
        self.icon = None
        self.outerFrame = None # 5/20/02
        self.iconFrame = None # 5/20/02
        self.statusFrame = None # 5/20/02
        self.statusText = None # 5/20/02
        self.statusLabel = None # 5/20/02
        
        # Used by event handlers...
        self.redrawCount = 0
        self.draggedItem = None
        self.controlKeyIsDown = False # For control-drags
        self.revertHeadline = None # Previous headline text for abortEditLabel.
        #@nonl
        #@-node:ekr.20031218072017.1802:<< set the leoTkinterFrame ivars >>
        #@nl
    #@-node:ekr.20031218072017.1801:f.__init__
    #@+node:ekr.20031218072017.3942:f.__repr__
    def __repr__ (self):
    
        return "<leoTkinterFrame: %s>" % self.title
    #@-node:ekr.20031218072017.3942:f.__repr__
    #@+node:ekr.20031218072017.3943:Creating the frame
    #@+node:ekr.20031218072017.3944:f.createCanvas
    def createCanvas (self,parentFrame):
        
        frame = self ; config = g.app.config
        
        scrolls = config.getBoolWindowPref('outline_pane_scrolls_horizontally')
        scrolls = g.choose(scrolls,1,0)
    
        canvas = Tk.Canvas(parentFrame,name="canvas",
            bd=0,bg="white",relief="flat")
    
        frame.treeBar = treeBar = Tk.Scrollbar(parentFrame,name="treeBar")
        
        # Bind mouse wheel event to canvas
        if sys.platform != "win32": # Works on 98, crashes on XP.
            canvas.bind("<MouseWheel>", self.OnMouseWheel)
            
        canvas['yscrollcommand'] = self.setCallback
        treeBar['command']     = self.yviewCallback
        
        treeBar.pack(side="right", fill="y")
        if scrolls: 
            treeXBar = Tk.Scrollbar( 
                parentFrame,name='treeXBar',orient="horizontal") 
            canvas['xscrollcommand'] = treeXBar.set 
            treeXBar['command'] = canvas.xview 
            treeXBar.pack(side="bottom", fill="x")
        
        canvas.pack(expand=1,fill="both")
    
        canvas.bind("<Button-1>", frame.OnActivateTree)
    
        # Handle mouse wheel in the outline pane.
        if sys.platform == "linux2": # This crashes tcl83.dll
            canvas.bind("<MouseWheel>", frame.OnMouseWheel)
        if 1:
            #@        << do scrolling by hand in a separate thread >>
            #@+node:ekr.20040709081208:<< do scrolling by hand in a separate thread >>
            import threading
            import time
            
            way = 'Down' # global.
            ev = threading.Event()
            
            def run(ev = ev):
                global way
                while 1:
                    ev.wait()
                    if way=='Down': canvas.yview("scroll", 1,"units")
                    else:           canvas.yview("scroll",-1,"units")
                    time.sleep(.1)
            
            t = threading.Thread(target = run)
            t.setDaemon(True)
            t.start()
                
            def exe(event,ev=ev,theWay='Down',canvas=canvas):
                global way
                if event.widget!=canvas: return
                if canvas.find_overlapping(event.x,event.y,event.x,event.y): return
                ev.set()
                way = theWay
                    
            def off(event,ev=ev,canvas=canvas):
                if event.widget!=canvas: return
                ev.clear()
            
            if 1: # Use shift-click
                canvas.bind_all('<Shift Button-3>',exe)
                canvas.bind_all('<Shift Button-1>',lambda event,way='Up': exe(event,theWay=way))
                canvas.bind_all('<Shift ButtonRelease-1>', off)
                canvas.bind_all('<Shift ButtonRelease-3>', off)
            else: # Use plain click.
                canvas.bind_all( '<Button-3>', exe)
                canvas.bind_all( '<Button-1>', lambda event,way='Up': exe(event,theWay=way))
                canvas.bind_all( '<ButtonRelease-1>', off)
                canvas.bind_all( '<ButtonRelease-3>', off)
            #@nonl
            #@-node:ekr.20040709081208:<< do scrolling by hand in a separate thread >>
            #@nl
        
        # g.print_bindings("canvas",canvas)
        return canvas
    #@nonl
    #@-node:ekr.20031218072017.3944:f.createCanvas
    #@+node:ekr.20031218072017.2176:f.finishCreate
    def finishCreate (self,c):
        
        frame = self ; frame.c = c ; gui = g.app.gui
    
        #@    << create the toplevel frame >>
        #@+node:ekr.20031218072017.2177:<< create the toplevel frame >>
        frame.top = top = Tk.Toplevel()
        gui.attachLeoIcon(top)
        top.title(frame.title)
        top.minsize(30,10) # In grid units.
        
        frame.top.protocol("WM_DELETE_WINDOW", frame.OnCloseLeoEvent)
        frame.top.bind("<Button-1>", frame.OnActivateLeoEvent)
        
        frame.top.bind("<Activate>", frame.OnActivateLeoEvent) # Doesn't work on windows.
        frame.top.bind("<Deactivate>", frame.OnDeactivateLeoEvent) # Doesn't work on windows.
        
        frame.top.bind("<Control-KeyPress>",frame.OnControlKeyDown)
        frame.top.bind("<Control-KeyRelease>",frame.OnControlKeyUp)
        #@nonl
        #@-node:ekr.20031218072017.2177:<< create the toplevel frame >>
        #@nl
        #@    << create all the subframes >>
        #@+node:ekr.20031218072017.2178:<< create all the subframes >>
        # Create the outer frame.
        self.outerFrame = outerFrame = Tk.Frame(top)
        self.outerFrame.pack(expand=1,fill="both")
        
        self.createIconBar()
        #@<< create both splitters >>
        #@+node:ekr.20031218072017.2179:<< create both splitters >>
        # Splitter 1 is the main splitter containing splitter2 and the body pane.
        f1,bar1,split1Pane1,split1Pane2 = self.createLeoSplitter(outerFrame, self.splitVerticalFlag)
        self.f1,self.bar1 = f1,bar1
        self.split1Pane1,self.split1Pane2 = split1Pane1,split1Pane2
        
        # Splitter 2 is the secondary splitter containing the tree and log panes.
        f2,bar2,split2Pane1,split2Pane2 = self.createLeoSplitter(split1Pane1, not self.splitVerticalFlag)
        self.f2,self.bar2 = f2,bar2
        self.split2Pane1,self.split2Pane2 = split2Pane1,split2Pane2
        #@nonl
        #@-node:ekr.20031218072017.2179:<< create both splitters >>
        #@nl
        
        # Create the canvas, tree, log and body.
        frame.canvas   = self.createCanvas(self.split2Pane1)
        frame.tree     = leoTkinterTree.leoTkinterTree(c,frame,frame.canvas)
        frame.log      = leoTkinterLog(frame,self.split2Pane2)
        frame.body     = leoTkinterBody(frame,self.split1Pane2)
        
        # Yes, this an "official" ivar: this is a kludge.
        frame.bodyCtrl = frame.body.bodyCtrl
        
        # Configure.  N.B. There may be Tk bugs here that make the order significant!
        frame.setTabWidth(c.tab_width)
        frame.tree.setTreeColorsFromConfig()
        self.reconfigurePanes()
        self.body.setFontFromConfig()
        
        if 0: # No longer done automatically.
        
            # Create the status line.
            self.createStatusLine()
            self.putStatusLine("Welcome to Leo")
        #@nonl
        #@-node:ekr.20031218072017.2178:<< create all the subframes >>
        #@nl
        #@    << create the first tree node >>
        #@+node:ekr.20031218072017.2180:<< create the first tree node >>
        t = leoNodes.tnode()
        v = leoNodes.vnode(c,t)
        p = leoNodes.position(v,[])
        v.initHeadString("NewHeadline")
        
        p.moveToRoot()
        c.beginUpdate()
        c.selectVnode(p)
        c.redraw()
        c.frame.getFocus()
        c.editPosition(p)
        c.endUpdate(False)
        #@-node:ekr.20031218072017.2180:<< create the first tree node >>
        #@nl
    
        self.menu = leoTkinterMenu.leoTkinterMenu(frame)
    
        v = c.currentVnode()
    
        if not g.doHook("menu1",c=c,v=v):
            frame.menu.createMenuBar(self)
    
        g.app.setLog(frame.log,"tkinterFrame.__init__") # the leoTkinterFrame containing the log
    
        g.app.windowList.append(frame)
        
        c.initVersion()
        c.signOnWithVersion()
        
        self.body.createBindings(frame)
    #@nonl
    #@-node:ekr.20031218072017.2176:f.finishCreate
    #@+node:ekr.20031218072017.3945:Creating the splitter
    #@+at 
    #@nonl
    # The key invariants used throughout this code:
    # 
    # 1. self.splitVerticalFlag tells the alignment of the main splitter and
    # 2. not self.splitVerticalFlag tells the alignment of the secondary 
    # splitter.
    # 
    # Only the general-purpose divideAnySplitter routine doesn't know about 
    # these invariants.  So most of this code is specialized for Leo's 
    # window.  OTOH, creating a single splitter window would be much easier 
    # than this code.
    #@-at
    #@+node:ekr.20031218072017.3946:resizePanesToRatio
    def resizePanesToRatio(self,ratio,secondary_ratio):
    
        self.divideLeoSplitter(self.splitVerticalFlag, ratio)
        self.divideLeoSplitter(not self.splitVerticalFlag, secondary_ratio)
        # g.trace(ratio)
    #@-node:ekr.20031218072017.3946:resizePanesToRatio
    #@+node:ekr.20031218072017.3947:bindBar
    def bindBar (self, bar, verticalFlag):
        
        if verticalFlag == self.splitVerticalFlag:
            bar.bind("<B1-Motion>", self.onDragMainSplitBar)
    
        else:
            bar.bind("<B1-Motion>", self.onDragSecondarySplitBar)
    #@-node:ekr.20031218072017.3947:bindBar
    #@+node:ekr.20031218072017.3948:createLeoSplitter
    # 5/20/03: Removed the ancient kludge for forcing the height & width of f.
    # The code in leoFileCommands.getGlobals now works!
    
    def createLeoSplitter (self, parent, verticalFlag):
        
        """Create a splitter window and panes into which the caller packs widgets.
        
        Returns (f, bar, pane1, pane2) """
        
        # Create the frames.
        f = Tk.Frame(parent,bd=0,relief="flat")
        f.pack(expand=1,fill="both",pady=1)
        pane1 = Tk.Frame(f)
        pane2 = Tk.Frame(f)
        bar =   Tk.Frame(f,bd=2,relief="raised",bg="LightSteelBlue2")
    
        # Configure and place the frames.
        self.configureBar(bar,verticalFlag)
        self.bindBar(bar,verticalFlag)
        self.placeSplitter(bar,pane1,pane2,verticalFlag)
    
        return f, bar, pane1, pane2
    #@nonl
    #@-node:ekr.20031218072017.3948:createLeoSplitter
    #@+node:ekr.20031218072017.3949:divideAnySplitter
    # This is the general-purpose placer for splitters.
    # It is the only general-purpose splitter code in Leo.
    
    def divideAnySplitter (self, frac, verticalFlag, bar, pane1, pane2):
    
        if verticalFlag:
            # Panes arranged vertically; horizontal splitter bar
            bar.place(rely=frac)
            pane1.place(relheight=frac)
            pane2.place(relheight=1-frac)
        else:
            # Panes arranged horizontally; vertical splitter bar
            bar.place(relx=frac)
            pane1.place(relwidth=frac)
            pane2.place(relwidth=1-frac)
    #@nonl
    #@-node:ekr.20031218072017.3949:divideAnySplitter
    #@+node:ekr.20031218072017.3950:divideLeoSplitter
    # Divides the main or secondary splitter, using the key invariant.
    def divideLeoSplitter (self, verticalFlag, frac):
        if self.splitVerticalFlag == verticalFlag:
            self.divideLeoSplitter1(frac,verticalFlag)
            self.ratio = frac # Ratio of body pane to tree pane.
        else:
            self.divideLeoSplitter2(frac,verticalFlag)
            self.secondary_ratio = frac # Ratio of tree pane to log pane.
    
    # Divides the main splitter.
    def divideLeoSplitter1 (self, frac, verticalFlag): 
        self.divideAnySplitter(frac, verticalFlag,
            self.bar1, self.split1Pane1, self.split1Pane2)
    
    # Divides the secondary splitter.
    def divideLeoSplitter2 (self, frac, verticalFlag): 
        self.divideAnySplitter (frac, verticalFlag,
            self.bar2, self.split2Pane1, self.split2Pane2)
    #@nonl
    #@-node:ekr.20031218072017.3950:divideLeoSplitter
    #@+node:ekr.20031218072017.3951:onDrag...
    def onDragMainSplitBar (self, event):
        self.onDragSplitterBar(event,self.splitVerticalFlag)
    
    def onDragSecondarySplitBar (self, event):
        self.onDragSplitterBar(event,not self.splitVerticalFlag)
    
    def onDragSplitterBar (self, event, verticalFlag):
    
        # x and y are the coordinates of the cursor relative to the bar, not the main window.
        bar = event.widget
        x = event.x
        y = event.y
        top = bar.winfo_toplevel()
    
        if verticalFlag:
            # Panes arranged vertically; horizontal splitter bar
            wRoot	= top.winfo_rooty()
            barRoot = bar.winfo_rooty()
            wMax	= top.winfo_height()
            offset = float(barRoot) + y - wRoot
        else:
            # Panes arranged horizontally; vertical splitter bar
            wRoot	= top.winfo_rootx()
            barRoot = bar.winfo_rootx()
            wMax	= top.winfo_width()
            offset = float(barRoot) + x - wRoot
    
        # Adjust the pixels, not the frac.
        if offset < 3: offset = 3
        if offset > wMax - 2: offset = wMax - 2
        # Redraw the splitter as the drag is occuring.
        frac = float(offset) / wMax
        # g.trace(frac)
        self.divideLeoSplitter(verticalFlag, frac)
    #@nonl
    #@-node:ekr.20031218072017.3951:onDrag...
    #@+node:ekr.20031218072017.3952:placeSplitter
    def placeSplitter (self,bar,pane1,pane2,verticalFlag):
    
        if verticalFlag:
            # Panes arranged vertically; horizontal splitter bar
            pane1.place(relx=0.5, rely =   0, anchor="n", relwidth=1.0, relheight=0.5)
            pane2.place(relx=0.5, rely = 1.0, anchor="s", relwidth=1.0, relheight=0.5)
            bar.place  (relx=0.5, rely = 0.5, anchor="c", relwidth=1.0)
        else:
            # Panes arranged horizontally; vertical splitter bar
            # adj gives tree pane more room when tiling vertically.
            adj = g.choose(verticalFlag != self.splitVerticalFlag,0.65,0.5)
            pane1.place(rely=0.5, relx =   0, anchor="w", relheight=1.0, relwidth=adj)
            pane2.place(rely=0.5, relx = 1.0, anchor="e", relheight=1.0, relwidth=1.0-adj)
            bar.place  (rely=0.5, relx = adj, anchor="c", relheight=1.0)
    #@nonl
    #@-node:ekr.20031218072017.3952:placeSplitter
    #@-node:ekr.20031218072017.3945:Creating the splitter
    #@+node:ekr.20031218072017.3953:Creating the icon area
    #@+node:ekr.20031218072017.3954:createIconBar
    def createIconBar (self):
        
        """Create an empty icon bar in the packer's present position"""
    
        if not self.iconFrame:
            self.iconFrame = Tk.Frame(self.outerFrame,height="5m",bd=2,relief="groove")
            self.iconFrame.pack(fill="x",pady=2)
    #@nonl
    #@-node:ekr.20031218072017.3954:createIconBar
    #@+node:ekr.20031218072017.3955:hideIconBar
    def hideIconBar (self):
        
        """Hide the icon bar by unpacking it.
        
        A later call to showIconBar will repack it in a new location."""
        
        if self.iconFrame:
            self.iconFrame.pack_forget()
    #@-node:ekr.20031218072017.3955:hideIconBar
    #@+node:ekr.20031218072017.3956:clearIconBar
    def clearIconBar(self):
        
        """Destroy all the widgets in the icon bar"""
        
        f = self.iconFrame
        if not f: return
        
        for slave in f.pack_slaves():
            slave.destroy()
    
        f.configure(height="5m") # The default height.
        g.app.iconWidgetCount = 0
        g.app.iconImageRefs = []
    #@-node:ekr.20031218072017.3956:clearIconBar
    #@+node:ekr.20031218072017.3957:showIconBar
    def showIconBar(self):
        
        """Show the icon bar by repacking it"""
    
        self.iconFrame.pack(fill="x",pady=2)
    #@nonl
    #@-node:ekr.20031218072017.3957:showIconBar
    #@+node:ekr.20031218072017.3958:addIconButton
    def addIconButton(self,text=None,imagefile=None,image=None,command=None,bg=None):
        
        """Add a button containing text or a picture to the icon bar.
        
        Pictures take precedence over text"""
        
        f = self.iconFrame
        if not imagefile and not image and not text: return
    
        # First define n.	
        try:
            g.app.iconWidgetCount += 1
            n = g.app.iconWidgetCount
        except:
            n = g.app.iconWidgetCount = 1
    
        if not command:
            def command(n=n):
                print "command for widget %s" % (n)
    
        if imagefile or image:
            #@        << create a picture >>
            #@+node:ekr.20031218072017.3959:<< create a picture >>
            try:
                if imagefile:
                    # Create the image.  Throws an exception if file not found
                    imagefile = g.os_path_join(g.app.loadDir,imagefile)
                    imagefile = g.os_path_normpath(imagefile)
                    image = Tk.PhotoImage(master=g.app.root,file=imagefile)
                    
                    # Must keep a reference to the image!
                    try:
                        refs = g.app.iconImageRefs
                    except:
                        refs = g.app.iconImageRefs = []
                
                    refs.append((imagefile,image),)
                
                if not bg:
                    bg = f.cget("bg")
            
                b = Tk.Button(f,image=image,relief="flat",bd=0,command=command,bg=bg)
                b.pack(side="left",fill="y")
                return b
                
            except:
                g.es_exception()
                return None
            #@nonl
            #@-node:ekr.20031218072017.3959:<< create a picture >>
            #@nl
        elif text:
            w = min(6,len(text))
            b = Tk.Button(f,text=text,width=w,relief="groove",bd=2,command=command)
            b.pack(side="left", fill="y")
            return b
            
        return None
    #@nonl
    #@-node:ekr.20031218072017.3958:addIconButton
    #@-node:ekr.20031218072017.3953:Creating the icon area
    #@+node:ekr.20031218072017.3960:Creating the status area
    
    
    #@+node:ekr.20031218072017.3961:createStatusLine
    def createStatusLine (self):
        
        if self.statusFrame and self.statusLabel:
            return
        
        self.statusFrame = statusFrame = Tk.Frame(self.outerFrame,bd=2)
        statusFrame.pack(fill="x",pady=1)
        
        text = "line 0, col 0"
        width = len(text) + 4
        self.statusLabel = Tk.Label(statusFrame,text=text,width=width,anchor="w")
        self.statusLabel.pack(side="left",padx=1)
        
        bg = statusFrame.cget("background")
        self.statusText = Tk.Text(statusFrame,height=1,state="disabled",bg=bg,relief="groove")
        self.statusText.pack(side="left",expand=1,fill="x")
    
        # Register an idle-time handler to update the row and column indicators.
        self.statusFrame.after_idle(self.updateStatusRowCol)
    #@nonl
    #@-node:ekr.20031218072017.3961:createStatusLine
    #@+node:ekr.20031218072017.3962:clearStatusLine
    def clearStatusLine (self):
        
        t = self.statusText
        if not t: return
        
        t.configure(state="normal")
        t.delete("1.0","end")
        t.configure(state="disabled")
    #@nonl
    #@-node:ekr.20031218072017.3962:clearStatusLine
    #@+node:EKR.20040424153344:enable/disableStatusLine & isEnabled
    def disableStatusLine (self):
        
        t = self.statusText
        if t:
            t.configure(state="disabled",background="gray")
        
    def enableStatusLine (self):
        
        t = self.statusText
        if t:
            t.configure(state="normal",background="pink")
            t.focus_set()
            
    def statusLineIsEnabled(self):
        t = self.statusText
        if t:
            state = t.cget("state")
            return state == "normal"
        else:
            return False
    #@nonl
    #@-node:EKR.20040424153344:enable/disableStatusLine & isEnabled
    #@+node:ekr.20031218072017.3963:putStatusLine
    def putStatusLine (self,s,color=None):
        
        t = self.statusText ; tags = self.statusColorTags
        if not t: return
    
        t.configure(state="normal")
        
        if "black" not in self.log.colorTags:
            tags.append("black")
            
        if color and color not in tags:
            tags.append(color)
            t.tag_config(color,foreground=color)
    
        if color:
            t.insert("end",s)
            t.tag_add(color,"end-%dc" % (len(s)+1),"end-1c")
            t.tag_config("black",foreground="black")
            t.tag_add("black","end")
        else:
            t.insert("end",s)
        
        t.configure(state="disabled")
    #@nonl
    #@-node:ekr.20031218072017.3963:putStatusLine
    #@+node:EKR.20040424154804:setFocusStatusLine
    def setFocusStatusLine (self):
        
        t = self.statusText
        if t:
            t.focus_set()
    #@nonl
    #@-node:EKR.20040424154804:setFocusStatusLine
    #@+node:ekr.20031218072017.1733:updateStatusRowCol
    def updateStatusRowCol (self):
        
        c = self.c ; body = self.bodyCtrl ; lab = self.statusLabel
        gui = g.app.gui
        if not lab: return
        
        # New for Python 2.3: may be called during shutdown.
        if g.app.killed:
            return
    
        if 0: # New code
            index = c.frame.body.getInsertionPoint()
            row,col = c.frame.body.indexToRowColumn(index)
            index1 = c.frame.body.rowColumnToIndex(row,0)
        else:
            index = body.index("insert")
            row,col = gui.getindex(body,index)
        
        if col > 0:
            if 0: # new code
                s = c.frame.body.getRange(index1,index2)
            else:
                s = body.get("%d.0" % (row),index)
            s = g.toUnicode(s,g.app.tkEncoding) # 9/28/03
            col = g.computeWidth (s,self.tab_width)
    
        if row != self.lastStatusRow or col != self.lastStatusCol:
            s = "line %d, col %d " % (row,col)
            lab.configure(text=s)
            self.lastStatusRow = row
            self.lastStatusCol = col
            
        # Reschedule this routine 100 ms. later.
        # Don't use after_idle: it hangs Leo.
        self.statusFrame.after(100,self.updateStatusRowCol)
    #@nonl
    #@-node:ekr.20031218072017.1733:updateStatusRowCol
    #@-node:ekr.20031218072017.3960:Creating the status area
    #@-node:ekr.20031218072017.3943:Creating the frame
    #@+node:ekr.20031218072017.3964:Destroying the frame
    #@+node:ekr.20031218072017.1975:destroyAllObjects
    def destroyAllObjects (self):
    
        """Clear all links to objects in a Leo window."""
    
        frame = self ; c = self.c ; tree = frame.tree ; body = self.body
    
        # Do this first.
        #@    << clear all vnodes and tnodes in the tree >>
        #@+node:ekr.20031218072017.1976:<< clear all vnodes and tnodes in the tree>>
        # Using a dict here is essential for adequate speed.
        vList = [] ; tDict = {}
        
        for p in c.allNodes_iter():
            vList.append(p.v)
            if p.v.t:
                key = id(p.v.t)
                if not tDict.has_key(key):
                    tDict[key] = p.v.t
        
        for key in tDict.keys():
            g.clearAllIvars(tDict[key])
        
        for v in vList:
            g.clearAllIvars(v)
        
        vList = [] ; tDict = {} # Remove these references immediately.
        #@nonl
        #@-node:ekr.20031218072017.1976:<< clear all vnodes and tnodes in the tree>>
        #@nl
    
        # Destroy all ivars in subclasses.
        g.clearAllIvars(c.atFileCommands)
        g.clearAllIvars(c.fileCommands)
        g.clearAllIvars(c.importCommands)
        g.clearAllIvars(c.tangleCommands)
        g.clearAllIvars(c.undoer)
        g.clearAllIvars(c)
        g.clearAllIvars(body.colorizer)
        g.clearAllIvars(body)
        g.clearAllIvars(tree)
    
        # This must be done last.
        frame.destroyAllPanels()
        g.clearAllIvars(frame)
    #@nonl
    #@-node:ekr.20031218072017.1975:destroyAllObjects
    #@+node:ekr.20031218072017.3965:destroyAllPanels
    def destroyAllPanels (self):
        
        """Destroy all panels attached to this frame."""
        
        panels = (self.comparePanel, self.colorPanel, self.fontPanel, self.prefsPanel)
    
        for panel in panels:
            if panel:
                panel.top.destroy()
                
        self.comparePanel = None
        self.colorPanel = None
        self.fontPanel = None
        self.prefsPanel = None
    #@nonl
    #@-node:ekr.20031218072017.3965:destroyAllPanels
    #@+node:ekr.20031218072017.1974:destroySelf
    def destroySelf (self):
        
        top = self.top # Remember this: we are about to destroy all of our ivars!
    
        if g.app.windowList:
            self.destroyAllObjects()
    
        top.destroy()
    #@nonl
    #@-node:ekr.20031218072017.1974:destroySelf
    #@-node:ekr.20031218072017.3964:Destroying the frame
    #@-node:ekr.20031218072017.3941: frame.Birth & Death
    #@+node:ekr.20031218072017.3966:bringToFront
    def bringToFront (self):
        
        """Bring the tkinter Prefs Panel to the front."""
    
        self.top.deiconify()
        self.top.lift()
    #@nonl
    #@-node:ekr.20031218072017.3966:bringToFront
    #@+node:ekr.20031218072017.3967:Configuration
    #@+node:ekr.20031218072017.3968:configureBar
    def configureBar (self, bar, verticalFlag):
        
        config = g.app.config
    
        # Get configuration settings.
        w = config.getWindowPref("split_bar_width")
        if not w or w < 1: w = 7
        relief = config.getWindowPref("split_bar_relief")
        if not relief: relief = "flat"
        color = config.getWindowPref("split_bar_color")
        if not color: color = "LightSteelBlue2"
    
        try:
            if verticalFlag:
                # Panes arranged vertically; horizontal splitter bar
                bar.configure(relief=relief,height=w,bg=color,cursor="sb_v_double_arrow")
            else:
                # Panes arranged horizontally; vertical splitter bar
                bar.configure(relief=relief,width=w,bg=color,cursor="sb_h_double_arrow")
        except: # Could be a user error. Use all defaults
            g.es("exception in user configuration for splitbar")
            g.es_exception()
            if verticalFlag:
                # Panes arranged vertically; horizontal splitter bar
                bar.configure(height=7,cursor="sb_v_double_arrow")
            else:
                # Panes arranged horizontally; vertical splitter bar
                bar.configure(width=7,cursor="sb_h_double_arrow")
    #@nonl
    #@-node:ekr.20031218072017.3968:configureBar
    #@+node:ekr.20031218072017.3969:configureBarsFromConfig
    def configureBarsFromConfig (self):
        
        config = g.app.config
    
        w = config.getWindowPref("split_bar_width")
        if not w or w < 1: w = 7
        
        relief = config.getWindowPref("split_bar_relief")
        if not relief or relief == "": relief = "flat"
    
        color = config.getWindowPref("split_bar_color")
        if not color or color == "": color = "LightSteelBlue2"
    
        if self.splitVerticalFlag:
            bar1,bar2=self.bar1,self.bar2
        else:
            bar1,bar2=self.bar2,self.bar1
            
        try:
            bar1.configure(relief=relief,height=w,bg=color)
            bar2.configure(relief=relief,width=w,bg=color)
        except: # Could be a user error.
            g.es("exception in user configuration for splitbar")
            g.es_exception()
    #@nonl
    #@-node:ekr.20031218072017.3969:configureBarsFromConfig
    #@+node:ekr.20031218072017.2246:reconfigureFromConfig
    def reconfigureFromConfig (self):
        
        frame = self ; c = frame.c
        
        # Not ready yet: just reset the width and color.
        # We need self.bar1 and self.bar2 ivars.
        # self.reconfigureBar(...)
        
        # The calls to redraw are workarounds for an apparent Tk bug.
        # Without them the text settings get applied to the wrong widget!
        # Moreover, only this order seems to work on Windows XP...
        frame.tree.setFontFromConfig()
        frame.tree.setTreeColorsFromConfig()
        frame.configureBarsFromConfig()
        c.redraw()
        frame.body.setFontFromConfig()
        frame.setTabWidth(c.tab_width) # 12/2/03
        c.redraw()
        frame.log.setFontFromConfig()
        c.redraw()
    #@-node:ekr.20031218072017.2246:reconfigureFromConfig
    #@+node:ekr.20031218072017.1625:setInitialWindowGeometry
    def setInitialWindowGeometry(self):
        
        """Set the position and size of the frame to config params."""
        
        config = g.app.config
    
        h = config.getIntWindowPref("initial_window_height")
        w = config.getIntWindowPref("initial_window_width")
        x = config.getIntWindowPref("initial_window_left")
        y = config.getIntWindowPref("initial_window_top")
        
        if h and w and x and y:
            self.setTopGeometry(w,h,x,y)
    #@nonl
    #@-node:ekr.20031218072017.1625:setInitialWindowGeometry
    #@+node:ekr.20031218072017.722:setTabWidth
    def setTabWidth (self, w):
        
        try: # This can fail when called from scripts
            # Use the present font for computations.
            font = self.bodyCtrl.cget("font")
            root = g.app.root # 4/3/03: must specify root so idle window will work properly.
            font = tkFont.Font(root=root,font=font)
            tabw = font.measure(" " * abs(w)) # 7/2/02
            self.bodyCtrl.configure(tabs=tabw)
            self.tab_width = w
            # g.trace(w,tabw)
        except:
            g.es_exception()
            pass
    #@-node:ekr.20031218072017.722:setTabWidth
    #@+node:ekr.20031218072017.1540:setWrap
    def setWrap (self,p):
        
        c = self.c
        dict = g.scanDirectives(c,p)
        if dict != None:
            # 8/30/03: Add scroll bars if we aren't wrapping.
            wrap = dict.get("wrap")
            if wrap:
                self.bodyCtrl.configure(wrap="word")
                self.bodyXBar.pack_forget()
            else:
                self.bodyCtrl.configure(wrap="none")
                self.bodyXBar.pack(side="bottom",fill="x")
    #@-node:ekr.20031218072017.1540:setWrap
    #@+node:ekr.20031218072017.2307:setTopGeometry
    def setTopGeometry(self,w,h,x,y,adjustSize=True):
        
        # Put the top-left corner on the screen.
        x = max(10,x) ; y = max(10,y)
        
        if adjustSize:
            top = self.top
            sw = top.winfo_screenwidth()
            sh = top.winfo_screenheight()
    
            # Adjust the size so the whole window fits on the screen.
            w = min(sw-10,w)
            h = min(sh-10,h)
    
            # Adjust position so the whole window fits on the screen.
            if x + w > sw: x = 10
            if y + h > sh: y = 10
        
        geom = "%dx%d%+d%+d" % (w,h,x,y)
        
        self.top.geometry(geom)
    #@nonl
    #@-node:ekr.20031218072017.2307:setTopGeometry
    #@+node:ekr.20031218072017.3970:reconfigurePanes (use config bar_width)
    def reconfigurePanes (self):
        
        border = g.app.config.getIntWindowPref('additional_body_text_border')
        if border == None: border = 0
        
        # The body pane needs a _much_ bigger border when tiling horizontally.
        border = g.choose(self.splitVerticalFlag,2+border,6+border)
        self.bodyCtrl.configure(bd=border)
        
        # The log pane needs a slightly bigger border when tiling vertically.
        border = g.choose(self.splitVerticalFlag,4,2) 
        self.log.configureBorder(border)
    #@nonl
    #@-node:ekr.20031218072017.3970:reconfigurePanes (use config bar_width)
    #@-node:ekr.20031218072017.3967:Configuration
    #@+node:ekr.20031218072017.3971:Event handlers (Frame)
    #@+node:ekr.20031218072017.3972:frame.OnCloseLeoEvent
    # Called from quit logic and when user closes the window.
    # Returns True if the close happened.
    
    def OnCloseLeoEvent(self):
    
        g.app.closeLeoWindow(self)
    #@nonl
    #@-node:ekr.20031218072017.3972:frame.OnCloseLeoEvent
    #@+node:ekr.20031218072017.3973:frame.OnControlKeyUp/Down
    def OnControlKeyDown (self,event=None):
        
        self.controlKeyIsDown = True
        
    def OnControlKeyUp (self,event=None):
    
        self.controlKeyIsDown = False
    
    #@-node:ekr.20031218072017.3973:frame.OnControlKeyUp/Down
    #@+node:ekr.20031218072017.3974:frame.OnVisibility
    # Handle the "visibility" event and attempt to attach the Leo icon.
    # This code must be executed whenever the window is redrawn.
    
    def OnVisibility (self,event):
    
        if self.icon and event.widget is self.top:
    
            # print "OnVisibility"
            self.icon.attach(self.top)
    #@nonl
    #@-node:ekr.20031218072017.3974:frame.OnVisibility
    #@+node:ekr.20031218072017.3975:OnActivateBody
    def OnActivateBody (self,event=None):
    
        try:
            frame = self ; c = frame.c ; gui = g.app.gui
            g.app.setLog(frame.log,"OnActivateBody")
            w = gui.get_focus(frame)
            if w != frame.body.bodyCtrl:
                self.tree.OnDeactivate()
                # Reference to bodyCtrl is allowable in an event handler.
                gui.set_focus(c,frame.body.bodyCtrl) 
        except:
            g.es_event_exception("activate body")
    #@nonl
    #@-node:ekr.20031218072017.3975:OnActivateBody
    #@+node:ekr.20031218072017.2253:OnActivateLeoEvent, OnDeactivateLeoEvent
    def OnActivateLeoEvent(self,event=None):
    
        try:
            g.app.setLog(self.log,"OnActivateLeoEvent")
        except:
            g.es_event_exception("activate Leo")
    
    def OnDeactivateLeoEvent(self,event=None):
        
        if 0: # This causes problems on the Mac.
            try:
                g.app.setLog(None,"OnDeactivateLeoEvent")
            except:
                g.es_event_exception("deactivate Leo")
    #@nonl
    #@-node:ekr.20031218072017.2253:OnActivateLeoEvent, OnDeactivateLeoEvent
    #@+node:ekr.20031218072017.3976:OnActivateTree
    def OnActivateTree (self,event=None):
    
        try:
            frame = self ; c = frame.c ; gui = g.app.gui
            g.app.setLog(frame.log,"OnActivateTree")
            # self.tree.undimEditLabel()
            gui.set_focus(c, frame.bodyCtrl)
        except:
            g.es_event_exception("activate tree")
    #@-node:ekr.20031218072017.3976:OnActivateTree
    #@+node:ekr.20031218072017.3977:OnBodyClick, OnBodyRClick (Events)
    def OnBodyClick (self,event=None):
    
        try:
            c = self.c ; v = c.currentVnode()
            if not g.doHook("bodyclick1",c=c,v=v,event=event):
                self.OnActivateBody(event=event)
            g.doHook("bodyclick2",c=c,v=v,event=event)
        except:
            g.es_event_exception("bodyclick")
    
    def OnBodyRClick(self,event=None):
        
        try:
            c = self.c ; v = c.currentVnode()
            if not g.doHook("bodyrclick1",c=c,v=v,event=event):
                pass # By default Leo does nothing.
            g.doHook("bodyrclick2",c=c,v=v,event=event)
        except:
            g.es_event_exception("iconrclick")
    #@nonl
    #@-node:ekr.20031218072017.3977:OnBodyClick, OnBodyRClick (Events)
    #@+node:ekr.20031218072017.3978:OnBodyDoubleClick (Events)
    def OnBodyDoubleClick (self,event=None):
    
        try:
            c = self.c ; v = c.currentVnode()
            if not g.doHook("bodydclick1",c=c,v=v,event=event):
                if event: # 8/4/02: prevent wandering insertion point.
                    index = "@%d,%d" % (event.x, event.y) # Find where we clicked
                    # 7/9/04
                    event.widget.tag_add('sel', 'insert wordstart', 'insert wordend')
                body = self.bodyCtrl
                start = body.index(index + " wordstart")
                end = body.index(index + " wordend")
                self.body.setTextSelection(start,end)
            g.doHook("bodydclick2",c=c,v=v,event=event)
        except:
            g.es_event_exception("bodydclick")
            
        return "break" # Restore this to handle proper double-click logic.
    #@nonl
    #@-node:ekr.20031218072017.3978:OnBodyDoubleClick (Events)
    #@+node:ekr.20031218072017.1803:OnMouseWheel (Tomaz Ficko)
    # Contributed by Tomaz Ficko.  This works on some systems.
    # On XP it causes a crash in tcl83.dll.  Clearly a Tk bug.
    
    def OnMouseWheel(self, event=None):
        
        g.trace()
    
        try:
            if event.delta < 1:
                self.canvas.yview(Tk.SCROLL, 1, Tk.UNITS)
            else:
                self.canvas.yview(Tk.SCROLL, -1, Tk.UNITS)
        except:
            g.es_event_exception("scroll wheel")
    
        return "break"
    #@nonl
    #@-node:ekr.20031218072017.1803:OnMouseWheel (Tomaz Ficko)
    #@-node:ekr.20031218072017.3971:Event handlers (Frame)
    #@+node:ekr.20031218072017.3979:Gui-dependent commands
    #@+node:ekr.20031218072017.3980:Edit Menu...
    #@+node:ekr.20031218072017.3981:abortEditLabelCommand
    def abortEditLabelCommand (self):
        
        frame = self ; c = frame.c ; v = c.currentVnode() ; tree = frame.tree
        
        if g.app.batchMode:
            c.notValidInBatchMode("Abort Edit Headline")
            return
    
        if self.revertHeadline and v.edit_text() and v == tree.editPosition():
        
            v.edit_text().delete("1.0","end")
            v.edit_text().insert("end",self.revertHeadline)
            tree.idle_head_key(v) # Must be done immediately.
            tree.revertHeadline = None
            tree.select(v)
            if v and len(v.t.vnodeList) > 0:
                tree.force_redraw() # force a redraw of joined headlines.
    #@nonl
    #@-node:ekr.20031218072017.3981:abortEditLabelCommand
    #@+node:ekr.20031218072017.840:Cut/Copy/Paste body text
    #@+node:ekr.20031218072017.841:frame.OnCut, OnCutFrom Menu
    def OnCut (self,event=None):
        
        """The handler for the virtual Cut event."""
    
        frame = self ; c = frame.c ; v = c.currentVnode()
        
        # This is probably being subverted by Tk.
        if g.app.gui.win32clipboard:
            data = frame.body.getSelectedText()
            if data:
                g.app.gui.replaceClipboardWith(data)
    
        # Activate the body key handler by hand.
        frame.body.forceFullRecolor()
        frame.body.onBodyWillChange(v,"Cut")
    
    def OnCutFromMenu (self):
        
        w = self.getFocus()
        w.event_generate(g.virtual_event_name("Cut"))
        
        frame = self ; c = frame.c ; v = c.currentVnode()
    
        if not frame.body.hasFocus(): # 1/30/04: Make sure the event sticks.
            frame.tree.onHeadChanged(v)
    
    
    
    
    #@-node:ekr.20031218072017.841:frame.OnCut, OnCutFrom Menu
    #@+node:ekr.20031218072017.842:frame.OnCopy, OnCopyFromMenu
    def OnCopy (self,event=None):
        
        frame = self
    
        if g.app.gui.win32clipboard:
            data = frame.body.getSelectedText()
            if data:
                g.app.gui.replaceClipboardWith(data)
            
        # Copy never changes dirty bits or syntax coloring.
        
    def OnCopyFromMenu (self):
    
        frame = self
        w = frame.getFocus()
        w.event_generate(g.virtual_event_name("Copy"))
    
    #@-node:ekr.20031218072017.842:frame.OnCopy, OnCopyFromMenu
    #@+node:ekr.20031218072017.843:frame.OnPaste & OnPasteFromMenu
    def OnPaste (self,event=None):
        
        frame = self ; c = frame.c ; v = c.currentVnode()
    
        # Activate the body key handler by hand.
        frame.body.forceFullRecolor()
        frame.body.onBodyWillChange(v,"Paste")
        
    def OnPasteFromMenu (self):
        
        frame = self ; c = frame.c ; v = c.currentVnode()
    
        w = self.getFocus()
        w.event_generate(g.virtual_event_name("Paste"))
        
        if not frame.body.hasFocus(): # 1/30/04: Make sure the event sticks.
            frame.tree.onHeadChanged(v)
    #@-node:ekr.20031218072017.843:frame.OnPaste & OnPasteFromMenu
    #@-node:ekr.20031218072017.840:Cut/Copy/Paste body text
    #@+node:ekr.20031218072017.3982:endEditLabelCommand
    def endEditLabelCommand (self):
    
        frame = self ; c = frame.c ; tree = frame.tree ; gui = g.app.gui
        
        if g.app.batchMode:
            c.notValidInBatchMode("End Edit Headline")
            return
        
        v = frame.tree.editPosition()
    
        # g.trace(v)
        if v and v.edit_text():
            tree.select(v)
        if v: # Bug fix 10/9/02: also redraw ancestor headlines.
            tree.force_redraw() # force a redraw of joined headlines.
    
        gui.set_focus(c,c.frame.bodyCtrl) # 10/14/02
    #@nonl
    #@-node:ekr.20031218072017.3982:endEditLabelCommand
    #@+node:ekr.20031218072017.3983:insertHeadlineTime
    def insertHeadlineTime (self):
    
        frame = self ; c = frame.c ; v = c.currentVnode()
        h = v.headString() # Remember the old value.
        
        if g.app.batchMode:
            c.notValidInBatchMode("Insert Headline Time")
            return
    
        if v.edit_text():
            sel1,sel2 = g.app.gui.getTextSelection(v.edit_text())
            if sel1 and sel2 and sel1 != sel2: # 7/7/03
                v.edit_text().delete(sel1,sel2)
            v.edit_text().insert("insert",c.getTime(body=False))
            frame.tree.idle_head_key(v)
    
        # A kludge to get around not knowing whether we are editing or not.
        if h.strip() == v.headString().strip():
            g.es("Edit headline to append date/time")
    #@nonl
    #@-node:ekr.20031218072017.3983:insertHeadlineTime
    #@-node:ekr.20031218072017.3980:Edit Menu...
    #@+node:ekr.20031218072017.3984:Window Menu...
    #@+node:ekr.20031218072017.3985:toggleActivePane
    def toggleActivePane(self):
        
        c = self.c ; gui = g.app.gui
        if gui.get_focus(self) == self.bodyCtrl:
            gui.set_focus(c,self.canvas)
        else:
            gui.set_focus(c,self.bodyCtrl)
    #@nonl
    #@-node:ekr.20031218072017.3985:toggleActivePane
    #@+node:ekr.20031218072017.3986:cascade
    def cascade(self):
    
        x,y,delta = 10,10,10
        for frame in g.app.windowList:
            top = frame.top
    
            # Compute w,h
            top.update_idletasks() # Required to get proper info.
            geom = top.geometry() # geom = "WidthxHeight+XOffset+YOffset"
            dim,junkx,junky = string.split(geom,'+')
            w,h = string.split(dim,'x')
            w,h = int(w),int(h)
    
            # Set new x,y and old w,h
            frame.setTopGeometry(w,h,x,y,adjustSize=False)
    
            # Compute the new offsets.
            x += 30 ; y += 30
            if x > 200:
                x = 10 + delta ; y = 40 + delta
                delta += 10
    #@-node:ekr.20031218072017.3986:cascade
    #@+node:ekr.20031218072017.3987:equalSizedPanes
    def equalSizedPanes(self):
    
        frame = self
        frame.resizePanesToRatio(0.5,frame.secondary_ratio)
    #@-node:ekr.20031218072017.3987:equalSizedPanes
    #@+node:ekr.20031218072017.3988:hideLogWindow
    def hideLogWindow (self):
        
        frame = self
        frame.divideLeoSplitter2(0.99, not frame.splitVerticalFlag)
    #@nonl
    #@-node:ekr.20031218072017.3988:hideLogWindow
    #@+node:ekr.20031218072017.3989:minimizeAll
    def minimizeAll(self):
    
        self.minimize(g.app.findFrame)
        self.minimize(g.app.pythonFrame)
        for frame in g.app.windowList:
            self.minimize(frame)
        
    def minimize(self, frame):
    
        if frame and frame.top.state() == "normal":
            frame.top.iconify()
    #@nonl
    #@-node:ekr.20031218072017.3989:minimizeAll
    #@+node:ekr.20031218072017.3990:toggleSplitDirection
    # The key invariant: self.splitVerticalFlag tells the alignment of the main splitter.
    def toggleSplitDirection(self):
        # Abbreviations.
        frame = self
        bar1 = self.bar1 ; bar2 = self.bar2
        split1Pane1,split1Pane2 = self.split1Pane1,self.split1Pane2
        split2Pane1,split2Pane2 = self.split2Pane1,self.split2Pane2
        # Switch directions.
        verticalFlag = self.splitVerticalFlag = not self.splitVerticalFlag
        orientation = g.choose(verticalFlag,"vertical","horizontal")
        g.app.config.setWindowPref("initial_splitter_orientation",orientation)
        # Reconfigure the bars.
        bar1.place_forget()
        bar2.place_forget()
        self.configureBar(bar1,verticalFlag)
        self.configureBar(bar2,not verticalFlag)
        # Make the initial placements again.
        self.placeSplitter(bar1,split1Pane1,split1Pane2,verticalFlag)
        self.placeSplitter(bar2,split2Pane1,split2Pane2,not verticalFlag)
        # Adjust the log and body panes to give more room around the bars.
        self.reconfigurePanes()
        # Redraw with an appropriate ratio.
        vflag,ratio,secondary_ratio = frame.initialRatios()
        self.resizePanesToRatio(ratio,secondary_ratio)
    #@nonl
    #@-node:ekr.20031218072017.3990:toggleSplitDirection
    #@+node:EKR.20040422130619:resizeToScreen
    def resizeToScreen (self):
        
        top = self.top
        
        w = top.winfo_screenwidth()
        h = top.winfo_screenheight()
        
        geom = "%dx%d%+d%+d" % (w-20,h-55,10,25)
    
        top.geometry(geom)
    #@nonl
    #@-node:EKR.20040422130619:resizeToScreen
    #@-node:ekr.20031218072017.3984:Window Menu...
    #@+node:ekr.20031218072017.3991:Help Menu...
    #@+node:ekr.20031218072017.3992:leoHelp
    def leoHelp (self):
        
        file = g.os_path_join(g.app.loadDir,"..","doc","sbooks.chm")
    
        if g.os_path_exists(file):
            os.startfile(file)
        else:	
            answer = g.app.gui.runAskYesNoDialog(
                "Download Tutorial?",
                "Download tutorial (sbooks.chm) from SourceForge?")
    
            if answer == "yes":
                try:
                    if 0: # Download directly.  (showProgressBar needs a lot of work)
                        url = "http://umn.dl.sourceforge.net/sourceforge/leo/sbooks.chm"
                        import urllib
                        self.scale = None
                        urllib.urlretrieve(url,file,self.showProgressBar)
                        if self.scale:
                            self.scale.destroy()
                            self.scale = None
                    else:
                        url = "http://prdownloads.sourceforge.net/leo/sbooks.chm?download"
                        import webbrowser
                        os.chdir(g.app.loadDir)
                        webbrowser.open_new(url)
                except:
                    g.es("exception dowloading sbooks.chm")
                    g.es_exception()
    #@nonl
    #@+node:ekr.20031218072017.3993:showProgressBar
    def showProgressBar (self,count,size,total):
    
        # g.trace("count,size,total:",count,size,total)
        if self.scale == None:
            #@        << create the scale widget >>
            #@+node:ekr.20031218072017.3994:<< create the scale widget >>
            top = Tk.Toplevel()
            top.title("Download progress")
            self.scale = scale = Tk.Scale(top,state="normal",orient="horizontal",from_=0,to=total)
            scale.pack()
            top.lift()
            #@nonl
            #@-node:ekr.20031218072017.3994:<< create the scale widget >>
            #@nl
        self.scale.set(count*size)
        self.scale.update_idletasks()
    #@nonl
    #@-node:ekr.20031218072017.3993:showProgressBar
    #@-node:ekr.20031218072017.3992:leoHelp
    #@-node:ekr.20031218072017.3991:Help Menu...
    #@-node:ekr.20031218072017.3979:Gui-dependent commands
    #@+node:ekr.20031218072017.998:Scrolling callbacks (frame)
    def setCallback (self,*args,**keys):
        
        """Callback to adjust the scrollbar.
        
        Args is a tuple of two floats describing the fraction of the visible area."""
    
        # g.trace(self.tree.redrawCount,args)
    
        apply(self.treeBar.set,args,keys)
    
        if self.tree.allocateOnlyVisibleNodes:
            self.tree.setVisibleArea(args)
            
    def yviewCallback (self,*args,**keys):
        
        """Tell the canvas to scroll"""
        
        # g.trace(vyiewCallback",args,keys)
    
        if self.tree.allocateOnlyVisibleNodes:
            self.tree.allocateNodesBeforeScrolling(args)
    
        apply(self.canvas.yview,args,keys)
    #@nonl
    #@-node:ekr.20031218072017.998:Scrolling callbacks (frame)
    #@+node:ekr.20031218072017.3995:Tk bindings...
    def getFocus(self):
        
        """Returns the widget that has focus, or body if None."""
        try:
            f = self.top.focus_displayof()
        except Exception:
            f = None
        if f:
            return f
        else:
            return self.bodyCtrl
            
    def getTitle (self):
        return self.top.title()
        
    def setTitle (self,title):
        return self.top.title(title)
        
    def get_window_info(self):
        return g.app.gui.get_window_info(self.top)
        
    def iconify(self):
        self.top.iconify()
    
    def deiconify (self):
        self.top.deiconify()
        
    def lift (self):
        self.top.lift()
        
    def update (self):
        self.top.update()
    #@-node:ekr.20031218072017.3995:Tk bindings...
    #@-others
#@nonl
#@-node:ekr.20031218072017.3940:class leoTkinterFrame
#@+node:ekr.20031218072017.3996:class leoTkinterBody
class leoTkinterBody (leoFrame.leoBody):
    
    """A class that represents the body pane of a Tkinter window."""

    #@    @+others
    #@+node:ekr.20031218072017.3997: Birth & death
    #@+node:ekr.20031218072017.2182:tkBody. __init__
    def __init__ (self,frame,parentFrame):
        
        # g.trace("leoTkinterBody")
        
        # Call the base class constructor.
        leoFrame.leoBody.__init__(self,frame,parentFrame)
    
        self.bodyCtrl = self.createControl(frame,parentFrame)
    
        self.colorizer = leoColor.colorizer(self.c)
    #@nonl
    #@-node:ekr.20031218072017.2182:tkBody. __init__
    #@+node:ekr.20031218072017.838:tkBody.createBindings
    def createBindings (self,frame):
        
        t = self.bodyCtrl
        
        # Event handlers...
        t.bind("<Button-1>", frame.OnBodyClick)
        t.bind("<Button-3>", frame.OnBodyRClick)
        t.bind("<Double-Button-1>", frame.OnBodyDoubleClick)
        t.bind("<Key>", frame.body.onBodyKey)
    
        # Gui-dependent commands...
        t.bind(g.virtual_event_name("Cut"), frame.OnCut)
        t.bind(g.virtual_event_name("Copy"), frame.OnCopy)
        t.bind(g.virtual_event_name("Paste"), frame.OnPaste)
    #@nonl
    #@-node:ekr.20031218072017.838:tkBody.createBindings
    #@+node:ekr.20031218072017.3998:tkBody.createControl
    def createControl (self,frame,parentFrame):
        
        config = g.app.config
    
        # A light selectbackground value is needed to make syntax coloring look good.
        wrap = config.getBoolWindowPref('body_pane_wraps')
        wrap = g.choose(wrap,"word","none")
        
        # Setgrid=1 cause severe problems with the font panel.
        body = Tk.Text(parentFrame,name='body',
            bd=2,bg="white",relief="flat",
            setgrid=0,wrap=wrap, selectbackground="Gray80") 
        
        bodyBar = Tk.Scrollbar(parentFrame,name='bodyBar')
        frame.bodyBar = self.bodyBar = bodyBar
        body['yscrollcommand'] = bodyBar.set
        bodyBar['command'] = body.yview
        bodyBar.pack(side="right", fill="y")
        
        # 8/30/03: Always create the horizontal bar.
        self.bodyXBar = bodyXBar = Tk.Scrollbar(
            parentFrame,name='bodyXBar',orient="horizontal")
        body['xscrollcommand'] = bodyXBar.set
        bodyXBar['command'] = body.xview
        self.bodyXbar = frame.bodyXBar = bodyXBar
        
        if wrap == "none":
            bodyXBar.pack(side="bottom", fill="x")
            
        body.pack(expand=1, fill="both")
    
        if 0: # Causes the cursor not to blink.
            body.configure(insertofftime=0)
            
        return body
    #@nonl
    #@-node:ekr.20031218072017.3998:tkBody.createControl
    #@-node:ekr.20031218072017.3997: Birth & death
    #@+node:ekr.20031218072017.2183:tkBody.setFontFromConfig
    def setFontFromConfig (self):
    
        config = g.app.config ; body = self.bodyCtrl
        
        font = config.getFontFromParams(
            "body_text_font_family", "body_text_font_size",
            "body_text_font_slant",  "body_text_font_weight",
            config.defaultBodyFontSize, tag = "body")
    
        if g.app.trace:
            g.trace(body.cget("font"),font.cget("family"),font.cget("weight"))
    
        body.configure(font=font)
        
        bg = config.getWindowPref("body_text_background_color")
        if bg:
            try: body.configure(bg=bg)
            except:
                g.es("exception setting body background color")
                g.es_exception()
        
        fg = config.getWindowPref("body_text_foreground_color")
        if fg:
            try: body.configure(fg=fg)
            except:
                g.es("exception setting body foreground color")
                g.es_exception()
    
        bg = config.getWindowPref("body_insertion_cursor_color")
        if bg:
            try: body.configure(insertbackground=bg)
            except:
                g.es("exception setting insertion cursor color")
                g.es_exception()
            
        if sys.platform != "win32": # Maybe a Windows bug.
            fg = config.getWindowPref("body_cursor_foreground_color")
            bg = config.getWindowPref("body_cursor_background_color")
            # print fg, bg
            if fg and bg:
                cursor="xterm" + " " + fg + " " + bg
                try: body.configure(cursor=cursor)
                except:
                    import traceback ; traceback.print_exc()
    #@nonl
    #@-node:ekr.20031218072017.2183:tkBody.setFontFromConfig
    #@+node:ekr.20031218072017.1320:body key handlers
    #@+at 
    #@nonl
    # The <Key> event generates the event before the body text is changed(!), 
    # so we register an idle-event handler to do the work later.
    # 
    # 1/17/02: Rather than trying to figure out whether the control or alt 
    # keys are down, we always schedule the idle_handler.  The idle_handler 
    # sees if any change has, in fact, been made to the body text, and sets 
    # the changed and dirty bits only if so.  This is the clean and safe way.
    # 
    # 2/19/02: We must distinguish between commands like "Find, Then Change", 
    # that call onBodyChanged, and commands like "Cut" and "Paste" that call 
    # onBodyWillChange.  The former commands have already changed the body 
    # text, and that change must be captured immediately.  The latter commands 
    # have not changed the body text, and that change may only be captured at 
    # idle time.
    #@-at
    #@@c
    
    #@+others
    #@+node:ekr.20031218072017.1321:idle_body_key
    def idle_body_key (self,p,oldSel,undoType,ch=None,oldYview=None,newSel=None,oldText=None):
        
        """Update the body pane at idle time."""
    
        # g.trace(ch,ord(ch))
        c = self.c
        if not c: return "break"
        if not p: return "break"
        if not c.isCurrentPosition(p): return "break"
    
        if g.doHook("bodykey1",c=c,v=p,ch=ch,oldSel=oldSel,undoType=undoType):
            return "break" # The hook claims to have handled the event.
        body = p.bodyString()
        if not newSel:
            newSel = c.frame.body.getTextSelection()
        if oldText != None:
            s = oldText
        else:
            s = c.frame.body.getAllText()
        #@    << return if nothing has changed >>
        #@+node:ekr.20031218072017.1322:<< return if nothing has changed >>
        # 6/22/03: Make sure we handle delete key properly.
        if ch not in ('\n','\r',chr(8)):
        
            if s == body:
                return "break"
        
            # Do nothing for control characters.
            if (ch == None or len(ch) == 0) and body == s[:-1]:
                return "break"
        #@nonl
        #@-node:ekr.20031218072017.1322:<< return if nothing has changed >>
        #@nl
        #@    << set removeTrailing >>
        #@+node:ekr.20031218072017.1323:<< set removeTrailing >>
        #@+at 
        #@nonl
        # Tk will add a newline only if:
        # 1. A real change has been made to the Tk.Text widget, and
        # 2. the change did _not_ result in the widget already containing a 
        # newline.
        # 
        # It's not possible to tell, given the information available, what Tk 
        # has actually done. We need only make a reasonable guess here.   
        # setUndoTypingParams stores the number of trailing newlines in each 
        # undo bead, so whatever we do here can be faithfully undone and 
        # redone.
        #@-at
        #@@c
        new = s ; old = body
        
        if len(new) == 0 or new[-1] != '\n':
            # There is no newline to remove.  Probably will never happen.
            removeTrailing = False
        elif len(old) == 0:
            # Ambigous case.  Formerly always returned False.
            if new == "\n\n":
                removeTrailing = True # Handle a very strange special case.
            else:
                removeTrailing = ch not in ('\r','\n')
        elif old == new[:-1]:
            # A single trailing character has been added.
            removeTrailing = ch not in ('\r','\n') # 6/12/04: Was false.
        else:
            # The text didn't have a newline, and now it does.
            # Moveover, some other change has been made to the text,
            # So at worst we have misrepresented the user's intentions slightly.
            removeTrailing = True
        
        if 0:
            print removeTrailing
            print repr(ch)
            print repr(oldText)
            print repr(old)
            print repr(new)
        #@nonl
        #@-node:ekr.20031218072017.1323:<< set removeTrailing >>
        #@nl
        if ch in ('\t','\n','\r',chr(8)):
            d = g.scanDirectives(c,p) # Support @tab_width directive properly.
            tab_width = d.get("tabwidth",c.tab_width) # ; g.trace(tab_width)
            if ch in ('\n','\r'):
                #@            << Do auto indent >>
                #@+node:ekr.20031218072017.1324:<< Do auto indent >> (David McNab)
                # Do nothing if we are in @nocolor mode or if we are executing a Change command.
                if self.frame.body.colorizer.useSyntaxColoring(p) and undoType != "Change":
                    # Get the previous line.
                    s=c.frame.bodyCtrl.get("insert linestart - 1 lines","insert linestart -1c")
                    # Add the leading whitespace to the present line.
                    junk,width = g.skip_leading_ws_with_indent(s,0,tab_width)
                    if s and len(s) > 0 and s[-1]==':':
                        # For Python: increase auto-indent after colons.
                        if self.colorizer.scanColorDirectives(p) == "python":
                            width += abs(tab_width)
                    if g.app.config.getBoolWindowPref("smart_auto_indent"):
                        # Added Nov 18 by David McNab, david@rebirthing.co.nz
                        # Determine if prev line has unclosed parens/brackets/braces
                        brackets = [width]
                        tabex = 0
                        for i in range(0, len(s)):
                            if s[i] == '\t':
                                tabex += tab_width - 1
                            if s[i] in '([{':
                                brackets.append(i+tabex + 1)
                            elif s[i] in '}])' and len(brackets) > 1:
                                brackets.pop()
                        width = brackets.pop()
                        # end patch by David McNab
                    ws = g.computeLeadingWhitespace (width,tab_width)
                    if ws and len(ws) > 0:
                        c.frame.bodyCtrl.insert("insert", ws)
                        removeTrailing = False # bug fix: 11/18
                #@nonl
                #@-node:ekr.20031218072017.1324:<< Do auto indent >> (David McNab)
                #@nl
            elif ch == '\t' and tab_width < 0:
                #@            << convert tab to blanks >>
                #@+node:ekr.20031218072017.1325:<< convert tab to blanks >>
                # Do nothing if we are executing a Change command.
                if undoType != "Change":
                    
                    # Get the characters preceeding the tab.
                    prev=c.frame.bodyCtrl.get("insert linestart","insert -1c")
                    
                    if 1: # 6/26/03: Convert tab no matter where it is.
                
                        w = g.computeWidth(prev,tab_width)
                        w2 = (abs(tab_width) - (w % abs(tab_width)))
                        # g.trace("prev w:",w,"prev chars:",prev)
                        c.frame.bodyCtrl.delete("insert -1c")
                        c.frame.bodyCtrl.insert("insert",' ' * w2)
                    
                    else: # Convert only leading tabs.
                    
                        # Get the characters preceeding the tab.
                        prev=c.frame.bodyCtrl.get("insert linestart","insert -1c")
                
                        # Do nothing if there are non-whitespace in prev:
                        all_ws = True
                        for ch in prev:
                            if ch != ' ' and ch != '\t':
                                all_ws = False
                        if all_ws:
                            w = g.computeWidth(prev,tab_width)
                            w2 = (abs(tab_width) - (w % abs(tab_width)))
                            # g.trace("prev w:",w,"prev chars:",prev)
                            c.frame.bodyCtrl.delete("insert -1c")
                            c.frame.bodyCtrl.insert("insert",' ' * w2)
                #@nonl
                #@-node:ekr.20031218072017.1325:<< convert tab to blanks >>
                #@nl
            elif ch in (chr(8)) and tab_width < 0:
                #@            << handle backspace with negative tab_width >>
                #@+node:EKR.20040604090913:<< handle backspace with negative tab_width >>
                # Get the preceeding characters.
                prev   =c.frame.bodyCtrl.get("insert linestart","insert")
                allPrev=c.frame.bodyCtrl.get("1.0","insert")
                n = len(allPrev)
                try:
                    oldAllPrev = body[:n]
                    assert(allPrev==oldAllPrev)
                    deletedChar = body[n:n+1]
                except (IndexError,AssertionError):
                    deletedChar = None
                
                if deletedChar in (u' ',' '):
                    n = len(prev) ; w = abs(tab_width)
                    n2 = n % w # Delete up to n2 - 1 spaces.
                    if n2 == w - 1: # Delete spaces only if they could have come from a tab.
                        count = 0
                        while n2 > 0:
                            n2 -= 1
                            ch = prev[n-count-1]
                            # g.trace(count,repr(ch))
                            if ch in (u' ',' '): count += 1
                            else: break
                        # g.trace(count,(n%w))
                        if count > 0:
                            c.frame.bodyCtrl.delete("insert -%dc" % count,"insert")
                #@nonl
                #@-node:EKR.20040604090913:<< handle backspace with negative tab_width >>
                #@nl
        #@    << set s to widget text, removing trailing newlines if necessary >>
        #@+node:ekr.20031218072017.1326:<< set s to widget text, removing trailing newlines if necessary >>
        s = c.frame.body.getAllText()
        if len(s) > 0 and s[-1] == '\n' and removeTrailing:
            s = s[:-1]
            
        # Major change: 6/12/04
        if s == body:
            # print "no real change"
            return "break"
        #@nonl
        #@-node:ekr.20031218072017.1326:<< set s to widget text, removing trailing newlines if necessary >>
        #@nl
        if undoType: # 11/6/03: set oldText properly when oldText param exists.
            if not oldText: oldText = body
            newText = s
            c.undoer.setUndoTypingParams(p,undoType,oldText,newText,oldSel,newSel,oldYview=oldYview)
        p.v.setTnodeText(s)
        p.v.t.insertSpot = c.frame.body.getInsertionPoint()
        #@    << recolor the body >>
        #@+node:ekr.20031218072017.1327:<< recolor the body >>
        self.frame.scanForTabWidth(p)
        
        incremental = undoType not in ("Cut","Paste") and not self.forceFullRecolorFlag
        self.frame.body.recolor_now(p,incremental=incremental)
        
        self.forceFullRecolorFlag = False
        #@nonl
        #@-node:ekr.20031218072017.1327:<< recolor the body >>
        #@nl
        if not c.changed:
            c.setChanged(True)
        #@    << redraw the screen if necessary >>
        #@+node:ekr.20031218072017.1328:<< redraw the screen if necessary >>
        redraw_flag = False
        
        c.beginUpdate()
        
        # Update dirty bits.
        if not p.isDirty() and p.setDirty(): # Sets all cloned and @file dirty bits
            redraw_flag = True
            
        # Update icons.
        val = p.computeIcon()
        
        # 7/8/04: During unit tests the node may not have been drawn,
        # So p.v.iconVal may not exist yet.
        if not hasattr(p.v,"iconVal") or val != p.v.iconVal:
            p.v.iconVal = val
            redraw_flag = True
        
        c.endUpdate(redraw_flag) # redraw only if necessary
        #@nonl
        #@-node:ekr.20031218072017.1328:<< redraw the screen if necessary >>
        #@nl
        g.doHook("bodykey2",c=c,v=p,ch=ch,oldSel=oldSel,undoType=undoType)
        return "break"
    #@-node:ekr.20031218072017.1321:idle_body_key
    #@+node:ekr.20031218072017.1329:onBodyChanged (called from core)
    # Called by command handlers that have already changed the text.
    
    def onBodyChanged (self,p,undoType,oldSel=None,oldYview=None,newSel=None,oldText=None):
        
        """Handle a change to the body pane."""
        
        c = self.c
        if not p:
            p = c.currentPosition()
    
        if not oldSel:
            oldSel = c.frame.body.getTextSelection()
    
        self.idle_body_key(p,oldSel,undoType,oldYview=oldYview,newSel=newSel,oldText=oldText)
    #@nonl
    #@-node:ekr.20031218072017.1329:onBodyChanged (called from core)
    #@+node:ekr.20031218072017.1330:onBodyKey
    def onBodyKey (self,event):
        
        """Handle any key press event in the body pane."""
    
        c = self.c ; ch = event.char
        
        # This translation is needed on MacOS.
        if ch == '':
            d = {'Return':'\r', 'Tab':'\t', 'BackSpace':chr(8)}
            ch = d.get(event.keysym,'')
    
        oldSel = c.frame.body.getTextSelection()
        
        p = c.currentPosition()
    
        if 0: # won't work when menu keys are bound.
            self.handleStatusLineKey(event)
            
        # We must execute this even if len(ch) > 0 to delete spurious trailing newlines.
        self.c.frame.bodyCtrl.after_idle(self.idle_body_key,p,oldSel,"Typing",ch)
    #@nonl
    #@+node:ekr.20040105223536:handleStatusLineKey
    def handleStatusLineKey (self,event):
        
        c = self.c ; frame = c.frame
        ch = event.char ; keysym = event.keysym
        keycode = event.keycode ; state = event.state
    
        if 1: # ch and len(ch)>0:
            #@        << trace the key event >>
            #@+node:ekr.20040105223536.1:<< trace the key event >>
            try:    self.keyCount += 1
            except: self.keyCount  = 1
            
            printable = g.choose(ch == keysym and state < 4,"printable","")
            
            print "%4d %s %d %s %x %s" % (
                self.keyCount,repr(ch),keycode,keysym,state,printable)
            #@nonl
            #@-node:ekr.20040105223536.1:<< trace the key event >>
            #@nl
    
        try:
            status = self.keyStatus
        except:
            status = [] ; frame.clearStatusLine()
        
        for sym,name in (
            ("Alt_L","Alt"),("Alt_R","Alt"),
            ("Control_L","Control"),("Control_R","Control"),
            ("Escape","Esc"),
            ("Shift_L","Shift"), ("Shift_R","Shift")):
            if keysym == sym:
                if name not in status:
                    status.append(name)
                    frame.putStatusLine(name + ' ')
                break
        else:
            status = [] ; frame.clearStatusLine()
    
        self.keyStatus = status
    #@nonl
    #@-node:ekr.20040105223536:handleStatusLineKey
    #@-node:ekr.20031218072017.1330:onBodyKey
    #@+node:ekr.20031218072017.1331:onBodyWillChange
    # Called by command handlers that change the text just before idle time.
    
    def onBodyWillChange (self,p,undoType,oldSel=None,oldYview=None):
        
        """Queue the body changed idle handler."""
        
        c = self.c
    
        if not oldSel:
            oldSel = c.frame.body.getTextSelection()
    
        if not p:
            p = c.currentPosition()
    
        self.c.frame.bodyCtrl.after_idle(self.idle_body_key,p,oldSel,undoType,oldYview)
    #@nonl
    #@-node:ekr.20031218072017.1331:onBodyWillChange
    #@-others
    #@nonl
    #@-node:ekr.20031218072017.1320:body key handlers
    #@+node:ekr.20031218072017.3999:forceRecolor
    def forceFullRecolor (self):
        
        self.forceFullRecolorFlag = True
    #@nonl
    #@-node:ekr.20031218072017.3999:forceRecolor
    #@+node:ekr.20031218072017.4000:Tk bindings (leoTkinterBody)
    #@+at
    # I could have used this to redirect all calls from the body class and the 
    # bodyCtrl to Tk. OTOH:
    # 
    # 1. Most of the wrappers do more than the old Tk routines now and
    # 2. The wrapper names are more discriptive than the Tk names.
    # 
    # Still, using the Tk names would have had its own appeal.  If I had 
    # prefixed the tk routine with tk_ the __getatt__ routine could have 
    # stripped it off!
    #@-at
    #@@c
    
    if 0: # This works.
        def __getattr__(self,attr):
            return getattr(self.bodyCtrl,attr)
            
    if 0: # This would work if all tk wrapper routines were prefixed with tk_
        def __getattr__(self,attr):
            if attr[0:2] == "tk_":
                return getattr(self.bodyCtrl,attr[3:])
    #@nonl
    #@+node:ekr.20031218072017.4001:Bounding box (Tk spelling)
    def bbox(self,index):
    
        return self.bodyCtrl.bbox(index)
    #@nonl
    #@-node:ekr.20031218072017.4001:Bounding box (Tk spelling)
    #@+node:ekr.20031218072017.4002:Color tags (Tk spelling)
    # Could have been replaced by the __getattr__ routine above...
    # 12/19/03: no: that would cause more problems.
    
    def tag_add (self,tagName,index1,index2):
        self.bodyCtrl.tag_add(tagName,index1,index2)
    
    def tag_bind (self,tagName,event,callback):
        self.bodyCtrl.tag_bind(tagName,event,callback)
    
    def tag_configure (self,colorName,**keys):
        self.bodyCtrl.tag_configure(colorName,keys)
    
    def tag_delete(self,tagName):
        self.bodyCtrl.tag_delete(tagName)
    
    def tag_remove (self,tagName,index1,index2):
        return self.bodyCtrl.tag_remove(tagName,index1,index2)
    #@nonl
    #@-node:ekr.20031218072017.4002:Color tags (Tk spelling)
    #@+node:ekr.20031218072017.2184:Configuration (Tk spelling)
    def cget(self,*args,**keys):
        
        val = self.bodyCtrl.cget(*args,**keys)
        
        if g.app.trace:
            g.trace(val,args,keys)
    
        return val
        
    def configure (self,*args,**keys):
        
        if g.app.trace:
            g.trace(args,keys)
        
        return self.bodyCtrl.configure(*args,**keys)
    #@nonl
    #@-node:ekr.20031218072017.2184:Configuration (Tk spelling)
    #@+node:ekr.20031218072017.4003:Focus
    def hasFocus (self):
        
        return self.bodyCtrl == self.frame.top.focus_displayof()
        
    def setFocus (self):
        
        self.bodyCtrl.focus_set()
    #@nonl
    #@-node:ekr.20031218072017.4003:Focus
    #@+node:ekr.20031218072017.4004:Height & width
    def getBodyPaneHeight (self):
        
        return self.bodyCtrl.winfo_height()
    
    def getBodyPaneWidth (self):
        
        return self.bodyCtrl.winfo_width()
    #@nonl
    #@-node:ekr.20031218072017.4004:Height & width
    #@+node:ekr.20031218072017.4005:Idle time...
    def scheduleIdleTimeRoutine (self,function,*args,**keys):
    
        self.bodyCtrl.after_idle(function,*args,**keys)
    #@nonl
    #@-node:ekr.20031218072017.4005:Idle time...
    #@+node:ekr.20031218072017.4006:Indices
    #@+node:ekr.20031218072017.4007:adjustIndex
    def adjustIndex (self,index,offset):
        
        t = self.bodyCtrl
        return t.index("%s + %dc" % (t.index(index),offset))
    #@nonl
    #@-node:ekr.20031218072017.4007:adjustIndex
    #@+node:ekr.20031218072017.4008:compareIndices
    def compareIndices(self,i,rel,j):
    
        return self.bodyCtrl.compare(i,rel,j)
    #@nonl
    #@-node:ekr.20031218072017.4008:compareIndices
    #@+node:ekr.20031218072017.4009:convertRowColumnToIndex
    def convertRowColumnToIndex (self,row,column):
        
        return self.bodyCtrl.index("%s.%s" % (row,column))
    #@nonl
    #@-node:ekr.20031218072017.4009:convertRowColumnToIndex
    #@+node:ekr.20031218072017.4010:convertIndexToRowColumn
    def convertIndexToRowColumn (self,index):
        
        index = self.bodyCtrl.index(index)
        start, end = string.split(index,'.')
        return int(start),int(end)
    #@nonl
    #@-node:ekr.20031218072017.4010:convertIndexToRowColumn
    #@+node:ekr.20031218072017.4011:getImageIndex
    def getImageIndex (self,image):
        
        return self.bodyCtrl.index(image)
    #@nonl
    #@-node:ekr.20031218072017.4011:getImageIndex
    #@+node:ekr.20031218072017.4012:tkIndex (internal use only)
    def tkIndex(self,index):
        
        """Returns the canonicalized Tk index."""
        
        if index == "start": index = "1.0"
        
        return self.bodyCtrl.index(index)
    #@nonl
    #@-node:ekr.20031218072017.4012:tkIndex (internal use only)
    #@-node:ekr.20031218072017.4006:Indices
    #@+node:ekr.20031218072017.4013:Insert point
    #@+node:ekr.20031218072017.495:getInsertionPoint & getBeforeInsertionPoint
    def getBeforeInsertionPoint (self):
        
        return self.bodyCtrl.index("insert-1c")
    
    def getInsertionPoint (self):
        
        return self.bodyCtrl.index("insert")
    #@nonl
    #@-node:ekr.20031218072017.495:getInsertionPoint & getBeforeInsertionPoint
    #@+node:ekr.20031218072017.4014:getCharAtInsertPoint & getCharBeforeInsertPoint
    def getCharAtInsertPoint (self):
        
        s = self.bodyCtrl.get("insert")
        return g.toUnicode(s,g.app.tkEncoding)
    
    def getCharBeforeInsertPoint (self):
    
        s = self.bodyCtrl.get("insert -1c")
        return g.toUnicode(s,g.app.tkEncoding)
    #@nonl
    #@-node:ekr.20031218072017.4014:getCharAtInsertPoint & getCharBeforeInsertPoint
    #@+node:ekr.20031218072017.4015:makeInsertPointVisible
    def makeInsertPointVisible (self):
        
        self.bodyCtrl.see("insert -5l")
    #@nonl
    #@-node:ekr.20031218072017.4015:makeInsertPointVisible
    #@+node:ekr.20031218072017.4016:setInsertionPointTo...
    def setInsertionPoint (self,index):
        self.bodyCtrl.mark_set("insert",index)
    
    def setInsertionPointToEnd (self):
        self.bodyCtrl.mark_set("insert","end")
        
    def setInsertPointToStartOfLine (self,lineNumber): # zero-based line number
        self.bodyCtrl.mark_set("insert",str(1+lineNumber)+".0 linestart")
    #@nonl
    #@-node:ekr.20031218072017.4016:setInsertionPointTo...
    #@-node:ekr.20031218072017.4013:Insert point
    #@+node:ekr.20031218072017.4017:Menus
    def bind (self,*args,**keys):
        
        return self.bodyCtrl.bind(*args,**keys)
    #@-node:ekr.20031218072017.4017:Menus
    #@+node:ekr.20031218072017.4018:Selection
    #@+node:ekr.20031218072017.4019:deleteTextSelection
    def deleteTextSelection (self,t=None):
        
        if t is None:
            t = self.bodyCtrl
        sel = t.tag_ranges("sel")
        if len(sel) == 2:
            start,end = sel
            if t.compare(start,"!=",end):
                t.delete(start,end)
    #@nonl
    #@-node:ekr.20031218072017.4019:deleteTextSelection
    #@+node:ekr.20031218072017.4020:getSelectedText
    def getSelectedText (self):
        
        """Return the selected text of the body frame, converted to unicode."""
    
        start, end = self.getTextSelection()
        if start and end and start != end:
            s = self.bodyCtrl.get(start,end)
            if s is None:
                return u""
            else:
                return g.toUnicode(s,g.app.tkEncoding)
        else:
            return None
    #@nonl
    #@-node:ekr.20031218072017.4020:getSelectedText
    #@+node:ekr.20031218072017.4021:getTextSelection
    def getTextSelection (self):
        
        """Return a tuple representing the selected range of body text.
        
        Return a tuple giving the insertion point if no range of text is selected."""
    
        bodyCtrl = self.bodyCtrl
        sel = bodyCtrl.tag_ranges("sel")
    
        if len(sel) == 2:
            return sel
        else:
            # Return the insertion point if there is no selected text.
            insert = bodyCtrl.index("insert")
            return insert,insert
    #@nonl
    #@-node:ekr.20031218072017.4021:getTextSelection
    #@+node:ekr.20031218072017.4022:hasTextSelection
    def hasTextSelection (self):
    
        sel = self.bodyCtrl.tag_ranges("sel")
        return sel and len(sel) == 2
    #@nonl
    #@-node:ekr.20031218072017.4022:hasTextSelection
    #@+node:ekr.20031218072017.4023:selectAllText
    def selectAllText (self):
    
        try:
            w = self.bodyCtrl.focus_get()
            g.app.gui.setTextSelection(w,"1.0","end")
        except:
            pass
    #@nonl
    #@-node:ekr.20031218072017.4023:selectAllText
    #@+node:ekr.20031218072017.4024:setTextSelection (tkinterBody)
    def setTextSelection (self,i,j=None):
        
        # Allow the user to pass either a 2-tuple or two separate args.
        if i is None:
            i,j = "1.0","1.0"
        elif len(i) == 2:
            i,j = i
    
        g.app.gui.setTextSelection(self.bodyCtrl,i,j)
    #@nonl
    #@-node:ekr.20031218072017.4024:setTextSelection (tkinterBody)
    #@-node:ekr.20031218072017.4018:Selection
    #@+node:ekr.20031218072017.4025:Text
    #@+node:ekr.20031218072017.4026:delete...
    def deleteAllText(self):
        self.bodyCtrl.delete("1.0","end")
    
    def deleteCharacter (self,index):
        t = self.bodyCtrl
        t.delete(t.index(index))
        
    def deleteLastChar (self):
        self.bodyCtrl.delete("end-1c")
        
    def deleteLine (self,lineNumber): # zero based line number.
        self.bodyCtrl.delete(str(1+lineNumber)+".0","end")
        
    def deleteLines (self,line1,numberOfLines): # zero based line numbers.
        self.bodyCtrl.delete(str(1+line1)+".0",str(1+line1+numberOfLines-1)+".0 lineend")
        
    def deleteRange (self,index1,index2):
        t = self.bodyCtrl
        t.delete(t.index(index1),t.index(index2))
    #@nonl
    #@-node:ekr.20031218072017.4026:delete...
    #@+node:ekr.20031218072017.4027:get...
    #@+node:ekr.20031218072017.4028:getAllText
    def getAllText (self):
        
        """Return all the body text, converted to unicode."""
        
        s = self.bodyCtrl.get("1.0","end")
        if s is None:
            return u""
        else:
            return g.toUnicode(s,g.app.tkEncoding)
    #@nonl
    #@-node:ekr.20031218072017.4028:getAllText
    #@+node:ekr.20031218072017.4029:getCharAtIndex
    def getCharAtIndex (self,index):
        
        """Return all the body text, converted to unicode."""
        
        s = self.bodyCtrl.get(index)
        if s is None:
            return u""
        else:
            return g.toUnicode(s,g.app.tkEncoding)
    #@nonl
    #@-node:ekr.20031218072017.4029:getCharAtIndex
    #@+node:ekr.20031218072017.4030:getInsertLines
    def getInsertLines (self):
        
        """Return before,after where:
            
        before is all the lines before the line containing the insert point.
        sel is the line containing the insert point.
        after is all the lines after the line containing the insert point.
        
        All lines end in a newline, except possibly the last line."""
        
        t = self.bodyCtrl
    
        before = t.get("1.0","insert linestart")
        ins    = t.get("insert linestart","insert lineend + 1c")
        after  = t.get("insert lineend + 1c","end")
    
        before = g.toUnicode(before,g.app.tkEncoding)
        ins    = g.toUnicode(ins,   g.app.tkEncoding)
        after  = g.toUnicode(after ,g.app.tkEncoding)
    
        return before,ins,after
    #@nonl
    #@-node:ekr.20031218072017.4030:getInsertLines
    #@+node:ekr.20031218072017.4031:getSelectionAreas
    def getSelectionAreas (self):
        
        """Return before,sel,after where:
            
        before is the text before the selected text
        (or the text before the insert point if no selection)
        sel is the selected text (or "" if no selection)
        after is the text after the selected text
        (or the text after the insert point if no selection)"""
        
        g.trace()
        t = self.bodyCtrl
        
        sel_index = t.getTextSelection()
        if len(sel_index) == 2:
            i,j = sel_index
            sel = t.get(i,j)
        else:
            i = j = t.index("insert")
            sel = ""
    
        before = t.get("1.0",i)
        after  = t.get(j,"end")
        
        before = g.toUnicode(before,g.app.tkEncoding)
        sel    = g.toUnicode(sel,   g.app.tkEncoding)
        after  = g.toUnicode(after ,g.app.tkEncoding)
        return before,sel,after
    #@nonl
    #@-node:ekr.20031218072017.4031:getSelectionAreas
    #@+node:ekr.20031218072017.2377:getSelectionLines (tkBody)
    def getSelectionLines (self):
        
        """Return before,sel,after where:
            
        before is the all lines before the selected text
        (or the text before the insert point if no selection)
        sel is the selected text (or "" if no selection)
        after is all lines after the selected text
        (or the text after the insert point if no selection)"""
        
        # At present, called only by c.getBodyLines.
    
        t = self.bodyCtrl
        sel_index = t.tag_ranges("sel") 
        if len(sel_index) != 2:
            if 1: # Choose the insert line.
                index = t.index("insert")
                sel_index = index,index
            else:
                return "","","" # Choose everything.
    
        i,j = sel_index
        i = t.index(i + "linestart")
        j = t.index(j + "lineend") # 10/24/03: -1c  # 11/4/03: no -1c.
        before = g.toUnicode(t.get("1.0",i),g.app.tkEncoding)
        sel    = g.toUnicode(t.get(i,j),    g.app.tkEncoding)
        after  = g.toUnicode(t.get(j,"end-1c"),g.app.tkEncoding)
        
        # g.trace(i,j)
        return before,sel,after
    #@nonl
    #@-node:ekr.20031218072017.2377:getSelectionLines (tkBody)
    #@+node:ekr.20031218072017.4032:getTextRange
    def getTextRange (self,index1,index2):
        
        t = self.bodyCtrl
        return t.get(t.index(index1),t.index(index2))
    #@nonl
    #@-node:ekr.20031218072017.4032:getTextRange
    #@-node:ekr.20031218072017.4027:get...
    #@+node:ekr.20031218072017.4033:Insert...
    #@+node:ekr.20031218072017.4034:insertAtInsertPoint
    def insertAtInsertPoint (self,s):
        
        self.bodyCtrl.insert("insert",s)
    #@nonl
    #@-node:ekr.20031218072017.4034:insertAtInsertPoint
    #@+node:ekr.20031218072017.4035:insertAtEnd
    def insertAtEnd (self,s):
        
        self.bodyCtrl.insert("end",s)
    #@nonl
    #@-node:ekr.20031218072017.4035:insertAtEnd
    #@+node:ekr.20031218072017.4036:insertAtStartOfLine
    def insertAtStartOfLine (self,lineNumber,s):
        
        self.bodyCtrl.insert(str(1+lineNumber)+".0",s)
    #@nonl
    #@-node:ekr.20031218072017.4036:insertAtStartOfLine
    #@-node:ekr.20031218072017.4033:Insert...
    #@+node:ekr.20031218072017.4037:setSelectionAreas (tkinterBody)
    def setSelectionAreas (self,before,sel,after):
        
        """Replace the body text by before + sel + after and
        set the selection so that the sel text is selected."""
    
        t = self.bodyCtrl ; gui = g.app.gui
        t.delete("1.0","end")
    
        if before: t.insert("1.0",before)
        sel_start = t.index("end-1c") # 10/24/03: -1c
    
        if sel: t.insert("end",sel)
        sel_end = t.index("end")
    
        if after:
            # A horrible Tk kludge.  Remove a trailing newline so we don't keep extending the text.
            if after[-1] == '\n':
                after = after[:-1]
            t.insert("end",after)
    
        gui.setTextSelection(t,sel_start,sel_end)
        # g.trace(sel_start,sel_end)
        
        return t.index(sel_start), t.index(sel_end)
    #@nonl
    #@-node:ekr.20031218072017.4037:setSelectionAreas (tkinterBody)
    #@-node:ekr.20031218072017.4025:Text
    #@+node:ekr.20031218072017.4038:Visibility & scrolling
    def makeIndexVisible (self,index):
        
        self.bodyCtrl.see(index)
        
    def setFirstVisibleIndex (self,index):
        
        self.bodyCtrl.yview("moveto",index)
        
    def getYScrollPosition (self):
        
        return self.bodyCtrl.yview()
        
    def setYScrollPosition (self,scrollPosition):
    
        if len(scrollPosition) == 2:
            first,last = scrollPosition
        else:
            first = scrollPosition
        self.bodyCtrl.yview("moveto",first)
        
    def scrollUp (self):
        
        self.bodyCtrl.yview("scroll",-1,"units")
        
    def scrollDown (self):
    
        self.bodyCtrl.yview("scroll",1,"units")
    #@nonl
    #@-node:ekr.20031218072017.4038:Visibility & scrolling
    #@-node:ekr.20031218072017.4000:Tk bindings (leoTkinterBody)
    #@-others
#@nonl
#@-node:ekr.20031218072017.3996:class leoTkinterBody
#@+node:ekr.20031218072017.4039:class leoTkinterLog
class leoTkinterLog (leoFrame.leoLog):
    
    """A class that represents the log pane of a Tkinter window."""

    #@    @+others
    #@+node:ekr.20031218072017.4040:tkLog.__init__
    def __init__ (self,frame,parentFrame):
        
        # g.trace("leoTkinterLog")
        
        # Call the base class constructor.
        leoFrame.leoLog.__init__(self,frame,parentFrame)
        
        self.colorTags = [] # list of color names used as tags in log window.
        
        self.logCtrl.bind("<Button-1>", self.onActivateLog)
    #@nonl
    #@-node:ekr.20031218072017.4040:tkLog.__init__
    #@+node:ekr.20031218072017.4041:tkLog.configureBorder & configureFont
    def configureBorder(self,border):
        
        self.logCtrl.configure(bd=border)
        
    def configureFont(self,font):
    
        self.logCtrl.configure(font=font)
    #@nonl
    #@-node:ekr.20031218072017.4041:tkLog.configureBorder & configureFont
    #@+node:ekr.20031218072017.4042:tkLog.createControl
    def createControl (self,parentFrame):
        
        config = g.app.config
        
        wrap = config.getBoolWindowPref('log_pane_wraps')
        wrap = g.choose(wrap,"word","none")
    
        log = Tk.Text(parentFrame,name="log",
            setgrid=0,wrap=wrap,bd=2,bg="white",relief="flat")
        
        self.logBar = logBar = Tk.Scrollbar(parentFrame,name="logBar")
    
        log['yscrollcommand'] = logBar.set
        logBar['command'] = log.yview
        
        logBar.pack(side="right", fill="y")
        # rr 8/14/02 added horizontal elevator 
        if wrap == "none": 
            logXBar = Tk.Scrollbar( 
                parentFrame,name='logXBar',orient="horizontal") 
            log['xscrollcommand'] = logXBar.set 
            logXBar['command'] = log.xview 
            logXBar.pack(side="bottom", fill="x")
        log.pack(expand=1, fill="both")
    
        return log
    #@nonl
    #@-node:ekr.20031218072017.4042:tkLog.createControl
    #@+node:ekr.20031218072017.4043:tkLog.getFontConfig
    def getFontConfig (self):
    
        font = self.logCtrl.cget("font")
        # g.trace(font)
        return font
    #@nonl
    #@-node:ekr.20031218072017.4043:tkLog.getFontConfig
    #@+node:ekr.20031218072017.4044:tkLog.hasFocus
    def hasFocus (self):
        
        return g.app.gui.get_focus(self.frame) == self.logCtrl
    #@nonl
    #@-node:ekr.20031218072017.4044:tkLog.hasFocus
    #@+node:ekr.20031218072017.4045:tkLog.onActivateLog
    def onActivateLog (self,event=None):
    
        try:
            g.app.setLog(self,"OnActivateLog")
            self.frame.tree.OnDeactivate()
        except:
            g.es_event_exception("activate log")
    #@nonl
    #@-node:ekr.20031218072017.4045:tkLog.onActivateLog
    #@+node:ekr.20031218072017.1473:tkLog.put & putnl & forceLogUpdate
    # All output to the log stream eventually comes here.
    def put (self,s,color=None):
        
        if g.app.quitting: return
        elif self.logCtrl:
            #@        << put s to log control >>
            #@+node:EKR.20040423082910:<< put s to log control >>
            if type(s) == type(u""): # 3/18/03
                s = g.toEncodedString(s,g.app.tkEncoding)
                
            if sys.platform == "darwin":
                print s,
            
            if color:
                if color not in self.colorTags:
                    self.colorTags.append(color)
                    self.logCtrl.tag_config(color,foreground=color)
                self.logCtrl.insert("end",s)
                self.logCtrl.tag_add(color,"end-%dc" % (len(s)+1),"end-1c")
                if "black" not in self.colorTags:
                    self.colorTags.append("black")
                    self.logCtrl.tag_config("black",foreground="black")
                self.logCtrl.tag_add("black","end")
            else:
                self.logCtrl.insert("end",s)
            
            self.logCtrl.see("end")
                
            self.forceLogUpdate()
            #@nonl
            #@-node:EKR.20040423082910:<< put s to log control >>
            #@nl
        else:
            #@        << put s to logWaiting and print s >>
            #@+node:EKR.20040423082910.1:<< put s to logWaiting and print s >>
            g.app.logWaiting.append((s,color),)
            
            print "Null tkinter log"
            if type(s) == type(u""): # 3/18/03
                s = g.toEncodedString(s,"ascii")
            print s
            #@nonl
            #@-node:EKR.20040423082910.1:<< put s to logWaiting and print s >>
            #@nl
    
    def putnl (self):
        if g.app.quitting: return
        elif self.logCtrl:
            #@        << put newline to log control >>
            #@+node:EKR.20040423082910.2:<< put newline to log control >>
            if sys.platform == "darwin":
                print
                
            self.logCtrl.insert("end",'\n')
            self.logCtrl.see("end")
            
            self.frame.tree.disableRedraw = True
            self.logCtrl.update_idletasks()
            #self.frame.outerFrame.update_idletasks() # 4/23/04
            #self.frame.top.update_idletasks()
            self.frame.tree.disableRedraw = False
            #@nonl
            #@-node:EKR.20040423082910.2:<< put newline to log control >>
            #@nl
        else:
            #@        << put newline to logWaiting and print newline >>
            #@+node:EKR.20040423082910.3:<< put newline to logWaiting and print newline >>
            g.app.logWaiting.append(('\n',"black"),)
            print "Null tkinter log"
            print
            #@nonl
            #@-node:EKR.20040423082910.3:<< put newline to logWaiting and print newline >>
            #@nl
            
    def forceLogUpdate (self):
        if sys.platform != "darwin": # Does not work on darwin.
            self.frame.tree.disableRedraw = True
            self.logCtrl.update_idletasks()
            #self.frame.outerFrame.update_idletasks() # 4/23/04
            #self.frame.top.update_idletasks()
            self.frame.tree.disableRedraw = False
    #@nonl
    #@-node:ekr.20031218072017.1473:tkLog.put & putnl & forceLogUpdate
    #@+node:ekr.20031218072017.4046:tkLog.setFontFromConfig
    def setFontFromConfig (self):
    
        logCtrl = self.logCtrl ; config = g.app.config
    
        font = config.getFontFromParams(
            "log_text_font_family", "log_text_font_size",
            "log_text_font_slant",  "log_text_font_weight",
            config.defaultLogFontSize)
        
        logCtrl.configure(font=font)
    
        bg = config.getWindowPref("log_text_background_color")
        if bg:
            try: logCtrl.configure(bg=bg)
            except: pass
        
        fg = config.getWindowPref("log_text_foreground_color")
        if fg:
            try: logCtrl.configure(fg=fg)
            except: pass
    #@nonl
    #@-node:ekr.20031218072017.4046:tkLog.setFontFromConfig
    #@-others
#@nonl
#@-node:ekr.20031218072017.4039:class leoTkinterLog
#@-others
#@nonl
#@-node:ekr.20031218072017.3939:@thin leoTkinterFrame.py
#@-leo
