#@+leo-ver=4-thin
#@+node:ekr.20031218072017.4100:@thin leoTkinterMenu.py
"""Tkinter menu handling for Leo."""

#@@language python
#@@tabwidth -4
#@@pagewidth 80

import leoGlobals as g
import leoMenu
import Tkinter as Tk
import tkFont

class leoTkinterMenu (leoMenu.leoMenu):
    """A class that represents a Leo window."""
    #@    @+others
    #@+node:ekr.20031218072017.4101:Birth & death
    #@+node:ekr.20031218072017.4102:leoTkinterMenu.__init__
    def __init__ (self,frame):
        
        # Init the base class.
        leoMenu.leoMenu.__init__(self,frame)
        
        self.top = frame.top
        self.c = frame.c
        self.frame = frame
    #@nonl
    #@-node:ekr.20031218072017.4102:leoTkinterMenu.__init__
    #@-node:ekr.20031218072017.4101:Birth & death
    #@+node:ekr.20060211101811:Activate menu commands
    #@+node:ekr.20060211100905.1:tkMenu.activateMenu
    def activateMenu (self,menuName):
        
        c = self.c ;  top = c.frame.top
        topx,topy = top.winfo_rootx(),top.winfo_rooty()
        menu = c.frame.menu.getMenu(menuName)
    
        if menu:
            d = self.computeMenuPositions()
            x = d.get(menuName)
            if x is None:
                 x = 0 ; g.trace('oops, no menu offset: %s' % menuName)
            
            menu.tk_popup(topx+d.get(menuName,0),topy) # Fix by caugm.  Thanks!
        else:
            g.trace('oops, no menu: %s' % menuName)
    #@nonl
    #@-node:ekr.20060211100905.1:tkMenu.activateMenu
    #@+node:ekr.20060210133835.1:tkMenu.computeMenuPositions
    def computeMenuPositions (self):
        
        # A hack.  It would be better to set this when creating the menus.
        menus = ('File','Edit','Outline','Plugins','Cmds','Window','Help')
        
        # Compute the *approximate* x offsets of each menu.
        d = {}
        n = 0
        for z in menus:
            menu = self.getMenu(z)
            fontName = menu.cget('font')
            font = tkFont.Font(font=fontName)
            # print '%8s' % (z),menu.winfo_reqwidth(),menu.master,menu.winfo_x()
            d [z] = n
            # A total hack: sorta works on windows.
            n += font.measure(z+' '*4)+1
            
        return d
    #@nonl
    #@-node:ekr.20060210133835.1:tkMenu.computeMenuPositions
    #@-node:ekr.20060211101811:Activate menu commands
    #@+node:ekr.20060211144330.1:getMacHelpMenu
    def getMacHelpMenu (self):
        
        return None ###
        
        try:
            helpMenu = Tk.Menu('top.help')
            return helpMenu
            
        except Exception:
            g.trace('Can not get MacOS Help menu')
            g.es_exception()
            return None
    #@nonl
    #@-node:ekr.20060211144330.1:getMacHelpMenu
    #@+node:ekr.20031218072017.4103:Tkinter menu bindings
    # See the Tk docs for what these routines are to do
    #@nonl
    #@+node:ekr.20031218072017.4104:Methods with Tk spellings
    #@+node:ekr.20031218072017.4105:add_cascade
    def add_cascade (self,parent,label,menu,underline):
        
        """Wrapper for the Tkinter add_cascade menu method."""
        
        return parent.add_cascade(label=label,menu=menu,underline=underline)
    
    #@-node:ekr.20031218072017.4105:add_cascade
    #@+node:ekr.20031218072017.4106:add_command
    def add_command (self,menu,**keys):
        
        """Wrapper for the Tkinter add_command menu method."""
    
        return menu.add_command(**keys)
        
    #@-node:ekr.20031218072017.4106:add_command
    #@+node:ekr.20031218072017.4107:add_separator
    def add_separator(self,menu):
        
        """Wrapper for the Tkinter add_separator menu method."""
    
        menu.add_separator()
        
    #@-node:ekr.20031218072017.4107:add_separator
    #@+node:ekr.20031218072017.4108:bind
    def bind (self,bind_shortcut,callback):
        
        """Wrapper for the Tkinter bind menu method."""
        
        # g.trace(bind_shortcut)
    
        return self.top.bind(bind_shortcut,callback)
    #@-node:ekr.20031218072017.4108:bind
    #@+node:ekr.20031218072017.4109:delete
    def delete (self,menu,realItemName):
        
        """Wrapper for the Tkinter delete menu method."""
    
        return menu.delete(realItemName)
    #@nonl
    #@-node:ekr.20031218072017.4109:delete
    #@+node:ekr.20031218072017.4110:delete_range
    def delete_range (self,menu,n1,n2):
        
        """Wrapper for the Tkinter delete menu method."""
    
        return menu.delete(n1,n2)
    
    #@-node:ekr.20031218072017.4110:delete_range
    #@+node:ekr.20031218072017.4111:destroy
    def destroy (self,menu):
        
        """Wrapper for the Tkinter destroy menu method."""
    
        return menu.destroy()
    
    #@-node:ekr.20031218072017.4111:destroy
    #@+node:ekr.20031218072017.4112:insert_cascade
    def insert_cascade (self,parent,index,label,menu,underline):
        
        """Wrapper for the Tkinter insert_cascade menu method."""
        
        return parent.insert_cascade(
            index=index,label=label,
            menu=menu,underline=underline)
    
    
    #@-node:ekr.20031218072017.4112:insert_cascade
    #@+node:ekr.20031218072017.4113:new_menu
    def new_menu(self,parent,tearoff=False):
        
        """Wrapper for the Tkinter new_menu menu method."""
    
        return Tk.Menu(parent,tearoff=tearoff)
    #@nonl
    #@-node:ekr.20031218072017.4113:new_menu
    #@-node:ekr.20031218072017.4104:Methods with Tk spellings
    #@+node:ekr.20031218072017.4114:Methods with other spellings (Tkmenu)
    #@+node:ekr.20041228063406:clearAccel
    def clearAccel(self,menu,name):
        
        realName = self.getRealMenuName(name)
        realName = realName.replace("&","")
    
        menu.entryconfig(realName,accelerator='')
    #@nonl
    #@-node:ekr.20041228063406:clearAccel
    #@+node:ekr.20031218072017.4115:createMenuBar
    def createMenuBar(self,frame):
    
        top = frame.top
        topMenu = Tk.Menu(top,postcommand=self.updateAllMenus)
        
        # Do gui-independent stuff.
        self.setMenu("top",topMenu)
        self.createMenusFromTables()
        
        top.config(menu=topMenu) # Display the menu.
    #@nonl
    #@-node:ekr.20031218072017.4115:createMenuBar
    #@+node:ekr.20051022042645:createOpenWithMenu
    def createOpenWithMenu(self,parent,label,index,amp_index):
        
        '''Create a submenu.'''
        
        menu = Tk.Menu(parent,tearoff=0)
        parent.insert_cascade(index,label=label,menu=menu,underline=amp_index)
        return menu
    #@nonl
    #@-node:ekr.20051022042645:createOpenWithMenu
    #@+node:ekr.20031218072017.4119:disableMenu
    def disableMenu (self,menu,name):
        
        try:
            menu.entryconfig(name,state="disabled")
        except: 
            try:
                realName = self.getRealMenuName(name)
                realName = realName.replace("&","")
                menu.entryconfig(realName,state="disabled")
            except:
                print "disableMenu menu,name:",menu,name
                g.es_exception()
                pass
    #@-node:ekr.20031218072017.4119:disableMenu
    #@+node:ekr.20031218072017.4120:enableMenu
    # Fail gracefully if the item name does not exist.
    
    def enableMenu (self,menu,name,val):
        
        state = g.choose(val,"normal","disabled")
        try:
            menu.entryconfig(name,state=state)
        except:
            try:
                realName = self.getRealMenuName(name)
                realName = realName.replace("&","")
                menu.entryconfig(realName,state=state)
            except:
                print "enableMenu menu,name,val:",menu,name,val
                g.es_exception()
                pass
    #@nonl
    #@-node:ekr.20031218072017.4120:enableMenu
    #@+node:ekr.20031218072017.4121:setMenuLabel
    def setMenuLabel (self,menu,name,label,underline=-1):
    
        try:
            if type(name) == type(0):
                # "name" is actually an index into the menu.
                menu.entryconfig(name,label=label,underline=underline)
            else:
                # Bug fix: 2/16/03: use translated name.
                realName = self.getRealMenuName(name)
                realName = realName.replace("&","")
                # Bug fix: 3/25/03" use tranlasted label.
                label = self.getRealMenuName(label)
                label = label.replace("&","")
                menu.entryconfig(realName,label=label,underline=underline)
        except:
            if not g.app.unitTesting:
                print "setMenuLabel menu,name,label:",menu,name,label
                g.es_exception()
    #@nonl
    #@-node:ekr.20031218072017.4121:setMenuLabel
    #@-node:ekr.20031218072017.4114:Methods with other spellings (Tkmenu)
    #@-node:ekr.20031218072017.4103:Tkinter menu bindings
    #@-others
#@nonl
#@-node:ekr.20031218072017.4100:@thin leoTkinterMenu.py
#@-leo
