==================================================================
urlcheck: A quick url page checker.
==================================================================

urlcheck is a simple command-line utility for checking this links within
one or a series of .html files and verifying that there are no broken links.

It can also be used to check .html files in the current working directory or
take user-supplied urls to check remotely.

Installation
------------

The easiest way to install most Python packages is via ``easy_install`` or ``pip``::

    $ easy_install urlcheck
    
    |or|
    
    $ pip install urlcheck

Usage
-----

Example use-cases::

    $ urlcheck
    
    |or|
    
    $ urlcheck -c
    look in the current directory for any .html files and check their links
    
    $ urlcheck -l file1.html file2.html ...
    take user-supplied .html files and check their links
    
    $ urlcheck -r http://url1.com http://url2.com ...
    take user-supplied urls and check their links
    
    $ urlcheck -v
    enables verbose output
    
    $ urlcheck -h for help


Example output::

    $ [filename]
    $ [RESPONSE CODE] :: [url]
    
    $ [ERRORS] (if any)
    
    -- [ NO ERRORS FOUND ] --
    
    $ urlcheck for file1.html
    $ 200 :: http://andrewtlyman.com
    $ 200 :: http://github.com/nerdylawman
    $ 302 :: http://horriblevacuum.com
    
    $ -------
    $ RESULT for file1.html
    
    $ Everything checks out!
    
    $ urlcheck for file2.html
    ...
    ..
    .
    
    -- [ ERRORS FOUND ] --
    
    $ urlcheck for file1.html
    
    $ 200 :: http://horriblevacuum.com
    $ 404 :: http://badlink.com
    $ 500 :: http://crashedserver.com
    
    $ -------
    $ RESULT for file1.html
    
    $ Found 2 ERRORS in file1.html:
    
    $ 404 :: http://badlink.com
    $ 500 :: http://crashedserver.com
    
    $ file2.html
    ...
    ..
    .