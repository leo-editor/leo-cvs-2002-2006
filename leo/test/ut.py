#@+leo-ver=4-thin
#@+node:ekr.20051208084010:@thin ut.py
import leoTest

# Open ut.leo
fileName = g.os_path_join(g.app.loadDir,'..','test','ut.leo')
ok, frame = g.openWithFileName(fileName,c)
old_c = c
c = frame.c # c is the new frame

# Select the 'Unit Test' node.
u = leoTest.testUtils()
h = 'Unit Tests'
p = u.findNodeAnywhere(c,h)
c.selectPosition(p)
# print 'Found unit tests in %s = %s' % (c.fileName(),p)

# Run the unit tests in the selected tree.
leoTest.doTests(all=False,c=c)
#@-node:ekr.20051208084010:@thin ut.py
#@-leo
