#@+leo-ver=4-thin
#@+node:bwmulder.20041017125718:@thin mod_shadow.py
# Warning: this code has not been heavily tested.

#@<<docstring>>
#@+node:bwmulder.20041017125718.1:<< docstring >>
"""
Use a subfolder for files with Leo comments.

Adapted for post 4.2 (cvs versoin).

I have not yet written unit tests for this plugin. Please use with
caution.

I have seen some messages when updating from external
sources, which I have not yet analysed.

This plugin allows you to use Leo with files which contain no
Leo comments, and still have information flow in both directions:
from the file into Leo, and from Leo into the file.

To start using this plugin:
    - Go to the directories where the sources are.
    - Create a subfolder called Leo (or whatever you have set shodow_subdir to).
    - Copy the files into the subfolder.
    - Replace the files with files of length 0.
        (actually: <= 2, so that on Windows you can say: @echo.>filename)
    - Enable this plugin.
    - Start Leo.
    
    After starting, Leo will copy the files from the Leo subfolder to the old
    location after removing all sentinels.
    
    After this initial setup, changes in Leo will be reflected both in the file
    in the Leo subfolder, and the file without sentinels.
    
    Conversely, changes in the file without sentinels will flow back to the file
    in the leo subfolder, and show up in Leo.
    
You can change the name of the shadow subfolder, default Leo, via the mod_shadow.ini
configuration file.

Configuraton:
    verbosity >= 1: print logon message in status pane.
    verbosity >= 2: print message each time the subfolder is used.
    
You can specify a prefix for the shadow files. This is so that the py.test script
does not pick up test scripts twice (once the file without Leo sentinels, once the
shadow file).
"""
#@-node:bwmulder.20041017125718.1:<< docstring >>
#@nl

# Terminology:
# 'push' create a file without sentinels from a file with sentinels.
# 'pull' propagate changes from a file without sentinels to a file with sentinels.

#@@language python
#@@tabwidth -4

__version__ = "0.9"
#@<< version history >>
#@+node:ekr.20041110090700:<< version history >>
#@@killcolor 
#@+at
# 
# 0.1: Original code by Bernhard Mulder.
# 
# 0.2: Modifications by EKR.
# 
# - The correct spelling is "Leo", not "LEO".
# - The name of the folder will be "leo-shadow", not "LEO"
#   This should perhaps be a configuration option.
# - Modified code to work with simplified atFile class.
# - Changed the name of the .ini file to mod_shadow.ini.
# - Use import leoGlobals as g.
# 
# 0.9 Adapt to cvs post 4.2 by Bernhard Mulder
# - fixed assertion in original_replaceTargetFileIfDifferent
# 
# 0.9.1 Added prefix option.
#@-at
#@nonl
#@-node:ekr.20041110090700:<< version history >>
#@nl
#@<< globals >>
#@+node:ekr.20041110091737:<< globals >>
testing = True 

print_copy_operations = True # True: tell when files are copied.

do_backups = False # True: always make backups of each file.

shadow_subdir = "Leo" # subdirectory for shadow files.

prefix = "" # Prefix to be used for shadow files, if any.

active = True # The plugin can be switched off by this switch

verbosity = 1

__version__ = "$Rev: 1765 $"
__author__  = "Bernhard Mulder"
__date__    = "$Date$"
__cvsid__   = "$Id$"
#@-node:ekr.20041110091737:<< globals >>
#@nl
#@<< Notes >>
#@+node:bwmulder.20041231171842:<< Notes >>
#@+doc
# 1. Not sure if I should do something about read-only files. Are they a 
# problem? Should I check for them?
# 
# 2. Introduced openForRead and openForWrite. Both are introduced only as a 
# hook for the mod_shadow plugin, and default to
# the predefined open.
# 
# 3. Changed replaceTargetFileIfDifferent to return True if the file has been 
# replaced (otherwise, it still returns None).
# 
# 4. In gotoLineNumber: encapsulated
#                 theFile=open(fileName)
#                 lines = theFile.readlines()
#                 theFile.close()
# into a new method "gotoLinenumberOpen"
# 
# 5. Introduced a new function "applyLineNumberMappingIfAny" in 
# gotoLineNumber. The default implementation returns the argument.
#@-doc
#@-node:bwmulder.20041231171842:<< Notes >>
#@nl
   
#@+others
#@+node:bwmulder.20041017130018:imports
import leoGlobals as g 

import leoAtFile
import leoCommands
import leoImport 
import leoPlugins

import ConfigParser 
import difflib
import os
import shutil
#@nonl
#@-node:bwmulder.20041017130018:imports
#@+node:bwmulder.20041018233934.1:plugin core
#@+node:bwmulder.20041017130118:auxilary functions
#@+node:bwmulder.20041017125718.4:copy_time
def copy_time (sourcefilename,targetfilename):
   """
   Set the modification time of the targetfile the same
   as the sourcefilename
   """
   st = os.stat(sourcefilename)
   if hasattr(os,'utime'):
      os.utime(targetfilename,(st.st_atime,st.st_mtime))
   elif hasattr(os,'mtime'):
      os.mtime(targetfilename,st.st_mtime)
   else:
      assert 0, "Sync operation can't work if no modification time can be set"
