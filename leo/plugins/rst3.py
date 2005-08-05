#@+leo-ver=4-thin
#@+node:ekr.20040331071319:@thin rst3.py
#@<< docstring >>
#@+node:ekr.20050420105800:<< docstring >>
'''A plugin to generate HTML or LaTeX files from reStructured Text embedded in
Leo outlines.

If a headline starts with @rst <filename>, double-clicking on it will write a
file in outline order.

If the name of the <filename> has the extension .html, .htm or .tex, and if you have
docutils installed, it will generate HTML or LaTeX, respectively.

There are many possible options:

- Headlines may be converted to section headings.
'''
#@nonl
#@-node:ekr.20050420105800:<< docstring >>
#@nl

# By Josef Dalcolmo: contributed under the same licensed as Leo.py itself.

#@<< imports >>
#@+node:ekr.20050420105800.1:<< imports >>
import leoGlobals as g
import leoPlugins

import os
import ConfigParser
import HTMLParser
import pprint
import StringIO
import sys

# Make sure the present directory in in sys.path.
dir,junk = os.path.split(__file__)
if dir not in sys.path: sys.path.append(dir)
        
try:
    import mod_http
except ImportError:
    mod_http = None
    
try:
    import docutils
    import docutils.parsers.rst
    # from docutils.core import Publisher
    from docutils.io import StringOutput, StringInput, FileOutput,FileInput
except ImportError:
    docutils = None
    
try:
    import SilverCity
except ImportError:
    SilverCity = None
#@-node:ekr.20050420105800.1:<< imports >>
#@nl
#@<< change log >>
#@+node:ekr.20040331071319.2:<< change log >>
#@+at 
#@nonl
# Change log:
# 
# - JD 2003-03-10 (rev 1.3): some more corrections to the unicode-> encoding 
# translation.
#   No only check for missing docutils (doesn't mask other errors any more).
# 
# - JD 2003-03-11 (rev 1.4): separated out the file launching code to a 
# different pluging.
# 
# - 2003-11-02 Added generation of LaTeX files, just make the extension of the 
# filename '.tex'. --Timo Honkasalo
# 
# - 2003-12-24 S Zatz modifications to introduce concept of plain @rst nodes 
# to improve program documentation
# 
# - 2004-04-08 EKR:
#     - Eliminated "comment" text at start of nodes.
#     - Rewrote code that strips @nocolor, @ignore and @wrap directives from 
# start of text.
#     - Changed code to show explicitly that it uses positions.
#     - Added comments to << define code-block>>
#     - Added div.code-block style to silver_city.css (see documentation)
#     - Rewrote documentation.
# 2.2 EKR 2005-03-07 changed publish() to publish(argv=[''])
# 
# 2.3 bwmulder
#     - added various options which can be set with @settings directive
#     - add support for mod_http plugin.
#     - added possible settings to the beginning of the Leo file
# 2.4 EKR:
#     - Call onFileOpen from both "new" and "open2" hooks.
# 2.5 EKR:
#     - Added init method.
#@-at
#@nonl
#@-node:ekr.20040331071319.2:<< change log >>
#@nl

#@+others
#@+node:ekr.20050802091909:Module level
#@+node:ekr.20050802084255: init
def init ():

    ok = True # Ok for unit testing.

    ## leoPlugins.registerHandler("icondclick1",processTree)
    leoPlugins.registerHandler(("new","open2"), onCreate)
    __version__ = "2.4"

    g.plugin_signon(__name__)
    return ok
#@nonl
#@-node:ekr.20050802084255: init
#@+node:bwmulder.20050320000243:onCreate
def onCreate(tag, keywords):
    c = keywords.get('new_c') or keywords.get('c')
    if c:
        rstClass(c)
#@nonl
#@-node:bwmulder.20050320000243:onCreate
#@+node:ekr.20040331071319.5:code_block
def code_block(name,arguments,options,content,lineno,content_offset,block_text,state,state_machine):
    
    '''Create a code-block directive for docutils.'''
    
    # See http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/252170
    language = arguments[0]
    module = getattr(SilverCity,language)
    generator = getattr(module,language+"HTMLGenerator")
    io = StringIO.StringIO()
    generator().generate_html(io, '\n'.join(content))
    html = '<div class="code-block">\n%s\n</div>\n'%io.getvalue()
    raw = docutils.nodes.raw('',html, format='html')
    return [raw]
    
