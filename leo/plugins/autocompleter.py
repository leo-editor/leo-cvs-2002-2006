#@+leo-ver=4-thin
#@+node:ekr.20040722104914:@thin autocompleter.py
"""Autocompletion plugin"""

#@@language python 
#@@tabwidth-4

#@<<autocompleter imports>>
#@+node:ekr.20040722105941:<< autocompleter imports >>
import leoGlobals as g 

import leoColor 
import leoPlugins 
import leoTkinterFrame 

try:
    import Pmw 
except ImportError:
    g.es("Autocompleter.py: can not import Pmw",color="blue")
    Pmw = None 

try:
    import Tkinter as Tk 
except ImportError:
    g.es("Autocompleter.py: can not import Tkinter",color="blue")
    Tk = None 

try:
    import sets 
except ImportError:
    g.es("Autocompleter.py: can not import sets",color="blue")
    sets = None 

import ConfigParser 
import os.path 
import re 
import string 
import threading 
#@nonl
#@-node:ekr.20040722105941:<< autocompleter imports >>
#@nl

watchwords ={}
calltips ={}

#@<<create pats dictionary>>
#@+node:ekr.20040722105941.16:<< create pats dictionary >>
pats ={}

space = r'[ \t\r\f\v ]+'

end = r'\w+\([^)]*\)'

pats['python'] = re.compile(r'def\s+'+end)

pats['java'] = re.compile(r'((public\s+|private\s+|protected\s+)?(static'+space+'|\w+'+space+'){1,2}'+end+')')

pats['perl'] = re.compile(r'sub\s+'+end)

pats['c++'] = re.compile(r'((virtual\s+)?\w+'+space+end+')')

pats['c'] = re.compile(r'\w+'+space+end)
#@nonl
#@-node:ekr.20040722105941.16:<< create pats dictionary >>
#@nl

r = string.punctuation.replace('(','').replace('.','')
pt = string.digits+string.letters+r 

useauto = 1
usecall = 1

#@+others
#@+node:ekr.20040722105941.1:watcher
def watcher (event):
    
    global lang 

    if event.char in('.','('):
        c = g.top()
        body = c.frame.body.bodyCtrl 
        txt = body.get('1.0',Tk.END)
        lang = c.frame.body.getColorizer().language 
        scanText(txt)
#@-node:ekr.20040722105941.1:watcher
#@+node:ekr.20040722105941.2:scanText
ripout = string.punctuation+string.whitespace+'\n'
ripout = ripout.replace('_','')

def scanText (txt):
    
    if useauto:
        #@        << handle autocompletion >>
        #@+node:ekr.20040722112432:<< handle autocompletion >>
        t1 = txt.split('.')
        g =[]
        reduce(lambda a,b:makeAutocompletionList(a,b,g),t1)
        if g:
            for a, b in g:
                if watchwords.has_key(a):
                    watchwords[a].add(b)
                else:
                    watchwords[a] = sets.Set([b])
        #@nonl
        #@-node:ekr.20040722112432:<< handle autocompletion >>
        #@nl
    
    if usecall:
        #@        << handle calltips >>
        #@+node:ekr.20040722112432.1:<< handle calltips >>
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
                if calltips.has_key(lang):
                    if calltips[lang].has_key(a):
                        # EKR: this has been known to throw a KeyError.
                        calltips[lang][a].add(z)
                    else:
                        from sets import Set 
                        calltips[lang][a] = Set([z])
                else:
                    from sets import Set 
                    calltips[lang] ={}
                    calltips[lang][a] = Set([z])
        #@nonl
        #@-node:ekr.20040722112432.1:<< handle calltips >>
        #@nl
#@nonl
#@-node:ekr.20040722105941.2:scanText
#@+node:ekr.20040722105941.3:makeAutocompletionList
def makeAutocompletionList (a,b,glist):
    a1 = _reverseFindWhitespace(a)
    if a1:
        b2 = _getCleanString(b)
        if b2!='':
            glist.append((a1,b2))
    return b 
#@nonl
#@-node:ekr.20040722105941.3:makeAutocompletionList
#@+node:ekr.20040722105941.4:_getCleanString
okchars ={}

for z in string.ascii_letters:
    okchars[z] = z 

okchars['_'] = '_'

def _getCleanString (s):
    if s.isalpha():return s 
    for n, l in enumerate(s):
        if l in okchars:pass 
        else:return s[:n]
    return s         
