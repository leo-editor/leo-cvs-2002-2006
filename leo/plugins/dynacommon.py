#@+leo-ver=4-thin
#@+node:ekr.20040916153817.70:@thin dynacommon.py
"""
helper code your macro can call from dyna_menu or other Leo script/plugin.
the first section is filenames, you have to edit in your correct path.

check your sys.path that plugins is there before import
from dynacommon import *
was clone, is common to dynabutton, dynatester & dyna_menu
exSButtton & htmlize use ScrollMenu

some things common like the dynaBunch & init you probably wont call
generate this file to exist in the Leo plugins directory.
"""

#__all__ = 'tmpfile py ptpath leosrc reindent pycheck2 pycheck '.split()
#this needs its own dictionary dopylint doreindent

#note, these changes are at the time the button or menu is created
#to effect these changes you have to 
#write the plugin and start a new python and leo. maybe reload
#execute script on the dynaclick node for the dynabutton
#they will take effect in dynatester imediatly
#preserve the space after to allow for parameters
#those that will be joined to pypath start with seperator \ or /
#any scripts should have their own full path, 

import sys, os
import leoGlobals as g
import Tkinter as Tk

#pypath = r'C:\c\py\Python233'         #nospace
pypath = g.os_path_split(sys.executable)[0]

#py =  pypath + '/python.exe -tOO '     #_space_
py =  g.os_path_join(pypath, 'python.exe') + ' -tOO '

#leosrc = r'c:\c\leo\leo4CVS233\src'
leosrc = g.app.loadDir

reindent = pypath + '/Tools/scripts/reindent.py '  #space

#print pypath, py, leosrc

#classic pychecker
pycheck = pypath + '/Lib/site-packages/pychecker/checker.py '  #space
#pychecker2, doesnt import, is alot slower and less details.
# and leaves some temp files, I guess its still experimental.
pycheck2 = pypath + '/Lib/site-packages/pychecker2/main.py '


#
#classic pychecker I think does import regex which causes a warning when called from plugin. maybe they fixed that in the latest version.
#not sure why dont see it when run from dynabutton. output on stderr?
#DeprecationWarning: the regsub module is deprecated; please use re.sub()
# was caused by tim1crunch, I supress the warning now.

#set to 1 to call pylint after pychecker or 0 for just pychecker
dopylint = 1  #this call in makatemp is too complicated to code in here
doreindent = 0 #in makatemp to forgo reindent step

#it might be preferable to generate a new tmpfile w/pid or something 
# ok for singleuser no security multiuser issues for now.
#YMMV, I set tmp and temp in autoexec, 
#use lower if on *nix. 
#windos may set TEMP and TMP by default, case insensitive.
#
#tmpfile = os.path.join(os.environ['tmp'],'tmptest.py')

#it seems pylint has to be able to import from site-packages
#look in makatemp trying to add tmp to syspath isnt easy from Leo
tmpfile = os.path.join(pypath, 'lib/site-packages', 'tmptest.py')

#replace forwardslash to backslash if required
#frd slash usually ok except for cd and sometimes openfile
#with filename as parameter in windos frdslash might be taken as option
tmpfile = tmpfile.replace('/', '\\')

try:
    True and False
except NameError:
    # match the 2.2 definition
    (True, False) = (1==1), (1==0)

false = False
true = True

#import StringIO
#possibly there are unicode anomalies in cStringIO?
try:
    import cStringIO as StringIO
except ImportError:
    import StringIO

__version__ = '0.0137'  #r04909p04:58

#@+others
#@+node:ekr.20040916153817.71:others

def _caller_symbols():
    """aspncookbook/52278
    Print an expression and its value, 
    along with filename and linenumber
    by Itamar Shtull-Trauring

    thanks I.! returns the callers callers globals and locals
    """
    try:
        raise StandardError
    except StandardError:
        t = sys.exc_info()[2].tb_frame
        return (t.f_back.f_back.f_globals, t.f_back.f_back.f_locals)
#@+node:ekr.20040916153817.72:DDList
"""Tkinter Drag'n'drop list John Fouhy
Last update: 2004/07/06, Version: 1.0, Category: User 
A Tkinter listbox which supports drag'n'drop reordering of the list.
"""

