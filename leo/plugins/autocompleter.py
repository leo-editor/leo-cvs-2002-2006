#@+leo-ver=4-thin
#@+node:ekr.20041017043622:@thin autocompleter.py
"""
autocompletion and calltips plugin.  Special characters:

'.' summons the autocompletion.
'(' summons the calltips
Escape closes either box.
Ctrl selects an item.
alt-up_arrow, alt-down_arrow moves up or down in the list.

This plugin scans the complete outline at startup if autocompletion is enabled.

You many enable or disable features in autocomplete.ini.
"""

#@@language python 
#@@tabwidth -4

#@<<imports>>
#@+node:ekr.20041017043622.26:<< imports >>
import leoGlobals as g 
import leoPlugins 
import leoTkinterFrame 

import leoColor 
import ConfigParser 
import os.path  

import re 
import sets 
import string 
import threading 

try:
    import Pmw 
except ImportError:
    Pmw = g.cantImport("Pmw",__name__)

try:
    import Tkinter as Tk 
except ImportError:
    Tk = g.cantImport("Tk",__name__)
    
try:
    import weakref 
except ImportError:
    weakref = g.cantImport("weakref",__name__)
#@nonl
#@-node:ekr.20041017043622.26:<< imports >>
#@nl
__version__ = ".55"
#@<<version history>>
#@+node:ekr.20041017102904:<<version history>>
#@+at
# .425:
#     -The initial scan thread is now a daemon thread.
#     -Creates autocompleter box and Calltip box once.
#     -Broke long functions apart.
#     -'Esc'now closes autobox and calltip.
# .500 EKR:
#     - Made minor changes based on .425:
#     -Improved docstring.
#     -Converted to 4.2style.
# .501 EKR:
#     - Changed select method following patch by original author.
#     - Added event.keysym=='Up' case to
# .55 Lu:
#      - Made the watcher def more greedy.  See def for rationale
#      - Made the calltip identification regex more liberal.
#      - streamlined some code.
#      - added DictSet class, experimental in the sense that I haven't had a 
# bug with it yet.
#        see <<DictSet>> node, under << globals>>
#      - discovered dependency between this and Chapters, auto needs to be 
# loaded first
#@-at
#@nonl
#@-node:ekr.20041017102904:<<version history>>
#@nl
#@<<load notes>>
#@+node:mork.20041020122041:<<load notes>>
#@+at 
# Autocompleter needs to be loaded before Chapters/chapters or the autobox and 
# the calltip label do
# not appear in the correct place.
# 
#@-at
#@@c 
#@nonl
#@-node:mork.20041020122041:<<load notes>>
#@nl
useauto = 1
usecall = 1
#@<<globals>>
#@+node:ekr.20041017100522:<< globals >>
orig_CreateControl = leoTkinterFrame.leoTkinterBody.createControl 

#@<<DictSet>>
#@+node:mork.20041020141804:<<DictSet>>
class DictSet( dict ):
    '''A dictionary that always returns either a fresh sets.Set or one that has been stored from a previous call.
    a different datatype can be used by setting the factory keyword in __init__ to a different class.  This is an experimental
    class but worth the attempt as it gets rid of some ugly code.'''
    
    def __init__( self , factory = sets.Set ):
        dict.__init__( self )
        self.factory = factory
        
    def __getitem__( self, key ):
        try:
            return dict.__getitem__( self, key )
        except:
            dict.__setitem__( self, key, self.factory() )
            return dict.__getitem__( self, key )
   
#@-node:mork.20041020141804:<<DictSet>>
#@nl
#watchwords ={} switched to DictSet
watchwords = DictSet()
#calltips ={} switched to DictSet
calltips = DictSet( factory = DictSet)
pats ={}
lang = None 

haveseen = weakref.WeakKeyDictionary()
autoboxes = weakref.WeakKeyDictionary()
clabels = weakref.WeakKeyDictionary()
#@nonl
#@-node:ekr.20041017100522:<< globals >>
#@nl
#@<<patterns>>
#@+node:ekr.20041017043622.2:<< patterns >>
#This section defines patterns for calltip recognition.  Autocompleter does not use regexes.
space = r'[ \t\r\f\v ]+'
end = r'\w+\s*\([^)]*\)'

pats['python'] = re.compile(r'def\s+'+end)