# These are documented at http://docutils.sourceforge.net/spec/howto/rst-directives.html.
code_block.arguments = (
    1, # Number of required arguments.
    0, # Number of optional arguments.
    0) # True if final argument may contain whitespace.

# A mapping from option name to conversion function.
code_block.options = {
    'language' :
    docutils.parsers.rst.directives.unchanged # Return the text argument, unchanged.
}

code_block.content = 1 # True if content is allowed.
 
# Register the directive with docutils.
docutils.parsers.rst.directives.register_directive('code-block',code_block)
#@nonl
#@-node:ekr.20040331071319.5:code_block
#@-node:ekr.20050802091909:Module level
#@+node:ekr.20050802091909.1:class rstClass
class rstClass:
    
    '''A class to write rst markup in Leo outlines.'''
    
#@+at 
#@nonl
# This plugin optionally stores information for the http plugin.
# 
# Each node can have one additional attribute, with the name 
# rst_http_attributename, which is a list.
# 
# The first three elements are stack of tags, the rest is html code.
# 
# [<tag n start>, <tag n end>, <other stack elements>, <html line 1>, <html 
# line 2>, ...]
# 
# <other stack elements has the same structure:
#     [<tag n-1 start>, <tag n-1 end>, <other stack elements>]
#@-at
#@@c
    
    #@    @+others
    #@+node:ekr.20050802091909.2: Birth
    #@+node:ekr.20050802091909.3: ctor
    def __init__ (self,c):
        
        global SilverCity
        
        self.c = c
        #@    << init ivars >>
        #@+node:ekr.20050802135411:<< init ivars >>
        # Debugging...
        self.rst2_debug_anchors = False
        self.debug_before_and_after_replacement = False
        self.debug_handle_endtag = False
        self.debug_handle_starttag = False
        self.debug_node_html_1 = False
        debug_show_unknownattributes = False
        self.debug_store_lines = False
        
        self.encoding = 'utf-8'
        # A node anchor is a marker beginning with node_begin_marker.
        # We assume that such markers do not occur in the rst document.
        self.http_map = {}
        self.last_marker = None
        self.node_counter = 0
        self.use_alternate_code_block = SilverCity is None
        
        # Set default values for options.
        self.add_menu_item = True
        self.clear_http_attributes = False
        self.http_server_support = False
        self.massage_body = False
        self.format_headlines = False
        self.write_pure_document = False
        self.use_file = False
        
        self.node_begin_marker = 'http-node-marker-'
        self.http_attributename = 'rst_http_attribute'
        #@nonl
        #@-node:ekr.20050802135411:<< init ivars >>
        #@nl
        
        self.applyConfiguration() ### This will become a pre-pass.
    
        if self.add_menu_item:
            self.addMenu()
    
        if c.config.getBool("rst2_run_on_open_window"):
            self.runOnOpen()
    #@nonl
    #@-node:ekr.20050802091909.3: ctor
    #@+node:bwmulder.20050327204614:addMenu
    def addMenu(self):
        
        c = self.c ; editMenu = c.frame.menu.getMenu('Edit')
        
        def callback():
            self.processTree(c.currentPosition())
                
        table = (
            ("-", None, None),
            ("Write Restructed Text", "", callback),
        )
            
        c.frame.menu.createMenuEntries(editMenu, table)
    #@nonl
    #@-node:bwmulder.20050327204614:addMenu
    #@+node:bwmulder.20050314131619:applyConfiguration
    def applyConfiguration (self):
    
        c = self.c
    
        
        self.getBool    ("clear_http_attributes",   'rst2_clear_http_attributes')
        self.getBool    ('format_headlines',        'rst2_format_headlines')
        self.getString  ('http_attributename',      'rst2_http_attributename')
        self.getBool    ('http_server_support',     'rst2_http_server_support')
        self.getBool    ('massage_body',            'rst2_massage_body')
        self.getString  ('node_begin_marker',       'rst2_node_begin_marker')
        self.getBool    ('use_file',                'rst2_use_file')
        self.getBool    ('write_pure_document',     'rst2_write_pure_document')
        
        if self.http_server_support and not mod_http:
            g.es('No http_server_support: can not import mod_http plugin',color='red')
            self.http_server_support = False
    #@nonl
    #@-node:bwmulder.20050314131619:applyConfiguration
    #@+node:ekr.20050802095216:runOnOpen  DELETE???
    def runOnOpen (self):
        
        g.trace()
        c = self.c
        ignoreset = {} ; http_map = {} ; anchormap = {}
        self.node_counter = 0 ; found = False
        
        for p in c.allNodes_iter():
            if p.v in self.ignoreset:
                continue
            s = p.headString()
            if s.startswith("@rst ") and len(s.split()) >= 2:
                for p1 in p.subtree_iter():
                    ignoreset[p1.v] = True
                try:
                    self.http_map = {}
                    self.anchormap = {}
                    self.processTree(p)
                    http_map.update(self.http_map)
                    anchormap.update(self.anchormap)
                    found = True
                except Exception:
                    g.es("Formatting failed for %s" % p, color='red')
                    g.es_exception()
        if found:
            self.http_map = http_map
            self.anchormap = anchormap
            relocate_references() 
            self.http_map = None
            self.anchormap = None
            g.es('html updated for html plugin', color="blue")
        if self.clear_http_attributes:
            g.es("http attributes cleared")
    #@nonl
    #@-node:ekr.20050802095216:runOnOpen  DELETE???
    #@+node:ekr.20050802093209.1:getboolean & getString
    def getBool(self,ivar_name,setting_name):
        
        c = self.c
        newvalue = c.config.getBool(setting_name)
    
        if newvalue is not None:
            setattr(self, ivar_name, newvalue)
            
    def getString(self,ivar_name,setting_name):
        
        c = self.c
        newvalue = c.config.getString(setting_name)
    
        if newvalue is not None:
            setattr(self, ivar_name, newvalue)
    #@nonl
    #@-node:ekr.20050802093209.1:getboolean & getString
    #@-node:ekr.20050802091909.2: Birth
    #@+node:ekr.20050802141932:encode
    def encode (self,s):
            
        return g.toEncodedString(s,encoding=self.encoding,reportErrors=True)
    #@nonl
    #@-node:ekr.20050802141932:encode
    #@+node:ekr.20040331071319.3:processTree & helpers
    # by Josef Dalcolmo 2003-01-13
    
    # this does not check for proper filename syntax.
    # path is the current dir, or the place @folder points to
    # this should probably be changed to @path or so.
    
    def processTree(self,p):
    
        c = self.c ; h = p.headString().strip()
    
        self.applyConfiguration(c)
    
        if g.match_word(h,0,"@rst"):
            if len(h) > 5:
                name = h[5:]
                junk,ext = g.os_path_splitext(name)
                ext = ext.lower()
                if ext in ('.htm','.html','.tex'):
                    if docutils:
                        self.writeSpecialTree(p,name,ext)
                    else:
                        g.es("Can't generate %s: can not import docutils" % (name),color='red')
                else:
                    theFile = file(name,'w')
                    self.writeTree(theFile,name,p)
                    self.report(name)
    #@nonl
    #@+node:bwmulder.20041011145032:massageBody
    def massageBody (self,p):
        
        '''Remove @ignore, @nocolor and @wrap directives.'''
    
        s = p.bodyString()
    
        while (s.startswith("@ignore") or
               s.startswith("@nocolor") or
               s.startswith("@wrap")):
           i = g.skip_line(s,0)
           s = s [i:]
    
        return s
    #@nonl
    #@-node:bwmulder.20041011145032:massageBody
    #@+node:ekr.20040331071319.8:underlineString
    # The first character is intentionally unused, to serve as the underline
    # character in a title (in the body of the @rst node)
    
    def underlineString (self,h,level):
    
        '''Return the underlining string to be used at the given level for headline h.'''
    
        str = '''#=+*^~"'`-:><_''' [level]
    
        return str * max(len(h),4) + '\n'
    #@nonl
    #@-node:ekr.20040331071319.8:underlineString
    #@+node:ekr.20040811064922:report
    def report (self,name):
    
        path = g.os_path_abspath(g.os_path_join(os.getcwd(),name))
    
        g.es('wrote: %s' % (path),color="blue")
    #@nonl
    #@-node:ekr.20040811064922:report
    #@+node:ekr.20040331071319.4:writeSpecialTree
    def writeSpecialFile (self,p,fname,ext):
    
        pub = docutils.core.Publisher()
        html = ext in ('.html','.htm')
        writer = g.choose(html,'html','latex')
        self.encoding = g.choose(html,'utf-8','iso-8859-1')
        syntax = SilverCity is not None
        if html and not SilverCity:
            g.es('SilverCity not present so no syntax highlighting')
    
        stringFile = StringIO.StringIO()
        self.writeTree(stringFile,fname,p,syntax=syntax)
        source = stringFile.getvalue()
        if self.use_file:
            #@        << write source to fname.txt >>
            #@+node:ekr.20050802111543:<< write source to fname.txt >>
            g.es('Writing %s.txt' % fname)
            theFile = file(name+'.txt','w')
            theFile.write(source)
            theFile.close()
            #@nonl
            #@-node:ekr.20050802111543:<< write source to fname.txt >>
            #@nl
    
        # This code snipped has been taken from code contributed by Paul Paterson 2002-12-05.
        if self.use_file:
            pub.source = FileInput(source_path=rstFileName) ###
            pub.destination = FileOutput(destination_path=fname,encoding='unicode')
        else:
            pub.source = StringInput(source=source)
            pub.destination = StringOutput(pub.settings,encoding=self.encoding)
        pub.set_reader('standalone',None,'restructuredtext')
        pub.set_writer(writer)
        output = pub.publish(argv=[''])
        if not self.use_file:
            convertedFile = file(fname,'w')
            convertedFile.write(output)
            convertedFile.close()
        self.report(fname)
        return self.http_support_main(tag,fname)
    #@nonl
    #@-node:ekr.20040331071319.4:writeSpecialTree
    #@+node:ekr.20040331071319.7:writeTree
    def writeTree(self,theFile,fname,p,syntax=False):
        
        '''Write p's tree to theFile.'''
                
        # we don't write a title, so the titlepage can be customized
        # use '#' for title under/overline
        c = self.c
        d = g.scanDirectives(c,p=p)
        self.encoding = d.get('encoding',c.config.default_derived_file_encoding)
        #@    << set code_block_string >>
        #@+node:ekr.20040403202850:<< set code_block_string >>
        if syntax:
            # SilverCity modules have first letter in caps.
            language = d.get('language','').lower()
            if language in ('python','ruby','perl','c'):
                code_block_string = '**code**:\n\n.. code-block:: %s\n\n' % language.swapcase()
            else:
                code_block_string = '**code**:\n\n.. class:: code\n..\n\n::\n\n'
        else:
            code_block_string = '**code**:\n\n.. class:: code\n..\n\n::\n\n'
        #@nonl
        #@-node:ekr.20040403202850:<< set code_block_string >>
        #@nl
        theFile.write('.. filename: %d\n\n' % self.encode(fname))
        if self.massage_body:  ### should be a dynamic option.
            s = massageBody(p)
        else:
            s = p.bodyString()
        theFile.write('%s\n\n' % self.encode(s))		# write body of titlepage.
        toplevel = p.level() + 1
        if self.http_server_support:
            #@        << handle http support >>
            #@+node:ekr.20050802105832:<< handle http support >>
            if self.tag == 'open2':
                http_map = self.http_map
            else:
                http_map = {}
                self.anchormap = {}
                # maps v nodes to markers.
                self.node_counter = 0
            #@nonl
            #@-node:ekr.20050802105832:<< handle http support >>
            #@nl
        for p in p.subtree_iter():
            self.writeNode(theFile,p)
        if self.http_server_support:
            self.http_map = http_map
    #@nonl
    #@-node:ekr.20040331071319.7:writeTree
    #@+node:ekr.20050802120055:writeHeadline
    def writeHeadline (self,theFile,p,toplevel):
        
        h = p.headString() ; level = p.level() - toplevel
        tag = '@file-nosent'
    
        if g.match_word(h,0,tag):
            h = h[len(tag):]
    
        theFile.write('%s\n%s\n' % (self.encode(h),self.underlineString(h,level)))
    #@nonl
    #@-node:ekr.20050802120055:writeHeadline
    #@+node:ekr.20050802113353:writeNode & helpers
    def writeNode (self,theFile,p):
        
        if self.http_server_support:
            self.add_node_marker(p,theFile)
    
        if self.write_pure_document or g.match_word(h,0,"@rst"):
            self.writeRstNode (theFile,p)
        else:
            self.writePlainNode (theFile,p)
    
        if self.clear_http_attributes:
            self.clearHttpAttributes(p)
    #@nonl
    #@+node:ekr.20050802093751:add_node_marker
    def add_node_marker(self,p,theFile):
            
        self.node_counter += 1
        self.last_marker = marker = htmlparserClass.generate_node_marker(self.node_counter)
        self.http_map[marker] = p.copy()
        theFile.write("\n\n.. _%s:\n\n" % marker)
    #@nonl
    #@-node:ekr.20050802093751:add_node_marker
    #@+node:bwmulder.20050315150045:clearHttpAttributes
    def clearHttpAttributes (self,p):
        
        name = self.http_attributename
    
        if hasattr(p.v,'unknownAttributes'):
            if  p.v.unknownAttributes.has_key(name):
                del p.v.unknownAttributes [name]
                if p.v.unknownAttributes == {}:
                    del p.v.unknownAttributes
    #@nonl
    #@-node:bwmulder.20050315150045:clearHttpAttributes
    #@+node:bwmulder.20050326125712:replace_code_block_directives
    def replace_code_block_directives (self,s):
        
        lines = s.split('\n') ; result = []
        
        for line in lines:
            if u"code-block::" in line:
                parts = line.split()
                if len(parts) == 3 and (parts[0] == '..') and (parts[1]=='code-block::'):
                    line = '%s code::\n' % parts[2]
            result.append(line)
    
        return '\n'.join(result)
    #@nonl
    #@-node:bwmulder.20050326125712:replace_code_block_directives
    #@+node:ekr.20040403202850.2:writePlainNode
    def writePlainNode (self,theFile,p):
    
        if not self.format_headlines: ### ??? not ???
            self.writeHeadline(theFile,p,toplevel)
            
        if self.massage_body:
            s = self.massageBody(p)
        else:
            s = p.bodyString()
        
        s = self.encode(s)
        if s.strip():
            theFile.write(code_block_string)
            i = 0 ; lines = g.splitLines(s)
            for line in lines:
                i += 1
                if not "@others" in linetext:
                    theFile.write('\t%2d  %s\n'%(i,line))
        
        theFile.write('\n')
    #@nonl
    #@-node:ekr.20040403202850.2:writePlainNode
    #@+node:ekr.20040403202850.1:writeRstNode
    def writeRstNode (self,theFile,p):
    
        s = self.encode(p.bodyString())
        
        # Skip any leading @ignore, @nocolor, @wrap directives.
        while (
            g.match_word(s,0,"@ignore") or
            g.match_word(s,0,"@nocolor") or
            g.match_word(s,0,"@wrap")
        ):
            i = g.skip_line(s,0)
            s = s [i:]
        
        if self.format_headlines:
            self.writeHeadline(theFile,p,toplevel)
         
        if self.use_alternate_code_block and 'code-block::' in s:
            s = self.replace_code_block_directives(s)
        
        theFile.write('%s\n\n' % s.strip())
    #@nonl
    #@-node:ekr.20040403202850.1:writeRstNode
    #@-node:ekr.20050802113353:writeNode & helpers
    #@-node:ekr.20040331071319.3:processTree & helpers
    #@+node:bwmulder.20050319191929:http methods...
    #@+node:bwmulder.20050320092000:http_support_main
    def http_support_main(tag, fname):
    
        if not self.http_server_support:
            return
            
        set_initial_http_attributes(fname)
        find_anchors()
        if tag == 'open2':
            return True
        
        # We relocate references here if we are only running
        # for one file, otherwise we must postpone the
        # relocation until we have processed all files.
        relocate_references() 
    
        self.http_map = None
        self.anchormap = None
    
        g.es('html updated for html plugin', color="blue")
        if self.clear_http_attributes:
            g.es("http attributes cleared")
    #@nonl
    #@-node:bwmulder.20050320092000:http_support_main
    #@+node:bwmulder.20050319152820.1:http_attribute_iter
    def http_attribute_iter ():
    
        for p in self.http_map.values():
            attr = mod_http.get_http_attribute(p)
            if attr:
                yield (p.copy(),attr)
    #@nonl
    #@-node:bwmulder.20050319152820.1:http_attribute_iter
    #@+node:bwmulder.20050319131813:set_initial_http_attributes
    def set_initial_http_attributes(filename):
    
        theFile = file(filename)
        parser = htmlparserClass(self.http_map)
    
        for line in theFile.readline():
            parser.feed(line)
    #@nonl
    #@-node:bwmulder.20050319131813:set_initial_http_attributes
    #@+node:bwmulder.20050319131813.1:relocate_references
    def relocate_references(self):
    
        for p, attr in http_attribute_iter():
            if self.debug_before_and_after_replacement:
                print "Before replacement:", p
                pprint.pprint (attr)
            http_lines = attr[3:]
            parser = link_htmlparserClass(p)
            for line in attr[3:]:
                parser.feed(line)
            replacements = parser.get_replacements()
            replacements.reverse()
            for line, column, href, href_file, http_node_ref in replacements:
                marker_parts = href.split("#")
                if len(marker_parts) == 2:
                    marker = marker_parts[1]
                    replacement = "%s#%s" % (http_node_ref, marker)
                    attr[line+2] = attr[line+2].replace('href="%s"' % href, 'href="%s"' % replacement)
                else:
                    filename = marker_parts[0]
                    attr[line+2] = attr[line+2].replace('href="%s"' % href, 'href="%s"' % http_node_ref)
    
        if self.debug_before_and_after_replacement:
            print "After replacement"
            pprint.pprint (attr)
            for i in range(3): print
    #@nonl
    #@-node:bwmulder.20050319131813.1:relocate_references
    #@+node:bwmulder.20050319152820:find_anchors
    def find_anchors(self):
    
        '''Find the anchors in all the nodes.'''
    
        first_node = True
    
        for vnode, attrs in http_attribute_iter():
            html = mod_http.reconstruct_html_from_attrs(attrs)
            if self.debug_node_html_1:
                pprint.pprint(html)
            parser = anchor_htmlparserClass(vnode, first_node)
            for line in html:
                parser.feed(line)
            first_node = parser.first_node
    
        if self.debug_anchors:
            print "Anchors found:"
            pprint.pprint(self.anchormap)
    #@-node:bwmulder.20050319152820:find_anchors
    #@-node:bwmulder.20050319191929:http methods...
    #@-others
