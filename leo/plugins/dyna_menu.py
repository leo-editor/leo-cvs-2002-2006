#@+leo-ver=4-thin
#@+node:ekr.20040916153817.1:@thin dyna_menu.py
#be sure and add dyna_menu.py to pluginsManager.txt

"""plugin creates a dyna menu of macro items.
 Alt+y the dyna menu accelerator key.   
 every time you save the leo one of the macros prints a timestamp.
 macros perform any actions you could have with execute script,
 with the added bonus, they work on the selected text or body text.
 they work as well from the dynatester node or dynabutton, insuring
 when they are included in the plugin, minimal time is lost debugging.

 add exS will re-install exS button on the toolbar.
 
you also need dynacommon.py in the plugins directory
and edit the paths in dynacommon.py to suit your system.

do post a bug report or feature request
on my comment page from:
 http://rclick.netfirms.com/rCpython.htm
or sourceforge forum:
<http://sourceforge.net/forum/forum.php?thread_id=1070770&forum_id=10226>

temporary latest version page.
http://rclick.netfirms.com/dyna_menu.py.html

sorry no proper changelog, expect constant maintance and additions

"""   
__version__ = '0.0137'  #r04909p04:58
#@<< initilize >>
#@+node:ekr.20040916153817.2:<< initilize >>

#from __future__ import generators + enumerate for less than py2.3
import leoPlugins
import leoGlobals as g

try: import Tkinter as Tk
except: Tk = None

#at this point in Leo, code from plugins isn't importable. later it is.
import sys
if g.os_path_join(g.app.loadDir, "..", "plugins") not in sys.path:
    sys.path.append(g.os_path_join(g.app.loadDir, "..", "plugins"))
try: 
    from dynacommon import *  #should use importfile?
    #reload(dynacommon) #if modify common
except ImportError: 
    #no gui maybe print better here? should guard the error too?
    g.es('you have to copy dynacommon.py to plugins')

"""t04511p12:30:22  
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
 
 another anomaly, 
 for the menu you left click, on the button you right click.
 I thought about changing the button to a menu.
 I thought about not changing to a menu.
 usually I forget to think about it.
 

 some sample macros included. look over and see if they 
 might do something useful or can be modified to do so.
 most of them print to log or the text transformed
 or paste over selected text 
  if the print/paste/doc item in the menu is toggled.
 if no text is selected, most will attempt to use the current body text.
 in a few cases the body text is filtered to comment out
  @directives. @other and namedsection nodes will be included
  see makatemp, tim1crunch, calls to fixbody get all the body.
  if you just want the current node, use selectall.

 Clip_dtef      shows how to insert into clipboard
                proof of concept called on every save to print time

 clipappend append selected to Clipboard

 c2py    the fantastic c2py script. translates c/c++ into python.
 	    works as well on java and javascript snippits or even python
     though be aware it ruthlessly removes braces so d = {} becomes d =
     you'll still have to make it more pythonic but it does alot.
    c2py doesn't generate an undo event so there is no turning back.
    might be a good idea to change smaller bits of code at a time.
    might be wise to have a copy of the node in the origioinal language.
    before anything there is an ok/cancel button that pops up 
    to give you a chance to quit without change.
    c2py will tabify and change in place the tree and its subnodes.
    prior to c2py and import into Leo a good indent will help.
    be sure to attribute any snipits of code you convert and use.
    I doubt c2py author intends this utility to make plaguisim easy.

 DQ3             adds text from the copybuffer around the text
                 if you have ( or other pair
                 then the matching pair will end the text
                 see the __doc__ and source for complete info.

 dyna_backslash  transforms paths from & to several forms
        like change forward slash to backslash, c:\temp to file:///c|temp

 dupe       duplicates the selected text. 
            good for those one line copies when something
            else is in the copy buffer. select to paste first.

 del first n char  does delete the first char.

 dumpbody     the standard hex dump of selected text or body

 geturls    extract urls from selected text, uniqued, sorted.
 
 everycase  take the selected word or sentance and output 
            in a variety of case. and to AND and And aND etc

 flipper         toggle selected recognized text, like True to False

 regexTX   turn a list of space or coma seperated words into a dict
           primarialy for Tk config and pack statements refactoring

 makatemp    run selected text or body thru reindent script
             then call pychecker and optionally pylint on the file.
             note: pychecker & pylint will import and therfore execute.

 pycheck2  doesn't import or compile the file first, like tim1crunch
            can be concidered safe to examine untrusted code.
            its in the pychecker dist, you have to install it by hand.
            
 tim_one_crunch  an old program posted on a forum by tim one,
                to report single use variables. good for debugging


 linenumber  print out selected text or body as Leo sees it
             adding linenumbers or using an int in the copy buffer
             to show a few lines before and after the target.

 sfdots add or remove dots from code posted on sourceforge forum

 swaper          swaps the selected text with copybuffer contents

 wraper uses textwrapper included in python 2.3
        wrap paragraph to the length of the first line.

 restoreSTD sometimes it seems the redirect to log gets confused
           this seems to only happen with callevaluator which
          isnt in the plugin by default unless I forgot to remove it.
T
 htmlize  curent node + subnodes. no selected text for now
  produce file currently c:\windows\temp\python.html, you edit this.
  colorized html of language python nodes 
  @language css html perl c  other sent to silvercity if installed.
  silvercity may not fully support java yet, please recomend something.
  
  du_test-str calls leoTest for @test and @suite nodes for unittests
   otherwise runs doctest on the node and subnodes, a few quirks
   did solve the temp file creation avoidance 
   so no mymod.py, pyc pyo will litter the current dir!

  pydent, takes a node w/ w/o dots runs thru syntax check twice
       evaluator and reindent and creates an import to @file
       replace evaluator with Leo's prettyprint if no evaluator

  disa  dissasembles the selected text code or node & subnodes.

  nflatten  recursive list of headlines in a node and its subnodes.

  
still to solve the evaluator code, whaere is it?
 maybe will default to Leo's new pretty printer if ImportError
 and when you run it the stdout to log is confused. not sure why.
 running macro restoreStd fixes it.
 
 there are other macros in the macrostore node,
 and the macros node of dynaclickbutton.
 you can copy or clone any which way you want to include the 
 items you require to appear in the dyna menu or dynabutton rclick.


todo, single _doc__ output for any macro clicked on while doc is toggled
possibly toggle error reporting, which is turned on full in dynabutton.
add unit testing to the dynatester idea so plugin can be unittested
each macro have a few go/nogo tests at minimum.
although doctest would be preferred in most cases ,
and unittest can do doctests since 2.3
maybe I can understand how to do that without writeing a file to import.


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



this version >.0420 breaks with 4.1 in a few places
related to positions and scripting support.
you can still grab the .032 version which works with Leo4.1
lightly tested with py2.2 or Leo4.2a1,2,3,4 b1 from cvs

v.0420+
tested in Leo 4.2 Beta3+  and Python 2.3.3 win9x

should not be a problem anywhere else.
but don't quote me on that.

for a productivity boost on windows,
http://www.geoshell.com replacement explorer shell
mulitiple window views, floating toolbars with many plugins
opensource, source available for plugins.
(not connected in any way, its just amazing)

see firefox browser for an enlightning approach to user options
based on the Netscape user.js and chrome.css and adds themes.

e
"""

