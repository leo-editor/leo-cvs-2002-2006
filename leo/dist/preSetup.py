#! /usr/bin/env python
#@+leo-ver=4-thin
#@+node:ekr.20031218072017.2567:@file-thin ../dist/preSetup.py
#@@first

""" Preprocess before executing setup.py. """

import leoGlobals as g
from leoGlobals import true,false

#@+others
#@+node:EKR.20040517111254.1:saveAllLeoFiles
def saveAllLeoFiles():
	
	for frame in g.app.windowList:
		c = frame.c
		name = c.mFileName
		if name == "": name = "untitled"
		if c.changed:
			print "saving ",name
			c.save()
#@nonl
#@-node:EKR.20040517111254.1:saveAllLeoFiles
#@+node:EKR.20040517111254.2:tangleLeoConfigDotLeo
def tangleLeoConfigDotLeo():

	c = None
	name = g.os_path_join("config","leoConfig.leo")
	oldtop = g.top()
	for frame in g.app.windowList:
		if frame.c.mFileName == name :
			c = frame.c
			break
	
	if c == None:
		c = g.top()
		flag,frame = g.openWithFileName(name,c)
		if not flag:
			print "can not open ",name
			return
		c = frame.c
			
	print "Tangling ", name
	g.app.setLog(oldtop.frame.log) # Keep sending messages to the original frame.
	c.tangleCommands.tangleAll()
	c.close()
	g.app.setLog(oldtop.frame.log)
#@nonl
#@-node:EKR.20040517111254.2:tangleLeoConfigDotLeo
#@-others

def setup():
	saveAllLeoFiles()
	tangleLeoConfigDotLeo()
	print "preSetup complete"
#@nonl
#@-node:ekr.20031218072017.2567:@file-thin ../dist/preSetup.py
#@-leo