#@-node:bwmulder.20041017125718.4:copy_time
#@+node:bwmulder.20041017125718.5:marker_from_extension
def marker_from_extension (filename):
   """
   Tries to guess the sentinel leadin
   comment from the filename extension.
   
   This code should probably be shared
   with the main Leo code.
   """
   root, ext = os.path.splitext(filename)
   if ext=='.tmp':
      root, ext = os.path.splitext(root)
   if ext in('.h','.c'):
      marker = "//@"
   elif ext in(".py",".cfg",".bat",".ksh",".txt"):
      marker = '#'+'@'
   else:
      assert 0, "extension %s not handled by this plugin"%ext 
   return marker 
#@-node:bwmulder.20041017125718.5:marker_from_extension
#@+node:bwmulder.20041017125718.3:write_if_changed
def write_if_changed (lines,sourcefilename,targetfilename):
   """
   
   Checks if 'lines' matches the contents of
   'targetfilename'. Refreshes the targetfile with 'lines' if not.

   Produces a message, if wanted, about the overrite, and optionally
   keeps the overwritten file with a backup name.

   """
   if not os.path.exists(targetfilename):
      copy = True 
   else:
      copy = lines!=file(targetfilename).readlines()
   if copy:
      if print_copy_operations:
         print "Copying ", sourcefilename, " to ", targetfilename, " without sentinals"

      if do_backups:
         # Keep the old file around while we are debugging this script
         if os.path.exists(targetfilename):
            count = 0
            backupname = "%s.~%s~"%(targetfilename,count)
            while os.path.exists(backupname):
               count+=1
               backupname = "%s.~%s~"%(targetfilename,count)
            os.rename(targetfilename,backupname)
            if print_copy_operations:
               print "backup file in ", backupname 
      outfile = open(targetfilename,"w")
      for line in lines:
         outfile.write(line)
      outfile.close()
      copy_time(sourcefilename,targetfilename)
   return copy 
#@-node:bwmulder.20041017125718.3:write_if_changed
#@+node:bwmulder.20041017125718.2:is_sentinel
def is_sentinel (line,marker):
   """
   Check if line starts with a Leo marker.
   
   Leo markers are filtered away by this script.
   
   Leo markers start with a comment character, which dependends
   on the language used. That's why the marker is passed in.
   """
   return line.lstrip().startswith(marker)
#@-node:bwmulder.20041017125718.2:is_sentinel
#@+node:bwmulder.20041017125718.6:class sourcereader

   
# The following classes have a very limited functionality. They help write 
# code
# which processes a list of lines slightly more succinctly.
# 
# You might consider expanding the code inline.

class sourcereader:
    """
    A simple class to read lines sequentially.
    
    The class keeps an internal index, so that each
    call to get returns the next line.
    
    Index returns the internal index, and sync
    advances the index to the the desired line.
    
    The index is the *next* line to be returned.
    
    The line numbering starts from 0.
    
    """
    #@	@+others
    #@+node:bwmulder.20041017125718.7:__init__
    def __init__ (self,lines):
       self.lines = lines 
       self.length = len(self.lines)
       self.i = 0
    #@-node:bwmulder.20041017125718.7:__init__
    #@+node:bwmulder.20041017125718.8:index
    def index (self):
       return self.i 
    #@-node:bwmulder.20041017125718.8:index
    #@+node:bwmulder.20041017125718.9:get
    def get (self):
       result = self.lines[self.i]
       self.i+=1
       return result 
    #@-node:bwmulder.20041017125718.9:get
    #@+node:bwmulder.20041017125718.10:sync
    def sync (self,i):
       self.i = i 
    #@-node:bwmulder.20041017125718.10:sync
    #@+node:bwmulder.20041017125718.11:size
    def size (self):
       return self.length 
    #@-node:bwmulder.20041017125718.11:size
    #@+node:bwmulder.20041017125718.12:atEnd
    def atEnd (self):
       return self.index>=self.length 
    #@-node:bwmulder.20041017125718.12:atEnd
    #@+node:bwmulder.20050102143357:clone
    def clone(self):
        sr = sourcereader(self.lines)
        sr.i = self.i
        return sr
    #@nonl
    #@-node:bwmulder.20050102143357:clone
    #@-others
#@-node:bwmulder.20041017125718.6:class sourcereader
#@+node:bwmulder.20041017125718.13:class sourcewriter
class sourcewriter:
    """
    Convenience class to capture output to a file.
    """
    #@	@+others
    #@+node:bwmulder.20041017125718.14:__init__
    def __init__ (self):
       self.i = 0
       self.lines =[]
    #@-node:bwmulder.20041017125718.14:__init__
    #@+node:bwmulder.20041017125718.15:push
    def push (self,line):
       self.lines.append(line)
       self.i+=1
    #@-node:bwmulder.20041017125718.15:push
    #@+node:bwmulder.20041017125718.16:index
    def index (self):
       return self.i 
    #@-node:bwmulder.20041017125718.16:index
    #@+node:bwmulder.20041017125718.17:getlines
    def getlines (self):
       return self.lines 
    #@-node:bwmulder.20041017125718.17:getlines
    #@-others
