#@+leo-ver=4-thin
#@+node:edream.110403140857.8:@thin color_markup.py
#@<< docstring >>
#@+node:ekr.20050912182434:<< docstring >>
'''Handle coloring for markup in doc parts and Python triple-double-quoted strings.
This plugin requires that the ``add_directives`` plugin is enabled.

To color a text using this plugin, the text must be in the range of an ``@markup wiki`` directive.

The currently supported markups are:

''text''                   # write text in italics
__text__                   # write text in bold
~~<color>:text~~           # write text in the color specified by <color> (e.g. blue, grey, etc)
{picture file=<filename>}  # load the picture indicated by <filename>
http://url                 # URL support: double clicking on the url will open it in the default browser.
https://url                # URL support: double clicking on the url will open it in the default browser.

-   Note 1: italics and bold markups can be nested, e.g.

        ''__text__''               # write text in italics and bold

    Just remember to terminate the tags in the order they were opened.

- Note 2: URLs must be terminated by a space.

By default, once the text has been markup up, the actual tags (e.g. __ for bold) are not displayed anymore. You can choose to display them selecting "Show Invisibles" from the Edit menu.
'''
#@nonl
#@-node:ekr.20050912182434:<< docstring >>
#@nl

#@@language python
#@@tabwidth -4

#@<< imports >>
#@+node:ekr.20050101090207.3:<< imports >>
import leoGlobals as g
import leoPlugins
import tkFileDialog

Tk =             g.importExtension('Tkinter',       pluginName=__name__,verbose=True)
tkColorChooser = g.importExtension('tkColorChooser',pluginName=__name__,verbose=True)

import os
import string  # zfill does not exist in Python 2.2.1
#@nonl
#@-node:ekr.20050101090207.3:<< imports >>
#@nl

__version__ = "1.6"
#@<< version history >>
#@+node:ekr.20050311104330:<< version history >>
#@@nocolor
#@+at
# 
# Initial version DS: 10/29/03.
# EKR: 11/4/03: mods for 4.1.
# 
# 1.5 EKR:
# - Use only 'new' and 'open2' hooks.
# - imported tkColorChooser.
# 1.6 EKR:
# - Removed call to g.top.
# - Used positions and p args instead of vnodes and v args.
# - Added to docs: text to be colored must be in range of ``@markup wiki`` 
# kdirective
#@-at
#@nonl
#@-node:ekr.20050311104330:<< version history >>
#@nl

#@+others
#@+node:ekr.20060108112937:Module-level
#@+node:ekr.20050311104330.1:init
def init ():
    
    ok = Tk and tkColorChooser # Ok for unit tests.
    
    if ok: 
        if g.app.gui is None:
            g.app.createTkGui(__file__)
    
        if g.app.gui.guiName() == "tkinter":
            print "wiki markup enabled"

            # default value for color-tagged wiki text
            global wikiColoredText
            wikiColoredText = "blue"
            leoPlugins.registerHandler("color-optional-markup", colorWikiMarkup)
            leoPlugins.registerHandler("init-color-markup", initAnyMarkup)
            #leoPlugins.registerHandler("bodykey1", onBodykey1)
            leoPlugins.registerHandler("bodydclick1", onBodydclick1)
            leoPlugins.registerHandler(('new','open2'), onCreate)
            g.plugin_signon(__name__)

    return ok
#@nonl
#@-node:ekr.20050311104330.1:init
#@+node:edream.110403140857.9:initAnyMarkup
def initAnyMarkup (tag,keywords):
    
    """initialize colorer.markup_string
    
    The colorer completely recolors the body pane when this changes"""
    
    keys = ("colorer","v")
    colorer,v = [keywords.get(key) for key in keys]

    c = colorer.c
    if not c or not c.exists or not v: return

    # underline means hyperlinks
    c.frame.body.tag_configure("http",underline=1) # EKR: 11/4/03
    c.frame.body.tag_configure("https",underline=1) # EKR: 11/4/03
    dict = g.scanDirectives(c,p=v) # v arg is essential.
    pluginsList = dict.get("pluginsList")
    
    if pluginsList:
        for d,v,s,k in pluginsList:
            if d == "markup":
                kind = s[k:]
                if kind:
                    colorer.markup_string = kind
                    return
                    
    colorer.markup_string = "unknown" # default
