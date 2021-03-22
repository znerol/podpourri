import os
import shutil
import subprocess
import tempfile
import unittest


class ScheduleSystemdTestCase(unittest.TestCase):
    systemctl_stub = ''
    workdir = None
    repodir = None
    clonedir = None
    homedir = None
    env = {}

    def setUp(self):
        self.systemctl_stub = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'stub',
            'systemctl'
        )

        self.workdir = tempfile.mkdtemp()
        self.repodir = os.path.join(self.workdir, 'my-container-image')

        os.mkdir(self.repodir)

        self._repo_cmd('git', 'init')
        self._repo_cmd('git', 'config', 'user.name', 'Test')
        self._repo_cmd('git', 'config', 'user.email', 'test@localhost')
        self._repo_cmd('git', 'symbolic-ref', 'HEAD', 'refs/heads/latest')
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

    def testNoCallsToSystemctlUnlessConfigured(self):
        output = self._wd_cmd('podpourri-schedule-systemd',
                              self.systemctl_stub, '--user')
        self.assertEqual(output, b'')

    def testCallsSystemctlIfBranchEnabled(self):
        confdir = os.path.join(self.homedir, '.config', 'podpourri')
        configfile = os.path.join(confdir, 'podpourri.conf')
        confcmds = [
            ['git', 'config', '--file', configfile,
                'autobuild.weekly', 'develop latest'],
            ['git', 'config', '--file', configfile,
             'autobuild.prefix', 'git@code.example.com:'],
        ]
        os.makedirs(confdir)
        for confcmd in confcmds:
            subprocess.check_call(confcmd)

        output = self._wd_cmd('podpourri-schedule-systemd',
                              self.systemctl_stub, '--user')

        expect_lines = [
            b'SYSTEMCTL called with args: --user enable --now podpourri-build-weekly@git\\x40code.example.com:my\\x2dcontainer\\x2dimage\\x23latest.timer',
            b''
        ]

        self.assertEqual(output, b'\n'.join(expect_lines))
