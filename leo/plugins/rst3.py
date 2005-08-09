#@+leo-ver=4-thin
#@+node:ekr.20050805162550:@thin rst3.py
#@<< docstring >>
#@+node:ekr.20050805162550.1:<< docstring >>
'''This plugin adds the 'Write Restructured Text' command to the Edit menu. This
command searches for all nodes whose headline starts with @rst <filename>. When
the plugin finds such 'rst trees' it can take many different kinds of actions
depending upon which options in effect.

This plugin processes rst trees in two passes. The first pass looks for options
embedded within the tree. Such 'dynamic' options override defaults that are
specified in whatever @settings trees are in effect.

You can specify dynamic options in several equivalent ways:

1. Nodes whose headlines start with @rst-options can set one or more options. The
body text should contain lines of the form:
    
<option-name> = <value>

2. Nodes whose headlines start with

@rst-option <option-name> = <value>

set a single named option.

3. @doc parts (in body text) that have the form:
    
    @ @rst-options
    
should contain lines of the form:
    
<option-name> = <value>

just as with @rst-option nodes. The entire doc part is scanned until the next @c
directive or the end of the body text.

There are too many options to describe fully here. See the documentation for
this plugin in leoPlugins.leo and LeoDocs.leo for full details. In brief,
options cause this plugin to do the following kinds of things:

- Generate 'implicit' rst markup from outlines not containing rst markup.

- Scan rst-trees for already-existing 'explicit' rst markup. This plugin can
massage this add or change such markup. For example, various options control
whether and how this plugin will generate further rst markup from headlines.

- Send rst markup (either implicit or explicit markup) to docutils for further
processing. Naturally, docutils must be installed for this to happen. In
particular, this plugin can take advantage of docutils ability to format HTML
and LaTeX files. Files with extensions .html, .htm and .tex are by processed as
HTML or LaTeX files by default.

- Options control whether this plugin writes debugging information and
intermediate text files while performing these tasks. Other options control the
location and names of style sheets and other kinds of files.
'''
#@nonl
#@-node:ekr.20050805162550.1:<< docstring >>
#@nl

# Original rst code by Josef Dalcolmo:
# contributed under the same licensed as Leo.py itself.

# rst3.py based on rst2.py v2.4.

__version__ = '0.05'

#@<< imports >>
#@+node:ekr.20050805162550.2:<< imports >>
import leoGlobals as g
import leoPlugins

import os
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
    import docutils.core
    import docutils.io
except ImportError:
    docutils = None
    
try:
    import SilverCity
except ImportError:
    print 'rst3 plugin: SilverCity not loaded'
    SilverCity = None
#@-node:ekr.20050805162550.2:<< imports >>
#@nl
#@<< change log >>
#@+node:ekr.20050805162550.3:<< change log >>
#@+others
#@+node:ekr.20050806161758.1:v 0.02
#@+at 
#@nonl
# EKR: Minor improvments:
# 
# - The code_block callback function now works when SilverCity is not present,
# which resolves a long-standing question.
# 
# - Options get set from @settings trees if possible.
# 
# - No longer uses double-click.  Adds item to Edit menu.
# 
# - @button rst3 in test.leo will run processTree method, or load the module 
# if it
# hasn't been loaded yet.
#@-at
#@nonl
#@-node:ekr.20050806161758.1:v 0.02
#@+node:ekr.20050806161758.2:v 0.03
#@+at 
#@nonl
# EKR: The first cut at an accurate docstring.
#@-at
#@nonl
#@-node:ekr.20050806161758.2:v 0.03
#@+node:ekr.20050808083547:v 0.04
#@+at 
#@nonl
# EKR: add preprocess and helpers in 'scanning for options'
#@-at
#@nonl
#@-node:ekr.20050808083547:v 0.04
#@+node:ekr.20050808185746:v 0.05
#@+at
# 
# Initing and scanning for options is mostly complete:
# 
# - Improved munge: it now removes rstN_ prefix where N is any digit.
# - Added createDefaultOptionsDict and initOptionsFromSettings.
# - Wrote scanAllOptions.
#@-at
#@nonl
#@-node:ekr.20050808185746:v 0.05
#@+node:ekr.20050809094214:v 0.06
#@+at
# 
# - Reorganized and simplified top-level write code.
# - The code that initializes settings appears to work.
# - Simplified munge.
# ** The big question now involve how do we use settings and context to 
# generate what we want.
#@-at
#@nonl
#@-node:ekr.20050809094214:v 0.06
#@-others
#@@nocolor
#@nonl
#@-node:ekr.20050805162550.3:<< change log >>
#@nl
#@<< to do >>
#@+node:ekr.20050806162146:<< to do >>
#@@nocolor
#@+at
# 
# - Remove @ @rst-options parts from source.
# 
# - More flexible options:
#     - Default to True if no value given.
#     - Add encoding rst-option (can override @encoding directives)
# 
# - Add _multiple_doc_parts entry to dicts.
# 
# - scanOptionsDocPartFromLines
# 
# - visitTree (can't use iterator), visitNode, visitHeadline, visitBody
# 
# - Simplify the code further, especially concerning the creation of files.
#@-at
#@nonl
#@-node:ekr.20050806162146:<< to do >>
#@nl