class DDList(Tk.Listbox ):
    """ A Tkinter listbox with drag'n'drop reordering of entries. """

    def __init__(self, master, ** kw ):

        kw['selectmode'] = Tk.SINGLE

        Tk.Listbox.__init__(self, master, kw )

        self.bind('<Button-1>', self.setCurrent )
        self.bind('<B1-Motion>', self.shiftSelection )

        self.curIndex = None

    def setCurrent(self, event ):
        self.curIndex = self.nearest(event.y )

    def shiftSelection(self, event ):
        i = self.nearest(event.y )

        if i < self.curIndex:
            x = self.get(i )
            self.delete(i )
            self.insert(i + 1, x )
            self.curIndex = i

        elif i > self.curIndex:
            x = self.get(i )
            self.delete(i )
            self.insert(i - 1, x )
            self.curIndex = i


if __name__ == '__main__':

    tk = Tk.Tk()
    length = 10
    dd = DDList(tk, height = length )
    dd.pack()

    for i in xrange(length ):
        dd.insert('end', str(i ))

    def show():
        for x in dd.get(0, 'end'):
            print x,
        print
        tk.after(2000, show )

    tk.after(2000, show )
    tk.mainloop()

    #

#
#@-node:ekr.20040916153817.72:DDList
#@+node:ekr.20040916153817.73:ScrolledMenu

class ScrolledMenu(Tk.Toplevel):
    def __init__(self, command=None):
        self.command = command
        Tk.Toplevel.__init__(self)
        self.withdraw()
        self.overrideredirect(1)
        self.listbox = DDList(self, name= 'lb')
        scroll = Tk.Scrollbar(self, orient='v', command=self.listbox.yview)
        self.listbox.configure(yscrollcommand=scroll.set)
        self.listbox.pack({'fill':'both', 'expand':1, 'side':'left', })
        scroll.pack({'fill':'y', 'side':'right', })
        self.bind('<ButtonPress-1>', self._press)
        self.bind('<ButtonPress>', self._close)
        self.bind('<KeyPress-Escape>', self._close)
        self.listbox.bind('<ButtonRelease-1>', self._select)
        self.up = 0

    def popup(self, onto):
        x = onto.winfo_rootx()
        y = onto.winfo_rooty() + onto.winfo_height()
        self.geometry('+%d+%d' % (x,y))
        self.deiconify()
        self.up = 1
        self.grab_set_global()

    def _close(self, event=None):
        self.grab_release()
        self.withdraw()
        self.up = 0

    def _select(self, event):
        self.update() # let the listbox change its selection
        self._close()
        index = self.listbox.curselection()
        value = self.listbox.get(index)[0]
        if self.command is not None:
            self.command(value)

    def _press(self, event):
        x,y = self.winfo_pointerxy()
        window = self.winfo_containing(x,y)
        if window is None or window.winfo_toplevel() != self:
            self._close()
            

class _Test(Tk.Tk):
    def __init__(self):
        Tk.__init__(self)
        self.sm = ScrolledMenu(self.result)
        apply(self.sm.listbox.insert, (0,)+tuple(string.lowercase))
        self.b= Button(self, text='Test', command=self.popup)
        self.b.pack()

    def result(self, value):
        print 'selected:', value

    def popup(self):
        self.sm.popup(self.b)

#if __name__ != 'exSButton':
#    mw = _Test()
#    mw.mainloop()
#@nonl
#@-node:ekr.20040916153817.73:ScrolledMenu
#@-node:ekr.20040916153817.71:others
#@+node:ekr.20040916153817.74:fixbody

def scriptbody(c, p):
    """AttributeError: vnode instance has no attribute 'copy'
    this removes all sentinals but might be switchable somehow
    something chged in 4.2b2+ while using linenumber macro
    df.write(p, nosentinels= true, scriptFile= fo)
  File "c:\c\leo\V42leos\leo\src\leoAtFile.py", line 4754, 
  in write scriptFile.clear()
AttributeError: StringIO instance has no attribute 'clear'
moveing away from 4.1final if use filelikeobject
chg to g.fileLikeObject() but really its toString= True
leaveing it false was trigering an assert, seems redundant
if scriptfile its onnvious that its to string also
but I dont really know the ins and outs of the new script stuff.
this whole thing can be replaced with g.getScript(c,p) in 4.2
but thats always with sentinals I guess... API moveing too fast
still getting an assert error sometimes

        """
    df = c.atFileCommands.new_df
    df.scanAllDirectives(p, scripting= True)
    # Force Python comment delims.
    df.startSentinelComment = "#"
    df.endSentinelComment = None
    # Write the "derived file" into fo.

    fo = g.fileLikeObject()  #was StringIO.StringIO() 

    #self.writeOpenFile(root,nosentinels,scriptFile,thinFile,toString)
    #df.write(p.copy(), nosentinels= true, scriptFile= fo)
    df.write(p.copy(), nosentinels= True, scriptFile= fo, toString= True)
    assert(p)  #why assert after the write?
    return fo.get() #getvalue() 


