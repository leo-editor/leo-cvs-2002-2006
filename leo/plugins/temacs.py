#@+leo-ver=4-thin
#@+node:mork.20041014112843.1:@thin temacs.py
'''temacs is a binding module for the Tkinter Text widget.

setBufferStrokes() will bind callbacks to the widget.  It is not an attempt
to emulate all Emacs keystrokes, but only a select few.
'''

#@@language python
#@@tabwidth -4

__version__ = '.5'
#@<< version history >>
#@+node:ekr.20041028081942:<< version history >>
#@+at
# 
# 0.3 Leo User: Original code.
# 
# 0.4 EKR: Minor style mods.
# 
# 0.5 EKR: cbDict must be defined at end of file.
#@-at
#@nonl
#@-node:ekr.20041028081942:<< version history >>
#@nl
#@<< imports >>
#@+node:ekr.20041028081841:<< imports >>
import leoGlobals as g

try:
    import Tkinter
    import tkFileDialog
except ImportError:
    Tkinter = g.cantImport("Tkinter",__name__)
    
    
import cPickle
import re
import string
#@-node:ekr.20041028081841:<< imports >>
#@nl
#@<< globals >>
#@+node:ekr.20041028084110:<< globals >>
# Abbreviations...
abbrevMode = False
abbrevOn = False
abbrevs = {}

# Macros...
lastMacro = None
macs = []
macro = []
namedMacros = {}
macroing = False

# Buffers...
mbuffers = {}
svars = {}

registers = {}

tailEnds = {}

undoers = {}
#@nonl
#@-node:ekr.20041028084110:<< globals >>
#@nl

isearch = False

#@+others
#@+node:mork.20041014112843.31:setBufferStrokes
def setBufferStrokes( buffer, label ):
        '''setBufferStrokes takes a Tk Text widget called buffer. 'stext' is a function or method
        that when called will return the value of the search text. 'rtext' is a function or method
        that when called will return the value of the replace text.  It is this method and
        getHelpText that users of the temacs module should call.  The rest are callback functions
        that enable the Emacs emulation.'''
        def cb( evstring ):
            _cb = None
            if cbDict.has_key( evstring ):
                _cb = cbDict[ evstring ]
            evstring = '<%s>' % evstring
            if evstring != '<Key>':
                buffer.bind( evstring,  lambda event, meth = _cb: masterCommand( event, meth , evstring) )
            else:
                buffer.bind( evstring,  lambda event, meth = _cb: masterCommand( event, meth , evstring), '+' )

        for z in cbDict:
            cb( z )
        
        mbuffers[ buffer ] = label
        svars[ buffer ] = Tkinter.StringVar()
        def setVar( event ):
            label = mbuffers[ event.widget ]
            svar = svars[ event.widget ]
            label.configure( textvariable = svar )
        buffer.bind( '<FocusIn>', setVar, '+' )
        cb( 'Key' )
#@-node:mork.20041014112843.31:setBufferStrokes
#@+node:mork.20041014112843.3:setLabelGrey
def setLabelGrey( label ):
    label.configure( background = 'lightgrey' )
#@-node:mork.20041014112843.3:setLabelGrey
#@+node:mork.20041014112843.4:setLabelBlue
def setLabelBlue( label ):
    label.configure( background = 'lightblue' ) 
#@-node:mork.20041014112843.4:setLabelBlue
#@+node:mork.20041014112843.5:_tailEnd
def _tailEnd( buffer ):
    return tailEnds[ buffer ]( buffer )
#@-node:mork.20041014112843.5:_tailEnd
#@+node:mork.20041014112843.6:setTailEnd
def setTailEnd( buffer , tailCall ):
    tailEnds[ buffer ] = tailCall
#@-node:mork.20041014112843.6:setTailEnd
#@+node:ekr.20041028083211.1:Undo...
#@+node:mork.20041014112843.7:setUndoer


def setUndoer( buffer, undoer ):
    undoers[ buffer ] = undoer
#@-node:mork.20041014112843.7:setUndoer
#@+node:mork.20041014112843.8:doUndo
def doUndo( event, amount = 1 ):
    buffer = event.widget
    if undoers.has_key( buffer ):
        for z in xrange( amount ):
            undoers[ buffer ]()
    return 'break'
#@-node:mork.20041014112843.8:doUndo
#@-node:ekr.20041028083211.1:Undo...
#@+node:ekr.20041028083211.2:Keyboard macros...
#@+node:mork.20041014112843.9:startKBDMacro
def startKBDMacro( event ):
    global macroing
    macroing = True
    return 'break'
#@-node:mork.20041014112843.9:startKBDMacro
#@+node:mork.20041014112843.10:recordKBDMacro
def recordKBDMacro( event, stroke ):
    if stroke != '<Key>':
        macro.append( (stroke, event.keycode, event.keysym, event.char) )
    elif stroke == '<Key>':
        if event.keysym != '??':
            macro.append( ( event.keycode, event.keysym ) )
    return
#@-node:mork.20041014112843.10:recordKBDMacro
#@+node:mork.20041014112843.11:stopKBDMacro
def stopKBDMacro( event ):
    global macro, lastMacro, macroing
    if macro:
        macro = macro[ : -4 ]
        macs.insert( 0, macro )
        lastMacro = macro
        macro = []

    macroing = False
    return 'break' 
#@-node:mork.20041014112843.11:stopKBDMacro
#@+node:mork.20041014112843.12:_executeMacro
def _executeMacro( macro, buffer ):
    for z in macro:
        if len( z ) == 2:
            buffer.event_generate( '<Key>', keycode = z[ 0 ], keysym = z[ 1 ] ) 
        else:
            meth = z[ 0 ].lstrip( '<' ).rstrip( '>' )
            method = cbDict[ meth ]
            ev = Tkinter.Event()
            ev.widget = buffer
            ev.keycode = z[ 1 ]
            ev.keysym = z[ 2 ]
            ev.char = z[ 3 ]
            masterCommand( ev , method, '<%s>' % meth )
    return _tailEnd( buffer )  
#@-node:mork.20041014112843.12:_executeMacro
#@+node:mork.20041014112843.13:executeLastMacro
def executeLastMacro( event ):
    buffer = event.widget
    if lastMacro:
        return _executeMacro( lastMacro, buffer )
    return 'break'
#@-node:mork.20041014112843.13:executeLastMacro
#@+node:mork.20041014112843.14:nameLastMacro
def nameLastMacro( event ):
    global macroing
    svar, label = getSvarLabel( event )    
    if macroing == False:
        macroing = 2
        svar.set( '' )
        setLabelBlue( label )
        return 'break'
    if event.keysym == 'Return':
        name = svar.get()
        _addToDoAltX( name, lastMacro )
        svar.set( '' )
        setLabelBlue( label )
        macroing = False
        return 'break'
    setSvar( event, svar )
    return 'break'
#@-node:mork.20041014112843.14:nameLastMacro
#@+node:mork.20041014112843.15:_addToDoAltX
def _addToDoAltX( name, macro ):
    if not doAltX.has_key( name ):
        def exe( event, macro = macro ):
            stopControlX( event )
            return _executeMacro( macro, event.widget )
        doAltX[ name ] = exe
        namedMacros[ name ] = macro
        return True
    else:
        return False
#@-node:mork.20041014112843.15:_addToDoAltX
#@+node:mork.20041014112843.16:loadMacros
def loadMacros( event ):

    f = tkFileDialog.askopenfile()
    if f == None: return 'break'
    else:
        return _loadMacros( f )       
#@-node:mork.20041014112843.16:loadMacros
#@+node:mork.20041014112843.17:_loadMacros
def _loadMacros( f ):
    macros = cPickle.load( f )
    for z in macros:
        _addToDoAltX( z, macros[ z ] )
    return 'break'
#@-node:mork.20041014112843.17:_loadMacros
#@+node:mork.20041014112843.18:getMacroName
def getMacroName( event ):
    global macroing
    svar, label = getSvarLabel( event )
    if not macroing:
        macroing = 3
        svar.set('')
        setLabelBlue( label )
        return 'break'
    if event.keysym == 'Return':
        macroing = False
        saveMacros( event, svar.get() )
        return 'break'
    if event.keysym == 'Tab':
        svar.set( _findMatch( svar, namedMacros ) )
        return 'break'        
    setSvar( event, svar )
    return 'break'    
#@-node:mork.20041014112843.18:getMacroName
#@+node:mork.20041014112843.19:saveMacros
def saveMacros( event, macname ):

        name = tkFileDialog.asksaveasfilename()
        if name:
            f = file( name, 'a+' )
            f.seek( 0 )
            if f:
                _saveMacros( f, macname ) 
        return 'break'
#@-node:mork.20041014112843.19:saveMacros
#@+node:mork.20041014112843.20:_saveMacros
def _saveMacros( f , name ):
    fname = f.name
    try:
        macs = cPickle.load( f )
    except:
        macs = {}
    f.close()
    if namedMacros.has_key( name ):
        macs[ name ] = namedMacros[ name ]
        f = file( fname, 'w' )
        cPickle.dump( macs, f )
        f.close()   
#@-node:mork.20041014112843.20:_saveMacros
#@-node:ekr.20041028083211.2:Keyboard macros...
#@+node:ekr.20041028083211.3:Emacs commands...
#@+node:ekr.20041028083211.4:Comment column
#@+node:mork.20041014112843.21:setCommentColumn
ccolumn = '0'
def setCommentColumn( event ):
    global ccolumn
    cc= event.widget.index( 'insert' )
    cc1, cc2 = cc.split( '.' )
    ccolumn = cc2
    return 'break'
#@-node:mork.20041014112843.21:setCommentColumn
#@+node:mork.20041014112843.22:indentToCommentColumn
def indentToCommentColumn( event ):
    buffer = event.widget
    i = buffer.index( 'insert lineend' )
    i1, i2 = i.split( '.' )
    i2 = int( i2 )
    c1 = int( ccolumn )
    if i2 < c1:
        wsn = c1 - i2
        buffer.insert( 'insert lineend', ' '* wsn )
    if i2 >= c1:
        buffer.insert( 'insert lineend', ' ')
    buffer.mark_set( 'insert', 'insert lineend' )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.22:indentToCommentColumn
#@-node:ekr.20041028083211.4:Comment column
#@+node:ekr.20041028083211.5:Editing commands
#@+node:mork.20041014112843.23:exchangePointMark
def exchangePointMark( event ):
    if not _chckSel( event ):
        return
    buffer = event.widget
    s1 = buffer.index( 'sel.first' )
    s2 = buffer.index( 'sel.last' )
    i = buffer.index( 'insert' )
    if i == s1:
        buffer.mark_set( 'insert', s2 )
    else:
        buffer.mark_set('insert', s1 )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.23:exchangePointMark
#@+node:mork.20041014112843.24:howMany
howM = False
def howMany( event ):
    global howM
    svar, label = getSvarLabel( event )
    if event.keysym == 'Return':
        buffer = event.widget
        txt = buffer.get( '1.0', 'end' )
        reg1 = svar.get()
        reg = re.compile( reg1 )
        i = reg.findall( txt )
        svar.set( '%s occurances found of %s' % (len(i), reg1 ) )
        setLabelGrey( label )
        howM = False
        return 'break'
    setSvar( event, svar )
    return 'break'
#@-node:mork.20041014112843.24:howMany
#@+node:mork.20041014112843.25:startHowMany
def startHowMany( event ):
    global howM
    howM = True
    svar, label = getSvarLabel( event )
    svar.set( '' )
    setLabelBlue( label )
    return 'break'
#@-node:mork.20041014112843.25:startHowMany
#@+node:mork.20041014112843.26:selectParagraph
def selectParagraph( event ):
    buffer = event.widget
    txt = buffer.get( 'insert linestart', 'insert lineend' )
    txt = txt.lstrip().rstrip()
    i = buffer.index( 'insert' )
    if not txt:
        while 1:
            i = buffer.index( '%s + 1 lines' % i )
            txt = buffer.get( '%s linestart' % i, '%s lineend' % i )
            txt = txt.lstrip().rstrip()
            if txt:
                _selectParagraph( buffer, i )
                break
            if buffer.index( '%s lineend' % i ) == buffer.index( 'end' ):
                return 'break'
    if txt:
        while 1:
            i = buffer.index( '%s - 1 lines' % i )
            txt = buffer.get( '%s linestart' % i, '%s lineend' % i )
            txt = txt.lstrip().rstrip()
            if not txt or buffer.index( '%s linestart' % i ) == buffer.index( '1.0' ):
                if not txt:
                    i = buffer.index( '%s + 1 lines' % i )
                _selectParagraph( buffer, i )
                break     
    return _tailEnd( buffer )
#@-node:mork.20041014112843.26:selectParagraph
#@+node:mork.20041014112843.27:_selectParagraph
def _selectParagraph( buffer, start ):
    i2 = start
    while 1:
        txt = buffer.get( '%s linestart' % i2, '%s lineend' % i2 )
        if buffer.index( '%s lineend' % i2 )  == buffer.index( 'end' ):
            break
        txt = txt.lstrip().rstrip()
        if not txt: break
        else:
            i2 = buffer.index( '%s + 1 lines' % i2 )
    buffer.tag_add( 'sel', '%s linestart' % start, '%s lineend' % i2 )
    buffer.mark_set( 'insert', '%s lineend' % i2 )