#@-node:ekr.20040916153817.2:<< initilize >>
#@nl
NDebug = True and False
#@+others
#@+node:ekr.20040916153817.3:macros
#@+at
# there may be some refrences to macros of their old names lurking
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
# you also need dynacommon.py in the plugins directory
# 
#@-at
#@+node:ekr.20040916153817.4:info macros
#@+node:ekr.20040916153817.5: Clip_dtef

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
        Leoconfigformat = '%m/%d/%Y %H:%M.%S'
        dt = time.strftime(Leoconfigformat) 


    if 'p' in ret: g.es('\n%s '%(dt,) )
    if 'c' in ret: g.app.gui.replaceClipboardWith(dt)
    #ret = r necessary, if dont specify it clips & prints by default
    if 'r' in ret: return dt  

#e
#@nonl
#@-node:ekr.20040916153817.5: Clip_dtef
#@+node:ekr.20040916153817.6:linenumber

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
    #@+node:ekr.20040916153817.7:<< more debugging tips >>
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
    #@-node:ekr.20040916153817.7:<< more debugging tips >>
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

        g.es('%- 3d '%(i,), newline= false, color= colr)

        g.es('%s'%(x,))
    g.es('There are %s lines in ? nodes'%(
            len(datalines),), color= 'turquoise4')

#
#@nonl
#@-node:ekr.20040916153817.6:linenumber
#@+node:ekr.20040916153817.8:nflatten

def dynaB_nflatten(c= None, current = None, indent= '  '):
    """like flatten but in macro so can
    print/paste or copy to buffer eventually. now out to log.
    should limit the recursion to less than the normal limit
    isn't following the more format of +-
    cant add - to indent due to the way its reusing indent...
    """    
    import leoGlobals as g
    if c is None:
        c = g.top()
    if current is None:
        current = c.currentPosition()
        g.es("%s"% deangle(current.headString()[:50]), color="purple")

    for p in current.children_iter():
        g.es(indent + deangle(p.headString()[:50]))
        if p.hasChildren():
            dynaB_nflatten(c, p, indent + '  ')
                
def deangle(s):
    """
    >>> deangle( '<%s'%'< whatever >>')
    '<+< whatever >>'
    >>> deangle('< whatever >>')
    '< whatever >>'
    """
    if s.startswith('<<') and s.endswith('>'+'>'):
        return '<+' + s[1:]
    return s

#dynaB_nflatten()
#print dir('')
#@+at
# from the docs
# The p.siblings_iter returns a list of all siblings of position p.
# The p.following_siblings_iter returns a list of all siblings that follow 
# position p
# added recursion for subnodes
#@-at
#@-node:ekr.20040916153817.8:nflatten
#@-node:ekr.20040916153817.4:info macros
#@+node:ekr.20040916153817.9:text macros
#@+node:ekr.20040916153817.10:+dyna_backslash

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
#@-node:ekr.20040916153817.10:+dyna_backslash
#@+node:ekr.20040916153817.11:geturls

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
        g.es_exception(full = False)
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
#@-node:ekr.20040916153817.11:geturls
#@+node:ekr.20040916153817.12:swaper

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
#@-node:ekr.20040916153817.12:swaper
#@+node:ekr.20040916153817.13:flipper

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
#@-node:ekr.20040916153817.13:flipper
#@+node:ekr.20040916153817.14:dupe

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
    #c.frame.body.see() 
    #how to unselect?
    #c.frame.bodyCtrl.unsel() is none
    #c.frame.bodyCtrl.event_generate('<Return>')

    dynaput(c, sx)
#@-node:ekr.20040916153817.14:dupe
#@+node:ekr.20040916153817.15:clipappend

def dynaM_clipappend(c):
    '''append selected to Clipboard
    
clipboard_append(s)

    '''
    newSel = dynaput(c, [])
    if not newSel: return

    Clip = g.app.gui.getTextFromClipboard()
    Clip += newSel
    g.app.gui.replaceClipboardWith(Clip)
