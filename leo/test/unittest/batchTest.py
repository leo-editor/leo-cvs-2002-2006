#@+leo-ver=4-thin
#@+node:ekr.20040327114250:@thin ../test/unittest/batchTest.py
# A file to be executed in batch mode as part of unit testing.

#@@language python
#@@tabwidth -4

import leoGlobals as g

# path = r"c:\prog\test\unittest\createdFile.txt"

path = g.os_path_join(g.app.loadDir,"..","test","unittest","createdFile.txt")

print "creating", path

f = None
try:
    f = open(path,"w")
    f.write("This is a test")
finally:
    if f: f.close()
#@nonl
#@-node:ekr.20040327114250:@thin ../test/unittest/batchTest.py
#@-leo
