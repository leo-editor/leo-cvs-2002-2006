#@+leo-ver=4-thin
#@+node:ekr.20040327114250:@thin ../test/unittest/batchTest.py
# A file to be executed in batch mode as part of unit testing.

#@@language python
#@@tabwidth -4

import leoGlobals as g

path = g.os_path_join(g.app.loadDir,"..","test","unittest","createdFile.txt")

if 1:
    print "creating", path

f = None
try:
    try:
        f = open(path,"w")
        f.write("This is a test")
    except IOError:
        g.es("Can not create", path)
finally:
    if f:
        f.close()
#@nonl
#@-node:ekr.20040327114250:@thin ../test/unittest/batchTest.py
#@-leo