def selecbody(data, sdict):
    """ if selected starts after @ it should be commented anyway?
    
    backslash inside string literal, always skips the next char 
    \s might have to be \\s in raw?
        """
    cmtdelim = '#'
    if sdict['language'] != u'python':
        #obviously for other language have to check is valid
        # is more than one, then have to trail each line etc
        #was delims[0] not sure where that came from
        #coverage tool might have caught that so far untested
        cmtdelim = sdict.get('delims', ['#'])[0]
        
    import re
    datalines = data.splitlines(True)
    #print 'data is %r'%(datalines,)


    #not sure why <\< works
    #does \s work like s, apparently not. 
    #though \s was only for rawstring w/o it misses indented @|<
    repATang = re.compile('\s*<\<.*?>>.*')  #^$ 
    repATc = re.compile('\s*@.*', re.MULTILINE )
    #could use it on the whole string, ok line by line too.


    sx = []
    inATc = False  #a comment, not @c. poor name choice here.
    for x in datalines:
        
        if inATc:  #chances are Leo already does this somewhere
            #what about the foolish @color inside already started comment?
            #any @ is end of comment directive, 
            if x.startswith('@c'): #@ but its not stopping till @x!
                inATc = False
            sx.append('%s%s'%(cmtdelim, x) )
            continue

        if repATc.match(x):  #is start of comment
            if x == '@\n' or x.startswith('@ ') or \
                x.startswith('@\t') or x.startswith('@doc'):
                inATc = True
            sx.append('%s%s'%(cmtdelim, x) )
            continue

        if repATang.match(x): #is sectionname
            #would need to get more fancy here
            sx.append('%s%s'%(cmtdelim, x) )
            continue
        
        #if x == '\n': continue  #delete blank lines?

        sx.append(x)

    return ''.join(sx)

def fixbody(data, c= g.top()):
    """ assumed leo body, forces str & expandtabs
    @directives commented out
    from @ to @c commented out
    have to make sure doesnt expand \n \t etc literals in strings
    that is a problem when include section refrences as data
    eventually follow @others, and section refrences or use Leo API
    comments sectionnames
    commented out indented @others or sectionnames 
    add a strip comments mode to speedup the processing on larger data
   I was a little confused about directive use. forgot @c is code
  (@ followed by a space, tab or newline) or @doc
  Body text from an @c or @code directive to the
    next @<space> or @directive.  
    Leo itself doesnt stop the comment if @path after @space
    @doc isnt commented, not sure what that is.
   @color/@nocolor work @path doesnt stop comments
   any htmlize of the body should follow these very closely
   even if just rendering code

    1/2h looking thru leodoc leopy, 1/2h looking thru leo*file
    I have no idea how to do this using the Leo API
    maybe some other plugin does it? rst must have some of it
    obvious solution would be a recurxive one.
    it seems the plugins and scripts do alot of the node traversal
    I dont see where they are calling Leo
    nor do I see how they follow @others or sectionnames
    
    luckily it continues on to comment after any @directive till @c
    the goal here is not to mimic Leo. but to render all @ as comments

    should get directives so the proper comment are rendered
    in c for ex, might want to mark and output /* comments */
    or in style section of html or inside script = javascript
    name fixbody is a misnomer here, I assume we are in body
    and the c would be valid but who knonws.
    its only passed data so that has to change.
    chg to data, c if data is None then assume the worst
    still going to need what node selected text is in?
    otherwise how to use language & delims
    

{'language': u'python', 'pagewidth': 80, 'encoding': None, 'delims': ('#', None, None), 'lineending': '\n', 'tabwidth': -4, 'wrap': 1, 'path': u'', 'pluginsList': []}
     just because I get the directives, doesn't mean I respect them all.
     
     
    the other piece is implimenting a toggle get @others or just node
    if if get @others, will the caller be responsible for knowing
    if the current node is the complete piece of the program? guess so.
    not ready to go recursive yet,   
    going to need a follow @other 
     but add dont comment mode & strip docstrings also 
    
    executescript in leocommands has code to derive a file to an object
    it takes care of comments and I assume adds sentinals.
    it does the @ comments, 
    but removes all other sentinal as presently setup
    selectedtext passes thru my @directive commenter
      """

    if not c:
        g.es("in fixbody, empty c")
        return

    p = c.currentPosition()
    v = c.currentVnode() # may want to chg for 4.2
    #sdict = g.scanDirectives(c, v) 
    sdict = g.scanDirectives(c, p) 
    #print sdict

    if not data:
        #g.es("in fixbody, empty data, using body")
        #data = v.bodyString()
        #data = str(scriptbody(c, p).expandtabs(4))
        data = g.getScript(c, p)  #.strip()

    else:
        print  'data is %r'%(data,)

        #gota be a better way than this
        try:
            data = str(selecbody(data, sdict).expandtabs(4))
        except (UnicodeEncodeError, Exception):
            g.es_exception(full = False)
            data = selecbody(data, sdict).expandtabs(4)

    if not data:  data = '\n'  #avoid error on empty script

    return data
