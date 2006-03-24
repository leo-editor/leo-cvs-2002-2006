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
    
        self.trace_status_line = None # Set in finishCreate.
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
        c.setLog()
        g.app.windowList.append(f)
        c.initVersion()
        c.signOnWithVersion()
        f.miniBufferWidget = f.createMiniBufferWidget()
        c.bodyWantsFocusNow()
        self.trace_status_line = c.config.getBool('trace_status_line')
        # f.enableTclTraces()
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
        if 0:
            f.top.bind("<Activate>",f.OnActivateLeoEvent)
            f.top.bind("<Deactivate>",f.OnDeactivateLeoEvent)
            f.top.bind("<Control-KeyPress>",f.OnControlKeyDown)
            f.top.bind("<Control-KeyRelease>",f.OnControlKeyUp)
        
        # Create the outer frame, the 'hull' component.
        f.outerFrame = Tk.Frame(top)
        f.outerFrame.pack(expand=1,fill="both")
        f.componentClass(c,'hull',f.outerFrame)
    #@nonl
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
        p = leoNodes.position(c,v,[])
        v.initHeadString("NewHeadline")
        p.moveToRoot()
        c.editPosition(p)
    #@nonl
    #@-node:ekr.20051009045404:createFirstTreeNode
    #@+node:ekr.20051121092320:f.enableTclTraces
    def enableTclTraces (self):
        
        c = self.c
    
        def tracewidget(event):
            g.trace('enabling widget trace')
            Pmw.tracetk(event.widget, 1)
        
        def untracewidget(event):
            g.trace('disabling widget trace')
            Pmw.tracetk(event.widget,0)
            
        def focusIn (event):
            print("Focus in  %s (%s)" % (
                event.widget,event.widget.winfo_class()))
            
        def focusOut (event):
            print("Focus out %s (%s)" % (
                event.widget,event.widget.winfo_class()))
    
        # Put this in unit tests before the assert:
        # c.frame.bar1.unbind_all("<FocusIn>")
        # c.frame.bar1.unbind_all("<FocusOut>")
    
        # Any widget would do:
        w = c.frame.bar1
        if 1:
            w.bind_all("<FocusIn>", focusIn)
            w.bind_all("<FocusOut>", focusOut)
        else:
            w.bind_all("<Control-1>", tracewidget)
            w.bind_all("<Control-Shift-1>", untracewidget)
    #@nonl
    #@-node:ekr.20051121092320:f.enableTclTraces
    #@-node:ekr.20031218072017.2176:f.finishCreate & helpers
    #@+node:ekr.20031218072017.3944:f.createCanvas & helpers
    def createCanvas (self,parentFrame,pack=True):
    
        # pageName is not used here: it is used for compatibility with the Chapters plugin.
    
        c = self.c
    
        scrolls = c.config.getBool('outline_pane_scrolls_horizontally')
        scrolls = g.choose(scrolls,1,0)
    
        if use_Pmw and Pmw:
            canvas = self.createPmwTreeCanvas(parentFrame,scrolls,pack)
        else:
            canvas = self.createTkTreeCanvas(parentFrame,scrolls,pack)
    
        return canvas
    #@nonl
    #@+node:ekr.20041221071131.1:createTkTreeCanvas
    def createTkTreeCanvas (self,parentFrame,scrolls,pack):
        
        frame = self
        
        canvas = Tk.Canvas(parentFrame,name="canvas",
            bd=0,bg="white",relief="flat")
            
        trace = self.c.config.getBool('trace_chapters') and not g.app.unitTesting
        if trace: g.trace(canvas)
            
        # g.trace('canvas',repr(canvas),'name',frame.c.widget_name(canvas))
    
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
        if 0:
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
    #@+node:ekr.20041221071131:createPmwTreeCanvas (not used)
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
    #@-node:ekr.20041221071131:createPmwTreeCanvas (not used)
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
        
        # g.trace(ratio,ratio2,g.callers())
        
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
            wRoot = top.winfo_rooty()
            barRoot = bar.winfo_rooty()
            wMax = top.winfo_height()
            offset = float(barRoot) + y - wRoot
        else:
            # Panes arranged horizontally; vertical splitter bar
            wRoot = top.winfo_rootx()
            barRoot = bar.winfo_rootx()
            wMax = top.winfo_width()
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
    #@+node:ekr.20031218072017.1974:destroySelf (tkFrame)
    def destroySelf (self):
        
        # Remember these: we are about to destroy all of our ivars!
        top = self.top 
        c = self.c
        
        # Indicate that the commander is no longer valid.
        c.exists = False 
        
        # g.trace(self)
    
        # Important: this destroys all the object of the commander too.
        self.destroyAllObjects()
        
        c.exists = False # Make sure this one ivar has not been destroyed.
    
        top.destroy()
    #@nonl
    #@-node:ekr.20031218072017.1974:destroySelf (tkFrame)
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
                height=1,state="disabled",bg=bg,relief="groove",name='status-line')
            self.textWidget.pack(side="left",expand=1,fill="x")
            self.textWidget.bind("<Button-1>", self.onActivate)
        #@nonl
        #@-node:ekr.20031218072017.3961: ctor
        #@+node:ekr.20031218072017.3962:clear
        def clear (self):
            
            t = self.textWidget
            if not t: return
            
            trace = self.c.frame.trace_status_line and not g.app.unitTesting
            if trace: g.trace(g.callers())
            
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
            c.bodyWantsFocus()
            
        def enable (self,background="white"):
            
            # g.trace()
            c = self.c ; t = self.textWidget
            if t:
                t.configure(state="normal",background=background)
                c.widgetWantsFocus(t)
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
                
        show = pack
        #@nonl
        #@-node:ekr.20041223111916:pack & show
        #@+node:ekr.20031218072017.3963:put (leoTkinterFrame:statusLineClass)
        def put(self,s,color=None):
            
            t = self.textWidget
            if not t: return
            
            trace = self.c.frame.trace_status_line and not g.app.unitTesting
            if trace: g.trace(s,g.callers())
            
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
            
            c = self.c ; w = self.bodyCtrl ; lab = self.labelWidget
            if g.app.killed or not self.isVisible:
                return
        
            index = w.index("insert")
            row,col = g.app.gui.getindex(w,index)
        
            if col > 0:
                s = w.get("%d.0" % (row),index)
                s = g.toUnicode(s,g.app.tkEncoding)
                col = g.computeWidth (s,c.tab_width)
        
            if 1: # row != self.lastRow or col != self.lastCol:
                s = "line %d, col %d " % (row,col)
                # Important: this does not change the focus because labels never get focus.
                lab.configure(text=s)
                self.lastRow = row
                self.lastCol = col
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
    #@+node:ekr.20060203115311:showMinibuffer
    def showMinibuffer (self):
        
        frame = self
        
        if not frame.minibufferVisible:
            frame.minibufferFrame.pack(side='bottom',fill='x')
            frame.minibufferVisible = True
            
    #@-node:ekr.20060203115311:showMinibuffer
    #@+node:ekr.20060203115311.1:hideMinibuffer
    def hideMinibuffer (self):
        
        frame = self
        if frame.minibufferVisible:
            frame.minibufferFrame.pack_forget()
            frame.minibufferVisible = False
    #@nonl
    #@-node:ekr.20060203115311.1:hideMinibuffer
    #@+node:ekr.20050920094212:f.createMiniBufferWidget
    def createMiniBufferWidget (self):
        
        '''Create the minbuffer below the status line.'''
        
        frame = self ; c = frame.c
    
        frame.minibufferFrame = f = Tk.Frame(frame.outerFrame,relief='flat',borderwidth=0)
        if c.showMinibuffer:
            f.pack(side='bottom',fill='x')
    
        lab = Tk.Label(f,text='mini-buffer',justify='left',anchor='nw',foreground='blue')
        lab.pack(side='left')
        
        if c.useTextMinibuffer:
            label = Tk.Text(f,height=1,relief='groove',background='lightgrey',name='minibuffer')
            label.pack(side='left',fill='x',expand=1,padx=2,pady=1)
        else:
            label = Tk.Label(f,relief='groove',justify='left',anchor='w',name='minibuffer')
            label.pack(side='left',fill='both',expand=1,padx=2,pady=1)
        
        frame.minibufferVisible = c.showMinibuffer
    
        return label
    #@nonl
    #@-node:ekr.20050920094212:f.createMiniBufferWidget
    #@+node:ekr.20060203114017:f.setMinibufferBindings
    def setMinibufferBindings (self):
        
        '''Create bindings for the minibuffer..'''
        
        f = self ; c = f.c ; k = c.k ; t = f.miniBufferWidget
        
        if not c.useTextMinibuffer: return
        
        for kind,callback in (
            ('<Key>',           k.masterKeyHandler),
            ('<Button-1>',      k.masterClickHandler),
            ('<Button-3>',      k.masterClick3Handler),
            ('<Double-1>',      k.masterDoubleClickHandler),
            ('<Double-3>',      k.masterDoubleClick3Handler),
        ):
            t.bind(kind,callback)
    
        if 0:
            if sys.platform.startswith('win'):
                # Support Linux middle-button paste easter egg.
                t.bind("<Button-2>",frame.OnPaste)
    #@nonl
    #@-node:ekr.20060203114017:f.setMinibufferBindings
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
        except Exception:
            # g.es_exception()
            pass # Support for chapters plugin.
    
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
        
    def updateStatusLine(self):
        return self.callStatus('update')
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
    
        c.redraw_now()
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
        
        f = self ; c = f.c
        
        if c.inCommand:
            g.trace('requesting window close')
            c.requestCloseWindow = True
        else:
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
            frame = self ; c = frame.c
            c.setLog()
            w = c.get_focus()
            if w != c.frame.body.bodyCtrl:
                frame.tree.OnDeactivate()
            c.bodyWantsFocus()
        except:
            g.es_event_exception("activate body")
            
        return 'break'
    #@nonl
    #@-node:ekr.20031218072017.3975:OnActivateBody (tkFrame)
    #@+node:ekr.20031218072017.2253:OnActivateLeoEvent, OnDeactivateLeoEvent
    def OnActivateLeoEvent(self,event=None):
        
        '''Handle a click anywhere in the Leo window.'''
        
        __pychecker__ = '--no-argsused' # event.
    
        self.c.setLog()
    
    def OnDeactivateLeoEvent(self,event=None):
        
        pass # This causes problems on the Mac.
    #@nonl
    #@-node:ekr.20031218072017.2253:OnActivateLeoEvent, OnDeactivateLeoEvent
    #@+node:ekr.20031218072017.3976:OnActivateTree
    def OnActivateTree (self,event=None):
    
        try:
            frame = self ; c = frame.c
            c.setLog()
    
            if 0: # Do NOT do this here!
                # OnActivateTree can get called when the tree gets DE-activated!!
                c.bodyWantsFocus()
                
        except:
            g.es_event_exception("activate tree")
    #@nonl
    #@-node:ekr.20031218072017.3976:OnActivateTree
    #@+node:ekr.20031218072017.3977:OnBodyClick, OnBodyRClick (Events)
    def OnBodyClick (self,event=None):
    
        try:
            c = self.c ; p = c.currentPosition()
            if not g.doHook("bodyclick1",c=c,p=p,v=p,event=event):
                self.OnActivateBody(event=event)
            g.doHook("bodyclick2",c=c,p=p,v=p,event=event)
        except:
            g.es_event_exception("bodyclick")
    
    def OnBodyRClick(self,event=None):
        
        try:
            c = self.c ; p = c.currentPosition()
            if not g.doHook("bodyrclick1",c=c,p=p,v=p,event=event):
                pass # By default Leo does nothing.
            g.doHook("bodyrclick2",c=c,p=p,v=p,event=event)
        except:
            g.es_event_exception("iconrclick")
    #@nonl
    #@-node:ekr.20031218072017.3977:OnBodyClick, OnBodyRClick (Events)
    #@+node:ekr.20031218072017.3978:OnBodyDoubleClick (Events)
    def OnBodyDoubleClick (self,event=None):
    
        try:
            c = self.c ; p = c.currentPosition()
            if not g.doHook("bodydclick1",c=c,p=p,v=p,event=event):
                if event: # Prevent wandering insertion point.
                    index = "@%d,%d" % (event.x, event.y) # Find where we clicked.
                    w = self.bodyCtrl
                    start = w.index(index + " wordstart")
                    end   = w.index(index + " wordend")
                    self.body.setTextSelection(start,end)
            g.doHook("bodydclick2",c=c,p=p,v=p,event=event)
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
    #@+node:ekr.20060209110128:Minibuffer commands... (tkFrame)
    
    #@+node:ekr.20060209110128.1:contractPane
    def contractPane (self,event=None):
        
        f = self ; c = f.c
        w = c.get_requested_focus()
        wname = c.widget_name(w)
    
        # g.trace(wname)
        if not w: return
        
        if wname.startswith('body'):
            f.contractBodyPane()
        elif wname.startswith('log'):
            f.contractLogPane()
        elif wname.startswith('head') or wname.startswith('canvas'):
            f.contractOutlinePane()
    #@nonl
    #@-node:ekr.20060209110128.1:contractPane
    #@+node:ekr.20060209110128.2:expandPane
    def expandPane (self,event=None):
    
        f = self ; c = f.c
            
        w = c.get_requested_focus()
        wname = c.widget_name(w)
    
        # g.trace(wname)
        if not w: return
        
        if wname.startswith('body'):
            f.expandBodyPane()
        elif wname.startswith('log'):
            f.expandLogPane()
        elif wname.startswith('head') or wname.startswith('canvas'):
            f.expandOutlinePane()
    #@nonl
    #@-node:ekr.20060209110128.2:expandPane
    #@+node:ekr.20060210123852:fullyExpandPane
    def fullyExpandPane (self,event=None):
    
        f = self ; c = f.c
            
        w = c.get_requested_focus()
        wname = c.widget_name(w)
    
        # g.trace(wname)
        if not w: return
        
        if wname.startswith('body'):
            f.fullyExpandBodyPane()
        elif wname.startswith('log'):
            f.fullyExpandLogPane()
        elif wname.startswith('head') or wname.startswith('canvas'):
            f.fullyExpandOutlinePane()
    #@nonl
    #@-node:ekr.20060210123852:fullyExpandPane
    #@+node:ekr.20060209143933:hidePane
    def hidePane (self,event=None):
    
        f = self ; c = f.c
            
        w = c.get_requested_focus()
        wname = c.widget_name(w)
    
        g.trace(wname)
        if not w: return
        
        if wname.startswith('body'):
            f.hideBodyPane()
            c.treeWantsFocusNow()
        elif wname.startswith('log'):
            f.hideLogPane()
            c.bodyWantsFocusNow()
        elif wname.startswith('head') or wname.startswith('canvas'):
            f.hideOutlinePane()
            c.bodyWantsFocusNow()
    #@nonl
    #@-node:ekr.20060209143933:hidePane
    #@+node:ekr.20060209110936:expand/contract/hide...Pane
    #@+at 
    #@nonl
    # The first arg to divideLeoSplitter means the following:
    # 
    #     f.splitVerticalFlag: use the primary   (tree/body) ratio.
    # not f.splitVerticalFlag: use the secondary (tree/log) ratio.
    #@-at
    #@@c
    
    def contractBodyPane (self,event=None):
        f = self ; r = min(1.0,f.ratio+0.1)
        f.divideLeoSplitter(f.splitVerticalFlag,r)
    
    def contractLogPane (self,event=None):
        f = self ; r = min(1.0,f.ratio+0.1)
        f.divideLeoSplitter(not f.splitVerticalFlag,r)
    
    def contractOutlinePane (self,event=None):
        f = self ; r = max(0.0,f.ratio-0.1)
        f.divideLeoSplitter(f.splitVerticalFlag,r)
        
    def expandBodyPane (self,event=None):
        self.contractOutlinePane()
    
    def expandLogPane(self,event=None):
        f = self ; r = max(0.0,f.ratio-0.1)
        f.divideLeoSplitter(not f.splitVerticalFlag,r)
        
    def expandOutlinePane (self,event=None):
        self.contractBodyPane()
    #@nonl
    #@-node:ekr.20060209110936:expand/contract/hide...Pane
    #@+node:ekr.20060210123852.1:fullyExpand/hide...Pane
    def fullyExpandBodyPane (self,event=None):
        f = self ; f.divideLeoSplitter(f.splitVerticalFlag,0.0)
    
    def fullyExpandLogPane (self,event=None):
        f = self ; f.divideLeoSplitter(not f.splitVerticalFlag,0.0)
    
    def fullyExpandOutlinePane (self,event=None):
        f = self ; f.divideLeoSplitter(f.splitVerticalFlag,1.0)
        
    def hideBodyPane (self,event=None):
        f = self ; f.divideLeoSplitter(f.splitVerticalFlag,1.0)
    
    def hideLogPane (self,event=None):
        f = self ; f.divideLeoSplitter(not f.splitVerticalFlag,1.0)
    
    def hideOutlinePane (self,event=None):
        f = self ; f.divideLeoSplitter(f.splitVerticalFlag,0.0)
    #@nonl
    #@-node:ekr.20060210123852.1:fullyExpand/hide...Pane
    #@-node:ekr.20060209110128:Minibuffer commands... (tkFrame)
    #@+node:ekr.20031218072017.3980:Edit Menu...
    #@+node:ekr.20031218072017.3981:abortEditLabelCommand
    def abortEditLabelCommand (self,event=None):
        
        frame = self ; c = frame.c ; tree = frame.tree
        p = c.currentPosition() ; w = p.edit_widget()
        
        if g.app.batchMode:
            c.notValidInBatchMode("Abort Edit Headline")
            return
            
        # g.trace('isEditing',p == tree.editPosition(),'revertHeadline',repr(tree.revertHeadline))
            
        if w and p == tree.editPosition():
            # Revert the headline text.
            w.delete("1.0","end")
            w.insert("end",tree.revertHeadline)
            p.initHeadString(tree.revertHeadline)
            c.beginUpdate()
            try:
                c.endEditing()
                c.selectPosition(p)
            finally:
                c.endUpdate()
    #@nonl
    #@-node:ekr.20031218072017.3981:abortEditLabelCommand
    #@+node:ekr.20031218072017.840:Cut/Copy/Paste (tkFrame)
    #@+node:ekr.20051011072903.2:copyText
    def copyText (self,event=None):
        
        '''Copy the selected text from the widget to the clipboard.'''
        
        f = self ; c = f.c ; w = event and event.widget
        if not w or not g.app.gui.isTextWidget(w): return
    
        # Set the clipboard text.
        i,j = g.app.gui.getTextSelection(w)
        if i != j:
            s = w.get(i,j)
            g.app.gui.replaceClipboardWith(s)
            
    OnCopyFromMenu = copyText
    #@nonl
    #@-node:ekr.20051011072903.2:copyText
    #@+node:ekr.20051011072049.2:cutText
    def cutText (self,event=None):
        
        '''Invoked from the mini-buffer and from shortcuts.'''
        
        f = self ; c = f.c ; w = event and event.widget
        if not w or not g.app.gui.isTextWidget(w): return
    
        name = c.widget_name(w)
        oldSel = g.app.gui.getTextSelection(w)
        oldText = w.get('1.0','end')
        i,j = g.app.gui.getTextSelection(w)
        
        # Update the widget and set the clipboard text.
        s = w.get(i,j)
        if i != j:
            w.delete(i,j)
            g.app.gui.replaceClipboardWith(s)
    
        if name.startswith('body'):
            c.frame.body.onBodyChanged('Cut',oldSel=oldSel,oldText=oldText)
        elif name.startswith('head'):
            # The headline is not officially changed yet.
            # p.initHeadString(s)
            w.configure(width=f.tree.headWidth(s=s))
        else: pass
    
    OnCutFromMenu = cutText
    #@nonl
    #@-node:ekr.20051011072049.2:cutText
    #@+node:ekr.20051011072903.5:pasteText
    def pasteText (self,event=None):
    
        '''Paste the clipboard into a widget.'''
    
        f = self ; c = f.c ; w = event and event.widget
        if not w or not g.app.gui.isTextWidget(w): return
    
        wname = c.widget_name(w)
        oldSel = g.app.gui.getTextSelection(w)
        oldText = w.get('1.0','end')
        i,j = g.app.gui.getTextSelection(w)
        s = s1 = g.app.gui.getTextFromClipboard()
        # g.trace(wname,s,i,j)
        
        singleLine = wname.startswith('head') or wname.startswith('minibuffer')
        
        if singleLine:
            # Strip trailing newlines so the truncation doesn't cause confusion.
            while s and s [ -1] in ('\n','\r'):
                s = s [: -1]
    
        try:
            # Update the widget.
            if i != j:
                w.delete(i,j)
            w.insert(i,s)
        
            if wname.startswith('body'):
                c.frame.body.onBodyChanged('Paste',oldSel=oldSel,oldText=oldText)
            elif singleLine:
                s = w.get('1.0','end')
                while s and s [ -1] in ('\n','\r'):
                    s = s [: -1]
                if wname.startswith('head'):
                    # The headline is not officially changed yet.
                    # p.initHeadString(s)
                    w.configure(width=f.tree.headWidth(s=s))
            else: pass
        except Exception:
            pass # Tk sometimes throws weird exceptions here.
            
        return 'break' # Essential
    
    OnPasteFromMenu = pasteText
    #@nonl
    #@-node:ekr.20051011072903.5:pasteText
    #@-node:ekr.20031218072017.840:Cut/Copy/Paste (tkFrame)
    #@+node:ekr.20031218072017.3982:endEditLabelCommand
    def endEditLabelCommand (self,event=None):
        
        '''End editing of a headline and move focus to the body pane.'''
    
        frame = self ; c = frame.c
        
        if g.app.batchMode:
            c.notValidInBatchMode("End Edit Headline")
        else:
            c.endEditing()
            c.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20031218072017.3982:endEditLabelCommand
    #@+node:ekr.20031218072017.3983:insertHeadlineTime
    def insertHeadlineTime (self,event=None):
    
        frame = self ; c = frame.c ; p = c.currentPosition()
        
        if g.app.batchMode:
            c.notValidInBatchMode("Insert Headline Time")
            return
            
        c.editPosition(p)
        c.frame.tree.setEditLabelState(p)
        w = p.edit_widget()
        if w:
            time = c.getTime(body=False)
            if 1: # We can't know if we were already editing, so insert at end.
                g.app.gui.setSelectionRange(w,'end','end')
                w.insert('end',time)
            else:
                i, j = g.app.gui.getTextSelection(w)
                if i != j:
                    w.delete(i,j)
                w.insert("insert",time)
            c.frame.tree.onHeadChanged(p,'Insert Headline Time')
    #@nonl
    #@-node:ekr.20031218072017.3983:insertHeadlineTime
    #@-node:ekr.20031218072017.3980:Edit Menu...
    #@+node:ekr.20031218072017.3984:Window Menu...
    #@+node:ekr.20031218072017.3985:toggleActivePane
    def toggleActivePane (self,event=None):
        
        '''Toggle the focus between the outline and body panes.'''
        
        frame = self ; c = frame.c
    
        if c.get_focus() == frame.bodyCtrl:
            c.treeWantsFocus()
        else:
            c.endEditing()
            c.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20031218072017.3985:toggleActivePane
    #@+node:ekr.20031218072017.3986:cascade
    def cascade (self,event=None):
    
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
    def equalSizedPanes (self,event=None):
    
        frame = self
        frame.resizePanesToRatio(0.5,frame.secondary_ratio)
    #@-node:ekr.20031218072017.3987:equalSizedPanes
    #@+node:ekr.20031218072017.3988:hideLogWindow
    def hideLogWindow (self,event=None):
        
        frame = self
        frame.divideLeoSplitter2(0.99, not frame.splitVerticalFlag)
    #@nonl
    #@-node:ekr.20031218072017.3988:hideLogWindow
    #@+node:ekr.20031218072017.3989:minimizeAll
    def minimizeAll (self,event=None):
    
        
        self.minimize(g.app.pythonFrame)
        for frame in g.app.windowList:
            self.minimize(frame)
            self.minimize(frame.findPanel)
        
    def minimize(self,frame):
    
        if frame and frame.top.state() == "normal":
            frame.top.iconify()
    #@nonl
    #@-node:ekr.20031218072017.3989:minimizeAll
    #@+node:ekr.20031218072017.3990:toggleSplitDirection (tkFrame)
    # The key invariant: self.splitVerticalFlag tells the alignment of the main splitter.
    
    def toggleSplitDirection (self,event=None):
        
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
        c.setLog()
        frame.log.restoreAllState(d)
        c.beginUpdate()
        try:
            c.selectPosition(p)
        finally:
            c.endUpdate()
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
    def resizeToScreen (self,event=None):
        
        top = self.top
        
        w = top.winfo_screenwidth()
        h = top.winfo_screenheight()
    
        if sys.platform == 'darwin':
            # Must leave room to get at very small resizing area.
            geom = "%dx%d%+d%+d" % (w-20,h-55,10,25)
        else:
            # Fill almost the entire screen.
            # Works on Windows. YMMV for other platforms.
            geom = "%dx%d%+d%+d" % (w-8,h-46,0,0)
       
        top.geometry(geom)
    #@nonl
    #@-node:EKR.20040422130619:resizeToScreen
    #@-node:ekr.20031218072017.3984:Window Menu...
    #@+node:ekr.20031218072017.3991:Help Menu...
    #@+node:ekr.20031218072017.3992:leoHelp
    def leoHelp (self,event=None):
        
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
    #@nonl
    # New in 4.3. The proper way to change focus is to call 
    # c.frame.xWantsFocus.
    # 
    # Important: This code never calls select, so there can be no race 
    # condition here
    # that alters text improperly.
    #@-at
    #@nonl
    #@-node:ekr.20050120083053:Delayed Focus (tkFrame)
    #@+node:ekr.20031218072017.3995:Tk bindings...
    def bringToFront (self):
        self.top.deiconify()
        self.top.lift()
    
    def getFocus(self):
        """Returns the widget that has focus, or body if None."""
        try:
            # This method is unreliable while focus is changing.
            # The call to update_idletasks may help.  Or not.
            self.top.update_idletasks()
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
        
        self.trace_onBodyChanged = c.config.getBool('trace_onBodyChanged')
    
        self.bodyCtrl = self.createControl(frame,parentFrame)
    
        self.colorizer = leoColor.colorizer(c)
    #@-node:ekr.20031218072017.2182:tkBody. __init__
    #@+node:ekr.20031218072017.838:tkBody.createBindings
    def createBindings (self):
    
        '''(tkBody) Create gui-dependent bindings.
        These are *not* made in nullBody instances.'''
        
        frame = self.frame ; c = self.c ; k = c.k ; t = self.bodyCtrl
        
        t.bind('<Key>', k.masterKeyHandler)
    
        for kind,func,handler in (
            ('<Button-1>',  frame.OnBodyClick,          k.masterClickHandler),
            ('<Button-3>',  frame.OnBodyRClick,         k.masterClick3Handler),
            ('<Double-1>',  frame.OnBodyDoubleClick,    k.masterDoubleClickHandler),
            ('<Double-3>',  None,                       k.masterDoubleClick3Handler),
        ):
            def bodyClickCallback(event,handler=handler,func=func):
                return handler(event,func)
    
            t.bind(kind,bodyClickCallback)
                
        if sys.platform.startswith('win'):
            # Support Linux middle-button paste easter egg.
            t.bind("<Button-2>",frame.OnPaste)
    #@nonl
    #@-node:ekr.20031218072017.838:tkBody.createBindings
    #@+node:ekr.20031218072017.3998:tkBody.createControl
    def createControl (self,frame,parentFrame):
        
        c = self.c
    
        wrap = c.config.getBool('body_pane_wraps')
        wrap = g.choose(wrap,"word","none")
        
        # Setgrid=1 cause severe problems with the font panel.
        body = Tk.Text(parentFrame,name='body-pane',
            bd=2,bg="white",relief="flat",setgrid=0,wrap=wrap)
            
        trace = c.config.getBool('trace_chapters') and not g.app.unitTesting
        if trace: g.trace('tkBody',body)
        
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
            c.config.defaultBodyFontSize)
        
        self.fontRef = font # ESSENTIAL: retain a link to font.
        body.configure(font=font)
    
        # g.trace("BODY",body.cget("font"),font.cget("family"),font.cget("weight"))
    #@nonl
    #@-node:ekr.20031218072017.2183:tkBody.setFontFromConfig
    #@+node:ekr.20031218072017.1329:onBodyChanged (tkBody) & removeTrailingNewlines
    # This is the only key handler for the body pane.
    def onBodyChanged (self,undoType,
        oldSel=None,oldText=None,oldYview=None,removeTrailing=None):
        
        '''Update Leo after the body has been changed.'''
        
        body = self ; c = self.c ; bodyCtrl = body.bodyCtrl
        trace = self.trace_onBodyChanged
        p = c.currentPosition()
        insert = bodyCtrl.index('insert')
        ch = g.choose(insert=='1.0','',bodyCtrl.get('insert-1c'))
        ch = g.toUnicode(ch,g.app.tkEncoding) # New in 4.4b3.
        newText = g.app.gui.getAllText(bodyCtrl) # New in 4.4b3: converts to unicode.
        newSel = g.app.gui.getTextSelection(bodyCtrl)
        if oldText is None: oldText = p.bodyString()
        if removeTrailing is None:
            removeTrailing = self.removeTrailingNewlines(oldText,newText,ch)
        if removeTrailing and newText:
            newText = newText[:-1]
        changed = oldText != newText
        if trace:
            g.trace(repr(ch),'changed:',changed)
            # g.trace('removeTrailing:',removeTrailing)
            g.trace('newText:',repr(newText))
            #g.trace('oldText:',repr(oldText))
        if changed:
            c.undoer.setUndoTypingParams(p,undoType,
                oldText=oldText,newText=newText,oldSel=oldSel,newSel=newSel,oldYview=oldYview)
            p.v.setTnodeText(newText)
            p.v.t.insertSpot = body.getInsertionPoint()
            #@        << recolor the body >>
            #@+node:ekr.20051026083733.6:<< recolor the body >>
            body.colorizer.interrupt()
            c.frame.scanForTabWidth(p)
            body.recolor_now(p,incremental=not self.forceFullRecolorFlag)
            self.forceFullRecolorFlag = False
            #@nonl
            #@-node:ekr.20051026083733.6:<< recolor the body >>
            #@nl
            if not c.changed: c.setChanged(True)
            #@        << redraw the screen if necessary >>
            #@+node:ekr.20051026083733.7:<< redraw the screen if necessary >>
            c.beginUpdate()
            try:
                redraw_flag = False
                # Update dirty bits.
                # p.setDirty() sets all cloned and @file dirty bits.
                if not p.isDirty() and p.setDirty():
                    redraw_flag = True
                    
                # Update icons. p.v.iconVal may not exist during unit tests.
                val = p.computeIcon()
                if not hasattr(p.v,"iconVal") or val != p.v.iconVal:
                    p.v.iconVal = val
                    redraw_flag = True
            finally:
                c.endUpdate(redraw_flag)
            #@nonl
            #@-node:ekr.20051026083733.7:<< redraw the screen if necessary >>
            #@nl
    #@nonl
    #@+node:ekr.20051026143009:removeTrailingNewlines
    #@+at 
    #@nonl
    # Tk will add a newline only if:
    # 1. A real change has been made to the Tk.Text widget, and
    # 2. the change did _not_ result in the widget already containing a 
    # newline.
    # 
    # It's not possible to tell, given the information available, what Tk has 
    # actually
    # done. We need only make a reasonable guess here. setUndoTypingParams 
    # stores the
    # number of trailing newlines in each undo bead, so whatever we do here 
    # can be
    # faithfully undone and redone.
    #@-at
    #@@c
    
    def removeTrailingNewlines (self,old,new,ch):
    
        '''Return True if a Tk has erroneously added a trailing newline.'''
    
        if not new.endswith('\n'):
            # There is no newline to remove.  Probably will never happen.
            return False
        elif not old:
            # Ambigous case.  Formerly always returned False.
            if new == "\n\n":
                return True # Handle a very strange special case.
            else:
                return ch not in ('\r','\n')
        ### elif g.safeStringCompare(old,new[-1]):
        elif old == new[:-1]:
            # A single trailing character has been added.
            return ch not in ('\r','\n') # Was False.
        else:
            # The text didn't have a newline, and now it does.
            # Moveover, some other change has been made to the text,
            # So at worst we have misrepresented the user's intentions slightly.
            return True
    #@nonl
    #@-node:ekr.20051026143009:removeTrailingNewlines
    #@-node:ekr.20031218072017.1329:onBodyChanged (tkBody) & removeTrailingNewlines
    #@+node:ekr.20031218072017.4003:Focus (tkBody)
    def hasFocus (self):
        
        return self.bodyCtrl == self.frame.top.focus_displayof()
        
    def setFocus (self):
        
        self.c.widgetWantsFocus(self.bodyCtrl)
    #@nonl
    #@-node:ekr.20031218072017.4003:Focus (tkBody)
    #@+node:ekr.20031218072017.3999:forceRecolor
    def forceFullRecolor (self):
        
        self.forceFullRecolorFlag = True
    #@nonl
    #@-node:ekr.20031218072017.3999:forceRecolor
    #@+node:ekr.20031218072017.4000:Tk bindings (tkBbody)
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
        
        self.bodyCtrl.see("insert") # -5l")
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
            return u'' # Bug fix: 1/8/06
    #@nonl
    #@-node:ekr.20031218072017.4020:getSelectedText
    #@+node:ekr.20031218072017.4021:getTextSelection
    def getTextSelection (self,sort=True):
        
        """Return a tuple representing the selected range of body text.
        
        Return a tuple giving the insertion point if no range of text is selected."""
    
        w = self.bodyCtrl
        
        sel = w.tag_ranges("sel")
    
        if len(sel) == 2:
            # New in 4.4a5: match behavior of g.app.gui.getTextSelection.
            if sort:
                i,j = sel
                if w.compare(i, ">", j):
                    i,j = j,i
            return sel
        else:
            # Return the insertion point if there is no selected text.
            insert = w.index("insert")
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
    def selectAllText (self,event=None):
        
        c = self.c ; k = c.k
    
        try:
            w = c.get_focus() ; wname = c.widget_name(w)
            n = 0
            if wname.startswith('head'):
                s = w.get('1.0','end')
                while s.endswith('\n') or s.endswith('\r'):
                    s = s[:-1] ; n += 1
                g.app.gui.setTextSelection(w,'1.0','end - %dc' % (n))
            elif wname.startswith('mini'):
                i,j = k.getEditableTextRange()
                g.app.gui.setTextSelection(w,i,j)
            else:
                g.app.gui.setTextSelection(w,'1.0','end - %dc' % (n))
        except:
            # g.es_exception()
            pass
    #@nonl
    #@-node:ekr.20031218072017.4023:selectAllText
    #@+node:ekr.20031218072017.4024:setTextSelection (tkinterBody)
    def setTextSelection (self,i,j=None,insert='sel.end'):
        
        # Allow the user to pass either a 2-tuple or two separate args.
        if i is None:
            i,j = "1.0","1.0"
        elif len(i) == 2:
            i,j = i
    
        g.app.gui.setTextSelection(self.bodyCtrl,i,j,insert)
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
    #@+node:ekr.20031218072017.4028:tkBody.getAllText
    def getAllText (self):
        
        """Return all the body text, converted to unicode."""
        
        s = self.bodyCtrl.get("1.0","end")
        if s is None:
            return u""
        else:
            return g.toUnicode(s,g.app.tkEncoding)
    #@nonl
    #@-node:ekr.20031218072017.4028:tkBody.getAllText
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
    #@-node:ekr.20031218072017.4000:Tk bindings (tkBbody)
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
        self.logNumber = 0 # To create unique name fields for Tk.Text widgets.
        self.menu = None # A menu that pops up on right clicks in the hull or in tabs.
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
            lowercommand = self.lowerTab,
            arrownavigation = 0,
        )
    
        menu = self.makeTabMenu(tabName=None)
    
        def hullMenuCallback(event):
            g.trace()
            return self.onRightClick(event,menu)
    
        self.nb.bind('<Button-3>',hullMenuCallback)
    
        self.nb.pack(fill='both',expand=1)
        self.selectTab('Log') # create the tab and make it the active tab.
        return self.logCtrl
    #@nonl
    #@-node:ekr.20031218072017.4042:tkLog.createControl
    #@+node:ekr.20051016103459:tkLog.createTextWidget
    def createTextWidget (self,parentFrame):
        
        self.logNumber += 1
        log = Tk.Text(parentFrame,name="log-%d" % self.logNumber,
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
                return self.deleteTab(tabName)
                
            label = g.choose(
                tabName in ('Find','Spell'),'Hide This Tab','Delete This Tab')
            menu.add_command(label=label,command=deleteTabCallback)
     
            def renameTabCallback():
                return self.renameTabFromMenu(tabName)
    
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
    def SetWidgetFontFromConfig (self,logCtrl=None):
    
        c = self.c
    
        if not logCtrl: logCtrl = self.logCtrl
    
        font = c.config.getFontFromParams(
            "log_text_font_family", "log_text_font_size",
            "log_text_font_slant", "log_text_font_weight",
            c.config.defaultLogFontSize)
    
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
            
    setFontFromConfig = SetWidgetFontFromConfig # Renaming supresses a pychecker warning.
    #@nonl
    #@-node:ekr.20031218072017.4046:tkLog.setFontFromConfig
    #@-node:ekr.20051016095907.1:Config & get/saveState
    #@+node:ekr.20051016095907.2:Focus & update (tkLog)
    #@+node:ekr.20031218072017.4045:tkLog.onActivateLog
    def onActivateLog (self,event=None):
    
        try:
            self.c.setLog()
            self.frame.tree.OnDeactivate()
            self.c.logWantsFocus()
        except:
            g.es_event_exception("activate log")
    #@nonl
    #@-node:ekr.20031218072017.4045:tkLog.onActivateLog
    #@+node:ekr.20031218072017.4044:tkLog.hasFocus
    def hasFocus (self):
        
        return self.c.get_focus() == self.logCtrl
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
            self.logCtrl.update_idletasks()
    #@nonl
    #@-node:ekr.20050208133438:forceLogUpdate
    #@-node:ekr.20051016095907.2:Focus & update (tkLog)
    #@+node:ekr.20051016101927:put & putnl (tkLog)
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
        
        c = self.c
        
        # print 'tkLog.put',self.c.shortFileName(),tabName,g.callers()
    
        if g.app.quitting or not c or not c.exists:
            return
    
        if tabName:
            self.selectTab(tabName)
        
        if self.logCtrl:
            #@        << put s to log control >>
            #@+node:EKR.20040423082910:<< put s to log control >>
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
            self.logCtrl.update_idletasks()
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
    #@-node:ekr.20051016101927:put & putnl (tkLog)
    #@+node:ekr.20051018061932:Tab (TkLog)
    #@+node:ekr.20051017212057:clearTab
    def clearTab (self,tabName,wrap='none'):
        
        self.selectTab(tabName,wrap=wrap)
        t = self.logCtrl
        t and t.delete('1.0','end')
    #@nonl
    #@-node:ekr.20051017212057:clearTab
    #@+node:ekr.20051024173701:createTab
    def createTab (self,tabName,wrap='none'):
        
        # g.trace(tabName,wrap)
        
        c = self.c ; k = c.k
        tabFrame = self.nb.add(tabName)
        self.menu = self.makeTabMenu(tabName)
        #@    << Create the tab's text widget >>
        #@+node:ekr.20051018072306:<< Create the tab's text widget >>
        t = self.createTextWidget(tabFrame)
        
        # Set the background color.
        configName = 'log_pane_%s_tab_background_color' % tabName
        bg = c.config.getColor(configName) or 'MistyRose1'
        
        if wrap not in ('none','char','word'): wrap = 'none'
        try: t.configure(bg=bg,wrap=wrap)
        except Exception: pass # Could be a user error.
        
        self.SetWidgetFontFromConfig(logCtrl=t)
        
        self.frameDict [tabName] = tabFrame
        self.textDict [tabName] = t
        
        # Switch to a new colorTags list.
        if self.tabName:
            self.colorTagsDict [self.tabName] = self.colorTags [:]
        
        self.colorTags = ['black']
        self.colorTagsDict [tabName] = self.colorTags
        #@nonl
        #@-node:ekr.20051018072306:<< Create the tab's text widget >>
        #@nl
    
        if tabName != 'Log':
            # c.k doesn't exist when the log pane is created.
            # k.makeAllBindings will call setTabBindings('Log')
            self.setTabBindings(tabName)
    #@nonl
    #@-node:ekr.20051024173701:createTab
    #@+node:ekr.20051018102027:deleteTab
    def deleteTab (self,tabName):
        
        if tabName == 'Log':
            pass
    
        elif tabName in ('Find','Spell'):
            self.selectTab('Log')
        
        elif tabName in self.nb.pagenames():
            self.nb.delete(tabName)
            self.colorTagsDict [tabName] = []
            self.textDict [tabName] = None
            self.frameDict [tabName] = None
            self.tabName = None
            self.selectTab('Log')
            
        # New in Leo 4.4b1.
        self.c.invalidateFocus()
        self.c.bodyWantsFocus()
        
    #@nonl
    #@-node:ekr.20051018102027:deleteTab
    #@+node:ekr.20060204124347:hideTab
    def hideTab (self,tabName):
        
        __pychecker__ = '--no-argsused' # tabName
        
        self.selectTab('Log')
    #@nonl
    #@-node:ekr.20060204124347:hideTab
    #@+node:ekr.20051027114433:getSelectedTab
    def getSelectedTab (self):
        
        return self.tabName
    #@nonl
    #@-node:ekr.20051027114433:getSelectedTab
    #@+node:ekr.20051018061932.1:lower/raiseTab
    def lowerTab (self,tabName):
        
        if tabName:
            b = self.nb.tab(tabName) # b is a Tk.Button.
            b.config(bg='grey80')
        self.c.invalidateFocus()
        self.c.bodyWantsFocus()
    
    def raiseTab (self,tabName):
    
        if tabName:
            b = self.nb.tab(tabName) # b is a Tk.Button.
            b.config(bg='LightSteelBlue1')
        self.c.invalidateFocus()
        self.c.bodyWantsFocus()
    #@nonl
    #@-node:ekr.20051018061932.1:lower/raiseTab
    #@+node:ekr.20051019170806:renameTab
    def renameTab (self,oldName,newName):
        
        label = self.nb.tab(oldName)
        label.configure(text=newName)
    #@nonl
    #@-node:ekr.20051019170806:renameTab
    #@+node:ekr.20051016101724.1:selectTab
    def selectTab (self,tabName,wrap='none'):
    
        '''Create the tab if necessary and make it active.'''
    
        c = self.c ; tabFrame = self.frameDict.get(tabName)
    
        if tabFrame:
            # Switch to a new colorTags list.
            newColorTags = self.colorTagsDict.get(tabName)
            self.colorTagsDict [self.tabName] = self.colorTags [:]
            self.colorTags = newColorTags
        else:
            self.createTab(tabName,wrap=wrap)
            
        self.nb.selectpage(tabName)
        # Update the status vars.
        self.tabName = tabName
        self.logCtrl = self.textDict.get(tabName)
        self.tabFrame = self.frameDict.get(tabName)
    
        return tabFrame
    #@nonl
    #@-node:ekr.20051016101724.1:selectTab
    #@+node:ekr.20051022162730:setTabBindings
    def setTabBindings (self,tabName):
        
        c = self.c ; k = c.k
        tab = self.nb.tab(tabName)
        w = self.textDict.get(tabName)
        
        # Send all event in the text area to the master handlers.
        for kind,handler in (
            ('<Key>',       k.masterKeyHandler),
            ('<Button-1>',  k.masterClickHandler),
            ('<Button-3>',  k.masterClick3Handler),
        ):
            w.bind(kind,handler)
        
        # Clicks in the tab area are harmless: use the old code.
        def tabMenuRightClickCallback(event,menu=self.menu):
            return self.onRightClick(event,menu)
            
        def tabMenuClickCallback(event,tabName=tabName):
            return self.onClick(event,tabName)
        
        tab.bind('<Button-1>',tabMenuClickCallback)
        tab.bind('<Button-3>',tabMenuRightClickCallback)
        
        k.completeAllBindingsForWidget(w)
    #@nonl
    #@-node:ekr.20051022162730:setTabBindings
    #@+node:ekr.20051019134106:Tab menu callbacks & helpers
    #@+node:ekr.20051019134422:onRightClick & onClick
    def onRightClick (self,event,menu):
        
        c = self.c
        menu.post(event.x_root,event.y_root)
        
        
    def onClick (self,event,tabName):
    
        self.selectTab(tabName)
    #@nonl
    #@-node:ekr.20051019134422:onRightClick & onClick
    #@+node:ekr.20051019140004.1:newTabFromMenu
    def newTabFromMenu (self,tabName='Log'):
    
        self.selectTab(tabName)
        
        # This is called by getTabName.
        def selectTabCallback (newName):
            return self.selectTab(newName)
    
        self.getTabName(selectTabCallback)
    #@nonl
    #@-node:ekr.20051019140004.1:newTabFromMenu
    #@+node:ekr.20051019165401:renameTabFromMenu
    def renameTabFromMenu (self,tabName):
    
        if tabName in ('Log','Completions'):
            g.es('can not rename %s tab' % (tabName),color='blue')
        else:
            def renameTabCallback (newName):
                return self.renameTab(tabName,newName)
    
            self.getTabName(renameTabCallback)
    #@nonl
    #@-node:ekr.20051019165401:renameTabFromMenu
    #@+node:ekr.20051019172811:getTabName
    def getTabName (self,exitCallback):
        
        canvas = self.nb.component('hull')
    
        # Overlay what is there!
        f = Tk.Frame(canvas)
        f.pack(side='top',fill='both',expand=1)
        
        row1 = Tk.Frame(f)
        row1.pack(side='top',expand=0,fill='x',pady=10)
        row2 = Tk.Frame(f)
        row2.pack(side='top',expand=0,fill='x')
    
        Tk.Label(row1,text='Tab name').pack(side='left')
    
        e = Tk.Entry(row1,background='white')
        e.pack(side='left')
    
        def getNameCallback (event=None):
            s = e.get().strip()
            f.pack_forget()
            if s: exitCallback(s)
            
        def closeTabNameCallback (event=None):
            f.pack_forget()
            
        b = Tk.Button(row2,text='Ok',width=6,command=getNameCallback)
        b.pack(side='left',padx=10)
        
        b = Tk.Button(row2,text='Cancel',width=6,command=closeTabNameCallback)
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