controller = None # For use by @button rst3 code.

#@+others
#@+node:ekr.20050805162550.4:Module level
#@+node:ekr.20050805162550.5: init
def init ():

    ok = docutils is not None # Ok for unit testing.
    
    if ok:
        leoPlugins.registerHandler(("new","open2"), onCreate)
        g.plugin_signon(__name__)
    else:
        s = 'rst3 plugin not loaded: can not load docutils'
        print s ; g.es(s,color='red')

    return ok
#@nonl
#@-node:ekr.20050805162550.5: init
#@+node:ekr.20050805162550.6:onCreate
def onCreate(tag, keywords):

    c = keywords.get('new_c') or keywords.get('c')
    if c:
        global controller
        controller = rstClass(c)
        
        # Warning: Do not return anything but None here!
        # Doing so suppresses the loadeing of other 'new' or 'open2' hooks!
#@nonl
#@-node:ekr.20050805162550.6:onCreate
#@+node:ekr.20050806101253:code_block
def code_block (name,arguments,options,content,lineno,content_offset,block_text,state,state_machine):

    '''Implement the code-block directive for docutils.'''

    try:
        language = arguments [0]
        # See http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/252170
        module = getattr(SilverCity,language)
        generator = getattr(module,language+"HTMLGenerator")
        io = StringIO.StringIO()
        generator().generate_html(io,'\n'.join(content))
        html = '<div class="code-block">\n%s\n</div>\n' % io.getvalue()
        raw = docutils.nodes.raw('',html,format='html')
        return [raw]
    except Exception: # Return html as shown.  Lines are separated by <br> elements.
        html = '<div class="code-block">\n%s\n</div>\n' % '<br>\n'.join(content)
        raw = docutils.nodes.raw('',html,format='html')
        return [raw]
        
# See http://docutils.sourceforge.net/spec/howto/rst-directives.html
code_block.arguments = (
    1, # Number of required arguments.
    0, # Number of optional arguments.
    0) # True if final argument may contain whitespace.

# A mapping from option name to conversion function.
code_block.options = {
    'language':
    docutils.parsers.rst.directives.unchanged # Return the text argument, unchanged.
}

code_block.content = 1 # True if content is allowed.