pats['java'] = re.compile(
    r'((public\s+|private\s+|protected\s+)?(static'+space+'|\w+'+space+'){1,2}'+end+')')
    
pats['perl'] = re.compile(r'sub\s+'+end)

pats['c++'] = re.compile(r'((virtual\s+)?\w+'+space+end+')')

pats['c'] = re.compile(r'\w+'+space+end)

r = string.punctuation.replace('(','').replace('.','')
pt = string.digits+string.letters+r 

ripout = string.punctuation+string.whitespace+'\n'
ripout = ripout.replace('_','')

okchars ={}
for z in string.ascii_letters:
    okchars[z] = z 
okchars['_'] = '_'
#@nonl
#@-node:ekr.20041017043622.2:<< patterns >>
#@nl

#@+others
#@+node:ekr.20041017043622.3:watcher
watchitems = ( '.',')' )
txt_template = '%s%s%s'

def watcher (event):
    
    global lang 

    if event.char.isspace() or event.char in watchitems:
        bCtrl = event.widget
        # This if statement ensures that attributes set in another node
        # are put in the database.  Of course the user has to type a whitespace
        # to make sure it happens.  We try to be selective so that we don't burn
        # through the scanText def for every whitespace char entered.  This will
        # help when the nodes become big.
        if event.char.isspace():
            # Don't do anything if the previous char was a whitespace
            if bCtrl.get( 'insert -1c' ).isspace():
                return 
            if bCtrl.get( 'insert -1c wordstart -1c') != '.': return
            
        c = bCtrl.commander
        lang = c.frame.body.getColorizer().language 
        txt = txt_template % (
            bCtrl.get( "1.0", Tk.INSERT ), 
            event.char, 
            bCtrl.get( Tk.INSERT, "end" )) #We have to add the newest char, its not in the bCtrl yet

        scanText(txt)
#@nonl
#@-node:ekr.20041017043622.3:watcher
#@+node:ekr.20041017043622.4:scanText
def scanText (txt):
    
    # This function guides what gets scanned.

    if useauto:
        scanForAutoCompleter(txt)

    if usecall:
        scanForCallTip(txt)
#@-node:ekr.20041017043622.4:scanText
#@+node:ekr.20041017043622.5:scanForAutoCompleter
def scanForAutoCompleter (txt):

    # This function scans text for the autocompleter database.
    t1 = txt.split('.')
    g =[]
    reduce(lambda a,b:makeAutocompletionList(a,b,g),t1)
    if g:
        for a, b in g:
            #if watchwords.has_key(a):
            #    watchwords[a].add(b)
            #else:
            #    watchwords[a] = sets.Set([b])
            watchwords[ a ].add( b )
                # Use the experimental DictSet class here,
#@nonl
#@-node:ekr.20041017043622.5:scanForAutoCompleter
#@+node:ekr.20041017043622.6:scanForCallTip
def scanForCallTip (txt):

    #this function scans text for calltip info
    pat2 = pats['python']
    if lang!=None:
        if pats.has_key(lang):
            pat2 = pats[lang]
    g2 = pat2.findall(txt)
    if g2:
        for z in g2:
            if isinstance(z,tuple):
                z = z[0]
            pieces2 = z.split('(')
            pieces2[0] = pieces2[0].split()[-1]
            a, b = pieces2[0], pieces2[1]
            calltips[ lang ][ a ].add( z )
                # Use the experimental DictSet here
#@nonl
#@-node:ekr.20041017043622.6:scanForCallTip
#@+node:ekr.20041017043622.7:makeAutocompletionList
def makeAutocompletionList (a,b,glist):

    a1 = _reverseFindWhitespace(a)
    if a1:
        b2 = _getCleanString(b)
        if b2!='':
            glist.append((a1,b2))
    return b 
#@-node:ekr.20041017043622.7:makeAutocompletionList
#@+node:ekr.20041017043622.8:_getCleanString
def _getCleanString (s):

    '''a helper for autocompletion scanning'''
    if s.isalpha():return s 

    for n, l in enumerate(s):
        if l in okchars:pass 
        else:return s[:n]
    return s 
