#@+leo-ver=4-thin
#@+node:ekr.20050217091823:@thin bibtex.py
"""Manage BibTeX files with Leo.

Create a bibliographic database by putting '@bibtex filename' in a headline.
Entries are added as nodes, with '@entrytype key' as the headline (for example
'@book jones99'), and the contents of the entry in the body text. The file is
written by double-clicking the node.

Strings are defined in @string nodes and they can contain multiple entries. 
All @string nodes are written at the start of the file.

BibTeX files can be imported by creating an empty node with '@bibtex filename'
in the headline. Double-clicking it will read the file 'filename' and parse it
into a @bibtex tree.
"""

#@@language python
#@@tabwidth -4

# By Timo Honkasalo: contributed under the same license as Leo.py itself.



#@<< about this plugin >>
#@+node:ekr.20050217091823.1:<<about this plugin >>
#@+at 
#@nonl
# This plugin can be used to manage BibTeX files with Leo.
# 
# Create a bibliographic database by putting '@bibtex filename' in a headline. 
# Entries are added as nodes, with '@entrytype key' as the headline, and the 
# contents of the entry in body text. The plugin will automatically insert a 
# template for the entry in the body pane when a new entry is created (hooked 
# to pressing enter when typing the headline text). The templates are defined 
# in dictionary 'templates' in the <<globals>> section, by default containing 
# all required fields for every entry.
# 
# The file is written by double-clicking the node. Thus the following outline:
# 
# -@bibtex biblio.bib
#  +@book key
#   author = {A. Uthor},
#   year = 1999
# 
# 
# will be written in the file 'biblio.bib' as:
# 
#  @book{key,
#  author = {A. Uthor},
#  year= 1999}
# 
# Strings are defined in @string nodes and they can contain multiple entries.
# All @string nodes are written at the start of the file. Thus the following
# outline:
# 
# -@bibtext biblio.bib
#  +@string
#   j1 = {Journal1}
#  +@article AUj1
#   author = {A. Uthor},
#   journal = j1
#  +@string
#   j2 = {Journal2}
#   j3 = {Journal3}
# 
# 
# Will be written as:
# 
#  @string{j1 = {Journal1}}
#  @string{j2 = {Journal2}}
#  @string{j3 = {Journal3}}
# 
#  @article{AUj1,
#  author = {A. Uthor},
#  journal = j1}
# 
# No error checking is made on the syntax. The entries can be organised under
# nodes --- if the headline doesn't start with '@', the headline and body text
# are ignored, but the child nodes are parsed as usual.
# 
# BibTeX files can be imported by creating an empty node with '@bibtex 
# filename'
# in the headline. Double-clicking it will read the file 'filename' and parse 
# it
# into a @bibtex tree. No syntax checking is made, 'filename' is expected to 
# be a valid BibTeX file.
# 
#@-at
#@nonl
#@-node:ekr.20050217091823.1:<<about this plugin >>
#@nl
__version__ = "0.3" # Set version for the plugin handler.
#@<< change log >>
#@+node:ekr.20050217091823.2:<<change log>>
#@+at 
#@nonl
# Change log:
# 
# 0.1 @bibtex nodes introduced, writing the contents in a BibTeX format.
#     Timo Honkasalo 2005/02/13
# 0.2 Importing BibTeX files added.
#     Timo Honkasalo 2005/02/14
# 0.3 Automatic inserting of templates when new entries are created.
#     Timo Honkasalo 2005/02/15
#@-at
#@-node:ekr.20050217091823.2:<<change log>>
#@nl
#@<< imports >>
#@+node:ekr.20050217091823.3:<<imports>>
import leoGlobals as g
import leoPlugins

import os
#@nonl
#@-node:ekr.20050217091823.3:<<imports>>
#@nl
#@<< globals >>
#@+node:ekr.20050217091823.4:<<globals>>
templates = {'@article':'author = {}\ntitle = {}\njournal = {}\nyear =',
             '@book':'author = {}\ntitle = {}\npublisher = {}\nyear =',
             '@booklet':'title = {}',
             '@conference':'author = {}\ntitle = {}\nbooktitle = {}\nyear =',
             '@inbook':'author = {}\ntitle = {}\nchapter = {}\npublisher = {}\nyear =',
             '@incollection':'author = {}\ntitle = {}\nbooktitle = {}\npublisher = {}\nyear =',
             '@inproceedings':'author = {}\ntitle = {}\nbooktitle = {}\nyear =',
             '@manual':'title = {}',
             '@mastersthesis':'author = {}\ntitle = {}\nschool = {}\nyear =',
             '@misc':'',
             '@phdthesis':'author = {}\ntitle = {}\nschool = {}\nyear =',
             '@proceedings':'title = {}\nyear =',
             '@techreport':'author = {}\ntitle = {}\ninstitution = {}\nyear =',
             '@unpublished':'author = {}\ntitle = {}\nnote = {}'
             }
#@nonl
#@-node:ekr.20050217091823.4:<<globals>>
#@nl
#@<< to do >>
#@+node:ekr.20050217091823.5:<<to do>>
#@+at 
#@nonl
# To do list (in approximate order of importance):
# 
# - Translating between non-ascii characters and LaTeX code when 
# reading/writing
# - Checking for duplicate keys
# - Customisable config file (for defining the templates)
# - Import/write in BibTeXml format
# - Sorting by chosen fields
# - Import/write in other bibliographic formats
# - Expanding strings
#@-at
#@-node:ekr.20050217091823.5:<<to do>>
#@nl

#@+others
#@+node:ekr.20050217091823.6:onIconDoubleClick
#
# this does not check for proper filename syntax.
# path is the current dir, or the place @folder points to
# this should probably be changed to @path or so.

