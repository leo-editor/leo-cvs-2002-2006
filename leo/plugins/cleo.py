#@+leo-ver=4-thin
#@+node:ekr.20050227071948.33:@thin cleo.py
#@<< docstring >>
#@+node:ekr.20050227071948.34:<< docstring >>
'''cleo.py  -- Coloured LEo Outlines

Cleo allows you to annotate or colour leo outlines based on priority, code
archetype, node types or some arbitary criteria. The annotations and colour
coding can play a similar role like that of syntax highlighting. Right-click on
the icon area to popup its menu to play with it.

Requires Leo 4.2a3 or greater, as it uses new drawing hooks.
'''
#@nonl
#@-node:ekr.20050227071948.34:<< docstring >>
#@nl

#@@language python
#@@tabwidth -4

#@<< imports >>
#@+node:ekr.20050227071948.35:<< imports >>
import leoGlobals as g
import leoPlugins
import leoTkinterTree

Tk = g.importExtension('Tkinter',pluginName=__name__,verbose=True)

import sys
#@nonl
#@-node:ekr.20050227071948.35:<< imports >>
#@nl
__version__ = "0.14"
#@<< version history >>
#@+node:ekr.20050227071948.36:<< version history >>
#@@killcolor

#@+at 
#@nonl
# Use and distribute under the same terms as leo itself.
# 
# Original code by Mark Ng <z3r0.00@gmail.com>
# 
# 0.5  Priority arrows and Archetype-based colouring of headline texts.
# 0.6  Arbitary headline colouring.
# 0.7  Colouring for node types. Added "Others" type option
# 0.8  Added "Clear Priority" option
# 0.8.1  Fixed popup location
# 0.8.2  Fixed unposting
# 0.9  Automatically colour @file and @ignore nodes
# 0.10 EKR:
# - Repackaged for leoPlugins.leo.
#     - Define g.  Eliminate from x import *.
# - Made code work with 4.3 code base:
#     - Override tree.setUnselectedHeadlineColors instead of 
# tree.setUnselectedLabelState
# - Create per-commander instances of cleoController in onCreate.
# - Converted some c/java style to python style.
# - Replaced string.find(s,...) by s.find(...) & removed import string.
# - show_menu now returns 'break':  fixes the 'popup menu is not unposting 
# bug)
# 0.11 EKR:
# - hasUD and getUD now make sure that the dict is actually a dict.
# 0.12 EKR:
# - Changed 'new_c' logic to 'c' logic.
# 0.13 EKR:
# - Installed patch roughly following code at 
# http://sourceforge.net/forum/message.php?msg_id=3517080
# - custom_colours now returns None for default.
# - Added override of setDisabledHeadlineColors so that color changes in 
# headlines happen immediately.
# - Removed checkmark menu item because there is no easy way to clear it.
# 0.14 EKR: Installed further patch to clear checkmark.
#@-at
#@nonl
#@-node:ekr.20050227071948.36:<< version history >>
#@nl

ok = Tk is not None
    
#@+others
#@+node:ekr.20050227071948.69:init
def init():

    if ok:
        leoPlugins.registerHandler(('open2',"new"),onCreate)
        g.plugin_signon(__name__)

    return ok
#@nonl
#@-node:ekr.20050227071948.69:init
#@+node:ekr.20050227085542:onCreate
def onCreate (tag,keywords):
    
    c = keywords.get('c')
    
    cc = cleoController(c)
    cc.install_drawing_overrides()
    
    leoPlugins.registerHandler("draw-outline-text-box",cc.draw)
    leoPlugins.registerHandler("iconrclick1",cc.show_menu)
#@nonl
#@-node:ekr.20050227085542:onCreate
#@+node:ekr.20050227071948.32:class TkPickleVar(Tk.Variable)
if ok: # Don't define this if import Tkinter failed.

    class TkPickleVar (Tk.Variable):
        
        def __setstate__(self,state):
            Tk.Variable.__init__(self)
            Tk.Variable.set(self,state)

        def __getstate__(self):
            p = Tk.Variable.get(self)
            # Beware of returning False!
            return p
