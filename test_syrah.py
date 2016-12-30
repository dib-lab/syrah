# Copyright (c) 2016, The Regents of the University of California.
import os
import subprocess
import hashlib

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


def test_basic_3():
    return

    # confirm that syrah outputs high-abundance k-mers
    # this does not currently work... not sure why!

    seqs = []
    for i in range(50):
        seqs.append('>a')
        seqs.append('ATGAGAGATGAGATGAGAGA')

    for i in range(5):
        seqs.append('>g')
        seqs.append('GGACAGAGGAGAGACGAATG')

    inp = "\n".join(seqs)
    print(inp)
    open('xxx', 'w').write(inp)
        
    cmd = """

        {scripts}/syrah

    """.format(scripts=scriptpath())
    (status, out, err) = run_shell_cmd(cmd, inp=inp, fail_ok=True)

    assert 0, (status, out, err)
