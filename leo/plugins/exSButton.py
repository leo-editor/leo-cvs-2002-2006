#@+leo-ver=4-thin
#@+node:ekr.20040916153817.66:@thin exSButton.py
#unfinshed, works, but, selectable options do nothing.
"""
you can execute script from every leo buttonbar.

to add a button to run a script , rclick on exS
a menu drop down with choices will appear
you can drag the options. the order doesn't persist yet.
also rClick doesnt copy and drag triggers the option.

options are/will be: 
*runfrom node, 
*run from memory
*persist its globals
*load/save ini
*etc etc

right click on the created button to get its options.
some default options + some gleaned from its doc string
many of the macros could use such option parsing.

remember to position youscript manually if required
otherwise you are at the current node.

  maybe you could change a few things and have it do
  something else you would find more useful.
  that will become easier as the code gets smarter.
  be sure and post your problems or suggestions.

am allowing exS to dissapear, dyna_menu can add it back. YMMV
thanks to the Leo and scriptButton creator for all the 
excess fun while working on this little set of toys.
[python developers] * thanks

do post a bug report or feature request
on my comment page from:
 http://rclick.netfirms.com/rCpython.htm
or sourceforge forum
"""
#@<< initilize >>
#@+node:ekr.20040916153817.67:<< initilize >>

import leoPlugins as lp
import leoGlobals as g
import sys

try: import Tkinter as Tk
except ImportError: Tk = None

#@+at
# 
# s04515p10:55:53 make a simple execute script button
# it works on the current selected text or body by default,
# same as always from the edit menu or rClick.
# script startup seeems a little slower when run from the button.
# wonder where the overhead is, have to do some actual test.
# 
# m04517a04:54:21 add to the plugin, solve can executescript on this node
#  or called from plugin. add status display/clear on enter/leave button
# wonder if dissapear on rclick is counterintunitive at this point?
# when run from plugin, button is far left. if dissapear then add
# its to the right of nodenavigator which is moved to far left.
# other stuff got added to the right. in no particular order, as I recall.
# glitch, when this node included under the common clone node,
#  reinstalled by default when run dynabutton or dynatester.
#  if I use the __version__ defined try then you wont be able to execute 
# script
# moved it out of common back to the plugin which has a choice to add exS
# t04525a01:06:35 Ive been playing fast and loose with instnace vars
# but what if there was already an eb? better make a more unique name
# and devise some way to call with a dict everything to setup a button
# might want to have more than one button but not duplicate the source.
# took care of the instance name anyway, rather made the caller responsible.
# might get an event or tag, keywords and should be using those
# 
# m04726a09:43:53 adding scrollbutton from faqs 508? and remove from dyna
# make its own plugin to compete w/scriptButton er, steal some ideas.
# rclick will pull down scrollbutton menu and alow it to either
# run from node or from memory. from node is really nice while working
# you can leave the edit curser where it is and just run
# but sometimes you want it to work ona particular node thats a problem too
# when you want to test you have to leave etc.
# would be nice if it could remember where you want to position while testing 
# or while using. all these could be seletable.
# 
# patched in DDElist from cookbook, now items can be user rearanged.
# problem is they get selected on drop unlike a regular listbox.
# have to solve that. rclick weird in it too it popsup but it doesnt select.
# havent implimented any of the items.
# looking for the best way to store code sections.
# added htmlize to dynamenu, frozen,
# better idea to make it a button w/dropdown options like exS
# seperate out common and put Scrolled and DDL in there
# what if the exS SB option was to parse the scripts __doc__
# for optparse options like that cookbook hack. and give standard
# rclick action of scrollmenu of dissapear and a listbox of option
# defaults specifyed in the doc? multiple choice.
# browse, #would popup file
# pick would be multiple choice for the operation
# dissapear, save defaults, restore defaults,
# {ifilename:
# default=c:/temp/tempfile.py,
# pick: (copybuffer, stdin, browse filename, node name enter}
# }
# {ofilename:
# default=stdout,
# pick: (copybuffer, stdout, browse filename, node name enter}
# }
# 
# 
# 
# 
# 
# for  Leo 4.2 there is a msg after script runs in purple
# maybe if script is named, or somehow detect if is 4.2
# and override that or change the color to the log bg color.
# 
# 
# other button ideas:
# add a gotolinenumber button to the statusbar
# 
# design a modebutton that changes its text & functions to the next one
#  from a list of text & functions. rclick to switch to next mode?
#  [('goto', gorolinenumber), ('exS', c.executescript), etc]
# 
# using a mode button, push/pull buffer. allow each add to add
#  a named or numbered seperate button. or an additional menu item
#   that is either push or pull. tooltip of the first n chars of its content.
#   if its labled push then its empty and you click it and it gets
#    the content of the copy buffer. now the lable is pull
#    you click it and the content is put into the copy buffer.
#    there could also be a swap at this point if that turns usefull.
# 
# selectall, paste, copy a general floating edit bar even w/standard icons.
# a save button would be used quite a bit
# 
# need a 2nd line on the toolbar, or another floating toolbar
# or a toolbar between the log and headlines
# smaller text and fonts by default in all buttons.
#@-at
#@-node:ekr.20040916153817.67:<< initilize >>
#@nl

