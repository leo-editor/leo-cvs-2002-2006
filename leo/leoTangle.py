#@+leo
#@+node:0::@file leoTangle.py
#@+body
#@@language python

# Tangle and Untangle.

from leoGlobals import *
from leoUtils import *
import os,string,traceback


#@<< about Tangle and Untangle >>
#@+node:1::<< about Tangle and Untangle >>
#@+body
#@+at
#  The Tangle command translates the selected @root tree into one or more 
# well-formatted C source files. The outline should contain directives, 
# sections references and section definitions, as described in Chapter 4. The 
# Untangle command is essentially the reverse of the Tangle command. The 
# Tangle command creates a derived file from an @root tree; the Untangle 
# command incorporates changes made to derived files back into the @root tree.
# 
# The Tangle command operates in two passes. The first pass discovers the 
# complete definitions of all sections and places these definitions in a 
# symbol table. The first pass also makes a list of root sections. Definitions 
# can appear in any order, so we must scan the entire input file to know 
# whether any particular definition has been completed.
# 
# Tangle's second pass creates one file for each @root node. Tangle rescans 
# each section in the list of roots, copying the root text to the output and 
# replacing each section reference by the section's definition. This is a 
# recursive process because any definition may contain other references. We 
# can not allow a section to be defined in terms of itself, either directly or 
# indirectly. We check for such illegally recursive definitions in pass 2 
# using the section stack class.  Tangle indicates where sections begin and 
# end using comment lines called sentinel lines.  The this part of the 
# appendix discusses the format of the sentinels output by the Tangle command.
# 
# The key design principle of the Tangle command is this: Tangle must output 
# newlines in a context-free manner. That is, Tangle must never output 
# conditional newlines, either directly or indirectly. Without this rule 
# Untangle could not determine whether to skip or copy newlines.
# 
# The Tangle command increases the indentation level of a section expansion 
# the minimum necessary to align the section expansion with the surrounding 
# code. In essence, this scheme aligns all section expansions with the line of 
# code in which the reference to the section occurs. In some cases, several 
# nested sections expansions will have the same indentation level. This can 
# occur, for example, when a section reference in an outline occurs at the 
# left margin of the outline.
# 
# This scheme is probably better than more obvious schemes that indent more 
# "consistently." Such schemes would produce too much indentation for deeply 
# nested outlines. The present scheme is clear enough and avoids indentation 
# wherever possible, yet indents sections adequately. End sentinel lines make 
# this scheme work by making clear where the expansion of one section ends and 
# the expansion of a containing section resumes.
# 
# Tangle increases indentation if the section reference does not start a line. 
# Untangle is aware of this hack and adjusts accordingly. This extra 
# indentation handles several common code idioms, which otherwise would create 
# under-indented code. In short, Tangle produces highly readable, given the 
# necessity of preserving newlines for Untangle.
# 
# Untangle is inherently complex.  It must do a perfect job of updating the 
# outline, especially whitespace, from expansions of section definitions 
# created by the Tangle command.  Such expansions need not be identical 
# because they may have been generated at different levels of indentation.  
# The Untangle command can not assume that all expansions of a section will be 
# identical in the derived file; within the derived file, the programmer may 
# have made incompatible changes to two different expansions of the same 
# section. Untangle must check to see that all expansions of a section are 
# "equivalent".  As an added complication, derived files do not contain all 
# the information found in @root trees.  @root trees may contain headlines 
# that generate no code at all.  Also, an outline may define a section in 
# several ways: with an @c or @code directive or with a section definition 
# line.  To be useful, Untangle must handle all these complications 
# flawlessly. The appendix discusses the various conventions used in the 
# sentinels output by the Tangle command.  These conventions allow the 
# Untangle command to recreate whitespace correctly.
# 
# Untangle operates in two passes. The first pass finds definitions in the 
# derived file and enters them into the Untangle Symbol Table, or UST.   
# Definitions often include references to other sections, so definitions often 
# include nested definitions of referenced sections. The first pass of 
# Untangle uses a definition stack to keep track of nested definitions. The 
# top of the stack represents the definition following the latest reference, 
# except for the very first entry pushed on the stack, which represents the 
# code in the outline that contains the @root directive. The stack never 
# becomes empty because of the entry for the @root section. All definitions of 
# a section should match--otherwise there is an inconsistent definition. This 
# pass uses a forgiving compare routine that ignores differences that do not 
# affect the meaning of a program.
# 
# Untangle's second pass enters definitions from the outline into the Tangle 
# Symbol Table, or TST. The second pass simultaneously updates all sections in 
# the outline whose definition in the TST does not match the definition in the 
# UST.  The central coding insight of the Untangle command is that the second 
# pass of Untangle is almost identical to the first pass of Tangle! That is, 
# Tangle and Untangle share key parts of code, namely the skip_body() method 
# and its allies.  Just when skip_body() enters a definition into the symbol 
# table, all the information is present that Untangle needs to update that definition.

#@-at
#@-body
#@-node:1::<< about Tangle and Untangle >>


#@<< constants & synonyms >>
#@+node:2::<< constants & synonyms >>
#@+body
# Synonyms for multiple_parts_flag.
allow_multiple_parts = 1
disallow_multiple_parts = 2
unused_parts_flag = 3

# Synonyms for root_flag to st_enter.
is_root_name = 1 ; not_root_name = 0

# Synonyms for scanAllDirectives
report_errors = 1 ; dont_report_errors = 0
require_path = 1 ; done_require_path = 0

# Synonyms for verbose_flag.
verbose = true ; brief = 0

# Constants...
max_errors = 20


#@+at
#  All these must be defined together, because they form a single 
# enumeration.  Some of these are used by utility functions.

#@-at
#@@c

if 1: # A single enum...

	# Used by token_type().
	plain_line = 1 # all other lines
	at_at	     = 2 # double-at sign.
	at_chapter = 3 # @chapter
	# at_c       = 4 # @c in noweb mode
	at_code	   = 5 # @code, or @c or @p in CWEB mode.
	at_doc	    = 6 # @doc
	at_other   = 7 # all other @directives
	at_root	   = 8 # @root or noweb * sections
	at_section = 9 # @section
	# at_space   = 10 # @space
	at_web	    = 11 # any CWEB control code, except at_at.
	
	# Returned by self.skip_section_name() and allies and used by token_type.
	bad_section_name = 12  # < < with no matching > >
	section_ref	 = 13  # < < name > >
	section_def	 = 14  # < < name > > =
	
	# Returned by is_sentinal_line.
	non_sentinel_line   = 15
	start_sentinel_line = 16
	end_sentinel_line   = 17
	
	# Stephen P. Schaefer 9/13/2002
	# add support for @first
	at_last    = 18
#@-body
#@-node:2::<< constants & synonyms >>



#@+others
#@+node:3::node classes
#@+node:1::class tst_node
#@+body
class tst_node:

	#@+others
	#@+node:1::tst_node.__init__
	#@+body
	def __init__ (self,name,root_flag):
	
		# trace("tst_node.__init__" + `name`)
		self.name = name
		self.is_root = root_flag
		self.referenced = false
		self.parts = []
	#@-body
	#@-node:1::tst_node.__init__
	#@+node:2::tst_node.__repr__
	#@+body
	def __repr__ (self):
	
		return "tst_node:" + self.name
	#@-body
	#@-node:2::tst_node.__repr__
	#@-others
#@-body
#@-node:1::class tst_node
#@+node:2::class part_node
#@+body
class part_node:

	#@+others
	#@+node:1::part_node.__init__
	#@+body
	def __init__ (self,name,code,doc,is_root,is_dirty):
	
		# trace("part_node.__init__" + `name`)
		self.name = name # Section or file name.
		self.code = code # The code text.
		self.doc = doc # The doc text.
		self.is_dirty = is_dirty # true: vnode for body text is dirty.
		self.is_root = is_root # true: name is a root name.
	#@-body
	#@-node:1::part_node.__init__
	#@+node:2::part_node.__repr__
	#@+body
	def __repr__ (self):
	
		return "part_node:" + self.name
	#@-body
	#@-node:2::part_node.__repr__
	#@-others
#@-body
#@-node:2::class part_node
#@+node:3::class ust_node
#@+body
class ust_node:

	#@+others
	#@+node:1::ust_node.__init__
	#@+body
	#@+at
	#  The text has been masssaged so that 1) it contains no leading 
	# indentation and 2) all code arising from section references have been 
	# replaced by the reference line itself.  Text for all copies of the same 
	# part can differ only in non-critical white space.

	#@-at
	#@@c

	def __init__ (self,name,code,part,of,nl_flag,update_flag):
	
		# trace("ust_node.__init__", `name` +":"+ `part`)
		self.name = name # section name
		self.parts = {} # parts dict
		self.code = code # code text
		self.part = part # n in "(part n of m)" or zero.
		self.of = of  # m in "(part n of m)" or zero.
		self.nl_flag = nl_flag  # true: section starts with a newline.
		self.update_flag = update_flag # true: section corresponds to a section in the outline.
	#@-body
	#@-node:1::ust_node.__init__
	#@+node:2::ust_node.__repr__
	#@+body
	def __repr__ (self):
	
		return "ust_node:" + self.name
	#@-body
	#@-node:2::ust_node.__repr__
	#@-others
#@-body
#@-node:3::class ust_node
#@+node:4::class def_node
#@+body
class def_node:

	#@+others
	#@+node:1::def_node.__init__
	#@+body
	#@+at
	#  The text has been masssaged so that 1) it contains no leading 
	# indentation and 2) all code arising from section references have been 
	# replaced by the reference line itself.  Text for all copies of the same 
	# part can differ only in non-critical white space.

	#@-at
	#@@c

	def __init__ (self,name,indent,part,of,nl_flag,code):
	
		if 0:
			trace("def_node.__init__",
				"name:" + name + ", part:" + `part` + ", of:" + `of` + ", indent:" + `indent`)
		self.name = name
		self.indent = indent
		self.code = code
		if self.code == None: self.code = ""
		self.part = part
		self.of = of
		self.nl_flag = nl_flag
	#@-body
	#@-node:1::def_node.__init__
	#@+node:2::def_node.__repr__
	#@+body
	def __repr__ (self):
	
		return "def_node:" + self.name
	#@-body
	#@-node:2::def_node.__repr__
	#@-others
#@-body
#@-node:4::class def_node
#@+node:5::class root_attributes (Stephen P. Schaefer)
#@+body
#@+doc
#  Stephen P. Schaefer, 9/2/2002
# Collect the root node specific attributes in an
# easy-to-use container.

#@-doc
#@@code
class root_attributes:

	#@+others
	#@+node:1::root_attributes.__init__
	#@+body
	#@+at
	#  Stephen P. Schaefer, 9/2/2002
	# Keep track of the attributes of a root node

	#@-at
	#@@c

	def __init__ (self, tangle_state):
	
		if 0:
			
			try:
				if tangle_state.path: pass
			except AttributeError:
				tangle_state.path = None
				
			trace("def_root_attribute.__init__",
				"language:" + tangle_state.language +
				", single_comment_string: " + tangle_state.single_comment_string +
				", start_comment_string: " + tangle_state.start_comment_string +
				", end_comment_string: " + tangle_state.end_comment_string +
				", use_header_flag: " + choose(tangle_state.use_header_flag, "true", "false") +
				", print_bits: " + represent_print_bits(tangle_state.print_bits) +
				", path: " + choose(tangle_state.path, tangle_state.path, "") +
				", page_width: " + tangle_state.page_width +
				", tab_width: " + tangle_state.tab_width +
				# Stephen P. Schaefer 9/13/2002
				", first_lines: " + tangle_state.first_lines)
		self.language = tangle_state.language
		self.single_comment_string = tangle_state.single_comment_string
		self.start_comment_string = tangle_state.start_comment_string
		self.end_comment_string = tangle_state.end_comment_string
		self.use_header_flag = tangle_state.use_header_flag
		self.print_bits = tangle_state.print_bits
		
		# of all the state variables, this one isn't set in tangleCommands.__init__
		# peculiar
		try:
			self.path = tangle_state.path
		except AttributeError:
			self.path = None
		
		self.page_width = tangle_state.page_width
		self.tab_width = tangle_state.tab_width
		self.first_lines = tangle_state.first_lines # Stephen P. Schaefer 9/13/2002
	#@-body
	#@-node:1::root_attributes.__init__
	#@+node:2::root_attributes.__repr__
	#@+body
	def __repr__ (self):
	
		return ("root_attributes: language: " + self.language +
	        ", single_comment_string: " + self.single_comment_string +
			", start_comment_string: " +	self.start_comment_string +
			", end_comment_string: " +	self.end_comment_string +
			", use_header_flag: " + choose(tangle_state.use_header_flag, "true", "false") +
			", print_bits: " + represent_print_bits(tangle_state.print_bits) +
			", path: " + tangle_state.path +
			", page_width: " + tangle_state.page_width +
			", tab_width: " + tangle_state.tab_width +
			# Stephen P. Schaefer 9/13/2002
			", first_lines: " + self.first_lines)
	
	#@-body
	#@-node:2::root_attributes.__repr__
	#@+node:3::root_attributes.represent_print_bits
	#@+body
	def represent_print_bits(print_bits):
		return choose(print_bits == verbose_bits, "verbose_bits",
	        choose(print_bits == terse_bits, "terse_bits",
	            choose(print_bits == silent_bits, "silent_bits", "?INVALID?")))
	
	#@-body
	#@-node:3::root_attributes.represent_print_bits
	#@-others
