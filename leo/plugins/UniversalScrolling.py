#@+leo-ver=4-thin
#@+node:ekr.20040831122004:@thin UniversalScrolling.py
"""
A plugin that enables the user to scroll down with a left mouse click and
hold, and to scroll up with a right mouse click and hold. Releasing in both
cases stops the scrolling.
"""

#@<< about this plugin >>
#@+node:ekr.20040915104230.5:<< about this plugin >>
#@+at
# 
# Originally designed as a workaround for various bugs in Tkinter scrolling,
# this may actually be superior to wheel scrolling, in that there is little 
# work
# a user has to do to scroll except to press a button.
# 
# We use a Thread and 4 Tkinter Events to enable this. Threading was
# necessary to deserialise Button Press and Button Release. Without a Thread
# there apparently was no way to split the two apart. Exterior processes were
# not considered as serious pieces of the mechanism, threading kept things
# simple.
#@-at
#@nonl
#@-node:ekr.20040915104230.5:<< about this plugin >>
#@nl

import leoTkinterFrame
import Tkinter
import time

createCanvas = leoTkinterFrame.leoTkinterFrame.createCanvas

#@+others
#@+node:ekr.20040915104230:addUThreading & callbacks
def addUThreading( self, parentFrame ):

    '''Replaces createCanvas, adding UniversalScolling'''

    canvas = createCanvas( self, parentFrame )
    import threading
    ev = threading.Event()

    class direction:
        way = 'Down'

    way = direction()
    
    # Define callbacks.
    #@    @+others
    #@+node:ekr.20040915104230.2:run
    #here we watch for events to begin scrolling.
    #it is also the target of the thread.
    def run( ev = ev , way = way):
        
        while 1:
            ev.wait()
            if way.way == 'Down':
                canvas.yview(Tkinter.SCROLL, 1, Tkinter.UNITS)
            else:
                canvas.yview( Tkinter.SCROLL, -1, Tkinter.UNITS )
            time.sleep( .1 )
    
    t = threading.Thread( target = run )
    t.setDaemon( True )
    t.start()
    #@nonl
    #@-node:ekr.20040915104230.2:run
    #@+node:ekr.20040915104230.3:exe
    def exe( event, ev = ev, wy = 'Down', way = way ):
        
        """A callback that starts scrolling."""
    
        x = event.widget.canvasx( event.x )
        y = event.widget.canvasy( event.y )
    
        if event.widget.find_overlapping( x,y,x,y): 
            return
    
        ev.set()
        way.way = wy 
        return 'break'
    #@nonl
    #@-node:ekr.20040915104230.3:exe
    #@+node:ekr.20040915104230.4:off
    def off( event, ev = ev ):
        
        """A callback that stops scrolling."""
    
        ev.clear()
    #@nonl
    #@-node:ekr.20040915104230.4:off
    #@-others

    # Replace the canvas bindings.
    canvas.bind( '<Button-1>', exe )
    canvas.bind( '<Button-3>', lambda event, way = 'Up': exe( event, wy = way ) )
    canvas.bind( '<ButtonRelease-1>', off )
    canvas.bind( '<ButtonRelease-3>', off )
    return canvas
#@nonl
#@-node:ekr.20040915104230:addUThreading & callbacks
#@-others

if 1:
    leoTkinterFrame.leoTkinterFrame.createCanvas = addUThreading 
#@nonl
#@-node:ekr.20040831122004:@thin UniversalScrolling.py
#@-leo
