# Copyright (c) 2016, The Regents of the University of California.
"""
Tests for syrah.
"""

import os
import subprocess
import hashlib
import tempfile
import shutil
import random

random.seed(5)

## utilities

def scriptpath(scriptname='syrah'):
    "Return the path to the syrah script, in both dev & install situations."
    path = os.path.dirname(__file__)
    if os.path.exists(os.path.join(path, scriptname)):
        return path

    path = os.path.join(os.path.dirname(__file__), "./EGG-INFO/scripts")
    if os.path.exists(os.path.join(path, scriptname)):
        return path

    for path in os.environ['PATH'].split(':'):
        if os.path.exists(os.path.join(path, scriptname)):
            return path


def run_shell_cmd(cmd, fail_ok=False, in_directory=None, inp=None):
    cwd = os.getcwd()
    if in_directory:
        os.chdir(in_directory)

    print('running: ', cmd)
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        (out, err) = proc.communicate(inp)

        out = out.decode('utf-8')
        err = err.decode('utf-8')

        if proc.returncode != 0 and not fail_ok:
            print('out:', out)
            print('err:', err)
            raise AssertionError("exit code is non zero: %d" % proc.returncode)

        return (proc.returncode, out, err)
    finally:
        os.chdir(cwd)


class TempDirectory(object):
    def __init__(self):
        self.tempdir = tempfile.mkdtemp(prefix='syrah_test_')

    def __enter__(self):
        return self.tempdir

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            shutil.rmtree(self.tempdir, ignore_errors=True)
        except OSError:
            pass

        if exc_type:
            return False


## actual tests!


def test_basic():
    # does it basically work!?
    cmd = """

        echo '>a\nAAAAAAAAAAAAAAAAAAAAA\n' |
        {scripts}/syrah

    """.format(scripts=scriptpath())
    (status, out, err) = run_shell_cmd(cmd, fail_ok=True)

    assert "(found 0; wanted 1000000)" in err
    assert not out


def test_basic_2():
    # confirm output md5sum -> correct
    cmd = """

        gunzip -c {scripts}/test-data/simple-genome-reads.fa.gz |
        {scripts}/syrah -n 1000 -k 15

    """.format(scripts=scriptpath())
    (status, out, err) = run_shell_cmd(cmd)

    x = hashlib.md5()
    x.update(out.encode('utf-8'))
    assert x.hexdigest() == '9bc85d0fd511639800ffcb13ebdb3844'


class TestKmerStuff(object):
    # confirm that syrah outputs high-abundance k-mers appropriately.

    def make_seqs(self, a_count, b_count):
        seqs = []
        for i in range(a_count):
            seqs.append('>a\nATGAGAGATGAGATGAGAGA\n')

        for i in range(b_count):
            seqs.append('>g\nGGACAGAGGAGAGACGAATG\n')

        random.shuffle(seqs)
        inp = "".join(seqs)

        return inp

    def run_cmd(self, seqs, k=21, n=1000, fail_ok=False):
        with TempDirectory() as location:
            fp = open(os.path.join(location, 'inp.fa'), 'w')
            fp.write(seqs)
            fp.close()
        
            cmd = """

               cat inp.fa | {scripts}/syrah -k {ksize} -n {n}

            """.format(scripts=scriptpath(), ksize=k, n=n)
            (status, out, err) = run_shell_cmd(cmd, fail_ok=fail_ok,
                                               in_directory = location)

        return status, out, err

    def test_nothing_returned(self):
        seqs = self.make_seqs(10, 10)
        status, out, err = self.run_cmd(seqs, fail_ok = True)

        assert status == 255
        assert not out
        assert 'found 0' in err

    def test_nothing_returned_2(self):
        seqs = self.make_seqs(10, 5)
        status, out, err = self.run_cmd(seqs, k=15, fail_ok=True)

        assert status == 255
        assert not out
        assert 'found 0' in err

    def test_single_a_returned(self):
        seqs = self.make_seqs(11, 5)
        status, out, err = self.run_cmd(seqs, k=15, fail_ok=True)

        assert status == 255
        assert out == '>0\nATGAGAGATGAGATGAGAGA\n'
        assert 'found 6' in err

    def test_double_a_returned(self):
        seqs = self.make_seqs(12, 5)
        status, out, err = self.run_cmd(seqs, k=15, fail_ok=True)

        assert status == 255
        assert out == '>0\nATGAGAGATGAGATGAGAGA\n>1\nATGAGAGATGAGATGAGAGA\n'
        assert 'found 6' in err

    def test_a_and_b_returned(self):
        seqs = self.make_seqs(11, 11)
        status, out, err = self.run_cmd(seqs, k=15, fail_ok=True)

        print(out)

        assert status == 255
        assert out == '>0\nGGACAGAGGAGAGACGAATG\n>1\nATGAGAGATGAGATGAGAGA\n'
        assert 'found 12' in err
