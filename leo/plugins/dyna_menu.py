#@+leo-ver=4-thin
#@+node:ekr.20050328091952.2:@thin dyna_menu.py
#be sure and add dyna_menu.py to pluginsManager.txt
#you don't need to enable dynacommon.py in pluginsManager.txt
#you do need dynacommon.py in the plugins directory 
#and edit the paths in dynacommon.py to suit your system.
#as time goes by, this part will become smarter and require less editing.
# see dyna_menu.ini for other options you can set, even while Leo is running.

#for py2.2 you have to enable from __future in initilize
#

"""this plugin creates a dyna menu of macro items.
 Alt+y the dyna menu accelerator key.   
 every time you save the leo one of the macros prints a timestamp.
 macros perform any actions you could have with execute script,
 with the added bonus, they work on the selected text or body text.
 they work as well from the dynatester node or dynabutton, insuring
 when they are included in the plugin, minimal time is lost debugging.

 add exS may re-install exS button on the toolbar.
 set doc and hit DQ3 with nothing selected to see docstring of all macros.
 

do post a bug report or feature request
on my comment page from:
 http://rclick.netfirms.com/rCpython.htm
or sourceforge forum:
<http://sourceforge.net/forum/forum.php?thread_id=1070770&forum_id=10226>

temporary latest version page.
http://rclick.netfirms.com/dyna_menu.py.html

expect constant maintance and additions

still todo
remove more bare Exception.
bribe someone to test it on mac and nix and give some feedback.
on windows remove the dos command window flash with pyw in htmlize 
"""   
__version__ = '0.0139c'  #m05328a03:50
__plugin_requires__ = ["dynacommon"]
#probably mention it elsewhere, some macros do need some non standard modules
#fallbacks or from later python versions in some cases

#@<< initilize >>
#@+node:ekr.20050328091952.3:<< initilize >>

from __future__ import generators  # + enumerate for less than py2.3
#@+at
# from future has to be first...
# but to check py version you have to import sys
# isn't that some kind of catch 22?
#@-at
#@@c
import sys
import ConfigParser
try:
    enumerate([])
    #print 'have enumerate'
except NameError:  #?
    def enumerate(seq): return zip(xrange(sys.maxint), seq)
    print 'now have enumerate'

import leoGlobals as g

Tk   = g.importExtension('Tkinter',pluginName=__name__,verbose=True)

#at this point in Leo, code from plugins isn't importable. later it is.
#replace w/importfromfile
#or patch leo to add plugindir sooner rather than later...

k = g.os_path_split(g.app.loadDir)[0]
#this should fix the slashes and lower cases' it on win9x
k = g.os_path_normpath(g.os_path_abspath(g.os_path_join(k, "plugins")))

#path being unicode can affect less than py2.3
if sys.version_info[:2] < (2, 3):
    k = str(k)

#might not be found in sys path on win9x, there is no unicode paths
if k not in sys.path:
    sys.path.append(k)
del k


#should this even be imported if batch mode or no Tk?
try: 
    #import dynacommon as dy
    from dynacommon import *  #should use importfile?
    dynacom = True
except ImportError: 
    dynacom = None
    #no gui maybe print better here? should guard the error too?
    g.es('you have to copy dynacommon.py to plugins')

"""
 to disable the timestamp thing, comment out this line below:
   ...registerHandler("save1", timestamp) 

for refrence, dynabutton and exS were other plugins from the URL below.


 macro items will be added from the macros subnode.
 technically, any function starting with the name 'dyna*_'.
 toggle print/paste in dynabutton or dyna_menu 
 only affect macros in their respective menus.
 toggle print/paste/doc on the menu. 
 you click on print, paste or doc to enable that action.
 the action refers to the output of the macro in most cases.
 open another leo resets back to print 
 because all dyna share an instance.

 there is a status display associated with some actions.
 most output actions are to the log,
 or using print redirected to log if you set that in config.
 'print' gets redirected to console if the macro is in the plugin.
 you have to change the macro accordingly from print x to g.es(x) 
 can't be helped. various macro's solve their own output problems.
 

with the dyna plugin loaded you can do things in your scripts like:
    
import sys
#theres probably an easier way than this.
sys.modules['dyna_menu'].dynaM_Clip_dtef(0, 'p')

#another way
import dyna_menu
#print help(dyna_menu)
#print dir(dyna_menu)  #dynaM_
print dyna_menu.dynaHexdump('testing 123')


#some macros that work on selected text maybe should seperate
#their data transformation from their aquisition of data.
#which wouldent depend on c. like this def in dump body.
Hexdump = sys.modules['dyna_menu'].dynaHexdump
print Hexdump('help')
assumes dyna plugin is loaded, would need default or try/except for use.

hard to know beforehand what might be reused in other macros.
reuse is more an art than a science, but using smmaler functions
that do something specific and not depending on global magic helps.
its also easier to test single well defined functions.


lightly tested with py2.2 or Leo4.3a3,4+ from cvs
tested Python 2.3, 2.4.1 win9x

should not be a problem anywhere else.
but don't quote me on that. make a bug report.

for a productivity boost on windows,
http://www.geoshell.com replacement explorer shell
mulitiple window views, floating toolbars with many plugins
opensource, source available for plugins.
(not connected in any way, its just amazing)

see firefox browser for an enlightning approach to user options
based on the Netscape user.js and chrome.css and adds themes.

e
"""
#@nonl
#@-node:ekr.20050328091952.3:<< initilize >>
#@nl
#@<< version history >>
#@+node:ekr.20050328091952.4:<< version history >>
#@+at
# 0.0138 few changes since forum post
# 
# 0.0139 e
#   - updates re Leo4.3 normpath and c for a few dialogs
#   - some config options for htmlize and du_test
#   - htmlize
#    - code folding: still in process
#    - improvements suggested by EKR & Bill P. not fully implimented
#       change fonts to css as an option  no
#       add a plain or RST output option  no
#       hey I could use that myself quite  bit!
#       did add option to stripnodesents, and stripdirectives & stripcomments 
# now works
#  - use subprocess if available when calling external pychecker & pylint
#  - made justPychecker an option not to print source after checking
#   - if you dont want to run pylint you have to edit the source.
#   - pylint is more configurable and doesn't fail on import errors now
#   - highly recomended. see dyna.txt for rc file and URLs'
#   - added a few more flippers from the plugin_menu
#     - for Leodebug, justPychecker and verbosity for @test and doctest
#   - added back a macro uses dynaplay to comment out a python selected text
#     many people asked for this, should get comment for whatever language is 
# active.
#     Leo can do this natively now but dyna can also put arbitrary text if you 
# like.
#   - cmd_flip_onoff_c_gotoline
#   - htmlze
#     -   switch on plain or rst, force @others and send to for docutils
#        and there if there are subnodes of @language preprocess them
#        somehow and this gets recursive and complicated...
#     -  option on src-highlite or silvercity for the remaining languages
#   + fix evaluator to select between Leo perttyprint, evaluator and
#   + /UTIL/DLL/astyle.exe?--pad=oper --style=kr %N for  c,java & python +?
# -a,b, leapahead to fix htmlize for plain and @rst as simple as possible
#@-at
#@nonl
#@-node:ekr.20050328091952.4:<< version history >>
#@nl
NDebug = True and False
dynaMvar = None
#@+others
#@+node:ekr.20050328091952.5:macros
#@+at
# 
# in theses macro nodes, copy or clone the macros
# you want to appear in dynamenu
# 
# dynaM_ or dynaS_ for macro and system macro
# arbitrary to segment into cascading menus at build time
# see load_menu, dont use beyond Z as a macroname dynaZ_whatever
# change the letter to change the order the macros are created
# change the name of the macro to change the alphabetical order.
# 
# not alot of error checking is done
# each macro must have the same name prefix, dyna*_
# and either take *a or c as argument
# dynaM_DQ3(c)  they appear in the menu in sorted order
# 
# 
# for other less used macros,
# use the dynabutton or the scriptButton
# 
# some of these are calling function further in the file
# that only works becase all parsing is done before calling
# 
#@-at
#@+node:ekr.20050328091952.6:info macros
#@+node:ekr.20050328091952.7: Clip_dtef

def dynaB_Clip_dtef(c, ret= 'cp'): #doesnt use c, clip, print, return
    """add time text to the clipboard
    ret='cpr' decide if to add to clipboard, print or return time text


    """
    try:
        #custom datetime format
        import binaryfun as bf
        dt = bf.dtef()
    except ImportError:
        import time
        #or whatever, Leo can insert time in body or headline
        #Leoconfigformat = '%m/%d/%Y %H:%M.%S'
        #dt = time.strftime(Leoconfigformat) 
        dt = c.getTime(body=True)

    if 'p' in ret: g.es('%s%s '%(EOLN, dt,) )
    if 'c' in ret: g.app.gui.replaceClipboardWith(dt)
    #ret = r necessary, if dont specify it clips & prints by default
    if 'r' in ret: return dt  
#@-node:ekr.20050328091952.7: Clip_dtef
#@+node:ekr.20050328091952.8:Graphviz node

def dynaB_Graphviznode(c= None):
    """take the EKR Graphviz pydot demo
    see the 4.2+ test.leo for the origional and other info
    http://www.dkbza.org/pydot.html
    http://www.research.att.com/sw/tools/graphviz/download.html
    pydot, python setup.py install
    install the full Graphviz in a subdir somewhere on  the path
    pydot has a path walker that will find it.
    works on win.

    bring it back down to 4.1 standards and macroize it
    put in a switch for >4.1 use the origional calls
    
    works on any node now. best if there are not too many subnodes
    the graph gets too dense and small
    
    the other demo graph node outline builder worked 4.1.
    also have to refocus. the demo was to visualize 4.2 t\/v nodes
    I dont need to see the numbers just the headlines
    some things are compatable some not. 
    need to dev a good list of what works
    list of cvs commits would help here maybe if the docs dont keep up.
    its not going to make a whole lot of sense in less than 4.2
    untill I find out about the diferences
    makes a nice looking graph though!

 a dependancy graph of which modules a program uses might be doable.
 more nodes for pieces in the module and other filesystem dependancies.
 
 
    numberOfChildren() nthChild(n) lastChild()
    """
    import leoGlobals as g
    import os
    import string  #why?
    try:
        import pydot
    except ImportError:
        g.es('you need http://www.dkbza.org/pydot.html')
        return

    try:
        import dynacommon as dy
        #reload(dy)
        fname = dy.leotmp('pydotOut.jpg')
    except ImportError:
        fname = 'pydotOut.jpg'
        

    #there is a way to know this for sure
    #you still might want to specify it
    Leo = 4.2


    if c is None: c = g.top()

    if Leo > 4.1:
         p = c.currentPosition()
    else:
         p = c.currentVnode()

    #@    << code >>
    #@+node:ekr.20050328091952.9:<< code >>
    #@+others
    #@+node:ekr.20050328091952.10:addLeoNodesToGraph
    
    def addLeoNodesToGraph(p, graph, top= False):
        """
        p.v attribute is 4.2, this might be a dealbreaker for 4.1?
        butchering it up just to get some output
        the node ovals are too large
        
        """
    
        # Create p's vnode.
        if Leo > 4.1:
            n = vnodeRepr(p.v)
            l = vnodeLabel(p.v)
        else:
            n = vnodeRepr(p)
            l = vnodeLabel(p)
    
        thisNode = pydot.Node(name= n, label= l)
        graph.add_node(thisNode)
    
        
        if p.hasChildren():
            child = p.firstChild()
            childNode = addLeoNodesToGraph(child, graph)
            graph.add_node(childNode)
    
            if Leo > 4.1:
                e1 = tnodeRepr(p.v.t)
                e2 = vnodeRepr(child.v)
            else:
                e1 = tnodeRepr(p)
                e2 = vnodeRepr(child)
    
            edge2 = pydot.Edge(e1, e2)
            graph.add_edge(edge2)
    
            
            #     child.next() could error?  hasattr(child, 'next()')?
            while child.next():  #child.hasNext() 4.2
                next = child.next()
                
                if Leo > 4.1:
                    e1 = vnodeRepr(child.v)
                    e2 = vnodeRepr(next.v)
                else:
                    e1 = vnodeRepr(child)
                    e2 = vnodeRepr(next)
    
                edge =  pydot.Edge(e1, e2, dir="both")
    
                nextNode = addLeoNodesToGraph(next, graph)
                graph.add_node(nextNode)
                graph.add_edge(edge)
                child = next
                
        if 1:
            if Leo > 4.1:
                n = tnodeRepr(p.v.t)
                l = tnodeLabel(p.v.t)
            else:
                n = tnodeRepr(p)
                l = tnodeLabel(p)
    
            tnode = pydot.Node(name= n, shape="box", label= l)
            
            if Leo > 4.1:
                e1 = vnodeRepr(p.v)
                e2 = tnodeRepr(p.v.t)
            else:
                e1 = vnodeRepr(p)
                e2 = tnodeRepr(p)
    
            edge1 = pydot.Edge(e1, e2, arrowhead= "none")
            graph.add_edge(edge1)
            graph.add_node(tnode)
        
        if 0: # Confusing.
            if not top and p.v._parent:
                edge = pydot.Edge(vnodeRepr(p.v),vnodeRepr(p.v._parent),
                    style="dotted",arrowhead="onormal")
                graph.add_edge(edge)
    
        if 0: # Marginally useful.
            for v in p.v.t.vnodeList:
                edge = pydot.Edge(tnodeRepr(p.v.t),vnodeRepr(v),
                    style="dotted",arrowhead="onormal")
                graph.add_edge(edge)
    
        return thisNode
    #@nonl
    #@-node:ekr.20050328091952.10:addLeoNodesToGraph
    #@+node:ekr.20050328091952.11:tnode/vnodeLabel
    
    def tnodeLabel(t):
    
        if Leo > 4.1:
            tl = len(t.vnodeList)
        else:
            tl = 0
    
        return "t %d [%d]" % (id(t), tl)
        
    def vnodeLabel(v):
        
        return "v %d %s" % (id(v),v.t.headString)
    #@-node:ekr.20050328091952.11:tnode/vnodeLabel
    #@+node:ekr.20050328091952.12:tnode/vnodeRepr
    
    def dotId(s):
        """Convert s to a C id"""
    
        s2 = [ch for ch in s if ch in (string.letters + string.digits + '_')]
        return string.join(s2,'')
    
    def tnodeRepr(t):
    
        return "t_%d" % id(t)
        
    def vnodeRepr(v):
        
        return "v_%d_%s" % (id(v),dotId(v.headString()))
    
    #@-node:ekr.20050328091952.12:tnode/vnodeRepr
    #@-others
    #@nonl
    #@-node:ekr.20050328091952.9:<< code >>
    #@nl
        
    graph = pydot.Dot(simplify= True, ordering= "out")

    root = p  #g.findNodeInTree(p, "Root") #another 4.2ism or in leotest

    addLeoNodesToGraph(root, graph, top= True)
    graph.write_jpeg(fname, prog= 'dot')

    g.es('graph of outline written to \n' + fname)
    import webbrowser
    webbrowser.open(fname, new= 1)

if __name__ != 'dyna_menu':
    dynaB_Graphviznode(c= None)
#@nonl
#@-node:ekr.20050328091952.8:Graphviz node
#@+node:ekr.20050328091952.13:linenumber

def dynaB_linenumber(c):
    """show selected text or body as Leo sees it, 
    numbering lines or if there is an integer in copybuffer,
     show just +- a few lines around that number.
    syntax errors, indentation errors ,  missing closing paren
    missing colon ':'  in def, if, class
    the actual error can be ahead or behind of the reported error line.
    often at the top of the block continuing the error.
    it wouldn't hurt to examine the bottom and middle either.
    sometimes a symptom is an undefined identifier that looks fine.
    you have to trust what you know, otherwise you will change
    10 things before you get to the point of the error. bad instinct
    at this point to change too many things. you still aren't going
    to see the effect of the change until the original error is fixed.
    in the cut paste and retry programming that I often do, its
    best to change only very few things and make sure you will see 
    the effect of the change while you're looking for it.
    and that the change will be tested with some part of the test 
    or an assert if you don't run -OO as you shouldn't do while testing.
    that -OO also limits the docstrings you get from help.
    watch the actual line endings. very often while pasting
    you can inadvertently have one line in a texteditor that wraps
    and lineup the indentation after the paste not realizing
    it's a line continued from the previous paste. 
    blank lines can be suspect too as they might have an odd number
    of spaces. show invisibles or run that section thru reindent.
    #@    << more debugging tips >>
    #@+node:ekr.20050328091952.14:<< more debugging tips >>
    #@@nocolor
    pass, often needed if you comment out the only live statements
     in a try/except or if/else block
     
    shadowing builtin names str, dict, file, list are popular,
    until a few lines later you try to use the function.
    its usually bad form to upper case a shadowed name just to
    get around the restriction. List instead of the builtin list.
    many people consistently name their classes and functions.
    in other languages even tagging variable names with the type.
    
    bugs can eat up much time and cause frustration for simple mistakes.
    you have to debug from the top of the file to the bottom.
    python wont evaluate something till it gets there. but, there
    must be no syntax errors anywhere. sometimes it helps to break
    down step by step line by line what you think will happen.
    actually describing what will happen sometimes makes' errors' obvious.
    a voice synthesizer here might even work. many bugs are that simple.
    
    properly formatted python (to your mind) helps to point out
    statements and expressions that might be in error.
    luckily most indentation errors are syntax errors 
    rather than logic errors which would be orders of magnitude
    harder to catch and laying in wait as latent bugs to trouble you later.
    if you indeed ever did catch them. 
    this is why the focus on unittests, coverage tools pychecker etc.
    which only can help if the file can be imported.
    hence my focus on evaluator using some of the techniques in pychecker2.
    
    run the code thru reindent wont always fix the problem.
    but its a good first step and is why the macros that run pychecker
    run thru reindent first. you can paste over the copy of your program
    or those sections that are troubling. 
    don't mix tabs and spaces. Edit -> Edit Body -> convert all tabs.
    a hexdump of the offending section sometimes will turn up
    a control code or other line ending problem.
    personally I never use tabs and always use unix lineendings 0x0A,
    unless it's a bat file which requires 0x0D0A.
    the other editor I use is EditPad which transparently writes
    in the same lineendings as the file has to begin with,
    you can move EditPad to notepad and windows will use it.
    
    forgetting self, as the first parameter to a class method.
    
    separate multiple statements/expressions on their own line.
    use temp variables to simplify and make readable complex expressions
    you can always reoptomize it back to gibberish later.
    
    its misplaced brain power to force too many mental caveats while
    you are trying to debug a section of code. one of the things I
    most was surprised at when I began learning python coming from
    c and javascript as my first and 2nd language, was how much I
    was depending on the preprocesser for macros to simplify code.
    and optimizations like in javascript and still useful 
    in python of making a temporary bind to localize globals.
    La = L.append  # speeds up access inside a loop.
    what you forget when you go overboard and code first in this way
    is that it is so often in parts of code that don't get exorcized
    much where the errors are. all the premature optimization does
    is leave the code un readable for later maintenance and debugging.
    I totally under estimated the amount of extra work it takes to
    lookup all these little code shortcuts later when you have to change
    something. there must be a more concise way to say that.
    
    
    turn on Leos Edit -> show invisibles command
    actually derive a file and look at it
    add @file whatever.py or whatever.ext 
    write @file and get an eye on it.
    
    extract section to further localize the error.
    turn a section of code into a function or method, this
    will often expose a dependance on a global that is wrecking havoc.
    
    from c.l.py w/o permission except the obvious
    Another problem that arises from time to time which produces the effect
    described by the OP is an "unclosed parens", that is, a parens that was
    open and never closed (or a square bracket).
    
    As Python considers an unclosed parens as an implicit continuation of
    the statement in the following line, the error is often "detected" in
    some place PAST the actual error.
    
    Something similar happens with "unclosed strings", but any editor with a
    decent syntax highlighting makes you notice this almost instantly.
    from Eru.
    
    
    try to create something that will repeat the error, in 
    the smallest possible amount of text. then report it.
    the process of simplification will often provide the answer.
    
    
    finally, and as a very, very last resort, blame the tools.
    might be something in how Leo derives file 
    or even how python is parsing it.
    take a break, sleep on it. read a few cookbook recipes,
    ask someone else to look at the code with fresh eyes.
    
    its entirely possibly the current algorithm will be superseded
    by further research anyway, why wait. don't sweat the small stuff.
    rip out the offending code and substitute some black box data 
    returned by a stub and press on, 
    endless debugging can be its own reward. like sand castles.
    
    Leo's goto linenumber works from the derived @file
    fixbody uses similar calls to find its line numbers.
    note: in some cases 
    some forms of fixbody with nothing selected 
    will strip out Leo @directives rather than comment them out.
    this will become fully consistent in the future.
    you know, the future where all the bugs are easy to describe.
    you should expect at least one anomaly per 100 lines of code.
    otherwise you're not working hard enough.
    
    it maybe that Edit-> gotolinenumber can never be correct because
    execute script strips the @directives. derived files comment them.
    I think exscript now includes directives in Leo4.2, Yha! I think.
    #@nonl
    #@-node:ekr.20050328091952.14:<< more debugging tips >>
    #@nl

    further enhancement, keep track of last section ref node
    last def last method of last class and output all the lines together
    rather than one at a time which can tie up Leo on long programs.
    should output current path and language and wrap to current wrap
    -n +n could be under/over the abs(int) in copy buffer

    could make it jump to linenumber based on env variable
    that way you wouldn't have to remake the plugin to change behavior
    several other macro also could use settable params at ex script time.

    selected text doesnt show sentinalsm but exscript uses them
    so lineenumber on selected text may not jive after an error
    
    might be a bit much for a docstring  
    """

    newSel = dynaput(c, [])
    #nothing selected will include sentinals
    data = fixbody(newSel, c) 
    datalines = data.splitlines()

    pln = g.app.gui.getTextFromClipboard()
    try:
        pln = int(pln)
        g.es('using line # %d'%(pln,), color= 'turquoise4')
    except Exception, err:
        g.es('no int in copy buffer', color= 'turquoise4')
        pln = 0

    if pln > len(datalines) or pln < 0:
        #who would select zero to print the first line?
        #maybe zero should be all lines as it would be if zero
        g.es('int found is out of range', color= 'turquoise4')
        #still possible to break and maybe too many messages
        if pln > len(datalines): pln = len(datalines) - 5
        if pln < 0: pln = 5

    for i, x in enumerate(datalines):
        if pln and i < (pln - 5): continue
        if pln and i > (pln + 5): break

        #would rather not go thru this every time thru the loop
        if pln and i == pln:
            colr = 'gray'
        else: 
            colr = 'slategray'

        g.es('%- 3d '%(i,), newline= False, color= colr)

        g.es('%s'%(x,))
    g.es('There are %s lines in ? nodes'%(
            len(datalines),), color= 'turquoise4')