#@nonl
#@-node:ekr.20050802091909.1:class rstClass
#@+node:ekr.20050802093751.1:html parser classes
#@<< class linkAnchorParserClass >>
#@+node:bwmulder.20050319181934: << class linkAnchorParserClass >>
class linkAnchorParserClass (HTMLParser.HTMLParser):
    
    '''A class to recognize anchors and links in HTML documents.'''

    #@    @+others
    #@+node:ekr.20050802140041:__init__
    def __init__(self,rst):
    
        HTMLParser.HTMLParser.__init__(self) # Init the base class.
        
        self.rst = rst
        self.c = rst.c
    #@nonl
    #@-node:ekr.20050802140041:__init__
    #@+node:bwmulder.20050319181934.2:is_anchor
    def is_anchor(self, tag, attrs):
    
        if tag != 'a':
            return False
    
        for name, value in attrs:
            if name == 'name':
                return True
    
        return False
    #@nonl
    #@-node:bwmulder.20050319181934.2:is_anchor
    #@+node:bwmulder.20050323091905:is_link
    def is_link(self, tag, attrs):
    
        if tag != 'a':
            return False
    
        for name, value in attrs:
            if name == 'href':
                return True
    
        return False
      
    #@-node:bwmulder.20050323091905:is_link
    #@-others
