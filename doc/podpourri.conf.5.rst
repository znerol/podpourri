.podpourri.conf
===============

Description
-----------

When building container images ``podpourri-build`` will read configuration from
*./podpourri.conf* at the base of the given ``context``.

The configuration file uses the same syntax as ``git-config``. In fact,
``git-config`` is internally used by ``podpourri`` binaries to read the config,
hence that tool can also be used to query and write the ``podpourri.job.conf``
file.

The following variables can be set in ``.podpourri.conf`` which influence the
behavior of podpourri:

Section ``podpourri``:

.. confValue:: podpourri.image

   Name of an image to be built. This option can be repeated multiple times in
   order to build multiple images from the same repository in one job.
   Additional details for individual image builds can be specified in
   ``podpourri-image`` subsections where subsection name is the image name.

.. confValue:: podpourri.pull

   Name of an image which should be pulled before the build. This option can be
   repeated multiple times in order to pull multiple images.

.. confValue:: podpourri.pullExcludeJobPrefix

   Prefixes of job tags when the image-pull step is to be skipped. This option
   can be repeated multiple times in order to specify several job prefixes.
   Specify ``pullExcludeJobPrefix = build-push-`` to disable pulling images
   when new refs are pushed to the repository while keep pulling images during
   automatic rebuilds.

.. confvalue:: podpourri.registryPrefix

   Prefix for all images built by ``podpourri-build``. When set, images built
   will be pushed to that container image registry after the build. Note that
   the value must include a terminating separator. In order to push images to a
   registry running on localhost on port 5000, use the following value:
   ``localhost:5000/``. Empty by default.

Subsection ``podpourri-image.<name>``:

.. confValue:: podpourri-image.<name>.method

   Method used to build an image. Possible values are ``podman`` (the default
   when empty) and ``mmdebstrap``.

.. confValue:: podpourri-image.<name>.cache

   Whether or not it is attempted to pull the image from the registry before the
   build. Default depends on the build method: ``false`` for ``podman`` and
   ``true`` for ``mmdebstrap``.

Subsection ``podpourri-image.<name>`` additional options if ``method`` is
``podman``:

.. confValue:: podpourri-image.<name>.context

   Build context to use. Defaults to the project root directory.

.. confValue:: podpourri-image.<name>.containerfile

   Containerfile / Dockerfile to use. Defaults to the build context.

Subsection ``podpourri-image.<name>`` additional options if ``method`` is
``mmdebstrap``:

.. confValue:: podpourri-image.<name>.dpkgOptFile

   A file containing default options for dpkg. Defaults to a file with the
   following contents:

   ::

      path-exclude=/usr/share/man/*
      path-include=/usr/share/man/man[1-9]/*
      path-exclude=/usr/share/locale/*
      path-include=/usr/share/locale/locale.alias
      path-exclude=/usr/share/{doc,info,man,omf,help,gnome/help}/*
      path-include=/usr/share/doc/*/copyright
      path-exclude=/usr/share/lintian/*
      path-exclude=/usr/share/linda/*

.. confValue:: podpourri-image.<name>.aptSourcesFile

   A ``sources.list`` file used by ``apt`` to install packages from. Defaults to
   a file with the following contents:

   ::

      deb https://deb.debian.org/debian bookworm main
      deb https://security.debian.org/debian-security bookworm-security main


Examples
========

With the following ``.podpourri.conf`` one image with the name ``simple`` is
built using a ``Containerfile`` / ``Dockerfile`` at the repository root:

.. code-block:: ini

   [podpourri]
      image = simple

With the following ``.podpourri.conf`` file two images are built ``myapp-ui``
and ``myapp-api``. If successfull, they get pushed to ``registry.example.com``.

.. code-block:: ini

   [podpourri]
      registryPrefix = registry.example.com/
      image = myapp-api
      image = myapp-ui

   [podpourri-image "myapp-api"]
      context = app
      containerfile = app/Containerfile.api

   [podpourri-image "myapp-ui"]
      context = app
      containerfile = app/Containerfile.ui


See Also
--------

:manpage:`podpourri-build(1)`, :manpage:`git-config(1)`
