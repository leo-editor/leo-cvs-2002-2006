#@+leo
#@+node:0::@file tangle_done.py
#@+body
#@@language python

# Example tangle_done.py file.
# Leo catches all exceptions thrown here; there is no need for try:except blocks.


#@+others
#@+node:1::run
#@+body
# Leo calls this routine if "Run tangle-done.py after Tangle" is checked in the Prefs panel.

def run (root_list):

	print "tangle_done roots:"
	for root in root_list:
		print root
	
	if 0: # Run code contributed by Paul Paterson.
		convertRSTfilesToHTML(root_list)
#@-body
#@-node:1::run
#@+node:2::convertRSTfilesToHTML
#@+body
#@+at
#  This routine creates .html files from all .rst files in root_list, the list 
# of files that have just been tangled.
# 
# Adapted from code by Paul Paterson.

#@-at
#@@c

def convertRSTfilesToHTML(root_list):

	# Leo will report the execption if docutils is not installed.
	from docutils.core import Publisher 
	from docutils.io import FileInput,StringOutput,StringInput 
	import os
	
	for root in root_list: 
		base,fullname = os.path.split(root)
		name,ext = os.path.splitext(fullname)
		if ext == ".rst":
			file = os.path.join(base,name+".html")
			
			#@<< Convert root to corresponding .html file >>
			#@+node:1::<< Convert root to corresponding .html file >>
			#@+body
			# Read .rst file into s.
			f = open(root,"r")
			s = f.read()
			f.close()
			
			# Restucture s into output.
			pub = Publisher() 
			pub.source = StringInput(pub.settings,source=s) 
			pub.destination = StringOutput(pub.settings,encoding="utf-8") 
			pub.set_reader('standalone',None,'restructuredtext') 
			pub.set_writer('html') 
			output = pub.publish()
			
			# Write the corresponding html file.
			f = open(file,"w")
			f.write(output)
			f.close()
			#@-body
			#@-node:1::<< Convert root to corresponding .html file >>


#@-body
#@-node:2::convertRSTfilesToHTML
#@-others
#@-body
#@-node:0::@file tangle_done.py
#@-leo