#@nonl
#@-node:edream.110403140857.9:initAnyMarkup
#@+node:edream.110403140857.16:onBodykey1 (not ready)
def onBodykey1(tag,keywords):

    c = keywords.get("c")
    body = c.frame.body
    idx = body.bodyCtrl.index("insert")
    line,char = map(int, idx.split('.'))
    elideRange = body.bodyCtrl.tag_prevrange("elide", idx) # EKR: 11/4/03
    if elideRange:
        elideLine,elideStart = map(int, elideRange[0].split('.'))
        elideLine,elideEnd   = map(int, elideRange[1].split('.'))
        if line==elideLine and elideStart<char<=elideEnd:
            pass
            # print "XXX: tag!"
            # body.bodyCtrl.mark_set("insert", "elide+1c")
    return 0 # do not override
#@-node:edream.110403140857.16:onBodykey1 (not ready)
#@+node:edream.110403140857.17:onBodydclick1 & allies
def onBodydclick1(tag,keywords):

    """Handle double clicks on a hyperlink."""

    c = keywords.get("c")
    url = getUrl(c, "http", "https")
    if url:
        try:
            import webbrowser
            webbrowser.open(url)
        except:
            g.es("exception opening " + url)
            g.es_exception()
#@+node:edream.110403140857.18:getUrl
def getUrl(c, *tags):
    """See if the current text belongs to a hyperlink tag and, if so, return the url."""
    
    body = c.frame.body
    selStart,selEnd = body.getTextSelection() # EKR: 11/4/03
    for tag in tags:
        hyperlink = body.bodyCtrl.tag_prevrange(tag,selEnd) # EKR: 11/4/03
        if hyperlink:
            hyperStart,hyperEnd = hyperlink
            if selStart==selEnd: 
                # kludge: only react on single chars, not on selections
                if body.bodyCtrl.compare(hyperStart,"<=",selStart) and body.bodyCtrl.compare(selStart,"<=",hyperEnd):
                    url = body.bodyCtrl.get(hyperStart,hyperEnd)
                    return url
    return None
#@nonl
#@-node:edream.110403140857.18:getUrl
#@-node:edream.110403140857.17:onBodydclick1 & allies
#@+node:edream.110403140857.20:onCreate
def onCreate (tag,keywords):

    """Create menu entries under Edit->Edit Body to insert wiki tags."""

    c = keywords.get('c')
    if not c: return

    editBodyMenuName = "Edit Body..."
    wikiMenuName = "&Wiki Tags..."
    if c.frame.menu.getMenu(wikiMenuName):
        return # wiki menu already created

    editBodyMenu = c.frame.menu.getMenu(editBodyMenuName)
    separator = (("-",None,None),)
    c.frame.menu.createMenuEntries(editBodyMenu,separator)

    wikiMenu = c.frame.menu.createNewMenu(wikiMenuName,editBodyMenuName)
    #@    << define menu callbacks >>
    #@+node:ekr.20060108113303:<< define menu callbacks >>
    def doWikiBoldCallback (event,c=c):
        doWikiBold(c)
    
    def doWikiItalicCallback (event,c=c):
        doWikiItalic(c)
    
    def doWikiPictureCallback (event,c=c):
        doWikiPicture(c)
    
    def doWikiColorCallback (event,c=c):
        doWikiColor(c)
    
    def doWikiChooseColorCallback (event,c=c):
        doWikiChooseColor(c)
    #@nonl
    #@-node:ekr.20060108113303:<< define menu callbacks >>
    #@nl
    
    newEntries = (
        ("&Bold","Alt+Shift+B",doWikiBoldCallback),
        ("&Italic","Alt+Shift+I",doWikiItalicCallback),
        #("Insert Pict&ure...", "Alt+Shift+U", doWikiPictureCallback),
        ("C&olor","Alt+Shift+O",doWikiColorCallback),
        ("Choose Co&lor...","Alt+Shift+L",doWikiChooseColorCallback),
    )

    c.frame.menu.createMenuEntries(wikiMenu,newEntries,dynamicMenu=True)
#@nonl
#@-node:edream.110403140857.20:onCreate
#@+node:edream.110403140857.10:colorWikiMarkup & helper
def colorWikiMarkup (tag,keywords):

    keys = ("colorer","v","s","i","j","colortag")
    colorer,v,s,i,j,colortag = [keywords.get(key) for key in keys]
    c = colorer.c
    dict = g.scanDirectives(c,p=v) # v arg is essential.
    pluginsList = dict.get("pluginsList")
    
    if pluginsList:
        for d,v,s2,k in pluginsList:
            if d == "markup":
                if g.match_word(s2,k,"wiki"):
                    doWikiText(colorer,v,s,i,j,colortag)
                    return True # We have colored the text.
            
    return None # We have not colored the text.