#@nonl
#@-node:ekr.20040916153817.74:fixbody
#@+node:ekr.20040916153817.75:dynastuff
#@+at
# #code for dyna
# 
#     - dynaBunch
#     - dynaerrout
#     - captureStd
#     - runcmd
#     - dynadoc
# 
# 
#@-at
#@+node:ekr.20040916153817.76:AskYesNo

#file leoTkinterGui.py
#import tkFont,Tkinter,tkFileDialog leoTkinterDialog
#class tkinterGui(leoGui.leoGui):
#when it works add some way to up the damm fonts!

def runAskYesNoCancelDialog(title,
    message=None,yesMessage="Yes",noMessage="No",defaultButton="Yes"):
    """Create and run an askYesNoCancel dialog ."""
    import leoTkinterDialog
    d = leoTkinterDialog.tkinterAskYesNoCancel(
        title,message,yesMessage,noMessage,defaultButton)
    #d.configure(font=(("Lucida", "Console"), 12)) #nfg
#AttributeError: tkinterAskYesNoCancel instance has no attribute 'configure'
    #d.buttonsFrame.configure(font=(("Lucida", "Console"), 12)) #nfg
    #tryed buttonsFrame, frame, top, root...

    return d.run(modal=true)
#@nonl
#@-node:ekr.20040916153817.76:AskYesNo
#@+node:ekr.20040916153817.77:dynaBunch

def init_dyna(c, *a, **k):
    """same for both button and menu
    """    
    caller_globals, caller_locals = _caller_symbols()

    dynainst = dynaBunch(
        dynadefaultFlag = Tk.IntVar(),
        dynapastelst = ['print', 'paste', 'doc'],
        dynapasteFlag = Tk.StringVar(),
        #getsubnodes different in button & menu, lst is a list of macros
        dynadeflst = dyna_getsubnodes(c,  globs= caller_globals),
        )
    
    #print to start, paste over selection later

    dynainst.dynapasteFlag.set(dynainst.dynapastelst[0] )
    dynainst.dynadefaultFlag.set(0)
    return dynainst


class dynaBunch(object):
    """tieing an instance of dynaBunch to c.frame is responsibility of caller
    Bunch aspn python cookbook 52308
    point = Bunch(datum=y, squared=y*y, coord=x)
    if point.squared > threshold:
        point.isok = 1
    in Leo From The Python Cookbook. used setattr & getattr
     not sure of the ivar stuff for now
    repr lifted from c.l.py
    clear might still use, need gc tests
     http://www.norvig.com/python-iaq.html  (Struct class)

    in the sprit of one obvious way to do it.
    the idom appears to be to change the name of the class
    and hype it as a way to turn a dict into a lot of instance vars
    alot are taking credit for this idea through the years,

        """
    import operator

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return '%s(%s)' % (self.__class__.__name__, '\n'.join(
            ['%s=%r' % keyval for keyval in self.__dict__.items()]))

    def __clear(self):
        g.es('attempting to clear')
        for key in self.__dict__.keys():
            g.es(';k=',key)
            del key
            g.es('deleted')
        g.es('\ndone clear')

    def set_ivars(self, c):
        """Set the ivars for the find, from searchbox
        might want to use this
        """
        # Modified from leoTkinterFind.set_ivars
        #for key in self.intKeys:
        #    setattr(c, key + "_flag", 0)  

    def ivars(self):
        return self.__dict__.keys()
        
    def __setitem__ (self,key,value):
        #allows access like dyna['dynalst']?
        return operator.setitem(self.__dict__,key,value)
        
    def __getitem__ (self,key):
        return operator.getitem(self.__dict__,key)

    """
    def load(infile):
        strng = infile.read()
        exec( 'bag = Bag(\n' + strng + ')' )
        return bag
    load = staticmethod(load)

    def save(self, outfile):"""
