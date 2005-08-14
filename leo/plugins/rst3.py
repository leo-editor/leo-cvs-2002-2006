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

__version__ = '0.3'

#@<< imports >>
#@+node:ekr.20050805162550.2:<< imports >>
import leoGlobals as g
import leoColor # for leoKeywords
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
#@+node:ekr.20050813103025:v 0.0x
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
#@+node:ekr.20050810085314:v 0.07
#@+at
# 
# - Completed writeTree: it now allows for skipping subtrees.
# 
# - Simplified options and their names: see createDefaultOptionsDict.
#     - Use rst3 prefix for all settings.
#     - The generate_rst setting will be the basis for generating rst or plain 
# text.
# 
# - Moved all headline-related stuff into writeHeadline.
# 
# - Added support for skip_this_node and skip_this_tree.
#     - More work is needed.
#@-at
#@nonl
#@-node:ekr.20050810085314:v 0.07
#@+node:ekr.20050811092824:v 0.08
#@+at
# 
# - Handled literal blocks properly in replaceCodeBlockDirectives.
#   This bug existed in rst2 plugin.
# 
# - Removed a confusing 'feature' from replaceCodeBlockDirectives.
# 
# This method now creates starts the code block with just '::'. The old code
# started the literal block with 'python code ::' This seemed very confusing.
# 
# - Default to True for all options.  This is especially useful for the 
# skip_node and skip_tree options.
# 
# - scanOption now warns if a unknown option is seen.
# 
# - Created writeBody method to replace writePlainNode and writeRstNode.
#     - writeBody removes special doc parts and leoDirectives under control of 
# user options.
#@-at
#@nonl
#@-node:ekr.20050811092824:v 0.08
#@+node:ekr.20050811112803:v 0.09
#@+at
# 
# ** Code mode mostly works, as do most kinds of markup.
# 
# - Handled @rst-markup doc parts properly.
# - Removed writePlainNode and writeRstNode.
# - Allowed .. comments in special doc parts.
# - settings in @rst-options doc parts may end with a comma.
# - Special doc parts now also stop at the start of another doc part.
# - Added number_code_lines option.
# - Wrote handleCodeMode.
# - Wrote scanHeadlineForOptions.
#@-at
#@nonl
#@-node:ekr.20050811112803:v 0.09
#@+node:ekr.20050812033346:v 0.010
#@+at 
#@nonl
# Another big step forward.  More collapses into simplicity...
# 
# There is no need for the following options:
#     rst3_include_markup_doc_parts
#     rst3_show_options_doc_parts
#     rst3_show_options_nodes
# 
# There are now so few options that named option sets aren't so useful!
# 
# Special doc parts will never be shown.  You can use rst literal blocks to 
# talk about such things!
# 
# - Always remove special doc parts
# - Always remove Leo directives in rst mode.
#     Again, you can use code-blocks or literal blocks if desired.
# 
# All @rst-xxx headlines enter rst mode, except for @rst-option and 
# @rst-options.
#     - This is a major simplification: most @rst-markup doc parts are not 
# needed.
# 
# - Bare @rst headline is equivalent to @rst-no-head.
#     - This makes rst3 compatible with rst2.
# 
# - Improved munge: changed - to underscore, lowercased everything.
#@-at
#@nonl
#@-node:ekr.20050812033346:v 0.010
#@+node:ekr.20050812092209:v 0.011
#@+at
# 
# - Wrote full path in report.
#@-at
#@nonl
#@-node:ekr.20050812092209:v 0.011
#@-node:ekr.20050813103025:v 0.0x
#@+node:ekr.20050813100922:v 0.1
#@+at
# 
# See http://webpages.charter.net/edreamleo/rstplugin3.html for full 
# documentation.
# 
# You can start reporting bugs now :-)
# 
# All major features work, and have been tested for usability while writing 
# the
# documentation for this plugin. Some bugs remain, but this version should be
# usable.
# 
# - Properly initied 'single node options'
# 
# - Use general names for @rst-option and @rst-options in 
# scanHeadlineForOptions.
# 
# - Added support for headlline commands.
# 
# - Handles ListManagerDocs.html in test.leo.
#@-at
#@nonl
#@-node:ekr.20050813100922:v 0.1
#@+node:ekr.20050813145858:v 0.2
#@+at
# 
# - Added support for rst3_stylesheet_name ad rst3_stylesheet_path options.
# 
# - Revised and simplified writeBody.
# 
# - Removed blank lines from code parts.
# 
# - Added support for show_doc_parts_as_paragraphs option.
# 
# Oh happy day. Doc parts included in code mode as the result of
# show_doc_parts_as_paragraphs option are equivalent to @ @rst-markup doc 
# parts!
# That is, they can contain rST markup.
#@-at
#@nonl
#@-node:ekr.20050813145858:v 0.2
#@+node:ekr.20050813173425:v 0.3
#@+at
# 
# - Added support for @rst-head command.
# 
# Testing @rst-head revealed the following bugs:
# 
#     - parseOptionLine: everything was getting turned to 'True'!
# 
#     - scanHeadlineForOptions was returning None instead of the dicts 
# returned by scanOption/s.
#@-at
#@nonl
#@-node:ekr.20050813173425:v 0.3
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
# First:
# 
# - Treat @rst-option and @rst-options identically.
# 
# - Test @rst-ignore-head and @rst-ignore-tree
# 
# * Handle http options.
# 
# Later:
# 
# ? show_context option.
# 
# ? Support named options sets.
# 
# ? encoding option: can override @encoding directives
# 
# ? Support docutils config files.
# 
# - (not so important now) Compute effective rst level, ignoring ignored 
# headlines.
#     - That is, most ignored headlines will be @rst nodes that don't have 
# descendents.
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

    # g.trace(c)
    
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
        #@    << init debugging ivars >>
        #@+node:ekr.20050810090137:<< init debugging ivars >>
        self.debug_anchors = False
        self.debug_before_and_after_replacement = False
        self.debug_handle_endtag = False
        self.debug_handle_starttag = False
        self.debug_node_html_1 = False
        self.debug_show_unknownattributes = False
        self.debug_store_lines = False
        #@nonl
        #@-node:ekr.20050810090137:<< init debugging ivars >>
        #@nl
        #@    << init ivars >>
        #@+node:ekr.20050805162550.11:<< init ivars >>
        # Non-inheritable options...
        self.ignore_this_headline = False
        self.show_this_headline = False
        self.skip_this_node = False
        self.skip_this_tree = False
        
        # Formatting...
        self.code_block_string = ''
        self.last_marker = None
        self.node_counter = 0
        self.toplevel = 0
        self.topNode = None
        self.use_alternate_code_block = SilverCity is None
        
        # Http support...
        self.http_map = {}
            # A node anchor is a marker beginning with node_begin_marker.
            # We assume that such markers do not occur in the rst document.
        
        # For writing.
        self.defaultEncoding = 'utf-8'
        self.leoDirectivesList = leoColor.leoKeywords
        self.encoding = self.defaultEncoding
        self.ext = None # The file extension.
        self.outputFileName = None # The name of the file being written.
        self.outputFile = None # The open file being written.
        #@nonl
        #@-node:ekr.20050805162550.11:<< init ivars >>
        #@nl
    
        self.createDefaultOptionsDict()
        self.initOptionsFromSettings() # Make sure all associated ivars exist.
        self.initHeadlineCommands() # Only needs to be done once.
        self.initSingleNodeOptions()
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
        
        # Warning: changing the names of options changes the names of the corresponding ivars.
        
        self.defaultOptionsDict = {
            # Http options...
            'rst3_clear_http_attributes':   False,
            'rst3_http_server_support':     False,
            'rst3_http_attributename':      'rst_http_attribute',
            'rst3_node_begin_marker':       'http-node-marker-',
            # Path options...
            'rst3_stylesheet_name': 'default.css',
            'rst3_stylesheet_path': '',
            # Global options...
            'rst3_number_code_lines': True,
            'rst3_underline_characters': '''#=+*^~"'`-:><_''',
            'rst3_verbose':True,
            'rst3_write_intermediate_file': False, # Used only if generate_rst is True.
            # Mode options...
            'rst3_code_mode': False, # True: generate rst markup from @code and @doc parts.
            'rst3_generate_rst': True, # True: generate rst markup.  False: generate plain text.
            # Formatting options that apply to both code and rst modes....
            'rst3_show_headlines': True,  # Can be set by @rst-no-head headlines.
            'rst3_show_organizer_nodes': True,
            # Formatting options that apply only to code mode.
            'rst3_show_doc_parts_as_paragraphs': False,
            'rst3_show_leo_directives': True,
            'rst3_show_markup_doc_parts': False,
            'rst3_show_options_doc_parts': False,
         
            # Names of headline commands...
            'rst3_code_prefix':             '@rst-code', # Enter code mode.
            'rst3_rst_prefix':              '@rst',      # Enter rst mode.
            'rst3_ignore_headline_prefix':  '@rst-no-head',
            'rst3_ignore_headlines_prefix': '@rst-no-headlines',
            'rst3_ignore_node_prefix':      '@rst-ignore-node',
            'rst3_ignore_tree_prefix':      '@rst-ignore-tree',
            'rst3_option_prefix':           '@rst-option',
            'rst3_options_prefix':          '@rst-options',
            'rst3_show_headline_prefix':    '@rst-head',
        }
    #@nonl
    #@-node:ekr.20050808064245:createDefaultOptionsDict
    #@+node:ekr.20050813083007:initHeadlineCommands
    def initHeadlineCommands (self):
    
        '''Init the list of headline commands used by writeHeadline.'''
    
        self.headlineCommands = [
            self.code_prefix,
            self.rst_prefix,
            self.ignore_headline_prefix,
            self.ignore_headlines_prefix,
            self.ignore_node_prefix,
            self.ignore_tree_prefix,
            self.option_prefix,
            self.options_prefix,
            self.show_headline_prefix,
        ]
    #@nonl
    #@-node:ekr.20050813083007:initHeadlineCommands
    #@+node:ekr.20050813085236:initSingleNodeOptions
    def initSingleNodeOptions (self):
        
        self.singleNodeOptions = [
            'ignore_this_headline',
            'show_this_headline',
            'skip_this_node',
            'skip_this_tree',
        ]
    #@nonl
    #@-node:ekr.20050813085236:initSingleNodeOptions
    #@+node:ekr.20050808072943:munge
    def munge (self,name):
        
        '''Convert an option name to the equivalent ivar name.'''
        
        i = g.choose(name.startswith('rst'),3,0)
    
        while i < len(name) and name[i].isdigit():
            i += 1
    
        if i < len(name) and name[i] == '_':
            i += 1
        
        s = name[i:].lower()
        s = s.replace('-','_')
        
        return s
    #@nonl
    #@-node:ekr.20050808072943:munge
    #@-node:ekr.20050805162550.9: Birth & init
    #@+node:ekr.20050805162550.16:encode
    def encode (self,s):
    
        return g.toEncodedString(s,encoding=self.encoding,reportErrors=True)
    #@nonl
    #@-node:ekr.20050805162550.16:encode
    #@+node:ekr.20050812122236:options...
    #@+node:ekr.20050812120933:dumpSettings
    def dumpSettings (self):
        
        d = self.defaultOptionsDict
        keys = d.keys() ; keys.sort()
        
        print 'present settings...'
        for key in keys:
            print '%20s %s' % (key,d.get(key))
    #@nonl
    #@-node:ekr.20050812120933:dumpSettings
    #@+node:ekr.20050807120331.1:preprocessTree & helpers
    def preprocessTree (self,root):
        
        # g.trace(self.topNode)
        
        self.tnodeOptionDict = {}
        
        for p in root.self_and_subtree_iter():
            d = self.tnodeOptionDict.get(p.v.t)
            if not d:
                d = self.scanNodeForOptions(p)
                if d:
                    self.tnodeOptionDict [p.v.t] = d
        if 0:
            g.trace(root.headString())
            g.printDict(self.tnodeOptionDict)
    #@nonl
    #@+node:ekr.20050808072943.1:parseOptionLine
    def parseOptionLine (self,s):
    
        '''Parse a line containing name=val and return (name,value) or None.
        
        If no value is found, default to True.'''
    
        s = s.strip()
        if s.endswith(','): s = s[:-1]
        # Get name.  Names may contain '-' and '_'.
        i = g.skip_id(s,0,chars='-_')
        name = s [:i]
        if not name: return None
        j = g.skip_ws(s,i)
        if g.match(s,j,'='):
            val = s [j+1:].strip()
            # g.trace(val)
            return name,val
        else:
            # g.trace('*True')
            return name,'True'
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
                        line = lines[n] ; n += 1 ; found = False
                        for stop in ('@c','@code', '@'):
                            if g.match_word(line,0,stop):
                                found = True ; break
                        if found:
                            break
                        else:
                            d2 = self.scanOption(p,line)
                            if d2: d.update(d2)
        return d
    #@nonl
    #@-node:ekr.20050808070018.2:scanForOptionDocParts
    #@+node:ekr.20050811173750:scanHeadlineForOptions
    def scanHeadlineForOptions (self,p):
        
        '''Return a dictionary containing the options implied by p's headline.'''
        
        h = p.headString().strip()
        
        if p == self.topNode:
            return {} # Don't mess with the root node.
        elif g.match_word(h,0,self.option_prefix): # '@rst-option'
            s = h [len(self.option_prefix):]
            return self.scanOption(p,s)
        elif g.match_word(h,0,self.options_prefix): # '@rst-options'
            return self.scanOptions(p,p.bodyString())
        else:
            # Careful: can't use g.match_word because options may have '-' chars.
            i = g.skip_id(h,0,chars='@-')
            word = h[0:i]
            
            for prefix,ivar,val in (
                (self.code_prefix,'code_mode',True), # '@rst-code' 
                (self.rst_prefix,'code_mode',False), # '@rst'    
                (self.ignore_headline_prefix,'ignore_this_headline',True), # '@rst-no-head'
                (self.show_headline_prefix,'show_this_headline',True), # '@rst-head'  
                (self.ignore_headlines_prefix,'show_headlines',False), # '@rst-no-headlines'
                (self.ignore_node_prefix,'ignore_node',True), # '@rst-ignore-node'
                (self.ignore_tree_prefix,'ignore_tree',True), # '@rst-ignore-tree'
            ):
                if word == prefix: # Do _not_ munge this prefix!
                    d = { ivar: val }
                    if ivar != 'code_mode':
                        d ['code_mode'] = False # Enter rst mode.
                    # Special case: Treat a bare @rst like @rst-no-head
                    if h == self.rst_prefix:
                        d ['ignore_this_headline'] = True
                    # g.trace(repr(h),repr(prefix),ivar,d)
                    return d
                    
            if h.startswith('@rst'):
                g.trace('unknown kind of @rst headline',p.headString())
                    
            return {}
    #@-node:ekr.20050811173750:scanHeadlineForOptions
    #@+node:ekr.20050807120331.2:scanNodeForOptions
    def scanNodeForOptions (self,p):
    
        '''Return a dictionary containing all the option-name:value entries in p.
        
        Such entries may arise from @rst-option or @rst-options in the headline,
        or from @ @rst-options doc parts.'''
    
        h = p.headString()
        
        d = self.scanHeadlineForOptions(p)
    
        d2 = self.scanForOptionDocParts(p,p.bodyString())
        
        # A fine point: body options over-ride headline options.
        d.update(d2)
    
        return d
    #@nonl
    #@-node:ekr.20050807120331.2:scanNodeForOptions
    #@+node:ekr.20050808070018:scanOption
    def scanOption (self,p,s):
        
        '''Return { name:val } if s is a line of the form name=val.
        Otherwise return {}'''
        
        if not s.strip() or s.strip().startswith('..'): return None
        
        data = self.parseOptionLine(s)
    
        if data:
            name,val = data
            fullName = 'rst3_' + self.munge(name)
            if fullName in self.defaultOptionsDict.keys():
                if   val.lower() == 'true': val = True
                elif val.lower() == 'false': val = False
                # g.trace('%24s %8s %s' % (self.munge(name),val,p.headString()))
                return { self.munge(name): val }
            else:
                g.es_print('ignoring unknown option: %s' % (name),color='red')
                return {}
        else:
            g.trace(repr(s))
            s2 = 'bad rst3 option in %s: %s' % (p.headString(),s)
            g.es_print(s2,color='red')
            return {}
    #@nonl
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
    #@+node:ekr.20050808142313.28:scanAllOptions & helpers
    # Once an option is seen, no other related options in ancestor nodes have any effect.
    
    def scanAllOptions(self,p):
        
        '''Scan position p and p's ancestors looking for options,
        setting corresponding ivars.
        '''
        
        self.initOptionsFromSettings() # Must be done on every node.
        self.handleSingleNodeOptions(p)
        seen = self.singleNodeOptions[:] # Suppress inheritance of single-node options.
        # g.trace('-'*20)
        for p in p.self_and_parents_iter():
            d = self.tnodeOptionDict.get(p.v.t, {})
            # g.trace(p.headString(),d)
            for key in d.keys():
                ivar = self.munge(key)
                if not ivar in seen:
                    seen.append(ivar)
                    val = d.get(key)
                    self.setIvar(key,val,p.headString())
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
                    self.setIvar(key,val,'initOptionsFromSettings')
                    break
    
        # Special case.
        if self.http_server_support and not mod_http:
            g.es('No http_server_support: can not import mod_http plugin',color='red')
            self.http_server_support = False
    #@nonl
    #@-node:ekr.20050805162550.13:initOptionsFromSettings
    #@+node:ekr.20050810103731:handleSingleNodeOptions
    def handleSingleNodeOptions (self,p):
    
        '''Init the settings of single-node options from the tnodeOptionsDict.
        
        All such options default to False.'''
        
        d = self.tnodeOptionDict.get(p.v.t, {} )
        
        for ivar in self.singleNodeOptions:
            val = d.get(ivar,False)
            #g.trace('%24s %8s %s' % (ivar,val,p.headString()))
            self.setIvar(ivar,val,p.headString())
    #@nonl
    #@-node:ekr.20050810103731:handleSingleNodeOptions
    #@-node:ekr.20050808142313.28:scanAllOptions & helpers
    #@+node:ekr.20050811135526:setIvar
    def setIvar (self,name,val,tag):
        
        ivar = self.munge(name)
             
        if 0: 
            if not hasattr(self,ivar):
                g.trace('init %24s %20s %s' % (ivar,val,tag))
            elif getattr(self,ivar) != val:
                g.trace('set  %24s %20s %s' % (ivar,val,tag))
        
        setattr(self,ivar,val)
    #@nonl
    #@-node:ekr.20050811135526:setIvar
    #@-node:ekr.20050812122236:options...
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
            self.code_block_string = '**code**:\n\n.. code-block:: %s\n' % language.title()
        else:
            self.code_block_string = '**code**:\n\n.. class:: code\n..\n\n::\n'
    #@nonl
    #@-node:ekr.20050809075309:initWrite
    #@+node:ekr.20050809080925:writeNormalTree
    def writeNormalTree (self,p):
    
        self.initWrite(p)
        self.outputFile = file(self.outputFileName,'w')
        self.writeTree(p)
        self.outputFile.close()
    #@nonl
    #@-node:ekr.20050809080925:writeNormalTree
    #@+node:ekr.20050805162550.17:processTree
    def processTree(self,p):
        
        '''Process all @rst nodes in a tree.'''
    
        self.topNode = p.copy()
        self.preprocessTree(p)
        found = False
        p = p.copy() ; after= p.nodeAfterTree()
        while p and p != after:
            h = p.headString().strip()
            if g.match_word(h,0,"@rst"):
                self.outputFileName = h[4:].strip()
                if self.outputFileName and self.outputFileName[0] != '-':
                    found = True
                    self.ext = ext = g.os_path_splitext(self.outputFileName)[1].lower()
                    if ext in ('.htm','.html','.tex'):
                        self.writeSpecialTree(p)
                    else:
                        self.writeNormalTree(p)
                    self.scanAllOptions(p) # Restore the top-level verbose setting.
                    self.report(self.outputFileName)
                    p.moveToNodeAfterTree()
                else:
                    p.moveToThreadNext()
            else: p.moveToThreadNext()
        if not found:
            g.es('No @rst nodes in selected tree',color='blue')
    #@nonl
    #@-node:ekr.20050805162550.17:processTree
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
    
        if self.write_intermediate_file:
            name = self.outputFileName + '.txt'
            f = file(name,'w')
            f.write(source)
            f.close()
            self.report(name)
            
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
    #@+node:ekr.20050809082854.1:writeToDocutils (sets argv)
    def writeToDocutils (self,s,isHtml):
        
        '''Send s to docutils and return the result.'''
    
        pub = docutils.core.Publisher()
    
        pub.source      = docutils.io.StringInput(source=s)
        pub.destination = docutils.io.StringOutput(pub.settings,encoding=self.encoding)
    
        pub.set_reader('standalone',None,'restructuredtext')
        pub.set_writer(g.choose(isHtml,'html','latex'))
        
        path = g.os_path_abspath(g.os_path_join(self.stylesheet_path, self.stylesheet_name))
        
        if g.os_path_exists(path):
            return pub.publish(argv=['--stylesheet=%s' % path])
        else:
            g.es_print('stylesheet does not exist: %s' % (path),color='red')
            return pub.publish(argv=[])
    #@nonl
    #@-node:ekr.20050809082854.1:writeToDocutils (sets argv)
    #@-node:ekr.20050809082854: Top-level write code
    #@+node:ekr.20050805162550.23:writeTree
    def writeTree(self,p):
        
        '''Write p's tree to self.outputFile.'''
    
        self.scanAllOptions(p)
        self.toplevel = p.level()
    
        if self.generate_rst:
            self.write(self.rstComment('rst3: filename: %s\n\n' % self.outputFileName))
            
        # We can't use an iterator because we may skip parts of the tree.
        p = p.copy() # Only one copy is needed.
        after = p.nodeAfterTree()
        while p and p != after:
            self.writeNode(p)
    #@nonl
    #@-node:ekr.20050805162550.23:writeTree
    #@+node:ekr.20050810083057:writeNode
    def writeNode (self,p):
        
        '''Format a node according to the options presently in effect.'''
        
        self.scanAllOptions(p)
        
        if 0:
            g.trace('%24s code_mode %s' % (p.headString(),self.code_mode))
        
        if self.skip_this_tree:
            p.moveToNodeAfterTree()
        elif self.skip_this_node:
            p.moveToThreadNext()
        else:
            h = p.headString().strip()
            if g.match_word(h,0,'@rst-options') and not self.show_options_nodes:
                pass
            else:
                self.writeHeadline(p)
                self.writeBody(p)
        
            p.moveToThreadNext()
    #@nonl
    #@-node:ekr.20050810083057:writeNode
    #@+node:ekr.20050811101550.1:writeBody & helpers
    def writeBody (self,p):
        
        # remove trailing cruft and split into lines.
        lines = p.bodyString().rstrip().split('\n') 
    
        if self.code_mode:
            if not self.show_options_doc_parts:
                lines = self.handleSpecialDocParts(lines,'@rst-options',
                    retainContents=False)
            if not self.show_markup_doc_parts:
                lines = self.handleSpecialDocParts(lines,'@rst-markup',
                    retainContents=False)
            if not self.show_leo_directives:
                lines = self.removeLeoDirectives(lines)
            lines = self.handleCodeMode(lines)
        else:
            lines = self.handleSpecialDocParts(lines,'@rst-options',
                retainContents=False)
            lines = self.handleSpecialDocParts(lines,'@rst-markup',
                retainContents=self.generate_rst)
            lines = self.removeLeoDirectives(lines)
            if self.generate_rst and self.use_alternate_code_block:
                lines = self.replaceCodeBlockDirectives(lines)
    
        s = '\n'.join(lines).strip()
        if s:
            self.write('%s\n\n' % s)
    #@nonl
    #@+node:ekr.20050811154552:getDocPart
    def getDocPart (self,lines,n):
    
        result = []
        while n < len(lines):
            s = lines [n] ; n += 1
            if g.match_word(s,0,'@code') or g.match_word(s,0,'@c'):
                break
            result.append(s)
        return n, result
    #@nonl
    #@-node:ekr.20050811154552:getDocPart
    #@+node:ekr.20050811150541:handleCodeMode & helper
    def handleCodeMode (self,lines):
    
        '''Handle the preprocessed body text in code mode as follows:
            
        - Blank lines are copied after being cleaned.
        - @ @rst-markup lines get copied as is.
        - Everything else gets put into a code-block directive.'''
    
        result = [] ; n = 0 ; code = []
        while n < len(lines):
            s = lines [n] ; n += 1
            if (
                self.isSpecialDocPart(s,'@rst-markup') or
                (self.show_doc_parts_as_paragraphs and self.isSpecialDocPart(s,None))
            ):
                if code:
                    self.finishCodePart(result,code)
                    code = []
                result.append('')
                n, lines2 = self.getDocPart(lines,n)
                result.extend(lines2)
            elif not s.strip() and not code:
                pass # Ignore blank lines before the first code block.
            elif not code: # Start the code block.
                result.append('')
                result.append(self.code_block_string)
                code.append(s)
            else: # Continue the code block.
                code.append(s)
    
        if code:
            self.finishCodePart(result,code)
            code = []
        return self.rstripList(result)
    #@nonl
    #@+node:ekr.20050811152104:formatCodeModeLine
    def formatCodeModeLine (self,s,n):
        
        if not s.strip(): s = ''
        
        if self.number_code_lines:
            return '\t%d: %s' % (n,s)
        else:
            return '\t%s' % s
    #@nonl
    #@-node:ekr.20050811152104:formatCodeModeLine
    #@+node:ekr.20050813155021:rstripList
    def rstripList (self,theList):
        
        '''Removed trailing blank lines from theList.'''
        
        s = '\n'.join(theList).rstrip()
        return s.split('\n')
    #@nonl
    #@-node:ekr.20050813155021:rstripList
    #@+node:ekr.20050813160208:finishCodePart
    def finishCodePart (self,result,code):
        
        code = self.rstripList(code)
        i = 0
        for line in code:
            i += 1
            result.append(self.formatCodeModeLine(line,i))
    #@nonl
    #@-node:ekr.20050813160208:finishCodePart
    #@-node:ekr.20050811150541:handleCodeMode & helper
    #@+node:ekr.20050811153208:isSpecialDocPart
    def isSpecialDocPart (self,s,kind):
        
        '''Return True if s is a special doc part of the indicated kind.
        
        If kind is None, return True if s is any doc part.'''
        
        if s.startswith('@') and len(s) > 1 and s[1].isspace():
            if kind:
                i = g.skip_ws(s,1)
                result = g.match_word(s,i,kind)
            else:
                result = True
        elif not kind:
            result = g.match_word(s,0,'@doc') or g.match_word(s,0,'@')
        else:
            result = False
            
        return result
    #@nonl
    #@-node:ekr.20050811153208:isSpecialDocPart
    #@+node:ekr.20050811163802:isAnySpecialDocPart
    def isAnySpecialDocPart (self,s):
        
        for kind in (
            '@rst-markup',
            '@rst-option',
            '@rst-options',
        ):
            if self.isSpecialDocPart(s,kind):
                return True
    
        return False
    #@-node:ekr.20050811163802:isAnySpecialDocPart
    #@+node:ekr.20050811105438:removeLeoDirectives
    def removeLeoDirectives (self,lines):
    
        '''Remove all Leo directives, except within literal blocks.'''
    
        n = 0 ; result = []
        while n < len(lines):
            s = lines [n] ; n += 1
            if s.strip().endswith('::'):
                n, lit = self.skip_literal_block(lines,n-1)
                result.extend(lit)
            elif s.startswith('@') and not self.isAnySpecialDocPart(s):
                for key in self.leoDirectivesList:
                    if g.match_word(s,0,key):
                        # g.trace('removing %s' % s)
                        break
                else:
                    result.append(s)
            else:
                result.append(s)
    
        return result
    #@nonl
    #@-node:ekr.20050811105438:removeLeoDirectives
    #@+node:ekr.20050811105438.1:handleSpecialDocParts
    def handleSpecialDocParts (self,lines,kind,retainContents):
    
        n = 0 ; result = []
        while n < len(lines):
            s = lines [n] ; n += 1
            if s.strip().endswith('::'):
                n, lit = self.skip_literal_block(lines,n-1)
                result.extend(lit)
            elif self.isSpecialDocPart(s,kind):
                n, lines2 = self.getDocPart(lines,n)
                if retainContents:
                    result.extend(lines2)
            else:
                result.append(s)
    
        return result
    #@nonl
    #@-node:ekr.20050811105438.1:handleSpecialDocParts
    #@+node:ekr.20050805162550.30:replaceCodeBlockDirectives
    def replaceCodeBlockDirectives (self,lines):
    
        '''Replace code-block directive, but not in literal blocks.'''
    
        n = 0 ; result = []
        while n < len(lines):
            s = lines [n] ; n += 1
            if s.strip().endswith('::'):
                n, lit = self.skip_literal_block(lines,n-1)
                result.extend(lit)
            else:
                i = g.skip_ws(s,0)
                if g.match(s,i,'..'):
                    i = g.skip_ws(s,i+2)
                    if g.match_word(s,i,'code-block'):
                        if 1: # Create a literal block to hold the code.
                            result.append('::\n')
                        else: # This 'annotated' literal block is confusing.
                            result.append('%s code::\n' % s[i+len('code-block'):])
                    else:
                        result.append(s)
                else:
                    result.append(s)
    
        return result
    #@nonl
    #@-node:ekr.20050805162550.30:replaceCodeBlockDirectives
    #@-node:ekr.20050811101550.1:writeBody & helpers
    #@+node:ekr.20050805162550.26:writeHeadline
    def writeHeadline (self,p):
    
        '''Generate an rST section if options permit it.
        Remove headline commands from the headline first,
        and never generate an rST section for @rst-option and @rst-options.'''
    
        h = p.headString().strip()
        
        if 0:
            g.trace('isTop:%-5s ignore_this:%-5s show_this:%-5s show:%-5s h: %s' % (
                p == self.topNode,
                self.ignore_this_headline,self.show_this_headline,
                self.show_headlines,h))
    
        if (
            p == self.topNode or
            (not h and not self.show_organizer_nodes) or
            self.ignore_this_headline or
            (not self.show_headlines and not self.show_this_headline) or 
            (not self.show_organizer_nodes and not p.bodyString().strip())
        ):
            return
    
        # Remove any headline command before writing the 
        i = g.skip_id(h,0,chars='@-')
        word = h [:i]
        if word:
            # Never generate a section for @rst-option or @rst-options.
            if word in (self.option_prefix,self.options_prefix):
                return
            # Remove all other headline commands from the headline.
            for prefix in self.headlineCommands:
                if word == prefix:
                    h = h [len(word):].strip()
                    break
    
        if self.generate_rst:
            self.write('%s\n%s\n' % (h,self.underline(h,p.level())))
        else:
            self.write('\n%s\n' % h)
    #@nonl
    #@-node:ekr.20050805162550.26:writeHeadline
    #@+node:ekr.20050811102607:skip_literal_block
    def skip_literal_block (self,lines,n):
        
        s = lines[n] ; result = [s] ; n += 1
        indent = g.skip_ws(s,0)
    
        # Skip lines until a non-blank line is found with same or less indent.
        while n < len(lines):
            s = lines[n]
            indent2 = g.skip_ws(s,0)
            if s and not s.isspace() and indent2 <= indent:
                break # We will rescan lines [n]
            n += 1
            result.append(s)
        
        # g.printList(result,tag='literal block')
        return n, result
    #@nonl
    #@-node:ekr.20050811102607:skip_literal_block
    #@-node:ekr.20050809074827:write methods
    #@+node:ekr.20050810083314:Utils
    #@+node:ekr.20050805162550.20:report
    def report (self,name):
    
        if self.verbose:
            
            name = g.os_path_abspath(name)
    
            g.es_print('wrote: %s' % (name),color="blue")
    #@nonl
    #@-node:ekr.20050805162550.20:report
    #@+node:ekr.20050810083856:rstComment
    def rstComment (self,s):
        
        return '.. %s' % s
    #@nonl
    #@-node:ekr.20050810083856:rstComment
    #@+node:ekr.20050805162550.19:underline
    def underline (self,s,level):
    
        '''Return the underlining string to be used at the given level for string s.'''
    
        u = self.underline_characters #  '''#=+*^~"'`-:><_'''
        
        level1 = level
        level = max(0,level-self.toplevel)
        level = min(level+1,len(u)-1) # Reserve the first character for explicit titles.
        
        # g.trace(level1,self.toplevel,level)
    
        ch = u [level]
    
        n = max(4,len(s))
    
        return ch * n + '\n'
    #@nonl
    #@-node:ekr.20050805162550.19:underline
    #@+node:ekr.20050809080031:write
    def write (self,s):
        
        s = self.encode(s)
        
        self.outputFile.write(s)
    #@nonl
    #@-node:ekr.20050809080031:write
    #@-node:ekr.20050810083314:Utils
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