#@nonl
#@+node:edream.110403140857.11:doWikiText
def doWikiText (colorer,v,s,i,end,colortag):

    firsti = i ; inserted = 0

    while i < end:
        #@        << set first to a tuple describing the first tag to be handled >>
        #@+node:edream.110403140857.12:<< set first to a tuple describing the first tag to be handled >>
        first = None
        
        for tag,delim1,delim2 in (
            ("bold","__","__"),
            ("italic","''","''"),
            ("picture","{picture file=","}"),
            ("color","~~","~~"),
            ("http","http://"," "),
            ("https","https://"," ")):
            n1 = s.find(delim1,i,end)
            if n1 > -1:
                n2 = s.find(delim2,n1+len(delim1),end)
                if n2 > -1:
                    if not first or (first and n1 < first[1]):
                        first = tag,n1,n2,delim1,delim2
        #@-node:edream.110403140857.12:<< set first to a tuple describing the first tag to be handled >>
        #@nl
        if first:
            tag,n1,n2,delim1,delim2 = first
            i = n2 + len(delim2)
            #@            << handle the tag using n1,n2,delim1,delim2 >>
            #@+node:edream.110403140857.13:<< handle the tag using n1,n2,delim1,delim2 >>
            if tag =="picture":
                colorer.tag("elide",n1,n2+len(delim2)) # Elide everything.
                filename = s[n1+len(delim1):n2]
                filename = os.path.join(g.app.loadDir,filename)
                filename = os.path.normpath(filename)
                inserted += insertWikiPicture(colorer,filename,n2+len(delim2))
            elif tag == "color":
                #@    << parse and handle color field >>
                #@+node:edream.110403140857.14:<< parse and handle color field >>
                # Parse the color value.
                j = n1+len(delim1)
                n = s.find(":",j,n2)
                if n2 > n > j > -1:
                    name = s[j:n]
                    if name[0] == '#' and len(name) > 1:
                        name = '#' + string.zfill(name[1:],6)
                    if name in colorer.color_tags_list:
                        colorer.tag("elide",n1,n+1)
                        colorer.tag(name,n+1,n2)
                        colorer.tag("elide",n2,n2+len(delim2))
                    else:
                        try:
                            # print "entering", name
                            colorer.body.bodyCtrl.tag_configure(name,foreground=name)
                            colorer.color_tags_list.append(name)
                            colorer.tag("elide",n1,n+1)
                            colorer.tag(name,n+1,n2)
                            colorer.tag("elide",n2,n2+len(delim2))
                        except: # an invalid color name: elide nothing.
                            pass # g.es_exception()
                #@nonl
                #@-node:edream.110403140857.14:<< parse and handle color field >>
                #@nl
            elif tag == "http" or tag == "https":
                colorer.tag(tag,n1,n2)
            else:
                # look for nested bold or italic.
                if tag == "bold":
                    delim3,delim4 = "''","''" # Look for nested italic.
                else:
                    delim3,delim4 = "__","__" # Look for nested bold.
                n3 = s.find(delim3,n1+len(delim1),n2) ; n4 = -1
                if n3 > -1:
                    n4 = s.find(delim4,n3+len(delim3),n2+len(delim2))
                if n3 > -1 and n4 > -1:
                    colorer.tag("elide",n1,n1+len(delim1))
                    colorer.tag("elide",n2,n2+len(delim2))
                    colorer.tag("elide",n3,n3+len(delim3))
                    colorer.tag("elide",n4,n4+len(delim4))
                    colorer.tag(tag,n1+len(delim1),n3)
                    colorer.tag("bolditalic",n3+len(delim3),n4)
                    colorer.tag(tag,n4+len(delim4),n2)
                else:
                    # No nested tag.
                    colorer.tag("elide",n1,n1+len(delim1))
                    colorer.tag("elide",n2,n2+len(delim2))
                    colorer.tag(tag,n1+len(delim1),n2)
            #@nonl
            #@-node:edream.110403140857.13:<< handle the tag using n1,n2,delim1,delim2 >>
            #@nl
        else: i = end
        
    colorer.tag(colortag,firsti,end+inserted)
