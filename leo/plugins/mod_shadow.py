#@+leo-ver=4-thin
#@+node:bwmulder.20041017125718:@thin ../plugins/mod_shadow.py
#@@language python
#@+others
#@+node:bwmulder.20041017125718.1:docstring
"""
THIS PLUGIN IS NOT YET WORKING!

DON'T USE IT!

By Bernhard Mulder

Use a LEO subfolder for files with LEO comments.

This is experimental code.

The hookup with LEO is not satisfactory. I am missing suitable hooks for implementing
an input / output filter, and the read / write functions
are too big to overwrite.

The goToLineNumber has been copied from 4.1, with the
insertions marked by bwm:.

I do not know how to avoid the code duplication.

To start using this plugin, check the standalone
script sentinel.py.
   
As soon as you modify a file, the plugin will update
your files in the usual place.

The plugin has special code to deal with 0 length derived files.
"""
#@-node:bwmulder.20041017125718.1:docstring
#@+node:bwmulder.20041017130018:imports
import leoPlugins
import leoGlobals as g

from ConfigParser import ConfigParser
from difflib      import SequenceMatcher
import sys, os, shutil, inspect

from leoGlobals import es, scanDirectives, os_path_join, app, skip_ws, match

import leoCommands, leoImport

from leoAtFile import atFile, newDerivedFile
from leoFileCommands import fileCommands

# Here is the code which removes sentinels, and propagates changes back from a 
# sentinel free file to a file with sentinels.
# 
# The code can be used either in a free standing script, or integrated with 
# Leo.
# 
# In this context, 'push' means creating a file without sentinels from a file 
# with sentinels.
# 
# 'pull' means propagating changes back from a file without sentinels to a 
# file with sentinels.
# A small collection of useful routines and classes which
# are not directly tied to the purpose of this plugin.
#@-node:bwmulder.20041017130018:imports
#@+node:bwmulder.20041018233934:old code
#@+node:bwmulder.20041017125718.34:read_old
def read(leofilename, filename):
   """
   Loefilename is the name of the LEO File.
   Filename is the name of the file specified by the user.
   """
   sq = sentinel_squasher()
   # special check for filelength 0:
   if os.path.getsize(filename) == 0:
      # assume that we have to copy the file leofilename to
      # filename.
      es("Copy %s to %s without sentinels" % (leofilename, filename))
      push_file(sourcefilename=leofilename, targetfilename=filename)
   else:
      sq.pull_source(sourcefile = leofilename, targetfile = filename)
   return open(leofilename, 'rb')
#@-node:bwmulder.20041017125718.34:read_old
#@+node:bwmulder.20041017125718.38:write_old
def write(leofilename, filename):
   """
   Loefilename is the name of the LEO File.
   Filename is the name of the file specified by the user.
   This case is slightly more complicated:
      everything must be done at the close.
   """
   return writeclass(leofilename, filename) 
#@-node:bwmulder.20041017125718.38:write_old
#@+node:bwmulder.20041017125718.32:goToLineNumber_4.1
def goToLineNumber (self):

   c = self ; v = c.currentVnode()
   # Search the present node first.
   j = v.t.joinList
   if v in j:
      j.remove(v)
   j.insert(0,v)
   
   # 10/15/03: search joined nodes if first search fails.
   root = None ; fileName = None
   for v in j:
      while v and not fileName:
         if v.isAtFileNode():
            fileName = v.atFileNodeName()
         elif v.isAtSilentFileNode():
            fileName = v.atSilentFileNodeName()
         elif v.isAtRawFileNode():
            fileName = v.atRawFileNodeName()
         else:
            v = v.parent()
      if fileName:
         root = v
         # trace("root,fileName",root,fileName)
         break # Bug fix: 10/25/03
   if not root:
      es("Go to line number: ancestor must be @file node", color="blue")
      return
   # 1/26/03: calculate the full path.
   d = scanDirectives(c)
   path = d.get("path")
   
   fileName = os_path_join(path,fileName)
   
   dir, simple_filename = os.path.split(fileName)
   leo_subfolder_filename = os.path.join(dir, 'Leo', simple_filename)
   leo_subfolder = os.path.exists(leo_subfolder_filename)
   if leo_subfolder:
      fileName = leo_subfolder_filename
   try:
      file=open(fileName)
      lines = file.readlines()
      file.close()
   except:
      es("not found: " + fileName)
      return
      
   if leo_subfolder:
      line_mapping = push_filter_mapping(lines, marker_from_extension(leo_subfolder_filename))
   n = app.gui.runAskOkCancelNumberDialog("Enter Line Number","Line number:")
   if n == -1:
      return
   # trace("n:"+`n`)
   if n==1:
      v = root ; n2 = 1 ; found = true
   elif n >= len(lines):
      v = root ; found = false
      n2 = v.bodyString().count('\n')
   elif root.isAtSilentFileNode():
      v = lastv = root ; after = root.nodeAfterTree()
      prev = 0 ; found = false
      while v and v != after:
         lastv = v
         s = v.bodyString()
         lines = s.count('\n')
         if len(s) > 0 and s[-1] != '\n':
            lines += 1
         # print lines,prev,v
         if prev + lines >= n:
            found = true ; break
         prev += lines
         v = v.threadNext()
      
      v = lastv
      n2 = max(1,n-prev)
   else:
      if leo_subfolder:
         n = line_mapping[n]
      vnodeName,childIndex,n2,delim = self.convertLineToVnodeNameIndexLine(lines,n,root)
      found = true
      if not vnodeName:
         es("invalid derived file: " + fileName)
         return
      after = root.nodeAfterTree()
      
      if childIndex == -1:
         # This is about the best that can be done without replicating the entire atFile write logic.
         
         ok = true
         
         if not hasattr(root,"tnodeList"):
            s = "no child index for " + root.headString()
            print s ; es(s, color="red")
            ok = false
         
         if ok:
            tnodeList = root.tnodeList
            tnodeIndex = -1 # Don't count the @file node.
            scanned = 0 # count of lines scanned.
            
            for s in lines:
               if scanned >= n:
                  break
               i = skip_ws(s,0)
               if match(s,i,delim):
                  i += len(delim)
                  if match(s,i,"+node"):
                     # trace(tnodeIndex,s.rstrip())
                     tnodeIndex += 1
               scanned += 1
            tnodeIndex = max(0,tnodeIndex)
            # We use the tnodeList to find a _tnode_ corresponding to the 
            # proper node, so the user will for sure be editing the proper 
            # text, even if several nodes happen to have the same headline.  
            # This is really all that we need.
            # 
            # However, this code has no good way of distinguishing between 
            # different cloned vnodes in the file: they all have the same 
            # tnode.  So this code just picks v = t.joinList[0] and leaves it 
            # at that.
            # 
            # The only way to do better is to scan the outline, replicating 
            # the write logic to determine which vnode created the given 
            # line.  That's way too difficult, and it would create an unwanted 
            # dependency in this code.
            
            # trace("tnodeIndex",tnodeIndex)
            if tnodeIndex < len(tnodeList):
               t = tnodeList[tnodeIndex]
               # Find the first vnode whose tnode is t.
               v = root
               while v and v != after:
                  if v.t == t:
                     break
                  v = v.threadNext()
               if not v:
                  s = "tnode not found for " + vnodeName
                  print s ; es(s, color="red") ; ok = false
               elif v.headString().strip() != vnodeName:
                  if 0: # Apparently this error doesn't prevent a later scan for working properly.
                     s = "Mismatched vnodeName\nExpecting: %s\n got: %s" % (v.headString(),vnodeName)
                     print s ; es(s, color="red")
                  ok = false
            else:
               s = "Invalid computed tnodeIndex: %d" % tnodeIndex
               print s ; es(s, color = "red") ; ok = false
                  
         if not ok:
            # Fall back to the old logic.
            v = root
            while v and v != after:
               if v.matchHeadline(vnodeName):
                  break
               v = v.threadNext()
            
            if not v or v == after:
               s = "not found: " + vnodeName
               print s ; es(s, color="red")
               return
      else:
         v = root
         while v and v != after:
            if v.matchHeadline(vnodeName):
               if childIndex <= 0 or v.childIndex() + 1 == childIndex:
                  break
            v = v.threadNext()
         
         if not v or v == after:
            es("not found: " + vnodeName, color="red")
            return
   c.beginUpdate()
   c.frame.tree.expandAllAncestors(v)
   c.selectVnode(v)
   c.endUpdate()
   if found:
      c.frame.body.setInsertPointToStartOfLine(n2-1)
   else:
      c.frame.body.setInsertionPointToEnd()
      es("%d lines" % len(lines), color="blue")
   
   c.frame.body.makeInsertPointVisible()