#@-node:ekr.20050328091952.13:linenumber
#@+node:ekr.20050328091952.15:nflatten

def dynaB_nflatten(c= None):
    """like flatten but in macro so can
    print/paste or copy to buffer eventually. now out to log.
    should limit the recursion to less than the normal limit
    isn't following the more format of +-
    chg to int, add index level, seperate out the recursive function
    so can return body size and assmble totals
    what is the meaning of the totals if index is one though?
    obviously have to get all and total in here, next refactor for that.

    show if there are subnodes even if dont enumerate.
    dynacolors being a global when run from dyna_menu makes this
    problematic when run from scriptButton now while debugging...
    going to have to exS with dynacommon namespace or something
    or import common if any macr needs them. more complications.
    should just extend g and be done with it

    uses dynacommon deangle, commafy 
    an ini setting could select just @nodes or just @file
    another could leave off the node counts and totals
    
    silly to create a newline connected string of rendered ints
    then splitlines and int on the split string! 
    better just return list of tupple?
    will make no sense to anyone except if they've seen previous version
    but is a major simplification, 
    why it happened in the first place, is surely a mystry.
    there may be a marginal tradeoff of computation for size of list
    and in a recursive function this might matter, we'll see how it goes.
    next will have to resolve why the total of all nodes != filesize
    not even counting @thin etc
    """    
    import leoGlobals as g
    if c is None:
        c = g.top()

    tbytes = 0
    oline = _nflatten(c, index= 1, sx= [])
    g.es("headString, +nodes, bytes")
    for st in oline:
        try:
            i, hs, sz, nz = st
            g.es("%s%s, +%d, %s"%(
                (' '*i), hs, nz, 
                      g.choose(sz<1024,
                       '%s'%sz, '%sk'% commafy(sz, '.')) ),
                     color= dycolors.gFuchsia)
            tbytes += sz
        except Exception:
            g.es(" ", s, dynaerrline(), color= dycolors.gError)  #

    if len(oline) > 1:
        g.es(" =%s"%(
            g.choose(tbytes<1024,'%s'%tbytes, '%sk'% commafy(tbytes, '.')),
            ), color= dycolors.gFuchsia)
        

def _nflatten(c= None, current= None, indent= 0, index= 0, sx= None):
    """may be trying to combine too many things
     efficency out the window to boot.
    """
    if current is None:
        current = c.currentPosition()
        t = (indent, deangle(current.headString()[:50]),
            len(current.bodyString()), len(list(current.children_iter())) )
        #g.es(t, color="purple")
        sx.append(t)
        indent += 2

    for p in current.children_iter():
        t = ( indent, deangle(p.headString()[:50]),
            len(p.bodyString()), len(list(p.children_iter()))  )
        #g.es(t)
        sx.append(t)
        if p.hasChildren() and index >0:
            _nflatten(c, p, indent +2, index -1, sx)
            continue

    return sx

#need dynatester to supply missing color definitions to doctest
#dynaB_nflatten()
#@nonl
#@-node:ekr.20050328091952.15:nflatten
#@+node:ekr.20050328091952.16:fileinfo

#@+others
#@+node:ekr.20050328091952.17:print perms

def perms(name):
    """
    a=\xc3 Padraig Brady - http://www.pixelbeat.org
     -rw-rw-rw- leo\src\..\config\leoConfig.txt
    """
    import sys
    import stat
    import os
     
    mode = stat.S_IMODE(os.lstat(name )[stat.ST_MODE ])
    #print mode
    perms = "-"
    for who in "USR", "GRP", "OTH":
        for what in "R", "W", "X":
            if mode & getattr(stat, "S_I" + what + who ):
                perms = perms + what.lower()
            else:
                perms = perms + "-"
    return perms
 
#@-node:ekr.20050328091952.17:print perms
#@-others

def dynaB_fileinfo(c= None, fname= None):
    """ show some basic file info size, create date etc.
    try to get filename from selected text then copybuffer,
    if none of these are valid filenames using os.isfile,
    then will try to get current @file @rst path & name,
    then finally c.mFileName of current leo.
    if more than one of these is True, 
    then its up to you to move out of that node, select or whatever.
    feel free to impliment the more stodgy browse to file name first idiom.
    
    might popup a dlg to set attributes in v9
    should get user name also
    winUserName = win32api.GetUserName()
    macUserName = ?
    nuxUserName = expand('~')?
    """
    import leoGlobals as g
    import os, time

    drif = 0 #do report intermediate failures 

    if c is None: c = g.top()

    def normit(fn): 
        #seems redundant till you get a weird join it fixes
        return fn  #g.os_path_norm()

    if fname is None:
        fname = c.frame.body.getSelectedText()
        if not g.os_path_isfile(normit(fname)):
            if drif and fname: g.es("- ", fname[:53])
            fname = g.app.gui.getTextFromClipboard()

        #chg 1 to 0 or will never try for @file
        if 0 and not g.os_path_isfile(normit(fname)):
            if drif and fname: g.es("- ", fname[:53])
            fname = 'python.txt' #testing default

    if not g.os_path_isfile(normit(fname)):
        if drif and fname: g.es("- ", fname[:53])
        fname = 'the current @file'
        p = c.currentPosition()
        #leocommands has goto should be using an API call to get filename.
        #coping some of the relevent code, its a jungle in there...
        #seems ok on @nosent, goto should be fixed since it skips them

        fileName = None
        for p in p.self_and_parents_iter():
            fileName = p.anyAtFileNodeName()
            if fileName: 
                break
            if p.headString()[:4] == '@rst':
                #this can fail if not the first @rst
                fileName = p.headString()[4:]
                #c:\c\leo\V42leos\ /c/leo/HTML/Colortest.html via join
                break

        if not fileName:
            if drif: g.es("ancestor not @file node")
        else:
            root = p.copy()
            d = g.scanDirectives(c)
            path = d.get("path")
            #need the directive length, thin, file-thin etc [1:] 

            fname = root.headString()
            fname = fname[fname.find(' ')+1:]
            fname = g.os_path_join(path, normit(fname))
            if not g.os_path_isfile(normit(fname)):
                #will double the msg if drif, 
                #but you might want to know
                g.es("not exists", fname[:53])

    if not g.os_path_isfile(normit(fname)):
        if drif and fname: g.es("- ", fname[:53])
        fname = c.mFileName #can fail if not saved

    if not g.os_path_isfile(normit(fname)):
        g.es("no valid filename found %s"% str(fname[:53]))
        return 

    #print g.file_date(fname, format=None)
    #print os.path.getatime(fname)
    fname = normit(fname)
    try:
        h = "%s % 5dK  %s\n%- 18s c) %24s m) %24s"%(
            perms(fname),
            os.path.getsize(fname)/1024L,       #comafy
            g.os_path_split(fname)[0],          #dirname
            g.os_path_split(fname)[1],          #text
            time.ctime(os.path.getctime(fname)), #is this locale?
            time.ctime(os.path.getmtime(fname)),
        )
    except (OSError, Exception):
        g.es_exception()
        h = fname

    g.es(h)
    #return h

if __name__ != 'dyna_menu':
    dynaB_fileinfo()
#@nonl
#@-node:ekr.20050328091952.16:fileinfo
#@-node:ekr.20050328091952.6:info macros
#@+node:ekr.20050328091952.18:text macros
#@+node:ekr.20050328091952.19:+dyna_backslash

def dynaM_backslash(c):
    """create a file monicur out of a path for IE or NS4
    @url file://some.bat will work, not sure with %20 can add params
    or chg forward or backslash to the other. add "'s or %20 for spaces
    dblclick on @url might not open IE for some reason
    r04212p7:05 whiped up out of my head in few mins
    editpad can't handle path with forwardslashes.
    u04509p08:56:53  cvrt to dyna, somehow need to select which...
    using copy buffer or just flip b\/f slashes
    should add 8.3 to longfilename and back
    dblbs isnt working, it want to flip bs/fs if they exist whatever else
    should probably just output the path in every way possible
    folowed by space delimited words make into valid get url
    backslash doesnt seem to flip back from slash again
    """
    newSel = dynaput(c, [])
    if not newSel: return
    newSel = str(newSel)

    repchar = g.app.gui.getTextFromClipboard()
    if not repchar in ['/', '\\' '\\\\', ':', '|', ' ',]:
        #if nothing in copy buffer flip the back/forward slashes
        if newSel.find('/') != -1:
            repchar = '\\'
        elif newSel.find('\\') != -1:
            repchar = '/'
        elif newSel.find('~') != -1:  #could be 8.3 also
            repchar = ':'
        
    sx = []
    for x in newSel.splitlines(True):
    
        if x == '': continue
    
        #check is valid, starts with drive : and has no non printables
    
        if repchar == ':':
            s =  x.replace('\\\\','\\').replace('\\','/').replace(':','|') 
            s = s.replace(' ','%20')
            sx.append('file:///' + s)
        elif repchar == '|':
            s = x.replace('file:///','').replace('|',':').replace('/','\\') 
            s = s.replace('%20',' ')
            sx.append(s)
    
        elif repchar == '\\\\':
            sx.append(x.replace('/','\\').replace('\\','\\\\') )
    
        elif repchar == '\\':
            sx.append(x.replace('/','\\') )
    
        elif repchar == '/':
            sx.append(x.replace('\\\\','\\').replace('\\','/') )
    
        elif repchar == ' ':
            sx.append(x.replace(' ','%20') )

        else:
            #sx.append(' " ",/,\\,:, %s'%(x,) )
            g.es(' err', x)
        
        g.es(' repchar= %r x=%r'%(repchar,x) )
        dynaput(c, sx)


#
#by pass while in plugin,
# for testing while included in dynatester node
#
if __name__ != 'dyna_menu':
    try:
        __version__
    except NameError:  
        def testbs():
            #some test paths , better encapsulation
            lst= r"""
            L:\\c\\Python22\\Doc\\lib\\modindex.html
            L:\c\Python22\Doc\lib\modindex.html
            C:/TEMP/leo/leo4CVS/plugins/mod_rclick.py.txt
            L:\c\Progr\leo-3.7\info\doc\ASPN
            file://L|/c/Progr/leo-3.7/info/doc/ASPN
            """.splitlines(True)
            lst =  [x.lstrip() for x in lst]
            return lst

        #need to have a better way to run all the lines
        # (cbuf, input, expected output)
        #need way to get something into the copy buffer 
        genteststr.tstlst = testbs()
        testmacro = 'dynaM_backslash'
#@-node:ekr.20050328091952.19:+dyna_backslash
#@+node:ekr.20050328091952.20:geturls

def dynaM_geturls(c):
    '''extract all urls from selected text. included som extra text.
    doesnt span line endings. misses any number of other mal formed urls.
    might use some ideas from the extend rclick post on sf.
    not 100% reliable and not intended to be the last word in re use.
    reconstruction of the found url is at this point just exploratory.

    testing in redemo, modifyed to include rClickclass 
    and multiline text for re's instead of single line entry.
    kodos works too, but always seeems a little less reliable

    some might want the ability to open the default browser with the url
    thats best let to another plugin or macro or could optionally
    add it to the clipboard which there isnt a clean way to do yet.
    
    seplit out into a dev version.
    add email harvester stage.
    view partial source on a list of url links will add cvrt to &amp;

click enable for geturls, create a page on the fly with the urls
pass it to IE so you can rclick on them
create a numbered range creator 

    added a sort step
   does py2.2 urllib have unquote_plus? remove %20 %7E stuff

    '''
    newSel = dynaput(c, [])
    if not newSel: return
    try:
        data = str(newSel)
    except (UnicodeEncodeError, Exception):
        g.es_exception(full= False)
        data = newSel


    import re, urllib

    #from leo
    # A valid url is (according to D.T.Hein):
    # 3 or more lowercase alphas, followed by,
    # one ':', followed by,
    # one or more of: (excludes !"#;<>[\]^`|)
    #   $%&'()*+,-./0-9:=?@A-Z_a-z{}~
    # followed by one of: (same as above, except no minus sign or 
    # comma).
    #   $%&'()*+/0-9:=?@A-Z_a-z}~
    #thers problems with this, I forget what just now.
    #
    #http etc from rClick plugin extension idea posted to leo forum, works
    #scan_url_re="(http|https|ftp)://([^/?#\s]*)([^?#\s]*)(\\?([^#\s]*))?(#(.*))?"
    #re.sub(scan_url_re,new_url_caller,text)  #leaves out a few types
    #
    #r04422a05:03:35 mine still doesnt match everything, and doesnt submatch as well
    #w04519p05:58:10 make a try at verbose,
    #shold relax it from expecting perfect links
    

    #leaves out a few types wais
    # excluding all invalid chars is always for security & sanity
    # worse than including all valid chars, there will be ommisions
    scan_url = r"""
   ([s]*http[s]*|ftp[s]*|[s]*news|gopher|telnet|prospero|link|mailto|file|ur[il])(://)
    ([_0-9a-z%]+?
    :?
    [_0-9a-z%]+?@?)  #takeing some liberties
    ([^/?#\s"']*)
   ([^?#\s"']*)
    (\?*[a-z0-9, %_.:+/-~=]*)
    (\#*[a-z0-9, %_.:+/-~=]*)  #lookup exact name ref link standard
     (&*[a-z0-9, %_.:+/-~=]*)  #needs work
     ([^"<'>\n[\]]*)  #catch the rest till learn repeat
 #   (#|&*[^&?]*.*)
    """
    #(\?*[^&#"'/>\\]*[a-z0-9, %_-~]*?)
    #(\?([^#\s]*?))  #this is doubling the params
    #(&(.*)*?)
    #(#(.*)*?)  
    #end game, this fails
    #urllib.unquote_plus( urllib.quote(

    scan_url_re = re.compile(scan_url, re.IGNORECASE | re.MULTILINE | re.VERBOSE)
    ndata = scan_url_re.findall(data)  #leaves out :// and /
    sx = []
    if ndata:
        g.es('just urls:')
        for x in ndata:
            if not x: continue
            xfixed = list(x)
            #print xfixed
            # some cnet addresses use quot?
            xfixed = [s.replace('&amp;', '&').replace('&quot;', '"')\
                            for s in xfixed]
            try:
                xfixed = [urllib.unquote_plus(s) for s in xfixed]
            except Exception:
                pass

            sx.append( ''.join(xfixed) + '\n')
            #note, this can totally screw things up...
    else: g.es('no urls')  #, data

    #sets another way to get uniq
    #sx = [x for x in dict(sx)] #uniqs it, has problems
    d = {}
    for x in sx:
        d[x] = 1
    sx = [x for x in d.keys()]
    sx.sort()
    dynaput(c, sx)


#
#by pass while in plugin,
# for testing while included in dynatester node
#
if __name__ != 'dyna_menu':
    try:
        __version__
    except NameError:  
    
        def testbs():
            lst = ["""\
http://uid:pw@adwords.google.com:80//http://www-106.ibm.com/""", """\
windows are.</SPAN><BR><BR>[<A target=_blank 
href="http://www.geoshell.com/plugins/zoom.asp?id=244">download</A>] [<A 
target=_blank href="http://docs.geoshell.com/R4/GeoXWM">documentation</A>] 
</DIV>""", """\ http://www-106.ibm.com/search/searchResults.jsp?searchType=1&searchSite=dW&query=python&searchScope=dW&Search.x=0&Search.y=0
    shttps://adwords.google.com/%7Esup%27port/bin/topic.py#topi
    https://adwords.google.com/support/bin/topic.py?topic=102
        href="http://www-106.ibm.com/developerworks/css/r1.css" type="text/css"/>')
        else if ((navigator.userAgent.indexOf("X11"))!= -1) 
             """] 
            #print 'lst =', lst
            return lst
    

        genteststr.tstlst = testbs()
        testmacro = 'dynaM_geturls'
#@nonl
#@-node:ekr.20050328091952.20:geturls
#@+node:ekr.20050328091952.21:swaper

def dynaM_swaper(c):
    '''swap selected and copybuffer. a common task is to cut
    one word or sentance, paste in another place then repete
    with the other word or sentance back to the first position.
    you now can copy the one you want moved, select where you
    want to replace it. and hit swapper. you will have the other
    in the copy buffer and can now paste it over the first.
    
    much harder to describe than to do.
    '''
    newSel = dynaput(c, [])
    if not newSel: return
    newSel = str(newSel)

    sx = []

    repchar = g.app.gui.getTextFromClipboard()
    if repchar:
        g.app.gui.replaceClipboardWith(newSel) 
        sx.append(repchar)

    if sx:        
        dynaput(c, sx)
#@-node:ekr.20050328091952.21:swaper
#@+node:ekr.20050328091952.22:flipper

def dynaM_flipper(c):
    '''flip selected True to False, 1 to 0 or vice versa
    add your favorite flippable words to the dict below.
    '''
    newSel = dynaput(c, [])
    if not newSel: return
    newSel = str(newSel)

    sx = []
    
    #only need one instance of each flip pair, updates w/reverse dict
    flip = {'true':'false',
            'True':'False', 
            # 1/'1' not the same hash, but maybe interchangeable?
             '1':'0',
              1:0,   
             'YES':'NO',
             'yes':'no',
             'right':'left',
             'top':'bottom',
             'up':'dn',
             'n':'f',
             'after':'before',
             'or':'and',
              }
    #print flip

    flip.update(dict([[v, k] for k, v in flip.items()]) )

    #print flip

    if newSel in flip.keys():
        sx.append(flip[newSel])

    if sx:        
        dynaput(c, sx)
#@nonl
#@-node:ekr.20050328091952.22:flipper
#@+node:ekr.20050328091952.23:dupe

def dynaM_dupe(c):
    '''very often I want to copy a line or 2, but I only realize
    after I already have something in the buffer to paste over.
    this will duplicate the selected lines after the selected lines
    takeing advantage of the insert point selected being before of after
    pot luck asto which it will be before or after.
    have to unselect first, also makes dependant on the body
    was hopeing to keep those depandancys in dynaput
    incase I allow changes to other widgets or the log
    or even virtual bodys.
    if unselect, or virtual event return to end select kluge
    then dynaput complains nothing selected!
    try just doubling the selected text
    works for single line select anyway. 90% use case
    maybe if nothing selected, copy & paste the node?
    you may need to swith node then back after undo a duped line
    redraw isnt perfect
    '''
    newSel = dynaput(c, [])
    if not newSel: return

    sx = newSel.splitlines(True)
    sx += newSel.splitlines(True)

    dynaput(c, sx)
#@nonl
#@-node:ekr.20050328091952.23:dupe
#@+node:ekr.20050328091952.24:clipappend

def dynaM_clipappend(c):
    '''append selected to Clipboard
    '''
    newSel = dynaput(c, [])
    if not newSel: return

    Clip = g.app.gui.getTextFromClipboard()
    Clip += newSel
    g.app.gui.replaceClipboardWith(Clip)
#@-node:ekr.20050328091952.24:clipappend
#@+node:ekr.20050328091952.25:everycase

def dynaM_everycase(c):
    '''take the word or sentance and output in every case
     you can then copy from the log pane which you want.
     this seems easier than trying to consequetively 
     flip through all th possibilities.
     rClick dev version rightclick context menu has this.
    '''
    newSel = dynaput(c, [])
    if not newSel: return
    s = str(newSel)

    sx = []

    for x in [
        s.upper(), '  ',
        s.lower(), '  ',
        s.capitalize(), EOLN,
        
        s.swapcase(), '  ',
        s.title(), '  ',
        s.title().swapcase(), EOLN,

        "'%s'"%s, '  ',
        "(%s)"%s, '  ',
        "('%s')"%s.lower(), EOLN,
         ]:
        sx.append(x)

    #here wordwrap or otherwise format and relist it.
    
    if sx:        
        dynaput(c, sx)
#@-node:ekr.20050328091952.25:everycase
#@+node:ekr.20050328091952.26:dyna_regexTk

def dynaM_regexTk(c):
    '''changing Tk pack options to dict's
    match alphanumeric on either side of =: or space or coma delimited
    build a dict or list from it. properly quote and verify numbers.
    its only been 3 minutes and I have better results 
    than in plex or pyparsing in more time than I care to admit.
    maybe need re, space double in space delimited means cant ignore
    avoided re for now. probably woulve been easiest

    cuts after the decimal on floats. might want = as an option too

reWhitespace = re.compile( r'[,\s\n]+', re.MULTILINE )
fields = reWhitespace.split( line )

partially convert to EOLN, need to setup more tests first
    
    '''
    newSel = dynaput(c, [])
    if not newSel: return
    newSel = str(newSel)

    g.es('text is', newSel)

    sx = []

    #premassage the data
    newSel = newSel.replace(' ', ',').replace(',,', ',').replace(',,', ',')
    #print 'newSel is %r'%(newSel,)

    for x in newSel: 

        if x in '\'"':
            continue

        if x in [' ', ',', EOLN]: #may fail in py2.2 w/\r\n
            sx.append(EOLN)
            continue

        if x in '=:':
            sx.append(':')
            continue
        
        sx.append(x)


    data = ''.join(sx)
    data = data.replace('\n\n', '\n').replace('\n\n', '\n')
    data = data.replace('\n,\n', ',').replace('\n:\n', ':').replace(',', '\n')
    data = data.replace('\n:', ':').replace(':\n', ':').replace('::', ':')
    #print 'data is %r'%(data,)

    sx = []
    sx.append('{')
    for x in data.splitlines():
        #print 'for x', x

        if not x: 
            continue

        if x in [' ', ',', EOLN]: 
            sx.append(", ")
            continue

        if x.find(':') != -1: 
            x1 = x.split(':') 
            for i, y in enumerate(x1):
                #print 'for y', y

                if i == 1: 
                    sx.append(":")

                try:
                    #sx.append("%d"%int(y) )
                    sx.append("%d"%float(y) )
        
                #maybe float and int will have different errors
                #maybe if int it isnt coerced to float? works for me.
                except Exception, e:
                    #print 'exception', e.args
        
                    s = y.replace('Tk.', "").replace('Tkinter.', "")
                    sx.append("'%s'"%(s.lower(),) )
                #else: sx.append(":") else is only if except tripped

        else: #no : seperator assume is a plain delimited list
                sx.append("'%s':1"%(x,)) 
        sx.append(", ")


    sx.append("}")
    dynaput(c, sx)


