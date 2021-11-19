import os
import shutil
import subprocess
import tempfile
import unittest


class ScheduleSystemdTestCase(unittest.TestCase):
    stub_method_path = ""
    workdir = None
    repodir = None
    clonedir = None
    homedir = None
    env = {}

    def setUp(self):
        self.stub_method_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'stub',
            'method',
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

    def testCallsConfiguredMethodIfBranchEnabled(self):
        confdir = os.path.join(self.homedir, '.config', 'podpourri')
        configfile = os.path.join(confdir, 'podpourri.job.conf')
        confcmds = [
            ['git', 'config', '--file', configfile,
             'autobuild.method', 'stub'],
        ]
        os.makedirs(confdir)
        for confcmd in confcmds:
            subprocess.check_call(confcmd)

        env=self._env(PATH="".join([self.stub_method_path, os.pathsep, os.environ['PATH']]))
        output = self._wd_cmd('podpourri-schedule', 'weekly', 'git@code.example.com:my-container-image#latest', env=env)

        expect_lines = [
            b'STUB-METHOD called with args: weekly git@code.example.com:my-container-image#latest',
            b''
        ]

        self.assertEqual(output, b'\n'.join(expect_lines))
