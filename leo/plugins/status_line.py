#@+leo-ver=4-thin
#@+node:ekr.20040201060959:@thin status_line.py
"""Adds status line to Leo window."""

#@@language python
#@@tabwidth -4

#@<< imports >>
#@+node:ekr.20041002154511:<< imports >>
import leoGlobals as g
import leoPlugins

# g.importExtension('Tkinter') does not seem to work.
try:
    import Tkinter as Tk
except ImportError:
    Tk = g.cantImport('Tkinter',pluginName=__name__)
#@nonl
#@-node:ekr.20041002154511:<< imports >>
#@nl

__version__ = "0.2"
#@<< version history >>
#@+node:ekr.20041002154511.1:<< version history >>
#@+at
# 
# 0.2 EKR:
# - Created statusLineClass.
#     - This solves problems with binding c.
#     - Moved most code into this class.
# - c.frame.updateStatusRowCol now longer schedules itself.
#     - There is no need to do that, and it caused problems.
# 0.3 EKR:
#     - Added input modes and all related code.
#@-at
#@nonl
#@-node:ekr.20041002154511.1:<< version history >>
#@nl

#@+others
#@+node:EKR.20040424152057:createStatusLine
def createStatusLine(tag,keywords):
    
    c = keywords.get("c")
    
    if c:
        statusLine = myStatusLineClass(c)
#@nonl
#@-node:EKR.20040424152057:createStatusLine
#@+node:ekr.20041002154511.2:class statusLineClass
class myStatusLineClass:
    
    """A class to manage a status line in a Leo window."""
    
    #@    @+others
    #@+node:ekr.20041002154511.3:ctor
    def __init__ (self,c):
        
        self.c = c
        
        c.frame.createStatusLine()
        c.frame.putStatusLine("Welcome to Leo")
        
        self.findText = ""
        self.changeText = ""
    
        # Create input modes.
        self.topMode    = topInputMode(c,self)
        self.optionsMode  = optionsInputMode(c,self)
        self.changeMode     = textInputMode(c,self,change=True)
        self.findChangeMode = textInputMode(c,self,change=False,willChange=True)
        self.findMode       = textInputMode(c,self,change=False)
        
        # To resolve refs to other classes.
        self.topMode.finishCreate()
        
        # Create the initial binding.
        self.c.frame.body.bodyCtrl.bind("<Key-Escape>",self.topMode.enterMode)
    #@nonl
    #@-node:ekr.20041002154511.3:ctor
    #@-others
#@nonl
#@-node:ekr.20041002154511.2:class statusLineClass
#@+node:ekr.20041026101757:class baseInputMode
class baseInputMode:
    
    """A class to represent an input mode in the status line and all related commands."""
    
    #@    @+others
    #@+node:ekr.20041026101757.1:ctor
    def __init__ (self,c,statusLine):
        
        self.c = c
        
        self.statusLine = statusLine
        self.signon = None
        self.name = "baseMode"
        self.clear = True
        self.keys = []
    #@nonl
    #@-node:ekr.20041026101757.1:ctor
    #@+node:ekr.20041026205259:doNothing
    def doNothing(self,event=None):
        
        return "break"
    #@nonl
    #@-node:ekr.20041026205259:doNothing
    #@+node:ekr.20041026113530:enterMode
    def enterMode (self,event=None):
        
        # g.trace(self.name)
            
        self.initBindings()
        
        if self.clear:
            self.clearStatusLine()
    
        if self.signon:
            self.putStatusLine(self.signon,color="red")
            
        self.originalLine = self.getStatusLine()
        if self.originalLine and self.originalLine[-1] == '\n':
            self.originalLine = self.originalLine[:-1]
    
        # g.trace(repr(self.originalLine))
    
        self.enableStatusLine()
        self.setFocusStatusLine()
        
        return "break"
    #@nonl
    #@-node:ekr.20041026113530:enterMode
    #@+node:ekr.20041026101757.3:exitMode
    def exitMode (self,event=None,nextMode=None):
        
        """Remove all key bindings for this mode."""
        
        # g.trace(self.name)
        
        self.unbindAll()
    
        if nextMode:
            nextMode.enterMode()
        else:
            self.clearStatusLine()
            self.disableStatusLine()
            self.c.frame.body.setFocus()
            self.c.frame.body.bodyCtrl.bind(
                "<Key-Escape>",self.statusLine.topMode.enterMode)
    
        return "break"
    #@nonl
    #@-node:ekr.20041026101757.3:exitMode
    #@+node:ekr.20041026101757.2:initBindings
    def initBindings (self):
        
        """Create key bindings for this mode using modeTable."""
        
        t = self.c.frame.statusText
        
        self.unbindAll()
    
        t.bind("<Key-Escape>",self.exitMode)
    #@nonl
    #@-node:ekr.20041026101757.2:initBindings
    #@+node:ekr.20041026103800.2:statusLine proxies
    def clearStatusLine (self):
        self.c.frame.clearStatusLine()
    
    def disableStatusLine (self):
        # g.trace()
        self.c.frame.disableStatusLine()
    
    def enableStatusLine (self):
        # g.trace()
        self.c.frame.enableStatusLine()
        
    def getStatusLine (self):
        return self.c.frame.getStatusLine()
    
    def putStatusLine(self,s,color="black"):
        self.c.frame.putStatusLine(s,color=color)
        
    def setFocusStatusLine(self):
        # g.trace()
        self.c.frame.setFocusStatusLine()
        
    def statusLineIsEnabled(self):
        return self.c.frame.statusLineIsEnabled()
    #@nonl
    #@-node:ekr.20041026103800.2:statusLine proxies
    #@+node:ekr.20041026171123:unbindAll
    def unbindAll (self):
        
        t = self.c.frame.statusText
        
        for b in t.bind():
            t.unbind(b)
    #@nonl
    #@-node:ekr.20041026171123:unbindAll
    #@-others