#@-body
#@-node:5::class root_attributes (Stephen P. Schaefer)
#@-node:3::node classes
#@+node:4::class tangleCommands methods
#@+body
class tangleCommands:

	#@+others
	#@+node:1::tangle.__init__
	#@+body
	def __init__ (self,commands):
	
		self.commands = commands
		self.init_ivars()
	#@-body
	#@-node:1::tangle.__init__
	#@+node:2::tangle.init_ivars & init_directive_ivars
	#@+body
	# Called by __init__
	
	def init_ivars(self):
	
		c = self.commands
		
		#@<< init tangle ivars >>
		#@+node:1::<< init tangle ivars >>
		#@+body
		# Various flags and counts...
		
		self.errors = 0 # The number of errors seen.
		self.tangling = true # true if tangling, false if untangling.
		self.path_warning_given = false # true: suppress duplicate warnings.
		self.tangle_indent = 0 # Level of indentation during pass 2, in spaces.
		self.file_name = c.frame.mFileName # The file name (was a bridge function)
		self.v = None # vnode being processed.
		self.output_file = None # The file descriptor of the output file.
		self.tangle_default_directory = None # Default directory set by scanAllDirectives.
		

		#@+at
		#  Symbol tables: the TST (Tangle Symbol Table) contains all section 
		# names in the outline. The UST (Untangle Symbol Table) contains all 
		# sections defined in the derived file.

		#@-at
		#@@c
		self.tst = {}
		self.ust = {}
		
		# The section stack for Tangle and the definition stack for Untangle.
		self.section_stack = []
		self.def_stack = []
		

		#@+at
		#  The list of all roots. The symbol table routines add roots to self 
		# list during pass 1. Pass 2 uses self list to generate code for all roots.

		#@-at
		#@@c
		self.root_list = []
		
		# The delimiters for comments created by the @comment directive.
		self.single_comment_string = "//"  # present comment delimiters.
		self.start_comment_string = "/*"
		self.end_comment_string = "*/"
		self.sentinel = None
		
		# The filename following @root in a headline.
		# The code that checks for < < * > > = uses these globals.
		self.root = None
		self.root_name = None
		
		# Formerly the "tangle private globals"
		# These save state during tangling and untangling.
		# It is possible that these will be removed...
		if 1:
			self.head_root = None
			self.code = None
			self.doc = None
			self.header_name = None
			self.header = None
			self.section_name = None
		

		#@+at
		#  The following records whether we have seen an @code directive in a 
		# body text.
		# If so, an @code represents < < header name > > = and it is valid to 
		# continue a section definition.

		#@-at
		#@@c
		self.code_seen = false # true if @code seen in body text.
		
		#@-body
		#@-node:1::<< init tangle ivars >>

		
		#@<< init untangle ivars >>
		#@+node:2::<< init untangle ivars >>
		#@+body
		#@+at
		#  Untangle vars used while comparing.

		#@-at
		#@@c
		self.line_comment = self.comment = self.comment_end = None
		self.comment2 = self.comment2_end = None
		self.string1 = self.string2 = self.verbatim = None
		self.message = None # forgiving compare message.
		#@-body
		#@-node:2::<< init untangle ivars >>

		
	# Called by scanAllDirectives
	
	def init_directive_ivars (self):
	
		c = self.commands
		
		#@<< init directive ivars >>
		#@+node:3::<< init directive ivars >> (tangle)
		#@+body
		if 0: # not used in this version of Leo
			self.allow_rich_text = default_allow_rich_text
			self.extended_noweb_flag = default_extended_noweb_flag
			self.target_language = default_target_language # uses c.target_lanuage instead
			
		# Global options
		self.page_width = c.page_width
		self.tab_width = c.tab_width
		self.tangle_batch_flag = c.tangle_batch_flag
		self.untangle_batch_flag = c.untangle_batch_flag
		
		# Default tangle options.
		self.tangle_directory = None # Initialized by scanAllDirectives
		self.output_doc_flag = c.output_doc_flag
		self.use_header_flag = c.use_header_flag
		
		# Default tangle language
		self.language = c.target_language
		delim1,delim2,delim3 = set_delims_from_language(self.language)
		# print `delim1`,`delim2`,`delim3`
		
		# 8/1/02: this now works as expected.
		self.single_comment_string = delim1
		self.start_comment_string = delim2
		self.end_comment_string = delim3
		
		# Abbreviations for self.language
		self.use_cweb_flag = self.language == cweb_language
		self.use_noweb_flag = not self.use_cweb_flag
		
		# Set only from directives.
		self.print_bits = verbose_bits
		
		# Stephen P. Schaefer 9/13/2002
		# support @first directive
		self.first_lines = ""
		#@-body
		#@-node:3::<< init directive ivars >> (tangle)
	#@-body
	#@-node:2::tangle.init_ivars & init_directive_ivars
	#@+node:3::top level
	#@+body
	#@+at
	#  Only top-level drivers initialize ivars.

	#@-at
	#@-body
	#@+node:1::cleanup
	#@+body
	# This code is called from tangleTree and untangleTree.
	
	def cleanup (self):
		
		#trace()
		if self.errors == 0:
		
			# Create a list of root names:
			root_names = [] ; dir = app().loadDir
			for section in self.root_list:
				for part in section.parts:
					if part.is_root:
						root_names.append(os.path.join(dir,part.name))
	
			if self.tangling and self.tangle_batch_flag:
				try:
					import tangle_done
					tangle_done.run(root_names)
				except:
					es("Can not execute tangle_done.run()")
					traceback.print_exc()
			if not self.tangling and self.untangle_batch_flag:
				try:
					import untangle_done
					untangle_done.run(root_names)
				except:
					es("Can not execute tangle_done.run()")
					traceback.print_exc()
	
		# Reinitialize the symbol tables and lists.
		self.tst = {}
		self.ust = {}
		self.root_list = []
		self.def_stack = []
	#@-body
	#@-node:1::cleanup
	#@+node:2::initTangleCommand
	#@+body
	def initTangleCommand (self):
	
		c = self.commands
		c.endEditing()
		
		es("Tangling...")
		c.setIvarsFromPrefs()
		self.init_ivars()
		self.tangling = true
	#@-body
	#@-node:2::initTangleCommand
	#@+node:3::initUntangleCommand
	#@+body
	def initUntangleCommand (self):
	
		c = self.commands
		c.endEditing()
		
		es("Untangling...")
		c.setIvarsFromPrefs()
		self.init_ivars()
		self.tangling = false
	#@-body
	#@-node:3::initUntangleCommand
	#@+node:4::tangle
	#@+body
	def tangle(self):
	
		c = self.commands ; v = c.currentVnode()
		self.initTangleCommand()
		self.tangleTree(v,report_errors)
		es("Tangle complete")
	#@-body
	#@-node:4::tangle
	#@+node:5::tangleAll
	#@+body
	def tangleAll(self):
	
		c = self.commands ; v = c.rootVnode()
		self.initTangleCommand()
		has_roots = false
	
		while v:
			ok = self.tangleTree(v,dont_report_errors)
			if ok: has_roots = true
			if self.path_warning_given:
				break # Fatal error.
			v = v.next()
	
		if not has_roots:
			es("----- The outline contains no roots")
		elif self.errors > 0 and not self.path_warning_given:
			es("----- Tangle halted because of errors")
		else:
			es("Tangle complete")
	#@-body
	#@-node:5::tangleAll
	#@+node:6::tangleMarked
	#@+body
	def tangleMarked(self):
	
		c = self.commands ; v = c.rootVnode()
		c.clearAllVisited() # No roots have been tangled yet.
		self.initTangleCommand()
		any_marked = false
	
		while v:
			is_ignore, i = is_special(v.bodyString(),0,"@ignore")
			# Only tangle marked and unvisited nodes.
			if is_ignore:
				v = v.nodeAfterTree()
			elif v.isMarked():
				ok = self.tangleTree(v,dont_report_errors)
				if ok: any_marked = true
				if self.path_warning_given:
					break # Fatal error.
				v = v.nodeAfterTree()
			else: v = v.threadNext()
	
		if not any_marked:
			es("----- The outline contains no marked roots")
		elif self.errors > 0 and not self.path_warning_given:
			es("----- Tangle halted because of errors")
		else:
			es("Tangle complete")
	#@-body
	#@-node:6::tangleMarked
	#@+node:7::tanglePass1
	#@+body
	#@+at
	#  This is the main routine of pass 1. It traverses the tree whose root is 
	# given, handling each headline and associated body text.

	#@-at
	#@@c

	def tanglePass1(self,v):
	
		next = v.nodeAfterTree()
		
		while v and v != next:
			self.v = v
			self.setRootFromHeadline(v)
			bits, dict = is_special_bits(v.bodyString(),[self.head_root])
			is_ignore = (bits & ignore_bits)!= 0
			if is_ignore:
				v = v.nodeAfterTree()
				continue
			# This must be called after root_name has been set.
			if self.tangling:
				self.scanAllDirectives(v,require_path,report_errors) # calls init_directive_ivars.
			# Scan the headline and body text.
			self.skip_headline(v)
			self.skip_body(v)
			v = v.threadNext()
			if self.errors >= max_errors:
				es("----- Halting Tangle: too many errors")
				break
	
		if self.tangling:
			self.st_check()
			# trace(self.st_dump(verbose))
	#@-body
	#@-node:7::tanglePass1
	#@+node:8::tanglePass2
	#@+body
	# At this point v is the root of the tree that has been tangled.
	
	def tanglePass2(self):
	
		self.v = None # self.v is not valid in pass 2.
	
		if self.errors > 0:
			es("----- No file written because of errors")
		elif self.root_list == None:
			es("----- The outline contains no roots")
		else:
			self.put_all_roots() # pass 2 top level function.
	#@-body
	#@-node:8::tanglePass2
	#@+node:9::tangleTree (calls cleanup)
	#@+body
	#@+at
	#  This funtion tangles all nodes in the tree whose root is v. It reports 
	# on its results if report_flag is true.
	# 
	# This function is called only from the top level, so there is no need to 
	# initialize globals.

	#@-at
	#@@c

	def tangleTree(self,v,report_flag):
	
		assert(v)
		any_root_flag = false
		next = v.nodeAfterTree()
		self.path_warning_given = false
	
		while v and v != next:
			self.setRootFromHeadline(v)
			bits, dict = is_special_bits(v.bodyString(),[self.head_root])
			is_ignore = (bits & ignore_bits) != 0
			is_root = (bits & root_bits) != 0
			is_unit = (bits & unit_bits) != 0
			if is_ignore:
				v = v.nodeAfterTree()
			elif not is_root and not is_unit:
				v = v.threadNext()
			else:
				self.tanglePass1(v) # sets self.v
				if self.root_list and self.tangling:
					any_root_flag = true
					self.tanglePass2() # self.v invalid in pass 2.
				self.cleanup()
				v = v.nodeAfterTree()
				if self.path_warning_given: break # Fatal error.
	
		if self.tangling and report_flag and not any_root_flag:
			# This is done by Untangle if we are untangling.
			es("----- The outline contains no roots")
		return any_root_flag
	#@-body
	#@-node:9::tangleTree (calls cleanup)
	#@+node:10::untangle
	#@+body
	def untangle(self):
	
		c = self.commands ; v = c.currentVnode()
		self.initUntangleCommand()
		
		c.beginUpdate()
		self.untangleTree(v,report_errors)
		c.endUpdate()
		es("Untangle complete")
	#@-body
	#@-node:10::untangle
	#@+node:11::untangleAll
	#@+body
	def untangleAll(self):
	
		c = self.commands ; v = c.rootVnode()
		self.initUntangleCommand()
		has_roots = false
	
		c.beginUpdate()
		while v:
			ok = self.untangleTree(v,false)
			if ok: has_roots = true
			v = v.next()
		c.endUpdate()
		
		if not has_roots:
			es("----- The outline contains no roots")
		elif self.errors > 0:
			es("----- Untangle command halted because of errors")
		else:
			es("Untangle complete")
	#@-body
	#@-node:11::untangleAll
	#@+node:12::untangleMarked
	#@+body
	def untangleMarked(self):
	
		c = self.commands ; v = c.rootVnode()
		self.initUntangleCommand()
		marked_flag = false
	
		c.beginUpdate()
		while v:
			if v.isMarked():
				ok = self.untangleTree(v,dont_report_errors)
				if ok: marked_flag = true
				if self.errors > 0: break
				v = v.nodeAfterTree()
			else: v = v.threadNext()
		c.endUpdate()
	
		if not marked_flag:
			es("----- The outline contains no marked roots")
		elif self.errors > 0:
			es("----- Untangle command halted because of errors")
		else:
			es("Untangle complete")
	#@-body
	#@-node:12::untangleMarked
	#@+node:13::untangleRoot (calls cleanup)
	#@+body
	#@+at
	#  This method untangles the derived files in a vnode known to contain at 
	# least one @root directive. The work is done in two passes. The first 
	# pass creates the UST by scanning the derived file. The second pass 
	# updates the outline using the UST and a TST that is created during the pass.
	# 
	# We assume that all sections from root to end are contained in the 
	# derived file, and we attempt to update all such sections. The begin/end 
	# params indicate the range of nodes to be scanned when building the TST.

	#@-at
	#@@c

	def untangleRoot(self,root,begin,end):
	
		# trace("root,begin,end:" + `root` + `begin` + `end`)
		
		#@<< Set path & root_name to the file specified in the @root directive >>
		#@+node:2::<< Set path & root_name to the file specified in the @root directive >>
		#@+body
		s = root.bodyString()
		i = 0
		while i < len(s):
			code, junk = self.token_type(s,i,report_errors)
			if code == at_root:
				# token_type sets root_name unless there is a syntax error.
				if self.root_name: path = self.root_name
				break
			else: i = skip_line(s,i)
			
		if not self.root_name:
			# A bad @root command.  token_type has already given an error.
			self.cleanup()
			return
		#@-body
		#@-node:2::<< Set path & root_name to the file specified in the @root directive >>

		
		#@<< return if @silent or unknown language >>
		#@+node:1::<< return if @silent or unknown language >>
		#@+body
		if self.language == unknown_language:
			es("**Unknown language for " + path)
			return
		
		if self.print_bits == silent_bits:
			es("@silent inhibits untangle for " + path)
			return
		#@-body
		#@-node:1::<< return if @silent or unknown language >>

		
		#@<< Read the file into file_buf >>
		#@+node:3::<< Read the file into file_buf  >>
		#@+body
		f = None
		try:
			path = os.path.join(self.tangle_directory,path)
			f = open(path)
			if f:
				file_buf = f.read()
				file_buf = string.replace(file_buf,body_ignored_newline,'')
		except:
			if f: f.close()
			es("error reading: " + path)
			traceback.print_exc()
			self.cleanup()
			return
		#@-body
		#@-node:3::<< Read the file into file_buf  >>

		es("@root " + path)
		# Pass 1: Scan the C file, creating the UST
		self.scan_derived_file(file_buf)
		# trace(self.ust_dump())
		if self.errors == 0:
			
			#@<< Pass 2: Untangle the outline using the UST and a newly-created TST >>
			#@+node:4::<< Pass 2:  Untangle the outline using the UST and a newly-created TST >>
			#@+body
			#@+at
			#  This code untangles the root and all its siblings. We don't 
			# call tangleTree here because we must handle all siblings.  
			# tanglePass1 handles an entire tree.  It also handles @ignore.

			#@-at
			#@@c

			v = begin
			while v and v != end:
				self.tanglePass1(v)
				if self.errors != 0:
					break
				v = v.nodeAfterTree()
			
			self.ust_warn_about_orphans()
			#@-body
			#@-node:4::<< Pass 2:  Untangle the outline using the UST and a newly-created TST >>

		self.cleanup()
	#@-body
	#@-node:13::untangleRoot (calls cleanup)
	#@+node:14::untangleTree
	#@+body
	# This funtion is called when the user selects any "Untangle" command.
	
	def untangleTree(self,v,report_flag):
	
		# trace(`v`)
		c = self.commands
		any_root_flag = false
		afterEntireTree = v.nodeAfterTree()
		# Initialize these globals here: they can't be cleared later.
		self.head_root = None
		self.errors = 0
		c.clearAllVisited() # Used by untangle code.
	
		while v and v != afterEntireTree and self.errors == 0:
			self.setRootFromHeadline(v)
			bits, dict = is_special_bits(v.bodyString(),[self.head_root])
			ignore =(bits & ignore_bits)!= 0
			root =(bits & root_bits)!= 0
			unit =(bits & unit_bits)!= 0
			if ignore:
				v = v.nodeAfterTree()
			elif unit:
				# Expand the context to the @unit directive.
				unitNode = v   # 9/27/99
				afterUnit = v.nodeAfterTree()
				v = v.threadNext()
				while v and v != afterUnit and self.errors == 0:
					self.setRootFromHeadline(v)
					bits, dict = is_special_bits(v.bodyString(),[self.head_root])
					root =(bits & root_bits)!= 0
					if root:
						any_root_flag = true
						end = None
						
						#@<< set end to the next root in the unit >>
						#@+node:1::<< set end to the next root in the unit >>
						#@+body
						#@+at
						#  The untangle_root function will untangle an entire 
						# tree by calling untangleTree, so the following code 
						# ensures that the next @root node will not be an 
						# offspring of v.

						#@-at
						#@@c

						end = v.threadNext()
						while end and end != afterUnit:
							flag, i = is_special(end.bodyString(),0,"@root")
							if flag and not v.isAncestorOf(end):
								break
							end = end.threadNext()
						
						#@-body
						#@-node:1::<< set end to the next root in the unit >>

						# trace("end:" + `end`)
						self.scanAllDirectives(v,require_path,report_errors)
						self.untangleRoot(v,unitNode,afterUnit)
						v = end
					else: v = v.threadNext()
			elif root:
				# Limit the range of the @root to its own tree.
				afterRoot = v.nodeAfterTree()
				any_root_flag = true
				self.scanAllDirectives(v,require_path,report_errors)
				self.untangleRoot(v,v,afterRoot) # 9/27/99
				v = afterRoot
			else:
				v = v.threadNext()
		if report_flag:
			if not any_root_flag:
				es("----- The outline contains no roots")
			elif self.errors > 0:
				es("----- Untangle command halted because of errors")
		return any_root_flag
	#@-body
	#@-node:14::untangleTree
	#@-node:3::top level
	#@+node:4::tangle
	#@+node:1::Pass 1
	#@+node:1::handle_newline
	#@+body
	#@+at
	#  This method handles newline processing while skipping a code section. 
	# It sets 'done' if the line contains an @directive or section definition 
	# that terminates the present code section. On entry: i should point to 
	# the first character of a line.  This routine scans past a line only if 
	# it could not contain a section reference.
	# 
	# Returns (i, done)

	#@-at
	#@@c

	def handle_newline(self,s,i):
	
		j = i ; done = false
		kind, end = self.token_type(s,i,dont_report_errors)
		# token_type will not skip whitespace in noweb mode.
		i = skip_ws(s,i)
		# trace(`kind` + "," + `get_line(s,i)`)
	
		if kind == plain_line:
			pass
		elif (kind == at_code or kind == at_doc or
			kind == at_root or kind == section_def):
			i = j ; done = true # Terminate this code section and rescan.
		elif kind == section_ref:
			# Enter the reference.
			ref = s[i:end]
			self.st_enter_section_name(ref,None,None,unused_parts_flag)
		elif kind == at_other or kind == at_chapter or kind == at_section:
			# We expect to see only @doc,@c or @root directives
			# while scanning a code section.
			i = skip_to_end_of_line(s,i)
			self.error("directive not valid here: " + s[j:i])
		elif kind == bad_section_name:
			if self.use_cweb_flag:
				i = skip_to_end_of_line(s,i)
		elif kind == at_web or kind == at_at:
			i += 2 # Skip a CWEB control code.
		else: assert(false)
	
		return i, done
	#@-body
	#@-node:1::handle_newline
	#@+node:2::skip_body
	#@+body
	# This method handles all the body text.
	
	def skip_body (self,v):
	
		# trace(`v`)
		s = v.bodyString()
		code_seen = false ; code = None ; anyChanged = false
		i, doc = self.skip_doc(s,0) # Start in doc section by default.
		if i >= len(s) and doc:
			
			#@<< Define a section containing only an @doc part >>
			#@+node:1::The interface between tangle and untangle
			#@+node:1::<< Define a section containing only an @doc part >>
			#@+body
			#@+at
			#  It's valid for an @doc directive to appear under a headline 
			# that does not contain a section name.  In that case, no section 
			# is defined.

			#@-at
			#@@c

			if self.header_name:
			
				# Tangle code.
				flag = choose(code_seen,allow_multiple_parts,disallow_multiple_parts)
				part = self.st_enter_section_name(self.header_name,code,doc,flag)
			
				# Untangle no longer updates doc parts.
				
			doc = None
			#@-body
			#@-node:1::<< Define a section containing only an @doc part >>
			#@-node:1::The interface between tangle and untangle

		while i < len(s):
			progress = i # progress indicator
			# line = get_line(s,i) ; trace(`line`)
			kind, end = self.token_type(s,i,report_errors)
			# if is_nl(s,i): i = skip_nl(s,i)
			i = skip_ws(s,i)
			if kind == section_def:
				
				#@<< Scan and define a section definition >>
				#@+node:1::The interface between tangle and untangle
				#@+node:2::<< Scan and define a section definition >>
				#@+body
				# We enter the code part and any preceding doc part into the symbol table.
				
				# Skip the section definition line.
				k = i ; i, kind, junk = self.skip_section_name(s,i)
				section_name = s[k:i]
				# trace(`section_name`)
				assert(kind == section_def)
				i = skip_to_end_of_line(s,i)
				
				# Tangle code: enter the section name even if the code part is empty.
				j = skip_blank_lines(s,i)
				i, code = self.skip_code(s,j)
				flag = choose(kind==section_def,allow_multiple_parts,disallow_multiple_parts)
				part = self.st_enter_section_name(section_name,code,doc,flag)
						
				if not self.tangling: # Untangle code.
					head = s[:j] ; tail = s[i:]
					s,i,changed = self.update_def(section_name,part,head,code,tail,not_root_name)
					if changed: anyChanged = true
					
				code = doc = None
				#@-body
				#@-node:2::<< Scan and define a section definition >>
				#@-node:1::The interface between tangle and untangle

			elif kind == at_code:
				if self.use_cweb_flag:
					i += 2 # Skip the at-c or at-p
				else:
					i = skip_line(s,i)
				
				#@<< Scan and define an @code defininition >>
				#@+node:1::The interface between tangle and untangle
				#@+node:3::<< Scan and define an @code defininition >>
				#@+body
				# All @c or @code directives denote < < headline_name > > =
				if self.header_name:
				
					# Tangle code.
					j = skip_blank_lines(s,i)
					i, code = self.skip_code(s,j)
					flag = choose(code_seen,allow_multiple_parts,disallow_multiple_parts)
					part = self.st_enter_section_name(self.header_name,code,doc,flag)
					if not self.tangling: # Untangle code.
						head = s[:j] ; tail = s[i:]
						s,i,changed = self.update_def(self.header,part,head,code,tail,not_root_name)
						if changed: anyChanged = true
				else:
					self.error("@c expects the headline: " + self.header + " to contain a section name")
				
				code_seen = true
				code = doc = None
				#@-body
				#@-node:3::<< Scan and define an @code defininition >>
				#@-node:1::The interface between tangle and untangle

			elif kind == at_root:
				i = skip_line(s,i)
				
				#@<< Scan and define a root section >>
				#@+node:1::The interface between tangle and untangle
				#@+node:4::<< Scan and define a root section >>
				#@+body
				# We save the file name in case another @root ends the code section.
				old_root_name = self.root_name
				
				# Tangle code.
				j = skip_blank_lines(s,i)
				k, code = self.skip_code(s,j)
				
				# Stephen Schaefer, 9/2/02, later
				# st_enter_root_name relies on scanAllDirectives to have set
				# the root attributes, such as language, *_comment_string,
				# use_header_flag, etc.
				self.st_enter_root_name(old_root_name,code,doc)
				
				if not self.tangling: # Untangle code.
					part = 1 # Use 1 for root part.
					head = s[:j] ; tail = s[k:]
					s,i,changed = self.update_def(old_root_name,part,head,code,tail,is_root_name)
					if changed: anyChanged = true
					
				code = doc = None
				#@-body
				#@-node:4::<< Scan and define a root section >>
				#@-node:1::The interface between tangle and untangle

			elif kind == at_doc:
				if self.use_cweb_flag:
					i += 2 # Skip the at-space
				else:
					i = skip_line(s,i)
				i, doc = self.skip_doc(s,i)
			elif kind == at_chapter or kind == at_section:
				i = skip_line(s,i)
				i, doc = self.skip_doc(s,i)
			else:
				i = skip_line(s,i)
			assert(progress < i) # we must make progress!
		# 3/4/02: Only call v.trimTrailingLines if we have changed its body.
		if anyChanged:
			v.trimTrailingLines()
	#@-body
	#@+node:1::The interface between tangle and untangle
	#@+body
	#@+at
	#  The following subsections contain the interface between the Tangle and 
	# Untangle commands.  This interface is an important hack, and allows 
	# Untangle to avoid duplicating the logic in skip_tree and its allies.
	# 
	# The aha is this: just at the time the Tangle command enters a definition 
	# into the symbol table, all the information is present that Untangle 
	# needs to update that definition.
	# 
	# To get whitespace exactly right we retain the outline's leading 
	# whitespace and remove leading whitespace from the updated definition.

	#@-at
	#@-body
	#@-node:1::The interface between tangle and untangle
	#@-node:2::skip_body
	#@+node:3::skip_code
	#@+body
	#@+at
	#  This method skips an entire code section. The caller is responsible for 
	# entering the completed section into the symbol table. On entry, i points 
	# at the line following the @directive or section definition that starts a 
	# code section. We skip code until we see the end of the body text or the 
	# next @ directive or section defintion that starts a code or doc part.

	#@-at
	#@@c

	def skip_code(self,s,i):
	
		# trace(`get_line(s,i)`)
		code1 = i
		nl_i = i # For error messages
		done = false # true when end of code part seen.
		if self.use_noweb_flag:
			
			#@<< skip a noweb code section >>
			#@+node:1::<< skip a noweb code section >>
			#@+body
			#@+at
			#  This code handles the following escape conventions: double 
			# at-sign at the start of a line and at-<< and at.>.

			#@-at
			#@@c

			i, done = self.handle_newline(s,i)
			while not done and i < len(s):
				ch = s[i]
				if is_nl(s,i):
					nl_i = i = skip_nl(s,i)
					i, done = self.handle_newline(s,i)
				elif ch == '@' and (match(s,i+1,"<<") or # must be on different lines
					match(s,i+1,">>")):
					i += 3 # skip the noweb escape sequence.
				elif ch == '<':
					
					#@<< handle possible noweb section reference >>
					#@+node:1::<< handle possible noweb section reference >>
					#@+body
					j, kind, end = self.is_section_name(s,i)
					if kind == section_def:
						k = skip_to_end_of_line(s,i)
						# We are in the middle of a line.
						i += 1
						self.error("chunk definition not valid here\n" + s[nl_i:k])
					elif kind == bad_section_name:
						i += 1 # This is not an error.  Just skip the '<'.
					else:
						assert(kind == section_ref)
						# Enter the reference into the symbol table.
						name = s[i:end]
						self.st_enter_section_name(name,None,None,unused_parts_flag)
						i = end
					#@-body
					#@-node:1::<< handle possible noweb section reference >>

				else: i += 1
			#@-body
			#@-node:1::<< skip a noweb code section >>

		else:
			
			#@<< skip a CWEB code section >>
			#@+node:2::<< skip a CWEB code section >>
			#@+body
			# This code is simple because CWEB control codes are valid anywhere.
			
			while not done and i < len(s):
				if s[i] == '@':
					
					#@<< handle CWEB control code >>
					#@+node:1::<< handle CWEB control code >>
					#@+body
					j, kind, end = self.is_section_name(s,i)
					
					if kind == section_def:
						done = true
					elif kind == bad_section_name:
						i += 2 # Any other control code.
					else:
						assert(kind == section_ref)
						# Enter the reference into the symbol table.
						name = s[i:j]
						self.st_enter_section_name(name,None,None,unused_parts_flag)
						i = j
					#@-body
					#@-node:1::<< handle CWEB control code >>

				else: i += 1
			#@-body
			#@-node:2::<< skip a CWEB code section >>

		code = s[code1:i]
		# trace(returns: + `code`)
		return i,code
	#@-body
	#@-node:3::skip_code
	#@+node:4::skip_doc
	#@+body
	def skip_doc(self,s,i):
	
		# trace(`get_line(s,i)`)
		# Skip @space, @*, @doc, @chapter and @section directives.
		doc1 = i
		while i < len(s):
			if is_nl(s,i):
				doc1 = i = skip_nl(s,i)
			elif match(s,i,"@ ") or match(s,i,"@\t") or match(s,i,"@*"):
				i = skip_ws(s,i+2) ; doc1 = i
			elif match(s,i,"@\n"):
				i += 1 ; doc1 = i
			elif (match_word(s,i,"@doc") or
				  match_word(s,i,"@chapter") or
				  match_word(s,i,"@section")):
				doc1 = i = skip_line(s,i)
			else: break
	
		while i < len(s):
			kind, end = self.token_type(s,i,dont_report_errors)
			if kind == at_code or kind == at_root or kind == section_def:
				break
			i = skip_line(s,i)
	
		doc = s[doc1:i]
		# trace(doc)
		return i, doc
	#@-body
	#@-node:4::skip_doc
	#@+node:5::skip_headline
	#@+body
	#@+at
	#  This function sets ivars that keep track of the indentation level. We 
	# also remember where the next line starts because it is assumed to be the 
	# first line of a documentation section.
	# 
	# A headline can contain a leading section name.  If it does, we 
	# substitute the section name if we see an @c directive in the body text.

	#@-at
	#@@c

	def skip_headline(self,v):
	
		# trace(`v`)
		self.header = s = v.headString()
		# Set self.header_name.
		j = i = skip_ws(s,0)
		i, kind, end = self.is_section_name(s,i)
		if kind == bad_section_name:
			self.header_name = None
		else:
			self.header_name = s[j:end]
	#@-body
	#@-node:5::skip_headline
	#@-node:1::Pass 1
	#@+node:2::Pass 2
	#@+node:1::oblank, oblanks, os, otab, otabs (Tangle)
	#@+body
	def oblank (self):
		self.oblanks(1)
	
	def oblanks (self,n):
		if abs(n) > 0:
			self.output_file.write(' ' * abs(n))
			
	def onl(self):
		self.os('\n')
			
	def os (self,s):
		s = string.replace(s,body_ignored_newline,body_newline)
		try:
			self.output_file.write(s)
		except UnicodeError: # 8/9/02
			xml_encoding = app().config.xml_version_string
			s = s.encode(xml_encoding)
			self.output_file.write(s) # 8/14/02
	
	def otab (self):
		self.otabs(1)
	
	def otabs (self,n):
		if abs(n) > 0:
			self.output_file.write('\t' * abs(n))
	#@-body
	#@-node:1::oblank, oblanks, os, otab, otabs (Tangle)
	#@+node:2::tangle.put_all_roots
	#@+body
	#@+at
	#  This is the top level method of the second pass. It creates a separate 
	# C file for each @root directive in the outline. As will be seen 
	# later,the file is actually written only if the new version of the file 
	# is different from the old version,or if the file did not exist 
	# previously. If changed_only_flag FLAG is true only changed roots are 
	# actually written.

	#@-at
	#@@c

	def put_all_roots(self):
	
		c = self.commands ; outline_name = c.frame.mFileName
	
		for section in self.root_list:
		
			# trace(`section.name`)
			file_name = os.path.join(self.tangle_directory,section.name)
			file_name = os.path.normpath(file_name)
			temp_name = create_temp_name()
			if not temp_name:
				es("Can not create temp file")
				break
			# Set the output_file global.
			self.output_file = open(temp_name,"wb")
			if not self.output_file:
				es("Can not create: " + temp_name)
				break
			
			#@<<Get root specific attributes>>
			#@+node:1::<<Get root specific attributes>>
			#@+body
			# Stephen Schaefer, 9/2/02
			# Retrieve the full complement of state for the root node
			self.language = section.root_attributes.language
			self.single_comment_string = section.root_attributes.single_comment_string
			self.start_comment_string = section.root_attributes.start_comment_string
			self.end_comment_string = section.root_attributes.end_comment_string
			self.use_header_flag = section.root_attributes.use_header_flag
			self.print_bits = section.root_attributes.print_bits
			self.path = section.root_attributes.path
			self.page_width = section.root_attributes.page_width
			self.tab_width = section.root_attributes.tab_width
			# Stephen P. Schaefer, 9/13/2002
			self.first_lines = section.root_attributes.first_lines
			#@-body
			#@-node:1::<<Get root specific attributes>>

			
			#@<<Put @first lines>>
			#@+node:2::<<Put @first lines>>
			#@+body
			# Stephen P. Schaefer 9/13/2002
			if self.first_lines:
				self.os(self.first_lines)
			#@-body
			#@-node:2::<<Put @first lines>>

			if self.use_header_flag and self.print_bits == verbose_bits:
				
				#@<< Write a banner at the start of the output file >>
				#@+node:3::<<Write a banner at the start of the output file>>
				#@+body
				if self.single_comment_string:
					self.os(self.single_comment_string)
					self.os(" Created by Leo from: ")
					self.os(outline_name)
					self.onl() ; self.onl()
				elif self.start_comment_string and self.end_comment_string:
					self.os(self.start_comment_string)
					self.os(" Created by Leo from: ")
					self.os(outline_name)
					self.oblank() ; self.os(self.end_comment_string)
					self.onl() ; self.onl()
				
				#@-body
				#@-node:3::<<Write a banner at the start of the output file>>

			for part in section.parts:
				if part.is_root:
					self.tangle_indent = 0 # Initialize global.
					self.put_part_node(part,false) # output first lws
			self.onl() # Make sure the file ends with a cr/lf
			self.output_file.close()
			self.output_file = None
			if self.errors == 0:
				update_file_if_changed(file_name,temp_name)
			else:
				es("unchanged:  " + file_name)
				
				#@<< Erase the temporary file >>
				#@+node:4::<< Erase the temporary file >>
				#@+body

				try: # Just delete the temp file.
					os.remove(temp_name)
				except: pass
				
				#@-body
				#@-node:4::<< Erase the temporary file >>
	#@-body
	#@-node:2::tangle.put_all_roots
	#@+node:3::put_code
	#@+body
	#@+at
	#  This method outputs a code section, expanding section references by 
	# their definition. We should see no @directives or section definitions 
	# that would end the code section.
	# 
	# Most of the differences bewteen noweb mode and CWEB mode are handled by 
	# token_type(called from put_newline). Here, the only difference is that 
	# noweb handles double-@ signs only at the start of a line.

	#@-at
	#@@c

	def put_code(self,s,no_first_lws_flag):
	
		# trace(`get_line(s,0)`)
		i = 0
		if i < len(s):
			i = self.put_newline(s,i,no_first_lws_flag)
			# Double @ is valid in both noweb and CWEB modes here.
			if match(s,i,"@@"):
				self.os('@') ; i += 2
		while i < len(s):
			progress = i
			ch = s[i]
			if (match(s,i,"<<") and self.use_noweb_flag or
				match(s,i,"@<") and self.use_cweb_flag):
				
				#@<< put possible section reference >>
				#@+node:1::<<put possible section reference >>
				#@+body
				j, kind, name_end = self.is_section_name(s,i)
				if kind == section_def:
					# We are in the middle of a code section
					self.error(
						"Should never happen:\n" +
						"section definition while putting a section reference: " +
						s[i:j])
					i += 1
				elif kind == bad_section_name:
					self.os(s[i]) ; i += 1 # This is not an error.
				else:
					assert(kind == section_ref)
					name = s[i:name_end]
					self.put_section(s,i,name,name_end)
					i = j
				#@-body
				#@-node:1::<<put possible section reference >>

			elif ch == '@': # We are in the middle of a line.
				if self.use_cweb_flag:
					
					#@<< handle 2-character CWEB control codes >>
					#@+node:2::<< handle 2-character CWEB control codes >>
					#@+body
					if match(s,i,"@@"):
						# Handle double @ sign.
						self.os('@') ; i += 2
					else:
						i += 1 # skip the @.
						if i+1 >= len(s) or is_ws_or_nl(s,i):
							# A control code: at-backslash is not a valid CWEB control code.
							# We are in CWEB mode, so we can output C block comments.
							self.os("/*@" + s[i] + "*/") ; i += 1
						else:
							self.os("@") # The at sign is not part of a control code.
					#@-body
					#@-node:2::<< handle 2-character CWEB control codes >>

				else:
					
					#@<< handle noweb @ < < convention >>
					#@+node:3::<< handle noweb @ < < convention >>
					#@+body
					#@+at
					#  The user must ensure that neither @ < < nor @ > > 
					# occurs in comments or strings. However, it is valid for 
					# @ < < or @ > > to appear in the doc chunk or in a 
					# single-line comment.

					#@-at
					#@@c

					if match(s,i,"@<<"):
						self.os("/*@*/<<") ; i += 3
					
					elif match(s,i,"@>>"):
						self.os("/*@*/>>") ; i += 3
						
					else: self.os("@") ; i += 1
					#@-body
					#@-node:3::<< handle noweb @ < < convention >>

			elif ch == body_ignored_newline:
				i += 1
			elif ch == body_newline:
				i += 1 ; self.onl()
				i = self.put_newline(s,i,false) # Put full lws
				if self.use_cweb_flag and match(s,i,"@@"):
					self.os('@') ; i += 2
			else: self.os(s[i]) ; i += 1
			assert(progress < i)
	#@-body
	#@-node:3::put_code
	#@+node:4::put_doc
	#@+body
	# This method outputs a doc section within a block comment.
	
	def put_doc(self,s):
	
		# trace(`get_line(s,0)`)
		width = self.page_width
		words = 0 ; word_width = 0 ; line_width = 0
		# 8/1/02: can't use choose here!
		if self.single_comment_string == None: single_w = 0
		else: single_w = len(self.single_comment_string)
		# Make sure we put at least 20 characters on a line.
		if width - max(0,self.tangle_indent) < 20:
			width = max(0,self.tangle_indent) + 20
		# Skip Initial white space in the doc part.
		i = skip_ws_and_nl(s,0)
		if i < len(s) and self.print_bits == verbose_bits:
			use_block_comment = self.start_comment_string and self.end_comment_string
			use_single_comment = not use_block_comment and self.single_comment_string
			# javadoc_comment = use_block_comment and self.start_comment_string == "/**"
			if use_block_comment or use_single_comment:
				if 0: # The section name ends in an self.onl().
					self.onl()
				self.put_leading_ws(self.tangle_indent)
				if use_block_comment:
					self.os(self.start_comment_string)
				
				#@<< put the doc part >>
				#@+node:1::<<put the doc part>>
				#@+body
				#@+at
				#  This code fills and outputs each line of a doc part. It 
				# keeps track of whether the next word will fit on a line,and 
				# starts a new line if needed.

				#@-at
				#@@c

				if use_single_comment:
					# New code: 5/31/00
					self.os(self.single_comment_string) ; self.otab()
					line_width =(single_w / abs(self.tab_width) + 1) * abs(self.tab_width)
				else:
					line_width = abs(self.tab_width)
					self.onl() ; self.otab()
				self.put_leading_ws(self.tangle_indent)
				line_width += max(0,self.tangle_indent)
				words = 0 ; word_width = 0
				while i < len(s):
					
					#@<<output or skip whitespace or newlines>>
					#@+node:1::<<output or skip whitespace or newlines>>
					#@+body
					#@+at
					#  This outputs whitespace if it fits, and ignores it 
					# otherwise, and starts a new line if a newline is seen. 
					# The effect of self code is that we never start a line 
					# with whitespace that was originally at the end of a line.

					#@-at
					#@@c

					while is_ws_or_nl(s,i):
						ch = s[i]
						if ch == '\t':
							pad = abs(self.tab_width) - (line_width % abs(self.tab_width))
							line_width += pad
							if line_width < width: self.otab()
							i += 1
						elif ch == ' ':
							line_width += 1
							if line_width < width: self.os(ch)
							i += 1
						else:
							assert(is_nl(s,i))
							self.onl()
							if use_single_comment:
								# New code: 5/31/00
								self.os(self.single_comment_string) ; self.otab()
								line_width = (single_w / abs(self.tab_width) + 1) * abs(self.tab_width)
							else:
								self.otab()
								line_width = abs(self.tab_width)
							i = skip_nl(s,i)
							words = 0
							self.put_leading_ws(self.tangle_indent)
					 		# tangle_indent is in spaces.
							line_width += max(0,self.tangle_indent)
					
					#@-body
					#@-node:1::<<output or skip whitespace or newlines>>

					if i >= len(s):
						break
					
					#@<<compute the width of the next word>>
					#@+node:2::<<compute the width of the next word>>
					#@+body
					j = i ; word_width = 0
					while j < len(s) and not is_ws_or_nl(s,j):
						word_width += 1
						j += 1
					#@-body
					#@-node:2::<<compute the width of the next word>>

					if words == 0 or line_width + word_width < width:
						words += 1
						
						#@<<output next word>>
						#@+node:3::<<output next word>>
						#@+body
						while i < len(s) and not is_ws_or_nl(s,i):
							self.os(s[i])
							i += 1
						#@-body
						#@-node:3::<<output next word>>

						line_width += word_width
					else:
						# 11-SEP-2002 DTHEIN: Fixed linewrapping bug in
						# tab-then-comment sequencing
						self.onl()
						if use_single_comment:
							self.os(self.single_comment_string) ; self.otab()
							line_width = (single_w / abs(self.tab_width) + 1) * abs(self.tab_width)
						else:
							self.otab()
							line_width = abs(self.tab_width)
						words = 0
						self.put_leading_ws(self.tangle_indent)
				 		# tangle_indent is in spaces.
						line_width += max(0,self.tangle_indent)
				
				#@-body
				#@-node:1::<<put the doc part>>

				self.onl()
				self.put_leading_ws(self.tangle_indent)
				if use_block_comment:
					self.os(self.end_comment_string)
				self.onl()
			else: self.onl()
	#@-body
	#@-node:4::put_doc
	#@+node:5::put_leading_ws
	#@+body
	# Puts tabs and spaces corresponding to n spaces, assuming that we are at the start of a line.
	
	def put_leading_ws(self,n):
	
		# trace("tab_width:" + `self.tab_width` + ", indent:" + `indent`)
		w = self.tab_width
	
		if w > 1:
			q,r = divmod(n,w) 
			self.otabs(q) 
			self.oblanks(r) 
		else:
			self.oblanks(n)
	
	#@-body
	#@-node:5::put_leading_ws
	#@+node:6::put_newline
	#@+body
	#@+at
	#  This method handles scanning when putting the start of a new line. 
	# Unlike the corresponding method in pass one, this method doesn't need to 
	# set a done flag in the caller because the caller already knows where the 
	# code section ends.

	#@-at
	#@@c

	def put_newline(self,s,i,no_first_lws_flag):
	
		kind, end = self.token_type(s,i,dont_report_errors)
		
		#@<< Output leading white space except for blank lines >>
		#@+node:1::<< Output leading white space except for blank lines >>
		#@+body
		j = i ; i = skip_ws(s,i)
		if i < len(s) and not is_nl(s,i):
			# Conditionally output the leading previous leading whitespace.
			if not no_first_lws_flag:
				self.put_leading_ws(self.tangle_indent)
			# Always output the leading whitespace of _this_ line.
			k, width = skip_leading_ws_with_indent(s,j,self.tab_width)
			self.put_leading_ws(width)
		#@-body
		#@-node:1::<< Output leading white space except for blank lines >>

		if i >= len(s):
			return i
		elif kind == at_web or kind == at_at:
			i += 2 # Allow the line to be scanned.
		elif kind == at_doc or kind == at_code:
			if self.use_cweb_flag:
				i += 2
		else:
			# These should have set limit in pass 1.
			assert(kind != section_def and kind != at_chapter and kind != at_section)
		return i
	#@-body
	#@-node:6::put_newline
	#@+node:7::put_part_node
	#@+body
	# This method outputs one part of a section definition.
	
	def put_part_node(self,part,no_first_lws_flag):
	
		if 0:
			if part: name = part.name # can't use choose.
			else: name = "<NULL part>"
			trace(`name`)
	
		if part.doc and self.output_doc_flag and self.print_bits != silent_bits and part.doc:
			self.put_doc(part.doc)
	
		if part.code:
			self.put_code(part.code,no_first_lws_flag)
	#@-body
	#@-node:7::put_part_node
	#@+node:8::put_section
	#@+body
	#@+at
	#  This method outputs the definition of a section and all sections 
	# referenced from the section. name is the section's name. This code 
	# checks for recursive definitions by calling section_check(). We can not 
	# allow section x to expand to code containing another call to section x, 
	# either directly or indirectly.

	#@-at
	#@@c

	def put_section(self,s,i,name,name_end):
	
		j = skip_line(s,i)
		# trace("indent:" + `self.tangle_indent`  + ", " + `s[i:j]`)
		outer_old_indent = self.tangle_indent
		trailing_ws_indent = 0 # Set below.
		inner_old_indent = 0 # Set below.
		newline_flag = false  # True if the line ends with the reference.
		assert(match(name,0,"<<") or match(name,0,"@<"))
		
		#@<< Calculate the new value of tangle_indent >>
		#@+node:1::<< Calculate the new value of tangle_indent >>
		#@+body
		# Find the start of the line containing the reference.
		j = i
		while j > 0 and not is_nl(s,j):
			j -= 1
		if is_nl(s,j):
			j = skip_nl(s,j)
		
		# Bump the indentation
		j, width = skip_leading_ws_with_indent(s,j,self.tab_width)
		self.tangle_indent += width
		# trace("leading ws:" + `width` + " + new indent:" + `self.tangle_indent`)
		
		# 4/27/01: Force no trailing whitespace in @silent mode.
		if self.print_bits == silent_bits:
			trailing_ws_indent = 0
		else:
			trailing_ws_indent = self.tangle_indent
		
		# Increase the indentation if the section reference does not immediately follow
		# the leading white space.  4/3/01: Make no adjustment in @silent mode.
		if (j < len(s) and self.print_bits != silent_bits and
			((self.use_noweb_flag and s[j] != '<') or
			(self.use_cweb_flag and s[j] != '@'))):
			self.tangle_indent += abs(self.tab_width)
		#@-body
		#@-node:1::<< Calculate the new value of tangle_indent >>

		
		#@<< Set 'newline_flag' if the line ends with the reference >>
		#@+node:2::<< Set 'newline_flag' if the line ends with the reference >>
		#@+body
		if self.print_bits != silent_bits:
			i = name_end
			i = skip_ws(s,i)
			newline_flag = (i >= len(s) or is_nl(s,i))
		#@-body
		#@-node:2::<< Set 'newline_flag' if the line ends with the reference >>

		section = self.st_lookup(name,not_root_name)
		if section and section.parts:
			# Expand the section only if we are not already expanding it.
			if self.section_check(name):
				self.section_stack.append(name)
				
				#@<< put all parts of the section definition >>
				#@+node:3::<<put all parts of the section definition>>
				#@+body
				#@+at
				#  This section outputs each part of a section definition. We 
				# first count how many parts there are so that the code can 
				# output a comment saying 'part x of y'.

				#@-at
				#@@c

				# Output each part of the section.
				sections = len(section.parts)
				count = 0
				for part in section.parts:
					count += 1
					# In @silent mode, there is no sentinel line to "use up" the previously output
					# leading whitespace.  We set the flag to tell put_part_node and put_code
					# not to call put_newline at the start of the first code part of the definition.
					no_first_leading_ws_flag = (count == 1 and self.print_bits == silent_bits)
					inner_old_indent = self.tangle_indent
					# 4/3/01: @silent inhibits newlines after section expansion.
					if self.print_bits != silent_bits:
						
						#@<< Put the section name in a comment >>
						#@+node:1::<< Put the section name in a comment >>
						#@+body
						if count > 1:
							self.onl()
							self.put_leading_ws(self.tangle_indent)
							
						# Don't print trailing whitespace
						name = string.rstrip(name)
						if self.single_comment_string:
							self.os(self.single_comment_string) ; self.oblank() ; self.os(name)
							
							#@<< put (n of m) >>
							#@+node:1::<< put ( n of m ) >>
							#@+body
							if sections > 1:
								self.oblank()
								self.os("(" + `count` + " of " + `sections` + ")")
							#@-body
							#@-node:1::<< put ( n of m ) >>

						else:
							assert(
								self.start_comment_string and len(self.start_comment_string) > 0 and
								self.end_comment_string and len(self.end_comment_string)> 0)
							self.os(self.start_comment_string) ; self.oblank() ; self.os(name)
							
							#@<< put (n of m) >>
							#@+node:1::<< put ( n of m ) >>
							#@+body
							if sections > 1:
								self.oblank()
								self.os("(" + `count` + " of " + `sections` + ")")
							#@-body
							#@-node:1::<< put ( n of m ) >>

							self.oblank() ; self.os(self.end_comment_string)
						
						self.onl() # Always output a newline.
						#@-body
						#@-node:1::<< Put the section name in a comment >>

					self.put_part_node(part,no_first_leading_ws_flag)
					# 4/3/01: @silent inhibits newlines after section expansion.
					if count == sections and self.print_bits != silent_bits:
						
						#@<< Put the ending comment >>
						#@+node:2::<< Put the ending comment >>
						#@+body
						#@+at
						#  We do not produce an ending comment unless we are 
						# ending the last part of the section,and the comment 
						# is clearer if we don't say(n of m).

						#@-at
						#@@c

						self.onl() ; self.put_leading_ws(self.tangle_indent)
						#  Don't print trailing whitespace
						while name_end > 0 and is_ws(s[name_end-1]):
							name_end -= 1
						
						if self.single_comment_string:
							self.os(self.single_comment_string) ; self.oblank()
							self.os("-- end -- ") ; self.os(name)
						else:
							self.os(self.start_comment_string) ; self.oblank()
							self.os("-- end -- ") ; self.os(name)
							self.oblank() ; self.os(self.end_comment_string)
							

						#@+at
						#  The following code sets a flag for untangle.
						# 
						# If something follows the section reference we must 
						# add a newline, otherwise the "something" would 
						# become part of the comment.  Any whitespace 
						# following the (!newline) should follow the section 
						# defintion when Untangled.

						#@-at
						#@@c

						if not newline_flag:
							self.os(" (!newline)") # LeoCB puts the leading blank, so we must do so too.
							# Put the whitespace following the reference.
							while name_end < len(s) and is_ws(s[name_end]):
								self.os(s[name_end])
								name_end += 1
							self.onl() # We must supply the newline!
						#@-body
						#@-node:2::<< Put the ending comment >>

					# Restore the old indent.
					self.tangle_indent = inner_old_indent
				#@-body
				#@-node:3::<<put all parts of the section definition>>

				self.section_stack.pop()
		else:
			
			#@<< Put a comment about the undefined section >>
			#@+node:4::<<Put a comment about the undefined section>>
			#@+body
			self.onl() ; self.put_leading_ws(self.tangle_indent)
			
			if self.print_bits != silent_bits:
				if self.single_comment_string:
					self.os(self.single_comment_string)
					self.os(" undefined section: ") ; self.os(name) ; self.onl()
				else:
					self.os(self.start_comment_string)
					self.os(" undefined section: ") ; self.os(name)
					self.oblank() ; self.os(self.end_comment_string) ; self.onl()
			
			self.error("Undefined section: " + name)
			#@-body
			#@-node:4::<<Put a comment about the undefined section>>

		if not newline_flag:
			self.put_leading_ws(trailing_ws_indent)
		self.tangle_indent = outer_old_indent
		return i, name_end
	#@-body
	#@-node:8::put_section
	#@+node:9::section_check
	#@+body
	#@+at
	#  We can not allow a section to be defined in terms of itself, either 
	# directly or indirectly.
	# 
	# We push an entry on the section stack whenever beginning to expand a 
	# section and pop the section stack at the end of each section.  This 
	# method checks whether the given name appears in the stack. If so, the 
	# section is defined in terms of itself.

	#@-at
	#@@c

	def section_check (self,name):
	
		if name in self.section_stack:
			s = "Invalid recursive reference of " + name + "\n"
			for n in self.section_stack:
				s += "called from: " + n + "\n"
			self.error(s)
			return false
		return true
	#@-body
	#@-node:9::section_check
	#@-node:2::Pass 2
	#@-node:4::tangle
	#@+node:5::tst
	#@+node:1::st_check
	#@+body
	#@+at
	#  This function checks the given symbol table for defined but never 
	# referenced sections.

	#@-at
	#@@c

	def st_check(self):
	
		keys = self.tst.keys()
		keys.sort()
		# trace(`keys`)
		for name in keys:
			section = self.tst[name]
			if not section.referenced:
				es(	' ' * 4 + "Warning: " +
					choose(self.use_noweb_flag,"<< ","@< ") +
					section.name +
					choose(self.use_noweb_flag," >>"," @>") +
					" has been defined but not used.")
	#@-body
	#@-node:1::st_check
	#@+node:2::st_dump
	#@+body
	# Dumps the given symbol table in a readable format.
	
	def st_dump(self,verbose_flag):
		
		s = "\ndump of symbol table...\n"
		keys = self.tst.keys()
		keys.sort()
		for name in keys:
			section = self.tst[name]
			if verbose_flag:
				s += self.st_dump_node(section)
			else:
				type = choose(len(section.parts)>0,"  ","un")
				s += ("\n" + type + "defined:[" + section.name + "]")
		return s
	#@-body
	#@-node:2::st_dump
	#@+node:3::st_dump_node
	#@+body
	# Dumps each part of a section's definition.
	
	def st_dump_node(self,section):
	
		s = ("\nsection: " + section.name +
			", referenced:" + `section.referenced` +
			", is root:" + `section.is_root`)
		
		if len(section.parts) > 0:
			s += "\n----- parts of " + angleBrackets(section.name)
			n = 1 # part list is in numeric order
			for part in section.parts:
				s += "\n----- Part " + `n`
				n += 1
				s += "\ndoc:  [" + `part.doc`  + "]"
				s += "\ncode: [" + `part.code` + "]"
			s += "\n----- end of partList\n"
		return s
	#@-body
	#@-node:3::st_dump_node
	#@+node:4::st_enter
	#@+body
	#@+at
	#  Enters names and their associated code and doc parts into the given 
	# symbol table.
	# `is_dirty` is used only when entering root names.

	#@-at
	#@@c

	def st_enter(self,name,code,doc,multiple_parts_flag,is_root_flag,
		# Stephen Schaefer, 9/2/02
		language=None,
		single_comment_string=None,
		start_comment_string=None,
		end_comment_string=None):
		
		# trace(`name`)
		section = self.st_lookup(name,is_root_flag)
		assert(section)
		if doc:
			doc = string.rstrip(doc) # remove trailing lines.
		if code:
			if self.print_bits != silent_bits: # @silent supresses newline processing.
				i = skip_blank_lines(code,0) # remove leading lines.
				if i > 0: code = code[i:] 
				if code and len(code) > 0: code = string.rstrip(code) # remove trailing lines.
			if len(code) == 0: code = None
		if code:
			
			#@<< check for duplicate code definitions >>
			#@+node:1::<<check for duplicate code definitions >>
			#@+body
			for part in section.parts:
			
				if part.code and multiple_parts_flag == disallow_multiple_parts:
					# Give the message only for non-empty parts.
					self.error("Multiple parts not allowed for " + name)
				  	return 0 # part number
			
				if self.tangling and code and code == part.code:
					es("Warning: possible duplicate definition of: <<" +
						section.name + ">>")
			#@-body
			#@-node:1::<<check for duplicate code definitions >>

		if code or doc:
			part = part_node(name,code,doc,is_root_flag,false) # not dirty
			section.parts.append(part)
		else: # A reference
			section.referenced = true
		if is_root_flag:
			self.root_list.append(section)
			section.referenced = true # Mark the root as referenced.
			
			#@<<remember root node attributes>>
			#@+node:2::<<remember root node attributes>>
			#@+body
			# Stephen Schaefer, 9/2/02
			# remember the language and comment characteristics
			section.root_attributes = root_attributes(self)
			#@-body
			#@-node:2::<<remember root node attributes>>