#@nonl
#@-node:ekr.20040916153817.77:dynaBunch
#@+node:ekr.20040916153817.78:dynaerrout

#quiet warnings from pychecker and tim1 about regex

import warnings

warnings.filterwarnings("ignore",
         r'the regex module is deprecated; please use the re module$',
         DeprecationWarning, r'(<string>|%s)$' % __name__)
warnings.filterwarnings("ignore",
         r' the regsub module is deprecated; please use re.sub\(\).$.$',
         DeprecationWarning, r'(<string>|%s)$' % __name__)

if sys.version_info >= (2, 3): #py2.2 no simple
    warnings.simplefilter("ignore", DeprecationWarning, append=0)

'''C:\c\leo\leo4CVS233\plugins\dyna_menu.py:774: DeprecationWarning: the regex module is deprecated; please use the re module
  import regex
C:\C\PY\PYTHON233\lib\regsub.py:15: DeprecationWarning: the regsub module is dep
recated; please use re.sub()
  DeprecationWarning)'''

#maybe can turn on full exception reporting 
#rather than rolling my own
# es_event_exception (eventName,full=false):
#excepthook() like displayhook?
# __displayhook__ = displayhook(...)
#        displayhook(object) -> None
#   __excepthook__ = excepthook(...)
#        excepthook(exctype, value, traceback) -> None

#    # dynaM_tim_one_crunch 909 1071
#    print 'co_name=', sys._getframe(1).f_code.co_name
#    print 'lineno=', sys._getframe(1).f_lineno  #
#sys._getframe().f_code.co_name returns ? while in exscript
#make a method of something so can use it to find the linenumber in macro
#possibly even jump directly to the source on error in dynatester
#lt = classmethod(doDefault) self = frame.f_locals['self'] 
#  import sys  g.es('lineno= ' + sys._getframe().f_lineno )


def dynaerrout(err, msg):
    """from fuzzy cmd
    Leo often masks the errors 
    making debuggin of this kind of script more painful than not
    """
    
    from traceback import print_exc

    g.es(msg, color= 'tomato')
    f = StringIO.StringIO()
    print_exc(file= f)
    a = f.getvalue().splitlines()
    for line in a:
        #g.app.goToLineNumber(int(newSel))
        g.es(line, color= 'tomato')
#@nonl
#@-node:ekr.20040916153817.78:dynaerrout
#@+node:ekr.20040916153817.79:getsubnodes

#code to operate dynamenu, no user code


def dyna_getsubnodes(c, globs= {}):
    """ changed API slightly, macros now need a common first 5 chars
    if I can change it to dont care about the name I will.
    
    from the plugin, the old way of walking the node to find macros
    is not going to work I just realized
    there is no current node, this has to run before the plugin is made
    and somehow encode the macros and decode them, 
    and insert them into the plugins namespace. yikes
    maybe if I put @others in a stratigic place, they will be included
    all that would remain is to get their names from a __dict__
    
    glitch, they arent added in the order defined in macros node.
    sorting
    glitch when in dynacommon globals isnt the callers globals!
    """
    lst = []

    try:
        lst = [x for x in globs
                if x.startswith('dyna')
                if x[5] == '_'   #x[4] specifys type of macro
                ]

        #possibly decorate somehow to respect the order defined in the py
        #maybe add a user char after _ to specify numeric position
        
    except Exception, e:
        # d=rew  Leo caught syntax error, space
        #Leo caught TypeError: ut() takes exactly 1 argument (2 given)
        #d=rew might not have caught this, or not printed full traceback
        dynaerrout(e, "initMdyna ")

    lst.sort()
    #es('dynamenu macros %s'%(lst,) )
    return lst
