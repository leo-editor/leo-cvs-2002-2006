#@+leo-ver=4-thin
#@+node:EKR.20040605181725.2:@thin autocompleter.py
"""A plugin to do auto completion while typing.
Requires Pmw (Python Mega Widgets)."""

#@<< autocompleter imports >>
#@+node:EKR.20040605183135:<< autocompleter imports >>
import leoTkinterFrame
import leoColor
import leoPlugins

import ConfigParser 
import re
import sets 
import string
import threading

import leoGlobals as g

try: import Tkinter as Tk
except ImportError:
	g.es("Can not load autocompleter.py...",color="blue")
	g.es("can not import Tkinter",color="blue")
	Tk = None

try: import Pmw
except ImportError:
	g.es("Can not load autocompleter.py...",color="blue")
	g.es("Can not import Pmw",color="blue")
	Pmw = None
#@nonl
#@-node:EKR.20040605183135:<< autocompleter imports >>
#@nl

useauto = 1
usecall = 1

#@<< autocompleter globals >>
#@+node:EKR.20040605183135.1:<< autocompleter globals >>
watchwords = {}
calltips = {}

pats = {}
space = r'[ \t\r\f\v ]+'
end = r'\w+\([^)]*\)'

pats['python'] = re.compile(r'def\s+'+end)
pats['java']   = re.compile(r'((public\s+|private\s+|protected\s+)?(static'+space+'|\w+'+space +'){1,2}'+ end + ')')
pats['perl']   = re.compile(r'sub\s+' + end)
pats['c++']    = re.compile(r'((virtual\s+)?\w+'+ space + end +')')
pats['c']      = re.compile(r'\w+'+ space + end)

pat = re.compile(r'(\b[^.\s]+?\.[^.\s]+?\W)')

lang = None
scanning = False # A lockout.
#@-node:EKR.20040605183135.1:<< autocompleter globals >>
#@nl
#@<< changes made by EKR >>
#@+node:EKR.20040605192854:<< changes made by EKR >>
#@+at
# 
# Style changes...
# 
# Tkinter -> Tk
# Tk.INSERT -> "insert", etc.
# g -> g1 (in one function)
# import leoGlobals as g
# os.path.x -> g.os_path_x
# l -> label
# lis -> aList
# vnd -> v
# xsl -> s
# removed whitespace around parens, square brackets and commas.
# 
# Substantive changes...
# 
# 1.  We must NOT create two threads for scanning at the same time.  Doing so 
# creates conflicts in the lang global, and perhaps in other places.  
# Therefore, I removed the "start2" hook.
# 
# 2.  Created the setLanguageFromBody function, and called this inside 
# scanText if lang is not defined.  scanText returns if lang is still not 
# defined.  This probably will never happen now that only one scanning thread 
# is likely to be running.
# 
# 3.  Now that lang is properly defined, scanText should just reuturn if 
# pats[lang] does not exist.  This is not an error: it just means that lang is 
# not supported.  There is no point in using the Python pattern in that case.
#@-at
#@nonl
#@-node:EKR.20040605192854:<< changes made by EKR >>
#@nl

#@+others
#@+node:EKR.20040605184409:Overridden methods in leoTkinterBody
#@+node:EKR.20040605182632:createControl
def createControl (self,frame,parentFrame):
	config = g.app.config

	# A light selectbackground value is needed to make syntax coloring look good.
	wrap = config.getBoolWindowPref('body_pane_wraps')
	wrap = g.choose(wrap,"word","none")
	c = Tk.Canvas(parentFrame) 
	#c.pack(fill = 'both', expand = 1)
	# Setgrid=1 cause severe problems with the font panel.
	body = Tk.Text(c ,name='body',
		bd=2,bg="white",relief="flat",
		setgrid=0,wrap=wrap, selectbackground="Gray80") 
	c.create_window(0, 0, window = body , anchor = 'nw', width = c.cget('width'), height = c.cget('height'))
	bodyBar = Tk.Scrollbar(parentFrame,name='bodyBar')
	frame.bodyBar = self.bodyBar = bodyBar
	body['yscrollcommand'] = bodyBar.set
	bodyBar['command'] = body.yview
	bodyBar.pack(side="right", fill="y")
	c.pack(fill = 'both', expand = 1)
	# 8/30/03: Always create the horizontal bar.
	self.bodyXBar = bodyXBar = Tk.Scrollbar(
		parentFrame,name='bodyXBar',orient="horizontal")
	body['xscrollcommand'] = bodyXBar.set
	bodyXBar['command'] = body.xview
	self.bodyXbar = frame.bodyXBar = bodyXBar

	if wrap == "none":
		bodyXBar.pack(side="bottom", fill="x")

	body.pack(expand=1, fill="both")

	if 0: # Causes the cursor not to blink.
		body.configure(insertofftime=0)
	c.on = False
	sel = lambda event,c=c,body=body: select(event,c,body)
	ai  = lambda event,c=c,body=body,colorizer=frame.body: add_item(event,c,body,colorizer.getColorizer())
	body.bind("<Key>", watcher, '+')
	body.bind("<Key>", sel, '+')
	body.bind("<Key>", ai, '+') 
	return body