def add_exSb(a, msg, *arg, **kwd):
    """your basic execute script enabler
    """
    #@    << callbacks >>
    #@+node:ekr.20040916153817.68:<< callbacks >>
    #at this point code from plugins isnt importable
    if g.os_path_join(g.app.loadDir, "..", "plugins") not in sys.path:
        sys.path.append(g.os_path_join(g.app.loadDir, "..", "plugins"))
    
    c = g.top()
    cf = c.frame
    
    try: 
        from dynacommon import ScrolledMenu, DDList
        #reload(dynacommon) #if modify common
    except ImportError: g.es('you have to copy dynacommon.py to plugins')
    
    def deleb(*ev): 
        eb = getattr(cf, a)
        eb.destroy()
        del eb
        delattr(cf, a)
        fmouse()()
    
    #alternative to lambda is return a call to subfunction
    #trick from pycon tile.py, is called while doing the bind
    #update the status bar on mouse Enter/Leave on the button
    def nmouse(cf= cf, msg= "exS execute script", *ev):
        def doit(*ev):   
            cf.clearStatusLine()
            cf.putStatusLine(msg)
            #self.statusFrame.after(100,self.updateStatusRowCol) 
        return doit
    
    def fmouse(cf= cf, msg= "", *ev):
        def doit(*ev):
            cf.clearStatusLine()
            cf.putStatusLine(msg)
        return doit
    #@nonl
    #@-node:ekr.20040916153817.68:<< callbacks >>
    #@nl

    #@    @+others
    #@+node:ekr.20040916153817.69:result
    def result(van):
        #should be able to get which, currently first letter
        #can we deduce the rest of the items text? last 2 chars?
        print 'selected:', van
        if van == 'd': deleb(None)
        elif van == 'm': print 'lets make a button'
    
    def popup(e):
        #should be able to update list first?
        eb.sm.popup(eb)
    #@nonl
    #@-node:ekr.20040916153817.69:result
    #@-others
    
    if not a: 
        #can it sense if name already taken and pick another?
        #can it sense if its the only one and not allow dissapear?
        a ='dynaExS'

    try:
        deleb(None)  #cleanup previous invocations of exS
    except Exception:
        pass
        

    setattr(cf, a, cf.addIconButton(text= "exS" ) )
    eb = getattr(cf, a)
    
    #you have to make the function call otherwise Tk passes an event
    #not sure why this isnt a problem in rClick
    
    eb.configure({'font':('verdana', 7, 'bold'), 'bg':'gold1',
        'command':(lambda c= c.executeScript: c()), })

    #use rclick to delete, it is annoying. what else should it do?. 
    #eb.bind('<3>', deleb )
    eb.sm = ScrolledMenu(result)
    apply(eb.sm.listbox.insert, (
           0, #leave 0 alone, first letter is the return value
          'make button',
          'toggle from node/mem',
          'edit exSB.ini',
          'find script',
          'dissapear',  #this implys someway to get it back
           ))
    eb.bind('<3>', popup)

    #announce on status if mouse enter/leave on/off.
    eb.bind('<Enter>', nmouse(cf))  
    eb.bind('<Leave>', fmouse(cf))  
    
    #AttributeError: Event instance has no __call__ method
    #cf.bodyCtrl.bind('<Alt-L2>', (lambda c= c.executeScript: c()) )

    g.es(msg)

#print '__name__ =', __name__  # __builtin__ when execscript
if __name__ != 'exSButton': add_exSb('dynaExS1', 'exS') #one extra

elif Tk:  #must be running as plugin
    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui and g.app.gui.guiName() == "tkinter":

        __version__ = '0.018'  #f04730p05:38:32 

        if sys.platform == 'win32':  #'after-create-leo-frame?', 
            lp.registerHandler(('open2', 'new'),
              add_exSb)
        else:
            lp.registerHandler(('start2', 'open2', "new"),
              add_exSb)

#@@language python
#@@color
#@nonl
#@-node:ekr.20040916153817.66:@thin exSButton.py
#@-leo
