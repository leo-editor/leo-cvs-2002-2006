Leo 4.2 alpha 3           June 1, 2004

This version fixes completes the essential features of version 4.2.  All known incompletions and bugs involving shared nodes and Leo's new file format have been fixed.  BTW, this version of Leo completes Leaps 201 and 202.

It should be safe to use this version for collaboration between Leo's developers.  I hereby encourage people to start using cvs for collaboration.  Only by doing so will we discover any possible problems.

The only item that must be completed before releasing 4.2 beta is fixing the Go To Line Number command so it supports thin derived files.

There are many known bugs in this version: most are minor bugs that have been around for a long time.  All known bugs will be fixed by the first release candidate.  See the to-do list in LeoPy.leo for the complete list.

The highlights of this version:

- All features of @file-thin are now complete and appear to be stable.
	- All .leo files in the distribution use @thin files where possible.
	- Leo ignores all directives within the range of the @all directive.
	- The @+middle and @-middle sentinels allow sections to be defined in any descendant node.
	- The @clone sentinel marks duplicate cloned siblings.
- The beginnings of a new undo scheme are in place.
- @thin, @nosent, @noref and @asis are abbreviations for @file-thin, @file-nosent, @file-noref and @file-asis.
- Created new iterators that return lists of vnodes and tnodes, including iterators that remove all duplicates from those lists.