<?xml version="1.0" encoding="UTF-8"?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="4545" clone_windows="0"/>
<globals body_outline_ratio="0.620296465222">
	<global_window_position top="10" left="342" height="877" width="916"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences>
</preferences>
<find_panel_settings>
	<find_string></find_string>
	<change_string></change_string>
</find_panel_settings>
<vnodes>
<v t="EKR.20040430162943"><vh>Notes...</vh>
<v t="ekr.20031218072017"><vh>@file-thin ../doc/leoDiary.txt</vh></v>
<v t="ekr.20031218072017.329"><vh>@file-thin ../doc/leoNotes.txt</vh></v>
</v>
<v t="ekr.20040117181936"><vh>@file-thin ../doc/leoToDo.txt</vh></v>
<v t="EKR.20040429143933"><vh>@file-thin leoProjects.txt</vh></v>
<v t="EKR.20040427074150"><vh>Bug: suboutline only option doesn't work</vh></v>
<v t="EKR.20040502125334"><vh>To do: create LeoPy(ref).leo</vh></v>
<v t="ekr.20031218072017.2406" a="TV"><vh>Code</vh>
<v t="ekr.20031218072017.2407"><vh>  Overview of code</vh>
<v t="ekr.20031218072017.2408"><vh>&lt;&lt; About clones &gt;&gt;</vh></v>
<v t="ekr.20031218072017.2409"><vh>&lt;&lt; About drawing &gt;&gt;</vh></v>
<v t="ekr.20031218072017.2410"><vh>&lt;&lt; About handling events &gt;&gt;</vh></v>
<v t="ekr.20031218072017.2411"><vh>&lt;&lt; About Tangle and Untangle &gt;&gt;</vh></v>
<v t="ekr.20031218072017.2412"><vh>&lt;&lt; About the vnode and tnode classes &gt;&gt;</vh></v>
<v t="ekr.20031218072017.2413"><vh>&lt;&lt; How Leo implements unlimited undo &gt;&gt;</vh></v>
<v t="ekr.20031218072017.2414"><vh>&lt;&lt; Theory of operation of find/change &gt;&gt;</vh></v>
</v>
<v t="ekr.20031218072017.2415"><vh>  Scripts</vh>
<v t="ekr.20040327103735.2"><vh>Script Tools (leoGlobals.py)</vh>
<v t="ekr.20031218072017.2418"><vh>g.initScriptFind (set up dialog)</vh></v>
<v t="ekr.20040321065415"><vh>g.findNodeInTree, findNodeAnywhere, findTopLevelNode</vh></v>
</v>
<v t="ekr.20031218072017.2416"><vh>Fnd/change scripts</vh>
<v t="ekr.20040201070845"><vh>Routines that execute script-find and script-change</vh>
<v t="ekr.20031218072017.3072"><vh>doFind...Script</vh></v>
<v t="ekr.20031218072017.2417"><vh>doChange...Script</vh></v>
</v>
<v t="ekr.20040201061928"><vh>Find script to check for dubious leading whitespace</vh>
<v t="ekr.20040130112145"><vh>Find script</vh></v>
<v t="ekr.20040201104001"><vh>test</vh></v>
</v>
<v t="ekr.20031218072017.2419"><vh>Find script to clean whitespace</vh>
<v t="ekr.20031218072017.2420"><vh>Find script</vh></v>
<v t="ekr.20031218072017.2421"><vh>Change script</vh></v>
</v>
<v t="ekr.20031218072017.2422"><vh>Find scripts to convert @doc comments to doc strings</vh>
<v t="ekr.20031218072017.2423"><vh>Find script</vh></v>
<v t="ekr.20031218072017.2424"><vh>Change script</vh></v>
<v t="ekr.20031218072017.2425"><vh>re tests</vh></v>
<v t="ekr.20031218072017.2426"><vh>early find script</vh></v>
</v>
</v>
<v t="ekr.20040201063019"><vh>Other scripts</vh>
<v t="ekr.20040304163125"><vh>Script to find and replace all functions in leoGlobals.py</vh>
<v t="ekr.20040330110202"><vh>&lt;&lt; set nameList to the list of functions in leoGlobals.py &gt;&gt;</vh></v>
<v t="ekr.20040304165432.1"><vh>findFunctionsInTree</vh></v>
<v t="ekr.20040304163522"><vh>findDefs</vh></v>
<v t="ekr.20040304164949"><vh>prependNamesInTree</vh>
<v t="ekr.20040304173234.1"><vh>&lt;&lt; look for name followed by '(' &gt;&gt;</vh></v>
<v t="ekr.20040304173234"><vh>&lt;&lt; print before and after &gt;&gt;</vh></v>
</v>
</v>
<v t="ekr.20031218072017.4251"><vh>Clear all timestamps</vh></v>
<v t="ekr.20031218072017.4248"><vh>Create a graphviz file</vh>
<v t="ekr.20031218072017.4249"><vh>&lt;&lt;about this script&gt;&gt;</vh></v>
<v t="ekr.20040201063200"><vh>rPrint</vh></v>
<v t="ekr.20040201063200.1"><vh>newLineize</vh></v>
<v t="ekr.20040201063200.2"><vh>graphvizString</vh></v>
</v>
<v t="ekr.20031218072017.2429"><vh>Count pages</vh></v>
<v t="ekr.20040321064134"><vh>Count separate nodes (tnodes)</vh></v>
<v t="ekr.20040318150556"><vh>Count total, visible nodes</vh></v>
<v t="ekr.20031218072017.2428"><vh>Find script to change OnX to x in body (didn't quite work :-)</vh></v>
<v t="ekr.20031218072017.2427"><vh>Find scripts to change OnX to x in headline</vh></v>
</v>
<v t="ekr.20040104184644"><vh>Recursive import script</vh>
<v t="ekr.20040104184913.1"><vh>importFiles</vh></v>
<v t="ekr.20040104184913.2"><vh>importDir</vh></v>
<v t="ekr.20040104184913.3"><vh>createLastChildOf</vh></v>
</v>
<v t="ekr.20031218072017.2431"><vh>Testing scripts</vh>
<v t="ekr.20031218072017.2432"><vh>Script to clean unused tnodeLists</vh></v>
<v t="ekr.20031218072017.2433"><vh>Script to check topology of all clones</vh></v>
<v t="ekr.20031218072017.2434"><vh>Scripts for checking clones</vh>
<v t="ekr.20031218072017.2435"><vh>checkForMismatchedJoinedNodes</vh></v>
<v t="ekr.20031218072017.2436"><vh>checkForPossiblyBrokenLinks</vh></v>
<v t="ekr.20031218072017.2437"><vh>checkTopologiesOfLinkedNodes</vh></v>
<v t="ekr.20031218072017.2438"><vh>checkLinksOfNodesWithSameTopologies (to do)</vh></v>
</v>
</v>
<v t="ekr.20031218072017.2439"><vh>The scripts directory... (to be deleted?)</vh>
<v t="ekr.20031218072017.2440"><vh>@file-nosent ../scripts/LinixInstall.py</vh></v>
<v t="ekr.20031218072017.2441"><vh>../scripts/findDosFile</vh></v>
<v t="ekr.20031218072017.2442" tnodeList="ekr.20031218072017.2442,ekr.20031218072017.2444,ekr.20031218072017.2445,ekr.20031218072017.2446,ekr.20031218072017.2447,ekr.20031218072017.2448,ekr.20031218072017.2450,ekr.20031218072017.2451,ekr.20031218072017.2452,ekr.20031218072017.2453,ekr.20031218072017.2454,ekr.20031218072017.2455,ekr.20031218072017.2456,ekr.20031218072017.2457,ekr.20031218072017.2459,ekr.20031218072017.2460,ekr.20031218072017.2461,ekr.20031218072017.2462,ekr.20031218072017.2463,ekr.20031218072017.2466,ekr.20031218072017.2467,ekr.20031218072017.2468,ekr.20031218072017.2469,ekr.20031218072017.2470,ekr.20031218072017.2471,ekr.20031218072017.2472,ekr.20031218072017.2473,ekr.20031218072017.2474,ekr.20031218072017.2475,ekr.20031218072017.2476,ekr.20031218072017.2477,ekr.20031218072017.2478,ekr.20031218072017.2479,ekr.20031218072017.2480,ekr.20031218072017.2481,ekr.20031218072017.2482,ekr.20031218072017.2483,ekr.20031218072017.2484,ekr.20031218072017.2485,ekr.20031218072017.2486,ekr.20031218072017.2487,ekr.20031218072017.2488,ekr.20031218072017.2489,ekr.20031218072017.2490,ekr.20031218072017.2491,ekr.20031218072017.2492,ekr.20031218072017.2493,ekr.20031218072017.2494,ekr.20031218072017.2495,ekr.20031218072017.2496,ekr.20031218072017.2497,ekr.20031218072017.2498,ekr.20031218072017.2499,ekr.20031218072017.2500,ekr.20031218072017.2501,ekr.20031218072017.2502,ekr.20031218072017.2503,ekr.20031218072017.2504,ekr.20031218072017.2505,ekr.20031218072017.2506,ekr.20031218072017.2507,ekr.20031218072017.2508,ekr.20031218072017.2509"><vh>@file ../scripts/c2py.py</vh>
<v t="ekr.20031218072017.2443"><vh>Documentation</vh>
<v t="ekr.20031218072017.2444"><vh>&lt;&lt; what c2py does &gt;&gt;</vh></v>
<v t="ekr.20031218072017.2445"><vh>&lt;&lt; theory of operation &gt;&gt;</vh></v>
</v>
<v t="ekr.20031218072017.2446"><vh>&lt;&lt; specifying user types &gt;&gt;</vh></v>
<v t="ekr.20031218072017.2447"><vh>&lt;&lt; define testData &gt;&gt;</vh></v>
<v t="ekr.20031218072017.2448"><vh>speedTest</vh></v>
<v t="ekr.20031218072017.2449"><vh>leo1to2</vh>
<v t="ekr.20031218072017.2450"><vh>leo1to2</vh></v>
<v t="ekr.20031218072017.2451"><vh>convertLeo1to2</vh></v>
<v t="ekr.20031218072017.2452"><vh>convertStringLeo1to2</vh></v>
<v t="ekr.20031218072017.2453"><vh>convertCodeList1to2</vh></v>
</v>
<v t="ekr.20031218072017.2454"><vh>c2py entry points</vh>
<v t="ekr.20031218072017.2455"><vh>convertCurrentTree</vh></v>
<v t="ekr.20031218072017.2456"><vh>convertLeoTree</vh></v>
<v t="ekr.20031218072017.2457"><vh>convertCFileToPython</vh></v>
</v>
<v t="ekr.20031218072017.2458"><vh>c2py Top Level</vh>
<v t="ekr.20031218072017.2459"><vh>convertCStringToPython</vh></v>
<v t="ekr.20031218072017.2460"><vh>convertCodeList</vh></v>
<v t="ekr.20031218072017.2461"><vh>convertDocList</vh></v>
<v t="ekr.20031218072017.2462"><vh>skipDocPart</vh></v>
<v t="ekr.20031218072017.2463"><vh>skipCodePart</vh></v>
</v>
<v t="ekr.20031218072017.2464"><vh>removeSentinels</vh></v>
<v t="ekr.20031218072017.2465"><vh>Scanning &amp; Replacing</vh>
<v t="ekr.20031218072017.2466"><vh>convertLeadingBlanks</vh></v>
<v t="ekr.20031218072017.2467"><vh>findInList</vh></v>
<v t="ekr.20031218072017.2468"><vh>findInCode</vh></v>
<v t="ekr.20031218072017.2469"><vh>mungeAllFunctions</vh>
<v t="ekr.20031218072017.2470"><vh>handlePossibleFunctionHeader</vh></v>
<v t="ekr.20031218072017.2471"><vh>massageFunctionArgs</vh></v>
<v t="ekr.20031218072017.2472"><vh>massageFunctionHead (sets gClassName)</vh></v>
<v t="ekr.20031218072017.2473"><vh>massageFunctionBody</vh>
<v t="ekr.20031218072017.2474"><vh>massageIvars</vh></v>
<v t="ekr.20031218072017.2475"><vh>removeCasts</vh></v>
<v t="ekr.20031218072017.2476"><vh>removeTypeNames</vh></v>
</v>
</v>
<v t="ekr.20031218072017.2477"><vh>handleAllKeywords</vh>
<v t="ekr.20031218072017.2478"><vh>handleKeyword</vh></v>
</v>
<v t="ekr.20031218072017.2479"><vh>isWs and isWOrNl</vh></v>
<v t="ekr.20031218072017.2480"><vh>isSectionDef</vh></v>
<v t="ekr.20031218072017.2481"><vh>isStringOrComment</vh></v>
<v t="ekr.20031218072017.2482"><vh>match</vh></v>
<v t="ekr.20031218072017.2483"><vh>matchWord</vh></v>
<v t="ekr.20031218072017.2484"><vh>prevNonWsChar and prevNonWsOrNlChar</vh></v>
<v t="ekr.20031218072017.2485"><vh>removeAllCComments</vh></v>
<v t="ekr.20031218072017.2486"><vh>removeAllCSentinels</vh></v>
<v t="ekr.20031218072017.2487"><vh>removeAllPythonComments</vh></v>
<v t="ekr.20031218072017.2488"><vh>removeAllPythonSentinels</vh></v>
<v t="ekr.20031218072017.2489"><vh>removeAtRoot</vh></v>
<v t="ekr.20031218072017.2490"><vh>removeBlankLines</vh></v>
<v t="ekr.20031218072017.2491"><vh>removeExcessWs</vh>
<v t="ekr.20031218072017.2492"><vh>removeExessWsFromLine</vh></v>
</v>
<v t="ekr.20031218072017.2493"><vh>removeLeadingAtCode</vh></v>
<v t="ekr.20031218072017.2494"><vh>removeMatchingBrackets</vh></v>
<v t="ekr.20031218072017.2495"><vh>removeSemicolonsAtEndOfLines</vh></v>
<v t="ekr.20031218072017.2496"><vh>removeTrailingWs</vh></v>
<v t="ekr.20031218072017.2497"><vh>replace</vh></v>
<v t="ekr.20031218072017.2498"><vh>replaceComments</vh></v>
<v t="ekr.20031218072017.2499"><vh>replaceSectionDefs</vh></v>
<v t="ekr.20031218072017.2500"><vh>safeReplace</vh></v>
<v t="ekr.20031218072017.2501"><vh>skipCBlockComment</vh></v>
<v t="ekr.20031218072017.2502"><vh>skipPastLine</vh></v>
<v t="ekr.20031218072017.2503"><vh>skipPastWord</vh></v>
<v t="ekr.20031218072017.2504"><vh>skipString</vh></v>
<v t="ekr.20031218072017.2505"><vh>skipStringOrComment</vh></v>
<v t="ekr.20031218072017.2506"><vh>skipToMatchingBracket</vh></v>
<v t="ekr.20031218072017.2507"><vh>skipWs and skipWsAndNl</vh></v>
<v t="ekr.20031218072017.2508"><vh>stringToList</vh></v>
<v t="ekr.20031218072017.2509"><vh>listToString</vh></v>
</v>
</v>
<v t="ekr.20031218072017.2510"><vh>@file ../scripts/disStats.py</vh>
<v t="ekr.20031218072017.2511"><vh>go</vh></v>
<v t="ekr.20031218072017.2512"><vh>getFiles</vh></v>
<v t="ekr.20031218072017.2513"><vh>getModules</vh></v>
<v t="ekr.20031218072017.2514"><vh>any</vh></v>
<v t="ekr.20031218072017.2515"><vh>code</vh></v>
<v t="ekr.20031218072017.2516"><vh>print_stats</vh></v>
</v>
<v t="ekr.20031218072017.2517"><vh>@file ../scripts/leoFindScript.py</vh>
<v t="ekr.20031218072017.2518"><vh>changeAll</vh></v>
<v t="ekr.20031218072017.2519"><vh>changeNext</vh></v>
<v t="ekr.20031218072017.2520"><vh>changePrev</vh></v>
<v t="ekr.20031218072017.2521"><vh>findAll</vh></v>
<v t="ekr.20031218072017.2522"><vh>findNext</vh></v>
<v t="ekr.20031218072017.2523"><vh>findPrev</vh></v>
<v t="ekr.20031218072017.2524"><vh>reChangeAll</vh></v>
<v t="ekr.20031218072017.2525"><vh>reChangeNext</vh></v>
<v t="ekr.20031218072017.2526"><vh>reChangePrev</vh></v>
<v t="ekr.20031218072017.2527"><vh>reFindAll</vh></v>
<v t="ekr.20031218072017.2528"><vh>reFindNext</vh></v>
<v t="ekr.20031218072017.2529"><vh>reFindPrev</vh></v>
<v t="ekr.20031218072017.2530"><vh>lineAtPos</vh></v>
<v t="ekr.20031218072017.2531"><vh>printFindList</vh></v>
</v>
<v t="ekr.20031218072017.2532"><vh>@file ../scripts/openLeo.py</vh></v>
<v t="ekr.20031218072017.2533"><vh>@file ../scripts/tangle_done.py</vh>
<v t="ekr.20031218072017.2534"><vh>run</vh></v>
<v t="ekr.20031218072017.2535"><vh>convertRSTfilesToHTML</vh>
<v t="ekr.20031218072017.2536"><vh>&lt;&lt; Convert root to corresponding .html file &gt;&gt;</vh></v>
</v>
</v>
<v t="ekr.20031218072017.2537"><vh>@file ../scripts/untangle_done.py</vh></v>
</v>
</v>
<v t="ekr.20031218072017.2538"><vh> Distribution &amp; version stuff</vh>
<v t="ekr.20031218072017.2539"><vh> Distribution scripts &amp; files</vh>
<v t="ekr.20031218072017.2540"><vh>leo.nsi</vh>
<v t="ekr.20031218072017.2541"><vh>@root ../dist/leo.nsi</vh>
<v t="ekr.20031218072017.2542"><vh>&lt;&lt; installer settings &gt;&gt;</vh>
<v t="ekr.20031218072017.2543"><vh>&lt;&lt; icons used by the installer &gt;&gt;</vh></v>
<v t="ekr.20031218072017.2544"><vh>&lt;&lt; the installation dir &gt;&gt;</vh></v>
<v t="ekr.20031218072017.2545"><vh>&lt;&lt; the user license &gt;&gt;</vh></v>
<v t="ekr.20031218072017.2546"><vh>&lt;&lt; Additional Installer Settings &gt;&gt;</vh></v>
</v>
<v t="ekr.20031218072017.2547"><vh>&lt;&lt; required files section &gt;&gt;</vh>
<v t="ekr.20031218072017.2548"><vh>&lt;&lt; check to see whether Python is installed &gt;&gt;</vh></v>
</v>
<v t="ekr.20031218072017.2549"><vh>&lt;&lt; optional files section&gt;&gt;</vh></v>
<v t="ekr.20031218072017.2550"><vh>&lt;&lt; file association &gt;&gt;</vh></v>
<v t="ekr.20031218072017.2551"><vh>&lt;&lt; post install section &gt;&gt;</vh></v>
<v t="ekr.20031218072017.2552"><vh>&lt;&lt; uninstall section &gt;&gt;</vh>
<v t="ekr.20031218072017.2553"><vh>&lt;&lt; remove file association &gt;&gt;</vh></v>
<v t="ekr.20031218072017.2554"><vh>&lt;&lt; remove program folder &gt;&gt;</vh></v>
<v t="ekr.20031218072017.2555"><vh>&lt;&lt; remove shortcuts &gt;&gt;</vh></v>
</v>
</v>
</v>
<v t="ekr.20031218072017.2556"><vh>@silentfile ../doc/LICENSE.TXT</vh></v>
<v t="ekr.20031218072017.2557"><vh>@silentfile ../doc/INSTALL.TXT</vh>
<v t="ekr.20031218072017.2558"><vh>System requirements</vh></v>
<v t="ekr.20031218072017.2559"><vh>Linux installation</vh></v>
<v t="ekr.20031218072017.2560"><vh>Windows installation</vh></v>
<v t="ekr.20031218072017.2561"><vh>MacOS installation</vh></v>
<v t="ekr.20031218072017.2562"><vh>Shell &amp; batch scripts</vh></v>
</v>
<v t="ekr.20031218072017.2563"><vh>@silentfile ../doc/PKG-INFO.TXT</vh></v>
<v t="ekr.20031218072017.2564"><vh>@silentfile ../doc/README.TXT</vh></v>
<v t="ekr.20031218072017.2565"><vh>@silentfile ../manifest.in</vh></v>
<v t="ekr.20031218072017.2566"><vh>setup &amp; pre/postSetup (usually @ignore'd)</vh>
<v t="ekr.20031218072017.2567" tnodeList="ekr.20031218072017.2567,ekr.20031218072017.2568,ekr.20031218072017.2569"><vh>@file ../preSetup.py</vh>
<v t="ekr.20031218072017.2568"><vh>saveAllLeoFiles</vh></v>
<v t="ekr.20031218072017.2569"><vh>tangleLeoConfigDotLeo</vh></v>
</v>
<v t="ekr.20031218072017.2570" tnodeList="ekr.20031218072017.2570,ekr.20031218072017.2572,ekr.20031218072017.2573,ekr.20031218072017.2574,ekr.20031218072017.2575,ekr.20031218072017.2571"><vh>@file ../setup.py</vh>
<v t="ekr.20031218072017.2571"><vh>&lt;&lt; setup info for setup.py &gt;&gt; UPDATE BY HAND (no spaces)</vh></v>
<v t="ekr.20031218072017.2572"><vh>printReminders</vh></v>
<v t="ekr.20031218072017.2573"><vh>generateModules</vh></v>
<v t="ekr.20031218072017.2574"><vh>replacePatterns</vh></v>
<v t="ekr.20031218072017.2575"><vh>setDefaultParams</vh></v>
</v>
<v t="ekr.20031218072017.2576" tnodeList="ekr.20031218072017.2576,ekr.20031218072017.2574,ekr.20031218072017.2577"><vh>@file ../postSetup.py</vh>
<v t="ekr.20031218072017.2574"><vh>replacePatterns</vh></v>
<v t="ekr.20031218072017.2577"><vh>unsetDefaultParams</vh></v>
</v>
</v>
<v t="ekr.20031218072017.2578"><vh>Linux scripts</vh>
<v t="ekr.20031218072017.2579"><vh>@silentfile ../install</vh></v>
<v t="ekr.20031218072017.2580" tnodeList="ekr.20031218072017.2580"><vh>@silentfile ../uninstall</vh></v>
</v>
</v>
<v t="ekr.20031218072017.2581"><vh> Version stuff (update this for every release)</vh>
<v t="ekr.20031218072017.2582"><vh> version &amp; signon stuff</vh></v>
<v t="ekr.20031218072017.2571"><vh>&lt;&lt; setup info for setup.py &gt;&gt; UPDATE BY HAND (no spaces)</vh></v>
<v t="ekr.20031218072017.2563"><vh>@silentfile ../doc/PKG-INFO.TXT</vh></v>
<v t="ekr.20031218072017.2564"><vh>@silentfile ../doc/README.TXT</vh></v>
<v t="ekr.20031218072017.2583"><vh>Previous readme files</vh>
<v t="ekr.20031218072017.2584"><vh>4.0</vh></v>
<v t="ekr.20031218072017.2585"><vh>3.x</vh>
<v t="ekr.20031218072017.2586"><vh>3.12</vh></v>
<v t="ekr.20031218072017.2587"><vh>3.11</vh></v>
<v t="ekr.20031218072017.2588"><vh>3.10</vh></v>
<v t="ekr.20031218072017.2589"><vh>3.9</vh></v>
<v t="ekr.20031218072017.2590"><vh>3.8</vh></v>
<v t="ekr.20031218072017.2591"><vh>3.7</vh></v>
<v t="ekr.20031218072017.2592"><vh>3.6</vh></v>
<v t="ekr.20031218072017.2593"><vh>3.5</vh></v>
<v t="ekr.20031218072017.2594"><vh>3.4</vh></v>
<v t="ekr.20031218072017.2595"><vh>3.3</vh></v>
<v t="ekr.20031218072017.2596"><vh>3.2</vh></v>
<v t="ekr.20031218072017.2597"><vh>3.1</vh></v>
<v t="ekr.20031218072017.2598"><vh>3.0</vh></v>
</v>
<v t="ekr.20031218072017.2599"><vh>2.x</vh>
<v t="ekr.20031218072017.2600"><vh>2.5</vh></v>
<v t="ekr.20031218072017.2601"><vh>2.4</vh></v>
<v t="ekr.20031218072017.2602"><vh>2.3</vh></v>
<v t="ekr.20031218072017.2603"><vh>2.2</vh></v>
</v>
</v>
</v>
</v>
<v t="ekr.20031218072017.2604"><vh>Core classes...</vh>
<v t="ekr.20031218072017.2605"><vh>@file-thin leo.py </vh></v>
<v t="ekr.20031218072017.2608"><vh>@file-thin leoApp.py</vh></v>
<v t="ekr.20031218072017.2794"><vh>@file-thin leoColor.py</vh></v>
<v t="ekr.20031218072017.3001"><vh>@file-thin leoConfig.py</vh></v>
<v t="ekr.20031218072017.3052"><vh>@file-thin leoFind.py</vh></v>
<v t="ekr.20031218072017.3206"><vh>@file-thin leoImport.py</vh></v>
<v t="ekr.20031218072017.3439"><vh>@file-thin leoPlugins.py</vh></v>
<v t="ekr.20031218072017.3446"><vh>@file-thin leoTangle.py</vh></v>
</v>
<v t="ekr.20031218072017.3625"><vh>Gui Base classes</vh>
<v t="ekr.20031218072017.3626"><vh>@file-thin leoColorPanel.py</vh></v>
<v t="ekr.20031218072017.3630"><vh>@file-thin leoCompare.py</vh></v>
<v t="ekr.20031218072017.3652"><vh>@file-thin leoFontPanel.py</vh></v>
<v t="ekr.20031218072017.3655"><vh>@file-thin leoFrame.py</vh></v>
<v t="ekr.20031218072017.3719"><vh>@file-thin leoGui.py</vh></v>
<v t="ekr.20031218072017.3748"><vh>@file-thin leoKeys.py</vh></v>
<v t="ekr.20031218072017.3812"><vh>@file-thin leoPrefs.py</vh></v>
</v>
<v t="ekr.20031218072017.3821"><vh>Gui Tkinter classes</vh>
<v t="ekr.20031218072017.3822"><vh>@file-thin leoTkinterColorPanels.py</vh></v>
<v t="ekr.20031218072017.3838"><vh>@file-thin leoTkinterComparePanel.py</vh></v>
<v t="ekr.20031218072017.3858"><vh>@file-thin leoTkinterDialog.py</vh></v>
<v t="ekr.20031218072017.3897"><vh>@file-thin leoTkinterFind.py</vh></v>
<v t="ekr.20031218072017.3909"><vh>@file-thin leoTkinterFontPanel.py</vh></v>
<v t="ekr.20031218072017.4047"><vh>@file-thin leoTkinterGui.py</vh></v>
<v t="ekr.20031218072017.4099"><vh>@file-thin leoTkinterKeys.py</vh></v>
<v t="ekr.20031218072017.4100"><vh>@file-thin leoTkinterMenu.py</vh></v>
<v t="ekr.20031218072017.4122"><vh>@file-thin leoTkinterPrefs.py</vh></v>
</v>
<v t="ekr.20040312122501"><vh>Active</vh>
<v t="ekr.20031218072017.2620"><vh>@file-thin leoAtFile.py </vh></v>
<v t="ekr.20031218072017.2810"><vh>@file-thin leoCommands.py</vh></v>
<v t="ekr.20031218072017.3018"><vh>@file-thin leoFileCommands.py</vh></v>
<v t="ekr.20031218072017.3093"><vh>@file-thin leoGlobals.py</vh></v>
<v t="ekr.20031218072017.3749"><vh>@file-thin leoMenu.py</vh></v>
<v t="ekr.20031218072017.3320"><vh>@file-thin leoNodes.py</vh></v>
<v t="ekr.20031218072017.3939"><vh>@file-thin leoTkinterFrame.py</vh></v>
<v t="ekr.20031218072017.4138"><vh>@file-thin leoTkinterTree.py</vh></v>
<v t="ekr.20031218072017.3603"><vh>@file-thin leoUndo.py</vh></v>
</v>
</v>
</vnodes>
<tnodes>
<t tx="EKR.20040427074150"></t>
<t tx="EKR.20040429143933">@ This part of the tree shows views of the outline related to specific projects or tasks.  I put such headlines in parentheses, and that is just my convention.

I create a new view by cloning headlines that relate to its task, and moving the cloned headlines under the task headline.  This greatly increases my focus.  Any changes made in a task view to clone headlines affect the other clones scattered throughout the outline.  In particular, all @file nodes containing changed clones become marked as dirty, so they will be written when the entire outline is saved.
@c

@language python
@all</t>
<t tx="EKR.20040430162943"></t>
<t tx="EKR.20040502125334"></t>
<t tx="ekr.20031218072017">@nocolor

Older diary entries are in LeoDocs.leo.

@others</t>
<t tx="ekr.20031218072017.329">@nocolor

This contains my notes for the Leo project.

@all</t>
<t tx="ekr.20031218072017.2406">@language python
@pagewidth 80

@ This section contains all the source code of leo.py.

Leo's code uses the following conventions throughout:

c:  a commander
ch: a character
d:  a dialog or a dict.
g:  the leoGlobal module.
i, j, k: indices into a string
lst: a list (Do _not_ use list, it is a Python global!)
p:  a position.
s:  a string
t:  a tnode or a text widget.
u:  an undoer
v:  a vnode

See the child of this node called "Overview of Code" for more documentation.</t>
<t tx="ekr.20031218072017.2407">@nocolor
@ignore

This documentation describes leo.py. Other versions of Leo are similar in design; the differences between versions are generally not interesting enough to describe here.

All versions of Leo are organized as a collection of classes.  The general organization of Leo has remained remarkably stable throughout all versions of Leo, although the names of classes are different in different versions. Smalltalk's Model/View/Controller terminology is a good way to organize Leo's classes conceptually.

Model classes represent the fundamental data. The vnode and tnode classes are Leo's primary model classes.

View classes draw the screen. The main view classes are leoFrame.py and leoTree.py.  The colorizer class in leoColor.py handles syntax coloring in the body pane. In leo.py, the view classes know about data stored in the vnode class. Most events (keystrokes and mouse actions) in the outline and body pane are handled in the leoTree class. The leoFrame class also creates the Leo window, including menus, and dispatches the appropriate members of the controller classes in response to menu commands.

Controller classes (aka commanders) control the application. In Leo, controllers mostly handle menu commands. In leo.py, the Commands class creates subcommanders to handle complex commands. The atFile class reads and writes files derived from @file trees. The leoFind class handles the Find and Change commands. The leoImportCommands class handles the Import and Export commands, the tangleCommands class handles the Tangle and Untangle commands and the undoer class handles the Undo command. Other classes could be considered controller classes.

Each Leo window has its own commander and subcommanders. Subcommanders are not subclasses of their commander. Instead, subcommanders know the commander that created them, and call that commander as needed. Commanders and subcommanders call the model and view classes as needed. For example, the Commands class handles outline commands. To move a headline, the commander for the window calls a vnode move routine to alter the data, then calls the view class to redraw the screen based on the new data.

A global g.app represents the application itself. The ivars of the g.app object are the equivalent of Leo's global variables. leoGlobals.py defines all application constants and data structures.  Naturally, most constants are local to the class that uses them.

Several classes combine aspects of model, view and controller. For example, the LeoPrefs class represents user preferences (model), the Preference Panel (view) and the Preferences menu command (controller). Similarly, the leoFind class represents find settings, the Find/Change dialog, and the Find/Change commands.

The children of this node are clones of code-level documentation found throughout this code.</t>
<t tx="ekr.20031218072017.2408">@ This is the design document for clones in Leo. It covers all important aspects of clones. Clones are inherently complex, and this paper will include several different definitions of clones and related concepts.

The following is a definition of clones from the user's point of view.

Definition 1

A clone node is a copy of a node that changes when the original changes. Changes to the children, grandchildren, etc. of a node are simultaneously made to the corresponding nodes contained in all cloned nodes. Clones are marked by a small clone arrow by its leader character.

As we shall see, this definition glosses over a number of complications. Note that all cloned nodes (including the original node) are equivalent. There is no such thing as a "master" node from which all clones are derived. When the penultimate cloned node is deleted, the remaining node becomes an ordinary node again.

Internally, the clone arrow is represented by a clone bit in the status field of the vnode. The Clone Node command sets the clone bits of the original and cloned vnodes when it creates the clone. Setting and clearing clone bits properly when nodes are inserted, deleted or moved, is non-trivial. We need the following machinery to do the job properly.

Two vnodes are joined if a) they share the same tnode (body text) and b) changes to any subtree of either joined vnodes are made to the corresponding nodes in all joined nodes.  For example, Definition 1 defines clones as joined nodes that are marked with a clone arrow.  Leo links all vnodes joined to each other in a circular list, called the join list. For any vnode n, let J(n) denote the join list of n, that is, the set of all vnodes joined to n. Again, maintaining the join lists in an outline is non-trivial.