#@-node:mork.20041014112843.27:_selectParagraph
#@+node:mork.20041014112843.28:killParagraph
def killParagraph( event ):   
    buffer = event.widget
    i = buffer.index( 'insert' )
    txt = buffer.get( 'insert linestart', 'insert lineend' )
    if not txt.rstrip().lstrip():
        i = buffer.search( r'\w', i, regexp = True, stopindex = 'end' )
    _selectParagraph( buffer, i )
    i2 = buffer.index( 'insert' )
    kill( event, i, i2 )
    buffer.mark_set( 'insert', i )
    buffer.selection_clear()
    return _tailEnd( buffer )
#@-node:mork.20041014112843.28:killParagraph
#@+node:mork.20041014112843.29:backwardKillParagraph
def backwardKillParagraph( event ):   
    buffer = event.widget
    i = buffer.index( 'insert' )
    i2 = i
    txt = buffer.get( 'insert linestart', 'insert lineend' )
    if not txt.rstrip().lstrip():
        movingParagraphs( event, -1 )
        i2 = buffer.index( 'insert' )
    selectParagraph( event )
    i3 = buffer.index( 'sel.first' )
    kill( event, i3, i2 )
    buffer.mark_set( 'insert', i )
    buffer.selection_clear()
    return _tailEnd( buffer )
#@-node:mork.20041014112843.29:backwardKillParagraph
#@+node:mork.20041014112843.30:iterateKillBuffer
reset = False
def iterateKillBuffer():
    global reset
    while 1:
        for z in killbuffer:
            if reset:
                reset = False
                break
            yield z
#@-node:mork.20041014112843.30:iterateKillBuffer
#@+node:mork.20041014112843.32:moveTo
def moveTo( event, spot ):
    buffer = event.widget
    buffer.mark_set( Tkinter.INSERT, spot )
    buffer.see( spot )
    return 'break'
#@-node:mork.20041014112843.32:moveTo
#@+node:mork.20041014112843.33:moveword
def moveword( event, way  ):
            buffer = event.widget
            c = 'c'
            i = way
            def wsBack( i , way):
                        while 1:
                            i = i + way
                            bs = ''
                            if i > 0:
                                bs = 'insert +%sc' % i 
                                char = buffer.get( bs ) 
                            if i < 0:
                                bs = 'insert'+str( i ) + c
                                char = buffer.get( bs ) 
                            if buffer.index( bs ) in ( '1.0', buffer.index( 'end' ) ):
                                char = 'stop'
                            if char not in string.whitespace:
                                buffer.mark_set( 'insert', bs + ' wordstart' )
                                buffer.see( 'insert' )
                                buffer.event_generate( '<Key>' )
                                buffer.update_idletasks()
                                return 'break'
            def toWs( i , way):                
                while 1:
                    bs = ''
                    if way < 0:
                        bs = 'insert %sc' % i 
                        char = buffer.get( bs )
                    if way > 0:
                        bs = 'insert +%sc' %  i  
                        char = buffer.get( bs )
                    if buffer.index( bs ) in ( '1.0', buffer.index( 'end' ) ):
                        return i                    
                    if char in string.whitespace: return i
                    i = i + way
            char = buffer.get( 'insert', 'insert + 1c' )
            if char in string.whitespace : return wsBack( i , way)
            else: return wsBack( toWs( i , way ) , way)
#@-node:mork.20041014112843.33:moveword
#@+node:mork.20041014112843.34:kill
def kill( event, frm, to  ):
    buffer = event.widget
    text = buffer.get( frm, to )
    addToKillBuffer( text )
    if frm == 'insert' and to =='insert lineend' and buffer.index( frm ) == buffer.index( to ):
        buffer.delete( 'insert', 'insert lineend +1c' )
        addToKillBuffer( '\n' )
    else:
        buffer.delete( frm, to )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.34:kill
#@+node:mork.20041014112843.35:deletelastWord
def deletelastWord( event ):
    buffer = event.widget
    i = buffer.get( 'insert' )
    moveword( event, -1 )
    kill( event, 'insert', 'insert wordend')
    moveword( event ,1 )
    return 'break'
#@-node:mork.20041014112843.35:deletelastWord
#@+node:mork.20041014112843.36:walkKB
def walkKB( event, frm, which, kb = iterateKillBuffer() ):
    global reset
    buffer = event.widget
    i = buffer.index( 'insert' )
    t , t1 = i.split( '.' )
    
    if killbuffer:
        if which == 'c':
            reset = True
            txt = kb.next()
            buffer.tag_delete( 'kb' )
            buffer.insert( frm, txt, ('kb') )
            buffer.mark_set( 'insert', i )
        else:
            txt = kb.next()
            t1 = str( int( t1 ) + len( txt ) )
            r = buffer.tag_ranges( 'kb' )
            if r and r[ 0 ] == i:
                buffer.delete( r[ 0 ], r[ -1 ] )
            buffer.tag_delete( 'kb' )
            buffer.insert( frm, txt, ('kb') )
            buffer.mark_set( 'insert', i )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.36:walkKB
#@+node:mork.20041014112843.37:killsentence
def killsentence( event, back = False ):
    buffer = event.widget
    i = buffer.search( '.' , 'insert', stopindex = 'end' )
    if back:
        i = buffer.search( '.' , 'insert', backwards = True, stopindex = '1.0' ) 
        if i == '':
            return 'break'
        i2 = buffer.search( '.' , i, backwards = True , stopindex = '1.0' )
        if i2 == '':
            i2 = '1.0'
            return kill( event, i2, '%s + 1c' % i )
    else:
        i = buffer.search( '.' , 'insert', stopindex = 'end' )
        i2 = buffer.search( '.', 'insert', backwards = True, stopindex = '1.0' )
    if i2 == '':
       i2 = '1.0'
    else:
       i2 = i2 + ' + 1c '
    if i == '': return 'break'
    return kill( event, i2, '%s + 1c' % i )
#@-node:mork.20041014112843.37:killsentence
#@+node:mork.20041014112843.38:search
def search( event, way ):
    buffer = event.widget
    svar, label = getSvarLabel( event )
    stext = svar.get()
    if stext == '': return 'break'
    if way == 'bak':
        i = buffer.search( stext, 'insert', backwards = True,  stopindex = '1.0' )
    else:
        if buffer.index( 'insert + 1c' ) == buffer.index( 'end' ):
            i = buffer.search(  stext, "insert", stopindex = 'end') 
        else:
            i = buffer.search(  stext, "insert + 1c", stopindex = 'end') 
    if i in string.whitespace : return 'break'
    buffer.mark_set( 'insert', i )
    buffer.see( 'insert' )
#@-node:mork.20041014112843.38:search
#@+node:mork.20041014112843.39:capitalize
def capitalize( event, which ):
    buffer = event.widget
    text = buffer.get( 'insert wordstart', 'insert wordend' )
    i = buffer.index( 'insert' )
    if text == ' ': return 'break'
    buffer.delete( 'insert wordstart', 'insert wordend' )
    if which == 'cap':
        text = text.capitalize() 
    if which == 'low':
        text = text.lower()
    if which == 'up':
        text = text.upper()
    buffer.insert( 'insert', text )
    buffer.mark_set( 'insert', i )    
    return 'break'
#@-node:mork.20041014112843.39:capitalize
#@+node:mork.20041014112843.40:swapWords
def swapWords( event , swapspots ):
    buffer = event.widget
    txt = buffer.get( 'insert wordstart', 'insert wordend' )
    if txt == ' ' : return 'break'
    i = buffer.index( 'insert wordstart' )
    if len( swapspots ) != 0:
        def swp( find, ftext, lind, ltext ):
            buffer.delete( find, '%s wordend' % find )
            buffer.insert( find, ltext )
            buffer.delete( lind, '%s wordend' % lind )
            buffer.insert( lind, ftext )
            swapspots.pop()
            swapspots.pop()
            return 'break'
        if buffer.compare( i , '>', swapspots[ 1 ] ):
            return swp( i, txt, swapspots[ 1 ], swapspots[ 0 ] )
        elif buffer.compare( i , '<', swapspots[ 1 ] ):
            return swp( swapspots[ 1 ], swapspots[ 0 ], i, txt )
        else:
            return 'break'
    else:
        swapspots.append( txt )
        swapspots.append( i )
        return 'break'
#@-node:mork.20041014112843.40:swapWords
#@+node:mork.20041014112843.41:getHelpText
def getHelpText():
            '''This returns a string that describes what all the
            keystrokes do with a bound Text widget.'''
            help = [ 'Buffer Keyboard Commands:',
            '----------------------------------------\n',
            '<Control-p>: move up one line',
            '<Control-n>: move down one line',
            '<Control-f>: move forward one char',
            '<Conftol-b>: move backward one char',
            '<Control-o>: insert newline',
            '<Control-Alt-o> : insert newline and indent',
            '<Alt-<> : move to start of Buffer',
            '<Alt- >' +' >: move to end of Buffer',
            '<Control a>: move to start of line',
            '<Control e> :move to end of line',
            '<Alt-Up>: move to start of line',
            '<Alt-Down>: move to end of line',
            '<Alt b>: move one word backward',
            '<Alt f> : move one word forward',
            '<Control - Right Arrow>: move one word forward',
            '<Control - Left Arrow>: move one word backwards',
            '<Alt-m> : move to beginning of indentation',
            '<Alt-g> : goto line number',
            '<Control-v>: scroll forward one screen',
            '<Alt-v>: scroll up one screen',
            '<Alt-a>: move back one sentence',
            '<Alt-e>: move forward one sentence',
            '<Alt-}>: move forward one paragraph',
            '<Alt-{>: move backwards one paragraph',
            '<Control-x . >: set fill prefix',
            '<Alt-q>: fill paragraph',
            '<Alt-h>: select current or next paragraph',
            '<Control-x Control-@>: pop global mark',
            '<Control-u>: universal command',
            '<Alt -n > : n is a number.  Functions like universal command',
            '<Control-x (>: start definition of kbd macro',
            '<Control-x ) > : stop definition of kbd macro',
            '<Control-u Control-x ( >: execute last macro and edit',
            '''<Control-x u > : advertised undo.   This function utilizes the environments.
              If the buffer is not configure explicitly, there is no operation.''',
              '<Control-_>: advertised undo.  See above',
            '----------------------------------------\n',
            '<Delete> : delete previous character',
            '<Control d>: delete next character',
            '<Control k> : delete from cursor to end of line. Text goes to kill buffer',
            '<Alt d>: delete word. Word goes to kill buffer',
            '<Alt Delete>: delete previous word. Word goes to kill buffer',
            '<Alt k >: delete current sentence. Sentence goes to kill buffer',
            '<Control x Delete>: delete previous sentence. Sentence goes to kill buffer',
            '<Control y >: yank last deleted text segment from\n kill buffer and inserts it.',
            '<Alt y >: cycle and yank through kill buffer.\n',
            '<Alt z >: zap to typed letter. Text goes to kill buffer',
            '<Alt-^ >: join this line to the previous one',
            '<Alt-\ >: delete surrounding spaces',
            '<Control-Alt-w>: next kill is appended to kill buffer\n'
            
            '----------------------------------------\n',
            '<Alt c>: Capitalize the word the cursor is under.',
            '<Alt u>: Uppercase the characters in the word.',
            '<Alt l>: Lowercase the characters in the word.',
             '----------------------------------------\n',
             '<Alt t>: Mark word for word swapping.  Marking a second\n word will swap this word with the first',
             '<Control-t>: Swap characters',
             '<Ctrl-@>: Begin marking region.',
             '<Ctrl-W>: Kill marked region',
             '<Alt-W>: Copy marked region',
             '<Ctrl-x Ctrl-u>: uppercase a marked region',
             '<Ctrl-x Ctrl-l>: lowercase a marked region',
             '<Ctrl-x h>: mark entire buffer',
             '<Alt-Ctrl-backslash>: indent region to indentation of line 1 of the region.',
             '<Ctrl-x tab> : indent region by 1 tab',
             '<Control-x Control-x> : swap point and mark',
             '<Control-x semicolon>: set comment column',
             '<Alt-semicolon>: indent to comment column',
              '----------------------------------------\n',
             '<Control-x a e>: expand abbreviation before point',
             '<Control-x a g>: set abbreviation for previous word',
             '<Control-x a i g>: set word as abbreviation for word',                        
            '----------------------------------------\n',
            '<Control s>: forward search, using pattern in Mini buffer.\n',
            '<Control r>: backward search, using pattern in Mini buffer.\n' ,
            '''<Alt-%>: begin query search/replace. n skips to next match. y changes current match.  
            q or Return exits. ! to replace all remaining matches with no more questions''',
            '<Alt-=>: count lines and characters in regions',
            '<Alt-( >: insert parentheses()',
            '<Alt-) >:  move past close',
            '<Control-x Control-t>: transpose lines.',
            '<Control-x Control-o>: delete blank lines' ,
            '<Control-x r s>: save region to register',
            '<Control-x r i>: insert to buffer from register',
            '<Control-x r +>: increment register',
            '<Control-x r n>: insert number 0 to register',
            '<Control-x r space > : point insert point to register',
            '<Control-x r j > : jump to register',
            '<Control-x x>: save region to register',
            '<Control-x r r> : save rectangle to register',
            '<Control-x r o>: open up rectangle',
            '<Control-x r c> : clear rectangle',
            '<Control-x r d> : delete rectangle',
            '<Control-x r t> : replace rectangle with string',
            '<Control-x r k> : kill rectangle',
            '<Control-x r y> : yank rectangle',
            '<Control-g> : keyboard quit\n',
            '<Control-x = > : position of cursor',
            '<Control-x . > : set fill prefix',
             '----------------------------------------\n',
             '<Alt - - Alt-l >: lowercase previous word',
             '<Alt - - Alt-u>: uppercase previous word',
             '<Alt - - Alt-c>: capitalise previous word',
             '----------------------------------------\n',
             '<Alt-/ >: dynamic expansion',
             '<Control-Alt-/>: dynamic expansion.  Expands to common prefix in buffer\n'
             '----------------------------------------\n',
             'Alt-x commands:\n'
             'replace-string  -  replace string with string',
             'append-to-register  - append region to register',
             'prepend-to-register - prepend region to register\n'
             'sort-lines - sort selected lines',
             'sort-columns - sort by selected columns',
             'reverse-region - reverse selected lines',
             'sort-fields  - sort by fields',
             'abbrev-mode - toggle abbrev mode on/off',
             'kill-all-abbrevs - kill current abbreviations',
             'expand-region-abbrevs - expand all abrevs in region',
             'read-abbrev-file - read abbreviations from file',
             'write-abbrev-file - write abbreviations to file',
             'list-abbrevs   - list abbrevs in minibuffer',
             'fill-region-as-paragraph - treat region as one paragraph and add fill prefix',
             'fill-region - fill paragraphs in region with fill prefix',
             'close-rectangle  - close whitespace rectangle',
             'how-many - counts occurances of python regular expression',
             'kill-paragraph - delete from cursor to end of paragraph',
             'backward-kill-paragraph - delete from cursor to start of paragraph',
            ]
            return '\n'.join( help )
