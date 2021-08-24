podpourri-job-ssh
=================

Synopsis
--------

**podpourri-job-ssh** *job-tag-prefix* *repo-url*


Description
-----------

Forward job execution to remote host via ssh. This is normally called by
``podpourri-job``.

Note: :confvalue:`job.sshDestination` must be configured in
**~/.config/podpourri/podpourri.conf** (see: :manpage:`podpourri.conf(5)`)

See Also
--------

:manpage:`podpourri-job(1)`, :manpage:`podpourri.conf(5)`, :manpage:`podpourri-build(1)`
