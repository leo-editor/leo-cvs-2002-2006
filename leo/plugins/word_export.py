#@+leo-ver=4-thin
#@+node:EKR.20040517075715.14:@thin word_export.py
"""Formats and exports the selected outline to a Word document.

Make sure word is running with an open (empty) document.

Use the Export menu item to do the actual export.
"""

# Note: the Export menu is a submenu of the Scripts:Word Export menu.

#@@language python
#@@tabwidth -4

__name__ = "Word Export"
__version__ = "0.3"

#@<< version history >>
#@+node:ekr.20040909110753:<< version history >>
#@+at
# 
# 0.3 EKR:
#     - Changed os.path.x to g.os_path_x for better handling of unicode 
# filenames.
#     - Better error messages.
#@-at
#@nonl
#@-node:ekr.20040909110753:<< version history >>
#@nl
#@<< imports >>
#@+node:ekr.20040909105522:<< imports >>
import leoGlobals as g
import leoPlugins

try:
    import win32com.client # From win32 extensions: http://www.python.org/windows/win32/
    client = win32com.client
except ImportError:
    client = None
import ConfigParser
#@nonl
#@-node:ekr.20040909105522:<< imports >>
#@nl

#@+others
#@+node:EKR.20040517075715.15:getConfiguration
def getConfiguration():
    
    """Called when the user presses the "Apply" button on the Properties form"""

    fileName = g.os_path_join(g.app.loadDir,"../","plugins","word_export.ini")
    config = ConfigParser.ConfigParser()
    config.read(fileName)
    return config
#@-node:EKR.20040517075715.15:getConfiguration
#@+node:EKR.20040517075715.16:getWordConnection
def getWordConnection():
    
    """Get a connection to Word"""

    g.es("Trying to connect to Word")
    
    try:
        word = win32com.client.Dispatch("Word.Application")
        return word
    except Exception, err:
        raise
        g.es("Failed to connect to Word",color="blue")
        g.es("Please make sure word is running with an open (empty) document.")
        return None
#@nonl
#@-node:EKR.20040517075715.16:getWordConnection
#@+node:EKR.20040517075715.17:doPara
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
#@-node:EKR.20040517075715.17:doPara
#@+node:EKR.20040517075715.18:writeNodeAndTree
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
    s = g.toEncodedString(s,encoding,reportErrors=True)
    doPara(word, s)
    #
    for i in range(vnode.numberOfChildren()):
        if usesections:
            thishead = "%s%d." % (sectionhead, i+1)
        else:
            thishead = ""
        child = vnode.nthChild(i)
        h = child.headString()
        h = g.toEncodedString(h, encoding, reportErrors=True)
        doPara(word, "%s %s" % (thishead, h), "%s %d" % (header_style, min(level, maxlevel)))
        writeNodeAndTree(word, header_style, level+1, maxlevel, usesections, thishead, child)
#@-node:EKR.20040517075715.18:writeNodeAndTree
#@+node:EKR.20040517075715.19:cmd_Export
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
        g.es("Exception writing Word",color="blue")
        g.es_exception()
#@nonl
#@-node:EKR.20040517075715.19:cmd_Export
#@-others

if client and not g.app.unitTesting:

    # No hooks, we just use the cmd_Export to trigger an export
    g.plugin_signon("word_export")
#@nonl
#@-node:EKR.20040517075715.14:@thin word_export.py
#@-leo
