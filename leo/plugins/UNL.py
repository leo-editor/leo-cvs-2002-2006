#@+leo-ver=4-thin
#@+node:rogererens.20041013082304:@thin UNL.py
"""
Displays a node's "address" (aka Uniform Node Locator) in the status line.
Also allows "jumping" to UNLs.
"""

#@@language python
#@@tabwidth -4

#@<< about this plugin >>
#@+node:rogererens.20041014104346:<< about this plugin >>
#@+at
# 
# This plugin consists of two parts.
# 
# 1) It shows the 'address' or 'path' (list of ancestors and itself) of the 
# currently selected node in the status line. 'Uniform Node
# Locator' (UNL) also seems a nice description of it.
# 
# I use it to be able to copy the UNL into mail when discussing stuff in the
# selected node, so other people can find the node of interest quickly in 
# their
# own copy of the outlines (given the same directory structure). It's a matter 
# of selecting the UNL in the status line and pressing CTRL-C (on windows XP) 
# in order to copy it onto the clipboard.
# 
# 2) This plugin also overrides the default way of handling doubleclicking on 
# @url nodes.
# When doubleclicking the icon of an @url node for the case of a leo file on 
# the
# file system, it is now possible to jump directly to a node in that leo
# file. This is accomplished by appending the '#'-sign and the UNL of a node 
# to the URL of the leo file. As an example, see the following node.
# 
# This way, the need for duplicating nodes among leo files
# ought to be reduced. (Duplicates will get out of sync surely, as currently
# can be seen at this moment with the 'About Hooks' node in both 
# leoPlugins.leo and in leoDocs.leo: one mentions the 'select3' hook, the 
# other does not).
# 
# Beware when moving nodes that are being referred to or changing a headline 
# name.
# (TODO: create a link checker script to see if nodes referred to still 
# exist).
# 
# Don't refer to nodes that contain UNLs in the headline, as this busts the
# recognition of UNLs. Instead, refer to the parent or child of such nodes.
# 
# An added bonus is that the need for URLs to contain '%20' in stead of spaces 
# is removed, since the invoked function urlparse.urlsplit() can handle 
# spaces. And I presume the recognition of valid URLs in Python's standard 
# libs is more solid than found in the current Leo Core code.
#@-at
#@nonl
#@-node:rogererens.20041014104346:<< about this plugin >>
#@nl
__version__ = "0.2"
#@<< version history >>
#@+node:rogererens.20041014104353:<< version history >>
#@+at
# 
# 0.1 rogererens: Initial version.
# 
# PS: wouldn't it be more handy to define __version__ in this section?
# 
# 0.2 ekr:  changes for new status line class.
#@-at
#@nonl
#@-node:rogererens.20041014104353:<< version history >>
#@nl
#@<< imports >>
#@+node:rogererens.20041014110709.1:<< imports >>
import leoGlobals as g
import leoPlugins

Tk = g.importExtension('Tkinter',pluginName=__name__,verbose=True)
#@nonl
#@-node:rogererens.20041014110709.1:<< imports >>
#@nl
#@<< globals >>
#@+node:rogererens.20041014111328:<< globals >>
#@+at
# 
#@-at
#@-node:rogererens.20041014111328:<< globals >>
#@nl

#@+others
#@+node:rogererens.20041130095659:@url file:C:/Leo/plugins/leoPlugins.leo#Plugins-->Experimental/unfinished plugins-->@thin UNL.py-->To do
#@+at
# 
# A contrived example targeted at MS WindowsXP with Leo installed in the C 
# directory.
# Naturally, a clone must be used instead of referring to nodes _within_ a leo 
# file.
# UNL is helpful for referring to nodes in _other_ leo files!
# 
# on windowsXP:
#     C:/Leo/plugins/leoPlugins.leo
#     can also be substituted with
#     C:\Leo\plugins\leoPlugins.leo
#@-at
#@nonl
#@-node:rogererens.20041130095659:@url file:C:/Leo/plugins/leoPlugins.leo#Plugins-->Experimental/unfinished plugins-->@thin UNL.py-->To do
#@+node:ekr.20041202032543:@url file:c:/prog/leoCvs/leo/doc/leoDocs.leo#Users Guide-->Chapter 8: Customizing Leo
#@-node:ekr.20041202032543:@url file:c:/prog/leoCvs/leo/doc/leoDocs.leo#Users Guide-->Chapter 8: Customizing Leo
#@+node:rogererens.20041013082304.1:createStatusLine
def createStatusLine(tag,keywords):

    """Create a status line.""" # Might already be done by another plugin. Checking needed?
    
    c = keywords.get("c")
    statusLine = c.frame.createStatusLine()
    statusLine.clear()
    statusLine.put("...")
#@nonl
#@-node:rogererens.20041013082304.1:createStatusLine
#@+node:rogererens.20041013084119:onSelect2
def onSelect2 (tag,keywords):
    """Shows the UNL in the status line whenever a node gets selected."""

    c = keywords.get("c")

    c.frame.clearStatusLine()
    
    myList = []
    for p in c.currentPosition().self_and_parents_iter():
        myList.insert(0, p.headString())
    myString = "-->".join(myList)   # Rich has reported using ::
                                    # Any suggestions for standardization?
    c.frame.putStatusLine(myString)
