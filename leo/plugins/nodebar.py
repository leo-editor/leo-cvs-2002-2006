#@+leo-ver=4-thin
#@+node:mork.20041022155742.1:@thin nodebar.py
'''Adds buttons at the bottom of the tree canvas.

The buttons correspond to commands found in the Outline commands. It is intended
to speed up a new users ability to use the outline. Experienced users may find
value in being able to quickly execute commands they do not use very often.
'''

#@<< imports >>
#@+node:ekr.20041024093652:<< imports >>
import leoGlobals as g
import leoPlugins

load_ok=True
try:
    import Pmw
    import weakref
    import Tkinter as Tk
except Exception, x:
    g.es( 'Could not load because of %s' % x )
    load_ok = False
#@nonl
#@-node:ekr.20041024093652:<< imports >>
#@nl
#@<< images  >>
#@+node:mork.20041022160850:<<images>>
nodeup = r'''R0lGODlhEAAQAIABAENMzf///yH+FUNyZWF0ZWQgd2l0aCBUaGUgR0lNUAAsAAAAABAAEAAAAhqM
j6nL7QDcgVBS2u5dWqfeTWA4lqYnpeqqFgA7'''

nodeupPI = Tk.PhotoImage( data = nodeup )

nodedown = r'''R0lGODlhEAAQAIABAENMzf///yH+FUNyZWF0ZWQgd2l0aCBUaGUgR0lNUAAsAAAAABAAEAAAAhuM
j6nL7Q2inLTaGW49Wqa+XBD1YE8GnOrKBgUAOw=='''

nodedownPI = Tk.PhotoImage( data = nodedown )

nodeleft = r'''R0lGODlhEAAQAIABAENMzf///yH+FUNyZWF0ZWQgd2l0aCBUaGUgR0lNUAAsAAAAABAAEAAAAiOM
jwDIqd3Ug0dOam/MC3JdfR0jjuRHBWjKpUbmvlIsm65WAAA7'''

nodeleftPI = Tk.PhotoImage( data = nodeleft )

noderight = r'''R0lGODlhEAAQAIABAENMzf///yH+FUNyZWF0ZWQgd2l0aCBUaGUgR0lNUAAsAAAAABAAEAAAAiGM
A3DLltrag/FMWi+WuiK9WWD4gdGYdenklUnrwqX8tQUAOw=='''

noderightPI = Tk.PhotoImage( data = noderight )

clone = r'''R0lGODlhEAAQAIABAP8AAP///yH+FUNyZWF0ZWQgd2l0aCBUaGUgR0lNUAAsAAAAABAAEAAAAhaM
j6nL7Q8jBDRWG8DThjvqSeJIlkgBADs='''

clonePI = Tk.PhotoImage( data = clone )

copy = r'''R0lGODlhEAAQAIAAAENMzf///yH+FUNyZWF0ZWQgd2l0aCBUaGUgR0lNUAAsAAAAABAAEAAAAh2M
j6nLBg8bnOw1ZO/JOnD9XaEEdFtpetOIrem7FAA7'''

copy3 = r'''R0lGODlhEAAQAMIEAAAAAI9pLOcxcaCclf///////////////ywAAAAAEAAQAAADLEi63P5vSLiC
vYHiq6+wXSB8mQKcJ2GNLAssr0fCaOyB0IY/ekn9wKBwSEgAADs='''

copy3PI = Tk.PhotoImage( data = copy3 )

cut = r'''R0lGODlhEAAQAIABAOcxcf/9/SH+FUNyZWF0ZWQgd2l0aCBUaGUgR0lNUAAsAAAAABAAEAAAAh2M
j6nLBg8bnOw1ZO/JOnD9XaEEdFtpetOIrem7FAA7'''

cutPI = Tk.PhotoImage( data = cut )

cut2 = r'''R0lGODlhEAAQAKECAAAAAKCclf///////yH+FUNyZWF0ZWQgd2l0aCBUaGUgR0lNUAAsAAAAABAA
EAAAAiaUDad7yS8cnDNYi4A0t7vNaCLTXR/ZZSBFrZMLbaIWzhLczCxTAAA7'''

cut2PI = Tk.PhotoImage( data = cut2 )

delete = r'''R0lGODlhEAAQAIABAOcxcf/9/SwAAAAAEAAQAAACJoyPacDNupyD7cxUbdYAP7RFHfhx3miSqHi2
qroG2wVLlFRCelIAADs='''

deletePI = Tk.PhotoImage( data = delete )

copyPI = Tk.PhotoImage( data = copy )

paste = r'''R0lGODlhEAAQAIABAENMzf///ywAAAAAEAAQAAACJIyPecDt6iJLU4VqMAVId76AkHiR3yc1W2qW
luW9rnzSoY0nBQA7'''

