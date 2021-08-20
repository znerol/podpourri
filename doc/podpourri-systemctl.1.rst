podpourri-systemctl
===================

Synopsis
--------

**podpourri-systemctl** *systemctl* *--user|--system* *daily|weekly* *repo-url* *branch*


Description
-----------

Uses *systemctl* to setup timers for automated container image rebuilds in the
desired systemd domain. This is normally called by
``podpourri-schedule-systemd-user`` and ``podpourri-schedule-systemd-sudo``
respectively.

See Also
--------

:manpage:`podpourri-schedule(1)`