#@-node:bwmulder.20041017125718.32:goToLineNumber_4.1
#@-node:bwmulder.20041018233934:old code
#@+node:bwmulder.20041018233934.1:plugin core
#@+node:bwmulder.20041017130118:auxilary functions
#@+node:bwmulder.20041017125718.4:copy_time
def copy_time(sourcefilename, targetfilename):
   """
   Set the modification time of the targetfile the same
   as the sourcefilename
   """
   st = os.stat(sourcefilename)
   if hasattr(os, 'utime'):
      os.utime(targetfilename, (st.st_atime, st.st_mtime))
   elif hasattr(os, 'mtime'):
      os.mtime(targetfilename, st.st_mtime)
   else:
      assert 0, "Sync operation can't work if no modification time can be set"
#@-node:bwmulder.20041017125718.4:copy_time
#@+node:bwmulder.20041017125718.5:marker_from_extension
def marker_from_extension(filename):
   """
   Tries to guess the sentinel leadin
   comment from the filename extension.
   
   This code should probably be shared
   with the main Leo code.
   """
   root, ext = os.path.splitext(filename)
   if ext == '.tmp':
      root, ext = os.path.splitext(root)
   if ext in ('.h', '.c'):
      marker = "//@"
   elif ext in (".py", ".cfg", ".bat", ".ksh"):
      marker = '#' + '@'
   else:
      assert 0, "extension %s not handled by this plugin" % ext
   return marker
#@-node:bwmulder.20041017125718.5:marker_from_extension
#@+node:bwmulder.20041017125718.3:write_if_changed
def write_if_changed(lines, sourcefilename, targetfilename):
   """
   
   Checks if 'lines' matches the contents of
   'targetfilename'. Refreshes the targetfile with 'lines' if not.

   Produces a message, if wanted, about the overrite, and optionally
   keeps the overwritten file with a backup name.

   """
   if not os.path.exists(targetfilename):
      copy = True
   else:
      copy = lines != file(targetfilename).readlines()
   if copy:
      if print_copy_operations:
         print "Copying ", sourcefilename, " to ", targetfilename, " without sentinals"

      if do_backups:
         # Keep the old file around while we are debugging this script
         if os.path.exists(targetfilename):
            count = 0
            backupname = "%s.~%s~" % (targetfilename, count)
            while os.path.exists(backupname):
               count += 1
               backupname = "%s.~%s~" % (targetfilename, count)
            os.rename(targetfilename, backupname)
            if print_copy_operations:
               print "backup file in ", backupname
      outfile = open(targetfilename, "w")
      for line in lines:
         outfile.write(line)
      outfile.close()
      copy_time(sourcefilename, targetfilename)
   return copy
#@-node:bwmulder.20041017125718.3:write_if_changed
#@+node:bwmulder.20041017125718.2:is_sentinel
def is_sentinel(line, marker):
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
    def __init__(self, lines):
       self.lines = lines
       self.length = len(self.lines)
       self.i = 0
    #@-node:bwmulder.20041017125718.7:__init__
    #@+node:bwmulder.20041017125718.8:index
    def index(self):
       return self.i
    #@-node:bwmulder.20041017125718.8:index
    #@+node:bwmulder.20041017125718.9:get
    def get(self):
       result = self.lines[self.i]
       self.i += 1
       return result
    #@-node:bwmulder.20041017125718.9:get
    #@+node:bwmulder.20041017125718.10:sync
    def sync(self, i):
       self.i = i
    #@-node:bwmulder.20041017125718.10:sync
    #@+node:bwmulder.20041017125718.11:size
    def size(self):
       return self.length
    #@-node:bwmulder.20041017125718.11:size
    #@+node:bwmulder.20041017125718.12:atEnd
    def atEnd(self):
       return self.index >= self.length
    #@-node:bwmulder.20041017125718.12:atEnd
    #@-others
#@-node:bwmulder.20041017125718.6:class sourcereader
#@+node:bwmulder.20041017125718.13:class sourcewriter
class sourcewriter:
    """
    Convenience class to capture output to a file.
    """
    #@	@+others
    #@+node:bwmulder.20041017125718.14:__init__
    def __init__(self):
       self.i = 0
       self.lines = []
    #@-node:bwmulder.20041017125718.14:__init__
    #@+node:bwmulder.20041017125718.15:push
    def push(self, line):
       self.lines.append(line)
       self.i += 1
    #@-node:bwmulder.20041017125718.15:push
    #@+node:bwmulder.20041017125718.16:index
    def index(self):
       return self.i
    #@-node:bwmulder.20041017125718.16:index
    #@+node:bwmulder.20041017125718.17:getlines
    def getlines(self):
       return self.lines
    #@-node:bwmulder.20041017125718.17:getlines
    #@-others
#@-node:bwmulder.20041017125718.13:class sourcewriter
#@+node:bwmulder.20041017125718.18:push_file
# The following functions filter out Leo comments.
# 
# Push file makes sure that the target file is only touched if there are real 
# differences.
def push_file(sourcefilename, targetfilename):
   outlines, sentinel_lines = push_filter(sourcefilename)
   write_if_changed(outlines, sourcefilename, targetfilename)
#@-node:bwmulder.20041017125718.18:push_file
#@+node:bwmulder.20041017125718.19:push_filter
def push_filter(sourcefilename):
   """
   
   Removes sentinels from the lines of 'sourcefilename'.
   
   """
   
   return push_filter_lines(file(sourcefilename).readlines(), marker_from_extension(sourcefilename))
#@-node:bwmulder.20041017125718.19:push_filter
#@+node:bwmulder.20041017125718.20:push_filter_lines
def push_filter_lines(lines, marker):
   """
   
   Removes sentinels from lines.
   
   """
   result, sentinel_lines = [], []
   for line in lines:
      if is_sentinel(line, marker):
         sentinel_lines.append(line)
      else:
         result.append(line)
   return result, sentinel_lines
#@-node:bwmulder.20041017125718.20:push_filter_lines
#@+node:bwmulder.20041017125718.30:push_filter_mapping
def push_filter_mapping(filelines, marker):
   """
   Given the lines of a file, filter out all
   Leo sentinels, and return a mapping:
      
      stripped file -> original file
      
   Filtering should be the same as
   push_filter_lines
   """
   
   mapping = [None]
   for linecount, line in enumerate(filelines):
      if not is_sentinel(line, marker):
         mapping.append(linecount+1)
   return mapping
#@-node:bwmulder.20041017125718.30:push_filter_mapping
#@+node:bwmulder.20041017125718.35:class writeclass
   
   
   
class writeclass(file):
    """
    Small class to remove the sentinels from the LEO
    file and write the result back to the derived file.
    This happens at the close operation of the file.
    """
    #@	@+others
    #@+node:bwmulder.20041017125718.36:__init__
    def __init__(self, leofilename, filename):
       self.leo_originalname = filename
       self.leo_filename = leofilename
       file.__init__(self, leofilename, 'wb')
    #@-node:bwmulder.20041017125718.36:__init__
    #@+node:bwmulder.20041017125718.37:close
    def close(self):
       file.close(self)
       leo_filename, leo_originalname = self.leo_filename, self.leo_originalname
       assert leo_filename.endswith(".tmp")
       shutil.copy2(leo_filename, leo_filename[:-4])
       # we update regular file in the Leo subdirectory, otherwise structural changes get lost.
       push_file(sourcefilename = self.leo_filename, targetfilename = self.leo_originalname)
       os.unlink(leo_filename)
    #@-node:bwmulder.20041017125718.37:close
    #@-others