#@-node:mork.20041014112843.41:getHelpText
#@+node:mork.20041014112843.42:addToKillBuffer
killbuffer = []
def addToKillBuffer( text ):
    global reset
    reset = True
    if previousStroke in ( '<Control-k>', '<Control-w>' ,
     '<Alt-d>', '<Alt-Delete', '<Alt-z>', '<Delete>',
     '<Control-Alt-w>' ) and len( killbuffer):
        killbuffer[ 0 ] = killbuffer[ 0 ] + text
        return
    killbuffer.insert( 0, text )
#@-node:mork.20041014112843.42:addToKillBuffer
#@+node:mork.20041014112843.43:masterCommand
controlx = False
csr = { '<Control-s>': 'for', '<Control-r>':'bak' }
pref = None
zap = False
goto = False
previousStroke = ''
def masterCommand( event, method , stroke): 
    global previousStroke, regXKey
    if macroing:
        if macroing == 2 and stroke != '<Control-x>':
            return nameLastMacro( event )
        elif macroing == 3 and stroke != '<Control-x>':
            return getMacroName( event )
        else:
            recordKBDMacro( event, stroke )
    
    if  stroke == '<Control-g>':
        previousStroke = stroke
        return stopControlX( event )
                   
    if uC:
        previousStroke = stroke
        return universalDispatch( event, stroke )
    
    if controlx:
        previousStroke = stroke
        return doControlX( event, stroke )
        
        
    if stroke in ('<Control-s>', '<Control-r>' ): 
        previousStroke = stroke
        return startIncremental( event, stroke )
            
    if  isearch:
       return  iSearch( event )
       
    if stroke == '<Alt-g>':
        previousStroke = stroke
        return startGoto( event )
    if goto:
        return Goto( event )
    
    if stroke == '<Alt-z>':
        previousStroke = stroke
        return startZap( event )

    if zap:
        return zapTo( event )
        
    if regXRpl:
        try:
            regXKey = event.keysym
            regXRpl.next()
        finally:
            return 'break'

    if howM:
        return howMany( event )
        
    if abbrevMode:
        return abbrevCommand1( event )
        
    if altx:
        return doAlt_X( event )

    if stroke == '<Alt-percent>':
        previousStroke = stroke
        return masterQR( event )  
    if qlisten:
        return masterQR( event )
        
    if rString:
        return replaceString( event )
     
    if negativeArg:
        return negativeArgument( event, stroke )
    
    if stroke == '<Control-Alt-w>':
        previousStroke = '<Control-Alt-w>'   
        return 'break' 
        
    if abbrevOn:
        if expandAbbrev( event ) :
            return 'break'       
        
    if method:
        rt = method( event )
        previousStroke = stroke
        return rt
#@-node:mork.20041014112843.43:masterCommand
#@-node:ekr.20041028083211.5:Editing commands
#@+node:ekr.20041028083211.6:Register commands...
#@+node:mork.20041014112843.44:copyToRegister
def copyToRegister( event ):
    if not _chckSel( event ):
        return
    if event.keysym in string.letters:
        event.keysym = event.keysym.lower()
        buffer = event.widget
        txt = buffer.get( 'sel.first', 'sel.last' )
        registers[ event.keysym ] = txt
        return 
    stopControlX( event )
#@-node:mork.20041014112843.44:copyToRegister
#@+node:mork.20041014112843.45:copyRectangleToRegister
def copyRectangleToRegister( event ):
    if not _chckSel( event ):
        return
    if event.keysym in string.letters:
        event.keysym = event.keysym.lower()
        buffer = event.widget
        r1, r2, r3, r4 = getRectanglePoints( event )
        rect = []
        while r1 <= r3:
            txt = buffer.get( '%s.%s' %( r1, r2 ), '%s.%s' %( r1, r4 ) )
            rect.append( txt )
            r1 = r1 +1
        registers[ event.keysym ] = rect
    stopControlX( event )        
#@-node:mork.20041014112843.45:copyRectangleToRegister
#@+node:mork.20041014112843.46:prependToRegister
def prependToRegister( event ):
    global regMeth, registermode, controlx, registermode
    event.keysym = 'p'
    setNextRegister( event )
    controlx = True
#@-node:mork.20041014112843.46:prependToRegister
#@+node:mork.20041014112843.47:appendToRegister
def appendToRegister( event ):
    global regMeth, registermode, controlx
    event.keysym = 'a'
    setNextRegister( event )
    controlx = True
#@-node:mork.20041014112843.47:appendToRegister
#@+node:mork.20041014112843.48:_chckSel
def _chckSel( event ):
     if not 'sel' in event.widget.tag_names():
        return False
     if not event.widget.tag_ranges( 'sel' ):
        return False  
     return True
#@-node:mork.20041014112843.48:_chckSel
#@+node:mork.20041014112843.49:_ToReg
def _ToReg( event , which):
    if not _chckSel( event ):
        return
    if _checkIfRectangle( event ):
        return
    if event.keysym in string.letters:
        event.keysym = event.keysym.lower()
        buffer = event.widget
        if not registers.has_key( event.keysym ):
            registers[ event.keysym ] = ''
        txt = buffer.get( 'sel.first', 'sel.last' )
        rtxt = registers[ event.keysym ]
        if which == 'p':
            txt = txt + rtxt
        else:
            txt = rtxt + txt
        registers[ event.keysym ] = txt
        return
#@-node:mork.20041014112843.49:_ToReg
#@+node:mork.20041014112843.50:_checkIfRectangle
def _checkIfRectangle( event ):
    if registers.has_key( event.keysym ):
        if isinstance( registers[ event.keysym ], list ):
            svar, label = getSvarLabel( event )
            stopControlX( event )
            svar.set( "Register contains Rectangle, not text" )
            return True
    return False           
#@-node:mork.20041014112843.50:_checkIfRectangle
#@+node:mork.20041014112843.51:insertFromRegister
def insertFromRegister( event ):
    buffer = event.widget
    if registers.has_key( event.keysym ):
        if isinstance( registers[ event.keysym ], list ):
            yankRectangle( event, registers[ event.keysym ] )
        else:
            buffer.insert( 'insert', registers[ event.keysym ] )
            buffer.event_generate( '<Key>' )
            buffer.update_idletasks()
    stopControlX( event )
#@-node:mork.20041014112843.51:insertFromRegister
#@+node:mork.20041014112843.52:incrementRegister
def incrementRegister( event ):
    if registers.has_key( event.keysym ):
        if _checkIfRectangle( event ):
            return
        if registers[ event.keysym ] in string.digits:
            i = registers[ event.keysym ]
            i = str( int( i ) + 1 )
            registers[ event.keysym ] = i
        else:
            invalidRegister( event, 'number' )
            return
    stopControlX( event )
#@-node:mork.20041014112843.52:incrementRegister
#@+node:mork.20041014112843.53:numberToRegister
def numberToRegister( event ):
    if event.keysym in string.letters:
        registers[ event.keysym.lower() ] = str( 0 )
    stopControlX( event )
#@-node:mork.20041014112843.53:numberToRegister
#@+node:mork.20041014112843.54:pointToRegister
def pointToRegister( event ):
    if event.keysym in string.letters:
        buffer = event.widget
        registers[ event.keysym.lower() ] = buffer.index( 'insert' )
    stopControlX( event )
#@-node:mork.20041014112843.54:pointToRegister
#@+node:mork.20041014112843.55:jumpToRegister
def jumpToRegister( event ):
    if event.keysym in string.letters:
        if _checkIfRectangle( event ):
            return
        buffer = event.widget
        i = registers[ event.keysym.lower() ]
        i2 = i.split( '.' )
        if len( i2 ) == 2:
            if i2[ 0 ].isdigit() and i2[ 1 ].isdigit():
                pass
            else:
                invalidRegister( event, 'index' )
                return
        else:
            invalidRegister( event, 'index' )
            return
        buffer.mark_set( 'insert', i )
        buffer.event_generate( '<Key>' )
        buffer.update_idletasks() 
    stopControlX( event ) 
#@-node:mork.20041014112843.55:jumpToRegister
#@+node:mork.20041014112843.56:invalidRegister
def invalidRegister( event, what ):
    deactivateRegister( event )
    svar, label = getSvarLabel( event )
    svar.set( 'Register does not contain valid %s'  % what)
    return    
#@-node:mork.20041014112843.56:invalidRegister
#@+node:mork.20041014112843.57:setNextRegister
regMeth = None
regMeths = {
's' : copyToRegister,
'i' : insertFromRegister,
'n': numberToRegister,
'plus': incrementRegister,
'space': pointToRegister,
'j': jumpToRegister,
'a': lambda event , which = 'a': _ToReg( event, which ),
'p': lambda event , which = 'p': _ToReg( event, which ),
'r': copyRectangleToRegister
}    

regText = {
's' : 'copy to register',
'i' : 'insert from register',
'plus': 'increment register',
'n' : 'number to register',
'p' : 'prepend to register',
'a' : 'append to register',
'space' : 'point to register',
'j': 'jump to register',
'r': 'rectangle to register'
}
def setNextRegister( event ):
    global regMeth, registermode
    if event.keysym == 'Shift':
        return
    if regMeths.has_key( event.keysym ):
        regMeth = regMeths[ event.keysym ]
        registermode = 2
        svar = svars[ event.widget ]
        svar.set( regText[ event.keysym ] )
        return
    stopControlX( event )
#@-node:mork.20041014112843.57:setNextRegister
#@+node:mork.20041014112843.58:executeRegister
def executeRegister( event ):
    regMeth( event )
    if registermode: 
        stopControlX( event )
    return
#@-node:mork.20041014112843.58:executeRegister
#@+node:mork.20041014112843.59:deactivateRegister
def deactivateRegister( event ):
    global registermode, regMeth
    svar, label = getSvarLabel( event )
    svar.set( '' )
    setLabelGrey( label )
    registermode = False
    regMeth = None
#@-node:mork.20041014112843.59:deactivateRegister
#@-node:ekr.20041028083211.6:Register commands...
#@+node:ekr.20041028083211.7:Abbreviations
#@+node:mork.20041014112843.60:abbreviationDispatch
def abbreviationDispatch( event, which ):
    global abbrevMode
    if not abbrevMode:
        abbrevMode = which
        svar, label = getSvarLabel( event )
        svar.set( '' )
        setLabelBlue( label )
        return 'break'
    if abbrevMode:
        abbrevCommand1( event )
    return 'break'
#@-node:mork.20041014112843.60:abbreviationDispatch
#@+node:mork.20041014112843.61:abbrevCommand1
def abbrevCommand1( event ):
    global abbrevMode
    if event.keysym == 'Return':
        buffer = event.widget
        word = buffer.get( 'insert -1c wordstart', 'insert -1c wordend' )
        if word == ' ': return
        svar, label = getSvarLabel( event )
        if abbrevMode == 1:
            abbrevs[ svar.get() ] = word
        elif abbrevMode == 2:
            abbrevs[ word ] = svar.get()
        abbrevMode = False
        resetMiniBuffer( event )
        return 'break'
    svar, label = getSvarLabel( event )
    setSvar( event, svar )
    return 'break'
#@-node:mork.20041014112843.61:abbrevCommand1
#@+node:mork.20041014112843.62:expandAbbrev
def expandAbbrev( event ):
    buffer = event.widget
    word = buffer.get( 'insert -1c wordstart', 'insert -1c wordend' )
    word = '%s%s' %( word, event.char )
    if abbrevs.has_key( word ):
        buffer.delete( 'insert -1c wordstart', 'insert -1c wordend' )
        buffer.insert( 'insert', abbrevs[ word ] )
        return True
    else: return False