#@-node:bwmulder.20041017125718.13:class sourcewriter
#@+node:bwmulder.20041017125718.18:push_file
# The following functions filter out Leo comments.
# 
# Push file makes sure that the target file is only touched if there are real 
# differences.
def push_file (sourcefilename,targetfilename):
   outlines, sentinel_lines = push_filter(sourcefilename)
   write_if_changed(outlines,sourcefilename,targetfilename)
#@-node:bwmulder.20041017125718.18:push_file
#@+node:bwmulder.20041017125718.19:push_filter
def push_filter (sourcefilename):
   """
   
   Removes sentinels from the lines of 'sourcefilename'.
   
   """
   
   return push_filter_lines(file(sourcefilename).readlines(),marker_from_extension(sourcefilename))
#@-node:bwmulder.20041017125718.19:push_filter
#@+node:bwmulder.20041017125718.20:push_filter_lines
def push_filter_lines (lines,marker):
   """
   
   Removes sentinels from lines.
   
   """
   result, sentinel_lines =[],[]
   for line in lines:
      if is_sentinel(line,marker):
         sentinel_lines.append(line)
      else:
         result.append(line)
   return result, sentinel_lines 
#@-node:bwmulder.20041017125718.20:push_filter_lines
#@+node:bwmulder.20041017125718.30:push_filter_mapping
def push_filter_mapping (filelines,marker):
   """
   Given the lines of a file, filter out all
   Leo sentinels, and return a mapping:
      
      stripped file -> original file
      
   Filtering should be the same as
   push_filter_lines
   """
   
   mapping =[None]
   for linecount, line in enumerate(filelines):
      if not is_sentinel(line,marker):
         mapping.append(linecount+1)
   return mapping 
#@-node:bwmulder.20041017125718.30:push_filter_mapping
#@+node:bwmulder.20041017125718.35:class writeclass
   
   
   
class writeclass(file):
    """
    Small class to remove the sentinels from the Leo
    file and write the result back to the derived file.
    This happens at the close operation of the file.
    """
    #@	@+others
    #@+node:bwmulder.20041017125718.36:__init__
    def __init__ (self,leofilename,filename):
       self.leo_originalname = filename 
       self.leo_filename = leofilename 
       file.__init__(self,leofilename,'wb')
    #@-node:bwmulder.20041017125718.36:__init__
    #@+node:bwmulder.20041017125718.37:close
    def close (self):
       file.close(self)
       leo_filename, leo_originalname = self.leo_filename, self.leo_originalname 
       assert leo_filename.endswith(".tmp")
       shutil.copy2(leo_filename,leo_filename[:-4])
       # we update regular file in the Leo subdirectory, otherwise structural changes get lost.
       push_file(sourcefilename=self.leo_filename,targetfilename=self.leo_originalname)
       os.unlink(leo_filename)
    #@-node:bwmulder.20041017125718.37:close
    #@-others
#@-node:bwmulder.20041017125718.35:class writeclass
#@-node:bwmulder.20041017130118:auxilary functions
#@+node:bwmulder.20041017125718.21:class sentinel_squasher
# The pull operation is more complicated than the pull operation: we must copy 
# back the sources into a Leo files, making sure that the code is in the 
# proper places between the Leo comments.
   
