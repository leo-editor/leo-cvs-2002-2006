#@+leo-ver=4-thin
#@+node:ekr.20040331071319:@thin rst2.py
"""A plugin to generate HTML or LaTeX files from reStructured Text
embedded in Leo outlines.

If a headline starts with @rst <filename>, double-clicking on it will 
write a file in outline order, with the headlines converted to reStructuredText 
section headings.

If the name of the <filename> has the extension .html, .htm or .tex, and if you have
docutils installed, it will generate HTML or LaTeX, respectively."""

# By Josef Dalcolmo: contributed under the same licensed as Leo.py itself.

import leoGlobals as g
import leoPlugins

import os

#@<< change log >>
#@+node:ekr.20040331071319.2:<< change log >>
#@+at 
#@nonl
# Change log:
# 
# - JD 2003-03-10 (rev 1.3): some more corrections to the unicode-> encoding translation.
#   No only check for missing docutils (doesn't mask other errors any more).
# 
# - JD 2003-03-11 (rev 1.4): separated out the file launching code to a different pluging.
# 
# - 2003-11-02 Added generation of LaTeX files, just make the extension of the filename '.tex'. --Timo Honkasalo
# 
# - 2003-12-24 S Zatz modifications to introduce concept of plain @rst nodes to improve program documentation
# 
# - 2004-04-08 EKR:
#     - Eliminated "comment" text at start of nodes.
#     - Rewrote code that strips @nocolor, @ignore and @wrap directives from start of text.
#     - Changed code to show explicitly that it uses positions.
#     - Added comments to << define code-block>>
#     - Added div.code-block style to silver_city.css (see documentation)
#     - Rewrote documentation.
#@-at
#@nonl
#@-node:ekr.20040331071319.2:<< change log >>
#@nl

#@+others
#@+node:ekr.20040331071319.3:onIconDoubleClick
# by Josef Dalcolmo 2003-01-13
#
# this does not check for proper filename syntax.
# path is the current dir, or the place @folder points to
# this should probably be changed to @path or so.

def onIconDoubleClick(tag,keywords):

    c = keywords.get("c")
    p = keywords.get("p")
    if not c or not p:
        return
    
    h = p.headString().strip()

    if g.match_word(h,0,"@rst"):
        if len(h) > 5:
            fname = h[5:]
            ext = os.path.splitext(fname)[1].lower()
            if ext in ('.htm','.html','.tex'):
                #@                << write rST as HTML/LaTeX >>
                #@+node:ekr.20040331071319.4:<< write rST as HTML/LaTeX >>
                try:
                    import docutils
                except:
                    g.es('HTML/LaTeX generation requires docutils')
                    return
                else:
                    import docutils.parsers.rst
                    from docutils.core import Publisher
                    from docutils.io import StringOutput, StringInput
                    import StringIO
                    
                # Set the writer and encoding for the converted file
                if ext in ('.html','.htm'):
                    writer='html' ; enc="utf-8"
                else:
                    writer='latex' ; enc="iso-8859-1"
                
                if writer == 'html':
                    try:
                        import SilverCity
                    except:
                        g.es('SilverCity not present so no syntax highlighting')
                        syntax = False
                    else:
                        #@        << define code-block >>
                        #@+node:ekr.20040331071319.5:<< define code-block >>
                        def code_block(name,arguments,options,content,lineno,content_offset,block_text,state,state_machine):
                            
                            """Create a code-block directive for docutils."""
                            
                            # See http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/252170
                            language = arguments[0]
                            module = getattr(SilverCity,language)
                            generator = getattr(module,language+"HTMLGenerator")
                            io = StringIO.StringIO()
                            generator().generate_html(io, '\n'.join(content))
                            html = '<div class="code-block">\n%s\n</div>\n'%io.getvalue()
                            raw = docutils.nodes.raw('',html, format='html') #(self, rawsource='', text='', *children, **attributes):
                            return [raw]
                            
                        # These are documented at http://docutils.sourceforge.net/spec/howto/rst-directives.html.
                        code_block.arguments = (
                            1, # Number of required arguments.
                            0, # Number of optional arguments.
                            0) # True if final argument may contain whitespace.
                        
                        # A mapping from option name to conversion function.
                        code_block.options = {
                            'language' :
                            docutils.parsers.rst.directives.unchanged # Return the text argument, unchanged
                        }
                        
                        code_block.content = 1 # True if content is allowed.
                         
                        # Register the directive with docutils.
                        docutils.parsers.rst.directives.register_directive('code-block',code_block)
                        #@nonl
                        #@-node:ekr.20040331071319.5:<< define code-block >>
                        #@nl
                        syntax = True     
                else:
                    syntax = False
                    
                rstFile = StringIO.StringIO()
                writeTreeAsRst(rstFile, fname, p, c, syntax)
                rstText = rstFile.getvalue()
                
                # This code snipped has been taken from code contributed by Paul Paterson 2002-12-05.
                pub = Publisher()
                pub.source = StringInput(source=rstText)
                pub.destination = StringOutput(pub.settings, encoding=enc)
                pub.set_reader('standalone', None, 'restructuredtext')
                pub.set_writer(writer)
                output = pub.publish()
                
                convertedFile = file(fname,'w')
                convertedFile.write(output)
                convertedFile.close()
                rstFile.close()
                writeFullFileName(fname)
                #@-node:ekr.20040331071319.4:<< write rST as HTML/LaTeX >>
                #@nl
            else:
                #@                << write rST file >>
                #@+node:ekr.20040331071319.6:<< write rST file >>
                rstFile = file(fname,'w')
                writeTreeAsRst(rstFile,fname,p,c)
                rstFile.close()
                writeFullFileName(fname)
                #@nonl
                #@-node:ekr.20040331071319.6:<< write rST file >>
                #@nl
        else:
            # if the headline only contains @rst then open the node and its parent in text editor
            # this works for me but needs to be generalized and should probably be a component
            # of the open_with plugin.
            if 0:
                c.openWith(("os.startfile", None, ".txt"))
                c.selectVnode(p.parent())
                c.openWith(("os.startfile", None, ".tp"))
