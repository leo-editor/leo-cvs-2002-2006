#@+leo

#@+node:0::@file leoTangle.py

#@+body
# Tangle and Untangle.

from leoGlobals import *
from leoUtils import *
import os,string


#@<< constants & synonyms >>

#@+node:1::<< constants & synonyms >>

#@+body
# Constants
max_errors = 20

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


#@-body

#@-node:1::<< constants & synonyms >>



#@<< define node classes >>

#@+node:2::<< define node classes >>

#@+body
class tst_node:
	
#@<< tst_node methods >>

	#@+node:1::<< tst_node methods >>

	#@+body

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

	#@-node:1::<< tst_node methods >>

	
class part_node:
	
#@<< part_node methods >>

	#@+node:2::<< part_node methods >>

	#@+body

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

	#@-node:2::<< part_node methods >>


class ust_node:
	
#@<< ust_node methods >>

	#@+node:3::<< ust_node methods >>

	#@+body

	#@+others

	#@+node:1::ust_node.__init__

	#@+body

	#@+at
	#  The text has been masssaged so that 1) it contains no leading indentation and 2) all code arising from section references 
	# have been replaced by the reference line itself.  Text for all copies of the same part can differ only in non-critical white space.

	#@-at

	#@@c
	
	def __init__ (self,name,text,part,of,nl_flag,update_flag):
	
		trace("ust_node.__init__" + `name`)
		self.name = name # section name
		self.parts = [] # part list
		self.text = text # part text
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

	#@-node:3::<< ust_node methods >>

#@-body

#@-node:2::<< define node classes >>


class tangleCommands:
	