class sentinel_squasher:
    """
    The heart of the script.
    
    Creates files without sentinels from files with sentinels.
    
    Propagates changes in the files without sentinels back
    to the files with sentinels.
    
    """
    #@	@+others
    #@+node:bwmulder.20041017125718.22:check_lines_for_equality
    def check_lines_for_equality (self,lines1,lines2,message,lines1_message,lines2_message):
       """
       Little helper function to get nice output if something goes wrong.
       """
       if lines1==lines2:
          return 
       print "================================="
       print message 
       print "================================="
       print lines1_message 
       print "---------------------------------"
       f1 = file("mod_shadow.tmp1", "w")
       for line in lines1:
          print line, 
          f1.write(line)
       f1.close()
       print "=================================="
       print lines2_message 
       print "---------------------------------"
       f1 = file("mod_shadow.tmp2", "w")
       for line in lines2:
          print line, 
          f1.write(line)
       f1.close()
       g.es("'push' did not re-create the output file; please check mod_shadow.tmp1 and mod_shadow.tmp2 for differences")
    #@-node:bwmulder.20041017125718.22:check_lines_for_equality
    #@+node:bwmulder.20041017125718.23:create_back_mapping
    def create_back_mapping (self,sourcelines,marker):
       """
    
       'sourcelines' is a list of lines of a file with sentinels.
    
       Creates a new list of lines without sentinels, and keeps a
       mapping which maps each source line in the new list back to its
       original line.
    
       Returns the new list of lines, and the mapping.
    
       To save an if statement later, the mapping is extended by one
       extra element.
    
       """
       mapping, resultlines =[],[]
    
       si, l = 0, len(sourcelines)
       while si<l:
          sline = sourcelines[si]
          if not is_sentinel(sline,marker):
             resultlines.append(sline)
             mapping.append(si)
          si+=1
    
       # for programing convenience, we create an additional mapping entry.
       # This simplifies the programming of the copy_sentinels function below.
       mapping.append(si)
       return resultlines, mapping 
    #@-node:bwmulder.20041017125718.23:create_back_mapping
    #@+node:bwmulder.20041017125718.24:copy_sentinels
    def copy_sentinels (self,writer_new_sourcefile,reader_leo_file,mapping,startline,endline, sentinels_to_copy):
        """
        
        Sentinels are NEVER deleted by this script. They are changed as
        a result of user actions in the Leo.
        
        If code is replaced, or deleted, then we must make sure that the
        sentinels are still in the Leo file.
        
        Taking lines from reader_leo_file, we copy lines to writer_new_sourcefile, 
        if those lines contain sentinels.
        
        We copy all sentinels up to, but not including, mapped[endline].
        
        We copy only the sentinels *after* the current position of reader_leo_file.
        
        We have two options to detect sentinel lines:
          1. We could detect sentinel lines by examining the lines of the leo file.
          2. We can check for gaps in the mapping.
         
        Since there is a complication in the detection of sentinels (@verbatim), we
        are choosing the 2. approach. This also avoids duplication of code.
        ???This has to be verified later???
        """
        
        old_mapped_line = mapping[startline]
        unmapped_line = startline+1
        
        sentinels_copied = 0
        while unmapped_line<=endline:
            mapped_line = mapping[unmapped_line]
            if old_mapped_line+1!=mapped_line:
                reader_leo_file.sync(old_mapped_line+1)
                # There was a gap. This gap must have consisted of sentinels, which have
                # been deleted.
                # Copy those sentinels.
                while reader_leo_file.index()<mapped_line:
                    line = reader_leo_file.get()
                    if sentinels_to_copy> 0:
                        if testing:
                            print "Copy sentinel:", line
                        writer_new_sourcefile.push(line)
                    elif sentinels_to_copy == 0:
                        self.uncopied_sentinels.append(line)
                        if testing:
                            print "Delay Copy sentinels:", line,
                sentinels_to_copy -= 1
                sentinels_copied += 1
                old_mapped_line = mapped_line 
            unmapped_line+=1
        reader_leo_file.sync(mapping[endline])
        return sentinels_copied
        
    #@nonl
    #@-node:bwmulder.20041017125718.24:copy_sentinels
    #@+node:bwmulder.20050102142213.1:copy_all_but_last_sentinel_block
    def copy_all_but_last_sentinel_block (self,writer_new_sourcefile,reader_leo_file,mapping,startline,endline):
        """
        Copy all but the last sentinel block.
        
        Put the last sentinel block into self.uncopied_sentinels
        """
        self.uncopied_sentinels = []
        if testing:
            print "copy_all_but_last_sentinel_block: dry run"
        nr_sentinel_blocks = self.copy_sentinels(g.nullObject(), reader_leo_file.clone(), mapping, startline, endline, -1)
        if testing:
            print "copy_all_but_last_sentinel_block: Actual copy",nr_sentinel_blocks -1
        self.copy_sentinels(writer_new_sourcefile, reader_leo_file, mapping, startline, endline, nr_sentinel_blocks -1)
    #@nonl
    #@-node:bwmulder.20050102142213.1:copy_all_but_last_sentinel_block
    #@+node:bwmulder.20050102142213.2:copy_delayed_sentinel_block
    def copy_delayed_sentinel_block(self, writer_new_sourcefile):
        if testing:
            if self.uncopied_sentinels:
                print "Copying uncopied sentinels"
        for line in self.uncopied_sentinels:
            writer_new_sourcefile.push(line)
        self.uncopied_sentinels = []
    #@nonl
    #@-node:bwmulder.20050102142213.2:copy_delayed_sentinel_block
    #@+node:bwmulder.20041017125718.25:pull_source
    def pull_source (self,sourcefile,targetfile):
        """
        Propagate the changes of targetfile back to sourcefile.
        Assume that sourcefile has sentinels, and targetfile does not.
        This is the heart of the script.
        """
        if testing: g.trace(sourcefile, targetfile)
        #@    << init vars >>
        #@+node:ekr.20041110094810:<< init vars >>
        marker = marker_from_extension(sourcefile)
        sourcelines = file(sourcefile).readlines()
        targetlines = file(targetfile).readlines()
        
        internal_sourcelines, mapping = self.create_back_mapping(sourcelines,marker)
        
        sm = difflib.SequenceMatcher(None,internal_sourcelines,targetlines)
        
        writer_new_sourcefile = sourcewriter()
        # collects the contents of the new file.
        
        reader_modified_file = sourcereader(targetlines)
        # reader_modified_file contains the changed source code.
        # There are no sentinels in 'targetlines'
        
        reader_internal_file = sourcereader(internal_sourcelines)
        # This is the same file as reader_leo_file, without sentinels.
        
        reader_leo_file = sourcereader(sourcelines)
        # This is the file which is currently produced by Leo, with sentinels.
        
        #@+at 
        #@nonl
        # We compare the 'targetlines' with 'internal_sourcelines' and 
        # propagate
        # the changes back into 'writer_new_sourcefile' while making sure that
        # all sentinels of 'sourcelines' are copied as well.
        # 
        # An invariant of the following loop is that all three readers are in 
        # sync.
        # In addition, writer_new_sourcefile has accumulated the new file, 
        # which
        # is going to replace reader_leo_file.
        #@-at
        #@@c
        
        # Check that all ranges returned by get_opcodes() are contiguous
        i2_internal_old, i2_modified_old = -1,-1
        
        self.uncopied_sentinels = []
        # The copying of the last sentinel block is delayed: if
        # an insert follows, then the insert is done before the sentinel
        # block is copied.
        # This way, the insertion can happen *inside* the sentinels, not outside.
        #@nonl
        #@-node:ekr.20041110094810:<< init vars >>
        #@nl
        #@    << copy the sentinels at the beginning of the file >>
        #@+node:ekr.20041110095546:<< copy the sentinels at the beginning of the file >>
        while reader_leo_file.index()<mapping[0]:
            line = reader_leo_file.get()
            writer_new_sourcefile.push(line)
        #@nonl
        #@-node:ekr.20041110095546:<< copy the sentinels at the beginning of the file >>
        #@nl
        for tag, i1_internal_file, i2_internal_file, i1_modified_file, i2_modified_file in sm.get_opcodes():
            #@        << trace the params >>
            #@+node:ekr.20041110094555:<< trace the params >>
            if testing:
                print "tag:", tag,\
                    "i1, i2 (internal file):", i1_internal_file, i2_internal_file,\
                    "i1, i2 (modified file)",  i1_modified_file, i2_modified_file
            #@nonl
            #@-node:ekr.20041110094555:<< trace the params >>
            #@nl
            #@        << check loop invariants >>
            #@+node:ekr.20041110094555.1:<< check loop invariants >>
            # We need the ranges returned by get_opcodes to completely cover the source lines being compared.
            # We also need the ranges not to overlap.
            if i2_internal_old!=-1:
             assert i2_internal_old==i1_internal_file 
             assert i2_modified_old==i1_modified_file 
            i2_internal_old, i2_modified_old = i2_internal_file, i2_modified_file 
            #@+at
            # Loosely speaking, the loop invariant is that we have processed 
            # everything up to,
            # but not including, the lower bound of the ranges returned by the 
            # iterator.
            # 
            # We have to check the three readers, reader_internal_file,
            # reader_modified_file, and reader_leo_file.
            # 
            # For the writer, the filter must reproduce the modified file
            # up until, but not including, i1_modified_file.
            # 
            # In addition, all the sentinels of the original Leo file, up 
            # until
            # mapping[i1_internal_file], must be present in the 
            # new_source_file.
            #@-at
            #@@c
            
            # Check the loop invariant.
            assert reader_internal_file.i==i1_internal_file 
            assert reader_modified_file.i==i1_modified_file 
            assert reader_leo_file.i==mapping[i1_internal_file]
            
            # These checks are a little bit costly.
            if testing and 0:
                # Must check if that still holds.
                t_sourcelines, t_sentinel_lines = push_filter_lines(writer_new_sourcefile.lines,marker)
                # Check that we have all the modifications so far.
                assert t_sourcelines==reader_modified_file.lines[:i1_modified_file]
                # Check that we kept all sentinels so far.
                assert t_sentinel_lines==push_filter_lines(reader_leo_file.lines[:reader_leo_file.i],marker)[1]
            #@nonl
            #@-node:ekr.20041110094555.1:<< check loop invariants >>
            #@nl
            if tag=='equal':
                #@            << handle 'equal' op >>
                #@+node:ekr.20041110095546.1:<< handle 'equal' op >>
                # nothing is to be done. Leave the Leo file alone.
                
                self.copy_delayed_sentinel_block(writer_new_sourcefile)
                # Copy the lines from the leo file to the new sourcefile.
                # This loop copies both text and sentinels.
                while reader_leo_file.index()<=mapping[i2_internal_file-1]:
                   line = reader_leo_file.get()
                   if testing:
                      print "Equal: copying ", line, 
                   writer_new_sourcefile.push(line)
                
                if testing:
                   print "Equal: syncing internal file from ", reader_internal_file.i, " to ", i2_internal_file 
                   print "Equal: syncing modified  file from ", reader_modified_file.i, " to ", i2_modified_file 
                reader_internal_file.sync(i2_internal_file)
                reader_modified_file.sync(i2_modified_file)
                
                # now we must copy the sentinels which might follow the lines which were equal.
                self.copy_all_but_last_sentinel_block(writer_new_sourcefile,reader_leo_file,mapping,i2_internal_file-1,i2_internal_file)
                #@nonl
                #@-node:ekr.20041110095546.1:<< handle 'equal' op >>
                #@nl
            elif tag=='replace':
                #@            << handle 'replace' op >>
                #@+node:ekr.20041110095546.2:<< handle 'replace' op >>
                #@+at 
                #@nonl
                # We have to replace lines that span several sections of 
                # sentinels.
                # 
                # For now, we put all the new contents after the first 
                # sentinels.
                # Different strategies may be possible later.
                # 
                # We might, for example, run the difflib across the different
                # lines and try to construct a mapping changed line => orignal 
                # line.
                #@-at
                #@@c
                self.copy_delayed_sentinel_block(writer_new_sourcefile)
                
                while reader_modified_file.index()<i2_modified_file:
                   line = reader_modified_file.get()
                   if testing:
                      print "Replace: copy modified line:", line, 
                   writer_new_sourcefile.push(line)
                
                # Take care of the sentinels which might be between the changed code.         
                self.copy_all_but_last_sentinel_block(writer_new_sourcefile,reader_leo_file,mapping,i1_internal_file,i2_internal_file)
                reader_internal_file.sync(i2_internal_file)
                #@nonl
                #@-node:ekr.20041110095546.2:<< handle 'replace' op >>
                #@nl
            elif tag=='delete':
                #@            << handle 'delete' op >>
                #@+node:ekr.20041110095546.3:<< handle 'delete' op >>
                # We have to delete lines.
                # However, we NEVER delete sentinels, so they must be copied over.
                
                # sync the readers
                self.copy_delayed_sentinel_block(writer_new_sourcefile)
                
                if testing:
                    print "delete: syncing modified file from ", reader_modified_file.i, " to ", i1_modified_file 
                    print "delete: syncing internal file from ", reader_internal_file.i, " to ", i1_internal_file
                
                reader_modified_file.sync(i2_modified_file)
                reader_internal_file.sync(i2_internal_file)
                
                self.copy_all_but_last_sentinel_block(writer_new_sourcefile,reader_leo_file,mapping,i1_internal_file,i2_internal_file)
                #@nonl
                #@-node:ekr.20041110095546.3:<< handle 'delete' op >>
                #@nl
            elif tag=='insert':
                #@            << handle 'insert' op >>
                #@+node:ekr.20041110095546.4:<< handle 'insert' op >>
                
                while reader_modified_file.index()<i2_modified_file:
                   line = reader_modified_file.get()
                   if testing:
                      print "insert: copy line:", line, 
                   writer_new_sourcefile.push(line)
                
                # Since (only) lines are inserted, we do not have to reposition any reader.
                self.copy_delayed_sentinel_block(writer_new_sourcefile)
                
                #@-node:ekr.20041110095546.4:<< handle 'insert' op >>
                #@nl
            else: assert 0
        #@    << copy the sentinels at the end of the file >>
        #@+node:ekr.20041110095546.6:<< copy the sentinels at the end of the file >>
        self.copy_delayed_sentinel_block(writer_new_sourcefile)
        
        while reader_leo_file.index()<reader_leo_file.size():
            writer_new_sourcefile.push(reader_leo_file.get())
        #@-node:ekr.20041110095546.6:<< copy the sentinels at the end of the file >>
        #@nl
        written = write_if_changed(writer_new_sourcefile.getlines(),targetfile,sourcefile)
        if written:
          #@      << check that the output makes sense >>
          #@+node:ekr.20041110095546.5:<< check that the output makes sense >>
          #@+at 
          #@nonl
          # We check two things:
          # - Applying a 'push' operation will produce the modified file.
          # - Our new sourcefile still has the same sentinels as the replaced 
          # one.
          #@-at
          #@@c
          
          s_outlines, sentinel_lines = push_filter(sourcefile)
          
          # Check that 'push' will re-create the changed file.
          self.check_lines_for_equality(
              s_outlines,targetlines,
              "Pull did not work as expected (source: %s, target: %s):" % (sourcefile, targetfile),
              "Content of sourcefile:",
              "Content of modified file:")
          
          # Check that no sentinels got lost.
          old_sentinel_lines = push_filter_lines(reader_leo_file.lines[:reader_leo_file.i],marker)[1]
          self.check_lines_for_equality(
              sentinel_lines,old_sentinel_lines,
              "Pull modified sentinel lines (source: %s, target: %s):" % (sourcefile, targetfile),
              "Current sentinel lines:",
              "Old sentinel lines:")
          #@nonl
          #@-node:ekr.20041110095546.5:<< check that the output makes sense >>
          #@nl
    #@nonl
    #@-node:bwmulder.20041017125718.25:pull_source
    #@-others