#@nonl
#@-node:ekr.20041026101757:class baseInputMode
#@+node:ekr.20041026122011:class topInputMode (baseInputMode)
class topInputMode (baseInputMode):
    
    """A class to represent the top-level input mode in the status line."""
    
    #@    @+others
    #@+node:ekr.20041026122415:ctor
    def __init__(self,c,statusLineClass):
        
        baseInputMode.__init__(self,c,statusLineClass)
    
        self.name = "topInputMode"
        
        
    #@nonl
    #@-node:ekr.20041026122415:ctor
    #@+node:ekr.20041026203704:finishCreate
    def finishCreate(self):
        
        s = self.statusLine
        
        self.bindings = (
            ('c','Change',s.findChangeMode),
            ('e','Edit',None),
            ('f','Find',s.findMode),
            ('h','Help',None),
            ('o','Outline',None),
            ('p','oPtions',s.optionsMode),
        )
    
        signon = ["%s: " % (text) for ch,text,f in self.bindings]
        self.signon = ''.join(signon)
    #@nonl
    #@-node:ekr.20041026203704:finishCreate
    #@+node:ekr.20041026122415.1:initBindings
    def initBindings (self):
        
        """Create key bindings for this mode using modeTable."""
        
        t = self.c.frame.statusText
    
        self.unbindAll()
        
        t.bind("<Key>",self.doNothing)
        t.bind("<Key-Escape>",self.exitMode)
        
        for ch,text,f in self.bindings:
    
            def callback(event,self=self,ch=ch,text=text,f=f):
                return self.doKey(ch,text,f)
    
            t.bind("<Key-%s>" % ch, callback)
    #@nonl
    #@-node:ekr.20041026122415.1:initBindings
    #@+node:ekr.20041026134146:doKey
    def doKey (self,ch,text,f):
        
        ch = ch.lower()
        
        if f is not None:
            self.exitMode(nextMode=f)
        else:
             g.trace(text)
             
        return "break"
        
        if ch == 'c':
            self.exitMode(nextMode=self.statusLine.findChangeMode)
        elif ch == 'f':
            self.exitMode(nextMode=self.statusLine.findMode)
        elif ch == 'p':
            self.exitMode(nextMode=self.statusLine.optionsMode)
        else:
            g.trace(text)
            # self.putStatusLine(text + ": ")
    
        return "break"
    #@nonl
    #@-node:ekr.20041026134146:doKey
    #@-others
#@nonl
#@-node:ekr.20041026122011:class topInputMode (baseInputMode)
#@+node:ekr.20041026132235:class optionsInputMode (baseInputMode)
class optionsInputMode (baseInputMode):
    
    """An input mode to set find/change options."""
    
    #@    @+others
    #@+node:ekr.20041026132301:ctor
    def __init__(self,c,statusLineClass):
        
        baseInputMode.__init__(self,c,statusLineClass)
        
        self.name = "optionsMode"
        self.clear = True
        self.findFrame = g.app.findFrame
        
        self.bindings = (
            ('a','Around','wrap'),
            ('b','Body','search_body'),
            ('e','Entire',None),
            ('h','Head','search_headline'),
            ('i','Ignore','ignore_case'),
            ('n','Node','node_only'),
            ('r','Reverse','reverse'),
            ('s','Suboutline','suboutline_only'),
            ('w','Word','whole_word'),
        )
        
        signon = ["%s " % (text) for ch,text,ivar in self.bindings]
        self.signon = ''.join(signon)
    #@nonl
    #@-node:ekr.20041026132301:ctor
    #@+node:ekr.20041026214436:enterMode
    def enterMode (self,event=None):
        
        baseInputMode.enterMode(self,event)
        
        # self.findFrame.top.withdraw()
        
        self.findFrame.bringToFront()
        
        # We need a setting that will cause the row/col update not to mess with the focus.
        # Or maybe we can just disable the row-col update.
        
        ### self.disableStatusLine()
    
        return "break"
    #@nonl
    #@-node:ekr.20041026214436:enterMode
    #@+node:ekr.20041026132504:initBindings
    def initBindings (self):
        
        """Create key bindings for this mode using modeTable."""
        
        t = self.c.frame.statusText
    
        self.unbindAll()
        
        t.bind("<Key>",self.doNothing)
        t.bind("<Key-Escape>",self.doEsc)
        t.bind("<Return>",self.doFindChange)
        t.bind("<Linefeed>",self.doFindChange)
    
        for ch,text,ivar in self.bindings:
    
            def callback(event,self=self,ch=ch,text=text,ivar=ivar):
                return self.doKey(ch,text,ivar)
    
            t.bind("<Key-%s>" % ch, callback)
    #@nonl
    #@-node:ekr.20041026132504:initBindings
    #@+node:ekr.20041026191941:doFindChange
    def doFindChange (self,event=None):
        
        g.trace(self.name)
    
        self.exitMode(nextMode=self.statusLine.topMode)
    
        return "break"
    #@nonl
    #@-node:ekr.20041026191941:doFindChange
    #@+node:ekr.20041026201316:doEsc
    def doEsc (self,event=None):
        
        # g.trace(self.name)
    
        self.exitMode(nextMode=self.statusLine.topMode)
    
        return "break"
    #@-node:ekr.20041026201316:doEsc
    #@+node:ekr.20041026133619:doKey
    def doKey (self,ch,text,ivar):
        
        if ivar:
            intVar = self.findFrame.dict.get(ivar)
            if intVar:
                val = intVar.get()
                g.trace(text,val)
                # Toggle the value.
                intVar.set(g.choose(val,0,1))
                
            # self.findFrame.bringToFront()
    
        return "break"
    #@nonl
    #@-node:ekr.20041026133619:doKey
    #@-others