The concept of structurally similar nodes provides an effective way of determining when two joined nodes should also have their cloned bit set.  Two joined nodes are structurally similar if a) their parents are distinct but joined and b) they are both the nth child of their (distinct) parents.  We can define cloned nodes using the concept of structurally similar nodes as follows:

Definition 2

Clones are joined vnodes such that at least two of the vnodes of J(n) are not structurally similar to each other. Non-cloned vnodes are vnodes such that all of the vnodes of J(n) are structurally similar. In particular, n is a non-cloned vnode if J(n) is empty.

Leo ensures that definitions 1 and 2 are consistent. Definition 1 says that changes to the children, grandchildren, etc. of a node are simultaneously made to the corresponding nodes contained in all cloned nodes. Making "corresponding changes" to the non-cloned descendents of all cloned nodes insures that the non-cloned joined nodes will be structurally similar. On the other hand, cloned nodes are never structurally similar. They are created as siblings, so they have the same parent with different "child indices."  To see how this works in practice, let's look at some examples.

Example 1

+ root
	+ a' (1)
	+ a' (2)

This example shows the simplest possible clone. A prime (') indicates a cloned node.  Node a in position (1) has just been cloned to produce a' in position (2). Clearly, these two cloned nodes are not structurally similar because their parents are not distinct and they occupy different positions relative to their common parent.

Example 2

If we add a node b to either a' node we get the following tree:

+ root
	+ a'
		+ b
	+ a'
		+ b

The b nodes are structurally similar because the a' nodes are joined and each b node is the first child of its parent.

Example 3

If we now clone either b, we will get:

+ root
	+ a'
		+ b' (1)
		+ b' (2)
	+ a'
		+ b' (1)
		+ b' (2)

All b' nodes must be clones because the nodes marked (1) are not structurally similar to the nodes marked (2).

Dependent nodes are nodes created or destroyed when corresponding linked nodes are created or destroyed in another tree. For example, going from example 1 to example 2 above, adding node b to either node a' causes another (dependent) node to be created as the ancestor of the other node a'. Similarly, going from example 2 to example 1, deleting node b from either node a' causes the other (dependent) node b to be deleted from the other node a'.  Cloned nodes may also be dependent nodes. In Example 3, all the b' nodes are dependent on any of the other b' nodes.

We can now give simple rules for inserting and deleting dependent vnodes when other vnodes are created, moved or destroyed. For the purposes of this discussion, moving a node is handled exactly like deleting the node then inserting the node; we need not consider moving nodes further.  We insert a new node n as the nth child of a parent node p as follows. We insert n, then for every node pi linked to p, we insert a dependent node ni as the nth child of pi. Each ni is linked to n. Clearly, each ni is structurally similar to n.  Similarly, it is easy to delete a node n that is the nth child of a parent node p. We delete each dependent node ni that is the nth child of any node pi linked to p. We then delete n.  When inserting or deleting any vnode n we must update its join list, J(n). Updating the join list is easy because the join list is circular: the entire list is accessible from any of its members.

Inserting or deleting nodes can cause the clone bits of all joined nodes to change in non-trivial ways. To see the problems that can arise, consider deleting any of the b' nodes from Example 3. We would be left with the tree in Example 2. There are two remaining b nodes, each with the clone bit set. Unless we know that both b nodes are structurally similar, there would be no way to conclude that we should clear the clone bits in each node. In order to update clone links properly we could examine many special cases, but there is an easier way. Because of definition 2, we can define a shouldBeCloned function that checks J(n) to see whether all nodes of J(n) are structurally similar.

Leo's XML file format does not contain join lists. This makes it easy to change a Leo file "by hand." If join lists were a part of the file, as they are in the Mac version of Leo, corrupting a join list would corrupt the entire file. It is easy to recreate the join lists when reading a file using a dedicated field in the tnode.  This field is the head of a list of all vnodes that points to the tnode. After reading all nodes, Leo creates this list with one pass through the vnodes.  Leo then converts each list to a circular list with one additional pass through the tnodes.
</t>
<t tx="ekr.20031218072017.2409">@ Leo must redraw the outline pane when commands are executed and as the result of mouse and keyboard events.  The main challenges are eliminating flicker and handling events properly.

Eliminating flicker.  Leo must update the outline pane with minimum flicker.  Various versions of Leo have approached this problem in different ways.  The drawing code in leo.py is robust, flexible, relatively simple and should work in almost any conceivable environment.

Leo assumes that all code that changes the outline pane will be enclosed in matching calls to the c.beginUpdate and c.endUpdate  methods of the Commands class. c.beginUpdate() inhibits drawing until the matching c.endUpdate().  These calls may be nested; only the outermost call to c.endUpdate() calls c.redraw() to force a redraw of the outline pane.

In leo.py, code may call c.endUpdate(flag) instead of c.endUpdate().  Leo redraws the screen only if flag is true.  This allows code to suppress redrawing entirely when needed.  For example, study the idle_body_key event handler to see how Leo conditionally redraws the outline pane.

The leoTree class redraws all icons automatically when c.redraw() is called.  This is a major simplification compared to previous versions of Leo.  The entire machinery of drawing icons in the vnode class has been eliminated.  The v.computeIcon method tells what the icon should be.  The v.iconVal ivar that tells what the present icon is. The event handler simply compares these two values and sets redraw_flag if they don't match.</t>
<t tx="ekr.20031218072017.2410">@ Leo must handle events or commands that change the text in the outline or body panes.  It is surprisingly difficult to ensure that headline and body text corresponds to the vnode and tnode corresponding to presently selected outline, and vice versa. For example, when the user selects a new headline in the outline pane, we must ensure that 1) the vnode and tnode of the previously selected node have up-to-date information and 2) the body pane is loaded from the correct data in the corresponding tnode.

Early versions of Leo attempted to satisfy these conditions when the user switched outline nodes.  Such attempts never worked well; there were too many special cases.  Later versions of Leo, including leo.py, use a much more direct approach.  The event handlers make sure that the vnode and tnode corresponding to the presently selected node are always kept up-to-date.  In particular, every keystroke in the body pane causes the presently selected tnode to be updated immediately.  There is no longer any need for the c.synchVnode method.  (That method still exists for compatibility with old scripts.)

The leoTree class contains all the event handlers for the tree pane, and the leoBody class contains the event handlers for the body pane.  The actual work is done in the idle_head_key and idle_body_key methods.  These routines are surprisingly complex; they must handle all the tasks mentioned above, as well as others. The idle_head_key and idle_body_key methods should not be called outside their respective classes.  However, sometimes code in the Commands must simulate an event.  That is, the code needs to indicate that headline or body text has changed so that the screen may be redrawn properly.   The leoBody class defines the following simplified event handlers: onBodyChanged, onBodyWillChange and onBodyKey. Similarly, the leoTree class defines onHeadChanged and onHeadlineKey.  Commanders and subcommanders call these event handlers to indicate that a command has changed, or will change, the headline or body text.  Calling event handlers rather than c.beginUpdate and c.endUpdate ensures that the outline pane is redrawn only when needed.
</t>
<t tx="ekr.20031218072017.2411">@ The Tangle command translates the selected @root tree into one or more well-formatted C source files. The outline should contain directives, sections references and section definitions, as described in Chapter 4. The Untangle command is essentially the reverse of the Tangle command. The Tangle command creates a derived file from an @root tree; the Untangle command incorporates changes made to derived files back into the @root tree.

The Tangle command operates in two passes. The first pass discovers the complete definitions of all sections and places these definitions in a symbol table. The first pass also makes a list of root sections. Definitions can appear in any order, so we must scan the entire input file to know whether any particular definition has been completed.

Tangle's second pass creates one file for each @root node. Tangle rescans each section in the list of roots, copying the root text to the output and replacing each section reference by the section's definition. This is a recursive process because any definition may contain other references. We can not allow a section to be defined in terms of itself, either directly or indirectly. We check for such illegally recursive definitions in pass 2 using the section stack class.  Tangle indicates where sections begin and end using comment lines called sentinel lines.  The this part of the appendix discusses the format of the sentinels output by the Tangle command.

The key design principle of the Tangle command is this: Tangle must output newlines in a context-free manner. That is, Tangle must never output conditional newlines, either directly or indirectly. Without this rule Untangle could not determine whether to skip or copy newlines.

The Tangle command increases the indentation level of a section expansion the minimum necessary to align the section expansion with the surrounding code. In essence, this scheme aligns all section expansions with the line of code in which the reference to the section occurs. In some cases, several nested sections expansions will have the same indentation level. This can occur, for example, when a section reference in an outline occurs at the left margin of the outline.

This scheme is probably better than more obvious schemes that indent more "consistently." Such schemes would produce too much indentation for deeply nested outlines. The present scheme is clear enough and avoids indentation wherever possible, yet indents sections adequately. End sentinel lines make this scheme work by making clear where the expansion of one section ends and the expansion of a containing section resumes.

Tangle increases indentation if the section reference does not start a line. Untangle is aware of this hack and adjusts accordingly. This extra indentation handles several common code idioms, which otherwise would create under-indented code. In short, Tangle produces highly readable, given the necessity of preserving newlines for Untangle.

Untangle is inherently complex.  It must do a perfect job of updating the outline, especially whitespace, from expansions of section definitions created by the Tangle command.  Such expansions need not be identical because they may have been generated at different levels of indentation.  The Untangle command can not assume that all expansions of a section will be identical in the derived file; within the derived file, the programmer may have made incompatible changes to two different expansions of the same section. Untangle must check to see that all expansions of a section are "equivalent".  As an added complication, derived files do not contain all the information found in @root trees.  @root trees may contain headlines that generate no code at all.  Also, an outline may define a section in several ways: with an @c or @code directive or with a section definition line.  To be useful, Untangle must handle all these complications flawlessly. The appendix discusses the various conventions used in the sentinels output by the Tangle command.  These conventions allow the Untangle command to recreate whitespace correctly.

Untangle operates in two passes. The first pass finds definitions in the derived file and enters them into the Untangle Symbol Table, or UST.   Definitions often include references to other sections, so definitions often include nested definitions of referenced sections. The first pass of Untangle uses a definition stack to keep track of nested definitions. The top of the stack represents the definition following the latest reference, except for the very first entry pushed on the stack, which represents the code in the outline that contains the @root directive. The stack never becomes empty because of the entry for the @root section. All definitions of a section should match--otherwise there is an inconsistent definition. This pass uses a forgiving compare routine that ignores differences that do not affect the meaning of a program.

Untangle's second pass enters definitions from the outline into the Tangle Symbol Table, or TST. The second pass simultaneously updates all sections in the outline whose definition in the TST does not match the definition in the UST.  The central coding insight of the Untangle command is that the second pass of Untangle is almost identical to the first pass of Tangle! That is, Tangle and Untangle share key parts of code, namely the skip_body() method and its allies.  Just when skip_body() enters a definition into the symbol table, all the information is present that Untangle needs to update that definition.
</t>
<t tx="ekr.20031218072017.2412">@ The vnode and tnode classes represent most of the data contained in the outline. These classes are Leo's fundamental Model classes.

A vnode (visual node) represents a headline at a particular location on the screen. When a headline is cloned, vnodes must be copied. vnodes persist even if they are not drawn on the screen. Commanders call vnode routines to insert, delete and move headlines.

The vnode contains data associated with a headline, except the body text data which is contained in tnodes. A vnode contains headline text, a link to its tnode and other information. In leo.py, vnodes contain structure links: parent, firstChild, next and back ivars. To insert, delete, move or clone a vnode the vnode class just alters those links. The Commands class calls the leoTree class to redraw the outline pane whenever it changes. The leoTree class knows about these structure links; in effect, the leoTree and vnode classes work together. The implementation of vnodes is quite different in the Borland version of Leo. This does not affect the rest of the Leo. Indeed, vnodes are designed to shield Leo from such implementation details.

A tnode, (text node) represents body text: a tnode is shared by all vnodes that are clones of each other. In other words, tnodes are the unit of sharing of body text. The tnode class is more private than the vnode class. Most commanders deal only with vnodes, though there are exceptions.

Because leo.py has unlimited Undo commands, vnodes and tnodes can be deleted only when the window containing them is closed. Nodes are deleted indirectly.

Leo uses several kinds of node indices. Leo's XML file format uses tnode indices to indicate which tnodes (t elements) belong to which vnodes (v elements). Such indices are required. Even if we duplicated the body text of shared tnodes within the file, the file format would still need an unambiguous way to denote that tnodes are shared.

Present versions of Leo recompute these tnodes indices whenever Leo writes any .leo file. Earlier versions of Leo remembered tnode indices and rewrote the same indices whenever possible. Those versions of Leo recomputed indices when executing the Save As and Save To commands, so using these commands was a way of "compacting" indices. The main reason for not wanting to change tnode indices in .leo files was to reduce the number of changes reported by CVS and other Source Code Control Systems. I finally abandoned this goal in the interest of simplifying the code. Also, CVS will likely report many differences between two versions of the same .leo file, regardless of whether tnode indices are conserved.

A second kind of node index is the clone index used in @+node sentinels in files derived from @file trees. As with indices in .leo files, indices in derived files are required so that Leo can know unambiguously which nodes are cloned to each other.

It is imperative that clone indices be computed correctly, that is, that tnode @+node sentinels have the same index if and only if the corresponding vnodes are cloned. Early versions of leo.py had several bugs involving these clone indices. Such bugs are extremely serious because they corrupt the derived file and cause read errors when Leo reads the @file tree. Leo must guarantee that clone indices are always recomputed properly. This is not as simple as it might appear at first. In particular, Leo's commands must ensure that @file trees are marked dirty whenever any changed is made that affects cloned nodes within the tree. For example, a change made outside any @file tree may make several @file trees dirty if the change is made to a node with clones in those @file trees.
</t>
<t tx="ekr.20031218072017.2413">@ Only leo.py supports unlimited undo.  Unlimited undo is straightforward; it merely requires that all commands that affect the outline or body text must be undoable. In other words, everything that affects the outline or body text must be remembered.

We may think of all the actions that may be Undone or Redone as a string of beads (undo nodes). Undoing an operation moves backwards to the next bead; redoing an operation moves forwards to the next bead. A bead pointer points to the present bead. The bead pointer points in front of the first bead when Undo is disabled.  The bead pointer points at the last bead when Redo is disabled. An undo node is a Python dictionary containing all information needed to undo or redo the operation.

The Undo command uses the present bead to undo the action, then moves the bead pointer backwards. The Redo command uses the bead after the present bead to redo the action, then moves the bead pointer forwards. All undoable operations call setUndoParams() to create a new bead. The list of beads does not branch; all undoable operations (except the Undo and Redo commands themselves) delete any beads following the newly created bead.

I did not invent this model of unlimited undo.  I first came across it in the documentation for Apple's Yellow Box classes.
</t>
<t tx="ekr.20031218072017.2414">@ The find and change commands are tricky; there are many details that must be handled properly. This documentation describes the leo.py code. Previous versions of Leo used an inferior scheme.  The following principles govern the leoFind class:

1.	Find and Change commands initialize themselves using only the state of the present Leo window. In particular, the Find class must not save internal state information from one invocation to the next. This means that when the user changes the nodes, or selects new text in headline or body text, those changes will affect the next invocation of any Find or Change command. Failure to follow this principle caused all kinds of problems in the Borland and Macintosh codes. There is one exception to this rule: we must remember where interactive wrapped searches start. This principle simplifies the code because most ivars do not persist. However, each command must ensure that the Leo window is left in a state suitable for restarting the incremental (interactive) Find and Change commands. Details of initialization are discussed below.

2. The Find and Change commands must not change the state of the outline or body pane during execution. That would cause severe flashing and slow down the commands a great deal. In particular, c.selectVnode and c.editPosition methods must not be called while looking for matches.

3. When incremental Find or Change commands succeed they must leave the Leo window in the proper state to execute another incremental command. We restore the Leo window as it was on entry whenever an incremental search fails and after any Find All and Change All command.

Initialization involves setting the self.c, self.v, self.in_headline, self.wrapping and self.s_text ivars. Setting self.in_headline is tricky; we must be sure to retain the state of the outline pane until initialization is complete. Initializing the Find All and Change All commands is much easier because such initialization does not depend on the state of the Leo window.

Using Tk.Text widgets for both headlines and body text results in a huge simplification of the code. Indeed, the searching code does not know whether it is searching headline or body text. The search code knows only that self.s_text is a Tk.Text widget that contains the text to be searched or changed and the insert and sel Tk attributes of self.search_text indicate the range of text to be searched. Searching headline and body text simultaneously is complicated. The selectNextVnode() method handles the many details involved by setting self.s_text and its insert and sel attributes.
</t>
<t tx="ekr.20031218072017.2415">@language python
@ignore

@ This section contains scripts and other files for creating, testing and distributing leo.py.  leo.py itself does not use any of the code in these scripts, nor do these scripts use any code in leo.py.
@c

# To convert from C to Python, do the following from Leo's Python window:
import c2py
c2py.convertCurrentTree()

# To convert from Leo1 to Leo2, do the following from Leo's Python window:
import c2py
c2py.leo1to2()

@  To create a source distribution using Python's distutils:

On windows: do the following from inside a console window:
	cd c:\prog\LeoPy
	sdist

On Linux do the following:
	cd LeoPy
	python setup.py sdist --force-manifest --formats=gztar,zip</t>
<t tx="ekr.20031218072017.2416"># Note:  the initScriptFind script makes setting up Find/Change scripts very easy.</t>
<t tx="ekr.20031218072017.2417">def doChangeScript (self):

	g.app.searchDict["type"] = "change"
	self.runChangeScript()

def doChangeAllScript (self):

	"""The user has just pressed the Change All button with script-change box checked.

	N.B. Only this code is executed."""

	g.app.searchDict["type"] = "changeAll"
	while 1:
		self.runChangeScript()
		if not g.app.searchDict.get("continue"):
			break

