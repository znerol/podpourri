podpourri.job.conf
==================

Description
-----------

Invoked from git post-receive hook and from podpourri systemd unit,
``podpourri-job`` will read configuration from
*$HOME/.config/podpourri/podpourri.job.conf* file if it exists.

The configuration file uses the same syntax as ``git-config``. In fact,
``git-config`` is internally used by ``podpourri`` binaries to read the config,
hence that tool can also be used to query and write the ``podpourri.job.conf``
file.

The following variables can be set in ``podpourri.job.conf`` which influence the
behavior of podpourri:


.. confvalue:: repo.basedir

   Base directory of repository hosting service. The base directory is removed
   from the PWD during execution of ``post-receive`` hook. Empty by default.

.. confvalue:: repo.baseurl

   Public base url of the repository hosting service. The base url is prepended
   after ``repo.basedir`` has been removed to generate the public repo url.
   Empty by default.

.. confvalue:: job.method

   Method used to execute a build job. Possible values are ``local`` (the
   default when empty) and ``ssh``.

.. confvalue:: job.sshDestination

   Required if ``job.method`` is set to ``ssh``. The remote (``user@host``)
   where ``podman-job`` will be run.

.. confvalue:: autobuild.schedules

   List of build schedules. Defaults to ``daily weekly``.

.. confvalue:: autobuild.daily

   Space separated list of branches which should be scheduled for daily
   automated rebuild. Empty by default.

.. confvalue:: autobuild.weekly

   Space separated list of branches which should be scheduled for weekly
   automated rebuild. Empty by default.

.. confvalue:: autobuild.method

   Method used to schedule the autobuild timer. Possible values are
   ``systemd-user`` (the default when empty) or ``systemd-sudo``. The latter
   will use ``sudo podpourri-systemctl --system ...``. Hence the calling user
   needs permission to execute the ``podpourri-systemctl`` script with root
   privileges and without a password. E.g.:

   ::

      podpourri   ALL = (root) NOPASSWD: /usr/local/bin/podpourri-systemctl --system *

   Defaults to ``systemd-user``.

.. confvalue:: autobuild.sshDestination

   Required if ``job.method`` is set to ``ssh``. The remote (``user@host``)
   where ``podman-schedule`` will be run.

See Also
--------

:manpage:`podpourri-job(1)`, :manpage:`podpourri-schedule(1)`,
:manpage:`podpourri-hook-post-receive(8)`,
:manpage:`podpourri-build@.service(8)` :manpage:`git-config(1)`