#@nonl
#@-node:bwmulder.20050319181934: << class linkAnchorParserClass >>
#@nl

#@+others
#@+node:bwmulder.20050314184440:class htmlparserClass (linkAnchorParserClass)
class htmlparserClass (linkAnchorParserClass):
    
    '''
    The responsibility of the html parser is:
        1. to find out which html belongs to which node.
        2. to keep a stack of html markings which proceed each node.
        
    Later, we have to relocate inter-file links: if a reference to another location
    is in a file, we must change the link.
    
    '''

    #@    @+others
    #@+node:bwmulder.20050315115739:__init__
    def __init__(self, http_map):
    
        linkAnchorParserClass.__init__(self) # Init the base class.
        self.stack = None
        # The stack contains lists of the form:
            # [text1, text2, previous].
            # text1 is the opening tag
            # text2 is the closing tag
            # previous points to the previous stack element
        
        self.http_map = http_map  # see comments in rstClass ctor.
            
        self.node_marker_stack = []
        # self.node_marker_stack.pop() returns True for a closing
        # tag if the opening tag identified an anchor belonging to a vnode.
        
        self.node_code = []
            # Accumulated html code.
            # Once the hmtl code is assigned a vnode, it is deleted here.
        
        self.deleted_lines = 0 # Number of lines deleted in self.node_code
        
        self.endpos_pending = False
        # Do not include self.node_code[0:self.endpos_pending] in the html code.
        
        self.last_position = None
        # Last position; we must attach html code to this node.
    #@nonl
    #@-node:bwmulder.20050315115739:__init__
    #@+node:bwmulder.20050315115739.1:handle_starttag
    def handle_starttag(self, tag, attrs):
        '''
        1. Find out if the current tag is an achor.
        2. If it is an anchor, we check if this anchor marks the beginning of a new 
           node
        3. If a new node begins, then we might have to store html code in the
           previous code.
        4. In any case, put the new tag on the stack.
        '''
        is_node_marker = False
        if self.is_anchor(tag, attrs):
            for name, value in attrs:
                if name == 'name' and value.startswith(self.node_begin_marker):
                    is_node_marker = True
                    break
            if is_node_marker:
                is_node_marker = value
                line, column = self.getpos()
                if self.last_position:
                    lines = self.node_code[:]
                    lines[0] = lines[0][self.startpos:]
                    del lines[line - self.deleted_lines - 1:]
                    if self.debug_store_lines:
                        print "rst2: Storing in", self.last_position, ":"
                        print lines
                    mod_http.get_http_attribute(self.last_position).extend(lines)
    
                    if self.debug_show_unknownattributes:
                        print "rst2: unknownAttributes[self.http_attributename]"
                        print "For:", self.last_position
                        pprint.pprint(get_http_attr(self.last_position))
                                
                if self.deleted_lines < line - 1:
                    del self.node_code[:line - 1 - self.deleted_lines]
                    self.deleted_lines = line - 1
                    self.endpos_pending = True
        if self.debug_handle_starttag:
            print "rst2: handle_starttag:", tag, attrs, is_node_marker
        starttag = self.get_starttag_text( ) 
        self.stack = [starttag, None, self.stack]
        self.node_marker_stack.append(is_node_marker)
                
    #@nonl
    #@-node:bwmulder.20050315115739.1:handle_starttag
    #@+node:bwmulder.20050315115739.2:handle_endtag
    def handle_endtag(self, tag):
        '''
        1. Set the second element of the current top of stack.
        2. If this is the end tag for an anchor for a node,
           store the current stack for that node.
        '''
        self.stack[1] = "</" + tag + ">"
    
        if self.debug_handle_endtag:
            print "rst2: handle_endtag:", tag
            pprint.pprint(self.stack)
    
        if self.endpos_pending:
            line, column = self.getpos()
            self.startpos = self.node_code[0].find(">", column) + 1
            self.endpos_pending = False
        is_node_marker = self.node_marker_stack.pop()
    
        if is_node_marker and not self.clear_http_attributes:
            self.last_position = self.http_map[is_node_marker]
            if is_node_marker != self.last_marker:
                mod_http.set_http_attribute(self.http_map[is_node_marker], self.stack)
    
        self.stack = self.stack[2]
        
    #@nonl
    #@-node:bwmulder.20050315115739.2:handle_endtag
    #@+node:bwmulder.20050315115739.3:generate_node_marker (a class method)
    def generate_node_marker(cls, number):
        
        '''Generate a node marker.'''
    
        return self.node_begin_marker + ("%s" % number)
        
    generate_node_marker = classmethod(generate_node_marker)
    #@nonl
    #@-node:bwmulder.20050315115739.3:generate_node_marker (a class method)
    #@+node:bwmulder.20050315134705:feed
    def feed(self, line):
    
        self.node_code.append(line)
    
        HTMLParser.HTMLParser.feed(self, line)
    #@-node:bwmulder.20050315134705:feed
    #@-others
