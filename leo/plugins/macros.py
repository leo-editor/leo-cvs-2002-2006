#@+leo-ver=4-thin
#@+node:ekr.20040916084945:@thin macros.py
"""
Creates new nodes containing parameterized section references.
"""
__version__ = "1.4"
#@<< version history >>
#@+node:ekr.20040916091520:<< version history >>
#@+at
# 
# 1.2 EKR:
#     - Converted to outline.
#     - Use g.angleBrackets to enclose lines with < < and > >.
#     - Use new instead of start2 hook.
#     - onCreate creates a new class for each commander.
#     - Removed all globals.
# 1.3 EKR:
#     - Changed 'new_c' logic to 'c' logic.
# 1.4 EKR:
#     - Replaced tree.begin/endUpdate by c.beginEndUpdate.
#@-at
#@nonl
#@-node:ekr.20040916091520:<< version history >>
#@nl

import leoGlobals as g
import leoPlugins
import re

#@+others
#@+node:ekr.20040916091520.1:onCreate
def onCreate(tag,keywords):
    
    c = keywords.get("c")
    if c:
        paramClass(c)
#@nonl
#@-node:ekr.20040916091520.1:onCreate
#@+node:ekr.20040916091520.2:class paramClass
class paramClass:
    
    #@    @+others
    #@+node:ekr.20040916091520.3:__init__
    def __init__ (self,c):
        
        self.c = c
        self.body = c.frame.body
        self.params = None
        self.pattern = g.angleBrackets(r'\w*?\(([^,]*?,)*?([^,])+?\)') + '$'
        self.regex = re.compile(self.pattern)
    
        self.addMenu()
    #@nonl
    #@-node:ekr.20040916091520.3:__init__
    #@+node:ekr.20040916084945.1:parameterize
    def parameterize(self):
    
        c = self.c
        tree = c.frame.tree
        body = c.frame.body
        current = c.currentVnode()
    
        if not self.params:
            self.params = self.findParameters( current )
            if not self.params: return
    
        sr = body.getAllText()
        sr = sr.split( '\n' )
    
        t = str( body.getInsertionPoint() ).split( '.' )
        sr = sr[ int(t[ 0 ]) - 1]
        sr = sr[ : int( t[ 1 ] ) ]
        sr = sr.rstrip()
        match = self.regex.search( sr )
        if not match: return
    
        sr = sr[ match.start() : match.end() ]
        for z in xrange( current.numberOfChildren() ):
            child = current.nthChild( z )
            if child.headString == sr:
                return
    
        pieces = sr.split( '(' , 1 )
        searchline = pieces[ 0 ] + ">>"
        pieces[ 1 ] = pieces[ 1 ].rstrip('>')
        pieces[ 1 ] = pieces[ 1 ].rstrip( ')' )
        sections = pieces[ 1 ].split( ',' );
    
        node = None
        for z in xrange( self.params.numberOfChildren() ):
            child = self.params.nthChild( z )
            if child.matchHeadline( searchline ):
                node = child
                break
            return
    
        bodys = node.bodyString()
        tn = tnode( bodys , sr )
        c.beginUpdate()
        try:
            v = current.insertAsNthChild( 0 , tn )
            for z in xrange( 0 , len( sections ) ):
                head = g.angleBrackets(str( z + 1) + "$")
                bod = sections[ z ]
                t = tnode( bod , head )
                v.insertAsNthChild( 0 , t )
        finally:
            c.endUpdate()
    #@nonl
    #@-node:ekr.20040916084945.1:parameterize
    #@+node:ekr.20040916084945.2:findParameters
    def findParameters (self,v):
        
        tag = "Parameterized Nodes"
        
        if v.level() != 0:
            rnode = findParameters( v.parent())
    
        bnode = v
        while bnode:
            if bnode.headString() == tag:
                return bnode
            bnode = bnode.back()
    
        nnode = v
        while nnode:
            if nnode.headString() == tag:
                return nnode
            nnode = nnode.next()
    
        return None
    #@nonl
    #@-node:ekr.20040916084945.2:findParameters
    #@+node:ekr.20040916084945.3:addMenu
    def addMenu(self):
        
        c = self.c
        table = ("Parameterize Section Reference",None,self.parameterize),
        c.frame.menu.createMenuItemsFromTable("Outline",table,dynamicMenu=True)
    #@nonl
    #@-node:ekr.20040916084945.3:addMenu
    #@-others
#@nonl
#@-node:ekr.20040916091520.2:class paramClass
#@-others

if 1: # Ok for unit testing: adds command to Outline menu.
    leoPlugins.registerHandler( ('new','open2') ,onCreate)
    g.plugin_signon(__name__)
#@nonl
#@-node:ekr.20040916084945:@thin macros.py
#@-leo