# Stephen Schaefer, 9/2/02	return len(section.parts) # part number
	
	#@-body
	#@-node:4::st_enter
	#@+node:5::st_enter_root_name
	#@+body
	# Enters a root name into the given symbol table.
	
	def st_enter_root_name(self,name,code,doc):
		
		# assert(code)
		if name: # User errors can result in an empty @root name.
			self.st_enter(name,code,doc,disallow_multiple_parts,is_root_name)
	#@-body
	#@-node:5::st_enter_root_name
	#@+node:6::st_enter_section_name
	#@+body
	#@+at
	#  This function enters a section name into the given symbol table.
	# The code and doc pointers are None for references.

	#@-at
	#@@c

	def st_enter_section_name(self,name,code,doc,multiple_parts_flag):
		
		return self.st_enter(name,code,doc,multiple_parts_flag,not_root_name)
	#@-body
	#@-node:6::st_enter_section_name
	#@+node:7::st_lookup
	#@+body
	#@+at
	#  This function looks up name in the symbol table and creates a tst_node 
	# for it if it does not exist.

	#@-at
	#@@c

	def st_lookup(self,name,is_root_flag):
	
		if is_root_flag:
			key = name
		else:
			key = self.standardize_name(name)
	
		if self.tst.has_key(key):
			section = self.tst[key]
			# trace("found:" + key)
			return section
		else:
			# trace("not found:" + key)
			section = tst_node(key,is_root_flag)
			self.tst [key] = section
			return section
	#@-body
	#@-node:7::st_lookup
	#@-node:5::tst
	#@+node:6::ust
	#@+node:1::ust_dump
	#@+body
	def ust_dump (self):
	
		s = "\n---------- Untangle Symbol Table ----------"
		keys = self.ust.keys()
		keys.sort()
		for name in keys:
			section = self.ust[name]
			s += "\n\n" + section.name
			for part in section.parts.values():
				assert(part.of == section.of)
				s += "\n----- part " + `part.part` + " of " + `part.of` + " -----\n"
				s += `get_line(part.code,0)`
		s += "\n--------------------"
		return s
	#@-body
	#@-node:1::ust_dump
	#@+node:2::ust_enter
	#@+body
	#@+at
	#  This routine enters names and their code parts into the given table. 
	# The 'part' and 'of' parameters are taken from the "(part n of m)" 
	# portion of the line that introduces the section definition in the C code.
	# 
	# If no part numbers are given the caller should set the 'part' and 'of' 
	# parameters to zero.  The caller is reponsible for checking for duplicate parts.
	# 
	# This function handles names scanned from a source file; the 
	# corresponding st_enter routine handles names scanned from outlines.

	#@-at
	#@@c

	def ust_enter (self,name,part,of,code,nl_flag,is_root_flag):
	
		if not is_root_flag:
			name = self.standardize_name(name)
		
		#@<< remove blank lines from the start and end of the text >>
		#@+node:1::<< remove blank lines from the start and end of the text >>
		#@+body
		i = skip_blank_lines(code,0)
		if i > 0:
			code = code[i:]
			code = string.rstrip(code)
		
		#@-body
		#@-node:1::<< remove blank lines from the start and end of the text >>

		u = ust_node(name,code,part,of,nl_flag,false) # update_flag
		if not self.ust.has_key(name):
			self.ust[name] = u
		section = self.ust[name]
		section.parts[part]=u # Parts may be defined in any order.
		# trace("section name: [" + name + "](" + `part` + " of " + `of` + ")..."+`get_line(code,0)`)
	#@-body
	#@-node:2::ust_enter
	#@+node:3::ust_lookup
	#@+body
	# Searches the given table for a part matching the name and part number.
	
	def ust_lookup (self,name,part_number,is_root_flag,update_flag):
		
		# trace(`name` + ":" + `part_number`)
		
		if not is_root_flag:
			name = self.standardize_name(name)
	
		if part_number == 0: part_number = 1 # A hack: zero indicates the first part.
		if self.ust.has_key(name):
			section = self.ust[name]
			if section.parts.has_key(part_number):
				part = section.parts[part_number]
				if update_flag: part.update_flag = true
				# trace("found:" + name + " (" + `part_number` + ")...\n" + `get_line(part.code,0)`)
				return part, true
	
		# trace("not found:" + name + " (" + `part_number` + ")...\n")
		return None, false
	#@-body
	#@-node:3::ust_lookup
	#@+node:4::ust_warn_about_orphans
	#@+body
	#@+at
	#  This function issues a warning about any sections in the derived file 
	# for which no corresponding section has been seen in the outline.

	#@-at
	#@@c

	def ust_warn_about_orphans (self):
	
		for section in self.ust.values():
			# trace(`section`)
			for part in section.parts.values():
				assert(part.of == section.of)
				if not part.update_flag:
					es("Warning: " +
						choose(self.use_noweb_flag,"<< ","@< ") +
						part.name +
						choose(self.use_noweb_flag," >>"," @>") +
						" is not in the outline")
					break # One warning per section is enough.
	#@-body
	#@-node:4::ust_warn_about_orphans
	#@-node:6::ust
	#@+node:7::untangle
	#@+node:1::compare_comments
	#@+body
	#@+at
	#  This function compares the interior of comments and returns true if 
	# they are identical except for whitespace or newlines. It is up to the 
	# caller to eliminate the opening and closing delimiters from the text to 
	# be compared.

	#@-at
	#@@c

	def compare_comments (self,s1,s2):
	
		tot_len = 0
		if self.comment: tot_len += len(self.comment)
		if self.comment_end: tot_len += len(self.comment_end)
		CWEB_flag = (self.language == c_language and not self.use_noweb_flag)
		
		p1, p2 = 0, 0
		while p1 < len(s1) and p2 < len(s2):
			p1 = skip_ws_and_nl(s1,p1)
			p2 = skip_ws_and_nl(s2,p2)
			if self.comment and self.comment_end:
				
				#@<< Check both parts for @ comment conventions >>
				#@+node:1::<< Check both parts for @ comment conventions >>
				#@+body
				#@+at
				#  This code is used in forgiving_compare()and in compare_comments().
				# 
				# In noweb mode we allow / * @ * /  (without the spaces)to be 
				# equal to @.
				# In CWEB mode we allow / * @ ? * / (without the spaces)to be 
				# equal to @?.
				# at-backslash is not a valid CWEB control code, so we don't 
				# have to equate
				# / * @ \\ * / with at-backslash.
				# 
				# We must be careful not to run afoul of this very convention here!

				#@-at
				#@@c

				if p1 < len(s1) and s1[p1] == '@':
					if match(s2,p2,self.comment + '@' + self.comment_end):
						p1 += 1
						p2 += tot_len + 1
						continue
					elif (CWEB_flag and s1[p1] == '@' and p1 + 1 < len(s1) and
						match(s2,p2,self.comment + '@' + s1[p1+1])):
						p1 += 2
						p2 += tot_len + 2
						continue
				elif p2 < len(s2) and s2[p2] == '@':
					if match(s1,p1,self.comment + '@' + self.comment_end):
						p2 += 1
						p1 += tot_len + 1
						continue
					elif (CWEB_flag and s1[p1] == '@' and p1 + 1 < len(s1) and
						match(s1,p1,self.comment + '@' + s2[p2+1])):
						p2 += 2
						p1 += tot_len + 2
						continue
				
				#@-body
				#@-node:1::<< Check both parts for @ comment conventions >>

			if p1 >= len(s1) or p2 >= len(s2):
				break
			if s1[p1] != s2[p2]:
				return false
			p1 += 1 ; p2 += 1
		p1 = skip_ws_and_nl(s1,p1)
		p2 = skip_ws_and_nl(s2,p2)
		return p1 == len(s1) and p2 == len(s2)
	
	#@-body
	#@-node:1::compare_comments
	#@+node:2::massage_block_comment (no longer used)
	#@+body
	#@+at
	#  This function is called to massage an @doc part in the ust. We call 
	# this routine only after a mismatch in @doc parts is found between the 
	# ust and tst. On entry, the parameters point to the inside of a block C 
	# comment: the opening and closing delimiters are not part of the text 
	# handled by self routine.
	# 
	# This code removes newlines that may have been inserted by the Tangle 
	# command in a block comment. Tangle may break lines differently in 
	# different expansions, but line breaks are ignored by forgiving_compare() 
	# and doc_compare() within block C comments.
	# 
	# We count the leading whitespace from the first non-blank line and remove 
	# this much whitespace from all lines. We also remove singleton newlines 
	# and replace sequences of two or more newlines by a single newline.

	#@-at
	#@@c

	def massage_block_comment (self,s):
	
		c = self.commands
		newlines = 0  # Consecutive newlines seen.
		i = skip_blank_lines(s,0)
		# Copy the first line and set n
		i, n = skip_leading_ws_with_indent(s,i,c.tab_width)
		j = i ; i = skip_to_end_of_line(s,i)
		result = s[j:i]
		while i < len(s):
			assert(is_nl(s,i))
			newlines += 1
			# Replace the first newline with a blank.
			result += ' ' ; i += 1
			while i < len(s) and is_nl(s,i):
				i += 1 # skip the newline.
			j = i ; i = skip_ws(s,i)
			if is_nl(s,i)and newlines > 1:
				# Skip blank lines.
				while is_nl(s,i):
					i += 1
			else:
				# Skip the leading whitespace.
				i = j # back track
				i = skip_leading_ws(s,i,n,c.tab_width)
				newlines = 0
				# Copy the rest of the line.
				j = i ; i = skip_to_end_of_line(s,i)
				result += s[j:i]
		return result
	
	#@-body
	#@-node:2::massage_block_comment (no longer used)
	#@+node:3::forgiving_compare
	#@+body
	#@+at
	#  This is the "forgiving compare" function.  It compares two texts and 
	# returns true if they are identical except for comments or non-critical 
	# whitespace.  Whitespace inside strings or preprocessor directives must 
	# match exactly.

	#@-at
	#@@c

	def forgiving_compare (self,name,part,s1,s2):
	
		# trace(`name` +":"+ `part` +"\n1:"+ `get_line(s1,0)` +"\n2:"+ `get_line(s2,0)`)
		
		#@<< Define forgiving_compare vars >>
		#@+node:1::<< Define forgiving_compare vars >>
		#@+body
		# scan_derived_file has set the ivars describing comment delims.
		first1 = first2 = 0
		
		tot_len = 0
		if self.comment: tot_len += len(self.comment)
		if self.comment_end: tot_len += len(self.comment_end)
		
		CWEB_flag = (self.language == c_language and not self.use_noweb_flag)
		#@-body
		#@-node:1::<< Define forgiving_compare vars >>

		p1 = skip_ws_and_nl(s1,0) 
		p2 = skip_ws_and_nl(s2,0)
		result = true
		while result and p1 < len(s1) and p2 < len(s2):
			first1 = p1 ; first2 = p2
			if self.comment and self.comment_end:
				
				#@<< Check both parts for @ comment conventions >>
				#@+node:2::<< Check both parts for @ comment conventions >>
				#@+body
				#@+at
				#  This code is used in forgiving_compare()and in compare_comments().
				# 
				# In noweb mode we allow / * @ * /  (without the spaces)to be 
				# equal to @.
				# In CWEB mode we allow / * @ ? * / (without the spaces)to be 
				# equal to @?.
				# at-backslash is not a valid CWEB control code, so we don't 
				# have to equate
				# / * @ \\ * / with at-backslash.
				# 
				# We must be careful not to run afoul of this very convention here!

				#@-at
				#@@c

				if p1 < len(s1) and s1[p1] == '@':
					if match(s2,p2,self.comment + '@' + self.comment_end):
						p1 += 1
						p2 += tot_len + 1
						continue
					elif (CWEB_flag and s1[p1] == '@' and p1 + 1 < len(s1) and
						match(s2,p2,self.comment + '@' + s1[p1+1])):
						p1 += 2
						p2 += tot_len + 2
						continue
				elif p2 < len(s2) and s2[p2] == '@':
					if match(s1,p1,self.comment + '@' + self.comment_end):
						p2 += 1
						p1 += tot_len + 1
						continue
					elif (CWEB_flag and s1[p1] == '@' and p1 + 1 < len(s1) and
						match(s1,p1,self.comment + '@' + s2[p2+1])):
						p2 += 2
						p1 += tot_len + 2
						continue
				
				#@-body
				#@-node:2::<< Check both parts for @ comment conventions >>

			ch1 = s1[p1]
			if ch1 == '\r' or ch1 == '\n':
				
				#@<< Compare non-critical newlines >>
				#@+node:3::<< Compare non-critical newlines >>
				#@+body
				p1 = skip_ws_and_nl(s1,p1)
				p2 = skip_ws_and_nl(s2,p2)
				
				#@-body
				#@-node:3::<< Compare non-critical newlines >>

			elif ch1 ==  ' ' or ch1 == '\t':
				
				#@<< Compare non-critical whitespace >>
				#@+node:4::<< Compare non-critical whitespace >>
				#@+body
				p1 = skip_ws(s1,p1)
				p2 = skip_ws(s2,p2)
				#@-body
				#@-node:4::<< Compare non-critical whitespace >>

			elif ch1 == '\'' or ch1 == '"':
				
				#@<< Compare possible strings >>
				#@+node:6::<< Compare possible strings >>
				#@+body
				# This code implicitly assumes that string1_len == string2_len == 1.
				# The match test ensures that the language actually supports strings.
				
				if (match(s1,p1,self.string1) or match(s1,p1,self.string2)) and s1[p1] == s2[p2]:
				
					if self.language == pascal_language:
						
						#@<< Compare Pascal strings >>
						#@+node:3::<< Compare Pascal strings >>
						#@+body
						#@+at
						#  We assume the Pascal string is on a single line so 
						# the problems with cr/lf do not concern us.

						#@-at
						#@@c

						first1 = p1 ; first2 = p2
						p1 = skip_pascal_string(s1,p1)
						p2 = skip_pascal_string(s2,p2)
						result = s1[first1,p1] == s2[first2,p2]
						
						#@-body
						#@-node:3::<< Compare Pascal strings >>

					else:
						
						#@<< Compare C strings >>
						#@+node:2::<< Compare C strings >>
						#@+body
						delim = s1[p1]
						result = s1[p1] == s2[p2]
						p1 += 1 ; p2 += 1
						
						while result and p1 < len(s1) and p2 < len(s2):
							if s1[p1] == delim and self.is_end_of_string(s1,p1,delim):
								result =(s2[p2] == delim and self.is_end_of_string(s2,p2,delim))
								p1 += 1 ; p2 += 1
								break
							elif is_nl(s1,p1) and is_nl(s2,p2):
								p1 = skip_nl(s1,p1)
								p2 = skip_nl(s2,p2)
							else:
								result = s1[p1] == s2[p2]
								p1 += 1 ; p2 += 1
						
						#@-body
						#@-node:2::<< Compare C strings >>

					if not result:
						self.mismatch("Mismatched strings")
				else:
					
					#@<< Compare single characters >>
					#@+node:1::<< Compare single characters >>
					#@+body
					assert(p1 < len(s1) and p2 < len(s2))
					result = s1[p1] == s2[p2]
					p1 += 1 ; p2 += 1
					if not result: self.mismatch("Mismatched single characters")
					#@-body
					#@-node:1::<< Compare single characters >>
				#@-body
				#@-node:6::<< Compare possible strings >>

			elif ch1 == '#':
				
				#@<< Compare possible preprocessor directives >>
				#@+node:5::<< Compare possible preprocessor directives >>
				#@+body
				if self.language == c_language:
					
					#@<< compare preprocessor directives >>
					#@+node:2::<< Compare preprocessor directives >>
					#@+body
					# We cannot assume that newlines are single characters.
					
					result = s1[p1] == s2[p2]
					p1 += 1 ; p2 += 1
					while result and p1 < len(s1) and p2 < len(s2):
						if is_nl(s1,p1):
							result = is_nl(s2,p2)
							if not result or self.is_end_of_directive(s1,p1):
								break
							p1 = skip_nl(s1,p1)
							p2 = skip_nl(s2,p2)
						else:
							result = s1[p1] == s2[p2]
							p1 += 1 ; p2 += 1
					if not result:
						self.mismatch("Mismatched preprocessor directives")
					#@-body
					#@-node:2::<< Compare preprocessor directives >>

				else:
					
					#@<< compare single characters >>
					#@+node:1::<< Compare single characters >>
					#@+body
					assert(p1 < len(s1) and p2 < len(s2))
					result = s1[p1] == s2[p2]
					p1 += 1 ; p2 += 1
					if not result: self.mismatch("Mismatched single characters")
					#@-body
					#@-node:1::<< Compare single characters >>

				
				#@-body
				#@-node:5::<< Compare possible preprocessor directives >>

			elif ch1 == '<' or ch1 == '@':
				
				#@<< Compare possible section references >>
				#@+node:7::<< Compare possible section references >>
				#@+body
				if s1[p1] == '@' and CWEB_flag:  start_ref = "@<"
				elif s1[p1] == '<' and not CWEB_flag:  start_ref = "<<"
				else: start_ref = None
				
				# Tangling may insert newlines.
				p2 = skip_ws_and_nl(s2,p2)
				
				junk, kind1, junk2 = self.is_section_name(s1,p1)
				junk, kind2, junk2 = self.is_section_name(s2,p2)
				
				if start_ref and (kind1 != bad_section_name or kind2 != bad_section_name):
					result = self.compare_section_names(s1[p1:],s2[p2:])
					if result:
						p1, junk1, junk2 = self.skip_section_name(s1,p1)
						p2, junk1, junk2 = self.skip_section_name(s2,p2)
					else: self.mismatch("Mismatched section names")
				else:
					# Neither p1 nor p2 points at a section name.
					result = s1[p1] == s2[p2]
					p1 += 1 ; p2 += 1
					if not result:
						self.mismatch("Mismatch at '@' or '<'")
				#@-body
				#@-node:7::<< Compare possible section references >>

			else:
				
				#@<< Compare comments or single characters >>
				#@+node:8::<< Compare comments or single characters >>
				#@+body
				if match(s1,p1,self.sentinel) and match(s2,p2,self.sentinel):
					first1 = p1 ; first2 = p2
					p1 = skip_to_end_of_line(s1,p1)
					p2 = skip_to_end_of_line(s2,p2)
					result = self.compare_comments(s1[first1:p1],s2[first2:p2])
					if not result:
						self.mismatch("Mismatched sentinel comments")
				elif match(s1,p1,self.line_comment) and match(s2,p2,self.line_comment):
					first1 = p1 ; first2 = p2
					p1 = skip_to_end_of_line(s1,p1)
					p2 = skip_to_end_of_line(s2,p2)
					result = self.compare_comments(s1[first1:p1],s2[first2:p2])
					if not result:
						self.mismatch("Mismatched single-line comments")
				elif match(s1,p1,self.comment) and match(s2,p2,self.comment):
					while (p1 < len(s1) and p2 < len(s2) and
						not match(s1,p1,self.comment_end) and not match(s2,p2,self.comment_end)):
						# ws doesn't have to match exactly either!
						if is_nl(s1,p1)or is_ws(s1[p1]):
							p1 = skip_ws_and_nl(s1,p1)
						else: p1 += 1
						if is_nl(s2,p2)or is_ws(s2[p2]):
							p2 = skip_ws_and_nl(s2,p2)
						else: p2 += 1
					p1 = skip_ws_and_nl(s1,p1)
					p2 = skip_ws_and_nl(s2,p2)
					if match(s1,p1,self.comment_end) and match(s2,p2,self.comment_end):
						first1 = p1 ; first2 = p2
						p1 += len(self.comment_end)
						p2 += len(self.comment_end)
						result = self.compare_comments(s1[first1:p1],s2[first2:p2])
					else: result = false
					if not result:
						self.mismatch("Mismatched block comments")
				elif match(s1,p1,self.comment2) and match(s2,p2,self.comment2):
					while (p1 < len(s1) and p2 < len(s2) and
						not match(s1,p1,self.comment2_end) and not match(s2,p2,self.comment2_end)):
						# ws doesn't have to match exactly either!
						if  is_nl(s1,p1)or is_ws(s1[p1]):
							p1 = skip_ws_and_nl(s1,p1)
						else: p1 += 1
						if is_nl(s2,p2)or is_ws(s2[p2]):
							p2 = skip_ws_and_nl(s2,p2)
						else: p2 += 1
					p1 = skip_ws_and_nl(s1,p1)
					p2 = skip_ws_and_nl(s2,p2)
					if match(s1,p1,self.comment2_end) and match(s2,p2,self.comment2_end):
						first1 = p1 ; first2 = p2
						p1 += len(self.comment2_end)
						p2 += len(self.comment2_end)
						result = self.compare_comments(s1[first1:p1],s2[first2:p2])
					else: result = false
					if not result:
						self.mismatch("Mismatched alternalte block comments")
				else:
					
					#@<< Compare single characters >>
					#@+node:1::<< Compare single characters >>
					#@+body
					assert(p1 < len(s1) and p2 < len(s2))
					result = s1[p1] == s2[p2]
					p1 += 1 ; p2 += 1
					if not result: self.mismatch("Mismatched single characters")
					#@-body
					#@-node:1::<< Compare single characters >>
				#@-body
				#@-node:8::<< Compare comments or single characters >>

		
		#@<< Make sure both parts have ended >>
		#@+node:9::<< Make sure both parts have ended >>
		#@+body
		if result:
			p1 = skip_ws_and_nl(s1,p1)
			p2 = skip_ws_and_nl(s2,p2)
			result = p1 >= len(s1) and p2 >= len(s2)
			if not result:
				# Show the ends of both parts.
				p1 = len(s1)
				p2 = len(s2)
				self.mismatch("One part ends before the other.")
		#@-body
		#@-node:9::<< Make sure both parts have ended >>

		if not result:
			
			#@<< trace the mismatch >>
			#@+node:10::<< Trace the mismatch >>
			#@+body
			if 0:
				trace(self.message +
					"\nPart " + `part` + ", section " + name +
					"\n1:" + get_line(s1,p1) +
					"\n2:" + get_line(s2,p2) )
			#@-body
			#@-node:10::<< Trace the mismatch >>

		return result
	#@-body
	#@-node:3::forgiving_compare
	#@+node:4::mismatch
	#@+body
	def mismatch (self,message):
	
		self.message = message
	#@-body
	#@-node:4::mismatch
	#@+node:5::scan_derived_file (pass 1)
	#@+body
	#@+at
	#  This function scans an entire derived file in s, discovering section or 
	# part definitions.
	# 
	# This is the easiest place to delete leading whitespace from each line: 
	# we simply don't copy it.  We also ignore leading blank lines and 
	# trailing blank lines.  The resulting definition must compare equal using 
	# the "forgiving" compare to any other definitions of that section or part.
	# 
	# We use a stack to handle nested expansions.  The outermost level of 
	# expansion corresponds to the @root directive that created the file.  
	# When the stack is popped, the indent variable is restored.
	# 
	# self.root_name is the name of the file mentioned in the @root directive.
	# 
	# The caller has deleted all body_ignored_newlines from the text.

	#@-at
	#@@c

	def scan_derived_file (self,s):
	
		c = self.commands
		self.def_stack = []
		
		#@<< set the private global matching vars >>
		#@+node:1::<< set the private global matching vars >>
		#@+body
		# Set defaults from the public globals set by the @comment command.
		if self.single_comment_string:
			self.sentinel = self.single_comment_string
			self.sentinel_end = None
		elif self.end_comment_string:
			self.sentinel = self.start_comment_string
			self.sentinel_end = self.end_comment_string
		else:
			self.sentinel = self.sentinel_end = None
			
		if 0:
			trace("single,start,end,sentinel:"+
				`self.single_comment_string` +":"+ `self.start_comment_string` +":"+
				`self.end_comment_string` +":"+ `self.sentinel`)
		
		# Set defaults.  See set_delims_from_langauge.
		self.line_comment = self.single_comment_string
		self.comment = self.start_comment_string
		self.comment_end = self.end_comment_string
		self.comment2 = self.comment2_end = None
		self.string1 = "\""
		self.string2 = "'"
		self.verbatim = None
		
		# Set special cases.
		if self.language == plain_text_language:
			self.string1 = self.string2 = None # This is debatable.
			self.line_comment = None
		if self.language == pascal_language:
			self.comment2 = "(*" ; self.comment2_end = "*)"
		#@-body
		#@-node:1::<< set the private global matching vars >>

		line_indent = 0  # The indentation to use if we see a section reference.
		# indent is the leading whitespace to be deleted.
		i, indent = skip_leading_ws_with_indent(s,0,self.tab_width)
		
		#@<< Skip the header line output by tangle >>
		#@+node:2::<< Skip the header line output by tangle >>
		#@+body
		if self.sentinel or self.comment:
			line = choose(self.sentinel,self.sentinel,self.comment) + " Created by Leo from" 
			if match(s,i,line):
				# Even a block comment will end on the first line.
				i = skip_to_end_of_line(s,i)
		#@-body
		#@-node:2::<< Skip the header line output by tangle >>

		# The top level of the stack represents the root.
		self.push_new_def_node(self.root_name,indent,1,1,true)
		while i < len(s):
			ch = s[i]
			if ch == body_ignored_newline:
				i += 1 # ignore
			elif ch == body_newline:
				
				#@<< handle the start of a new line >>
				#@+node:3::<< handle the start of a new line >>
				#@+body
				self.copy(ch) ; i += 1 # This works because we have one-character newlines.
				
				# Set line_indent, used only if we see a section reference.
				junk, line_indent = skip_leading_ws_with_indent(s,i,c.tab_width)
				i = skip_leading_ws(s,i,indent,c.tab_width) # skip indent leading white space.
				#@-body
				#@-node:3::<< handle the start of a new line >>

			elif match(s,i,self.sentinel) and self.is_sentinel_line(s,i):
				
				#@<< handle a sentinel line  >>
				#@+node:4::<< handle a sentinel line >>
				#@+body
				#@+at
				#  This is the place to eliminate the proper amount of 
				# whitespace from the start of each line. We do this by 
				# setting the 'indent' variable to the leading whitespace of 
				# the first _non-blank_ line following the opening sentinel.
				# 
				# Tangle increases the indentation by one tab if the section 
				# reference is not the first non-whitespace item on the 
				# line,so self code must do the same.

				#@-at
				#@@c

				# trace(`get_line(s,i)`)
				result,junk,kind,name,part,of,end,nl_flag = self.is_sentinel_line_with_data(s,i)
				assert(result==true)
				
				#@<< terminate the previous part of this section if it exists >>
				#@+node:1::<< terminate the previous part of this section if it exists >>
				#@+body
				#@+at
				#  We have just seen a sentinel line. Any kind of sentinel 
				# line will terminate a previous part of the present 
				# definition. For end sentinel lines, the present section name 
				# must match the name on the top of the stack.

				#@-at
				#@@c

				if len(self.def_stack) > 0:
					dn = self.def_stack[-1]
					if self.compare_section_names(name,dn.name):
						dn = self.def_stack.pop()
						if len(dn.code) > 0:
							thePart, found = self.ust_lookup(name,dn.part,false,false) # not root, not update
							# Check for incompatible previous definition.
							if found and not self.forgiving_compare(name,dn.part,dn.code,thePart.code):
								self.error("Incompatible definitions of " + name)
							elif not found:
								self.ust_enter(name,dn.part,dn.of,dn.code,dn.nl_flag,false) # not root
					elif kind == end_sentinel_line:
						self.error("Missing sentinel line for: " + name)
				#@-body
				#@-node:1::<< terminate the previous part of this section if it exists >>

				
				if kind == start_sentinel_line:
					indent = line_indent
					# Increase line_indent by one tab width if the
					# the section reference does not start the line.
					j = i - 1
					while j >= 0:
						if is_nl(s,j):
							break
						elif not is_ws(s[j]):
							indent += abs(self.tab_width) ; break
						j -= 1
					# copy the section reference to the _present_ section,
					# but only if this is the first part of the section.
					if part < 2: self.copy(name)
					# Skip to the first character of the new section definition.
					i = skip_to_end_of_line(s,i)
					# Start the new section.
					self.push_new_def_node(name,indent,part,of,nl_flag)
				else:
					assert(kind == end_sentinel_line)
					# Skip the sentinel line.
					i = skip_to_end_of_line(s,i)
					# Skip a newline only if it was added after(!newline)
					if not nl_flag:
						i = skip_ws(s,i)
						i = skip_nl(s,i)
						i = skip_ws(s,i)
						# Copy any whitespace following the (!newline)
						while end and is_ws(s[end]):
							self.copy(s[end])
							end += 1
					# Restore the old indentation level.
					if len(self.def_stack) > 0:
						indent = self.def_stack[-1].indent
				#@-body
				#@-node:4::<< handle a sentinel line >>

			elif match(s,i,self.line_comment) or match(s,i,self.verbatim):
				
				#@<< copy the entire line >>
				#@+node:5::<< copy the entire line >>
				#@+body
				j = i ; i = skip_to_end_of_line(s,i)
				self.copy(s[j:i])
				
				#@-body
				#@-node:5::<< copy the entire line >>

			elif match(s,i,self.comment):
				
				#@<< copy a multi-line comment >>
				#@+node:7::<< copy a multi-line comment >>
				#@+body
				assert(self.comment_end)
				
				# Scan for the ending delimiter.
				j = i ; i += len(self.comment)
				while i < len(s) and not match(s,i,self.comment_end):
					i += 1
				if match(s,i,self.comment_end):
					i += len(self.comment_end)
				self.copy(s[j:i])
				#@-body
				#@-node:7::<< copy a multi-line comment >>

			elif match(s,i,self.comment2):
				
				#@<< copy an alternate multi-line comment >>
				#@+node:8::<< copy an alternate multi-line comment >>
				#@+body
				assert(self.comment2_end)
				j = i
				# Scan for the ending delimiter.
				i += len(self.comment2)
				while i < len(s) and not match(s,i,self.comment2_end):
					i += 1
				if match(s,i,self.comment2_end):
					i += len(self.comment2)
				self.copy(s[j:i])
				#@-body
				#@-node:8::<< copy an alternate multi-line comment >>

			elif match(s,i,self.string1) or match(s,i,self.string2):
				
				#@<< copy a string >>
				#@+node:6::<< copy a string >>
				#@+body
				j = i
				if self.language == pascal_language:
					i = skip_pascal_string(s,i)
				else:
					i = skip_string(s,i)
				self.copy(s[j:i])
				#@-body
				#@-node:6::<< copy a string >>

			else:
				self.copy(ch) ; i += 1
		
		#@<< end all open sections >>
		#@+node:9::<< end all open sections >>
		#@+body
		dn= None
		while len(self.def_stack) > 0:
			dn = self.def_stack.pop()
			if len(self.def_stack) > 0:
				self.error("Unterminated section: " + dn.name)
		if dn:
			# Terminate the root setcion.
			i = len(s)
			if dn.code and len(dn.code) > 0:
				self.ust_enter(dn.name,dn.part,dn.of,dn.code,dn.nl_flag,true) # is_root_flag
			else:
				self.error("Missing root part")
		else:
			self.error("Missing root section")
		#@-body
		#@-node:9::<< end all open sections >>
	#@-body
	#@-node:5::scan_derived_file (pass 1)
	#@+node:6::update_def (pass 2)
	#@+body
	#@+at
	#  This function handles the actual updating of section definitions in the 
	# web.  Only code parts are updated, never doc parts.
	# 
	# During pass 2 of Untangle, skip_body() calls this routine when it 
	# discovers the definition of a section in the outline.  We look up the 
	# name in the ust. If an entry exists, we compare the code (the code part 
	# of an outline node) with the code part in the ust. We update the code 
	# part if necessary.
	# 
	# We use the forgiving_compare() to compare code parts. It's not possible 
	# to change only trivial whitespace using Untangle because 
	# forgiving_compare() ignores trivial whitespace.

	#@-at
	#@@c

	# Major change: 2/23/01: Untangle never updates doc parts.
	
	def update_def (self,name,part_number,head,code,tail,is_root_flag): # Doc parts are never updated!
	
		# trace(`name` + ":" + `part_number` + ":" + `code`)
		v = self.v ; body = v.bodyString()
		if not head: head = ""
		if not tail: tail = ""
		if not code: code = ""
		false_ret = head + code + tail, len(head) + len(code), false
		part, found = self.ust_lookup(name,part_number,is_root_flag,true) # Set update
		if not found:
			return false_ret  # Not an error.
		ucode = part.code
		
		#@<< Remove leading blank lines and comments from ucode >>
		#@+node:1::<< Remove leading blank lines and comments from ucode >>
		#@+body
		#@+at
		#  We assume that any leading comments came from an @doc part.  This 
		# isn't always valid and this code will eliminate such leading 
		# comments.  This is a defect in Untangle; it can hardly be avoided.

		#@-at
		#@@c

		i = skip_blank_lines(ucode,0)
		j = skip_ws(ucode,i)
		# trace("comment,end,single:"+`self.comment`+":"+`self.comment_end`+":"+`self.line_comment`)
		
		if self.comment and self.comment_end:
			if ucode and match(ucode,j,self.comment):
				# Skip to the end of the block comment.
				i = j + len(self.comment)
				i = string.find(ucode,self.comment_end,i)
				if i == -1: ucode = None # An unreported problem in the user code.
				else:
					i += len(self.comment_end)
					i = skip_blank_lines(ucode,i)
		elif self.line_comment:
			while ucode and match(ucode,j,self.line_comment):
				i = skip_line(ucode,i)
				i = skip_blank_lines(ucode,i)
				j = skip_ws(ucode,i)
		# Only the value of ucode matters here.
		if ucode: ucode = ucode[i:]
		#@-body
		#@-node:1::<< Remove leading blank lines and comments from ucode >>

		# trace(`ucode`)
		if not ucode or len(ucode) == 0:
			return false_ret # Not an error.
		if code and self.forgiving_compare(name,part,code,ucode):
			return false_ret # Not an error.
		# Update the body.
		es("***Updating: " + v.headString())
		i = skip_blank_lines(ucode,0)
		ucode = ucode[i:]
		ucode = string.rstrip(ucode)
		# Add the trailing whitespace of code to ucode.
		code2 = string.rstrip(code)
		trail_ws = code[len(code2):]
		ucode = ucode + trail_ws
		body = head + ucode + tail
		self.update_current_vnode(body)
		if 0:
			trace("head:" + `head`)
			trace("ucode:" + `ucode`)
			trace("tail:" + `tail`)
		return body, len(head) + len(ucode),true
	
	#@-body
	#@-node:6::update_def (pass 2)
	#@+node:7::update_current_vnode
	#@+body
	#@+at
	#  This function is called from within the Untangle logic to update the 
	# body text of self.v.

	#@-at
	#@@c

	def update_current_vnode (self,s):
	
		c = self.commands ; v = self.v
		assert(self.v)
		v.setBodyStringOrPane(s)
	
		c.beginUpdate()
		c.setChanged(true)
		v.setDirty()
		v.setMarked()
		c.endUpdate()
	#@-body
	#@-node:7::update_current_vnode
	#@-node:7::untangle
	#@+node:8::utility methods
	#@+body
	#@+at
	#  These utilities deal with tangle ivars, so they should be methods.

	#@-at
	#@-body
	#@+node:1::compare_section_names
	#@+body
	# Compares section names or root names.
	# Arbitrary text may follow the section name on the same line.
	
	def compare_section_names (self,s1,s2):
	
		# trace(`get_line(s1,0)` + ":" + `get_line(s2,0)`)
		if match(s1,0,"<<") or match(s1,0,"@<"):
			# Use a forgiving compare of the two section names.
			delim = choose(self.use_cweb_flag,"@>",">>")
			i1 = i2 = 0
			while i1 < len(s1) and i2 < len(s2):
				ch1 = s1[i1] ; ch2 = s2[i2]
				if is_ws(ch1) and is_ws(ch2):
					i1 = skip_ws(s1,i1)
					i2 = skip_ws(s2,i2)
				elif match(s1,i1,delim) and match(s2,i2,delim):
					return true
				elif string.lower(ch1) == string.lower(ch2):
					i1 += 1 ; i2 += 1
				else: return false
			return false
		else: # A root name.
			return s1 == s2
	#@-body
	#@-node:1::compare_section_names
	#@+node:2::copy
	#@+body
	def copy (self, s):
	
		assert(len(self.def_stack) > 0)
		dn = self.def_stack[-1] # Add the code at the top of the stack.
		dn.code += s
	#@-body
	#@-node:2::copy
	#@+node:3::error, pathError, warning
	#@+body
	def error (self,s):
		self.errors += 1
		es(s)
		
	def pathError (self,s):
		if not self.path_warning_given:
			self.path_warning_given = true
			self.error(s)
		
	def warning (self,s):
		es(s)
	
	#@-body
	#@-node:3::error, pathError, warning
	#@+node:4::is_end_of_directive
	#@+body
	# This function returns true if we are at the end of preprocessor directive.
	
	def is_end_of_directive (self,s,i):
	
		return is_nl(s,i) and not self.is_escaped(s,i)
	#@-body
	#@-node:4::is_end_of_directive
	#@+node:5::is_end_of_string
	#@+body
	def is_end_of_string (self,s,i,delim):
	
		return i < len(s) and s[i] == delim and not self.is_escaped(s,i)
	#@-body
	#@-node:5::is_end_of_string
	#@+node:6::is_escaped
	#@+body
	# This function returns true if the s[i] is preceded by an odd number of back slashes.
	
	def is_escaped (self,s,i):
	
		back_slashes = 0 ; i -= 1
		while i >= 0 and s[i] == '\\':
			back_slashes += 1
			i -= 1
		return (back_slashes & 1) == 1
	
	#@-body
	#@-node:6::is_escaped
	#@+node:7::is_section_name
	#@+body
	def is_section_name(self,s,i):
	
		kind = bad_section_name ; end = -1
	
		if self.use_cweb_flag :
			if match(s,i,"@<"):
				i, kind, end = self.skip_cweb_section_name(s,i)
		elif match(s,i,"<<"):
			i, kind, end = self.skip_noweb_section_name(s,i)
	
		# trace(`kind` + ":" + `get_line(s,end)`)
		return i, kind, end
	#@-body
	#@-node:7::is_section_name
	#@+node:8::is_sentinel_line & is_sentinel_line_with_data
	#@+body
	#@+at
	#  This function returns true if i points to a line a sentinel line of one 
	# of the following forms:
	# 
	# start_sentinel <<section name>> end_sentinel
	# start_sentinel <<section name>> (n of m) end_sentinel
	# start_sentinel -- end -- <<section name>> end_sentinel
	# start_sentinel -- end -- <<section name>> (n of m) end_sentinel
	# 
	# start_sentinel: the string that signals the start of sentinel lines\
	# end_sentinel:   the string that signals the endof sentinel lines.
	# 
	# end_sentinel may be None,indicating that sentinel lines end with a newline.
	# 
	# Any of these forms may end with (!newline), indicating that the section 
	# reference was not followed by a newline in the orignal text.  We set 
	# nl_flag to false if such a string is seen. The name argument contains 
	# the section name.
	# 
	# The valid values of kind param are:
	# 
	# non_sentinel_line,   # not a sentinel line.
	# start_sentinel_line, #   /// <section name> or /// <section name>(n of m)
	# end_sentinel_line  //  /// -- end -- <section name> or /// -- end -- 
	# <section name>(n of m).

	#@-at
	#@@c
	def is_sentinel_line (self,s,i):
	
		result,i,kind,name,part,of,end,nl_flag = self.is_sentinel_line_with_data(s,i)
		return result
	
	def is_sentinel_line_with_data (self,s,i):
	
		start_sentinel = self.sentinel
		end_sentinel = self.sentinel_end
		
		#@<< Initialize the return values >>
		#@+node:1::<< Initialize the return values  >>
		#@+body
		name = end = None
		part = of = 1
		kind = non_sentinel_line
		nl_flag = true
		false_data = (false,i,kind,name,part,of,end,nl_flag)
		
		#@-body
		#@-node:1::<< Initialize the return values  >>

		
		#@<< Make sure the line starts with start_sentinel >>
		#@+node:2::<< Make sure the line starts with start_sentinel >>
		#@+body
		if is_nl(s,i): i = skip_nl(s,i)
		i = skip_ws(s,i)
		
		# 4/18/00: We now require an exact match of the sentinel.
		if match(s,i,start_sentinel):
			i += len(start_sentinel)
		else:
			return false_data
		#@-body
		#@-node:2::<< Make sure the line starts with start_sentinel >>

		
		#@<< Set end_flag if we have -- end -- >>
		#@+node:3::<< Set end_flag if we have -- end -- >>
		#@+body
		# If i points to "-- end --", this code skips it and sets end_flag.
		
		end_flag = false
		i = skip_ws(s,i)
		if match(s,i,"--"):
			while i < len(s) and s[i] == '-':
				i += 1
			i = skip_ws(s,i)
			if not match(s,i,"end"):
				return false_data # Not a valid sentinel line.
			i += 3 ; i = skip_ws(s,i)
			if not match(s,i,"--"):
				return false_data # Not a valid sentinel line.
			while i < len(s) and s[i] == '-':
				i += 1
			end_flag = true
		#@-body
		#@-node:3::<< Set end_flag if we have -- end -- >>

		
		#@<< Make sure we have a section reference >>
		#@+node:4::<< Make sure we have a section reference >>
		#@+body
		i = skip_ws(s,i)
		
		if (self.use_noweb_flag and match(s,i,"<<") or
			self.use_cweb_flag  and match(s,i,"@<") ):
		
			j = i ; i, kind, end = self.skip_section_name(s,i)
			if kind != section_ref:
				return false_data
			name = s[j:i]
		else:
			return false_data
		#@-body
		#@-node:4::<< Make sure we have a section reference >>

		
		#@<< Set part and of if they exist >>
		#@+node:5::<< Set part and of if they exist >>
		#@+body
		# This code handles (m of n), if it exists.
		i = skip_ws(s,i)
		if match(s,i,'('):
			j = i
			i += 1 ; i = skip_ws(s,i)
			i, part = self.scan_short_val(s,i)
			if part == -1:
				i = j # back out of the scanning for the number.
				part = 1
			else:
				i = skip_ws(s,i)
				if not match(s,i,"of"):
					return false_data
				i += 2 ; i = skip_ws(s,i)
				i, of = self.scan_short_val(s,i)
				if of == -1:
					return false_data
				i = skip_ws(s,i)
				if match(s,i,')'):
					i += 1 # Skip the paren and do _not_ return.
				else:
					return false_data
		#@-body
		#@-node:5::<< Set part and of if they exist >>

		
		#@<< Set nl_flag to false if !newline exists >>
		#@+node:6::<< Set nl_flag to false if !newline exists >>
		#@+body
		line = "(!newline)"
		i = skip_ws(s,i)
		if match(s,i,line):
			i += len(line)
			nl_flag = false
		
		#@-body
		#@-node:6::<< Set nl_flag to false if !newline exists >>

		
		#@<< Make sure the line ends with end_sentinel >>
		#@+node:7::<< Make sure the line ends with end_sentinel >>
		#@+body
		i = skip_ws(s,i)
		if end_sentinel:
			# Make sure the line ends with the end sentinel.
			if match(s,i,end_sentinel):
				i += len(end_sentinel)
			else:
				return false_data
		
		end = i # Show the start of the whitespace.
		i = skip_ws(s,i)
		if i < len(s) and not is_nl(s,i):
			return false_data
		#@-body
		#@-node:7::<< Make sure the line ends with end_sentinel >>

		kind = choose(end_flag,end_sentinel_line,start_sentinel_line)
		return true,i,kind,name,part,of,end,nl_flag
	#@-body
	#@-node:8::is_sentinel_line & is_sentinel_line_with_data
	#@+node:9::push_new_def_node
	#@+body
	# This function pushes a new def_node on the top of the section stack.
	
	def push_new_def_node (self,name,indent,part,of,nl_flag):
			
		# trace(`name` + ":" + `part`)
		node = def_node(name,indent,part,of,nl_flag,None)
		self.def_stack.append(node)
	#@-body
	#@-node:9::push_new_def_node
	#@+node:10::scan_short_val
	#@+body
	# This function scans a positive integer.
	# returns (i,val), where val == -1 if there is an error.
	
	def scan_short_val (self,s,i):
	
		if i >= len(s) or s[i] not in string.digits:
			return i, -1
	
		j = i
		while i < len(s) and s[i] in string.digits:
			i += 1
	
		val = int(s[j:i])
		# trace(s[j:i] + ":" + `val`)
		return i, val
	#@-body
	#@-node:10::scan_short_val
	#@+node:11::setRootFromHeadline
	#@+body
	def setRootFromHeadline (self,v):
	
		# trace(`v`)
		s = v.headString()
	
		if s[0:5] == "@root":
			i = skip_ws(s,5)
			if i < len(s): # Non-empty file name.
				# self.root_name must be set later by token_type().
				self.root = s
	#@-body
	#@-node:11::setRootFromHeadline
	#@+node:12::setRootFromText
	#@+body
	#@+at
	#  This code skips the file name used in @root directives.  i points after 
	# the @root directive.
	# 
	# File names may be enclosed in < and > characters, or in double quotes.  
	# If a file name is not enclosed be these delimiters it continues until 
	# the next newline.

	#@-at
	#@@c
	def setRootFromText(self,s,err_flag):
		
		# trace(`s`)
		self.root_name = None
		i = skip_ws(s,0)
		if i >= len(s): return i
		# Allow <> or "" as delimiters, or a bare file name.
		if s[i] == '"':
			i += 1 ; delim = '"'
		elif s[i] == '<':
			i += 1 ; delim = '>'
		else: delim = body_newline
	
		root1 = i # The name does not include the delimiter.
		while i < len(s) and s[i] != delim and not is_nl(s,i):
			i += 1
		root2 = i
	
		if delim != body_newline and not match(s,i,delim):
			if err_flag:
				scanError("bad filename in @root " + s[:i])
		else:
			self.root_name = string.strip(s[root1:root2])
		return i
	#@-body
	#@-node:12::setRootFromText
	#@+node:13::skip_CWEB_section_name
	#@+body
	#@+at
	#  This function skips past a section name that starts with @< and ends 
	# with @>. This code also skips any = following the section name.
	# 
	# Returns (i, kind, end), where kind is:
	# 
	# 	bad_section_name:  @ < with no matching @ >
	# 	section_ref: @ < name @ >
	# 	section_def: @ < name @ > =
	# 
	# Unlike noweb, bad section names generate errors.

	#@-at
	#@@c

	def skip_cweb_section_name(self,s,i):
		
		j = i # Used for error message.
		kind = bad_section_name ; end = -1
		runon = false ; empty_name = true
		assert(s[i:i+2]=="@<")
		i += 2
		while i < len(s):
			if match(s,i,"@>="):
				i += 3 ; end = i-1 ; kind = section_def ; break
			elif match(s,i,"@>"):
				i += 2 ; end = i ; kind = section_ref ; break
			elif match(s,i,"@<"):
				runon = true ; break
			elif match(s,i,"@@"): i += 2
			elif is_ws_or_nl(s,i): i += 1
			else:
				i += 1 ; empty_name = false
	
		if empty_name:
			scanError("empty CWEB section name: " + s[j:i])
			return i, bad_section_name, -1
		elif i >= len(s) or runon:
			scanError("Run on CWEB section name: " + s[j:i])
			return i, bad_section_name, -1
		else:
			return i, kind, end
	#@-body
	#@-node:13::skip_CWEB_section_name
	#@+node:14::skip_noweb_section_name
	#@+body
	#@+at
	#  This function skips past a section name that starts with < < and might 
	# end with > > or > > =. The entire section name must appear on the same line.
	# 
	# Note: this code no longer supports extended noweb mode.
	# 
	# Returns (i, kind, end),
	# 	end indicates the end of the section name itself (not counting the =).
	# 	kind is one of:
	# 		bad_section_name: "no matching ">>" or ">>"  This is _not_ a user error!
	# 		section_ref: < < name > >
	# 		section_def: < < name > > =
	# 		at_root:     < < * > > =

	#@-at
	#@@c
	def skip_noweb_section_name(self,s,i):
		
		assert(match(s,i,"<<"))
		i += 2
		j = i # Return this value if no section name found.
		kind = bad_section_name ; end = -1 ; empty_name = true
	
		# Scan for the end of the section name.
		while i < len(s) and not is_nl(s,i):
			if match(s,i,">>="):
				i += 3 ; end = i - 1 ; kind = section_def ; break
			elif match(s,i,">>"):
				i += 2 ; end = i ; kind = section_ref ; break
			elif is_ws_or_nl(s,i):
				i += 1
			elif empty_name and s[i] == '*':
				empty_name = false
				i = skip_ws(s,i+1) # skip the '*'
				if match(s,i,">>="):
					i += 3 ; end = i - 1 ; kind = at_root ; break
			else:
				i += 1 ; empty_name = false
	
		if empty_name:
			kind = bad_section_name
		if kind == bad_section_name:
			i = j
		return i, kind, end
	#@-body
	#@-node:14::skip_noweb_section_name
	#@+node:15::skip_section_name
	#@+body
	# Returns a tuple (i, kind, end)
	
	def skip_section_name(self,s,i):
	
		if self.use_noweb_flag:
			return self.skip_noweb_section_name(s,i)
		else:
			return self.skip_cweb_section_name(s,i)
	#@-body
	#@-node:15::skip_section_name
	#@+node:16::standardize_name
	#@+body
	#@+at
	#  This code removes leading and trailing brackets, converts white space 
	# to a single blank and converts to lower case.

	#@-at
	#@@c

	def standardize_name (self,name):
	
		# Convert to lowercase.
		name = string.lower(name)
		# Convert whitespace to a single space.
		name = string.replace(name,'\t',' ')
		name = string.replace(name,'  ',' ')
		# Remove leading '<'
		i = 0 ; n = len(name)
		while i < n and name[i] == '<':
			i += 1
		j = i
		# Find the first '>'
		while i < n and name [i] != '>':
			i += 1
		name = string.strip(name[j:i])
		# trace(`name`)
		return name
	#@-body
	#@-node:16::standardize_name
	#@+node:17::tangle.scanAllDirectives
	#@+body
	#@+at
	#  This code scans the node v and all its ancestors looking for 
	# directives.  If found,the corresponding globals are set for use by 
	# Tangle, Untangle and syntax coloring.
	# 
	# Once a directive is seen, related directives in ancesors have no 
	# effect.  For example, if an @color directive is seen in node x, no 
	# @color or @nocolor directives are examined in any ancestor of x.

	#@-at
	#@@c

	def scanAllDirectives(self,v,require_path_flag,issue_error_flag):
	
		c = self.commands ; config = app().config
		# trace(`v`)
		old_bits = 0 # One bit for each directive.
		self.init_directive_ivars()
		# Stephen P. Schaefer 9/13/2002
		# Add support for @first
		# Unlike other root attributes, does *NOT* inherit
		# from parent nodes
		if v:
			s = v.bodyString()
			
			#@<< Collect @first attributes >>
			#@+node:1::<< Collect @first attributes >>
			#@+body
			# Stephen P. Schaefer 9/13/2002
			tag = "@first"
			i = 0
			while 1:
				j = string.find(s,tag,i)
				if j >= 0:
					i = j + len(tag)
					j = i = skip_ws(s,i)
					i = skip_to_end_of_line(s,i)
					if i>j:
						self.first_lines += s[j:i] + '\n'
					i = skip_nl(s,i)
				else:
					break
			
			
			#@-body
			#@-node:1::<< Collect @first attributes >>

		while v:
			s = v.bodyString()
			bits, dict = is_special_bits(s)
			# trace("bits:" + `bits` + ", dict:" + `dict`, ", " + `v`)
			
			#@<< Test for @comment or @language >>
			#@+node:2::<< Test for @comment or @language >>
			#@+body
			if btest(old_bits,comment_bits)or btest(old_bits,language_bits):
				 pass # Do nothing more.
				 
			elif btest(bits,comment_bits):
				i = dict["comment"]
				# self.set_root_delims(s[i:])
				(delim1,delim2,delim3) = set_delims_from_string(s[i:])
				if delim1 or delim2:
					self.single_comment_string = delim1
					self.start_comment_string = delim2
					self.end_comment_string = delim3
					# @comment effectively disables Untangle.
					self.language = unknown_language
				else:
					if issue_error_flag:
						es("ignoring: " + s[i:])
			
			elif btest(bits,language_bits):
				issue_error_flag = false
				i = dict["language"]
				language,delim1,delim2,delim3 = set_language(s,i,issue_error_flag)
				self.language = language
				# 8/1/02: Now works as expected.
				self.single_comment_string = delim1
				self.start_comment_string = delim2
				self.end_comment_string = delim3
				if 0:
					trace(`self.single_comment_string` + "," +
					`self.start_comment_string` + "," +
					`self.end_comment_string`)
			#@-body
			#@-node:2::<< Test for @comment or @language >>

			
			#@<< Test for @verbose,@terse or @silent >>
			#@+node:3::<< Test for @verbose, @terse or @silent >>
			#@+body
			#@+at
			#  It is valid to have more than one of these directives in the 
			# same body text: the more verbose directive takes precedence.

			#@-at
			#@@c

			if btest(old_bits,verbose_bits)or btest(old_bits,terse_bits)or btest(old_bits,silent_bits):
				pass # Do nothing more.
			elif btest(bits,verbose_bits):
				self.print_bits = verbose_bits
			elif btest(bits,terse_bits):
				self.print_bits = terse_bits
			elif btest(bits,silent_bits):
				self.print_bits = silent_bits
			
			#@-body
			#@-node:3::<< Test for @verbose, @terse or @silent >>

			
			#@<< Test for @path >>
			#@+node:4::<< Test for @path >>
			#@+body
			if require_path_flag and btest(bits,path_bits)and not btest(old_bits,path_bits):
			
				k = dict["path"]
				
				#@<< compute path from s[k:] >>
				#@+node:1::<< compute path from s[k:] >>
				#@+body
				j = i = k + len("@path")
				i = skip_to_end_of_line(s,i)
				path = string.strip(s[j:i])
				
				# Remove leading and trailing delims if they exist.
				if len(path) > 2 and (
					(path[0]=='<' and path[-1] == '>') or
					(path[0]=='"' and path[-1] == '"') ):
					path = path[1:-1]
				
				path = string.strip(path)
				path = os.path.join(app().loadDir,path) # EKR: 9/5/02
				# trace("path: " + path)
				#@-body
				#@-node:1::<< compute path from s[k:] >>

				dir = path
				if len(dir) > 0:
					base = getBaseDirectory() # returns "" on error.
					if dir and len(dir) > 0:
						dir = os.path.join(base,dir)
						if os.path.isabs(dir):
							
							#@<< handle absolute @path >>
							#@+node:2::<< handle absolute @path >>
							#@+body
							if os.path.exists(dir):
								self.tangle_directory = dir
							else: # 9/25/02
								config = app().config
								if config.path_directive_creates_directories:
									try:
										os.mkdir(dir)
										es("creating @path directory:" + dir)
										self.default_directory = dir
										break
									except:
										self.error("can not create @path directory: " + dir)
										traceback.print_exc()
								elif issue_error_flag and not self.path_warning_given:
									self.path_warning_given = true # supress future warnings
									self.error("invalid directory: " + '"' + s[i:j] + '"')
							#@-body
							#@-node:2::<< handle absolute @path >>

						elif issue_error_flag and not self.path_warning_given:
							self.path_warning_given = true # supress future warnings
							self.error("ignoring relative path:" + dir)
				elif issue_error_flag and not self.path_warning_given:
					self.path_warning_given = true # supress future warnings
					self.error("ignoring empty @path")
			
			#@-body
			#@-node:4::<< Test for @path >>

			
			#@<< Test for @pagewidth and @tabwidth >>
			#@+node:5::<< Test for @pagewidth and @tabwidth >>
			#@+body
			if btest(bits,page_width_bits) and not btest(old_bits,page_width_bits):
				i = dict["page_width"] # 7/18/02 (!)
				i, val = skip_long(s,i+10) # Point past @pagewidth
				if val != None and val > 0:
					self.page_width = val
				else:
					if issue_error_flag:
						j = skip_to_end_of_line(s,i)
						es("ignoring " + s[i:j])
			
			if btest(bits,tab_width_bits)and not btest(old_bits,tab_width_bits):
				i = dict["tab_width"] # 7/18/02 (!)
				i, val = skip_long(s,i+9) # Point past @tabwidth.
				if val != None and val != 0:
					self.tab_width = val
				else:
					if issue_error_flag:
						j = skip_to_end_of_line(s,i)
						es("ignoring " + s[i:j])
			
			#@-body
			#@-node:5::<< Test for @pagewidth and @tabwidth >>

			
			#@<< Test for @header or @noheader >>
			#@+node:6::<< Test for @header or @noheader >>
			#@+body
			if btest(old_bits,header_bits)or btest(old_bits,noheader_bits):
				pass # Do nothing more.
			elif btest(bits,header_bits)and btest(bits,noheader_bits):
				if issue_error_flag:
					es("conflicting @header and @noheader directives")
			elif btest(bits,header_bits):
				self.use_header_flag = true
			elif btest(bits,noheader_bits):
				self.use_header_flag = false
			
			#@-body
			#@-node:6::<< Test for @header or @noheader >>

			old_bits |= bits
			v = v.parent()
		
		#@<< Set self.tangle_directory >>
		#@+node:7::<< Set self.tangle_directory >>
		#@+body
		#@+at
		#  This code sets self.tangle_directory if it has not already been set 
		# by an @path directive.
		# 
		# An absolute file name in an @root directive will override the 
		# directory set here.
		# A relative file name gets appended later to the default directory.
		# That is, the final file name will be os.path.join(self.tangle_directory,fileName)

		#@-at
		#@@c

		if c.frame and require_path_flag and not self.tangle_directory:
		
			if self.root_name and len(self.root_name) > 0:
				root_dir = os.path.dirname(self.root_name)
			else:
				root_dir = None
			table = ( # This is a precedence table.
				(root_dir,"@root"), 
				(c.tangle_directory,"default tangle"), # Probably should be eliminated.
				(c.frame.openDirectory,"open"))
			base = getBaseDirectory() # returns "" on error.
			for dir, kind in table:
				if dir and len(dir) > 0:
					dir = os.path.join(base,dir)
					if os.path.isabs(dir): # Errors may result in relative or invalid path.
						
						#@<< handle absolute path >>
						#@+node:1::<< handle absolute path >>
						#@+body
						if os.path.exists(dir):
							self.tangle_directory = dir ; break
						else: # 9/25/02
							config = app().config
							if config.path_directive_creates_directories:
								try:
									os.mkdir(dir)
									es("creating @root directory:" + dir)
									self.default_directory = dir ; break
								except:
									self.error("can not create @root directory: " + dir)
									traceback.print_exc()
							elif issue_error_flag:
								self.warning("ignoring invalid " + kind + " directory: " + dir)
						#@-body
						#@-node:1::<< handle absolute path >>

		
		if not self.tangle_directory and issue_error_flag:
			self.pathError("No directory specified by @root, @path or Preferences.")
		#@-body
		#@-node:7::<< Set self.tangle_directory >>
	#@-body
	#@-node:17::tangle.scanAllDirectives
	#@+node:18::token_type
	#@+body
	#@+at
	#  This method returns a code indicating the apparent kind of token at the 
	# position i. The caller must determine whether section definiton tokens 
	# are valid.
	# 
	# returns (kind, end) and sets global root_name using setRootFromText().

	#@-at
	#@@c

	def token_type(self,s,i,err_flag):
	
		kind = plain_line ; end = -1
		if self.use_noweb_flag:
			
			#@<< set token_type in noweb mode >>
			#@+node:1::<< set token_type in noweb mode >>
			#@+body
			if match(s,i,"<<"):
				i, kind, end = self.skip_section_name(s,i)
				if kind == bad_section_name:
					kind = plain_line # not an error.
				elif kind == at_root:
					if self.head_root:
						self.setRootFromText(self.head_root,err_flag)
					else:
						kind = bad_section_name # The warning has been given.
			elif match(s,i,"@ ") or match(s,i,"@\t") or match(s,i,"@\n"): kind = at_doc
			elif match(s,i,"@@"): kind = at_at
			elif i < len(s) and s[i] == '@': kind = at_other
			else: kind = plain_line
			#@-body
			#@-node:1::<< set token_type in noweb mode >>

		else:
			
			#@<< set token_type for CWEB mode >>
			#@+node:2::<< set token_type for CWEB mode >>
			#@+body
			i = skip_ws(s,i)
			if match(s,i,"@*") or match(s,i,"@ "): kind = at_doc
			elif match(s,i,"@<"): i, kind, end = self.skip_section_name(s,i)
			elif match(s,i,"@@"): kind = at_at
			elif match_word(s,i,"@c") or match_word(s,i,"@p"): kind = at_code
			elif i < len(s) and s[i] == '@':
				if   i + 1 >= len(s): kind = at_doc
				elif i + 1 < len(s) and s[i+1] not in string.letters:
					kind = at_web
				else: kind = at_other # Set kind later
			else: kind = plain_line
			#@-body
			#@-node:2::<< set token_type for CWEB mode >>

		if kind == at_other :
			
			#@<< set kind for directive >>
			#@+node:3::<< set kind for directive >>
			#@+body
			# This code will return at_other for any directive other than those listed.
			
			for name, type in [ ("@chapter", at_chapter),
				("@c", at_code), # 2/28/02: treat @c just like @code.
				("@code", at_code), ("@doc", at_doc),
				("@root", at_root), ("@section", at_section) ]:
				if match_word(s,i,name):
					kind = type ; break
			
			if kind == at_root:
				i = self.setRootFromText(s[i+5:],err_flag)
			#@-body
			#@-node:3::<< set kind for directive >>

		# trace(`kind` + ":" + `get_line(s,i)`)
		return kind, end
	#@-body
	#@-node:18::token_type
	#@-node:8::utility methods
	#@-others
#@-body
#@-node:4::class tangleCommands methods
#@-others
#@-body
#@-node:0::@file leoTangle.py
#@-leo
