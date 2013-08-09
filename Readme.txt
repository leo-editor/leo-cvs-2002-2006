===================
Leo History Project
===================

Building the most continuous possible source code history for the Leo Editor (www.leoeditor.com).

This branch, represents is the state of Leo from 2002 to 2008, when it was hosted on sourceforge CVS (http://leo.cvs.sourceforge.net/).

started in August of 2013 by Matt Wilkie <maphew@gmail.com>


Method:

    1. Get local copy of CVS repository
    2. Convert to bazaar fast-import format
    3. Import to bazaar, push to Launchpad
    
   
=== 1. Backup CVS repository (actual repo, not a working copy):

    rsync -av rsync://leo.cvs.sourceforge.net/cvsroot/leo/* leo-cvs-repo
  


=== 2. Convert to bazaar fast-import format

    python cvs2svn-2.4.0\cvs2bzr --options=cvs2bzr.options
    
This took a LONG time to complete, a little over 13 hours, and generated a 3.5GB dumpfile (which crunched down to 78mb zipped).

Initially there was an error converting to Unicode. I set the fallback encoding to ascii, so there maybe some log messages which have been slightly garbled. 

    Time for pass1 (CollectRevsPass): 7.766 seconds.
    ----- pass 2 (CleanMetadataPass) -----
    Converting metadata to UTF8...
    WARNING: Problem decoding log message:
    ---------------------------------------------------------------------------
    Copy getpreferredencoding() from locale.py in Python 2.3alpha2 to leoGlobals.py.
    Use getpreferredencoding() instead of locale.getdefaultlocale(), which according to Martin v. L÷wis is broken and can't be fixed.

    ---------------------------------------------------------------------------
    ERROR: There were warnings converting author names and/or log messages
    to Unicode (see messages above).  Please restart this pass
    with one or more '--encoding' parameters or with
    '--fallback-encoding'.


Final report:

    cvs2svn Statistics:
    ------------------
    Total CVS Files:               539
    Total CVS Revisions:         11606
    Total CVS Branches:              0
    Total CVS Tags:               9317
    Total Unique Tags:              49
    Total Unique Branches:           0
    CVS Repos Size in KB:       385978
    Total SVN Commits:            4398
    First Revision Date:    Fri Mar 10 12:21:31 2000
    Last Revision Date:     Wed Mar 29 15:51:16 2006
    ------------------
    Timings (seconds):
    ------------------
        7   pass1    CollectRevsPass
        0   pass2    CleanMetadataPass
        0   pass3    CollateSymbolsPass
        2   pass4    FilterSymbolsPass
        0   pass5    SortRevisionsPass
        0   pass6    SortSymbolsPass
        2   pass7    InitializeChangesetsPass
        2   pass8    BreakRevisionChangesetCyclesPass
        2   pass9    RevisionTopologicalSortPass
        1   pass10   BreakSymbolChangesetCyclesPass
        2   pass11   BreakAllChangesetCyclesPass
        2   pass12   TopologicalSortPass
        6   pass13   CreateRevsPass
        0   pass14   SortSymbolOpeningsClosingsPass
        0   pass15   IndexSymbolsPass
    49445   pass16   OutputPass
    49473   total


=== 3. Import to bazaar, push to Launchpad

    bzr fast-import D:/code/leo-csv/cvs2svn_dumpfile.raw leo-from-cvs.bzr
    cd leo-from-cvs.bzr
    bzr push lp:~maphew/leo-editor/cvs-2002-2006
    
was uneventful, and took the better part of an hour, for each step.