def runChangeScript (self):

	c = self.c
	try:
		assert(c.script_change_flag) # 2/1/04
		exec c.change_text in {} # Use {} to get a pristine environment.
	except:
		g.es("exception executing change script")
		g.es_exception(full=false)
		g.app.searchDict["continue"] = false # 2/1/04</t>
<t tx="ekr.20031218072017.2418">def initScriptFind(findHeadline,changeHeadline=None,firstNode=None,
	script_search=true,script_change=true):
	
	import leoTest
	import leoGlobals as g
	from leoGlobals import true,false
	
	# Find the scripts.
	c = g.top() ; p = c.currentPosition()
	u = leoTest.testUtils()
	find_p = u.findNodeInTree(p,findHeadline)
	if find_p:
		find_text = find_p.bodyString()
	else:
		g.es("no Find script node",color="red")
		return
	if changeHeadline:
		change_p = u.findNodeInTree(p,changeHeadline)
	else:
		change_p = None
	if change_p:
		change_text = change_p.bodyString()
	else:
		change_text = ""
	# print find_p,change_p
	
	# Initialize the find panel.
	c.script_search_flag = script_search
	c.script_change_flag = script_change and change_text
	if script_search:
		c.find_text = find_text.strip() + "\n"
	else:
		c.find_text = find_text
	if script_change:
		c.change_text = change_text.strip() + "\n"
	else:
		c.change_text = change_text
	g.app.findFrame.init(c)
	c.findPanel()</t>
<t tx="ekr.20031218072017.2419"># Initialize Leo's find panel using the named children of this node.
import leoGlobals as g
from leoGlobals import true,false

g.app.searchDict = {} # Clear dict.get("v") logic.
g.initScriptFind("Find script","Change script")

c = g.top()
c.selectVnode(c.rootPosition())
c.redraw()</t>
<t tx="ekr.20031218072017.2420">import leoGlobals as g
from leoGlobals import true,false

c = g.top() ; v = c.currentVnode() ; d = g.app.searchDict
findAll = d.get("type") == "findAll"

if findAll and c.suboutline_only_flag:
	after = v.nodeAfterTree()
else:
	after = None

found = false ; count = 0
while v and v != after and not found:
	s = v.bodyString()
	lines = s.split('\n')
	for line in lines:
		if line and not line.strip():
			if findAll:
				g.es(v.headString()) ; count += 1
			else:
				c.frame.tree.expandAllAncestors(v)
				c.selectVnode(v)
				c.redraw() # Necessary to make the new node visible.
				if not findAll:
					g.es("found node with whitespace to clean")
				found = true 
			break
	v = v.threadNext()

if not found:
	if findAll:
		g.es("found %d nodes" % (count), color="blue")
	else:
		g.es("not found")
</t>
<t tx="ekr.20031218072017.2421">import leoGlobals as g
from leoGlobals import true,false

c = g.top() ; d = g.app.searchDict
changeAll = d.get("type") == "changeAll"
count = d.get("count",0)
if changeAll:
	v = d.get("v")
	if v:
		v = v.threadNext()
		after = d.get("after")
		if v == after: v = None
	else:
		v = c.currentVnode()
		d["count"] = 0
		after = g.choose(c.suboutline_only_flag,v.nodeAfterTree(),None)
		d["after"] = after
	d["v"] = v ; d["continue"] = v != None
else:
	v = c.currentVnode()

if v:
	s = oldText = v.bodyString()
	lines = s.split('\n')
	lines = [line.rstrip() for line in lines]
	s = '\n'.join(lines)
	if s != oldText:
		v.setBodyStringOrPane(s,encoding=g.app.tkEncoding)
		if changeAll:
			g.es(v.headString()) ; d["count"] = count + 1
		else:
			c.frame.body.onBodyChanged(v,"Change",oldText=oldText) # Handles undo.
			c.frame.body.setInsertPointToStartOfLine(0)
else:
	if changeAll:
		g.es("found %d nodes" % (count), color="blue")
	else:
		g.es("done")</t>
<t tx="ekr.20031218072017.2422"># Initialize Leo's find panel using the named children of this node.
import leoGlobals as g
from leoGlobals import true,false

g.app.searchDict = {} # Clear dict.get("v") logic.
g.initScriptFind("Find script","Change script")

# Start searching at the top.
c = g.top()
c.selectVnode(c.rootPosition())</t>
<t tx="ekr.20031218072017.2423">import leoGlobals as g
from leoGlobals import true,false

import re

docPart = re.compile("""^(@$|@ |@doc)(.*)$
^@c[ \t]*(.*?)$
^(def[ \t]*.*?:.*?)$
(.*)""", re.MULTILINE | re.DOTALL)

c = g.top() ; d = g.app.searchDict
v = c.currentVnode()
# Move past previously matched node.
last_v = d.get("v")
if last_v:
	if v == last_v: v = last_v.threadNext()
	d["v"] = None
d["m"] = None ; d["c"] = c
while v:
	m = docPart.match(v.bodyString())
	if m:
		d["m"] = m ; d["v"] = v
		c.frame.tree.expandAllAncestors(v)
		c.selectVnode(v)
		c.redraw() # Necessary to make the new node visible.
		break
	v = v.threadNext()
if not d.get("v"):
	g.es("no @doc part found",color="blue")</t>
<t tx="ekr.20031218072017.2424">import leoGlobals as g
from leoGlobals import true,false

def replaceDocPart(m,body):
	# Warning: m.group(0) is the _whole_ match.
	directive = m.group(1)
	doc = m.group(2)
	blanks = m.group(3).strip()
	if blanks: blanks += "\n\n"
	else: blanks = ""
	defLine = m.group(4)
	rest = m.group(5)
	docList = doc.split('\n')
	doc = string.join(docList,"\n\t")
	if body.hasTextSelection():  # If text is selected only that text becomes the doc part.
		sel = body.getSelectedText()
		i = doc.find(sel)
		if i &gt; -1:
			doc = doc[:i] + doc[i + len(sel):] # Remove selected text.
			return directive + doc.rstrip() + "\n@c\n\n" + defLine + '\n\n\t"""' + sel + '"""\n' + rest
		else:
			g.es("selection should be in @doc part")
			return None # This disables any replacement.
	else:
		return blanks + defLine + '\n\n\t"""' + doc.strip() + '"""\n' + rest
		
d = g.app.searchDict ; c = d.get("c") ; v = d.get("v") ; m = d.get("m")
if c and v and m:
	body = c.frame.body
	oldText = v.bodyString()
	s = replaceDocPart(m,body)
	if s: # Don't make a replacement if there was an error.
		v.setBodyStringOrPane(s,encoding=g.app.tkEncoding)
		body.onBodyChanged(v,"Change",oldText=oldText) # Handles undo.</t>
<t tx="ekr.20031218072017.2425">import leoGlobals as g
from leoGlobals import true,false
import re

s = """@doc line 0
line 1d
line 2
@c

# a comment

def abc(self): xx

after 1
after 2"""

pat = re.compile("""^(@$|@ |@doc)(.*?)$
^@c[ \t]*(.*?)$
^(def[ \t]*.*?:.*?)$
(.*)""", re.MULTILINE | re.DOTALL)

m = pat.match(s)
print "---"
if m:
	print "doc:   ", m.group(2).strip()
	print "blanks:", m.group(3).strip()
	print "def:   ", m.group(4).strip()
	print "rest:  ", m.group(5).strip()
else:
	print "no match"
</t>
<t tx="ekr.20031218072017.2426"># This script was a breakthrough.
# Executing this script initializes the Find text from the given script string.
# To do: get the script from a named child of this node.
import leoGlobals as g
from leoGlobals import true,false

script = """
import leoGlobals as g
from leoGlobals import true,false
c = g.top() ; v = c.currentVnode()
print v
v = v.threadNext()
c.selectVnode(v)"""

g.app.searchDict = {} # Communication between search &amp; change scripts
c = g.top()
c.script_search_flag = true
c.find_text = script
g.app.findFrame.init(c)
c.frame.OnFindPanel()</t>
<t tx="ekr.20031218072017.2427">if 0: # Script to change OnXxx to xxx in all headlines
	import leoGlobals as g
	from leoGlobals import true,false

	c = g.top() ; v = c.currentVnode()
	after = v.nodeAfterTree()
	while v and v != after:
		h = v.headString()
		if g.match(h,0,"On") and len(h) &gt; 2:
			h = h[2].lower() + h[3:]
			print h
			v.setHeadString(h)
		v = v.threadNext()
		
# Script to change OnXXX to xxx in all body text.
if 0:
	import leoGlobals as g
	from leoGlobals import true,false

	c = g.top() ; v = c.currentVnode()
	after = v.nodeAfterTree()
	while v and v != after:
		s = v.bodyString()
		if s:
			i = s.find("def ")
			if i &gt; -1:
				c = s[i+6].lower()
				s = s[:i] + "def " + c + s[i+7:]
				print v.headString()
				v.setBodyStringOrPane(s)
		v = v.threadNext()</t>
<t tx="ekr.20031218072017.2428"># Script to change OnXXX to xxx in all body text.
if 0:
	import leoGlobals as g
	from leoGlobals import true,false

	c = g.top() ; v = c.currentVnode()
	v = v.threadNext()
	after = v.nodeAfterTree()
	count = 0
	while v and v != after:
		while 1:
			s = v.bodyString()
			if not s: break
			i = s.find("c.On")
			if i == -1: break
			c = s[i+4].lower()
			s = s[:i] + 'c.' + c + s[i+5:]
			v.setBodyStringOrPane(s)
			count += 1
		v = v.threadNext()
	print count</t>
<t tx="ekr.20031218072017.2429">import leoGlobals as g
from leoGlobals import true,false

import leoTest

u = leoTest.testUtils()
nodes = 0 ; lines = 0
c = g.top()
c.clearAllVisited()
if 0:
	v = u.findNodeAnywhere(c,"Code")
else:
	root = u.findRootNode (c.currentVnode())
	v = u.findNodeInTree(root,"Code")

after = v.nodeAfterTree()
# g.trace(v,after)

while v and v != after:
	if not v.t.isVisited():
		v.t.setVisited()
		nodes += 1
		lines += len(g.splitLines(v.bodyString()))
	v = v.threadNext()
	
pages = ((nodes * 10) + lines) / 60
print "nodes,lines,pages",nodes,lines,pages
g.es("nodes,lines,pages",nodes,lines,pages)</t>
<t tx="ekr.20031218072017.2431"></t>
<t tx="ekr.20031218072017.2432">import leoGlobals as g
from leoGlobals import true,false

c = g.top()
v = c.rootVnode()
while v:
	# 12/13/03: Empty tnodeLists are not errors because they never get written to the .leo file.
	# New in 4.2: tnode list is in tnode.
	if hasattr(v.t,"tnodeList") and len(v.t.tnodeList) &gt; 0 and not v.isAnyAtFileNode():
		g.es("deleting tnodeList for ",v,color="blue")
		delattr(v.t,"tnodeList")
		c.setChanged(true)
	v = v.threadNext()
g.es("tnodeList script complete")</t>
<t tx="ekr.20031218072017.2433">import leoGlobals as g
from leoGlobals import true,false

g.checkTopologyOfAllClones()</t>
<t tx="ekr.20031218072017.2434">if 0:
	checkForMismatchedJoinedNodes()
	
	print g.createTopologyList(c=g.top(),root=g.top().currentVnode().parent(),useHeadlines=false)
	
	checkTopologiesOfLinkedNodes()
	
	checkForPossiblyBrokenLinks()</t>
<t tx="ekr.20031218072017.2435">def checkForMismatchedJoinedNodes (c=None):
	
	"""Checks outline for possible broken join lists"""

	if not c: c = g.top()
	d = {} # Keys are tnodes, values are headlines.
	v = c.rootVnode()
	while v:
		aTuple = d.get(v.t)
		if aTuple:
			head,body = aTuple
			if v.headString()!= head:
				g.es("headline mismatch in joined nodes",v)
			if v.bodyString()!= body:
				g.es("body mismatch in joined nodes",v)
		else:
			d[v.t] = (v.headString(),v.bodyString())
		v = v.threadNext()

	g.es("end of checkForMismatchedJoinedNodes")
</t>
<t tx="ekr.20031218072017.2436">def checkForPossiblyBrokenLinks (c=None):
	
	"""Checks outline for possible broken join lists"""
	
	if not c: c = g.top()
	d = {} # Keys are headlines, values are (tnodes,parent) tuples
	v = c.rootVnode()
	while v:
		h = v.headString()
		parent = v.parent()
		aTuple = d.get(h)
		if aTuple:
			t,p = aTuple
			if (t != v.t and p and parent and p.t != parent.t and
				p.headString() == parent.headString() and
				len(h) &gt; 1 and h != "NewHeadline"):
				g.es("different tnodes with same headline and parent headlines: " + v.headString())
		else:
			d[h] = (v.t,parent)
		v = v.threadNext()
</t>
<t tx="ekr.20031218072017.2437">def checkTopologiesOfLinkedNodes(c=None):
	
	if not c: c = g.top()
	d = {} # Keys are tnodes, values are topology lists.
	v = c.rootVnode()
	count = 0
	while v:
		top1 = g.createTopologyList(c=c,root=v)
		top2 = d.get(v.t)
		if top2:
			count += 1
			if top1 != top1:
				g.es("mismatched topologies for two vnodes with the same tnode!",v)
		else:
			d[v.t] = top1
		v = v.threadNext()
	g.es("end of checkTopologiesOfLinkedNodes. Checked %d nodes: " % count)</t>
<t tx="ekr.20031218072017.2438">@ Nodes with the same topologies should be joined PROVIDED:
	- Topologies are non-trivial.
	- Topologies include tnodes somehow.
	- Topologies include headlines somehow.
</t>
<t tx="ekr.20031218072017.2439">@ignore</t>
<t tx="ekr.20031218072017.2440">@first #!/usr/bin/python

"""
A simple script to install Leo on Linux.

Contributed by David McNab &lt;david@rebirthing.co.nz&gt;
"""

import commands,os,sys # commands module is for Unix only.

# We must be root to use this script.
if os.getuid() != 0:
	print "You need to run this install script as root"
	sys.exit(1)

# Create /usr/lib/leo and copy all files there.
print "***** Installing Leo to /usr/lib/leo..."
commands.getoutput("mkdir -p /usr/lib/leo")
commands.getoutput("cp -rp * /usr/lib/leo")

# Create user's 'leo' command script into /usr/bin/leo
print "***** Creating Leo startup script -&gt; /usr/bin/leo"
fd = open("/usr/bin/leo", "w")
fd.write("""#!/usr/bin/python
import commands,sys
files = " ".join(sys.argv[1:])
print commands.getoutput("python /usr/lib/leo/leo.py %s" % files)
""")
fd.close()
commands.getoutput("chmod 755 /usr/bin/leo")
print "***** Leo installed successfully - type 'leo filename.leo' to use it."
</t>
<t tx="ekr.20031218072017.2441">import fnmatch, os

def findDosFile(pattern, dirname):
	
	"""Check for crlf in files"""
	
	from leoGlobals import os_path_isfile,os_path_join

	files = os.listdir(dirname)
	names = fnmatch.filter(files, pattern)
	for name in names:
		path = g.os_path_join(dirname, name)
		if g.os_path_isfile(path):
			bytes = open(path, 'rb').read()
			count = bytes.count('\r\n')
			if '\0' not in bytes and count:
				print "%4d %s" % (count,path)

dir = "c:\prog\leoCvs\leo"
print ; findDosFile("*",dir)

# The following files were reported:  MANIFEST, PKG-INFO.
# Both were created by @silentfile.</t>
<t tx="ekr.20031218072017.2442">@first #! /usr/bin/env python
@language python

@ When using c2py as a script to translate entire files, use convertCFileToPython().  When using c2py within Leo, use convertCurrentTree().

Please set user data in the &lt;&lt; specifying user types &gt;&gt; section.
@c

&lt;&lt; what c2py does &gt;&gt;
&lt;&lt; theory of operation &gt;&gt;
import string
&lt;&lt; specifying user types &gt;&gt;
true = 1 ; false = None
tabWidth = 4 # how many blanks in a tab.
printFlag = false
doLeoTranslations = true ; dontDoLeoTranslations = false
&lt;&lt; define testData &gt;&gt;
@others

gClassName = "" # The class name for the present function.  Used to modify ivars.
gIvars = [] # List of ivars to be converted to self.ivar

def test():
	global printFlag ; printFlag = true
	for s in testData:
		convertCStringToPython(s, doLeoTranslations)
		
def go():
	test()

if __name__ == "__main__":
	speedTest(2)</t>
<t tx="ekr.20031218072017.2443"></t>
<t tx="ekr.20031218072017.2444">@ c2py converts C or C++ text into python text.  The conversion is not complete.  Nevertheless, c2py eliminates much of the tedious text manipulation that would otherwise be required.

The following is a list of the translations performed by c2py.  These transformations are controlled by convertCodeList().

I.  Prepass

These translations before removing all curly braces.

Suppose we are translating:

	aTypeSpec aClass::aMethod(t1 v1,...,tn vn)
	{
		body
	}

1. Translates the function prototype, i.e., translates:

	aTypeSpec aClass::aMethod(t1 v1,...,tn vn)
to:
	def aMethod(v1,...vn):

As a special case, c2py translates:

	aTypeSpec aClass::aClass(t1 v1,...,tn vn)
to:
	aClass.__init__(t1 v1,...,tn vn)

Yes, I know, aClass.__init__ isn't proper Python, but retaining the class name is useful.

2. Let t denote any member of typeList or classList.

	a) Removes all casts of the form (t) or (t*) or (t**), etc.
	b) Converts t x, t *x, t **x, etc. to x.
	c) Converts x = new t(...) to x = t(...)
	d) For all i in ivarsDict[aClass] converts this -&gt; i to self.i
	e) For all i in ivarsDict[aClass] converts i to self.i

3. Converts &lt; &lt; x &gt; &gt; = to @c.  This Leo-specific translation is not done when translating files.

II.  Main Pass

This pass does the following simple translations everywhere except in comments and strings.

Changes all -&gt; to .
Changes all this.self to self (This corrects problems during the prepass.)
Removes all curly braces
Changes all #if to if
Changes all else if to elif
Changes all #else to else:
Changes all else to else:
Removes all #endif
Changes all &amp;&amp; to and
Changes all || to or
Changes all TRUE to true
Changes all FALSE to false
Changes all NULL to None
Changes all this to self
Changes all @code to @c.  This Leo-specific translation is not done when translating files.

III.  Complex Pass

This pass attempts more complex translations.

Converts if ( x ) to if x:
Converts elif ( x ) to elif x:
Converts while ( x ) to while x:
Converts for ( x ; y ; z ) to for x SEMI y SEMI z:

remove all semicolons.

IV.  Final Pass

This pass completes the translation.

Removes all semicolons.
Removes @c if it starts the text.  This Leo-specific translation is not done when translating files.
Removes all blank lines.
Removes excess whitespace from all lines, leaving leading whitespace unchanged.
Replaces C/C++ comments by Python comments.
Removes trailing whitespace from all lines.
</t>
<t tx="ekr.20031218072017.2445">@ Strategy and Performance

c2py is straightforward.  The speed of c2py is unimportant.  We don't care about the memory used because we translate only small pieces of text at a time.

We can do body[i:j] = x, regardless of len(x).  We can also do del body[i:j] to delete characters.

We scan repeatedly through the text.  Using many passes greatly simplifies the code and does not slow down c2py significantly.

No scans are done within strings or comments.  The idiom to handle such scans is the following:

def someScan(body):
	i = 0
	while i &lt; body(len):
		if isStringOrComment(body,i):
			i = skipStringOrComment(body,i)
		elif &lt;&lt; found what we are looking for ? &gt;&gt; :
			&lt;&lt; convert what we are looking for, setting i &gt;&gt;
		else: i += 1

That's about all there is to it.  The code was remarkably easy to write and seems clear to me.
</t>
<t tx="ekr.20031218072017.2446">@ Please change the following lists so they contain the types and classes used by your program.

c2py removes all type definitions correctly; it converts
	new aType(...)
to
	aType(...)
@c

classList = [
	"vnode", "tnode", "Commands",
	"wxString", "wxTreeCtrl", "wxTextCtrl", "wxSplitterWindow" ]
	
typeList = ["char", "void", "short", "long", "int", "double", "float"]

@ Please change ivarsDict so it represents the instance variables (ivars) used by your program's classes.

ivarsDict is a dictionary used to translate ivar i of class c to self.i.  It also translates this-&gt;i to self.i.
@c
	
ivarsDict = {
	"atFile": [ "mCommands", "mErrors", "mStructureErrors",
		"mTargetFileName", "mOutputFileName", "mOutputStream",
		"mStartSentinelComment", "mEndSentinelComment", "mRoot"],

	"vnode": ["mCommands", "mJoinList", "mIconVal", "mTreeID", "mT", "mStatusBits"],

	"tnode": ["mBodyString", "mBodyRTF", "mJoinHead", "mStatusBits", "mFileIndex",
		"mSelectionStart", "mSelectionLength", "mCloneIndex"],
		
	"LeoFrame": ["mNextFrame", "mPrevFrame", "mCommands"],

	"Commands": [
		# public
		"mCurrentVnode", "mLeoFrame", "mInhibitOnTreeChanged", "mMaxTnodeIndex",
		"mTreeCtrl", "mBodyCtrl", "mFirstWindowAndNeverSaved",
		#private
		"mTabWidth", "mChanged", "mOutlineExpansionLevel", "mUsingClipboard",
		"mFileName", "mMemoryInputStream", "mMemoryOutputStream", "mFileInputStream",
		"mInputFile", "mFileOutputStream", "mFileSize", "mTopVnode", "mTagList",
		"mMaxVnodeTag",
		"mUndoType", "mUndoVnode", "mUndoParent", "mUndoBack", "mUndoN",
		"mUndoDVnodes", "mUndoLastChild", "mUndoablyDeletedVnode" ]}</t>
<t tx="ekr.20031218072017.2447">testData = [ "\n@doc\n\
This is a doc part: format, whilest, {};-&gt;.\n\
&lt;&lt;\
section def&gt;&gt;=\n\
LeoFrame::LeoFrame(vnode *v, char *s, int i)\n\
{\n\
	// test ; {} /* */.\n\
	#if 0 //comment\n\
		if(gLeoFrameList)gLeoFrameList -&gt; mPrevFrame = this ;\n\
		else\n\
			this -&gt; mNextFrame = gLeoFrameList ;\n\
	#else\n\
		\n\
		vnode *v = new vnode(a,b);\n\
		Commands *commander = (Commands) NULL ; // after cast\n\
		this -&gt; mPrevFrame = NULL ;\n\
	#endif\n\
	if (a==b)\n\
		a = 2;\n\
	else if (a ==c)\n\
		a = 3;\n\
	else return; \n\
	/* Block comment test:\n\
		if(2):while(1): end.*/\n\
	for(int i = 1; i &lt; limit; ++i){\n\
		mVisible = FALSE ;\n\
		mOnTop = TRUE ;\n\
	}\n\
	// trailing ws.	 \n\
	mCommands = new Commands(this, mTreeCtrl, mTextCtrl) ;\n\
	gActiveFrame = this ;\n\
}\n\
	", "&lt;&lt;" +
"vnode methods &gt;&gt;=\n\
\n\
void vnode::OnCopyNode(wxCommandEvent&amp; WXUNUSED(event))\n\
{\n\
	mCommands -&gt; copyOutline();\n\
}\n\
\n@doc\n\
another doc part if, then, else, -&gt; \n&lt;&lt;" +
"vnode methods &gt;&gt;=\n\
void vnode::OnPasteNode(wxCommandEvent&amp; WXUNUSED(event))\n\
{\n\
	mCommands -&gt; pasteOutline();\n\
}\n" ]</t>
<t tx="ekr.20031218072017.2448">def speedTest(passes):

	import time
	file = r"c:\prog\LeoPy\LeoPy.leo"
	f=open(file)
	if not f:
		print "not found: ", file
		return
	s=f.read()
	f.close()
	print "file:", file, " size:", len(s), " passes:", passes
	print "speedTest start"
	time1 = time.clock()
	p = passes
	while p &gt; 0:
		n = len(s) ; i = 0 ; lines = 0
		while -1 &lt; i &lt; n:
			if s[i] == '\n':
				lines += 1 ; i += 1
			else:
				i = s.find('\n',i) # _much_ faster than list-based-find.
			continue
			# match is about 9 times slower than simple test.
			if s[i]=='\n': # g.match(s,i,'\n'): # 
				i += 1
			else:
				i += 1
		p -= 1
	time2 = time.clock()
	print "lines:", lines
	print "speedTest done:"
	print "elapsed time:", time2-time1
	print "time/pass:", (time2-time1)/passes</t>
<t tx="ekr.20031218072017.2449"></t>
<t tx="ekr.20031218072017.2450">def leo1to2():

	import leo
	import leoGlobals
	c=leoGlobals.top()
	v=c.currentVnode()
	convertLeo1to2(v,c)
</t>
<t tx="ekr.20031218072017.2451">def convertLeo1to2(v,c):

	after=v.nodeAfterTree()
	while v and v != after:
		s=v.bodyString()
		print "converting:", v.headString()
		s=convertStringLeo1to2(s)
		v.setBodyStringOrPane(s)
		v=v.threadNext()

	c.Repaint() # for backward compatibility
	print "end of leo1to2"</t>
