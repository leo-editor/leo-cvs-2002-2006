# -*- coding: utf-8 -*-
#@+leo-ver=4
#@+node:@file spellpyx.py
#@@first

"""Spell Checker Plugin.

- Perfoms spell checking on nodes within a Leo document.
- Uses aspell.exe to do the checking and suggest alternatives.

Written by Paul Paterson and 'e'.
"""

#@@language python
#@@tabwidth -4

visibleInitially = True # True: open spell dialog initially.

# Specify the path to the top-level Aspell directory.
# This directory should contain aspell.pyd.
# Change this path in setup.py if you recompile the pyd.
aspell_dir = r'c:/Aspell'

#@<< spellpx imports >>
#@+node:<< spellpx imports >>
import leoGlobals as g
import leoPlugins
import leoTkinterFind

try:
    import Tkinter as Tk
except ImportError:
    Tk = None
    s = "Can not import Tk"
    print s ; g.es(s,color="blue")

aspell = g.importFromPath("aspell",aspell_dir,verbose=False)
if not aspell:
    s = "Can not import aspell from %s" % aspell_dir
    print s ; g.es(s,color="blue")
    
import ConfigParser
import os
import re
import string
import sys
import traceback
#@nonl
#@-node:<< spellpx imports >>
#@nl

if Tk and aspell and not g.app.unitTesting:

    # print "spellpy loaded",aspell

    #@    @+others
    #@+node:Functions
    #@+node:createSpellMenu
    def createSpellMenu(tag, keywords):
    
        """Create the Check Spelling menu item in the Edit menu."""
        
        if g.app.unitTesting: return
        
        c = keywords.get("c")
    
        table = (
            ("-", None, None),
            ("Check Spelling", "Alt+Shift+A", spellFrame.checkSpelling))
    
        c.frame.menu.createMenuItemsFromTable("Edit", table)
    #@nonl
    #@-node:createSpellMenu
    #@+node:onSelect
    def onSelect(tag, keywords):
        
        """A new vnode has just been selected.  Update the Spell Check window."""
        
        if g.app.unitTesting: return
    
        c = keywords.get("c")
        v = keywords.get("new_v")
        global spellFrame
        
        if g.top() and c and c.currentVnode():
            if c.currentVnode() != spellFrame.v:
                # print "onSelect",tag,`c.currentVnode()`,`spellFrame.v`
                spellFrame.update(show= False, fill= True)
            else:
                spellFrame.updateButtons()
    #@nonl
    #@-node:onSelect
    #@+node:onCommand
    def onCommand(tag, keywords):
        """Update the Spell Check window after any command that might change text."""
    
        global spellFrame
        
        if g.app.unitTesting: return
        
        if g.top() and g.top().currentVnode():
            
            # print "onCommand", tag
            spellFrame.update(show= False, fill= False)
    #@nonl
    #@-node:onCommand
    #@-node:Functions
    #@+node:class Aspell
    class Aspell:
        """A wrapper class for Aspell spell checker"""
        
        #@    @+others
        #@+node:Birth & death
        #@+node:__init__
        def __init__(self,aspell,local_dictionary_file,local_language_code):
            
            """Ctor for the Aspell class."""
        
            self.sc = aspell.spell_checker(prefix= aspell_dir)
            
            self.aspell_exe_loc = self.getAspellDirectory()
            self.local_language_code = local_language_code
            
            if local_dictionary_file:
                self.local_dictionary_file = local_dictionary_file
                self.local_dictionary = "%s.wl" % os.path.splitext(local_dictionary_file)[0]
            else:
                print "failed to set aspell.local_dictionary"
                self.local.dictionary_file = None
                self.local_dictionary = None
        #@nonl
        #@-node:__init__
        #@+node:getAspellDirectory
        def getAspellDirectory(self):
        
            """Get the directory containing aspell.exe from mod_spelling.ini"""
        
            try:
                fileName = os.path.join(
                        g.app.loadDir, "../", "plugins", "mod_spelling.ini")
                config = ConfigParser.ConfigParser()
                config.read(fileName)
                return config.get("main", "aspell_dir")
            except:
                g.es_exception()
                return None
        #@nonl
        #@-node:getAspellDirectory
        #@-node:Birth & death
        #@+node:processWord
        def processWord(self, word):
            """Pass a word to aspell and return the list of alternatives.
            OK: 
            * 
            Suggestions: 
            & «original» «count» «offset»: «miss», «miss», ... 
            None: 
            # «original» «offset» 
            simplifyed to not create the string then make a list from it    
            """
            
            # print "processWord",`word`
            #ret = "*\n"
            retl = None
        
            if not self.sc.check(word):
                retl = self.sc.suggest(word)
                #if not retl:
                #    ret = "& %s %d 0: %s\n"%(word, len(retl), ','.join(retl))
        
            # print "processWord ret", `retl`  #`ret`
            #the pipe was returning a coma delimited string
        
            #why make a string then reprocess to strip it back out?
            #if ret == "*\n": return None
            return retl #self.listAlternates(ret)  
        #@nonl
        #@-node:processWord
        #@+node:updateDictionary
        def updateDictionary(self):
        
            """Update the aspell dictionary from a list of words.
            
            Return True if the dictionary was update correctly."""
        
            try:
                # Create master list
                basename = os.path.splitext(self.local_dictionary)[0]
                cmd = (
                    "%s --lang=%s create master %s.wl < %s.txt" %
                    (self.aspell_exe_loc, self.local_language_code, basename,basename))
                os.popen(cmd)
                return True
        
            except Exception, err:
                g.es("Unable to update local aspell dictionary: %s" % err)
                print err
                add_dicts = ""
                return False
        #@nonl
        #@-node:updateDictionary
        #@-others
    #@-node:class Aspell
    #@+node:class spellDialog (leoTkinterFind)
    class spellDialog(leoTkinterFind.leoTkinterFind):
    
        """A class to create and manage Leo's Spell Check dialog."""
        
        #@    @+others
        #@+node:Birth & death
        #@+node:spellDialog.__init__
        def __init__(self,aspell):
            """Ctor for the Leo Spelling dialog."""
        
            # Call the base ctor to create the dialog.
            leoTkinterFind.leoTkinterFind.__init__(self,
                "Leo Spell Checking", resizeable= False)
        
            self.local_dictionary_file = self.getLocalDictionary()
            self.local_language_code = self.getLocalLanguageCode("en")
            self.aspell = Aspell(aspell,self.local_dictionary_file,self.local_language_code)
            #@    << set self.dictionary >>
            #@+node:<< set self.dictionary >>
            if self.local_dictionary_file:
            
                self.dictionary = self.readLocalDictionary(self.local_dictionary_file)
                if self.dictionary:
                    g.es("Aspell local dictionary: %s" % \
                        g.shortFileName(self.local_dictionary_file), color="blue")
                    if 0:
                        keys = self.dictionary.keys()
                        keys.sort()
                        print "local dict:", keys
                else:
                    self.dictionary = {}
                    self.local_dictionary_file = None
            else:
                self.dictionary = {}
            #@nonl
            #@-node:<< set self.dictionary >>
            #@nl
            
            self.fillbox([])
            
            # State variables.
            self.currentWord = None
            self.suggestions = []
            self.c = None
            self.v = None
            self.body = None
            self.workCtrl = Tk.Text(None) # A text widget for scanning.
        
            self.listBox.bind("<Double-Button-1>",self.onChangeThenFindButton)
            self.listBox.bind("<Button-1>",self.onSelectListBox)
            self.listBox.bind("<Map>",self.onMap)
        #@nonl
        #@-node:spellDialog.__init__
        #@+node:getLocalDictionary
        def getLocalDictionary(self):
            
            """Get the dictionaries containing words not in the standard dictionary from mod_spelling.ini"""
        
            try:
                fileName = os.path.join(g.app.loadDir,"../","plugins","mod_spelling.ini")
                config = ConfigParser.ConfigParser()
                config.read(fileName)
                return config.get("main","local_leo_dictionary",None)
            except:
                g.es_exception()
                return None
        #@nonl
        #@-node:getLocalDictionary
        #@+node:getLocalLanguageCode
        def getLocalLanguageCode(self, defaultLanguageCode):
            """Get the dictionaries containing words not in the standard dictionary from mod_spelling.ini"""
        
            try:
                fileName = os.path.join(g.app.loadDir,"../","plugins","mod_spelling.ini")
                config = ConfigParser.ConfigParser()
                config.read(fileName)
                return config.get("main", "local_language_code", defaultLanguageCode)
            except:
                g.es_exception()
                return defaultLanguageCode
        #@nonl
        #@-node:getLocalLanguageCode
        #@+node:readLocalDictionary
        def readLocalDictionary(self, local_dictionary):
            """Read the dictionary of words which we use as a local dictionary
            
            Although Aspell itself has the functionality to handle this kind of things
            we duplicate it here so that we can also use it for the "ignore" functionality
            and so that in future a Python only solution could be developed."""
        
            try:
                f = open(local_dictionary,"r")
            except IOError:
                g.es("Unable to open local dictionary '%s' - using a blank one instead" % local_dictionary)
                return None
            
            try:
                # Create the dictionary - there are better ways to do this
                # in later Python's but we stick with this method for compatibility
                dct = {}
                for word in f.readlines():
                    dct[word.strip().lower()] = 0
            finally:
                f.close()
        
            return dct
        #@nonl
        #@-node:readLocalDictionary
        #@+node:destroySelf
        def destroySelf (self):
            
            self.top.destroy() # 11/7/03
        #@nonl
        #@-node:destroySelf
        #@-node:Birth & death
        #@+node:createFrame
        def createFrame(self):
            """Create the Spelling dialog."""
            
            # Create the find panel...
            outer = Tk.Frame(self.frame, relief= "groove", bd= 2)
            outer.pack({'padx':2, 'pady':2, 'expand':1, 'fill':'both', })
            
            #@    << Create the text and suggestion panes >>
            #@+node:<< Create the text and suggestion panes >>
            f = outer
            
            f2 = Tk.Frame(f)
            f2.pack({'expand':1, 'fill':'x', })
            self.wordLabel = Tk.Label(f2, text="Suggestions for:")
            self.wordLabel.pack({'side':'left', })
            self.wordLabel.configure(font=('verdana', 10, 'bold'))
            
            fpane = Tk.Frame(f, bd= 2)
            fpane.pack({'side':'top', 'expand':1, 'fill':'x', })
            
            self.listBox = Tk.Listbox(fpane, height= 16, width= 20, selectmode= "single")
            self.listBox.pack({'side':'left', 'expand':1, 'fill':'both', })
            
            self.listBox.configure(font=('verdana', 11, 'normal'))
            
            listBoxBar = Tk.Scrollbar(fpane, name= 'listBoxBar')
            
            for bar,txt in ((listBoxBar, self.listBox),):
                txt['yscrollcommand'] = bar.set
                bar['command'] = txt.yview
                bar.pack({'side':'right', 'fill':'y', })
            #@-node:<< Create the text and suggestion panes >>
            #@nl
            #@    << Create the spelling buttons >>
            #@+node:<< Create the spelling buttons >>
            # Create the button panes
            buttons1  = Tk.Frame(outer,bd=1)
            buttons1.pack ({'anchor':'n', 'expand':1, 'fill':'x', })
            
            buttons2  = Tk.Frame(outer,bd=1)
            buttons2.pack ({'anchor':'n', 'expand':1, 'fill':'none', })
            
            buttonList = []
            for text,command in (
                ("Find",self.onFindButton),
                ("Change",self.onChangeButton),
                ("Change, Find",self.onChangeThenFindButton),
                ("Add",self.onAddButton)):
                font = ('verdana', 9, 'normal')
                width = max(6,len(text)-1)
                b=Tk.Button(
                    buttons1, font= font, width= width, text= text, command= command)
                b.pack({'side':'left', 'fill':'none', 'expand':1, })
            
                buttonList.append(b)
                    
            for text,command in (
                ("Undo",self.onUndoButton),
                ("Redo",self.onRedoButton),
                ("Ignore",self.onIgnoreButton),
                ("Hide",self.onHideButton)):
                font = ('verdana', 9, 'normal')
                width = max(6,len(text)-1)
                b=Tk.Button(
                    buttons2, font= font, width= width, text= text, command= command)
                b.pack({'side':'left', 'fill':'none', 'expand':0, })
                buttonList.append(b)
            
            # We need these to enable or disable buttons.
            (self.findButton, self.changeButton,
             self.changeFindButton, self.addButton, 
             self.undoButton, self.redoButton,
             self.ignoreButton, self.hideButton) = buttonList
            #@nonl
            #@-node:<< Create the spelling buttons >>
            #@nl
        
            #fix if the user hits exit button, don't want to destroy forever
            self.frame.master.protocol("WM_CLOSE", self.onHideButton)
            self.frame.master.protocol("WM_DELETE_WINDOW", self.onHideButton)
        #@-node:createFrame
        #@+node:Buttons
        #@+node:onAddButton
        def onAddButton(self):
            """Handle a click in the Add button in the Check Spelling dialog."""
        
            self.add()
            #self.closePipes()
        
        #@-node:onAddButton
        #@+node:onIgnoreButton
        def onIgnoreButton(self):
            """Handle a click in the Ignore button in the Check Spelling dialog."""
        
            self.ignore()
            #self.closePipes()
        #@nonl
        #@-node:onIgnoreButton
        #@+node:onChangeButton & onChangeThenFindButton
        def onChangeButton(self):
            """Handle a click in the Change button in the Check Spelling dialog."""
        
            self.change()
            #self.closePipes()
            self.updateButtons()
            
        # Event needed for double-click event.
        def onChangeThenFindButton(self,event=None): 
            """Handle a click in the "Change, Find" button in the Check Spelling dialog."""
        
            if self.change():
                self.find()
            #self.closePipes()
            self.updateButtons()
        #@nonl
        #@-node:onChangeButton & onChangeThenFindButton
        #@+node:onFindButton
        def onFindButton(self):
            """Handle a click in the Find button in the Check Spelling dialog."""
        
            self.find()
            self.updateButtons()
            #self.closePipes()
        #@nonl
        #@-node:onFindButton
        #@+node:onHideButton
        def onHideButton(self):
            """Handle a click in the Hide button in the Check Spelling dialog."""
        
            #self.closePipes()
            self.top.withdraw()
        #@-node:onHideButton
        #@+node:onRedoButton & onUndoButton
        def onRedoButton(self):
            """Handle a click in the Redo button in the Check Spelling dialog."""
        
            self.c.undoer.redo() # Not a command, so command hook doesn't fire.
            self.update(show= False, fill= False)
            self.c.frame.body.bodyCtrl.focus_force()
            
        def onUndoButton(self):
            """Handle a click in the Undo button in the Check Spelling dialog."""
        
            self.c.undoer.undo() # Not a command, so command hook doesn't fire.
            self.update(show= False, fill= False)
            self.c.frame.body.bodyCtrl.focus_force()
        #@nonl
        #@-node:onRedoButton & onUndoButton
        #@-node:Buttons
        #@+node:Commands
        #@+node:add
        def add(self):
            """Add the selected suggestion to the dictionary."""
            
            if not self.local_dictionary_file:
                return
            
            try:
                f = None
                try:
                    # Rewrite the dictionary in alphabetical order.
                    f = open(self.local_dictionary_file, "r")
                    words = f.readlines()
                    f.close()
                    words = [word.strip() for word in words]
                    words.append(self.currentWord)
                    words.sort()
                    f = open(self.local_dictionary_file, "w")
                    for word in words:
                        f.write("%s\n" % word)
                    f.flush()
                    f.close()
                    g.es("Adding ", color= "blue", newline= False) 
                    g.es('%s' % self.currentWord)
                except IOError:
                    g.es("Can not add %s to dictionary" % self.currentWord, color="red")
            finally:
                if f: f.close()
                
            self.dictionary[self.currentWord.lower()] = 0
            
            # Restart aspell so that it re-reads its dictionary.
            #why? since we are checking local words ourself anyway
            #self.aspell.closePipes()
            #self.aspell.openPipes()
            
            self.onFindButton()
        #@nonl
        #@-node:add
        #@+node:change
        def change(self):
            """Make the selected change to the text"""
        
            c = self.c ; v = self.v ; body = self.body ; t = body.bodyCtrl
            
            selection = self.getSuggestion()
            if selection:
                start,end = oldSel = g.app.gui.getTextSelection(t)
                if start:
                    if t.compare(start, ">", end):
                        start,end = end,start
                    t.delete(start,end)
                    t.insert(start,selection)
                    g.app.gui.setTextSelection(t,start,start + "+%dc" % (len(selection)))
                    newSel = g.app.gui.getTextSelection(t)
        
                    # update node, undo status, dirty flag, changed mark & recolor
                    c.beginUpdate()
                    c.frame.body.onBodyChanged(v,"Change",oldSel=oldSel,newSel=newSel)
                    c.endUpdate(True)
                    t.focus_set()
                    return True
        
            # The focus must never leave the body pane.
            t.focus_set()
            return False
        #@nonl
        #@-node:change
        #@+node:checkSpelling
        def checkSpelling(self,event=None):
            """Open the Check Spelling dialog."""
        
            self.top.deiconify()
            self.top.lift()
            self.update(show= True, fill= False)
        #@nonl
        #@-node:checkSpelling
        #@+node:find
        def find(self):
            """Find the next unknown word."""
            
            # Reload the work pane from the present node.
            s = self.body.bodyCtrl.get("1.0", "end").rstrip()
            self.workCtrl.delete("1.0", "end")
            self.workCtrl.insert("end", s)
            
            # Reset the insertion point of the work widget.
            ins = self.body.bodyCtrl.index("insert")
            self.workCtrl.mark_set("insert", ins)
        
            alts, word = self.findNextMisspelledWord()
            self.currentWord = word # Need to remember this for 'add' and 'ignore'
            
            if alts:
                self.fillbox(alts, word)
                self.body.bodyCtrl.focus_set()
                            
                # Copy the working selection range to the body pane
                start, end = g.app.gui.getTextSelection(self.workCtrl)
                g.app.gui.setTextSelection(self.body.bodyCtrl, start, end)
                #fix selection getting hidden in not visable section of body
                self.body.bodyCtrl.see(start)
            else:
                g.es("no more misspellings")
                self.fillbox([])
        #@nonl
        #@-node:find
        #@+node:ignore
        def ignore(self):
            """Ignore the incorrect word for the duration of this spell check session."""
            
            g.es("Ignoring ", color= "blue", newline= False)
            g.es('%s' % self.currentWord)
        
            self.dictionary[self.currentWord.lower()] = 0
            self.onFindButton()
        #@nonl
        #@-node:ignore
        #@-node:Commands
        #@+node:Helpers
        #@+node:fillbox
        def fillbox(self, alts, word=None):
            """Update the suggestions listbox in the Check Spelling dialog."""
            
            self.suggestions = alts
            
            if not word:
                word = ""
        
            self.wordLabel.configure(text= "Suggestions for: " + word)
            self.listBox.delete(0, "end")
        
            for i in xrange(len(self.suggestions)):
                self.listBox.insert(i, self.suggestions[i])
            
            # This doesn't show up because we don't have focus.
            if len(self.suggestions):
                self.listBox.select_set(1) 
        
        #@-node:fillbox
        #@+node:findNextMisspelledWord
        def findNextMisspelledWord(self):
            """Find the next unknown word."""
            
            aspell = self.aspell ; alts = None ; word = None
            c = self.c ; v = self.v
            try:
                #aspell.openPipes()
                try:
                    while 1:
                        v, word = self.findNextWord(v) 
                        if not v or not word:
                            alts = None
                            break
                        #@                << Skip word if ignored or in local dictionary >>
                        #@+node:<< Skip word if ignored or in local dictionary >>
                        #@+at 
                        #@nonl
                        # We don't bother to call apell if the word is in our 
                        # dictionary. The dictionary contains both locally 
                        # 'allowed' words and 'ignored' words. We put the test 
                        # before aspell rather than after aspell because the 
                        # cost of checking aspell is higher than the cost of 
                        # checking our local dictionary. For small local 
                        # dictionaries this is probably not True and this code 
                        # could easily be located after the aspell call
                        #@-at
                        #@@c
                        
                        if self.dictionary.has_key(word.lower()):
                            
                            # print "Ignored", word
                            continue
                            
                        # print "Didn't ignore '%s'" % word
                        #@nonl
                        #@-node:<< Skip word if ignored or in local dictionary >>
                        #@nl
                        alts = aspell.processWord(word)
                        if alts:
                            self.v = v
                            c.beginUpdate()
                            c.frame.tree.expandAllAncestors(v)
                            c.selectVnode(v)
                            c.endUpdate()
                            break
                except:
                    g.es_exception()
            finally:
                #aspell.closePipes()
                return alts, word
        #@nonl
        #@-node:findNextMisspelledWord
        #@+node:findNextWord
        def findNextWord(self, v):
            """Scan for the next word, leaving the result in the work widget"""
        
            t = self.workCtrl
            word_start = string.letters + '_'
            t.mark_set("insert", "insert wordend + 1c")
            while 1:
                # print `t.index("insert")`, `t.index("end-1c")`
                if t.compare("insert",">=", "end - 1c"):
                    v = v.threadNext()
                    if not v: return None,None
                    t.delete("1.0", "end")
                    t.insert("end", v.bodyString())
                    t.mark_set("insert", "1.0")
                elif t.compare("insert",">=", "insert lineend - 1c"):
                    t.mark_set("insert", "insert lineend + 1line")
                else:
                    ch = t.get("insert")
                    if ch in word_start:
                        word = t.get("insert wordstart", "insert wordend")
                        g.app.gui.setTextSelection(
                                    t, "insert wordstart", "insert wordend")
                        # print "findNextWord:",`word`
                        return v, word
                    elif ch:
                        t.mark_set("insert", "insert + 1c")
        #@nonl
        #@-node:findNextWord
        #@+node:getSuggestion
        def getSuggestion(self):
            """Return the selected suggestion from the listBox."""
            
            # Work around an old Python bug.  Convert strings to ints.
            items = self.listBox.curselection()
            try:
                items = map(int, items)
            except ValueError: pass
        
            if items:
                n = items[0]
                suggestion = self.suggestions[n]
                return suggestion
            else:
                return None
        #@nonl
        #@-node:getSuggestion
        #@+node:onMap
        def onMap (self, event=None):
            """Respond to a Tk <Map> event."""
            
            self.update(show= False, fill= False)
        #@nonl
        #@-node:onMap
        #@+node:onSelectListBox
        def onSelectListBox(self, event=None):
            """Respond to a click in the selection listBox."""
            
            self.updateButtons()
            self.body.bodyCtrl.focus_set()
        #@-node:onSelectListBox
        #@+node:update
        def update(self, show= True, fill= False):
            """Update the Spell Check dialog."""
            
            # print "update(show=%d,fill=%d)" % (show,fill)
            
            # Always assume that the user has changed text.
            self.c = c = g.top()
            self.v = c.currentVnode()
            self.body = c.frame.body
            if fill:
                self.fillbox([])
            self.updateButtons()
            if show:
                self.top.deiconify()
                # Don't interfere with Edit Headline commands.
                self.body.bodyCtrl.focus_set()
        #@-node:update
        #@+node:updateButtons
        def updateButtons(self):
            """Enable or disable buttons in the Check Spelling dialog."""
            
            start,end = g.app.gui.getTextSelection(self.body.bodyCtrl)
            state = g.choose(self.suggestions and start,"normal", "disabled")
            
            self.changeButton.configure(state= state)
            self.changeFindButton.configure(state= state)
        
            state = g.choose(self.c.undoer.canRedo(), "normal", "disabled")
            self.redoButton.configure(state= state)
            
            state = g.choose(self.c.undoer.canUndo(), "normal", "disabled")
            self.undoButton.configure(state= state)
            
            state = g.choose(self.local_dictionary_file, "normal", "disabled")
            self.addButton.configure(state= state)
        
            self.ignoreButton.configure(state= "normal")
        #@nonl
        #@-node:updateButtons
        #@-node:Helpers
        #@-others
    #@nonl
    #@-node:class spellDialog (leoTkinterFind)
    #@-others

    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":
        spellFrame = spellDialog(aspell)
        if not visibleInitially: spellFrame.top.withdraw()
        g.app.globalWindows.append(spellFrame)
        leoPlugins.registerHandler("create-optional-menus", createSpellMenu)
        leoPlugins.registerHandler("command2", onCommand) 
        leoPlugins.registerHandler(
                ("bodyclick2","bodydclick2","bodyrclick2","bodykey2","select2"),onSelect)
        
        __version__ = "0.5"
            # 0.4: EKR: Use the new leoTkinterFind class.
            # 0.4.1: e: Use Pyrex wrapper and aspell.pyd.
                # No longer uses pipes: much faster and more reliable.
                # Uses the existing mod_spelling.ini and txt local word list.
            # 0.5: EKR: Various minor mods, including support for unit testing.
        g.plugin_signon(__name__)
#@nonl
#@-node:@file spellpyx.py
#@-leo
