podpourri-build@.service
========================

Synopsis
--------

**podpourri-build-daily@.service**

**podpourri-build-weekly@.service**

**podpourri-build-daily@.timer**

**podpourri-build-weekly@.timer**


Description
-----------

Periodically rebuilds container images.

The instance name (systemd instance string specifier ``%I``) is used as the
repository url.


Environment
-----------

.. envvar:: PODPOURRI_REPO

   URL of the repository where a container image build file is maintained.
   Defaults to the instance specifier.

.. envvar:: PODPOURRI_JOBTAG_PREFIX

   Prefix for tag added to the container image registry and the git repository
   after the build. Defaults to ``build-daily-`` and ``build-weekly-``
   respectively.

Files
-----

.. envfile:: ~/.config/podpourri/env

   Optional environment file shared by all instances and podpourri services.

.. envfile:: ~/.config/podpourri/%i.env

   Optional per-instance environment file shared by all podpourri services.

.. envfile:: ~/.config/podpourri/podpourri-build.env

   Optional per-service environment file shared by all podpourri service
   instances.

.. envfile:: ~/.config/podpourri/%i.podpourri-build.env

   Optional per-instance and per-service environment file.


See Also
--------

:manpage:`podpourri-build(1)`