#@nonl
#@-node:EKR.20040605182632:createControl
#@+node:EKR.20040605182632.1:createBindings
def createBindings (self,frame):

	t = self.bodyCtrl

	# Event handlers...
	t.bind("<Button-1>", frame.OnBodyClick)
	t.bind("<Button-3>", frame.OnBodyRClick)
	t.bind("<Double-Button-1>", frame.OnBodyDoubleClick)
	t.bind("<Key>", frame.body.onBodyKey, '+')

	# Gui-dependent commands...
	t.bind(g.virtual_event_name("Cut"), frame.OnCut)
	t.bind(g.virtual_event_name("Copy"), frame.OnCopy)
	t.bind(g.virtual_event_name("Paste"), frame.OnPaste)
#@nonl
#@-node:EKR.20040605182632.1:createBindings
#@-node:EKR.20040605184409:Overridden methods in leoTkinterBody
#@+node:EKR.20040605184409.3:Event handlers...
#@+node:EKR.20040605182632.7:moveSelItem
def moveSelItem (event,canvas):
	
	# g.trace(event)

	i = canvas.sl.curselection()
	if len(i) == 0:
		return None
	i = int(i[0])
	try:
		if event.keysym == 'Down':
			if canvas.sl.size() - 1 > canvas.sl.index(i):
				i = i + 1
		else:
			if i != 0:
				i = i - 1
	finally:
		canvas.sl.select_clear(0, "end")
		canvas.sl.select_set(i)
		canvas.sl.see(i)
		return "break"
#@nonl
#@-node:EKR.20040605182632.7:moveSelItem
#@+node:EKR.20040605182632.8:select
def select (event,canvas,body):
	
	# g.trace(event)

	if not canvas.on : return None
	if event.keysym == "??":
		return None
	if canvas.which and event.keysym in ('parenright','Control_L', 'Control_R'):
		canvas.delete(canvas.i)
		canvas.on = False
	elif event.keysym in ("Shift_L", "Shift_R"):
		return None
	elif not canvas.which and event.char in ripout:
		canvas.delete(canvas.i)
		unbind(canvas, body)
	if canvas.which == 1:
		return None

	ind = body.index('insert-1c wordstart')
	pat = body.get(ind , "insert") + event.char
	pat = pat.lstrip('.')
	ww = list(canvas.sl.get(0,"end"))
	aList = reducer(ww , pat)
	if len(aList) == 0 : return None
	i = ww.index(aList[0])
	canvas.sl.select_clear(0,"end")
	canvas.sl.select_set(i)
	canvas.sl.see(i)
#@nonl
#@-node:EKR.20040605182632.8:select
#@+node:EKR.20040605182632.9:remove
def remove (event,canvas,body,scrllistbx):
	
	# g.trace(event)

	if event.keysym in ("Alt_L", "Alt_R"):
		return None
	canvas.delete(canvas.i)
	a = scrllistbx.getvalue()
	if len(a) == 0 : return None
	try:
		a = a[0]
		ind = body.index('insert-1c wordstart')
		pat = body.get(ind , "insert")
		pat = pat.lstrip('.')

		if a.startswith(pat) : a = a[len(pat) :]
		body.insert("insert", a)
		body.event_generate("<Key>")
		body.update_idletasks()
	finally:
		unbind(canvas, body)
