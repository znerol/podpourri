podpourri-build
===================

Synopsis
--------

**podpourri-build** [*additional-tags* ...]


Description
-----------

Builds and pushes container from spec found at git toplevel directory.

Information is derived from repository whenever possible. I.e.:

- Image name is derived from basename of origin URL.
- Container tag is derived from git branch. (no builds for non-branch refs).
  Thus when run on ``latest`` branch creates ``latest`` container tag.
- Additional tags can be specified on the command line.

Additional information and automated build setup can be specified in
**~/.config/podpourri/podpourri.conf** (see: :manpage:`podpourri.conf(5)`)

See Also
--------

:manpage:`podpourri.conf(5)`, :manpage:`git(1)`, :manpage:`podpourri-build@.service(8)`