#@-node:bwmulder.20041017125718.21:class sentinel_squasher
#@-node:bwmulder.20041018233934.1:plugin core
#@+node:bwmulder.20041018233934.2:interface
#@+node:bwmulder.20041019071205:plugin specific functions
#@+node:bwmulder.20041017125718.27:putInHooks
def putInHooks ():
    """Modify methods in Leo's core to support this plugin."""
    
    # Need to modify Leos Kernel first
    # Overwrite existing Leo methods.
    g.funcToMethod(replaceTargetFileIfDifferent,leoAtFile.atFile)
    g.funcToMethod(massageComment,leoImport.leoImportCommands)

    # Add new methods used by this plugin to various classes.
    g.funcToMethod(openForRead,leoAtFile.atFile)
    g.funcToMethod(openForWrite,leoAtFile.atFile)
    g.funcToMethod(gotoLineNumberOpen,leoCommands.Commands)
    g.funcToMethod(applyLineNumberMappingIfAny, leoCommands.Commands)
#@-node:bwmulder.20041017125718.27:putInHooks
#@+node:bwmulder.20041017125718.26:applyConfiguration
def applyConfiguration (config=None):

    """Called when the user presses the "Apply" button on the Properties form.
   
    Not sure yet if we need configuration options for this plugin."""

    global active, testing, print_copy_operations, do_backups, shadow_subdir, verbosity, prefix
   
    if config is None:
        fileName = os.path.join(g.app.loadDir,"..","plugins","mod_shadow.ini")
        if os.path.exists(fileName):
            config = ConfigParser.ConfigParser()
            config.read(fileName)
    if config:
        active = config.getboolean("Main","Active")
        testing = config.getboolean("Main", "testing")
        verbosity = config.getint("Main", "verbosity")
        prefix = config.get("Main", "prefix")
        print_copy_operations = config.get("Main", "print_copy_operations")
        shadow_subdir = config.get("Main", "shadow_subdir")