#
#by pass while in plugin,
# for testing while included in dynatester node
#
if __name__ != 'dyna_menu':
    try:
        __version__
    except NameError:  
    
        #test passing quoted strings, space before and after, 
        #either numeric and real is getting parsed as 2
        #and isnt continuing to the next pair. stops at the first one
        #whatever "side"=1,  (whatever side) 
        def testbs():
            lst = """"\
            one two three
            side= Tk.LEFT , expand =1, 'fill'=Tk.BOTH,
            side"=1, expand = 1 , fi_ll=Tk.BOTH
            (=), [=], whatever 
                    """.splitlines(True)
            #print 'lst =', lst
            return lst

        genteststr.tstlst = testbs()
        testmacro = 'dynaM_regexTk'
#@-node:ekr.20050328091952.26:dyna_regexTk
#@+node:ekr.20050328091952.27:wraper

def dynaM_wraper(c):
    '''wrap selected to the len of the first line
    requires the py2.3 textwrap
    some code duplication in dynadoc for now
    http://cvs.sourceforge.net/viewcvs.py/python/
    '''
    try:
        import textwrap as tw
    except ImportError:
        tw = None
        g.es('please get textwrap from python cvs or py2.3')
        return

    newSel = dynaput(c, [])
    if not newSel: return

    data = str(newSel)

    sx = []
    
    datalines = data.splitlines(True)
    if datalines: width = len(datalines[0])

    width = width or 40
    #get starting indent from first line too
    
    t = tw.TextWrapper(
             width= width,
            initial_indent=' ',
           subsequent_indent= ' ',
           expand_tabs= True,
          replace_whitespace= True,
         fix_sentence_endings= False,
        break_long_words= True )

    st = t.fill(data)
    sx.append(st)  #[x for x in st]

    if st:        
        dynaput(c, sx)
    g.es( "len= %d lines= %d len firstline= %d words= %d"%(
        len(data), len(datalines), width, len(data.split())) )
#@nonl
#@-node:ekr.20050328091952.27:wraper
#@+node:ekr.20050328091952.28:+rsortnumb

def dynaM_rsortnumb(c):
    """caller to dyna_sortnumb(c, d= 1 )
    the reverse list will be called before output there
    """
    dynaM_sortnumb.direction = 1
    dynaM_sortnumb(c)

#@-node:ekr.20050328091952.28:+rsortnumb
#@+node:ekr.20050328091952.29:+sortnumb

def dynaM_sortnumb(c):
    """do a numeric aware sort, add field selection later
    maybe even a regex selection or other field specifyer
    can sort a list by copying the seperator then selecting some words
    default seperator is space, \n for multilines
    I realize other options might sometimes be required
    for those times, copy DQ3 and make something specilized.
    checking for multiple lines could be less redundant, ok for now.
    now how do I do a reverse sort?
    have a little helper function to call this with d=1
    need to preserve lineending if selected multiline,
     splitlines(True) ok if body
     how. each choice gets me deeper into trying to guess everything

     keeping indented lines together would allow sorting headlines
     and possibly functions. using a script in the copy buffer?

    """    
    nothingselected = False
    data = dynaput(c, [])
    g.es("selected ")
    if not data:
        nothingselected = True
        g.es("...skip, dump the body")
        v = c.currentVnode() # may chg in 4.2
        data = v.bodyString()

    #maybe use DQ3 thing of the copybuffer to select the splitchar
    splitchar = g.app.gui.getTextFromClipboard()

    multiline = ''
    if not splitchar:
        splitchar = ' '

    
    if 1 == len(data.splitlines(True)):
        sx = [x + splitchar for x in data.split(splitchar)]
    else: 
        multiline = EOLN
        sx = data.splitlines() #True
        
        
    sx.sort(compnum)

    try:
        if dynaM_sortnumb.direction == 1:
            sx.reverse()
            dynaM_sortnumb.direction = 0

    except AttributeError:
        pass

    #deal with nothing selected, must be sort of whole body as lines
    if nothingselected:
        #nothing selected so cant be paste over
        for x in sx:
            print x #might this double line?
    else:
        if multiline:
            sx = [x + multiline for x in sx]
        dynaput(c, sx)

def compnum(x, y ):
    """214202 Pretty_sorting_.htm
    Submitter: Su'\xe9'bastien Keim
    Last Updated: 2003/08/05 
    Sorting strings whith embeded numbers.
    #  sample
    >>> L1 = ["file~%d.txt"%i for i in range(1,5)]
    >>> L2 = L1[:]

    >>> L1.sort()
    >>> L2.sort(compnum)
    
    >>> for i,j in zip(L1, L2):
    ... print "%15s %15s" % (i,j)
     file~1.txt      file~1.txt  not the exact result
     file~2.txt      file~7.txt
     file~3.txt      file~3.txt
     file~4.txt      file~6.txt
     file~5.txt      file~5.txt
    """
    import re
    DIGITS = re.compile(r'[0-9]+')

    nx = ny = 0
    while True:
        a = DIGITS.search(x, nx )
        b = DIGITS.search(y, ny )
        if None in (a, b ):
            return cmp(x[nx:], y[ny:])
        r = (cmp(x[nx:a.start()], y[ny:b.start()])or
            cmp(int(x[a.start():a.end()]), int(y[b.start():b.end()])))
        if r:
            return r
        nx, ny = a.end(), b.end()

#
#@nonl
#@-node:ekr.20050328091952.29:+sortnumb
#@+node:ekr.20050328091952.30:del_last_char

def dynaM_del_last_char(c):
    """like del first char in the line except
    delete the last char in all the selected lines

    """
    newSel = dynaput(c, [])
    if not newSel: return
    
    try:
        newSel = str(newSel)
    except (UnicodeEncodeError, Exception):
        g.es_exception(full= False)


    sx = []
    for x in newSel.splitlines():
        sx.append(x[:-1] + EOLN )

    dynaput(c, sx)
#@-node:ekr.20050328091952.30:del_last_char
#@+node:ekr.20050328091952.31:call_dynaplay

def dynaM_dynaplay(c):
    """first cut attempt to get playback of commands into buffer
    currently whatever is in the copy buffer or '#'
    also unless set to paste it won't look like its working
    might change when leo has python instead of Tk indexes
    """    
    #dynaplay(c, ['#', '%%C,[home]', '%%C,[down]', '%%C,[repeat]' )
    #dynaplay(c, ['#', '%%C,[home]', '%%C,[down]4', '%%C,[repeat]3'] )

    #could get the Leo single char comment from whichever @language
    stext = g.app.gui.getTextFromClipboard()
    if not stext: stext = '#'
    dynaplayer(c, [stext, '%%C,[home]', '%%C,[down]',] )  #works
    
    #here it gets tricky changing print x, y, z or print x + y #
    #in find/change it would also be difficult
    #this one needs work, end not implimented
    #also not tested with single line selection
    #would need to go outside the selection to do this
    #dynaplay(c, ['g.es(', '%%C,[end]', ' )', '%%C,[home]', '%%C,[down]',] )
#@-node:ekr.20050328091952.31:call_dynaplay
#@-node:ekr.20050328091952.18:text macros
#@+node:ekr.20050328091952.32:codeing macros
#@+node:ekr.20050328091952.33:pydent

#@<< checkFileSyntax >>
#@+node:ekr.20050328091952.34:<< checkFileSyntax >>
#from leoTest params opposit from there
def checkFileSyntax(s, fileName= 'Script'):
    """too hard to get the traceback exact in full= False
    >>> checkFileSyntax(''' eros''') 
    '  File "<string>", line 1'
    ''
    '    eros'
    ''
    '    ^'
    ''
    'SyntaxError: invalid syntax'
    ''
    True
    >>> checkFileSyntax('''\\n#ok''')
    False
    """
    import leoGlobals as g
    import compiler
    try:
        compiler.parse(s.replace('\r\n', '\n') + '\n')  
        #,"<string>" parse(buf, mode='exec')
        #compile( string, filename, kind[, flags[, dont_inherit]]) 

    except SyntaxError:
        g.es("Syntax error in: %s" % fileName, color= "blue")
        g.es_exception(full= False, color= "orangered")
        return True  #raise

    return False
#@nonl
#@-node:ekr.20050328091952.34:<< checkFileSyntax >>
#@nl

#us pydent descriptive? more like pyimportwithindent
def dynaS_pydent(c, dopt={}): #should I pass the opts?
    """script to combine sfdots, reindent and import to @file
    make a scriptButton of this script. needs dyna_menu. 
    assumes the code is all in one node. will undo properly,
    but modifys the current node and will write to a temp file,
    then create a subnode from that file.
should be free of syntax error, obviously.
start off with docstring for any date or comments.
when done, move left, delete the temp node,
set @path or whatever and fix the headline.

overwrite False, no sfdots or evaluator
do I need a pause or update between the selectall and an action?
    """
    import dyna_menu as dy
    select = g.app.gui.setTextSelection
    overwrite = True
    
    
    start = dy.dynaB_Clip_dtef(None, ret='rp')

    if not c: c = g.top()
    p = c.currentPosition()

    if overwrite: 
        #enable to overwrite else will print to log
        dy.dynaMvar.dynapasteFlag.set('paste')
        select(p.c.frame.bodyCtrl, '0.0', 'end')
        dy.dynaS_sfdots(p.c, nodotreturn= True)


    #getsctipy now and check syntax... before/after evaluator
    #what about the undo? can I roll that back too?
    s = g.getScript(c, p)
    if checkFileSyntax(s): g.es(s, 'do undo twice'); return

    #now reindent isnt overwrite and want to run evaluator first
    #but I guess after is ok too.
    #tim1 leaves reindented code in the tmp.py

    if overwrite: 
        select(p.c.frame.bodyCtrl, '0.0', 'end')
        dy.dynaS_evaluator(p.c)


    s = g.getScript(c, p)
    if checkFileSyntax(s): g.es(s, 'do undo thrice'); return


    select(p.c.frame.bodyCtrl, '0.0', 'end')
    dy.dynaS_tim_one_crunch(p.c)

    c.beginUpdate()
    #might still have to remove a few sentinal lines start & end
    #can this return a sucess or fail? and the maybe the node pointer

    try:
        c.importCommands.importFilesCommand([dy.tmpfile], '@file')
    except Exception:
        g.es_exception()

    #else: is this if the exception? I can never remember
    #p.selectVnode('after') or something...
    #if headline == ('@file ' + dy.tmpfile):
    #    p.setHeadline('@file some.py')
    #   move before, then select node after, selectall & delete
    c.endUpdate()
    c.redraw()  #update no, redraw seems to work

    dy.dynaMvar.dynapasteFlag.set('print')
    g.es('st:%s\n sp:%s\n may have to wait \nand click to see the new node'%(
        start, dy.dynaB_Clip_dtef(None, ret='r')) )

    #should select child and move left. what if it failed?

#need an if exS because this gets run from doctest
#dynaS_pydent(None)

#@-node:ekr.20050328091952.33:pydent
#@+node:ekr.20050328091952.35:disa

def dynaS_pydisa(c= None, dopt={}):
    """produce a dissasembly into python bytecodes
    of selected text lines of code or the full script
    sentinals are striped to avoid confusing the output
    but of course in execute script they are there
    as should be noted in any timeit type usage
    """
    import leoGlobals as g
    import dis, sys

    import dyna_menu as dy

    if not c: c = g.top()
    p = c.currentPosition()

    #get selected text if any or the whole script
    newSel = dy.dynaput(c, []) 
    if not newSel: 
        #newSel = dy.fixbody(newSel, c)
        newSel = g.getScript(c, p)

    if not newSel or len(newSel) == 0:
        return

    newSel = stripSentinels(newSel)

    g.es('dissasembly of: '+ p.headString()[:50])
    g.es(newSel, color= 'MediumOrchid4')
    nc = compile(newSel, '<string>', 'exec')

    #have to find a way to encapsulate this better
    o = g.fileLikeObject()
    sys.stdout = o

    dis.dis(nc)

    s = o.get()
    sys.stdout = sys.__stdout__

    g.es(s.replace('   ', ' '), color= 'sienna3')
#@-node:ekr.20050328091952.35:disa
#@+node:ekr.20050328091952.36:changeleoGlobal

def dynaS_changeleoGlobal(c):
    '''converted to dyna to work on the current node
    of course including every macro in the plugin can get to be annoying. 
    have to dev a module to load on demand sub functions like this
  found an older script, updateing it not to hardwire whats in globals
  unfortunatly its using positions?

   script from,  Edward K. Ream - edream
 RE: A script to change leoGlobal functions
2004-05-31 09:12 from the tips&tricks forum
 > how would I specify the file, or subtree containing the lines that generate the file as an argument to the script?
First, the script must be copied to the .leo file that is to be changed. The present code for the script on cvs is:
 <note, it wasnt even a complete script!
 was missing key functions
 and I didnt see anything in latest cvs but didnt look too hard
 parts of it look like code to change not yet running Leo
 recomended rather than the static list tof functions. yikes
 we dont have that problem>
    
  here the dyna idea is you bring the script to the node
  select the node, then fire the macro and stand back
  think it might be proper to warn here also
  I usually never have more than a dozzen to change, easily by hand.
AttributeError: vnode instance has no attribute 'self_and_subtree_iter'
p.movetonext? need more than childnode here
startting to get iffy
implimented one of the new 4.2 iters dumbed down and a moveto
it went thru the whole outline, lucky didnt doit here...
looks like it was ment to scan from here to end of outline
didnt chg app or the import * line
    #g.top()
    p.bodyString()
have to chg all true/false to True/False
doesnt get g.app for some reason
maybe is sometimes app()
simplifyed getnames if not __versions__ fails as standalone
should skip directive lines incase is a path same as word in globals

    '''
    import leoGlobals as g
    import string

    #@    @+others
    #@+node:ekr.20050328091952.37:getgnames
    
    
    import leoGlobals as g
    def getgnames():
        import sys
    
        d = g.__dict__
        #should be just plain adding subbing from a dict
        
        names = [x for x in d.keys() if not x.startswith('__')]
        names.sort()
        
        exclud = ['time ', 'sys', 'os', 'cgitb', 'locale', 'difflib',
                 'string', 'gc', 'types', 'traceback', 'operator'
                 'unittest', 'doctest', 'imp', 'pprint', ] #stat?
        exclud += ['False', 'True',]
        
        names = [x for x in names 
                    if not hasattr(sys.modules, x)
                    if x not in exclud]
    
        return names
    
    if 0: #or not __version__:
        g.es("\nNames defined in leoGlobals")
        for name in getgnames():
                g.es(name)
    #@nonl
    #@-node:ekr.20050328091952.37:getgnames
    #@+node:ekr.20050328091952.38:subtree_iter
    
    #@verbatim
    #@+node:EKR.20040528151551.2:self_subtree_iter`from 4.2 branch
    def dynasubtree_iter(v):
        """Return all nodes of self's tree in outline order."""
        if v:
            yield v
            child = v.firstChild()  #t._firstChild
            while child:
                for v1 in dynasubtree_iter(child):  #.
                    yield v1
                child = child.next()
                
    dynaself_and_subtree_iter = dynasubtree_iter
    #@-node:ekr.20050328091952.38:subtree_iter
    #@+node:ekr.20050328091952.39:moveToNext
    
    def dynamoveToNext(p):
        
        """Move a position to its next sibling."""
        
        #p.v = p.v and p.v._next
        p = p and p.next()
        
        return p
    #@-node:ekr.20050328091952.39:moveToNext
    #@+node:ekr.20050328091952.40:prependNamesInTree
    
    def prependNamesInTree(p, nameList, prefix, replace= False):
        
        c = p.c
        
        assert(len(prefix) > 0)
        ch1 = string.letters + '_'
        ch2 = string.letters + string.digits + '_'
        def_s = "def " ; def_n = len(def_s)
        prefix_n = len(prefix)
        total = 0
        c.beginUpdate()
        for p in dynaself_and_subtree_iter(p):  #p.self_and_subtree_iter()
            count = 0 ; s = p.bodyString()
            printFlag = True
            if s:
                for name in nameList:
                    i = 0 ; n = len(name)
                    while 1:
                        #@                    << look for name followed by '(' >>
                        #@+node:ekr.20050328091952.41:<< look for name followed by '(' >>
                        i = s.find(name, i)
                        if i == -1:
                            break
                        elif g.match(s,i-1,'.'):
                            i += n # Already an attribute.
                        elif g.match(s,i-prefix_n,prefix):
                            i += n # Already preceded by the prefix.
                        elif g.match(s,i-def_n,def_s):
                            i += n # preceded by "def"
                        elif i > 0 and s[i-1] in ch1:
                            i += n # Not a word match.
                        elif i+n < len(s) and s[i+n] in ch2:
                            i += n # Not a word match.
                        else:
                            j = i + n
                            j = g.skip_ws(s,j)
                            if j >= len(s) or s[j] != '(':
                                i += n
                            else: # Replace name by prefix+name
                                s = s[:i] + prefix + name + s[i+n:]
                                i += n ; count += 1
                                # g.es('.',newline=False)
                                if 1:
                                    if not printFlag:
                                        printFlag = True
                                        # print p.headString()
                                    g.es(g.get_line(s,i-n))
                        #@-node:ekr.20050328091952.41:<< look for name followed by '(' >>
                        #@nl
    
                #assume s is the word, wont catch app() anymore?
                if s in chgdict:
                    s = chgdct[s]  #True for true etc
                    count += 1    #why thi is +=
                if count and replace:
                    if 1:
                        #@                    << print before and after >>
                        #@+node:ekr.20050328091952.42:<< print before and after >>
                        g.es("-"*10,count, p.headString())
                        g.es("before...")
                        g.es(p.bodyString())
                        #g.es("-"*10, "after...")
                        #g.es(s)
                        #@nonl
                        #@-node:ekr.20050328091952.42:<< print before and after >>
                        #@nl
                    p.setBodyStringOrPane(s)
                    p.setDirty()
            g.es("%3d %s"%(count, p.headString()))
            total += count
        c.endUpdate()
        return total
    #@nonl
    #@-node:ekr.20050328091952.40:prependNamesInTree
    #@-others

    c = g.top()
    
    mess = """\
    the current node & subnodes will be changed
    any in leoGlobals to g.whatever
     and there is no undo
     you might want to copy the node or backup the leo
     we'll wait...
     BTW, be afraid, be very afraid.
     """
    nameList = getgnames()
    #isnt getting app() either way well, app() becomes g.app()
    #app stays app, doesnt get true or false either
    chgdict = {'false':'False', 'true':'True', 'Tkinter':'Tk', 
             'app()':'g.app', 'app':'g.app', }


    #g.alert(mess)  #g.app.gui
    ans = runAskYesNoCancelDialog(c,"changeleoGlobal", 
            message= mess, yesMessage= 'ok')

    if 'ok' != ans: g.es('changeleoGlobal cancled'); return

    p = c.currentVnode() ; count = 0
    vafter = p.nodeAfterTree()

    while p and p != vafter:
        # Just prints if replace == false.
        count += prependNamesInTree(p, nameList, "g.", replace= True) 
        #p.moveToNext()
        p = dynamoveToNext(p)
    s = "%d --- done --- " % count
    #if count: 
    #c.frame.body.onBodyWillChange(p, "Typing") 
    #does update, not sure this will do anything if subnodes changes
    #nothing in undo, you have to click ouside the target node.
    #this has changed since 4.1 and will probably get fixed.

    #if you want to see the nameslist exS on the getnames node
    s = "concidered %d leoGlobals" % len(nameList)
    s += "\nyou have to add\nimport leoGlobals as g"
    s += "\ntry:\n    import Tkinter as Tk\nexcept ImportError: Tk = None"
    g.es(s)
    s = "change app(). or app. to g.app.\ntrue/false to True/False"
    g.es(s)
    #g.es('click outside node to see changes') #fixed in v4.2b3
    c.redraw()

#@-node:ekr.20050328091952.36:changeleoGlobal
#@+node:ekr.20050328091952.43:c2py