#@-node:rogererens.20041013084119:onSelect2
#@+node:rogererens.20041021091837:onUrl1
def onUrl1 (tag,keywords):
    """Redefine the @url functionality of Leo Core: allows jumping to URL _and UNLs_. Spaces are now allowed in URLs."""
    c = keywords.get("c")
    v = keywords.get("v")
    url = v.headString()[4:].strip() # remove the "@url" part and possible leading and trailing whitespace characters

#@+at 
#@nonl
# Most browsers should handle the following urls:
#   ftp://ftp.uu.net/public/whatever.
#   http://localhost/MySiteUnderDevelopment/index.html
#   file://home/me/todolist.html
#@-at
#@@c

    try:
        import os       # should these imports also be in the <<imports
        import urlparse # >> section?
        
        try:
            urlTuple = urlparse.urlsplit(url)
            #@            << log url-stuff >>
            #@+node:rogererens.20041125015212:<<log url-stuff>>
            #@+at
            # g.es("scheme  : " + urlTuple[0])
            # g.es("network : " + urlTuple[1])
            # g.es("path    : " + urlTuple[2])
            # g.es("query   : " + urlTuple[3])
            # g.es("fragment: " + urlTuple[4])
            #@-at
            #@nonl
            #@-node:rogererens.20041125015212:<<log url-stuff>>
            #@nl
        except:
            g.es("exception interpreting the url " + url)
            g.es_exception()
       
        if not urlTuple[0]:
            urlProtocol = "file"    # assume this protocol by default
        else:
            urlProtocol = urlTuple[0]
        
        if urlProtocol == "file" and urlTuple[2].endswith(".leo"):
            ok,frame = g.openWithFileName(urlTuple[2], c)
            if ok:
                #@                << go to the node>>
                #@+node:rogererens.20041125015212.1:<<go to the node>>
                c2 = g.top()
                if urlTuple[4]: # we have a UNL!
                    nodeList = urlTuple[4].split("-->")
                    p = g.findTopLevelNode(nodeList[0])
                    for headline in nodeList[1:]:
                        p = g.findNodeInTree(p, headline)
                    c2.selectPosition(p)
                
                c2.frame.bringToFront() # now, how do I keep it to the front,
                                        # like the opening of LeoDocs.leo from the Help menu?
                                        # Maybe something to do with the handling of the doubleclick event?
                #@nonl
                #@-node:rogererens.20041125015212.1:<<go to the node>>
                #@nl
        else:
            import webbrowser
            
            # Mozilla throws a weird exception, then opens the file!
            try: webbrowser.open(url)
            except: pass
            
        return 1    # PREVENTS THE EXECUTION OF LEO'S CORE CODE IN
                    # Code-->Gui Base classes-->@thin leoFrame.py-->class leoTree-->tree.OnIconDoubleClick (@url)
    except:
        g.es("exception opening " + url)
        g.es_exception()
#@nonl
#@+node:rogererens.20041201000126:@url file:C:/Leo/src/LeoPy.leo#Code-->Gui Base classes-->@thin leoFrame.py-->class leoTree-->tree.OnIconDoubleClick (@url)
#@-node:rogererens.20041201000126:@url file:C:/Leo/src/LeoPy.leo#Code-->Gui Base classes-->@thin leoFrame.py-->class leoTree-->tree.OnIconDoubleClick (@url)
#@-node:rogererens.20041021091837:onUrl1
#@+node:rogererens.20041014110709:To do
#@+at
# 
# How about other plugins that create a status line? Should I test whether the 
# status line is already created?
# 
# Don't know exactly yet about the interaction with other plugins. The info in 
# the status line may be overwritten by them. That's fine with me: I can 
# always click on the icon of the node again to show the info again.
# 
# Keep the pane of the UNL referred to on top (now the pane with the referring 
# node stays on top).
# Maybe this should be a settings-dependent behaviour. Could this be solved by 
# using the 'onCreate' idiom and a UNLclass?
# 
# Find out about the difference between the event 'select2' and 'select3'.
# 
# A UNL checker script would be handy to check whether all references are 
# still valid.
# 
# Deal with path-separators for various platforms?
# 
# Handle relative paths?
# 
# Introduce a menu item to improve documentation? By firing up a browser, 
# directing it to leo on sourceforge (sourceforge userid needed?). EKR could 
# start up a new thread beforehand, "documentation improvements", where a new 
# message might be posted with the relevant UNL placed automatically in the 
# text box. Then the user just needs to type in his/her comments and post the 
# message.
#@-at
#@nonl
#@-node:rogererens.20041014110709:To do
#@-others

if Tk: # Ok for unit testing.
    if g.app.gui is None:
        g.app.createTkGui(__file__)

    if g.app.gui.guiName() == "tkinter":
        leoPlugins.registerHandler("after-create-leo-frame", createStatusLine)
        leoPlugins.registerHandler("select2", onSelect2)    # show UNL
        leoPlugins.registerHandler("@url1", onUrl1)         # jump to URL or UNL
                
        g.plugin_signon(__name__)
#@nonl
#@-node:rogererens.20041013082304:@thin UNL.py
#@-leo
