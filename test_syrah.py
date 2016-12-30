# Copyright (c) 2016, The Regents of the University of California.
import os
import subprocess

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


def run_shell_cmd(cmd, fail_ok=False, in_directory=None):
    cwd = os.getcwd()
    if in_directory:
        os.chdir(in_directory)

    print('running: ', cmd)
    try:
        proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE)
        (out, err) = proc.communicate()

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
    cmd = """

        echo '>a\nAAAAAAAAAAAAAAAAAAAAA\n' |
        {scripts}/syrah

    """.format(scripts=scriptpath())
    (status, out, err) = run_shell_cmd(cmd, fail_ok=True)

    assert "(found 0; wanted 1000000)" in err
    assert not out