def dynaS_c2py(c):
    """call the fantastic first cut c2py script
    you still have to make it more pythonic but it does quite alot.
    c2py doesnt generate an undo event so there is no turning back.    
    @language c

    still some things to work out. if the c file is in one node
    it might be better to import it first as c, then let c2py convert it
    using convertCurrentTree it converts in place.
     that might be dangerous if it
    fails or if you need to refer to it later
    OTOH, from a tempfile you wouldent be able to import
    as there may be logic problems left over from the conversion.

    c2py being a direct translation of c would
    often serve to rethink some of the program flow
    ranther than depend ona line by line translation.
    droping just the relevant algorythm translated in to python
    into a more generic pythonic wrapper can save alot of time.

    on selected text or body written to tempfile.
    previously foundit easier to call c2py with a filename
    then import the modifyed file. which did work well.
    usually stick with what works. glad I didnt this time.
    having dyna provide the currentvnode was the missing piece
    and should allow the import as well without a filewrite.
    
    might still make  a backup to another node or to a derived file.
    it also might make sense to run the c thru indent first
    you definatly want the origional to refer to.
    need to run thru reindent or remove tabs maybe too before usage.
    there are clues to give c2py which might help with some specific
    conversions which I havent examined.
    in the case of declarations I wouldve left comments on the type
    int x, becomes just x. might have been char or double who knows.
# 
# c2py removes all type definitions correctly; it converts
# 	new aType(...)
# to
# 	aType(...)


classList = [
    "vnode", "tnode", "Commands",
    "wxString", "wxTreeCtrl", "wxTextCtrl", "wxSplitterWindow" ]
    
typeList = ["char", "void", "short", "long", "int", "double", "float"]

 Please change ivarsDict so it represents the instance variables (ivars) used  by your program's classes.
ivarsDict is a dictionary used to translate ivar i of class c to self.i.  
It  also translates this->i to self.i.

    
ivarsDict = {
    "atFile": [ "mCommands", "mErrors", "mStructureErrors",
        "mTargetFileName", "mOutputFileName", "mOutputStream",
        "mStartSentinelComment", "mEndSentinelComment", "mRoot"],

    "vnode": ["mCommands", "mJoinList", "mIconVal", "mTreeID", "mT", "mStatusBits"],

    "tnode": ["mBodyString", "mBodyRTF", "mJoinHead", "mStatusBits", "mFileIndex",
        "mSelectionStart", "mSelectionLength", "mCloneIndex"],
        
    "LeoFrame": ["mNextFrame", "mPrevFrame", "mCommands"],

    "Commands": [
        # public
        "mCurrentVnode", "mLeoFrame", "mInhibitOnTreeChanged", "mMaxTnodeIndex",
        "mTreeCtrl", "mBodyCtrl", "mFirstWindowAndNeverSaved",
        #private
        "mTabWidth", "mChanged", "mOutlineExpansionLevel", "mUsingClipboard",
        "mFileName", "mMemoryInputStream", "mMemoryOutputStream", "mFileInputStream",
        "mInputFile", "mFileOutputStream", "mFileSize", "mTopVnode", "mTagList",
        "mMaxVnodeTag",
        "mUndoType", "mUndoVnode", "mUndoParent", "mUndoBack", "mUndoN",
        "mUndoDVnodes", "mUndoLastChild", "mUndoablyDeletedVnode" ]}  

def convertCurrentTree():
    import c2py
    import leo
    import leoGlobals
    c=leoGlobals.top()
    v = c.currentVnode()
    c2py.convertLeoTree(v,c) 
    
    wouldent this obviate any changes to ivars or other code?
    might have to do the same setup w/o the fresh import
    and where to get th custom info from if using M_c2py from plugin?


    messages are going to console instead of log
    converting: NewHeadline
    end of c2py

   x = {}  will have the {} removed. not sure why...
   removeBlankLines never?
    run tabs to spaces    y/n
    """
    import sys
    
    s = g.os_path_join(str(g.app.loadDir), '../scripts')

    #sc2py = g.os_path_join(s, 'c2py.py')
    if not s in sys.path:
        sys.path.append(s)

    #__import__(../scripts/c2py.py )

    import c2py
    mess = """\
    the current node & subnodes will be changed
     and there is no undo
     """
    #g.alert(mess)  #g.app.gui
    ans = runAskYesNoCancelDialog(c, "c2py",
                 message= mess, yesMessage= 'ok')

    if 'ok' != ans: g.es('c2py cancled'); return

    #get selected or body... getbody language sensitive
    #write the temp

    #c2py.convertCurrentTree()  #reimports c2py but does work

    #this might fail, but want to try and set some things
    #if it reimports they might get lost...
    c2py.convertLeoTree(c.currentVnode(), c)
    
    #convertLeoTree just node walks, might pass from fixbody
    #then try and reimport to @file from that.
    
    #tmpfile should just be a basename you add extension to?
    #temp = tmpfile[:-3] + '.c'

    #c2py.convertCFileToPython(file) #another way to go

    #cmd = py + c2py + temp
    #out, err = runcmd(cmd)
    #g.es('click outside node to see changes') #fixed in v4.2b3
    c.redraw()  #update nor redraw seems to work
#@-node:ekr.20050328091952.43:c2py
#@+node:ekr.20050328091952.44:+dynaHexdump

def dynaS_dump_body(c, ret= 'p'):
    """yadayada call hexdump, on selected text or body
      if you need need an exact output, including any lineendings?
      Leo translates to unicode first so that might be relevant
      calls dynaHexdump(src, length=8)

UnicodeDecodeError: 'ascii' codec can't decode byte 0x9f in position 1: ordinal not in range(128)
since its not a char at a time, this is going to be hard to trap
maybe will have to filter first. 
need feedback from someone who cares about unicode.
    """

    data = dynaput(c, [])
    g.es("selected ")
    if not data:
        g.es("...skip, dump the body")
        v = c.currentVnode() # may chg in 4.2
        data = v.bodyString()

    if data and len(data) > 0:
        #newdata = re.sub("\n", "\r\n", data)
        newdata = dynaHexdump(data)
        if newdata != data:
            #v.setBodyStringOrPane(newdata)
            if 'p' in ret: g.es(newdata)
            if 'r' in ret: return newdata

#had to unicode the FILTER for Leo plugin use
FILTER= u''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])

def dynaHexdump(src, length=8):
    """
    m02A14p6:31 ASPN Python Cookbook
    Title: Hexdumper.py  Submitter: S?stien Keim  2002/08/05 Version no: 1.0
    Hexadecimal display of a byte stream
    later, output to logwindow of selected text add as a menu option
    maybe can make it read from a file and output as hex
    #r04408ap11:16 chg += to append & join,  not that its particularly slow
    >>> Hexdump('ASPN Python Cook')
    >>> #Hexdump('01')
    '0000   41 53 50 4E 20 50 79 74    ASPN Pyt\n0008   68 6F 6E 20 43 6F 6F 6B    hon Cook'
    """
    N = 0; result = []
    while src:
        s, src = src[:length], src[length:]
        hexa = ' '.join(["%02X"%ord(x) for x in s] )
        s = s.translate(FILTER)
        result.append("%04X   %-*s   %s  % 3dd" % (N, length * 3, hexa, s, N) )
        N += length
    return '\n'.join(result)
#@-node:ekr.20050328091952.44:+dynaHexdump
#@+node:ekr.20050328091952.45:_sfdots

def dynaS_sfdots(c, nodotreturn= False, stripsentinals= True):
    """w04310p3:22 process code from sourceforge forum
    which replaces . for leading indentation which sourceforge eats
    make the reverser too so posters can run their code thru first
    it would be nice if it could standardize to 4spaces per level
    maybe replacing and rerunning or something to catch max indentation
    run thru reindent and pychecker could be usefull
    the UPL adds only 3 dots when you have 4 spaces and nothing else
    that would probably be an error
    t04323a12:31 optomizing for python indentation, adding use,is at first line
    later make that selectable so can do anything, and or put thru reindent
    and allow add or eat first n chars for command to add to rClick
    using a section header to put the code into a subnode
    precedence of i+1 % n slightly different than c, use (i+1)%n
    messedup indentation this wont fix! shoulve saved a copy of the org...
    this version adds indentation numbers and fails if i>n as yet.
    \n was interpreted from the section literlly as a newline in the output...
    need a slick way to check or switch triple Sq/Dq
    its not transforming 2space into 4spacem it eats \t also
    maybe would be better to change dots to tabs then '\t\tfoo'.expandtabs(2)
    sf eats long lines & spaces ? in view source too. 
    the wiki eats angle brackets and moost html and if you click edit it retranslates 
    f04514a11:22:06 convert to dyna, some sillyness to handle inconsistant dots
    if starts with dots, convert to space DNL
    if all spaces or tabs then is UPL convert to dots
    should check the users tab setting, might want one dot to equal one tab
    other times 4 dots= one tab. you edit in what you want I guess.
    you can run it thru reindent after tim1crunch, copy over then c2py
    which defaults to using tabs. which I will change if I find out how.
    I guess c2py doesnt fail if it finds only python, it tabs it up.
    most of the time that should get standrd indenting no matter what.
   
  I think it still screws up \n literal in strings. not tested w/tabs or unicode
  also will hit a limit on indentation if greater than typical for sf post
  can look weird if printed to log w/non proportional font
  
This means that the code would refer to Tk.widget instead of Tkinter.widget.  Also, please avoid the use of the completely useless Tk constants such as Tk.RIGHT, Tk.TOP.  Use "right" or "top" instead.  
havent done any replace on the incomming or outgoing data.
chg to fixbody except not sure paste makes sence if it isnt in one node  
might send a download automatically thru reindent then evaluator

allowing conversion of full body, if you try and paste over it will
not follow nodes but probably just overwrite the selected node.

add select leading char ini option 
allow from/to of intrepreter >>> ... for doctest prep
 """
    newSel = dynaput(c, [])
    g.es("selected ")
    if not newSel:
        g.es("...skip, dump the body")
        #v = c.currentVnode() # may chg in 4.2
        #data = v.bodyString()
    data = fixbody(newSel, c)  #bad idea fixbody rearange order of c

    if not data or len(data) == 0: return
    import re
    respc = re.compile(r'^[\s.]*$')

    isdots = [x[:1] for x in data.splitlines() if x.startswith('.')]
    #print 'isdotslist', isdots
    isdots = len(isdots) > 0

    if nodotreturn and not isdots: return

    #py <2.3 YOYO isdots == True , works w/o 
    direction=['UPL', 'DNL',][isdots]  

    #doesnt python have a simpler way to swap varbs? 
    #is this clearer to read though. a='.';b=' '; if UPL: a,b=b,a; 
    #could you have '....' be the eat char in a perfect world?
    
    if direction == 'UPL':
        eatchar=' '
        repchar='.'
    else:
        eatchar='.'
        repchar=' '
    
    if stripsentinals:
        data = stripSentinels(data, stripnodesents=0 )

    #4,3
    lines = ('4,4\n' + str(data.expandtabs(4))).splitlines(True)
    
    #fixes dopy dots, starting off with 3 then continuing with 2
    
    
    n, nm = lines[0].split(',')
    n = int(n) or 4  #what one dot equals
    nm = int(nm) or 3

    #print 'len & direction', len(data), len(lines), direction,
    #print n, nm 

    def chkout(t):
        if respc.findall(t): #cut lines on ., ,\t,\f,\n
            t = '\n'
        return t

    sx = []
    for lt in lines[1:]:
        i = 0
        ix = 0
        for o in lt:
            if o == eatchar: 
                i += 1
                continue
            break
        #print i,
        if i > 0 and len(lt) > 0:
            #this should handle 2 4 or 3 on the first then 2 dots,
            #it will get confused if starts and continues with 3
            if nm == 4: ix = i
            elif i==3 or i == 2: ix = n
            elif i==5 or i == 4: ix = n*2
            elif i==7 or i == 6: ix = n*3
            elif i==9 or i == 8: ix = n*4
            elif i==11 or i == 10: ix = n*5
            elif i==13 or i == 12: ix = n*6
            elif i==15 or i == 14: ix = n*7
            elif i==17 or i == 16: ix = n*8
            else: g.es('**bad ix',i)
            #print (repchar*(ix))+lt[i:]
            sx.append(chkout((repchar*(ix))+lt[i:]) )
            continue
        elif i > 0:
            g.es('')
            continue
        
        #print lt
        sx.append(chkout(lt))

    #print sx
    #reindent or evaluator would help too. before the dots obiously
    dynaput(c, sx)    
    
#@-node:ekr.20050328091952.45:_sfdots
#@+node:ekr.20050328091952.46:+call_evaluator

def dynaS_evaluator(c):
    """calc_util.py and its unit tests and rClickclass 
    ******* not available yet *********
   from http://rclick.netfirms.com/rCpython.htm

    parsing python programs perfectly presumes perfect programming.
    its so close, I use it all the time to verify code.
    but I know its limitations and I cant realease it yet,


   does good job of reindenting, but still can make mistakes indenting after dedent or comment or before an indent
   compare to origional code carefully!
   
    forgot to tell evaluator to skip to @c if it finds @ alone
    output to log doesnt colorize so isnt immediatly obvious
    the html mode should be reparsed to change to es color output
    need to add an eval mode so can get expression outpt as well
    have to trap stdout so can use to paste if thats selected
    capture seems to be working now from plugin or button
    fixbody takes care of commenting out @directives now.

    if nothing selected, it seems to have nothing?
    weird, its now going to the console again from the button
    and from plugin nothing if nothing selected.
    this is easily the 3rd time it was then wasnt working.
    all the calls are same as pychecker2, it sometimes prints the data
    inside the if. something is erroring and getting masked.
    
    """
    try:
        import calc_util ;#reload(calc_util) #if working on calc_util
    except ImportError:
        #can I use Leo prettyprinter instead?
        g.es('you have to get the evaluator first')
        return

    newSel = dynaput(c, [])
    data = fixbody(newSel, c)
    #print repr(data)


    if data and len(data) > 0:

        #ta = g.stdOutIsRedirected()
        #g.restoreStdout()
            

        #print repr(data)

        o = captureStd()
        o.captureStdout()

        try:
            #this has print on line by line as parsed
            newdata = calc_util.file_test(data, q= 1,
                 doEval= 0, formater= 'py2py',  #py2py raw html
                    onlyPrintFails= 0, printAny= 0 )

        except Exception, err:
            dynaerrout(err,'evaluator ')

        output = o.releaseStdout()
        #if ta:
        #    g.redirectStdout()
            

        dynaput(c, output.splitlines(True))

    #elif len(data) < 80: maybe check for newlines better?
    #    eror, result, ppir = calc_util.evalcall(data)

#
#@nonl
#@-node:ekr.20050328091952.46:+call_evaluator
#@+node:ekr.20050328091952.47:makatemp

def dynaS_makatemp(c):
    '''create a file and lightly test it.
     default to a tmp filename
     if copy buffer has a valid path like name, use that
     take the selected text or body (eventually @other & section ref too)

     write out the file and run it thru reindent then pychecker
     or maybe what is wanted is to take from the copy buffer
     makeatemp and run it thru pychecker then create a subnode with it
     usecsae, posting from c.l.py or from other artical
     handling @directives, not @others nor section nodes yet.
     

  for some reason only the @ is getting thru from exS in dynatest
  the re isnt commenting them out either. I HATE re's
  doh, comedy of errors again. forgot the * after .
  was testing date instead of data, misnamed single use varb.
  generated new macro idea to scan for those mistakes.

  have to tell it to skip from @ to @c as well
  
  the name verifyer re isnt workring yet. not fully implimented
  
  
  external pychecker still has a problem resolveing from import leo*
  not sure how to resolve that. 
  maybe import pythecker.pychecker in the macro?
  wpp[s, this whole thing is breaking down. I forgot one other thing
  the import phase will cause the code to be run. this may or may not be a problem,
  adding a name == main if one doesnt exist might be better
  \nif __name__ == '__main__': pass
  which wont help unless all the indentation on executable lines are indented
  that is too much work I think.
  checking selected text or filenames of generated modules still usefull
  pylint still complaining it cant find the py in temp in sys modules
  may have to dig deeper into that as well
  adding tempdir where the file is doesnt seem to be enough for pylint

  tryed a bunch more things. pychecker works, nearly got pylint.
  pychecker still balks on leo* stuff 
  so checking plugins would have to add import pychecker; pychecker.pychecker()?
  
    have to abstract the get path thing out to return a tuple of 
    leo, python, scripts, site-packages
    so all macros can find and user only has to change one place
    

  using expandtabs(4)
  ***************
    warning, this makes asumptions about where python is, 
    what and where reindent and pychecker is
    at least you have to edit in your correct paths.
    I could guess more but still wouldent be totally sure.
    see the .rc file usefull for pychecker in leoPy.leo
    pylint the same thing.
    url's ...

    I have no idea if pychecker is safe to run on insecure code
    it will create a py and pyc or pyo and maybe a bak file in tmp
    hold me harmless or delete this now.
  ***************
  all paths below are woefully hardwired, you must edit them all.
  you may have to download pychecker and or pylint and install it too.
  
should   we insert # -*- coding: utf8 -*-
 at the top of the file? or cp1252 or mbswhatever if on windows
 should getscript have that option?
 and dyna does this in several places, need to cosolidate them into one place
    '''
    #1no print, reindent to create tmp then pychecker on that tmp
    justPyChecker = g.app.dynaMvar.justPyChecker


    newSel = dynaput(c, [])
    data = fixbody(newSel, c)

    if not data or len(data) == 0: 
        return

    tmpname = tmpfile #global or from copybuffer

    import re, os, sys
    import leoTkinterDialog as lTkD



    #you might not have to fix leo/src either
    #better to get basepath or something, look it up later
    #one run and its in sys.path, sys.path is global for all leo's?
    #another append will be twice in there
    #Leo prepends its src dir but pychecker isnt finding it.

    #this could be trouble on nix or mac. YOYO
    #might not even be necessary in the app, maybe some other
    if sys.platform[:3] == 'win':
        
        oldpPath = os.environ['PYTHONPATH']
        oldpSath = sys.path
        #these changes will be compounded at every run of the script

        if not leosrc in sys.path:
            sys.path.append(leosrc)

        if not g.os_path_split(tmpname)[0] in sys.path:
            sys.path.append(g.os_path_split(tmpname)[0] )
        
        #Leo may have already zero this out to just path of python.

        try:
            if not leosrc in os.environ['PYTHONPATH']:
                os.environ['PYTHONPATH'] = os.environ['PYTHONPATH'] + \
                    ';' + leosrc

        #[py2.2 :'in <string>' requires character as left operand
        except TypeError:
            pass

        #g.es(sys.path )
        #g.es(os.environ['PYTHONPATH'] )

    elif sys.platform[:5] == 'linux':
        pass
    
    #print lTkD.tkinterAskYesNoCancel(tmpname)

    #pylint has to be able to import the file on sys.path?
    #pychecker seems to be able to import from the filename arg
    #pychecker can find it now and does report ok if no leo* stuff in there
    #it can import the leo* ok just not resolve from what I can tell.


    #pylint = r'\Tools\scripts\pylint.bat ' 
    #have to create a py the win version ships with a bat
    #was Run(sys.argv[1:])
    #Exception: Unable to find module for C:\WINDOWS\TEMP\tmptest in C:\c\leo, 
    #Leo doenst send the sys we are hacking on above to the exec?
    #think I realized this once before and didnt know how to solve it.
    #think pylint can only handle modules, so dup filenames will be  problem
    #if its expecting sys.arg maybe a list?
    #F:  0: Unable to load module tmptest (No module named tmptest)
    #temp is in sys.path so why it refuses to load I have no idea




    #valid name consists of many more chars on win and nix
    #I may never use this, but will continue testing
    re_testname = re.compile(
    r"""
\s*
([a-zA-Z0-9]*?)
(:?)
(/|\\\\*[a-z]*?[a-zA-Z0-9_\s]*?)  #this needs to repeat however many times
(\.*?)
([a-zA-Z0-9_\.\s]*?)
\s*
""", re.VERBOSE )  

    #g.es('data is %r'%(data,) )

    #raise SystemExit  maybe dangerous inside Leo tho was ok.
    #e32 = r34   #works as an error to stop execution too

    name = g.app.gui.getTextFromClipboard()
    #if name:
    #    print re_testname.search(name).groups()

    g.es('writeing tmpname', tmpname )
    fo = file(tmpname,'w')
    fo.writelines(data + "%s#e%s"%(EOLN, EOLN, ))
    fo.close()
    
    if doreindent:
        g.es('running reindent', py + reindent + tmpname )
        out, err = runcmd(py + reindent + tmpname)
        for x in (out + err).splitlines():
            g.es(x)
        
    g.es('running pychecker', py + pycheck + tmpname )
    out, err = runcmd(py + pycheck + tmpname)
    for x in (out + err).splitlines():
        g.es(x)

    if dopylint:
        pylname = g.os_path_split(tmpname)[1][:-3] #cut off .py
        g.es('pylint module', pylname )
        pylint = \
        " -c \"import sys; from logilab.pylint import lint;\
                   lint.Run([r\'%s\',])\" "%(pylname,)

        g.es('running pylint', py + pylint )
        out, err = runcmd( py + pylint)
        for x in (out + err).splitlines():
            g.es(x)
    
    if not justPyChecker:
        g.es('#source for ', tmpname, color='blue' ) 
        TextFile = file(tmpname)
        Text = TextFile.read()
        TextFile.close()
        g.es(Text)
    
    #should be restored even if error. oh well
    if sys.platform[:3] == 'win':
        
        os.environ['PYTHONPATH'] = oldpPath
        sys.path = oldpSath  #Leo discards this?

    g.es('done ', color='blue' ) 

#
#by pass while in plugin,
#this for testing while included in dynatester node
#
if __name__ != 'dyna_menu':
    try:
        __version__
    except NameError:  
    
        lst = """@language python

from leoGlobals import *
import string,Tkinter

Tk = Tkinter

#@verbatim
#@+others     C:/TEMP/leo/leo4CVS/plugins/mod_rclick.py
    L:\\c\\Python22\\Doc\\lib\\modindex.html
    L:\c\Python22\Doc\lib\modindex.html
    """  #.splitlines(True)
        #lst =  [x.lstrip() for x in lst]
        genteststr.tstlst = lst
        testmacro = 'dynaM_makatemp'
#@nonl
#@-node:ekr.20050328091952.47:makatemp
#@+node:ekr.20050328091952.48:pycheck2

