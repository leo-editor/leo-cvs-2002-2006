#@+leo-ver=4
#@+node:@file color_markup.py
"""Handle coloring for markup in doc parts and Python triple-double-quoted strings"""

#@@language python

from leoPlugins import *
from leoGlobals import *

try:
	import Tkinter
except ImportError:
	Tkinter = None

import string  # zfill does not exist in Python 2.2.1
import tkColorChooser

if Tkinter: # Register the handlers...

	#@	@+others
	#@+node:initAnyMarkup
	def initAnyMarkup (tag,keywords):
		
		"""initialize colorer.markup_string
		
		The colorer completely recolors the body pane when this changes"""
		
		keys = ("colorer","v")
		colorer,v = [keywords.get(key) for key in keys]
	
		c = colorer.c
		if not c or not v or not top(): return
	
		# underline means hyperlinks
		c.frame.body.tag_configure("http",underline=1) # EKR: 11/4/03
		c.frame.body.tag_configure("https",underline=1) # EKR: 11/4/03
		# trace()
		dict = scanDirectives(c,p=v) # v arg is essential.
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
	#@-node:initAnyMarkup
	#@+node:colorWikiMarkup
	colorCount = 0
	
	def colorWikiMarkup (tag,keywords):
	
		keys = ("colorer","v","s","i","j","colortag")
		colorer,v,s,i,j,colortag = [keywords.get(key) for key in keys]
	
		global colorCount ; colorCount += 1
		
		c = colorer.c
		dict = scanDirectives(c,p=v) # v arg is essential.
		pluginsList = dict.get("pluginsList")
		
		if pluginsList:
			for d,v,s2,k in pluginsList:
				if d == "markup":
					# trace(`colorCount`,`d`)
					if match_word(s2,k,"wiki"):
						doWikiText(colorer,v,s,i,j,colortag)
						return true # We have colored the text.
				
		# trace(`colorCount`,"no markup")
		return None # We have not colored the text.
	#@nonl
	#@-node:colorWikiMarkup
	#@+node:doWikiText
	def doWikiText (colorer,v,s,i,end,colortag):
	
		firsti = i ; inserted = 0
	
		while i < end:
			#@		<< set first to a tuple describing the first tag to be handled >>
			#@+node:<< set first to a tuple describing the first tag to be handled >>
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
			#@-node:<< set first to a tuple describing the first tag to be handled >>
			#@nl
			if first:
				tag,n1,n2,delim1,delim2 = first
				i = n2 + len(delim2)
				#@			<< handle the tag using n1,n2,delim1,delim2 >>
				#@+node:<< handle the tag using n1,n2,delim1,delim2 >>
				if tag =="picture":
					colorer.tag("elide",n1,n2+len(delim2)) # Elide everything.
					filename = s[n1+len(delim1):n2]
					filename = os.path.join(app.loadDir,filename)
					filename = os.path.normpath(filename)
					inserted += insertWikiPicture(colorer,filename,n2+len(delim2))
				elif tag == "color":
					#@	<< parse and handle color field >>
					#@+node:<< parse and handle color field >>
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
								pass # es_exception()
					#@nonl
					#@-node:<< parse and handle color field >>
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
				#@-node:<< handle the tag using n1,n2,delim1,delim2 >>
				#@nl
			else: i = end
			
		colorer.tag(colortag,firsti,end+inserted)
	#@nonl
	#@-node:doWikiText
	#@+node:insertWikiPicture
	def insertWikiPicture (colorer,filename,i):
		
		"""Try to insert a picture with the give filename.
		
		Returns the number of characters actually inserted"""
		
		# trace(`colorer.color_pass`)
		if colorer.color_pass == 0:
			colorer.redoColoring = true # schedule a two-pass recoloring.
			return 0
			
		if colorer.color_pass == 2:
			return 0 # The second redo pass.
			
		# trace(`filename`,`v`)
		if not os.path.exists(filename):
			return 0
	
		try:
			# Create the image
			photo = Tkinter.PhotoImage(master=app.root, file=filename)
			image = colorer.body.bodyCtrl.image_create(colorer.index(i),image=photo,padx=0)
			
			# Keep references so images stay on the canvas.
			colorer.image_references.append((photo,image,colorer.line_index,i),)
			return 1
		except:
			es_exception()
			return 0
	#@nonl
	#@-node:insertWikiPicture
	#@+node:onBodykey1 (not ready)
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
	#@-node:onBodykey1 (not ready)
	#@+node:onBodydclick1 & allies
	def onBodydclick1(tag,keywords):
		"""Handle double clicks on a hyperlink."""
	
		c = keywords.get("c")
		url = getUrl(c, "http", "https")
		if url:
			try:
				import webbrowser
				webbrowser.open(url)
			except:
				es("exception opening " + url)
				es_exception()
	#@-node:onBodydclick1 & allies
	#@+node:getUrl
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
	#@-node:getUrl
	#@+node:createWikiMenu
	def createWikiMenu(tag, keywords):
		"""Create menu entries under Edit->Edit Body to insert wiki tags."""
	
		if	(tag=="open2" or tag=="start2" or
			(tag=="command2" and keywords.get("label")=="new")):
	
			c = top()
			
			editBodyMenuName = "Edit Body..."
			wikiMenuName = "&Wiki Tags..."
			if c.frame.menu.getMenu(wikiMenuName):
				return # wiki menu already created
	
			editBodyMenu = c.frame.menu.getMenu(editBodyMenuName)
			separator = (("-", None, None),)
			c.frame.menu.createMenuEntries(editBodyMenu, separator)
			
			wikiMenu = c.frame.menu.createNewMenu(wikiMenuName, editBodyMenuName)
			newEntries = (
				("&Bold", "Alt+Shift+B", doWikiBold),
				("&Italic", "Alt+Shift+I", doWikiItalic),
				#("Insert Pict&ure...", "Alt+Shift+U", doWikiPicture),
				("C&olor", "Alt+Shift+O", doWikiColor),
				("Choose Co&lor...", "Alt+Shift+L", doWikiChooseColor),
				)
			
			c.frame.menu.createMenuEntries(wikiMenu, newEntries)
	
	#@-node:createWikiMenu
	#@+node:doWikiBold
	def doWikiBold(event=None):
		c = top()
		v = c.currentVnode()
		if not v: return
	
		insertWikiMarkup(c,v,"__","__")
		return
	#@nonl
	#@-node:doWikiBold
	#@+node:doWikiItalic
	def doWikiItalic(event=None):
		c = top()
		v = c.currentVnode()
		if not v: return
	
		insertWikiMarkup(c,v,"''","''")
		return
	#@-node:doWikiItalic
	#@+node:doWikiColor
	def doWikiColor(event=None):
		global wikiColoredText
		
		c = top()
		v = c.currentVnode()
		if not v: return
	
		insertWikiMarkup(c,v,"~~%s:" % wikiColoredText,"~~")
		return
	#@-node:doWikiColor
	#@+node:doWikiChooseColor
	def doWikiChooseColor(event=None):
		global wikiColoredText
		
		c = top()
		v = c.currentVnode()
		if not v: return
		
		rgb,val = tkColorChooser.askcolor(color=wikiColoredText)
		if val:
			wikiColoredText = val
			doWikiColor()
	#@-node:doWikiChooseColor
	#@+node:doWikiPicture (not ready)
	def doWikiPicture(event=None):
		import tkFileDialog
	
		c = top()
		v = c.currentVnode()
		if not v: return
	
		name = tkFileDialog.askopenfilename(
			title="Insert Picture",
			filetypes=[("All files", "*")]
			)
		if name == "":	return
		
		insertWikiMarkup(c,v,"{picture file=%s}" % name,"")
		return
	#@nonl
	#@-node:doWikiPicture (not ready)
	#@+node:insertWikiMarkup
	def insertWikiMarkup(c,v,leftTag,rightTag):
		body = c.frame.body
		oldSel = body.bodyCtrl.tag_ranges("sel")
		if oldSel:
			#@		<< apply markup to selection >>
			#@+node:<< apply markup to selection >>
			start,end = oldSel
			body.bodyCtrl.insert(start, leftTag)
			# we need to review where the selection now ends
			start,end = body.bodyCtrl.tag_ranges("sel")
			body.bodyCtrl.insert(end, rightTag)
			app.gui.setTextSelection(body.bodyCtrl, start + "-" + `len(leftTag)`  + "c",
									 end + "+" + `len(rightTag)` + "c")
			newSel = body.getTextSelection()
			c.frame.onBodyChanged(v,"Change",oldSel=oldSel,newSel=newSel)
			#@-node:<< apply markup to selection >>
			#@nl
		else:
			#@		<< handle no selection >>
			#@+node:<< handle no selection >>
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
			c.frame.onBodyChanged(v,"Typing",oldSel=oldSel,newSel=newSel)
			#@-node:<< handle no selection >>
			#@nl
	
		body.focus_set()
	#@nonl
	#@-node:insertWikiMarkup
	#@-others

	if app.gui is None:
		app.createTkGui(__file__)

	if app.gui.guiName() == "tkinter":
		
		print "wiki markup enabled"
		
		# default value for color-tagged wiki text
		wikiColoredText = "blue"

		registerHandler("color-optional-markup", colorWikiMarkup)
		registerHandler("init-color-markup", initAnyMarkup)
		#registerHandler("bodykey1", onBodykey1)
		registerHandler("bodydclick1", onBodydclick1)
		registerHandler(("start2","open2","command2"), createWikiMenu)
	
		__version__ = "1.4" # DS: 10/29/03.  EKR: 11/4/03: mods for 4.1.
		plugin_signon(__name__)
#@-node:@file color_markup.py
#@-leo