#@<< tangleCommands methods >>

	#@+node:3::<< tangleCommands methods >>

	#@+body

	#@+others

	#@+node:1::tangle.__init__

	#@+body
	def __init__ (self,commands):
	
		self.commands = commands
		self.init_ivars()
	#@-body

	#@-node:1::tangle.__init__

	#@+node:2:C=1:tangle.init_ivars & init_directive_ivars

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
		#  Symbol tables: the TST (Tangle Symbol Table) contains all section names in the outline. The UST (Untangle Symbol Table) 
		# contains all sections defined in the derived file.

		#@-at

		#@@c
		self.tst = {}
		self.ust = {}
		
		# The section stack for Tangle and the definition stack for Untangle.
		self.section_stack = []
		self.def_stack = []
		

		#@+at
		#  The list of all roots. The symbol table routines add roots to self list during pass 1. Pass 2 uses self list to 
		# generate code for all roots.

		#@-at

		#@@c
		self.root_list = []
		
		# The delimiters for comments created by the @comment directive.
		self.single_comment_string = "//"  # present comment delimiters.
		self.start_comment_string = "/*"
		self.end_comment_string = "*/"
		
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
		#  The following records whether we have seen an @code directive in a body text.
		# If so, an @code represents < < header name > > = and it is valid to continue a section definition.

		#@-at

		#@@c
		self.code_seen = false # true if @code seen in body text.
		#@-body

		#@-node:1::<< init tangle ivars >>

		
	# Called by scanAllDirectives
	
	def init_directive_ivars (self):
	
		c = self.commands
		
	#@<< init directive ivars >>

		#@+node:2::<< init directive ivars >>

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
		(	self.single_comment_string,
			self.start_comment_string,
			self.end_comment_string ) = set_delims_from_language(self.language)
		
		# Abbreviations for self.language
		self.use_cweb_flag = self.language == cweb_language
		self.use_noweb_flag = not self.use_cweb_flag
		
		# Set only from directives.
		self.print_bits = verbose_bits
		#@-body

		#@-node:2::<< init directive ivars >>

	#@-body

	#@-node:2:C=1:tangle.init_ivars & init_directive_ivars

	#@+node:3::top level

	#@+body

	#@+at
	#  Only top-level drivers initialize ivars.

	#@-at

	#@-body

	#@+node:1:C=2:cleanup

	#@+body
	# This code is called from tangleTree and untangleTree.
	
	def cleanup(self):
	
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
				except: es("Can not execute tangle_done.run()")
			if not self.tangling and self.untangle_batch_flag:
				try:
					import untangle_done
					untangle_done.run(root_names)
				except: es("Can not execute tangle_done.run()")
	
		# Reinitialize the symbol tables and lists.
		self.tst = {}
		self.ust = {}
		self.root_list = []
		self.def_stack = []
	#@-body

	#@-node:1:C=2:cleanup

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
	def initUnangleCommand (self):
	
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
	#@-body

	#@-node:4::tangle

	#@+node:5:C=3:tangleAll

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
	#@-body

	#@-node:5:C=3:tangleAll

	#@+node:6:C=4:tangleMarked

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
	#@-body

	#@-node:6:C=4:tangleMarked

	#@+node:7::tanglePass1

	#@+body

	#@+at
	#  This is the main routine of pass 1. It traverses the tree whose root is given, handling each headline and associated body text.

	#@-at

	#@@c
	
	def tanglePass1(self,v):
	
		c = self.commands
		next = v.nodeAfterTree()
		
		while v and v != next:
			self.v = v
			self.set_root_from_headline(v)
			bits, dict = is_special_bits(v.bodyString(),set_root_from_headline)
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
			if not self.tangling:
				v.trimTrailingLines() # Stamp out those trailing blank lines!
			v = v.threadNext()
			if self.errors >= max_errors:
				es("----- Halting Tangle: too many errors")
				break
	
		if self.tangling:
			self.st_check()
			trace(self.st_dump(brief))
	#@-body

	#@-node:7::tanglePass1

	#@+node:8::tanglePass2

	#@+body
	# At this point v is the root of the tree that has been tangled.
	
	def tanglePass2(self,v,unitFlag):
	
		self.v = None # self.v is not valid in pass 2.
	
		if self.errors > 0:
			es("----- No file written because of errors")
		elif self.root_list == None:
			es("----- The outline contains no roots")
		else:
			self.put_all_roots() # pass 2 top level function.
	#@-body

	#@-node:8::tanglePass2

	#@+node:9:C=5:tangleTree (calls cleanup)

	#@+body

	#@+at
	#  This funtion tangles all nodes in the tree whose root is v. It reports on its results if report_flag is true.
	# 
	# This function is called only from the top level, so there is no need to initialize globals.

	#@-at

	#@@c
	
	def tangleTree(self,v,report_flag):
	
		assert(v)
		any_root_flag = false
		next = v.nodeAfterTree()
		self.path_warning_given = false
	
		while v and v != next:
			self.set_root_from_headline(v)
			bits, dict = is_special_bits(v.bodyString(),set_root_from_headline)
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
					self.tanglePass2(v,is_unit)
				self.cleanup()
				v = v.nodeAfterTree()
				if self.path_warning_given: break # Fatal error.
	
		if self.tangling and report_flag and not any_root_flag:
			# This is done by Untangle if we are untangling.
			es("----- The outline contains no roots")
		return any_root_flag
	#@-body

	#@-node:9:C=5:tangleTree (calls cleanup)

	#@+node:10::untangle

	#@+body
	def untangle(self):
	
		c = self.commands ; v = c.currentVnode()
		self.initUntangleCommand()
		
		c.beginUpdate()
		self.untangleTree(v,report_errors)
		c.endUpdate()
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
	#@-body

	#@-node:11::untangleAll

	#@+node:12::untangleMarked

	#@+body
	def untangleMarked(self):
	
		c = self.commands ; v = c.rootVnode()
		self.initUntangleCommand()
		any_root_flag = false
	
		c.beginUpdate()
		while v:
			if v.isMarked():
				ok = self.untangleTree(v,dont_report_errors)
				if ok: marked_flag = true
				if self.errors > 0: break
				v = v.nodeAfterTree()
			else: v = v.threadNext()
		c.endUpdate()
	
		if not any_root_flag:
			es("----- The outline contains no marked roots")
		elif self.errors > 0:
			es("----- Untangle command halted because of errors")
	#@-body

	#@-node:12::untangleMarked

	#@+node:13::untangleTree (calls cleanup)

	#@+body
	# This funtion is called when the user selects any "Untangle" command.
	
	def untangleTree(self,v,report_flag):
	
		es(self.__name__ + " not ready yet")
		return ##
	
		any_root_flag = false
		afterEntireTree = v.nodeAfterTree()
		# Initialize these globals here: they can't be cleared later.
		self.head_root = None
		self.errors = 0
		self.clearAllVisited()# Used by untangle code.
	
		while v and v != afterEntireTree and self.errors == 0:
			self.set_root_from_headline(v)
			bits, dict = is_special_bits(v.bodyString(),set_root_from_headline)
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
					set_root_from_headline(v)
					bits, dict = is_special_bits(v.t.bodyString,set_root_from_headline)
					root =(bits & root_bits)!= 0
					if root:
						any_root_flag = true
						end = None
						
	#@<< set end to the next root in the unit >>

						#@+node:1::<< set end to the next root in the unit >>

						#@+body

						#@+at
						#  The untangle_root function will untangle an entire tree by calling untangleTree,so the following code 
						# ensures that the next @root node will not be an offspring of v.

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

						self.scanAllDirectives(v,require_path,report_errors)
						self.untangleRoot(v,unitNode,afterUnit)
						v = end
					else: v = v.threadNext()
				self.cleanup()
			elif root:
				# Limit the range of the @root to its own tree.
				afterRoot = v.nodeAfterTree()
				any_root_flag = true
				self.scanAllDirectives(v,require_path,dont_report_errors)
				self.untangleRoot(v,v,afterRoot) # 9/27/99
				self.cleanup()
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

	#@-node:13::untangleTree (calls cleanup)

	#@+node:14::untangleRoot (uses token_type)

	#@+body

	#@+at
	#  This method untangles the derived files in a vnode known to contain at least one @root directive. The work is done in two 
	# passes. The first pass creates the UST by scanning the derived file. The second pass updates the outline using the UST and a 
	# TST that is created during the pass.
	# 
	# We assume that all sections from root to end are contained in the derived file, and we attempt to update all such sections. 
	# The begin/end params indicate the range of nodes to be scanned when building the TST.

	#@-at

	#@@c
	
	def untangleRoot(self,root,begin,end):
	
		
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

		
	#@<< Set path & root_name to the file specified in the @root directive >>

		#@+node:2::<< Set path & root_name to the file specified in the @root directive >>

		#@+body
		s = root.bodyString()
		i = 0
		while i < len(body):
			code, end = self.token_type(s,i,report_errors)
			if code == at_root:
				# token_type sets root_name unless there is a syntax error.
				if self.root_name: path = self.root_name
				break
			else: i = skip_line(s,i)
			
		if not self.root_name:
			# A bad @root command.  token_type has already given an error.
			self.tangleCleanUp()
			return
		#@-body

		#@-node:2::<< Set path & root_name to the file specified in the @root directive >>

		
	#@<< Read the file into file_buf >>

		#@+node:3::<< Read the file into file_buf  >>

		#@+body
		try:
			file_buf = file.read(path)
			file_buf = string.replace(file_buf,body_ignored_newline,'')
		except:
			es("error reading: " + path)
			self.tangleCleanUp()
			return
		#@-body

		#@-node:3::<< Read the file into file_buf  >>

		es("@root " + path)
		# Pass 1: Scan the C file, creating the UST
		scan_derived_file(file_buf)
		trace(self.ust_dump())
		if self.errors == 0:
			
	#@<< Pass 2: Untangle the outline using the UST and a newly-created TST >>

			#@+node:4::<< Pass 2:  Untangle the outline using the UST and a newly-created TST >>

			#@+body

			#@+at
			#  This code untangles the root and all its siblings. We don't call tangleTree here because we must handle all 
			# siblings.  tanglePass1 handles an entire tree.  It also handles @ignore.

			#@-at

			#@@c
			
			v = begin
			while v and v != end:
				this.tanglePass1(v)
				if self.errors != 0:
					break
				v = v.nodeAfterTree()
			
			self.ust_warn_about_orphans()
			trace(st_dump(brief))
			#@-body

			#@-node:4::<< Pass 2:  Untangle the outline using the UST and a newly-created TST >>

	#@-body

	#@-node:14::untangleRoot (uses token_type)

	#@-node:3::top level

	#@+node:4::tangle

	#@+node:1::Pass 1

	#@+node:1::handle_newline

	#@+body

	#@+at
	#  This method handles newline processing while skipping a code section. It sets 'done' if the line contains an @directive or 
	# section definition that terminates the present code section. On entry: i should point to the first character of a line.  
	# This routine scans past a line only if it could not contain a section reference.
	# 
	# Returns (i, done)

	#@-at

	#@@c
	
	def handle_newline(self,s,i):
	
		j = i ; done = false
		kind, end = self.token_type(s,i,dont_report_errors)
		# token_type will not skip whitespace in noweb mode.
		i = skip_ws(s,i)
	
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
			self.error("SWEB directive not valid here: " + s[j:i])
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
		is_dirty_flag = v.isDirty()
		code_seen = false ; code = None ; doc = None
		i, doc = self.skip_doc(s,0) # Start in doc section by default.
		if i >= len(s) and doc:
			
	#@<< Define a section containing only an @doc part >>

			#@+node:1::The interface between tangle and untangle

			#@+node:1::<< Define a section containing only an @doc part >>

			#@+body

			#@+at
			#  It's valid for an @doc directive to appear under a headline that does not contain a section name.  In that case, no 
			# section is defined.

			#@-at

			#@@c
			
			if self.header_name:
				# Original Tangle code.
				flag = choose(code_seen,allow_multiple_parts,disallow_multiple_parts)
				part = self.st_enter_section_name(self.header_name,code,doc,flag)
			
				if not self.tangling:
					s = self.update_def(s,self.header_name,part,c,code,doc,not_root_name)
			#@-body

			#@-node:1::<< Define a section containing only an @doc part >>

			#@-node:1::The interface between tangle and untangle

		while i < len(s):
			progress = i # progress indicator
			kind, end = self.token_type(s,i,report_errors)
			if is_nl(s,i): i = skip_nl(s,i)
			i = skip_ws(s,i)
			if kind == section_def:
				
	#@<< Scan and define a section definition >>

				#@+node:1::The interface between tangle and untangle

				#@+node:2::<< Scan and define a section definition >>

				#@+body

				#@+at
				#  This code skips an entire code section then enters it and any preceding doc part into the symbol table.

				#@-at

				#@@c
				
				k = i
				i, kind, end_i = self.skip_section_name(s,i)
				section_name = s[k:i]
				assert(kind == section_def)
				i = skip_to_end_of_line(s,i)
				i = skip_blank_lines(s,i)
				i, code = self.skip_code(s,i)
				# We must enter the section name even if the code part is empty.
				# Original Tangle code.
				flag = choose(kind == section_def,allow_multiple_parts,disallow_multiple_parts)
				part = self.st_enter_section_name(section_name,code,doc,flag)
						
				if not self.tangling:
					part = 0
					s = self.update_def(s,section_name,part,code,doc,not_root_name)
				# Original Tangle code,part 2.
				doc = None
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
				# All @c directives denote < < headline_name > > =
				
				i = skip_blank_lines(s,i)
				i, code = self.skip_code(s,i)
				code = string.rstrip(code)
				if self.header_name:
					# Original Tangle code.
					flag = choose(code_seen,allow_multiple_parts,disallow_multiple_parts)
					part = self.st_enter_section_name(self.header_name,code,doc,flag)
						
					if not self.tangling:
						s = self.update_def(self.header,ip2,part,s,code,doc,not_root_name)
				else:
					self.error("@c expects the header: " + header + " to contain a section name")
				code_seen = true
				doc = None
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
				i = skip_blank_lines(s,i)
				i, code = self.skip_code(s,i)
				# Original Tangle code.
				self.st_enter_root_name(old_root_name,code,doc)
				if not self.tangling:
					part = 1 # Use 1 for root part.
					s = self.update_def(s,old_root_name,part,code,doc,is_root_name)
				# Original Tangle code,part 2.
				doc = None
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
	#@-body

	#@+node:1::The interface between tangle and untangle

	#@+body

	#@+at
	#  The following subsections contain the interface between the Tangle and Untangle commands.  This interface is an important 
	# hack, and allows Untangle to avoid duplicating the logic in skip_tree and its allies.  The aha is as follows:
	# 
	# Just at the time the Tangle command would enter a section (or root) definition into the symbol table, all the information is 
	# present that Untangle needs to update that definition.
	# 
	# Only one modification had to be made to the original Tangle code: st_enter_section_name now returns the part number of the 
	# part that has just been entered.  This part is sent to update_def so it can know which part of a multiple-part definition 
	# must be updated.

	#@-at

	#@-body

	#@-node:1::The interface between tangle and untangle

	#@-node:2::skip_body

	#@+node:3::skip_code

	#@+body

	#@+at
	#  This method skips an entire code section. The caller is responsible for entering the completed section into the symbol 
	# table. On entry, i points at the line following the @directive or section definition that starts a code section. We skip 
	# code until we see the end of the body text or the next @ directive or section defintion that starts a code or doc part.

	#@-at

	#@@c
	
	def skip_code(self,s,i):
	
		# j = skip_line(s,i) ; trace(`s[i:j]`)
		code1 = i
		nl_i = i # For error messages
		done = false # TRUE when end of code part seen.
		if self.use_noweb_flag:
			
	#@<< skip a noweb code section >>

			#@+node:1::<< skip a noweb code section >>

			#@+body

			#@+at
			#  This code handles the following escape conventions: double at-sign at the start of a line and at-<< and at.>.

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
						part = self.st_enter_section_name(name,None,None,unused_parts_flag)
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
						part = self.st_enter_section_name(name,None,None,unused_parts_flag)
						i = j
					#@-body

					#@-node:1::<< handle CWEB control code >>

				else: i += 1
			#@-body

			#@-node:2::<< skip a CWEB code section >>

		return i, s[code1:i]
	#@-body

	#@-node:3::skip_code

	#@+node:4::skip_doc

	#@+body
	def skip_doc(self,s,i):
	
		# j = skip_line(s,i) ; trace(`s[i:j]`)
		# Ignore initial blank lines and @doc, @chapter and @section directives.
		doc1 = i
		while i < len(s):
			doc1 = i
			if is_nl(s,i):
				doc1 = i = skip_nl(s,i)
				continue
			kind, end = self.token_type(s,i,dont_report_errors)
			if kind == at_doc:
				if self.use_cweb_flag:
					i += 2 # Skip the at-space.
				else:
					i = skip_line(s,i)
				doc1 = i
			elif kind == at_chapter or kind == at_section:
				doc1 = i = skip_line(s,i)
			else: break
	
		while i < len(s):
			kind, end = self.token_type(s,i,dont_report_errors)
			if kind == at_code or kind == at_root or kind == section_def:
				break
			i = skip_line(s,i)
	
		return i, s[doc1:i]
	#@-body

	#@-node:4::skip_doc

	#@+node:5::skip_headline

	#@+body

	#@+at
	#  This function sets ivars that keep track of the indentation level. We also remember where the next line starts because it 
	# is assumed to be the first line of a documentation section.
	# 
	# A headline can contain a leading section name.  If it does, we substitute the section name if we see an @c directive in the 
	# body text.

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

	#@+node:1::oblank, oblanks, os, otab, otabs

	#@+body
	def oblank (self):
		self.oblanks(1)
	
	def oblanks (self,n):
		if n > 0:
			self.output_file.write(' ' * n)
			
	def onl(self):
		self.os('\n')
			
	def os (self,s):
		s = string.replace(s,body_ignored_newline,body_newline)
		self.output_file.write(s)
	
	def otab (self):
		self.otabs(1)
	
	def otabs (self,n):
		if n > 0:
			self.output_file.write('\t' * n)
	#@-body

	#@-node:1::oblank, oblanks, os, otab, otabs

	#@+node:2:C=6:tangle.put_all_roots (open)

	#@+body

	#@+at
	#  This is the top level method of the second pass. It creates a separate C file for each @root directive in the outline. As 
	# will be seen later,the file is actually written only if the new version of the file is different from the old version,or if 
	# the file did not exist previously. If changed_only_flag FLAG is true only changed roots are actually written.

	#@-at

	#@@c
	
	def put_all_roots(self):
	
		c = self.commands ; outline_name = c.frame.mFileName
	
		for section in self.root_list:
		
			trace(`section.name`)
			file_name = os.path.join(self.tangle_directory,section.name)
			file_name = os.path.normpath(file_name)
			temp_name = create_temp_name(section.name)
			if not temp_name: break
			# Set the output_file global.
			self.output_file = open(temp_name,"w")
			if not self.output_file:
				es("Can not create: " + temp_name)
				break
			if self.use_header_flag and self.print_bits == verbose_bits:
				
	#@<< Write a banner at the start of the output file >>

				#@+node:1::<<Write a banner at the start of the output file>>

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

				#@-node:1::<<Write a banner at the start of the output file>>

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

				#@+node:2::<< Erase the temporary file >>

				#@+body
				
				try: # Just delete the temp file.
					os.remove(temp_name)
				except: pass

				#@-body

				#@-node:2::<< Erase the temporary file >>

	#@-body

	#@-node:2:C=6:tangle.put_all_roots (open)

	#@+node:3::put_code

	#@+body

	#@+at
	#  This method outputs a code section, expanding section references by their definition. We should see no @directives or 
	# section definitions that would end the code section.
	# 
	# Most of the differences bewteen noweb mode and CWEB mode are handled by token_type(called from put_newline). Here, the only 
	# difference is that noweb handles double-@ signs only at the start of a line.

	#@-at

	#@@c
	
	def put_code(self,s,no_first_lws_flag):
	
		# j = skip_line(s,0) ; trace(`s[:j]`)
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
					#  The user must ensure that neither @ < < nor @ > > occurs in comments or strings. However, it is valid for @ 
					# < < or @ > > to appear in the doc chunk or in a single-line comment.

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
	
		# j = skip_line(s,0) ; trace(`s[:j]`)
		width = self.page_width
		words = 0 ; word_width = 0 ; line_width = 0
		single_w = choose(self.single_comment_string,len(self.single_comment_string),0)
		# Make sure we put at least 20 characters on a line.
		if width - max(0,self.tangle_indent) < 20:
			width = max(0,self.tangle_indent) + 20
		# Skip Initial white space in the doc part.
		i = skip_ws_and_nl(s,0)
		if i < len(s) and self.print_bits == verbose_bits:
			use_block_comment = self.start_comment_string and self.end_comment_string
			use_single_comment = not use_block_comment and self.single_comment_string
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
				#  This code fills and outputs each line of a doc part. It keeps track of whether the next word will fit on a 
				# line,and starts a new line if needed.

				#@-at

				#@@c
				
				if use_single_comment:
					# New code: 5/31/00
					self.os(self.single_comment_string) ; self.otab()
					line_width =(single_w / self.tab_width + 1) * self.tab_width
				else:
					line_width = self.tab_width
					self.onl() ; self.otab()
				self.put_leading_ws(self.tangle_indent)
				line_width += max(0,self.tangle_indent)
				words = 0 ; word_width = 0
				while i < len(s):
					
				#@<<output or skip whitespace or newlines>>

					#@+node:1::<<output or skip whitespace or newlines>>

					#@+body

					#@+at
					#  This outputs whitespace if it fits, and ignores it otherwise, and starts a new line if a newline is seen. 
					# The effect of self code is that we never start a line with whitespace that was originally at the end of a line.

					#@-at

					#@@c
					
					while is_ws_or_nl(s,i):
						ch = s[i]
						if ch == '\t':
							pad = self.tab_width - (line_width % self.tab_width)
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
								line_width = (single_w / self.tab_width + 1) * self.tab_width
							else:
								self.otab()
								line_width = self.tab_width
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
						self.onl() ; self.otab()
						line_width = self.tab_width
						if use_single_comment:
							self.os(self.single_comment_string) ; self.oblank()
							line_width += len(self.single_comment_string)+ 1
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
	# Outputs leading whitespace, converting tab_width blanks to tabs.
	
	def put_leading_ws(self,indent):
	
		# trace("tab_width:" + `self.tab_width` + ", indent:" + `indent`)
	
		if self.tab_width > 1:
			# Output tabs if possible.
			self.otabs  (indent / self.tab_width)
			self.oblanks(indent % self.tab_width)
		else:
			self.oblanks(indent)

	#@-body

	#@-node:5::put_leading_ws

	#@+node:6::put_newline

	#@+body

	#@+at
	#  This method handles scanning when putting the start of a new line. Unlike the corresponding method in pass one,self method 
	# doesn't need to set a done flag in the caller because the caller already knows where the code section ends.

	#@-at

	#@@c
	
	def put_newline(self,s,i,no_first_lws_flag):
	
		# j = skip_line(s,i) ; trace(`s[i:j]`)
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
	
		if part: name = part.name # can't use choose.
		else: name = "<NULL part>"
		# trace(`name`)
	
		if part.doc and self.output_doc_flag and self.print_bits != silent_bits and part.doc:
			self.put_doc(part.doc)
	
		if part.code:
			self.put_code(part.code,no_first_lws_flag)
	#@-body

	#@-node:7::put_part_node

	#@+node:8::put_section

	#@+body

	#@+at
	#  This method outputs the definition of a section and all sections referenced from the section. name is the section's name. 
	# This code checks for recursive definitions by calling section_check(). We can not allow section x to expand to code 
	# containing another call to section x, either directly or indirectly.

	#@-at

	#@@c
	
	def put_section(self,s,i,name,name_end):
	
		j = skip_line(s,i)
		# trace("indent:" + `self.tangle_indent`  + ", " + `s[i:j]`)
		outer_old_indent = self.tangle_indent
		trailing_ws_indent = 0 # Set below.
		inner_old_indent = 0 # Set below.
		newline_flag = false  # True if the line ends with the reference.
		assert(match(name,0,"<<") or match(name,0,"@<",2))
		
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
			self.tangle_indent += self.tab_width
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
				#  This section outputs each part of a section definition. We first count how many parts there are so that the 
				# code can output a comment saying 'part x of y'.

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
						#  We do not produce an ending comment unless we are ending the last part of the section,and the comment 
						# is clearer if we don't say(n of m).

						#@-at

						#@@c
						
						self.onl() ; self.put_leading_ws(self.tangle_indent)
						#  Don't print trailing whitespace
						name_end -= 1
						while name_end > 0 and is_ws(s[name_end]):
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
						# If something follows the section reference we must add a newline, otherwise the "something" would become 
						# part of the comment.  Any whitespace following the (!newline) should follow the section defintion when Untangled.

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
	#  We can not allow a section to be defined in terms of itself, either directly or indirectly.
	# 
	# We push an entry on the section stack whenever beginning to expand a section and pop the section stack at the end of each 
	# section.  This method checks whether the given name appears in the stack. If so, the section is defined in terms of itself.

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
	#  This function checks the given symbol table for defined but never referenced sections.

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
	#  Enters names and their associated code and doc parts into the given symbol table.
	# `is_dirty` is used only when entering root names.

	#@-at

	#@@c
	
	def st_enter(self,name,code,doc,multiple_parts_flag,is_root_flag):
		
		# trace(`name`)
		v = self.v ; is_dirty = v.isDirty()
		section = self.st_lookup(name,is_root_flag)
		assert(section)
		if doc:
			doc = string.rstrip(doc) # remove trailing lines.
		if code:
			if self.print_bits != silent_bits: # @silent supresses newline processing.
				i = skip_blank_lines(code,0) # remove leading lines.
				if i > 0: code = code[i:]
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
		return len(section.parts) # part number
	#@-body

	#@-node:4::st_enter

	#@+node:5::st_enter_section_name

	#@+body

	#@+at
	#  This function enters a section name into the given symbol table.
	# The code and doc pointers are None for references.

	#@-at

	#@@c
	
	def st_enter_section_name(self,name,code,doc,multiple_parts_flag):
		
		return self.st_enter(name,code,doc,multiple_parts_flag,not_root_name)
	#@-body

	#@-node:5::st_enter_section_name

	#@+node:6::st_enter_root_name

	#@+body
	# Enters a root name into the given symbol table.
	
	def st_enter_root_name(self,name,code,doc):
		
		assert(code)
		if name: # User errors can result in an empty @root name.
			self.st_enter(name,code,doc,disallow_multiple_parts,is_root_name)
	#@-body

	#@-node:6::st_enter_root_name

	#@+node:7::st_lookup

	#@+body

	#@+at
	#  This function looks up name in the symbol table and creates a tst_node for it if it does not exist.

	#@-at

	#@@c
	
	def st_lookup(self,name,is_root_flag):
	
		if is_root_flag:
			key = name
		else:
			key = self.standardize(name)
	
		if key in self.tst.keys():
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

	#@+node:6::untangle

	#@+node:1::compare_comments

	#@+body

	#@+at
	#  This function compares the interior of comments and returns true if they are identical except for whitespace or newlines. 
	# It is up to the caller to eliminate the opening and closing delimiters from the text to be compared.

	#@-at

	#@@c
	
	def compare_comments(self,s1,s2):
	
		comment = self.comment ; comment_end = self.comment_end
		tot_len = len(comment) + len(comment_end)
		CWEB_flag = (self.language == c_language and not self.use_noweb_flag)
		
		p1, p2 = 0, 0
		while p1 < len(s1) and p2 < len(s2):
			p1 = skip_ws_and_nl(s1,p1)
			p2 = skip_ws_and_nl(s2,p2)
			if comment and comment_end:
				
	#@<< Check both parts for @ comment conventions >>

				#@+node:1:C=7:<< Check both parts for @ comment conventions >>

				#@+body

				#@+at
				#  This code is used in forgiving_compare()and in compare_comments().
				# To put self code in the main switch of forgiving_compare()would require splitting the code across cases,which 
				# would greatly obscure the logic and make it impossible to share the code with compare_comments().
				# 
				# In noweb mode we allow / * @ * /  (without the spaces)to be equal to @.
				# In CWEB mode we allow / * @ ? * / (without the spaces)to be equal to @?.
				# at-backslash is not a valid CWEB control code so,we don't have to equate
				# / * @ \\ * / with at-backslash.
				# 
				# We must be careful not to run afoul of this very convention here!

				#@-at

				#@@c
				
				if s1[p1] == '@':
					if s2[p2:p2+tot_len+1] == comment + '@' + end_comment:
						p1 += 1
						p2 += tot_len + 1
						continue
					elif (CWEB_flag and s1[p1] == '@' and p1 + 1 < len(s1) and
						s2[p2:p2+tot_len+2] == comment + '@' + s1[p1+1] ):
						p1 += 2
						p2 += tot_len + 2
						continue
					
				elif s2[p2] == '@':
					if s1[p1:p1+tot_len+1] == comment + '@' + end_comment:
						p2 += 1
						p1 += tot_len + 1
						continue
					elif (CWEB_flag and s1[p1] == '@' and p1 + 1 < len(s1) and
						s1[p1:p1+tot_len+2] == comment + '@' + s2[p2+1] ):
						p2 += 2
						p1 += tot_len + 2
						continue

				#@-body

				#@-node:1:C=7:<< Check both parts for @ comment conventions >>

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

	#@+node:2::definition stack

	#@+node:1::pop_def_node

	#@+body
	def pop_def_node (self):
	
		data = self.def_stack.pop()
		return data

	#@-body

	#@-node:1::pop_def_node

	#@+node:2::push_new_def_node

	#@+body
	# This function pushes a new def_node on the top of the section stack.
	
	def push_new_def_node (self,indent,name,part,of,nl_flag):
	
		trace("name: " + name + ", part: " + `part` +
			", of: " + `of` + ", indent: " + `indent`)
		
		data = (name,indent,part,of,nl_flag,None) # text buffer
		self.def_stack.push(data)
	#@-body

	#@-node:2::push_new_def_node

	#@-node:2::definition stack

	#@+node:3::forgiving_compare

	#@+body

	#@+at
	#  This is the "forgiving compare" function.  It compares two texts and returns true if they are identical except for comments 
	# or non-critical whitespace.  Whitespace inside strings or preprocessor directives must match exactly.

	#@-at

	#@@c
	
	def forgiving_compare(name,part,s1,s2):
	
		
	#@<< Define forgiving_compare vars >>

		#@+node:1::<< Define forgiving_compare vars >>

		#@+body
		# The private globals describing comment delims have already been set by scan_derived_file.
		
		comment = self.comment ; comment_end = self.comment_end
		tot_len = len(comment) + len(comment_end)
		CWEB_flag = (self.language == c_language and not self.use_noweb_flag)
		start_ref = None  # For code that handles section references.
		message = None   # Error message if result is FALSE.
		#@-body

		#@-node:1::<< Define forgiving_compare vars >>

		p1 = 0 ; p2 = skip_ws_and_nl(s2,0) # Allow leading ws in s2 as well.
		result = true
		while result and p1 < len(s1) and p2 < len(s2):
			first1 = p1 ; first2 = p2
			if comment and comment_end:
				
	#@<< Check both parts for @ comment conventions >>

				#@+node:2:C=7:<< Check both parts for @ comment conventions >>

				#@+body

				#@+at
				#  This code is used in forgiving_compare()and in compare_comments().
				# To put self code in the main switch of forgiving_compare()would require splitting the code across cases,which 
				# would greatly obscure the logic and make it impossible to share the code with compare_comments().
				# 
				# In noweb mode we allow / * @ * /  (without the spaces)to be equal to @.
				# In CWEB mode we allow / * @ ? * / (without the spaces)to be equal to @?.
				# at-backslash is not a valid CWEB control code so,we don't have to equate
				# / * @ \\ * / with at-backslash.
				# 
				# We must be careful not to run afoul of this very convention here!

				#@-at

				#@@c
				
				if s1[p1] == '@':
					if s2[p2:p2+tot_len+1] == comment + '@' + end_comment:
						p1 += 1
						p2 += tot_len + 1
						continue
					elif (CWEB_flag and s1[p1] == '@' and p1 + 1 < len(s1) and
						s2[p2:p2+tot_len+2] == comment + '@' + s1[p1+1] ):
						p1 += 2
						p2 += tot_len + 2
						continue
					
				elif s2[p2] == '@':
					if s1[p1:p1+tot_len+1] == comment + '@' + end_comment:
						p2 += 1
						p1 += tot_len + 1
						continue
					elif (CWEB_flag and s1[p1] == '@' and p1 + 1 < len(s1) and
						s1[p1:p1+tot_len+2] == comment + '@' + s2[p2+1] ):
						p2 += 2
						p1 += tot_len + 2
						continue

				#@-body

				#@-node:2:C=7:<< Check both parts for @ comment conventions >>

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
				
				if (match1(string1,string1_len) or match1(string2,string2_len)) and s1[p1] == s2[p2]:
				
					if self.language == pascal_language:
						
				#@<< Compare Pascal strings >>

						#@+node:3::<< Compare Pascal strings >>

						#@+body

						#@+at
						#  We assume the Pascal string is on a single line so the problems with cr/lf do not concern us.

						#@-at

						#@@c
						
						first1 = p1 ; first2 = p2
						p1 = skip_pascal_string(s1,p1)
						p2 = skip_pascal_string(s2,p2)
						resutl = s1[first1,p1] == s2[first2,p2]

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
							if s1[p1] == delim and is_end_of_string(s1,p1,delim):
								result =(s2[p2] == delim and is_end_of_string(s1,p2,delim))
								p1 += 1 ; p2 += 1
								break
							elif is_nl(s1,p1)and is_nl(s2,p2):
								p1 = skip_nl(s1,p1)
								p2 = skip_nl(s2,p2)
							else:
								result = s1[p1] == s2[p2]
								p1 += 1 ; p2 += 1

						#@-body

						#@-node:2::<< Compare C strings >>

					if not result:
						mismatch("Mismatched strings")
				else:
					
				#@<< Compare single characters >>

					#@+node:1:C=8:<< Compare single characters >>

					#@+body
					assert(p1 < len(s1) and p2 < len(s2))
					result = s1[p1] == s2[p2]
					p1 += 1 ; p2 += 1
					if not result: mismatch("Mismatched single characters")
					#@-body

					#@-node:1:C=8:<< Compare single characters >>

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
							if not result or is_end_of_directive(s1,p1):
								break
							p1 = skip_nl(s1,p1)
							p2 = skip_nl(s2,p2)
						else:
							result = s1[p1] == s2[p2]
							p1 += 1 ; p2 += 1
					if not result:
						mismatch("Mismatched preprocessor directives")
					#@-body

					#@-node:2::<< Compare preprocessor directives >>

				else:
					
				#@<< compare single characters >>

					#@+node:1:C=8:<< Compare single characters >>

					#@+body
					assert(p1 < len(s1) and p2 < len(s2))
					result = s1[p1] == s2[p2]
					p1 += 1 ; p2 += 1
					if not result: mismatch("Mismatched single characters")
					#@-body

					#@-node:1:C=8:<< Compare single characters >>


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
					result = compare_section_names(s1[p1:],s2[p2:])
					if result:
						p1, junk1, junk2 = self.skip_section_name(s1,p1)
						p2, junk1, junk2 = self.skip_section_name(s2,p2)
					else: mismatch("Mismatched section names")
				else:
					# Neither p1 nor p2 points at a section name.
					result = s1[p1] == s2[p2]
					p1 += 1 ; p2 += 1
					if not result:
						mismatch("Mismatch at '@' or '<'")
				#@-body

				#@-node:7::<< Compare possible section references >>

			else:
				
	#@<< Compare comments or single characters >>

				#@+node:8::<< Compare comments or single characters >>

				#@+body
				if match_both(sentinel,sentinel_len):
					first1 = p1, first2 = p2
					p1 = skip_to_end_of_line(s1,p1)
					p2 = skip_to_end_of_line(s2,p2)
					result = self.compare_comments(s1[first1:p1],s2[first2:p2])
					if not result:
						mismatch("Mismatched sentinel comments")
				elif match_both(line_comment,line_comment_len):
					first1 = p1, first2 = p2
					p1 = skip_to_end_of_line(s1,p1)
					p2 = skip_to_end_of_line(s2,p2)
					result = compare_comments(s1[first1:p1],s2[first2:p2])
					if not result:
						mismatch("Mismatched single-line comments")
				elif match_both(comment,len(comment)):
					while (p1 < len(s1) and p2 < len(s2) and
						not match_either(comment_end,len(comment_end))):
						# ws doesn't have to match exactly either!
						if is_nl(s1,p1)or is_ws(s1[p1]):
							p1 = skip_ws_and_nl(s1,p1)
						else: p1 += 1
						if is_nl(s2,p2)or is_ws(s2[p2]):
							p2 = skip_ws_and_nl(s2,p2)
						else: p2 += 1
					p1 = skip_ws_and_nl(s1,p1)
					p2 = skip_ws_and_nl(s2,p2)
					if match_both(comment_end,len(comment_end)):
						first1 = p1, first2 = p2
						p1 += len(comment_end)
						p2 += len(comment_end)
						result = compare_comments(s1[first1:p1],s2[first2:p2])
					else: result = false
					if not result:
						mismatch("Mismatched block comments")
				elif match_both(comment2,comment2_len):
					while (p1 < len(s1) and p2 < len(s2) and
						not match_either(comment2_end,comment2_end_len)):
						# ws doesn't have to match exactly either!
						if  is_nl(s1,p1)or is_ws(s1[p1]):
							p1 = skip_ws_and_nl(s1,p1)
						else: p1 += 1
						if is_nl(s2,p2)or is_ws(s2[p2]):
							p2 = skip_ws_and_nl(s2,p2)
						else: p2 += 1
					p1 = skip_ws_and_nl(s1,p1)
					p2 = skip_ws_and_nl(s2,p2)
					if match_both(comment2_end,comment2_end_len):
						first1 = p1, first2 = p2
						p1 += comment2_end_len
						p2 += comment2_end_len
						result = compare_comments(s1[first1:p1],s2[first2:p2])
					else: result = false
					if not result:
						mismatch("Mismatched alternalte block comments")
				else:
					
				#@<< Compare single characters >>

					#@+node:1:C=8:<< Compare single characters >>

					#@+body
					assert(p1 < len(s1) and p2 < len(s2))
					result = s1[p1] == s2[p2]
					p1 += 1 ; p2 += 1
					if not result: mismatch("Mismatched single characters")
					#@-body

					#@-node:1:C=8:<< Compare single characters >>

				#@-body

				#@-node:8::<< Compare comments or single characters >>

		
	#@<< Make sure both parts have ended >>

		#@+node:9::<< Make sure both parts have ended >>

		#@+body
		if result:
			p1 = skip_ws_and_nl(s1,p1)
			p2 = skip_ws_and_nl(s2,p2)
			result = p1 == len(s1) and p2 == len(s2)
			if not result:
				# Show the ends of both parts.
				p1 = len(s1)
				p2 = len(s2)
				mismatch("One part ends before the other.")
		#@-body

		#@-node:9::<< Make sure both parts have ended >>

		if not result:
			
	#@<< Give error message >>

			#@+node:10::<< Give error message >>

			#@+body
			pp1 = max(entry_p1,first1-10)
			pp2 = max(entry_p2,first2-10)
			lim1 = min(len(s1),p1+10)
			lim2 = min(len(s2),p2+10)
				
			trace("Warning: " + message +
				"\nAt part " + `part` + " of section " + name +
				"\np1..." + s1[pp1,lim1] + "\np2..." + s2[pp2,lim2] )
			#@-body

			#@-node:10::<< Give error message >>

		return result
	#@-body

	#@-node:3::forgiving_compare

	#@+node:4::massage_block_comment

	#@+body

	#@+at
	#  This function is called to massage an @doc part in the UST. We call self routine only after a mismatch in @doc parts is 
	# found between the UST and TST. On entry:,the parameters point to the inside of a block C comment: the opening and closing 
	# delimiters are not part of the text handled by self routine.
	# 
	# This code removes newlines that may have been inserted by the Tangle command in a block comment. Tangle may break lines 
	# differently in different expansions, but line breaks are ignored by forgiving_compare() and doc_compare() within block C comments.
	# 
	# We count the leading whitespace from the first non-blank line and remove this much whitespace from all lines. We also remove 
	# singleton newlines and replace sequences of two or more newlines by a single newline.

	#@-at

	#@@c
	
	def massage_block_comment(self,s):
	
		w = self.tab_width
		newlines = 0  # Consecutive newlines seen.
		first = i = skip_blank_lines(s,0)
		# Copy the first line and set n
		i, n = skip_leading_ws_with_indent(s,i,w)
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
				i = skip_leading_ws(s,i,n)
				newlines = 0
				# Copy the rest of the line.
				j = i ; i = skip_to_end_of_line(s,i)
				result += s[j:i]
		return result

	#@-body

	#@-node:4::massage_block_comment

	#@+node:5::scan_derived_file (pass 1)

	#@+body

	#@+at
	#  This function scans an entire derived file in s, discovering section or part definitions.
	# 
	# This is the easiest place to delete leading whitespace from each line: we simply don't copy it.  We also ignore leading 
	# blank lines and trailing blank lines.  The resulting definition must compare equal using the "forgiving" compare to any 
	# other definitions of that section or part.
	# 
	# We use a stack to handle nested expansions.  The outermost level of expansion corresponds to the @root directive that 
	# created the file.  When the stack is popped, the indent variable is restored.
	# self.root_name is the name of the file mentioned in the @root directive.
	# 
	# The caller has deleted all body_ignored_newlines from the text.

	#@-at

	#@@c
		
	def scan_derived_file(s,i):
	
		
	#@<< define scan_derived_file vars >>

		#@+node:1::<< define scan_derived_file vars >>

		#@+body
		first_ip = i
		indent = 0   # The leading whitespace to be deleted(in columns).
		line_indent = 0   # The indentation to use if we see a section reference.
		
		# These are for the call to is_sentinel_line.
		nl_flag = 0 ; result = 0 ; of = 0 ; part = 0
		#@-body

		#@-node:1::<< define scan_derived_file vars >>

		
	#@<< set the private global matching vars >>

		#@+node:2::<< set the private global matching vars >>

		#@+body
		# Set defaults from the public globals set by the @comment command.
		if self.single_comment_string:
			self.sentinel = single_comment_string
			self.sentinel_end = None
		elif self.end_comment_string:
			self.sentinel = self.start_comment_string
			self.sentinel_end = self.end_comment_string
		else:
			self.sentinel = sentinel_end = None
		
		# Set defaults to C
		line_comment = "//" 
		comment = self.start_comment_string
		comment_end = self.end_comment_string
		comment2 = comment2_end = None
		string1 = "\""
		string2 = "'"
		verbatim = None
		
		# Set all special cases.
		if   self.language == c_language: verbatim = "#"
		elif self.language == html_language: line_comment = None
		elif self.language == java_language:
			pass
		elif self.language == pascal_language:
			comment2 = "(*"
			comment2_end = "*)"
		elif self.language == perl_language:
			line_comment = "##"
		elif self.language == perlpod_language:
			line_comment = "##"
			comment2 = "=pod"
			comment2_end = "=cut"
		elif self.language == plain_text_language:
			string1 = string2 = None # This is debatable.
			line_comment = None
		elif self.language == python_language:
			pass
		elif self.language == shell_language:
			line_comment = "##"
		
		# Set the lengths of all delimiter strings.
		if 0: # use len instead
			set(len(comment),     comment)
			set(comment2_len,comment2)
			set(len(comment_end),comment_end)
			set(comment2_end_len,comment2_end)
			set(sentinel_len,sentinel)
			set(sentinel_end_len,sentinel_end)
			set(line_comment_len,line_comment)
			set(string1_len,string1)
			set(string2_len,string2)
			set(verbatim_len,verbatim)
		#@-body

		#@-node:2::<< set the private global matching vars >>

		# Set indent.
		i, indent = skip_leading_ws_with_indent(s,i,self.tab_width)
		
	#@<< Skip the header line output by tangle >>

		#@+node:3::<< Skip the header line output by tangle >>

		#@+body
		if sentinel or comment:
			line = " Created by Leo from" + choose(sentinel,sentinel,comment)
			if s[i:i+len(line)] == line:
				# Even a block comment will end on the first line.
				i = skip_to_end_of_line(s,i)
		#@-body

		#@-node:3::<< Skip the header line output by tangle >>

		# The top level of the stack represents the root.
		push_new_def_node(indent,self.root_name,1,1,TRUE)
		while i < len(s):
			ch = s[i]
			if ch == body_ignored_newline:
				i += 1 # ignore
			elif ch == body_newline:
				
	#@<< handle the start of a new line >>

				#@+node:4::<< handle the start of a new line >>

				#@+body
				copy(ch) ; i += 1 # This works because we have one-character newlines.
				
				# Set line_indent,for use only if we see a section reference.
				junk, line_indent = skip_leading_ws_with_indent(s,i,self.tab_width)
				i = skip_leading_ws(s,i,indent) # skip indent leading white space.
				#@-body

				#@-node:4::<< handle the start of a new line >>

			elif match(s,i,sentinel) and test_sentinel(s,i,sentinel):
				
	#@<< handle a sentinel line  >>

				#@+node:5::<< handle a sentinel line >>

				#@+body

				#@+at
				#  This is the place to eliminate the proper amount of whitespace from the start of each line. We do self by 
				# setting the 'indent' variable to the leading whitespace of the first _non-blank_ line following the opening sentinel.
				# 
				# Tangle increases the indentation by one tab if the section reference is not the first non-whitespace item on the 
				# line,so self code must do the same.

				#@-at

				#@@c
				
				if result == end_sentinel_line:
					trace("--end--" + name)
					
				
				#@<< terminate the previous part of this section if it exists >>

				#@+node:1::<< terminate the previous part of this section if it exists >>

				#@+body

				#@+at
				#  We have just seen a sentinel line. Any kind of sentinel line will terminate a previous part of the present 
				# definition. For end sentinel lines, the present section name must match the name on the top of the stack.

				#@-at

				#@@c
				
				if len(self.def_stack) > 0:
					dn = self.def_stack[0]
					if compare_section_names(name,dn.name):
						dn = pop_def_node()
						if len(dn.text) > 0:
							# prev_ip = None ; prev_limit = None
							part, nl_flag = ust_lookup(name,dn.part,dn.text,false,false) # not root, not update
							# Check for incompatible previous definition.
							if found and not forgiving_compare(name,dn.part,dn.text):
								self.error("Incompatible definitions of " + name)
							elif not found:
								self.ust_enter(ust,name,dn.part,dn.of,dn.text,dn.nl_flag,false) # not root
					elif result == end_sentinel_line:
						self.error("Missing sentinel line for: " + name)
				#@-body

				#@-node:1::<< terminate the previous part of this section if it exists >>

				if result == start_sentinel_line:
					indent = line_indent
					# Increase line_indent by one tab width if the
					# the section reference does not start the line.
					j = i - 1
					while j >= 0:
						if is_nl(s,j):
							break
						elif not is_ws(s[j]):
							indent += self.tab_width ; break
						j -= 1
					# copy the section reference to the _present_ section,
					# but only if this is the first part of the section.
					if part < 2: copy(name)
					# Skip to the first character of the new section definition.
					i = skip_to_end_of_line(s,i)
					# Start the new section.
					self.push_new_def_node(indent,name,part,of,nl_flag)
				else:
					assert(result == end_sentinel_line)
					# Skip the sentinel line.
					i = skip_to_end_of_line(s,i)
					# Skip a newline only if it was added after(!newline)
					if not nl_flag:
						i = skip_ws(s,i)
						i = skip_nl(s,i)
						i = skip_ws(s,i)
						# Copy any whitespace following the(!newline)
						while end_p and is_ws(s[end_p]):
							self.copy(s[end_p])
							end_p += 1
					# Restore the old indentation level.
					if self.def_stack:
						indent = self.def_stack.indent ## ?????
				#@-body

				#@-node:5::<< handle a sentinel line >>

			elif (match(line_comment,line_comment_len) or
				match(verbatim,verbatim_len)):
				
	#@<< copy the entire line >>

				#@+node:6::<< copy the entire line >>

				#@+body
				j = i ; i = skip_to_end_of_line(s,i)
				self.copy(s[j:i])

				#@-body

				#@-node:6::<< copy the entire line >>

			elif match(comment,len(comment)):
				
	#@<< copy a multi-line comment >>

				#@+node:8::<< copy a multi-line comment >>

				#@+body
				assert(comment_end)
				j = i
				# Scan for the ending delimiter.
				i += len(comment)
				while i < len(s) and not match(s,i,comment_end):
					i += 1
				if match(s,i,comment_end):
					i += len(comment_end)
				self.copy(s[j:i])
				#@-body

				#@-node:8::<< copy a multi-line comment >>

			elif match(comment2,comment2_len):
				
	#@<< copy an alternate multi-line comment >>

				#@+node:9::<< copy an alternate multi-line comment >>

				#@+body
				assert(comment2_end)
				j = i
				# Scan for the ending delimiter.
				i += len(comment2)
				while i < len(s) and not match(s,i,comment2_end):
					i += 1
				if match(s,i,comment2_end):
					i += len(comment2)
				self.copy(s[j:i])
				#@-body

				#@-node:9::<< copy an alternate multi-line comment >>

			elif (match(string1,string1_len) or
				match(string2,string2_len)):
				
	#@<< copy a string >>

				#@+node:7::<< copy a string >>

				#@+body
				j = i
				if self.language == pascal_language:
					i = skip_pascal_string(s,i)
				else:
					i = skip_string(s,i)
				self.copy(s[j:i])
				#@-body

				#@-node:7::<< copy a string >>

			else:
				self.copy(ch) ; i += 1
		
	#@<< end all open sections >>

		#@+node:10::<< end all open sections >>

		#@+body
		dn= None
		while len(self.def_stack) > 0:
			dn = pop_def_node()
			if len(sefl.def_stack) > 0:
				self.error("Unterminated section: " + dn.name)
		if dn:
			# Terminate the root setcion.
			i = len(s)
			if text and len(text) > 0:
				self.ust_enter(dn.name,dn.part,dn.of,dn.text,dn.nl_flag,true) # is_root_flag
			else:
				self.error("Missing root part")
		else:
			self.error("Missing root section")
		#@-body

		#@-node:10::<< end all open sections >>

	#@-body

	#@-node:5::scan_derived_file (pass 1)

	#@+node:6::scanning & copying

	#@+node:1::copy

	#@+body
	def copy(self, s):
	
		dn = self.def_stack[0]
		dn.text += s
	#@-body

	#@-node:1::copy

	#@+node:2::is_end_of_directive

	#@+body
	# This function returns true if we are at the end of preprocessor directive.
	
	def is_end_of_directive(s,i):
	
		return is_nl(s,i) and not is_escaped(s,i)
	#@-body

	#@-node:2::is_end_of_directive

	#@+node:3::is_end_of_string

	#@+body
	def is_end_of_string(s,i,delim):
	
		return i < len(s) and s[i] == delim and not is_escaped(s,i)
	#@-body

	#@-node:3::is_end_of_string

	#@+node:4::is_escaped

	#@+body
	# This function returns true if the s[i] is preceded by an odd number of back slashes.
	
	def is_escaped(s,i):
	
		back_slashes = 0 ; i -= 1
		while i >= 0 and s[i] == '\\':
			back_slashes += 1
			i -= 1
		return (back_slashes & 1) == 1

	#@-body

	#@-node:4::is_escaped

	#@+node:5::is_sentinel_line & is_sentinel_line_with_data

	#@+body

	#@+at
	#  This function returns true if i points to a line a sentinel line of one of the following forms:
	# 
	# start_sentinel <<section name>> end_sentinel
	# start_sentinel <<section name>> (n of m) end_sentinel
	# start_sentinel -- end -- <<section name>> end_sentinel
	# start_sentinel -- end -- <<section name>> (n of m) end_sentinel
	# 
	# start_sentinel: the string that signals the start of sentinel lines\
	# end_sentinel:   the string that signals the endof sentinel lines.
	# 
	# end_sentinel may be None,indicating that sentinel lines end with a newline. Any of these forms may end with (!newline), 
	# indicating that the section reference was not followed by a newline in the orignal text.
	# 
	# This routine sets the newline flag to false in the caller if such a string is seen. We set the name_ip1 and name_ip2 
	# arguments in the caller to the start and end of the section name. This function sets the result param in the caller. The 
	# valid values of result are:
	# 
	# non_sentinel_line,   # not a sentinel line.
	# start_sentinel_line, #   /// <section name> or /// <section name>(n of m)
	# end_sentinel_line  //  /// -- end -- <section name> or /// -- end -- <section name>(n of m).

	#@-at

	#@@c
	
	def is_sentinel_line(self,s,i):
	
		result, i, kind, name, part, of, end, nl_flag = self.is_sentinel_line_with_data(s,i)
		return result
	
	def is_sentinel_line_with_data(self,s,i):
	
		
	#@<< Initialize the return values >>

		#@+node:1::<< Initialize the return values  >>

		#@+body
		name = end = None
		part = of = 1
		kind = non_sentinel_line
		nl_flag = true
		
		false_data = false, i, kind, name, part, of, end, nl_flag

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
		# If i points to "-- end --",self code skips it and sets end_flag.
		
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
		
			i, kind, name = self.skip_section_name(s,i)
			if result != section_ref:
				return false_data
		else:
			return false_data
		#@-body

		#@-node:4::<< Make sure we have a section reference >>

		
	#@<< Set part and of if they exist >>

		#@+node:5::<< Set part and of if they exist >>

		#@+body
		# This code handles(m of n),if it exists.
		
		i = skip_ws(s,i)
		if match(c,i,'('):
			j = i
			i += 1 ; i = skip_ws(s,i)
			i, part = self.scan_short_val(s,i)
			if part == -1:
				i = j # back out of the scanning for the number.
			else:
				i = skip_ws(s,i)
				if not match(s,i,"of"):
					return false_data
				i += 2 ; i = skip_ws(s,i)
				i, of = scan_short_val(s,i)
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
				i += end_sentinel_len
			else:
				return false_data
		
		end = i # Show the start of the whitespace.
		i = skip_ws(s,i)
		if i < len(s) and not is_nl(s,i):
			return false_data
		#@-body

		#@-node:7::<< Make sure the line ends with end_sentinel >>

		kind = choose(end_flag,end_sentinel_line,start_sentinel_line)
		return true, i, kind, name, part, of, end, nl_flag
	#@-body

	#@-node:5::is_sentinel_line & is_sentinel_line_with_data

	#@+node:6::scan_short_val

	#@+body
	# This function scans a positive integer.
	# returns (i,val), where val == -1 if there is an error.
	
	def scan_short_val(s,i):
	
		if i >= len(s) or s[i] not in string.digits:
			return i, -1
	
		val = 0
		while i < len(s) and s[i] in string.digits:
			val = val * 10 + (s[i] - '0')
			i += 1
		return i, val
	#@-body

	#@-node:6::scan_short_val

	#@-node:6::scanning & copying

	#@+node:7::update_def (pass 2)

	#@+body

	#@+at
	#  This function handles the actual updating of section definitions in the web.  Only code parts are updated, never doc parts.
	# 
	# During pass 2 of Untangle, skip_body() call this routine when it the Tangle code discovers the definition of a section in 
	# the outline.  We look up the name in the ust. If an entry exists, we compare the code (the code part of an outline node) 
	# with the code parts in the ust. We update the code part if necessary.
	# 
	# We use the forgiving_compare() to compare code parts. It's not possible to change only trivial whitespace using Untangle 
	# because forgiving_compare() ignores trivial whitespace.

	#@-at

	#@@c
	
	# Major change: 2/23/01: Untangle never updates doc parts.
	
	def update_def(self,name,part,code1,code2,is_root_flag): # Doc parts are never updated!
	
		v = self.v ; body = v.bodyString()
		code = body[code1:code2]
		ucode, nl_flag = ust_lookup(name,part,is_root_flag,true) # Set update
		
	#@<< Remove leading blank lines and block comments from ucode >>

		#@+node:1::<< Remove leading blank lines and block comments from ucode >>

		#@+body
		i = skip_blank_lines(ucode,0)
		ucode = ucode[i:]
		i = skip_ws(ucode,i)
		
		if comment and comment_end and match(ucode,i,comment):
			
			# Skip to the end of the comment.
			i += len(comment)
			while i < len(ucode):
				if match(ucode,i,end_comment):
					i += len(comment_end)
					i = skip_ws_and_nl(ucode,i)
					ucode = ucode[i:]
					break
				else: i += 1
		

		#@-body

		#@-node:1::<< Remove leading blank lines and block comments from ucode >>

		if not ucode:
			return # Not an error.
		if code and forgiving_compare(name,part,code,ucode):
			return
		# Replace code with ucode
		es("***Updating:   " + v.headString())
		# Strip leading and trailing blank lines.
		i = skip_blank_lines(ucode,0)
		ucode =ucode[i:]
		ucode = string.rstrip(ucode)
		body = body[:code1] + ucode + body[code2:] # update the body
		self.update_current_vnode(body)
		return body

	#@-body

	#@-node:7::update_def (pass 2)

	#@+node:8::update_current_vnode

	#@+body

	#@+at
	#  This function is called from within the Untangle logic to update the body text of the vnode indicated by the global bridge_vnode.

	#@-at

	#@@c
	
	def update_current_vnode(self,s):
	
		c = self.commands ; v = self.v
		assert(self.v)
		v.setBodyStringOrPane(s)
		
		c.beginUpdate()
		c.setChanged(true)
		v.setDirty()
		v.setMarked()
		c.endUpdate()
	#@-body

	#@-node:8::update_current_vnode

	#@-node:6::untangle

	#@+node:7::ust

	#@+node:1::ust_dump

	#@+body
	def ust_dump(table):
	
		s = "\n---------- Dump of Untangle Symbol Table ----------\n"
		keys = self.ust.keys()
		keys.sort()
		for name in keys:
			section = self.ust[name]
			s += "\nsection:" + section.name
			for part in section.parts:
				assert(part.of == section.of)
				s += "\n----- part " + `part.part` + " of " + `part.of` + " -----\n"
				s += `part.code`
		return s
	#@-body

	#@-node:1::ust_dump

	#@+node:2::ust_enter

	#@+body

	#@+at
	#  This routine enters names and their code parts into the given table. The 'part' and 'of' parameters are taken from the 
	# "(part n of m)" portion of the line that introduces the section definition in the C code.
	# 
	# If no part numbers are given the caller should set the 'part' and 'of' parameters to zero.  The caller is reponsible for 
	# checking for duplicate parts.
	# 
	# This function handles names scanned from a source file; the corresponding st_enter routine handles names scanned from outlines.

	#@-at

	#@@c
	
	def ust_enter(self,name,part,of,code,nl_flag,is_root_flag):
	
		if not is_root_flag:
			name = self.standardize_name(name)
		
	#@<< remove blank lines from the start and end of the text >>

		#@+node:1::<< remove blank lines from the start and end of the text >>

		#@+body
		i = skip_blank_lines(text,0)
		if i > 0: text = text[i:]
		text = string.rstrip(text)

		#@-body

		#@-node:1::<< remove blank lines from the start and end of the text >>

		u = ustNode(name,text,part,of,nl_flag,false) # update_flag
		if self.ust.has_key(name):
			section = ust[name]
			## does not check part or of.
			section.parts.append(u)
		else:
			self.ust[name] = u
	
		trace("section name: [" + name + "](" + `part` + " of " + `of` + ")...")
	#@-body

	#@-node:2::ust_enter

	#@+node:3::ust_lookup

	#@+body
	# This function searches the given table for a part matching the section_name and part number.
	
	# new: it just returns the part.  nl_flag not used!  (caller can set it)
	
	def ust_lookup(self,name,text,part_number,nl_flag,is_root_flag,update_flag):
	
		if not is_root_flag:
			name = self.standardize_name(name)
	
		if self.ust.has_key(name):
			section = self.ust[name]
			if len(section.parts) >= part_number:
				part = section.parts[part_number]
			else: part = None
				
		trace(choose(part,"found","not found") +
			": " + choose(is_root_flag,"root","section") +
			" name: [" + name + "](" + `part_number` + ")...\n")
		# trace(`part.code`)
		
		if part and update_flag: part.update_flag = true
		return part
	#@-body

	#@-node:3::ust_lookup

	#@+node:4::ust_warn_about_orphans

	#@+body

	#@+at
	#  This function issues a warning about any sections in the derived file for which no corresponding section has been seen in 
	# the outline.

	#@-at

	#@@c
	
	def ust_warn_about_orphans(self):
	
		for section in self.ust:
			for part in section.parts:
				assert(part.of == bucket.of)
				if not part.update_flag:
					es("Warning: " +
	 					choose(self.use_noweb_flag,"<< ","@< ") +
						part.name +
						choose(self.use_noweb_flag," >>"," @>") +
						" is not in the outline")
					break # One warning per section is enough.

	#@-body

	#@-node:4::ust_warn_about_orphans

	#@-node:7::ust

	#@+node:8::utility methods

	#@+body

	#@+at
	#  These utilities deal with tangle ivars, so they should be methods.

	#@-at

	#@-body

	#@+node:1::error & warning

	#@+body
	def error (self,s):
	
		self.errors += 1
		es(s)
		
	def warning (self,s):
	
		es(s)
	#@-body

	#@-node:1::error & warning

	#@+node:2::is_section_name

	#@+body
	def is_section_name(self,s,i):
	
		kind = bad_section_name ; end = -1
	
		if self.use_cweb_flag :
			if match(s,i,"@<"):
				i, kind, end = self.skip_cweb_section_name(s,i)
		elif match(s,i,"<<"):
			i, kind, end = self.skip_noweb_section_name(s,i)
	
		return i, kind, end
	#@-body

	#@-node:2::is_section_name

	#@+node:3:C=9:tangle.scanAllDirectives

	#@+body

	#@+at
	#  This code scans the node v and all its ancestors looking for directives.  If found,the corresponding globals are set for 
	# use by Tangle, Untangle and syntax coloring.
	# 
	# Once a directive is seen, related directives in ancesors have no effect.  For example, if an @color directive is seen in 
	# node x, no @color or @nocolor directives are examined in any ancestor of x.

	#@-at

	#@@c
	
	def scanAllDirectives(self,v,require_path_flag,issue_error_flag):
	
		c = self.commands ; frame = c.frame
		# trace(`v`)
		old_bits = 0 # One bit for each directive.
		self.init_directive_ivars()
		while v:
			s = v.bodyString()
			bits, dict = is_special_bits(s,dont_set_root_from_headline)
			# trace("bits:" + `bits` + ", dict:" + `dict`, ", " + `v`)
			
	#@<< Test for @comment or @language >>

			#@+node:1::<< Test for @comment or @language >>

			#@+body
			if btest(old_bits,comment_bits)or btest(old_bits,language_bits):
				 pass # Do nothing more.
			elif btest(bits,comment_bits):
				i = dict["comment"]
				set_root_delims(s[i:])
				# @comment effectively disables Untangle.
				arg_present_language = unknown_language
			elif btest(bits,language_bits):
				issue_error_flag = false
				i = dict["language"]
				set_language(s,i,issue_error_flag,c.target_language)

			#@-body

			#@-node:1::<< Test for @comment or @language >>

			
	#@<< Test for @verbose,@terse or @silent >>

			#@+node:2::<< Test for @verbose, @terse or @silent >>

			#@+body

			#@+at
			#  It is valid to have more than one of these directives in the same body text: the more verbose directive takes precedence.

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

			#@-node:2::<< Test for @verbose, @terse or @silent >>

			
	#@<< Test for @path,@pagewidth and @tabwidth >>

			#@+node:3::<< Test for @path, @pagewidth and @tabwidth >>

			#@+body
			if require_path_flag and btest(bits,path_bits)and not btest(old_bits,path_bits):
				i = dict["path"]
				j = skip_to_end_of_line(s,i+5) # Point past @path
				path = string.strip(s[i+5:j])
				
			#@<< Remove leading and trailing delims if they exist >>

				#@+node:1::<< Remove leading and trailing delims if they exist >>

				#@+body
				# es(ftag + " path: " + path)
				# Remove leading and trailing delims if they exist.
				if len(path) > 2 and (
					(path[0]=='<' and path[-1] == '>') or
					(path[0]=='"' and path[-1] == '"') ):
					path = path[1:-1]
				path = string.strip(path)
				#@-body

				#@-node:1::<< Remove leading and trailing delims if they exist >>

				if len(path) > 0:
					dir = os.path.dirname(path)
					if len(dir) > 0 and os.path.exists(dir):
						self.tangle_directory = dir
						trace("@path dir:" + `dir`)
					elif issue_error_flag and not self.path_warning_given:
						self.path_warning_given = true # supress future warnings
						self.error("Invalid directory: " + `s[i:j]`)
				elif issue_error_flag and not self.path_warning_given:
					self.path_warning_given = true # supress future warnings
					self.error("Empty @path")
			
			if btest(bits,page_width_bits) and not btest(old_bits,page_width_bits):
				i = dict["pagewidth"]
				i, val = skip_long(s,i+10) # Point past @pagewidth
				if val == -1:
					if issue_error_flag:
						j = skip_to_end_of_line(s,i)
						es("ignoring " + s[i:j])
				else: arg_page_width = val
			
			if btest(bits,tab_width_bits)and not btest(old_bits,tab_width_bits):
				i = dict["tabwidth"]
				i, val = skip_long(s,i+9) # Point past @tabwidth.
				if val == -1:
					if issue_error_flag:
						j = skip_to_end_of_line(s,i)
						es("ignoring " + s[i:j])
				else: arg_tab_width = val
			#@-body

			#@-node:3::<< Test for @path, @pagewidth and @tabwidth >>

			
	#@<< Test for @header or @noheader >>

			#@+node:4::<< Test for @header or @noheader >>

			#@+body
			if btest(old_bits,header_bits)or btest(old_bits,noheader_bits):
				pass # Do nothing more.
			elif btest(bits,header_bits)and btest(bits,noheader_bits):
				if issue_error_flag:
					es("conflicting @header and @noheader directives")
			elif btest(bits,header_bits):
				arg_use_header_flag = true
			elif btest(bits,noheader_bits):
				arg_use_header_flag = false

			#@-body

			#@-node:4::<< Test for @header or @noheader >>

			old_bits |= bits
			v = v.parent()
		if c.frame and require_path_flag and not self.tangle_directory:
			# No path is in effect.
			
	#@<< Set self.tangle_directory >>

			#@+node:5::<< Set self.tangle_directory >>

			#@+body

			#@+at
			#  This code sets self.tangle_directory--it has not already been set by an @path directive.
			# 
			# An explicit file name in an @root directive will override the directory set here.  The final file name will be os.path.join(self.tangle_directory,fileName)
			# 
			# If no @path directive is in effect we use the following directories:
			# 1. The directory in the @root directive (self.root_name)
			# 2. The Tangle Default Directory specified in the Preferences panel.
			# 3. The directory set by the Open command

			#@-at

			#@@c
			
			# Always check @root directory if it exists.
			if self.root_name and len(self.root_name) > 0:
				dir = os.path.dirname(self.root_name)
				if len(dir) > 0 and os.path.exists(dir):
					self.tangle_directory = dir
					trace("@root directory:" + `dir`)
				elif len(dir) > 0 and issue_error_flag and not self.path_warning_given:
					self.path_warning_given = true
					self.error("@root directory missing or invalid: " + dir)
			
			if not self.tangle_directory and c.tangle_directory and len(c.tangle_directory) > 0:
				dir = c.tangle_directory
				if len(dir) > 0 and os.path.exists(dir):
					self.tangle_directory = dir
					trace("Default tangle directory:" + `dir`)
				elif len(dir) > 0 and issue_error_flag and not self.path_warning_given:
					self.path_warning_given = true
					self.error("Invalid Default Tangle Directory: " + dir)
			
			if not self.tangle_directory and c.frame.openDirectory and len(c.frame.openDirectory) > 0:
				dir = c.frame.openDirectory # Try the directory used in the Open command
				if len(dir) > 0 and os.path.exists(dir):
					self.tangle_directory = dir
					trace("Open directory:" + `dir`)
				elif len(dir) > 0 and issue_error_flag and not self.path_warning_given:
					self.path_warning_given = true
					self.error("Invalid Open directory: " + dir)
			
			if not self.tangle_directory and issue_error_flag and not self.path_warning_given:
				self.path_warning_given = true
				self.error("No directory specified by @root, @path or Preferences.")
			#@-body

			#@-node:5::<< Set self.tangle_directory >>

		trace(`self.tangle_directory`)
	#@-body

	#@-node:3:C=9:tangle.scanAllDirectives

	#@+node:4::set_root_delims

	#@+body
	def set_root_delims(self,s):
	
		(self.single_comment_string,
		self.start_comment_string,
		self.end_comment_string) = set_delims_from_string(s)
	#@-body

	#@-node:4::set_root_delims

	#@+node:5::set_root_from_headline

	#@+body
	def set_root_from_headline (self,v):
	
		# trace(`v`)
		s = v.headString()
	
		if s[0:5] == "@root":
			i = skip_ws(s,5)
			if i < len(s): # Non-empty file name.
				# self.root_name must be set later by token_type().
				self.root = s
	#@-body

	#@-node:5::set_root_from_headline

	#@+node:6::set_root_from_text

	#@+body

	#@+at
	#  This code skips the file name used in @root directives.  i points after the @root directive.
	# 
	# File names may be enclosed in < and > characters, or in double quotes.  If a file name is not enclosed be these delimiters 
	# it continues until the next newline.

	#@-at

	#@@c
	def set_root_from_text(self,s,err_flag):
		
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

	#@-node:6::set_root_from_text

	#@+node:7::skip_CWEB_section_name

	#@+body

	#@+at
	#  This function skips past a section name that starts with @< and ends with @>. This code also skips any = following the 
	# section name.
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

	#@-node:7::skip_CWEB_section_name

	#@+node:8::skip_noweb_section_name

	#@+body

	#@+at
	#  This function skips past a section name that starts with < < and might end with > > or > > =. The entire section name must 
	# appear on the same line.
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
		while i < len(s) and not match(s, i, body_newline):
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

	#@-node:8::skip_noweb_section_name

	#@+node:9::skip_section_name

	#@+body
	# Returns a tuple (i, kind, end)
	
	def skip_section_name(self,s,i):
	
		if self.use_noweb_flag:
			return self.skip_noweb_section_name(s,i)
		else:
			return self.skip_cweb_section_name(s,i)
	#@-body

	#@-node:9::skip_section_name

	#@+node:10::standardize

	#@+body

	#@+at
	#  This code removes leading and trailing brackets, converts white space to a single blank and converts to lower case.

	#@-at

	#@@c
	
	def standardize (self,name):
	
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

	#@-node:10::standardize

	#@+node:11::token_type

	#@+body

	#@+at
	#  This method returns a code indicating the apparent kind of token at the position i. The caller must determine whether 
	# section definiton tokens are valid.
	# 
	# returns (kind, end) and sets global root_name using set_root_from_text().

	#@-at

	#@@c
	
	def token_type(self,s,i,err_flag):
	
		# j = skip_line(s,i) ; trace(`s[i:j]`)
		kind = plain_line ; end = -1
		if self.use_noweb_flag :
			
	#@<< set token_type in noweb mode >>

			#@+node:1::<< set token_type in noweb mode >>

			#@+body
			if match(s,i,"<<"):
				i, kind, end = self.skip_section_name(s,i)
				if kind == bad_section_name:
					kind = plain_line # not an error.
				elif kind == at_root:
					if head_root:
						self.set_root_from_text(head_root,err_flag)
					else:
						kind = bad_section_name # The warning has been given.
			elif match(s,i,"@ ") or match(s,i,"@\n"): kind = at_doc
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
				("@code", at_code), ("@doc", at_doc),
				("@root", at_root), ("@section", at_section) ]:
				if match_word(s,i,name):
					kind = type ; break
			
			if kind == at_root:
				j = i + 5
				i = self.set_root_from_text(s[i+5:],err_flag)
			#@-body

			#@-node:3::<< set kind for directive >>

		return kind, end
	#@-body

	#@-node:11::token_type

	#@-node:8::utility methods

	#@-others
	
	#@-body

	#@-node:3::<< tangleCommands methods >>

#@-body

#@-node:0::@file leoTangle.py

#@-leo