#@-node:mork.20041014112843.62:expandAbbrev
#@+node:mork.20041014112843.63:regionalExpandAbbrev
regXRpl = None
regXKey = None
def regionalExpandAbbrev( event ):
    global regXRpl
    if not _chckSel( event ):
        return
    buffer = event.widget
    i1 = buffer.index( 'sel.first' )
    i2 = buffer.index( 'sel.last' ) 
    ins = buffer.index( 'insert' )
    def searchXR( i1 , i2, ins, event ):
        buffer.tag_add( 'sXR', i1, i2 )
        while i1:
            tr = buffer.tag_ranges( 'sXR' )
            if not tr: break
            i1 = buffer.search( r'\w', i1, stopindex = tr[ 1 ] , regexp = True )
            if i1:
                word = buffer.get( '%s wordstart' % i1, '%s wordend' % i1 )
                buffer.tag_delete( 'found' )
                buffer.tag_add( 'found',  '%s wordstart' % i1, '%s wordend' % i1 )
                buffer.tag_config( 'found', background = 'yellow' )
                if abbrevs.has_key( word ):
                    svar, label = getSvarLabel( event )
                    svar.set( 'Replace %s with %s? y/n' % ( word, abbrevs[ word ] ) )
                    yield None
                    if regXKey == 'y':
                        ind = buffer.index( '%s wordstart' % i1 )
                        buffer.delete( '%s wordstart' % i1, '%s wordend' % i1 )
                        buffer.insert( ind, abbrevs[ word ] )
                i1 = '%s wordend' % i1
        buffer.mark_set( 'insert', ins )
        buffer.selection_clear()
        buffer.tag_delete( 'sXR' )
        buffer.tag_delete( 'found' )
        svar, label = getSvarLabel( event )
        svar.set( '' )
        setLabelGrey( label )
        _setRAvars()
    regXRpl = searchXR( i1, i2, ins, event)
    regXRpl.next()
    return 'break' 
#@-node:mork.20041014112843.63:regionalExpandAbbrev
#@+node:mork.20041014112843.64:_setRAvars
def _setRAvars():
    global regXRpl, regXKey
    regXRpl = regXKey = None 
#@-node:mork.20041014112843.64:_setRAvars
#@+node:mork.20041014112843.65:killAllAbbrevs
def killAllAbbrevs( event ):
    global abbrevs
    abbrevs = {}
#@-node:mork.20041014112843.65:killAllAbbrevs
#@+node:mork.20041014112843.66:toggleAbbrevMode
def toggleAbbrevMode( event ):
    global abbrevOn
    if abbrevOn:
        abbrevOn = False
    else:
        abbrevOn = True
#@-node:mork.20041014112843.66:toggleAbbrevMode
#@+node:mork.20041014112843.67:listAbbrevs
def listAbbrevs( event ):
    svar, label = getSvarLabel( event )
    txt = ''
    for z in abbrevs:
        txt = '%s%s=%s\n' %( txt, z, abbrevs[ z ] )
    svar.set( '' )
    svar.set( txt )
    return 'break'
#@-node:mork.20041014112843.67:listAbbrevs
#@+node:mork.20041014112843.68:readAbbreviations
def readAbbreviations( event ):

    f = tkFileDialog.askopenfile()
    if f == None: return 'break'        
    return _readAbbrevs( f )
#@nonl
#@-node:mork.20041014112843.68:readAbbreviations
#@+node:mork.20041014112843.69:_readAbbrevs
def _readAbbrevs( f ):
    for x in f:
        a, b = x.split( '=' )
        b = b[ : -1 ]
        abbrevs[ a ] = b
    f.close()        
    return 'break'
#@-node:mork.20041014112843.69:_readAbbrevs
#@+node:mork.20041014112843.70:writeAbbreviations
def writeAbbreviations( event ):

    f = tkFileDialog.asksaveasfile() 
    if f == None: return 'break' 
    return _writeAbbrevs( f )
#@-node:mork.20041014112843.70:writeAbbreviations
#@+node:mork.20041014112843.71:_writeAbbrevs
def _writeAbbrevs( f ):
    print abbrevs
    for x in abbrevs:
        f.write( '%s=%s\n' %( x, abbrevs[ x ] ) )
    f.close()    
    return 'break'
#@-node:mork.20041014112843.71:_writeAbbrevs
#@-node:ekr.20041028083211.7:Abbreviations
#@+node:ekr.20041028083211.8:Paragraph commands...
#@+node:mork.20041014112843.72:movingParagraphs
def movingParagraphs( event, way ):
    buffer = event.widget
    i = buffer.index( 'insert' )
    
    if way == 1:
        while 1:
            txt = buffer.get( '%s linestart' % i, '%s lineend' %i )
            txt = txt.rstrip().lstrip()
            if not txt:
                i = buffer.search( r'\w', i, regexp = True, stopindex = 'end' )
                i = '%s' %i
                break
            else:
                i = buffer.index( '%s + 1 lines' % i )
                if buffer.index( '%s linestart' % i ) == buffer.index( 'end' ):
                    i = buffer.search( r'\w', 'end', backwards = True, regexp = True, stopindex = '1.0' )
                    i = '%s + 1c' % i
                    break
    else:
        while 1:
            txt = buffer.get( '%s linestart' % i, '%s lineend' %i )
            txt = txt.rstrip().lstrip()
            if not txt:
                i = buffer.search( r'\w', i, backwards = True, regexp = True, stopindex = '1.0' )
                i = '%s +1c' %i
                break
            else:
                i = buffer.index( '%s - 1 lines' % i )
                if buffer.index( '%s linestart' % i ) == '1.0':
                    i = buffer.search( r'\w', '1.0', regexp = True, stopindex = 'end' )
                    break
    if i : 
        buffer.mark_set( 'insert', i )
        buffer.see( 'insert' )
        return _tailEnd( buffer )
    return 'break'
#@-node:mork.20041014112843.72:movingParagraphs
#@+node:mork.20041014112843.73:setFillPrefix
fillPrefix = ''
def setFillPrefix( event ):
    global fillPrefix
    buffer = event.widget
    txt = buffer.get( 'insert linestart', 'insert' )
    fillPrefix = txt
    return 'break'
#@-node:mork.20041014112843.73:setFillPrefix
#@+node:mork.20041014112843.74:fillParagraph
def fillParagraph( event ):
    buffer = event.widget
    txt = buffer.get( 'insert linestart', 'insert lineend' )
    txt = txt.lstrip().rstrip()
    if txt:
        i = buffer.index( 'insert' )
        i2 = i
        txt2 = txt
        while txt2:
            pi2 = buffer.index( '%s - 1 lines' % i2)
            txt2 = buffer.get( '%s linestart' % pi2, '%s lineend' % pi2 )
            if buffer.index( '%s linestart' % pi2 ) == '1.0':
                i2 = buffer.search( '\w', '1.0', regexp = True, stopindex = 'end' )
                break
            if txt2.lstrip().rstrip() == '': break
            i2 = pi2
        i3 = i
        txt3 = txt
        while txt3:
            pi3 = buffer.index( '%s + 1 lines' %i3 )
            txt3 = buffer.get( '%s linestart' % pi3, '%s lineend' % pi3 )
            if buffer.index( '%s lineend' % pi3 ) == buffer.index( 'end' ):
                i3 = buffer.search( '\w', 'end', backwards = True, regexp = True, stopindex = '1.0' )
                break
            if txt3.lstrip().rstrip() == '': break
            i3 = pi3
        ntxt = buffer.get( '%s linestart' %i2, '%s lineend' %i3 )
        ntxt = _addPrefix( ntxt )
        buffer.delete( '%s linestart' %i2, '%s lineend' % i3 )
        buffer.insert( i2, ntxt )
        buffer.mark_set( 'insert', i )
        return _tailEnd( buffer )
#@-node:mork.20041014112843.74:fillParagraph
#@+node:mork.20041014112843.75:_addPrefix
def _addPrefix( ntxt ):
        ntxt = ntxt.split( '.' )
        ntxt = map( lambda a: fillPrefix+a, ntxt )
        ntxt = '.'.join( ntxt )               
        return ntxt
#@-node:mork.20041014112843.75:_addPrefix
#@+node:mork.20041014112843.76:fillRegionAsParagraph
def fillRegionAsParagraph( event ):
    if not _chckSel( event ):
        return
    buffer = event.widget
    i1 = buffer.index( 'sel.first linestart' )
    i2 = buffer.index( 'sel.last lineend' )
    txt = buffer.get(  i1,  i2 )
    txt = _addPrefix( txt )
    buffer.delete( i1, i2 )
    buffer.insert( i1, txt )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.76:fillRegionAsParagraph
#@+node:mork.20041014112843.77:fillRegion
def fillRegion( event ):
    if not _chckSel( event ):
        return
    buffer = event.widget
    i = buffer.index( 'insert' ) 
    s1 = buffer.index( 'sel.first' )
    s2 = buffer.index( 'sel.last' )
    buffer.mark_set( 'insert', s1 )
    movingParagraphs( event, -1 )
    if buffer.index( 'insert linestart' ) == '1.0':
        fillParagraph( event )
    while 1:
        movingParagraphs( event, 1 )
        if buffer.compare( 'insert', '>', s2 ):
            break
        fillParagraph( event )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.77:fillRegion
#@+node:mork.20041014112843.78:doControlX
registermode = False
def doControlX( event, stroke, previous = [] ):
    global registermode
    previous.insert( 0, event.keysym )
    if len( previous ) > 10: previous.pop()
    if stroke == '<Key>':
        if event.keysym in ( 'Shift_L', 'Shift_R' ):
            return
        if event.keysym == 'period':
            stopControlX( event )
            return setFillPrefix( event )
        if event.keysym == 'parenleft':
            stopControlX( event )
            return startKBDMacro( event )
        if event.keysym == 'parenright':
            stopControlX( event )
            return stopKBDMacro( event )
        if event.keysym == 'semicolon':
            stopControlX( event )
            return setCommentColumn( event )
        if event.keysym == 'Tab':
            stopControlX( event )
            return tabIndentRegion( event )
        if sRect:
            stringRectangle( event )
            return 'break'
        if event.keysym in ( 'a', 'i' , 'e'):
            svar, label = getSvarLabel( event )
            if svar.get() != 'a' and event.keysym == 'a':
                svar.set( 'a' )
                return 'break'
            elif svar.get() == 'a':
                if event.char == 'i':
                    svar.set( 'a i' )
                elif event.char == 'e':
                    stopControlX( event )
                    event.char = ''
                    expandAbbrev( event )
                return 'break'
        if event.keysym == 'g':
            svar, label = getSvarLabel( event )
            l = svar.get()
            if l == 'a':
                stopControlX( event )
                return abbreviationDispatch( event, 1 )
            elif l == 'a i':
                stopControlX( event )
                return abbreviationDispatch( event, 2 )
        if event.keysym == 'e':
            stopControlX( event )
            return executeLastMacro( event )
        if event.keysym == 'x' and previous[ 1 ] not in ( 'Control_L', 'Control_R'):
            event.keysym = 's' 
            setNextRegister( event )
            return 'break'
        if event.keysym == 'o' and registermode == 1:
            openRectangle( event )
            return 'break'
        if event.keysym == 'c' and registermode == 1:
            clearRectangle( event )
            return 'break'
        if event.keysym == 't' and registermode == 1:
            stringRectangle( event )
            return 'break'
        if event.keysym == 'y' and registermode == 1:
            yankRectangle( event )
            return 'break'
        if event.keysym == 'd' and registermode == 1:
            deleteRectangle( event )
            return 'break'
        if event.keysym == 'k' and registermode == 1:
            killRectangle( event )
            return 'break'       
        if registermode == 1:
            setNextRegister( event )
            return 'break'
        elif registermode == 2:
            executeRegister( event )
            return 'break'
        if event.keysym == 'r':
            registermode = 1
            svar = svars[ event.widget ]
            svar.set( 'C - x r' )
            return 'break'
        if event.keysym== 'h':
           stopControlX( event )
           event.widget.tag_add( 'sel', '1.0', 'end' )
           return 'break' 
        if event.keysym == 'equal':
            lineNumber( event )
            return 'break'
        if event.keysym == 'u':
            stopControlX( event )
            return doUndo( event, 2 )
    if stroke in xcommands:
        xcommands[ stroke ]( event )
        stopControlX( event )
    return 'break'
#@-node:mork.20041014112843.78:doControlX
#@-node:ekr.20041028083211.8:Paragraph commands...
#@+node:ekr.20041028083211.9:Search...
#@+node:mork.20041014112843.79:startIncremental
def startIncremental( event, stroke ):
    global isearch, pref
    widget = event.widget
    if isearch:
        search( event, way = csr[ stroke ] )
        pref = csr[ stroke ]
        scolorizer( event )
        return 'break'
    else:
        svar, label = getSvarLabel( event )
        isearch = True
        pref = csr[ stroke ]
        label.configure( background = 'lightblue' )
        label.configure( textvariable = svars )
        return 'break'
#@-node:mork.20041014112843.79:startIncremental
#@+node:mork.20041014112843.80:iSearch
def iSearch( event ):
    if len( event.char ) == 0: return
    widget = event.widget
    svar, label = getSvarLabel( event )
    label.configure( textvariable = svar )
    if event.keysym == 'Return':
          return stopControlX( event )
    setSvar( event, svar )
    if event.char != '\b':
       stext = svar.get()
       z = widget.search( stext , 'insert' , stopindex = 'insert +%sc' % len( stext ) )
       if not z:
           search( event, pref )
    scolorizer( event )
    return 'break'
#@-node:mork.20041014112843.80:iSearch
#@+node:mork.20041014112843.81:startZap
def startZap( event ):
    global zap
    zap = True
    svar, label = getSvarLabel( event )
    label.configure( background = 'lightblue' )
    svar.set( 'Zap To Character' )
    return 'break'
