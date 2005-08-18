#! /usr/bin/env python
#@+leo-ver=4
#@+node:@file C:/Python24/Lib/site-packages/docutils/writers/leo_pdf.py
#@@first

#@<< docstring >>
#@+node:<< docstring >>
'''This is a docutils writer that emits a pdf file using the reportlab module.

The original code written by Engelbert Gruber.
Rewritten by Edward K. Ream for the Leo rst3 plugin.

'''
#@-node:<< docstring >>
#@nl

# Note: you must copy this file to the Python/Lib/site-packages/docutils/writers folder.

# This file is derived from rlpdf.py at 
# The copyright below applies only to this file.

#@@language python
#@@tabwidth -4

#@<< copyright >>
#@+node:<< copyright >>
#####################################################################################
#
#	Copyright (c) 2000-2001, ReportLab Inc.
#	All rights reserved.
#
#	Redistribution and use in source and binary forms, with or without modification,
#	are permitted provided that the following conditions are met:
#
#		*	Redistributions of source code must retain the above copyright notice,
#			this list of conditions and the following disclaimer. 
#		*	Redistributions in binary form must reproduce the above copyright notice,
#			this list of conditions and the following disclaimer in the documentation
#			and/or other materials provided with the distribution. 
#		*	Neither the name of the company nor the names of its contributors may be
#			used to endorse or promote products derived from this software without
#			specific prior written permission. 
#
#	THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
#	ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
#	WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
#	IN NO EVENT SHALL THE OFFICERS OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
#	INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED
#	TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS;
#	OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
#	IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
#	IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
#	SUCH DAMAGE.
#
#####################################################################################
#@nonl
#@-node:<< copyright >>
#@nl
#@<< version history >>
#@+node:<< version history >>
#@@nocolor
#@+others
#@+node:Initial conversion
#@+at
# 
# - Added 'c:\reportlab_1_20' to sys.path.
# 
# - Obtained this file and stylesheet.py from
#   http://docutils.sourceforge.net/sandbox/dreamcatcher/rlpdf/
# 
# - Put stylesheet.py in docutils/writers directory.
#   This is a stylesheet class used by the file.
# 
# - Made minor mods to stop crashes.
#     - Added support for the '--stylesheet' option.
#         - This may be doing more harm than good.
#     - Changed the following methods of the PDFTranslator class:
#         - createParagraph
#         - depart_title
#@-at
#@nonl
#@-node:Initial conversion
#@+node:0.0.1
#@+at
# 
# - Removed '\r' characters in Writer.translate.
# - Created self.push and self.pop.
# - Rewrote visit/depart_title.  The code now is clear and works properly.
# 
# To do:
#     The code in several places uses x in self.context.
#     This won't work when g.Bunches are on the context stack,
#     so we shall need a method that searches the bunches on the stack.
#@-at
#@nonl
#@-node:0.0.1
#@+node:0.0.2
#@+at
# 
# - Fixed bug in visit_reference: added self.push(b).
#@-at
#@nonl
#@-node:0.0.2
#@-others
#@nonl
#@-node:<< version history >>
#@nl

__version__ = '0.0.2'
__docformat__ = 'reStructuredText'
#@<< imports >>
#@+node:<< imports >>
import sys
sys.path.append(r'c:\reportlab_1_20') 

import leoGlobals as g

# Formatting imports...
import docutils
import reportlab.platypus
import reportlab.platypus.para
import stylesheet # To do: get this a better way.

# General imports...
import StringIO
import time
import types







#@-node:<< imports >>
#@nl

