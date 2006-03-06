#@+leo-ver=4-thin
#@+node:ekr.20060123151617:@thin leoFind.py
#@@language python
#@@tabwidth -4
#@@pagewidth 80

import leoGlobals as g

#@<< Theory of operation of find/change >>
#@+node:ekr.20031218072017.2414:<< Theory of operation of find/change >>
#@+at 
#@nonl
# The find and change commands are tricky; there are many details that must be 
# handled properly. This documentation describes the leo.py code. Previous 
# versions of Leo used an inferior scheme.  The following principles govern 
# the leoFind class:
# 
# 1. Find and Change commands initialize themselves using only the state of 
# the present Leo window. In particular, the Find class must not save internal 
# state information from one invocation to the next. This means that when the 
# user changes the nodes, or selects new text in headline or body text, those 
# changes will affect the next invocation of any Find or Change command. 
# Failure to follow this principle caused all kinds of problems in the Borland 
# and Macintosh codes. There is one exception to this rule: we must remember 
# where interactive wrapped searches start. This principle simplifies the code 
# because most ivars do not persist. However, each command must ensure that 
# the Leo window is left in a state suitable for restarting the incremental 
# (interactive) Find and Change commands. Details of initialization are 
# discussed below.
# 
# 2. The Find and Change commands must not change the state of the outline or 
# body pane during execution. That would cause severe flashing and slow down 
# the commands a great deal. In particular, c.selectVnode and c.editPosition 
# methods must not be called while looking for matches.
# 
# 3. When incremental Find or Change commands succeed they must leave the Leo 
# window in the proper state to execute another incremental command. We 
# restore the Leo window as it was on entry whenever an incremental search 
# fails and after any Find All and Change All command.
# 
# Initialization involves setting the self.c, self.p, self.in_headline, 
# self.wrapping and self.s_ctrl ivars. Setting self.in_headline is tricky; we 
# must be sure to retain the state of the outline pane until initialization is 
# complete. Initializing the Find All and Change All commands is much easier 
# because such initialization does not depend on the state of the Leo window.
# 
# Using Tk.Text widgets for both headlines and body text results in a huge 
# simplification of the code. Indeed, the searching code does not know whether 
# it is searching headline or body text. The search code knows only that 
# self.s_ctrl is a Tk.Text widget that contains the text to be searched or 
# changed and the insert and sel Tk attributes of self.search_text indicate 
# the range of text to be searched. Searching headline and body text 
# simultaneously is complicated. The selectNextPosition() method handles the 
# many details involved by setting self.s_ctrl and its insert and sel 
# attributes.
#@-at
#@-node:ekr.20031218072017.2414:<< Theory of operation of find/change >>
#@nl

