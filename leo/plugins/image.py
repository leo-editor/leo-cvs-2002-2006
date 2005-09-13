#@+leo-ver=4-thin
#@+node:edream.110203113231.753:@thin image.py
"""Handles images in body text.

Based on work by Gil Scwartz.
Brent Burley provided many important insights. See:
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/52264"""

#@@language python
#@@tabwidth -4

#@<< imports >>
#@+node:ekr.20050101090207.1:<< imports >>
import leoGlobals as g
import leoPlugins

Tk = g.importExtension('Tkinter',pluginName=__name__,verbose=True)
#@nonl
#@-node:ekr.20050101090207.1:<< imports >>
#@nl

#@+others
#@+node:edream.110203113231.754:onSelect
def onSelect (tag,keywords):

    new_v = keywords.get("new_v")
    h = new_v.headString()
    if h[:7] == "@image ":
        filename = h[7:]
        #@        << Select Image >>
        #@+node:edream.110203113231.755:<< Select Image >>
        # Display the image file in the text pane, if you can find the file
        a = g.app
        c = keywords.get("c")
        body = c.frame.body
        
        if os.path.isfile(filename):
            try:
                # Note that Tkinter only understands GIF
                photo = Tk.PhotoImage(master=a.root, file=filename)
            except:
                g.es("error: cannot load image")
                return
            # Nicely display the image at the center top and push the text below.
            a.gsphoto = photo # This is soooo important.
            photoWidth = photo.width()
            bodyWidth = body.bodyCtrl.winfo_width()
            padding = int((bodyWidth - photoWidth - 16) / 2)
            padding = max(0,padding)
            a.gsimage = body.bodyCtrl.image_create("1.0",image=photo,padx=padding)
        else:
            g.es("warning: missing image file")
        #@nonl
        #@-node:edream.110203113231.755:<< Select Image >>
        #@nl
#@nonl
#@-node:edream.110203113231.754:onSelect
#@+node:edream.110203113231.756:onUnselect
def onUnselect (tag,keywords):

    a = g.app
    old_v = keywords.get("old_v")
    if old_v:
        h = old_v.headString()
        if h[:7] == "@image ":
            #@            << Unselect Image >>
            #@+node:edream.110203113231.757:<< Unselect Image >>
            # Erase image if it was previously displayed
            a = g.app ; c = keywords.get("c")
            
            if a.gsimage:
                try:
                     c.frame.body.bodyCtrl.delete(a.gsimage)
                except:
                    g.es("info: no image to erase")
            
            # And forget about it
            a.gsimage = None
            a.gsphoto = None
            #@-node:edream.110203113231.757:<< Unselect Image >>
            #@nl
    else: # Leo is initializing.
        a.gsphoto = None # Holds our photo file
        a.gsimage = None # Holds our image instance within the text pane
#@nonl
#@-node:edream.110203113231.756:onUnselect
#@-others

import os

if Tk: # Ok for unit testing.

    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":
        
        leoPlugins.registerHandler("select2", onSelect)
        leoPlugins.registerHandler("unselect1", onUnselect)
        
        __version__ = "1.2" # Set version for the plugin handler.
        g.plugin_signon(__name__)
#@nonl
#@-node:edream.110203113231.753:@thin image.py
#@-leo
