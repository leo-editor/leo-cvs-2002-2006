#@+leo-ver=4-thin
#@+node:edream.110203113231.669:@file-thin import_cisco_config.py
"""Import cisco configuration files"""

import leoPlugins
import leoGlobals as g
from leoGlobals import true,false

#@@language python

try:
	import tkFileDialog
except ImportError:
	tkFileDialog = None

#@<< about this plugin >>
#@+node:edream.110203113231.670:<< about this plugin >>
#@+at 
#@nonl
# This plugin adds a menu item under the File->Import menu to import
# Cisco configuration files.
# 
# The plugin will:
# 
# 1) create a new node, under the current node, where the configuration will 
# be
# written. This node will typically have references to several sections (see 
# below).
# 
# 2) create sections (child nodes) for the indented blocks present in the 
# original
# config file. These child nodes will have sub-nodes grouping similar blocks 
# (e.g.
# there will be an 'interface' child node, with as many sub-nodes as there are 
# real
# interfaces in the configuration file).
# 
# 3) create sections for the custom keywords specified in the customBlocks[] 
# list in
# importCiscoConfig(). You can modify this list to specify different keywords. 
# DO
# NOT put keywords that are followed by indented blocks (these are taken care 
# of by
# point 2 above). The negated form of the keywords (for example, if the 
# keyword is
# 'service', the negated form is 'no service') is also included in the 
# sections.
# 
# 4) not display consecutive empty comment lines (lines with only a '!').
# 
# All created sections are alphabetically ordered.
# 
# Feedback on this plugin can be sent to Davide Salomoni 
# (dsalomoni@yahoo.com).
#@-at
#@-node:edream.110203113231.670:<< about this plugin >>
#@nl

if tkFileDialog:
	
	#@	@+others
	#@+node:edream.110203113231.671:create_import_cisco_menu
	def create_import_cisco_menu(tag, keywords):
		if	(tag=="open2" or
			(tag=="start2" and not keywords.has_key('c')) or
			(tag=="command2" and keywords.get("label")=="new")):
	
			c = g.top()
			importMenu = c.frame.menu.getMenu('import')
			newEntries = (
				("-", None, None),
				("Import C&isco Configuration", "Shift+Ctrl+I", importCiscoConfig))
			
			c.frame.menu.createMenuEntries(importMenu, newEntries)
	#@nonl
	#@-node:edream.110203113231.671:create_import_cisco_menu
	#@+node:edream.110203113231.672:importCiscoConfig
	def importCiscoConfig(event=None):
		c = g.top(); current = c.currentVnode()
		if current == None: return
		#@	<< open file >>
		#@+node:edream.110203113231.673:<< open file >>
		name = tkFileDialog.askopenfilename(
			title="Import Cisco Configuration File",
			filetypes=[("All files", "*")]
			)
		if name == "":	return
		
		v = current.insertAsNthChild(0)
		c.beginUpdate()
		v.setHeadString("cisco config: %s" % name)
		c.endUpdate()
		
		try:
			fh = open(name)
			g.es("importing: %s" % name)
			linelist = fh.read().splitlines()
			fh.close()
		except IOError,msg:
			g.es("error reading %s: %s" % (name, msg))
			return
		#@nonl
		#@-node:edream.110203113231.673:<< open file >>
		#@nl
	
		# define which additional child nodes will be created
		# these keywords must NOT be followed by indented blocks
		customBlocks = ['aaa','ip as-path','ip prefix-list','ip route',
						'ip community-list','access-list','snmp-server','ntp',
						'boot','service','logging']
		out = []
		blocks = {}
		children = []
		lines = len(linelist)
		i = 0
		skipToNextLine = 0
		# create level-0 and level-1 children
		while i<(lines-1):
			for customLine in customBlocks:
				if (linelist[i].startswith(customLine) or
					linelist[i].startswith('no %s' % customLine)):
					#@				<< process custom line >>
					#@+node:edream.110203113231.674:<< process custom line >>
					if not blocks.has_key(customLine):
						blocks[customLine] = []
						out.append(g.angleBrackets(customLine))
						# create first-level child
						child = v.insertAsNthChild(0)
						child.setHeadStringOrHeadline(g.angleBrackets(customLine))
						children.append(child)
					
					blocks[customLine].append(linelist[i])
					#@nonl
					#@-node:edream.110203113231.674:<< process custom line >>
					#@nl
					skipToNextLine = 1
					break
			if skipToNextLine:
				skipToNextLine = 0
			else:
				if linelist[i+1].startswith(' '):
					#@				<< process indented block >>
					#@+node:edream.110203113231.675:<< process indented block >>
					space = linelist[i].find(' ')
					if space == -1:
						space = len(linelist[i])
					key = linelist[i][:space]
					if not blocks.has_key(key):
						blocks[key] = []
						out.append(g.angleBrackets(key))
						# create first-level child
						child = v.insertAsNthChild(0)
						child.setHeadStringOrHeadline(g.angleBrackets(key))
						children.append(child)
					
					value = [linelist[i]]
					# loop through the indented lines
					i = i+1
					try:
						while linelist[i].startswith(' '):
							value.append(linelist[i])
							i = i+1
					except:
						# EOF
						pass
					i = i-1 # restore index
					# now add the value to the dictionary
					blocks[key].append(value)
					#@nonl
					#@-node:edream.110203113231.675:<< process indented block >>
					#@nl
				else:
					out.append(linelist[i])
			i=i+1
		# process last line
		out.append(linelist[i])
		
		#@	<< complete outline >>
		#@+node:edream.110203113231.676:<< complete outline >>
		# first print the level-0 text
		outClean = []
		prev = ''
		for line in out:
			if line=='!' and prev=='!':
				pass # skip repeated comment lines
			else:
				outClean.append(line)
			prev = line
		v.setBodyStringOrPane('\n'.join(outClean))
		
		# scan through the created outline and add children
		for child in children:
			# extract the key from the headline. Uhm... :)
			key = child.headString().split('<<'
				)[1].split('>>')[0].strip()
			if blocks.has_key(key):
				if type(blocks[key][0]) == type(''):
					# it's a string, no sub-children, so just print the text
					child.setBodyStringOrPane('\n'.join(blocks[key]))
				else:
					# it's a multi-level node
					for value in blocks[key]:
						# each value is a list containing the headline and then the text
						subchild = child.insertAsNthChild(0)
						subchild.setHeadStringOrHeadline(value[0])
						subchild.setBodyStringOrPane('\n'.join(value))
				child.sortChildren()
			else:
				# this should never happen
				g.es("Unknown key: %s" % key)
		v.sortChildren()
		#@nonl
		#@-node:edream.110203113231.676:<< complete outline >>
		#@nl
	#@nonl
	#@-node:edream.110203113231.672:importCiscoConfig
	#@-others
	
	if g.app.gui is None:
		g.app.createTkGui(__file__)

	if g.app.gui.guiName() == "tkinter":

		# Register the handlers...
		leoPlugins.registerHandler(("start2","open2","command2"),
			create_import_cisco_menu)

		__version__ = "1.3" 
		g.plugin_signon(__name__)
#@-node:edream.110203113231.669:@file-thin import_cisco_config.py
#@-leo
