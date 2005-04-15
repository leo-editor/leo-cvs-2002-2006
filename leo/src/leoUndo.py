#@+leo-ver=4-thin
#@+node:ekr.20031218072017.3603:@thin leoUndo.py
'''Undo manager.'''

#@@language python
#@@tabwidth -4
#@@pagewidth 80

#@<< How Leo implements unlimited undo >>
#@+node:ekr.20031218072017.2413:<< How Leo implements unlimited undo >>
#@+at 
#@nonl
# Only leo.py supports unlimited undo.  Unlimited undo is straightforward; it 
# merely requires that all commands that affect the outline or body text must 
# be undoable. In other words, everything that affects the outline or body 
# text must be remembered.
# 
# We may think of all the actions that may be Undone or Redone as a string of 
# beads (undo nodes). Undoing an operation moves backwards to the next bead; 
# redoing an operation moves forwards to the next bead. A bead pointer points 
# to the present bead. The bead pointer points in front of the first bead when 
# Undo is disabled.  The bead pointer points at the last bead when Redo is 
# disabled. An undo node is a Python dictionary containing all information 
# needed to undo or redo the operation.
# 
# The Undo command uses the present bead to undo the action, then moves the 
# bead pointer backwards. The Redo command uses the bead after the present 
# bead to redo the action, then moves the bead pointer forwards. All undoable 
# operations call setUndoParams() to create a new bead. The list of beads does 
# not branch; all undoable operations (except the Undo and Redo commands 
# themselves) delete any beads following the newly created bead.
# 
# I did not invent this model of unlimited undo.  I first came across it in 
# the documentation for Apple's Yellow Box classes.
#@-at
#@-node:ekr.20031218072017.2413:<< How Leo implements unlimited undo >>
#@nl

import leoGlobals as g
import string