#@nonl
#@-node:bwmulder.20050314184440:class htmlparserClass (linkAnchorParserClass)
#@+node:bwmulder.20050319180047:class anchor_htmlparserClass (linkAnchorParserClass)
class anchor_htmlparserClass (linkAnchorParserClass):
    
    '''
    This htmlparser does the first step of relocating: finding all the anchors within the html node.
    
    Each anchor is mapped to a tuple:
        (current_file, vnode).
        
    Filters out markers which mark the beginning of the html code for a node.
    '''

    #@    @+others
    #@+node:bwmulder.20050319235437: __init__
    def __init__(self, vnode, first_node):
    
        linkAnchorParserClass.__init__(self)
    
        self.vnode = vnode
        self.anchormap = self.anchormap
        self.first_node = first_node
    #@-node:bwmulder.20050319235437: __init__
    #@+node:bwmulder.20050319181934.3:handle_starttag
    def handle_starttag(self, tag, attrs):
        '''
        1. Find out if the current tag is an achor.
        2. If the current tag is an anchor, update the mapping;
             anchor -> vnode
        '''
        if not self.is_anchor(tag, attrs):
            return
    
        if self.first_node:
            self.anchormap[self.current_file] = (self.current_file, self.vnode)
            self.first_node = False
    
        for name, value in attrs:
            if name == 'name':
                if not value.startswith(self.node_begin_marker):
                    self.anchormap[value] = (self.current_file, self.vnode)
                  
    #@nonl
    #@-node:bwmulder.20050319181934.3:handle_starttag
    #@-others
