#@+leo-ver=4-thin
#@+node:ekr.20040722142445:@thin editAttributes.py
"""A plugin to add and edit unknown attributes of a node

Summon it by pressing button-2 or button-3 on an icon Box in the outline."""

#@@language python
#@@tabwidth -4

#@<< editAttributes imports >>
#@+node:ekr.20040722142445.1:<< editAttributes imports >>
import leoGlobals as g
import leoPlugins

try:
    import Tkinter as Tk
except ImportError:
    g.es("editAttributes.py: can not import Tk",color="blue")
    Tk = None
    
try:
    import Pmw
except ImportError:
    g.es("editAttributes.py: can not import Pmw",color="blue")
    Tk = None

try:
    import weakref
except ImportError:
    g.es("editAttributes.py: can not import weakref",color="blue")
    weakref = None
#@nonl
#@-node:ekr.20040722142445.1:<< editAttributes imports >>
#@nl

#@+others
#@+node:ekr.20040722142445.2:addAttrDetection
def addAttrDetection( tag, keywords ):
    
    if keywords.has_key( 'c' ):
        c = keywords[ 'c' ]
    else:
        c = keywords[ 'new_c' ]
    if haveseen.has_key( c ): return

    haveseen[ c ] = None
    can = c.frame.canvas
    #@    << define hit callback >>
    #@+node:ekr.20040722143218:<< define hit callback >>
    def hit (event, c = c):
        
        # Modified for 4.2 code base.
        tree = c.frame.tree
        iddict = tree.iconIds # was tree.icon_id_dict
        can = event.widget
        x = can.canvasx( event.x )
        y = can.canvasy( event.y )
        olap = can.find_overlapping( x, y, x, y)
        
        # g.trace(olap,iddict.get(olap[0]))
            
        # EKR: search for the key.
        found = False
        for item in olap:
            if iddict.get(item):
                p,generation = iddict[item] # New in 4.2.
                found = True ; break
            
        if found:
            par = can.master
            can.pack_forget()
            
            if hasattr(p.v,'unknownAttributes' ):
                b = p.v.unknownAttributes
            else:
                b = p.v.unknownAttributes = {}
        
            v = p
            #@        << create widgets >>
            #@+node:ekr.20040722144601:<< create widgets >>
            f = Tk.Frame( par )
            l = Tk.Label(f, text = v.headString() )
            l.pack()
            f3 = Tk.Frame( f )
            f.pack()
            lb = Pmw.ScrolledListBox( f3 )
            lblb = lb.component( 'listbox' )
            lblb.configure( background = 'white', foreground = 'blue', selectbackground = '#FFE7C6', selectforeground = 'blue' )
            bk = b.keys()
            bk.sort()
            lb.setlist( bk )
            lb.pack( side = 'left' )
            tx = Tk.Text( f3, background = 'white', foreground = 'blue' )
            
            # define inner callbacks...
            #@+others
            #@+node:ekr.20040722143521.1:add
            def add():
            
                txt = e.get()
                if txt.strip() == '': return
                e.delete( 0, 'end' )
                b[ txt ] = ''
                bk = b.keys()
                bk.sort()
                lb.setlist( bk )
                lb.setvalue( txt )
                tx.delete( '1.0', 'end' )
            #@nonl
            #@-node:ekr.20040722143521.1:add
            #@+node:ekr.20040722143637:clz
            def clz():
            
                f.pack_forget()
                can.pack( expand = 1 , fill = 'both' )
                f.destroy()
            #@nonl
            #@-node:ekr.20040722143637:clz
            #@+node:ekr.20040722143521.2:rmv
            def rmv():
                
                cs = lb.curselection()
                if len( cs ) != 0 : cs = cs[ 0 ]
                else: return
                del b[ lb.get( cs ) ]
                bk = b.keys()
                bk.sort()
                lb.setlist( bk )
                tx.delete( '1.0', 'end' )
            #@-node:ekr.20040722143521.2:rmv
            #@+node:ekr.20040722143521:selcommand
            def selcommand():
            
                cs = lb.getcurselection()
                if len( cs ) != 0: cs = cs[ 0 ]
                else: return
                txt = b[ cs ]
                tx.delete( '1.0', 'end' )
                tx.insert( '1.0' ,txt)
            #@nonl
            #@-node:ekr.20040722143521:selcommand
            #@+node:ekr.20040722143218.2:setText
            def setText( event):
            
                if event.char == '': return
                cs = lb.getcurselection()
                if len( cs ) == 0: return
                cs = cs[ 0 ]
                txt = tx.get( '1.0', 'end -1c' )
                b[ cs ] = txt + event.char
            #@nonl
            #@-node:ekr.20040722143218.2:setText
            #@-others
            
            tx.bind( '<Key>', setText )
            tx.pack( side = 'right' )
            #
            lb.configure( selectioncommand = selcommand )
            f2 = Tk.Frame( f )
            f2.pack( side = 'bottom')
            f3.pack()
            e = Tk.Entry( f2 , background = 'white', foreground = 'blue' )
            e.pack( side = 'left')
            ba = Tk.Button( f2, text = 'Add' )
            #
            ba.configure( command = add )
            ba.pack( side = 'left' )
            br = Tk.Button( f2, text = 'Remove' )
            #
            br.configure( command = rmv )
            br.pack( side = 'left' )
            bu = Tk.Button( f2, text = 'Close' )
            #
            bu.configure( command = clz )
            bu.pack( side = 'right' )
            f.pack()
            #@nonl
            #@-node:ekr.20040722144601:<< create widgets >>
            #@nl
    #@nonl
    #@-node:ekr.20040722143218:<< define hit callback >>
    #@nl
    can.bind( '<Button-2>', hit, '+')
    can.bind( '<Button-3>', hit, '+') # EKR
#@nonl
#@-node:ekr.20040722142445.2:addAttrDetection
#@-others

haveseen = weakref.WeakKeyDictionary()

if Tk and Pmw and weakref and not g.app.unitTesting:
    leoPlugins.registerHandler('open2', addAttrDetection)
    __version__ = ".0.2"
        # 0.2 EKR: converted to outline.  Fixed some bugs.
    g.plugin_signon( __name__ )
#@nonl
#@-node:ekr.20040722142445:@thin editAttributes.py
#@-leo
