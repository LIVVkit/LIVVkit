# coding=utf-8

from livvkit.util import functions


def test_mkdir_p_new_dir_and_parent(tmpdir):
    testdir = tmpdir.join('mkdir_p', 'test_depth')
    functions.mkdir_p(testdir)
    assert testdir.check(dir=True) is True


def test_mkdir_p_silent_existing(tmpdir):
    testdir = tmpdir.mkdir('mkdir_p')
    functions.mkdir_p(testdir)

