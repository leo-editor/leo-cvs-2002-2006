#@+leo-ver=4-thin
#@+node:edream.110203113231.933:@thin mod_spelling.py
"""Spell Checker Plugin

- Performs spell checking on nodes within a Leo document.
- Uses aspell.exe to do the checking and suggest alternatives."""

#@@language python
#@@tabwidth -4

#@<< mod_spelling imports >>
#@+node:ekr.20040809111112:<< mod_spelling imports >>
import leoGlobals as g
import leoPlugins

import leoTkinterFind

Tk = g.importExtension('Tkinter',pluginName=__name__,verbose=True)

import ConfigParser
import os
import popen2
import re
import string
import sys
import traceback
#@nonl
#@-node:ekr.20040809111112:<< mod_spelling imports >>
#@nl

if Tk and not g.app.unitTesting: # Ok for unit testing, but doesn't work ;-)

    #@    @+others
    #@+node:edream.110203113231.934:Functions
    #@+node:edream.110203113231.935:createSpellMenu
    def createSpellMenu(tag,keywords):
        
        """Create the Check Spelling menu item in the Edit menu."""
        
        if g.app.unitTesting: return
        
        c = keywords.get("c")
    
        table = (
            ("-",None,None),
            ("Check Spelling","Alt+Shift+A",spellFrame.checkSpelling))
    
        c.frame.menu.createMenuItemsFromTable("Edit",table)
    #@nonl
    #@-node:edream.110203113231.935:createSpellMenu
    #@+node:edream.110203113231.936:onSelect
    def onSelect (tag,keywords):
        
        """A new vnode has just been selected.  Update the Spell Check window."""
        
        global spellFrame
        
        if g.app.unitTesting: return
    
        c = keywords.get("c")
        v = keywords.get("new_v")
    
        if g.top() and c and c.currentVnode():
            if c.currentVnode() != spellFrame.v:
                # print "onSelect",tag,`c.currentVnode()`,`spellFrame.v`
                spellFrame.update(show=False,fill=True)
            else:
                spellFrame.updateButtons()
    #@nonl
    #@-node:edream.110203113231.936:onSelect
    #@+node:edream.110203113231.937:onCommand
    def onCommand (tag,keywords):
        
        """Update the Spell Check window after any command that might change text."""
    
        global spellFrame
        
        if g.app.unitTesting: return
        
        if g.top() and g.top().currentVnode():
            
            # print "onCommand",tag
            spellFrame.update(show=False,fill=False)
    #@nonl
    #@-node:edream.110203113231.937:onCommand
    #@-node:edream.110203113231.934:Functions
    #@+node:edream.110203113231.938:class Aspell
    class Aspell:
        
        """A wrapper class for Aspell spell checker"""
        
        #@    @+others
        #@+node:edream.110203113231.939:Birth & death
        #@+node:edream.110203113231.940:__init__
        def __init__(self,local_dictionary_file,local_language_code):
            
            """Ctor for the Aspell class."""
            
            self.altre = re.compile(".\s(.+)\s(\d+)\s(\d+):(.*)")
            self.attached = None
            self.input,self.output = None,None
            self.signonGiven = False
            
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
        #@-node:edream.110203113231.940:__init__
        #@+node:edream.110203113231.941:getAspellDirectory
        def getAspellDirectory(self):
            
            """Get the directory containing aspell.exe from mod_spelling.ini"""
        
            try:
                fileName = os.path.join(g.app.loadDir,"../","plugins","mod_spelling.ini")
                config = ConfigParser.ConfigParser()
                config.read(fileName)
                return config.get("main","aspell_dir")
            except:
                g.es_exception()
                return None
        #@nonl
        #@-node:edream.110203113231.941:getAspellDirectory
        #@-node:edream.110203113231.939:Birth & death
        #@+node:edream.110203113231.942:openPipes
        def openPipes (self):
            
            """Open the pipes to aspell.exe"""
            
            if self.input or self.output:
                print "pipes already open!"
                self.closePipes()
            
            #@    << Ensure local dictionary is present >>
            #@+node:edream.110203113231.943:<< Ensure local dictionary is present >>
            add_dicts = ""
            
            if self.local_dictionary:
                if self.updateDictionary():
                    add_dicts = "--add-extra-dicts %s" % self.local_dictionary
            
            
            #@-node:edream.110203113231.943:<< Ensure local dictionary is present >>
            #@nl
            cmd = "%s pipe %s" % (self.aspell_exe_loc, add_dicts)
            if not self.local_dictionary:
                print "openPipes: command = " + cmd
            
            try:
                self.input, self.output = popen2.popen2(cmd)
            except:
                print "exception opening pipe"
                self.input = self.output = None
            
            if self.input:
                # g.trace(self.input)
                self.attached = self.input.readline()
            else:
                self.attached = None
                
            if not self.signonGiven:
                self.signonGiven = True
                if self.attached:
                    print self.attached
                    g.es(self.attached,color="blue")
                else:
                    print "can not open aspell"
                    g.es("can not open aspell",color="red")
        #@nonl
        #@-node:edream.110203113231.942:openPipes
        #@+node:edream.110203113231.944:closePipes
        def closePipes (self):
            
            """Close the pipes to aspell.exe"""
            
            # if self.input or self.output: print "closePipes"
            
            if self.input:
                self.input.close()
                self.input = None
        
            if self.output:
                self.output.close()
                self.output = None
        #@nonl
        #@-node:edream.110203113231.944:closePipes
        #@+node:edream.110203113231.945:listAlternates
        def listAlternates(self, aspell_return):
            
            """Return a list of alternates from aspell."""
            
            match = self.altre.match(aspell_return)
        
            if match:
                return [item.strip() for item in match.groups()[3].split(",")]
            else:
                return []
        #@nonl
        #@-node:edream.110203113231.945:listAlternates
        #@+node:edream.110203113231.946:processWord
        def processWord(self, word):
        
            """Pass a word to aspell and return the list of alternatives."""
            
            if not self.attached:
                return None
        
            # print "processWord",`word`,`self.output`
            
            self.output.write("%s\n" % word)
            
            ret,junk = self.input.readline(),self.input.readline()
        
            if ret == "*\n":
                return None
            else:
                return self.listAlternates(ret)
        #@nonl
        #@-node:edream.110203113231.946:processWord
        #@+node:edream.110203113231.947:updateDictionary
        def updateDictionary(self):
            
            """Update the aspell dictionary from a list of words.
            
            Return True if the dictionary was update correctly."""
        
            try:
                # Create master list
                basename = os.path.splitext(self.local_dictionary)[0]
                cmd = (
                    "%s --lang=%s create master %s.wl < %s.txt" %
                    (self.aspell_exe_loc,self.local_language_code,basename,basename))
                os.popen(cmd)
                return True
        
            except Exception, err:
                g.es("Unable to update local aspell dictionary: %s" % err)
                print err
                add_dicts = ""
                return False
        #@nonl
        #@-node:edream.110203113231.947:updateDictionary
        #@-others
    #@-node:edream.110203113231.938:class Aspell
    #@+node:edream.110203113231.948:class spellDialog
    class spellDialog (leoTkinterFind.leoTkinterFind):
        
        """A class to create and manage Leo's Spell Check dialog."""
        
        #@    @+others
        #@+node:edream.110203113231.949:Birth & death
        #@+node:edream.110203113231.950:spell.__init__
        def __init__ (self):
            
            """Ctor for the Leo Spelling dialog."""
            
            # Call the base ctor to create the dialog.
            leoTkinterFind.leoTkinterFind.__init__(self,"Leo Spell Checking",resizeable=False)
        
            self.local_dictionary_file = self.getLocalDictionary()
            self.local_language_code = self.getLocalLanguageCode("en")
            self.aspell = Aspell(self.local_dictionary_file,self.local_language_code)
            #@    << set self.dictionary >>
            #@+node:edream.110203113231.951:<< set self.dictionary >>
            if self.local_dictionary_file:
            
                self.dictionary = self.readLocalDictionary(self.local_dictionary_file)
                if self.dictionary:
                    # print "Local dictionary:", self.local_dictionary_file
                    g.es("Local dictionary: %s" % g.shortFileName(self.local_dictionary_file),color="blue")
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
            #@-node:edream.110203113231.951:<< set self.dictionary >>
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
        #@-node:edream.110203113231.950:spell.__init__
        #@+node:edream.110203113231.952:getLocalDictionary
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
        #@-node:edream.110203113231.952:getLocalDictionary
        #@+node:edream.110203113231.953:getLocalLanguageCode
        def getLocalLanguageCode(self,defaultLanguageCode):
            
            """Get the dictionaries containing words not in the standard dictionary from mod_spelling.ini"""
        
            try:
                fileName = os.path.join(g.app.loadDir,"../","plugins","mod_spelling.ini")
                config = ConfigParser.ConfigParser()
                config.read(fileName)
                return config.get("main","local_language_code",defaultLanguageCode)
            except:
                g.es_exception()
                return defaultLanguageCode
        #@nonl
        #@-node:edream.110203113231.953:getLocalLanguageCode
        #@+node:edream.110203113231.954:readLocalDictionary
        def readLocalDictionary (self,local_dictionary):
            
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
        #@-node:edream.110203113231.954:readLocalDictionary
        #@+node:edream.110703030027:destroySelf
        def destroySelf (self):
            
            self.top.destroy() # 11/7/03
        #@nonl
        #@-node:edream.110703030027:destroySelf
        #@-node:edream.110203113231.949:Birth & death
        #@+node:edream.110203113231.955:createFrame
        def createFrame (self):
            
            """Create the Spelling dialog."""
            
            # Create the find panel...
            outer = Tk.Frame(self.frame,relief="groove",bd=2)
            outer.pack(padx=2,pady=2,expand=1,fill="both")
        
            #@    << Create the text and suggestion panes >>
            #@+node:edream.110203113231.956:<< Create the text and suggestion panes >>
            f = outer
            
            f2 = Tk.Frame(f)
            f2.pack(expand=1,fill="x")
            self.wordLabel = Tk.Label(f2, text="Suggestions for:")
            self.wordLabel.pack(side="left")
            
            fpane = Tk.Frame(f,bd=2)
            fpane.pack(side="top", expand=1, fill="x")
            
            self.listBox = Tk.Listbox(fpane,height=30,selectmode="single")
            self.listBox.pack(side="left", expand=1, fill="both")
            
            listBoxBar = Tk.Scrollbar(fpane,name='listBoxBar')
            
            for bar,txt in ((listBoxBar,self.listBox),):
                txt['yscrollcommand'] = bar.set
                bar['command'] = txt.yview
                bar.pack(side="right", fill="y")
            #@-node:edream.110203113231.956:<< Create the text and suggestion panes >>
            #@nl
            #@    << Create the spelling buttons >>
            #@+node:edream.110203113231.957:<< Create the spelling buttons >>
            # Create the button panes
            buttons1  = Tk.Frame(outer,bd=1)
            buttons1.pack (anchor="n",expand=1,fill="x")
            
            buttons2  = Tk.Frame(outer,bd=1)
            buttons2.pack (anchor="n",expand=1,fill="none")
            
            buttonList = []
            for text,command in (
                ("Find",self.onFindButton),
                ("Change",self.onChangeButton),
                ("Change, Find",self.onChangeThenFindButton),
                ("Add",self.onAddButton)):
                width = max(6,len(text))
                b=Tk.Button(buttons1,width=width,text=text,command=command)
                b.pack(side="left",fill="none",expand=1)
                buttonList.append(b)
                    
            for text,command in (
                ("Undo",self.onUndoButton),
                ("Redo",self.onRedoButton),
                ("Ignore",self.onIgnoreButton),
                ("Hide",self.onHideButton)):
                width = max(6,len(text))
                b=Tk.Button(buttons2,width=width,text=text,command=command)
                b.pack(side="left",fill="none",expand=0)
                buttonList.append(b)
            
            # We need these to enable or disable buttons.
            (self.findButton, self.changeButton,
             self.changeFindButton, self.addButton, 
             self.undoButton, self.redoButton,
             self.ignoreButton, self.hideButton) = buttonList
            #@nonl
            #@-node:edream.110203113231.957:<< Create the spelling buttons >>
            #@nl
        #@-node:edream.110203113231.955:createFrame
        #@+node:edream.110203113231.958:Buttons
        #@+node:edream.110203113231.959:onAddButton
        def onAddButton (self):
            
            """Handle a click in the Add button in the Check Spelling dialog."""
        
            self.add()
            self.closePipes()
        
        #@-node:edream.110203113231.959:onAddButton
        #@+node:edream.110203113231.960:onIgnoreButton
        def onIgnoreButton (self):
        
            """Handle a click in the Ignore button in the Check Spelling dialog."""
        
            self.ignore()
            self.closePipes()
        #@nonl
        #@-node:edream.110203113231.960:onIgnoreButton
        #@+node:edream.110203113231.961:onChangeButton & onChangeThenFindButton
        def onChangeButton (self):
            
            """Handle a click in the Change button in the Check Spelling dialog."""
        
            self.change()
            self.closePipes()
            self.updateButtons()
            
        # Event needed for double-click event.
        def onChangeThenFindButton (self,event=None): 
                
            """Handle a click in the "Change, Find" button in the Check Spelling dialog."""
        
            if self.change():
                self.find()
            self.closePipes()
            self.updateButtons()
        #@nonl
        #@-node:edream.110203113231.961:onChangeButton & onChangeThenFindButton
        #@+node:edream.110203113231.962:onFindButton
        def onFindButton (self):
            
            """Handle a click in the Find button in the Check Spelling dialog."""
        
            self.find()
            self.updateButtons()
            self.closePipes()
        #@nonl
        #@-node:edream.110203113231.962:onFindButton
        #@+node:edream.110203113231.963:onHideButton
        def onHideButton (self):
            
            """Handle a click in the Hide button in the Check Spelling dialog."""
        
            self.closePipes()
            self.top.withdraw()
        #@-node:edream.110203113231.963:onHideButton
        #@+node:edream.110203113231.964:onRedoButton & onUndoButton
        def onRedoButton (self):
            
            """Handle a click in the Redo button in the Check Spelling dialog."""
        
            self.c.undoer.redo() # Not a command, so command hook doesn't fire.
            self.update(show=False,fill=False)
            self.c.frame.body.bodyCtrl.focus_force()
            
        def onUndoButton (self):
            
            """Handle a click in the Undo button in the Check Spelling dialog."""
        
            self.c.undoer.undo() # Not a command, so command hook doesn't fire.
            self.update(show=False,fill=False)
            self.c.frame.body.bodyCtrl.focus_force()
        #@nonl
        #@-node:edream.110203113231.964:onRedoButton & onUndoButton
        #@-node:edream.110203113231.958:Buttons
        #@+node:edream.110203113231.965:Commands
        #@+node:edream.110203113231.966:add
        def add (self):
        
            """Add the selected suggestion to the dictionary."""
            
            if not self.local_dictionary_file:
                return
            
            try:
                f = None
                try:
                    # Rewrite the dictionary in alphabetical order.
                    f = open(self.local_dictionary_file,"r")
                    words = f.readlines()
                    f.close()
                    words = [word.strip() for word in words]
                    words.append(self.currentWord)
                    words.sort()
                    f = open(self.local_dictionary_file,"w")
                    for word in words:
                        f.write("%s\n" % word)
                    f.flush()
                    f.close()
                    g.es("Adding ",color="blue",newline=False) ; g.es('%s' % self.currentWord)
                except IOError:
                    g.es("Can not add %s to dictionary" % self.currentWord,color="red")
            finally:
                if f: f.close()
                
            self.dictionary[self.currentWord.lower()] = 0
            
            # Restart aspell so that it re-reads its dictionary.
            self.aspell.closePipes()
            self.aspell.openPipes()
            
            self.onFindButton()
        #@nonl
        #@-node:edream.110203113231.966:add
        #@+node:edream.110203113231.967:change
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
        #@-node:edream.110203113231.967:change
        #@+node:edream.110203113231.968:checkSpelling
        def checkSpelling (self,event=None):
            
            """Open the Check Spelling dialog."""
        
            self.bringToFront()
            self.update(show=True,fill=False)
        #@nonl
        #@-node:edream.110203113231.968:checkSpelling
        #@+node:edream.110203113231.969:find
        def find(self):
            
            """Find the next unknown word."""
            
            # Reload the work pane from the present node.
            s = self.body.bodyCtrl.get("1.0","end").rstrip()
            self.workCtrl.delete("1.0","end")
            self.workCtrl.insert("end",s)
            
            # Reset the insertion point of the work widget.
            ins = self.body.bodyCtrl.index("insert")
            self.workCtrl.mark_set("insert",ins)
        
            alts,word = self.findNextMisspelledWord()
            self.currentWord = word # Need to remember this for 'add' and 'ignore'
            
            if alts:
                self.fillbox(alts,word)
                self.body.bodyCtrl.focus_set()
                            
                # Copy the working selection range to the body pane
                start,end = g.app.gui.getTextSelection(self.workCtrl)
                g.app.gui.setTextSelection(self.body.bodyCtrl,start,end)
            else:
                g.es("no more misspellings")
                self.fillbox([])
        #@nonl
        #@-node:edream.110203113231.969:find
        #@+node:edream.110203113231.970:ignore
        def ignore (self):
            
            """Ignore the incorrect word for the duration of this spell check session."""
            
            g.es("Ignoring ",color="blue",newline=False) ; g.es('%s' % self.currentWord)
            self.dictionary[self.currentWord.lower()] = 0
            self.onFindButton()
        #@nonl
        #@-node:edream.110203113231.970:ignore
        #@-node:edream.110203113231.965:Commands
        #@+node:edream.110203113231.971:Helpers
        #@+node:ekr.20041226080101:bringToFront
        def bringToFront (self):
            
            if self.top:
                self.top.deiconify()
                self.top.lift()
        #@nonl
        #@-node:ekr.20041226080101:bringToFront
        #@+node:edream.110203113231.972:closePipes
        def closePipes(self):
            
            self.aspell.closePipes()
        #@nonl
        #@-node:edream.110203113231.972:closePipes
        #@+node:edream.110203113231.973:fillbox
        def fillbox(self,alts,word=None):
        
            """Update the suggestions listbox in the Check Spelling dialog."""
            
            self.suggestions = alts
            
            if not word:
                word = ""
        
            self.wordLabel.configure(text = "Suggestions for: " + word)
            self.listBox.delete(0,"end")
        
            for i in xrange(len(self.suggestions)):
                self.listBox.insert(i,self.suggestions[i])
            
            if len(self.suggestions):
                self.listBox.select_set(1) # This doesn't show up because we don't have focus.
        #@nonl
        #@-node:edream.110203113231.973:fillbox
        #@+node:edream.110203113231.974:findNextMisspelledWord
        def findNextMisspelledWord(self):
            
            """Find the next unknown word."""
            
            aspell = self.aspell ; alts = None ; word = None
            c = self.c ; v = self.v
            try:
                aspell.openPipes()
                try:
                    while 1:
                        v,word = self.findNextWord(v) 
                        if not v or not word:
                            alts = None
                            break
                        #@                << Skip word if ignored or in local dictionary >>
                        #@+node:edream.110203113231.975:<< Skip word if ignored or in local dictionary >>
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
                        #@-node:edream.110203113231.975:<< Skip word if ignored or in local dictionary >>
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
                aspell.closePipes()
                return alts, word
        #@nonl
        #@-node:edream.110203113231.974:findNextMisspelledWord
        #@+node:edream.110203113231.976:findNextWord
        def findNextWord (self,v):
            
            """Scan for the next word, leaving the result in the work widget"""
        
            t = self.workCtrl
            word_start = string.letters + '_'
            t.mark_set("insert","insert wordend + 1c")
            while 1:
                # print `t.index("insert")`,`t.index("end-1c")`
                if t.compare("insert",">=","end - 1c"):
                    v = v.threadNext()
                    if not v: return None,None
                    t.delete("1.0","end")
                    t.insert("end",v.bodyString())
                    t.mark_set("insert","1.0")
                elif t.compare("insert",">=","insert lineend - 1c"):
                    t.mark_set("insert","insert lineend + 1line")
                else:
                    ch = t.get("insert")
                    if ch in word_start:
                        word = t.get("insert wordstart","insert wordend")
                        g.app.gui.setTextSelection(t,"insert wordstart","insert wordend")
                        # print "findNextWord:",`word`
                        return v,word
                    elif ch:
                        t.mark_set("insert","insert + 1c")
        #@nonl
        #@-node:edream.110203113231.976:findNextWord
        #@+node:edream.110203113231.977:getSuggestion
        def getSuggestion (self):
            
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
        #@-node:edream.110203113231.977:getSuggestion
        #@+node:edream.110203113231.978:onMap
        def onMap (self,event=None):
            
            """Respond to a Tk <Map> event."""
            
            self.update(show=False,fill=False)
        #@nonl
        #@-node:edream.110203113231.978:onMap
        #@+node:edream.110203113231.979:onSelectListBox
        def onSelectListBox (self,event=None):
            
            """Respond to a click in the selection listBox."""
            
            self.updateButtons()
            self.body.bodyCtrl.focus_set()
        #@-node:edream.110203113231.979:onSelectListBox
        #@+node:edream.110203113231.980:update
        def update (self,show=True,fill=False):
            
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
                self.bringToFront()
                # Don't interfere with Edit Headline commands.
                self.body.bodyCtrl.focus_set()
                
            # Give the signon if it hasn't been given yet.
            if not self.aspell.signonGiven:
                self.aspell.openPipes()
                self.aspell.closePipes()
        #@nonl
        #@-node:edream.110203113231.980:update
        #@+node:edream.110203113231.981:updateButtons
        def updateButtons (self):
            
            """Enable or disable buttons in the Check Spelling dialog."""
            
            start,end = g.app.gui.getTextSelection(self.body.bodyCtrl)
            state = g.choose(self.suggestions and start,"normal","disabled")
            
            self.changeButton.configure(state=state)
            self.changeFindButton.configure(state=state)
        
            state = g.choose(self.c.undoer.canRedo(),"normal","disabled")
            self.redoButton.configure(state=state)
            
            state = g.choose(self.c.undoer.canUndo(),"normal","disabled")
            self.undoButton.configure(state=state)
            
            state = g.choose(self.local_dictionary_file,"normal","disabled")
            self.addButton.configure(state=state)
        
            self.ignoreButton.configure(state="normal")
        #@nonl
        #@-node:edream.110203113231.981:updateButtons
        #@-node:edream.110203113231.971:Helpers
        #@-others
    #@nonl
    #@-node:edream.110203113231.948:class spellDialog
    #@-others

    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":

        spellFrame = spellDialog()
        spellFrame.top.withdraw()
        g.app.globalWindows.append(spellFrame)
        
        leoPlugins.registerHandler("create-optional-menus",createSpellMenu)
        leoPlugins.registerHandler("select2",onSelect)
        leoPlugins.registerHandler("command2",onCommand) # For any command that might change the text.
        leoPlugins.registerHandler("bodykey2",onSelect) # For updating buttons.
        leoPlugins.registerHandler(("bodyclick2","bodydclick2","bodyrclick2"),onSelect) # These affect selection.
        
        __version__ = "0.4.0" # EKR: 11/12/03: modified to use new leoTkinterFind class.
        g.plugin_signon(__name__)
#@nonl
#@-node:edream.110203113231.933:@thin mod_spelling.py
#@-leo
