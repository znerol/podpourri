import subprocess
import unittest


class XargsTestCase(unittest.TestCase):

    def testCallsSubcommandWithTagPrefix(self):
        cmd = ['podpourri-tag-xargs', 'pfx-', 'echo']

        output_first = subprocess.check_output(cmd)
        output_second = subprocess.check_output(cmd)

        self.assertTrue(output_first.startswith(b'pfx-'))
        self.assertTrue(output_second.startswith(b'pfx-'))

        self.assertNotEqual(output_first, output_second)
