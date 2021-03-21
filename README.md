# podpourri - Simple git based container image build service

A collection of scripts and systemd units which make it easy to setup a
centralized container image build service with git.

## DEPENDENCIES

Podpourri requires `podman`, `git` and [git-gau].

## INSTALL

Navigate to the releases page and pick the latest `podpourri-dist.tar.gz`
tarball. Copy it to the target machine and unpack it there.

    $ scp dist/podpourri-dist.tar.gz me@example.com:~
    $ ssh me@example.com sudo tar -C /usr/local -xzf ~/podpourri-dist.tar.gz

## BUILD

*Preferred method*: Build a distribution tarball, copy it to the target machine
and unpack it there.

    $ make dist
    $ scp dist/podpourri-dist.tar.gz me@example.com:~
    $ ssh me@example.com sudo tar -C /usr/local -xzf ~:podpourri-dist.tar.gz

*Alternative method*: Check out this repository on the traget machine and
install it directly. The destination directory can be changed with the `prefix`
variable in order to change the installation prefix to something else than
`/usr/local`.

    $ make all
    $ sudo make prefix=/opt/local install

[Sphinx] is necessary in order to build the man pages and the users guide. This
step can be skipped by using the `install-bin` target.

[git-gau]: https://github.com/znerol/git-gau
[Sphinx]: https://www.sphinx-doc.org/
