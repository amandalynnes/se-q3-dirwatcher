#!/usr/bin/env python

import unittest
import subprocess
import shlex

__author__ = 'madarp'

# invoke process
# process = subprocess.Popen(
#     shlex.split(command),
#     shell=False,
#     stdout=process.PIPE
# )

# # Poll process.stdout to show stdout live
# while process.poll() is not None:
#     output = process.stdout.readline()
#     if output:
#         print output.strip()
# rc = process.poll()

PKG_NAME = "dirwatcher"
MODULE_NAME = "dirwatcher.py"


def run_capture(cmd_string, timeout=None):
    """Runs a program for awhile in a separate process, captures output"""
    try:
        result = subprocess.run(
            shlex.split(cmd_string),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            universal_newlines=True,
            timeout=timeout
            )
    except subprocess.CalledProcessError as cpe:
        # Here we have some kind of SystemExit that was triggered.
        result = cpe
    except subprocess.TimeoutExpired as exc:
        result = exc

    # Convert bytes to utf-8
    if isinstance(result.stderr, bytes):
        result.stderr = result.stderr.decode()
    if isinstance(result.stdout, bytes):
        result.stdout = result.stdout.decode()
    return result  # see https://docs.python.org/3/library/subprocess.html#subprocess.CompletedProcess


class TestDirwatcher(unittest.TestCase):

    def test_no_arguments(self):
        """Check error message when required args are missing"""
        result = run_capture("python soln/dirwatcher.py")
        assert "error: the following arguments are required" in result.stderr

    def test_logging_to_stdout(self):
        """
        Check if log messages are going to sys.stdout
        They should be going to sys.stdout, not sys.stderr (default)
        """
        result = run_capture(
            "python soln/dirwatcher.py watchme ERROR",
            timeout=4.0)

        self.assertIsNone(
            result.stderr,
            "The program should not have generated output on stderr: %s" % result.stderr
            )

        self.assertGreater(
            len(result.stdout), 0,
            "The program did not log anything to stdout"
        )
        
    

if __name__ == '__main__':
    unittest.main()
