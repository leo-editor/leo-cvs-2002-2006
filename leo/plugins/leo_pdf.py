#! /usr/bin/env python
#@+leo-ver=4
#@+node:@file C:/Python24/Lib/site-packages/docutils/writers/leo_pdf.py
#@@first

#@<< docstring >>
#@+node:<< docstring >>
"""
:Author: Engelbert Gruber
:Contact: goodger@users.sourceforge.net
:Revision: $Revision$
:Date: $Date$
:Copyright: This module has been placed in the public domain.

Simple pdf writer.

The output uses reportlabs module.

Some stylesheet is needed.
"""

#@-node:<< docstring >>
#@nl

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
#@<< what I did >>
#@+node:<< what I did >>
#@@nocolor
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
#         - append_para
#         - depart_title
#@-at
#@nonl
#@-node:<< what I did >>
#@nl
__docformat__ = 'reStructuredText'
#@<< imports >>
#@+node:<< imports >>
import sys
sys.path.append(r'c:\reportlab_1_20') 

import leoGlobals as g # EKR

import time
from types import ListType, TupleType, UnicodeType
from docutils import writers, nodes, languages

from stylesheet import getStyleSheet # Got this module from same place as rlpdf.py

from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import *
from reportlab.lib.pagesizes import A4
from reportlab.platypus import *
from reportlab.platypus.para import Paragraph
from reportlab.lib import colors
from reportlab.lib.units import inch

from StringIO import StringIO
#@nonl
#@-node:<< imports >>
#@nl

#@+others
#@+node:class Writer
class Writer(writers.Writer):
	
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
    
        writers.Writer.__init__(self)
        self.translator_class = PDFTranslator
        g.trace('(Writer)')
    #@-node:__init__
    #@+node:translate
    def translate(self):
        
        visitor = self.translator_class(self.document)
        self.document.walkabout(visitor)
        self.story = visitor.as_what()
        self.output = self.record()
    #@nonl
    #@-node:translate
    #@+node:record
    def record(self):
    
        from reportlab.platypus import SimpleDocTemplate
    
        out = StringIO()
        doc = SimpleDocTemplate(out, pagesize=A4)
        doc.build(self.story)
        return out.getvalue()
    #@-node:record
    #@+node:lower
    def lower(self):
    
        return 'pdf'
    #@nonl
    #@-node:lower
    #@-others