#@+others
#@+node:class Writer (docutils.writers.Writer)
class Writer (docutils.writers.Writer):
	
    #@	<< class Writer declarations >>
    #@+node:<< class Writer declarations >>
    supported = ('pdf','rlpdf')
    """Formats this writer supports."""
    
    settings_spec = (
        'PDF-Specific Options',
        None,
        (
            # EKR: added this entry.
        (   'Specify a stylesheet URL, used verbatim.  Overrides '
            '--stylesheet-path.  Either --stylesheet or --stylesheet-path '
            'must be specified.',
            ['--stylesheet'],
            {'metavar': '<URL>', 'overrides': 'stylesheet_path'}),
             
        (   'Specify a stylesheet file, relative to the current working '
            'directory.  The path is adjusted relative to the output HTML '
            'file.  Overrides --stylesheet.',
            ['--stylesheet-path'],
            {'metavar': '<file>', 'overrides': 'stylesheet'}),
    
        (   'Format for footnote references: one of "superscript" or '
            '"brackets".  Default is "brackets".',
            ['--footnote-references'],
            {'choices': ['superscript', 'brackets'], 'default': 'brackets',
            'metavar': '<FORMAT>'}),
        )
    )
    
    output = None
    """Final translated form of `document`."""
    #@nonl
    #@-node:<< class Writer declarations >>
    #@nl

    #@	@+others
    #@+node:__init__
    def __init__(self):
    
        docutils.writers.Writer.__init__(self)
    
        # self.translator_class = PDFTranslator
    #@-node:__init__
    #@+node:translate
    def translate(self):
        
        # Create a list of paragraphs using Platypus.
        visitor = PDFTranslator(self.document)
        self.document.walkabout(visitor)
        story = visitor.as_what()
        
        if 0:
            g.trace('story','*'*40)
            g.printList(story)
        
        # Create the .pdf file using Platypus.
        self.output = self.createPDF_usingPlatypus(story)
        
        # Solve the newline problem by brute force.
        self.output = self.output.replace('\r','')
        
        if 0:
            g.trace('output','*'*40)
            lines = g.splitLines(self.output)
            g.printList(lines)
    #@nonl
    #@-node:translate
    #@+node:createPDF_usingPlatypus
    def createPDF_usingPlatypus (self,story):
    
        out = StringIO.StringIO()
    
        doc = reportlab.platypus.SimpleDocTemplate(out,
            pagesize=reportlab.lib.pagesizes.A4)
        
        doc.build(story)
    
        return out.getvalue()
    #@-node:createPDF_usingPlatypus
    #@+node:lower
    def lower(self):
    
        return 'pdf'
    #@nonl
    #@-node:lower
    #@-others
