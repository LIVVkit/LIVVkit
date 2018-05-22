# coding=utf-8

import pytest

from livvkit.util import functions


def test_mkdir_p_new_dir_and_parent(tmpdir):
    testdir = tmpdir.join('mkdir_p', 'test_depth')
    functions.mkdir_p(testdir)

    assert testdir.check(dir=True) is True


def test_mkdir_p_silent_existing(tmpdir):
    testdir = tmpdir.mkdir('mkdir_p')
    functions.mkdir_p(testdir)


def test_parse_gptl(ref_data):
    timing_file = ref_data.join('titan-gnu', 'CISM_glissade',
                                'dome', 'dome', 's0', 'p1',
                                'dome.0031.p001.cism_timing_stats')
    timing_results = functions.parse_gptl(timing_file, ['cism'])

    assert timing_results['cism'] == pytest.approx(66.73883)


def test_find_file(ref_data):
    search_dir = ref_data.join('titan-gnu', 'CISM_glissade',
                               'dome', 'dome', 's0', 'p1')
    found_file = functions.find_file(search_dir, '*.cism_timing_stats')

    assert found_file == search_dir.join('dome.0031.p001.cism_timing_stats')
