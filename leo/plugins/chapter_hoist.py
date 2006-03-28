#@+leo-ver=4-thin
#@+node:ekr.20060328125925:@thin chapter_hoist.py
#@<< docstring >>
#@+node:ekr.20060328125925.1:<< docstring >>
"""A plugin to create hoist buttons.  It is kind of a Chapters lite plugin

This plugin puts two buttons in the icon area: a button called 'Save Hoist' and
a button called 'Dehoist'.

The 'Save Hoist' button hoists the presently selected node and creates a button
which can later rehoist the same node.

The 'Dehoist' button performs one level of dehoisting

Requires at least version 0.19 of mod_scripting
"""
#@nonl
#@-node:ekr.20060328125925.1:<< docstring >>
#@nl
#@<< imports >>
#@+node:ekr.20060328125925.2:<< imports >>
import leoGlobals as g
import leoPlugins
from mod_scripting import scriptingController

Tk = g.importExtension('Tkinter',pluginName=__name__,verbose=True)
#@-node:ekr.20060328125925.2:<< imports >>
#@nl

__version__ = "0.2"
#@<< version history >>
#@+node:ekr.20060328125925.3:<< version history >>
#@+at
# 
# 0.1 btheado: initial creation.
# 0.2 EKR: changed to @thin.
#@-at
#@nonl
#@-node:ekr.20060328125925.3:<< version history >>
#@nl

#@+others
#@+node:ekr.20060328125925.4:init
def init ():
    
    ok = Tk and not g.app.unitTesting
    
    if ok:
        if g.app.gui is None:
            g.app.createTkGui(__file__)
            
        ok = g.app.gui.guiName() == "tkinter"

        if ok:
            # Note: call onCreate _after_ reading the .leo file.
            # That is, the 'after-create-leo-frame' hook is too early!
            leoPlugins.registerHandler(('new','open2'),onCreate)
            g.plugin_signon(__name__)
        
    return ok
#@nonl
#@-node:ekr.20060328125925.4:init
#@+node:ekr.20060328125925.5:onCreate
def onCreate (tag, keys):

    """Handle the onCreate event in the chapterHoist plugin."""
    
    c = keys.get('c')

    if c:
        sc = scriptingController(c)
        ch = chapterHoist(sc,c)
#@-node:ekr.20060328125925.5:onCreate
#@+node:ekr.20060328125925.6:class chapterHoist
class chapterHoist:
    #@    @+others
    #@+node:ekr.20060328125925.7: ctor
    def __init__ (self,sc,c):
        self.createSaveHoistButton(sc,c)
        self.createDehoistButton(sc,c)
    #@-node:ekr.20060328125925.7: ctor
    #@+node:ekr.20060328125925.8:createSaveHoistButton
    def createSaveHoistButton(self,sc,c):
        b = sc.createIconButton('Save Hoist', 'Create hoist button current node', bg='LightSteelBlue1')
        def saveHoistCallback(self=self,sc=sc,c=c):
            self.createChapterHoistButton(sc,c,c.currentPosition())
            c.hoist()
        b.configure(command=saveHoistCallback)
        return b
    #@nonl
    #@-node:ekr.20060328125925.8:createSaveHoistButton
    #@+node:ekr.20060328125925.9:createDehoistButton
    def createDehoistButton(self,sc,c):
        b = sc.createIconButton('Dehoist', 'Dehoist', bg='LightSteelBlue1')
        def dehoistCallback(c=c):
            c.dehoist()
        b.configure(command=dehoistCallback)
        return b
    #@nonl
    #@-node:ekr.20060328125925.9:createDehoistButton
    #@+node:ekr.20060328125925.10:createChapterHoistButton
    def createChapterHoistButton (self,sc,c,p):
        '''Generates a hoist button for the headline at the given position'''    
        h = p.headString()
        buttonText = sc.getButtonText(h)
        statusLine = "Hoist %s" % h
        b = sc.createIconButton(text=buttonText,statusLine=statusLine,bg='LightSteelBlue1')
        def deleteButtonCallback(event=None,sc=sc,b=b):
            sc.deleteButton(b)
                
        def hoistButtonCallback (event=None,c=c,p=p.copy()):
            while (c.canDehoist()):
                c.dehoist()
            c.selectPosition(p)
            c.hoist()
    
        b.configure(command=hoistButtonCallback)
        b.bind('<3>',deleteButtonCallback)
    #@-node:ekr.20060328125925.10:createChapterHoistButton
    #@-others
#@nonl
#@-node:ekr.20060328125925.6:class chapterHoist
#@-others
#@nonl
#@-node:ekr.20060328125925:@thin chapter_hoist.py
#@-leo