# Register the directive with docutils.
docutils.parsers.rst.directives.register_directive('code-block',code_block)
#@nonl
#@-node:ekr.20050806101253:code_block
#@-node:ekr.20050805162550.4:Module level
#@+node:ekr.20050805162550.8:class rstClass
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
    #@+node:ekr.20050805162550.9: Birth & init
    #@+node:ekr.20050805162550.10: ctor (rstClass)
    def __init__ (self,c):
        
        global SilverCity
        
        self.c = c
        #@    << init ivars >>
        #@+node:ekr.20050805162550.11:<< init ivars >>
        # Debugging...
        self.rst2_debug_anchors = False
        self.debug_before_and_after_replacement = False
        self.debug_handle_endtag = False
        self.debug_handle_starttag = False
        self.debug_node_html_1 = False
        self.debug_show_unknownattributes = False
        self.debug_store_lines = False
        
        self.defaultEncoding = 'utf-8'
        self.encoding = self.defaultEncoding
        
        # For communication between methods...
        self.code_block_string = ''
        self.http_map = {}
            # A node anchor is a marker beginning with node_begin_marker.
            # We assume that such markers do not occur in the rst document.
        self.last_marker = None
        self.node_counter = 0
        self.toplevel = 0
        self.use_alternate_code_block = False ### SilverCity is None
        
        # For writing.
        self.ext = None # The file extension.
        self.outputFileName = None # The name of the file being written.
        self.outputFile = None # The open file being written.
        #@nonl
        #@-node:ekr.20050805162550.11:<< init ivars >>
        #@nl
    
        self.createDefaultOptionsDict()
        self.addMenu()
    #@nonl
    #@-node:ekr.20050805162550.10: ctor (rstClass)
    #@+node:ekr.20050805162550.12:addMenu
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
    #@-node:ekr.20050805162550.12:addMenu
    #@+node:ekr.20050808064245:createDefaultOptionsDict
    def createDefaultOptionsDict(self):
        
        self.defaultOptionsDict = {
        
            # Original rst2 options...
            'rst2_clear_http_attributes': False,
            'rst2_format_headlines': False,
            'rst2_http_server_support': False,
            'rst2_http_attributename': 'rst_http_attribute',
            'rst2_node_begin_marker':   'http-node-marker-',
            
            # rst2 options to be deleted...
            'rst2_massage_body': False,
            'rst2_write_pure_document': False,  # to be deleted
    
            # How to interpret @rst-settings nodes and @rst-settings and @rst-markup doc parts...
            'rst3_ignore_leo_directives_in_auto_mode': False,
            'rst3_ignore_leo_directives_in_manual_mode': True,
            'rst3_always_ignore_these_directives': None, # list of directives
            'rst3_never_ignore_these_directives':  None, # list of directives
            
            'rst3_ignore_option_nodes_in_auto_mode': False,
            'rst3_ignore_option_doc_parts_in_auto_mode': False,
            'rst3_ignore_markup_doc_parts_in_auto_mode': False,
            
            'rst3_ignore_option_nodes_in_manual_mode': True,
            'rst3_ignore_option_doc_parts_in_manual_mode': True,
            'rst3_ignore_markup_doc_parts_in_manual_mode': True,
            
            # How to process nodes, headlines and body text...
            'rst3_ignore_all_headlines_in_auto_mode': False,
            'rst3_ignore_all_headlines_in_manual_mode': False,
            
            'rst3_ignore_organizer_nodes_in_auto_mode': False,
            'rst3_ignore_organizer_nodes_in_manual_mode': False,
            
            'rst3_ignore_headlines_with_prefix_in_auto_mode': None,
            'rst3_ignore_headlines_with_prefix_in_manual_mode': None,
            
            'rst3_process_only_headlines_with_prefix_in_auto_mode': None,
            'rst3_process_only_headlines_with_prefix_in_manual_mode': None,
            
            'rst3_process_only_bodies_with_headline_prefix_in_auto_mode': None,
            'rst3_process_only_bodies_with_headline_prefix_in_manual_mode': None,
            
            'rst3_process_only_nodes_with_headline_prefix_in_auto_mode': None,
            'rst3_process_only_nodes_with_headline_prefix_in_manual_mode': None,
            
            # rst-specific options...
            'rst3_underline_characters': '', #whatever the default chars are presently
            'rst3_write_docutils_sources_to_file': False,
        }
        
    #@nonl
    #@-node:ekr.20050808064245:createDefaultOptionsDict
    #@+node:ekr.20050808072943:munge
    def munge (self,name):
        
        '''Remove rstNNN_ prefix.'''
        
        # s = g.app.config.canonicalizeSettingName(name)
        
        i = g.choose(name.startswith('rst'),3,0)
    
        while i < len(name) and name[i].isdigit():
            i += 1
    
        if i < len(name) and name[i] == '_':
            i += 1
        
        return name[i:]
    #@nonl
    #@-node:ekr.20050808072943:munge
    #@-node:ekr.20050805162550.9: Birth & init
    #@+node:ekr.20050805162550.16:encode
    def encode (self,s):
    
        return g.toEncodedString(s,encoding=self.encoding,reportErrors=True)
    #@nonl
    #@-node:ekr.20050805162550.16:encode
    #@+node:ekr.20050807120331.1:preprocessTree & helpers
    def preprocessTree (self,root):
        
        self.tnodeOptionDict = {}
        
        for p in root.self_and_subtree_iter():
            d = self.tnodeOptionDict.get(p.v.t)
            if not d:
                d = self.scanNodeForOptions(p)
                if d:
                    self.tnodeOptionDict [p.v.t] = (p.headString(),d)
                
        if 0:
            g.trace(root.headString())
            g.printDict(self.tnodeOptionDict)
    #@nonl
    #@+node:ekr.20050808072943.1:parseOptionLine
    def parseOptionLine (self,s):
    
        '''Parse a line containing name=val and return (name,value) or None.'''
    
        s = s.strip()
        # Get name.  Names may contain '-' and '_'.
        i = g.skip_id(s,0,chars='-_')
        name = s [:i]
        if not name: return None
        # Skip the '='.
        j = g.skip_ws(s,i)
        if not g.match(s,j,'='): return None
        # Get val.
        val = s [j+1:].strip()
        if val:
            return (name,val)
        else:
            return None
    #@nonl
    #@-node:ekr.20050808072943.1:parseOptionLine
    #@+node:ekr.20050808070018.2:scanForOptionDocParts
    def scanForOptionDocParts (self,p,s):
        
        '''Return a dictionary containing all options from @rst-options doc parts in p.
        Multiple @rst-options doc parts are allowed: this code aggregates all options.
        '''
    
        d = {} ; n = 0 ; lines = g.splitLines(s)
        while n < len(lines):
            line = lines[n] ; n += 1
            if line.startswith('@'):
                i = g.skip_ws(line,1)
                if g.match_word(line,i,'@rst-options'):
                    # Add options until the end of the doc part.
                    while n < len(lines):
                        line = lines[n] ; n += 1
                        if g.match_word(line,0,'@c') or g.match_word(line,0,'@code'):
                            break
                        else:
                            d2 = self.scanOption(p,line)
                            if d2: d.update(d2)
        return d
    #@nonl
    #@-node:ekr.20050808070018.2:scanForOptionDocParts
    #@+node:ekr.20050807120331.2:scanNodeForOptions
    def scanNodeForOptions (self,p):
    
        '''Return a dictionary containing all the option-name:value entries in p.
        
        Such entries may arise from @rst-option or @rst-options in the headline,
        or from @ @rst-options doc parts.'''
    
        h = p.headString()
    
        if g.match_word(h,0,'@rst-option'):
            s = h [len('@rst-option'):]
            d = self.scanOption(p,s)
        elif g.match_word(h,0,'@rst-options'):
            d = self.scanOptions(p,p.bodyString())
        else:
            d = self.scanForOptionDocParts(p,p.bodyString())
            
        # g.trace(p.headString(),d)
        return d
    #@nonl
    #@-node:ekr.20050807120331.2:scanNodeForOptions
    #@+node:ekr.20050808070018:scanOption
    def scanOption (self,p,s):
        
        '''Return { name:val } is s is a line of the form name=val.
        Otherwise return {}'''
        
        data = self.parseOptionLine(s)
    
        if data:
            name,val = data
            if   val.lower() == 'true': val = True
            elif val.lower() == 'false': val = False
            return { self.munge(name): val }
        else:
            g.trace(repr(s))
            s2 = 'bad rst3 option in %s: %s' % (p.headString(),s)
            g.es(s2,color='blue')
            return {}
    #@-node:ekr.20050808070018:scanOption
    #@+node:ekr.20050808070018.1:scanOptions
    def scanOptions (self,p,s):
        
        '''Return a dictionary containing all the options in s.'''
         
        d = {}
    
        for line in g.splitLines(s):
            d2 = self.scanOption(p,line)
            if d2: d.update(d2)
            
        return d
    #@nonl
    #@-node:ekr.20050808070018.1:scanOptions
    #@-node:ekr.20050807120331.1:preprocessTree & helpers
    #@+node:ekr.20050808142313.28:scanAllOptions & helper
    # Once an option is seen, no other related options in ancestor nodes haveany effect.
    
    def scanAllOptions(self,p):
        
        '''Scan position p and p's ancestors looking for options,
        setting corresponding ivars.
        '''
        
        self.initOptionsFromSettings() # Must be done on every node.
        result = {}
        for p in p.self_and_parents_iter():
            d = tnodeOptionDict.get(p.v.t)
            if d:
                for key in d.keys():
                    if not result.has_key(key):
                        val = d.get(key)
                        ivar = self.munge(key)
                        result [ivar] = val
                        g.trace(ivar,val)
        return result
    #@nonl
    #@+node:ekr.20050805162550.13:initOptionsFromSettings
    def initOptionsFromSettings (self):
    
        c = self.c ; d = self.defaultOptionsDict
        keys = d.keys() ; keys.sort()
    
        for key in keys:
            for getter,kind in (
                (c.config.getBool,'@bool'),
                (c.config.getString,'@string'),
                (d.get,'default'),
            ):
                val = getter(key)
                if kind == 'default' or val is not None:
                    ivar = self.munge(key)
                    if kind != 'default': print '%7s %55s %s' % (kind,ivar,val)
                    setattr(self,ivar,val)
                    break
    
        # Special case.
        if self.http_server_support and not mod_http:
            g.es('No http_server_support: can not import mod_http plugin',color='red')
            self.http_server_support = False
    #@-node:ekr.20050805162550.13:initOptionsFromSettings
    #@-node:ekr.20050808142313.28:scanAllOptions & helper
    #@+node:ekr.20050809074827:write methods
    #@+node:ekr.20050809082854: Top-level write code
    #@+node:ekr.20050809075309:initWrite
    def initWrite (self,p,encoding=None):
        
        # Set the encoding from any parent @encoding directive.
        # This can be overridden by @rst-option encoding=whatever.
        d = g.scanDirectives(c=self.c,p=p)
        self.encoding = encoding or d.get('encoding') or self.defaultEncoding
    
        # Make sure all ivars are defined.  Also called by scanAllOptions.
        self.initOptionsFromSettings()
        
        language = d.get('language','').lower()
        syntax = SilverCity is not None
    
        if syntax and language in ('python','ruby','perl','c'):
            self.code_block_string = '**code**:\n\n.. code-block:: %s\n\n' % language.swapcase()
        else:
            self.code_block_string = '**code**:\n\n.. class:: code\n..\n\n::\n\n'
            
        self.toplevel = p.level() + 1
    #@nonl
    #@-node:ekr.20050809075309:initWrite
    #@+node:ekr.20050805162550.17:processTree
    def processTree(self,p):
        
        '''Process all @rst nodes in a tree.'''
    
        self.preprocessTree(p)
        found = False
        p = p.copy() ; after= p.nodeAfterTree()
        while p and p != after:
            h = p.headString().strip()
            if g.match_word(h,0,"@rst"):
                self.outputFileName = h[4:].strip()
                if self.outputFileName:
                    found = True
                    g.trace(self.outputFileName)
                    self.ext = ext = g.os_path_splitext(self.outputFileName)[1].lower()
                    if ext in ('.htm','.html','.tex'):
                        self.writeSpecialTree(p)
                    else:
                        self.writeNormalTree(p)
                    self.report(self.outputFileName)
                    p.moveToNodeAfterTree()
                else:
                    p.moveToThreadNext()
            else: p.moveToThreadNext()
        if not found:
            g.es('No @rst nodes in selected tree',color='blue')
    #@nonl
    #@-node:ekr.20050805162550.17:processTree
    #@+node:ekr.20050809080925:writeNormalTree
    def writeNormalTree (self,p):
    
        self.initWrite(p)
        self.outputFile = file(self.outputFileName,'w')
        self.writeTree(p)
        self.outputFile.close()
    #@nonl
    #@-node:ekr.20050809080925:writeNormalTree
    #@+node:ekr.20050805162550.21:writeSpecialTree
    def writeSpecialTree (self,p):
        
        isHtml = self.ext in ('.html','.htm')
        if isHtml and not SilverCity:
            g.es('SilverCity not present so no syntax highlighting')
        
        self.initWrite(p,encoding=g.choose(isHtml,'utf-8','iso-8859-1'))
        self.outputFile = StringIO.StringIO()
        self.writeTree(p)
        source = self.outputFile.getvalue()
        self.outputFile = None
    
        if self.write_docutils_sources_to_file:
            name = self.outputFileName + '.txt'
            g.es('Writing docutils sources to %s' % (name),color='blue')
            f = file(name,'w')
            f.write(source)
            f.close()
            
        try:
            output = self.writeToDocutils(source,isHtml)
        except Exception:
            output = None
            
        if output:
            f = file(self.outputFileName,'w')
            f.write(output)
            f.close()
            
        return self.http_support_main(self.outputFileName)
    #@nonl
    #@-node:ekr.20050805162550.21:writeSpecialTree
    #@-node:ekr.20050809082854: Top-level write code
    #@+node:ekr.20050805162550.18:massageBody
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
    #@-node:ekr.20050805162550.18:massageBody
    #@+node:ekr.20050805162550.20:report
    def report (self,name):
    
        path = g.os_path_abspath(g.os_path_join(os.getcwd(),name))
    
        g.es('wrote: %s' % (path),color="blue")
    #@nonl
    #@-node:ekr.20050805162550.20:report
    #@+node:ekr.20050805162550.19:underlineString
    # The first character is intentionally unused, to serve as the underline
    # character in a title (in the body of the @rst node)
    
    def underlineString (self,h,level):
    
        '''Return the underlining string to be used at the given level for headline h.'''
    
        str = '''#=+*^~"'`-:><_''' [level]
    
        return str * max(len(h),4) + '\n'
    #@nonl
    #@-node:ekr.20050805162550.19:underlineString
    #@+node:ekr.20050809080031:write
    def write (self,s):
        
        s = self.encode(s)
        
        self.outputFile.write(s)
    #@nonl
    #@-node:ekr.20050809080031:write
    #@+node:ekr.20050805162550.26:writeHeadline
    def writeHeadline (self,p):
        
        h = p.headString() ; level = p.level() - self.toplevel
        tag = '@file-nosent'
    
        if g.match_word(h,0,tag):
            h = h[len(tag):]
    
        self.write('%s\n%s\n' % (self.encode(h),self.underlineString(h,level)))
    #@nonl
    #@-node:ekr.20050805162550.26:writeHeadline
    #@+node:ekr.20050805162550.27:writeNode & helpers
    def writeNode (self,p):
    
        if self.http_server_support:
            self.add_node_marker(p)
    
        if self.write_pure_document or g.match_word(p.headString(),0,"@rst"):
            self.writeRstNode(p)
        else:
            self.writePlainNode(p)
    
        if self.clear_http_attributes:
            self.clearHttpAttributes(p)
    #@nonl
    #@+node:ekr.20050805162550.28:add_node_marker
    def add_node_marker(self,p):
            
        self.node_counter += 1
        self.last_marker = marker = htmlparserClass.generate_node_marker(self.node_counter)
        self.http_map[marker] = p.copy()
        self.write("\n\n.. _%s:\n\n" % marker)
    #@nonl
    #@-node:ekr.20050805162550.28:add_node_marker
    #@+node:ekr.20050805162550.29:clearHttpAttributes
    def clearHttpAttributes (self,p):
        
        name = self.http_attributename
    
        if hasattr(p.v,'unknownAttributes'):
            if  p.v.unknownAttributes.has_key(name):
                del p.v.unknownAttributes [name]
                if p.v.unknownAttributes == {}:
                    del p.v.unknownAttributes
    #@nonl
    #@-node:ekr.20050805162550.29:clearHttpAttributes
    #@+node:ekr.20050805162550.30:replace_code_block_directives
    def replace_code_block_directives (self,s):
    
        lines = s.split('\n') ; result = []
    
        for line in lines:
            if u"code-block::" in line:
                parts = line.split()
                if len(parts) == 3 and (parts[0]=='..') and (parts[1]=='code-block::'):
                    line = '%s code::\n' % parts [2]
            result.append(line)
    
        return '\n'.join(result)
    #@nonl
    #@-node:ekr.20050805162550.30:replace_code_block_directives
    #@+node:ekr.20050805162550.31:writePlainNode
    def writePlainNode (self,p):
    
        if not self.format_headlines: ### ??? not ???
            self.writeHeadline(p)
            
        if self.massage_body:
            s = self.massageBody(p)
        else:
            s = p.bodyString()
        
        s = self.encode(s)
        if s.strip():
            self.write(self.code_block_string)
            i = 0 ; lines = g.splitLines(s)
            for line in lines:
                i += 1
                if not "@others" in linetext:
                    self.write('\t%2d  %s\n'%(i,line))
        
        self.write('\n')
    #@nonl
    #@-node:ekr.20050805162550.31:writePlainNode
    #@+node:ekr.20050805162550.32:writeRstNode
    def writeRstNode (self,p):
    
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
            self.writeHeadline(p)
    
        if self.use_alternate_code_block and 'code-block::' in s:
            s = self.replace_code_block_directives(s)
    
        self.write('%s\n\n' % s.strip())
    #@nonl
    #@-node:ekr.20050805162550.32:writeRstNode
    #@-node:ekr.20050805162550.27:writeNode & helpers
    #@+node:ekr.20050805162550.23:writeTree
    def writeTree(self,p):
        
        '''Write p's tree to self.outputFile.'''
                
        # Don't write a title, so the titlepage can be customized
        # use '#' for title under/overline
        self.write('.. filename: %s\n\n' % self.outputFileName)
        if self.massage_body:
            s = massageBody(p)
        else:
            s = p.bodyString()
        self.write('%s\n\n' % s)		# write body of titlepage.
        
        if self.http_server_support:
            #@        << handle http support >>
            #@+node:ekr.20050805162550.25:<< handle http support >>
            if 1:
                http_map = {}
            else:  # Not ready yet.
                if self.tag == 'open2':
                    http_map = self.http_map
                else:
                    http_map = {}
                    self.anchormap = {}
                    # maps v nodes to markers.
                    self.node_counter = 0
            #@nonl
            #@-node:ekr.20050805162550.25:<< handle http support >>
            #@nl
            
        for p in p.subtree_iter():
            self.writeNode(p)
    
        if self.http_server_support:
            self.http_map = http_map
    #@-node:ekr.20050805162550.23:writeTree
    #@+node:ekr.20050809082854.1:writeToDocutils (sets argv)
    def writeToDocutils (self,s,isHtml):
        
        '''Send s to docutils and return the result.'''
    
        pub = docutils.core.Publisher()
    
        pub.source      = docutils.io.StringInput(source=s)
        pub.destination = docutils.io.StringOutput(pub.settings,encoding=self.encoding)
    
        pub.set_reader('standalone',None,'restructuredtext')
        pub.set_writer(g.choose(isHtml,'html','latex'))
        
        return pub.publish(argv=[r'--stylesheet=c:\prog\leoCvs\leo\doc\default.css'])
    #@nonl
    #@-node:ekr.20050809082854.1:writeToDocutils (sets argv)
    #@-node:ekr.20050809074827:write methods
    #@+node:ekr.20050805162550.33:http methods...
    #@+node:ekr.20050805162550.34:http_support_main
    def http_support_main (self,fname):
    
        if not self.http_server_support:
            return
    
        g.trace()
    
        self.set_initial_http_attributes(fname)
        self.find_anchors()
        # if tag == 'open2':
            # return True
    
        # We relocate references here if we are only running
        # for one file, otherwise we must postpone the
        # relocation until we have processed all files.
        self.relocate_references()
    
        self.http_map = None
        self.anchormap = None
    
        g.es('html updated for html plugin',color="blue")
        if self.clear_http_attributes:
            g.es("http attributes cleared")
    #@nonl
    #@-node:ekr.20050805162550.34:http_support_main
    #@+node:ekr.20050805162550.35:http_attribute_iter
    def http_attribute_iter (self):
    
        for p in self.http_map.values():
            attr = mod_http.get_http_attribute(p)
            if attr:
                yield (p.copy(),attr)
    #@nonl
    #@-node:ekr.20050805162550.35:http_attribute_iter
    #@+node:ekr.20050805162550.36:set_initial_http_attributes
    def set_initial_http_attributes (self,filename):
    
        f = file(filename)
        parser = htmlparserClass(self.http_map)
    
        for line in f.readline():
            parser.feed(line)
            
        f.close()
    #@nonl
    #@-node:ekr.20050805162550.36:set_initial_http_attributes
    #@+node:ekr.20050805162550.37:relocate_references
    def relocate_references (self):
    
        for p, attr in http_attribute_iter():
            if self.debug_before_and_after_replacement:
                print "Before replacement:", p
                pprint.pprint(attr)
            http_lines = attr [3:]
            parser = link_htmlparserClass(p)
            for line in attr [3:]:
                parser.feed(line)
            replacements = parser.get_replacements()
            replacements.reverse()
            for line, column, href, href_file, http_node_ref in replacements:
                marker_parts = href.split("#")
                if len(marker_parts) == 2:
                    marker = marker_parts [1]
                    replacement = "%s#%s" % (http_node_ref,marker)
                    attr [line + 2] = attr [line + 2].replace('href="%s"' % href,'href="%s"' % replacement)
                else:
                    filename = marker_parts [0]
                    attr [line + 2] = attr [line + 2].replace('href="%s"' % href,'href="%s"' % http_node_ref)
    
        if self.debug_before_and_after_replacement:
            print "After replacement"
            pprint.pprint(attr)
            for i in range(3): print
    #@nonl
    #@-node:ekr.20050805162550.37:relocate_references
    #@+node:ekr.20050805162550.38:find_anchors
    def find_anchors (self):
    
        '''Find the anchors in all the nodes.'''
    
        first_node = True
    
        for vnode, attrs in http_attribute_iter():
            html = mod_http.reconstruct_html_from_attrs(attrs)
            if self.debug_node_html_1:
                pprint.pprint(html)
            parser = anchor_htmlparserClass(vnode,first_node)
            for line in html:
                parser.feed(line)
            first_node = parser.first_node
    
        if self.debug_anchors:
            print "Anchors found:"
            pprint.pprint(self.anchormap)
    #@-node:ekr.20050805162550.38:find_anchors
    #@-node:ekr.20050805162550.33:http methods...
    #@-others
