#@+leo-ver=4-thin
#@+node:mork.20041013092542.1:@thin usetemacs.py
'''A Leo plugin that patches the temacs modules Emacs emulation
into the standard Leo Tkinter Text editor.

It is recommended that the user of usetemacs rebinds any conflicting keystrokes
in leoConfig.txt, for example: Ctrl-s is incremental search forward but also
default Save in Leo.

Emacian Search and Replace use the Find panels search and replace Text widgets.
This cuts down on the efficiency of the keystrokes and may be replaced in future
iterations.'''

#@@language python
#@@tabwidth -4

#@<< imports >>
#@+node:mork.20041013092542.2:<< imports >>
import leoGlobals as g
import leoPlugins
import Tkinter as Tk
import Pmw
import os.path
import os
import weakref
import sys
try:
    pth = os.path.split( g.app.loadDir ) 
    ppath = pth[ 0 ] + os.sep + 'plugins'
    sys.path.append( ppath )
    temacs = __import__( 'temacs', globals(), locals())
except Exception, x:
    g.es( "temacs not loadable. Aborting load of usetemacs because of: " + str( x ))
    temacs = None
import leoTkinterFrame

#@-node:mork.20041013092542.2:<< imports >>
#@nl
__version__ = '.5'
#@<< version history >>
#@+node:ekr.20041028162818:<< version history >>
#@+at
# 
# 0.3: Original from Leo User
# 0.4 EKR: Style changes.
#@-at
#@nonl
#@-node:ekr.20041028162818:<< version history >>
#@nl

haveseen = weakref.WeakKeyDictionary()
labels = weakref.WeakKeyDictionary()

#@+others
#@+node:mork.20041013092542.3:utTailEnd
def utTailEnd( buffer ):
    
    buffer.event_generate( '<Key>' )
    buffer.update_idletasks()
    return 'break'
#@-node:mork.20041013092542.3:utTailEnd
#@+node:mork.20041013092542.6:seeHelp
def seeHelp():
    
    tl = Tk.Toplevel()
    tl.title( "Temacs Help" )
    def clz( tl = tl ):
        tl.withdraw()
        tl.destroy()
    b = Tk.Button( tl, text = 'Close' , command = clz )
    b.pack( side = 'bottom' )
    fixedFont = Pmw.logicalfont( 'Fixed' )
    t = Pmw.ScrolledText( tl ,
        text_font = fixedFont ,
        text_background = 'white',
        hscrollmode = 'static',
        text_wrap='none')
    t.pack( expand = 1, fill = 'both')
    t.settext( temacs.getHelpText() )
#@-node:mork.20041013092542.6:seeHelp
#@+node:mork.20041013092542.5:addMenu
def addMenu( tag, keywords ):

    c = g.top()
    if haveseen.has_key( c ):
        return

    haveseen[ c ] = None
    men = c.frame.menu
    men = men.getMenu( 'Help' )
    men.add_separator()
    men.add_command( label = 'Temacs Help', command = seeHelp )
#@nonl
#@-node:mork.20041013092542.5:addMenu
#@-others

if temacs:
    if g.app.gui is None: 
        g.app.createTkGui(__file__)
    if g.app.gui.guiName() == "tkinter":
        olBindings = leoTkinterFrame.leoTkinterBody.createBindings
        #@        << define createBindings callback >>
        #@+node:ekr.20041028084650:<< define createBindings callback >>
        def createBindings (self,frame):
        
            olBindings(self,frame )
        
            #stext = lambda : g.app.findFrame.find_text.get( '1.0', 'end').rstrip( '\n' )
            #rtext = lambda : g.app.findFrame.change_text.get( '1.0', 'end' ).rstrip( '\n' )
        
            if not labels.has_key(frame ):
                group = Pmw.Group(frame.split2Pane2, tag_text = 'mini buffer' )
                group.pack( side = 'bottom', fill='x' )
                for z in frame.split2Pane2.children.values():
                    group.pack_configure( before = z )
                label = Tk.Label( group.interior() )
                label.pack( fill = 'both', expand = 1 )   
                labels[ frame ] = label  
            else:
                label = labels[ frame ]
        
            temacs.setBufferStrokes( frame.bodyCtrl, label )
            temacs.setUndoer( frame.bodyCtrl, self.c.undoer.undo ) 
            temacs.setTailEnd( frame.bodyCtrl, utTailEnd )
        #@nonl
        #@-node:ekr.20041028084650:<< define createBindings callback >>
        #@nl
        leoTkinterFrame.leoTkinterBody.createBindings = createBindings
        g.plugin_signon(__name__)
        leoPlugins.registerHandler(('start2','open2',"new"), addMenu )
        if temacs:
            #@            << load macros >>
            #@+node:ekr.20041028084650.1:<< load macros >>
            pth = os.path.split( g.app.loadDir ) 
            aini = pth[ 0 ] + os.sep + 'plugins' + os.sep
            if os.path.exists( aini + r'usetemacs.kbd' ):
                f = file( aini +  r'usetemacs.kbd', 'r' )
                temacs._loadMacros( f )
            if os.path.exists( aini + r'usetemacs.abv' ):
                f = file( aini + r'usetemacs.abv', 'r' )
                temacs._readAbbrevs( f )
            #@nonl
            #@-node:ekr.20041028084650.1:<< load macros >>
            #@nl
#@nonl
#@-node:mork.20041013092542.1:@thin usetemacs.py
#@-leo
