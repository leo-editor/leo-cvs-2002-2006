#@+leo-ver=4
#@+node:@file ../test/batchTest.py
# A file to be executed in batch mode as part of unit testing.

#@@language python
#@@tabwidth -4

import leoGlobals as g

# path = r"c:\prog\test\unittest\createdFile.txt"

path = g.os_path_join(g.app.loadDir,"..","test","createdFile.txt")

print "creating", path

f = None
try:
    f = open(path,"w")
    f.write("This is a test")
finally:
    if f: f.close()
#@nonl
#@-node:@file ../test/batchTest.py
#@-leo
