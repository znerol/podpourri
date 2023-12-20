import os
import shutil
import subprocess
import tempfile
import unittest


class BuildPodmanTestCase(unittest.TestCase):
    workdir = None
    repodir = None
    env = {}

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.repodir = os.path.join(self.workdir, 'my-image-repo')

        os.mkdir(self.repodir)

        self._repo_cmd('git', 'init', '-b', 'latest')
        self._repo_cmd('git', 'config', 'user.name', 'Test')
        self._repo_cmd('git', 'config', 'user.email', 'test@localhost')
        self._repo_cmd('git', 'commit', '--quiet',
                       '--allow-empty', '-m', 'Initial commit')

        bin_stub = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            'stub',
            'bin'
        )

        self.env = os.environ.copy()
        self.env.update({
            'PATH': f"{bin_stub}:{self.env['PATH']}",
        })

    def tearDown(self):
        if self.workdir is not None:
            shutil.rmtree(self.workdir)

    def _repo_cmd(self, *args, **kwds):
        kwds.setdefault('cwd', self.repodir)
        kwds.setdefault('env', self.env)
        return subprocess.check_output(args, **kwds)

    def testCallsPodmanBuildWithoutPush(self):
        with open(os.path.join(self.repodir, ".podpourri.conf"), "w") as fp:
            print("\n".join([
                "[podpourri]",
                "    image = my-container-image",
            ]), file=fp)

        output = self._repo_cmd(
            'podpourri-build', self.repodir, 'jobtag-xyz')

        expect_lines = [
            f'PODMAN build called with args: -t my-container-image:latest {self.repodir}',
            'PODMAN tag called with args: my-container-image:latest my-container-image:jobtag-xyz',
            ''
        ]

        self.assertEqual(output, '\n'.join(expect_lines).encode())

    def testCallsPodmanBuildAndPodmanPush(self):
        with open(os.path.join(self.repodir, ".podpourri.conf"), "w") as fp:
            print("\n".join([
                "[podpourri]",
                "    image = my-container-image",
                "    registryPrefix = registry.example.com/path/",
            ]), file=fp)

        output = self._repo_cmd(
            'podpourri-build', self.repodir, 'jobtag-xyz')

        expect_lines = [
            f'PODMAN build called with args: -t registry.example.com/path/my-container-image:latest {self.repodir}',
            'PODMAN tag called with args: registry.example.com/path/my-container-image:latest registry.example.com/path/my-container-image:jobtag-xyz',
            'PODMAN push called with args: registry.example.com/path/my-container-image:jobtag-xyz',
            'PODMAN push called with args: registry.example.com/path/my-container-image:latest',
            ''
        ]

        self.assertEqual(output, '\n'.join(expect_lines).encode())

    def testCallsPodmanPullAndBuildAndPush(self):
        with open(os.path.join(self.repodir, ".podpourri.conf"), "w") as fp:
            print("\n".join([
                "[podpourri]",
                "    pull = public-registry.example.com/library/base:latest",
                "    image = my-container-image",
                "    registryPrefix = registry.example.com/path/",
            ]), file=fp)

        output = self._repo_cmd(
            'podpourri-build', self.repodir, 'jobtag-xyz')

        expect_lines = [
            'PODMAN pull called with args: public-registry.example.com/library/base:latest',
            f'PODMAN build called with args: -t registry.example.com/path/my-container-image:latest {self.repodir}',
            'PODMAN tag called with args: registry.example.com/path/my-container-image:latest registry.example.com/path/my-container-image:jobtag-xyz',
            'PODMAN push called with args: registry.example.com/path/my-container-image:jobtag-xyz',
            'PODMAN push called with args: registry.example.com/path/my-container-image:latest',
            ''
        ]

        self.assertEqual(output, '\n'.join(expect_lines).encode())

    def testCallsPodmanExcludePullAndBuildAndPush(self):
        with open(os.path.join(self.repodir, ".podpourri.conf"), "w") as fp:
            print("\n".join([
                "[podpourri]",
                "    pull = public-registry.example.com/library/base:latest",
                "    pullExcludeJobPrefix = jobtag-",
                "    image = my-container-image",
                "    registryPrefix = registry.example.com/path/",
            ]), file=fp)

        output = self._repo_cmd(
            'podpourri-build', self.repodir, 'jobtag-xyz')

        expect_lines = [
            f'PODMAN build called with args: -t registry.example.com/path/my-container-image:latest {self.repodir}',
            'PODMAN tag called with args: registry.example.com/path/my-container-image:latest registry.example.com/path/my-container-image:jobtag-xyz',
            'PODMAN push called with args: registry.example.com/path/my-container-image:jobtag-xyz',
            'PODMAN push called with args: registry.example.com/path/my-container-image:latest',
            ''
        ]

        self.assertEqual(output, '\n'.join(expect_lines).encode())

    def testPreventsAccessToBuildContextOutsideWorkingDirectory(self):
        with open(os.path.join(self.repodir, ".podpourri.conf"), "w") as fp:
            print("\n".join([
                "[podpourri]",
                "    image = my-container-image",
                "",
                '[podpourri-image "my-container-image"]',
                "    context = ../../../etc",
            ]), file=fp)

        with self.assertRaises(subprocess.CalledProcessError) as processError:
            output = self._repo_cmd(
                'podpourri-build', self.repodir, 'jobtag-xyz')

        exc = processError.exception
        self.assertEqual(exc.returncode, 1)
        self.assertEqual(exc.output, b"")

    def testPreventsAccessToSymlinkedBuildContextOutsideWorkingDirectory(self):
        os.symlink("/etc", os.path.join(self.repodir, "etc"))

        with open(os.path.join(self.repodir, ".podpourri.conf"), "w") as fp:
            print("\n".join([
                "[podpourri]",
                "    image = my-container-image",
                "",
                '[podpourri-image "my-container-image"]',
                "    context = etc",
            ]), file=fp)

        with self.assertRaises(subprocess.CalledProcessError) as processError:
            output = self._repo_cmd(
                'podpourri-build', self.repodir, 'jobtag-xyz')

        exc = processError.exception
        self.assertEqual(exc.returncode, 1)
        self.assertEqual(exc.output, b"")

    def testPreventsAccessToContainerfileOutsideWorkingDirectory(self):
        privaterepo = os.path.join(self.workdir, "privaterepo")
        os.mkdir(privaterepo)
        with open(os.path.join(privaterepo, "Containerfile"), "w") as fp:
            print("FROM registry.example.com/private/app", file=fp)

        with open(os.path.join(self.repodir, ".podpourri.conf"), "w") as fp:
            print("\n".join([
                "[podpourri]",
                "    image = my-container-image",
                "",
                '[podpourri-image "my-container-image"]',
                "    containerfile = ../privaterepo/Containerfile",
            ]), file=fp)

        with self.assertRaises(subprocess.CalledProcessError) as processError:
            output = self._repo_cmd(
                'podpourri-build', self.repodir, 'jobtag-xyz')

        exc = processError.exception
        self.assertEqual(exc.returncode, 1)
        self.assertEqual(exc.output, b"")

    def testPreventsAccessToSymlinkedContainerfileOutsideWorkingDirectory(self):
        privaterepo = os.path.join(self.workdir, "privaterepo")
        os.mkdir(privaterepo)
        with open(os.path.join(privaterepo, "Containerfile"), "w") as fp:
            print("FROM registry.example.com/private/app", file=fp)

        os.symlink("../privaterepo/Containerfile", os.path.join(self.repodir, "Containerfile"))

        with open(os.path.join(self.repodir, ".podpourri.conf"), "w") as fp:
            print("\n".join([
                "[podpourri]",
                "    image = my-container-image",
                "",
                '[podpourri-image "my-container-image"]',
                "    containerfile = Containerfile",
            ]), file=fp)

        with self.assertRaises(subprocess.CalledProcessError) as processError:
            output = self._repo_cmd(
                'podpourri-build', self.repodir, 'jobtag-xyz')

        exc = processError.exception
        self.assertEqual(exc.returncode, 1)
        self.assertEqual(exc.output, b"")
