<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="21" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="-4" left="25" height="31" width="87"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences allow_rich_text="0">
</preferences>
<find_panel_settings>
	<find_string></find_string>
	<change_string></change_string>
</find_panel_settings>
<vnodes>
<v t="T1" a="E"><vh>NSIS Sample Scripts</vh>
<v t="T2" a="V"><vh>Change log</vh></v>
<v t="T3" a="E"><vh>NSIS script for Leo</vh>
<v t="T4"><vh>@root leo.nsi</vh>
<v t="T5"><vh>&lt;&lt; installer settings &gt;&gt;</vh>
<v t="T6"><vh>&lt;&lt; icons used by the installer &gt;&gt;</vh></v>
<v t="T7"><vh>&lt;&lt; the installation dir &gt;&gt;</vh></v>
<v t="T8"><vh>&lt;&lt; the user license &gt;&gt;</vh></v>
<v t="T9"><vh>&lt;&lt; Additional Installer Settings &gt;&gt;</vh></v>
</v>
<v t="T10"><vh>&lt;&lt; required files section&gt;&gt;</vh>
<v t="T11"><vh>&lt;&lt; check to see whether Python is installed &gt;&gt;</vh></v>
</v>
<v t="T12"><vh>&lt;&lt; optional files section&gt;&gt;</vh></v>
<v t="T13"><vh>&lt;&lt; file association &gt;&gt;</vh></v>
<v t="T14"><vh>&lt;&lt; post install section &gt;&gt;</vh></v>
<v t="T15" a="E"><vh>&lt;&lt; uninstall section &gt;&gt;</vh>
<v t="T16"><vh>&lt;&lt; remove file association &gt;&gt;</vh></v>
<v t="T17"><vh>&lt;&lt; remove program folder &gt;&gt;</vh></v>
<v t="T18"><vh>&lt;&lt; remove shortcuts &gt;&gt;</vh></v>
</v>
</v>
<v><vh>hold</vh>
<v t="T19"><vh>&lt;&lt; get the path to pythonw.exe &gt;&gt;</vh></v>
</v>
</v>
<v t="T20"><vh>License file</vh>
<v t="T21"><vh>@root leo_license.txt</vh></v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="T1">@doc

This file contains sample NSIS script(s). Use these scripts with NSIS to create an installer packages.

NSIS is Nullsoft's nifty free installer, available at http://www.nullsoft.com

Version 1.0 of this Leo file by Joe Orr, donated to public domain.</t>
<t tx="T2">8/13/02: Added sbooks.chm to manifest.</t>
<t tx="T3">@nocolor

NSIS Script for LEO - Literate Programming Editor with Outlines
http://sourceforge.net/projects/leo

