#@+leo-ver=4
#@+node:@file word_export.py
"""Exports an outline to a word document.

Make sure word is running with an open (empty) document.

Click "plugins ... word export ... export"
to export the selected outline to Word."""

#@@language python

import leoPlugins
import leoGlobals as g
from leoGlobals import true,false
try:
	import win32com.client # From win32 extensions: http://www.python.org/windows/win32/
	client = win32com.client
except ImportError:
	client = None
import ConfigParser

#@+others
#@+node:getConfiguration
def getConfiguration():
	
	"""Called when the user presses the "Apply" button on the Properties form"""

	fileName = os.path.join(g.app.loadDir,"../","plugins","word_export.ini")
	config = ConfigParser.ConfigParser()
	config.read(fileName)
	return config
#@-node:getConfiguration
#@+node:getWordConnection
def getWordConnection():
	
	"""Get a connection to Word"""

	g.es("Trying to connect to Word")
	try:
		word = win32com.client.Dispatch("Word.Application")
		return word
	except Exception, err:
		# g.es("Failed to connect to Word: %s", err)
		g.es("Failed to connect to Word",color="blue")
		g.es("Please make sure word is running with an open (empty) document.")
		return None
#@nonl
#@-node:getWordConnection
#@+node:doPara
def doPara(word, text, style=None):
	
	"""Write a paragraph to word"""
	
	doc = word.Documents(word.ActiveDocument)
	sel = word.Selection
	if style:
		try:
			sel.Style = doc.Styles(style)
		except:
			g.es("Unknown style: '%s'" % style)
	sel.TypeText(text)
	sel.TypeParagraph()
#@nonl
#@-node:doPara
#@+node:writeNodeAndTree
def writeNodeAndTree(word, header_style, level, maxlevel=3, usesections=1, sectionhead="", vnode=None):
	
	"""Write a node and its children to Word"""

	c = g.top()
	if vnode is None:
		vnode = g.top().currentVnode()
	#
	dict = g.scanDirectives(c,p=vnode)
	encoding = dict.get("encoding",None)
	if encoding == None:
		encoding = g.app.config.default_derived_file_encoding
	# 
	s = vnode.bodyString()
	s = g.toEncodedString(s,encoding,reportErrors=true)
	doPara(word, s)
	#
	for i in range(vnode.numberOfChildren()):
		if usesections:
			thishead = "%s%d." % (sectionhead, i+1)
		else:
			thishead = ""
		child = vnode.nthChild(i)
		h = child.headString()
		h = g.toEncodedString(h, encoding, reportErrors=true)
		doPara(word, "%s %s" % (thishead, h), "%s %d" % (header_style, min(level, maxlevel)))
		writeNodeAndTree(word, header_style, level+1, maxlevel, usesections, thishead, child)
#@-node:writeNodeAndTree
#@+node:cmd_Export
def cmd_Export(event=None):

	"""Export the current node to Word"""

	try:
		word = getWordConnection()
		if word:
			header_style = getConfiguration().get("Main", "Header_Style")
			# Based on the rst plugin
			g.es("Writing tree to Word",color="blue")
			config = getConfiguration()
			writeNodeAndTree(word,
				config.get("Main", "header_style").strip(),
				1,
				int(config.get("Main", "max_headings")),
				config.get("Main", "use_section_numbers") == "Yes",
				"")						 
			g.es("Done!")
	except Exception,err:
		g.es("Failed to connect to Word",color="blue")
		g.es("Please make sure an empty word document is open.")
#@nonl
#@-node:cmd_Export
#@-others

if client: # Register the handlers...

	# No hooks, we just use the cmd_Export to trigger an export
	__version__ = "0.1"
	__name__ = "Word Export"

	g.plugin_signon("word_export")
#@nonl
#@-node:@file word_export.py
#@-leo
