podpourri-schedule-ssh
======================

Synopsis
--------

**podpourri-schedule-ssh** *schedule* *repo-url*


Description
-----------

Forward setup of a schedule for automated container image rebuilds to remote
host via ssh. This is normally called by ``podpourri-schedule``.

Note: :confvalue:`autobuild.sshDestination` must be configured in
**~/.config/podpourri/podpourri.job.conf** (see: :manpage:`podpourri.job.conf(5)`)

See Also
--------

:manpage:`podpourri-schedule(1)`, :manpage:`podpourri.job.conf(5)`