#@nonl
#@-node:ekr.20050227071948.32:class TkPickleVar(Tk.Variable)
#@+node:ekr.20050227085542.1:class cleoController
class cleoController:
    
    '''A per-commander class that recolors outlines.'''
    
    #@    @+others
    #@+node:ekr.20050227085542.2: birth
    def __init__ (self,c):
        
        self.c = c
        self.menu = None
        self.donePriority = 100
        self.smiley = None
    
        # image ids should be a property of the node
        # use {marking,image id} as the kv pair.
        self.images = {}
        
        #@    << define colors >>
        #@+node:ekr.20050227085542.3:<< define colors >>
        self.colours = [
            'Black',
            'Brown', 'Purple', 'Red', 'Pink',
            'Yellow', 'Orange', 'Khaki', 'Gold'
            'DarkGreen', 'Green', 'OliveDrab2',
            'Blue', 'Lightblue', 'SteelBlue2',
            'White',
        ]
        
        self.archetype_colours = {
            'Data' : 'Purple',
            'Thing' : 'Green3',
            'Logic' : 'Blue',
            'Interface': 'DarkOrange',
            'Moment-Interval' : 'Red',
        }
        
        self.node_colours = {
            'file' : 'lightgreen',
            'Major Branch' : 'SandyBrown',
            'Feature' : 'peachpuff',
            'Comments': 'lightblue',
        }
        
        self.priority_colours = {
            1 : 'red',
            2 : 'orange',
            3 : 'yellow',
            4 : 'green',
            5 : 'background-colour'
        }
        
        self.background_colour = c.frame.tree.canvas.cget('background')
        #@nonl
        #@-node:ekr.20050227085542.3:<< define colors >>
        #@nl
    #@nonl
    #@+node:ekr.20050227071948.68:install_drawing_overrides
    def install_drawing_overrides (self):
        
        # print "Cleo plugin: installing overrides for",self.c.shortFileName()
    
        tree = self.c.frame.tree # NOT leoTkinterTree.leoTkinterTree
        
        g.funcToMethod(self.setUnselectedHeadlineColors,tree)
        g.funcToMethod(self.setDisabledHeadlineColors,tree)
    #@nonl
    #@-node:ekr.20050227071948.68:install_drawing_overrides
    #@-node:ekr.20050227085542.2: birth
    #@+node:ekr.20050227071948.38:attributes...
    #@+at
    # These methods should really be part of vnode in accordance with the 
    # principles
    # of encapsulation and information hiding.
    # 
    # annotate was the previous name of this plugin, which is why the default 
    # values
    # for several keyword args is 'annotate'.
    #@-at
    #@nonl
    #@+node:ekr.20050227074440:delUD
    def delUD (self,node,udict="annotate"):
    
        ''' Remove our dict from the node'''
    
        if hasattr(node,"unknownAttributes" ) and \
               node.unknownAttributes.has_key(udict):
    
            del node.unknownAttributes[udict]
    #@nonl
    #@-node:ekr.20050227074440:delUD
    #@+node:ekr.20050227074440.1:hasUD
    def hasUD (self,node,udict="annotate"):
    
        ''' Return True if the node has an UD.'''
        
        # g.trace(node) # EKR: node had better not be a position!
       
        return (
            hasattr(node,"unknownAttributes") and
            node.unknownAttributes.has_key(udict) and
            type(node.unknownAttributes.get(udict)) == type({}) # EKR
        )
    #@nonl
    #@-node:ekr.20050227074440.1:hasUD
    #@+node:ekr.20050227074440.2:getUD
    def getUD (self,node,udict="annotate"):
        
        ''' Create or retrive the user dict'''
    
        if not hasattr(node,'unknownAttributes'):
            node.unknownAttributes = {}
            
        # Create a subdictionary for the private use of my plugin.
        d = node.unknownAttributes.get(udict)
    
        if d is None or type(d) != type({}): # EKR
            node.unknownAttributes[udict] = d = {}
            
        return d
    #@nonl
    #@-node:ekr.20050227074440.2:getUD
    #@-node:ekr.20050227071948.38:attributes...
    #@+node:ekr.20050227071948.50:colours...
    #@+node:ekr.20050227071948.60:remove_colours
    def remove_colours(self,v):
        
        d = self.getUD(v)
        del d['fg']
        del d['bg']
        self.c.redraw()
    #@-node:ekr.20050227071948.60:remove_colours
    #@+node:ekr.20050227071948.61:custom_colours
    # use return values to set the colours so no need to muck around when loading up files.
    
    def custom_colours(self,v):
    
        ''' Returns the vnodes custom colours if it has them '''
        
        fg, bg = None, None
        d = self.getUD(v)
    
        # XXX This is ugly and inefficient !!
        #@    << auto headline colours >>
        #@+node:ekr.20050227071948.62:<< auto headline colours >>
        # set bg of @file type of nodes
        h = v.headString()
        
        for f in ["@file", "@thin", "@nosen", "@asis", "@root"]:
            if h.find(f, 0, 5) == 0:
                bg = self.node_colours['file']
        
        # set bg of @ignore type of nodes
        if h.find("@ignore") == 0:
            bg = self.node_colours['Comments']
        #@nonl
        #@-node:ekr.20050227071948.62:<< auto headline colours >>
        #@nl
        #@    << node colours >>
        #@+node:ekr.20050227071948.63:<< node colours >>
        # Node-based colouring --- bg only
        n = d.get('node')
        if n:
            bg = self.node_colours.get(n.get(), bg)
        #@nonl
        #@-node:ekr.20050227071948.63:<< node colours >>
        #@nl
        #@    << archetype colours >>
        #@+node:ekr.20050227071948.64:<< archetype colours >>
        # Archetype-based colouring --- fg only
        a = d.get('archetype')
        if a:
            fg = self.archetype_colours.get(a.get(), fg)
        #@nonl
        #@-node:ekr.20050227071948.64:<< archetype colours >>
        #@nl
        #@    << arbitary colours >>
        #@+node:ekr.20050227071948.65:<< arbitary colours >>
        # User defined colours overrides all
        fgv = d.get('fg')
        if fgv:
            f = fgv.get()
            if f:
                fg = f
        
        bgv = d.get('bg')
        if bgv:
            b = bgv.get()
            if b:
                bg = b
        #@nonl
        #@-node:ekr.20050227071948.65:<< arbitary colours >>
        #@nl
    
        #print "> (%s,%s) %s" % (fg,bg,v.headString())
        return fg,bg
    #@nonl
    #@-node:ekr.20050227071948.61:custom_colours
    #@-node:ekr.20050227071948.50:colours...
    #@+node:ekr.20050227100857:drawing...
    #@+node:ekr.20050227071948.39:redraw
    def redraw(self):
        
        c = self.c ; tree = c.frame.tree
        c.setChanged(True)
        c.redraw_now()
    #@nonl
    #@-node:ekr.20050227071948.39:redraw
    #@+node:ekr.20050227071948.37:clear_all
    def clear_all(self,v):
    
        self.delUD(v)
        self.redraw()
    #@nonl
    #@-node:ekr.20050227071948.37:clear_all
    #@+node:ekr.20050227071948.44:draw box area
    #@+node:ekr.20050227091634:draw
    def draw (self,tag,key):
    
        ''' Redraws all the indicators for the markups of v '''
    
        v = key['p'].v
    
        if not self.hasUD(v):
            # colour='white'
            # self.draw_arrow(v,colour)
            # self.draw_tick(v)
            return None
    
        d = self.getUD(v)
        if d.get('priority'):
            priority = d['priority'].get()
            colour = self.priority_colours.get(priority,False)
            if colour:
                self.draw_arrow(v,colour)
            if priority==self.donePriority:
                self.draw_tick(v)
    
        # Archetype are not drawn here
        return None 
    #@nonl
    #@-node:ekr.20050227091634:draw
    #@+node:ekr.20050227071948.45:draw_icon Not used
    if 0:# Not used
    
        c = self.c
        print "> Drawing:"
        print v 
    
        canvas = c.frame.tree.canvas 
        #draw_box(v, 'blue', canvas)
        draw_topT(v,'yellow',canvas)
    
        if not self.smiley:
            print "loading image"
            self.smiley = PhotoImage(file="/tmp/smile.gif")
        draw_icon(v,self.smiley,canvas)
        return None 
    
        def draw_icon (v,img,canvas):
            print canvas 
            global images 
            images[v] = canvas.create_image(v.iconx-9,v.icony,anchor=NW,image=img)
        
        def draw0 (tag,key):
            print "> Drawing:"
            print tag 
            print key 
            return None 
    #@-node:ekr.20050227071948.45:draw_icon Not used
    #@+node:ekr.20050227071948.46:draw_box
    def draw_box (self,v,color,canvas):
        
        if v.isVisible():
            x, y = v.iconx, v.icony 
            canvas.create_rectangle(x,y,x+10,y+10,fill=color)
    #@nonl
    #@-node:ekr.20050227071948.46:draw_box
    #@+node:ekr.20050227071948.47:draw_arrow
    # If too long can obscure +/- box
    
    def draw_arrow (self,v,colour='darkgreen'):
    
        # print ">> Action"
        c = self.c ; tree = c.frame.tree ; canvas = tree.canvas
        clear = colour == 'background-colour'
    
        if clear:
            colour = self.background_colour
    
        canvas.create_line(v.iconx-10,v.icony+8,v.iconx+5,v.icony+8,
            arrow = "last", fill = colour, width = 4)
    
        if clear:
            # canvas.create_line(v.iconx-10,v.icony+7,v.iconx+5,v.icony+7,
                # fill = 'Gray50',width=1)
    
            # Define the 3 points of a check mark to allow quick adjustment.
            XpointA = v.iconx-15 + 3
            YpointA = v.icony + 8-2
            XpointB = v.iconx-7
            YpointB = v.icony + 13
            XpointC = v.iconx + 5
            YpointC = v.icony-2
            # "white-out" the check mark.
            canvas.create_line(XpointA,YpointA,XpointB,YpointB,fill=colour,width=2)
            canvas.create_line(XpointB,YpointB,XpointC,YpointC,fill=colour,width=2)
            # restore line 
            canvas.create_line(v.iconx-12,v.icony+7,v.iconx+6,v.icony+7,fill='Gray50',width=1)
    #@nonl
    #@-node:ekr.20050227071948.47:draw_arrow
    #@+node:ekr.20050227071948.48:draw_tick
    def draw_tick (self,v,colour='salmon'):
    
        canvas = self.c.frame.tree.canvas
    
        # canvas.create_line(v.iconx+13-5,v.icony+8,v.iconx+13,v.icony+13,fill=colour,width=2)
        # canvas.create_line(v.iconx+13,v.icony+13,v.iconx+13+12,v.icony-2,fill=colour,width=2)
    
        # Define the 3 points of a check mark to allow quick adjustment.
        XpointA = v.iconx-15 + 3
        YpointA = v.icony + 8-2
        XpointB = v.iconx-7
        YpointB = v.icony + 13
        XpointC = v.iconx + 5
        YpointC = v.icony-2
        # draw the check-mark
        canvas.create_line(XpointA,YpointA,XpointB,YpointB,fill=colour,width=2)
        canvas.create_line(XpointB,YpointB,XpointC,YpointC,fill=colour,width=2)
    #@nonl
    #@-node:ekr.20050227071948.48:draw_tick
    #@+node:ekr.20050227074440.3:draw_invertedT
    def draw_invertedT (self,v,color,canvas):
        
        '''Draw the symbol for data.'''
    
        if v.isVisible():
    
            x, y = v.iconx, v.icony ; bottom = y+13
            
            # Draw horizontal line.
            canvas.create_line(x,bottom,x+10,bottom,fill=color,width=2)
            
            # Draw vertical line.
            canvas.create_line(x+5,bottom-5,x+5,bottom,fill=color,width=2)
    #@nonl
    #@-node:ekr.20050227074440.3:draw_invertedT
    #@+node:ekr.20050227074440.4:draw_topT
    def draw_topT (self,v,color,canvas):
        
        '''Draw the symbol for interfaces.'''
        
        if v.isVisible():
    
            x, y = v.iconx, v.icony ; topl = y 
    
            # Draw the horizontal line.
            canvas.create_line(x,topl,x+10,topl,fill=color,width=2)
    
            # Draw the vertical line.
            canvas.create_line(x+5,topl,x+5,topl+15,fill=color,width=2)
    #@nonl
    #@-node:ekr.20050227074440.4:draw_topT
    #@-node:ekr.20050227071948.44:draw box area
    #@+node:ekr.20050227081640:overrides of leoTkinterTree methods
    #@+node:ekr.20050227081640.8:setUnselectedHeadlineColors
    def setUnselectedHeadlineColors (self,p):
    
        c = self.c ; w = p.edit_widget()
    
        fg, bg = self.custom_colours(p.v)
    
        fg = fg or c.config.getColor("headline_text_unselected_foreground_color") or 'black'
        bg = bg or c.config.getColor("headline_text_unselected_background_color") or 'white'
    
        try:
            w.configure(state="disabled",highlightthickness=0,fg=fg,bg=bg)
        except:
            g.es_exception()
    #@nonl
    #@-node:ekr.20050227081640.8:setUnselectedHeadlineColors
    #@+node:ekr.20060112060601:setDisabledHeadlineColors
    def setDisabledHeadlineColors (self,p):
    
        c = self.c ; w = p.edit_widget()
    
        fg, bg = self.custom_colours(p.v)
    
        fg = fg or c.config.getColor("headline_text_selected_foreground_color") or 'black'
        bg = bg or c.config.getColor("headline_text_selected_background_color") or 'grey80'
    
        try:
            w.configure(state="disabled",highlightthickness=0,fg=fg,bg=bg)
        except:
            g.es_exception()
    #@nonl
    #@-node:ekr.20060112060601:setDisabledHeadlineColors
    #@-node:ekr.20050227081640:overrides of leoTkinterTree methods
    #@-node:ekr.20050227100857:drawing...
    #@+node:ekr.20050227100643:menus...
    #@+node:ekr.20050227071948.53:archetype_menu
    def archetype_menu(self,parent,p):
    
        d = self.getUD(p.v)
        if d.has_key('archetype'):
            a = d['archetype']
        else:
            d['archetype'] = a = TkPickleVar()
    
        menu = Tk.Menu(parent,tearoff=0,takefocus=1)
    
        for label,value in (
            ('Data/Description','Data'),
            ('Thing/Place','Thing'),
            ('Logic/Function','Logic'),
            ('Interface/Role','Interface'),
            ('Moment-Interval/Event Handler','Moment-Interval'),
            ('Other','Other'),
        ):
            menu.add_radiobutton(label=label,
                underline=0,command=self.redraw,
                variable=a,value=value)
        
        parent.add_cascade(label='Code Archetypes',underline=6,menu=menu)
    
        return menu
    #@nonl
    #@-node:ekr.20050227071948.53:archetype_menu
    #@+node:ekr.20050227071948.59:colours_menu
    def colours_menu(self,parent, p):
        
        d = self.getUD(p.v)
        if d.has_key('fg'):
            fg = d['fg']
        else:
            d['fg'] = fg = TkPickleVar()
    
        if d.has_key('bg'):
            bg = d['bg']
        else:
            d['bg'] = bg = TkPickleVar()
    
        # Radio buttons don't look that good. 
        for label,var in (('Foreground',fg),('Background',bg)):
            menu = Tk.Menu(parent,tearoff=0,takefocus=1)
            for color in self.colours:
                menu.add_radiobutton(label=color,
                    variable=var, value=color,
                    command=self.redraw)
            parent.add_cascade(label=label,underline=0,menu=menu)
                        
        def cleoColorsMenuCallback():
            self.remove_colours(p.v)
    
        parent.add_command(label='Remove Colouring', underline=0,
            command=cleoColorsMenuCallback)
    #@nonl
    #@-node:ekr.20050227071948.59:colours_menu
    #@+node:ekr.20050227071948.56:node menu
    def nodes_menu(self,parent,p):
    
        d = self.getUD(p.v)
    
        if d.has_key('node'):
            n = d['node']
        else:
            d['node'] = n = TkPickleVar()
    
        menu = Tk.Menu(parent,tearoff=0,takefocus=1)
        
        for label,value in (
            ('@file','file'),
            ('Major Branch','Major Branch'),
            ('Feature/Concern','Feature'),
            ('Comments/@ignore','Comments'),
            ('Other','Other'),
        ):
            menu.add_radiobutton(label=label,underline=0,
                command=self.redraw,variable=n,value=value)
    
        parent.add_cascade(label='Node types',underline=0,menu=menu)
    #@nonl
    #@-node:ekr.20050227071948.56:node menu
    #@+node:ekr.20050227071948.41:priority_menu
    def priority_menu(self,parent,p):
    
        d = self.getUD(p.v)
        if d.has_key('priority'):
            pr = d['priority']
        else:
            d['priority'] = pr = TkPickleVar()
            pr.set(9999)
    
        menu = Tk.Menu(parent,tearoff=0,takefocus=1)
    
        parent.add_cascade(label='Priority', menu=menu,underline=1)
    
        # Instead of just redraw, set changed too.
        for value,label in (
            (1,'Very High'),
            (2,'High'),
            (3,'Medium'),
            (4,'Low',),
            (5,'None',),
            (self.donePriority,'Done'),
        ):
            s = '%d %s' % (value,label)
            menu.add_radiobutton(
                label=s,variable=pr,value=value,
                command=self.redraw,underline=0)
    
        menu.add_separator()
    
        menu.add_command(label='Clear',
            command=lambda p=p:self.priority_clear(p.v),underline=0)
    
        return menu
    #@nonl
    #@-node:ekr.20050227071948.41:priority_menu
    #@+node:ekr.20050227071948.26:show_menu
    def show_menu (self,tag,k):
    
        if self.menu:
            # Destroy any previous popup.
            self.menu.unpost()
            self.menu.destroy()
            
        p = k['p']
        v = k['p'].v ## EKR
        event = k['event']
        d = self.getUD(v)
        
        # Create the menu.
        self.menu = menu = Tk.Menu(None,tearoff=0,takefocus=0)
        self.priority_menu(menu,p)
        self.archetype_menu(menu, p)
        self.nodes_menu(menu,p)
        menu.add_separator()
        self.colours_menu(menu,p)
        # fonts_menu(menu,p)
        menu.add_separator()
        menu.add_command(label='Clear All',
            underline=0,command=lambda:self.clear_all(v))
        
        # Show the menu.
        menu.post(event.x_root,event.y_root)
        
        return 'break' # EKR: Prevent other right clicks.
    #@nonl
    #@-node:ekr.20050227071948.26:show_menu
    #@-node:ekr.20050227100643:menus...
    #@+node:ekr.20050227071948.43:priority_clear
    def priority_clear(self,v):
        
        g.trace(v)
    
        d = self.getUD(v)
        del d['priority']
        self.redraw()
    #@nonl
    #@-node:ekr.20050227071948.43:priority_clear
    #@-others
#@nonl
#@-node:ekr.20050227085542.1:class cleoController
#@-others
#@nonl
#@-node:ekr.20050227071948.33:@thin cleo.py
#@-leo
