#@+leo-ver=4-thin
#@+node:ekr.20050529142847:@thin __jEdit_colorizer__.py
'''Replace colorizer with colorizer using jEdit language description files'''

#@@language python
#@@tabwidth -4
#@@pagewidth 80

__version__ = '0.5'
#@<< version history >>
#@+node:ekr.20050529142916.2:<< version history >>
#@@killcolor
#@+at
# 
# 0.1 EKR: Initial version:
#     - Split large methods into smaller methods.
# 0.2 EKR:
#     - Moved contentHandler and modeClass into the plugin.
#     - colorizer.__init__ reads python.xml, but does nothing with it.
# 0.3 EKR:
#     - Wrote and tested createRuleMatchers.
# 0.4 EKR:
#     - Basic syntax coloring now works.
# 0.5 EKR:
#     - Giant step forward 1: colorOneChunk and interrupt allow very fast 
# keyboard response.
#     - Giant step forward 2: no need for incremental coloring!
#     - Giant step forward 3: eliminated flashing & eliminated most calls to 
# removeAllTags.
#     See to-do list.
#@-at
#@nonl
#@-node:ekr.20050529142916.2:<< version history >>
#@nl
#@<< to do >>
#@+node:ekr.20050601081132:<< to do >>
#@@nocolor
#@+at
# 
# - Handle doc parts, leo directives, section references.
#     - Add generic Leo rules to all rule sets.
# 
# - Handle rules attributes, esp. NO_WORD_SEP.
#     - Any non-alphanumeric character not appearing in a keyword definition 
# or
#       the ruleset's NO_WORD_SEP attribute is considered a word separator.
#     - Scan keyword list for characters to add to word list.
# 
# - Figure out how to do mark_previous and mark_following.
#     - In particular, what are the previous and following token??
# 
# - Handle regular expressions: finish match_regexp_helper.
# 
# - Define tags corresponding to token types.
#     - At present doColor translates from token types to old tags.
#     - Eventually we shall want to specify the coloring for new token types 
# using prefs.
# 
# - Make sure pictures get drawn properly.
#@-at
#@nonl
#@-node:ekr.20050601081132:<< to do >>
#@nl
#@<< imports >>
#@+node:ekr.20050529142916.3:<< imports >>
import leoGlobals as g
import leoPlugins

import os
import re
import string
import threading
import xml.sax
import xml.sax.saxutils

# php_re = re.compile("<?(\s|=|[pP][hH][pP])")
php_re = re.compile("<?(\s[pP][hH][pP])")
#@nonl
#@-node:ekr.20050529142916.3:<< imports >>
#@nl
#@<< define leoKeywords >>
#@+node:ekr.20050529143413:<< define leoKeywords >>
# leoKeywords is used by directivesKind, so it should be a module-level symbol.

# leoKeywords must be a list so that plugins may alter it.

leoKeywords = [
    "@","@all","@c","@code","@color","@comment",
    "@delims","@doc","@encoding","@end_raw",
    "@first","@header","@ignore",
    "@killcolor",
    "@language","@last","@lineending",
    "@nocolor","@noheader","@nowrap","@others",
    "@pagewidth","@path","@quiet","@raw","@root","@root-code","@root-doc",
    "@silent","@tabwidth","@terse",
    "@unit","@verbose","@wrap", ]
#@nonl
#@-node:ekr.20050529143413:<< define leoKeywords >>
#@nl
#@<< define default_colors_dict >>
#@+node:ekr.20050529143413.1:<< define default_colors_dict >>
# These defaults are sure to exist.
default_colors_dict = {
    # tag name      :(     option name,           default color),
    "comment"       :("comment_color",               "red"),
    "cwebName"      :("cweb_section_name_color",     "red"),
    "pp"             :("directive_color",             "blue"),
    "docPart"        :("doc_part_color",              "red"),
    "keyword"        :("keyword_color",               "blue"),
    "leoKeyword"     :("leo_keyword_color",           "blue"),
    "link"           :("section_name_color",          "red"),
    "nameBrackets"   :("section_name_brackets_color", "blue"),
    "string"         :("string_color",                "#00aa00"), # Used by IDLE.
    "name"           :("undefined_section_name_color","red"),
    "latexBackground":("latex_background_color","white") }
#@nonl
#@-node:ekr.20050529143413.1:<< define default_colors_dict >>
#@nl
case_insensitiveLanguages = []  ## To be deleted

#@+others
#@+node:ekr.20050529142916.4:init
def init ():

    leoPlugins.registerHandler('start1',onStart1)
    g.plugin_signon(__name__)

    return True
#@nonl
#@-node:ekr.20050529142916.4:init
#@+node:ekr.20050529142916.5:onStart1
def onStart1 (tag, keywords):
    
    import leoColor
    
    leoColor.colorizer = colorizer
#@nonl
#@-node:ekr.20050529142916.5:onStart1
#@+node:ekr.20050530065723.58:class contentHandler
class contentHandler (xml.sax.saxutils.XMLGenerator):
    
    '''A sax content handler class that handles jEdit language-description files.
    
    Creates a list of modes that can be retrieved using getModes method.'''

    #@    @+others
    #@+node:ekr.20050530065723.59: __init__ & helpers
    def __init__ (self,c,fileName,trace=False,verbose=False):
    
        self.c = c
        self.fileName = fileName
        self.trace = trace
        self.verbose = verbose
        
        # Init the base class.
        xml.sax.saxutils.XMLGenerator.__init__(self)
        
        # Non-mode statistics.
        self.numberOfAttributes = 0
        self.numberOfElements = 0
        
        # Options...
        self.ignoreWs = True # True: don't print contents with only ws.
        self.newLineAfterStartElement = [
            'keywords','mode','props','property','rules','span','eol_span',
            # 'seq',
        ]
        
        # Printing options
        if verbose:
            self.printAllElements = True
            self.printCharacters = False or self.printAllElements
            self.printAttributes = False and not self.printAllElements
            self.printElements = [
                #'begin','end',
                #'eol_span',
                #'keyword1','keyword2','keyword3','keyword4',
                #'mark_previous',
                #'mode',
                #'props',
                #'property',
                #'rules',
                #'span',
                #'seq',
            ]
            
            if self.printAllElements:
                self.suppressContent = []
            else:
                self.suppressContent = ['keyword1','keyword2','keyword3','keyword4']
        else:
            self.printAllElements = False
            self.printCharacters = False
            self.printAttributes = False
            self.printElements = []
      
        # Semantics: most of these should be mode ivars.
        self.elementStack = []
        self.mode = None # The present mode, or None if outside all modes.
        self.modes = [] # All modes defined here or by imports.
    #@nonl
    #@-node:ekr.20050530065723.59: __init__ & helpers
    #@+node:ekr.20050530065723.60:helpers
    #@+node:ekr.20050530065723.61:attrsToList
    def attrsToList (self,attrs):
        
        '''Convert the attributes to a list of g.Bunches.
        
        attrs: an Attributes item passed to startElement.
        
        sep: the separator charater between attributes.'''
        
        return [
            g.Bunch(name=name,val=attrs.getValue(name))
            for name in attrs.getNames()
        ]
    #@nonl
    #@-node:ekr.20050530065723.61:attrsToList
    #@+node:ekr.20050530065723.62:attrsToString
    def attrsToString (self,attrs,sep='\n'):
        
        '''Convert the attributes to a string.
        
        attrs: an Attributes item passed to startElement.
        
        sep: the separator charater between attributes.'''
    
        result = [
            '%s="%s"' % (bunch.name,bunch.val)
            for bunch in self.attrsToList(attrs)
        ]
    
        return sep.join(result)
    #@nonl
    #@-node:ekr.20050530065723.62:attrsToString
    #@+node:ekr.20050530065723.63:clean
    def clean(self,s):
    
        return g.toEncodedString(s,"ascii")
    #@nonl
    #@-node:ekr.20050530065723.63:clean
    #@+node:ekr.20050530065723.64:error
    def error (self, message):
        
        print
        print
        print 'XML error: %s' % (message)
        print
    #@nonl
    #@-node:ekr.20050530065723.64:error
    #@+node:ekr.20050530065723.65:printStartElement
    def printStartElement(self,name,attrs):
    
        if attrs.getLength() > 0:
            print '<%s %s>' % (
                self.clean(name).strip(),
                self.attrsToString(attrs,sep=' ')),
        else:
            print '<%s>' % (self.clean(name).strip()),
    
        if name.lower() in self.newLineAfterStartElement:
            print
    #@nonl
    #@-node:ekr.20050530065723.65:printStartElement
    #@+node:ekr.20050530065723.66:printSummary
    def printSummary (self):
        
        print '-' * 10, 'non- mode statistics'
        print 'modes',len(self.modes)
        print 'elements', self.numberOfElements
    #@nonl
    #@-node:ekr.20050530065723.66:printSummary
    #@-node:ekr.20050530065723.60:helpers
    #@+node:ekr.20050530065723.67:sax over-rides
    #@+node:ekr.20050530065723.68: Do nothing...
    #@+node:ekr.20050530065723.69:other methods
    def ignorableWhitespace(self):
        g.trace()
    
    def processingInstruction (self,target,data):
        g.trace()
    
    def skippedEntity(self,name):
        g.trace(name)
    
    def startElementNS(self,name,qname,attrs):
        g.trace(name)
    
    def endElementNS(self,name,qname):
        g.trace(name)
    #@nonl
    #@-node:ekr.20050530065723.69:other methods
    #@+node:ekr.20050530065723.70:endDocument
    def endDocument(self):
    
        pass
    
    
    #@-node:ekr.20050530065723.70:endDocument
    #@+node:ekr.20050530065723.71:startDocument
    def startDocument(self):
        
        pass
    #@nonl
    #@-node:ekr.20050530065723.71:startDocument
    #@-node:ekr.20050530065723.68: Do nothing...
    #@+node:ekr.20050530065723.72:characters
    def characters(self,content):
        
        content = content.replace('\r','').strip()
        content = self.clean(content)
    
        elementName = self.elementStack and self.elementStack[-1]
        elementName = elementName.lower()
        
        if 1: # new code
            if self.printAllElements:
                print content,
            elif self.printCharacters and content and elementName not in self.suppressContent:
                print 'content:',elementName,repr(content)
        else:
            if self.printCharacters and content and elementName not in self.suppressContent:
                if self.printAllElements:
                    print content,
                else:
                    print 'content:',elementName,repr(content)
                
        if self.mode:
            self.mode.doContent(elementName,content)
        else:
            self.error('characters outside of mode')
    #@nonl
    #@-node:ekr.20050530065723.72:characters
    #@+node:ekr.20050530065723.73:endElement
    def endElement(self,name):
    
        self.doEndElement(name)
    
        name2 = self.elementStack.pop()
        assert name == name2
    #@nonl
    #@-node:ekr.20050530065723.73:endElement
    #@+node:ekr.20050530065723.74:startElement
    def startElement(self,name,attrs):
        
        if self.mode:
            self.mode.numberOfElements += 1
        else:
            self.numberOfElements += 1
            
        self.elementStack.append(name)
        self.doStartElement(name,attrs)
    #@nonl
    #@-node:ekr.20050530065723.74:startElement
    #@-node:ekr.20050530065723.67:sax over-rides
    #@+node:ekr.20050530065723.75:doStartElement
    def doStartElement (self,elementName,attrs):
        
        if self.printAllElements or elementName.lower() in self.printElements:
            self.printStartElement(elementName,attrs)
    
        elementName = elementName.lower()
        
        if elementName == 'mode':
            self.mode = modeClass(self,self.fileName)
        elif self.mode:
            self.mode.startElement(elementName)
            for bunch in self.attrsToList(attrs):
                if self.printAttributes:
                    print 'attr:',elementName,bunch.name,'=',bunch.val
                self.mode.doAttribute(bunch.name,bunch.val)
        else:
            self.error('Start element appears outside of Mode:%s' % elementName)
            for bunch in self.attrsToList(attrs):
                self.error('Attribute appears outside of Mode:%s' % bunch.name)
    #@nonl
    #@-node:ekr.20050530065723.75:doStartElement
    #@+node:ekr.20050530065723.76:doEndElement
    def doEndElement (self,elementName):
        
        if self.printAllElements or elementName.lower() in self.printElements:
            print '</' + self.clean(elementName).strip() + '>'
            
        if elementName.lower() == 'mode':
            self.modes.append(self.mode)
            if self.verbose:
                self.mode.printSummary()
            self.mode = None
        elif self.mode:
            self.mode.endElement(elementName)
        else:
            self.error('End element appears outside of Mode:%s' % elementName)
            for bunch in self.attrsToList(attrs):
                self.error('Attribute appears outside of Mode:%s' %bunch.name)
    #@nonl
    #@-node:ekr.20050530065723.76:doEndElement
    #@+node:ekr.20050530071955:getModes
    def getModes (self):
        
        return self.modes
    #@nonl
    #@-node:ekr.20050530071955:getModes
    #@-others
#@nonl
#@-node:ekr.20050530065723.58:class contentHandler
#@+node:ekr.20050530065723.49:class modeClass
class modeClass:
    
    '''A class representing one jEdit language-description mode.
    
    Use getters to access the attributes, properties and rules of this mode.'''
    
    #@    @+others
    #@+node:ekr.20050530065723.50: mode.__init__
    def __init__ (self,contentHandler,fileName):
    
        self.contentHandler = contentHandler
        self.fileName = fileName # The file from which the mode was imported.
        self.verbose = self.contentHandler.verbose
    
        # Mode statistics...
        self.numberOfAttributes = 0
        self.numberOfElements = 0
        self.numberOfErrors = 0
        self.numberOfPropertyAttributes = 0
        self.numberOfRuleAttributes = 0
        
        # List of boolean attributes.
        self.boolAttrs = [
            'at_line_start','at_whitespace_end','at_word_start',
            'exclude_match','highlight_digits','ignore_case',
            'no_escape','no_line_break','no_word_break','no_word_sep',]
    
        # List of elements that start a rule.
        self.ruleElements = [
            'eol_span','eol_span_regexp','import','keywords',
            'mark_following','mark_previous','seq','seq_regexp',
            'span','span_regexp','terminate',]
    
        if 0: # Not used at present.
            self.seqSpanElements = [
                'eol_span','eol_span_regexp','seq','seq_regexp',
                'span','span_regexp',]
    
        # Mode semantics.
        self.attributes = {}
        self.inProps = False
        self.inRules = False
        self.props = []
        self.property = None
        self.rule = None
        self.rules = []
        self.rulesAttributes = {}
    #@nonl
    #@-node:ekr.20050530065723.50: mode.__init__
    #@+node:ekr.20050530073825: mode.__str__ & __repr__
    def __str__ (self):
        
        return '<modeClass for %s>' % self.fileName
        
    __repr__ = __str__
    #@nonl
    #@-node:ekr.20050530073825: mode.__str__ & __repr__
    #@+node:ekr.20050530081700: Printing...
    #@+node:ekr.20050530075602:printModeAttributes, printRuleAttributes & printAttributesHelper
    def printModeAttributes (self):
        
        self.printAttributesHelper('mode attributes',self.attributes)
        
    def printRuleAttributes (self):
        
        self.printAttributesHelper('rule attributes',self.rulesAttributes)
        
    def printAttributesHelper (self,kind,attrs):
        
        print '%-20s' % (kind),'attrs:',attrs
    #@nonl
    #@-node:ekr.20050530075602:printModeAttributes, printRuleAttributes & printAttributesHelper
    #@+node:ekr.20050530080452:printProperty
    def printProperty (self,property):
        
        # A property is a bunch.
        d = property.attributes
        if d:
            self.printAttributesHelper('property',d)
    #@nonl
    #@-node:ekr.20050530080452:printProperty
    #@+node:ekr.20050530075602.1:printRule
    def printRule (self,rule):
        
        # A rule is a g.Bunch.
        if rule.name == 'keywords':
            print '%-20s' % ('rule:keywords'),
            for key in ('keyword1','keyword2','keyword3','keyword4'):
                theList = rule.get(key,[])
                print key,len(theList),
            print
        else:
            d = rule.attributes
            d2 = rule.get('contents')
            if d or d2:
                print '%-20s' % ('rule:'+rule.name),
                if d and d2: print 'attrs:',d,'chars:',d2
                elif d:  print 'attrs:',d
                else:    print 'chars:',d2
    #@nonl
    #@-node:ekr.20050530075602.1:printRule
    #@+node:ekr.20050530065723.56:printSummary
    def printSummary (self,printStats=True):
    
        if printStats:
            print '-' * 10, 'mode statistics'
            print 'elements',self.numberOfElements
            print 'errors',self.numberOfErrors
            print 'mode attributes',self.numberOfAttributes
            print 'property attributes',self.numberOfPropertyAttributes
            print 'rule attributes',self.numberOfRuleAttributes
    
        self.printModeAttributes()
        self.printRuleAttributes()
        for bunch in self.props:
            self.printProperty(bunch)
        for rule in self.rules:
            self.printRule(rule)
    #@nonl
    #@-node:ekr.20050530065723.56:printSummary
    #@-node:ekr.20050530081700: Printing...
    #@+node:ekr.20050530065723.51:doAttribute
    def doAttribute (self,name,val):
        
        name = str(name.lower())
        
        if name in self.boolAttrs:
            val = g.choose(val=='True',True,False)
        else:
            val = str(val) # Do NOT lower this value!
    
        if self.rule:
            d = self.rule.get('attributes')
            d [name] = val
            self.numberOfRuleAttributes += 1
        elif self.property:
            d = self.property.get('attributes')
            d [name] = val
            self.numberOfPropertyAttributes += 1
        elif self.inRules:
            self.rulesAttributes[name] = val
            self.numberOfAttributes += 1
        else:
            self.attributes[name] = val
            self.numberOfAttributes += 1
    #@nonl
    #@-node:ekr.20050530065723.51:doAttribute
    #@+node:ekr.20050530065723.52:doContent
    def doContent (self,elementName,content):
        
        if not content:
            return
        
        name = str(elementName.lower())
    
        if name in ('keyword1','keyword2','keyword3','keyword4'):
            if self.inRule('keywords'):
                theList = self.rule.get(name,[])
                theList.append(content)
                self.rule[name] = theList
            else:
                self.error('%d not in keywords' % name)
    
        elif self.rule:
            d = self.rule.get('contents',{})
            s = d.get(name,'')
            d [name] = s + content
            self.rule['contents'] = d
    #@nonl
    #@-node:ekr.20050530065723.52:doContent
    #@+node:ekr.20050530065723.53:endElement
    def endElement (self,elementName):
    
        name = elementName.lower()
        
        if name == 'props':
            self.inProps = True
        if name == 'rules':
            self.inRules = False
        if name == 'property':
            if self.property:
                self.props.append(self.property)
                self.property = None
            else:
                self.error('end %s not matched by start %s' % (name,name))
        if name in self.ruleElements:
            if self.inRule(name):
                self.rules.append(self.rule)
                self.rule = None
            else:
                self.error('end %s not matched by start %s' % (name,name))
    #@nonl
    #@-node:ekr.20050530065723.53:endElement
    #@+node:ekr.20050530065723.54:error
    def error (self,message):
        
        self.numberOfErrors += 1
    
        self.contentHandler.error(message)
    #@nonl
    #@-node:ekr.20050530065723.54:error
    #@+node:ekr.20050530074431:getters
    def getAttributes (self):
        
        return self.attributes
    
    def getProperties (self):
        
        return self.props
        
    def getRules (self):
        
        return self.rules
    #@nonl
    #@-node:ekr.20050530074431:getters
    #@+node:ekr.20050530065723.55:inRule
    def inRule (self,elementName):
    
        return self.rule and self.rule.get('name') == elementName
    #@nonl
    #@-node:ekr.20050530065723.55:inRule
    #@+node:ekr.20050530065723.57:startElement
    def startElement (self,elementName):
    
        name = elementName.lower()
        
        if name == 'props':
            self.inProps = True
        if name == 'rules':
            self.inRules = True
        if name == 'property':
            if self.inProps:
                self.property = g.bunch(name=name,attributes={})
            else:
                self.error('property not in props element')
        if name in self.ruleElements:
            if self.inRules:
                self.rule = g.bunch(name=name,attributes={})
            else:
                self.error('%s not in rules element' % name)
    #@nonl
    #@-node:ekr.20050530065723.57:startElement
    #@-others