#@nonl
#@-node:ekr.20050805162550.8:class rstClass
#@+node:ekr.20050805162550.39:html parser classes
#@<< class linkAnchorParserClass >>
#@+node:ekr.20050805162550.40: << class linkAnchorParserClass >>
class linkAnchorParserClass (HTMLParser.HTMLParser):
    
    '''A class to recognize anchors and links in HTML documents.'''

    #@    @+others
    #@+node:ekr.20050805162550.41:__init__
    def __init__(self,rst):
    
        HTMLParser.HTMLParser.__init__(self) # Init the base class.
        
        self.rst = rst
        self.c = rst.c
    #@nonl
    #@-node:ekr.20050805162550.41:__init__
    #@+node:ekr.20050805162550.42:is_anchor
    def is_anchor(self, tag, attrs):
    
        if tag != 'a':
            return False
    
        for name, value in attrs:
            if name == 'name':
                return True
    
        return False
    #@nonl
    #@-node:ekr.20050805162550.42:is_anchor
    #@+node:ekr.20050805162550.43:is_link
    def is_link(self, tag, attrs):
    
        if tag != 'a':
            return False
    
        for name, value in attrs:
            if name == 'href':
                return True
    
        return False
      
    #@-node:ekr.20050805162550.43:is_link
    #@-others
