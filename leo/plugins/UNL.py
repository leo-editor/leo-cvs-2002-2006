#@+leo-ver=4-thin
#@+node:rogererens.20041013082304:@thin UNL.py
#@<< docstring >>
#@+node:ekr.20050119144617:<< docstring >>
'''This plugin supports Uniform Node Locators (UNL's). UNL's specify nodes within
Leo files. UNL's are not limited to nodes within the present Leo file; you can
use them to create cross-Leo-file links! UNL

This plugin consists of two parts:

1) Selecting a node shows the UNL in the status line at the bottom of the Leo
   window. You can copy from the status line and paste it into headlines, emails,
   whatever. 

2) Double-clicking @url nodes containing UNL's select the node specified in the
   UNL. If the UNL species in another Leo file, the other file will be opened.

Format of UNL's:

UNL's referring to nodes within the present outline have the form::

    headline1-->headline2-->...-->headlineN

headline1 is the headline of a top-level node, and each successive headline is
the headline of a child node.

UNL's of the form::

    file:<path>#headline1-->...-->headlineN

refer to a node specified in <path> For example, double clicking the following
headline will take you to Chapter 8 of Leo's Users Guide::

    @url file:c:/prog/leoCvs/leo/doc/leoDocs.leo#Users Guide-->Chapter 8: Customizing Leo
    
For example, suppose you want to email someone with comments about a Leo file.
Create a comments.leo file containing @url UNL nodes. That is, headlines are
@url followed by a UNL. The body text contains your comments about the nodes in
the _other_ Leo file! Send the comments.leo to your friend, who can use the
comments.leo file to quickly navigate to the various nodes you are talking
about. As another example, you can copy UNL's into emails. The recipient can
navigate to the nodes 'by hand' by following the arrows in the UNL.

**Notes**:

- At present, UNL's refer to nodes by their position in the outline. Moving a
  node will break the link.

- Don't refer to nodes that contain UNL's in the headline. Instead, refer to the
  parent or child of such nodes.

- You don't have to replace spaces in URL's or UNL's by '%20'.
'''
#@nonl
#@-node:ekr.20050119144617:<< docstring >>
#@nl

#@@language python
#@@tabwidth -4

__version__ = "0.3"
#@<< version history >>
#@+node:rogererens.20041014104353:<< version history >>
#@+at
# 
# 0.1 rogererens: Initial version.
# 
# PS: wouldn't it be more handy to define __version__ in this section?
# 
# 0.2 ekr:  changes for new status line class.
# 
# 0.3 ekr: Added support for url keyword in '@url1' hook.
# As a result, this plugin now support single and double quoted urls.
#@-at
#@nonl
#@-node:rogererens.20041014104353:<< version history >>
#@nl
#@<< imports >>
#@+node:rogererens.20041014110709.1:<< imports >>
import leoGlobals as g
import leoPlugins

Tk = g.importExtension('Tkinter',pluginName=__name__,verbose=True)

import os       
import urlparse 
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
#@+node:rogererens.20041130095659:@url 'file: ./../../plugins/leoPlugins.leo#Plugins-->Enhancing the icon and status areas-->@thin UNL.py-->To do'
#@+at 
#@nonl
# It is possible to link to nodes within the same file.  However clones might 
# be better.
#@-at
#@-node:rogererens.20041130095659:@url 'file: ./../../plugins/leoPlugins.leo#Plugins-->Enhancing the icon and status areas-->@thin UNL.py-->To do'
#@+node:ekr.20041202032543:@url 'file:./../doc/leoDocs.leo#Users Guide-->Chapter 8: Customizing Leo'
#@-node:ekr.20041202032543:@url 'file:./../doc/leoDocs.leo#Users Guide-->Chapter 8: Customizing Leo'
#@+node:rogererens.20041013084119:onSelect2
def onSelect2 (tag,keywords):

    """Shows the UNL in the status line whenever a node gets selected."""

    c = keywords.get("c")

    # c.currentPosition() is not valid while using the settings panel.
    new_p = keywords.get('new_p')
    
    # g.trace(new_p)
    
    if new_p:
        c.frame.clearStatusLine()
        myList = [p.headString() for p in new_p.self_and_parents_iter()]
        myList.reverse()

        # Rich has reported using ::
        # Any suggestions for standardization?
        s = "-->".join(myList)
        c.frame.putStatusLine(s)
#@nonl
#@-node:rogererens.20041013084119:onSelect2
#@+node:rogererens.20041013082304.1:createStatusLine
def createStatusLine(tag,keywords):

    """Create a status line.""" # Might already be done by another plugin. Checking needed?
    
    c = keywords.get("c")
    statusLine = c.frame.createStatusLine()
    statusLine.clear()
    statusLine.put("...")
#@nonl
#@-node:rogererens.20041013082304.1:createStatusLine
#@+node:rogererens.20041021091837:onUrl1
def onUrl1 (tag,keywords):
    """Redefine the @url functionality of Leo Core: allows jumping to URL _and UNLs_. Spaces are now allowed in URLs."""
    c = keywords.get("c")
    v = keywords.get("v")
    # The unl key is new in 4.3 beta 2.
    # The unl ends with the first blank, unless either single or double quotes are used.
    url = keywords.get('url')
    # url = v.headString()[4:].strip() # remove the "@url" part and possible leading and trailing whitespace characters

#@+at 
#@nonl
# Most browsers should handle the following urls:
#   ftp://ftp.uu.net/public/whatever.
#   http://localhost/MySiteUnderDevelopment/index.html
#   file://home/me/todolist.html
#@-at
#@@c

    try:
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
            urlProtocol = "file" # assume this protocol by default
        else:
            urlProtocol = urlTuple[0]
        
        if urlProtocol == "file" and urlTuple[2].endswith(".leo"):
            ok,frame = g.openWithFileName(urlTuple[2], c)
            if ok:
                #@                << go to the node>>
                #@+node:rogererens.20041125015212.1:<<go to the node>>
                c2 = frame.c
                
                if urlTuple[4]: # we have a UNL!
                    nodeList = urlTuple[4].split("-->")
                    p = g.findTopLevelNode(nodeList[0])
                    for headline in nodeList[1:]:
                        p = g.findNodeInTree(p, headline)
                    c2.selectPosition(p)
                    
                #@+at
                # 
                # EKR: The reason there are problems with selection is that 
                # button-1 is bound to
                # OnActivateTree, which calls g.app.gui.set_focus.
                #@-at
                #@nonl
                #@-node:rogererens.20041125015212.1:<<go to the node>>
                #@nl
        else:
            import webbrowser
            
            # Mozilla throws a weird exception, then opens the file!
            try: webbrowser.open(url)
            except: pass
            
        return True  # PREVENTS THE EXECUTION OF LEO'S CORE CODE IN
                    # Code-->Gui Base classes-->@thin leoFrame.py-->class leoTree-->tree.OnIconDoubleClick (@url)
    except:
        g.es("exception opening " + url)
        g.es_exception()
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