def onIconDoubleClick(tag,keywords):
    """Read or write a bibtex file when the node is double-clicked.
    
    Write the @bibtex tree as bibtex file when the root node is double-clicked. 
    If it has no child nodes, read bibtex file."""
    
    v = keywords.get("p") or keywords.get("v")
    c = keywords.get("c")
    h = v.headString().strip()
    if g.match_word(h,0,"@bibtex"):
        fname = h[8:]
        if v.hasChildren():
            #@            << write bibtex file >>
            #@+node:ekr.20050217091823.8:<< write bibtex file >>
            bibFile = file(fname,'w')
            writeTreeAsBibTex(bibFile, v, c)
            
            bibFile.close()
            g.es('written: '+str(fname))
            #@nonl
            #@-node:ekr.20050217091823.8:<< write bibtex file >>
            #@nl
        else:
            #@            << read bibtex file >>
            #@+node:ekr.20050217091823.7:<< read bibtex file >>
            g.es('reading: ' + str(fname))
            try: 
                bibFile = file(fname,'r')
            except IOError:
                g.es('IOError: file not found')
                return    
            readBibTexFileIntoTree(bibFile, c)
            
            bibFile.close()
            #@-node:ekr.20050217091823.7:<< read bibtex file >>
            #@nl
       
               
#@-node:ekr.20050217091823.6:onIconDoubleClick
#@+node:ekr.20050217091823.9:onHeadKey
def onHeadKey(tag,keywords):
    """Write template for the entry in body pane.
    
    If body pane is empty, get template for the entry from a dictionary 'templates ' and write it in the body pane."""
    # checking for duplicate keys will be also done in this function (to be implemented).
    
    v = keywords.get("p") or keywords.get("v")
    c = keywords.get("c")
    h = v.headString().strip()
    ch = keywords.get("ch")
    if (ch == '\r') and (h[:h.find(' ')] in templates.keys()) and (not v.bodyString()):
        for p in v.parents_iter():
            if p.headString()[:8] == '@bibtex ':
                #@                << write template >>
                #@+node:ekr.20050217091823.10:<< write template >>
                v.setBodyStringOrPane(templates[h[:h.find(' ')]])
                return
                #@nonl
                #@-node:ekr.20050217091823.10:<< write template >>
                #@nl
                
       
#@nonl
#@-node:ekr.20050217091823.9:onHeadKey
#@+node:ekr.20050217091823.11:writeTreeAsBibTex
def writeTreeAsBibTex(bibFile, vnode, c):
    'Write the tree under vnode to the file bibFile'
    # body text of @bibtex node is ignored
    dict = g.scanDirectives(c,p=vnode)
    encoding = dict.get("encoding",None)
    if encoding == None:
        encoding = g.app.config.default_derived_file_encoding
    
    toplevel = vnode.level()
    stopHere = vnode.nodeAfterTree()
    v = vnode.threadNext()
    strings = ''
    entries = ''
    # repeat for all nodes in this tree
    while v != stopHere:
        h = v.headString()
        h = g.toEncodedString(h,encoding,reportErrors=True)
        if h[0]=='@':
            s = v.bodyString()
            s = g.toEncodedString(s,encoding,reportErrors=True)
            if h == '@string': # store string declarations in strings
                for i in s.split('\n'):
                    if i and (not i.isspace()):
                         strings = strings + '@string{' + i + '}\n'
            else:  # store other stuff in entries  
                entries = entries + h[:h.find(' ')] + '{' + h[h.find(' ')+1:]+  ',\n' + s + '}\n\n'
        v = v.threadNext()
    if strings:
        bibFile.write(strings + '\n\n')
    bibFile.write(entries)  
#@nonl
#@-node:ekr.20050217091823.11:writeTreeAsBibTex
#@+node:ekr.20050217091823.12:readBibTexFileIntoTree
def readBibTexFileIntoTree(bibFile, c):
    """Read BibTeX file and parse it into @bibtex tree
    
    The file is split at '@'s and each section is divided into headline ('@string' in strings and '@entrytype key' in others) and body text (without outmost braces). These are stored in biblist, which is a list of tuples ('headline','body text') for each entry, all the strings in the first element. For each element of biblist, a vnode is created and headline and body text put into place."""
    
    entrylist = []
    strings = ''
    biblist = []
    for i in bibFile.read().split('@')[1:]:
        if i[:6] == 'string':
            strings = strings + i[7:].strip()[:-1] + '\n'
        else: 
            entrylist.append(('@' + i[:i.find(',')].replace('{',' ').replace('(',' ').replace('\n',''),i[i.find(',')+1:].rstrip().lstrip('\n')[:-1]))
    if strings:
        biblist.append(('@string',strings)) 
    biblist = biblist+entrylist
    if biblist:
        c.doCommand(c.insertHeadline,'')
        c.doCommand(c.moveOutlineRight,'')
        v=c.currentPosition()
        v.setHeadStringOrHeadline(str(biblist[0][0]))
        v.setBodyStringOrPane(str(biblist[0][1]))
        for i in biblist[1:]:
            c.doCommand(c.insertHeadline,'')
            v=c.currentPosition()
            v.setHeadStringOrHeadline(str(i[0]))
            v.setBodyStringOrPane(str(i[1]))
        



#@-node:ekr.20050217091823.12:readBibTexFileIntoTree
#@-others

if not g.app.unitTesting:

    # Register the handlers...
    leoPlugins.registerHandler("icondclick1",onIconDoubleClick)
    leoPlugins.registerHandler("headkey2",onHeadKey)
    g.plugin_signon(__name__)
#@nonl
#@-node:ekr.20050217091823:@thin bibtex.py
#@-leo