#@nonl
#@-node:ekr.20050805162550.40: << class linkAnchorParserClass >>
#@nl

#@+others
#@+node:ekr.20050805162550.44:class htmlparserClass (linkAnchorParserClass)
class htmlparserClass (linkAnchorParserClass):
    
    '''
    The responsibility of the html parser is:
        1. to find out which html belongs to which node.
        2. to keep a stack of html markings which proceed each node.
        
    Later, we have to relocate inter-file links: if a reference to another location
    is in a file, we must change the link.
    
    '''

    #@    @+others
    #@+node:ekr.20050805162550.45:__init__
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
    #@-node:ekr.20050805162550.45:__init__
    #@+node:ekr.20050805162550.46:handle_starttag
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
    #@-node:ekr.20050805162550.46:handle_starttag
    #@+node:ekr.20050805162550.47:handle_endtag
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
    #@-node:ekr.20050805162550.47:handle_endtag
    #@+node:ekr.20050805162550.48:generate_node_marker (a class method) NOT READY
    def generate_node_marker(cls, number):
        
        '''Generate a node marker.'''
        
        return ### 
    
        return self.node_begin_marker + ("%s" % number)
        
    generate_node_marker = classmethod(generate_node_marker)
    #@nonl
    #@-node:ekr.20050805162550.48:generate_node_marker (a class method) NOT READY
    #@+node:ekr.20050805162550.49:feed
    def feed(self, line):
    
        self.node_code.append(line)
    
        HTMLParser.HTMLParser.feed(self, line)
    #@-node:ekr.20050805162550.49:feed
    #@-others
