#@+leo-ver=4-thin
#@+node:ekr.20040915085351:@thin at_produce.py
"""
Executes commands in nodes whose body text starts with @produce.
"""

#@@language python
#@@tabwidth -4

#@<< about this plugin >>
#@+node:ekr.20040915085351.1:<< about this plugin >>
#@+at
# 
# To use, put in the body text of a node:
# 
# @produce javac -verbose Test.java
# 
# To execute, you goto Outline and look at Produce.  Choose Execute All 
# Produce
# or Execute Tree Produce.  The Tree does the current Tree, All does the whole
# Outline.  Executing will fire javac, or whatever your using.  @produce 
# functions
# as a directive.  After executing, a log file/node is created at the top of 
# the
# Outline.  Any output, even error messages, should be there.
# 
# It executes in a hierarchal manner.  Nodes that come before that contain 
# @produce
# go first.
# 
# Im hoping that this orthogonal to @run nodes and anything like that.  Its 
# not
# intended as a replacement for make or Ant, but as a simple substitute when 
# that
# machinery is overkill.
# 
# WARNING: trying to execute a non-existent command will hang Leo.
#@-at
#@nonl
#@-node:ekr.20040915085351.1:<< about this plugin >>
#@nl
__version__ = '.1'
#@<< imports >>
#@+node:ekr.20040915085715:<< imports >>
import leoGlobals as g
import leoPlugins

from leoNodes import *

import os
import threading
import time

try:
    import Tkinter as Tk
except ImportError:
    Tk = cantImport("Tk")
    
try:
    import weakref
except ImportError:
    weakref = cantImport("weakref")
#@-node:ekr.20040915085715:<< imports >>
#@nl

pr = '@' + 'produce'

#@+others
#@+node:ekr.20040915085814:cantImport
def cantImport (s):
    
    message = "Can not import " + s
    print message
    g.es(message,color="blue")
#@-node:ekr.20040915085814:cantImport
#@+node:ekr.20040915085351.2:makeProduceList & allies
def makeProduceList( c, root = True ):

    pl = []
    if root:
        rvnode = c.rootVnode()
        stopnode = rvnode
    else:
        rvnode = c.currentVnode()
        stopnode = rvnode.next()

    for z in travel(rvnode,stopnode):
        body = z.bodyString()
        body = body.split( '\n' )
        body = filter(teststart, body)
        if body:
            map( lambda i : pl.append( i ), body )
    
    return pl
#@nonl
#@+node:ekr.20040915085351.3:teststart
def teststart( a ):
    return a.startswith( pr )
#@nonl
#@-node:ekr.20040915085351.3:teststart
#@+node:ekr.20040915085351.4:travel
def travel(vn,stopnode):

    while vn:
        yield vn
        vn = vn.threadNext()
        if vn == stopnode:
            vn = None
#@nonl
#@-node:ekr.20040915085351.4:travel
#@-node:ekr.20040915085351.2:makeProduceList & allies
#@+node:ekr.20040915085351.5:exeProduce
def exeProduce(  c, root = True ):

    pl = makeProduceList(c, root)
    # Define the callback with argument bound to p1.
    #@    @+others
    #@+node:ekr.20040915085351.6:runPL
    def runPL(pl=pl):
        f = open( 'produce.log', 'w+' )
        for z in pl:
            if z.startswith(pr):
                z = z.lstrip( pr )
                z = z.lstrip()
                f.write( 'produce: %s\n' % z )
                fi, fo, fe  = os.popen3( z )
                while 1:
                    txt = fo.read()
                    f.write( txt )
                    if txt == '': break
                while 1:
                    txt = fe.read()
                    f.write( txt )
                    if txt == '': break
                fi.close()
                fo.close()
                fe.close() 
                f.write('===============\n' )    
        f.seek( 0 )
        rv = c.rootVnode()
        nv = rv.insertAfter()
        nv.setBodyStringOrPane( f.read() )
        nv.setHeadString( 'produce.log from %s' % time.asctime() )
        f.close()
        os.remove( 'produce.log' )
    #@nonl
    #@-node:ekr.20040915085351.6:runPL
    #@-others
    t = threading.Thread( target = runPL )
    t.setDaemon( True )
    t.start()
#@nonl
#@-node:ekr.20040915085351.5:exeProduce
#@+node:ekr.20040915085351.7:addMenu
def addMenu( tag, keywords ):

    c = g.top()
    if c in haveseen: return

    haveseen[ c ] = None
    men = c.frame.menu
    men = men.getMenu( 'Outline' )
    men2 = Tk.Menu( men , tearoff = 0 )
    men.add_cascade( menu = men2, label = 'Produce' )
    men2.add_command( label = "Execute All Produce", command = lambda  c = c: exeProduce( c ))
    men2.add_command( label = "Execute Tree Produce", command = lambda c = c: exeProduce( c, root = False ) )
#@nonl
#@-node:ekr.20040915085351.7:addMenu
#@-others

if Tk and weakref:
    haveseen = weakref.WeakKeyDictionary()
    leoPlugins.registerHandler( ("start2", "open2", "new") , addMenu )
    g.globalDirectiveList.append( 'produce' ) 
    g.plugin_signon( __name__ )
#@nonl
#@-node:ekr.20040915085351:@thin at_produce.py
#@-leo
