# coding=utf-8

import os
import pybtex.database

import livvkit
from livvkit.util import bib


DATA_DIR = os.path.join(os.path.dirname(livvkit.__file__), 'data')

KENNEDY2017_HTML = '<div class="bibliography"><h2>References</h2>' \
                    '<p>LIVVkit is an open source project licensed under a BSD 3-clause License. ' \
                    'We ask that you please acknowledge LIVVkit in any work it is used or supports. ' \
                    'In any corresponding published work, please cite: </p>' \
                    '<dl><dt>1</dt> <dd>Joseph&nbsp;H. Kennedy, ' \
                   'Andrew&nbsp;R. Bennett, Katherine&nbsp;J. Evans, Stephen Price, ' \
                   'Matthew Hoffman, William&nbsp;H. Lipscomb, Jeremy Fyke, Lauren Vargo, ' \
                   'Adrianna Boghozian, Matthew Norman, and Patrick&nbsp;H. Worley. ' \
                   'Livvkit: an extensible, python-based, land ice verification and validation ' \
                   'toolkit for ice sheet models. <em>Journal of Advances in Modeling Earth ' \
                   'Systems</em>, 9(2):854–869, 2017. ' \
                   '<a href="https://doi.org/10.1002/2017MS000916">doi:10.1002/2017MS000916</a>.' \
                   '</dd> </dl></div>'

KENNEDY2017_EVANS2019_HTML = '<div class="bibliography"><h2>References</h2>' \
                             '<p>LIVVkit is an open source project licensed under a BSD 3-clause License. ' \
                             'We ask that you please acknowledge LIVVkit in any work it is used or supports. ' \
                             'In any corresponding published work, please cite: </p>' \
                             '<dl><dt>1</dt> <dd>K.&nbsp;J. Evans, ' \
                             'J.&nbsp;H. Kennedy, D.&nbsp;Lu, M.&nbsp;M. Forrester, S.&nbsp;Price, ' \
                             'J.&nbsp;Fyke, A.&nbsp;R. Bennett, M.&nbsp;J. Hoffman, I.&nbsp;Tezaur, ' \
                             'C.&nbsp;S. Zender, and M.&nbsp;Vizca\\\'<span class="bibtex-protected">ı</span>no. ' \
                             'Livvkit 2.1: automated and extensible ice sheet model validation. ' \
                             '<em>Geoscientific Model Development</em>, 12(3):1067–1086, 2019. URL: ' \
                             '<a href="https://www.geosci-model-dev.net/12/1067/2019/">' \
                             'https://www.geosci-model-dev.net/12/1067/2019/</a>, ' \
                             '<a href="https://doi.org/10.5194/gmd-12-1067-2019">' \
                             'doi:10.5194/gmd-12-1067-2019</a>.</dd> <dt>2</dt> <dd>Joseph&nbsp;H. Kennedy, ' \
                             'Andrew&nbsp;R. Bennett, Katherine&nbsp;J. Evans, Stephen Price, Matthew Hoffman, ' \
                             'William&nbsp;H. Lipscomb, Jeremy Fyke, Lauren Vargo, Adrianna Boghozian, ' \
                             'Matthew Norman, and Patrick&nbsp;H. Worley. Livvkit: an extensible, ' \
                             'python-based, land ice verification and validation toolkit for ice sheet ' \
                             'models. <em>Journal of Advances in Modeling Earth Systems</em>, 9(2):854–869, ' \
                             '2017. <a href="https://doi.org/10.1002/2017MS000916">doi:10.1002/2017MS000916</a>.' \
                             '</dd> </dl></div>'




def test_bib2html_str():
    html = bib.bib2html(os.path.join(DATA_DIR, 'Kennedy2017.bib'))
    assert html == KENNEDY2017_HTML


def test_bib2html_list():
    html = bib.bib2html([
        os.path.join(DATA_DIR, 'Kennedy2017.bib'), os.path.join(DATA_DIR, 'Evans2019.bib')
    ])
    assert html == KENNEDY2017_EVANS2019_HTML


def test_bib2html_set():
    html = bib.bib2html({
        os.path.join(DATA_DIR, 'Kennedy2017.bib'), os.path.join(DATA_DIR, 'Evans2019.bib')
    })

    assert html == KENNEDY2017_EVANS2019_HTML


def test_bib2html_tuple():
    html = bib.bib2html((
        os.path.join(DATA_DIR, 'Kennedy2017.bib'), os.path.join(DATA_DIR, 'Evans2019.bib')
    ))

    assert html == KENNEDY2017_EVANS2019_HTML


def test_bib2html_bibliographydata():
    bibliography = pybtex.database.parse_file(os.path.join(DATA_DIR, 'Kennedy2017.bib'))

    html = bib.bib2html(bibliography)

    assert html == KENNEDY2017_HTML


def test_bib2html_duplicate_elements():
    html = bib.bib2html([
        os.path.join(DATA_DIR, 'Kennedy2017.bib'), os.path.join(DATA_DIR, 'Kennedy2017.bib')
    ])
    assert html == KENNEDY2017_HTML