#@-node:ekr.20040916153817.15:clipappend
#@+node:ekr.20040916153817.16:everycase

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
        s.capitalize(), '\n',
        
        s.swapcase(), '  ',
        s.title(), '  ',
        s.title().swapcase(), '\n',

        "'%s'"%s, '  ',
        "(%s)"%s, '  ',
        "('%s')"%s.lower(), '\n',
         ]:
        sx.append(x)

    #here wordwrap or otherwise format and relist it.
    
    if sx:        
        dynaput(c, sx)
#@-node:ekr.20040916153817.16:everycase
#@+node:ekr.20040916153817.17:dyna_regexTk

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

        if x in ' ,\n':
            sx.append('\n')
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

        if x in ' ,\n': 
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


    
#@-node:ekr.20040916153817.17:dyna_regexTk
#@+node:ekr.20040916153817.18:wraper

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
#@-node:ekr.20040916153817.18:wraper
#@+node:ekr.20040916153817.19:+rsortnumb

def dynaM_rsortnumb(c):
    """caller to dyna_sortnumb(c, d= 1 )
    the reverse list will be called before output there
    """
    dynaM_sortnumb.direction = 1
    dynaM_sortnumb(c)

#@-node:ekr.20040916153817.19:+rsortnumb
#@+node:ekr.20040916153817.20:+sortnumb

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
        multiline = '\n'
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
#@-node:ekr.20040916153817.20:+sortnumb
#@-node:ekr.20040916153817.9:text macros
#@+node:ekr.20040916153817.21:codeing macros
#@+node:ekr.20040916153817.22:pydent

#@<< checkFileSyntax >>
#@+node:ekr.20040916153817.23:<< checkFileSyntax >>
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
        compiler.parse(s + '\n')  #,"<string>" parse(buf, mode='exec')
    except SyntaxError:
        g.es("Syntax error in: %s" % fileName, color= "blue")
        g.es_exception(full= False, color= "orangered")
        return True  #raise

    return False
#@nonl
#@-node:ekr.20040916153817.23:<< checkFileSyntax >>
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
    #dyna_dir = g.os_path_join(g.app.loadDir,"..","plugins")
    #dynac = g.importFromPath("dynacommon",dyna_dir,verbose= True)
    #if not dynac:
    #    s = "Can not import dyna from %s" % dyna_dir
    #    g.es(s, color="blue")
    #could import common too? except as macro that doesnt work...
    #common pulled in by dyna already
    #as script this works as macro is not required
    #can I do dy = None? when as macro or something more compliated.
    import dyna_menu as dy
    select = g.app.gui.setTextSelection
    overwrite = True
    
    #print dir(dyna_menu)
    #print dynac.tmpfile
    #print dy.tmpfile
    start = dy.dynaB_Clip_dtef(None, ret='rp')

    if not c: c = g.top()
    p = c.currentPosition()

    #have to remember to run sfdots first is not from sf
    
    #dy.yesno('', '', 'do dodots?')
    #need to jusst only dodots if there are dots., needs a force flag...
    #maybe they should return some status of what they did.
    #sfdots, paste, stripsentinals, nodotreturn, returned

    if overwrite: 
        #enable to overwrite else will print to log
        #its currently global for all leo windows and scripts
        dy.dynaMvar.dynapasteFlag.set('paste')
        select(p.c.frame.bodyCtrl, '0.0', 'end')
        dy.dynaS_sfdots(p.c, nodotreturn= True)


    #getsctipy now and check syntax... before/after evaluator
    #what about the undo? can I roll that back too?
    #it seems to have inserted NOP 51 before and after in the body!
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

    #might still have to remove a few sentinal lines start & end
    #can this return a sucess or fail? and the maybe the node pointer
    c.importCommands.importFilesCommand([dy.tmpfile], '@file')
    
    #p.selectVnode('after') or something...
    #if headline == ('@file ' + dy.tmpfile):
    #    p.setHeadline('@file some.py')
    #   move before, then select node after, selectall & delete

    dy.dynaMvar.dynapasteFlag.set('print')
    g.es('st:%s\n sp:%s\n may have to wait \nand click to see the new node'%(
        start, dy.dynaB_Clip_dtef(None, ret='r')) )

    #should select child and move left. what if it failed?

#need an if exS because this gets run from doctest
#dynaS_pydent(None)

#@+at
# r04812p03:27:01 needs dyna obviously will be its own macro soon
# the missing piece was the import from file syntax
# from the URLoader plugin the other day. saves me looking it up.
# for plugins misses rearanging
# version
# for not plugins not from sf would forgo the sfdots step
# for upload want to get into script, remove sentinals then sfdots
# so sfdots needs to be callable with a string and on option here
# but it does work much slicker than doing it by hand!
# have to work on trapping if there was a syntax error
# that would stop further processing.
# or would suggest where the error was and continue import? dangerous
# 
# does the new syntax check return T/F on syntax error
#  that could save a problem later on...
#  another common problem is property w/o subclassing object
# might patch in fule sybtax check akthough by then reubdebt wiill catch ut
# and there will be a few steps to undo if its wrong
# added a few vars to sfdodots to bail instead of do the opposit if nodots
# now it strips sentinals which might not be good for #@count #@repeat
# one weird experiance the syntax check seemed to insert Nop51's
# around the syntax error. added some simmple doctest
# need to get wraps around everything to return T/F on Fail/Ok or p|c
# just make it a macro
# 
#@-at
#@-node:ekr.20040916153817.22:pydent
#@+node:ekr.20040916153817.24:disa

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

    #need a generic sentinal stripper again, does Leo have one?
    #should fixbody stripping sentinals per a sentstrip=True?
    newSel = sentstrip(newSel)

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