#@-node:bwmulder.20041017125718.26:applyConfiguration
#@+node:bwmulder.20041017184636:check_for_shadow_file
def check_for_shadow_file (self,filename):
    """
    Check if there is a shadow file for filename.
    Return:
        - the name of the shadow file,
        - an indicator if the file denoted by 'filename' is
        of zero length.
    """
    dir, simplename = os.path.split(filename)
    rootname, ext = os.path.splitext(simplename)
    if ext=='.tmp':
        shadow_filename = os.path.join(dir,shadow_subdir,prefix + rootname)
        if os.path.exists(shadow_filename):
            resultname = os.path.join(dir,shadow_subdir,prefix + simplename)
            return resultname, False 
        else:
            return '', False 
    else:
        shadow_filename = os.path.join(dir,shadow_subdir,prefix + simplename)
        if os.path.exists(shadow_filename):
            return shadow_filename, os.path.getsize(filename)<= 2
        else:
            return '', False 
#@-node:bwmulder.20041017184636:check_for_shadow_file
#@-node:bwmulder.20041019071205:plugin specific functions
#@+node:bwmulder.20041019071909:additional core functions
#@+node:bwmulder.20041017135327:openForRead
def openForRead (self,filename,rb):
    """
    Replaces the standard open for reads.
    Checks and handles shadow files:
        if the length of the real file is zero:
            update the real file from the shadow file.
        else:
            update the shadow file from the real file.
    """
    try:
        dir, simplename = os.path.split(filename)
        shadow_filename = os.path.join(dir,shadow_subdir,prefix + simplename)
        if os.path.exists(shadow_filename):
            file_to_read_from = shadow_filename 
            if os.path.exists(filename)and os.path.getsize(filename)<=2:
                if verbosity >= 2:
                    g.es("Copy %s to %s without sentinels"%(shadow_filename,filename))
                push_file(sourcefilename=shadow_filename,targetfilename=filename)
            else:
                sq = sentinel_squasher()
                if verbosity >= 2:
                    g.es("reading in shadow directory %s"% shadow_subdir,color="orange")
                sq.pull_source(sourcefile=shadow_filename,targetfile=filename)
        else:
            file_to_read_from = filename 
        return open(file_to_read_from,'rb')
    except:
        # Make sure failures to open a file generate clear messages.
        g.es_exception()
        raise 