def dynaS_pycheck2(c):
    '''this takes a long time 
    and leave a 2+meg file CACHE_FILE = '/temp/t'  in pychecker2/main.py
 have to modify the dump line chg 0 to -2, highest proto supported auto

    needs a progressbar, Leo will wait till its done, so will you.
    takes over 2 mins on pII300 on a simple Tk program of about 50k.
    pycheck2 doesnt import or compile the file first,
    so it is safer to use on untrusted code or code with sideeffects.
    it should also work regardless if the file is in sys.path .
    runs thru reindent first as a rough syntax error test.
    install pychecker from the source, move pychecker2 dir to site-packages
    and fix the path in common for pycheck2
    this is also self described IIR experimental so dont expect miricals
    it might even Traceback or crash. though it hasn't crashed for me, 
    has at least found unused vars. its no pychecker.
    not sure if it uses the same rc file as pychecker.
  seems not to be able to find leoglobals at all
  seems to check problems in modules not even related
  console, win32con pyreadline, ctypes. not sure whats going on there


ImportError: No module named IterableUserDict
 might have to get cvs version. first run a cpickle is left in /temp/t
 2nd run it will fail. didnt notice this before. could delete it
 could chg to text instead of binary which has failed for me before
 also could try pickle instead of cpickle

     checker = cPickle.load(open(CACHE_FILE, 'rb')) 
     chg dump protocall from 1 to 0 didnt help, douled size of file
import cPickler; print cPickle.__doc__
 have to modify the dump line chg 0 to -2, highest proto supported auto
 now cache file is only 50k 
 and doesnt error on 2nd run 
 and is quite a bit faster.
  but after a few runs it came back, going to have to del the t
    '''
    #1no print, reindent to create tmp then pychecker on that tmp
    justPyChecker = g.app.dynaMvar.justPyChecker
    CACHE_FILE = '/temp/t'  #defined in pychecker2.main

    newSel = dynaput(c, [])
    data = fixbody(newSel, c)

    if not data or len(data) == 0: 
        return

    tmpname = tmpfile #global or from copybuffer later

    import os
    try:
        os.remove(CACHE_FILE)
        pass
    except Exception:
        pass

    g.es('writeing tmpname', tmpname )
    fo = file(tmpname,'w')
    fo.writelines(data + "%s#e%s"%(EOLN, EOLN, ))
    fo.close()
    
    if not justPyChecker:
        g.es('running reindent', py + reindent + tmpname )
        out, err = runcmd(py + reindent + tmpname)
        for x in (out + err).splitlines():
            g.es(x)

    #see if this works, dyna_menu. didnt, maybe g.dyna_menu., lg.?
    #pristine enviorment?
    #g.dyna_menu.dynaM_Clip_dtef(c, ret= 'p')  #rough timestamp
    g.es(' be paitent,\n can take several minutes')
    g.es('running pychecker2', py + pycheck2 + tmpname )
    out, err = runcmd(py + pycheck2 + tmpname)
    for x in (out + err).splitlines():
        g.es(x.replace(tmpname, tmpname[-10:]))
    
    
    if not justPyChecker:
        g.es('#source for ', tmpname, color='blue' ) 
        TextFile = file(tmpname)
        Text = TextFile.read()
        TextFile.close()
        g.es(Text)
    

    g.es('done ', color='blue' ) 
#@nonl
#@-node:ekr.20050328091952.48:pycheck2
#@+node:ekr.20050328091952.49:tim_one_crunch

def dynaS_tim_one_crunch(c):
    '''
    #t04504p10:05:08 bit of old code from tim peters gooogle, 
    had to un-htmlify it, then uu.decode it. quite a PITA.

    riped code from makatemp to preprocess the selected text or body
    hardwire write a file then see how many single use varbs there are
    it generates alot of false positives
   try the bugfix, slightly more complicated in a later post
   double check the name polution, uses regex and string too
   woh, was not going to work or needs some updateing.
   use the old crunch for now. better than nothing when trouble starts.
    need to finish the code to use a filename instead of writeing a new temp
    that will be usefull for pychecker & pylint too.
    its alot faster than you would think too 
    parse & create a tmpfile, crunch parse it and display the results.
    on few page bodys, I can barely get off the button and its done.
    might run the makatmp first to create the file and just parse it with this
    rather than pulling in the reindent call. few more lines, what the hell
    reindent doesnt fix to standard indentation. why do I keep thinking it does?
    have to wait till the last few bugs worked out of evaluator.
    could use to test against known methods and modules in use by the code
    could reduce the false positives.
    if you make the same mistake twice, its no longer unique. is that caught?

    try compile as a way to verify code will import? is it safe?
    why doesnt it just pass the data directly to StringIO unless it is a filename?
    OTOH, reindent proves the thing has correct syntax so may as well keep it
  using the bugfix version now, patched in import keyword
   added dir(list,dict from the older version
   commented out __modules__ __builtins__ for now
   building a more complete keyword list is the holy grail
   of autocomplete and debuggers and code evaluators of all kinds.



    Tim Peters tim_one@msn.com    Thu, 27 Feb 97 09:00:30 UT 
 ----
    Attached is a Python program that reports identifiers used only once in a .py (text) file, except for keywords, builtins, and methods on dicts & lists (& the way to expand that set should be obvious). 
    This is much dumber than the other approaches on the table, but has the clear advantage that it's written <wink>, and catches things like "bound but never used" (including-- and this is a mixed blessing! --functions & classes defined but not referenced in their file). 
        '''
    #1no print, reindent to create tmp then checker on that tmp
    justPyChecker = g.app.dynaMvar.justPyChecker


    newSel = dynaput(c, [])
    data = fixbody(newSel, c)

    if not data or len(data) == 0: 
        #here check copybutffer for valid filename

        return

    tmpname = tmpfile #global or from copybuffer

    g.es('writeing tmpname', tmpname )
    fo = file(tmpname,'w')
    fo.writelines(data + "%s#e%s"%(EOLN, EOLN, ))
    fo.close()
    
    if not justPyChecker:
        g.es('running reindent', py + reindent + tmpname )
        out, err = runcmd(py + reindent + tmpname)
        for x in (out + err).splitlines():
            g.es(x)

    o = file(tmpname)
    so = StringIO.StringIO(o.read())
    o.close()

    #made a caller to hide some of the globals
    Bugfixcrunch(so.readline)
    
    if not justPyChecker:

        g.es('#source for ', tmpname, color='blue' ) 
        
        so.seek(0, 0)
        #.read() and .readlines() doubled up because of \n\r on win
        for x in so.getvalue().splitlines(True):
            g.es(x, newline= false)
    g.es('done ', color='blue' ) 


#
#@nonl
#@+node:ekr.20050328091952.50:Bugfixcrunch

def Bugfixcrunch(getline):
    """u04523p12:01:20  madifying use of globals with 
    calling functions bfcrunch embeded
    the origional crunch has alot of false positives
    
    >Bugfix (RE: Patch to Tim Peters python lint)</H1>
     <B>Tim Peters</B> <A HREF="mailto:tim_one@msn.com"
     TITLE="Bugfix (RE: Patch to Tim Peters python
     lint)">tim_one@msn.com</A><BR> <I>
     Wed, 5 Mar 97 05:14:38 UT
      I'll agree to fix errors in the hard-core parsing crap (&
     there are at least  </I><BR><P> <BR>><i> two more
     (small & unlikely) holes that I know of ...
     </I><BR><P> Ya, ya, ya.  One of them was this: <P>
     <BR>><i> [anonymous nagger <wink>] </I><BR>><i>
     </I><BR>><i> LABEL = "\ </I><BR>><i> </I><BR>><i>
     (that is, a quote followed by a backslash followed by
     a newline) </I><BR>><i> seems to cause an infinite
     loop... </I><BR><P> More, *any* unclosed uni-quoted
     string fell into that loop -- continued  uni-quoted
     strings are a feature of Python I never used, so was
     blind to the  possibility at first; then conveniently
     convinced myself nobody else used that  misfeature
     <wink> either so I could ignore it.  I lose! <P>
     Attached version fixes that by treating uni-quoted
     and triple-quoted strings  pretty much the same
     (although the former have more-irksome rules to
     check, so  are messier). <P> Too busy to have
     incorporated other suggestions yet. <P> What else?
     Yup:  the current regex implementation is known to
     commit blunders  of various sorts when passed "very
     long" strings, & I've already done all I  can to
     avoid that.  If you have Python source with multi-
     hundred character  lines, things may not work, and if
     so that won't get fixed soon.  Parsing a  character
     at a time would work, but would be so much slower the
     tool wouldn't  get used; while speed isn't crucial
     here, a gross slowdown is unacceptable. <P> 
    sez-me-anyway-ly y'rs  - tim <P> Tim Peters    <A
     HREF="mailto:tim_one@msn.com">tim_one@msn.com</A>, <A
     HREF="mailto:tim@dragonsys.com">tim@dragonsys.com</A>
     not speaking for Dragon Systems Inc."""

    [NOTE, CAUTION, WARNING, ERROR] = range(4)
    _level_msg = ['note', 'caution', 'warning', 'error']

    # The function bound to module vrbl "format_msg" defaults to the
    # following, and is used to generate all output; if you don't
    # like this one, you know what to do <wink>.
    
    def _format_msg(
          # the error msg, like "unique id"
          msg,
    
          # sequence of details, passed thru str & joined with
          # space; if empty, not printed
          details = (),
    
          # name of source file
          filename = '???.py',
    
          # source file line number of offending line
          lineno = 0,
    
          # the offending line, w/ trailing newline;
          # or, if null string, not printed
          line = '',
    
          # severity (NOTE, CAUTION, WARNING, ERROR)
          level = CAUTION ):
        try:
            severity = _level_msg[level]
        except:
            raise ValueError, 'unknown error level ' + `level`

        g.es('%(filename)s:%(lineno)d:[%(severity)s]' % locals() )
        if details:
            from string import join
            g.es("%s:" % msg, join(map(str, details)) )
        else:
            g.es(msg)
        if line:
            g.es(line)
    
    format_msg = _format_msg
    
    # Create sets of 'safe' names.
    import sys

    _system_name = {}   # set of __xxx__ special names
    for name in """\
          abs add and
          bases builtins
          call class cmp coerce copy copyright
          deepcopy del delattr delitem delslice
              dict div divmod doc
          file float
          getattr getinitargs getitem getslice getstate
          hash hex
          init int invert
          len long lshift
          members methods mod mul
          name neg nonzero
          oct or
          pos pow
          radd rand rdiv rdivmod repr rlshift rmod rmul ror
              rpow rrshift rshift rsub rxor
          self setattr setitem setslice setstate str sub
          version
          xor""".strip().split():
        _system_name['__' + name + '__'] = 1
    _is_system_name = _system_name.has_key

    import keyword
    
    _keyword = {}   # set of Python keywords
    for name in keyword.kwlist + ['as', 'str'] + dir(__builtins__) + \
            dir(list) + dir(dict):
        _keyword[name] = 1

    #builtins isnt the same from exec as from script outside Leo
    #maybe import builtins? same with methods if it even exists

    _builtin = {}   # set of builtin names
    """for name in dir(__builtins__) + sys.builtin_module_names:
        _builtin[name] = 1
    """
    _methods = {}   # set of common method names
    """for name in [].__methods__ + {}.__methods__:
        _methods[name] = 1"""
    
    _lotsa_names = {}   # the union of the preceding
    for dct in (_system_name, _keyword, _builtin, _methods):
        for name in dct.keys():
            _lotsa_names[name] = 1
    
    #del sys, name  #, dct string,  dict


    
    # Compile helper regexps.
    import regex
    
    # regexps to find the end of a triple quote, given that
    # we know we're in one; use the "match" method; .regs[0][1]
    # will be the index of the character following the final
    # quote
    _dquote3_finder = regex.compile(
        '\([^\\\\"]\|'
        '\\\\.\|'
        '"[^\\\\"]\|'
        '"\\\\.\|'
        '""[^\\\\"]\|'
        '""\\\\.\)*"""' )
    _squote3_finder = regex.compile(
        "\([^\\\\']\|"
        "\\\\.\|"
        "'[^\\\\']\|"
        "'\\\\.\|"
        "''[^\\\\']\|"
        "''\\\\.\)*'''" )
    
    # regexps to find the end of a "uni"-quoted string, given that
    # we know we're in one; use the "match" method; .regs[0][1]
    # will be the index of the character following the final
    # quote
    _dquote1_finder = regex.compile( '\([^"\\\\]\|\\\\.\)*"' )
    _squote1_finder = regex.compile( "\([^'\\\\]\|\\\\.\)*'" )
    
    # _is_junk matches pure comment or blank line
    _is_junk = regex.compile( "^[ \t]*\(#\|$\)" ).match
    
    # find leftmost splat or quote
    _has_nightmare = regex.compile( """["'#]""" ).search
    
    # find Python identifier; .regs[2] bounds the id found;
    # & it's a decent bet that the id is being used as an
    # attribute if and only if .group(1) == '.'
    _id_finder = regex.compile(
        "\(^\|[^_A-Za-z0-9]\)"  # bol or not id char
        "\([_A-Za-z][_A-Za-z0-9]*\)" ) # followed by id

    #del regex, keyword
    #@    << bfcrunch >>
    #@+node:ekr.20050328091952.51:<< bfcrunch >>
    
    def bfcrunch(getline, filename='???.py' ):
        # for speed, give local names to compiled regexps
        is_junk, has_nightmare, id_finder, is_system_name = \
            _is_junk, _has_nightmare, _id_finder, _is_system_name
    
        end_finder = { "'": { 1: _squote1_finder,
                              3: _squote3_finder },
                       '"': { 1: _dquote1_finder,
                              3: _dquote3_finder }
                     }
    
        multitudinous = {}  # 'safe' names + names seen more than once
        for name in _lotsa_names.keys():
            multitudinous[name] = 1
    
        trail = {}  # maps seen-once name to (lineno, line) pair
        in_quote = last_quote_lineno = lineno = 0
        while 1:
            # eat one line
            where = lineno, line = lineno + 1, getline()
            if not line:
                break
            if in_quote:
                if in_quote.match(line) < 0:
                    # not out of the quote yet, in which case a uni-
                    # quoted string *must* end with a backslash
                    if quote_length == 3 or (len(line) > 1 and
                                             line[-2] == '\\'):
                        continue
                    format_msg( "continued uni-quoted string must \
    end with backslash",  # making this line its own test case <wink>
                                filename=filename,
                                lineno=lineno,
                                line=where[1],
                                level=ERROR )
                    # the source code is so damaged that more
                    # msgs would probably be spurious, so just
                    # get out
                    return
                # else the quote has ended; get rid of everything thru the
                # end of the string & continue
                end = in_quote.regs[0][1]
                line = line[end:]
                in_quote = 0
            # get rid of junk early, for speed
            if is_junk(line) >= 0:
                continue
            # awaken from the nightmares
            while 1:
                i = has_nightmare(line)
                if i < 0:
                    break
                ch = line[i]    # splat or quote
                if ch == '#':
                    # chop off comment; and there are no quotes
                    # remaining because splat was leftmost
                    line = line[:i]
                    break
                else:
                    # a quote is leftmost
                    last_quote_lineno = lineno
                    quote_length = 1  # assume uni-quoted
                    if ch*3 == line[i:i+3]:
                        quote_length = 3
                    in_quote = end_finder[ch][quote_length]
                    if in_quote.match(line, i + quote_length) >= 0:
                        # remove the string & continue
                        end = in_quote.regs[0][1]
                        line = line[:i] + line[end:]
                        in_quote = 0
                    else:
                        # stuck in the quote, but anything
                        # to its left remains fair game
                        if quote_length == 1 and line[-2] != '\\':
                            format_msg( 'continued uni-quoted string \
    must end with backslash',
                                        filename=filename,
                                        lineno=lineno,
                                        line=where[1],
                                        level=ERROR )
                            # the source code is so damaged that more
                            # msgs would probably be spurious, so just
                            # get out
                            return
                        line = line[:i]
                        break
    
            # find the identifiers & remember 'em
            idi = 0     # index of identifier
            while 1:
                if id_finder.search(line, idi) < 0:
                    break
                start, idi = id_finder.regs[2]
                word = line[start:idi]
                if multitudinous.has_key(word):
                    continue
                if trail.has_key(word):
                    # saw it before; don't want to see it again
                    del trail[word]
                    multitudinous[word] = 1
                else:
                    trail[word] = where
                    if word[:2] == '__' == word[-2:] and \
                       not is_system_name(word):
                        format_msg( 'dubious reserved name',
                                    details=[word],
                                    filename=filename,
                                    lineno=where[0],
                                    line=where[1],
                                    level=WARNING )
    
        if in_quote:
            format_msg( 'still in string at EOF',
                        details=['started on line', last_quote_lineno],
                        filename=filename,
                        lineno=lineno,
                        level=ERROR)
    
        inverted = {}
        for oddball, where in trail.items():
            if inverted.has_key(where):
                inverted[where].append(oddball)
            else:
                inverted[where] = [oddball]
        bad_lines = inverted.keys()
        bad_lines.sort()    # i.e., sorted by line number
        for where in bad_lines:
            words = inverted[where]
            format_msg( 'unique id' + 's'[:len(words)>1],
                        details=words,
                        filename=filename,
                        lineno=where[0],
                        line=where[1],
                        level=CAUTION )
    
    #@-node:ekr.20050328091952.51:<< bfcrunch >>
    #@nl

    bfcrunch(getline, filename= 'exS')

#@-node:ekr.20050328091952.50:Bugfixcrunch
#@-node:ekr.20050328091952.49:tim_one_crunch
#@-node:ekr.20050328091952.32:codeing macros
#@+node:ekr.20050328091952.52:pre/post macros
#@+node:ekr.20050328091952.53:+DQ3

def dynaZ_DQ3(c):
    """enclose the selected txt in  whatever is in the copy buffer 
    gets put before and the matching after
    if '(' is in the copy then (selected) is put
    {'(':')', '{':'}', '[':']', '<-- ':' -->', '/*':'*/'}
     chose SQ, DQ DQ3 SQ3
    is there a DQ2 SQ2?

    have to have something selected to insert anything even an empty.
    fix that. now if nothing selected put a blank docstring
    its not easy to have an empty copy buffer with the present Tk copy
    or cut with nothing selected no change takes place.

    used for commenting out sections of code or to create docstrings
    might be usefull to backtrack to the previous line, insert enter
    that will put the insertpoint on the right indent
    maybe too much magic though
    add reverse dict to allow selection of either start or end char
    add try/except if/else
    subfunction the replace so can add doctest to it. same elsewhere.
    """
    
    newSel = dynaput(c, [])
    #print '%r'%newSel
    if not newSel: data = '\n'
    else: data = str(newSel)

    #need something to reselect wtith the newsel inserted in case it was empty
    #in circular logic land

    repchar = g.app.gui.getTextFromClipboard()
    if not repchar or not newSel:
        repchar = '"""'

    repdict = {'(':')', '{':'}', '[':']', '<!-- ':' -->', '/*':'*/'}
    #get cute and use a reverse dict if repchar in .values()
    revdict = dict([[v, k] for k, v in repdict.items()])

    #add some specialized sourounders, need to add to choice menu in putmenu
    repdict.update({'try':'except', 'if':'else', '>>>':'...',})
    
    #could also use a method if # or //, then put at front of every line

    if repchar in repdict.keys():
        rep2char = repdict[repchar]

    elif repchar in revdict.keys():
        #allow user to copy or either start or end char
        #output will be in the correct order of the pair
        repchar = revdict[repchar]
        rep2char = repdict[repchar]

    else: rep2char = repchar  #rep2char.reverse()?

    sx = []
    #   these will messup because they dont try to follow proper indent
    #  for language another than python obviously you would need more
    if repchar == 'try':
        sx.append('\n%s:\n    %s %s Exception:\ng.es_exception("eme", full= True)'%(
                repchar, data, rep2char))
    elif repchar == 'if':
        sx.append('\n%s 1 == 1:\n    %s%s:\npass'%(
                repchar, data, rep2char))
    elif repchar == '>>>':
        sx.append('\n    """\n    %s\n    %s %s\n    """\n'%(
                repchar, rep2char, data ))
    else:
        sx.append('%s%s%s'%(repchar, data, rep2char))
        
    if not newSel: g.es(''.join(sx) ) #life is too short
    else: dynaput(c, sx)
#@-node:ekr.20050328091952.53:+DQ3
#@+node:ekr.20050328091952.54:du_test-str
""" if you runthis script on itself it can get infinate on you.
not anymore, but if you do get some recursion in your script,
  if you have a console hit ^C once. save your work often.
  python -i leo your.leo is how to get the console
 @test error reporting seems to go only to the console as yet.
 
 also import of leo* files might be a problem. 
 best used in named sections for functions, 
 you can also put the doc under test in its own node.
 you can also put the code in a named function in a subnode
 inside triple quotes so that the code still has syntax highlighting.
 care to include an extra >>> #blank at the end if used this way.
 there are a few examples in dynacommon, sanitizte_ , ??

 fixed problem for py2.4, master removed from doctest __all__ 
verbosity= fails if leoTest 4.3a1 or earlier

can an option be the first time you click on a dyna item
it becomes a button. 
du_test, delfirstchar often you can't stop at just once.

0 passed and 0 failed. shoud report even if verbosity 0
"""
#@+at
# 
# DO NOT LOAD leo*.py files with load_module it will crash Leo
# leoTest.py is ok, is more or less a standalone to provide @test
# 
# Leo has a safeimport, once it stabalizes can use it for @file.
# you must not run python -OO to use doctest! we detect this
# -O is ok but note, this removes asserts, maybe counter productive!
# 
# 
# uses parts of Rollbackimporter and fileLikeObject
# many thanks to python cookbook providers and contributers
#@-at
#@@c

import leoGlobals as g

#@<< Classes >>
#@+node:ekr.20050328091952.55:<< Classes >>
import os, sys, time

import StringIO

#__metaclass__ = type

#is sys.platform in less than py2.3?
if sys.platform[:3] == 'win':  
    if sys.version_info[:2] >= (2, 3):
        win_version = {4: "NT", 5: "2K", 6: "XP",
            }[os.sys.getwindowsversion()[0]]
    else: win_version = 'NT' #os.name?
else: win_version = 'NM'

if sys.version_info[:2] >= (2, 5): win_version += ' py>24'
elif sys.version_info[:2] >= (2, 4): win_version += ' py>23'
elif sys.version_info[:2] >= (2, 3): win_version += ' py>22'
elif sys.version_info[:2] >= (2, 2): win_version += ' py>21'
elif sys.version_info[:3] == (1, 5, 2): win_version += ' py152'
else: win_version += ' py<21'

#@verbatim
#@suite unittestfromdoctest needs py2.3

try:
    g.app._t
except Exception:
    import unittest
    class _t_(unittest.TestCase):
        def runTest(self):
            pass
    _t = _t_()
    g.app._t = _t  #allow you to use _t in your script
    del _t
    #del unittest?