#@-node:mork.20041014112843.81:startZap
#@+node:mork.20041014112843.82:zapTo
def zapTo( event ):
    global zap
    widget = event.widget
    s = string.ascii_letters + string.digits + string.punctuation
    if len( event.char ) != 0 and event.char in s:
        zap = False
        i = widget.search( event.char , 'insert',  stopindex = 'end' )
        resetMiniBuffer( event )
        if i:
            t = widget.get( 'insert', '%s+1c'% i )
            addToKillBuffer( t )
            widget.delete( 'insert', '%s+1c' % i)
            return 'break'
    else:
        return 'break'
#@nonl
#@-node:mork.20041014112843.82:zapTo
#@+node:mork.20041014112843.83:changecbDict
def changecbDict( changes ):
    for z in changes:
        if cbDict.has_key( z ):
            cbDict[ z ] = changes[ z ]
#@-node:mork.20041014112843.83:changecbDict
#@+node:mork.20041014112843.84:startControlX
def startControlX( event ):  
    global controlx
    controlx = True
    svar, label = getSvarLabel( event )
    svar.set( 'Control - X' )
    label.configure( background = 'lightblue' )
    return 'break'
#@-node:mork.20041014112843.84:startControlX
#@+node:mork.20041014112843.85:stopControlX
def stopControlX( event ): 
    global controlx, rstring, isearch, sRect,negativeArg, uC, howM, altx
    altx = False
    howM = False
    controlx = False
    isearch = False
    sRect = False
    uC = False
    negativeArg = False
    event.widget.tag_delete( 'color' )
    event.widget.tag_delete( 'color1' )
    if registermode:
        deactivateRegister( event )
    rString = False
    resetMiniBuffer( event )
    return 'break'
#@-node:mork.20041014112843.85:stopControlX
#@+node:mork.20041014112843.86:resetMiniBuffer
def resetMiniBuffer( event ):
    svar, label = getSvarLabel( event )
    svar.set( '' )
    label.configure( background = 'lightgrey' )
#@-node:mork.20041014112843.86:resetMiniBuffer
#@+node:mork.20041014112843.87:setRegion
def setRegion( event ):   
    mrk = 'sel'
    buffer = event.widget
    def extend( event ):
        widget = event.widget
        widget.mark_set( 'insert', 'insert + 1c' )
        if inRange( widget, mrk ):
            widget.tag_remove( mrk, 'insert -1c' )
        else:
            widget.tag_add( mrk, 'insert -1c' )
            widget.tag_configure( mrk, background = 'lightgrey' )
            testinrange( widget )
        return 'break'
        
    def truncate( event ):
        widget = event.widget
        widget.mark_set( 'insert', 'insert -1c' )
        if inRange( widget, mrk ):
            testinrange( widget )
            widget.tag_remove( mrk, 'insert' )
        else:
            widget.tag_add( mrk, 'insert' )
            widget.tag_configure( mrk, background = 'lightgrey' )
            testinrange( widget  )
        return 'break'
        
    def up( event ):
        widget = event.widget
        if not testinrange( widget ):
            return 'break'
        widget.tag_add( mrk, 'insert linestart', 'insert' )
        i = widget.index( 'insert' )
        i1, i2 = i.split( '.' )
        i1 = str( int( i1 ) - 1 )
        widget.mark_set( 'insert', i1+'.'+i2)
        widget.tag_add( mrk, 'insert', 'insert lineend + 1c' )
        if inRange( widget, mrk ,l = '-1c', r = '+1c') and widget.index( 'insert' ) != '1.0':
            widget.tag_remove( mrk, 'insert', 'end' )  
        return 'break'
        
    def down( event ):
        widget = event.widget
        if not testinrange( widget ):
            return 'break'
        widget.tag_add( mrk, 'insert', 'insert lineend' )
        i = widget.index( 'insert' )
        i1, i2 = i.split( '.' )
        i1 = str( int( i1 ) + 1 )
        widget.mark_set( 'insert', i1 +'.'+i2 )
        widget.tag_add( mrk, 'insert linestart -1c', 'insert' )
        if inRange( widget, mrk , l = '-1c', r = '+1c' ): 
            widget.tag_remove( mrk, '1.0', 'insert' )
        return 'break'
        
    extend( event )   
    buffer.bind( '<Right>', extend, '+' )
    buffer.bind( '<Left>', truncate, '+' )
    buffer.bind( '<Up>', up, '+' )
    buffer.bind( '<Down>', down, '+' )
    return 'break'
#@-node:mork.20041014112843.87:setRegion
#@+node:mork.20041014112843.88:inRange
def inRange( widget, range, l = '', r = '' ):
    ranges = widget.tag_ranges( range )
    i = widget.index( 'insert' )
    for z in xrange( 0,  len( ranges) , 2 ):
        z1 = z + 1
        l1 = 'insert%s' %l
        r1 = 'insert%s' % r
        if widget.compare( l1, '>=', ranges[ z ]) and widget.compare( r1, '<=', ranges[ z1] ):
            return True
    return False
#@-node:mork.20041014112843.88:inRange
#@+node:mork.20041014112843.89:contRanges
def contRanges( widget, range ):
    ranges = widget.tag_ranges( range)
    t1 = widget.get( ranges[ 0 ], ranges[ -1 ] )
    t2 = []
    for z in xrange( 0,  len( ranges) , 2 ):
        z1 = z + 1
        t2.append( widget.get( ranges[ z ], ranges[ z1 ] ) )
    t2 = '\n'.join( t2 )
    return t1 == t2
#@-node:mork.20041014112843.89:contRanges
#@+node:mork.20041014112843.90:testinrange
def testinrange( widget ):
    mrk = 'sel'
    ranges = widget.tag_ranges( mrk)
    if not inRange( widget , mrk) or not contRanges( widget, mrk ):
        removeRKeys( widget )
        return False
    return True
#@-node:mork.20041014112843.90:testinrange
#@+node:mork.20041014112843.91:killRegion
def killRegion( event, which ):
    mrk = 'sel'
    range = event.widget.tag_ranges( mrk )
    if len( range ) != 0:
        txt = event.widget.get( range[ 0 ] , range[ -1 ] )
        if which == 'd':
            event.widget.delete( range[ 0 ], range[ -1 ] )   
        addToKillBuffer( txt )
    removeRKeys( event.widget )
    return 'break'
#@-node:mork.20041014112843.91:killRegion
#@+node:mork.20041014112843.92:removeRKeys
def removeRKeys( widget ):
    mrk = 'sel'
    widget.tag_delete( mrk )
    widget.unbind( '<Left>' )
    widget.unbind( '<Right>' )
    widget.unbind( '<Up>' )
    widget.unbind( '<Down>' )
#@-node:mork.20041014112843.92:removeRKeys
#@+node:mork.20041014112843.93:indentRegion
def indentRegion( event ):
    buffer = event.widget
    mrk = 'sel'
    range = buffer.tag_ranges( mrk )
    if len( range ) != 0:
        text = buffer.get( '%s linestart' % range[ 0 ] ,  '%s lineend' % range[ 0 ])
        sstring = text.lstrip()
        sstring = sstring[ 0 ]
        ws = text.split( sstring )
        if len( ws ) > 1:
            ws = ws[ 0 ]
        else:
            ws = ''
        s , s1 = range[ 0 ].split( '.' )
        e , e1 = range[ -1 ].split( '.' )
        s = int( s )
        s = s + 1
        e = int( e ) + 1
        for z in xrange( s , e ):
            t2 = buffer.get( '%s.0' %z ,  '%s.0 lineend'%z)
            t2 = t2.lstrip()
            t2 = ws + t2
            buffer.delete( '%s.0' % z ,  '%s.0 lineend' %z)
            buffer.insert( '%s.0' % z, t2 )
        buffer.event_generate( '<Key>' )
        buffer.update_idletasks()
    removeRKeys( buffer )
    return 'break'
#@-node:mork.20041014112843.93:indentRegion
#@+node:mork.20041014112843.94:tabIndentRegion
def tabIndentRegion( event ):
    buffer = event.widget
    if not _chckSel( event ):
        return
    i = buffer.index( 'sel.first' )
    i2 = buffer.index( 'sel.last' )
    i = buffer.index( '%s linestart' %i )
    i2 = buffer.index( '%s linestart' % i2)
    while 1:
        buffer.insert( i, '\t' )
        if i == i2: break
        i = buffer.index( '%s + 1 lines' % i )    
    return _tailEnd( buffer )
#@-node:mork.20041014112843.94:tabIndentRegion
#@+node:mork.20041014112843.95:manufactureKeyPress
def manufactureKeyPress( event, which ):
    buffer = event.widget
    buffer.event_generate( '<Key>',  keysym = which  )
    buffer.update_idletasks()
    return 'break'
#@-node:mork.20041014112843.95:manufactureKeyPress
#@+node:mork.20041014112843.96:backToIndentation
def backToIndentation( event ):
    buffer = event.widget
    i = buffer.index( 'insert linestart' )
    i2 = buffer.search( r'\w', i, stopindex = '%s lineend' % i, regexp = True )
    buffer.mark_set( 'insert', i2 )
    buffer.update_idletasks()
    return 'break'
#@-node:mork.20041014112843.96:backToIndentation
#@+node:mork.20041014112843.97:deleteIndentation
def deleteIndentation( event ):
    buffer = event.widget
    txt = buffer.get( 'insert linestart' , 'insert lineend' )
    txt = ' %s' % txt.lstrip()
    buffer.delete( 'insert linestart' , 'insert lineend +1c' )    
    i  = buffer.index( 'insert - 1c' )
    buffer.insert( 'insert -1c', txt )
    buffer.mark_set( 'insert', i )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.97:deleteIndentation
#@+node:mork.20041014112843.98:deleteNextChar
def deleteNextChar( event ):
    buffer = event.widget
    i = buffer.index( 'insert' )
    buffer.delete( i, '%s +1c' % i )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.98:deleteNextChar
#@+node:mork.20041014112843.99:deleteSpaces
def deleteSpaces( event , insertspace = False):
    buffer = event.widget
    char = buffer.get( 'insert', 'insert + 1c ' )
    if char in string.whitespace:
        i = buffer.index( 'insert' )
        wf = buffer.search( r'\w', i, stopindex = '%s lineend' % i, regexp = True )
        wb = buffer.search( r'\w', i, stopindex = '%s linestart' % i, regexp = True, backwards = True )
        if '' in ( wf, wb ):
            return 'break'
        buffer.delete( '%s +1c' %wb, wf )
        if insertspace:
            buffer.insert( 'insert', ' ' )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.99:deleteSpaces
#@+node:mork.20041014112843.100:measure
def measure( buffer ):
    i = buffer.index( 'insert' )
    i1, i2 = i.split( '.' )
    start = int( i1 )
    watch = 0
    ustart = start
    pone = 1
    top = i
    bottom = i
    while pone:
        ustart = ustart - 1
        if ustart < 0:
            break
        ds = '%s.0' % ustart
        pone = buffer.dlineinfo( ds )
        if pone:
            top = ds
            watch = watch  + 1
    
    pone = 1
    ustart = start
    while pone:
        ustart = ustart +1
        ds = '%s.0' % ustart
        pone = buffer.dlineinfo( ds )
        if pone:
            bottom = ds
            watch = watch + 1
            
    return watch , top, bottom
#@-node:mork.20041014112843.100:measure
#@+node:mork.20041014112843.101:screenscroll
def screenscroll( event, way = 'north' ):
    buffer = event.widget
    chng = measure( buffer )
    i = buffer.index( 'insert' )
    
    if way == 'north':
        top = chng[ 1 ]
        i1, i2 = i.split( '.' )
        i1 = int( i1 ) - chng[ 0 ]
    else:
        bottom = chng[ 2 ]
        i1, i2 = i.split( '.' )
        i1 = int( i1 ) + chng[ 0 ]
        
    buffer.mark_set( 'insert', '%s.%s' % ( i1, i2 ) )
    buffer.see( 'insert' )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.101:screenscroll
#@+node:mork.20041014112843.102:countRegion
def countRegion( event ):
    buffer = event.widget
    txt = buffer.get( 'sel.first', 'sel.last')
    svar = svars[ buffer ]
    lines = 1
    chars = 0
    for z in txt:
        if z == '\n': lines = lines + 1
        else:
            chars = chars + 1       
    svar.set( 'Region has %s lines, %s characters' %( lines, chars ) )
    return 'break'
#@-node:mork.20041014112843.102:countRegion
#@+node:mork.20041014112843.103:insertParentheses
def insertParentheses( event ):
    buffer = event.widget
    buffer.insert( 'insert', '()' )
    buffer.mark_set( 'insert', 'insert -1c' )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.103:insertParentheses
#@+node:mork.20041014112843.104:listenQR
qQ = None
qR = None
qlisten = False
lqR = Tkinter.StringVar()
lqR.set( 'Query with: ' )
def listenQR( event ):
    global qgetQuery, qlisten
    qlisten = True
    buffer = event.widget
    svar, label = getSvarLabel( event )
    label.configure( background = 'lightblue' , textvariable = lqR)
    qgetQuery = True
#@-node:mork.20041014112843.104:listenQR
#@+node:mork.20041014112843.105:qsearch
def qsearch( event ):
    if qQ:
        buffer = event.widget
        i = buffer.search( qQ, 'insert', stopindex = 'end' )
        buffer.tag_delete( 'qR' )
        if i:
            buffer.mark_set( 'insert', i )
            buffer.update_idletasks()
            buffer.tag_add( 'qR', 'insert', 'insert +%sc'% len( qQ ) )
            buffer.tag_config( 'qR', background = 'lightblue' )
            return True
        quitQSearch( event )
        return False
