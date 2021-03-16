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
  Thus when run on `latest` branch creates `latest` container tag.
- Additional tags can be specified on the command line.

Additional information can be supplied via configfile in
~/.config/podpourri/podpourri.conf:

- Pushes image and tags to registry when registry.prefix is specified in
  config file. Use the following config to push to a registry on localhost:
  [registry]
  	prefix = localhost:5000/
- Enables and starts systemd units which rebuild and push specified branches
  periodically.


See Also
--------

:manpage:`git(1)`, :manpage:`podpourri-build@.service(8)`
