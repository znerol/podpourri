import os
import shutil
import subprocess
import tempfile
import unittest


class BuildTestCase(unittest.TestCase):
    podman_stub = ''
    workdir = None
    repodir = None
    clonedir = None
    homedir = None
    env = {}

    def setUp(self):
        self.podman_stub = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'stub',
            'podman'
        )

        self.workdir = tempfile.mkdtemp()
        self.repodir = os.path.join(self.workdir, 'my-container-image')

        os.mkdir(self.repodir)

        self._repo_cmd('git', 'init', '-b', 'latest')
        self._repo_cmd('git', 'config', 'user.name', 'Test')
        self._repo_cmd('git', 'config', 'user.email', 'test@localhost')
        self._repo_cmd('git', 'commit', '--quiet',
                       '--allow-empty', '-m', 'Initial commit')

        self.clonedir = os.path.join(self.workdir, 'wd')
        clonecmd = ['git', 'clone', '--quiet', self.repodir, self.clonedir]
        subprocess.check_call(clonecmd)

        self.homedir = os.path.join(self.workdir, 'home')
        os.mkdir(self.homedir)

        self.env = os.environ.copy()
        self.env.update({
            'HOME': self.homedir
        })

    def tearDown(self):
        if self.workdir is not None:
            shutil.rmtree(self.workdir)

    def _repo_cmd(self, *args, **kwds):
        kwds.setdefault('cwd', self.repodir)
        kwds.setdefault('env', self.env)
        return subprocess.check_output(args, **kwds)

    def _wd_cmd(self, *args, **kwds):
        kwds.setdefault('cwd', self.clonedir)
        kwds.setdefault('env', self.env)
        return subprocess.check_output(args, **kwds)

    def testCallsPodmanBuildWithoutPush(self):
        output = self._wd_cmd('podpourri-build', 'context', 'jobtag-xyz',
                              self.podman_stub, '--build-arg=X=Y', '--jobs=0')

        expect_lines = [
            b'PODMAN build called with args: -t my-container-image:jobtag-xyz -t my-container-image:latest --build-arg=X=Y --jobs=0 context',
            b''
        ]

        self.assertEqual(output, b'\n'.join(expect_lines))

    def testCallsPodmanBuildAndPodmanPush(self):
        confdir = os.path.join(self.homedir, '.config', 'podpourri')
        configfile = os.path.join(confdir, 'podpourri.conf')
        confcmd = ['git', 'config', '--file', configfile,
                   'registry.prefix', 'registry.example.com/path/']
        os.makedirs(confdir)
        subprocess.check_call(confcmd)

        output = self._wd_cmd('podpourri-build', 'context', 'jobtag-xyz',
                              self.podman_stub, '--build-arg=X=Y', '--jobs=0')

        expect_lines = [
            b'PODMAN build called with args: -t registry.example.com/path/my-container-image:jobtag-xyz -t registry.example.com/path/my-container-image:latest --build-arg=X=Y --jobs=0 context',
            b'PODMAN push called with args: registry.example.com/path/my-container-image:jobtag-xyz',
            b'PODMAN push called with args: registry.example.com/path/my-container-image:latest',
            b''
        ]

        self.assertEqual(output, b'\n'.join(expect_lines))
