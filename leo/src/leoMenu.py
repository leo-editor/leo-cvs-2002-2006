#@+leo-ver=4-thin
#@+node:ekr.20031218072017.3749:@thin leoMenu.py
"""Gui-independent menu handling for Leo."""

#@@language python
#@@tabwidth -4
#@@pagewidth 80

import leoGlobals as g
import string
import sys

#@+others
#@+node:ekr.20031218072017.3750:class leoMenu
class leoMenu:
    
    """The base class for all Leo menus."""
    
    __pychecker__ = '--no-argsused' # base classes have many unused args.

    #@    @+others
    #@+node:ekr.20031218072017.3751: leoMenu.__init__
    def __init__ (self,frame):
        
        self.c = c = frame.c
        self.frame = frame
        self.menus = {} # Menu dictionary.
        self.menuShortcuts = {}
        
        # To aid transition to emacs-style key handling.
        self.useCmdMenu = c.config.getBool('useCmdMenu')
        
        self.newBinding = True
            # True if using new binding scheme.
            # You can set this to False in an emergency to revert to the old way.
    
        self.defineMenuTables()
    #@nonl
    #@-node:ekr.20031218072017.3751: leoMenu.__init__
    #@+node:ekr.20031218072017.3775:oops
    def oops (self):
    
        print "leoMenu oops:", g.callerName(2), "should be overridden in subclass"
    #@nonl
    #@-node:ekr.20031218072017.3775:oops
    #@+node:ekr.20031218072017.3776:Gui-independent menu enablers
    #@+node:ekr.20031218072017.3777:updateAllMenus
    def updateAllMenus (self):
        
        """The Tk "postcommand" callback called when a click happens in any menu.
        
        Updates (enables or disables) all menu items."""
    
        # Allow the user first crack at updating menus.
        c = self.c
        c.setLog()
        p = c.currentPosition()
    
        if not g.doHook("menu2",c=c,p=p,v=p):
            self.updateFileMenu()
            self.updateEditMenu()
            self.updateOutlineMenu()
    #@nonl
    #@-node:ekr.20031218072017.3777:updateAllMenus
    #@+node:ekr.20031218072017.3778:updateFileMenu
    def updateFileMenu (self):
        
        c = self.c ; frame = c.frame
        if not c: return
    
        try:
            enable = frame.menu.enableMenu
            menu = frame.menu.getMenu("File")
            enable(menu,"Revert To Saved", c.canRevert())
            enable(menu,"Open With...", g.app.hasOpenWithMenu)
        except:
            g.es("exception updating File menu")
            g.es_exception()
    #@nonl
    #@-node:ekr.20031218072017.3778:updateFileMenu
    #@+node:ekr.20031218072017.836:updateEditMenu
    def updateEditMenu (self):
    
        c = self.c ; frame = c.frame ; gui = g.app.gui
        if not c: return
        try:
            # Top level Edit menu...
            enable = frame.menu.enableMenu
            menu = frame.menu.getMenu("Edit")
            c.undoer.enableMenuItems()
            #@        << enable cut/paste >>
            #@+node:ekr.20040130164211:<< enable cut/paste >>
            if frame.body.hasFocus():
                data = frame.body.getSelectedText()
                canCut = data and len(data) > 0
            else:
                # This isn't strictly correct, but we can't get the Tk headline selection.
                canCut = True
            
            enable(menu,"Cut",canCut)
            enable(menu,"Copy",canCut)
            
            data = gui.getTextFromClipboard()
            canPaste = data and len(data) > 0
            enable(menu,"Paste",canPaste)
            #@nonl
            #@-node:ekr.20040130164211:<< enable cut/paste >>
            #@nl
            if 0: # Always on for now.
                menu = frame.menu.getMenu("Find...")
                enable(menu,"Find Next",c.canFind())
                flag = c.canReplace()
                enable(menu,"Replace",flag)
                enable(menu,"Replace, Then Find",flag)
            # Edit Body submenu...
            menu = frame.menu.getMenu("Edit Body...")
            enable(menu,"Extract Section",c.canExtractSection())
            enable(menu,"Extract Names",c.canExtractSectionNames())
            enable(menu,"Extract",c.canExtract())
            enable(menu,"Match Brackets",c.canFindMatchingBracket())
        except:
            g.es("exception updating Edit menu")
            g.es_exception()
    #@nonl
    #@-node:ekr.20031218072017.836:updateEditMenu
    #@+node:ekr.20031218072017.3779:updateOutlineMenu
    def updateOutlineMenu (self):
    
        c = self.c ; frame = c.frame
        if not c: return
    
        p = c.currentPosition()
        hasParent = p.hasParent()
        hasBack = p.hasBack()
        hasNext = p.hasNext()
        hasChildren = p.hasChildren()
        isExpanded = p.isExpanded()
        isCloned = p.isCloned()
        isMarked = p.isMarked()
    
        try:
            enable = frame.menu.enableMenu
            #@        << enable top level outline menu >>
            #@+node:ekr.20040131171020:<< enable top level outline menu >>
            menu = frame.menu.getMenu("Outline")
            enable(menu,"Cut Node",c.canCutOutline())
            enable(menu,"Delete Node",c.canDeleteHeadline())
            enable(menu,"Paste Node",c.canPasteOutline())
            enable(menu,"Paste Node As Clone",c.canPasteOutline())
            enable(menu,"Clone Node",c.canClone()) # 1/31/04
            enable(menu,"Sort Siblings",c.canSortSiblings())
            enable(menu,"Hoist",c.canHoist())
            enable(menu,"De-Hoist",c.canDehoist())
            #@nonl
            #@-node:ekr.20040131171020:<< enable top level outline menu >>
            #@nl
            #@        << enable expand/contract submenu >>
            #@+node:ekr.20040131171020.1:<< enable expand/Contract submenu >>
            menu = frame.menu.getMenu("Expand/Contract...")
            enable(menu,"Contract Parent",c.canContractParent())
            enable(menu,"Contract Node",hasChildren and isExpanded)
            enable(menu,"Contract Or Go Left",(hasChildren and isExpanded) or hasParent)
            enable(menu,"Expand Node",hasChildren and not isExpanded)
            enable(menu,"Expand Prev Level",hasChildren and isExpanded)
            enable(menu,"Expand Next Level",hasChildren)
            enable(menu,"Expand To Level 1",hasChildren and isExpanded)
            enable(menu,"Expand Or Go Right",hasChildren)
            for i in xrange(2,9):
                frame.menu.enableMenu(menu,"Expand To Level " + str(i), hasChildren)
            #@nonl
            #@-node:ekr.20040131171020.1:<< enable expand/Contract submenu >>
            #@nl
            #@        << enable move submenu >>
            #@+node:ekr.20040131171020.2:<< enable move submenu >>
            menu = frame.menu.getMenu("Move...")
            enable(menu,"Move Down",c.canMoveOutlineDown())
            enable(menu,"Move Left",c.canMoveOutlineLeft())
            enable(menu,"Move Right",c.canMoveOutlineRight())
            enable(menu,"Move Up",c.canMoveOutlineUp())
            enable(menu,"Promote",c.canPromote())
            enable(menu,"Demote",c.canDemote())
            #@nonl
            #@-node:ekr.20040131171020.2:<< enable move submenu >>
            #@nl
            #@        << enable go to submenu >>
            #@+node:ekr.20040131171020.3:<< enable go to submenu >>
            menu = frame.menu.getMenu("Go To...")
            enable(menu,"Go Prev Visited",c.beadPointer > 1)
            enable(menu,"Go Next Visited",c.beadPointer + 1 < len(c.beadList))
            enable(menu,"Go To Prev Visible",c.canSelectVisBack())
            enable(menu,"Go To Next Visible",c.canSelectVisNext())
            if 0: # These are too slow.
                enable(menu,"Go To Next Marked",c.canGoToNextMarkedHeadline())
                enable(menu,"Go To Next Changed",c.canGoToNextDirtyHeadline())
            enable(menu,"Go To Next Clone",isCloned)
            enable(menu,"Go To Prev Node",c.canSelectThreadBack())
            enable(menu,"Go To Next Node",c.canSelectThreadNext())
            enable(menu,"Go To Parent",hasParent)
            enable(menu,"Go To Prev Sibling",hasBack)
            enable(menu,"Go To Next Sibling",hasNext)
            #@nonl
            #@-node:ekr.20040131171020.3:<< enable go to submenu >>
            #@nl
            #@        << enable mark submenu >>
            #@+node:ekr.20040131171020.4:<< enable mark submenu >>
            menu = frame.menu.getMenu("Mark/Unmark...")
            label = g.choose(isMarked,"Unmark","Mark")
            frame.menu.setMenuLabel(menu,0,label)
            enable(menu,"Mark Subheads",hasChildren)
            if 0: # These are too slow.
                enable(menu,"Mark Changed Items",c.canMarkChangedHeadlines())
                enable(menu,"Mark Changed Roots",c.canMarkChangedRoots())
            enable(menu,"Mark Clones",isCloned)
            #@nonl
            #@-node:ekr.20040131171020.4:<< enable mark submenu >>
            #@nl
        except:
            g.es("exception updating Outline menu")
            g.es_exception()
    #@nonl
    #@-node:ekr.20031218072017.3779:updateOutlineMenu
    #@+node:ekr.20031218072017.3780:hasSelection
    # Returns True if text in the outline or body text is selected.
    
    def hasSelection (self):
        
        body = self.frame.body
    
        if body:
            first, last = body.getTextSelection()
            return first != last
        else:
            return False
    #@nonl
    #@-node:ekr.20031218072017.3780:hasSelection
    #@-node:ekr.20031218072017.3776:Gui-independent menu enablers
    #@+node:ekr.20031218072017.3781:Gui-independent menu routines
    #@+node:ekr.20051022053758: Top level
    #@+node:ekr.20031218072017.3784:createMenuItemsFromTable
    def createMenuItemsFromTable (self,menuName,table,dynamicMenu=False):
        
        try:
            menu = self.getMenu(menuName)
            if menu == None:
                print "menu does not exist: ",menuName
                g.es("menu does not exist: ",menuName)
                return
            self.createMenuEntries(menu,table,dynamicMenu=dynamicMenu)
        except:
            s = "exception creating items for %s menu" % menuName
            g.es_print(s)
            g.es_exception()
            
        g.app.menuWarningsGiven = True
    #@nonl
    #@-node:ekr.20031218072017.3784:createMenuItemsFromTable
    #@+node:ekr.20031218072017.3785:createMenusFromTables & helpers
    def createMenusFromTables (self):
        
        c = self.c
        
        self.createFileMenuFromTable()
        self.createEditMenuFromTable()
        self.createOutlineMenuFromTable()
        
        g.doHook("create-optional-menus",c=c)
        
        if self.useCmdMenu:
            self.createEditorMenuFromTable()
    
        self.createWindowMenuFromTable()
        self.createHelpMenuFromTable()
    #@nonl
    #@+node:ekr.20031218072017.3790:createFileMenuFromTable
    def createFileMenuFromTable (self):
        
        c = self.c
        fileMenu = self.createNewMenu("&File")
        self.createMenuEntries(fileMenu,self.fileMenuTopTable)
        self.createNewMenu("Open &With...","File")
        self.createMenuEntries(fileMenu,self.fileMenuTop2Table)
        #@    << create the recent files submenu >>
        #@+node:ekr.20031218072017.3791:<< create the recent files submenu >>
        self.createNewMenu("Recent &Files...","File")
        c.recentFiles = c.config.getRecentFiles()
        
        if 0: # Not needed, and causes problems in wxWindows...
            self.createRecentFilesMenuItems()
        #@nonl
        #@-node:ekr.20031218072017.3791:<< create the recent files submenu >>
        #@nl
        self.add_separator(fileMenu)
        #@    << create the read/write submenu >>
        #@+node:ekr.20031218072017.3792:<< create the read/write submenu >>
        readWriteMenu = self.createNewMenu("&Read/Write...","File")
        
        self.createMenuEntries(readWriteMenu,self.fileMenuReadWriteMenuTable)
        #@nonl
        #@-node:ekr.20031218072017.3792:<< create the read/write submenu >>
        #@nl
        #@    << create the tangle submenu >>
        #@+node:ekr.20031218072017.3793:<< create the tangle submenu >>
        tangleMenu = self.createNewMenu("&Tangle...","File")
        
        self.createMenuEntries(tangleMenu,self.fileMenuTangleMenuTable)
        #@nonl
        #@-node:ekr.20031218072017.3793:<< create the tangle submenu >>
        #@nl
        #@    << create the untangle submenu >>
        #@+node:ekr.20031218072017.3794:<< create the untangle submenu >>
        untangleMenu = self.createNewMenu("&Untangle...","File")
        
        self.createMenuEntries(untangleMenu,self.fileMenuUntangleMenuTable)
        #@nonl
        #@-node:ekr.20031218072017.3794:<< create the untangle submenu >>
        #@nl
        #@    << create the import submenu >>
        #@+node:ekr.20031218072017.3795:<< create the import submenu >>
        importMenu = self.createNewMenu("&Import...","File")
        
        self.createMenuEntries(importMenu,self.fileMenuImportMenuTable)
        #@nonl
        #@-node:ekr.20031218072017.3795:<< create the import submenu >>
        #@nl
        #@    << create the export submenu >>
        #@+node:ekr.20031218072017.3796:<< create the export submenu >>
        exportMenu = self.createNewMenu("&Export...","File")
        
        self.createMenuEntries(exportMenu,self.fileMenuExportMenuTable)
        #@nonl
        #@-node:ekr.20031218072017.3796:<< create the export submenu >>
        #@nl
        self.add_separator(fileMenu)
        self.createMenuEntries(fileMenu,self.fileMenuTop3MenuTable)
    #@nonl
    #@-node:ekr.20031218072017.3790:createFileMenuFromTable
    #@+node:ekr.20031218072017.3786:createEditMenuFromTable
    def createEditMenuFromTable (self):
    
        editMenu = self.createNewMenu("&Edit")
        self.createMenuEntries(editMenu,self.editMenuTopTable)
    
        #@    << create the edit body submenu >>
        #@+node:ekr.20031218072017.3787:<< create the edit body submenu >>
        editBodyMenu = self.createNewMenu("Edit &Body...","Edit")
        
        self.createMenuEntries(editBodyMenu,self.editMenuEditBodyTable)
        #@nonl
        #@-node:ekr.20031218072017.3787:<< create the edit body submenu >>
        #@nl
        #@    << create the edit headline submenu >>
        #@+node:ekr.20031218072017.3788:<< create the edit headline submenu >>
        editHeadlineMenu = self.createNewMenu("Edit &Headline...","Edit")
        
        self.createMenuEntries(editHeadlineMenu,self.editMenuEditHeadlineTable)
        #@nonl
        #@-node:ekr.20031218072017.3788:<< create the edit headline submenu >>
        #@nl
        #@    << create the find submenu >>
        #@+node:ekr.20031218072017.3789:<< create the find submenu >>
        findMenu = self.createNewMenu("&Find...","Edit")
        
        self.createMenuEntries(findMenu,self.editMenuFindMenuTable)
        #@nonl
        #@-node:ekr.20031218072017.3789:<< create the find submenu >>
        #@nl
        
        self.createMenuEntries(editMenu,self.editMenuTop2Table)
    #@nonl
    #@-node:ekr.20031218072017.3786:createEditMenuFromTable
    #@+node:ekr.20031218072017.3797:createOutlineMenuFromTable
    def createOutlineMenuFromTable (self):
    
        outlineMenu = self.createNewMenu("&Outline")
        
        self.createMenuEntries(outlineMenu,self.outlineMenuTopMenuTable)
        
        #@    << create check submenu >>
        #@+node:ekr.20040711140738.1:<< create check submenu >>
        checkOutlineMenu = self.createNewMenu("Chec&k...","Outline")
        
        self.createMenuEntries(checkOutlineMenu,self.outlineMenuCheckOutlineMenuTable)
        #@nonl
        #@-node:ekr.20040711140738.1:<< create check submenu >>
        #@nl
        #@    << create expand/contract submenu >>
        #@+node:ekr.20031218072017.3798:<< create expand/contract submenu >>
        expandMenu = self.createNewMenu("E&xpand/Contract...","Outline")
        
        self.createMenuEntries(expandMenu,self.outlineMenuExpandContractMenuTable)
        #@nonl
        #@-node:ekr.20031218072017.3798:<< create expand/contract submenu >>
        #@nl
        #@    << create move submenu >>
        #@+node:ekr.20031218072017.3799:<< create move submenu >>
        moveSelectMenu = self.createNewMenu("&Move...","Outline")
        
        self.createMenuEntries(moveSelectMenu,self.outlineMenuMoveMenuTable)
        #@nonl
        #@-node:ekr.20031218072017.3799:<< create move submenu >>
        #@nl
        #@    << create mark submenu >>
        #@+node:ekr.20031218072017.3800:<< create mark submenu >>
        markMenu = self.createNewMenu("M&ark/Unmark...","Outline")
        
        self.createMenuEntries(markMenu,self.outlineMenuMarkMenuTable)
        #@nonl
        #@-node:ekr.20031218072017.3800:<< create mark submenu >>
        #@nl
        #@    << create goto submenu >>
        #@+node:ekr.20031218072017.3801:<< create goto submenu >>
        gotoMenu = self.createNewMenu("&Go To...","Outline")
        
        self.createMenuEntries(gotoMenu,self.outlineMenuGoToMenuTable)
        #@nonl
        #@-node:ekr.20031218072017.3801:<< create goto submenu >>
        #@nl
    #@nonl
    #@-node:ekr.20031218072017.3797:createOutlineMenuFromTable
    #@+node:ekr.20050921103736:createEditorMenuFromTable
    def createEditorMenuFromTable (self):
    
        cmdsMenu = self.createNewMenu('C&mds')
    
        for name,table,sep in (
            #('View...',   self.emacsMenuViewMenuTable,    True),
            ('Commands...',self.emacsMenuCommandsMenuTable,True),
            ('Tools...',   self.emacsMenuToolsMenuTable,   True),
            ('Options...', self.emacsMenuOptionsMenuTable, True),
            ('Buffers...', self.emacsMenuBuffersMenuTable, False),
        ):
            menu = self.createNewMenu(name,'Cmds')
            self.createMenuEntries(menu,table)
            if sep: self.add_separator(cmdsMenu)
    #@nonl
    #@-node:ekr.20050921103736:createEditorMenuFromTable
    #@+node:ekr.20031218072017.3802:createWindowMenuFromTable
    def createWindowMenuFromTable (self):
    
        windowMenu = self.createNewMenu("&Window")
        
        self.createMenuEntries(windowMenu,self.windowMenuTopTable)
    #@nonl
    #@-node:ekr.20031218072017.3802:createWindowMenuFromTable
    #@+node:ekr.20031218072017.3803:createHelpMenuFromTable
    def createHelpMenuFromTable (self):
    
        helpMenu = self.createNewMenu("&Help")
        
        self.createMenuEntries(helpMenu,self.helpMenuTopTable)
        
        if sys.platform=="win32":
            self.createMenuEntries(helpMenu,self.helpMenuTop2Table)
        
        self.createMenuEntries(helpMenu,self.helpMenuTop3Table)
    #@nonl
    #@-node:ekr.20031218072017.3803:createHelpMenuFromTable
    #@-node:ekr.20031218072017.3785:createMenusFromTables & helpers
    #@+node:ekr.20031218072017.3804:createNewMenu (contains Tk code)
    def createNewMenu (self,menuName,parentName="top",before=None):
    
        try:
            parent = self.getMenu(parentName) # parent may be None.
            menu = self.getMenu(menuName)
            if menu:
                g.es("menu already exists: " + menuName,color="red")
            else:
                menu = self.new_menu(parent,tearoff=0)
                self.setMenu(menuName,menu)
                label = self.getRealMenuName(menuName)
                amp_index = label.find("&")
                label = label.replace("&","")
                if before: # Insert the menu before the "before" menu.
                    index_label = self.getRealMenuName(before)
                    amp_index = index_label.find("&")
                    index_label = index_label.replace("&","")
                    index = parent.index(index_label)
                    self.insert_cascade(parent,index=index,label=label,menu=menu,underline=amp_index)
                else:
                    self.add_cascade(parent,label=label,menu=menu,underline=amp_index)
                return menu
        except:
            g.es("exception creating " + menuName + " menu")
            g.es_exception()
            return None
    #@nonl
    #@-node:ekr.20031218072017.3804:createNewMenu (contains Tk code)
    #@+node:ekr.20031218072017.4116:createOpenWithMenuFromTable
    #@+at 
    #@nonl
    # Entries in the table passed to createOpenWithMenuFromTable are
    # tuples of the form (commandName,shortcut,data).
    # 
    # - command is one of "os.system", "os.startfile", "os.spawnl", 
    # "os.spawnv" or "exec".
    # - shortcut is a string describing a shortcut, just as for 
    # createMenuItemsFromTable.
    # - data is a tuple of the form (command,arg,ext).
    # 
    # Leo executes command(arg+path) where path is the full path to the temp 
    # file.
    # If ext is not None, the temp file has the given extension.
    # Otherwise, Leo computes an extension based on the @language directive in 
    # effect.
    #@-at
    #@@c
    
    def createOpenWithMenuFromTable (self,table):
    
        c = self.c
        g.app.openWithTable = table # Override any previous table.
        # Delete the previous entry.
        parent = self.getMenu("File")
        label = self.getRealMenuName("Open &With...")
        amp_index = label.find("&")
        label = label.replace("&","")
        try:
            index = parent.index(label)
            parent.delete(index)
        except:
            try:
                index = parent.index("Open With...")
                parent.delete(index)
            except: return
        # Create the Open With menu.
        openWithMenu = self.createOpenWithMenu(parent,label,index,amp_index)
        self.setMenu("Open With...",openWithMenu)
        # Create the menu items in of the Open With menu.
        for entry in table:
            if len(entry) != 3: # 6/22/03
                g.es("createOpenWithMenuFromTable: invalid data",color="red")
                return
        self.createOpenWithMenuItemsFromTable(openWithMenu,table)
        for entry in table:
            name,shortcut,data = entry
            c.keyHandler.bindOpenWith (shortcut,name,data)
    #@-node:ekr.20031218072017.4116:createOpenWithMenuFromTable
    #@+node:ekr.20031218072017.2078:createRecentFilesMenuItems (leoMenu)
    def createRecentFilesMenuItems (self):
        
        c = self.c
        recentFilesMenu = self.getMenu("Recent Files...")
        
        # Delete all previous entries.
        self.delete_range(recentFilesMenu,0,len(c.recentFiles)+2)
        
        # Create the first two entries.
        table = (
            ("Clear Recent Files",None,c.clearRecentFiles),
            ("-",None,None))
        self.createMenuEntries(recentFilesMenu,table)
        
        # Create all the other entries.
        i = 3
        for name in c.recentFiles:
            def recentFilesCallback (event=None,c=c,name=name):
                __pychecker__ = '--no-argsused' # event not used, but must be present.
                c.openRecentFile(name)
            label = "%d %s" % (i-2,g.computeWindowTitle(name))
            self.add_command(recentFilesMenu,label=label,command=recentFilesCallback,underline=0)
            i += 1
    #@nonl
    #@-node:ekr.20031218072017.2078:createRecentFilesMenuItems (leoMenu)
    #@+node:ekr.20031218072017.3752:defineMenuTables & helpers
    def defineMenuTables (self):
        
        c = self.c
        
        self.defineEditMenuTables()
        self.defineFileMenuTables()
        self.defineOutlineMenuTables()
        self.defineWindowMenuTables()
    
        if self.useCmdMenu:
            self.defineEditorMenuTables()
    
        self.defineHelpMenuTables()
    #@nonl
    #@+node:ekr.20031218072017.3753:defineEditMenuTables & helpers
    def defineEditMenuTables (self):
    
        self.defineEditMenuTopTable()
        self.defineEditMenuEditCursorTable()
        self.defineEditMenuEditBodyTable()
        self.defineEditMenuEditHeadlineTable()
        self.defineEditMenuFindMenuTable()
        self.defineEditMenuTop2Table()
    #@nonl
    #@+node:ekr.20031218072017.839:defineEditMenuTopTable
    def defineEditMenuTopTable (self):
        
        __pychecker__ = 'no-unusednames=[f]' # We define 'f' just in case.
    
        c = self.c ; f = self.frame
        
        self.editMenuTopTable = [
            ("Can't Undo",c.undoer.undo), # &U reserved for Undo
            ("Can't Redo",c.undoer.redo), # &R reserved for Redo
            ("-",None),
            ("Cu&t",f.OnCutFromMenu), 
            ("Cop&y",f.OnCopyFromMenu),
            ("&Paste",f.OnPasteFromMenu),
            ("&Delete",c.editCommands.backwardDeleteCharacter),
            ("Select &All",f.body.selectAllText),
            ("-",None),
        ]
    
        # Top-level shortcuts here:  a,d,p,t,u,y,z
        # Top-level shortcuts later: e,g,n,v
    #@nonl
    #@-node:ekr.20031218072017.839:defineEditMenuTopTable
    #@+node:ekr.20050711091931:defineEditMenuEditCursorTable
    def defineEditMenuEditCursorTable (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
    
        if 0: ### Not ready yet.
            # These should have Emacs names...
            self.editMenuEditCursorTable = [
                ('Delete Right',c.deleteRightChar), 
                ('Delete Left',c.deleteLeftChar), 
                # Moving the cursor.
                ('Start of Line',c.moveToStartOfLine), 
                ('End of Line',c.moveToEndOfLine), 
                ('Start of Node',c.moveToStartOfNode),
                ('End of Node',c.moveToEndOfNode), 
                ('-',None,None),
                # Extending the selection...
                ('Select Line',c.selectEntireLine),
                ('Extend To Start of Word',c.extendToStartOfWord),
                ('Extend To End of Word',c.extendToEndOfWord),
                ('Extend To Start Of Line',c.extendToStartOfLine), 
                ('Extend To End Of Line',c.extendToEndOfLine), 
                ('Extend To End of Node',c.extendToEndOfNode),
                # The mark...
            ]
    #@nonl
    #@-node:ekr.20050711091931:defineEditMenuEditCursorTable
    #@+node:ekr.20031218072017.3754:defineEditMenuEditBodyTable
    def defineEditMenuEditBodyTable (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
    
        self.editMenuEditBodyTable = [
            ("Extract &Section",c.extractSection),
            ("Extract &Names",c.extractSectionNames),
            ("&Extract",c.extract),
            ("-",None,None),
            ("Convert All B&lanks",c.convertAllBlanks),
            ("Convert All T&abs",c.convertAllTabs),
            ("Convert &Blanks",c.convertBlanks),
            ("Convert &Tabs",c.convertTabs),
            ("Insert Body Time/&Date",c.insertBodyTime),
            ("&Reformat Paragraph",c.reformatParagraph),
            ("-",None,None),
            ("&Indent",c.indentBody),
            ("&Unindent",c.dedentBody),
            ("&Match Brackets",c.findMatchingBracket),
            ("Add Comments",c.addComments),
            ("Delete Comments",c.deleteComments),
        ]
        # Shortcuts a,b,d,e,i,l,m,n,r,s,t,u
    #@nonl
    #@-node:ekr.20031218072017.3754:defineEditMenuEditBodyTable
    #@+node:ekr.20031218072017.3755:defineEditMenuEditHeadlineTable
    def defineEditMenuEditHeadlineTable (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
        
        self.editMenuEditHeadlineTable = [
            ("Edit &Headline",c.editHeadline),
            ("&End Edit Headline",f.endEditLabelCommand),
            ("&Abort Edit Headline",f.abortEditLabelCommand),
            ("Insert Headline Time/&Date",f.insertHeadlineTime),
            ("Toggle Angle Brackets",c.toggleAngleBrackets),
        ]
    #@nonl
    #@-node:ekr.20031218072017.3755:defineEditMenuEditHeadlineTable
    #@+node:ekr.20031218072017.3756:defineEditMenuFindMenuTable
    def defineEditMenuFindMenuTable (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
        
        if 1: # Bind to the Find tab.
            sc = c.searchCommands
            self.editMenuFindMenuTable = [
                ("&Show Find Tab",sc.openFindTab),
                ("&Hide Find Tab",sc.hideFindTab),
                ("-",None),
                ("Find &Next",          sc.findTabFindNext),
                ("Find &Previous",      sc.findTabFindPrev),
                ("&Replace",            sc.findTabChange),
                ("Replace, &Then Find", sc.findTabChangeThenFind),
            ]
        else: # Bind to deprecated Find dialog.
            self.editMenuFindMenuTable = [
                ("&Find Panel",c.showFindPanel),
                ("-",None),
                ("Find &Next",c.findNext),
                ("Find &Previous",c.findPrevious),
                ("&Replace",c.replace),
                ("Replace, &Then Find",c.replaceThenFind),
            ]
    #@nonl
    #@-node:ekr.20031218072017.3756:defineEditMenuFindMenuTable
    #@+node:ekr.20031218072017.3757:defineEditMenuTop2Table
    def defineEditMenuTop2Table (self):
        
        __pychecker__ = 'no-unusednames=c,f'
    
        c = self.c ; f = self.frame
    
        try:        show = c.frame.body.getColorizer().showInvisibles
        except:     show = False
        label = g.choose(show,"Hide In&visibles","Show In&visibles")
            
        self.editMenuTop2Table = [
            ("&Go To Line Number",c.goToLineNumber),
            ("&Execute Script",c.executeScript),
            (label,c.viewAllCharacters),
            ("Setti&ngs",c.preferences),
        ]
    
        # Top-level shortcuts earlier: a,d,p,t,u,y,z
        # Top-level shortcuts here: e,g,n,v
    #@nonl
    #@-node:ekr.20031218072017.3757:defineEditMenuTop2Table
    #@-node:ekr.20031218072017.3753:defineEditMenuTables & helpers
    #@+node:ekr.20031218072017.3758:defineFileMenuTables & helpers
    def defineFileMenuTables (self):
    
        self.defineFileMenuTopTable()
        self.defineFileMenuTop2Table()
        self.defineFileMenuReadWriteMenuTable()
        self.defineFileMenuTangleMenuTable()
        self.defineFileMenuUntangleMenuTable()
        self.defineFileMenuImportMenuTable()
        self.defineFileMenuExportMenuTable()
        self.defineFileMenuTop3MenuTable()
    #@nonl
    #@+node:ekr.20031218072017.3759:defineFileMenuTopTable
    def defineFileMenuTopTable (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
    
        self.fileMenuTopTable = [
            ("&New",c.new),
            ("&Open...",c.open),
        ]
    #@nonl
    #@-node:ekr.20031218072017.3759:defineFileMenuTopTable
    #@+node:ekr.20031218072017.3760:defineFileMenuTop2Table
    def defineFileMenuTop2Table (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
    
        self.fileMenuTop2Table = [
            ("-",None),
            ("&Close",c.close),
            ("&Save",c.save),
            ("Save &As",c.saveAs),
            ("Save To",c.saveTo), # &Tangle
            ("Re&vert To Saved",c.revert), # &Read/Write
        ]
    #@nonl
    #@-node:ekr.20031218072017.3760:defineFileMenuTop2Table
    #@+node:ekr.20031218072017.3761:defineFileMenuReadWriteMenuTable
    def defineFileMenuReadWriteMenuTable (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame ; fc = c.fileCommands
    
        self.fileMenuReadWriteMenuTable = [
            ("&Read Outline Only",c.readOutlineOnly),
            ("Read @file &Nodes",c.readAtFileNodes),
            ("-",None),
            ("Write &Dirty @file Nodes",fc.writeDirtyAtFileNodes),
            ("Write &Missing @file Nodes",fc.writeMissingAtFileNodes),
            ("Write &Outline Only",fc.writeOutlineOnly),
            ("&Write @file Nodes",fc.writeAtFileNodes),
        ]
    #@nonl
    #@-node:ekr.20031218072017.3761:defineFileMenuReadWriteMenuTable
    #@+node:ekr.20031218072017.3762:defineFileMenuTangleMenuTable
    def defineFileMenuTangleMenuTable (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
    
        self.fileMenuTangleMenuTable = [
            ("Tangle &All",c.tangleAll),
            ("Tangle &Marked",c.tangleMarked),
            ("&Tangle",c.tangle),
        ]
    #@nonl
    #@-node:ekr.20031218072017.3762:defineFileMenuTangleMenuTable
    #@+node:ekr.20031218072017.3763:defineFileMenuUntangleMenuTable
    def defineFileMenuUntangleMenuTable (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
    
        self.fileMenuUntangleMenuTable = [
            ("Untangle &All",c.untangleAll),
            ("Untangle &Marked",c.untangleMarked),
            ("&Untangle",c.untangle),
        ]
    #@nonl
    #@-node:ekr.20031218072017.3763:defineFileMenuUntangleMenuTable
    #@+node:ekr.20031218072017.3764:defineFileMenuImportMenuTable
    def defineFileMenuImportMenuTable (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
    
        self.fileMenuImportMenuTable = [
            ("Import Derived File",c.importDerivedFile),
            ("Import To @&file",c.importAtFile),
            ("Import To @&root",c.importAtRoot),
            ("Import &CWEB Files",c.importCWEBFiles),
            ("Import &noweb Files",c.importNowebFiles),
            ("Import Flattened &Outline",c.importFlattenedOutline),
        ]
    #@nonl
    #@-node:ekr.20031218072017.3764:defineFileMenuImportMenuTable
    #@+node:ekr.20031218072017.3765:defineFileMenuExportMenuTable
    def defineFileMenuExportMenuTable (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
    
        self.fileMenuExportMenuTable = [
            ("Export &Headlines",c.exportHeadlines),
            ("Outline To &CWEB",c.outlineToCWEB),
            ("Outline To &Noweb",c.outlineToNoweb),
            ("&Flatten Outline",c.flattenOutline),
            ("&Remove Sentinels",c.removeSentinels),
            ("&Weave",c.weave),
        ]
    #@nonl
    #@-node:ekr.20031218072017.3765:defineFileMenuExportMenuTable
    #@+node:ekr.20031218072017.3766:defineFileMenuTop3MenuTable
    def defineFileMenuTop3MenuTable (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
    
        self.fileMenuTop3MenuTable = [
            ("E&xit",g.app.onQuit),
        ]
    #@nonl
    #@-node:ekr.20031218072017.3766:defineFileMenuTop3MenuTable
    #@-node:ekr.20031218072017.3758:defineFileMenuTables & helpers
    #@+node:ekr.20031218072017.3767:defineOutlineMenuTables & helpers
    def defineOutlineMenuTables (self):
    
        self.defineOutlineMenuTopMenuTable()
        self.defineOutlineMenuCheckOutlineMenuTable()
        self.defineOutlineMenuExpandContractMenuTable()
        self.defineOutlineMenuMoveMenuTable()
        self.defineOutlineMenuMarkMenuTable()
        self.defineOutlineMenuGoToMenuTable()
    #@nonl
    #@+node:ekr.20031218072017.3768:defineOutlineMenuTopMenuTable
    def defineOutlineMenuTopMenuTable (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
    
        self.outlineMenuTopMenuTable = [
            ("C&ut Node",c.cutOutline),
            ("C&opy Node",c.copyOutline),
            ("&Paste Node",c.pasteOutline),
            ("Pas&te Node As Clone",c.pasteOutlineRetainingClones),
            ("&Delete Node",c.deleteOutline),
            ("-",None,None),
            ("&Insert Node",c.insertHeadline),
            ("&Clone Node",c.clone),
            ("Sort Childre&n",c.sortChildren), # Conflicted with Hoist.
            ("&Sort Siblings",c.sortSiblings),
            ("-",None),
            ("&Hoist",c.hoist),
            ("D&e-Hoist",f.c.dehoist),
            ("-",None),
        ]
        # Ampersand bindings:  a,c,d,e,h,i,n,o,p,t,s,
        # Bindings for entries that go to submenus: a,g,k,m,x
    #@nonl
    #@-node:ekr.20031218072017.3768:defineOutlineMenuTopMenuTable
    #@+node:ekr.20040711140738:defineOutlineMenuCheckOutlineMenuTable
    def defineOutlineMenuCheckOutlineMenuTable (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
    
        self.outlineMenuCheckOutlineMenuTable = [
            ("Check &Outline",c.checkOutline),
            ("&Dump Outline",c.dumpOutline),
            ("-",None),
            ("Check &All Python Code",c.checkAllPythonCode),
            ("&Check Python &Code",c.checkPythonCode),
            ("-",None),
            ("Pretty P&rint All Python Code",c.prettyPrintAllPythonCode),
            ("&Pretty Print Python Code",c.prettyPrintPythonCode),
        ]
        # shortcuts used: a,c,d,o,p,r
    #@nonl
    #@-node:ekr.20040711140738:defineOutlineMenuCheckOutlineMenuTable
    #@+node:ekr.20031218072017.3769:defineOutlineMenuExpandContractMenuTable
    def defineOutlineMenuExpandContractMenuTable (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
    
        self.outlineMenuExpandContractMenuTable = [
            ("&Contract All",c.contractAllHeadlines),
            ("Contract &Node",c.contractNode),
            ("Contract &Parent",c.contractParent),
            ("Contract Or Go Left",c.contractNodeOrGoToParent),
            ("-",None),
            ("Expand P&rev Level",c.expandPrevLevel),
            ("Expand N&ext Level",c.expandNextLevel),
            ("Expand And Go Right",c.expandNodeAndGoToFirstChild),
            ("Expand Or Go Right",c.expandNodeOrGoToFirstChild),
            ("-",None),
            ("Expand To Level &1",c.expandLevel1),
            ("Expand To Level &2",c.expandLevel2),
            ("Expand To Level &3",c.expandLevel3),
            ("Expand To Level &4",c.expandLevel4),
            ("Expand To Level &5",c.expandLevel5),
            ("Expand To Level &6",c.expandLevel6),
            ("Expand To Level &7",c.expandLevel7),
            ("Expand To Level &8",c.expandLevel8),
            ("-",None),
            ("Expand &All",c.expandAllHeadlines),
            ("Expand N&ode",c.expandNode),
        ]
    #@nonl
    #@-node:ekr.20031218072017.3769:defineOutlineMenuExpandContractMenuTable
    #@+node:ekr.20031218072017.3770:defineOutlineMenuMoveMenuTable
    def defineOutlineMenuMoveMenuTable (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
    
        self.outlineMenuMoveMenuTable = [
            ("Move &Down",c.moveOutlineDown),
            ("Move &Left",c.moveOutlineLeft),
            ("Move &Right",c.moveOutlineRight),
            ("Move &Up",c.moveOutlineUp),
            ("-",None),
            ("&Promote",c.promote),
            ("&Demote",c.demote),
        ]
    #@nonl
    #@-node:ekr.20031218072017.3770:defineOutlineMenuMoveMenuTable
    #@+node:ekr.20031218072017.3771:defineOutlineMenuMarkMenuTable
    def defineOutlineMenuMarkMenuTable (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
    
        self.outlineMenuMarkMenuTable = [
            ("&Mark",c.markHeadline),
            ("Mark &Subheads",c.markSubheads),
            ("Mark Changed &Items",c.markChangedHeadlines),
            ("Mark Changed &Roots",c.markChangedRoots),
            ("Mark &Clones",c.markClones),
            ("&Unmark All",c.unmarkAll),
        ]
    #@nonl
    #@-node:ekr.20031218072017.3771:defineOutlineMenuMarkMenuTable
    #@+node:ekr.20031218072017.3772:defineOutlineMenuGoToMenuTable
    def defineOutlineMenuGoToMenuTable (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
    
        self.outlineMenuGoToMenuTable = [
            ("Go Prev Visited",c.goPrevVisitedNode), # Usually use buttons for this.
            ("Go Next Visited",c.goNextVisitedNode),
            ("Go To Prev Node",c.selectThreadBack),
            ("Go To Next Node",c.selectThreadNext),
            ("-",None),
            ("Go To Next Marked",c.goToNextMarkedHeadline),
            ("Go To Next Changed",c.goToNextDirtyHeadline),
            ("Go To Next Clone",c.goToNextClone),
            ("-",None),
            ("Go To First Node",c.goToFirstNode),
            ("Go To Prev Visible",c.selectVisBack),
            ("Go To Next Visible",c.selectVisNext),
            ("Go To Last Node",c.goToLastNode),
            ('Go To Last Visible',c.goToLastVisibleNode),
            ("-",None),
            ("Go To Parent",c.goToParent),
            ('Go To First Sibling',c.goToFirstSibling),
            ('Go To Last Sibling',c.goToLastSibling),
            ("Go To Prev Sibling",c.goToPrevSibling),
            ("Go To Next Sibling",c.goToNextSibling),
        ]
    #@nonl
    #@-node:ekr.20031218072017.3772:defineOutlineMenuGoToMenuTable
    #@-node:ekr.20031218072017.3767:defineOutlineMenuTables & helpers
    #@+node:ekr.20050921103230:defineEditorMenuTables
    def defineEditorMenuTables (self):
        
        def dummyCommand():
            pass
        
        self.emacsMenuCommandsMenuTable = [
            ('Cmnd Command 1',dummyCommand),
        ]
        
        self.emacsMenuToolsMenuTable = [
            ('Tools Command 1',dummyCommand),
        ]
    
        self.emacsMenuOptionsMenuTable = [
            ('Options Command 1',dummyCommand),
        ]
    
        self.emacsMenuBuffersMenuTable = [
            ('Buffers Command 1',dummyCommand),
        ]
    #@nonl
    #@-node:ekr.20050921103230:defineEditorMenuTables
    #@+node:ekr.20031218072017.3773:defineWindowMenuTables
    def defineWindowMenuTables (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
    
        self.windowMenuTopTable = [
            ("&Equal Sized Panes",f.equalSizedPanes),
            ("Toggle &Active Pane",f.toggleActivePane),
            ("Toggle &Split Direction",f.toggleSplitDirection),
            ("-",None),
            ("Resize To Screen",f.resizeToScreen),
            ("Casca&de",f.cascade),
            ("&Minimize All",f.minimizeAll),
            ("-",None),
            ("Open &Compare Window",c.openCompareWindow),
            ("Open &Python Window",c.openPythonWindow),
        ]
    #@nonl
    #@-node:ekr.20031218072017.3773:defineWindowMenuTables
    #@+node:ekr.20031218072017.3774:defineHelpMenuTables
    def defineHelpMenuTables (self):
        
        __pychecker__ = 'no-unusednames=c,f'
        
        c = self.c ; f = self.frame
    
        self.helpMenuTopTable = [
            ("&About Leo...",c.about),
            ("Online &Home Page",c.leoHome),
            ("Open Online &Tutorial",c.leoTutorial),
        ]
    
        self.helpMenuTop2Table = [
            ("Open &Offline Tutorial",f.leoHelp),
        ]
    
        self.helpMenuTop3Table = [
            ("-",None,None),
            ("Open Leo&Docs.leo",c.leoDocumentation),
            ("Open Leo&Plugins.leo",c.openLeoPlugins),
            ("Open Leo&Settings.leo",c.openLeoSettings),
        ]
    #@nonl
    #@-node:ekr.20031218072017.3774:defineHelpMenuTables
    #@-node:ekr.20031218072017.3752:defineMenuTables & helpers
    #@+node:ekr.20031218072017.3805:deleteMenu
    def deleteMenu (self,menuName):
    
        try:
            menu = self.getMenu(menuName)
            if menu:
                self.destroy(menu)
                self.destroyMenu(menuName)
            else:
                g.es("can't delete menu: " + menuName)
        except:
            g.es("exception deleting " + menuName + " menu")
            g.es_exception()
    #@nonl
    #@-node:ekr.20031218072017.3805:deleteMenu
    #@+node:ekr.20031218072017.3806:deleteMenuItem
    def deleteMenuItem (self,itemName,menuName="top"):
        
        """Delete itemName from the menu whose name is menuName."""
    
        try:
            menu = self.getMenu(menuName)
            if menu:
                realItemName = self.getRealMenuName(itemName)
                self.delete(menu,realItemName)
            else:
                g.es("menu not found: " + menuName)
        except:
            g.es("exception deleting " + itemName + " from " + menuName + " menu")
            g.es_exception()
    #@nonl
    #@-node:ekr.20031218072017.3806:deleteMenuItem
    #@-node:ekr.20051022053758: Top level
    #@+node:ekr.20031218072017.1723:createMenuEntries
    def createMenuEntries (self,menu,table,dynamicMenu=False):
            
        '''Create a menu entry from the table.
        New in 4.4: this method shows the shortcut in the menu,
        but this method **never** binds any shortcuts.'''
        
        c = self.c ; f = c.frame ; k = c.keyHandler
        
        if g.app.unitTesting: return
    
        for data in table:
            #@        << get label & command or continue >>
            #@+node:ekr.20051021091958:<< get label & command or continue >>
            ok = (
                type(data) in (type(()), type([])) and
                len(data) in (2,3)
            )
                
            if ok:
                if len(data) == 2:
                    label,command = data
                else:
                    # New in 4.4: we ignore shortcuts bound in menu tables.
                    label,junk,command = data
            else:
                g.trace('bad data in menu table: %s' % repr(data))
                continue # Ignore bad data
                 
            if ok and label in (None,'-'):
                self.add_separator(menu)
                continue # That's all.
            #@nonl
            #@-node:ekr.20051021091958:<< get label & command or continue >>
            #@nl
            #@        << compute commandName & accel from label & command >>
            #@+node:ekr.20031218072017.1725:<< compute commandName & accel from label & command >>
            # First, get the old-style name.
            commandName = self.computeOldStyleShortcutKey(label)
            rawKey,bunchList = c.config.getShortcut(commandName)
            bunch = bunchList and bunchList[0]
            accel = bunch and bunch.val
            
            # Second, get new-style name.
            if not accel:
                #@    << compute emacs_name >>
                #@+node:ekr.20051021100806.1:<< compute emacs_name >>
                #@+at 
                #@nonl
                # One not-so-horrible kludge remains.
                # 
                # The cut/copy/paste commands in the menu tables are not the 
                # same as the methods
                # actually bound to cut/copy/paste-text minibuffer commands, 
                # so we must do a bit
                # of extra translation to discover whether the user has 
                # overridden their
                # bindings.
                #@-at
                #@@c
                
                if command in (f.OnCutFromMenu,f.OnCopyFromMenu,f.OnPasteFromMenu):
                    emacs_name = '%s-text' % commandName
                else:
                    try: # User errors in the table can cause this.
                        emacs_name = k.inverseCommandsDict.get(command.__name__)
                    except Exception:
                        emacs_name = None
                #@nonl
                #@-node:ekr.20051021100806.1:<< compute emacs_name >>
                #@nl
                    # Contains the not-so-horrible kludge.
                if emacs_name:
                    commandName = emacs_name
                    rawKey,bunchList = c.config.getShortcut(emacs_name)
                    bunch = bunchList and bunchList[0]
                    accel = bunch and bunch.val
                elif not dynamicMenu:
                    g.trace('No inverse for %s' % commandName)
            #@nonl
            #@-node:ekr.20031218072017.1725:<< compute commandName & accel from label & command >>
            #@nl
            rawKey,menu_shortcut = self.canonicalizeShortcut(accel)
            menuCallback = self.defineMenuCallback(command,commandName)
            realLabel = self.getRealMenuName(label)
            #@        << set amp_index using rawKey and realLabel >>
            #@+node:ekr.20031218072017.1728:<< set amp_index using rawKey and realLabel >>
            if rawKey:
                amp_index = rawKey.find("&")
            else:
                amp_index = -1
            
            if amp_index == -1:
                amp_index = realLabel.find("&")
            #@nonl
            #@-node:ekr.20031218072017.1728:<< set amp_index using rawKey and realLabel >>
            #@nl
            realLabel = realLabel.replace("&","")
            self.add_command(menu,label=realLabel,
                accelerator= menu_shortcut or '',
                command=menuCallback,underline=amp_index)
    #@nonl
    #@-node:ekr.20031218072017.1723:createMenuEntries
    #@+node:ekr.20051022053758.1:Helpers
    #@+node:ekr.20031218072017.3783:canonicalizeMenuName & cononicalizeTranslatedMenuName
    def canonicalizeMenuName (self,name):
        
        name = name.lower() ; newname = ""
        chars = string.ascii_letters + string.digits
        for ch in name:
            # if ch not in (' ','\t','\n','\r','&'):
            if ch in chars:
                newname = newname+ch
        return newname
        
    def canonicalizeTranslatedMenuName (self,name):
        
        name = name.lower() ; newname = ""
        for ch in name:
            if ch not in (' ','\t','\n','\r','&'):
            # if ch in string.ascii_letters:
                newname = newname+ch
        return newname
    #@-node:ekr.20031218072017.3783:canonicalizeMenuName & cononicalizeTranslatedMenuName
    #@+node:ekr.20031218072017.2098:canonicalizeShortcut
    #@+at 
    #@nonl
    # This code "canonicalizes" both the shortcuts that appear in menus and 
    # the
    # arguments to bind, mostly ignoring case and the order in which special 
    # keys are
    # specified.
    # 
    # For example, Ctrl+Shift+a is the same as Shift+Control+A. Each generates
    # Shift+Ctrl-A in the menu and Control+A as the argument to bind.
    # 
    # Returns (bind_shortcut, menu_shortcut)
    #@-at
    #@@c
    
    def canonicalizeShortcut (self,shortcut):
        
        if shortcut == None or len(shortcut) == 0:
            return None,None
        s = shortcut.strip().lower()
        
        has_cmd   = s.find("cmd") >= 0     or s.find("command") >= 0 # 11/18/03
        has_ctrl  = s.find("control") >= 0 or s.find("ctrl") >= 0
        has_alt   = s.find("alt") >= 0
        has_shift = s.find("shift") >= 0   or s.find("shft") >= 0
        if sys.platform == "darwin":
            if has_ctrl and not has_cmd:
                has_cmd = True ; has_ctrl = False
            if has_alt and not has_ctrl: # 9/14/04
                has_ctrl = True ; has_alt = False
        #@    << set the last field, preserving case >>
        #@+node:ekr.20031218072017.2102:<< set the last field, preserving case >>
        s2 = shortcut
        s2 = string.strip(s2)
        
        # Replace all minus signs by plus signs, except a trailing minus:
        if len(s2) > 0 and s2[-1] == "-":
            s2 = string.replace(s2,"-","+")
            s2 = s2[:-1] + "-"
        else:
            s2 = string.replace(s2,"-","+")
        
        fields = string.split(s2,"+")
        if fields == None or len(fields) == 0:
            if not g.app.menuWarningsGiven:
                print "bad shortcut specifier:", s
            return None,None
        
        last = fields[-1]
        if last == None or len(last) == 0:
            if not g.app.menuWarningsGiven:
                print "bad shortcut specifier:", s
            return None,None
        #@nonl
        #@-node:ekr.20031218072017.2102:<< set the last field, preserving case >>
        #@nl
        #@    << canonicalize the last field >>
        #@+node:ekr.20031218072017.2099:<< canonicalize the last field >>
        bind_last = menu_last = last
        if len(last) == 1:
            ch = last[0]
            if ch in string.ascii_letters:
                menu_last = string.upper(last)
                if has_shift:
                    bind_last = string.upper(last)
                else:
                    bind_last = string.lower(last)
            elif ch in string.digits:
                bind_last = "Key-" + ch # 1-5 refer to mouse buttons, not keys.
            else:
                #@        << define dict of Tk bind names >>
                #@+node:ekr.20031218072017.2100:<< define dict of Tk bind names >>
                # These are defined at http://tcl.activestate.com/man/tcl8.4/TkCmd/keysyms.htm.
                theDict = {
                    "!" : "exclam",
                    '"' : "quotedbl",
                    "#" : "numbersign",
                    "$" : "dollar",
                    "%" : "percent",
                    "&" : "ampersand",
                    "'" : "quoteright",
                    "(" : "parenleft",
                    ")" : "parenright",
                    "*" : "asterisk",
                    "+" : "plus",
                    "," : "comma",
                    "-" : "minus",
                    "." : "period",
                    "/" : "slash",
                    ":" : "colon",
                    ";" : "semicolon",
                    "<" : "less",
                    "=" : "equal",
                    ">" : "greater",
                    "?" : "question",
                    "@" : "at",
                    "[" : "bracketleft",
                    "\\": "backslash",
                    "]" : "bracketright",
                    "^" : "asciicircum",
                    "_" : "underscore",
                    "`" : "quoteleft",
                    "{" : "braceleft",
                    "|" : "bar",
                    "}" : "braceright",
                    "~" : "asciitilde" }
                #@nonl
                #@-node:ekr.20031218072017.2100:<< define dict of Tk bind names >>
                #@nl
                if ch in theDict.keys():
                    bind_last = theDict[ch]
        elif len(last) > 0:
            #@    << define dict of special names >>
            #@+node:ekr.20031218072017.2101:<< define dict of special names >>
            # These keys are simply made-up names.  The menu_bind values are known to Tk.
            # Case is not significant in the keys.
            
            theDict = {
                "bksp"    : ("BackSpace","BkSp"),
                "esc"     : ("Escape","Esc"),
                # Arrow keys...
                "dnarrow" : ("Down", "DnArrow"),
                "ltarrow" : ("Left", "LtArrow"),
                "rtarrow" : ("Right","RtArrow"),
                "uparrow" : ("Up",   "UpArrow"),
                # Page up/down keys...
                "pageup"  : ("Prior","PgUp"),
                "pagedn"  : ("Next", "PgDn")
            }
            
            #@+at  
            #@nonl
            # The following are not translated, so what appears in the menu is 
            # the same as what is passed to Tk.  Case is significant.
            # 
            # Note: the Tk documentation states that not all of these may be 
            # available on all platforms.
            # 
            # F1,F2,F3,F4,F5,F6,F7,F8,F9,F10,
            # BackSpace, Break, Clear, Delete, Escape, Linefeed, Return, Tab,
            # Down, Left, Right, Up,
            # Begin, End, Home, Next, Prior,
            # Num_Lock, Pause, Scroll_Lock, Sys_Req,
            # KP_Add, KP_Decimal, KP_Divide, KP_Enter, KP_Equal,
            # KP_Multiply, KP_Separator,KP_Space, KP_Subtract, KP_Tab,
            # KP_F1,KP_F2,KP_F3,KP_F4,
            # KP_0,KP_1,KP_2,KP_3,KP_4,KP_5,KP_6,KP_7,KP_8,KP_9
            #@-at
            #@nonl
            #@-node:ekr.20031218072017.2101:<< define dict of special names >>
            #@nl
            last2 = string.lower(last)
            if last2 in theDict.keys():
                bind_last,menu_last = theDict[last2]
        #@nonl
        #@-node:ekr.20031218072017.2099:<< canonicalize the last field >>
        #@nl
        #@    << synthesize the shortcuts from the information >>
        #@+node:ekr.20031218072017.2103:<< synthesize the shortcuts from the information >>
        bind_head = menu_head = ""
        
        if has_shift:
            menu_head = "Shift+"
            if len(last) > 1 or (len(last)==1 and last[0] not in string.ascii_letters):
                bind_head = "Shift-"
        if has_alt:
            bind_head = bind_head + "Alt-"
            menu_head = menu_head + "Alt+"
        
        if has_ctrl:
            bind_head = bind_head + "Control-"
            menu_head = menu_head + "Ctrl+"
            
        if has_cmd: # 11/18/03
            bind_head = bind_head + "Command-"
            menu_head = menu_head + "Command+"
            
        bind_shortcut = "<" + bind_head + bind_last + ">"
        menu_shortcut = menu_head + menu_last
        #@nonl
        #@-node:ekr.20031218072017.2103:<< synthesize the shortcuts from the information >>
        #@nl
        # print repr(shortcut),repr(bind_shortcut),repr(menu_shortcut)
        return bind_shortcut,menu_shortcut
    #@nonl
    #@-node:ekr.20031218072017.2098:canonicalizeShortcut
    #@+node:ekr.20051022044950:computeOldStyleShortcutKey
    def computeOldStyleShortcutKey (self,s):
        
        '''Compute the old-style shortcut key for @shortcuts entries.'''
        
        chars = string.ascii_letters + string.digits
        
        result = [ch for ch in s.strip().lower() if ch in chars]
                
        return ''.join(result)
    #@nonl
    #@-node:ekr.20051022044950:computeOldStyleShortcutKey
    #@+node:ekr.20051022043608.1:createOpenWithMenuItemsFromTable
    def createOpenWithMenuItemsFromTable (self,menu,table):
        
        '''Create an entry in the Open with Menu from the table.
        
        Each entry should be a sequence with 2 or 3 elements.'''
    
        if g.app.unitTesting: return
    
        for data in table:
            #@        << get label, accelerator & command or continue >>
            #@+node:ekr.20051022043713.1:<< get label, accelerator & command or continue >>
            ok = (
                type(data) in (type(()), type([])) and
                len(data) in (2,3)
            )
                
            if ok:
                if len(data) == 2:
                    label,openWithData = data ; accelerator = None
                else:
                    label,accelerator,openWithData = data
                    junk,accelerator = self.canonicalizeShortcut(accelerator)
            else:
                g.trace('bad data in Open With table: %s' % repr(data))
                continue # Ignore bad data
            #@nonl
            #@-node:ekr.20051022043713.1:<< get label, accelerator & command or continue >>
            #@nl
            realLabel = self.getRealMenuName(label)
            underline=realLabel.find("&")
            realLabel = realLabel.replace("&","")
            callback = self.defineOpenWithMenuCallback(openWithData)
        
            self.add_command(menu,label=realLabel,
                accelerator=accelerator or '',
                command=callback,underline=underline)
    #@-node:ekr.20051022043608.1:createOpenWithMenuItemsFromTable
    #@+node:ekr.20031218072017.4117:defineMenuCallback
    def defineMenuCallback(self,command,name):
        
        # The first parameter must be event, and it must default to None.
        def menuCallback(event=None,self=self,command=command,label=name):
            __pychecker__ = '--no-argsused' # event not used, and must be present.
            
            c = self.c
            return c.doCommand(command,label)
    
        return menuCallback
    #@nonl
    #@-node:ekr.20031218072017.4117:defineMenuCallback
    #@+node:ekr.20031218072017.4118:defineOpenWithMenuCallback
    def defineOpenWithMenuCallback(self,data):
        
        # The first parameter must be event, and it must default to None.
        def openWithMenuCallback(event=None,self=self,data=data):
            __pychecker__ = '--no-argsused' # event param must be present.
            return self.c.openWith(data=data)
    
        return openWithMenuCallback
    #@nonl
    #@-node:ekr.20031218072017.4118:defineOpenWithMenuCallback
    #@+node:ekr.20031218072017.3782:get/setRealMenuName & setRealMenuNamesFromTable
    # Returns the translation of a menu name or an item name.
    
    def getRealMenuName (self,menuName):
    
        cmn = self.canonicalizeTranslatedMenuName(menuName)
        return g.app.realMenuNameDict.get(cmn,menuName)
        
    def setRealMenuName (self,untrans,trans):
    
        cmn = self.canonicalizeTranslatedMenuName(untrans)
        g.app.realMenuNameDict[cmn] = trans
    
    def setRealMenuNamesFromTable (self,table):
    
        try:
            for untrans,trans in table:
                self.setRealMenuName(untrans,trans)
        except:
            g.es("exception in setRealMenuNamesFromTable")
            g.es_exception()
    #@nonl
    #@-node:ekr.20031218072017.3782:get/setRealMenuName & setRealMenuNamesFromTable
    #@+node:ekr.20031218072017.3807:getMenu, setMenu, destroyMenu
    def getMenu (self,menuName):
    
        cmn = self.canonicalizeMenuName(menuName)
        return self.menus.get(cmn)
        
    def setMenu (self,menuName,menu):
        
        cmn = self.canonicalizeMenuName(menuName)
        self.menus [cmn] = menu
        
    def destroyMenu (self,menuName):
        
        cmn = self.canonicalizeMenuName(menuName)
        del self.menus[cmn]
    #@nonl
    #@-node:ekr.20031218072017.3807:getMenu, setMenu, destroyMenu
    #@-node:ekr.20051022053758.1:Helpers
    #@-node:ekr.20031218072017.3781:Gui-independent menu routines
    #@+node:ekr.20031218072017.3808:Must be overridden in menu subclasses
    #@+node:ekr.20031218072017.3809:9 Routines with Tk spellings
    def add_cascade (self,parent,label,menu,underline):
        self.oops()
        
    def add_command (self,menu,**keys):
        self.oops()
        
    def add_separator(self,menu):
        self.oops()
        
    def bind (self,bind_shortcut,callback):
        self.oops()
    
    def delete (self,menu,realItemName):
        self.oops()
        
    def delete_range (self,menu,n1,n2):
        self.oops()
    
    def destroy (self,menu):
        self.oops()
    
    def insert_cascade (self,parent,index,label,menu,underline):
        self.oops()
    
    def new_menu(self,parent,tearoff=0):
        self.oops()
    #@nonl
    #@-node:ekr.20031218072017.3809:9 Routines with Tk spellings
    #@+node:ekr.20031218072017.3810:8 Routines with new spellings
    def clearAccel (self,menu,name):
        self.oops()
    
    def createMenuBar (self,frame):
        self.oops()
        
    if 0: # Now defined in the base class
        def createOpenWithMenuFromTable (self,table):
            self.oops()
    
        def defineMenuCallback(self,command,name):
            self.oops()
            
        def defineOpenWithMenuCallback(self,command):
            self.oops()
        
    def disableMenu (self,menu,name):
        self.oops()
        
    def enableMenu (self,menu,name,val):
        self.oops()
        
    def setMenuLabel (self,menu,name,label,underline=-1):
        self.oops()
    #@nonl
    #@-node:ekr.20031218072017.3810:8 Routines with new spellings
    #@-node:ekr.20031218072017.3808:Must be overridden in menu subclasses
    #@-others
#@nonl
#@-node:ekr.20031218072017.3750:class leoMenu
#@+node:ekr.20031218072017.3811:class nullMenu
class nullMenu(leoMenu):
    
    """A null menu class for testing and batch execution."""
    
    __pychecker__ = '--no-argsused' # This calss has many unused args.
    
    #@    @+others
    #@+node:ekr.20050104094308:ctor
    def __init__ (self,frame):
        
        # Init the base class.
        leoMenu.__init__(self,frame)
    #@nonl
    #@-node:ekr.20050104094308:ctor
    #@+node:ekr.20050104094029:oops
    def oops (self):
    
        # g.trace("leoMenu", g.callerName(2))
        pass
    #@nonl
    #@-node:ekr.20050104094029:oops
    #@-others
#@nonl
#@-node:ekr.20031218072017.3811:class nullMenu
#@-others
#@nonl
#@-node:ekr.20031218072017.3749:@thin leoMenu.py
#@-leo
