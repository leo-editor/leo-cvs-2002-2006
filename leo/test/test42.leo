<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="2346" clone_windows="0"/>
<globals body_outline_ratio="0.44343434343434346">
	<global_window_position top="60" left="115" height="990" width="1071"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences>
</preferences>
<find_panel_settings>
	<find_string></find_string>
	<change_string></change_string>
</find_panel_settings>
<vnodes>
<v t="ekr.20040301204729"><vh>Root</vh></v>
<v t="ekr.20040126105605" a="E"><vh>Clone test</vh>
<v t="ekr.20040302092753"><vh>aa</vh></v>
<v t="ekr.20040126105605.2" a="E"><vh>a</vh>
<v t="ekr.20040126105605.3" a="E"><vh>b</vh>
<v t="ekr.20040301191933" a="E"><vh>c</vh>
<v t="ekr.20040302092753.1" a="E"><vh>c2</vh>
<v t="ekr.20040302092753.2"><vh>c3</vh></v>
<v t="ekr.20040302092753.3"><vh>c4</vh></v>
</v>
</v>
</v>
<v t="ekr.20040126105605.3"><vh>b</vh>
<v t="ekr.20040301191933"><vh>c</vh>
<v t="ekr.20040302092753.1"><vh>c2</vh>
<v t="ekr.20040302092753.2"><vh>c3</vh></v>
<v t="ekr.20040302092753.3"><vh>c4</vh></v>
</v>
</v>
</v>
</v>
<v t="ekr.20040301191933.1" a="E"><vh>d</vh>
<v t="ekr.20040126105605.2"><vh>a</vh>
<v t="ekr.20040126105605.3"><vh>b</vh>
<v t="ekr.20040301191933"><vh>c</vh>
<v t="ekr.20040302092753.1"><vh>c2</vh>
<v t="ekr.20040302092753.2"><vh>c3</vh></v>
<v t="ekr.20040302092753.3"><vh>c4</vh></v>
</v>
</v>
</v>
<v t="ekr.20040126105605.3"><vh>b</vh>
<v t="ekr.20040301191933"><vh>c</vh>
<v t="ekr.20040302092753.1"><vh>c2</vh>
<v t="ekr.20040302092753.2"><vh>c3</vh></v>
<v t="ekr.20040302092753.3"><vh>c4</vh></v>
</v>
</v>
</v>
</v>
</v>
<v t="ekr.20040301191933.2"><vh>e</vh></v>
<v t="ekr.20040302092753.4"><vh>z</vh></v>
</v>
<v t="ekr.20040302091705"><vh>Test of moving positions</vh></v>
<v t="ekr.20040301162657" a="E"><vh>Mini tests of position class</vh>
<v t="ekr.20040301203156"><vh>test p.level</vh></v>
<v t="ekr.20040302103704"><vh>test test parent/child links</vh>
<v t="ekr.20040302110220"><vh>&lt;&lt; check that the parent of p's first child is p &gt;&gt;</vh></v>
<v t="ekr.20040302110220.1"><vh>&lt;&lt; check that the parent of all parent's children is parent &gt;&gt;</vh></v>
</v>
<v t="ekr.20040302110925"><vh>test next/back links</vh></v>
<v t="ekr.20040302113435" a="M"><vh>test vnodeList</vh></v>
<v t="ekr.20040302114642" a="TV"><vh>test threadNext/threadBack</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="ekr.20040126105605"></t>
<t tx="ekr.20040126105605.2"></t>
<t tx="ekr.20040126105605.3"></t>
<t tx="ekr.20040301162657"></t>
<t tx="ekr.20040301191933"></t>
<t tx="ekr.20040301191933.1"></t>
<t tx="ekr.20040301191933.2"></t>
<t tx="ekr.20040301203156">from leoGlobals import *

c = top()
c.convertTreeToSharedNodes()
c.disableSaveCommands()

print ; print "start"

p = c.rootPosition()
while p and p.v.headString().strip().lower() != "clone test":
	p.moveToThreadNext()
	
