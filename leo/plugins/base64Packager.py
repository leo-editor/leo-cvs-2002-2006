#@+leo-ver=4-thin
#@+node:mork.20041020082242.1:@thin base64Packager.py
import leoPlugins
import leoGlobals as g
import leoNodes
import os.path
import base64

try:
    import Tkinter as Tk
    import Pmw
    import tkFileDialog
    import weakref
    importok = True
except Exception, x:
    g.es( "Cant Import %s" % x )
    importof = False

pload = '<'+'<'+'payload>' + '>'
b64 = "@base64"

#@+others
#@+node:mork.20041020101221:docs
#@+at
# base64Packager is a plugin that allows the user to import binary data and 
# store it in Leo as
# a base64 string.  Importing is offered in the Import menu and is called 
# 'Import base64'.  Importing
# a file will result in:
#     a new node with the headline @base64
#     followed by the name of the file
#     The body of this node will kill the colorizer , add some info on the 
# original file
#     and create a section reference to the payload node, which contains the 
# data.
# 
# To export this data, goto Export and choose 'Export base64'.  This will ask 
# for a location to place the file.  Then the system will determine if the 
# structrue of the base64 node is what it expected, basically what
# an import operation creates.  If Ok, it will write the file to the selected 
# directory.
# 
# There is an option to view the base64 under Outline.  It is the 'view 
# base64' option.  This will start up a Pmw Dialog with a Scrolled Canvas in 
# it.  Then the base64 payload is fed to a PhotoImage, and the data is 
# displayed.  This currently only supports formats recognized by the 
# PhotoImage class.  This would be the .gif format.  This functionality may be 
# enhanced in the future by PIL to support more image types.
# 
# Depending on the size of the image, you  may have to scroll around to see 
# it.  For example, a leo clone icon will require scrolling to find.  Id like 
# to change this in the future.
#@-at
#@@c
#@nonl
#@-node:mork.20041020101221:docs
#@+node:mork.20041020082653:base64Import
def base64Import( c ):
    
    pos = c.currentPosition()
    f = tkFileDialog.askopenfile()
    if f:
        data = f.read()
        name = os.path.basename( f.name )
        size = os.path.getsize( f.name )
        ltime = os.path.getmtime( f.name )
        f.close()
        b64_data = base64.encodestring( data )
        c.beginUpdate()
        body = '''
            @%s
            size: %s
            lastchanged: %s
                
            %s 
                '''% ( "killcolor", size, ltime, pload)
        tnode = leoNodes.tnode( body, "%s %s" % ( b64, name ) )
        npos = pos.insertAfter( tnode )
        payload = leoNodes.tnode( b64_data, pload)
        npos.insertAsNthChild( 0, payload)
        c.endUpdate()

#@-node:mork.20041020082653:base64Import
#@+node:mork.20041020082907:base64Export
def base64Export( c ):

    pos = c.currentPosition()
    hS = pos.headString()
    payload = pos.nthChild( 0 )
    if hS.startswith( b64 ) and payload.headString()== pload:
        f = tkFileDialog.askdirectory()
        hS2 = hS.split()
        if hS2[ -1 ] == b64: return
        f = '%s/%s' %( f, hS2[ - 1 ] )
        nfile = open( f, 'wb' )
        pdata = payload.bodyString()
        pdata = base64.decodestring( pdata )
        nfile.write( pdata )
        nfile.close()
#@-node:mork.20041020082907:base64Export
#@+node:mork.20041020092429:viewAsGif
def viewAsGif( c ):
    
    pos = c.currentPosition()
    hS = pos.headString()
    if not hS.startswith( b64 ): return None
    data = pos.nthChild( 0 )
    if data.headString() != pload: return None
    d = Pmw.Dialog( title = hS , buttons = [ 'Close', ])
    sc = Pmw.ScrolledCanvas( d.interior(), hscrollmode = 'static', vscrollmode = 'static' )
    sc.pack( expand = 1, fill= 'both' )
    pi = Tk.PhotoImage( data = str( data.bodyString() ) )
    tag = sc.interior().create_image( 0, 0, image = pi )
    d.activate()
#@nonl
#@-node:mork.20041020092429:viewAsGif
#@+node:mork.20041020082242.2:addMenu
haveseen = weakref.WeakKeyDictionary()
def addMenu( tag, keywords ):
    c = None
    if keywords.has_key( 'c' ):
        c = keywords[ 'c' ]
    elif keywords.has_key( 'new_c' ):
        c = keywords[ 'new_c' ]
    if not c: return None
    if haveseen.has_key( c ):
        return
    haveseen[ c ] = None
    men = c.frame.menu
    imen = men.getMenu( 'Import' )
    imen.add_command( label = "Import To base64", command = lambda c = c: base64Import( c ) )
    emen = men.getMenu( 'Export' )
    emen.add_command( label = "Export base64", command = lambda c = c : base64Export( c ) )
    omen = men.getMenu( 'Outline' )
    omen.add_command( label = 'View base64', command = lambda c = c: viewAsGif( c ) )

    


#@-node:mork.20041020082242.2:addMenu
#@+node:mork.20041020082242.3:if 1:
if importok:

    leoPlugins.registerHandler( ('start2' , 'open2', "new") , addMenu )
    __version__ = ".1"
    g.plugin_signon( __name__ )   
    
#@-node:mork.20041020082242.3:if 1:
#@-others
#@nonl
#@-node:mork.20041020082242.1:@thin base64Packager.py
#@-leo
