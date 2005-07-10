#@+leo-ver=4-thin
#@+node:ekr.20050710142719:@thin leoEditCommands.py
'''Basic editor commands for Leo.

Modelled after Emacs and Vim commands.'''

class editCommands:
    #@    @+others
    #@+node:ekr.20050710142746:ctor
    def __init__ (self,c):
        
        self.c = c
        self.mode = 'default'
        self.modeStack = []
    #@nonl
    #@-node:ekr.20050710142746:ctor
    #@-others
#@nonl
#@-node:ekr.20050710142719:@thin leoEditCommands.py
#@-leo
