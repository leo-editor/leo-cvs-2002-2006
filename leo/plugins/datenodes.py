#@+leo-ver=4-thin
#@+node:gfunch.20041207100416:@thin datenodes.py
"""
This plugin adds 'date nodes' (nodes with dates as their headlines) to the
current outline. Date nodes may be added one at a time, a month's-worth at a
time, or a year's-worth at a time. The format of the labels (headlines) is
configurable in the ini file.
"""

#@@language python
#@@tabwidth -4

#@<< about this plugin >>
#@+node:gfunch.20041207100416.1:<< about this plugin >>
#@+at
# 
# This plugin adds 'date nodes' (nodes with dates as their headlines) to the 
# current outline.
# Date nodes may be added one at a time, a month's-worth at a time, or a 
# year's-worth at a time.
# The format of the labels (headlines) is configurable in the ini file.
#@-at
#@nonl
#@-node:gfunch.20041207100416.1:<< about this plugin >>
#@nl

__version__ = "0.3"
#@<< version history >>
#@+node:gfunch.20041207100416.2:<< version history >>
#@+at
# 
# 0.1: Initial version.
# 0.2: Improved menu structure. Added ini file.
# 0.3: Changed docstring slightly.
#@-at
#@-node:gfunch.20041207100416.2:<< version history >>
#@nl

#@<< imports >>
#@+node:gfunch.20041207100416.3:<< imports >>
#@@c

import leoGlobals as g
import leoPlugins

import os
import calendar
import datetime
import ConfigParser
#@-node:gfunch.20041207100416.3:<< imports >>
#@nl

#@+others
#@+node:gfunch.20041207100416.5:class DateNodes
#@@c

class DateNodes:
    """Main DateNodes class"""
    
    #@    @+others
    #@+node:gfunch.20041207100416.6:__init__
    #@@c
    
    months = range(1,13)
    
    def __init__(self, c, config_dat):
        # initialize instance variables
        self.c = c
        # set configuration options
        self._set_config(config_dat)
    
        
    #@-node:gfunch.20041207100416.6:__init__
    #@+node:gfunch.20041209073652:_set_config
    #@@c
    
    def _set_config(self, config_dat):
        """Set any configuration options."""
        
        # default settings
        settings = {
        'day node'   : {'day_heading': '%Y-%m-%d'},
        'month nodes': {'day_heading': '%d: %A', 'month_heading': '%B %Y'},
        'year nodes' : {'day_heading': '%d: %A', 'month_heading': '%B', 'year_heading': '%Y'}
        }
        
        settings.update(config_dat)
        
        self.d_dfmt = settings['day node']['day_heading']
        self.m_dfmt = settings['month nodes']['day_heading']
        self.m_mfmt = settings['month nodes']['month_heading']
        self.y_dfmt = settings['year nodes']['day_heading']
        self.y_mfmt = settings['year nodes']['month_heading']
        self.y_yfmt = settings['year nodes']['year_heading']
        
        self.d_body = settings['day node']['body']
    
    
    
            
    #@-node:gfunch.20041209073652:_set_config
    #@+node:gfunch.20041208093039:_get_current_date
    #@@c
    
    def _get_current_date(self):
        """Get the current date in tuple form (year, month, day)."""
        
        date = datetime.date.today().timetuple()[:3]
    
        return date
    #@-node:gfunch.20041208093039:_get_current_date
    #@+node:gfunch.20041207100416.9:_get_month_info
    #@@c
    
    def _get_month_info(self, date=None):
        """Get the start date and number of dayss in a given month."""
            
        year, month, day = date or self._get_current_date()
        
        start,num_days = calendar.monthrange(year,month)
        start_day = calendar.day_name[start]
        
        return (start_day,num_days)
    
    #@-node:gfunch.20041207100416.9:_get_month_info
    #@+node:gfunch.20041208095742:_create_node_label
    #@@c
    
    def _create_node_label(self, date, fmt='%Y-%m-%d'):
        """Create a formatted node label (heading)."""
        
        year,month,day = date
        
        label = str(datetime.date(year, month, day).strftime(fmt))
        
        return label
    #@nonl
    #@-node:gfunch.20041208095742:_create_node_label
    #@+node:gfunch.20041208074734:insert_day_node
    #@@c
    
    def insert_day_node(self, date=None, day_fmt=None):
        """Insert a date node into the outline as 
        a subnode of the current selection."""
            
        #@    << get settings >>
        #@+node:gfunch.20041209141737:<< get settings >>
        c = self.c
            
        year, month, day = date or self._get_current_date()
        day_fmt = day_fmt or self.d_dfmt
        #@nonl
        #@-node:gfunch.20041209141737:<< get settings >>
        #@nl
        
        c.beginUpdate()
        #@    << insert day node >>
        #@+node:gfunch.20041209141737.1:<< insert day node >>
        p = c.currentPosition()
        
        v = p.insertAsLastChild()    
        label = self._create_node_label(date=(year,month,day),fmt=day_fmt)
        v.setHeadStringOrHeadline(label)
        v.setBodyStringOrPane(self.d_body)
            
        c.setCurrentPosition(p)
        #@-node:gfunch.20041209141737.1:<< insert day node >>
        #@nl
        c.endUpdate()
    #@-node:gfunch.20041208074734:insert_day_node
    #@+node:gfunch.20041207100416.11:insert_month_nodes
    #@@c
    
    def insert_month_nodes(self, date=None, day_fmt=None, month_fmt=None):
        """Insert a months-worth of date nodes into the outline as 
        subnodes of the current selection."""
    
        #@    << get settings >>
        #@+node:gfunch.20041209141737.2:<< get settings >>
        c = self.c
            
        year, month, day = date or self._get_current_date()
        day_fmt = day_fmt or self.m_dfmt
        month_fmt = month_fmt or self.m_mfmt
        #@nonl
        #@-node:gfunch.20041209141737.2:<< get settings >>
        #@nl
        
        c.beginUpdate()
        #@    << insert month node >>
        #@+node:gfunch.20041209141737.3:<< insert month node >>
        (start_day,num_days) = self._get_month_info(date)
            
        p = c.currentPosition()
        
        v = p.insertAsLastChild()    
        label = self._create_node_label(date=(year,month,day), fmt=month_fmt)
        v.setHeadStringOrHeadline(label)
        #@-node:gfunch.20041209141737.3:<< insert month node >>
        #@nl
        #@    << insert day sub-nodes >>
        #@+node:gfunch.20041209141737.4:<< insert day sub-nodes >>
        c.setCurrentPosition(v)
        
        pp = c.currentPosition()
        for day in range(1, num_days+1):
            self.insert_day_node(date=(year,month,day), day_fmt=day_fmt)
        #@nonl
        #@-node:gfunch.20041209141737.4:<< insert day sub-nodes >>
        #@nl
        c.setCurrentPosition(p)
        
        c.endUpdate()
    
    
    
    
    #@-node:gfunch.20041207100416.11:insert_month_nodes
    #@+node:gfunch.20041207100416.12:insert_year_nodes
    #@@c
    
    def insert_year_nodes(self, date=None, day_fmt=None, month_fmt=None, year_fmt=None):
        """Insert a years-worth of date nodes into the outline as 
        subnodes of the current selection."""
        
        #@    << get settings >>
        #@+node:gfunch.20041209141737.5:<< get settings >>
        c = self.c
            
        year, month, day = date or self._get_current_date()
        day_fmt = day_fmt or self.y_dfmt
        month_fmt = month_fmt or self.y_mfmt
        year_fmt = year_fmt or self.y_yfmt
        #@-node:gfunch.20041209141737.5:<< get settings >>
        #@nl
    
        c.beginUpdate()
        #@    << insert year node >>
        #@+node:gfunch.20041209141737.6:<< insert year node >>
        p = c.currentPosition()
        
        v = p.insertAsLastChild()    
        label = self._create_node_label(date=(year,month,day), fmt=year_fmt)
        v.setHeadStringOrHeadline(label)
            
        c.setCurrentPosition(v)
        #@nonl
        #@-node:gfunch.20041209141737.6:<< insert year node >>
        #@nl
        #@    << insert month sub-nodes >>
        #@+node:gfunch.20041209141737.7:<< insert month sub-nodes >>
        for month in self.months:
            self.insert_month_nodes(date=(year, month, day), day_fmt=day_fmt, month_fmt=month_fmt)
        #@nonl
        #@-node:gfunch.20041209141737.7:<< insert month sub-nodes >>
        #@nl
        c.endUpdate()
    
    
    #@-node:gfunch.20041207100416.12:insert_year_nodes
    #@-others
