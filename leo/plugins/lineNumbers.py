#@+leo-ver=4-thin
#@+node:ekr.20040419105219:@thin lineNumbers.py
"""Adds #line directives in perl and perlpod programs."""

#@+at 
#@nonl
# Over-ride two methods in leoAtFile.py to write #line directives after node 
# sentinels.
# This allows compilers to give locations of errors in relation to the node 
# name rather than the filename.
# Currently supports only perl and perlpod.
# 
# Use and distribute under the same terms as Leo.
# Original code by Mark Ng <markn@cs.mu.oz.au>
#@-at
#@@c

import leoGlobals as g
import leoPlugins

import leoAtFile
import re

linere = re.compile("^#line 1 \".*\"$")

#@+others
#@+node:ekr.20040419105219.1:writing derived files
oldOpenNodeSentinel = leoAtFile.newDerivedFile.putOpenNodeSentinel

def putLineNumberDirective(self,v,inAtAll=False,inAtOthers=False,middle=False):

    oldOpenNodeSentinel(self,v,inAtAll,inAtOthers,middle)

    if self.language in ("perl","perlpod"):
        line = 'line 1 "node:%s (%s)"' % (self.nodeSentinelText(v),self.shortFileName)
        self.putSentinel(line)
        
g.funcToMethod(putLineNumberDirective,	
    leoAtFile.newDerivedFile,"putOpenNodeSentinel")
#@nonl
#@-node:ekr.20040419105219.1:writing derived files
#@+node:ekr.20040419105219.2:reading derived files
readNormalLine = leoAtFile.newDerivedFile.readNormalLine

def skipLineNumberDirective(self, s, i):

    if linere.search(s): 
        return  # Skipt the line.
    else:		
        readNormalLine(self,s,i)

g.funcToMethod(skipLineNumberDirective,
    leoAtFile.newDerivedFile,"readNormalLine")
#@nonl
#@-node:ekr.20040419105219.2:reading derived files
#@-others

__version__ = "0.2"
    # 0.1: Mark Ng
    # 0.2: EKR: Convert to new coding conventions.

g.plugin_signon(__name__)
#@nonl
#@-node:ekr.20040419105219:@thin lineNumbers.py
#@-leo
