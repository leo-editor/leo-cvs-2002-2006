#@+leo-ver=4-thin
#@+node:EKR.20040609213754:@thin Configurator.py
# This is not a plugin.

#@@language python
#@@tabwidth -4

#@<< imports >>
#@+node:ekr.20041019075507:<< imports >>
import leoGlobals as g

try:
    import Tkinter as Tk
except ImportError:
    Tk = g.cantImport("Tk",__name__)

try:
    import Pmw as Pmw
except ImportError:
    Pmw = g.cantImport("Pmw",__name__)

import sys
import ConfigParser as cp
import sets
import os
#@-node:ekr.20041019075507:<< imports >>
#@nl

#@+others
#@+node:EKR.20040609213754.1:createFrame
def createFrame():
    c = g.top() ; dirties = {}
    #@    << create the top-level frame >>
    #@+node:ekr.20041114120827.1:<< create the top-level frame >>
    top = c.frame.top # g.app.root # Tk.Tk()
    
    tlf = Tk.Frame( top )
    tlf.pack( side = 'bottom' )
    
    b = Tk.Button( tlf, text = 'Save' )
    b.pack( side = 'left' )
    
    def quit(event=None,top=top):
        top.destroy()
        # sys.exit
    
    b2 = Tk.Button( tlf ,text = 'Quit' ,command = quit)
    b2.pack( side = 'right' )
    
    Pmw.initialise( top )
    nb = Pmw.NoteBook( top )
    nb.pack( fill = 'both', expand = 1 )
    #@nonl
    #@-node:ekr.20041114120827.1:<< create the top-level frame >>
    #@nl
    cfp = cp.ConfigParser()
    cfp.read(fileName)
    #@    << define the save callback >>
    #@+node:ekr.20041114120827.2:<< define the save callback >>
    def save():
    
        for d in dirties:
            s = dirties[ d ]
            for sd in s:
                l = sd.component( 'label' )
                lt = l.cget( 'text' )
                cfp.set( d, lt, sd.getvalue() )
    
        config = file(fileName,'w')
        cfp.write( config)
        config.close()
    #@nonl
    #@-node:ekr.20041114120827.2:<< define the save callback >>
    #@nl
    b.configure( command = save )
    for z in cfp.sections():
        i = nb.add( z )
        sf = Pmw.ScrolledFrame( i )
        sf.pack( fill = 'both', expand = 1 )
        c = sf.interior()
        dirties[ z ] = sets.Set()
        opts = cfp.options( z )
        opts.sort()
        for x in opts:
            val = cfp.get( z, x )
            ef = Pmw.EntryField( c , labelpos = 'w', label_text = x, value = val )
            ef.component( 'entry' ).configure(background='white',foreground= 'blue')
            def markAsDirty( section = z, ef = ef):
                s = dirties[ section ]
                s.add( ef )
            ef.configure( modifiedcommand = markAsDirty )
            ef.pack( side = 'top', fill = 'x', expand = 1 )

    return top
#@nonl
#@-node:EKR.20040609213754.1:createFrame
#@-others

if Tk and Pmw and not g.app.unitTesting:

    fileName = g.os_path_join(g.app.loadDir,"..","config","leoConfig.txt")
    
    if os.path.exists(fileName):
        top = createFrame()
        top.geometry('%sx%s+0+0' % ( top.winfo_screenwidth(), top.winfo_screenheight()-100 ) )
        top.deiconify()
        top.title(fileName)
        top.mainloop()
#@nonl
#@-node:EKR.20040609213754:@thin Configurator.py
#@-leo