#@+others
#@+node:ekr.20050328091952.56:ExitError
class ExitError(Exception):
    """
    this is a cleaner way to exit a script
    raise SystemExit or something else causes much traceback
    so does this but maybe can solve that eventually
    maybe del frames from sys.exception
    also may be called after printing trace from real error
    """
    def __init__(self, value= 'Script decided to bail\n'):
        self.value = value

    def __str__(self):
        return `self.value`
#@-node:ekr.20050328091952.56:ExitError
#@+node:ekr.20050328091952.57:importCode
"""aspncookbook/82234
Importing a dynamically generated module
by Anders Hammarquist
Last update: 2001/10/17, Version: 1.0, Category: System
This recipe will let you import a module from code that is dynamically
generated. My original use for it was to import a module stored in a
database, but it will work for modules from any source.
had to add \n and chg name module and del if already in modules
"""

def importCode(code, name, add_to_sys_modules= 0):
    """
    Import dynamically generated code as a module. code is the
    object containing the code (a string, a file handle or an
    actual compiled code object, same types as accepted by an
    exec statement). The name is the name to give to the module,
    and the final argument says wheter to add it to sys.modules
    or not. If it is added, a subsequent import statement using
    name will return this module. If it is not added to sys.modules
    import will try to load it in the normal fashion.

    import foo

    is equivalent to

    foofile = open("/path/to/foo.py")
    foo = importCode(foofile, "foo", 1)

    Returns a newly generated module.

    tried to inject a sample unittest sub class
    just to get assert_ and maybe the other tests automatically
    it is shown in the verbose though doctest can be told to ignore.
    next problem, if the test class is injected first, 
    the scripts first docstring is no longer the __doc__ of the module
    if its injected last then _t is undefined...
    do I exec it first to get the doc, then set mymod.__doc__ = doc?
    cant have any code before the doc. might be an acceptable price to pay
    but unittest also doesnt know it then the scripts cant do both
    """
    import sys, imp
    try:
        if hasattr(sys.modules, name):
            del(sys.modules[name])
    
        modl = imp.new_module(name )  #was module

        #problem if run du_test now on new Leo4.3 scripts w/o c,g,p defined
        #shoulden't matter if its other than c,g,p then still errors?
        #might not even be necessary. had a script that was a getscript on itself
        try:
            exec code + '\n' in modl.__dict__ #du_test
        except AttributeError, e:
            g.es('%s\npossibly no doc string defined?'%(e,))
            g.g.es_exception(full= True)

        except NameError:
            c = g.top(); p = c.currentPosition()
            d = {'c':c, 'p':p, 'g':g}
            g.es('*** defining c,g & p ***')
            modl.__dict__.update(d)
            exec code + '\n' in modl.__dict__ #du_test w/c,g,p

        if add_to_sys_modules:
            sys.modules[name ] = modl

    except Exception:  #probably not exactly correct
        #g.es_exception()
        raise # ImportError
   
    return modl

if 0: # Example
    code = """
def testFunc():
    print "spam!"

class testClass:
    def testMethod(self):
        print "eggs!"

import unittest
class _t_(unittest.TestCase):
    def runTest(self):
        pass
_t = _t_()
"""

    m = importCode(code, "test")
    m.testFunc()
    o = m.testClass()
    t = m._t_()
    o.testMethod()

#
#@nonl
#@-node:ekr.20050328091952.57:importCode
#@-others
#@nonl
#@-node:ekr.20050328091952.55:<< Classes >>
#@nl

def dynaZ_du_test(c= None):
    """
    takeoff from run @test, see test.leo >py2.3 doctest

    run a unittest from a doctest docstring in the script
    will also run if headline is @test using leoTest in 4.2beta2+
    and in that case, all subnodes of @test will run, @suite too
    
 care required because the script under test is exec with any sideeffects.

 _functions ignored in doctest 
 nested sub functions ignored in doctest , py2.4b2+ too?
 note also you have to double backslashes or use r raw strings.

    in your script you can use:
    g.app._t.assert_(1 == 2) and other unittest compares
    you have to import leoGlobals to use it.
    which isn't a much of a deal breaker.
    
    is redirecting the unittest error to log properly. 
    try append -v to argv, no luck.
    need setting for verbose in leoTest instead of hardwired call
    dyna_menu.ini verbosity=0/1/2

    must be in leoText. run w/console python -i open to see
    need version 2.3. convert a doctest into a unittest if use leoTest
    du_test doesn't create temp files and doesn't require @file
seems I have developed a superstition about reload of sys and unittest. 
but dammed if @test nodes stoped redirecting, so reloads are back in again!
put all 3 back but one or the other might be enough. subject closed again.
flip verbose now flips 0 to 1, 1 to 2 and 2 to 0, default starts out at 0

    """
    import doctest
    import sys, os

    #1 leo globals, 0 forcefull sys, 2 underlying file stdio nfg
    use_Leo_redirect = 0 

    if c is None: c = g.top()
    p = c.currentPosition() 

    #solve the doc/unittest infinate problem if run test on this node
    if p.headString().startswith('du_test-str'): g.es('infinate'); return

    c.frame.putStatusLine('testing '+ p.headString()[:25], color= 'blue')
    #c.frame.statusText.configure(
    #    state="disabled", background="AntiqueWhite1")


    if pyO[0] == 'O':
        g.es('assert disabled, use g.app._t.assert_()',
            color= 'tomato')
        #unreliable as yet...
        if 0 and dynaZ_du_test.__doc__ is None:
            g.es('YOU HAVE RUN python -OO \ndoctest fails, @test ok',
                color= 'tomato')

    s = '*'*10
    g.es(win_version, time.strftime(
        #why is this not available? 
        #g.app.config.body_time_format_string or 
        '%H:%M.%S %m/%d/%Y'
    ))
    

    g.es('%s \ntesting in %s\n%s\n'%(
        s, p.headString()[:25], s), color= 'DodgerBlue')

    reload(sys)
    #print sys.argv
    #if not '-v' in sys.argv:
    #    sys.argv.append('-v')
    #    g.es(sys.argv)

    #@    << n_redirect >>
    #@+middle:ekr.20050328091952.58:guts
    #@+node:ekr.20050328091952.59:<< n_redirect >>
    #when run on @test print goes to console
    #this simple redirect isnt working
    #might need to set stdout/err more forcefully
    #have the same problem with evaluator 
    #and it screwsup log redirect after its done.
    if use_Leo_redirect == 1:
        g.redirectStdout(); g.redirectStderr()
    
    elif use_Leo_redirect == 0:
        sys.stdout = g.fileLikeObject() #'cato'
        sys.stderr = g.fileLikeObject() #'cate'
    
        #usually you dont want to do this,
        _sosav = sys.__stdout__
        sys.__stdout__ = sys.stdout
        _sesav = sys.__stderr__
        sys.__stderr__ = sys.stderr
    
    elif use_Leo_redirect == 2: #c.l.py suggested
        #how ironic, I can remove the requirement for temp file
        #for docutils, but not for redirecting IO? dup needs fileno
        _sosav = sys.__stderr__
        #_sesav = sys.stderr
        def myfileno(self= None, *argy, **kews):
            print 'fn', argy, kews
            return 1
        #g.funcToMethod(myfileno, g.fileLikeObject, 'fileno')
        #g.funcToMethod(fileno, g.fileLikeObject)
    
        #g.fileLikeObject.fileno = myfileno
        f = g.fileLikeObject()
        #f.fileno = 1  
        f.fileno = myfileno  #()
        #not callable, when it is callable it says not attribute!
        #AttributeError: redirectClass instance has no attribute 'fileno'
        #it goes deeper than I first thought, the redirecttolog is still there
    
    
        #f = file('out.txt', 'a')
        #os.dup2(1, sys.__stderr__.fileno())
        os.dup2(f.fileno, sys.__stderr__.fileno())
        #os.dup2(f.fileno(), sys.stderr.fileno())
    #@-node:ekr.20050328091952.59:<< n_redirect >>
    #@-middle:ekr.20050328091952.58:guts
    #@afterref
  #a bad named section is ignored when run
    #import/reload after redirect fixes redirect to log from unittest
    import leoTest
    import unittest

    reload(unittest)
    reload(leoTest)
    

    if p.headString().startswith('@test ') or\
         p.headString().startswith('@suite '):
        leoTest.doTests(all= False,
         verbosity= g.app.dynaMvar.du_test_verbose) #

    else:
        #@        << DocTest >>
        #@+middle:ekr.20050328091952.58:guts
        #@+node:ekr.20050328091952.60:<< DocTest >>
        
        tmpimp = tmp = 'mymod' #name for the mock module
        
        #g.es('mock writeing ', tmpimp)  #
        fo = None
        
        try:
            #could add a real/mock mode default mock, 
            #need to simulate file open for write+ since read will fail
        
            #fo = g.fileLikeObject(tmpimp) 
            script = g.getScript(c, p) #.strip()
            if not script: g.es('no script no test'); return
        
            #fo.write(script + "\n#e\n")
            #fo.seek(0, 0)  #rewind
            #fo.geek()  #test unknown attribute
        
        except Exception:
            g.es_exception(full= False)
            raise ExitError  #be nice if this happened w/o extra exytax error
        
        mod = None
        try:
        
            #mod = __import__(fo, {}, {}, ["*"])
            mod = importCode(script, tmpimp, add_to_sys_modules= 1)
        
        #could be other errors the way this is setup isnt there yet.
        except ImportError, err:
            g.es('error importing tmpimp\n', tmpimp, color='tomato')
            g.es_exception()
            #except needs a break or maybe the doctest goes in else?
            #you cant mix except and finally...
            #an exit w/o rais would belp too still need to close the file
        
        try:
            if mod:
                #need to tell it to ignore testing class t_
        
                doctest.testmod(mod, verbose= g.app.dynaMvar.du_test_verbose,
                     report= 1, globs=None, isprivate= doctest.is_private)
                #doctest.master.summarize()
                try:
                    #no longer exposed in py2.4
                    del doctest.master #bad idea if don't set to None
                    doctest.master = None
                except Exception:
                    pass
        
        except Exception, err:
            g.es('error doctest mod\n', mod, color='tomato')
            g.es_exception()
        
        if fo: fo.close() 
        #@nonl
        #@-node:ekr.20050328091952.60:<< DocTest >>
        #@-middle:ekr.20050328091952.58:guts
        #@nl

    #@    << f_redirect >>
    #@+middle:ekr.20050328091952.58:guts
    #@+node:ekr.20050328091952.61:<< f_redirect >>
    #code below may cause problem if not run 
    #if except traps further up
    #needs its own try/finally
    #is the __ mangling causing sys.__std* not to work corectly?
    
    if use_Leo_redirect == 1:
        g.restoreStdout(); g.restoreStderr()
    
    elif use_Leo_redirect == 0:
        oo = sys.stdout.get()  #read get()
        oe = sys.stderr.get()  #get()
        sys.stdout.close()
        sys.stderr.close()
    
        #if you didnt do this it wouldent need to be reversed
        sys.__stdout__ = _sosav
        sys.__stderr__ = _sesav
    
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
    
    elif use_Leo_redirect == 2:
        #if this works eliminate choice 0
        oo = 'stderr'  #sys.stderr.read()  #read get()
        #oe = sys.stderr.get()  #get()
        oe =''
        #sys.stderr.close()
        #sys.stderr.close()
        sys.__stderr__ = _sosav
        #sys.__stderr__ = _sesav
    
    if use_Leo_redirect != 1:
        for x in (oo + oe).splitlines():
            g.es('%s'%x, color= 'chocolate')
    #@nonl
    #@-node:ekr.20050328091952.61:<< f_redirect >>
    #@-middle:ekr.20050328091952.58:guts
    #@nl

    g.es('nonews is goodnews%s'%(g.choose(pyO[0] == 'O', ' +-O', ''),),
        color= 'DodgerBlue')


    #not sure why but this dissapears in a few seconds, 
    #maybe script end clears it? add an idle 200ms
    c.frame.putStatusLine(' fini ', color= 'DodgerBlue')
    #bad color here causes too much traceback
    #c.frame.statusText.configure(background="AntiqueWhite2")

#@+node:ekr.20050328091952.58:guts
#@-node:ekr.20050328091952.58:guts
#@-node:ekr.20050328091952.54:du_test-str
#@+node:ekr.20050328091952.62: htmlize

