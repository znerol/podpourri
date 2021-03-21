podpourri-build
===============

Synopsis
--------

**podpourri-build** *context* *jobtag* *podman* [*podman args* ...]


Description
-----------

Uses *podman* to build and push a container image build file found at *context*
directory. The specified *jobtag* is used to tag the resulting image.

Information is derived from repository whenever possible. I.e.:

- Image name is derived from basename of origin URL.
- An additional image tag is derived from *git branch*. (no builds for
  non-branch refs). Thus when run on ``latest`` branch creates ``latest``
  image tag.

Additional information and automated build setup can be specified in
**~/.config/podpourri/podpourri.conf** (see: :manpage:`podpourri.conf(5)`)

See Also
--------

:manpage:`podpourri.conf(5)`, :manpage:`git(1)`, :manpage:`podpourri-build@.service(8)`
