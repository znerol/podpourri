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

.. confvalue:: autobuild.daily

   Space separated list of branches which should be scheduled for daily
   automated rebuild. Empty by default.

.. confvalue:: autobuild.weekly

   Space separated list of branches which should be scheduled for weekly
   automated rebuild. Empty by default.

.. confvalue:: autobuild.prefix

   Git URL prefix to use when scheduling automated rebuilds. This is used by
   ``podpourri-build`` to determine the fully qualified URL to the repository
   when scheduling automated rebuilds. Note that the value must include a
   terminating separator (i.e., ``/`` or ``:``). E.g., when using gitolite and
   SSH for repository hosting, the value used here should be something like
   ``git@repos.example.com:``. Empty by default.


See Also
--------

:manpage:`podpourri-build(1)`, :manpage:`git-config(1)`