#@nonl
#@-node:bwmulder.20041017135327:openForRead
#@+node:bwmulder.20041017131319:openForWrite
def openForWrite (self,filename,wb):
    """
    Replaces the standard open for writes:
        - Check if filename designates a file
          which has a shadow file.
          If so, write to the shadow file,
          and update the real file after the close.
    """
    dir, simplename = os.path.split(filename)
    rootname, ext = os.path.splitext(simplename)
    assert ext=='.tmp'
    shadow_filename = os.path.join(dir,shadow_subdir,prefix + rootname)
    self.writing_to_shadow_directory = os.path.exists(shadow_filename)
    if self.writing_to_shadow_directory:
        self.shadow_filename = shadow_filename 
        if verbosity >= 2: 
            g.es("Using shadow file in folder %s" % shadow_subdir,color="orange")
        file_to_use = os.path.join(dir,shadow_subdir,prefix + simplename)
    else:
        file_to_use = filename 
    return open(file_to_use,'wb')
#@-node:bwmulder.20041017131319:openForWrite
#@+node:bwmulder.20041018075528:gotoLineNumberOpen
def gotoLineNumberOpen (self,filename):
    """
    Open a file for "goto linenumber" command and check if a shadow file exists.
    Construct a line mapping. This line_mapping instance variable is empty if
    no shadow file exist, otherwise it contains a mapping 
    shadow file number -> real file number.
    """
    try:
        dir, simplename = os.path.split(filename)
        shadow_filename = os.path.join(dir,shadow_subdir,prefix + simplename)
        if os.path.exists(shadow_filename):
            lines = file(shadow_filename).readlines()
            self.line_mapping = push_filter_mapping(lines,marker_from_extension(simplename))
        else:
            self.line_mapping ={}
            lines = file(filename).readlines()
        return lines 
    except:
        # Make sure failures to open a file generate clear messages.
        g.es_exception()
        raise