#@-node:ekr.20041017043622.8:_getCleanString
#@+node:ekr.20041017043622.9:_reverseFindWhitespace
def _reverseFindWhitespace (s):

    '''A helper for autocompletion scan'''
    for n, l in enumerate(s):
        n =(n+1)*-1
        if s[n].isspace()or s[n]=='.':return s[n+1:]
    return s 
#@-node:ekr.20041017043622.9:_reverseFindWhitespace
#@+node:ekr.20041017043622.10:initialScan
def initialScan (tag,keywords):
    
    c = keywords.get("c")or keywords.get("new_c")
    if haveseen.has_key(c):
        return 

    haveseen[c] = None 

    def scan ():
        pth = os.path.split(g.app.loadDir)   
        aini = pth[0]+r"/plugins/autocompleter.ini"
        if os.path.exists(aini):
            readConfigFile(aini)
        bankpath = pth[0]+r"/plugins/autocompleter/"
        readLanguageFiles(bankpath)
        readOutline(c)
    
    # Use a thread to do the initial scan so as not to interfere with the user.            
    t = threading.Thread(target=scan)
    t.setDaemon(True)
    t.start()
#@-node:ekr.20041017043622.10:initialScan
#@+node:ekr.20041017043622.11:readConfigFile
def readConfigFile (aini):

    global usecall, useauto, pat 
    #reads the autocompleter config file in.
    cp = ConfigParser.ConfigParser()
    cp.read(aini)
    ac = None 
    for z in cp.sections():
        if z.strip()=='autocompleter':
            ac = z 
            continue 
        ipats = r''+cp.get(z,'pat').strip()
        z = z.strip()
        pats[z] = re.compile(ipats)
        if cp.has_section(ac):
            if cp.has_option(ac,'useauto'):
                useauto = int(cp.get(ac,'useauto'))
            if cp.has_option(ac,'usecalltips'):
                usecall = int(cp.get(ac,'usecalltips'))
            if cp.has_option(ac,'autopattern'):
                pat = re.compile(cp.get(ac,'autopattern'))
#@-node:ekr.20041017043622.11:readConfigFile
#@+node:ekr.20041017043622.12:readLanguageFiles
def readLanguageFiles (bankpath):
    global lang 
    #reads language files in directory specified by bankpath
    for z in pats:
        bpath = bankpath+z+'.ato'
        if os.path.exists(bpath):
            f = open(bpath)
            lang = z 
            map( scanText, f )
            #for x in f:
            #    scanText(x)
            f.close()
#@nonl
#@-node:ekr.20041017043622.12:readLanguageFiles
#@+node:ekr.20041017043622.13:readOutline
def readOutline (c):
    global lang 
    #This method walks the Outline(s) and builds the database from which
    #autocompleter draws its autocompletion options
    #c is a commander in this case
    if 'Chapters'in g.app.loadedPlugins:
        import chapters 
        it = chapters.walkChapters()
        for x in it:
            lang = None 
            setLanguage(x)
            scanText(x.bodyString())
    else:
        for z in c.rootPosition().allNodes_iter():
            setLanguage( z )
            scanText( z.bodyString() )
#@nonl
#@-node:ekr.20041017043622.13:readOutline
#@+node:ekr.20041017043622.14:reducer
def reducer (lis,pat):

    return[x for x in lis if x.startswith(pat)]
#@-node:ekr.20041017043622.14:reducer
#@+node:ekr.20041017043622.15:unbind
def unbind (canvas):

    canvas.on = False
    map( canvas.unbind, ( "<Control_L>", "<Control_R>", "<Alt-Up>", "<Alt-Down>", "<Alt_L>" , "<Alt_R>" ) )
#@-node:ekr.20041017043622.15:unbind
#@+node:ekr.20041017043622.16:moveSelItem
def moveSelItem (event,c):
    #c in this def is not a commander but a Tk Canvas
    i = c.sl.curselection()
    if len(i)==0:
        return None 
    i = int(i[0])
    # g.trace(event.keysym,i)
    try:
        if event.keysym=='Down':
            if c.sl.size()-1>c.sl.index(i):
                i += 1
            elif i!=0:
                i -1
        elif event.keysym=='Up': # EKR.
            if i > 0:
                i -= 1
    finally:
        c.sl.select_clear(0,'end')
        c.sl.select_set(i)
        c.sl.see(i)
        return "break"
