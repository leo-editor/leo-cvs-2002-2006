# -*- coding: utf-8 -*-
#@+leo-ver=4-thin
#@+node:ekr.20031218072017.3939:@thin leoTkinterFrame.py
#@@first

#@@language python
#@@tabwidth -4
#@@pagewidth 80

#@<< imports >>
#@+node:ekr.20041221070525:<< imports >>

import leoGlobals as g

import leoColor,leoFrame,leoNodes
import leoTkinterMenu
import leoTkinterTree
import Tkinter as Tk
import tkFont

import os
import string
import sys
import threading
import time

Pmw = g.importExtension("Pmw",pluginName="leoTkinterFrame.py",verbose=False)
#@nonl
#@-node:ekr.20041221070525:<< imports >>
#@nl

use_Pmw = False

#@+others
#@+node:ekr.20031218072017.3940:class leoTkinterFrame
class leoTkinterFrame (leoFrame.leoFrame):
    
    """A class that represents a Leo window rendered in Tk/tkinter."""

    #@    @+others
    #@+node:ekr.20031218072017.3941: Birth & Death (tkFrame)
    #@+node:ekr.20031218072017.1801:__init__ (tkFrame)
    def __init__(self,title,gui):
    
        # Init the base class.
        leoFrame.leoFrame.__init__(self,gui)
    
        self.title = title
    
        leoTkinterFrame.instances += 1
    
        self.c = None # Set in finishCreate.
        self.iconBar = None
    
        #@    << set the leoTkinterFrame ivars >>
        #@+node:ekr.20031218072017.1802:<< set the leoTkinterFrame ivars >>
        # "Official ivars created in createLeoFrame and its allies.
        self.bar1 = None
        self.bar2 = None
        self.body = None
        self.bodyBar = None
        self.bodyCtrl = None
        self.bodyXBar = None
        self.f1 = self.f2 = None
        self.findPanel = None # Inited when first opened.
        self.iconBarComponentName = 'iconBar'
        self.iconFrame = None 
        self.log = None
        self.canvas = None
        self.outerFrame = None 
        self.statusFrame = None
        self.statusLineComponentName = 'statusLine'
        self.statusText = None 
        self.statusLabel = None 
        self.top = None
        self.tree = None
        self.treeBar = None
        
        # Used by event handlers...
        self.controlKeyIsDown = False # For control-drags
        self.draggedItem = None
        self.isActive = True
        self.redrawCount = 0
        self.revertHeadline = None # Previous headline text for abortEditLabel.
        self.wantedWidget = None
        self.wantedCallbackScheduled = False
        self.scrollWay = None
        #@nonl
        #@-node:ekr.20031218072017.1802:<< set the leoTkinterFrame ivars >>
        #@nl
    #@nonl
    #@-node:ekr.20031218072017.1801:__init__ (tkFrame)
    #@+node:ekr.20031218072017.3942:__repr__ (tkFrame)
    def __repr__ (self):
    
        return "<leoTkinterFrame: %s>" % self.title
    #@-node:ekr.20031218072017.3942:__repr__ (tkFrame)
    #@+node:ekr.20041221122440:f.component & components
    def component (self,name):
        
        return self.componentsDict.get(name)
        
    def components (self):
    
        return self.componentsDict.keys()
    #@nonl
    #@-node:ekr.20041221122440:f.component & components
    #@+node:ekr.20031218072017.2176:f.finishCreate & helpers
    def finishCreate (self,c):
        
        f = self ; f.c = c
        # g.trace('tkFrame')
        
        # This must be done after creating the commander.
        f.splitVerticalFlag,f.ratio,f.secondary_ratio = f.initialRatios()
        f.createOuterFrames()
        f.createIconBarComponents()
        f.createSplitterComponents()
        f.createStatusLineComponents()
        f.createFirstTreeNode()
        f.menu = leoTkinterMenu.leoTkinterMenu(f)
            # c.finishCreate calls f.createMenuBar later.
        g.app.setLog(f.log,"tkinterFrame.__init__") # the leoTkinterFrame containing the log
        g.app.windowList.append(f)
        c.initVersion()
        c.signOnWithVersion()
        f.miniBufferWidget = f.createMiniBufferWidget()
        f.body.createBindings(f)
    #@nonl
    #@+node:ekr.20051009044751:createOuterFrames
    def createOuterFrames (self):
    
        f = self ; c = f.c
        f.top = top = Tk.Toplevel()
        g.app.gui.attachLeoIcon(top)
        top.title(f.title)
        top.minsize(30,10) # In grid units.
        
        if g.os_path_exists(g.app.user_xresources_path):
            f.top.option_readfile(g.app.user_xresources_path)
        
        f.top.protocol("WM_DELETE_WINDOW", f.OnCloseLeoEvent)
        f.top.bind("<Button-1>", f.OnActivateLeoEvent)
        
        # These don't work on Windows. Because of bugs in window managers,
        # there is NO WAY to know which window is on top!
        f.top.bind("<Activate>",f.OnActivateLeoEvent)
        f.top.bind("<Deactivate>",f.OnDeactivateLeoEvent)
        
        f.top.bind("<Control-KeyPress>",f.OnControlKeyDown)
        f.top.bind("<Control-KeyRelease>",f.OnControlKeyUp)
        
        # Create the outer frame, the 'hull' component.
        f.outerFrame = Tk.Frame(top)
        f.outerFrame.pack(expand=1,fill="both")
        f.componentClass(c,'hull',f.outerFrame)
    #@-node:ekr.20051009044751:createOuterFrames
    #@+node:ekr.20051009044920:createIconBarComponents
    # Warning: there is also a method called createIconBar.
    
    def createIconBarComponents (self):
    
        f = self ; c = f.c
    
        iconBar = f.iconBarClass(c,f.outerFrame)
        f.iconFrame = iconBar.iconFrame
        f.iconBar = f.componentClass(c,
            f.iconBarComponentName,iconBar.iconFrame,
            iconBar,iconBar.pack,iconBar.unpack)
        f.iconBar.show()
    #@nonl
    #@-node:ekr.20051009044920:createIconBarComponents
    #@+node:ekr.20051009045208:createSplitterComponents
    def createSplitterComponents (self):
    
        f = self ; c = f.c
    
        f.createLeoSplitters(f.outerFrame)
        
        # Create the canvas, tree, log and body.
        f.canvas = f.createCanvas(f.split2Pane1)
        f.tree   = leoTkinterTree.leoTkinterTree(c,f,f.canvas)
        f.log    = leoTkinterLog(f,f.split2Pane2)
        f.body   = leoTkinterBody(f,f.split1Pane2)
        
        f.componentClass(c,'tree',f.split2Pane1, f.tree, f.packTree, f.unpackTree)
        f.componentClass(c,'log', f.split2Pane2, f.log,  f.packLog,  f.unpackLog)
        f.componentClass(c,'body',f.split1Pane2, f.body, f.packBody, f.unpackBody)
        
        # Yes, this an "official" ivar: this is a kludge.
        f.bodyCtrl = f.body.bodyCtrl
        
        # Configure.
        f.setTabWidth(c.tab_width)
        f.tree.setColorFromConfig()
        f.reconfigurePanes()
        f.body.setFontFromConfig()
        f.body.setColorFromConfig()
    #@nonl
    #@-node:ekr.20051009045208:createSplitterComponents
    #@+node:ekr.20051009045300:createStatusLineComponents
    # Warning: there is also a method called createStatusLine.
    
    def createStatusLineComponents (self):
        
        f = self ; c = f.c
        statusLine = f.statusLineClass(c,f.outerFrame)
        
        # Create offical ivars in the frame class.
        f.statusFrame = statusLine.statusFrame
        f.statusLabel = statusLine.labelWidget
        f.statusText  = statusLine.textWidget
        
        f.statusLine = f.componentClass(c,
            f.statusLineComponentName,
            statusLine.statusFrame,statusLine,statusLine.pack,statusLine.unpack)
        f.statusLine.show() # Show status line by default.
    #@nonl
    #@-node:ekr.20051009045300:createStatusLineComponents
    #@+node:ekr.20051009045404:createFirstTreeNode
    def createFirstTreeNode (self):
        
        f = self ; c = f.c
    
        t = leoNodes.tnode()
        v = leoNodes.vnode(c,t)
        p = leoNodes.position(v,[])
        v.initHeadString("NewHeadline")
        p.moveToRoot()
    
        c.beginUpdate()
        try:
            c.selectVnode(p)
            c.redraw()
            c.frame.getFocus()
            c.editPosition(p)
        finally:
            c.endUpdate(False)
    #@nonl
    #@-node:ekr.20051009045404:createFirstTreeNode
    #@+node:ekr.20050920094212:createMiniBufferWidget
    def createMiniBufferWidget (self):
        
        '''Create the minbuffer below the status line.'''
        
        frame = self ; c = frame.c
    
        frame.minibufferFrame = f = Tk.Frame(frame.outerFrame,relief='flat',borderwidth=0)
        if c.showMinibuffer:
            f.pack(side='bottom',fill='x')
    
        lab = Tk.Label(f,text='mini-buffer',justify='left',anchor='nw',foreground='blue')
        lab.pack(side='left')
    
        label = Tk.Label(f,relief='groove',justify='left',anchor='w')
        label.pack(side='left',fill='both',expand=1,padx=2,pady=1)
        
        frame.minibufferVisible = c.showMinibuffer
    
        return label
    #@nonl
    #@-node:ekr.20050920094212:createMiniBufferWidget
    #@-node:ekr.20031218072017.2176:f.finishCreate & helpers
    #@+node:ekr.20031218072017.3944:f.createCanvas & helpers
    def createCanvas (self,parentFrame,pack=True):
        
        c = self.c
        
        scrolls = c.config.getBool('outline_pane_scrolls_horizontally')
        scrolls = g.choose(scrolls,1,0)
        
        if use_Pmw and Pmw:
            canvas = self.createPmwTreeCanvas(parentFrame,scrolls,pack)
        else:
            canvas = self.createTkTreeCanvas(parentFrame,scrolls,pack)
    
        return canvas
    #@nonl
    #@+node:ekr.20041221071131:createPmwTreeCanvas
    def createPmwTreeCanvas (self,parentFrame,hScrollMode,pack):
        
        hscrollmode = g.choose(hScrollMode,'dynamic','none')
        
        self.scrolledCanvas = scrolledCanvas = Pmw.ScrolledCanvas(
            parentFrame,
            hscrollmode=hscrollmode,
            vscrollmode='dynamic')
    
        if pack:
            scrolledCanvas.pack(side='top',expand=1,fill="both")
    
        self.treeBar = scrolledCanvas.component('vertscrollbar')
        
        canvas = scrolledCanvas.component('canvas')
        canvas.configure(background='white')
        
        return canvas
    #@nonl
    #@-node:ekr.20041221071131:createPmwTreeCanvas
    #@+node:ekr.20041221071131.1:createTkTreeCanvas
    def createTkTreeCanvas (self,parentFrame,scrolls,pack):
        
        frame = self
        
        canvas = Tk.Canvas(parentFrame,name="canvas",
            bd=0,bg="white",relief="flat")
    
        frame.treeBar = treeBar = Tk.Scrollbar(parentFrame,name="treeBar")
        
        # Bind mouse wheel event to canvas
        if sys.platform != "win32": # Works on 98, crashes on XP.
            canvas.bind("<MouseWheel>", frame.OnMouseWheel)
            if 1: # New in 4.3.
                #@            << workaround for mouse-wheel problems >>
                #@+node:ekr.20050119210541:<< workaround for mouse-wheel problems >>
                # Handle mapping of mouse-wheel to buttons 4 and 5.
                
                def mapWheel(e):
                    if e.num == 4: # Button 4
                        e.delta = 120
                        return frame.OnMouseWheel(e)
                    elif e.num == 5: # Button 5
                        e.delta = -120
                        return frame.OnMouseWheel(e)
                
                canvas.bind("<ButtonPress>",mapWheel,add=1)
                #@nonl
                #@-node:ekr.20050119210541:<< workaround for mouse-wheel problems >>
                #@nl
            
        canvas['yscrollcommand'] = self.setCallback
        treeBar['command']     = self.yviewCallback
        treeBar.pack(side="right", fill="y")
        if scrolls: 
            treeXBar = Tk.Scrollbar( 
                parentFrame,name='treeXBar',orient="horizontal") 
            canvas['xscrollcommand'] = treeXBar.set 
            treeXBar['command'] = canvas.xview 
            treeXBar.pack(side="bottom", fill="x")
        
        if pack:
            canvas.pack(expand=1,fill="both")
    
        canvas.bind("<Button-1>", frame.OnActivateTree)
    
        # Handle mouse wheel in the outline pane.
        if sys.platform == "linux2": # This crashes tcl83.dll
            canvas.bind("<MouseWheel>", frame.OnMouseWheel)
        if 1:
            #@        << do scrolling by hand in a separate thread >>
            #@+node:ekr.20040709081208:<< do scrolling by hand in a separate thread >>
            # New in 4.3: replaced global way with scrollWay ivar.
            ev = threading.Event()
            
            def run(self=self,canvas=canvas,ev=ev):
            
                while 1:
                    ev.wait()
                    if self.scrollWay =='Down': canvas.yview("scroll", 1,"units")
                    else:                       canvas.yview("scroll",-1,"units")
                    time.sleep(.1)
            
            t = threading.Thread(target = run)
            t.setDaemon(True)
            t.start()
            
            def scrollUp(event): scrollUpOrDown(event,'Down')
            def scrollDn(event): scrollUpOrDown(event,'Up')
                
            def scrollUpOrDown(event,theWay):
                if event.widget!=canvas: return
                if 0: # This seems to interfere with scrolling.
                    if canvas.find_overlapping(event.x,event.y,event.x,event.y): return
                ev.set()
                self.scrollWay = theWay
                    
            def off(event,ev=ev,canvas=canvas):
                if event.widget!=canvas: return
                ev.clear()
            
            if 1: # Use shift-click
                # Shift-button-1 scrolls up, Shift-button-2 scrolls down
                canvas.bind_all('<Shift Button-3>',scrollDn)
                canvas.bind_all('<Shift Button-1>',scrollUp)
                canvas.bind_all('<Shift ButtonRelease-1>',off)
                canvas.bind_all('<Shift ButtonRelease-3>',off)
            else: # Use plain click.
                canvas.bind_all( '<Button-3>',scrollDn)
                canvas.bind_all( '<Button-1>',scrollUp)
                canvas.bind_all( '<ButtonRelease-1>',off)
                canvas.bind_all( '<ButtonRelease-3>',off)
            #@nonl
            #@-node:ekr.20040709081208:<< do scrolling by hand in a separate thread >>
            #@nl
        
        # g.print_bindings("canvas",canvas)
        return canvas
    #@nonl
    #@-node:ekr.20041221071131.1:createTkTreeCanvas
    #@-node:ekr.20031218072017.3944:f.createCanvas & helpers
    #@+node:ekr.20041221123325:createLeoSplitters & helpers
    def createLeoSplitters (self,parentFrame):
        
        if use_Pmw and Pmw:
            #@        << create Pmw splitters and their components >>
            #@+node:ekr.20041223130032:<< create Pmw splitters and their components >>
            # Create splitter1 and its components.
            splitter1 = self.createLeoPmwSplitter(parentFrame,self.splitVerticalFlag,'splitter1')
            self.split1Pane1 = splitter2Frame = splitter1.add('splitter2Frame',min=50,size=300)
            self.split1Pane2 = splitter1.add('body',min=50,size=300)
            
            # Create splitter2 and its components.
            splitter2 = self.createLeoPmwSplitter(splitter2Frame,not self.splitVerticalFlag,'splitter2')
            self.split2Pane1 = splitter2.add('outline',min=50,size=300)
            self.split2Pane2 = splitter2.add('log',min=50,size=50)
            
            # Set the colors of the separator and handle after adding the dynamic frames.
            for splitter in (splitter1,splitter2):
                bar = splitter.component('separator-1')
                bar.configure(background='LightSteelBlue2')
                handle = splitter.component('handle-1')
                handle.configure(background='SteelBlue2')
            #@nonl
            #@-node:ekr.20041223130032:<< create Pmw splitters and their components >>
            #@nl
        else:
            # Splitter 1 is the main splitter containing splitter2 and the body pane.
            f1,bar1,split1Pane1,split1Pane2 = self.createLeoTkSplitter(
                parentFrame,self.splitVerticalFlag,'splitter1')
    
            self.f1,self.bar1 = f1,bar1
            self.split1Pane1,self.split1Pane2 = split1Pane1,split1Pane2
    
            # Splitter 2 is the secondary splitter containing the tree and log panes.
            f2,bar2,split2Pane1,split2Pane2 = self.createLeoTkSplitter(
                split1Pane1,not self.splitVerticalFlag,'splitter2')
    
            self.f2,self.bar2 = f2,bar2
            self.split2Pane1,self.split2Pane2 = split2Pane1,split2Pane2
    #@nonl
    #@+node:ekr.20041221195402:Pmw...
    #@+node:ekr.20041221073427:createLeoPmwSplitter
    def createLeoPmwSplitter (self,parent,verticalFlag,name):
        
        c = self.c
        
        orient = g.choose(verticalFlag,'vertical','horizontal')
        command = g.choose(name=='splitter1',
            self.onPmwResizeSplitter1,self.onPmwResizeSplitter2)
    
        panedFrame = Pmw.PanedWidget(parent,
            orient=orient,
            separatorthickness = 6, # default is 2
            handlesize = 8,         # default is 8
            command = command)
    
        panedFrame.pack(expand=1,fill='both')
        
        self.componentClass(c,name,panedFrame,panedFrame)
    
        return panedFrame
    #@nonl
    #@-node:ekr.20041221073427:createLeoPmwSplitter
    #@+node:ekr.20031218072017.3946:resizePanesToRatio
    def resizePanesToRatio(self,ratio,ratio2):
        
        # g.trace(ratio,ratio2)
        
        if use_Pmw and Pmw:
            #@        << resize the Pmw panes >>
            #@+node:ekr.20050104084531:<< resize the Pmw panes >>
            self.ratio = ratio
            self.secondary_ratio = ratio2
            splitter1 = self.component('splitter1').getObject()
            splitter2 = self.component('splitter2').getObject()
            
            if self.splitVerticalFlag:
                # Use ratio to set splitter2 height.
                size = ratio * float(splitter1.winfo_height())
                splitter1.configurepane('splitter2Frame',size=int(size))
                # Use ratio2 to set outline width.
                size = ratio2 * float(splitter2.winfo_width())
                splitter2.configurepane('outline',size=int(size))
            else:
                # Use ratio to set splitter2 width.
                size = ratio * float(splitter1.winfo_width())
                splitter1.configurepane('splitter2Frame',size=int(size))
                # Use ratio2 to set outline height.
                size = ratio2 * float(splitter2.winfo_height())
                splitter2.configurepane('outline',size=int(size))
            #@nonl
            #@-node:ekr.20050104084531:<< resize the Pmw panes >>
            #@nl
        else:
            self.divideLeoSplitter(self.splitVerticalFlag,ratio)
            self.divideLeoSplitter(not self.splitVerticalFlag,ratio2)
    #@nonl
    #@-node:ekr.20031218072017.3946:resizePanesToRatio
    #@+node:ekr.20041221075743:onPmwResizeSplitter1/2
    #@+at 
    #@nonl
    # These methods cause problems because Pmw.PanedWidget's calls these 
    # methods way too often.
    # 
    # We don't need to remember changes to pane sizes, for several reasons:
    # 1. The initial secondary ratio is always set by 
    # leoFrame.initialRatios().
    #     - Remembering this ratio implies a change to the file format and is 
    # not worth the cost.
    #     - The user can set these initial ratios with user options.
    # 2. The only benefit of remembering the secondary ratio is when using the 
    # Equal Sized Panes command.
    #     - But resetting the secondary ratio to the default secondary ratio 
    # is good enough.
    # 3. Not remembering these ratios simplifies the code enough to be worth 
    # doing.
    #@-at
    #@@c
    
    def onPmwResizeSplitter1 (self,sizes):
        if 0: # Don't try to remember size changes.
            if not self.initing:
                n1,n2 = sizes
                n1,n2 = float(n1),float(n2)
                self.ratio = n1/(n1+n2)
                # g.trace(self.ratio)
        
    def onPmwResizeSplitter2 (self,sizes):
        if 0: # Don't try to remember size changes.
            if not self.initing:
                n1,n2 = sizes
                n1,n2 = float(n1),float(n2)
                self.secondary_ratio = n1/(n1+n2)
                # g.trace(self.secondary_ratio)
    #@nonl
    #@-node:ekr.20041221075743:onPmwResizeSplitter1/2
    #@-node:ekr.20041221195402:Pmw...
    #@+node:ekr.20041221185246:Tk...
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
    #@nonl
    #@+node:ekr.20041221073427.1:createLeoTkSplitter
    def createLeoTkSplitter (self,parent,verticalFlag,componentName):
        
        c = self.c
    
        # Create the frames.
        f = Tk.Frame(parent,bd=0,relief="flat")
        f.pack(expand=1,fill="both",pady=1)
        
        f1 = Tk.Frame(f)
        f2 = Tk.Frame(f)
        bar = Tk.Frame(f,bd=2,relief="raised",bg="LightSteelBlue2")
    
        # Configure and place the frames.
        self.configureBar(bar,verticalFlag)
        self.bindBar(bar,verticalFlag)
        self.placeSplitter(bar,f1,f2,verticalFlag)
        
        # Define the splitter, bar and outer frame components.
        # It would be useless to define placed components here.
        # N.B. All frames managed by the placer must descend from splitterFrame1 or splitterFrame2
        self.componentClass(self.c,componentName,f)
        if componentName == 'splitter1':
            self.componentClass(c,'splitter1Frame',f)
            self.componentClass(c,'splitBar1',bar)
        else:
            self.componentClass(c,'splitter2Frame',f)
            self.componentClass(c,'splitBar2',bar)
    
        return f, bar, f1, f2
    #@nonl
    #@-node:ekr.20041221073427.1:createLeoTkSplitter
    #@+node:ekr.20031218072017.3947:bindBar
    def bindBar (self, bar, verticalFlag):
    
        if verticalFlag == self.splitVerticalFlag:
            bar.bind("<B1-Motion>", self.onDragMainSplitBar)
    
        else:
            bar.bind("<B1-Motion>", self.onDragSecondarySplitBar)
    #@nonl
    #@-node:ekr.20031218072017.3947:bindBar
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
    
        if use_Pmw and Pmw:
            return
    
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
    #@-node:ekr.20041221185246:Tk...
    #@-node:ekr.20041221123325:createLeoSplitters & helpers
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
    
        # Destroy all ivars in subcommanders.
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
        
        panels = (self.comparePanel, self.colorPanel, self.findPanel, self.fontPanel, self.prefsPanel)
    
        for panel in panels:
            if panel:
                panel.top.destroy()
    #@nonl
    #@-node:ekr.20031218072017.3965:destroyAllPanels
    #@+node:ekr.20031218072017.1974:destroySelf
    def destroySelf (self):
        
        top = self.top # Remember this: we are about to destroy all of our ivars!
        
        # g.trace(self)
    
        self.destroyAllObjects()
    
        top.destroy()
    #@nonl
    #@-node:ekr.20031218072017.1974:destroySelf
    #@-node:ekr.20031218072017.3964:Destroying the frame
    #@-node:ekr.20031218072017.3941: Birth & Death (tkFrame)
    #@+node:ekr.20041223095751:class componentClass (componentBaseClass)
    class componentClass (leoFrame.componentBaseClass):
        
        '''A class to manage components of Leo windows'''
        
        #@    @+others
        #@+node:ekr.20041223095751.1: ctor
        def __init__ (self,c,name,frame,obj=None,packer=None,unpacker=None):
            
            # Init the base class.
            leoFrame.componentBaseClass.__init__(
                self,c,name,frame,obj,packer,unpacker)
            
            self.setPacker(packer)
            self.setUnpacker(unpacker)
        #@nonl
        #@-node:ekr.20041223095751.1: ctor
        #@+node:ekr.20041223154028.4:__repr__
        def __repr__ (self):
            
            return '<component %s>' % self.name
        #@nonl
        #@-node:ekr.20041223154028.4:__repr__
        #@+node:ekr.20041223124022:destroy
        def destroy (self):
            
            try:
                del c.frame.componentsDict[self.name]
            except KeyError:
                g.es("No component named %s" % name,color='blue')
        #@nonl
        #@-node:ekr.20041223124022:destroy
        #@+node:ekr.20041223124022.1:getters & setters
        # Setters...
        def setPacker (self,packer):
            if not packer: # Define default packer.
                def packer():
                    if self.frame:
                        self.frame.pack(side='top',expand=1,fill='both')
            self.packer = packer
        
        def setUnpacker (self,unpacker):
            if not unpacker: # Define default unpacker.
                def unpacker():
                    if self.frame:
                        self.frame.pack_forget()
            self.unpacker = unpacker
        #@nonl
        #@-node:ekr.20041223124022.1:getters & setters
        #@+node:ekr.20041223095751.2:pack & unpack
        def pack (self):
        
            self.packer()
            
        def unpack (self):
        
            self.unpacker()
        #@nonl
        #@-node:ekr.20041223095751.2:pack & unpack
        #@-others
    #@nonl
    #@-node:ekr.20041223095751:class componentClass (componentBaseClass)
    #@+node:ekr.20041223104933:class statusLineClass
    class statusLineClass:
        
        '''A class representing the status line.'''
        
        #@    @+others
        #@+node:ekr.20031218072017.3961: ctor
        def __init__ (self,c,parentFrame):
            
            self.c = c
            self.bodyCtrl = c.frame.bodyCtrl
            self.colorTags = [] # list of color names used as tags.
            self.enabled = False
            self.isVisible = False
            self.lastRow = self.lastCol = 0
            self.log = c.frame.log
            #if 'black' not in self.log.colorTags:
            #    self.log.colorTags.append("black")
            self.parentFrame = parentFrame
            self.statusFrame = Tk.Frame(parentFrame,bd=2)
            text = "line 0, col 0"
            width = len(text) + 4
            self.labelWidget = Tk.Label(self.statusFrame,text=text,width=width,anchor="w")
            self.labelWidget.pack(side="left",padx=1)
            
            bg = self.statusFrame.cget("background")
            self.textWidget = Tk.Text(self.statusFrame,
                height=1,state="disabled",bg=bg,relief="groove")
            self.textWidget.pack(side="left",expand=1,fill="x")
            self.textWidget.bind("<Button-1>", self.onActivate)
        #@nonl
        #@-node:ekr.20031218072017.3961: ctor
        #@+node:ekr.20031218072017.3962:clear
        def clear (self):
            
            t = self.textWidget
            if not t: return
            
            t.configure(state="normal")
            t.delete("1.0","end")
            t.configure(state="disabled")
        #@nonl
        #@-node:ekr.20031218072017.3962:clear
        #@+node:EKR.20040424153344:enable, disable & isEnabled
        def disable (self,background=None):
            
            c = self.c ; t = self.textWidget
            if t:
                if not background:
                    background = self.statusFrame.cget("background")
                t.configure(state="disabled",background=background)
            self.enabled = False
            c.frame.bodyWantsFocus(c.frame.bodyCtrl,tag='statusLine.disable')
            
        def enable (self,background="white"):
            
            # g.trace()
            c = self.c ; t = self.textWidget
            if t:
                t.configure(state="normal",background=background)
                c.frame.statusLineWantsFocus(t,tag='statusLine.ensable')
                t.focus_set()
            self.enabled = True
                
        def isEnabled(self):
            return self.enabled
        #@nonl
        #@-node:EKR.20040424153344:enable, disable & isEnabled
        #@+node:ekr.20041026132435:get
        def get (self):
            
            t = self.textWidget
            if t:
                return t.get("1.0","end")
            else:
                return ""
        #@nonl
        #@-node:ekr.20041026132435:get
        #@+node:ekr.20041223114744:getFrame
        def getFrame (self):
            
            return self.statusFrame
        #@nonl
        #@-node:ekr.20041223114744:getFrame
        #@+node:ekr.20050120093555:onActivate
        def onActivate (self,event=None):
            
            # Don't change background as the result of simple mouse clicks.
            background = self.statusFrame.cget("background")
            self.enable(background=background)
        #@nonl
        #@-node:ekr.20050120093555:onActivate
        #@+node:ekr.20041223111916:pack & show
        def pack (self):
            
            if not self.isVisible:
                self.isVisible = True
                self.statusFrame.pack(fill="x",pady=1)
        
                # Register an idle-time handler to update the row and column indicators.
                self.statusFrame.after_idle(self.update)
                
        show = pack
        #@nonl
        #@-node:ekr.20041223111916:pack & show
        #@+node:ekr.20031218072017.3963:put (leoTkinterFrame:statusLineClass)
        def put(self,s,color=None):
            
            t = self.textWidget
            if not t: return
            
            t.configure(state="normal")
                
            if color and color not in self.colorTags:
                self.colorTags.append(color)
                t.tag_config(color,foreground=color)
        
            if color:
                t.insert("end",s)
                t.tag_add(color,"end-%dc" % (len(s)+1),"end-1c")
                t.tag_config("black",foreground="black")
                t.tag_add("black","end")
            else:
                t.insert("end",s)
            
            t.configure(state="disabled")
            t.update_idletasks()
        #@nonl
        #@-node:ekr.20031218072017.3963:put (leoTkinterFrame:statusLineClass)
        #@+node:EKR.20040424154804:setFocus
        if 0: # No longer used in 4.3.  Done as the result of statusLineWantsFocus.
        
            def setFocus (self):
            
                # Force the focus to the icon area.
                t = self.textWidget
                if t:
                    t.focus_set()
        #@nonl
        #@-node:EKR.20040424154804:setFocus
        #@+node:ekr.20041223111916.1:unpack & hide
        def unpack (self):
            
            if self.isVisible:
                self.isVisible = False
                self.statusFrame.pack_forget()
        
        hide = unpack
        #@nonl
        #@-node:ekr.20041223111916.1:unpack & hide
        #@+node:ekr.20031218072017.1733:update
        def update (self):
            
            c = self.c ; body = self.bodyCtrl ; lab = self.labelWidget
            if g.app.killed or not self.isVisible:
                return
        
            index = body.index("insert")
            row,col = g.app.gui.getindex(body,index)
        
            if col > 0:
                s = body.get("%d.0" % (row),index)
                s = g.toUnicode(s,g.app.tkEncoding)
                col = g.computeWidth (s,c.tab_width)
        
            if row != self.lastRow or col != self.lastCol:
                s = "line %d, col %d " % (row,col)
                lab.configure(text=s)
                self.lastRow = row
                self.lastCol = col
        
            self.statusFrame.after(500,self.update)
        #@nonl
        #@-node:ekr.20031218072017.1733:update
        #@-others
    #@nonl
    #@-node:ekr.20041223104933:class statusLineClass
    #@+node:ekr.20041223102225:class iconBarClass
    class iconBarClass:
        
        '''A class representing the singleton Icon bar'''
        
        #@    @+others
        #@+node:ekr.20041223102225.1: ctor
        def __init__ (self,c,parentFrame):
            
            self.c = c
            
            self.iconFrame = Tk.Frame(
                parentFrame,height="5m",bd=2,relief="groove") # ,background='blue')
            self.parentFrame = parentFrame
            self.visible = False
        #@nonl
        #@-node:ekr.20041223102225.1: ctor
        #@+node:ekr.20031218072017.3958:add
        def add(self,*args,**keys):
            
            """Add a button containing text or a picture to the icon bar.
            
            Pictures take precedence over text"""
            
            f = self.iconFrame
            text = keys.get('text')
            imagefile = keys.get('imagefile')
            image = keys.get('image')
            command = keys.get('command')
            bg = keys.get('bg')
        
            if not imagefile and not image and not text: return
        
            # First define n.	
            try:
                g.app.iconWidgetCount += 1
                n = g.app.iconWidgetCount
            except:
                n = g.app.iconWidgetCount = 1
        
            if not command:
                def command():
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
                
                b = Tk.Button(f,text=text,relief="groove",bd=2,command=command)
                if sys.platform != 'darwin':
                    width = max(6,len(text))
                    b.configure(width=width)
                b.pack(side="left", fill="y")
                return b
                
            return None
        #@nonl
        #@-node:ekr.20031218072017.3958:add
        #@+node:ekr.20031218072017.3956:clear
        def clear(self):
            
            """Destroy all the widgets in the icon bar"""
            
            f = self.iconFrame
            
            for slave in f.pack_slaves():
                slave.destroy()
            self.visible = False
        
            f.configure(height="5m") # The default height.
            g.app.iconWidgetCount = 0
            g.app.iconImageRefs = []
        #@-node:ekr.20031218072017.3956:clear
        #@+node:ekr.20041223114821:getFrame
        def getFrame (self):
        
            return self.iconFrame
        #@nonl
        #@-node:ekr.20041223114821:getFrame
        #@+node:ekr.20041223102225.2:pack (show)
        def pack (self):
            
            """Show the icon bar by repacking it"""
            
            if not self.visible:
                self.visible = True
                self.iconFrame.pack(fill="x",pady=2)
                
        show = pack
        #@nonl
        #@-node:ekr.20041223102225.2:pack (show)
        #@+node:ekr.20031218072017.3955:unpack (hide)
        def unpack (self):
            
            """Hide the icon bar by unpacking it.
            
            A later call to show will repack it in a new location."""
            
            if self.visible:
                self.visible = False
                self.iconFrame.pack_forget()
                
        hide = unpack
        #@nonl
        #@-node:ekr.20031218072017.3955:unpack (hide)
        #@-others
    #@nonl
    #@-node:ekr.20041223102225:class iconBarClass
    #@+node:ekr.20041222060024:tkFrame.unpack/repack...
    #@+node:ekr.20041223160653:pane packers
    def placePane1(self,verticalFlag,pane1,frac):
        if verticalFlag:
            pane1.place(relx=0.5,rely=0,anchor="n",relwidth=1.0,relheight=frac)
        else:
            pane1.place(rely=0.5,relx=0,anchor="w",relheight=1.0,relwidth=frac)
            
    def placePane2(self,verticalFlag,pane2,frac):
        if verticalFlag:
            pane2.place(relx=0.5,rely=1.0,anchor="s",relwidth=1.0,relheight=1-frac)
        else:
            pane2.place(rely=0.5,relx=1.0,anchor="e",relheight=1.0,relwidth=1-frac)
    
    # These are the packers of the corresponding components.
    # These are called from, packComponent('body'), etc.
    def packBody (self):
        # Pane 2 of primary splitter.
        self.placePane2(self.splitVerticalFlag,self.split1Pane2,self.ratio)
    def packLog (self):
        # Pane 2 of secondary splitter.
        self.placePane2(not self.splitVerticalFlag,self.split2Pane2,self.secondary_ratio)
    def packTree (self):
        # Pane 1 of secondary splitter.
        self.placePane1(not self.splitVerticalFlag,self.split2Pane1,self.secondary_ratio)
    #@nonl
    #@-node:ekr.20041223160653:pane packers
    #@+node:ekr.20041224102942:pane replacers
    #@+node:ekr.20041224105456.1:replaceBodyPaneWithComponent
    def replaceBodyPaneWithComponent (self,componentName):
        component = self.component(componentName)
        if component:
            f = component.getFrame()
            if f:
                component.setPacker(self.packBody)
                component.setUnpacker(self.unpackBody)
                self.unpackComponent('body')
                self.split1Pane2 = f
                self.packBody()
    #@nonl
    #@-node:ekr.20041224105456.1:replaceBodyPaneWithComponent
    #@+node:ekr.20041224105456.3:replaceLogPaneWithComponent
    def replaceLogPaneWithComponent (self,componentName):
        component = self.component(componentName)
        if component:
            f = component.getFrame()
            if f:
                component.setPacker(self.packLog)
                component.setUnpacker(self.unpackLog)
                self.unpackComponent('log')
                self.split2Pane2 = f
                self.packLog()
                self.divideLeoSplitter(not self.splitVerticalFlag,self.secondary_ratio)
    #@nonl
    #@-node:ekr.20041224105456.3:replaceLogPaneWithComponent
    #@+node:ekr.20041224105456.4:replaceTreePaneWithComponent
    def replaceTreePaneWithComponent (self,componentName):
        component = self.component(componentName)
        if component:
            f = component.getFrame()
            if f:
                component.setPacker(self.packTree)
                component.setUnpacker(self.unpackTree)
                self.unpackComponent('tree')
                self.split2Pane1 = f
                self.packTree()
                self.divideLeoSplitter(not self.splitVerticalFlag,self.secondary_ratio)
    #@nonl
    #@-node:ekr.20041224105456.4:replaceTreePaneWithComponent
    #@-node:ekr.20041224102942:pane replacers
    #@+node:ekr.20041223162512:pane unpackers
    # These are the packers of the corresponding components.
    
    def unpackBody(self):
        self.split1Pane2.place_forget()
        
    def unpackLog(self):
        self.split2Pane2.place_forget()
    
    def unpackTree(self):
        self.split2Pane1.place_forget()
    #@nonl
    #@-node:ekr.20041223162512:pane unpackers
    #@+node:ekr.20041222061439:pack/unpackComponent
    # Note: the 'packers' for the 'body', 'log' and 'tree' components are actually placers,
    # so packing twice does not duplicate those component.
    
    def packComponent (self,name,verbose=True):
        component = self.component(name)
        if component:
            component.pack()
        elif verbose:
            g.es("packComponent: no component named %s" % name,color='blue')
    
    def unpackComponent (self,name,verbose=True):
        component = self.component(name)
        if component:
            component.unpack()
        elif verbose:
            g.es("unpackComponent: no component named %s" % name,color='blue')
    #@nonl
    #@-node:ekr.20041222061439:pack/unpackComponent
    #@+node:ekr.20041224072631:show/hideComponent
    def hideComponent (self,name):
        component = self.component(name)
        if component:
            component.hide()
        else:
            g.es("hideComponent: no component named %s" % name,color='blue')
    
    def showComponent (self,name):
        component = self.component(name)
        if component:
            component.show()
        else:
            g.es("showComponent: no component named %s" % name,color='blue')
    #@nonl
    #@-node:ekr.20041224072631:show/hideComponent
    #@-node:ekr.20041222060024:tkFrame.unpack/repack...
    #@+node:ekr.20051014154752:Minibuffer methods
    def showMinibuffer (self):
        
        frame = self
        
        if not frame.minibufferVisible:
            frame.minibufferFrame.pack(side='bottom',fill='x')
            frame.minibufferVisible = True
            
    def hideMinibuffer (self):
        
        frame = self
        if frame.minibufferVisible:
            frame.minibufferFrame.pack_forget()
            frame.minibufferVisible = False
    #@nonl
    #@-node:ekr.20051014154752:Minibuffer methods
    #@+node:ekr.20031218072017.3953:Icon area methods (compatibility)
    def getIconBarObject(self):
        component = self.component(self.iconBarComponentName)
        if not component: return g.trace("No iconBar component")
        obj = component.getObject()
        if obj: return obj
        else: return g.trace(
            "%s component has no status line object" % (
                self.iconBarComponentName))
                    
    def callIconBar(self,name,*args,**keys):
        obj = self.getIconBarObject()
        if not obj: return
        try:
            f = getattr(obj,name)
            return f(*args,**keys)
        except AttributeError:
            return g.trace("%s component has no '%s' method" % (
                self.iconBarComponentName,name))
    
    def addIconButton (self,*args,**keys):
        return self.callIconBar('add',*args,**keys)
    
    def clearIconBar (self):
        return self.callIconBar('clear')
    
    def createIconBar (self):
        self.callIconBar('show')
        return self.getIconBarObject() # For compatibility.
    
    def hideIconBar (self):
        return self.callIconBar('hide')
    #@nonl
    #@-node:ekr.20031218072017.3953:Icon area methods (compatibility)
    #@+node:ekr.20041223105114.1:Status line methods (compatibility)
    def getStatusObject(self):
        component = self.component(self.statusLineComponentName)
        if not component: return g.trace("No statusLine component")
        obj = component.getObject()
        if obj: return obj
        else: return g.trace(
            "%s component has no status line object" % (
                self.statusLineComponentName))
                    
    def callStatus(self,name,*args,**keys):
        obj = self.getStatusObject()
        if not obj: return
        try:
            f = getattr(obj,name)
            return f(*args,**keys)
        except AttributeError:
            return g.trace("%s component has no '%s' method" % (
                self.statusLineComponentName,name))
    
    def createStatusLine (self):
        self.callStatus('show')
        return self.getStatusObject() # For compatibility.
    
    def clearStatusLine (self):
        return self.callStatus('clear')
        
    def disableStatusLine (self,background=None):
        return self.callStatus('disable',background)
    
    def enableStatusLine (self,background="white"):
        return self.callStatus('enable',background)
    
    def getStatusLine (self):
        return self.callStatus('get')
        
    def putStatusLine (self,s,color=None):
        return self.callStatus('put',s,color)
        
    def setFocusStatusLine (self):
        return self.callStatus('setFocus')
    
    def statusLineIsEnabled(self):
        return self.callStatus('isEnabled')
    #@nonl
    #@-node:ekr.20041223105114.1:Status line methods (compatibility)
    #@+node:ekr.20031218072017.3967:Configuration (tkFrame)
    #@+node:ekr.20031218072017.3968:configureBar
    def configureBar (self,bar,verticalFlag):
        
        c = self.c
    
        # Get configuration settings.
        w = c.config.getInt("split_bar_width")
        if not w or w < 1: w = 7
        relief = c.config.get("split_bar_relief","relief")
        if not relief: relief = "flat"
        color = c.config.getColor("split_bar_color")
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
        
        c = self.c
    
        w = c.config.getInt("split_bar_width")
        if not w or w < 1: w = 7
        
        relief = c.config.get("split_bar_relief","relief")
        if not relief or relief == "": relief = "flat"
    
        color = c.config.getColor("split_bar_color")
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
        
        frame.tree.setFontFromConfig()
        frame.tree.setColorFromConfig()
        
        frame.configureBarsFromConfig()
        
        frame.body.setFontFromConfig()
        frame.body.setColorFromConfigt()
        
        frame.setTabWidth(c.tab_width)
        frame.log.setFontFromConfig()
        frame.log.setColorFromConfig()
    
        c.redraw()
    #@nonl
    #@-node:ekr.20031218072017.2246:reconfigureFromConfig
    #@+node:ekr.20031218072017.1625:setInitialWindowGeometry
    def setInitialWindowGeometry(self):
        
        """Set the position and size of the frame to config params."""
        
        c = self.c
    
        h = c.config.getInt("initial_window_height")
        w = c.config.getInt("initial_window_width")
        x = c.config.getInt("initial_window_left")
        y = c.config.getInt("initial_window_top")
        
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
    #@+node:ekr.20031218072017.1540:f.setWrap
    def setWrap (self,p):
        
        c = self.c
        theDict = g.scanDirectives(c,p)
        if not theDict: return
        
        wrap = theDict.get("wrap")
        if self.body.wrapState == wrap: return
    
        self.body.wrapState = wrap
        # g.trace(wrap)
        if wrap:
            self.bodyCtrl.configure(wrap="word")
            self.bodyXBar.pack_forget()
        else:
            self.bodyCtrl.configure(wrap="none")
            # Bug fix: 3/10/05: We must unpack the text area to make the scrollbar visible.
            self.bodyCtrl.pack_forget()
            self.bodyXBar.pack(side="bottom", fill="x")
            self.bodyCtrl.pack(expand=1,fill="both")
    #@nonl
    #@-node:ekr.20031218072017.1540:f.setWrap
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
        
        if use_Pmw and Pmw:
            return
        
        c = self.c
        
        border = c.config.getInt('additional_body_text_border')
        if border == None: border = 0
        
        # The body pane needs a _much_ bigger border when tiling horizontally.
        border = g.choose(self.splitVerticalFlag,2+border,6+border)
        self.bodyCtrl.configure(bd=border)
        
        # The log pane needs a slightly bigger border when tiling vertically.
        border = g.choose(self.splitVerticalFlag,4,2) 
        self.log.configureBorder(border)
    #@-node:ekr.20031218072017.3970:reconfigurePanes (use config bar_width)
    #@-node:ekr.20031218072017.3967:Configuration (tkFrame)
    #@+node:ekr.20031218072017.3971:Event handlers (tkFrame)
    #@+node:ekr.20031218072017.3972:frame.OnCloseLeoEvent
    # Called from quit logic and when user closes the window.
    # Returns True if the close happened.
    
    def OnCloseLeoEvent(self):
    
        g.app.closeLeoWindow(self)
    #@nonl
    #@-node:ekr.20031218072017.3972:frame.OnCloseLeoEvent
    #@+node:ekr.20031218072017.3973:frame.OnControlKeyUp/Down
    def OnControlKeyDown (self,event=None):
        
        __pychecker__ = '--no-argsused' # event not used.
        
        self.controlKeyIsDown = True
        
    def OnControlKeyUp (self,event=None):
        
        __pychecker__ = '--no-argsused' # event not used.
    
        self.controlKeyIsDown = False
    #@nonl
    #@-node:ekr.20031218072017.3973:frame.OnControlKeyUp/Down
    #@+node:ekr.20031218072017.3975:OnActivateBody (tkFrame)
    def OnActivateBody (self,event=None):
        
        __pychecker__ = '--no-argsused' # event not used.
    
        try:
            frame = self ; gui = g.app.gui
            g.app.setLog(frame.log,"OnActivateBody")
            w = gui.get_focus(frame)
            if w != frame.body.bodyCtrl:
                self.tree.OnDeactivate()
            self.bodyWantsFocus(self.bodyCtrl,tag='OnActivateBody')
        except:
            g.es_event_exception("activate body")
    #@nonl
    #@-node:ekr.20031218072017.3975:OnActivateBody (tkFrame)
    #@+node:ekr.20031218072017.2253:OnActivateLeoEvent, OnDeactivateLeoEvent
    def OnActivateLeoEvent(self,event=None):
        
        __pychecker__ = '--no-argsused' # event not used.
        
        # g.trace(self.c.shortFileName())
    
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
        
        __pychecker__ = '--no-argsused' # event not used.
    
        try:
            frame = self
            g.app.setLog(frame.log,"OnActivateTree")
            if 0: # Do NOT do this here!
                # OnActivateTree can get called when the tree gets DE-activated!!
                frame.bodyWantsFocus(frame.bodyCtrl,tag='OnActivateTree')
                
        except:
            g.es_event_exception("activate tree")
    #@-node:ekr.20031218072017.3976:OnActivateTree
    #@+node:ekr.20031218072017.3977:OnBodyClick, OnBodyRClick (Events)
    def OnBodyClick (self,event=None):
    
        try:
            c = self.c ; v = c.currentVnode()
            if not g.doHook("bodyclick1",c=c,p=v,v=v,event=event):
                self.OnActivateBody(event=event)
            g.doHook("bodyclick2",c=c,p=v,v=v,event=event)
        except:
            g.es_event_exception("bodyclick")
    
    def OnBodyRClick(self,event=None):
        
        try:
            c = self.c ; v = c.currentVnode()
            if not g.doHook("bodyrclick1",c=c,p=v,v=v,event=event):
                pass # By default Leo does nothing.
            g.doHook("bodyrclick2",c=c,p=v,v=v,event=event)
        except:
            g.es_event_exception("iconrclick")
    #@nonl
    #@-node:ekr.20031218072017.3977:OnBodyClick, OnBodyRClick (Events)
    #@+node:ekr.20031218072017.3978:OnBodyDoubleClick (Events)
    def OnBodyDoubleClick (self,event=None):
    
        try:
            c = self.c ; v = c.currentVnode()
            if not g.doHook("bodydclick1",c=c,p=v,v=v,event=event):
                if event: # 8/4/02: prevent wandering insertion point.
                    index = "@%d,%d" % (event.x, event.y) # Find where we clicked.
                    event.widget.tag_add('sel', 'insert wordstart', 'insert wordend')
                body = self.bodyCtrl
                start = body.index(index + " wordstart")
                end = body.index(index + " wordend")
                self.body.setTextSelection(start,end)
            g.doHook("bodydclick2",c=c,p=v,v=v,event=event)
        except:
            g.es_event_exception("bodydclick")
            
        return "break" # Restore this to handle proper double-click logic.
    #@nonl
    #@-node:ekr.20031218072017.3978:OnBodyDoubleClick (Events)
    #@+node:ekr.20031218072017.1803:OnMouseWheel (Tomaz Ficko)
    # Contributed by Tomaz Ficko.  This works on some systems.
    # On XP it causes a crash in tcl83.dll.  Clearly a Tk bug.
    
    def OnMouseWheel(self, event=None):
    
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
    #@-node:ekr.20031218072017.3971:Event handlers (tkFrame)
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
            if 1: # New code in 4.4a1.
                tree.endEditLabel()
                tree.select(tree.editPosition())
            else: # Old code:
                tree.select(v)
                if v and len(v.t.vnodeList) > 0:
                    tree.force_redraw() # force a redraw of joined headlines.
    #@nonl
    #@-node:ekr.20031218072017.3981:abortEditLabelCommand
    #@+node:ekr.20031218072017.840:Cut/Copy/Paste (tkFrame)
    #@+node:ekr.20031218072017.841:f.cut methods
    
    
    #@+node:ekr.20051011072049:OnCut (no longer used)
    # No longer used.  Was called from tkBody.createBindings.
    
    def OnCut (self,event=None):
        
        """The handler for the virtual Cut event."""
        
        __pychecker__ = '--no-argsused' # event not used.
        
        f = self ; c = f.c
        
        if 0: # g.app.gui.win32clipboard is always None.
            if g.app.gui.win32clipboard:
                data = f.body.getSelectedText()
                if data:
                    g.app.gui.replaceClipboardWith(data)
    
        # Activate the body key handler by hand.
        f.body.forceFullRecolor()
        f.body.onBodyWillChange(c.currentPosition(),"Cut")
    #@nonl
    #@-node:ekr.20051011072049:OnCut (no longer used)
    #@+node:ekr.20051011072049.1:OnCutFromMenu
    def OnCutFromMenu (self):
        
        ''' Called **only** when invoked using the menu instead of a shortcut.
        menu.createMenuEntries contains a horrible kludge to make this happen.'''
        
        f = self ; c = f.c ; w = f.getFocus()
        isBody = w == f.body.bodyCtrl
        # g.trace('isBody',isBody)
    
        if isBody:
            w.event_generate(g.virtual_event_name("Cut"))
        else:
            # Necessary
            w.event_generate(g.virtual_event_name("Cut"))
            f.tree.onHeadChanged(c.currentPosition())
    #@nonl
    #@-node:ekr.20051011072049.1:OnCutFromMenu
    #@+node:ekr.20051011072049.2:cutText
    def cutText (self):
        
        '''Invoked from the mini-buffer and from shortcuts.'''
        
        f = self ; c = f.c ; w = f.getFocus()
        isBody = w == f.body.bodyCtrl
        #g.trace('isBody',isBody)
    
        if isBody:
            w.event_generate(g.virtual_event_name("Cut"))
        else:
            f.tree.onHeadChanged(c.currentPosition())
    #@nonl
    #@-node:ekr.20051011072049.2:cutText
    #@-node:ekr.20031218072017.841:f.cut methods
    #@+node:ekr.20031218072017.842:f.copy methods
    #@+node:ekr.20051011072903:OnCopy (no longer used)
    # No longer used.  Was called from tkBody.createBindings.
    
    def OnCopy (self,event=None):
        
        __pychecker__ = '--no-argsused' # event not used.
    
        if 0: # g.app.gui.win32clipboard is always None.
            f = self
            if g.app.gui.win32clipboard:
                data = f.body.getSelectedText()
                if data:
                    g.app.gui.replaceClipboardWith(data)
            
        # Copy never changes dirty bits or syntax coloring.
        
    #@-node:ekr.20051011072903:OnCopy (no longer used)
    #@+node:ekr.20051011072903.1:OnCopyFromMenu
    def OnCopyFromMenu (self):
        
        ''' Called **only** when invoked using the menu instead of a shortcut.
        menu.createMenuEntries contains a horrible kludge to make this happen.'''
        
        f = self ; c = f.c ; w = f.getFocus()
        isBody = w == f.body.bodyCtrl
        # g.trace('isBody',isBody,'isMenu',isMenu)
    
        if isBody:
            w.event_generate(g.virtual_event_name("Copy"))
        else:
            # Necessary when not using shortcut keys.
            w.event_generate(g.virtual_event_name("Copy"))
    #@nonl
    #@-node:ekr.20051011072903.1:OnCopyFromMenu
    #@+node:ekr.20051011072903.2:copyText
    def copyText (self):
        
        '''Invoked from the mini-buffer and from shortcuts.'''
        
        f = self ; c = f.c ; w = f.getFocus()
        isBody = w == f.body.bodyCtrl
        # g.trace('isBody',isBody)
    
        if isBody:
            w.event_generate(g.virtual_event_name("Copy"))
        else:
            pass
    
    #@-node:ekr.20051011072903.2:copyText
    #@-node:ekr.20031218072017.842:f.copy methods
    #@+node:ekr.20031218072017.843:f.OnPaste & OnPasteFromMenu & pasteText
    #@+node:ekr.20051011072903.3:OnPaste (no longer used)
    # No longer used.  Was called from tkBody.createBindings.
    
    def OnPaste (self,event=None):
        
        __pychecker__ = '--no-argsused' # event not used.
        
        f = self ; c = f.c
      
        if 0: # sys.platform=="linux2": # ??? workaround paste problems on Linux.
            bodyCtrl = f.body.bodyCtrl
            s = bodyCtrl.selection_get( selection='CLIPBOARD' )
            bodyCtrl.insert('insert', s)
            bodyCtrl.event_generate('<Key>')
            bodyCtrl.update_idletasks()
        else:
            # Activate the body key handler by hand.
            f.body.forceFullRecolor()
            f.body.onBodyWillChange(c.currentPosition(),"Paste")
        
    #@-node:ekr.20051011072903.3:OnPaste (no longer used)
    #@+node:ekr.20051011072903.4:OnPasteFromMenu
    def OnPasteFromMenu (self):
        
        ''' Called **only** when invoked using the menu instead of a shortcut.
        menu.createMenuEntries contains a horrible kludge to make this happen.'''
        
        f = self ; c = f.c ; w = f.getFocus()
    
        w = self.getFocus()
        isBody = w == f.body.bodyCtrl
        # g.trace('isBody',isBody,'isMenu',isMenu)
    
        if isBody:
            w.event_generate(g.virtual_event_name("Paste"))
        else:
            w.event_generate(g.virtual_event_name("Paste"))
            f.tree.onHeadChanged(c.currentPosition())
    #@nonl
    #@-node:ekr.20051011072903.4:OnPasteFromMenu
    #@+node:ekr.20051011072903.5:pasteText
    def pasteText (self):
        
        '''This should be called **only** when invoked using the menu.
        menu.createMenuEntries contains a horrible kludge to make this happen.'''
        
        f = self ; c = f.c ; w = f.getFocus()
        isBody = w == f.body.bodyCtrl
        # g.trace('isBody',isBody)
    
        if isBody:
            w.event_generate(g.virtual_event_name("Paste"))
        else:
            # Do **not** call w.event_generate here.
            f.tree.onHeadChanged(c.currentPosition())
    #@nonl
    #@-node:ekr.20051011072903.5:pasteText
    #@-node:ekr.20031218072017.843:f.OnPaste & OnPasteFromMenu & pasteText
    #@-node:ekr.20031218072017.840:Cut/Copy/Paste (tkFrame)
    #@+node:ekr.20031218072017.3982:endEditLabelCommand
    def endEditLabelCommand (self):
    
        frame = self ; c = frame.c ; tree = frame.tree
        
        if g.app.batchMode:
            c.notValidInBatchMode("End Edit Headline")
            return
            
        if 1: # New code in 4.4a1.
            tree.endEditLabel()
            tree.select(tree.editPosition())
        else:
            v = frame.tree.editPosition()
            # g.trace(v)
            if v and v.edit_text():
                tree.select(v)
            if v: # Bug fix 10/9/02: also redraw ancestor headlines.
                tree.force_redraw() # force a redraw of joined headlines.
    
        frame.bodyWantsFocus(frame.bodyCtrl,tag='body:endEditLabelCommand')
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
        
        frame = self
    
        # Toggle the focus immediately.
        if g.app.gui.get_focus(self) == frame.bodyCtrl:
            frame.treeWantsFocus(frame.canvas,later=False,tag='toggleActivePane')
        else:
            frame.bodyWantsFocus(frame.bodyCtrl,later=False,tag='toggleActivePane')
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
    
        
        self.minimize(g.app.pythonFrame)
        for frame in g.app.windowList:
            self.minimize(frame)
            self.minimize(frame.findPanel)
        
    def minimize(self, frame):
    
        if frame and frame.top.state() == "normal":
            frame.top.iconify()
    #@nonl
    #@-node:ekr.20031218072017.3989:minimizeAll
    #@+node:ekr.20031218072017.3990:toggleSplitDirection (tkFrame)
    # The key invariant: self.splitVerticalFlag tells the alignment of the main splitter.
    
    def toggleSplitDirection(self):
        
        # Switch directions.
        c = self.c
        self.splitVerticalFlag = not self.splitVerticalFlag
        orientation = g.choose(self.splitVerticalFlag,"vertical","horizontal")
        c.config.set("initial_splitter_orientation","string",orientation)
        
        if use_Pmw and Pmw:
            self.togglePmwSplitDirection(self.splitVerticalFlag)
        else:
            self.toggleTkSplitDirection(self.splitVerticalFlag)
    #@nonl
    #@+node:ekr.20041221122440.1:togglePmwSplitDirection
    #@+at 
    #@nonl
    # Alas, there seems to be is no way to
    # a) change the orientation of a Pmw.PanedWidget, or
    # b) change the parent of a widget.
    # Therefore, we must recreate all widgets to toggle the orientation!
    #@-at
    #@@c
    
    def togglePmwSplitDirection (self,verticalFlag):
        
        __pychecker__ = '--no-argsused' # verticalFlag not used.
        
        frame = self ; c = self.c ; p = c.currentPosition()
        
        for name in ('splitter1','splitter2'):
            splitter = self.component(name).getObject()
            splitter.pack_forget()
    
        # Remember the contents of the log, including most tags.
        d = self.log.saveAllState()
    
        # Recreate everything: similar to code in finishCreate.
        self.createLeoSplitters(self.outerFrame)
        frame.canvas = self.createCanvas(self.split2Pane1) # Also packs canvas
        frame.tree  = leoTkinterTree.leoTkinterTree(c,frame,frame.canvas)
        frame.log   = leoTkinterLog(frame,self.split2Pane2)
        frame.body  = leoTkinterBody(frame,self.split1Pane2)
        
        # A kludge: reset this "official" ivar.
        frame.bodyCtrl = frame.body.bodyCtrl
    
        # Configure: similar to code in finishCreate.
        frame.setTabWidth(c.tab_width)
        frame.tree.setColorFromConfig()
        self.reconfigurePanes()
        self.body.setFontFromConfig()
        self.body.setColorFromConfig()
    
        # Restore everything.
        g.app.setLog(self.log)
        frame.log.restoreAllState(d)
        c.selectPosition(p)
        c.redraw()
    #@nonl
    #@-node:ekr.20041221122440.1:togglePmwSplitDirection
    #@+node:ekr.20041221122440.2:toggleTkSplitDirection
    def toggleTkSplitDirection (self,verticalFlag):
    
        # Abbreviations.
        frame = self
        bar1 = self.bar1 ; bar2 = self.bar2
        split1Pane1,split1Pane2 = self.split1Pane1,self.split1Pane2
        split2Pane1,split2Pane2 = self.split2Pane1,self.split2Pane2
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
    #@-node:ekr.20041221122440.2:toggleTkSplitDirection
    #@-node:ekr.20031218072017.3990:toggleSplitDirection (tkFrame)
    #@+node:EKR.20040422130619:resizeToScreen
    def resizeToScreen (self):
        
        top = self.top
        
        w = top.winfo_screenwidth()
        h = top.winfo_screenheight()
    
        if 1: # Fill the entire screen (almost)
            # This works well on Windows.  YMMV for other platforms.
            geom = "%dx%d%+d%+d" % (w-8,h-46,0,0)
        else: # The old way.
            geom = "%dx%d%+d%+d" % (w-20,h-55,10,25)
    
        top.geometry(geom)
    #@nonl
    #@-node:EKR.20040422130619:resizeToScreen
    #@-node:ekr.20031218072017.3984:Window Menu...
    #@+node:ekr.20031218072017.3991:Help Menu...
    #@+node:ekr.20031218072017.3992:leoHelp
    def leoHelp (self):
        
        frame = self ; c = frame.c
        
        theFile = g.os_path_join(g.app.loadDir,"..","doc","sbooks.chm")
    
        if g.os_path_exists(theFile):
            os.startfile(theFile)
        else:	
            answer = g.app.gui.runAskYesNoDialog(c,
                "Download Tutorial?",
                "Download tutorial (sbooks.chm) from SourceForge?")
    
            if answer == "yes":
                try:
                    if 0: # Download directly.  (showProgressBar needs a lot of work)
                        url = "http://umn.dl.sourceforge.net/sourceforge/leo/sbooks.chm"
                        import urllib
                        self.scale = None
                        urllib.urlretrieve(url,theFile,self.showProgressBar)
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
    #@+node:ekr.20050120083053:Delayed Focus (tkFrame)
    #@+at
    # 
    # New in 4.3
    # 
    # Rather than calling g.app.gui.set_focus directly, the code calls
    # self.xWantsFocus. This defers to idle-time code in the status-line 
    # class.
    # 
    # N.B.  This code never calls select, so there can be no race condition 
    # here that alters text improperly.
    #@-at
    #@nonl
    #@+node:ekr.20050120092028:xWantsFocus (tkFrame)
    #@+at 
    #@nonl
    # All these do the same thing, but separate names are good for tracing and
    # makes the intent of the code clearer.
    #@-at
    #@@c 
    
    def bodyWantsFocus(self,widget,later=True,tag=''):
        # g.trace(tag,self.c.shortFileName())
        self.set_focus(widget,later=later,tag=tag)
        
    def logWantsFocus(self,widget,later=True,tag=''):
        # g.trace(tag)
        self.set_focus(widget,later=later,tag=tag)
        
    def statusLineWantsFocus(self,widget,later=True,tag=''):
        # g.trace(tag)
        self.set_focus(widget,later=later,tag=tag)
        
    def treeWantsFocus(self,widget,later=True,tag=''):
        # g.trace(tag,repr(widget))
        self.set_focus(widget,later=later,tag=tag)
        
    def widgetWantsFocus(self,widget,later=True,tag=''):
        # g.trace(tag,repr(widget))
        self.set_focus(widget,later=later,tag=tag)
    #@nonl
    #@-node:ekr.20050120092028:xWantsFocus (tkFrame)
    #@+node:ekr.20050120092028.1:set_focus (tkFrame)
    #@+at
    # Very tricky code:
    # Many Tk calls can mess with the focus, so we must always set the focus,
    # regardless of what we did previously.
    # 
    # Alas, because of bugs in Tk and/or window managers, we can not call 
    # method at
    # idle time: that would interfere with switching between windows. Instead, 
    # the
    # xWnatFocus routines call this with later=True, to queue up a ONE-SHOT 
    # later call
    # to g.app.g.app.gui.set_focus.
    #@-at
    #@@c
    
    def set_focus(self,widget,later=False,tag=''):
        
        '''Set the focus to the widget specified in the xWantsFocus methods.'''
        
        __pychecker__ = '--no-argsused' # tag good for debugging.
    
        c = self.c
        # g.trace(tag) # c.shortFileName())
    
        if widget and not g.app.unitTesting:
            # Messing with focus may be dangerous in unit tests.
            if later:
                # Queue up the call (just once) for later.
                def setFocusCallback(c=c):
                    self.wantedCallbackScheduled = False
                    if c == g.app.wantedCommander and c.frame.wantedWidget:
                        # g.trace(c.frame.wantedWidget)
                        g.app.gui.set_focus(
                            g.app.wantedCommander,
                            c.frame.wantedWidget,
                            tag='frame.setFocus')
                    self.wantedWidget = None
                    g.app.wantedCommander = None
                        
                # Crucial: This may change what the callback does.
                self.wantedWidget = widget
                g.app.wantedCommander = c
                if not self.wantedCallbackScheduled:
                    # g.trace(tag,c.shortFileName())
                    self.wantedCallbackScheduled = True
                    # We don't have to wait so long now that we don't call this so often.
                    # The difference between 500 msec. and 100 msec. is significant.
                    # New in 4.4: set the delay to 1 msec.: the smaller the better.
                    self.outerFrame.after(1,setFocusCallback)
            else:
                # g.trace(tag,c.shortFileName())
                g.app.gui.set_focus(c,widget,tag='frame.setFocus')
                # Crucial: cancel any previous callback.
                # It may be re-enabled later, but that doesn't matter.
                self.wantedWidget = None
                g.app.wantedCommander = None
        else:
            # Cancel any previous request.
            self.wantedWidget = None
            g.app.wantedCommander = None
    #@nonl
    #@-node:ekr.20050120092028.1:set_focus (tkFrame)
    #@-node:ekr.20050120083053:Delayed Focus (tkFrame)
    #@+node:ekr.20031218072017.3995:Tk bindings...
    def bringToFront (self):
        self.top.deiconify()
        self.top.lift()
    
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
    #@nonl
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
        
        c = self.c
    
        self.bodyCtrl = self.createControl(frame,parentFrame)
    
        self.colorizer = leoColor.colorizer(c)
    #@nonl
    #@-node:ekr.20031218072017.2182:tkBody. __init__
    #@+node:ekr.20031218072017.838:tkBody.createBindings
    def createBindings (self,frame):
        
        '''(tkBody) Create gui-dependent bindings.
        These are *not* made in nullBody instances.'''
        
        c = self.c ; t = self.bodyCtrl
        
        # Event handlers...
        t.bind("<Button-1>", frame.OnBodyClick)
        if sys.platform == "win32":
            # Support Linux middle-button paste easter egg.
            t.bind("<Button-2>", frame.OnPaste)
        t.bind("<Button-3>", frame.OnBodyRClick)
        t.bind("<Double-Button-1>", frame.OnBodyDoubleClick)
        
        if 0: # The changeover to the mini-buffer code is complete.
            g.trace('binding <Key> to frame.body.onBodyKey')
            t.bind("<Key>", self.onBodyKey)
    
        # Gui-dependent bindings...
        if 0:
            # These cause problems when cut/copy/paste-text commands are bound.
            t.bind(g.virtual_event_name("Cut"), frame.OnCut)
            t.bind(g.virtual_event_name("Copy"), frame.OnCopy)
            t.bind(g.virtual_event_name("Paste"), frame.OnPaste)
    #@nonl
    #@-node:ekr.20031218072017.838:tkBody.createBindings
    #@+node:ekr.20031218072017.3998:tkBody.createControl
    def createControl (self,frame,parentFrame):
        
        c = self.c
    
        wrap = c.config.getBool('body_pane_wraps')
        wrap = g.choose(wrap,"word","none")
        
        # Setgrid=1 cause severe problems with the font panel.
        body = Tk.Text(parentFrame,name='body',
            bd=2,bg="white",relief="flat",setgrid=0,wrap=wrap)
        
        bodyBar = Tk.Scrollbar(parentFrame,name='bodyBar')
        frame.bodyBar = self.bodyBar = bodyBar
        body['yscrollcommand'] = bodyBar.set
        bodyBar['command'] = body.yview
        bodyBar.pack(side="right", fill="y")
        
        # Always create the horizontal bar.
        frame.bodyXBar = self.bodyXBar = bodyXBar = Tk.Scrollbar(
            parentFrame,name='bodyXBar',orient="horizontal")
        body['xscrollcommand'] = bodyXBar.set
        bodyXBar['command'] = body.xview
        self.bodyXbar = frame.bodyXBar = bodyXBar
        
        if wrap == "none":
            # g.trace(parentFrame)
            bodyXBar.pack(side="bottom", fill="x")
            
        body.pack(expand=1,fill="both")
    
        self.wrapState = wrap
    
        if 0: # Causes the cursor not to blink.
            body.configure(insertofftime=0)
            
        return body
    #@nonl
    #@-node:ekr.20031218072017.3998:tkBody.createControl
    #@-node:ekr.20031218072017.3997: Birth & death
    #@+node:ekr.20041217135735.1:tkBody.setColorFromConfig
    def setColorFromConfig (self):
        
        c = self.c ; body = self.bodyCtrl
            
        bg = c.config.getColor("body_text_background_color") or 'white'
        try: body.configure(bg=bg)
        except:
            g.es("exception setting body text background color")
            g.es_exception()
        
        fg = c.config.getColor("body_text_foreground_color") or 'black'
        try: body.configure(fg=fg)
        except:
            g.es("exception setting body textforeground color")
            g.es_exception()
    
        bg = c.config.getColor("body_insertion_cursor_color")
        if bg:
            try: body.configure(insertbackground=bg)
            except:
                g.es("exception setting body pane cursor color")
                g.es_exception()
            
        sel_bg = c.config.getColor('body_text_selection_background_color') or 'Gray80'
        try: body.configure(selectbackground=sel_bg)
        except Exception:
            g.es("exception setting body pane text selection background color")
            g.es_exception()
    
        sel_fg = c.config.getColor('body_text_selection_foreground_color') or 'white'
        try: body.configure(selectforeground=sel_fg)
        except Exception:
            g.es("exception setting body pane text selection foreground color")
            g.es_exception()
      
        if sys.platform != "win32": # Maybe a Windows bug.
            fg = c.config.getColor("body_cursor_foreground_color")
            bg = c.config.getColor("body_cursor_background_color")
            if fg and bg:
                cursor="xterm" + " " + fg + " " + bg
                try: body.configure(cursor=cursor)
                except:
                    import traceback ; traceback.print_exc()
    #@nonl
    #@-node:ekr.20041217135735.1:tkBody.setColorFromConfig
    #@+node:ekr.20031218072017.2183:tkBody.setFontFromConfig
    def setFontFromConfig (self):
    
        c = self.c ; body = self.bodyCtrl
        
        font = c.config.getFontFromParams(
            "body_text_font_family", "body_text_font_size",
            "body_text_font_slant",  "body_text_font_weight",
            c.config.defaultBodyFontSize, tag = "body")
        
        self.fontRef = font # ESSENTIAL: retain a link to font.
        body.configure(font=font)
    
        # g.trace("BODY",body.cget("font"),font.cget("family"),font.cget("weight"))
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
    #@+node:ekr.20031218072017.1321:idle_body_key & helpers
    def idle_body_key (self,p,oldSel,undoType,ch=None,oldYview=None,newSel=None,oldText=None):
        
        """Update the body pane at idle time."""
        
        __pychecker__ = 'maxlines=500'
    
        c = self.c
        if not c: return "break"
        if not p: return "break"
        if not c.isCurrentPosition(p): return "break"
        # g.trace(repr(ch))
    
        if g.doHook("bodykey1",c=c,p=p,v=p,ch=ch,oldSel=oldSel,undoType=undoType):
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
        # Make sure we handle delete key properly.
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
            #@        << handle special characters >>
            #@+node:ekr.20050526080309:<< handle special characters >>
            d = g.scanDirectives(c,p) # Support @tab_width directive properly.
            tab_width = d.get("tabwidth",c.tab_width) # ; g.trace(tab_width)
            
            if ch in ('\n','\r'):
                # Do nothing if we are in @nocolor mode or if we are executing a Change command.
                if self.frame.body.colorizer.useSyntaxColoring(p) and undoType != "Change":
                    removeTrailing = self.doAutoIndent(p,removeTrailing,tab_width,undoType)
            
            elif ch == '\t' and tab_width < 0:
                # Do nothing if we are executing a Change command.
                if undoType != "Change":
                    self.convertBlanksToTabs(tab_width)
            
            elif ch in (chr(8)) and tab_width < 0:
                #@    << handle backspace with negative tab_width >>
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
                            newSel = c.frame.body.getTextSelection() # Fixes crasher in undo logic.
                #@nonl
                #@-node:EKR.20040604090913:<< handle backspace with negative tab_width >>
                #@nl
            #@nonl
            #@-node:ekr.20050526080309:<< handle special characters >>
            #@nl
        #@    << set s to widget text, removing trailing newlines if necessary >>
        #@+node:ekr.20031218072017.1326:<< set s to widget text, removing trailing newlines if necessary >>
        s = c.frame.body.getAllText()
        if len(s) > 0 and s[-1] == '\n' and removeTrailing:
            s = s[:-1]
            
        # Major change: 6/12/04
        if s == body:
            # g.trace('no real change')
            return "break"
        #@nonl
        #@-node:ekr.20031218072017.1326:<< set s to widget text, removing trailing newlines if necessary >>
        #@nl
        # g.trace(repr(ch),undoType)
        if undoType:
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
        try:
            # Update dirty bits.
            if not p.isDirty() and p.setDirty(): # Sets all cloned and @file dirty bits
                redraw_flag = True
            # Update icons.
            val = p.computeIcon()
            # During unit tests the node may not have been drawn,
            # So p.v.iconVal may not exist yet.
            if not hasattr(p.v,"iconVal") or val != p.v.iconVal:
                p.v.iconVal = val
                redraw_flag = True
        finally:
            c.endUpdate(redraw_flag) # redraw only if necessary
        #@nonl
        #@-node:ekr.20031218072017.1328:<< redraw the screen if necessary >>
        #@nl
        g.doHook("bodykey2",c=c,p=p,v=p,ch=ch,oldSel=oldSel,undoType=undoType)
        return "break"
    #@nonl
    #@+node:ekr.20031218072017.1324:doAutoIndent (David McNab)
    def doAutoIndent (self,p,removeTrailing,tab_width,undoType):
        
        __pychecker__ = '--no-argsused' # 'undoType' unused, but must be present.
        
        c = self.c
        # Get the previous line.
        s=c.frame.bodyCtrl.get("insert linestart - 1 lines","insert linestart -1c")
        # g.trace(repr(s))
        # Add the leading whitespace to the present line.
        junk,width = g.skip_leading_ws_with_indent(s,0,tab_width)
        if s and len(s) > 0 and s[-1]==':':
            # For Python: increase auto-indent after colons.
            if self.colorizer.scanColorDirectives(p) == "python":
                width += abs(tab_width)
        if c.config.getBool("smart_auto_indent"):
            # Added Nov 18 by David McNab, david@rebirthing.co.nz
            # Determine if prev line has unclosed parens/brackets/braces
            brackets = [width] ; tabex = 0
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
            removeTrailing = False
                
        return removeTrailing
    #@nonl
    #@-node:ekr.20031218072017.1324:doAutoIndent (David McNab)
    #@+node:ekr.20031218072017.1325:convertBlanksToTabs
    def convertBlanksToTabs (self,tab_width):
    
        c = self.c
        
        # Get the characters preceeding the tab.
        prev=c.frame.bodyCtrl.get("insert linestart","insert -1c")
        
        if 1:
            #@        << convert tab no matter where it is >>
            #@+node:ekr.20050526081024:<< convert tab no matter where it is >>
            w = g.computeWidth(prev,tab_width)
            w2 = (abs(tab_width) - (w % abs(tab_width)))
            # g.trace("prev w:",w,"prev chars:",prev)
            c.frame.bodyCtrl.delete("insert -1c")
            c.frame.bodyCtrl.insert("insert",' ' * w2)
            #@nonl
            #@-node:ekr.20050526081024:<< convert tab no matter where it is >>
            #@nl
        else:
            #@        << convert only leading tabs >>
            #@+node:ekr.20050526081024.1:<< convert only leading tabs >>
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
            #@-node:ekr.20050526081024.1:<< convert only leading tabs >>
            #@nl
    #@nonl
    #@-node:ekr.20031218072017.1325:convertBlanksToTabs
    #@-node:ekr.20031218072017.1321:idle_body_key & helpers
    #@+node:ekr.20031218072017.1329:onBodyChanged (tkTree)
    # Called by command handlers that have already changed the text.
    
    def onBodyChanged (self,p,undoType,oldSel=None,oldYview=None,newSel=None,oldText=None):
        
        """Handle a change to the body pane."""
        
        c = self.c
        if not p:
            p = c.currentPosition()
    
        if not oldSel:
            oldSel = c.frame.body.getTextSelection()
    
        self.c.frame.body.colorizer.interrupt()
        self.idle_body_key(p,oldSel,undoType,oldYview=oldYview,newSel=newSel,oldText=oldText)
    #@nonl
    #@-node:ekr.20031218072017.1329:onBodyChanged (tkTree)
    #@+node:ekr.20031218072017.1330:onBodyKey
    def onBodyKey (self,event,undoType='Typing'):
        
        '''Handle any key press event in the body pane.'''
    
        # New in Leo 4.4.  May be called with event = None
        c = self.c
        ch = (event and event.char) or ''
        keysym = (event and event.keysym) or ''
    
        # g.trace(repr(ch),repr(event.keysym))
    
        # This translation is needed on MacOS.
        if ch == '':
            d = {'Return':'\r', 'Tab':'\t', 'BackSpace':chr(8)}
            ch = d.get(event.keysym,'')
    
        oldSel = c.frame.body.getTextSelection()
        
        p = c.currentPosition()
            
        # We must execute this even if len(ch) > 0 to delete spurious trailing newlines.
        self.c.frame.body.colorizer.interrupt()
        self.c.frame.bodyCtrl.after_idle(self.idle_body_key,p,oldSel,undoType,ch)
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
    
        self.c.frame.body.colorizer.interrupt()
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
    #@+node:ekr.20031218072017.4006:Indices (leoTkinterBody)
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
    #@-node:ekr.20031218072017.4006:Indices (leoTkinterBody)
    #@+node:ekr.20031218072017.4013:Insert point
    #@+node:ekr.20050710102922:get/setPythonInsertionPoint
    def getPythonInsertionPoint (self,t=None,s=None):
        
        b = self
        if t is None: t = self.bodyCtrl
        if s is None: s = t.get('1.0','end')
        i = t.index("insert")
        row,col = b.convertIndexToRowColumn(i)
        
        return g.convertRowColToPythonIndex(s,row-1,col)
        
    def setPythonInsertionPoint (self,i,t=None,s=None):
        
        if t is None: t = self.bodyCtrl
        if s is None: s = t.get('1.0','end')
        row,col = g.convertPythonIndexToRowCol(s,i)
        t.mark_set( 'insert','%d.%d' % (row+1,col))
    #@nonl
    #@-node:ekr.20050710102922:get/setPythonInsertionPoint
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
    def deleteTextSelection (self):
        
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
    #@+node:ekr.20050710104804:getPythonTextSelection
    def getPythonTextSelection (self):
        
        """Return a tuple representing the selected range of body text.
        
        Return a tuple giving the insertion point if no range of text is selected."""
    
        b = self ; t = self.bodyCtrl
        sel = t.tag_ranges("sel")
    
        if len(sel) == 2:
            s = t.get('1.0','end')
            i,j = sel
            row,col = b.convertIndexToRowColumn(i)
            i1 = g.convertRowColToPythonIndex(s,row-1,col)
            row,col = b.convertIndexToRowColumn(j)
            i2 = g.convertRowColToPythonIndex(s,row-1,col)
            return i1,i2
        else:
            # Return the insertion point if there is no selected text.
            i = self.getPythonTextSelection()
            return i,i
    #@nonl
    #@-node:ekr.20050710104804:getPythonTextSelection
    #@+node:ekr.20050710104804.1:setPythonTextSelection
    def setPythonTextSelection(self,i,j):
    
        t = self.bodyCtrl
        s = t.get('1.0','end')
        row,col = g.convertPythonIndexToRowCol(s,i)
        i1 = '%d.%d' % (row+1,col)
        row,col = g.convertPythonIndexToRowCol(s,j)
        i2 = '%d.%d' % (row+1,col)
        g.app.gui.setTextSelection(self.bodyCtrl,i1,i2)
    #@nonl
    #@-node:ekr.20050710104804.1:setPythonTextSelection
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
    #@+node:ekr.20051016095907:tkLog Birth
    #@+node:ekr.20031218072017.4040:tkLog.__init__
    def __init__ (self,frame,parentFrame):
        
        # g.trace("leoTkinterLog")
        
        self.c = c = frame.c # Also set in the base constructor, but we need it here.
        
        self.colorTags = []
            # The list of color names used as tags in present tab.
            # This gest switched by selectTab.
    
        self.wrap = g.choose(c.config.getBool('log_pane_wraps'),"word","none")
        
        # New in 4.4a2: The log pane is a Pmw.Notebook...
    
        self.nb = None      # The Pmw.Notebook that holds all the tabs.
        self.colorTagsDict = {} # Keys are page names.  Values are saved colorTags lists.
        self.frameDict = {}  # Keys are page names. Values are Tk.Frames.
        self.tabMenu = None # A menu that pops up on right clicks in the hull or in tabs.
        self.textDict = {}  # Keys are page names. Values are Tk.Text widgets.
        self.newTabCount = 0 # Number of new tabs created.
        
        # Official status variables.  Can be used by client code.
        self.tabName = None # The name of the active tab.
        self.logCtrl = None # Same as self.textDict.get(self.tabName)
        self.tabFrame = None # Same as self.frameDict.get(self.tabName)
        
        # Call the base class constructor and calls createControl.
        leoFrame.leoLog.__init__(self,frame,parentFrame)
    #@-node:ekr.20031218072017.4040:tkLog.__init__
    #@+node:ekr.20031218072017.4042:tkLog.createControl
    def createControl (self,parentFrame):
    
        c = self.c
    
        self.nb = Pmw.NoteBook(parentFrame,
            borderwidth = 1, pagemargin = 0,
            raisecommand = self.raiseTab,
            lowercommand = self.lowerTab
        )
    
        menu = self.makeTabMenu(tabName=None)
    
        def hullMenuCallback(event):
            self.onRightClick(event,menu)
    
        self.nb.bind('<Button-3>',hullMenuCallback)
    
        self.nb.pack(fill='both',expand=1)
        self.selectTab('Log') # create the tab and make it the active tab.
        return self.logCtrl
    #@-node:ekr.20031218072017.4042:tkLog.createControl
    #@+node:ekr.20051016103459:tkLog.createTextWidget
    def createTextWidget (self,parentFrame):
        
        log = Tk.Text(parentFrame,name="log",
            setgrid=0,wrap=self.wrap,bd=2,bg="white",relief="flat")
        
        logBar = Tk.Scrollbar(parentFrame,name="logBar")
    
        log['yscrollcommand'] = logBar.set
        logBar['command'] = log.yview
        
        logBar.pack(side="right", fill="y")
        # rr 8/14/02 added horizontal elevator 
        if self.wrap == "none": 
            logXBar = Tk.Scrollbar( 
                parentFrame,name='logXBar',orient="horizontal") 
            log['xscrollcommand'] = logXBar.set 
            logXBar['command'] = log.xview 
            logXBar.pack(side="bottom", fill="x")
        log.pack(expand=1, fill="both")
    
        return log
    #@nonl
    #@-node:ekr.20051016103459:tkLog.createTextWidget
    #@+node:ekr.20051019134106.1:tkLog.makeTabMenu
    def makeTabMenu (self,tabName=None):
    
        '''Create a tab popup menu.'''
    
        c = self.c
        hull = self.nb.component('hull') # A Tk.Canvas.
        
        menu = Tk.Menu(hull,tearoff=0)
        menu.add_command(label='New Tab',command=self.newTabFromMenu)
        
        if tabName:
            # Important: tabName is the name when the tab is created.
            # It is not affected by renaming, so we don't have to keep
            # track of the correspondence between this name and what is in the label.
            def deleteTabCallback():
                self.deleteTab(tabName)
    
            menu.add_command(label='Delete This Tab',command=deleteTabCallback)
     
            def renameTabCallback():
                self.renameTabFromMenu(tabName)
    
            menu.add_command(label='Rename This Tab',command=renameTabCallback)
    
        return menu
    #@nonl
    #@-node:ekr.20051019134106.1:tkLog.makeTabMenu
    #@-node:ekr.20051016095907:tkLog Birth
    #@+node:ekr.20051016095907.1:Config & get/saveState
    #@+node:ekr.20031218072017.4041:tkLog.configureBorder & configureFont
    def configureBorder(self,border):
        
        self.logCtrl.configure(bd=border)
        
    def configureFont(self,font):
    
        self.logCtrl.configure(font=font)
    #@nonl
    #@-node:ekr.20031218072017.4041:tkLog.configureBorder & configureFont
    #@+node:ekr.20031218072017.4043:tkLog.getFontConfig
    def getFontConfig (self):
    
        font = self.logCtrl.cget("font")
        # g.trace(font)
        return font
    #@nonl
    #@-node:ekr.20031218072017.4043:tkLog.getFontConfig
    #@+node:ekr.20041222043017:tkLog.restoreAllState
    def restoreAllState (self,d):
        
        '''Restore the log from a dict created by saveAllState.'''
        
        logCtrl = self.logCtrl
    
        # Restore the text.
        text = d.get('text')
        logCtrl.insert('end',text)
    
        # Restore all colors.
        colors = d.get('colors')
        for color in colors.keys():
            if color not in self.colorTags:
                self.colorTags.append(color)
                logCtrl.tag_config(color,foreground=color)
            items = list(colors.get(color))
            while items:
                start,stop = items[0],items[1]
                items = items[2:]
                logCtrl.tag_add(color,start,stop)
    #@nonl
    #@-node:ekr.20041222043017:tkLog.restoreAllState
    #@+node:ekr.20041222043017.1:tkLog.saveAllState
    def saveAllState (self):
        
        '''Return a dict containing all data needed to recreate the log in another widget.'''
        
        logCtrl = self.logCtrl ; colors = {}
    
        # Save the text
        text = logCtrl.get('1.0','end')
    
        # Save color tags.
        tag_names = logCtrl.tag_names()
        for tag in tag_names:
            if tag in self.colorTags:
                colors[tag] = logCtrl.tag_ranges(tag)
                
        d = {'text':text,'colors': colors}
        # g.trace('\n',g.dictToString(d))
        return d
    #@nonl
    #@-node:ekr.20041222043017.1:tkLog.saveAllState
    #@+node:ekr.20041217135735.2:tkLog.setColorFromConfig
    def setColorFromConfig (self):
        
        c = self.c
        
        bg = c.config.getColor("log_pane_background_color") or 'white'
        
        try:
            self.logCtrl.configure(bg=bg)
        except:
            g.es("exception setting log pane background color")
            g.es_exception()
    #@nonl
    #@-node:ekr.20041217135735.2:tkLog.setColorFromConfig
    #@+node:ekr.20031218072017.4046:tkLog.setFontFromConfig
    def setFontFromConfig (self):
    
        c = self.c ; logCtrl = self.logCtrl
    
        font = c.config.getFontFromParams(
            "log_text_font_family", "log_text_font_size",
            "log_text_font_slant",  "log_text_font_weight",
            c.config.defaultLogFontSize, tag = "log")
    
        self.fontRef = font # ESSENTIAL: retain a link to font.
        logCtrl.configure(font=font)
        
        # g.trace("LOG",logCtrl.cget("font"),font.cget("family"),font.cget("weight"))
    
        bg = c.config.getColor("log_text_background_color")
        if bg:
            try: logCtrl.configure(bg=bg)
            except: pass
        
        fg = c.config.getColor("log_text_foreground_color")
        if fg:
            try: logCtrl.configure(fg=fg)
            except: pass
    #@nonl
    #@-node:ekr.20031218072017.4046:tkLog.setFontFromConfig
    #@-node:ekr.20051016095907.1:Config & get/saveState
    #@+node:ekr.20051016095907.2:Focus & update
    #@+node:ekr.20031218072017.4045:tkLog.onActivateLog
    def onActivateLog (self,event=None):
        
        __pychecker__ = '--no-argsused' # event not used.
    
        try:
            g.app.setLog(self,"OnActivateLog")
            self.frame.tree.OnDeactivate()
            self.frame.logWantsFocus(self.logCtrl,tag='onActivateLog')
        except:
            g.es_event_exception("activate log")
    #@nonl
    #@-node:ekr.20031218072017.4045:tkLog.onActivateLog
    #@+node:ekr.20031218072017.4044:tkLog.hasFocus
    def hasFocus (self):
        
        return g.app.gui.get_focus(self.frame) == self.logCtrl
    #@nonl
    #@-node:ekr.20031218072017.4044:tkLog.hasFocus
    #@+node:ekr.20050208133438:forceLogUpdate
    def forceLogUpdate (self,s):
    
        if sys.platform == "darwin": # Does not work on MacOS X.
            try:
                print s, # Don't add a newline.
            except UnicodeError:
                # g.app may not be inited during scripts!
                print g.toEncodedString(s,'utf-8')
        else:
            self.frame.tree.disableRedraw = True
            self.logCtrl.update_idletasks()
            self.frame.tree.disableRedraw = False
    #@nonl
    #@-node:ekr.20050208133438:forceLogUpdate
    #@-node:ekr.20051016095907.2:Focus & update
    #@+node:ekr.20051016101927:put & putnl (LeoTkinterLog)
    #@+at 
    #@nonl
    # Printing uses self.logCtrl, so this code need not concern itself
    # with which tab is active.
    # 
    # Also, selectTab switches the contents of colorTags, so that is not 
    # concern.
    # It may be that Pmw will allow us to dispense with the colorTags logic...
    #@-at
    #@nonl
    #@+node:ekr.20031218072017.1473:put
    # All output to the log stream eventually comes here.
    def put (self,s,color=None,tabName='Log'):
        
        # print 'tkLog.put',self.c.shortFileName(),s,
    
        if g.app.quitting:
            return
        if tabName:
            self.selectTab(tabName)
        
        if self.logCtrl:
            #@        << put s to log control >>
            #@+node:EKR.20040423082910:<< put s to log control >>
            if 0:
                # Doing this here messes up the display in the log pane.
                if type(s) == type(u""):
                    s = g.toEncodedString(s,g.app.TkEncoding)
                    
            # g.trace(repr(self.logCtrl))
            
            if color:
                if color not in self.colorTags:
                    self.colorTags.append(color)
                    self.logCtrl.tag_config(color,foreground=color)
                self.logCtrl.insert("end",s)
                self.logCtrl.tag_add(color,"end-%dc" % (len(s)+1),"end-1c")
                self.logCtrl.tag_add("black","end")
            else:
                self.logCtrl.insert("end",s)
            
            self.logCtrl.see("end")
                
            self.forceLogUpdate(s)
            #@nonl
            #@-node:EKR.20040423082910:<< put s to log control >>
            #@nl
        else:
            #@        << put s to logWaiting and print s >>
            #@+node:EKR.20040423082910.1:<< put s to logWaiting and print s >>
            g.app.logWaiting.append((s,color),)
            
            print "Null tkinter log"
            
            if type(s) == type(u""):
                s = g.toEncodedString(s,"ascii")
            
            print s
            #@nonl
            #@-node:EKR.20040423082910.1:<< put s to logWaiting and print s >>
            #@nl
    #@nonl
    #@-node:ekr.20031218072017.1473:put
    #@+node:ekr.20051016101927.1:putnl
    def putnl (self,tabName='Log'):
    
        if g.app.quitting:
            return
        if tabName:
            self.selectTab(tabName)
        
        if self.logCtrl:
            self.logCtrl.insert("end",'\n')
            self.logCtrl.see("end")
            self.forceLogUpdate('\n')
        else:
            # Put a newline to logWaiting and print newline
            g.app.logWaiting.append(('\n',"black"),)
            print "Null tkinter log"
            print
    #@-node:ekr.20051016101927.1:putnl
    #@-node:ekr.20051016101927:put & putnl (LeoTkinterLog)
    #@+node:ekr.20051018061932:Tab (TkLog)
    #@+node:ekr.20051017212057:clearTab
    def clearTab (self,tabName):
        
        self.selectTab(tabName)
        t = self.logCtrl
        t.delete('1.0','end')
    #@nonl
    #@-node:ekr.20051017212057:clearTab
    #@+node:ekr.20051018102027:deleteTab
    def deleteTab (self,tabName):
        
        if tabName != 'Log' and tabName in self.nb.pagenames():
            self.nb.delete(tabName)
            self.colorTagsDict [tabName] = []
            self.textDict [tabName] = None
            self.frameDict [tabName] = None
            self.tabName = None
            self.selectTab('Log')
    #@nonl
    #@-node:ekr.20051018102027:deleteTab
    #@+node:ekr.20051018061932.1:ower/raiseTab
    def lowerTab (self,tabName):
        
        if tabName:
            b = self.nb.tab(tabName) # b is a Tk.Button.
            b.config(bg='grey80')
        
    def raiseTab (self,tabName):
    
        if tabName:
            b = self.nb.tab(tabName) # b is a Tk.Button.
            b.config(bg='LightSteelBlue1')
    #@nonl
    #@-node:ekr.20051018061932.1:ower/raiseTab
    #@+node:ekr.20051019170806:renameTab
    def renameTab (self,oldName,newName):
        
        label = self.nb.tab(oldName)
        label.configure(text=newName)
    #@nonl
    #@-node:ekr.20051019170806:renameTab
    #@+node:ekr.20051016101724.1:selectTab
    def selectTab (self,tabName):
    
        '''Create the tab if necessary and make it active.'''
        
        c = self.c ; tabFrame = self.frameDict.get(tabName)
        # g.trace(g.choose(tabName,'switching to','creating'),tabName)
        if tabFrame:
            # Switch to a new colorTags list.
            newColorTags = self.colorTagsDict.get(tabName)
            self.colorTagsDict [self.tabName] = self.colorTags [:]
            self.colorTags = newColorTags
        else:
            tabFrame = self.nb.add(tabName)
            #@        << bind a tab-specific pop-up menu to the tab >>
            #@+node:ekr.20051020075416:<< bind a tab-specific pop-up menu to the tab >>
            menu = self.makeTabMenu(tabName)
            tab = self.nb.tab(tabName)
            
            def menuClickCallback(event):
                self.onRightClick(event,menu)
            
            tab.bind('<Button-3>',menuClickCallback)
            #@nonl
            #@-node:ekr.20051020075416:<< bind a tab-specific pop-up menu to the tab >>
            #@nl
            #@        << Create the tab's text widget >>
            #@+node:ekr.20051018072306:<< Create the tab's text widget >>
            textWidget = self.createTextWidget(tabFrame)
            
            # Set the background color.
            configName = 'log_pane_%s_tab_background_color' % tabName
            bg = c.config.getColor(configName) or 'MistyRose1'
            try: textWidget.configure(bg=bg)
            except Exception: pass # Could be a user error.
            
            self.frameDict [tabName] = tabFrame
            self.textDict [tabName] = textWidget
            
            # Switch to a new colorTags list.
            if self.tabName:
                self.colorTagsDict [self.tabName] = self.colorTags [:]
            self.colorTags = ['black']
            self.colorTagsDict [tabName] = self.colorTags
            
            # Make the bindings.
            textWidget.bind("<Button-1>",self.onActivateLog)
            textWidget.tag_config('black',foreground='black')
            #@nonl
            #@-node:ekr.20051018072306:<< Create the tab's text widget >>
            #@nl
            # Update immediately so we can queue the request to change focus.
            tabFrame.update_idletasks()
            self.c.frame.bodyWantsFocus(self.c.frame.bodyCtrl,tag='tkLog.selectTab')
            
        self.nb.selectpage(tabName)
        # Update the status vars.
        self.tabName = tabName
        self.logCtrl = self.textDict.get(tabName)
        self.tabFrame = self.frameDict.get(tabName)
        # g.trace(self.tabName,repr(self.logCtrl))
        return tabFrame
    #@nonl
    #@-node:ekr.20051016101724.1:selectTab
    #@+node:ekr.20051019134106:Tab menu callbacks & helpers
    #@+node:ekr.20051019134422:onRightClick
    def onRightClick (self,event,menu):
    
        menu.post(event.x_root,event.y_root)
    #@nonl
    #@-node:ekr.20051019134422:onRightClick
    #@+node:ekr.20051019140004.1:newTabFromMenu
    def newTabFromMenu (self,tabName='Log'):
    
        self.selectTab(tabName)
        parentFrame = self.frameDict.get(tabName)
        
        # This is called by getTabName.
        def selectTabCallback (oldName,newName):
            self.selectTab(newName)
    
        self.getTabName(parentFrame,'',selectTabCallback)
    #@nonl
    #@-node:ekr.20051019140004.1:newTabFromMenu
    #@+node:ekr.20051019165401:renameTabFromMenu
    def renameTabFromMenu (self,tabName):
    
        if tabName in ('Log','Completions'):
            g.es('can not rename %s tab' % (tabName),color='blue')
        else:
            parentFrame = self.frameDict.get(tabName)
            self.getTabName(parentFrame,tabName,self.renameTab)
    #@nonl
    #@-node:ekr.20051019165401:renameTabFromMenu
    #@+node:ekr.20051019172811:getTabName
    def getTabName (self,parentFrame,tabName,exitCallback):
    
        f = Tk.Frame(parentFrame)
        f.pack(side='bottom',fill='x',expand=1)
    
        Tk.Label(f,text='Tab name').pack(side='left')
    
        e = Tk.Entry(f,background='white')
        e.pack(side='left')
    
        def getNameCallback (event=None):
            s = e.get().strip()
            f.pack_forget()
            if s: exitCallback(tabName,s)
        
        if 0:
            b = Tk.Button(row,text="Close",command=getNameCallback)
            b.pack(side='left')
    
        e.focus_force()
        e.bind('<Return>',getNameCallback)
    #@nonl
    #@-node:ekr.20051019172811:getTabName
    #@-node:ekr.20051019134106:Tab menu callbacks & helpers
    #@-node:ekr.20051018061932:Tab (TkLog)
    #@-others
#@nonl
#@-node:ekr.20031218072017.4039:class leoTkinterLog
#@-others
#@nonl
#@-node:ekr.20031218072017.3939:@thin leoTkinterFrame.py
#@-leo