#@nonl
#@-node:bwmulder.20050319180047:class anchor_htmlparserClass (linkAnchorParserClass)
#@+node:bwmulder.20050320102006:class link_htmlparserClass (linkAnchorParserClass)
class link_htmlparserClass (linkAnchorParserClass):
    
    '''This html parser does the second step of relocating links:
    1. It scans the html code for links.
    2. If there is a link which links to a previously processed file
       then this link is changed so that it now refers to the node.
    '''

    #@    @+others
    #@+node:bwmulder.20050320102006.2:__init__
    def __init__(self, p):
        
        linkAnchorParserClass.__init__(self)
    
        self.p = p
        self.anchormap = self.anchormap ### ???
        self.replacements = []
    #@nonl
    #@-node:bwmulder.20050320102006.2:__init__
    #@+node:bwmulder.20050320102006.3:handle_starttag
    def handle_starttag(self, tag, attrs):
        '''
        1. Find out if the current tag is an achor.
        2. If the current tag is an anchor, update the mapping;
             anchor -> p
        '''
        if not self.is_link(tag, attrs):
            return
    
        marker = self.node_begin_marker
    
        for name, value in attrs:
            if name == 'href':
                href = value
                href_parts = href.split("#")
                if len(href_parts) == 1:
                    href_a = href_parts[0]
                else:
                    href_a = href_parts[1]
                if not href_a.startswith(marker):
                    if href_a in self.anchormap:
                        href_file, href_node = self.anchormap[href_a]
                        http_node_ref = mod_http.node_reference(href_node)
                        line, column = self.getpos()
                        self.replacements.append((line, column, href, href_file, http_node_ref))
    #@nonl
    #@-node:bwmulder.20050320102006.3:handle_starttag
    #@+node:bwmulder.20050320155022:get_replacements
    def get_replacements(self):
    
        return self.replacements
    #@nonl
    #@-node:bwmulder.20050320155022:get_replacements
    #@-others
#@nonl
#@-node:bwmulder.20050320102006:class link_htmlparserClass (linkAnchorParserClass)
#@-others
#@nonl
#@-node:ekr.20050802093751.1:html parser classes
#@-others
#@nonl
#@-node:ekr.20040331071319:@thin rst3.py
#@-leo