#@nonl
#@-node:ekr.20040916153817.79:getsubnodes
#@+node:ekr.20040916153817.80:captureStd
class captureStd(object):
    """the typical redirect stdout
    add stderr and stdin later
    borrowing the class from PH testsuite for redirect stdout

    leo also has filelike objects and its own redirect    
    there isa config option and a plugin to redirect to log
    and to append to body of captured output

    another way
    sys.displayhook = mydisplayhook

    >>> def mydisplayhook(a):
    ...     if a is not None:
    ...             sys.stdout.write("%r\n" % (a,))
    ...
        """
    def captureStdout(self):
        sys.stdout = StringIO.StringIO()

    def releaseStdout(self):
        captured = sys.stdout.getvalue()
        sys.stdout = sys.__stdout__
        return captured
#@nonl
#@-node:ekr.20040916153817.80:captureStd
#@+node:ekr.20040916153817.81:runcmd

#runcmd(cmds) & forklike(*cmds)

def runcmd(cmds):
    """for win9x this works better than other popen for me.
    on *nix you can import commands or something else popen5 maybe
    this does wait and leo is inactive so if there is a chance
    the process will infinate loop, better use a spawner
    you get the return output outerr stdout stderr
    """
    import os
    child_stdin, child_stdout, child_stderr = os.popen3(cmds)
    
    output = child_stdout.read()
    outerr = child_stderr.read()
    
    return output, outerr
    
    
def forklike(*cmds):
    """still experimenting
     on *nix you can commands or fork or this 
    this does not wait and leo is active 
    but it appears to reuse the same console if there is one
    not sure what happens if use leo.pyw

    returns the pid I guess its meaningless on windows?

cmds
('C:\\c\\py\\Python233\\python.exe -tOO ', 'C:\\c\\py\\Python233\\lib\\site-packages\\tmptest.py')

params, para
['C:\\c\\py\\Python233\\python.exe', '-tOO'] ['-tOO', 'C:\\c\\py\\Python233\\lib\\site-packages\\tmptest.py']
says needs string only
startfile( os.path.normpath(path) ) 

times( ) Return a 5-tuple of floating point numbers indicating accumulated (processor or other) times, in seconds. The items are: user time, system time, children's user time, children's system time, and elapsed real time since a fixed point in the past, in that order. 
(2868845789.5628495, 0.0, 0.0, 0.0, 0.0)

tryed startfile
WindowsError: [Errno 2] The system cannot find the file specified: 'C:\\c\\py\\Python233\\python.exe -tOO C:\\c\\py\\Python233\\lib\\site-packages\\tmptest.py'
    """
    import os

    #all the good ones are *nix only
    # from spawnl got traceback return spawnv(mode, file, args)

    params = cmds[0].split()
    para = ''
    if len(params) > 1:
        para = params[1:] + list(cmds[1:])
        # os.path.normpath(path) 

    #print os.times()
    print cmds
    print params, para


    cmd = params[0]
    #cmd = 'c:/Command.com' #c:/windows/system32/cmd.exe 

    #s = ' '.join(['%s'%x.replace('\\\\', '\\') for x in para])
    #print s
    #output = os.startfile(s)  #cant handle command w/params?

    output = os.spawnl(os.P_NOWAIT, cmd, *para )
    
    return output
#@nonl
#@-node:ekr.20040916153817.81:runcmd
#@+node:ekr.20040916153817.82:dynadoc

