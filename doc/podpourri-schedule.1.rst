podpourri-schedule
==================

Synopsis
--------

**podpourri-schedule** *schedule* *repo-url*


Description
-----------

Schedules automated builds for the container image build file found in the given
*repo-url*.


By default **podpourri-schedule** uses **podpourri-schedule-systemd-user**
method to configure a timer in the systemd user domain. This behavior can be
overridden from within **~/.config/podpourri/podpourri.conf** as well.

See Also
--------

:manpage:`podpourri.conf(5)`, :manpage:`git(1)`, :manpage:`podpourri-build@.service(8)`