<t tx="ekr.20031218072017.2452">def convertStringLeo1to2 (s):

	# print "convertStringLeo1to2:start\n", s
	codeList = stringToList(s) ; outputList = []
	i = 0
	while i &lt; len(codeList):
		j = skipCodePart(codeList,i)
		if j &gt; i:
			code = codeList[i:j]
			convertCodeList1to2(code)
			i = j
			#print "-----code:", g.listToString(code)
			for item in code:
				outputList.append(item)
		j = skipDocPart(codeList,i)
		if j &gt; i:
			doc = codeList[i:j]
			convertDocList(doc) # same as in c2py
			#print "-----doc:", g.listToString(doc)
			i = j
			for item in doc:
				outputList.append(item)
	
	result = g.listToString(outputList)
	global printFlag
	if printFlag: print "-----:\n", result
	return result</t>
<t tx="ekr.20031218072017.2453">@ We do _not_ replace @root by @file or insert @others as needed.  Inserting @others can be done easily enough by hand, and may take more global knowledge than we can reasonably expect to have.
@c

def convertCodeList1to2(list):

	if 0: # There isn't much reason to do this.
		removeAtRoot(list)
	safeReplace(list, "@code", "@c")
	replaceSectionDefs(list)
	removeLeadingAtCode(list)
</t>
<t tx="ekr.20031218072017.2454">@ We separate the processing into two parts, 1) a leo-aware driver that iterates over @file trees and 2) a text-based part that processes one or more files or strings.
</t>
<t tx="ekr.20031218072017.2455">def convertCurrentTree():

	import c2py
	import leo
	import leoGlobals
	c=leoGlobals.top()
	v = c.currentVnode()
	c2py.convertLeoTree(v,c)</t>
<t tx="ekr.20031218072017.2456">def convertLeoTree(v,c):

	after=v.nodeAfterTree()
	while v and v != after:
		s=v.bodyString()
		print "converting:", v.headString()
		s=convertCStringToPython(s, doLeoTranslations )
		v.setBodyStringOrPane(s)
		v=v.threadNext()
	c.Repaint() # for backward compatibility.
	print "end of c2py"</t>
<t tx="ekr.20031218072017.2457">def convertCFileToPython(file):

	f=open(file, 'r')
	if not f: return
	s = f.read()
	f.close();
	f=open(file + ".py", 'w')
	if not f: return
	s = convertCStringToPython(s, dontDoLeoTranslations )
	f.write(s)
	f.close()</t>
<t tx="ekr.20031218072017.2458"></t>
<t tx="ekr.20031218072017.2459">def convertCStringToPython(s, leoFlag):

	# print "convertCStringToPython:start\n", s
	firstPart = true
	codeList = stringToList(s)
	
	if not leoFlag:
		convertCodeList(codeList, firstPart, dontDoLeoTranslations)
		return g.listToString(codeList)

	outputList = []
	i = 0
	while i &lt; len(codeList):
		j = skipCodePart(codeList,i)
		if j &gt; i:
			code = codeList[i:j]
			convertCodeList(code, firstPart, doLeoTranslations)
			i = j
			#print "-----code:", g.listToString(code)
			for item in code:
				outputList.append(item)
		firstPart = false # don't remove @c from here on.
		j = skipDocPart(codeList,i)
		if j &gt; i:
			doc = codeList[i:j]
			convertDocList(doc)
			#print "-----doc:", g.listToString(doc)
			i = j
			for item in doc:
				outputList.append(item)
	
	result = g.listToString(outputList)
	global printFlag
	if printFlag: print "-----:\n", result
	return result</t>
<t tx="ekr.20031218072017.2460">def convertCodeList(list, firstPart, leoFlag):
	#first
	replace(list, "\r", None)
	convertLeadingBlanks(list)
	if leoFlag:
		replaceSectionDefs(list)
	mungeAllFunctions(list)
	#next
	safeReplace(list, " -&gt; ", '.')
	safeReplace(list, "-&gt;", '.')
	safeReplace(list, " . ", '.')
	safeReplace(list, "this.self", "self")
	safeReplace(list, "{", None)
	safeReplace(list, "}", None)
	safeReplace(list, "#if", "if")
	safeReplace(list, "#else", "else")
	safeReplace(list, "#endif", None)
	safeReplace(list, "else if", "elif")
	safeReplace(list, "else", "else:")
	safeReplace(list, "&amp;&amp;", "and")
	safeReplace(list, "||", "or")
	safeReplace(list, "TRUE", "true")
	safeReplace(list, "FALSE", "false")
	safeReplace(list, "NULL", "None")
	safeReplace(list, "this", "self")
	safeReplace(list, "try", "try:")
	safeReplace(list, "catch", "except:")
	if leoFlag:
		safeReplace(list, "@code", "@c")
	#next
	handleAllKeywords(list)
	# after processing for keywords
	removeSemicolonsAtEndOfLines(list)
	#last
	if firstPart and leoFlag: removeLeadingAtCode(list)
	removeBlankLines(list)
	removeExcessWs(list)
	# your taste may vary: in Python I don't like extra whitespace
	safeReplace(list, " :", ":") 
	safeReplace(list, ", ", ",")
	safeReplace(list, " ,", ",")
	safeReplace(list, " (", "(")
	safeReplace(list, "( ", "(")
	safeReplace(list, " )", ")")
	safeReplace(list, ") ", ")")
	replaceComments(list) # should follow all calls to safeReplace
	g.removeTrailingWs(list)
	safeReplace(list, "\t ", "\t") # happens when deleting declarations.</t>
<t tx="ekr.20031218072017.2461">def convertDocList(docList):

	# print "convertDocList:", docList
	if matchWord(docList, 0, "@doc"):
		i = skipWs(docList, 4)
		if g.match(docList, i, "\n"):
			i += 1
		docList[0:i] = list("@ ")</t>
<t tx="ekr.20031218072017.2462">def skipDocPart(list, i):
	
	# print "skipDocPart", i
	while i &lt; len(list):
		if matchWord(list, i, "@code") or matchWord(list, i, "@c"):
			break
		elif isSectionDef(list,i):
			break
		else: i = skipPastLine(list, i)
	return i</t>
<t tx="ekr.20031218072017.2463">def skipCodePart(codeList, i):
	
	# print "skipCodePart", i
	if matchWord(codeList, i, "@doc") or matchWord(codeList, i, "@"):
		return i
	while i &lt; len(codeList):
		if g.match(codeList, i, "//"):
			i = skipPastLine(codeList,i)
		elif g.match(codeList, i, "/*"):
			i = skipCBlockComment(codeList,i)
		elif g.match(codeList, i, '"') or g.match(codeList, i, "'"):
			i = skipString(codeList,i)
		elif g.match(codeList, i, "\n"):
			i += 1
			if matchWord(codeList, i, "@doc") or matchWord(codeList, i, "@"):
				break
		else: i += 1
	return i</t>
<t tx="ekr.20031218072017.2464"></t>
<t tx="ekr.20031218072017.2465"></t>
<t tx="ekr.20031218072017.2466">def convertLeadingBlanks(list):

	global tabWidth
	if tabWidth &lt; 2: return
	i = 0
	while i &lt; len(list):
		n = 0
		while i &lt; len(list) and list[i] == ' ':
			n += 1 ; i += 1
			if n == tabWidth:
				list[i-tabWidth:i] = ['\t']
				i = i - tabWidth + 1
				n = 0
		i = skipPastLine(list, i)</t>
<t tx="ekr.20031218072017.2467">def findInList(list, i, findStringOrList):

	findList = stringToList(findStringOrList)
	
	while i &lt; len(list):
		if g.match(list, i, findList): return i
		else: i += 1
	return -1</t>
<t tx="ekr.20031218072017.2468">def findInCode(codeList, i, findStringOrList):

	findList = stringToList(findStringOrList)
	
	while i &lt; len(codeList):
		if isStringOrComment(codeList,i):
			i = skipStringOrComment(codeList,i)
		elif g.match(codeList, i, findList):
			return i
		else: i += 1
	return -1</t>
<t tx="ekr.20031218072017.2469"># We scan for a '{' at the top level that is preceeded by ')'
# @code and &lt; &lt; x &gt; &gt; = have been replaced by @c
def mungeAllFunctions(codeList):

	prevSemi = 0 # Previous semicolon: header contains all previous text
	i = 0
	firstOpen = None
	while i &lt; len(codeList):
		if isStringOrComment(codeList,i):
			i = skipStringOrComment(codeList,i)
			prevSemi = i
		elif g.match(codeList, i, '('):
			if not firstOpen:
				firstOpen = i
			i += 1
		elif g.match(codeList, i, '#'):
			i = skipPastLine(codeList, i)
			prevSemi = i
		elif g.match(codeList, i, ';'):
			i += 1
			prevSemi = i
		elif matchWord(codeList, i, "@code"):
			i += 5
			prevSemi = i # restart the scan
		elif matchWord(codeList, i, "@c"):
			i += 2 ; prevSemi = i # restart the scan
		elif g.match(codeList, i, "{"):
			i = handlePossibleFunctionHeader(codeList,i,prevSemi,firstOpen)
			prevSemi = i ; firstOpen = None # restart the scan
		else: i += 1</t>
<t tx="ekr.20031218072017.2470"># converts function header lines from c++ format to python format.
# That is, converts
# x1..nn w::y ( t1 z1,..tn zn) {
# to
# def y (z1,..zn): {

def handlePossibleFunctionHeader(codeList, i, prevSemi, firstOpen):

	assert(g.match(codeList,i,"{"))
	prevSemi = skipWsAndNl(codeList, prevSemi)
	close = prevNonWsOrNlChar(codeList, i)
	if close &lt; 0 or codeList[close] != ')':
		return 1 + skipToMatchingBracket(codeList, i)
	if not firstOpen:
		return 1 + skipToMatchingBracket(codeList, i)
	close2 = skipToMatchingBracket(codeList, firstOpen)
	if close2 != close:
		return 1 + skipToMatchingBracket(codeList, i)
	open = firstOpen
	assert(codeList[open]=='(')
	head = codeList[prevSemi:open]
	# do nothing if the head starts with "if", "for" or "while"
	k = skipWs(head,0)
	if k &gt;= len(head) or not head[k] in string.letters:
		return 1 + skipToMatchingBracket(codeList, i)
	kk = skipPastWord(head,k)
	if kk &gt; k:
		headString = g.listToString(head[k:kk])
		# C keywords that might be followed by '{'
		# print "headString:", headString
		if headString in [ "class", "do", "for", "if", "struct", "switch", "while"]:
			return 1 + skipToMatchingBracket(codeList, i)
	args = codeList[open:close+1]
	k = 1 + skipToMatchingBracket(codeList,i)
	body = codeList[i:k]
	#print "head:", g.listToString(head)
	#print "args:", g.listToString(args)
	#print "body:", g.listToString(body)
	#print "tot: ", g.listToString(codeList[prevSemi:k])
	head = massageFunctionHead(head)
	args = massageFunctionArgs(args)
	body = massageFunctionBody(body)
	#print "head2:", g.listToString(head)
	#print "args2:", g.listToString(args)
	#print "body2:", g.listToString(body)
	#print "tot2: ", g.listToString(codeList[prevSemi:k])
	result = []
	for item in head:
		result.append(item)
	for item in args:
		result.append(item)
	for item in body:
		result.append(item)
	codeList[prevSemi:k] = result
	return k</t>
<t tx="ekr.20031218072017.2471">def massageFunctionArgs(args):
	global gClassName
	assert(args[0]=='(')
	assert(args[-1]==')')

	result = ['('] ; lastWord = []
	if gClassName:
		for item in list("self,"): result.append(item) #can put extra comma

	i = 1
	while i &lt; len(args):
		i = skipWsAndNl(args, i)
		c = args[i]
		if c in string.letters:
			j = skipPastWord(args,i)
			lastWord = args[i:j]
			i = j
		elif c == ',' or c == ')':
			for item in lastWord:
				result.append(item)
			if lastWord != [] and c == ',':
				result.append(',')
			lastWord = []
			i += 1
		else: i += 1
	if result[-1] == ',':
		del result[-1]
	result.append(')')
	result.append(':')
	# print "new args:", g.listToString(result)
	return result</t>
<t tx="ekr.20031218072017.2472">def massageFunctionHead(head):

	# print "head:", g.listToString(head)
	result = []
	prevWord = []
	global gClassName ; gClassName = []
	i = 0
	while i &lt; len(head):
		i = skipWsAndNl(head, i)
		if i &lt; len(head) and head[i] in string.letters:
			result = []
			j = skipPastWord(head,i)
			prevWord = head[i:j]
			i = j
			# look for ::word2
			i = skipWs(head,i)
			if g.match(head,i,"::"):
				# Set the global to the class name.
				gClassName = g.listToString(prevWord)
				# print "class name:", gClassName
				i = skipWs(head, i+2)
				if i &lt; len(head) and (head[i]=='~' or head[i] in string.letters):
					j = skipPastWord(head,i)
					if head[i:j] == prevWord:
						for item in list("__init__"): result.append(item)
					elif head[i]=='~' and head[i+1:j] == prevWord:
						for item in list("__del__"): result.append(item)
					else:
						# for item in "::": result.append(item)
						for item in head[i:j]: result.append(item)
					i = j
			else:
				for item in prevWord:result.append(item)
		else: i += 1
		
	finalResult = list("def ")
	for item in result: finalResult.append(item)
	# print "new head:", g.listToString(finalResult)
	return finalResult</t>
<t tx="ekr.20031218072017.2473">def massageFunctionBody(body):

	body = massageIvars(body)
	body = removeCasts(body)
	body = removeTypeNames(body)
	return body</t>
<t tx="ekr.20031218072017.2474">def massageIvars(body):

	if gClassName and ivarsDict.has_key(gClassName):
		ivars = ivarsDict [ gClassName ]
	else:
		ivars = []
	# print "key,ivars:",gClassName,ivars

	i = 0
	while i &lt; len(body):
		if isStringOrComment(body,i):
			i = skipStringOrComment(body,i)
		elif body[i] in string.letters:
			j = skipPastWord(body,i)
			word = g.listToString(body[i:j])
			# print "looking up:", word
			if word in ivars:
				# replace word by self.word
				# print "replacing", word, " by self.", word
				word = "self." + word
				word = list(word)
				body[i:j] = word
				delta = len(word)-(j-i)
				i = j + delta
			else: i = j
		else: i += 1
	return body</t>
<t tx="ekr.20031218072017.2475">def removeCasts(body):

	i = 0
	while i &lt; len(body):
		if isStringOrComment(body,i):
			i = skipStringOrComment(body,i)
		elif g.match(body, i, '('):
			start = i
			i = skipWs(body, i+1)
			if body[i] in string.letters:
				j = skipPastWord(body,i)
				word = g.listToString(body[i:j])
				i = j
				if word in classList or word in typeList:
					i = skipWs(body, i)
					while g.match(body,i,'*'):
						i += 1
					i = skipWs(body, i)
					if g.match(body,i,')'):
						i += 1
						# print "removing cast:", g.listToString(body[start:i])
						del body[start:i]
						i = start
		else: i += 1
	return body</t>
<t tx="ekr.20031218072017.2476"># Do _not_ remove type names when preceeded by new.

def removeTypeNames(body):

	i = 0
	while i &lt; len(body):
		if isStringOrComment(body,i):
			i = skipStringOrComment(body,i)
		elif matchWord(body, i, "new"):
			i = skipPastWord(body,i)
			i = skipWs(body,i)
			# don't remove what follows new.
			if body[i] in string.letters:
				i = skipPastWord(body,i)
		elif body[i] in string.letters:
			j = skipPastWord(body,i)
			word = g.listToString(body[i:j])
			if word in classList or word in typeList:
				k = skipWs(body, j)
				while g.match(body,k,'*'):
					k += 1 ; j = k
				# print "Deleting type name:", g.listToString(body[i:j])
				del body[i:j]
			else:
				i = j
		else: i += 1
	return body</t>
<t tx="ekr.20031218072017.2477"># converts if ( x ) to if x:
# converts while ( x ) to while x:
def handleAllKeywords(codeList):

	# print "handAllKeywords:", g.listToString(codeList)
	i = 0
	while i &lt; len(codeList):
		if isStringOrComment(codeList,i):
			i = skipStringOrComment(codeList,i)
		elif ( matchWord(codeList,i,"if") or
			matchWord(codeList,i,"while") or
			matchWord(codeList,i,"for") or
			matchWord(codeList,i,"elif") ):
			i = handleKeyword(codeList,i)
		else:
			i += 1
	# print "handAllKeywords2:", g.listToString(codeList)</t>
<t tx="ekr.20031218072017.2478">def handleKeyword(codeList,i):

	isFor = false
	if (matchWord(codeList,i,"if")):
		i += 2
	elif (matchWord(codeList,i,"elif")):
		i += 4
	elif (matchWord(codeList,i,"while")):
		i += 5
	elif (matchWord(codeList,i,"for")):
		i += 3
		isFor = true
	else: assert(0)
	# Make sure one space follows the keyword
	k = i
	i = skipWs(codeList,i)
	if k == i:
		c = codeList[i]
		codeList[i:i+1] = [ ' ', c ]
		i += 1
	# Remove '(' and matching ')' and add a ':'
	if codeList[i] == "(":
		j = removeMatchingBrackets(codeList,i)
		if j &gt; i and j &lt; len(codeList):
			c = codeList[j]
			codeList[j:j+1] = [":", " ", c]
			j = j + 2
		return j
	return i</t>
<t tx="ekr.20031218072017.2479">def isWs(c):
	return c == ' ' or c == '\t'
	
def isWsOrNl(c):
	return c == ' ' or c == '\t' or c == '\n'</t>
<t tx="ekr.20031218072017.2480"># returns the ending index if i points to &lt; &lt; x &gt; &gt; =
def isSectionDef(list, i):

	i = skipWs(list,i)
	if not g.match(list,i,"&lt;&lt;"): return false
	while i &lt; len(list) and list[i] != '\n':
		if g.match(list,i,"&gt;&gt;="): return i+3
		else: i += 1
	return false</t>
<t tx="ekr.20031218072017.2481">def isStringOrComment(list, i):

	return g.match(list,i,"'") or g.match(list,i,'"') or g.match(list,i,"//") or g.match(list,i,"/*")</t>
<t tx="ekr.20031218072017.2482"># returns true if findList matches starting at codeList[i]

def match (codeList, i, findStringOrList):

	findList = stringToList(findStringOrList)
	n = len(findList)
	j = 0
	while i+j &lt; len(codeList) and j &lt; len(findList):
		if codeList[i+j] != findList[j]:
			return false
		else:
			j += 1
			if j == n:
				return i+j
	return false</t>
<t tx="ekr.20031218072017.2483">def matchWord (codeList, i, findStringOrList):

	j = g.match(codeList,i,findStringOrList)
	if not j:
		return false
	elif j &gt;= len(codeList):
		return true
	else:
		c = codeList[j]
		return not (c in string.letters or c in string.digits or c == '_')</t>
<t tx="ekr.20031218072017.2484">def prevNonWsChar(list, i):

	i -= 1
	while i &gt;= 0 and isWs(list[i]):
		i -= 1
	return i

def prevNonWsOrNlChar(list, i):

	i -= 1
	while i &gt;= 0 and isWsOrNl(list[i]):
		i -= 1
	return i</t>
<t tx="ekr.20031218072017.2485">def removeAllCComments(list, delim):

	i = 0
	while i &lt; len(list):
		if g.match(list,i,"'") or g.match(list,i,'"'):
			i = skipString(list,i)
		elif g.match(list,i,"//"):
			j = skipPastLine(list,i)
			print "deleting single line comment:", g.listToString(list[i:j])
			del list[i:j]
		elif g.match(list,i,"/*"):
			j = skipCBlockComment(list,i)
			print "deleting block comment:", g.listToString(list[i:j])
			del list[i:j]
		else:
			i += 1</t>
<t tx="ekr.20031218072017.2486">def removeAllCSentinels(list, delim):

	i = 0
	while i &lt; len(list):
		if g.match(list,i,"'") or g.match(list,i,'"'):
			# string starts a line.
			i = skipString(list,i)
			i = skipPastLine(list,i)
		elif g.match(list,i,"/*"):
			# block comment starts a line
			i = skipCBlockComment(list,i)
			i = skipPastLine(line,i)
		elif g.match(list,i,"//@"):
			j = skipPastLine(list,i)
			print "deleting sentinel:", g.listToString(list[i:j])
			del list[i:j]
		else:
			i = skipPastLine(list,i)</t>
<t tx="ekr.20031218072017.2487">def removeAllPythonComments(list, delim):

	i = 0
	while i &lt; len(list):
		if g.match(list,i,"'") or g.match(list,i,'"'):
			i = skipString(list,i)
		elif g.match(list,i,"#"):
			j = skipPastLine(list,i)
			print "deleting comment:", g.listToString(list[i:j])
			del list[i:j]
		else:
			i += 1</t>
<t tx="ekr.20031218072017.2488">def removeAllPythonSentinels(list, delim):

	i = 0
	while i &lt; len(list):
		if g.match(list,i,"'") or g.match(list,i,'"'):
			# string starts a line.
			i = skipString(list,i)
			i = skipPastLine(list,i)
		elif g.match(list,i,"#@"):
			j = skipPastLine(list,i)
			print "deleting sentinel:", g.listToString(list[i:j])
			del list[i:j]
		else:
			i = skipPastLine(list,i)</t>
<t tx="ekr.20031218072017.2489">def removeAtRoot (codeList):

	i = skipWs(codeList, 0)
	if matchWord(codeList,i,"@root"):
		j = skipPastLine(codeList,i)
		del codeList[i:j]

	while i &lt; len(codeList):
		if isStringOrComment(codeList,i):
			i = skipStringOrComment(codeList,i)
		elif g.match(codeList,i,"\n"):
			i = skipWs(codeList, i+1)
			if matchWord (codeList,i,"@root"):
				j = skipPastLine(codeList,i)
				del codeList[i:j]
		else: i += 1
</t>
<t tx="ekr.20031218072017.2490">def removeBlankLines(codeList):

	i = 0
	while i &lt; len(codeList):
		j = i
		while j &lt; len(codeList) and (codeList[j]==" " or codeList[j]=="\t"):
			j += 1
		if j== len(codeList) or codeList[j] == '\n':
			del codeList[i:j+1]
		else:
			oldi = i
			i = skipPastLine(codeList,i)</t>
<t tx="ekr.20031218072017.2491">def removeExcessWs(codeList):

	i = 0
	i = removeExcessWsFromLine(codeList,i)
	while i &lt; len(codeList):
		if isStringOrComment(codeList,i):
			i = skipStringOrComment(codeList,i)
		elif g.match(codeList,i,'\n'):
			i += 1
			i = removeExcessWsFromLine(codeList,i)
		else: i += 1</t>
<t tx="ekr.20031218072017.2492">def removeExcessWsFromLine(codeList,i):

	assert(i==0 or codeList[i-1] == '\n')
	i = skipWs(codeList,i)
	while i &lt; len(codeList):
		if isStringOrComment(codeList,i): break # safe
		elif g.match(codeList, i, '\n'): break
		elif g.match(codeList, i, ' ') or g.match(codeList, i, '\t'):
			# Replace all whitespace by one blank.
			k = i
			i = skipWs(codeList,i)
			codeList[k:i] = [' ']
			i = k + 1 # make sure we don't go past a newline!
		else: i += 1
	return i</t>
<t tx="ekr.20031218072017.2493">def removeLeadingAtCode(codeList):

	i = skipWsAndNl(codeList,0)
	if matchWord(codeList,i,"@code"):
		i = skipWsAndNl(codeList,5)
		del codeList[0:i]
	elif matchWord(codeList,i,"@c"):
		i = skipWsAndNl(codeList,2)
		del codeList[0:i]</t>
<t tx="ekr.20031218072017.2494">def removeMatchingBrackets(codeList, i):

	j = skipToMatchingBracket(codeList, i)
	if j &gt; i and j &lt; len(codeList):
		# print "del brackets:", g.listToString(codeList[i:j+1])
		c = codeList[j]
		if c == ')' or c == ']' or c == '}':
			del codeList[j:j+1]
			del codeList[i:i+1]
			# print "returning:", g.listToString(codeList[i:j])
			return j - 1
		else: return j + 1
	else: return j</t>
<t tx="ekr.20031218072017.2495">def removeSemicolonsAtEndOfLines(list):

	i = 0
	while i &lt; len(list):
		if isStringOrComment(list,i):
			i = skipStringOrComment(list,i)
		elif list[i] == ';':
			j = skipWs(list,i+1)
			if j &gt;= len(list) or g.match(list,j,'\n') or g.match(list,j,'#') or g.match(list,j,"//"):
				del list[i]
			else: i += 1
		else: i += 1</t>
<t tx="ekr.20031218072017.2496">def removeTrailingWs(list):

	i = 0
	while i &lt; len(list):
		if isWs(list[i]):
			j = i
			i = skipWs(list,i)
			assert(j &lt; i)
			if i &gt;= len(list) or list[i] == '\n':
				# print "removing trailing ws:", i-j
				del list[j:i]
				i = j
		else: i += 1</t>
<t tx="ekr.20031218072017.2497"># Replaces all occurances of findString by changeString.
# Deletes all occurances if change is None
def replace(codeList, findString, changeString):

	if len(findString)==0: return
	findList = stringToList(findString)
	changeList = stringToList(changeString)

	i = 0
	while i &lt; len(codeList):
		if g.match(codeList, i, findList):
			codeList[i:i+len(findList)] = changeList
			i += len(changeList)
		else: i += 1</t>
<t tx="ekr.20031218072017.2498"># For Leo we expect few block comments; doc parts are much more common.

