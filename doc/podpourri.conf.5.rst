podpourri.conf
==============

Description
-----------

When building container images ``podpourri-build`` will read configuration from
*$HOME/.config/podpourri/podpourri.conf* file if it exists.

The configuration file uses the same syntax as ``git-config``. In fact,
``git-config`` is internally used by ``podpourri-build`` to read the config,
hence that tool can also be used to query and write the ``podpourri.conf``
file.

The following variables can be set in ``podpourri.conf`` which influence the
behavior of podpourri:


.. confvalue:: registry.prefix

   Prefix for all images built by ``podpourri-build``. When set, images built
   will be pushed to that container image registry after the build. Note that
   the value must include a terminating separator. In order to push images to a
   registry running on localhost on port 5000, use the following value:
   ``localhost:5000/``. Empty by default.

.. confvalue:: repo.basedir

   Base directory of repository hosting service. The base directory is removed
   from the PWD during execution of ``post-receive`` hook. Empty by default.

.. confvalue:: repo.baseurl

   Public base url of the repository hosting service. The base url is prepended
   after ``repo.basedir`` has been removed to generate the public repo url.
   Empty by default.

.. confvalue:: job.method

   Method used to execute a build job. Possible values are ``local`` (the
   default when empty).

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
   will use ``sudo podpourri-systemctl systemctl --system ...``. Hence the
   calling user needs permission to execute the ``podpourri-systemctl`` script
   with root privileges and without a password. E.g.:

      podpourri   ALL = NOPASSWD: /usr/local/bin/podpourri-systemctl

   Defaults to ``systemd-user``.


See Also
--------

:manpage:`podpourri-build(1)`, :manpage:`git-config(1)`