#@nonl
#@-node:edream.110403140857.11:doWikiText
#@-node:edream.110403140857.10:colorWikiMarkup & helper
#@+node:edream.110403140857.15:insertWikiPicture
def insertWikiPicture (colorer,filename,i):
    
    """Try to insert a picture with the give filename.
    
    Returns the number of characters actually inserted"""

    if colorer.color_pass == 0:
        colorer.redoColoring = True # schedule a two-pass recoloring.
        return 0

    if colorer.color_pass == 2:
        return 0 # The second redo pass.

    if not os.path.exists(filename):
        return 0

    try:
        # Create the image
        photo = Tk.PhotoImage(master=g.app.root, file=filename)
        image = colorer.body.bodyCtrl.image_create(colorer.index(i),image=photo,padx=0)
        
        # Keep references so images stay on the canvas.
        colorer.image_references.append((photo,image,colorer.line_index,i),)
        return 1
    except:
        g.es_exception()
        return 0
#@nonl
#@-node:edream.110403140857.15:insertWikiPicture
#@-node:ekr.20060108112937:Module-level
#@+node:edream.110403140857.19:Menu commands
#@+node:edream.110403140857.21:doWikiBold
def doWikiBold(c):
    
    insertWikiMarkup(c,"__","__")
#@nonl
#@-node:edream.110403140857.21:doWikiBold
#@+node:edream.110403140857.22:doWikiItalic
def doWikiItalic(c):

    insertWikiMarkup(c,"''","''")
#@nonl
#@-node:edream.110403140857.22:doWikiItalic
#@+node:edream.110403140857.23:doWikiColor
def doWikiColor(c):
    
    global wikiColoredText
    
    insertWikiMarkup(c,"~~%s:" % wikiColoredText,"~~")
#@nonl
#@-node:edream.110403140857.23:doWikiColor
#@+node:edream.110403140857.24:doWikiChooseColor
def doWikiChooseColor(c):
    
    global wikiColoredText
    
    if c and c.exists:
        rgb,val = tkColorChooser.askcolor(color=wikiColoredText)
        if val:
            wikiColoredText = val
            doWikiColor()
#@nonl
#@-node:edream.110403140857.24:doWikiChooseColor
#@+node:edream.110403140857.25:doWikiPicture (not ready)
def doWikiPicture(c):
    
    if c and c.exists:
        name = tkFileDialog.askopenfilename(
            title="Insert Picture",
            filetypes=[("All files", "*")],
        )
        if name:
            insertWikiMarkup(c,"{picture file=%s}" % name,"")
#@nonl
#@-node:edream.110403140857.25:doWikiPicture (not ready)
#@+node:edream.110403140857.26:insertWikiMarkup
def insertWikiMarkup(c,leftTag,rightTag):
    
    if not c or not c.exists: return
    
    body = c.frame.body
    oldSel = body.bodyCtrl.tag_ranges("sel")
    if oldSel:
        #@        << apply markup to selection >>
        #@+node:edream.110403140857.27:<< apply markup to selection >>
        start,end = oldSel
        body.bodyCtrl.insert(start, leftTag)
        # we need to review where the selection now ends
        start,end = body.bodyCtrl.tag_ranges("sel")
        body.bodyCtrl.insert(end, rightTag)
        g.app.gui.setTextSelection(body.bodyCtrl, start + "-" + `len(leftTag)`  + "c",
                                 end + "+" + `len(rightTag)` + "c")
        newSel = body.getTextSelection()
        c.frame.onBodyChanged("Change",oldSel=oldSel)
        #@-node:edream.110403140857.27:<< apply markup to selection >>
        #@nl
    else:
        #@        << handle no selection >>
        #@+node:edream.110403140857.28:<< handle no selection >>
        # Note: this does not currently handle mixed nested tags,
        # e.g. <b><i>text</b></i>. One should always close the
        # tags in the order they were opened, as in <b><i>text</i></b>.
        oldSel = body.getTextSelection() # EKR: 11/04/03
        nextChars = body.bodyCtrl.get(oldSel[0], "%s+%dc" % (oldSel[0],len(rightTag)))
        if nextChars == rightTag:
            # if the next chars are the right tag, just move beyond it
            newPos = "%s+%dc" % (oldSel[0],len(rightTag))
        else:
            # insert a pair of tags and set cursor between the tags
            body.bodyCtrl.insert("insert", leftTag)
            body.bodyCtrl.insert("insert", rightTag)
            newPos = "%s+%dc" % (oldSel[0],len(leftTag))
        body.setTextSelection(newPos, newPos)
        newSel = body.getTextSelection()
        c.frame.onBodyChanged("Typing",oldSel=oldSel)
        #@-node:edream.110403140857.28:<< handle no selection >>
        #@nl

    body.focus_set()
#@nonl
#@-node:edream.110403140857.26:insertWikiMarkup
#@-node:edream.110403140857.19:Menu commands
#@-others
#@nonl
#@-node:edream.110403140857.8:@thin color_markup.py
#@-leo