#@+others
#@+node:ekr.20031218072017.3605:class undoer
class baseUndoer:
    """The base class of the undoer class."""
    #@    @+others
    #@+node:ekr.20031218072017.3606:undo.__init__ & clearIvars
    def __init__ (self,c):
        
        u = self ; u.c = c
    
        u.debug = False # True: enable debugging code in new undo scheme.
        u.debug_print = False # True: enable print statements in debug code.
    
        u.granularity = c.config.getString('undo_granularity')
        if u.granularity: u.granularity = u.granularity.lower()
        if u.granularity not in ('node','line','word','char'):
            u.granularity = 'line'
        # g.trace('undoer',u.granularity)
    
        # Statistics comparing old and new ways (only if u.debug is on).
        u.new_mem = 0
        u.old_mem = 0
    
        # State ivars...
        u.undoType = "Can't Undo"
        # These must be set here, _not_ in clearUndoState.
        u.redoMenuLabel = "Can't Redo"
        u.undoMenuLabel = "Can't Undo"
        u.realRedoMenuLabel = "Can't Redo"
        u.realUndoMenuLabel = "Can't Undo"
        u.undoing = False # True if executing an Undo command.
        u.redoing = False # True if executing a Redo command.
        
        # New in 4.2...
        u.optionalIvars = []
        u.redrawFlag = True
    #@nonl
    #@+node:ekr.20031218072017.3607:clearIvars
    def clearIvars (self):
        
        u = self
        
        u.p = None # The position/node being operated upon for undo and redo.
    
        for ivar in u.optionalIvars:
            setattr(u,ivar,None)
    #@nonl
    #@-node:ekr.20031218072017.3607:clearIvars
    #@-node:ekr.20031218072017.3606:undo.__init__ & clearIvars
    #@+node:ekr.20031218072017.3608:State routines...
    #@+node:ekr.20031218072017.3609:clearUndoState
    def clearUndoState (self):
    
        """Clears then entire Undo state.
        
        All non-undoable commands should call this method."""
        
        u = self
        u.setRedoType("Can't Redo")
        u.setUndoType("Can't Undo")
        u.beads = [] # List of undo nodes.
        u.bead = -1 # Index of the present bead: -1:len(beads)
        u.clearIvars()
    #@nonl
    #@-node:ekr.20031218072017.3609:clearUndoState
    #@+node:ekr.20031218072017.3610:canRedo & canUndo
    # Translation does not affect these routines.
    
    def canRedo (self):
    
        u = self
        return u.redoMenuLabel != "Can't Redo"
    
    def canUndo (self):
    
        u = self
        return u.undoMenuLabel != "Can't Undo"
    #@-node:ekr.20031218072017.3610:canRedo & canUndo
    #@+node:ekr.20031218072017.3611:enableMenuItems
    def enableMenuItems (self):
    
        u = self ; frame = u.c.frame
        
        menu = frame.menu.getMenu("Edit")
        frame.menu.enableMenu(menu,u.redoMenuLabel,u.canRedo())
        frame.menu.enableMenu(menu,u.undoMenuLabel,u.canUndo())
    #@-node:ekr.20031218072017.3611:enableMenuItems
    #@+node:ekr.20031218072017.3612:getBead & peekBead
    #@+node:EKR.20040526150818:getBeed
    def getBead (self,n):
        
        u = self
        if n < 0 or n >= len(u.beads):
            return None
    
        bunch = u.beads[n]
        # g.trace(n,len(u.beads),'-'*20)
        self.clearIvars()
    
        if 0: # Debugging.
            keys = bunch.keys()
            keys.sort()
            for key in keys:
                g.trace(key,bunch.get(key))
    
        for key in bunch.keys():
            val = bunch.get(key)
            setattr(u,key,val)
            if key not in u.optionalIvars:
                u.optionalIvars.append(key)
    
        return bunch
    #@nonl
    #@-node:EKR.20040526150818:getBeed
    #@+node:EKR.20040526150818.1:peekBeed
    def peekBead (self,n):
        
        u = self
        if n < 0 or n >= len(u.beads):
            return None
        d = u.beads[n]
        # g.trace(n,len(u.beads),d)
        return d
    #@nonl
    #@-node:EKR.20040526150818.1:peekBeed
    #@-node:ekr.20031218072017.3612:getBead & peekBead
    #@+node:ekr.20031218072017.3613:redoMenuName, undoMenuName
    def redoMenuName (self,name):
    
        if name=="Can't Redo":
            return name
        else:
            return "Redo " + name
    
    def undoMenuName (self,name):
    
        if name=="Can't Undo":
            return name
        else:
            return "Undo " + name
    #@nonl
    #@-node:ekr.20031218072017.3613:redoMenuName, undoMenuName
    #@+node:ekr.20031218072017.3614:setRedoType, setUndoType
    # These routines update both the ivar and the menu label.
    def setRedoType (self,theType):
        u = self ; frame = u.c.frame
        menu = frame.menu.getMenu("Edit")
        name = u.redoMenuName(theType)
        if name != u.redoMenuLabel:
            # Update menu using old name.
            realLabel = frame.menu.getRealMenuName(name)
            if realLabel == name:
                underline=g.choose(g.match(name,0,"Can't"),-1,0)
            else:
                underline = realLabel.find("&")
            realLabel = realLabel.replace("&","")
            frame.menu.setMenuLabel(menu,u.realRedoMenuLabel,realLabel,underline=underline)
            u.redoMenuLabel = name
            u.realRedoMenuLabel = realLabel
    
    def setUndoType (self,theType):
        u = self ; frame = u.c.frame
        menu = frame.menu.getMenu("Edit")
        name = u.undoMenuName(theType)
        if name != u.undoMenuLabel:
            # Update menu using old name.
            realLabel = frame.menu.getRealMenuName(name)
            if realLabel == name:
                underline=g.choose(g.match(name,0,"Can't"),-1,0)
            else:
                underline = realLabel.find("&")
            realLabel = realLabel.replace("&","")
            frame.menu.setMenuLabel(menu,u.realUndoMenuLabel,realLabel,underline=underline)
            u.undoType = theType
            u.undoMenuLabel = name
            u.realUndoMenuLabel = realLabel
    #@nonl
    #@-node:ekr.20031218072017.3614:setRedoType, setUndoType
    #@+node:ekr.20031218072017.3616:setUndoTypes
    def setUndoTypes (self):
        
        u = self
    
        # g.trace(u.bead,len(u.beads))
    
        # Set the undo type and undo menu label.
        bunch = u.peekBead(u.bead)
        if bunch:
            u.setUndoType(bunch.undoType)
        else:
            u.setUndoType("Can't Undo")
    
        # Set only the redo menu label.
        bunch = u.peekBead(u.bead+1)
        if bunch:
            u.setRedoType(bunch.undoType)
        else:
            u.setRedoType("Can't Redo")
    #@nonl
    #@-node:ekr.20031218072017.3616:setUndoTypes
    #@-node:ekr.20031218072017.3608:State routines...
    #@+node:EKR.20040606195417:Top-level entries...
    #@+node:ekr.20050412110627:setUndoParams DUMMY
    def setUndoParams (self,undo_type,p,**keywords):
        pass
    #@nonl
    #@-node:ekr.20050412110627:setUndoParams DUMMY
    #@+node:ekr.20031218072017.1490:setUndoTypingParams & recognizeStartOfTypingWord
    #@+at 
    #@nonl
    # This routine saves enough information so a typing operation can be 
    # undone and redone.
    # 
    # We do nothing when called from the undo/redo logic because the Undo and 
    # Redo commands merely reset the bead pointer.
    #@-at
    #@@c
    
    def setUndoTypingParams (self,p,undo_type,oldText,newText,oldSel,newSel,oldYview=None):
        
        # g.trace(undo_type) # ,p,"old:",oldText,"new:",newText)
        u = self ; c = u.c
        #@    << return if there is nothing to do >>
        #@+node:ekr.20040324061854:<< return if there is nothing to do >>
        if u.redoing or u.undoing:
            return None
        
        if undo_type == None:
            return None
        
        if undo_type == "Can't Undo":
            u.clearUndoState()
            return None
        
        if oldText == newText:
            # g.trace("no change")
            return None
        #@nonl
        #@-node:ekr.20040324061854:<< return if there is nothing to do >>
        #@nl
        #@    << init the undo params >>
        #@+node:ekr.20040324061854.1:<< init the undo params >>
        # Clear all optional params.
        for ivar in u.optionalIvars:
            setattr(u,ivar,None)
        
        # Set the params.
        u.undoType = undo_type
        u.p = p.copy()
        #@nonl
        #@-node:ekr.20040324061854.1:<< init the undo params >>
        #@nl
        #@    << compute leading, middle & trailing  lines >>
        #@+node:ekr.20031218072017.1491:<< compute leading, middle & trailing  lines >>
        #@+at 
        #@nonl
        # Incremental undo typing is similar to incremental syntax coloring.  
        # We compute the number of leading and trailing lines that match, and 
        # save both the old and new middle lines.
        # 
        # NB: the number of old and new middle lines may be different.
        #@-at
        #@@c
        
        old_lines = string.split(oldText,'\n')
        new_lines = string.split(newText,'\n')
        new_len = len(new_lines)
        old_len = len(old_lines)
        min_len = min(old_len,new_len)
        
        i = 0
        while i < min_len:
            if old_lines[i] != new_lines[i]:
                break
            i += 1
        leading = i
        
        if leading == new_len:
            # This happens when we remove lines from the end.
            # The new text is simply the leading lines from the old text.
            trailing = 0
        else:
            i = 0
            while i < min_len - leading:
                if old_lines[old_len-i-1] != new_lines[new_len-i-1]:
                    break
                i += 1
            trailing = i
            
        # NB: the number of old and new middle lines may be different.
        if trailing == 0:
            old_middle_lines = old_lines[leading:]
            new_middle_lines = new_lines[leading:]
        else:
            old_middle_lines = old_lines[leading:-trailing]
            new_middle_lines = new_lines[leading:-trailing]
        
        # Remember how many trailing newlines in the old and new text.
        i = len(oldText) - 1 ; old_newlines = 0
        while i >= 0 and oldText[i] == '\n':
            old_newlines += 1
            i -= 1
        
        i = len(newText) - 1 ; new_newlines = 0
        while i >= 0 and newText[i] == '\n':
            new_newlines += 1
            i -= 1
        
        if 0: ## u.debug_print:
            print "lead,trail",leading,trailing
            print "old mid,nls:",len(old_middle_lines),old_newlines,oldText
            print "new mid,nls:",len(new_middle_lines),new_newlines,newText
            #print "lead,trail:",leading,trailing
            #print "old mid:",old_middle_lines
            #print "new mid:",new_middle_lines
            print "---------------------"
        #@nonl
        #@-node:ekr.20031218072017.1491:<< compute leading, middle & trailing  lines >>
        #@nl
        #@    << save undo text info >>
        #@+node:ekr.20031218072017.1492:<< save undo text info >>
        #@+at 
        #@nonl
        # This is the start of the incremental undo algorithm.
        # 
        # We must save enough info to do _both_ of the following:
        # 
        # Undo: Given newText, recreate oldText.
        # Redo: Given oldText, recreate oldText.
        # 
        # The "given" texts for the undo and redo routines are simply 
        # v.bodyString().
        #@-at
        #@@c
        
        if u.debug:
            # Remember the complete text for comparisons...
            u.oldText = oldText
            u.newText = newText
            # Compute statistics comparing old and new ways...
            # The old doesn't often store the old text, so don't count it here.
            u.old_mem += len(newText)
            s1 = string.join(old_middle_lines,'\n')
            s2 = string.join(new_middle_lines,'\n')
            u.new_mem += len(s1) + len(s2)
        else:
            u.oldText = None
            u.newText = None
        
        u.leading = leading
        u.trailing = trailing
        u.oldMiddleLines = old_middle_lines
        u.newMiddleLines = new_middle_lines
        u.oldNewlines = old_newlines
        u.newNewlines = new_newlines
        #@nonl
        #@-node:ekr.20031218072017.1492:<< save undo text info >>
        #@nl
        #@    << save the selection and scrolling position >>
        #@+node:ekr.20040324061854.2:<< save the selection and scrolling position >>
        #Remember the selection.
        u.oldSel = oldSel
        u.newSel = newSel
        
        # Remember the scrolling position.
        if oldYview:
            u.yview = oldYview
        else:
            u.yview = c.frame.body.getYScrollPosition()
        #@-node:ekr.20040324061854.2:<< save the selection and scrolling position >>
        #@nl
        #@    << adjust the undo stack, clearing all forward entries >>
        #@+node:ekr.20040324061854.3:<< adjust the undo stack, clearing all forward entries >>
        #@+at 
        #@nonl
        # New in Leo 4.3. Instead of creating a new bead on every character, 
        # we may adjust the top bead:
        # 
        # word granularity: adjust the top bead if the typing would continue 
        # the word.
        # line granularity: adjust the top bead if the typing is on the same 
        # line.
        # node granularity: adjust the top bead if the typing is anywhere on 
        # the same node.
        #@-at
        #@@c
        
        granularity = u.granularity
        
        old_d = u.peekBead(u.bead)
        old_p = old_d and old_d.get('p')
        
        #@<< set newBead if we can't share the previous bead >>
        #@+node:ekr.20050125220613:<< set newBead if we can't share the previous bead >>
        if (
            not old_d or not old_p or
            old_p.v != p.v or
            old_d.get('kind') != 'typing' or
            old_d.get('undoType') != 'Typing' or
            undo_type != 'Typing'
        ):
            newBead = True # We can't share the previous node.
        elif granularity == 'char':
            newBead = True # This was the old way.
        elif granularity == 'node':
            newBead = False # Always replace previous bead.
        else:
            assert granularity in ('line','word')
            # Replace the previous bead if only the middle lines have changed.
            newBead = (
                old_d.get('leading',0)  != u.leading or 
                old_d.get('trailing',0) != u.trailing
            )
            if granularity == 'word' and not newBead:
                # Protect the method that may be changed by the user
                try:
                    #@            << set newBead if the change does not continue a word >>
                    #@+node:ekr.20050125203937:<< set newBead if the change does not continue a word >>
                    old_start,old_end = oldSel
                    new_start,new_end = newSel
                    if old_start != old_end or new_start != new_end:
                        # The new and old characters are not contiguous.
                        newBead = True
                    else:
                        old_row,old_col = old_start.split('.')
                        new_row,new_col = new_start.split('.')
                        old_row,old_col = int(old_row),int(old_col)
                        new_row,new_col = int(new_row),int(new_col)
                        old_lines = g.splitLines(oldText)
                        new_lines = g.splitLines(newText)
                        #g.trace(old_row,old_col,len(old_lines))
                        #g.trace(new_row,new_col,len(new_lines))
                        # Recognize backspace, del, etc. as contiguous.
                        if old_row != new_row or abs(old_col-new_col) != 1:
                            # The new and old characters are not contiguous.
                            newBead = True
                        elif old_col == 0 or new_col == 0:
                            pass # We have just inserted a line.
                        else:
                            old_s = old_lines[old_row-1]
                            new_s = new_lines[new_row-1]
                            old_ch = old_s[old_col-1]
                            new_ch = new_s[new_col-1]
                            # g.trace(repr(old_ch),repr(new_ch))
                            newBead = self.recognizeStartOfTypingWord(
                                old_lines,old_row,old_col,old_ch,
                                new_lines,new_row,new_col,new_ch)
                    #@nonl
                    #@-node:ekr.20050125203937:<< set newBead if the change does not continue a word >>
                    #@nl
                except Exception:
                    if 0:
                        g.trace('old_lines',old_lines)
                        g.trace('new_lines',new_lines)
                    g.es('Exception in setUndoRedoTypingParams',color='blue')
                    g.es_exception()
                    newBead = True
        #@nonl
        #@-node:ekr.20050125220613:<< set newBead if we can't share the previous bead >>
        #@nl
        
        if newBead:
            # Push params on undo stack, clearing all forward entries.
            u.bead += 1
            bunch = g.Bunch(
                p = p.copy(),
                kind='typing',
                undoType = undo_type,
                undoHelper=u.undoTyping,
                redoHelper=u.redoTyping,
                oldText=u.oldText,
                oldSel=u.oldSel,
                oldNewlines=u.oldNewlines,
                oldMiddleLines=u.oldMiddleLines,
            )
        else:
            bunch = old_d
        
        bunch.leading=u.leading
        bunch.trailing= u.trailing
        bunch.newNewlines=u.newNewlines
        bunch.newMiddleLines=u.newMiddleLines
        bunch.newSel=u.newSel
        bunch.newText=u.newText
        bunch.yview=u.yview
        
        u.beads[u.bead:] = [bunch]
            
        # g.trace(newBead,'u.bead',u.bead,undo_type,old_p)
        #@nonl
        #@-node:ekr.20040324061854.3:<< adjust the undo stack, clearing all forward entries >>
        #@nl
        u.setUndoTypes() # Recalculate the menu labels.
        return bunch
    #@nonl
    #@+node:ekr.20050126081529:recognizeStartOfTypingWord
    def recognizeStartOfTypingWord (self,
        old_lines,old_row,old_col,old_ch, 
        new_lines,new_row,new_col,new_ch):
            
        ''' A potentially user-modifiable method that should return True if the
        typing indicated by the params starts a new 'word' for the purposes of
        undo with 'word' granularity.
        
        u.setUndoTypingParams calls this method only when the typing could possibly
        continue a previous word. In other words, undo will work safely regardless
        of the value returned here.
        
        old_ch is the char at the given (Tk) row, col of old_lines.
        new_ch is the char at the given (Tk) row, col of new_lines.
        
        The present code uses only old_ch and new_ch. The other arguments are given
        for use by more sophisticated algorithms.'''
        
        ws = string.whitespace
        word_chars = string.letters + string.digits + '_'
    
        if 1: # This seems like the best way.
            # Start a word if new_ch begins whitespace + word
            return old_ch not in ws and new_ch in ws
    
        if 0: # Problems with punctuation within words.
            return old_ch in ws and new_ch not in ws
    
        if 0: # Problems with punctuation within words.
            return new_ch in word_chars and not old_ch in word_chars
            
        else: return False # Keeps Pychecker happy.
    #@nonl
    #@-node:ekr.20050126081529:recognizeStartOfTypingWord
    #@-node:ekr.20031218072017.1490:setUndoTypingParams & recognizeStartOfTypingWord
    #@+node:EKR.20040528075307:u.saveTree
    def saveTree (self,p,treeInfo=None):
        
        """Return a list of tuples with all info needed to handle a general undo operation."""
    
        # WARNING: read this before doing anything "clever"
        #@    << about u.saveTree >>
        #@+node:EKR.20040530114124:<< about u.saveTree >>
        #@+at 
        # The old code made a free-standing copy of the tree using v.copy and 
        # t.copy.  This looks "elegant" and is WRONG.  The problem is that it 
        # can not handle clones properly, especially when some clones were in 
        # the "undo" tree and some were not.   Moreover, it required complex 
        # adjustments to t.vnodeLists.
        # 
        # Instead of creating new nodes, the new code creates all information 
        # needed to properly restore the vnodes and tnodes.  It creates a list 
        # of tuples, on tuple for each vnode in the tree.  Each tuple has the 
        # form,
        # 
        # (vnodeInfo, tnodeInfo)
        # 
        # where vnodeInfo and tnodeInfo are dicts contain all info needed to 
        # recreate the nodes.  The v.createUndoInfoDict and 
        # t.createUndoInfoDict methods correspond to the old v.copy and t.copy 
        # methods.
        # 
        # Aside:  Prior to 4.2 Leo used a scheme that was equivalent to the 
        # createUndoInfoDict info, but quite a bit uglier.
        #@-at
        #@nonl
        #@-node:EKR.20040530114124:<< about u.saveTree >>
        #@nl
        
        u = self ; topLevel = (treeInfo == None)
        if topLevel: treeInfo = []
    
        # Add info for p.v and p.v.t.  Duplicate tnode info is harmless.
        data = (p.v,p.v.createUndoInfo(),p.v.t.createUndoInfo())
        treeInfo.append(data)
    
        # Recursively add info for the subtree.
        child = p.firstChild()
        while child:
            self.saveTree(child,treeInfo)
            child = child.next()
    
        # if topLevel: g.trace(treeInfo)
        return treeInfo
    #@-node:EKR.20040528075307:u.saveTree
    #@+node:EKR.20040530121329:u.restoreTree
    def restoreTree (self,treeInfo):
        
        """Use the tree info to restore all vnode and tnode data,
        including all links."""
        
        # This effectively relinks all vnodes.
        
        for v,vInfo,tInfo in treeInfo:
            v.restoreUndoInfo(vInfo)
            v.t.restoreUndoInfo(tInfo)
    #@nonl
    #@-node:EKR.20040530121329:u.restoreTree
    #@-node:EKR.20040606195417:Top-level entries...
    #@+node:ekr.20050315133212.1:New top-level entries...
    #@+node:ekr.20050318085432.3:before undo handlers...
    #@+node:ekr.20050318085432.2:createCommonBunch
    def createCommonBunch (self,p):
        
        '''Return a bunch containing all common undo info.
        This is mostly the info for recreating an empty node at position p.'''
        
        u = self ; c = u.c ; body = c.frame.body
        
        return g.Bunch(
            oldChanged = c.isChanged(),
            oldDirty = p.isDirty(),
            oldMarked = p.isMarked(),
            oldSel = body.getTextSelection(),
            p = p.copy(),
        )
    #@nonl
    #@-node:ekr.20050318085432.2:createCommonBunch
    #@+node:ekr.20050315133212.2:beforeChangeNodeContents
    def beforeChangeNodeContents (self,p):
        
        '''Return data that gets passed to afterChangeNode'''
        
        u = self
        
        bunch = u.createCommonBunch(p)
        
        bunch.oldBody = p.bodyString()
        bunch.oldHead = p.headString()
    
        return bunch
    #@nonl
    #@-node:ekr.20050315133212.2:beforeChangeNodeContents
    #@+node:ekr.20050315134017.6:beforeChangeTree
    def beforeChangeTree (self,p):
        
        # g.trace(p.headString())
        
        u = self ; body = u.c.frame.body
    
        bunch = u.createCommonBunch(p)
    
        bunch.oldSel = body.getTextSelection()
        bunch.oldText = body.getAllText()
        bunch.oldTree = u.saveTree(p)
        
        return bunch
    #@nonl
    #@-node:ekr.20050315134017.6:beforeChangeTree
    #@+node:ekr.20050315134017.7:beforeChangeGroup
    def beforeChangeGroup (self,p,command):
        
        u = self
        bunch = u.createCommonBunch(p)
        
        # Set types.
        bunch.kind = 'beforeGroup'
        bunch.undoType = command
        
        # Set helper only for redo:
        # The bead pointer will point to an 'afterGroup' bead for undo.
        bunch.undoHelper = None
        bunch.redoHelper = u.redoGroup
    
        # Push the bunch.
        u.bead += 1
        u.beads[u.bead:] = [bunch]
    #@nonl
    #@-node:ekr.20050315134017.7:beforeChangeGroup
    #@+node:ekr.20050412080354:beforeCloneNodeTEST
    def beforeCloneNode (self,p):
        
        u = self
    
        bunch = u.createCommonBunch(p)
    
        return bunch
    #@nonl
    #@-node:ekr.20050412080354:beforeCloneNodeTEST
    #@+node:ekr.20050411193627.3:beforeDeleteNode TEST
    def beforeDeleteNode (self,p):
        
        u = self
    
        bunch = u.createCommonBunch(p)
        
        bunch.oldBack = p.back()
        bunch.oldParent = p.parent()
        
        return bunch
    #@nonl
    #@-node:ekr.20050411193627.3:beforeDeleteNode TEST
    #@+node:ekr.20050411193627.4:beforeInsertNode TEST
    def beforeInsertNode (self,p):
        
        u = self
    
        bunch = u.createCommonBunch(p)
    
        return bunch
    #@nonl
    #@-node:ekr.20050411193627.4:beforeInsertNode TEST
    #@+node:ekr.20050410110215:beforeMoveNode
    def beforeMoveNode (self,p):
        
        u = self
        
        bunch = u.createCommonBunch(p)
        
        bunch.oldBack = p.back()
        bunch.oldN = p.childIndex()
        bunch.oldParent = p.parent()
    
        return bunch
    #@nonl
    #@-node:ekr.20050410110215:beforeMoveNode
    #@-node:ekr.20050318085432.3:before undo handlers...
    #@+node:ekr.20050318085432.4:after undo handlers...
    #@+node:ekr.20050315134017.2:afterChangeNodeContents TESTED
    def afterChangeNodeContents (self,p,command,bunch):
    
        '''Create an undo node using d created by beforeChangeNode.'''
        
        u = self ; body = u.c.frame.body
        if u.redoing or u.undoing:
            return
    
        # Set the type & helpers.
        bunch.kind = 'node'
        bunch.undoType = command
        bunch.undoHelper = u.undoNodeContents
        bunch.redoHelper = u.redoNodeContents
    
        bunch.newBody = p.bodyString()
        bunch.newChanged = u.c.isChanged()
        bunch.newDirty = p.isDirty()
        bunch.newHead = p.headString()
        bunch.newMarked = p.isMarked()
        bunch.newSel = body.getTextSelection()
        
        # Push the bunch.
        u.bead += 1
        u.beads[u.bead:] = [bunch]
    
        # Recalculate the menu labels.
        u.setUndoTypes()
    #@nonl
    #@-node:ekr.20050315134017.2:afterChangeNodeContents TESTED
    #@+node:ekr.20050315134017.3:afterChangeTree (Needed?)
    def afterChangeTree (self,p,command,bunch):
    
        '''Create an undo node for general tree operations using d created by beforeChangeTree'''
        
        u = self ; body = u.c.frame.body
        if u.redoing or u.undoing: return
        
        # Set the types & helpers.
        bunch.kind = 'tree'
        bunch.undoType = command
        bunch.undoHelper = u.undoTree
        bunch.redoHelper = u.redoTree
    
        # Set by beforeChangeTree: changed, oldSel, oldText, oldTree, p
        bunch.newSel = body.getTextSelection()
        bunch.newText = body.getAllText()
        bunch.newTree = u.saveTree(p) # Was done in setUndoParams...
    
        # Push the bunch, not a dict.
        u.bead += 1
        u.beads[u.bead:] = [bunch]
    
        # Recalculate the menu labels.
        u.setUndoTypes()
    #@nonl
    #@-node:ekr.20050315134017.3:afterChangeTree (Needed?)
    #@+node:ekr.20050315134017.4:afterChangeGroup TESTED
    def afterChangeGroup (self,p,command,reportFlag=False,dirtyVnodeList=[]):
    
        '''Create an undo node for general tree operations using d created by beforeChangeTree'''
        
        u = self ; body = u.c.frame.body
        if u.redoing or u.undoing: return
        
        # Must use a _separate_ bunch than that created by beforeChangeGroup.
        # (To allow separate bunch.kind fields.
        bunch = u.createCommonBunch(p)
    
        # Set the types & helpers.
        bunch.kind = 'afterGroup'
        bunch.undoType = command
        
        # Set helper only for undo:
        # The bead pointer will point to an 'beforeGroup' bead for redo.
        bunch.undoHelper = u.undoGroup
        bunch.redoHelper = None
        
        bunch.dirtyVnodeList = dirtyVnodeList
        
        bunch.newP = p.copy()
        bunch.newSel = body.getTextSelection()
        
        # Tells whether to report the number of separate changes undone/redone.
        bunch.reportFlag = reportFlag
    
        # Push the bunch.
        u.bead += 1
        u.beads[u.bead:] = [bunch]
    
        # Recalculate the menu labels.
        u.setUndoTypes()
    #@-node:ekr.20050315134017.4:afterChangeGroup TESTED
    #@+node:ekr.20050411193627.5:afterCloneNode TEST
    def afterCloneNode (self,p,command,bunch,dirtyVnodeList=[]):
        
        u = self
        
        # Set types & helpers
        bunch.kind = 'clone'
        bunch.undoType = command
        
        # Set helpers
        bunch.undoHelper = u.undoCloneNode
        bunch.redoHelper = u.redoCloneNode
        
        bunch.newP = p.copy()
        bunch.dirtyVnodeList = dirtyVnodeList
        
        bunch.newChanged = p.c.isChanged()
        bunch.newDirty = p.isDirty()
        bunch.newMarked = p.isMarked()
    
        # Push the bunch.
        u.bead += 1
        u.beads[u.bead:] = [bunch]
        
        # Recalculate the menu labels.
        u.setUndoTypes()
    #@nonl
    #@-node:ekr.20050411193627.5:afterCloneNode TEST
    #@+node:ekr.20050411193627.6:afterDehoistNode TEST
    def afterDehoistNode (self,p,command):
    
        u = self
        
        bunch = u.createCommonBunch(p)
        
        # Set types & helpers
        bunch.kind = 'dehoist'
        bunch.undoType = command
        
        # Set helpers
        bunch.undoHelper = u.undoDehoistNode
        bunch.redoHelper = u.redoDehoistNode
    
        # Push the bunch.
        u.bead += 1
        u.beads[u.bead:] = [bunch]
        
        # Recalculate the menu labels.
        u.setUndoTypes()
    #@nonl
    #@-node:ekr.20050411193627.6:afterDehoistNode TEST
    #@+node:ekr.20050411193627.7:afterHoistNode TEST
    def afterHoistNode (self,p,command):
        
        u = self
        
        bunch = u.createCommonBunch(p)
        
        # Set types & helpers
        bunch.kind = 'hoist'
        bunch.undoType = command
        
        # Set helpers
        bunch.undoHelper = u.undoHoistNode
        bunch.redoHelper = u.redoHoistNode
    
        # Push the bunch.
        u.bead += 1
        u.beads[u.bead:] = [bunch]
        
        # Recalculate the menu labels.
        u.setUndoTypes()
    #@nonl
    #@-node:ekr.20050411193627.7:afterHoistNode TEST
    #@+node:ekr.20050411193627.8:afterDeleteNode TEST
    def afterDeleteNode (self,p,command,bunch,dirtyVnodeList=[]):
        
        u = self
        
        # Set types & helpers
        bunch.kind = 'delete'
        bunch.undoType = command
        
        # Set helpers
        bunch.undoHelper = u.undoDeleteNode
        bunch.redoHelper = u.redoDeleteNode
        
        bunch.newP = p.copy()
        bunch.dirtyVnodeList = dirtyVnodeList
        
        bunch.newChanged = p.c.isChanged()
        bunch.newDirty = p.isDirty()
        bunch.newMarked = p.isMarked()
    
        # Push the bunch.
        u.bead += 1
        u.beads[u.bead:] = [bunch]
        
        # Recalculate the menu labels.
        u.setUndoTypes()
    #@nonl
    #@-node:ekr.20050411193627.8:afterDeleteNode TEST
    #@+node:ekr.20050411193627.9:afterInsertNode TEST
    def afterInsertNode (self,p,command,bunch,dirtyVnodeList=[]):
        
        u = self ; c = u.c
        
        # Set types & helpers
        bunch.kind = 'insert'
        bunch.undoType = command
        
        # Set helpers
        bunch.undoHelper = u.undoInsertNode
        bunch.redoHelper = u.redoInsertNode
        
        bunch.newP = p.copy()
        bunch.newCurrent = c.currentPosition()
        bunch.newBack = p.back()
        bunch.newParent = p.parent()
    
        bunch.dirtyVnodeList = dirtyVnodeList
        
        bunch.newChanged = c.isChanged()
        bunch.newDirty = p.isDirty()
        bunch.newMarked = p.isMarked()
    
        # Push the bunch.
        u.bead += 1
        u.beads[u.bead:] = [bunch]
        
        # Recalculate the menu labels.
        u.setUndoTypes()
    #@nonl
    #@-node:ekr.20050411193627.9:afterInsertNode TEST
    #@+node:ekr.20050410110343:afterMoveNode
    def afterMoveNode (self,p,command,bunch,dirtyVnodeList=[]):
        
        u = self
        
        # Set the types & helpers.
        bunch.kind = 'move'
        bunch.undoType = command
        
        # Set helper only for undo:
        # The bead pointer will point to an 'beforeGroup' bead for redo.
        bunch.undoHelper = u.undoMove
        bunch.redoHelper = u.redoMove
        
        bunch.newChanged = p.c.isChanged()
        bunch.newDirty = p.isDirty()
        bunch.newMarked = p.isMarked()
        
        bunch.dirtyVnodeList = dirtyVnodeList
    
        bunch.newBack   = p.back()
        bunch.newN = p.childIndex()
        bunch.newParent = p.parent()
        
        # Push the bunch.
        u.bead += 1
        u.beads[u.bead:] = [bunch]
    
        # Recalculate the menu labels.
        u.setUndoTypes()
    #@nonl
    #@-node:ekr.20050410110343:afterMoveNode
    #@-node:ekr.20050318085432.4:after undo handlers...
    #@+node:ekr.20050410095424:updateMarks
    def updateMarks (self,oldOrNew):
        
        '''Update dirty and marked bits.'''
        
        u = self
        
        if oldOrNew not in ('new','old'):
            g.trace("can't happen")
            return
    
        isOld = oldOrNew=='old'
        dirty   = g.choose(isOld,u.oldDirty,  u.newDirty)
        marked  = g.choose(isOld,u.oldMarked, u.newMarked)
        changed = g.choose(isOld,u.oldChanged,u.newChanged)
    
        if dirty:   u.p.setDirty(setDescendentsDirty=False)
        else:       u.p.clearDirty()
            
        if marked:  u.p.setMarked()
        else:       u.p.clearMarked()
    
        u.c.setChanged(changed,tag='updateMarks')
    #@-node:ekr.20050410095424:updateMarks
    #@-node:ekr.20050315133212.1:New top-level entries...
    #@+node:ekr.20031218072017.2030:redo & helpers...
    def redo (self):
    
        u = self ; c = u.c
        if not u.canRedo(): return
        if not u.getBead(u.bead+1): return
        if not  c.currentPosition(): return
        # g.trace(u.bead+1,len(u.beads),u.peekBead(u.bead+1))
    
        u.redoing = True 
        u.redrawFlag = True
        u.groupCount = 0
    
        # Execute the redoHelper.
        c.beginUpdate()
        u.redoHelper()
        c.endUpdate(u.redrawFlag)
    
        u.redoing = False
        u.bead += 1
        u.setUndoTypes()
    #@nonl
    #@+node:ekr.20050412083057:redoCloneNode TEST
    def redoCloneNode (self):
        
        u = self ; c = u.c
        
        if u.newBack:
            u.newP.linkAfter(u.newBack)
        elif u.newParent:
            u.newP.linkAsNthChild(u.newParent,0)
        else:
            oldRoot = c.rootPosition()
            u.newP.linkAsRoot(oldRoot)
    
        c.selectVnode(u.newP)
    #@nonl
    #@-node:ekr.20050412083057:redoCloneNode TEST
    #@+node:EKR.20040526072519.2:redoDeleteNode TEST
    def redoDeleteNode (self):
        
        u = self ; c = u.c
    
        c.selectPosition(u.newP)
        c.deleteOutline()
        c.selectPosition(u.p)
    #@nonl
    #@-node:EKR.20040526072519.2:redoDeleteNode TEST
    #@+node:ekr.20050412084532:redoInsertNode TEST
    def redoInsertNode (self):
        
        u = self ; c = u.c
    
        if u.newBack:
            u.newP.linkAfter(u.newBack)
        elif u.newParent:
            u.newP.linkAsNthChild(u.newParent,0)
        else:
            oldRoot = c.rootPosition()
            u.newP.linkAsRoot(oldRoot)
            
        # Restore all vnodeLists (and thus all clone marks).
        u.newP.restoreLinksInTree()
    
        c.selectVnode(u.newCurrent)
    #@nonl
    #@-node:ekr.20050412084532:redoInsertNode TEST
    #@+node:ekr.20050412085138.1:redoHoistNode & redoDehoistNode TEST
    def redoHoistNode (self):
        
        u = self ; c = u.c
        
        c.selectVnode(u.p)
        c.hoist()
        
    def redoDehoistNode (self):
        
        u = self ; c = u.c
        
        c.selectVnode(u.p)
        c.dehoist()
    #@nonl
    #@-node:ekr.20050412085138.1:redoHoistNode & redoDehoistNode TEST
    #@+node:ekr.20050318085432.6:redoGroup
    def redoGroup (self):
        
        '''Process beads until the matching 'afterGroup' bead is seen.'''
        
        u = self ; c = u.c ; count = 0
        u.groupCount += 1
        while 1:
            u.bead += 1
            d = u.getBead(u.bead+1) # sets ivars, including u.p.
            if not d:
                s = "Undo stack overrun for %s" % u.undoType
                g.trace(s) ; g.es(s, color="red")
                break
            elif u.kind == 'afterGroup':
                break
            elif u.redoHelper:
                count += 1
                u.redoHelper()
            else:
                s = "No redo helper for %s" % u.undoType
                g.trace(s) ; g.es(s, color="red")
        u.groupCount -= 1
        
        if u.dirtyVnodeList: # May be None instead of [].
            for v in u.dirtyVnodeList:
                v.t.setDirty()
    
        if u.reportFlag:
            g.es("redo %d instances" % count)
            
        c.selectVnode(u.p)
        if u.newSel:
            c.frame.body.setTextSelection(u.newSel)
    #@nonl
    #@-node:ekr.20050318085432.6:redoGroup
    #@+node:ekr.20050318085432.7:redoNodeContents
    def redoNodeContents (self):
        
        u = self
        
        u.p.v.setTnodeText(u.newBody)
        u.p.v.initHeadString(u.newHead)
        
        if u.groupCount == 0 and u.newSel:
            u.c.frame.body.setTextSelection(u.newSel)
        
        u.updateMarks('new')
    #@nonl
    #@-node:ekr.20050318085432.7:redoNodeContents
    #@+node:ekr.20050411111847:redoMove
    def redoMove (self):
        
        u = self ; c = u.c
    
        # g.trace(u.p)
    
        if u.newParent:
            u.p.moveToNthChildOf(u.newParent,u.newN)
        elif u.newBack:
            u.p.moveAfter(u.newBack)
        else:
            oldRoot = c.rootPosition()
            u.p.moveToRoot(oldRoot)
            
        u.updateMarks('new')
    
        for v in u.dirtyVnodeList:
            v.t.setDirty()
            
        # Selecting can scroll the tree which causes flash.
        if u.groupCount == 0:
            c.selectPosition(u.p)
    #@nonl
    #@-node:ekr.20050411111847:redoMove
    #@+node:ekr.20050318085432.8:redoTree
    def redoTree (self):
        
        '''Redo replacement of an entire tree.'''
        
        u = self ; c = u.c
        
        g.trace()
    
        u.p = self.undoRedoTree(u.p,u.oldTree,u.newTree)
        c.selectVnode(u.p) # Does full recolor.
        if u.newSel:
            c.frame.body.setTextSelection(u.newSel)
    #@nonl
    #@-node:ekr.20050318085432.8:redoTree
    #@+node:EKR.20040526075238.5:redoTyping
    def redoTyping (self):
    
        u = self ; c = u.c ; current = c.currentPosition()
    
        # selectVnode causes recoloring, so avoid if possible.
        if current != u.p:
            c.selectVnode(u.p)
        elif u.undoType in ('Cut','Paste','Clear Recent Files'):
            c.frame.body.forceFullRecolor()
    
        self.undoRedoText(
            u.p,u.leading,u.trailing,
            u.newMiddleLines,u.oldMiddleLines,
            u.newNewlines,u.oldNewlines,
            tag="redo",undoType=u.undoType)
        
        if u.newSel:
            c.frame.body.setTextSelection(u.newSel)
        if u.yview:
            c.frame.body.setYScrollPosition(u.yview)
            
        u.redrawFlag = (current != u.p)
    #@nonl
    #@-node:EKR.20040526075238.5:redoTyping
    #@-node:ekr.20031218072017.2030:redo & helpers...
    #@+node:ekr.20031218072017.2039:undo & helpers...
    def undo (self):
    
        """Undo the operation described by the undo parmaters."""
        
        u = self ; c = u.c
        if not u.canUndo(): return
        if not u.getBead(u.bead): return # Sets ivars.
        if not c.currentPosition(): return
        # g.trace(len(u.beads),u.bead,u.peekBead(u.bead))
    
        c.endEditing()# Make sure we capture the headline for a redo.
        u.undoing = True
        u.redrawFlag = True
        u.groupCount = 0
    
        # Execute the undoHelper.
        c.beginUpdate()
        u.undoHelper()
        c.endUpdate(u.redrawFlag)
    
        u.undoing = False
        u.bead -= 1
        u.setUndoTypes()
    #@nonl
    #@+node:ekr.20050412083057.1:undoCloneNode TEST
    def undoCloneNode (self):
        
        u = self ; c = u.c
    
        c.selectVnode(u.newP)
        c.deleteOutline()
        c.selectVnode(u.p)
    #@nonl
    #@-node:ekr.20050412083057.1:undoCloneNode TEST
    #@+node:ekr.20050412084055:undoDeleteNode TEST
    def undoDeleteNode (self):
        
        u = self ; c = u.c
        
        if u.oldBack:
            u.p.linkAfter(u.oldBack)
        elif u.parent:
            u.p.linkAsNthChild(u.oldParent,0)
        else:
            oldRoot = c.rootPosition()
            u.p.linkAsRoot(oldRoot)
            
        # Restore all vnodeLists (and thus all clone marks).
        u.p.restoreLinksInTree()
    
        c.selectVnode(u.p)
    #@nonl
    #@-node:ekr.20050412084055:undoDeleteNode TEST
    #@+node:ekr.20050318085713:undoGroup
    def undoGroup (self):
        
        '''Process beads until the matching 'beforeGroup' bead is seen.'''
    
        u = self ; c = u.c ; count = 0
        reportFlag = u.reportFlag
        u.groupCount += 1
    
        while 1:
            u.bead -= 1
            d = u.getBead(u.bead) # sets ivars, including u.p.
            if not d:
                s = "Undo stack underrun for %s" % u.undoType
                g.trace(s) ; g.es(s, color="red")
                break
            elif u.kind == 'beforeGroup':
                break
            elif u.undoHelper:
                count += 1
                u.undoHelper()
            else:
                s = "No undo helper for %s" % u.undoType
                g.trace(s) ; g.es(s, color="red")
               
        if u.dirtyVnodeList: # May be None instead of [].
            for v in u.dirtyVnodeList:
                v.t.clearDirty()
    
        u.groupCount -= 1
        if reportFlag:
            g.es("undo %d instances" % count)
            
        c.selectPosition(u.p)
        if u.oldSel:
            c.frame.body.setTextSelection(u.oldSel)
    #@nonl
    #@-node:ekr.20050318085713:undoGroup
    #@+node:ekr.20050412083244:undoHoistNode & undoDehoistNode TEST
    def undoHoistNode (self):
        
        u = self ; c = u.c
    
        c.selectVnode(u.p)
        c.dehoist()
        
    def undoDehoistNode (self):
        
        u = self ; c = u.c
    
        c.selectVnode(u.p)
        c.hoist()
    #@nonl
    #@-node:ekr.20050412083244:undoHoistNode & undoDehoistNode TEST
    #@+node:ekr.20050412085112:undoInsertNode TEST
    def undoInsertNode (self):
        
        u = self ; c = u.c
    
        c.selectVnode(u.newP)
        c.deleteOutline()
        c.selectVnode(u.p)
    #@nonl
    #@-node:ekr.20050412085112:undoInsertNode TEST
    #@+node:ekr.20050411112033:undoMove
    def undoMove (self):
        
        u = self ; c = u.c
    
        # g.trace(u.p)
    
        if u.oldParent:
            u.p.moveToNthChildOf(u.oldParent,u.oldN)
        elif u.oldBack:
            u.p.moveAfter(u.oldBack)
        else:
            oldRoot = c.rootPosition()
            u.p.moveToRoot(oldRoot)
    
        u.updateMarks('old')
        
        for v in u.dirtyVnodeList:
            v.t.clearDirty()
    
        # Selecting can scroll the tree which causes flash.
        if u.groupCount == 0:
            c.selectPosition(u.p)
    #@nonl
    #@-node:ekr.20050411112033:undoMove
    #@+node:ekr.20050318085713.1:undoNodeContents
    def undoNodeContents (self):
        
        '''Undo all changes to the contents of a node,
        including headline and body text, and dirty and marked bits.
        '''
        
        u = self
        
        u.p.v.setTnodeText(u.oldBody)
        u.p.v.initHeadString(u.oldHead)
    
        if u.groupCount == 0 and u.oldSel:
            u.c.frame.body.setTextSelection(u.oldSel)
        
        u.updateMarks('old')
    #@nonl
    #@-node:ekr.20050318085713.1:undoNodeContents
    #@+node:ekr.20050318085713.2:undoTree (needed??)
    def undoTree (self):
        
        '''Redo replacement of an entire tree.'''
        
        u = self ; c = u.c
    
        u.p = self.undoRedoTree(u.p,u.newTree,u.oldTree)
        c.selectVnode(u.p) # Does full recolor.
        if u.oldSel:
            c.frame.body.setTextSelection(u.oldSel)
    #@nonl
    #@-node:ekr.20050318085713.2:undoTree (needed??)
    #@+node:ekr.20050408100042:undoRedoTree
    def undoRedoTree (self,p,new_data,old_data):
        
        '''Replace p and its subtree using old_data during undo.'''
        
        # Same as undoReplace except uses g.Bunch.
    
        u = self ; c = u.c
        
        if new_data == None:
            # This is the first time we have undone the operation.
            # Put the new data in the bead.
            bunch = u.beads[u.bead]
            bunch.newTree = u.saveTree(p.copy())
            u.beads[u.bead] = bunch
        
        # Replace data in tree with old data.
        u.restoreTree(old_data)
        p.setBodyStringOrPane(p.bodyString())
        
        return p # Nothing really changes.
    #@nonl
    #@-node:ekr.20050408100042:undoRedoTree
    #@+node:EKR.20040526090701.4:undoTyping
    def undoTyping (self):
        
        u = self ; c = u.c ; current = c.currentPosition()
    
        # selectVnode causes recoloring, so don't do this unless needed.
        if current != u.p:
            c.selectVnode(u.p)
        elif u.undoType in ("Cut","Paste",'Clear Recent Files'):
            c.frame.body.forceFullRecolor()
    
        self.undoRedoText(
            u.p,u.leading,u.trailing,
            u.oldMiddleLines,u.newMiddleLines,
            u.oldNewlines,u.newNewlines,
            tag="undo",undoType=u.undoType)
    
        if u.oldSel:
            c.frame.body.setTextSelection(u.oldSel)
        if u.yview:
            c.frame.body.setYScrollPosition(u.yview)
            
        u.redrawFlag = (current != u.p)
    #@nonl
    #@-node:EKR.20040526090701.4:undoTyping
    #@+node:ekr.20031218072017.1493:undoRedoText
    # Handle text undo and redo.
    # The terminology is for undo: converts _new_ text into _old_ text.
    
    def undoRedoText (self,p,
        leading,trailing, # Number of matching leading & trailing lines.
        oldMidLines,newMidLines, # Lists of unmatched lines.
        oldNewlines,newNewlines, # Number of trailing newlines.
        tag="undo", # "undo" or "redo"
        undoType=None):
    
        u = self ; c = u.c
        assert(p == c.currentPosition())
    
        #@    << Incrementally update the Tk.Text widget >>
        #@+node:ekr.20031218072017.1494:<< Incrementally update the Tk.Text widget >>
        # Only update the changed lines.
        mid_text = string.join(oldMidLines,'\n')
        new_mid_len = len(newMidLines)
        # Maybe this could be simplified, and it is good to treat the "end" with care.
        if trailing == 0:
            c.frame.body.deleteLine(leading)
            if leading > 0:
                c.frame.body.insertAtEnd('\n')
            c.frame.body.insertAtEnd(mid_text)
        else:
            if new_mid_len > 0:
                c.frame.body.deleteLines(leading,new_mid_len)
            elif leading > 0:
                c.frame.body.insertAtStartOfLine(leading,'\n')
            c.frame.body.insertAtStartOfLine(leading,mid_text)
        # Try to end the Tk.Text widget with oldNewlines newlines.
        # This may be off by one, and we don't care because
        # we never use body text to compute undo results!
        s = c.frame.body.getAllText()
        newlines = 0 ; i = len(s) - 1
        while i >= 0 and s[i] == '\n':
            newlines += 1 ; i -= 1
        # g.trace(newlines,oldNewlines)
        while newlines > oldNewlines:
            c.frame.body.deleteLastChar()
            newlines -= 1
        if oldNewlines > newlines:
            c.frame.body.insertAtEnd('\n'*(oldNewlines-newlines))
        #@nonl
        #@-node:ekr.20031218072017.1494:<< Incrementally update the Tk.Text widget >>
        #@nl
        #@    << Compute the result using p's body text >>
        #@+node:ekr.20031218072017.1495:<< Compute the result using p's body text >>
        # Recreate the text using the present body text.
        body = p.bodyString()
        body = g.toUnicode(body,"utf-8")
        body_lines = body.split('\n')
        s = []
        if leading > 0:
            s.extend(body_lines[:leading])
        if len(oldMidLines) > 0:
            s.extend(oldMidLines)
        if trailing > 0:
            s.extend(body_lines[-trailing:])
        s = string.join(s,'\n')
        # Remove trailing newlines in s.
        while len(s) > 0 and s[-1] == '\n':
            s = s[:-1]
        # Add oldNewlines newlines.
        if oldNewlines > 0:
            s = s + '\n' * oldNewlines
        result = s
        if u.debug_print:
            print "body:  ",body
            print "result:",result
        #@nonl
        #@-node:ekr.20031218072017.1495:<< Compute the result using p's body text >>
        #@nl
        # g.trace(undoType)
        p.setTnodeText(result)
        #@    << Get textResult from the Tk.Text widget >>
        #@+node:ekr.20031218072017.1496:<< Get textResult from the Tk.Text widget >>
        textResult = c.frame.body.getAllText()
        
        if textResult != result:
            # Remove the newline from textResult if that is the only difference.
            if len(textResult) > 0 and textResult[:-1] == result:
                textResult = result
        #@nonl
        #@-node:ekr.20031218072017.1496:<< Get textResult from the Tk.Text widget >>
        #@nl
        if textResult == result:
            if undoType in ("Cut","Paste"):
                # g.trace("non-incremental undo")
                c.frame.body.recolor(p,incremental=False)
            else:
                # g.trace("incremental undo:",leading,trailing)
                c.frame.body.recolor_range(p,leading,trailing)
        else: # 11/19/02: # Rewrite the pane and do a full recolor.
            if u.debug_print:
                #@            << print mismatch trace >>
                #@+node:ekr.20031218072017.1497:<< print mismatch trace >>
                print "undo mismatch"
                print "expected:",result
                print "actual  :",textResult
                #@nonl
                #@-node:ekr.20031218072017.1497:<< print mismatch trace >>
                #@nl
            # g.trace("non-incremental undo")
            p.setBodyStringOrPane(result)
    #@nonl
    #@-node:ekr.20031218072017.1493:undoRedoText
    #@-node:ekr.20031218072017.2039:undo & helpers...
    #@-others
    
class undoer (baseUndoer):
    """A class that implements unlimited undo and redo."""
    pass
#@nonl
#@-node:ekr.20031218072017.3605:class undoer
#@+node:ekr.20031218072017.2243:class nullUndoer
class nullUndoer (undoer):

    def __init__ (self,c):
        
        undoer.__init__(self,c) # init the base class.

    def clearUndoState (self):
        pass
        
    def canRedo (self):
        return False

    def canUndo (self):
        return False
        
    def enableMenuItems (self):
        pass

    def getBead (self,n):
        return {}
    
    def peekBead (self,n):
        return {}

    def redoMenuName (self,name):
        return "Can't Redo"
    
    def undoMenuName (self,name):
        return "Can't Undo"
            
    def setUndoParams (self,undo_type,v,**keywords):
        pass
        
    def setUndoTypingParams (self,v,undo_type,oldText,newText,oldSel,newSel,oldYview=None):
        pass
        
    def setUndoTypes (self):
        pass
#@-node:ekr.20031218072017.2243:class nullUndoer
#@-others
#@nonl
#@-node:ekr.20031218072017.3603:@thin leoUndo.py
#@-leo
