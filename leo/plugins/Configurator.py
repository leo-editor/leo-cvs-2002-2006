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

if Tk and Pmw and not g.app.unitTesting:

    if 1: # Standalone doesn't work well
        fileName = r"c:\prog\leoCVS\leo\config\leoConfig.txt"
    else:
        if len( sys.argv ) < 2 or not os.path.exists( sys.argv[ 1 ] ):
            sys.exit( 0 )
        fileName = sys.argv[1]
    
    if os.path.exists(fileName):
        #@        << create the top frame tl and its contents >>
        #@+node:EKR.20040609213754.1:<< create the top frame tl and its contents >>
        tl = Tk.Tk()
        tlf = Tk.Frame( tl )
        tlf.pack( side = 'bottom' )
        b = Tk.Button( tlf, text = 'Save' )
        b.pack( side = 'left' )
        b2 = Tk.Button( tlf ,text = 'Quit' , command = sys.exit ) 
        b2.pack( side = 'right' )
        Pmw.initialise( tl )
        nb = Pmw.NoteBook( tl )
        nb.pack( fill = 'both', expand = 1 )
        cfp = cp.ConfigParser()
        cfp.read(fileName) # sys.argv[ 1 ] )
        dirties = {}
        def save():
            for d in dirties:
                s = dirties[ d ]
                for sd in s:
                    l = sd.component( 'label' )
                    lt = l.cget( 'text' )
                    cfp.set( d, lt, sd.getvalue() )
            config = file(fileName,'w') # sys.argv[ 1 ], 'w' )
            cfp.write( config)
            config.close()
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
        #@nonl
        #@-node:EKR.20040609213754.1:<< create the top frame tl and its contents >>
        #@nl
        tl.geometry('%sx%s+0+0' % ( tl.winfo_screenwidth(), tl.winfo_screenheight()-100 ) )
        tl.deiconify()
        tl.title(fileName)
        tl.mainloop()
#@nonl
#@-node:EKR.20040609213754:@thin Configurator.py
#@-leo