def dynaZ_htmlize(c= None):
    """htmlize a script, popup webbrowser to show.
    
    grabed parser fromfrom the moinmoin, 
    default is to strip leo sentinal lines.

    you must edit in browser & filename, 
       explorer c:\WINDOWS\TEMP\python.html
       or use %tmp%/htmlfile.html defined in dynacommon
    #@    <<more doc>>
    #@+node:ekr.20050328091952.63:<<more doc>>
    you can tweek the title in the format and sanitize_ method
    edit in your favorite style bits there too.
    copy silver_city.css where the filename will be
    
    uses psyco if available.
    
    script should be python, free from most syntax errors 
    but accepts other languages 
    and eveutually will use the keywords from that language
    for now call another parser, silvercity if it exists.
    sends @language css html perl c java and others to silvercity
    (not fully tested in all languages for all syntax)
    
    you can choose to colorize Names, Operators and Numbers seperately
    or not at all by editing the htmlize macro hopts dictionary. 
    Note: filesize larger if all 3 different than Text color.
    
    needs Leo4.2 but is easily revertable.
    
    could add linenumber and code metrics options.
    
    can make it capable of reading writing a file as well?
    wonder can I open browser and send it virtual html like in js?
    might mod for class & span instead of pre & font
    
    have to have path set for getScript to work. 
    in new leo it will traceback if not saved once?
    added some traps for empty script. 
    meaningfull errors messages can't really be determiate
    w/o some novice/expert clue from the system. 
    have a few depandancies on dyna otherwise could be scriptButton
    use python webbrowser.
    add experimental code folding on def & class for python only
     works in IE5 and firefox1 and shouldent affect others much
     might just be an extra header above def and class
     eventually will option it invisable for printing and copy&paste
     enable/disable in the htmlize options bunch as with other options
     and there would be an ini option available too in the great beyond.
    its cutting the def/class name and not enclosing the body of it
    
    this guy took it to the next level, like the idea of color themes.
    http://bellsouthpwp.net/m/e/mefjr75 /python/PySourceColor.py
    
    more advanced stripSentinals suggested by EKR.
    getconfig for ini options in hopts
    need another option to looklikeLeo
    show directives but not commented out, 
    others w/o excess space, verbatim as it is etc
    then can almost use extract named section to recreate nodes
    
    if showdefaults, it doesn't take into account
    the override factor in the defaults in hopts
    complicated by Properties dialog not being able to handle them all
    need to have more than one ini seletable as well
    for various class or color schemes or some other way to select them
    which css to embed. maybe get it from parsing a parent node or ???
    
    seems to be taking little longer to popup browser in py2.4.1, not always.
    if not python should check for silvercity, then one of the others
    maybe need option default colorizer, otherwise there is too much guessing.
    if neither then output as text. as it is now, temfile is written first
    and only output as text if it is not one of silvercity languages
    the others have more or less languages supported. a config nightmare.
    check is @file and offer to produce file.xyz.html
    check is @rst and if option dorst then send plain to docutils?
    add option css/font and if css 
    then eliminate dups is mandatory, css triples filesize.
    
    option   silvercity or src-hilite for other than plain or rst or @rst
    sent plain or rst to docutils if if available 
      else pre/pre w/wraping and headlines made of any node healines
    
    there should be an @language rst to help with REST syntax 
    possibly this would be a major pain just because.
    idea for further study though. @rst for now good enough
    and should not interfere with any rst* plugin
    #@nonl
    #@-node:ekr.20050328091952.63:<<more doc>>
    #@nl
    
    wonder still about how to solve encoding?
    rst/plain option not fully realized
    source-highlite still wants to make verbose to stderr?
    finish implementing EOLN and check in plain per body
    for new directives of wrap and lineending and language
    will any of this output survive various encoding
    will it validate as error free html?
    """
    #@    << initilize >>
    #@+node:ekr.20050328091952.64:<< initilize >>
    import os, sys
    import leoGlobals as g
    
    import cgi, cStringIO, re
    import keyword, token, tokenize
    
    #trick from aspn/299485
    #htmlize is really plenty fast even on >100k source, 
    #but may as well see if this ever causes errors
    #forgot to get some base timeings before and after.
    #doesnt help the silvercity branch
    
    base_class = object #is object in py2.2
    if 1:
        try:
            # If available use the psyco optimizing
            #might psyco be enabled elsewhere and still work in here?
            import psyco.classes
            if sys.version_info[:2] >= (2, 3):
                base_class = psyco.classes.psyobj
        except ImportError:
            pass 
    
    #this well could be version dependant
    _KEYWORD = token.NT_OFFSET + 1
    _TEXT    = token.NT_OFFSET + 2
    
    #is this going to have to be optionale too?
    #began the process, all attribs are htmlize_token_whatever
    #but is not as easy because the actual attributes don't match _colors
    _colors = {
        token.NUMBER:     '#483D8B', #black/darkslateblue
        token.OP:         '#000080', #black/navy
        token.STRING:     '#00AA00', #green 00cc66
        tokenize.COMMENT: '#DD0000', #red cc0033
        token.NAME:       '#4B0082', #black/indigo
        token.ERRORTOKEN: '#FF8080', #redred bare null does it
        _KEYWORD:         '#0066ff', #blue
        _TEXT:            '#000000', #black /is text fg color too
        '_leodir':        '#228B22', #directive, forest comment
        '_leosen':        '#BC8F8F', #sentinal, tan fade comment
        'bg':             '#FFFAFA', #snow
    }
    
    #@+at
    # m04726p05:10:02
    # m04726p10:20:11 posted to sf with a few minor slipups
    # did a few more reselects on the color. working well now
    # no dot before pre in style.
    # #@    @+others missed, need re, fixed.
    # see if can not write font for names and let it be text color
    # thats the bulk of the words and will reduce file size alot.
    # 
    # and empty node screws it up totally even though parent node python
    # going to need to test for language maybe.
    # and it should be parsable and probably free of most syntax errors
    # more problems
    # from the wtf dept. used rstrip to find indented sentinals?
    # and it finds them...
    # seems to eat directives only nodes. and the start of comment to Atc
    # attempt to drop to text if plain name to avoid the excess font baggage
    # set stdout back to default
    # problem can arise while debuggon changes to this script
    # sat that point stdout is redirected to file
    # and es_exception says its a closed file.
    # need a try/finally to close & restore, test if trips on error
    # already know finally happens before any return
    # 
    # htmlize works better as a button w/rclick checkbox options.
    # it should sense if python use parser,
    # if c or other silvercity language use that
    # if not a language other than plain, attempt to scan
    # and colorize at least the keywords outsise strings
    # otherwise just treat as text and flatten it and htmlize
    # maybe additionally headlineing the headlines.
    # make it immune to empty bodys.
    # obviously may as well strip comment.
    # maybe better to find a way to style then so they can be hid
    # then select all will only copy the code...
    # making a hide compatible w/firefox proveing to be difficult.
    # 
    # implimented programatic eating of comment sentinals option
    # it just returns.
    # im noticing some extra indentation after namedsection or ATothers
    # just the first line is extra indented,
    # adding an extra blank line cures it.
    # think it cant be getscript since the script still works!
    # didnt notice this problem yesterday though
    # had to move return from nosentinals before the writespace option
    # 
    # also its adding NL where the sentinal was sometimes, have to fix that.
    # inside the parser not so easy. should just pre strip them. fixed
    # fixed reversal of sanitizefilename use in title instead of first heading
    # 
    # maybe can make the parser relax to just colorize keywords in other 
    # languages. oddly enough it seems to do it pretty well already,
    # but it flaggs ?/@/other chars not valid outside strings/comment in 
    # python
    # r04805a01:41:32 and then there were decorators. more later, like py2.4 
    # later
    # perfect export will then be required.
    # getscript will handle it so it probably wont affect htmlize much
    # just made a long overdue shortcut to pythonw.exe,
    # damm the os.system flashes a command screen when silvercity is called.
    # have to see if there is a way around that. start minimized?
    # without starting from a pif that specifys that really cant go there.
    # wonder if that happened in mod_spelling? another reason to like spellpyx
    # m05314a09:22 finishing up configurables for 4.3 beta maybe
    # where does the time go?
    #@-at
    #@nonl
    #@-node:ekr.20050328091952.64:<< initilize >>
    #@nl

    #@    @+others
    #@+node:ekr.20050328091952.65:class Parser
    
    class Parser(base_class):
        """ prep the source for any language
            parse and Send colored python source.
        """
        #@	@+others
        #@+node:ekr.20050328091952.66:__init__
        
        def __init__(self, raw):
            """ Store the source text.
            """
            #self.raw = string.strip(string.expandtabs(raw) )
            self.raw = raw.strip().expandtabs(4) 
            #might normalize nl too
            
            #need to know delim
            cmtdelim = '#'
            if lang != 'python':
                sdict = g.scanDirectives(c, p) 
                #obviously for other language have to check is valid
                #or need open/close comment. 
                #misses the opening html cmt, [0] only for singles
                #not sure I even know all the comment specifyers
                # its @, // html, ' are there any that screwup regex?
                cmtdelim = sdict.get('delims', ['#'])
                cmtdelim = cmtdelim[0] or cmtdelim[1]
            
            self.posspan = 0 #keep pos for collapse links on def & class
            self.spancnt = 0
            
            self.fnd = re.compile(r"%s@\s*@+."%(cmtdelim,) )
        
            #g.es('using delim=', cmtdelim)
            
            #if hopts['stripsentinals']: almost always do something
            self.raw = stripSentinels(self.raw, **hopts)
        
        #@-node:ekr.20050328091952.66:__init__
        #@+node:ekr.20050328091952.67:format
        
        def format(self, formatter, form):
            """ Parse and send the colored source.
            """
        
            # store line offsets in self.lines
            self.lines = [0, 0]
            pos = 0
            while 1:
                pos = self.raw.find(EOLN, pos) + 1
                if not pos: break
                self.lines.append(pos)
            self.lines.append(len(self.raw))
        
        
            self.pos = 0
            text = cStringIO.StringIO(self.raw)
        
            #use of \n not sure if will follow users lineending, but it should
            #anywhere htmlize adds it should use EOLN
        
            # parse the source and write it
            try:
                tokenize.tokenize(text.readline, self)
            except tokenize.TokenError, ex:
                msg = ex[0]
                line = ex[1][0]
                print "<h3>ERROR: %s</h3>%s" % (
                    msg, self.raw[self.lines[line]:])
        #@-node:ekr.20050328091952.67:format
        #@+node:ekr.20050328091952.68:__call__
        
        def __call__(self, toktype, toktext, (srow,scol), (erow,ecol), line):
            """ Token handler.
            """
            if 0: print "type", toktype, token.tok_name[toktype], "text",\
                    toktext, "start", srow,scol, "end", erow,ecol, "<br>"
        
        
            # calculate new positions
            oldpos = self.pos
            newpos = self.lines[srow] + scol
            self.pos = newpos + len(toktext)
        
            # handle newlines
            if toktype in [token.NEWLINE, tokenize.NL]:
                print
                return
        
            if hopts['codefold']: 
                if self.posspan >= self.pos:
                    dospan = False
                else: dospan = True
        
            style = ''
            if toktype == tokenize.COMMENT:
                #setrip comment a little more complicated than sentinals
                #sentinals are always exactly one line, sometimes indented
                #comments after code would need to do NL?
                
                if toktext.lstrip().startswith('#@'):
                    
                    #if hopts['stripsentinals']: return  #do in __init__
                        
                    if self.fnd.findall(toktext):
                        toktype = '_leodir'
                    else:
                        toktype = '_leosen'
        
            # send the original whitespace, if needed
            if newpos > oldpos:
                sys.stdout.write(self.raw[oldpos:newpos])
        
            # skip indenting tokens
            if toktype in [token.INDENT, token.DEDENT]:
                self.pos = newpos
                return
        
            # map token type to a color group
            if token.LPAR <= toktype and toktype <= token.OP:
                toktype = token.OP
        
            elif toktype == token.NAME and keyword.iskeyword(toktext):
                toktype = _KEYWORD
        
                if hopts['codefold'] and toktext in ['def', 'class',]:
                    dospan = True
                    self.posspan = self.pos
                    self.spancnt += 1
                    tag = '%s%s'%(cgi.escape(toktext), self.spancnt,)
                    sys.stdout.write("""\
        <a onclick="toggle(%s)" onmouseover="this.style.color='red'" onmouseout="this.style.color='black'">
        <h5>%s<img src="rarrow.gif" width="14" height="14"></h5></a>
        <span ID=%s Style=Display:''>
        """%(tag, tag, tag,  # None, none turns it off by default
            )) #need a 2pass to do this right, or look 1ahead to def/class name
        
        
            #this could be a decorator if run on py2.4 code from <py2.4
            if toktype == token.ERRORTOKEN:
                style = ' style="border: solid 1.5pt #FF0000;"'
        
            #color = _colors.get(toktype, _colors[_TEXT])
            #instead use try to bail if no key defaulting to body fg color
        
            dofont = True
            try:
                color = _colors[toktype]
                sys.stdout.write('<font color="%s"%s>' % (color, style))
            except Exception:
                dofont = False
        
            sys.stdout.write(cgi.escape(toktext))
            if dofont: sys.stdout.write('</font>')
        
            if hopts['codefold']: 
                #this is going to need allot more work to be reliable
                if dospan: #set when out of the def or class
                    self.posspan = 0
                    sys.stdout.write('</span>')
        #@nonl
        #@-node:ekr.20050328091952.68:__call__
        #@-others
    #@-node:ekr.20050328091952.65:class Parser
    #@-others

    if c is None: c = g.top()
    p = c.currentPosition() 
    silvercity = err = None
    
    #to remind, really need to get keywords from Leo for some languages
    #then could handle odd languages better w/same parser
    #c.frame.body.colorizer.python_keywords.append("as")
    #@    <<hopts>>
    #@+node:ekr.20050328091952.69:<<hopts>>
    #dyna would have read the ini already into a global Bunch
    #that will be one of the options for htmlize
    #its probably still possible to screwup the ini and dyna won't import
    
    #need to use a getter in Bynch so nonesistant ivar returns None?
    #possibly could set it with a get and default if doesn't exist property?
    
    if not hasattr(g.app.dynaMvar, 'htmlize_filename') or\
             g.app.dynaMvar.htmlize_filename == 'default':
        filename = sys.modules['dyna_menu'].htmlfile
    else:
        #and don't blame me or Leo if you make this a URI and get burned...
        filename = g.app.dynaMvar.htmlize_filename
    
    if not hasattr(g.app.dynaMvar, 'htmlize_timestring') or\
            g.app.dynaMvar.htmlize_timestring == 'default':
        timestring = sys.modules['dyna_menu'].dynaB_Clip_dtef(None, ret= 'r')
    elif g.app.dynaMvar.htmlize_timestring == 'leodefault':
        timestring = c.getTime(body=True)
    
    else:
        #effectively a string because I'm not planning on using eval
        timestring = g.app.dynaMvar.htmlize_timestring
    
    #decide which options to apply
    #strip sentinals, comments, syntaxcheck for only python?
    #then create alternate reality for c, c++, other language
    #assume text only nodes are language plain? respect killcolor?
    #to simplify the output 
    #set True for noNUMBER, noOP or noNAME 
    #to disable seperate colors for that entity.
    # the more colors the bigger the output html
    #have to switch to lowerrunoncase names, ini is not case sensitive for items
    #could make another run thru to use the proper cased attributes but life is too short
    #or make it a caseinsensitive Bunch subclass
    #why isnt this a Bunch already?
    hopts = {
      'codefold':False, #experimental, can be more confusing
      'stripcomments':False, #still to do
      'stripsentinals':True,   #you can have directives if no sentinals.
      'stripnodesents': False, # False: leave node sentinels.
      'stripdirectives':False,
      #no color key, that item defaults to text color
      'nonumber':False,
      'noop':False,
      'noname':True,  
      'filename': filename,  #in dynacommon or ini
      'timestring': timestring,
       #path to silvercity css file, that might be too hard to debug.
    }
    
    #syncup ini with default hopts
    for k,v in hopts.items():
        if k in ['filename', 'timestring', ]: continue
        #g.trace(k, v)
        if not hasattr(g.app.dynaMvar, 'htmlize_'+k.lower()): continue
        #g.trace('has :', getattr(g.app.dynaMvar, 'htmlize_'+k.lower()))
        #these should already be verified T/F
        hopts[k] = getattr(g.app.dynaMvar, 'htmlize_'+k.lower())
    
    #much as I hate to admit it, the colors will have to be changable
    #and color might be different for each language
    #should allow external css or settable style options same way
    #the Properties dialog only can handle a dozzen options on a large screen
    
    #I know there is a way to do this inside the _color dict
    #it would involve setting hopts before calling initilize
    if hopts['nonumber']: del _colors[token.NUMBER]
    if hopts['noop']:     del _colors[token.OP]
    if hopts['noname']:  del _colors[token.NAME]
    #@nonl
    #@-node:ekr.20050328091952.69:<<hopts>>
    #@nl
    lang = g.scanForAtLanguage(c, p)

    #str only fails is there is no current encoding.
    #was erroniously thinking it always fails on Unicode.
    lang = str(lang).lower()
    titl = "%s Leo %s script %s"%(
            p.headString()[:75], lang, hopts['timestring'])

    #think this trips an assert if you pass a vnode    
    #redundant if @rst or plain and fails if the first node is empty
    #will have to redesign this flow
    source = g.getScript(c, p)  #.strip()

    #if no path set getScript will return empty script, bug <4.3a4
    #must get text other way and do another type of htmlize

    _sysstdsav = sys.__stdout__
    #@    <<header plain footer>>
    #@+node:ekr.20050328091952.70:<<header plain footer>>
    def outheader():
        sx = []
        #this will have to get actual encoding but its a start
        meta = ['<meta http-equiv="Content-Type" content="text/html; charset=utf-8">']
        #append anyo ther meta required
        sx.append('<html><head>%s%s<title>'%(EOLN, EOLN.join(meta),))
        sx.append('%s </title>%s'%(sanitize_(titl), EOLN))
    
        #here would be a good spot for @noindent directive but skip a line
        #or build the string in the outermost indentation
        sx.append("""<STYLE TYPE="text/css"><!--
    pre, H1 {color:%s; FONT-SIZE: 80%%; FONT-WEIGHT: bold; }
    Text {background:%s;}
    --></STYLE>
    <SCRIPT LANGUAGE="JavaScript"><!-- 
    //Serenity Right Mouse Click Customisation
    function toggle(e) 
    {  
    if (e.style.display == "none") 
    	{
    	e.style.display = "";
    	 } 
    else 
    	{     
    	e.style.display = "none";  
    	}
    }
    //--></SCRIPT>"""%(
           _colors[_TEXT], _colors['bg'])) #was both #cc9999
    
        sx.append('</head><body text="%s" bgColor="%s">'%(
            _colors[_TEXT], _colors['bg']))
        sx.append('<H3># %s</H3>%s'%(titl, EOLN,))
        sx.append('<pre>')  # style
        sx.append('<font face="Lucida,Courier New">')
    
        return EOLN.join(sx)
        
    def plainout(src):
        g.es('bad or no hiliter language or option')
        return '%s%s%s'%(EOLN, src, EOLN)
    
    def outfooter():
        sx = []
        sx.append('</font></pre>')
        sx.append('</body></html>')
        return EOLN.join(sx)
    #@-node:ekr.20050328091952.70:<<header plain footer>>
    #@nl
    try:
        if not source: raise ValueError

        # write colorized version to "python.html"/filename
        sys.stdout = open(hopts['filename'], 'wb')  # wt, wb, w

        #fix dups when get silversity to do fragments
        #sys.stdout.write(outheader())

        #you cant have get both @lang python and @rst
        #but subnodes of @lang might be syntax colored later somehow
        #possibly will have to capture stdout and make a function
        #and sentinals as comments can be wacky if @language changes
        

        g.es('output', p.headString())

        if lang in ['plain', 'rst', None, '',] or \
              c.currentPosition().headString().strip()[:4] == '@rst':
            g.es('rst or %s , wait...'% lang)
            sys.stdout.write(outheader())
            #@            << plain or rst >>
            #@+node:ekr.20050328091952.71:<< plain or rst >>
            
            #do a linear node crawl, 
            # htmlize @language nodes
            # append docutils or plain text wrapped output
            #can you want plain or rst and also not stripsentinals?
            #might have to add option or flipper to not follow subnodes
            #thats the theory anyway...  FIXME
            
            #codeblock and latex not supported much yet
            #don't want to reimpliment rst2 either
            #individual bodys are not getting enough <Br>
            
            try:
                import docutils
            except:
                docutils = None
            else:
                #have to investigate custom config files
                #please evolve faster docutils.
                import docutils.parsers.rst
                from docutils.core import Publisher
                from docutils.io import StringOutput, StringInput
                pub = Publisher()
                #still depends on silvercity installed
                #@    << define code-block >>
                #@+node:ekr.20050328091952.72:<< define code-block >>
                def code_block(name,arguments,options,content,lineno,content_offset,block_text,state,state_machine):
                    
                    """Create a code-block directive for docutils.
                    lifted from rst2 and attempt to use 
                    in either src-hilite or silvercity while @language plain
                    or provide own generator if neither active
                    """
                    
                    # See http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/252170
                    language = arguments[0]
                    module = getattr(SilverCity,language)
                
                    generator = getattr(module,language+"HTMLGenerator")
                    io = StringIO.StringIO()
                    generator().generate_html(io, EOLN.join(content))
                    html = '<div class="code-block">\n%s\n</div>\n'%io.getvalue()
                    raw = docutils.nodes.raw('',html, format='html') #(self, rawsource='', text='', *children, **attributes):
                    return [raw]
                    
                # These are documented at http://docutils.sourceforge.net/spec/howto/rst-directives.html.
                code_block.arguments = (
                    1, # Number of required arguments.
                    0, # Number of optional arguments.
                    0) # True if final argument may contain whitespace.
                
                # A mapping from option name to conversion function.
                code_block.options = {
                    'language' :
                    docutils.parsers.rst.directives.unchanged # Return the text argument, unchanged
                }
                
                code_block.content = 1 # True if content is allowed.
                 
                # Register the directive with docutils.
                docutils.parsers.rst.directives.register_directive('code-block',code_block)
                #@nonl
                #@-node:ekr.20050328091952.72:<< define code-block >>
                #@nl
             
            current = c.currentPosition()
            def outheadline(cur, ):
                hl = g.choose(cur.headString().startswith('@rst'), 5, 4)
                return '<H%d>%s</H%d>%s'%(hl, cur.headString(), hl, EOLN )
            
            sys.stdout.write(outheadline(current))
            
            for psib in current.self_and_subtree_iter():
                sys.stdout.write(outheadline(psib))
                s = psib.bodyString()
                #.. code-block:: Python
            #@verbatim
                #@ignore
            
                #here let docutils have the body, but what about
                #previous Rest commands that might still be active?
                #dynawrap defaults textwrap or will do Leo wrap
                #have to fixit do it returns rather than prints though
                #also check for @language & few others and highlight
                #so will have to functionalize the highliters eventually
                #also might want some nodes line numbered, 
                #using docutils css on some nodes and on other elements 
                #H3 maybe should include a class=
                #subnodes should be indented? that could cause Rest errors
                
                # This code snipet has been taken from code in rst2
                #snipped from code contributed by Paul Paterson 2002-12-05.
                if docutils and s.strip():
                    pub.source = StringInput(source=s)
            
                    # need to set output so doesn't generate
                    #its own footers and headers on every other block
                    #nowhere does it mention other options! 
                    #docutils docs heal thyself.
                    writer='html' ; enc="utf-8"
                    #standalone, pep, python
                    pub.set_reader('standalone', None, 'restructuredtext')
            
                    pub.destination = StringOutput(pub.settings, encoding=enc)
                    pub.set_writer(writer)
            
                    
                    try:
                        output = pub.publish(argv=['']) #--traceback
                    except Exception:
                        #docutils puts errors to stderr, not redirected
                        g.es('ERRORS Found in rstText', psib.headString())
                        output = s
                else:
                    #output = s.replace(' ', '&nbsp').replace('\n', '<Br>\n')
                    output = s
            
                #till I get more docutil aware
                output = output.replace('<body>','').replace('<html>','')
                output = output.replace('</body>','').replace('</html>','')
                sys.stdout.write(output)
            #@-node:ekr.20050328091952.71:<< plain or rst >>
            #@nl

        elif lang == 'python':
            #this may no longer be advantagouus 
            #for every option to do first. and in the same order
            sys.stdout.write(outheader())
            pars = Parser(source)
            pars.format(None, None)

        else:
            g.es('hilite %s , wait...'% lang)
            #should decide somehow if can do the language
            #before commiting to a colorizer
            #plain should always be the fallback instead of first
            #this will get some reflow analisis

            #@            << restripper >>
            #@+node:ekr.20050328091952.73:<< restripper >>
            #source1 = stripSentinels(source, 1,0,1,1)
            #this may not be optimal either if language overlap
            #dissallowing strip* for now, later may preprocess
            #problem is delimiters in mixed @language...
            
            #source = stripSentinels(source, 1,0,0,0) 
            #& fix delims that are also sentinals? but how?
            #for now this is just as broken as before. just less noise
            #might have to find another option than getScript
            #skipping it altogether
            
            
            #q&d restripper of delimited sentinals.
            #a fix in stripSentinals is possibly but still problematic.
            #if you have mixed lang this can still fail
            #mixed languages in html of javascript css are not uncommom
            #just strip all single line comments start w[1:2]@[+-@] for a few langs
            #sorry if I missed your favorite
            #will determine how to add back stripnodesents option a different way
            #and or improvestripSentinals for mixed @language
            sx = []
            badsent = ('//@', '#@', '/*@', ';@', )
            
            for x in source.splitlines(True):
                #can this be faster than not x and not x: append instead of continue?
                if x[0:2] in badsent or x[0:3] in badsent: continue
                sx.append(x)
            source = ''.join(sx)
            #@nonl
            #@-node:ekr.20050328091952.73:<< restripper >>
            #@nl

            if hasattr(g.app.dynaMvar, 'htmlize_hiliter') and\
                g.app.dynaMvar.htmlize_hiliter and\
                  g.app.dynaMvar.htmlize_hiliter != 'silvercity' :
                sys.stdout.write(outheader())
                #@                << src-highlite >>
                #@+node:ekr.20050328091952.74:<< src-highlite >>
                #@+at
                # does better job on java than silvercity and has more 
                # languages
                # what no elisp in a gnu language?
                # 
                # need to get the css option without the bloated size
                # which might mean a post processing step.
                # why can't I inject font color default on the command line?
                # 
                # sourceforge.net/sourceforge/gnuwin32/src-highlite-1.11-bin.zip 
                # win32
                # other systems will have to build or find their own
                # 
                # source-highlight -s cpp -f html $*
                # source-highlight -s java -f html $*
                # java, javascript, cpp, prolog, perl, php3, python, ruby, 
                # flex, changelog, lua, caml, sml, log)
                #        keyword blue b ;      for language keywords
                #        type darkgreen ;      for basic types
                #        string red ;          for strings and chars
                #        comment brown i ;     for comments
                #        number purple ;       for literal numbers
                #        preproc darkblue b ;  for preproc directives (e.g. 
                # #include, import)
                #        symbol darkred ;      for simbols (e.g. <, >, +)
                #        function black b;     for function calls and 
                # declarations
                #        cbracket red;         for block brackets (e.g. {, })
                # much nicer than silvercity and it does more langs
                # have to play w/the tags.j2h file for colors
                # not sure about the css option yet from htmlize but the file 
                # will be huge!
                # 
                # 
                # ? -f html  --doc --tags-file="c:\UTIL\DLL\xtags.j2h" %N
                # -v source-highlight 1.11 Trying with... tags.j2h 
                # c:/progra~1/Src-Highlite/share/source-highlight/tags.j2h 
                # C:\UTIL/share/source-highlight/tags.j2h No tags.j2h file, 
                # using defaults ...
                # damm,. what ugly default colors source-highlite has
                # putting tags in $HOME and why don't they check there?
                # 
                # java and javascript are not equilevent
                # there is no jscript or javascript in Leo yet.
                # its turning into more and more of a rats nest.
                # 
                #@-at
                #@@c
                
                if lang in [  #leo may not have all of these yet
                       'csharp', 'c', 'c++', 'cpp',
                        'css', 
                      'htm', 'html', #
                        'perlpod', 'perl', 
                        'ruby',
                        'sql',
                        'xml',
                        'xslt',
                        'yaml',
                        'elisp', 'php', 'java', 'rapidq', 'actionscript', 'css',
                    ]:
                    if lang in ['htm', 'html', 
                                    'actionscript', 'css', ]: lang = 'sml'
                
                    elif lang in ['java', 'rapidq',]: lang = 'javascript'
                    elif lang in ['jscript', 'javascript',]: lang = 'javascript'
                    elif lang in ['c', 'c++', 'cpp']: lang = 'cpp'
                    elif lang in ['php', ]: lang = 'php3'
                    elif lang in ['perlpod', 'perl',]: lang = 'perl'
                    elif lang in ['elisp',]: lang = 'perl'
                
                
                    #should be try
                    # wont complain if it isnt the right extension
                    g.es('writeing tmpname', tmpfile )
                    fo = file(tmpfile, 'w')
                    fo.writelines(source + EOLN)
                    fo.close()
                    
                    #little foggy here, options for src-hilite might be different
                    #than any other unknown and so should use hiliter options
                    #but I have no other hiliter in mind yet, so punting.
                    cmd = g.app.dynaMvar.htmlize_hiliter
                
                    #dont want it to create the file, send to stdout
                    #
                    #
                    #have to account for quoted path with space in them and no comma?
                    params = cmd.split(',')
                
                    if len(params) < 2:  #must be source_hilite
                        params = ' -s %s -f html -T %s %s --tags-file=%s --no-doc -i %s'%(
                           lang, sanitize_(titl),
                           g.choose(g.app.dynaMvar.du_test_verbose != 0, '-v', ' '), #!''
                            g.os_path_join(g.app.homeDir,'tags.j2h'),
                            tmpfile,)  
                    else:
                        #not the best way to handle shell commands, but ok YMMV.
                        params = ' '.join(params[1:])
                
                    g.es('running %s \n'% g.app.dynaMvar.htmlize_hiliter, cmd + params )
                    out, err = runcmd(cmd + params )
                
                else:
                    print plainout(source)
                #@-node:ekr.20050328091952.74:<< src-highlite >>
                #@nl

            elif hasattr(g.app.dynaMvar, 'htmlize_hiliter') and\
                  g.app.dynaMvar.htmlize_hiliter == 'silvercity':
                #@                << silvercity >>
                #@+node:ekr.20050328091952.75:<< silvercity >>
                #@+at
                # have to do a multitute of things for this to work
                # sc cant read script so have to write tmpfile
                # can view or redirect and use our viewer caller
                # 
                # default colors in silvercity.css need to be matched to Leo
                #@-at
                #@@c
                
                if lang in [  #leo may not have all of these yet
                       'csharp', 'c', 'c++', 'cpp', # (C and C++)
                        'css', # (Cascading Style Sheets)
                      'htm', 'html', # HTML/PHP w/ JavaScript, VBScript, Python
                        'perlpod', 'perl', # (Perl)
                        #'python', # (Python)
                        'ruby', # (Ruby)
                        'smart_python', # (Python with styled strings)
                        'sql', # (SQL)
                        'xml', # (XML)
                        'xslt', # (XSLT)
                        'yaml', # (YAML)
                        #basic & java? missing. might send java as c?
                        'elisp', 'php', 'java', 'rapidq', 'actionscript', 'css',
                    ]:
                    if lang in ['htm', 'html', 'php', 'java', 'rapidq',
                                    'actionscript', 'css', ]: lang = 'html'
                    elif lang in ['c', 'c++', 'cpp']: lang = 'cpp'
                    elif lang in ['perlpod', 'perl',]: lang = 'perl'
                    elif lang in ['elisp',]: lang = 'perl'
                
                
                    #dont want it to create the file, send to stdin
                    #should btry
                    # won't complain if it isn't the right extension
                    g.es('writeing tmpname', tmpfile )
                    fo = file(tmpfile, 'w')
                    fo.writelines(source + "%s"%EOLN)
                    fo.close()
                    
                    cmd = g.os_path_join(pypath, 'Scripts', 'source2html.py')
                
                    #dont want it to create the file, send to stdout
                    #" --view %N  %N.html"
                    # --css=file copy silver_city.css where the filename will be
                    # source2html.py --list-generators
                    params = ' --generator=%s --title=%s --css=silver_city.css %s'%(
                       lang, sanitize_(titl), tmpfile,)  
                
                    if not g.os_path_exists(cmd):
                        g.es('cant find source2html install silvercity')
                        print 'cant find source2html from silvercity'
                
                    else:
                
                        g.es('running silvercity \n', py + cmd + params )
                        out, err = runcmd(py + cmd + params )
                        silvercity = 'FIXME'
                else:
                    print plainout(source)
                
                #@-node:ekr.20050328091952.75:<< silvercity >>
                #@nl

            else:
                sys.stdout.write(outheader())
                out = plainout(source)
        
            if out:
                for x in out.splitlines():
                        print x
            if err and g.app.dynaMvar.du_test_verbose: 
                g.es(' ** '.join(err.splitlines()), color='tomato')

        #getmetrics(source)
        #tack on fileinfo as a comment
        #generate linkable index of keywords

        if silvercity is None: #fix when can get it to do fragments
            sys.stdout.write(outfooter())
    
        sys.stdout.close()
        sys.stdout = _sysstdsav #missing from org cgi.
    
        # load HTML page into browser, py2.2?
        if 0: 
            #might want this if to use other than default browser
            if os.name == "nt":
                os.system(r'explorer %s'%hopts['filename'])
            else:
                os.system("netscape %s &"%hopts['filename'])
        elif 1:
            import webbrowser
            webbrowser.open(hopts['filename'], new= 1) #

    except ValueError:
        g.es('no @path set, unsupported lang or empty script', 
                color= 'tomato')
        g.es(lang, p.headString())

    except Exception:
        g.es('htmlize malfunction?', color= 'tomato')
        g.es_exception(full= True)

    sys.stdout = _sysstdsav #twice is nice