def sentstrip(s):
    l = []
    for x in s.splitlines():
        if x.lstrip().startswith('#@'): continue
        l.append(x)
    return '\n'.join(l)


#dynaS_pydisa()
#@nonl
#@-node:ekr.20040916153817.24:disa
#@+node:ekr.20040916153817.25:changeleoGlobal

def dynaS_changeleoGlobal(c):
    '''converted to dyna to work on the current node
    of course including every macro in the plugin can get to be annoying. 
    have to dev a module to load on demand sub functions like this
  found an older script, updateing it not to hardwire whats in globals
  unfortunatly its using positions?

  idea from,    
    By: Edward K. Ream - edream
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
    #@+node:ekr.20040916153817.26:getgnames
    
    
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
    #@-node:ekr.20040916153817.26:getgnames
    #@+node:ekr.20040916153817.27:subtree_iter
    
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
    #@-node:ekr.20040916153817.27:subtree_iter
    #@+node:ekr.20040916153817.28:moveToNext
    
    def dynamoveToNext(p):
        
        """Move a position to its next sibling."""
        
        #p.v = p.v and p.v._next
        p = p and p.next()
        
        return p
    #@-node:ekr.20040916153817.28:moveToNext
    #@+node:ekr.20040916153817.29:prependNamesInTree
    
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
                        #@+node:ekr.20040916153817.30:<< look for name followed by '(' >>
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
                        #@-node:ekr.20040916153817.30:<< look for name followed by '(' >>
                        #@nl
    
                #assume s is the word, wont catch app() anymore?
                if s in chgdict:
                    s = chgdct[s]  #True for true etc
                    count += 1    #why thi is +=
                if count and replace:
                    if 1:
                        #@                    << print before and after >>
                        #@+node:ekr.20040916153817.31:<< print before and after >>
                        g.es("-"*10,count, p.headString())
                        g.es("before...")
                        g.es(p.bodyString())
                        #g.es("-"*10, "after...")
                        #g.es(s)
                        #@nonl
                        #@-node:ekr.20040916153817.31:<< print before and after >>
                        #@nl
                    p.setBodyStringOrPane(s)
                    p.setDirty()
            g.es("%3d %s"%(count, p.headString()))
            total += count
        c.endUpdate()
        return total
    #@nonl
    #@-node:ekr.20040916153817.29:prependNamesInTree
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
    ans = runAskYesNoCancelDialog("changeleoGlobal", 
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

#e

#@-node:ekr.20040916153817.25:changeleoGlobal
#@+node:ekr.20040916153817.32:c2py

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
    ans = runAskYesNoCancelDialog("c2py",
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
#@-node:ekr.20040916153817.32:c2py
#@+node:ekr.20040916153817.33:+dynaHexdump

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
#@-node:ekr.20040916153817.33:+dynaHexdump
#@+node:ekr.20040916153817.34:_sfdots

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
    #could you have '    ' be the eat char in a perfect world?
    
    if direction == 'UPL':
        eatchar=' '
        repchar='.'
    else:
        eatchar='.'
        repchar=' '
    

    if stripsentinals:
        l = []
        for x in data.splitlines(True):
            if x.lstrip().startswith("#@"): continue
            l.append(x)
        data = ''.join(l)

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
    #add strip sentinals re from htmlize
    dynaput(c, sx)    
    
    
    #e
#@nonl
#@-node:ekr.20040916153817.34:_sfdots
#@+node:ekr.20040916153817.35:+call_evaluator

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
#@-node:ekr.20040916153817.35:+call_evaluator
#@+node:ekr.20040916153817.36:makatemp

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
    '''
    #1no print, reindent to create tmp then pychecker on that tmp
    justPyChecker = 0


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

        if not os.path.split(tmpname)[0] in sys.path:
            sys.path.append(os.path.split(tmpname)[0] )
        
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
    fo.writelines(data + "\n#e\n")
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
        pylname = os.path.split(tmpname)[1][:-3] #cut off .py
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
#@-node:ekr.20040916153817.36:makatemp
#@+node:ekr.20040916153817.37:pycheck2

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
    justPyChecker = 1
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
    fo.writelines(data + "\n#e\n")
    fo.close()
    
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
#@-node:ekr.20040916153817.37:pycheck2
#@+node:ekr.20040916153817.38:tim_one_crunch

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
    justPyChecker = 0


    newSel = dynaput(c, [])
    data = fixbody(newSel, c)

    if not data or len(data) == 0: 
        #here check copybutffer for valid filename

        return

    tmpname = tmpfile #global or from copybuffer

    g.es('writeing tmpname', tmpname )
    fo = file(tmpname,'w')
    fo.writelines(data + "\n#e\n")
    fo.close()
    
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
#@+node:ekr.20040916153817.39:Bugfixcrunch

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
    #@+node:ekr.20040916153817.40:<< bfcrunch >>
    
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
    
    #@-node:ekr.20040916153817.40:<< bfcrunch >>
    #@nl

    bfcrunch(getline, filename= 'exS')

#@-node:ekr.20040916153817.39:Bugfixcrunch
#@-node:ekr.20040916153817.38:tim_one_crunch
#@-node:ekr.20040916153817.21:codeing macros
#@+node:ekr.20040916153817.41:pre/post macros
#@+node:ekr.20040916153817.42:+DQ3

