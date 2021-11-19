podpourri-hook-post-receive
===========================

Synopsis
--------

**/usr/local/lib/podpourri/git-hooks/post-receive**


Description
-----------

A hook script for :program:`git` designed to run ``podpourri-job`` for each
pushed ref and schedule automated rebuilds using ``podpourri-schedule``.

A build job is run for each pushed branch. The public repository URL is
generated from :confvalue:`repo.basedir` and :confvalue:`repo.baseurl`.

A list of branches considered for automated builds can be specified in
**~/.config/podpourri/podpourri.job.conf** (see: :manpage:`podpourri.job.conf(5)`)

See Also
--------

:manpage:`podpourri-job(1)`, :manpage:`podpourri-schedule(1)`, :manpage:`githooks(5)`