def dynadoc(c, sub= 'all' , globs= {}):
    """read dynadeflst and createdoc for them
        was previously print, but that doesnt work well in plugin
        add a simple wrap, which isnt appending dash in midword like expected
        could set wrap on for the log. then off again, 
        would probably unwrap  though

    combined the call to all and removed else. works because
    a list is made from sub, will preclude docing a macro named all

    using now \python233\lib\textwrap.py, if available
    too many amonalies in fordoc too little time.
    made a wraper macro, dont really want another depency
    would have to extract the relevant code and have the 
    macro call it too. ok a little code duplication for now
    
    expand to show macro's internal __dict__
    getting doc for fliper for ex, might be nice to know
    
  """
    import sys
    try:
        import textwrap as tw
    except ImportError:
        tw = None  #or overwrite formdoc
        g.es('textwrap is going to produce better resiults.')
        g.es('get it from the python cvs archive\n')
        

    #from pydoc import resolve, describe, inspect, text, plain

    def formdoc(doc):
        """create a rough wraper to 40 charlines"""
        sx = doc.expandtabs(2).splitlines()
        sl = ['\n']
        for i, x in enumerate(sx):
            if i > 6: break  #beyond that is implimentation details

            if len(x) < 42: sl.append('  ' + x.lstrip()); continue

            if len(x) > 50: ax = 50
            else: ax = len(x) - 1

            dash = '-'
            while ax > 35:
                if x[ax] in ' .,(){}[]?\n': dash = ''; break
                ax -= 1
            #if ax w/in few char of len(x) may as well be one line
            #check it isnt eating a char at ends
            sl.append('  ' + x.lstrip()[:ax] + dash)
            sl.append('   ' + x.lstrip()[ax:])

        sl.append('\n')
        return '\n'.join(sl)

    lst = [sub ] 
    if sub == 'all':
        lst = g.app.dynaMvar.dynadeflst

    #g.es(g.__dict__.keys()) {}
    #g.es(g.app.__dict__.keys()) Leo ivars

    for x in lst:
        #need to get the callers globals
        #f = g.app.dynaMvar.globals()[x]  nor globals()[x]
        #f = g.app.__dict__[x]  #is this same as app.globals()[x]
        try:
            f = globs[x]  #
        except Exception:
            g.es('cant find', x)
            continue
        
        coln = 460

        #if no doc problems
        #try to get len of unsized object or unscriptable object
        #hasattr(f, '__doc__') always true for a function
        if f.__doc__:
            doc = f.__doc__[:coln]
            if len(f.__doc__) > coln: elip = ' ...'
            else: elip = ''
        else:
            doc = ' no additional info '
            elip = ''

        if not tw:
            st = formdoc(doc)
        else:
            t = tw.TextWrapper(
                     width= 42,
                    initial_indent=' ',
                   subsequent_indent= ' ',
                   expand_tabs= True,
                  replace_whitespace= True,
                 fix_sentence_endings= False,
                break_long_words= True )

            st = t.fill(doc)


        g.es('\n' + x + '.__doc__\n' + st + elip)
        #g.es('\n' + str(f.__dict__))  #{}

    #obj, name = resolve(x, 0)
    #desc = describe(obj)
    #g.es(text.docroutine(f, x))
    
#@nonl
#@-node:ekr.20040916153817.82:dynadoc
#@-node:ekr.20040916153817.75:dynastuff
#@+node:ekr.20040916153817.83:dynaput

def dynaput(c, slst):
    """return the text selection or put it if slst is not None
    assumes slst is a list to be joined and print/paste as toggled
     add other option, paste w/o delete
    up to the caller to insert \n if required
    eventially pass in event so can get text from any widget
    for now, hardwired to use the Leo API to the Tk text widget   
    **slight problem, wont insert something wth nothing selected
 leoTkinterFrame

  add another menu toggle for print to clipboard 
    in addition to printing or instead of printing
     and replace or append to clipboard.
  bodyCtrl
  allowing fixbody to be called so added test for paste & no selected 
  and selected or slst
  if nothing selected and slst then 3rd choice. must be a full body
  bad idea to past over the node because it wont follow nodes.
  
  problem since split into dynacommonm
  g.top().frame.dynaMvar no longer reliable doe some reason
  maybe that shouve always been based on c? isnt that already c? 
  still havent got a handle on why its failing.
  decide to spend another var. g. works but g.app better
    """
    cg = g.app.dynaMvar #top().frame.
    #print cg

    #this depends on the macro calling dynaput first as they mostly do now
    #bound to be some sideffects untill I put it in the right place
    #maybe the menu has to have a function caller instead of calling the function
    if 'doc' == cg.dynapasteFlag.get():

        #what about dynabutton
        #g.es(sys.modules[dyna_menu].keys())
        caller_globals, caller_locals = _caller_symbols()
        #g.es("this_caller", caller_globals)

        #in dynabutton they are all radio buttions 
        #and its easy to see which was called. unlike in plugin
        #dump all for now
        dynadoc(c, globs= caller_globals)
        return

    Tx = c.frame.body
    if Tx.hasTextSelection() or slst: #*
        
        #returns selection point if nothing selected
        Tst,  Ten = Tx.getTextSelection()

        if not slst: #**and Tx.hasTextSelection()
            return Tx.getTextRange(Tst, Ten)

        else:

            #ux = g.toUnicode(x[1:] )  ?? need to know the encodeing!
            # toUnicode(before,app.tkEncoding), hope Leo handles this
            ux = ''.join(slst)
    
            if 'print' == cg.dynapasteFlag.get():
                #print ux
                g.es(ux)

            elif 'paste' == cg.dynapasteFlag.get() and \
                    Tx.hasTextSelection():
                g.es('overwrite\n', str(Tx.getTextRange(Tst, Ten)) )

                v = c.currentVnode() #should this be positions in 4.2?
        
                #btw, Tk insert doesnt disturb the selection.
                Tx.deleteTextSelection()
                #Tx.onBodyWillChange(v, "Delete")
        
                Tx.setInsertionPoint(Tst)
        
                #print '%r', ux
                Tx.insertAtInsertPoint(ux)
                Tx.onBodyWillChange(v, "Typing")
        
                #selection may wander depending on the final size
                Tx.setTextSelection(Tst,  Ten)

            else:
                g.es('nothing selected',
                         cg.dynapasteFlag.get() )

    else: g.es("no text selected", color= 'orangered' )
