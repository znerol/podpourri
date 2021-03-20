podpourri-build
===============

Synopsis
--------

**podpourri-build** *context* *podman* [*additional-tags* ...]


Description
-----------

Uses *podman* to build and push an image from spec found at *context*
directory.

Information is derived from repository whenever possible. I.e.:

- Image name is derived from basename of origin URL.
- Image tag is derived from git branch. (no builds for non-branch refs).
  Thus when run on ``latest`` branch creates ``latest`` image tag.
- Additional tags can be specified on the command line.

Additional information and automated build setup can be specified in
**~/.config/podpourri/podpourri.conf** (see: :manpage:`podpourri.conf(5)`)

See Also
--------

:manpage:`podpourri.conf(5)`, :manpage:`git(1)`, :manpage:`podpourri-build@.service(8)`