#@nonl
#@-node:ekr.20040722105941.4:_getCleanString
#@+node:ekr.20040722105941.5:_reverseFindWhitespace
def _reverseFindWhitespace (s):
    
    for n, l in enumerate(s):
        n =(n+1)*-1
        if s[n].isspace()or s[n]=='.':return s[n+1:]
    return s 
#@-node:ekr.20040722105941.5:_reverseFindWhitespace
#@+node:ekr.20040722105941.6:initialScan
lang = None 

def initialScan (tag,keywords):
    
    if keywords.has_key('c'):
        c = keywords['c']
    elif keywords.has_key('new_c'):
        c = keywords['new_c']

    #@    <<define scan callback>>
    #@+node:ekr.20040722110753:<< define scan callback >>
    def scan ():
        global lang, usecall, useauto, pat 
        pth = os.path.split(g.app.loadDir)
        aini = pth[0]+r"/plugins/autocompleter.ini"
        if os.path.exists(aini):
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
        
        bankpath = pth[0]+r"/plugins/autocompleter/"
        for z in pats:
            bpath = bankpath+z+'.ato'
            if os.path.exists(bpath):
                f = open(bpath)
                lang = z 
                for x in f:
                    scanText(x)
                f.close()
                
        if 'Chapters'in g.app.loadedPlugins:
            import Chapters 
            it = Chapters.walkChapters()
            for x in it:
                lang = None 
                setLanguage(x)
                scanText(x.bodyString())
        else:
            v = c.rootVnode()
            while v:
                setLanguage(v)
                scanText(v.bodyString())
                v = v.threadNext()
    #@nonl
    #@-node:ekr.20040722110753:<< define scan callback >>
    #@nl
                
    threading.Thread(target=scan).start()
#@nonl
#@-node:ekr.20040722105941.6:initialScan
#@+node:ekr.20040722105941.7:reducer
def reducer (lis,pat):

    return[x for x in lis if x.startswith(pat)]
#@nonl
#@-node:ekr.20040722105941.7:reducer
#@+node:ekr.20040722105941.8:unbind
def unbind (canvas,body):
    
    canvas.on = False 
    c = canvas 
    c.unbind("<Control_L>")
    c.unbind("<Control_R>")
    c.unbind("<Alt-Up>")
    c.unbind("<Alt-Down>")
    c.unbind("<Alt_L>")
    c.unbind("<Alt_R>")
#@-node:ekr.20040722105941.8:unbind
#@+node:ekr.20040722105941.9:moveSelItem
def moveSelItem (event,c):

    #c in this def is not a commander but a Tk Canvas
    i = c.sl.curselection()
    if len(i)==0:
        return None 
    i = int(i[0])
    try:
        if event.keysym=='Down':
            if c.sl.size()-1>c.sl.index(i):
                i = i+1
        else:
            if i!=0:
                i = i-1
    finally:
        c.sl.select_clear(0,'end')
        c.sl.select_set(i)
        c.sl.see(i)
        return "break"
#@nonl
#@-node:ekr.20040722105941.9:moveSelItem
#@+node:ekr.20040722105941.10:select
def select (event,c,body):
    #c in this def is not a commander but a Tk Canvas
    if not c.on:return None 
    if event.keysym=="??":
        return None 
    if c.which and event.keysym in('parenright',
    'Control_L','Control_R'):
        c.delete(c.i)
        c.on = False 
    elif event.keysym in("Shift_L","Shift_R"):
        return None 
    elif not c.which and event.char in ripout:
        c.delete(c.i)
        unbind(c,body)
    if c.which==1:
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
#@-node:ekr.20040722105941.10:select
#@+node:ekr.20040722105941.11:remove
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
        unbind(c,body)