#@nonl
#@-node:bwmulder.20041018075528:gotoLineNumberOpen
#@-node:bwmulder.20041019071909:additional core functions
#@+node:bwmulder.20041019071205.1:Leo overwrites
#@+node:bwmulder.20041231222931:gotoLineNumber
#@+node:bwmulder.20041231222931.1:applyLineNumberMappingIfAny
def applyLineNumberMappingIfAny(self, n):
    """
    Hook for mod_shadow plugin.
    """
    if self.line_mapping:
        return self.line_mapping[n]
    else:
        return n
#@nonl
#@-node:bwmulder.20041231222931.1:applyLineNumberMappingIfAny
#@-node:bwmulder.20041231222931:gotoLineNumber
#@+node:bwmulder.20041019071205.3:writing
#@+doc 
# Just like for reading, we redirect the writing to the shadow file, if
# one is there.
# 
# Writing is slightly more complicated by the fact
# that Leo writes the information first to a
# temporary file, before renaming the temporary file
# to the real filename.
# 
# We must therefore patch in two places:
#     -When the temporary file is written(openWriteFile)
#     -When Leo renames the file(replaceTargetFileIfDifferent).
#@-doc
#@nonl
#@+node:bwmulder.20041018224835:atFile.replaceTargetFileIfDifferent
original_replaceTargetFileIfDifferent = leoAtFile.atFile.replaceTargetFileIfDifferent

def replaceTargetFileIfDifferent (self):
    
    # Check if we are dealing with a shadow file
    try:
        targetFileName = self.targetFileName 
        outputFileName = self.outputFileName 
        if self.writing_to_shadow_directory:
            self.targetFileName = self.shadow_filename 
            self.outputFileName = self.shadow_filename+'.tmp'
        if original_replaceTargetFileIfDifferent(self):
            # Original_replaceTargetFileIfDifferent should be oblivious
            # to the existance of the shadow directory.
            if self.writing_to_shadow_directory:
                if verbosity >= 2:
                    g.es("Updating file from shadow folder %s" % shadow_subdir,color='orange')
                push_file(self.shadow_filename,targetFileName)

    finally:
        if self.writing_to_shadow_directory:
            assert self.targetFileName == self.shadow_filename 
            assert self.outputFileName == self.shadow_filename+'.tmp'
        else:
            assert self.targetFileName == targetFileName
            assert self.outputFileName == outputFileName
            # We need to check what's going on if the targetFileName or the outputFileName is changed.
        
        # Not sure if this finally clause is needed or not
        self.targetFileName = targetFileName
        self.outputFileName = outputFileName 
#@nonl
#@-node:bwmulder.20041018224835:atFile.replaceTargetFileIfDifferent
#@-node:bwmulder.20041019071205.3:writing
#@+node:bwmulder.20041017125718.33:massageComment
def massageComment (self,s):

	"""Leo has no busines changing comments!"""

	return s 
#@-node:bwmulder.20041017125718.33:massageComment
#@-node:bwmulder.20041019071205.1:Leo overwrites
#@-node:bwmulder.20041018233934.2:interface
#@+node:bwmulder.20041017125718.39:stop_testing
def stop_testing ():
   global testing 
   testing = False 
#@-node:bwmulder.20041017125718.39:stop_testing
#@+node:bwmulder.20050120235957:main
def main():
    global active, verbosity
try:
    g.app
    assert g.app is not None
    # if g.app is not defined, we are not
    # imported from Leo
except:
    active = False
else:
    applyConfiguration()

if active and not g.app.unitTesting: # Not safe for unit testing: changes Leo's core.
   putInHooks() # Changes Leo's core.
   # leoPlugins.registerHandler("idle", autosave)
   if verbosity >= 1:
      g.es("Shadow plugin enabled!",color="orange")
    
#@nonl
#@-node:bwmulder.20050120235957:main
#@-others

main()
#@nonl
#@-node:bwmulder.20041017125718:@thin mod_shadow.py
#@-leo
