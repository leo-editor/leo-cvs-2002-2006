#@+leo-ver=4-thin
#@+node:ekr.20041011102931:@thin xsltWithNodes.py
"""Adds XSLT-Node Command submen item to the Outline menu.

This menu contains the following items:
    
- Set StyleSheet Node:
    - Selects the current node as the xsl stylesheet the plugin will use.

- Process Node with Stylesheet Node:
    - Processes the current node as an xml document,
      resolving section references and Leo directives.
    - Creates a sibling containing the results.

Requires 4Suite 1.0a3 or better, downloadable from http://4Suite.org.
"""

#@@language python
#@@tabwidth -4

#@<< imports >>
#@+node:ekr.20041011105212:<< imports >>
import leoGlobals as g
import leoNodes
import leoPlugins

try:
    import Ft
    from Ft.Xml import InputSource 
    from Ft.Xml.Xslt.Processor import Processor
except ImportError:
    Ft = g.cantImport("Ft")

try:
    import Tkinter as Tk
except ImportError:
    Tk = g.cantImport("Tk")

import weakref 
import cStringIO 

#@-node:ekr.20041011105212:<< imports >>
#@nl
__version__ = "0.2"
#@<< version history >>
#@+node:ekr.20041011105658:<< version history >>
#@+at
# 
# 0.1: Original code.
# 
# 0.2 EKR: Converted to outline.
#@-at
#@nonl
#@-node:ekr.20041011105658:<< version history >>
#@nl
new_at_file = True

stylenodes = weakref.WeakKeyDictionary()
haveseen = weakref.WeakKeyDictionary()

#@+others
#@+node:ekr.20041011103436:setStyleNode
def setStyleNode (c):

    stylenodes[c] = c.currentPosition()
#@nonl
#@-node:ekr.20041011103436:setStyleNode
#@+node:ekr.20041011103436.1:processDocumentNode
def processDocumentNode (c):
    
    c.beginUpdate()
    try:
        if not styleNodeSelected(c):return
        proc = Processor()
        stylenode = stylenodes[c]
        pos = c.currentPosition()
        c.selectPosition(stylenode)
        sIO = getStream(c)
        hstring = str(stylenode.headString())
        if hstring=="":hstring = "no headline"
        stylesource = InputSource.DefaultFactory.fromStream(sIO,uri=hstring)
        proc.appendStylesheet(stylesource)
        c.selectPosition(pos)
        xmlnode = pos.v.t
        xIO = getStream(c)
        xhead = str(xmlnode.headString)
        if xhead=="":xhead = "no headline"
        xmlsource = InputSource.DefaultFactory.fromStream(xIO,uri=xhead)
        result = proc.run(xmlsource)
        nhline = "xsl:transform of "+str(xmlnode.headString)
        tnode = leoNodes.tnode(result,nhline)
        pos.insertAfter(tnode)
        
    except Exception, x:
        g.es('exception '+str(x))
    c.endUpdate()
#@nonl
#@-node:ekr.20041011103436.1:processDocumentNode
#@+node:ekr.20041011103436.2:addXSLTNode
def addXSLTNode (c):
    
    pos = c.currentPosition()
    
    #body = '''<?xml version="1.0"?>'''
   # body = '''<?xml version="1.0"?>
#<xsl:transform xmlns:xsl="http:///www.w3.org/1999/XSL/Transform" version="1.0">'''

    body = '''<?xml version="1.0"?>
<xsl:transform xmlns:xsl="http:///www.w3.org/1999/XSL/Transform" version="1.0">    
</xsl:transform>'''

    tnode = leoNodes.tnode(body,"xslt stylesheet")
    c.beginUpdate()
    pos.insertAfter(tnode)
    c.endUpdate()
#@-node:ekr.20041011103436.2:addXSLTNode
#@+node:ekr.20041011103436.3:addXSLTemplate
def addXSLTemplate (c):

    bodyCtrl = c.frame.bodyCtrl
    template = '''<xsl:template match="">'''
    template = '''<xsl:template match="">
</xsl:template>'''

    bodyCtrl.insert('insert',template)
    bodyCtrl.event_generate('<Key>')
    bodyCtrl.update_idletasks()
#@nonl
#@-node:ekr.20041011103436.3:addXSLTemplate
#@+node:ekr.20041011103436.5:getStream
def getStream (c):

    at = c.atFileCommands
    pos = c.currentPosition()
    cS = cStringIO.StringIO()
    
    if new_at_file: # 4.3 code base.
        at.toStringFlag = True
        # at.outputFile = cS 
        at.writeOpenFile(pos,nosentinels=True,toString=True)
        # at.outputFile = None 
        # at.toStringFlag = False 

    else: # 4.2 code base
        at.new_df.toStringFlag = True
        at.new_df.outputFile = cS
        at.new_df.writeOpenFile(pos,nosentinels=True,toString=True)
        at.new_df.outputFile = None
        at.new_df.toStringFlag = False

    cS.seek(0)
    return cS
#@nonl
#@-node:ekr.20041011103436.5:getStream
#@+node:ekr.20041011103436.6:jumpToStyleNode
def jumpToStyleNode (c):

    if not styleNodeSelected(c):return
    pos = stylenodes[c]

    c.beginUpdate()
    c.selectPosition(pos)
    c.endUpdate()
#@nonl
#@-node:ekr.20041011103436.6:jumpToStyleNode
#@+node:ekr.20041011103436.7:styleNodeSelected
def styleNodeSelected (c):

    if not stylenodes.has_key(c):
        g.es("No Style Node selected")
        return False

    return True
#@nonl
#@-node:ekr.20041011103436.7:styleNodeSelected
#@+node:ekr.20041011103436.8:addMenu
def addMenu (tag,keywords):
    c = g.top()
    if haveseen.has_key(c): return
    haveseen[c] = None 
    menu = c.frame.menu 
    menu = menu.getMenu('Outline')
    xmen = Tk.Menu(menu,tearoff=False)
    xmen.add_command(
        label="Set Stylesheet Node",
        command=lambda c=c:setStyleNode(c))
    xmen.add_command(
        label="Jump To Style Node",
        command=lambda c=c:jumpToStyleNode(c))
    xmen.add_command(
        label="Process Node with Stylesheet Node",
        command=lambda c=c:processDocumentNode(c))
    xmen.add_separator()
    xmen.add_command(
        label="Create Stylesheet Node",
        command=lambda c=c:addXSLTNode(c))
    xmen.add_command(
        label="Insert <xsl:template> elements",
        command=lambda c=c:addXSLTemplate(c))
    menu.add_cascade(
        menu=xmen,
        label="XSLT-Node Commands")
#@nonl
#@-node:ekr.20041011103436.8:addMenu
#@-others

if Ft and Tk:
    leoPlugins.registerHandler(('start2','open2',"new"),addMenu)
    g.plugin_signon(__name__)
#@nonl
#@-node:ekr.20041011102931:@thin xsltWithNodes.py
#@-leo