#@nonl
#@-node:ekr.20050805162550.44:class htmlparserClass (linkAnchorParserClass)
#@+node:ekr.20050805162550.50:class anchor_htmlparserClass (linkAnchorParserClass)
class anchor_htmlparserClass (linkAnchorParserClass):
    
    '''
    This htmlparser does the first step of relocating: finding all the anchors within the html node.
    
    Each anchor is mapped to a tuple:
        (current_file, vnode).
        
    Filters out markers which mark the beginning of the html code for a node.
    '''

    #@    @+others
    #@+node:ekr.20050805162550.51: __init__
    def __init__(self, vnode, first_node):
    
        linkAnchorParserClass.__init__(self)
    
        self.vnode = vnode
        self.anchormap = self.anchormap
        self.first_node = first_node
    #@-node:ekr.20050805162550.51: __init__
    #@+node:ekr.20050805162550.52:handle_starttag
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
    #@-node:ekr.20050805162550.52:handle_starttag
    #@-others
#@nonl
#@-node:ekr.20050805162550.50:class anchor_htmlparserClass (linkAnchorParserClass)
#@+node:ekr.20050805162550.53:class link_htmlparserClass (linkAnchorParserClass)
class link_htmlparserClass (linkAnchorParserClass):
    
    '''This html parser does the second step of relocating links:
    1. It scans the html code for links.
    2. If there is a link which links to a previously processed file
       then this link is changed so that it now refers to the node.
    '''

    #@    @+others
    #@+node:ekr.20050805162550.54:__init__
    def __init__(self, p):
        
        linkAnchorParserClass.__init__(self)
    
        self.p = p
        self.anchormap = self.anchormap ### ???
        self.replacements = []
    #@nonl
    #@-node:ekr.20050805162550.54:__init__
    #@+node:ekr.20050805162550.55:handle_starttag
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
    #@-node:ekr.20050805162550.55:handle_starttag
    #@+node:ekr.20050805162550.56:get_replacements
    def get_replacements(self):
    
        return self.replacements
    #@nonl
    #@-node:ekr.20050805162550.56:get_replacements
    #@-others
#@nonl
#@-node:ekr.20050805162550.53:class link_htmlparserClass (linkAnchorParserClass)
#@-others
#@nonl
#@-node:ekr.20050805162550.39:html parser classes
#@-others
#@nonl
#@-node:ekr.20050805162550:@thin rst3.py
#@-leo
