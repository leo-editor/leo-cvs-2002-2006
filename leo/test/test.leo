<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="2857" clone_windows="0"/>
<globals body_outline_ratio="0.463110102157">
	<global_window_position top="32" left="228" height="881" width="866"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences>
</preferences>
<find_panel_settings>
	<find_string></find_string>
	<change_string></change_string>
</find_panel_settings>
<vnodes>
<v t="ekr.20040414074728" a="TV"><vh>Distribution checklist</vh>
<v t="ekr.20040414074728.1" tnodeList="ekr.20040414074728.1"><vh>@file-nosent c:\prog\leoCVS\.pycheckrc</vh></v>
<v t="ekr.20040414074728.2"><vh>@url http://www.python.org/pypi?:action=submit_form</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="ekr.20040414074728">@color

# **** Run this from test.leo ****

# Run pychecker from idle.
if 1:
	import pychecker.checker
	import leo
@nocolor
Documentation
	- Update readme.txt
	- Update LeoDocs.leo
	** Update version number on web site.
Version numbers
	- Update version number in Help menu.
	- Update version number in setup.py (@ignore'd!!)
	** Make sure the top-level directory has no spaces in its name.
@color

if 1: # Save all files and tangle leoConfig.leo
	from leoGlobals import importFromPath
	preSetup = importFromPath("preSetup","c:\prog\leoCvs\leo")
	preSetup.setup()

if 1: # Replace config settings and create .zip file.
	import os
	os.system(r"c:\python22\python c:\prog\leoCvs\leo\setup.py sdist --formats=zip")

@nocolor
Create and test leosetup.exe.
	- Create leosetup.exe by right-clicking leo.nsi and choosing "compile with NSI (bz2)"
	- Test created leosetup.exe file.
	- test the files created in c:\program files\leo

@color
# **** Scan all folders &amp; files before uploading.
@nocolor

Create Release on SourceForge

Uploads
    - Upload leodocs.zip
	- Upload leosetup.exe
	- Upload leo-x-y.zip
	- Upload sbook.chm if it has been changed.
Announcements
	- Announce to SourceForge itself. USE ANNOUNCEMENT FORMAT, not readme format.
	- Announce to Leo's SourceForce site.
	- Announce to comp.lang.python
	- Announce to comp.programming.literate
	- Register Leo at http://www.python.org/pypi?:action=submit_form</t>
<t tx="ekr.20040414074728.1"># Sample defaults file for PyChecker 0.8.13
# This file should be called:  .pycheckrc
# It should be placed in your home directory (value of $HOME).
# If $HOME is not set, it will look in the current directory.

# file = c:/prog/leoCVS/leo/src/leo.py

# bool: warnings for Doc Strings
noDocModule = 0
noDocClass = 0
noDocFunc = 0

# bool: when checking if class data members (attributes) are set
#       check all members or __init__() only
onlyCheckInitForMembers = 0

# bool: warn when all module variables are not used (including private vars)
allVariablesUsed = 0

# bool: produce warnings for each occurrence of a warning for global (xxx)
reportAllGlobals = 0

# bool: warn when private module variables are not used (_var)
privateVariableUsed = 1

# bool: warn when imports are not used
importUsed = 1

# bool: warn when import and from ... import are used for same module
mixImport = 0 # EKR

# bool: warn when imports are not used in __init__.py
packageImportUsed = 1

# bool: warn when a module reimports another module (import &amp; from/import)
moduleImportErrors = 0 # EKR

# bool: warn when modules import themselves
reimportSelf = 0 # EKR

# bool: warn when local variables are not used
localVariablesUsed = 1

# bool:  assume a, b, and c are used in this case:  a, b, c = func()
unusedLocalTuple = 0

# bool:  warn when class attributes (data members) are unused
membersUsed = 0

# bool: warn when Subclass.__init__ is not called in a subclass
baseClassInitted = 1

# bool: warn when Subclass needs to override methods that only throw exceptions
abstractClasses = 1

# bool: warn when __init__ is defined in a subclass
initDefinedInSubclass = 0

# bool: warn when __init__ returns None
returnNoneFromInit = 1

# bool: warn when code is not reachable
unreachableCode = 0

# bool: warn when a constant is used in a conditional statement (if '':)
constantConditions = 1

# bool: warn when 1 is used in a conditional statement, (if 1: while 1: etc)
constant1 = 0

# bool: warn when iterating over a string in a for loop
stringIteration = 1

# bool: warn when setting a variable to different types
inconsistentTypes = 0

# bool: warn when setting a tuple of variables to a non-sequence (a, b = None)
unpackNonSequence = 1

# bool: warn when setting a tuple of variables to the wrong length (a, b = 1,)
unpackLength = 1

# bool: warn when using strings exceptions or 
#       other classes not derived from Exception to raise/catch exceptions
badExceptions = 1

# bool: warn when statements appear to have no effect
noEffect = 1

# bool: warn when using (expr % 1), it has no effect on integers and strings
modulo1 = 1

# bool: warn if using (expr is const-literal), 
# doesn't always work on integers and strings
isLiteral = 0 # EKR

# bool: warn when using a deprecated module or function
deprecated = 1

# bool: warn when the class attribute does not exist
classAttrExists = 1

# bool: warn when calling an attribute not a method
callingAttribute = 0

# bool: warn when using named arguments: func(a=1, b=2), where def func(a, b):
#       def func2(a, b, **kw): doesn't generate a warning
namedArgs = 0 # EKR

# str: name of 'self' parameter
methodArgName = 'self'

# list of str: names of first parameter to classmethods
## classmethodArgNames = ['cls', 'klass']

# bool: warn when method/function arguments are unused
argumentsUsed = 1

# bool: ignore if self is unused in methods
ignoreSelfUnused = 0

# bool: warn if functions/classes/methods names are redefined in same scope
redefiningFunction = 1

# bool:  check if an overriden method has the same signature
#	 as base class method (__init__() methods are not checked)
checkOverridenMethods = 1

# bool:  check if a special (reserved) method has the correct signature
#	 and is known (these are methods that begin and end with __
## checkSpecialMethods = 1

# int: warnings for code complexity, max value before generating a warning
maxLines = 2000
maxBranches = 500
maxReturns = 100
maxArgs = 100
maxLocals = 250
maxReferences = 500

# bool:  ignore all warnings from standard library components
#	 (this includes anything under the standard library, eg, site-packages)
ignoreStandardLibrary = 1 # EKR

# list of strings: ignore unused locals/arguments if name is one of
unusedNames = [
	'_', 'empty', 'unused', 'dummy', 'event', 'commander',
	'c', 'i', 'j', 'k', 's',
	'tag', 'args', 'keys', 'keywords']

# list of strings: ignore warnings generated from these modules
blacklist = [
	'leoGlobals',
	'leoConfig',
	'leoFrame', 'leoMenu', 'leoGui', # Base classes have lots of unused params.
	'Tkinter', 'wxPython', 'gtk', 'GTK', 'GDK', ]

# list of strings: ignore global variables not used if name is one of
variablesToIgnore = [ '__all__', '__version__', '__copyright__', ]

# bool: print the PyChecker parse of modules, classes, etc.
printParse = 0

# bool: turn debugging of PyChecker on
debug = 0

# bool: check that attributes of objects exist
checkObjectAttrs = 1

# bool: various warnings about incorrect usage of __slots__
slots = 1

# bool: check if __slots__ is empty
emptySlots = 1

# bool: check for using properties in classic classes
classicProperties = 1

# bool: check for integer division (may be problem between Python versions)
intDivide = 1

# bool: check if local variables shadow a global variable with same name
shadows = 0 # EKR

# bool: check if input() is used, which is a security problem, use raw_input()
usesInput = 1

# bool: check if using a constant string to getattr()/setattr()
# Doesn't exist.
## constAttr = 1

# bool: check for using +variable, since it is almost always has no effect
unaryPositive = 1

# bool: check for modifying a parameter with a default value
#       (value must be: list, dict, instance)
#       modifying the value may have undesirable/unexpected side-effects
modifyDefaultValue = 1

# bool: check if the exec statement is used (possible security problem)
usesExec = 0

# bool: check consistent return values
checkReturnValues = 1

# bool: check if using implict and explicit return values
checkImplicitReturns = 1

# dict: suppress warnings, key is module.class.method or module.function
#	value is a string of command line arguments (can omit -- for long args)
#       { 'module1': 'no-namedargs maxlines=0',
#	  'module2.my_func': 'argsused',
#	  'module3.my_class': 'no-initreturn', }
if 1:
	suppressions = {}
else: # Doesn't work
	suppressions = {
		'leoFrame' : 'argumentsUsed=0',
		'leoGui' : 'argumentsUsed=0' }

# dict: suppress warnings where keys can be regular expressions
suppressionRegexs = {}</t>
<t tx="ekr.20040414074728.2"></t>
</tnodes>
</leo_file>