#@-node:mork.20041014112843.105:qsearch
#@+node:mork.20041014112843.106:quitQSearch
def quitQSearch( event ):
        global qQ, qR, qlisten, qrexecute
        event.widget.tag_delete( 'qR' )
        qQ = None
        qR = None
        qlisten = False
        qrexecute = False
        svar, label = getSvarLabel( event )
        svar.set( '' )
        label.configure( background = 'lightgrey' )
        event.widget.event_generate( '<Key>' )
        event.widget.update_idletasks()
#@-node:mork.20041014112843.106:quitQSearch
#@+node:mork.20041014112843.107:qreplace
def qreplace( event ):
    if event.keysym == 'y':
        _qreplace( event )
        return
    elif event.keysym in ( 'q', 'Return' ):
        quitQSearch( event )
    elif event.keysym == 'exclam':
        while qrexecute:
            _qreplace( event )
    elif event.keysym in ( 'n', 'Delete'):
        i = event.widget.index( 'insert' )
        event.widget.mark_set( 'insert', 'insert +%sc' % len( qQ ) )
        qsearch( event )
    event.widget.see( 'insert' )
#@-node:mork.20041014112843.107:qreplace
#@+node:mork.20041014112843.108:_qreplace
def _qreplace( event ):
    i = event.widget.tag_ranges( 'qR' )
    event.widget.delete( i[ 0 ], i[ 1 ] )
    event.widget.insert( 'insert', qR )
    qsearch( event )
#@-node:mork.20041014112843.108:_qreplace
#@+node:mork.20041014112843.109:getQuery
qgetQuery = False
lqQ = Tkinter.StringVar()
lqQ.set( 'Replace with:' )      
def getQuery( event ):
    global qQ, qgetQuery, qgetReplace
    l = event.keysym
    svar, label = getSvarLabel( event )
    label.configure( textvariable = svar )
    if l == 'Return':
        qgetQuery = False
        qgetReplace = True
        qQ = svar.get()
        svar.set( '')
        label.configure( textvariable = lqQ)
        return
    setSvar( event, svar )
#@-node:mork.20041014112843.109:getQuery
#@+node:mork.20041014112843.110:getReplace
qgetReplace = False
def getReplace( event ):
    global qR, qgetReplace, qrexecute
    l = event.keysym
    svar, label = getSvarLabel( event )
    label.configure( textvariable = svar )
    if l == 'Return':
        qgetReplace = False
        qR = svar.get()
        svar.set( 'Replace %s with %s y/n' %( qQ, qR ) )
        qrexecute = True
        ok = qsearch( event )
        return
    setSvar( event, svar )
#@-node:mork.20041014112843.110:getReplace
#@+node:mork.20041014112843.111:masterQR
qrexecute = False   
def masterQR( event ):

    if qgetQuery:
        getQuery( event )
    elif qgetReplace:
        getReplace( event )
    elif qrexecute:
        qreplace( event )
    else:
        listenQR( event )
    return 'break'
#@-node:mork.20041014112843.111:masterQR
#@+node:ekr.20041028083211.10:Search utils...
#@+node:mork.20041014112843.112:getSvarLabel
def getSvarLabel( event ):
    svar = svars[ event.widget ]
    label = mbuffers[ event.widget ]
    return svar, label
#@-node:mork.20041014112843.112:getSvarLabel
#@+node:mork.20041014112843.113:setSvar
def setSvar( event, svar ):  
    t = svar.get()  
    if event.char == '\b':
           if len( t ) == 1:
               t = ''
           else:
               t = t[ 0 : -1 ]
           svar.set( t )
    else:
            t = t + event.char
            svar.set( t )
#@-node:mork.20041014112843.113:setSvar
#@+node:mork.20041014112843.114:movePastClose
def movePastClose( event ):
    buffer = event.widget
    i = buffer.search( '(', 'insert' , backwards = True ,stopindex = '1.0' )
    icheck = buffer.search( ')', 'insert',  backwards = True, stopindex = '1.0' )
    if ''  ==  i:
        return 'break'
    if icheck:
        ic = buffer.compare( i, '<', icheck )
        if ic: 
            return 'break'
    i2 = buffer.search( ')', 'insert' ,stopindex = 'end' )
    i2check = buffer.search( '(', 'insert', stopindex = 'end' )
    if '' == i2:
        return 'break'
    if i2check:
        ic2 = buffer.compare( i2, '>', i2check )
        if ic2:
            return 'break'
    ib = buffer.index( 'insert' )
    buffer.mark_set( 'insert', '%s lineend +1c' % i2 )
    if buffer.index( 'insert' ) == buffer.index( '%s lineend' % ib ):
        buffer.insert( 'insert' , '\n')
    return _tailEnd( buffer )
#@-node:mork.20041014112843.114:movePastClose
#@+node:mork.20041014112843.115:replaceString
rString = False
_sString = ''
_rpString = ''
def replaceString( event ):
    global rString, _sString, _rpString
    svar, label = getSvarLabel( event )
    if event.keysym in ( 'Control_L', 'Control_R' ):
        return
    if not rString:
        rString = 1
        _sString = ''
        _rpString = ''
        svar.set( 'Replace String' )
        return
    if event.keysym == 'Return':
        rString = rString + 1
    if rString == 1:
        svar.set( '' )
        rString = rString + 1
    if rString == 2:
        setSvar( event, svar )
        _sString = svar.get()
        return 'break'
    if rString == 3:
        svar.set( 'Replace string %s with:' % _sString )
        rString = rString + 1
        return 'break'
    if rString == 4:
        svar.set( '' )
        rString = rString + 1
    if rString == 5:
        setSvar( event, svar )
        _rpString = svar.get()
        return 'break'
    if rString == 6:
        buffer = event.widget
        i = 'insert'
        ct = 0
        while i:
            i = buffer.search( _sString, i, stopindex = 'end' )
            if i:
                buffer.delete( i, '%s +%sc' %( i, len( _sString) ))
                buffer.insert( i, _rpString )
                ct = ct +1
        svar.set( 'Replaced %s occurances' % ct )
        label.configure( background = 'lightgrey' ) 
        rString = False
        return _tailEnd( buffer )
#@-node:mork.20041014112843.115:replaceString
#@+node:mork.20041014112843.116:swapCharacters
def swapCharacters( event ):
    buffer = event.widget
    i = buffer.index( 'insert' )
    c1 = buffer.get( 'insert', 'insert +1c' )
    c2 = buffer.get( 'insert -1c', 'insert' )
    buffer.delete( 'insert -1c', 'insert' )
    buffer.insert( 'insert', c1 )
    buffer.delete( 'insert', 'insert +1c' )
    buffer.insert( 'insert', c2 )
    buffer.mark_set( 'insert', i )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.116:swapCharacters
#@+node:mork.20041014112843.117:insertNewLine
def insertNewLine( event ):
    buffer = event.widget
    i = buffer.index( 'insert' )
    buffer.insert( 'insert', '\n' )
    buffer.mark_set( 'insert', i )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.117:insertNewLine
#@+node:mork.20041014112843.118:lineNumber
def lineNumber( event ):
    stopControlX( event )
    svar, label = getSvarLabel( event )
    buffer = event.widget
    i = buffer.index( 'insert' )
    i1, i2 = i.split( '.' )
    c = buffer.get( 'insert', 'insert + 1c' )
    txt = buffer.get( '1.0', 'end' )
    txt2 = buffer.get( '1.0', 'insert' )
    perc = len( txt ) * .01
    perc = int( len( txt2 ) / perc )
    svar.set( 'Char: %s point %s of %s(%s%s)  Column %s' %( c, len( txt2), len( txt), perc,'%', i1 ) )
    return 'break'
#@-node:mork.20041014112843.118:lineNumber
#@+node:mork.20041014112843.119:prevNexSentence
def prevNexSentence( event , way ):
    buffer = event.widget
    if way == 'bak':
        i = buffer.search( '.', 'insert', backwards = True, stopindex = '1.0' )
        if i:
            i2 = buffer.search( '.', i, backwards = True, stopindex = '1.0' )
            if not i2:
                i2 = '1.0'
            if i2:
                i3 = buffer.search( '\w', i2, stopindex = i, regexp = True )
                if i3:
                    buffer.mark_set( 'insert', i3 )
        else:
            buffer.mark_set( 'insert', '1.0' )
    else:
        i = buffer.search( '.', 'insert', stopindex = 'end' )
        if i:
            buffer.mark_set( 'insert', '%s +1c' %i )
        else:
            buffer.mark_set( 'insert', 'end' )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.119:prevNexSentence
#@+node:mork.20041014112843.120:openRectangle
def openRectangle( event ):
    if not _chckSel( event ):
        return
    buffer = event.widget
    r1, r2, r3, r4 = getRectanglePoints( event )
    lth = ' ' * ( r4 - r2 )
    stopControlX( event )
    while r1 <= r3:
        buffer.insert( '%s.%s' % ( r1, r2 ) , lth)
        r1 = r1 + 1
    return _tailEnd( buffer )
#@-node:mork.20041014112843.120:openRectangle
#@+node:mork.20041014112843.121:clearRectangle
def clearRectangle( event ):
    if not _chckSel( event ):
        return
    buffer = event.widget
    r1, r2, r3, r4 = getRectanglePoints( event )
    lth = ' ' * ( r4 - r2 )
    stopControlX( event )
    while r1 <= r3:
        buffer.delete( '%s.%s' % ( r1, r2 ) , '%s.%s' % ( r1, r4 )  )
        buffer.insert( '%s.%s' % ( r1, r2 ) , lth)
        r1 = r1 + 1
    return _tailEnd( buffer )
#@-node:mork.20041014112843.121:clearRectangle
#@+node:mork.20041014112843.122:deleteRectangle
def deleteRectangle( event ):
    if not _chckSel( event ):
        return
    buffer = event.widget
    r1, r2, r3, r4 = getRectanglePoints( event )
    lth = ' ' * ( r4 - r2 )
    stopControlX( event )
    while r1 <= r3:
        buffer.delete( '%s.%s' % ( r1, r2 ) , '%s.%s' % ( r1, r4 )  )
        r1 = r1 + 1
    return _tailEnd( buffer )
#@-node:mork.20041014112843.122:deleteRectangle
#@+node:mork.20041014112843.123:stringRectangle
sRect = False   
def stringRectangle( event ):
    global sRect
    svar, label = getSvarLabel( event )
    if not sRect:
        sRect = 1
        svar.set( 'String rectangle :' )
        setLabelBlue( label )
        return 'break'
    if event.keysym == 'Return':
        sRect = 3
    if sRect == 1:
        svar.set( '' )
        sRect = 2
    if sRect == 2:
        setSvar( event, svar )
        return 'break'
    if sRect == 3:
        if not _chckSel( event ):
            stopControlX( event )
            return
        buffer = event.widget
        r1, r2, r3, r4 = getRectanglePoints( event )
        lth = svar.get()
        stopControlX( event )
        while r1 <= r3:
            buffer.delete( '%s.%s' % ( r1, r2 ),  '%s.%s' % ( r1, r4 ) )
            buffer.insert( '%s.%s' % ( r1, r2 ) , lth )
            r1 = r1 + 1
        return _tailEnd( buffer )
#@-node:mork.20041014112843.123:stringRectangle
#@+node:mork.20041014112843.124:killRectangle
krectangle = None       
def killRectangle( event ):
    global krectangle
    if not _chckSel( event ):
        return
    buffer = event.widget
    r1, r2, r3, r4 = getRectanglePoints( event )
    lth = ' ' * ( r4 - r2 )
    stopControlX( event )
    krectangle = []
    while r1 <= r3:
        txt = buffer.get( '%s.%s' % ( r1, r2 ) , '%s.%s' % ( r1, r4 )  )
        krectangle.append( txt )
        buffer.delete( '%s.%s' % ( r1, r2 ) , '%s.%s' % ( r1, r4 )  )
        r1 = r1 + 1
    return _tailEnd( buffer )
#@-node:mork.20041014112843.124:killRectangle
#@+node:mork.20041014112843.125:closeRectangle
def closeRectangle( event ):
    if not _chckSel( event ):
        return
    buffer = event.widget
    r1, r2, r3, r4 = getRectanglePoints( event ) 
    ar1 = r1
    txt = []
    while ar1 <= r3:
        txt.append( buffer.get( '%s.%s' %( ar1, r2 ), '%s.%s' %( ar1, r4 ) ) )
        ar1 = ar1 + 1 
    for z in txt:
        if z.lstrip().rstrip():
            return
    while r1 <= r3:
        buffer.delete( '%s.%s' %(r1, r2 ), '%s.%s' %( r1, r4 ) )
        r1 = r1 + 1
    return _tailEnd( buffer )
#@-node:mork.20041014112843.125:closeRectangle
#@+node:mork.20041014112843.126:yankRectangle
def yankRectangle( event , krec = None ):
    stopControlX( event )
    if not krec:
        krec = krectangle
    if not krec:
        return 'break'
    buffer = event.widget
    txt = buffer.get( 'insert linestart', 'insert' )
    txt = getWSString( txt )
    i = buffer.index( 'insert' )
    i1, i2 = i.split( '.' )
    i1 = int( i1 )
    for z in krec:        
        txt2 = buffer.get( '%s.0 linestart' % i1, '%s.%s' % ( i1, i2 ) )
        if len( txt2 ) != len( txt ):
            amount = len( txt ) - len( txt2 )
            z = txt[ -amount : ] + z
        buffer.insert( '%s.%s' %( i1, i2 ) , z )
        if buffer.index( '%s.0 lineend +1c' % i1 ) == buffer.index( 'end' ):
            buffer.insert( '%s.0 lineend' % i1, '\n' )
        i1 = i1 + 1
    return _tailEnd( buffer )
