bpython - A fancy curses interface to the Python interactive interpreter
========================================================================

This is a fork of bpython for use with Hy (http://docs.hylang.org/en/latest/).

See http://bitbucket.org/bobf/bpython/ for the real bpython.

CLI Windows Support
===================

Dependencies
------------
Curses
    Use the appropriate version compiled by Christoph Gohlke
    http://www.lfd.uci.edu/~gohlke/pythonlibs/

pyreadline
    Use the version in the cheeseshop
    http://pypi.python.org/pypi/pyreadline/

Recommended
-----------
Obtain the less program from GnuUtils. This makes the pager work as intended.
It can be obtained from cygwin or GnuWin32 or msys

Current version is tested with
------------------------------
 * Curses 2.2
 * pyreadline 1.7

Curses Notes
------------
The curses used has a bug where the colours are displayed incorrectly:
 * red  is swapped with blue
 * cyan is swapped with yellow

To correct this I have provided my windows.theme file.

This curses implementation has 16 colors (dark and light versions of the
colours)