#@-node:ekr.20041017043622.16:moveSelItem
#@+node:ekr.20041017043622.17:select
def select (event,c,body):
    #c in this def is not a commander but a Tk Canvas
    if not c.on:return None #nothing on, might as well return
    if event.keysym=="??":
        return None 
    if event.keysym=='Escape':
        #turn everything off
        c.delete(c.i)
        unbind( c )
        return None 
    if c.which and event.keysym in('parenright','Control_L','Control_R'):
        c.delete(c.i)
        c.on = False 
    elif event.keysym in("Shift_L","Shift_R"):
        #so the user can use capital letters.
        return None 
    elif not c.which and event.char in ripout:
        c.delete(c.i)
        unbind( c )
    if c.which==1:
        #no need to add text if its calltip time.
        return None 
    ind = body.index('insert-1c wordstart')
    pat = body.get(ind,'insert')+event.char 
    pat = pat.lstrip('.')
    ww = list(c.sl.get(0,'end'))
    lis = reducer(ww,pat)
    if len(lis)==0:return None 
    i = ww.index(lis[0])
    c.sl.select_clear(0,'end')
    c.sl.select_set(i)
    c.sl.see(i)
#@nonl
#@-node:ekr.20041017043622.17:select
#@+node:ekr.20041017043622.18:remove
def remove (event,c,body,scrllistbx):
    
    #c in this def is not a commander but a Tk Canvas
    if event.keysym in("Alt_L","Alt_R"):
        return None 

    c.delete(c.i)
    a = scrllistbx.getvalue()
    if len(a)==0:return None 
    try:
        a = a[0]
        ind = body.index('insert-1c wordstart')
        pat = body.get(ind,'insert')
        pat = pat.lstrip('.')

        if a.startswith(pat):a = a[len(pat):]
        body.insert('insert',a)
        body.event_generate("<Key>")
        body.update_idletasks()
    finally:
        unbind( c )
#@-node:ekr.20041017043622.18:remove
#@+node:ekr.20041017043622.19:add_item
def add_item (event,c,body,colorizer):
    #c in this def is not a commander but a Tk Canvas
    if not event.char in('.','(')or c.on:return None 
    txt = body.get('insert linestart','insert')
    txt = _reverseFindWhitespace(txt)
    if event.char!='('and not watchwords.has_key(txt):
         return None 

    if event.char=='.':
        c.on = True 
        ww = list(watchwords[txt])
        ww.sort()
        # f is a Frame, b is the AutoBox
        f, b = getAutoBox(c,ww)
        calculatePlace(body,c.sl,c,f)
        c.sl.select_set(0)
        c.which = 0 #indicates its in autocompletion mode
        add_bindings( c, body, b )
        return
    elif event.char=='(':
        language = colorizer.language 
        if calltips.has_key(language):
            if calltips[language].has_key(txt):
                c.on = True 
                ct = getCtipLabel(c)
                s = list(calltips[language][txt])
                t = '\n'.join(s)
                ct.configure(text=t)
                calculatePlace(body,ct,c,ct)
                c.which = 1 #indicates its in calltip mode
        else:
            c.on = False 
            return None 
#@-node:ekr.20041017043622.19:add_item
#@+node:mork.20041020110810:add_bindings
def add_bindings( c, body, b ):
                
    event = Tk.Event()
    event.keysym = ''
    rmv = lambda event = event , c = c, body = body, scrllistbx = b : remove( event, c, body, scrllistbx )
    b.configure( selectioncommand = rmv )
    msi = lambda event, c = c :moveSelItem( event, c )
    bindings = ( ( "<Control_L>", rmv ), ( "<Control_R>", rmv ),
                 ( "<Alt-Up>", msi ), ( "<Alt-Down>", msi ),
                 ( "<Alt_L>", rmv ), ( "<Alt_R>", rmv ) )
    map( lambda b: c.bind( *b ) , bindings )
#@-node:mork.20041020110810:add_bindings
#@+node:ekr.20041017043622.20:getAutoBox
def getAutoBox (c,ww):
    # a factory method that returns either a new box or one that was created previously
    #c in this case is a canvas not a commander
    if autoboxes.has_key(c):
        f = autoboxes[c]
        configureAutoBox(f.b,ww)
        return f, f.b 
    f = Tk.Frame(c)
    f.b = b = Pmw.ScrolledListBox(f,hscrollmode='none',
                listbox_selectbackground='#FFE7C6',
                listbox_selectforeground='blue',
                listbox_background='white',
                listbox_foreground='blue',
                vertscrollbar_background='#FFE7C6',
                vertscrollbar_width=10)
    c.sl = b.component('listbox')
    b.pack()
    autoboxes[c] = f 
    configureAutoBox(b,ww)
    return f, b 