#@nonl
#@-node:ekr.20040331071319.3:onIconDoubleClick
#@+node:ekr.20040811064922:writeFullFileName
def writeFullFileName (fname):
    
    path = g.os_path_join(os.getcwd(),fname)
    path = g.os_path_abspath(path)
    
    g.es('rst written: ' + path,color="blue")
#@nonl
#@-node:ekr.20040811064922:writeFullFileName
#@+node:ekr.20040331071319.7:writeTreeAsRst
def writeTreeAsRst(rstFile,fname,p,c,syntax):
    
    'Write the tree under position p to the file rstFile (fname is the filename)'
    
    # we don't write a title, so the titlepage can be customized
    # use '#' for title under/overline
    directives = g.scanDirectives(c,p=p) # changed name because don't want to use keyword dict
    #@    << set encoding >>
    #@+node:ekr.20040408160625.1:<< set encoding >>
    encoding = directives.get("encoding",None)
    if encoding == None:
        encoding = c.config.default_derived_file_encoding
    #@nonl
    #@-node:ekr.20040408160625.1:<< set encoding >>
    #@nl
    #@    << set code_dir >>
    #@+node:ekr.20040403202850:<< set code_dir >>
    if syntax:
        lang_dict = {'python':'Python', 'ruby':'Ruby', 'perl':'Perl', 'c':'CPP'}
        language = directives['language']
        # SilverCity modules have first letter in caps
        if language in lang_dict:
            code_dir = '**code**:\n\n.. code-block:: %s\n\n' % lang_dict[language]
        else:
            code_dir = '**code**:\n\n.. class:: code\n..\n\n::\n\n'
    else:
        code_dir = '**code**:\n\n.. class:: code\n..\n\n::\n\n'
    #@nonl
    #@-node:ekr.20040403202850:<< set code_dir >>
    #@nl
    s = g.toEncodedString(fname,encoding,reportErrors=True)
    rstFile.write('.. filename: '+s+'\n')
    rstFile.write('\n')

    s = p.bodyString()
    s = g.toEncodedString(s,encoding,reportErrors=True)
    rstFile.write(s+'\n')		# write body of titlepage.
    rstFile.write('\n')
    
    toplevel = p.level()+1 # Dec 20
    h = p.headString()
    
    for p in p.subtree_iter():
        h = p.headString().strip()
        if g.match_word(h,0,"@rst"):
            #@            << handle an rst node >>
            #@+node:ekr.20040403202850.1:<< handle an rst node >>
            s = p.bodyString()
            s = g.toEncodedString(s,encoding,reportErrors=True)
            
            # Skip any leading @ignore, @nocolor, @wrap directives.
            while (
                g.match_word(s,0,"@ignore") or
                g.match_word(s,0,"@nocolor") or
                g.match_word(s,0,"@wrap")
            ):
                i = g.skip_line(s,0)
                s = s[i:]
                
            rstFile.write('%s\n\n'%s.strip())
            #@-node:ekr.20040403202850.1:<< handle an rst node >>
            #@nl
        else:
            #@            << handle a plain node >>
            #@+node:ekr.20040403202850.2:<< handle a plain node >>
            if g.match_word(h,0,"@file-nosent"):
                h = h[13:]
            h = g.toEncodedString(h,encoding,reportErrors=True)
            
            s = p.bodyString()
            s = g.toEncodedString(s,encoding,reportErrors=True)
            
            rstFile.write(h+'\n')
            rstFile.write(underline(h,p.level()-toplevel))
            rstFile.write('\n')
            
            if s.strip():
                rstFile.write(code_dir)
                s = s.split('\n')
                for linenum,linetext in enumerate(s[:-1]):
                    if "@others" in linetext: #deleting lines with @other directive from output
                        continue
                    rstFile.write('\t%2d  %s\n'%(linenum+1,linetext))
            
            rstFile.write('\n')
            #@nonl
            #@-node:ekr.20040403202850.2:<< handle a plain node >>
            #@nl
#@nonl
#@-node:ekr.20040331071319.7:writeTreeAsRst
#@+node:ekr.20040331071319.8:underline
# note the first character is intentionally unused, to serve as the underline
# character in a title (in the body of the @rst node)

def underline(h,level):
    
    """Return the underlining string to be used at the given level for headline h."""

    str = """#=+*^~"'`-:><_"""[level]

    return str*max(len(h),4)+'\n'
#@nonl
#@-node:ekr.20040331071319.8:underline
#@-others

# Register the handlers...
leoPlugins.registerHandler("icondclick1",onIconDoubleClick)
__version__ = "2.1"
g.plugin_signon(__name__)
#@nonl
#@-node:ekr.20040331071319:@thin rst2.py
#@-leo
