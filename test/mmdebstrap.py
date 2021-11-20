import os
import re
import shutil
import shutil
import subprocess
import tempfile
import unittest


class BuildMmdebstrapTestCase(unittest.TestCase):
    workdir = None
    repodir = None
    env = {}

    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.repodir = os.path.join(self.workdir, 'my-image-repo')

        os.mkdir(self.repodir)

        self._repo_cmd('git', 'init', '-b', 'latest')
        self._repo_cmd('git', 'config', 'user.name', 'Test')
        self._repo_cmd('git', 'config', 'user.email', 'test@localFst')
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

    def testCallsMmdebstrapdWithoutPush(self):
        shutil.copyfile(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'stub',
                'scratch',
                'dpkg.cfg'
            ),
            os.path.join(self.repodir, "dpkg.cfg")
        )
        shutil.copyfile(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'stub',
                'scratch',
                'sources.list'
            ),
            os.path.join(self.repodir, "sources.list")
        )
        with open(os.path.join(self.repodir, ".podpourri.conf"), "w") as fp:
            print("\n".join([
                "[podpourri]",
                "    image = my-container-image",
                "",
                "[podpourri-image \"my-container-image\"]",
                "    method = mmdebstrap",
                "    aptSourcesFile = sources.list",
                "    dpkgOptFile = dpkg.cfg",
            ]), file=fp)

        epoch="1234567890"
        # incorrect shasum for given epoch
        shasum="0123456789abcdef"

        output = self._repo_cmd('podpourri-build', self.repodir, 'jobtag-xyz',
                              env=dict(
                                  **self.env,
                                  SOURCE_DATE_EPOCH=epoch,
                                  PODMAN_STUB_SHA256_SUM=shasum
                              ))

        expect_lines = [
            b'PODMAN exists called with args: my-container-image:latest',
            b'PODMAN import called with args: [^ ]+ my-container-image:latest',
            b'PODMAN tag called with args: my-container-image:latest my-container-image:jobtag-xyz',
        ]

        self.assertRegex(output, b'^' + b'\n'.join(expect_lines) + b'\n$')

    def testDoesNotImportBuiltImageIfShasumMatches(self):
        shutil.copyfile(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'stub',
                'scratch',
                'dpkg.cfg'
            ),
            os.path.join(self.repodir, "dpkg.cfg")
        )
        shutil.copyfile(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                'stub',
                'scratch',
                'sources.list'
            ),
            os.path.join(self.repodir, "sources.list")
        )
        with open(os.path.join(self.repodir, ".podpourri.conf"), "w") as fp:
            print("\n".join([
                "[podpourri]",
                "    image = my-container-image",
                "",
                "[podpourri-image \"my-container-image\"]",
                "    method = mmdebstrap",
                "    aptSourcesFile = sources.list",
                "    dpkgOptFile = dpkg.cfg",
            ]), file=fp)

        epoch="1234567890"
        # correct shasum for given epoch
        shasum="e1a8cd773fb9663d7b2b71fd41f3e5b3c9b9302dda1c4b0c4a57f6af1126f89e"

        output = self._repo_cmd('podpourri-build', self.repodir, 'jobtag-xyz',
                              env=dict(
                                  **self.env,
                                  SOURCE_DATE_EPOCH=epoch,
                                  PODMAN_STUB_SHA256_SUM=shasum
                              ))

        expect_lines = [
            b'PODMAN exists called with args: my-container-image:latest',
            b'PODMAN tag called with args: my-container-image:latest my-container-image:jobtag-xyz',
        ]

        self.assertRegex(output, b'^' + b'\n'.join(expect_lines) + b'\n$')

    def testPreventsAccessToDpkgCfgOutsideWorkingDirectory(self):
        privaterepo = os.path.join(self.workdir, "privaterepo")
        os.mkdir(privaterepo)
        with open(os.path.join(privaterepo, "dpkg.cfg"), "w") as fp:
            print("", file=fp)

        with open(os.path.join(self.repodir, ".podpourri.conf"), "w") as fp:
            print("\n".join([
                "[podpourri]",
                "    image = my-container-image",
                "",
                '[podpourri-image "my-container-image"]',
                "    method = mmdebstrap",
                "    dpkgOptFile = ../privaterepo/dpkg.cfg",
            ]), file=fp)

        with self.assertRaises(subprocess.CalledProcessError) as processError:
            output = self._repo_cmd(
                'podpourri-build', self.repodir, 'jobtag-xyz')

        exc = processError.exception
        self.assertEqual(exc.returncode, 1)
        self.assertEqual(exc.output, b"")

    def testPreventsAccessToSymlinkedDpkgCfgOutsideWorkingDirectory(self):
        privaterepo = os.path.join(self.workdir, "privaterepo")
        os.mkdir(privaterepo)
        with open(os.path.join(privaterepo, "dpkg.cfg"), "w") as fp:
            print("", file=fp)

        os.symlink("../privaterepo/dpkg.cfg", os.path.join(self.repodir, "dpkg.cfg"))

        with open(os.path.join(self.repodir, ".podpourri.conf"), "w") as fp:
            print("\n".join([
                "[podpourri]",
                "    image = my-container-image",
                "",
                '[podpourri-image "my-container-image"]',
                "    method = mmdebstrap",
                "    dpkgOptFile = dpkg.cfg",
            ]), file=fp)

        with self.assertRaises(subprocess.CalledProcessError) as processError:
            output = self._repo_cmd(
                'podpourri-build', self.repodir, 'jobtag-xyz')

        exc = processError.exception
        self.assertEqual(exc.returncode, 1)
        self.assertEqual(exc.output, b"")

    def testPreventsAccessToSourcesListOutsideWorkingDirectory(self):
        privaterepo = os.path.join(self.workdir, "privaterepo")
        os.mkdir(privaterepo)
        with open(os.path.join(privaterepo, "sources.list"), "w") as fp:
            print("deb https://apt:debian@example.org/debian bullseye main", file=fp)

        with open(os.path.join(self.repodir, ".podpourri.conf"), "w") as fp:
            print("\n".join([
                "[podpourri]",
                "    image = my-container-image",
                "",
                '[podpourri-image "my-container-image"]',
                "    method = mmdebstrap",
                "    aptSourcesFile = ../privaterepo/sources.list",
            ]), file=fp)

        with self.assertRaises(subprocess.CalledProcessError) as processError:
            output = self._repo_cmd(
                'podpourri-build', self.repodir, 'jobtag-xyz')

        exc = processError.exception
        self.assertEqual(exc.returncode, 1)
        self.assertEqual(exc.output, b"")

    def testPreventsAccessToSymlinkedSourcesListOutsideWorkingDirectory(self):
        privaterepo = os.path.join(self.workdir, "privaterepo")
        os.mkdir(privaterepo)
        with open(os.path.join(privaterepo, "sources.list"), "w") as fp:
            print("deb https://apt:debian@example.org/debian bullseye main", file=fp)

        os.symlink("../privaterepo/sources.list", os.path.join(self.repodir, "sources.list"))

        with open(os.path.join(self.repodir, ".podpourri.conf"), "w") as fp:
            print("\n".join([
                "[podpourri]",
                "    image = my-container-image",
                "",
                '[podpourri-image "my-container-image"]',
                "    method = mmdebstrap",
                "    aptSourcesFile = sources.list",
            ]), file=fp)

        with self.assertRaises(subprocess.CalledProcessError) as processError:
            output = self._repo_cmd(
                'podpourri-build', self.repodir, 'jobtag-xyz')

        exc = processError.exception
        self.assertEqual(exc.returncode, 1)
        self.assertEqual(exc.output, b"")