#@nonl
#@-node:ekr.20040722105941.11:remove
#@+node:ekr.20040722105941.12:add_item
def add_item (event,c,body,colorizer):
    #c in this def is not a commander but a Tk Canvas
    if not event.char in('.','(')or c.on:return None 
    txt = body.get('insert linestart','insert')
    txt = _reverseFindWhitespace(txt)
    if event.char!='('and not watchwords.has_key(txt):
        return None 
    c.on = False 
    c.which = 0
    b = None 
    if event.char=='.':
        #@        << handle '.' character >>
        #@+node:ekr.20040722112432.2:<< handle '.' character >>
        c.on = True 
        f = Tk.Frame(c)
        ww = list(watchwords[txt])
        ww.sort()
        
        b = Pmw.ScrolledListBox(f,items=tuple(ww),hscrollmode='none')
        c.sl = b.component('listbox')
        c.sl.configure(selectbackground='#FFE7C6',selectforeground='blue')
        vsb = b.component('vertscrollbar')
        vsb.configure(background='#FFE7C6',width=10)
        h = b.component('hull')
        height = len(ww)
        
        if height>5:height = 5
        
        c.sl.configure(background='white',foreground='blue',height=height)
        b.pack()
        calculatePlace(body,c.sl,c,f)
        c.sl.select_set(0)
        c.which = 0
        #@nonl
        #@-node:ekr.20040722112432.2:<< handle '.' character >>
        #@nl
    elif event.char=='(':
        #@        << handle '(' character >>
        #@+node:ekr.20040722112432.3:<< handle '(' character >>
        language = colorizer.language
        
        if calltips.has_key(language):
        
            if 0: #
                g.trace(txt)
                keys = calltips[language].keys()
                keys.sort()
                for key in keys:
                    print key
        
            if calltips[language].has_key(txt):
                c.on = True 
                ct = Tk.Label(c,background='lightyellow',foreground='black')
                s = list(calltips[language][txt])
                t = '\n'.join(s)
                ct.configure(text=t)
                calculatePlace(body,ct,c,ct)
                c.which = 1
        else:
            c.on = False 
            return None
        #@nonl
        #@-node:ekr.20040722112432.3:<< handle '(' character >>
        #@nl

    if b:
        event = Tk.Event()
        event.keysym = ''
        rmv = lambda event = event, c = c, body = body, scrllistbx = b:remove(event,c,body,scrllistbx)
        b.configure(selectioncommand=rmv)
        c.bind("<Control_L>",rmv)
        c.bind("<Control_R>",rmv)
        c.bind("<Alt-Up>",lambda event,c=c:moveSelItem(event,c))
        c.bind("<Alt-Down>",lambda event,c=c:moveSelItem(event,c))
        c.bind("<Alt_L>",rmv)
        c.bind("<Alt_R>",rmv)
#@nonl
#@-node:ekr.20040722105941.12:add_item
#@+node:ekr.20040722105941.13:calculatePlace
def calculatePlace (body,cwidg,c,f):

    #c in this def is not a commander but a Tk Canvas
    try:
        x, y, lww, lwh = body.bbox('insert -1c')
        x, y = x+lww, y+lwh 
    except:
        x = 1
        y = 1

    rwidth  = cwidg.winfo_reqwidth()
    rheight = cwidg.winfo_reqheight()

    if body.winfo_width()<x+rwidth:
        x = x-rwidth

    if y>body.winfo_height()/2:
        h2 = rheight 
        h3 = h2+lwh 
        y  = y-h3

    c.i = c.create_window(x,y,window=f,anchor='nw')
#@nonl
#@-node:ekr.20040722105941.13:calculatePlace
#@+node:ekr.20040722105941.14:setLanguage
def setLanguage (vnd):
    
    global lang

    while vnd:
        xs1 = vnd.bodyString()
        dict = g.get_directives_dict(xs1)
        if dict.has_key('language'):
            lang = g.set_language(xs1,dict['language'])[0]
            break 
        vnd = vnd.parent()
#@nonl
#@-node:ekr.20040722105941.14:setLanguage
#@+node:ekr.20040722105941.15:newCreateControl
def newCreateControl (self,frame,parentFrame):
    
    c = Tk.Canvas(parentFrame,background='white')
    c.pack(expand=1,fill='both')
    f = Tk.Frame(c)
    c.create_window(0,0,window=f,anchor='nw')
    f.pack_configure(fill='both',expand=1)
    body = olCreateControl(self,frame,f)
    c.on = False 
    sel = lambda event, c = c, body = body:select(event,c,body)
    ai = lambda event, c = c, body = body, colorizer = frame.body:add_item(event,c,body,colorizer.getColorizer())
    c.bind("<Key>",watcher,'+')
    c.bind("<Key>",sel,'+')
    c.bind("<Key>",ai,'+')
    ctags = c.bindtags()
    btags = body.bindtags()
    btags =(ctags[0],btags[0],btags[1],btags[2],btags[3])
    body.bindtags(btags)
    return body
#@nonl
#@-node:ekr.20040722105941.15:newCreateControl
#@-others

olCreateControl = leoTkinterFrame.leoTkinterBody.createControl 

if Tk and Pmw and sets:
    leoTkinterFrame.leoTkinterBody.createControl = newCreateControl 
    leoPlugins.registerHandler('open2',initialScan) # EKR: We _must_ remove the start2 hook!
    __version__ = ".150"
    print "autocompleter v%s installed" % __version__
    g.plugin_signon(__name__)
#@nonl
#@-node:ekr.20040722104914:@thin autocompleter.py
#@-leo