def replaceComments(codeList):

	i = 0
	if g.match(codeList, i, "//"):
		codeList[0:2] = ['#']
	while i &lt; len(codeList):
		if g.match(codeList, i, "//"):
			codeList[i:i+2] = ['#']
			i = skipPastLine(codeList,i)
		elif g.match(codeList, i, "/*"):
			j = skipCBlockComment(codeList,i)
			del codeList[j-2:j]
			codeList[i:i+2] = ['#']
			j -= 2 ; k = i ; delta = -1
			while k &lt; j + delta :
				if codeList[k]=='\n':
					codeList[k:k+1] = ['\n', '#', ' ']
					delta += 2 ; k += 3 # progress!
				else: k += 1
			i = j + delta
		elif g.match(codeList, i, '"') or g.match(codeList, i, "'"):
			i = skipString(codeList,i)
		else: i += 1</t>
<t tx="ekr.20031218072017.2499"># Replaces &lt; &lt; x &gt; &gt; = by @c (at the start of lines).
def replaceSectionDefs(codeList):

	i = 0
	j = isSectionDef(codeList,i)
	if j &gt; 0: codeList[i:j] = list("@c ")

	while i &lt; len(codeList):
		if isStringOrComment(codeList,i):
			i = skipStringOrComment(codeList,i)
		elif g.match(codeList,i,"\n"):
			i += 1
			j = isSectionDef(codeList,i)
			if j &gt; i: codeList[i:j] = list("@c ")
		else: i += 1</t>
<t tx="ekr.20031218072017.2500"># Replaces occurances of findString by changeString outside of C comments and strings.
# Deletes all occurances if change is None.
def safeReplace(codeList, findString, changeString):

	if len(findString)==0: return
	findList = stringToList(findString)
	changeList = stringToList(changeString)
	i = 0
	if findList[0] in string.letters: #use matchWord
		while i &lt; len(codeList):
			if isStringOrComment(codeList,i):
				i = skipStringOrComment(codeList,i)
			elif matchWord(codeList, i, findList):
				codeList[i:i+len(findList)] = changeList
				i += len(changeList)
			else: i += 1
	else: #use match
		while i &lt; len(codeList):
			if g.match(codeList, i, findList):
				codeList[i:i+len(findList)] = changeList
				i += len(changeList)
			else: i += 1</t>
<t tx="ekr.20031218072017.2501">def skipCBlockComment(codeList, i):

	assert(g.match(codeList, i, "/*"))
	i += 2

	while i &lt; len(codeList):
		if g.match(codeList, i, "*/"): return i + 2
		else: i += 1
	return i</t>
<t tx="ekr.20031218072017.2502">def skipPastLine(codeList, i):

	while i &lt; len(codeList) and codeList[i] != '\n':
		i += 1
	if i &lt; len(codeList) and codeList[i] == '\n':
		i += 1
	return i</t>
<t tx="ekr.20031218072017.2503">def skipPastWord(list, i):

	assert(list[i] in string.letters or list[i]=='~')
	
	# Kludge: this helps recognize dtors.
	if list[i]=='~':
		i += 1
	
	while i &lt; len(list) and (
		list[i] in string.letters or
		list[i] in string.digits or
		list[i]=='_'):
		i += 1
	return i</t>
<t tx="ekr.20031218072017.2504">def skipString(codeList, i):

	delim = codeList[i] # handle either single or double-quoted strings
	assert(delim == '"' or delim == "'")
	i += 1

	while i &lt; len(codeList):
		if codeList[i] == delim: return i + 1
		elif codeList[i] == '\\': i += 2
		else: i += 1
	return i</t>
<t tx="ekr.20031218072017.2505">def skipStringOrComment(list,i):

	if g.match(list,i,"'") or g.match(list,i,'"'):
		return skipString(list,i)
	if g.match(list, i, "//"):
		return skipPastLine(list,i)
	elif g.match(list, i, "/*"):
		return skipCBlockComment(list,i)
	else: assert(0)</t>
<t tx="ekr.20031218072017.2506">def skipToMatchingBracket(codeList, i):

	c = codeList[i]
	if   c == '(': delim = ')'
	elif c == '{': delim = '}'
	elif c == '[': delim = ']'
	else: assert(0)

	i += 1
	while i &lt; len(codeList):
		c = codeList[i]
		if isStringOrComment(codeList,i):
			i = skipStringOrComment(codeList,i)
		elif c == delim:
			return i
		elif c == '(' or c == '[' or c == '{':
			i = skipToMatchingBracket(codeList,i)
			i += 1 # skip the closing bracket.
		else: i += 1
	return i</t>
<t tx="ekr.20031218072017.2507">def skipWs(list, i):

	while i &lt; len(list):
		c = list[i]
		if c == ' ' or c == '\t':
			i += 1
		else: break
	return i
	
def skipWsAndNl(list, i):

	while i &lt; len(list):
		c = list[i]
		if c == ' ' or c == '\t' or c == '\n':
			i += 1
		else: break
	return i</t>
<t tx="ekr.20031218072017.2508"># converts a string to a list containing one item per character of the list.
# converts None to the empty string and leaves other types alone.

# list(string) does not work on none.
def stringToList(string):

	if string:
		return list(string)
	else:
		return []</t>
<t tx="ekr.20031218072017.2509">def listToString(list):

	return string.join(list,"")</t>
<t tx="ekr.20031218072017.2510"># routines to gather static statistics about opcodes based on dis module.
import leoGlobals as g
from leoGlobals import true,false

import compiler,dis,os,string,sys,types

@others</t>
<t tx="ekr.20031218072017.2511">def go():
	
	dir = "c:/prog/leoCVS/leo/"
	modules = getModules(dir)
	stats = [0] * 256
	try:
		# Importing these might start leo itself and hang idle.
		modules.remove("leo")
		modules.remove("openLeo")
		modules.remove("openEkr")
		modules.remove("setup")
	except: pass
	# print modules
	
	for m in modules:
		try:
			print "module:", m
			exec("import " + m)
			a = eval(m)
			any(a,stats)
		except:
			import traceback ; traceback.print_exc()
			print "----- no matching class in", m
			
	g.print_stats(stats)</t>
<t tx="ekr.20031218072017.2512">def getFiles (dir):
	
	from leoGlobals import os_path_join,os_path_split,os_path_splitext

	# Generate the list of modules.
	allFiles = os.listdir(dir)
	files = []
	for f in allFiles:
		head,tail = g.os_path_split(f)
		root,ext = g.os_path_splitext(tail)
		if ext==".py":
			files.append(g.os_path_join(dir,f))
			
	return files</t>
<t tx="ekr.20031218072017.2513">def getModules (dir):
	
	"""Return the list of Python files in dir."""
	
	from leoGlobals import os_path_split,os_path_splitext
	
	files = []
	
	try:
		allFiles = os.listdir(dir)
		for f in allFiles:
			head,tail = g.os_path_split(f)
			fn,ext = g.os_path_splitext(tail)
			if ext==".py":
				files.append(fn)
	except: pass
			
	return files</t>
<t tx="ekr.20031218072017.2514">def any(x,stats,printName = 0):
	# based on dis.dis()
	"""Gathers statistics for classes, methods, functions, or code."""
	if not x:
		return
	if type(x) is types.InstanceType:
		x = x.__class__
	if hasattr(x, 'im_func'):
		x = x.im_func
	if hasattr(x, 'func_code'):
		x = x.func_code
	if hasattr(x, '__dict__'):
		items = x.__dict__.items()
		items.sort()
		for name, x1 in items:
			if type(x1) in (types.MethodType,
							types.FunctionType,
							types.CodeType):
				if printName: print name
				try:
					any(x1,stats)
				except TypeError, msg:
					print "Sorry:", msg
	elif hasattr(x, 'co_code'):
		code(x,stats)
	else:
		raise TypeError, \
			  "don't know how to disassemble %s objects" % \
			  type(x).__name__</t>
<t tx="ekr.20031218072017.2515">def code (co, stats):
	"""Gather static count statistics for a code object."""

	codeList = co.co_code
	# Count the number of occurances of each opcode.
	i = 0 ;  n = len(codeList)
	while i &lt; n:
		c = codeList[i]
		op = ord(c)
		stats[op] += 1
		i = i+1
		if op &gt;= dis.HAVE_ARGUMENT:
			i = i+2</t>
<t tx="ekr.20031218072017.2516">def print_stats (stats):

	stats2 = [] ; total = 0
	for i in xrange(0,256):
		if stats[i] &gt; 0:
			stats2.append((stats[i],i))
		total += stats[i]

	stats2.sort()
	stats2.reverse()
	for stat,i in stats2:
		print string.rjust(repr(stat),6), dis.opname[i]
	print "total", total</t>
<t tx="ekr.20031218072017.2517">@language python

@ This file contains functions for non-interactive searching.  You might find these useful while running other scripts.
@c

import leo, string, re

@others</t>
<t tx="ekr.20031218072017.2518">def changeAll ( commander, findPat, changePat, bodyFlag = 1 ):
	"""
	changeAll	make changes in an entire Leo outline.
	
	commander	Commands object for a Leo outline window.
	findPat		the search string.
	changePat	the replacement string.
	bodyFlag	true: change body text.  false: change headline text.
	"""
	n = len(changePat)
	v = commander.rootVnode()
	pos = 0
	while v != None:
		v, pos = changeNext(v, pos, findPat, changePat, bodyFlag)
		pos = pos + n</t>
<t tx="ekr.20031218072017.2519">def changeNext ( v, pos, findPat, changePat, bodyFlag = 1 ):
	"""
	changeNext:	use string.find() to change text in a Leo outline.
	
	v	 		the vnode to start the search.
	pos			the position within the body text of v to start the search.
	findPat		the search string.
	changePat	the replacement string.
	bodyFlag	true: change body text.  false: change headline text.
	
	returns a tuple (v,pos) showing where the change occured.
	returns (None,0) if no further match in the outline was found.

	Note: if (v,pos) is a tuple returned previously from changeNext,
	changeNext(v,pos+len(findPat),findPat,changePat)
	changes the next matching string.
	"""
	n = len(findPat)
	v, pos = findNext(v, pos, findPat, bodyFlag)
	if v == None:
		return None, 0
	if bodyFlag:
		s = v.bodyString()
		# s[pos:pos+n] = changePat
		s = s[:pos] + changePat + s[pos+n:]
		v.setBodyStringOrPane(s)
	else:
		s = v.headString()
		# s[pos:pos+n] = changePat
		s = s[:pos] + changePat + s[pos+n:]
		v.setHeadStringOrHeadline(s)
		print "setting head string: ", result
	return v, pos</t>
<t tx="ekr.20031218072017.2520">def changePrev ( v, pos, findPat, changePat, bodyFlag = 1 ):
	"""
	changePrev:	use string.rfind() to change text in a Leo outline.
	
	v	 		the vnode to start the search.
	pos			the position within the body text of v to start the search.
	findPat		the search string.
	changePat	the replacement string.
	bodyFlag	true: change body text.  false: change headline text.
	
	returns a tuple (v,pos) showing where the change occured.
	returns (None,0) if no further match in the outline was found.

	Note: if (v,pos) is a tuple returned previously from changePrev,
	changePrev(v,pos-len(findPat),findPat,changePat)
	changes the next matching string.
	"""
	n = len(findPat)
	v, pos = findPrev(v, pos, findPat, bodyFlag)
	if v == None:
		return None, 0
	if bodyFlag:
		s = v.bodyString()
		# s[pos:pos+n] = changePat
		s = s[:pos] + changePat + s[pos+n:]
		v.setBodyStringOrPane(s)
	else:
		s = v.headString()
		#s[pos:pos+n] = changePat
		s = s[:pos] + changePat + s[pos+n:]
		v.setHeadStringOrHeadline(s)
	return v, pos</t>
<t tx="ekr.20031218072017.2521">def findAll(c,pattern,bodyFlag=1):
	"""
	findAll		search an entire Leo outline for a pattern.
	
	c        commander for a Leo outline window.
	pattern		the search string.
	bodyFlag	true: search body text. false: search headline text.
	
	returns a list of tuples (v,pos) showing where matches occured.
	returns [] if no match were found.
	"""
	v = c.rootVnode()
	n = len(pattern)
	result = [] ; pos = 0
	while v != None:
		v, pos = findNext(v,pos,pattern,bodyFlag)
		if v:
			result.append ((v, pos),)
		pos = pos + n
	return result</t>
<t tx="ekr.20031218072017.2522">def findNext ( v, pos, pattern, bodyFlag = 1 ):
	"""
	findNext:	use string.find() to find a pattern in a Leo outline.
	
	v	 		the vnode to start the search.
	pos			the position within the body text of v to start the search.
	pattern		the search string.
	bodyFlag	true: search body text.  false: search headline text.
	
	returns a tuple (v,pos) showing where the match occured.
	returns (None,0) if no further match in the outline was found.

	Note: if (v,pos) is a tuple returned previously from findNext,
	findNext(v,pos+len(pattern),pattern) finds the next match.
	"""
	while v != None:
		if bodyFlag:
			s = v.bodyString()
		else:
			s = v.headString()
		pos = s.find(pattern,pos )
		if pos != -1:
			return v, pos
		v = v.threadNext()
		pos = 0
	return None, 0</t>
<t tx="ekr.20031218072017.2523">def findPrev ( v, pos, pattern, bodyFlag = 1 ):
	"""
	findPrev:	use string.rfind() to find a pattern in a Leo outline.
	
	v	 		the vnode to start the search.
	pos			the position within the body text of v to start the search.
	pattern		the search string
	bodyFlag	true: search body text.  false: search headline text.
	
	returns a tuple (v,pos) showing where the match occured.
	returns (None,0) if no further match in the outline was found.

	Note: if (v,pos) is a tuple returned previously from findPrev,
	findPrev(v,pos-len(pattern),pattern) finds the next match.
	"""
	while v != None:
		if bodyFlag:
			s = v.bodyString()
		else:
			s = v.headString()
		pos = s.rfind(pattern,0,pos)
		if pos != -1:
			return v, pos
		v  = v.threadBack()
		pos = -1
	return None, 0</t>
<t tx="ekr.20031218072017.2524">def reChangeAll ( commander, findPat, changePat, bodyFlag, reFlags = None ):
	"""
	reChangeAll: make changes in an entire Leo outline using re module.
	
	commander	Commands object for a Leo outline window.
	findPat		the search string.
	changePat	the replacement string.
	bodyFlag	true: change body text.  false: change headline text.
	reFlags		flags argument to re.search().
	"""
	n = len(changePat)
	v = commander.rootVnode()
	pos = 0
	while v != None:
		v, mo, pos = reChangeNext(
			v, pos, findPat, changePat, bodyFlag, reFlags)
		pos = pos + n</t>
<t tx="ekr.20031218072017.2525">def reChangeNext ( v, pos, findPat, changePat, bodyFlag, reFlags = None ):
	"""
	reChangeNext: use re.search() to change text in a Leo outline.
	
	v	 		the vnode to start the search.
	pos			the position within the body text of v to start the search.
	findPat		the search string.
	changePat	the replacement string.
	bodyFlag	true: change body text.  false: change headline text.
	reFlags		flags argument to re.search().
	
	returns a tuple (v,pos) showing where the change occured.
	returns (None,0) if no further match in the outline was found.

	Note: if (v,pos) is a tuple returned previously from reChangeNext,
	reChangeNext(v,pos+len(findPat),findPat,changePat,bodyFlag)
	changes the next matching string.
	"""
	n = len(findPat)
	v, mo, pos = reFindNext(v, pos, findPat, bodyFlag, reFlags)
	if v == None:
		return None, None, 0
	if bodyFlag:
		s = v.bodyString()
		print s, findPat, changePat
		# s[pos:pos+n] = changePat
		s = s[:pos] + changePat + s[pos+n:]
		v.setBodyStringOrPane(s)
	else:
		s = v.headString()
		# s[pos:pos+n] = changePat
		s = s[:pos] + changePat + s[pos+n:]
		v.setHeadStringOrHeadline(s)
	return v, mo, pos</t>
<t tx="ekr.20031218072017.2526">def reChangePrev ( v, pos, findPat, changePat, bodyFlag, reFlags = None ):
	"""
	reChangePrev: use re.search() to change text in a Leo outline.
	
	v	 		the vnode to start the search.
	pos			the position within the body text of v to start the search.
	findPat		the search string.
	changePat	the replacement string.
	bodyFlag	true: change body text.  false: change headline text.
	reFlags		flags argument to re.search().
	
	returns a tuple (v,pos) showing where the change occured.
	returns (None,0) if no further match in the outline was found.

	Note: if (v,pos) is a tuple returned previously from reChangePrev,
	reChangePrev(v,pos-len(findPat),findPat,changePat,bodyFlag)
	changes the next matching string.
	"""
	n = len(findPat)
	v, mo, pos = reFindPrev(v, pos, findPat, bodyFlag, reFlags)
	if v == None:
		return None, None, 0
	if bodyFlag:
		s = v.bodyString()
		# s[pos:pos+n] = changePat
		s = s[:pos] + changePat + s[pos+n:]
		v.setBodyStringOrPane(s)
	else:
		s = v.headString()
		# s[pos:pos+n] = changePat
		s = s[:pos] + changePat + s[pos+n:]
		v.setHeadStringOrHeadline(s)
	return v, mo, pos</t>
<t tx="ekr.20031218072017.2527">def reFindAll(c,findPat,bodyFlag,reFlags=None):
	"""
	reFindAll	search an entire Leo outline using re module.
	
	c	     commander for a Leo outline window.
	pattern		the search string.
	bodyFlag	true: search body text.  false: search headline text.
	reFlags		flags argument to re.search().

	returns a list of tuples (v,pos) showing where matches occured.
	returns [] if no match were found.
	"""
	v = c.rootVnode()
	n = len(findPat)
	result = [] ; pos = 0
	while v != None:
		v, mo, pos = reFindNext(v,pos,findPat,bodyFlag,reFlags)
		if v != None:
			result.append ( (v,mo,pos) )
		pos = pos + n
	return result</t>
<t tx="ekr.20031218072017.2528">def reFindNext ( v, pos, pattern, bodyFlag, reFlags = None ):
	"""
	reFindNext:	use re.search() to find pattern in a Leo outline.
	
	v	 		the vnode to start the search.
	pos			the position within the body text of v to start the search.
	pattern		the search string
	bodyFlag	true: search body text.  false: search headline text.
	reFlags		the flags argument to re.search()
	
	returns a tuple (v,mo,pos) showing where the match occured.
	returns (None,None,0) if no further match in the outline was found.
	mo is a "match object"

	Note: if (v,pos) is a tuple returned previously from reFindNext,
	reFindNext(v,pos+len(pattern),pattern) finds the next match.
	"""
	while v != None:
		if bodyFlag:
			s = v.bodyString()
		else:
			s = v.headString()
		if reFlags == None:
			mo = re.search ( pattern, s[pos:] )
		else:
			mo = re.search ( pattern, s[pos:], reFlags )
		if mo != None:
			return v, mo, pos + mo.start()
		v = v.threadNext()
		pos = 0
	return None, None, 0</t>
<t tx="ekr.20031218072017.2529">def reFindPrev ( v, pos, pattern, bodyFlag, reFlags = None ):
	"""
	reFindPrev:	use re.search() to find pattern in a Leo outline.

	v	 		the vnode to start the search.
	pos			the position within the body text of v to start the search.
	pattern		the search string
	bodyFlag	true: search body text.  false: search headline text.
	reFlags		the flags argument to re.search()
	
	returns a tuple (v,mo,pos) showing where the match occured.
	returns (None,None,0) if no further match in the outline was found.
	
	Note 1: Searches vnodes in reverse (v.threadBack) direction.
	Searches text of vnodes in _forward_ direction.
	
	Note 2: if (v,pos) is a tuple returned previously from reFindPrev,
	reFindPrev(v,pos-len(pattern),pattern) finds the next match.
	"""
	while v != None:
		if bodyFlag:
			s = v.bodyString()
		else:
			s = v.headString()
		# Forward search through text...
		if reFlags == None:
			mo = re.search ( pattern, s[pos:] )
		else:
			mo = re.search ( pattern, s[pos:], reFlags )
		if mo != None:
			return v, mo, pos+mo.start()
		# Reverse search through vnode.
		v = v.threadBack()
		pos = 0
	return None, None, 0</t>
<t tx="ekr.20031218072017.2530">def lineAtPos ( s, pos ):
	"""
	lineAtPos: return the line of a string containing the given index.
	s		a string
	pos		an index into s
	"""
	# find the start of the line containing the match
	if len(s) &lt; 1:
		return ""
	if pos &gt; len(s):
		pos = len(s)-1
		
	while pos &gt; 0:
		if s[pos] == '\n':
			pos = pos + 1
			break
		else:
			pos = pos - 1
	# return the line containing the match
	s = s[pos:]
	list = s.split("\n")
	return list[0]</t>
<t tx="ekr.20031218072017.2531">def printFindList( findList, bodyFlag = 1 ):
	"""
	printFindList:	Print matching lines from the list.
	
	findList:		a list of (v,pos) tuples returned from findAll().
	Only the line containing the match is printed.
	Lines are printed once for each match found on the line.
	"""
	for v,pos in findList:
		if v != None:
			if bodyFlag:
				s = v.bodyString()
			else:
				s = v.headString()
			print lineAtPos(s, pos)</t>
<t tx="ekr.20031218072017.2532">@first #! /usr/bin/env python
@language python

@ This tiny script is intended to be called from go.bat to open LeoPy.leo.  You could change the file name to be any file you work on a lot...
@c

import leo
leo.run("c:\prog\leoCVS\leo\LeoPy.leo")</t>
<t tx="ekr.20031218072017.2533">@first #! /usr/bin/env python
@language python

# Example tangle_done.py file.
# Leo catches all exceptions thrown here; there is no need for try:except blocks.

@others</t>
<t tx="ekr.20031218072017.2534"># Leo calls this routine if "Run tangle-done.py after Tangle" is checked in the Prefs panel.

def run (root_list):

	print "tangle_done roots:"
	for root in root_list:
		print root
	
	if 0: # Run code contributed by Paul Paterson.
		convertRSTfilesToHTML(root_list)</t>
<t tx="ekr.20031218072017.2535"># Adapted from code by Paul Paterson.

def convertRSTfilesToHTML(root_list):

	"""This routine creates .html files from all .rst files in root_list, the list of files that have just been tangled."""
	
	from leoGlobals import os_path_join,os_path_split,os_path_splitext
	
	for root in root_list: 
		base,fullname = g.os_path_split(root)
		name,ext = g.os_path_splitext(fullname)
		if ext == ".rst":
			file = g.os_path_join(base,name+".html")
			&lt;&lt; Convert root to corresponding .html file &gt;&gt;
</t>
<t tx="ekr.20031218072017.2536"># Leo will report the execption if docutils is not installed.
from docutils.core import Publisher 
from docutils.io import FileInput,StringOutput,StringInput 

# Read .rst file into s.
f = open(root,"r")
s = f.read()
f.close()

# Restucture s into output.
pub = Publisher() 
pub.source = StringInput(pub.settings,source=s) 
pub.destination = StringOutput(pub.settings,encoding="utf-8") 
pub.set_reader('standalone',None,'restructuredtext') 
pub.set_writer('html') 
output = pub.publish()

# EKR: 3/7/03: convert output using the present encoding.
dict = g.scanDirectives(self.c,p=root)
encoding = dict.get("encoding",None)
if encoding == None:
	encoding = g.app.config.default_derived_file_encoding
output = g.toEncodedString(output,encoding,reportErrors=true) 

# Write the corresponding html file.
f = open(file,"w")
f.write(output)
f.close()</t>
<t tx="ekr.20031218072017.2537">@first #! /usr/bin/env python
@language python

# Example untangle_done script

def run(root_list):

	print "untangle_done roots:", root_list</t>
<t tx="ekr.20031218072017.2538"></t>
<t tx="ekr.20031218072017.2539">@nocolor</t>
<t tx="ekr.20031218072017.2540">@color

@ NSIS Script for LEO - Literate Programming Editor with Outlines
http://sourceforge.net/projects/leo

