import os
import re
import shutil
import shutil
import subprocess
import tempfile
import unittest


class BuildTestCase(unittest.TestCase):
    podman_stub = ''
    mmdebstrap_stub = ''
    stubdir = ''
    workdir = None
    repodir = None
    clonedir = None
    homedir = None
    env = {}

    def setUp(self):
        self.stubdir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'stub',
        )
        self.podman_stub = os.path.join(self.stubdir, 'podman')
        self.mmdebstrap_stub = os.path.join(self.stubdir, 'mmdebstrap')

        self.workdir = tempfile.mkdtemp()
        self.repodir = os.path.join(self.workdir, 'my-container-image')

        os.mkdir(self.repodir)

        self._repo_cmd('git', 'init', '--bare', '-b', 'latest')

        self.clonedir = os.path.join(self.workdir, 'wd')
        clonecmd = ['git', 'clone', '--quiet', self.repodir, self.clonedir]
        subprocess.check_call(clonecmd)

        shutil.copyfile(
            os.path.join(self.stubdir, 'scratch', 'dpkg.cfg'),
            os.path.join(self.clonedir, 'dpkg.cfg')
        )
        shutil.copyfile(
            os.path.join(self.stubdir, 'scratch', 'sources.list'),
            os.path.join(self.clonedir, 'sources.list')
        )
        self._wd_cmd('git', 'config', 'user.name', 'Test')
        self._wd_cmd('git', 'config', 'user.email', 'test@localhost')
        self._wd_cmd('git', 'add', 'sources.list', 'dpkg.cfg')
        self._wd_cmd('git', 'branch', '-m', 'latest')
        self._wd_cmd('git', 'commit', '-m', 'Add sources.list and dpkg.cfg')
        self._wd_cmd('git', 'push', '--quiet', 'origin', 'HEAD')

        self.homedir = os.path.join(self.workdir, 'home')
        os.mkdir(self.homedir)

    def tearDown(self):
        if self.workdir is not None:
            shutil.rmtree(self.workdir)

    def _env(self, **kwds):
        env = os.environ.copy()
        if self.homedir:
            env.update({
                'HOME': self.homedir
            })
        env.update(kwds)
        return env

    def _repo_cmd(self, *args, **kwds):
        kwds.setdefault('cwd', self.repodir)
        kwds.setdefault('env', self._env())
        return subprocess.check_output(args, **kwds)

    def _wd_cmd(self, *args, **kwds):
        kwds.setdefault('cwd', self.clonedir)
        kwds.setdefault('env', self._env())
        return subprocess.check_output(args, **kwds)

    def testCallsMmdebstrapdWithoutPush(self):
        epoch="1234567890"
        # incorrect shasum for given epoch
        shasum="0123456789abcdef"

        output = self._wd_cmd('podpourri-build-mmdebstrap', self.clonedir, 'jobtag-xyz',
                              self.podman_stub, self.mmdebstrap_stub, env=self._env(
                                  SOURCE_DATE_EPOCH=epoch,
                                  PODMAN_STUB_SHA256_SUM=shasum
                              ))

        expect_lines = [
            b'PODMAN pull called with args: my-container-image:latest',
            b'PODMAN import called with args: [^ ]+\\.tar my-container-image:jobtag-xyz my-container-image:latest',
        ]

        self.assertRegex(output, b'^' + b'\n'.join(expect_lines) + b'\n$')

    def testDoesNotImportBuiltImageIfShasumMatches(self):
        epoch="1234567890"
        # correct shasum for given epoch
        shasum="e1a8cd773fb9663d7b2b71fd41f3e5b3c9b9302dda1c4b0c4a57f6af1126f89e"

        output = self._wd_cmd('podpourri-build-mmdebstrap', self.clonedir, 'jobtag-xyz',
                              self.podman_stub, self.mmdebstrap_stub, env=self._env(
                                  SOURCE_DATE_EPOCH=epoch,
                                  PODMAN_STUB_SHA256_SUM=shasum
                              ))

        expect_lines = [
            b'PODMAN pull called with args: my-container-image:latest',
        ]

        self.assertRegex(output, b'^' + b'\n'.join(expect_lines) + b'\n$')
