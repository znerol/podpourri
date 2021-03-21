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

    def setUp(self):
      self.podman_stub = os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        'stub',
        'podman'
      )

      self.workdir = tempfile.mkdtemp()
      self.repodir = os.path.join(self.workdir, 'my-container-image')

      os.mkdir(self.repodir)

      self._repo_cmd('git', 'init')
      self._repo_cmd('git', 'config', 'user.name', 'Test')
      self._repo_cmd('git', 'config', 'user.email', 'test@localhost')
      self._repo_cmd('git', 'symbolic-ref', 'HEAD', 'refs/heads/latest')
      self._repo_cmd('git', 'commit', '--allow-empty', '-m', 'Initial commit')

      self.clonedir = os.path.join(self.workdir, 'wd')
      clonecmd = ['git', 'clone', self.repodir, self.clonedir]
      subprocess.check_call(clonecmd)


    def tearDown(self):
        if self.workdir is not None:
            shutil.rmtree(self.workdir)

    def _repo_cmd(self, *args, **kwds):
        kwds.setdefault('cwd', self.repodir)
        return subprocess.check_output(args, **kwds)

    def _wd_cmd(self, *args, **kwds):
        kwds.setdefault('cwd', self.clonedir)
        return subprocess.check_output(args, **kwds)

    def testCallsPodmanBuildAndPodmanPush(self):
        output = self._wd_cmd('podpourri-build', 'context', 'jobtag-xyz',
                           self.podman_stub, '--build-arg=X=Y', '--jobs=0')

        expect_lines = [
          b'PODMAN build called with args: -t my-container-image:jobtag-xyz -t my-container-image:latest --build-arg=X=Y --jobs=0 context',
          b''
        ]

        self.assertEqual(output, b'\n'.join(expect_lines))
