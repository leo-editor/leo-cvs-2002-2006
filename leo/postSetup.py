#! /usr/bin/env python
#@+leo-ver=4-thin
#@+node:ekr.20031218072017.2576:@file-thin ../postSetup.py
#@@first

""" Postprocess after executing setup.py """

import leoGlobals as g
from leoGlobals import true,false

#@+others
#@-others

def setup():
	if 1: # Use this only for final distributions.
		unsetDefaultParams()
	print "postSetup complete"
#@nonl
#@-node:ekr.20031218072017.2576:@file-thin ../postSetup.py
#@-leo
