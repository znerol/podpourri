podpourri-build
===============

Synopsis
--------

**podpourri-build** [*-n*] [*context*] [*jobtag*]


Description
-----------

Reads configuration from ``.podpourri.conf`` file found in the *context*
directory and builds the specified images. Neither pulls nor pushes built images
if ``-n`` is specified. Uses the current directory unless *context* is
specified. Additionally tags the resulting image with *jobtag* if specified.


See Also
--------

:manpage:`podpourri.conf(5)`