#@nonl
#@-node:ekr.20050530065723.49:class modeClass
#@+node:ekr.20050529143413.4:class colorizer
class colorizer:
    
    '''New colorizer using jEdit language description files'''

    #@    << define colorizer keywords >>
    #@+node:ekr.20050529143413.5:<< define colorizer keywords >> colorizer
    #@+others
    #@+node:ekr.20050529143413.6:actionscript keywords
    actionscript_keywords = [
    #Jason 2003-07-03 
    #Actionscript keywords for Leo adapted from UltraEdit syntax highlighting
    "break", "call", "continue", "delete", "do", "else", "false", "for", "function", "goto", "if", "in", "new", "null", "return", "true", "typeof", "undefined", "var", "void", "while", "with", "#include", "catch", "constructor", "prototype", "this", "try", "_parent", "_root", "__proto__", "ASnative", "abs", "acos", "appendChild", "asfunction", "asin", "atan", "atan2", "attachMovie", "attachSound", "attributes", "BACKSPACE", "CAPSLOCK", "CONTROL", "ceil", "charAt", "charCodeAt", "childNodes", "chr", "cloneNode", "close", "concat", "connect", "cos", "createElement", "createTextNode", "DELETEKEY", "DOWN", "docTypeDecl", "duplicateMovieClip", "END", "ENTER", "ESCAPE", "enterFrame", "entry", "equal", "eval", "evaluate", "exp", "firstChild", "floor", "fromCharCode", "fscommand", "getAscii", "getBeginIndex", "getBounds", "getBytesLoaded", "getBytesTotal", "getCaretIndex", "getCode", "getDate", "getDay", "getEndIndex", "getFocus", "getFullYear", "getHours", "getMilliseconds", "getMinutes", "getMonth", "getPan", "getProperty", "getRGB", "getSeconds", "getTime", "getTimer", "getTimezoneOffset", "getTransform", "getURL", "getUTCDate", "getUTCDay", "getUTCFullYear", "getUTCHours", "getUTCMilliseconds", "getUTCMinutes", "getUTCMonth", "getUTCSeconds", "getVersion", "getVolume", "getYear", "globalToLocal", "gotoAndPlay", "gotoAndStop", "HOME", "haschildNodes", "hide", "hitTest", "INSERT", "Infinity", "ifFrameLoaded", "ignoreWhite", "indexOf", "insertBefore", "int", "isDown", "isFinite", "isNaN", "isToggled", "join", "keycode", "keyDown", "keyUp", "LEFT", "LN10", "LN2", "LOG10E", "LOG2E", "lastChild", "lastIndexOf", "length", "load", "loaded", "loadMovie", "loadMovieNum", "loadVariables", "loadVariablesNum", "localToGlobal", "log", "MAX_VALUE", "MIN_VALUE", "max", "maxscroll", "mbchr", "mblength", "mbord", "mbsubstring", "min", "NEGATIVE_INFINITY", "NaN", "newline", "nextFrame", "nextScene", "nextSibling", "nodeName", "nodeType", "nodeValue", "on", "onClipEvent", "onClose", "onConnect", "onData", "onLoad", "onXML", "ord", "PGDN", "PGUP", "PI", "POSITIVE_INFINITY", "parentNode", "parseFloat", "parseInt", "parseXML", "play", "pop", "pow", "press", "prevFrame", "previousSibling", "prevScene", "print", "printAsBitmap", "printAsBitmapNum", "printNum", "push", "RIGHT", "random", "release", "removeMovieClip", "removeNode", "reverse", "round", "SPACE", "SQRT1_2", "SQRT2", "scroll", "send", "sendAndLoad", "set", "setDate", "setFocus", "setFullYear", "setHours", "setMilliseconds", "setMinutes", "setMonth", "setPan", "setProperty", "setRGB", "setSeconds", "setSelection", "setTime", "setTransform", "setUTCDate", "setUTCFullYear", "setUTCHours", "setUTCMilliseconds", "setUTCMinutes", "setUTCMonth", "setUTCSeconds", "setVolume", "setYear", "shift", "show", "sin", "slice", "sort", "start", "startDrag", "status", "stop", "stopAllSounds", "stopDrag", "substr", "substring", "swapDepths", "splice", "split", "sqrt", "TAB", "tan", "targetPath", "tellTarget", "toggleHighQuality", "toLowerCase", "toString", "toUpperCase", "trace", "UP", "UTC", "unescape", "unloadMovie", "unLoadMovieNum", "unshift", "updateAfterEvent", "valueOf", "xmlDecl", "_alpha", "_currentframe", "_droptarget", "_focusrect", "_framesloaded", "_height", "_highquality", "_name", "_quality", "_rotation", "_soundbuftime", "_target", "_totalframes", "_url", "_visible", "_width", "_x", "_xmouse", "_xscale", "_y", "_ymouse", "_yscale", "and", "add", "eq", "ge", "gt", "le", "lt", "ne", "not", "or", "Array", "Boolean", "Color", "Date", "Key", "Math", "MovieClip", "Mouse", "Number", "Object", "Selection", "Sound", "String", "XML", "XMLSocket"
    ]
    #@nonl
    #@-node:ekr.20050529143413.6:actionscript keywords
    #@+node:ekr.20050529143413.7:ada keywords
    ada_keywords = [
        "abort",       "else",       "new",        "return",
        "abs",         "elsif",      "not",        "reverse",
        "abstract",    "end",        "null",
        "accept",      "entry",      "select",
        "access",      "exception",  "separate",
        "aliased",     "exit",       "of",         "subtype",
        "all",                       "or",
        "and",         "for",        "others",     "tagged",
        "array",       "function",   "out",        "task",
        "at",                                      "terminate",
                       "generic",    "package",    "then",
        "begin",       "goto",       "pragma",     "type",
        "body",                      "private",
                       "if",         "procedure",
        "case",        "in",         "protected",  "until",
        "constant",    "is",                       "use",
                                     "raise",
        "declare",                   "range",      "when",
        "delay",       "limited",    "record",     "while",
        "delta",       "loop",       "rem",        "with",
        "digits",                    "renames",
        "do",          "mod",        "requeue",    "xor"
       ]
    #@nonl
    #@-node:ekr.20050529143413.7:ada keywords
    #@+node:ekr.20050529143413.8:c# keywords
    csharp_keywords = [
        "abstract","as",
        "base","bool","break","byte",
        "case","catch","char","checked","class","const","continue",
        "decimal","default","delegate","do","double",
        "else","enum","event","explicit","extern",
        "false","finally","fixed","float","for","foreach",
        "get","goto",
        "if","implicit","in","int","interface","internal","is",
        "lock","long",
        "namespace","new","null",
        "object","operator","out","override",
        "params","partial","private","protected","public",
        "readonly","ref","return",
        "sbyte","sealed","set","short","sizeof","stackalloc",
        "static","string","struct","switch",
        "this","throw","true","try","typeof",
        "uint","ulong","unchecked","unsafe","ushort","using",
        "value","virtual","void","volatile",
        "where","while",
        "yield"]
    #@nonl
    #@-node:ekr.20050529143413.8:c# keywords
    #@+node:ekr.20050529143413.9:c/c++ keywords
    c_keywords = [
        # C keywords
        "auto","break","case","char","continue",
        "default","do","double","else","enum","extern",
        "float","for","goto","if","int","long","register","return",
        "short","signed","sizeof","static","struct","switch",
        "typedef","union","unsigned","void","volatile","while",
        # C++ keywords
        "asm","bool","catch","class","const","const_cast",
        "delete","dynamic_cast","explicit","false","friend",
        "inline","mutable","namespace","new","operator",
        "private","protected","public","reinterpret_cast","static_cast",
        "template","this","throw","true","try",
        "typeid","typename","using","virtual","wchar_t"]
    #@nonl
    #@-node:ekr.20050529143413.9:c/c++ keywords
    #@+node:ekr.20050529143413.10:css keywords
    css_keywords = [
    #html tags
    "address", "applet", "area", "a", "base", "basefont",
    "big", "blockquote", "body", "br", "b", "caption", "center",
    "cite", "code", "dd", "dfn", "dir", "div", "dl", "dt", "em", "font",
    "form", "h1", "h2", "h3", "h4", "h5", "h6", "head", "hr", "html", "img",
    "input", "isindex", "i", "kbd", "link", "li", "link", "map", "menu",
    "meta", "ol", "option", "param", "pre", "p", "samp",
    "select", "small", "span", "strike", "strong", "style", "sub", "sup",
    "table", "td", "textarea", "th", "title", "tr", "tt", "ul", "u", "var",
    #units
    "mm", "cm", "in", "pt", "pc", "em", "ex", "px",
    #colors
    "aqua", "black", "blue", "fuchsia", "gray", "green", "lime", "maroon", "navy", "olive", "purple", "red", "silver", "teal", "yellow", "white",
    #important directive
    "!important",
    #font rules
    "font", "font-family", "font-style", "font-variant", "font-weight", "font-size",
    #font values
    "cursive", "fantasy", "monospace", "normal", "italic", "oblique", "small-caps",
    "bold", "bolder", "lighter", "medium", "larger", "smaller",
    "serif", "sans-serif",
    #background rules
    "background", "background-color", "background-image", "background-repeat", "background-attachment", "background-position",
    #background values
    "contained", "none", "top", "center", "bottom", "left", "right", "scroll", "fixed",
    "repeat", "repeat-x", "repeat-y", "no-repeat",
    #text rules
    "word-spacing", "letter-spacing", "text-decoration", "vertical-align", "text-transform", "text-align", "text-indent", "text-transform", "text-shadow", "unicode-bidi", "line-height",
    #text values
    "normal", "none", "underline", "overline", "blink", "sub", "super", "middle", "top", "text-top", "text-bottom",
    "capitalize", "uppercase", "lowercase", "none", "left", "right", "center", "justify",
    "line-through",
    #box rules
    "margin", "margin-top", "margin-bottom", "margin-left", "margin-right",
    "margin", "padding-top", "padding-bottom", "padding-left", "padding-right",
    "border", "border-width", "border-style", "border-top", "border-top-width", "border-top-style", "border-bottom", "border-bottom-width", "border-bottom-style", "border-left", "border-left-width", "border-left-style", "border-right", "border-right-width", "border-right-style", "border-color",
    #box values
    "width", "height", "float", "clear",
    "auto", "thin", "medium", "thick", "left", "right", "none", "both",
    "none", "dotted", "dashed", "solid", "double", "groove", "ridge", "inset", "outset",
    #display rules
    "display", "white-space", 
    "min-width", "max-width", "min-height", "max-height",
    "outline-color", "outline-style", "outline-width",
    #display values
    "run-in", "inline-block", "list-item", "block", "inline", "none", "normal", "pre", "nowrap", "table-cell", "table-row", "table-row-group", "table-header-group", "inline-table", "table-column", "table-column-group", "table-cell", "table-caption"
    #list rules
    "list-style", "list-style-type", "list-style-image", "list-style-position",
    #list values
    "disc", "circle", "square", "decimal", "decimal-leading-zero", "none",
    "lower-roman", "upper-roman", "lower-alpha", "upper-alpha", "lower-latin", "upper-latin",
    #table rules
    "border-collapse", "caption-side",
    #table-values
    "empty-cells", "table-layout",
    #misc values/rules
    "counter-increment", "counter-reset",
    "marker-offset", "z-index",
    "cursor", "direction", "marks", "quotes",
    "clip", "content", "orphans", "overflow", "visibility",
    #aural rules
    "pitch", "range", "pitch-during", "cue-after", "pause-after", "cue-before", "pause-before", "speak-header", "speak-numeral", "speak-punctuation", "speed-rate", "play-during", "voice-family",
    #aural values
    "stress", "azimuth", "elevation", "pitch", "richness", "volume",
    "page-break", "page-after", "page-inside"]
    #@nonl
    #@-node:ekr.20050529143413.10:css keywords
    #@+node:ekr.20050529143413.11:elisp keywords
    # EKR: needs more work.
    elisp_keywords = [
        # Maybe...
        "error","princ",
        # More typical of other lisps...
        "apply","eval",
        "t","nil",
        "and","or","not",
        "cons","car","cdr",
        "cond",
        "defconst","defun","defvar",
        "eq","ne","equal","gt","ge","lt","le",
        "if",
        "let",
        "mapcar",
        "prog","progn",
        "set","setq",
        "type-of",
        "unless",
        "when","while"]
    #@nonl
    #@-node:ekr.20050529143413.11:elisp keywords
    #@+node:ekr.20050529143413.12:forth keywords
    # Default forth keywords: extended by leo-forthwords.txt.
    forth_keywords = [
        "variable", "constant", "code", "end-code",
        "dup", "2dup", "swap", "2swap", "drop", "2drop",
        "r>", ">r", "2r>", "2>r",
        "if", "else", "then",
        "begin", "again", "until", "while", "repeat",
        "v-for", "v-next", "exit",
        "meta", "host", "target", "picasm", "macro",
        "needs", "include",
        "'", "[']",
        ":", ";",
        "@", "!", ",", "1+", "+", "-",
        "<", "<=", "=", ">=", ">",
        "invert", "and", "or", 
        ]
    
    # Forth words which define other words: extended by leo-forthdefwords.txt.
    forth_definingwords = [
        ":", "variable", "constant", "code",
        ]
    
    # Forth words which start strings: extended by leo-forthstringwords.txt.
    forth_stringwords = [
        's"', '."', '"', '."',
        'abort"',
        ]
    
    # Forth words to be rendered in boldface: extended by leo-forthboldwords.txt.
    forth_boldwords = [ ]
    
    # Forth words to be rendered in italics: extended by leo-forthitalicwords.txt.
    forth_italicwords = [ ]
    
    # Forth bold-italics words: extemded leo-forthbolditalicwords.txt if present
    # Note: on some boxen, bold italics may show in plain bold.
    forth_bolditalicwords = [ ]
    #@nonl
    #@-node:ekr.20050529143413.12:forth keywords
    #@+node:ekr.20050529143413.13:html keywords
    # No longer used by syntax colorer.
    html_keywords = []
    
    if 0: # Not used at present.
        unused_keywords = [
            # html constructs.
            "a","body","cf",
            "h1","h2","h3","h4","h5","h6",
            "head","html","hr",
            "i","img","li","lu","meta",
            "p","title","ul",
            # Common tags
            "caption","col","colgroup",
            "table","tbody","td","tfoot","th","thead","tr",
            "script","style"]
    
        html_specials = [ "<%","%>" ]
    #@nonl
    #@-node:ekr.20050529143413.13:html keywords
    #@+node:ekr.20050529143413.14:java keywords
    java_keywords = [
        "abstract","boolean","break","byte","byvalue",
        "case","cast","catch","char","class","const","continue",
        "default","do","double","else","extends",
        "false","final","finally","float","for","future",
        "generic","goto","if","implements","import","inner",
        "instanceof","int","interface","long","native",
        "new","null","operator","outer",
        "package","private","protected","public","rest","return",
        "short","static","super","switch","synchronized",
        "this","throw","transient","true","try",
        "var","void","volatile","while"]
    #@nonl
    #@-node:ekr.20050529143413.14:java keywords
    #@+node:ekr.20050529143413.15:latex keywords
    #If you see two idenitical words, with minor capitalization differences
    #DO NOT ASSUME that they are the same word. For example \vert produces
    #a single vertical line and \Vert produces a double vertical line
    #Marcus A. Martin.
    
    latex_special_keyword_characters = "@(){}%"
    
    latex_keywords = [
        #special keyworlds
        "\\%", # 11/9/03
        "\\@", "\\(", "\\)", "\\{", "\\}",
        #A
        "\\acute", "\\addcontentsline", "\\addtocontents", "\\addtocounter", "\\address",
        "\\addtolength", "\\addvspace", "\\AE", "\\ae", "\\aleph", "\\alph", "\\angle",
        "\\appendix", 
        "\\approx",	"\\arabic", "\\arccos", "\\arcsin", "\\arctan", "\\ast", "\\author",
        #B
        "\\b", "\\backmatter", "\\backslash", "\\bar", "\\baselineskip", "\\baselinestretch",
        "\\begin", "\\beta", "\\bezier", "\\bf", "\\bfseries", "\\bibitem", "\\bigcap", 
        "\\bigcup", "\\bigodot", "\\bigoplus", "\\bigotimes", "\\bigskip", "\\biguplus", 
        "\\bigvee", "\\bigwedge",	"\\bmod", "\\boldmath", "\\Box", "\\breve", "\\bullet",
        #C
        "\\c", "\\cal", "\\caption", "\\cdot", "\\cdots", "\\centering", "\\chapter", 
        "\\check", "\\chi", "\\circ", "\\circle", "\\cite", "\\cleardoublepage", "\\clearpage", 
        "\\cline",	"\\closing", "\\clubsuit", "\\coprod", "\\copywright", "\\cos", "\\cosh", 
        "\\cot", "\\coth",	"csc",
        #D
        "\\d", "\\dag", "\\dashbox", "\\date", "\\ddag", "\\ddot", "\\ddots", "\\decl", 
        "\\deg", "\\Delta", 
        "\\delta", "\\depthits", "\\det", 
        "\\DH", "\\dh", "\\Diamond", "\\diamondsuit", "\\dim", "\\div", "\\DJ", "\\dj", 
        "\\documentclass", "\\documentstyle", 
        "\\dot", "\\dotfil", "\\downarrow",
        #E
        "\\ell", "\\em", "\\emph", "\\end", "\\enlargethispage", "\\ensuremath", 
        "\\enumi", "\\enuii", "\\enumiii", "\\enuiv", "\\epsilon", "\\equation", "\\equiv",	
        "\\eta", "\\example", "\\exists", "\\exp",
        #F
        "\\fbox", "\\figure", "\\flat", "\\flushbottom", "\\fnsymbol", "\\footnote", 
        "\\footnotemark", "\\fotenotesize", 
        "\\footnotetext", "\\forall", "\\frac", "\\frame", "\\framebox", "\\frenchspacing", 
        "\\frontmatter",
        #G
        "\\Gamma", "\\gamma", "\\gcd", "\\geq", "\\gg", "\\grave", "\\guillemotleft", 
        "\\guillemotright",	"\\guilsinglleft", "\\guilsinglright",
        #H
        "\\H", "\\hat", "\\hbar", "\\heartsuit", "\\heightits", "\\hfill", "\\hline", "\\hom",
        "\\hrulefill",	"\\hspace", "\\huge",	"\\Huge",	"\\hyphenation"
        #I
        "\\Im", "\\imath", "\\include", "includeonly", "indent", "\\index", "\\inf", "\\infty", 
        "\\input", "\\int", "\\iota",	"\\it", "\\item", "\\itshape",
        #J
        "\\jmath", "\\Join",
        #K
        "\\k", "\\kappa", "\\ker", "\\kill",
        #L
        "\\label", "\\Lambda", "\\lambda", "\\langle", "\\large", "\\Large", "\\LARGE", 
        "\\LaTeX", "\\LaTeXe", 
        "\\ldots", "\\leadsto", "\\left", "\\Leftarrow", "\\leftarrow", "\\lefteqn", "\\leq",
        "\\lg", "\\lhd", "\\lim", "\\liminf", "\\limsup", "\\line", 	"\\linebreak", 
        "\\linethickness", "\\linewidth",	"\\listfiles",
        "\\ll", "\\ln", "\\location", "\\log", "\\Longleftarrow", "\\longleftarrow", 
        "\\Longrightarrow",	"longrightarrow",
        #M
        "\\mainmatter", "\\makebox", "\\makeglossary", "\\makeindex","\\maketitle", "\\markboth", "\\markright",
        "\\mathbf", "\\mathcal", "\\mathit", "\\mathnormal", "\\mathop",
        "\\mathrm", "\\mathsf", "\\mathtt", "\\max", "\\mbox", "\\mdseries", "\\medskip",
        "\\mho", "\\min", "\\mp", "\\mpfootnote", "\\mu", "\\multicolumn", "\\multiput",
        #N
        "\\nabla", "\\natural", "\\nearrow", "\\neq", "\\newcommand", "\\newcounter", 
        "\\newenvironment", "\\newfont",
        "\\newlength",	"\\newline", "\\newpage", "\\newsavebox", "\\newtheorem", "\\NG", "\\ng",
        "\\nocite", "\\noindent", "\\nolinbreak", "\\nopagebreak", "\\normalsize",
        "\\not", "\\nu", "nwarrow",
        #O
        "\\Omega", "\\omega", "\\onecolumn", "\\oint", "\\opening", "\\oval", 
        "\\overbrace", "\\overline",
        #P
        "\\P", "\\page", "\\pagebreak", "\\pagenumbering", "\\pageref", "\\pagestyle", 
        "\\par", "\\parbox",	"\\paragraph", "\\parindent", "\\parskip", "\\part", 
        "\\partial", "\\per", "\\Phi", 	"\\phi",	"\\Pi", "\\pi", "\\pm", 
        "\\pmod", "\\pounds", "\\prime", "\\printindex", "\\prod", "\\propto", "\\protext", 
        "\\providecomamnd", "\\Psi",	"\\psi", "\\put",
        #Q
        "\\qbezier", "\\quoteblbase", "\\quotesinglbase",
        #R
        "\\r", "\\raggedbottom", "\\raggedleft", "\\raggedright", "\\raisebox", "\\rangle", 
        "\\Re", "\\ref", 	"\\renewcommand", "\\renewenvironment", "\\rhd", "\\rho", "\\right", 
        "\\Rightarrow",	"\\rightarrow", "\\rm", "\\rmfamily",
        "\\Roman", "\\roman", "\\rule", 
        #S
        "\\s", "\\samepage", "\\savebox", "\\sbox", "\\sc", "\\scriptsize", "\\scshape", 
        "\\searrow",	"\\sec", "\\section",
        "\\setcounter", "\\setlength", "\\settowidth", "\\settodepth", "\\settoheight", 
        "\\settowidth", "\\sf", "\\sffamily", "\\sharp", "\\shortstack", "\\Sigma", "\\sigma", 
        "\\signature", "\\sim", "\\simeq", "\\sin", "\\sinh", "\\sl", "\\SLiTeX",
        "\\slshape", "\\small", "\\smallskip", "\\spadesuit", "\\sqrt", "\\sqsubset",	
        "\\sqsupset", "\\SS",
        "\\stackrel", "\\star", "\\subsection", "\\subset", 
        "\\subsubsection", "\\sum", "\\sup", "\\supressfloats", "\\surd", "\\swarrow",
        #T
        "\\t", "\\table", "\\tableofcontents", "\\tabularnewline", "\\tan", "\\tanh", 
        "\\tau", "\\telephone",	"\\TeX", "\\textbf",
        "\\textbullet", "\\textcircled", "\\textcompworkmark",	"\\textemdash", 
        "\\textendash", "\\textexclamdown", "\\textheight", "\\textquestiondown", 
        "\\textquoteblleft", "\\textquoteblright", "\\textquoteleft",
        "\\textperiod", "\\textquotebl", "\\textquoteright", "\\textmd", "\\textit", "\\textrm", 
        "\\textsc", "\\textsl", "\\textsf", "\\textsuperscript", "\\texttt", "\\textup",
        "\\textvisiblespace", "\\textwidth", "\\TH", "\\th", "\\thanks", "\\thebibligraphy",
        "\\Theta", "theta", 
        "\\tilde", "\\thinlines", 
        "\\thispagestyle", "\\times", "\\tiny", "\\title",	"\\today", "\\totalheightits", 
        "\\triangle", "\\tt", 
        "\\ttfamily", "\\twocoloumn", "\\typeout", "\\typein",
        #U
        "\\u", "\\underbrace", "\\underline", "\\unitlength", "\\unlhd", "\\unrhd", "\\Uparrow",
        "\\uparrow",	"\\updownarrow", "\\upshape", "\\Upsilon", "\\upsilon", "\\usebox",	
        "\\usecounter", "\\usepackage", 
        #V
        "\\v", "\\value", "\\varepsilon", "\\varphi", "\\varpi", "\\varrho", "\\varsigma", 
        "\\vartheta", "\\vdots", "\\vec", "\\vector", "\\verb", "\\Vert", "\\vert", 	"\\vfill",
        "\\vline", "\\vphantom", "\\vspace",
        #W
        "\\widehat", "\\widetilde", "\\widthits", "\\wp",
        #X
        "\\Xi", "\\xi",
        #Z
        "\\zeta" ]
    #@nonl
    #@-node:ekr.20050529143413.15:latex keywords
    #@+node:ekr.20050529143413.16:pascal keywords
    pascal_keywords = [
        "and","array","as","begin",
        "case","const","class","constructor","cdecl"
        "div","do","downto","destructor","dispid","dynamic",
        "else","end","except","external",
        "false","file","for","forward","function","finally",
        "goto","if","in","is","label","library",
        "mod","message","nil","not","nodefault""of","or","on",
        "procedure","program","packed","pascal",
        "private","protected","public","published",
        "record","repeat","raise","read","register",
        "set","string","shl","shr","stdcall",
        "then","to","true","type","try","until","unit","uses",
        "var","virtual","while","with","xor"
        # object pascal
        "asm","absolute","abstract","assembler","at","automated",
        "finalization",
        "implementation","inherited","initialization","inline","interface",
        "object","override","resident","resourcestring",
        "threadvar",
        # limited contexts
        "exports","property","default","write","stored","index","name" ]
    #@nonl
    #@-node:ekr.20050529143413.16:pascal keywords
    #@+node:ekr.20050529143413.17:perl keywords
    perl_keywords = [
        "continue","do","else","elsif","format","for","format","for","foreach",
        "if","local","package","sub","tr","unless","until","while","y",
        # Comparison operators
        "cmp","eq","ge","gt","le","lt","ne",
        # Matching ooperators
        "m","s",
        # Unary functions
        "alarm","caller","chdir","cos","chroot","exit","eval","exp",
        "getpgrp","getprotobyname","gethostbyname","getnetbyname","gmtime",
        "hex","int","length","localtime","log","ord","oct",
        "require","reset","rand","rmdir","readlink",
        "scalar","sin","sleep","sqrt","srand","umask",
        # Transfer ops
        "next","last","redo","go","dump",
        # File operations...
        "select","open",
        # FL ops
        "binmode","close","closedir","eof",
        "fileno","getc","getpeername","getsockname","lstat",
        "readdir","rewinddir","stat","tell","telldir","write",
        # FL2 ops
        "bind","connect","flock","listen","opendir",
        "seekdir","shutdown","truncate",
        # FL32 ops
        "accept","pipe",
        # FL3 ops
        "fcntl","getsockopt","ioctl","read",
        "seek","send","sysread","syswrite",
        # FL4 & FL5 ops
        "recv","setsocket","socket","socketpair",
        # Array operations
        "pop","shift","split","delete",
        # FLIST ops
        "sprintf","grep","join","pack",
        # LVAL ops
        "chop","defined","study","undef",
        # f0 ops
        "endhostent","endnetent","endservent","endprotoent",
        "endpwent","endgrent","fork",
        "getgrent","gethostent","getlogin","getnetent","getppid",
        "getprotoent","getpwent","getservent",
        "setgrent","setpwent","time","times","wait","wantarray",
        # f1 ops
        "getgrgid","getgrnam","getprotobynumber","getpwnam","getpwuid",
        "sethostent","setnetent","setprotoent","setservent",
        # f2 ops
        "atan2","crypt",
        "gethostbyaddr","getnetbyaddr","getpriority","getservbyname","getservbyport",
        "index","link","mkdir","msgget","rename",
        "semop","setpgrp","symlink","unpack","waitpid",
        # f2 or 3 ops
        "index","rindex","substr",
        # f3 ops
        "msgctl","msgsnd","semget","setpriority","shmctl","shmget","vec",
        # f4 & f5 ops
        "semctl","shmread","shmwrite","msgrcv",
        # Assoc ops
        "dbmclose","each","keys","values",
        # List ops
        "chmod","chown","die","exec","kill",
        "print","printf","return","reverse",
        "sort","system","syscall","unlink","utime","warn"]
    #@nonl
    #@-node:ekr.20050529143413.17:perl keywords
    #@+node:ekr.20050529143413.18:php keywords
    php_keywords = [ # 08-SEP-2002 DTHEIN
        "__CLASS__", "__FILE__", "__FUNCTION__", "__LINE__",
        "and", "as", "break",
        "case", "cfunction", "class", "const", "continue",
        "declare", "default", "do",
        "else", "elseif", "enddeclare", "endfor", "endforeach",
        "endif", "endswitch",  "endwhile", "eval", "extends",
        "for", "foreach", "function", "global", "if",
        "new", "old_function", "or", "static", "switch",
        "use", "var", "while", "xor" ]
        
    # The following are supposed to be followed by ()
    php_paren_keywords = [
        "array", "die", "echo", "empty", "exit",
        "include", "include_once", "isset", "list",
        "print", "require", "require_once", "return",
        "unset" ]
        
    # The following are handled by special case code:
    # "<?php", "?>"
    #@-node:ekr.20050529143413.18:php keywords
    #@+node:ekr.20050529143413.19:python keywords
    python_keywords = [
        "and",       "del",       "for",       "is",        "raise",    
        "assert",    "elif",      "from",      "lambda",    "return",   
        "break",     "else",      "global",    "not",       "try",      
        "class",     "except",    "if",        "or",        "yield",   
        "continue",  "exec",      "import",    "pass",      "while",
        "def",       "finally",   "in",        "print"]
    #@nonl
    #@-node:ekr.20050529143413.19:python keywords
    #@+node:ekr.20050529143413.20:rapidq keywords
    rapidq_keywords = [
    # Syntax file for RapidQ
    "$APPTYPE","$DEFINE","$ELSE","$ENDIF","$ESCAPECHARS","$IFDEF","$IFNDEF",
    "$INCLUDE","$MACRO","$OPTIMIZE","$OPTION","$RESOURCE","$TYPECHECK","$UNDEF",
    "ABS","ACOS","ALIAS","AND","AS","ASC","ASIN","ATAN","ATN","BIN$","BIND","BYTE",
    "CALL","CALLBACK","CALLFUNC","CASE","CEIL","CHDIR","CHDRIVE","CHR$","CINT",
    "CLNG","CLS","CODEPTR","COMMAND$","COMMANDCOUNT","CONSOLE","CONST","CONSTRUCTOR",
    "CONVBASE$","COS","CREATE","CSRLIN","CURDIR$","DATA","DATE$","DEC","DECLARE",
    "DEFBYTE","DEFDBL","DEFDWORD","DEFINT","DEFLNG","DEFSHORT","DEFSNG","DEFSTR",
    "DEFWORD","DELETE$","DIM","DIR$","DIREXISTS","DO","DOEVENTS","DOUBLE","DWORD",
    "ELSE","ELSEIF","END","ENVIRON","ENVIRON$","EVENT","EXIT","EXP","EXTENDS",
    "EXTRACTRESOURCE","FIELD$","FILEEXISTS","FIX","FLOOR","FOR","FORMAT$","FRAC",
    "FUNCTION","FUNCTIONI","GET$","GOSUB","GOTO","HEX$","IF","INC","INITARRAY",
    "INKEY$","INP","INPUT","INPUT$","INPUTHANDLE","INSERT$","INSTR","INT","INTEGER",
    "INV","IS","ISCONSOLE","KILL","KILLMESSAGE","LBOUND","LCASE$","LEFT$","LEN",
    "LFLUSH","LIB","LIBRARYINST","LOCATE","LOG","LONG","LOOP","LPRINT","LTRIM$",
    "MEMCMP","MESSAGEBOX","MESSAGEDLG","MID$","MKDIR","MOD","MOUSEX","MOUSEY",
    "NEXT","NOT","OFF","ON","OR","OUT","OUTPUTHANDLE","PARAMSTR$","PARAMSTRCOUNT",
    "PARAMVAL","PARAMVALCOUNT","PCOPY","PEEK","PLAYWAV","POKE","POS","POSTMESSAGE",
    "PRINT","PROPERTY","QUICKSORT","RANDOMIZE","REDIM","RENAME","REPLACE$",
    "REPLACESUBSTR$","RESOURCE","RESOURCECOUNT","RESTORE","RESULT","RETURN",
    "REVERSE$","RGB","RIGHT$","RINSTR","RMDIR","RND","ROUND","RTRIM$","RUN",
    "SCREEN","SELECT","SENDER","SENDMESSAGE","SETCONSOLETITLE","SGN","SHELL",
    "SHL","SHORT","SHOWMESSAGE","SHR","SIN","SINGLE","SIZEOF","SLEEP","SOUND",
    "SPACE$","SQR","STACK","STATIC","STEP","STR$","STRF$","STRING","STRING$",
    "SUB","SUBI","SWAP","TALLY","TAN","THEN","TIME$","TIMER","TO","TYPE","UBOUND",
    "UCASE$","UNLOADLIBRARY","UNTIL","VAL","VARIANT","VARPTR","VARPTR$","VARTYPE",
    "WEND","WHILE","WITH","WORD","XOR"]
    #@nonl
    #@-node:ekr.20050529143413.20:rapidq keywords
    #@+node:ekr.20050529143413.21:rebol keywords
    rebol_keywords = [
    #Jason 2003-07-03 
    #based on UltraEdit syntax highlighting
    "about", "abs", "absolute", "add", "alert", "alias", "all", "alter", "and", "and~", "any", "append", "arccosine", "arcsine", "arctangent", "array", "ask", "at",  
    "back", "bind", "boot-prefs", "break", "browse", "build-port", "build-tag",  
    "call", "caret-to-offset", "catch", "center-face", "change", "change-dir", "charset", "checksum", "choose", "clean-path", "clear", "clear-fields", "close", "comment", "complement", "compose", "compress", "confirm", "continue-post", "context", "copy", "cosine", "create-request", "crypt", "cvs-date", "cvs-version",  
    "debase", "decode-cgi", "decode-url", "decompress", "deflag-face", "dehex", "delete", "demo", "desktop", "detab", "dh-compute-key", "dh-generate-key", "dh-make-key", "difference", "dirize", "disarm", "dispatch", "divide", "do", "do-boot", "do-events", "do-face", "do-face-alt", "does", "dsa-generate-key", "dsa-make-key", "dsa-make-signature", "dsa-verify-signature",  
    "echo", "editor", "either", "else", "emailer", "enbase", "entab", "exclude", "exit", "exp", "extract", 
    "fifth", "find", "find-key-face", "find-window", "flag-face", "first", "flash", "focus", "for", "forall", "foreach", "forever", "form", "forskip", "fourth", "free", "func", "function",  
    "get", "get-modes", "get-net-info", "get-style",  
    "halt", "has", "head", "help", "hide", "hide-popup",  
    "if", "import-email", "in", "inform", "input", "insert", "insert-event-func", "intersect", 
    "join", 
    "last", "launch", "launch-thru", "layout", "license", "list-dir", "load", "load-image", "load-prefs", "load-thru", "log-10", "log-2", "log-e", "loop", "lowercase",  
    "make", "make-dir", "make-face", "max", "maximum", "maximum-of", "min", "minimum", "minimum-of", "mold", "multiply",  
    "negate", "net-error", "next", "not", "now",  
    "offset-to-caret", "open", "open-events", "or", "or~", 
    "parse", "parse-email-addrs", "parse-header", "parse-header-date", "parse-xml", "path-thru", "pick", "poke", "power", "prin", "print", "probe", "protect", "protect-system",  
    "q", "query", "quit",  
    "random", "read", "read-io", "read-net", "read-thru", "reboot", "recycle", "reduce", "reform", "rejoin", "remainder", "remold", "remove", "remove-event-func", "rename", "repeat", "repend", "replace", "request", "request-color", "request-date", "request-download", "request-file", "request-list", "request-pass", "request-text", "resend", "return", "reverse", "rsa-encrypt", "rsa-generate-key", "rsa-make-key", 
    "save", "save-prefs", "save-user", "scroll-para", "second", "secure", "select", "send", "send-and-check", "set", "set-modes", "set-font", "set-net", "set-para", "set-style", "set-user", "set-user-name", "show", "show-popup", "sine", "size-text", "skip", "sort", "source", "split-path", "square-root", "stylize", "subtract", "switch",  
    "tail", "tangent", "textinfo", "third", "throw", "throw-on-error", "to", "to-binary", "to-bitset", "to-block", "to-char", "to-date", "to-decimal", "to-email", "to-event", "to-file", "to-get-word", "to-hash", "to-hex", "to-idate", "to-image", "to-integer", "to-issue", "to-list", "to-lit-path", "to-lit-word", "to-local-file", "to-logic", "to-money", "to-none", "to-pair", "to-paren", "to-path", "to-rebol-file", "to-refinement", "to-set-path", "to-set-word", "to-string", "to-tag", "to-time", "to-tuple", "to-url", "to-word", "trace", "trim", "try",  
    "unfocus", "union", "unique", "uninstall", "unprotect", "unset", "until", "unview", "update", "upgrade", "uppercase", "usage", "use",  
    "vbug", "view", "view-install", "view-prefs",  
    "wait", "what", "what-dir", "while", "write", "write-io",  
    "xor", "xor~",  
    "action!", "any-block!", "any-function!", "any-string!", "any-type!", "any-word!",  
    "binary!", "bitset!", "block!",  
    "char!",  
    "datatype!", "date!", "decimal!", 
    "email!", "error!", "event!",  
    "file!", "function!",  
    "get-word!",  
    "hash!",  
    "image!", "integer!", "issue!",  
    "library!", "list!", "lit-path!", "lit-word!", "logic!",  
    "money!",  
    "native!", "none!", "number!",  
    "object!", "op!",  
    "pair!", "paren!", "path!", "port!",  
    "refinement!", "routine!",  
    "series!", "set-path!", "set-word!", "string!", "struct!", "symbol!",  
    "tag!", "time!", "tuple!",  
    "unset!", "url!",  
    "word!",  
    "any-block?", "any-function?", "any-string?", "any-type?", "any-word?",  
    "binary?", "bitset?", "block?",  
    "char?", "connected?", "crypt-strength?", 
    "datatype?", "date?", "decimal?", "dir?",  
    "email?", "empty?", "equal?", "error?", "even?", "event?", "exists?", "exists-key?",
    "file?", "flag-face?", "found?", "function?",  
    "get-word?", "greater-or-equal?", "greater?",  
    "hash?", "head?",  
    "image?", "in-window?", "index?", "info?", "input?", "inside?", "integer?", "issue?",  
    "length?", "lesser-or-equal?", "lesser?", "library?", "link-app?", "link?", "list?", "lit-path?", "lit-word?", "logic?",  
    "modified?", "money?",  
    "native?", "negative?", "none?", "not-equal?", "number?",  
    "object?", "odd?", "offset?", "op?", "outside?",  
    "pair?", "paren?", "path?", "port?", "positive?",  
    "refinement?", "routine?",  
    "same?", "screen-offset?", "script?", "series?", "set-path?", "set-word?", "size?", "span?", "strict-equal?", "strict-not-equal?", "string?", "struct?",  
    "tag?", "tail?", "time?", "tuple?", "type?",  
    "unset?", "url?",  
    "value?", "view?", 
    "within?", "word?",  
    "zero?"
    ]
    #@nonl
    #@-node:ekr.20050529143413.21:rebol keywords
    #@+node:ekr.20050529143413.22:shell keywords
    shell_keywords = [
        # reserved keywords
        "case","do","done","elif","else","esac","fi",
        "for","if","in","then",
        "until","while",
        "break","cd","chdir","continue","eval","exec",
        "exit","kill","newgrp","pwd","read","readonly",
        "return","shift","test","trap","ulimit",
        "umask","wait" ]
    #@nonl
    #@-node:ekr.20050529143413.22:shell keywords
    #@+node:ekr.20050529143413.23:tcl/tk keywords
    tcltk_keywords = [ # Only the tcl keywords are here.
        "after",     "append",    "array",
        "bgerror",   "binary",    "break",
        "catch",     "cd",        "clock",
        "close",     "concat",    "continue",
        "dde",
        "encoding",  "eof",       "eval",
        "exec",      "exit",      "expr",
        "fblocked",  "fconfigure","fcopy",     "file",      "fileevent",
        "filename",  "flush",     "for",       "foreach",   "format",
        "gets",      "glob",      "global",
        "history",
        "if",        "incr",      "info",      "interp",
        "join",
        "lappend",   "lindex",    "linsert",   "list",      "llength",
        "load",      "lrange",    "lreplace",  "lsearch",   "lsort",
        "memory",    "msgcat",
        "namespace",
        "open",
        "package",   "parray",    "pid",
        "proc",      "puts",      "pwd",
        "read",      "regexp",    "registry",   "regsub",
        "rename",    "resource",  "return",
        "scan",      "seek",      "set",        "socket",   "source",
        "split",     "string",    "subst",      "switch",
        "tell",      "time",      "trace",
        "unknown",   "unset",     "update",     "uplevel",   "upvar",
        "variable",  "vwait",
        "while" ]
    #@nonl
    #@-node:ekr.20050529143413.23:tcl/tk keywords
    #@-others
    
    cweb_keywords = c_keywords
    perlpod_keywords = perl_keywords
    #@nonl
    #@-node:ekr.20050529143413.5:<< define colorizer keywords >> colorizer
    #@nl

    #@    @+others
    #@+node:ekr.20050529143413.24:color.__init__
    def __init__(self,c):
        
        g.trace('jEdit_colorizer.__init__')
    
        self.c = c
        self.frame = c.frame
        self.body = c.frame.body
        
        self.modes = self.parse_jEdit_file('python')
        if 1:
            mode0 = self.modes[0]
            mode0.printSummary (printStats=False)
            self.ruleMatchers = self.createRuleMatchers(mode0.rules)
            self.color_thread = None
            self.kill_thread = False
    
        self.count = 0 # how many times this has been called.
        self.use_hyperlinks = False # True: use hyperlinks and underline "live" links.
        self.enabled = True # True: syntax coloring enabled
        self.showInvisibles = False # True: show "invisible" characters.
        self.comment_string = None # Set by scanColorDirectives on @comment
        # For incremental coloring.
        self.tags = (
            "blank","comment","cwebName","docPart","keyword","leoKeyword",
            "latexModeBackground","latexModeKeyword",
            "latexBackground","latexKeyword",
            "link","name","nameBrackets","pp","string","tab",
            "elide","bold","bolditalic","italic") # new for wiki styling.
        self.color_pass = 0
        self.incremental = False
        self.redoColoring = False
        self.redoingColoring = False
        self.sel = None
        self.lines = []
        self.states = []
        self.last_flag = "unknown"
        self.last_language = "unknown"
        self.last_comment = "unknown"
        # For use of external markup routines.
        self.last_markup = "unknown" 
        self.markup_string = "unknown"
        #@    << ivars for communication between colorizeAnyLanguage and its allies >>
        #@+node:ekr.20050529143413.25:<< ivars for communication between colorizeAnyLanguage and its allies >>
        # Copies of arguments.
        self.p = None
        self.language = None
        self.flag = None
        self.killFlag = False
        self.line_index = 0
        
        # Others.
        self.single_comment_start = None
        self.block_comment_start = None
        self.block_comment_end = None
        self.case_sensitiveLanguage = True
        self.has_string = None
        self.string_delims = ("'",'"')
        self.has_pp_directives = None
        self.keywords = None
        self.lb = None
        self.rb = None
        self.rootMode = None # None, "code" or "doc"
        
        self.latex_cweb_docs     = c.config.getBool("color_cweb_doc_parts_with_latex")
        self.latex_cweb_comments = c.config.getBool("color_cweb_comments_with_latex")
        # print "docs,comments",self.latex_cweb_docs,self.latex_cweb_comments
        #@nonl
        #@-node:ekr.20050529143413.25:<< ivars for communication between colorizeAnyLanguage and its allies >>
        #@nl
        #@    << define dispatch dicts >>
        #@+node:ekr.20050529143413.26:<< define dispatch dicts >>
        self.state_dict = {
            "blockComment" : self.continueBlockComment,
            "doubleString" : self.continueDoubleString,
            "nocolor"      : self.continueNocolor,
            "normal"       : self.doNormalState,
            "singleString" : self.continueSingleString,
            "string3s"     : self.continueSinglePythonString,
            "string3d"     : self.continueDoublePythonString,
            "doc"          : self.continueDocPart }
            
        # Eventually all entries in these dicts will be entered dynamically
        # under the control of the XML description of the present language.
        
        if 0: # not ready yet.
        
            self.dict1 = { # 1-character patterns.
                '"' : self.doString,
                "'" : self.doString,
                '@' : self.doPossibleLeoKeyword,
                ' ' : self.doBlank,
                '\t': self.doTab }
        
            self.dict2 = {} # 2-character patterns
            
            # Searching this list might be very slow!
            mutli_list = [] # Multiple character patterns.
            
            # Enter single-character patterns...
            if self.has_pp_directives:
                dict1 ["#"] = self.doPPDirective
                        
            for ch in string.ascii_letters:
                dict1 [ch] = self.doPossibleKeyword
            dict1 ['_'] = self.doPossibleKeyword
            
            if self.language == "latex":
                dict1 ['\\'] = self.doPossibleKeyword
                
            if self.language == "php":
                dict1 ['<'] = self.doSpecialPHPKeyword
                dict1 ['?'] = self.doSpecialPHPKeyword
            
            # Enter potentially multi-character patterns.  (or should this be just 2-character patterns)
            if self.language == "cweb":
                dict2 ["@("] = self.doPossibleSectionRefOrDef
            else:
                dict2 ["<<"] = self.doPossibleSectionRefOrDef
                
            if self.single_comment_start:
                n = len(self.single_comment_start)
                if n == 1:
                    dict1 [self.single_comment_start] = self.doSingleCommentLine
                elif n == 2:
                    dict2 [self.single_comment_start] = self.doSingleCommentLine
                else:
                    mutli_list.append((self.single_comment_start,self.doSingleCommentLine),)
            
            if self.block_comment_start:
                n = len(self.block_comment_start)
                if n == 1:
                    dict1 [self.block_comment_start] = self.doBlockComment
                elif n == 2:
                    ddict2 [self.block_comment_start] = self.doBlockComment
                else:
                    mutli_list.append((self.block_comment_start,self.doBlockComment),)
        #@nonl
        #@-node:ekr.20050529143413.26:<< define dispatch dicts >>
        #@nl
        self.setFontFromConfig()
        #@    << extend forth words from files >>
        #@+node:ekr.20050529143413.27:<< extend forth words from files >>
        # Associate files with lists: probably no need to edit this.
        forth_items = (
            (self.forth_definingwords, "leo-forthdefwords.txt", "defining words"),
            (self.forth_keywords, "leo-forthwords.txt", "words"),
            (self.forth_stringwords, "leo-forthstringwords.txt", "string words"),
            (self.forth_boldwords, "leo-forthboldwords.txt", "bold words"),
            (self.forth_bolditalicwords, "leo-forthbolditalicwords.txt", "bold-italic words"),
            (self.forth_italicwords, "leo-forthitalicwords.txt", "italic words"),
        )
        
        # Add entries from files (if they exist) and to the corresponding wordlists.
        for (lst, path, typ) in forth_items:
            try:
                extras = []
                path = g.os_path_join(g.app.loadDir,"..","plugins",path) # EKR.
                for line in file(path).read().strip().split("\n"):
                    line = line.strip()
                    if line and line[0] != '\\':
                        extras.append(line)
                if extras:
                    if 0: # I find this annoying.  YMMV.
                        if not g.app.unitTesting and not g.app.batchMode:
                            print "Found extra forth %s" % typ + ": " + " ".join(extras)
                    lst.extend(extras)
            except IOError:
                # print "Not found",path
                pass
        #@nonl
        #@-node:ekr.20050529143413.27:<< extend forth words from files >>
        #@nl
    #@nonl
    #@-node:ekr.20050529143413.24:color.__init__
    #@+node:ekr.20050529145203:Entry points & helpers
    #@+node:ekr.20050529143413.30:colorize (Main entry point)
    def colorize(self,p,incremental=False):
        
        '''The main colorizer entry point.'''
    
        if self.enabled:
            self.incremental=incremental
            self.updateSyntaxColorer(p)
            return self.colorizeAnyLanguage(p)
        else:
            return "ok" # For unit testing.
    #@nonl
    #@-node:ekr.20050529143413.30:colorize (Main entry point)
    #@+node:ekr.20050529143413.28:disable
    def disable (self):
    
        print "disabling all syntax coloring"
        self.enabled=False
    #@nonl
    #@-node:ekr.20050529143413.28:disable
    #@+node:ekr.20050529145203.1:recolor_range
    def recolor_range(self,p,leading,trailing):
        
        '''An entry point for the colorer called from incremental undo code.
        Colorizes the lines between the leading and trailing lines.'''
        
        g.trace()
        
        if self.enabled:
            self.incremental=True
            self.updateSyntaxColorer(p)
            return self.colorizeAnyLanguage(p,leading=leading,trailing=trailing)
        else:
            return "ok" # For unit testing.
    #@nonl
    #@-node:ekr.20050529145203.1:recolor_range
    #@+node:ekr.20050529143413.84:schedule & idle_colorize
    def schedule(self,p,incremental=0):
        
        __pychecker__ = '--no-argsused'
        # p not used, but it is difficult to remove.
    
        if self.enabled:
            self.incremental=incremental
            g.app.gui.setIdleTimeHook(self.idle_colorize)
            
    def idle_colorize(self):
    
        # New in 4.3b1: make sure the colorizer still exists!
        if hasattr(self,'enabled') and self.enabled:
            p = self.c.currentPosition()
            if p:
                self.colorize(p,self.incremental)
    #@nonl
    #@-node:ekr.20050529143413.84:schedule & idle_colorize
    #@+node:ekr.20050529143413.87:updateSyntaxColorer & helpers
    def updateSyntaxColorer (self,p):
    
        p = p.copy()
        # self.flag is True unless an unambiguous @nocolor is seen.
        self.flag = self.useSyntaxColoring(p)
        self.scanColorDirectives(p)
    #@nonl
    #@+node:ekr.20050529143413.81:scanColorDirectives
    def scanColorDirectives(self,p):
        
        """Scan position p and p's ancestors looking for @comment, @language and @root directives,
        setting corresponding colorizer ivars.
        """
    
        p = p.copy() ; c = self.c
        if c == None: return # self.c may be None for testing.
    
        language = c.target_language
        self.language = language # 2/2/03
        self.comment_string = None
        self.rootMode = None # None, "code" or "doc"
        
        for p in p.self_and_parents_iter():
            # g.trace(p)
            s = p.v.t.bodyString
            theDict = g.get_directives_dict(s)
            #@        << Test for @comment or @language >>
            #@+node:ekr.20050529143413.82:<< Test for @comment or @language >>
            # 10/17/02: @comment and @language may coexist in the same node.
            
            if theDict.has_key("comment"):
                k = theDict["comment"]
                self.comment_string = s[k:]
            
            if theDict.has_key("language"):
                i = theDict["language"]
                language,junk,junk,junk = g.set_language(s,i)
                self.language = language # 2/2/03
            
            if theDict.has_key("comment") or theDict.has_key("language"):
                break
            #@nonl
            #@-node:ekr.20050529143413.82:<< Test for @comment or @language >>
            #@nl
            #@        << Test for @root, @root-doc or @root-code >>
            #@+node:ekr.20050529143413.83:<< Test for @root, @root-doc or @root-code >>
            if theDict.has_key("root") and not self.rootMode:
            
                k = theDict["root"]
                if g.match_word(s,k,"@root-code"):
                    self.rootMode = "code"
                elif g.match_word(s,k,"@root-doc"):
                    self.rootMode = "doc"
                else:
                    doc = c.config.at_root_bodies_start_in_doc_mode
                    self.rootMode = g.choose(doc,"doc","code")
            #@nonl
            #@-node:ekr.20050529143413.83:<< Test for @root, @root-doc or @root-code >>
            #@nl
    
        return self.language # For use by external routines.
    #@nonl
    #@-node:ekr.20050529143413.81:scanColorDirectives
    #@+node:ekr.20050529143413.88:useSyntaxColoring
    def useSyntaxColoring (self,p):
        
        """Return True unless p is unambiguously under the control of @nocolor."""
        
        p = p.copy() ; first = p.copy()
        val = True ; self.killFlag = False
        for p in p.self_and_parents_iter():
            # g.trace(p)
            s = p.v.t.bodyString
            theDict = g.get_directives_dict(s)
            no_color = theDict.has_key("nocolor")
            color = theDict.has_key("color")
            kill_color = theDict.has_key("killcolor")
            # A killcolor anywhere disables coloring.
            if kill_color:
                val = False ; self.killFlag = True ; break
            # A color anywhere in the target enables coloring.
            if color and p == first:
                val = True ; break
            # Otherwise, the @nocolor specification must be unambiguous.
            elif no_color and not color:
                val = False ; break
            elif color and not no_color:
                val = True ; break
    
        return val
    #@-node:ekr.20050529143413.88:useSyntaxColoring
    #@-node:ekr.20050529143413.87:updateSyntaxColorer & helpers
    #@-node:ekr.20050529145203:Entry points & helpers
    #@+node:ekr.20050529150436:Colorizer code
    #@+node:ekr.20050529143413.31:colorizeAnyLanguage
    def colorizeAnyLanguage (self,p,leading=None,trailing=None):
        
        '''Color the body pane.  All coloring starts here.'''
        
        # g.trace("incremental",self.incremental,p.headString())
        if self.killFlag:
            # @killcolor is in effect.
            self.removeAllTags()
            return
        try:
            s,lines,state = self.init_ivars(p)
            self.configure_tags()
            g.doHook("init-color-markup",colorer=self,p=self.p,v=self.p)
            self.colorAll(s)
            if 0:  ## TO BE REMOVED
                self.color_pass = 0
                if self.incremental and (
                    #@                << all state ivars match >>
                    #@+node:ekr.20050529143413.35:<< all state ivars match >>
                    self.flag == self.last_flag and
                    self.last_language == self.language and
                    self.comment_string == self.last_comment and
                    self.markup_string == self.last_markup
                    #@nonl
                    #@-node:ekr.20050529143413.35:<< all state ivars match >>
                    #@afterref
 ):
                    self.color_incremental(lines,state,leading,trailing)
                else: self.color_nonincremental(lines,state)
                if self.redoColoring: self.recolor_all()
                #@            << update state ivars >>
                #@+node:ekr.20050529143413.44:<< update state ivars >>
                self.last_flag = self.flag
                self.last_language = self.language
                self.last_comment = self.comment_string
                self.last_markup = self.markup_string
                #@nonl
                #@-node:ekr.20050529143413.44:<< update state ivars >>
                #@nl
            return "ok" # for testing.
        except Exception:
            self.last_flag = self.last_language = self.last_comment = 'unknown'
            g.es_exception()
            return "error" # for unit testing.
    #@nonl
    #@-node:ekr.20050529143413.31:colorizeAnyLanguage
    #@+node:ekr.20050601042620:colorAll & interrupt
    def colorAll(self,s):
        '''Colorize all of s.'''
        # Init colorOneChunk.
        self.chunk_s = s
        self.chunk_i = 0
        self.prev_token = None
        self.follow_token = None
        self.kill_chunk = False
        self.colorOneChunk()
    
    # This is needed, even without threads.
    def interrupt(self):
        '''Interrupt colorOneChunk'''
        self.kill_chunk = True
    #@nonl
    #@-node:ekr.20050601042620:colorAll & interrupt
    #@+node:ekr.20050601105358:colorOneChunk
    def colorOneChunk(self):
        '''Colorize a fixed number (50) of tokens.
        If not done, queue this method again to continue coloring later.'''
        s,i = self.chunk_s,self.chunk_i
        prev,follow = self.prev_token,self.follow_token
        count = 0
        while i < len(s):
            count += 1
            # Exit only after finishing the row.  This reduces flash.
            if i == 0 or s[i-1] == '\n':
                if self.kill_chunk: return
                if count >= 50:
                    #@                << queue up this method >>
                    #@+node:ekr.20050601162452.1:<< queue up this method >>
                    self.chunk_s,self.chunk_i = s,i
                    self.prev_token,self.follow_token = prev,follow
                    self.c.frame.top.after_idle(self.colorOneChunk)
                    #@nonl
                    #@-node:ekr.20050601162452.1:<< queue up this method >>
                    #@nl
                    return
                #@            << remove all tags from this row >>
                #@+node:ekr.20050601162452:<< remove all tags from this row >>
                row,col = g.convertPythonIndexToRowCol(s,i)
                x1 = '%d.0' % (row+1) ; x2 = '%d.end' % (row+1)
                
                for tag in self.tags:
                    self.body.tag_remove(tag,x1,x2)
                
                for tag in self.color_tags_list:
                    self.body.tag_remove(tag,x1,x2)
                #@nonl
                #@-node:ekr.20050601162452:<< remove all tags from this row >>
                #@nl
            for f,kind,token_type in self.ruleMatchers:
                n = f(self,s,i)
                if n > 0:
                    self.doRule(s,i,i+n,kind,token_type)
                    i += n
                    break
            else:
                # g.trace('no match')
                i += 1
    #@-node:ekr.20050601105358:colorOneChunk
    #@+node:ekr.20050529143413.33:configure_tags
    def configure_tags (self):
        
        c = self.c
    
        for name in default_colors_dict.keys(): # Python 2.1 support.
            option_name,default_color = default_colors_dict[name]
            option_color = c.config.getColor(option_name)
            color = g.choose(option_color,option_color,default_color)
            # Must use foreground, not fg.
            try:
                self.body.tag_configure(name, foreground=color)
            except: # Recover after a user error.
                self.body.tag_configure(name, foreground=default_color)
        
        # underline=var doesn't seem to work.
        if 0: # self.use_hyperlinks: # Use the same coloring, even when hyperlinks are in effect.
            self.body.tag_configure("link",underline=1) # defined
            self.body.tag_configure("name",underline=0) # undefined
        else:
            self.body.tag_configure("link",underline=0)
            if self.underline_undefined:
                self.body.tag_configure("name",underline=1)
            else:
                self.body.tag_configure("name",underline=0)
                
        # Only create tags for whitespace when showing invisibles.
        if self.showInvisibles:
            for name,option_name,default_color in (
                ("blank","show_invisibles_space_background_color","Gray90"),
                ("tab",  "show_invisibles_tab_background_color",  "Gray80")):
                option_color = c.config.getColor(option_name)
                color = g.choose(option_color,option_color,default_color)
                try:
                    self.body.tag_configure(name,background=color)
                except: # Recover after a user error.
                    self.body.tag_configure(name,background=default_color)
            
        # Colors for latex characters.  Should be user options...
        
        if 1: # Alas, the selection doesn't show if a background color is specified.
            self.body.tag_configure("latexModeBackground",foreground="black")
            self.body.tag_configure("latexModeKeyword",foreground="blue")
            self.body.tag_configure("latexBackground",foreground="black")
            self.body.tag_configure("latexKeyword",foreground="blue")
        else: # Looks cool, and good for debugging.
            self.body.tag_configure("latexModeBackground",foreground="black",background="seashell1")
            self.body.tag_configure("latexModeKeyword",foreground="blue",background="seashell1")
            self.body.tag_configure("latexBackground",foreground="black",background="white")
            self.body.tag_configure("latexKeyword",foreground="blue",background="white")
            
        # Tags for wiki coloring.
        if self.showInvisibles:
            self.body.tag_configure("elide",background="yellow")
        else:
            self.body.tag_configure("elide",elide="1")
        self.body.tag_configure("bold",font=self.bold_font)
        self.body.tag_configure("italic",font=self.italic_font)
        self.body.tag_configure("bolditalic",font=self.bolditalic_font)
        for name in self.color_tags_list:
            self.body.tag_configure(name,foreground=name)
    #@nonl
    #@-node:ekr.20050529143413.33:configure_tags
    #@+node:ekr.20050601162452.3:doRule
    def doRule (self,s,i,j,kind,token_type):
        
        if kind == 'mark_following':
            pass
        
        elif kind == 'mark_previous':
            if 0: # This make no sense at all.
                if prev:
                    i2,j2,token_type2 = self.prev
                    g.trace('mark_previous',i2,j2,token_type2)
                    self.doColor(s,i2,j2,token_type) # Use the type specified in the mark_previous.
                    self.prev = None
        else:
            # g.trace('%3d %2d'%(i,j),state,repr(s[i:i+n]))
            self.doColor(s,i,j,token_type)
            self.prev = (i,j,token_type)
    #@nonl
    #@-node:ekr.20050601162452.3:doRule
    #@+node:ekr.20050529143413.32:init_ivars
    def init_ivars (self,p):
        
        c = self.c
        self.p = p
    
        # Add any newly-added user keywords.
        for d in g.globalDirectiveList:
            name = '@' + d
            if name not in leoKeywords:
                leoKeywords.append(name)
    
        # Get the body text, converted to unicode.
        s = self.body.getAllText()
        self.sel = sel = self.body.getInsertionPoint()
        start,end = self.body.convertIndexToRowColumn(sel)
        
        # g.trace(self.language)
        # g.trace(self.count,self.p)
        # g.trace(body.tag_names())
        
        if 0:
            if not self.incremental:
                self.removeAllTags()
                self.removeAllImages()
        
        self.redoColoring = False
        self.redoingColoring = False
        
        self.underline_undefined = c.config.getBool("underline_undefined_section_names")
        self.use_hyperlinks = c.config.getBool("use_hyperlinks")
        
        #@    << configure language-specific settings >>
        #@+node:ekr.20050529143413.34:<< configure language-specific settings >>
        # Define has_string, keywords, single_comment_start, block_comment_start, block_comment_end.
        
        if self.language == "cweb": # Use C comments, not cweb sentinel comments.
            delim1,delim2,delim3 = g.set_delims_from_language("c")
        elif self.comment_string:
            delim1,delim2,delim3 = g.set_delims_from_string(self.comment_string)
        elif self.language == "plain":
            delim1,delim2,delim3 = None,None,None
        else:
            delim1,delim2,delim3 = g.set_delims_from_language(self.language)
        
        self.single_comment_start = delim1
        self.block_comment_start = delim2
        self.block_comment_end = delim3
        
        # A strong case can be made for making this code as fast as possible.
        # Whether this is compatible with general language descriptions remains to be seen.
        self.case_sensitiveLanguage = self.language not in case_insensitiveLanguages
        self.has_string = self.language != "plain"
        if self.language == "plain":
            self.string_delims = ()
        elif self.language in ("elisp","html"):
            self.string_delims = ('"')
        else:
            self.string_delims = ("'",'"')
        self.has_pp_directives = self.language in ("c","csharp","cweb","latex")
        
        # The list of languages for which keywords exist.
        languages = [
            "actionscript","ada","c","csharp","css","cweb","elisp","forth","html","java","latex",
            "pascal","perl","perlpod","php","python","rapidq","rebol","shell","tcltk"]
        
        self.keywords = []
        if self.language == "cweb":
            for i in self.c_keywords:
                self.keywords.append(i)
            for i in self.cweb_keywords:
                self.keywords.append(i)
        else:
            for name in languages:
                if self.language==name: 
                    # g.trace("setting keywords for",name)
                    self.keywords = getattr(self, name + "_keywords")
        
        # For forth.
        self.nextForthWordIsNew = False
        
        if 1: # We color both kinds of references in cweb mode.
            self.lb = "<<"
            self.rb = ">>"
        else:
            self.lb = g.choose(self.language == "cweb","@<","<<")
            self.rb = g.choose(self.language == "cweb","@>",">>")
        #@nonl
        #@-node:ekr.20050529143413.34:<< configure language-specific settings >>
        #@nl
        
        self.hyperCount = 0 # Number of hypertext tags
        self.count += 1
        lines = string.split(s,'\n')
        
        # Color plain text unless we are under the control of @nocolor.
        state = self.setFirstLineState()
        self.word_chars = string.letters + '_'
        
        return s,lines,state
    #@nonl
    #@-node:ekr.20050529143413.32:init_ivars
    #@+node:ekr.20050529143413.42:recolor_all
    def recolor_all (self):
    
        # This code is executed only if graphics characters will be inserted by user markup code.
        
        # Pass 1:  Insert all graphics characters.
        self.removeAllImages()
        s = self.body.getAllText()
        lines = s.split('\n')
        
        self.color_pass = 1
        self.line_index = 1
        state = self.setFirstLineState()
        for s in lines:
            state = self.colorizeLine(s,state)
            self.line_index += 1
        
        # Pass 2: Insert one blank for each previously inserted graphic.
        self.color_pass = 2
        self.line_index = 1
        state = self.setFirstLineState()
        for s in lines:
            #@        << kludge: insert a blank in s for every image in the line >>
            #@+node:ekr.20050529143413.43:<< kludge: insert a blank in s for every image in the line >>
            #@+at 
            #@nonl
            # A spectacular kludge.
            # 
            # Images take up a real index, yet the get routine does not return 
            # any character for them!
            # In order to keep the colorer in synch, we must insert dummy 
            # blanks in s at the positions corresponding to each image.
            #@-at
            #@@c
            
            inserted = 0
            
            for photo,image,line_index,i in self.image_references:
                if self.line_index == line_index:
                    n = i+inserted ; 	inserted += 1
                    s = s[:n] + ' ' + s[n:]
            #@-node:ekr.20050529143413.43:<< kludge: insert a blank in s for every image in the line >>
            #@nl
            state = self.colorizeLine(s,state)
            self.line_index += 1
    #@nonl
    #@-node:ekr.20050529143413.42:recolor_all
    #@+node:ekr.20050529143413.91:setFirstLineState
    def setFirstLineState (self):
        
        if self.flag:
            if self.rootMode:
                state = g.choose(self.rootMode=="code","normal","doc")
            else:
                state = "normal"
        else:
            state = "nocolor"
    
        return state
    #@nonl
    #@-node:ekr.20050529143413.91:setFirstLineState
    #@-node:ekr.20050529150436:Colorizer code
    #@+node:ekr.20050601082256:To be removed...
    #@+node:ekr.20050529143413.36:color_incremental
    #@+at  
    #@nonl
    # Each line has a starting state.  The starting state for the first line 
    # is always "normal".
    # 
    # We need remember only self.lines and self.states between colorizing.  It 
    # is not necessary to know where the text comes from, only what the 
    # previous text was!  We must colorize everything when changing nodes, 
    # even if all lines match, because the context may be different.
    # 
    # We compute the range of lines to be recolored by comparing leading lines 
    # and trailing lines of old and new text.  All other lines (the middle 
    # lines) must be colorized, as well as any trailing lines whose states may 
    # have changed as the result of changes to the middle lines.
    #@-at
    #@@c
    
    def color_incremental (self,lines,state,leading,trailing):
    
        g.trace(state)
    
        # Make a copies of everything
        old_lines = self.lines[:]
        old_states = self.states[:]
        new_lines = lines[:]
        new_states = []
        
        new_len = len(new_lines)
        old_len = len(old_lines)
        
        if new_len == 0:
            self.states = []
            self.lines = []
            return
        
        # Must test against None.
        if leading != None and trailing != None:
            # print "leading,trailing:",leading,trailing
            leading_lines = leading
            trailing_lines = trailing
        else:
            #@        << compute leading, middle & trailing lines >>
            #@+node:ekr.20050529143413.37:<< compute leading, middle & trailing  lines >>
            #@+at 
            #@nonl
            # The leading lines are the leading matching lines.  The trailing 
            # lines are the trailing matching lines.  The middle lines are all 
            # other new lines.  We will color at least all the middle lines.  
            # There may be no middle lines if we delete lines.
            #@-at
            #@@c
            
            min_len = min(old_len,new_len)
            
            i = 0
            while i < min_len:
                if old_lines[i] != new_lines[i]:
                    break
                i += 1
            leading_lines = i
            
            if leading_lines == new_len:
                # All lines match, and we must color _everything_.
                # (several routine delete, then insert the text again,
                # deleting all tags in the process).
                # print "recolor all"
                leading_lines = trailing_lines = 0
            else:
                i = 0
                while i < min_len - leading_lines:
                    if old_lines[old_len-i-1] != new_lines[new_len-i-1]:
                        break
                    i += 1
                trailing_lines = i
            #@nonl
            #@-node:ekr.20050529143413.37:<< compute leading, middle & trailing  lines >>
            #@nl
            
        middle_lines = new_len - leading_lines - trailing_lines
        # print "middle lines", middle_lines
        
        #@    << clear leading_lines if middle lines involve @color or @recolor  >>
        #@+node:ekr.20050529143413.38:<< clear leading_lines if middle lines involve @color or @recolor  >>
        #@+at 
        #@nonl
        # 11/19/02: Changing @color or @nocolor directives requires we recolor 
        # all leading states as well.
        #@-at
        #@@c
        
        if trailing_lines == 0:
            m1 = new_lines[leading_lines:]
            m2 = old_lines[leading_lines:]
        else:
            m1 = new_lines[leading_lines:-trailing_lines]
            m2 = old_lines[leading_lines:-trailing_lines]
        m1.extend(m2) # m1 now contains all old and new middle lines.
        if m1:
            for s in m1:
                s = g.toUnicode(s,g.app.tkEncoding) # 10/28/03
                i = g.skip_ws(s,0)
                if g.match_word(s,i,"@color") or g.match_word(s,i,"@nocolor"):
                    leading_lines = 0
                    break
        #@-node:ekr.20050529143413.38:<< clear leading_lines if middle lines involve @color or @recolor  >>
        #@nl
        #@    << initialize new states >>
        #@+node:ekr.20050529143413.39:<< initialize new states >>
        # Copy the leading states from the old to the new lines.
        i = 0
        while i < leading_lines and i < old_len: # 12/8/02
            new_states.append(old_states[i])
            i += 1
            
        # We know the starting state of the first middle line!
        if middle_lines > 0 and i < old_len:
            new_states.append(old_states[i])
            i += 1
            
        # Set the state of all other middle lines to "unknown".
        first_trailing_line = max(0,new_len - trailing_lines)
        while i < first_trailing_line:
            new_states.append("unknown")
            i += 1
        
        # Copy the trailing states from the old to the new lines.
        i = max(0,old_len - trailing_lines)
        while i < old_len and i < len(old_states):
            new_states.append(old_states[i])
            i += 1
        
        # Complete new_states by brute force.
        while len(new_states) < new_len:
            new_states.append("unknown")
        #@nonl
        #@-node:ekr.20050529143413.39:<< initialize new states >>
        #@nl
        #@    << colorize until the states match >>
        #@+node:ekr.20050529143413.40:<< colorize until the states match >>
        # All middle lines have "unknown" state, so they will all be colored.
        
        # Start in the state _after_ the last leading line, which may be unknown.
        i = leading_lines
        while i > 0:
            if i < old_len and i < new_len:
                state = new_states[i]
                # assert(state!="unknown") # This can fail.
                break
            else:
                i -= 1
        
        if i == 0:
            # Color plain text unless we are under the control of @nocolor.
            # state = g.choose(self.flag,"normal","nocolor")
            state = self.setFirstLineState()
            new_states[0] = state
        
        # The new_states[] will be "unknown" unless the lines match,
        # so we do not need to compare lines here.
        while i < new_len:
            self.line_index = i + 1
            state = self.colorizeLine(new_lines[i],state)
            i += 1
            # Set the state of the _next_ line.
            if i < new_len and state != new_states[i]:
                new_states[i] = state
            else: break
            
        # Update the ivars
        self.states = new_states
        self.lines = new_lines
        #@nonl
        #@-node:ekr.20050529143413.40:<< colorize until the states match >>
        #@nl
    #@nonl
    #@-node:ekr.20050529143413.36:color_incremental
    #@+node:ekr.20050529143413.41:color_nonincremental
    def color_nonincremental (self,lines,state):
        
        self.line_index = 1 # The Tk line number for indices, as in n.i
    
        for s in lines:
            state = self.colorizeLine(s,state)
            self.line_index += 1
    #@nonl
    #@-node:ekr.20050529143413.41:color_nonincremental
    #@+node:ekr.20050529143413.46:colorizeLine & allies
    def colorizeLine (self,s,state):
    
        # g.trace('line,inc,state,s:',self.line_index,self.incremental,state,s)
        s = g.toUnicode(s,g.app.tkEncoding)
    
        if self.incremental:
            self.removeTagsFromLine()
    
        i = 0
        while i < len(s):
            self.progress = i
            func = self.state_dict[state]
            i,state = func(s,i)
    
        return state
    #@nonl
    #@-node:ekr.20050529143413.46:colorizeLine & allies
    #@+node:ekr.20050529145355:Language-specific utils: (to be removed)
    #@+node:ekr.20050529143413.85:getCwebWord
    def getCwebWord (self,s,i):
        
        # g.trace(g.get_line(s,i))
        if not g.match(s,i,"@"):
            return None
        
        ch1 = ch2 = word = None
        if i + 1 < len(s): ch1 = s[i+1]
        if i + 2 < len(s): ch2 = s[i+2]
    
        if g.match(s,i,"@**"):
            word = "@**"
        elif not ch1:
            word = "@"
        elif not ch2:
            word = s[i:i+2]
        elif (
            (ch1 in string.ascii_letters and not ch2 in string.ascii_letters) or # single-letter control code
            ch1 not in string.ascii_letters # non-letter control code
        ):
            word = s[i:i+2]
    
        # if word: g.trace(word)
            
        return word
    #@nonl
    #@-node:ekr.20050529143413.85:getCwebWord
    #@+node:ekr.20050529143413.92:skip_id
    def skip_id(self,s,i,chars=None):
    
        n = len(s)
        while i < n:
            ch = s[i]
            if ch in string.ascii_letters or ch in string.digits or ch == '_':
                i += 1
            elif chars and ch in chars:
                i += 1
            else: break
        return i
    #@-node:ekr.20050529143413.92:skip_id
    #@+node:ekr.20050529143413.94:skip_string
    def skip_string(self,s,i):
        
        """Skip a string literal."""
    
        allow_newlines = self.language == "elisp"
        delim = s[i] ; i += 1
        continue_state = g.choose(delim=="'","singleString","doubleString")
        assert(delim == '"' or delim == "'")
        n = len(s)
        while i < n and s[i] != delim and (allow_newlines or not s[i] == '\n'): # 6/3/04: newline ends most strings.
            if s[i:] == "\\": # virtual trailing newline.
                return n,continue_state
            elif s[i] == '\\': i += 2
            else: i += 1
    
        if i >= n:
            return n, g.choose(allow_newlines,continue_state,"normal")
        if s[i] == delim:
            i += 1
        return i,"normal"
    #@nonl
    #@-node:ekr.20050529143413.94:skip_string
    #@+node:ekr.20050529143413.93:skip_python_string
    def skip_python_string(self,s,i):
    
        delim = s[i:i+3]
        if delim == "'''" or delim == '"""':
            k = s.find(delim,i+3)
            if k == -1:
                return len(s),g.choose(delim=="'''","string3s","string3d")
            else:
                return k+3, "normal"
        else:
            return self.skip_string(s,i)
    #@nonl
    #@-node:ekr.20050529143413.93:skip_python_string
    #@-node:ekr.20050529145355:Language-specific utils: (to be removed)
    #@+node:ekr.20050529180421.46:Helpers for colorizerLine (to be deleted)
    #@+node:ekr.20050529143413.47:continueBlockComment
    def continueBlockComment (self,s,i):
        
        j = s.find(self.block_comment_end,i)
    
        if j == -1:
            j = len(s) # The entire line is part of the block comment.
            if self.language=="cweb":
                self.doLatexLine(s,i,j)
            else:
                if not g.doHook("color-optional-markup",
                    colorer=self,p=self.p,v=self.p,s=s,i=i,j=j,colortag="comment"):
                    self.tag("comment",i,j)
            return j,"blockComment" # skip the rest of the line.
    
        else:
            # End the block comment.
            k = len(self.block_comment_end)
            if self.language=="cweb" and self.latex_cweb_comments:
                self.doLatexLine(s,i,j)
                self.tag("comment",j,j+k)
            else:
                if not g.doHook("color-optional-markup",
                    colorer=self,p=self.p,v=self.p,s=s,i=i,j=j+k,colortag="comment"):
                    self.tag("comment",i,j+k)
            i = j + k
            return i,"normal"
    #@nonl
    #@-node:ekr.20050529143413.47:continueBlockComment
    #@+node:ekr.20050529143413.48:continueSingle/DoubleString
    def continueDoubleString (self,s,i):
        return self.continueString(s,i,'"',"doubleString")
        
    def continueSingleString (self,s,i):
        return self.continueString(s,i,"'","singleString")
    
    # Similar to skip_string.
    def continueString (self,s,i,delim,continueState):
        # g.trace(delim + s[i:])
        continueFlag = g.choose(self.language in ("elisp","html"),True,False)
        j = i
        while i < len(s) and s[i] != delim:
            if s[i:] == "\\":
                i = len(s) ; continueFlag = True ; break
            elif s[i] == "\\":
                i += 2
            else:
                i += 1
        if i >= len(s):
            i = len(s)
        elif s[i] == delim:
            i += 1 ; continueFlag = False
        self.tag("string",j,i)
        state = g.choose(continueFlag,continueState,"normal")
        return i,state
    #@nonl
    #@-node:ekr.20050529143413.48:continueSingle/DoubleString
    #@+node:ekr.20050529143413.49:continueDocPart
    def continueDocPart (self,s,i):
        
        state = "doc"
        if self.language == "cweb":
            #@        << handle cweb doc part >>
            #@+node:ekr.20050529143413.50:<< handle cweb doc part >>
            word = self.getCwebWord(s,i)
            if word and len(word) > 0:
                j = i + len(word)
                if word in ("@<","@(","@c","@d","@f","@p"):
                    state = "normal" # end the doc part and rescan
                else:
                    # The control code does not end the doc part.
                    self.tag("keyword",i,j)
                    i = j
                    if word in ("@^","@.","@:","@="): # Ended by "@>"
                        j = s.find("@>",i)
                        if j > -1:
                            self.tag("cwebName",i,j)
                            self.tag("nameBrackets",j,j+2)
                            i = j + 2
            elif g.match(s,i,self.lb):
                j = self.doNowebSecRef(s,i)
                if j == i + 2: # not a section ref.
                    self.tag("docPart",i,j)
                i = j
            elif self.latex_cweb_docs:
                # Everything up to the next "@" is latex colored.
                j = s.find("@",i+1)
                if j == -1: j = len(s)
                self.doLatexLine(s,i,j)
                i = j
            else:
                # Everthing up to the next "@" is in the doc part.
                j = s.find("@",i+1)
                if j == -1: j = len(s)
                self.tag("docPart",i,j)
                i = j
            #@nonl
            #@-node:ekr.20050529143413.50:<< handle cweb doc part >>
            #@nl
        else:
            #@        << handle noweb doc part >>
            #@+node:ekr.20050529143413.51:<< handle noweb doc part >>
            if i == 0 and g.match(s,i,"<<"):
                # Possible section definition line.
                return i,"normal" # rescan the line.
            
            if i == 0 and s[i] == '@':
                j = self.skip_id(s,i+1,chars='-')
                word = s[i:j]
                word = word.lower()
            else:
                word = ""
                
            if word in ["@c","@code","@unit","@root","@root-code","@root-doc","@color","@nocolor"]:
                # End of the doc part.
                self.body.tag_remove("docPart",self.index(i),self.index(j)) # 10/27/03
                self.tag("leoKeyword",i,j)
                state = "normal"
                if word != '@nocolor': i = j # 3/8/05: Rescan @nocolor.
            else:
                # The entire line is in the doc part.
                j = len(s)
                if not g.doHook("color-optional-markup",
                    colorer=self,p=self.p,v=self.p,s=s,i=i,j=j,colortag="docPart"):
                    self.tag("docPart",i,j)
                i = j # skip the rest of the line.
            #@-node:ekr.20050529143413.51:<< handle noweb doc part >>
            #@nl
        return i,state
    #@nonl
    #@-node:ekr.20050529143413.49:continueDocPart
    #@+node:ekr.20050529143413.52:continueNocolor
    def continueNocolor (self,s,i):
    
        if i == 0 and s[i] == '@':
            j = self.skip_id(s,i+1)
            word = s[i:j]
            word = word.lower()
        else:
            word = ""
        
        if word == "@color" and self.language != "plain":
            # End of the nocolor part.
            self.tag("leoKeyword",0,j)
            return i,"normal"
        else:
            # The entire line is in the nocolor part.
            # Add tags for blanks and tabs to make "Show Invisibles" work.
            for ch in s[i:]:
                if ch == ' ':
                    self.tag("blank",i,i+1)
                elif ch == '\t':
                    self.tag("tab",i,i+1)
                i += 1
            return i,"nocolor"
    #@nonl
    #@-node:ekr.20050529143413.52:continueNocolor
    #@+node:ekr.20050529143413.53:continueSingle/DoublePythonString
    def continueDoublePythonString (self,s,i):
        j = s.find('"""',i)
        return self.continuePythonString(s,i,j,"string3d")
    
    def continueSinglePythonString (self,s,i):
        j = s.find("'''",i)
        return self.continuePythonString(s,i,j,"string3s")
    
    def continuePythonString (self,s,i,j,continueState):
    
        if j == -1: # The entire line is part of the triple-quoted string.
            j = len(s)
            if continueState == "string3d":
                if not g.doHook("color-optional-markup",
                    colorer=self,p=self.p,v=self.p,s=s,i=i,j=j,colortag="string"):
                    self.tag("string",i,j)
            else:
                self.tag("string",i,j)
            return j,continueState # skip the rest of the line.
    
        else: # End the string
            if continueState == "string3d":
                if not g.doHook("color-optional-markup",
                    colorer=self,p=self.p,v=self.p,s=s,i=i,j=j,colortag="string"):
                    self.tag("string",i,j+3)
                else:
                    self.tag("string",i,j+3)
            else:
                self.tag("string",i,j+3)
            return j+3,"normal"
    #@nonl
    #@-node:ekr.20050529143413.53:continueSingle/DoublePythonString
    #@+node:ekr.20050529143413.54:doAtKeyword: NOT for cweb keywords
    # Handles non-cweb keyword.
    
    def doAtKeyword (self,s,i):
    
        j = self.skip_id(s,i+1,chars="-") # to handle @root-code, @root-doc
        word = s[i:j]
        word = word.lower()
        if i != 0 and word not in ("@others","@all"):
            word = "" # can't be a Leo keyword, even if it looks like it.
        
        # 7/8/02: don't color doc parts in plain text.
        if self.language != "plain" and (word == "@" or word == "@doc"):
            # at-space is a Leo keyword.
            self.tag("leoKeyword",i,j)
            k = len(s) # Everything on the line is in the doc part.
            if not g.doHook("color-optional-markup",
                colorer=self,p=self.p,v=self.p,s=s,i=j,j=k,colortag="docPart"):
                self.tag("docPart",j,k)
            return k,"doc"
        elif word == "@nocolor":
            # Nothing on the line is colored.
            self.tag("leoKeyword",i,j)
            return j,"nocolor"
        elif word in leoKeywords:
            self.tag("leoKeyword",i,j)
            return j,"normal"
        else:
            return j,"normal"
    #@nonl
    #@-node:ekr.20050529143413.54:doAtKeyword: NOT for cweb keywords
    #@+node:ekr.20050529143413.55:doLatexLine
    # Colorize the line from i to j.
    
    def doLatexLine (self,s,i,j):
    
        while i < j:
            if g.match(s,i,"\\"):
                k = self.skip_id(s,i+1)
                word = s[i:k]
                if word in self.latex_keywords:
                    self.tag("latexModeKeyword",i,k)
                i = k
            else:
                self.tag("latexModeBackground",i,i+1)
                i += 1
    #@nonl
    #@-node:ekr.20050529143413.55:doLatexLine
    #@+node:ekr.20050529143413.56:doNormalState
    ## To do: rewrite using dynamically generated tables.
    
    def doNormalState (self,s,i):
        
        __pychecker__ = 'maxlines=500'
    
        ch = s[i] ; state = "normal"
        assert(type(ch)==type(u""))
    
        if ch in string.ascii_letters or ch == '_' or (
            (ch == '\\' and self.language=="latex") or
            (ch in '/&<>' and self.language=="html") or
            (ch == '$' and self.language=="rapidq") or
            (self.language == 'forth' and ch in "`~!@#$%^&*()_+-={}|[];':\",./<>?")
        ):
            #@        << handle possible keyword >>
            #@+middle:ekr.20050529143413.57:Valid regardless of latex mode
            #@+node:ekr.20050529143413.58:<< handle possible  keyword >>
            if self.language == "latex":
                #@    << handle possible latex keyword >>
                #@+node:ekr.20050529143413.59:<< handle possible latex keyword >>
                if g.match(s,i,"\\"):
                    if i + 1 < len(s) and s[i+1] in self.latex_special_keyword_characters:
                        j = i + 2 # A special 2-character LaTex keyword.
                    else:
                        j = self.skip_id(s,i+1)
                    word = s[i:j]
                    if word in self.latex_keywords:
                        self.tag("latexKeyword",i,j)
                    else:
                        self.tag("latexBackground",i,j)
                else:
                    self.tag("latexBackground",i,i+1)
                    j = i + 1 # skip the character.
                #@nonl
                #@-node:ekr.20050529143413.59:<< handle possible latex keyword >>
                #@nl
            elif self.language == "html":
                #@    << handle possible html keyword >>
                #@+node:ekr.20050529143413.60:<< handle possible html keyword >>
                if g.match(s,i,"<!---") or g.match(s,i,"<!--"):
                    if g.match(s,i,"<!---"): k = 5
                    else: k = 4
                    self.tag("comment",i,i+k)
                    j = i + k ; state = "blockComment"
                elif g.match(s,i,"<"):
                    if g.match(s,i,"</"): k = 2
                    else: k = 1
                    j = self.skip_id(s,i+k)
                    self.tag("keyword",i,j)
                elif g.match(s,i,"&"):
                    j = self.skip_id(s,i+1,';')
                    self.tag("keyword",i,j)
                elif g.match(s,i,"/>"):
                    j = i + 2
                    self.tag("keyword",i,j)
                elif g.match(s,i,">"):
                    j = i + 1
                    self.tag("keyword",i,j)
                else:
                    j = i + 1
                #@-node:ekr.20050529143413.60:<< handle possible html keyword >>
                #@nl
            elif self.language == "forth":
                #@    << handle possible forth keyword >>
                #@+node:ekr.20050529143413.62:<< handle possible forth keyword >>
                j = self.skip_id(s,i+1,chars="`~!@#$%^&*()-_=+[]{};:'\\\",./<>?")
                word = s[i:j]
                
                #print "word=%s" % repr(word)
                
                if not self.case_sensitiveLanguage:
                    word = word.lower()
                
                if self.nextForthWordIsNew:
                    #print "trying to bold the defined word '%s'" % word
                    self.tag("bold", i, j)
                    self.nextForthWordIsNew = False
                else:
                    if word in self.forth_definingwords:
                        self.nextForthWordIsNew = True
                    
                    if word in self.forth_boldwords:
                        self.tag("bold", i, j)
                    elif word in self.forth_bolditalicwords:
                        self.tag("bolditalic", i, j)
                    elif word in self.forth_italicwords:
                        self.tag("italic", i, j)
                    elif word in self.forth_stringwords:
                        self.tag("keyword", i, j-1)
                        i = j - 1
                        j, state = self.skip_string(s,j-1)
                        self.tag("string",i,j)
                        word = ''
                    elif word in self.keywords:
                        self.tag("keyword",i,j)
                #@nonl
                #@-node:ekr.20050529143413.62:<< handle possible forth keyword >>
                #@nl
            else:
                #@    << handle general keyword >>
                #@+node:ekr.20050529143413.61:<< handle general keyword >>
                if self.language == "rapidq":
                    j = self.skip_id(s,i+1,chars="$")
                elif self.language == "rebol":
                    j = self.skip_id(s,i+1,chars="-~!?")
                elif self.language in ("elisp","css"):
                    j = self.skip_id(s,i+1,chars="-")
                else:
                    j = self.skip_id(s,i)
                
                word = s[i:j]
                if not self.case_sensitiveLanguage:
                    word = word.lower()
                
                if word in self.keywords:
                    self.tag("keyword",i,j)
                elif self.language == "php":
                    if word in self.php_paren_keywords and g.match(s,j,"()"):
                        self.tag("keyword",i,j+2)
                        j += 2
                #@nonl
                #@-node:ekr.20050529143413.61:<< handle general keyword >>
                #@nl
            i = j
            #@nonl
            #@-node:ekr.20050529143413.58:<< handle possible  keyword >>
            #@-middle:ekr.20050529143413.57:Valid regardless of latex mode
            #@nl
        elif g.match(s,i,self.lb):
            i = self.doNowebSecRef(s,i)
        elif ch == '@':
            #@        << handle at keyword >>
            #@+middle:ekr.20050529143413.57:Valid regardless of latex mode
            #@+node:ekr.20050529143413.63:<< handle at keyword >>
            if self.language == "cweb":
                if g.match(s,i,"@(") or g.match(s,i,"@<"):
                    #@        << handle cweb ref or def >>
                    #@+node:ekr.20050529143413.64:<< handle cweb ref or def >>
                    self.tag("nameBrackets",i,i+2)
                    
                    # See if the line contains the right name bracket.
                    j = s.find("@>=",i+2)
                    k = g.choose(j==-1,2,3)
                    if j == -1:
                        j = s.find("@>",i+2)
                    
                    if j == -1:
                        i += 2
                    else:
                        self.tag("cwebName",i+2,j)
                        self.tag("nameBrackets",j,j+k)
                        i = j + k
                    #@-node:ekr.20050529143413.64:<< handle cweb ref or def >>
                    #@nl
                else:
                    word = self.getCwebWord(s,i)
                    if word:
                        #@            << Handle cweb control word >>
                        #@+node:ekr.20050529143413.65:<< Handle cweb control word >>
                        # Color and skip the word.
                        assert(self.language=="cweb")
                        
                        j = i + len(word)
                        self.tag("keyword",i,j)
                        i = j
                        
                        if word in ("@ ","@\t","@\n","@*","@**"):
                            state = "doc"
                        elif word in ("@<","@(","@c","@d","@f","@p"):
                            state = "normal"
                        elif word in ("@^","@.","@:","@="): # Ended by "@>"
                            j = s.find("@>",i)
                            if j > -1:
                                self.tag("cwebName",i,j)
                                self.tag("nameBrackets",j,j+2)
                                i = j + 2
                        #@nonl
                        #@-node:ekr.20050529143413.65:<< Handle cweb control word >>
                        #@nl
                    else:
                        i,state = self.doAtKeyword(s,i)
            else:
                i,state = self.doAtKeyword(s,i)
            #@nonl
            #@-node:ekr.20050529143413.63:<< handle at keyword >>
            #@-middle:ekr.20050529143413.57:Valid regardless of latex mode
            #@nl
        elif g.match(s,i,self.single_comment_start):
            #@        << handle single-line comment >>
            #@+middle:ekr.20050529143413.57:Valid regardless of latex mode
            #@+node:ekr.20050529143413.66:<< handle single-line comment >>
            # print "single-line comment i,s:",i,s
            
            if self.language == "cweb" and self.latex_cweb_comments:
                j = i + len(self.single_comment_start)
                self.tag("comment",i,j)
                self.doLatexLine(s,j,len(s))
                i = len(s)
            elif self.language == "shell" and (i>0 and s[i-1]=='$'):
                i += 1 # '$#' in shell should not start a comment (DS 040113)
            else:
                j = len(s)
                if not g.doHook("color-optional-markup",
                    colorer=self,p=self.p,v=self.p,s=s,i=i,j=j,colortag="comment"):
                    self.tag("comment",i,j)
                i = j
            #@nonl
            #@-node:ekr.20050529143413.66:<< handle single-line comment >>
            #@-middle:ekr.20050529143413.57:Valid regardless of latex mode
            #@nl
        elif g.match(s,i,self.block_comment_start):
            #@        << start block comment >>
            #@+middle:ekr.20050529143413.57:Valid regardless of latex mode
            #@+node:ekr.20050529143413.67:<< start block comment >>
            k = len(self.block_comment_start)
            
            if not g.doHook("color-optional-markup",
                colorer=self,p=self.p,v=self.p,s=s,i=i,j=i+k,colortag="comment"):
                self.tag("comment",i,i+k)
            
            i += k ; state = "blockComment"
            #@nonl
            #@-node:ekr.20050529143413.67:<< start block comment >>
            #@-middle:ekr.20050529143413.57:Valid regardless of latex mode
            #@nl
        elif ch == '%' and self.language=="cweb":
            #@        << handle latex line >>
            #@+middle:ekr.20050529143413.57:Valid regardless of latex mode
            #@+node:ekr.20050529143413.68:<< handle latex line >>
            self.tag("keyword",i,i+1)
            i += 1 # Skip the %
            self.doLatexLine(s,i,len(s))
            i = len(s)
            #@nonl
            #@-node:ekr.20050529143413.68:<< handle latex line >>
            #@-middle:ekr.20050529143413.57:Valid regardless of latex mode
            #@nl
        elif self.language=="latex":
            #@        << handle latex normal character >>
            #@+middle:ekr.20050529143413.69:Vaid only in latex mode
            #@+node:ekr.20050529143413.70:<< handle latex normal character >>
            if self.language=="cweb":
                self.tag("latexModeBackground",i,i+1)
            else:
                self.tag("latexBackground",i,i+1)
            i += 1
            #@nonl
            #@-node:ekr.20050529143413.70:<< handle latex normal character >>
            #@-middle:ekr.20050529143413.69:Vaid only in latex mode
            #@nl
        # ---- From here on self.language != "latex" -----
        elif ch in self.string_delims:
            #@        << handle string >>
            #@+middle:ekr.20050529143413.71:Valid when not in latex_mode
            #@+node:ekr.20050529143413.72:<< handle string >>
            # g.trace(self.language)
            
            if self.language == "python":
            
                delim = s[i:i+3]
                j, state = self.skip_python_string(s,i)
                if delim == '"""':
                    # Only handle wiki items in """ strings.
                    if not g.doHook("color-optional-markup",
                        colorer=self,p=self.p,v=self.p,s=s,i=i,j=j,colortag="string"):
                        self.tag("string",i,j)
                else:
                    self.tag("string",i,j)
                i = j
            
            else:
                j, state = self.skip_string(s,i)
                self.tag("string",i,j)
                i = j
            #@-node:ekr.20050529143413.72:<< handle string >>
            #@-middle:ekr.20050529143413.71:Valid when not in latex_mode
            #@nl
        elif ch == '#' and self.has_pp_directives:
            #@        << handle C preprocessor line >>
            #@+middle:ekr.20050529143413.71:Valid when not in latex_mode
            #@+node:ekr.20050529143413.73:<< handle C preprocessor line >>
            # 10/17/02: recognize comments in preprocessor lines.
            j = i
            while i < len(s):
                if g.match(s,i,self.single_comment_start) or g.match(s,i,self.block_comment_start):
                    break
                else: i += 1
            
            self.tag("pp",j,i)
            #@nonl
            #@-node:ekr.20050529143413.73:<< handle C preprocessor line >>
            #@-middle:ekr.20050529143413.71:Valid when not in latex_mode
            #@nl
        elif self.language == "php" and (g.match(s,i,"<") or g.match(s,i,"?")):
            # g.trace("%3d" % i,php_re.match(s,i),s)
            #@        << handle special php keywords >>
            #@+middle:ekr.20050529143413.71:Valid when not in latex_mode
            #@+node:ekr.20050529143413.74:<< handle special php keywords >>
            if g.match(s.lower(),i,"<?php"):
                self.tag("keyword",i,i+5)
                i += 5
            elif g.match(s,i,"?>"):
                self.tag("keyword",i,i+2)
                i += 2
            else:
                i += 1
            
            #@-node:ekr.20050529143413.74:<< handle special php keywords >>
            #@-middle:ekr.20050529143413.71:Valid when not in latex_mode
            #@nl
        elif ch == ' ':
            #@        << handle blank >>
            #@+middle:ekr.20050529143413.71:Valid when not in latex_mode
            #@+node:ekr.20050529143413.75:<< handle blank >>
            if self.showInvisibles:
                self.tag("blank",i,i+1)
            i += 1
            #@nonl
            #@-node:ekr.20050529143413.75:<< handle blank >>
            #@-middle:ekr.20050529143413.71:Valid when not in latex_mode
            #@nl
        elif ch == '\t':
            #@        << handle tab >>
            #@+middle:ekr.20050529143413.71:Valid when not in latex_mode
            #@+node:ekr.20050529143413.76:<< handle tab >>
            if self.showInvisibles:
                self.tag("tab",i,i+1)
            i += 1
            #@nonl
            #@-node:ekr.20050529143413.76:<< handle tab >>
            #@-middle:ekr.20050529143413.71:Valid when not in latex_mode
            #@nl
        else:
            #@        << handle normal character >>
            #@+middle:ekr.20050529143413.71:Valid when not in latex_mode
            #@+node:ekr.20050529143413.77:<< handle normal character >>
            # self.tag("normal",i,i+1)
            i += 1
            #@nonl
            #@-node:ekr.20050529143413.77:<< handle normal character >>
            #@-middle:ekr.20050529143413.71:Valid when not in latex_mode
            #@nl
    
        if 0: # This can fail harmlessly when using wxPython plugin.  Don't know exactly why.
            g.trace(self.progress,i,state)
            assert(self.progress < i)
        return i,state
    #@nonl
    #@+node:ekr.20050529143413.57:Valid regardless of latex mode
    #@-node:ekr.20050529143413.57:Valid regardless of latex mode
    #@+node:ekr.20050529143413.69:Vaid only in latex mode
    #@-node:ekr.20050529143413.69:Vaid only in latex mode
    #@+node:ekr.20050529143413.71:Valid when not in latex_mode
    #@-node:ekr.20050529143413.71:Valid when not in latex_mode
    #@-node:ekr.20050529143413.56:doNormalState
    #@+node:ekr.20050529143413.78:doNowebSecRef
    def doNowebSecRef (self,s,i):
    
        self.tag("nameBrackets",i,i+2)
        
        # See if the line contains the right name bracket.
        j = s.find(self.rb+"=",i+2)
        k = g.choose(j==-1,2,3)
        if j == -1:
            j = s.find(self.rb,i+2)
        if j == -1:
            return i + 2
        else:
            searchName = self.body.getTextRange(self.index(i),self.index(j+k)) # includes brackets
            ref = g.findReference(searchName,self.p)
            if ref:
                self.tag("link",i+2,j)
                if self.use_hyperlinks:
                    #@                << set the hyperlink >>
                    #@+node:ekr.20050529143413.79:<< set the hyperlink >>
                    # Set the bindings to vnode callbacks.
                    # Create the tag.
                    # Create the tag name.
                    tagName = "hyper" + str(self.hyperCount)
                    self.hyperCount += 1
                    self.body.tag_delete(tagName)
                    self.tag(tagName,i+2,j)
                    
                    ref.tagName = tagName
                    self.body.tag_bind(tagName,"<Control-1>",ref.OnHyperLinkControlClick)
                    self.body.tag_bind(tagName,"<Any-Enter>",ref.OnHyperLinkEnter)
                    self.body.tag_bind(tagName,"<Any-Leave>",ref.OnHyperLinkLeave)
                    #@nonl
                    #@-node:ekr.20050529143413.79:<< set the hyperlink >>
                    #@nl
            elif k == 3: # a section definition
                self.tag("link",i+2,j)
            else:
                self.tag("name",i+2,j)
            self.tag("nameBrackets",j,j+k)
            return j + k
    #@nonl
    #@-node:ekr.20050529143413.78:doNowebSecRef
    #@-node:ekr.20050529180421.46:Helpers for colorizerLine (to be deleted)
    #@-node:ekr.20050601082256:To be removed...
    #@+node:ekr.20050529143413.89:Utils
    #@+at 
    #@nonl
    # These methods are like the corresponding functions in leoGlobals.py 
    # except they issue no error messages.
    #@-at
    #@+node:ekr.20050529143413.80:removeAllTags & removeTagsFromLines
    def removeAllTags (self):
        
        # Warning: the following DOES NOT WORK: self.body.tag_delete(self.tags)
        for tag in self.tags:
            self.body.tag_delete(tag)
    
        for tag in self.color_tags_list:
            self.body.tag_delete(tag)
        
    def removeTagsFromLine (self):
        
        # print "removeTagsFromLine",self.line_index
        for tag in self.tags:
            self.body.tag_remove(tag,self.index(0),self.index("end"))
            
        for tag in self.color_tags_list:
            self.body.tag_remove(tag,self.index(0),self.index("end"))
    #@nonl
    #@-node:ekr.20050529143413.80:removeAllTags & removeTagsFromLines
    #@+node:ekr.20050529143413.90:index & tag
    def index (self,i):
        
        return self.body.convertRowColumnToIndex(self.line_index,i)
            
    def tag (self,name,i,j):
    
        self.body.tag_add(name,self.index(i),self.index(j))
    #@nonl
    #@-node:ekr.20050529143413.90:index & tag
    #@+node:ekr.20050529143413.86:removeAllImages
    def removeAllImages (self):
        
        for photo,image,line_index,i in self.image_references:
            try:
                self.body.deleteCharacter(image) # 10/27/03
            except:
                pass # The image may have been deleted earlier.
        
        self.image_references = []
    #@nonl
    #@-node:ekr.20050529143413.86:removeAllImages
    #@+node:ekr.20050529143413.29:setFontFromConfig
    def setFontFromConfig (self):
        
        c = self.c
        
        self.bold_font = c.config.getFontFromParams(
            "body_text_font_family", "body_text_font_size",
            "body_text_font_slant",  "body_text_font_weight",
            c.config.defaultBodyFontSize, tag = "colorer bold")
        
        if self.bold_font:
            self.bold_font.configure(weight="bold")
        
        self.italic_font = c.config.getFontFromParams(
            "body_text_font_family", "body_text_font_size",
            "body_text_font_slant",  "body_text_font_weight",
            c.config.defaultBodyFontSize, tag = "colorer italic")
            
        if self.italic_font:
            self.italic_font.configure(slant="italic",weight="normal")
        
        self.bolditalic_font = c.config.getFontFromParams(
            "body_text_font_family", "body_text_font_size",
            "body_text_font_slant",  "body_text_font_weight",
            c.config.defaultBodyFontSize, tag = "colorer bold italic")
            
        if self.bolditalic_font:
            self.bolditalic_font.configure(weight="bold",slant="italic")
            
        self.color_tags_list = []
        self.image_references = []
    #@nonl
    #@-node:ekr.20050529143413.29:setFontFromConfig
    #@+node:ekr.20050601044345:get_word (new)
    def get_word(self,s,i):
    
        j = i
        while j < len(s) and s[j] in self.word_chars:
            j += 1
            
        # g.trace(s[i:j])
        return s[i:j]
    #@-node:ekr.20050601044345:get_word (new)
    #@+node:ekr.20050601065451:doColor
    def doColor(self,s,i,j,token_type):
    
        d = {
            'seq': None,
            'literal1': 'string',
            'literal2': 'string',
            'keyword-n': 'keyword',
            'comment1': 'comment',
            'operator': None,
            # 'function': 'comment', # just for testing.
        }
        
        tag = d.get(token_type)
    
        if tag:
            row,col = g.convertPythonIndexToRowCol(s,i)
            x1 = '%d.%d' % (row+1,col)
            row,col = g.convertPythonIndexToRowCol(s,j)
            x2 = '%d.%d' % (row+1,col)
            self.body.tag_add(tag,x1,x2)
    #@nonl
    #@-node:ekr.20050601065451:doColor
    #@-node:ekr.20050529143413.89:Utils
    #@+node:ekr.20050530065723.47:parse_jEdit_file
    def parse_jEdit_file(self,fileName,verbose=False):
        
        if not fileName.endswith('.xml'):
            fileName = fileName + '.xml'
    
        path = os.path.join(g.app.loadDir,'../','modes',fileName)
        path = os.path.normpath(path)
        
        try: f = open(path)
        except IOError: return None
    
        try:
            try:
                parser = xml.sax.make_parser()
                handler = contentHandler(self.c,fileName,verbose=verbose)
                parser.setContentHandler(handler)
                parser.parse(f)
                if verbose: handler.printSummary()
                modes = handler.getModes()
            except Exception:
                g.es('unexpected exception parsing %s' % (languageName),color='red')
                g.es_exception()
                return None
        finally:
            f.close()
            return modes
    #@nonl
    #@-node:ekr.20050530065723.47:parse_jEdit_file
    #@+node:ekr.20050529180421.47:Rule matching methods
    #@+node:ekr.20050530112849:createRuleMatchers
    def createRuleMatchers (self,rules):
        
        ruleNumber = 0 ; result = []
        for rule in rules:
            result.append(self.createRuleMatcher(rule,ruleNumber))
            ruleNumber += 1
        return result
        
        # return [self.createRuleMatcher(rule) for rule in rules]
    #@nonl
    #@-node:ekr.20050530112849:createRuleMatchers
    #@+node:ekr.20050530112849.1:createRuleMatcher
    def createRuleMatcher (self,rule,ruleNumber):
        
        name = rule.name ; d = rule.attributes or {}
        token_type    = d.get('type','<no type>').lower()
        at_line_start = d.get('at_line_start',False)
        at_ws_end     = d.get('at_ws_end',False)
        at_word_start = d.get('at_word_start',False)
        d2 = rule.get('contents',{})
        seq     = d2.get(name,'')
        begin   = d2.get('begin','')
        end     = d2.get('end','')
        
        if name == 'eol_span':
            def f(self,s,i,seq=seq,at_line_start=at_line_start,at_ws_end=at_ws_end,at_word_start=at_word_start):
                return self.match_eol_span(s,i,seq,at_line_start,at_ws_end,at_word_start)
        elif name == 'eol_span_regexp':
            def f(self,s,i,seq=seq,at_line_start=at_line_start,at_ws_end=at_ws_end,at_word_start=at_word_start):
                return self.match_eol_span_regexp(s,i,seq,at_line_start,at_ws_end,at_word_start)
        elif name == 'keywords':
            def f(self,s,i):
                return self.match_keywords(s,i)
            token_type = 'keyword-n' ### To be replaced by keyword1,...,keyword4,leoKeyword.
        elif name in ('mark_following','mark_previous','seq'):
            def f(self,s,i,seq=seq,at_line_start=at_line_start,at_ws_end=at_ws_end,at_word_start=at_word_start):
                return self.match_seq(s,i,seq,at_line_start,at_ws_end,at_word_start)
        elif name == 'seq_regexp':
            def f(self,s,i,seq=seq,at_line_start=at_line_start,at_ws_end=at_ws_end,at_word_start=at_word_start):
                return self.match_seq_regexp(s,i,seq,at_line_start,at_ws_end,at_word_start)
        elif name == 'span':
            def f(self,s,i,begin=begin,end=end,at_line_start=at_line_start,at_ws_end=at_ws_end,at_word_start=at_word_start):
                return self.match_span(s,i,begin,end,at_line_start,at_ws_end,at_word_start)
        elif name == 'span_regexp':
            def f(self,s,i,begin=begin,end=end,at_line_start=at_line_start,at_ws_end=at_ws_end,at_word_start=at_word_start):
                return self.match_span_regexp(s,i,begin,end,at_line_start,at_ws_end,at_word_start)
        else:
            g.trace('no function for %s' % name)
            def f(self,s,i):
                return 0
    
        # g.trace('%-25s'%(name+':'+token_type),at_line_start,at_ws_end,at_word_start,repr(seq),repr(begin),repr(end))
        # state = 'rule %2d %-14s %9s' % (ruleNumber,name,token_type)
        return f,name,token_type
    #@nonl
    #@-node:ekr.20050530112849.1:createRuleMatcher
    #@+node:ekr.20050529190857:match_keywords
    # Keywords only match whole words.
    # Words are runs of text separated by non-alphanumeric characters.
    
    def match_keywords (self,s,i):
        
        '''Return the length of the keyword if present position matches any keyword.
        Otherwise, return 0.'''
        
        # We must be at the start of a word.
        if i > 0 and s[i-1] in self.word_chars:
            return 0
    
        word = self.get_word(s,i)
        if word and word in self.keywords:
            return len(word)
        else:
            return 0
    #@nonl
    #@-node:ekr.20050529190857:match_keywords
    #@+node:ekr.20050529182335:match_regexp_helper (TO DO)
    def match_regexp_helper (self,s,i,seq):
        
        '''Return the length of the matching text if seq (a regular expression) matches the present position.'''
        
        ### We may want to return a match object too.
        
        return 0 ### Not ready yet.
    #@nonl
    #@-node:ekr.20050529182335:match_regexp_helper (TO DO)
    #@+node:ekr.20050601045930:match_eol_span
    def match_eol_span (self,s,i,seq,at_line_start,at_ws_end,at_word_start):
        
        '''Return the length of the rest of line if SEQ matches s[i:]
        Return 0 if no match.
    
        'at_line_start':    True: sequence must start the line.
        'at_ws_end':        True: sequence must be first non-whitespace text of the line.
        'at_word_start':    True: sequence must start a word.'''
    
        if at_line_start and i != 0: return 0
        if at_ws_end and i != g.skip_ws(s,0): return 0
        if at_word_start and i > 0 and s[i-1] not in self.word_chars: return 0
    
        if g.match(s,i,seq):
            j = g.skip_to_end_of_line(s,i)
            return j - i 
        else:
            return 0
    #@-node:ekr.20050601045930:match_eol_span
    #@+node:ekr.20050601063317:match_eol_span_regexp
    def match_eol_span_regexp (self,s,i,seq,at_line_start,at_ws_end,at_word_start,hash_char):
        
        '''Return the length of rest if the line if seq (a regx) matches s[i:]
        Return 0 if no match.
    
        'at_line_start':    True: sequence must start the line.
        'at_ws_end':        True: sequence must be first non-whitespace text of the line.
        'at_word_start':    True: sequence must start a word.
        'hash_char':        The first character of the regexp (for speed).'''
    
        if at_line_start and i != 0: return 0
        if at_ws_end and i != g.skip_ws(s,0): return 0
        if at_word_start and i > 0 and s[i-1] not in self.word_chars: return 0
        
        # Test hash_char first to increase speed.
        if i < len(s) and s[i] == hash_char:
            n = self.match_regexp_helper(s,i,seq)
            if n > 0:
                j = g.skip_to_end_of_line(s,i)
                return j - i
            else:
                return 0
        else:
            return 0
    #@nonl
    #@-node:ekr.20050601063317:match_eol_span_regexp
    #@+node:ekr.20050529182335.1:match_seq, match_mark_following/previous
    def match_seq (self,s,i,seq,at_line_start,at_ws_end,at_word_start):
        
        '''Return the length of a matched SEQ or 0 if no match.
    
        'at_line_start':    True: sequence must start the line.
        'at_ws_end':        True: sequence must be first non-whitespace text of the line.
        'at_word_start':    True: sequence must start a word.'''
    
        if at_line_start and i != 0: return 0
        if at_ws_end and i != g.skip_ws(s,0): return 0
        if at_word_start and i > 0 and s[i-1] not in self.word_chars: return 0
    
        if g.match(s,i,seq): return len(seq)
        else: return 0
    
    # For spans & marks, seq comes from the contents.
    match_mark_following  = match_seq
    match_mark_previous   = match_seq
    #@nonl
    #@-node:ekr.20050529182335.1:match_seq, match_mark_following/previous
    #@+node:ekr.20050529215620:match_seq_regexp
    def match_seq_regexp (self,s,i,seq,at_line_start,at_ws_end,at_word_start,hash_char):
        
        '''Return the length of a matched SEQ_REGEXP or 0 if no match.
    
        'at_line_start':    True: sequence must start the line.
        'at_ws_end':        True: sequence must be first non-whitespace text of the line.
        'at_word_start':    True: sequence must start a word.
        'hash_char':        The first character of the regexp (for speed).'''
    
        if at_line_start and i != 0: return 0
        if at_ws_end and i != g.skip_ws(s,0): return 0
        if at_word_start and i > 0 and s[i-1] not in self.word_chars: return 0
        
        # Test hash_char first to increase speed.
        if i < len(s) and s[i] == hash_char:
            return self.match_regexp_helper(s,i,seq)
        else:
            return 0
    #@nonl
    #@-node:ekr.20050529215620:match_seq_regexp
    #@+node:ekr.20050529185208.2:match_span
    def match_span (self,s,i,begin,end,at_line_start,at_ws_end,at_word_start):
        
        '''Return the length of a matched SPAN or 0 if no match.
    
        'at_line_start':    True: sequence must start the line.
        'at_ws_end':        True: sequence must be first non-whitespace text of the line.
        'at_word_start':    True: sequence must start a word.'''
        
        if at_line_start and i != 0: return 0
        if at_ws_end and i != g.skip_ws(s,0): return 0
        if at_word_start and i > 0 and s[i-1] not in self.word_chars: return 0
    
        if g.match(s,i,begin):
            j = s.find(end,i+len(begin))
            if j > -1:
                return j + len(end) - i
            else:
                return 0
        else:
            return 0
    #@nonl
    #@-node:ekr.20050529185208.2:match_span
    #@+node:ekr.20050529215732:match_span_regexp
    def match_span_regexp (self,s,i,begin,end,hash_char):
        
        '''Return the length of a matched SPAN_REGEXP or 0 if no match.
    
        'at_line_start':    True: sequence must start the line.
        'at_ws_end':        True: sequence must be first non-whitespace text of the line.
        'at_word_start':    True: sequence must start a word.
        'hash_char':        The first character of the regexp (for speed).'''
        
        if at_line_start and i != 0: return 0
        if at_ws_end and i != g.skip_ws(s,0): return 0
        if at_word_start and i > 0 and s[i-1] not in self.word_chars: return 0
        
        # Test hash_char first to increase speed.
        if i < len(s) and s[i] == hash_char:
            n = self.match_regexp_helper(s,i,begin)
            # We may have to allow $n here, in which case we must use a regex object?
            if n > 0 and g.match(s,i+n,end):
                return n + len(end)
        else:
            return 0
    #@nonl
    #@-node:ekr.20050529215732:match_span_regexp
    #@-node:ekr.20050529180421.47:Rule matching methods
    #@-others
#@nonl
#@-node:ekr.20050529143413.4:class colorizer
#@-others
#@nonl
#@-node:ekr.20050529142847:@thin __jEdit_colorizer__.py
#@-leo
