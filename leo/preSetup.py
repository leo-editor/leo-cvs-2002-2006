#! /usr/bin/env python
#@+leo-ver=4
#@+node:ekr.20031218072017.2567:@file-thin ../preSetup.py
#@@first

""" Preprocess before executing setup.py. """

import leoGlobals as g
from leoGlobals import true,false

#@+others
#@-others

def setup():
	saveAllLeoFiles()
	tangleLeoConfigDotLeo()
	print "preSetup complete"
#@nonl
#@-node:ekr.20031218072017.2567:@file-thin ../preSetup.py
#@-leo