#@-node:gfunch.20041207100416.5:class DateNodes
#@+node:gfunch.20041207100654:on_create
def on_create(tag, keywords):

    #@    << get settings >>
    #@+node:gfunch.20041209141737.8:<< get settings >>
    c = keywords.get("c")
        
    # get the configuration settings
    config_file = g.os_path_join(g.app.loadDir,"../","plugins","datenodes.ini")
    settings = read_config(config_file)
            
    
    #@-node:gfunch.20041209141737.8:<< get settings >>
    #@nl
    
    # establish a class instance
    myDateNodes = DateNodes(c, settings)
    
    # create the plug-in menu
    create_menu(c,myDateNodes)
#@nonl
#@-node:gfunch.20041207100654:on_create
#@+node:gfunch.20041209063345:read_config
def read_config(fname):
    """Read the configuration (ini) file and parse it into a dictionary.""" 
    config = ConfigParser.ConfigParser()
    config.read(fname)
    sections = config.sections()
    config_dat = {}
    for section in sections:
        config_dat[section] = {}
        for item in config.items(section):
            name, val = item
            config_dat[section].update({name: val})
    return config_dat
#@nonl
#@-node:gfunch.20041209063345:read_config
#@+node:gfunch.20041207102456:create_menu
def create_menu(c, instance):

    """Create the plug-in menu."""

    # create a menu separator
    c.frame.menu.createMenuItemsFromTable("Outline",[("-", None, None),])

    # create an expandable menu
    table = [("Single Day", None, instance.insert_day_node),
             ("Full Month", None, instance.insert_month_nodes),
             ("Full Year", None, instance.insert_year_nodes)]

    expandMenu = c.frame.menu.createNewMenu("Insert Date Nodes...","Outline")
    c.frame.menu.createMenuEntries(expandMenu,table,dynamicMenu=True)
#@nonl
#@-node:gfunch.20041207102456:create_menu
#@-others

if 1: # OK for unit testing.
    leoPlugins.registerHandler("after-create-leo-frame", on_create)
    g.plugin_signon(__name__)
#@nonl
#@-node:gfunch.20041207100416:@thin datenodes.py
#@-leo