pastePI = Tk.PhotoImage( data = paste )

paste2 = r'''R0lGODlhEAAQAKECAAAAAB89vP///////yH+FUNyZWF0ZWQgd2l0aCBUaGUgR0lNUAAsAAAAABAA
EAAAAiOUH3nLktHYm9HMV92FWfPugQcgjqVBnmm5dsD7gmsbwfEZFQA7'''

paste2PI = Tk.PhotoImage( data = paste2 )


insert = r'''R0lGODlhEAAQAIABAENMzf///yH+FUNyZWF0ZWQgd2l0aCBUaGUgR0lNUAAsAAAAABAAEAAAAiCM
j3nA7YyeBGrRqiBOelsfXWDQgaV3bim2GtMTvq1XAAA7'''

insertPI = Tk.PhotoImage( data = insert )

insert2 = r'''R0lGODlhEAAQAKECAAAAAB89vP///////ywAAAAAEAAQAAACKJRhqSvIDGJ8yjWa5MQ5BX4JwXdo
3RiYRyeSjRqKmGZRVv3Q4M73VAEAOw=='''

insert2PI = Tk.PhotoImage( data = insert2 )

demote = r'''R0lGODlhEAAQAKECACMj3ucxcf///////yH+FUNyZWF0ZWQgd2l0aCBUaGUgR0lNUAAsAAAAABAA
EAAAAiiUj2nBrNniW+G4eSmulqssgAgoduYWeZ+kANPkCsBM1/abxLih70gBADs='''

demotePI = Tk.PhotoImage( data = demote )

promote = r'''R0lGODlhEAAQAKECACMj3ucxcf///////yH+FUNyZWF0ZWQgd2l0aCBUaGUgR0lNUAAsAAAAABAA
EAAAAiWUj6kX7cvcgy1CUU1ecvJ+YUGIbKSJAAlqqGQLxPI8t29650YBADs='''

promotePI = Tk.PhotoImage( data = promote )

pasteclone = r'''R0lGODlhEAAQAKEDACMj3v8AAP/9/f///ywAAAAAEAAQAAACOJSPaTPgoxBzgEVDM4yZbtU91/R8
ClkJzGqp7MK21rcG9tYedSCb7sDjwRLAGs7HsPF8khjzcigAADs='''

pasteclonePI = Tk.PhotoImage( data = pasteclone )

hoist = r'''R0lGODlhEAAQAKECAAAAAENMzf/9/f/9/SwAAAAAEAAQAAACI5SPaRCtypp7S9rw4sVwzwQYW4ZY
JAWhqYqE7OG+QvzSrI0WADs='''

hoistPI = Tk.PhotoImage( data = hoist )

dehoist = r'''R0lGODlhEAAQAKECAAAAACMj3v/9/f/9/SH+FUNyZWF0ZWQgd2l0aCBUaGUgR0lNUAAsAAAAABAA
EAAAAiOUj6lrwOteivLQKi4LXCcOegJIBmIZLminklbLISIzQ9hbAAA7'''

dehoistPI = Tk.PhotoImage( data = dehoist )

question = r'''R0lGODlhEAAQAIABAENMzf/9/SwAAAAAEAAQAAACJYwNqXAdC91LTlXbaMZH9/VJE+ZdpYicKIem
TPu98Cyxrb2qQQEAOw=='''

sortchildren = r'''R0lGODlhEAAQAKECAAAAAB89vP/9/f/9/SwAAAAAEAAQAAACJJSPKcGt2NwzbKpqYcg68oN9ITde
UQCkKgCeCvutsDXPk/wlBQA7'''

sortchildrenPI = Tk.PhotoImage( data = sortchildren )

sortsiblings = r'''R0lGODlhEAAQAKECAAAAAB89vP/9/f/9/SH+FUNyZWF0ZWQgd2l0aCBUaGUgR0lNUAAsAAAAABAA
EAAAAiWUFalxbatcS7IiZh3NE2L+fOAGXpknal4JlAIAw2Br0Fksu1YBADs='''

sortsiblingsPI = Tk.PhotoImage( data = sortsiblings )

questionPI = Tk.PhotoImage( data = question )

paint = r'''R0lGODlhEAAQAMIEAAAAAI9pLMOZVufHlf/9/f/9/f/9/f/9/SwAAAAAEAAQAAADNEi60LAwhhmi
Je5dSOtmzrd0opJ9Qqqu1uoK7atawwDUtz3Qen/zueAugivqgMYf0VdcJAAAOw=='''

paintPI = Tk.PhotoImage( data = paint )

