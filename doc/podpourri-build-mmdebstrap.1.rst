podpourri-build-mmdebstrap
==========================

Synopsis
--------

**podpourri-build-mmdebstrap** *context* *jobtag* *podman* *mmdebstrap* [*mmdebstrap args* ...]


Description
-----------

Uses *mmdebstrap* to build a reproducible base image. The specified *jobtag* is
used to tag the resulting image.

Information is derived from repository whenever possible. I.e.:

- Image name is derived from basename of origin URL.
- An additional image tag is derived from *git branch*. (no builds for
  non-branch refs). Thus when run on ``latest`` branch creates ``latest``
  image tag.

If the file ``sources.list`` is present in the repository, packages are
installed from the specified sources. Defaults to the ``/etc/apt/sources.list``
of the host system.

If the file ``dpkg.cfg`` is present in the repository, it is passed to
`mmdebstrap``s ``--dpkgopt`` command line flag. If not present a built-in
default is used which excludes documentation, locales and lintian rules.

Additional information and automated build setup can be specified in
**~/.config/podpourri/podpourri.conf** (see: :manpage:`podpourri.conf(5)`)

See Also
--------

:manpage:`podpourri.conf(5)`, :manpage:`git(1)`, :manpage:`podpourri-build@.service(8)`