How to create an installer for Leo using this script:
	1. Install NSIS (from http://www.nullsoft.com)
	2. Put the leo.nsi file in the directory containing the Leo program files.
	3. Right-click on the leo.nsi file and choose "Compile"
	
Version 1.0 of this script by Joe Orr, donated to public domain.
</t>
<t tx="ekr.20031218072017.2541">@comment ;
@silent
@root ../dist/leo.nsi

; NOTE: this .NSI script is designed for NSIS v1.8+

&lt;&lt; installer settings &gt;&gt;
&lt;&lt; required files section &gt;&gt;
&lt;&lt; optional files section &gt;&gt;
&lt;&lt; file association &gt;&gt;
&lt;&lt; post install section &gt;&gt;
&lt;&lt; uninstall section &gt;&gt;

; eof</t>
<t tx="ekr.20031218072017.2542">@code

# [Installer Attributes]
Name "Leo"
OutFile "leosetup.exe"
Caption "Leo Installer"

&lt;&lt; Additional Installer Settings &gt;&gt;
&lt;&lt; icons used by the installer &gt;&gt;
&lt;&lt; the user license &gt;&gt;
&lt;&lt; the installation dir &gt;&gt;

ComponentText "This will install Leo on your computer. Select which optional components you would also like to install."</t>
<t tx="ekr.20031218072017.2543">@code
Icon c:\prog\leoCVS\leo\Icons\leo_inst.ico
EnabledBitmap c:\prog\leoCVS\leo\Icons\leo_on.bmp
DisabledBitmap c:\prog\leoCVS\leo\Icons\leo_off.bmp</t>
<t tx="ekr.20031218072017.2544">@code

InstallDir "$PROGRAMFILES\Leo"
InstallDirRegKey HKEY_LOCAL_MACHINE "SOFTWARE\EKR\leo" ""
DirShow show # (make this hide to not let the user change it)
DirText "Select the directory to install Leo in:"</t>
<t tx="ekr.20031218072017.2545">@code
LicenseText "You must agree to this license before installing."
LicenseData c:\prog\leoCVS\leo\doc\LICENSE.TXT</t>
<t tx="ekr.20031218072017.2546">@ You may not need to change these for your own app...
@c
ShowInstDetails show
AutoCloseWindow false
SilentInstall normal
CRCCheck on
SetCompress auto
SetDatablockOptimize on
SetOverwrite ifnewer
WindowIcon off</t>
<t tx="ekr.20031218072017.2547">@code

Section "Leo" ; (default, required section)

  &lt;&lt; check to see whether Python is installed &gt;&gt;

ok:
  # List all files to included in installer	
  
  SetOutPath $INSTDIR
  File c:\prog\leoCVS\leo\__init__.py
  CreateShortCut "$INSTDIR\Shortcut to leo.py.lnk" "$INSTDIR\src\leo.py" "" "$INSTDIR\src\leo.py" 0

  SetOutPath $INSTDIR\config
  File c:\prog\leoCVS\leo\config\leoConfig.leo
  File c:\prog\leoCVS\leo\config\leoConfig.txt
 
  SetOutPath $INSTDIR\doc
  File c:\prog\leoCVS\leo\doc\LeoDocs.leo
  File c:\prog\leoCVS\leo\doc\README.TXT
  File c:\prog\leoCVS\leo\doc\INSTALL.TXT
  File c:\prog\leoCVS\leo\doc\PKG-INFO.TXT
  File c:\prog\leoCVS\leo\doc\LICENSE.TXT
  # File c:\prog\leoCVS\leo\doc\manifest.in
  
  SetOutPath $INSTDIR\Icons
  File c:\prog\leoCVS\leo\Icons\*.*
  
  SetOutPath $INSTDIR\examples
  
  SetOutPath $INSTDIR\plugins
  File c:\prog\leoCVS\leo\plugins\leoPlugins.leo
  File c:\prog\leoCVS\leo\plugins\*.py
  File c:\prog\leoCVS\leo\plugins\*.ini
  File c:\prog\leoCVS\leo\plugins\*.txt
  
  SetOutPath $INSTDIR\scripts
  File c:\prog\leoCVS\leo\scripts\*.py
  
  SetOutPath $INSTDIR\scripts\install
  File c:\prog\leoCVS\leo\scripts\install\*
  
  SetOutPath $INSTDIR\scripts\other
  File c:\prog\leoCVS\leo\scripts\other\*.py
  
  SetOutPath $INSTDIR\scripts\tangle
  File c:\prog\leoCVS\leo\scripts\tangle\*.py
  
  SetOutPath $INSTDIR\src
  File c:\prog\leoCVS\leo\src\LeoPy.leo
  File c:\prog\leoCVS\leo\src\leo*.py
  
  SetOutPath $INSTDIR\test
  File c:\prog\leoCVS\leo\test\test.leo
 
  SetOutPath $INSTDIR\tools

SectionEnd ; end of default section
</t>
<t tx="ekr.20031218072017.2548">@code
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
  
  Delete "$INSTDIR\config\*.*" ; config dir
  RMDir "$INSTDIR\config"
  Delete "$INSTDIR\doc\*.*" ; doc dir
  RMDir "$INSTDIR\doc"
  Delete "$INSTDIR\examples\*.*" ; src dir
  RMDir "$INSTDIR\examples"
  Delete "$INSTDIR\Icons\*.*" ; Icons dir
  RMDir "$INSTDIR\Icons"
  Delete "$INSTDIR\plugins\*.*" ; plugins dir
  RMDir "$INSTDIR\plugins"
  Delete "$INSTDIR\scripts\*.*" ; scripts dir
  RMDir "$INSTDIR\scripts"
  Delete "$INSTDIR\src\*.*" ; src dir
  RMDir "$INSTDIR\src"
  Delete "$INSTDIR\test\*.*" ; test dir
  RMDir "$INSTDIR\test"
  Delete "$INSTDIR\tools\*.*" ; tools dir
  RMDir "$INSTDIR\tools"
  Delete "$INSTDIR\*.*" ; Leo directory
  RMDir "$INSTDIR"

  Quit


</t>
<t tx="ekr.20031218072017.2549">@code

# optional sections

Section "Start Menu Shortcuts"
  CreateDirectory "$SMPROGRAMS\Leo"
  CreateShortCut "$SMPROGRAMS\Leo\Uninstall.lnk" "$INSTDIR\uninst.exe" "" "$INSTDIR\uninst.exe" 0
  CreateShortCut "$SMPROGRAMS\Leo\Leo.lnk" "$8" '"$INSTDIR\src\leo.py"' "$INSTDIR\Icons\LeoApp.ico" 0  
SectionEnd

Section "Desktop Shortcut"
  CreateShortCut "$DESKTOP\Leo.lnk" "$8" '"$INSTDIR\src\leo.py"' "$INSTDIR\Icons\LeoApp.ico" 0
SectionEnd</t>
<t tx="ekr.20031218072017.2550">@code

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
  WriteRegStr HKCR "LeoFile\shell\open\command" "" '$8 "$INSTDIR\src\leo.py" %1'  

SectionEnd</t>
<t tx="ekr.20031218072017.2551">@code

Section "-post" # (post install section, happens last after any optional sections)

  # add any commands that need to happen after any optional sections here
  WriteRegStr HKEY_LOCAL_MACHINE "SOFTWARE\EKR\leo" "" "$INSTDIR"
  WriteRegStr HKEY_LOCAL_MACHINE "Software\Microsoft\Windows\CurrentVersion\Uninstall\leo" "DisplayName" "Leo (remove only)"
  WriteRegStr HKEY_LOCAL_MACHINE "Software\Microsoft\Windows\CurrentVersion\Uninstall\leo" "UninstallString" '"$INSTDIR\uninst.exe"'

  # write out uninstaller
  WriteUninstaller "$INSTDIR\uninst.exe"

SectionEnd ; end of -post section

</t>
<t tx="ekr.20031218072017.2552">@code

# [ begin uninstall settings/section ]
UninstallText "This will uninstall Leo from your system"
UninstallCaption "Uninstall Leo"
UninstallIcon c:\prog\leoCVS\leo\Icons\uninst.ico

Section Uninstall

DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\EKR\leo"
DeleteRegKey HKEY_LOCAL_MACHINE "SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\leo"

&lt;&lt; remove file association &gt;&gt;
&lt;&lt; remove program folder &gt;&gt;
&lt;&lt; remove shortcuts &gt;&gt;

; remove directories used.
RMDir "$SMPROGRAMS\Leo"

SectionEnd ; end of uninstall section</t>
<t tx="ekr.20031218072017.2553">@code

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
<t tx="ekr.20031218072017.2554">@code
MessageBox MB_YESNO|MB_ICONQUESTION \
			 "Delete all files in Leo Program folder?" \
			 IDNO NoDelete  

  Delete "$INSTDIR\config\*.*" ; config dir
  RMDir "$INSTDIR\config"
  Delete "$INSTDIR\doc\*.*" ; doc dir
  RMDir "$INSTDIR\doc"
  Delete "$INSTDIR\examples\*.*" ; src dir
  RMDir "$INSTDIR\examples"
  Delete "$INSTDIR\Icons\*.*" ; Icons dir
  RMDir "$INSTDIR\Icons"
  Delete "$INSTDIR\plugins\*.*" ; plugins dir
  RMDir "$INSTDIR\plugins"
  Delete "$INSTDIR\scripts\install\*.*" ; scripts\install dir
  RMDir "$INSTDIR\scripts\install"
  Delete "$INSTDIR\scripts\other\*.*" ; scripts\other dir
  RMDir "$INSTDIR\scripts\other"
  Delete "$INSTDIR\scripts\tangle\*.*" ; scripts\tangle dir
  RMDir "$INSTDIR\scripts\tangle"
  Delete "$INSTDIR\scripts\*.*" ; scripts dir
  RMDir "$INSTDIR\scripts"
  Delete "$INSTDIR\src\*.*" ; src dir
  RMDir "$INSTDIR\src"
  Delete "$INSTDIR\test\*.*" ; test dir
  RMDir "$INSTDIR\test"
  Delete "$INSTDIR\tools\*.*" ; tools dir
  RMDir "$INSTDIR\tools"
  Delete "$INSTDIR\*.*" ; Leo directory
  RMDir "$INSTDIR"

NoDelete:
</t>
<t tx="ekr.20031218072017.2555">@code
Delete "$SMPROGRAMS\Leo\*.*"
Delete "$DESKTOP\Leo.lnk"</t>
<t tx="ekr.20031218072017.2556">Leo is Open Software and is distributed under the terms of the Python License. The gist of the license is that Leo is absolutely free, even for commercial use (including resale). There is no GNU-like "copyleft" restriction. The Open Source Initiative board has voted to certify the Python license as Open Source. This license is compatible with the GPL.

Copyright (c) 1997-2003 by Edward K. Ream. All Rights Reserved.

Permission to use, copy, modify, and distribute this software and its documentation for any purpose and without fee is hereby granted, provided that the above copyright notice appear in all copies and that both that copyright notice and this permission notice appear in supporting documentation, and that the names of Leo or Edward K. Ream not be used in advertising or publicity pertaining to distribution of the software without specific, written prior permission.

DISCLAIMER OF WARRANTIES

EDWARD K. REAM (REAM) SPECIFICALLY DISCLAIMS ALL WARRANTIES, EXPRESSED OR IMPLIED, WITH RESPECT TO THIS COMPUTER SOFTWARE, INCLUDING BUT NOT LIMITED TO IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE. IN NO EVENT SHALL REAM BE LIABLE FOR ANY LOSS OF PROFIT OR ANY COMMERCIAL DAMAGE, INCLUDING BUT NOT LIMITED TO SPECIAL, INCIDENTAL, CONSEQUENTIAL OR OTHER DAMAGES.</t>
<t tx="ekr.20031218072017.2557"></t>
<t tx="ekr.20031218072017.2558">System requirements for leo.py
------------------------------

leo.py requires Python 2.2 or above and tcl/tk 8.4 or above.

	Download Python from http://python.org/ 
	Download tcl/Tk from http://tcl.activestate.com/software/tcltk/

Warning: When building Tcl on Linux, do not specify "--enable-threads" .
Only use Tcl with the default "threads not enabled" case.</t>
<t tx="ekr.20031218072017.2559">
Installing the leo.py on Linux
------------------------------

You can install Leo using the install script provided.  Remember to 'chmod +x' before running this script.

Leo is distributed as a single compressed (.zip) folder.  Simply uncompress this folder, put the folder in a convenient place and run leo.py.  You can run leo.py by double-clicking leo.py.  You can also run leo.py from a Python interpreter as follows:

	import leo
	leo.run() # runs leo.py, opening a new outline.
	leo.go() # runs leo.py after reloading all modules.
	leo.leoOpen(fileName) # runs leo.py, reloads all modules, and opens fileName.

You may specify options using the configuration file called leoConfig.txt.  You should generate this file using leoConfig.leo.</t>
<t tx="ekr.20031218072017.2560">
Installing the leo.py on Windows
--------------------------------

Important: You can install leo.py on Windows using the single-click installer called leosetup.exe.

Leo is distributed as a single compressed (.zip) folder.  Uncompress this folder, put the folder in a convenient place and run leo.py.  You can run leo.py by double-clicking leo.py.  You can also run leo.py from a Python interpreter as follows:

	import leo
	leo.run() # runs leo.py, opening a new outline.
	leo.go() # runs leo.py after reloading all modules.
	leo.leoOpen(fileName) # runs leo.py, reloads all modules, and opens fileName.

You may specify options using the configuration file called leoConfig.txt.  You should generate this file using leoConfig.leo.
</t>
<t tx="ekr.20031218072017.2561">
Installing leo.py on MacOs
--------------------------

Bruce M. Bolden, bruceb@cs.uidaho.edu, is using Leo on MaxOS X.  Here is his description of how to get Leo working there:

I installed: 
- Latest OS X Developer tools
- latest (as of about two weeks ago) tk/tcl
		 MacOSXTk8.4a4-2.tar.gz
- the machopython distribution
http://prdownloads.sourceforge.net/wxpython/MachoPython-2.2.1.dmg

For OS X 10.1, I followed the directions at:
	http://tony.lownds.com/macosx/tkinter.html

That worked fine for 10.1, but didn't work for 10.2.  It
took awhile to find a Python distribution that worked
correctly with tk/tcl.

I was just getting into Leo about a week before 10.2 was released and thought about---what if it breaks....10.2 broke it, but I was able to find a solution as described above.

More re MacOS from Bruce Bolden
-------------------------------

I just finished building tk successfully!  The magic step was the execution of the command

cp ../generic/prolog.ps to ../library/prolog.ps

AFTER 

cd ../../tk/macosx

in the instructions on "Steps to build Tcl/Tk 8.4.0 on MacOS X":

http://mini.net/tcl/4052

I found this solution while looking at the tcl-mac mailing list archive.  The earlier (current?) tar ball on SourceForge did not have the file prolog.ps in the library directory:

http://sourceforge.net/mailarchive/forum.php?thread_id=1060496&amp;forum_id=3853

Copy and Paste seem to work just fine now in Leo!  This was my original question for you.

I also noticed that someone else built everything on OS X 10.2 (Jaguar), but they did it under X.  Since, the new version of Tk appears to support the OS X interface quite well, I'm not going to bother installing X (for now).

So, Leo works two different ways on OS X 10.2.
</t>
<t tx="ekr.20031218072017.2562">
Using shell scripts and batch files to make using Leo easier
------------------------------------------------------------

On Linux, the following shell script will allow you to open foo.leo files by typing leo foo

#!/bin/sh 
python &lt;leopath&gt;/leo.py $1

where &lt;leopath&gt; is replaced with the path to the leo directory. 

On Windows, the equivalent batch file would be:

c:\python22\python &lt;leopath&gt;leo.py %1

</t>
<t tx="ekr.20031218072017.2563">Metadata-Version: 1.0
Name: leo
Version: 4.2-a1
Summary: Leo: Literate Editor with Outlines
Home-page: http://webpages.charter.net/edreamleo/front.html
Author: Edward K. Ream
Author-email: edreamleo@charter.net
License: Python
Description: Leo is an outline-oriented editor written in 100% pure Python.
		Leo works on any platform that supports Python 2.2 or above and the Tk toolkit.
		This version of Leo was developed with Python 2.3.3 and Tk 8.4.3.
		You may download Python from http://python.org/ and
		tcl/Tk from http://tcl.activestate.com/software/tcltk/
		Leo features a multi-window outlining editor, Python colorizing,
		powerful outline commands and many other things, including 
		Unlimited Undo/Redo and an integrated Python shell(IDLE) window.
		Leo will place its own icon in Leo windows provided that you have
		installed Fredrik Lundh's PIL and tkIcon packages:
		Download PIL from http://www.pythonware.com/downloads/index.htm#pil
		Download tkIcon from http://www.effbot.org/downloads/#tkIcon
Platform: Windows, Linux, Macintosh
</t>
<t tx="ekr.20031218072017.2564">Important note: See INSTALL.TXT for installation instructions.

Leo is available at:  http://sourceforge.net/projects/leo/
Leo requires Python 2.1 or above and tcl/tk 8.3 or above.
Leo will work on Linux, Windows and MacOs X Jaguar.

Leo 4.2 alpha 1            April 14, 2004

This is a "semi-public" release of the new 4.2 code base.  I am releasing this code now to create a snapshot.  In particular, I shall use this snapshot to begin development work on the Macintosh.  This will allow me fix long-standing *nix bugs.

This main feature of this release is that Leo represents clones as nodes that
share trees of vnodes. To make this work Leo introduces _positions_. A position
is a location in the traversal of an outline.

This code appears stable.  I have been using the 4.2 code base for several weeks for all my work with no significant problems.  Nevertheless, this _is_ alpha (or even pre-alpha) quality code.  Use at your own risk.  Make frequent backups.

See the "4.2 Projects" node in LeoPy.leo for details of what has been done so far.  I shall be updating documentation more fully for the first beta release.

Leo 4.1 Final              February 20, 2004

Leo 4.1 Final is the culmination of four months of work. No significant bugs
have been reported since 4.1 rc4. Several people have contributed nifty plugins
recently. See leoPlugins.leo for full details.

The highlights of Leo 4.1:

- Leo runs in batch mode when invoked with --script aScriptFile.py
- Leo supports Unicode characters (e.g. Chinese) in path and file names.
- @directives and section references are now valid when executing scripts.
- @ignored and orphan nodes now valid in @file-nosent trees.
- Script-based find/change commands.
- Check Outline command.
- Hoist &amp; DeHoist commands.
- A new gui-agnostic architecture: useful for batch mode and unit tests.
- Several new configuration settings.
- Many new unit tests.
- Excellent new plugins.
- A host of bug fixes.</t>
<t tx="ekr.20031218072017.2565"># The manifest template: specifies all files to be included in the distribution.

# Note: these are glob patterns!  Be careful:  .. may not work.

include __init__.py

include config/leoConfig.leo
include config/leoConfig.txt

include doc/LeoDocs.leo
include doc/README.TXT
include doc/INSTALL.TXT
include doc/PKG-INFO.TXT
include doc/LICENSE.TXT

include Icons/*.*

include plugins/*.*
exclude plugins/*.pyc

include src/LeoPy.leo
include src/leo*.py

include scripts/*
include scripts/install/*.py
include scripts/other/*.py
include scripts/tangle/*.py

include test/test.leo

include install
include uninstall
include manifest.in
include MANIFEST

# Setup is more confusing than helpful.
exclude setup.py</t>
<t tx="ekr.20031218072017.2566">@ignore
@color

import prepareSetup
prepareSetup.setup()

import os

# This _must_ be run from the main leo directory
os.system("python setup.py sdist --formats=zip")
</t>
<t tx="ekr.20031218072017.2567">@first #! /usr/bin/env python
@language python
@color

# Prepare to execute setup.py
import leoGlobals as g
from leoGlobals import true,false

@others

def setup():
	saveAllLeoFiles()
	tangleLeoConfigDotLeo()
	print "preSetup complete"
</t>
<t tx="ekr.20031218072017.2568">def saveAllLeoFiles():
	
	for frame in g.app.windowList:
		c = frame.c
		name = c.mFileName
		if name == "": name = "untitled"
		if c.changed:
			print "saving ",name
			c.save()
</t>
<t tx="ekr.20031218072017.2569">def tangleLeoConfigDotLeo():
	
	from leoGlobals import os_path_join

	c = None
	name = g.os_path_join("config","leoConfig.leo")
	oldtop = g.top()
	for frame in g.app.windowList:
		if frame.c.mFileName == name :
			c = frame.c
			break
	
	if c == None:
		c = g.top()
		flag,frame = g.openWithFileName(name,c)
		if not flag:
			print "can not open ",name
			return
		c = frame.c
			
	print "Tangling ", name
	g.app.setLog(oldtop.frame.log) # Keep sending messages to the original frame.
	c.tangleCommands.tangleAll()
	c.close()
	g.app.setLog(oldtop.frame.log)</t>
<t tx="ekr.20031218072017.2570">@first #! /usr/bin/env python
@language python

@ Script for creating distributions of leo.py using Python's distutils package.
Invoke this script as follows:

import os
os.system(r"cd C:\prog\leoCVS\leo")
os.system("python setup.py sdist --formats=zip")
@c

import leoGlobals as g
from leoGlobals import true,false

from distutils.core import setup
import distutils,os,sys

@others

if 1: # Use this only for final distributions.
	if sys.argv[1] == "sdist":
		setDefaultParams()

# modules = generateModules()
modules = []

setup (
	&lt;&lt; setup info for setup.py &gt;&gt;
)

if sys.argv[1] == "sdist":
	print "setup complete"</t>
<t tx="ekr.20031218072017.2571">name="leo",
version="4.2-a1",
author="Edward K. Ream",
author_email="edream@tds.net",
url="http://personalpages.tds.net/~edream/front.html",
py_modules=modules, # leo*.py also included in manifest
description = "Leo: Literate Editor with Outlines",
licence="Python", # [sic], not license
platforms=["Windows, Linux, Macintosh"],
long_description =
"""Leo is an outline-oriented editor written in 100% pure Python.
Leo works on any platform that supports Python 2.2 or above and the Tk toolkit.
This version of Leo was developed with Python 2.3.3 and Tk 8.4.3.

Download Python from http://python.org/
Download tcl/Tk from http://tcl.activestate.com/software/tcltk/

Leo features a multi-window outlining editor with powerful outline commands,
support for literate programming features, syntax colorizing for many common
languages, unlimited Undo/Redo, an integrated Python shell(IDLE) window,
and many user options including user-definable colors and fonts and user-
definable shortcuts for all menu commands.

Leo a unique program editor, outline editor, literate programming tool,
data manager and project manager. Cloned outlines are a key enabling feature
that make possible multiple views of a project within a single Leo outline.
"""</t>
<t tx="ekr.20031218072017.2572">def printReminders ():

	print
	print "- Update version numbers"
	print "- Clear Default Tangle Directory"
	print "- Distribute both leox-y.zip and leosetup.exe"
	print</t>
<t tx="ekr.20031218072017.2573"># Generate the list of modules in the distribution.

def generateModules():
	
	from leoGlobals import os_path_join,os_path_split,os_path_splitext

	dir = os.getcwd()
	dir = g.os_path_join(dir,"src")
	files = os.listdir(dir)
	modules = []
	for f in files:
		head,tail = g.os_path_split(f)
		root,ext = g.os_path_splitext(tail)
		if tail[0:3]=="leo" and ext==".py":
			modules.append(root)
			
	modules.sort()
	# print "modules:", modules
	return modules
</t>
<t tx="ekr.20031218072017.2574">def replacePatterns (file,pats):

	try:
		path = os.getcwd()
		name  = g.os_path_join(path,file)
		f = open(name)
	except:
		print "*****", file, "not found"
		return
	try:
		data = f.read()
		f.close()
		changed = false
		for pat1,pat2 in pats:
			newdata = data.replace(pat1,pat2)
			if data != newdata:
				changed = true
				data = newdata
				print file,"replaced",pat1,"by",pat2
		if changed:
			f = open(name,"w")
			f.write(data)
			f.close()
	except:
		import traceback ; traceback.print_exc()
		sys.exit()
</t>
<t tx="ekr.20031218072017.2575">def setDefaultParams():

	print "setDefaultParams"

	pats = (
		("create_nonexistent_directories = 1","create_nonexistent_directories = 0"),
		("read_only = 1","read_only = 0"),
		("use_plugins = 1","use_plugins = 0"))

	replacePatterns(g.os_path_join("config","leoConfig.leo"),pats)
	replacePatterns(g.os_path_join("config","leoConfig.txt"),pats)</t>
<t tx="ekr.20031218072017.2576">@first #! /usr/bin/env python
@language python
@color

# Postprocess after executing setup.py

import leoGlobals as g
from leoGlobals import true,false

@others

def setup():
	if 1: # Use this only for final distributions.
		unsetDefaultParams()
	print "postSetup complete"
</t>
<t tx="ekr.20031218072017.2577">def unsetDefaultParams():
	
	from leoGlobals import os_path_join

	print "unsetDefaultParams"
	
	pats = (("use_plugins = 0","use_plugins = 1"),)

	replacePatterns(g.os_path_join("config","leoConfig.leo"),pats)
	replacePatterns(g.os_path_join("config","leoConfig.txt"),pats)</t>
<t tx="ekr.20031218072017.2578">@color
@lineending nl
@language shell</t>
<t tx="ekr.20031218072017.2579">#!/bin/sh

############################################
# This is a small install script to install
# leo on GNU/Linux. 
# Leo is Open Software and is distributed under the terms 
# of the Python License.  Please see:
# docs/LICENSE.TXT for details.
#
# This install script created by Frank Merenda 
# (fmerenda@yahoo.com)
#
# verison 1.0 - 06/30/2003
# - initial creation 
#
# 
# - minor changes to try and use a "prefix" directory
# - step 5 copies the src and config directories as 
# directories rather that file (this seems to prevent
# the need to remove ".." from the python scripts on RH9
# anyway.)
# - IMPORTANT NOTE: I did not understand step 6 so its
# commented out. Someone who knows leo better than I do
# should look at this.
# - Note: I'm a leo newbie so I don't know if this fixes plugin
# problems since I don't think I use them.
# David Holden (dh@iucr.org)
#   
#
############################################


################################
# Variables for usage in this script.
################################
LEO_PREFIX="/usr/local"
LEO_RUN_SCRIPT_SOURCE='./scripts/install/leo-script.txt'
LEO_RUN_SCRIPT_OUTPUT="${LEO_PREFIX}/bin/leo"
LEO_LIB_DIR="${LEO_PREFIX}/lib/leo"


echo ""
echo "Prefix directory set to \"$LEO_PREFIX\""

################################
# Step 1
# Verify the current user is root
################################
CURRENT_USER=$(whoami)

if [ "$CURRENT_USER" = "root" ] ; then
	echo ""
    echo Verified user is root
else
	echo ""
    echo You must be root to run this program
    exit 0;
fi    
   
################################
# Step 2
# Make the directory structure
################################
echo ""
echo Making directory structure $LEO_LIB_DIR

RESULTS=`mkdir -p $LEO_LIB_DIR 2&gt;&amp;1`
if [ $? -ne 0 ]; then
    echo Failure making directory $LEO_LIB_DIR!
    exit 0;
fi
   
################################
# Step 3
# Copy the files
################################
echo ""
echo Copying files.....

RESULTS=`cp -rp * $LEO_LIB_DIR/ 2&gt;&amp;1`
if [ $? -ne 0 ]; then
    echo Failure copying files to $LEO_LIB_DIR
    exit 0;
fi

###############################
# Step 4
# Clean up the duplicate files so it's not
# confusing to the user. These files
# Are copied directly to the main 
# directory. Assume you have permissions
# since you checked above.
###############################
rm -rf $LEO_LIB_DIR/src
rm -rf $LEO_LIB_DIR/config
   
###############################
# Step 5
# Don't make a liar out of me in step 4.
# Copy the files. that you just deleted....   
###############################
cp -rp src $LEO_LIB_DIR/.
cp -rp config $LEO_LIB_DIR/.

###############################
# Step 6
# Add in symbolic links to point to 
# leoConfig and LeoDocs.   
###############################
#mkdir -p /usr/lib/config 
#chmod 777 /usr/lib/config
#ln -sf /$LEO_LIB_DIR/leoConfig.leo /usr/lib/config/leoConfig.leo
#chmod 666 /$LEO_LIB_DIR/leoConfig.leo  
#
#ln -sf /$LEO_LIB_DIR/leoConfig.txt /usr/lib/config/leoConfig.txt
#chmod 666 /$LEO_LIB_DIR/leoConfig.txt  
#
#mkdir -p /usr/lib/doc
#ln -sf $LEO_LIB_DIR/doc/LeoDocs.leo /usr/lib/doc/LeoDocs.leo
#chmod 666 $LEO_LIB_DIR/doc/LeoDocs.leo 
   
################################
# Step 7
# Create the startup script
################################
echo ""
echo Creating startup script located at: $LEO_RUN_SCRIPT_OUTPUT

echo "python ${LEO_PREFIX}/lib/leo/src/leo.py \$1" &gt; $LEO_RUN_SCRIPT_OUTPUT

RESULTS=`chmod 755 $LEO_RUN_SCRIPT_OUTPUT`   
   
echo ""
echo "***** Leo installed successfully - "
echo "      make sure ${LEO_PREFIX}/bin is in your path then"
echo "      type 'leo filename.leo' to use it."   
echo "                                                 *****"
echo ""
exit 0;</t>
<t tx="ekr.20031218072017.2580">#!/bin/sh

############################################
# This is a small install script to install
# leo on GNU/Linux. 
# Leo is Open Software and is distributed under the terms 
# of the Python License.  Please see:
# docs/LICENSE.TXT for details.
#
# This install script created by Frank Merenda 
# (fmerenda@yahoo.com)
#
# verison 1.0 - 06/30/2003
# - initial creation 
#
# 
# - minor changes to try and use a "prefix" directory
# - step 5 copies the src and config directories as 
# directories rather that file (this seems to prevent
# the need to remove ".." from the python scripts on RH9
# anyway.)
# - IMPORTANT NOTE: I did not understand step 6 so its
# commented out. Someone who knows leo better than I do
# should look at this.
# - Note: I'm a leo newbie so I don't know if this fixes plugin
# problems since I don't think I use them.
# David Holden (dh@iucr.org)
#   
#
############################################


################################
# Variables for usage in this script.
################################
LEO_PREFIX="/usr/local"
LEO_RUN_SCRIPT_SOURCE='./scripts/install/leo-script.txt'
LEO_RUN_SCRIPT_OUTPUT="${LEO_PREFIX}/bin/leo"
LEO_LIB_DIR="${LEO_PREFIX}/lib/leo"

echo ""
echo "Prefix directory set to \"$LEO_PREFIX\""

################################
# Step 1
# show commands to remove leo
################################
echo ""
echo "To uninstall leo check the following \"rm\" commands
if they look ok execute them as root."

echo "
rm -fr $LEO_LIB_DIR
rm -f  $LEO_RUN_SCRIPT_OUTPUT

"</t>
<t tx="ekr.20031218072017.2581">@ignore</t>
<t tx="ekr.20031218072017.2582">def getBuildNumber(self):
	c = self
	return c.ver[10:-1] # Strip off "(dollar)Revision" and the trailing "$"

def getSignOnLine (self):
	c = self
	return "Leo 4.2 alpha 1, build %s, April 14, 2004" % c.getBuildNumber()
	
def initVersion (self):
	c = self
	c.ver = "$Revision$" # CVS will update this.
	
def signOnWithVersion (self):

	c = self
	color = g.app.config.getWindowPref("log_error_color")
	signon = c.getSignOnLine()
	n1,n2,n3,junk,junk=sys.version_info
	tkLevel = c.frame.top.getvar("tk_patchLevel")
	
	g.es("Leo Log Window...",color=color)
	g.es(signon)
	g.es("Python %d.%d.%d, Tk %s, %s" % (n1,n2,n3,tkLevel,sys.platform))
	g.enl()</t>
<t tx="ekr.20031218072017.2583">@nocolor</t>
<t tx="ekr.20031218072017.2584">Leo 4.0 final                     October 17, 2003

More than a year in the making, Leo 4.0 is finally here.

Highlights of 4.0 final:
-----------------------

** Improved and simplified format of derived files.
	- Eliminated child indices, extraneous blank lines and @body sentinels.
	- Eliminated @node sentinels that indicate outline structure.
	- New @nl and @nonl sentinels indicate where newlines are and aren't.
	- These changes will largely eliminate unwanted cvs conflicts.

** Greatly improved error handling.
	- Reading derived files _never_ alter outline structure or links.
	- Read errors leave the outline completely unchanged.
	- Broken clone links are gone forever.
	- As a result, 4.0 is much safer than all previous versions.

** Full compatibility will previous versions of Leo.
	- Leo 4.0 reads all derived files properly, regardless of version.
	- Leo writes new-format derived files by default, and this default may be changed.
	- New commands in the read/write menu allow you to explicitly specify the format of derived files.

* New commands:
	- Write 3.x Derived File and Write 4.x Derived File.
	- Import Derived File.
	- Clear Recent Files.

* Dozens of other improvements, including:
	- Better Unicode support.
	- New configuration settings.
	- Several new plugins.

See the notes for the various beta releases for full details.</t>
<t tx="ekr.20031218072017.2585"></t>
<t tx="ekr.20031218072017.2586">Leo 3.12.1 beta 1                     July 25, 2003

This version exists to test the new Linux install scripts and the related distribution stuff.

Leo 3.12                              July 17, 2003

Window sizes are now in pixels rather than grid units, so you must resize existing outlines (.leo files) when opening them for the first time using this version of Leo.  Don't panic!

Highlights of this version:

* Plugged a huge memory leak.
* Fixed a major bug involving undo.
* Added Icon &amp; Status areas to Leo window for use by plugins.
* Important new plugins:
  - The file leoPlugins.leo now contains all plugins.
  - add_directives.py allows plugins to define new directives.
  - color_markup.py supports wiki-styled markup.
  - mod_spelling.py checks spelling (requires aspell to be installed).
  - nav_buttons.py creates browser-style navigation plugins in the icon area.
  - plugins_menu.py creates a Plugins menu items for all loaded plugins.
  - scripts_menu.py creates a Scripts menu for all scripts in scripts folder.
  - spell
  - trace_gc traces all changes to memory at idle time.
* Other enhancements:
  - Redesigned the Find panel.   Non-functional options are dimmed.
  - Added @wrap and @nowrap directives.
  - Added Write Dirty @file Nodes command.
  - Added several new "stub hooks".
  - Hyperlinks are now enabled by default.
  - Leo now loads plugins in alphabetical order.
  - Leo now remembers the size and location of Leo windows.
  - Undo now restores the insert point or the selection range after most commands.
  - Added apply button to Font panel.
  - Improved the reporting of characters that do not exist in the present encoding.
* The usual assortment of bug fixes and minor improvements.
  - There are no known bugs in this version of Leo.</t>
<t tx="ekr.20031218072017.2587">Leo 3.11.1                       May 1, 2003

This version fixes two bugs:
	
- Leo threw an exception at startup on some Linux systems.
- Creating clones by control dragging did not always work.

This code contains permanently disabled 4.0 code.

Leo 3.11                         April 27, 2003

This version of Leo contains many important improvements since 3.10,
especially support for unicode and a new plugin architecture.

The Highlights of 3.11:

** Leo supports unicode properly.
  - New @encoding directives specifies encoding for derived files.
  - New settings specify default encodings for .leo and derived files.
  - Derived files specify encodings used to create them.
** A new plugin architecture for customizing Leo.
- New commands:
  - Toggle Angle Brackets.
  - Insert Time/Date (in headline or body text).
  - Go To First/Last Node, Parent, Next/Previous Sibling.
  - Write Missing @file Nodes.
  - Expand/Contract Node.
- Improved commands:
  - Fixed a huge performance bug that slowed moving nodes left.
  - Expand/Contract commands now operate on the selected tree.
	  ( A major improvement)
  - Sort Siblings command can now sort top-level nodes.
  - Leo now allows multiple writes of cloned nodes.
	  (Useful when different @path directives are in effect.)
- Other improvements:
  - New @lineending directive specifies line endings.
  - Improved syntax coloring for html and xml.
  - Leo scrolls partially visible headlines into full view.
  - Added "Replace tabs with spaces" checkbox in Prefs panel.
- New settings in leoConfig.leo/.txt.
  - Added "tk_encoding" setting and related logic.
  - Colors for Show Invisibibles command and body_insertion_cursor
  - Settings affecting when control-drags start.
  - Defaults for unicode (see above).
- Many other bug fixes and improvements.</t>
<t tx="ekr.20031218072017.2588">Leo 3.10                             December 14, 2002

This version of Leo corrects bugs, improves Leo's documentation and adds many new features:

- Rewrote Scripting Chapter in Leo's Users Guide.
- Improved the Customization Chapter of the Users Guide.
- Adds several customizations contributed by Leo's users.
  Among these: @read-only nodes. Reading empty .leo files.
  Redirecting stderr and stdout to Leo's log pane.
- New Mark Clones and Go To Next Clone commands.
- New Export Headlines command.
- Control-dragging a node now clones it.
- New "Node Only checkbox in the Find/Change panel.
- @root-code trees start in code mode by default.
  This allows @root trees to work like @file trees.
- @root-doc  trees start in doc  mode by default.
- Converted leoConfig.py to use @root-code
- New at_root_bodies_start_in_doc_mode option in leoConfig.py.
  Specifies whether @root trees work like @root-code or @root-doc.
- New synonyms: @file-asis = @silentfile
  @file-nosent = @nosentinelsfile ; @file-noref = @rawfile.
- Leo now supports navigation of menus using underlined menus.
- Added an easy way to replace any Leo method by a function.
  Hooks can now override part of Leo's code!
- Added routines to redirect stderr and stdout to Leo's log pane.
  These routines can be called from hooks.
- Added "event1" and "event2" hooks for customize event handling.
- Improved Leo's window icon, and improved how that icon is loaded.
- Added contributed code to support @read-only nodes.
  This code show how easy it is to customize Leo.
- The usual assortment of bug fixes and minor improvements.
  Actually, this release fixes more than the usual number of bugs.</t>
<t tx="ekr.20031218072017.2589">Leo 3.9                               Nov 23, 2002

This is one of the most interesting versions of Leo ever released:

* Major performance improvements:
  - Incremental syntax coloring speeds response when typing.
  - Incremental undo drastically reduces memory used.

* Major improvements in customizing Leo:
  - Leo looks in the file customizeLeo.py for user-specific customizations.
  - Leo calls "hook routines" in customizeLeo.py for all commands and events.
	These hook routines can modify or replace any command or event.
  - New convenience routines simplify creating and modifying menus.
  - Easy translation of menus to other languages using customizeLeo.py.

* Better integration with other tools:
  - The Open With command allows you to communicate back and forth to other editors.
  - The Go To Line Number command converts lines numbers in derived files
	to locations in the outline.
  - Double-clicking the icon of a @url node launches any url in your web browser.
  - The Execute Script command executes Python code in any body pane.
	This is much more convenient than opening Leo's Idle window.
  - Much better support for cweb. At last, Leo has a power user of cweb.
	By default, @space, @* and @** sections are colored as latex text.
	Leo properly generates @q..@&gt; sentinels.
  - @nosentinelfile is like @file except Leo writes no sentinel lines.

* Other improvements:
  - Optional Emacs-style auto-indent.
  - Reformat Paragraph command.
  - Leo will optionally create nonexistent directories specified in
	@file, @root or @path, including all nonexistent parent directories.
  - Leo will place its own icon in Leo windows provided that you have
	installed Fredrik Lundh's PIL and tkIcon packages.
  - The usual assortment of bug fixes.
</t>
<t tx="ekr.20031218072017.2590">Leo 3.8                                 October 29, 2002

Many major improvements have been made to Leo, all made as the result of user requests:

- New @rawfile and @silentfile trees complement @file trees.
  @rawfile and @silentfile trees create derived files without using sections.
  @rawfile files contain only those sentinels needed to automatically untangle them.
  @silentfile trees contain no sentinels at all.
- New @raw and @end_raw directives allow unformatted code within @file trees.
- Much better support for CWEB.  You may organize .w files using noweb!
- The @comment and @language directives may now apply simultaneously.
- Leo can now read, remember and write &lt;?xml-stylesheet...?&gt; lines,
  under control of the new stylesheet option.
- The new output_newline option specifies the line endings used when writing files.
- The new output_initial_comment option specifies the text to appear
  in an @comment sentinel at the start of each derived file.
- New commands in the help menu make it much easier to change configuration options.
- Dozens of minor improvements and bug fixes.</t>
<t tx="ekr.20031218072017.2591">Leo 3.7                                 October 9, 2002

Many improvements have been made to Leo.  The highlights:

- Now works with Python 2.1.  Previous versions required Python 2.2.
- Many new user options, including user-definable shortcuts for all commands.
  and colors for all parts of Leo's windows.
  As a result, it is now possible to use arrow keys as you desire.
- Minimal support for Unicode Latin-1 (iso-8859-1) encoding. Better support is coming.
- Improved handling of relative path names.
- The @first directive allows lines to precede the opening @+leo sentinel line.
- The @last  directive allows lines to follow  the closing @-leo sentinel line.
- Better support for Perl+pod.
- Leo now ends all lines with '\n' regardless of platform.
- Leo is now compatible with Python 2.1.
- Simplified sentinels reduce spurious CVS diffs.
- Many other minor improvements and bug fixes.
</t>
<t tx="ekr.20031218072017.2592">Leo 3.6                                   September 11, 2002

Highlights:

- Fixed a large number of bugs, especially bugs that appear only on Linux.
- Leo now remembers the previous insertion point and location of the scrollbar when switching between nodes.
- Added Match Brackets command.
- Added support for MouseWheel (Linux only).
- Added support for LaTex and PHP.
- Improved all aspects of the Help menu.
- Discovered a minor bug involving the Python (Idle) window and documented a workaround.
</t>
<t tx="ekr.20031218072017.2593">Leo 3.5                                    August 14, 2002

The many bugs were reported in 3.4 show that  Leo is being heavily used.  This version corrects all known bugs and adds some new features:

- Added new entries in the help menu,
  (Including a link to Joe Orr's excellent ScreenBook tutorial).
- Added configuration options for horizontal scrollbars.
- Added an importFiles script for mass imports.
- Added better warnings for read-only files.
- Removed all '\r' characters when reading derived files.
- Fixed crasher in Read Outline Only command.
- Fixed crasher when leoConfig.txt did not exist.
- Many small improvements and bug fixes.</t>
<t tx="ekr.20031218072017.2594">Leo 3.4                                     August 11, 2002

This version contains many small improvements and bug fixes:

- Fixed several crashers involving Unicode.
- The Show Invisibles command now makes blanks and tabs look much better.
- Created leoConfig.leo, from which leoConfig.txt is now derived.
- Added save_clears_undo_buffer configuration option.
- Fixed a large number of problems with the configuration code.
- The usual minor improvements and bug fixes.</t>
<t tx="ekr.20031218072017.2595">Leo 3.3                                     August 3, 2002

This version of Leo:

- Adds support for Unicode.
- Improved the Import commands.
- Fixed numerous bugs related to configuration settings.
- Fixed the "Javadoc" bug and several latent bugs related to it.</t>
<t tx="ekr.20031218072017.2596">Leo 3.2                                     July 30, 2002

This version generalizes the @others directive, improves the Import command and fixes several bugs.  See the children of this node for full details.

The highlights:

- Nested @others directives are now valid, an important improvement.
  This simplifies files that define more than one class.
- Improved the Import command and squashed several bugs lurking there.
- Made the various Go commands in the Outline-Move/Select menu functional
  by reassigning keyboard shorts
- Fixed a crasher in the Prefs Panel.
- Fixed numerous bugs in the Set Colors command.
- Fixed syntax coloring of C strings that span multiple lines.
- The usual minor improvements and bug fixes.
</t>
<t tx="ekr.20031218072017.2597">Leo 3.1                                     July 20, 2002

This version fixes a blunder that affects only  Leo 3.0.
I recommend that all users of 3.0 upgrade to 3.1.

With this release Leo's to-do list is now empty!
I shall fix bugs as they are reported.
I'll add new features only if convinced that they contribute significantly to Leo.

The highlights:

- Fixed a blunder: Leo 3.0 did nothing when it was opened directly from  Leo.
  (Opening leo using openLeo.py did work.)
- Created a compare panel to control scripts in leoCompare.py.
- Added many new settings in leoConfig.txt to initialize the compare panel.
- The FAQ tells how to add support for new languages.
- The usual minor improvements and bug fixes.</t>
<t tx="ekr.20031218072017.2598">Leo 3.0                                     July 16, 2002

This version is called 3.0 because it can optionally produce files that
can _not_ be read by the  Leo 2.x or the Borland version of Leo.
By default,  Leo 3.0 _does_ produce files that all previous versions of Leo can read.

As always, see LeoDocs.leo for full details.  The highlights:

- Many new user options in leoConfig.txt, including, among others,
  fonts in all panes, colors for syntax coloring and default window size and position.
- Support for .leo files with XML types like "ISO-8859-1", controlled by a user option.
  Note: by default, Leo writes files compatible with previous versions of Leo.
- Powerful new Color and Font pickers, fully connected to user options.
- Added Toggle Split Direction command, under control of user options.
- Added autoscrolling in the outline pane.
- Windows open at the position in which they were saved.
- The size and position of new windows can be controlled with user options.
- Eliminated drawing problems while opening files.
- Improved syntax coloring for @comment plain.
- The Convert All Blanks and Convert All Tabs commands are now undoable.
- Leo warns and aborts if Python 2.2 or above is not running.
- The usual bug fixes.
</t>
<t tx="ekr.20031218072017.2599"></t>
<t tx="ekr.20031218072017.2600">Leo version 2.5.1                           July 7, 2002

This version corrects crashers that affect undo/redo move commands.
Version 2.5 has been withdrawn.

ANYONE USING 2.5 SHOULD IMMEDIATELY SWITCH TO 2.5.1.

Leo version 2.5                             July 7, 2002

See LeoDocs.leo for full details.  The highlights:

- Leo supports tab widths properly, and negative tab widths cause
  Leo to convert tabs to blanks as you type.
- Three new commands appear in the Edit Body menu:
  Convert Tabs, Convert All Tabs and Convert All Blanks.
  Convert All Tabs and Convert All Spaces convert the entire selected tree.
- Leo now allows you to override selected preferences using a
  configuration file called leoConfig.txt.
  Leo acts as before if this file does not exist.
- The Preferences panel is now contains Ok, Cancel and Revert buttons.
- Cut and paste work properly in all situations.
  You can cut and paste between Leo and other applications,
  or between two different copies of Leo.
- Added the Recent Files submenu to the File menu.
- Fixed several crashers.
- Fixed several bugs in the Import commands.
- Leo will no longer abort reading if it detects an invalid directory name
  in the Default Tangle Directory in the Preferences panel.</t>
<t tx="ekr.20031218072017.2601">Leo version 2.4                             June 20, 2002

This version fixes some annoying bugs and adds some nice features:

- Leo now properly highlights the headline of a newly created node.
- The Edit Headline command now works properly.
  Double and triple clicking in a headline now works as expected.
- You can now reorganize drag headlines around.
  You must drag from a node's icon and release on another node's icon.
- You can now open .leo files in  Leo by double clicking on .leo files,
  provided that you associate  Leo with .leo files.
- Improved error recovery when there are errors writing .leo files.
- All parts of LeoDocs.leo now match the documentation on Leo's web site.</t>
<t tx="ekr.20031218072017.2602">Leo version 2.3                             June 12, 2002

This version fixes a minor problem with Leo.

- The code that reads and writes @file nodes now uses the directory containing the
 .leo file as a default when the Default Tangle Directory setting is empty in the Preferences panel.
- The Tangle and Untangle commands have used this convention for a long time.
- This default allows us to distribute LeoPy.leo without specifying
  a directory in the Preferences Panel.</t>
<t tx="ekr.20031218072017.2603">Leo version 2.2                             June 2, 2002

The version fixes two bugs that happen rarely and can cause loss of data when they do happen.

- In certain circumstances  Leo v2.1 would delete most of an outline when
  a node was moved in front of the previous root node!
- All previous versions of Leo will crash when saving body text containing unicode characters.
  This could occur as the result of cutting and pasting text from another application into the body pane.
- Leo now writes body text containing unicode characters using Python's u-prefixed notation.
  That is, the body text is written as: u'escaped_text', where escaped text replaces unicode characters
  not in the ascii character set by escape sequences of the form \uxxxx.
- The result contains nothing but ascii characters, so Leo will have no problem reading it.
  Naturally, compilers and other tools may not understand Python's notation,
  so you may have to convert escaped text to something that your tools can understand.

Edward K. Ream</t>
<t tx="ekr.20031218072017.2604"></t>
<t tx="ekr.20031218072017.2605">@first #! /usr/bin/env python

"""Entry point for Leo in Python."""

@language python

&lt;&lt; Import pychecker &gt;&gt;

# Warning: do not import any Leo modules here!
# Doing so would make g.app invalid in the imported files.

import os,string,sys

@others

if __name__ == "__main__":
	if len(sys.argv) &gt; 1:
		if sys.platform=="win32": # Windows
			fileName = string.join(sys.argv[1:],' ')
		else:
			fileName = sys.argv[1]
		run(fileName)
	else:
		run()



</t>
<t tx="ekr.20031218072017.2608">@first # -*- coding: utf-8 -*-

@language python

import leoGlobals as g
from leoGlobals import true,false

import os,sys

class LeoApp:

	"""A class representing the Leo application itself.
	
	Ivars of this class are Leo's global variables."""
	
	@others
</t>
<t tx="ekr.20031218072017.2620">"""Classes to read and write @file nodes."""

@language python

import leoGlobals as g
from leoGlobals import true,false

if g.app.config.use_psyco:
	# print "enabled psyco classes",__file__
	try: from psyco.classes import *
	except ImportError: pass

import leoColor,leoNodes
import filecmp,os,string,time

&lt;&lt; global atFile constants &gt;&gt;

class baseAtFile:
	"""The base class for the top-level atFile subcommander."""
	&lt;&lt; class baseAtFile methods &gt;&gt;
	
class atFile (baseAtFile):
	pass # May be overridden in plugins.
	
class baseOldDerivedFile:
	"""The base class to read and write 3.x derived files."""
	&lt;&lt; class baseOldDerivedFile methods &gt;&gt;
	
class oldDerivedFile(baseOldDerivedFile):
	pass # May be overridden in plugins.
	
class baseNewDerivedFile(oldDerivedFile):
	"""The base class to read and write 4.x derived files."""
	&lt;&lt; class baseNewDerivedFile methods &gt;&gt;

class newDerivedFile(baseNewDerivedFile):
	pass # May be overridden in plugins.
</t>
<t tx="ekr.20031218072017.2794">"""Syntax coloring routines for Leo."""

@language python

import leoGlobals as g
from leoGlobals import true,false

import re
import string

# php_re = re.compile("&lt;?(\s|=|[pP][hH][pP])")
php_re = re.compile("&lt;?(\s[pP][hH][pP])")

&lt;&lt; define leo keywords &gt;&gt;
&lt;&lt; define colorizer constants &gt;&gt;

@others</t>
<t tx="ekr.20031218072017.2810">@language python

import leoGlobals as g
from leoGlobals import true,false

if g.app.config.use_psyco:
	# print "enabled psyco classes",__file__
	try: from psyco.classes import *
	except ImportError: pass

import leoAtFile,leoFileCommands,leoImport,leoNodes,leoTangle,leoUndo
import os
import string
import sys
import tempfile

class baseCommands:
	"""The base class for Leo's main commander."""
	@others

class Commands (baseCommands):
	"""A class that implements most of Leo's commands."""
	pass</t>
<t tx="ekr.20031218072017.3001">@language python

import leoGlobals as g
from leoGlobals import true,false

import ConfigParser,exceptions,os,string,sys

class baseConfig:
	"""The base class for Leo's configuration handler."""
	&lt;&lt; define defaultsDict &gt;&gt;
	@others
	
class config (baseConfig):
	"""A class to manage configuration settings."""
	pass</t>
<t tx="ekr.20031218072017.3018">@language python

import leoGlobals as g
from leoGlobals import true,false

if g.app.config.use_psyco:
	# print "enabled psyco classes",__file__
	try: from psyco.classes import *
	except ImportError: pass

import leoNodes
import os,string,time

@ The list of language names that are written differently from the names in language_delims_dict in leoGlobals.py.  This is needed for compatibility with the borland version of Leo.

We convert from names in xml_language_names to names in language_delims_dict by converting the name to lowercase and by removing slashes.
@c

xml_language_names = (
	"CWEB","C","HTML","Java","LaTeX",
	"Pascal","PerlPod","Perl","Plain","Python","tcl/tk")

class BadLeoFile(Exception):
	def __init__(self, message):
		self.message = message
		Exception.__init__(self,message) # 4/26/03: initialize the base class.
	def __str__(self):
		return "Bad Leo File:" + self.message

class baseFileCommands:
	"""A base class for the fileCommands subcommander."""
	@others
	
class fileCommands (baseFileCommands):
	"""A class creating the fileCommands subcommander."""
	pass
</t>
<t tx="ekr.20031218072017.3052">@language python

import leoGlobals as g
from leoGlobals import true,false

&lt;&lt; Theory of operation of find/change &gt;&gt;

class leoFind:

	"""The base class for Leo's Find commands."""

	@others</t>
<t tx="ekr.20031218072017.3072">def doFindScript (self):

	g.app.searchDict["type"] = "find"
	self.runFindScript()

def doFindAllScript (self):

	"""The user has just pressed the Find All button with script-find radio button checked.

	N.B. Only this code is executed."""

	g.app.searchDict["type"] = "findAll"
	while 1:
		self.runFindScript()
		if not g.app.searchDict.get("continue"):
			break

def runFindScript (self):

	c = self.c
	try:
		exec c.find_text in {} # Use {} to get a pristine environment.
	except:
		g.es("exception executing find script")
		g.es_exception(full=false)
		g.app.searchDict["continue"] = false # 2/1/04
</t>
<t tx="ekr.20031218072017.3093">@first # -*- coding: utf-8 -*-

"""Global constants, variables and utility functions used throughout Leo."""

@language python

import leoGlobals as g # So code can use g below.
# true,false defined below.

import os,string,sys,time,traceback,types

&lt;&lt; define general constants &gt;&gt;

app = None # The singleton app object.

# Visible externally so plugins may add to the list of directives.

globalDirectiveList = [
	"color", "comment", "encoding", "header", "ignore",
	"language", "lineending", "nocolor", "noheader", "nowrap",
	"pagewidth", "path", "quiet", "root", "silent",
	"tabwidth", "terse", "unit", "verbose", "wrap"]

@others</t>
<t tx="ekr.20031218072017.3206">@language python

import leoGlobals as g
from leoGlobals import true,false

import string

class baseLeoImportCommands:
	"""The base class for Leo's import commands."""
	@others
	
class leoImportCommands (baseLeoImportCommands):
	"""A class that implements Leo's import commands."""
	pass</t>
<t tx="ekr.20031218072017.3320">@language python

&lt;&lt; About the vnode and tnode classes &gt;&gt;
&lt;&lt; About clones &gt;&gt;

import leoGlobals as g
from leoGlobals import true,false

if g.app.config.use_psyco:
	# print "enabled psyco classes",__file__
	try: from psyco.classes import *
	except ImportError: pass

import string,time,types

@others</t>
<t tx="ekr.20031218072017.3439">"""Install and run Leo plugins.

On startup:
- doPlugins() calls loadHandlers() to import all
  mod_XXXX.py files in the Leo directory.

- Imported files should register hook handlers using the
  registerHandler and registerExclusiveHandler functions.
  Only one "exclusive" function is allowed per hook.

After startup:
- doPlugins() calls doHandlersForTag() to handle the hook.
- The first non-None return is sent back to Leo.
"""

import leoGlobals as g
from leoGlobals import true,false

handlers = {}

def doPlugins(tag,keywords):
	if g.app.killed:
		return
	if tag == "start1":
		loadHandlers()
	return doHandlersForTag(tag,keywords)
		
@others</t>
<t tx="ekr.20031218072017.3446">@language python

# Tangle and Untangle.
import leoGlobals as g
from leoGlobals import true,false

import os,string

&lt;&lt; about Tangle and Untangle &gt;&gt;
&lt;&lt; constants &amp; synonyms &gt;&gt;

@others</t>
<t tx="ekr.20031218072017.3603">@language python

# Undo manager for leo.py.

&lt;&lt; How Leo implements unlimited undo &gt;&gt;
&lt;&lt; Define optional ivars &gt;&gt;

import leoGlobals as g
from leoGlobals import true,false

import string,types

@others</t>
<t tx="ekr.20031218072017.3625"></t>
<t tx="ekr.20031218072017.3626">import leoGlobals as g
from leoGlobals import true,false

class leoColorPanel:
	
	"""A base class to create Leo's color panel.
	
	Subclasses may create subsidiary panels."""
	
	&lt;&lt; define default color panel data &gt;&gt;

	@others</t>
<t tx="ekr.20031218072017.3630">@language python

"""Leo's base compare class."""

import leoGlobals as g
from leoGlobals import true,false

import difflib,filecmp,os,string

@others</t>
<t tx="ekr.20031218072017.3652">@language python

import leoGlobals as g
from leoGlobals import true,false

import sys,string
	
class leoFontPanel:
	
	"""The base class for Leo's font panel."""

	@others</t>
<t tx="ekr.20031218072017.3655">"""The base classes for all Leo Windows, their body, log and tree panes, key bindings and menus.

These classes should be overridden to create frames for a particular gui."""

import leoGlobals as g
from leoGlobals import true,false

import leoColor,leoMenu,leoNodes,leoUndo
import os,string,sys,time

&lt;&lt; About handling events &gt;&gt;

@others</t>
<t tx="ekr.20031218072017.3719">@first # -*- coding: utf-8 -*-

"""A module containing the base leoGui class.

This class and its subclasses hides the details of which gui is actually being used.
Leo's core calls this class to allocate all gui objects.

Plugins may define their own gui classes by setting g.app.gui."""

import leoGlobals as g
from leoGlobals import true,false

import leoFrame # for null gui.

@others</t>
<t tx="ekr.20031218072017.3748">"""Gui-independent keystroke handling for Leo."""

import leoGlobals as g
from leoGlobals import true,false</t>
<t tx="ekr.20031218072017.3749">"""Gui-independent menu handling for Leo."""

import leoGlobals as g
from leoGlobals import true,false

import string,sys

@others</t>
<t tx="ekr.20031218072017.3812">@language python

import leoGlobals as g
from leoGlobals import true,false

import string
	
class leoPrefs:
	
	&lt;&lt; define leoPrefs constants &gt;&gt;

	"""A base class that creates Leo's preferenes panel."""
	@others</t>
<t tx="ekr.20031218072017.3821"></t>
<t tx="ekr.20031218072017.3822">import leoGlobals as g
from leoGlobals import true,false

import leoColorPanel
import string,Tkinter,tkColorChooser

Tk = Tkinter

&lt;&lt; define gui-dependent color panel data &gt;&gt;

@others</t>
<t tx="ekr.20031218072017.3838">@language python

"""Leo's base compare class."""

import leoGlobals as g
from leoGlobals import true,false

import leoCompare
import Tkinter,tkFileDialog

Tk = Tkinter

class leoTkinterComparePanel (leoCompare.leoCompare):
	
	"""A class that creates Leo's compare panel."""

	@others</t>
<t tx="ekr.20031218072017.3858">@language python

import leoGlobals as g
from leoGlobals import true,false
import string,Tkinter

Tk = Tkinter

@others</t>
<t tx="ekr.20031218072017.3897">import leoGlobals as g
from leoGlobals import true,false

import leoFind, leoTkinterDialog
import string,sys,Tkinter,types

Tk=Tkinter

class leoTkinterFind (leoFind.leoFind,leoTkinterDialog.leoTkinterDialog):

	"""A class that implements Leo's tkinter find dialog."""

	@others</t>
<t tx="ekr.20031218072017.3909">@language python

import leoGlobals as g
from leoGlobals import true,false

import leoFontPanel
import Tkinter,tkFont
import sys,string

Tk = Tkinter

class leoTkinterFontPanel (leoFontPanel.leoFontPanel):
	
	"""A class to create and run a tkinter font panel."""

	@others</t>
<t tx="ekr.20031218072017.3939">@first # -*- coding: utf-8 -*-

# To do: Use config params for window height, width and bar color, relief and width.

@language python

import leoGlobals as g
from leoGlobals import true,false

import leoColor,leoFrame,leoNodes
import leoTkinterMenu,leoTkinterTree
import Tkinter,tkFont
import os,string,sys,time

Tk = Tkinter

@others
</t>
<t tx="ekr.20031218072017.4047">@first # -*- coding: utf-8 -*-

"""Leo's Tkinter Gui module."""

import leoGlobals as g
from leoGlobals import true,false

import leoGui
import leoTkinterColorPanels,leoTkinterComparePanel,leoTkinterDialog
import leoTkinterFind,leoTkinterFontPanel,leoTkinterFrame
import leoTkinterPrefs
import tkFont,Tkinter,tkFileDialog

import string,sys

Tk = Tkinter

class tkinterGui(leoGui.leoGui):
	
	"""A class encapulating all calls to tkinter."""
	
	@others</t>
<t tx="ekr.20031218072017.4099">"""Tkinter keystroke handling for Leo."""

import leoGlobals as g
from leoGlobals import true,false</t>
<t tx="ekr.20031218072017.4100">"""Tkinter menu handling for Leo."""

import leoGlobals as g
from leoGlobals import true,false

import leoMenu
import Tkinter

class leoTkinterMenu (leoMenu.leoMenu):
	"""A class that represents a Leo window."""
	@others</t>
<t tx="ekr.20031218072017.4122">@language python

import leoGlobals as g
from leoGlobals import true,false

import leoPrefs
import string,Tkinter
Tk = Tkinter

class leoTkinterPrefs (leoPrefs.leoPrefs):

	"""A class that creates Leo's preferenes panel."""

	@others</t>
<t tx="ekr.20031218072017.4138">@language python

&lt;&lt; about the tree classes &gt;&gt;

import leoGlobals as g
from leoGlobals import true,false

if g.app.config.use_psyco:
	# print "enabled psyco classes",__file__
	try: from psyco.classes import *
	except ImportError: pass

import leoFrame
import Tkinter,tkFont
import os,string,sys,types

&lt;&lt; about drawing &gt;&gt;
&lt;&lt; drawing constants &gt;&gt;

class leoTkinterTree (leoFrame.leoTree):
	
	callbacksInjected = false

	"""Leo tkinter tree class."""
	
	@others</t>
<t tx="ekr.20031218072017.4248"># Warning: changes by EKR have not been properly tested!
import leoGlobals as g
from leoGlobals import true,false

import re

&lt;&lt; about this script &gt;&gt;

@others

c = g.top() ; v = c.rootVnode()

s = []
while v:
	s.append(graphvizString(v))
	v = v.next()
s = ''.join(s)

# Look for an @encoding directive.
dict = g.scanDirectives(c,c.rootVnode())
encoding = dict.get("encoding",None)
if encoding is None:
	encoding = g.app.config.default_derived_file_encoding

if 0: # testing
	print s
else:
	gvFile = open('/tmp/leo.dot','w')
	gvFile.write('digraph foo {\n')
	gvFile.write(g.toEncodedString(s,encoding))
	gvFile.write('}\n')
	gvFile.close()</t>
<t tx="ekr.20031218072017.4249">@

http://sourceforge.net/forum/message.php?msg_id=2337165

Here's a simple script to create a graphviz .DOT file from a Leo outline. The
output is in /tmp/leo.dot. You then need to run "dot" (part of the graphviz
package) on the .dot file to produce a graph in whatever format you want (JPEG,
PNG, Postscript, etc).

It's really simple and it doesn't seem to work on leodocs.leo because of some
unicode issues. But anyway, here it is, maybe someone can improve on it.

This code is hereby released as public domain - do whatever you want with it,
but hopefully, improve it and post it back here :-)</t>
<t tx="ekr.20031218072017.4251"># About the only time you should run this script is when:
# - changing the format of timestamps in nodeIndices.setTimestamp or
# - when making a retroactive change to leoID.txt.

import leoGlobals as g
from leoGlobals import true,false

if 0: # This is usually a very bad idea.

	c = g.top() ; v = c.rootVnode()
	while v:
		v.t.fileIndex = None
		v = v.threadNext()
		
	g.es("all timestamps cleared")</t>
<t tx="ekr.20040104184644"># An example of running this script:
import leoGlobals as g
from leoGlobals import true,false

@others

types = (".py",) #,".c",".html",".txt")

dir = "c:/Zope-2.6.2-src/lib/python"
dir = "c:/Zope-2.6.2-src/lib/Components"

importFiles(dir,types,recursive=true)

g.es("done",color="blue")</t>
<t tx="ekr.20040104184913.1">def importFiles (dir,type=None,kind="@file",recursive=false):
	
	c = g.top() ; v = c.currentVnode()

	# Check the params.
	if kind != "@file" and kind != "@root":
		g.es("kind must be @file or @root: " + kind)
		return

	if not g.os_path_exists(dir):
		g.es("directory does not exist: " + dir)
		return
	
	c.beginUpdate()
	root = createLastChildOf(v,"imported files")
	try:
		importDir (dir,type,kind,recursive,root)
		root.contract()
	except:
		g.es_exception()
	c.endUpdate()
</t>
<t tx="ekr.20040104184913.2">def importDir (dir,types,kind,recursive,root):
	
	c = g.top() # Get the commander.
	g.es("dir: " + dir,color="blue")
	
	try:
		files = os.listdir(dir)
		files2 = [] ; dirs =[]
		for f in files:
			path = g.os_path_join(dir,f)
			if g.os_path_isfile(path):
				name, ext = g.os_path_splitext(f)
				if not types or ext in types:
					files2.append(path)
			elif recursive:
				dirs.append(path)
		if len(files2) &gt; 0 or len(dirs) &gt; 0:
			child = createLastChildOf(root,dir)
			c.selectVnode(child)
		if len(files2) &gt; 0:
			c.importCommands.importFilesCommand(files2,kind)
		if len(dirs) &gt; 0:
			dirs.sort()
			for dir in dirs:
				importDir(dir,types,kind,recursive,child)
	except:
		g.es("exception in importFiles script")
		g.es_exception()
</t>
<t tx="ekr.20040104184913.3">def createLastChildOf (v,headline):
	
	child = v.insertAsLastChild()
	child.initHeadString(headline)
	return child
</t>
<t tx="ekr.20040117181936">@nocolor

- Shared nodes working perfectly.
- Perfect import
- Mac/Linux bugs
- @file-thin
- zodb
- Jython

@color

@all</t>
<t tx="ekr.20040130112145">import leoGlobals as g
from leoGlobals import true,false

c = g.top() ; v = c.currentVnode()
last_v = g.app.searchDict.get("v")
if last_v and v == last_v:
	v = v.threadNext()
found = false
while v:
	lines = v.bodyString().split('\n')
	for s in lines:
		i = g.skip_ws(s,0)
		leading = s[0:i]
		if leading:
			blanks, tabs = 0,0
			for ch in leading:
				if ch == ' ':
					blanks += 1
				if ch == '\t':
					tabs += 1 ; break
			if blanks &gt; 0 and tabs &gt; 0:
				# g.trace(leading)
				g.es("blanks precede leading tab: " + v.headString())
				found = true ; break
	if found: break
	v = v.threadNext()
if found:
	g.app.searchDict["v"] = v
	c.selectVnode(v)
	c.redraw()
else:
	g.es("done",color="blue")
	g.app.searchDict["v"] = None
g.app.searchDict["continue"] = false</t>
<t tx="ekr.20040201061928"># Initialize Leo's find panel using the named children of this node.
import leoGlobals as g
from leoGlobals import true,false

g.app.searchDict = {} # Clear dict.get("v") logic.
g.initScriptFind("Find script")

c = g.top()
c.selectVnode(c.rootPosition())
c.redraw()</t>
<t tx="ekr.20040201063019"></t>
<t tx="ekr.20040201063200">def rPrint(node,level):

	indent = "%*s" % (4*level,"")
	print indent + str(node.headString())
	child = node.firstChild()
	while(child):
		rPrint(child,level+1)
		child = child.next()

</t>
<t tx="ekr.20040201063200.1">def newLineize(s):

	return re.sub('"',"'",re.sub(r"\s", r"\n", s))

</t>
<t tx="ekr.20040201063200.2">def graphvizString(node):

	result = []
	child = node.firstChild()
	while child:
		result.append('"%s" -&gt; "%s";\n%s' % (
			newLineize(node.headString()),
			newLineize(child.headString()),
			graphvizString(child)))
		child = child.next()
	return ''.join(result)
</t>
<t tx="ekr.20040201070845"></t>
<t tx="ekr.20040201104001">if 1:
 	dubious line</t>
<t tx="ekr.20040304163125">import leoGlobals as g
from leoGlobals import true,false
import string
c = g.top()

@others

if 1:
	&lt;&lt; set nameList to the list of functions in leoGlobals.py &gt;&gt;
else:
	p = g.findNodeAnywhere("@file leoGlobals.py")
	nameList = findFunctionsInTree(p)

	nameList.sort() ; g.enl()
	for name in nameList: g.es("'%s'," % name)
	
	s = "%d functions in leoGlobals.py" % len(nameList)
	print s ; g.es(s)

if 0:
	p = g.findTopLevelNode(c,"Code")
	g.enl() ; g.enl()
	count = prependNamesInTree(p,nameList,"g.",replace=true) # Just prints if replace==false.
	s = "%d --- done --- " % count
	print s ; g.es(s)</t>
<t tx="ekr.20040304163522">def findDefs(body):
	
	lines = body.split('\n')
	names = []
	for s in lines:
		i = g.skip_ws(s,0)
		if g.match(s,i,"class"):
			return [] # The classes are defined in a single node.
		if g.match(s,i,"def"):
			i = g.skip_ws(s,i+3)
			j = g.skip_c_id(s,i)
			if j &gt; i:
				name = s[i:j]
				if g.match(name,0,"__init__"): 
					return [] # Disallow other class methods.
				names.append(name)
	return names</t>
<t tx="ekr.20040304164949">def prependNamesInTree(p,nameList,prefix,replace=false):
	
	c = p.c
	
	assert(len(prefix) &gt; 0)
	ch1 = string.letters + '_'
	ch2 = string.letters + string.digits + '_'
	def_s = "def " ; def_n = len(def_s)
	prefix_n = len(prefix)
	total = 0
	c.beginUpdate()
	for p in p.self_and_subtree_iter():
		count = 0 ; s = p.bodyString()
		printFlag = false
		if s:
			for name in nameList:
				i = 0 ; n = len(name)
				while 1:
					&lt;&lt; look for name followed by '(' &gt;&gt;
			if count and replace:
				if 0:
					&lt;&lt; print before and after &gt;&gt;
				p.setBodyStringOrPane(s)
				p.setDirty()
		g.es("%3d %s" % (count,p.headString()))
		total += count
	c.endUpdate()
	return total</t>
<t tx="ekr.20040304165432.1">def findFunctionsInTree(p):
	
	nameList = []
	for p in p.self_and_subtree_iter():
		names = findDefs(p.bodyString())
		if names:
			for name in names:
				if name not in nameList:
					nameList.append(name)
	return nameList</t>
<t tx="ekr.20040304173234">print "-"*10,count,p.headString()
print "before..."
print p.bodyString()
print "-"*10,"after..."
print s</t>
<t tx="ekr.20040304173234.1">i = s.find(name,i)
if i == -1:
	break
elif g.match(s,i-1,'.'):
	i += n # Already an attribute.
elif g.match(s,i-prefix_n,prefix):
	i += n # Already preceded by the prefix.
elif g.match(s,i-def_n,def_s):
	i += n # preceded by "def"
elif i &gt; 0 and s[i-1] in ch1:
	i += n # Not a word match.
elif i+n &lt; len(s) and s[i+n] in ch2:
	i += n # Not a word match.
else:
	j = i + n
	j = g.skip_ws(s,j)
	if j &gt;= len(s) or s[j] != '(':
		i += n
	else: # Replace name by prefix+name
		s = s[:i] + prefix + name + s[i+n:]
		i += n ; count += 1
		# g.es('.',newline=false)
		if 1:
			if not printFlag:
				printFlag = true
				# print p.headString()
			print g.get_line(s,i-n)</t>
<t tx="ekr.20040312122501"></t>
<t tx="ekr.20040318150556">import leoGlobals as g
c = g.top()

total,visible = 0,0

if 0: # old way:
	v = c.rootVnode()
	while v:
		total += 1
		v = v.threadNext()
	
	v = c.rootVnode()
	while v:
		visible += 1
		v = v.visNext()
else:
	for p in c.allNodes_iter():
		total += 1
	
	p = c.rootPosition()
	while p:
		visible += 1
		p.moveToVisNext()
	
print "total,visible",total,visible</t>
<t tx="ekr.20040321064134">import leoGlobals as g
c = g.top()

p = g.findTopLevelNode("Code")
tnodes = {} ; count = 0
for p in p.self_and_subtree_iter():
	tnodes[p.v.t]=p.v.t
	count += 1
	
s = "%4s: %d vnodes, %d distinct" % ("Code",count,len(tnodes.keys()))
print s ; g.es(s)

tnodes = {} ; count = 0
for p in c.allNodes_iter():
	tnodes[p.v.t]=p.v.t
	count += 1
		
s = "%4s: %d vnodes, %d distinct" % ("All",count,len(tnodes.keys()))
print s ; g.es(s)</t>
<t tx="ekr.20040321065415">def findNodeInTree(p,headline):

	"""Search for a node in v's tree matching the given headline."""
	
	c = p.c
	for p in p.subtree_iter():
		if p.headString().strip() == headline.strip():
			return p.copy()
	return c.nullPosition()

def findNodeAnywhere(headline):
	
	c = g.top()
	for p in c.allNodes_iter():
		if p.headString().strip() == headline.strip():
			return p.copy()
	return c.nullPosition()
	
def findTopLevelNode(headline):
	
	c = g.top()
	for p in c.rootPosition().self_and_siblings_iter():
		if p.headString().strip() == headline.strip():
			return p.copy()
	return c.nullPosition()</t>
<t tx="ekr.20040327103735.2"></t>
<t tx="ekr.20040330110202">nameList = (
'alert',
'angleBrackets',
'appendToList',
'callerName',
'CheckVersion',
'choose',
'clearAllIvars',
'clear_stats',
'collectGarbage',
'computeLeadingWhitespace',
'computeWidth',
'computeWindowTitle',
'createTopologyList',
'create_temp_name',
'disableIdleTimeHook',
'doHook',
'dump',
'ecnl',
'ecnls',
'enableIdleTimeHook',
'enl',
'ensure_extension',
'es',
'esDiffTime',
'es_error',
'es_event_exception',
'es_exception',
'escaped',
'executeScript',
'file_date',
'findNodeAnywhere',
'findTopLevelNode',
'findNodeInTree',
'findReference',
'find_line_start',
'find_on_line',
'flattenList',
'funcToMethod',
'getBaseDirectory',
'getOutputNewline',
'getTime',
'get_Sherlock_args',
'get_directives_dict',
'get_leading_ws',
'get_line',
'get_line_after',
'getpreferredencoding',
'idleTimeHookHandler',
'importFromPath',
'initScriptFind',
'init_sherlock',
'init_trace',
'isUnicode',
'isValidEncoding',
'is_c_id',
'is_nl',
'is_special',
'is_ws',
'is_ws_or_nl',
'joinLines',
'listToString',
'makeAllNonExistentDirectories',
'makeDict',
'match',
'match_c_word',
'match_ignoring_case',
'match_word',
'module_date',
'openWithFileName',
'optimizeLeadingWhitespace',
'os_path_abspath',
'os_path_basename',
'os_path_dirname',
'os_path_exists',
'os_path_getmtime',
'os_path_isabs',
'os_path_isdir',
'os_path_isfile',
'os_path_join',
'os_path_norm',
'os_path_normcase',
'os_path_normpath',
'os_path_split',
'os_path_splitext',
'pause',
'plugin_date',
'plugin_signon',
'printDiffTime',
'printGc',
'printGcRefs',
'printGlobals',
'printLeoModules',
'print_bindings',
'print_stats',
'readlineForceUnixNewline',
'redirectStderr',
'redirectStdout',
'removeLeadingWhitespace',
'removeTrailingWs',
'reportBadChars',
'restoreStderr',
'restoreStdout',
'sanitize_filename',
'scanAtEncodingDirective',
'scanAtFileOptions',
'scanAtLineendingDirective',
'scanAtPagewidthDirective',
'scanAtRootOptions',
'scanAtTabwidthDirective',
'scanDirectives',
'scanError',
'scanf',
'set_delims_from_language',
'set_delims_from_string',
'set_language',
'shortFileName',
'skip_blank_lines',
'skip_block_comment',
'skip_braces',
'skip_c_id',
'skip_heredoc_string',
'skip_leading_ws',
'skip_leading_ws_with_indent',
'skip_line',
'skip_long',
'skip_matching_delims',
'skip_nl',
'skip_non_ws',
'skip_parens',
'skip_pascal_begin_end',
'skip_pascal_block_comment',
'skip_pascal_braces',
'skip_pascal_string',
'skip_php_braces',
'skip_pp_directive',
'skip_pp_if',
'skip_pp_part',
'skip_python_string',
'skip_string',
'skip_to_char',
'skip_to_end_of_line',
'skip_to_semicolon',
'skip_typedef',
'skip_ws',
'skip_ws_and_nl',
'splitLines',
'stat',
'stdErrIsRedirected',
'stdOutIsRedirected',
'toEncodedString',
'toUnicode',
'toUnicodeFileEncoding',
'top',
'trace',
'trace_tag',
'update_file_if_changed',
'utils_rename',
'windows',
'wrap_lines')</t>
</tnodes>
</leo_file>