def dynaZ_DQ3(c):  #part of the dynabutton macro script
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

    #add some specialized sourounders,
    repdict.update({'try':'except', 'if':'else', })
    
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
        sx.append('\n%s:\n    %s%s Exception:\ng.es_exception("eme", True)'%(
                repchar, data, rep2char))
    elif repchar == 'if':
        sx.append('\n%s 1 == 1:\n    %s%s:\npass'%(
                repchar, data, rep2char))
    else:
        sx.append('%s%s%s'%(repchar, data, rep2char))
        
    if not newSel: g.es(''.join(sx) ) #life is too short
    else: dynaput(c, sx)
#@-node:ekr.20040916153817.42:+DQ3
#@+node:ekr.20040916153817.43:du_test-str
""" if you runthis script on itself it can get infinate on you.
not anymore, but if you do get some recursion in your script,
  if you have a console hit ^C once. save your work often.
  python -i leo your.leo is how to get the console
 @test error reporting seems to go only to the console as yet.
 
 potential problem in py2.4 master removed from doctest __all__ 
"""
#@+at
# 
# DO NOT LOAD leo*.py files with load_module it will crash Leo
# leoTest.py is ok, is more or less a standalone to provide @test
# 
# Leo has a safeimport, once it stabalizes can use it for @file.
# you must not run python -OO to use doctest! can we detect this?
# -O is ok but note, this removes asserts, maybe counter productive!
# 
# 
# uses parts of Rollbackimporter and fileLikeObject
# many thanks to python cookbook providers and contributers
#@-at
#@@c

import leoGlobals as g

#@<< Classes >>
#@+node:ekr.20040916153817.44:<< Classes >>
import os, sys, time

import StringIO

#__metaclass__ = type

if sys.platform[:3] == 'win':
    win_version = {4: "NT", 5: "2K", 6: "XP",
        }[os.sys.getwindowsversion()[0]]
else: win_version = 'NM'

if sys.version_info[:2] >= (2, 5): win_version += ' py>24'
elif sys.version_info[:2] >= (2, 4): win_version += ' py>23'
elif sys.version_info[:2] >= (2, 3): win_version += ' py>22'
elif sys.version_info[:2] >= (2, 2): win_version += ' py>21'
elif sys.version_info[:3] == (1, 5, 2): win_version += ' py152'
else: win_version += ' py<21'



import unittest
class _t_(unittest.TestCase):
    def runTest(self):
        pass
try:
    g.app._t
except Exception:
    _t = _t_()
    g.app._t = _t  #allow you to use _t in your script
    del _t
    #del unittest?

#make part of a larger basic python sanity check
try:
    assert(1 == 0)
    print 'YOU HAVE RUN python -O but tests can still fail w/_t'
    #raise SystemExit
except Exception: 
    #print 'assert is a statement, using assert_'
    pass
#@+others
#@+node:ekr.20040916153817.45:ExitError
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
#@-node:ekr.20040916153817.45:ExitError
#@+node:ekr.20040916153817.46:importCode
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
    
        exec code + '\n' in modl.__dict__

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
#@-node:ekr.20040916153817.46:importCode
#@-others
#@-node:ekr.20040916153817.44:<< Classes >>
#@nl