#@-node:ekr.20041017043622.20:getAutoBox
#@+node:ekr.20041017043622.21:configureAutoBox
def configureAutoBox (sl,ww):

    #sets data and size of autobox
    sl.setlist(ww)
    lb = sl.component('listbox')
    height = len(ww)
    if height>5:height = 5
    lb.configure(height=height)
#@-node:ekr.20041017043622.21:configureAutoBox
#@+node:ekr.20041017043622.22:getCtipLabel
def getCtipLabel (c):
    #c in this case is a canvas not a commander.
    #this def is a factory of Tk Labels for a canvas, saves the
    #plugin from generating a new one each time a calltip is needed.
    if clabels.has_key(c):
        ct = clabels[c]
        return ct 
    ct = Tk.Label(c,background='lightyellow',
    foreground='black')
    clabels[c] = ct 
    return ct  
#@nonl
#@-node:ekr.20041017043622.22:getCtipLabel
#@+node:ekr.20041017043622.23:calculatePlace
def calculatePlace (body,cwidg,c,f):
    #c in this def is not a commander but a Tk Canvas
    try:
        x, y, lww, lwh = body.bbox('insert -1c')
        x, y = x+lww, y+lwh 
    except:
         x = 1
         y = 1
    rwidth = cwidg.winfo_reqwidth()
    rheight = cwidg.winfo_reqheight()
    if body.winfo_width()<x+rwidth:  
        x = x-rwidth 
    if y>body.winfo_height()/2:
        h2 = rheight 
        h3 = h2+lwh 
        y = y-h3 
    c.i = c.create_window(x,y,window=f,anchor='nw')
#@-node:ekr.20041017043622.23:calculatePlace
#@+node:ekr.20041017043622.24:setLanguage
def setLanguage (vnd):
    global lang 
    while vnd:
        xs1 = vnd.bodyString()
        dict = g.get_directives_dict(xs1)
        if dict.has_key('language'):
            lang = g.set_language(xs1,dict['language'])[0]
            break 
        vnd = vnd.parent()
#@-node:ekr.20041017043622.24:setLanguage
#@+node:ekr.20041017043622.25:newCreateControl
def newCreateControl (self,frame,parentFrame):
    
    #creating background
    c = Tk.Canvas(parentFrame,background='white')
    c.pack(expand=1,fill='both')
    f = Tk.Frame(c)
    c.create_window(0,0,window=f,anchor='nw')
    f.pack_configure(fill='both',expand=1)
    #finished createing background
    
    body = orig_CreateControl(self,frame,f)
    body.commander = self.c
    c.on = False 
    
    sel = lambda event, c = c, body = body:select(event,c,body)
    ai = lambda event, c = c, body = body, colorizer = frame.body:add_item(
        event,c,body,colorizer.getColorizer())
    for z in ( watcher, sel, ai ):
        c.bind( "<Key>", z, '+' )
    #set the bindtags for the body, protects the autocompleter from other plugins unbinding events.
    ctags = [ c.bindtags()[ 0 ] , ]
    btags = body.bindtags()
    ctags.extend( btags ) 
    body.bindtags( tuple( ctags ))
    return body  
#@nonl
#@-node:ekr.20041017043622.25:newCreateControl
#@+node:ekr.20041017105122.2:onOpenWindow
def onOpenWindow ():
    
    c = keywords.get("c") or keywords.get("new_c")

    if haveseen.has_key(c):
        return 
        
    autocompleter = autocomplet(c)
#@nonl
#@-node:ekr.20041017105122.2:onOpenWindow
#@-others

if Pmw and Tk and weakref:

    leoTkinterFrame.leoTkinterBody.createControl = newCreateControl 
    leoPlugins.registerHandler(('start2','open2'),initialScan)
   
    g.plugin_signon(__name__)
#@nonl
#@-node:ekr.20041017043622:@thin autocompleter.py
#@-leo