#@nonl
#@-node:EKR.20040605182632.9:remove
#@+node:EKR.20040605182632.10:add_item
def add_item (event,canvas,body,colorizer):
	
	# g.trace()

	if not event.char in('.' , '(') or canvas.on : return None
	ind = body.index('insert-1c wordstart')
	txt = body.get(ind , "insert")
	if event.char != '(' and not watchwords.has_key(txt):
		return None
	canvas.on = False
	canvas.which = 0
	b = None
	if event.char == '.':
		#@		<< handle '.' >>
		#@+node:EKR.20040605184409.4:<< handle '.' >>
		canvas.on = True
		f = Tk.Frame(canvas)
		ww = list(watchwords[txt])
		ww.sort()
		
		b = Pmw.ScrolledListBox(f,items=tuple(ww),hscrollmode='none')
		canvas.sl = b.component('listbox')
		h = b.component('hull')
		
		height = min(5,len(ww))
		
		canvas.sl.configure(background='white',foreground='blue',height=height)
		b.pack()
		
		calculatePlace(body, canvas.sl,canvas,f)
		canvas.sl.select_set(0)
		canvas.which = 0
		#@nonl
		#@-node:EKR.20040605184409.4:<< handle '.' >>
		#@nl
	elif event.char == '(':
		#@		<< handle '(' >>
		#@+node:EKR.20040605184409.5:<< handle '(' >>
		language = colorizer.language
		
		if 0:
			g.trace(language,calltips.has_key(language),calltips[language].has_key(txt))
			g.trace(txt)
			d = calltips[language]
			for key in d.keys():
				print key # ,d[key]
		
		if calltips.has_key(language):
			if calltips[language].has_key(txt):
				canvas.on = True
				ct = Tk.Label(canvas,background ='lightyellow',foreground = 'black')
				s = list(calltips[language][txt])
				t = '\n'.join(s)
				ct.configure(text = t)
				calculatePlace(body,ct,canvas,ct)
				canvas.which = 1
		else: 
			canvas.on = False
			return None
		#@nonl
		#@-node:EKR.20040605184409.5:<< handle '(' >>
		#@nl

	if b :
		event = Tk.Event() ; event.keysym = ''
		rmv = lambda event=event,canvas=canvas,body=body,scrllistbx=b : remove(event,canvas,body,scrllistbx)

		b.configure(selectioncommand = rmv)
		body.bind("<Control_L>", rmv)
		body.bind("<Control_R>", rmv)
		body.bind("<Alt-Up>",   lambda event,canvas=canvas: moveSelItem(event,canvas))
		body.bind("<Alt-Down>", lambda event,canvas=canvas: moveSelItem(event,canvas))
		body.bind("<Alt_L>", rmv)
		body.bind("<Alt_R>", rmv)
#@nonl
#@-node:EKR.20040605182632.10:add_item
#@-node:EKR.20040605184409.3:Event handlers...
#@+node:EKR.20040605182632.4:Scanning...
#@+node:EKR.20040605182632.3:scanText
ripout = string.punctuation + string.whitespace+'\n'
ripout = ripout.replace('_', '')

def scanText (txt):
	
	global lang # EKR

	if useauto:
		g1 = pat.findall(txt)
		if g1 : 
			for z in g1:
				pieces = z.split('.')
				a, b = pieces[0] , pieces[1]
				b = b.strip(ripout)
				if watchwords.has_key(a):
					watchwords[a].add(b)
				else:
					watchwords[a] = sets.Set([b])

	if usecall:
		if not lang: # EKR: new code.
			# Threads make setting lang tricky.
			setLanguageFromBody()
			# assert(lang)
			if not lang: return
		try: # EKR: New code
			pat2 = pats[lang]
		except KeyError:
			# This is _not_ an error, it just means the language is not supported.
			# g.trace("no dict for",lang)
			return
		g2 = pat2.findall(txt)
		# if g2: g.trace(lang,g2)
		if g2 : 
			for z in g2:
				if isinstance(z, tuple):
					z = z[0]
				pieces2 = z.split('(')
				pieces2[0] = pieces2[0].split()[-1]
				a, b = pieces2[0] , pieces2[1]
				if calltips.has_key(lang):
					if calltips[lang].has_key(a):
						calltips[lang][a].add(z)
					else:
						calltips[lang][a] = sets.Set([z])
				else:
					calltips[lang] = {}
					calltips[lang][a] = sets.Set([z])
				
#@nonl
#@-node:EKR.20040605182632.3:scanText
#@+node:EKR.20040605184657:initialScan
def initialScan (tag,keywords):
	
	if keywords.has_key('c'):
		c = keywords['c']
	elif keywords.has_key('new_c'):
		c = keywords['new_c']
		
	# It is imperative that this only one scanning thread be running at any one time.
	# Otherwise, the threads can clash over setting the lang global.

	def scan(c=c):
		global scanning
		if not scanning:
			scanning = True
			doScan(c)
			scanning = False

	threading.Thread(target=scan).start()