def dynaZ_du_test(c= None):
    """
    takeoff from run @test, see test.leo >py2.3 doctest

    run a unittest from a doctest docstring in the script
    will also run if headline is @test using leoTest in 4.2beta2+
    and in that case, all subnodes of @test will run, @suite too
    
    in your script you can use:
    g.app._t.assert_(1 == 2) and other unittest compares
    you have to import leoGlobals to use it.
    which isn't a much of a deal breaker.
    
    still not redirecting the unit test error to log properly. 
    must be in leoText. run w/console python -i open to see
    need version 2.3. convert a doctest into a unittest if use leoTest
    du_test doesnt create temp files and doesnt require @file

    """
    import leoTest
    reload(leoTest)
    
    import doctest
    import sys

    use_Leo_redirect = 0
    if c is None: c = g.top()
    p = c.currentPosition() 

    #solve the doc/unittest infinate problem if run test on this node
    if p.headString().startswith('du_test-str'): g.es('infinate'); return

    c.frame.putStatusLine('testing '+ p.headString()[:25], color= 'blue')
    c.frame.statusText.configure(
        state="disabled", background="AntiqueWhite1")

    s = '*'*10
    g.es(win_version, time.strftime('%H:%M.%S %m/%d/%Y'))
    g.es('%s \ntesting in %s\n%s\n'%(
        s, p.headString()[:25], s), color= 'DodgerBlue')


    #when run on @test print goes to console
    #this simple redirect isnt working
    #might need to set stdout/err more forcefully
    #have the same problem with evaluator 
    #and it screwsup log redirect after its done.
    if use_Leo_redirect:
        g.redirectStdout(); g.redirectStderr()
    else:
        sys.stdout = g.fileLikeObject() #'cato'
        sys.stderr = g.fileLikeObject() #'cate'

        #usually you dont want to do this,
        _sosav = sys.__stdout__
        sys.__stdout__ = sys.stdout
        _sesav = sys.__stderr__
        sys.__stderr__ = sys.stderr

    if p.headString().startswith('@test '):
        leoTest.doTests(all= False)

    elif p.headString().startswith('@suite '):
        #@        << TestSuite >>
        #@+middle:ekr.20040916153817.47:guts
        #@+node:ekr.20040916153817.48:<< TestSuite >>
        suite = unittest.makeSuite(unittest.TestCase)
        leoTest.makeTestSuite (c, p)
        g.app.scriptDict['suite'] = suite
        leoTest.doTests(all= False)
        #@nonl
        #@-node:ekr.20040916153817.48:<< TestSuite >>
        #@-middle:ekr.20040916153817.47:guts
        #@nl
    else:
        #@        << DocTest >>
        #@+middle:ekr.20040916153817.47:guts
        #@+node:ekr.20040916153817.49:<< DocTest >>
        
        tmpimp = tmp = 'mymod' #name for the mock module
        
        g.es('mock writeing ', tmpimp)  #
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
        
                doctest.testmod(mod, verbose= 1,
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
        #@-node:ekr.20040916153817.49:<< DocTest >>
        #@-middle:ekr.20040916153817.47:guts
        #@nl


    #code below may cause problem if not run 
    #if except traps further up
    #needs its own try/finally
    #is the __ mangling causing sys.__std* not to work corectly?

    if use_Leo_redirect:
        g.restoreStdout(); g.restoreStderr()
    else:
        oo = sys.stdout.get()  #read get()
        oe = sys.stderr.get()  #get()
        sys.stdout.close()
        sys.stderr.close()

        #if you didnt do this it wouldent need to be reversed
        sys.__stdout__ = _sosav
        sys.__stderr__ = _sesav

        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
    
        for x in (oo + oe).splitlines():
            g.es('%r'%x, color= 'chocolate')

    g.es('nonews is goodnews', color= 'DodgerBlue')
    #not sure why but this dissapears in a few seconds, 
    #maybe script end clears it? add an idle 200ms
    c.frame.putStatusLine(' fini ', color= 'DodgerBlue')
    #bad color here causes too much traceback
    c.frame.statusText.configure(background="AntiqueWhite2")


#setup while testing 
if __name__ !=  'dyna_menu':
    try:
        dynaZ_du_test()
    except Exception:
        g.es_exception()
#@nonl
#@+node:ekr.20040916153817.47:guts
#@-node:ekr.20040916153817.47:guts
#@+node:ekr.20040916153817.50:comments
#@+at
# you must not run python -OO to use doctest! can we detect this?
# -O is ok but note, this removes asserts, maybe counter productive!
# not sure -O removes unittest.assert* stuff too.
# need a test suite test suite to check sanity before doing real tests
# m04726a11:01:48 copied to dyna_menu, exSButton is its own plugin now
# thinking about letting it choose names for the submenu randomly
# based on the letter T, S, M or anything chosen
# have to fix why @test result isnt routed to log properly
# and fix creation of those pesky temp files I didnt detect right away
# done! importCode from cookbook was nearly there...
# can try redirect output using Leo fileLikeObject, ok dostest
# still doesnt redirect catch the unittest output. same problem w/evaluator
# attach g.app._t  little more verbose and needs the import but works.
# g._t works too but dont want to bog g down
# tried to set __stdout__ and __stderr__ too, unittest wont budge
# sys hook is next. doctest now seems to do well
# need to be able to toggle verbose and pass verbose to @test
# the fun never ends
# 
#@-at
#@-node:ekr.20040916153817.50:comments
#@-node:ekr.20040916153817.43:du_test-str
#@+node:ekr.20040916153817.51: htmlize

#copy in dynamenu is frozen! has remove sentinals

def dynaZ_htmlize(c= None):
    """htmlize a script, popup webbrowser to show.
    
    grabed parser fromfrom the moinmoin, 
    default is to strip leo sentinal lines.

    you must edit in browser & filename, 
       explorer c:\WINDOWS\TEMP\python.html

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

    """
    #@    << initilize >>
    #@+node:ekr.20040916153817.52:<< initilize >>
    
    import cgi, cStringIO, re
    import keyword, token, tokenize
    
    #trick from aspn/299485
    #htmlize is really plenty fast even on >100k source, 
    #but may as well see if this ever causes errors
    #forgot to get some base timeings before and after.
    #doesnt help the silvercity branch
    try:
        # If available use the psyco optimizing
        import psyco.classes
        base_class = psyco.classes.psyobj
    except ImportError:
        base_class = object  #is there object in py2.2? think so...
    
    _KEYWORD = token.NT_OFFSET + 1
    _TEXT    = token.NT_OFFSET + 2
    
    
    _colors = {
        token.NUMBER:     '#483D8B', #black/darkslateblue
        token.OP:         '#000080', #black/navy
        token.STRING:     '#00cc66', #green
        tokenize.COMMENT: '#cc0033', #red
        token.NAME:       '#4B0082', #black/indigo
        token.ERRORTOKEN: '#FF8080', #redred bare null does it
        _KEYWORD:         '#0066ff', #blue
        _TEXT:            '#000000', #black /is text fg color too
        '_LeoDir':        '#228B22', #directive, forest comment
        '_LeoSen':        '#BC8F8F', #sentinal, tan fade comment
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
    # 
    # 
    # 
    # 
    #@-at
    #@-node:ekr.20040916153817.52:<< initilize >>
    #@nl

    import os, sys
    import leoGlobals as g

    #@    @+others
    #@+node:ekr.20040916153817.53:sanitize_
    
    def sanitize_(s):
        """ Leo's sanitize_filename is too aggressive and too lax
        origional regex from away.js
        this should make nobody happy equally.
    
        >>> sanitize_("|\\ /!@=#$%,^&?:;.\\"'<>`~*+")
        '_____________'
        >>> sanitize_("@abc123[],(),{}")
        '_abc123[]_()_{}'
        """
        if not s: return
        import re
    
        res = re.compile(r"""
        [|\\ /!@=\#\$%,\x5E&\x3F:;.\x22\x27<>`~\*\+\t\n\f\r\b\a]
        """, re.IGNORECASE | re.VERBOSE);  
        #  ^?"' \xnn,  [],(),{} ok, * not sure always ok
    
        #should test for unicode before str()
        return res.sub('_', str(s.strip())).replace('__','_')[:128]
    #@nonl
    #@-node:ekr.20040916153817.53:sanitize_
    #@+node:ekr.20040916153817.54:class Parser
    
    class Parser(base_class):
        """ prep the source for any language
            parse and Send colored python source.
        """
        #@	@+others
        #@+node:ekr.20040916153817.55:__init__
        
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
            
            self.fnd = re.compile(r"%s@\s*@+."%(cmtdelim,) )
        
            #g.es('using delim=', cmtdelim)
            
            if hopts['stripsentinals']: 
                l = []
                for x in self.raw.splitlines():
                    if x.lstrip().startswith("%s@"%(cmtdelim,)): continue
                    l.append(x)
                self.raw = '\n'.join(l)
        
        #@-node:ekr.20040916153817.55:__init__
        #@+node:ekr.20040916153817.56:format
        
        def format(self, formatter, form):
            """ Parse and send the colored source.
            """
        
            # store line offsets in self.lines
            self.lines = [0, 0]
            pos = 0
            while 1:
                pos = self.raw.find('\n', pos) + 1
                if not pos: break
                self.lines.append(pos)
            self.lines.append(len(self.raw))
        
        
            self.pos = 0
            text = cStringIO.StringIO(self.raw)
            sys.stdout.write('<html><head><title>')
            sys.stdout.write('%s </title>\n'%(sanitize_(titl), ))
        
            #here would be a good spot for @noindent directive but skip a line
            #
            sys.stdout.write("""<STYLE TYPE="text/css"><!--
        pre, H1 {color:%s; FONT-SIZE: 80%%; FONT-WEIGHT: bold; }
        Text {background:%s;}
        --></STYLE>
        <SCRIPT LANGUAGE="JavaScript">
        <!-- //
        //-->
        </SCRIPT>"""%(
               _colors[_TEXT], _colors['bg'])) #was both #cc9999
        
            sys.stdout.write('</head><body text="%s" bgColor="%s">'%(
                _colors[_TEXT], _colors['bg']))
            sys.stdout.write('<H3># %s</H3>\n'%(titl,))
            sys.stdout.write('<pre>')  # style
            sys.stdout.write('<font face="Lucida,Courier New">')
            # parse the source and write it
            try:
                tokenize.tokenize(text.readline, self)
            except tokenize.TokenError, ex:
                msg = ex[0]
                line = ex[1][0]
                print "<h3>ERROR: %s</h3>%s" % (
                    msg, self.raw[self.lines[line]:])
            sys.stdout.write('</font></pre>')
            sys.stdout.write('</body"></html>')
        #@nonl
        #@-node:ekr.20040916153817.56:format
        #@+node:ekr.20040916153817.57:__call__
        
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
        
            style = ''
            if toktype == tokenize.COMMENT:
                #setrip comment a little more complicated than sentinals
                #sentinals are always exactly one line, sometimes indented
                #comments after code would need to do NL?
                
                if toktext.lstrip().startswith('#@'):
                    
                    if hopts['stripsentinals']: return  #do in __init__
                        
                    if self.fnd.findall(toktext):
                        toktype = '_LeoDir'
                    else:
                        toktype = '_LeoSen'
        
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
        
        #@-node:ekr.20040916153817.57:__call__
        #@-others
    #@-node:ekr.20040916153817.54:class Parser
    #@-others

    if c is None: c = g.top()
    p = c.currentPosition() 
    
    #to remind, really need to get keywords from Leo for some languages
    #then could handle odd languages better w/same parser
    #c.frame.body.colorizer.python_keywords.append("as")


    #decide which options to apply
    #strip sentinals, comments, syntaxcheck for only python?
    #then create alternate reality for c, c++, other language
    #assume text only nodes are language plain? respect killcolor?
    #to simplify the output 
    #set True for noNUMBER, noOP or noNAME 
    #to disable seperate colors for that entity.
    # the more colors the bigger the output html
    hopts = {
      'stripcomments':False, #would strip sentinals too now
      'stripsentinals':True,  #strips directives too now
      'stripdirectives':False,
      #no color key, that item defaults to text color
      'noNUMBER':False,
      'noOP':False,
      'noNAME':True,  
      'filename':r'c:\WINDOWS\TEMP\python.html',
      'timestring': sys.modules['dyna_menu'].dynaB_Clip_dtef(None, ret= 'r'),
       #path to silvercity css file
    }
    #setting up to read from ini file directly
    #if it doesnt exist, create it else update from it?
    #much as I hate to admit it, the colors will have to be changable
    #and color might be different for each language
    #should allow external css or settable style options same way

    #I know there is a way to do this inside the _color dict
    #it would involve setting hopts before calling initilize
    if hopts['noNUMBER']: del _colors[token.NUMBER]
    if hopts['noOP']:     del _colors[token.OP]
    if hopts['noNAME']:  del _colors[token.NAME]
    filename = hopts['filename']

    lang = g.scanForAtLanguage(c, p)
    lang = str(lang).lower()
    titl = "%s Leo %s script %s"%(
            p.headString()[:75], lang, hopts['timestring'])

    #think this trips an assert if you pass a vnode    
    source = g.getScript(c, p)  #.strip()

    #if no path set getScript will return empty script, bug?
    #must get text other way and do another type of htmlize
        
    try:
        if not source: raise ValueError

        g.es('output', lang, p.headString())
        pars = Parser(source)
    
        # write colorized version to "python.html"/filename
        sys.stdout = open(filename, 'wt')

        if lang == 'python':
            pars.format(None, None)
        else:
            #@            << silvercity >>
            #@+node:ekr.20040916153817.58:<< silvercity >>
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
                    'plain', #null (No styling)
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
                if lang == 'plain' or lang == None: lang = 'null'
            
            
                #should be try
                #silvercity wont complain if it isnt the right extension
                g.es('writeing tmpname', tmpfile )
                fo = file(tmpfile, 'w')
                fo.writelines(pars.raw + "\n")
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
                    for x in (out + err).splitlines():
                        print x
            else:
                print '<i>not a known htmlize supported language</i>'
                print pars.raw
            #@nonl
            #@-node:ekr.20040916153817.58:<< silvercity >>
            #@nl
    
        #getmetrics(source)
    
        sys.stdout.close()
        sys.stdout = sys.__stdout__ #missing from org.
    
        # load HTML page into browser
        if os.name == "nt":
            os.system(r'explorer %s'%filename)
        else:
            os.system("netscape python.html &")

    except ValueError:
        g.es('no @path set, unsupported lang or empty script', 
                color= 'tomato')
        g.es(lang, p.headString())

    except Exception:
        g.es('htmlize malfunction?', color= 'tomato')
        g.es_exception(full= True)


#dynaZ_htmlize()  #uncomment & exS to run standalone test
#@-node:ekr.20040916153817.51: htmlize
#@+node:ekr.20040916153817.59:restoreStd

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
#@-node:ekr.20040916153817.59:restoreStd
#@+node:ekr.20040916153817.60:+del first n char

def dynaZ_del_first_char(c):  #part of the dynabutton macro script
    """del first char in the line
    abstracted everything get/insert related to dynaput
    del_2nd_char would occasionally be usefuil

    applying the logical reverse, what about an add first char?
    might use that to comment out a section of code
    always remembering to have something selected & copyed could get to be a pain
    decided best to have that in another macro, using dynaplayer

    """
    newSel = dynaput(c, [])
    if not newSel: return
    
    try:
        newSel = str(newSel)
    except (UnicodeEncodeError, Exception):
        g.es_exception(full= False)


    sx = []
    for x in newSel.splitlines():
        sx.append(x[1:] + '\n' )

    dynaput(c, sx)
#@-node:ekr.20040916153817.60:+del first n char
#@-node:ekr.20040916153817.41:pre/post macros
#@-node:ekr.20040916153817.3:macros
#@+node:ekr.20040916153817.61:load_menu

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
            g.es('load_ dynaMvar is None')

    #@    << togprpa >>
    #@+node:ekr.20040916153817.62:<< togprpa >>
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
    #@-node:ekr.20040916153817.62:<< togprpa >>
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
    table.append(
        (lst[-2][6:], None, lambda c= c, f= globals()[lst[-2]]: f(c) ))

    #@    << add items >>
    #@+node:ekr.20040916153817.63:<< add items >>
    #there better be at least one macro in lst and one cas entry
    a = 0
    ch = dynaMvar.dynadeflst[0][4]
    subtable = []
    sub = None
    #dynaMvar.dynadeflst.append('dynaz_') #add break sentinal
    
    #the way Leo menu add works is 
    #A. similar to Tk, B. incomprehensable C. it just "works"
    #and why is submenu text  smaller? and how cant I change it.
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
    
    
    #@-node:ekr.20040916153817.63:<< add items >>
    #@nl

    #@    << .add_exSb >>
    #@+node:ekr.20040916153817.64:<< .add_exSb >>
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
        except NameError: #pass
            #g.es_exception()
            g.es(' exSButton no!')
    
    table.append(("add exSButton", None,  #^E or is it shifted too?
                   ecall) )
    #@nonl
    #@-node:ekr.20040916153817.64:<< .add_exSb >>
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
    #@+node:ekr.20040916153817.65:<< show clip >>
    #show whats in the clipboard, replace clipboard with left side of pair
    #this isnt dynamically updated each menu invocation in plugin
    #nu.add_command(label= "Clip=%r"%(
    #            g.app.gui.getTextFromClipboard()[:6],), )
    
    dynai = Tk.Menu(None, tearoff= 0, takefocus= 0 )
    for x in  '\' Sq, " Dq, \'\'\' Sq3, """ Dq3, : file, | !file, \\\\ Dbs, ( ), { }, [  ], try /ex, if /else '.split(', '):
            dynai.add_command(label= x, 
              command= lambda x= x, f= g.app.gui.replaceClipboardWith: 
              f(x.split()[0]) ) 
    
    nu.add_cascade(menu= dynai, label= 'choice' )
    #@nonl
    #@-node:ekr.20040916153817.65:<< show clip >>
    #@nl
#@-node:ekr.20040916153817.61:load_menu
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


if Tk:
    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui and g.app.gui.guiName() == "tkinter":

        dynaMvar = None

        if NDebug:
            g.es("dyna_menu", color="gold2")

        #w/o create-optional-menus is called from dynacaller
        # menu is created after last standard leo menu , Help
        #after-create-leo-frame is called after create-optional-menus
        #start1 and new may or may not be called on new
        #everything is a quandry before it works

        leoPlugins.registerHandler("create-optional-menus", load_menu )
        
        
        #stealing code from timestamp plugin
        # lp.registerHandler("command1", timestamp)
        #isnt there a finer grained control than command1?
        #seems like this would slow things down conciderable
        #probably because wanted to catch tangle too
        # save1 should be less overhead
        leoPlugins.registerHandler("save1", timestamp)
        

        #plugin_signon reloads the plugin, can forgo that
        #g.plugin_signon(__name__)  # + __version__
        #__name__.__doc__ = ""

#

#@@language python
#@@color
#@nonl
#@-node:ekr.20040916153817.1:@thin dyna_menu.py
#@-leo
