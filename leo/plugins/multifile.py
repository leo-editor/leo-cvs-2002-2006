#@+leo-ver=4-thin
#@+node:mork.20041018204908.1:@thin multifile.py
#@<< docstring >>
#@+node:ekr.20050226114732:<< docstring >>
'''Multipath enables the ability to write a file to multiple locations.

It acts as a post-write mechanism, a file must be written to the filesystem for
it to work. At this point it is not a replacement for @path or an absolute path,
it works in tandem with them.

To use, place @multipath at the start of a line in the root node or an ancestor
of the node. The format is (On Unixy systems)::
    
    @multipath /machine/unit/:/machine/robot/:/machine/
    
It will places copy of the written file in each of these directories.

There is an additional directive that simplifies common paths, it is called
@multiprefix. By typing @multiprefix with a path following it, before a
@multipath directive you set the beginning of the paths in the @multipath
directive.

For example: (note I put # in front of the directives here because I
dont want someone browsing this file to accidentilly save mulitple copies of
this file to their system :) )

#@verbatim
#@multiprefix /leo #@multipath /plugins 

or

#@verbatim
#@multiprefix /leo/
#@verbatim
#@multipath plugins: fungus : drain

copies a file to /leo/plugins /leo/fungus /leo/drain.

The @multiprefix stays in effect for the entire tree until reset with another
@multiprefix directive. @multipath is cumulitive, in that for each @multipath in
an ancestor a copy of the file is created. These directives must at the
beginning of the line and by themselves.
'''
#@nonl
#@-node:ekr.20050226114732:<< docstring >>
#@nl

#@@language python
#@@tabwidth -4

#@<< imports >>
#@+node:ekr.20050226114732.1:<< imports >>
from leoPlugins import *   
import leoGlobals as g 
from leoNodes import *     
from leoAtFile import *   
import shutil
import new
import os.path

try:
    import tkFileDialog
    import weakref
    ok = True
except ImportError:
    ok = False
#@nonl
#@-node:ekr.20050226114732.1:<< imports >>
#@nl

__version__ = ".5"
#@<< version history >>
#@+node:ekr.20050226115130:<< version history >>
#@@killcolor

#@+at
# 
# 0.3 EKR:
#     - Added init method.
#     - Minor code reorg.  The actual code is unchanged.
# 
# 0.4 EKR:
#     - Changed 'new_c' logic to 'c' logic.
# 
# 0.5 EKR:
#     - Use 'new' and 'open2' hooks to call addMenu.
#@-at
#@nonl
#@-node:ekr.20050226115130:<< version history >>
#@nl

multiprefix = '@multiprefix'   
multipath = '@multipath'
haveseen = {}   
files = {}

#@+others
#@+node:ekr.20050226115130.1:init
def init ():
    
    if ok:
        g.globalDirectiveList.append( 'multipath' ) 
        g.globalDirectiveList.append( 'multiprefix' ) 
        registerHandler( 'save1' , start )
        registerHandler( 'save2', stop )
        registerHandler(('new', 'start2'),addMenu )
        g.plugin_signon(__name__)  

    return ok
#@nonl
#@-node:ekr.20050226115130.1:init
#@+node:mork.20041018204908.3:decoratedOpenWriteFile
def decoratedOpenWriteFile( self,root,toString):
    
    oWF = haveseen[ root.c ]  
    rt = oWF( root, toString ) 
    if root.isDirty(): files[ self.targetFileName ] = root.copy()
    return rt
#@nonl
#@-node:mork.20041018204908.3:decoratedOpenWriteFile
#@+node:mork.20041018204908.4:start
def start( tag , keywords ):
 
    c = keywords.get('c')
    if not haveseen.has_key( c ): 
        ndf = c.atFileCommands.new_df
        haveseen[ c ] = ndf.openWriteFile
        ndf.openWriteFile = new.instancemethod( decoratedOpenWriteFile, ndf, ndf.__class__ )
#@nonl
#@-node:mork.20041018204908.4:start
#@+node:mork.20041018204908.5:scanForMultiPath
def scanForMultiPath():
    multi = {}
    for z in files.keys():
        pos = files[ z ]
        order = []
        map( order.append, pos.self_and_parents_iter( True ) )
        order.reverse()
        prefix = ''
        for pos in order:
            txt = pos.bodyString().split('\n')
            for t in txt:
                if t.startswith( multiprefix ):
                    prefix = t.lstrip( multiprefix ).strip()
                elif t.startswith( multipath ):
                    if not multi.has_key( z ):
                        multi[ z ] = []
                    paths = t.lstrip( multipath ).strip().split(':')
                    paths =[ prefix + x.strip() for x in paths ]
                    [ multi[ z ].append( x ) for x in paths ]                     
    return multi    
#@-node:mork.20041018204908.5:scanForMultiPath
#@+node:mork.20041018204908.6:stop
def stop( tag, keywords ):

    multi = scanForMultiPath()  
    for z in multi.keys():
        paths = multi[ z ]
        for x in paths:
            try:
                if os.path.isdir( x ):
                    shutil.copy2( z , x )
                    g.es( "multifile:\nWrote %s to %s" % ( z, x ), color = "blue" )
                else:
                    g.es( "multifile:\n%s is not a directory, not writing %s" %( x, z ), color = "red" )
            except:
                g.es( "multifile:\nCant write %s to %s" % ( z,x ), color = "red" )  
    files.clear()
#@nonl
#@-node:mork.20041018204908.6:stop
#@+node:mork.20041019091317:addMenu
haveseen = weakref.WeakKeyDictionary()

def addMenu( tag, keywords ):
    
    c = keywords.get('c')
    if not c or haveseen.has_key( c ):
        return
    haveseen[ c ] = None
    men = c.frame.menu
    men = men.getMenu( 'Edit' )
    men.add_command(
        label = "Insert Directory String", 
        command = lambda c = c: insertDirectoryString( c ) )
#@nonl
#@-node:mork.20041019091317:addMenu
#@+node:mork.20041019091524:insertDirectoryString
def insertDirectoryString( c ):
    
    dir = tkFileDialog.askdirectory()
    if dir:
        
        bodyCtrl = c.frame.body.bodyCtrl
        bodyCtrl.insert( 'insert', dir )
        bodyCtrl.event_generate( '<Key>' )
        bodyCtrl.update_idletasks()
#@nonl
#@-node:mork.20041019091524:insertDirectoryString
#@-others
#@nonl
#@-node:mork.20041018204908.1:@thin multifile.py
#@-leo