#@nonl
#@-node:EKR.20040605184657:initialScan
#@+node:EKR.20040605184409.1:doScan
def doScan (c):

	global lang, usecall, useauto, pat
	
	# g.trace(c)
	
	pth = g.os_path_split(g.app.loadDir)
	ini_path = pth[0] + r"/plugins/autocompleter.ini" 
	if g.os_path_exists(ini_path):
		#@		<< get config settings >>
		#@+node:EKR.20040605184409.2:<< get config settings >>
		cp = ConfigParser.ConfigParser()
		cp.read(ini_path)
		ac = None
		
		for z in cp.sections():
			if z.strip() == 'autocompleter':
				ac = z
				continue
			ipats = r'' + cp.get(z, 'pat').strip()
			z = z.strip()
			pats[z] = re.compile(ipats)
		
		if cp.has_section(ac):
			if cp.has_option(ac, 'useauto'):
				useauto = int(cp.get(ac, 'useauto'))
			if cp.has_option(ac, 'usecalltips'):
				usecall = int(cp.get(ac, 'usecalltips'))
			if cp.has_option(ac, 'autopattern'):
				pat = re.compile(cp.get(ac, 'autopattern'))
		#@nonl
		#@-node:EKR.20040605184409.2:<< get config settings >>
		#@nl

	bankpath = pth[0] + r"/plugins/autocompleter/"
	for z in pats:
		bpath = bankpath +z + '.ato' 
		if g.os_path_exists(bpath):
			f = open(bpath)
			lang = str(z)
			g.trace("z",z)
			for x in f:
				scanText(x)
			f.close()

	if 'Chapters' in g.app.loadedPlugins:
		import Chapters
		it = Chapters.walkChapters()
		for x in it:
			setLanguage(x)
			scanText(x.bodyString())
	else:
		v = c.rootVnode()
		while v:
			setLanguage(v) 
			scanText(v.bodyString())
			v = v.threadNext()

#@-node:EKR.20040605184409.1:doScan
#@-node:EKR.20040605182632.4:Scanning...
#@+node:EKR.20040607074710:Utilities...
#@+node:EKR.20040605182906:calculatePlace
def calculatePlace (body,cwidg,canvas,f):

	label = Tk.Label(body)
	body.window_create("insert",window=label)
	body.update_idletasks()

	lwh = label.winfo_height()
	x, y = label.winfo_x() , label.winfo_y() + lwh
	body.delete(label)

	rwidth = cwidg.winfo_reqwidth()
	rheight = cwidg.winfo_reqheight()
	if body.winfo_width() < x + rwidth:
		x = x - rwidth
	if y > body.winfo_height()/2:
		h2 = rheight
		h3 = h2 + lwh
		y = y - h3

	canvas.i = canvas.create_window(x,y,window=f,anchor='nw')
#@nonl
#@-node:EKR.20040605182906:calculatePlace
#@+node:EKR.20040605182632.5:reducer
def reducer (aList,pat):

	return [x for x in aList if x.startswith(pat)]
#@nonl
#@-node:EKR.20040605182632.5:reducer
#@+node:EKR.20040605182906.1:setLanguage
def setLanguage (v):
	
	c = v.c
	
	global lang ; lang = None

	while v:
		s = v.bodyString()
		dict = g.get_directives_dict(s)
		if dict.has_key('language'):
			lang = g.set_language(s, dict['language'])[0]
			break
		v = v.parent()

	if not lang:
		lang = c.target_language
		
	lang = str(lang)
	
	try:
		assert(lang)
	except AssertionError:
		g.trace(lang)
		g.trace(c.target_language)
#@nonl
#@-node:EKR.20040605182906.1:setLanguage
#@+node:EKR.20040607085953:setLanguageFromBody
def setLanguageFromBody ():
	
	c = g.top() ; global lang

	lang = c.frame.body.getColorizer().language
	if not lang:
		lang = c.target_language
	lang = str(lang)
	assert(lang)
#@nonl
#@-node:EKR.20040607085953:setLanguageFromBody
#@+node:EKR.20040605182632.6:unbind
def unbind (canvas,body):

	canvas.on = False
	body.unbind("<Control_L>")
	body.unbind("<Control_R>")
	body.unbind("<Alt-Up>")
	body.unbind("<Alt-Down>")
	body.unbind("<Alt_L>")
	body.unbind("<Alt_R>")
#@nonl
#@-node:EKR.20040605182632.6:unbind
#@+node:EKR.20040605182632.2:watcher
def watcher (event):
	
	global lang

	if event.char in ('.', '('):

		c = g.top()

		body = c.frame.body.bodyCtrl
		txt = body.get('1.0', "end")
		
		scanText(txt)
#@nonl
#@-node:EKR.20040605182632.2:watcher
#@-node:EKR.20040607074710:Utilities...
#@-others

if Tk and Pmw:

	# Override some of Leo's core functions.
	leoTkinterFrame.leoTkinterBody.createControl = createControl
	leoTkinterFrame.leoTkinterBody.createBindings = createBindings
	
	# It is imperative that this only one scanning thread be running at any one time.
	# Otherwise, the threads can clash over setting the lang global.
	# Therefore, we must remove the "start2" hook.

	leoPlugins.registerHandler('open2',initialScan)

	__version__ = ".126a" # Mods made by EKR.
	__name__ = 'autocompleter'
	g.plugin_signon(__name__)
#@nonl
#@-node:EKR.20040605181725.2:@thin autocompleter.py
#@-leo