#@nonl
#@-node:class Writer
#@+node:class PDFTranslator
class PDFTranslator(nodes.NodeVisitor):

    #@	@+others
    #@+node:__init__
    def __init__(self, doctree):
        
        g.trace('PDFTranslator')
    
        self.settings = settings = doctree.settings
        self.styleSheet = getStyleSheet()
        g.trace(self.styleSheet)
        nodes.NodeVisitor.__init__(self, doctree)
        self.language = languages.get_language(doctree.settings.language_code)
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
    
    #@-node:__init__
    #@+node:as_what
    def as_what(self):
    
        return self.story
    #@-node:as_what
    #@+node:encode
    def encode(self, text):
    
        """Encode special characters in `text` & return."""
        if type(text) is UnicodeType:
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
    #@+node:append_para
    def append_para (self,text,in_style='Normal',bulletText=None):
    
        if type(text) in (ListType,TupleType):
            text = ''.join([self.encode(t) for t in text])
    
        try:
            style = self.styleSheet [in_style.strip()] ### EKR: added strip.
        except KeyError:
            g.trace('in_style not found',repr(in_style),'using "Normal"')
            style = self.styleSheet ['Normal'] ### EKR
    
        self.story.append(
            Paragraph(self.encode(text),style,
            bulletText = bulletText, context = self.styleSheet))
    #@-node:append_para
    #@+node:starttag
    def starttag (self,node,tagname,suffix='\n',**attributes):
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
        attlist = atts.items()
        attlist.sort()
        parts = [tagname]
        for name, value in attlist:
            if value is None: # boolean attribute
                parts.append(name.lower())
            elif isinstance(value,ListType):
                values = [str(v) for v in value]
                parts.append('%s="%s"' % (name.lower(),
                                          self.encode(' '.join(values))))
            else:
                parts.append('%s="%s"' % (name.lower(),
                                          self.encode(str(value))))
        return '<%s>%s' % (' '.join(parts),suffix)
    #@nonl
    #@-node:starttag
    #@+node:visit_Text
    def visit_Text(self, node):
        self.context.append('#text')
        self.body.append(node.astext())
    #@-node:visit_Text
    #@+node:depart_Text
    def depart_Text(self, node):
        self.context.pop()
    #@-node:depart_Text
    #@+node:visit_admonition
    def visit_admonition(self, node, name):
        pass
    #@-node:visit_admonition
    #@+node:depart_admonition
    def depart_admonition(self):
        pass
    #@-node:depart_admonition
    #@+node:visit_attention
    def visit_attention(self, node):
        self.visit_admonition(node, 'attention')
    #@-node:visit_attention
    #@+node:depart_attention
    def depart_attention(self, node):
        self.depart_admonition()
    #@-node:depart_attention
    #@+node:visit_author
    def visit_author(self, node):
        self.visit_docinfo_item(node, 'author')
    #@-node:visit_author
    #@+node:depart_author
    def depart_author(self, node):
        self.depart_docinfo_item()
    #@-node:depart_author
    #@+node:visit_address
    def visit_address(self, node):
        self.visit_docinfo_item(node, 'address')
    #@-node:visit_address
    #@+node:depart_address
    def depart_address(self, node):
        self.depart_docinfo_item()
    #@-node:depart_address
    #@+node:visit_version
    def visit_version(self, node):
        self.visit_docinfo_item(node, 'version')
    #@-node:visit_version
    #@+node:depart_version
    def depart_version(self, node):
        self.depart_docinfo_item()
    #@-node:depart_version
    #@+node:visit_system_message
    def visit_system_message(self, node):
        pass
    #@-node:visit_system_message
    #@+node:depart_system_message
    def depart_system_message(self, node):
        pass
    #@-node:depart_system_message
    #@+node:visit_term
    def visit_term(self, node):
        self.context.append('dt')
        self.body.append(self.starttag(node, 'dt', ''))
    #@-node:visit_term
    #@+node:depart_term
    def depart_term(self, node):
        # Closes on visit_definition
        self.context.pop()
    #@-node:depart_term
    #@+node:visit_authors
    def visit_authors(self, node):
        pass
    #@-node:visit_authors
    #@+node:depart_authors
    def depart_authors(self, node):
        pass
    #@-node:depart_authors
    #@+node:visit_block_quote
    def visit_block_quote(self, node):
        pass
    #@-node:visit_block_quote
    #@+node:depart_block_quote
    def depart_block_quote(self, node):
        pass
    #@-node:depart_block_quote
    #@+node:visit_bullet_list
    def visit_bullet_list(self, node):
        self.context.append(len(self.body))
        self.context.append('ul')
        self.body.append('<ul bulletText="%s">' % self.bulletText)
    #@-node:visit_bullet_list
    #@+node:depart_bullet_list
    def depart_bullet_list(self, node):
        self.context.pop()
        self.body.append('</ul>')
        start = self.context.pop()
        if not 'ul' in self.context:
            self.append_para(self.body[start:])
            self.body = self.body[:start]
    #@-node:depart_bullet_list
    #@+node:visit_caption
    def visit_caption(self, node):
        pass
    #@-node:visit_caption
    #@+node:depart_caption
    def depart_caption(self, node):
        pass
    #@-node:depart_caption
    #@+node:visit_caution
    def visit_caution(self, node):
        self.visit_admonition(node, 'caution')
    #@-node:visit_caution
    #@+node:depart_caution
    def depart_caution(self, node):
        self.depart_admonition()
    #@-node:depart_caution
    #@+node:visit_citation
    def visit_citation(self, node):
        pass
    #@-node:visit_citation
    #@+node:depart_citation
    def depart_citation(self, node):
        pass
    #@-node:depart_citation
    #@+node:visit_citation_reference
    def visit_citation_reference(self, node):
        pass
    #@-node:visit_citation_reference
    #@+node:depart_citation_reference
    def depart_citation_reference(self, node):
        pass
    #@-node:depart_citation_reference
    #@+node:visit_classifier
    def visit_classifier(self, node):
        pass
    #@-node:visit_classifier
    #@+node:depart_classifier
    def depart_classifier(self, node):
        pass
    #@-node:depart_classifier
    #@+node:visit_colspec
    def visit_colspec(self, node):
        pass
    #@-node:visit_colspec
    #@+node:depart_colspec
    def depart_colspec(self, node):
        pass
    #@-node:depart_colspec
    #@+node:visit_contact
    def visit_contact(self, node):
        self.visit_docinfo_item(node, 'contact')
    #@-node:visit_contact
    #@+node:depart_contact
    def depart_contact(self, node):
        self.depart_docinfo_item()
    #@-node:depart_contact
    #@+node:visit_copyright
    def visit_copyright(self, node):
        self.visit_docinfo_item(node, 'copyright')
    #@-node:visit_copyright
    #@+node:depart_copyright
    def depart_copyright(self, node):
        self.depart_docinfo_item()
    #@-node:depart_copyright
    #@+node:visit_danger
    def visit_danger(self, node):
        self.visit_admonition(node, 'danger')
    #@-node:visit_danger
    #@+node:depart_danger
    def depart_danger(self, node):
        self.depart_admonition()
    #@-node:depart_danger
    #@+node:visit_date
    def visit_date(self, node):
        self.visit_docinfo_item(node, 'date')
    #@-node:visit_date
    #@+node:depart_date
    def depart_date(self, node):
        self.depart_docinfo_item()
    #@-node:depart_date
    #@+node:visit_definition
    def visit_definition(self, node):
    
        self.body.append('</dt>')
        self.context.append('dd')
        self.body.append(self.starttag(node, 'dd'))
    #@-node:visit_definition
    #@+node:depart_definition
    def depart_definition(self, node):
        self.context.pop()
        self.body.append('</dd>')
    #@-node:depart_definition
    #@+node:visit_definition_list
    def visit_definition_list(self, node):
        self.context.append(len(self.body))
        self.context.append('dl')
        self.body.append(self.starttag(node, 'dl'))
    #@-node:visit_definition_list
    #@+node:depart_definition_list
    def depart_definition_list(self, node):
        self.context.pop()
        self.body.append('</dl>')
        start = self.context.pop()
        if not 'dl' in self.context:
            self.append_para(self.body[start:])
            self.body = self.body[:start]
    #@-node:depart_definition_list
    #@+node:visit_definition_list_item
    def visit_definition_list_item(self, node):
        pass
    #@-node:visit_definition_list_item
    #@+node:depart_definition_list_item
    def depart_definition_list_item(self, node):
        pass
    #@-node:depart_definition_list_item
    #@+node:visit_description
    def visit_description(self, node):
        pass
    #@-node:visit_description
    #@+node:depart_description
    def depart_description(self, node):
        pass
    #@-node:depart_description
    #@+node:visit_docinfo
    def visit_docinfo(self, node):
        self.context.append(len(self.body))
        self.in_docinfo = 1
    #@-node:visit_docinfo
    #@+node:depart_docinfo
    def depart_docinfo(self, node):
        start = self.context.pop()
        docinfo = self.body[start:]
        self.body = self.body[:start]
        self.append_para(docinfo)
        self.in_docinfo = None
    #@-node:depart_docinfo
    #@+node:visit_docinfo_item
    def visit_docinfo_item(self, node, name):
        
        self.body.append('<para style="DocInfo"><b>%s: </b>' % self.language.labels[name])
    
    #@-node:visit_docinfo_item
    #@+node:depart_docinfo_item
    def depart_docinfo_item(self):
        self.body.append('</para>')
    #@-node:depart_docinfo_item
    #@+node:visit_doctest_block
    def visit_doctest_block(self, node):
        self.visit_literal_block(node)
    #@-node:visit_doctest_block
    #@+node:depart_doctest_block
    def depart_doctest_block(self, node):
        self.depart_literal_block(node)
    #@-node:depart_doctest_block
    #@+node:visit_line_block
    def visit_line_block(self, node):
        self.visit_literal_block(node)
    #@-node:visit_line_block
    #@+node:depart_line_block
    def depart_line_block(self, node):
        self.depart_literal_block(node)
    #@-node:depart_line_block
    #@+node:visit_document
    def visit_document(self, node):
        pass
    #@-node:visit_document
    #@+node:depart_document
    def depart_document(self, node):
        pass
    #@-node:depart_document
    #@+node:visit_emphasis
    def visit_emphasis(self, node):
        self.context.append('i')
        self.body.append('<i>')
    #@-node:visit_emphasis
    #@+node:depart_emphasis
    def depart_emphasis(self, node):
        self.context.pop()
        self.body.append('</i>')
    #@-node:depart_emphasis
    #@+node:visit_entry
    def visit_entry(self, node):
        pass
    #@-node:visit_entry
    #@+node:depart_entry
    def depart_entry(self, node):
        pass
    #@-node:depart_entry
    #@+node:visit_enumerated_list
    def visit_enumerated_list(self, node):
        self.context.append(len(self.body))
        self.context.append('ol')
        self.body.append('<ol>')
    #@-node:visit_enumerated_list
    #@+node:depart_enumerated_list
    def depart_enumerated_list(self, node):
        self.context.pop()
        self.body.append('</ol>')
        start = self.context.pop()
        if not 'ol' in self.context:
            self.append_para(self.body[start:])
            self.body = self.body[:start]
    #@-node:depart_enumerated_list
    #@+node:visit_error
    def visit_error(self, node):
        self.visit_admonition(node, 'error')
    #@-node:visit_error
    #@+node:depart_error
    def depart_error(self, node):
        self.depart_admonition()
    #@-node:depart_error
    #@+node:visit_field
    def visit_field(self, node):
        self.body.append('<para>')
    #@-node:visit_field
    #@+node:depart_field
    def depart_field(self, node):
        self.body.append('</para>')
    #@-node:depart_field
    #@+node:visit_field_argument
    def visit_field_argument(self, node):
        pass
    #@-node:visit_field_argument
    #@+node:depart_field_argument
    def depart_field_argument(self, node):
        pass
    #@-node:depart_field_argument
    #@+node:visit_field_list
    def visit_field_list(self, node):
        self.context.append(len(self.body))
        self.body.append('<para>')
    #@-node:visit_field_list
    #@+node:depart_field_list
    def depart_field_list(self, node):
        start = self.context.pop()
        self.body.append('</para>')
        self.append_para(self.body[start:])
        self.body = self.body[:start]
    #@-node:depart_field_list
    #@+node:visit_field_name
    def visit_field_name(self, node):
        self.body.append('<b>')
    #@-node:visit_field_name
    #@+node:depart_field_name
    def depart_field_name(self, node):
        self.body.append(': </b>')
    #@-node:depart_field_name
    #@+node:visit_field_body
    def visit_field_body(self, node):
        pass
    #@-node:visit_field_body
    #@+node:depart_field_body
    def depart_field_body(self, node):
        pass
    #@-node:depart_field_body
    #@+node:visit_footnote
    def visit_footnote(self, node):
        
        self.context.append('footnotes')
        self.footnote_backrefs(node)
    
    #@-node:visit_footnote
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
            self.append_para(self.body)
            self.body = []
    #@-node:footnote_backrefs_depart
    #@+node:depart_footnote
    def depart_footnote(self, node):
        self.context.pop()
        self.footnote_backrefs_depart(node)
    #@-node:depart_footnote
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
    #@+node:visit_hint
    def visit_hint(self, node):
        self.visit_admonition(node, 'hint')
    #@-node:visit_hint
    #@+node:depart_hint
    def depart_hint(self, node):
        self.depart_admonition()
    #@-node:depart_hint
    #@+node:visit_image
    def visit_image(self, node):
        pass
    #@-node:visit_image
    #@+node:depart_image
    def depart_image(self, node):
        pass
    #@-node:depart_image
    #@+node:visit_important
    def visit_important(self, node):
        self.visit_admonition(node, 'important')
    #@-node:visit_important
    #@+node:depart_important
    def depart_important(self, node):
        self.depart_admonition()
    #@-node:depart_important
    #@+node:visit_interpreted
    def visit_interpreted(self, node):
        pass
    #@-node:visit_interpreted
    #@+node:depart_interpreted
    def depart_interpreted(self, node):
        pass
    #@-node:depart_interpreted
    #@+node:visit_label
    def visit_label(self, node):
        if 'footnotes' in self.context:
            self.body.append('[')
    #@-node:visit_label
    #@+node:depart_label
    def depart_label(self, node):
        if 'footnotes' in self.context:
            self.body.append(']')
            self.body.append(self.context.pop())
            self.body.append(self.context.pop())
        self.body.append('   ')
    #@-node:depart_label
    #@+node:visit_legend
    def visit_legend(self, node):
        pass
    #@-node:visit_legend
    #@+node:depart_legend
    def depart_legend(self, node):
        pass
    #@-node:depart_legend
    #@+node:visit_list_item
    def visit_list_item(self, node):
        self.context.append('li')
        self.body.append('<li>')
    #@-node:visit_list_item
    #@+node:depart_list_item
    def depart_list_item(self, node):
        self.context.pop()
        self.body.append('</li>')
    #@-node:depart_list_item
    #@+node:visit_literal
    def visit_literal(self, node):
        self.context.append('literal')
    #@-node:visit_literal
    #@+node:depart_literal
    def depart_literal(self, node):
        self.context.pop()
    #@-node:depart_literal
    #@+node:visit_literal_block
    def visit_literal_block(self, node):
        self.story.append(Preformatted(node.astext(), self.styleSheet['Code']))
        raise nodes.SkipNode
    #@-node:visit_literal_block
    #@+node:depart_literal_block
    def depart_literal_block(self, node):
        pass
    #@-node:depart_literal_block
    #@+node:visit_meta
    def visit_meta(self, node):
        self.head.append(self.starttag(node, 'meta', **node.attributes))
    #@-node:visit_meta
    #@+node:depart_meta
    def depart_meta(self, node):
        pass
    #@-node:depart_meta
    #@+node:visit_note
    def visit_note(self, node):
        self.visit_admonition(node, 'note')
    #@-node:visit_note
    #@+node:depart_note
    def depart_note(self, node):
        self.depart_admonition()
    #@-node:depart_note
    #@+node:visit_option
    def visit_option(self, node):
        pass
    #@-node:visit_option
    #@+node:depart_option
    def depart_option(self, node):
        pass
    #@-node:depart_option
    #@+node:visit_option_argument
    def visit_option_argument(self, node):
        pass
    #@-node:visit_option_argument
    #@+node:depart_option_argument
    def depart_option_argument(self, node):
        pass
    #@-node:depart_option_argument
    #@+node:visit_option_group
    def visit_option_group(self, node):
        pass
    #@-node:visit_option_group
    #@+node:depart_option_group
    def depart_option_group(self, node):
        pass
    #@-node:depart_option_group
    #@+node:visit_option_list
    def visit_option_list(self, node):
        self.context.append(len(self.body))
        self.context.append('option_list')
    #@-node:visit_option_list
    #@+node:depart_option_list
    def depart_option_list(self, node):
        self.context.pop()
        start = self.context.pop()
        if not 'option_list' in self.context:
            self.append_para(self.body[start:])
            self.body = self.body[:start]
    #@-node:depart_option_list
    #@+node:visit_option_list_item
    def visit_option_list_item(self, node):
        pass
    #@-node:visit_option_list_item
    #@+node:depart_option_list_item
    def depart_option_list_item(self, node):
        pass
    #@-node:depart_option_list_item
    #@+node:visit_option_string
    def visit_option_string(self, node):
        pass
    #@-node:visit_option_string
    #@+node:depart_option_string
    def depart_option_string(self, node):
        pass
    #@-node:depart_option_string
    #@+node:visit_organization
    def visit_organization(self, node):
        self.visit_docinfo_item(node, 'organization')
    #@-node:visit_organization
    #@+node:depart_organization
    def depart_organization(self, node):
        self.depart_docinfo_item()
    #@-node:depart_organization
    #@+node:visit_paragraph
    def visit_paragraph(self, node):
        self.context.append(len(self.body))
        self.context.append('p')
    #@-node:visit_paragraph
    #@+node:depart_paragraph
    def depart_paragraph(self, node):
        self.context.pop()
        start = self.context.pop()
        if not self.context and self.body:
            self.append_para(self.body[start:])
            self.body = self.body[:start]
    #@-node:depart_paragraph
    #@+node:visit_problematic
    def visit_problematic(self, node):
        pass
    #@-node:visit_problematic
    #@+node:depart_problematic
    def depart_problematic(self, node):
        pass
    #@-node:depart_problematic
    #@+node:visit_raw
    def visit_raw(self, node):
        if node.has_key('format') and node['format'] == 'html':
            self.body.append(node.astext())
        raise nodes.SkipNode
    #@-node:visit_raw
    #@+node:visit_target
    def visit_target(self, node):
    
        if not (node.has_key('refuri') or node.has_key('refid')
                or node.has_key('refname')):
            href = ''
            if node.has_key('id'):
                href = node['id']
            elif node.has_key('name'):
                href = node['name']
            self.body.append("%s%s" % (self.starttag(node, 'setLink', '', destination=href), \
                             '</setLink>'))
        raise nodes.SkipNode
    #@-node:visit_target
    #@+node:depart_target
    def depart_target(self, node):
        pass
    #@-node:depart_target
    #@+node:visit_reference
    def visit_reference (self,node):
    
        self.context.append('a')
    
        if node.has_key('refuri'):
            href = node ['refuri']
            self.body.append(self.starttag(node,'a','',href=href))
            self.context.append('</a>')
        else:
            if node.has_key('id'):
                self.body.append(self.starttag({},'setLink','',destination=node['id']))
                self.context.append('</setLink>')
            if node.has_key('refid'):
                href = node ['refid']
            elif node.has_key('refname'):
                href = self.document.nameids [node ['refname']]
            self.body.append(self.starttag(node,'link','',destination=href))
            self.context.append('</link>')
    #@-node:visit_reference
    #@+node:depart_reference
    def depart_reference(self, node):
        if node.has_key('id') and \
           not node.has_key('refuri'):
            self.body.append(self.context.pop())
        self.body.append(self.context.pop())
        self.context.pop()
    #@-node:depart_reference
    #@+node:visit_revision
    def visit_revision(self, node):
        self.visit_docinfo_item(node, 'revision')
    #@-node:visit_revision
    #@+node:depart_revision
    def depart_revision(self, node):
        self.depart_docinfo_item()
    #@-node:depart_revision
    #@+node:visit_row
    def visit_row(self, node):
        pass
    #@-node:visit_row
    #@+node:depart_row
    def depart_row(self, node):
        pass
    #@-node:depart_row
    #@+node:visit_section
    def visit_section(self, node):
        self.sectionlevel += 1
    #@-node:visit_section
    #@+node:depart_section
    def depart_section(self, node):
        self.sectionlevel -= 1
    #@-node:depart_section
    #@+node:visit_status
    def visit_status(self, node):
        self.visit_docinfo_item(node, 'status')
    #@-node:visit_status
    #@+node:depart_status
    def depart_status(self, node):
        self.depart_docinfo_item()
    #@-node:depart_status
    #@+node:visit_strong
    def visit_strong(self, node):
        self.context.append('b')
        self.body.append('<b>')
    #@-node:visit_strong
    #@+node:depart_strong
    def depart_strong(self, node):
        self.context.pop()
        self.body.append('</b>')
    #@-node:depart_strong
    #@+node:visit_subtitle
    def visit_subtitle(self, node):
        self.context.append(len(self.body))
        self.context.append('subtitle')
    #@-node:visit_subtitle
    #@+node:depart_subtitle
    def depart_subtitle(self, node):
        style = self.context.pop()
        start = self.context.pop()
        self.append_para(self.body[start:], style)
        self.body = self.body[:start]
    #@-node:depart_subtitle
    #@+node:visit_title
    def visit_title (self,node):
        atts = {}
        self.context.append(len(self.body))
        self.context.append('title')
        if isinstance(node.parent,nodes.topic):
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
    #@-node:visit_title
    #@+node:depart_title
    def depart_title(self, node):
    
        # g.trace(repr(node))
        if node.hasattr('refid'):
            self.body.append(self.context.pop())
        if node.parent.hasattr('id'):
            self.body.append(self.context.pop())
        style = self.context.pop()
        self.context.pop()
        if isinstance(node.parent, nodes.topic):
            style = self.topic_class
        start = self.context.pop()
        
        #g.trace('body',repr(self.body))
        g.trace('start',repr(start))
        try:
            self.append_para(self.body[start:], style)
        except:
            start = len(start) ### EKR
            self.append_para(self.body[start:], style)
        
        self.body = self.body[:start]
    #@nonl
    #@-node:depart_title
    #@+node:unimplemented_visit
    def unimplemented_visit(self, node):
        
        raise NotImplementedError(
            'visiting unimplemented node type: %s' % node.__class__.__name__)
    #@-node:unimplemented_visit
    #@+node:visit_topic
    def visit_topic(self, node):
        if node.hasattr('id'):
            self.context.append('</setLink>')
            self.body.append(self.starttag({}, 'setLink', '', destination=node['id']))
    #@-node:visit_topic
    #@+node:depart_topic
    def depart_topic(self, node):
        if node.hasattr('id'):
            self.body.append(self.context.pop())
    #@-node:depart_topic
    #@+node:visit_generated
    def visit_generated(self, node):
        pass
    #@-node:visit_generated
    #@+node:depart_generated
    def depart_generated(self, node):
        pass
    #@-node:depart_generated
    #@+node:invisible_visit
    def invisible_visit(self, node):
        """Invisible nodes should be ignored."""
        pass
    #@-node:invisible_visit
    #@+node:visit_comment
    def visit_comment(self, node):
        raise nodes.SkipNode
    #@-node:visit_comment
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
#@-node:class PDFTranslator
#@-others
#@nonl
#@-node:@file C:/Python24/Lib/site-packages/docutils/writers/leo_pdf.py
#@-leo