How to create an installer for Leo using this script:
	1. Install NSIS (from http://www.nullsoft.com)
	2. Put the leo.nsi file in the directory containing the Leo program files.
	3. Right-click on the leo.nsi file and choose "Compile"
	
Version 1.0 of this script by Joe Orr, donated to public domain.

@color</t>
<t tx="T4">@comment ;
@silent
@root leo.nsi

; NOTE: this .NSI script is designed for NSIS v1.8+

&lt;&lt; installer settings &gt;&gt;
&lt;&lt; required files section &gt;&gt;
&lt;&lt; optional files section &gt;&gt;
&lt;&lt; file association &gt;&gt;
&lt;&lt; post install section &gt;&gt;
&lt;&lt; uninstall section &gt;&gt;

; eof</t>
<t tx="T5">@code

# [Installer Attributes]
Name "Leo"
OutFile "leosetup.exe"
Caption "Leo Installer"

&lt;&lt; Additional Installer Settings &gt;&gt;

&lt;&lt; icons used by the installer &gt;&gt;
&lt;&lt; the user license &gt;&gt;
&lt;&lt; the installation dir &gt;&gt;

ComponentText "This will install Leo on your computer. Select which optional components you would also like to install."</t>
<t tx="T6">@code
Icon Icons\leo_inst.ico
EnabledBitmap Icons\leo_on.bmp
DisabledBitmap Icons\leo_off.bmp</t>
<t tx="T7">@code
InstallDir "$PROGRAMFILES\Leo"
InstallDirRegKey HKEY_LOCAL_MACHINE "SOFTWARE\EKR\leo" ""
DirShow show # (make this hide to not let the user change it)
DirText "Select the directory to install Leo in:"</t>
<t tx="T8">@code
LicenseText "You must agree to this license before installing."
LicenseData "leo_license.txt"</t>
<t tx="T9">@ You may not need to change these for your own app...
@c
ShowInstDetails show
AutoCloseWindow false
SilentInstall normal
CRCCheck on
SetCompress auto
SetDatablockOptimize on
SetOverwrite ifnewer
WindowIcon off</t>
<t tx="T10">@code

Section "Leo" ; (default, required section)

  &lt;&lt; check to see whether Python is installed &gt;&gt;

ok:
  # here we list all files to included in installer	
  # first list the folder (using SetOutPath) then the filespec
  SetOutPath "$INSTDIR"
  File leo_license.txt
  File LeoPy.leo
  File LeoDocs.leo
  File leoConfig.leo
  File leo*.py
  File leoConfig.txt
  File c2py.py
  File openLeo.py
  File tangle_done.py
  File untangle_done.py
  File __init__.py
  File README.txt
  File leo.rc
  File leo.res
  File sdist.bat
  File sbooks.chm
  File manifest.in
  SetOutPath "$INSTDIR\Icons"
  File "Icons\*.*"

SectionEnd ; end of default section</t>
<t tx="T11">@code
# I sure hope there is a better way to do this, but other techniques don't seem to work.

# Supposedly the Python installer creates the following registry entry
# HKEY_LOCAL_MACHINE\Software\Python\PythonCore\CurrentVersion
# and then we can read find the Python folder location via
# HKEY_LOCAL_MACHINE\Software\Python\PythonCore\{versionno}. 
# Unfortunately, at the time of this writing, the Python installer is NOT writing the first entry. There is no way to know what the current versionno is.
# Hence, the following hack.

# Get pythonw.exe path from registry... except it isn't there, nor is it an environment variable... thanks guys!
# We'll have to get it in a roundabout way
ReadRegStr $9 HKEY_LOCAL_MACHINE "SOFTWARE\Classes\Python.NoConFile\shell\open\command" ""

# cut 8 characters from back of the open command
StrCpy $8 $9 -8

IfFileExists $8 ok tryagain

tryagain:
# ok, that  didn't work, but since the Python installer doesn't seem to be consistent, we'll try again
# cut 3 characters from back of the open command
StrCpy $8 $9 -3

IfFileExists $8 ok ng

ng:
  MessageBox MB_OK "Python is not installed on this system. $\nPlease install Python first. $\n$\nClick OK to cancel installation and remove installation Files."
  Delete "$INSTDIR\Icons\*.*" ; Icons dir
  RMDir "$INSTDIR\Icons"
  Delete "$INSTDIR\*.*" ; 
  RMDir "$INSTDIR"
  Quit
  
</t>
<t tx="T12">@code

# optional sections

Section "Start Menu Shortcuts"
  CreateDirectory "$SMPROGRAMS\Leo"
  CreateShortCut "$SMPROGRAMS\Leo\Uninstall.lnk" "$INSTDIR\uninst.exe" "" "$INSTDIR\uninst.exe" 0
  CreateShortCut "$SMPROGRAMS\Leo\Leo.lnk" "$8" '"$INSTDIR\leo.py"' "$INSTDIR\Icons\LeoApp.ico" 0  
SectionEnd

Section "Desktop Shortcut"
  CreateShortCut "$DESKTOP\Leo.lnk" "$8" '"$INSTDIR\leo.py"' "$INSTDIR\Icons\LeoApp.ico" 0
SectionEnd</t>
<t tx="T13">@code

Section ".leo File Association"
  SectionIn 1
  SectionIn 2
  SectionIn 3

  # back up old value of .leo in case some other program was using it
  ReadRegStr $1 HKCR ".leo" ""
  StrCmp $1 "" Label1
  StrCmp $1 "LeoFile" Label1
  WriteRegStr HKCR ".leo" "backup_val" $1
 
Label1:
  WriteRegStr HKCR ".leo" "" "LeoFile"
  WriteRegStr HKCR "LeoFile" "" "Leo File"
  WriteRegStr HKCR "LeoFile\shell" "" "open"
  WriteRegStr HKCR "LeoFile\DefaultIcon" "" $INSTDIR\Icons\LeoDoc.ico,0 
  WriteRegStr HKCR "LeoFile\shell\open\command" "" '$8 "$INSTDIR\leo.py" %1'  

SectionEnd</t>
<t tx="T14">@code

Section "-post" # (post install section, happens last after any optional sections)

  # add any commands that need to happen after any optional sections here
  WriteRegStr HKEY_LOCAL_MACHINE "SOFTWARE\EKR\leo" "" "$INSTDIR"
  WriteRegStr HKEY_LOCAL_MACHINE "Software\Microsoft\Windows\CurrentVersion\Uninstall\leo" "DisplayName" "Leo (remove only)"
  WriteRegStr HKEY_LOCAL_MACHINE "Software\Microsoft\Windows\CurrentVersion\Uninstall\leo" "UninstallString" '"$INSTDIR\uninst.exe"'

  # write out uninstaller
  WriteUninstaller "$INSTDIR\uninst.exe"

SectionEnd ; end of -post section

</t>
<t tx="T15">@code

# [ begin uninstall settings/section ]
UninstallText "This will uninstall Leo from your system"
UninstallCaption "Uninstall Leo"
UninstallIcon Icons\uninst.ico

Section Uninstall

DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\EKR\leo"
DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\leo"

&lt;&lt; remove file association &gt;&gt;
&lt;&lt; remove program folder &gt;&gt;
&lt;&lt; remove shortcuts &gt;&gt;

; remove directories used.
RMDir "$SMPROGRAMS\Leo"

SectionEnd ; end of uninstall section</t>
<t tx="T16">@code

  ReadRegStr $1 HKCR ".leo" ""
  StrCmp $1 "LeoFile" 0 NoOwn ; only do this if we own it
    ReadRegStr $1 HKCR ".leo" "backup_val"
    StrCmp $1 "" 0 RestoreBackup ; if backup == "" then delete the whole key
      DeleteRegKey HKCR ".leo"
    Goto NoOwn
    RestoreBackup:
      WriteRegStr HKCR ".leo" "" $1
      DeleteRegValue HKCR ".leo" "backup_val"
  NoOwn:
</t>
<t tx="T17">@code
MessageBox MB_YESNO|MB_ICONQUESTION \
             "Delete all files in Leo Program folder?" \
             IDNO NoDelete
  Delete "$INSTDIR\Icons\*.*" ; Icons dir
  RMDir "$INSTDIR\Icons"
  Delete "$INSTDIR\*.*" ; 
  RMDir "$INSTDIR"
NoDelete:
</t>
<t tx="T18">@code
Delete "$SMPROGRAMS\Leo\*.*"
Delete "$DESKTOP\Leo.lnk"</t>
<t tx="T19">
# yo - why doesn't this work?
#ExecShell open "$INSTDIR\getpypath.pyw"

#IfFileExists "$INSTDIR\pypath.txt" ok ng
#ok:
#  FileOpen $9 "$INSTDIR\pypath.txt" "r"
#  FileRead $9 $8
#  FileClose $9
#  Delete "$INSTDIR\pypath.txt"
#  MessageBox MB_OK "urk"
#  Return
#ng:
#  MessageBox MB_OK "Python is not installed on this system. $\nPlease install Python first. $\n$\nClick OK to cancel installation and remove installation Files."
#  Delete "$INSTDIR\Icons\*.*" ; Icons dir
#  RMDir "$INSTDIR\Icons"
#  Delete "$INSTDIR\*.*" ; 
#  RMDir "$INSTDIR"
#  Quit

</t>
<t tx="T20">@nocolor

Note: the copyright sign in the license will appear properly when rendered in the encoding specified for this Leo file.  By default this is UTF-8.</t>
<t tx="T21">@silent
@root leo_license.txt

Leo is Open Software and is distributed under the terms of the Python License. The gist of the license is that Leo is absolutely free, even for commercial use (including resale). There is no GNU-like "copyleft" restriction. The Open Source Initiative board has voted to certify the Python license as Open Source. This license is compatible with the GPL.

Copyright (c) 1997-2002 by Edward K. Ream. All Rights Reserved.

Permission to use, copy, modify, and distribute this software and its documentation for any purpose and without fee is hereby granted, provided that the above copyright notice appear in all copies and that both that copyright notice and this permission notice appear in supporting documentation, and that the names of Leo or Edward K. Ream not be used in advertising or publicity pertaining to distribution of the software without specific, written prior permission.

DISCLAIMER OF WARRANTIES

EDWARD K. REAM (REAM) SPECIFICALLY DISCLAIMS ALL WARRANTIES, EXPRESSED OR IMPLIED, WITH RESPECT TO THIS COMPUTER SOFTWARE, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS RO A PARTICULAR PURPOSE. IN NO EVENT SHALL REAM BE LIABLE FOR ANY LOSS OF PROFIT OR ANY COMMERCIAL DAMAGE, INCLUDING BUT NOT LIMITED TO SPECIAL, INCIDENTAL, CONSEQUENTIAL OR OTHER DAMAGES.</t>
</tnodes>
</leo_file>