#@nonl
#@-node:ekr.20041026132235:class optionsInputMode (baseInputMode)
#@+node:ekr.20041026140159:class textInputMode (baseInputMode):
class textInputMode (baseInputMode):
    
    """An input mode to set the find/change string."""
    
    #@    @+others
    #@+node:ekr.20041026140159.1:ctor
    def __init__(self,c,statusLineClass,change=False,willChange=False):
        
        baseInputMode.__init__(self,c,statusLineClass)
        
        if willChange:
            self.name = "findChangeTextMode"
            self.signon = "Replace: "
            self.clear = True
        elif change:
            self.name = "changeTextMode"
            self.signon = " By: "
            self.clear = False
        else:
            self.name = "findTextMode"
            self.signon = "Find: "
            self.clear = True
    
        self.change = change
        self.willChange = willChange
    #@-node:ekr.20041026140159.1:ctor
    #@+node:ekr.20041026164652:doFindChange
    def doFindChange (self,event=None):
        
        c = self.c
        
        # g.trace(self.name)
        
        s = self.getStatusLine()
        newText = s[len(self.originalLine):]
        if newText and newText[-1] == '\n':
            newText = newText [:-1]
        
        if self.change:
            self.statusLine.changeText = newText
        else:
            self.statusLine.findText = newText
    
        if self.willChange:
            nextMode = self.statusLine.changeMode
        elif self.change:
            g.trace("CHANGE",repr(self.statusLine.findText),"TO",repr(self.statusLine.changeText))
            nextMode = None
        else:
            f = g.app.findFrame
            g.trace("FIND",repr(self.statusLine.findText))
            if 0:
                f.setFindText(findText)
            else:
                f.find_text.delete("1.0","end")
                f.find_text.insert("end",self.statusLine.findText)
            f.findNextCommand(self.c)
            nextMode = None
    
        self.exitMode(nextMode=nextMode)
    
        return "break"
    #@-node:ekr.20041026164652:doFindChange
    #@+node:ekr.20041026142227:initBindings
    def initBindings (self):
        
        """Create key bindings for this mode using modeTable."""
        
        t = self.c.frame.statusText
        
        self.unbindAll()
    
        t.bind("<Key-Return>",self.doFindChange)
        t.bind("<Key-Linefeed>",self.doFindChange)
        t.bind("<Key-Escape>",self.doEsc)
        t.bind("<Key>",self.doKey)
    #@nonl
    #@-node:ekr.20041026142227:initBindings
    #@+node:ekr.20041026201151:doEsc
    def doEsc (self,event=None):
        
        # g.trace(self.name)
    
        self.exitMode(nextMode=self.statusLine.topMode)
    
        return "break"
    #@-node:ekr.20041026201151:doEsc
    #@+node:ekr.20041026142434:doKey
    def doKey (self,event=None):
        
        if event and event.keysym == "BackSpace":
            
            t = self.c.frame.statusText
            
            s = self.getStatusLine()
            
            # This won't work if we click in the frame.
            # Maybe we can disable the widget??
            if len(s) <= len(self.originalLine):
                return "break"
        
        return "continue"
    #@nonl
    #@-node:ekr.20041026142434:doKey
    #@-others
#@nonl
#@-node:ekr.20041026140159:class textInputMode (baseInputMode):
#@-others

if Tk and not g.app.unitTesting:

    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":
        leoPlugins.registerHandler("after-create-leo-frame", createStatusLine)
        g.plugin_signon(__name__)
#@nonl
#@-node:ekr.20040201060959:@thin status_line.py
#@-leo