trash = r'''R0lGODlhEAAQAMIEAAAAAB89vKCclbq3sv///////////////yH+FUNyZWF0ZWQgd2l0aCBUaGUg
R0lNUAAsAAAAABAAEAAAAzJIutwKELoGVp02Xmy5294zDSSlBAupMleAEhoYuahaOq4yCPswvYQe
LyT0eYpEW8iRAAA7'''

trashPI = Tk.PhotoImage( data = trash )
#@nonl
#@-node:mork.20041022160850:<<images>>
#@nl
__version__ = ".2"
#@<< version >>
#@+node:mork.20041023091529:<<version>>
#@+at
# .1 made initial icons
# 
# .15 eliminated most of the letter icons, made them node based icons.
# 
# .2 EKR:
#     - Fixed hang when help dialog selected.
#     - Write help string to status area on mouse over.
#     - Added test for if g.app.gui.guiName() == "tkinter"
#@-at
#@nonl
#@-node:mork.20041023091529:<<version>>
#@nl

#@+others
#@+node:mork.20041022160305:addNodeBar
haveseen = weakref.WeakKeyDictionary()

def addNodeBar( tag, keywords ):
    c = keywords.get( 'c' ) or keywords.get( 'new_c' )
    if not c: return
    if haveseen.has_key( c ): return
    haveseen[ c ] = None
    frame = c.frame.split2Pane1
    mbox = Tk.Frame( frame )
    mbox.pack( side = 'bottom' )
    bcommands = ( 
      ( c.moveOutlineUp, nodeupPI, 'Move Node Up' ),
      ( c.moveOutlineDown, nodedownPI , 'Move Node Down' ),
      ( c.moveOutlineLeft, nodeleftPI , 'Move Node Left' ),
      ( c.moveOutlineRight, noderightPI, 'Move Node Right' ),
      ( c.clone, clonePI , 'Clone Node' ),
      ( c.copyOutline, copy3PI, 'Copy Node' ),
      ( c.cutOutline, cut2PI, 'Cut Node' ),
      ( c.deleteOutline, trashPI, 'Delete Node' ),
      ( c.pasteOutline, paste2PI , 'Paste Node' ),
      ( c.pasteOutlineRetainingClones, pasteclonePI, 'Paste Retaining Clones' ),
      ( c.insertHeadline, insert2PI, 'Insert Node' ),
      ( c.demote, demotePI, 'Demote' ),
      ( c.promote, promotePI , 'Promote' ) ,
      ( c.hoist, hoistPI, 'Hoist'),
      ( c.dehoist, dehoistPI, 'De-Hoist' ),
      ( c.sortChildren, sortchildrenPI, 'Sort Children' ),
      ( c.sortSiblings, sortsiblingsPI, 'Sort Siblings' ),
    )
    for command,image,label in bcommands:
        add (c,mbox,command,image,label)
        
    #@    << Create the help button >>
    #@+node:ekr.20041024095639:<< Create the help button >>
    ques = Tk.Button( mbox, image = questionPI, command = lambda items = bcommands: help(c,items) )    
    ques.pack( side = 'right' )
    
    def callback(event,c=c,):
        c.frame.clearStatusLine()
        c.frame.putStatusLine("Open Help Dialog")
    
    ques.bind("<Enter>",callback)
    #@nonl
    #@-node:ekr.20041024095639:<< Create the help button >>
    #@nl
#@nonl
#@-node:mork.20041022160305:addNodeBar
#@+node:mork.20041022172156:add
def add(c, frame, command, image, label):
    
    b = Tk.Button( frame, command = command, image = image )
    b.pack( side = 'left' )
    
    def callback(event,c=c,s=label):
        c.frame.clearStatusLine()
        c.frame.putStatusLine(s)
    
    b.bind("<Enter>",callback)
#@nonl
#@-node:mork.20041022172156:add
#@+node:mork.20041022175619:help
def help(c, items):
    
    dialog = Pmw.Dialog(c.frame.top,title = 'Button Help' )
    sf = Pmw.ScrolledFrame( dialog.interior() )
    
    sf.pack()
    sfi = sf.interior()

    for z in items:
        lw = Pmw.LabeledWidget( sfi , labelpos = 'e', label_text = z[ 2 ] )
        l = Tk.Button( lw.interior() , image = z[ 1 ] )
        lw.pack()
        l.pack()

    dialog.activate()
#@nonl
#@-node:mork.20041022175619:help
#@-others

if load_ok:
    
    if g.app.gui is None: 
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":
        leoPlugins.registerHandler( ('start2' , 'open2', "new") , addNodeBar )
        g.plugin_signon( __name__ )
#@nonl
#@-node:mork.20041022155742.1:@thin nodebar.py
#@-leo