after = p.getNodeAfterTree()
while p and p != after:
	print p.level(), p.v.headString()
	p.moveToThreadNext()
		
print ; print "done"</t>
<t tx="ekr.20040301204729"></t>
<t tx="ekr.20040302091705">from leoGlobals import *

class position:
	def __init__(self):
		self.v = "a"
	def move(self):
		self.v = "b"

p = position()
v = p.v
print "before", v, p.v, v is p.v
p.move()
print "after ", v, p.v, v is p.v</t>
<t tx="ekr.20040302092753"></t>
<t tx="ekr.20040302092753.1"></t>
<t tx="ekr.20040302092753.2"></t>
<t tx="ekr.20040302092753.3"></t>
<t tx="ekr.20040302092753.4"></t>
<t tx="ekr.20040302103704">from leoGlobals import *

c = top()
c.convertTreeToSharedNodes()
c.disableSaveCommands()

print ; print "checking parent/child relationships"

p = c.rootPosition() ; count = 0
while p:
	count += 1
	&lt;&lt; check that the parent of p's first child is p &gt;&gt;
	parent = p.getParent()
	if parent:
		&lt;&lt; check that the parent of all parent's children is parent &gt;&gt;
	p.moveToThreadNext()
		
print ; print "checked %d nodes" % count</t>
<t tx="ekr.20040302110220">firstChild = p.getFirstChild()
if firstChild:
	parent = firstChild.getParent()
	if p != parent:
		print "mismatch:p,parent,child",p,parent,firstChild</t>
<t tx="ekr.20040302110220.1">found = false
child = parent.getFirstChild()
if not child:
	print "parent has no children"
while child:
	if child == p: found
	childParent = child.getParent()
	if childParent != parent:
		print "mismatch:parent,childParent",parent,childParent
	child = child.moveToNext()</t>
<t tx="ekr.20040302110925">from leoGlobals import *

c = top()
c.convertTreeToSharedNodes()
c.disableSaveCommands()

print ; print "checking next/back links"

p = c.rootPosition() ; count = 0
while p:
	back = p.getBack()
	next = p.getNext()
	if back:
		count += 1
		assert(back.getNext() == p)
	if next:
		count += 1
		assert(next.getBack() == p)
	p.moveToThreadNext()
		
print ; print "checked %d nodes" % count</t>
<t tx="ekr.20040302113435">from leoGlobals import *

c = top()
c.convertTreeToSharedNodes()
c.disableSaveCommands()

print ; print "checking consistency of vnodeList"

p = c.rootPosition() ; count = 0
while p:
	vnodeList = p.v.t.vnodeList
	for v in vnodeList:
		count += 1
		assert(v.t == p.v.t)
		if p.v.isCloned():
			assert(v.isCloned())
			assert(len(vnodeList) &gt; 1)
		else:
			assert(not v.isCloned())
			assert(len(vnodeList) == 1)
	
	p.moveToThreadNext()
		
print ; print "checked %d cloned nodes" % count</t>
<t tx="ekr.20040302114642">from leoGlobals import *

c = top()
c.convertTreeToSharedNodes()
c.disableSaveCommands()

print ; print "checking threadBack/threadNext"

p = c.rootPosition() ; count = 0

while p:
	count += 1
	threadBack = p.getThreadBack()
	threadNext = p.getThreadNext()
	if threadBack:
		if threadBack.getThreadNext() != p:
			print "p.threadBack.threadNext != p"
			print "p,threadBack,threadBack.threadNext:"
			print p,threadBack,threadBack.getThreadNext()
		assert(threadBack.getThreadNext()==p)
	if threadNext:
		if threadNext.getThreadBack() != p:
			print "p.threadNext.threadBack != p"
			print "p,threadNext,threadNext.threadBack:"
			print p,threadNext,threadNext.getThreadBack()
		assert(threadNext.getThreadBack()==p)
	p.moveToThreadNext()

print ; print "checked %d nodes" % count</t>
</tnodes>
</leo_file>
