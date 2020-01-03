# coding=utf-8

import pytest
import numpy as np
from collections import OrderedDict

import livvkit
from livvkit.util import functions


def test_fn_mkdir_p_new_dir_and_parent(tmpdir):
    testdir = tmpdir.join('mkdir_p', 'test_depth')
    functions.mkdir_p(str(testdir))

    assert testdir.check(dir=True) is True


def test_fn_mkdir_p_silent_existing(tmpdir):
    testdir = tmpdir.mkdir('mkdir_p')
    functions.mkdir_p(str(testdir))


def test_fn_merge_dicts():
    d1 = {'a': 0, 'b': 1, 'c': {'c0': 0, 'c1': 1, 'c2': 2}}
    d2 = {'d': 'dee', 'e': 'ee', 'f': {'f0': 'eff', 'f1': 'eeff', 'f2': 2}}
    truth = {'a': 0, 'b': 1, 'c': {'c0': 0, 'c1': 1, 'c2': 2},
             'd': 'dee', 'e': 'ee', 'f': {'f0': 'eff', 'f1': 'eeff', 'f2': 2}}
    test = functions.merge_dicts(d1, d2)

    assert test == truth


def test_fn_parse_gptl(ref_data):
    timing_file = ref_data.join('titan-gnu', 'CISM_glissade',
                                'dome', 'dome', 's0', 'p1',
                                'dome.0031.p001.cism_timing_stats')
    timing_results = functions.parse_gptl(str(timing_file), ['cism'])

    assert timing_results['cism'] == pytest.approx(66.73883)


def test_fn_find_file(ref_data):
    search_dir = ref_data.join('titan-gnu', 'CISM_glissade',
                               'dome', 'dome', 's0', 'p1')
    found_file = functions.find_file(str(search_dir), '*.cism_timing_stats')

    assert found_file == search_dir.join('dome.0031.p001.cism_timing_stats')


def test_fn_sort_processor_counts_good():
    base = [(0, ''), (0, ''), (256, ''), (2, '-z80'), (700, '-z5000')]
    truth = [p for p, z in base]
    test = [functions.sort_processor_counts('p{}{}'.format(p, z)) for p, z in base]

    assert test == truth


def test_fn_sort_scale_good():
    truth = [0, 1, 27, 5000]
    test = [functions.sort_scale('s{}'.format(s)) for s in truth]

    assert test == truth


def test_fn_create_page_from_template(tmpdir):
    create_path = tmpdir.mkdir('template')
    functions.create_page_from_template('index.html', str(create_path))

    assert create_path.join('index.html').check(file=True) is True


def test_fn_read_write_json(tmpdir):
    j_path = tmpdir.join('fn_read_write_json.json')
    truth = OrderedDict([("ismip-hom-a", OrderedDict([
                                                      ("x", [0.0, 1.0]),
                                                      ("y", [0.25, 0.25]),
                                                      ("pattern", ["ExpA_Fig5_???.txt"]),
                                                      ("xlabel", ["Normalized x"]),
                                                      ("ylabel", ["Velocity (m/a)"]),
                                                      ("data_dir", "data/numerics/ismip-hom")
                                                      ]))])

    functions.write_json(truth, j_path.dirname, j_path.basename)
    test = functions.read_json(str(j_path))

    assert test == truth


def test_fn_read_write_numpy_json(tmpdir):
    j_path = tmpdir.join('fn_read_write_numpy_json.json')
    np_json = OrderedDict([("ismip-hom-a", OrderedDict([
                                                        ("x", np.array([0.0, 1.0])),
                                                        ("y", np.array([0.25, 0.25])),
                                                        ("pattern", ["ExpA_Fig5_???.txt"]),
                                                        ("xlabel", ["Normalized x"]),
                                                        ("ylabel", ["Velocity (m/a)"]),
                                                        ("data_dir", "data/numerics/ismip-hom")
                                                        ]))])

    truth = OrderedDict([("ismip-hom-a", OrderedDict([
                                                      ("x", [0.0, 1.0]),
                                                      ("y", [0.25, 0.25]),
                                                      ("pattern", ["ExpA_Fig5_???.txt"]),
                                                      ("xlabel", ["Normalized x"]),
                                                      ("ylabel", ["Velocity (m/a)"]),
                                                      ("data_dir", "data/numerics/ismip-hom")
                                                      ]))])

    functions.write_json(np_json, str(j_path.dirname), str(j_path.basename))
    test = functions.read_json(str(j_path))

    assert test == truth


def test_fn_collect_cases(ref_data):
    case_dir = ref_data.join('titan-gnu', 'CISM_glissade', 'dome')
    truth = {'s1-p1', 's1-p4', 's0-p1', 's0-p4', 's0-p2', 's0-p8', 's2-p1',
             's2-p256', 's2-p16', 's4-p256', 's3-p64', 's3-p256'}

    cases = functions.collect_cases(str(case_dir))
    test = set(cases['dome'])

    assert test == truth


def test_fn_setup_output(tmpdir):
    idir = tmpdir.join('setup_output')
    livvkit.index_dir = str(idir)
    functions.setup_output()

    test = idir.join('data.txt').readlines()[0].strip()

    assert test == livvkit.timestamp