#@-node:mork.20041014112843.126:yankRectangle
#@+node:mork.20041014112843.127:getWSString
def getWSString( txt ):
    ntxt = []
    for z in txt:
        if z == '\t':
            ntxt.append( z )
        else:
            ntxt.append( ' ' )
    return ''.join( ntxt )
#@-node:mork.20041014112843.127:getWSString
#@+node:mork.20041014112843.128:getRectanglePoints
def getRectanglePoints( event ):
    buffer = event.widget
    i = buffer.index( 'sel.first' )
    i2 = buffer.index( 'sel.last' )
    r1, r2 = i.split( '.' )
    r3, r4 = i2.split( '.' )
    r1 = int( r1 )
    r2 = int( r2 )
    r3 = int( r3 )
    r4 = int( r4 )
    return r1, r2, r3, r4
#@-node:mork.20041014112843.128:getRectanglePoints
#@+node:mork.20041014112843.129:negativeArgument
negativeArg = False
def negativeArgument( event, stroke = None ):
    global negativeArg
    svar, label = getSvarLabel( event )
    svar.set( "Negative Argument" )
    label.configure( background = 'lightblue' )
    if not negativeArg:
        negativeArg = True
    if negativeArg:
        if negArgs.has_key( stroke ):
            negArgs[ stroke ]( event , stroke)
    return 'break'
#@-node:mork.20041014112843.129:negativeArgument
#@+node:mork.20041014112843.130:changePreviousWord
def changePreviousWord( event, stroke ):
    buffer = event.widget
    i = buffer.index( 'insert' )
    moveword( event, -1  )
    if stroke == '<Alt-c>': 
        capitalize( event, 'cap' )
    elif stroke =='<Alt-u>':
         capitalize( event, 'up' )
    elif stroke == '<Alt-l>': 
        capitalize( event, 'low' )
    buffer.mark_set( 'insert', i )
    stopControlX( event )
    return _tailEnd( buffer )    
#@-node:mork.20041014112843.130:changePreviousWord
#@+node:mork.20041014112843.131:insertNewLineIndent
negArgs = { '<Alt-c>': changePreviousWord,
'<Alt-u>' : changePreviousWord,
'<Alt-l>': changePreviousWord }



def insertNewLineIndent( event ):
    buffer =  event.widget
    txt = buffer.get( 'insert linestart', 'insert lineend' )
    txt = getWSString( txt )
    i = buffer.index( 'insert' )
    buffer.insert( i, txt )
    buffer.mark_set( 'insert', i )    
    return insertNewLine( event )
#@-node:mork.20041014112843.131:insertNewLineIndent
#@+node:mork.20041014112843.132:dynamicExpansion
def dynamicExpansion( event, store = {'rlist': [], 'stext': ''} ):
    buffer = event.widget
    rlist = store[ 'rlist' ]
    stext = store[ 'stext' ]
    i = buffer.index( 'insert -1c wordstart' )
    i2 = buffer.index( 'insert -1c wordend' )
    txt = buffer.get( i, i2 )
    dA = buffer.tag_ranges( 'dA' )
    buffer.tag_delete( 'dA' )
    def doDa( txt ):
        buffer.delete( 'insert -1c wordstart', 'insert -1c wordend' ) 
        buffer.insert( 'insert', txt )
        buffer.tag_add( 'dA', 'insert -1c wordstart', 'insert -1c wordend' )
        return _tailEnd( buffer )
        
    if dA:
        if i == dA[ 0 ] and i2 == dA[ 1 ]:
            if rlist:
                txt = rlist.pop()
            else:
                txt = stext
                getDynamicList( buffer, txt, rlist )
            return doDa( txt )
        else:
            dA = None
            
    if not dA:
        store[ 'stext' ] = txt
        store[ 'rlist' ] = rlist = []
        getDynamicList( buffer, txt, rlist )
        if not rlist:
            return 'break'
        txt = rlist.pop()
        return doDa( txt )
#@-node:mork.20041014112843.132:dynamicExpansion
#@+node:mork.20041014112843.133:dynamicExpansion2
def dynamicExpansion2( event ):
    buffer = event.widget
    i = buffer.index( 'insert -1c wordstart' )
    i2 = buffer.index( 'insert -1c wordend' )
    txt = buffer.get( i, i2 )   
    rlist = []
    getDynamicList( buffer, txt, rlist )
    dEstring = reduce( findPre, rlist )
    if dEstring:
        buffer.delete( i , i2 )
        buffer.insert( i, dEstring )    
        return _tailEnd( buffer )          
#@-node:mork.20041014112843.133:dynamicExpansion2
#@+node:mork.20041014112843.134:getDynamicList
def getDynamicList( buffer, txt , rlist ):
     i = '1.0'
     while i:
         i = buffer.search( txt, i,  stopindex = 'end' )
         if i == buffer.index( 'insert -1c wordstart' ): 
            i = '%s wordend' % i
            continue
         if i:
            if i == buffer.index( '%s wordstart' % i ):
                word = buffer.get( i, '%s wordend' % i )
                if word not in rlist:
                    rlist.append ( word )
                else:
                    rlist.remove( word )
                    rlist.append( word )
            i = '%s wordend' % i
#@-node:mork.20041014112843.134:getDynamicList
#@+node:mork.20041014112843.135:findPre
def findPre( a, b ):
    st = ''
    for z in a:
        st1 = st + z
        if b.startswith( st1 ):
            st = st1
        else:
            return st
    return st  
#@-node:mork.20041014112843.135:findPre
#@+node:mork.20041014112843.136:sortLines
def sortLines( event , which):
    buffer = event.widget
    if not _chckSel( event ):
        return
    i = buffer.index( 'sel.first' )
    i2 = buffer.index( 'sel.last' )
    is1 = i.split( '.' )
    is2 = i2.split( '.' )
    txt = buffer.get( '%s.0' % is1[ 0 ], '%s.0 lineend' % is2[ 0 ] )
    ins = buffer.index( 'insert' )
    txt = txt.split( '\n' )
    buffer.delete( '%s.0' % is1[ 0 ], '%s.0 lineend' % is2[ 0 ] )
    txt.sort()
    if which:
        txt.reverse()
    inum = int(is1[ 0 ])
    for z in txt:
        buffer.insert( '%s.0' % inum, '%s\n' % z ) 
        inum = inum + 1
    buffer.mark_set( 'insert', ins )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.136:sortLines
#@+node:mork.20041014112843.137:sortColumns
def sortColumns( event ):
    buffer = event.widget
    if not _chckSel( event ):
        return
    ins = buffer.index( 'insert' )
    is1 = buffer.index( 'sel.first' )
    is2 = buffer.index( 'sel.last' )   
    sint1, sint2 = is1.split( '.' )
    sint2 = int( sint2 )
    sint3, sint4 = is2.split( '.' )
    sint4 = int( sint4 )
    txt = buffer.get( '%s.0' % sint1, '%s.0 lineend' % sint3 )
    buffer.delete( '%s.0' % sint1, '%s.0 lineend' % sint3 )
    columns = []
    i = int( sint1 )
    i2 = int( sint3 )
    while i <= i2:
        t = buffer.get( '%s.%s' %( i, sint2 ), '%s.%s' % ( i, sint4 ) )
        columns.append( t )
        i = i + 1
    txt = txt.split( '\n' )
    zlist = zip( columns, txt )
    zlist.sort()
    i = int( sint1 )      
    for z in xrange( len( zlist ) ):
         buffer.insert( '%s.0' % i, '%s\n' % zlist[ z ][ 1 ] ) 
         i = i + 1
    buffer.mark_set( 'insert', ins )
    return _tailEnd( buffer ) 
#@-node:mork.20041014112843.137:sortColumns
#@+node:mork.20041014112843.138:reverseRegion
def reverseRegion( event ):
    buffer = event.widget
    if not _chckSel( event ):
        return
    ins = buffer.index( 'insert' )
    is1 = buffer.index( 'sel.first' )
    is2 = buffer.index( 'sel.last' )    
    txt = buffer.get( '%s linestart' % is1, '%s lineend' %is2 )
    buffer.delete( '%s linestart' % is1, '%s lineend' %is2  )
    txt = txt.split( '\n' )
    txt.reverse()
    istart = is1.split( '.' )
    istart = int( istart[ 0 ] )
    for z in txt:
        buffer.insert( '%s.0' % istart, '%s\n' % z )
        istart = istart + 1
    buffer.mark_set( 'insert', ins )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.138:reverseRegion
#@+node:mork.20041014112843.139:sortFields
def sortFields( event, which = None ):
    buffer = event.widget
    if not _chckSel( event ):
        return
    ins = buffer.index( 'insert' )
    is1 = buffer.index( 'sel.first' )
    is2 = buffer.index( 'sel.last' )    
    txt = buffer.get( '%s linestart' % is1, '%s lineend' % is2 )
    txt = txt.split( '\n' )
    fields = []
    fn = r'\w+'
    frx = re.compile( fn )
    for z in txt:
        f = frx.findall( z )
        if not which:
            fields.append( f[ 0 ] )
        else:
            i =  int( which )
            if len( f ) < i:
                return _tailEnd( buffer )
            i = i - 1            
            fields.append( f[ i ] )
    nz = zip( fields, txt )
    nz.sort()
    buffer.delete( '%s linestart' % is1, '%s lineend' % is2 )
    i = is1.split( '.' )
    i2 = is2.split( '.' )
    int1 = int( i[ 0 ] )
    for z in nz:
        buffer.insert( '%s.0' % int1, '%s\n'% z[1] )
        int1 = int1 + 1
    buffer.mark_set( 'insert' , ins )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.139:sortFields
#@+node:mork.20041014112843.140:alt_X
altx = False
def alt_X( event , which = None):
    global altx
    if which:
        altx = which
    else:
        altx = 'True'
    svar, label = getSvarLabel( event )
    if which:
        svar.set( '%s M-x:' % which )
    else:
        svar.set( 'M-x:' )
    setLabelBlue( label )
    return 'break'
#@-node:mork.20041014112843.140:alt_X
#@+node:mork.20041014112843.141:doAlt_X
doAltX= {
'prepend-to-register': prependToRegister,
'append-to-register': appendToRegister,
'replace-string': replaceString,
'sort-lines': sortLines,
'sort-columns': sortColumns,
'reverse-region': reverseRegion,
'sort-fields': sortFields,
'abbrev-mode': toggleAbbrevMode,
'kill-all-abbrevs': killAllAbbrevs,
'expand-region-abbrevs': regionalExpandAbbrev,
'write-abbrev-file': writeAbbreviations,
'read-abbrev-file': readAbbreviations,
'fill-region-as-paragraph': fillRegionAsParagraph,
'fill-region': fillRegion,
'close-rectangle': closeRectangle,
'how-many': startHowMany,
'kill-paragraph': killParagraph,
'backward-kill-paragraph': backwardKillParagraph,
'name-last-kbd-macro': nameLastMacro,
'load-file': loadMacros,
'insert-keyboard-macro' : getMacroName,
'list-abbrevs': listAbbrevs
}

x_hasNumeric = [ 'sort-lines' , 'sort-fields']


def doAlt_X( event ):
    global altx
    svar, label = getSvarLabel( event )
    if svar.get().endswith( 'M-x:' ): svar.set( '' )
    if event.keysym == 'Return':
        txt = svar.get()
        if doAltX.has_key( txt ):
            if altx.isdigit() and txt in x_hasNumeric:
                doAltX[ txt]( event, altx )
            else:
                doAltX[ txt ]( event )
        else:
            svar.set('Command does not exist' )
            setLabelGrey( label )
        altx = False
        return 'break'
    if event.keysym == 'Tab':
        svar.set( _findMatch( svar ) )
        return 'break'        
    setSvar( event, svar )
    return 'break'
#@-node:mork.20041014112843.141:doAlt_X
#@+node:mork.20041014112843.142:_findMatch
def _findMatch( svar, fdict = doAltX ):
    txt = svar.get()
    pmatches = filter( lambda a : a.startswith( txt ), fdict )
    if pmatches:
        mstring = reduce( findPre, pmatches )
        return mstring
    return txt
#@-node:mork.20041014112843.142:_findMatch
#@+node:mork.20041014112843.143:universalDispatch
uC = False
def universalDispatch( event, stroke ):
    global uC    
    if not uC:
        uC = 1
        svar, label = getSvarLabel( event )
        svar.set( '' )
        setLabelBlue( label ) 
    elif uC == 1:
        universalCommand1( event, stroke )
    elif uC == 2:
        universalCommand3( event, stroke )
    return 'break'
#@-node:mork.20041014112843.143:universalDispatch
#@+node:mork.20041014112843.144:universalCommand1
uCstring = string.digits + '\b'

def universalCommand1( event, stroke ):
    global uC
    if event.char not in uCstring:
        return universalCommand2( event, stroke )
    svar, label = getSvarLabel( event )
    setSvar( event, svar )
    if event.char != '\b':
        svar.set( '%s ' %svar.get() )