#@nonl
#@-node:class Writer (docutils.writers.Writer)
#@+node:class PDFTranslator (docutils.nodes.NodeVisitor)
class PDFTranslator (docutils.nodes.NodeVisitor):

    #@	@+others
    #@+node:__init__
    def __init__(self, doctree):
    
        self.settings = settings = doctree.settings
        self.styleSheet = stylesheet.getStyleSheet()
        docutils.nodes.NodeVisitor.__init__(self, doctree) # Init the base class.
        self.language = docutils.languages.get_language(doctree.settings.language_code)
        self.in_docinfo = None
        self.head = []
        self.body = []
        self.foot = []
        self.sectionlevel = 0
        self.context = []
        self.topic_class = ''
        self.story = []
        self.bulletText = '\267'	# maybe move this into stylesheet.
        self.bulletlevel = 0
    #@nonl
    #@-node:__init__
    #@+node:Utilities
    #@+node:as_what
    def as_what(self):
    
        return self.story
    #@-node:as_what
    #@+node:inContext
    def inContext (self,kind):
        
        '''Return true if any context bunch has the indicated kind.'''
        
        g.trace(kind)
        
        for obj in self.context:
            # Eventually everything on the context stack will be a g.Bunch.
            try:
                if kind == obj:
                    return True
                if kind == obj.kind:
                    return True
            except Exception:
                pass
    
        return False
    #@nonl
    #@-node:inContext
    #@+node:dumpContext
    def dumpContext (self):
        
        print ; print '-' * 40
        print 'Dump of context'
            
        i = 0
        for obj in self.context:
            print '%2d %s' % (i,obj)
            i += 1
    #@nonl
    #@-node:dumpContext
    #@+node:encode
    def encode(self, text):
    
        """Encode special characters in `text` & return."""
        if type(text) is types.UnicodeType:
            text = text.replace(u'\u2020', u' ')
            text = text.replace(u'\xa0', u' ')
            text = text.encode('utf-8')
        #text = text.replace("&", "&amp;")
        #text = text.replace("<", '"')
        #text = text.replace('"', "(quot)")
        #text = text.replace(">", '"')
        # footnotes have character values above 128 ?
        return text
    #@-node:encode
    #@+node:push & pop
    def push (self,bunch):
        
        self.context.append(bunch)
        
    def pop (self,kind):
        
        bunch = self.context.pop()
        assert bunch.kind == kind,'wrong bunch kind popped.  Expected: %s Got: %s' % (
            kind, bunch.kind)
    
        return bunch
    #@nonl
    #@-node:push & pop
    #@-node:Utilities
    #@+node:putHead & putTail
    def putHead (self,start,style='Normal',bulletText=None):
        
        self.createParagraph(self.body[:start],
            style=style,bulletText=bulletText)
    
        self.body = self.body[start:]
    
    
    def putTail (self,start,style='Normal',bulletText=None):
        
        self.createParagraph(self.body[start:],
            style=style,bulletText=bulletText)
    
        self.body = self.body[:start]
    #@-node:putHead & putTail
    #@+node:createParagraph
    def createParagraph (self,text,style='Normal',bulletText=None):
    
        if type(text) in (types.ListType,types.TupleType):
            text = ''.join([self.encode(t) for t in text])
    
        if not style.strip(): ### EKR
            style = 'Normal'
            
        g.trace('%8s, text: %s' % (style,repr(text)))
    
        style = self.styleSheet [style]
        
        try:
            self.story.append(
                reportlab.platypus.para.Paragraph (
                    self.encode(text), style,
                    bulletText = bulletText,
                    context = self.styleSheet))
        except Exception:
            g.es_print('Exception in createParagraph')
            g.es_exception()
            self.dumpContext()
            raise
    #@nonl
    #@-node:createParagraph
    #@+node:starttag
    def starttag (self,node,tagname,suffix='\n',**attributes):
        
        g.trace(tagname,repr(node))
        atts = {}
        for (name,value) in attributes.items():
            atts [name.lower()] = value
        for att in ('class',): # append to node attribute
            if node.has_key(att):
                if atts.has_key(att):
                    atts [att] = node [att] + ' ' + atts [att]
        for att in ('id',): # node attribute overrides
            if node.has_key(att):
                atts [att] = node [att]
        
        attlist = atts.items() ; attlist.sort()
        parts = [tagname]
        for name, value in attlist:
            if value is None: # boolean attribute
                parts.append(name.lower())
            elif isinstance(value,types.ListType):
                values = [str(v) for v in value]
                parts.append('%s="%s"' % (
                    name.lower(),
                    self.encode(' '.join(values))))
            else:
                parts.append('%s="%s"' % (
                    name.lower(),
                    self.encode(str(value))))
    
        return '<%s>%s' % (' '.join(parts),suffix)
    #@-node:starttag
    #@+node:Node handlers...
    #@+node:  do nothings...
    #@+node:authors
    def visit_authors(self, node):
        pass
    
    def depart_authors(self, node):
        pass
    #@-node:authors
    #@+node:block_quote
    def visit_block_quote(self, node):
        pass
        
    def depart_block_quote(self, node):
        pass
    #@nonl
    #@-node:block_quote
    #@+node:caption
    def visit_caption(self, node):
        pass
    
    def depart_caption(self, node):
        pass
    #@-node:caption
    #@+node:citation
    def visit_citation(self, node):
        pass
    
    def depart_citation(self, node):
        pass
    #@-node:citation
    #@+node:citation_reference
    def visit_citation_reference(self, node):
        pass
    
    def depart_citation_reference(self, node):
        pass
    #@-node:citation_reference
    #@+node:classifier
    def visit_classifier(self, node):
        pass
    
    def depart_classifier(self, node):
        pass
    #@-node:classifier
    #@+node:colspec
    def visit_colspec(self, node):
        pass
    
    def depart_colspec(self, node):
        pass
    #@-node:colspec
    #@+node:definition_list_item
    def visit_definition_list_item(self, node):
        pass
    
    def depart_definition_list_item(self, node):
        pass
    #@nonl
    #@-node:definition_list_item
    #@+node:description
    def visit_description(self, node):
        pass
    
    def depart_description(self, node):
        pass
    #@-node:description
    #@+node:document
    def visit_document(self, node):
        pass
    
    def depart_document(self, node):
        pass
    #@-node:document
    #@+node:entry
    def visit_entry(self, node):
        pass
    
    def depart_entry(self, node):
        pass
    #@-node:entry
    #@+node:field_argument
    def visit_field_argument(self, node):
        pass
    
    def depart_field_argument(self, node):
        pass
    #@-node:field_argument
    #@+node:field_body
    def visit_field_body(self, node):
        pass
    
    def depart_field_body(self, node):
        pass
    #@-node:field_body
    #@+node:generated
    def visit_generated(self, node):
        pass
    
    def depart_generated(self, node):
        pass
    #@-node:generated
    #@+node:image
    def visit_image(self, node):
        pass
    
    def depart_image(self, node):
        pass
    #@-node:image
    #@+node:interpreted
    def visit_interpreted(self, node):
        pass
    
    def depart_interpreted(self, node):
        pass
    #@-node:interpreted
    #@+node:legend
    def visit_legend(self, node):
        pass
    
    def depart_legend(self, node):
        pass
    #@-node:legend
    #@+node:option
    def visit_option(self, node):
        pass
    
    def depart_option(self, node):
        pass
    #@-node:option
    #@+node:option_argument
    def visit_option_argument(self, node):
        pass
    
    def depart_option_argument(self, node):
        pass
    #@-node:option_argument
    #@+node:option_group
    def visit_option_group(self, node):
        pass
    
    def depart_option_group(self, node):
        pass
    #@-node:option_group
    #@+node:option_list_item
    def visit_option_list_item(self, node):
        pass
    
    def depart_option_list_item(self, node):
        pass
    #@-node:option_list_item
    #@+node:option_string
    def visit_option_string(self, node):
        pass
    
    def depart_option_string(self, node):
        pass
    #@-node:option_string
    #@+node:problematic
    def visit_problematic(self, node):
        pass
    
    def depart_problematic(self, node):
        pass
    #@-node:problematic
    #@+node:system_message
    def visit_system_message(self, node):
        pass
    
    def depart_system_message(self, node):
        pass
    #@-node:system_message
    #@+node:visit_row
    def visit_row(self, node):
        pass
    
    def depart_row(self, node):
        pass
    #@-node:visit_row
    #@-node:  do nothings...
    #@+node:  special handlers...
    #@+node:comment
    def visit_comment(self, node):
    
        raise docutils.nodes.SkipNode
    #@-node:comment
    #@+node:invisible_visit
    def invisible_visit(self, node):
        
        """Invisible nodes should be ignored."""
        pass
    #@nonl
    #@-node:invisible_visit
    #@+node:unimplemented_visit
    def unimplemented_visit(self, node):
        
        raise NotImplementedError(
            'visiting unimplemented node type: %s' % node.__class__.__name__)
    #@-node:unimplemented_visit
    #@+node:visit_raw
    def visit_raw(self, node):
    
        if node.has_key('format') and node['format'] == 'html':
            self.body.append(node.astext())
    
        raise docutils.nodes.SkipNode
    #@-node:visit_raw
    #@-node:  special handlers...
    #@+node: admonitions...
    def visit_admonition(self, node, name):
        pass
    
    def depart_admonition(self):
        pass
    #@+node:attention
    def visit_attention(self, node):
    
        self.visit_admonition(node, 'attention')
    
    def depart_attention(self, node):
    
        self.depart_admonition()
    #@-node:attention
    #@+node:caution
    def visit_caution(self, node):
        self.visit_admonition(node, 'caution')
    
    def depart_caution(self, node):
        self.depart_admonition()
    #@-node:caution
    #@+node:danger
    def visit_danger(self, node):
        
        self.visit_admonition(node, 'danger')
    
    def depart_danger(self, node):
    
        self.depart_admonition()
    #@-node:danger
    #@+node:error
    def visit_error(self, node):
        self.visit_admonition(node, 'error')
    
    def depart_error(self, node):
        self.depart_admonition()
    #@nonl
    #@-node:error
    #@+node:hint
    def visit_hint(self, node):
        self.visit_admonition(node, 'hint')
    
    def depart_hint(self, node):
        self.depart_admonition()
    #@-node:hint
    #@+node:important
    def visit_important(self, node):
        self.visit_admonition(node, 'important')
    
    def depart_important(self, node):
        self.depart_admonition()
    #@-node:important
    #@+node:note
    def visit_note(self, node):
        
        self.visit_admonition(node, 'note')
    
    def depart_note(self, node):
    
        self.depart_admonition()
    #@-node:note
    #@-node: admonitions...
    #@+node: docinfos...
    #@+node:address
    def visit_address(self, node):
        self.visit_docinfo_item(node, 'address')
    
    def depart_address(self, node):
        self.depart_docinfo_item()
    #@-node:address
    #@+node:author
    def visit_author(self, node):
        self.visit_docinfo_item(node, 'author')
    
    def depart_author(self, node):
        self.depart_docinfo_item()
    #@-node:author
    #@+node:contact
    def visit_contact(self, node):
        
        self.visit_docinfo_item(node, 'contact')
    
    def depart_contact(self, node):
    
        self.depart_docinfo_item()
    #@-node:contact
    #@+node:copyright
    def visit_copyright(self, node):
        
        self.visit_docinfo_item(node, 'copyright')
    
    def depart_copyright(self, node):
    
        self.depart_docinfo_item()
    #@-node:copyright
    #@+node:date
    def visit_date(self, node):
        
        self.visit_docinfo_item(node, 'date')
    
    def depart_date(self, node):
        
        self.depart_docinfo_item()
    
    #@-node:date
    #@+node:docinfo
    def visit_docinfo(self, node):
        
        self.push(g.Bunch(kind='docinfo',start=len(self.body)))
        self.in_docinfo = True
    
    def depart_docinfo(self, node):
        
        b = self.pop('docinfo')
        self.putHead(b.start)
        self.in_docinfo = False
    #@nonl
    #@-node:docinfo
    #@+node:docinfo_item
    def visit_docinfo_item(self, node, name):
        
        self.body.append(
            '<para style="DocInfo"><b>%s: </b>' % (
                self.language.labels[name]))
    
    def depart_docinfo_item(self):
        
        self.body.append('</para>')
    #@-node:docinfo_item
    #@+node:organization
    def visit_organization(self, node):
        
        self.visit_docinfo_item(node, 'organization')
    
    def depart_organization(self, node):
    
        self.depart_docinfo_item()
    #@-node:organization
    #@+node:revision
    def visit_revision(self, node):
    
        self.visit_docinfo_item(node, 'revision')
    
    def depart_revision(self, node):
    
        self.depart_docinfo_item()
    #@-node:revision
    #@+node:status
    def visit_status(self, node):
        
        self.visit_docinfo_item(node, 'status')
    
    def depart_status(self, node):
    
        self.depart_docinfo_item()
    #@-node:status
    #@+node:version
    def visit_version(self, node):
        self.visit_docinfo_item(node, 'version')
    
    def depart_version(self, node):
        self.depart_docinfo_item()
    #@-node:version
    #@-node: docinfos...
    #@+node: Incomplete
    #@+node:definition
    def visit_definition(self, node):
    
        self.body.append('</dt>')
        self.context.append('dd')
        self.body.append(self.starttag(node, 'dd'))
    
    def depart_definition(self, node):
        self.context.pop()
        self.body.append('</dd>')
    #@-node:definition
    #@+node:footnotes (complex)
    #@+node:footnote
    def visit_footnote(self, node):
        
        self.context.append('footnotes')
        self.footnote_backrefs(node)
    
    def depart_footnote(self, node):
        
        self.context.pop()
        self.footnote_backrefs_depart(node)
    
    #@-node:footnote
    #@+node:footnote_backrefs  (Leaves unusual stuff on context)
    #@+node:footnote_backrefs
    def footnote_backrefs (self,node):
    
        if self.settings.footnote_backlinks and node.hasattr('backrefs'):
            backrefs = node ['backrefs']
            if len(backrefs) == 1:
                self.context.append("%s%s" % (
                    self.starttag({},'setLink','',destination=node['id']),
                    '</setLink>'))
                self.context.append("%s%s" % (
                    self.starttag({},'link','',destination=backrefs[0]),
                    '</link>'))
            else:
                i = 1
                backlinks = []
                for backref in backrefs:
                    backlinks.append("%s%s%s" % (
                        self.starttag({},'link','',destination=backref),
                        i, '</link>'))
                    i += 1
                self.context.append(' <i>(%s)</i> ' % ', '.join(backlinks))
                self.context.append("%s%s" % (
                    self.starttag({},'setLink','',destination=node['id']),
                    '</setLink>'))
        else:
            self.context.append("%s%s" % (
                self.starttag({},'setLink','',destination=node['id']),
                '</setLink>'))
            self.context.append('')
    #@-node:footnote_backrefs
    #@+node:footnote_backrefs_depart
    def footnote_backrefs_depart(self, node):
    
        if not self.context and self.body:
            self.createParagraph(self.body)
            self.body = []
    #@-node:footnote_backrefs_depart
    #@-node:footnote_backrefs  (Leaves unusual stuff on context)
    #@+node:footnode_reference
    #@+node:visit_footnote_reference
    def visit_footnote_reference(self, node):
        # for backrefs
        if self.settings.footnote_backlinks and node.has_key('id'):
            self.body.append(self.starttag(node, 'setLink', '', destination=node['id']))
            self.context.append('</setLink>')
        else:
            self.context.append('')
    
        href = ''
        if node.has_key('refid'):
            href = node['refid']
        elif node.has_key('refname'):
            href = self.document.nameids[node['refname']]
        format = self.settings.footnote_references
        if format == 'brackets':
            suffix = '['
            self.context.append(']')
        elif format == 'superscript':
            suffix = '<super>'
            self.context.append('</super>')
        else: # shouldn't happen
            suffix = '???'
            self.content.append('???')
        self.body.append(self.starttag(node, 'link', suffix, destination=href))
    #@nonl
    #@-node:visit_footnote_reference
    #@+node:depart_footnote_reference
    def depart_footnote_reference(self, node):
        self.body.append(self.context.pop())
        self.body.append('</link>')
        self.body.append(self.context.pop())
    #@-node:depart_footnote_reference
    #@-node:footnode_reference
    #@-node:footnotes (complex)
    #@+node:label (non-trivial)  (extra pops: may balance footnote stuff)
    def visit_label(self, node):
        
        if self.inContext('footnotes'):
            self.body.append('[')
    
    def depart_label(self, node):
        
        if self.inContext('footnotes'):
            self.body.append(']')
            self.body.append(self.context.pop())
            self.body.append(self.context.pop())
    
        self.body.append('   ')
    #@-node:label (non-trivial)  (extra pops: may balance footnote stuff)
    #@+node:strong
    def visit_strong(self, node):
        
        self.context.append('b')
        self.body.append('<b>')
    
    def depart_strong(self, node):
        
        self.context.pop()
        self.body.append('</b>')
    
    #@-node:strong
    #@+node:subtitle
    def visit_subtitle(self, node):
        
        self.context.append(len(self.body))
        self.context.append('subtitle')
    
    def depart_subtitle(self, node):
        
        style = self.context.pop()
        start = self.context.pop()
        self.putTail(start,style)
    #@-node:subtitle
    #@+node:term (weird use of context)
    def visit_term(self, node):
        self.context.append('dt')
        self.body.append(self.starttag(node, 'dt', ''))
    
    def depart_term(self, node):
        # Closes on visit_definition
        self.context.pop()
    #@nonl
    #@-node:term (weird use of context)
    #@+node:topic
    def visit_topic(self, node):
        
        if node.hasattr('id'):
            self.context.append('</setLink>')
            self.body.append(self.starttag({}, 'setLink', '', destination=node['id']))
    
    def depart_topic(self, node):
        
        if node.hasattr('id'):
            self.body.append(self.context.pop())
    
    #@-node:topic
    #@+node:list_item
    def visit_list_item(self, node):
        
        self.context.append('li')
        self.body.append('<li>')
    
    def depart_list_item(self, node):
        
        self.context.pop()
        self.body.append('</li>')
    #@-node:list_item
    #@-node: Incomplete
    #@+node: Unusual...
    #@+node: Raise SkipNode
    #@+node: literal_blocks...
    def visit_literal_block(self, node):
        
        self.story.append(Preformatted(node.astext(),self.styleSheet['Code']))
    
        raise docutils.nodes.SkipNode
    
    def depart_literal_block(self, node):
        pass
    #@+node:doctest_block
    def visit_doctest_block(self, node):
        
        self.visit_literal_block(node)
    
    def depart_doctest_block(self, node):
        
        self.depart_literal_block(node)
    
    #@-node:doctest_block
    #@+node:line_block
    def visit_line_block(self, node):
        self.visit_literal_block(node)
    
    def depart_line_block(self, node):
        self.depart_literal_block(node)
    #@-node:line_block
    #@-node: literal_blocks...
    #@+node:target
    def visit_target (self,node):
    
        if not (
            node.has_key('refuri') or
            node.has_key('refid') or
            node.has_key('refname')
        ):
            href = ''
            if node.has_key('id'):
                href = node ['id']
            elif node.has_key('name'):
                href = node ['name']
            self.body.append("%s%s" % (
                self.starttag(node,'setLink','',destination=href),
                '</setLink>'))
        raise docutils.nodes.SkipNode
    
    def depart_target (self,node):
        pass
    #@nonl
    #@-node:target
    #@-node: Raise SkipNode
    #@+node:meta
    def visit_meta(self, node):
    
        self.head.append(
            self.starttag(node, 'meta', **node.attributes))
    
    def depart_meta(self, node):
        pass
    #@nonl
    #@-node:meta
    #@+node:section
    def visit_section(self, node):
        
        self.sectionlevel += 1
    
    def depart_section(self, node):
    
        self.sectionlevel -= 1
    #@-node:section
    #@-node: Unusual...
    #@+node:bullet_list
    def visit_bullet_list(self, node):
        
        self.push(g.Bunch(kind='ul',start=len(self.body)))
    
        self.body.append('<ul bulletText="%s">' % self.bulletText)
    
    def depart_bullet_list(self, node):
        
        b = self.pop('ul')
    
        self.body.append('</ul>')
        
        if not self.inContext('ul'):
            self.putTail(b.start)
    #@nonl
    #@-node:bullet_list
    #@+node:definition_list
    def visit_definition_list(self, node):
        
        self.push(g.Bunch(kind='dl',start=len(self.body)))
        
        self.body.append(self.starttag(node, 'dl'))
    
    def depart_definition_list(self, node):
        
        b = self.pop('dl')
    
        self.body.append('</dl>')
    
        if not self.inContext('dl'):
            self.putTail(b.start)
    #@-node:definition_list
    #@+node:emphasis
    def visit_emphasis(self, node):
        
        self.push(g.Bunch(kind='i'))
        
        self.body.append('<i>')
    
    def depart_emphasis(self, node):
        
        self.pop('i')
    
        self.body.append('</i>')
    #@-node:emphasis
    #@+node:enumerated_list
    def visit_enumerated_list(self, node):
        
        self.push(g.Bunch(kind='ol',start=len(self.body)))
    
        self.body.append('<ol>')
    
    def depart_enumerated_list(self, node):
        
        b = self.pop('ol')
    
        self.body.append('</ol>')
    
        if not self.inContext('ol'):
            self.putTail(b.start)
    #@nonl
    #@-node:enumerated_list
    #@+node:field (does not change context)
    def visit_field(self, node):
        
        self.body.append('<para>')
    
    def depart_field(self, node):
    
        self.body.append('</para>')
    #@-node:field (does not change context)
    #@+node:field_list
    def visit_field_list(self, node):
        
        self.push(g.Bunch(kind='<para>',start=len(self.body)))
    
    def depart_field_list(self, node):
        
        b = self.pop('<para>')
        
        self.body.append('</para>')
        
        self.putTail(b.start)
    #@nonl
    #@-node:field_list
    #@+node:field_name (does not change context)
    def visit_field_name(self, node):
    
        self.body.append('<b>')
    
    def depart_field_name(self, node):
    
        self.body.append(': </b>')
    #@nonl
    #@-node:field_name (does not change context)
    #@+node:literal
    def visit_literal(self, node):
        
        self.push(g.Bunch(kind='literal'))
        
    def depart_literal(self, node):
        
        self.pop('literal')
    #@nonl
    #@-node:literal
    #@+node:option_list
    def visit_option_list(self, node):
        
        self.push(g.Bunch(kind='option-list',start=len(self.body)))
    
    def depart_option_list(self, node):
        
        b = self.pop('option-list')
    
        if not self.inContext('option_list'):
            self.putTail(b.start)
            
    #@nonl
    #@-node:option_list
    #@+node:paragraph...
    def visit_paragraph(self, node):
        
        self.push (g.Bunch(kind='p',start=len(self.body)))
        
    def depart_paragraph(self, node):
        
        b = self.pop('p')
        
        if not self.context and self.body:
            self.putTail(b.start)
    #@nonl
    #@-node:paragraph...
    #@+node:reference... (complex, may be buggy)
    #@+node:visit_reference
    def visit_reference (self,node):
        
        b = g.Bunch(kind='a',markup=[])
        if node.has_key('refuri'):
            href = node ['refuri']
            self.body.append(self.starttag(node,'a','',href=href))
            b.markup.append('</a>')
        else:
            if node.has_key('id'):
                self.body.append(self.starttag({},'setLink','',destination=node['id']))
                b.markup.append('</setLink>')
            if node.has_key('refid'):
                href = node ['refid']
            elif node.has_key('refname'):
                href = self.document.nameids [node ['refname']]
            self.body.append(self.starttag(node,'link','',destination=href))
            b.markup.append('</link>')
        self.push(b)
    #@nonl
    #@-node:visit_reference
    #@+node:depart_reference
    def depart_reference(self, node):
        
        b = self.pop('a')
    
        for s in b.markup:
            self.body.append(s)
    #@nonl
    #@-node:depart_reference
    #@-node:reference... (complex, may be buggy)
    #@+node:Text...
    def visit_Text (self,node):
    
        self.push(g.bunch(kind='#text'))
    
        self.body.append(node.astext())
    
        # g.trace('body',repr(self.body))
    
    def depart_Text (self,node):
    
        self.pop('#text')
    #@nonl
    #@-node:Text...
    #@+node:title
    #@+node:visit_title
    def visit_title (self,node):
    
        atts = {}
        isTopic = isinstance(node.parent,docutils.nodes.topic)
        isTitle = self.sectionlevel == 0
        b = g.Bunch(kind='title',start=len(self.body),markup=[])
    
        if isTopic:   b.style = 'topic-title'
        elif isTitle: b.style = 'title'
        else:         b.style = "h%s" % self.sectionlevel
    
        if b.style != 'title':
            if node.parent.hasattr('id'):
                self.body.append(
                    self.starttag({},'setLink','',destination=node.parent['id']))
                b.markup.append('</setLink>')
            if node.hasattr('refid'):
                self.body.append(
                    self.starttag({},'link','',destination=node['refid']))
                b.markup.append('</link>')
        self.push(b)
    
        if 0:
            #@        << old code >>
            #@+node:<< old code >>
            self.context.append(len(self.body))
            self.context.append('title')
            if isinstance(node.parent,docutils.nodes.topic):
                self.context.append('')
                self.topic_class = 'topic-title'
            elif self.sectionlevel == 0:
                self.context.append('title')
            else:
                self.context.append("h%s" % self.sectionlevel)
            
            if self.context [ -1] != 'title':
                if node.parent.hasattr('id'):
                    self.context.append('</setLink>')
                    self.body.append(self.starttag({},'setLink','',destination=node.parent['id']))
                if node.hasattr('refid'):
                    self.context.append('</link>')
                    self.body.append(self.starttag({},'link','',destination=node['refid']))
            else:
                self.context.append('')
            #@nonl
            #@-node:<< old code >>
            #@nl
    #@nonl
    #@-node:visit_title
    #@+node:depart_title
    def depart_title (self,node):
    
        b = self.pop('title')
        for z in b.markup:
            self.body.append(z)
            
        self.putTail(b.start,style=b.style)
    
        if 0:
            #@        << old code >>
            #@+node:<< old code >>
            if node.hasattr('refid'):
                self.body.append(self.context.pop())
            
            if node.parent.hasattr('id'):
                self.body.append(self.context.pop())
            
            style = self.context.pop()
            self.context.pop()
            
            if isinstance(node.parent, docutils.nodes.topic):
                style = self.topic_class
            start = self.context.pop()
            
            self.createParagraph(self.body[start:], style)
            self.body = self.body[:start]
            #@nonl
            #@-node:<< old code >>
            #@nl
    #@nonl
    #@-node:depart_title
    #@-node:title
    #@-node:Node handlers...
    #@-others

    depart_comment = invisible_visit
    visit_substitution_definition = visit_comment
    depart_substitution_definition = depart_comment
    visit_figure = visit_comment
    depart_figure = depart_comment

    visit_sidebar = invisible_visit
    visit_warning = invisible_visit
    visit_tip = invisible_visit
    visit_tbody = invisible_visit
    visit_thead = invisible_visit
    visit_tgroup = invisible_visit
    visit_table = invisible_visit
    visit_title_reference = invisible_visit
    visit_transition = invisible_visit
    visit_pending = invisible_visit
    depart_pending = invisible_visit
    depart_transition = invisible_visit
    depart_title_reference = invisible_visit
    depart_table = invisible_visit
    depart_tgroup = invisible_visit
    depart_thead = invisible_visit
    depart_tbody = invisible_visit
    depart_tip = invisible_visit
    depart_warning = invisible_visit
    depart_sidebar = invisible_visit
#@nonl
#@-node:class PDFTranslator (docutils.nodes.NodeVisitor)
#@-others
#@nonl
#@-node:@file C:/Python24/Lib/site-packages/docutils/writers/leo_pdf.py
#@-leo