class leoFind:

    """The base class for Leo's Find commands."""

    #@    @+others
    #@+node:ekr.20031218072017.3053:leoFind.__init__
    def __init__ (self,c,title=None):
    
        self.c = c
        
        # Spell checkers use this class, so we can't always compute a title.
        if title:
            self.title = title
        else:
            #@        << compute self.title >>
            #@+node:ekr.20041121145452:<< compute self.title >>
            if not c.mFileName:
                s = "untitled"
            else:
                path,s = g.os_path_split(c.mFileName)
                
            self.title = "Find/Change for %s" %  s
            #@nonl
            #@-node:ekr.20041121145452:<< compute self.title >>
            #@nl
    
        #@    << init the gui-independent ivars >>
        #@+node:ekr.20031218072017.3054:<< init the gui-independent ivars >>
        self.wrapPosition = None
        self.onlyPosition = None
        self.find_text = ""
        self.change_text = ""
        self.unstick = False
        
        #@+at
        # New in 4.3:
        # - These are the names of leoFind ivars. (no more _flag hack).
        # - There are no corresponding commander ivars to keep in synch 
        # (hurray!)
        # - These ivars are inited (in the subclass by init) when this class 
        # is created.
        # - These ivars are updated (in the subclass by update_ivars) just 
        # before doing any find.
        #@-at
        #@@c
        
        #@<< do dummy initialization to keep Pychecker happy >>
        #@+node:ekr.20050123164539:<< do dummy initialization to keep Pychecker happy >>
        if 1:
            self.batch = None
            self.clone_find_all = None
            self.ignore_case = None
            self.node_only = None
            self.pattern_match = None
            self.search_headline = None
            self.search_body = None
            self.suboutline_only = None
            self.mark_changes = None
            self.mark_finds = None
            self.reverse = None
            self.script_search = None
            self.script_change = None
            self.selection_only = None
            self.wrap = None
            self.whole_word = None
        #@nonl
        #@-node:ekr.20050123164539:<< do dummy initialization to keep Pychecker happy >>
        #@nl
        
        self.intKeys = [
            "batch","ignore_case", "node_only",
            "pattern_match", "search_headline", "search_body",
            "suboutline_only", "mark_changes", "mark_finds", "reverse",
            "script_search","script_change","selection_only",
            "wrap", "whole_word",
        ]
        
        self.newStringKeys = ["radio-find-type", "radio-search-scope"]
        
        # Ivars containing internal state...
        self.c = None # The commander for this search.
        self.clone_find_all = False
        self.p = None # The position being searched.  Never saved between searches!
        self.in_headline = False # True: searching headline text.
        self.s_ctrl = None # The search text for this search.
        self.wrapping = False # True: wrapping is enabled.
            # This is _not_ the same as self.wrap for batch searches.
        
        #@+at 
        #@nonl
        # Initializing a wrapped search is tricky.  The search() method will 
        # fail if p==wrapPosition and pos >= wrapPos.  selectNextPosition() 
        # will fail if p == wrapPosition.  We set wrapPos on entry, before the 
        # first search.  We set wrapPosition in selectNextPosition after the 
        # first search fails.  We also set wrapPosition on exit if the first 
        # search suceeds.
        #@-at
        #@@c
        
        self.wrapPosition = None # The start of wrapped searches: persists between calls.
        self.onlyPosition = None # The starting node for suboutline-only searches.
        self.wrapPos = None # The starting position of the wrapped search: persists between calls.
        self.errors = 0
        self.selStart = self.selEnd = None # For selection-only searches.
        #@nonl
        #@-node:ekr.20031218072017.3054:<< init the gui-independent ivars >>
        #@nl
    #@nonl
    #@-node:ekr.20031218072017.3053:leoFind.__init__
    #@+node:ekr.20060123065756.1:Top Level Buttons
    #@+node:ekr.20031218072017.3057:changeAllButton
    # The user has pushed the "Change All" button from the find panel.
    
    def changeAllButton(self):
    
        c = self.c
        self.setup_button()
        c.clearAllVisited() # Clear visited for context reporting.
    
        if self.script_change:
            self.doChangeAllScript()
        elif self.selection_only:
            self.change()
        else:
            self.changeAll()
    #@nonl
    #@-node:ekr.20031218072017.3057:changeAllButton
    #@+node:ekr.20031218072017.3056:changeButton
    # The user has pushed the "Change" button from the find panel.
    
    def changeButton(self):
    
        self.setup_button()
    
        if self.script_change:
            self.doChangeScript()
        else:
            self.change()
    #@nonl
    #@-node:ekr.20031218072017.3056:changeButton
    #@+node:ekr.20031218072017.3058:changeThenFindButton
    # The user has pushed the "Change Then Find" button from the find panel.
    
    def changeThenFindButton(self):
    
        self.setup_button()
    
        if self.script_change:
            self.doChangeScript()
            if self.script_search:
                self.doFindScript()
            else:
                self.findNext()
        else:
            if self.script_search:
                self.change()
                self.doFindScript()
            else:
                self.changeThenFind()
    #@nonl
    #@-node:ekr.20031218072017.3058:changeThenFindButton
    #@+node:ekr.20031218072017.3060:findAllButton
    # The user has pushed the "Find All" button from the find panel.
    
    def findAllButton(self):
    
        c = self.c
        self.setup_button()
        c.clearAllVisited() # Clear visited for context reporting.
    
        if self.script_search:
            self.doFindAllScript()
        elif self.selection_only:
            self.findNext()
        else:
            self.findAll()
    #@nonl
    #@-node:ekr.20031218072017.3060:findAllButton
    #@+node:ekr.20031218072017.3059:findButton
    # The user has pushed the "Find" button from the find panel.
    
    def findButton(self):
    
        self.setup_button()
    
        if self.script_search:
            self.doFindScript()
        else:
            self.findNext()
    #@nonl
    #@-node:ekr.20031218072017.3059:findButton
    #@+node:ekr.20031218072017.3065:setup_button
    # Initializes a search when a button is pressed in the Find panel.
    
    def setup_button(self):
        
        c = self.c
        self.p = c.currentPosition()
    
        c.bringToFront()
        if 0: # We _must_ retain the editing status for incremental searches!
            c.endEditing()
    
        self.update_ivars()
        self.adjust_ivars()
    #@nonl
    #@-node:ekr.20031218072017.3065:setup_button
    #@-node:ekr.20060123065756.1:Top Level Buttons
    #@+node:ekr.20031218072017.3055:Top Level Commands
    #@+node:ekr.20031218072017.3061:changeCommand
    # The user has selected the "Replace" menu item.
    
    def changeCommand(self,c):
    
        self.setup_command()
    
        if self.script_search:
            self.doChangeScript()
        else:
            self.change()
    #@nonl
    #@-node:ekr.20031218072017.3061:changeCommand
    #@+node:ekr.20031218072017.3062:changeThenFindCommand
    # The user has pushed the "Change Then Find" button from the Find menu.
    
    def changeThenFindCommand(self,c):
    
        self.setup_command()
    
        if self.script_search:
            self.doChangeScript()
            self.doFindScript()
        else:
            self.changeThenFind()
    #@nonl
    #@-node:ekr.20031218072017.3062:changeThenFindCommand
    #@+node:ekr.20051013084200.1:dismiss: defined in subclass class
    def dismiss (self):
        pass
    #@nonl
    #@-node:ekr.20051013084200.1:dismiss: defined in subclass class
    #@+node:ekr.20031218072017.3063:findNextCommand
    # The user has selected the "Find Next" menu item.
    
    def findNextCommand(self,c):
    
        self.setup_command()
    
        if self.script_search:
            self.doFindScript()
        else:
            self.findNext()
    #@nonl
    #@-node:ekr.20031218072017.3063:findNextCommand
    #@+node:ekr.20031218072017.3064:findPreviousCommand
    # The user has selected the "Find Previous" menu item.
    
    def findPreviousCommand(self,c):
    
        self.setup_command()
    
        self.reverse = not self.reverse
    
        if self.script_search:
            self.doFindScript()
        else:
            self.findNext()
    
        self.reverse = not self.reverse
    #@nonl
    #@-node:ekr.20031218072017.3064:findPreviousCommand
    #@+node:EKR.20040503070514:handleUserClick
    def handleUserClick (self,p):
        
        """Reset suboutline-only search when the user clicks a headline."""
        
        try:
            if self.c and self.suboutline_only:
                # g.trace(p)
                self.onlyPosition = p.copy()
        except: pass
    #@nonl
    #@-node:EKR.20040503070514:handleUserClick
    #@+node:ekr.20031218072017.3066:setup_command
    # Initializes a search when a command is invoked from the menu.
    
    def setup_command(self):
        
        # g.trace('leoFind')
    
        if 0: # We _must_ retain the editing status for incremental searches!
            self.c.endEditing()
    
        self.update_ivars()
        self.adjust_ivars()
    #@nonl
    #@-node:ekr.20031218072017.3066:setup_command
    #@-node:ekr.20031218072017.3055:Top Level Commands
    #@+node:ekr.20031218072017.3067:Find/change utils
    #@+node:ekr.20050204084635:find.adjust_ivars
    def adjust_ivars (self):
        
        '''New in 4.3.
        
        Adjust ivars, particularly the find and change text.
        This is called just before executing a command and
        just after calling update_ivars.
        
        Plugins may replace this code as desired.'''
        
        if 0:
            # The TkFind class now removes tailing newlines.
        
            ft = self.find_text
            if not ft: return
        
            # Remove a trailing newline unless that is all there is.
            if len(ft) > 1 and ft[-1] in ('\n','\r'):
                ft = ft[:-1]
                self.adjust_find_text(ft)
                if 0:
                    g.es('before:',repr(self.find_text))
                    g.es(' after:',repr(ft))
                self.find_text = ft
        
            return
    #@nonl
    #@-node:ekr.20050204084635:find.adjust_ivars
    #@+node:ekr.20031218072017.2293:batchChange (sets start of change-all group)
    #@+at 
    #@nonl
    # This routine performs a single batch change operation, updating the head 
    # or body string of p and leaving the result in s_ctrl.  We update the 
    # body if we are changing the body text of c.currentVnode().
    # 
    # s_ctrl contains the found text on entry and contains the changed text on 
    # exit.  pos and pos2 indicate the selection.  The selection will never be 
    # empty. NB: we can not assume that self.p is visible.
    #@-at
    #@@c
    
    def batchChange (self,pos1,pos2):
    
        c = self.c ; u = c.undoer
        p = self.p ; st = self.s_ctrl ; gui = g.app.gui
        # Replace the selection with self.change_text
        if gui.compareIndices(st,pos1, ">", pos2):
            pos1,pos2=pos2,pos1
        gui.replaceSelectionRangeWithText(st,pos1,pos2,self.change_text)
        s = gui.getAllText(st)
        # Update the selection.
        insert=g.choose(self.reverse,pos1,pos1+'+'+str(len(self.change_text))+'c')
        gui.setSelectionRange(st,insert,insert)
        gui.setInsertPoint(st,insert)
        # Update the node
        if self.in_headline:
            #@        << change headline >>
            #@+node:ekr.20031218072017.2294:<< change headline >>
            if len(s) > 0 and s[-1]=='\n': s = s[:-1]
            
            if s != p.headString():
                
                undoData = u.beforeChangeNodeContents(p)
            
                p.initHeadString(s)
                if self.mark_changes:
                    p.setMarked()
                p.setDirty()
                if not c.isChanged():
                    c.setChanged(True)
                
                u.afterChangeNodeContents(p,'Change Headline',undoData)
            #@nonl
            #@-node:ekr.20031218072017.2294:<< change headline >>
            #@nl
        else:
            #@        << change body >>
            #@+node:ekr.20031218072017.2295:<< change body >>
            if len(s) > 0 and s[-1]=='\n': s = s[:-1]
            
            if s != p.bodyString():
                
                undoData = u.beforeChangeNodeContents(p)
            
                p.setBodyStringOrPane(s)
                if self.mark_changes:
                    p.setMarked()
                p.setDirty()
                if not c.isChanged():
                    c.setChanged(True)
                 
                u.afterChangeNodeContents(p,'Change Body',undoData)
            #@nonl
            #@-node:ekr.20031218072017.2295:<< change body >>
            #@nl
    #@nonl
    #@-node:ekr.20031218072017.2293:batchChange (sets start of change-all group)
    #@+node:ekr.20031218072017.3068:change
    def change(self):
    
        if self.checkArgs():
            self.initInHeadline()
            self.changeSelection()
    #@nonl
    #@-node:ekr.20031218072017.3068:change
    #@+node:ekr.20031218072017.3069:changeAll (sets end of change-all group)
    def changeAll(self):
    
        c = self.c ; u = c.undoer ; undoType = 'Change All'
        current = c.currentPosition()
        st = self.s_ctrl ; gui = g.app.gui
        if not self.checkArgs(): return
        self.initInHeadline()
        saveData = self.save()
        self.initBatchCommands()
        count = 0
        c.beginUpdate()
        try: # In update...
            u.beforeChangeGroup(current,undoType)
            while 1:
                pos1, pos2 = self.findNextMatch()
                if not pos1: break
                count += 1
                self.batchChange(pos1,pos2)
                line = gui.getLineContainingIndex(st,pos1)
                self.printLine(line,allFlag=True)
            p = c.currentPosition()
            u.afterChangeGroup(p,undoType,reportFlag=True)
            g.es("changed: %d instances" % (count))
        finally:
            c.endUpdate()
            self.restore(saveData)
    #@nonl
    #@-node:ekr.20031218072017.3069:changeAll (sets end of change-all group)
    #@+node:ekr.20031218072017.3070:changeSelection
    # Replace selection with self.change_text.
    # If no selection, insert self.change_text at the cursor.
    
    def changeSelection(self):
    
        c = self.c ; p = self.p ; gui = g.app.gui
        # g.trace(self.in_headline)
        t = g.choose(self.in_headline,p.edit_widget(),c.frame.bodyCtrl)
        oldSel = sel = gui.getTextSelection(t)
        if sel and len(sel) == 2:
            start,end = sel
            if start == end:
                sel = None
        if not sel or len(sel) != 2:
            g.es("No text selected")
            return False
    
        # Replace the selection in _both_ controls.
        start,end = oldSel
        gui.replaceSelectionRangeWithText(t,          start,end,self.change_text)
        gui.replaceSelectionRangeWithText(self.s_ctrl,start,end,self.change_text)
    
        # Update the selection for the next match.
        gui.setSelectionRangeWithLength(t,start,len(self.change_text))
        c.widgetWantsFocus(t)
    
        # No redraws here: they would destroy the headline selection.
        c.beginUpdate()
        try:
            if self.mark_changes:
                p.setMarked()
            if self.in_headline:
                c.frame.tree.onHeadChanged(p,'Change')
            else:
                c.frame.body.onBodyChanged('Change',oldSel=oldSel)
        finally:
            c.endUpdate(False)
            c.frame.tree.drawIcon(p) # redraw only the icon.
         
        return True
    #@-node:ekr.20031218072017.3070:changeSelection
    #@+node:ekr.20031218072017.3071:changeThenFind
    def changeThenFind(self):
    
        if not self.checkArgs():
            return
    
        self.initInHeadline()
        if self.changeSelection():
            self.findNext(False) # don't reinitialize
    #@nonl
    #@-node:ekr.20031218072017.3071:changeThenFind
    #@+node:ekr.20031218072017.2417:doChange...Script
    def doChangeScript (self):
    
        g.app.searchDict["type"] = "change"
        self.runChangeScript()
    
    def doChangeAllScript (self):
    
        """The user has just pressed the Change All button with script-change box checked.
    
        N.B. Only this code is executed."""
    
        g.app.searchDict["type"] = "changeAll"
        while 1:
            self.runChangeScript()
            if not g.app.searchDict.get("continue"):
                break
    
    def runChangeScript (self):
    
        try:
            assert(self.script_change)
            exec self.change_text in {} # Use {} to get a pristine environment.
        except:
            g.es("exception executing change script")
            g.es_exception(full=False)
            g.app.searchDict["continue"] = False # 2/1/04
    #@nonl
    #@-node:ekr.20031218072017.2417:doChange...Script
    #@+node:ekr.20031218072017.3072:doFind...Script
    def doFindScript (self):
    
        g.app.searchDict["type"] = "find"
        self.runFindScript()
    
    def doFindAllScript (self):
    
        """The user has just pressed the Find All button with script-find radio button checked.
    
        N.B. Only this code is executed."""
    
        g.app.searchDict["type"] = "findAll"
        while 1:
            self.runFindScript()
            if not g.app.searchDict.get("continue"):
                break
    
    def runFindScript (self):
    
        try:
            exec self.find_text in {} # Use {} to get a pristine environment.
        except:
            g.es("exception executing find script")
            g.es_exception(full=False)
            g.app.searchDict["continue"] = False # 2/1/04
    #@-node:ekr.20031218072017.3072:doFind...Script
    #@+node:ekr.20031218072017.3073:findAll
    def findAll(self):
    
        c = self.c ; t = self.s_ctrl ; u = c.undoer
        gui = g.app.gui ; undoType = 'Clone Find All'
        if not self.checkArgs():
            return
        self.initInHeadline()
        data = self.save()
        self.initBatchCommands()
        count = 0 ; clones = []
        while 1:
            pos, newpos = self.findNextMatch()
            if not pos: break
            count += 1
            line = gui.getLineContainingIndex(t,pos)
            self.printLine(line,allFlag=True)
            if self.clone_find_all and self.p.v.t not in clones:
                if not clones:
                    #@                << create the found node and begin the undo group >>
                    #@+node:ekr.20051113110735:<< create the found node and begin the undo group >>
                    u.beforeChangeGroup(c.currentPosition(),undoType)
                    undoData = u.beforeInsertNode(c.currentPosition())
                    oldRoot = c.rootPosition()
                    found = oldRoot.insertAfter()
                    found.moveToRoot(oldRoot)
                    found.setHeadString('Found: ' + self.find_text)
                    u.afterInsertNode(found,undoType,undoData,dirtyVnodeList=[])
                    #@nonl
                    #@-node:ekr.20051113110735:<< create the found node and begin the undo group >>
                    #@nl
                #@            << create a clone of p under the find node >>
                #@+node:ekr.20051113110851:<< create a clone of p under the find node >>
                clones.append(self.p.v.t)
                undoData = u.beforeCloneNode(self.p)
                q = self.p.clone(self.p)
                q.moveToLastChildOf(found)
                u.afterCloneNode(q,undoType,undoData,dirtyVnodeList=[])
                #@nonl
                #@-node:ekr.20051113110851:<< create a clone of p under the find node >>
                #@nl
        if self.clone_find_all and clones:
            c.setChanged(True)
            u.afterChangeGroup(c.currentPosition(),undoType,reportFlag=True)   
        c.redraw_now()
        g.es("found: %d matches" % (count))
        self.restore(data)
    #@nonl
    #@-node:ekr.20031218072017.3073:findAll
    #@+node:ekr.20031218072017.3074:findNext
    def findNext(self,initFlag=True):
    
        c = self.c
        if not self.checkArgs():
            return
    
        if initFlag:
            self.initInHeadline()
            data = self.save()
            self.initInteractiveCommands()
        else:
            data = self.save()
    
        pos, newpos = self.findNextMatch()
    
        if pos:
            self.showSuccess(pos,newpos)
        else:
            if self.wrapping:
                g.es("end of wrapped search")
            else:
                g.es("not found: " + "'" + self.find_text + "'")
            self.restore(data)
    #@nonl
    #@-node:ekr.20031218072017.3074:findNext
    #@+node:ekr.20031218072017.3075:findNextMatch
    # Resumes the search where it left off.
    # The caller must call set_first_incremental_search or set_first_batch_search.
    
    def findNextMatch(self):
    
        c = self.c
    
        if not self.search_headline and not self.search_body:
            return None, None
    
        if len(self.find_text) == 0:
            return None, None
    
        p = self.p
        while p:
            pos, newpos = self.search()
            if pos:
                if self.mark_finds:
                    p.setMarked()
                    c.frame.tree.drawIcon(p) # redraw only the icon.
                return pos, newpos
            elif self.errors:
                return None,None # Abort the search.
            elif self.node_only:
                return None,None # We are only searching one node.
            else:
                p = self.p = self.selectNextPosition()
        return None, None
    #@nonl
    #@-node:ekr.20031218072017.3075:findNextMatch
    #@+node:ekr.20031218072017.3076:resetWrap
    def resetWrap (self,event=None):
    
        self.wrapPosition = None
        self.onlyPosition = None
    #@nonl
    #@-node:ekr.20031218072017.3076:resetWrap
    #@+node:ekr.20031218072017.3077:search
    def search (self):
    
        """Searches the present headline or body text for self.find_text and returns True if found.
    
        self.whole_word, self.ignore_case, and self.pattern_match control the search."""
    
        c = self.c ; p = self.p ; t = self.s_ctrl ; gui = g.app.gui
        assert(c and t and p)
        if self.selection_only:
            index,stopindex = self.selStart, self.selEnd
            if index == stopindex:
                return None, None
        else:
            index = gui.getInsertPoint(t)
            stopindex = g.choose(self.reverse,gui.firstIndex(),gui.lastIndex())
        while 1:
            try:
                pos = self.gui_search(t,self.find_text,index,
                    stopindex=stopindex,backwards=self.reverse,
                    regexp=self.pattern_match,nocase=self.ignore_case)
            except Exception:
                g.es_exception(full=False)
                self.errors += 1 ; break
            if not pos: break
            if self.find_text == '\n':
                newpos = gui.moveIndexToNextLine(t,pos)
            else:
                newpos = gui.moveIndexForward(t,pos,len(self.find_text))
            if newpos is None: break
            #@        << break if we are passed the wrap point >>
            #@+node:ekr.20031218072017.3079:<< break if we are passed the wrap point >>
            if self.wrapping and self.wrapPos and self.wrapPosition and self.p == self.wrapPosition:
            
                if self.reverse and gui.compareIndices(t,pos, "<", self.wrapPos):
                    # g.trace("wrap done")
                    break
            
                if not self.reverse and gui.compareIndices(t,newpos, ">", self.wrapPos):
                    break
            #@nonl
            #@-node:ekr.20031218072017.3079:<< break if we are passed the wrap point >>
            #@nl
            if self.whole_word:
                index = t.index(g.choose(self.reverse,pos,newpos))
                #@            << continue if not whole word match >>
                #@+node:ekr.20031218072017.3080:<< continue if not whole word match >>
                # Set pos to None if word characters preceed or follow the selection.
                before = gui.getCharBeforeIndex(t,pos)
                first  = gui.getCharAtIndex    (t,pos)
                last   = gui.getCharBeforeIndex(t,newpos)
                after  = gui.getCharAtIndex    (t,newpos)
                
                #g.trace("before,first",before,first,g.is_c_id(before),g.is_c_id(first))
                #g.trace("after,last",  after,last,  g.is_c_id(after), g.is_c_id(last))
                
                if g.is_c_id(before) and g.is_c_id(first):
                    continue
                
                if g.is_c_id(after) and g.is_c_id(last):
                    continue
                #@nonl
                #@-node:ekr.20031218072017.3080:<< continue if not whole word match >>
                #@nl
            #g.trace("found:",pos,newpos,p)
            gui.setTextSelection(t,pos,newpos)
            return pos, newpos
        # g.trace('not found',p.headString())
        return None,None
    #@nonl
    #@-node:ekr.20031218072017.3077:search
    #@+node:ekr.20031218072017.3081:selectNextPosition
    # Selects the next node to be searched.
    
    def selectNextPosition(self):
    
        c = self.c ; p = self.p
    
        if self.selection_only:
            return None
    
        # Start suboutline only searches.
        if self.suboutline_only and not self.onlyPosition:
            # p.copy not needed because the find code never calls p.moveToX.
            # Furthermore, p might be None, so p.copy() would be wrong!
            self.onlyPosition = p 
    
        # Start wrapped searches.
        if self.wrapping and not self.wrapPosition:
            assert(self.wrapPos != None)
            # p.copy not needed because the find code never calls p.moveToX.
            # Furthermore, p might be None, so p.copy() would be wrong!
            self.wrapPosition = p 
    
        if self.in_headline and self.search_body:
            # just switch to body pane.
            self.in_headline = False
            self.initNextText()
            # g.trace('switching to body',g.callers(5))
            return p
    
        if self.reverse: p = p.threadBack()
        else:            p = p.threadNext()
        
        # New in 4.3: restrict searches to hoisted area.
        # End searches outside hoisted area.
        if c.hoistStack:
            if not p:
                if self.wrapping:
                    g.es('Wrap disabled in hoisted outlines',color='blue')
                return
            bunch = c.hoistStack[-1]
            if not bunch.p.isAncestorOf(p):
                g.es('Found match outside of hoisted outline',color='blue')
                return None
    
        # Wrap if needed.
        if not p and self.wrapping and not self.suboutline_only:
            p = c.rootPosition()
            if self.reverse:
                # Set search_v to the last node of the tree.
                while p and p.next():
                    p = p.next()
                if p: p = p.lastNode()
    
        # End wrapped searches.
        if self.wrapping and p and p == self.wrapPosition:
            # g.trace("ending wrapped search")
            p = None ; self.resetWrap()
    
        # End suboutline only searches.
        if (self.suboutline_only and self.onlyPosition and p and
            (p == self.onlyPosition or not self.onlyPosition.isAncestorOf(p))):
            # g.trace("end outline-only")
            p = None ; self.onlyPosition = None
    
        # p.copy not needed because the find code never calls p.moveToX.
        # Furthermore, p might be None, so p.copy() would be wrong!
        self.p = p # used in initNextText().
        if p: # select p and set the search point within p.
            self.in_headline = self.search_headline
            self.initNextText()
        return p
    #@nonl
    #@-node:ekr.20031218072017.3081:selectNextPosition
    #@-node:ekr.20031218072017.3067:Find/change utils
    #@+node:ekr.20031218072017.3082:Initing & finalizing
    #@+node:ekr.20031218072017.3083:checkArgs
    def checkArgs (self):
    
        val = True
        if not self.search_headline and not self.search_body:
            g.es("not searching headline or body")
            val = False
        if len(self.find_text) == 0:
            g.es("empty find patttern")
            val = False
        return val
    #@nonl
    #@-node:ekr.20031218072017.3083:checkArgs
    #@+node:ekr.20031218072017.3084:initBatchCommands
    # Initializes for the Find All and Change All commands.
    
    def initBatchCommands (self):
    
        c = self.c
        self.in_headline = self.search_headline # Search headlines first.
        self.errors = 0
    
        # Select the first node.
        if self.suboutline_only or self.node_only or self.selection_only:
            self.p = c.currentPosition()
            if self.selection_only: self.selStart,self.selEnd = c.frame.body.getTextSelection()
            else:                   self.selStart,self.selEnd = None,None
        else:
            p = c.rootPosition()
            if self.reverse:
                while p and p.next():
                    p = p.next()
                p = p.lastNode()
            self.p = p
    
        # Set the insert point.
        self.initBatchText()
    #@nonl
    #@-node:ekr.20031218072017.3084:initBatchCommands
    #@+node:ekr.20031218072017.3085:initBatchText & initNextText
    # Returns s_ctrl with "insert" point set properly for batch searches.
    def initBatchText(self):
        p = self.p
        self.wrapping = False # Only interactive commands allow wrapping.
        s = g.choose(self.in_headline,p.headString(), p.bodyString())
        return self.init_s_ctrl(s)
    
    # Call this routine when moving to the next node when a search fails.
    # Same as above except we don't reset wrapping flag.
    def initNextText(self):
        p = self.p
        s = g.choose(self.in_headline,p.headString(), p.bodyString())
        return self.init_s_ctrl(s)
    #@nonl
    #@-node:ekr.20031218072017.3085:initBatchText & initNextText
    #@+node:ekr.20031218072017.3086:initInHeadline
    # Guesses which pane to start in for incremental searches and changes.
    # This must not alter the current "insert" or "sel" marks.
    
    def initInHeadline (self):
    
        c = self.c ; p = self.p
    
        # Do not change this without careful thought and extensive testing!
        if self.search_headline and self.search_body:
            # A temporary expedient.
            if self.reverse:
                self.in_headline = False
            else:
                # Search headline first.
                self.in_headline = (
                    p == c.frame.tree.editPosition() and
                    c.get_focus() != c.frame.body.bodyCtrl)
        else:
            self.in_headline = self.search_headline
    #@nonl
    #@-node:ekr.20031218072017.3086:initInHeadline
    #@+node:ekr.20031218072017.3087:initInteractiveCommands
    # For incremental searches
    
    def initInteractiveCommands(self):
    
        c = self.c ; p = self.p ; gui = g.app.gui
    
        self.errors = 0
        if self.in_headline:
            c.frame.tree.setEditPosition(p)
            t = p.edit_widget()
            sel = None
        else:
            t = c.frame.bodyCtrl
            sel = gui.getTextSelection(t)
        pos = gui.getInsertPoint(t)
        st = self.initNextText()
        c.widgetWantsFocus(t)
        gui.setInsertPoint(st,pos)
        if sel:
            self.selStart,self.selEnd = sel
        else:
            self.selStart,self.selEnd = None,None
        self.wrapping = self.wrap
        if self.wrap and self.wrapPosition == None:
            self.wrapPos = pos
            # Do not set self.wrapPosition here: that must be done after the first search.
    #@nonl
    #@-node:ekr.20031218072017.3087:initInteractiveCommands
    #@+node:ekr.20031218072017.3088:printLine
    def printLine (self,line,allFlag=False):
    
        both = self.search_body and self.search_headline
        context = self.batch # "batch" now indicates context
    
        if allFlag and both and context:
            g.es('-' * 20,self.p.headString())
            theType = g.choose(self.in_headline,"head: ","body: ")
            g.es(theType + line)
        elif allFlag and context and not self.p.isVisited():
            # We only need to print the context once.
            g.es('-' * 20,self.p.headString())
            g.es(line)
            self.p.setVisited()
        else:
            g.es(line)
    #@nonl
    #@-node:ekr.20031218072017.3088:printLine
    #@+node:ekr.20031218072017.3089:restore
    # Restores the screen after a search fails
    
    def restore (self,data):
    
        c = self.c ; gui = g.app.gui
        in_headline,p,t,insert,start,end = data
        
        c.frame.bringToFront() # Needed on the Mac
    
        # Don't try to reedit headline.
        c.selectPosition(p)
        
        if not in_headline:
            # Looks good and provides clear indication of failure or termination.
            gui.setSelectionRange(t,insert,insert)
            gui.setInsertPoint(t,insert)
            gui.makeIndexVisible(t,insert)
        
        #g.trace(c.widget_name(t))
        
        if 1: # I prefer always putting the focus in the body.
            c.invalidateFocus()
            c.bodyWantsFocusNow()
        else:
            c.widgetWantsFocusNow(t)
    #@nonl
    #@-node:ekr.20031218072017.3089:restore
    #@+node:ekr.20031218072017.3090:save
    def save (self):
    
        c = self.c ; p = self.p ; gui = g.app.gui
        t = g.choose(self.in_headline,p.edit_widget(),c.frame.bodyCtrl)
        insert = gui.getInsertPoint(t)
        sel = gui.getSelectionRange(t)
        if len(sel) == 2:
            start,end = sel
        else:
            start,end = None,None
        return (self.in_headline,p,t,insert,start,end)
    #@nonl
    #@-node:ekr.20031218072017.3090:save
    #@+node:ekr.20031218072017.3091:showSuccess
    def showSuccess(self,pos,newpos):
    
        """Displays the final result.
    
        Returns self.dummy_vnode, p.edit_widget() or c.frame.bodyCtrl with
        "insert" and "sel" points set properly."""
    
        c = self.c ; p = self.p ; gui = g.app.gui
        
        c.frame.bringToFront() # Needed on the Mac
        c.beginUpdate()
        try:
            c.selectPosition(p)
        finally:
            c.endUpdate(scroll=True)
        if self.in_headline:
            c.editPosition(p)
        # Set the focus and selection after the redraw.
        t = g.choose(self.in_headline,p.edit_widget(),c.frame.bodyCtrl)
        insert = g.choose(self.reverse,pos,newpos)
        # New in 4.4a3: a much better way to ensure progress in backward searches.
        # g.trace(id(t),pos,newpos)
        c.widgetWantsFocusNow(t)
        gui.setSelectionRange(t,pos,newpos,insert=insert)
        # c.widgetWantsFocusNow(t)
        gui.makeIndexVisible(t,insert)
        if self.wrap and not self.wrapPosition:
            self.wrapPosition = self.p
    #@nonl
    #@-node:ekr.20031218072017.3091:showSuccess
    #@-node:ekr.20031218072017.3082:Initing & finalizing
    #@+node:ekr.20031218072017.3092:Must be overridden in subclasses
    def init_s_ctrl (self,s):
        __pychecker__ = '--no-argsused'
        self.oops()
    
    def bringToFront (self):
        self.oops()
    
    def gui_search (self,t,*args,**keys):
        __pychecker__ = '--no-argsused'
        self.oops()
       
    # New in 4.3: allows base class to adjust controls. 
    def adjust_find_text(self,s):
        __pychecker__ = '--no-argsused'
        self.oops()
    
    def oops(self):
        print ("leoFind oops:",
            g.callers(),"should be overridden in subclass")
            
    def update_ivars(self):
        self.oops()
    #@nonl
    #@-node:ekr.20031218072017.3092:Must be overridden in subclasses
    #@-others
#@nonl
#@-node:ekr.20060123151617:@thin leoFind.py
#@-leo