#@-node:bwmulder.20041017125718.35:class writeclass
#@-node:bwmulder.20041017130118:auxilary functions
#@+node:bwmulder.20041017125718.21:class sentinel_squasher
# The pull operation is more complicated than the pull operation: we must copy 
# back the sources into a LEO files, making sure that the code is in the 
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
    def check_lines_for_equality(self, lines1, lines2, message, lines1_message, lines2_message):
       """
       Little helper function to get nice output if something goes wrong.
       """
       if lines1 == lines2:
          return
       print "================================="
       print message
       print "================================="
       print lines1_message
       print "---------------------------------"
       for line in lines1:
          print line,
       print "=================================="
       print lines2_message
       print "---------------------------------"
       for line in lines2:
          print line,
       assert 0,message
    #@-node:bwmulder.20041017125718.22:check_lines_for_equality
    #@+node:bwmulder.20041017125718.23:create_back_mapping
    def create_back_mapping(self, sourcelines, marker):
       """
    
       'sourcelines' is a list of lines of a file with sentinels.
    
       Creates a new list of lines without sentinels, and keeps a
       mapping which maps each source line in the new list back to its
       original line.
    
       Returns the new list of lines, and the mapping.
    
       To save an if statement later, the mapping is extended by one
       extra element.
    
       """
       mapping, resultlines = [], []
    
       si, l = 0, len(sourcelines)
       while si < l:
          sline = sourcelines[si]
          if not is_sentinel(sline, marker):
             resultlines.append(sline)
             mapping.append(si)
          si += 1
    
       # for programing convenience, we create an additional mapping entry.
       # This simplifies the programming of the copy_sentinels function below.
       mapping.append(si)
       return resultlines, mapping
    #@-node:bwmulder.20041017125718.23:create_back_mapping
    #@+node:bwmulder.20041017125718.24:copy_sentinels
    def copy_sentinels(self, writer_new_sourcefile, reader_leo_file, mapping, startline, endline):
       """
       
       Sentinels are NEVER deleted by this script. They are changed as
       a result of user actions in the LEO.
    
       If code is replaced, or deleted, then we must make sure that the
       sentinels are still in the LEO file.
    
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
       unmapped_line = startline + 1
       
       while unmapped_line <= endline:
          mapped_line = mapping[unmapped_line]
          if old_mapped_line + 1 != mapped_line:
             reader_leo_file.sync(old_mapped_line + 1)
             # There was a gap. This gap must have consisted of sentinels, which have
             # been deleted.
             # Copy those sentinels.
             while reader_leo_file.index() < mapped_line:
                line = reader_leo_file.get()
                if testing:
                   print "Copy sentinels:", line,
                writer_new_sourcefile.push(line)
          old_mapped_line = mapped_line
          unmapped_line += 1
       reader_leo_file.sync(mapping[endline])
    #@-node:bwmulder.20041017125718.24:copy_sentinels
    #@+node:bwmulder.20041017125718.25:pull_source
    def pull_source(self, sourcefile, targetfile):
       """
    
       Propagate the changes of targetfile back to sourcefile. Assume
       that sourcefile has sentinels, and targetfile has not.
       
       This is the heart of the script.
    
       """
       if testing:
          print "pull_source:", sourcefile, targetfile
       marker = marker_from_extension(sourcefile)
       sourcelines = file(sourcefile).readlines()
       targetlines = file(targetfile).readlines()
    
       internal_sourcelines, mapping = self.create_back_mapping(sourcelines, marker)
    
       sm = SequenceMatcher(None, internal_sourcelines, targetlines)
    
       writer_new_sourcefile = sourcewriter()
       # collects the contents of the new file.
    
       reader_modified_file = sourcereader(targetlines)
       # reader_modified_file contains the changed source code. There
       # are no sentinels in 'targetlines'
    
       reader_internal_file = sourcereader(internal_sourcelines)
       # This is the same file as reader_leo_file, without sentinels.
    
       reader_leo_file = sourcereader(sourcelines)
       # This is the file which is currently produced by LEO,
       # with sentinels.
    
       # we compare the 'targetlines' with 'internal_sourcelines' and propagate
       # the changes back into 'writer_new_sourcefile' while making sure that
       # all sentinels of 'sourcelines' are copied as well.
    
       # An invariant of the following loop is that all three readers are in sync.
       # In addition, writer_new_sourcefile has accumulated the new file, which
       # is going to replace reader_leo_file.
    
       # Check that all ranges returned by get_opcodes() are contiguous
       i2_internal_old, i2_modified_old = -1, -1
       
       # Copy the sentinels at the beginning of the file.
       while reader_leo_file.index() < mapping[0]:
          line = reader_leo_file.get()
          writer_new_sourcefile.push(line)
       for tag, i1_internal_file, i2_internal_file, i1_modified_file, i2_modified_file in sm.get_opcodes():
          if testing:
             print "tag:", tag, "i1, i2 (internal file):", i1_internal_file, i2_internal_file, "i1, i2 (modified file)", i1_modified_file, i2_modified_file
          
          # We need the ranges returned by get_opcodes to completely cover the source lines being compared.
          # We also need the ranges not to overlap.
          if i2_internal_old != -1:
             assert i2_internal_old == i1_internal_file
             assert i2_modified_old == i1_modified_file
          i2_internal_old, i2_modified_old = i2_internal_file, i2_modified_file
          
          # Loosely speaking, the loop invariant is that
          # we have processed everything up to, but not including,
          # the lower bound of the ranges returned by the iterator.
          # 
          # We have to check the three readers, reader_internal_file,
          # reader_modified_file, and reader_leo_file.
          # 
          # For the writer, the filter must reproduce the modified file
          # up until, but not including, i1_modified_file.
          # 
          # In addition, all the sentinels of the original LEO file, up until
          # mapping[i1_internal_file], must be present in the new_source_file.
          # 
          # 
          # Check the loop invariant.
          assert reader_internal_file.i == i1_internal_file
          assert reader_modified_file.i == i1_modified_file
          assert reader_leo_file.i == mapping[i1_internal_file]
          if testing:
             # These conditions are a little bit costly to check. Do this only if we are testing
             # the script.
             t_sourcelines, t_sentinel_lines = push_filter_lines(writer_new_sourcefile.lines, marker)
             
             # Check that we have all the modifications so far.
             assert t_sourcelines == reader_modified_file.lines[:i1_modified_file]
             
             # Check that we kept all sentinels so far.
             assert t_sentinel_lines == push_filter_lines(reader_leo_file.lines[:reader_leo_file.i], marker)[1]
    
          
          if tag == 'equal':
             # nothing is to be done.
             # Leave the LEO file alone.
             #
             # Copy the lines from the leo file to the new sourcefile.
             # This loop copies both text and sentinels.
             while reader_leo_file.index() <= mapping[i2_internal_file - 1]:
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
             self.copy_sentinels(writer_new_sourcefile, reader_leo_file, mapping, i2_internal_file - 1, i2_internal_file)
    
          elif tag == 'replace':
             # We have to replace lines.
             # The replaced lines may span across several sections of sentinels.
    
             # For now, we put all the new contents after the first sentinels.
             # Different strategies may be possible later.
    
             # We might, for example, run the difflib across the different
             # lines and try to construct a mapping changed line => orignal line.
             #
             # Since this will make this portion of the script considerably more
             # complex, we postpone this idea for now.
             while reader_modified_file.index() < i2_modified_file:
                line = reader_modified_file.get()
                if testing:
                   print "Replace: copy modified line:", line,
                writer_new_sourcefile.push(line)
    
             # now we must take care of the sentinels which might be between the
             # changed code.         
             self.copy_sentinels(writer_new_sourcefile, reader_leo_file, mapping, i1_internal_file, i2_internal_file)
             reader_internal_file.sync(i2_internal_file)
                                 
          elif tag == 'delete':
             # We have to delete lines.
             # However, we NEVER delete sentinels, so they must be copied over.
    
             # sync the readers
             if testing:
                print "delete: syncing modified file from ", reader_modified_file.i, " to ", i1_modified_file
                print "delete: syncing internal file from ", reader_internal_file.i, " to ", i1_internal_file
             reader_modified_file.sync(i2_modified_file)
             reader_internal_file.sync(i2_internal_file)
    
             self.copy_sentinels(writer_new_sourcefile, reader_leo_file, mapping, i1_internal_file, i2_internal_file)
             
          elif tag == 'insert':
             while reader_modified_file.index() < i2_modified_file:
                line = reader_modified_file.get()
                if testing:
                   print "insert: copy line:", line,
                writer_new_sourcefile.push(line)
             
             # Since (only) lines are inserted, we do not have to reposition any reader.
             
          else:
             assert 0
    
       # now copy the sentinels at the end of the file.
       while reader_leo_file.index() < reader_leo_file.size():
          writer_new_sourcefile.push(reader_leo_file.get())
          
       written = write_if_changed(writer_new_sourcefile.getlines(), targetfile, sourcefile)
       if written:
          # For the initial usage, we check that the output actually makes sense.
          # We check two things:
          #    1. Applying a 'push' operation will produce the modified file.
          #    2. Our new sourcefile still has the same sentinels as the replaced one.
          
          s_outlines, sentinel_lines = push_filter(sourcefile)
          
          # Check that 'push' will re-create the changed file.
          self.check_lines_for_equality(s_outlines, targetlines, "Pull did not work as expected", "Content of sourcefile:", "Content of modified file:")
          
          # Check that no sentinels got lost.
          old_sentinel_lines = push_filter_lines(reader_leo_file.lines[:reader_leo_file.i], marker)[1]
          self.check_lines_for_equality(sentinel_lines, old_sentinel_lines, "Pull modified sentinel lines:", "Current sentinel lines:", "Old sentinel lines:")
    #@-node:bwmulder.20041017125718.25:pull_source
    #@-others
#@-node:bwmulder.20041017125718.21:class sentinel_squasher
#@-node:bwmulder.20041018233934.1:plugin core
#@+node:bwmulder.20041018233934.2:interface
#@+node:bwmulder.20041017125718.27:putInHooks
# Is this the canonical way to overwrite code?
def putInHooks():
    """
    Put in hooks to use the LEO subfolder.
    
    We have to intercept open calls which open
    file to read and write derived files.
    
    goToLineNumber and messageCommment are
    replaced.
    """
    setattr(atFile, 'read', read)
    setattr(atFile, 'openRead', openRead)
    setattr(atFile, 'check_for_shadow_file', check_for_shadow_file)
   # setattr(fileCommands, 'write_Leo_file', write_Leo_file)
    setattr(fileCommands, 'openWrite', openWrite)
    setattr(fileCommands, 'check_for_shadow_file', check_for_shadow_file)
    setattr(newDerivedFile, 'replaceTargetFileIfDifferent', replaceTargetFileIfDifferent)
    setattr(leoCommands.Commands, 'goToLineNumber', goToLineNumber)
    setattr(newDerivedFile, 'check_for_shadow_file', check_for_shadow_file)
    setattr(newDerivedFile, 'openWriteFile', openWriteFile)
    setattr(newDerivedFile, 'openWrite', openWrite)
    setattr(leoImport.leoImportCommands, 'massageComment', massageComment)
#@nonl
#@-node:bwmulder.20041017125718.27:putInHooks
#@+node:bwmulder.20041017125718.26:applyConfiguration
def applyConfiguration(config=None):
   """Called when the user presses the "Apply" button on the Properties form.
   
   Not sure yet if we need configuration options for this plugin."""

   global active
   if config is None:
      fileName = os.path.join(g.app.loadDir,"../","plugins","mod_LeoSubFolder.ini")
   config = ConfigParser()
   if os.path.exists(fileName):
      config.read(fileName)
      active = config.get("Main", "Active")
   else:
      active = True
#@-node:bwmulder.20041017125718.26:applyConfiguration
#@+node:bwmulder.20041017184636:check_for_shadow_file
def check_for_shadow_file(self, filename):
    """
    Check if there is a shadow file for filename.
    Return:
        - the name of the shadow file,
        - an indicator if the file denoted by 'filename' is
        of zero length.
    """
    dir, simplename = os.path.split(filename)
    rootname, ext = os.path.splitext(simplename)
    if ext == '.tmp':
        shadow_filename = os.path.join(dir, 'LEO', rootname)
        if os.path.exists(shadow_filename):
            resultname = os.path.join(dir, 'LEO', simplename)
            return resultname, False
        else:
            return '', False
    else:
        shadow_filename = os.path.join(dir, 'LEO', simplename)
        if os.path.exists(shadow_filename):
            return shadow_filename, os.path.getsize(filename) == 0
        else:
            return '', False
    
#@nonl
#@-node:bwmulder.20041017184636:check_for_shadow_file
#@-node:bwmulder.20041018233934.2:interface
#@+node:bwmulder.20041017131310:top_df.read
# The caller has enclosed this code in beginUpdate/endUpdate.

def read(self,root,importFileName=None,thinFile=False):
    
    """Common read logic for any derived file."""
    
    at = self ; c = at.c
    at.errors = 0
    importing = importFileName is not None
    #@    << set fileName from root and importFileName >>
    #@+node:bwmulder.20041017131310.1:<< set fileName from root and importFileName >>
    at.scanDefaultDirectory(root,importing=importing)
    if at.errors: return
    
    if importFileName:
        fileName = importFileName
    elif root.isAnyAtFileNode():
        fileName = root.anyAtFileNodeName()
    else:
        fileName = None
    
    if not fileName:
        at.error("Missing file name.  Restoring @file tree from .leo file.")
        return False
    #@nonl
    #@-node:bwmulder.20041017131310.1:<< set fileName from root and importFileName >>
    #@nl
    #@    << open file or return False >>
    #@+node:bwmulder.20041017131310.2:<< open file or return false >>
    fn = g.os_path_join(at.default_directory,fileName)
    fn = g.os_path_normpath(fn)
    
    try:
        # 11/4/03: open the file in binary mode to allow 0x1a in bodies & headlines.
        file = self.openRead(fn,'rb') # bwm
        if file:
            #@        << warn on read-only file >>
            #@+node:bwmulder.20041017131310.3:<< warn on read-only file >>
            try:
                read_only = not os.access(fn,os.W_OK)
                if read_only:
                    g.es("read only: " + fn,color="red")
            except:
                pass # os.access() may not exist on all platforms.
            #@nonl
            #@-node:bwmulder.20041017131310.3:<< warn on read-only file >>
            #@nl
        else: return False
    except:
        at.error("Can not open: " + '"@file ' + fn + '"')
        root.setDirty()
        return False
    #@nonl
    #@-node:bwmulder.20041017131310.2:<< open file or return false >>
    #@nl
    g.es("reading: " + root.headString())
    firstLines,read_new = at.scanHeader(file,fileName)
    df = g.choose(read_new,at.new_df,at.old_df)
    # g.trace(g.choose(df==at.new_df,"new","old"))
    #@    << copy ivars to df >>
    #@+node:bwmulder.20041017131310.4:<< copy ivars to df >>
    # Telling what kind of file we are reading.
    df.importing = importFileName != None
    df.raw = False
    if importing and df == at.new_df:
        thinFile = True
    df.thinFile = thinFile
    
    # Set by scanHeader.
    df.encoding = at.encoding
    df.endSentinelComment = at.endSentinelComment
    df.startSentinelComment = at.startSentinelComment
    
    # Set other common ivars.
    df.errors = 0
    df.file = file
    df.importRootSeen = False
    df.indent = 0
    df.targetFileName = fileName
    df.root = root
    df.root_seen = False
    df.perfectImportRoot = None # Set only in readOpenFile.
    #@nonl
    #@-node:bwmulder.20041017131310.4:<< copy ivars to df >>
    #@nl
    root.clearVisitedInTree()
    try:
        # 1/28/04: Don't set comment delims when importing.
        # 1/28/04: Call scanAllDirectives here, not in readOpenFile.
        importing = importFileName is not None
        df.scanAllDirectives(root,importing=importing,reading=True)
        df.readOpenFile(root,file,firstLines)
    except:
        at.error("Unexpected exception while reading derived file")
        g.es_exception()
    file.close()
    root.clearDirty() # May be set dirty below.
    after = root.nodeAfterTree()
    #@    << warn about non-empty unvisited nodes >>
    #@+node:bwmulder.20041017131310.5:<< warn about non-empty unvisited nodes >>
    for p in root.self_and_subtree_iter():
    
        # g.trace(p)
        try: s = p.v.t.tempBodyString
        except: s = ""
        if s and not p.v.t.isVisited():
            at.error("Not in derived file:" + p.headString())
            p.v.t.setVisited() # One message is enough.
    #@nonl
    #@-node:bwmulder.20041017131310.5:<< warn about non-empty unvisited nodes >>
    #@nl
    if df.errors == 0:
        if not df.importing:
            #@            << copy all tempBodyStrings to tnodes >>
            #@+node:bwmulder.20041017131310.6:<< copy all tempBodyStrings to tnodes >>
            for p in root.self_and_subtree_iter():
                try: s = p.v.t.tempBodyString
                except: s = ""
                if s != p.bodyString():
                    if 0: # For debugging.
                        print ; print "changed: " + p.headString()
                        print ; print "new:",s
                        print ; print "old:",p.bodyString()
                    if thinFile:
                        p.v.setTnodeText(s)
                        if p.v.isDirty():
                            p.setAllAncestorAtFileNodesDirty()
                    else:
                        p.setBodyStringOrPane(s) # Sets v and v.c dirty.
                        
                    if not thinFile or (thinFile and p.v.isDirty()):
                        g.es("changed: " + p.headString(),color="blue")
                        p.setMarked()
            #@nonl
            #@-node:bwmulder.20041017131310.6:<< copy all tempBodyStrings to tnodes >>
            #@nl
    #@    << delete all tempBodyStrings >>
    #@+node:bwmulder.20041017131310.7:<< delete all tempBodyStrings >>
    for p in c.allNodes_iter():
        
        if hasattr(p.v.t,"tempBodyString"):
            delattr(p.v.t,"tempBodyString")
    #@nonl
    #@-node:bwmulder.20041017131310.7:<< delete all tempBodyStrings >>
    #@nl
    return df.errors == 0
#@nonl
#@-node:bwmulder.20041017131310:top_df.read
#@+node:bwmulder.20041017135227:atFile.openWriteFile (used by both old and new code)
# Open files.  Set root.orphan and root.dirty flags and return on errors.

def openWriteFile (self,root,toString):
    
    print "bwms version of openWriteFile:"
    self.toStringFlag = toString
    self.errors = 0 # Bug fix: 6/25/04.
    self.root = root # Bug fix: 7/30/04: needed by error logic.

    try:
        self.scanAllDirectives(root)
        valid = self.errors == 0
    except:
        self.writeError("exception in atFile.scanAllDirectives")
        g.es_exception()
        valid = False
        
    if valid and toString:
        self.targetFileName = self.outputFileName = "<string-file>"
        self.outputFile = g.fileLikeObject()
        self.stringOutput = ""
        return valid

    if valid:
        try:
            fn = self.targetFileName
            self.shortFileName = fn # name to use in status messages.
            self.targetFileName = g.os_path_join(self.default_directory,fn)
            self.targetFileName = g.os_path_normpath(self.targetFileName)
            path = g.os_path_dirname(self.targetFileName)
            if not path or not g.os_path_exists(path):
                self.writeError("path does not exist: " + path)
                valid = False
        except:
            self.writeError("exception creating path:" + fn)
            g.es_exception()
            valid = False

    if valid and g.os_path_exists(self.targetFileName):
        try:
            if not os.access(self.targetFileName,os.W_OK):
                self.writeError("can not create: read only: " + self.targetFileName)
                valid = False
        except:
            pass # os.access() may not exist on all platforms.
        
    if valid:
        try:
            root.clearOrphan() # Bug fix: 5/25/04.
            self.outputFileName = self.targetFileName + ".tmp"
            self.outputFile = self.openWrite(self.outputFileName,'wb') # bwm
            if self.outputFile is None:
                self.writeError("can not create " + self.outputFileName)
                valid = False
        except:
            g.es("exception creating:" + self.outputFileName)
            g.es_exception()
            valid = False
            self.outputFile = None # 3/22/04

    if not valid:
        root.setOrphan()
        root.setDirty()
        self.outputFile = None # 1/29/04
    
    return valid
#@nonl
#@-node:bwmulder.20041017135227:atFile.openWriteFile (used by both old and new code)
#@+node:bwmulder.20041018163332:write_Leo_file
def write_Leo_file(self,fileName,outlineOnlyFlag):

    c = self.c ; config = g.app.config

    self.assignFileIndices()
    if not outlineOnlyFlag:
        #@        << write all @file nodes >>
        #@+node:bwmulder.20041018163332.1:<< write all @file nodes >>
        try:
            # Write all @file nodes and set orphan bits.
            c.atFileCommands.writeAll()
        except:
            g.es_error("exception writing derived files")
            g.es_exception()
            return False
        #@nonl
        #@-node:bwmulder.20041018163332.1:<< write all @file nodes >>
        #@nl
    #@    << return if the .leo file is read-only >>
    #@+node:bwmulder.20041018163332.2:<< return if the .leo file is read-only >>
    # self.read_only is not valid for Save As and Save To commands.
    
    if g.os_path_exists(fileName):
        try:
            if not os.access(fileName,os.W_OK):
                g.es("can not create: read only: " + fileName,color="red")
                return False
        except:
            pass # os.access() may not exist on all platforms.
    #@nonl
    #@-node:bwmulder.20041018163332.2:<< return if the .leo file is read-only >>
    #@nl
    try:
        #@        << create backup file >>
        #@+node:bwmulder.20041018163332.3:<< create backup file >>
        # rename fileName to fileName.bak if fileName exists.
        if g.os_path_exists(fileName):
            try:
                backupName = g.os_path_join(g.app.loadDir,fileName)
                backupName = fileName + ".bak"
                if g.os_path_exists(backupName):
                    os.unlink(backupName)
                # os.rename(fileName,backupName)
                g.utils_rename(fileName,backupName)
            except OSError:
                if self.read_only:
                    g.es("read only",color="red")
                else:
                    g.es("exception creating backup file: " + backupName)
                    g.es_exception()
                return False
            except:
                g.es("exception creating backup file: " + backupName)
                g.es_exception()
                backupName = None
                return False
        else:
            backupName = None
        #@nonl
        #@-node:bwmulder.20041018163332.3:<< create backup file >>
        #@nl
        self.mFileName = fileName
        #@        << create the output file >>
        #@+node:bwmulder.20041018163332.4:<< create the output file >>
        self.outputFile = self.openWrite(fileName, 'wb') # 9/18/02 # bwm
        if not self.outputFile:
            g.es("can not open " + fileName)
            #@    << delete backup file >>
            #@+node:bwmulder.20041018163332.5:<< delete backup file >>
            if backupName and g.os_path_exists(backupName):
                try:
                    os.unlink(backupName)
                except OSError:
                    if self.read_only:
                        g.es("read only",color="red")
                    else:
                        g.es("exception deleting backup file:" + backupName)
                        g.es_exception()
                    return False
                except:
                    g.es("exception deleting backup file:" + backupName)
                    g.es_exception()
                    return False
            #@-node:bwmulder.20041018163332.5:<< delete backup file >>
            #@nl
            return False
        #@nonl
        #@-node:bwmulder.20041018163332.4:<< create the output file >>
        #@nl
        #@        << update leoConfig.txt >>
        #@+node:bwmulder.20041018163332.6:<< update leoConfig.txt >>
        c.setIvarsFromFind()
        config.setConfigFindIvars(c)
        c.setIvarsFromPrefs()
        config.setCommandsIvars(c)
        config.update()
        #@nonl
        #@-node:bwmulder.20041018163332.6:<< update leoConfig.txt >>
        #@nl
        #@        << put the .leo file >>
        #@+node:bwmulder.20041018163332.7:<< put the .leo file >>
        self.putProlog()
        self.putHeader()
        self.putGlobals()
        self.putPrefs()
        self.putFindSettings()
        #start = g.getTime()
        self.putVnodes()
        #start = g.printDiffTime("vnodes ",start)
        self.putTnodes()
        #start = g.printDiffTime("tnodes ",start)
        self.putPostlog()
        #@nonl
        #@-node:bwmulder.20041018163332.7:<< put the .leo file >>
        #@nl
    except:
        #@        << report the exception >>
        #@+node:bwmulder.20041018163332.8:<< report the exception >>
        g.es("exception writing: " + fileName)
        g.es_exception() 
        if self.outputFile:
            try:
                self.outputFile.close()
                self.outputFile = None
            except:
                g.es("exception closing: " + fileName)
                g.es_exception()
        #@nonl
        #@-node:bwmulder.20041018163332.8:<< report the exception >>
        #@nl
        #@        << erase filename and rename backupName to fileName >>
        #@+node:bwmulder.20041018163332.9:<< erase filename and rename backupName to fileName >>
        g.es("error writing " + fileName)
        
        if fileName and g.os_path_exists(fileName):
            try:
                os.unlink(fileName)
            except OSError:
                if self.read_only:
                    g.es("read only",color="red")
                else:
                    g.es("exception deleting: " + fileName)
                    g.es_exception()
            except:
                g.es("exception deleting: " + fileName)
                g.es_exception()
                
        if backupName:
            g.es("restoring " + fileName + " from " + backupName)
            try:
                g.utils_rename(backupName, fileName)
            except OSError:
                if self.read_only:
                    g.es("read only",color="red")
                else:
                    g.es("exception renaming " + backupName + " to " + fileName)
                    g.es_exception()
            except:
                g.es("exception renaming " + backupName + " to " + fileName)
                g.es_exception()
        #@nonl
        #@-node:bwmulder.20041018163332.9:<< erase filename and rename backupName to fileName >>
        #@nl
        return False
    if self.outputFile:
        #@        << close the output file >>
        #@+node:bwmulder.20041018163332.10:<< close the output file >>
        try:
            self.outputFile.close()
            self.outputFile = None
        except:
            g.es("exception closing: " + fileName)
            g.es_exception()
        #@nonl
        #@-node:bwmulder.20041018163332.10:<< close the output file >>
        #@nl
        #@        << delete backup file >>
        #@+middle:bwmulder.20041018163332.4:<< create the output file >>
        #@+node:bwmulder.20041018163332.5:<< delete backup file >>
        if backupName and g.os_path_exists(backupName):
            try:
                os.unlink(backupName)
            except OSError:
                if self.read_only:
                    g.es("read only",color="red")
                else:
                    g.es("exception deleting backup file:" + backupName)
                    g.es_exception()
                return False
            except:
                g.es("exception deleting backup file:" + backupName)
                g.es_exception()
                return False
        #@-node:bwmulder.20041018163332.5:<< delete backup file >>
        #@-middle:bwmulder.20041018163332.4:<< create the output file >>
        #@nl
        return True
    else: # This probably will never happen because errors should raise exceptions.
        #@        << erase filename and rename backupName to fileName >>
        #@+node:bwmulder.20041018163332.9:<< erase filename and rename backupName to fileName >>
        g.es("error writing " + fileName)
        
        if fileName and g.os_path_exists(fileName):
            try:
                os.unlink(fileName)
            except OSError:
                if self.read_only:
                    g.es("read only",color="red")
                else:
                    g.es("exception deleting: " + fileName)
                    g.es_exception()
            except:
                g.es("exception deleting: " + fileName)
                g.es_exception()
                
        if backupName:
            g.es("restoring " + fileName + " from " + backupName)
            try:
                g.utils_rename(backupName, fileName)
            except OSError:
                if self.read_only:
                    g.es("read only",color="red")
                else:
                    g.es("exception renaming " + backupName + " to " + fileName)
                    g.es_exception()
            except:
                g.es("exception renaming " + backupName + " to " + fileName)
                g.es_exception()
        #@nonl
        #@-node:bwmulder.20041018163332.9:<< erase filename and rename backupName to fileName >>
        #@nl
        return False
        
write_LEO_file = write_Leo_file # For compatibility with old plugins.
#@nonl
#@-node:bwmulder.20041018163332:write_Leo_file
#@+node:bwmulder.20041017135327:openRead
def openRead(self, filename, rb):
    """
    Replaces the standard open for reads.
    """
    shadow_filename, file_is_zero = self.check_for_shadow_file(filename)
    if shadow_filename:
        if file_is_zero:
            es("Copy %s to %s without sentinels" % (shadow_filename, filename))
            push_file(sourcefilename=shadow_filename, targetfilename=filename)
        else:
            sq = sentinel_squasher()
            g.es("reading %s instead of %s" %  (shadow_filename, filename), color="orange")
            sq.pull_source(sourcefile = shadow_filename, targetfile=filename)
        return open(shadow_filename, 'rb')
    else:
        return open(filename, 'rb')
#@nonl
#@-node:bwmulder.20041017135327:openRead
#@+node:bwmulder.20041017131319:openWrite
def openWrite(self, filename, wb):
    """
    Replaces the standard open for writes:
        - Check if filename designates a file
          which has a shadow file.
          If so, write to the shadow file,
          and update the real file after the close.
    """
    shadow_filename, file_is_zero = self.check_for_shadow_file(filename)
    if shadow_filename:
        g.es("Writing to %s instead of %s" %  (shadow_filename, filename), color="orange")
        file_to_use = shadow_filename
    else:
        file_to_use = filename
    return open(file_to_use, 'wb')
#@-node:bwmulder.20041017131319:openWrite
#@+node:bwmulder.20041018224835:atFile.replaceTargetFileIfDifferent
def replaceTargetFileIfDifferent (self):
    
    assert(self.outputFile is None)
    
    self.fileChangedFlag = False
    # Check if we are dealing with a shadow file
    dir, shortfilename = os.path.split(self.targetFileName)
    shadow_filename = os.path.join(dir, 'LEO', shortfilename)
    try:
        targetFileName = self.targetFileName
        outputFileName = self.outputFileName
        if os.path.exists(shadow_filename):
            self.targetFileName = shadow_filename
            self.outputFileName = shadow_filename + '.tmp'
            is_shadowfile = True
        else:
            is_shadowfile = False
        if g.os_path_exists(self.targetFileName):
            if self.compareFilesIgnoringLineEndings(
                self.outputFileName,self.targetFileName):
                #@                << delete the output file >>
                #@+node:bwmulder.20041018224835.1:<< delete the output file >>
                try: # Just delete the temp file.
                    os.remove(self.outputFileName)
                except:
                    g.es("exception deleting:" + self.outputFileName)
                    g.es_exception()
                
                g.es("unchanged: " + self.shortFileName)
                #@nonl
                #@-node:bwmulder.20041018224835.1:<< delete the output file >>
                #@nl
            else:
                #@                << replace the target file with the output file >>
                #@+node:bwmulder.20041018224835.2:<< replace the target file with the output file >>
                try:
                    # 10/6/02: retain the access mode of the previous file,
                    # removing any setuid, setgid, and sticky bits.
                    mode = (os.stat(self.targetFileName))[0] & 0777
                except:
                    mode = None
                
                try: # Replace target file with temp file.
                    os.remove(self.targetFileName)
                    try:
                        g.utils_rename(self.outputFileName,self.targetFileName)
                        if mode != None: # 10/3/02: retain the access mode of the previous file.
                            try:
                                os.chmod(self.targetFileName,mode)
                            except:
                                g.es("exception in os.chmod(%s)" % (self.targetFileName))
                        g.es("writing: " + self.shortFileName)
                        self.fileChangedFlag = True
                    except:
                        # 6/28/03
                        self.writeError("exception renaming: %s to: %s" % (self.outputFileName,self.targetFileName))
                        g.es_exception()
                except:
                    self.writeError("exception removing:" + self.targetFileName)
                    g.es_exception()
                    try: # Delete the temp file when the deleting the target file fails.
                        os.remove(self.outputFileName)
                    except:
                        g.es("exception deleting:" + self.outputFileName)
                        g.es_exception()
                #@nonl
                #@-node:bwmulder.20041018224835.2:<< replace the target file with the output file >>
                #@nl
                g.es("Updating %s with %s" % (targetFileName, shadow_filename), color='orange')
                push_file(shadow_filename, targetFileName)
        else:
            #@            << rename the output file to be the target file >>
            #@+node:bwmulder.20041018224835.3:<< rename the output file to be the target file >>
            try:
                g.utils_rename(self.outputFileName,self.targetFileName)
                g.es("creating: " + self.targetFileName)
                self.fileChangedFlag = True
            except:
                self.writeError("exception renaming:" + self.outputFileName +
                    " to " + self.targetFileName)
                g.es_exception()
            #@nonl
            #@-node:bwmulder.20041018224835.3:<< rename the output file to be the target file >>
            #@nl
    finally:
        self.targetFileName = targetFileName
        self.outputFileName = outputFileName
#@nonl
#@-node:bwmulder.20041018224835:atFile.replaceTargetFileIfDifferent
#@+node:bwmulder.20041017221549:goToLineNumber & allies
def goToLineNumber (self,root=None,lines=None,n=None):

    c = self ; p = c.currentPosition() ; root1 = root
    if root is None:
        #@        << set root to the nearest ancestor @file node >>
        #@+node:bwmulder.20041017221549.1:<< set root to the nearest ancestor @file node >>
        fileName = None
        for p in p.self_and_parents_iter():
            fileName = p.anyAtFileNodeName()
            if fileName: break
        
        # New in 4.2: Search the entire tree for joined nodes.
        if not fileName:
            p1 = c.currentPosition()
            for p in c.all_positions_iter():
                if p.v.t == p1.v.t and p != p1:
                    # Found a joined position.
                    for p in p.self_and_parents_iter():
                        fileName = p.anyAtFileNodeName()
                        # New in 4.2 b3: ignore @all nodes.
                        if fileName and not p.isAtAllNode(): break
                if fileName: break
            
        if fileName:
            root = p.copy()
        else:
            g.es("Go to line number: ancestor must be @file node", color="blue")
            return
        #@nonl
        #@-node:bwmulder.20041017221549.1:<< set root to the nearest ancestor @file node >>
        #@nl
    if lines is None:
        #@        << read the file into lines >>
        #@+node:bwmulder.20041017221549.2:<< read the file into lines >>
        # 1/26/03: calculate the full path.
        d = g.scanDirectives(c)
        path = d.get("path")
        
        fileName = g.os_path_join(path,fileName)
        
        try:
        #    file=open(fileName) # bwm
            file, line_mapping = gotoLineNumberOpen(filename)
            lines = file.readlines()
            file.close()
        except:
            g.es("not found: " + fileName)
            return
        #@nonl
        #@-node:bwmulder.20041017221549.2:<< read the file into lines >>
        #@nl
    if n is None:
        #@        << get n, the line number, from a dialog >>
        #@+node:bwmulder.20041017221549.3:<< get n, the line number, from a dialog >>
        n = g.app.gui.runAskOkCancelNumberDialog("Enter Line Number","Line number:")
        if n == -1:
            return
        #@nonl
        #@-node:bwmulder.20041017221549.3:<< get n, the line number, from a dialog >>
        #@nl
        #@        <<Adjust line number for mapping>>
        #@+node:bwmulder.20041018075929:<<Adjust line number for mapping>>
        if line_mapping:
            try:
                n = line_mapping[n]
            except:
                g.es("In real file: line %s not found: " % n, color="red")
                
            
            
        #@-node:bwmulder.20041018075929:<<Adjust line number for mapping>>
        #@nl
    if n==1:
        p = root ; n2 = 1 ; found = True
    elif n >= len(lines):
        p = root ; found = False
        n2 = p.bodyString().count('\n')
    elif root.isAtAsisFileNode():
        #@        << count outline lines, setting p,n2,found >>
        #@+node:bwmulder.20041017221549.4:<< count outline lines, setting p,n2,found >> (@file-nosent only)
        p = lastv = root
        prev = 0 ; found = False
        
        for p in p.self_and_subtree_iter():
            lastv = p.copy()
            s = p.bodyString()
            lines = s.count('\n')
            if len(s) > 0 and s[-1] != '\n':
                lines += 1
            # print lines,prev,p
            if prev + lines >= n:
                found = True ; break
            prev += lines
        
        p = lastv
        n2 = max(1,n-prev)
        #@nonl
        #@-node:bwmulder.20041017221549.4:<< count outline lines, setting p,n2,found >> (@file-nosent only)
        #@nl
    else:
        vnodeName,childIndex,gnx,n2,delim = self.convertLineToVnodeNameIndexLine(lines,n,root)
        found = True
        if not vnodeName:
            g.es("error handling: " + root.headString())
            return
        #@        << set p to the node given by vnodeName and gnx or childIndex or n >>
        #@+node:bwmulder.20041017221549.5:<< set p to the node given by vnodeName and gnx or childIndex or n >>
        if gnx:
            #@    << 4.2: get node from gnx >>
            #@+node:bwmulder.20041017221549.6:<< 4.2: get node from gnx >>
            found = False
            gnx = g.app.nodeIndices.scanGnx(gnx,0)
            
            # g.trace(vnodeName)
            # g.trace(gnx)
            
            for p in root.self_and_subtree_iter():
                if p.matchHeadline(vnodeName):
                    # g.trace(p.v.t.fileIndex)
                    if p.v.t.fileIndex == gnx:
                        found = True ; break
            
            if not found:
                g.es("not found: " + vnodeName, color="red")
                return
            #@nonl
            #@-node:bwmulder.20041017221549.6:<< 4.2: get node from gnx >>
            #@nl
        elif childIndex == -1:
            #@    << 4.x: scan for the node using tnodeList and n >>
            #@+node:bwmulder.20041017221549.7:<< 4.x: scan for the node using tnodeList and n >>
            # This is about the best that can be done without replicating the entire atFile write logic.
            
            ok = True
            
            if not hasattr(root.v.t,"tnodeList"):
                s = "no child index for " + root.headString()
                print s ; g.es(s, color="red")
                ok = False
            
            if ok:
                tnodeList = root.v.t.tnodeList
                #@    << set tnodeIndex to the number of +node sentinels before line n >>
                #@+node:bwmulder.20041017221549.8:<< set tnodeIndex to the number of +node sentinels before line n >>
                tnodeIndex = -1 # Don't count the @file node.
                scanned = 0 # count of lines scanned.
                
                for s in lines:
                    if scanned >= n:
                        break
                    i = g.skip_ws(s,0)
                    if g.match(s,i,delim):
                        i += len(delim)
                        if g.match(s,i,"+node"):
                            # g.trace(tnodeIndex,s.rstrip())
                            tnodeIndex += 1
                    scanned += 1
                #@nonl
                #@-node:bwmulder.20041017221549.8:<< set tnodeIndex to the number of +node sentinels before line n >>
                #@nl
                tnodeIndex = max(0,tnodeIndex)
                #@    << set p to the first vnode whose tnode is tnodeList[tnodeIndex] or set ok = False >>
                #@+node:bwmulder.20041017221549.9:<< set p to the first vnode whose tnode is tnodeList[tnodeIndex] or set ok = false >>
                #@+at 
                #@nonl
                # We use the tnodeList to find a _tnode_ corresponding to the 
                # proper node, so the user will for sure be editing the proper 
                # text, even if several nodes happen to have the same 
                # headline.  This is really all that we need.
                # 
                # However, this code has no good way of distinguishing between 
                # different cloned vnodes in the file: they all have the same 
                # tnode.  So this code just picks p = t.vnodeList[0] and 
                # leaves it at that.
                # 
                # The only way to do better is to scan the outline, 
                # replicating the write logic to determine which vnode created 
                # the given line.  That's way too difficult, and it would 
                # create an unwanted dependency in this code.
                #@-at
                #@@c
                
                # g.trace("tnodeIndex",tnodeIndex)
                if tnodeIndex < len(tnodeList):
                    t = tnodeList[tnodeIndex]
                    # Find the first vnode whose tnode is t.
                    found = False
                    for p in root.self_and_subtree_iter():
                        if p.v.t == t:
                            found = True ; break
                    if not found:
                        s = "tnode not found for " + vnodeName
                        print s ; g.es(s, color="red") ; ok = False
                    elif p.headString().strip() != vnodeName:
                        if 0: # Apparently this error doesn't prevent a later scan for working properly.
                            s = "Mismatched vnodeName\nExpecting: %s\n got: %s" % (p.headString(),vnodeName)
                            print s ; g.es(s, color="red")
                        ok = False
                else:
                    if root1 is None: # Kludge: disable this message when called by goToScriptLineNumber.
                        s = "Invalid computed tnodeIndex: %d" % tnodeIndex
                        print s ; g.es(s, color = "red")
                    ok = False
                #@nonl
                #@-node:bwmulder.20041017221549.9:<< set p to the first vnode whose tnode is tnodeList[tnodeIndex] or set ok = false >>
                #@nl
                        
            if not ok:
                # Fall back to the old logic.
                #@    << set p to the first node whose headline matches vnodeName >>
                #@+node:bwmulder.20041017221549.10:<< set p to the first node whose headline matches vnodeName >>
                found = False
                for p in root.self_and_subtree_iter():
                    if p.matchHeadline(vnodeName):
                        found = True ; break
                
                if not found:
                    s = "not found: " + vnodeName
                    print s ; g.es(s, color="red")
                    return
                #@nonl
                #@-node:bwmulder.20041017221549.10:<< set p to the first node whose headline matches vnodeName >>
                #@nl
            #@nonl
            #@-node:bwmulder.20041017221549.7:<< 4.x: scan for the node using tnodeList and n >>
            #@nl
        else:
            #@    << 3.x: scan for the node with the given childIndex >>
            #@+node:bwmulder.20041017221549.11:<< 3.x: scan for the node with the given childIndex >>
            found = False
            for p in root.self_and_subtree_iter():
                if p.matchHeadline(vnodeName):
                    if childIndex <= 0 or p.childIndex() + 1 == childIndex:
                        found = True ; break
            
            if not found:
                g.es("not found: " + vnodeName, color="red")
                return
            #@nonl
            #@-node:bwmulder.20041017221549.11:<< 3.x: scan for the node with the given childIndex >>
            #@nl
        #@nonl
        #@-node:bwmulder.20041017221549.5:<< set p to the node given by vnodeName and gnx or childIndex or n >>
        #@nl
    #@    << select p and make it visible >>
    #@+node:bwmulder.20041017221549.12:<< select p and make it visible >>
    c.beginUpdate()
    c.frame.tree.expandAllAncestors(p)
    c.selectVnode(p)
    c.endUpdate()
    #@nonl
    #@-node:bwmulder.20041017221549.12:<< select p and make it visible >>
    #@nl
    #@    << put the cursor on line n2 of the body text >>
    #@+node:bwmulder.20041017221549.13:<< put the cursor on line n2 of the body text >>
    if found:
        c.frame.body.setInsertPointToStartOfLine(n2-1)
    else:
        c.frame.body.setInsertionPointToEnd()
        g.es("%d lines" % len(lines), color="blue")
    
    c.frame.body.makeInsertPointVisible()
    #@nonl
    #@-node:bwmulder.20041017221549.13:<< put the cursor on line n2 of the body text >>
    #@nl
#@nonl
#@+node:bwmulder.20041017221549.14:convertLineToVnodeNameIndexLine
#@+at 
#@nonl
# We count "real" lines in the derived files, ignoring all sentinels that do 
# not arise from source lines.  When the indicated line is found, we scan 
# backwards for an @+body line, get the vnode's name from that line and set p 
# to the indicated vnode.  This will fail if vnode names have been changed, 
# and that can't be helped.
# 
# Returns (vnodeName,offset)
# 
# vnodeName: the name found in the previous @+body sentinel.
# offset: the offset within p of the desired line.
#@-at
#@@c

def convertLineToVnodeNameIndexLine (self,lines,n,root):
    
    """Convert a line number n to a vnode name, (child index or gnx) and line number."""
    
    c = self ; at = c.atFileCommands
    childIndex = 0 ; gnx = None ; newDerivedFile = False
    thinFile = root.isAtThinFileNode()
    #@    << set delim, leoLine from the @+leo line >>
    #@+node:bwmulder.20041017221549.15:<< set delim, leoLine from the @+leo line >>
    # Find the @+leo line.
    tag = "@+leo"
    i = 0 
    while i < len(lines) and lines[i].find(tag)==-1:
        i += 1
    leoLine = i # Index of the line containing the leo sentinel
    
    if leoLine < len(lines):
        s = lines[leoLine]
        valid,newDerivedFile,start,end = at.parseLeoSentinel(s)
        if valid: delim = start + '@'
        else:     delim = None
    else:
        delim = None
    #@-node:bwmulder.20041017221549.15:<< set delim, leoLine from the @+leo line >>
    #@nl
    if not delim:
        g.es("bad @+leo sentinel")
        return None,None,None,None,None
    #@    << scan back to @+node, setting offset,nodeSentinelLine >>
    #@+node:bwmulder.20041017221549.16:<< scan back to  @+node, setting offset,nodeSentinelLine >>
    offset = 0 # This is essentially the Tk line number.
    nodeSentinelLine = -1
    line = n - 1
    while line >= 0:
        s = lines[line]
        # g.trace(s)
        i = g.skip_ws(s,0)
        if g.match(s,i,delim):
            #@        << handle delim while scanning backward >>
            #@+node:bwmulder.20041017221549.17:<< handle delim while scanning backward >>
            if line == n:
                g.es("line "+str(n)+" is a sentinel line")
            i += len(delim)
            
            if g.match(s,i,"-node"):
                # The end of a nested section.
                line = self.skipToMatchingNodeSentinel(lines,line,delim)
            elif g.match(s,i,"+node"):
                nodeSentinelLine = line
                break
            elif g.match(s,i,"<<") or g.match(s,i,"@first"):
                offset += 1 # Count these as a "real" lines.
            #@nonl
            #@-node:bwmulder.20041017221549.17:<< handle delim while scanning backward >>
            #@nl
        else:
            offset += 1 # Assume the line is real.  A dubious assumption.
        line -= 1
    #@nonl
    #@-node:bwmulder.20041017221549.16:<< scan back to  @+node, setting offset,nodeSentinelLine >>
    #@nl
    if nodeSentinelLine == -1:
        # The line precedes the first @+node sentinel
        # g.trace("before first line")
        return root.headString(),0,gnx,1,delim # 10/13/03
    s = lines[nodeSentinelLine]
    # g.trace(s)
    #@    << set vnodeName and (childIndex or gnx) from s >>
    #@+node:bwmulder.20041017221549.18:<< set vnodeName and (childIndex or gnx) from s >>
    if newDerivedFile:
        i = 0
        if thinFile:
            # gnx is lies between the first and second ':':
            i = s.find(':',i)
            if i > 0:
                i += 1
                j = s.find(':',i)
                if j > 0:
                    gnx = s[i:j]
                else: i = len(s)
            else: i = len(s)
        # vnode name is everything following the first or second':'
        # childIndex is -1 as a flag for later code.
        i = s.find(':',i)
        if i > -1: vnodeName = s[i+1:].strip()
        else: vnodeName = None
        childIndex = -1
    else:
        # vnode name is everything following the third ':'
        i = 0 ; colons = 0
        while i < len(s) and colons < 3:
            if s[i] == ':':
                colons += 1
                if colons == 1 and i+1 < len(s) and s[i+1] in string.digits:
                    junk,childIndex = g.skip_long(s,i+1)
            i += 1
        vnodeName = s[i:].strip()
        
    # g.trace("gnx",gnx,"vnodeName:",vnodeName)
    if not vnodeName:
        vnodeName = None
        g.es("bad @+node sentinel")
    #@nonl
    #@-node:bwmulder.20041017221549.18:<< set vnodeName and (childIndex or gnx) from s >>
    #@nl
    # g.trace("childIndex,offset",childIndex,offset,vnodeName)
    return vnodeName,childIndex,gnx,offset,delim
#@-node:bwmulder.20041017221549.14:convertLineToVnodeNameIndexLine
#@+node:bwmulder.20041017221549.19:skipToMatchingNodeSentinel
def skipToMatchingNodeSentinel (self,lines,n,delim):
    
    s = lines[n]
    i = g.skip_ws(s,0)
    assert(g.match(s,i,delim))
    i += len(delim)
    if g.match(s,i,"+node"):
        start="+node" ; end="-node" ; delta=1
    else:
        assert(g.match(s,i,"-node"))
        start="-node" ; end="+node" ; delta=-1
    # Scan to matching @+-node delim.
    n += delta ; level = 0
    while 0 <= n < len(lines):
        s = lines[n] ; i = g.skip_ws(s,0)
        if g.match(s,i,delim):
            i += len(delim)
            if g.match(s,i,start):
                level += 1
            elif g.match(s,i,end):
                if level == 0: break
                else: level -= 1
        n += delta
        
    # g.trace(n)
    return n
#@nonl
#@-node:bwmulder.20041017221549.19:skipToMatchingNodeSentinel
#@-node:bwmulder.20041017221549:goToLineNumber & allies
#@+node:bwmulder.20041017125718.33:massageComment
def massageComment (self,s):

	"""Leo has no busines changing comments!"""

	return s
#@-node:bwmulder.20041017125718.33:massageComment
#@+node:bwmulder.20041018075528:gotoLineNumberOpen
def gotoLineNumberOpen(self, filename):
    shadow_filename, file_is_zero = self.check_for_shadow_file(filename)
    if shadow_filename:
        mapping = push_filter_mapping(lines, marker_from_extension(leo_subfolder_filename))
    else:
        mapping = {}
    return open(filename), mapping
#@-node:bwmulder.20041018075528:gotoLineNumberOpen
#@+node:bwmulder.20041017125718.39:stop_testing
testing = False

print_copy_operations = False
# Should this script tell if files are copied?

do_backups = False
# Just in case something goes wrong, there will always be
# a backup file around

def stop_testing():
   global testing
   testing = False
#@-node:bwmulder.20041017125718.39:stop_testing
#@-others
   
applyConfiguration()

if active:
   print "Hooks put into Leo..."
   putInHooks()
   # Register the handlers...
   # ?leoPlugins.registerHandler("idle", autosave)
   __version__ = "0.1"
   g.es("Plugin enabled: Use a LEO subfolder for files with LEO sentinels",color="orange")
   
#@nonl
#@-node:bwmulder.20041017125718:@thin ../plugins/mod_shadow.py
#@-leo
