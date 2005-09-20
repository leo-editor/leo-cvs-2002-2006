#@+leo-ver=4-thin
#@+node:ekr.20050723062822:@thin __core_emacs.py
''' A plugin to provide Emacs commands.
Soon to move to Leo's core.'''

# Based on temacs version .57

#@<< imports >>
#@+node:ekr.20050723062822.1:<< imports >>
import leoGlobals as g
import leoPlugins

import Tkinter as Tk

import leoTkinterFrame
import leoMenu
import leoTkinterMenu
#@-node:ekr.20050723062822.1:<< imports >>
#@nl

# Module globals:  original versions of methods.
# These are used to call the originals after executing the modified code.

orig_frame_finishCreate = None
orig_OnBodyKey = None

#@+others
#@+node:ekr.20050723062822.2:init
def init ():

    ok = Tk and not g.app.unitTesting

    if ok:
        if g.app.gui is None:
            g.app.createTkGui(__file__)

        ok = g.app.gui.guiName() == "tkinter"
        if ok:
            g.plugin_signon(__name__)
            #@            << override core methods >>
            #@+node:ekr.20050724080456:<< override core methods >>
            try:
                global orig_frame_finishCreate
                orig_frame_finishCreate = leoTkinterFrame.leoTkinterFrame.finishCreate
                leoTkinterFrame.leoTkinterFrame.finishCreate = frameFinishCreate
                    
                global orig_OnBodyKey
                orig_OnBodyKey = leoTkinterFrame.leoTkinterBody.onBodyKey
                leoTkinterFrame.leoTkinterBody.onBodyKey = modifyOnBodyKey
            
                leoMenu.leoMenu.defineMenuTables = modifyDefineMenuTables
                leoMenu.leoMenu.createMenusFromTables = modifyCreateMenusFromTables
                leoMenu.leoMenu.createEmacsMenuFromTable = createEmacsMenuFromTable
                leoMenu.leoMenu.defineEmacsMenuTables = defineEmacsMenuTables
            
            except Exception:
                g.es_exception()
                print 'overrides failed'
                ok = False
            #@nonl
            #@-node:ekr.20050724080456:<< override core methods >>
            #@nl

    # g.trace(ok)
    return ok
#@nonl
#@-node:ekr.20050723062822.2:init
#@+node:ekr.20050724074642.23:Overridden methods in Leo's core
#@+node:ekr.20050920121217:frameFinishCreate
def frameFinishCreate (self,c):
    
    '''Call frame.finishCreate with frame.useMiniBuffer = True.'''
    
    # g.trace()
    
    self.useMiniBuffer = True

    orig_frame_finishCreate(self,c)
#@nonl
#@-node:ekr.20050920121217:frameFinishCreate
#@+node:ekr.20050724074642.24:modifyOnBodyKey
def modifyOnBodyKey (self,event):
    
    '''stops Return and Tab from being processed if the Emacs instance has state.'''
    
    # Self is an instance of leoTkinterBody, so self.c is defined.
    c = self.c

    if event.char.isspace(): 
        if c.keyHandler.stateManager.hasState():
            # g.trace('hasState')
            return None # Must be None, not 'break'
    else:
        return orig_OnBodyKey(self,event)
#@nonl
#@-node:ekr.20050724074642.24:modifyOnBodyKey
#@+node:ekr.20050801090011:modifyDefineMenuTables & helper
def modifyDefineMenuTables (self):

    self.defineEditMenuTables()
    self.defineFileMenuTables()
    self.defineOutlineMenuTables()
    self.defineWindowMenuTables()
    self.defineEmacsMenuTables() # New menu.
    self.defineHelpMenuTables()
#@nonl
#@+node:ekr.20050801093531:defineEmacsMenuTables
def defineEmacsMenuTables (self):
    
    def dummyCommand():
        g.trace()
    
    self.emacsMenuCmdsMenuTable = [
        ('Cmnd Command 1',None,dummyCommand),
    ]
    
    self.emacsMenuToolsMenuTable = [
        ('Tools Command 1',None,dummyCommand),
    ]

    self.emacsMenuOptionsMenuTable = [
        ('Options Command 1',None,dummyCommand),
    ]

    self.emacsMenuBuffersMenuTable = [
        ('Buffers Command 1',None,dummyCommand),
    ]
#@nonl
#@-node:ekr.20050801093531:defineEmacsMenuTables
#@-node:ekr.20050801090011:modifyDefineMenuTables & helper
#@+node:ekr.20050801093531.1:modifyCreateMenusFromTables & helper
def modifyCreateMenusFromTables (self):
    
    c = self.c
    
    self.createFileMenuFromTable()
    self.createEditMenuFromTable()
    self.createOutlineMenuFromTable()

    g.doHook("create-optional-menus",c=c)

    self.createWindowMenuFromTable()
    self.createEmacsMenuFromTable() # New menu.
    self.createHelpMenuFromTable()
#@nonl
#@+node:ekr.20050801093531.2:createEmacsMenuFromTable
def createEmacsMenuFromTable (self):

    emacsMenu = self.createNewMenu("Emacs")

    for name,table,sep in (
        #('View...',   self.emacsMenuViewMenuTable,    True),
        ('Cmds...',    self.emacsMenuCmdsMenuTable,    True),
        ('Tools...',   self.emacsMenuToolsMenuTable,   True),
        ('Options...', self.emacsMenuOptionsMenuTable, True),
        ('Buffers...', self.emacsMenuBuffersMenuTable, False),
    ):
        menu = self.createNewMenu(name,"Emacs")
        self.createMenuEntries(menu,table,init=True)
        if sep: self.add_separator(emacsMenu)
#@nonl
#@-node:ekr.20050801093531.2:createEmacsMenuFromTable
#@-node:ekr.20050801093531.1:modifyCreateMenusFromTables & helper
#@-node:ekr.20050724074642.23:Overridden methods in Leo's core
#@-others
#@nonl
#@-node:ekr.20050723062822:@thin __core_emacs.py
#@-leo