#@nonl
#@-node:ekr.20050328091952.62: htmlize
#@+node:ekr.20050328091952.76:restoreStd

def dynaZ_restoreStd(c):
    """every now and again run this if prints are blocked"""
    import leoGlobals as g
    print "stdout isRedirected:", g.stdOutIsRedirected()
    print "stderr isRedirected:", g.stdErrIsRedirected()
    g.redirectStderr()
    g.redirectStdout()

    g.restoreStdout()
    g.restoreStderr()
if __name__ != 'dyna_menu':
    try:
        __version__
    except NameError:  
        dynaZ_restoreStd(0)
#@nonl
#@-node:ekr.20050328091952.76:restoreStd
#@+node:ekr.20050328091952.77:del first n char

def dynaZ_del_first_char(c):
    """del first char in the line
    abstracted everything get/insert related to dynaput
    del_2nd_char would occasionally be usefuil

    applying the logical reverse, what about an add first char?
    might use that to comment out a section of code
    always remembering to have something selected & copyed could get to be a pain
    decided best to have that in another macro, using dynaplayer
    could defl 2 at a time, but make one at a time changes 
    so you could undo one if you only want one. usually its 4 for me anyway.

    """
    newSel = dynaput(c, [])
    if not newSel: return
    
    try:
        newSel = str(newSel)
    except (UnicodeEncodeError, Exception):
        g.es_exception(full= False)


    sx = []
    for x in newSel.splitlines():
        sx.append(x[1:] + EOLN )

    dynaput(c, sx)
#@-node:ekr.20050328091952.77:del first n char
#@-node:ekr.20050328091952.52:pre/post macros
#@-node:ekr.20050328091952.5:macros
#@+node:ekr.20050328091952.78:config
#for the plugin manager using the ini
#verbose set 0 in the ini but sometimes not untill flip it
#needed getint in config
#some of these should be dyna menu items anyway in case no plugin_menu
#calling them prototypes for now. so many switches so little time
#maybe can have some to flip styles & colors for htmlize
#@+node:ekr.20050328091952.79:cmd_flipverbose

def cmd_flip_du_test_verbose(): 
    """for @test nodes
    requires change in leoTest, (added Leo4.3a2 no objections)
    you still get traceback on syntax and other errors with just dots ==1
     ==2 is verbosity in unittest @test and @suite. slightly different
     either 1 or 2 is verbose for doctest and 0 is nothing except errors reported
    
    validating config options hasn't been implimented yet either
    can I call a more general flipper for other vars too?
    can there be a cascade of flip vars in plugin_menu?
    """
    g.app.dynaMvar.du_test_verbose += 1
    # is 1 or 0? True or False not sure 2.2 even has this option too?
    #this, like debug,  should increment in a connected range 0..3
    g.app.dynaMvar.du_test_verbose = g.choose(
        g.app.dynaMvar.du_test_verbose >= 3, 0, g.app.dynaMvar.du_test_verbose)
    g.es('now is', g.app.dynaMvar.du_test_verbose)
#@nonl
#@-node:ekr.20050328091952.79:cmd_flipverbose
#@+node:ekr.20050328091952.80:cmd_flipLeo_debug

def cmd_flip_Leo_debug(): 
    """0,1,2,3 for Leo debug switch
    careful, 3 istarts pdb which has some unpredictable results
    maybe it should start rpdb or the debugger of your choice
    and in a seperate thread and in its own window.
    """
    g.app.debugSwitch += 1
    g.app.debugSwitch = g.choose(
        g.app.debugSwitch >= 4, 0, g.app.debugSwitch)

    g.es('debugSwitch now is', g.app.debugSwitch)
    if g.app.debugSwitch >= 2: g.es('pdb is now active on errors', color='tomato')
#@nonl
#@-node:ekr.20050328091952.80:cmd_flipLeo_debug
#@+node:ekr.20050328091952.81:cmd_flipjustPyChecker

def cmd_flip_justPyChecker(): 
    """for tim1crunch makeatemp and pychecker2
    1 is don't print source after running the check
    """
    g.app.dynaMvar.justPyChecker = g.choose(
        g.app.dynaMvar.justPyChecker != 0, 0, 1)
    g.es('now is', g.app.dynaMvar.justPyChecker)
#@nonl
#@-node:ekr.20050328091952.81:cmd_flipjustPyChecker
#@+node:ekr.20050328091952.82:flip_onoff_c_gotoline
def cmd_flip_onoff_c_gotoline(): 
    """this totally violates the goto feature in executeScript
    presently broken if called from selected text.
      unselects the text and goes to the line in the full script.
    broken if error happens in another module
    and you are working in a subnode from a scriptButton
    you probably don't want to goto the top of the script.
      you might not even want or need to see the error
      by then its all too painful what the problem is
      the traceback is just a reminder it isn't fixed yet.
    this solves the one thing. 

    no one wants to see the error wrongly reported ever.
    the other thing is a problem with exec and python and tracebacks.
    compiling the script first would get you a better filename than <SCRIPT>
    but showing exec and leoCommands as part of the problem isn't helpful,
    to old and new alike. grin and bear it I guess.
    
    subsequent calls turn goto back on or off
    
    and why do I need to know Leo knows this:  
     'No ancestor @file node: using script line numbers'
    when gotolinenumber from Edit menu? (no problem if flipped off)

    no idea if c.goToLineNumber called from other scripts 
    or parts of Leo or other leos' will be adversely impacted if off.
    
    of course a config setting or option to turn off goto,
    option to turn off show error in context, would be better.
    for those vanishingly fewer and fewer times when they are wrong.
    mean time, take no prisoners. this works today.
    """

    import leoGlobals as g
    c = g.top()
    atribs = cmd_flip_onoff_c_gotoline

    if hasattr(atribs, 'flip'):
        atribs.flip = not atribs.flip
    else:
        atribs.gotolinesave = c.goToLineNumber
        atribs.flip = True

    if atribs.flip:
        def dummygotoline(n, *a, **k):
            'goto is fliped off'
            pass
        c.goToLineNumber = dummygotoline
        g.es('turning off goToLineNumber', color= 'purple')
    else:
        c.goToLineNumber = atribs.gotolinesave
        g.es('turning on goToLineNumber', color= 'purple')

#@-node:ekr.20050328091952.82:flip_onoff_c_gotoline
#@+node:ekr.20050328091952.83:cmd_SetAsDefault

def cmd_SetAsDefault(): 
    """
    set default would be harder, 
    no interest in maintaing seperate defaults.
    """
    #g.alert('no ini, check back in 5 minutes')
    #getConfiguration(rw= 'w') #force write
    g.es('no change at this time')
    
#@-node:ekr.20050328091952.83:cmd_SetAsDefault
#@+node:ekr.20050328091952.84:cmd_ShowDefaults

def cmd_ShowDefault(): 
    """
    no interest in maintaing seperate defaults.
    no need to show all the defaults actually, just user configurables
    shoud show hopts also and make a function so can have the intersection
    with the ini overriding hardwired default values. maybe next time.
    """
    g.es(g.app.dynaMvar)
#@-node:ekr.20050328091952.84:cmd_ShowDefaults
#@+node:ekr.20050328091952.85:applyConfiguration

def applyConfiguration(config):
    """plugin menu calls this after ini edit 
    and on first menu creation or first dyna click if I can swing it.
    
    True/False config saves as string? seems to work ok though
    also if non existant will be error, have to trap
    so default written in plugin can override if no attribute
    or attribute contains nonsense or whole ini or section doesn't exist.
    this addhockism has to go, 
    the ini format is 20 years old an im winging it here again.
    is it lowercasing items but not section names? what about values?
    seems to preserve case now, but decided better if dumenu doesn't
    this way lies maddness to debug otherwise. not everyone is a coder.

    another way to look at it is:
        if you don't want no errors, don't make any mistakes.
    all required options are hardwired defaulted 
    and should be ok if ini is wrong or missing
    
    """
    if not config: return
    badini = ''
    dyna = g.app.dynaMvar

    #2nd time thru it may be set some other way
    dyna.htmlize_filename = 'default'

    #should warn if no section header found?
    items = config.items('main') + config.items('htmlize')
    #g.es(items)

    for x in items:
        xl = x[0].lower()
        if xl == 'verbosity':
            dyna.du_test_verbose = x[1]

        if xl == 'justpychecker':
            dyna.justPyChecker = x[1]


        if xl == 'hiliter':
            dyna.htmlize_hiliter = x[1]
        if xl == 'filename':
            dyna.htmlize_filename = x[1]


    lx = """\
         timestring
        codefold stripcomments stripsentinals
        stripnodesents stripdirectives 
        noNAME noOP noNUMBER

        token_NUMBER      token_OP
        token_STRING      token_COMMENT
        token_NAME        token_ERRORTOKEN
        token_KEYWORD     token_TEXT
        token_LeoDir      token_LeoSen
        token_bg""".replace('\n',' ').split()

    #g.es(lx)
    for xini in [xl.strip().lower() for xl in lx]:
        x = 'bad'

        try:
            #this actually needs another step to be caseinsensitive
            #but well leave it to FIXME later as above was done
            x = config.get('htmlize', xini).lower()

        except (ConfigParser.NoOptionError, ConfigParser.NoSectionError, Exception):
            #g.trace('not found', xini, x)
            badini += '.'
            continue

        #no attribute or sometimes default means let dyna handle it
        if not x or x == 'bad': 
            #g.trace('not xImped', xini, x)
            badini += '.'
            continue

        #getboolean might work for these few
        elif ('%s'%(x, )).strip().lower() in ('true', '1', 'on', 'n', 't'):
            xval = True
        elif ('%s'%(x, )).strip().lower() in ('false', '0', 'off', 'f', ''): 
            xval = False

        elif xini.startswith('token_') or\
             xini in ('timestring', ): 
            #maybe validate is proper hex and has # or good color name
            #or whatever the user wants the user gets in this case
            xval = x

        else: 
            #g.trace('not Imped', xini, x)
            badini += '.'
            continue

        setattr(dyna, 'htmlize_'+xini, xval)

    
    #might want to write the unnamed options commented out?
    #g.es(config.items('htmlize'))

    #is NDEBUGMSG a global?
    #g.es('current dyna configized w/%s defaulted values'% len(badini))
    #cmd_ShowDefault()
#@nonl
#@-node:ekr.20050328091952.85:applyConfiguration
#@+node:ekr.20050328091952.86:getConfiguration
def getConfiguration(): 
    """Return the config object
    should this look in homeDir first then plugins?   
    check __file__ works in py2.2 and under test.leo of plugin 

Default values can be specified by passing them into the ConfigParser constructor as a dictionary. Additional defaults may be passed into the get() method which will override all others. 



    """ 

    #if ini doesn't exist, should we create it?

    fileName = g.os_path_join(g.app.loadDir,"..","plugins",
            g.os_path_split(__file__)[1][:-3]+".ini") 
    #g.trace(fileName)
    config = ConfigParser.ConfigParser() 
    config.read(fileName) 
    return config 
#@-node:ekr.20050328091952.86:getConfiguration
#@-node:ekr.20050328091952.78:config
#@+node:ekr.20050328091952.87:load_menu

#no user code besides cascade names tuple

def load_menu(tag, keywords ):
    global dynaMvar

    c = keywords.get("c") #, 'new_c')  #chg incase there is no c
    cf = c.frame
    if NDebug:
        g.es('entering load_menu')

    if dynaMvar is None: #was or was changed to c
        #dare I assert g.top() == c  on the first leo is no top().frame
        dynaMvar = g.app.dynaMvar = init_dyna(c)
        #problem, do I try again later or fail?
        if NDebug:
            g.es('load_ dynaMvar was None')
        
        #this will have been set before 2nd leo can be opened
        #set to default even if no ini can be read and not used otherwise
        #all dyna_menus share the same state, read/save the same ini
        #and I have not done anything with @settings but plan to soon
        #maybe pospone ini read further, till first time dyna is clicked?
        if not hasattr(g.app.dynaMvar, 'htmlize_filename'):
            applyConfiguration(getConfiguration())

    #@    << togprpa >>
    #@+node:ekr.20050328091952.88:<< togprpa >>
    def togprpa(cf= cf, *a):
        """called from the menu to set status and Flag
    
        woops, the least obvious appears to work. 
        was doing if print set paste etc
        now is if print set print
        """
        def doprpa(*a):
            if 'print' == dynaMvar.dynapasteFlag.get():
                dynaMvar.dynapasteFlag.set('print') 
            elif 'paste' == dynaMvar.dynapasteFlag.get():
                dynaMvar.dynapasteFlag.set('paste') 
            elif 'doc' == dynaMvar.dynapasteFlag.get():
                dynaMvar.dynapasteFlag.set('doc') 
    
            cf.clearStatusLine()
            cf.putStatusLine("dynamenu " + dynaMvar.dynapasteFlag.get())
    
        return doprpa
    #@nonl
    #@-node:ekr.20050328091952.88:<< togprpa >>
    #@nl
    casnamtup = (
        'infos', #B  htmlize, restoreST, clipdtef, linenumber
        'mod text',   #M 
        'codeing', #S

        'pre/post', #A:y
        'zzzzz', #never gets here dont use past Z as a sentinal
    )

    table = []  #first table is built then some items use .add
    nu = dynaMvar.dynasMenu = c.frame.menu.createNewMenu("d&yna", "top")


    #eventually build some entries outside submenus
    #maybe the first and last letter save for this reason A:z
    #then work from copy lst with those items subtracted
    lst = dynaMvar.dynadeflst[:]
    lst.reverse() #makes no sense but we do it anyway.

    #you change the macro order you assume full responsinility
    #know B_clipdtef is the first one add B_linenumber now
    #this could be fragile if you use less macros than are standard
    try:
        table.append(
            (lst[-4][6:], None, lambda c= c, f= globals()[lst[-4]]: f(c) ))
    except Exception:
        pass

    #@    << add items >>
    #@+node:ekr.20050328091952.89:<< add items >>
    #there better be at least one macro in lst and one cas entry
    a = 0
    ch = dynaMvar.dynadeflst[0][4]
    subtable = []
    sub = None
    #dynaMvar.dynadeflst.append('dynaz_') #add break sentinal
    
    #the way Leo menu add works is 
    #A. similar to Tk, B. incomprehensable C. it just "works"
    #and why is submenu text  smaller? and how can't I change it.
    #submenus seem to get sorted? forced to the top at some point.
    
    #add items till the 5th char changes, then get next subname
    #does not always degrade gracefully if you go out of bounds
    for s in dynaMvar.dynadeflst:
    
        if s[4] != ch or sub is None:
            #g.es('a=', a, 's=', s, `subtable`, color= 'orange')
            if sub:
                c.frame.menu.createMenuEntries(sub, subtable)
                subtable = []
                a += 1 #yada yada test end of cas
                ch = s[4]
            if s[4] >= 'Z': break
            sub = c.frame.menu.createNewMenu(casnamtup[a], "dyna") #nu
    
        subtable.append(
            (s[6:], None, lambda c= c, f= globals()[s]: f(c) ))
    
        lst.pop() #quick if not efficent
    
    #append z entries, see above and below above
    for s in lst:
        table.append(
            (s[6:], None, lambda c= c, f= globals()[s]: f(c) ))
    
    
    #@-node:ekr.20050328091952.89:<< add items >>
    #@nl

    #@    << .add_exSb >>
    #@+node:ekr.20050328091952.90:<< .add_exSb >>
    #exS in its own plugin, can I trust this to work? can you? 
    #would have to look into hasattr(sys.modules, 'exSButton') & import
    #is it because e is initilized after d?
    #chg to callback to delay the init and substutute the callback
    #actually would need to get the menu nu and change it there
    #could persist it in the def dec nux= nu
    def ecall(*a, **k):
        try:
            #globals()['exSButton'] ng
            sys.modules['exSButton'] #it loaded yet?
            #ecall = lambda exS = sys.modules['exSButton']: exS.add_exSb('dynaExS1', 'from dyna') replace function ng
    
            sys.modules['exSButton'].add_exSb('dynaExS1', 'from dyna')
            g.es(' exSButton yes!')
        except KeyError: #pass
            #g.es_exception()
            g.es(' exSButton no!')
    
    table.append(("add exSButton", None,  #^E or is it shifted too?
                   ecall) )
    #@nonl
    #@-node:ekr.20050328091952.90:<< .add_exSb >>
    #@nl
    #nu.add_separator()  #gets out of synch w/table here
    table.append(('-', None, None))

    c.frame.menu.createMenuEntries(nu, table)

    dynaMvar.dynapasteFlag.set('print')
    
    nu.add_radiobutton(label= 'print',
            variable = dynaMvar.dynapasteFlag,
            command= togprpa(cf= cf) )
    nu.add_radiobutton(label= 'paste',
            variable = dynaMvar.dynapasteFlag,
            command= togprpa(cf= cf) )
    nu.add_radiobutton(label= 'doc',
            variable = dynaMvar.dynapasteFlag,
            command= togprpa(cf= cf) )
    #@    << show clip >>
    #@+node:ekr.20050328091952.91:<< show clip >>
    #show whats in the clipboard, replace clipboard with left side of pair
    #this isnt dynamically updated each menu invocation in plugin
    #nu.add_command(label= "Clip=%r"%(
    #            g.app.gui.getTextFromClipboard()[:6],), )
    
    dynai = Tk.Menu(None, tearoff= 0, takefocus= 0 )
    for x in  '\' Sq, " Dq, \'\'\' Sq3, """ Dq3, : file, | !file, \\\\ Dbs, ( ), { }, [  ], try /ex, if /else, >>> /...'.split(', '):
            dynai.add_command(label= x, 
              command= lambda x= x, f= g.app.gui.replaceClipboardWith: 
              f(x.split()[0]) ) 
    
    nu.add_cascade(menu= dynai, label= 'choice' )
    #@nonl
    #@-node:ekr.20050328091952.91:<< show clip >>
    #@nl
#@nonl
#@-node:ekr.20050328091952.87:load_menu
#@+node:ekr.20050328091952.92:init
def init():
    """this is one less than one too many ok's.
    various macros will fail with out some various non standard modules.
    but they trap ImportError and fall back if possible.

    """
    ok = Tk and dynacom and not g.app.unitTesting

    if ok:
        if g.app.gui is None:
            g.app.createTkGui(__file__ )
    
        ok = g.app.gui.guiName() == "tkinter"
    
        if ok:
            import leoPlugins
    
            if NDebug:
                g.es("dyna_menu", color="gold2")
    
            leoPlugins.registerHandler("create-optional-menus", load_menu)
    
            #stealing code from timestamp plugin
            # lp.registerHandler("command1", timestamp)
            #isnt there a finer grained control than command1?
            #seems like this would slow things down conciderable
            #probably because wanted to catch tangle too
            # save1 should be less overhead
            leoPlugins.registerHandler("save1", timestamp)
            
    
            #plugin_signon reloads the plugin, can forgo that
            #g.plugin_signon(__name__)  # + __version__

    return ok
#@nonl
#@-node:ekr.20050328091952.92:init
#@-others

#you can use a macro in other ways
def timestamp(tag=None, keywords=None):
    """stolen from the timestamp plugin
    chged hook from command1 to save1
    how to hook write @file so can timestamp that?
    
    add nag you if changed and not saved over 5 minutes
    add nag if typing after sunset over 3 hours, yea right~
    """
    cmd = keywords.get('label', 'save')

    if cmd.startswith("save") or cmd.startswith("tangle"):
        dynaB_Clip_dtef(None, ret= 'p')  #just print
        c = keywords.get('c', g.top())
        g.es('at node:' + (c.currentVnode().headString().strip())[:128])




#@@language python
#@@color
#@-node:ekr.20050328091952.2:@thin dyna_menu.py
#@-leo