#@-node:mork.20041014112843.144:universalCommand1
#@+node:mork.20041014112843.145:universalCommand2
def universalCommand2( event , stroke ):
    global uC
    uC = False
    svar, label = getSvarLabel( event )
    txt = svar.get()
    txt = txt.replace( ' ', '' )
    resetMiniBuffer( event )
    if not txt.isdigit():
        if stroke == '<Control-x>':
            uC = 2
            return universalCommand3( event, stroke )
        return _tailEnd( event.widget )
    if uCdict.has_key( stroke ):
            uCdict[ stroke ]( event , txt )
    else:
        buffer = event.widget
        i = int( txt )
        stroke = stroke.lstrip( '<' ).rstrip( '>' )
        if cbDict.has_key( stroke ):
            for z in xrange( i ):
                method = cbDict[ stroke ]
                ev = Tkinter.Event()
                ev.widget = event.widget
                ev.keysym = event.keysym
                ev.keycode = event.keycode
                ev.char = event.char
                masterCommand( ev , method, '<%s>' % stroke )
        else:
            for z in xrange( i ):
                event.widget.event_generate( '<Key>', keycode = event.keycode, keysym = event.keysym )
#@-node:mork.20041014112843.145:universalCommand2
#@+node:mork.20041014112843.146:universalCommand3
uCdict = { '<Alt-x>' : alt_X }

def universalCommand3( event, stroke ):
    svar, label = getSvarLabel( event )
    svar.set( 'Control-u %s' % stroke.lstrip( '<' ).rstrip( '>' ) )
    setLabelBlue( label )
    if event.keysym == 'parenleft':
        stopControlX( event )
        startKBDMacro( event )
        executeLastMacro( event )
        return 'break'
#@-node:mork.20041014112843.146:universalCommand3
#@+node:mork.20041014112843.147:numberCommand
def numberCommand( event, stroke, number ):
    universalDispatch( event, stroke )
    buffer = event.widget
    buffer.event_generate( '<Key>', keysym = number )
    return 'break'       
#@-node:mork.20041014112843.147:numberCommand
#@+node:mork.20041014112843.148:transposeLines
def transposeLines( event ):
    buffer = event.widget
    i = buffer.index( 'insert' )
    i1, i2 = i.split( '.' )
    i1 = str( int( i1 ) -1 )
    if i1 != '0':
        l2 = buffer.get( 'insert linestart', 'insert lineend' )
        buffer.delete( 'insert linestart-1c', 'insert lineend' )
        buffer.insert( i1+'.0', l2 +'\n')
    else:
        l2 = buffer.get( '2.0', '2.0 lineend' )
        buffer.delete( '2.0', '2.0 lineend' )
        buffer.insert( '1.0', l2 + '\n' )         
#@nonl
#@-node:mork.20041014112843.148:transposeLines
#@+node:mork.20041014112843.149:upperLowerRegion
def upperLowerRegion( event, way ):
    buffer = event.widget
    mrk = 'sel'
    range = buffer.tag_ranges( mrk )
    if len( range ) != 0:
        text = buffer.get( range[ 0 ] , range[ -1 ] )
        i = buffer.index( 'insert' )
        if text == ' ': return 'break'
        buffer.delete( range[ 0 ], range[ -1 ] )
        if way == 'low':
            text = text.lower()
        if way == 'up':
            text = text.upper()
        buffer.insert( 'insert', text )
        buffer.mark_set( 'insert', i ) 
    removeRKeys( buffer )
    return 'break'
#@-node:mork.20041014112843.149:upperLowerRegion
#@+node:mork.20041014112843.150:removeBlankLines
def removeBlankLines( event ):
    buffer = event.widget
    i = buffer.index( 'insert' )
    i1, i2 = i.split( '.' )
    i1 = int( i1 )
    dindex = []
    if buffer.get( 'insert linestart', 'insert lineend' ).strip() == '':
        while 1:
            if str( i1 )+ '.0'  == '1.0' :
                break 
            i1 = i1 - 1
            txt = buffer.get( '%s.0' % i1, '%s.0 lineend' % i1 )
            txt = txt.strip()
            if len( txt ) == 0:
                dindex.append( '%s.0' % i1)
                dindex.append( '%s.0 lineend' % i1 )
            elif dindex:
                buffer.delete( '%s-1c' % dindex[ -2 ], dindex[ 1 ] )
                buffer.event_generate( '<Key>' )
                buffer.update_idletasks()
                break
            else:
                break
    i = buffer.index( 'insert' )
    i1, i2 = i.split( '.' )
    i1 = int( i1 )
    dindex = []
    while 1:
        if buffer.index( '%s.0 lineend' % i1 ) == buffer.index( 'end' ):
            break
        i1 = i1 + 1
        txt = buffer.get( '%s.0' % i1, '%s.0 lineend' % i1 )
        txt = txt.strip()
        if len( txt ) == 0:
            dindex.append( '%s.0' % i1 )
            dindex.append( '%s.0 lineend' % i1 )
        elif dindex:
            buffer.delete( '%s-1c' % dindex[ 0 ], dindex[ -1 ] )
            buffer.event_generate( '<Key>' )
            buffer.update_idletasks()
            break
        else:
            break
#@-node:mork.20041014112843.150:removeBlankLines
#@+node:mork.20041014112843.151:insertFile
def insertFile( event ):
    buffer = event.widget
    f = tkFileDialog.askopenfile()
    if f == None: return None
    txt = f.read()
    f.close()
    buffer.insert( 'insert', txt )
    return _tailEnd( buffer )
#@-node:mork.20041014112843.151:insertFile
#@+node:mork.20041014112843.152:saveFile
def saveFile( event ):
    buffer = event.widget
    txt = buffer.get( '1.0', 'end' )
    f = tkFileDialog.asksaveasfile()
    if f == None : return None
    f.write( txt )
    f.close()
#@-node:mork.20041014112843.152:saveFile
#@+node:mork.20041014112843.153:scolorizer
xcommands = {
'<Control-t>': transposeLines, 
'<Control-u>': lambda event , way ='up': upperLowerRegion( event, way ),
'<Control-l>':  lambda event , way ='low': upperLowerRegion( event, way ),
'<Control-o>': removeBlankLines,
'<Control-i>': insertFile,
'<Control-s>': saveFile,
'<Control-x>': exchangePointMark,
'<Control-Shift-at>': lambda event: event.widget.selection_clear(),
'<Delete>' : lambda event, back = True: killsentence( event, back ),
}

def scolorizer( event ):

    buffer = event.widget
    svar, label = getSvarLabel( event )
    stext = svar.get()
    buffer.tag_delete( 'color' )
    buffer.tag_delete( 'color1' )
    if stext == '': return 'break'
    ind = '1.0'
    while ind:
        ind = buffer.search( stext, ind, stopindex = 'end')
        if ind:
            i, d = ind.split('.')
            d = str(int( d ) + len( stext ))
            index = buffer.index( 'insert' )
            if ind == index:
                buffer.tag_add( 'color1', ind, '%s.%s' % (i,d) )
            buffer.tag_add( 'color', ind, '%s.%s' % (i, d) )
            ind = i +'.'+d
    buffer.tag_config( 'color', foreground = 'red' ) 
    buffer.tag_config( 'color1', background = 'lightblue' ) 
#@-node:mork.20041014112843.153:scolorizer
#@+node:mork.20041014112843.154:startGoto
def startGoto( event ):
    global goto
    goto = True
    label = mbuffers[ event.widget ] 
    label.configure( background = 'lightblue' )
    return 'break'
#@-node:mork.20041014112843.154:startGoto
#@+node:mork.20041014112843.155:Goto
def Goto( event ):
    global goto
    widget = event.widget
    svar, label = getSvarLabel( event )
    if event.keysym == 'Return':
          i = svar.get()
          resetMiniBuffer( event )
          goto = False
          if i.isdigit():
              widget.mark_set( 'insert', '%s.0' % i )
              widget.event_generate( '<Key>' )
              widget.update_idletasks()
              widget.see( 'insert' )
          return 'break'
    t = svar.get()
    if event.char == '\b':
           if len( t ) == 1:
               t = ''
           else:
               t = t[ 0 : -1 ]
           svar.set( t )
    else:
            t = t + event.char
            svar.set( t )
    return 'break'
#@-node:mork.20041014112843.155:Goto
#@-node:ekr.20041028083211.10:Search utils...
#@-node:ekr.20041028083211.9:Search...
#@-node:ekr.20041028083211.3:Emacs commands...
#@-others

#@<< define cbDict >>
#@+node:ekr.20041028083211:<< define cbDict >>
cbDict = {
'Alt-less' : lambda event, spot = '1.0' :moveTo( event, spot ),
'Alt-greater': lambda event, spot = 'end' :moveTo( event, spot ),
'Control-Right': lambda event, way = 1: moveword( event, way ),
'Control-Left': lambda event, way = -1: moveword( event, way ),
'Control-a': lambda event, spot = 'insert linestart': moveTo( event, spot ),
'Control-e': lambda event, spot = 'insert lineend': moveTo( event, spot ),
'Alt-Up': lambda event, spot = 'insert linestart': moveTo( event, spot ),
'Alt-Down': lambda event, spot = 'insert lineend': moveTo( event, spot ),
'Alt-f': lambda event, way = 1: moveword( event, way ),
'Alt-b' : lambda event, way = -1: moveword( event, way ),
'Control-o': insertNewLine,
'Control-k': lambda event, frm = 'insert', to = 'insert lineend': kill( event, frm, to) ,
'Alt-d': lambda event, frm = 'insert wordstart', to = 'insert wordend': kill( event,frm, to ),
'Alt-Delete': lambda event: deletelastWord( event ),
"Control-y": lambda event, frm = 'insert', which = 'c': walkKB( event, frm, which),
"Alt-y": lambda event , frm = "insert", which = 'a': walkKB( event, frm, which ),
"Alt-k": lambda event : killsentence( event ),
 'Control-s' : None,
 'Control-r' : None,
 'Alt-c': lambda event, which = 'cap' : capitalize( event, which ),
 'Alt-u': lambda event, which = 'up' : capitalize( event, which ),
 'Alt-l': lambda event, which = 'low' : capitalize( event, which ),
 'Alt-t': lambda event, sw = []: swapWords( event, sw ),
 'Alt-x': alt_X,
'Control-x': startControlX,
'Control-g': stopControlX,
'Control-Shift-at': setRegion,
'Control-w': lambda event, which = 'd' :killRegion( event, which ),
'Alt-w': lambda event, which = 'c' : killRegion( event, which ),
'Control-t': swapCharacters,
'Control-u': None,
'Control-l': None,
'Alt-z': None,
'Control-i': None,
'Alt-Control-backslash': indentRegion,
'Alt-m' : backToIndentation,
'Alt-asciicircum' : deleteIndentation,
'Control-d': deleteNextChar,
'Alt-backslash': deleteSpaces, 
'Alt-g': None,
'Control-v' : lambda event, way = 'south': screenscroll( event, way ),
'Alt-v' : lambda event, way = 'north' : screenscroll( event, way ),
'Alt-equal': countRegion,
'Alt-parenleft': insertParentheses,
'Alt-parenright': movePastClose,
'Alt-percent' : None,
'Delete': lambda event, which = 'BackSpace': manufactureKeyPress( event, which ),
'Control-p': lambda event, which = 'Up': manufactureKeyPress( event, which ),
'Control-n': lambda event, which = 'Down': manufactureKeyPress( event, which ),
'Control-f': lambda event, which = 'Right': manufactureKeyPress( event, which ),
'Control-b': lambda event, which = 'Left': manufactureKeyPress( event, which ),
'Control-Alt-w': None,
'Alt-a': lambda event, which = 'bak': prevNexSentence( event, which ),
'Alt-e': lambda event, which = 'for': prevNexSentence( event, which ),
'Control-Alt-o': insertNewLineIndent,
'Alt-minus': negativeArgument,
'Alt-slash': dynamicExpansion,
'Control-Alt-slash': dynamicExpansion2,
'Control-u': lambda event, keystroke = '<Control-u>': universalDispatch( event, keystroke ),
'Alt-braceright': lambda event, which = 1: movingParagraphs( event, which ),
'Alt-braceleft': lambda event , which = 0: movingParagraphs( event, which ),
'Alt-q': fillParagraph,
'Alt-h': selectParagraph,
'Alt-semicolon': indentToCommentColumn,
'Alt-0': lambda event, stroke = '<Alt-0>', number = 0: numberCommand( event, stroke, number ) ,
'Alt-1': lambda event, stroke = '<Alt-1>', number = 1: numberCommand( event, stroke, number ) ,
'Alt-2': lambda event, stroke = '<Alt-2>', number = 2: numberCommand( event, stroke, number ) ,
'Alt-3': lambda event, stroke = '<Alt-3>', number = 3: numberCommand( event, stroke, number ) ,
'Alt-4': lambda event, stroke = '<Alt-4>', number = 4: numberCommand( event, stroke, number ) ,
'Alt-5': lambda event, stroke = '<Alt-5>', number = 5: numberCommand( event, stroke, number ) ,
'Alt-6': lambda event, stroke = '<Alt-6>', number = 6: numberCommand( event, stroke, number ) ,
'Alt-7': lambda event, stroke = '<Alt-7>', number = 7: numberCommand( event, stroke, number ) ,
'Alt-8': lambda event, stroke = '<Alt-8>', number = 8: numberCommand( event, stroke, number ) ,
'Alt-9': lambda event, stroke = '<Alt-9>', number = 9: numberCommand( event, stroke, number ) ,
'Control-underscore': doUndo,
}
#@-node:ekr.20041028083211:<< define cbDict >>
#@nl
#@nonl
#@-node:mork.20041014112843.1:@thin temacs.py
#@-leo
