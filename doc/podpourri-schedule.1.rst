podpourri-schedule
==================

Synopsis
--------

**podpourri-schedule**


Description
-----------

Schedules automated builds for the container imague build file found at the
origin URL of the currently checked out git working copy.

Information is derived from repository whenever possible. I.e.:

- Image name is derived from basename of origin URL.
- Image tag is derived from git branch. (no builds for non-branch refs). Thus
  when run on ``latest`` branch creates ``latest`` image tag.

A list of branches considered for automated builds can be specified in
**~/.config/podpourri/podpourri.conf** (see: :manpage:`podpourri.conf(5)`)

By default **podpourri-schedule** uses **podpourri-schedule-systemd-user**
method to configure a timer in the systemd user domain. This behavior can be
overridden from within **~/.config/podpourri/podpourri.conf** as well.

See Also
--------

:manpage:`podpourri.conf(5)`, :manpage:`git(1)`, :manpage:`podpourri-build@.service(8)`