#@-node:ekr.20040916153817.83:dynaput
#@+node:ekr.20040916153817.84:dynaplay

def dynaplay(c, splst):
    """playback commands from a list into the selected or body text
    inventing a new little language isnt a trivial endevor
    should do some research to find out if I can steal one
    didnt takevery long to get initial results
    need to preparse and push repeat n, and parse n for other commands
    preparsing is dificult, untill you act you dont know if it will raise an error
    this first cut wont allow repeat and n as easily
    repete means startover to the repete -= 1. 
    what if there is another repete, the previous repete needs to be reset

    need to set insert point so repete works, independant of paste mode?
    tricky, first time thru insert can be outside of selection
    and commands can try to insert outside of selection
    undo doesnt change insertpoint

    """
    if not splst: return

    def g_row(ip): return int(ip)
    def g_col(ip): return int(ip - g_row(ip))

    nothingselected = False
    data = dynaput(c, [])
    g.es("selected ")
    if not data:
        nothingselected = True
        g.es("...skip, dump the body")
        v = c.currentVnode() # may chg in 4.2
        data = v.bodyString()

    ip = float(c.frame.body.getInsertionPoint())
    #this apparently does the right thing if nothing selected 
    Tst,  Ten = c.frame.body.getTextSelection()

    #on selection insert is at end or start
    #if repete play you want the insert if its midselection somewhere
    #print 'Tst%r <= ip%r <= Ten%r'%(Tst, ip, Ten)

    if c.frame.body.hasTextSelection():
        if float(Tst) <= ip < float(Ten):
            pass
        else: ip = float(Tst)
    

    sx = data.splitlines(True)
    sx[0:0] = ' ' #make it base1

    for x in splst:
        if x.startswith('%%C,'): #command
            comd = x[4:].lower()
            if comd == '[down]':
                ip += 1.0

            elif comd == '[up]':
                ip -= 1.0

            elif comd == '[home]':
                ip = float("%d.%d"%(g_row(ip), 0 ))

            elif comd == '[end]':
                ip = float("%d.%d"%(g_row(ip), len(sx[g_row(ip)]) ))

        else: #must be an insert something
            try:
                b = sx[g_row(ip)][:g_col(ip)]
                m = x
                a = sx[g_row(ip)][g_col(ip):]
    
                sx[g_row(ip)] = '%s%s%s'%(b,m,a)
                ip = "%d.%d"%(g_row(ip), len(x) + g_col(ip) )
                ip = float(ip)
                c.frame.body.setInsertionPoint(ip)
            except IndexError, err:
                g.es('command outside selection', err)

        g.es('ip=%r, x=%r'%(ip, x))

    dynaput(c, sx[1:])
    c.frame.body.setInsertionPoint(ip)
#@-node:ekr.20040916153817.84:dynaplay
#@-others
#
#@nonl
#@-node:ekr.20040916153817.70:@thin dynacommon.py
#@-leo